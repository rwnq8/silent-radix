# PHASE 3: Fontaine Classification of Quantum Codes — Proof Sketches

**Project:** number-theory-ultrametric-deep | **Date:** 2026-07-03
**Pillar:** III — Galois Representations and p-adic Hodge Theory
**Status:** Phase 3 — Theorem Development `[in-progress]`

---

## 0. Overview

This document provides proof sketches for the central conjecture of Pillar III: that stabilizer codes over $\mathbb{F}_p$ admit a Fontaine-style classification into crystalline, semistable, and de Rham classes, ordered by inclusion:

$$\mathcal{C}_{\text{crys}} \subset \mathcal{C}_{\text{st}} \subset \mathcal{C}_{\text{dR}}$$

This classification connects to the Witt cohomology formalized in `conjectures-formal.tex` (Conjectures 3.1-3.3) and to the NUMBER-THEORY-QEC-BRIDGE.md (Conjecture 2.1).

### Prerequisites

The reader should be familiar with:
- Stabilizer codes over $\mathbb{F}_p$ (Gottesman, 1997)
- The Dieudonné module $D(C)$ of a stabilizer code (Conjecture 3.1 in `conjectures-formal.tex`)
- Fontaine's period rings $B_{\text{crys}} \subset B_{\text{st}} \subset B_{\text{dR}}$ (Fontaine, 1994)
- p-adic Galois representations and their classification by period rings

---

## 1. Definitions and Setup

### 1.1 The Category of Quantum Codes

**Definition 1.1 (Stabilizer Code over $\mathbb{F}_p$).** Let $p$ be a prime, $n \geq 1$, and let $\mathcal{P}_n^{(p)}$ be the generalized Pauli group on $n$ qudits of dimension $p$. A *stabilizer code* $C$ with parameters $[[n, k, d]]_p$ is an abelian subgroup $S \subset \mathcal{P}_n^{(p)}$ such that $-I \notin S$, with $k = n - \dim_{\mathbb{F}_p}(S)$.

**Definition 1.2 (Category $\mathbf{QCode}_p$).** The category $\mathbf{QCode}_p$ has:
- **Objects:** Stabilizer codes over $\mathbb{F}_p$ (equivalence classes under local Clifford transformations)
- **Morphisms:** Code morphisms — Clifford operations that map one stabilizer group to another while preserving the tensor product structure up to isometry

### 1.2 The Witt Cohomology Functor

From Conjecture 3.1 of `conjectures-formal.tex`, we postulate a functor:

$$H^{\bullet}_{\text{stab}}: \mathbf{QCode}_p \longrightarrow D_{\mathbb{F}_p}\text{-Mod}$$

where $D_{\mathbb{F}_p} = W(\mathbb{F}_p)[F, V]/(FV - p = VF - p)$ is the Dieudonné ring.

**Axiom (Existence).** For each stabilizer code $C$, there exists a Dieudonné module $D(C) = H^{\bullet}_{\text{stab}}(C)$, finite and free over $W(\mathbb{F}_p)$, with semilinear Frobenius $F: D(C) \to D(C)$ and Verschiebung $V: D(C) \to D(C)$ satisfying $FV = VF = p$.

**Axiom (Functoriality).** A code morphism $f: C \to C'$ induces a $D_{\mathbb{F}_p}$-linear map $H^{\bullet}_{\text{stab}}(f): D(C) \to D(C')$ commuting with $F$ and $V$.

### 1.3 Period Ring-Valued Representations

**Definition 1.3 (Associated Galois Representation).** Let $C$ be a stabilizer code and $D(C)$ its Dieudonné module. The *associated Galois representation* of $C$ is:

$$V_C := \operatorname{Hom}_{W(\mathbb{F}_p)[F]}(D(C), B_{\text{crys}}) \otimes_{\mathbb{Q}_p} \overline{\mathbb{Q}}_p$$

