# Exercises

## Exercise 1. Rebuild the transforms (45 min)

a. Without importing `mmm`, compute the adstock and saturation of the TV series with the true parameters (decay 0.60, K 1100) and confirm that `beta × saturation` reproduces the `true_tv` column in `data/weekly.csv`.
b. Plot (or tabulate) the saturation curve for K = 300, 1100 and 3000. At what adstock level does each reach 63% of its maximum? Explain why K is hard to estimate for a channel that rarely spends enough to saturate.

## Exercise 2. Break the identification (60 min)

Using `generate.simulate()` and `mmm.fit`, vary the world one thing at a time and report the ROI errors:

a. Raise the TV–social correlation further (make social a scaled copy of TV plus small noise). How do the two ROIs behave? Is the *sum* of their contributions better determined than either alone?
b. Make search budget completely independent of demand. Does its ROI become accurate? What does that say about the cause of its bias in the shipped data?
c. Shorten the history to 78 weeks. Which channels degrade first?

## Exercise 3. A saturation you did not model (75 min)

Change the generator so one channel follows a different response curve (for example an S-shaped Hill curve, or a linear one) while the model still fits an exponential saturation. Compare ROIs, marginal ROIs and held-out error with the matched-model results. How large does the specification error have to be before the held-out error shows it?

## Exercise 4. Profile and plan (60 min)

a. Run `profile_roi.py` for each channel and tabulate the range of ROIs not rejected at the 95% level.
b. Rank the channels by *value of an experiment*: roughly, how wide is the range multiplied by the spend at stake? Which would you test first?
c. Design that experiment using Module 5's tools: choice of design (holdout or geo), duration, size, and the smallest effect it could detect.

## Exercise 5. The allocation memo (75 min, 500 words)

You must recommend how to shift 15% of the media budget among TV, social and search. You have the uncalibrated model, one reliable geo-lift on TV, and a platform report on social. Write the memo. State the recommendation and the evidence, report each channel's range rather than a point, explain how the average-versus-marginal distinction changes the advice, name what you would test next, and say which result would reverse the recommendation.

---

## Hints and reference points

**Exercise 1b.** Saturation reaches 63% when adstock equals K. For a channel whose adstock never exceeds K, the curve looks nearly linear over the observed range, and K and beta become hard to separate: a larger K with a larger beta produces almost the same curve. This trade-off is a standing source of instability in practice.

**Exercise 2.** For (a), expect the *sum* of the two contributions to remain much better determined than the split, which is the signature of collinearity. For (b) and (c), report what you measure; the shipped results suggest independent variation is the main lever (scenario F improved social from a 65% to a 16% error).

**Exercise 3.** There is no reference answer; the question is whether held-out error warns you. Note whether it does.

**Exercise 4.** From the shipped analysis the widest range belongs to search, but it also has the smallest marginal return (1.5 on the truth), so the value of resolving it is mostly in not over-spending. Social has both a wide range and a large budget. Argue your own ranking with numbers.

**Exercise 5.** Strong memos avoid recommending a move that depends on a ranking the data cannot support. Where the evidence is weak, propose a *staged* move paired with the experiment that would settle it.
