"""Reference solution for Exercise 2: empirical cohort payback by channel.

    python cohort_payback.py
"""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

from unit_economics import cohort_payback_month, payback_months_simple

DATA = Path(__file__).resolve().parent.parent / "data" / "cohorts.csv"


def load():
    with DATA.open() as fh:
        return list(csv.DictReader(fh))


def channel_curves(rows):
    """Pooled cumulative gross profit per customer by age, using only cohorts old
    enough to be observed at that age (avoids survivorship distortion)."""
    by = defaultdict(lambda: defaultdict(lambda: [0.0, 0]))
    cac = defaultdict(list)
    for r in rows:
        ch, age = r["channel"], int(r["age_months"])
        n = int(r["customers_in_cohort"])
        by[ch][age][0] += float(r["gross_profit"])
        by[ch][age][1] += n
        if age == 0:
            cac[ch].append((float(r["loaded_cac_per_customer"]), n))
    out = {}
    for ch, ages in by.items():
        cum, running = [], 0.0
        for age in sorted(ages):
            gp, n = ages[age]
            running += gp / n
            cum.append(running)
        weighted = sum(c * n for c, n in cac[ch]) / sum(n for _, n in cac[ch])
        out[ch] = (weighted, cum)
    return out


def main():
    rows = load()
    for ch, (cac, cum) in channel_curves(rows).items():
        pb = cohort_payback_month(cac, cum)
        first_order_gp = cum[0]
        naive = payback_months_simple(cac, 1150 if ch == "paid_social" else 1300, 0.58, 0.6)
        label = f"{pb:.1f} months" if pb is not None else "not within window"
        print(
            f"{ch:13s} loaded CAC {cac:7.0f} | first-order GP {first_order_gp:6.0f} | "
            f"cohort payback {label} | naive-formula payback {naive:.1f} months"
        )


if __name__ == "__main__":
    main()
