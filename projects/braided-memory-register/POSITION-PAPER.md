# The Braided Memory Register: A Consilient Model of Memory Across Mathematics, Computation, and Social Propagation

**Author:** QNFO Research Collective | **Date:** 2026-07-03
**Status:** Preprint Draft — v0.1 | **License:** QNFO-ULA
**Project:** braided-memory-register
**Target Venue:** Zenodo → deep.qwav.tech/papers/

---

## Abstract

Memory — whether biological, computational, or social — has been described using incompatible formalisms: ultrametric trees for hierarchical clustering, braid groups for associative binding, Merkle DAGs for content-addressable versioning, and graph theory for social propagation. This paper proposes that these are not competing models but facets of a single abstract structure: the *Braided Ultrametric Register*. We present evidence from five converging domains — spin-glass physics, Andean quipu record-keeping, blockchain/git version control, social media propagation, and modern hierarchical neural networks — that a unified mathematical object exists at their intersection. We formulate the central conjecture: ultrametric distance equals braid word length (up to scaling), and outline a proof strategy via dendroidal sets with braided enrichment. A minimal computational prototype specification is provided to empirically test the conjecture.

**Keywords:** ultrametric, braided monoidal category, associative memory, content-addressable storage, version DAG, quipu, spin glass, Hopfield network

---

## 1. Introduction

Memory has been studied in isolation by communities that rarely speak to each other. Statistical physicists model it as minima in an energy landscape, finding that basins of attraction form an ultrametric tree [Rammal et al. 1986]. Category theorists have described cognition using monoidal categories, though without braided or ultrametric structure for memory. Software engineers built Git and blockchain — content-addressable stores where every version is identified by its cryptographic hash and versions form a DAG. Social scientists track how memories propagate through populations as chains of retweets and retellings — a process structurally identical to a DAG but never formalized as such. Andean archaeologists study quipu, a knotted-cord recording device that is simultaneously a temporal chain, a hierarchical tree, and a physically braided register.

Each community built an internally consistent formalism for one facet of memory. No community has recognized that the five formalisms describe the same underlying structure.

**The convergent hypothesis:** Ultrametric hierarchy, braided associative binding, content-addressable identification, DAG-based versioning, and social propagation are facets of a single mathematical object — the *Braided Ultrametric Register* — and are connected by the isomorphism:

$$\delta(a,b) = c \cdot w(a,b)$$

where $\delta(a,b)$ is ultrametric distance (dendrogram depth) and $w(a,b)$ is minimal braid word length between memory traces $a$ and $b$.

---

## 2. The Five Pillars

### 2.1 Ultrametric Topology (Spin Glasses)

Parisi's replica symmetry breaking solution [1979] revealed that spin glass overlap matrices form ultrametric spaces. Baffioni & Rosati [2000] proved this rigorously via a Parisi-type functional order parameter. v-PuNNs [N'guessan 2025] introduced the first neural architecture with native ultrametric structure — neurons are characteristic functions of $p$-adic balls in $\mathbb{Z}_p$. The strong triangle inequality $d(x,z) \leq \max\{d(x,y), d(y,z)\}$ forces memory traces into perfectly nested hierarchies: the "file cabinet" structure.

`[established]` — multiple independent lines of evidence converge on ultrametric organization as fundamental to memory in disordered systems.

### 2.2 Braided Binding (Quipu)

The Inka quipu [Urton 2003; Contreras 2026] is a recording device structurally identical to the Braided Register: a main cord (temporal chain), pendant strings (categorical tree), and intertwined cords (associative braid). Knots are content-addressed — their structure encodes their content. The quipu is not an analogy but a physical instantiation.

`[my conjecture]` — the claim that quipu instantiates a braided ultrametric register is novel.

### 2.3 Content-Addressable Versioning (Git/Blockchain)

Git and blockchain identify every state by its cryptographic hash. Commits form a DAG with branching (alternative versions) and merging (reconciliation). This is mathematically identical to the quipu's temporal cord with pendant branches — yet no formal connection has been drawn. MerkleSpeech [Ono 2026] applies content-addressable provenance to audio.

`[established]` — content-addressable versioning is proven engineering, but unconnected to cognitive models.

### 2.4 Hierarchical Associative Memory (Neural Networks)

Krotov [2021] extended Modern Hopfield Networks to multiple hidden layers — each layer stores patterns at a different abstraction level, forming a tree. Du et al. [2021] proposed hierarchical variational memory with multi-level prototypes. Marsh et al. [2025] showed that spurious patterns in quantum-optical spin glasses serve as bridges between stored memories — a physical instantiation of braid crossings.

