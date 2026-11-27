# Marketing Analytics

A working repository for building a course and project library in marketing analytics, customer analytics and analytics strategy.

It began with a research pass over the public output of one marketing educator (Apurv Singh, @apurv_sngh, and the HQ Digital site) to see which ideas in a heavily followed, practice-led corner of the field translate into teachable analytical method. The pass was then widened and gap-checked against what a serious analytics curriculum needs. Everything here is written from scratch; nothing is copied from paid or gated material.

## Where things are

```
research/
  01-source-extraction.md   what was read, what was not, what it is worth as evidence
  02-agentic-loop-method.md the observe-extract-score-cluster-gap-check-build loop
  03-idea-backlog.md        scored project ideas by subject (marketing, customer, strategy, AI, competitive)
course/
  00-syllabus.md            twelve modules in four parts, with build order
  module-01-unit-economics/ complete: lessons, exercises, case study, tested code, synthetic data
  module-04-attribution/    complete: credit rules vs causal truth, reconciliation, calibration
  module-05-experimentation/ complete: power, peeking, holdouts, geo-lift
  module-06-mmm/            complete: adstock, saturation, identifiability, calibration, marginal returns
  module-07-cohorts-retention/ complete: cohorts, censoring, BG/NBD from scratch, simulated customer base with ground truth
  module-08-segmentation-value/ complete: RFM, holdout validation, concentration, probabilistic value
```

## Start here

1. Read `research/03-idea-backlog.md` for the map of ideas and why each scored as it did.
2. Read `course/00-syllabus.md` for the arc.
3. Work through Module 1, then 4, 5 and 6 (the causal arc: attribution, experiments, media mix; 4 and 5 share a simulated world), then 7 and 8 (shared simulated customer base). All code needs only Python 3.10+ and the standard library:

```bash
cd course/module-01-unit-economics/code
python3 -m unittest -v
python3 generate_cohorts.py
python3 cohort_payback.py
```

Every module follows the same pattern (`python3 -m unittest`, then the scripts named in each module's README).

## Status

| Piece | State |
|---|---|
| Source research, first pass | done |
| Idea backlog | done, scored |
| Syllabus | done |
| Module 1 | done, 10 tests passing |
| Module 4 | done, 12 tests passing |
| Module 5 | done, 14 tests passing |
| Module 6 | done, 14 tests passing |
| Module 7 | done, 7 tests passing |
| Module 8 | done, 13 tests passing |
| Modules 2, 3, 9 to 12 | specified, not yet written |
| Second research loop (YouTube, newsletter) | not started |

## Product direction

The course code is deliberately dependency-free reference implementation: unit economics, cohort and BG/NBD models, attribution and reconciliation, power and incrementality tools, validated segmentation. The plan is to build custom SaaS products for marketing analytics on top of these. The pieces most likely to carry over are the formula libraries, the simulators with known ground truth (useful for regression-testing any analytics product against a known answer), and the reconciliation and validation patterns. Nothing here has been packaged, hardened or security-reviewed for production use.

## Caveats worth keeping in view

Benchmarks quoted from practitioner sources are priors, not findings; the course asks learners to test them. All datasets in this repository are synthetic. Instagram video content was not transcribed, so inferences about it rest on captions.
