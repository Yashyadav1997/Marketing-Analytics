# Lesson 3. Calibration, marginal returns and decisions

## Using experiments to anchor the model

Module 5 produced incrementality estimates with intervals. An MMM can use them. Treat a lift test as one extra, noisy observation of a channel's average ROI and add it to the fit: the model is then pulled toward the experiment in proportion to how precise the experiment is. In `mmm.fit` this appears as a *pseudo-observation*, `calib={"tv": (target_roi, standard_error, noise_sd)}`.

The results across five scenarios:

| Scenario | TV | Social | Search | Held-out error |
|---|---|---|---|---|
| True | 4.47 | 2.63 | 2.39 | |
| A. No calibration | 3.77 | 4.35 | 4.08 | 3.16% |
| C. Correct tests on TV and social | 4.38 | 3.10 | 4.32 | 2.73% |
| D. A *wrong* test: social = 5.0 | 3.54 | 4.88 | 3.96 | 3.31% |
| E. All three channels tested | 4.34 | 3.11 | 2.65 | 2.85% |

Three things to notice.

**Calibration helps where it is applied.** Testing TV and social pulls both toward the truth (TV 3.77 to 4.38; social 4.35 to 3.10). Search, which was not tested, stays overstated at 4.32. Calibration does not spread knowledge to channels you did not test; it only anchors the ones you did. When all three are tested (E), all three move close, and out-of-sample error improves a little.

**Social settles at 3.10, not 2.63.** The model is trading the experiment off against its own data, and where the two disagree it ends up in between. That is correct behaviour, but it means a calibrated number is a compromise, not the experiment result.

**A wrong test is invisible.** Scenario D feeds the model a lift test claiming social returns 5.0 when the truth is 2.63. The held-out error moves from 3.16% to 3.31%, which no one would notice. The model happily reports social at 4.88. This is the central warning of the module: the forecast cannot audit the calibration, because the data cannot discriminate between plausible ROIs (Lesson 2). A calibration input must therefore be vetted *as an experiment*: was it randomised, was it powered, did it run long enough, does its interval include the value being imposed?

## Average is not marginal

Every ROI above is an *average*: total contribution over total spend. A budget decision concerns the *next* unit of spend, whose return is lower whenever the response curve is flattening. `marginal_roi` raises a channel's spend by 10% in every week and measures the extra sales per extra unit:

| Channel | True average ROI | TRUE marginal | Uncalibrated marginal | All lift-tested marginal |
|---|---|---|---|---|
| TV | 4.47 | 2.49 | 2.24 | 2.56 |
| Social | 2.63 | 1.77 | 2.69 | 2.12 |
| Search | 2.39 | 1.54 | 2.66 | 1.85 |

Marginal returns are lower than average for every channel, which is just diminishing returns made visible. More important is the ranking. The truth says TV has the highest marginal return, then social, then search. The uncalibrated model puts social and search (both about 2.7) *above* TV (2.2). Acting on it means shifting money from the best channel to the other two. The fully calibrated model restores the correct order (2.56, 2.12, 1.85).

This is the point at which an MMM stops being an academic exercise: allocation decisions turn on the *ranking* of marginal returns, and the ranking is exactly what weak identification corrupts.

## Using it responsibly

**Report ranges.** A single ROI per channel is a false precision. Show the plausible range and say which channels are poorly determined.

**Say what it cannot answer.** MMM is coarse in time and in resolution. It speaks to quarterly budget splits, not to which creative to run on Tuesday.

**Pre-register the specification.** Decide the controls, the functional form and the validation scheme before looking at channel results. Revising them until a favourite channel looks good turns the model into an advertisement.

**Refresh and compare.** Rerun on a schedule and watch how the estimates move. Instability is itself a diagnostic: a channel whose ROI swings between refits is a channel the data cannot pin down.

**Triangulate.** Compare with attribution (Module 4) and with experiments (Module 5). Agreement across instruments that fail in different ways is the strongest evidence you will get. Disagreement tells you where to run the next experiment.

**Close the loop.** The best use of an MMM is often to decide *what to test next*: the channels with the widest plausible ranges and the largest spend are where an experiment buys the most information.

## What this module did not cover

Bayesian estimation with informative priors (the usual professional approach, and a more principled way to express calibration), time-varying effects, interactions between channels, hierarchical models across regions, and the choice between different saturation curves. Each matters in practice; each is easier to understand after seeing what the simple model cannot do.

## Check your understanding

1. In scenario C, search remains overstated at 4.32. If you could fund one more lift test, which channel would you test and why?
2. Explain why an MMM that is calibrated with a *noisy but unbiased* experiment is better than one calibrated with a *precise but biased* one, using scenario D.
3. A planner moves 20% of TV budget to social on the strength of the uncalibrated table above. Use the marginal ROIs to estimate the direction of the effect on total sales.
