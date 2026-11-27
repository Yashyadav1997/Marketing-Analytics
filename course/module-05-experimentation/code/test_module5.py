import unittest

import geolift
import holdout
import peeking
from power import holdout_users_needed, mde_relative, n_per_arm


class PowerTests(unittest.TestCase):
    def test_known_sample_size(self):
        # 2% baseline, 10% relative lift: about 80.7k per arm (standard calculators agree to ~1%)
        self.assertAlmostEqual(n_per_arm(0.02, 0.10), 80_679, delta=800)

    def test_smaller_effects_need_quadratically_more(self):
        ratio = n_per_arm(0.02, 0.05) / n_per_arm(0.02, 0.10)
        self.assertTrue(3.6 < ratio < 4.4)

    def test_mde_inverts_sample_size(self):
        n = n_per_arm(0.02, 0.15)
        self.assertAlmostEqual(mde_relative(0.02, n), 0.15, places=3)

    def test_dilution_inflates_sample_size(self):
        self.assertGreater(holdout_users_needed(0.06, 0.30, 0.20), 8 * n_per_arm(0.06, 0.20))


class PeekingTests(unittest.TestCase):
    def test_single_look_is_nominal(self):
        fp = peeking.false_positive_rate(1, runs=3000)
        self.assertTrue(0.035 < fp < 0.07, fp)

    def test_fixed_horizon_ignoring_interim_looks_is_nominal(self):
        fp = peeking.false_positive_rate(10, runs=3000, stop_at_first=False)
        self.assertTrue(0.035 < fp < 0.07, fp)

    def test_stopping_at_first_significant_look_inflates_errors(self):
        fp = peeking.false_positive_rate(10, runs=3000)
        self.assertGreater(fp, 0.14)


class GeoLiftTests(unittest.TestCase):
    def test_naive_before_after_is_badly_biased(self):
        s = geolift.simulate(true_lift=0.05)
        self.assertGreater(geolift.naive_before_after(s), 0.14)

    def test_did_is_unbiased_on_average(self):
        ests = [geolift.did(geolift.simulate(true_lift=0.05, seed=900 + k)) for k in range(80)]
        self.assertAlmostEqual(sum(ests) / len(ests), 0.05, delta=0.006)

    def test_permutation_includes_real_assignment(self):
        s = geolift.simulate(true_lift=0.05)
        pl = geolift.placebo_distribution(s)
        self.assertEqual(len(pl), 15504)  # C(20, 5)
        self.assertTrue(any(abs(p - geolift.did(s)) < 1e-12 for p in pl))

    def test_clear_effect_is_detected(self):
        s = geolift.simulate(true_lift=0.08, seed=77)
        self.assertLess(geolift.p_value(geolift.did(s), geolift.placebo_distribution(s)), 0.01)


class HoldoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.social = holdout.rct("paid_social")
        cls.naive_brand, cls.truth_brand, _ = holdout.naive("search_brand")

    def test_rct_interval_covers_truth(self):
        r = self.social
        self.assertTrue(r["lo"] <= r["truth"] <= r["hi"], r)

    def test_rct_detects_a_real_channel(self):
        self.assertGreater(self.social["lo"], 0)

    def test_naive_comparison_overstates_selected_channel(self):
        self.assertGreater(self.naive_brand, 5 * self.truth_brand)


if __name__ == "__main__":
    unittest.main()
