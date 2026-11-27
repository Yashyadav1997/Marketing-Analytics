# Lesson 4. Pricing from the client's P&L

Everything so far has been about a brand's own marketing. This lesson turns the same logic on a service provider, and it is shorter because the idea is simple and the discipline is in applying it.

The usual ways to price marketing or analytics work are all about the provider: what experience is worth, how many hours it will take, what competitors charge. There is a fourth route that starts from the buyer. Ask what the client's business can bear, and what your work has to achieve for the fee to be justified.

## The break-even on a fee

If you charge a monthly fee, the client needs to earn it back from the margin on whatever extra revenue you create. So:

```
required incremental revenue = monthly fee ÷ incremental contribution margin
```

A fee of Rs 2,00,000 against a 20% incremental contribution margin means the engagement must add about Rs 10,00,000 of monthly revenue merely to pay for itself. That is the same arithmetic as break-even ROAS with the fee playing the part of ad spend, and it is worth saying to a prospective client in exactly those terms. (`unit_economics.required_incremental_revenue` implements it.)

## A worked illustration, with its assumptions in plain view

Take a brand doing Rs 1 crore a month in net revenue and assume, as one illustrative set of working figures, that it spends about 20% of revenue on marketing, that roughly 65% of that goes to paid media, and that a further 5 to 10% of the marketing budget could reasonably go to strategic expertise.

- Marketing budget: Rs 20 lakh a month.
- Paid media at 65%: Rs 13 lakh. The remaining Rs 7 lakh is already spoken for by creative, agencies, tools and staff.
- Strategic expertise at 5 to 10% of the budget: Rs 1 to 2 lakh.

So a Rs 2 lakh fee sits at the top of what that budget structure would plausibly absorb, and to justify it the engagement has to lift monthly revenue by about Rs 10 lakh, a 10% increase on the base, assuming a 20% incremental contribution margin. Whether that is realistic depends on how much headroom the brand has. For a brand with weak conversion and poor retention, perhaps. For a mature brand already near its efficient frontier, probably not.

Treat every percentage there as a placeholder. These are working assumptions, the kind a practitioner uses to decide whether a prospect is worth pursuing before writing a proposal, and the right ones vary with category, margin, growth stage and the repeat rate. The value of the exercise is that it forces you to find the real numbers.

## Three ways to reshape a deal that does not clear

When the arithmetic says the fee is too high for the client's economics, there are three honest moves and one tempting one that should be avoided.

1. **Narrow the scope.** A smaller engagement at a lower fee, with the same quality of work on fewer things.
2. **Link part of the fee to results.** A fixed base plus a performance component aligns incentives, provided the measurement of the result is agreed in advance and is hard to dispute (this is where Module 5's incrementality thinking pays for itself).
3. **Create value by cutting cost.** Sometimes the biggest return is stopping spend that does nothing, which raises contribution margin and makes the arithmetic easier.

The one to avoid is offering the same scope at a lower price. It teaches the client that the original price was negotiable and leaves you doing the same work for less.

## Why this belongs in an analytics course

It is the clearest small example of the course's central habit: do not accept a number (a fee, a ROAS, a CAC) until you have placed it against the economics that make it meaningful. The same reasoning prices an internal analytics team. A team costing Rs 40 lakh a year needs to change decisions worth enough, at the margin the business earns, to repay that. Few analytics functions have ever stated that bar out loud, and the ones that do tend to survive budget season.

## Check your understanding

1. Recompute the illustration for a brand with Rs 50 lakh monthly revenue and a 35% contribution margin. What fee range does the structure support and what lift would it require?
2. Where in this calculation would you most want better data, and how would you get it?
3. Design a fixed-plus-performance structure for a Rs 1.5 lakh monthly fee. What would you measure, over what window, and how would you stop the dispute you can already imagine?
