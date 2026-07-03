import json, re
from collections import Counter

papers_json = r"C:\Users\LENOVO\AppData\Local\Temp\qnfo_papers.json"
with open(papers_json, encoding="utf-8") as f:
    data = json.load(f)

papers = data.get("nodes", data)
AUTHOR_RE = re.compile(r"^author:\s*(.+?)$", re.MULTILINE | re.IGNORECASE)

mapping = {}
found = 0
missing = 0

for p in papers:
    props = p.get("properties", {})
    pid = props.get("paper_id", p.get("id", "?"))
    title = props.get("title", p.get("name", "?"))
    abstract = props.get("abstract", "")
    m = AUTHOR_RE.search(abstract) if abstract else None
    author = m.group(1).strip() if m else None
    if author:
        if author == "Rowan Brad Quni":
            author = "Rowan Brad Quni-Gudzinas"
        mapping[pid] = {"title": title, "author": author, "node_id": p.get("id", "")}
        found += 1
    else:
        mapping[pid] = {"title": title, "author": None, "node_id": p.get("id", "")}
        missing += 1

print(f"Total: {len(papers)}")
print(f"Found author: {found}")
print(f"Missing author: {missing}")

ad = Counter(v["author"] for v in mapping.values() if v["author"])
for a, c in ad.most_common():
    print(f"  {a}: {c}")

print()
print("=== MISSING ===")
for pid, info in mapping.items():
    if not info["author"]:
        print(f"  {pid}: {info['title'][:80]}")

out = "projects/braided-memory-register/scripts/author_mapping.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(mapping, f, indent=2, ensure_ascii=False)
print(f"\nSaved to {out}")
