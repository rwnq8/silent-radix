# DEEP-READ: Ranked Core Paper List
## Project: number-theory-ultrametric-deep
**Date:** 2026-07-03 | **Source:** 216 papers across 7 pillars + supplementary searches

---

## Executive Summary

From 216 papers aggregated across preprint API searches for all 7 pillars, I identify 12 high-priority papers for deep reading, organized by relevance to the project's research questions. The selection prioritizes: (a) papers that directly connect number theory to physical or quantum contexts, (b) foundational exposition on key mathematical tools (Fontaine theory, Dieudonné modules, Néron models, isogeny graphs), and (c) recent work (post-2020) in active areas. Papers with no quantum/physics connection are marked "mathematical foundation — read abstract only."

**Key finding:** No paper in any search directly connects class field theory, p-adic Hodge theory, or the Langlands program to quantum error correction. This confirms the research gap the project seeks to fill. The reading list therefore emphasizes mathematical foundations that the project must build upon.

---

## Tier 1: Must Read (Directly Relevant to Multiple Pillars)

### 1. Dragovich, B. (2000) — "On Adelic Strings"
- **Preprint:** hep-th/0005200v1
- **Relevance:** Pillars II, IV — The ONLY paper in the entire corpus that connects adelic mathematics to a physical theory (string theory). Uses adelic product formula to construct a unified description across all completions. This is the closest existing work to the project's Hasse principle for quantum codes (Pillar II) and adelic measurement framework (Pillar IV).
- **Why read:** Understand the existing paradigm for applying adeles to physics. The Dragovich approach (adelic strings) may suggest how to structure the quantum code analog. Also: Dragovich's 2001 follow-up "Adelic Strings and Noncommutativity" (hep-th/0105103v1).

### 2. Marcolli, M. (2025) — "Adelic Models of Percolation"
- **Preprint:** 2508.07601v2
- **Relevance:** Pillars II, V — Recent (2025) paper from a Fields-Medal-contributing mathematical physicist. Applies adelic methods to percolation — a statistical physics model. The structural analogy (adelic method → statistical physics) is the closest template for the project's goal (adelic method → quantum codes).
- **Why read:** Marcolli is a leading figure in mathematical physics at the intersection of number theory and geometry. Her approach to "adelic models" of physical systems is the most credible precedent for the project.

### 3. Chen, L., Liu, X. et al. (2021) — "Bending the Bruhat-Tits Tree II: the p-adic BTZ Black Hole and Local D..."
- **Preprint:** 2102.12024v2
- **Relevance:** Pillars I, VII — Direct application of Bruhat-Tits trees to physics (BTZ black holes in 3D gravity). The BT building serves as the geometric backdrop for a physical theory. This is the type of bridge the project seeks to build.
- **Why read:** Demonstrates a working methodology: BT tree → physical theory. Understanding this template will inform how to map BT buildings to quantum code spaces.

---

## Tier 2: High Priority (Foundational Mathematics for Active Pillars)

### 4. Frenkel, E. (2005) — "Lectures on the Langlands Program and Conformal Field Theory"
- **Preprint:** hep-th/0512172v1
- **Relevance:** Pillar VII — Accessible lectures connecting the Langlands program to physics (CFT). Essential for understanding how the Langlands correspondence might connect to quantum codes, since CFT provides the mathematical framework for topological codes (anyons).
- **Why read:** Before attempting RQ7.8 (geometric Langlands for topological codes), understand the existing Langlands-physics bridge.

### 5. Emerton, M., Gee, T. et al. (2022) — "An introduction to the categorical p-adic Langlands program"
- **Preprint:** 2210.01404v5
- **Relevance:** Pillar VII — Recent (2022) exposition of the modern categorical formulation of p-adic Langlands. This is the mathematical framework that the RQ7.3-7.7 conjectures would need to engage with.
- **Why read:** The project's Langlands conjectures (RQ7.6-7.8) need to be stated in terms compatible with current mathematical practice. This paper provides that vocabulary.

