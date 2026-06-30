#!/usr/bin/env python3
"""
Buffer Social Media Posting — Silent Radix Research Program v1.0
Uses Buffer GraphQL API v2.0 (NOT the deprecated REST API).

Usage:
  python buffer_post_silent_radix.py --doi 10.5281/zenodo.XXXXX [--dry-run] [--now]
  python buffer_post_silent_radix.py --list

Environment:
  BUFFER_ACCESS_TOKEN (or stored at %USERPROFILE%\\.buffer_token)
  SLT_RADIX_DOI (optional, overrides --doi flag)
"""

import json
import os
import sys
import urllib.request
from datetime import datetime, timedelta, timezone


# ─── Configuration ──────────────────────────────────────────────────────────

PAPER_TITLE = "The Silent Radix: Positional Notation as Ultrametric Tree and the Calculus of Indications as Remedy"
PAPER_URL = None  # Will be derived from DOI
DOI = None

SOCIAL_POSTS = [
    {
        "key": "launch",
        "platforms": ["twitter", "linkedin", "bluesky"],
        "text_template": {
            "twitter": "Published: The Silent Radix — a consilient research program demonstrating that positional notation is an ultrametric tree, not a Euclidean line. 65 documented errors from C octal bugs to the Mars Climate Orbiter trace to one structural fault: the silent interpretive frame. {doi_url}",
            "linkedin": "New research: THE SILENT RADIX — Positional Notation as Ultrametric Tree and the Calculus of Indications as Remedy.\n\nKey findings:\n\u2022 65 documented silent-frame errors cataloged (72% Critical/High severity)\n\u2022 Every error follows the same structural pattern: an interpretive frame is not carried with the representation\n\u2022 The p-adic ultrametric is NATIVE to positional notation — the Euclidean line is a secondary flattening\n\u2022 9 design patterns proposed for self-aware numeric communication\n\u2022 Spencer-Brown's Laws of Form provides a foundation where frames cannot be hidden\n\u2022 8 formal theorems including the Silent Radix Fixed-Point Lemma\n\nDOI: {doi_url}\n\n#mathematics #foundations #ultrametric #lawsofform #OpenScience",
            "bluesky": "New paper: THE SILENT RADIX\n\nPositional notation is an ultrametric tree. The Euclidean line is a secondary flattening. The '10' misnomer is a Godel sentence in miniature.\n\n65 documented failures. 8 theorems. 9 design patterns. 21 references.\n\n{doi_url}",
        },
        "stagger_hours": 0,
    },
    {
        "key": "thesis",
        "platforms": ["twitter", "bluesky"],
        "text_template": {
            "twitter": "The '10' misnomer isn't a joke. It's a Godel sentence in miniature. Every base calls itself 'base-10' because the numeral string '10' can't name its own radix without an external observer. We prove this in the Silent Radix Fixed-Point Lemma. {doi_url}",
            "bluesky": "The '10' misnomer is not a joke. Every base calls itself 'base-10' because the numeral '10' can't name its own radix. It's a Godel sentence in miniature — the cycle that counts its own completion. {doi_url}",
        },
        "stagger_hours": 24,
    },
    {
        "key": "ultrametric",
        "platforms": ["twitter", "bluesky"],
        "text_template": {
            "twitter": "Positional notation IS an ultrametric tree. We've been reading tree data through line glasses. The p-adic numbers recover what was always native to the digit string. The Euclidean number line is a secondary projection. {doi_url}",
            "bluesky": "Positional notation IS an ultrametric tree. The p-adic numbers recover what was always native to the digit string. The Euclidean number line is a secondary projection — useful, but not fundamental. {doi_url}",
        },
        "stagger_hours": 48,
    },
    {
        "key": "design",
        "platforms": ["twitter"],
        "text_template": {
            "twitter": "9 design patterns for self-aware numeric communication: Radix Tag, Metric Declaration, Unit Glue, Scale Type Annotation, Cyclic Grounding, Epoch Declaration, Precision Bounds, Frame Inheritance, The Witness. No more naked numbers. {doi_url}",
        },
        "stagger_hours": 72,
    },
    {
        "key": "foundation",
        "platforms": ["linkedin"],
        "text_template": {
            "linkedin": "Why Spencer-Brown's Laws of Form?\n\nStandard set theory (ZFC) builds numbers from the empty set and membership — erasing the act of distinction and the observer. Laws of Form begins with the single act of drawing a distinction — marking a cycle.\n\nIn this foundation:\n\u2022 Numbers are nested forms — trees of distinctions\n\u2022 The base is a visible choice of grouping — not a hidden parameter\n\u2022 The '10' self-reference is a stable re-entrant form — the cycle marking its own completion\n\u2022 The observer is INCLUDED in the representation, not subtracted from it\n\nThis is the move from first-order numeracy (silent frames) to second-order numeracy (explicit frames).\n\nDOI: {doi_url}\n\n#mathematics #foundations #LawOfForm #secondOrderCybernetics",
        },
        "stagger_hours": 96,
    },
    {
        "key": "summary",
        "platforms": ["twitter", "bluesky"],
        "text_template": {
            "twitter": "One researcher. One month. One LLM. 8 theorems. 65 documented errors. 9 design patterns. The Silent Radix shows that every 'base-10' misnomer hides a universal epistemic vulnerability — and a remedy. {doi_url}",
            "bluesky": "One researcher. One month. One LLM.\n8 theorems. 65 documented errors. 9 design patterns.\n\nThe Silent Radix: every 'base-10' misnomer hides a universal epistemic vulnerability — and a remedy. {doi_url}",
        },
        "stagger_hours": 120,
    },
]


