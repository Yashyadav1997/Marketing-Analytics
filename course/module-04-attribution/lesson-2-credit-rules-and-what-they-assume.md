# Lesson 2. Credit rules and what they assume

An attribution model is a rule for dividing one sale among the touches that preceded it. Each rule embeds a theory of how marketing works, usually unstated.

| Rule | Theory it embeds |
|---|---|
| Last-click | The final nudge is what matters; earlier exposure is decoration |
| First-click | Introducing the brand is what matters; later touches merely collect |
| Linear | Every touch contributes equally |
| Position-based (40/20/40) | Opening and closing carry weight; the middle is supporting |
| Platform (any touch) | Whatever I touched, I caused |

None of these is derived from evidence about causation. They are conventions, chosen for convenience and stability, which is a perfectly reasonable thing for a convention to be. The trouble starts when a convention is read as a finding.

## What the simulation shows

The same 3,440 touched orders, divided five ways, then compared with the true incremental orders:

| Channel | Last-click | First-click | Linear | Position | Platform | TRUE incremental |
|---|---|---|---|---|---|---|
| Influencer | 109 | 325 | 205 | 211 | 377 | 121 |
| Paid social | 586 | 1,439 | 966 | 985 | 1,566 | 532 |
| Generic search | 235 | 297 | 290 | 278 | 551 | 102 |
| Email | 763 | 857 | 913 | 870 | 1,656 | 198 |
| Brand search | 1,747 | 522 | 1,065 | 1,095 | 1,857 | 76 |

And as return on spend (revenue-based):

| Channel | Last-click | First-click | Position | Platform | TRUE |
|---|---|---|---|---|---|
| Influencer | 0.24 | 0.73 | 0.47 | 0.84 | 0.27 |
| Paid social | 1.73 | 4.26 | 2.91 | 4.63 | 1.57 |
| Generic search | 0.74 | 0.94 | 0.88 | 1.74 | 0.32 |
| Email | 37.99 | 42.68 | 43.31 | 82.46 | 9.86 |
| Brand search | 13.96 | 4.17 | 8.75 | 14.84 | 0.61 |

Read across the rows rather than down the columns.

**Brand search** is the cleanest case. Last-click credits it with 1,747 orders, a return of nearly 14; the truth is 76 orders and 0.61. Why? People search a brand's name because they already intend to buy, and 60% of high-intent users in this world did so. The channel sits at the end of nearly every journey because that is where intent ends up, so last-click hands it the credit. Cut the spend and most of those customers simply type the name and click the organic result.

**Paid social** is the mirror. It starts journeys. First-click credits it with 1,439 orders and a return of 4.26, nearly three times the truth, since it appears first in many journeys that would have continued without it. Last-click is closer to the truth for social (1.73 against 1.57) almost by luck, because the errors partly cancel.

**Email** shows that a good ROAS can be wrong in magnitude yet right in direction. Every model rates it far above the rest, and the truth agrees it is the best channel, but at 9.86 rather than 38. Cheap channels have enormous ROAS under any rule because the denominator is tiny; what matters is whether the *incremental* orders are worth more than they cost, and for email they clearly are.

**Platform self-reporting** overstates every channel. That is its design: it counts presence.

## Why no credit rule can be right

The pattern above is not an accident of these five rules; it follows from what they use as input. Each rule is a function of *journey position*: who came first, who came last, how many touched. The causal contribution of a channel depends on something else entirely, namely how likely the customer was to buy anyway and how much the channel changed that probability. Two customers with identical journeys can have very different counterfactuals. A rule that sees only the journey cannot tell them apart.

This is selection at work. Channels do not reach a random sample of people. They reach people chosen by targeting, by intent, by prior relationship. When the people a channel reaches are the people most likely to buy, the channel's correlation with sales will far exceed its effect on sales, and any rule that credits presence will pass that correlation on as if it were effect.

## Data-driven models

Commercial tools offer "data-driven" attribution, using Shapley values or Markov removal effects. These are fairer ways to *divide* credit, since they consider what happens when a channel is absent from observed journeys. But they work with observed journeys, and the people who skip a channel in observed data are not a random sample either. They still inherit the selection problem, only less visibly. Exercise 2 has you implement one and score it against the truth; the lesson is better learned by doing than by assertion.

## Non-additivity

One more complication, apparent in the bottom line of the report. Summing the per-channel true incremental orders gives 1,029, but only 1,012 orders disappear if every channel is switched off together. Where two channels could each have "saved" the same order, each gets counted as essential, yet removing both removes it once. Marginal contributions do not add up to the total. A tidy table in which channel contributions sum to 100% is therefore always a modelling convention, never a discovery.

## Check your understanding

1. Using the tables above, which rule gives the *best* ROAS ranking of channels relative to the truth? Which gives the worst? Is the best one trustworthy?
2. Suppose brand search were switched off and the brand lost only 76 orders. What would you expect to see in organic search traffic and in total sales, and why might you fail to notice it in a platform report?
3. Explain in one paragraph why last-click would perform *better* in a world where channels reached customers at random.
