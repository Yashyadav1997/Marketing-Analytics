import unittest

import mmm
from generate import TRUTH, simulate

N = 143
SIGMA = 260.0


class TransformTests(unittest.TestCase):
    def test_adstock(self):
        self.assertEqual(mmm.adstock([10, 0, 0], 0.5), [10, 5.0, 2.5])

    def test_saturation_bounds_and_monotone(self):
        s = mmm.saturate([0, 10, 100, 1000], 100.0)
        self.assertEqual(s[0], 0.0)
        self.assertTrue(all(a < b for a, b in zip(s, s[1:])))
        self.assertLess(s[-1], 1.0)

    def test_solver(self):
        x = mmm.solve([[2.0, 1.0], [1.0, 3.0]], [5.0, 10.0])
        self.assertAlmostEqual(x[0], 1.0)
        self.assertAlmostEqual(x[1], 3.0)

    def test_least_squares_recovers_exact_fit(self):
        t = [float(i) for i in range(20)]
        y = [3.0 + 2.0 * v for v in t]
        b = mmm.least_squares([[1.0] * 20, t], y, ridge=0.0)
        self.assertAlmostEqual(b[0], 3.0, places=6)
        self.assertAlmostEqual(b[1], 2.0, places=6)

    def test_simulation_is_deterministic(self):
        self.assertEqual(simulate()["sales"][:5], simulate()["sales"][:5])


class FitTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = mmm.load()
        cls.free = mmm.fit(cls.d, n_train=N)
        cls.roi = mmm.roi_table(cls.free, cls.d)

    def test_predicts_well_out_of_sample(self):
        self.assertLess(mmm.mape(self.free, self.d, N, 156), 0.05)

    def test_coefficients_nonnegative(self):
        self.assertTrue(all(b >= 0 for b in self.free["coef"][self.free["n_ctrl"]:]))

    def test_well_identified_channel_is_recovered(self):
        decay, _ = self.free["params"]["tv"]
        self.assertAlmostEqual(decay, TRUTH["tv"]["decay"], delta=0.1)
        self.assertAlmostEqual(self.roi["tv"]["est"], self.roi["tv"]["true"], delta=0.25 * self.roi["tv"]["true"])

    def test_good_prediction_does_not_imply_good_attribution(self):
        for c in ("social", "search"):
            self.assertGreater(self.roi[c]["est"], 1.4 * self.roi[c]["true"], c)

    def test_optimiser_is_not_the_problem(self):
        other = mmm.fit(self.d, n_train=N, seed=3, max_iter=1500)
        for c in mmm.CHANNELS:
            self.assertAlmostEqual(mmm.roi_table(other, self.d)[c]["est"], self.roi[c]["est"], places=2)

    def test_omitting_controls_inflates_the_demand_following_channel(self):
        m = mmm.fit(self.d, n_train=N, controls=False)
        self.assertGreater(mmm.roi_table(m, self.d)["search"]["est"], 3 * self.roi["search"]["true"])

    def test_calibration_pulls_towards_lift_test(self):
        m = mmm.fit(self.d, n_train=N, calib={"tv": (4.47, 0.5, SIGMA)})
        est = mmm.roi_table(m, self.d)["tv"]["est"]
        self.assertLess(abs(est - 4.47), abs(self.roi["tv"]["est"] - 4.47))

    def test_wrong_calibration_is_invisible_to_holdout_error(self):
        m = mmm.fit(self.d, n_train=N, calib={"social": (5.0, 0.5, SIGMA)})
        self.assertLess(abs(mmm.mape(m, self.d, N, 156) - mmm.mape(self.free, self.d, N, 156)), 0.01)
        self.assertGreater(mmm.roi_table(m, self.d)["social"]["est"], self.roi["social"]["est"])

    def test_marginal_below_average(self):
        for c in mmm.CHANNELS:
            self.assertLess(mmm.marginal_roi(self.free, self.d, c), self.roi[c]["est"])


if __name__ == "__main__":
    unittest.main()
