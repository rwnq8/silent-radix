# CYCLIC MEASUREMENT: Positional Notation as Ultrametric Time Trees

**Author:** QNFO Research | **Date:** 2026-06-29 | **Status:** Draft v0.1

---

## Abstract

This paper presents three related theses on the structure of measurement, time, and computation. Thesis I argues that positional notation is a rooted tree of nested time-cycles whose native geometry is ultrametric — the distance between two numerals is the depth of their shared nesting. The historical "silent radix" is diagnosed as the erasure of this cyclic structure through flattening into an Archimedean line. Thesis II extends this to physics: from the Zitterbewegung of the Dirac electron to cyclic cosmological models, time manifests as a hierarchy of nested cycles, and the Big Bang is a phase boundary, not an origin. Thesis III proposes that the ultrametric tree is a native model of computation — where cyclic codes, hierarchical memory, and self-referential measurement form a unified architecture in which the observer is constituted by the act of counting cycles.

---

## THESIS I: Positional Notation as a Tree of Cyclic Time

### 1. The Tree Structure of Positional Notation

Positional notation constructs a rooted tree where each level's branching factor is the radix. Given a base $b$, the numeral $d_n d_{n-1} \ldots d_1 d_0$ defines a path from root to leaf through $n+1$ levels, with $b$ branches at each level. The root corresponds to zero (the unmarked state), and each digit $d_k \in \{0, 1, \ldots, b-1\}$ selects a branch at level $k$.

This correspondence is mathematically established through $p$-adic visualization [Holly 2001]. For the ring of integers under the $p$-adic metric, an integer $x$ is located according to its power series representation $x = \sum_{n=0}^{\infty} a_n p^n$, with $a_n \in \{0, 1, \ldots, p-1\}$. The tree is constructed from the root with $p$ paths according to $a_0$, then level 1 with $p$ paths according to $a_1$, and so on.

### 2. The Native Ultrametric

The distance function on this tree is:

$$d(x, y) = p^{-n_0}$$

where $a_i = b_i$ for $i = 0, 1, \ldots, n_0 - 1$ and $a_{n_0} \neq b_{n_0}$. This is the ultrametric of shared nesting depth — the number of matching trailing digits. It satisfies the strong triangle inequality $d(x, z) \leq \max\{d(x, y), d(y, z)\}$ [established], which distinguishes ultrametric from Euclidean geometry.

The generalization to symbolic ultrametrics is well-established: Böcker and Dress introduced two-way symmetric maps whose range is an arbitrary set of symbols, extending ultrametricity beyond real-valued distances [Huber, Moulton, & Scholz 2017]. These define edge-colored complete graphs representable as vertex-colored trees.

**Thesis claim:** The ultrametric is not merely a visualization convenience — it is the native geometry of the numeral. The Euclidean line is a secondary projection. [my conjecture]

### 3. The Silent Radix Error

The historical transition from mixed-radix systems (Babylonian sexagesimal, Mayan base-20/18) to monocultural decimal erased the cyclic structure of measurement and replaced it with an unmarked default [established from historical record]. The decimal system displaced native scales across Polynesia and Africa via trade routes [established].

The "silent radix error" is the thesis's diagnostic term for this erasure: by making the base invisible, the notation pretends there is no boundary-crossing between levels. The number appears as a static object on a line rather than a dynamic process of counting cycles. [my conjecture]

### 4. Zero as the Unmarked State

Manca (2015) proves that zero is not necessary for positional representation — a zero-free positional representation retains all essential properties of classical base-$k$ notation. This challenges the "common belief" that zero is intrinsic to positional notation [established].

The thesis interprets zero constructively: zero is the deliberate marking of absence, the explicit representation of the unmarked state within the marked system. The Indian invention of zero was the moment the tree became fully explicit — it allowed branches that went unactivated while deeper levels were active [my conjecture].

### 5. The Re-entrant "10" as Minimal Observer

