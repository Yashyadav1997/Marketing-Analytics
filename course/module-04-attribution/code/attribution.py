"""Rule-based attribution models and a reconciliation report.

    python attribution.py
"""

from __future__ import annotations

from collections import defaultdict

from world import CHANNELS, REVENUE_PER_ORDER, User, simulate, spend, true_incremental, true_programme_incremental


def last_click(touches):
    return {touches[-1]: 1.0} if touches else {}


def first_click(touches):
    return {touches[0]: 1.0} if touches else {}


def linear(touches):
    return {c: 1.0 / len(touches) for c in touches} if touches else {}


def position_based(touches):
    """40% first, 40% last, 20% shared across the middle; 1 touch gets 100%, 2 touches 50/50."""
    n = len(touches)
    if n == 0:
        return {}
    if n == 1:
        return {touches[0]: 1.0}
    if n == 2:
        return {touches[0]: 0.5, touches[1]: 0.5}
    credit = defaultdict(float)
    credit[touches[0]] += 0.4
    credit[touches[-1]] += 0.4
    for c in touches[1:-1]:
        credit[c] += 0.2 / (n - 2)
    return dict(credit)


def any_touch(touches):
    """What each platform reports about itself: full credit whenever it had a touch.
    Credit sums to more than the number of orders because platforms do not deduplicate each other."""
    return {c: 1.0 for c in touches}


MODELS = {
    "last-click": last_click,
    "first-click": first_click,
    "linear": linear,
    "position-based": position_based,
    "platform (any touch)": any_touch,
}


def credit_by_channel(users: list[User], model) -> dict[str, float]:
    out = {c: 0.0 for c in CHANNELS}
    for u in users:
        if u.converted:
            for c, w in model(u.touches).items():
                out[c] += w
    return out


def report(users: list[User]) -> None:
    sp = spend(users)
    truth = true_incremental(users)
    orders = sum(u.converted for u in users)
    untouched = sum(1 for u in users if u.converted and not u.touches)
    print(f"{len(users):,} users, {orders:,} orders ({untouched:,} with no tracked touch)\n")

    print("Credited orders by model (platform row sums to more than the real total)")
    header = f"{'channel':15s}" + "".join(f"{m[:14]:>16s}" for m in MODELS) + f"{'TRUE incr.':>12s}"
    print(header)
    credits = {m: credit_by_channel(users, f) for m, f in MODELS.items()}
    for c in CHANNELS:
        print(f"{c:15s}" + "".join(f"{credits[m][c]:16.0f}" for m in MODELS) + f"{truth[c]:12d}")
    print(f"{'sum':15s}" + "".join(f"{sum(credits[m].values()):16.0f}" for m in MODELS) + f"{sum(truth.values()):12d}")

    print("\nROAS = credited revenue / spend")
    print(f"{'channel':15s}{'spend':>10s}" + "".join(f"{m[:14]:>16s}" for m in MODELS) + f"{'TRUE iROAS':>12s}")
    for c in CHANNELS:
        row = f"{c:15s}{sp[c]:10,.0f}"
        for m in MODELS:
            row += f"{credits[m][c] * REVENUE_PER_ORDER / sp[c]:16.2f}"
        row += f"{truth[c] * REVENUE_PER_ORDER / sp[c]:12.2f}"
        print(row)

    total_sp = sum(sp.values())
    print(f"\nBlended MER (all revenue / all spend): {orders * REVENUE_PER_ORDER / total_sp:.2f}")
    prog = true_programme_incremental(users)
    print(f"True incremental ROAS of the whole programme: {prog * REVENUE_PER_ORDER / total_sp:.2f} "
          f"({prog:,} orders vanish if every channel is switched off, {prog / orders:.1%} of all orders)")
    print(f"Sum of the per-channel incremental figures: {sum(truth.values()):,} "
          f"(larger than {prog:,} because overlapping channels each 'save' the same order)")


if __name__ == "__main__":
    report(simulate())
