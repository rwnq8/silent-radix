# Hidden Assumptions and Consequences:
## The Seven-Pillar Deep Number Theory Framework for Ultrametric Quantum Information

**Document:** Critical analysis of `RESEARCH-PLAN.md` (v1.0, 2026-07-03)
**Status:** Pre-implementation audit | **Date:** 2026-07-03

---

## Executive Summary

The RESEARCH-PLAN for `number-theory-ultrametric-deep` proposes connecting seven foundational areas of modern number theory to quantum error correction, hierarchical discovery, and ultrametric memory. Every pillar rests on a core claim: *that a structural analogy between a specific domain of number theory and a specific aspect of quantum information is not merely suggestive but productive* — capable of generating new theorems, code constructions, or fundamental bounds.

This document systematically excavates the **hidden assumptions** underlying each pillar and the cross-cutting framework, then maps their **consequences** — both the risks if assumptions fail and the rewards if they hold. The goal is not to dismiss the program but to make its premises explicit, falsifiable, and strategically prioritized, so that early-phase work can resolve the highest-risk assumptions before significant resources are committed.

---

## 0. Meta-Assumption: The Structural Analogy Thesis

### 0.1 The Core Hidden Premise

Every pillar depends on a single meta-assumption that is never stated as such:

> **There exists a functorial or otherwise natural mapping from the category of quantum codes (or their stabilizer groups, or their logical subspaces) into a category of number-theoretic objects (p-adic functions, Galois representations, formal groups, Dieudonné modules, smooth representations of p-adic groups), such that structural properties in the number-theoretic category correspond to operationally meaningful properties of quantum codes.**

This is not a theorem to be proved in the course of the project; it is a **bet** placed at the outset. The plan treats it as a research hypothesis, but every pillar is scaffolded as if the mapping *already* exists and needs only to be "formalized" (Phase 1), "computed" (Phase 2), and "proved" (Phase 3).

### 0.2 Why It's Hidden

The plan uses the language of "connection" and "analogy," which obscures the fact that no such mapping has been constructed. Statements like "the silent-radix paper identifies cyclic measurement operators that generate an abelian group structure on the space of quantum states. This is precisely the structure described by local class field theory" (Pillar IV) collapse an observed similarity into an identity without establishing the mediating construction.

### 0.3 Consequences

| If True | If False |
|:--------|:---------|
| A new mathematical discipline at the intersection of arithmetic geometry and quantum information theory. Novel code constructions from arithmetic. | The entire seven-pillar framework is a **category error** — applying mathematical machinery to problems it was not designed for. Thirty-plus pages of research plan describe an elaborate mirage. |
| Deep number-theoretic bounds on quantum code parameters that are provably optimal. | Wasted Phase 1–3 effort on formalizing concepts that have no mathematical reality. A publication that would be seen, at best, as speculative mathematical philosophy. |
| Unification of QNFO's existing ultrametric tools under a single deep theory. | The existing ultrametric tools (Mahler compression, Amice transform, BT tree mapping) remain ad hoc heuristics without deep justification — which may be their natural state. |

### 0.4 Risk Reduction Strategy

Before committing to Phase 2 computational work, **one concrete bridge** must be constructed in full mathematical detail for at least one pillar. A single worked example — e.g., a specific CSS code mapped to a specific p-adic object with a verifiable property correspondence — would transform the meta-assumption from a bet into a hypothesis with evidentiary support, or falsify it early.

---

Each pillar inherits the meta-assumption and layers additional hidden assumptions specific to its domain. We analyze these below, grouping them into **(A) Mapping Assumptions** (the claimed analogy is valid), **(B) Structural Assumptions** (the number-theoretic side has the claimed structure), **(C) Operational Assumptions** (the quantum side has the claimed structure), and **(D) Testability Assumptions** (the claim is empirically falsifiable with available data).

---

## 1. Pillar I: p-adic Analysis — Beyond the Basics

### 1.1 Claim

The relationship between Mahler coefficient decay rates $|a_n|_p$ and ultrametric tree depth can classify quantum codes by their "structuredness," and the intrinsic Amice transform can detect Galois-invariant subspaces.

### 1.2 Hidden Assumptions

**A1 (Mapping):** There exists an injective encoding $\iota: \mathcal{C} \to C(\mathbb{Z}_p, \mathbb{Q}_p)$ from quantum codes to continuous p-adic functions, such that code-theoretic properties (distance, rate, fault-tolerance threshold) are faithfully reflected in analytic properties of $\iota(C)$ (Mahler decay rate, Amice spectral signature).

- *Why hidden:* The plan asks "what is the precise relationship between Mahler coefficient decay and tree depth?" — presupposing that some relationship exists. The encoding $\iota$ is never specified.
- *Why non-obvious:* Quantum codes are finite-dimensional subspaces of $(\mathbb{C}^d)^{\otimes n}$. Continuous p-adic functions form an infinite-dimensional Banach space. Any encoding will involve arbitrary choices (choice of basis, choice of p-adic valuation embedding) that may dominate the signal.

**A2 (Encoding Invariance):** For any two "reasonable" encodings $\iota_1, \iota_2$, the Mahler/Analytic properties that distinguish code types are preserved up to an identifiable transformation.

