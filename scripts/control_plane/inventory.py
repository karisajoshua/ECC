#!/usr/bin/env python3
"""Read-only public repository health inventory for ECC."""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

OWNER = os.environ.get("ECC_GITHUB_OWNER", "karisajoshua")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
API = "https://api.github.com"
HEADERS = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "ecc-control-plane-audit",
    "X-GitHub-Api-Version": "2022-11-28",
}
if TOKEN:
    HEADERS["Authorization"] = f"Bearer {TOKEN}"


def get(path):
    req = urllib.request.Request(API + path, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        if exc.code in (403, 404):
            return None
        raise


def main():
    results = []
    page = 1
    while True:
        query = urllib.parse.urlencode({"per_page": 100, "page": page, "type": "public"})
        repos = get(f"/users/{urllib.parse.quote(OWNER)}/repos?{query}")
        if repos is None:
            raise RuntimeError("Unable to retrieve public repository inventory")
        if not repos:
            break
        for repo in repos:
            if repo.get("archived"):
                status = "ARCHIVED"
            else:
                status = "NOT_VERIFIED"
            results.append({
                "repository": repo["full_name"],
                "visibility": "public",
                "archived": bool(repo.get("archived")),
                "default_branch": repo.get("default_branch"),
                "health": status,
                "note": "Workflow runs and branch protections are not verified by this inventory.",
            })
        if len(repos) < 100:
            break
        page += 1
        if page > 100:
            raise RuntimeError("Inventory pagination safety limit reached")
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "owner": OWNER,
        "scope": "public repositories only",
        "private_repositories_included": False,
        "repositories": results,
        "count": len(results),
    }
    with open("ecc-public-repository-inventory.json", "w", encoding="utf-8") as output:
        json.dump(report, output, indent=2)
    print(f"Inventory completed: {len(results)} public repositories; CI and security status not verified.")
    with open(os.environ.get("GITHUB_STEP_SUMMARY", os.devnull), "a", encoding="utf-8") as summary:
        summary.write("## ECC Public Repository Inventory\n\n")
        summary.write(f"- Owner: \`{OWNER}\`\n")
        summary.write(f"- Public repositories discovered: **{len(results)}**\n")
        summary.write("- Private repositories: **not included**\n")
        summary.write("- CI, vulnerability and deployment status: **not verified**\n")
        summary.write("- No repository was modified.\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
