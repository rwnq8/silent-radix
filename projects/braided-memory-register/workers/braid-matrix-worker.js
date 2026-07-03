/**
 * Braid Matrix Worker — QNFO Braided Memory Register
 * 
 * Computes the associative co-occurrence matrix over the QNFO research corpus
 * (119 papers in living-paper D1) and serves braid word-length distances.
 * 
 * Data sources:
 *   - Graph API (graph-api.q08.workers.dev) for paper nodes + REFERENCES edges
 *   - R2 (qnfo bucket) for matrix caching
 * 
 * Endpoints:
 *   GET  /             — API documentation (HTML)
 *   GET  /matrix       — Full co-occurrence matrix (paper-slug → paper-slug → distance)
 *   GET  /pairwise?slug1=X&slug2=Y — Distance between two specific papers
 *   POST /rebuild?key=SECRET — Force matrix rebuild (admin)
 *   GET  /stats        — Matrix statistics (papers, edges, density, max/min distance)
 */

// ═════════════════════════════════════════════════════════════════════
// Configuration
// ═════════════════════════════════════════════════════════════════════

const GRAPH_API = "https://graph-api.q08.workers.dev";
const R2_KEY = "qnfo/braided-register/braid-matrix.json";
const REBUILD_SECRET = "qnfo-braid-rebuild-2026"; // Rotate before production

// ═════════════════════════════════════════════════════════════════════
// Main handler
// ═════════════════════════════════════════════════════════════════════

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;

    // GET / — API docs
    if (path === "/" || path === "") {
      return apiDocs();
    }

    // GET /matrix — full co-occurrence matrix
    if (path === "/matrix" && request.method === "GET") {
      return await serveMatrix(env);
    }

    // GET /pairwise?slug1=X&slug2=Y — pairwise distance
    if (path === "/pairwise" && request.method === "GET") {
      return await servePairwise(url.searchParams, env);
    }

    // POST /rebuild?key=SECRET — force rebuild
    if (path === "/rebuild" && request.method === "POST") {
      return await handleRebuild(url.searchParams, env);
    }

    // GET /stats — matrix statistics
    if (path === "/stats" && request.method === "GET") {
      return await serveStats(env);
    }

    return new Response(JSON.stringify({ error: "Not found", endpoints: ["/", "/matrix", "/pairwise", "/rebuild", "/stats"] }), {
      status: 404,
      headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
    });
  }
};

// ═════════════════════════════════════════════════════════════════════
// API Documentation
// ═════════════════════════════════════════════════════════════════════

function apiDocs() {
  const html = `<!DOCTYPE html>
<html><head><title>QNFO Braid Matrix Worker</title>
<style>body{font-family:Inter,sans-serif;max-width:800px;margin:2rem auto;padding:0 1rem;color:#1a1a2e}pre{background:#f5f5f5;padding:1rem;border-radius:6px;overflow-x:auto}code{font-size:0.9em}h2{border-bottom:2px solid #1a56db;padding-bottom:0.25rem}a{color:#1a56db}</style></head>
<body>
<h1>🧠 QNFO Braid Matrix Worker</h1>
<p>Computes associative co-occurrence (braid word-length proxy) over the QNFO research corpus.</p>

<h2>Endpoints</h2>

<h3>GET /matrix</h3>
<p>Returns the full co-occurrence distance matrix as a JSON object keyed by paper slug.</p>
<pre>curl https://braid-matrix.q08.workers.dev/matrix</pre>

<h3>GET /pairwise?slug1=X&slug2=Y</h3>
<p>Returns the associative distance between two specific papers.</p>
<pre>curl "https://braid-matrix.q08.workers.dev/pairwise?slug1=v-punns&slug2=hierarchical-associative-memory"</pre>
<p>Response: <code>{"slug1":"v-punns","slug2":"hierarchical-associative-memory","distance":3,"path_length":3}</code></p>

<h3>GET /stats</h3>
<p>Returns matrix statistics: paper count, edge count, density, min/max distances.</p>
<pre>curl https://braid-matrix.q08.workers.dev/stats</pre>

<h3>POST /rebuild?key=SECRET</h3>
<p>Forces a complete matrix rebuild from the Graph API. Requires admin key.</p>

<h2>Interpretation</h2>
<p><strong>distance</strong> = shortest-path length in the associative co-occurrence graph.</p>
<p>This is a <em>proxy</em> for braid word length w(a,b) — the number of σᵢ crossings needed to swap memory strands a and b.</p>
<p>In the Braided Ultrametric Register conjecture: <strong>ultrametric dendrogram depth ≈ braid distance</strong>.</p>

<h2>Data Sources</h2>
<ul>
<li>Paper metadata: <a href="${GRAPH_API}">graph-api.q08.workers.dev</a> (D1 qnfo-graph)</li>
<li>Citation edges: Graph API /edges?type=REFERENCES</li>
<li>Matrix cache: R2 qnfo bucket</li>
</ul>
</body></html>`;
  return new Response(html, { headers: { "Content-Type": "text/html; charset=utf-8" } });
}

