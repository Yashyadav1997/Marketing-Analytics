"""User-level holdout versus naive exposed-versus-unexposed, checked against ground truth.

For a chosen channel, randomly withhold it from a fraction of users and compare conversion
(intention-to-treat). Alongside, compute what an analyst would get without an experiment
by comparing exposed with unexposed users in the ordinary world.

    python holdout.py [channel ...]
"""

from __future__ import annotations

import sys
from math import sqrt
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "module-04-attribution" / "code"))

from world import REVENUE_PER_ORDER, SPEC, User, simulate, spend, true_incremental  # noqa: E402

N_USERS = 200_000
HOLDOUT = 0.20


def rct(channel: str, n: int = N_USERS, frac: float = HOLDOUT, seed: int = 4_2026):
    users = simulate(n, seed=seed, experiment=(channel, frac))
    test = [u for u in users if not u.held_out]
    hold = [u for u in users if u.held_out]
    rt = sum(u.converted for u in test) / len(test)
    rh = sum(u.converted for u in hold) / len(hold)
    se = sqrt(rt * (1 - rt) / len(test) + rh * (1 - rh) / len(hold))
    est = (rt - rh) * len(test)
    lo, hi = (rt - rh - 1.96 * se) * len(test), (rt - rh + 1.96 * se) * len(test)
    truth = true_incremental(test)[channel]
    cost = spend(test)[channel]
    return dict(est=est, lo=lo, hi=hi, truth=truth, cost=cost, n_test=len(test), n_hold=len(hold))


def naive(channel: str, n: int = N_USERS, seed: int = 4_2026):
    users = simulate(n, seed=seed)
    exp = [u for u in users if channel in u.touches]
    unexp = [u for u in users if channel not in u.touches]
    diff = sum(u.converted for u in exp) / len(exp) - sum(u.converted for u in unexp) / len(unexp)
    return diff * len(exp), true_incremental(users)[channel], spend(users)[channel]


def report(channels):
    print(f"{N_USERS:,} users; holdout = {HOLDOUT:.0%} randomly withheld. Orders are incremental orders.\n")
    print(f"{'channel':15s} {'TRUE':>7s} {'RCT est.':>9s} {'RCT 95% interval':>20s} {'naive est.':>11s} {'RCT iROAS':>10s} {'true iROAS':>11s}")
    for ch in channels:
        r = rct(ch)
        nv, _, _ = naive(ch)
        print(f"{ch:15s} {r['truth']:7d} {r['est']:9.0f} {r['lo']:9.0f} to {r['hi']:6.0f} {nv:11.0f} "
              f"{r['est'] * REVENUE_PER_ORDER / r['cost']:10.2f} {r['truth'] * REVENUE_PER_ORDER / r['cost']:11.2f}")


if __name__ == "__main__":
    report(sys.argv[1:] or ["paid_social", "email", "search_brand", "influencer"])
