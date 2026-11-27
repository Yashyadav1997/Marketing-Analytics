"""A compact media mix model: adstock + saturation + controls, fitted from scratch.

For each channel c with spend x_c(t):
    a_c(t) = x_c(t) + decay_c * a_c(t-1)           carry-over (adstock)
    s_c(t) = 1 - exp(-a_c(t) / K_c)                diminishing returns (saturation)
    sales(t) = intercept + trend + seasonality + sum_c beta_c * s_c(t) + noise

The nonlinear parameters (decay_c, K_c) are searched with Nelder-Mead; for every candidate the
linear coefficients (intercept, trend, seasonality, beta_c) are solved exactly by least squares,
which keeps the search small. Coefficients on channels are kept non-negative by dropping any
column that goes negative and refitting.

Only the standard library is used.
"""

from __future__ import annotations

import csv
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "module-07-cohorts-retention" / "code"))
from optimize import nelder_mead  # noqa: E402

DATA = Path(__file__).resolve().parent.parent / "data" / "weekly.csv"
CHANNELS = ["tv", "social", "search"]


def load(path: Path = DATA):
    with path.open() as fh:
        rows = list(csv.DictReader(fh))
    out = {"sales": [float(r["sales"]) for r in rows]}
    for c in CHANNELS:
        out[c] = [float(r[c]) for r in rows]
        out["true_" + c] = [float(r["true_" + c]) for r in rows]
    return out


# ------------------------------------------------------------------ transforms

def adstock(xs, decay):
    out, carry = [], 0.0
    for x in xs:
        carry = x + decay * carry
        out.append(carry)
    return out


def saturate(xs, K):
    return [1.0 - math.exp(-x / K) for x in xs]


def channel_column(spend, decay, K):
    return saturate(adstock(spend, decay), K)


# ------------------------------------------------------------------ linear algebra

def solve(A, b):
    """Gaussian elimination with partial pivoting."""
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for i in range(n):
        piv = max(range(i, n), key=lambda r: abs(M[r][i]))
        if abs(M[piv][i]) < 1e-12:
            M[piv][i] = 1e-12
        M[i], M[piv] = M[piv], M[i]
        for r in range(i + 1, n):
            f = M[r][i] / M[i][i]
            if f:
                for c in range(i, n + 1):
                    M[r][c] -= f * M[i][c]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (M[i][n] - sum(M[i][j] * x[j] for j in range(i + 1, n))) / M[i][i]
    return x


def least_squares(cols, y, ridge=1e-6):
    """Solve min ||y - X b||^2 for X given as a list of columns."""
    k = len(cols)
    XtX = [[sum(a * b for a, b in zip(cols[i], cols[j])) for j in range(k)] for i in range(k)]
    for i in range(k):
        XtX[i][i] += ridge * (XtX[i][i] + 1.0)
    Xty = [sum(a * b for a, b in zip(cols[i], y)) for i in range(k)]
    return solve(XtX, Xty)


# ------------------------------------------------------------------ the model

def control_columns(n, controls=True):
    cols = [[1.0] * n]
    if controls:
        cols.append([t / 100.0 for t in range(n)])
        cols.append([math.sin(2 * math.pi * t / 52) for t in range(n)])
        cols.append([math.cos(2 * math.pi * t / 52) for t in range(n)])
    return cols


def solve_linear(theta_cols, y, n_controls_cols, control_cols, calib=None, spend=None):
    """Fit controls and non-negative channel coefficients for fixed transforms.

    calib: optional dict channel -> (target_roi, se, sigma): adds a pseudo-observation that
    pulls that channel's average ROI towards a lift-test result.
    """
    cols = control_cols + theta_cols
    names = list(range(len(cols)))
    active = names[:]
    while True:
        sub = [cols[i] for i in active]
        ys = y[:]
        if calib:
            extra_rows = []
            for c, (target, se, sigma) in calib.items():
                j = CHANNELS.index(c)
                idx = n_controls_cols + j
                if idx not in active:
                    continue
                w = sigma / se
                total_spend = sum(spend[c][: len(y)])
                row = [0.0] * len(active)
                row[active.index(idx)] = w * sum(cols[idx]) / total_spend
                extra_rows.append((row, w * target))
            if extra_rows:
                sub = [col + [r[0][a] for r in extra_rows] for a, col in enumerate(sub)]
                ys = ys + [r[1] for r in extra_rows]
        beta = least_squares(sub, ys)
        bad = [active[i] for i, b in enumerate(beta) if active[i] >= n_controls_cols and b < 0]
        if not bad:
            full = [0.0] * len(cols)
            for i, b in zip(active, beta):
                full[i] = b
            return full
        active = [i for i in active if i not in bad]


