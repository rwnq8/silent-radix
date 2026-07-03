/**
 * Conjecture Test Worker — QNFO Braided Memory Register
 * 
 * Tests the central conjecture: δ(a,b) = c · w(a,b)
 * — ultrametric dendrogram depth ≈ braid word-length (up to scaling)
 * 
 * Data sources:
 *   - ask-qwav Worker (ask.qwav.tech) — ultrametric dendrogram distances δ(a,b)
 *   - braid-matrix Worker — associative braid distances w(a,b)  
 * 
 * Endpoints:
 *   GET  /                — API docs + live conjecture status
 *   GET  /test            — Full conjecture test (R², Pearson r, Spearman ρ)
 *   GET  /scatter         — Scatter plot data (δ vs w for all paper pairs)
 *   GET  /papers          — Paper list with both ultrametric and braid distances
 *   GET  /paper/:slug     — Single paper's distances to all others
 */

// ═════════════════════════════════════════════════════════════════════
// Configuration
// ═════════════════════════════════════════════════════════════════════

const ASK_QWAV = "https://ask.qwav.tech";
const BRAID_MATRIX = "https://braid-matrix.q08.workers.dev";
const CACHE_TTL = 3600; // Cache results for 1 hour

// ═════════════════════════════════════════════════════════════════════
// Main handler
// ═════════════════════════════════════════════════════════════════════

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;

    const headers = {
      "Content-Type": "application/json",
      "Access-Control-Allow-Origin": "*",
      "Cache-Control": `public, max-age=${CACHE_TTL}`
    };

    // GET / — docs
    if (path === "/" || path === "") {
      return conjectureDocs();
    }

    // GET /test — full conjecture test
    if (path === "/test") {
      const result = await runConjectureTest(env);
      return new Response(JSON.stringify(result, null, 2), { headers });
    }

    // GET /scatter — scatter plot data
    if (path === "/scatter") {
      const result = await getScatterData(env);
      return new Response(JSON.stringify(result), { headers });
    }

    // GET /papers — paper list
    if (path === "/papers") {
      const result = await getPaperList(env);
      return new Response(JSON.stringify(result), { headers });
    }

    // GET /paper/:slug
    const paperMatch = path.match(/^\/paper\/(.+)$/);
    if (paperMatch) {
      const result = await getPaperDetail(paperMatch[1], env);
      return new Response(JSON.stringify(result), { headers });
    }

    return new Response(JSON.stringify({ 
      error: "Not found", 
      endpoints: ["/", "/test", "/scatter", "/papers", "/paper/:slug"] 
    }), {
      status: 404, headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
    });
  }
};

// ═════════════════════════════════════════════════════════════════════
// Conjecture Test Engine
// ═════════════════════════════════════════════════════════════════════

