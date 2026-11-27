# Lesson 1. Power: how much data a question costs

Before running a test, ask what size of effect you hope to see and how many people it takes to see it reliably. The two answers are tied together by a calculation that is easy to skip and expensive to skip.

## The calculation

For a two-arm test on a conversion rate, with a 5% significance level and 80% power, the users needed in *each* arm are roughly

```
n ≈ (z_alpha/2 + z_power)² × [p0(1−p0) + p1(1−p1)] / (p1 − p0)²
```

where p0 is the baseline rate and p1 the rate you hope to detect. `power.n_per_arm` implements it. Output from `power.py`:

| Baseline rate | 5% lift | 10% lift | 20% lift | 50% lift |
|---|---|---|---|---|
| 0.2% | 3,211,440 | 822,398 | 215,366 | 39,143 |
| 1% | 637,008 | 163,092 | 42,691 | 7,747 |
| 2% | 315,204 | 80,679 | 21,106 | 3,823 |
| 6% | 100,668 | 25,737 | 6,717 | 1,207 |

(The lift is relative: 10% on a 2% baseline means 2.0% to 2.2%.)

Three features deserve attention.

**Small base rates are punishing.** To spot a 10% relative lift, a 6% baseline needs about 25,700 users per arm. A 0.2% baseline needs more than 800,000. Most ad clicks and most purchases are rare events, so the arithmetic of rare events governs.

**Halving the effect roughly quadruples the sample.** The 5% column is about four times the 10% column. This is the square in the denominator. It means that the small improvements marketers typically chase are exactly the ones that are hardest to confirm.

**You can run the calculation backwards.** `mde_relative` gives the smallest lift an arm of a given size can reliably detect. At a 2% baseline:

| Users per arm | Detectable relative lift |
|---|---|
| 2,000 | 72% |
| 10,000 | 29.7% |
| 50,000 | 12.8% |
| 200,000 | 6.3% |

A test with 2,000 users per arm can see only a transformation of the business. Many ad creative "tests" are run at this scale and read as if they could detect a few percent.

## Dilution

A subtler cost arises when only part of the audience is reached. Suppose a channel touches 30% of users and lifts conversion among those reached by 20% on a 6% base. In a holdout over *all* users, the 70% who are never reached contribute no signal, and the measurable relative lift shrinks to 6% overall. The code gives the per-arm size needed: 70,226, against 6,717 if everyone were exposed, a factor of more than ten. Designing the holdout over the *reached* population where possible (for instance, ghost-ad or intent-to-treat on eligible users) removes much of this penalty, at the cost of extra care about how "reached" is defined.

## Power is a decision, not a formality

The 80% convention is a habit. It means that if a real effect of the stated size exists, you will detect it four times in five. For a decision where missing a real effect is costly, you might want 90%. For a cheap, reversible choice, 70% may do. The significance level is likewise a choice. What matters is that the trade-off is made before looking at data, in terms of the decision, and written down.

The same applies to the effect size itself. The most useful version of the question is not "what lift do we expect?" (which invites optimism) but "what is the smallest lift that would change what we do?" That number, the minimum effect worth acting on, sets the sample size. If the sample is unaffordable, the honest options are to run the test longer, accept lower power, test a bolder change, or decide that this question will be settled by judgement, not data.

## Check your understanding

1. A 1% baseline conversion test must detect a 10% relative lift. You get 3,000 visitors a day to each variant. How many days? What would you say if the answer is 54?
2. Why is a "bolder" treatment easier to test, and what is the risk in always choosing bolder ones?
3. A colleague proposes stopping the test "once we have a few hundred conversions in each arm." What is wrong with this rule as a sample-size plan?
