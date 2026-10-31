import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from src.simulator.models import Config
from src.simulator.runner import ROOT, run_trace
from src.simulator.trace import read_trace


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        self.config = Config.load(ROOT / "configs/DAI-v1.json")

    def trace(self, text):
        p = self.folder / "input.trace"
        p.write_text(text, encoding="utf-8")
        return p

    def test_parser_comments_hex_decimal_and_line_numbers(self):
        path = self.trace("# note\n\nR 0x0000001c 4 # line end\nW 00032 4\n")
        accesses = list(read_trace(path))
        self.assertEqual([(a.operation, a.address, a.line_number) for a in accesses], [("R", 28, 3), ("W", 32, 4)])

    def test_parser_rejects_bad_lines_without_silent_skipping(self):
        for text in ("R 0 4\nR 2 4", "R 0 4 extra", "r 0 4", "R 0 8", "R 0x100000000 4", "R abc 4"):
            with self.subTest(text=text), self.assertRaisesRegex(ValueError, "line"):
                list(read_trace(self.trace(text)))

    def test_runner_warmup_events_and_reproducible_counters(self):
        path = self.trace("W 0 4\nR 2080 4\nR 0 4\nR 4160 4\nR 0 4\n")
        events = []
        a = run_trace(self.config, path, warmup=3, measured=2, on_event=events.append)
        b = run_trace(self.config, path, warmup=3, measured=2)
        self.assertEqual(a["status"], "SUCCESS")
        self.assertEqual(a["observed"], {"warmup_accesses": 3, "measured_accesses": 2})
        self.assertEqual(a["counters"]["hits"], 1)
        self.assertEqual(a["counters"], b["counters"])
        self.assertEqual([e["measured"] for e in events], [False] * 3 + [True] * 2)
        self.assertEqual(a["trace"]["sha256"], b["trace"]["sha256"])
        self.assertEqual(a["simulator"]["source_sha256"], b["simulator"]["source_sha256"])

    def test_short_extra_invalid_and_missing_trace_fail(self):
        for text, n in [("R 0 4\n", 2), ("R 0 4\nR 32 4\n", 1), ("R 0 4\nR 2 4\n", 2)]:
            with self.subTest(text=text, n=n):
                r = run_trace(self.config, self.trace(text), warmup=0, measured=n)
                self.assertEqual(r["status"], "FAIL")
                self.assertIn("error", r)
        self.assertEqual(run_trace(self.config, self.folder / "missing", warmup=0, measured=1)["status"], "FAIL")

    def test_zero_measurement_and_no_flush(self):
        r = run_trace(self.config, self.trace("W 0 4\n"), warmup=1, measured=0)
        self.assertEqual(r["status"], "SUCCESS")
        self.assertIsNone(r["metrics"]["miss_rate"])
        self.assertEqual(r["metrics"]["memory_traffic_bytes"], 0)
        r = run_trace(self.config, self.trace("W 0 4\n"), warmup=0, measured=1)
        self.assertEqual(r["counters"]["dirty_writebacks"], 0)
        self.assertEqual(r["metrics"]["memory_traffic_bytes"], 32)

    def test_invalid_periods_and_official_sizes_are_rejected(self):
        path = self.trace("")
        for kwargs in ({"warmup": -1}, {"measured": True}, {"mode": "unknown"},
                       {"mode": "official", "warmup": 0, "measured": 0},
                       {"mode": "official"}, {"seed": "1"}):
            with self.subTest(kwargs=kwargs):
                self.assertEqual(run_trace(self.config, path, **kwargs)["status"], "FAIL")

    def test_protocol_sized_debug_run_uses_default_periods(self):
        path = self.trace("R 0 4\n" * 110000)
        r = run_trace(self.config, path)
        self.assertEqual(r["status"], "SUCCESS")
        self.assertEqual(r["mode"], "debug")
        self.assertEqual(r["observed"], {"warmup_accesses": 10000, "measured_accesses": 100000})
        self.assertEqual(r["counters"]["hits"], 100000)
        self.assertEqual(r["counters"]["misses"], 0)
        self.assertEqual(r["metrics"]["memory_traffic_bytes"], 0)

    def test_invariant_failure_is_retained_as_failed_record(self):
        path = self.trace("R 0 4\n")
        with patch("src.simulator.runner.Cache.check_invariants", side_effect=AssertionError("injected validation failure")):
            result = run_trace(self.config, path, warmup=0, measured=1)
        self.assertEqual(result["status"], "FAIL")
        self.assertFalse(result["metrics_validated"])
        self.assertIn("injected validation failure", result["error"])
        self.assertEqual(result["counters"]["accesses"], 1)

    def test_cli_success_failure_and_no_overwrite(self):
        trace = self.trace("W 2048 4\nR 2048 4\nR 32 4\nR 4192 4\n")
        output, events = self.folder / "result.json", self.folder / "events.jsonl"
        cmd = [sys.executable, "-m", "src.simulator.runner", "--config", "configs/DAI-v1.json",
               "--trace", str(trace), "--warmup", "0", "--measure", "4", "--output", str(output),
               "--events", str(events)]
        run = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(run.returncode, 0, run.stderr)
        result = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(result["metrics"]["memory_traffic_bytes"], 128)
        self.assertEqual(len(events.read_text().splitlines()), 4)
        original = output.read_bytes()
        again = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        self.assertNotEqual(again.returncode, 0)
        self.assertEqual(output.read_bytes(), original)
        fail_output = self.folder / "failure.json"
        failed = subprocess.run([sys.executable, "-m", "src.simulator.runner", "--config", "configs/D0.json",
                                 "--trace", str(trace), "--warmup", "0", "--measure", "5",
                                 "--output", str(fail_output)], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(failed.returncode, 1)
        self.assertEqual(json.loads(fail_output.read_text())["status"], "FAIL")
