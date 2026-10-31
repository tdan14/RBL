import unittest
from tools.analyze_experiments import describe, relative_reduction


class AnalysisTests(unittest.TestCase):
    def test_zero_baseline_and_relative_vs_absolute(self):
        self.assertIsNone(relative_reduction(0, 0))
        self.assertIsNone(relative_reduction(0, .1))
        self.assertAlmostEqual(relative_reduction(.2, .15), 25)
        self.assertAlmostEqual(relative_reduction(.1, .2), -100)

    def test_sample_standard_deviation_not_population(self):
        self.assertEqual(describe([1, 2, 3]), dict(mean=2, sample_stddev=1, minimum=1, maximum=3, n=3))
        self.assertIsNone(describe([0])["sample_stddev"])
