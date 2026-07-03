# RESEARCH PLAN: Braided Memory Register — A Consilient Model of Memory Across Mathematics, Computation, and Social Propagation

**Author:** QNFO Research Agent | **Date:** 2026-07-03 | **Status:** Phase 1 — Literature Review
**Project:** braided-memory-register

---

## 1. Research Genesis

This project emerged from a dialogue tracing a chain of converging analogies, each revealing a different facet of memory structure. The thread itself performed what it described — a self-similar, braided construction:

| Conceptual Thread | Domain | Core Insight |
|:------------------|:-------|:-------------|
| **Ultrametrics** | Mathematics | Memory is tree-like, not network-like. The strong triangle inequality d(x,z) <= max{d(x,y), d(y,z)} forces nested hierarchical clustering — the "file cabinet" structure. Recall is an energy cascade down ultrametric basins of attraction. |
| **Quipu (Khipu)** | Andean record-keeping | Memory is a braided physical register: a main cord (time), pendant strings (categories), and knots (multimodal bindings). Strings intertwine — associative cross-links between branches. |
| **Blockchain** | Distributed ledgers | Memory requires sequential integrity via hash-linked chains. Forking and consensus mirror memory consolidation of conflicting versions. |
| **Git version control** | Software engineering | Memory is a DAG of commits — branching (alternative pasts), merging (reconciled narratives), blame (provenance tracking). Every commit is content-addressable. |
| **Conversation forwards/reposts** | Social propagation | Memory propagates socially, forking with each retweet. The chain of attribution is a quipu whose main cord splits as it passes through minds. The dialogue itself is a live instance. |

### The Convergent Hypothesis

These five domains are not merely analogous — they converge on a **single abstract structure**: a *braided, versioned, ultrametric weave* where every knot is content-addressable, carries proof of provenance, and sits at the intersection of hierarchical similarity (tree), temporal order (chain), associative binding (knot), version history (DAG), and social propagation (forwarding).

**Central research question:** Is there a formal mathematical framework that unifies these properties — ultrametric topology, braided monoidal structure, and content-addressable versioning — into a single model of memory applicable to both biological and artificial systems?

---

## 2. Theoretical Pillars

### 2.1 Ultrametric Topology of Memory

Memory representations form an ultrametric space where:
- **Distance** = dissimilarity between memory traces
- **The strong triangle inequality** guarantees that all triangles are acutely isosceles, forcing hierarchical clustering
- **Energy landscapes** (Hopfield networks, spin glasses) exhibit ultrametric organization of attractor basins [established]
- **Recall** is a flow along the ultrametric tree from a cue to the nearest stored pattern

Key references to verify: Rammal et al. (1986) on ultrametricity in spin glasses; Parga & Virasoro (1986) on ultrametric organization of memories in neural networks; Parisi's replica symmetry breaking solution [established].

### 2.2 Quipu as a Material Model of Braided Memory

The quipu encodes information in a structure that is simultaneously:
- **Linear** (main cord = temporal sequence)
- **Hierarchical** (pendant and subsidiary strings = categorical nesting)
- **Associative** (intertwined cords = cross-modal binding at knots)
- **Positional** (knot type and position encode value in a base-10 system)

This suggests a formal model: memory traces as **braids in a category** where objects are temporal positions, morphisms are associative links, and the braid group B_n captures the non-commutative intertwining of memory strands [my conjecture].

### 2.3 Content-Addressable Versioning

Git and blockchain share a critical property: **content-addressable storage** — the identifier of a memory is a cryptographic hash of its content. This ensures:
- **Immutability:** altering content changes its address (tamper-evident)
- **Provenance:** each version points to its predecessor(s) via hash
- **Forking:** multiple versions can coexist (alternative memories, counterfactuals)

This maps to cognitive phenomena: memory reconsolidation (rewriting with awareness of prior version), source monitoring (attributing a memory to its origin), and the boundary between episodic and semantic memory (forked vs. merged branches) [speculative].

### 2.4 Social Propagation and Collective Memory

Conversation threads, retweet chains, and oral traditions exhibit the same structure at the social scale:
- Each forward/repost is a **fork** of the original memory
- The chain of attribution is a **DAG** of provenance
- Repeated retelling **re-encodes** the memory (knots tighten or loosen)
- Collective consensus is a **merge** operation over conflicting versions