### 6. Lau, E. (2008, 2010) — "A duality theorem for Dieudonne displays" + "A relation between Dieudonne displays and crystalline Dieudonne theory"
- **Preprints:** 0807.4051v1, 1006.2720v4
- **Relevance:** Pillar VI — Foundational exposition on Dieudonné modules and displays. The Dieudonné module is the central object of Pillar VI. Understanding its structure is essential before attempting to assign one to a stabilizer code (RQ6.1-6.3).
- **Why read:** The project's Dieudonné module conjecture (definition in §6 of definitions.tex) requires working knowledge of what a Dieudonné module actually is. Lau's papers are standard references.

### 7. Pop, H.C. (1997) — "Row-reducing the quantum determinant and Dieudonne determinant"
- **Preprint:** q-alg/9703003v1
- **Relevance:** Pillar VI — The only paper that references both "quantum" (in the quantum group sense) and "Dieudonné determinant." While about quantum groups rather than quantum codes, the methodology of applying Dieudonné determinants to quantum algebraic structures is instructive.
- **Why read:** A rare bridge paper. Understand the approach to see if the methodology generalizes to quantum codes.

---

## Tier 3: Important Background (Pillar-Specific Foundations)

### 8. Goldring, W., Nicole, M-H. (2013) — "The μ-ordinary Hasse invariant of unitary Shimura varieties"
- **Preprint:** 1305.6956v2
- **Relevance:** Pillars II, III — Hasse invariants are the mathematical object that the project's Hasse principle analog (Pillar II, RQ2.2) would need to generalize. This paper connects Hasse invariants to Shimura varieties (which appear in the Langlands program — Pillar VII).
- **Why read:** Understand what a "Hasse invariant" actually is mathematically, as a template for what the "quantum code Hasse invariant" might be.

### 9. Jarossay, D. (2015, 2016) — p-adic Cyclotomic Multiple Harmonic Sums
- **Preprints:** 1501.04893v6 (Pro-unipotent harmonic actions), 1610.09107v3 (Dynamical properties)
- **Relevance:** Pillar IV — The most computationally-oriented papers on p-adic cyclotomic structures. Jarossay's work on pro-unipotent actions directly engages with the p-adic Galois theory that underlies the project's class field theory analog (Pillar IV, RQ4.1-4.2).
- **Why read:** These are the papers most likely to contain concrete computational methods that can be adapted for the Phase 2 prototypes (Mahler spectrum, local invariants).

### 10. Colò, L., Kohel, D. (2020) — "Orienting supersingular isogeny graphs"
- **Preprint:** 2012.10803v1
- **Relevance:** Pillar V — Isogeny graphs are the mathematical infrastructure for the Pillar V conjecture (RQ5.3: isogeny path = code-switching protocol). Understanding how isogeny graphs are oriented (given direction) is essential for mapping them to directed code-switching sequences.
- **Why read:** The "orientation" problem in isogeny graphs may correspond to the "directionality" of code-switching operations. Also: Florit & Smith (2021) on automorphisms and Richelot isogeny graph atlas — companion papers.

### 11. Wingberg, K. (2000) — "On the Fontaine-Mazur Conjecture for CM-Fields"
- **Preprint:** math/0007210v1
- **Relevance:** Pillar III — Direct engagement with the Fontaine-Mazur conjecture, which the project proposes as an analog criterion for physical realizability of quantum codes (RQ3.1, Fontaine-Mazur analog conjecture).
- **Why read:** Understand what the Fontaine-Mazur conjecture actually says and what evidence supports it, to assess whether an analog for quantum codes is plausible.

### 12. Suzuki, T. (2018) — "Neron models of 1-motives and duality"
- **Preprint:** 1806.07641v4
- **Relevance:** Pillar V — The most recent paper on Néron models for motives (generalizations of abelian varieties). The "duality" aspect may connect to the code-duality operations in stabilizer codes.
- **Why read:** Together with Orecchia (2019, 1904.03886v1 — monodromy criterion for Néron model existence), these papers provide the mathematical vocabulary for the Kodaira-Néron degeneration conjecture (RQ5.1).

