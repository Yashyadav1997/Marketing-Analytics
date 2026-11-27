# Exercises

## Exercise 1. Read a cohort table with appropriate suspicion (45 min)

Run `cohorts.py`.

a. For each cohort compute the 95% interval on its period-1 active rate. How many cohorts have intervals that exclude the overall average of period 1?
b. Pool cohorts 0 to 3 and cohorts 9 to 12. Is there a detectable difference in period-1 rate? Report the difference and its interval.
c. Write two sentences a product lead could act on, and one sentence on what the table cannot support.

## Exercise 2. Exposure (30 min)

a. Reproduce 0.956 (naive) and 0.037 per week (exposure-adjusted) from `transactions.csv` without calling the helper functions.
b. Recompute with the cutoff at weeks 26, 40 and 52. The rate is not constant. Explain why, given that exposure already corrects for different observation lengths.
c. Construct a small example (five customers will do) where the naive figure and the exposure figure disagree by a factor of three.

## Exercise 3. Fit and forecast (60 min)

a. Build (x, t_x, T) for each customer from `transactions.csv` using only transactions up to week 52.
b. Fit with `bgnbd.fit`. Compare the four estimates with `customers_truth.csv`. For r and α, compare the fitted *population mean* r/α with the average true λ; for a and b, compare a/(a+b) with the average true p.
c. Using only the fit, forecast total repeat orders for weeks 52 to 78 and compare with the holdout.
d. Group customers into deciles of P(alive). In each decile, what share is actually alive according to the truth file, and what share placed a holdout order? Plot or tabulate. Where is the model least reliable?

## Exercise 4. Break it (60 min)

Run `misspecification.py` and read the output.

a. Explain, in your own words, why a promotion in the holdout causes under-forecasting, while a promotion in the calibration window produces over-forecasting in this experiment.
b. Propose two practical remedies. For each, state what data it needs and what could go wrong with it.
c. A colleague says: "The model was 99% right on the clean data, so it must be fine." Reply in three sentences.

## Exercise 5. Win-back targeting memo (60 min, 400 words)

A retention manager can fund a win-back offer for 300 customers. Using P(alive) and expected future purchases, say which 300, and why not the 300 with the *lowest* P(alive) and not the 300 with the highest. State what you would need to learn from a small randomised test before rolling out beyond that first 300, and how you would size that test.

---

## Answers and hints

**Lesson 1.** (1) Standard error of a difference ≈ sqrt(2) × 2.4 = 3.4 points, so about 6.7 points is needed at 95% confidence. (2) Which cohort? Compared with what baseline, over what period, and how many cohorts did they look at before this one? One cohort of 200 cannot distinguish 13% from 17%. (3) Because a calendar date is a different age for every cohort.

**Lesson 2.** (1) The rate rises slightly as the cutoff moves earlier (about 0.0402 at week 26, 0.0386 at 40, 0.0371 at 52), because exposure corrects for observation length but not for attrition: the longer customers are observed, the more of them have dropped out, and the average rate per customer-week falls. (2) Biased downward: it counts only customers who have already left, excluding the still-active long-lived ones. Use survival methods that treat active customers as censored, not absent. (3) Because the same purchase count means something different after 10 weeks than after 50; the model needs to know how long it has been watching to judge how surprising silence is.

**Lesson 3.** (1) Fitted model: P(alive) is about 0.10 for x = 6, versus about 0.46 for x = 2, both with t_x = 20 and T = 52. A frequent buyer's 32 weeks of silence is far more surprising. (2) Options: add a separate dropout parameter for the first gap, treat one-time buyers as their own segment with an independent model, or add a time-to-second-purchase model (a hazard on the first interval). (3) Useful for budgeting, capacity and valuing the base. Poor for individual-level decisions, where per-customer error matters.

**Exercise 4.** Reference numbers from the shipped seed: with no promotion the forecast error is −1.2%. A 4-week promotion at 2× in the holdout gives −10.5%; at 3×, −15.0%. A 3× promotion in the calibration window instead gives +5.3%, since the model absorbs the spike into higher purchase rates and carries it forward. Remedies include fitting on promotion-free windows, adding promotion covariates, or modelling baseline separately and layering an uplift estimate on top.
