"""Reproduce automated validation; all results are DEBUG, never official runs."""

from datetime import datetime, timedelta, timezone
import hashlib
import io
import json
from pathlib import Path
import platform
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.simulator.models import Config
from src.simulator.runner import run_trace, sha256, source_identity
from tests.reference import ReferenceCache
from src.simulator.trace import read_trace


def main():
    now = datetime.now(timezone(timedelta(hours=7)))
    folder = ROOT / "validation" / now.strftime("check_%Y%m%d_%H%M%S_%f")
    folder.mkdir(parents=True, exist_ok=False)
    suite = unittest.defaultTestLoader.discover(str(ROOT / "tests"), top_level_dir=str(ROOT))
    stream = io.StringIO()
    tests = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    (folder / "test_report.txt").write_text(stream.getvalue(), encoding="utf-8")
    print(stream.getvalue())
    comparisons = []
    scenarios = [("repeat", 0, 2), ("lru", 0, 5), ("dirty", 0, 4),
                 ("boundary", 0, 3), ("warmup", 3, 2)]
    for design in ("D0", "D1", "D2", "DAI-v1"):
        config = Config.load(ROOT / f"configs/{design}.json")
        for scenario, warmup, measured in scenarios:
            path = ROOT / f"traces/debug/{scenario}.trace"
            events = []
            result = run_trace(config, path, warmup=warmup, measured=measured,
                               run_id=f"DEBUG-{design}-{scenario}", trace_id=f"DEBUG-{scenario}", on_event=events.append)
            # Oracle uses full block IDs/list recency and no compressed tag reconstruction.
            oracle = ReferenceCache(config)
            expected_hits = expected_misses = expected_evictions = expected_wb = 0
            expected_events = []
            for i, item in enumerate(read_trace(path)):
                hit, victim, wb = oracle.access(item.operation, item.address)
                expected_events.append((hit, victim, wb))
                if i >= warmup:
                    expected_hits += int(hit)
                    expected_misses += int(not hit)
                    expected_evictions += int(victim is not None)
                    expected_wb += int(wb is not None)
            expected = {"hits": expected_hits, "misses": expected_misses,
                        "evictions": expected_evictions, "dirty_writebacks": expected_wb}
            event_match = [(e["hit"], e["victim_block"], e["writeback_base"]) for e in events] == expected_events
            passed = result["status"] == "SUCCESS" and event_match and all(result["counters"][k] == v for k, v in expected.items())
            comparisons.append({"design": design, "scenario": scenario, "status": "PASS" if passed else "FAIL",
                                "expected": expected, "actual": {k: result["counters"][k] for k in expected},
                                "all_events_match": event_match})
            (folder / f"{design}_{scenario}.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            (folder / f"{design}_{scenario}.events.jsonl").write_text(
                "".join(json.dumps(e) + "\n" for e in events), encoding="utf-8")
    passed = tests.wasSuccessful() and all(c["status"] == "PASS" for c in comparisons)
    report = {"status": "PASS" if passed else "FAIL", "recorded_at": now.isoformat(),
              "scope": "AI-assisted automated implementation validation; no human sign-off, Ripes, W1-W5 official traces or benchmarks",
              "unit_tests": tests.testsRun, "unit_failures": len(tests.failures), "unit_errors": len(tests.errors),
              "comparison_count": len(comparisons), "comparisons": comparisons,
              "source": source_identity(), "python": sys.version, "platform": platform.platform()}
    (folder / "summary.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # Freeze a reproducible snapshot including tests, oracle, runner inputs and evidence.
    inputs = list((ROOT / "src").rglob("*.py")) + list((ROOT / "tests").glob("*.py"))
    inputs += list((ROOT / "configs").glob("*.json")) + list((ROOT / "traces/debug").glob("*.trace"))
    inputs += [Path(__file__), ROOT / "ai/AI_DESIGN_FREEZE.md", ROOT / "experiment_protocol.md"]
    paths = inputs + list(folder.glob("*"))
    manifest = {str(p.relative_to(ROOT)).replace("\\", "/"): sha256(p) for p in sorted(paths)}
    (folder / "checksums.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (ROOT / "validation/LATEST.txt").write_text(folder.name + "\n", encoding="utf-8")
    print(f"{report['status']}: {tests.testsRun} unit tests, {len(comparisons)} trace/config comparisons")
    print(folder)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