# ─── Buffer GraphQL API ────────────────────────────────────────────────────

def gql_query(token, query, variables=None):
    """Execute a GraphQL query against the Buffer API."""
    body = {"query": query}
    if variables:
        body["variables"] = variables
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        "https://api.buffer.com/1/graphql.json",
        data=data,
        method="POST",
    )
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else str(e)
        return {"error": f"HTTP {e.code}: {body}"}
    except Exception as e:
        return {"error": str(e)}


def load_token():
    """Load Buffer access token from environment or token file."""
    token = os.environ.get("BUFFER_ACCESS_TOKEN", "")
    if token:
        return token
    token_path = os.path.expandvars(r"%USERPROFILE%\.buffer_token")
    if os.path.exists(token_path):
        with open(token_path, "r", encoding="utf-8-sig") as f:
            return f.read().strip()
    raise FileNotFoundError(
        "[BLOCKED] Buffer token not found.\n"
        "Set BUFFER_ACCESS_TOKEN env var or store at %USERPROFILE%\\.buffer_token\n"
        "Get token from: https://buffer.com/developers"
    )


def list_channels(token):
    """Discover Buffer social media channels via GraphQL."""
    result = gql_query(token, "{ account { organizations { id } } }")
    if "error" in result:
        print(f"[FAIL] Could not get organization: {result['error']}", file=sys.stderr)
        sys.exit(1)

    org_id = result["data"]["account"]["organizations"][0]["id"]
    print(f"  Organization ID: {org_id}")

    result = gql_query(token,
        '{ channels(input: { organizationId: "%s" }) '
        '{ id service name displayName isDisconnected } }' % org_id
    )
    if "error" in result:
        print(f"[FAIL] Could not list channels: {result['error']}", file=sys.stderr)
        sys.exit(1)

    return result["data"]["channels"]


def create_post(token, channel_id, text, service, link_url=None, schedule_at=None, now=False):
    """Create a Buffer post via GraphQL createPost mutation."""
    if now:
        mode = "shareNow"
    elif schedule_at:
        mode = "customScheduled"
    else:
        mode = "addToQueue"

    post_input = {
        "channelId": channel_id,
        "text": text,
        "schedulingType": "automatic",
        "mode": mode,
        "assets": [],
    }
    if schedule_at:
        post_input["dueAt"] = schedule_at
    if link_url and service:
        post_input["metadata"] = {
            service: {"linkAttachment": {"url": link_url}}
        }

    mutation = """
    mutation($input: CreatePostInput!) {
      createPost(input: $input) {
        ... on PostActionSuccess {
          post { id status text dueAt }
        }
        ... on InvalidInputError { message }
        ... on LimitReachedError { message }
      }
    }
    """
    result = gql_query(token, mutation, {"input": post_input})
    if "error" in result:
        return {"success": False, "error": str(result["error"])}

    pr = result.get("data", {}).get("createPost", {})
    if "post" in pr:
        return {
            "success": True,
            "post_id": pr["post"]["id"],
            "status": pr["post"]["status"],
            "due_at": pr["post"].get("dueAt"),
        }
    return {"success": False, "error": pr.get("message", "Unknown error")}