In base $b$, the numeral "10" means: one cycle at the next level, zero cycles at the current level. But this numeral is written in the notation whose base is $b$. So "10" is self-referential — it is the point in the tree where a cycle completes and is counted as a unit of the next level.

In Spencer-Brown's Laws of Form (1969), the re-entrant form $f = \neg f$ is a distinction that re-enters its own space, producing oscillation — interpreted as memory, self-reference, and the genesis of time. The string "10" is a stable re-entrant form: the cycle that marks its own completion. [my conjecture]

### 6. Seven Principles for Cyclic-Frame Quantitative Practice

1. **Cyclic Grounding:** Every numeral shall declare the cycles it counts. The base(s) shall correspond to observed or chosen periodicities.
2. **Explicit Frame:** No number shall be transmitted without its radix, metric, unit, and scale type. The frame is part of the number's identity.
3. **Native Ultrametric:** The default distance between numerals is the ultrametric of shared nesting depth. Any other metric requires explicit, justified transformation.
4. **Included Observer:** The act of counting cycles shall be represented within the notation. "10" is the minimal mark of the observer.
5. **Unmarked Root:** Zero is the unmarked state, the root of the measurement tree.
6. **Arithmetic Invariance:** The laws of arithmetic hold across all frames, but interpretation depends on the frame.
7. **Layered Abstraction:** The Archimedean line and real numbers are legitimate derived abstractions, flagged as secondary projections.

---

## THESIS II: Time as Cycles — From Zitterbewegung to the Cosmos

### 1. The Compton Clock

De Broglie's association of a wave with every particle implies that massive particles possess an intrinsic periodicity — the "Compton clock" [de Broglie 1924]. The Compton frequency for a stationary massive particle is:

$$f = \frac{mc^2}{h}$$

Each massive particle is a quantum clock that ticks once every reduced Compton time period. Electron channeling experiments provide direct evidence of this periodicity [Canadian Journal of Physics 2018].

**Thesis claim:** Mass is not a static property but a frequency — a rate of cycling. [speculative]

### 2. Zitterbewegung as the Fundamental Temporal Cycle

Schrödinger's analysis of the Dirac equation predicted a rapid oscillatory motion of elementary particles at angular frequency $\omega = 2mc^2 / \hbar$ — twice the Compton angular frequency [Schrödinger 1930]. This Zitterbewegung ("trembling motion") arises from quantum interference between positive and negative energy states.

Recent theoretical work by de la Peña, Cetto, and Valdés-Hernández (2020) proposes that the duration of atomic quantum jumps is determined by a resonance of the atomic electron with modes of the zero-point radiation field at the Compton frequency. Their result, approximately $(\alpha \omega_C)^{-1}$ where $\alpha$ is the fine structure constant, yields attosecond-scale durations — consistent with experimental estimates [speculative].

### 3. Zitterbewegung as Cosmological Oscillation

A remarkable development by Toupin (2026) proves that the Zitterbewegung of a free Dirac fermion is "the physical signature of oscillation across the cosmological time-reversal boundary." In a T-symmetric cosmology, negative-energy solutions — identified via the Feynman-Stueckelberg correspondence as particles propagating on the opposite side of the $t=0$ boundary — interfere with positive-energy components to produce the observed trembling [speculative].

Consequences proven as theorems include: both fermion helicities are observed because the oscillation samples both sides within every Compton cycle; the $4\pi$ periodicity of spin-½ arises from the two-sheeted topology; the Majorana condition is forced by boundary geometry; the massless lightest neutrino is predicted by Bott periodicity [speculative].

### 4. The Middle Scales

The nested-cycle structure extends through all scales:
- **Atomic transitions:** Quantum jump durations are finite, determined by resonance with the zero-point field [de la Peña et al. 2020].
- **Biological rhythms:** Circadian, lunar, and seasonal cycles entrain organisms [established].
- **Calendar systems:** Hour within day within week within month — explicit cyclic bases [established].

