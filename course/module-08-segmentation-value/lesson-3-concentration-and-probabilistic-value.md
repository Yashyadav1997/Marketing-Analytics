# Lesson 3. Concentration and probabilistic value

## Averages mislead where value is concentrated

In the holdout, mean revenue per customer is 840. The median is zero. More than three fifths of customers placed no order in the 26 weeks, so the "typical" customer contributed nothing, while the top 10% of customers delivered 56% of revenue and the top 20% delivered 79%.

This has three consequences for the work in earlier modules.

- **Module 1's LTV formula multiplies averages**, and an average over a population like this describes almost nobody. Using the mean to decide how much to pay for a customer is a bet that you will acquire your share of the heavy buyers, and it is a bet on a tail.
- **Cohort comparisons are fragile.** A cohort that happened to land two extra heavy buyers looks like an improvement in "quality". With revenue this skewed, comparing cohort means requires either large cohorts or robust summaries.
- **Concentration changes what retention is worth.** Retaining the median customer is nearly worthless; retaining one of the top decile is worth many times the average. A retention programme that treats everyone equally spends most of its money where the value is not.

One caution on reading the figures. They come from a 26-week window and a simulation tuned to give heterogeneous buyers. Real concentration varies by category: grocery is flatter, luxury steeper. The method of measuring it, share of revenue held by the top decile and by the top fifth, travels well; the numbers do not.

## A customer-level value estimate

Module 1's formula can be replaced by something that works customer by customer:

```
expected value over horizon = expected repeat orders (BG/NBD) × expected order value
```

`probabilistic_value` computes both pieces. The first comes straight from Module 7. The second needs a small piece of care: a customer with one order has an observed average order value that is a single, noisy number. Using it raw would rank customers by luck in their first basket. Instead, the code *shrinks* each customer's observed average toward the population average, with the weight on their own history growing as they accumulate orders:

```
shrunk spend = (n × own mean + k × population mean) / (n + k)
```

The constant k is estimated from the data as the ratio of within-customer to between-customer variance in log order value. Here it comes out at 0.44 (the true ratio in the simulation is about 0.51), meaning a single order already carries a little over twice the weight of the population prior (1 against 0.44) and a handful of orders dominate it. This is the intuition of the Gamma-Gamma model that practitioners pair with BG/NBD; the version here has fewer moving parts and the same idea.

## How well does it do?

The summed forecast of holdout revenue is 2.06 million against an actual 2.10 million, a miss of 1.7%. At the individual level it ranks customers better than the alternatives (Lesson 2), though far from the oracle. It is a decent estimate of the aggregate and a modest improvement at identifying individuals, and one should hold the two claims apart.

## What the number leaves out

A figure called customer value invites over-reading. As implemented it is *expected revenue*, and several things separate it from what a business would call value:

- **Margin.** Revenue is not profit. Multiply by product-level margin, and by the customer's own mix, since they may favour low-margin lines.
- **Cost to serve.** Returns, discounts used, support contacts, shipping subsidies. These differ by customer and can reverse the sign of the apparent value.
- **Time and risk.** A rupee in six months counts for less than a rupee today. A discount rate is easy to add and rarely is.
- **Dependence between frequency and spend.** The simulation makes them independent. If real heavy buyers also buy larger baskets, the multiplication understates their value; if discount-driven heavy buyers buy small baskets, it overstates it. Test it before assuming.
- **Causality.** High expected value says nothing about whether intervention will change behaviour. The customer most likely to buy anyway is the worst place to spend a win-back budget. The question "who is persuadable?" belongs to experimentation and uplift modelling, which this course addresses in Module 5 and on the backlog as a later topic.

## Putting it to use

A reasonable workflow: score all customers; summarise by decile; look at concentration; choose a decision (who gets the retention budget, who gets the high-touch service, who should not be chased); run a small randomised test of that decision; and only then scale. The score tells you where value *is*. The test tells you where spending *changes* it, and that difference is what retention budgets are really about.

## Check your understanding

1. In this dataset the median holdout revenue is zero. What summary would you report to a board, and why?
2. Why shrink order value toward the population mean rather than using each customer's own average?
3. List two ways the value score as built could rank customers wrongly even if its aggregate forecast is spot on.