---

## 3. Research Questions

1. **RQ1 (Formal):** Can the ultrametric tree, braid group, and content-addressable DAG be unified in a single mathematical structure — e.g., a *braided ultrametric space* or a *dendroidal object with braided enrichment*?

2. **RQ2 (Cognitive):** Does human memory empirically exhibit versioning/merging behavior (as git does), and if so, under what conditions do memories fork vs. overwrite?

3. **RQ3 (Neural):** Is there evidence for ultrametric organization in actual neural population dynamics during memory recall, beyond the theoretical models of Hopfield/Parisi?

4. **RQ4 (AI Architecture):** Can we design an artificial memory system (for LLMs, RAG, or autonomous agents) that natively implements braided-ultrametric-versioned storage, rather than bolting together vector DBs, context windows, and chain-of-thought?

5. **RQ5 (Mathematical):** Does the category of ultrametric spaces admit a braided monoidal structure? What are the coherence conditions?

6. **RQ6 (Quipu):** What formal grammars or information-theoretic analyses exist for quipu encoding? Can quipu be modeled as a braided operad?

---

## 4. Phased Research Plan

### Phase 1 — Literature Review (CURRENT)
- Search: ultrametric memory, hierarchical clustering in neural networks, braided categories in cognition, content-addressable memory models, quipu information theory, memory reconsolidation as versioning
- Sources: Preprint servers, Semantic Scholar, QNFO Vectorize, web search
- Output: Classified literature brief with core/supporting/background tiers

### Phase 2 — Deep Reading & Formalization
- Close-read core papers
- Extract formal definitions and theorems
- Map existing formalisms to the braided-register model
- Identify gaps where no formal bridge exists

### Phase 3 — Mathematical Synthesis
- Attempt to construct a unified definition: *Braided Ultrametric Register*
- Connect existing theorems (ultrametric to dendrogram, braid to knot invariants, DAG to partial order, content-addressable to Merkle tree)
- Identify what new mathematics would need to be proved

### Phase 4 — Publication
- Target: Zenodo preprint to Cloudflare Pages deployment
- Format: Technical report with mathematical formalism
- Potential contribution: A unified abstract model of memory across biological, computational, and social domains

---

## 5. Expected Contributions

1. A **consilient synthesis** across five disparate domains, demonstrating that they are facets of a single abstract structure
2. A **formal definition** of a Braided Ultrametric Register (or proof that no such object exists under standard assumptions)
3. **Empirical predictions** for cognitive science: do memories exhibit git-like branching/merging?
4. **Architectural implications** for AI: what would a braided-register memory system look like for LLMs?

---

## 6. Uncertainty and Limitations

- [my conjecture] The claim that these five domains converge on a single abstract object has not been formally proved — it is a hypothesis derived from structural analogy
- [not yet falsifiable] Some aspects of the cognitive versioning hypothesis (RQ2) may not be empirically testable with current methods
- **Falsifiability condition:** The braided-register hypothesis would be disconfirmed if (a) no formal structure exists that simultaneously satisfies ultrametric, braided, and content-addressable properties, or (b) empirical evidence shows memory retrieval is flat/network-like rather than hierarchically ultrametric
- **Scope boundary:** This is a theoretical synthesis. It does not claim to explain all of memory — only to unify a particular set of structural analogies that have emerged as robust across domains.

---

## 7. Related QNFO Work

- **silent-radix** (2026-07 release): Radix underwater wireless — no direct overlap but shares the theme of information encoding in physical structures
- **radix-uw-bt-synthesis**: Possibly adjacent in its concern with hierarchical information encoding
- **Ultrametric Engine**: Existing QNFO infrastructure for ultrametric tree construction and p-adic ranking — directly applicable as a computational substrate for the proposed model

---

---

## 8. Phase 1 Results — Literature Review (2026-07-03)

### Search Summary

| Metric | Value |
|:-------|------:|
| Sources | Preprint API (10 query threads) |
| Raw papers retrieved | ~186 |
| After deduplication | 177 |
| Core papers | 5 |
| Supporting papers | 48 |
| Background papers | 78 |
| Rejected | 46 |