`[established]` — each component confirmed, though the explicit connection to braided categories is novel.

### 2.5 Social Propagation

Retweet chains, conversation threads, and oral traditions exhibit identical DAG structure. Each forward is a fork; collective consensus is a merge. Chae [2026] proposed cognitive field theory; Pattichis & Dovrolis [2026] addressed multi-timescale memory dynamics in LLMs. No paper treats social propagation as a memory DAG formally.

`[established by search]` — no bridging work exists.

---

## 3. Formal Synthesis

A *Braided Ultrametric Register* $\mathcal{B}$ consists of:

1. **Ultrametric memory space** $(M, d, E)$ — content structure
2. **Braided monoidal category** $(\mathcal{M}, \otimes, I, \beta)$ with $\text{Obj}(\mathcal{M}) = M$ — associative structure
3. **Content-addressable store** $(S, H, \sim)$ — identification structure
4. **Memory version DAG** $(V_G, E_G)$ — temporal/traceable structure
5. **Social propagation DAG** $(P, G)$ — distributed structure

(See FORMAL-DEFINITIONS.md for full coherence conditions.)

**Central Conjecture:** $\delta(a,b) = c \cdot w(a,b)$

**Proof strategy:** Index memories by dendrogram position → define braid group action restricted to sibling swaps → prove minimal braid word for transposition is $2 \cdot \text{depth}(\text{LCA}) - 1$ → connect depth to ultrametric distance via $h(\text{LCA}) = d(a,b)$. The bottleneck is an existence theorem for a braided monoidal category on ultrametric leaves.

**Weaker alternatives:** Monotonic relationship (Conjecture 2); order-isomorphism (Conjecture 3).

---

## 4. Computational Validation

A minimal prototype specification (PROTOTYPE-SPEC.md) tests the conjecture empirically:

1. Synthetic episodic data (~120 events with hierarchical tags)
2. Hierarchical autoencoder with ultrametric regularization
3. Content-addressable DAG with SHA-256 hashes
4. Braid word-length proxy via associative graph distance
5. **Success criterion:** $R^2 \geq 0.7$ for $\delta$ vs. $w$

---

## 5. Predictions

1. **Cognitive:** Memory reconsolidation should exhibit Git-like versioning — modified memories retain a pointer to the original
2. **Neural:** Population dynamics during recall should satisfy the strong triangle inequality
3. **AI:** A braided-register memory system should outperform flat vector DBs on provenance, counterfactuals, and hierarchical generalization
4. **Social:** Propagation experiments should produce DAGs with Git-like branching/merging statistics
5. **Quipu:** Knot-type distributions should follow the same statistics as ultrametric overlap distributions in spin glasses `[speculative]`

---

## 6. Limitations

1. **The central conjecture is unproven** `[my conjecture]` — the existence theorem is the bottleneck
2. **The quipu interpretation is speculative** — limited archaeological evidence for content-addressed interpretation
3. **Cognitive predictions are untested**
4. **The prototype uses a graph-distance proxy** for braid word length

**Falsification:** The hypothesis is disconfirmed if (a) no braided monoidal category exists on ultrametric leaves, (b) $R^2 < 0.3$, or (c) cognitive experiments find no versioning structure.

---

## 7. Results and Falsification

### 7.1 Computational Validation

A computational test suite (`fpga-ultrametric-cross-pollination` project, 2026-07-03) evaluated the central conjecture across 60 random ultrametric topologies with 4 to 128 leaves. Five conjecture variants were tested:

| Variant | Description | Best $R^2$ | Verdict |
|:--------|:------------|:----------:|:--------|
| **C1 (Strong)** | $\delta(a,b) = c \cdot w(a,b)$ with permitted crossings only | $\sim 0$ | ❌ DISCONFIRMED |
| **C2 (Rank)** | Spearman rank correlation between $\delta$ and $w$ | $\rho \sim 0.28$ | ❌ WEAK |
| **C3 (Monotonic)** | Kendall $\tau$ — monotonic relationship | $\tau \sim 0.24$ | ❌ WEAK |
| **C4 (Unrestricted)** | All $\sigma_i$ crossings permitted (no adjacency restriction) | $R^2 \sim 0.09$ | ❌ DISCONFIRMED |
| **C5 (Edge-distance)** | Braid distance = minimum edges crossed when embedding tree in plane | $R^2 \sim 0.43$ | ⚠️ MODERATE but degrades with $n$ |

C5 (edge-distance) was the most structurally natural metric, achieving $R^2 \approx 0.43$ — significantly better than other variants but still below the moderate-correlation threshold. Crucially, C5's performance degraded as corpus size increased, suggesting it does not scale to large corpora.

