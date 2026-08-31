#!/usr/bin/env python3
"""Copy the check_nsclient user documentation into this site.

The pages in `docs/docs/check_nsclient/` are **generated** — they are owned by
https://github.com/mickem/check_nsclient (`docs/*.md` there) and copied here so
they are published together with the agent documentation. Edit them upstream,
then re-run this script:

    python scripts/sync-check-nsclient-docs.py ../check_nsclient

The only transformation applied is link rewriting: upstream links out to the
site with absolute `https://nsclient.org/docs/...` URLs so they work when the
files are read in their own repository. Here the same targets are local pages,
so they are turned into relative links, which lets mkdocs validate them and
keeps them working when the site is built for a preview or a subdirectory.

Every rewritten link is resolved against the files on disk; an URL that points
at a page which does not exist is reported and the script exits non-zero rather
than publishing a dead link.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path, PurePosixPath

# Upstream file -> page name in docs/docs/check_nsclient/
PAGES = {
    "index.md": "index.md",
    "nsclient.md": "nsclient.md",
    "profile.md": "profile.md",
}

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_ROOT = REPO_ROOT / "docs"
TARGET_DIR = DOCS_ROOT / "docs" / "check_nsclient"

# https://nsclient.org/docs/reference/index.html style links back into this site.
SITE_LINK = re.compile(r"https://nsclient\.org/docs/([^)\s#]*)(#[^)\s]*)?")

BANNER = """<!--
  This page is generated. It is maintained in the check_nsclient repository:
  https://github.com/mickem/check_nsclient/blob/main/docs/{source}
  Run scripts/sync-check-nsclient-docs.py to refresh it; edits made here are
  overwritten.
-->
"""


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


def rewrite_links(text: str, source: str, errors: list[str]) -> str:
    def replace(match: re.Match[str]) -> str:
        url_path, anchor = match.group(1), match.group(2) or ""
        page = resolve_site_page(url_path)
        if page is None:
            errors.append(f"{source}: no page for https://nsclient.org/docs/{url_path}")
            return match.group(0)
        relative = PurePosixPath(os.path.relpath(page, TARGET_DIR).replace(os.sep, "/"))
        return f"{relative}{anchor}"

    return SITE_LINK.sub(replace, text)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "source",
        type=Path,
        help="path to a check_nsclient checkout (or its docs/ directory)",
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

    for upstream_name, page_name in PAGES.items():
        upstream = source / upstream_name
        if not upstream.is_file():
            errors.append(f"missing upstream page: {upstream}")
            continue

        text = upstream.read_text(encoding="utf-8")
        text = BANNER.format(source=upstream_name) + "\n" + rewrite_links(
            text, upstream_name, errors
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
