# FORMAL DEFINITIONS: The Braided Ultrametric Register

**Author:** QNFO Research Agent | **Date:** 2026-07-03
**Status:** Working Draft — Phase 3 Mathematical Synthesis
**Project:** braided-memory-register

---

## 1. Motivation

The Braided Register hypothesis asserts that five structural properties — ultrametric hierarchy, braided associative binding, content-addressable identification, DAG-based versioning, and social propagation — are facets of a single mathematical object. This document provides formal definitions for each component and proposes a unified structure.

**Epistemic status:** These definitions are `[my conjecture]` — they have not been peer-reviewed and may contain category-theoretic errors. They are offered as a starting point for formalization, not as settled mathematics. Falsification condition: if no category admits all five structures simultaneously, or if the coherence axioms produce a contradiction, the hypothesis is disconfirmed.

---

## 2. Component Definitions

### 2.1 Ultrametric Memory Space

**Definition 2.1.1 (Ultrametric space).** A set $X$ equipped with a function $d: X \times X \to \mathbb{R}_{\geq 0}$ is an *ultrametric space* if for all $x, y, z \in X$:

1. $d(x, y) = 0 \iff x = y$ (identity of indiscernibles)
2. $d(x, y) = d(y, x)$ (symmetry)
3. $d(x, z) \leq \max\{d(x, y), d(y, z)\}$ (strong triangle inequality)

The third condition is strictly stronger than the usual triangle inequality. It implies that every triangle is *acutely isosceles* — two of the three distances are equal and at least as large as the third. This forces the distance matrix to induce a rooted tree (dendrogram) via single-linkage hierarchical clustering [established — Rammal et al. 1986].

**Definition 2.1.2 (Ultrametric memory space).** An *ultrametric memory space* is a pair $(M, d)$ where:

- $M$ is a finite set of *memory traces* (patterns, representations, or neural activity vectors)
- $d$ is an ultrametric on $M$
- Each $m \in M$ has an *energy* $E(m) \in \mathbb{R}_{\geq 0}$ such that $E(m) \propto d(m, m_0)$ for some distinguished *cue trace* $m_0$

**Definition 2.1.3 (Ultrametric recall).** Given a cue $q \in X$ and an ultrametric memory space $(M, d)$, the *recalled memory* $m^*$ is:

$m^* = \arg\min_{m \in M} d(q, m)$

subject to an energy threshold $E(m) \leq E_{\text{threshold}}$. The recall process corresponds to a descent through the ultrametric dendrogram from the leaf containing $q$ to the basin of attraction containing $m^*$ [speculative — see Krotov 2021 for hierarchical Hopfield descent].