async function runConjectureTest(env) {
  // Step 1: Fetch both distance matrices
  const [dendroResult, braidResult] = await Promise.all([
    fetchDendrogramDistances(env),
    fetchBraidDistances(env)
  ]);

  // Step 2: Extract paired (δ, w) samples
  const samples = [];
  const dendro = dendroResult.distances || {};
  const braid = braidResult.distances || {};

  const slugs = Object.keys(dendro).filter(s => braid[s]);
  console.log(`[conjecture-test] ${slugs.length} papers with both dendro and braid data`);

  for (const s1 of slugs) {
    for (const s2 of slugs) {
      if (s1 >= s2) continue; // Upper triangle only
      const d = dendro[s1]?.[s2];
      const w = braid[s1]?.[s2];
      if (d !== undefined && w !== undefined && w < Infinity) {
        samples.push({ slug1: s1, slug2: s2, delta: d, w });
      }
    }
  }

  console.log(`[conjecture-test] ${samples.length} paired samples`);

  if (samples.length < 10) {
    return {
      error: "Insufficient paired data",
      samples: samples.length,
      min_required: 10
    };
  }

  // Step 3: Compute statistics
  const deltas = samples.map(s => s.delta);
  const ws = samples.map(s => s.w);
  const n = samples.length;

  // Means
  const meanD = deltas.reduce((a, b) => a + b, 0) / n;
  const meanW = ws.reduce((a, b) => a + b, 0) / n;

  // Covariance and variances (for Pearson r and regression)
  let cov = 0, varW = 0, varD = 0;
  for (let i = 0; i < n; i++) {
    const dw = ws[i] - meanW;
    const dd = deltas[i] - meanD;
    cov += dw * dd;
    varW += dw * dw;
    varD += dd * dd;
  }

  // Pearson r
  const pearsonR = varW > 0 && varD > 0 ? cov / Math.sqrt(varW * varD) : 0;
  const rSquared = pearsonR * pearsonR;

  // Linear regression: δ = slope * w + intercept
  const slope = varW > 0 ? cov / varW : 0;
  const intercept = meanD - slope * meanW;

  // Spearman rho (rank correlation)
  const spearmanRho = computeSpearman(deltas, ws);

  // p-value approximation (two-tailed, normal approximation)
  const t = pearsonR * Math.sqrt((n - 2) / (1 - rSquared));
  // Simplified — full t-distribution CDF is heavy; use threshold instead
  const pValueApprox = Math.abs(t) > 2.58 ? "< 0.01" : Math.abs(t) > 1.96 ? "< 0.05" : "> 0.05";

  // Step 4: Conjecture verdict
  let verdict;
  if (rSquared >= 0.7) {
    verdict = "SUPPORTED: Strong conjecture (δ ≈ c·w). R² ≥ 0.7.";
  } else if (Math.abs(spearmanRho) >= 0.5 && rSquared >= 0.3) {
    verdict = "PARTIAL: Weak conjecture (monotonic). Spearman ρ ≥ 0.5 but R² < 0.7.";
  } else if (Math.abs(spearmanRho) >= 0.3) {
    verdict = "WEAK: Marginal monotonicity. Further investigation needed.";
  } else {
    verdict = "REJECTED: No significant relationship between δ and w.";
  }

  return {
    conjecture: "δ(a,b) = c · w(a,b)",
    verdict,
    statistics: {
      samples: n,
      pearson_r: pearsonR.toFixed(4),
      r_squared: rSquared.toFixed(4),
      spearman_rho: spearmanRho.toFixed(4),
      slope: slope.toFixed(6),
      intercept: intercept.toFixed(4),
      p_value: pValueApprox,
      mean_delta: meanD.toFixed(4),
      mean_w: meanW.toFixed(4),
      delta_range: [Math.min(...deltas).toFixed(4), Math.max(...deltas).toFixed(4)],
      w_range: [Math.min(...ws).toFixed(4), Math.max(...ws).toFixed(4)]
    },
    data_sources: {
      dendrogram: ASK_QWAV,
      braid_matrix: BRAID_MATRIX
    },
    timestamp: new Date().toISOString(),
    interpretation: {
      strong_supported: rSquared >= 0.7,
      weak_supported: Math.abs(spearmanRho) >= 0.5,
      note: "If R² ≥ 0.7, ultrametric dendrogram depth is strongly predicted by associative braid distance. This would provide empirical evidence for the Braided Ultrametric Register conjecture."
    }
  };
}

async function getScatterData(env) {
  const [dendroResult, braidResult] = await Promise.all([
    fetchDendrogramDistances(env),
    fetchBraidDistances(env)
  ]);

  const points = [];
  const dendro = dendroResult.distances || {};
  const braid = braidResult.distances || {};
  const slugs = Object.keys(dendro).filter(s => braid[s]);

  for (const s1 of slugs) {
    for (const s2 of slugs) {
      if (s1 >= s2) continue;
      const d = dendro[s1]?.[s2];
      const w = braid[s1]?.[s2];
      if (d !== undefined && w !== undefined && w < Infinity) {
        points.push({ slug1: s1, slug2: s2, delta: d, w });
      }
    }
  }

  return {
    points,
    count: points.length,
    format: "Array of {slug1, slug2, delta (ultrametric), w (braid)}"
  };
}

async function getPaperList(env) {
  const [dendroResult, braidResult] = await Promise.all([
    fetchDendrogramDistances(env),
    fetchBraidDistances(env)
  ]);

  const dendro = dendroResult.distances || {};
  const braid = braidResult.distances || {};
  const allSlugs = [...new Set([...Object.keys(dendro), ...Object.keys(braid)])];

  const papers = allSlugs.map(slug => ({
    slug,
    has_dendro_data: !!dendro[slug],
    has_braid_data: !!braid[slug],
    avg_dendro_distance: dendro[slug] ? averageDistance(dendro[slug]) : null,
    avg_braid_distance: braid[slug] ? averageDistance(braid[slug]) : null
  }));

  return { papers, count: papers.length };
}

