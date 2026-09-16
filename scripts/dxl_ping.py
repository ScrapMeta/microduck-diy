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

Dependency: none on Linux. Protocol 2.0 (packets + CRC-16) is implemented in this
file, so there is no SDK version to drift. The serial handle prefers `pyserial` when
it is importable and otherwise falls back to a stdlib `termios` backend - a freshly
flashed Zero 3W has neither `pyserial` nor `python3 -m pip`, so requiring the package
would make the bench procedure unrunnable there. Run `self-test` to prove the codec
with no hardware and no dependencies at all.

    python3 dxl_ping.py self-test
    python3 dxl_ping.py scan  --port COM7
    python3 dxl_ping.py info  --port COM7 --id 1
    python3 dxl_ping.py probe --port COM7

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
import os
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

# Some DXL-2.0-compatible servos insert a constant byte between LEN and ERROR.
# Observed value on the XL330-CN bench kit (Issue #4, 2026-09-16).
STATUS_PREFIX_BYTE = 0x55

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
    frame = HEADER + body
    # CRC-16/IBM covers the whole packet from the header through the last parameter.
    return frame + update_crc(0, frame).to_bytes(2, "little")


class Status:
    __slots__ = ("dxl_id", "error", "params", "raw", "prefix")

    def __init__(self, dxl_id: int, error: int, params: bytes, raw: bytes):
        self.dxl_id = dxl_id
        self.error = error
        self.params = params
        self.raw = raw
        # Set when a non-standard status prefix byte was present (see Bus._read_status).
        self.prefix = None

    @property
    def alert(self) -> bool:
        return bool(self.error & 0x80)

    def __repr__(self) -> str:
        return f"Status(id={self.dxl_id}, error=0x{self.error:02X}, params={self.params.hex()})"


# --------------------------------------------------------------------------- serial


