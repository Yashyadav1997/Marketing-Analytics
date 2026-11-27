"""The experiments the Module 6 lessons refer to.

    python experiments.py
"""
from __future__ import annotations

import mmm

N_TRAIN = 143   # first 143 weeks to fit; last 13 weeks held out
SIGMA = 260.0


def line(label, m, data):
    r = mmm.roi_table(m, data)
    cells = "  ".join(f"{c} {r[c]['est']:5.2f} (true {r[c]['true']:4.2f})" for c in mmm.CHANNELS)
    print(f"{label:34s} {cells} | holdout MAPE {100 * mmm.mape(m, data, N_TRAIN, len(data['sales'])):4.2f}%")


if __name__ == "__main__":
    d = mmm.load()
    free = mmm.fit(d, n_train=N_TRAIN)
    print("Fitted nonlinear parameters (true: tv 0.60/1100, social 0.30/700, search 0.10/450)")
    for c, (dec, K) in free["params"].items():
        print(f"  {c:7s} decay {dec:.2f}  K {K:6.0f}")
    print("\nAverage ROI = estimated contribution / spend over all 156 weeks\n")
    line("A. full model", free, d)
    line("B. no trend/seasonality controls", mmm.fit(d, n_train=N_TRAIN, controls=False), d)
    ok = {"tv": (4.47, 0.5, SIGMA), "social": (2.63, 0.5, SIGMA)}
    line("C. correct lift tests: tv, social", mmm.fit(d, n_train=N_TRAIN, calib=ok), d)
    line("D. WRONG lift test: social = 5.0", mmm.fit(d, n_train=N_TRAIN, calib={"social": (5.0, 0.5, SIGMA)}), d)
    line("E. all three lift-tested", mmm.fit(d, n_train=N_TRAIN, calib={**ok, "search": (2.39, 0.5, SIGMA)}), d)
    from generate import TRUTH, simulate
    alt = simulate(decouple_social=True)
    d2 = {"sales": alt["sales"], **{c: alt["spend"][c] for c in mmm.CHANNELS},
          **{"true_" + c: alt["contrib"][c] for c in mmm.CHANNELS}}
    print()
    line("F. social flighted independently", mmm.fit(d2, n_train=N_TRAIN), d2)
    from generate import TRUTH
    true_params = {c: (TRUTH[c]["decay"], TRUTH[c]["K"]) for c in mmm.CHANNELS}
    true_coef = [0.0] * free["n_ctrl"] + [TRUTH[c]["beta"] for c in mmm.CHANNELS]
    cal_all = mmm.fit(d, n_train=N_TRAIN, calib={**ok, "search": (2.39, 0.5, SIGMA)})
    print("\nMarginal ROI of the next unit of spend (+10% in every week); average ROI is higher for every channel")
    print(f"{'channel':8s} {'TRUE':>6s} {'uncalibrated':>13s} {'all lift-tested':>16s}")
    for c in mmm.CHANNELS:
        t = mmm.marginal_roi(free, d, c, params=true_params, coef=true_coef)
        print(f"{c:8s} {t:6.2f} {mmm.marginal_roi(free, d, c):13.2f} {mmm.marginal_roi(cal_all, d, c):16.2f}")
    starts = [mmm.fit(d, n_train=N_TRAIN, seed=s, max_iter=1500) for s in range(6)]
    spread = max(max(abs(mmm.roi_table(m, d)[c]["est"] - mmm.roi_table(free, d)[c]["est"]) for c in mmm.CHANNELS) for m in starts)
    print(f"\nSix random starting points: largest disagreement in any ROI = {spread:.3f} (the optimiser is not the problem)")
