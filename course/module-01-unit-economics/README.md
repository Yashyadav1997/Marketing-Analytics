# Module 1. Unit economics and the marketing financial model

## Why this comes first

A platform will report ROAS, CPM and cost per click without being asked. It will not report whether the business made money. This module builds the short chain of quantities that connects a campaign to the profit and loss account, and then spends most of its time on the places where that chain gives a flattering answer.

## Learning outcomes

By the end you should be able to:

1. Derive break-even ROAS from margin and explain why a target ROAS set without margin is arbitrary.
2. Build a loaded CAC from the cost lines that platforms leave out, and say which denominator you used and why.
3. Compute payback two ways, by formula and from cohort data, and explain the gap.
4. Show how the LTV:CAC verdict changes under different lifetime assumptions.
5. Size a fee or budget request against a client's incremental contribution margin.
6. Write a 500-word decision memo that separates what the numbers support from what they only suggest.

## Contents

| Part | File | Time |
|---|---|---|
| Lesson 1 | [Why ROAS lies](lesson-1-why-roas-lies.md) | 40 min |
| Lesson 2 | [Loaded CAC and payback](lesson-2-loaded-cac-and-payback.md) | 60 min |
| Lesson 3 | [LTV, cohorts and the formula trap](lesson-3-ltv-cohorts-and-the-formula-trap.md) | 75 min |
| Lesson 4 | [Pricing from the client's P&L](lesson-4-pricing-from-the-clients-pl.md) | 30 min |
| Exercises | [exercises.md](exercises.md) | 3 to 4 hours |
| Case study | [case-study-beauty-d2c.md](case-study-beauty-d2c.md) | 60 min |
| Code | [code/](code/) | reference |

## Running the code

Python 3.10 or later, standard library only.

```bash
cd course/module-01-unit-economics/code
python3 -m unittest -v              # 10 tests on the formulas
python3 generate_cohorts.py         # writes ../data/cohorts.csv (synthetic, seeded)
python3 cohort_payback.py           # reference output for Exercise 2
```

## A note on the data

`data/cohorts.csv` is synthetic. It was designed so that two channels have different cost and different loyalty, because that is the structure that makes blended averages mislead. The numbers are not benchmarks and should not be quoted as such.

## A note on the benchmarks

You will see figures in these lessons such as "payback under nine months" and "LTV:CAC of three to one". They come from practitioner writing, chiefly a consultant's published guide based on a roughly fifty-brand portfolio. Treat them as priors to be checked against your own business, not as laws. The exercises make you do the checking.
