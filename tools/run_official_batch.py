"""Run exactly the frozen 24 x 4 matrix, preserving raw results and failures."""

import csv
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
from src.simulator.models import Config
from src.simulator.runner import run_trace, sha256, source_identity
from prepare_experiments import OPERATOR, now, audit, write_json


def main():
    frozen = json.loads((ROOT / "evidence/PRE_RUN_MANIFEST.json").read_text(encoding="utf-8"))
    for rel, expected in frozen["files"].items():
        if sha256(ROOT / rel) != expected: raise RuntimeError(f"Frozen file changed: {rel}")
    manifest = json.loads((ROOT / "traces/manifests/manifest.json").read_text(encoding="utf-8"))
    for trace in manifest["traces"]:
        if sha256(ROOT / trace["path"]) != trace["sha256"]: raise RuntimeError("Frozen trace changed")
    batch = ROOT / "runs/BATCH01"; batch.mkdir(parents=True, exist_ok=False)
    log = (batch / "batch.log").open("x", encoding="utf-8")
    run_manifest = (batch / "RUN_MANIFEST.csv").open("x", encoding="utf-8", newline="")
    fields = ["run_id", "operator", "executor", "trace_id", "design_id", "seed", "status", "started_at", "finished_at", "result_path", "result_sha256"]
    writer = csv.DictWriter(run_manifest, fieldnames=fields); writer.writeheader(); run_manifest.flush()
    audit("BATCH_STARTED", batch_id="BATCH01", planned_runs=96, status="STARTED")
    successes = failures = 0
    for trace in manifest["traces"]:
        for design in ("D0", "D1", "D2", "DAI-v1"):
            number = successes + failures + 1; ident = f"RUN-{number:06d}"
            folder = batch / ident; folder.mkdir()
            config_path = ROOT / f"configs/{design}.json"; config = Config.load(config_path)
            write_json(folder / "config.json", config.snapshot()); write_json(folder / "trace_reference.json", trace)
            began = now(); audit("RUN_STARTED", run_id=ident, trace_id=trace["trace_id"], design_id=design, status="STARTED")
            log.write(f"{began} START {ident} {trace['trace_id']} {design} operator={OPERATOR} executor=Codex/Python\n"); log.flush()
            started = time.monotonic()
            try:
                result = run_trace(config, ROOT / trace["path"], mode="official", run_id=ident,
                                   trace_id=trace["trace_id"], seed=trace["seed"])
                if result["trace"].get("sha256") != trace["sha256"]: raise RuntimeError("Run used a different trace hash")
                if result["simulator"]["source_sha256"] != manifest["simulator"]["source_sha256"]: raise RuntimeError("Source changed during batch")
            except Exception as error:
                result = dict(status="FAIL", error=f"{type(error).__name__}: {error}", mode="official",
                              run_id=ident, design_id=design, started_at=began, finished_at=now())
            result.update(operator=OPERATOR, executor="Codex / Python", workload_family=trace["family"],
                          scenario_id=trace["trace_id"].split("-S")[0], elapsed_wall_seconds=time.monotonic()-started,
                          pre_run_manifest_sha256=sha256(ROOT / "evidence/PRE_RUN_MANIFEST.json"),
                          trace_manifest_sha256=sha256(ROOT / "traces/manifests/manifest.json"))
            # Wall time is execution evidence, never a simulated hardware latency metric.
            write_json(folder / "result.json", result)
            digest = sha256(folder / "result.json")
            row = dict(run_id=ident, operator=OPERATOR, executor="Codex/Python", trace_id=trace["trace_id"],
                       design_id=design, seed=trace["seed"], status=result["status"], started_at=result["started_at"],
                       finished_at=result["finished_at"], result_path=(folder / "result.json").relative_to(ROOT).as_posix(), result_sha256=digest)
            writer.writerow(row); run_manifest.flush()
            if result["status"] == "SUCCESS": successes += 1
            else: failures += 1
            with (folder / "run.log").open("x", encoding="utf-8") as f:
                f.write(json.dumps({**row, "trace_sha256": trace["sha256"], "config": config.snapshot(),
                                    "requested_warmup": 10000, "requested_measured": 100000,
                                    "counters": result.get("counters"), "error": result.get("error")}, ensure_ascii=False, indent=2))
            audit("RUN_FINISHED", run_id=ident, trace_id=trace["trace_id"], design_id=design,
                  status=result["status"], result_sha256=digest, path=row["result_path"])
            message = f"{result['finished_at']} {number}/96 {ident} {trace['trace_id']} {design} {result['status']}"
            log.write(message + "\n"); log.flush(); print(message, flush=True)
    run_manifest.close(); log.close()
    # Verify inputs still match after the entire batch.
    for rel, expected in frozen["files"].items():
        if sha256(ROOT / rel) != expected: raise RuntimeError(f"Frozen file changed during batch: {rel}")
    write_json(batch / "summary.json", dict(batch_id="BATCH01", status="SUCCESS" if successes == 96 else "FAIL",
               operator=OPERATOR, executor="Codex/Python", finished_at=now(), successes=successes, failures=failures,
               planned_runs=96, note="Raw run JSON/logs never overwritten; failures retained, no automatic tuning/retries"))
    audit("BATCH_FINISHED", status="SUCCESS" if successes == 96 else "FAIL", successes=successes, failures=failures)
    return 0 if successes == 96 else 1


if __name__ == "__main__": raise SystemExit(main())
