"""The peeking problem: stop an A/A test the moment it looks significant.

Both arms have the same true conversion rate, so every "significant" result is a false
positive. A fixed-sample test is wrong 5% of the time by construction; checking after every
batch and stopping at the first p < 0.05 is wrong much more often.

Batch counts are drawn from the normal approximation to the binomial (fast, and accurate at
these sample sizes), which keeps the script runnable on any Python 3.10+.

    python peeking.py
"""

from __future__ import annotations

import random
from math import sqrt
from statistics import NormalDist

_N = NormalDist()


def _batch(rng: random.Random, n: int, p: float) -> int:
    x = round(rng.gauss(n * p, sqrt(n * p * (1 - p))))
    return max(0, min(n, x))


def z_stat(x1: int, n1: int, x2: int, n2: int) -> float:
    pooled = (x1 + x2) / (n1 + n2)
    se = sqrt(pooled * (1 - pooled) * (1 / n1 + 1 / n2))
    return 0.0 if se == 0 else (x1 / n1 - x2 / n2) / se


def false_positive_rate(
    looks: int, p: float = 0.04, n_per_look: int = 2000, runs: int = 4000,
    alpha: float = 0.05, seed: int = 11, stop_at_first: bool = True,
) -> float:
    rng = random.Random(seed)
    crit = _N.inv_cdf(1 - alpha / 2)
    hits = 0
    for _ in range(runs):
        x1 = x2 = n = 0
        flagged = False
        for k in range(1, looks + 1):
            x1 += _batch(rng, n_per_look, p)
            x2 += _batch(rng, n_per_look, p)
            n += n_per_look
            significant = abs(z_stat(x1, n, x2, n)) > crit
            if stop_at_first and significant:
                flagged = True
                break
            if not stop_at_first and k == looks:
                flagged = significant
        hits += flagged
    return hits / runs


if __name__ == "__main__":
    print("False-positive rate in A/A tests (true effect = 0), nominal 5%")
    print(f"{'looks':>6s} {'stop at first p<0.05':>22s} {'single look at end':>20s}")
    for looks in (1, 2, 5, 10, 20):
        peek = false_positive_rate(looks)
        once = false_positive_rate(looks, stop_at_first=False)
        print(f"{looks:6d} {peek:22.1%} {once:20.1%}")
    crit = _N.inv_cdf(1 - 0.05 / 2)
    print(f"\nBonferroni for 10 looks: test each at alpha/10 -> z > {_N.inv_cdf(1 - 0.05 / 20):.2f} instead of {crit:.2f}")
    print(f"10 looks, Bonferroni: {false_positive_rate(10, alpha=0.005):.1%}")
