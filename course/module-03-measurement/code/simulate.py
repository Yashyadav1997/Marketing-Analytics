"""Simulate a store's analytics export with known, labelled tracking defects.

People shop on one or two devices, some log in, some decline consent, some run ad blockers, and a
few "devices" are bots. Events are then emitted with realistic defects at known rates. Alongside the
export we keep (a) the true ledger of every real purchase and (b) a label for every defective event,
so audits can be scored against the truth. Invented figures throughout.

    python simulate.py      # prints a summary
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field

SEED = 3_2026
N_PEOPLE = 20000
DAYS = 28
P_DECLINE_CONSENT = 0.18
P_ADBLOCK = 0.08
P_SECOND_DEVICE = 0.30
P_LOGGED_IN = 0.60        # has an account
P_LOGIN_SESSION = 0.70    # given an account, logged in during a given session
N_BOTS = 15

# defect rates (per eligible event unless noted)
R_NAME_VARIANT = 0.02
R_MISSING_TID = 0.03
R_DUPLICATE = 0.04
R_VALUE_STRING = 0.02
R_MISSING_CURRENCY = 0.03
R_BAD_TS = 0.01

NAME_VARIANTS = ["Purchase", "purchase ", "purchase_complete"]


@dataclass
class Dataset:
    events: list[dict]
    labels: dict[str, set[str]]           # defect -> set of event_ids carrying it
    ledger: list[dict]                    # every real purchase, tracked or not
    people: dict[int, dict] = field(default_factory=dict)


def simulate(n_people: int = N_PEOPLE, seed: int = SEED) -> Dataset:
    rng = random.Random(seed)
    events: list[dict] = []
    labels: dict[str, set[str]] = {k: set() for k in
        ["name_variant", "missing_tid", "duplicate", "value_string", "missing_currency", "bad_ts", "bot"]}
    ledger, people = [], {}
    seq = [0]
    horizon = DAYS * 86400.0

    def emit(name, ts, device, user_id, params, defect_ok=True):
        seq[0] += 1
        ev = dict(event_id=f"e{seq[0]}", name=name, ts=ts, device=device, user_id=user_id, params=params)
        events.append(ev)
        return ev

    for pid in range(n_people):
        consent = rng.random() > P_DECLINE_CONSENT
        blocked = rng.random() < P_ADBLOCK
        n_dev = 2 if rng.random() < P_SECOND_DEVICE else 1
        devices = [f"d{pid}_{k}" for k in range(n_dev)]
        user_id = f"u{pid}" if rng.random() < P_LOGGED_IN else None
        people[pid] = dict(devices=devices, user_id=user_id, consent=consent, blocked=blocked)
        for _ in range(rng.choice([1, 1, 2, 2, 3, 4])):             # sessions
            t0 = rng.uniform(0, horizon - 3600)
            dev = rng.choice(devices)
            uid = user_id if (user_id is not None and rng.random() < P_LOGIN_SESSION) else None
            visible = consent and not blocked
            t = t0
            def step():
                nonlocal t
                t += rng.uniform(5, 90)
                return t
            for _ in range(rng.randint(1, 5)):
                if visible:
                    emit("page_view", step(), dev, uid, {"page_location": f"/p/{rng.randint(1, 80)}"})
            if rng.random() < 0.45:
                item = f"sku{rng.randint(1, 60)}"
                if visible:
                    emit("view_item", step(), dev, uid, {"item_id": item})
                if rng.random() < 0.45:
                    value = round(math.exp(rng.gauss(math.log(1200), 0.45)), 2)
                    if visible:
                        emit("add_to_cart", step(), dev, uid, {"item_id": item, "value": value})
                    if rng.random() < 0.55:
                        if visible:
                            emit("begin_checkout", step(), dev, uid, {"value": value})
                        if rng.random() < 0.60:
                            tid = f"T{len(ledger) + 1:06d}"
                            ts = step()
                            ledger.append(dict(transaction_id=tid, value=value, person=pid, ts=ts))
                            if visible:
                                _emit_purchase(rng, emit, labels, ts, dev, uid, tid, value, horizon)
    # bots: a handful of devices hammering page_view
    for b in range(N_BOTS):
        dev = f"bot{b}"
        day = rng.randint(0, DAYS - 1)
        for _ in range(rng.randint(150, 400)):
            ev = emit("page_view", day * 86400 + rng.uniform(0, 3600), dev, None, {"page_location": f"/p/{rng.randint(1, 80)}"})
            labels["bot"].add(ev["event_id"])
    rng.shuffle(events)       # exports are not neatly ordered
    return Dataset(events, labels, ledger, people)


def _emit_purchase(rng, emit, labels, ts, dev, user_id, tid, value, horizon):
    params = {"transaction_id": tid, "value": value, "currency": "INR"}
    name, defects = "purchase", []
    if rng.random() < R_NAME_VARIANT:
        name = rng.choice(NAME_VARIANTS)
        defects.append("name_variant")
    if rng.random() < R_MISSING_TID:
        del params["transaction_id"]
        defects.append("missing_tid")
    if rng.random() < R_VALUE_STRING:
        params["value"] = f"{value:,.2f}"
        defects.append("value_string")
    if rng.random() < R_MISSING_CURRENCY:
        del params["currency"]
        defects.append("missing_currency")
    ts_out = ts
    if rng.random() < R_BAD_TS:
        ts_out = horizon + rng.uniform(3600, 86400 * 3)
        defects.append("bad_ts")
    ev = emit(name, ts_out, dev, user_id, params)
    for d in defects:
        labels[d].add(ev["event_id"])
    if rng.random() < R_DUPLICATE and "missing_tid" not in defects:
        for _ in range(rng.choice([1, 1, 2])):
            dup = emit(name, ts_out + rng.uniform(0.2, 4), dev, user_id, dict(params))
            labels["duplicate"].add(dup["event_id"])
            for d in defects:
                labels[d].add(dup["event_id"])


if __name__ == "__main__":
    ds = simulate()
    print(f"{len(ds.events):,} events, {len(ds.ledger):,} real purchases in the ledger")
    for k, v in ds.labels.items():
        print(f"  injected {k:17s}: {len(v):6,d} events")
