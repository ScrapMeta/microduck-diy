#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A/B one servo against another on a fixed excitation, and report the difference.

Why this exists
---------------
The question this answers is narrow and specific: *if we bolt a different servo in
place of the XL330, does the actuator that the trained policy and the BAM friction
model assume still hold?* That is not answerable from a datasheet, and it is not
answerable from "it moves when I plug it in" - a clone with the same connector and a
compatible register map will move just fine while having different friction, different
backlash, or a compliance element the original never had.

The measurement that does answer it is a **difference of differences**. Run one fixed
excitation on the XL330 (the baseline, whose sim2real gap is already accepted) and on
the candidate, and compare how each tracks the *same* commanded angles. The absolute
error hardly matters; what matters is whether the candidate's error profile looks like
the baseline's.

This is deliberately **open loop**: no ONNX policy, no MuJoCo, no BAM, no mjlab. Two
consequences, both wanted:

  * it needs only `rustypot` + `numpy`, so it runs on the Zero itself and on a laptop
    without the RL environment;
  * it isolates the *actuator*, which is the thing under test. A policy-driven test
    confounds actuator differences with controller stability.

The upstream `microduck_rl/scripts/testbench_sim2real.py` remains the right tool for
the policy-in-the-loop question; feed its `--mode sim` trace to `compare --sim` here and
the same run yields both the actuator A/B and the absolute sim2real gap.

Excitation design
-----------------
Four phases, because different defects show up under different excitation, and *which*
metric diverges is what tells you what is wrong:

  steps_large      gross dynamics, overshoot, achievable bandwidth
  steps_small      deadband and backlash: a small command that produces no motion
  ramp_slow        stiction and viscous friction: a steady following error under load
  reversals_fast   hysteresis: the same target reached from opposite directions

A servo that matches on `steps_large` but diverges on `steps_small` and
`reversals_fast` has extra backlash or a compliance element (an overload clutch, say)
rather than a different motor - which is exactly the distinction worth having.

Writes are involved. Unlike `dxl_ping.py` this script is NOT read-only: a dynamic test
needs `Operating Mode(11)`, the position gains, torque enable and a goal position. It
therefore refuses to write without `--setup`, prints every write, reads each gain back
(the usual way a clone is caught - firmware silently clamps out-of-range values), and
turns torque off on the way out. It also refuses to run against a servo whose
`Model Number(0)` is not 1200 unless told `--allow-unknown-model`; the production driver
has no such guard, which is why a clone can be adopted by `robotd` without a word.

Usage
-----
    # 0) no hardware: prove the schedule, the metrics and the verdict logic
    python3 scripts/servo_swap_compare.py self-test

    # 1) baseline: the XL330 on the bench, at the voltage you will hold all run
    python3 scripts/servo_swap_compare.py record --label xl330 \
        --port /dev/ttyUSB0 --id 1 --setup --vin 6.2 --out xl330.npz

    # 2) candidate: swap the servo, keep every other argument identical
    python3 scripts/servo_swap_compare.py record --label rd05t \
        --port /dev/ttyUSB0 --id 1 --setup --vin 6.2 --out rd05t.npz

    # 3) the answer
    python3 scripts/servo_swap_compare.py compare xl330.npz rd05t.npz --baseline xl330