**Connection to literature:**
- Baffioni & Rosati (2000): the overlap matrix $Q_{ab}$ in mean-field spin glasses is provably ultrametric
- v-PuNNs (N'guessan, 2025): neurons are characteristic functions of $p$-adic balls, giving explicit ultrametric structure
- Krotov (2021): hierarchical Hopfield networks implement multi-layer recall descent

---

### 2.2 Braided Memory Structure

**Definition 2.2.1 (Braided monoidal category).** A *braided monoidal category* $(\mathcal{C}, \otimes, I, \alpha, \lambda, \rho, \beta)$ consists of:

- A category $\mathcal{C}$
- A tensor product $\otimes: \mathcal{C} \times \mathcal{C} \to \mathcal{C}$
- A unit object $I$
- Associator $\alpha_{A,B,C}: (A \otimes B) \otimes C \cong A \otimes (B \otimes C)$
- Left/right unitors $\lambda_A: I \otimes A \cong A$, $\rho_A: A \otimes I \cong A$
- Braiding $\beta_{A,B}: A \otimes B \cong B \otimes A$

satisfying the pentagon identity (for $\alpha$), triangle identity (for $\lambda, \rho$), and hexagon identities (for $\beta$ with $\alpha$).

**Definition 2.2.2 (Memory braid category).** Let $\mathcal{M}$ be a category where:

- **Objects** are memory traces $m \in M$
- **Morphisms** $f: m \to n$ are associative links — a morphism exists if $m$ and $n$ are associatively bound (e.g., share an episode, context, or emotional tag)
- **Monoidal product** $m \otimes n$ is the *co-occurrence* of two memory traces in a composite episode — the simultaneous storage or retrieval of two associated traces
- **Braiding** $\beta_{m,n}: m \otimes n \to n \otimes m$ is the *associative swap* — recalling $m$ then $n$ vs. recalling $n$ then $m$, where the order matters because recall is non-commutative (context effects, priming)

The braiding $\beta_{m,n}$ is NOT the trivial swap. In the quipu model, $\beta_{m,n}$ corresponds to physically twisting two cords together — the ordering of knots on intertwined cords matters. The hexagon identity $\beta_{m \otimes n, p} = (\beta_{m,p} \otimes \text{id}_n) \circ (\text{id}_m \otimes \beta_{n,p})$ encodes the consistency of multi-way associative binding.

**Definition 2.2.3 (Knot as a morphism).** A *knot* in the memory braid is a morphism $k: m \otimes n \to m \otimes n$ that is not isotopic to the identity — i.e., the associative link between $m$ and $n$ cannot be undone without cutting the strands. In the quipu model, this is the physical knot tied at a specific position on the main cord.

**Connection to literature:**
- Marsh et al. (2025): spurious patterns in quantum-optical spin glasses serve as dynamical bridges between stored memories — these bridges are the morphisms in $\mathcal{M}$
- The braid group $B_n$ provides the formal language: $\sigma_i$ = "braid strand $i$ over strand $i+1$" maps to "associate memory $i$ with memory $i+1$"

---

### 2.3 Content-Addressable Version DAG

**Definition 2.3.1 (Content-addressable memory store).** A *content-addressable memory store* is a triple $(S, H, \sim)$ where:

- $S$ is a set of memory *states* (representations of memories at a given time)
- $H: S \to \{0,1\}^k$ is a *hash function* mapping each state to a fixed-length identifier
- $\sim$ is an equivalence relation on $S$ defined by $s \sim s' \iff H(s) = H(s')$

The hash $H(s)$ is the *content address* — retrieving a memory requires knowing its content (or a close approximation), not its location. This is the fundamental property of both Hopfield networks (recall by pattern completion, not by index) and Git (retrieval by hash, not by filename).

**Definition 2.3.2 (Memory version DAG).** A *memory version DAG* is a directed acyclic graph $(V, E)$ where:

- $V \subseteq S$ is a set of memory states (each content-addressed)
- $(u, v) \in E$ iff $v$ is a *modification* of $u$ — i.e., $v$ was produced by recalling $u$ and altering it (reconsolidation, context shift, or counterfactual elaboration)
- The DAG property ensures no circular dependencies (a memory cannot be a modification of its own modification)
- Multiple outgoing edges from $u$ represent *forks* (alternative versions)
- Multiple incoming edges to $v$ represent *merges* (two memories reconciled)

**Definition 2.3.3 (Merge operation).** A *merge* is a binary operation $\sqcup: S \times S \to S$ such that:

- $H(u \sqcup v)$ depends on both $H(u)$ and $H(v)$ (the merged memory's address reflects both sources)
- $u$ and $v$ are both ancestors of $u \sqcup v$ in the DAG
- $u \sqcup v \neq u$ and $u \sqcup v \neq v$ (merge produces a genuinely new state)
- $u \sqcup v = v \sqcup u$ (merge is commutative — reconciliation order does not matter)

**Connection to literature:**
- Git: each commit is content-addressed (SHA-1 hash of tree + parent + message). Merge commits have two parents.
- MerkleSpeech (Ono, 2026): audio chunks hashed in a Merkle tree for provenance verification
- Memory reconsolidation literature: updating a memory creates a new trace while the hippocampus retains a versioned record [speculative — see supporting papers]

---

### 2.4 Social Propagation DAG

**Definition 2.4.1 (Social memory propagation DAG).** A *social memory propagation DAG* is a pair $(P, G)$ where:

- $P = \{p_1, p_2, \dots, p_n\}$ is a set of *agents* (minds, accounts, nodes)
- $G = (V_G, E_G)$ is a DAG where:
  - Each node $v \in V_G$ is a memory state held by a specific agent at a specific time
  - An edge $(u, v) \in E_G$ indicates that agent $A(v)$ received memory $v$ from agent $A(u)$ (a *forward*, *retweet*, or *retelling*)
  - The global DAG $G$ is the union of all propagation chains

**Definition 2.4.2 (Fork and attribution).** A node $v \in V_G$ *forks* if it has exactly one incoming edge but multiple outgoing edges — i.e., one agent propagates to many. The *attribution chain* of $v$ is the unique path from the root (original memory) to $v$, which is always a chain (each node has at most one parent in a single propagation lineage).

**Observation 2.4.3 (Structural identity).** The social propagation DAG is structurally identical to a Git commit DAG where branches are independent propagation chains and merges are collaborative reconciliations (shared narratives, consensus memories). The quipu model adds that each forward is a *new pendant string* tied to the main cord at the point of reception [my conjecture].

---

## 3. The Unified Structure: Braided Ultrametric Register

### 3.1 Tentative Definition

**Definition 3.1.1 (Braided Ultrametric Register).** A *Braided Ultrametric Register* $\mathcal{B}$ consists of:

1. **An ultrametric memory space** $(M, d, E)$ — the hierarchical content structure (the "tree")

2. **A braided monoidal category** $(\mathcal{M}, \otimes, I, \beta)$ where $\text{Obj}(\mathcal{M}) = M$ — the associative binding structure (the "braids")

3. **A content-addressable store** $(S, H, \sim)$ where $S = \bigcup_{t \in T} M_t$ is the set of all memory states across all times — the identification structure (the "hashes")

4. **A memory version DAG** $(V_G, E_G)$ where $V_G \subseteq S$ — the temporal/traceable structure (the "versions")

5. **A social propagation DAG** $(P, G)$ — the distributed structure (the "forwards")

6. **Coherence conditions:**

   **(a) Ultrametric-Braiding compatibility.** For any $m, n, p \in M$, the ultrametric distance $d$ and the braiding $\beta$ must satisfy:
   $$d(m, n) \leq \max\{d(m, m \otimes n), d(n, m \otimes n)\}$$
   This ensures that the monoidal product (co-occurrence) respects the ultrametric hierarchy — co-occurring memories are at least as close to each other as either is to the composite.

   **(b) Content-Addressable DAG compatibility.** For any edge $(u, v) \in E_G$:
   $$d(u, v) \leq \epsilon \cdot d_{\text{max}}$$
   where $\epsilon < 1$ is a threshold. Adjacent versions in the DAG must be similar (a modification preserves most of the original content).

   **(c) Social propagation as DAG embedding.** For each agent $p \in P$, the subgraph $G|_p$ (the portion of $G$ visible to agent $p$) is isomorphic to the agent's local version DAG. The global DAG $G$ is the pushout of all local DAGs over shared memory states.

   **(d) Braid-word length = ultrametric depth.** For any two memory traces $m, n \in M$, the minimal braid word $\beta_{m,n}$ (the shortest sequence of $\sigma_i$ that swaps $m$ and $n$) has length equal to the ultrametric distance $d(m, n)$ (up to a scaling factor). This is the **central conjectured connection** — `[my conjecture — unproven]`.

### 3.2 Implications

If condition 6(d) holds, it provides a **direct isomorphism** between the ultrametric dendrogram (hierarchical clustering of memory traces) and the braid group representation of associative links:

- **Ultrametric depth = 0** ($d(m,n) = 0$): $m$ and $n$ are the same memory — braid word is empty
- **Ultrametric depth = 1**: $m$ and $n$ share an immediate parent — adjacent in the associative web, swapped by a single $\sigma_i$
- **Ultrametric depth = k**: $m$ and $n$ are separated by k branching levels — requires k braid crossings

This would mean the "file cabinet" structure (tree depth) and the "associative binding" structure (braid crossings) are **two representations of the same underlying order**. The quipu's intertwined cords and the dendrogram's nested clusters describe the same thing — one in physical terms (knots between strings) and one in metric terms (distances between leaves).

### 3.3 Remaining Formal Questions

1. **Existence:** Does there exist a category $\mathcal{M}$ that simultaneously admits both an ultrametric distance $d$ on its objects and a braided monoidal structure whose braid word lengths are proportional to ultrametric distances?

2. **Uniqueness:** If such a category exists, is it unique up to equivalence? Or are there multiple inequivalent braided ultrametric categories?

3. **Coherence:** Do the four coherence conditions (a-d) imply any contradiction with the standard axioms of braided monoidal categories?

4. **Completion:** Given a braided ultrametric register $\mathcal{B}$ defined only on a subset of $M \times T \times P$, can we uniquely extend it to new memories, times, or agents?

---

## 4. Connection to Existing Mathematics

| Component | Existing Mathematical Structure | Gap |
|:----------|:-------------------------------|:----|
| Ultrametric tree | $\mathbb{Z}_p$ with $p$-adic metric; dendrograms from hierarchical clustering | No braided enrichment |
| Braided monoidal category | $B_n$-representations; any braided monoidal category (e.g., representations of a quantum group) | No ultrametric structure on objects |
| Content-addressable store | Merkle tree; cryptographic hash DAG | No connection to neural/cognitive models |
| Version DAG | Git object model; causal set theory | DAGs don't have ultrametric or braided structure |
| Social propagation | Graph theory; information cascade models | No formal pushout semantics for distributed memory |

---

## 5. Minimal Prototype Specification

To validate the Braided Ultrametric Register computationally, a minimal prototype should:

1. **Ultrametric layer:** Use v-PuNNs ($\mathbb{Z}_p$ ball neurons) to learn hierarchical representations of a small corpus of episodic memories
2. **Association layer:** Encode co-occurrence counts as braid crossings between memory traces — edge weight determines $\sigma_i$ order
3. **Version layer:** Store each recall/modification as a content-addressed node in a DAG, with hashes of neural states
4. **Propagation layer:** Simulate forward/repost chains as DAG edges across simulated agents

**Input:** Sequences of temporally ordered events with multimodal tags.
**Output:** A DAG where recall traversals respect ultrametric energy descent and braided associative binding.
**Validation:** The braid word length = ultrametric depth conjecture (3.1.1 condition 6d) should hold empirically on the learned representation.

---

## References

1. Baffioni, F. & Rosati, F. (2000). "Some Exact Results on the Ultrametric Overlap Distribution in Mean Field Spin Glass Models (I)." DOI: 10.1007/s100510070123.
2. N'guessan, G.L.R. (2025). "v-PuNNs: van der Put Neural Networks for Transparent Ultrametric Representation Learning." arXiv:2508.01010v2.
3. Marsh, B.P. et al. (2025). "High-capacity associative memory in a quantum-optical spin glass." arXiv:2509.12202v1.
4. Krotov, D. (2021). "Hierarchical Associative Memory." arXiv:2107.06446v1.
5. Rammal, R., Toulouse, G., & Virasoro, M.A. (1986). "Ultrametricity for physicists." Reviews of Modern Physics, 58(3), 765.

---

*Working Draft v1.0 — 2026-07-03. Subject to revision. All conjectured connections labeled `[my conjecture]`. Falsification condition: contradiction among coherence axioms or lack of existence of a category satisfying all five properties.*
