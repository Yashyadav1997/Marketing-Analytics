# Idea backlog: projects and subjects

Scores are Relevance / Evidence / Buildability, each out of 5. "Source" says whether the idea came from the Instagram footprint or was added in the gap-check. Entries are uneven on purpose; some deserve a paragraph and others a line.

## A. Marketing analytics

**A1. Unit-economics chain for a D2C brand** (5 / 4 / 5) *Source: HQ guide.*
Margin, break-even ROAS, loaded CAC, payback, LTV:CAC, spend ratio, built as a model that updates monthly. Project: replicate it in a spreadsheet and in Python, then break it, by changing return rate, discounting and mix of new versus repeat buyers, and watch which link fails first. **Built as Module 1.**

**A2. Cohort payback versus formula payback** (5 / 4 / 5) *Gap-check, motivated by A1.*
The constant-frequency payback formula is optimistic when repeat rates decay. Project: quantify the gap on cohort data by channel. Built into Module 1 with synthetic data; a natural extension is to run it on a public e-commerce dataset.

**A3. Attribution and its disagreements** (5 / 3 / 4) *Gap-check.*
Platform-reported conversions versus GA4 versus a post-purchase survey versus blended MER. Project: reconcile three numbers for one month and explain every gap. The source supports the motivation (loaded CAC runs well above platform CAC) but supplies no method.

**A4. Incrementality and geo-lift experiments** (5 / 3 / 3) *Gap-check.*
The honest answer to "did the ads cause this?". Project: design a matched-market holdout, power it, and decide what effect size would justify the spend.

**A5. Lightweight media mix modelling** (4 / 3 / 3) *Gap-check.*
Bayesian or regularised regression on weekly spend and sales, with saturation and adstock. Project: fit on synthetic data with a known truth and test whether the model recovers it.

**A6. Funnel-destination tracking** (4 / 4 / 3) *Source: HQ Index post of 24 Nov.*
Log where ads land over time using the Meta Ad Library (landing page, homepage, marketplace) and watch for structural changes. Project: track five brands in one category for eight weeks and report funnel shifts. Mind the platform's terms and keep it to public, aggregate observation.

## B. Customer analytics

**B1. RFM and behavioural segmentation** (5 / 3 / 5) *Gap-check.*
Classic, cheap, still useful. Project: segment an order table, then test whether the segments differ in downstream value out of sample, which most tutorials skip.

**B2. Retention curves and repeat-purchase modelling** (5 / 3 / 4) *Gap-check, supports A2.*
Beta-geometric / BG-NBD style models for non-contractual settings. Project: forecast second-order probability and compare with the naive average.

**B3. Customer lifetime value, honestly** (5 / 4 / 4) *Source: HQ guide, extended.*
The simple LTV formula assumes constant frequency and fixed lifespan. Project: compare it with a cohort-based and a probabilistic LTV and show how the LTV:CAC verdict changes.

**B4. Situation-led audience insight ("Who x Now")** (4 / 3 / 4) *Source: post of 21 Nov.*
Turn the audience-plus-situation idea into a research design: survey or review mining to surface situations, then map them to messages. Project: mine 500 public product reviews for purchase situations and cluster them.

**B5. Churn and winback targeting** (4 / 2 / 4) *Gap-check.*
Uplift modelling rather than propensity alone: who is *persuadable*. Easy to get wrong, so worth a module.

## C. Analytics strategy

**C1. Strategy before KPIs** (5 / 3 / 4) *Source: post of 17 Nov.*
Take a brand, write the choices (target customers, reason to prefer, deliberate omissions, testable assumptions), then derive the measurement plan from them. Project: build a KPI tree and name, for each metric, the assumption it tests.

**C2. Pricing a client engagement from the client's P&L** (4 / 4 / 5) *Source: post of 27 Nov.*
Break-even on a fee. Small but transferable: the same logic prices an internal analytics team. Built into Module 1, Lesson 4.

**C3. Measurement plans and governance** (4 / 2 / 5) *Gap-check.*
Event taxonomy, naming conventions, consent, data quality checks. Dull and decisive. Project: audit a GA4 property against a written spec.

**C4. Building an analytics function** (3 / 2 / 3) *Gap-check.*
Where analytics sits, who owns definitions, how decisions get logged. More case-based than technical.

## D. AI-era analytics

**D1. Measuring AI-search visibility without fooling yourself** (4 / 3 / 4) *Source: AEO/GEO posts and HQ Index.*
Prompt sets, repeated sampling, share-of-answer, and the variance problem (model answers differ run to run). Project: build a repeatable visibility audit with confidence intervals. The source itself warns that prompt-level volumes are not published, which is the right starting scepticism.

**D2. LLM-assisted analysis with verification gates** (5 / 3 / 5) *Source: posts of 25 and 22 Nov.*
Use a model to draft queries and summaries, then check against a known-answer set. Project: a harness that scores model-generated SQL against ground truth.

**D3. Agentic reporting workflows** (3 / 2 / 4) *Source: Claude-app posts.*
Scheduled analyses that produce a written read with every number traceable. Interesting, but tool-dependent and fast-ageing, so it sits late and stays short.

## E. Competitive and creative intelligence

**E1. Category league tables** (3 / 3 / 3) *Source: HQ Index.*
Composite brand scores are easy to build and easy to over-trust. Project: reproduce a league table method and run a sensitivity analysis on the weights. Mostly a lesson in how much a ranking depends on arbitrary choices.

**E2. Creative testing design** (4 / 3 / 4) *Source: Who x Now; gap-check.*
Hypotheses, sample size, and why most ad "tests" are underpowered. Project: power calculations for a realistic CTR and CVR.

## What was dropped

Pure model-release news, tool walkthroughs, and the career-mindset posts. They are valuable to their audience but do not teach a transferable analytical method, and they date quickly.

## Gaps the source does not cover

Causal inference beyond A/B tests, forecasting, experimentation platforms, privacy and consent regimes, and non-D2C settings (B2B pipelines, subscriptions, marketplaces). The syllabus fills these deliberately and marks them as non-source material.
