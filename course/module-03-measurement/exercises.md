# Exercises

## Exercise 1. Write the spec you wish you had (60 min)

a. Add a `refund` event to `spec.py` with required parameters (a transaction id linking to the purchase, a value, a reason code). Add the KPIs that depend on it (net revenue, refund rate).
b. Extend `simulate.py` to emit refunds for a share of purchases, with two injected defects of your choice. Extend `audit.py` to catch them and score the audit against your labels.
c. State how net revenue should be reconciled to the ledger once refunds exist, and which row of the waterfall they affect.

## Exercise 2. Find a defect nobody labelled (75 min)

Add a defect to the simulator without telling the audit: for example, purchase values that are far too small (a currency subunit used by one app version), or `add_to_cart` events firing before any `view_item`.

a. Write a detector from exploration of the data alone: distributions, ratios, event sequences. Describe how you found it.
b. Why can this kind of discovery not be done by a spec-based audit? What does it need instead?

## Exercise 3. Move the consent rate (60 min)

Change `P_DECLINE_CONSENT` to 0.05, 0.18 and 0.35 and rerun `reconcile.py`.

a. Plot invisible loss against the consent decline rate and compare with the independence prediction 1 − (1 − decline)(1 − blocked).
b. Make declining people *more* likely to be high-value buyers (adjust the value distribution for them). What happens to the invisible share of *revenue* compared with the invisible share of *people*? What does that do to AOV measured in analytics?
c. Write two sentences for a CFO on how to read tracked revenue under each assumption.

## Exercise 4. Stitching (60 min)

Vary `P_LOGGED_IN` and `P_LOGIN_SESSION` and `P_SECOND_DEVICE`, and measure the device-count overstatement and the post-stitching overstatement with `identity.people_counts`.

a. Which parameter does most to reduce the residual overcount after stitching?
b. Suppose a product team can raise login rates by 10 points at a cost of friction. Using the repeat-buyer rate as the outcome, what is the measurement benefit, and how would you weigh it against the friction?

## Exercise 5. Reconciliation memo (60 min, 400 words)

The CMO has seen that analytics revenue is within 1% of finance's figure and concludes tracking is fine, so she wants to use analytics-based ROAS to cut a channel. Write the memo. Itemise why the agreement is not evidence, state what you would show instead, name the one extra check you would run first, and say what you would need to see before agreeing.

---

## Hints and reference points

**Exercise 1c.** Refunds reduce net revenue after the sale. Decide whether the ledger records them as a reduction in the period of the refund or of the original sale, and reconcile on the same basis.

**Exercise 3a.** At the shipped settings the independence prediction is 24.6% and the observed loss is 24.0%. Expect closer agreement with larger samples. **3b.** If non-consenters buy more per order, the invisible share of revenue rises above the invisible share of people, and tracked AOV understates true AOV.

**Exercise 4a.** The probability of logging in during a session and the probability of having an account both matter, and they combine: a device is only linked if at least one of its sessions was logged in. Report your measured sensitivities.

**Exercise 5.** Strong answers separate the three claims bundled in "within 1%": the total agrees, the components do not, and the agreement is a coincidence of offsetting errors. The extra check is an itemised reconciliation (a waterfall) on a different month.
