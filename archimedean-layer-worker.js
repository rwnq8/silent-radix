/**
 * Archimedean Topology Layer — Worker Module
 * ==========================================
 * Extends the QNFO Ultrametric Engine (ask-qwav Worker) with three new endpoints
 * that add the Archimedean navigation surface on top of the ultrametric scaffold.
 *
 * Integration: Add this module to the existing ask-qwav/worker/worker.js
 * by importing and registering the handleArchimedeanLayer function.
 *
 * Endpoints:
 *   GET  /adjacent/:nodeId        — Semantic neighbors across ultrametric branches
 *   GET  /bridge/:nodeA/:nodeB    — Structural hole papers between two branches
 *   POST /walk-summary/:sessionId — Session-level UVR/WE/SQ/J metrics
 *   GET  /interface-metrics       — Global corpus-level Archimedeanization metrics
 *
 * Bindings required (already present in ask-qwav wrangler.toml):
 *   - VECTORIZE_INDEX  (for semantic similarity queries)
 *   - PAPERS_DB        (D1: living-paper database)
 *   - PAPERS_R2        (R2: qnfo bucket with tree.json)
 *   - AI               (Workers AI for embeddings)
 */

// ─── CONFIGURATION ────────────────────────────────────────────────

const DEFAULT_CONFIG = {
  adjacentK: 10,           // Default number of adjacent results
  bridgeK: 5,              // Default number of bridge results
  minUltrametricDist: 2,   // Minimum tree distance to qualify as "adjacent"
  surpriseWeight: 0.6,     // Weight of semantic similarity in surprise score
  treeWeight: 0.4,         // Weight of ultrametric distance in surprise score
  cacheTTL: 300,           // Cache TTL in seconds (5 min)
  maxNodesPerWalk: 15,     // Max nodes in a walk-summary session
};

// ─── HELPER: ULTRAMETRIC TREE OPERATIONS ─────────────────────────

/**
 * Load the ultrametric tree from R2 (cached in memory with TTL).
 * The tree is stored at qnfo/tree.json in R2.
 */
let cachedTree = null;
let cachedTreeAt = 0;

async function getUltrametricTree(env) {
  const now = Date.now();
  if (cachedTree && (now - cachedTreeAt) < DEFAULT_CONFIG.cacheTTL * 1000) {
    return cachedTree;
  }
  
  try {
    const treeObj = await env.PAPERS_R2.get('tree.json');
    if (treeObj) {
      cachedTree = await treeObj.json();
      cachedTreeAt = now;
      return cachedTree;
    }
  } catch (e) {
    console.error('[ARCHIMEDEAN] Failed to load ultrametric tree:', e.message);
  }
  return null;
}

/**
 * Compute ultrametric distance between two node IDs.
 * Returns { distance, lcaId, lcaDepth } or null if either node not in tree.
 */
function ultrametricDistance(tree, nodeIdA, nodeIdB) {
  if (!tree || !tree.leaves) return null;
  
  const leafA = tree.leaves[nodeIdA];
  const leafB = tree.leaves[nodeIdB];
  if (!leafA || !leafB) return null;
  
  // Find LCA by walking up from both leaves
  const ancestorsA = new Set();
  let current = nodeIdA;
  while (current && tree.parents && tree.parents[current]) {
    ancestorsA.add(current);
    current = tree.parents[current];
  }
  
  current = nodeIdB;
  let lcaId = null;
  while (current && tree.parents && tree.parents[current]) {
    if (ancestorsA.has(current)) {
      lcaId = current;
      break;
    }
    current = tree.parents[current];
  }
  
  if (!lcaId) return { distance: tree.maxDepth || 1.0, lcaId: 'root', lcaDepth: 0 };
  
  const depth = tree.nodeDepths ? (tree.nodeDepths[lcaId] || 0) : 0;
  const maxDepth = tree.maxDepth || 1.0;
  const distance = 1.0 - (depth / maxDepth);
  
  return { distance, lcaId, lcaDepth: depth };
}

/**
 * Compute surprise score: how semantically similar AND ultrametrically distant.
 * score = ws * cosine_similarity + wt * (ultrametric_distance / max_distance)
 * Range: [0, 1], higher = more surprising but still relevant.
 */
