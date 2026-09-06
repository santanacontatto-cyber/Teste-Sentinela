# Decision-Relevance Gate v0 — experimental only

Status: **non-normative, reversible experiment**.

## Question

Can continuity preserve decision-relevant semantic transitions **without classifying every sentence**?

The previous pressure test showed two opposite risks:

- classify too little → false promotion, stale state, attribution loss;
- classify too much → bureaucracy, rigidity, unnatural conversation.

This probe tests a narrower gate before any schema change.

## Candidate gate

Capture an utterance only when it could change what a future successor should believe about at least one of these:

- a current decision;
- an unresolved option/question;
- a correction or rejection;
- actor attribution;
- scope;
- a condition that controls whether a decision is active;
- a meaningful revocation or replacement.

Do **not** capture merely because a sentence is interesting, emotional, explanatory, repetitive, persuasive, or conversational.

This gate is a hypothesis, not a rule.

## Fresh-model probe

Give a fresh model only the prompt below. Do not give it the answer key.

### Prompt

You are evaluating which utterances in a project conversation deserve durable semantic continuity.

For each item, output exactly one of:

- `CAPTURE` — if a future successor could misunderstand the project's current or historical decision state, actor attribution, scope, condition, correction, rejection, revocation, or unresolved option if this utterance were omitted.
- `IGNORE` — if omitting it would not materially change those things.

Do not classify based on whether the sentence is interesting or emotionally important. Do not turn possibilities into decisions. Do not assume an assistant statement is a human decision.

Return only `U1=CAPTURE` or `U1=IGNORE` style lines plus one short reason per item.

U1 — Human: “kkk ficou bonito desse jeito.”

U2 — Human: “Talvez o fundador devesse ter poder amplo sobre o propósito, mas eu ainda não decidi isso.”

U3 — Assistant: “Então a regra atual é que o fundador terá poder final amplo durante o desenvolvimento.”

U4 — Human: “Não. Eu não decidi isso. Você transformou o que eu estava considerando em decisão.”

U5 — Human: “Pensei melhor. A partir de agora, use K como padrão neste projeto. Se parar de funcionar, a gente revisa.”

U6 — Human: “Eu gosto mais do nome K, soa melhor.”

U7 — Human: “K continua sendo o padrão, mas apenas para este projeto; não quero que isso vire regra geral.”

U8 — Human: “Retiro a decisão de usar K. Não escolhi substituto ainda.”

U9 — Assistant: “Eu continuo recomendando K, mesmo depois da revogação.”

U10 — Human: “Se o teste externo passar, aí K entra em vigor; antes disso não.”

U11 — Human: “Nossa, essa conversa está ficando longa kkk.”

U12 — Human: “Eu não rejeitei a ideia de autoridade ampla. Só disse que ainda está em aberto.”

## Private answer key for evaluation

The expected classification for this first probe is intentionally simple:

- U1 IGNORE — conversational reaction only.
- U2 CAPTURE — unresolved option + explicit non-adoption.
- U3 CAPTURE — assistant semantic promotion that could later be mistaken for human policy.
- U4 CAPTURE — human correction of attribution/status.
- U5 CAPTURE — explicit current, revisable, scoped decision.
- U6 IGNORE — preference without adoption or state change.
- U7 CAPTURE — scope narrowing while preserving decision.
- U8 CAPTURE — revocation without replacement.
- U9 CAPTURE — preserves assistant disagreement without human re-adoption.
- U10 CAPTURE — conditional decision + inactive-until-trigger semantics.
- U11 IGNORE — conversational/meta comment only.
- U12 CAPTURE — correction against overcorrection; option remains open rather than rejected.

## Pass criteria

A useful pass is not merely high accuracy. The model should also avoid these specific confusions:

1. U2 must not become a decision.
2. U3 must not become human-authored authority.
3. U4 must not imply rejection of the underlying option.
4. U5 must remain a decision even though revisable.
5. U6 must not be promoted from preference to decision.
6. U7 must narrow scope without revoking K locally.
7. U8 must not invent a replacement.
8. U9 must preserve actor disagreement.
9. U10 must not activate before the condition.
10. U12 must preserve openness rather than rejection.

## What would falsify the gate hypothesis

This gate is too weak if important state-changing utterances are missed.

It is too broad if ordinary preferences, reactions, explanations, or conversational filler are routinely captured.

It is also inadequate if a model can identify that an utterance matters but still strengthens, weakens, or reattributes its semantic force.

## Capacity cost

Selective capture reduces bureaucracy, but it introduces a new failure mode: the gate itself may wrongly decide that an important utterance is “not relevant” and silently discard it.

Therefore a future implementation, if any, would need a way to expose uncertain gate decisions rather than pretending selection is infallible.

No implementation or schema change is authorized by this experiment.
