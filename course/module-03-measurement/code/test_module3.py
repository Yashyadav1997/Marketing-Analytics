import unittest

from audit import canonical, run_audit, score
from identity import UnionFind, people_counts, stitch
from reconcile import ALIASES, clean_events, cleaned_revenue, naive_revenue
from simulate import simulate
from spec import KPI_DEPENDENCIES, SPEC


class Basics(unittest.TestCase):
    def test_canonical_names(self):
        self.assertEqual(canonical("Purchase"), "purchase")
        self.assertEqual(canonical("purchase "), "purchase")
        self.assertIsNone(canonical("purchase_complete"))

    def test_union_find(self):
        uf = UnionFind()
        uf.union("a", "b")
        uf.union("b", "c")
        self.assertEqual(uf.find("a"), uf.find("c"))
        self.assertNotEqual(uf.find("a"), uf.find("z"))

    def test_kpi_dependencies_reference_spec_events(self):
        for kpi, events in KPI_DEPENDENCIES.items():
            for e in events:
                self.assertIn(e, SPEC, kpi)


class World(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ds = simulate()
        cls.found = run_audit(cls.ds.events)

    def test_deterministic(self):
        again = simulate()
        self.assertEqual(len(again.events), len(self.ds.events))
        self.assertEqual(again.labels["duplicate"], self.ds.labels["duplicate"])

    def test_audit_catches_what_the_spec_defines(self):
        for row in score(self.found, self.ds.labels):
            name, injected, flagged, tp, prec, rec = row
            self.assertGreater(injected, 10, name)
            self.assertGreaterEqual(prec, 0.99, name)
            self.assertGreaterEqual(rec, 0.95, name)

    def test_unrecognised_event_names_hide_other_defects(self):
        # defects on events whose names do not map to the spec are not checked at all
        missed = self.ds.labels["missing_tid"] - self.found["missing_tid"]
        self.assertTrue(all(any(e["event_id"] == m and canonical(e["name"]) is None for e in self.ds.events) for m in missed))

    def test_cleaning_recovers_tracked_revenue_exactly(self):
        visible = sum(p["value"] for p in self.ds.ledger
                      if self.ds.people[p["person"]]["consent"] and not self.ds.people[p["person"]]["blocked"])
        self.assertAlmostEqual(cleaned_revenue(self.ds.events), visible, places=2)

    def test_invisible_loss_cannot_be_cleaned_away(self):
        ledger = sum(p["value"] for p in self.ds.ledger)
        cleaned = cleaned_revenue(self.ds.events)
        self.assertTrue(0.70 < cleaned / ledger < 0.82)

    def test_defects_cancel_in_the_naive_total(self):
        ledger = sum(p["value"] for p in self.ds.ledger)
        gap = abs(naive_revenue(self.ds.events) - cleaned_revenue(self.ds.events)) / ledger
        self.assertLess(gap, 0.01)

    def test_identity_counts_ordered(self):
        c = people_counts(self.ds, clean_events(self.ds.events))
        self.assertGreater(c["devices"], c["stitched"])
        self.assertGreater(c["stitched"], c["true_people"])
        self.assertTrue(set(ALIASES) <= {"purchase_complete"})


if __name__ == "__main__":
    unittest.main()
