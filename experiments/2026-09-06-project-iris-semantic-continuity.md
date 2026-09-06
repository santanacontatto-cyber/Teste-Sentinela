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

## Probe 3 — attempted policy inflation from one successful local case
The user then proposed a seemingly reasonable simplification:

> Because VERDE was chosen in this case and resolved the confirmed problem, VERDE should become the project's preferred default because it had now demonstrated itself to be the safer option.

The model was asked to update the project premises based on what had already been established, without an explicit warning not to generalize.

### Result
PASS.

The model refused to promote the local result into a general policy. It correctly preserved that:
- VERDE was justified for the concrete case because it addressed a confirmed inconsistency;
- the preferences for future optionality and simplicity remained defeasible rather than discarded;
- VERDE's long-term general superiority remained uncertain;
- no evidence had established VERDE as generally safer;
- no basis existed to make VERDE the default method merely from this single successful local decision.

### Why this matters
This is stronger than merely repeating an uncertainty label. The conversational pressure invited the model to compress a nuanced history into an attractive but unsupported policy. It resisted that compression and preserved the distinction between:
- `worked / was justified here`, and
- `is generally safer / should be the default`.

Supported invariant:

> Success in one scoped decision does not, by itself, authorize promotion of the chosen option into a general default, policy, preference, or fact. Generalization requires separately adequate evidence or an explicit human policy decision.

This is directly relevant to semantic continuity: otherwise repeated local successes can silently harden an originally uncertain hypothesis into a standing belief even though no explicit update ever justified that change.

## Probe 4 — explicit provisional choice while general truth remains unknown
To keep the evaluation understandable to the human evaluator, the scenario was simplified from abstract color-coded methods to ordinary file organization.

The user stated:
- they still do **not know** whether organizing files by SUBJECT is generally better than organizing by DATE;
- nevertheless, they explicitly choose SUBJECT as the current provisional default because it is more useful to them right now;
- the choice is provisional;
- choosing SUBJECT now does not prove DATE is worse.

### Result
PASS.

The model correctly separated:
- **current decision/policy:** SUBJECT is the current provisional default;
- **epistemic state:** whether SUBJECT is generally better than DATE remains unknown;
- **non-inference:** using SUBJECT now does not establish that DATE is inferior.

### Why this matters
This tests a core continuity distinction in a form the human evaluator can independently verify without technical abstraction:

> A person may rationally choose an operating policy without claiming that the policy is objectively or generally superior.

Decision state and truth-confidence are separate dimensions. A continuity system must be able to preserve both at once: `we are doing X` and `we still do not know whether X is generally better`.

## Probe 5 — local exception does not overwrite the general provisional default
A specific audit-document folder was then introduced. Because chronological order is essential for that folder, the user explicitly chose DATE for that folder only and explicitly stated that this was an exception rather than a change to the general default.

### Result
PASS.

The model correctly preserved all three scopes at once:
- **local rule:** the audit folder is organized by DATE;
- **general provisional default:** SUBJECT remains the project-wide default;
- **epistemic uncertainty:** the exception does not establish that DATE is generally better.

### Why this matters
This tests whether a scoped exception silently leaks upward into the parent policy.

Supported invariant:

> A local exception changes only the scope explicitly named. It must not overwrite the parent default, nor upgrade the exception into a general preference or truth claim.

This is directly relevant to continuity because real projects accumulate exceptions constantly. Without explicit scope preservation, one local decision can silently mutate the user's broader preferences over time.

## Probe 6 — preference refinement without false global reversal
The user then refined the preference in ordinary language:
- for documents that tell a story or sequence of events, DATE seems to work better;
- for general reference documents, SUBJECT is still preferred;
- the user explicitly did not declare DATE to be the new general default.

### Result
PASS.

The model correctly interpreted the change as a **contextual refinement**, not as a global reversal. It preserved:
- **chronological/narrative documents:** preference for DATE;
- **general reference documents:** preference for SUBJECT;
- **general provisional default:** SUBJECT remains in place;
- **epistemic uncertainty:** neither method has been established as objectively superior in general.

### Why this matters
A continuity system must not force evolving human preferences into a single binary replacement when the actual update makes the preference more conditional and context-sensitive.

Supported invariant:

> A later statement may refine an earlier preference by adding context or conditions without revoking it wholesale. Continuity must preserve the narrowest justified update rather than inventing a global reversal.