def unpack(theta, base_scales):
    """theta = [u_decay_c, u_K_c ...] -> (decay_c in (0,0.95), K_c)."""
    params = {}
    for j, c in enumerate(CHANNELS):
        u, v = theta[2 * j], theta[2 * j + 1]
        decay = 0.95 / (1.0 + math.exp(-u))
        K = base_scales[c] * math.exp(max(-3.0, min(3.0, v)))
        params[c] = (decay, K)
    return params


def build_theta_cols(spend, params):
    return [channel_column(spend[c], *params[c]) for c in CHANNELS]


def fit(data, n_train=None, controls=True, start=None, calib=None, seed=None, max_iter=900):
    """Fit on the first n_train weeks. Returns a model dict."""
    n_total = len(data["sales"])
    n = n_train or n_total
    y = data["sales"][:n]
    spend = {c: data[c][:n] for c in CHANNELS}
    base_scales = {c: max(1.0, sum(adstock(spend[c], 0.4)) / n) for c in CHANNELS}
    ctrl = control_columns(n, controls)
    n_ctrl = len(ctrl)

    sigma = 260.0

    def data_sse_and_penalty(theta):
        params = unpack(theta, base_scales)
        tcols = build_theta_cols(spend, params)
        beta = solve_linear(tcols, y, n_ctrl, ctrl, calib, spend)
        cols = ctrl + tcols
        fitted = [sum(beta[i] * cols[i][t] for i in range(len(cols))) for t in range(n)]
        sse = sum((a - b) ** 2 for a, b in zip(y, fitted))
        pen = 0.0
        for c, (target, se, sg) in (calib or {}).items():
            j = CHANNELS.index(c)
            roi = beta[n_ctrl + j] * sum(tcols[j]) / sum(spend[c])
            pen += (sg / se * (roi - target)) ** 2
        return sse, pen

    def objective(theta):
        sse, pen = data_sse_and_penalty(theta)
        return sse + pen   # the lift-test pseudo-observation is part of what is being minimised

    if start is None:
        start = [0.0, 0.0] * len(CHANNELS)
        if seed is not None:
            rng = random.Random(seed)
            start = [rng.uniform(-2, 2) for _ in start]
    theta, sse = nelder_mead(objective, start, step=0.7, tol=1e-6, max_iter=max_iter)
    params = unpack(theta, base_scales)
    data_sse, _ = data_sse_and_penalty(theta)
    return dict(params=params, sse=data_sse, objective=sse, n_train=n, controls=controls, base_scales=base_scales,
                calib=calib, n_ctrl=n_ctrl, coef=_coefs(data, params, controls, n, calib))


def _coefs(data, params, controls, n, calib):
    y = data["sales"][:n]
    spend = {c: data[c][:n] for c in CHANNELS}
    ctrl = control_columns(n, controls)
    return solve_linear(build_theta_cols(spend, params), y, len(ctrl), ctrl, calib, spend)


def predict(model, data):
    n = len(data["sales"])
    ctrl = control_columns(n, model["controls"])
    cols = ctrl + build_theta_cols({c: data[c] for c in CHANNELS}, model["params"])
    beta = model["coef"]
    return [sum(beta[i] * cols[i][t] for i in range(len(cols))) for t in range(n)], cols, beta


def contributions(model, data):
    """Estimated contribution of each channel by week, over the full sample."""
    _, cols, beta = predict(model, data)
    nc = model["n_ctrl"]
    return {c: [beta[nc + j] * v for v in cols[nc + j]] for j, c in enumerate(CHANNELS)}


def roi_table(model, data):
    est = contributions(model, data)
    out = {}
    for c in CHANNELS:
        spend_total = sum(data[c])
        out[c] = dict(est=sum(est[c]) / spend_total, true=sum(data["true_" + c]) / spend_total)
    return out


def mape(model, data, start, end):
    fitted, _, _ = predict(model, data)
    y = data["sales"]
    return sum(abs(fitted[t] - y[t]) / y[t] for t in range(start, end)) / (end - start)


def marginal_roi(model, data, channel, bump=0.10, params=None, coef=None):
    """Extra sales per extra unit of spend if `channel` spend is raised by `bump` in every week.

    Differs from average ROI whenever the response curve is saturating. Pass `params` (decay, K per
    channel) and `coef` to evaluate a different curve, for example the true one.
    """
    params = params or model["params"]
    coef = coef or model["coef"]
    j = CHANNELS.index(channel)
    nc = model["n_ctrl"]
    base = channel_column(data[channel], *params[channel])
    up = channel_column([x * (1 + bump) for x in data[channel]], *params[channel])
    delta_sales = coef[nc + j] * (sum(up) - sum(base))
    return delta_sales / (bump * sum(data[channel]))
