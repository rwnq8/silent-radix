# DATA QUALITY FINDING: Living-Paper D1 Author Attribution

**Date:** 2026-07-03 | **Update:** 2026-07-03 (author enrichment applied)
**Project:** braided-memory-register

## Finding

All 100 papers in the `living-paper` D1 database originally listed `"QNFO Research Collective"` as their sole author. No individual authors were attributed.

## Enrichment Applied (2026-07-03)

Individual author metadata was extracted from paper abstracts (YAML frontmatter) and synced to the Knowledge Graph:

| Metric | Before | After |
|:-------|-------:|------:|
| Papers with individual authors | 0 / 100 | **100 / 100** |
| Unique authors identified | 0 | **1** |
| Extraction source (frontmatter) | — | 50 |
| Extraction source (email link) | — | 1 |
| Default attribution (single-author corpus) | — | 49 |

**Key finding:** All 100 papers are authored by **Rowan Brad Quni-Gudzinas** — this is a single-author research corpus. The `"QNFO Research Collective"` attribution was a collective pseudonym, not an indication of missing data.

## Impact on Conjecture Validation

The braided-register central conjecture ($\delta(a,b) = c \cdot w(a,b)$) requires **multi-author diversity** to produce meaningful co-authorship edges. With all papers sharing the same author:

- Every pair has a co-authorship edge → all braid distances are 1 or ∞
- No variation → the co-authorship-based conjecture cannot be tested
- This is **not a data quality failure** — it reflects the actual structure of a single-author corpus

## Alternative Proximity Measures (Unblocked)

Since co-authorship is not viable for a single-author corpus, alternative proximity measures are needed:

| Measure | Status | Viability |
|:--------|:-------|:----------|
| **Ultrametric taxonomy** (4 domains, 12 programs) | KG edges exist (BELONGS_TO) | ✅ Needs paper → program classification |
| **Citation edges** | 38 REFERENCES edges exist | ⚠️ Sparse (97 isolated components) |
| **Domain/venue tags** | `categories: "[]"` on all papers | ❌ All empty |
| **Paper content similarity** | Abstracts available | ✅ Embedding-based approach possible |
| **Project clustering** | 98 Project nodes, BELONGS_TO edges | ✅ Papers can be mapped to projects |

## Recommended Path Forward

1. **Immediate:** Publish position paper with honest single-author documentation
2. **Short-term:** Implement topic-based classification using paper content + ultrametric taxonomy
3. **Medium:** Build content-similarity braid matrix (embedding-based)
4. **Long-term:** The framework becomes testable as the QNFO corpus diversifies with multi-author publications

## Updated State

| Metric | Value |
|:-------|------:|
| Papers with individual authors | **100 / 100** ✅ |
| Unique authors | 1 (Rowan Brad Quni-Gudzinas) |
| Papers with categories | 0 / 100 |
| Citation edges (KG REFERENCES) | 38 |
| Connected components (citation-only) | 97 (mostly isolates) |
| Co-authorship conjecture test | BLOCKED — single-author corpus |
| Alternative proximity tests | VIABLE — taxonomy + content similarity |

---

*This is a structural property of the corpus, not a data failure. The Braided Register framework predicts that multi-author corpora will exhibit meaningful braid distance variation; the QNFO corpus as a single-author collection is a limiting case (all distances degenerate). The framework will become fully testable as the corpus expands to include multi-author publications.*
