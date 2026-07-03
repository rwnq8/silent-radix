# DATA QUALITY FINDING: Living-Paper D1 Author Attribution

**Date:** 2026-07-03 | **Project:** braided-memory-register

## Finding

All 100 papers in the `living-paper` D1 database (queried via graph-api) have `"QNFO Research Collective"` as their sole author. No individual authors are attributed to any paper in the dataset.

## Impact on Conjecture Validation

The braided-register central conjecture ($\delta(a,b) = c \cdot w(a,b)$) requires **individual author attribution** to produce meaningful co-authorship edges. With all papers sharing the same author, every pair has a co-authorship edge → all braid distances are 1 → no variation → the conjecture cannot be tested.

## Required Remediation

1. Populate living-paper D1 with individual author names for each paper
2. Alternatively: use domain/category tags as an intermediate proximity measure
3. Alternatively: use the Knowledge Graph's ultrametric taxonomy (4 domains, 12 programs) to classify papers

## Current State

| Metric | Value |
|:-------|------:|
| Papers with individual authors | 0 / 100 |
| Papers with categories | ~10 / 100 (mostly empty arrays) |
| Citation edges (KG REFERENCES) | 38 |
| Connected components (citation-only) | 97 (mostly isolates) |
| Viable conjecture test | BLOCKED — insufficient metadata |

## Next Steps

1. **Immediate:** Publish position paper as-is, documenting this data gap honestly
2. **Medium:** Populate living-paper with individual author attributions
3. **Medium:** Generate domain tags from existing QNFO taxonomy
4. **Long-term:** Re-run conjecture test with enriched metadata

---

*This is a data infrastructure finding, not a model failure. The Braided Register framework predicts that with proper metadata (individual authors, categories, citation links), the relaxed conjectures will show significant correlation between ultrametric and braid distances.*
