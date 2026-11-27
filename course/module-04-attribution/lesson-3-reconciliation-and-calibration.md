# Lesson 3. Reconciliation and calibration

If credit rules cannot recover causation, and experiments (Module 5) are costly and slow, what should a team actually do on a Tuesday? The answer used by careful practitioners has three parts, none glamorous.

## 1. Reconcile, in writing

One table, refreshed monthly, with the same rows each time:

| Layer | What it is | Why it differs from the one above |
|---|---|---|
| Ledger revenue | What finance booked | The anchor; everything else is compared to it |
| Analytics-tool revenue | Tracked sessions that converted | Loses untracked users, devices, consent refusals |
| Platform-claimed revenue | Sum of each platform's own reports | Overlap, view-through, loose windows |
| Rule-based attribution | One agreed convention | Convention, not causation |
| Experiment-based incrementality | Measured lift from holdouts and geo tests | Limited to what has been tested, noisy |

The value of the table is the discipline of naming, for each gap, its cause. It also gives a finance partner something to check.

## 2. Use experiments to correct the credit

Suppose experiments (as in Module 5) have estimated that, for a channel, true incremental orders are some fraction of what your agreed attribution rule credits. That fraction is a *calibration factor*. In the simulated world, with last-click as the working rule:

| Channel | Calibration factor (true incremental ÷ last-click credit) |
|---|---|
| Influencer | about 1.1 |
| Paid social | about 0.9 |
| Generic search | about 0.4 |
| Email | about 0.25 |
| Brand search | about 0.05 |

Multiply a channel's attributed orders by its factor and the corrected figure tracks the truth. Brand search's 1,747 attributed orders become about 76 once multiplied by roughly 0.04 to 0.05. This is how many mature teams run: a standing, cheap attribution rule for day-to-day reporting, corrected by factors refreshed from periodic experiments.

Now the caveats, because this method is easy to misuse.

**Factors are only as stable as the world.** Across eight freshly generated worlds the factors above varied very little (brand search stayed near 0.05, email near 0.25). That stability is *a property of the simulation*, which never changes its targeting, creative or seasonality. Real factors drift when targeting shifts, when a promotion pulls forward high-intent buyers, when a competitor moves. A factor is a dated measurement, not a constant, and it should carry an expiry.

**Average is not marginal.** An experiment on current spend tells you the average return of the dollars already spent. The budget decision is about the *next* dollar, and returns diminish. A channel with a healthy average can have a poor margin. Calibration answers "is the channel worth having?" far better than "should I add 20% to it?"

**Experiments are noisy.** A single holdout gives an interval, sometimes a wide one (Module 5 shows brand search's running from a loss to a large gain). A calibration factor built on that interval inherits it, and should be reported with it.

**Interactions.** A factor measured with all other channels running does not tell you what happens when you remove another. Channels support each other; the factors are not independent.

## 3. Triangulate where experiments are impossible

You cannot holdout everything. Triangulation uses several imperfect instruments that fail in different ways:

- **Post-purchase surveys** ("how did you first hear about us?") capture awareness channels the click trail misses, and are biased by memory and by which answer is easiest to pick.
- **Branded search and direct traffic trends** often move with upper-funnel spend and can hint at what attribution misses.
- **Media mix modelling** (Module 6) estimates channel effects from aggregate spend and sales variation, needs no user-level tracking, and can be wrong in other ways.

When these disagree with the attribution rule, the disagreement is the finding. A rule that says social is mediocre while surveys, branded search and the MMM all point the other way is telling you which instrument to distrust.

## What a good report sounds like

Not "paid social returned 4.6x." Something closer to: "Platform claims 4.6x; our agreed rule credits 1.7x; the last holdout, six months ago, suggested 1.3 to 1.9x with an interval wide enough to include 1. We treat social as roughly break-even on revenue, which is below our margin-based threshold, and we have a geo test scheduled to narrow the range before we cut or expand."

That is longer than a number. It is also the only version of the sentence that will survive a challenge from the finance director.

## Check your understanding

1. A calibration factor for brand search was 0.05 in January. In March the brand ran a major television campaign. Would you reuse the factor? What would you do?
2. Why is a channel's calibration factor not a substitute for a marginal return estimate?
3. Draft the reconciliation table for a business you know. Which row would you be least able to fill in, and what would you do about it?
