"""mkdocs hook: fetch latest GitHub releases at build time.

Writes trimmed release data into the built site so visitors never have to call
the GitHub API directly (which is rate-limited to 60/hr per IP when
unauthenticated). One file per project:

    data/releases.json                  mickem/nscp            (the agent)
    data/check_nsclient-releases.json   mickem/check_nsclient  (the CLI)

`assets/js/latest-release.js` reads them to fill in versions, dates and
download links on the home page and on /download/.

Set GITHUB_TOKEN in the environment to bump the build-time rate limit to
5000/hr (auto-set inside GitHub Actions).
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request

# key -> (GitHub repo, file written under <site>/data/)
PROJECTS = {
    "nscp": ("mickem/nscp", "releases.json"),
    "check_nsclient": ("mickem/check_nsclient", "check_nsclient-releases.json"),
}
PER_PAGE = 15
KEEP = 5
CACHE_DIR = ".cache"
CACHE_TTL_SECONDS = 60 * 60
TIMEOUT_SECONDS = 10


def _cache_path(key):
    if key == "nscp":
        # Keep the original name so existing caches stay valid.
        return os.path.join(CACHE_DIR, "github-releases.json")
    return os.path.join(CACHE_DIR, "github-releases-%s.json" % key)


def _load_cache(key):
    path = _cache_path(key)
    try:
        if not os.path.exists(path):
            return None
        if time.time() - os.path.getmtime(path) > CACHE_TTL_SECONDS:
            return None
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        if not isinstance(data, list):
            return None
        return data
    except (OSError, ValueError):
        return None


def _save_cache(key, data):
    path = _cache_path(key)
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(data, fh)
    except OSError:
        pass


def _fetch_github(repo):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "nsclient-docs-build",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request(
        "https://api.github.com/repos/" + repo + "/releases?per_page=" + str(PER_PAGE),
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


def _write(config, key, repo, filename):
    cached = _load_cache(key)
    if cached is not None:
        releases = cached
        source = "cache"
    else:
        try:
            releases = _fetch_github(repo)
            _save_cache(key, releases)
            source = "github"
        except (urllib.error.URLError, TimeoutError, ValueError) as e:
            print("fetch_releases: %s fetch failed: %s" % (repo, e), file=sys.stderr)
            return

    trimmed = _trim(releases)
    if not trimmed:
        print("fetch_releases: no stable releases for %s, skipping" % repo, file=sys.stderr)
        return

    out_path = os.path.join(config["site_dir"], "data", filename)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(trimmed, fh)

    print("fetch_releases: %s -> %s, %d stable releases (source: %s)"
          % (repo, filename, len(trimmed), source))


def on_post_build(config, **kwargs):
    for key, (repo, filename) in PROJECTS.items():
        _write(config, key, repo, filename)