async function getPaperDetail(slug, env) {
  const [dendroResult, braidResult] = await Promise.all([
    fetchDendrogramDistances(env),
    fetchBraidDistances(env)
  ]);

  const dendro = dendroResult.distances || {};
  const braid = braidResult.distances || {};

  return {
    slug,
    dendro_distances: dendro[slug] || {},
    braid_distances: braid[slug] || {},
    has_dendro: !!dendro[slug],
    has_braid: !!braid[slug]
  };
}

// ═════════════════════════════════════════════════════════════════════
// Data fetching
// ═════════════════════════════════════════════════════════════════════

async function fetchDendrogramDistances(env) {
  // Try cache first
  const cacheKey = "dendro-distances";
  try {
    const cached = await env.CONJECTURE_CACHE?.get(cacheKey);
    if (cached) return JSON.parse(cached);
  } catch (e) { }

  try {
    // Fetch dendrogram JSON from ask-qwav
    const resp = await fetch(`${ASK_QWAV}/dendrogram-json`, {
      headers: { "User-Agent": "QNFO-ConjectureTest/1.0" }
    });
    if (!resp.ok) throw new Error(`ask-qwav returned ${resp.status}`);
    const tree = await resp.json();

    // Convert dendrogram tree to pairwise distances
    const distances = dendrogramToDistances(tree);
    const result = { distances, source: ASK_QWAV };

    // Cache
    try {
      await env.CONJECTURE_CACHE?.put(cacheKey, JSON.stringify(result), { expirationTtl: CACHE_TTL });
    } catch (e) { }

    return result;
  } catch (e) {
    console.error(`[conjecture-test] Dendrogram fetch failed: ${e.message}`);
    return { distances: {}, source: "error", error: e.message };
  }
}

function dendrogramToDistances(tree) {
  /**
   * Converts a dendrogram tree (from ask-qwav /dendrogram-json) to a pairwise distance matrix.
   * 
   * Expected tree format (from D3 hierarchy):
   * {
   *   name: "root",
   *   children: [
   *     { name: "cluster-1", height: 0.5, children: [...] },
   *     { name: "cluster-2", height: 0.5, children: [...] }
   *   ]
   * }
   * 
   * Distance between two leaves = height of their lowest common ancestor.
   */
  const distances = {};
  const leaves = [];

  // Collect all leaves
  function collectLeaves(node, path = []) {
    if (!node.children || node.children.length === 0) {
      leaves.push({ slug: slugify(node.name), path: [...path], height: node.height || 0 });
      return;
    }
    for (const child of node.children) {
      collectLeaves(child, [...path, child]);
    }
  }
  collectLeaves(tree);

  // Compute distances via LCA height
  for (const leaf1 of leaves) {
    distances[leaf1.slug] = {};
    for (const leaf2 of leaves) {
      if (leaf1.slug === leaf2.slug) {
        distances[leaf1.slug][leaf2.slug] = 0;
        continue;
      }
      // Find LCA: last common ancestor in the path
      let lcaHeight = 0;
      const minLen = Math.min(leaf1.path.length, leaf2.path.length);
      for (let i = 0; i < minLen; i++) {
        if (leaf1.path[i] === leaf2.path[i]) {
          lcaHeight = leaf1.path[i].height || 0;
        } else {
          break;
        }
      }
      distances[leaf1.slug][leaf2.slug] = lcaHeight || 1;
    }
  }

  return distances;
}

async function fetchBraidDistances(env) {
  const cacheKey = "braid-distances";
  try {
    const cached = await env.CONJECTURE_CACHE?.get(cacheKey);
    if (cached) return JSON.parse(cached);
  } catch (e) { }

  try {
    const resp = await fetch(`${BRAID_MATRIX}/matrix`, {
      headers: { "User-Agent": "QNFO-ConjectureTest/1.0" }
    });
    if (!resp.ok) throw new Error(`braid-matrix returned ${resp.status}`);
    const data = await resp.json();
    const result = { distances: data.distances || {}, source: BRAID_MATRIX };

    try {
      await env.CONJECTURE_CACHE?.put(cacheKey, JSON.stringify(result), { expirationTtl: CACHE_TTL });
    } catch (e) { }

    return result;
  } catch (e) {
    console.error(`[conjecture-test] Braid matrix fetch failed: ${e.message}`);
    return { distances: {}, source: "error", error: e.message };
  }
}

