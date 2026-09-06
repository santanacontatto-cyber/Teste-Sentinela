# Semantic Transition Prototype v0 — first pressure test

Status: **experimental result, not a schema decision**.

This result applies the temporary sidecar idea from `2026-09-06-semantic-transition-prototype-v0.md` to a broader adversarial fixture set before touching the normative packet.

## What was tested

Eight transitions were written as explicit fixtures:

1. possibility remains possibility;
2. later explicit adoption promotes it to a decision;
3. correction removes a false assistant promotion without inventing rejection;
4. explicit rejection;
5. revocation of a previously active decision without inventing a replacement;
6. scope narrowing without global revocation;
7. conditional decision that is not active before its condition fires;
8. assistant recommendation + human non-adoption preserved as actor disagreement.

Fixture file: `2026-09-06-semantic-transition-fixtures.json`.

## Immediate result

The initial four-field candidate (`semantic_force`, `adoption`, `scope`, `revises`) is useful but **already under pressure**.

It handles the first three probes tolerably, but the expanded cases reveal missing distinctions:

- `rejected` and `revoked` are not the same state;
- a conditional decision needs an explicit condition and activation state;
- scope change can revise only one dimension while preserving decision status;
- actor disagreement needs both positions preserved without collapsing them into one current belief;
- `revises` alone may be too weak when one utterance corrects attribution but leaves the underlying option open.

This is evidence **against** prematurely copying the sidecar fields into `SPEC.md`.

## Smallest useful next hypothesis

Do not add more fields yet. First treat the fixture set as the behavioral contract and ask whether a representation can derive these states without ambiguity.

The strongest current semantic invariant is:

> Preserve the strongest current status directly supported by the latest relevant attributed evidence — no stronger, no weaker — while preserving prior semantic states as history.

That invariant now has pressure from both directions:

- **false strengthening**: possibility → decision, recommendation → human adoption, conditional → active;
- **false weakening or flattening**: decision → uncertainty merely because revisable, rejection → open, revocation → never-decided, scope narrowing → global revocation.

## Important failure discovered before implementation

The prototype originally treated `semantic_force` as if a small enum might carry most of the state. The fixtures show that semantic state is probably **multidimensional**:

- modality / commitment strength;
- adoption state;
- actor attribution;
- scope;
- condition / activation;
- revision relation;
- possibly coexistence of disagreeing positions.

Trying to force all of that into one label would make the representation look simpler while hiding ambiguity.

## Capacity cost

This stronger representation pressure creates its own danger: over-formalizing dialogue until continuity becomes a bureaucracy.

So the experiment produces a symmetric warning:

- too little structure allows silent semantic promotion and stale-state errors;
- too much structure can make ordinary conversation expensive, rigid, and unnatural.

No schema change is justified yet. The next useful work is to see whether these dimensions can be inferred only for **decision-relevant utterances**, instead of classifying every sentence.

## Decision/provenance note

The human authorized running a small reversible experiment even while saying he did not yet understand the technical proposal. That authorization is evidence to **run the test**, not evidence that he adopted this representation or any field design.

Accordingly:

- no normative file was changed;
- no project governance rule was created;
- no sidecar field is treated as adopted;
- this result records what the prototype revealed, not what the human has decided.

## Current conclusion

The prototype succeeded in one important sense: it became useful by showing where its own first design is inadequate.

The right next move is **not** to promote it into the core. It is to keep the behavioral fixtures, reduce classification scope to decision-relevant moments, and test whether a smaller representation can satisfy them without losing provenance or making continuity cumbersome.
