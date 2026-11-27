import unittest

from unit_economics import (
    break_even_roas,
    cac_load_factor,
    cohort_payback_month,
    gross_margin,
    loaded_cac,
    ltv_cac_ratio,
    ltv_simple,
    marketing_spend_ratio,
    payback_months_simple,
    required_incremental_revenue,
    summarise,
)


class UnitEconomicsTests(unittest.TestCase):
    def test_gross_margin_worked_example(self):
        # Rs 1,000 product, Rs 420 COGS -> 58%
        self.assertAlmostEqual(gross_margin(1000, 420), 0.58)

    def test_break_even_roas(self):
        self.assertAlmostEqual(break_even_roas(0.58), 1.7241, places=4)
        # a 3x ROAS on a 40% margin is exactly 1.2x gross-profit cover, not "great"
        self.assertAlmostEqual(3 * 0.40, 1.2)
        self.assertAlmostEqual(break_even_roas(0.40), 2.5)

    def test_loaded_cac_exceeds_platform_cac(self):
        platform = 500.0
        loaded = loaded_cac(
            ad_spend=500_000, new_customers=1000,
            agency_fees=150_000, creative_costs=120_000, tools=30_000, team_time=50_000,
        )
        self.assertAlmostEqual(loaded, 850.0)
        self.assertAlmostEqual(cac_load_factor(platform, loaded), 0.70)

    def test_payback_simple(self):
        self.assertAlmostEqual(payback_months_simple(850, 1200, 0.58, 0.6), 2.0354, places=3)

    def test_cohort_payback_interpolates(self):
        cum = [300.0, 450.0, 600.0, 700.0]  # cumulative gross profit per customer
        self.assertAlmostEqual(cohort_payback_month(525, cum), 1.5)
        self.assertIsNone(cohort_payback_month(5000, cum))
        self.assertEqual(cohort_payback_month(200, cum), 0.0)

    def test_ltv_cac(self):
        ltv = ltv_simple(aov=1200, margin=0.58, annual_orders=3, lifespan_years=2)
        self.assertAlmostEqual(ltv, 4176.0)
        self.assertAlmostEqual(ltv_cac_ratio(ltv, 850), 4.9129, places=3)

    def test_spend_ratio(self):
        self.assertAlmostEqual(marketing_spend_ratio(20, 100), 0.20)

    def test_fee_threshold_matches_pricing_example(self):
        # Rs 2 lakh fee at 20% incremental contribution margin -> Rs 10 lakh revenue
        self.assertAlmostEqual(required_incremental_revenue(200_000, 0.20), 1_000_000)

    def test_summarise_chain(self):
        s = summarise(
            revenue=1000, cogs=420, ad_spend=500_000, new_customers=1000,
            aov=1200, monthly_orders=0.6, lifespan_years=2,
            agency_fees=150_000, creative_costs=120_000, tools=30_000, team_time=50_000,
        )
        self.assertAlmostEqual(s.margin, 0.58)
        self.assertAlmostEqual(s.loaded_cac, 850.0)

    def test_bad_inputs_raise(self):
        with self.assertRaises(ValueError):
            break_even_roas(0)
        with self.assertRaises(ValueError):
            loaded_cac(100, 0)


if __name__ == "__main__":
    unittest.main()
