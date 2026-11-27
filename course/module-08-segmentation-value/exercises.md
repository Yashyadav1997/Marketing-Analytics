# Exercises

## Exercise 1. Features without leakage (40 min)

a. Rebuild recency, frequency, average order value and tenure for every customer from `transactions.csv`, **without** importing `rfm.py`, using only transactions up to week 52.
b. Verify your numbers against `rfm.build_customers` for ten customers chosen at random.
c. Deliberately introduce a leak (for example, compute recency from week 78) and rerun the validation in `validate.py` logic against the holdout. How much does the apparent performance improve, and why is that improvement worthless?

## Exercise 2. Two metrics, two verdicts (45 min)

Using `validate.py` output:

a. Explain, in a paragraph, why recency-only scores a rank correlation of 0.297 but a top-10% capture of only 19.7%.
b. Construct, with a small hand-built example (ten customers is plenty), a score with high rank correlation and poor top-decile capture, and one with the reverse.
c. For each of these decisions, name the metric you would use and why: (i) choosing 250 customers for a costly concierge service; (ii) ordering the full list for an email campaign sent in waves; (iii) deciding how much total budget the retention team needs.

## Exercise 3. How sure are you? (45 min)

Run `robustness.py`.

a. The BG/NBD advantage over the RFM composite is about 4.7 points on average, with a standard deviation of about 2 on each method. Estimate, roughly, how often a single dataset of this size would show an advantage of less than 1 point or even a reversal. Compare with the actual outcome across the ten seeds (BG/NBD wins every time) and explain any tension.
b. Change the number of customers to 800 in `simulate()` and rerun the comparison. What happens to the spread, and to your confidence in the ranking?
c. Why is "the model wins on average" a weaker statement than "the model wins on my data"?

## Exercise 4. Fix the tenure trap (60 min)

Lesson 1 showed that "one-time" customers out-earn "lapsed" ones because the group blends new and stale buyers.

a. Redefine the segments so that tenure (T) is part of the rule. Propose at least five segments.
b. Compute mean holdout revenue and a 95% interval for each. Do the segments now order sensibly?
c. Count how many segments are distinguishable from their neighbours, and decide which to merge.
d. State one downside of adding segments, even if each is valid.

## Exercise 5. Value is not the same as worth acting on (60 min, 500 words)

You must spend a retention budget on 250 customers. You have three candidate lists: the top 250 by expected value, the top 250 by probability alive among those with at least three orders, and 250 chosen at random from customers with moderate value.

Write a memo recommending how to allocate the money, including a small randomised test. Say specifically:

- why the highest-value customers might be the wrong people to treat (think about what they would have done anyway);
- what you would measure, over what window, and what result would make you stop;
- one thing about this simulation (for example, spend being independent of frequency) that could make your recommendation wrong on real data.

---

## Hints and reference points

**Exercise 1c.** A leak of this kind inflates apparent accuracy because the score then contains the answer. The tell is a result better than the oracle, which cannot be exceeded legitimately.

**Exercise 2a.** Recency separates active from long-gone customers, which determines most of the rank order in a population dominated by non-buyers. It cannot separate a heavy buyer from an occasional one among the active, which is what the top decile needs.

**Exercise 3a.** Treating the two top-10% shares as independent, each with a spread of about 2 points, gives a spread of the difference near 3 points, so a 4.7-point mean advantage would sometimes fall below 1 point. Measured across seeds, though, the spread of the *paired* difference is only about 0.5 to 0.7 points, because both scores are computed on the same customers and share their luck. That is why the model wins in every comparison across 22 seeds. It also makes the shipped dataset, with a gap of about one point, a genuine outlier of several paired standard deviations, which the lesson leaves unexplained. A good answer says that plainly, and notes that a customer-level bootstrap of the shipped sample gives an interval (about -1.2 to +3.5) that includes both zero and the typical gap.

**Exercise 4.** One workable scheme splits one-time buyers by tenure (under 8 weeks, 8 to 26, over 26) and repeat buyers by recency (as in the shipped rule). Expect the new one-time-and-recent group to rank high and the old one-time group to rank near the bottom. Whether the intermediate groups separate at this sample size is the question.

**Exercise 5.** The strongest answers separate "expected value" from "expected change in value". The first is a prediction about customers; the second is a causal quantity that only a test measures.
