"""BG/NBD model (Fader, Hardie and Lee, 2005) for non-contractual repeat purchase.

Inputs per customer, all measured in the same time unit (weeks here):
    x    number of *repeat* purchases in the calibration window
    t_x  time of last purchase, measured from the customer's first purchase
    T    length of the customer's observation window (calibration end minus acquisition)

The model has four parameters: r, alpha (purchase-rate heterogeneity) and
a, b (dropout heterogeneity). Estimation is by maximum likelihood; optimisation
is on the log scale so the parameters stay positive.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable, Sequence

from optimize import nelder_mead


@dataclass(frozen=True)
class Params:
    r: float
    alpha: float
    a: float
    b: float


def _logsumexp(u: float, v: float) -> float:
    m = max(u, v)
    return m + math.log(math.exp(u - m) + math.exp(v - m))


def customer_loglik(p: Params, x: int, t_x: float, T: float) -> float:
    r, al, a, b = p.r, p.alpha, p.a, p.b
    base = (
        math.lgamma(r + x) - math.lgamma(r) + r * math.log(al)
        + math.lgamma(a + b) + math.lgamma(b + x) - math.lgamma(b) - math.lgamma(a + b + x)
    )
    alive_term = -(r + x) * math.log(al + T)
    if x == 0:
        return base + alive_term
    dead_term = math.log(a) - math.log(b + x - 1) - (r + x) * math.log(al + t_x)
    return base + _logsumexp(alive_term, dead_term)


def total_loglik(p: Params, data: Sequence[tuple[int, float, float]]) -> float:
    return sum(customer_loglik(p, x, tx, T) for x, tx, T in data)


def fit(data: Sequence[tuple[int, float, float]], start: Iterable[float] = (0.5, 10.0, 0.5, 2.0)):
    """Return (Params, log-likelihood). `data` is a list of (x, t_x, T)."""

    def neg(theta: Sequence[float]) -> float:
        try:
            p = Params(*(math.exp(v) for v in theta))
            val = -total_loglik(p, data)
        except (ValueError, OverflowError, ZeroDivisionError):
            return 1e18
        return val if math.isfinite(val) else 1e18

    theta, val = nelder_mead(neg, [math.log(s) for s in start], step=0.4, tol=1e-9, max_iter=4000)
    # restart once from the optimum to escape a collapsed simplex
    theta, val = nelder_mead(neg, theta, step=0.1, tol=1e-10, max_iter=4000)
    return Params(*(math.exp(v) for v in theta)), -val


def p_alive(p: Params, x: int, t_x: float, T: float) -> float:
    """Probability the customer is still active at the end of observation."""
    if x == 0:
        return 1.0
    ratio = (p.alpha + T) / (p.alpha + t_x)
    return 1.0 / (1.0 + (p.a / (p.b + x - 1)) * ratio ** (p.r + x))


def _hyp2f1(a: float, b: float, c: float, z: float, terms: int = 600) -> float:
    """Gauss hypergeometric series; adequate for 0 <= z < 0.9, which covers this use."""
    total = term = 1.0
    for k in range(terms):
        term *= (a + k) * (b + k) / ((c + k) * (k + 1)) * z
        total += term
        if abs(term) < 1e-14 * abs(total):
            break
    return total


def expected_purchases(p: Params, x: int, t_x: float, T: float, horizon: float) -> float:
    """Expected repeat purchases in the next `horizon` periods given history (x, t_x, T).

    Closed form from Fader, Hardie and Lee (2005), eq. 10.
    """
    r, al, a, b = p.r, p.alpha, p.a, p.b
    z = horizon / (al + T + horizon)
    inner = 1.0 - ((al + T) / (al + T + horizon)) ** (r + x) * _hyp2f1(r + x, b + x, a + b + x - 1, z)
    numerator = (a + b + x - 1) / (a - 1) * inner
    denominator = 1.0
    if x > 0:
        denominator += (a / (b + x - 1)) * ((al + T) / (al + t_x)) ** (r + x)
    return numerator / denominator