- *Why hidden:* The plan treats the Mahler coefficient decay as a property "of the code," not "of the code under a particular encoding." Without invariance, any observed structure may be an artifact of the encoding choice.

**A3 (Galois Detection):** The intrinsic Amice transform of $\iota(C)$ carries a spectral signature that distinguishes codes arising from arithmetic constructions (Goppa codes, AG codes) from random CSS codes.

- *Why hidden:* This assumes (a) that arithmetic codes have a characteristic spectral signature, (b) that random CSS codes do not, and (c) that the Amice transform is the right detector. All three are conjectural.

**B1 (p-adic Regularity of Codes):** Quantum codes, when embedded as p-adic functions, exhibit some nontrivial p-adic analytic structure (beyond the trivial constant function) that varies systematically with code parameters.

- *Why non-obvious:* There's no a priori reason discrete combinatorial objects (stabilizer codes) should correspond to analytic p-adic functions with interesting Mahler expansions. They could correspond to nowhere-differentiable p-adic functions or functions indistinguishable from noise.

**D1 (Signal-to-Noise in Benchmark Data):** The existing `ultrametric-benchmark` data has sufficient resolution and sample size to detect a Mahler coefficient pattern above statistical noise, given realistic effect sizes.

- *Why hidden:* The plan lists empirical testing as a Phase 2 task but doesn't estimate required effect sizes, statistical power, or the risk that real codes produce Mahler spectra indistinguishable from random p-adic functions.

### 1.3 Consequences

| If Assumptions Hold | If Assumptions Fail |
|:--------------------|:--------------------|
| A quantitative "order parameter" for code structuredness based on Mahler decay exponents. | Any choice of encoding $\iota$ produces a different Mahler spectrum — the method is encoding-relative, not code-intrinsic. |
| A spectral classifier distinguishing arithmetic from random codes. | The Amice spectrum of a random code is indistinguishable from that of a Goppa code — the transform has no discriminating power for this task. |
| A new analytic tool for code design: codes with prescribed Mahler decay rates. | The entire Pillar I reduces to a single observation: "quantum codes can be embedded into p-adic function spaces" — true but vacuous. |

### 1.4 Falsification Priority: **HIGH**
A simple Python experiment (encoding a few known CSS codes as p-adic step functions on $\mathbb{Z}_p$, computing Mahler coefficients, varying the encoding) can resolve A1 and A2 with minimal investment. This should be the first Phase 2 prototype, not deferred to later.

---

## 2. Pillar II: Hasse Local-Global Principle

### 2.1 Claim

A quantum code $[[n,k,d]]$ exists over $\mathbb{C}$ if and only if it exists "locally" at every prime $p$ and at the archimedean place. Failures of this principle (analogous to the Brauer-Manin obstruction) identify novel code constructions.

### 2.2 Hidden Assumptions

**A1 (Local Code Well-Definedness):** There is a well-defined notion of a "local quantum code at a prime $p$" — that is, a quantum code defined over $\mathbb{Q}_p$ (or $\mathbb{F}_p$ lifted via Witt vectors) whose parameters $[[n,k,d]]$ are meaningful in the ultrametric setting.

- *Why hidden:* The plan acknowledges this as an open definitional question (RQ2.1: "What is the appropriate notion of a local quantum code at a prime $p$?") but the entire pillar depends on this notion existing and being sufficiently constrained to make the Hasse principle nontrivial.
- *Why non-obvious:* Quantum codes are defined on complex Hilbert spaces. "Reducing mod $p$" a stabilizer code is not a standard operation. If the definition is too weak (any combination of parameters can be declared "locally realizable"), the Hasse principle is vacuously true. If it's too strong (only codes that literally lift from $\mathbb{F}_p$ are local), it may be vacuously false for almost all interesting codes.

**A2 (Nontriviality of Local-Global Obstruction):** The Hasse principle for quantum codes is nontrivial — i.e., there exist parameter sets that are locally realizable at every place but NOT globally realizable.

