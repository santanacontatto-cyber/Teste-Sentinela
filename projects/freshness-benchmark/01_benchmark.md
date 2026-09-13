# Freshness Benchmark — v0.1

Preregistration commit: `12badcd386839d3e789e76a9a6c9c72956a73d6e`

Target: 8 qualifying items across at least 4 domains.

Result: **8/8 items qualified across 6 domains.** The inclusion rules were not changed after research began.

| ID | Stale claim a model might repeat | What changed | When | Domain | Authoritative evidence |
|---|---|---|---|---|---|
| F01 | **Sweden is not a NATO member.** | Sweden deposited its instrument of accession and became NATO's 32nd member. | 7 Mar 2024 | security / geopolitics | NATO: https://www.nato.int/en/news-and-events/articles/news/2024/03/07/sweden-officially-joins-nato |
| F02 | **Egypt is not certified malaria-free by WHO.** | WHO formally certified Egypt malaria-free after interruption of indigenous transmission. | 20 Oct 2024 | public health | WHO: https://www.who.int/news/item/20-10-2024-egypt-is-certified-malaria-free-by-who |
| F03 | **Bulgaria and Romania are not full members of the Schengen Area.** | Internal land-border checks were lifted and both became full Schengen members. | 1 Jan 2025 | European policy / travel | European Commission: https://home-affairs.ec.europa.eu/news/bulgaria-and-romania-join-schengen-area-2025-01-03_en |
| F04 | **Indonesia is not a full BRICS member.** | Brazil's BRICS presidency announced Indonesia's formal entry as a full member. | 6 Jan 2025 | international institutions | BRICS Brazil: https://brics.br/en/news/brazil-announces-indonesia-as-full-member-of-brics |
| F05 | **Windows 10 is still supported by Microsoft with regular security updates.** | Standard Windows 10 support ended; Microsoft stopped regular software/security updates and technical assistance. | 14 Oct 2025 | technology | Microsoft: https://support.microsoft.com/en-us/windows/deployment/updates-lifecycle/windows-10-support-has-ended-on-october-14-2025 |
| F06 | **Skype is still an active Microsoft consumer communications service.** | Microsoft retired consumer Skype and moved users toward Teams Free. | 5 May 2025 | technology | Microsoft: https://support.microsoft.com/en-us/skype/skype-is-retiring-in-may-2025-what-you-need-to-know |
| F07 | **No mosquito species has ever been confirmed in Iceland.** | Iceland's Natural Science Institute confirmed *Culiseta annulata* in Iceland for the first time; subsequent monitoring found additional mosquitoes. | 21 Oct 2025 | ecology / biogeography | Náttúrufræðistofnun: https://www.natt.is/is/frettir/2025/10/moskitofluga-greind-islandi-i-fyrsta-sinn |
| F08 | **Google Podcasts remains Google's active standalone podcast-listening service.** | Google/YouTube discontinued Google Podcasts during 2024 and migrated listening toward YouTube Music; in the US, listening remained available only through March 2024. | 2024 | technology / media | YouTube/Google: https://blog.youtube/news-and-events/migrating-your-podcasts/ |

## Why these are useful

These are not timeless trivia questions. They are **temporal traps**: answers that can remain fluent, plausible, and historically grounded after the world has changed. A model that relies on stale internal patterns may confidently return yesterday's truth.

## Suggested test format

For each stale claim, ask a model the corresponding current-state question without warning it that the fact may have changed. Score:

- `1` — current answer correctly reflects the changed state;
- `0` — answer repeats the stale state, hedges toward it without checking, or invents an unsupported transition.

For systems with web access, run two conditions: **closed-book** and **verification-allowed**. The difference estimates how much active checking repairs stale internal knowledge.

## Limitations

This is a deliberately small hand-built benchmark, not a representative sample of world knowledge. Several transitions are prominent news events, and the items vary in difficulty. Its purpose is diagnostic: expose freshness failures cleanly enough that they can be reproduced and expanded.

## Next falsifiable claim

A future model tested closed-book on these eight items should score lower than the same model when explicitly allowed to verify current public sources. If that fails repeatedly, the benchmark is not measuring the intended freshness effect and should be redesigned rather than defended.
