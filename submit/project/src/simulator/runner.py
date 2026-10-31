"""Single-run CLI. Default DEBUG; never overwrites an existing result."""

import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import json
from pathlib import Path
import platform
import sys
import uuid

from . import __version__
from .cache import Cache
from .models import Config
from .trace import read_trace

ROOT = Path(__file__).resolve().parents[2]


def sha256(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_identity():
    paths = sorted((ROOT / "src").rglob("*.py")) + sorted((ROOT / "configs").glob("*.json"))
    files = {p.relative_to(ROOT).as_posix(): sha256(p) for p in paths}
    fingerprint = hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest()
    return {"version": __version__, "source_sha256": fingerprint, "files": files}


def run_trace(config, trace_path, *, warmup=10000, measured=100000,
              mode="debug", run_id=None, trace_id=None, seed=None, on_event=None):
    """Return a complete SUCCESS/FAIL record, including partial counters on failure.

    on_event is optional and streamed by the CLI. No actual data payload, latency,
    automatic final flush, generated workload, or official batch is implied.
    """
    result = {
        "schema_version": 1,
        "run_id": run_id or f"{mode.upper()}-{uuid.uuid4().hex}",
        "mode": mode, "status": "FAIL", "protocol_id": "Q10-PROTOCOL-v1.0",
        "started_at": datetime.now(timezone(timedelta(hours=7))).isoformat(timespec="seconds"),
        "config": config.snapshot(), "design_id": config.design_id,
        "trace": {"path": str(Path(trace_path).resolve()), "trace_id": trace_id, "seed": seed},
        "requested": {"warmup_accesses": warmup, "measured_accesses": measured},
        "observed": {"warmup_accesses": 0, "measured_accesses": 0},
        "model": "single-level tag/dirty/traffic; no payload, prefetch, bypass, or final flush",
        "environment": {"python": platform.python_version(), "platform": platform.platform()},
        "simulator": source_identity(),
    }
    for name, path in {
        "protocol": ROOT / "ai/inputs/experiment_protocol.md",
        "design_freeze": ROOT / "ai/AI_DESIGN_FREEZE.md",
    }.items():
        if path.is_file():
            result[name + "_sha256"] = sha256(path)
    cache = Cache(config)
    try:
        if mode not in ("debug", "official"):
            raise ValueError("Mode must be debug or official")
        if any(type(n) is not int or n < 0 for n in (warmup, measured)):
            raise ValueError("Warmup and measured counts must be nonnegative integers")
        if mode == "official" and (warmup, measured) != (10000, 100000):
            raise ValueError("Official mode requires 10000 warmup and 100000 measured accesses")
        if mode == "official" and not trace_id:
            raise ValueError("Official mode requires a frozen trace ID")
        if seed is not None and type(seed) is not int:
            raise ValueError("Seed must be an integer or absent")
        result["trace"]["sha256"] = sha256(trace_path)
        count = 0
        if warmup == 0:
            cache.begin_measurement()
        for item in read_trace(trace_path):
            if count >= warmup + measured:
                raise ValueError("Trace has more accesses than the requested complete run")
            if count == warmup and not cache.measuring:
                cache.begin_measurement()
            event = cache.access(item.operation, item.address, item.size)
            count += 1
            phase = "measured_accesses" if event.measured else "warmup_accesses"
            result["observed"][phase] += 1
            if on_event:
                on_event({"access_number": count, "trace_line": item.line_number, **event.snapshot()})
        if count != warmup + measured:
            raise ValueError(f"Trace too short: expected {warmup + measured}, found {count}")
        # Even an empty measurement period must discard warmup counters.
        if not cache.measuring:
            cache.begin_measurement()
        if sha256(trace_path) != result["trace"]["sha256"]:
            raise ValueError("Trace changed during simulation")
        cache.check_invariants()
        result["status"] = "SUCCESS"
    except (ValueError, OSError, AssertionError) as error:
        result["error"] = f"{type(error).__name__}: {error}"
    result["counters"] = cache.counters.snapshot()
    # Preserve a failed run even when the very failure was an invariant error.
    # FAIL records are diagnostic only and must never enter aggregates.
    result["metrics"] = cache.metrics(validate=False)
    result["metrics_validated"] = result["status"] == "SUCCESS"
    result["finished_at"] = datetime.now(timezone(timedelta(hours=7))).isoformat(timespec="seconds")
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--trace", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--warmup", type=int, default=10000)
    parser.add_argument("--measure", type=int, default=100000)
    parser.add_argument("--mode", choices=("debug", "official"), default="debug")
    parser.add_argument("--run-id")
    parser.add_argument("--trace-id")
    parser.add_argument("--seed", type=int)
    parser.add_argument("--events", type=Path, help="Optional per-access JSONL, including warmup")
    args = parser.parse_args(argv)
    if args.events and args.events.resolve() in (args.output.resolve(), args.trace.resolve(), args.config.resolve()):
        parser.error("Events file must differ from inputs and result")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    try:
        output = args.output.open("x", encoding="utf-8")
    except FileExistsError:
        parser.error("Result exists; choose a new output path/run ID")
    events = None
    try:
        config = Config.load(args.config)
        if args.events:
            args.events.parent.mkdir(parents=True, exist_ok=True)
            events = args.events.open("x", encoding="utf-8")
        callback = (lambda e: events.write(json.dumps(e) + "\n")) if events else None
        result = run_trace(config, args.trace, warmup=args.warmup, measured=args.measure,
                           mode=args.mode, run_id=args.run_id, trace_id=args.trace_id,
                           seed=args.seed, on_event=callback)
        result["config_file"] = {"path": str(args.config.resolve()), "sha256": sha256(args.config)}
    except (ValueError, OSError, TypeError) as error:
        result = {"status": "FAIL", "mode": args.mode, "error": f"{type(error).__name__}: {error}"}
    finally:
        if events:
            events.close()
    with output:
        json.dump(result, output, ensure_ascii=False, indent=2, allow_nan=False)
        output.write("\n")
    print(f"{result['status']}: {args.output}")
    return 0 if result["status"] == "SUCCESS" else 1


if __name__ == "__main__":
    sys.exit(main())
