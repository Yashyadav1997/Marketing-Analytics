# Exercises

## Exercise 1. Rebuild the credit tables (45 min)

Using `world.simulate()` and without calling `attribution.credit_by_channel`, compute last-click, first-click and linear credit by channel. Reproduce the first three columns of the report. Then verify, by direct count, that the platform "any touch" total is 6,007 and that the rule-based totals each equal the 3,440 touched orders.

## Exercise 2. A smarter rule, scored (90 min)

Implement one "data-driven" model: either a Shapley-style allocation over channel subsets, or a Markov removal-effect model on journeys (transition probabilities between channel states, conversion and null absorbing states, removal effect of each channel).

a. Compute its credited orders and ROAS by channel.
b. Compare with last-click, position-based and the ground truth. Is it closer to the truth than the best rule-based model? On which channels?
c. Explain what remains uncorrected, in terms of what the model sees (observed journeys) and what the truth requires (counterfactuals).

*No reference result is given. Report what you find, including if the data-driven model does worse than you expected.*

## Exercise 3. Change the world (60 min)

Edit `SPEC` in `world.py`, one change at a time, rerun `attribution.py`, and describe what happens to the gap between last-click and the truth for each affected channel.

a. Make brand search reach low- and high-intent users equally (exposure 0.30 for both).
b. Make email reach everyone with the same probability.
c. Double the true lift of brand search.

For each, state the principle the result illustrates. Which of these changes makes last-click *less* misleading, and why?

## Exercise 4. The decision memo (60 min, 400 words)

The CFO asks: "Brand search costs 125,000 and the dashboard says it returns 14x. Can we cut it?" Using only what you could know in a real business (not the ground truth), write the memo. State the recommendation, the evidence for and against, the single experiment you would run first, how you would design it so it can fail, and what result would change your mind.

## Exercise 5. Calibration and its limits (60 min)

a. Compute calibration factors (true incremental ÷ last-click credit) for each channel in the default world.
b. Re-simulate with five other seeds and report the spread of each factor.
c. Now modify `SPEC` to simulate a change of targeting (for example, email now reaches 0.30 of high-intent users instead of 0.50) and apply the *old* factors to the new world. How far off is the corrected estimate for email? What does that say about how often a factor must be refreshed?

---

## Hints and reference points

**Exercise 1.** The platform total is the sum over converting users of the number of distinct channels touched. Note that credit totals only count converting users.

**Exercise 3.** (a) Last-click error for brand search shrinks substantially, because the channel no longer concentrates on people who would have bought anyway; selection, not position, was the driver. (b) The same logic applies to email. (c) A larger true lift narrows the gap in relative terms but does not fix the structural over-credit. Check these against your own output rather than taking them on trust.

**Exercise 4.** A strong memo does not argue from the 14x. It notes the intent-selection mechanism, proposes a randomised holdout or a geo test that suppresses brand search for a sample, and sets a pre-agreed decision rule. Module 5 supplies the design, including the sample size you would need, which for a low-incrementality channel is larger than people expect.

**Exercise 5.** In the default world the factors are very stable across seeds (for example brand search about 0.05, email about 0.25) because nothing about the world changes between them. The targeting change in (c) is what breaks the factor; the size of the error is for you to find.
