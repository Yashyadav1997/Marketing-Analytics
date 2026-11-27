# Module 3. Measurement design and tracking foundations

## Why this module sits underneath the others

Every earlier calculation (CAC, cohort retention, attribution, incrementality) assumed that someone had counted the sales and the customers correctly. This module is about whether they did. Tracking fails quietly: a dashboard with a duplicated purchase event or an unrecognised event name still draws a smooth chart. The failures that matter most are also the least visible, such as the share of customers who never appear in the data at all.

The module builds a simulated store's analytics export with defects injected at known rates, then audits it, then reconciles it against the true ledger. The central finding is uncomfortable: a perfect audit still leaves a quarter of revenue untracked, and cleaning the data can make the headline number look *worse*.

## Outcomes

1. Derive a tracking specification from a strategy, so every metric traces to an assumption and every event to a metric.
2. Audit an export against a written spec, and say what an audit can and cannot detect.
3. Reconcile analytics revenue with the ledger, itemising each gap by cause.
4. Measure how much device-level counts overstate people, and what login stitching recovers.
5. Treat consent and privacy as constraints on the design, not as afterthoughts.

## Contents

| Part | File | Time |
|---|---|---|
| Lesson 1 | [From strategy to a tracking spec](lesson-1-from-strategy-to-spec.md) | 60 min |
| Lesson 2 | [Auditing what you can see](lesson-2-auditing.md) | 60 min |
| Lesson 3 | [Reconciliation, identity and the invisible gap](lesson-3-reconciliation-and-identity.md) | 75 min |
| Exercises | [exercises.md](exercises.md) | 3 to 4 hours |
| Code | [code/](code/) | reference |

## Running it

Standard library only.

```bash
cd course/module-03-measurement/code
python3 -m unittest -v     # 10 tests
python3 simulate.py        # counts of events and injected defects
python3 audit.py           # audit scored against the injected truth
python3 reconcile.py       # ledger-to-dashboard waterfall and identity counts
```

## The simulated store

20,000 people, 28 days, about 130,000 events. People may decline consent (18%), run ad blockers (8%), use a second device (30%), and hold an account they log in to in some sessions (60% have one, logging in on 70% of sessions). Fifteen bot devices generate page views. Events then carry defects at known rates: unrecognised or inconsistently written event names, missing transaction ids, duplicate purchase events, values written as text, missing currency, and impossible timestamps. A side table labels every defective event and the ledger records every real purchase, tracked or not.

Rates and revenue are invented. They are chosen to be plausible, not to be benchmarks; real consent and blocking rates vary widely by market, audience and consent design.

This module describes technical measurement practice. It is not legal advice, and consent requirements differ by jurisdiction.
