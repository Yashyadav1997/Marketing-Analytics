import unittest

from attribution import (
    MODELS, any_touch, credit_by_channel, first_click, last_click, linear, position_based,
)
from world import CHANNELS, simulate, spend, true_incremental, true_programme_incremental


class RuleTests(unittest.TestCase):
    def test_single_touch_gets_everything(self):
        for f in (last_click, first_click, linear, position_based):
            self.assertEqual(f(["email"]), {"email": 1.0})

    def test_position_based_weights(self):
        self.assertEqual(position_based(["a", "b"]), {"a": 0.5, "b": 0.5})
        w = position_based(["a", "b", "c", "d"])
        self.assertAlmostEqual(w["a"], 0.4)
        self.assertAlmostEqual(w["d"], 0.4)
        self.assertAlmostEqual(w["b"], 0.1)
        self.assertAlmostEqual(sum(w.values()), 1.0)

    def test_linear_and_empty(self):
        self.assertAlmostEqual(sum(linear(["a", "b", "c"]).values()), 1.0)
        for f in MODELS.values():
            self.assertEqual(f([]), {})

    def test_any_touch_does_not_deduplicate(self):
        self.assertEqual(sum(any_touch(["a", "b", "c"]).values()), 3.0)


class WorldTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.users = simulate()
        cls.truth = true_incremental(cls.users)
        cls.orders = sum(u.converted for u in cls.users)
        cls.touched_orders = sum(1 for u in cls.users if u.converted and u.touches)

    def test_deterministic(self):
        again = simulate()
        self.assertEqual([u.converted for u in again[:500]], [u.converted for u in self.users[:500]])
        self.assertEqual([u.touches for u in again[:500]], [u.touches for u in self.users[:500]])

    def test_potential_outcomes_are_monotone(self):
        # removing a channel can never create a sale
        for u in self.users:
            for c in CHANNELS:
                if u.without[c]:
                    self.assertTrue(u.converted)

    def test_rule_based_models_conserve_orders(self):
        for name in ("last-click", "first-click", "linear", "position-based"):
            total = sum(credit_by_channel(self.users, MODELS[name]).values())
            self.assertAlmostEqual(total, self.touched_orders, places=6, msg=name)

    def test_platform_view_overcounts(self):
        total = sum(credit_by_channel(self.users, any_touch).values())
        self.assertGreater(total, 1.3 * self.touched_orders)

    def test_last_click_overrewards_brand_search(self):
        lc = credit_by_channel(self.users, last_click)
        self.assertGreater(lc["search_brand"], 10 * self.truth["search_brand"])
        self.assertEqual(max(lc, key=lc.get), "search_brand")

    def test_first_click_overrewards_social_relative_to_truth(self):
        fc = credit_by_channel(self.users, first_click)
        self.assertGreater(fc["paid_social"], 2 * self.truth["paid_social"])

    def test_programme_incrementality_below_sum_and_below_blended(self):
        prog = true_programme_incremental(self.users)
        self.assertLessEqual(prog, sum(self.truth.values()))
        sp = sum(spend(self.users).values())
        self.assertLess(prog * 1000 / sp, self.orders * 1000 / sp)

    def test_true_ranking_differs_from_last_click(self):
        lc = credit_by_channel(self.users, last_click)
        sp = spend(self.users)
        by_lc = sorted(CHANNELS, key=lambda c: -lc[c] / sp[c])
        by_truth = sorted(CHANNELS, key=lambda c: -self.truth[c] / sp[c])
        self.assertNotEqual(by_lc, by_truth)


if __name__ == "__main__":
    unittest.main()
