# Lesson 1. RFM and where it misleads

Recency, frequency and monetary value is the oldest customer segmentation in direct marketing, and it has lasted because it is cheap, interpretable and tolerably predictive. Each customer gets three numbers: how long since their last purchase, how many purchases, how much per order or in total. Score each from one to five by quintile, combine, and you have a ranking and a vocabulary ("champions", "at risk") that a whole organisation can use.

`rfm.build_customers` constructs the features from the Module 7 log. A few details deserve attention because they are where errors enter.

**Recency is measured from the cutoff**, not from today. Features must be computed as of the calibration end, or the holdout is contaminated.

**Frequency counts repeat purchases here** (x), consistent with the BG/NBD input. Counting the first purchase as well shifts everyone by one and changes nothing in a rank-based score, but it matters if you ever compute rates.

**Monetary value is average order value**, not total spend. Total spend is largely frequency again, and would make the monetary score a noisy duplicate of the frequency score.

## The tie problem

In this dataset 55% of customers have made no repeat purchase. Their frequency is identical, so any quintile scheme must give them all the same score or split them arbitrarily. `quintile_scores` assigns tied values their average rank, so they share a score. Many commercial implementations instead sort and cut into equal-sized groups, which scatters identical customers across different quintiles by accident of row order. Two customers with exactly the same behaviour can end up in different "segments", and the segment sizes look tidy while meaning nothing.

## What a composite hides

Adding R, F and M scores (a range of 3 to 15) treats a customer with scores 5-1-5 the same as 1-5-5. Those are not the same customer: one is new and high-spending, the other a faded loyalist. The usual response, a three-digit RFM code with 125 cells, solves the problem by creating hundreds of near-empty segments that nobody can act on.

Equal weights are also a choice, and an arbitrary one. In the validation in Lesson 2, monetary value on its own is barely better than chance at identifying future revenue, so giving it a third of the weight dilutes a composite that would do better with less of it.

## Rule-based segments and the tenure trap

A very common alternative is a handful of named rules. The code builds a simple one: one-time buyers; active repeat buyers (last order within 13 weeks); cooling (13 to 26 weeks); lapsed (beyond 26 weeks).

Check how each segment actually performed in the holdout:

| Segment | Share of customers | Mean holdout revenue |
|---|---|---|
| active repeat | 26.5% | 1,623 |
| cooling | 11.1% | 732 |
| lapsed | 7.4% | 364 |
| one-time | 55.0% | 548 |

The ordering is sensible except for one row. "One-time" customers outperform "lapsed" ones. That is not a quirk; it is a design flaw. The one-time segment mixes customers acquired three weeks ago, who are still in their first window and very likely to return, with customers who bought once a year ago and never came back. Both are labelled by the same count, because the rule ignores tenure. The segment average is a blend of two quite different populations.

The remedy is to condition on how long the customer has been observable (the variable T). "One-time, acquired within the last 8 weeks" and "one-time, acquired over 6 months ago" are different segments with different treatments, and the second is closer to lost than the first. Exercise 4 asks you to redesign the rules and test whether it helped.

## What RFM is good for

For a team with no modelling capacity it is a defensible, explainable baseline, and, as Lesson 2 will show, a clearly better one than any single dimension. The point of the exercise is not to dismiss it. It is to keep it honest: know where it ties, where it blends and what it fails to use.

## Check your understanding

1. Why would a monetary score built from *total* spend be a poor third dimension?
2. Construct two customers with identical R, F and M quintile scores but very different futures.
3. A colleague adds a fourth dimension, "channel acquired through". Is that still RFM? What new problems does it create?
