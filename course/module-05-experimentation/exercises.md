# Exercises

## Exercise 1. Power by hand (45 min)

a. Derive the sample-size formula from the sampling variance of a difference of two proportions. Verify `n_per_arm(0.02, 0.10)` against your own calculation.
b. A test must detect a 5% relative lift on a 3% baseline and the site receives 1,500 visitors a day split between two arms. How long must it run? What would you tell the team if the answer is more than a quarter?
c. Using `holdout_users_needed`, size a holdout for a channel reaching 25% of users with a 15% lift among those reached on a 4% base.

## Exercise 2. Peeking, measured (45 min)

a. Rerun `peeking.py` with `n_per_look` of 500 and of 10,000. How does the false-positive rate at 10 looks change, and why?
b. Add an O'Brien-Fleming-style rule: use critical values `z_k = z_final * sqrt(K / k)` at look k of K. Measure the false-positive rate and compare with Bonferroni.
c. Write the test charter you would give a marketing manager: three rules, no jargon.

## Exercise 3. Holdout design for a hard channel (75 min)

Run `holdout.py` for `search_brand` with holdout fractions 0.2, 0.5 and 0.8, and with 50,000, 200,000 and 800,000 users (change `HOLDOUT` and `N_USERS` or call `rct` directly).

a. Tabulate the width of the 95% interval in each case. Which lever buys more precision per unit of cost?
b. The true incremental return of brand search in this world is below 1. How large a holdout does it take for the interval to exclude a return of 1.0?
c. Holding out 80% of users from a channel is costly: those users lose the channel. Write down what the business gives up and when it is worth it.

## Exercise 4. Geo test planning (75 min)

a. Using `geolift.replicate`, estimate how often a 1.5% true lift is detected with 5 treated regions of 20. Then change `TREATED` to ten regions. What happens to detection, and what does the business give up?
b. Make the festive surge region-specific (for example, 20% in half the regions, 5% in the rest, with the treated regions drawn from the high-surge half). What happens to difference-in-differences? Which assumption has been violated, and how would you check for it in real data?
c. Add a pre-period check: regress treated-region log sales on control-region log sales before the campaign and measure how well it fits. How would you use this to choose control regions?

## Exercise 5. The incrementality memo (75 min, 500 words)

Your CFO has two results. A holdout on brand search estimated 91 incremental orders with a 95% interval of −380 to 563; a platform report credits it with 1,747 orders. Write the memo recommending what to do. Cover: what each number means, what the interval implies about the question, the design of a more informative follow-up with its cost, and the decision rule you would pre-commit to before seeing the data.

---

## Hints and reference points

**Exercise 1a.** Var(p̂₁ − p̂₀) = p₀(1−p₀)/n + p₁(1−p₁)/n; set the detectable difference equal to (z_α/2 + z_power) × sqrt of that variance and solve for n. The function uses exactly this.

**Exercise 2a.** The false-positive rate at 10 looks stays at about 19% (measured: 20.0%, 18.8% and 18.7% at 500, 2,000 and 10,000 users per look, which differ by no more than sampling noise). With equally spaced looks, the test statistic follows the same path in "information time" whatever the batch size, so only the *number* of looks matters, not how much data arrives between them. The batch size changes how long the test takes, not how often it lies.

**Exercise 3.** In the shipped run with 200,000 users and a 20% holdout, the brand-search interval is about −380 to 563 orders. Report your own interval widths for each combination, and say which lever (holdout fraction or total users) bought more precision. Raising the holdout fraction costs the business exposure on the withheld users; adding users costs time or reach.

**Exercise 4a.** Replicated detection at 2% lift with 5 treated regions is about two runs in three (68% over 300 runs); measure the 1.5% case yourself. **4b.** Expect the parallel-trends assumption to fail, so that difference-in-differences is biased towards the treated regions' higher surge; confirm the direction and size in your own run.

**Exercise 5.** Strong answers refuse both extremes: neither "the dashboard says 14x" nor "the experiment found nothing". The interval is compatible with a harmful, a negligible and a valuable channel, which is the finding. The follow-up is a design with enough power, run for long enough, with a decision rule agreed in advance.