---

## Papers to Skim (Read Abstract Only)

These papers are mathematically relevant but their connection to the project's specific research questions is indirect:

| Paper | Year | ID | Why Skim |
|:------|:-----|:---|:---------|
| Murtagh — Ultrametric Model of Mind I, II | 2012 | 1201.2711v3, 1201.2719v3 | Ultrametric methodology, not number theory |
| Remy, Thuillier — BT buildings and analytic geometry | 2011 | 1110.1362v3 | BT → analytic geometry bridge |
| Ben-Zvi, Chen — Coherent/Constructible Langlands | 2023 | 2302.00039v1 | Modern Langlands — too advanced for Phase 2 |
| Etingof, Frenkel — Analytic Langlands | 2023 | 2311.03743v2 | Modern Langlands — too advanced |
| Caraiani, Shin — Langlands reciprocity for GL_n | 2023 | 2311.13382v1 | Shimura variety techniques — advanced |
| Zhu — Coherent sheaves on Langlands parameters | 2020 | 2008.02998v3 | Stack-theoretic Langlands — too advanced |
| Rüd, Bu — Projective Twist on Hasse Norm Theorem | 2024 | 2410.11159v1 | Recent Hasse technique, abstract only |
| Florit, Smith — Richelot isogeny graph atlas | 2021 | 2101.00917v2 | Isogeny graph classification |
| Orecchia — Monodromy criterion for Neron models | 2019 | 1904.03886v1 | Companion to Suzuki (2018) |
| Adams, Bogner, Weinzierl — The Elliptic Sunrise | 2015 | 1510.03883v1 | Elliptic curve mathematics |

---

## Priority by Pillar (for Session Planning)

| Session | Pillar(s) | Papers to Read | Estimated Time |
|:--------|:----------|:---------------|:---------------|
| 1 | I, IV | Dragovich (2000), Marcolli (2025), Jarossay (2015, 2016) | 2-3 hours |
| 2 | II, VII | Goldring (2013), Chen (2021), Frenkel (2005), Emerton (2022) | 2-3 hours |
| 3 | III, VI | Wingberg (2000), Lau (2008, 2010), Pop (1997) | 2-3 hours |
| 4 | V | Colò (2020), Suzuki (2018), Florit & Smith (2021) | 1-2 hours |

---

## Cross-Reference: Silent-Radix Paper Findings

The silent-radix synthesis paper (radix-uw-bt-synthesis, published 2026-07-02, DOI: 10.5281/zenodo.21134188) provides two concrete results that directly inform the deep-read:

1. **Ultrametric stability:** The Wheeler-DeWitt constrained spin glass ensemble is RS-stable across βJ ∈ [1, 30], with the AT eigenvalue never crossing zero. This 10-15× suppression of replica symmetry breaking demonstrates that ultrametric constraints act as a rigid structural backbone — a physical manifestation that the project's conjectured number-theoretic constraints might also enforce geometric stability on quantum code spaces.

2. **p-adic distance is nontrivial only for primes p ≤ 23** in the D=4 Fourier clock system. This provides a concrete bound for Pillar II (Hasse principle): local quantum codes may only be interesting/vary meaningfully for the first ~9 primes. The project's definition of "local quantum code at p" (§2 of definitions.tex) should be calibrated to test whether p-adic distance variation of codes follows the same p ≤ 23 pattern.

3. **Spencer-Brown's calculus of indications** provides a non-archimedean foundation that the paper argues unifies ultrametric geometry and measurement theory. This may inform the foundational philosophy of the project but is not directly testable as a mathematical conjecture.

---

*Deep-read list v1.0 — 2026-07-03. Companion to LITERATURE-BRIEF.md and definitions.tex.*
