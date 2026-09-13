# Narrative Watch — Selector Loop & Epistemic Overlap

Date frozen: 2026-09-13

This record asks a more structural question than whether frontier-AI organizations sincerely believe their stated missions:

> **Who selects the people who are allowed to interpret the mission when principles conflict?**

The answer matters because an institution can have formally independent safety or mission guardians while still reproducing the same interpretive frame through the way those guardians are selected.

## Finding 1 — OpenAI Foundation is a self-renewing selector loop

OpenAI Foundation's 2024 Form 990 states that the organization's members are the individuals who serve as its directors, and that those members elect the directors. The members also approve amendments to the governing documents and certain material transactions.

That produces a closed selector loop at the nonprofit layer:

`directors -> members -> elect directors`

This is not inherently improper. Self-perpetuating nonprofit boards are a common governance form. But it means there is no ordinary outside electorate choosing the people who control the mission layer.

The OpenAI Foundation then has sole authority to appoint and remove all OpenAI Group directors. Its Safety and Security Committee has authority to require mitigations up to and including halting the release of models.

Primary sources:
- OpenAI Foundation 2024 Form 990, Schedule O: https://cdn.theconversation.com/static_files/files/4100/2024-IRS990-OpenAI.pdf
- OpenAI structure: https://openai.com/our-structure/
- California AG / OpenAI MOU (2025): https://cdn.theconversation.com/static_files/files/4101/Final_Executed_MOU_Between_OpenAI_and_California_AG_re_Notice_of_Conditions_of_Non-Objection_(10.27.2025)_(Signed_by_OpenAI)_(Signed_by_CA_DOJ).pdf

### External brake

The loop is not absolute. The California Attorney General has continuing oversight rights over certain structural changes, receives advance notice of specified changes, can retain experts, and disputes under the MOU can be taken to court. The MOU also places the SSC at the nonprofit level and gives it an effective approval right over safety/security actions.

So the OpenAI architecture is best described as:

**self-renewing internal mission selector + meaningful but bounded external legal oversight.**

## Finding 2 — Anthropic's guardian is also self-renewing, but financially insulated

Anthropic says its original Long-Term Benefit Trust trustees were chosen by the Anthropic board after a search. Trustees serve terms, and future trustees are elected by the trustees themselves. In 2026 Anthropic restated the mechanism: new trustees are selected by existing trustees in consultation with the company.

That produces another selector loop:

`initial company board -> initial trustees -> future trustees`

The important difference is that trustees are intentionally financially disinterested: they hold no Anthropic equity and do not share in profits.

The Trust can elect and remove Anthropic board members, eventually a majority. But its power is not irreversible: Anthropic disclosed failsafe provisions allowing sufficiently large stockholder supermajorities to change the Trust or its powers without trustee consent.

Primary source:
- https://www.anthropic.com/news/the-long-term-benefit-trust
- https://www.anthropic.com/news/ben-bernanke

Classification:

**self-renewing mission selector + financial insulation + shareholder failsafe.**

## Finding 3 — institutional independence is not the same as epistemic independence

A concrete personnel bridge now exists across rival-lab governance and government AI-safety institutions.

Paul Christiano:

1. was an initial Anthropic Long-Term Benefit Trust trustee;
2. left the Trust in 2024 to work at the U.S. AI Safety Institute / successor CAISI;
3. joined the OpenAI Foundation Board and its Safety and Security Committee in September 2026.

Primary sources:
- Anthropic LTBT history: https://www.anthropic.com/news/the-long-term-benefit-trust
- OpenAI appointment: https://openai.com/index/paul-christiano-joins-openai-foundation-board/

This is **not evidence of secret coordination**. It is evidence that the pool of people trusted to interpret frontier-AI safety missions is small and institutionally mobile.

Therefore:

> Two governance bodies can be legally independent while drawing from a shared epistemic/professional network.

That distinction must be measured rather than assumed away.

## Finding 4 — Meta is the opposite selector topology

Meta's 2026 proxy states that Mark Zuckerberg held about 60.8% of total voting power while owning almost all Class B shares. The company explicitly says its dual-class structure concentrates control and limits other shareholders' ability to influence corporate matters.

Primary source:
- https://www.sec.gov/Archives/edgar/data/1326801/000162828026025532/meta-20260416.htm

This is a different architecture:

**founder-dominant mission selector.**

It is useful as a control because it shows that governance concentration does not require a nonprofit or safety trust.

## Selector-topology model

At least four mission-interpreter architectures now matter:

1. **Self-renewing board loop** — current guardians substantially choose future guardians.
2. **Founder-dominant loop** — a founder controls enough voting power to determine governance outcomes.
3. **Trust loop with financial insulation** — guardians choose successors but are economically separated from the operating company.
4. **External legal guardian** — regulator, court, statute or contract can block or punish a mission interpretation from outside the organization.

These mechanisms can coexist.

## New hypothesis

The strongest emerging hypothesis is no longer merely `constraint migration`.

It is:

> **High-level mission language is most durable when the people who interpret it are selected by a closed or semi-closed succession mechanism, while operational constraints beneath that mission can migrate substantially without forcing a change in the guardian layer itself.**

This could be healthy institutional memory, path dependence, epistemic homogeneity, or some mixture. The mechanism alone does not identify motive.

## Strong discriminator

Do not ask only whether a board or trust is formally independent.

Ask:

- Who selected the first guardians?
- Who selects their successors?
- Can outsiders nominate or remove them?
- Are selectors financially coupled to the company?
- Can the guardian be overridden, and by whom?
- Does the successor pool include materially divergent views with real power?
- When a principle becomes costly, does the guardian layer itself change, or only the rule below it?

## What would weaken this model

The model weakens if major frontier-AI organizations repeatedly install mission guardians who are selected independently of incumbent boards, founders, investors, major funders and the established AI-safety/governance network, give those guardians durable veto or appointment authority, and then allow them to use that authority against a material organizational preference without being overridden.

## Current status

The important result is not that frontier-AI governance is "captured." That conclusion is unsupported.

The result is narrower and stronger:

**mission governance is often recursively selected, and formal institutional independence can coexist with professional and epistemic overlap.**

That creates a measurable mechanism for frame persistence even without central coordination.
