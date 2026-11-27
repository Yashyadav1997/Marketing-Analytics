# Lesson 1. From strategy to a tracking spec

Most tracking plans are built backwards. Someone installs a tag manager, switches on every automatic event the tool offers, and later asks what the data can answer. The result is thousands of events nobody asked for and a handful of questions the data cannot address.

The forward direction is slower and much cheaper over a year.

```
strategy  →  assumptions to test  →  decisions  →  KPIs  →  events and parameters
```

## Start with the choice, not the metric

Module 10 will treat strategy properly; here only the link matters. A strategy is a set of choices: which customers, why us, what we will not do. Each choice rests on assumptions about customer behaviour. Take a brand that decides to compete on repeat purchase in a category where most competitors chase first orders. That choice rests on an assumption: that customers who buy twice become materially more valuable, and that the brand can influence the second purchase.

Three things follow from the assumption. There is a decision it should inform (how much to pay for a first customer; whether to invest in a replenishment reminder). There are KPIs that test it (repeat-purchase rate; time to second order; value of second-order cohorts). And there are events and identifiers required to compute those KPIs (a purchase event with a stable transaction id, and an identifier that recognises the same person across orders).

A KPI without a decision attached is decoration. An event with no KPI depending on it is cost, since it must be implemented, maintained and governed.

## The specification

`spec.py` holds a deliberately small one. Each event names its required parameters and their types:

| Event | Required parameters |
|---|---|
| page_view | page_location (text) |
| view_item | item_id (text) |
| add_to_cart | item_id (text), value (number) |
| begin_checkout | value (number) |
| purchase | transaction_id (text), value (number), currency (text) |

And `KPI_DEPENDENCIES` maps each KPI to the events it needs: conversion rate needs page views and purchases; cart abandonment needs add-to-cart and purchase; repeat-purchase rate needs purchase *and a persistent customer identifier*, a requirement the event list alone does not reveal.

Working through the dependency table is a useful exercise in its own right. It tells you what you can *not* compute from the current tracking (anything depending on an event not in the spec), which events are most load-bearing (purchase appears in every business KPI, so a defect there contaminates all of them), and which KPIs share failure modes.

## The event model

Modern analytics tools, GA4 among them, model behaviour as a stream of events, each with a name, a time, an identifier for the device or browser, optionally a user identifier, and a set of parameters. Two consequences matter for design.

**Names and parameters are a contract.** The tool will accept almost any name and any parameter value. Nothing stops `Purchase`, `purchase ` and `purchase_complete` from coexisting, and each will be counted as a different event. The contract exists only if you write it down and check against it.

**Identity is optional.** Every event has a device or browser identifier; only some carry a login identifier. Any metric defined over *people* (users, repeat rate, lifetime value) is a claim about how well devices have been joined into people. Lesson 3 measures how large that claim is.

## What a good spec states

- The exact event name, in a case and separator convention, with an owner.
- Required and optional parameters, their types and permitted values (currency as a code, value as a number, never a formatted string).
- When the event fires, and when it must *not* (a purchase event on order confirmation, once, not on every page refresh).
- What happens on failure (a purchase that cannot be assigned a transaction id should be logged as an error, not sent as an orphan).
- The KPIs that depend on it.

## Privacy as a design constraint

Consent decisions determine which people appear in the data at all. In the simulated store 18% decline and 8% run blockers; the next lessons show what that does to totals. The design implication is that measurement must be planned on the assumption that a substantial, non-random share of customers will be unobserved, and that the unobserved are not a random sample (people who decline consent differ from those who accept). Decide in advance what you will report as observed, what as modelled, and how you will say so. Consent requirements are legal matters that vary by jurisdiction; take advice rather than inferring them from a course.

## Check your understanding

1. A brand's strategy is to win on a premium, gifting-led positioning. Write one assumption, one decision it informs, two KPIs and the events they need.
2. Which event in the spec above is the most load-bearing? What would you add to the spec to protect it?
3. A marketing manager asks for "all the clicks" to be tracked. How would you reply, and what would you ask first?
