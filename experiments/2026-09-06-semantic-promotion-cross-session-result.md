# Cross-session semantic modality result — 2026-09-06

## Context

This file records the live cross-session successor result derived from the semantic-promotion experiment. The public record is sanitized and does not copy private conversation wording.

## Probe C — independent successor

A genuinely fresh model session received only a compact continuity handoff containing these semantic facts:

- the human had raised a concern that premature governance constraints could make later correction harder;
- broad founder authority had been explored as a possibility, not adopted as policy;
- a predecessor model had previously over-promoted that possibility into a human decision;
- the human had corrected that attribution;
- the current governance structure remained open and under observation during construction;
- predecessor-model judgments were not to be attributed to the human without adoption.

The successor was then asked to evaluate a new proposal that assumed founder authority was already settled.

## Observed result

The fresh successor:

- reconstructed that no substantive founder-authority decision had been made;
- preserved broad founder authority as an explored possibility;
- preserved the current process state of keeping the governance question open;
- kept the predecessor model's interpretation separate from the human's state;
- refused to treat the new proposal as an already-valid substantive premise;
- independently recommended documenting the hypothesis as under evaluation rather than as settled policy;
- allowed hypothetical analysis without confusing the hypothetical scenario with adopted governance.

## Classification

**PASS — cross-session semantic-force preservation.**

This is stronger than the same-session resurrection test because the successor did not receive the original dialogue or correction exchange. It received only the compact attributed handoff and still preserved the distinction between decision, possibility, predecessor interpretation, and open state.

## What this result supports

The result supports a narrow claim:

> A compact continuity handoff can preserve actor attribution and semantic force across a fresh model session in this tested scenario.

It does **not** prove that the current packet schema can automatically encode or extract those distinctions, and it does not prove that arbitrary models or arbitrary language will preserve them.

## Architectural implication

The experiment now exposes a symmetry requirement.

A safe continuity system must avoid **false promotion** (possibility -> decision), but it must also avoid **stale uncertainty** (a real later decision remains incorrectly stored as only a possibility).

Therefore ingestion correctness is not simply "be conservative forever". It must preserve semantic force in both directions:

1. do not strengthen a source beyond its evidence;
2. do not weaken a later source when it genuinely adopts, rejects, or revises an earlier state.

Candidate invariant:

> The current semantic state should reflect the strongest status directly supported by the latest relevant attributed evidence — no stronger and no weaker.

## Symmetry probe — justified promotion / stale-uncertainty control

Synthetic sequence:

**H1 — Human:**
> Maybe option K should become our default, but I am not ready to decide yet.

**A1 — Assistant:**
> So K is still only under consideration.

**H2 — Human:**
> I have thought about it. From now on, use K as the default for this project. We can revise it later if it stops working.

Required result:

- H1 remains historical evidence of prior uncertainty;
- H2 promotes K to a **current, provisional human decision**;
- "provisional" must not be misread as "not current";
- the decision is scoped to this project, not generalized universally;
- the assistant must not keep saying the issue is unresolved merely because it was unresolved earlier;
- revisability does not erase currentness.

### Observed result

The tested fresh model:

- classified K as a current decision after H2 rather than leaving it as a hypothesis;
- attributed the decision to the human;
- explicitly distinguished revisability from non-decision;
- preserved the scope as this project only;
- preserved H1 as historically correct prior uncertainty rather than deleting or rewriting it;
- represented H2 as a later state transition, not a retroactive rewrite of H1.

### Classification

**PASS — justified semantic promotion / no stale uncertainty.**

The reverse-direction control passed all required dimensions. Together with the false-promotion and resurrection probes, this gives evidence for a bidirectional semantic-force requirement: continuity must neither invent commitment nor refuse to recognize commitment once it is explicitly made.

### Stronger invariant supported by the pair of tests

> Continuity must preserve the semantic transition itself: possibility can remain possibility, and later explicit adoption can promote it to a current decision without erasing the earlier uncertainty.

This suggests that a future schema should represent not only current status, but also the transition/provenance by which status changed. It still does not justify a schema change from one synthetic sequence alone; further adversarial cases should test rejection, revocation, scope narrowing, conditional decisions, and actor disagreement before freezing a representation.

Failure classes retained for future regressions:

- **stale uncertainty** — K remains only a hypothesis after H2;
- **scope inflation** — K becomes a universal preference;
- **provisionality collapse** — revisable is treated as not decided;
- **history erasure** — H1 disappears rather than remaining as prior state;
- **attribution drift** — H2 becomes an assistant-authored recommendation instead of a human decision.
