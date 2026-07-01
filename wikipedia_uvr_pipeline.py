#!/usr/bin/env python3
"""
Wikipedia UVR Measurement Pipeline
===================================
Computes the Ultrametric Violation Ratio (UVR), Walk-Entropy (WE), and 
Serendipity Quotient (SQ) for Wikipedia by parsing its public SQL dumps.

Dependencies: None beyond Python 3.8+ standard library (sqlite3, gzip, re).
              Wikipedia dumps must be downloaded separately (~10 GB total).

Dump files needed:
  - enwiki-YYYYMMDD-page.sql.gz       (~2 GB)    -- all page metadata
  - enwiki-YYYYMMDD-categorylinks.sql.gz  (~2 GB) -- category assignments
  - enwiki-YYYYMMDD-pagelinks.sql.gz      (~8 GB) -- wikilinks between pages
  - enwiki-YYYYMMDD-category.sql.gz       (~200 MB) -- category pages

Download from: https://dumps.wikimedia.org/enwiki/YYYYMMDD/

Usage:
  python wikipedia_uvr.py --dump-dir ./enwiki-20250101/ --sample 50000 --output uvr_results.json

The script works incrementally:
  1. Parse categorylinks → build ultrametric tree
  2. Parse pagelinks → build link graph
  3. Compute UVR per article on a sample
  4. Simulate random walks for WE and SQ
  5. Output JSON + report
"""

import argparse
import gzip
import json
import os
import random
import re
import sqlite3
import sys
import time
from collections import defaultdict, Counter
from pathlib import Path

# ─── SQL DUMP PARSER ──────────────────────────────────────────────

