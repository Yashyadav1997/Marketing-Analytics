# Lesson 3. LTV, cohorts and the formula trap

Lifetime value is the number people most want and the one they most often fabricate. The usual formula is neat:

```
LTV = AOV × margin × orders per year × lifespan in years
LTV:CAC = LTV ÷ loaded CAC
```

With an AOV of 1,200, a 58% margin, three orders a year and a two-year lifespan, LTV is Rs 4,176. Against a loaded CAC of 850 that is a ratio of 4.9, which reads as "very strong, scale with confidence" on the benchmark ladder that circulates in practitioner writing (below 2:1 is thin, 3:1 to 5:1 is healthy, above that either exceptional or under-invested).

Now change two inputs, both plausible. Suppose the customer buys twice a year and stays one year. LTV is 1,392 and the ratio is 1.6. The business went from "scale aggressively" to "barely clear of the line" without any change in what it actually knows. All that moved were two assumptions that nobody had measured.

## Why the formula is fragile

It multiplies four averages. Each average hides a distribution, and the product of averages is not the average of the product. Frequency and lifespan are especially treacherous because they are correlated: customers who buy often tend to stay, so the heavy buyers dominate the mean while the typical customer buys once and leaves. In many consumer categories the median customer's LTV is close to their first-order gross profit, and a minority of loyal buyers carry the rest.

The other source of trouble is timing. A rupee of gross profit in month 18 is not worth a rupee in month 1, to a lender or to a founder worrying about runway. The simple formula applies no discount and no uncertainty.

## A better working method

**Observe cohorts.** Group customers by month of first purchase. For each cohort track cumulative gross profit per customer by months since acquisition. Plot the curves. You are reading three things at once: the first-order contribution (the intercept), the rate of repeat purchase (the slope) and whether it flattens (the asymptote). A projected LTV is then an extension of an observed curve, which you can defend, rather than a product of four guesses.

**Cut by acquisition source.** Blended cohorts conceal the thing that matters. In the shipped data, brand-search customers repay their acquisition cost on the first order and keep buying; paid-social customers cost roughly twice as much and repurchase more slowly. A blended LTV:CAC would average two different businesses into a figure that describes neither.

**Be honest about the unobserved tail.** A cohort observed for twelve months says nothing certain about month twenty-four. Extrapolate explicitly, with a stated decay assumption, and show a range. For a stronger treatment, the probabilistic customer-base models (beta-geometric / negative binomial family) estimate the chance a customer is still "alive" from their recency and frequency, and are the standard next step; Module 7 takes them up.

**Report a range, not a point.** "LTV:CAC between 1.8 and 3.2 depending on whether second-year repeat rates hold" is more useful to a decision-maker than "2.6".

## What the ratio is for

The ratio is a screening device. Under about 1.5 you should look hard at whether the acquisition model works at all. Above about 3 you should ask whether you are under-investing, since a brand with exceptional ratios and flat growth may simply be leaving customers on the table. Between them, the ratio mostly tells you to check payback and cash. It was never meant to carry a budget decision by itself, and a benchmark ladder invented for one set of brands should not be allowed to settle the question for another.

## Check your understanding

1. Using `unit_economics.ltv_simple`, find the frequency at which LTV:CAC falls below 3 for the worked example. Is your answer more sensitive to frequency or to lifespan?
2. Why is the *median* customer's value often more informative than the mean for deciding how much to pay for a first order?
3. A cohort has been observed for nine months and shows repeat rates falling by about 20% a month. Sketch the extrapolated twelve-month cumulative profit and say what you would want to know before trusting it.
