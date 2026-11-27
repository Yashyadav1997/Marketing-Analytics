# Lesson 1. Why the numbers disagree

Run `python3 attribution.py` and look at the first line: 50,000 users, 3,956 orders, 516 of them with no tracked touch from any channel. Then look at the credited-orders table. The "platform (any touch)" column sums to 6,007. The business made 3,956 sales.

Nothing is broken. Each platform is reporting, faithfully by its own rule, the number of orders where it had a touch. A customer who saw social, clicked an email and searched the brand name is counted three times, once by each system, because no platform can see the others. The sum of what channels claim is not the total of what happened; it is a measure of how much the channels overlap.

## Four distinct sources of disagreement

It helps to separate causes that are usually bundled together.

**Counting rules.** Who gets credit when several channels touched the customer? Last touch, first touch, all of them? Different rules give different answers on identical data. This is the part most discussed and, in a sense, the least troubling, since it is at least visible.

**Visibility.** Each source sees a slice. The platform sees its own impressions and clicks but not your email. The analytics tool sees sessions but loses users who decline tracking or switch devices. Here, 516 of 3,956 orders (13%) carry no tracked touch at all. They are not "organic"; they are unattributed, which is a different thing, and many of them will have been influenced by something unseen.

**Windows and definitions.** A 7-day click window versus a 1-day view window, a conversion that counts at checkout versus at payment, returns netted or not. Small settings, large differences.

**Causation.** The deepest one, and the one no counting rule addresses. Credit says who was present near the sale. It does not say whose absence would have cost the sale. A channel can be present at almost every purchase and responsible for almost none.

## Blended numbers are honest but blunt

Marketing efficiency ratio (MER) divides total revenue by total marketing spend and needs no attribution at all. In this world it is 3.17. That reads as healthy. But the true incremental return of the entire programme, measured by switching off every channel jointly, is 0.81: of the 3,956 orders, 1,012 (25.6%) would not have happened without marketing. The rest were going to happen anyway.

MER is reliable as an accounting fact and uninformative as a causal one, because it credits marketing with every sale. A business with a loyal base and a large brand will show an excellent MER even if its advertising is accomplishing nothing. This is why MER works well for *trends* (is efficiency drifting?) and poorly for *levels* (is this spend worthwhile?).

## The first habit

Before debating which model is right, build the reconciliation table: platform-claimed, analytics-tool, ledger, unattributed. Write down, for each gap, which of the four causes explains it. A team that can say "the 2,051 order gap between platform claims and the ledger is overlap, and the 516 unattributed orders are untracked sessions" has done more for its credibility than one that picks the number it likes best.

## Check your understanding

1. In the report, platform claims total 6,007 against 3,440 orders that had at least one touch. What does the ratio of 1.75 tell you about the overlap structure of this business?
2. Why can MER rise while true incremental efficiency falls? Construct a scenario.
3. A colleague says unattributed orders "must be organic." What would you want to know before agreeing?
