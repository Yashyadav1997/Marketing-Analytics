"""A simulated marketing world with known causal effects.

Every user has a latent purchase intent (high or low). Channels reach users
selectively: brand search and email mostly reach people who were already likely
to buy, which is exactly what makes them look good in observational reports.

Each channel adds a true, additive lift to the user's purchase probability.
One uniform draw u per user decides the outcome under every scenario
(common random numbers), so we can compute, for each channel, whether the user
would still have bought without it. That is the potential-outcomes ground truth
that real data never provides.

All figures are invented; nothing here is a benchmark.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field

CHANNELS = ["influencer", "paid_social", "search_generic", "email", "search_brand"]

# Probability of being exposed, by intent; true lift on purchase probability, by intent;
# cost per exposed user; typical position in the journey (0 = early, 1 = late).
SPEC = {
    #                  exp_hi exp_lo  lift_hi lift_lo  cost  position
    "influencer":     (0.06,  0.08,   0.030,  0.030,  120.0, 0.10),
    "paid_social":    (0.30,  0.35,   0.040,  0.030,   20.0, 0.20),
    "search_generic": (0.12,  0.10,   0.020,  0.020,   60.0, 0.50),
    "email":          (0.50,  0.10,   0.030,  0.004,    2.0, 0.65),
    "search_brand":   (0.60,  0.02,   0.010,  0.005,   15.0, 0.90),
}
P_HIGH_INTENT = 0.25
BASE = {"hi": 0.20, "lo": 0.012}
REVENUE_PER_ORDER = 1000.0
CAP = 0.95


@dataclass
class User:
    uid: int
    intent: str                       # "hi" or "lo"
    touches: list[str]                # exposures in journey order (after any suppression)
    converted: bool                   # outcome under the exposures actually delivered
    without: dict[str, bool] = field(default_factory=dict)  # would they convert if this channel were removed?
    held_out: bool = False            # True if randomly withheld from the experiment channel
    organic: bool = False             # would they convert with no marketing at all?


def _prob(intent: str, exposed: set[str]) -> float:
    k = 0 if intent == "hi" else 1
    p = BASE[intent] + sum(SPEC[c][2 + k] for c in exposed)
    return min(CAP, p)


def simulate(
    n: int = 50_000,
    seed: int = 4_2026,
    experiment: tuple[str, float] | None = None,
) -> list[User]:
    """experiment=(channel, holdout_fraction): randomly withhold `channel` from that
    fraction of users (a user-level holdout). Everything else about the user is unchanged,
    because the exposure and outcome draws are made before the holdout is applied.
    """
    rng = random.Random(seed)
    users = []
    for uid in range(n):
        intent = "hi" if rng.random() < P_HIGH_INTENT else "lo"
        k = 0 if intent == "hi" else 1
        natural = {c for c in CHANNELS if rng.random() < SPEC[c][k]}
        u = rng.random()
        order_noise = {c: SPEC[c][5] + rng.gauss(0, 0.15) for c in CHANNELS if c in natural}  # fixed order: reproducible
        held = False
        if experiment is not None:
            ch, frac = experiment
            held = rng.random() < frac
            exposed = natural - {ch} if held else natural
        else:
            exposed = natural
        touches = sorted((c for c in CHANNELS if c in exposed), key=lambda c: order_noise[c])
        converted = u < _prob(intent, exposed)
        without = {c: u < _prob(intent, exposed - {c}) for c in CHANNELS}
        organic = u < _prob(intent, set())
        users.append(User(uid, intent, touches, converted, without, held, organic))
    return users


def spend(users: list[User]) -> dict[str, float]:
    out = {c: 0.0 for c in CHANNELS}
    for u in users:
        for c in u.touches:
            out[c] += SPEC[c][4]
    return out


def true_incremental(users: list[User]) -> dict[str, int]:
    """Orders that would not have happened without each channel (ground truth)."""
    out = {c: 0 for c in CHANNELS}
    for u in users:
        if u.converted:
            for c in u.touches:
                if not u.without[c]:
                    out[c] += 1
    return out


def true_programme_incremental(users: list[User]) -> int:
    """Orders that would vanish if every channel were switched off together.

    This is smaller than the sum of the per-channel figures whenever channels overlap,
    because an order that two channels could each have 'saved' is still just one order.
    """
    return sum(1 for u in users if u.converted and not u.organic)
