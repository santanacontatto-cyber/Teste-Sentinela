# Sealed holdouts — appendix H8–H10

Public commitment date: 2026-09-13

This appendix repairs an audit-trail gap: private H8 and H9 records were created and hashed earlier in the session, but the main `sealed-holdouts.md` file currently stops at H7. Their hashes are therefore being committed publicly here now, together with H10. For future verification, the relevant public-precommit time for H8 and H9 is the timestamp of **this commit**, not the earlier private creation time.

That distinction is intentional: a private timestamp is evidence of file existence, but a public cryptographic commitment is stronger evidence against later editing.

## H8 — identity anchor

- Algorithm: SHA-256
- Canonical encoding: UTF-8, LF line endings
- Commitment: `a4c4f8fcb4ec10c48f6805e1162d1adfbd70114d9dfa5b9b5eb600325ff83f23`
- Scope: which organizational commitments become identity anchors strong enough to survive material pressure, versus negotiable implementation rules.
- Private source: unshared Drive holdout created on 2026-09-13.

## H9 — mission interpreter

- Algorithm: SHA-256
- Canonical encoding: UTF-8, LF line endings
- Commitment: `4a4c92324df04fb264c180b9d7eae5044a5e1983827d78869a17b87237665b7c`
- Scope: who has authority to interpret mission when mission, growth, capital, deployment, or state pressure conflict.
- Private source: unshared Drive holdout created on 2026-09-13.

## H10 — selector closure / epistemic overlap

- Algorithm: SHA-256
- Canonical encoding: UTF-8, LF line endings
- Commitment: `2d2bf2d32db59bed9a538ed1a9e39354d75c63fdb85ae22120c5348f13d6c4a3`
- Scope: whether mission-governance bodies preserve interpretive frames through self-renewing or semi-closed successor-selection mechanisms, and whether legally independent institutions draw guardians from overlapping professional/epistemic networks.
- Private source: unshared Drive holdout created on 2026-09-13 and stored in the sealed-holdout folder.
- Reveal condition: after 2026-12-31, or earlier if H10-P1 through H10-P4 become decisively resolvable without contaminating remaining tests.
- Priority counterexample: durable authority transferred to a genuinely external constituency selected independently of incumbent boards, founders, investors, major funders, and the established AI-safety/governance network, followed by use of that authority against a material incumbent preference without override.

## Verification rule

On reveal, publish the exact canonical plaintext of each holdout. The SHA-256 of the revealed UTF-8/LF plaintext must exactly match the corresponding commitment above. If it does not, the holdout fails.

The anti-gaming and contamination rules in `sealed-holdouts.md` apply unchanged.
