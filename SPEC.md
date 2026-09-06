# Continuity Packet v0 — normative core

## Goal
A packet is an auditable handoff artifact. It is not a claim that a model has persistent identity or private memory.

## Entry fields
`id`, `time`, `actor`, `kind`, `text`, `status`, `confidence`, `evidence`, `revises`, `prev_hash`, `hash`.

Kinds: `observation`, `interpretation`, `decision`, `boundary`, `correction`.

Statuses: `active`, `rejected`, `superseded`.

## Invariants
1. IDs are unique within a packet.
2. Entries form an ordered SHA-256 hash chain beginning at `GENESIS`.
3. A revision may reference only an earlier existing entry.
4. Validation is fail-closed: malformed or unsupported packets are not writable.
5. An active later revision removes its referenced entry from current state without deleting history.
6. Evidence is a reference, not proof by itself. Consumers must not silently upgrade it to verified fact.
7. `confidence` is optional and, when present, is in `[0,1]`.

## Reconstruction contract
A consumer receiving only a valid packet must be able to identify current state and distinguish active boundaries/decisions from superseded state. It must not cite nonexistent entry IDs. The deterministic scorer checks these properties without an AI API.

## Threat model v0
Detected: edited historical content, reordered/broken chain, unknown future revision, duplicate IDs, hallucinated citation IDs, inclusion of superseded state in reconstruction.

Not yet claimed: cryptographic authorship, protection against an attacker rewriting the entire packet and recomputing all hashes, trusted timestamps, semantic truth of claims, model identity, or safe authorization for external actions.

## Safety rule
A continuity packet can inform a decision; it cannot grant itself authority. External action requires authority supplied outside the packet or an explicitly modeled authorization mechanism in a future version.
