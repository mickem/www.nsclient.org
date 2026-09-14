#!/usr/bin/env python3
"""Copy the NSClient Fleet server documentation into this site.

The pages in `docs/docs/fleet/` are **generated** — they are owned by
https://github.com/mickem/nsclient-fleet-server (`docs/*.md` there) and copied
here so the server documentation is published together with the agent's. Edit
them upstream, then re-run this script:

    python scripts/sync-fleet-server-docs.py ../nsclient-fleet-server

`docs/docs/fleet/index.md` is the exception: it is the section landing page,
written for this site and not present upstream, so the script leaves it alone.

Three transformations are applied:

* Links out to this site (`https://nsclient.org/docs/...`) become relative
  links, so mkdocs validates them and they keep working when the site is built
  for a preview or a subdirectory. Upstream also uses the `docs.nsclient.org`
  spelling, which redirects to the site root and loses the path; it is
  normalised here and should be fixed upstream when you see it.
* Links to files elsewhere in the upstream repository (`../docker/…`) become
  absolute GitHub URLs, since only `docs/` is copied.
* Heading anchors are translated from GitHub's slugs to mkdocs'. The two
  disagree wherever a heading contains punctuation GitHub drops but still
  counts as a word break — `## Step 6 — Make it trusted` anchors as
  `#step-6--make-it-trusted` on GitHub and `#step-6-make-it-trusted` here — so
  upstream cannot spell a link that works in both places, and this end gets
  fixed up rather than upstream being made wrong on its own repository page.

Every rewritten link is resolved against the files on disk: an URL that points
at a page which does not exist, or an anchor that matches no heading under
either slug, is reported and the script exits non-zero rather than publishing a
dead link.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path, PurePosixPath

from markdown.extensions.toc import slugify

# Upstream file -> page name in docs/docs/fleet/
PAGES = {
    "linux-install.md": "linux-install.md",
    "windows-install.md": "windows-install.md",
    "docker.md": "docker.md",
    "deployment.md": "deployment.md",
    "agent-implementation.md": "agent-implementation.md",
    "agent-integration.md": "agent-integration.md",
    "ca-rotation-playbook.md": "ca-rotation-playbook.md",
}

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_ROOT = REPO_ROOT / "docs"
TARGET_DIR = DOCS_ROOT / "docs" / "fleet"

UPSTREAM_REPO = "https://github.com/mickem/nsclient-fleet-server"
UPSTREAM_BLOB = f"{UPSTREAM_REPO}/blob/main"

# https://nsclient.org/docs/setup/fleet/ style links back into this site, and
# the docs.nsclient.org spelling of the same thing (which redirects to the site
# root, dropping the path — so it is a dead link in practice, not a slow one).
SITE_LINK = re.compile(
    r"https://(?:docs\.nsclient\.org|nsclient\.org/docs)/([^)\s#]*)(#[^)\s]*)?"
)
# Links that leave docs/ for the rest of the upstream repository.
REPO_LINK = re.compile(r"\]\(\.\./([^)\s]+)\)")
# A link to another page in this set, or to this page, carrying an anchor.
ANCHORED_LINK = re.compile(r"\]\((?P<page>[^)\s#]*)#(?P<anchor>[^)\s]+)\)")

HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*$")
FENCE = re.compile(r"^\s*(```|~~~)")

BANNER = """<!--
  This page is generated. It is maintained in the nsclient-fleet-server repository:
  https://github.com/mickem/nsclient-fleet-server/blob/main/docs/{source}
  Run scripts/sync-fleet-server-docs.py to refresh it; edits made here are
  overwritten.
