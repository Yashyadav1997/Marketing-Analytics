"""Matched-market (geo) lift with a placebo test, on synthetic regional sales.

Twenty regions are observed for 70 days. A campaign runs in 5 treated regions on days 49-69.
All regions share a seasonal-weekly pattern, a slow trend, and a festive surge that starts on
the same day as the campaign, which is exactly why a before/after comparison on the treated
regions alone is misleading.

    python geolift.py
"""

from __future__ import annotations

import itertools
import random
from math import exp, log, sqrt

N_GEOS, N_DAYS, START = 20, 70, 49
TREATED = list(range(5))
WEEKDAY = [1.00, 0.95, 0.90, 0.90, 1.00, 1.15, 1.10]
TREND_PER_DAY = 0.001
FESTIVE = 0.12            # common surge from START on, hits every region
NOISE = 0.06              # sd of multiplicative noise per region-day
SEED = 5_2026


def simulate(true_lift: float = 0.05, seed: int = SEED, treated=None):
    treated = TREATED if treated is None else treated
    rng = random.Random(seed)
    base = [exp(rng.gauss(log(1000), 0.5)) for _ in range(N_GEOS)]
    sales = [[0.0] * N_DAYS for _ in range(N_GEOS)]
    for g in range(N_GEOS):
        for d in range(N_DAYS):
            v = base[g] * WEEKDAY[d % 7] * (1 + TREND_PER_DAY) ** d
            if d >= START:
                v *= 1 + FESTIVE
                if g in treated:
                    v *= 1 + true_lift
            sales[g][d] = v * exp(rng.gauss(0, NOISE))
    return sales


def _mean(xs):
    return sum(xs) / len(xs)


def _geo_log_change(row):
    """log(mean sales in campaign window) - log(mean sales in the weeks before)."""
    pre = row[:START]
    post = row[START:]
    return log(_mean(post)) - log(_mean(pre))


def naive_before_after(sales, treated=TREATED) -> float:
    ch = _mean([_geo_log_change(sales[g]) for g in treated])
    return exp(ch) - 1


def did(sales, treated=TREATED) -> float:
    """Difference in differences on log changes: treated change minus control change."""
    ctrl = [g for g in range(N_GEOS) if g not in treated]
    t = _mean([_geo_log_change(sales[g]) for g in treated])
    c = _mean([_geo_log_change(sales[g]) for g in ctrl])
    return exp(t - c) - 1


def placebo_distribution(sales, treated=TREATED):
    """Permutation distribution of the effect statistic.

    Re-label every possible group of len(treated) regions among ALL regions (the real treated
    group is one of them) and compute the same difference-in-differences each time. If the
    campaign did nothing, the real effect is just one more draw from this distribution. Leaving
    the real treated regions out of the permutation set makes the test too liberal.
    """
    ch = [_geo_log_change(sales[g]) for g in range(N_GEOS)]   # computed once per region
    total, k, n = sum(ch), len(treated), N_GEOS
    out = []
    for combo in itertools.combinations(range(n), k):
        s_in = sum(ch[g] for g in combo)
        out.append(exp(s_in / k - (total - s_in) / (n - k)) - 1)
    return out


def p_value(real: float, placebos) -> float:
    return (1 + sum(abs(p) >= abs(real) for p in placebos)) / (1 + len(placebos))


def replicate(true_lift: float, runs: int = 300, first_seed: int = 1000):
    """Repeat the whole experiment on fresh noise; summarise the estimator's behaviour."""
    ests, sig = [], 0
    for k in range(runs):
        s = simulate(true_lift=true_lift, seed=first_seed + k)
        e = did(s)
        ests.append(e)
        sig += p_value(e, placebo_distribution(s)) < 0.05
    m = _mean(ests)
    sd = sqrt(sum((x - m) ** 2 for x in ests) / (runs - 1))
    return dict(mean=m, sd=sd, share_significant=sig / runs)


if __name__ == "__main__":
    for lift in (0.05, 0.02, 0.0):
        s = simulate(true_lift=lift)
        est = did(s)
        pl = placebo_distribution(s)
        sd = sqrt(sum(p * p for p in pl) / len(pl))  # spread of the permutation distribution
        print(f"true lift {lift:5.1%} | naive before/after {naive_before_after(s):7.1%} | "
              f"DiD {est:6.1%} | placebo sd {sd:5.1%} | permutation p = {p_value(est, pl):.3f}")

    print("\nReplicated over 300 fresh draws of the noise:")
    for lift in (0.05, 0.02, 0.01, 0.0):
        r = replicate(lift)
        print(f"true lift {lift:5.1%} | mean DiD {r['mean']:6.2%} | sd {r['sd']:5.2%} | "
              f"flagged significant (p<0.05) in {r['share_significant']:.0%} of runs")
