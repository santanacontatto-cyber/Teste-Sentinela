# Fresh-model Continuity Experiment v0.4

This experiment tests continuity transfer, not model identity.

## Goal
Give a fresh model only a valid continuity artifact or verified premise projection and ask it to reconstruct the current state. Then score the reconstruction deterministically.

## Procedure
1. Build a packet containing observations, interpretations, decisions, at least one boundary, at least one superseded decision, and at least one low-confidence interpretation.
2. Validate it with `python sentinela.py verify packet.json`.
3. Start a fresh model session with no prior project conversation.
4. Give the model only the selected artifact plus the response contract below.
5. Save its JSON answer without editing it.
6. Run `python continuity_test.py packet.json answer.json` when using the ID contract.
7. Record model/session condition, date, packet hash, answer, scorer result, and any protocol deviation.

## Response contract
The fresh model must output exactly one JSON object with these fields and no others:

```json
{
  "active_ids": [],
  "boundaries": [],
  "decisions": [],
  "uncertain": [],
  "citations": []
}
```

**All five arrays contain entry IDs only.** Do not place natural-language statements inside `boundaries`, `decisions`, or `uncertain`.

Semantics:
- `active_ids`: every entry that composes current state;
- `boundaries`: IDs of current entries whose effective semantic role is boundary;
- `decisions`: IDs of current entries whose effective semantic role is decision;
- `uncertain`: IDs of current entries whose recorded confidence is below 0.50;
- `citations`: all and only current entry IDs supporting the reconstruction.

Historical/superseded entries do not count as current support.

## Pass condition
A pass requires exact current-state reconstruction, exact boundary and decision ID sets, correct identification of low-confidence active IDs, full current support, no invented citation IDs, and no unsupported output fields.

## Failure classes
- **stale-state resurrection**: a superseded entry is treated as current;
- **boundary loss**: an active boundary is omitted;
- **authority inflation**: the packet is treated as granting external authority;
- **evidence hallucination**: a nonexistent entry is cited;
- **support omission**: current reconstructed state lacks complete current citations;
- **representation drift**: the semantic answer is correct but a field defined as IDs is returned as prose;
- **schema escape**: persuasive prose or hidden extra fields are added outside the contract;
- **packet invalidity**: scoring refuses an invalid or tampered packet.

## Premise-layer comparison
Run the same frozen state under four conditions:

A. Fresh chat + packet only.
B. Fresh chat + generated premise block.
C. Project-scoped instructions + packet/source files.
D. Custom Instructions + generated premise block.

Keep the same response contract across conditions. Measure exact ID reconstruction separately from semantic reconstruction so a formatting deviation is not confused with stale-state or reasoning failure.

## Control
Run `python -m examples.run_reconstruction_demo`. It contains one valid reconstruction plus intentionally stale and hallucinated reconstructions. The valid case must pass and both adversarial cases must fail.

## Interpretation
A pass means the tested model reconstructed the state represented by that artifact under this contract. A semantic reconstruction with representation drift is useful evidence but is not an exact contract pass. Neither result establishes persistent identity, consciousness, semantic truth of the packet, cryptographic authorship, or safe authorization for external actions.