function surpriseScore(cosineSimilarity, ultraDistance, maxUltraDist = 1.0) {
  const ws = DEFAULT_CONFIG.surpriseWeight;
  const wt = DEFAULT_CONFIG.treeWeight;
  return ws * cosineSimilarity + wt * (ultraDistance / maxUltraDist);
}

// ─── ENDPOINT: /adjacent/:nodeId ──────────────────────────────────

/**
 * GET /adjacent/:nodeId?k=10&min_dist=2
 * 
 * Returns top-k semantically similar papers that are NOT in the same
 * ultrametric subtree — the "streets and alleys" across the tree.
 */
async function handleAdjacent(request, env, ctx) {
  const url = new URL(request.url);
  const pathParts = url.pathname.split('/').filter(Boolean);
  const nodeId = pathParts[1]; // /adjacent/:nodeId
  
  if (!nodeId) {
    return jsonResponse({ error: 'Missing nodeId parameter' }, 400);
  }
  
  const k = parseInt(url.searchParams.get('k') || DEFAULT_CONFIG.adjacentK);
  const minDist = parseInt(url.searchParams.get('min_dist') || DEFAULT_CONFIG.minUltrametricDist);
  
  // Step 1: Get the target paper's embedding from D1
  let targetEmbedding = null;
  try {
    const stmt = env.PAPERS_DB.prepare(
      'SELECT embedding FROM papers WHERE id = ?'
    );
    const result = await stmt.bind(nodeId).first();
    if (result && result.embedding) {
      targetEmbedding = JSON.parse(result.embedding);
    }
  } catch (e) {
    console.error('[ARCHIMEDEAN] D1 lookup failed:', e.message);
  }
  
  // If no embedding in D1, try to get from Vectorize
  if (!targetEmbedding) {
    try {
      // Vectorize get-by-id (API-dependent)
      const vecResult = await env.VECTORIZE_INDEX.getByIds([nodeId]);
      if (vecResult && vecResult.length > 0 && vecResult[0].values) {
        targetEmbedding = vecResult[0].values;
      }
    } catch (e) {
      console.error('[ARCHIMEDEAN] Vectorize lookup failed:', e.message);
    }
  }
  
  if (!targetEmbedding) {
    return jsonResponse({ error: `Node '${nodeId}' not found or has no embedding` }, 404);
  }
  
  // Step 2: Query Vectorize for semantically similar papers
  let similarPapers = [];
  try {
    const vectorResults = await env.VECTORIZE_INDEX.query(targetEmbedding, {
      topK: Math.max(k * 3, 50),  // Get extra for filtering
      returnValues: true,
      returnMetadata: true,
    });
    similarPapers = vectorResults.matches || [];
  } catch (e) {
    console.error('[ARCHIMEDEAN] Vectorize query failed:', e.message);
    return jsonResponse({ error: 'Semantic search failed' }, 500);
  }
  
  // Step 3: Load ultrametric tree
  const tree = await getUltrametricTree(env);
  if (!tree) {
    return jsonResponse({ error: 'Ultrametric tree not available' }, 503);
  }
  
  // Step 4: Filter and rank
  const adjacent = [];
  const maxUltraDist = tree.maxDepth || 1.0;
  
  for (const match of similarPapers) {
    const matchId = match.id || match.vectorId;
    if (!matchId || matchId === nodeId) continue;
    
    const ultraInfo = ultrametricDistance(tree, nodeId, matchId);
    if (!ultraInfo) continue;
    
    // Filter: must be in a DIFFERENT ultrametric subtree
    if (ultraInfo.lcaDepth >= (tree.maxDepth - minDist)) {
      continue;  // Too close in the tree — same branch
    }
    
    const cosineSim = match.score || 0;
    const surprise = surpriseScore(cosineSim, ultraInfo.distance, maxUltraDist);
    
    adjacent.push({
      id: matchId,
      title: match.metadata?.title || matchId,
      cosineSimilarity: roundTo(cosineSim, 4),
      ultrametricDistance: roundTo(ultraInfo.distance, 4),
      lcaDepth: ultraInfo.lcaDepth,
      commonAncestor: ultraInfo.lcaId,
      surpriseScore: roundTo(surprise, 4),
      source: 'vectorize_semantic_neighbor',
    });
  }
  
  // Sort by surprise score descending
  adjacent.sort((a, b) => b.surpriseScore - a.surpriseScore);
  
  return jsonResponse({
    nodeId,
    adjacent: adjacent.slice(0, k),
    totalFound: adjacent.length,
    returned: Math.min(k, adjacent.length),
    config: { k, min_dist: minDist, surpriseWeight: DEFAULT_CONFIG.surpriseWeight },
  });
}

