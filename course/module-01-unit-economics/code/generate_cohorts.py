"""Generate a synthetic monthly-cohort dataset for the Module 1 exercises.

Nothing here is real brand data. Retention decays geometrically with noise and
two acquisition channels differ in cost and in how loyal their customers are,
which is the pattern that makes blended payback misleading.

    python generate_cohorts.py            # writes ../data/cohorts.csv
"""

from __future__ import annotations

import csv
import random
from pathlib import Path

SEED = 20261127
MONTHS_OBSERVED = 12
COHORT_STARTS = 12  # twelve monthly acquisition cohorts

CHANNELS = {
    # platform CAC, loaded multiplier, month-1 repeat rate, monthly decay of repeat rate
    "paid_social": dict(platform_cac=520, load=1.75, repeat0=0.16, decay=0.78, aov=1150),
    "search_brand": dict(platform_cac=310, load=1.55, repeat0=0.24, decay=0.86, aov=1300),
}
MARGIN = 0.58


def main() -> None:
    rng = random.Random(SEED)
    rows = []
    for channel, p in CHANNELS.items():
        for cohort in range(COHORT_STARTS):
            customers = rng.randint(700, 1500)
            noise_cac = rng.uniform(0.92, 1.12)
            loaded = p["platform_cac"] * p["load"] * noise_cac
            alive = customers
            for age in range(MONTHS_OBSERVED - cohort):
                if age == 0:
                    orders = customers
                else:
                    rate = p["repeat0"] * (p["decay"] ** (age - 1)) * rng.uniform(0.85, 1.15)
                    orders = int(customers * rate)
                revenue = orders * p["aov"] * rng.uniform(0.97, 1.04)
                rows.append(
                    dict(
                        channel=channel,
                        cohort_month=cohort,
                        age_months=age,
                        customers_in_cohort=customers,
                        orders=orders,
                        revenue=round(revenue, 2),
                        gross_profit=round(revenue * MARGIN, 2),
                        loaded_cac_per_customer=round(loaded, 2),
                    )
                )
    out = Path(__file__).resolve().parent.parent / "data" / "cohorts.csv"
    out.parent.mkdir(exist_ok=True)
    with out.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} rows to {out}")


if __name__ == "__main__":
    main()