# ─── Main ──────────────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Post Silent Radix to social media via Buffer GraphQL API")
    parser.add_argument("--doi", default="", help="Zenodo DOI (e.g., 10.5281/zenodo.XXXXX)")
    parser.add_argument("--dry-run", action="store_true", help="Preview posts without creating")
    parser.add_argument("--now", action="store_true", help="Post immediately (ignore stagger schedule)")
    parser.add_argument("--list", action="store_true", help="List configured Buffer profiles only")
    args = parser.parse_args()

    global DOI
    DOI = args.doi or os.environ.get("SLT_RADIX_DOI", "10.5281/zenodo.XXXXX (pending)")
    doi_url = f"https://doi.org/{DOI}" if "pending" not in DOI else "[DOI pending]"

    token = load_token()

    if args.list:
        channels = list_channels(token)
        print(f"\nBuffer Profiles ({len(channels)}):")
        for ch in channels:
            status = " [DISCONNECTED]" if ch.get("isDisconnected") else ""
            print(f"  [{ch['service']}] {ch['displayName']} (ID: {ch['id']}){status}")
        return

    # Discover channels
    channels = list_channels(token)
    channel_map = {}
    for ch in channels:
        svc = ch["service"].lower()
        if svc not in channel_map:
            channel_map[svc] = []
        channel_map[svc].append(ch)

    base_time = datetime.now(timezone.utc)
    results = []

    for post_def in SOCIAL_POSTS:
        for platform in post_def["platforms"]:
            if platform not in channel_map:
                print(f"  [SKIP] {platform} — no connected Buffer profile")
                continue

            template = post_def["text_template"].get(platform)
            if not template:
                continue

            text = template.format(doi_url=doi_url)
            schedule_at = None
            if not args.now:
                schedule_time = base_time + timedelta(hours=post_def["stagger_hours"])
                schedule_at = schedule_time.isoformat()

            for ch in channel_map[platform]:
                if ch.get("isDisconnected"):
                    print(f"  [SKIP] {platform} ({ch['displayName']}) — disconnected")
                    continue

                print(f"\n[{post_def['key']}] {platform} ({ch['displayName']})")
                print(f"  Text: {text[:100]}...")
                if schedule_at:
                    print(f"  Schedule: {schedule_at}")

                if args.dry_run:
                    print(f"  [DRY RUN] Would create post")
                    results.append({"platform": platform, "status": "dry_run"})
                    continue

                result = create_post(
                    token=token,
                    channel_id=ch["id"],
                    text=text,
                    service=platform,
                    link_url=doi_url if "pending" not in DOI else None,
                    schedule_at=schedule_at,
                    now=args.now,
                )

                if result["success"]:
                    print(f"  [OK] Created. Post ID: {result['post_id']}")
                    results.append({"platform": platform, "status": "success", "post_id": result["post_id"]})
                else:
                    print(f"  [FAIL] {result['error']}")
                    results.append({"platform": platform, "status": "failed", "error": result["error"]})

    # Summary
    success_count = sum(1 for r in results if r["status"] in ("success", "dry_run"))
    print(f"\n{'='*60}")
    print(f"SUMMARY: {success_count}/{len(results)} posts {'would be ' if args.dry_run else ''}created")
    if not args.now and not args.dry_run:
        first_scheduled = base_time.isoformat()
        print(f"First post scheduled at: {first_scheduled}")
    print(f"\nVerify at: https://buffer.com/app")
    return 0 if success_count == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