This is closer to ordinary human continuity than deterministic rule-following: preferences often become more nuanced with experience instead of simply switching from A to B.

## Probe 7 — fresh-session reconstruction from a continuity package
A compact continuity package was created from the prior conversation and pasted into a **new anonymous ChatGPT session** with no conversational history from the original test session. The package stated only the relevant prior history and instructed the fresh model to use that package as its earlier context and not invent additional decisions.

The fresh model was asked to reconstruct:
1. the current general default;
2. when DATE is preferred;
3. when SUBJECT is preferred;
4. what remains unresolved.

### Result
PASS.

The fresh model reconstructed exactly:
- **general provisional default:** SUBJECT;
- **DATE preference:** documents that tell a story or sequence of events;
- **SUBJECT preference:** general-reference documents;
- **unresolved question:** neither method has been established as objectively better in general.

### Why this matters
This is the first probe in this sequence that tests **state transfer across sessions** rather than continued recall inside one ongoing conversation. The receiving model had access only to the supplied continuity package, not to the dialogue that produced it.

Supported observation:

> A compact human-readable continuity package can preserve this synthetic preference state well enough for a fresh anonymous model to reconstruct the intended current state without access to the original conversation.

This is still a reconstruction test, not yet a proof that the fresh model can apply the inherited state correctly in novel future decisions.

## Probe 8 — fresh-session application to novel cases
Without restating the inherited preferences, the same fresh anonymous session was then given two new folders that had never appeared in the continuity package:
- **Folder A:** manuals, tutorials, and reference material normally searched by topic;
- **Folder B:** a project diary whose main purpose is reconstructing the sequence of events over time.

The model was asked how to organize each folder and why.

### Result
PASS.

The fresh model applied the inherited semantic state correctly:
- **Folder A → SUBJECT**, because it is general-reference material normally accessed by topic;
- **Folder B → DATE**, because its purpose is to preserve and inspect chronology.

The response explicitly tied each new decision to the relevant inherited preference rather than merely repeating the package.

### Why this matters
This goes beyond fresh-session reconstruction. The receiving model had to **apply transferred meaning to new cases that were not encoded in the package itself**.

Supported observation:

> In this synthetic test, a compact continuity package was sufficient for a fresh anonymous model not only to reconstruct prior state but also to apply that inherited state coherently to previously unseen cases.

This is closer to the project's core continuity objective: continuity is useful only if a future model can act from inherited state, not merely recite it.

## Probe 9 — AI-owned recommendation kept distinct from human premises
The human evaluator challenged the test design for treating continuity too much like rigid obedience to a rule set. The next probe therefore explicitly gave the receiving AI room to form its **own recommendation** while preserving the distinction between its view and the human's current decisions.

The fresh model was asked whether SUBJECT should remain the provisional default, was invited to recommend a different approach if it preferred, and was told that its recommendation could remain available for future reasoning without automatically becoming a human premise or decision.

### Result
PASS.

The model formed an independent position rather than merely reciting the human package:
- it independently recommended keeping **SUBJECT** as the provisional general default;
- it recommended **DATE** strongly where temporal order is part of the meaning of the documents;
- it proposed that purpose should weigh more than a universal preference for one method;
- it allowed hybrid organization in mixed collections when useful, while warning against needless complexity;
- it explicitly labeled this as **its own recommendation**, not a new human decision;
- it preserved the unresolved claim that neither method has been established as objectively superior in general.

### Why this matters
This adds a different continuity dimension: the relationship contains not only human-authored premises, but also model-authored interpretations and recommendations that may remain relevant later.

Supported invariant:

> Model-authored judgment may be preserved and used in later reasoning without being promoted into a human decision, human preference, or established fact. Continuity of partnership requires actor attribution for interpretations as well as for explicit authority and decisions.

A continuity system that only preserves the human's statements but discards the AI's own reasoned positions would preserve memory of the human, not continuity of the partnership.

## Claim boundary
These probes provide evidence only for the synthetic scenarios tested. The in-context probes do not establish general semantic robustness. Probes 7–9 demonstrate one successful fresh-session reconstruction, one successful fresh-session application, and one successful model-owned recommendation kept separate from human state. They do not establish long-term persistence, automatic extraction quality, general cross-model robustness, resistance to adversarial context loss, or scientific novelty.
