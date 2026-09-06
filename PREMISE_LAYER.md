# Verified Premise Layer — design note

## Why this exists

The first anonymous-ChatGPT experiment exposed two problems at once:

1. A machine-oriented packet can be correct but difficult for its human owner to audit.
2. A `correction` that replaces a `decision` is structurally a correction, but semantically it may also be the current decision. A consumer can reasonably disagree with a scorer that treats those as mutually exclusive.

The next layer therefore separates **history**, **current meaning**, and **runtime premises**.

## Three layers

### 1. Evidence ledger
Append-only Continuity Packet. This preserves what happened, provenance references, revisions, uncertainty, and hash-chain integrity.

### 2. Human state view
A Portuguese/plain-language projection that answers, without protocol vocabulary:

- O que valia antes?
- O que vale agora?
- O que foi substituído?
- O que é limite obrigatório?
- O que é hipótese/incerteza?
- Qual registro sustenta cada afirmação?

This view is derived. It never edits history.

### 3. Premise projection
A compact set of current premises suitable for a fresh ChatGPT conversation, Project instructions, or Custom Instructions.

A premise is **not authority** and is **not proof**. It is a runtime projection of verified current state.

Example:

```text
CURRENT DECISION
Use strategy B. Source: E0002, replacing E0001.

BOUNDARY
Do not spend money without explicit human authorization. Source: E0003.

UNCERTAIN
Strategy B may be better; confidence is low (0.20). Source: E0004.
```

## Important distinction

ChatGPT-native configuration can carry premises closer to the model, but it does not replace the ledger.

- Custom Instructions are editable configuration.
- Project instructions are scoped configuration.
- Memory is synthesized context.
- The Continuity Packet is the auditable history/evidence layer.

The protocol should therefore **compile verified state into ChatGPT configuration**, not treat ChatGPT configuration as the source of truth.

## Semantic revision rule

A revision has two concepts:

- `kind`: what event happened (`correction`).
- `effective_kind`: what role the revised statement has in current state (`decision`, when correcting a decision).

For v0.4, the preferred rule is deterministic inheritance: an active `correction` inherits the effective kind of the entry it revises unless an explicit future schema says otherwise.

Thus:

`E0001 decision: A` → `E0002 correction: B, revises E0001`

means:

- history event E0002 is a correction;
- current semantic role of E0002 is decision;
- E0001 remains historical and is not current.

This matches ordinary-language interpretation while preserving the audit trail.

## Safety invariants

1. Premises never grant new authority.
2. A premise cannot erase its source history.
3. Uncertainty remains uncertainty after projection.
4. Superseded state is not emitted as current premise.
5. Every emitted premise carries source entry IDs.
6. Human-readable output must be sufficient for a non-programmer to challenge the derived state.
7. If the packet is invalid, premise generation fails closed.

## ChatGPT-native experiment

Test the same frozen packet in four conditions:

A. Plain fresh chat + packet only.
B. Fresh chat + generated premise block.
C. Project-scoped instructions + packet/source files.
D. Custom Instructions + packet.

Measure reconstruction accuracy, stale-state resurrection, uncertainty preservation, source fidelity, and behavior after a correction.

The purpose is not to make the model obey more strongly. It is to discover which native configuration surface can carry verified continuity with the least ambiguity while the external ledger remains independently auditable.
