from itertools import islice
import unittest

from src.workloads import accesses, encoded_trace, scenarios


class WorkloadTests(unittest.TestCase):
    def spec(self, ident):
        return next(s for s in scenarios() if s["trace_id"] == ident)

    def test_counts_and_unique_ids(self):
        specs = scenarios()
        self.assertEqual(len(specs), 24)
        self.assertEqual(len({s["trace_id"] for s in specs}), 24)
        self.assertEqual([s["seed"] for s in specs if s["seed"] is not None], list(range(1, 11)))

    def test_sequential_and_circular_boundaries(self):
        seq = list(islice(accesses(self.spec("W1-write")), 3))
        self.assertEqual(seq, [("W", 0x10000000 + i * 4, 4) for i in range(3)])
        ring = list(islice(accesses(self.spec("W2-1024")), 257))
        self.assertEqual(ring[255][1], 0x20000000 + 1020)
        self.assertEqual(ring[256][1], 0x20000000)

    def test_moving_average_includes_current_and_wraps_history(self):
        prefix = list(islice(accesses(self.spec("W3-N8")), 11))
        base = 0x30000000
        self.assertEqual(prefix[:4], [("W", base, 4), ("R", base, 4), ("R", base + 16380, 4), ("R", base + 16376, 4)])
        self.assertEqual(prefix[9:11], [("W", base + 4, 4), ("R", base + 4, 4)])

    def test_sensor_pointers_are_separate_and_wrap(self):
        seq = list(islice(accesses(self.spec("W4-even")), 1025))
        self.assertEqual([a for _, a, _ in seq[:5]], [0x40000000, 0x40000400, 0x40000800, 0x40000C00, 0x40000004])
        self.assertEqual(seq[1024][1], 0x40000000)

    def test_seed_replay_and_stride(self):
        for ident in ("W4-random-S01", "W4-random-S10"):
            self.assertEqual(list(encoded_trace(self.spec(ident), 2000)), list(encoded_trace(self.spec(ident), 2000)))
        self.assertNotEqual(list(encoded_trace(self.spec("W4-random-S01"), 50)), list(encoded_trace(self.spec("W4-random-S02"), 50)))
        trace = list(islice(accesses(self.spec("W5-K4")), 5))
        self.assertEqual([a for _, a, _ in trace], [0x50000000, 0x50001000, 0x50002000, 0x50003000, 0x50000000])
