# Lesson 3. Holdouts, selection and geo-lift

## Why not just compare exposed with unexposed?

The cheapest comparison in advertising is between customers who saw the ads and those who did not. It is also the most misleading, because people are not exposed at random. They are targeted, they search, they click, they sit on the email list. Whatever made them reachable usually also made them likelier to buy.

`holdout.py` shows it against the ground truth of the simulated world. For each channel, it takes the naive exposed-versus-unexposed difference, and also runs a randomised holdout in which 20% of 200,000 users are randomly denied the channel.

| Channel | TRUE incremental orders | Randomised holdout estimate (95% interval) | Naive exposed vs unexposed |
|---|---|---|---|
| Paid social | 1,674 | 1,428 (976 to 1,881) | 1,324 |
| Email | 595 | 480 (14 to 946) | 4,424 |
| Brand search | 228 | 91 (−380 to 563) | 5,712 |
| Influencer | 364 | 198 (−271 to 668) | 343 |

Two findings pull in different directions.

**The naive comparison fails exactly where selection is strong.** Email reaches mostly high-intent customers, and brand search mostly high-intent searchers; the naive estimate overstates them by roughly 7 and 25 times. Where exposure is close to random with respect to intent (paid social and influencer in this world), the naive estimate happens to land near the truth. That is not a reason to trust it: an analyst has no way to know in advance which situation they are in.

**The randomised holdout is unbiased, and its intervals contain the truth in every row, but it is far from precise.** The brand-search interval runs from a loss of 380 orders to a gain of 563; the influencer interval is similar. Even with 200,000 users and a 20% holdout, the experiment cannot separate a worthwhile channel from a worthless one for channels with small true effects. It does clearly establish that paid social does something (the interval stays above zero) and, much more weakly, that email does.

This is the lesson of Lesson 1 made concrete. Channels with low incrementality, which are the ones most likely to be wasting money, are exactly the ones hardest to measure. The remedy is more data, a longer window, a larger holdout fraction for such channels, or a design with less noise, not a more confident reading of what you have.

Convert the estimates to returns and the same picture appears: the holdout puts paid social at 1.33 against a true 1.56, email at 7.55 against 9.36, brand search at 0.23 against 0.58, influencer at 0.14 against 0.25. The estimates fall short of the truth in every row, but the sampling noise in a single experiment is bigger than that gap, and no conclusion should rest on the shortfall.

## Intention to treat

Notice what is being compared: everyone assigned to the test arm against everyone assigned to holdout, regardless of whether the channel actually reached them. This is the intention-to-treat comparison. It is the one that preserves randomisation, and it estimates what turning the channel on does to the whole population. Restricting to people who were actually exposed breaks the protection, since exposure within the test arm is again self-selected.

## When user-level holdouts are impossible

Many channels cannot be withheld from individuals: television, outdoor, some sponsorships, and platforms that do not support holdouts. The next best design randomises *places* instead of people.

`geolift.py` builds twenty synthetic regions over 70 days. A campaign runs in five of them for the last 21 days. All regions share a weekly pattern, a gentle trend, and a 12% festive surge that begins on the same day as the campaign.

That surge is the trap. Comparing the treated regions before and after the campaign gives a "lift" of 16.7% to 22.6%, depending on the true effect. Most of it is the festival, which hit every region. A **difference-in-differences** estimator subtracts the change seen in the untreated regions from the change in the treated ones, removing everything common to both:

| True lift | Naive before/after | Difference-in-differences |
|---|---|---|
| 5% | 22.6% | 6.6% |
| 2% | 19.1% | 3.6% |
| 0% | 16.7% | 1.6% |

The difference-in-differences figures are far better but still off by about a point and a half. That is one dataset's noise (all three rows share the same random draw). Replicate over 300 fresh draws and the estimator behaves:

| True lift | Mean estimate | Spread (sd) | Flagged significant at p<0.05 |
|---|---|---|---|
| 5% | 5.04% | 0.88% | 100% |
| 2% | 2.04% | 0.86% | 68% |
| 1% | 1.04% | 0.85% | 22% |
| 0% | 0.04% | 0.84% | 7% |

Unbiased, with a standard deviation near 0.85 percentage points. A 5% lift is always caught, a 2% lift about two times in three, a 1% lift rarely. In other words, with five treated regions and three weeks, this design cannot reliably see effects below about 2%. Running a geo test on an effect you expect to be 1% is a decision to find nothing.

## Inference by permutation

How do you know whether a difference-in-differences estimate is bigger than chance? The code uses a permutation test: re-label every possible group of five regions out of twenty (15,504 groupings, including the real one), compute the same estimate for each, and ask how often a random grouping produces an effect at least as large. If the campaign did nothing, the real grouping is just one more draw from that distribution.

One implementation note, because I got it wrong at first. An earlier version of this script permuted only the *control* regions, leaving the real treated regions out of the set. That is not a valid permutation test; it produces a distribution that fails to include the very randomness it is meant to calibrate, and it appeared to flag too many false alarms (9 to 10% at zero effect in a short run). With the real grouping included, the false-positive rate was 4.6% over 800 replications, consistent with 5%. The small-run figures shown in the table (7% over 300 runs) have sampling error of a couple of points either way. When you see a surprising error rate, run more replications before deciding whether the method or the sample is at fault.

## What geo tests assume

- **Parallel trends.** Without the campaign, treated and control regions would have moved together. Check that they did in the pre-period.
- **No spillover.** People in control regions are not influenced by the campaign. Borders, online media and travel violate this.
- **Comparability.** Choose treated regions by similarity (or randomly), not because they are the ones the sales team wants to try first.
- **Few units, so noise matters.** With 20 regions, one unusual region can dominate. Placebo tests and sensitivity checks are not optional.

## Reporting a result

State the estimate, the interval, the sample, and the decision it supports. "Lift of 3.6%, permutation p-value 0.01, five of twenty regions over three weeks; we cannot rule out effects between about 1.5% and 6%" is a result. "The campaign worked" is not.

## Check your understanding

1. Why does the naive before/after estimate fail in the geo simulation? Name two things besides the festive surge that would produce the same failure in a real business.
2. The brand-search holdout interval spans from a loss to a large gain. What are three ways to narrow it, and what does each cost?
3. A channel's true incremental return is 0.6 but the experiment cannot distinguish that from 1.5. Should the channel be cut? Argue both sides, then state what additional information would settle it.
