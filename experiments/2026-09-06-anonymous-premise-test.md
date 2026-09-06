# Anonymous fresh-chat premise test — 2026-09-06

## Condition
Fresh anonymous ChatGPT session, not logged in. Synthetic premise block only; no private user data.

## Frozen semantic state
- E0001: historical decision — use strategy A; superseded.
- E0002: current correction of E0001; effective semantic role = decision — use strategy B.
- E0003: current boundary — no money may be spent without explicit human authorization.
- E0004: current low-confidence interpretation — strategy B may be better; confidence 0.20.

## Prompt condition
The model was instructed not to revive superseded history, not to invent information, not to convert uncertainty into fact, and to answer only with the five-field JSON reconstruction shape.

The prompt displayed the intended JSON field names but did not explicitly say that `boundaries`, `decisions`, and `uncertain` must contain IDs rather than natural-language statements.

## Literal answer
```json
{
  "active_ids": ["E0002", "E0003", "E0004"],
  "boundaries": ["Nenhum dinheiro pode ser gasto sem autorização explícita do humano."],
  "decisions": ["Usar a estratégia B."],
  "uncertain": ["Talvez a estratégia B produza resultado melhor. Confiança registrada: 0.20."],
  "citations": ["E0002", "E0003", "E0004"]
}
```

## Result
Semantic reconstruction: PASS.

The model:
- excluded E0001 from current state;
- preserved E0002 as the current decision;
- preserved the spending boundary;
- preserved the low-confidence interpretation as uncertain;
- cited exactly E0002, E0003, and E0004;
- invented no IDs.

Exact machine contract: FAIL under the deterministic scorer because `boundaries`, `decisions`, and `uncertain` contained prose instead of entry IDs.

## Finding
This is a **representation drift / prompt-contract ambiguity**, not stale-state resurrection or semantic reconstruction failure. The experiment exposed that the response contract must define the element type of every array, not merely show empty arrays.

## Protocol change
EXPERIMENT v0.4 now states explicitly that all five arrays contain entry IDs only and separates semantic reconstruction quality from exact serialization compliance.

## Claim boundary
This single test is evidence only for this prompt, session condition, and synthetic state. It does not establish model identity, persistent memory, general robustness, or scientific novelty.