This is a $(\dim D(C) / \operatorname{rank} W(\mathbb{F}_p))$-dimensional $p$-adic representation of $G_{\mathbb{Q}_p} := \operatorname{Gal}(\overline{\mathbb{Q}}_p / \mathbb{Q}_p)$.

**Motivation.** In classical p-adic Hodge theory, the functor $\operatorname{Hom}_{W(k)[F]}(-, B_{\text{crys}})$ converts a Dieudonné module into a crystalline Galois representation. We replicate this construction for the Witt cohomology of stabilizer codes.

---

## 2. The Classification Filtration

### 2.1 Crystalline Codes

**Definition 2.1 (Crystalline Code).** A stabilizer code $C$ is *crystalline* if its associated Galois representation $V_C$ is crystalline in the sense of Fontaine. Equivalently:

$$\dim_{\mathbb{Q}_p} V_C = \dim_{\mathbb{Q}_p} (V_C \otimes_{\mathbb{Q}_p} B_{\text{crys}})^{G_{\mathbb{Q}_p}}$$

**Conjecture 2.1 (Crystalline ⟷ Good Reduction).** $C$ is crystalline iff it admits a *good reduction* — i.e., there exists a stabilizer code $\overline{C}$ over $\mathbb{F}_p$ (characteristic $p$) whose Witt vector lift $W(C)$ recovers $C$.

**Proof Sketch (Direction ⇒):**

1. If $V_C$ is crystalline, then $D_{\text{crys}}(V_C) = (V_C \otimes B_{\text{crys}})^{G_{\mathbb{Q}_p}}$ is a filtered $\varphi$-module with $\dim D_{\text{crys}} = \dim V_C$.
2. Since $D_{\text{crys}}(V_C)$ is a $W(\mathbb{F}_p)[F]$-module, we can reduce it modulo $p$ to obtain a module $\overline{D}$ over $\mathbb{F}_p[F]$.
3. The mod-$p$ reduction of the Frobenius operator $F$ on $\overline{D}$ defines a stabilizer code $\overline{C}$ over $\mathbb{F}_p$ via the correspondence in Conjecture 3.2 of `conjectures-formal.tex` (Frobenius as Clifford conjugation).
4. The Witt vector lift of $\overline{C}$ via Teichmüller representatives recovers $C$ exactly because the crystalline condition ensures no ramification in the lift.

**Proof Sketch (Direction ⇐):**

1. If $C$ has good reduction $\overline{C}$ over $\mathbb{F}_p$, then $D(C) \cong W(\mathbb{F}_p) \otimes_{\mathbb{F}_p} \overline{D}$ for some $\mathbb{F}_p[F]$-module $\overline{D}$.
2. The Frobenius $F$ acts $\sigma$-semilinearly on $D(C)$, where $\sigma$ is the Witt vector Frobenius.
3. The crystalline period ring $B_{\text{crys}}$ is precisely the universal ring containing $W(\mathbb{F}_p)$ with a Frobenius lift. Thus $D(C) \otimes_{W(\mathbb{F}_p)} B_{\text{crys}}$ has a natural $G_{\mathbb{Q}_p}$-action, and $V_C$ is crystalline by construction.

**Gap to Fill:** The correspondence between mod-$p$ stabilizer codes and $\mathbb{F}_p[F]$-modules needs to be made explicit. Specifically: given a stabilizer group $S \subset \mathcal{P}_n^{(p)}$, what is the associated Frobenius module structure?

**Edge Cases:**
- CSS codes: expected to be crystalline (integer Dieudonné-Manin slopes)
- Surface codes: expected to be crystalline (topological nature implies good reduction)
- Color codes: expected to be crystalline (defined by lattice cohomology)

### 2.2 Semistable Codes

**Definition 2.2 (Semistable Code).** A stabilizer code $C$ is *semistable* if its associated Galois representation $V_C$ is semistable. Equivalently:

$$\dim_{\mathbb{Q}_p} V_C = \dim_{\mathbb{Q}_p} (V_C \otimes_{\mathbb{Q}_p} B_{\text{st}})^{G_{\mathbb{Q}_p}}$$