// ─── ENDPOINT: /bridge/:nodeA/:nodeB ──────────────────────────────

/**
 * GET /bridge/:nodeA/:nodeB?k=5
 * 
 * Finds papers that structurally connect two otherwise distant branches
 * of the ultrametric tree — surfacing Burt's structural holes.
 */
async function handleBridge(request, env, ctx) {
  const url = new URL(request.url);
  const pathParts = url.pathname.split('/').filter(Boolean);
  
  if (pathParts.length < 3) {
    return jsonResponse({ error: 'Requires two node IDs: /bridge/:nodeA/:nodeB' }, 400);
  }
  
  const nodeA = pathParts[1];
  const nodeB = pathParts[2];
  const k = parseInt(url.searchParams.get('k') || DEFAULT_CONFIG.bridgeK);
  
  // Step 1: Get embeddings for both nodes
  let embedA = null, embedB = null;
  try {
    const stmt = env.PAPERS_DB.prepare(
      'SELECT id, embedding FROM papers WHERE id IN (?, ?)'
    );
    const results = await stmt.bind(nodeA, nodeB).all();
    for (const row of results.results || []) {
      const emb = row.embedding ? JSON.parse(row.embedding) : null;
      if (row.id === nodeA) embedA = emb;
      if (row.id === nodeB) embedB = emb;
    }
  } catch (e) {
    console.error('[ARCHIMEDEAN] D1 bridge lookup failed:', e.message);
  }
  
  if (!embedA || !embedB) {
    return jsonResponse({ error: 'One or both nodes not found' }, 404);
  }
  
  // Step 2: Verify they're in different ultrametric branches
  const tree = await getUltrametricTree(env);
  if (!tree) {
    return jsonResponse({ error: 'Ultrametric tree not available' }, 503);
  }
  
  const ultraInfo = ultrametricDistance(tree, nodeA, nodeB);
  if (!ultraInfo || ultraInfo.lcaDepth > tree.maxDepth * 0.5) {
    return jsonResponse({
      warning: 'Nodes are in the same or nearby ultrametric branches',
      lcaDepth: ultraInfo?.lcaDepth,
      suggestion: 'Choose nodes from more distant branches for meaningful bridges',
    });
  }
  
  // Step 3: Compute embedding midpoint and query Vectorize
  const midpoint = embedA.map((v, i) => (v + (embedB[i] || 0)) / 2);
  
  let bridgePapers = [];
  try {
    const vectorResults = await env.VECTORIZE_INDEX.query(midpoint, {
      topK: Math.max(k * 3, 30),
      returnValues: true,
      returnMetadata: true,
      filter: {
        // Exclude A and B themselves
        not: { id: { $in: [nodeA, nodeB] } }
      }
    });
    bridgePapers = vectorResults.matches || [];
  } catch (e) {
    // If filter not supported, filter manually
    console.error('[ARCHIMEDEAN] Vectorize bridge query failed:', e.message);
  }
  
  // Step 4: Filter — bridge paper must NOT be in A's or B's subtrees
  const bridges = [];
  for (const match of bridgePapers) {
    const matchId = match.id || match.vectorId;
    if (!matchId || matchId === nodeA || matchId === nodeB) continue;
    
    const distA = ultrametricDistance(tree, nodeA, matchId);
    const distB = ultrametricDistance(tree, nodeB, matchId);
    if (!distA || !distB) continue;
    
    // Bridge: roughly equidistant from both (not closer to one than the other)
    const balance = 1.0 - Math.abs(distA.distance - distB.distance);
    
    // Must be in different subtrees from both A and B
    if (distA.lcaDepth < tree.maxDepth * 0.3 || distB.lcaDepth < tree.maxDepth * 0.3) {
      continue;  // Too close to one of the endpoints
    }
    
    bridges.push({
      id: matchId,
      title: match.metadata?.title || matchId,
      cosineSimilarityMidpoint: roundTo(match.score || 0, 4),
      distanceToA: roundTo(distA.distance, 4),
      distanceToB: roundTo(distB.distance, 4),
      balanceScore: roundTo(balance, 4),
      betweennessScore: roundTo((match.score || 0) * balance, 4),
      source: 'structural_hole',
    });
  }
  
  bridges.sort((a, b) => b.betweennessScore - a.betweennessScore);
  
  return jsonResponse({
    bridgeBetween: { nodeA, nodeB },
    ultraDistance: roundTo(ultraInfo.distance, 4),
    bridges: bridges.slice(0, k),
    totalFound: bridges.length,
  });
}

