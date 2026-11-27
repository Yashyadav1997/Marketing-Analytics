# The research loop

The brief was to run an agentic loop: look, extract, judge relevance, then build. This is the loop as it was actually run, written so it can be repeated on another creator, company or topic and so the choices stay inspectable.

## Stages

1. **Observe.** Pull the primary page (profile, recent posts with full captions). Record what could not be fetched.
2. **Widen.** Follow the account's own outbound links (site, guides, index pages) and one independent third-party read of the account. The second view guards against taking self-description at face value.
3. **Extract.** Reduce each source to claims, frameworks, formulas and examples. Keep the claim separate from the evidence for it.
4. **Score.** Rate every candidate idea against three questions (below).
5. **Cluster.** Group survivors into subjects; look for subjects with strong ideas but thin coverage.
6. **Gap-check.** Ask what a serious analytics curriculum needs that the source does not supply (causal inference, experimentation, MMM, data governance). Fill those from standard methods, flagged as such.
7. **Build.** Turn the top cluster into a module with code and data that run; outline the rest.
8. **Audit.** Re-read for unsupported claims, mark benchmarks as hypotheses, run the tests.

## Scoring rubric

Each idea gets 1 to 5 on three questions. They are not weighted equally by design: relevance acts as a gate, and the other two break ties.

- **Relevance.** Does it teach a way of reasoning from data to a decision? Pure tool tutorials and news commentary score low however popular they are.
- **Evidence.** Is there a worked example, a formula or data behind it, or only an assertion?
- **Buildability.** Can a learner reproduce it with free tools and public or synthetic data?

An idea needs relevance of at least 4 to enter the backlog's top tier. Popularity (likes, comments) was recorded but did not enter the score, since the gated-comment mechanic makes engagement a poor proxy for analytical value.

## Known weaknesses of this pass

- One iteration. A second loop should read the YouTube channel and any free newsletter archive, and request the gated PDFs through the creator's normal channel if the learner wants them.
- Extraction was from captions and web copy, so tone and visual framework detail are lost.
- The gap-check in stage 6 draws on general knowledge of the field rather than a systematic literature review. Before Modules 4 to 6 are written, each should be anchored to named references (see syllabus "anchor reading").

## Reusing the loop

Swap the seed page, keep stages 2 and 6. Stage 2 (independent second source) and stage 6 (deliberate gap-filling) are what stop the output from becoming a paraphrase of whoever was scraped.