class TermiosSerial:
    """Minimal pyserial-compatible handle built on termios (Linux, stdlib only).

    `pip` is not always present on a freshly flashed board - on the Zero 3W there is
    no `pyserial` *and* `python3 -m pip` is missing, while `apt install python3-serial`
    needs root. Termios is in the stdlib, so the bench script still runs on the target
    without installing anything.
    """

    _BAUD_ATTR = {
        9600: "B9600",
        57600: "B57600",
        115200: "B115200",
        1000000: "B1000000",
        2000000: "B2000000",
        3000000: "B3000000",
        4000000: "B4000000",
    }

    def __init__(self, port: str, baud: int, timeout: float = 0.05):
        import select
        import termios

        self._os = os
        self._select = select
        self._termios = termios
        self.timeout = timeout

        attr = self._BAUD_ATTR.get(baud)
        if attr is None or not hasattr(termios, attr):
            raise RuntimeError(f"termios backend cannot set {baud} bps on this system")

        self.fd = os.open(port, os.O_RDWR | os.O_NOCTTY)
        try:
            iflag, oflag, cflag, lflag, _ispeed, _ospeed, cc = termios.tcgetattr(self.fd)

            iflag = 0  # raw: no IXON/IXOFF/IXANY, no CR/LF translation
            oflag = 0
            lflag = 0

            # 8N1, ignore modem control lines (the bus is half-duplex TTL).
            cflag = termios.CS8 | termios.CREAD | termios.CLOCAL
            if hasattr(termios, "CRTSCTS"):
                cflag &= ~termios.CRTSCTS

            speed = getattr(termios, attr)
            cc = list(cc)
            cc[termios.VMIN] = 0  # pure timed reads, like pyserial
            cc[termios.VTIME] = 0
            termios.tcsetattr(
                self.fd,
                termios.TCSANOW,
                [iflag, oflag, cflag, lflag, speed, speed, cc],
            )
            termios.tcflush(self.fd, termios.TCIFLUSH)
        except Exception:
            os.close(self.fd)
            self.fd = -1
            raise

    def read(self, size: int = 1) -> bytes:
        """Pyserial semantics: up to `size` bytes, give up once `timeout` expires."""
        data = bytearray()
        deadline = time.monotonic() + self.timeout
        while len(data) < size:
            remain = deadline - time.monotonic()
            if remain <= 0:
                break
            try:
                ready, _, _ = self._select.select([self.fd], [], [], remain)
            except (OSError, ValueError):
                break
            if not ready:
                break
            try:
                chunk = self._os.read(self.fd, size - len(data))
            except OSError:
                break
            if not chunk:
                break
            data += chunk
        return bytes(data)

    def write(self, data: bytes) -> int:
        written = 0
        while written < len(data):
            try:
                written += self._os.write(self.fd, data[written:])
            except OSError:
                break
        return written

    def reset_input_buffer(self) -> None:
        try:
            self._termios.tcflush(self.fd, self._termios.TCIFLUSH)
        except Exception:
            pass

    def close(self) -> None:
        if self.fd >= 0:
            try:
                self._os.close(self.fd)
            finally:
                self.fd = -1


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
            if serial is not None:
                self.ser = serial.Serial(port, baud, timeout=timeout, write_timeout=timeout)
            elif os.name == "posix":
                self.ser = TermiosSerial(port, baud, timeout=timeout)
            else:
                raise RuntimeError(
                    "pyserial is required on this platform (pip install pyserial)"
                )
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

    def _read_status(self, expect_len: int | None = None) -> Status | None:
        """Read one status packet, tolerating garbage before the header.

        `expect_len` is the DATA length the spec says this instruction returns
        (PING -> 3 = model(2) + firmware(1); READ -> the requested byte count). It
        is what lets us tell the two candidate framings apart, because both are
        numerically consistent with LEN on their own:

          standard : LEN = 1(ERROR) + DATA + 2(CRC)
          prefixed : LEN = 1(prefix) + 1(ERROR) + DATA + 2(CRC)

        Bench finding (Issue #4, 2026-09-16, /dev/ttyS2 @ 57 600): the servo shipped
        with the XL330-CN kit replies in the *prefixed* form, with a constant 0x55
        byte between LEN and ERROR. The servo's own LEN and CRC both cover that byte,
        so it is genuinely on the wire - it is not something this parser invents.
        Before this was understood every reply looked like `error=0x55` with every
        register shifted one byte, which reads as plausible-but-wrong data.
        """
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
        # CRC-16/IBM covers the header too: HEADER + ID + LEN + ERR + PARAM.
        want = update_crc(0, HEADER + frame[:-2])
        got = frame[-2] | (frame[-1] << 8)
        if want != got:
            if self.verbose:
                sys.stderr.write(f"  ! CRC mismatch: want {want:04X}, got {got:04X}\n")
            return None

        body = frame[3:-2]  # everything LEN counts, minus the 2 CRC bytes

        # standard body = ERROR + DATA          -> len == expect_len + 1
        # prefixed body = PREFIX + ERROR + DATA -> len == expect_len + 2
        # On error the servo may return no DATA at all, which makes the two lengths
        # collide; fall back to the prefix value in that case.
        prefixed = False
        if expect_len is not None and len(body) == expect_len + 2:
            prefixed = True
        elif expect_len is not None and len(body) == expect_len + 1:
            prefixed = bool(body) and body[0] == STATUS_PREFIX_BYTE
        else:
            prefixed = bool(body) and body[0] == STATUS_PREFIX_BYTE

        if prefixed:
            prefix = body[0] if body else None
            error = body[1] if len(body) > 1 else 0
            params = body[2:]
            if self.verbose:
                sys.stderr.write(
                    f"  ! non-standard status framing: prefix 0x{prefix:02X}, "
                    f"LEN = DATA + 4 (spec says + 3)\n"
                )
        else:
            prefix, error, params = None, (body[0] if body else 0), body[1:]

        raw = HEADER + frame
        if self.verbose:
            sys.stderr.write(f"  < {raw.hex(' ')}\n")
        status = Status(dxl_id, error, params, raw)
        status.prefix = prefix
        return status

    def _transact(self, dxl_id: int, instruction: int, params: bytes = b"",
                  expect_len: int | None = None) -> Status | None:
        packet = build_packet(dxl_id, instruction, params)
        if self.verbose:
            sys.stderr.write(f"  > {packet.hex(' ')}\n")
        try:
            self.ser.reset_input_buffer()
        except Exception:
            pass
        self.ser.write(packet)
        return self._read_status(expect_len=expect_len)

    def ping(self, dxl_id: int) -> Status | None:
        # A PING status returns ERROR + model number(2) + firmware version(1).
        return self._transact(dxl_id, INST_PING, expect_len=3)

    def read(self, dxl_id: int, address: int, length: int) -> Status | None:
        params = address.to_bytes(2, "little") + length.to_bytes(2, "little")
        return self._transact(dxl_id, INST_READ, params, expect_len=length)


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

    # 2) packet round-trip, anchored to a published vector.
    # The canonical DXL Protocol 2.0 PING of ID 1 is the byte string below; the CRC
    # must cover the 4-byte header too. Computing it over the body only yields
    # `... 01 3a 6c`, a packet a real servo ignores - which is exactly the kind of
    # silent failure that shows up at the bench as "no reply from the hardware".
    ping1 = build_packet(1, INST_PING)
    if ping1 != bytes.fromhex("fffffd000103000119 4e".replace(" ", "")):
        failures.append(f"PING id1 = {ping1.hex(' ')}, expected ff ff fd 00 01 03 00 01 19 4e")

    class Loopback:
        """Answers a PING as an XL330 would: id 1, no error, model 1200."""

        def __init__(self, model=MODEL_NUMBER_XL330, error=0x00):
            self.buf = bytearray()
            self.model = model
            self.error = error

        def write(self, data):
            for dxl_id, instruction, params in parse_packet(data):
                if instruction == INST_PING:
                    # Status LEN = ERROR(1) + model(2) + firmware(1) + CRC(2) = 6.
                    body = bytes([dxl_id, 0x06, 0x00, self.error]) \
                        + self.model.to_bytes(2, "little") + bytes([0x35])
                    frame = HEADER + body
                    self.buf += frame + update_crc(0, frame).to_bytes(2, "little")
                elif instruction == INST_READ:
                    body = bytes([dxl_id, 0x05, 0x00, self.error]) + (0x2C).to_bytes(2, "little")
                    frame = HEADER + body
                    self.buf += frame + update_crc(0, frame).to_bytes(2, "little")
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

    # 4) the framing this bench kit actually replies with (Issue #4, 2026-09-16).
    # These are verbatim captures from /dev/ttyS2 @ 57 600; the extra 0x55 byte
    # after LEN is on the wire and covered by the servo's own CRC.
    class Replay:
        def __init__(self, frames):
            self.frames = [bytes.fromhex(f) for f in frames]
            self.buf = bytearray()

        def write(self, data):
            self.buf += self.frames.pop(0) if self.frames else b""
            return len(data)

        def read(self, n=1):
            out = bytes(self.buf[:n])
            del self.buf[:n]
            return out

        def reset_input_buffer(self):
            pass

        def close(self):
            pass

    replay = Replay([
        # PING id 1
        "fffffd000107005500b00435b754",
        # READ(addr=0, len=2) -> model number
        "fffffd000106005500b004d47b",
        # READ(addr=7, len=1) -> id
        "fffffd0001050055000156a1",
        # READ(addr=0xFFFF, len=1) -> error reply, no DATA
        "fffffd000104005507b08c",
    ])
    bus = Bus(replay, BUS_BAUD)
    st = bus.ping(1)
    if st is None:
        failures.append("prefixed PING did not parse")
    else:
        if st.error != 0x00:
            failures.append(f"prefixed PING error = 0x{st.error:02X}, expected 0x00")
        if model_of(st) != MODEL_NUMBER_XL330:
            failures.append(f"prefixed PING model = {model_of(st)}, expected {MODEL_NUMBER_XL330}")
        if st.params[2] != 0x35:
            failures.append(f"prefixed PING firmware = {st.params[2]}, expected 0x35")

    st = bus.read(1, 0, 2)
    if st is None or st.params != bytes([0xB0, 0x04]):
        failures.append(f"prefixed READ(model,2) = {st.params.hex() if st else None}, expected b004")

    # a 1-byte register still yields exactly one byte of DATA
    st = bus.read(1, 7, 1)
    if st is None or st.params != bytes([0x01]):
        failures.append(f"prefixed READ(id,1) = {st.params.hex() if st else None}, expected 01")

    # an error reply carries no DATA, so only the prefix distinguishes the framing
    st = bus.read(1, 0xFFFF, 1)
    if st is None:
        failures.append("prefixed error reply did not parse")
    elif st.error != 0x07 or st.params != b"":
        failures.append(f"error reply = error 0x{st.error:02X} params {st.params.hex()}, "
                        f"expected 0x07 and empty")

    # 5) shutdown decode
    if decode_shutdown(53) != "InputVoltage|Overheating|ElectricalShock|Overload":
        failures.append(f"shutdown 53 decoded as {decode_shutdown(53)!r}")
    if "InputVoltage" in decode_shutdown(52):
        failures.append("shutdown 52 must NOT include InputVoltage (robotd clears bit 0)")

    if failures:
        print("self-test FAILED:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("self-test OK: CRC (bitwise == table), packet round-trip, CRC rejection, "
          "prefixed framing replay, shutdown bits")
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