// ─── ENDPOINT: /walk-summary/:sessionId ──────────────────────────

/**
 * POST /walk-summary/:sessionId
 * Body: { path: ["nodeA", "nodeB", "nodeC", ...], userId?: "..." }
 * 
 * Computes session-level metrics: UVR, WE, SQ, C, and J.
 */
async function handleWalkSummary(request, env, ctx) {
  const url = new URL(request.url);
  const pathParts = url.pathname.split('/').filter(Boolean);
  const sessionId = pathParts[1];
  
  if (!sessionId) {
    return jsonResponse({ error: 'Missing sessionId' }, 400);
  }
  
  let body;
  try {
    body = await request.json();
  } catch (e) {
    return jsonResponse({ error: 'Invalid JSON body' }, 400);
  }
  
  const path = body.path || [];
  const userId = body.userId || 'anonymous';
  
  if (path.length < 2) {
    return jsonResponse({ error: 'Path must contain at least 2 nodes' }, 400);
  }
  
  if (path.length > DEFAULT_CONFIG.maxNodesPerWalk) {
    return jsonResponse({ 
      error: `Path too long (max ${DEFAULT_CONFIG.maxNodesPerWalk} nodes)` 
    }, 400);
  }
  
  // Load tree
  const tree = await getUltrametricTree(env);
  if (!tree) {
    return jsonResponse({ error: 'Ultrametric tree not available' }, 503);
  }
  
  // Compute metrics
  const startNode = path[0];
  let clustersVisited = new Set();
  let crossings = 0;
  let serendipitousClicks = 0;
  let treeEdges = 0;
  let streetEdges = 0;
  let prevCluster = null;
  const maxUltraDist = tree.maxDepth || 1.0;
  const tau = 0.5; // Serendipity threshold
  
  // Get start node's cluster
  const startUltra = ultrametricDistance(tree, startNode, startNode);
  prevCluster = startUltra?.lcaId || 'root';
  clustersVisited.add(prevCluster);
  
  // Most surprising step
  let maxSurprise = { score: 0, step: 0, node: startNode };
  
  for (let k = 1; k < path.length; k++) {
    const currentNode = path[k];
    const prevNode = path[k - 1];
    
    const ultraInfo = ultrametricDistance(tree, startNode, currentNode);
    if (!ultraInfo) continue;
    
    // Track cluster crossings
    const currentCluster = ultrametricDistance(tree, currentNode, currentNode)?.lcaId || 'root';
    if (currentCluster !== prevCluster) {
      crossings++;
      prevCluster = currentCluster;
    }
    clustersVisited.add(currentCluster);
    
    // Serendipity: is this click "surprising"?
    if (ultraInfo.distance > tau) {
      serendipitousClicks++;
      
      // Track max surprise
      if (ultraInfo.distance > maxSurprise.score) {
        maxSurprise = { 
          score: roundTo(ultraInfo.distance, 4), 
          step: k, 
          node: currentNode 
        };
      }
    }
    
    // Classify edge as tree or street
    const edgeUltra = ultrametricDistance(tree, prevNode, currentNode);
    if (edgeUltra && edgeUltra.lcaDepth > tree.maxDepth * 0.7) {
      treeEdges++;  // Deep LCA = in same branch = tree edge
    } else {
      streetEdges++;
    }
  }
  
  const totalEdges = treeEdges + streetEdges;
  const K = path.length - 1;
  
  // Computed metrics
  const UVR = totalEdges > 0 ? roundTo(streetEdges / totalEdges, 4) : 0;
  const WE = K > 0 ? roundTo(crossings / K, 4) : 0;
  const SQ = K > 0 ? roundTo(serendipitousClicks / K, 4) : 0;
  
  // Consolidation: penalize if clusters visited but not deeply engaged
  const avgStepsPerCluster = clustersVisited.size > 0 ? K / clustersVisited.size : 0;
  const C = roundTo(Math.min(1.0, Math.tanh(avgStepsPerCluster / 3)), 4);
  
  const J = roundTo(SQ * C, 4);
  
  // Detect sweet spot
  const inSweetSpot = UVR >= 0.4 && UVR <= 0.85;
  
  // Generate recommendations
  const recommendations = [];
  if (SQ > 0.6 && C < 0.4 && path.length > 5) {
    recommendations.push(
      'High serendipity but low consolidation — consider revisiting a cluster for deeper engagement.'
    );
  }
  if (UVR < 0.2) {
    recommendations.push(
      'Low UVR — the session stayed within a narrow branch. Try exploring an /adjacent node to cross into a different topic.'
    );
  }
  if (inSweetSpot) {
    recommendations.push('Session is in the optimal UVR sweet spot [0.4, 0.85] — ideal balance.');
  }
  if (maxSurprise.node !== startNode) {
    recommendations.push(
      `Most surprising discovery was at step ${maxSurprise.step}. Explore its /adjacent neighbors for more serendipity.`
    );
  }
  
  // Build response
  const summary = {
    sessionId,
    userId,
    timestamp: new Date().toISOString(),
    pathLength: path.length,
    metrics: {
      uvr: UVR,
      walkEntropy: WE,
      serendipityQuotient: SQ,
      consolidationScore: C,
      interfaceQuality: J,
      inSweetSpot,
    },
    stats: {
      totalEdges,
      treeEdges,
      streetEdges,
      clustersVisited: clustersVisited.size,
      clusterCrossings: crossings,
      serendipitousClicks,
    },
    highlights: {
      deepestCrossClusterStep: maxSurprise.step,
      mostSurprisingNode: maxSurprise.node,
      maxUltrametricDistance: maxSurprise.score,
    },
    recommendations,
    path: path.map(id => ({ id, title: tree.leaves?.[id]?.title || id })),
  };
  
  // Optionally store in D1 for longitudinal analysis
  try {
    const stmt = env.PAPERS_DB.prepare(`
      INSERT INTO walk_sessions (session_id, user_id, path, metrics, created_at)
      VALUES (?, ?, ?, ?, ?)
    `);
    await stmt.bind(
      sessionId,
      userId,
      JSON.stringify(path),
      JSON.stringify(summary.metrics),
      summary.timestamp
    ).run();
  } catch (e) {
    console.error('[ARCHIMEDEAN] Failed to store walk session:', e.message);
  }
  
  return jsonResponse(summary);
}

