# Lesson 1. The model: carry-over, saturation and controls

## Two ideas that make advertising different from a price change

**Carry-over.** An advertisement does not act only in the week it is bought. Someone sees a television spot on Monday and buys on Saturday; a campaign that stops leaves an afterglow that fades. The standard device is *adstock*: each week's effective exposure is that week's spend plus a fraction of last week's effective exposure,

```
a(t) = x(t) + decay × a(t−1)
```

A decay of 0.6 means 60% of last week's exposure still counts this week. Television usually carries over for weeks; a search click barely at all. In the simulated world, TV has a true decay of 0.60, social 0.30, search 0.10.

**Diminishing returns.** The hundredth thousand spent on a channel does less than the first. A saturating curve captures this:

```
s(t) = 1 − exp(−a(t) / K)
```

which climbs steeply from zero and flattens towards one; K sets how much exposure it takes to get most of the way. Sales then respond to `beta × s(t)`, where `beta` is the most the channel can add.

## The full model

```
sales(t) = intercept + trend + seasonality + Σ_c beta_c × s_c(t) + noise
```

The first three terms are *controls*: they absorb everything that moves sales regardless of marketing. They are not decoration. Lesson 2 shows that leaving them out can multiply a channel's apparent return by almost five.

## Fitting

`mmm.fit` separates the problem into two parts. For any candidate set of nonlinear parameters (a decay and a K for each channel) the remaining coefficients are linear, and they can be solved exactly by least squares. So the optimiser only searches over six numbers, and for each guess the rest is solved on the spot. Channel coefficients are held non-negative: advertising is not allowed to reduce sales, and a negative fitted coefficient is a symptom of collinearity rather than a finding.

The last 13 weeks are held out and used only to judge predictions.

## What it recovers

| Channel | True decay / K | Fitted decay / K |
|---|---|---|
| TV | 0.60 / 1,100 | 0.59 / 1,222 |
| Social | 0.30 / 700 | 0.44 / 680 |
| Search | 0.10 / 450 | 0.45 / 763 |

Out-of-sample error on the held-out weeks is 3.2% (mean absolute percentage error), and residuals are about the size of the true noise. By any ordinary standard the model is excellent.

Look at the table again. TV's parameters are recovered closely. Search's decay is estimated at 0.45 against a truth of 0.10, and social's at 0.44 against 0.30. A model that predicts sales this well has the carry-over of two of three channels substantially wrong. That is the subject of the next lesson. For now note only what it implies: **prediction quality does not tell you whether the pieces inside the model are right.**

## What MMM is for

- **Channels you cannot track at user level**: television, radio, outdoor, sponsorships.
- **Privacy-constrained measurement**: it uses aggregates, so it survives the loss of cookies and identifiers.
- **Budget allocation across channels** over months and quarters, which is a different timescale from campaign optimisation.
- **Triangulation** against attribution (Module 4) and experiments (Module 5).

## What it needs

- Long history: two to three years of weekly data is a common floor, since seasonality has to be separated from marketing and you need several cycles to see it.
- **Variation in spend.** A channel run at a constant level every week cannot be distinguished from the baseline. Channels with little variation have wide uncertainty by construction.
- Honest controls: price changes, promotions, distribution changes, competitors, macro conditions. Omitted drivers get absorbed by whichever channel they happen to correlate with.
- A fixed, documented specification. A model re-tuned until the answers look right is storytelling with arithmetic.

## Check your understanding

1. Explain, with a numerical example, why a channel with a decay of 0.8 and a spend of 100 a week has an effective steady-state exposure of 500, not 100.
2. Why does the model need K to be estimated rather than fixed? What goes wrong if K is set too large?
3. A colleague proposes dropping the trend control "because sales look flat." What would you check first?
