# Lesson 2. Auditing what you can see

An audit compares what the tracking sent with what the spec says it should have sent. `audit.py` does this for the simulated export of about 130,000 events and then, because the injected defects are labelled, grades itself.

| Defect | Injected | Flagged | Caught | Precision | Recall |
|---|---|---|---|---|---|
| Event name not in spec (case, spaces, aliases) | 51 | 51 | 51 | 100% | 100% |
| Missing transaction id | 57 | 56 | 56 | 100% | 98.2% |
| Duplicate purchase events | 96 | 96 | 96 | 100% | 100% |
| Value written as text | 44 | 44 | 44 | 100% | 100% |
| Missing currency | 61 | 59 | 59 | 100% | 96.7% |
| Impossible timestamps | 23 | 23 | 23 | 100% | 100% |
| Bot traffic | 4,096 | 4,096 | 4,096 | 100% | 100% |

It looks like a triumph. It should be read with some suspicion.

## Why the audit scores so well

Because the audit checks precisely the things the spec says and the simulation injects precisely those defects. Perfect precision is close to a tautology: the labels and the detectors were written to agree. This is the first lesson of auditing: **an audit finds violations of the contract you wrote, not problems in general.** Real exports contain defects nobody anticipated (a promotion code leaking into the value field, a currency symbol in an id, two apps firing the same event with different parameters), and finding those requires exploring the data without a rule to match.

## The two misses are the instructive part

Two rows fall short of perfect recall. Three events carried a missing transaction id or currency and were not flagged. Every one of them had an event name that the audit could not map to the spec (`purchase_complete`). The audit trims whitespace and lower-cases names, so `Purchase` and `purchase ` are recognised and checked; `purchase_complete` is a different word, so the audit reports the unknown name but skips the parameter checks on it. The defects on those events went unexamined because the events were not recognised.

The general principle: **an event you do not recognise is an event you cannot check.** Unknown names are not a cosmetic problem; they open a hole in the audit exactly where the data is already suspect. Reviewing and resolving unknown names is the first job of any audit, before the parameter checks mean anything.

## What each defect does

**Name variants** split a single event across several names. A dashboard filtering on exactly `purchase` silently drops the rest. In this simulation it loses a small slice of revenue, but over months, as developers add new variants, the loss grows.

**Missing transaction ids** make deduplication impossible: you cannot tell whether two events are one purchase counted twice or two purchases.

**Duplicates** inflate purchases, revenue and conversion rate, and usually come from a confirmation page that fires on refresh or two tags on one page. They are among the commonest and most costly errors.

**Text values** (`"1,299.00"` in place of `1299.0`) are ignored by tools that sum numbers, so revenue silently falls.

**Missing currency** makes revenue ambiguous in a multi-currency business.

**Impossible timestamps** push events outside the reporting window, so they are counted in no period or the wrong one.

**Bots** inflate page views and sessions without ever buying, depressing conversion rate. Here 15 devices produced 4,096 events: about 3% of all events and 4.0% of page views, which understates a conversion rate computed per page view by about 4%. That is a small bias in absolute terms and a large one against the few-percent improvements a team may be trying to detect.

## Building an audit that lasts

A one-off audit decays within weeks. Make the checks run on a schedule against fresh data, and report the counts, not just pass or fail. Alert on *changes*: a jump in unknown names, a rise in duplicates after a release. Keep the spec in version control, so a code change to the site and a change to the spec travel together. And log which defect each check found at what rate, because the rate trend is often more informative than the value.

## What the audit cannot see

Everything in the table above is data that arrived but was wrong. The next lesson is about data that never arrived. No check on the received export can detect a customer who was never recorded, which is why the audit is necessary and nowhere near sufficient.

## Check your understanding

1. Add a defect not in the table (for example, a purchase whose value is negative or zero). Write the check and say how you would confirm it is not a false alarm.
2. Why is it dangerous to fix an unknown event name by silently mapping it to a known one in the pipeline?
3. A release raises duplicate purchases from 4% to 9% of purchase events. What would you want to know before reverting the release?