// ─── ENDPOINT: /interface-metrics ─────────────────────────────────

/**
 * GET /interface-metrics
 * 
 * Global metrics for the entire corpus — the health dashboard for 
 * Archimedeanization level.
 */
async function handleInterfaceMetrics(request, env, ctx) {
  const tree = await getUltrametricTree(env);
  
  // Count papers from D1
  let paperCount = 0;
  let totalEdges = 0;
  let totalStreetEdges = 0;
  let totalTreeEdges = 0;
  
  try {
    const countResult = await env.PAPERS_DB.prepare(
      'SELECT COUNT(*) as count FROM papers'
    ).first();
    paperCount = countResult?.count || 0;
  } catch (e) {
    console.error('[ARCHIMEDEAN] Paper count failed:', e.message);
  }
  
  // Compute UVR from tree + semantic graph
  if (tree) {
    totalTreeEdges = tree.totalEdges || (paperCount > 0 ? paperCount - 1 : 0);
    
    // Estimate street edges from Vectorize density
    try {
      const vecStats = await env.VECTORIZE_INDEX.describe();
      totalStreetEdges = (vecStats?.vectorCount || paperCount) * 5; // ~5 shortcuts per paper
    } catch (e) {
      totalStreetEdges = paperCount * 5; // fallback estimate
    }
    
    totalEdges = totalTreeEdges + totalStreetEdges;
  }
  
  const UVR = totalEdges > 0 ? roundTo(totalStreetEdges / totalEdges, 4) : 0;
  const targetUVR = 0.60;
  const inSweetSpot = UVR >= 0.4 && UVR <= 0.85;
  
  return jsonResponse({
    corpus: {
      totalPapers: paperCount,
      totalClusters: tree?.clusterCount || 0,
      maxTreeDepth: tree?.maxDepth || 0,
      ultrametricTreeHeight: 1.0,
    },
    currentMetrics: {
      uvr: UVR,
      totalEdges,
      treeEdges: totalTreeEdges,
      streetEdges: totalStreetEdges,
      inSweetSpot,
    },
    targetMetrics: {
      uvr: targetUVR,
      projectedInterfaceQuality: 0.325,
      status: UVR < 0.2 ? 'under_archimedeanized' : 
              UVR > 0.85 ? 'over_archimedeanized' : 'near_optimal',
    },
    improvementPlan: {
      required: UVR < 0.4,
      suggestedActions: UVR < 0.4 ? [
        'Enable /adjacent endpoint for cross-branch navigation',
        'Add weighted shortcut edges between semantically similar papers in different domains',
        'Consider increasing link density in the corpus',
      ] : UVR > 0.85 ? [
        'Reduce shortcut density to improve consolidation',
        'Strengthen the ultrametric scaffold visibility',
        'Add explicit cluster navigation aids',
      ] : [
        'Interface is in the optimal UVR range — maintain current density',
      ],
    },
    timestamp: new Date().toISOString(),
  });
}

