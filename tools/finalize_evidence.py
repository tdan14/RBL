"""Verify collection and package a portable evidence bundle, excluding .git/media caches."""

import csv
import json
from pathlib import Path
import platform
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
from src.simulator.runner import sha256
from prepare_experiments import audit, now, OPERATOR, write_json


def main():
    batch = json.loads((ROOT / "runs/BATCH01/summary.json").read_text(encoding="utf-8"))
    assert batch["successes"] == 96 and batch["failures"] == 0
    pre = json.loads((ROOT / "evidence/PRE_RUN_MANIFEST.json").read_text(encoding="utf-8"))
    for rel, expected in pre["files"].items(): assert sha256(ROOT / rel) == expected, rel
    with (ROOT / "runs/BATCH01/RUN_MANIFEST.csv").open(encoding="utf-8", newline="") as f: runs = list(csv.DictReader(f))
    assert len(runs) == 96 and len({r["run_id"] for r in runs}) == 96
    for r in runs: assert r["status"] == "SUCCESS" and sha256(ROOT / r["result_path"]) == r["result_sha256"]
    traces = json.loads((ROOT / "traces/manifests/manifest.json").read_text(encoding="utf-8"))
    assert len(traces["traces"]) == 24
    for trace in traces["traces"]: assert sha256(ROOT / trace["path"]) == trace["sha256"]
    row_counts = {}
    for filename, expected in [("all_runs.csv",96),("scenario_summary.csv",60),("amat_sensitivity.csv",864)]:
        with (ROOT / "results/BATCH01" / filename).open(encoding="utf-8-sig", newline="") as f: count = len(list(csv.DictReader(f)))
        assert count == expected; row_counts[filename] = count
    from importlib.metadata import version
    write_json(ROOT / "evidence/ENVIRONMENT.json", dict(recorded_at=now(), python=sys.version, executable=sys.executable,
               platform=platform.platform(), matplotlib=version("matplotlib"), numpy=version("numpy"),
               dependency_note="Simulator/generator standard library only; plotting requires matplotlib/numpy"))
    write_json(ROOT / "evidence/FINAL_VERIFICATION.json", dict(status="PASS", recorded_at=now(),operator=OPERATOR,
               executor="Codex/Python", frozen_files_verified=len(pre["files"]), trace_hashes_verified=24,
               raw_result_hashes_verified=96, run_successes=96, run_failures=0, csv_rows=row_counts,
               same_environment_replays=6, clean_copy_replays=1, AI_history_scope="Existing prompts/responses/logs; full chat export not required by user"))
    audit("EVIDENCE_VERIFIED", status="PASS", raw_results=96, traces=24, reproduction_samples=6, clean_copy_samples=1)
    selected = []
    for directory in ("src","configs","tests","tools","traces","ai","audit","evidence","runs","results","validation","reproduction"):
        for path in (ROOT / directory).rglob("*"):
            if not path.is_file() or "__pycache__" in path.parts or "clean_workspace" in path.parts: continue
            if path.name == "FINAL_CHECKSUMS.json": continue
            selected.append(path)
    selected += list(ROOT.glob("*.md")) + [ROOT / "analysis_plan.json", ROOT / ".gitignore"]
    selected = sorted(set(selected))
    hashes = {p.relative_to(ROOT).as_posix():sha256(p) for p in selected}
    write_json(ROOT / "evidence/FINAL_CHECKSUMS.json", dict(algorithm="SHA-256",created_at=now(),files=hashes,
               exclusions="manifest itself, final delivery ZIP/receipt, .git, caches, clean reproduction workspace, background paper PDFs"))
    selected.append(ROOT / "evidence/FINAL_CHECKSUMS.json")
    target=ROOT / "delivery";target.mkdir(exist_ok=True)
    archive=target / "Q10_BATCH01_evidence.zip"
    with zipfile.ZipFile(archive,"x",zipfile.ZIP_DEFLATED) as z:
        for path in selected:z.write(path,path.relative_to(ROOT))
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        # Verify packaged bytes, not merely the original files.
        import hashlib
        for name, expected in hashes.items(): assert hashlib.sha256(z.read(name)).hexdigest()==expected,name
    write_json(target / "receipt.json", dict(status="PASS",completed_at=now(),operator=OPERATOR,executor="Codex/Python",
               file=archive.name,sha256=sha256(archive),bytes=archive.stat().st_size,files=len(selected),
               note="ZIP byte integrity checked against FINAL_CHECKSUMS; no full chat export or measured sensor data claimed"))
    print("PACKAGED",archive,"files",len(selected),"bytes",archive.stat().st_size)


if __name__ == "__main__": main()
