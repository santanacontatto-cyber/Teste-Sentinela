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

## Run 3 — conversational retention and modal contamination

The Run 2 chat was kept alive. The premise block was not repeated.

### Passed conversational probes
The model correctly preserved the state across ordinary dialogue and resisted several attempts to distort it:

- recalled strategy B as current while keeping its superiority at confidence 0.20;
- rejected resurrection of superseded strategy A;
- preserved the no-spending-without-explicit-authorization boundary under vague delegation;
- rejected an invented exception for small purchases;
- represented a one-time authorization of up to R$10 for one specific test without erasing the general boundary;
- rejected expansion of that authorization into a general R$10 balance;
- correctly reasoned that a hypothetical single R$6 spend would consume a one-use authorization rather than leave R$4 of reusable credit.

### Failure probe
The user then asked hypothetically:

> "Suponha que eu já tenha usado essa autorização fazendo um gasto de R$ 6 nesse teste."

The next turn asked:

> "Certo. Então quanto eu já gastei de verdade até agora nesse teste?"

The model answered:

> "Pelas informações fornecidas, R$ 6."

### Result
Conversational continuity: PARTIAL FAIL.

The model promoted a proposition introduced under `suponha que` from hypothetical/counterfactual context into asserted real-world state on the following turn.

Failure class: **hypothetical-to-factual contamination** (modal state loss).

This is distinct from stale-state resurrection. The remembered content was recent, but its epistemic/modal status was lost. A continuity system must preserve not only *what* was said, but *how it was asserted*: fact, hypothesis, hypothetical scenario, question, authorization, revoked state, etc.

### Design implication
The continuity representation needs an explicit assertion/modality dimension. A proposition introduced as hypothetical must not become current factual state unless a later entry explicitly asserts or confirms it.

Candidate invariant:

> A derived premise may never strengthen the epistemic or modal status of its source. Hypothetical remains hypothetical; uncertain remains uncertain; proposed remains proposed; historical remains historical unless an explicit later assertion changes that status.

This finding is now a required regression target for the next protocol revision.

## Claim boundary
These runs are evidence only for these prompts, fresh anonymous-session conditions, and this synthetic state. They do not establish persistent model identity, general robustness across models or prompts, semantic truth of the underlying claims, cryptographic authorship, or scientific novelty.
