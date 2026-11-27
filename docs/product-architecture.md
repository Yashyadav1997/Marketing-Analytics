# From course code to products: an architecture note

*A planning document, not a commitment. Nothing in this repository has been security-reviewed, hardened or packaged, and every dataset in it is synthetic. Function names and figures below are taken from the code and lessons as they stand.*

## The starting point

The built modules are small, dependency-free reference implementations written to teach. That is a strength and a limit. They are short enough to audit line by line, and each one is paired with a simulation where the right answer is known. They are also pure Python on toy-sized data, with no notion of a customer, a tenant or a bad input. The honest framing is that the repo holds three kinds of asset, in descending order of how directly they transfer: the *simulators and the habits of validating against them*, the *formula and reconciliation logic*, and the *model code*, which would mostly be replaced by production-grade libraries but whose behaviour defines what "correct" means.

## What each module could become

**Unit economics (Module 1)** is the most product-ready, because it is arithmetic. `summarise` in `unit_economics.py` runs the chain from `gross_margin` through `loaded_cac`, `payback_months_simple` and `ltv_simple` to `ltv_cac_ratio`, and `cohort_payback_month` replaces the constant-rate payback with one read from observed cohorts. The lesson that the formula said 2.4 months for paid social where cohorts said 3.7 is itself a product behaviour: show both, side by side, and flag the gap. `required_incremental_revenue` turns a fee or budget into the lift it must earn, a small feature that sells itself in a sales conversation.

**Measurement and data quality (Module 3)** may be the best entry point of all, because it addresses the thing every other feature silently depends on. `run_audit` checks an event export against a written spec (`SPEC`) and `score` grades the audit against labelled defects; `clean_events` and `reconcile.main` produce a waterfall from ledger revenue to dashboard revenue; `stitch` and `people_counts` show how far device counts overstate people. In the simulation the headline lesson is a product behaviour in itself: naive dashboard revenue (76.3% of the ledger) and cleaned revenue (76.0%) look almost identical because defects that lose revenue (−3.0%) and defects that add it (+3.3%) cancel, while 24.0% was never tracked at all because of declined consent and ad blockers. A product that audits tracking *and* reconciles to the ledger would tell a customer something their dashboard cannot.

**Customer value (Modules 7 and 8)** would be built on `cohort_table` (which blanks cells that are not yet fully observable), `exposure_adjusted_rate`, and the BG/NBD pair `fit` and `p_alive`, plus `expected_purchases` for forecasts. Module 8's `build_customers`, `probabilistic_value` (expected repeat orders times shrunk order value, with `estimate_shrinkage_k`) and the tie-aware `top_share` and `spearman` give a scoring and validation layer. The product idea is not "a segmentation" but "a segmentation that reports its own holdout performance": every score shipped alongside its top-decile capture against a time-split holdout.

**Attribution reconciliation (Module 4)** is a reporting product more than a model. `credit_by_channel` with the rule functions (`last_click`, `first_click`, `linear`, `position_based`, `any_touch`) produces the columns of the reconciliation table; what a product adds is the ledger and analytics-tool rows, the unattributed-orders line, and calibration factors derived from experiments.

**Experiment planning and readout (Module 5)** maps to `n_per_arm`, `mde_relative` and `holdout_users_needed` for planning, `false_positive_rate` as the explanation of why peeking is unsafe, and `did` with `placebo_distribution` and `p_value` for geo tests. The permutation set must include the real treated regions; the lesson records that an earlier version got this wrong.

**Media mix modelling (Module 6)** is `mmm.fit` (adstock and saturation parameters searched with `nelder_mead`, linear coefficients solved exactly by `least_squares`), with `roi_table`, `marginal_roi`, the `calib` pseudo-observation for lift tests and `profile_roi.profile` for plausible ranges. This is the module a production system would most likely rebuild on a Bayesian library; the code's role would be as a specification of expected behaviour.

## The simulators as acceptance tests

The most distinctive thing in the repo, and the least obvious to package, is that three generators produce data with *known ground truth*: `world.py` (potential outcomes per user and channel, giving `true_incremental` and `true_programme_incremental`), `simulate.py` (a BG/NBD customer base with `customers_truth.csv`), and `generate.py` (weekly sales with true channel contributions). Ordinary analytics software has no oracle. This does.

