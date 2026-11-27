# Lesson 1. Cohort tables and how to read them

A cohort table groups customers by when they first bought and follows each group forward. Rows are acquisition periods, columns are time since the first purchase, and each cell says something about how that group behaved at that age. The aim is to compare like with like: a customer acquired in January and one acquired in June are at different stages of the same story, and the table lines the stages up.

Run `python3 cohorts.py` and you get thirteen rows of four-week acquisition blocks. Each cell is the share of that cohort that placed an order during the corresponding four-week period after their own first purchase. A glance suggests a gentle decline: in the first period after acquisition roughly 15% of a cohort orders, by period nine or ten it is nearer 10%.

## Three things the picture does well

It shows the shape of decay. Not a single "retention rate", but whether the drop is steep and early or slow and steady, which is what separates a product bought on impulse from one bought out of habit.

It shows whether newer cohorts are better or worse than older ones, which is the only honest way to find out whether product, targeting or onboarding changes did anything.

It exposes seasonality and promotions as diagonal stripes, because a calendar event hits every cohort at a different age.

## The part most dashboards skip: how noisy it is

Each cohort here has about 190 customers. If the true chance of ordering in a period is 12%, the standard error of an observed rate is sqrt(0.12 × 0.88 / 190), about 2.4 percentage points. That means a cell reading 16.9% against its neighbour's 11.1% is entirely compatible with no difference at all. Look at row 6, with 23.0% in its first period, and row 5, with 11.6%: a stronger story is tempting, and the arithmetic says to resist it.

The practical consequences:

- Compare patterns across many cells and cohorts, not single cells.
- Pool adjacent cohorts, or smooth along age, before drawing a curve.
- Put an interval on any difference you intend to act on. Cohorts of a few hundred will rarely distinguish a two-point change.
- Be most suspicious of the cells that tell the most exciting story.

## Choosing what a cell measures

"Share who ordered in the period" is one choice. Others, each answering a different question:

| Measure | Answers | Weakness |
|---|---|---|
| Active rate in period k | Are customers still engaged? | Ignores how much they spend |
| Cumulative orders per customer | How much have they bought so far? | Never falls, so decay is hidden |
| Cumulative gross profit per customer | Has acquisition cost been repaid? | Needs margin and CAC alongside |
| Share ever ordered again | How many convert to a second purchase? | A single yes/no, loses timing |

Module 1's payback analysis used the third. Retention work usually starts with the first.

## Blank cells are information

A cell is blank when the cohort has not yet lived long enough to be observed at that age. The table above leaves them empty, and `cohort_table` enforces the rule: a cell appears only if every customer in the cohort could have been observed for the whole period. Filling blanks with whatever data exists so far is the commonest way to make young cohorts look worse than old ones. That is Lesson 2.

## Check your understanding

1. For cohorts of 190, how large must a difference in active rate be before you would call it real at roughly 95% confidence? (Use the standard error of a difference between two proportions.)
2. A product team claims the new onboarding "lifted period-1 retention from 13% to 17%" on one cohort of 200. What would you ask?
3. Why does a seasonal promotion show as a diagonal in a cohort table rather than a vertical stripe?