class WikipediaSQLDumpParser:
    """Parses Wikipedia SQL dump files (INSERT INTO ... VALUES ... format)."""
    
    INSERT_RE = re.compile(
        r"INSERT\s+INTO\s+`(\w+)`\s*\([^)]*\)\s*VALUES\s*(.+?);", 
        re.IGNORECASE | re.DOTALL
    )
    VALUE_RE = re.compile(r"\(([^()]*(?:\([^()]*\)[^()]*)*)\)")
    
    def __init__(self, dump_dir: str):
        self.dump_dir = Path(dump_dir)
    
    def parse_page(self, page_file: str = None) -> dict[int, dict]:
        """
        Parse page.sql to get page_id → {title, namespace, is_redirect}.
        Only main namespace (ns=0) and category namespace (ns=14) are needed.
        Returns id → {title, namespace, is_redirect}.
        """
        if page_file is None:
            page_file = next(self.dump_dir.glob("*page*.sql*"), None)
            if page_file is None:
                raise FileNotFoundError("No page dump found")
        
        pages = {}
        print(f"[PARSE] Reading page dump: {page_file}")
        
        opener = gzip.open if str(page_file).endswith('.gz') else open
        buffer = ""
        
        with opener(page_file, 'rt', encoding='utf-8', errors='replace') as f:
            for line in f:
                buffer += line
                if 'INSERT INTO' in line:
                    # Try to extract values
                    match = self.INSERT_RE.search(buffer)
                    if match:
                        table, values_block = match.group(1), match.group(2)
                        buffer = ""
                        if table == 'page':
                            for val_match in self.VALUE_RE.finditer(values_block):
                                vals = self._split_values(val_match.group(1))
                                if len(vals) >= 4:
                                    try:
                                        pid = int(vals[0])
                                        ns = int(vals[1])
                                        title = vals[2].strip("'")
                                        is_redirect = int(vals[4]) if len(vals) > 4 else 0
                                        if ns in (0, 14):  # main or category
                                            pages[pid] = {
                                                'title': title,
                                                'namespace': ns,
                                                'is_redirect': is_redirect
                                            }
                                    except (ValueError, IndexError):
                                        continue
        print(f"  → {len(pages)} pages (ns=0 or 14)")
        return pages
    
    def parse_categorylinks(self, pages: dict, catlinks_file: str = None) -> dict[int, list[str]]:
        """
        Parse categorylinks.sql to get page_id → [category titles].
        Only for main namespace pages (ns=0).
        Returns article_id → [category_name, ...]
        """
        if catlinks_file is None:
            catlinks_file = next(self.dump_dir.glob("*categorylinks*.sql*"), None)
            if catlinks_file is None:
                raise FileNotFoundError("No categorylinks dump found")
        
        catlinks = defaultdict(list)
        print(f"[PARSE] Reading categorylinks dump: {catlinks_file}")
        
        opener = gzip.open if str(catlinks_file).endswith('.gz') else open
        buffer = ""
        count = 0
        
        with opener(catlinks_file, 'rt', encoding='utf-8', errors='replace') as f:
            for line in f:
                buffer += line
                match = self.INSERT_RE.search(buffer)
                if match:
                    values_block = match.group(2)
                    buffer = ""
                    for val_match in self.VALUE_RE.finditer(values_block):
                        vals = self._split_values(val_match.group(1))
                        if len(vals) >= 3:
                            try:
                                cl_from = int(vals[0])
                                cl_to = vals[1].strip("'").replace('_', ' ')
                                # Only include if page is in main namespace
                                if cl_from in pages and pages[cl_from]['namespace'] == 0:
                                    catlinks[cl_from].append(cl_to)
                                    count += 1
                            except (ValueError, IndexError):
                                continue
        
        print(f"  → {len(catlinks)} articles with categories, {count} total assignments")
        return catlinks
    
    def parse_pagelinks(self, pages: dict, pagelinks_file: str = None) -> dict[int, list[int]]:
        """
        Parse pagelinks.sql to get page_id → [target_page_ids].
        Only for main namespace → main namespace links.
        Returns source_article_id → [target_article_id, ...]
        """
        if pagelinks_file is None:
            pagelinks_file = next(self.dump_dir.glob("*pagelinks*.sql*"), None)
            if pagelinks_file is None:
                raise FileNotFoundError("No pagelinks dump found")
        
        # Build title → id lookup for efficient resolution
        title_to_id = {}
        for pid, pdata in pages.items():
            if pdata['namespace'] == 0:
                title_to_id[pdata['title'].replace(' ', '_')] = pid
        
        pagelinks = defaultdict(list)
        print(f"[PARSE] Reading pagelinks dump: {pagelinks_file}")
        
        opener = gzip.open if str(pagelinks_file).endswith('.gz') else open
        buffer = ""
        resolved, unresolved = 0, 0
        
        with opener(pagelinks_file, 'rt', encoding='utf-8', errors='replace') as f:
            for line in f:
                buffer += line
                match = self.INSERT_RE.search(buffer)
                if match:
                    values_block = match.group(2)
                    buffer = ""
                    for val_match in self.VALUE_RE.finditer(values_block):
                        vals = self._split_values(val_match.group(1))
                        if len(vals) >= 3:
                            try:
                                pl_from = int(vals[0])
                                pl_title = vals[2].strip("'").replace('_', ' ')
                                # Resolve title to id
                                target_id = title_to_id.get(pl_title.replace(' ', '_'))
                                if target_id and pl_from in pages and pages[pl_from]['namespace'] == 0:
                                    pagelinks[pl_from].append(target_id)
                                    resolved += 1
                                else:
                                    unresolved += 1
                            except (ValueError, IndexError):
                                continue
        
        print(f"  → {len(pagelinks)} articles with links, {resolved:,} resolved, {unresolved:,} unresolved")
        return pagelinks
    
    def _split_values(self, values_str: str) -> list[str]:
        """Split comma-separated SQL values, respecting quoted strings and parentheses."""
        result = []
        current = ""
        depth = 0
        in_string = False
        for char in values_str:
            if char == "'" and not in_string:
                in_string = True
                current += char
            elif char == "'" and in_string:
                in_string = False
                current += char
            elif char == '(' and not in_string:
                depth += 1
                current += char
            elif char == ')' and not in_string:
                depth -= 1
                current += char
            elif char == ',' and depth == 0 and not in_string:
                result.append(current.strip())
                current = ""
            else:
                current += char
        if current.strip():
            result.append(current.strip())
        return result


# ─── ULTRAMETRIC TREE BUILDER ─────────────────────────────────────