// ═════════════════════════════════════════════════════════════════════
// Matrix serving (with R2 caching)
// ═════════════════════════════════════════════════════════════════════

async function serveMatrix(env) {
  // Try R2 cache first
  try {
    const cached = await env.BRAID_R2.get(R2_KEY);
    if (cached) {
      const body = await cached.text();
      return new Response(body, {
        headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*", "X-Cache": "HIT" }
      });
    }
  } catch (e) {
    // R2 miss — build fresh
  }

  // Build matrix from Graph API
  const matrix = await buildMatrix();
  return new Response(JSON.stringify(matrix), {
    headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*", "X-Cache": "MISS" }
  });
}

async function servePairwise(params, env) {
  const slug1 = params.get("slug1");
  const slug2 = params.get("slug2");
  if (!slug1 || !slug2) {
    return new Response(JSON.stringify({ error: "Missing slug1 or slug2 parameter" }), {
      status: 400, headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
    });
  }

  // Try cached matrix
  let matrix;
  try {
    const cached = await env.BRAID_R2.get(R2_KEY);
    if (cached) {
      matrix = await cached.json();
    }
  } catch (e) { }

  if (!matrix) {
    matrix = await buildMatrix();
  }

  const dist = matrix.distances?.[slug1]?.[slug2];
  if (dist === undefined) {
    return new Response(JSON.stringify({ error: "One or both paper slugs not found", slug1, slug2 }), {
      status: 404, headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
    });
  }

  return new Response(JSON.stringify({ slug1, slug2, distance: dist, path_length: dist }), {
    headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
  });
}

async function serveStats(env) {
  let matrix;
  try {
    const cached = await env.BRAID_R2.get(R2_KEY);
    if (cached) {
      matrix = await cached.json();
    }
  } catch (e) { }

  if (!matrix) {
    matrix = await buildMatrix();
  }

  const papers = Object.keys(matrix.distances || {});
  const n = papers.length;
  let totalPairs = 0, sumDist = 0, maxDist = 0, minDist = Infinity, reachable = 0;

  for (const s1 of papers) {
    for (const s2 of papers) {
      const d = matrix.distances[s1]?.[s2];
      if (d !== undefined && d > 0) {
        totalPairs++;
        sumDist += d;
        if (d > maxDist) maxDist = d;
        if (d < minDist) minDist = d;
        if (d < Infinity) reachable++;
      }
    }
  }

  const density = n > 1 ? reachable / (n * (n - 1)) : 0;
  const avgDist = totalPairs > 0 ? sumDist / totalPairs : 0;

  return new Response(JSON.stringify({
    paper_count: n,
    total_pairs: totalPairs,
    reachable_pairs: reachable,
    density: density.toFixed(4),
    avg_distance: avgDist.toFixed(2),
    max_distance: maxDist,
    min_distance: minDist,
    papers: papers
  }), {
    headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
  });
}

async function handleRebuild(params, env) {
  const key = params.get("key");
  if (key !== REBUILD_SECRET) {
    return new Response(JSON.stringify({ error: "Invalid rebuild key" }), {
      status: 403, headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
    });
  }

  const matrix = await buildMatrix();
  
  // Cache in R2
  try {
    await env.BRAID_R2.put(R2_KEY, JSON.stringify(matrix));
    return new Response(JSON.stringify({ 
      status: "rebuilt", 
      papers: Object.keys(matrix.distances).length,
      cached: true,
      timestamp: new Date().toISOString()
    }), {
      headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
    });
  } catch (e) {
    return new Response(JSON.stringify({ 
      status: "rebuilt", 
      papers: Object.keys(matrix.distances).length,
      cached: false,
      error: "R2 cache write failed: " + e.message
    }), {
      headers: { "Content-Type": "application/json", "Access-Control-Allow-Origin": "*" }
    });
  }
}

// ═════════════════════════════════════════════════════════════════════
// Matrix construction (core algorithm)
// ═════════════════════════════════════════════════════════════════════

