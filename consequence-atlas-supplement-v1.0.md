# CONSEQUENCE ATLAS SUPPLEMENT: 15 Additional Entries

**Part of the Silent Radix Research Program**
**Version 1.0 — 2026-06-29**

---

## Section F: Additional Scientific and Statistical (Entries 51–58)

### F-1: The $p$-value Dichotomization — 0.05 as Magic Threshold

| Field | Detail |
|:------|:-------|
| **Frame Violated** | Silent Scale Type (variant: silent threshold) |
| **Domain** | All empirical sciences |
| **Symptom** | Results with $p = 0.049$ are treated as "significant" while $p = 0.051$ is "non-significant." The threshold 0.05 is a silent, arbitrary convention treated as an ontological boundary. |
| **Root Cause** | Fisher's original suggestion of 0.05 as a "convenient" threshold was reified over decades into a dichotomous decision rule. The continuous $p$-value was binarized without acknowledging that 0.05 is a convention, not a law. |
| **Severity** | **CRITICAL** — Replication crisis central driver |
| **Real Incidents** | ASA (2016) statement: "The widespread use of 'statistical significance' as a license for making a claim of a scientific finding leads to considerable distortion of the scientific process." |
| **Detection** | Report exact $p$-values, not inequalities; use confidence intervals and Bayes factors. |
| **Fix** | Abandon the "significance" dichotomization; report continuous measures of evidence with explicit threshold justifications if thresholds are used. |

### F-2: Berkson's Paradox — Selection Bias via Silent Conditioning

| Field | Detail |
|:------|:-------|
| **Frame Violated** | Silent Frame (general — silent conditioning) |
| **Domain** | Epidemiology, econometrics, social science |
| **Symptom** | Studying only hospitalized patients (a selected sample) induces a spurious negative correlation between diseases that are independently distributed in the general population. The conditioning event is a silent parameter. |
| **Root Cause** | Berkson (1946): when both exposure and outcome affect selection into the sample, conditioning on selection induces collider bias. The selection criterion is a hidden frame on the data. |
| **Severity** | **HIGH** — Spurious causal conclusions |
| **Real Incidents** | COVID-19 studies using only hospitalized patients found protective effects of smoking — a Berkson's paradox artifact (Griffith et al., 2020). |
| **Detection** | DAG (Directed Acyclic Graph) analysis; explicit documentation of selection criteria. |
| **Fix** | Report selection mechanism; use inverse probability weighting or Heckman correction when selection is non-random. |

### F-3: Simpson's Paradox — Aggregation Reversal

| Field | Detail |
|:------|:-------|
| **Frame Violated** | Silent Frame (silent grouping structure) |
| **Domain** | All data-driven fields |
| **Symptom** | A trend that appears in aggregated data reverses or disappears when data is disaggregated by a lurking variable. The grouping variable is a silent frame. |
| **Root Cause** | Simpson (1951): when groups have different sizes and baseline rates, aggregation can produce a trend opposite to the within-group trends. The choice of aggregation level is a hidden parameter. |
| **Severity** | **CRITICAL** — Policy, medicine, and legal decisions |
| **Real Incidents** | UC Berkeley gender bias case (Bickel et al., 1975): aggregate data showed bias against women, but department-level data showed no bias — women applied to more competitive departments. |
| **Detection** | Always disaggregate by plausible confounders before drawing conclusions. |
| **Fix** | Report both aggregated and disaggregated results; use multilevel models that explicitly model the grouping structure. |

### F-4: Base Rate Fallacy — Silent Prior Probability

| Field | Detail |
|:------|:-------|
| **Frame Violated** | Silent Radix (variant: silent base rate) |
| **Domain** | Medicine, law, risk assessment |
| **Symptom** | A test with 95% accuracy produces a positive result. The patient is told they have a 95% chance of having the disease — ignoring that the disease prevalence (base rate) is 0.1%. The true positive predictive value is only ~1.9%. |
| **Root Cause** | Bayes' theorem: $P(D|+) = P(+|D)P(D) / P(+)$. The prior $P(D)$ is a silent parameter — the "base" of the probability calculation, analogous to the radix of a numeral. |
| **Severity** | **CRITICAL** — Medical misdiagnosis, legal wrongful conviction |
| **Real Incidents** | Mammogram interpretation: doctors and patients routinely overestimate cancer probability from a positive mammogram because the low base rate is ignored (Gigerenzer, 2002). |
| **Detection** | Require base rate to be stated alongside every conditional probability. |
| **Fix** | Present probabilities in natural frequencies ("1 in 1000 have the disease; of those, 950 test positive; of the 999 without, 50 test positive → 950/1000 positive tests are true positives"). |

