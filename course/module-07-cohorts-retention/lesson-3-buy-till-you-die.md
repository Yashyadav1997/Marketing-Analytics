# Lesson 3. Buy till you die

## The problem a table cannot solve

In a subscription business, churn is visible: the customer cancels. In a retail business it is not. A customer who last bought ten weeks ago is either gone or between purchases, and nothing in the data distinguishes the two. Yet decisions hang on it. Who gets a win-back offer? Who is already lost? How many orders should next quarter's forecast contain?

The family of "buy till you die" models addresses this by writing down a plausible story of customer behaviour and letting the data choose its parameters. The BG/NBD model (Fader, Hardie and Lee, 2005) tells a particularly economical one.

## The story

- While a customer is active, purchases arrive at random at a steady rate λ.
- After each repeat purchase, the customer becomes permanently inactive with probability p.
- Customers differ. Purchase rates λ vary across the population as a Gamma distribution (parameters r and α); dropout probabilities p vary as a Beta distribution (parameters a and b).

Four numbers describe the whole population. Two things make the model attractive: it is simple enough to fit with a few lines of code, and it needs only three facts per customer, namely how many repeat purchases they made (x), when the last one happened (t_x), and how long they have been observed (T). Individual order dates are not needed.

## What the fit says

`bgnbd.fit` maximises the likelihood over the 2,500 simulated customers and returns r = 0.600, α = 11.9, a = 0.66, b = 2.41. The data was generated with r = 0.6, α = 12, a = 0.7, b = 2.5, so the method has recovered the truth to within a few percent. In words:

- Mean purchase rate r/α is 0.05 per week, but the Gamma shape of 0.6 (below one) means heterogeneity is large: a lot of slow buyers and a thin tail of frequent ones.
- Mean dropout probability a/(a+b) is about 0.21 per repeat purchase, with wide spread between customers.

## Probability alive

The most practically useful output is `p_alive(x, t_x, T)`. Three patterns are worth seeing for yourself in the function:

- A customer with several purchases who bought recently is almost certainly alive.
- The same customer, silent for a long stretch, becomes less likely to be alive, and the more purchases they had made at a quick pace, the faster the probability falls, because a long silence is more surprising from a frequent buyer.
- A customer with no repeat purchases is assigned probability one in this model. That is a property of the model (dropout is only possible after a repeat purchase), not a discovery about customers, and it is a limitation worth noting. One-time buyers are often the biggest group, and a model that cannot call them lost is flattering them.

Averaged across the base, the model puts the active share at 83.9% at the calibration cutoff. The simulation's ground truth is 84.4%. Individually the probabilities are uncertain; collectively they are well calibrated here.

## Forecasting, and the holdout test

`expected_purchases` gives the expected number of repeat orders over a future horizon, customer by customer. Summed over all customers for the 26-week holdout, the model predicts 1,888 orders. The holdout contains 1,910. That is an error of about one percent on a quantity the model never saw.

This is the test that matters. A model that fits the past tells you little; a model that forecasts a held-out period within tolerance has earned some trust. Always hold out time, not random customers, because the future is what you will use it for.

## Why the success is not the lesson

The data was produced by the model. Recovery under its own assumptions is a check that the *code* is correct, not evidence that the *model* describes real customers. Real behaviour violates the assumptions in ways that matter:

- **Stationary purchase rates.** Real rates swing with seasons, promotions, price changes and product launches.
- **Dropout only after purchases, and permanent.** Real customers lapse gradually, and many return after long gaps.
- **Independence of rate and dropout.** Heavy buyers may well be more loyal, or the reverse.
- **Homogeneous environment.** Channels, products and discounts are ignored, though they plainly change behaviour.

Exercise 4 adds a festive promotion to the simulator and measures how far the forecast drifts. Practitioners handle this with covariates, with separate fits per segment or acquisition channel, or by treating the model's output as a baseline against which promotional uplift is measured.

## Where the model earns its keep

- **Customer base valuation.** Expected future orders summed over active customers, multiplied by margin, is a defensible basis for estimating the value of the existing base.
- **Targeting.** Win-back effort belongs among customers whose probability alive is middling and falling, not among the clearly active (who would have bought anyway) nor the clearly lost.
- **Early warning.** A fall in the base-wide average probability alive precedes a fall in revenue.
- **Cleaner LTV.** Module 8 combines expected purchases with a spend model to give a customer-level LTV that replaces the four-averages formula from Module 1.

## Check your understanding

1. Why is a customer with x = 6 and t_x = 20, T = 52 less likely to be alive than one with x = 2, t_x = 20, T = 52? Check with `p_alive`.
2. The model assigns P(alive) = 1 to every customer with no repeat purchase. Propose a way to handle first-time buyers who have not returned.
3. If your forecast for a holdout period is accurate in total but poor by customer, is it still useful? For what and for what not?