A CI harness would regenerate a world, run a candidate feature over it, and assert on the *truth*, not on the previous output. Concretely, from the existing tests: the BG/NBD fit must recover r, α, a and b to within stated tolerances and forecast the 26-week holdout within 5% (the shipped result is 1,888 predicted against 1,910 actual orders); last-click must over-credit brand search by more than tenfold relative to `true_incremental`; a randomised holdout interval must cover the true incremental orders for paid social; the geo-lift estimator must be unbiased across replications (mean 5.04% at a true 5%). A new attribution engine, a faster BG/NBD, or a rewritten MMM would be accepted only if it passes these, which converts "does it look right?" into a regression suite. The generators can also be made adversarial on purpose, as Module 7's promotion option and Module 6's `decouple_social` flag already do, to check that a product degrades the way the lessons say it should.

## What is missing for production

The list is long, and each item has a lesson in the repo that argues for it.

*Performance.* Everything is pure Python. `bgnbd.fit` runs a Nelder-Mead search over per-customer log-likelihoods; at 2,500 customers it takes about a second, and nothing here suggests it scales to millions without vectorisation or a compiled library. `mmm.fit` re-solves a linear system inside every optimiser step, which is fine for six parameters and 156 weeks and unproven beyond that.

*Inputs.* There is no schema validation, no handling of missing weeks, duplicate orders, timezone drift or negative spend. Module 7's censoring lesson and Module 4's note that 516 of 3,956 orders carried no tracked touch both describe data conditions a real connector will meet constantly.

*Multi-tenancy, authentication, consent and PII.* None exists, and the code has no concept of a tenant. Customer-level scoring (Modules 7 and 8) handles exactly the data that privacy law cares about. This needs design from the start, not as a retrofit. There is also no audit trail of which data, parameters and calibration inputs produced a given number, which Module 6's warning about unvetted lift tests makes more than a compliance nicety.

*Uncertainty in the outputs.* The products do not yet attach intervals to what they report. `roi_table` returns point estimates; the intervals live in `profile_roi.py`, which makes assumptions the lesson itself flags (known noise variance, fixed curve shape) and are therefore too narrow.

*Validation on real data.* Every result comes from synthetic data in which the fitted model form equals the generating form. Module 6 says this directly and Module 7's promotion experiment shows a 10 to 15% forecast miss when the stationarity assumption breaks. Nothing here establishes performance on a real business, and a product should not claim it.

*Single-sample conclusions.* Module 8 is the standing example: on the shipped dataset BG/NBD beats the RFM composite by about one point of top-decile capture, with a bootstrap interval including zero, while across 22 other seeds the gap is 3.4 to 5.5. A production system must not choose between methods on one customer's one sample without that kind of check.

## A staged build order

The smallest useful slice, on the evidence of the repo, is a **reconciliation and unit-economics report** rather than any model: Module 1's chain plus Module 4's table, with Module 3's tracking audit and ledger waterfall in front of it, fed from a CSV export and a ledger total. Three reasons. It needs no unproven statistics, so it can be correct on day one. Its central claim, that platform-reported, analytics-tool and ledger figures disagree and the disagreement should be itemised, is already demonstrated with numbers (6,007 platform-credited orders against 3,956 real; blended MER 3.17 against a true programme return of 0.81 in the simulation). And it forces the data-ingestion, validation and tenancy work that every later feature depends on, at low risk.

After it, roughly in order of increasing statistical risk: experiment planning and readout (sample-size and holdout tools, where being wrong is cheap and visible); customer cohorts and probabilistic value with holdout self-validation; calibrated MMM last, because it is the module where the repo's own evidence says outputs are easiest to over-trust.

Questions that belong to the founder, not to this note: who the first customer is (an in-house D2C team, an agency running many clients, a consultancy); which connectors to build first and what each costs in maintenance; whether the product's promise is a number, a decision, or an audit; whether pricing follows data volume, seats, or value delivered; and how much of the education content stays public as acquisition.

## Principles to carry into the interface

Report ranges, not points. Module 6's profile shows TV's plausible ROI as roughly 2.8 to 4.8 and search's as 1.3 to above 7; a single "4.1" for search would misstate what the data know.

Show the reconciliation, always. The gaps between ledger, analytics tool and platforms, each labelled with its cause, are the product's credibility.

Record calibration provenance. A lift test pulled social's modelled ROI toward the wrong value without moving held-out error by more than 0.15 points, so every calibrated number must say which experiment produced it, how it was designed and whether its interval supports the value imposed.

Separate average from marginal. The uncalibrated model ranked social and search above TV on marginal ROI, the reverse of the truth; any allocation view should be built on marginal returns and say so.

Refuse when identification is weak. If two channels' spend correlates at 0.89, or a channel's plausible range spans a factor of five, the right output is the range and a recommendation to test, not a ranking. A product that sometimes says "the data cannot tell" is more useful, and harder to build, than one that always answers.