// ═════════════════════════════════════════════════════════════════════
// Utilities
// ═════════════════════════════════════════════════════════════════════

function computeSpearman(xs, ys) {
  // Rank the data
  const n = xs.length;
  const rankX = rank(xs);
  const rankY = rank(ys);

  let d2 = 0;
  for (let i = 0; i < n; i++) {
    const diff = rankX[i] - rankY[i];
    d2 += diff * diff;
  }

  return 1 - (6 * d2) / (n * (n * n - 1));
}

function rank(arr) {
  const sorted = arr.map((v, i) => ({ v, i })).sort((a, b) => a.v - b.v);
  const ranks = new Array(arr.length);
  for (let i = 0; i < sorted.length; i++) {
    ranks[sorted[i].i] = i + 1;
  }
  return ranks;
}

function slugify(name) {
  return (name || "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
}

function averageDistance(dists) {
  const values = Object.values(dists).filter(v => v > 0 && v < Infinity);
  if (values.length === 0) return null;
  return values.reduce((a, b) => a + b, 0) / values.length;
}

function conjectureDocs() {
  const html = `<!DOCTYPE html>
<html><head><title>QNFO Conjecture Test Worker</title>
<style>body{font-family:Inter,sans-serif;max-width:800px;margin:2rem auto;padding:0 1rem;color:#1a1a2e}pre{background:#f5f5f5;padding:1rem;border-radius:6px;overflow-x:auto}h2{border-bottom:2px solid #1a56db;padding-bottom:0.25rem}.verdict{font-size:1.5rem;font-weight:bold;padding:1rem;border-radius:8px;margin:1rem 0}.supported{background:#d4edda;color:#155724}.partial{background:#fff3cd;color:#856404}.rejected{background:#f8d7da;color:#721c24}a{color:#1a56db}</style></head>
<body>
<h1>🧪 QNFO Braided Register — Conjecture Test</h1>
<p>Tests the central conjecture: <strong>ultrametric dendrogram depth (δ) ≈ braid word length (w)</strong></p>
<p>Data: <strong>ask-qwav</strong> (ultrametric dendrogram) + <strong>braid-matrix</strong> (associative co-occurrence graph)</p>

<h2>Run Test</h2>
<pre>curl https://conjecture-test.q08.workers.dev/test</pre>
<p><a href="/test">Run now →</a></p>

<h2>Scatter Plot Data</h2>
<pre>curl https://conjecture-test.q08.workers.dev/scatter</pre>
<p><a href="/scatter">View →</a></p>

<h2>Paper List</h2>
<pre>curl https://conjecture-test.q08.workers.dev/papers</pre>

<h2>Paper Detail</h2>
<pre>curl https://conjecture-test.q08.workers.dev/paper/v-punns</pre>

<h2>Interpretation</h2>
<table style="width:100%;border-collapse:collapse">
<tr style="border-bottom:1px solid #ddd"><th style="text-align:left;padding:0.5rem">R²</th><th style="text-align:left;padding:0.5rem">Verdict</th></tr>
<tr style="border-bottom:1px solid #ddd"><td style="padding:0.5rem">≥ 0.7</td><td style="padding:0.5rem">✅ Strong conjecture supported</td></tr>
<tr style="border-bottom:1px solid #ddd"><td style="padding:0.5rem">0.3 – 0.7</td><td style="padding:0.5rem">⚠️ Weak conjecture (check Spearman ρ)</td></tr>
<tr style="border-bottom:1px solid #ddd"><td style="padding:0.5rem">< 0.3</td><td style="padding:0.5rem">❌ Conjecture rejected</td></tr>
</table>

<h2>Data Flow</h2>
<pre>
ask-qwav /dendrogram-json ──► ultrametric distances δ(a,b)
                                    │
                                    ▼
braid-matrix /matrix ─────────► braid distances w(a,b)
                                    │
                                    ▼
                            ┌───────────────┐
                            │  δ(a,b) vs    │
                            │  w(a,b)       │
                            │  R², r, ρ     │
                            └───────────────┘
</pre>
</body></html>`;
  return new Response(html, { headers: { "Content-Type": "text/html; charset=utf-8" } });
}
