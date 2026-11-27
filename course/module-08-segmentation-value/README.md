# Module 8. Segmentation and customer value

## Why this follows Module 7

Module 7 produced, for each customer, a probability of still being active and an expected number of future orders. Module 8 asks what to do with that: how to group customers, how to value them, and, more awkwardly, how to find out whether a segmentation is any good. Most segmentation work stops at the picture (a coloured grid, a set of names) and never checks whether the groups predict anything. Here every method is scored against a holdout period it could not see.

## Outcomes

1. Compute recency, frequency and monetary features correctly, including for customers whose history is short.
2. Build RFM and rule-based segments, and say what each one hides.
3. Validate any score against a holdout using more than one metric, and explain why the metrics can disagree.
4. Quantify how concentrated customer value is, and what that does to averages.
5. Produce a probabilistic customer value estimate and state what it leaves out.

## Contents

| Part | File | Time |
|---|---|---|
| Lesson 1 | [RFM and where it misleads](lesson-1-rfm-and-where-it-misleads.md) | 45 min |
| Lesson 2 | [Validating a segmentation](lesson-2-validating-a-segmentation.md) | 75 min |
| Lesson 3 | [Concentration and probabilistic value](lesson-3-concentration-and-probabilistic-value.md) | 60 min |
| Exercises | [exercises.md](exercises.md) | 3 to 4 hours |
| Code | [code/](code/) | reference |

## Running it

Needs Module 7's code and data (it reuses them).

```bash
cd course/module-08-segmentation-value/code
python3 -m unittest -v      # 13 tests
python3 validate.py         # the table every lesson refers to
python3 robustness.py       # 10 simulated datasets, about 10 seconds
```

## What the data can and cannot teach

It is the simulated purchase log from Module 7, with an unusual advantage: `customers_truth.csv` lets the code build an *oracle* score from the true purchase rate and who is truly still active. No real method can reach it, which is exactly why it is useful. It shows how much of the variation in future revenue is predictable at all, and how much is chance.

Because customer spend in the simulation is independent of purchase frequency by construction, this module cannot show what happens when the two are correlated, which they often are in real retail. Exercise 5 asks you to think through that gap.
