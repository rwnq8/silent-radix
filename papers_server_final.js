var __defProp = Object.defineProperty;
var __name = (target, value) => __defProp(target, "name", { value, configurable: true });

// papers-server-v3.mjs
var BLUE = {
  primary: "#1a56db",
  dark: "#1040a8",
  light: "#dbeafe",
  subtle: "#eff6ff",
  mid: "#6094e8"
};
function slugify(t) {
  if (!t) return "untitled";
  let s = t.toLowerCase().replace(/[^a-z0-9\s-]/g, "").replace(/\s+/g, "-").replace(/-+/g, "-").substring(0, 60);
  while (s.endsWith("-")) s = s.substring(0, s.length - 1);
  return s || "untitled";
}
__name(slugify, "slugify");
function esc(s) {
  return String(s || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}
__name(esc, "esc");
function escAttr(s) {
  return String(s || "").replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/'/g, "&#39;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}
__name(escAttr, "escAttr");
var CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, OPTIONS"
};
function htmlHeaders(extra) {
  return { "Content-Type": "text/html; charset=utf-8", ...extra };
}
__name(htmlHeaders, "htmlHeaders");
var CSS = (
  /*css*/
  `
:root {
  --blue: ${BLUE.primary};
  --blue-dark: ${BLUE.dark};
  --blue-light: ${BLUE.light};
  --blue-subtle: ${BLUE.subtle};
  --blue-mid: ${BLUE.mid};
  --text: #1a1a2e;
  --text-muted: #6b7280;
  --bg: #ffffff;
  --border: #e5e7eb;
  --card-bg: #f9fafb;
  --max-w: 960px;
  --radius: 8px;
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { -webkit-text-size-adjust: 100%; scroll-behavior: smooth; }
body {
  font-family: "Source Serif 4", "Charter", "Georgia", "Times New Roman", serif;
  font-size: 17px;
  line-height: 1.7;
  color: var(--text);
  background: var(--bg);
  -webkit-font-smoothing: antialiased;
}
h1, h2, h3, h4 { font-family: "Inter", system-ui, -apple-system, sans-serif; font-weight: 600; }
h1 { font-size: 2rem; letter-spacing: -0.02em; line-height: 1.25; }
h2 { font-size: 1.35rem; margin: 2rem 0 0.75rem; color: var(--blue-dark); }
h3 { font-size: 1.1rem; margin: 1.5rem 0 0.5rem; }
a { color: var(--blue); text-decoration: none; }
a:hover { text-decoration: underline; color: var(--blue-dark); }

/* \u2500\u2500 Nav \u2500\u2500 */
.topbar {
  position: sticky; top: 0; z-index: 100;
  background: rgba(255,255,255,0.92);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
}
.nav {
  max-width: var(--max-w); margin: 0 auto;
  display: flex; align-items: center; gap: 1.5rem;
  padding: 0.75rem 1.5rem;
  font-family: "Inter", system-ui, sans-serif; font-size: 0.875rem;
}
.nav a { color: var(--text-muted); font-weight: 500; transition: color 0.15s; }
.nav a:hover { color: var(--blue); text-decoration: none; }
.nav .brand { font-weight: 700; color: var(--text); font-size: 1rem; letter-spacing: -0.01em; margin-right: auto; }
.nav .brand span { color: var(--blue); }

/* \u2500\u2500 Content \u2500\u2500 */
.content { max-width: var(--max-w); margin: 0 auto; padding: 2rem 1.5rem 4rem; }

/* \u2500\u2500 Index: Hero \u2500\u2500 */
.hero { text-align: center; padding: 3rem 0 1.5rem; }
.hero h1 { font-size: 2.5rem; margin-bottom: 0.5rem; }
.hero h1 span { color: var(--blue); }
.hero p { color: var(--text-muted); font-size: 1.05rem; max-width: 560px; margin: 0 auto; }

/* \u2500\u2500 Search \u2500\u2500 */
.search-wrap { max-width: 640px; margin: 0 auto 2rem; position: relative; }
.search-wrap input {
  width: 100%; padding: 0.85rem 1rem 0.85rem 2.75rem;
  font-size: 1rem; font-family: inherit;
  border: 2px solid var(--border); border-radius: var(--radius);
  background: var(--card-bg); transition: border-color 0.2s, box-shadow 0.2s;
}
.search-wrap input:focus {
  outline: none; border-color: var(--blue);
  box-shadow: 0 0 0 3px ${BLUE.light};
}
.search-wrap svg {
  position: absolute; left: 0.9rem; top: 50%; transform: translateY(-50%);
  width: 20px; height: 20px; color: var(--text-muted);
}

/* \u2500\u2500 Stats bar \u2500\u2500 */
.stats-bar {
  display: flex; align-items: center; justify-content: space-between;
  flex-wrap: wrap; gap: 0.5rem;
  margin-bottom: 1.25rem;
  font-size: 0.85rem; color: var(--text-muted);
  font-family: "Inter", system-ui, sans-serif;
}

/* \u2500\u2500 Filter pills \u2500\u2500 */
.filter-pills { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-bottom: 1.25rem; }
.filter-pills button {
  padding: 0.3rem 0.75rem; border: 1px solid var(--border);
  border-radius: 20px; background: var(--card-bg);
  font-size: 0.8rem; cursor: pointer; font-family: "Inter", system-ui, sans-serif;
  color: var(--text-muted); transition: all 0.15s;
}
.filter-pills button:hover { border-color: var(--blue-mid); color: var(--blue); }
.filter-pills button.active { background: var(--blue); border-color: var(--blue); color: #fff; }

/* \u2500\u2500 Card \u2500\u2500 */
.paper-card {
  border: 1px solid var(--border); border-radius: var(--radius);
  padding: 1.25rem 1.5rem; margin-bottom: 0.75rem;
  background: #fff; transition: box-shadow 0.15s, border-color 0.15s;
}
.paper-card:hover {
  box-shadow: 0 2px 12px rgba(0,0,0,0.06);
  border-color: var(--blue-mid);
}
.paper-card h3 { margin: 0 0 0.35rem; font-size: 1.1rem; }
.paper-card h3 a { color: var(--text); }
.paper-card h3 a:hover { color: var(--blue); text-decoration: none; }
.paper-card .meta-line {
  font-size: 0.82rem; color: var(--text-muted);
  margin-bottom: 0.5rem; font-family: "Inter", system-ui, sans-serif;
  display: flex; flex-wrap: wrap; align-items: center; gap: 0.5rem;
}
.paper-card .abstract-preview {
  font-size: 0.9rem; color: #4b5563; line-height: 1.55;
  display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical;
  overflow: hidden;
}

/* \u2500\u2500 Badges \u2500\u2500 */
.badge {
  display: inline-flex; align-items: center; gap: 0.25rem;
  padding: 0.15rem 0.55rem; border-radius: 4px;
  font-size: 0.72rem; font-weight: 600; font-family: "Inter", system-ui, sans-serif;
  letter-spacing: 0.01em;
}
.badge-doi    { background: ${BLUE.subtle}; color: ${BLUE.primary}; border: 1px solid ${BLUE.light}; }
.badge-type   { background: #f3e8ff; color: #7c3aed; border: 1px solid #e9d5ff; }
.badge-cat    { background: #ecfdf5; color: #065f46; border: 1px solid #d1fae5; }
.badge-tag    { background: var(--card-bg); color: var(--text-muted); border: 1px solid var(--border); }
.badge-license { background: #fff7ed; color: #c2410c; border: 1px solid #fed7aa; }

/* \u2500\u2500 Paper Detail \u2500\u2500 */
.paper-header { margin-bottom: 2rem; }
.paper-header h1 { margin-bottom: 0.5rem; }
.paper-header .subtitle { font-size: 1.15rem; color: var(--text-muted); margin-bottom: 0.75rem; font-style: italic; }
.paper-header .authors { font-size: 1.05rem; color: #374151; margin-bottom: 0.75rem; }
.paper-header .meta-row {
  display: flex; flex-wrap: wrap; gap: 0.5rem; align-items: center;
  margin-bottom: 0.5rem; font-family: "Inter", system-ui, sans-serif;
}
.paper-body { line-height: 1.75; }
.paper-body h1 { font-size: 1.5rem; }
.paper-body h2 { font-size: 1.25rem; }
.paper-body p { margin-bottom: 1rem; }
.paper-body pre { background: var(--card-bg); padding: 14px 18px; border-radius: 6px; overflow-x: auto; font-size: 0.88rem; line-height: 1.5; }
.paper-body code { font-family: "JetBrains Mono", "Fira Code", monospace; font-size: 0.88em; }
.paper-body blockquote {
  border-left: 3px solid var(--blue-mid); padding: 0.5rem 1rem;
  margin: 1rem 0; color: #4b5563; background: var(--blue-subtle);
  border-radius: 0 6px 6px 0;
}
.paper-body img { max-width: 100%; border-radius: 6px; }
.paper-body table { border-collapse: collapse; width: 100%; margin: 1rem 0; overflow-x: auto; display: block; }
.paper-body th, .paper-body td { padding: 8px 12px; border-bottom: 1px solid var(--border); text-align: left; }
.paper-body th { font-weight: 600; }

/* \u2500\u2500 AI Query Box \u2500\u2500 */
.ai-query {
  margin: 2.5rem 0; padding: 1.5rem;
  border: 2px solid ${BLUE.light}; border-radius: var(--radius);
  background: linear-gradient(135deg, ${BLUE.subtle} 0%, #fff 100%);
}
.ai-query h3 {
  font-family: "Inter", system-ui, sans-serif; font-size: 1rem;
  font-weight: 600; color: var(--blue-dark); margin: 0 0 0.5rem;
  display: flex; align-items: center; gap: 0.4rem;
}
.ai-query h3 svg { width: 18px; height: 18px; }
.ai-query .ai-row {
  display: flex; gap: 0.5rem; align-items: stretch;
}
.ai-query input {
  flex: 1; padding: 0.7rem 0.9rem;
  border: 1px solid var(--border); border-radius: 6px;
  font-size: 0.95rem; font-family: inherit; background: #fff;
  transition: border-color 0.2s;
}
.ai-query input:focus { outline: none; border-color: var(--blue); box-shadow: 0 0 0 2px ${BLUE.light}; }
.ai-query button {
  padding: 0.7rem 1.25rem; border: none; border-radius: 6px;
  background: var(--blue); color: #fff; font-size: 0.9rem;
  font-weight: 600; cursor: pointer; font-family: "Inter", system-ui, sans-serif;
  transition: background 0.15s; white-space: nowrap;
}
.ai-query button:hover { background: var(--blue-dark); }
.ai-query .ai-hint {
  font-size: 0.78rem; color: var(--text-muted); margin-top: 0.5rem;
  font-family: "Inter", system-ui, sans-serif;
}

/* \u2500\u2500 Related Papers \u2500\u2500 */
.related-section { margin: 2.5rem 0; }
.related-section h2 { margin-bottom: 1rem; }
.related-card {
  border: 1px solid var(--border); border-radius: 6px;
  padding: 0.9rem 1.1rem; margin-bottom: 0.5rem;
  transition: border-color 0.15s;
}
.related-card:hover { border-color: var(--blue-mid); }
.related-card h4 { font-size: 0.95rem; margin: 0 0 0.25rem; font-weight: 500; }
.related-card h4 a { color: var(--text); }
.related-card h4 a:hover { color: var(--blue); text-decoration: none; }
.related-card .related-meta {
  font-size: 0.78rem; color: var(--text-muted);
  font-family: "Inter", system-ui, sans-serif;
}

/* \u2500\u2500 Empty state \u2500\u2500 */
.empty { text-align: center; padding: 3rem; color: var(--text-muted); }
.empty svg { width: 48px; height: 48px; margin-bottom: 1rem; color: var(--border); }

/* \u2500\u2500 Footer \u2500\u2500 */
.footer {
  max-width: var(--max-w); margin: 0 auto;
  padding: 1.5rem; text-align: center;
  font-size: 0.82rem; color: var(--text-muted);
  border-top: 1px solid var(--border);
  font-family: "Inter", system-ui, sans-serif;
}
.footer a { color: var(--text-muted); }

/* \u2500\u2500 404 \u2500\u2500 */
.notfound { text-align: center; padding: 4rem 0; }
.notfound h1 { font-size: 5rem; color: var(--border); margin: 0; font-weight: 700; }
.notfound p { color: var(--text-muted); margin: 0.5rem 0 1.5rem; }
.notfound a { display: inline-block; padding: 0.6rem 1.5rem; background: var(--blue); color: #fff; border-radius: 6px; font-weight: 600; }
.notfound a:hover { background: var(--blue-dark); text-decoration: none; }

/* \u2500\u2500 Responsive \u2500\u2500 */
@media (max-width: 768px) {
  .hero h1 { font-size: 1.8rem; }
  .ai-query .ai-row { flex-direction: column; }
  .nav { gap: 1rem; padding: 0.6rem 1rem; }
  .content { padding: 1.25rem 1rem 3rem; }
  .paper-card { padding: 1rem 1.1rem; }
}
@media (max-width: 480px) {
  body { font-size: 15px; }
  h1 { font-size: 1.5rem; }
  .topbar .nav a:not(.brand) { display: none; }
}

/* \u2500\u2500 MathJax \u2500\u2500 */
mjx-container[display="true"] { text-align: left !important; margin: 1em 0; overflow-x: auto; }
`
);
var ICONS = {
  search: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="m21 21-5.197-5.197m0 0A7.5 7.5 0 1 0 5.196 5.196a7.5 7.5 0 0 0 10.607 10.607Z"/></svg>',
  sparkles: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.455 2.456L21.75 6l-1.036.259a3.375 3.375 0 0 0-2.455 2.456Z"/></svg>',
  doi: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" style="width:12px;height:12px"><path stroke-linecap="round" stroke-linejoin="round" d="M13.19 8.688a4.5 4.5 0 0 1 1.242 7.244l-4.5 4.5a4.5 4.5 0 0 1-6.364-6.364l1.757-1.757m13.35-.622 1.757-1.757a4.5 4.5 0 0 0-6.364-6.364l-4.5 4.5a4.5 4.5 0 0 0 1.242 7.244"/></svg>',
  empty: '<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 0 18 18a8.967 8.967 0 0 0-6 2.292m0-14.25v14.25"/></svg>'
};
var NAV = `<div class="topbar"><nav class="nav">
  <a href="/" class="brand">QWAV <span>Research</span> Papers</a>
  <a href="/">Index</a>
  <a href="/archive">Archive</a>
  <a href="https://qnfo.org">QNFO Hub</a>
  <a href="https://ask.qwav.tech">AI Query</a>
</nav></div>`;
var FOOTER = `<div class="footer">
  QNFO &middot; <a href="https://qnfo.org">qnfo.org</a> &middot;
  <a href="https://legal.qnfo.org">License</a> &middot;
  <a href="https://ask.qwav.tech">Ask QWAV AI</a>
  <br>Rendered dynamically from D1 (living-paper database) + R2 object storage.
</div>`;
function shell(title, body, extraHead = "") {
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>${esc(title)}</title>
<meta name="description" content="QWAV Research Papers \u2014 QNFO research catalog, dynamically rendered from D1 + R2">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&display=swap" rel="stylesheet">
<script>window.MathJax={tex:{inlineMath:[["$","$"],["\\\\(","\\\\)"]],displayMath:[["$$","$$"],["\\\\[","\\\\]"]]}};<\/script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"><\/script>
<style>${CSS}</style>
${extraHead}
</head>
<body>
${NAV}
${body}
${FOOTER}
</body>
</html>`;
}
__name(shell, "shell");
async function getAllPapers(env) {
  try {
    const { results } = await env.DB.prepare(
      `SELECT identifier, id, slug, title, authors, doi, abstract, published,
              paper_type, categories, keywords, journal, language, license,
              subtitle, version, zenodo_doi, ipfs_cid, kg_node_id,
              "references", paper_refs
       FROM papers ORDER BY title`
    ).all();
    return (results || []).map((p) => ({
      slug: p.slug || slugify(p.title || ""),
      id: p.id || "",
      identifier: p.identifier || "",
      title: p.title || "Untitled",
      abstract: p.abstract || "",
      authors: p.authors || "",
      doi: p.doi || "",
      zenodo_doi: p.zenodo_doi || "",
      published: p.published || "",
      paper_type: p.paper_type || "",
      categories: p.categories || "",
      keywords: p.keywords || "",
      journal: p.journal || "",
      language: p.language || "",
      license: p.license || "",
      subtitle: p.subtitle || "",
      version: p.version || "",
      ipfs_cid: p.ipfs_cid || "",
      kg_node_id: p.kg_node_id || "",
      references: p.references || "",
      paper_refs: p.paper_refs || ""
    }));
  } catch (e) {
    try {
      let all = [];
      for (let off = 0; off < 300; off += 100) {
        const r = await fetch(`https://ask-qwav.q08.workers.dev/api/papers?limit=100&offset=${off}`);
        const d = await r.json();
        if (d.success && d.data?.length) all = all.concat(d.data);
        if (!d.data || d.data.length < 100) break;
      }
      return all.map((p) => ({
        slug: p.slug || slugify(p.title || ""),
        id: p.id || "",
        identifier: p.id || p.doi || slugify(p.title || "") || "",
        title: p.title || "Untitled",
        abstract: p.abstract || "",
        authors: p.authors || "",
        doi: p.doi || "",
        zenodo_doi: "",
        published: "",
        paper_type: "",
        categories: "",
        keywords: "",
        journal: "",
        language: "",
        license: "",
        subtitle: "",
        version: "",
        ipfs_cid: "",
        kg_node_id: "",
        references: "",
        paper_refs: ""
      }));
    } catch (e2) {
      return [];
    }
  }
}
__name(getAllPapers, "getAllPapers");
function parseAuthors(raw) {
  if (!raw) return ["QNFO Research Collective"];
  try {
    const arr = JSON.parse(raw);
    if (Array.isArray(arr) && arr.length > 0) return arr;
  } catch (e) {
  }
  return raw.split(",").map((s) => s.trim()).filter(Boolean);
}
__name(parseAuthors, "parseAuthors");
function formatAuthors(raw) {
  const authors = parseAuthors(raw);
  return authors.map((a) => esc(a)).join(", ");
}
__name(formatAuthors, "formatAuthors");
function parseCategories(raw) {
  if (!raw) return [];
  try {
    const arr = JSON.parse(raw);
    if (Array.isArray(arr) && arr.length > 0) return arr.filter(Boolean);
  } catch (e) {
    return raw.split(",").map((s) => s.trim()).filter(Boolean).filter((c) => c !== "[]" && c !== '""');
  }
  if (typeof raw === "string" && raw.startsWith("[")) {
    try {
      return JSON.parse(raw).filter(Boolean);
    } catch (e) {
    }
  }
  return raw.split(",").map((s) => s.trim()).filter(Boolean);
}
__name(parseCategories, "parseCategories");
function indexPage(allPapers) {
  const paperJson = JSON.stringify(allPapers);
  const cats = /* @__PURE__ */ new Set();
  allPapers.forEach((p) => {
    parseCategories(p.categories).forEach((c) => cats.add(c));
  });
  const catList = [...cats].sort().slice(0, 12);
  const body = `
<div class="content">
  <div class="hero">
    <h1><span>QWAV</span> Research Papers</h1>
    <p>Complete research catalog &mdash; <strong>${allPapers.length} papers</strong>. Dynamically rendered from D1 living-paper database + R2 markdown.</p>
  </div>
  <div class="search-wrap">
    ${ICONS.search}
    <input id="searchInput" placeholder="Search by title, author, abstract, or keyword..." oninput="filterAndRender()" autofocus>
  </div>
  <div class="filter-pills" id="filterPills">${catList.map((c) => `<button onclick="setCategoryFilter('${escAttr(c)}', this)">${esc(c)}</button>`).join("")}</div>
  <div class="stats-bar"><span id="stats">Showing ${allPapers.length} of ${allPapers.length} papers</span></div>
  <div id="paperList"></div>
</div>
<script>
var PAPERS = ${paperJson};
var activeCategory = null;

function setCategoryFilter(cat, btn) {
  if (activeCategory === cat) { activeCategory = null; } else { activeCategory = cat; }
  document.querySelectorAll('#filterPills button').forEach(b => b.classList.remove('active'));
  if (activeCategory) btn.classList.add('active');
  filterAndRender();
}

function filterAndRender() {
  var q = (document.getElementById('searchInput').value || '').toLowerCase().trim();
  var filtered = PAPERS.filter(function(p) {
    var matchSearch = !q || p.title.toLowerCase().includes(q) || (p.authors||'').toLowerCase().includes(q) || (p.abstract||'').toLowerCase().includes(q) || (p.keywords||'').toLowerCase().includes(q) || (p.categories||'').toLowerCase().includes(q);
    var matchCat = !activeCategory || (p.categories||'').includes(activeCategory);
    return matchSearch && matchCat;
  });
  document.getElementById('stats').textContent = 'Showing ' + filtered.length + ' of ' + PAPERS.length + ' papers';
  renderList(filtered);
}

function renderList(papers) {
  var el = document.getElementById('paperList');
  if (!papers.length) {
    el.innerHTML = '<div class="empty">' + '${ICONS.empty}' + '<p>No papers match your search.</p></div>';
    return;
  }
  el.innerHTML = papers.map(function(p) {
    var abs = (p.abstract || '').substring(0, 280);
    if (p.abstract && p.abstract.length > 280) abs += '&hellip;';
    var typeBadge = p.paper_type ? '<span class="badge badge-type">' + escHtml(p.paper_type) + '</span>' : '';
    var doiBadge = p.doi ? '<span class="badge badge-doi">${ICONS.doi} ' + escHtml(p.doi.substring(0,30)) + '</span>' : '';
    var authorStr = p.authors;
    try { var a = JSON.parse(p.authors); if (Array.isArray(a)) authorStr = a.join(', '); } catch(e) {}
    var catsArr = parseCat(p.categories);
    var catTags = catsArr.slice(0,3).map(function(c){return '<span class="badge badge-cat">'+escHtml(c)+'</span>';}).join(' ');
    return '<div class="paper-card">' +
      '<h3><a href="/papers/' + p.slug + '/">' + escHtml(p.title) + '</a></h3>' +
      '<div class="meta-line">' + escHtml(authorStr) + (p.published ? ' &middot; ' + escHtml(p.published.substring(0,10)) : '') + '</div>' +
      '<div class="meta-line">' + typeBadge + ' ' + doiBadge + ' ' + catTags + '</div>' +
      '<div class="abstract-preview">' + escHtml(abs) + '</div>' +
    '</div>';
  }).join('');
}

function escHtml(s) { return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;'); }
function parseCat(raw) {
  if (!raw) return [];
  try { var a=JSON.parse(raw); if (Array.isArray(a)) return a.filter(Boolean); } catch(e){}
  return raw.split(',').map(function(s){return s.trim();}).filter(Boolean).filter(function(c){return c!=='[]' && c!=='""'});
}

filterAndRender();
<\/script>`;
  const siteHead = `<meta property="og:title" content="QWAV Research Papers"><meta property="og:description" content="QNFO research catalog \u2014 ${allPapers.length} papers dynamically rendered from D1 + R2"><meta property="og:image" content="https://papers.qnfo.org/og-image.png"><meta property="og:url" content="https://papers.qnfo.org/"><meta property="og:type" content="website"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="QWAV Research Papers"><meta name="twitter:description" content="QNFO research catalog \u2014 ${allPapers.length} papers"><link rel="canonical" href="https://papers.qnfo.org/"><script type="application/ld+json">{"@context":"https://schema.org","@type":"WebSite","name":"QWAV Research Papers","url":"https://papers.qnfo.org","description":"QNFO research catalog","publisher":{"@type":"Organization","name":"QNFO","url":"https://qnfo.org"}}<\/script>`;
  return shell("QWAV Research Papers", body, siteHead);
}
__name(indexPage, "indexPage");
async function paperDetailPage(slug, allPapers, env) {
  const paper = allPapers.find((p) => p.slug === slug || p.id === slug || p.identifier === slug);
  if (!paper) return null;
  const authors = formatAuthors(paper.authors);
  const categories = parseCategories(paper.categories);
  const keywords = parseCategories(paper.keywords);
  const hasDoi = !!(paper.doi || paper.zenodo_doi);
  const effectiveDoi = paper.doi || paper.zenodo_doi || "";
  let doiBadgeHtml = "";
  if (effectiveDoi) {
    doiBadgeHtml = `<a href="https://doi.org/${escAttr(effectiveDoi)}" target="_blank" rel="noopener" class="badge badge-doi" title="View on doi.org">${ICONS.doi} DOI: ${esc(effectiveDoi.substring(0, 40))}${effectiveDoi.length > 40 ? "\u2026" : ""}</a>`;
  }
  let typeBadgeHtml = "";
  if (paper.paper_type) {
    typeBadgeHtml = `<span class="badge badge-type">${esc(paper.paper_type)}</span>`;
  }
  let catBadgesHtml = categories.slice(0, 6).map((c) => `<span class="badge badge-cat">${esc(c)}</span>`).join(" ");
  let kwBadgesHtml = keywords.slice(0, 8).map((k) => `<span class="badge badge-tag">${esc(k)}</span>`).join(" ");
  let licenseBadgeHtml = "";
  if (paper.license) {
    licenseBadgeHtml = `<span class="badge badge-license">${esc(paper.license)}</span>`;
  }
  const metaItems = [];
  if (paper.published) metaItems.push(`<span title="Published">\u{1F4C5} ${esc(paper.published.substring(0, 10))}</span>`);
  if (paper.version) metaItems.push(`<span title="Version">v${esc(paper.version)}</span>`);
  if (paper.language) metaItems.push(`<span title="Language">\u{1F310} ${esc(paper.language)}</span>`);
  const metaRow = metaItems.length ? `<div class="meta-row" style="color:var(--text-muted);font-size:0.82rem;gap:1rem;margin-bottom:0.75rem;">${metaItems.join(" ")}</div>` : "";
  let bodyHtml = "";
  const r2Paths = [
    `qnfo/publications/${slug}/paper.md`,
    `qnfo/releases/${slug}/paper.md`
  ];
  if (paper.identifier) {
    r2Paths.push(`qnfo/publications/${paper.identifier}/paper.md`);
  }
  try {
    for (const r2path of r2Paths) {
      const obj = await env.PAPERS_BUCKET.get(r2path);
      if (obj) {
        const md = await obj.text();
        bodyHtml = `<div class="paper-body">${simpleMarkdown(md)}</div>`;
        break;
      }
    }
  } catch (e) {
  }
  if (!bodyHtml) {
    bodyHtml = `
<div style="background:${BLUE.subtle};border:1px solid ${BLUE.light};border-radius:var(--radius);padding:1.25rem 1.5rem;margin-bottom:2rem;font-size:0.9rem;color:var(--text-muted);">
  <strong>Metadata-only mode</strong> &mdash; Full markdown content is not yet available on R2.
</div>
<div style="border-top:1px solid var(--border);padding-top:1.5rem;">
  <h2>Abstract</h2>
  <p style="color:#4b5563;line-height:1.65;">${esc(paper.abstract || "No abstract available.")}</p>
</div>`;
  }
  const aiQueryHtml = `
<div class="ai-query">
  <h3>${ICONS.sparkles} Ask AI about this paper</h3>
  <div class="ai-row">
    <input id="aiQueryInput" type="text" placeholder="e.g., Summarize the key findings of this paper..." onkeydown="if(event.key==='Enter')askAI()">
    <button onclick="askAI()">Ask AI</button>
  </div>
  <div class="ai-hint">Queries are processed by the QWAV AI research assistant. <a href="https://ask.qwav.tech">Open full AI interface \u2192</a></div>
</div>
<script>
function askAI() {
  var q = document.getElementById('aiQueryInput').value.trim();
  if (!q) { document.getElementById('aiQueryInput').focus(); return; }
  var query = encodeURIComponent('Regarding the paper "' + ${JSON.stringify(paper.title)} + '": ' + q);
  window.open('https://ask.qwav.tech/?q=' + query, '_blank');
}
<\/script>`;
  const relatedSet = new Set(categories.concat(keywords).filter(Boolean));
  let related = [];
  if (relatedSet.size > 0) {
    related = allPapers.filter((p) => p.id !== paper.id && p.slug !== paper.slug && p.identifier !== paper.identifier).map((p) => {
      const pCats = parseCategories(p.categories);
      const pKws = parseCategories(p.keywords);
      const pSet = new Set(pCats.concat(pKws));
      const overlap = [...relatedSet].filter((t) => pSet.has(t)).length;
      return { paper: p, overlap };
    }).filter((r) => r.overlap > 0).sort((a, b) => b.overlap - a.overlap).slice(0, 6);
  }
  if (related.length === 0) {
    related = allPapers.filter((p) => p.id !== paper.id && p.slug !== paper.slug && p.identifier !== paper.identifier).slice(0, 5).map((p) => ({ paper: p, overlap: 0 }));
  }
  let relatedHtml = "";
  if (related.length > 0) {
    relatedHtml = `
<div class="related-section">
  <h2>Related Papers</h2>
  ${related.map((r) => `
    <div class="related-card">
      <h4><a href="/papers/${escAttr(r.paper.slug)}/">${esc(r.paper.title)}</a></h4>
      <div class="related-meta">${formatAuthors(r.paper.authors)}${r.overlap > 0 ? ` &middot; ${r.overlap} matching topic${r.overlap > 1 ? "s" : ""}` : ""}</div>
    </div>
  `).join("")}
</div>`;
  }
  let refsHtml = "";
  if (paper.references) {
    try {
      const refs = JSON.parse(paper.references);
      if (Array.isArray(refs) && refs.length > 0) {
        refsHtml = `
<div style="margin-top:2.5rem;padding-top:1.5rem;border-top:1px solid var(--border);">
  <h2>References</h2>
  <ol style="font-size:0.9rem;">${refs.slice(0, 20).map((r) => `<li>${esc(typeof r === "string" ? r : r.title || r.citation || JSON.stringify(r))}</li>`).join("")}</ol>
  ${refs.length > 20 ? `<p style="color:var(--text-muted);font-size:0.85rem;">\u2026and ${refs.length - 20} more references.</p>` : ""}
</div>`;
      }
    } catch (e) {
    }
  }
  const body = `
<div class="content">
  <div class="paper-header">
    <h1>${esc(paper.title)}</h1>
    ${paper.subtitle ? `<div class="subtitle">${esc(paper.subtitle)}</div>` : ""}
    <div class="authors">${authors}</div>
    ${metaRow}
    <div class="meta-row">
      ${typeBadgeHtml}
      ${doiBadgeHtml}
      ${licenseBadgeHtml}
    </div>
    ${catBadgesHtml ? `<div class="meta-row">${catBadgesHtml}</div>` : ""}
    ${kwBadgesHtml ? `<div style="display:flex;flex-wrap:wrap;gap:0.35rem;margin-top:0.5rem;">${kwBadgesHtml}</div>` : ""}
  </div>
  ${bodyHtml}
  ${aiQueryHtml}
  ${relatedHtml}
  ${refsHtml}
</div>`;
  return shell(`${paper.title} \u2014 QWAV`, body);
}
__name(paperDetailPage, "paperDetailPage");
function simpleMarkdown(md) {
  let html = esc(md);
  html = html.replace(/```(\w*)\n([\s\S]*?)```/g, (_, lang, code) => {
    return `<pre><code class="language-${lang}">${code.replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">")}</code></pre>`;
  });
  html = html.replace(/`([^`]+)`/g, "<code>$1</code>");
  html = html.replace(/^#### (.+)$/gm, "<h4>$1</h4>");
  html = html.replace(/^### (.+)$/gm, "<h3>$1</h3>");
  html = html.replace(/^## (.+)$/gm, "<h2>$1</h2>");
  html = html.replace(/^# (.+)$/gm, "<h1>$1</h1>");
  html = html.replace(/\*\*\*(.+?)\*\*\*/g, "<strong><em>$1</em></strong>");
  html = html.replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  html = html.replace(/\*(.+?)\*/g, "<em>$1</em>");
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener">$1</a>');
  html = html.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img src="$2" alt="$1" loading="lazy">');
  html = html.replace(/^&gt; (.+)$/gm, "<blockquote>$1</blockquote>");
  html = html.replace(/^---$/gm, "<hr>");
  html = html.replace(/^[-*] (.+)$/gm, "<li>$1</li>");
  html = html.replace(/^\d+\. (.+)$/gm, "<li>$1</li>");
  const blocks = html.split(/\n\n+/);
  html = blocks.map((block) => {
    block = block.trim();
    if (!block) return "";
    if (block.startsWith("<h") || block.startsWith("<pre") || block.startsWith("<blockquote") || block.startsWith("<hr") || block.startsWith("<ul") || block.startsWith("<ol") || block.startsWith("<li") || block.startsWith("<table")) {
      return block;
    }
    const lis = block.match(/<li>/g);
    if (lis && block.indexOf("<li>") === 0) {
      return "<ul>" + block + "</ul>";
    }
    return "<p>" + block.replace(/\n/g, "<br>") + "</p>";
  }).join("\n");
  return html;
}
__name(simpleMarkdown, "simpleMarkdown");
function archivePage() {
  const body = `
