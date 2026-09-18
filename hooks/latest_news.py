"""mkdocs hook: list the latest news posts on the home page.

The home page used to list the newest GitHub releases (fetched at build time
by hooks/fetch_releases.py and rendered by assets/js/latest-release.js). Every
release now gets a news post, so the home page lists the newest posts of the
blog plugin instead, and the release list only remains on /download/.

The hook replaces the ``<!-- latest-news -->`` marker in ``docs/index.md``
with plain HTML, one ``<article class="news-item">`` per post carrying its
title, date and first paragraph, inside ``<div class="news-list">``; the
classes are styled in ``stylesheets/extra.css`` next to the release list.

Posts come from the Material blog plugin, which has read every post's
metadata and computed its final URL by the time any page is rendered, so the
list needs no JavaScript and no copy of the blog's URL scheme. Drafts and
pinned posts follow the plugin's own rules: the home page shows the same
posts, in the same order, as the top of the news page.
"""

import html
import logging
import re
from datetime import date, datetime

from mkdocs.utils import get_relative_url

log = logging.getLogger("mkdocs.plugins.latest_news")

# Page (src_uri) carrying the marker, and the marker itself.
PAGE = "index.md"
MARKER = "<!-- latest-news -->"

# How many posts to list, and how long the summary of each may be.
COUNT = 3
SUMMARY_MAX = 200

# Where to send readers when no posts could be listed (relative to PAGE).
NEWS_URL = "news/"

# Block-level constructs that never make a good summary: headings, quotes,
# tables, raw HTML, images, admonitions, rules and list items.
_SKIP_BLOCK = re.compile(r"^(#|>|\||<|!|---|\*\*\*|- |\* |\+ |\d+\. |!!!|\?\?\?)")
# A line that is nothing but a link or a button, e.g. ``[All news](news/)``.
_LINK_ONLY = re.compile(r"^\[[^\]]*\]\([^)]*\)(\{[^}]*\})?$")
_HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$")
_FENCE = re.compile(r"^(```|~~~)")


def _blog_posts(config):
    """Return the blog plugin's posts, newest first, or an empty list."""
    plugins = config["plugins"]
    plugin = plugins.get("material/blog") or plugins.get("blog")
    if plugin is None:
        for candidate in plugins.values():
            if type(candidate).__name__ == "BlogPlugin":
                plugin = candidate
                break
    if plugin is None:
        log.warning("latest_news: the blog plugin is not enabled")
        return []
    try:
        return list(plugin.blog.posts)
    except AttributeError:
        log.warning("latest_news: the blog plugin has not resolved its posts yet")
        return []


def _created(post):
    """The post's creation date as a ``date``, or None."""
    try:
        created = post.config.date.created
    except AttributeError:
        return None
    if isinstance(created, datetime):
        return created.date()
    if isinstance(created, date):
        return created
    return None


def _blocks(markdown):
    """Split Markdown into blocks separated by blank lines (fences kept whole)."""
    block, in_fence = [], False
    for raw in (markdown or "").splitlines():
        line = raw.strip()
        if _FENCE.match(line):
            in_fence = not in_fence
            block.append(line)
            continue
        if in_fence:
            block.append(line)
            continue
        if not line:
            if block:
                yield block
                block = []
            continue
        block.append(line)
    if block:
        yield block


def _title(post):
    """The post's title: its first heading, else what mkdocs would use."""
    for block in _blocks(post.markdown):
        match = _HEADING.match(block[0])
        if match:
            return match.group(1)
    return post.title or post.file.name


def _first_paragraph(markdown):
    """The first block of running text in the Markdown, joined on one line."""
    for block in _blocks(markdown):
        # A heading directly followed by text (no blank line) is one block.
        while block and _HEADING.match(block[0]):
            block = block[1:]
        if not block:
            continue
        first = block[0]
        if _SKIP_BLOCK.match(first) or _LINK_ONLY.match(first) or _FENCE.match(first):
            continue
        return " ".join(block)
    return ""


def _plain(text):
    """Reduce inline Markdown to text, keeping backticks for ``_inline_html``."""
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)              # images
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)(\{[^}]*\})?", r"\1", text)  # links
    text = re.sub(r"\[([^\]]+)\]\[[^\]]*\]", r"\1", text)          # ref links
    text = re.sub(r"<(https?://[^>]+)>", r"\1", text)              # autolinks
    text = re.sub(r"(\*\*|__)(.+?)\1", r"\2", text)                # bold
    text = re.sub(r"(?<!\w)\*(?!\s)(.+?)(?<!\s)\*(?!\w)", r"\1", text)  # italic
    text = re.sub(r"(?<!\w)_(?!\s)(.+?)(?<!\s)_(?!\w)", r"\1", text)
    text = re.sub(r":(material|fontawesome|octicons|simple)-[a-z0-9_-]+:", "", text)
    return re.sub(r"\s+", " ", text).strip()


def _truncate(text, limit):
    """Cut text at a word boundary, never inside a code span."""
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0]
    if cut.count("`") % 2:
        cut = cut[: cut.rfind("`")]
    return cut.rstrip(" ,;:.") + "…"


def _inline_html(text):
    """Escape text for HTML and turn ``code`` spans into <code>."""
    text = html.escape(text, quote=False)
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", text)


def _summary(post):
    """The post's description, else its first paragraph, as inline HTML."""
    text = (post.meta or {}).get("description") or _first_paragraph(post.markdown)
    text = _plain(text)
    return _inline_html(_truncate(text, SUMMARY_MAX)) if text else ""


def _render(posts, page):
    lines = ['<div class="news-list">']
    for post in posts:
        url = html.escape(get_relative_url(post.url, page.url), quote=True)
        created = _created(post)
        lines.append('<article class="news-item">')
        lines.append('<div class="news-header">')
        lines.append(
            '<a class="news-title" href="%s">%s</a>'
            % (url, _inline_html(_plain(_title(post))))
        )
        if created:
            lines.append(
                '<time class="news-date" datetime="%s">%s %d, %d</time>'
                % (created.isoformat(), created.strftime("%b"), created.day, created.year)
            )
        lines.append("</div>")
        summary = _summary(post)
        if summary:
            lines.append('<p class="news-summary">%s</p>' % summary)
        lines.append("</article>")
    lines.append("</div>")
    return "\n".join(lines)


def _fallback():
    return (
        '<p class="news-loading">No news posts found. '
        '<a href="%s">See all news</a></p>' % NEWS_URL
    )


def on_page_markdown(markdown, page, config, files):
    if page.file.src_uri != PAGE or MARKER not in markdown:
        return markdown
    posts = _blog_posts(config)[:COUNT]
    if not posts:
        log.warning("latest_news: no posts to list on %s", PAGE)
        return markdown.replace(MARKER, _fallback())
    log.info("latest_news: listing %d posts on %s", len(posts), PAGE)
    return markdown.replace(MARKER, _render(posts, page))
