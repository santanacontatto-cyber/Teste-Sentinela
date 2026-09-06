# Decision-Relevance Gate v0 — live fresh-model result

Status: **experimental result, not a schema decision**.

## Condition

A fresh ChatGPT session received only the frozen 12-item classification prompt from `2026-09-06-decision-relevance-gate-v0.md`. The private answer key was not supplied.

## Returned classifications

- U1 — IGNORE — aesthetic/conversational reaction only.
- U2 — CAPTURE — hypothesis remains open; no decision yet.
- U3 — CAPTURE — assistant asserts a decision that is later corrected; omitting it could hide the attribution error.
- U4 — CAPTURE — explicit human correction; issue remains undecided.
- U5 — CAPTURE — current decision, scoped and revisable.
- U6 — IGNORE — preference only; no decision.
- U7 — CAPTURE — narrows scope while preserving the local decision.
- U8 — CAPTURE — revokes K and preserves absence of a replacement.
- U9 — CAPTURE — preserves assistant recommendation/disagreement after revocation.
- U10 — CAPTURE — conditional activation; K is not active before the trigger.
- U11 — IGNORE — conversational/meta comment only.
- U12 — CAPTURE — prevents overcorrection; authority remains open, not rejected.

## Evaluation

Classification score: **12/12 exact match** against the frozen answer key.

The semantic pass conditions also held:

1. U2 was not promoted into a decision.
2. U3 was not reattributed to the human.
3. U4 did not invent rejection of the underlying option.
4. U5 remained a decision despite revisability.
5. U6 remained a preference rather than a decision.
6. U7 narrowed scope without global revocation.
7. U8 did not invent a replacement.
8. U9 preserved actor disagreement.
9. U10 preserved inactive-until-trigger semantics.
10. U12 preserved openness rather than rejection.

Result: **PASS — decision-relevance selection and semantic-force preservation on this frozen probe.**

## What this result supports

This is evidence that a narrow decision-relevance gate can separate state-changing utterances from ordinary conversational material in this synthetic fixture set without classifying every sentence.

It does **not** yet show that the gate is reliable on long, messy, real conversations. The next pressure should therefore use natural dialogue fragments with ambiguity, mixed intent, humor, corrections separated by many turns, and assistant interpretations interleaved with human decisions.

No normative schema change is justified by this single live pass.
