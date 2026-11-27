# Lesson 2. Fit is not identification

Run `python3 experiments.py`. The first row, the full model with controls, gives:

| Channel | Estimated average ROI | True average ROI |
|---|---|---|
| TV | 3.77 | 4.47 |
| Social | 4.35 | 2.63 |
| Search | 4.08 | 2.39 |

The model fits the data to within the noise and predicts the held-out weeks to 3.2%. Yet it assigns social and search returns 65% and 70% above the truth and understates TV by 16%. If a finance team acted on this table, it would move money out of the best channel and into two mediocre ones, and the model's accuracy would defend it all the way.

## Why: two mechanisms, both ordinary

**Correlated spend.** TV and social were flighted together, with a spend correlation of 0.89. When they rise and fall in step, the data contain very little information about how to *divide* their joint effect. Many splits fit almost equally well. The model picks one, and nothing in the fit warns you that the split is arbitrary.

**Demand-following budgets.** Search budget is raised when demand is expected to be high. So search spend and sales rise together even if search does nothing at all. Seasonality controls remove the predictable part. What is left in search spend is the small week-to-week noise, which is the only variation the model can use to learn the channel's effect. That is not much to learn from, and the estimate is correspondingly fragile.

Remove the controls and the problem is exposed (row B):

| | Estimated | True |
|---|---|---|
| TV | 5.62 | 4.47 |
| Social | 3.92 | 2.63 |
| Search | 11.38 | 2.39 |

Search is credited with nearly five times its true return, because its budget tracks the season and the model, with no other way to explain the season, assigns it to search. Out-of-sample error doubles to 6.2%, so here the error is at least visible in the forecast. That is the easy case. With controls in place, the attribution is still wrong and the forecast is still good.

## It is not the optimiser

A tempting explanation for weird MMM results is that the optimiser landed in a bad local optimum. Here that is ruled out directly: six random starting points all converge to the same fit, and the largest disagreement in any channel's ROI is 0.000. The estimate is a stable, reproducible, systematically biased answer. Stability and correctness are different virtues.

## What the data can and cannot say

A *profile analysis* asks, for each possible value of a channel's ROI, how badly the data object to it. `profile.py` forces the model to a series of assumed ROIs, refits everything else, and reports how much the squared error rises, in units of the noise variance. A rise under about 3.84 means the value cannot be rejected at the 95% level.

| Channel | ROI values the data cannot reject | True ROI |
|---|---|---|
| TV | roughly 2.8 to 4.8 | 4.47 (inside) |
| Social | roughly 2.8 to 6.9 | 2.63 (just outside) |
| Search | roughly 1.3 to above 7 | 2.39 (inside) |

The statement worth taking from this is not the exact bounds but the widths. TV's plausible range is narrow enough to act on. Social's spans a factor of 2.5, and search's is close to uninformative: the data are consistent with search being a poor channel or a spectacular one. Reporting "search ROI 4.1" from this model conveys precision the data do not have.

A caution about the intervals themselves. They are conditional on the model form being right and on the noise variance being known, and they ignore uncertainty in the nonlinear parameters. They are therefore too narrow, and social's true value falling just outside is a small demonstration. Treat them as a lower bound on your uncertainty.

## The cheapest fix: vary the spend on purpose

Because the root problem is a lack of independent variation, the most effective remedy is to create it. In scenario F the social flights are scheduled independently of TV (spend correlation drops to −0.11):

| | Correlated flights | Independent flights | True (independent world) |
|---|---|---|---|
| TV | 3.77 | 4.65 | 4.47 |
| Social | 4.35 | 2.96 | 2.55 |

Social's error falls from 65% to 16%, and TV's from 16% to 4%. No cleverer algorithm achieved this; a different media calendar did. Search, whose budget still follows demand, remains overstated at 3.44 against 2.37. The practical rule: if you plan the media calendar with measurement in mind (staggering launches, occasionally varying channel levels, running geo-split pulses), the next MMM will be more informative than any change to the model.

This also shows an uncomfortable dependence. A mature advertiser who optimises spend patterns for efficiency tends to produce exactly the correlated, flat, demand-following histories that MMM struggles with. The better the media planner, the harder the model's job, unless someone protects some variation for learning.

## Check your understanding

1. Search's budget follows expected demand. List three controls you could add, beyond the seasonal terms, to help separate its effect, and what each requires.
2. Why can a model with controls still over-credit search? (Think about what is left in the search series after the controls take out the predictable part.)
3. A vendor shows a model with a 2% out-of-sample error and says it proves the channel ROIs are right. Write a three-sentence reply.
