# Module 4. Attribution and its disagreements

## The situation every marketing team recognises

Open the ad platform and it claims a conversion. Open the analytics tool and it claims a different one. Add up what each channel says it delivered and the total exceeds the sales ledger. Meanwhile finance wants one number. The disagreement is usually treated as a tooling bug to be fixed, but most of it is structural: the sources are answering different questions, and none of them is the question the budget actually turns on, which is *what would have happened without this spend?*

This module builds a small world in which that last question has a known answer, then runs the standard attribution rules over it and scores them.

## Outcomes

1. Explain why platform, analytics-tool and finance figures disagree, and classify each source of disagreement.
2. State the assumption built into each rule-based model (last-click, first-click, linear, position-based) and predict which channels it will flatter.
3. Distinguish *credit* from *causal contribution*, and explain why credit rules cannot recover the second.
4. Produce a reconciliation table that a finance lead would accept, with its limits stated.
5. Use experimental estimates to calibrate attribution, and say when that is unsafe.

## Contents

| Part | File | Time |
|---|---|---|
| Lesson 1 | [Why the numbers disagree](lesson-1-why-the-numbers-disagree.md) | 45 min |
| Lesson 2 | [Credit rules and what they assume](lesson-2-credit-rules-and-what-they-assume.md) | 75 min |
| Lesson 3 | [Reconciliation and calibration](lesson-3-reconciliation-and-calibration.md) | 60 min |
| Exercises | [exercises.md](exercises.md) | 3 to 4 hours |
| Code | [code/](code/) | reference |

## Running it

```bash
cd course/module-04-attribution/code
python3 -m unittest -v       # 12 tests
python3 attribution.py       # the reconciliation report every lesson cites
```

## The simulated world

`world.py` generates 50,000 users, each with a latent purchase intent. Five channels (influencer, paid social, generic search, email, brand search) reach users selectively. Brand search and email mostly reach people who were already likely to buy. Each channel adds a true lift to purchase probability. A single random draw per user decides whether they buy under every scenario, so for each user and channel the code knows whether the sale would have happened without that channel. Real data never offers this.

All parameters are invented. The point is the *structure* of the errors, not their size. Revenue per order is a flat 1,000, so ROAS here is revenue-based; real decisions need margin (Module 1).

**Anchor reading** (to verify before relying on it): the literature on observational versus randomised estimates of advertising effects, notably Gordon, Zettelmeyer, Bhargava and Chapsky on Facebook ad measurement.