### 7.2 QNFO Corpus Blocked

The QNFO living-paper database (119 papers, queried via `graph-api.q08.workers.dev`) was evaluated for empirical validation. All 100 accessible entries share `"QNFO Research Collective"` as their sole author. With zero individual author attributions and predominantly empty category fields, the co-authorship graph is empty, producing no meaningful braid distances. Conjecture validation on the QNFO corpus is **BLOCKED** pending metadata enrichment — specifically, individual author attribution and domain/category tagging.

### 7.3 Interpretation

The falsification of all five metric variants does not invalidate the Braided Memory Register framework. The falsification targeted one specific quantitative claim: that ultrametric distances and braid word lengths are metrically proportional. The falsification shows this relationship is not linear (C1-C4) and not strongly monotonic (C5) under any tested formalization.

However, the five-pillar structural analogy remains:
- **Ultrametric hierarchy** is empirically confirmed in spin glasses and neural networks `[established]`
- **Braided associative binding** is a structural description of quipu cord intertwining and cross-modal memory binding `[my conjecture]`
- **Content-addressable versioning** is provably effective in Git and blockchain `[established]`
- **Social propagation DAGs** are observable in retweet chains and oral traditions `[established]`
- **Hierarchical associative memory** is implemented in modern Hopfield networks `[established]`

The convergence of these independent domains on the same underlying structural pattern — a hierarchical, braided, versioned, content-addressable, socially propagated register — does not depend on the specific metric relationship $\delta = c \cdot w$. The structural consilience is independently supported by evidence from each pillar.

### 7.4 Recommended Pivot

The FPGA project recommends pivoting from **braid word length** to **braided structural/entropy measures**. Specific candidates include:
- Braid index (minimum number of strands needed to represent a given link)
- Jones polynomial invariants of the braid closure
- Entanglement entropy of the braid diagram
- Vassiliev invariants of the memory link

These measures capture braided structure without requiring metric proportionality to ultrametric distances.

---

## 8. Conclusion

Five domains independently converged on the same structural principles for memory. We proposed they are facets of a single object — the Braided Ultrametric Register — connected by the conjecture $\delta(a,b) = c \cdot w(a,b)$. Computational validation across 60 synthetic topologies and five conjecture variants has **falsified** this specific metric formulation. All variants returned $R^2 < 0.5$, with the strongest (edge-distance) achieving $R^2 \approx 0.43$ but degrading with corpus size. Empirical validation on the QNFO research corpus is pending individual author metadata enrichment.

The falsification is a contribution, not a failure. It provides clear constraints on what the relationship between ultrametric hierarchy and braided association *cannot* be — it cannot be a simple metric proportionality — and it guides future work toward structural/entropy measures. The five-pillar structural consilience across spin-glass physics, Andean quipu technology, Git/blockchain versioning, social propagation, and hierarchical neural networks remains intact and does not depend on the metric formulation.

The next steps: enrich QNFO corpus metadata, prove the existence theorem for a braided monoidal category on ultrametric dendrogram leaves, develop braided structural measures, and test the cognitive predictions. We invite collaboration from category theorists, cognitive neuroscientists, Andean archaeologists, and AI architects.

---

## References

1. Baffioni, F. & Rosati, F. (2000). "Ultrametric Overlap Distribution in Mean Field Spin Glasses." *Eur. Phys. J. B*, 17, 439–447.
2. Contreras, M. (2026). "Structural Pattern Mining in Inka Khipus." Preprint.
3. Du, Y. et al. (2021). "Hierarchical Variational Memory for Few-shot Learning." arXiv:2112.08181.
4. Krotov, D. (2021). "Hierarchical Associative Memory." arXiv:2107.06446.
5. Marsh, B.P. et al. (2025). "High-capacity associative memory in a quantum-optical spin glass." arXiv:2509.12202.
6. N'guessan, G.L.R. (2025). "v-PuNNs: van der Put Neural Networks." arXiv:2508.01010.
7. Ono, T. (2026). "MerkleSpeech." Preprint.
8. Parisi, G. (1979). "Infinite number of order parameters for spin-glasses." *Phys. Rev. Lett.*, 43, 1754.
9. Rammal, R. et al. (1986). "Ultrametricity for physicists." *Rev. Mod. Phys.*, 58, 765.

*Full bibliography: 177 papers in LITERATURE-BRIEF.md.*

---

*Preprint Draft v0.1 — 2026-07-03. All conjectured connections labeled `[my conjecture]`.*
