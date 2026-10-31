import random
import unittest
from pathlib import Path

from src.simulator.mapping import Mapping
from src.simulator.models import Config

ROOT = Path(__file__).resolve().parents[1]


class MappingTests(unittest.TestCase):
    def test_round_trip_all_designs_boundaries_and_samples(self):
        rng = random.Random(30102026)
        blocks = [0, 1, 63, 64, 65, 127, 128, 129, 130, 8191, 8192, 2**26, 2**27-1]
        blocks += [rng.randrange(2**27) for _ in range(10000)]
        for name in ("D0", "D1", "D2", "DAI-v1"):
            mapping = Mapping(Config.load(ROOT / f"configs/{name}.json"))
            for b in blocks:
                with self.subTest(design=name, block=b):
                    _, index, tag = mapping.split(b * 32)
                    self.assertEqual(mapping.recover_block(index, tag), b)

    def test_dai_high_bits_and_inverse_writeback(self):
        m = Mapping(Config.load(ROOT / "configs/DAI-v1.json"))
        self.assertEqual(m.split(2048), (64, 1, 1))
        self.assertEqual(m.recover_block(1, 1) * 32, 2048)
        self.assertEqual(m.split(0xFFFFFFFC), (0x7FFFFFF, 0, 0x1FFFFF))
        self.assertNotEqual(m.split(0)[2], m.split(0x80000000)[2])

    def test_frozen_config_rejects_mutations(self):
        base = Config.load(ROOT / "configs/DAI-v1.json").snapshot()
        for key, value in [("sets", 128), ("ways", 4), ("mapping", "modulo"),
                           ("capacity_bytes", 8192), ("line_bytes", 64),
                           ("prefetch", True), ("bypass", True), ("replacement", "PLRU"),
                           ("sets", 64.0), ("ways", True)]:
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                Config(**{**base, key: value})

    def test_logic_metadata(self):
        self.assertEqual([Config.load(ROOT / f"configs/{n}.json").metadata_bytes
                          for n in ("D0", "D1", "D2", "DAI-v1")], [352, 376, 416, 376])
