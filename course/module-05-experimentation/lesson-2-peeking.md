# Lesson 2. Discipline: peeking and stopping rules

A significance test is calibrated for a single look at a pre-planned sample. The 5% false-positive rate is a promise about *that* procedure. Check the result every day and stop when it first turns significant, and you are running a different procedure, whose error rate is much higher.

## The experiment on the experiment

`peeking.py` runs thousands of A/A tests: both arms have exactly the same conversion rate, so any "significant" difference is a false positive by construction. It compares two rules. One checks after every batch and stops at the first p < 0.05. The other looks once, at the end.

| Number of looks | Stop at first p<0.05 | Single look at the end |
|---|---|---|
| 1 | 5.2% | 5.2% |
| 2 | 8.8% | 5.2% |
| 5 | 13.6% | 4.7% |
| 10 | 18.8% | 4.9% |
| 20 | 24.6% | 5.0% |

The right-hand column is the promise, kept: about 5%, whatever the number of interim looks, provided you do not act on them. The middle column is what peeking does. Ten looks nearly quadruples the false-positive rate, and twenty brings it to about one in four. The test did not become less valid by being watched; the decision rule became different.

The intuition is that the test statistic wanders. Over a long run it is quite likely to cross the threshold at some point even when nothing is happening, and a rule that stops the moment it crosses will find that crossing nearly every time it exists.

## Why it matters in marketing

Dashboards update daily and everyone looks. A manager sees a creative test "winning" on day three and ends it. The result is then reported, repeated in a deck and acted on. Across a year of such tests, a substantial fraction of the "wins" are noise, and the business slowly adopts a collection of changes that do nothing, believing each one worked. It is a quiet cost because nobody can see the counterfactual.

## Honest ways to look early

**Decide the sample size in advance and do not stop on a p-value.** The simplest rule and the hardest to keep.

**Correct for the number of looks.** A crude correction tests each look at α divided by the number of looks (Bonferroni). For ten looks that means demanding z > 2.81 instead of 1.96. In the simulation it brought the false-positive rate to 2.8%, under the target: the correction is conservative because looks are correlated, so it costs power. Alpha-spending designs (Pocock, O'Brien-Fleming) are more efficient and are what dedicated experimentation platforms implement.

**Use sequential methods built for continuous monitoring.** These control error at any stopping time, at some cost in sample size. They exist because the demand to peek is not going away.

**Separate monitoring from deciding.** Looking at guardrail metrics (is the test breaking checkout?) to *stop for harm* is a different activity from looking at the primary metric to *stop for success*. It is legitimate and wise to do the first continuously.

## Other ways a valid test goes wrong

- **Sample ratio mismatch.** If you assigned 50/50 and observed 52/48 over 100,000 users, something is wrong with assignment or logging, and the result is unreliable whatever the p-value says. Check the split before reading the outcome.
- **Many metrics.** Test twenty metrics at 5% and you expect one false positive. Name one primary metric in advance.
- **Segment fishing.** "It lost overall but won among women over 35" is a hypothesis for the next test, not a finding.
- **Novelty and carry-over effects.** A new creative may win in week one because it is new. Run long enough to span the effect, and avoid reusing the same users across tests that interact.

## Check your understanding

1. Predict, then check by changing `n_per_look`: does the false-positive rate from peeking at 10 looks change if each look adds more data? (It does not, to within noise. Explain why the number of looks, not the batch size, drives the error.)
2. A team runs 50 creative tests a year with daily peeking and stopping at significance. Roughly how many "wins" would you expect if none of the creatives had any effect?
3. Write a one-paragraph "test charter" for a creative test: primary metric, sample size, stopping rule, what you will do with each outcome.
