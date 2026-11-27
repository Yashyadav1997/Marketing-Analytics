"""A small Nelder-Mead minimiser so the course needs nothing beyond the standard library."""

from __future__ import annotations

from typing import Callable, Sequence


def nelder_mead(
    f: Callable[[Sequence[float]], float],
    x0: Sequence[float],
    step: float = 0.3,
    tol: float = 1e-8,
    max_iter: int = 2000,
) -> tuple[list[float], float]:
    n = len(x0)
    simplex = [list(x0)]
    for i in range(n):
        p = list(x0)
        p[i] += step
        simplex.append(p)
    vals = [f(p) for p in simplex]
    for _ in range(max_iter):
        order = sorted(range(n + 1), key=vals.__getitem__)
        simplex = [simplex[i] for i in order]
        vals = [vals[i] for i in order]
        if abs(vals[-1] - vals[0]) < tol:
            break
        centroid = [sum(p[j] for p in simplex[:-1]) / n for j in range(n)]
        worst = simplex[-1]

        def move(c: float) -> list[float]:
            return [centroid[j] + c * (worst[j] - centroid[j]) for j in range(n)]

        xr = move(-1.0)
        fr = f(xr)
        if fr < vals[0]:
            xe = move(-2.0)
            fe = f(xe)
            simplex[-1], vals[-1] = (xe, fe) if fe < fr else (xr, fr)
        elif fr < vals[-2]:
            simplex[-1], vals[-1] = xr, fr
        else:
            xc = move(0.5 if fr >= vals[-1] else -0.5)
            fc = f(xc)
            if fc < min(fr, vals[-1]):
                simplex[-1], vals[-1] = xc, fc
            else:  # shrink toward the best point
                best = simplex[0]
                simplex = [best] + [
                    [best[j] + 0.5 * (p[j] - best[j]) for j in range(n)] for p in simplex[1:]
                ]
                vals = [vals[0]] + [f(p) for p in simplex[1:]]
    i = min(range(n + 1), key=vals.__getitem__)
    return simplex[i], vals[i]