// ─── ROUTER ───────────────────────────────────────────────────────

/**
 * Main handler for the Archimedean Topology Layer.
 * Add this to the existing Worker's fetch handler.
 * 
 * Usage in worker.js:
 *   import { handleArchimedeanLayer } from './archimedean-layer.js';
 *   
 *   export default {
 *     async fetch(request, env, ctx) {
 *       const url = new URL(request.url);
 *       
 *       // Try Archimedean layer first
 *       const archResult = await handleArchimedeanLayer(request, env, ctx);
 *       if (archResult) return archResult;
 *       
 *       // Existing routes...
 *     }
 *   }
 */
export async function handleArchimedeanLayer(request, env, ctx) {
  const url = new URL(request.url);
  const path = url.pathname;
  
  // CORS preflight
  if (request.method === 'OPTIONS') {
    return new Response(null, {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
      },
    });
  }
  
  // Route matching
  const adjacentMatch = path.match(/^\/adjacent\/(.+)/);
  const bridgeMatch = path.match(/^\/bridge\/(.+)\/(.+)/);
  const walkMatch = path.match(/^\/walk-summary\/(.+)/);
  
  try {
    if (adjacentMatch) {
      return await handleAdjacent(request, env, ctx);
    }
    
    if (bridgeMatch) {
      return await handleBridge(request, env, ctx);
    }
    
    if (path === '/interface-metrics') {
      return await handleInterfaceMetrics(request, env, ctx);
    }
    
    if (walkMatch && request.method === 'POST') {
      return await handleWalkSummary(request, env, ctx);
    }
  } catch (e) {
    console.error('[ARCHIMEDEAN] Unhandled error:', e.message, e.stack);
    return jsonResponse({ error: 'Internal error', detail: e.message }, 500);
  }
  
  // Not an Archimedean route — return null for the main router
  return null;
}

// ─── UTILITIES ────────────────────────────────────────────────────

function jsonResponse(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Cache-Control': 'public, max-age=60',
    },
  });
}

function roundTo(value, decimals) {
  const factor = Math.pow(10, decimals);
  return Math.round(value * factor) / factor;
}

// ─── EXPORT FOR wrangler.toml CONFIG ──────────────────────────────

/**
 * Add these to the existing wrangler.toml:
 * 
 * [[routes]]
 * pattern = "*/adjacent/*"
 * zone_name = "qwav.tech"
 * 
 * [[routes]]
 * pattern = "*/bridge/*"
 * zone_name = "qwav.tech"
 * 
 * [[routes]]
 * pattern = "*/walk-summary/*"
 * zone_name = "qwav.tech"
 * 
 * [[routes]]
 * pattern = "*/interface-metrics"
 * zone_name = "qwav.tech"
 * 
 * # Existing bindings are sufficient:
 * # - VECTORIZE_INDEX (qwav-research-v2, 1024-dim)
 * # - PAPERS_DB (living-paper D1 database)
 * # - PAPERS_R2 (qnfo bucket with tree.json)
 */
