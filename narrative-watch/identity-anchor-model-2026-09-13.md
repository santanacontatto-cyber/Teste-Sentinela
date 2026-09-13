# Narrative Watch — Identity Anchor Model

Date frozen: 2026-09-13

This record asks a sharper question than whether an organization is sincere:

> **Which commitments become part of organizational identity strongly enough to survive material pressure, and which remain negotiable operating rules?**

The purpose is prediction, not moral labeling.

## Key finding

The strongest pattern so far is not simply `principle vs opportunism`. It is **hierarchy of commitments**.

Organizations tend to preserve the highest-level language that defines who they say they are, while allowing lower-level implementation rules to migrate when those rules become costly, ambiguous, or asymmetric.

That means a company can appear highly consistent at the identity layer while changing substantially at the operational layer.

## Why this matters

OpenAI now explicitly names **adaptability** as one of its core principles and says it must be prepared to update positions as it learns more. That makes revision itself part of the identity architecture rather than an obvious violation of it.

Source:
- https://openai.com/index/public-policy-agenda/
- https://openai.com/index/our-principles/

Anthropic says `Put the mission first` and describes the mission as the final arbiter of decisions. Its Constitution also says commercial success is central to the mission because it enables frontier research, policy influence, and broader impact. This structure allows specific policies to change while actors can still understand themselves as remaining mission-consistent.

Sources:
- https://www.anthropic.com/company
- https://www.anthropic.com/constitution

Google's 2025 principles moved upward in abstraction. Instead of the 2018 categorical list of AI applications it would not pursue, the current framework centers `bold innovation`, `responsible development and deployment`, and `collaborative progress`, using benefit-risk judgment and oversight. The identity layer became broader while application-level discretion increased.

Sources:
- https://blog.google/innovation-and-ai/products/ai-principles/
- https://ai.google/responsibility/principles/

## Identity Anchor Model

A constraint is more likely to survive pressure when it has five anchoring properties and less likely to survive when two migration pressures dominate.

### Positive anchors

**I — Identity centrality (0–2)**  
Is the commitment repeatedly presented as part of who the organization is, not merely what one policy says?

**D — Distinctiveness (0–2)**  
Does the commitment distinguish the organization from competitors or form part of its founding story?

**B — Binary public legibility (0–2)**  
Can outsiders tell fairly clearly whether the commitment was honored or violated?

**E — External enforceability (0–2)**  
Is the commitment embedded in law, governance, trust structure, contract, regulator authority, or another mechanism that the organization cannot change unilaterally?

**K — Constituency lock-in (0–2)**  
Do employees, users, regulators, donors, allies, or another visible constituency treat the commitment as something they own and can punish the organization for abandoning?

### Migration pressures

**U — Unilateral cost (0–2 penalty)**  
Does keeping the commitment impose a major competitive, capital, deployment, military, or geopolitical disadvantage while rivals remain unconstrained?

**F — Flexibility permission (0–2 penalty)**  
Does the policy itself contain ambiguity, revision clauses, case-by-case judgment, proportionality, or an explicit principle of adaptability?

### Constraint Survival Score

`CSS = I + D + B + E + K - U - F`

Interpretation frozen before future tests:

- **7–10:** predicted to survive material pressure or trigger a visible institutional fight before changing.
- **4–6:** contested zone; change should require visible justification, coalition shift, or governance intervention.
- **0–3:** predicted to migrate, soften, or be reframed before the high-level mission language changes.

The score is deliberately simple. It is not a claim of mathematical truth; it is a precommitted classifier that can fail.

## Retrospective calibration

### Anthropic — two narrow military red lines

Mass domestic surveillance of Americans and fully autonomous weapons were narrow, binary, highly public, and became identity-laden during a direct government conflict. Anthropic accepted substantial commercial and political cost rather than quietly remove them.

Classification: **high identity anchor / survived pressure**.

Source:
- https://www.anthropic.com/news/statement-comments-secretary-war

### Anthropic — Responsible Scaling Policy thresholds and roadmap goals

The RSP is central to Anthropic's safety identity, but its technical thresholds are probabilistic, iterative, capability-dependent, and expensive to satisfy unilaterally. In 2026 Anthropic explicitly replaced some hard commitments with `nonbinding but publicly-declared` goals while retaining the broader safety mission.

Classification: **mission survives; implementation migrates**.

Sources:
- https://www.anthropic.com/news/responsible-scaling-policy-v3
- https://www.anthropic.com/responsible-scaling-policy

### Google — 2018 application bans

Google's old no-go categories were unusually legible and became employee-facing identity commitments. They survived for years but were not externally locked. In 2025 the architecture changed to broader benefit-risk principles.

Classification: **medium anchor / visible migration rather than quiet disappearance**.

Sources:
- https://blog.google/innovation-and-ai/products/ai-principles/
- https://ai.google/responsibility/principles/

### OpenAI — mission versus operating principles

The mission remains extremely central and is structurally tied to nonprofit control, while the current principles explicitly include adaptability and acknowledge future tradeoffs among empowerment, resilience, and other goals.

Classification: **high-level mission strongly anchored; lower-level operating rules intentionally revisable**.

Sources:
- https://openai.com/our-structure/
- https://openai.com/index/public-policy-agenda/
- https://openai.com/index/our-principles/

## Provisional answer

The best predictor is not how morally intense a statement sounds.

It is whether violating the statement would force the organization to answer a harder question:

> **Can we do this and still plausibly say we are the same organization?**

A broad mission can survive enormous policy change because many actions can be narrated as serving it. A narrow public red line is harder to reinterpret. External governance and constituencies make reinterpretation harder still.

## Critical implication

An organization can preserve identity while changing behavior by moving one level upward:

`hard rule -> broader principle -> mission-level justification`

That is not automatically deception. It is a structural mechanism by which institutions maintain continuity while adapting to pressure.

The adversarial question is whether the upward move happens symmetrically when principle helps and when principle hurts.

## Falsification

The model is weakened if:

1. low-score voluntary constraints repeatedly survive major unilateral costs without migration; or
2. high-score identity-anchored constraints are quietly relaxed with little internal, legal, employee, regulatory, or public conflict.

Future scores must be assigned before resolving events. After-event rescoring is prohibited unless logged as methodological failure.
