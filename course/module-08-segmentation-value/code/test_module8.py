import math
import unittest

from rfm import (
    HORIZON, average_ranks, build_customers, estimate_shrinkage_k, load_transactions,
    named_segments, probabilistic_value, quintile_scores, rfm_composite, spearman, top_share,
)
import bgnbd


class ScoringPrimitives(unittest.TestCase):
    def test_average_ranks_with_ties(self):
        self.assertEqual(average_ranks([10, 20, 20, 30]), [1.0, 2.5, 2.5, 4.0])

    def test_quintiles_cover_one_to_five(self):
        s = quintile_scores(list(range(100)))
        self.assertEqual(min(s), 1)
        self.assertEqual(max(s), 5)
        self.assertEqual(s.count(1), 20)

    def test_quintiles_direction(self):
        lowers_best = quintile_scores([1, 2, 3, 4, 5], higher_is_better=False)
        self.assertEqual(lowers_best[0], 5)
        self.assertEqual(lowers_best[-1], 1)

    def test_spearman(self):
        self.assertAlmostEqual(spearman([1, 2, 3, 4], [10, 20, 30, 40]), 1.0)
        self.assertAlmostEqual(spearman([1, 2, 3, 4], [4, 3, 2, 1]), -1.0)

    def test_top_share_is_tie_aware(self):
        # identical scores carry no information: top 10% must capture exactly 10%
        outcomes = [float(i) for i in range(100)]
        self.assertAlmostEqual(top_share([1.0] * 100, outcomes, 0.10), 0.10)

    def test_top_share_perfect_score(self):
        outcomes = [float(i) for i in range(100)]
        share = top_share(outcomes, outcomes, 0.10)
        self.assertAlmostEqual(share, sum(range(90, 100)) / sum(range(100)))


class WithData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.txns = load_transactions()
        cls.cust = build_customers(cls.txns)
        cls.y = [c.holdout_revenue for c in cls.cust]
        cls.params, _ = bgnbd.fit([(c.x, c.t_x, c.T) for c in cls.cust])
        cls.k = estimate_shrinkage_k(cls.txns)
        cls.value = probabilistic_value(cls.cust, cls.params, cls.k)

    def test_features_consistent(self):
        for c in self.cust[:200]:
            self.assertGreaterEqual(c.recency, 0)
            self.assertAlmostEqual(c.T, c.t_x + c.recency, places=6)
            self.assertEqual(c.n_orders, c.x + 1)

    def test_shrinkage_near_true_ratio(self):
        # true within/between variance ratio of log spend is 0.25^2 / 0.35^2 = 0.51
        self.assertTrue(0.25 < self.k < 0.9)

    def test_total_revenue_forecast_close(self):
        pred, actual = sum(self.value), sum(self.y)
        self.assertLess(abs(pred / actual - 1), 0.05)

    def test_value_score_beats_chance_and_recency(self):
        v = top_share(self.value, self.y, 0.10)
        rec = top_share([-c.recency for c in self.cust], self.y, 0.10)
        self.assertGreater(v, 0.25)
        self.assertGreater(v, rec)

    def test_value_is_concentrated(self):
        ranked = sorted(self.y, reverse=True)
        self.assertGreater(sum(ranked[: len(ranked) // 10]) / sum(ranked), 0.4)

    def test_every_customer_gets_a_named_segment(self):
        segs = {named_segments(c) for c in self.cust}
        self.assertEqual(segs, {"one-time", "active repeat", "cooling", "lapsed"})

    def test_rfm_composite_range(self):
        s = rfm_composite(self.cust)
        self.assertTrue(all(3 <= v <= 15 for v in s))


if __name__ == "__main__":
    unittest.main()
