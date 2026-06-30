#!/usr/bin/env python3
"""
Zenodo Publication — Silent Radix Research Program v1.0
Creates a Zenodo deposition and uploads all 8 research artifacts.

Usage:
  python zenodo_upload_silent_radix.py
  python zenodo_upload_silent_radix.py --dry-run

Environment:
  ZENODO_TOKEN (required)
  Create at: https://zenodo.org/account/settings/applications/
  Scopes: deposit:actions, deposit:write
"""

import json
import os
import sys
import urllib.request
import urllib.error


# ─── Configuration ──────────────────────────────────────────────────────────

ZENODO_BASE = "https://zenodo.org/api"

METADATA = {
    "title": "The Silent Radix: Positional Notation as Ultrametric Tree and the Calculus of Indications as Remedy",
    "description": (
        "A consilient research program demonstrating that positional notation is an ultrametric tree "
        "whose radix encodes a chosen grouping cycle; that the systematic errors of silent radices, "
        "silent metrics, and assumed linearity arise from substituting a monocultural decimal default "
        "and flattening the tree into an Archimedean line; and that re-founding on Spencer-Brown's "
        "calculus of indications restores the observer, the ultrametric, and the self-measuring '10' "
        "as the seed of all self-aware quantity.\n\n"
        "Deliverables:\n"
        "- Consequence Atlas: 65 documented silent-frame errors across computing, science, cognition, and history\n"
        "- Synthesis Paper: 9-section research paper with literature anchoring\n"
        "- Formal Appendix: 8 theorems including Silent Radix Fixed-Point Lemma and Observer Necessity Theorem\n"
        "- Explicit Frame Pattern Language: 9 design patterns for self-aware numeric communication\n"
        "- LoF Number Builder Specification: Interactive web application design\n"
        "- Cross-Reference Index: Bidirectional Atlas-to-paper claim mapping\n"
        "- README: Master index with thesis compression and literature anchoring"
    ),
    "creators": [
        {"name": "QNFO Research", "affiliation": "QWAV / QNFO"}
    ],
    "keywords": [
        "positional notation", "ultrametric", "silent radix", "Laws of Form",
        "p-adic", "foundation of mathematics", "measurement theory", "cycles",
        "Spencer-Brown", "calculus of indications", "explicit frames",
        "second-order cybernetics", "observer", "re-entry"
    ],
    "license": "cc-by-4.0",
    "upload_type": "publication",
    "publication_type": "workingpaper",
    "access_right": "open",
    "version": "1.0.0",
    "language": "eng",
    "notes": (
        "One-month research sprint. Single researcher with LLM orchestration. "
        "All claims anchored in published literature. "
        "Consequence Atlas contains 65 verified silent-frame errors. "
        "Formal Appendix contains 8 theorems with proof sketches."
    ),
}

ARTIFACTS = [
    "silent-radix-synthesis-paper-v1.0.md",
    "consequence-atlas-v1.0.md",
    "consequence-atlas-supplement-v1.0.md",
    "formal-appendix-silent-radix-theorem.md",
    "explicit-frame-pattern-language-v1.0.md",
    "lof-number-builder-specification-v1.0.md",
    "cross-reference-index-v1.0.md",
    "README-silent-radix-research-program.md",
]


# ─── Zenodo API ─────────────────────────────────────────────────────────────

def zenodo_request(method, endpoint, token, data=None, content_type="application/json"):
    """Make a request to the Zenodo API."""
    url = f"{ZENODO_BASE}/{endpoint}"
    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", f"Bearer {token}")

    if method in ("POST", "PUT") and data is not None:
        if content_type == "application/json":
            body = json.dumps(data).encode("utf-8")
        else:
            body = data if isinstance(data, bytes) else data.encode("utf-8")
        req.add_header("Content-Type", content_type)
    else:
        body = None

    try:
        resp = urllib.request.urlopen(req, data=body, timeout=30)
        return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else str(e)
        return {"error": f"HTTP {e.code}: {body}"}
    except Exception as e:
        return {"error": str(e)}