**Thesis claim:** The Archimedean line is a flattening of this nested structure — a projection that erases the cyclic origin of time at every scale. [my conjecture]

### 5. Cyclic Cosmology

In ekpyrotic and cyclic cosmologies, the Big Bang is described as a collision of branes in higher-dimensional space — "the big bang is not the beginning of time" [Lehners 2008]. Before the Big Bang, an ekpyrotic phase with $w = P/\rho \gg 1$ slowly contracts the universe, resolving standard cosmological puzzles and generating a nearly scale-invariant perturbation spectrum [speculative].

Penrose's Conformal Cyclic Cosmology proposes infinite aeons, each conformally connected to the previous one [Penrose 2010, speculative]. Loop Quantum Cosmology replaces the classical singularity with a quantum bounce [speculative]. A 2026 study in modified teleparallel gravity estimates a full cycle duration of approximately 55.1 Gyr [Physics Letters A 2026, speculative].

**Thesis claim:** The Big Bang is not the origin of time but a transition — the cosmological analogue of "10," marking the completion of one cycle and the commencement of the next. [my conjecture]

### 6. Unified Thesis

Time is a hierarchy of nested cycles, from the Zitterbewegung of the quantum vacuum to the cosmic cycles of universal expansion and contraction. Every massive particle is a clock ticking at its Compton frequency. The Zitterbewegung is the signature of oscillation across the cosmological time-reversal boundary. All temporal measurement is counting cycles. The Archimedean line is a derived abstraction — a limit where cycle durations go to zero.

---

## THESIS III: The Ultrametric Tree as a Native Model of Computation [PHILOSOPHY]

### 1. Cyclic Codes and Hierarchical Memory

If positional notation is a tree of cycles and time is a hierarchy of nested frequencies, then computation itself can be understood as navigation within an ultrametric tree. This thesis proposes that:

**Cyclic codes** — error-correcting codes defined over finite fields — are formal analogues of positional trees. A cyclic code of length $n$ over $\mathbb{F}_q$ is an ideal in the ring $\mathbb{F}_q[x]/(x^n - 1)$. The factorization of $x^n - 1$ defines a hierarchical decomposition that mirrors the tree structure of positional notation [established for cyclic codes; the tree interpretation is my conjecture].

**Hierarchical memory** — the organization of storage and retrieval by nested cycles — maps naturally onto ultrametric trees. A memory system organized by shared temporal depth (cache lines within pages within segments) is an ultrametric structure. The native distance between two memory addresses is the depth of their shared hierarchy, not their linear offset [my conjecture].

### 2. Self-Referential Measurement as Computation

In Laws of Form, the re-entrant form generates oscillation — and oscillation is the primitive of computation. A system that can mark the completion of its own cycles can:
- **Count:** Distinguish between states by accumulated cycles
- **Compare:** Detect shared nesting depth (ultrametric similarity)
- **Recurse:** Apply the same counting operation at each level of the tree

This is the architecture of the observer: a self-referential measurement system that navigates an ultrametric tree of nested cycles. The observer is not external to the computation — the observer IS the re-entrant form that marks cycle completions [my conjecture].

### 3. Implications for AI and Cognitive Architecture

Dehaene's logarithmic compression of number sense can be reinterpreted as tree perception — a clustering of quantities by order of magnitude, which is an ultrametric grouping [speculative]. If the brain's number sense is a tree perception rather than a line perception, then cognitive architectures built on ultrametric trees may be more neurologically plausible than those built on Euclidean embeddings [my conjecture].

Temporal hierarchical clustering — investigated by Dey, Rossi, and Sidiropoulos (2017) — provides algorithmic support: hierarchical clusterings of metric spaces that change over time can be encoded by embedding point sets into ultrametric spaces, which naturally induce hierarchical clusterings [established].

### 4. The Three Theses Unified

| Thesis | Domain | Core Claim | Geometry |
|:-------|:-------|:-----------|:---------|
| **I** | Measurement | Positional notation is a tree of nested cycles | Ultrametric |
| **II** | Physics | Time is a hierarchy of nested frequencies | Cyclic |
| **III** | Computation | Observation is self-referential cycle-counting | Tree-based |

