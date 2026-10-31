"""Replay a collected run to a NEW output, comparing scientific fields only."""

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.simulator.models import Config
from src.simulator.runner import run_trace, sha256, source_identity


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not args.run_id.startswith("RUN-") or not args.run_id[4:].isdigit(): parser.error("Invalid run ID")
    folder = ROOT / "runs/BATCH01" / args.run_id
    original = json.loads((folder / "result.json").read_text(encoding="utf-8"))
    trace = json.loads((folder / "trace_reference.json").read_text(encoding="utf-8"))
    config = Config(**json.loads((folder / "config.json").read_text(encoding="utf-8")))
    if sha256(ROOT / trace["path"]) != trace["sha256"]: raise RuntimeError("Trace modified")
    if source_identity()["source_sha256"] != original["simulator"]["source_sha256"]: raise RuntimeError("Simulator source changed")
    if args.output.exists(): parser.error("Choose a new output; never overwrite evidence")
    result = run_trace(config, ROOT / trace["path"], mode="debug", run_id="REPLAY-" + args.run_id,
                       trace_id=trace["trace_id"], seed=trace["seed"])
    fields = ("counters", "metrics", "config", "observed")
    checks = {field: result[field] == original[field] for field in fields}
    checks["trace_sha256"] = result["trace"]["sha256"] == original["trace"]["sha256"]
    matched = result["status"] == "SUCCESS" and all(checks.values())
    result["reproduction"] = dict(original_run=args.run_id, original_result_sha256=sha256(folder / "result.json"),
                                   comparison=checks, matches_original=matched,
                                   note="Debug replay, not a new independent experimental sample")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", encoding="utf-8") as f: json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"{'MATCH' if matched else 'MISMATCH'} {args.run_id}: {args.output}")
    return 0 if matched else 1


if __name__ == "__main__": raise SystemExit(main())