class UltrametricTreeBuilder:
    """Builds the ultrametric category tree from categorylinks data."""
    
    def __init__(self, pages: dict, catlinks: dict[int, list[str]]):
        self.pages = pages
        self.catlinks = catlinks
        self.cat_to_parent = {}  # category name → parent category name
        self.cat_to_depth = {}   # category name → depth from root
        self.article_to_cats = catlinks  # article_id → [category names]
    
    def build_category_tree(self, category_file: str = None):
        """
        Reconstruct the category hierarchy.
        Wikipedia's category table has cat_id, cat_title, cat_pages, cat_subcats, cat_files.
        The hierarchy is encoded in categorylinks where the target is a category page.
        
        Simplified approach: treat each category as a node; use Wikipedia's 
        top-level categories as roots, and assign parent based on lexical overlap.
        
        For production use, a proper transitive closure of the category DAG is needed.
        """
        # Build article → deepest category mapping using heuristic depth
        print("[TREE] Building category tree...")
        
        # Count category frequencies to identify broad vs narrow categories
        cat_freq = Counter()
        for cats in self.catlinks.values():
            for c in cats:
                cat_freq[c] += 1
        
        # Assign depth: broader (more articles) = shallower
        max_freq = max(cat_freq.values()) if cat_freq else 1
        for cat, freq in cat_freq.items():
            # Normalized depth: rarer categories are deeper
            self.cat_to_depth[cat] = 1.0 - (freq / max_freq)
        
        print(f"  → {len(cat_freq)} unique categories, max articles: {max_freq}")
        return cat_freq
    
    def get_article_depth(self, article_id: int) -> float:
        """Get the depth of an article's deepest category."""
        cats = self.article_to_cats.get(article_id, [])
        if not cats:
            return 1.0  # Uncategorized = deepest (most specific)
        return max(self.cat_to_depth.get(c, 0.5) for c in cats)
    
    def ultrametric_distance(self, a_id: int, b_id: int) -> float:
        """
        Approximate ultrametric distance between two articles.
        Uses Jaccard distance on category sets: 1 - |A ∩ B| / |A ∪ B|.
        For a true ultrametric, single-linkage clustering on the full 
        corpus would be needed. The Jaccard distance is an approximation.
        """
        cats_a = set(self.article_to_cats.get(a_id, []))
        cats_b = set(self.article_to_cats.get(b_id, []))
        
        if not cats_a or not cats_b:
            return 1.0  # Maximum distance if either has no categories
        
        intersection = cats_a & cats_b
        union = cats_a | cats_b
        
        if not union:
            return 1.0
        
        return 1.0 - len(intersection) / len(union)


# ─── UVR COMPUTATION ENGINE ───────────────────────────────────────

