"""Reconcile analytics revenue with the ledger, and quantify what cleaning can and cannot recover.

    python reconcile.py
"""

from __future__ import annotations

from audit import canonical, run_audit
from identity import people_counts, repeat_buyer_rate
from simulate import Dataset, simulate

# mapping learned from the audit: a name the spec does not know but whose meaning is clear
ALIASES = {"purchase_complete": "purchase"}


def _value(v):
    if isinstance(v, (int, float)):
        return float(v)
    try:
        return float(str(v).replace(",", ""))
    except ValueError:
        return None


def naive_revenue(events) -> float:
    """What a dashboard filtering on name == 'purchase' and summing numeric values reports."""
    return sum(e["params"]["value"] for e in events
               if e["name"] == "purchase" and isinstance(e["params"].get("value"), (int, float)))


def clean_events(events):
    """Normalise names, drop bots, drop out-of-range timestamps from time series (keep for totals),
    and remove duplicate transaction ids."""
    found = run_audit(events)
    out, seen = [], set()
    for e in sorted(events, key=lambda e: e["ts"]):
        if e["event_id"] in found["bot"]:
            continue
        name = ALIASES.get(e["name"].strip().lower(), canonical(e["name"]) or e["name"])
        e = dict(e, name=name, params=dict(e["params"]))
        if name == "purchase":
            tid = e["params"].get("transaction_id")
            if tid is not None:
                if tid in seen:
                    continue
                seen.add(tid)
            v = _value(e["params"].get("value"))
            if v is not None:
                e["params"]["value"] = v
        out.append(e)
    return out


def cleaned_revenue(events) -> float:
    return sum(e["params"]["value"] for e in clean_events(events)
               if e["name"] == "purchase" and isinstance(e["params"].get("value"), float))


def main(ds: Dataset | None = None):
    ds = ds or simulate()
    ledger = sum(p["value"] for p in ds.ledger)
    visible = sum(p["value"] for p in ds.ledger
                  if ds.people[p["person"]]["consent"] and not ds.people[p["person"]]["blocked"])
    naive = naive_revenue(ds.events)
    cleaned = cleaned_revenue(ds.events)
    dup_inflation = sum(e["params"]["value"] for e in ds.events
                        if e["event_id"] in ds.labels["duplicate"] and e["name"] == "purchase"
                        and isinstance(e["params"].get("value"), (int, float)))
    print(f"{'Ledger revenue (truth)':44s} {ledger:12,.0f}   100.0%")
    print(f"{'  less: consent declined / ad-blocked':44s} {visible - ledger:12,.0f}   {100 * (visible - ledger) / ledger:5.1f}%   (invisible to any audit)")
    print(f"{'= revenue that could be tracked':44s} {visible:12,.0f}   {100 * visible / ledger:5.1f}%")
    defect_loss = visible - (naive - dup_inflation)
    print(f"{'  less: lost to name/format defects':44s} {-defect_loss:12,.0f}   {-100 * defect_loss / ledger:5.1f}%")
    print(f"{'  plus: duplicate purchase events':44s} {dup_inflation:12,.0f}   {100 * dup_inflation / ledger:5.1f}%")
    print(f"{'= naive dashboard revenue':44s} {naive:12,.0f}   {100 * naive / ledger:5.1f}%")
    print(f"{'cleaned revenue (after audit fixes)':44s} {cleaned:12,.0f}   {100 * cleaned / ledger:5.1f}%")
    print(f"\nNaive dashboard is {100 * (naive / ledger - 1):+.1f}% against the ledger; cleaned data is "
          f"{100 * (cleaned / ledger - 1):+.1f}%. Cleaning moves the total by {100 * (cleaned - naive) / ledger:+.1f} points "
          f"(the defects were cancelling), and the {100 * (ledger - visible) / ledger:.1f}% never tracked stays missing.")

    ev = clean_events(ds.events)
    c = people_counts(ds, ev)
    print(f"\nPeople who left any tracked trace: true {c['true_people']:,}; device count {c['devices']:,} "
          f"({c['devices'] / c['true_people'] - 1:+.1%}); after login stitching {c['stitched']:,} "
          f"({c['stitched'] / c['true_people'] - 1:+.1%})")
    purchases = [e for e in ev if e["name"] == "purchase"]
    print("Repeat-buyer rate: " + "; ".join(
        f"{k} {repeat_buyer_rate(ds, purchases, k):.1%}" for k in ("device", "stitched", "person")))


if __name__ == "__main__":
    main()
