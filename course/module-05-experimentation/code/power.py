"""Sample size and minimum detectable effect for a two-arm test on a conversion rate.

    python power.py
"""

from __future__ import annotations

from math import ceil, sqrt
from statistics import NormalDist

_N = NormalDist()


def n_per_arm(p0: float, rel_lift: float, alpha: float = 0.05, power: float = 0.80) -> int:
    """Users needed in EACH arm to detect a relative lift in a rate p0 (two-sided z-test,
    unpooled variance under the alternative). Uses the standard normal approximation."""
    p1 = p0 * (1 + rel_lift)
    z_a = _N.inv_cdf(1 - alpha / 2)
    z_b = _N.inv_cdf(power)
    var = p0 * (1 - p0) + p1 * (1 - p1)
    return ceil((z_a + z_b) ** 2 * var / (p1 - p0) ** 2)


def mde_relative(p0: float, n: int, alpha: float = 0.05, power: float = 0.80) -> float:
    """Smallest relative lift detectable with n users per arm (solved by bisection)."""
    lo, hi = 1e-6, 5.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if n_per_arm(p0, mid, alpha, power) > n:
            lo = mid
        else:
            hi = mid
    return hi


def holdout_users_needed(p0: float, exposed_share: float, rel_lift_among_exposed: float,
                         alpha: float = 0.05, power: float = 0.80) -> int:
    """Per-arm size for a holdout where only `exposed_share` of users are ever reached.

    Unexposed users dilute the intention-to-treat effect by that share, so the effect
    you can actually see is exposed_share x the effect among the exposed.
    """
    return n_per_arm(p0, exposed_share * rel_lift_among_exposed, alpha, power)


if __name__ == "__main__":
    print("Users per arm to detect a relative lift (alpha 0.05, power 0.80)")
    print(f"{'baseline rate':>14s}" + "".join(f"{f'{int(l*100)}% lift':>12s}" for l in (0.05, 0.10, 0.20, 0.50)))
    for p0 in (0.002, 0.01, 0.02, 0.06):
        print(f"{p0:14.1%}" + "".join(f"{n_per_arm(p0, l):12,d}" for l in (0.05, 0.10, 0.20, 0.50)))
    print("\nDetectable relative lift with a given arm size, baseline 2%")
    for n in (2_000, 10_000, 50_000, 200_000):
        print(f"  n = {n:>7,d} per arm -> {mde_relative(0.02, n):6.1%}")
    print("\nDilution: a channel reaching 30% of users, true lift among the exposed 20% on a 6% base")
    print(f"  per-arm size needed: {holdout_users_needed(0.06, 0.30, 0.20):,d} "
          f"(vs {n_per_arm(0.06, 0.20):,d} if everyone were exposed)")