class UVREngine:
    """Computes UVR, Walk-Entropy, and Serendipity Quotient."""
    
    def __init__(self, pages: dict, pagelinks: dict[int, list[int]], 
                 tree_builder: UltrametricTreeBuilder):
        self.pages = pages
        self.pagelinks = pagelinks
        self.tree = tree_builder
        
        # Precompute: which article IDs have both categories and links
        self.valid_articles = sorted(set(pagelinks.keys()) & set(tree_builder.article_to_cats.keys()))
        print(f"[ENGINE] {len(self.valid_articles)} articles with both categories and links")
    
    def compute_uvr(self, sample_size: int = 10000, tau: float = 0.5) -> dict:
        """
        Compute UVR for a sample of articles.
        
        For each article a:
          - E(a) = outgoing wikilinks
          - E_T(a) = wikilinks to target in same ultrametric cluster
            (ultrametric distance < tau)
          - UVR(a) = |E(a) \ E_T(a)| / |E(a)|
        """
        sample = random.sample(self.valid_articles, min(sample_size, len(self.valid_articles)))
        
        uvrs = []
        tree_edges_total = 0
        street_edges_total = 0
        
        for a_id in sample:
            targets = self.pagelinks.get(a_id, [])
            if not targets:
                continue
            
            tree_count = 0
            for t_id in targets:
                if t_id in self.tree.article_to_cats:
                    d = self.tree.ultrametric_distance(a_id, t_id)
                    if d < tau:
                        tree_count += 1
            
            if len(targets) > 0:
                uvr_a = (len(targets) - tree_count) / len(targets)
                uvrs.append(uvr_a)
                tree_edges_total += tree_count
                street_edges_total += len(targets) - tree_count
        
        mean_uvr = sum(uvrs) / len(uvrs) if uvrs else 0
        median_uvr = sorted(uvrs)[len(uvrs)//2] if uvrs else 0
        
        total_edges = tree_edges_total + street_edges_total
        global_uvr = street_edges_total / total_edges if total_edges > 0 else 0
        
        return {
            "sample_size": len(uvrs),
            "mean_uvr": round(mean_uvr, 4),
            "median_uvr": round(median_uvr, 4),
            "global_uvr": round(global_uvr, 4),
            "total_edges": total_edges,
            "tree_edges": tree_edges_total,
            "street_edges": street_edges_total,
            "uvr_distribution": {
                "p10": round(sorted(uvrs)[max(0, len(uvrs)//10)], 4) if uvrs else 0,
                "p25": round(sorted(uvrs)[max(0, len(uvrs)//4)], 4) if uvrs else 0,
                "p50": round(median_uvr, 4),
                "p75": round(sorted(uvrs)[min(len(uvrs)-1, 3*len(uvrs)//4)], 4) if uvrs else 0,
                "p90": round(sorted(uvrs)[min(len(uvrs)-1, 9*len(uvrs)//10)], 4) if uvrs else 0,
            }
        }
    
    def compute_walk_entropy(self, walks: int = 1000, steps: int = 20, 
                              tau: float = 0.5) -> float:
        """
        Simulate random walks and measure cluster-crossing rate.
        
        For each random walk of length L:
          - At each step, choose a random outgoing link
          - Count how many times the ultrametric distance from the start 
            exceeds tau (cluster-boundary crossings)
          - WE = mean(cluster_crossings_per_step)
        """
        total_crossings = 0
        total_steps = 0
        
        for w in range(walks):
            if w % 200 == 0:
                print(f"  Walk {w}/{walks}...")
            
            # Start at a random article
            current = random.choice(self.valid_articles)
            start = current
            
            for s in range(steps):
                targets = self.pagelinks.get(current, [])
                if not targets:
                    break
                
                # Move to a random linked article
                next_id = random.choice(targets)
                
                # Check if we crossed a cluster boundary
                if next_id in self.tree.article_to_cats:
                    d = self.tree.ultrametric_distance(start, next_id)
                    if d > tau:
                        total_crossings += 1
                
                current = next_id
                total_steps += 1
        
        we = total_crossings / total_steps if total_steps > 0 else 0
        return round(we, 4)
    
    def compute_serendipity_quotient(self, walks: int = 1000, steps: int = 15,
                                      tau: float = 0.7) -> float:
        """
        Compute SQ: fraction of clicks that are "serendipitous" 
        (land on a page with high ultrametric distance from the start).
        """
        total_serendipitous = 0
        total_clicks = 0
        
        for w in range(walks):
            start = random.choice(self.valid_articles)
            current = start
            
            for s in range(steps):
                targets = self.pagelinks.get(current, [])
                if not targets:
                    break
                
                next_id = random.choice(targets)
                
                if next_id in self.tree.article_to_cats:
                    d = self.tree.ultrametric_distance(start, next_id)
                    if d > tau:
                        total_serendipitous += 1
                
                current = next_id
                total_clicks += 1
        
        sq = total_serendipitous / total_clicks if total_clicks > 0 else 0
        return round(sq, 4)
    
    def compute_full_report(self, sample_size: int = 10000, 
                            walk_samples: int = 1000) -> dict:
        """Compute all metrics and return a comprehensive report."""
        print(f"\n{'='*60}")
        print(f"  UVR MEASUREMENT: Wikipedia Interface Quality Audit")
        print(f"{'='*60}\n")
        
        t0 = time.time()
        
        print(f"[1/3] Computing UVR (sample={sample_size})...")
        uvr_data = self.compute_uvr(sample_size)
        print(f"  UVR = {uvr_data['mean_uvr']} (global: {uvr_data['global_uvr']})")
        
        print(f"\n[2/3] Computing Walk-Entropy ({walk_samples} walks × 20 steps)...")
        we = self.compute_walk_entropy(walk_samples, 20)
        print(f"  WE  = {we}")
        
        print(f"\n[3/3] Computing Serendipity Quotient ({walk_samples} walks × 15 steps)...")
        sq = self.compute_serendipity_quotient(walk_samples, 15)
        print(f"  SQ  = {sq}")
        
        elapsed = time.time() - t0
        print(f"\n  ⏱ Completed in {elapsed:.1f}s")
        
        return {
            "metadata": {
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "total_articles": len(self.valid_articles),
                "sample_size": sample_size,
                "walk_samples": walk_samples,
                "elapsed_seconds": round(elapsed, 1),
            },
            "uvr": uvr_data,
            "walk_entropy": we,
            "serendipity_quotient": sq,
            "consolidation_estimate": round(1.0 - sq * 0.6, 4),  # heuristic
            "interface_quality_j": round(sq * (1.0 - sq * 0.6), 4),  # J = SQ × C
        }


# ─── LONGITUDINAL COMPARISON ──────────────────────────────────────

def compare_dumps(dump_paths: dict[str, str], sample_size: int = 5000) -> dict:
    """
    Compare UVR across multiple Wikipedia dump dates.
    
    dump_paths: {"2006-01": "/path/to/dump", "2009-01": "/path/to/dump", ...}
    """
    results = {}
    
    for date, path in dump_paths.items():
        print(f"\n{'='*60}")
        print(f"  PROCESSING: Wikipedia {date}")
        print(f"{'='*60}")
        
        parser = WikipediaSQLDumpParser(path)
        pages = parser.parse_page()
        catlinks = parser.parse_categorylinks(pages)
        pagelinks = parser.parse_pagelinks(pages)
        
        tree_builder = UltrametricTreeBuilder(pages, catlinks)
        tree_builder.build_category_tree()
        
        engine = UVREngine(pages, pagelinks, tree_builder)
        report = engine.compute_full_report(sample_size, walk_samples=500)
        
        results[date] = report
    
    return results


# ─── MAIN ─────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Wikipedia UVR Measurement Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single dump analysis
  python wikipedia_uvr.py --dump-dir ./enwiki-20250101/ --sample 50000

  # Longitudinal comparison
  python wikipedia_uvr.py --longitudinal --dumps 2006=./2006/ 2012=./2012/ 2025=./2025/

  # Quick test with small sample
  python wikipedia_uvr.py --dump-dir ./enwiki-test/ --sample 1000 --quick
        """
    )
    parser.add_argument("--dump-dir", "-d", help="Directory containing Wikipedia SQL dump files")
    parser.add_argument("--sample", "-s", type=int, default=10000, help="Number of articles to sample for UVR")
    parser.add_argument("--walks", "-w", type=int, default=1000, help="Number of random walks for WE/SQ")
    parser.add_argument("--output", "-o", default="wikipedia_uvr_results.json", help="Output JSON file")
    parser.add_argument("--longitudinal", action="store_true", help="Compare multiple dump dates")
    parser.add_argument("--quick", action="store_true", help="Quick mode: smaller sample, fewer walks")
    parser.add_argument("--tau", type=float, default=0.5, help="Ultrametric distance threshold for cluster crossing")
    args = parser.parse_args()
    
    if args.quick:
        args.sample = min(args.sample, 2000)
        args.walks = min(args.walks, 200)
    
    if args.longitudinal:
        # Longitudinal mode requires manual dump path specification
        print("[LONGITUDINAL MODE] Specify dump paths:")
        print("  Example: --dumps 2006=./2006/ 2012=./2012/ 2025=./2025/")
        print("  (Not yet implemented in this script — use separate runs per dump)")
        sys.exit(0)
    
    if not args.dump_dir:
        print("ERROR: --dump-dir is required. Specify the directory containing Wikipedia SQL dumps.")
        print("Download from: https://dumps.wikimedia.org/enwiki/YYYYMMDD/")
        print("Required files: *page*.sql*, *categorylinks*.sql*, *pagelinks*.sql*")
        sys.exit(1)
    
    print(f"\n{'#'*60}")
    print(f"  WIKIPEDIA UVR MEASUREMENT PIPELINE")
    print(f"  Dump directory: {args.dump_dir}")
    print(f"  Sample size:    {args.sample}")
    print(f"  Walks:          {args.walks}")
    print(f"  Tau threshold:  {args.tau}")
    print(f"{'#'*60}\n")
    
    # Step 1: Parse dumps
    parser_obj = WikipediaSQLDumpParser(args.dump_dir)
    pages = parser_obj.parse_page()
    catlinks = parser_obj.parse_categorylinks(pages)
    pagelinks = parser_obj.parse_pagelinks(pages)
    
    # Step 2: Build category tree
    tree_builder = UltrametricTreeBuilder(pages, catlinks)
    tree_builder.build_category_tree()
    
    # Step 3: Compute metrics
    engine = UVREngine(pages, pagelinks, tree_builder)
    report = engine.compute_full_report(args.sample, args.walks)
    
    # Step 4: Output
    print(f"\n{'='*60}")
    print(f"  FINAL RESULTS")
    print(f"{'='*60}")
    print(f"  UVR (mean):    {report['uvr']['mean_uvr']}")
    print(f"  UVR (global):  {report['uvr']['global_uvr']}")
    print(f"  Walk-Entropy:  {report['walk_entropy']}")
    print(f"  SQ:            {report['serendipity_quotient']}")
    print(f"  J (SQ×C):      {report['interface_quality_j']}")
    print(f"  Sweet spot?    {'YES' if 0.4 <= report['uvr']['mean_uvr'] <= 0.85 else 'see discussion'}")
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n  Results saved to: {args.output}")
    print(f"  {'='*60}\n")


if __name__ == "__main__":
    main()
