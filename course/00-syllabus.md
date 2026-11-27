# Syllabus: Marketing, Customer and Strategic Analytics

A twelve-module course that moves from the money behind a metric, through measurement and customer behaviour, to the organisational question of what analytics is for. It is written for working marketers and early-career analysts who can use a spreadsheet and are willing to read a little Python.

The modules are not the same size. Some are a week of work, others an afternoon, and that unevenness reflects how much each topic really needs.

**Status:** Modules 1, 4, 5, 6, 7 and 8 are complete (lessons, code, tests, exercises). Modules 2, 3 and 9 to 12 are specified below and will be built in the order shown under "Build order".

## Arc

The course makes one argument in three movements. Metrics only mean something once tied to the economics of the business (Part I). Whether an effect is *caused* by marketing, and what customers do over time, are separate questions that need their own methods (Parts II and III). And none of it matters unless the organisation changes a decision because of it, which is a strategy and governance problem rather than a technical one (Part IV).

## Part I: The economics under the metrics

**Module 1. Unit economics and the marketing financial model** *(built)*
Margin, break-even ROAS, loaded CAC, payback, LTV:CAC, spend ratio; why each simple formula fails and what replaces it. Pricing a consulting fee from the client's P&L.
*Source basis:* HQ Digital financial-model guide and 17/27 Nov posts, extended with cohort analysis.

**Module 2. Reading a P&L as a marketer**
Contribution margin, fixed versus variable cost, operating leverage, working capital and why fast-growing brands run out of cash while profitable on paper.

## Part II: Measurement and causation

**Module 3. Measurement design and tracking foundations**
Event taxonomy, GA4 data model, consent, identity, data-quality checks. Writing a measurement plan from a strategy.

**Module 4. Attribution and its disagreements** *(built)*
Why platform, analytics and finance numbers differ, what each credit rule assumes, scoring rules against a simulated world with known causal truth, reconciliation and calibration.

**Module 5. Experimentation and incrementality** *(built)*
Power and sample size, the peeking problem, user-level holdouts versus naive comparison, geo-lift with permutation inference, reporting uncertainty honestly.

**Module 6. Media mix modelling in practice** *(built)*
Adstock, saturation and controls fitted from scratch on three simulated years with known channel contributions; why a model that predicts well can still misallocate credit; profile analysis; calibration with lift tests; average versus marginal returns. Bayesian priors are named as the standard next step but not implemented.

## Part III: Customers over time

**Module 7. Cohorts, retention and repeat purchase** *(built)*
Cohort tables and their noise, censoring and exposure, the BG/NBD model fitted from scratch and tested on a holdout, and what breaks when a promotion violates its assumptions.

**Module 8. Segmentation and customer value** *(built)*
RFM and its tie and tenure traps, holdout validation with more than one metric, value concentration, probabilistic customer value with shrinkage. Clustering is deferred to a later revision.

**Module 9. Situations, messages and creative testing**
Turning "who is the audience" into "what are they going through now": review mining, angle design, test planning.

## Part IV: Strategy and the AI-era toolkit

**Module 10. Analytics strategy**
Choices before KPIs; KPI trees; linking each metric to the assumption it tests; decision logs.

**Module 11. Competitive and category intelligence**
Ad-library and search-demand tracking, funnel-destination changes, composite scores and their sensitivity to weights.

**Module 12. Analytics with AI, and checking it**
LLM-assisted querying with ground-truth gates, AI-search visibility audits with confidence intervals, agentic reporting and where it should not be trusted.

## Anchor reading (to be verified before each module is written)

Named references are deliberately listed as candidates rather than citations, since each must be read before it is cited.

- Unit economics and LTV: Fader and Hardie's work on probabilistic customer-base models (BG/NBD, Pareto/NBD).
- Experimentation: Kohavi, Tang and Xu, *Trustworthy Online Controlled Experiments*.
- Causal measurement: Gordon et al. on ad-effectiveness measurement and the gap between observational and randomised estimates.
- MMM: published open-source documentation from the major MMM libraries.
- Strategy: Rumelt, *Good Strategy / Bad Strategy*, for the strategy-versus-plan distinction that runs through Module 10.

## Build order and reasoning

1, 4, 5, 7 and 8 are done (7 and 8 share one simulated customer base; 4 and 5 share one simulated marketing world). The causal arc (4, 5, 6) is complete. Next 2 and 3, then 10, 9, 11, 12. Module 12 goes last because the tooling changes fastest and the verification habits it teaches depend on everything before it.

## Assessment

Each module ends with a short applied task and a written decision memo of no more than 500 words that states what the numbers support, what they do not, and what the reader should do. The memo is the real assessment. A correct calculation with no decision attached earns little.
