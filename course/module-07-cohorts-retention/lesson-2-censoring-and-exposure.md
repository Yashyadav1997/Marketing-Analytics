# Lesson 2. Censoring, exposure and the denominator problem

Suppose a report says "customers placed 0.96 repeat orders each in the last year." It sounds like a fact about customers. It is really a fact about the calendar.

In the shipped data, customers are acquired uniformly over the year. A customer who joined in week 2 had fifty weeks in which to reorder. One who joined in week 50 had two. Summing repeat orders and dividing by headcount treats both as if they had been watching for the same time. The average customer here has been observed for about 26 weeks, so the headline figure covers roughly half a year of behaviour while being labelled as annual.

The fix is to use *exposure*, the time each customer was actually at risk, as the denominator:

```
repeat rate = total repeat purchases ÷ total customer-weeks observed
```

With the data in this module, that gives 0.037 repeat purchases per customer-week, which is about 1.9 a year. The naive figure of 0.96 understated annual repeat behaviour by roughly half. Neither number is "wrong" arithmetic; only one answers the question people think they are asking.

## The general principle

Whenever you divide by a count of customers, ask whether all of them have been observed for the same length of time. If not, you have right-censored data: for the recent customers, the story is unfinished. The standard cures are:

- **Align by age**, as the cohort table does, and drop cells that cannot yet be observed.
- **Use exposure** in the denominator of rates.
- **Use methods that model the unfinished story**, such as survival analysis or the BG/NBD model in the next lesson, which use each customer's observation length as an input rather than ignoring it.

## A relative of the same trap: survivorship

If you compute average spend only over customers who have placed three or more orders, you will find a flattering number, because you have filtered to people who stayed. It answers "how much do loyal customers spend?" and is often presented as "how much does a customer spend?". The cohort and exposure approach avoids it by keeping every acquired customer in the denominator whatever they went on to do.

## Where it hurts in practice

A retention dashboard that refreshes daily will show the most recent cohort's retention rising every day as its cells fill in, then flattening. People celebrate. A subscription renewal rate computed on all customers who *could have* renewed this month is a different animal from one computed on all active subscribers. A marketing mix model fitted on a year of data with a late-launched channel is quietly comparing a full year of one channel to a few weeks of another.

## Check your understanding

1. Using `cohorts.exposure_adjusted_rate`, recompute with the calibration cutoff at week 40 instead of 52. Should the rate change? Does it, and why or why not?
2. A company reports "average customer lifetime: 14 months" computed from customers who have already churned. Which direction is the bias and what would you do about it?
3. Why does the BG/NBD model need T (the length of each customer's observation window) as an input, and not only the number of purchases?
