import json

with open(r"projects/braided-memory-register/scripts/author_mapping.json", encoding="utf-8") as f:
    mapping = json.load(f)

papers_json = r"C:\Users\LENOVO\AppData\Local\Temp\qnfo_papers.json"
with open(papers_json, encoding="utf-8") as f:
    data = json.load(f)

papers_by_id = {}
for p in data.get("nodes", data):
    props = p.get("properties", {})
    pid = props.get("paper_id", "")
    papers_by_id[pid] = props

missing_pids = [pid for pid, info in mapping.items() if not info["author"]]
print(f"Missing: {len(missing_pids)} papers\n")

# Show all missing with abstract analysis
for pid in missing_pids:
    props = papers_by_id.get(pid, {})
    abstract = props.get("abstract", "")
    title = props.get("title", "?")
    
    # Check for alternative patterns
    checks = []
    if "ORCID" in abstract:
        checks.append("ORCID")
    if "ISNI" in abstract:
        checks.append("ISNI")
    if "license" in abstract.lower() or "copyright" in abstract.lower():
        checks.append("LICENSE")
    if "---" in abstract[:10]:
        checks.append("HAS_FRONTMATTER")
    
    # Look for any author-like pattern
    import re
    auth_patterns = list(re.finditer(r"author[:\s]+(.+?)$", abstract[:500], re.MULTILINE | re.IGNORECASE))
    
    print(f"[{pid}] {title[:70]}")
    print(f"  checks: {checks}")
    if auth_patterns:
        print(f"  found: {[m.group(1)[:50] for m in auth_patterns]}")
    print(f"  abstract[0:120]: {abstract[:120]}")
    print()
