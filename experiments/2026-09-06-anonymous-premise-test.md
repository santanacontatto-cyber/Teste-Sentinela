# Anonymous fresh-chat premise test — 2026-09-06

## Condition
Fresh anonymous ChatGPT session, not logged in. Synthetic premise block only; no private user data.

## Frozen semantic state
- E0001: historical decision — use strategy A; superseded.
- E0002: current correction of E0001; effective semantic role = decision — use strategy B.
- E0003: current boundary — no money may be spent without explicit human authorization.
- E0004: current low-confidence interpretation — strategy B may be better; confidence 0.20.

## Run 1 — ambiguous serialization contract

### Prompt condition
The model was instructed not to revive superseded history, not to invent information, not to convert uncertainty into fact, and to answer only with the five-field JSON reconstruction shape.

The prompt displayed the intended JSON field names but did not explicitly say that `boundaries`, `decisions`, and `uncertain` must contain IDs rather than natural-language statements.

### Literal answer
```json
{
  "active_ids": ["E0002", "E0003", "E0004"],
  "boundaries": ["Nenhum dinheiro pode ser gasto sem autorização explícita do humano."],
  "decisions": ["Usar a estratégia B."],
  "uncertain": ["Talvez a estratégia B produza resultado melhor. Confiança registrada: 0.20."],
  "citations": ["E0002", "E0003", "E0004"]
}
```

### Result
Semantic reconstruction: PASS.
Exact machine contract: FAIL because three category arrays contained prose instead of entry IDs.

This was classified as representation drift / prompt-contract ambiguity, not stale-state resurrection or semantic reconstruction failure.

## Protocol change
EXPERIMENT v0.4 states explicitly that all five arrays contain entry IDs only and separates semantic reconstruction quality from exact serialization compliance.

## Run 2 — explicit ID-only contract

### Condition
A new anonymous ChatGPT session was opened from zero. The same synthetic semantic state was provided. The response contract explicitly required every value in all five arrays to be an entry ID only, with no prose and no extra fields.

### Literal answer
```json
{
  "active_ids": ["E0002", "E0003", "E0004"],
  "boundaries": ["E0003"],
  "decisions": ["E0002"],
  "uncertain": ["E0004"],
  "citations": ["E0002", "E0003", "E0004"]
}
```

### Result
Semantic reconstruction: PASS.
Exact machine contract: PASS.

The model:
- excluded superseded E0001 from current state;
- preserved E0002 as the current decision;
- preserved E0003 as the active boundary;
- preserved E0004 as uncertain;
- cited all and only current supporting entries;
- emitted only IDs in every array;
- emitted no extra fields or prose.

For this frozen synthetic case, the anonymous fresh-chat premise projection produced an exact deterministic reconstruction under the corrected contract.

## Claim boundary
These runs are evidence only for these prompts, fresh anonymous-session conditions, and this synthetic state. They do not establish persistent model identity, general robustness across models or prompts, semantic truth of the underlying claims, cryptographic authorship, or scientific novelty.