All three converge on a single architecture: the ultrametric tree as the native structure of measurement, time, and computation. The observer is constituted by the act of distinguishing and counting cycles — the minimal act of computation. The Archimedean line is a derived projection that erases this structure. Recovering the tree recovers the observer, the time-structure of the measured world, and the computational foundation of self-reference.

---

## GAPS AND LIMITATIONS

Several claims in this paper represent novel syntheses rather than established findings:

1. The identification of positional notation's tree with time specifically is the paper's most original but least empirically grounded claim. While $p$-adic tree visualization is established, its interpretation as a "time tree" is a philosophical extension [my conjecture].

2. The "silent radix error" as a named phenomenon does not appear in the historical or mathematical literature. It is this paper's diagnostic term [my conjecture].

3. The empirical claim about the brain's number sense being "ultrametric" remains speculative. While logarithmic compression is well-documented [Dehaene, established], its formalization as ultrametric tree perception is not [my conjecture].

4. The Zitterbewegung as oscillation across a cosmological time-reversal boundary is a single paper's result [Toupin 2026, speculative] and has not been independently verified.

5. Thesis III is philosophical in character [PHILOSOPHY]. The mapping between cyclic codes and positional trees is a formal analogy, not a proven equivalence. This thesis would be disconfirmed if cyclic codes were shown to have no natural hierarchical decomposition corresponding to the tree structure of numerals [not yet falsifiable in current form].

---

## References

1. Holly, J. E. (2001). Pictures of ultrametric spaces, the $p$-adic numbers, and valued fields. *American Mathematical Monthly*, 108(8), 721–728. Zbl 1039.12003.

2. Huber, K. T., Moulton, V., & Scholz, G. E. (2017). Three-way symbolic tree-maps and ultrametrics. arXiv:1707.08010.

3. Dey, T. K., Rossi, A., & Sidiropoulos, A. (2017). Temporal Hierarchical Clustering. arXiv:1707.09904.

4. Manca, V. (2015). On the lexicographic representation of numbers. arXiv:1505.00458.

5. Spencer-Brown, G. (1969). *Laws of Form*. George Allen and Unwin.

6. de la Peña, L., Cetto, A. M., & Valdés-Hernández, A. (2020). How fast is a quantum jump? arXiv:2009.02426.

7. Lehners, J.-L. (2008). Ekpyrotic and Cyclic Cosmology. arXiv:0806.1245.

8. Toupin, D. (2026). Zitterbewegung as Oscillation Across the Cosmological Time-Reversal Boundary. PhilPapers.

9. Anisotropic cyclic cosmology in $f(T)$ gravity: A Bianchi type-II framework for periodic big bang big crunch evolution. *Physics Letters A*, 586, 131681 (2026).

10. de Broglie clock, electron channeling, and time in quantum mechanics. *Canadian Journal of Physics* (2018).

11. Penrose, R. (2010). *Cycles of Time: An Extraordinary New View of the Universe*. Bodley Head.

12. Dehaene, S. (2011). *The Number Sense: How the Mind Creates Mathematics*. Oxford University Press.

13. Schrödinger, E. (1930). Über die kräftefreie Bewegung in der relativistischen Quantenmechanik. *Sitzungsberichte der Preußischen Akademie der Wissenschaften*, 418–428.

14. de Broglie, L. (1924). *Recherches sur la théorie des quanta*. PhD Thesis, Université de Paris.

15. Feynman, R. P. (1949). The theory of positrons. *Physical Review*, 76(6), 749–759.

16. Stueckelberg, E. C. G. (1941). Remarque à propos de la création de paires de particules en théorie de relativité. *Helvetica Physica Acta*, 14, 588–594.

---

*Generated under QNFO Research Integrity Mandate (QNFO-POL-COM-001). Certainty labels applied throughout.*
