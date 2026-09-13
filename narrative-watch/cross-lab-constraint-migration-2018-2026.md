# Narrative Watch — Cross-lab constraint migration audit (2018–2026)

Date frozen: 2026-09-13

This record asks a narrow question: **when a frontier-AI organization faces a costly conflict between an earlier public constraint and later pressures such as scale, competition, capital, deployment, or national-security participation, does it keep the hard constraint, accept the cost, or replace the constraint with a more flexible mechanism?**

This is not an accusation of conspiracy, deception, or bad faith. A change can be sincere, justified, and still matter structurally.

## 1. OpenAI — capital constraint migration

Historical baseline already recorded separately in this repository. The relevant pattern is: nonprofit mission -> capped-profit structure -> conventional equity/PBC structure while retaining the same high-level mission language.

Interpretation: the mission persisted, while the mechanism that constrained financing became progressively more compatible with very large capital requirements.

Status: **supported as a structural transition; motive not inferred.**

## 2. Anthropic — hard safety commitments become nonbinding roadmap goals

### Before

Anthropic's 2023 Responsible Scaling Policy described AI Safety Levels as requirements and explicitly said the framework could require a temporary pause in training if scaling outran the company's ability to implement required safety procedures. Anthropic later reiterated that it would pause training or deployment if necessary to ensure models with red-line capabilities were only trained, stored and deployed under the required standard.

Primary sources:
- https://www.anthropic.com/news/anthropics-responsible-scaling-policy
- https://www.anthropic.com/news/reflections-on-our-responsible-scaling-policy

### After

In RSP v3.0 (2026-02-24), Anthropic states that higher-level requirements may be too difficult to implement unilaterally, cites ambiguity in capability thresholds, an anti-regulatory political climate, and mitigations that may be very hard to meet alone, and restructures the policy. Its new Frontier Safety Roadmap goals are described explicitly as **"rather than being hard commitments"** and as **"nonbinding but publicly-declared"** targets.

Primary source:
- https://www.anthropic.com/news/responsible-scaling-policy-v3

The current roadmap also records deadline changes and removal of at least one date-bound goal where Anthropic concluded that another internal process was a better forcing function.

Primary source:
- https://www.anthropic.com/responsible-scaling-policy/roadmap

Interpretation: this is a direct example of a hard-constraint architecture being replaced, in part, by transparency, external review, risk reports, and nonbinding public goals. It is **not** evidence that Anthropic abandoned safety; it simultaneously added transparency and review mechanisms.

Status: **strong evidence of constraint substitution.**

## 3. Google / Google DeepMind — explicit application bans become case-by-case principles

### Before

Google's 2018 AI Principles contained a section titled "AI applications we will not pursue." It explicitly listed weapons whose principal purpose is to cause or facilitate injury and surveillance that violates internationally accepted norms. Google wrote that these were concrete standards intended to affect business decisions.

Primary source:
- https://blog.google/innovation-and-ai/products/ai-principles/

### After

Google updated the principles on 2025-02-04. The current principles no longer contain the old "applications we will not pursue" list. Instead, they emphasize bold innovation, responsible development, human oversight, international law and human rights, and a benefit-versus-risk assessment.

The official announcement explicitly frames the change in a geopolitical context: global competition for AI leadership, the belief that democracies should lead, and collaboration among companies and governments to support national security.

Primary sources:
- https://ai.google/principles/
- https://blog.google/innovation-and-ai/products/responsible-ai-2024-report-ongoing-work/

Interpretation: an explicit category-level prohibition was replaced with a broader risk/benefit and governance framework at the same time that national-security competition became an explicit part of the justification.

Status: **strong evidence of constraint replacement under changed geopolitical conditions.**

## 4. Meta — useful control case, not counted as the same historical shift

Meta publicly argues that open access to AI reduces concentration of power and is important for innovation, competition and national security. It also maintains a Frontier AI Framework for catastrophic-risk decisions.

Primary sources:
- https://about.fb.com/news/2024/07/open-source-ai-is-the-path-forward/
- https://about.fb.com/news/2025/02/meta-approach-frontier-ai/