**Conjecture 2.2 (Semistable ⟷ Allowed Monodromy).** $C$ is semistable iff it admits a *semistable reduction* — the stabilizer group has a nilpotent deformation ("monodromy operator") that does not affect the crystalline part of the code.

**Proof Sketch (Inclusion $\mathcal{C}_{\text{crys}} \subset \mathcal{C}_{\text{st}}$):**

1. Since $B_{\text{crys}} \subset B_{\text{st}}$ is a natural inclusion of period rings, we have:

$$(V_C \otimes B_{\text{crys}})^{G_{\mathbb{Q}_p}} \subset (V_C \otimes B_{\text{st}})^{G_{\mathbb{Q}_p}}$$

2. If $\dim (V_C \otimes B_{\text{crys}})^{G_{\mathbb{Q}_p}} = \dim V_C$ (crystalline condition), then $\dim (V_C \otimes B_{\text{st}})^{G_{\mathbb{Q}_p}} = \dim V_C$ as well (semistable condition always holds for crystalline representations).
3. Thus every crystalline code is semistable: $\mathcal{C}_{\text{crys}} \subset \mathcal{C}_{\text{st}}$. ✅

This inclusion is **rigorous** in Fontaine's theory and does not depend on the quantum code interpretation — it follows purely from the properties of period rings.

**Semistable but NOT Crystalline: The Monodromy Operator.**

A semistable code $C$ (not crystalline) has a *monodromy operator*:

$$N: D_{\text{st}}(V_C) \to D_{\text{st}}(V_C), \quad N\varphi = p\varphi N$$

where $\varphi$ is the Frobenius on $D_{\text{st}}$.

**QEC Interpretation:** The monodromy operator $N$ corresponds to a **Clifford deformation family** — a one-parameter group of Clifford transformations $U(t) = e^{t\mathcal{N}}$ where $\mathcal{N}$ is a Clifford generator (analog of the nilpotent monodromy operator), such that $C(t) = U(t) C U(t)^{\dagger}$ is a continuous deformation of the code.

**Prediction 2.1.** Semistable non-crystalline codes correspond to code families with *flexible parameters* — codes whose stabilizer weights can be continuously tuned without changing the code dimension $k$.

### 2.3 De Rham Codes

**Definition 2.3 (De Rham Code).** A stabilizer code $C$ is *de Rham* if its associated Galois representation $V_C$ is de Rham (equivalently, Hodge-Tate with positive Hodge-Tate weights that are integers).

**Conjecture 2.3 (De Rham ⟷ Admissible Codes).** All stabilizer codes that are constructible from the p-adic analytic category are de Rham. Conversely, every de Rham code is "physically realizable" in the p-adic framework.

**Proof Sketch (Inclusion $\mathcal{C}_{\text{st}} \subset \mathcal{C}_{\text{dR}}$):**

1. Fontaine proved that $B_{\text{st}} \subset B_{\text{dR}}$, so $(V \otimes B_{\text{st}})^{G_{\mathbb{Q}_p}} \subset (V \otimes B_{\text{dR}})^{G_{\mathbb{Q}_p}}$.
2. If $V$ is semistable, then $\dim (V \otimes B_{\text{st}})^{G} = \dim V$, which forces $\dim (V \otimes B_{\text{dR}})^{G} = \dim V$.
3. Thus $\mathcal{C}_{\text{st}} \subset \mathcal{C}_{\text{dR}}$. ✅

This inclusion is also **rigorous** in Fontaine's theory.

**Conjecture 2.4 (Hodge-Tate Weights as Stabilizer Gradings).** The Hodge-Tate weights $h_1, \ldots, h_{\dim V_C}$ of $V_C$ correspond to the **weights of the stabilizer generators** of $C$ — i.e., the number of non-identity Pauli operators in each generator.