### F-5: The Texas Sharpshooter Fallacy — Clustering Illusion

| Field | Detail |
|:------|:-------|
| **Frame Violated** | Silent Frame (silent hypothesis space) |
| **Domain** | Epidemiology, geography, data mining |
| **Symptom** | After observing a cancer cluster in a town, researchers draw a target around it and declare significance — ignoring that with enough towns, some clusters are expected by chance alone. The hypothesis was generated by the data, not prior to it. |
| **Root Cause** | Multiple comparisons problem without correction. The "target" (the set of hypotheses tested) is a silent parameter. |
| **Severity** | **HIGH** — Public panic, misallocated resources |
| **Real Incidents** | Cancer cluster investigations that find "significant" clusters post-hoc without correcting for the number of locations examined. |
| **Detection** | Pre-register hypotheses; use spatial scan statistics with proper multiple-testing correction. |
| **Fix** | Apply Bonferroni, FDR, or permutation-based corrections for the full hypothesis space considered. |

### F-6: Confirmation Bias in Numeric Interpretation

| Field | Detail |
|:------|:-------|
| **Frame Violated** | Silent Frame (silent prior belief) |
| **Domain** | Cognitive psychology, science, policy |
| **Symptom** | The same numeric result ($d = 0.3$) is interpreted as "promising" by advocates and "negligible" by skeptics. The prior belief frame is a silent parameter coloring interpretation. |
| **Root Cause** | Motivated reasoning: people evaluate evidence strength based on whether it supports their prior beliefs. The numeric effect size is constant; the interpretation varies with the unstated frame. |
| **Severity** | **MEDIUM-HIGH** — Policy polarization, scientific disputes |
| **Real Incidents** | Climate change debates where identical temperature data is interpreted as "alarming trend" or "natural variability." |
| **Detection** | Pre-register interpretation criteria before seeing results. |
| **Fix** | Separate result reporting from interpretation; report effect sizes with pre-specified thresholds for "meaningful" vs. "negligible." |

### F-7: The Prosecutor's Fallacy — Transposed Conditional

| Field | Detail |
|:------|:-------|
| **Frame Violated** | Silent Scale Type (probability direction inversion) |
| **Domain** | Law, forensic science |
| **Symptom** | "The probability that the DNA matches by chance is 1 in a million, so there's a 1 in a million chance the defendant is innocent." This transposes $P(\text{match} \mid \text{innocent})$ with $P(\text{innocent} \mid \text{match})$. |
| **Root Cause** | The conditional probability direction is a silent parameter. $P(A|B) \neq P(B|A)$ in general, but the verbal form "the probability that..." obscures which is the condition and which is the event. |
| **Severity** | **CRITICAL** — Wrongful convictions |
| **Real Incidents** | R v. Sally Clark (1999): expert testified that probability of two SIDS deaths in one family was 1 in 73 million, which the jury interpreted as probability of innocence. Conviction later overturned. |
| **Detection** | Require Bayesian formulation of all forensic probability statements. |
| **Fix** | State: "If the defendant were innocent, the probability of observing this DNA match is X. This is not the probability the defendant is innocent." |

### F-8: McNamara Fallacy — What Gets Measured Gets Managed

| Field | Detail |
|:------|:-------|
| **Frame Violated** | Silent Scale Type (measurable proxy mistaken for target) |
| **Domain** | Management, policy, education |
| **Symptom** | "Body count" as measure of success in Vietnam War (McNamara). Student test scores as measure of educational quality. GDP as measure of national well-being. The measurable proxy replaces the actual goal without acknowledging the substitution. |
| **Root Cause** | The decision to measure a particular quantity is a frame choice — selecting what counts. When the frame becomes invisible, the proxy is reified as the goal. |
| **Severity** | **CRITICAL** — Policy distortion at scale |
| **Real Incidents** | Campbell's Law: "The more any quantitative social indicator is used for social decision-making, the more subject it will be to corruption pressures." Teaching to the test; hospitals refusing high-risk patients to improve mortality statistics. |
| **Detection** | Always state what is NOT being measured alongside what is. |
| **Fix** | Use multiple metrics; regularly audit whether the proxy is still aligned with the goal; rotate metrics to prevent gaming. |

