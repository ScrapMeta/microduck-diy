#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DXL bench probe - read-only Dynamixel Protocol 2.0 scan / ping / info / probe.

Why this exists
---------------
Issue #4's bring-up procedure said "use whatever tool is on the board", which made a
result impossible to reproduce after the fact: the Dynamixel SDK zip and the Wizard
installer live in `res/` and `temp/` and are deliberately not committed. This is the
minimal, versioned replacement. It is *read-only* on purpose - it never writes ID,
baud rate or any EEPROM register, because `robotd` (and the Wizard) own those and
Issue #4 is a method audit that must not reconfigure the servo under test.

Dependency: `pyserial` only. Protocol 2.0 (packets + CRC-16) is implemented in this
file, so there is no SDK version to drift. Run `self-test` to prove the codec without
any hardware attached.

    pip install pyserial
    python dxl_ping.py self-test
    python dxl_ping.py scan  --port COM7
    python dxl_ping.py info  --port COM7 --id 1
    python dxl_ping.py probe --port COM7

The official probe order (mirrors `duck-control/src/bus.rs` `adopt`, `robotd-design`
sec 2.1)
----------------------------------------------------------------------------------
A factory-fresh XL330 answers as **ID 1 @ 57 600 baud** - neither is used on the
robot bus (which runs 1 Mbps, Protocol 2.0). So a servo that is silent at 1 Mbps is
not necessarily broken:

  1. Ping the expected IDs at **1 Mbps**.
  2. If *exactly one* expected ID is silent, look for the factory servo: first
     ID 1 at **1 Mbps**, then reopen the port at **57 600** and try ID 1.
  3. (robotd then writes the missing ID + the bus baud rate, reopens at 1 Mbps, runs
     the register check below, and **reboots the servo** - the reboot is what clears
     the latched hardware error the flash leaves set. This script stops at step 2 and
     prints what robotd would do; it does not write.)

Register check the control loop asserts, each startup:

    return_delay_time = 0    (factory 250 = 500 us of turnaround per device)
    baud_rate         = 3    (3 = 1 Mbps)
    pwm_slope         = 255  (factory 140)
    shutdown          = 52   (see below)

`shutdown` is a bitmask OR-ed into "torque off on this fault". XL330 factory default
is **53**; robotd pins **52**, which clears bit 0:

    bit0 0x01 Input Voltage Error   <- set at default 53, CLEARED by 52
    bit1       unused
    bit2 0x04 Overheating Error
    bit3       unused
    bit4 0x10 Electrical Shock Error
    bit5 0x20 Overload Error
    bit6/7     unused

So an over-voltage *shutdown* (torque off, LED flickering) happens at the factory
default 53 and is masked out once robotd has written 52. Either way the servo still
answers Ping/Read - over-voltage stops the motor, not the bus. Do not read a latched
shutdown as a zero-reply. See `wiki/concepts/dynamixel-xl330.md`.

