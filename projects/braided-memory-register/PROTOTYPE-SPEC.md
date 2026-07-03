# PROTOTYPE SPECIFICATION: Minimal Braided Ultrametric Register

**Author:** QNFO Research Agent | **Date:** 2026-07-03
**Status:** Specification — Phase 3c Computational Validation
**Project:** braided-memory-register

---

## 1. Purpose

Validate the central conjecture — ultrametric distance = braid word length (up to scaling) — on a small, synthetic corpus before attempting full mathematical proof. This prototype is *not* intended to be production-scale; it exists to test the hypothesis that training a hierarchical neural memory on temporally ordered, associatively linked events produces representations where dendrogram depth and braid crossings are proportionally related.

**Scope:** Single-machine Python. No Cloudflare deployment. Synthetic data only (10-20 episodic sequences with tagged associations). Runtime target: under 60 seconds for full pipeline.

---

## 2. Architecture

```
┌─────────────────────────────────────────────────┐
│               INPUT: Event corpus                 │
│  (temporally ordered sequences, each event has   │
│   tags: [category, emotion, context, agent])      │
└────────────────────┬────────────────────────────┘
                     │
     ┌───────────────┼───────────────┐
     ▼               ▼               ▼
┌─────────┐   ┌────────────┐  ┌──────────────┐
│  LAYER 1│   │  LAYER 2   │  │  LAYER 3     │
│ Tokenize│   │ Hierarchical│  │ Version DAG  │
│ events  │──▶│ embedding  │──▶│ constructor  │
│         │   │ (v-PuNN    │  │ (content-    │
│         │   │  analog)   │  │ addressable) │
└─────────┘   └─────┬──────┘  └──────┬───────┘
                    │                │
                    ▼                ▼
           ┌────────────┐   ┌──────────────┐
           │ ULTRAMETRIC│   │ BRAID MATRIX │
           │ DENDROGRAM │   │ (associative  │
           │ (distance   │   │  links from  │
           │  matrix)    │   │  co-occur.)  │
           └─────┬──────┘   └──────┬───────┘
                 │                │
                 └───────┬────────┘
                         ▼
                ┌─────────────────┐
                │   VALIDATION    │
                │ δ(i,j) vs w(i,j)│
                │ R² correlation  │
                └─────────────────┘
```

### Layer 1: Event Tokenizer

Translates raw events into numerical vectors. Since we use synthetic data, no NLP needed — direct one-hot or learned embedding of categorical tags.

```python
def tokenize_events(events):
    """
    Input: events = [
        {"time": 0, "agent": "A", "action": "see", "object": "tree", "emotion": "calm"},
        {"time": 1, "agent": "B", "action": "speak", "object": "A", "emotion": "curious"},
        ...
    ]
    Output: matrix of shape (num_events, embed_dim)
    """
    # Simple approach: concatenate one-hot encodings of categorical fields
    # embed_dim = sum of vocab sizes across all fields
    # For prototype: ~200-dimensional vectors for ~20 events
    pass
```

### Layer 2: Hierarchical Embedding (v-PuNN Analog)

