"""Does the ranking of scoring methods survive different simulated datasets?

Reference for Exercise 3. Takes about 30 seconds.

    python robustness.py
"""

from __future__ import annotations

import statistics as st
from collections import defaultdict

from rfm import (
    build_customers, estimate_shrinkage_k, probabilistic_value, rfm_composite,
    spearman, top_share,
)
import bgnbd  # noqa: E402
from simulate import simulate  # noqa: E402

SEEDS = range(101, 111)


def one(seed: int):
    txns, _ = simulate(seed=seed)
    by = defaultdict(list)
    for cid, wk, amt in txns:
        by[cid].append((wk, amt))
    for v in by.values():
        v.sort()
    cust = build_customers(by)
    y = [c.holdout_revenue for c in cust]
    params, _ = bgnbd.fit([(c.x, c.t_x, c.T) for c in cust])
    scores = {
        "BG/NBD x spend": probabilistic_value(cust, params, estimate_shrinkage_k(by)),
        "RFM composite": rfm_composite(cust),
        "frequency only": [float(c.x) for c in cust],
        "recency only": [-c.recency for c in cust],
    }
    return {k: (top_share(s, y, 0.10), spearman(s, y)) for k, s in scores.items()}


if __name__ == "__main__":
    runs = [one(s) for s in SEEDS]
    print(f"{len(runs)} simulated datasets (seeds {SEEDS.start} to {SEEDS.stop - 1})")
    print(f"{'method':18s} {'top-10% share (mean ± sd)':>28s} {'Spearman (mean)':>16s}")
    for name in runs[0]:
        shares = [r[name][0] for r in runs]
        rhos = [r[name][1] for r in runs]
        print(f"{name:18s} {100*st.mean(shares):17.1f}% ± {100*st.stdev(shares):4.1f}   {st.mean(rhos):14.3f}")
    wins = sum(r["BG/NBD x spend"][0] > r["RFM composite"][0] for r in runs)
    gaps = [100 * (r["BG/NBD x spend"][0] - r["RFM composite"][0]) for r in runs]
    print(f"\nBG/NBD beats RFM composite on top-10% share in {wins} of {len(runs)} datasets "
          f"(gap {min(gaps):.1f} to {max(gaps):.1f} points, mean {st.mean(gaps):.1f})")

    # The shipped dataset (default seed) is a different story: bootstrap its own gap.
    import random

    from rfm import build_customers as _bc, load_transactions
    txns = load_transactions()
    cust = _bc(txns)
    y = [c.holdout_revenue for c in cust]
    params, _ = bgnbd.fit([(c.x, c.t_x, c.T) for c in cust])
    a = probabilistic_value(cust, params, estimate_shrinkage_k(txns))
    b = rfm_composite(cust)
    rng, n, diffs = random.Random(5), len(cust), []
    for _ in range(300):
        idx = [rng.randrange(n) for _ in range(n)]
        yy = [y[i] for i in idx]
        diffs.append(100 * (top_share([a[i] for i in idx], yy, .1) - top_share([b[i] for i in idx], yy, .1)))
    diffs.sort()
    print(f"shipped dataset: gap {100*(top_share(a, y, .1) - top_share(b, y, .1)):.1f} points, "
          f"bootstrap 95% interval {diffs[7]:.1f} to {diffs[292]:.1f}")