<div class="content" style="text-align:center;padding-top:3rem;">
  <h1 style="margin-bottom:0.5rem;">Research Archive</h1>
  <p style="color:var(--text-muted);">Historical papers, deprecated versions, and reference materials.</p>
  <p style="margin-top:2rem;">
    <a href="/" style="display:inline-block;padding:0.6rem 1.5rem;background:var(--blue);color:#fff;border-radius:6px;font-weight:600;">&larr; Browse Active Papers</a>
  </p>
</div>`;
  return shell("Archive \u2014 QWAV", body);
}
__name(archivePage, "archivePage");
function notFoundPage(path) {
  const body = `
<div class="content notfound">
  <h1>404</h1>
  <p><code>${esc(path)}</code> not found on this server.</p>
  <a href="/">&larr; Back to Papers Index</a>
</div>`;
  return shell("404 \u2014 Not Found", body);
}
__name(notFoundPage, "notFoundPage");
var papers_server_v3_default = {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname.replace(/\/+$/, "");
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: CORS });
    }
    try {
      if (path === "" || path === "/") {
        const papers = await getAllPapers(env);
        return new Response(indexPage(papers), { headers: htmlHeaders(CORS) });
      }
      const paperMatch = path.match(/^\/papers\/([a-zA-Z0-9_-]+)\/?$/);
      if (paperMatch) {
        const slug = paperMatch[1];
        const papers = await getAllPapers(env);
        const html = await paperDetailPage(slug, papers, env);
        if (!html) return new Response(notFoundPage(path), { status: 404, headers: htmlHeaders(CORS) });
        return new Response(html, { headers: htmlHeaders(CORS) });
      }
      if (path === "/archive") {
        return new Response(archivePage(), { headers: htmlHeaders(CORS) });
      }
      if (path === "/api/papers") {
        const papers = await getAllPapers(env);
        return new Response(JSON.stringify(papers), {
          headers: { ...CORS, "Content-Type": "application/json" }
        });
      }
      const seoFiles = ['/robots.txt', '/sitemap.xml', '/llms.txt', '/llms-full.txt', '/ai.txt'];
      if (seoFiles.includes(path)) {
        try {
          const seoResp = await fetch(`https://qnfo-publications.pages.dev${path}`);
          if (seoResp.ok) {
            const ct = path.endsWith('.xml') ? 'application/xml' : 'text/plain';
            return new Response(await seoResp.text(), {
              headers: { ...CORS, 'Content-Type': ct, 'Cache-Control': 'public, max-age=3600' }
            });
          }
        } catch (_) {}
      }
      return new Response(notFoundPage(path), { status: 404, headers: htmlHeaders(CORS) });
    } catch (err) {
      return new Response(
        shell("Error", `<div class="content"><h1>500 \u2014 Internal Error</h1><p>${esc(err.message)}</p><p><a href="/">&larr; Back to Index</a></p></div>`),
        { status: 500, headers: htmlHeaders(CORS) }
      );
    }
  }
};
export {
  papers_server_v3_default as default
};
//# sourceMappingURL=papers-server-v3.js.map