async function buildMatrix() {
  // Step 1: Fetch all paper nodes from Graph API
  const papers = await fetchPapers();
  console.log(`[braid-matrix] Fetched ${papers.length} papers`);

  // Step 2: Fetch all REFERENCES edges from Graph API
  const refEdges = await fetchReferenceEdges();
  console.log(`[braid-matrix] Fetched ${refEdges.length} reference edges`);

  // Step 3: Build co-occurrence graph
  // Two papers are adjacent if:
  //   a) They share a citation edge (paper A references paper B, or vice versa)
  //   b) They share at least one author
  //   c) They share domain tags (from KG taxonomy)

  const adj = {}; // paperSlug -> Set of neighbor slugs
  for (const p of papers) {
    adj[p.slug] = new Set();
  }

  // Citation edges
  for (const edge of refEdges) {
    const src = slugify(edge.source_name || edge.source_id);
    const tgt = slugify(edge.target_name || edge.target_id);
    if (adj[src] && adj[tgt]) {
      adj[src].add(tgt);
      adj[tgt].add(src);
    }
  }

  // Co-authorship edges
  for (let i = 0; i < papers.length; i++) {
    for (let j = i + 1; j < papers.length; j++) {
      const authorsI = new Set((papers[i].authors || []).map(a => a.toLowerCase().trim()));
      const authorsJ = new Set((papers[j].authors || []).map(a => a.toLowerCase().trim()));
      const shared = [...authorsI].filter(a => authorsJ.has(a));
      if (shared.length > 0) {
        adj[papers[i].slug].add(papers[j].slug);
        adj[papers[j].slug].add(papers[i].slug);
      }
    }
  }

  // Shared domain edges (papers in same KG domain/program)
  for (let i = 0; i < papers.length; i++) {
    for (let j = i + 1; j < papers.length; j++) {
      if (papers[i].domain && papers[i].domain === papers[j].domain) {
        adj[papers[i].slug].add(papers[j].slug);
        adj[papers[j].slug].add(papers[i].slug);
      }
    }
  }

  console.log(`[braid-matrix] Built adjacency graph`);

  // Step 4: Compute all-pairs shortest path (Floyd-Warshall or BFS from each node)
  const slugs = papers.map(p => p.slug);
  const n = slugs.length;
  const distances = {};

  // BFS from each node (sparse graph — more efficient than Floyd-Warshall)
  for (const slug of slugs) {
    distances[slug] = {};
    distances[slug][slug] = 0;

    const visited = new Set([slug]);
    const queue = [slug];

    while (queue.length > 0) {
      const current = queue.shift();
      const currentDist = distances[slug][current];

      for (const neighbor of (adj[current] || [])) {
        if (!visited.has(neighbor)) {
          visited.add(neighbor);
          distances[slug][neighbor] = currentDist + 1;
          queue.push(neighbor);
        }
      }
    }
  }

  console.log(`[braid-matrix] Computed all-pairs distances`);

  return {
    papers: slugs,
    paper_count: n,
    adjacency: Object.fromEntries(
      Object.entries(adj).map(([k, v]) => [k, [...v]])
    ),
    distances,
    metadata: {
      built_at: new Date().toISOString(),
      source: "graph-api.q08.workers.dev",
      edge_types: ["citation", "co-authorship", "shared-domain"]
    }
  };
}

// ═════════════════════════════════════════════════════════════════════
// Data fetching helpers
// ═════════════════════════════════════════════════════════════════════

async function fetchPapers() {
  try {
    const resp = await fetch(`${GRAPH_API}/nodes?label=Paper`, {
      headers: { "User-Agent": "QNFO-BraidMatrix/1.0" }
    });
    if (!resp.ok) throw new Error(`Graph API returned ${resp.status}`);
    const data = await resp.json();
    const nodes = data.nodes || [];

    return nodes.map(n => ({
      slug: slugify(n.name || n.id),
      name: n.name || n.id,
      authors: (n.properties?.authors || "").split(",").map(a => a.trim()).filter(Boolean),
      domain: n.properties?.domain || n.properties?.program || null,
      year: n.properties?.year || n.properties?.published || null
    }));
  } catch (e) {
    console.error(`[braid-matrix] Failed to fetch papers: ${e.message}`);
    return [];
  }
}

async function fetchReferenceEdges() {
  try {
    const resp = await fetch(`${GRAPH_API}/edges?type=REFERENCES`, {
      headers: { "User-Agent": "QNFO-BraidMatrix/1.0" }
    });
    if (!resp.ok) throw new Error(`Graph API returned ${resp.status}`);
    const data = await resp.json();
    return data.edges || data || [];
  } catch (e) {
    console.error(`[braid-matrix] Failed to fetch REFERENCE edges: ${e.message}`);
    return [];
  }
}

function slugify(name) {
  return (name || "").toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
}

// ═════════════════════════════════════════════════════════════════════
// OPTIONAL: Cron trigger for periodic rebuild
// ═════════════════════════════════════════════════════════════════════

export const scheduled = {
  async scheduled(event, env, ctx) {
    // Rebuild matrix daily at midnight
    const matrix = await buildMatrix();
    try {
      await env.BRAID_R2.put(R2_KEY, JSON.stringify(matrix));
      console.log(`[braid-matrix-cron] Rebuilt: ${Object.keys(matrix.distances).length} papers`);
    } catch (e) {
      console.error(`[braid-matrix-cron] R2 write failed: ${e.message}`);
    }
  }
};