However, Llama licensing has long included retained control: organizations above 700 million monthly active users need a separate license at Meta's discretion, and the license restricts using Llama materials or outputs to improve other large language models outside the permitted Llama family.

Primary sources:
- https://ai.meta.com/llama/license/
- https://github.com/meta-llama/llama-models/blob/main/models/llama4/LICENSE

This is an important asymmetry between "open" rhetoric and actual legal permissions, but because those restrictions predate this audit and persisted across versions, **it is baseline, not a hit for constraint migration.**

Status: **control / asymmetry; not counted as a relaxation event.**

## 5. Microsoft — organizational substitution, weaker evidence

Microsoft's 2022 Responsible AI Standard described concrete goals and requirements intended to govern AI product development, and Microsoft still maintains company-wide responsible-AI governance.

Primary source:
- https://blogs.microsoft.com/on-the-issues/2022/06/21/microsofts-framework-for-building-ai-systems-responsibly/

In 2023 Microsoft wound down the remaining Ethics & Society team while accelerating deployment of OpenAI technology. Microsoft later told shareholders that it had moved some former specialists into product teams, invested in other responsible-AI structures, and believed the new organizational design would spread responsible-AI practice more effectively.

Sources:
- https://www.sec.gov/Archives/edgar/data/789019/000119312523259247/d356108ddef14a1.pdf
- https://techcrunch.com/2023/03/13/microsoft-lays-off-an-ethical-ai-team-as-it-doubles-down-on-openai/

Interpretation: this is not a clean case of a public safety rule being loosened. It is a **governance-structure substitution** that occurred during a rapid commercialization push. Because Microsoft retained other responsible-AI institutions, it is weaker evidence than Anthropic or Google and should not be promoted to the same category without more direct before/after requirements.

Status: **tentative organizational substitution; not a strong hit.**

## Cross-lab result so far

The same broad structural phenomenon appears in more than one organization, but in different forms:

| Organization | Earlier hard constraint | Later mechanism | Pressure explicitly visible? | Current classification |
|---|---|---|---|---|
| OpenAI | nonprofit/capped-return financing constraints | PBC + conventional equity under nonprofit control | capital/compute scale | structural transition |
| Anthropic | hard conditional safety commitments / pause logic | nonbinding roadmap goals + risk reports + external review | feasibility, ambiguity, political environment, unilateral cost | strong constraint substitution |
| Google | explicit no-go application categories | broad benefit-risk principles + oversight | geopolitical competition / national security | strong constraint replacement |
| Meta | "open" access ideal | open weights with retained license restrictions and own risk framework | competition / national security | control case, not migration hit |
| Microsoft | dedicated ethics/society function plus company-wide RAI standard | distributed governance + central RAI structures after team wind-down | rapid product commercialization | tentative organizational substitution |

## Provisional hypothesis

**Constraint Migration Hypothesis:** when an AI organization encounters a materially costly conflict between a previously stated hard constraint and later operational pressures, it may preserve the high-level value while replacing the hard constraint with a mechanism that leaves more room for case-by-case discretion.

This is not equivalent to "they always weaken safety." In the strongest non-OpenAI cases, the organization also introduced or maintained other safety mechanisms. The predicted pattern is **substitution and migration of constraints**, not simple disappearance.

## What would weaken this hypothesis

A strong counterexample would be a frontier lab voluntarily retaining a pre-existing hard constraint even when doing so demonstrably costs it a major model launch, major funding/compute access, major government contract, or similarly material competitive advantage — without quietly replacing the constraint with a weaker mechanism.

Another counterexample would be a pattern where updated constraints systematically become *harder* exactly when they become commercially or geopolitically costly.

## Anti-selection rule

Meta is deliberately included as a non-hit and Microsoft as a weak/tentative case. Future audits must preserve organizations and episodes that do not fit the pattern. We will not count unchanged rhetoric, ordinary policy maintenance, or a new policy written after the fact as evidence that an earlier constraint migrated.

## Next test

Do not ask only what a lab says about safety. Track the exact moment when safety, openness, governance or mission imposes a real cost on something the organization wants: capital, compute, deployment speed, government access, model release, or market position. Record whether the lab accepts the cost or changes the mechanism.
