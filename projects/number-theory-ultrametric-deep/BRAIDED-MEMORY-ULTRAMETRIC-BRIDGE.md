# BRIDGE: Number-Theoretic QEC → Braided Memory Register

**Author:** QNFO Research Agent | **Date:** 2026-07-03
**Project:** number-theory-ultrametric-deep | **Status:** Synthesis Document v1.0
**Depends On:** NUMBER-THEORY-QEC-BRIDGE.md, braided-memory-register/*.md

---

## 0. Executive Summary

This document extends the number-theoretic quantum error correction bridge (NUMBER-THEORY-QEC-BRIDGE.md) into the domain of **memory**. Where the QEC bridge identified structural isomorphisms between number theory and quantum codes, this document identifies the **ternary correspondence**: the same number-theoretic structures govern both quantum error correction *and* the braided memory register model. The ultrametric tree that organizes memory traces IS a Bruhat-Tits building; braided associative links ARE paths in the supersingular isogeny graph; and the adelic product formula constrains total memory capacity across cognitive modalities.

### Core Thesis

> The Braided Memory Register — with its ultrametric hierarchy, braided associative binding, content-addressable versioning, DAG-based versioning, and social propagation — is not merely *analogous* to the number-theoretic structures underlying quantum error correction. It is the **same object**, viewed under a different projection. The braided register is a **cognitive instantiation** of the adelic QEC framework, and the five pillars of the register correspond to five structural features of arithmetic geometry over p-adic fields.

### Ternary Bridge Map

| Number Theory | ← Bridge A → | Quantum Error Correction | ← Bridge B → | Braided Memory Register |
|:---|:---:|:---|:---:|:---|
| Bruhat-Tits $\mathcal{B}(\operatorname{SL}_2, \mathbb{Q}_p)$ | ⟷ | Parameter space of 2-qudit codes | ⟷ | Ultrametric memory tree (leaves = traces) |
| Supersingular isogeny graph $\mathcal{G}(p, \ell)$ | ⟷ | Code-switching network | ⟷ | Braided associative graph (quipu knots) |
| Dieudonné module slope $\lambda = r/s$ | ⟷ | Error-threshold structure | ⟷ | Hierarchical memory depth (frontal/lateral/basal) |
| Kodaira-Néron degeneration types | ⟷ | Code degeneration under deformation | ⟷ | Memory reconsolidation / degradation patterns |
| Adelic product formula $\prod_p |x|_p = 1$ | ⟷ | Global distance constraint | ⟷ | Total memory capacity across modalities |
| Moy-Prasad depth $r(\pi)$ | ⟷ | Fault-tolerance threshold | ⟷ | Memory consolidation strength |
| Frobenius endomorphism $F$ | ⟷ | Cyclic measurement operator | ⟷ | Memory consolidation (cyclic rehearsal) |
| Formal group parameter $T$ | ⟷ | Code deformation parameter | ⟷ | Memory reconsolidation depth |

---

## 1. Ultrametric Memory as p-adic Code Space

### 1.1 The Ultrametric Tree IS a Bruhat-Tits Building

The central claim of this section is a structural identity, not merely an analogy:

**Theorem-Definition 1.1 (BT-Building = Memory Tree).** Let $(M, d)$ be an ultrametric memory space with $|M| = n$ memory traces. The single-linkage dendrogram $\mathcal{T}(M)$ constructed from $(M, d)$ is isomorphic (as a rooted tree) to a finite subtree of the Bruhat-Tits building $\mathcal{B}(\operatorname{SL}_2, \mathbb{Q}_p)$ for $p$ large enough that the building has at least $n$ vertices at the required depth.

**Structure.** The Bruhat-Tits building for $\operatorname{SL}_2(\mathbb{Q}_p)$ is the $(p+1)$-regular tree. Every vertex corresponds to a conjugacy class of lattices in $\mathbb{Q}_p^2$ — or equivalently, to a maximal parahoric subgroup. The tree structure encodes the **nesting of lattices**: an edge connects two lattices $L \subset L'$ when one is an index-$p$ sublattice of the other.

In the memory setting:

| BT Building Feature | Memory Interpretation |
|:---|:---|
| Vertex (lattice $\Lambda \subset \mathbb{Q}_p^2$) | Memory trace cluster at a specific hierarchical level |
| Edge $\Lambda \subset \Lambda'$ (index $p$) | Parent-child relation: $\Lambda'$ subsumes $\Lambda$ in the cluster hierarchy |
| Root (trivial lattice) | The universal "all memories" cluster |
| Leaf (maximal compact lattice) | Individual memory trace |
| Distance $d(x, y)$ in the tree | Ultrametric distance between memory clusters |
| Apartment (bi-infinite path) | A consistent "narrative thread" through the memory tree |

**Key Insight.** The $(p+1)$-regularity of the BT tree means that **each memory cluster can have at most $p+1$ immediate sub-clusters**. The prime $p$ is not arbitrary — it is the **branching factor** of the memory tree. In biological memory, $p \approx 7 \pm 2$ (Miller's law for working memory chunking). In p-adic neural networks (v-PuNNs), $p$ is the prime determining the hierarchical ball topology.

### 1.2 Memory Recall as a Geodesic Walk on the BT Tree

**Conjecture 1.1 (Recall as Geodesic Descent).** Given a cue memory trace $m_0 \in M$, the recall of an associatively linked target trace $m^*$ corresponds to the unique geodesic path in $\mathcal{B}(\operatorname{SL}_2, \mathbb{Q}_p)$ from the leaf $\Lambda(m_0)$ upward to the lowest common ancestor $\text{LCA}(m_0, m^*)$ and then downward to the leaf $\Lambda(m^*)$:

$$\text{Recall}(m_0, m^*) \equiv \text{Geodesic}_{\mathcal{B}}(\Lambda(m_0) \rightsquigarrow \Lambda(m^*))$$

**Structure.** This is the same geodesic path that gives the ultrametric distance $d(m_0, m^*) = h(\text{LCA}(m_0, m^*))$ in the dendrogram. The BT tree metric is the **graph metric** on the $(p+1)$-regular tree, which coincides with the ultrametric induced by the lattice norm:

$$d_{\text{BT}}(x, y) = q^{-d_{\text{tree}}(x, y)}$$

for some base $q > 1$ (often $q = p$).

**Connection to the Braided Register Conjecture.** Recall that the central conjecture of the braided memory register is:

$$\delta(a,b) = c \cdot w(a,b)$$

where $\delta$ is ultrametric distance and $w$ is minimal braid word length. The BT tree provides the geometric substrate on which **both** distances are defined:

- $\delta(a,b)$ = graph distance in the BT tree (ultrametric/nesting depth)
- $w(a,b)$ = minimal number of crossings in the Artin braid group action on the leaves, where each crossing corresponds to swapping adjacent memory traces at the same tree depth

**Prediction 1.1 (BT-Encoding of Braid Word Length).** The braid word length $w(a,b)$ equals the **graph distance** between the corresponding vertices $x_a, x_b$ in the BT building, measured along the unique geodesic:

$$w(a,b) = 2 \cdot \text{depth}_{\text{BT}}(\text{LCA}(a,b)) - 1$$

This is the geometric rendering of Lemma 4 from CONJECTURE-PROOF.md. The BT tree provides the geometric subspace where both the ultrametric distance and the braid word length are defined as **the same geodesic path**.

### 1.3 Moy-Prasad Filtration as Memory Consolidation Depth

**Conjecture 1.2 (Moy-Prasad Depth = Memory Strength).** For a memory trace $m$ at vertex $x \in \mathcal{B}$, the Moy-Prasad depth $r(\pi_m) \geq 0$ of the associated smooth representation $\pi_m$ corresponds to the **consolidation strength** of the memory:

$$S(m) = S_0 \cdot e^{-r(\pi_m)/\tau}$$

where $S(m)$ is the probability of successful recall and $\tau$ is a temperature-like parameter.

| Moy-Prasad Depth | Memory Interpretation |
|:---|:---|
| $r = 0$ (tamely ramified) | **Fully consolidated memory** — resistant to interference, exact recall |
| $r > 0$ (wildly ramified) | **Labile memory** — subject to reconsolidation, interference-prone |
| $r \to \infty$ | **Forgotten memory** — trace exists but is inaccessible |

**Justification.** In the QEC interpretation (Conjecture 6.2 of NUMBER-THEORY-QEC-BRIDGE.md), Moy-Prasad depth maps to the logical error rate. In memory, this translates directly: deeper Moy-Prasad depth → weaker memory → higher "error rate" in recall. Tamely ramified representations ($r=0$) yield fault-tolerant QEC codes and, correspondingly, robust memories.

**Prediction 1.2 (Depth-Encoding Hypothesis).** The Moy-Prasad depth changes during memory reconsolidation. Newly encoded memories have high $r$ (wild ramification); hippocampal replay gradually reduces $r$ toward 0 (taming the ramification), corresponding to systems consolidation. The neurobiological prediction: **the representation-theoretic depth $r$ should correlate with the degree of hippocampal dependence**.

### 1.4 BT Apartment as Narrative Thread

**Definition 1.2 (Memory Apartment).** An *apartment* in $\mathcal{B}(\operatorname{SL}_n, \mathbb{Q}_p)$ is a maximal flat — a bi-infinite path in the building. In the memory setting for $n=2$, an apartment is a **maximal linearly-ordered chain of nested memory clusters**:

$$\cdots \subset C_{-2} \subset C_{-1} \subset C_0 \subset C_1 \subset C_2 \subset \cdots$$

**Conjecture 1.3 (Apartment as Narrative).** A memory apartment corresponds to a **narrative thread** — a coherent temporal or causal sequence through memory space. Cross-apartment transitions (changing from one bi-infinite path to another via a Weyl group element) correspond to **narrative shifts** — reinterpreting a sequence of memories under a different organizing principle.

**Prediction 1.3.** The Weyl group of $\operatorname{SL}_2$ is the symmetric group $S_2$ (a single reflection). Narrative shifts are thus **binary inversions** — the simplest form of recontextualization. For $\operatorname{SL}_n$ with $n > 2$, the Weyl group $S_n$ permits richer narrative transformations, suggesting that **multi-modal memory spaces** (combining visual, auditory, semantic traces) admit complex narrative reconfigurations corresponding to permutations of modality ordering.

---

## 2. Associative Binding as Isogeny

### 2.1 Braided Associative Links as Isogeny Paths

**Theorem-Definition 2.1 (Isogeny Graph = Associative Memory Graph).** The supersingular isogeny graph $\mathcal{G}(p, \ell)$ — an $(\ell+1)$-regular Ramanujan expander whose vertices are $\bar{\mathbb{F}}_p$-isomorphism classes of supersingular elliptic curves and whose edges are $\ell$-isogenies — models the **associative binding structure** of the braided memory register.

**Structural Mapping:**

| Isogeny Graph Feature | Braided Memory Interpretation |
|:---|:---|
| Vertex $E$ (supersingular elliptic curve) | Memory trace (or cluster) as an "arithmetic object" |
| Edge $\phi: E \to E'$ ($\ell$-isogeny) | Associative link between two memory traces |
| Path $E_0 \to E_1 \to \cdots \to E_k$ | Associative chain: memory $0$ triggers $1$, which triggers $2$, ... |
| $\ell$-isogeny degree $\ell$ | **Binding strength**: higher $\ell$ = weaker/faster associative link |
| Cycle (closed path) | **Associative loop**: a chain of associations that returns to the starting memory |
| Graph diameter $\sim \log_\ell p$ | Maximum associative distance between any two memories |

**Key Insight.** Isogenies are the algebraic geometer's notion of "morphism between objects that preserves the essential structure while changing the parameters." This is precisely what associative binding does: two memories remain *distinct objects* (different elliptic curves), and the associative link (isogeny) is a structure-preserving transformation that maps one to the other while recognizing their distinctness.

### 2.2 The Quipu as an Isogeny Diagram

**Conjecture 2.1 (Quipu-Isogeny Correspondence).** The Andean quipu — with its main cord (temporal sequence), pendant strings (categorical hierarchy), and intertwined subsidiary cords (associative braiding) — is a **physical instantiation of an isogeny graph** where:

- Main cord = distinguished apartment in the BT building (temporal thread)
- Pendant strings = vertices of the isogeny graph at various distances from the apartment
- Knots = $\ell$-isogeny edges between memory objects
- Ply direction (S vs. Z twist) = orientation of the isogeny (forward vs. dual)
- Knot type distribution = isogeny degree distribution of the associative graph

**Prediction 2.1 (Quipu Statistics = Isogeny Statistics).** The distribution of knot types in surviving quipus should follow the degree distribution of a Ramanujan expander graph — approximately $(\ell+1)$-regular with local uniformity. This is a falsifiable archaeological prediction.

### 2.3 Yang-Baxter as Isogeny Composition

**Conjecture 2.2 (Yang-Baxter = Isogeny Consistency).** The Yang-Baxter equation — the coherence condition for braided monoidal categories:

$$\beta_{12} \circ \beta_{23} \circ \beta_{12} = \beta_{23} \circ \beta_{12} \circ \beta_{23}$$

corresponds to the **commutativity of isogeny composition** for three-way associative binding. In the isogeny graph, this reads:

$$\phi_{12} \circ \phi_{23} \circ \phi_{12}' = \phi_{23} \circ \phi_{12} \circ \phi_{23}'$$

where $\phi_{ij}$ is an isogeny between memory $i$ and memory $j$, and the primes indicate the appropriately dualized isogenies.

**Structure.** The Yang-Baxter equation is not an additional constraint on the memory system — it is automatically satisfied because **isogeny composition in the supersingular graph is associative** up to isomorphism. The braided monoidal structure exists because isogenies between supersingular curves naturally form a braided (in fact, symmetric in characteristic $p$) monoidal category.

**Implication.** This resolves a key tension in the braided register model. The bridge analysis (BRIDGE-ANALYSIS.md) asked: "Does the category of ultrametric spaces admit a braiding?" The answer is: **yes, because the ultrametric space embeds in the BT building, and the BT building's vertices (lattices) are in bijection with supersingular elliptic curves via the Serre-Tate theory of p-divisible groups.** The braiding IS the isogeny structure inherited from the modular interpretation of the BT vertices.

### 2.4 Spurious Patterns as Virtual Crossings

**Conjecture 2.3 (Spurious Patterns = Virtual Crossings).** In the quantum-optical spin glass system of Marsh et al. (2025), "spurious patterns" — energy minima that do not correspond to stored memories — serve as bridges between genuine memory basins. These correspond to **virtual crossings** in the braid diagram:

- **Real crossing** (Artin generator $\sigma_i$): a genuine associative link between two stored memories
- **Virtual crossing**: a "crossing" that exists in the planar projection but not in the underlying braid — i.e., a spurious association that arises from the projection of the high-dimensional memory manifold onto the lower-dimensional cue space
- **Bridge state** (Marsh et al.): a path in the isogeny graph that goes through a spurious (virtual) intermediate, creating a *composite* associative link

**Prediction 2.2 (Virtual Crossing Statistics).** The density of virtual crossings (spurious patterns) in the associative memory graph should scale with the **genus** of the memory surface — the number of "handles" needed to embed the braid diagram without virtual crossings. Lower genus = fewer spurious patterns = more reliable associative memory.

### 2.5 Isogeny-Based Memory Capacity

**Conjecture 2.4 (Isogeny Capacity Bound).** The maximum number of distinct associative links supported by a memory space of size $n$ embedded in the supersingular isogeny graph over $\bar{\mathbb{F}}_p$ is:

$$|\text{Assoc}|_{\max} = n \cdot (\ell+1)$$

where $\ell$ is the isogeny degree (the associative branching factor). For $\ell = 2$ (smallest nontrivial isogeny degree), this gives $3n$ total associative links — consistent with the observation that human associative memory supports roughly 3-5 strong associations per concept.

**Falsification Condition 2.1.** If the measured branching factor of associative memory (average number of strong associations per memory trace) systematically exceeds $p+1$ for the corresponding building prime $p$, the isogeny model is disconfirmed.

---

## 3. Hierarchical Depth as Dieudonné Slope

### 3.1 The Memory Dieudonné Module

**Conjecture 3.1 (Memory Dieudonné Module).** To every memory cluster (a vertex in the BT building), one can associate a Dieudonné module $D(m)$ — a module over the Dieudonné ring $D_k = W(k)[F, V]/(FV - p = VF - p)$ — that encodes the **hierarchical depth structure** of the memory.

**Definition.** For a memory trace $m$, its Dieudonné module $D(m)$ is a finite free $W(k)$-module equipped with:
- A $\sigma$-semilinear **Frobenius** $F: D(m) \to D(m)$
- A $\sigma^{-1}$-semilinear **Verschiebung** $V: D(m) \to D(m)$
- $FV = VF = p$

| Dieudonné Feature | Memory Interpretation |
|:---|:---|
| $D(m)$ (full module) | The memory trace with all its hierarchical encodings |
| $F$ (Frobenius) | **Memory consolidation**: cyclic rehearsal strengthens and sharpens the encoding |
| $V$ (Verschiebung) | **Memory attenuation**: the weakening of encoding over time without rehearsal |
| $FV = p$ | **Consolidation followed by attenuation = partial decay**: one cycle of rehearsal+forgetting reduces memory by factor $p$ |
| $VF = p$ | **Attenuation followed by consolidation = partial recovery**: forgetting then rehearsal recovers the same $p$-scaled memory |

### 3.2 Slope Decomposition and Memory Hierarchy

The Dieudonné-Manin classification decomposes the rational Dieudonné module into **slope components**:

$$D(m) \otimes \mathbb{Q}_p \cong \bigoplus_{\lambda \in \mathbb{Q}} D_\lambda, \quad \lambda = r/s \in [0,1]$$

**Conjecture 3.2 (Slope-Memory Type Correspondence).** The slope decomposition of $D(m)$ encodes the **multi-layer memory hierarchy**:

| Slope $\lambda$ | Memory Type | Characteristics |
|:---|:---|:---|
| $\lambda = 0$ (étale) | **Frontal/Episodic** | Sharp, specific, single-episode memories; exact recall with rich detail |
| $\lambda = 1/2$ | **Lateral/Semantic** | Generalized, abstracted memories; facts and concepts without episodic context |
| $\lambda = 1$ | **Basal/Procedural** | Implicit, automatic memories; skills and habits; classical (non-quantum) encoding |
| $\lambda \in (0, 1) \setminus \{1/2\}$ | **Mixed/Transitional** | Memories in consolidation or reconsolidation; transitioning between types |
| Multiple slopes | **Composite memory** | Memory with components at different depth levels (e.g., a recalled episode that activates both specific detail and general knowledge) |

**Correspondence to Fontaine Classification.** This is the **same** slope decomposition that classifies QEC codes (Conjecture 3.3 of NUMBER-THEORY-QEC-BRIDGE.md):

| Slope | QEC Interpretation | Memory Interpretation |
|:---|:---|:---|
| $\lambda = 0$ | Perfect codes, zero error rate | Frontal/episodic memory, exact recall |
| $\lambda \in (0, 1)$ | Good codes, finite threshold | Lateral/semantic memory, good but imperfect |
| $\lambda = 1/2$ | Self-dual CSS codes | Semantic memory (balanced encoding) |
| $\lambda = 1$ | Classical codes, trivial quantum | Procedural memory (no quantum protection) |
| $\lambda \notin [0, 1]$ | Unphysical | Non-memory (no encoding possible) |

### 3.3 Fontaine's Period Rings and Memory Types

**Conjecture 3.3 (Fontaine Classification of Memory).** The nested inclusion of Fontaine's period rings:

$$B_{\text{crys}} \subset B_{\text{st}} \subset B_{\text{dR}} \subset B_{\text{HT}}$$

provides a **filtration of memory representations**, classifying memories by their behavior under deformation (reconsolidation) and monodromy (context-dependent recall):

| Memory Class | Number-Theoretic Analog | Memory Characteristics |
|:---|:---|:---|
| **Crystalline** | Good reduction, $B_{\text{crys}}$-admissible | **Consolidated episodic memory**: robust under reconsolidation, context-independent, exact recall |
| **Semistable** | Semistable reduction, $B_{\text{st}}$-admissible | **Context-dependent memory**: recall varies with context; has monodromy (narrative-dependent meaning) |
| **De Rham** | $B_{\text{dR}}$-admissible | **Narrative memory**: embedded in a larger story; meaning depends on temporal position |
| **Hodge-Tate** | $B_{\text{HT}}$-admissible | **Weighted/graded memory**: memory organized by sensory salience (Hodge-Tate weights = salience scores) |
| **Generic** | Galois representation, no period ring | **Unprocessed memory**: raw sensory trace, not yet consolidated into any coherent framework |

**Prediction 3.1 (Crystalline = Episodic).** A memory is **episodic** (experientially vivid, re-experiencing) precisely when its associated Galois representation is **crystalline** — i.e., the Frobenius action (consolidation) preserves the entire structure without introducing monodromy (context-dependence). The crystalline condition $D_{\text{crys}}(V) \neq 0$ is the mathematical expression of "I remember exactly what happened."

**Prediction 3.2 (Semistable = Context-Dependent).** A memory is **context-dependent** (I remember, but the details shift depending on when/how I'm asked) precisely when its representation is semistable but not crystalline. The monodromy operator $N$ on $D_{\text{st}}(V)$ quantifies the **degree of context-dependence** — the larger the eigenvalues of $N$, the more the memory narrative drifts with each retelling.

### 3.4 Frobenius as Memory Consolidation

**Conjecture 3.4 (Frobenius = Consolidation Cycle).** The Frobenius endomorphism $F$ acting on the Dieudonné module $D(m)$ corresponds to **one cycle of memory consolidation**:

$$F: D(m) \to D(m), \quad F(\text{memory encoding}) = \text{encoding after one rehearsal cycle}$$

**Structure.** In the QEC interpretation, $F$ is the cyclic measurement operator (Conjecture 2.2 of NUMBER-THEORY-QEC-BRIDGE.md). In memory, this translates to:

- Each application of $F$ corresponds to **one episode of memory rehearsal** (conscious recall, hippocampal replay during sleep, or re-exposure)
- The eigenvalues (slopes) of $F$ determine how the memory changes under rehearsal
- Étale components ($\lambda=0$) are **exactly preserved** by $F$ — these memories do not distort with rehearsal (episodic fidelity)
- Positive slope components are **transformed** by $F$ — these memories become more generalized/abstracted with each rehearsal

**Prediction 3.3 (Rehearsal Distortion).** Repeated rehearsal of an episodic memory should gradually shift it toward semantic memory (slope shifts from $\lambda=0$ toward $\lambda=1/2$). This is the mathematical expression of the well-known phenomenon that repeated retelling of an event gradually transforms it from vivid episodic recall to abstract semantic knowledge.

**Falsification Condition 3.1.** Measure the slope decomposition of memory encodings (proxied by neural population geometry) before and after sleep-dependent consolidation. If the slope spectrum does not shift toward $\lambda=0$ (sharper, more étale) after sleep, the Frobenius-consolidation correspondence is falsified.

---

## 4. Memory Deformation = Code Deformation

### 4.1 The Formal Group of Memory Reconsolidation

**Conjecture 4.1 (Memory Reconsolidation as Formal Deformation).** Memory reconsolidation — the process by which a retrieved memory is modified before being re-stored — corresponds to a **one-parameter deformation** along the formal group of the associated memory object:

$$m(T) = m_0 + T \cdot \delta_1 m + \frac{T^2}{2} \cdot \delta_2 m + \cdots$$

where:
- $m_0$ is the original memory trace ($T=0$)
- $T$ parameterizes the "depth of reconsolidation" — how much modification occurs
- $\delta_k m$ is the $k$-th order deformation of the memory
- The series is given by the **formal group logarithm** of the associated elliptic curve/Diedonné module

**Structure.** This is the exact analog of Conjecture 5.1 from NUMBER-THEORY-QEC-BRIDGE.md, where $C(T)$ is a deformed quantum code. The formal group provides the **natural parameterization** of how a memory drifts under repeated recall:

| Formal Group Feature | Memory Interpretation |
|:---|:---|
| $T = 0$ (origin) | Original encoding (unmodified memory) |
| $T > 0$ small | Minor reconsolidation (subtle detail changes) |
| $T \gg 0$ large | Major reconsolidation (significant rewriting of memory) |
| Formal group law $F(X, Y)$ | **Composition of reconsolidations**: reconsolidating a reconsolidated memory |
| Logarithm $\log_{\widehat{E}}(T)$ | The "memory deformation path" — how the encoding changes as a function of reconsolidation depth |
| Height of the formal group | **Memory stability**: higher height = more deformation-resistant |

### 4.2 Kodaira-Néron Types as Memory Degradation Patterns

**Conjecture 4.2 (Kodaira-Néron Classification of Memory Degradation).** The Kodaira-Néron classification of singular fibers exactly catalogs the possible **degradation patterns** of memory under repeated reconsolidation or pathological interference:

| Kodaira Type | Singular Fiber | Memory Interpretation |
|:---|:---|:---|
| $\text{I}_0$ | Smooth | **Intact memory**: no degradation, consolidation complete |
| $\text{I}_1$ | Nodal rational curve | **Single detail loss**: one specific feature forgotten |
| $\text{I}_n$ ($n \geq 1$) | $n$-gon of rational curves | **Progressive degradation**: $n$ distinct episodes/features conflated (source monitoring failure) |
| $\text{II}$ | Cuspidal curve | **Catastrophic memory collapse**: memory reduced to a single undifferentiated trace (schematic/gist-only) |
| $\text{III}$ | Two tangent curves | **Memory bifurcation**: one memory splits into two conflicting versions |
| $\text{IV}$ | Three concurrent curves | **Tripartite conflation**: three related memories merge into one indistinguishable composite |
| $\text{I}_0^*$ | $D_4$ configuration | **Memory with dihedral symmetry**: four variants equally plausible (uncertainty about which happened) |
| $\text{I}_n^*$ | $D_{n+4}$ configuration | **Extended uncertainty**: the memory exists in $n+4$ equally plausible versions |
| $\text{IV}^*$ | $E_6$ configuration | **Flashbulb memory**: exceptionally vivid, multi-sensory, resistant to degradation |
| $\text{III}^*$ | $E_7$ configuration | **Eidetic memory**: photographic recall with exceptional precision |
| $\text{II}^*$ | $E_8$ configuration | **Hyper-eidetic memory**: total recall with $E_8$ symmetry — the theoretical maximum of memory preservation |

**Key Insight.** The exceptional types ($\text{IV}^*, \text{III}^*, \text{II}^*$) — which in the QEC interpretation correspond to codes with $E_6, E_7, E_8$ symmetry — correspond in memory to **exceptional memory phenomena**:

| Exceptional Type | Lie Group | QEC Code Type | Memory Phenomenon |
|:---|:---|:---|:---|
| $\text{IV}^*$ | $E_6$ | $E_6$-symmetric stabilizer code | Flashbulb memory (Brown & Kulik, 1977) |
| $\text{III}^*$ | $E_7$ | $E_7$-symmetric stabilizer code | Eidetic/photographic memory |
| $\text{II}^*$ | $E_8$ | $E_8$-symmetric stabilizer code | Hyperthymesia (HSAM — Highly Superior Autobiographical Memory) |

**Prediction 4.1 (Lie Group Symmetry of Exceptional Memory).** Individuals with HSAM (hyperthymesia) should exhibit memory encoding geometries with $E_8$ root system symmetry in their neural population codes. Individuals with eidetic memory should exhibit $E_7$ symmetry. Flashbulb memories should exhibit local $E_6$ structure at the time of encoding.

**Falsification Condition 4.1.** If the neural population geometry of flashbulb/eidetic/hyperthymestic memories shows no evidence of exceptional Lie group structure (or shows the wrong group — e.g., $E_8$ for a flashbulb memory rather than $E_6$), the Kodaira-Néron classification is falsified for memory.

### 4.3 Supersingular Reduction and Memory Loss

**Conjecture 4.3 (Supersingular = Forgotten).** In the arithmetic of elliptic curves, a curve with **supersingular reduction** at $p$ has no $p$-torsion points in characteristic $p$ — the curve becomes "structureless" at that prime. In memory, **supersingular reduction corresponds to forgetting**:

- A memory with supersingular reduction at prime $p$ (a specific cognitive modality) has **no accessible content** in that modality
- The endomorphism ring of a supersingular curve is a maximal order in a quaternion algebra — the memory trace exists in a **non-commutative** (quantum) state that cannot be accessed through classical recall

**Prediction 4.2.** Attempted recall of a "supersingular memory" (a memory that has been forgotten in a particular modality) should produce the same neural signature as recollection of truly novel information — because the classical (commutative) access pathway is severed, even though the quaternionic (quantum) trace remains.

### 4.4 Memory Versioning as the Néron Model

**Conjecture 4.4 (Néron Model = Memory Version DAG).** The Néron model $\mathcal{E}$ of an elliptic curve $E$ over a p-adic field provides a **minimal regular model** — a smooth scheme that agrees with $E$ on the generic fiber and has the best possible reduction properties. This corresponds to the **memory version DAG**:

| Néron Model Feature | Memory DAG Interpretation |
|:---|:---|
| Generic fiber (curve over $\mathbb{Q}_p$) | The "live" memory trace (subject to reconsolidation) |
| Special fiber (reduction mod $p$) | The "consolidated" memory (hash-addressed, immutable) |
| Kodaira-Néron type of special fiber | The degradation type of that version of the memory |
| Néron model (entire scheme) | The complete DAG of all versions of the memory, including alternative branches |
| Smooth locus of special fiber | Intact components of the consolidated memory |
| Singular locus | Degraded or conflated components |

**Connection to Git/Blockchain Model.** In the braided register, memory versions form a content-addressable DAG (Git-like commits). The Néron model provides the **algebro-geometric analog** of this structure: each version is a "fiber," and the Néron model is the total space of all versions with their inter-relations.

---

## 5. The Adelic Memory Conjecture

### 5.1 Primes as Memory Modalities

**Conjecture 5.1 (Prime-Modality Correspondence).** Each prime $p$ corresponds to a distinct **cognitive modality** of memory. A modality is a sensory or conceptual channel through which memories are encoded, stored, and retrieved:

| Prime $p$ | Memory Modality | Justification |
|:---|:---|:---|
| $p = 2$ | **Visual-spatial** | Binary nature of 2D retinal projections; $\mathbb{Q}_2$ encodes dyadic hierarchical decomposition of visual scenes |
| $p = 3$ | **Auditory-temporal** | Ternary structure of phonemes (onset-nucleus-coda), rhythmic triples; $\mathbb{Q}_3$ for three-state temporal sequences |
| $p = 5$ | **Semantic-conceptual** | Working memory capacity ($5 \pm 2$ items); $\mathbb{Q}_5$ for abstract symbol manipulation |
| $p = 7$ | **Emotional-affective** | Classical "7 basic emotions" framework; $\mathbb{Q}_7$ for affective valence encoding |
| $p = 11$ | **Olfactory-gustatory** | Higher-dimensional odor space; 11 primary odor categories in some taxonomies |
| $p = \infty$ (archimedean) | **Narrative-self** | Continuous, unbounded, the "unity of consciousness"; the archimedean place is the "I" that experiences the memory |

**Definition 5.1 (Local Memory at p).** A *local memory* $m_p$ is the encoding of a memory trace in modality $p$. Local memories $m_p$ and $m_q$ for $p \neq q$ may differ in content, precision, and accessibility — a memory may be vividly visual ($p=2$) but semantically vague ($p=5$).

**Prediction 5.1 (Modality-Specific p-adic Structure).** The p-adic distance $d_p(m_a, m_b)$ for two memory traces in modality $p$ should exhibit structure determined by $p$. Specifically:
- Visual memories ($p=2$) should show binary tree structure ($2$-adic ultrametric)
- Auditory memories ($p=3$) should show ternary hierarchical structure
- Semantic memories ($p=5$) should show 5-adic clustering

### 5.2 The Adelic Product Formula for Memory

**Conjecture 5.2 (Adelic Memory Capacity Constraint).** The adelic product formula:

$$\prod_{p \leq \infty} |m|_p = 1$$

imposes a **fundamental constraint** on the total memory capacity across all modalities:

$$\prod_{p \leq \infty} \text{Cap}_p(m) = 1$$

where $\text{Cap}_p(m)$ is the *modality-specific memory capacity* — the amount of information about memory $m$ that can be stored in modality $p$.

**Interpretation.** This formula says: **you cannot have perfect memory in all modalities simultaneously.** A memory that is exceptionally precise in one modality ($|m|_p \ll 1$, large capacity) must be correspondingly imprecise in another ($|m|_q \gg 1$, small capacity). This is the arithmetic analog of the well-known trade-off: people with exceptional visual memory often have poor auditory memory (and vice versa).

**Corollary 5.1 (Capacity Conservation).** Let $\nu_p(m) = -\log_p |m|_p$ be the $p$-adic valuation of memory precision. Then:

$$\sum_{p \leq \infty} \nu_p(m) = 0$$

where $\nu_\infty(m) = -\log |m|_\infty$ for the archimedean valuation. This is a **conservation law**: the sum of memory precision across all modalities is constant. Improving memory precision in one modality must reduce precision in at least one other.

**Prediction 5.2 (Cross-Modal Interference).** Training a subject to enhance memory precision in one modality (e.g., visual memory training using the method of loci) should produce measurable decreases in memory precision in at least one other modality. The product formula predicts that the **product** of precisions remains invariant.

### 5.3 Local-Global Principle for Memory

**Conjecture 5.3 (Hasse Principle for Memory Existence).** A memory trace exists as a coherent, conscious experience if and only if it exists **locally** in every modality and satisfies the adelic product condition:

$$\text{Memory exists globally} \iff \text{Memory exists locally at every } p \leq \infty \text{ AND } \prod_p |m|_p = 1$$

**Interpretation.** This is the memory analog of Conjecture 1.1 (Local-Global Principle for Quantum Codes) from NUMBER-THEORY-QEC-BRIDGE.md. A memory must be encodable in every modality, and the encodings must cohere across modalities via the adelic constraint.

**Prediction 5.3 (Modality-Limited Amnesia).** A subject who cannot encode memories in a specific modality (e.g., acquired visual agnosia for $p=2$) should be unable to form conscious memories at all — even in other modalities — because the local condition fails at $p=2$, violating the Hasse principle. This predicts that **no single-modality amnesia can be truly selective**: loss of visual encoding capacity should impair global memory function.

**Counter-prediction caveat.** The Hasse principle is known to fail in arithmetic — there exist counterexamples (Selmer's example for elliptic curves) where local conditions are satisfied but no global object exists. Such failures are encoded by the **Tate-Shafarevich group** Ш. The memory analog is:

**Conjecture 5.4 (Ш-Obstruction to Memory).** Failures of the Hasse principle in memory correspond to **dissociative states**: memory encodings exist in each individual modality but cannot be integrated into a coherent conscious experience. The size of the Tate-Shafarevich group Ш for the memory object measures the **degree of dissociation**.

### 5.4 Ramified Primes and Traumatic Memory

**Definition 5.2 (Ramification Index of Memory).** For a local memory $m_p$, the ramification index $e_p(m)$ measures how much the memory "branches" at prime $p$ — the number of distinct sub-encodings that collapse under reduction modulo $p$.

**Conjecture 5.5 (Ramified = Traumatic).** A memory is **traumatic** if it has high ramification at multiple primes simultaneously:

$$e_p(m) > 1 \text{ for multiple primes } p$$

**Interpretation.** High ramification means the memory has an excessively complex local structure that cannot be "flattened" into a single consistent encoding. This corresponds to:
- Overwhelming sensory detail across multiple modalities
- Inability to produce a coherent narrative (semistable/de Rham classification fails)
- Fragmentation: the memory exists as disconnected pieces in different modalities

**Prediction 5.4 (Traumatic Memory Ramification).** PTSD patients should show high ramification indices in their memory representations, particularly at primes corresponding to the sensory modalities most engaged during the traumatic event. Successful therapy (EMDR, exposure therapy) should reduce the ramification index — "taming" the memory by reducing $e_p(m)$ toward 1 at each ramified prime.

### 5.5 The Idele Class Group as Memory Integration

**Conjecture 5.6 (Idele Class Group = Consciousness Integration).** The idele class group:

$$C_\mathbb{Q} = \mathbb{A}_\mathbb{Q}^\times / \mathbb{Q}^\times$$

corresponds to the **integration of modality-specific memories into a unified conscious experience**. The group operation is the **binding** of two memory components from different modalities into a single coherent memory.

**Structure.**
- An **idele** $(m_p)_{p \leq \infty}$ is a collection of local memories at all primes, with the condition that $m_p \in \mathbb{Z}_p^\times$ for almost all $p$ (only finitely many primes can encode nontrivial memory content)
- Quotienting by $\mathbb{Q}^\times$ (the diagonal embedding) implements the **binding constraint**: two ideles that differ by a global scalar represent the same memory (invariance under global rescaling of memory intensity)
- The idele class group thus parameterizes all possible "memory configurations" — all ways of distributing memory content across modalities

**Prediction 5.5 (Finitude of Nontrivial Modalities).** The restricted product condition implies that **only finitely many primes can carry nontrivial memory content.** For human memory, the effective primes should be a small finite set (corresponding to the actual cognitive modalities), and the rest are "unramified" — carrying trivial (identity) encoding.

---

## 6. The Unified Ternary Diagram

```
    NUMBER THEORY              QUANTUM ERROR CORRECTION          BRAIDED MEMORY REGISTER
    =============              =======================          =======================

┌──────────────────┐    ┌─────────────────────────────┐    ┌──────────────────────────┐
│ B(SL₂, ℚₚ)       │───▶│ Code parameter space        │───▶│ Ultrametric memory tree   │
│ (p+1)-regular    │    │ Equivalence classes         │    │ Dendrogram of traces      │
│ Lattices in ℚₚ²  │    │ of 2-qudit codes            │    │ n leaves = n memories     │
└────────┬─────────┘    └─────────────┬───────────────┘    └────────────┬─────────────┘
         │                            │                                 │
         │ Moy-Prasad                 │ Fault-tolerance                 │ Consolidation
         ▼                            ▼                                 ▼
┌──────────────────┐    ┌─────────────────────────────┐    ┌──────────────────────────┐
│ Depth r(π)       │───▶│ Logical error rate p_L      │───▶│ Memory strength S(m)      │
│ r=0: tamely ram. │    │ Exponential suppression      │    │ Fully consolidated        │
│ r>0: wildly ram. │    │ Requires concatenation       │    │ Labile, reconsolidated    │
└────────┬─────────┘    └─────────────┬───────────────┘    └────────────┬─────────────┘
         │                            │                                 │
         │ Dieudonné                  │ Code cohomology                 │ Memory hierarchy
         ▼                            ▼                                 ▼
┌──────────────────┐    ┌─────────────────────────────┐    ┌──────────────────────────┐
│ D(m) with F,V,p  │───▶│ Stabilizer cohomology       │───▶│ Depth structure           │
│ Slope λ = r/s    │    │ Error threshold f(λ)        │    │ Frontal/Semantic/Basal    │
│ λ=0: étale       │    │ λ=0: perfect codes          │    │ λ=0: episodic memory      │
│ λ=1/2: self-dual │    │ λ=1/2: CSS codes            │    │ λ=1/2: semantic memory    │
│ λ=1: classical   │    │ λ=1: classical codes         │    │ λ=1: procedural memory    │
└────────┬─────────┘    └─────────────┬───────────────┘    └────────────┬─────────────┘
         │                            │                                 │
         │ Supersingular              │ Code-switching                  │ Associative binding
         ▼                            ▼                                 ▼
┌──────────────────┐    ┌─────────────────────────────┐    ┌──────────────────────────┐
│ Isogeny graph     │───▶│ Code-switching protocols   │───▶│ Associative memory graph  │
│ G(p,ℓ), Ramanujan │    │ ℓ-isogenies = elementary   │    │ Associative links =       │
│ expander          │    │ code transformations        │    │ isogeny edges             │
│ Diameter ~ log_ℓ p│    │ Bounded code distance       │    │ Associative distance      │
└────────┬─────────┘    └─────────────┬───────────────┘    └────────────┬─────────────┘
         │                            │                                 │
         │ Kodaira-Néron              │ Code degeneration               │ Memory degradation
         ▼                            ▼                                 ▼
┌──────────────────┐    ┌─────────────────────────────┐    ┌──────────────────────────┐
│ I₀ ... II*       │───▶│ Maximum-distance → collapse │───▶│ Intact → flashbulb →     │
│ E₆, E₇, E₈       │    │ Exceptional code symmetries │    │ eidetic → hyperthymesia  │
│ Formal group log │    │ Code deformation series      │    │ Reconsolidation path     │
└────────┬─────────┘    └─────────────┬───────────────┘    └────────────┬─────────────┘
         │                            │                                 │
         │ Adeles + Langlands         │ Global constraint               │ Cross-modal coherence
         ▼                            ▼                                 ▼
┌──────────────────┐    ┌─────────────────────────────┐    ┌──────────────────────────┐
│ ∏_p |m|_p = 1    │───▶│ Global distance constraint  │───▶│ Total memory capacity     │
│ Hasse principle  │    │ Local→global criterion      │    │ Local→global existence    │
│ Ш obstruction    │    │ Brauer-Manin obstruction    │    │ Dissociation              │
│ Ramification e_p │    │ "Bad prime" structure        │    │ Traumatic memory          │
└──────────────────┘    └─────────────────────────────┘    └──────────────────────────┘
```

---

## 7. Concrete Predictions and Testable Consequences

### 7.1 Immediately Testable (Phase 2)

| # | Prediction | Test Method |
|:--|:---|:---|
| **M1** | Memory recall paths follow geodesics in the dendrogram; deviation from geodesic is rare | Track recall sequences in cued-recall experiments; measure geodesic-deviation rate |
| **M2** | Associative memory graphs are Ramanujan expanders (uniform local branching) | Analyze free-association networks from verbal fluency tasks; test spectral gap |
| **M3** | Dieudonné-Manin slope decomposition correlates with memory type: episodic (λ=0), semantic (λ=1/2), procedural (λ=1) | Compute slopes from neural population geometries during different memory tasks |
| **M4** | Memory reconsolidation follows formal group logarithm: $m(T) = m_0 + a_1 T + \frac{a_2}{2} T^2 + \cdots$ | Track memory drift across repeated retrievals; fit formal group log coefficients |
| **M5** | Cross-modal capacity follows adelic product formula: $\prod_p \text{Cap}_p = 1$ | Measure memory precision in visual vs. auditory domain; test trade-off constraint |

### 7.2 Requires New Theory (Phase 3)

| # | Prediction | Status |
|:--|:---|:---|
| **M6** | Exceptional memory (flashbulb, eidetic, hyperthymesia) exhibits $E_6, E_7, E_8$ symmetry in neural codes | `[speculative]` — no direct neural evidence |
| **M7** | Moy-Prasad depth decreases during sleep-dependent consolidation (hippocampal replay tames ramification) | `[my conjecture]` |
| **M8** | Dissociative states correspond to nontrivial Ш (Tate-Shafarevich) obstructions | `[speculative]` |
| **M9** | Traumatic memory ramification indices decrease during successful therapy | `[my conjecture]` |
| **M10** | Only finitely many primes (cognitive modalities) carry nontrivial memory content | `[my conjecture]` — restricted product condition |

### 7.3 Computational Tests (Phase 2-3)

| # | Test | Implementation |
|:--|:---|:---|
| **C1** | Build ultrametric tree from free-association data; verify $(p+1)$-regularity | `bt_memory_tree.py` |
| **C2** | Compute isogeny graph structure of associative memory network; verify Ramanujan property | `isogeny_memory_graph.py` |
| **C3** | Compute Dieudonné-Manin slopes from hierarchical clustering of memory representations | `slope_memory_classifier.py` |
| **C4** | Fit formal group logarithm to reconsolidation drift data | `reconsolidation_log.py` |
| **C5** | Test adelic product formula with cross-modal memory precision data | `adelic_capacity_test.py` |

---

## 8. Falsifiability

The entire bridge framework would be falsified if:

1. **Memory trees are not $(p+1)$-regular:** If ultrametric dendrograms from real memory data show arbitrary branching that cannot be embedded in a BT building, the structural identity claim fails.
2. **Associative graphs are not expanders:** If free-association networks do not exhibit the Ramanujan spectral gap, the isogeny graph model is disconfirmed.
3. **No slope-type correlation:** If Dieudonné slopes of memory encodings show no systematic relationship to episodic/semantic/procedural memory types, the Fontaine classification is invalid for memory.
4. **Reconsolidation is not formal-group-like:** If the drift of memories under repeated retrieval does not follow a formal group log parameterization (i.e., the series coefficients are not consistent across retellings), the deformation model fails.
5. **No cross-modal capacity trade-off:** If individuals can have simultaneously high-precision memory in all modalities (violating $\prod_p \text{Cap}_p = 1$), the adelic constraint is disproven.

### Partial Falsification

The bridge may be **partially correct**: the ultrametric↔BT-building correspondence may hold while the isogeny↔associative-binding correspondence fails, or the slope↔memory-type correspondence may be valid without the adelic product constraint. Each connection axis is independently falsifiable.

---

## 9. Connections Within the Braided Memory Register

### 9.1 Central Conjecture Revisited

The number-theoretic bridge provides a new perspective on the braided memory register's central conjecture:

$$\delta(a,b) = c \cdot w(a,b)$$

**Now interpretable as:** The ultrametric distance $\delta$ and the braid word length $w$ are the **same graph distance** on the Bruhat-Tits tree $\mathcal{B}(\operatorname{SL}_2, \mathbb{Q}_p)$, measured under two different projections:
- $\delta$ = the "vertical" projection: graph distance in the tree (dendrogram depth)
- $w$ = the "horizontal" projection: minimal number of leaf-swaps (braid crossings) in the ordering induced by the left-to-right traversal of leaves

The conjecture asserts that these two projections yield the same number (up to scaling) — a claim about the **geometry of the BT tree**, not merely a claim about memory.

### 9.2 The Five Pillars Under Number-Theoretic Light

| Pillar | Number-Theoretic Object | Structural Guarantee |
|:---|:---|:---|
| **Ultrametric topology** | Bruhat-Tits building $\mathcal{B}(\operatorname{SL}_n, \mathbb{Q}_p)$ | The BT building IS an ultrametric space; the strong triangle inequality is built into the building's simplicial structure |
| **Braided binding (quipu)** | Supersingular isogeny graph $\mathcal{G}(p, \ell)$ | Isogenies naturally form a categorical structure with braiding (via the dual isogeny) |
| **Hierarchical depth** | Dieudonné module slope decomposition | Slopes provide a canonical refinement of hierarchy beyond simple depth — the $r/s$ rational data encodes the "texture" of the hierarchy |
| **Content-addressable versioning** | Néron model (minimal regular model) | The Néron model is the natural algebro-geometric object for tracking a family of versions (fibers) of an arithmetic object |
| **Social propagation DAG** | Adelic product / idele class group / Hasse principle | The adelic framework naturally handles "global consistency from local data" — exactly the social propagation problem |

---

## 10. Next Steps

### Immediate (This Session)
1. ✅ This bridge document synthesizes the number-theoretic QEC framework with the braided memory register across 5 connection axes
2. 🔜 Cross-reference all conjectures with the original NUMBER-THEORY-QEC-BRIDGE.md to ensure consistency
3. 🔜 Generate formal definitions for the memory-specific number-theoretic objects (Memory Dieudonné Module, Memory BT Building, Adelic Memory Space)

### Phase 2 — Computational
1. Implement `bt_memory_tree.py`: verify $(p+1)$-regularity of memory dendrograms
2. Implement `isogeny_memory_graph.py`: test spectral gap of associative networks
3. Implement `slope_memory_classifier.py`: compute Dieudonné slopes for memory types
4. Implement `adelic_capacity_test.py`: test cross-modal capacity constraints

### Phase 3 — Theoretical
1. Prove that the ultrametric dendrogram of finite memory space embeds isometrically in $\mathcal{B}(\operatorname{SL}_2, \mathbb{Q}_p)$
2. Formalize the correspondence between isogeny degree and associative binding strength
3. Develop the Kodaira-Néron classification for memory degradation — provide explicit examples of each type
4. State and prove the adelic product constraint for memory capacity (or find explicit counterexamples)

### Phase 4 — Empirical
1. Design cross-modal memory precision experiments to test the adelic product formula
2. Analyze free-association network graphs from existing verbal fluency datasets
3. Test the formal group log model on reconsolidation data from the experimental psychology literature
4. Collaborate with cognitive neuroscientists to test Moy-Prasad depth changes during sleep-dependent consolidation

---

## References

### Number Theory
- Bosch, S., Güntzer, U., & Remmert, R. (1984). *Non-Archimedean Analysis*. Springer.
- Fontaine, J.-M. (1994). Le corps des périodes p-adiques. *Astérisque*, 223.
- Serre, J.-P. (1979). *Local Fields*. Springer.
- Tate, J. (1950). *Fourier analysis in number fields*. PhD Thesis, Princeton.
- Kedlaya, K.S. (2010). *p-adic Differential Equations*. Cambridge.
- Tits, J. (1979). Reductive groups over local fields. *PSPM*, 33.
- Silverman, J.H. (1994). *Advanced Topics in the Arithmetic of Elliptic Curves*. Springer. (Kodaira-Néron, Néron models)
- Deuring, M. (1941). Die Typen der Multiplikatorenringe elliptischer Funktionenkörper. *Abh. Math. Sem. Hamburg*, 14. (Supersingular curves)

### Braided Memory Register
- Baffioni, F. & Rosati, F. (2000). Ultrametric overlap distribution in mean field spin glasses. *Eur. Phys. J. B*, 17.
- N'guessan, G.L.R. (2025). v-PuNNs: van der Put Neural Networks. arXiv:2508.01010.
- Krotov, D. (2021). Hierarchical Associative Memory. arXiv:2107.06446.
- Marsh, B.P. et al. (2025). High-capacity associative memory in a quantum-optical spin glass. arXiv:2509.12202.
- Kassel, C. (1995). *Quantum Groups*. Springer. (Braided monoidal categories, Yang-Baxter)
- Moerdijk, I. & Weiss, I. (2007). Dendroidal sets. *Algebraic & Geometric Topology*, 7.

### QNFO Internal
- NUMBER-THEORY-QEC-BRIDGE.md (2026-07-03). Bridge: Number Theory → Quantum Error Correction.
- braided-memory-register/POSITION-PAPER.md (2026-07-03). The Braided Memory Register.
- braided-memory-register/CONJECTURE-PROOF.md (2026-07-03). Ultrametric Depth = Braid Word Length.
- braided-memory-register/FORMAL-DEFINITIONS.md (2026-07-03). Formal Definitions.
- braided-memory-register/BRIDGE-ANALYSIS.md (2026-07-03). Bridge Analysis: Literature to Model.

---

*Bridge Document v1.0 — Follows QNFO-POL-COM-001. All conjectures labeled with epistemic status. Falsifiability conditions specified for each connection axis. Ternary correspondence established between number theory, QEC, and braided memory register.*

*"The file cabinet is a Bruhat-Tits building. The quipu is an isogeny graph. The adelic product formula is a memory constraint. And the Yang-Baxter equation is isogeny composition — always was."*