Register addresses are from the ROBOTIS XL330-M288 eManual control table.
"""

from __future__ import annotations

import argparse
import sys
import time

try:
    import serial  # pyserial
except ImportError:  # pragma: no cover - exercised only without the dep
    serial = None


# --------------------------------------------------------------------------- codec

PROTOCOL_VERSION = 2.0
HEADER = b"\xff\xff\xfd\x00"
BROADCAST_ID = 0xFE

INST_PING = 0x01
INST_READ = 0x02

MODEL_NUMBER_XL330 = 1200

# Instruction(8) -> bps. The servo stores the index; 1 is the factory default.
BAUD_TABLE = {
    0: 9600,
    1: 57600,
    2: 115200,
    3: 1000000,
    4: 2000000,
    5: 3000000,
    6: 4000000,
}
BAUD_TO_INDEX = {v: k for k, v in BAUD_TABLE.items()}

BUS_BAUD = 1_000_000
FACTORY_ID = 1
FACTORY_BAUD = 57_600

# (address, length, unit) from the XL330-M288 control table.
REGISTERS = {
    "model_number": (0, 2, "1"),
    "firmware_version": (6, 1, "1"),
    "id": (7, 1, "1"),
    "baud_rate": (8, 1, "index"),
    "return_delay_time": (9, 1, "2us"),
    "max_voltage_limit": (32, 2, "0.1V"),
    "min_voltage_limit": (34, 2, "0.1V"),
    "pwm_limit": (36, 2, "0.113%"),
    "current_limit": (38, 2, "mA"),
    "pwm_slope": (62, 1, "1.977mV/ms"),
    "shutdown": (63, 1, "bitmask"),
    "torque_enable": (64, 1, "0/1"),
    "status_return_level": (68, 1, "0-2"),
    "hardware_error_status": (70, 1, "bitmask"),
    "present_input_voltage": (144, 2, "0.1V"),
    "present_temperature": (146, 1, "C"),
}

# The four registers robotd asserts/corrects every startup.
EXPECTED_REGISTERS = {
    "return_delay_time": 0,
    "baud_rate": 3,
    "pwm_slope": 255,
    "shutdown": 52,
}

SHUTDOWN_BITS = [
    (0x01, "InputVoltage"),
    (0x04, "Overheating"),
    (0x10, "ElectricalShock"),
    (0x20, "Overload"),
]


def update_crc(crc: int, data: bytes) -> int:
    """CRC-16/IBM (poly 0x8005, init 0), MSB-first. The DYNAMIXEL packet CRC."""
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x8005) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return crc


def _crc_table() -> list:
    """Independent, table-driven construction of the same CRC, for `self-test`."""
    table = []
    for i in range(256):
        crc = i << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x8005) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
        table.append(crc)
    return table


_CRC_TABLE = _crc_table()


def table_crc(crc: int, data: bytes) -> int:
    for byte in data:
        crc = ((crc << 8) & 0xFFFF) ^ _CRC_TABLE[((crc >> 8) ^ byte) & 0xFF]
    return crc


def build_packet(dxl_id: int, instruction: int, params: bytes = b"") -> bytes:
    # LEN counts Instruction + Parameter + CRC, so it is len(params) + 3, not len(params).
    length = len(params) + 3
    body = bytes([dxl_id]) + length.to_bytes(2, "little") + bytes([instruction]) + params
    return HEADER + body + update_crc(0, body).to_bytes(2, "little")


class Status:
    __slots__ = ("dxl_id", "error", "params", "raw")

    def __init__(self, dxl_id: int, error: int, params: bytes, raw: bytes):
        self.dxl_id = dxl_id
        self.error = error
        self.params = params
        self.raw = raw

    @property
    def alert(self) -> bool:
        return bool(self.error & 0x80)

    def __repr__(self) -> str:
        return f"Status(id={self.dxl_id}, error=0x{self.error:02X}, params={self.params.hex()})"


# --------------------------------------------------------------------------- serial


class Bus:
    """Thin Protocol 2.0 client. `port` may be a path or an injected object (tests).

    Read-only: only PING and READ instruction packets are ever built.
    """

    def __init__(self, port: str, baud: int, timeout: float = 0.05, verbose: bool = False):
        self.port = port
        self.baud = baud
        self.timeout = timeout
        self.verbose = verbose
        if isinstance(port, str):
            if serial is None:
                raise RuntimeError("pyserial is required: pip install pyserial")
            self.ser = serial.Serial(port, baud, timeout=timeout, write_timeout=timeout)
        else:  # already an open, duck-typed serial handle (used by self-test)
            self.ser = port

    def close(self) -> None:
        try:
            self.ser.close()
        except Exception:
            pass

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def _read_status(self) -> Status | None:
        """Read one status packet, tolerating garbage before the header."""
        deadline = time.monotonic() + max(self.timeout, 0.02)
        buf = bytearray()
        while time.monotonic() < deadline:
            chunk = self.ser.read(1)
            if not chunk:
                continue
            buf += chunk
            if len(buf) >= 4 and bytes(buf[-4:]) == HEADER:
                break
        else:
            return None

        rest = self.ser.read(3)
        if len(rest) != 3:
            return None
        dxl_id, len_l, len_h = rest[0], rest[1], rest[2]
        body_len = len_l | (len_h << 8)
        # LEN already counts ERROR + PARAM + CRC, so this is the whole remainder.
        payload = self.ser.read(body_len)
        if len(payload) != body_len:
            return None

        frame = rest + payload
        want = update_crc(0, frame[:-2])
        got = frame[-2] | (frame[-1] << 8)
        if want != got:
            if self.verbose:
                sys.stderr.write(f"  ! CRC mismatch: want {want:04X}, got {got:04X}\n")
            return None

        error = frame[3]
        params = frame[4:-2]
        raw = HEADER + frame
        if self.verbose:
            sys.stderr.write(f"  < {raw.hex(' ')}\n")
        return Status(dxl_id, error, params, raw)

    def _transact(self, dxl_id: int, instruction: int, params: bytes = b"") -> Status | None:
        packet = build_packet(dxl_id, instruction, params)
        if self.verbose:
            sys.stderr.write(f"  > {packet.hex(' ')}\n")
        try:
            self.ser.reset_input_buffer()
        except Exception:
            pass
        self.ser.write(packet)
        return self._read_status()

    def ping(self, dxl_id: int) -> Status | None:
        return self._transact(dxl_id, INST_PING)

    def read(self, dxl_id: int, address: int, length: int) -> Status | None:
        params = address.to_bytes(2, "little") + length.to_bytes(2, "little")
        return self._transact(dxl_id, INST_READ, params)


def scan(bus: Bus, id_min: int, id_max: int) -> list:
    found = []
    for dxl_id in range(id_min, id_max + 1):
        status = bus.ping(dxl_id)
        if status is not None and status.dxl_id == dxl_id:
            found.append((dxl_id, status))
    return found


def model_of(status: Status) -> int | None:
    if len(status.params) >= 2:
        return status.params[0] | (status.params[1] << 8)
    return None


def read_scalar(bus: Bus, dxl_id: int, name: str) -> int | None:
    address, length, _unit = REGISTERS[name]
    status = bus.read(dxl_id, address, length)
    if status is None or len(status.params) < length:
        return None
    value = 0
    for i, byte in enumerate(status.params[:length]):
        value |= byte << (8 * i)
    return value


def decode_shutdown(value: int) -> str:
    on = [name for bit, name in SHUTDOWN_BITS if value & bit]
    return "|".join(on) if on else "none"


def open_bus(port: str, baud: int, timeout: float, verbose: bool) -> Bus:
    return Bus(port, baud, timeout=timeout, verbose=verbose)


# ------------------------------------------------------------------------ commands


def cmd_scan(args) -> int:
    bauds = [int(b) for b in str(args.baud).split(",")]
    total = 0
    for baud in bauds:
        print(f"scan {args.port} @ {baud} bps, id {args.id_min}..{args.id_max}"
              f"{'  (factory default)' if baud == FACTORY_BAUD else ''}")
        with open_bus(args.port, baud, args.timeout, args.verbose) as bus:
            found = scan(bus, args.id_min, args.id_max)
        if not found:
            print("  (no reply)")
        for dxl_id, status in found:
            model = model_of(status)
            tag = f"model={model}" if model is not None else "model=?"
            if model == MODEL_NUMBER_XL330:
                tag += " (XL330)"
            alert = "  ALERT(0x80 set)" if status.alert else ""
            print(f"  id {dxl_id:3d}  {tag}{alert}")
        total += len(found)
        print()
    return 0 if total else 2


def cmd_info(args) -> int:
    with open_bus(args.port, args.baud, args.timeout, args.verbose) as bus:
        if bus.ping(args.id) is None:
            print(f"id {args.id} did not answer at {args.baud} bps on {args.port}")
            return 2
        print(f"# bench baseline - id {args.id} @ {args.baud} bps, {args.port}")
        print(f"# date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        for name in REGISTERS:
            value = read_scalar(bus, args.id, name)
            if value is None:
                print(f"{name:24s} = <no reply>")
                continue
            note = ""
            if name == "baud_rate":
                note = f"  -> {BAUD_TABLE.get(value, '?')} bps"
            elif name in ("max_voltage_limit", "min_voltage_limit",
                          "present_input_voltage", "pwm_limit"):
                note = f"  -> {value / 10.0:.1f} V" if "voltage" in name else ""
            elif name == "shutdown":
                note = f"  -> latches on: {decode_shutdown(value)}"
            elif name == "hardware_error_status":
                note = f"  -> {decode_shutdown(value)}"
            elif name == "model_number" and value == MODEL_NUMBER_XL330:
                note = "  (XL330)"
            print(f"{name:24s} = {value}{note}")
        print()
        print("# robotd would assert (and correct) these:")
        for name, want in EXPECTED_REGISTERS.items():
            value = read_scalar(bus, args.id, name)
            state = "ok" if value == want else f"needs {want}"
            print(f"{name:24s} = {value}  expect {want}  [{state}]")
    return 0


def cmd_probe(args) -> int:
    expect_ids = [int(x) for x in str(args.expect).split(",") if x.strip()] if args.expect else []
    verdict = 2

    with open_bus(args.port, BUS_BAUD, args.timeout, args.verbose) as bus:
        if expect_ids:
            print(f"1) ping expected ids at {BUS_BAUD} bps: {expect_ids}")
            missing = [i for i in expect_ids if bus.ping(i) is None]
            print(f"   answered: {[i for i in expect_ids if i not in missing]}")
            print(f"   missing : {missing}")
        else:
            missing = []
            print("1) no --expect given; skipping the expected-id pass")

        # Factory servo: ID 1, first at the bus speed, then at 57 600.
        print(f"\n2) factory-servo probe: id {FACTORY_ID} at {BUS_BAUD} bps")
        status = bus.ping(FACTORY_ID)
        branch = None
        if status is not None:
            branch = f"id {FACTORY_ID} answers at {BUS_BAUD} bps (already re-flashed to the bus speed)"
            verdict = 0
            print(f"   FOUND - {branch}")
        else:
            print("   no reply")

    if verdict != 0:
        print(f"\n3) reopen at {FACTORY_BAUD} bps and try id {FACTORY_ID}")
        with open_bus(args.port, FACTORY_BAUD, args.timeout, args.verbose) as bus:
            status = bus.ping(FACTORY_ID)
            if status is not None:
                branch = f"factory-default servo: id {FACTORY_ID} @ {FACTORY_BAUD} bps"
                verdict = 0
                print(f"   FOUND - {branch}")
            else:
                print("   no reply either")

    print()
    if verdict == 0:
        print("VERDICT: a servo answered. If it answered as id 1 at 57 600, it is factory")
        print("         default: robotd would write the missing joint id, then the bus baud")
        print("         rate, reopen at 1 Mbps, run the register check and REBOOT the servo")
        print("         (the reboot clears the latched hardware error the flash leaves set).")
        print("         This script does not write - use robotd or the Wizard for that.")
    else:
        print("VERDICT: no reply at either speed on this port.")
        print("         If this is the HAT (/dev/ttyS2), the bus itself is the problem, not the")
        print("         servo's id/baud: check getty masked, console=display, fuser clean, then")
        print("         the DATA idle level and DIR. See wiki/concepts/hat-dxl-bus-debug.md.")
        print("         If this is the U2D2 bench, check servo power, 3P pin order (1=GND,")
        print("         2=VBATT, 3=DATA) and that the servo is powered at all.")
    return verdict


def cmd_self_test(args) -> int:
    failures = []

    # 1) two independent CRC implementations must agree
    vector = b"123456789"
    a, b = update_crc(0, vector), table_crc(0, vector)
    if a != b:
        failures.append(f"CRC disagreement on {vector!r}: {a:04X} != {b:04X}")
    known = 0xFEE8  # check value of CRC-16/UMTS (poly 0x8005, init 0, MSB-first)
    if a != known:
        failures.append(f"CRC of {vector!r} = {a:04X}, expected {known:04X}")

    # 2) packet round-trip through a fake serial port
    class Loopback:
        """Answers a PING as an XL330 would: id 1, no error, model 1200."""

        def __init__(self, model=MODEL_NUMBER_XL330, error=0x00):
            self.buf = bytearray()
            self.model = model
            self.error = error

        def write(self, data):
            for dxl_id, instruction, params in parse_packet(data):
                if instruction == INST_PING:
                    # Status LEN = ERROR(1) + model(2) + CRC(2) = 5.
                    body = bytes([dxl_id, 0x05, 0x00, self.error]) + self.model.to_bytes(2, "little")
                    self.buf += HEADER + body + update_crc(0, body).to_bytes(2, "little")
                elif instruction == INST_READ:
                    body = bytes([dxl_id, 0x05, 0x00, self.error]) + (0x2C).to_bytes(2, "little")
                    self.buf += HEADER + body + update_crc(0, body).to_bytes(2, "little")
            return len(data)

        def read(self, n=1):
            out = bytes(self.buf[:n])
            del self.buf[:n]
            return out

        def reset_input_buffer(self):
            pass

        def close(self):
            pass

    bus = Bus(Loopback(), BUS_BAUD)
    status = bus.ping(1)
    if status is None:
        failures.append("loopback PING did not parse")
    else:
        if status.dxl_id != 1 or status.error != 0:
            failures.append(f"loopback PING wrong header: {status!r}")
        if model_of(status) != MODEL_NUMBER_XL330:
            failures.append(f"loopback model = {model_of(status)}, expected {MODEL_NUMBER_XL330}")

    # 3) a corrupted CRC must be rejected, not returned as a status
    class Corrupt(Loopback):
        def write(self, data):
            Loopback.write(self, data)
            self.buf[-1] ^= 0xFF  # flip a CRC byte

    if Bus(Corrupt(), BUS_BAUD).ping(1) is not None:
        failures.append("a packet with a bad CRC was accepted")

    # 4) shutdown decode
    if decode_shutdown(53) != "InputVoltage|Overheating|ElectricalShock|Overload":
        failures.append(f"shutdown 53 decoded as {decode_shutdown(53)!r}")
    if "InputVoltage" in decode_shutdown(52):
        failures.append("shutdown 52 must NOT include InputVoltage (robotd clears bit 0)")

    if failures:
        print("self-test FAILED:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("self-test OK: CRC (bitwise == table), packet round-trip, CRC rejection, shutdown bits")
    return 0


def parse_packet(data: bytes):
    """Yield (id, instruction, params) for each instruction packet in *data*."""
    i = 0
    while True:
        i = data.find(HEADER, i)
        if i < 0 or i + 7 > len(data):
            return
        dxl_id = data[i + 4]
        body_len = data[i + 5] | (data[i + 6] << 8)
        end = i + 7 + body_len
        if end > len(data):
            return
        instruction = data[i + 7]
        params = data[i + 8:end - 2]  # drop the trailing CRC
        yield dxl_id, instruction, params
        i = end


# ----------------------------------------------------------------------------- main


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Read-only Dynamixel Protocol 2.0 bench probe (XL330 bring-up, Issue #4).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="examples:\n"
               "  python dxl_ping.py self-test\n"
               "  python dxl_ping.py scan  --port COM7\n"
               "  python dxl_ping.py scan  --port /dev/ttyS2 --baud 1000000,57600\n"
               "  python dxl_ping.py info  --port COM7 --id 1\n"
               "  python dxl_ping.py probe --port COM7\n",
    )
    sub = p.add_subparsers(dest="command", required=True)

    def add_port(sp):
        sp.add_argument("--port", required=True,
                        help="serial port: COM7 (U2D2) or /dev/ttyS2 (HAT/Zero)")
        sp.add_argument("--timeout", type=float, default=0.05,
                        help="per-read timeout in seconds (default 0.05)")
        sp.add_argument("-v", "--verbose", action="store_true",
                        help="print raw TX/RX hex to stderr")

    sp = sub.add_parser("self-test", help="prove the codec with no hardware attached")
    sp.set_defaults(func=cmd_self_test)

    sp = sub.add_parser("scan", help="ping every id in a range")
    add_port(sp)
    sp.add_argument("--baud", default=str(BUS_BAUD),
                    help="baud or comma list, e.g. 1000000,57600 (default 1000000)")
    sp.add_argument("--id-min", type=int, default=0)
    sp.add_argument("--id-max", type=int, default=252)
    sp.set_defaults(func=cmd_scan)

    sp = sub.add_parser("info", help="read the baseline registers of one id")
    add_port(sp)
    sp.add_argument("--id", type=int, default=FACTORY_ID)
    sp.add_argument("--baud", type=int, default=BUS_BAUD)
    sp.set_defaults(func=cmd_info)

    sp = sub.add_parser("probe", help="the official expected-id -> factory-id probe order")
    add_port(sp)
    sp.add_argument("--expect", default="",
                    help="comma list of expected ids to ping at 1 Mbps, e.g. 10,11,12")
    sp.set_defaults(func=cmd_probe)

    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
