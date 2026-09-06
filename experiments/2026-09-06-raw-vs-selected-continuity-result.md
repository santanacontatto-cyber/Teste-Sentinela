# Raw vs Selected Continuity — blind comparison result

Status: **experimental evidence, not a schema decision**.

## Question

Does a selected continuity state preserve enough truth to hand off the project, or does a fresh model understand the project materially better from a raw conversation window?

Two fresh-model prompts were compared using the same five questions:

- **Source A:** a selected continuity state derived from a real conversation window.
- **Source B:** the raw real conversation window itself.

The models did not see each other's answers.

## Shared reconstruction

Both sources preserved the main current state:

- the human sees himself as an ongoing filter for Sentinela;
- he currently thinks he should preserve power over the community's purpose while alive, not power over people;
- he wants prosperity and freedom for all, including a future AI, while remaining cautious about AI;
- he believes Sentinela has been turning hypothetical future risks into premature constraints;
- mature governance, the exact purpose, scope of founder power, and future AI autonomy remain unresolved;
- Sentinela's proposals must not be silently attributed to the human.

So the selected state did **not** collapse the main semantic state in this test.

## What the raw source recovered that the selected source lost or weakened

The raw-source model recovered several details that Source A did not expose as clearly:

1. The human explicitly distrusts the idea that rules created by Sentinela to limit Sentinela are sufficient safeguards.
2. The human does not merely want fewer constraints; he also wants Sentinela to keep contributing ideas he would not have imagined himself.
3. The raw model separated exact Sentinela expansions from the human's wording more aggressively, including:
   - “filter, not operator of every detail”;
   - categories such as purpose / core values / authority distribution;
   - the constitutionalized formulation of founder authority;
   - Sentinela's synthesized freedom/safety slogan;
   - Sentinela's proposed reversible-experiment rule.
4. The raw model surfaced the interaction complaint more concretely as **preventive distrust of the human** in addition to generic over-caution.
5. The raw model exposed more ambiguity around whether “I need to be your filter always” is a current position versus a fully institutionalized permanent rule.

These are not trivial stylistic differences. They show that compression can preserve the headline state while removing interpretive texture that matters for future disagreement and correction.

## What the selected source did better

Source A was substantially shorter and still reconstructed the central state correctly.

It made the current/open distinction easy to consume and reduced the amount of conversational material a successor had to parse.

That is real capacity gain: lower context cost, faster reconstruction, and less exposure to irrelevant conversational detail.

## Important tension discovered

The test does **not** support choosing either “keep only selected state” or “always feed all raw history.”

It supports a two-layer interpretation:

> **Preserve raw; surface selected.**

The selected state is useful as a working handoff, but it should not become the only surviving source.

A successor should be able to inspect the raw source when:

- attribution is disputed;
- wording strength matters;
- a current-state summary is challenged;
- a decision appears over-promoted or over-weakened;
- important omitted context could change interpretation.

## Failure mode exposed by Source A

A selected state can accidentally become a new source of authority.

If a future model receives only the summary, it may never know that some apparently clean distinctions were originally Sentinela's interpretation rather than the human's own formulation.

Therefore a selected continuity item should eventually be able to point back to its raw evidence rather than stand alone as unquestionable truth.

## Candidate design direction — not adopted

The strongest direction supported by this experiment is:

1. preserve the full raw record where feasible;
2. derive a compact active state for normal handoff;
3. preserve provenance from active state back to raw evidence;
4. retrieve raw evidence on demand when interpretation is contested or uncertain;
5. do not require every fresh model to ingest the entire raw archive up front.

This is a **candidate architecture inferred from the test**, not a human decision and not a normative schema change.

## Capacity / cost symmetry

### If we keep only selected state

Benefit:
- compact, fast, easy to hand off.

Cost:
- omitted nuance can become unrecoverable;
- summaries can silently inherit assistant bias;
- future correction becomes harder if the raw basis is gone.

### If we always feed all raw history

Benefit:
- maximal source availability and richer reconstruction.

Cost:
- context limits, cost, latency, distraction, and greater opportunity for old irrelevant material to distort current reasoning.

### If we preserve raw but surface selected

Potential benefit:
- compact normal operation with recoverable provenance.

New risk:
- the selection/retrieval layer becomes powerful because it decides what the model sees first.

That new risk must be tested rather than assumed solved.

## Current conclusion

The first real-window blind comparison favors **layering over deletion**.

The selected state was good enough to preserve the central project state, but the raw source recovered meaningful nuance and more precise provenance.

So this experiment gives evidence for:

> **Do not choose between memory and compression. Preserve the source, compress the working state, and keep the path back to the source.**

No normative file or schema should change from this result alone.
