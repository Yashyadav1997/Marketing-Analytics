# Module 6. Media mix modelling in practice

## Where this fits

Module 4 showed that credit rules cannot recover causation from user journeys. Module 5 showed that experiments can, at a cost in sample size and for only the channels you can withhold. Media mix modelling (MMM) is the third instrument: it works from aggregate weekly spend and sales, needs no user-level tracking, and can include channels that cannot be experimented on, television and outdoor among them. Its weakness is the mirror image of its strength. With only a few hundred weekly observations and several channels that move together, the data can fit well while saying little about *which* channel did the work.

This module builds a model from scratch, runs it on a simulated three years in which every channel's true contribution is known, and spends most of its time on the gap between fitting the data and identifying the effects.

## Outcomes

1. Specify a model with carry-over (adstock), diminishing returns (saturation) and controls, and fit it.
2. Distinguish predictive accuracy from causal identification, and show the difference with a profile analysis.
3. Explain how correlated spend and demand-following budgets bias estimates, and how omitting controls makes it worse.
4. Calibrate a model with lift-test results, and say what that can and cannot fix.
5. Distinguish average from marginal return and see how mistakes in the first lead to wrong budget moves.

## Contents

| Part | File | Time |
|---|---|---|
| Lesson 1 | [The model: carry-over, saturation and controls](lesson-1-the-model.md) | 60 min |
| Lesson 2 | [Fit is not identification](lesson-2-fit-is-not-identification.md) | 90 min |
| Lesson 3 | [Calibration, marginal returns and decisions](lesson-3-calibration-and-decisions.md) | 75 min |
| Exercises | [exercises.md](exercises.md) | 4 hours |
| Code | [code/](code/) | reference |

## Running it

Standard library only (it reuses Module 7's small optimiser).

```bash
cd course/module-06-mmm/code
python3 -m unittest -v      # 14 tests
python3 generate.py         # regenerates ../data/weekly.csv (seeded) and prints the true ROIs
python3 experiments.py      # the scenarios every lesson refers to (about 5 seconds)
python3 profile_roi.py         # profile analysis of each channel (about 10 seconds)
```

## About the data

156 weeks, three channels, invented figures in thousands. TV is flighted in bursts. Social is flighted alongside TV (spend correlation 0.89). Search budget is raised in the seasonal peak, so it moves with demand for reasons unrelated to its own effect. `data/weekly.csv` includes the true weekly contribution of each channel, which a real project never has.

The model form used to fit is *the same as the one that generated the data*. That makes every result in this module flattering: real response curves are not exactly exponential saturation, and real analysts do not know the right functional form. When the model fits badly here, expect it to fit worse on real data.

**Anchor reading** (to verify before relying on it): the published documentation and papers of the major open-source MMM libraries, for Bayesian treatments with priors, which are the usual way of expressing what the data alone cannot determine.
