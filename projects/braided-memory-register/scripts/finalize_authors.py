import json
import re
from collections import Counter

# Load existing mapping
with open(r"projects/braided-memory-register/scripts/author_mapping.json", encoding="utf-8") as f:
    mapping = json.load(f)

papers_json = r"C:\Users\LENOVO\AppData\Local\Temp\qnfo_papers.json"
with open(papers_json, encoding="utf-8") as f:
    data = json.load(f)

# Enrich missing papers: check for author in text, ORCID, email patterns
EMAIL_AUTHOR_RE = re.compile(r"\[(Rowan Brad Quni(?:-Gudzinas)?)\]\(mailto:", re.IGNORECASE)
TEXT_AUTHOR_RE = re.compile(r"\*\*(Rowan Brad Quni(?:-Gudzinas)?)\*\*", re.IGNORECASE)
DEFAULT_AUTHOR = ["Rowan Brad Quni-Gudzinas"]

papers_props = {}
for p in data.get("nodes", data):
    props = p.get("properties", {})
    pid = props.get("paper_id", "")
    papers_props[pid] = props

enriched = 0
still_missing = 0
other_authors = []

for pid, info in mapping.items():
    if info["author"]:
        continue  # Already found
    
    props = papers_props.get(pid, {})
    abstract = props.get("abstract", "")
    
    # Try email link pattern: [Rowan Brad Quni](mailto:...)
    m = EMAIL_AUTHOR_RE.search(abstract)
    if m:
        name = m.group(1)
        if name == "Rowan Brad Quni":
            name = "Rowan Brad Quni-Gudzinas"
        info["author"] = name
        info["source"] = "email_link"
        enriched += 1
        if name != DEFAULT_AUTHOR[0]:
            other_authors.append((pid, name))
        continue
    
    # Try bold text pattern: **Rowan Brad Quni**
    m = TEXT_AUTHOR_RE.search(abstract)
    if m:
        name = m.group(1)
        if name == "Rowan Brad Quni":
            name = "Rowan Brad Quni-Gudzinas"
        info["author"] = name
        info["source"] = "bold_text"
        enriched += 1
        if name != DEFAULT_AUTHOR[0]:
            other_authors.append((pid, name))
        continue
    
    # Default: attribute to Rowan (single-author corpus)
    info["author"] = DEFAULT_AUTHOR[0]
    info["source"] = "default_single_author"
    enriched += 1

# Save enriched mapping
with open(r"projects/braided-memory-register/scripts/author_mapping.json", "w", encoding="utf-8") as f:
    json.dump(mapping, f, indent=2, ensure_ascii=False)

# ── Build sync payload for graph-api ──────────────────────────────────
sync_nodes = []
for pid, info in mapping.items():
    authors_list = [info["author"]] if isinstance(info["author"], str) else info["author"]
    sync_nodes.append({
        "id": info["node_id"],
        "label": "Paper",
        "name": info["title"],
        "properties": {
            "authors": json.dumps(authors_list),
        }
    })

sync_payload = {"nodes": sync_nodes, "edges": []}
with open(r"projects/braided-memory-register/scripts/author_sync_payload.json", "w", encoding="utf-8") as f:
    json.dump(sync_payload, f, indent=2, ensure_ascii=False)

# ── Generate report ───────────────────────────────────────────────────
ad = Counter()
source_stats = Counter()
for info in mapping.values():
    ad[info["author"]] += 1
    source_stats[info.get("source", "frontmatter")] += 1

report = f"""# Author Extraction Report — Final
**Date:** 2026-07-03

## Summary
- **Total papers:** {len(mapping)}
- **All attributed to:** Rowan Brad Quni-Gudzinas (single-author corpus)

## Extraction Sources
"""
for src, count in source_stats.most_common():
    report += f"- **{src}**: {count}\n"

report += f"""
## Author Distribution
"""
for author, count in ad.most_common():
    report += f"- **{author}**: {count} papers\n"

if other_authors:
    report += "\n## Non-default Authors\n"
    for pid, name in other_authors:
        report += f"- `{pid}` → {name}\n"

report += f"""
## Sync Payload
- File: `author_sync_payload.json`
- Nodes to update: {len(sync_nodes)}
- Target: `POST https://graph-api.q08.workers.dev/sync`
"""

with open(r"projects/braided-memory-register/scripts/author_extraction_report.md", "w", encoding="utf-8") as f:
    f.write(report)

# Print summary
print(f"Total papers: {len(mapping)}")
print(f"Author distribution:")
for author, count in ad.most_common():
    print(f"  {author}: {count}")
print(f"\nExtraction sources:")
for src, count in source_stats.most_common():
    print(f"  {src}: {count}")
print(f"\nSync payload: {len(sync_nodes)} nodes → author_sync_payload.json")
print(f"Report → author_extraction_report.md")
if other_authors:
    print(f"\nNon-default authors found: {len(other_authors)}")
    for pid, name in other_authors:
        print(f"  {pid}: {name}")
