"""Validate segmentations and value scores against the holdout period.

    python validate.py
"""

from __future__ import annotations

import csv
import math

from rfm import (  # importing rfm first puts the Module 7 code on sys.path
    HORIZON, M7, build_customers, estimate_shrinkage_k, load_transactions,
    named_segments, probabilistic_value, rfm_composite, spearman, top_share,
)
import bgnbd  # noqa: E402


def truth_scores(customers):
    """Oracle: true purchase rate x P(alive at cutoff) x true mean spend. A ceiling, not a method."""
    rows = {int(r["customer_id"]): r for r in csv.DictReader((M7.parent / "data" / "customers_truth.csv").open())}
    out = []
    for c in customers:
        r = rows[c.cid]
        d = r["dropout_week"]
        alive = d == "" or float(d) > 52.0
        out.append(float(r["true_lambda"]) * HORIZON * float(r["true_mean_spend"]) * (1.0 if alive else 0.0))
    return out


def report():
    txns = load_transactions()
    cust = build_customers(txns)
    y = [c.holdout_revenue for c in cust]

    params, _ = bgnbd.fit([(c.x, c.t_x, c.T) for c in cust])
    k = estimate_shrinkage_k(txns)
    methods = {
        "recency only (lower is better)": [-c.recency for c in cust],
        "frequency only": [float(c.x) for c in cust],
        "monetary only": [c.avg_amount for c in cust],
        "RFM composite (R+F+M quintiles)": rfm_composite(cust),
        "BG/NBD x shrunk spend": probabilistic_value(cust, params, k),
        "oracle (uses ground truth)": truth_scores(cust),
    }
    n = len(cust)
    print(f"{n} customers; holdout revenue total {sum(y):,.0f}; "
          f"customers with any holdout order: {sum(1 for v in y if v > 0)/n:.1%}\n")
    print(f"{'score':34s} {'Spearman':>9s} {'top10% share':>13s} {'top20% share':>13s}")
    for name, s in methods.items():
        print(f"{name:34s} {spearman(s, y):9.3f} {top_share(s, y, .10):13.1%} {top_share(s, y, .20):13.1%}")
    print(f"{'(random scoring would give)':34s} {0.0:9.3f} {'10.0%':>13s} {'20.0%':>13s}")

    pred = sum(methods["BG/NBD x shrunk spend"])
    print(f"\nforecast total holdout revenue {pred:,.0f} vs actual {sum(y):,.0f} "
          f"({100*(pred/sum(y)-1):+.1f}%); shrinkage k = {k:.2f}")

    print("\nRule-based segments (validated on holdout)")
    print(f"{'segment':14s} {'n':>5s} {'share':>6s} {'mean holdout rev':>17s} {'95% interval':>20s}")
    by = {}
    for c in cust:
        by.setdefault(named_segments(c), []).append(c.holdout_revenue)
    for seg in ("active repeat", "cooling", "lapsed", "one-time"):
        v = by.get(seg, [])
        if not v:
            continue
        m = sum(v) / len(v)
        sd = math.sqrt(sum((a - m) ** 2 for a in v) / max(1, len(v) - 1))
        se = sd / math.sqrt(len(v))
        print(f"{seg:14s} {len(v):5d} {len(v)/n:6.1%} {m:17.0f} {m-1.96*se:9.0f} to {m+1.96*se:7.0f}")

    ranked = sorted(y, reverse=True)
    mean = sum(y) / n
    median = sorted(y)[n // 2]
    print(f"\nValue concentration: mean holdout revenue {mean:.0f}, median {median:.0f}; "
          f"top 10% of customers = {sum(ranked[:n//10])/sum(y):.1%} of revenue, "
          f"top 20% = {sum(ranked[:n//5])/sum(y):.1%}")


if __name__ == "__main__":
    report()
