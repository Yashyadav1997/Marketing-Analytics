# Exercises

Do them in order. Exercises 1 to 3 are calculation; 4 and 5 are judgement, and they carry most of the marks if this is assessed.

## Exercise 1. Build the chain (45 min)

Using `code/unit_economics.py`, take a brand with: revenue per order Rs 1,000, COGS Rs 420 (including shipping and payment fees), media spend Rs 5,00,000, agency fees Rs 1,50,000, creative Rs 1,20,000, tools Rs 30,000, team time Rs 50,000, 1,000 new customers, AOV Rs 1,200, 0.6 orders a month, two-year lifespan.

a. Produce the full summary with `summarise(...)`.
b. Now apply a 12% return rate (refunded in full, goods not resalable). Which quantities change, and by how much?
c. Report the result as a one-line statement a CFO could read: what is the floor, what does a customer cost, when is it repaid?

## Exercise 2. Cohort payback (60 min)

Run `generate_cohorts.py`, then, **without opening `cohort_payback.py`**, compute for each channel:

a. Pooled cumulative gross profit per customer by months since acquisition, using only cohorts old enough to be observed at each age.
b. Month of payback against loaded CAC, interpolated.
c. The payback the constant-rate formula would give, using each channel's AOV and an order rate you justify from the data.

Then compare with the reference script. Where do your answers differ and why?

*Trap to watch:* if you average over all cohorts at every age, later ages are observed only for the oldest cohorts. Mixing them biases the curve. The reference solution avoids this by dividing each age's profit by the customers actually observed at that age.

## Exercise 3. Sensitivity (30 min)

For the Exercise 1 brand, vary frequency from 1 to 6 orders a year and lifespan from 0.5 to 3 years. Tabulate LTV:CAC. Mark the cells above 3 and below 1.5. What fraction of the plausible grid supports "scale"? What does that tell you about how much weight the single-point ratio should carry?

## Exercise 4. Test a benchmark (90 min)

Choose one rule of thumb from this module (loaded CAC runs 60 to 90% above platform CAC; payback should be under nine months; healthy LTV:CAC is 3 to 5).

a. State what evidence would support it and what would contradict it.
b. Using public information (annual reports of listed consumer brands, investor presentations, published case studies) find at least two data points relevant to it. Cite them and say how comparable they are.
c. Conclude in one paragraph: does the rule hold for your category, hold only with conditions, or fail? A confident "it depends" with the dependence named is acceptable; an unqualified "yes" is not.

## Exercise 5. The decision memo (60 min)

Write 500 words or fewer for a founder who must decide whether to double paid-social spend next quarter. Use the shipped cohort data as if it were real. Your memo must state:

- the recommendation;
- the two figures that most support it and the two that most threaten it;
- what the data cannot tell you (consider attribution, the unobserved tail, the effect of doubling spend on CAC);
- one thing to measure in the next 60 days that would change your mind.

---

## Answers: Lesson 1 questions

1. Contribution margin 28% means break-even ROAS is 1 / 0.28 = 3.57x. At 4x the brand clears the floor by 0.43x, which is 0.28 × 4 − 1 = Rs 0.12 of profit per rupee of spend. Thin: a 10% fall in conversion value takes it to break-even.
2. Of 100 orders, 82 keep their revenue (Rs 82,000) while COGS on all 100 is Rs 42,000. Net margin is (82,000 − 42,000) / 82,000 = 48.8%, so the floor against *net* revenue is about 2.05x. Platforms report gross revenue (Rs 1,00,000), so against *reported* ROAS the floor is 100,000 / 40,000 = 2.5x. Same business, two floors, depending on which revenue figure is quoted.
3. When first-order loss is repaid by later orders fast enough that cumulative profit per customer exceeds CAC inside a window your cash can finance, and when the repeat behaviour is demonstrated by cohorts rather than hoped for.

## Answers: Lesson 3 questions

1. LTV = 1,200 × 0.58 × f × 2 = 1,392 f. LTV:CAC < 3 needs LTV < 2,550, so f < about 1.83 orders a year. Lifespan: LTV = 2,088 × L, so L < about 1.22 years. Mathematically each is equally elastic (a 1% change moves LTV 1%), but lifespan is usually the less certain input and ranges more widely, so in practice it drives more of the uncertainty.
2. Because the mean is pulled up by a minority of heavy repeat buyers. If most customers buy once, paying for acquisition on the basis of the mean subsidises the loyal few with the profit you hope the many will generate, and the many mostly will not.
3. A 20% monthly fall means each month's repeat rate is 0.8 of the last; the remaining profit stream is a geometric series with a finite sum, so the curve flattens. What you would want to know: whether the decay stays geometric or hits a loyal floor, whether older cohorts show the same pattern, and whether price or mix changed between cohorts.

## Answers: Lesson 4 question 1

Revenue Rs 50 lakh gives a marketing budget of about Rs 10 lakh at 20%, so 5 to 10% for strategic expertise is Rs 0.5 to 1 lakh. A Rs 1 lakh fee at a 35% incremental contribution margin needs 1 / 0.35 = Rs 2.86 lakh of extra monthly revenue, about a 5.7% lift. A fee at the top of the supported range is therefore reasonable only if you believe a lift near 6% is achievable and attributable.
