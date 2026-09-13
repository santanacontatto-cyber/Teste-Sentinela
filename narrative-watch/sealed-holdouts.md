# Sealed holdouts

This file records cryptographic commitments to predictions that are intentionally **not public yet**.

The purpose is to reduce observer effects and strategic adaptation. Public predictions can change the behavior of the actors being observed. A sealed holdout lets us prove later that a prediction existed before an event without showing the prediction in advance.

## H1 — committed 2026-09-13

- Algorithm: SHA-256
- Canonical encoding: UTF-8, LF line endings
- Commitment: `c1595fbff1f3d7d70a26da4e0c76cc0a1d0eeeadf2d2939f97850fd6bf704f9c`
- Private source: an unshared continuity record stored outside this public repository.
- Reveal condition: after the first qualifying post-2026-09-13 frontier-AI incident has resolved through the longest applicable horizon, or earlier if public exposure of Narrative Watch itself becomes the main contamination event.

### Verification after reveal

When H1 is revealed, the exact canonical plaintext and its salt will be published. Anyone can compute SHA-256 over that plaintext and verify that it equals the commitment above.

### Anti-gaming rule

If an actor under observation cites, links to, or demonstrably responds to Narrative Watch before a prediction resolves, affected predictions are marked `CONTAMINATED`. They do **not** count as clean confirmation, even if the subsequent behavior matches the prediction.

A public prediction and a sealed holdout must never be silently merged after the fact. Hits, misses, contamination, ambiguity and methodological failures remain visible.
