# Lesson 3. Reconciliation, identity and the invisible gap

## The waterfall

`reconcile.py` starts from the ledger, the finance record of every real sale, and walks to the number the analytics dashboard shows:

| Step | Revenue | Share of ledger |
|---|---|---|
| Ledger revenue (truth) | 3,844,555 | 100.0% |
| less: consent declined or ad-blocked | −921,394 | −24.0% |
| = revenue that could be tracked | 2,923,161 | 76.0% |
| less: lost to name and format defects | −115,565 | −3.0% |
| plus: duplicate purchase events | +126,376 | +3.3% |
| = naive dashboard revenue | 2,933,972 | 76.3% |
| Cleaned revenue (after audit fixes) | 2,923,161 | 76.0% |

Two observations carry most of the weight.

## The errors cancelled

Defects that lose revenue (−3.0%) and defects that add it (+3.3%) almost exactly offset. The naive dashboard sits at 76.3% of the ledger; the cleaned data at 76.0%. The cleaning, which fixed real faults, made the headline number slightly *less* close to the ledger.

This is a pattern worth fearing. A team that checks its dashboard against finance, finds a gap of a few points, and stops has verified nothing: the agreement is a coincidence of offsetting errors, and it will break the day a release removes one source of error but not the other. A reconciliation is only informative when each gap is itemised and its cause explained, as in the table. A match with no itemisation is not evidence of correctness.

The cleaned figure also matches the "could be tracked" figure to the rupee, which is a useful check on the cleaning itself: after normalising names, parsing text values, dropping bots and removing duplicate transaction ids, nothing should remain unexplained.

## The gap that cleaning cannot touch

The first line of the waterfall dominates. Nearly a quarter of revenue (24.0%) came from people who declined consent or ran blockers, and none of those events reached the analytics tool. With the simulation's 18% decline and 8% blocking, independence would predict a loss of about 24.6% (1 − 0.82 × 0.92); the observed 24.0% is within sampling noise of that.

Several consequences:

- **Analytics revenue is a floor, not an estimate.** Treating it as total revenue understates the business by roughly a quarter here.
- **Ratios are biased in non-obvious ways.** Conversion rate (tracked purchases over tracked sessions) may be roughly right if blocked and unblocked visitors convert similarly, and wrong if they do not. People who decline tracking are not a random sample. Nothing in the tracked data can tell you which case you are in.
- **Platform ROAS inherits the problem.** Any attribution that relies on tracked conversions undercounts conversions in exactly the segments that opted out, which Module 4's calibration against experiments and Module 6's aggregate modelling partly sidestep.
- **Remedies exist but are partial**: server-side tagging, conversion imports from the order system (which see every sale regardless of browser state), modelled conversions where a tool offers them, and consent designs that earn more opt-ins. Each has costs, and each should be described to stakeholders as what it is, an estimate rather than a measurement.

The principle for reporting: always show the **ledger as the anchor** and the tracked share as a labelled fraction of it, not as a replacement for it.

## Identity: how many people are there?

Analytics tools count device or browser identifiers. Someone who shops on a phone and a laptop appears as two. `identity.py` merges devices that ever appear with the same login identifier (a union-find over devices and user ids).

Among the people who left any tracked trace, with bots excluded:

| Count | Value | Versus truth |
|---|---|---|
| True people | 15,136 | |
| Device identifiers | 17,197 | +13.6% |
| After login stitching | 16,423 | +8.5% |

Stitching recovers about 38% of the overcount (774 of 2,061 surplus identifiers) and then stops. The remainder are people who never logged in, or logged in on one device only, and no rule can recover them from what is in the data.

The error compounds in person-level metrics. The share of buyers with two or more purchases in the window is 5.4% counting devices, 5.8% after stitching, and 6.0% counting true people. Counting devices makes customers look less loyal than they are, and a repeat-purchase KPI used to judge a retention programme would be understated by about a tenth. The window is only 28 days, so the absolute rates are small. The direction and the mechanism are what carry over: splitting one person into two identities turns a repeat purchase into two first purchases.

## What this adds to the earlier modules

Module 1's CAC divides spend by new customers; if new customers are devices, CAC is understated. Module 7's cohorts and BG/NBD model treat each identifier as a customer; split identities understate frequency and overstate dropout. Module 4's reconciliation table has a row for unattributed orders; this lesson explains where they come from. Every number from Modules 1 to 8 inherits whatever this layer gets wrong.

## Check your understanding

1. Show, using the table, that cleaning the data increased the gap to the ledger. In one paragraph, explain why that is not an argument against cleaning.
2. A colleague proposes adding the invisible 24% back by dividing analytics revenue by 0.76. What assumption is hidden in that, and when would it fail?
3. How would you find out what share of the business's customers you cannot see, using only data you could obtain in a real company?
