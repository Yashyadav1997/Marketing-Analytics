# Module 7. Cohorts, retention and repeat purchase

## The question this module answers

Module 1 ended with an uncomfortable admission: the payback and LTV formulas rest on an assumed shape of repeat behaviour, and that shape can be observed. Here we observe it, and then ask a harder question than "what happened?", namely "which customers are still with us, and what will they do next?" The second question cannot be answered by looking at the data alone, because a customer who has not bought for ten weeks may be gone or merely between purchases. The data cannot say which. A model has to.

## Outcomes

1. Build a cohort table that does not mislead, and say how much of its variation is noise.
2. Explain right-censoring and use exposure, not headcount, as the denominator for rates.
3. Fit the BG/NBD model, interpret its four parameters, and read a customer-level probability of being alive.
4. Test a forecast against a genuine holdout, and recognise when the model's assumptions have broken.

## Contents

| Part | File | Time |
|---|---|---|
| Lesson 1 | [Cohort tables and how to read them](lesson-1-cohort-tables.md) | 45 min |
| Lesson 2 | [Censoring, exposure and the denominator problem](lesson-2-censoring-and-exposure.md) | 45 min |
| Lesson 3 | [Buy till you die](lesson-3-buy-till-you-die.md) | 90 min |
| Exercises | [exercises.md](exercises.md) | 3 to 4 hours |
| Code | [code/](code/) | reference |

## Running it

```bash
cd course/module-07-cohorts-retention/code
python3 -m unittest -v      # 7 tests, about one second
python3 simulate.py         # regenerates ../data/ (seeded, so identical each time)
python3 cohorts.py          # cohort table and exposure-adjusted rate
```

## About the data

`data/transactions.csv` is a simulated purchase log of 2,500 customers, acquired across 52 weeks and observed for 78, with a 26-week holdout. `data/customers_truth.csv` records each customer's true purchase rate, dropout probability and dropout week, which real data never gives you. Use the truth file only to *check* your work, never to build it.

The data was generated from the very model Lesson 3 fits, so recovery is flattering by construction. The point of the simulation is to show that the machinery works when its assumptions hold; Exercise 4 then breaks the assumptions to show what failure looks like.

**Anchor reading** (read before relying on this module): Fader, Hardie and Lee, "Counting Your Customers the Easy Way: An Alternative to the Pareto/NBD Model" (*Marketing Science*, 2005), the source of the model and of the formulas implemented here.
