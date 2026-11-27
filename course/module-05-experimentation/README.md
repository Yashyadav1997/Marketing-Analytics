# Module 5. Experimentation and incrementality

## Where Module 4 left us

Credit rules divide a sale among the touches that preceded it. They cannot say whether the sale would have happened anyway, because they never observe the world in which the channel was absent. An experiment manufactures that world: withhold the treatment from a random subset and compare. This module is about doing that well enough to trust the answer, and about being honest when a business cannot afford the sample size the question demands.

## Outcomes

1. Compute the sample size for a conversion test and explain why small effects on small base rates are expensive.
2. Explain why exposure-based comparisons are biased and a randomised holdout is not.
3. Recognise and quantify the peeking problem.
4. Run and read a geo-based lift test with placebo inference.
5. Report an incrementality result with its interval, and know when "we cannot tell" is the correct finding.

## Contents

| Part | File | Time |
|---|---|---|
| Lesson 1 | [Power: how much data a question costs](lesson-1-power.md) | 60 min |
| Lesson 2 | [Discipline: peeking and stopping rules](lesson-2-peeking.md) | 45 min |
| Lesson 3 | [Holdouts, selection and geo-lift](lesson-3-holdouts-and-geolift.md) | 90 min |
| Exercises | [exercises.md](exercises.md) | 4 hours |
| Code | [code/](code/) | reference |

## Running it

Reuses the simulated world from Module 4.

```bash
cd course/module-05-experimentation/code
python3 -m unittest -v       # 14 tests, about 5 seconds
python3 power.py             # sample-size tables
python3 peeking.py           # false-positive rates under repeated looks
python3 holdout.py           # user-level holdouts vs naive, graded against truth (about 15 s)
python3 geolift.py           # matched-market lift with permutation inference (about 15 s)
```

**Anchor reading** (to verify before relying on it): Kohavi, Tang and Xu, *Trustworthy Online Controlled Experiments*, for the practice of online experimentation including sample ratio checks and sequential testing.
