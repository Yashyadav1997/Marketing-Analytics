"""Customer features, RFM scoring, tie-aware validation metrics and a probabilistic value score.

Reuses the Module 7 simulated purchase log and BG/NBD implementation.
"""

from __future__ import annotations

import math
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

M7 = Path(__file__).resolve().parents[2] / "module-07-cohorts-retention" / "code"
sys.path.insert(0, str(M7))

import bgnbd  # noqa: E402
from cohorts import load_transactions  # noqa: E402
from simulate import CAL_END, END  # noqa: E402

HORIZON = END - CAL_END


@dataclass(frozen=True)
class Customer:
    cid: int
    x: int                # repeat purchases in calibration window
    t_x: float            # weeks from first purchase to last calibration purchase
    T: float              # weeks from first purchase to calibration end
    recency: float        # weeks since last calibration purchase
    avg_amount: float     # mean order value in calibration window
    n_orders: int
    holdout_orders: int
    holdout_revenue: float


def build_customers(txns, cal_end: float = CAL_END) -> list[Customer]:
    out = []
    for cid, orders in sorted(txns.items()):
        cal = [(t, a) for t, a in orders if t <= cal_end]
        if not cal:
            continue
        hold = [(t, a) for t, a in orders if t > cal_end]
        first, last = cal[0][0], cal[-1][0]
        out.append(
            Customer(
                cid=cid, x=len(cal) - 1, t_x=last - first, T=cal_end - first,
                recency=cal_end - last, avg_amount=sum(a for _, a in cal) / len(cal),
                n_orders=len(cal), holdout_orders=len(hold),
                holdout_revenue=sum(a for _, a in hold),
            )
        )
    return out


# ---------------------------------------------------------------- scoring

def average_ranks(values: list[float]) -> list[float]:
    """1-based ranks, ties share the average rank."""
    order = sorted(range(len(values)), key=values.__getitem__)
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        avg = (i + j) / 2 + 1
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def quintile_scores(values: list[float], higher_is_better: bool = True) -> list[int]:
    """1 (worst) to 5 (best) by percentile of average rank; tied values share a score."""
    sign = 1 if higher_is_better else -1
    ranks = average_ranks([sign * v for v in values])
    n = len(values)
    return [min(5, int((r - 0.5) / n * 5) + 1) for r in ranks]


def rfm_composite(customers: list[Customer]) -> list[float]:
    r = quintile_scores([c.recency for c in customers], higher_is_better=False)
    f = quintile_scores([c.x for c in customers])
    m = quintile_scores([c.avg_amount for c in customers])
    return [float(a + b + c) for a, b, c in zip(r, f, m)]


def spearman(xs: list[float], ys: list[float]) -> float:
    rx, ry = average_ranks(list(xs)), average_ranks(list(ys))
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    cov = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    vx = math.sqrt(sum((a - mx) ** 2 for a in rx))
    vy = math.sqrt(sum((b - my) ** 2 for b in ry))
    return cov / (vx * vy)


def top_share(scores: list[float], outcomes: list[float], frac: float = 0.10) -> float:
    """Share of total outcome captured by the top `frac` of customers by score.

    Tie-aware: if a group of equal scores straddles the cut, it contributes in
    proportion, so a coarse score is not rewarded or punished by sort order.
    """
    n = len(scores)
    k = frac * n
    total = sum(outcomes)
    groups = defaultdict(list)
    for s, o in zip(scores, outcomes):
        groups[s].append(o)
    captured, taken = 0.0, 0.0
    for s in sorted(groups, reverse=True):
        g = groups[s]
        room = k - taken
        if room <= 0:
            break
        take = min(len(g), room)
        captured += sum(g) / len(g) * take
        taken += take
    return captured / total if total else 0.0


# ---------------------------------------------------------------- value

def estimate_shrinkage_k(txns) -> float:
    """Moment estimate of within/between variance ratio of log order value.

    Used to shrink a customer's observed mean order value toward the population mean:
    shrunk = (n * mean + k * pop_mean) / (n + k). A Gamma-Gamma model is the standard
    formal version; this is the same idea with fewer moving parts.
    """
    within_ss = within_df = 0.0
    means, ns = [], []
    for orders in txns.values():
        logs = [math.log(a) for t, a in orders if t <= CAL_END]
        if len(logs) >= 2:
            m = sum(logs) / len(logs)
            within_ss += sum((v - m) ** 2 for v in logs)
            within_df += len(logs) - 1
        if logs:
            means.append(sum(logs) / len(logs))
            ns.append(len(logs))
    s2_within = within_ss / within_df
    grand = sum(means) / len(means)
    n_bar = sum(ns) / len(ns)
    s2_between = max(1e-6, sum((m - grand) ** 2 for m in means) / (len(means) - 1) - s2_within / n_bar)
    return s2_within / s2_between


def probabilistic_value(customers: list[Customer], params: bgnbd.Params, k: float) -> list[float]:
    """Expected holdout-period revenue = expected repeat orders x shrunk order value."""
    pop = sum(c.avg_amount for c in customers) / len(customers)
    out = []
    for c in customers:
        spend = (c.n_orders * c.avg_amount + k * pop) / (c.n_orders + k)
        out.append(bgnbd.expected_purchases(params, c.x, c.t_x, c.T, HORIZON) * spend)
    return out


def named_segments(c: Customer) -> str:
    """A rule-based segmentation of the kind commonly built in a dashboard."""
    if c.x == 0:
        return "one-time"
    if c.recency <= 13:
        return "active repeat"
    if c.recency <= 26:
        return "cooling"
    return "lapsed"
