"""Cohort tables and exposure-aware repeat rates from a transaction log.

    python cohorts.py
"""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

from simulate import CAL_END, END

DATA = Path(__file__).resolve().parent.parent / "data"
BLOCK = 4.0  # weeks per period


def load_transactions(path: Path | None = None) -> dict[int, list[tuple[float, float]]]:
    """customer_id -> sorted list of (week, amount)."""
    out: dict[int, list[tuple[float, float]]] = defaultdict(list)
    with (path or DATA / "transactions.csv").open() as fh:
        for r in csv.DictReader(fh):
            out[int(r["customer_id"])].append((float(r["week"]), float(r["amount"])))
    for v in out.values():
        v.sort()
    return out


def cohort_table(txns, horizon: float = END, block: float = BLOCK, max_age: int = 10):
    """Active-rate table. Rows: acquisition block. Columns: age in periods (1..max_age).

    A customer's period k covers weeks (a + block*(k-1), a + block*k] from their own
    first purchase a. A cell is reported only if *every* customer in the cohort has
    been observable for the whole period; otherwise it is None. That rule is what
    stops young cohorts from dragging the averages down (right-censoring).
    """
    cohorts: dict[int, list[list[float]]] = defaultdict(list)
    for orders in txns.values():
        a = orders[0][0]
        cohorts[int(a // block)].append([t for t, _ in orders[1:]] + [a])
    table = {}
    for c, custs in sorted(cohorts.items()):
        row = []
        for k in range(1, max_age + 1):
            observable, active = 0, 0
            for ts in custs:
                a = ts[-1]
                if a + block * k > horizon:
                    continue
                observable += 1
                lo, hi = a + block * (k - 1), a + block * k
                active += any(lo < t <= hi for t in ts[:-1])
            row.append(None if observable < len(custs) else active / len(custs))
        table[c] = (len(custs), row)
    return table


def exposure_adjusted_rate(txns, cal_end: float = CAL_END) -> float:
    """Repeat purchases per customer-week, using each customer's actual exposure."""
    repeats = exposure = 0.0
    for orders in txns.values():
        a = orders[0][0]
        if a >= cal_end:  # not yet acquired at the cutoff: no exposure
            continue
        repeats += sum(1 for t, _ in orders[1:] if t <= cal_end)
        exposure += cal_end - a
    return repeats / exposure


def naive_repeats_per_customer(txns, cal_end: float = CAL_END) -> float:
    """What a careless report shows: total repeats / customers, ignoring exposure."""
    total = sum(sum(1 for t, _ in o[1:] if t <= cal_end) for o in txns.values())
    return total / len(txns)


def main() -> None:
    txns = load_transactions()
    table = cohort_table(txns)
    print("cohort (4-week block) | n | share ordering in period k since first purchase")
    for c, (n, row) in table.items():
        cells = " ".join("  .  " if v is None else f"{100*v:4.1f}%" for v in row)
        print(f"{c:>3} {n:>5} | {cells}")
    rate = exposure_adjusted_rate(txns)
    print(f"\nexposure-adjusted repeat rate: {rate:.4f} per customer-week "
          f"(~{rate*52:.2f} per year)")
    print(f"naive repeats per customer in calibration window: {naive_repeats_per_customer(txns):.3f}")


if __name__ == "__main__":
    main()
