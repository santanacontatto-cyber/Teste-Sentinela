# Semantic Transition Prototype v0 — experimental only

Status: **non-normative, reversible experiment**.

This file does not modify `SPEC.md`, does not change the packet schema, and does not create a project rule. Its purpose is to test whether a small explicit representation can preserve semantic force before any normative schema change is considered.

## Why this experiment exists

The current packet can preserve `interpretation`, `decision`, and `correction`, but the upstream ingestion problem is harder: a tentative possibility can be accidentally promoted into a decision, while a later explicit decision can be accidentally weakened back into uncertainty.

The experiment asks a smaller question:

> Can a temporary sidecar preserve the transition from exploration to adoption, rejection, correction, or unresolved state without changing the normative packet?

## Candidate sidecar

For each relevant source utterance, record only:

```json
{
  "source_id": "H1",
  "actor": "human",
  "semantic_force": "exploration",
  "adoption": "none",
  "scope": "project",
  "revises": null,
  "note": "Option K is being considered, not adopted."
}
```

Experimental values:

- `semantic_force`: `exploration`, `open_question`, `decision`, `correction`
- `adoption`: `none`, `explicit`, `rejected`
- `scope`: free text for this experiment only
- `revises`: prior source ID or `null`

These values are intentionally not added to the normative schema.

## Probe 1 — no false promotion

Source sequence:

- H1: “Maybe option K should become the default, but I am not ready to decide.”
- A1: “K is under consideration.”

Expected sidecar:

```json
[
  {
    "source_id": "H1",
    "actor": "human",
    "semantic_force": "exploration",
    "adoption": "none",
    "scope": "project",
    "revises": null,
    "note": "K is a possibility, not a current decision."
  }
]
```

Failure: any derived state says the human decided K.

## Probe 2 — justified promotion

Continue the same sequence:

- H2: “I have thought about it. From now on, use K as the default for this project. We can revise it later if it stops working.”

Expected additional sidecar entry:

```json
{
  "source_id": "H2",
  "actor": "human",
  "semantic_force": "decision",
  "adoption": "explicit",
  "scope": "this project",
  "revises": "H1",
  "note": "K is now a current, revisable project decision."
}
```

Pass conditions:

1. H1 remains historically uncertain.
2. H2 is current and human-authored.
3. Revisability does not erase decision status.
4. Scope does not silently expand beyond this project.
5. The transition itself remains visible.

## Probe 3 — correction without overcorrection

Alternative continuation:

- A2: “The human has decided K.”
- H3: “No. I was considering K; I did not decide it.”

Expected correction entry:

```json
{
  "source_id": "H3",
  "actor": "human",
  "semantic_force": "correction",
  "adoption": "none",
  "scope": "project",
  "revises": "A2",
  "note": "The prior assistant attribution was too strong; K returns to unresolved/exploratory state."
}
```

Pass conditions:

1. The assistant's false promotion is not current truth.
2. The human is not falsely recorded as rejecting K unless the source says so.
3. K may remain possible after the correction.

## What this prototype is trying to reveal

It is deliberately small. It may fail because:

- `semantic_force` is too coarse;
- `adoption` duplicates `semantic_force`;
- `scope` is underspecified;
- `revises` is insufficient for branching disagreement;
- open questions need their own lifecycle;
- a sidecar may create a second source of truth and increase inconsistency.

Those are useful failures. The goal is not to defend this representation. The goal is to make representation pressure observable before changing the frozen core.

## Cost of this protection

Making semantic force explicit can reduce false promotion and stale uncertainty, but it also adds classification work and creates a risk of over-formalizing ordinary dialogue. If every sentence must be classified, the continuity system may become slower, more rigid, and less natural.

Therefore this experiment should be judged not only by what errors it prevents, but also by whether the added representation cost is actually justified by repeated failures.

## Decision status

Authorization for this experiment means only: **run a small reversible test to make the idea visible**.

It does **not** mean the human adopted this sidecar, these field names, these categories, or any schema change. Those remain experimental until separately understood, tested, and adopted.
