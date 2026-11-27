"""Profile the data's ability to pin down each channel's return.

For a range of assumed average ROIs for one channel, force the model to that value (a very
tight lift-test pseudo-observation) and refit everything else. The rise in squared error,
measured in units of the noise variance, says how strongly the data object to that value.
Values whose error rise is under about 3.84 (the 95% point of a chi-square with one degree of
freedom) cannot be ruled out. This assumes the noise variance is known (260^2 here).

    python profile.py [channel]
"""
from __future__ import annotations

import sys

import mmm

SIGMA = 260.0


def profile(data, channel, grid, n_train=None):
    n = n_train or len(data["sales"])
    free = mmm.fit(data, n_train=n)
    out = []
    for target in grid:
        m = mmm.fit(data, n_train=n, calib={channel: (target, 0.02, SIGMA)})
        roi = mmm.roi_table(m, data)[channel]["est"]
        out.append((target, roi, (m["sse"] - free["sse"]) / SIGMA**2))
    return free, out


if __name__ == "__main__":
    data = mmm.load()
    chans = sys.argv[1:] or mmm.CHANNELS
    truth = mmm.roi_table(mmm.fit(data), data)
    for ch in chans:
        free, rows = profile(data, ch, [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 6.0, 7.0], n_train=143)
        print(f"\n{ch}: free-fit ROI {mmm.roi_table(free, data)[ch]['est']:.2f}, true {truth[ch]['true']:.2f}")
        print(f"{'assumed ROI':>12s} {'error rise (x sigma^2)':>24s}  {'plausible at 95%?':>18s}")
        for target, roi, rise in rows:
            print(f"{target:12.1f} {rise:24.1f}  {'yes' if rise < 3.84 else 'no':>18s}")
