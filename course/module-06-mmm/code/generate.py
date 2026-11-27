"""Simulate three years of weekly sales with known channel contributions.

Sales = baseline (level + trend + annual seasonality) + sum of channel effects + noise,
where each channel effect is  beta * (1 - exp(-adstock(spend) / K)):
geometric carry-over (adstock) followed by diminishing returns (saturation).

Two features make recovery hard, on purpose, because they are what real data is like:
  * TV and social are flighted together, so their spend is correlated.
  * Search budget follows expected demand (it is raised in the seasonal peak), so search
    spend is correlated with sales for reasons that have nothing to do with its effect.

Units: money in thousands. Every parameter is invented.

    python generate.py       # writes ../data/weekly.csv
"""

from __future__ import annotations

import csv
import math
import random
from pathlib import Path

SEED = 6_2026
WEEKS = 156

# channel: (adstock decay, saturation scale K, max effect beta)
TRUTH = {
    "tv":     dict(decay=0.60, K=1100.0, beta=3200.0),
    "social": dict(decay=0.30, K=700.0,  beta=1800.0),
    "search": dict(decay=0.10, K=450.0,  beta=1400.0),
}
LEVEL, TREND, SEASON_AMP, NOISE_SD = 6000.0, 6.0, 1200.0, 260.0

DATA = Path(__file__).resolve().parent.parent / "data"


def adstock(xs, decay):
    out, carry = [], 0.0
    for x in xs:
        carry = x + decay * carry
        out.append(carry)
    return out


def saturate(xs, K):
    return [1.0 - math.exp(-x / K) for x in xs]


def season(t):
    return math.sin(2 * math.pi * t / 52 - 1.0)


def simulate(seed: int = SEED, weeks: int = WEEKS, decouple_social: bool = False):
    """decouple_social=True flights social on its own random schedule instead of alongside TV,
    which is what deliberately designed spend variation looks like."""
    rng = random.Random(seed)
    # TV: flights of 4-8 weeks on, 3-8 weeks off
    tv, t = [], 0
    while t < weeks:
        on = rng.randint(4, 8)
        tv += [max(0.0, rng.gauss(70, 12)) for _ in range(on)]
        off = rng.randint(3, 8)
        tv += [max(0.0, rng.gauss(4, 3)) for _ in range(off)]
        t += on + off
    tv = tv[:weeks]
    # Social: follows TV flights (correlated), plus its own always-on base
    social = [max(0.0, 12 + 0.45 * x + rng.gauss(0, 8)) for x in tv]
    if decouple_social:
        social, t = [], 0
        while t < weeks:
            on, off = rng.randint(3, 7), rng.randint(3, 7)
            social += [max(0.0, rng.gauss(45, 10)) for _ in range(on)] + [max(0.0, rng.gauss(8, 5)) for _ in range(off)]
            t += on + off
        social = social[:weeks]
    # Search: budget scales with expected demand (endogenous)
    search = [max(0.0, 28 * (1 + 0.55 * season(t)) + rng.gauss(0, 4)) for t in range(weeks)]
    spend = {"tv": [10 * x for x in tv], "social": [10 * x for x in social], "search": [10 * x for x in search]}

    contrib = {}
    for ch, p in TRUTH.items():
        contrib[ch] = [p["beta"] * s for s in saturate(adstock(spend[ch], p["decay"]), p["K"])]
    base = [LEVEL + TREND * t + SEASON_AMP * season(t) for t in range(weeks)]
    sales = [base[t] + sum(contrib[c][t] for c in TRUTH) + rng.gauss(0, NOISE_SD) for t in range(weeks)]
    return dict(spend=spend, contrib=contrib, base=base, sales=sales)


def main():
    d = simulate()
    DATA.mkdir(exist_ok=True)
    cols = ["week", "sales", "tv", "social", "search", "true_base", "true_tv", "true_social", "true_search"]
    with (DATA / "weekly.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(cols)
        for t in range(WEEKS):
            w.writerow([t, f"{d['sales'][t]:.2f}", f"{d['spend']['tv'][t]:.2f}", f"{d['spend']['social'][t]:.2f}",
                        f"{d['spend']['search'][t]:.2f}", f"{d['base'][t]:.2f}",
                        f"{d['contrib']['tv'][t]:.2f}", f"{d['contrib']['social'][t]:.2f}", f"{d['contrib']['search'][t]:.2f}"])
    print(f"wrote {WEEKS} weeks to {DATA / 'weekly.csv'}")
    for ch in TRUTH:
        tot = sum(d["contrib"][ch])
        sp = sum(d["spend"][ch])
        print(f"  true {ch:7s}: spend {sp:8.0f}  contribution {tot:9.0f}  average ROI {tot / sp:5.2f}")


if __name__ == "__main__":
    main()