### Core Papers

| # | Title | Authors | Year | Relevance |
|:--|:------|:--------|-----:|:----------|
| 1 | **v-PuNNs: van der Put Neural Networks for Transparent Ultrametric Representation Learning** | G.L.R. N'guessan | 2025 | Directly implements ultrametric (p-adic) neural architectures — provides computational substrate for Pillar 2.1 |
| 2 | **High-capacity associative memory in a quantum-optical spin glass** | Marsh, Schuller, Ji | 2025 | Demonstrates associative recall in spin glass energy landscapes — confirms the ultrametric basin model of Pillar 2.1 |
| 3 | **Hierarchical Associative Memory** | Dmitry Krotov | 2021 | Extends Modern Hopfield Networks to hierarchical (multi-layer) associative memory — bridges Pillars 2.1 and 2.3 |
| 4 | **Hierarchical Variational Memory for Few-shot Learning Across Domains** | Du, Zhen, Shao | 2021 | Hierarchical latent memory with multi-level storage — empirical validation of tree-structured memory in ML |
| 5 | **Some Exact Results on the Ultrametric Overlap Distribution in Mean Field Spin Glasses** | Baffioni, Rosati | 2000 | Foundational paper on ultrametricity in spin glass energy landscapes — mathematical basis for the entire framework |

### Key Supporting Papers (Selected)

- **Structural Pattern Mining in Inka Khipus** (Contreras, 2026) — computational analysis of quipu structures, directly relevant to Pillar 2.2
- **MerkleSpeech: Public-Key Verifiable Speech Provenance** (Ono, 2026) — Merkle tree-based provenance tracking, aligns with Pillar 2.3
- **Continual Knowledge Updating in LLM Systems** (Pattichis, Dovrolis, 2026) — multi-timescale memory dynamics, relevant to RQ4

### Thread-by-Thread Analysis

| Thread | Papers | Core | Key Finding |
|:-------|-------:|-----:|:------------|
| ultrametric_memory | 20 | 2 | Strong existing literature on ultrametric neural nets and p-adic architectures |
| associative_hierarchical | 20 | 2 | Hierarchical memory models well-developed in ML (Modern Hopfield, variational memory) |
| hopfield_spin_glass | 19 | 1 | Foundational work on ultrametricity in disordered systems confirmed |
| braided_memory | 20 | 0 | No core papers — category theory / braid groups rarely applied to memory |
| content_addressable | 20 | 0 | Content-addressable memory in hardware/CS literature, not linked to neural models |
| reconsolidation | 20 | 0 | Rich neuroscience literature on memory updating, but no versioning/merging formalism |
| quipu_encoding | 6 | 0 | Computational archaeology emerging; no formal information-theoretic model of quipu |
| dendrogram_neural | 20 | 0 | Dendrograms used as visualization, not as first-class data structures |
| merkle_version | 12 | 0 | Merkle trees for provenance, not connected to memory theory |
| category_memory | 20 | 0 | Category theory applied to learning, but no braided structure for memory |

### Gap Confirmation

The literature search **confirms the research gap**: no existing paper unifies ultrametric hierarchy, braided structure, content-addressable versioning, and social propagation into a single memory model. Each pillar exists in isolation:

- **Ultrametricity** is well-studied in spin glasses and emerging in ML (v-PuNNs, 2025)
- **Hierarchical memory** is active in ML (Krotov 2021, Du et al. 2021)
- **Braided/topological models** of cognition are scattered and underdeveloped
- **Content-addressable versioning** (Merkle/Git) has no cognitive application
- **Quipu information theory** is an emerging computational archaeology field
- **Social propagation as memory DAG** has no formal treatment

The convergent hypothesis — that these are facets of a single abstract structure — remains **unexplored in the literature** [established by search — no paper found bridging these domains].

### Recommended Next Phase

1. Deep-read Core Papers 1-5 with formal note-taking
2. Map each paper's formalism onto the braided-register model properties
3. Identify the minimal mathematical bridge needed between ultrametric topology and braided monoidal categories
4. Draft a position paper outlining the convergent hypothesis with evidence from each pillar

---

*Generated 2026-07-03. This plan is a living document — update as literature is integrated.*