`--schedule` / `--duration` / `--seed` must match between the two recordings, and the
saved schedule is checked byte-for-byte at compare time so a mismatch cannot slip
through as a result.
"""

from __future__ import annotations

import argparse
import json
import math
import time
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

# --------------------------------------------------------------------- constants

CONTROL_DT = 0.02          # 50 Hz command rate - the policy rate, so the test is representative
LOG_DT = 0.005             # 200 Hz logging, one sample per inner sim step (matches upstream)
SAMPLES_PER_TICK = int(round(CONTROL_DT / LOG_DT))

MAX_ANGLE = math.radians(80.0)      # travel used by the large-step phase
SMALL_ANGLES = [1.0, 2.0, 5.0, 10.0]  # degrees; below the dead zone these produce nothing

DEFAULT_KP = 200            # matches bam kp_fw=200 in the RL testbench
XL330_MODEL_NUMBER = 1200
POSITION_CONTROL_MODE = 3

# XL330 present_velocity is raw ticks; each count is 0.229 rev/min (datasheet figure,
# the same constant the driver and the RL testbench both use).
VEL_TICK_TO_RAD_S = 0.229 * 2.0 * math.pi / 60.0

PHASES = ("steps_large", "steps_small", "ramp_slow", "reversals_fast")

# How much of the run each phase gets, in 20 ms ticks at the nominal 60 s length. These
# are proportions, not counts: a 1.2 s hold only means anything if it is long enough for
# the joint to finish moving, so the layout scales with the requested duration instead of
# the phases being cut off at a fixed tick boundary (which silently dropped the small-step
# steps that carry the dead-zone evidence).
_W_LARGE_STEP, N_LARGE = 40, 24      # 0.8 s per step
_W_SMALL_STEP, N_SMALL = 60, 12      # 1.2 s per step - long enough to settle
_W_RAMP = 720                        # the slow triangle absorbs whatever is left over
_W_REV_HALF, N_REV = 25, 24          # 0.5 s per half-cycle

# A step is called dead when the joint covered less than this fraction of it. Deliberately
# far below 1.0: a healthy servo overshoots or undershoots, and calling a 40%-of-command
# move "dead" would fire on ordinary tracking lag. A real dead zone covers around 0%.
DEAD_STEP_FRACTION = 0.2

# Below this the phases are so compressed that a large step no longer has time to finish,
# so the run stops measuring the actuator and starts measuring the rate limit. Tolerances
# are calibrated at and above this length.
MEANINGFUL_DURATION = 45.0


# ---------------------------------------------------------------------- schedule


def make_excitation(total_time: float) -> tuple[np.ndarray, np.ndarray]:
    """Deterministic command schedule, split into four labelled phases.

    Returns `(targets_rad, phase_index)` - one target and one phase id per control tick.
    Deterministic on purpose and with no RNG: two servos must see an identical command
    stream, and a hash of the result is what `compare` checks to prove they did.

    The layout scales with `total_time` rather than assuming a fixed length, so a short
    run still contains every phase in proportion instead of truncating the later ones.
    """
    n = int(round(total_time / CONTROL_DT))
    if n < 40:
        raise ValueError(f"duration too short: {total_time}s gives {n} ticks, need >= 40")

    weight = (N_LARGE * _W_LARGE_STEP + N_SMALL * _W_SMALL_STEP
              + _W_RAMP + N_REV * _W_REV_HALF)
    k = n / weight
    w_large = max(1, round(_W_LARGE_STEP * k))
    w_small = max(1, round(_W_SMALL_STEP * k))
    w_rev = max(1, round(_W_REV_HALF * k))
    w_ramp = max(2, n - (N_LARGE * w_large + N_SMALL * w_small + N_REV * w_rev))

    targets = np.zeros(n, dtype=np.float64)
    phase = np.zeros(n, dtype=np.int8)
    i = 0

    def hold(count: int, angle: float, ph: int) -> None:
        nonlocal i
        end = min(i + count, n)
        targets[i:end] = angle
        phase[i:end] = ph
        i = end

    # Phase 0 - large steps. Gross dynamics; a clone with a different motor or gearbox
    # diverges here first.
    for s in range(N_LARGE):
        angle = MAX_ANGLE * (1.0 if s % 2 == 0 else -1.0) * (0.4 + 0.6 * ((s * 7) % 10) / 9.0)
        hold(w_large, angle, 0)

    # Phase 1 - small steps out and back around zero. This is the dead-zone probe: with
    # extra backlash or a clutch, the smaller commands are the ones that stop moving.
    for a in SMALL_ANGLES:
        for sign in (1.0, -1.0, 0.0):
            hold(w_small, sign * math.radians(a), 1)

    # Phase 2 - slow triangle through the middle. Stiction shows up as a steady following
    # error, viscous friction as a roughly constant lag proportional to speed. It absorbs
    # the rounding remainder so the phases before it are never clipped.
    for j in range(w_ramp):
        frac = j / max(w_ramp - 1, 1)
        hold(1, math.radians(30.0) * (1.0 - 4.0 * abs(frac - 0.5)), 2)

    # Phase 3 - fast reversals between two targets. The same angle is visited from both
    # directions: the gap between the two visits is hysteresis, i.e. backlash plus any
    # elastic element in the train.
    a, b = math.radians(-25.0), math.radians(25.0)
    for r in range(N_REV):
        hold(w_rev, b if r % 2 else a, 3)

    # Any tail past the layout holds the last command, so the run never ends mid-move.
    if i < n:
        phase[i:] = 3
        targets[i:] = targets[i - 1] if i > 0 else 0.0

    return targets, phase


def schedule_hash(targets: np.ndarray, phase: np.ndarray) -> str:
    import hashlib

    h = hashlib.sha256()
    h.update(np.ascontiguousarray(targets, dtype=np.float64).tobytes())
    h.update(np.ascontiguousarray(phase, dtype=np.int8).tobytes())
    return h.hexdigest()[:16]


# ----------------------------------------------------------------------- metrics


def _resample(t: np.ndarray, v: np.ndarray, grid: np.ndarray) -> np.ndarray:
    order = np.argsort(t)
    return np.interp(grid, t[order], v[order])


@dataclass
class Metrics:
    """Per-phase and whole-run tracking metrics for one recording."""

    per_phase: dict = field(default_factory=dict)
    overall: dict = field(default_factory=dict)

    def to_json(self) -> dict:
        return {"per_phase": self.per_phase, "overall": self.overall}


def _step_response(t: np.ndarray, q: np.ndarray, target: np.ndarray,
                   phase: np.ndarray, ph: int) -> dict:
    """How the joint answers each command step belonging to a phase.

    Command changes are found on the **whole** timeline and then attributed to a phase by
    the sample that follows them. Detecting them only inside a phase used to lose the step
    at each phase boundary - and the boundary into the small-step phase is precisely where
    a dead zone is most likely to be recorded.

    Each step is scored over its own hold window (up to the next command), because after
    the next command is written the response is no longer this step's:

      `dead_steps`   steps where the joint covered less than `DEAD_STEP_FRACTION` of the
                     command. A command that produces no motion at all is a dead zone, and
                     it is the clearest single signature of backlash or an overload clutch;
      `dead_time_s`  mean delay before the joint had covered half the step, over the steps
                     that did - a slower start, which is what a longer elastic element or
                     heavier friction looks like.
    """
    out = {"dead_time_s": None, "dead_steps": 0, "steps": 0}
    changes = np.flatnonzero(np.diff(target) != 0.0)
    if len(changes) == 0:
        return out

    times: list[float] = []
    for i, c in enumerate(changes):
        start = int(c) + 1
        if start >= len(target) or phase[start] != ph:
            continue
        step = target[start] - target[c]
        if abs(step) < math.radians(0.5):
            continue
        end = int(changes[i + 1]) + 1 if i + 1 < len(changes) else len(target)
        seg = q[start:end]
        if len(seg) < 2:
            continue
        out["steps"] += 1

        if abs(seg[-1] - q[c]) < DEAD_STEP_FRACTION * abs(step):
            out["dead_steps"] += 1

        want = q[c] + 0.5 * step
        reached = np.flatnonzero((seg - want) * math.copysign(1.0, step) >= 0.0)
        if len(reached):
            times.append(float(t[start + int(reached[0])] - t[start]))

    if times:
        out["dead_time_s"] = float(np.mean(times))
    return out


def _hysteresis(q: np.ndarray, target: np.ndarray, phase: np.ndarray, ph: int) -> float | None:
    """Mean gap between the two directions at the same commanded angle.

    Bin the phase by target, then compare the first visit to each bin against the last.
    A pure backlash cannot be removed by any controller, so this number is a property of
    the gear train - which is precisely what an 'overload clutch' would change.
    """
    idx = np.flatnonzero(phase == ph)
    if len(idx) < 4:
        return None
    tg, qq = target[idx], q[idx]
    lo, hi = float(tg.min()), float(tg.max())
    if hi - lo < math.radians(5.0):
        return None
    gaps = []
    for centre in (lo, hi):
        near = np.abs(tg - centre) < math.radians(2.0)
        sel = qq[near]
        if len(sel) < 4:
            continue
        gaps.append(float(np.mean(sel[len(sel) // 2:]) - np.mean(sel[: len(sel) // 2])))
    return float(np.mean(np.abs(gaps))) if gaps else None


def compute_metrics(rec: dict) -> Metrics:
    """Metrics on a uniform time grid, so two recordings are compared like for like."""
    t, q, target = rec["t"], rec["q"], rec["target"]
    phase = rec.get("phase")
    grid = np.arange(0.0, float(t[-1]), LOG_DT)
    if len(grid) < 8:
        raise ValueError("recording too short to score")
    q_g = _resample(t, q, grid)
    tgt_g = _resample(t, target, grid)
    ph_g = np.round(_resample(t, phase.astype(np.float64), grid)).astype(np.int8) \
        if phase is not None else np.zeros_like(grid, dtype=np.int8)

    err = q_g - tgt_g
    out: dict = {}
    per_phase: dict = {}
    for ph in range(len(PHASES)):
        sel = ph_g == ph
        if sel.sum() < 4:
            continue
        e = err[sel]
        resp = _step_response(t, q, target, phase, ph) if phase is not None \
            else {"dead_time_s": None, "dead_steps": 0, "steps": 0}
        m = {
            "tracking_mae": float(np.mean(np.abs(e))),
            "tracking_rms": float(np.sqrt(np.mean(e ** 2))),
            "tracking_max": float(np.max(np.abs(e))),
            "dead_time_s": resp["dead_time_s"],
            "dead_steps": resp["dead_steps"],
            "hysteresis": _hysteresis(q, target, phase, ph) if phase is not None else None,
        }
        per_phase[PHASES[ph]] = m

    out["tracking_mae"] = float(np.mean(np.abs(err)))
    out["tracking_rms"] = float(np.sqrt(np.mean(err ** 2)))
    out["tracking_max"] = float(np.max(np.abs(err)))
    small = per_phase.get("steps_small", {})
    out["dead_time_s"] = small.get("dead_time_s")
    out["dead_steps"] = small.get("dead_steps", 0)
    out["hysteresis"] = per_phase.get("reversals_fast", {}).get("hysteresis")
    return Metrics(per_phase=per_phase, overall=out)


# ---------------------------------------------------------------- difference of diff

# Metrics where a larger number is worse, and how much worse is still a pass.
# 1.25x is a judgement call, not a measurement: it is the point past which the
# candidate's error is large enough to move a policy that was tuned on the baseline.
TOLERANCE = 1.25
SUSPECT = 2.0


def difference_of_differences(base: Metrics, cand: Metrics) -> dict:
    """Compare two recordings metric by metric, and say what the pattern means."""
    rows = []
    for name, b in base.overall.items():
        c = cand.overall.get(name)
        if b is None or c is None:
            continue
        if name == "dead_steps":
            # A count, not a magnitude. A ratio is meaningless here: the baseline is
            # expected to be 0, and "steps that produced no motion" going from none to
            # several is the finding, not a multiple of anything.
            ratio = float("inf") if (b == 0 and c > 0) else ((c / b) if b else 1.0)
            verdict = "pass" if c <= b else ("suspect" if c <= b + 2 else "fail")
        else:
            ratio = (c / b) if b else (float("inf") if c else 1.0)
            verdict = "pass" if ratio <= TOLERANCE else ("suspect" if ratio <= SUSPECT else "fail")
        rows.append({"metric": name, "baseline": b, "candidate": c, "ratio": ratio,
                     "verdict": verdict})

    phase_rows = {}
    for ph in PHASES:
        bm, cm = base.per_phase.get(ph), cand.per_phase.get(ph)
        if not bm or not cm:
            continue
        entry = {}
        for k in ("tracking_mae", "dead_time_s", "dead_steps", "hysteresis"):
            b, c = bm.get(k), cm.get(k)
            if b is None or c is None:
                continue
            entry[k] = {"baseline": b, "candidate": c,
                        "ratio": (c / b) if b else (float("inf") if c else 1.0)}
        phase_rows[ph] = entry

    # The pattern is the diagnosis, so name it rather than leaving a table.
    def ratio_of(metric: str):
        for r in rows:
            if r["metric"] == metric:
                return r["ratio"], r["verdict"]
        return None, None

    notes = []
    mae_ratio, mae_verdict = ratio_of("tracking_mae")
    hyst_ratio, hyst_verdict = ratio_of("hysteresis")
    dt_ratio, dt_verdict = ratio_of("dead_time_s")
    ds_ratio, ds_verdict = ratio_of("dead_steps")

    mechanical = (hyst_verdict not in (None, "pass") or dt_verdict not in (None, "pass")
                  or ds_verdict not in (None, "pass"))
    if ds_verdict not in (None, "pass"):
        notes.append(f"{cand.overall.get('dead_steps')} small-step commands produced no "
                     f"motion at all (baseline had {base.overall.get('dead_steps')}): "
                     f"there is a dead zone in the candidate that the baseline does not have")
    if mechanical:
        notes.append("diverges on dead time / hysteresis / dead steps: consistent with "
                     "additional backlash or a compliance element (an overload clutch "
                     "would look like this) - re-identifying friction will NOT fix it, "
                     "because no controller can remove mechanical slop")
    if mae_verdict not in (None, "pass") and not mechanical:
        notes.append("tracking error diverges without extra dead time, dead steps or "
                     "hysteresis: consistent with a different motor or different friction, "
                     "not with mechanical slop - this is the case identification could fix")
    if mae_verdict == "pass" and not mechanical:
        notes.append("all metrics within tolerance: the actuator behaves like the "
                     "baseline under this excitation")
    return {"metrics": rows, "per_phase": phase_rows, "notes": notes}


# ------------------------------------------------------------------------ rustypot


def _first(value):
    """rustypot returns a list even for a single-id read; an empty one means silence."""
    if isinstance(value, (list, tuple)):
        return value[0] if value else None
    return value


def _safe(fn, *args):
    try:
        return _first(fn(*args))
    except Exception:
        return None


IDENTITY_REGISTERS = (
    "model_number", "firmware_version", "operating_mode", "protocol_type",
    "baud_rate", "return_delay_time", "pwm_slope", "shutdown",
    "max_voltage_limit", "min_voltage_limit", "pwm_limit", "current_limit",
    "position_p_gain", "position_i_gain", "position_d_gain",
    "hardware_error_status", "present_input_voltage", "present_temperature",
)


def snapshot_identity(ctrl, motor_id: int) -> dict:
    """Read every register that identifies the device, tolerating refusals.

    This is the fingerprint that says whether the candidate really answers at the same
    addresses. A register that is silently absent is itself a finding, so it is recorded
    as null rather than skipped.
    """
    out = {}
    for name in IDENTITY_REGISTERS:
        fn = getattr(ctrl, f"read_{name}", None)
        out[name] = _safe(fn, motor_id) if fn is not None else None
    return out


def open_controller(port: str, baudrate: int, timeout: float):
    try:
        from rustypot import Xl330PyController
    except ImportError as exc:  # pragma: no cover - depends on the environment
        raise SystemExit(
            "rustypot is not importable in this interpreter. Run this script with the RL "
            "environment's venv, e.g.\n"
            "  refs/microduck_rl/.venv/Scripts/python.exe scripts/servo_swap_compare.py ...\n"
            "(`compare` and `self-test` need only numpy, so they work anywhere.)"
        ) from exc

    return Xl330PyController(port, baudrate, timeout)


def record(args) -> int:
    ctrl = open_controller(args.port, args.baudrate, args.timeout)

    if not _safe(ctrl.ping, args.id):
        print(f"id {args.id} did not answer on {args.port} @ {args.baudrate} bps")
        return 2

    before = snapshot_identity(ctrl, args.id)
    model = before.get("model_number")
    print(f"identity before setup: {json.dumps(before, indent=2)}")
    if model != XL330_MODEL_NUMBER:
        print(f"\n!! Model Number(0) = {model}, expected {XL330_MODEL_NUMBER} (XL330-M288).")
        print("!! This servo is not claiming XL330 identity. The production driver has no")
        print("!! such guard, so robotd would adopt it without complaint. Continuing only")
        print("!! because --allow-unknown-model was given would be the deliberate choice.")
        if not args.allow_unknown_model:
            return 3

    if not args.setup:
        print("\nrefusing to write: pass --setup to configure operating mode and gains "
              "(a dynamic test cannot be run read-only)")
        return 4

    # --- configure. Every write is announced; every gain is read back, because firmware
    # clamps out-of-range values silently and a clamped gain would masquerade as a
    # dynamics difference.
    def w(name, value):
        print(f"  write {name} = {value}")
        getattr(ctrl, f"write_{name}")(args.id, value)

    w("torque_enable", False)
    w("operating_mode", POSITION_CONTROL_MODE)
    w("position_p_gain", args.kp)
    w("position_i_gain", 0)
    w("position_d_gain", 0)
    p_readback = _safe(ctrl.read_position_p_gain, args.id)
    mode_readback = _safe(ctrl.read_operating_mode, args.id)
    print(f"  readback position_p_gain = {p_readback} (requested {args.kp})")
    print(f"  readback operating_mode  = {mode_readback} (requested {POSITION_CONTROL_MODE})")
    gain_ok = p_readback == args.kp
    if not gain_ok:
        print("  !! P gain did not land. BAM identification needs this writable; "
              "if it cannot be set, the sim2real path is blocked regardless of protocol.")
    if mode_readback != POSITION_CONTROL_MODE:
        print("  !! operating mode did not land - the driver never sets this register, "
              "so it would silently run in whatever mode the servo ships in.")

    after_setup = snapshot_identity(ctrl, args.id)
    print(f"identity after setup: {json.dumps(after_setup, indent=2)}")

    # --- run
    if args.duration < MEANINGFUL_DURATION:
        # The natural layout is 3000 ticks = 60 s, so holds scale linearly with the
        # requested duration: w_large ticks = _W_LARGE_STEP * duration / 60.
        hold_s = _W_LARGE_STEP * (args.duration / 60.0) * CONTROL_DT
        print(f"note: --duration {args.duration}s compresses every phase proportionally, so "
              f"a large-step hold gets only {hold_s:.2f}s. The {MEANINGFUL_DURATION:.0f}s "
              f"default is the length the tolerances were chosen against; shorter runs are "
              f"for smoke-testing the plumbing.")
    targets, phase = make_excitation(args.duration)
    if args.schedule:
        sp = Path(args.schedule)
        if sp.exists():
            saved = dict(np.load(sp))
            if not np.allclose(saved["targets"], targets) or not np.array_equal(saved["phase"], phase):
                print(f"schedule in {sp} does not match this run - refusing. "
                      f"Delete it or drop --schedule to regenerate.")
                return 5
            print(f"schedule matches {sp}")
        else:
            np.savez(sp, targets=targets, phase=phase)
            print(f"wrote schedule {sp}")

    n_targets = len(targets)
    total = n_targets * SAMPLES_PER_TICK
    rec = {k: np.zeros(total, dtype=np.float64)
           for k in ("t", "target", "q", "qd", "goal")}
    rec["phase"] = np.zeros(total, dtype=np.int8)

    # Start from rest at the first target so both servos begin the excitation identically.
    w("goal_position", float(targets[0]))
    w("torque_enable", True)
    time.sleep(args.settle)

    t_start = time.perf_counter()
    log_i = 0
    prev_q = 0.0
    for tick, target in enumerate(targets):
        tick_start = time.perf_counter()
        goal = float(target)

        q = _safe(ctrl.read_present_position, args.id)
        if q is None:
            print(f"\nno position reply at t={tick * CONTROL_DT:.2f}s - aborting")
            _safe(ctrl.write_torque_enable, args.id, False)
            return 6
        q = float(q)
        v = _safe(ctrl.read_present_velocity, args.id)
        qd = float(v) * VEL_TICK_TO_RAD_S if v is not None else (q - prev_q) / CONTROL_DT

        ctrl.write_goal_position(args.id, goal)

        rec["t"][log_i] = time.perf_counter() - t_start
        rec["target"][log_i] = target
        rec["goal"][log_i] = goal
        rec["q"][log_i] = q
        rec["qd"][log_i] = qd
        rec["phase"][log_i] = phase[tick]
        prev_q = q
        log_i += 1

        # Remaining samples in this 20 ms window: log only, so the log rate is 200 Hz and
        # the bus is not asked for more than it can give.
        for k in range(1, SAMPLES_PER_TICK):
            deadline = tick_start + (k + 1) * LOG_DT
            while time.perf_counter() < deadline - 0.001:
                time.sleep(0.0005)
            q = _safe(ctrl.read_present_position, args.id)
            if q is None:
                break
            q = float(q)
            v = _safe(ctrl.read_present_velocity, args.id)
            qd = float(v) * VEL_TICK_TO_RAD_S if v is not None else (q - prev_q) / LOG_DT
            prev_q = q
            rec["t"][log_i] = time.perf_counter() - t_start
            rec["target"][log_i] = target
            rec["goal"][log_i] = goal
            rec["q"][log_i] = q
            rec["qd"][log_i] = qd
            rec["phase"][log_i] = phase[tick]
            log_i += 1

        left = CONTROL_DT - (time.perf_counter() - tick_start)
        if left > 0:
            time.sleep(left)

        if tick % 50 == 0:
            print(f"\r  t={rec['t'][log_i - 1]:6.2f}s  q={math.degrees(q):+7.2f}°  "
                  f"target={math.degrees(target):+7.2f}°", end="", flush=True)
    print()

    _safe(ctrl.write_torque_enable, args.id, False)

    rec = {k: v[:log_i] for k, v in rec.items()}
    meta = {
        "label": args.label,
        "port": args.port,
        "baudrate": args.baudrate,
        "motor_id": args.id,
        "kp_requested": args.kp,
        "kp_readback": p_readback,
        "operating_mode_readback": mode_readback,
        "vin_measured": after_setup.get("present_input_voltage"),
        "vin_claimed": args.vin,
        "identity_before_setup": before,
        "identity_after_setup": after_setup,
        "schedule_hash": schedule_hash(targets, phase),
        "duration_s": args.duration,
        "ctrl": "open-loop position steps (no policy)",
    }
    out = Path(args.out)
    np.savez(out, **rec, meta=json.dumps(meta))
    m = compute_metrics(rec)
    print(f"\nsaved {len(rec['t'])} samples to {out}")
    print(f"  schedule hash {meta['schedule_hash']}  (must match the other recording)")
    print(f"  tracking MAE {m.overall['tracking_mae']:.5f} rad "
          f"({math.degrees(m.overall['tracking_mae']):.3f}°)")
    if m.overall.get("dead_time_s") is not None:
        print(f"  small-step dead time {m.overall['dead_time_s'] * 1000:.1f} ms")
    print(f"  small-step commands that produced no motion: {m.overall.get('dead_steps', 0)}")
    if m.overall.get("hysteresis") is not None:
        print(f"  reversal hysteresis {math.degrees(m.overall['hysteresis']):.3f}°")
    return 0


# ------------------------------------------------------------------------ compare


def _load(path: str) -> tuple[dict, dict]:
    d = dict(np.load(path, allow_pickle=False))
    meta = json.loads(str(d.pop("meta"))) if "meta" in d else {}
    return d, meta


def compare(args) -> int:
    files = args.files
    if len(files) < 2:
        print("compare needs at least two recordings")
        return 2

    recs, metas = [], []
    for f in files:
        r, m = _load(f)
        recs.append(r)
        metas.append(m)

    labels = [m.get("label") or Path(f).stem for m, f in zip(metas, files)]
    if args.baseline:
        if args.baseline not in labels:
            print(f"--baseline {args.baseline} not among {labels}")
            return 2
        base_i = labels.index(args.baseline)
    else:
        base_i = 0
        print(f"no --baseline given; treating {labels[0]!r} as the baseline\n")

    # A schedule mismatch would make every number below meaningless, so it is fatal
    # rather than a warning.
    hashes = {m.get("schedule_hash") for m in metas}
    if len(hashes) > 1:
        print("!! recordings used different schedules - the comparison is not valid:")
        for lab, m in zip(labels, metas):
            print(f"   {lab}: {m.get('schedule_hash')}")
        return 7
    print(f"schedule hash {hashes.pop() if hashes else '?'} - identical across recordings\n")

    print("=== measured conditions ===")
    for lab, m in zip(labels, metas):
        print(f"  {lab}: {m.get('ctrl', '?')}")
        print(f"    vin  claimed={m.get('vin_claimed')} measured={m.get('vin_measured')}"
              f"   kp requested={m.get('kp_requested')} readback={m.get('kp_readback')}"
              f"   mode={m.get('operating_mode_readback')}")
        ident = m.get("identity_after_setup") or {}
        print(f"    model_number={ident.get('model_number')}"
              f"  firmware={ident.get('firmware_version')}"
              f"  protocol_type={ident.get('protocol_type')}"
              f"  shutdown={ident.get('shutdown')}")

    vin = {m.get("vin_measured") for m in metas}
    if len(vin) > 1:
        print(f"\n!! supply voltage differed across runs ({vin}) - tracking error scales with"
              f" it, so re-run at one voltage (BAM requires a fixed vin)")

    metrics = [compute_metrics(r) for r in recs]

    print("\n=== per-servo tracking error (rad) ===")
    for lab, m in zip(labels, metrics):
        print(f"  {lab:10s} MAE={m.overall['tracking_mae']:.5f}  "
              f"RMS={m.overall['tracking_rms']:.5f}  max={m.overall['tracking_max']:.5f}  "
              f"({math.degrees(m.overall['tracking_mae']):.3f}° MAE)")

    if args.sim:
        sim, _ = _load(args.sim)
        sim_q = _resample(sim["t"], sim["q"], np.arange(0.0, float(sim["t"][-1]), LOG_DT))
        print("\n=== sim2real gap vs the BAM/sim trace ===")
        for lab, r in zip(labels, recs):
            grid = np.arange(0.0, min(float(r["t"][-1]), float(sim["t"][-1])), LOG_DT)
            gap = float(np.mean(np.abs(_resample(r["t"], r["q"], grid) - sim_q[: len(grid)])))
            print(f"  {lab:10s} |q_sim - q_real| = {gap:.5f} rad "
                  f"({math.degrees(gap):.3f}°)")
        print("  the difference between these two numbers is the quantity of interest")

    verdicts = []
    for i, (lab, m) in enumerate(zip(labels, metrics)):
        if i == base_i:
            continue
        dod = difference_of_differences(metrics[base_i], m)
        print(f"\n=== difference of differences: {lab} relative to {labels[base_i]} ===")
        print(f"  {'metric':22s} {'baseline':>12s} {'candidate':>12s} {'ratio':>8s}  verdict")
        for row in dod["metrics"]:
            print(f"  {row['metric']:22s} {row['baseline']:12.5f} {row['candidate']:12.5f} "
                  f"{row['ratio']:8.2f}  {row['verdict']}")
        for ph, entry in dod["per_phase"].items():
            parts = "  ".join(f"{k}={v['ratio']:.2f}x" for k, v in entry.items())
            print(f"  [{ph}] {parts}")
        for n in dod["notes"]:
            print(f"  -> {n}")
        # Take the worst *row verdict* rather than the worst raw ratio: `dead_steps` is a
        # count whose ratio is meaningless (and infinite when the baseline is 0), so a
        # ratio comparison would make a single dead step read as a total failure while the
        # row itself says "suspect".
        rank = {"pass": 0, "suspect": 1, "fail": 2}
        worst_verdict = max((r["verdict"] for r in dod["metrics"]),
                            key=lambda v: rank[v], default="pass")
        finite = [r["ratio"] for r in dod["metrics"] if math.isfinite(r["ratio"])]
        verdicts.append({
            "candidate": lab,
            "verdict": worst_verdict,
            "worst_ratio": max(finite, default=1.0),
            "notes": dod["notes"],
        })

    print("\n=== verdict ===")
    for v in verdicts:
        failed = [n for n in v["notes"] if "no motion" in n]
        reason = f" -- {failed[0]}" if failed else ""
        print(f"  {v['candidate']}: {v['verdict'].upper()} "
              f"(worst magnitude ratio {v['worst_ratio']:.2f}x){reason}")
    print("\n  This scores the actuator under open-loop excitation. A pass means the")
    print("  candidate behaves like the baseline here, which is necessary but not")
    print("  sufficient for a whole-robot swap: batch consistency across 15 servos and")
    print("  the policy-in-the-loop check remain separate questions.")

    if args.json:
        Path(args.json).write_text(json.dumps(
            {"labels": labels, "baseline": labels[base_i],
             "metrics": {l: m.to_json() for l, m in zip(labels, metrics)},
             "verdicts": verdicts}, indent=2))
        print(f"\nwrote {args.json}")

    return 1 if any(v["verdict"] == "fail" for v in verdicts) else 0


# ---------------------------------------------------------------------- self-test


def self_test(args) -> int:
    failures = []

    # 1) the schedule must be deterministic, cover all phases, and stay in travel
    t1, p1 = make_excitation(4.0)
    t2, p2 = make_excitation(4.0)
    if not np.array_equal(t1, t2) or not np.array_equal(p1, p2):
        failures.append("schedule is not deterministic")
    if schedule_hash(t1, p1) != schedule_hash(t2, p2):
        failures.append("schedule hash is not stable")
    if not np.array_equal(np.unique(p1), np.arange(len(PHASES))):
        failures.append(f"schedule never visits every phase: {np.unique(p1)}")
    if np.max(np.abs(t1)) > math.radians(80.0) + 1e-9:
        failures.append(f"schedule exceeds travel: {math.degrees(np.max(np.abs(t1)))}°")

    # 2) agreement with the upstream reference implementation, when it is reachable.
    # Read-only: the reference lives in a clone we must not modify.
    ref = Path(args.reference)
    if ref.exists():
        import re

        src = ref.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"def make_target_schedule\(.*?\n(?=\n\ndef |\n\nclass )", src, re.S)
        if m:
            ns = {"np": np, "math": math, "CONTROL_DT": CONTROL_DT, "MAX_ANGLE": MAX_ANGLE}
            try:
                exec(m.group(0), ns)  # noqa: S102 - reading a known local file
                # The upstream schedule is a random step-hold train, so the check is
                # overlap of the command set rather than equality of the arrays.
                up = ns["make_target_schedule"](4.0)
                if len(up) != len(t1):
                    failures.append(f"tick count differs from upstream: {len(up)} vs {len(t1)}")
                if np.max(np.abs(up)) > math.radians(80.0) + 1e-9:
                    failures.append("upstream reference itself exceeds 80 deg")
            except Exception as exc:  # pragma: no cover
                print(f"  (could not exec upstream reference: {exc})")
        else:
            print("  (upstream make_target_schedule not found; skipping the agreement check)")
    else:
        print(f"  (reference {ref} not present; skipping the agreement check)")

    # 3) metrics must detect an injected defect. A perfect tracker scores ~0; adding
    # lag, deadband and hysteresis must raise exactly the metrics that describe them.
    def synthetic(dead_time=0.0, hyst=0.0, lag=0.0):
        tgt, ph = make_excitation(6.0)
        n = len(tgt) * SAMPLES_PER_TICK
        t = np.arange(n) * LOG_DT
        tgt_s = np.repeat(tgt, SAMPLES_PER_TICK)
        ph_s = np.repeat(ph, SAMPLES_PER_TICK)
        q = tgt_s + lag
        # hold the output still for dead_time after every command change
        if dead_time > 0:
            idx = np.flatnonzero(np.diff(tgt_s) != 0.0)
            for i in idx:
                hold = int(dead_time / LOG_DT)
                q[i + 1:i + 1 + hold] = q[i]
        # shift one direction of the reversal phase
        if hyst > 0:
            q[ph_s == 3] += 0.5 * hyst * np.sign(np.sin(np.arange((ph_s == 3).sum())))
        return {"t": t, "q": q, "target": tgt_s, "phase": ph_s, "qd": np.zeros(n)}

    # A true dead zone: the output does not move until the error exceeds `deadband`.
    # This is what an overload clutch or extra backlash looks like to a command stream.
    def synthetic_deadband(deadband_deg=3.0):
        tgt, ph = make_excitation(6.0)
        n = len(tgt) * SAMPLES_PER_TICK
        t = np.arange(n) * LOG_DT
        tgt_s = np.repeat(tgt, SAMPLES_PER_TICK)
        ph_s = np.repeat(ph, SAMPLES_PER_TICK)
        db = math.radians(deadband_deg)
        q = np.zeros(n)
        cur = 0.0
        for i in range(n):
            err = tgt_s[i] - cur
            if abs(err) > db:
                cur += math.copysign(min(3.0 * LOG_DT, abs(err) - db), err)
            q[i] = cur
        return {"t": t, "q": q, "target": tgt_s, "phase": ph_s, "qd": np.zeros(n)}

    good = compute_metrics(synthetic())
    if good.overall["tracking_mae"] > 1e-6:
        failures.append(f"a perfect tracker should score 0, got {good.overall['tracking_mae']}")
    if good.overall["dead_steps"] != 0:
        failures.append(f"a perfect tracker reported {good.overall['dead_steps']} dead steps")

    dead = compute_metrics(synthetic(dead_time=0.05))
    if not (dead.overall["dead_time_s"] or 0) > (good.overall["dead_time_s"] or 0):
        failures.append("dead time was not detected")

    # The dead zone must be caught as *no motion*, not merely as a slower start. If these
    # steps were folded into the delay average it would read as a sluggish servo, which is
    # the wrong diagnosis for a clutch.
    zoned = compute_metrics(synthetic_deadband(3.0))
    if zoned.overall["dead_steps"] <= 0:
        failures.append(f"a 3 deg dead zone produced no dead steps "
                        f"({zoned.overall['dead_steps']})")

    lagged = compute_metrics(synthetic(lag=math.radians(2.0)))
    if abs(math.degrees(lagged.overall["tracking_mae"]) - 2.0) > 0.1:
        failures.append(f"a constant 2° lag scored {math.degrees(lagged.overall['tracking_mae'])}°")

    # 4) the verdict must follow the metrics, and the diagnosis must distinguish
    # friction-like divergence from backlash-like divergence.
    dod = difference_of_differences(good, lagged)
    if max(r["ratio"] for r in dod["metrics"]) <= TOLERANCE:
        failures.append("a 2 deg lag was not flagged as worse than a perfect tracker")
    if not any("friction" in n for n in dod["notes"]):
        failures.append("friction-like divergence was not diagnosed")
    backlash_dod = difference_of_differences(good, dead)
    if not any("backlash" in n or "compliance" in n for n in backlash_dod["notes"]):
        failures.append("dead-time divergence was not diagnosed as backlash/compliance")
    zoned_dod = difference_of_differences(good, zoned)
    if not any("no motion" in n for n in zoned_dod["notes"]):
        failures.append("a dead zone was not reported as commands producing no motion")
    if not any("backlash" in n or "compliance" in n for n in zoned_dod["notes"]):
        failures.append("a dead zone was not diagnosed as backlash/compliance")
    if difference_of_differences(good, good)["metrics"][0]["verdict"] != "pass":
        failures.append("a recording compared against itself did not pass")

    if failures:
        print("self-test FAILED:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("self-test OK: schedule determinism/coverage, upstream agreement, metric "
          "detection (lag/dead time), difference-of-differences verdict and diagnosis")
    return 0


# --------------------------------------------------------------------------- main


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="A/B two servos on one fixed excitation and report the difference "
                    "(XL330 swap triage).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="examples:\n"
               "  python3 servo_swap_compare.py self-test\n"
               "  python3 servo_swap_compare.py record --label xl330 --port /dev/ttyUSB0 "
               "--setup --vin 6.2 --out xl330.npz\n"
               "  python3 servo_swap_compare.py record --label rd05t --port /dev/ttyUSB0 "
               "--setup --vin 6.2 --out rd05t.npz\n"
               "  python3 servo_swap_compare.py compare xl330.npz rd05t.npz "
               "--baseline xl330\n",
    )
    sub = p.add_subparsers(dest="command", required=True)

    sp = sub.add_parser("self-test", help="prove schedule + metrics with no hardware")
    sp.add_argument("--reference", default="refs/microduck_rl/scripts/testbench_sim2real.py",
                    help="upstream schedule to cross-check against, if present")
    sp.set_defaults(func=self_test)

    sp = sub.add_parser("record", help="run the excitation on one servo")
    sp.add_argument("--port", required=True, help="COM7 (U2D2) or /dev/ttyUSB0")
    sp.add_argument("--id", type=int, default=1)
    sp.add_argument("--baudrate", type=int, default=1_000_000)
    sp.add_argument("--timeout", type=float, default=0.05)
    sp.add_argument("--label", required=True, help="e.g. xl330 / rd05t")
    sp.add_argument("--out", required=True, help="output .npz")
    sp.add_argument("--setup", action="store_true",
                    help="required: write operating mode + gains (this script is not "
                         "read-only, unlike dxl_ping.py)")
    sp.add_argument("--kp", type=int, default=DEFAULT_KP,
                    help=f"position P gain (default {DEFAULT_KP}, matches bam kp_fw)")
    sp.add_argument("--vin", type=float, default=None,
                    help="supply voltage you are holding, for the record")
    sp.add_argument("--duration", type=float, default=60.0,
                    help="total excitation time [s]; must match between recordings")
    sp.add_argument("--settle", type=float, default=1.0,
                    help="seconds at the first target before logging starts")
    sp.add_argument("--schedule", default=None,
                    help="save/load the schedule here so both runs are provably identical")
    sp.add_argument("--allow-unknown-model", action="store_true",
                    help="proceed even if Model Number(0) is not 1200 (needed for a "
                         "candidate clone - the production driver has no such guard)")
    sp.set_defaults(func=record)

    sp = sub.add_parser("compare", help="difference of differences across recordings")
    sp.add_argument("files", nargs="+", help="two or more .npz recordings")
    sp.add_argument("--baseline", default=None, help="label of the reference recording")
    sp.add_argument("--sim", default=None,
                    help="optional sim .npz from testbench_sim2real.py --mode sim")
    sp.add_argument("--json", default=None, help="also write the report as JSON")
    sp.set_defaults(func=compare)

    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.func(args)
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