def load_token():
    """Load Zenodo token from environment or token file."""
    token = os.environ.get("ZENODO_TOKEN", "")
    if token:
        return token
    token_path = os.path.expandvars(r"%USERPROFILE%\.zenodo_token")
    if os.path.exists(token_path):
        with open(token_path, "r", encoding="utf-8-sig") as f:
            return f.read().strip()
    raise FileNotFoundError(
        "[BLOCKED] Zenodo token not found.\n"
        "Set ZENODO_TOKEN env var or store at %USERPROFILE%\\.zenodo_token\n"
        "Get token from: https://zenodo.org/account/settings/applications/"
    )


# ─── Main ──────────────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Publish Silent Radix to Zenodo")
    parser.add_argument("--dry-run", action="store_true", help="Validate artifacts but don't publish")
    args = parser.parse_args()

    token = load_token()
    print("=== SILENT RADIX — Zenodo Publication v1.0 ===\n")

    # Step 1: Validate all artifacts exist
    print("[1/4] Validating artifacts...")
    missing = []
    for f in ARTIFACTS:
        if os.path.isfile(f):
            size = os.path.getsize(f)
            print(f"  OK  {f} ({size} B)")
        else:
            print(f"  MISS  {f}")
            missing.append(f)

    if missing:
        print(f"\n[BLOCKED] {len(missing)} artifact(s) missing. Aborting.")
        sys.exit(1)

    if args.dry_run:
        print("\n[DRY RUN] All artifacts validated. Would create deposition and upload.")
        return

    # Step 2: Create deposition
    print("\n[2/4] Creating deposition...")
    dep_metadata = {"metadata": METADATA}
    result = zenodo_request("POST", "deposit/depositions", token, dep_metadata)
    if "error" in result:
        print(f"[FAIL] {result['error']}")
        sys.exit(1)

    deposition_id = result["id"]
    bucket_url = result["links"]["bucket"]
    print(f"  Deposition ID: {deposition_id}")
    print(f"  Bucket: {bucket_url}")

    # Step 3: Upload artifacts
    print("\n[3/4] Uploading artifacts...")
    uploaded = 0
    for f in ARTIFACTS:
        with open(f, "rb") as fh:
            data = fh.read()
        endpoint = f"{bucket_url}/{f}"
        # Use raw PUT to bucket URL
        req = urllib.request.Request(endpoint, data=data, method="PUT")
        req.add_header("Authorization", f"Bearer {token}")
        req.add_header("Content-Type", "application/octet-stream")
        try:
            urllib.request.urlopen(req, timeout=60)
            print(f"  OK  {f} ({len(data)} B)")
            uploaded += 1
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8") if e.fp else str(e)
            print(f"  FAIL {f}: HTTP {e.code}: {body[:200]}")

    if uploaded < len(ARTIFACTS):
        print(f"\n[WARN] {uploaded}/{len(ARTIFACTS)} uploaded. Deposition NOT published. Review errors and retry.")
        print(f"  Deposition ID: {deposition_id} (draft — not yet published)")
        sys.exit(1)

    # Step 4: Publish
    print("\n[4/4] Publishing deposition...")
    result = zenodo_request("POST", f"deposit/depositions/{deposition_id}/actions/publish", token)
    if "error" in result:
        print(f"[FAIL] {result['error']}")
        sys.exit(1)

    doi = result["doi"]
    record_url = result["links"]["record"]

    print(f"\n{'='*60}")
    print(f"PUBLICATION COMPLETE")
    print(f"  DOI:        {doi}")
    print(f"  Record URL: {record_url}")
    print(f"  Concept DOI: {result.get('conceptdoi', 'N/A')}")
    print(f"  Deposition:  {deposition_id}")
    print(f"\nSet env var for Buffer:  SLT_RADIX_DOI={doi}")
    print(f"Buffer command:           python buffer_post_silent_radix.py --doi {doi}")

    # Write DOI to a file for downstream tools
    with open("SLT_RADIX_DOI.txt", "w") as f:
        f.write(doi)


if __name__ == "__main__":
    main()
