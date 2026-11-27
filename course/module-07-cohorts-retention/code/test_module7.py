import math
import unittest
from collections import defaultdict

import bgnbd
from cohorts import cohort_table, exposure_adjusted_rate, load_transactions
from optimize import nelder_mead
from simulate import CAL_END, END, simulate


def calibration_data(txns):
    by = defaultdict(list)
    for cid, wk, amt in txns:
        by[cid].append(wk)
    data, holdout = [], []
    for ts in by.values():
        ts.sort()
        a = ts[0]
        cal = [t for t in ts if t <= CAL_END]
        data.append((len(cal) - 1, cal[-1] - a, CAL_END - a))
        holdout.append(sum(t > CAL_END for t in ts))
    return data, holdout


class OptimiserTests(unittest.TestCase):
    def test_quadratic(self):
        x, v = nelder_mead(lambda p: (p[0] - 3) ** 2 + (p[1] + 1) ** 2, [0, 0])
        self.assertAlmostEqual(x[0], 3, places=3)
        self.assertAlmostEqual(x[1], -1, places=3)


class BGNBDTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        txns, _ = simulate()
        cls.data, cls.holdout = calibration_data(txns)
        cls.params, cls.ll = bgnbd.fit(cls.data)

    def test_parameters_recovered(self):
        p = self.params
        self.assertAlmostEqual(p.r, 0.6, delta=0.12)
        self.assertAlmostEqual(p.alpha, 12.0, delta=2.5)
        self.assertAlmostEqual(p.a, 0.7, delta=0.25)
        self.assertAlmostEqual(p.b, 2.5, delta=0.8)

    def test_holdout_forecast_within_five_percent(self):
        pred = sum(bgnbd.expected_purchases(self.params, *d, END - CAL_END) for d in self.data)
        actual = sum(self.holdout)
        self.assertLess(abs(pred - actual) / actual, 0.05)

    def test_p_alive_behaves(self):
        p = self.params
        self.assertEqual(bgnbd.p_alive(p, 0, 0.0, 30.0), 1.0)  # model property: x=0 treated as alive
        recent = bgnbd.p_alive(p, 5, 50.0, 52.0)
        stale = bgnbd.p_alive(p, 5, 10.0, 52.0)
        self.assertGreater(recent, stale)
        self.assertTrue(0 < stale < recent <= 1)

    def test_likelihood_finite(self):
        self.assertTrue(math.isfinite(self.ll))


class CohortTests(unittest.TestCase):
    def test_young_cohorts_have_blank_late_cells(self):
        table = cohort_table(load_transactions())
        youngest = max(table)
        n, row = table[youngest]
        self.assertIsNone(row[-1])
        oldest_n, oldest_row = table[min(table)]
        self.assertIsNotNone(oldest_row[0])

    def test_exposure_rate_is_positive(self):
        r = exposure_adjusted_rate(load_transactions())
        self.assertTrue(0 < r < 0.2)


if __name__ == "__main__":
    unittest.main()