---

## Section G: Additional Temporal and Mixed-Radix (Entries 59–63)

### G-1: The Leap Second — Earth Rotation vs Atomic Time

| Field | Detail |
|:------|:-------|
| **Frame Violated** | Silent Radix (incommensurable cycles) |
| **Domain** | Global timekeeping, computing |
| **Symptom** | Atomic time (TAI) and astronomical time (UT1) diverge because Earth's rotation is irregular. Leap seconds are inserted to reconcile them, but software systems that assume a uniform 86400-second day break when a leap second occurs. |
| **Root Cause** | Two natural cycles (Earth rotation and atomic oscillation) are incommensurable. The UTC time standard is a mixed-radix system with an irregularly varying component — but software treats it as a uniform system. |
| **Severity** | **HIGH** — System crashes, financial trading halts |
| **Real Incidents** | 2012 leap second crashed Reddit, Gawker, Mozilla, and disrupted Qantas Airways' reservation system. 2015 and 2016 leap seconds caused similar failures. |
| **Detection** | Test systems with simulated leap seconds; use `CLOCK_MONOTONIC` for interval timing. |
| **Fix** | Smear the leap second over a longer period (Google's "leap smear"); or abolish leap seconds (proposed for 2035). |

### G-2: The International Date Line — Longitude as Discontinuous Time

| Field | Detail |
|:------|:-------|
| **Frame Violated** | Silent Radix (cyclic crossing boundary) |
| **Domain** | Navigation, communication, computing |
| **Symptom** | Crossing the International Date Line causes a discontinuous ±1 day shift in calendar date while the continuous time flow is unchanged. Software that models time as a linear coordinate breaks at the discontinuity. |
| **Root Cause** | The Earth's rotation is a cycle; the zero-longitude meridian (Greenwich) is an arbitrary origin. The Date Line is the point where the cycle wraps around — a boundary artifact of projecting a cyclic phenomenon onto a linear coordinate. |
| **Severity** | **MEDIUM** — Scheduling, logistics |
| **Real Incidents** | Flight booking systems that show incorrect arrival dates; military planning errors across the Pacific. |
| **Detection** | Test all time-zone and date-line edge cases in software. |
| **Fix** | Use UTC internally; convert to local time with explicit zone only at display; test circular data handling. |

### G-3: Epoch Time Zero — The 1970 Assumption

| Field | Detail |
|:------|:-------|
| **Frame Violated** | Silent Radix (silent epoch) |
| **Domain** | All computing |
| **Symptom** | Every UNIX timestamp is "seconds since 1970-01-01T00:00:00Z." The epoch is a silent parameter carried in every timestamp. Systems that store timestamps as integers without epoch metadata are vulnerable when the epoch convention changes or is misunderstood. |
| **Root Cause** | The epoch choice (1970-01-01) was arbitrary — chosen for pragmatic reasons (recent, aligned with UTC). But like the radix, the epoch is a frame that determines interpretation and is not carried with the data. |
| **Severity** | **POTENTIALLY CATASTROPHIC** — Year 2038 problem |
| **Real Incidents** | GPS epoch (1980-01-06) differs from UNIX epoch (1970-01-01). Systems that mix GPS and UNIX timestamps without conversion produce 10-year offset errors. |
| **Detection** | Always annotate timestamps with epoch metadata. |
| **Fix** | ISO 8601 with explicit epoch: `2026-06-29T00:00:00Z`; store epoch alongside integer representations. |

### G-4: The 12-Hour Clock — AM/PM Ambiguity

| Field | Detail |
|:------|:-------|
| **Frame Violated** | Silent Radix (silent half-day cycle) |
| **Domain** | Universal timekeeping |
| **Symptom** | "12:00" means noon or midnight. "12:00 AM" is ambiguous — some interpret it as midnight, others as noon. The AM/PM marker is an incomplete frame that doesn't fully resolve the cycle. |
| **Root Cause** | The 12-hour clock is a mixed-radix system (12:60) with an ambiguous modulus. The half-day cycle (AM/PM) is a poor frame — it fails at the boundary (12:00). |
| **Severity** | **MEDIUM-HIGH** — Medical scheduling, transportation |
| **Real Incidents** | Medication errors: patients receiving 12-hour doses at wrong time due to AM/PM confusion; hospital protocols now mandate 24-hour time. |
| **Detection** | Hospital policy: always use 24-hour time for critical scheduling. |
| **Fix** | Use 24-hour clock (ISO 8601) for all critical systems: `14:00`, not `2:00 PM`. |

### G-5: Fiscal Week Numbering — ISO 8601 vs US Convention

| Field | Detail |
|:------|:-------|
| **Frame Violated** | Silent Radix (silent week origin) |
| **Domain** | Business, logistics, international trade |
| **Symptom** | ISO 8601 defines week 1 as the week containing the first Thursday of the year. The US convention starts week 1 on January 1. A date in early January can be in different week numbers depending on the convention. |
| **Root Cause** | The week is a 7-day cycle. The origin (first week of the year) is a silent parameter. Different conventions choose different anchoring rules. |
| **Severity** | **MEDIUM** — Supply chain, financial reporting |
| **Real Incidents** | International logistics: a shipment scheduled for "week 1" arrives in the wrong week because sender and receiver use different week numbering conventions. |
| **Detection** | Always specify the week numbering convention: ISO 8601 week or US week. |
| **Fix** | Use ISO 8601 week dates: `2026-W27-1` (Monday of week 27, 2026). |

---

## Section H: Additional Cognitive and Educational (Entries 64–65)

### H-1: The Number-Word Length Effect — Phonological Loop Interference

| Field | Detail |
|:------|:-------|
| **Frame Violated** | Silent Radix (representation-dependent cognition) |
| **Domain** | Cognitive psychology, cross-cultural studies |
| **Symptom** | Chinese-speaking children outperform English-speaking children on digit span tasks because Chinese number words are shorter (monosyllabic: yi, er, san vs. one, two, three). The phonological loop can hold more items when words are shorter. |
| **Root Cause** | The linguistic representation of numbers (word length) is a silent parameter affecting cognitive capacity. The number is the same; the *representation* of the number changes what the mind can do. |
| **Severity** | **MEDIUM** — Cross-cultural comparison bias |
| **Real Incidents** | Cross-national IQ comparisons using digit span are confounded by language differences; the measured "ability" partly reflects the representation system, not pure cognition. |
| **Detection** | Control for language representation in cross-cultural cognitive tests. |
| **Fix** | Use non-linguistic number tasks (dot enumeration, approximate number system) for cross-cultural comparison. |

### H-2: The Positional Notation Learning Barrier — Place Value as "Magic"

| Field | Detail |
|:------|:-------|
| **Frame Violated** | Silent Radix (the base is never explained) |
| **Domain** | Mathematics education |
| **Symptom** | Children are taught to write "10" after "9" without explanation that the "1" means "one group of ten." The carry operation is taught as a rote procedure ("carry the one") without the underlying tree structure being made visible. |
| **Root Cause** | Positional notation is introduced as an opaque symbolic system. The base (10) is the number of available digits, but this is rarely stated explicitly to young learners. The tree structure — the most intuitive part — is hidden behind the algorithm. |
| **Severity** | **HIGH** — Foundational mathematics education |
| **Real Incidents** | Students who can perform multi-digit arithmetic correctly but cannot explain what the "1" in "15" means (Ma, 1999: "Knowing and Teaching Elementary Mathematics"). |
| **Detection** | Diagnostic: ask students "In the number 25, what does the 2 mean?" — errors reveal place-value opacity. |
| **Fix** | Dienes blocks, Montessori golden beads, and explicit base-labeled place-value charts from the earliest instruction; teach the tree before the algorithm. |

---

## Statistical Summary (Updated — 65 Total Entries)

| Frame Type | Count | Critical/Catastrophic | High | Medium | Low |
|:-----------|:-----:|:---------------------:|:----:|:------:|:---:|
| Silent Radix | 20 | 4 | 10 | 4 | 2 |
| Silent Metric | 10 | 3 | 4 | 2 | 1 |
| Silent Unit | 5 | 5 | 0 | 0 | 0 |
| Silent Scale Type | 9 | 4 | 2 | 2 | 1 |
| Silent Frame (general) | 6 | 2 | 3 | 1 | 0 |
| Mixed / Temporal | 15 | 6 | 5 | 3 | 1 |
| **TOTAL** | **65** | **24 (37%)** | **24 (37%)** | **12 (18%)** | **5 (8%)** |

---

*Consequence Atlas Supplement v1.0 — Part of the Silent Radix Research Program. [EXECUTED]*
