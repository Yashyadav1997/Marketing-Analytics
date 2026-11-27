"""Audit an event export against the written spec and score the audit against the injected truth.

    python audit.py
"""

from __future__ import annotations

from collections import Counter, defaultdict

from simulate import DAYS, Dataset, simulate
from spec import SPEC

BOT_EVENTS_PER_DEVICE = 100
HORIZON = DAYS * 86400.0


def canonical(name: str):
    """Spec name this event name maps to after trimming and lower-casing, else None."""
    n = name.strip().lower()
    return n if n in SPEC else None


def _type_ok(value, expected) -> bool:
    if expected is float:
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    return isinstance(value, expected)


def run_audit(events: list[dict]) -> dict[str, set[str]]:
    found = {k: set() for k in
             ["name_variant", "missing_tid", "duplicate", "value_string", "missing_currency", "bad_ts", "bot"]}
    purchases_by_tid = defaultdict(list)
    per_device = Counter(e["device"] for e in events)
    bots = {d for d, n in per_device.items() if n > BOT_EVENTS_PER_DEVICE}

    for e in events:
        eid, name, p = e["event_id"], e["name"], e["params"]
        if name not in SPEC:
            found["name_variant"].add(eid)           # not an exact spec name (includes unmappable ones)
        c = canonical(name)
        if c is not None:
            for param, typ in SPEC[c].items():
                if param not in p:
                    if param == "transaction_id":
                        found["missing_tid"].add(eid)
                    elif param == "currency":
                        found["missing_currency"].add(eid)
                elif not _type_ok(p[param], typ) and param == "value":
                    found["value_string"].add(eid)
            if c == "purchase" and "transaction_id" in p:
                purchases_by_tid[p["transaction_id"]].append(e)
        if not (0 <= e["ts"] <= HORIZON):
            found["bad_ts"].add(eid)
        if e["device"] in bots:
            found["bot"].add(eid)

    for group in purchases_by_tid.values():
        if len(group) > 1:
            group.sort(key=lambda e: e["ts"])
            for extra in group[1:]:
                found["duplicate"].add(extra["event_id"])
    return found


def score(found: dict[str, set[str]], labels: dict[str, set[str]]):
    rows = []
    for k in labels:
        tp = len(found[k] & labels[k])
        fp = len(found[k] - labels[k])
        fn = len(labels[k] - found[k])
        prec = tp / (tp + fp) if tp + fp else float("nan")
        rec = tp / (tp + fn) if tp + fn else float("nan")
        rows.append((k, len(labels[k]), len(found[k]), tp, prec, rec))
    return rows


def main(ds: Dataset | None = None):
    ds = ds or simulate()
    found = run_audit(ds.events)
    print(f"{len(ds.events):,} events audited against the spec\n")
    print(f"{'defect':18s} {'injected':>9s} {'flagged':>8s} {'caught':>7s} {'precision':>10s} {'recall':>8s}")
    for k, inj, flg, tp, pr, rc in score(found, ds.labels):
        print(f"{k:18s} {inj:9d} {flg:8d} {tp:7d} {pr:10.1%} {rc:8.1%}")


if __name__ == "__main__":
    main()