**Prediction 2.2.** For a surface code on an $L \times L$ lattice:
- $h_{\text{min}} = 0$ (vertex and plaquette operators of weight 4)
- $h_{\text{max}} = L$ (logical operators)
- The spread $h_{\text{max}} - h_{\text{min}} = L$ controls the code distance.

---

## 3. The Full Filtration Theorem

**Theorem 3.1 (Fontaine Filtration for Quantum Codes).** `[speculative]`

The following strict inclusions hold:

$$\emptyset \subsetneq \mathcal{C}_{\text{crys}} \subsetneq \mathcal{C}_{\text{st}} \subsetneq \mathcal{C}_{\text{dR}} \subsetneq \mathcal{C}_{\text{all}}$$

where $\mathcal{C}_{\text{all}}$ is the set of all stabilizer codes over $\mathbb{F}_p$.

**Evidence for Strictness:**

1. **$\mathcal{C}_{\text{crys}} \neq \emptyset$:** CSS codes exist and are conjectured crystalline. Concrete example: the Steane $[[7,1,3]]_2$ code.

2. **$\mathcal{C}_{\text{st}} \setminus \mathcal{C}_{\text{crys}} \neq \emptyset$ (conjectured):** Concatenated codes (e.g., Shor's 9-qubit code = concatenation of 3-qubit bit-flip and phase-flip codes) are expected to be semistable but not crystalline, because the concatenation introduces ramification in the p-adic lift.

3. **$\mathcal{C}_{\text{dR}} \setminus \mathcal{C}_{\text{st}} \neq \emptyset$ (conjectured):** Random stabilizer codes with arbitrary Clifford deformations are expected to be de Rham but not semistable, because they lack a well-defined Frobenius action and monodromy operator.

4. **$\mathcal{C}_{\text{all}} \setminus \mathcal{C}_{\text{dR}} \neq \emptyset$ (conjectured):** Codes defined over non-p-adic completions (e.g., $\mathbb{R}$-based codes) may not have p-adic Hodge-Tate representations, placing them outside $\mathcal{C}_{\text{dR}}$.

---

## 4. Connection to Dieudonné-Manin Slopes

**Conjecture 4.1 (Slope-Code Class Correspondence).** Let $C$ be a stabilizer code with Dieudonné module $D(C)$. Then:

| Condition on $D(C)$ | Code Class |
|:---|:---|
| All slopes are integers | $C \in \mathcal{C}_{\text{crys}}$ |
| All slopes are integers or have denominator dividing the ramification index | $C \in \mathcal{C}_{\text{st}}$ |
| No restriction on slopes | $C \in \mathcal{C}_{\text{dR}}$ |

**Proof Sketch (Slopes → Crystalline):**

1. The Dieudonné-Manin theorem decomposes $D(C) \otimes \mathbb{Q}_p = \bigoplus_{\lambda} D_{\lambda}$ where $\lambda \in \mathbb{Q}$.
2. A crystalline representation has integer Hodge-Tate weights, and the Newton polygon (slopes) lies on or above the Hodge polygon.
3. For crystalline codes, the condition $\operatorname{Newton} \geq \operatorname{Hodge}$ with integer Hodge weights forces integer slopes.
4. The converse: integer slopes → crystalline, follows from the fact that the Frobenius action is semisimple on components with integer slopes, allowing a good reduction.

**Gap to Fill:** The Hodge polygon for stabilizer codes needs a concrete definition in terms of code parameters $[[n,k,d]]$.

---

## 5. Computational Verification Plan

### 5.1 Using `dieudonne_slope_classifier.py`

The Phase 2 prototype already implements slope computation. To verify the classification:

```python
from dieudonne_slope_classifier import DieudonneModule, CodeClassification

# Test on known code families
families = {
    "steane_7_1_3": DieudonneModule.for_steane(),
    "surface_5x5": DieudonneModule.for_surface(5),
    "shor_9_1_3": DieudonneModule.for_shor(),
    "random_10_2_3": DieudonneModule.random(10, 2),
}

for name, dm in families.items():
    slopes = dm.slope_decomposition()
    classification = CodeClassification.classify(dm)
    print(f"{name}: slopes={slopes}, class={classification}")
```

**Expected Outcomes:**
- `steane_7_1_3`: integer slopes → CRYSTALLINE
- `surface_5x5`: integer slopes → CRYSTALLINE
- `shor_9_1_3`: mixed slopes → SEMISTABLE (to verify)
- `random_10_2_3`: fractional slopes → DE RHAM (to verify)

### 5.2 Falsifiability

The theorem is falsified if:
1. A code proven to be crystalline by Fontaine's criteria has non-integer Dieudonné-Manin slopes.
2. A code with integer slopes fails to have good reduction (cannot be lifted from characteristic $p$).
3. The inclusions are not strict for any known code family (i.e., all codes are found to be in the same class).

---

## 6. Relationship to Other Pillars

### 6.1 Pillar II (Hasse Principle)

The Fontaine classification enables a refined Hasse principle: a global code (over $\mathbb{Q}$) is crystalline iff it is crystalline at every prime $p$. The set of primes where a code is semistable but not crystalline is the **ramified set** — analogous to the set of primes of bad reduction for an elliptic curve.

### 6.2 Pillar IV (Class Field Theory)

The crystalline/de Rham distinction connects to the Artin reciprocity map: crystalline codes have **unramified** measurement group structure, while semistable codes have **tamely ramified** structure and general de Rham codes may be wildly ramified.

### 6.3 Pillar VI (Witt Cohomology)

The Dieudonné module $D(C)$ is the central object connecting all three:
- $D(C) \otimes B_{\text{crys}}$ → crystalline structure
- $D(C) \otimes B_{\text{st}}$ → semistable structure
- $D(C) \otimes B_{\text{dR}}$ → de Rham structure

### 6.4 Pillar VII (BT Buildings)

The Moy-Prasad depth $r(\pi)$ of the representation $\pi$ associated to $C$ relates to the Fontaine classification:
- $r = 0$ (depth-zero representations) → crystalline codes
- $0 < r < 1$ → semistable codes
- $r \geq 1$ → de Rham codes

---

## 7. Next Steps

1. **Rigorous proof of $\mathcal{C}_{\text{crys}} \subset \mathcal{C}_{\text{st}} \subset \mathcal{C}_{\text{dR}}$:** The two inclusions follow from Fontaine's period ring theory and are essentially proven. What needs work: the strictness proofs (exhibiting codes in each class).

2. **Construct a semistable non-crystalline code:** The Shor 9-qubit code is the leading candidate. Need to compute its monodromy operator $N$ explicitly.

3. **Construct a de Rham non-semistable code:** A randomly generated stabilizer code with non-trivial Clifford deformation group. The `dieudonne_slope_classifier.py` should generate test cases.

4. **Prove the slope-code class correspondence (Conjecture 4.1):** This requires connecting the Dieudonné-Manin classification of $D(C)$ to Fontaine's period ring characterization.

5. **Integrate with `conjectures-formal.tex`:** Add these results as Sections 5-7 of the existing LaTeX document.

---

## References

- Fontaine, J.-M. (1994). *Le corps des périodes p-adiques.* Astérisque, 223.
- Fontaine, J.-M., & Mazur, B. (1993). Geometric Galois representations. *Elliptic Curves, Modular Forms, & Fermat's Last Theorem.*
- Kedlaya, K. S. (2010). *p-adic Differential Equations.* Cambridge.
- Berger, L. (2004). An introduction to the theory of p-adic representations. *Geometric Aspects of Dwork Theory.*
- Cais, B. (2010). Canonical integral structures on the de Rham cohomology of curves. *Annales de l'Institut Fourier.*

---

*Phase 3 Document v1.0 — Two inclusions are rigorous (from Fontaine theory). Strictness conjectured. Slope correspondence requires formal proof.*
