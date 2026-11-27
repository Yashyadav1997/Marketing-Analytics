"""Simulate a non-contractual customer base with known ground truth.

Each customer follows the BG/NBD story (Fader, Hardie and Lee, 2005):
  - purchases arrive as a Poisson process with a customer-specific rate lambda,
    where lambda ~ Gamma(shape R, rate ALPHA)  (per week);
  - after each *repeat* purchase the customer drops out for good with
    probability p, where p ~ Beta(A, B).
Order value varies by customer (lognormal) and by order (lognormal).

Customers are acquired at a uniformly random week in [0, CAL_END). Transactions
are observed to END. The calibration window ends at CAL_END; the remainder is
a holdout used to check forecasts and segments (Modules 7 and 8).

    python simulate.py        # writes ../data/transactions.csv and customers_truth.csv
"""

from __future__ import annotations

import csv
import math
import random
from pathlib import Path

SEED = 7_2026
N_CUSTOMERS = 2500
CAL_END = 52.0   # weeks
END = 78.0       # weeks (26-week holdout)

R, ALPHA = 0.6, 12.0    # mean purchase rate R/ALPHA = 0.05 per week
A, B = 0.7, 2.5         # mean dropout probability A/(A+B) ~ 0.22
MEAN_SPEND, SPEND_SD = 1000.0, 0.35

DATA = Path(__file__).resolve().parent.parent / "data"


def simulate(n: int = N_CUSTOMERS, seed: int = SEED, promo: tuple[float, float, float] | None = None):
    """Return (transactions, truth). `promo=(start_week, end_week, multiplier)` multiplies
    every active customer's purchase rate inside the window, which violates the model's
    stationarity assumption (used by Exercise 4). With promo=None the random stream is
    unchanged, so the shipped data is reproduced exactly."""
    rng = random.Random(seed)
    txns, truth = [], []
    for cid in range(1, n + 1):
        acquired = rng.uniform(0, CAL_END)
        lam = rng.gammavariate(R, 1.0 / ALPHA)
        p = rng.betavariate(A, B)
        mu = math.log(MEAN_SPEND) + rng.gauss(0, SPEND_SD)
        txns.append((cid, acquired, round(math.exp(mu + rng.gauss(0, 0.25)), 2)))
        t, dropout = acquired, math.inf
        while lam > 0:
            if promo is None:
                t += rng.expovariate(lam)
            else:  # thinning: propose at the peak rate, accept in proportion to the true rate
                peak = lam * max(1.0, promo[2])
                t += rng.expovariate(peak)
                rate = lam * (promo[2] if promo[0] <= t < promo[1] else 1.0)
                if rng.random() > rate / peak:
                    continue
            if t > END:
                break
            txns.append((cid, t, round(math.exp(mu + rng.gauss(0, 0.25)), 2)))
            if rng.random() < p:
                dropout = t
                break
        truth.append((cid, acquired, lam, p, math.exp(mu), dropout))
    return txns, truth


def main() -> None:
    txns, truth = simulate()
    DATA.mkdir(exist_ok=True)
    with (DATA / "transactions.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["customer_id", "week", "amount"])
        for cid, wk, amt in sorted(txns, key=lambda r: (r[0], r[1])):
            w.writerow([cid, f"{wk:.4f}", amt])
    with (DATA / "customers_truth.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["customer_id", "acquired_week", "true_lambda", "true_p", "true_mean_spend", "dropout_week"])
        for cid, acq, lam, p, mu, d in truth:
            w.writerow([cid, f"{acq:.4f}", f"{lam:.6f}", f"{p:.4f}", f"{mu:.2f}", "" if d == math.inf else f"{d:.4f}"])
    print(f"{len(txns)} transactions, {len(truth)} customers -> {DATA}")


if __name__ == "__main__":
    main()
