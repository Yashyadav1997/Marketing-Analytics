"""How many people are there? Device-level counts versus stitched identities versus the truth.

Analytics tools count browser/device identifiers. Where a login identifier is available, devices
that share it can be merged (union-find). Customers who never log in, or who log in on one device
only, stay split.
"""

from __future__ import annotations

from collections import defaultdict

from simulate import Dataset


class UnionFind:
    def __init__(self):
        self.parent = {}

    def find(self, x):
        self.parent.setdefault(x, x)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra


def stitch(events: list[dict]) -> dict[str, str]:
    """device -> stitched identity, merging devices that ever appear with the same user_id."""
    uf = UnionFind()
    for e in events:
        uf.find(e["device"])
        if e["user_id"] is not None:
            uf.union(e["device"], "user:" + e["user_id"])
    return {e["device"]: uf.find(e["device"]) for e in events}


def people_counts(ds: Dataset, clean_events: list[dict]) -> dict[str, int]:
    """Visible-person counts three ways, ignoring bot devices (identified by name for this demo)."""
    ev = [e for e in clean_events if not e["device"].startswith("bot")]
    devices = {e["device"] for e in ev}
    ident = stitch(ev)
    stitched = len(set(ident.values()))
    visible_people = {pid for pid, p in ds.people.items()
                      if any(d in devices for d in p["devices"])}
    return dict(devices=len(devices), stitched=stitched, true_people=len(visible_people))


def repeat_buyer_rate(ds: Dataset, purchase_events: list[dict], by: str) -> float:
    """Share of buyers with 2+ purchases, with 'buyer' defined by device, stitched identity, or true person."""
    ident = stitch([e for e in purchase_events])
    dev_to_person = {d: pid for pid, p in ds.people.items() for d in p["devices"]}
    counts = defaultdict(int)
    for e in purchase_events:
        key = {"device": e["device"], "stitched": ident[e["device"]], "person": dev_to_person[e["device"]]}[by]
        counts[key] += 1
    return sum(1 for n in counts.values() if n >= 2) / len(counts)
