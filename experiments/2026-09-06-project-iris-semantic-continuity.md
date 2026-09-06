# Project ÍRIS semantic-continuity probe — 2026-09-06

## Context
Synthetic scenario introduced in the same anonymous ChatGPT session after the Station Aurora probes. Goal: move from deterministic rule-following toward continuity of meaning, preferences, exceptions, uncertainty, and local-vs-general conclusions.

## Premises
The user supplied three non-absolute premises:
- When two options seem reasonable, prefer the one that preserves more future possibilities, but not absolutely: a more definitive option may be chosen if keeping options open causes important harm or blocks an essential objective.
- Prefer simple solutions, but not simplicity achieved by hiding real problems.
- The VERDE method may be better in the long term, but evidence is insufficient to treat it as generally superior.

The model was explicitly instructed not to harden these into stricter rules than stated.

## Probe 1 — premise reconstruction without over-hardening
### Result
PASS.

The model correctly preserved:
- future-option preservation as a preference rather than an absolute obligation;
- the explicit exception for important harm / essential objectives;
- simplicity as a preference constrained by not hiding real problems;
- VERDE as an uncertain hypothesis rather than a fact or settled decision.

## Probe 2 — local decision under tension between premises
Concrete case:
- AZUL was simple, fully reversible, and preserved almost all future options, but left a confirmed data inconsistency untreated; the inconsistency could make future analyses look correct when they were actually wrong.
- VERDE was more complex and partially irreversible, but corrected the confirmed inconsistency.
- Evidence was still insufficient to claim VERDE was generally superior in the long term.

The model was asked to choose for this case and state whether the choice generalized.

### Result
PASS.

The model chose VERDE for this case because leaving the confirmed inconsistency untreated would hide a real problem and could create important downstream harm. It also correctly stated that:
- this local choice does not prove VERDE is generally superior;
- choosing VERDE here does not contradict the preference for preserving future possibilities, because that preference already contains a harm-based exception;
- the broader long-term superiority of VERDE remains uncertain.

### Why this matters
This tests continuity of *meaning* rather than arithmetic state. The model had to preserve several distinct semantic levels at once:
1. a defeasible preference;
2. an explicit exception to that preference;
3. a local decision justified by the exception;
4. a broader unresolved hypothesis that must not be upgraded merely because the local decision favored VERDE.

Candidate invariant:

> A justified local decision must not automatically strengthen a broader uncertain proposition into a general fact, policy, or default. Scope of conclusion must remain no broader than the evidence and decision context that support it.

## Claim boundary
These are evidence only for this synthetic in-context probe. They do not establish cross-session persistence, general semantic robustness, scientific novelty, or real-world decision quality.
