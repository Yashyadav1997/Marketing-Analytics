"""Reference for Exercise 4: what a promotion in the holdout does to a forecast.

The model is fitted on a calibration window that contains no promotion, then asked
to forecast a holdout in which a promotion lifts purchase rates. The forecast is
blind to the promotion by construction.

    python misspecification.py
"""

from __future__ import annotations

import bgnbd
from simulate import CAL_END, END, simulate
from test_module7 import calibration_data


def run(label, promo):
    txns, _ = simulate(promo=promo)
    data, holdout = calibration_data(txns)
    params, _ = bgnbd.fit(data)
    pred = sum(bgnbd.expected_purchases(params, *d, END - CAL_END) for d in data)
    actual = sum(holdout)
    print(f"{label:34s} forecast {pred:7.0f}  actual {actual:6d}  error {100*(pred-actual)/actual:+5.1f}%")


if __name__ == "__main__":
    run("no promotion", None)
    run("promo wk 60-64, rates x2", (60.0, 64.0, 2.0))
    run("promo wk 60-64, rates x3", (60.0, 64.0, 3.0))
    run("promo wk 20-24 (in calibration), x3", (20.0, 24.0, 3.0))
