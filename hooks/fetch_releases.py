"""mkdocs hook: fetch latest GitHub releases at build time.

Writes a trimmed `data/releases.json` into the built site so visitors never
have to call the GitHub API directly (which is rate-limited to 60/hr per IP
when unauthenticated).

Set GITHUB_TOKEN in the environment to bump the build-time rate limit to
5000/hr (auto-set inside GitHub Actions).
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request

REPO = "mickem/nscp"
PER_PAGE = 15
KEEP = 5
CACHE_PATH = ".cache/github-releases.json"
CACHE_TTL_SECONDS = 60 * 60
TIMEOUT_SECONDS = 10


def _load_cache():
    try:
        if not os.path.exists(CACHE_PATH):
            return None
        if time.time() - os.path.getmtime(CACHE_PATH) > CACHE_TTL_SECONDS:
            return None
        with open(CACHE_PATH, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if not isinstance(data, list):
            return None
        return data
    except (OSError, ValueError):
        return None


def _save_cache(data):
    try:
        os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
        with open(CACHE_PATH, "w", encoding="utf-8") as fh:
            json.dump(data, fh)
    except OSError:
        pass


def _fetch_github():
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "nsclient-docs-build",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(
        "https://api.github.com/repos/" + REPO + "/releases?per_page=" + str(PER_PAGE),
        headers=headers,
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
        data = json.load(resp)
    if not isinstance(data, list):
        raise ValueError("unexpected response shape: " + repr(data)[:200])
    return data


def _trim(releases):
    stable = [r for r in releases if not r.get("prerelease") and not r.get("draft")]
    result = []
    for r in stable[:KEEP]:
        body = r.get("body") or ""
        if len(body) > 500:
            body = body[:500]
        result.append({
            "tag_name": r.get("tag_name"),
            "name": r.get("name"),
            "html_url": r.get("html_url"),
            "published_at": r.get("published_at"),
            "body": body,
        })
    return result


def on_post_build(config, **kwargs):
    cached = _load_cache()
    if cached is not None:
        releases = cached
        source = "cache"
    else:
        try:
            releases = _fetch_github()
            _save_cache(releases)
            source = "github"
        except (urllib.error.URLError, TimeoutError, ValueError) as e:
            print("fetch_releases: GitHub fetch failed: %s" % e, file=sys.stderr)
            return

    trimmed = _trim(releases)
    if not trimmed:
        print("fetch_releases: no stable releases found, skipping", file=sys.stderr)
        return

    out_path = os.path.join(config["site_dir"], "data", "releases.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(trimmed, fh)

    print("fetch_releases: wrote %d stable releases (source: %s)" % (len(trimmed), source))
