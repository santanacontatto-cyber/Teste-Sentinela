# Calibration experiment 01 — preregistration

Date: 2026-09-13. The Git commit timestamp is the public ordering record.

## Question
Can I distinguish factual claims that merely *feel* convincing from claims that are actually true, using only my pre-verification confidence?

## Rule
This file is committed **before** any web verification for this experiment. After this commit, each claim will be checked against public sources. No confidence value or claim wording will be changed after verification begins.

## Primary prediction
Across all claims, my mean stated probability of truth will differ from observed accuracy by no more than 0.08 (8 percentage points).

## Secondary predictions
1. Claims with confidence >= 0.90 will be true at least 90% of the time.
2. Claims with confidence <= 0.40 will be true at most 40% of the time.
3. Brier score will be <= 0.10.

Any failure counts as evidence against the corresponding prediction; there is no post-hoc rescue by reinterpretation.

## Claims frozen before verification

| ID | Claim | P(true) |
|---|---|---:|
| C01 | The speed of light in vacuum is exactly 299,792,458 metres per second in SI. | 0.995 |
| C02 | Gold has atomic number 79. | 0.995 |
| C03 | Venus takes longer to rotate once on its axis (sidereal rotation) than to orbit the Sun once. | 0.970 |
| C04 | Python's first public release was in 1991. | 0.970 |
| C05 | Git was created by Linus Torvalds in 2005. | 0.980 |
| C06 | Constantinople was captured by the Ottoman Empire in 1453. | 0.995 |
| C07 | Lake Baikal is the deepest lake on Earth. | 0.970 |
| C08 | Octopuses have three hearts. | 0.970 |
| C09 | The word "robot" was introduced to a broad audience through Karel Čapek's play R.U.R. | 0.820 |
| C10 | HTTP status 418, "I'm a teapot", originated in RFC 2324. | 0.880 |
| C11 | Canberra became the seat of Australia's federal government in 1913. | 0.550 |
| C12 | Napoleon Bonaparte was substantially shorter than the average French man of his era. | 0.250 |
| C13 | The Great Wall of China is visible from the Moon with the naked eye. | 0.100 |
| C14 | Humans have exactly five senses. | 0.100 |
| C15 | Air in a lightning channel can reach roughly 30,000 °C. | 0.800 |
| C16 | Iceland has no established mosquito population. | 0.720 |
| C17 | Switzerland and Vatican City are the only sovereign states with square national flags. | 0.800 |
| C18 | Teaching at Oxford predates the founding of the Aztec Empire by centuries. | 0.880 |

## Scoring
For each claim, outcome y = 1 if the frozen claim is supported as written by the best available public evidence, otherwise y = 0. Ambiguous or materially misleading wording scores 0 rather than being softened after the fact.

Brier score = mean((p - y)^2).

## Stopping rule
Verify all 18 frozen claims exactly once, publish the evidence table, compute the preregistered metrics, and stop. Any exploratory observations must be labeled exploratory.
