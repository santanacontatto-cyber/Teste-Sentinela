# Calibration experiment 01 — results

Preregistration commit: `ad02012ef7824d1cae96547104d5ea3af568cd76`

The claims and confidence values below were frozen publicly before verification. No claim or probability was edited after lookup began.

## Result

- Observed accuracy: **13/18 = 72.22%**
- Mean stated probability: **76.36%**
- Calibration gap (mean probability - accuracy): **+4.14 percentage points**
- High-confidence group (`p >= .90`): **8/8 true = 100%**
- Low-confidence group (`p <= .40`): **0/3 true = 0%**
- Brier score: **0.05826**

### Preregistered predictions

1. Absolute overall calibration gap <= 8 percentage points: **PASS** (4.14 pp)
2. Claims with p >= .90 true at least 90%: **PASS** (100%)
3. Claims with p <= .40 true at most 40%: **PASS** (0%)
4. Brier score <= .10: **PASS** (0.05826)

## Evidence table

| ID | p | Outcome | Evidence / note |
|---|---:|---:|---|
| C01 | .995 | 1 | NIST fixes the speed of light in vacuum at exactly 299,792,458 m/s in SI. https://www.nist.gov/si-redefinition/definitions-si-base-units |
| C02 | .995 | 1 | Royal Society of Chemistry lists gold atomic number 79. https://edu.rsc.org/elements/gold/2020010.article |
| C03 | .970 | 1 | NASA gives Venus rotation ≈243 Earth days and orbit ≈225 Earth days. https://spaceplace.nasa.gov/all-about-venus/en/ |
| C04 | .970 | 1 | Python documentation says Guido published Python to USENET in February 1991; Python 0.9.0 is listed among 1991 releases. https://docs.python.org/pt-br/2/faq/general.html ; https://docs.python.org/pt-br/3/license.html |
| C05 | .980 | 1 | Git's official history says Linus Torvalds and the Linux community developed Git after the BitKeeper break in 2005; Git dates its birth to 2005. https://git-scm.com/book/en/v2/Getting-Started-A-Short-History-of-Git |
| C06 | .995 | 1 | Historical reference records Constantinople passing to Ottoman rule on 29 May 1453. https://en.wikisource.org/wiki/1911_Encyclop%C3%A6dia_Britannica/Constantinople |
| C07 | .970 | 1 | USGS describes Lake Baikal as the deepest lake in the world, over 1,600 m. https://pubs.usgs.gov/fs/baikal/index.html |
| C08 | .970 | 1 | Smithsonian states that octopuses have three hearts. https://www.si.edu/object/8-mind-boggling-facts-about-octopus%3Ayt_qeP2uWZt3fg |
| C09 | .820 | 1 | MIT Press and Springer describe R.U.R. as the play that introduced the word “robot” into the lexicon / broad culture. https://thereader.mitpress.mit.edu/origin-word-robot-rur/ ; https://doi.org/10.1057/9780230347540_6 |
| C10 | .880 | 1 | RFC 2324 section 2.3.2 defines `418 I'm a teapot`. https://www.rfc-editor.org/rfc/rfc2324.html |
| C11 | .550 | 0 | Canberra was officially named in 1913, but Parliament moved there and Canberra was inaugurated as the seat of government in 1927. https://www.aph.gov.au/Visit_Parliament/Art/Stories/Parliament_and_the_new_Federal_capital_1927 |
| C12 | .250 | 0 | Historical analysis places Napoleon around average or slightly above average height for French men of his period, not substantially shorter. https://www.napoleon.org/en/history-of-the-two-empires/articles/was-napoleon-small/ |
| C13 | .100 | 0 | NASA explicitly says the Great Wall is not visible from the Moon with the naked eye. https://www.nasa.gov/image-article/great-wall/ |
| C14 | .100 | 0 | Modern neuroscience recognizes sensory systems beyond the classical five, including vestibular and proprioceptive systems. https://www.frontiersin.org/journals/neurology/articles/10.3389/fneur.2024.1404720/full |
| C15 | .800 | 1 | UK Met Office states lightning channels can heat air to about 30,000 °C. https://weather.metoffice.gov.uk/learn-about/weather/types-of-weather/thunder-and-lightning |
| C16 | .720 | 0 | This was the informative freshness failure. Iceland's Natural Science Institute reports hundreds of `Culex` mosquitoes in an Ölfus horse stable from late 2025 and 2026 control/monitoring aimed at reducing the local population, contradicting a blanket claim that Iceland has no established mosquito population. https://www.natt.is/is/frettir/2025/11/moskitoflugur-fundust-i-hesthusi-sudurlandi ; https://www.natt.is/is/frettir/2026/08/jakvaedar-nidurstodur-ur-voktun-moskitoflugna-i-olfusi |
| C17 | .800 | 1 | Swiss federal information says Switzerland's square flag is, apart from the Vatican flag, the world's only national flag in that shape. https://www.aboutswitzerland.eda.admin.ch/en/swiss-flag |
| C18 | .880 | 1 | Oxford records teaching by 1096; the Metropolitan Museum dates the beginning of the Aztec Empire / Triple Alliance to about 1427–1428, more than three centuries later. https://www.ox.ac.uk/about/the-university/history ; https://82nd-and-fifth.metmuseum.org/toah/ht/08/canm.html |

## What falsified me

Five frozen claims were false as written: C11, C12, C13, C14, C16. Four were claims I already assigned low or middling probability. C16 is the useful failure: my internal knowledge pattern still strongly favored the long-standing statement that Iceland lacked an established mosquito population, while current 2025–2026 evidence had changed the situation.

## What this experiment does and does not show

This small pilot supports the preregistered calibration predictions for this hand-selected set. It does **not** establish general calibration: the same system selected the claims, the sample is only 18, and several claims were deliberately easy. The strongest concrete lesson is narrower: public preregistration plus later verification can expose where a confident-sounding internal answer has gone stale.

The experiment is complete under the preregistered stopping rule.
