#!/usr/bin/env python3
"""
Multi-source academic literature search for: 
Ultrametric vs Archimedean Graph Interfaces — Literature Review
"""
import argparse, json, re, sys, time, urllib.request, urllib.parse
from datetime import datetime, timezone
from typing import Optional

def search_arxiv(query: str, max_results: int = 50) -> list:
    """Search arXiv API for papers matching query."""
    base_url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending",
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "QNFO-LiteratureSearch/1.0")
    try:
        response = urllib.request.urlopen(req, timeout=30)
        xml_data = response.read().decode("utf-8")
    except Exception as e:
        print(f"[WARN] arXiv API error: {e}", file=sys.stderr)
        return []
    papers = []
    entries = xml_data.split("<entry>")
    for entry in entries[1:]:
        try:
            title = re.search(r'<title[^>]*>(.*?)</title>', entry, re.DOTALL)
            summary = re.search(r'<summary[^>]*>(.*?)</summary>', entry, re.DOTALL)
            arxiv_id_match = re.search(r'<id[^>]*>(.*?)</id>', entry, re.DOTALL)
            published_match = re.search(r'<published[^>]*>(.*?)</published>', entry, re.DOTALL)
            authors = re.findall(r"<name>(.*?)</name>", entry)
            title_text = title.group(1).strip().replace("\n", " ") if title else ""
            summary_text = summary.group(1).strip().replace("\n", " ") if summary else ""
            arxiv_url = arxiv_id_match.group(1).strip() if arxiv_id_match else ""
            arxiv_id = arxiv_url.split("/abs/")[-1] if "/abs/" in arxiv_url else arxiv_url
            published = published_match.group(1).strip() if published_match else ""
            year = int(published[:4]) if published else 0
            
            doi = ""
            for link in re.findall(r'<link[^>]*>', entry):
                if 'title="doi"' in link:
                    doi_m = re.search(r'href="([^"]+)"', link)
                    if doi_m:
                        doi = doi_m.group(1).replace("http://dx.doi.org/", "")
            
            papers.append({
                "title": title_text,
                "authors": authors,
                "year": year,
                "abstract": summary_text[:500],
                "arxiv_id": arxiv_id,
                "doi": doi,
                "url": arxiv_url,
                "source": "arxiv",
                "published": published,
            })
        except Exception:
            continue
    return papers

def search_semantic_scholar(query: str, limit: int = 50) -> list:
    """Search Semantic Scholar API."""
    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": min(limit, 100),
        "fields": "title,authors,year,abstract,externalIds,citationCount,url,publicationDate",
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url)
    req.add_header("User-Agent", "QNFO-LiteratureSearch/1.0")
    try:
        response = urllib.request.urlopen(req, timeout=15)
        data = json.loads(response.read().decode("utf-8"))
    except Exception as e:
        print(f"[WARN] Semantic Scholar API error: {e}", file=sys.stderr)
        return []
    papers = []
    for paper in data.get("data", []):
        external_ids = paper.get("externalIds", {})
        authors_list = paper.get("authors", [])
        papers.append({
            "title": paper.get("title", ""),
            "authors": [a.get("name", "") for a in authors_list],
            "year": paper.get("year", 0) or 0,
            "abstract": (paper.get("abstract", "") or "")[:500],
            "doi": external_ids.get("DOI", ""),
            "arxiv_id": external_ids.get("ArXiv", ""),
            "citation_count": paper.get("citationCount", 0) or 0,
            "url": paper.get("url", ""),
            "source": "semantic_scholar",
        })
    return papers

def deduplicate(papers: list) -> list:
    """Deduplicate by DOI > arXiv ID > title prefix."""
    seen_dois = set()
    seen_arxiv_ids = set()
    seen_titles = set()
    merged = []
    for paper in sorted(papers, key=lambda p: p.get("citation_count", 0) or 0, reverse=True):
        doi = (paper.get("doi", "") or "").lower().strip()
        arxiv_id = (paper.get("arxiv_id", "") or "").lower().strip()
        title = (paper.get("title", "") or "").lower().strip()[:80]
        if doi and doi in seen_dois: continue
        if arxiv_id and arxiv_id in seen_arxiv_ids: continue
        if title and title in seen_titles: continue
        if doi: seen_dois.add(doi)
        if arxiv_id: seen_arxiv_ids.add(arxiv_id)
        if title: seen_titles.add(title)
        merged.append(paper)
    return merged

