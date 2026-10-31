from copy import deepcopy
from pathlib import Path
import random
import unittest

from src.simulator.cache import Cache
from src.simulator.models import Config
from tests.reference import ReferenceCache

ROOT = Path(__file__).resolve().parents[1]


def make(name="DAI-v1"):
    cache = Cache(Config.load(ROOT / f"configs/{name}.json"))
    cache.begin_measurement()
    return cache


class CacheTests(unittest.TestCase):
    def test_R003_expected_sequences(self):
        cases = [
            ("T01", [("R", 0), ("R", 0)], "MH", 0, 0),
            ("T02", [("R", x) for x in (0, 4096, 0, 4096)], "MMHH", 0, 0),
            ("T03", [("R", x) for x in (0, 2080, 0, 4160, 2080)], "MMHMM", 2, 0),
            ("T04-dirty", [("W", 2048), ("R", 2048), ("R", 32), ("R", 4192)], "MHMM", 1, 1),
            ("T04-clean", [("R", x) for x in (2048, 2048, 32, 4192)], "MHMM", 1, 0),
            ("T05", [("R", x) for x in (28, 32, 28)], "MMH", 0, 0),
            ("X01", [("R", x) for x in (0, 2080, 0)], "MMH", 0, 0),
            ("X02", [("R", x) for x in (0, 0x80000000, 0, 0x80000000)], "MMHH", 0, 0),
            ("X03", [("R", 0xFFFFFFFC)] * 2, "MH", 0, 0),
            ("X05", [("R", x) for x in (0, 2080, 4160, 0, 2080, 4160)], "MMMMMM", 4, 0),
        ]
        for name, seq, expected, evictions, wb in cases:
            with self.subTest(test_id=name):
                cache = make()
                events = [cache.access(op, a) for op, a in seq]
                self.assertEqual("".join("H" if e.hit else "M" for e in events), expected)
                self.assertEqual(cache.counters.evictions, evictions)
                self.assertEqual(cache.counters.dirty_writebacks, wb)
                self.assertEqual(cache.counters.line_fills, expected.count("M"))
                cache.check_invariants()
                if name == "T04-dirty":
                    self.assertEqual(events[-1].writeback_base, 2048)
                    self.assertEqual(cache.metrics()["memory_traffic_bytes"], 128)
                if name == "T04-clean":
                    self.assertEqual(cache.metrics()["memory_traffic_bytes"], 96)

    def test_T06_circular_wrap(self):
        cache = make()
        for i in range(257):
            cache.access("R", i * 4 % 1024)
        self.assertEqual((cache.counters.accesses, cache.counters.misses, cache.counters.hits), (257, 32, 225))
        self.assertEqual(cache.counters.evictions, 0)

    def test_warmup_preserves_dirty_and_recency(self):
        cache = make()
        cache.reset_run()
        for op, a in [("W", 0), ("R", 2080), ("R", 0)]:
            cache.access(op, a)
        self.assertEqual(cache.counters.accesses, 0)
        cache.begin_measurement()
        first, second = cache.access("R", 4160), cache.access("R", 0)
        self.assertEqual(first.victim_block, 65)
        self.assertFalse(first.hit)
        self.assertTrue(second.hit)
        self.assertEqual(cache.counters.dirty_writebacks, 0)
        self.assertTrue(cache.lines[0][second.way].dirty)

    def test_invalid_inputs_do_not_mutate(self):
        cache = make()
        cache.access("W", 0)
        for args in [("X", 0, 4), ("R", 0, 8), ("R", 2, 4), ("R", -4, 4),
                     ("R", 2**32, 4), ("R", True, 4), ("R", 4.0, 4), ("R", 0, True)]:
            before = deepcopy(cache.__dict__)
            with self.subTest(args=args), self.assertRaises(ValueError):
                cache.access(*args)
            self.assertEqual(cache.lines, before["lines"])
            self.assertEqual(cache.counters, before["counters"])
            self.assertEqual(cache.lru_way, before["lru_way"])

    def test_reset_and_empty_metrics(self):
        cache = make()
        cache.access("W", 0)
        cache.reset_run()
        self.assertIsNone(cache.metrics()["miss_rate"])
        self.assertFalse(any(l.valid or l.dirty for lines in cache.lines for l in lines))
        cache.begin_measurement()
        self.assertFalse(cache.access("R", 0).hit)

    def test_D2_exact_LRU_on_read_write_hit_and_fill(self):
        for op in ("R", "W"):
            with self.subTest(operation=op):
                cache = make("D2")
                for b in (0, 32, 64, 96):
                    cache.access("R", b * 32)
                cache.access(op, 0)
                event = cache.access("R", 128 * 32)
                self.assertEqual(event.victim_block, 32)
                # Fill made 128 MRU, so the next victim must be 64.
                self.assertEqual(cache.access("R", 160 * 32).victim_block, 64)
                cache.check_invariants()

    def test_D1_DAI_write_hit_changes_exact_LRU(self):
        for name, addresses in [("D1", (0, 2048, 4096)), ("DAI-v1", (0, 2080, 4160))]:
            cache = make(name)
            cache.access("R", addresses[0]); cache.access("R", addresses[1])
            cache.access("W", addresses[0])
            self.assertEqual(cache.access("R", addresses[2]).victim_block, addresses[1] // 32)

    def test_differential_against_full_block_list_oracle(self):
        rng = random.Random(7401)
        # Collision-heavy and high-address debug accesses, not W1-W5 official data.
        blocks = [i * 32 for i in range(25)] + [2**26, 2**27-1, 64, 65, 128, 130]
        accesses = [(rng.choice(("R", "W")), rng.choice(blocks) * 32 + rng.randrange(8) * 4)
                    for _ in range(4000)]
        for name in ("D0", "D1", "D2", "DAI-v1"):
            cache = make(name); oracle = ReferenceCache(cache.config)
            for i, (op, a) in enumerate(accesses):
                if i == 117:
                    cache.begin_measurement()  # Must not change victims/state.
                event = cache.access(op, a)
                self.assertEqual((event.hit, event.victim_block, event.writeback_base), oracle.access(op, a), (name, i))
                cache.check_invariants()
