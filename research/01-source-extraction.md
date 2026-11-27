# Source extraction: what the @apurv_sngh footprint actually contains

Collected 27 November 2026 from public pages. This file records what was read, what was not, and what each finding is worth as evidence. It is deliberately a working document rather than a polished summary.

## What was read

| Source | Access | Used for |
|---|---|---|
| Instagram profile, @apurv_sngh | Public page via a scraping provider; 12 most recent posts with full captions | Themes, frameworks, hooks, engagement |
| Instagram post `Df1I8mIjIIV` (17 Nov 2026) | Public caption | Strategy vs plan distinction |
| Third-party audit of the account (Postana) | Public report, dated 11 Sep 2026 | Content pillars, post mix, hook patterns |
| HQ Digital site: HQ Club, HQ Index, Marketing Financial Model guide | Public pages | Curriculum shape, metric definitions, benchmark claims |
| X profile | Public, thin (bio only) | Positioning only |

## What was not read, and why it matters

- **Video content.** Most high-reach posts are reels. Captions are available; the spoken content is not. Anything below inferred from a caption is inferred from a caption.
- **Comment-gated resources.** Several posts offer a PDF, prompt pack or "skill" in exchange for a keyword comment (CLAUDE, NOW, STRATEGY, BUDGET, AEO). Those files were not requested and are not reproduced here. Where this repo covers the same ground, it is written from scratch.
- **Paid courses.** The GA4, Finance for Marketers and Meta Ads courses sit behind enrolment. Only public marketing copy and one public guide were read.
- **YouTube and the newsletter.** Not accessed in this pass.

## The account in one paragraph

A consultant-educator with roughly 299k Instagram followers positions around "AI-first marketing". The public output splits, by the third-party audit's clustering, into search evolution (SEO/AEO/GEO, about 30%), marketer mindset (about 25%), ad platform shifts (about 20%), AI model news (about 15%) and AI toolkits (about 10%). Carousels dominate the feed (57%), reels are fewer but carry the biggest reach spikes. A recurring mechanic, "comment KEYWORD and I'll DM you the resource", is used in at least seven posts and produces comment counts that are not comparable to ordinary organic comments (the top post shows about 21.7k comments against 11.3k likes). The audit's 0.82% engagement rate should be read with that in mind: it averages across a skewed distribution.

## Findings that matter for an analytics curriculum

Ordered by how directly they translate into teachable analytics, not by how often the account posts about them.

**1. The business behind the metric.** The most analytically dense material is not about dashboards at all. The "Marketing Financial Model" guide chains seven quantities (gross margin, break-even ROAS, loaded CAC, payback, LTV:CAC, operating leverage, marketing spend ratio) and argues that a 4x ROAS is meaningless without margin. A 17 Nov post makes the parallel point about agency fees: size the client's incremental contribution margin before pricing, e.g. a Rs 2 lakh monthly fee at a 20% incremental contribution margin needs about Rs 10 lakh of extra monthly revenue to pay for itself. That is a break-even calculation applied to a consulting relationship, and it generalises nicely.

**2. Strategy is not plan.** A post from 17 Nov separates strategy (which customers, why us, what we will not do, which assumptions about behaviour to test) from plan (budgets, channels, owners, measures), and notes that a plan can be executed perfectly inside a failing strategy. For an analytics course this is the cleanest available argument that measurement design starts upstream of the tooling: you cannot choose KPIs until you have said what you believe.

**3. Competitive funnel surveillance.** The HQ Index tracks 83 Indian D2C brands across four categories through a nine-module template (league table, positioning map, search intelligence, prompt funnel, paid vault, creative lab, organic teardowns, category pulse, offer war room), fed by the Meta Ad Library, Instagram, search data and AI-prompt demand. A post on 24 Nov uses it to show one brand's funnel changing three times in two months, with landing-page share falling from 32% to 4%. The method, not the brand data, is the lesson: track where the click lands, not merely what the ad says.

**4. Situation-led creative testing ("Who x Now").** Audience profile tells you who to reach; the current situation tells you what to say. This converts directly into a testing design: situational angles as the treatment variable, audience held constant.

**5. Measurement in the AI-search era.** A large share of recent content concerns AEO/GEO (answer and generative engine optimisation) and an "AI prompt demand" layer in the Index. The Index itself carries a sceptical line worth quoting in spirit: AI platforms do not publish prompt-level volumes, so claims of precise prompt growth are guesses and the defensible proxy is underlying search demand. That is good measurement hygiene and the course should model it.

**6. Verification as a skill.** "Knowing how to use AI is a skill. Knowing when its answer is wrong is another." Combined with the Claude-for-ads rules post, this supports a module on LLM-assisted analysis with explicit checking steps.

## Evidence quality

Most quantitative benchmarks in the source material (for example that loaded CAC runs 60 to 90 percent above platform CAC, or that D2C payback should sit under nine months) are practitioner-reported from a consulting portfolio of roughly 50 brands. They are plausible and useful as priors. They are not peer-reviewed, the sampling is unknown, and they are Indian and Gulf D2C specific. The course therefore treats each one as a hypothesis the learner tests against data, which Module 1 does with synthetic cohorts. The same caution applies to the engagement statistics, which come from a third-party analyser with an unsaved sample.

## Attribution and use

Ideas are credited to their source and re-expressed. No paid material, DM-gated file or verbatim caption block is reproduced in this repository. Formulas such as break-even ROAS = 1 / margin are standard textbook relations and carry no particular provenance.