-->
"""


def headings(text: str) -> list[str]:
    """Every ATX heading in a markdown document, skipping fenced code."""
    found: list[str] = []
    fence: str | None = None
    for line in text.splitlines():
        opener = FENCE.match(line)
        if opener:
            marker = opener.group(1)
            if fence is None:
                fence = marker
            elif line.strip().startswith(fence):
                fence = None
            continue
        if fence is not None:
            continue
        match = HEADING.match(line)
        if match:
            found.append(match.group(2))
    return found


def github_slug(heading: str) -> str:
    """GitHub's anchor for a heading: drop punctuation, spaces become hyphens.

    Punctuation is removed where it stands, so the spaces on either side of a
    dropped em dash survive as two hyphens — which is the whole reason this
    differs from mkdocs.
    """
    text = re.sub(r"[^\w\s-]", "", heading.lower(), flags=re.UNICODE)
    return text.replace(" ", "-")


def anchor_map(text: str) -> dict[str, str]:
    """GitHub anchor -> mkdocs anchor, for every heading that needs translating."""
    mapping: dict[str, str] = {}
    for heading in headings(text):
        mkdocs_anchor = slugify(heading, "-")
        mapping.setdefault(github_slug(heading), mkdocs_anchor)
        mapping.setdefault(mkdocs_anchor, mkdocs_anchor)
    return mapping


def resolve_site_page(url_path: str) -> Path | None:
    """Map a `/docs/<path>/` URL onto the markdown file that produces it."""
    clean = url_path.strip("/")
    if not clean:
        return DOCS_ROOT / "docs" / "index.md"
    candidates = [
        DOCS_ROOT / "docs" / f"{clean}.md",
        DOCS_ROOT / "docs" / clean / "index.md",
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def rewrite_links(
    text: str,
    source: str,
    anchors: dict[str, dict[str, str]],
    errors: list[str],
) -> str:
    def replace_anchor(match: re.Match[str]) -> str:
        page, anchor = match.group("page"), match.group("anchor")
        target = page or source
        if target not in anchors:
            return match.group(0)
        translated = anchors[target].get(anchor)
        if translated is None:
            errors.append(f"{source}: {target} has no heading for #{anchor}")
            return match.group(0)
        return f"]({page}#{translated})"

    def replace_site(match: re.Match[str]) -> str:
        url_path, anchor = match.group(1), match.group(2) or ""
        page = resolve_site_page(url_path)
        if page is None:
            errors.append(f"{source}: no page for {match.group(0)}")
            return match.group(0)
        relative = PurePosixPath(os.path.relpath(page, TARGET_DIR).replace(os.sep, "/"))
        return f"{relative}{anchor}"

    def replace_repo(match: re.Match[str]) -> str:
        return f"]({UPSTREAM_BLOB}/{match.group(1)})"

    # Repo links first: rewriting site links produces relative `../` links of
    # exactly the shape REPO_LINK matches, and they must not be caught by it.
    text = SITE_LINK.sub(replace_site, REPO_LINK.sub(replace_repo, text))
    return ANCHORED_LINK.sub(replace_anchor, text)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "source",
        type=Path,
        help="path to an nsclient-fleet-server checkout (or its docs/ directory)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="do not write, only report whether the copies are up to date",
    )
    args = parser.parse_args()

    source = args.source.resolve()
    if (source / "docs").is_dir():
        source = source / "docs"
    if not source.is_dir():
        parser.error(f"{source} is not a directory")

    errors: list[str] = []
    stale: list[str] = []
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    sources: dict[str, str] = {}
    for upstream_name in PAGES:
        upstream = source / upstream_name
        if not upstream.is_file():
            errors.append(f"missing upstream page: {upstream}")
            continue
        sources[upstream_name] = upstream.read_text(encoding="utf-8")

    # Anchors of every page in the set, so a link into another one can be
    # translated and checked without reading that page again per link.
    anchors = {name: anchor_map(text) for name, text in sources.items()}

    for upstream_name, page_name in PAGES.items():
        text = sources.get(upstream_name)
        if text is None:
            continue

        text = BANNER.format(source=upstream_name) + "\n" + rewrite_links(
            text, upstream_name, anchors, errors
        )

        target = TARGET_DIR / page_name
        current = target.read_text(encoding="utf-8") if target.is_file() else None
        if current == text:
            print(f"unchanged  {target.relative_to(REPO_ROOT)}")
            continue

        if args.check:
            stale.append(str(target.relative_to(REPO_ROOT)))
            continue

        target.write_text(text, encoding="utf-8", newline="\n")
        print(f"{'updated   ' if current else 'created   '}{target.relative_to(REPO_ROOT)}")

    for error in errors:
        print(f"error: {error}", file=sys.stderr)
    for path in stale:
        print(f"out of date: {path}", file=sys.stderr)

    if errors or stale:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