Ideally we would use true v-PuNNs (N'guessan, 2025) with $p$-adic ball neurons. For the prototype, we approximate with a **hierarchical clustering autoencoder**: a bottleneck architecture that learns a tree-structured latent space.

```python
def build_hierarchical_embedder(input_dim, tree_depth=4):
    """
    Returns a PyTorch model that:
    - Encodes input -> latent at each level of tree_depth
    - Supports hierarchical regularization loss:
      distance in latent space proportional to tree depth
    - Output: latent_vectors shape (num_events, tree_depth, latent_dim)
    """
    model = HierarchicalAutoencoder(
        encoder_dims=[input_dim, 128, 64, 32, 16],   # decreasing
        decoder_dims=[16, 32, 64, 128, input_dim],   # symmetric
        tree_depth=tree_depth
    )
    return model

# Loss function enforces ultrametric structure:
def ultrametric_regularization(latent_vectors):
    """
    For all triples (i,j,k), penalize violations of:
        d(i,k) <= max(d(i,j), d(j,k))
    Loss = sum of positive violations (ReLU)
    """
    n = len(latent_vectors)
    dist = pairwise_euclidean(latent_vectors)
    violations = 0
    for i in range(n):
        for j in range(n):
            for k in range(n):
                v = dist[i][k] - max(dist[i][j], dist[j][k])
                violations += max(0, v)
    return violations
```

### Layer 3: Content-Addressable Version DAG

Each event's latent vector is hashed (SHA-256 of binarized representation). Temporal ordering defines parent-child edges. Co-occurrence defines fork/merge edges.

```python
import hashlib

def hash_latent(latent_vec, precision=4):
    """Content-address memory via hash of quantized latent."""
    quantized = tuple(round(float(x), precision) for x in latent_vec.numpy())
    h = hashlib.sha256(str(quantized).encode()).hexdigest()[:16]
    return h

def build_version_dag(events, latent_vectors, association_threshold=0.7):
    """
    Builds DAG where:
    - Nodes = events, content-addressed by hash of latent
    - Edges = temporal order (parent -> child) + associative co-occurrence
    """
    nodes = []
    edges = []
    for i, (event, vec) in enumerate(zip(events, latent_vectors)):
        node_id = hash_latent(vec)
        nodes.append({"id": node_id, "event": event, "time": event["time"]})
        if i > 0:
            edges.append((nodes[i-1]["id"], node_id, "temporal"))
    
    # Add associative edges based on shared context tags
    for i in range(len(events)):
        for j in range(i+1, len(events)):
            sim = cosine_similarity(latent_vectors[i], latent_vectors[j])
            if sim > association_threshold:
                edges.append((nodes[i]["id"], nodes[j]["id"], "associative"))
    
    return nodes, edges
```

---

## 3. Synthetic Data Generation

```python
def generate_synthetic_episodes(num_episodes=10, events_per_episode=8):
    """
    Generates structured episodic memory data with hierarchical categories.
    
    Structure:
    - 3 top-level domains: [HOME, WORK, SOCIAL]
    - Each domain has 2-3 sub-domains
    - Each episode is a temporal sequence within one sub-domain
    - Cross-episode associations: same agent appears in multiple episodes
    
    Returns: list of event dicts with time, agent, domain, subdomain, action, emotion
    """
    import random
    random.seed(42)  # reproducibility
    
    domains = ["HOME", "WORK", "SOCIAL"]
    subdomains = {
        "HOME": ["morning_routine", "evening_meal", "weekend_chores"],
        "WORK": ["meeting", "coding", "break"],
        "SOCIAL": ["party", "coffee", "walk"]
    }
    agents = ["Alice", "Bob", "Carol", "Dave"]
    emotions = ["calm", "anxious", "happy", "frustrated", "curious", "tired"]
    actions = {
        "morning_routine": ["wake", "shower", "breakfast", "dress"],
        "evening_meal": ["cook", "eat", "clean", "relax"],
        "weekend_chores": ["laundry", "garden", "shop", "organize"],
        "meeting": ["present", "discuss", "note", "decide"],
        "coding": ["write", "test", "debug", "commit"],
        "break": ["coffee", "chat", "walk", "return"],
        "party": ["arrive", "greet", "dance", "leave"],
        "coffee": ["order", "sip", "talk", "pay"],
        "walk": ["start", "observe", "think", "return"]
    }
    
    events = []
    time = 0
    for ep in range(num_episodes):
        domain = random.choice(domains)
        subdomain = random.choice(subdomains[domain])
        agent = random.choice(agents)
        for act in actions[subdomain]:
            events.append({
                "time": time,
                "episode": ep,
                "domain": domain,
                "subdomain": subdomain,
                "agent": agent,
                "action": act,
                "emotion": random.choice(emotions)
            })
            time += 1
    return events
```

---

## 4. Braid Matrix Construction

The "braid word length" $w(i,j)$ is computed from the associative co-occurrence matrix — not from a true braid group representation, but from a proxy: the **shortest path** in the undirected graph where nodes are events and edges are associative links.

```python
def compute_braid_word_lengths(nodes, edges, n_events):
    """
    Proxy for braid word length: shortest path in the associative graph.
    
    In the full Braided Ultrametric Register, this would be the minimal
    sequence of sigma_i generators to swap two memory positions.
    For the prototype, we approximate with graph distance.
    """
    # Build adjacency from associative edges only
    adj = {i: set() for i in range(n_events)}
    for src_id, tgt_id, etype in edges:
        if etype == "associative":
            src_idx = id_to_index[src_id]
            tgt_idx = id_to_index[tgt_id]
            adj[src_idx].add(tgt_idx)
            adj[tgt_idx].add(src_idx)
    
    # Dijkstra for all pairs
    from collections import deque
    w = [[float('inf')] * n_events for _ in range(n_events)]
    for start in range(n_events):
        w[start][start] = 0
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if w[start][v] == float('inf'):
                    w[start][v] = w[start][u] + 1
                    queue.append(v)
    return w
```

---

## 5. Validation: Correlation Test

```python
def validate_conjecture(distance_matrix, braid_matrix):
    """
    Tests: delta(i,j) = c * w(i,j)
    
    Computes:
    1. Linear regression: delta ~ c * w + intercept
    2. R² (coefficient of determination)
    3. Pearson r
    4. Spearman rho (monotonicity test for weaker conjecture)
    
    Returns: dict of statistics
    """
    import numpy as np
    from scipy import stats
    
    n = len(distance_matrix)
    deltas = []
    ws = []
    for i in range(n):
        for j in range(i+1, n):
            if braid_matrix[i][j] < float('inf'):
                deltas.append(distance_matrix[i][j])
                ws.append(braid_matrix[i][j])
    
    deltas = np.array(deltas)
    ws = np.array(ws)
    
    # Linear regression
    slope, intercept, r_value, p_value, std_err = stats.linregress(ws, deltas)
    r_squared = r_value ** 2
    
    # Monotonicity (weaker conjecture)
    spearman_r, spearman_p = stats.spearmanr(ws, deltas)
    
    return {
        "slope": slope,
        "intercept": intercept,
        "r_squared": r_squared,
        "pearson_r": r_value,
        "p_value": p_value,
        "spearman_rho": spearman_r,
        "n_pairs": len(deltas),
        "supports_strong": r_squared > 0.7,
        "supports_weak": abs(spearman_r) > 0.5
    }
```

---

## 6. Success Criteria

| Criterion | Threshold | Meaning |
|:----------|:---------|:--------|
| $R^2$ (strong conjecture) | $\geq 0.7$ | Ultrametric distance is strongly predicted by braid word length |
| Spearman $\rho$ (weak conjecture) | $\geq 0.5$ | Ultrametric distance is monotonically related to braid word length |
| Ultrametric regularization loss | Decreases over training | Model learns hierarchical structure |
| DAG consistency | No cycles | Version DAG is well-formed |

---

## 7. Execution Plan

```python
def main():
    # 1. Generate synthetic data
    events = generate_synthetic_episodes(num_episodes=15, events_per_episode=8)
    # ~120 events total
    
    # 2. Tokenize
    vectors = tokenize_events(events)  # shape (120, 200)
    
    # 3. Train hierarchical embedder
    model = build_hierarchical_embedder(input_dim=200, tree_depth=4)
    vectors, loss_history = train_with_ultrametric_reg(model, vectors, epochs=500)
    # Monitor ultrametric regularization loss
    
    # 4. Build DAG
    nodes, edges = build_version_dag(events, vectors)
    
    # 5. Compute ultrametric distances
    dist_matrix = pairwise_euclidean(vectors)
    # Verify ultrametric condition empirically
    ultrametric_violation_rate = compute_ultrametric_violations(dist_matrix)
    
    # 6. Compute braid word lengths
    braid_matrix = compute_braid_word_lengths(nodes, edges, len(events))
    
    # 7. Validate
    results = validate_conjecture(dist_matrix, braid_matrix)
    
    # 8. Report
    print(f"Ultrametric violation rate: {ultrametric_violation_rate:.4f}")
    print(f"R² (strong): {results['r_squared']:.4f}")
    print(f"Spearman ρ (weak): {results['spearman_rho']:.4f}")
    
    if results["supports_strong"]:
        print("[PASS] Strong conjecture supported: δ(i,j) = c · w(i,j)")
    elif results["supports_weak"]:
        print("[PARTIAL] Weak conjecture supported: monotonic relationship")
    else:
        print("[FAIL] Neither conjecture supported on this data")
```

---

## 8. Dependencies

```bash
pip install torch numpy scipy scikit-learn networkx
```

Standard scientific Python stack. No proprietary libraries. ~10MB download.

---

## 9. Extensions (Beyond Minimal Prototype)

1. **True v-PuNN integration:** Replace the hierarchical autoencoder with actual $p$-adic ball neurons using the `vPuNN` layer from the paper
2. **Real braid group:** Replace graph-distance proxy with actual braid word-length computation using the Artin presentation and the Garside normal form algorithm
3. **Social propagation layer:** Simulate multi-agent forwarding with merge operations
4. **Real episodic data:** Replace synthetic data with the Ego4D or Epic-Kitchens dataset

---

*Specification v1.0 — 2026-07-03. Implementable in a single Python file (~300 lines). Runtime target: < 60 seconds on consumer hardware.*