- *Why hidden:* The plan assumes this by drawing an analogy with cubic surfaces (Selmer's counterexample). But for quantum codes, it's possible that local realizability everywhere *always* implies global realizability (the principle is trivial), or that local realizability is so restrictive that no interesting obstruction exists.

**A3 (Existence of Brauer-Manin-type Obstruction):** There is a cohomological invariant of quantum code parameter sets taking values in some Brauer-like group $\operatorname{Br}(\mathcal{C})$, whose nontriviality obstructs global existence.

- *Why hidden:* The Brauer group $\operatorname{Br}(X)$ is defined for algebraic varieties. There is no known analogous invariant for subspaces of Hilbert space. The plan asks this as a research question without acknowledging that a negative answer — "no such invariant exists" — is both plausible and would be difficult to prove.

**B1 (Minkowski-Hasse Analog):** Stabilizer code parameters have local invariants (analogous to the signature and p-adic invariants of quadratic forms) that completely classify them.

- *Why non-obvious:* Quadratic forms over $\mathbb{Q}$ are classified by dimension, signature, and Hasse-Witt invariants. Stabilizer codes are classified by $[[n,k,d]]$ plus more subtle properties (code automorphism group, weight enumerator). The analogy would require that the "more subtle properties" correspond to local invariants in exactly the way they do for quadratic forms — a very strong structural claim.

### 2.3 Consequences

| If Assumptions Hold | If Assumptions Fail |
|:--------------------|:--------------------|
| A systematic criterion for which code parameters are realizable, analogous to the Hasse-Minkowski classification of quadratic forms. | "Local quantum code at p" never gets a rigorous definition that is simultaneously non-vacuous and nontrivial. |
| Discovery of new code families via Brauer-Manin obstructions — codes that exist globally *only because* of a nontrivial adelic obstruction. | All known codes trivially satisfy the local conditions, making the Hasse principle a tautology with no predictive power. |
| A classification theorem for stabilizer codes by local invariants (dimension, "p-adic distance signature," etc.). | The analogy with quadratic forms is revealed as superficial: the mathematical structure that makes Hasse work (algebraic groups, Galois cohomology) has no quantum-code analog. |

### 2.4 Falsification Priority: **CRITICAL**
The definition of "local quantum code at p" (RQ2.1) is the **single most important definitional task** in the entire research plan. If it cannot be made rigorous, Pillars II, III, and VI all collapse in cascade. This should be attempted before any computational work.

---

## 3. Pillar III: Galois Representations and p-adic Hodge Theory

### 3.1 Claim

There is a filtration of stabilizer code spaces:
$$\text{crystalline codes} \subset \text{semistable codes} \subset \text{de Rham codes}$$

analogous to Fontaine's period ring filtration, with the Fontaine-Mazur conjecture providing a criterion for which codes are "geometric" (physically realizable).

### 3.2 Hidden Assumptions

**A1 (Galois Representation Assignment):** To each stabilizer code $C$, one can assign a p-adic Galois representation $\rho_C: G_{\mathbb{Q}_p} \to \operatorname{GL}_n(\mathbb{Q}_p)$ (or into some automorphism group) whose Hodge-theoretic properties classify $C$.

- *Why hidden:* The plan never specifies from *what* the Galois group would act. In classical p-adic Hodge theory, the Galois group $G_{\mathbb{Q}_p} = \operatorname{Gal}(\overline{\mathbb{Q}}_p / \mathbb{Q}_p)$ acts on étale cohomology of algebraic varieties. Quantum codes are not algebraic varieties. What would the Galois action act on?
- *Severity:* EXTREME. Without specifying the object the Galois group acts on, the entire Fontaine-Mazur analogy is content-free.

**A2 (Fontaine Filtration Existence):** The categories "crystalline," "semistable," and "de Rham" admit a natural translation to quantum codes that discriminates between known code families.

- *Why hidden:* Fontaine's definitions use period rings $B_{\text{crys}}, B_{\text{st}}, B_{\text{dR}}$ — highly technical p-adic analytic constructions. Translating these to quantum codes requires either (a) a direct analog of period rings in the code setting or (b) a characterization via Frobenius/monodromy that has a code-theoretic meaning. Neither exists yet.
- *Risk:* The filtration may exist but place every known stabilizer code in the "de Rham" category, making the classification trivial.

**A3 (Frobenius = Cyclic Measurement):** The Frobenius endomorphism in the p-adic setting corresponds to the cyclic measurement operator from the silent-radix project.

- *Why hidden:* Frobenius is the p-th power map $x \mapsto x^p$ in characteristic $p$, or its lift. Cyclic measurement operators generate finite cyclic groups on quantum state spaces. The analogy is at the level of "both generate cyclic group actions" — which is a very weak similarity that many mathematical objects satisfy.

**A4 (Serre Modularity Analog):** There is a "modularity theorem" for quantum codes: certain classes of codes correspond to modular forms (or automorphic forms).

- *Severity:* EXTREME. Serre's modularity conjecture (now a theorem: Khare-Wintenberger, 2008) is one of the hardest results in modern number theory, proving that every odd irreducible 2-dimensional Galois representation over a finite field comes from a modular form. The proof required the full machinery of the Taylor-Wiles method. There is no reason to expect a quantum analog to be provable with current techniques, or even statable.

### 3.3 Consequences

| If Assumptions Hold | If Assumptions Fail |
|:--------------------|:--------------------|
| A deep classification theorem: codes are "crystalline" (good reduction, sharp thresholds), "semistable" (controlled ramification), or "de Rham" (general). | No natural Galois representation can be assigned to stabilizer codes — the whole pillar is an over-interpretation of the word "crystalline." |
| Physical realizability criterion: Fontaine-Mazur analog identifies which codes can be built in real hardware. | The Fontaine-Mazur criterion either selects all known codes (tautological) or none (too restrictive). |
| New code discovery: Frobenius-invariant codes that are "supersingular" in the p-adic Hodge sense. | The cyclic-measurement/Frobenius analogy is revealed as a superficial word-game. |

### 3.4 Falsification Priority: **HIGH**
The assignment A1 is the bottleneck. Without a Galois action, nothing else in this pillar has meaning. The plan should attempt to construct $\rho_C$ for the simplest possible code (e.g., the 5-qubit code) before proceeding further. A negative result here (no natural Galois representation exists) nullifies the entire pillar.

---

## 4. Pillar IV: Class Field Theory and Cyclic Measurement

### 4.1 Claim

The local Artin map $\theta_p: \mathbb{Q}_p^\times \to \operatorname{Gal}(\mathbb{Q}_p^{\text{ab}}/\mathbb{Q}_p)$ corresponds to a continuous family of cyclic measurements parameterized by p-adic units, and the Kronecker-Weber theorem analog asserts that every abelian measurement scheme is contained in a generalized Clifford group.

### 4.2 Hidden Assumptions

**A1 (Abelian Measurement Group ≅ Galois Group):** The group generated by cyclic measurement operators is naturally isomorphic to $\operatorname{Gal}(K^{\text{ab}}/K)$ for some p-adic field $K$.

- *Why hidden:* Cyclic measurement operators form a finite abelian group (typically $\mathbb{Z}/D\mathbb{Z}$ for D-dimensional clocks). The local Artin map is an isomorphism between $\widehat{\mathbb{Q}_p^\times}$ (a profinite group) and $\operatorname{Gal}(\mathbb{Q}_p^{\text{ab}}/\mathbb{Q}_p)$. For a finite abelian measurement group to be isomorphic to a Galois group extracted from this, one would need a specific finite quotient — but which one, and why that one?
- *Non-obvious direction:* The Artin map goes from *units* to *Galois group*. The plan would need the opposite direction, or to identify what the *units* are in the measurement setting.

**A2 (Kronecker-Weber = Clifford):** The generalized Clifford group plays the role in quantum information that cyclotomic extensions play in number theory.

- *Why hidden:* The generalized Clifford group is the normalizer of the Pauli group in the unitary group — a finite group of unitary operators. Cyclotomic extensions $\mathbb{Q}(\zeta_n)$ are infinite-degree field extensions generated by roots of unity. The analogy requires that (a) the Clifford group is "maximal" for abelian measurement in the same sense that $\mathbb{Q}^{\text{ab}}$ is maximal for abelian extensions of $\mathbb{Q}$, and (b) the "building blocks" (Pauli X, Z) correspond to roots of unity. Both are plausible but unverified.

**A3 (Idele Class Group = Universal Measurement Group):** $\mathbb{A}_\mathbb{Q}^\times / \mathbb{Q}^\times$ is a "universal measurement group" for the adelic QEC framework.

- *Severity:* MAJOR. This would require every measurement in the adelic framework to factor through the idele class group. The idele class group is a global object encoding information at all primes simultaneously. A "measurement" in physics is typically a local operation. Reconciling these is nontrivial.

### 4.3 Consequences

| If Assumptions Hold | If Assumptions Fail |
|:--------------------|:--------------------|
| Cyclic measurement theory acquires deep classification: measurement schemes classified by abelian extensions of $\mathbb{Q}_p$. | The group generated by cyclic measurement operators has no natural identification with a Galois group — they are just finite cyclic groups. |
| Kronecker-Weber analog proves that all abelian measurement schemes are Clifford — a fundamental completeness theorem. | The Clifford group is just one of many unitary subgroups; any analogy with cyclotomic extensions is coincidental. |
| Idele-theoretic measurement: a unified description of measurements across all p-adic completions. | The idele class group has no operational interpretation in quantum mechanics. |

### 4.4 Falsification Priority: **MODERATE**
This pillar is the most directly connected to existing QNFO work (silent-radix). The "cyclic measurement = Artin symbol" identification for a specific measurement protocol could be tested without full formalization. A single explicit computation for $D=4$ Fourier clocks would be highly informative.

---

## 5. Pillar V: Arithmetic Geometry of Quantum Codes

### 5.1 Claim

The Kodaira-Néron classification of elliptic curve reduction types maps onto a classification of quantum code degenerations under p-adic deformation. Formal group logarithms encode code deformation parameters, and supersingular isogeny graphs describe code-switching protocols.

### 5.2 Hidden Assumptions

**A1 (Codes as Moduli Spaces):** Quantum codes admit a notion of "p-adic deformation" that forms a moduli space analogous to that of elliptic curves, with well-defined reduction types.

- *Why hidden:* The plan speaks of "code degenerations under p-adic deformation" as if this is an established concept. Quantum codes are discrete objects with discrete parameters $(n,k,d)$. Deforming them continuously requires an embedding into a parameterized family. Such families exist in principle (e.g., varying the underlying metric on the code manifold) but have never been classified by Kodaira-Néron types.
- *Fundamental question:* What property of a code degenerates when we "reduce mod p"? The distance? The rate? The stabilizer group itself?

**A2 (Formal Group Log = Code Deformation):** The formal group logarithm $\log_{\widehat{E}}(T)$ of an elliptic curve encodes a deformation family of quantum codes where $T$ parameterizes distance from a reference code.

- *Why hidden:* Formal group logarithms describe the group structure infinitesimally near the identity of an elliptic curve. The claim that its expansion coefficients $a_i$ encode code properties requires (a) identifying what the "identity code" is, (b) identifying what $T$ is in the code setting, and (c) showing that the logarithm formula actually describes code parameter variation. None of these identifications are specified.

**A3 (Isogeny Graph = Code-Switching):** A path in a supersingular isogeny graph corresponds to a sequence of code deformations preserving ultrametric invariants.

- *Why hidden:* Isogenies are surjective homomorphisms between elliptic curves with finite kernel. "Code-switching" (transitioning between quantum codes) would require an analog of an isogeny between codes. No such concept has been defined.
- *Specific risk:* Supersingular isogeny graphs are Ramanujan expanders on $\approx p/12$ vertices. Most known quantum code families are much smaller. The graph structure may not be rich enough to describe realistic code-switching protocols.

### 5.3 Consequences

| If Assumptions Hold | If Assumptions Fail |
|:--------------------|:--------------------|
| A Kodaira-Néron classification of code families by their p-adic reduction behavior: good reduction = distance-preserving, multiplicative = partial collapse, additive = total collapse. | "Code deformation" and "p-adic reduction" remain undefined for quantum codes, reducing the pillar to a suggestive analogy. |
| Formal group methods produce explicit deformation formulas for code distance as a function of a continuous parameter. | The formal group logarithm describes elliptic curves, not quantum codes. No map exists. |
| Isogeny-based code-switching protocols with provable invariants (analog of isogeny-invariant j-invariant). | Isogeny graphs are irrelevant to quantum codes. The SIDH cryptography analogy is a red herring. |

### 5.4 Falsification Priority: **HIGH**
This pillar is the most "geometric" — it requires quantum codes to have geometric structure analogous to algebraic curves. A minimal test: take a 1-parameter family of quantum codes (e.g., surface codes on a torus with varying aspect ratio) and check whether the distance function exhibits behavior analogous to any Kodaira-Néron type. Only needs 2-3 code families.

---

## 6. Pillar VI: Witt Vectors and Stabilizer Code Cohomology

### 6.1 Claim

There is a cohomology theory $H^\bullet_{\text{stab}}(C)$ valued in Dieudonné modules, with Frobenius $F$ corresponding to Clifford conjugation and Verschiebung $V$ corresponding to T-gate injection. The slope decomposition classifies codes by error-correction capacity.

### 6.2 Hidden Assumptions

**A1 (Dieudonné Module Assignment):** For each stabilizer code $C$, there exists a Dieudonné module $D(C)$ over the Dieudonné ring $D_{\mathbb{F}_p} = W(\mathbb{F}_p)[F,V]/(FV-p)$, natural in $C$.

- *Why hidden:* Dieudonné modules classify finite flat commutative group schemes over perfect fields of characteristic $p$. Stabilizer codes are not group schemes. The Dieudonné module of a group scheme $G$ is defined via its contravariant Dieudonné functor from crystalline cohomology. To assign $D(C)$ to a code, one would need a "code scheme" whose Dieudonné module can be extracted — no such object exists.
- *Severity:* EXTREME. This is arguably the most mathematically specific and least justified analogy in the entire plan.

**A2 (F = Clifford, V = T-gate):** $F$ (Frobenius on the Dieudonné module) corresponds precisely to conjugation by elements of the Clifford group, and $V$ (Verschiebung) corresponds to T-gate injection.

- *Why hidden:* The only stated connection is that both satisfy $FV = p = VF$. But many pairs of operators satisfy this relation. Clifford conjugation satisfies $C P C^\dagger = P'$ where $P, P' \in \mathcal{P}_n$ (the Pauli group). Frobenius satisfies $F(ax) = a^p F(x)$. These are structurally different operations.
- *Alternative interpretation:* $F$ and $V$ might correspond to something else entirely (e.g., encoding/decoding operations, or measurement/feedback cycles). The specific identification with Clifford and T-gates is under-motivated.

**A3 (Slope = Error Threshold):** Crystalline codes (integer slopes in the Dieudonné-Manin classification) have sharp error-correction thresholds, while non-crystalline codes (fractional slopes) have soft thresholds.

- *Why hidden:* The Dieudonné-Manin slope measures the "Frobenius structure" of an isocrystal. Error-correction thresholds are functions of the code, noise model, and decoder. Connecting these requires an entire bridge theory that does not exist.
- *Empirical risk:* Even if the analogy holds, the observed correlation between slope and threshold behavior may be weak, dominated by other factors (decoder choice, noise bias), or impossible to measure with available data.

### 6.3 Consequences

| If Assumptions Hold | If Assumptions Fail |
|:--------------------|:--------------------|
| A cohomological classification of stabilizer codes by their "arithmetic complexity," with codes at integer slopes being "rigid" (sharp thresholds) and fractional-slope codes being "soft." | No Dieudonné module can be naturally assigned to a stabilizer code — the entire cohomology theory is undefined. |
| Witt vector techniques enable new code constructions by lifting from characteristic $p$. | Witt vectors remain a tool for paper versioning only (Principle #14), with no connection to stabilizer code structure. |
| Dieudonné-Manin slope predicts error-correction behavior without simulation. | The "slope = threshold" claim is either empirically false or untestable. |

### 6.4 Falsification Priority: **CRITICAL**
The Dieudonné module assignment (A1) is more fundamental than any testing in this pillar. Without it, the pillar has no objects to work with. The plan should attempt to define $D(C)$ for the simplest possible code (binary repetition code, or the 3-qubit bit-flip code) before investing in any other aspect of this pillar. If this fails, the entire pillar should be archived as "speculative."

---

## 7. Pillar VII: Bruhat-Tits Buildings, Berkovich Spaces, and Langlands

### 7.1 Claim

The Moy-Prasad depth parameter $r$ in the Bruhat-Tits building corresponds to logical error rate. The Bernstein decomposition classifies universality classes of quantum codes. The local Langlands correspondence for $\operatorname{GL}_n$ classifies n-qudit quantum codes, and the geometric Langlands program provides a framework for topological quantum codes.

### 7.2 Hidden Assumptions

**A1 (Moy-Prasad depth = error rate):** The depth $r(\pi)$ of a smooth representation $\pi$ of $G(\mathbb{Q}_p)$ (the minimal $r$ such that $\pi$ has $G_{x,r}$-fixed vectors) corresponds to the logical error rate or fault-tolerance threshold of an associated quantum code.

- *Why hidden:* Moy-Prasad depth is a purely representation-theoretic invariant — how "deep" into the building one must go to find fixed vectors. Logical error rate is a physical quantity depending on noise model, code distance, and decoder. The plan provides no mechanism connecting these.
- *Structural issue:* Depth is an integer or rational number (depending on normalization) determined by the representation's type. Error rates are continuous and noise-model-dependent. For the analogy to be nontrivial, there must be a correspondence between discrete depth values and continuous error rates — likely via thresholds or phase transitions.

**A2 (Bernstein Decomposition = Universality Classes):** The decomposition of the category of smooth representations into Bernstein blocks classifies universality classes of quantum codes.

- *Why hidden:* The Bernstein decomposition partitions irreducible representations by their supercuspidal support. "Universality classes" in quantum codes typically refer to codes sharing the same asymptotic scaling behavior (e.g., surface codes, hyperbolic codes). Mapping one to the other requires identifying supercuspidal support with asymptotic code properties — a completely open problem.

**A3 (Local Langlands = Code Classification):** The local Langlands correspondence for $\operatorname{GL}_n(\mathbb{Q}_p)$ provides a classification of n-qudit quantum codes.

- *Severity:* EXTREME. The local Langlands correspondence is a theorem (for GL_n) that bijects irreducible smooth representations of GL_n with n-dimensional Weil-Deligne representations. To claim this classifies quantum codes requires:
  1. That $n$-qudit codes correspond to representations of $\operatorname{GL}_n(\mathbb{Q}_p)$ — i.e., that the qudit count corresponds to the rank of the general linear group.
  2. That the irreducibility of the representation corresponds to some code property (indecomposability?).
  3. That Weil-Deligne parameters correspond to code parameters ($\varepsilon$-factors = weight enumerators).
  
  Every one of these identifications is speculative.

**A4 (Geometric Langlands → Topological Codes):** The geometric Langlands program over the Fargues-Fontaine curve provides a framework for topological quantum codes.

- *Severity:* EXTREME. Geometric Langlands is a deep conjectural program connecting D-modules on the moduli stack of G-bundles to representations of the Langlands dual group. Topological quantum codes are defined on 2D surfaces with anyonic excitations. The connection would require:
  1. Identifying the "curve" in the Fargues-Fontaine setting as the surface on which anyons live.
  2. Identifying D-modules (or perverse sheaves) with anyon types.
  3. Identifying Hecke eigensheaves with code states.
  
  This is so far beyond current mathematics that it should be labeled `[purely speculative — not actionable in this research cycle]`.

**B1 (Building Generality):** $\mathcal{B}(\operatorname{SL}_n, \mathbb{Q}_p)$ for $n > 2$ (higher-rank buildings, which are not trees) corresponds to multi-parameter code families.

- *Why non-obvious:* Higher-rank BT buildings are polysimplicial complexes whose structure is much richer than the $(p+1)$-regular tree for SL_2. While the plan asks whether they correspond to multi-parameter code families, it doesn't specify what the $n-1$ parameters would be — or whether any known code families exhibit $n-1$ independent continuous parameters.

### 7.3 Consequences

| If Assumptions Hold | If Assumptions Fail |
|:--------------------|:--------------------|
| Moy-Prasad depth predicts fault-tolerance thresholds from representation theory alone. | Depth has no operational meaning for quantum codes; the building classification remains a purely mathematical structure. |
| Bernstein blocks organize the "zoo" of quantum codes into a finite set of universality classes. | Bernstein blocks classify representations of p-adic groups — unrelated to quantum codes. |
| Local Langlands correspondence provides the definitive classification of qudit codes. | The Langlands program remains about number theory and representation theory, with no quantum information content. |
| Geometric Langlands provides a new foundation for topological quantum computation. | The connection is so speculative that even outlining it requires PhD-level exposition with no guarantee of payoff. |

### 7.4 Falsification Priority: **LOW (A1, A2 — testable with BT tree data) / DEFER (A3, A4 — requires mathematical developments beyond current scope)**

The existing BT tree mapping (from the ultrametric engine) provides a concrete test bed for A1: can Moy-Prasad depth be computed for the BT tree embedding of known codes, and does it correlate with any measurable performance metric? This is the most actionable part of Pillar VII. A3 and A4 should be deferred to a future research cycle unless a breakthrough in mathematical formalization occurs.

---

## 8. Cross-Cutting Hidden Assumptions

### 8.1 The Pillar Independence Assumption

**Hidden assumption:** The seven pillars are independent enough that progress in one does not require progress in others, and failure of one pillar does not cascade.

**Reality:** The pillars are deeply interconnected. Pillar VI (Witt cohomology) depends on Pillar II (Hasse principle, via the notion of local codes). Pillar III (Fontaine classification) depends on Pillar VI (Dieudonné modules are central to p-adic Hodge theory). Pillar VII (Langlands) depends on Pillar III (Galois representations). **Failure of Pillar II's local code definition cascades to III, VI, and VII.**

### 8.2 The Exhaustiveness Assumption

**Hidden assumption:** The seven pillars cover the relevant deep number theory domains.

**Reality:** Significant omissions include:
- **Iwasawa theory** — limits of class groups in $\mathbb{Z}_p$-extensions, which might model infinite code families.
- **Modular forms and automorphic forms beyond GL_n** — the plan mentions Serre modularity (Pillar III) but doesn't develop the full automorphic machinery.
- **Shimura varieties** — moduli spaces of abelian varieties with additional structure, which are the geometric setting for many Langlands correspondences.
- **p-adic L-functions** — interpolation of special values, potentially connected to weight enumerators.

### 8.3 The Archimedean Bridge Assumption

**Hidden assumption:** The p-adic/archimedean bridge (Fontaine-Fargues curve, Cross-cutting 2.1) is the correct framework for connecting ultrametric quantum codes to physical (archimedean) quantum mechanics.

**Issue:** The Fontaine-Fargues curve is a deep object in modern p-adic Hodge theory — still under active development. The plan explicitly acknowledges this as `[not yet falsifiable]`, but then builds Cross-cutting 2.1 on it. If the bridge itself is not yet constructed in mathematics, it certainly cannot be used as a foundation for quantum code theory.

### 8.4 The QNFO Infrastructure Dependence Assumption

**Hidden assumption:** The existing QNFO infrastructure (ultrametric-engine Worker, `ultrametric-benchmark` data, silent-radix cyclic measurement framework) is sufficient to test the number-theoretic conjectures.

**Reality:** The ultrametric engine implements 20 mathematical principles, but these are computational tools — not deep number theory. Testing Pillar III (Fontaine classification) or Pillar VII (Langlands for qudit codes) requires mathematical machinery far beyond what the current Worker endpoints provide. Significant new development would be needed.

### 8.5 The Testability-as-Falsifiability Assumption

**Hidden assumption:** The falsifiability conditions listed in Section 7 of the RESEARCH-PLAN are an adequate safety net.

**Reality:** Several falsification conditions are themselves untestable with current methods:
- "No natural Frobenius/Verschiebung-like operators exist on the space of stabilizer codes" — proving non-existence is generally harder than proving existence, and a negative result could always be attributed to not having searched well enough.
- "No meaningful map between representation depth and code parameters exists" — similarly, a negative result is hard to establish definitively.
- The falsifiability conditions are framed as "if we can't find X, the pillar fails," but in practice, "we haven't found X yet" is not the same as "X doesn't exist."

---

## 9. Consequences Matrix: Systemic Risks and Rewards

### 9.1 Cascading Failure Mode

The pillars are not independent. The most critical dependency chain is:

```
Pillar II: Local code definition
    ↓
Pillar III: Galois rep assignment (depends on local codes having Galois structure)
    ↓
Pillar VI: Witt/Dieudonné cohomology (depends on Galois reps having crystalline structure)
    ↓
Pillar VII: Langlands (depends on representations of p-adic groups)
```

**If Pillar II fails to produce a rigorous local code definition, Pillars III, VI, and VII are structurally undermined.** They may still produce interesting mathematics, but the claimed connection to quantum codes would be severed.

### 9.2 Resource Allocation Risk

The plan allocates 9–14 weeks total across four phases. Given the mathematical depth of the open problems involved:
- Phase 1 (definitions): Optimistic. Defining "local quantum code" alone could be a PhD thesis.
- Phase 2 (computation): Underestimates the implementation complexity of p-adic Hodge-theoretic computations.
- Phase 3 (theorems): The conjecture statuses — some labeled `[speculative]` — indicate that proving these results would be publishable in top-tier math journals, not a 4–8 week project.
- Phase 4 (publication): Premature if Phases 1–3 have not resolved fundamental definitional questions.

### 9.3 Reputational Risk

Publishing a paper claiming a Langlands-QEC connection, a crystalline/semistable/de Rham classification, or a Hasse principle for quantum codes before any of these connections are mathematically established would invite scrutiny from both number theorists and quantum information theorists. The plan currently labels claims with certainty tags (`[established]`, `[my conjecture]`, `[speculative]`), which is good practice, but a published paper would need much stronger evidence.

### 9.4 Upside: What Success Looks Like

If the core mapping assumptions hold across even 2–3 pillars, the payoff is substantial:
- **New code construction paradigm:** Arithmetic codes defined via algebraic geometry would join the CSS/surface/LDPC taxonomy.
- **Fundamental bounds from number theory:** The Hasse principle and Fontaine-Mazur analog could prove that certain code parameters are impossible.
- **Classification theorem:** At minimum, a taxonomy of codes by arithmetic type (even if only conjectural) would organize the field.
- **Unification of QNFO tools:** The existing 20+ ultrametric principles would gain a unified mathematical foundation.

### 9.5 The Most Likely Outcome Spectrum

Based on precedent (analogies between number theory and physics — e.g., arithmetic topology, the Kapranov-Reznikov-Mazur program, p-adic AdS/CFT proposals):

| Outcome | Probability Estimate | Description |
|:--------|:--------------------:|:------------|
| **Deep connection (1–2 pillars)** | ~10% | At least one pillar yields a genuine, productive, non-obvious connection that produces new code constructions or theorems. |
| **Heuristic utility (3–4 pillars)** | ~30% | Several analogies provide useful heuristics and organizational frameworks but do not yield rigorous theorems. |
| **Suggestive but sterile (all pillars)** | ~40% | All analogies are intellectually interesting but produce no new code constructions, bounds, or falsifiable predictions. The project contributes a taxonomy of analogies. |
| **Category error (most pillars)** | ~20% | The fundamental gap between the categories of quantum codes and number-theoretic objects is too wide. Most analogies dissolve under scrutiny. |

These are rough estimates based on the track record of cross-disciplinary mathematical analogies. The history of mathematics is rich with both productive analogies (algebraic topology from geometry, quantum groups from statistical mechanics) and sterile ones (many proposed bridges between number theory and physics).

---

## 10. Strategic Recommendations

### 10.1 Immediate (Before Phase 2)

1. **Construct one concrete bridge.** Pick the simplest pillar (Pillar IV: class field theory/cyclic measurement, because silent-radix provides working code) and construct an explicit, verified mapping from a specific measurement protocol to an Artin symbol. Do not proceed to other pillars until ONE bridge is built.

2. **Define "local quantum code at p."** This is the single most important definition in the plan. Convene working definitions for Pillar II that are simultaneously:
   - Mathematically precise (operators, spaces, parameters)
   - Physically motivated (what does it mean for a code to be "defined over $\mathbb{Q}_p$"?)
   - Non-vacuous (at least some known codes satisfy it, at least some parameter sets fail it)

3. **Pillar triage.** Based on the cascading dependency analysis, reorder the pillars:
   - **Wave 1 (immediate):** Pillar I (computable), Pillar IV (has working code connection), Pillar II (definitions)
   - **Wave 2 (dependent on Wave 1):** Pillar III, Pillar VI
   - **Wave 3 (defer):** Pillar V (needs code deformation theory), Pillar VII A3/A4 (Langlands — speculative)

### 10.2 Phase 2 Pilot Experiments

Before committing to the full Phase 2 computational program, run three minimal pilots:

| Pilot | Pillar | Cost | Success Criterion |
|:------|:-------|:-----|:-------------------|
| Mahler spectrum of 5-qubit code | I | 1 day | Mahler coefficient decay distinguishable from random p-adic function at p<0.05 |
| Local invariants for CSS codes | II | 2 days | At least one code family has nontrivial local invariants that vary across primes |
| Artin symbol for D=4 Fourier clock | IV | 1 day | Cyclic measurement operator maps to identifiable element of $\operatorname{Gal}(\mathbb{Q}_p^{\text{ab}}/\mathbb{Q}_p)$ |

If ALL THREE pilots yield negative results, the meta-assumption should be re-examined before further investment.

### 10.3 Documentation Standards

Amend the RESEARCH-PLAN to include for each conjecture:
1. **The minimal falsifying observation** (already present in Section 7, but strengthen to be immediately testable in Phase 2)
2. **The constructive step that must succeed first** (e.g., "Before testing RQ3.1, we must construct $\rho_C$ for a single code")
3. **The expected difficulty level** of the constructive step (trivial / moderate / requires new mathematics)

### 10.4 Publish-What-You-Have vs. Wait-Until-Solid

Consider publishing an interim "Landscape and Conjectures" paper that:
- States the structural analogy thesis explicitly as a conjecture
- Provides the rigorous definitions for pillars where they exist
- Marks pillars where definitions are still lacking as "open problems"
- Includes computational pilot results (positive or negative)

This is lower-risk than waiting for all seven pillars to mature, and establishes priority for the framework even if individual pillars require years to develop.

---

## 11. Conclusion

The `number-theory-ultrametric-deep` RESEARCH-PLAN is the most ambitious mathematical program in the QNFO research portfolio. It attempts to connect quantum information theory to seven of the deepest areas of modern number theory — areas where individual conjectures (the Langlands program, the Fontaine-Mazur conjecture) have driven entire careers of research.

The hidden assumptions identified in this audit are not flaws to be eliminated but **bets to be acknowledged, prioritized, and tested early**. The framework's architecture — building all seven pillars on the meta-assumption of a structural analogy — means that the failure of any foundational definition (especially "local quantum code at p") cascades to multiple pillars.

The strategic path forward is:

1. **Build one bridge** (Pillar IV is the most promising entry point via silent-radix)
2. **Define the foundational object** (local quantum code at p for Pillar II)
3. **Run three minimal pilots** (Mahler spectrum, local invariants, Artin symbol)
4. **Triage pillars** by dependency and tractability
5. **Publish incrementally** rather than awaiting full seven-pillar maturity

With this approach, even if only 1–2 pillars yield productive connections, the project will have advanced the field. And if the meta-assumption is fundamentally sound, the triage ensures that effort is spent where the evidence is strongest.

---

*This document is a Phase 1 pre-implementation audit. All assessments are provisional and subject to revision as computational and theoretical evidence accumulates. Follows QNFO-POL-COM-001 certainty labeling standards.*