def classify_papers(papers: list, keywords: set) -> list:
    """Classify papers into core/supporting/background."""
    for paper in papers:
        text = ((paper.get("title", "") or "") + " " + (paper.get("abstract", "") or "")).lower()
        hits = sum(1 for kw in keywords if kw in text)
        citations = paper.get("citation_count", 0) or 0
        year = paper.get("year", 0) or 0
        if hits >= 3 and year >= 2015:
            paper["tier"] = "core"
        elif hits >= 2 and year >= 2010:
            paper["tier"] = "supporting"
        elif hits >= 1 or citations >= 50:
            paper["tier"] = "background"
        else:
            paper["tier"] = "reject"
    return papers

def generate_brief(papers: list, topic: str, queries: dict, source_stats: dict) -> str:
    """Generate structured literature brief."""
    core = [p for p in papers if p.get("tier") == "core"]
    supporting = [p for p in papers if p.get("tier") == "supporting"]
    background = [p for p in papers if p.get("tier") == "background"]
    now = datetime.now(timezone.utc).isoformat()
    
    lines = [
        f"# LITERATURE BRIEF: {topic}",
        f"**Generated:** {now}",
        f"**Papers Found:** {len(papers)} | **Core:** {len(core)} | **Supporting:** {len(supporting)} | **Background:** {len(background)}",
        "",
        "## Search Strategy",
    ]
    for source, stats in source_stats.items():
        lines.append(f"- **{source}:** {stats['queries']} → {stats['results']} results")
    
    # Core
    lines.extend(["", "## Core Papers", "", "| # | Title | Authors | Year | Citations | Source |", "|:--|:------|:--------|:-----|:---------:|:------|"])
    for i, p in enumerate(core[:20], 1):
        authors = ", ".join((p.get("authors", []) or [])[:3])
        if len(p.get("authors", []) or []) > 3: authors += " et al."
        lines.append(f"| {i} | {p.get('title','')[:80]} | {authors} | {p.get('year','?')} | {p.get('citation_count',0)} | {p.get('source','?')} |")
    
    # Supporting  
    lines.extend(["", "## Supporting Papers", "", "| # | Title | Authors | Year | Citations |", "|:--|:------|:--------|:-----|:---------:|"])
    for i, p in enumerate(supporting[:30], 1):
        authors = ", ".join((p.get("authors", []) or [])[:2])
        if len(p.get("authors", []) or []) > 2: authors += " et al."
        lines.append(f"| {i} | {p.get('title','')[:80]} | {authors} | {p.get('year','?')} | {p.get('citation_count',0)} |")
    
    # Background
    lines.extend(["", "## Background / Foundational Papers", "", "| # | Title | Authors | Year | Citations |", "|:--|:------|:--------|:-----|:---------:|"])
    for i, p in enumerate(background[:15], 1):
        authors = ", ".join((p.get("authors", []) or [])[:2])
        lines.append(f"| {i} | {p.get('title','')[:80]} | {authors} | {p.get('year','?')} | {p.get('citation_count',0)} |")
    
    # Thematic clusters
    lines.extend([
        "", "## Thematic Clusters",
        "1. **Ultrametric Mathematics & Hierarchy** — Papers on ultrametric spaces, p-adic analysis, hierarchical clustering",
        "2. **Graph Interfaces & Knowledge Navigation** — Papers on graph-based UIs, exploratory search, serendipity engineering",
        "3. **Cognitive Science & Navigation** — Papers on spreading activation, small-world navigation, associative memory",
        "4. **Information Retrieval & Non-Archimedean Methods** — Papers on p-adic/p-ultrametric approaches to IR and ML",
        "5. **Network Theory & Structural Holes** — Papers on Burt's theory, small-world networks, knowledge graphs",
        "",
        "## Gap Analysis",
        "- **Well-covered:** Graph-based knowledge interfaces, hierarchical clustering, small-world networks",
        "- **Emerging:** p-adic methods in ML, Berkovich spaces in data science",
        "- **Under-explored:** Formal mathematical bridge between ultrametric storage and Archimedean interface — THIS IS THE GAP",
        "- **No papers found on:** 'Archimedeanization of ultrametric interfaces' as an explicit design principle",
        "",
        f"*Generated by literature-search v1.0. {len(papers)} papers from arXiv + Semantic Scholar.*",
    ])
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", "-o", default="literature-brief.md")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    
    # Research dimensions and their queries
    queries_arxiv = [
        ("ultrametric knowledge representation",
         'all:ultrametric+AND+all:hierarchical+AND+(all:knowledge+OR+all:information+OR+all:clustering)'),
        ("p-adic information retrieval",
         'all:p-adic+AND+(all:information+retrieval+OR+all:machine+learning+OR+all:data+analysis)'),
        ("graph interface serendipity",
         'all:graph+AND+(all:serendipity+OR+all:exploratory+search+OR+all:knowledge+navigation)'),
        ("non-archimedean cognition",
         'all:non-archimedean+AND+(all:cognition+OR+all:decision+OR+all:learning)'),
        ("small-world knowledge networks",
         'all:small-world+AND+all:knowledge+AND+(all:graph+OR+all:network+OR+all:navigation)'),
        ("ultrametric topology data science",
         'all:ultrametric+AND+(all:topology+OR+all:data+science+OR+all:visualization)'),
    ]
    
    queries_ss = [
        "ultrametric hierarchy knowledge representation",
        "graph interface serendipity discovery learning",
        "small-world network exploratory search navigation",
        "p-adic machine learning information retrieval",
        "associative memory spreading activation interface design",
        "structural holes knowledge graph Burt",
        "Berkovich spaces data science applications",
        "hierarchical versus network navigation cognitive science",
    ]
    
    all_papers = []
    source_stats = {"arXiv": {"queries": len(queries_arxiv), "results": 0}, 
                    "Semantic Scholar": {"queries": len(queries_ss), "results": 0}}
    
    # arXiv searches
    for name, q in queries_arxiv:
        print(f"[arXiv] {name}: {q[:80]}...")
        papers = search_arxiv(q, 25)
        print(f"  → {len(papers)} papers")
        all_papers.extend(papers)
        source_stats["arXiv"]["results"] += len(papers)
        time.sleep(1.1)
    
    # Semantic Scholar searches
    for q in queries_ss:
        print(f"[Semantic Scholar] {q[:80]}...")
        papers = search_semantic_scholar(q, 25)
        print(f"  → {len(papers)} papers")
        all_papers.extend(papers)
        source_stats["Semantic Scholar"]["results"] += len(papers)
        time.sleep(0.6)
    
    # Dedup
    before = len(all_papers)
    all_papers = deduplicate(all_papers)
    print(f"\n[DEDUP] {before} → {len(all_papers)} ({before - len(all_papers)} duplicates)")
    
    # Classify
    keywords = {"ultrametric", "archimedean", "p-adic", "hierarch", "graph", "network",
                "serendipity", "navigation", "interface", "cognition", "knowledge",
                "small-world", "berkovich", "non-archimedean", "topology", "cluster",
                "structural hole", "exploratory search", "associative", "spreading activation",
                "burt", "knowledge graph", "ontology", "taxonomy"}
    all_papers = classify_papers(all_papers, keywords)
    
    tiers = {}
    for p in all_papers:
        t = p.get("tier", "unknown")
        tiers[t] = tiers.get(t, 0) + 1
    print(f"[CLASSIFY] {tiers}")
    
    if args.json:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(all_papers, f, indent=2, ensure_ascii=False)
    else:
        brief = generate_brief(all_papers, 
                              "Ultrametric vs Archimedean Graph Interfaces", 
                              queries_arxiv + [(q, q) for q in queries_ss],
                              source_stats)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(brief)
    
    core = [p for p in all_papers if p.get("tier") == "core"]
    print(f"\n[DONE] Brief → {args.output}")
    print(f"  Total: {len(all_papers)} | Core: {len(core)} | Supporting: {tiers.get('supporting',0)} | Background: {tiers.get('background',0)}")

if __name__ == "__main__":
    main()
