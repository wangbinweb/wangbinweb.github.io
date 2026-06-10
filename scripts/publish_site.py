#!/usr/bin/env python3
import argparse
import html
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


ROOT = Path(__file__).resolve().parents[1]
MD_DIR = ROOT / "md"
HTM_DIR = ROOT / "htm"
STYLE_PATH = ROOT / "stylesheets" / "site.css"
RECENT_COUNT = 12
SITE_TITLE = "王斌的网站"
SITE_SUBTITLE = "随手记录一些乱七八糟的东西。"


@dataclass
class Post:
    slug: str
    date: str
    title: str
    content_html: str

    @property
    def year(self) -> str:
        return self.date[:4]

    @property
    def url(self) -> str:
        return f"htm/{self.slug}.htm"

    @property
    def display_date(self) -> str:
        if len(self.date) == 8 and self.date.isdigit():
            return f"{self.date[:4]}.{self.date[4:6]}.{self.date[6:]}"
        return self.date


STYLE = """:root {
  color-scheme: light;
  --page: #f8f6f1;
  --ink: #24221f;
  --muted: #77716a;
  --line: #e6ded2;
  --accent: #735845;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  color: var(--ink);
  background: var(--page);
  font-family: Georgia, "Times New Roman", "Songti SC", "SimSun", serif;
  line-height: 1.75;
  -webkit-font-smoothing: antialiased;
}

a {
  color: inherit;
  text-decoration: none;
}

a:hover {
  color: var(--accent);
}

img {
  max-width: 100%;
  height: auto;
}

pre {
  overflow-x: auto;
  padding: 18px 20px;
  background: rgba(255, 255, 255, .45);
  border: 1px solid var(--line);
}

code {
  font-family: "Courier New", monospace;
  font-size: .92em;
}

blockquote {
  margin: 28px 0;
  padding-left: 22px;
  color: var(--muted);
  border-left: 2px solid var(--soft, #d9d2c7);
}

.site-header,
.page-shell,
.site-footer {
  width: min(1120px, calc(100% - 48px));
  margin-inline: auto;
}

.site-header {
  padding: 56px 0 34px;
  border-bottom: 1px solid var(--line);
}

.site-title {
  display: inline-block;
  font-size: 28px;
  line-height: 1.2;
}

.site-header p {
  max-width: 520px;
  margin: 12px 0 0;
  color: var(--muted);
  font-size: 15px;
}

.page-shell {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 320px;
  gap: 72px;
  padding: 58px 0 64px;
}

.page-shell.single {
  display: block;
  max-width: 820px;
}

.content {
  max-width: 700px;
}

.content.single {
  max-width: 760px;
  margin-inline: auto;
}

.content.archive {
  max-width: 820px;
  margin-inline: auto;
}

.eyebrow,
.content time {
  color: var(--accent);
  font-size: 13px;
  letter-spacing: .08em;
}

.content time {
  display: block;
  margin-bottom: 12px;
  color: var(--muted);
  letter-spacing: 0;
}

.content h1 {
  margin: 0 0 30px;
  font-size: clamp(34px, 5vw, 58px);
  font-weight: 400;
  line-height: 1.16;
}

.content h2,
.content h3,
.content h4 {
  margin: 34px 0 16px;
  font-weight: 400;
  line-height: 1.35;
}

.content p {
  margin: 0 0 22px;
  font-size: 18px;
}

.read-more,
.back-link {
  display: inline-flex;
  margin-top: 16px;
  padding-bottom: 4px;
  color: var(--accent);
  border-bottom: 1px solid currentColor;
  font-size: 15px;
}

.post-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 18px 28px;
  margin-top: 16px;
}

.post-actions .back-link {
  margin-top: 0;
}

.archive-heading {
  margin: 0 0 28px;
  font-size: clamp(32px, 4vw, 48px);
  font-weight: 400;
  line-height: 1.2;
}

.archive-posts {
  list-style: none;
  margin: 0;
  padding: 0;
}

.archive-posts li {
  border-top: 1px solid var(--line);
}

.archive-posts a {
  display: grid;
  grid-template-columns: 96px minmax(0, 1fr);
  gap: 22px;
  padding: 18px 0;
}

.archive-posts time {
  color: var(--muted);
  font-size: 14px;
}

.sidebar {
  border-left: 1px solid var(--line);
  padding-left: 32px;
}

.side-section + .side-section {
  margin-top: 44px;
}

.side-section h2 {
  margin: 0 0 18px;
  color: var(--accent);
  font-size: 14px;
  font-weight: 400;
  letter-spacing: .12em;
}

.post-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.post-list li + li {
  border-top: 1px solid var(--line);
}

.post-list a {
  display: grid;
  grid-template-columns: 68px minmax(0, 1fr);
  gap: 14px;
  padding: 12px 0;
}

.post-list time {
  color: var(--muted);
  font-size: 12px;
  line-height: 1.5;
}

.post-list span {
  font-size: 14px;
  line-height: 1.55;
}

.archive-list {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px 18px;
}

.archive-list a {
  color: var(--muted);
  font-size: 14px;
}

.site-footer {
  display: flex;
  flex-wrap: wrap;
  gap: 12px 24px;
  padding: 26px 0 46px;
  border-top: 1px solid var(--line);
  color: var(--muted);
  font-size: 14px;
}

@media (max-width: 820px) {
  .site-header,
  .page-shell,
  .site-footer {
    width: min(100% - 28px, 680px);
  }

  .site-header {
    padding-top: 34px;
  }

  .page-shell {
    grid-template-columns: 1fr;
    gap: 44px;
    padding-top: 38px;
  }

  .page-shell.single {
    max-width: min(100% - 28px, 680px);
  }

  .content p {
    font-size: 16px;
  }

  .archive-posts a {
    grid-template-columns: 1fr;
    gap: 4px;
  }

  .sidebar {
    border-left: 0;
    border-top: 1px solid var(--line);
    padding: 34px 0 0;
  }
}
"""


def clean_text(value: str) -> str:
    return re.sub(r"\s+", " ", strip_tags(value)).strip()


def strip_tags(value: str) -> str:
    return re.sub(r"<[^>]+>", "", value)


def normalize_date(value: str) -> str:
    value = clean_text(value)
    match = re.search(r"(\d{4})\D*(\d{1,2})\D*(\d{1,2})", value)
    if match:
        year, month, day = match.groups()
        return f"{year}{int(month):02d}{int(day):02d}"
    match = re.search(r"(\d{8})", value)
    if match:
        return match.group(1)
    raise ValueError(f"Cannot parse date: {value}")


def slugify_title(title: str) -> str:
    text = re.sub(r"<[^>]+>", "", title).strip().lower()
    text = re.sub(r"[^\w\u4e00-\u9fff]+", "-", text)
    return text.strip("-") or "post"


def extract_tag(text: str, tag: str) -> Optional[str]:
    match = re.search(rf"\[{tag}\]\s*([\s\S]+?)\s*\[/{tag}\]", text)
    return match.group(1).strip() if match else None


def split_metadata(raw: str, path: Path) -> tuple[str, str, str, str]:
    filename = extract_tag(raw, "FileName")
    date = extract_tag(raw, "Time")
    title = extract_tag(raw, "Title")
    content = extract_tag(raw, "Content")
    if filename and date and title and content:
        return filename, normalize_date(date), clean_text(title), content.strip()

    lines = raw.splitlines()
    first_date = None
    first_title = None
    content_start = 0
    for index, line in enumerate(lines[:12]):
        stripped = line.strip()
        if stripped.startswith("####") and first_date is None:
            first_date = normalize_date(stripped.lstrip("#").strip())
            content_start = max(content_start, index + 1)
        elif stripped.startswith("##") and first_title is None:
            first_title = stripped.lstrip("#").strip()
            content_start = max(content_start, index + 1)

    if not first_date or not first_title:
        raise ValueError(f"Missing date/title metadata in {path}")

    return path.stem, first_date, clean_text(first_title), "\n".join(lines[content_start:]).strip()


def parse_reference_links(text: str) -> tuple[str, dict[str, tuple[str, str]]]:
    refs: dict[str, tuple[str, str]] = {}
    kept_lines: list[str] = []
    ref_pattern = re.compile(r'^\[([^\]]+)\]:\s*(\S+)(?:\s+title="([^"]+)")?\s*$')
    for line in text.splitlines():
        match = ref_pattern.match(line.strip())
        if match:
            key, url, title = match.groups()
            refs[key] = (url, title or "")
        else:
            kept_lines.append(line)
    return "\n".join(kept_lines), refs


def convert_inline(text: str, refs: dict[str, tuple[str, str]]) -> str:
    escaped = html.escape(text, quote=False)

    def replace_ref(match: re.Match[str]) -> str:
        label, key = match.groups()
        url, title = refs.get(key, ("", ""))
        if not url:
            return match.group(0)
        title_attr = f' title="{html.escape(title)}"' if title else ""
        return f'<a href="{html.escape(url, quote=True)}"{title_attr}>{label}</a>'

    def replace_inline(match: re.Match[str]) -> str:
        label, url = match.groups()
        return f'<a href="{html.escape(url, quote=True)}">{label}</a>'

    escaped = re.sub(r"\[([^\]]+)\]\[([^\]]+)\]", replace_ref, escaped)
    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", replace_inline, escaped)
    return escaped


def markdown_to_html(text: str) -> str:
    if re.search(r"<(p|h\d|pre|ul|ol|blockquote|img|table|div|br)\b", text):
        return drop_duplicate_title_paragraph(text.strip(), "")

    text, refs = parse_reference_links(text)
    blocks: list[str] = []
    paragraph: list[str] = []
    code: list[str] = []
    in_code = False

    def flush_paragraph() -> None:
        if paragraph:
            blocks.append(f"<p>{convert_inline(' '.join(paragraph), refs)}</p>")
            paragraph.clear()

    for line in text.splitlines():
        stripped = line.rstrip()
        if stripped.startswith("```"):
            if in_code:
                blocks.append(f"<pre><code>{html.escape(chr(10).join(code))}</code></pre>")
                code.clear()
                in_code = False
            else:
                flush_paragraph()
                in_code = True
            continue
        if in_code:
            code.append(stripped)
            continue
        if not stripped.strip():
            flush_paragraph()
            continue
        if stripped.startswith("#"):
            flush_paragraph()
            level = min(len(stripped) - len(stripped.lstrip("#")), 4)
            heading = stripped.lstrip("#").strip()
            blocks.append(f"<h{level}>{convert_inline(heading, refs)}</h{level}>")
            continue
        if stripped.startswith(">"):
            flush_paragraph()
            quote = stripped.lstrip(">").strip()
            blocks.append(f"<blockquote>{convert_inline(quote, refs)}</blockquote>")
            continue
        paragraph.append(stripped.strip())

    flush_paragraph()
    if in_code and code:
        blocks.append(f"<pre><code>{html.escape(chr(10).join(code))}</code></pre>")
    return "\n".join(blocks)


def drop_duplicate_title_paragraph(content: str, title: str) -> str:
    if not title:
        return content
    title_text = clean_text(title)
    pattern = re.compile(r"^\s*<p>(.*?)</p>\s*", re.S)
    match = pattern.match(content)
    if match and clean_text(match.group(1)) == title_text:
        return content[match.end():].lstrip()
    return content


def parse_md_post(path: Path) -> Post:
    raw = path.read_text(encoding="utf-8")
    slug, date, title, content = split_metadata(raw, path)
    content_html = markdown_to_html(content)
    content_html = drop_duplicate_title_paragraph(content_html, title)
    return Post(slug=slug, date=date, title=title, content_html=content_html)


def parse_html_post(path: Path) -> Post:
    raw = path.read_text(encoding="utf-8")
    slug = path.stem.removeprefix("old-")
    title_match = re.search(r"<h2[^>]*>([\s\S]*?)</h2>", raw)
    date_match = re.search(r"<h4[^>]*>([\s\S]*?)</h4>", raw)
    body_match = re.search(r'<div id="container">\s*[\s\S]*?</h2>([\s\S]*?)</div>\s*<nav', raw)
    if not title_match or not date_match or not body_match:
        raise ValueError(f"Cannot parse old HTML post: {path}")
    title = clean_text(title_match.group(1))
    date = normalize_date(date_match.group(1))
    content = drop_duplicate_title_paragraph(body_match.group(1).strip(), title)
    return Post(slug=slug, date=date, title=title, content_html=content)


def load_posts() -> list[Post]:
    posts_by_slug: dict[str, Post] = {}
    skipped_md: dict[str, str] = {}
    if MD_DIR.exists():
        for path in sorted(MD_DIR.glob("*.md")):
            try:
                post = parse_md_post(path)
                posts_by_slug[post.slug] = post
            except Exception as exc:
                skipped_md[path.stem] = f"Skip {path}: {exc}"

    if HTM_DIR.exists():
        for path in sorted(HTM_DIR.glob("old-*.htm")) + sorted(HTM_DIR.glob("*.htm")):
            slug = path.stem.removeprefix("old-")
            if slug in posts_by_slug:
                continue
            try:
                posts_by_slug[slug] = parse_html_post(path)
            except Exception as exc:
                print(f"Skip {path}: {exc}")

    for slug, message in skipped_md.items():
        if slug not in posts_by_slug:
            print(message)

    return sorted(posts_by_slug.values(), key=lambda post: (post.date, post.slug), reverse=True)


def archive_old_html() -> None:
    for path in sorted(ROOT.rglob("*.htm")) + sorted(ROOT.rglob("*.html")):
        if ".git" in path.parts:
            continue
        if path.name.startswith("old-"):
            continue
        old_path = path.with_name(f"old-{path.name}")
        if old_path.exists():
            continue
        path.rename(old_path)


def sidebar(posts: list[Post], current_slug: Optional[str] = None) -> str:
    recent_items = "\n".join(
        f'          <li><a href="{relative_url(post.url, current_slug)}"><time>{post.date}</time><span>{html.escape(post.title)}</span></a></li>'
        for post in posts[:RECENT_COUNT]
    )
    archive_items = "\n".join(
        f'          <a href="{relative_url(f"{year}index.htm", current_slug)}">{year if year != "2014" else "2014 与以前"}</a>'
        for year in archive_years(posts)
    )
    return f"""    <aside class="sidebar" aria-label="文章导航">
      <section class="side-section">
        <h2>近日</h2>
        <ol class="post-list">
{recent_items}
        </ol>
      </section>

      <section class="side-section">
        <h2>归档</h2>
        <nav class="archive-list" aria-label="年份归档">
{archive_items}
        </nav>
      </section>
    </aside>"""


def archive_years(posts: list[Post]) -> list[str]:
    years = sorted({post.year if int(post.year) > 2014 else "2014" for post in posts}, reverse=True)
    return years


def relative_url(url: str, current_slug: Optional[str]) -> str:
    if current_slug and not url.startswith(("http://", "https://", "mailto:")):
        return "../" + url
    return url


def footer() -> str:
    return """  <footer class="site-footer">
    <a href="http://heimaphoto.com" target="_blank">黑马摄影</a>
  </footer>"""


def page(
    title: str,
    body: str,
    posts: list[Post],
    current_slug: Optional[str] = None,
    include_sidebar: bool = True,
    shell_class: str = "page-shell",
) -> str:
    home_url = "../index.html" if current_slug else "index.html"
    css_url = "../stylesheets/site.css" if current_slug else "stylesheets/site.css"
    sidebar_html = f"\n{sidebar(posts, current_slug)}" if include_sidebar else ""
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="chrome=1">
  <meta name="description" content="Wangbinweb.GitHub.io : 王斌的博客网站">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" type="text/css" media="screen" href="{css_url}">
  <title>{html.escape(title)}</title>
</head>
<body>
  <header class="site-header">
    <a class="site-title" href="{home_url}">{SITE_TITLE}</a>
    <p>{SITE_SUBTITLE}</p>
  </header>

  <main class="{shell_class}">
{body}
{sidebar_html}
  </main>

{footer()}
</body>
</html>
"""


def excerpt_html(post: Post) -> str:
    if "<!--more-->" in post.content_html:
        return post.content_html.split("<!--more-->", 1)[0].strip()
    paragraphs = re.findall(r"<p>[\s\S]*?</p>", post.content_html)
    if paragraphs:
        return "\n".join(paragraphs[:2])
    return post.content_html


def render_index(posts: list[Post]) -> str:
    latest = posts[0]
    body = f"""    <article class="content">
      <p class="eyebrow">最近文章</p>
      <time datetime="{latest.date}">{latest.display_date}</time>
      <h1>{html.escape(latest.title)}</h1>
{indent(excerpt_html(latest), 6)}
      <a class="read-more" href="{latest.url}">继续阅读</a>
    </article>
"""
    return page(SITE_TITLE, body, posts)


def render_post(post: Post, posts: list[Post]) -> str:
    body = f"""    <article class="content single">
      <time datetime="{post.date}">{post.display_date}</time>
      <h1>{html.escape(post.title)}</h1>
{indent(post.content_html, 6)}
      <nav class="post-actions" aria-label="文章导航">
        <a class="back-link" href="../index.html">回主页</a>
        <a class="back-link" href="https://www.douban.com/group/514220/" target="_blank">留言板</a>
      </nav>
    </article>
"""
    return page(post.title, body, posts, current_slug=post.slug, include_sidebar=False, shell_class="page-shell single")


def render_archive(year: str, year_posts: list[Post], posts: list[Post]) -> str:
    label = "2014 与以前" if year == "2014" else year
    items = "\n".join(
        f'        <li><a href="{post.url}"><time>{post.date}</time><span>{html.escape(post.title)}</span></a></li>'
        for post in year_posts
    )
    body = f"""    <section class="content archive">
      <h1 class="archive-heading">{label}</h1>
      <ol class="archive-posts">
{items}
      </ol>
      <a class="back-link" href="index.html">回到首页</a>
    </section>
"""
    return page(f"{label} - {SITE_TITLE}", body, posts, include_sidebar=False, shell_class="page-shell single")


def indent(text: str, spaces: int) -> str:
    prefix = " " * spaces
    return "\n".join(prefix + line if line else line for line in text.splitlines())


def rebuild(archive_old: bool = False) -> None:
    if archive_old:
        archive_old_html()
    HTM_DIR.mkdir(exist_ok=True)
    STYLE_PATH.parent.mkdir(exist_ok=True)
    STYLE_PATH.write_text(STYLE, encoding="utf-8")
    posts = load_posts()
    if not posts:
        raise SystemExit("No posts found.")
    (ROOT / "index.html").write_text(render_index(posts), encoding="utf-8")
    for post in posts:
        (HTM_DIR / f"{post.slug}.htm").write_text(render_post(post, posts), encoding="utf-8")
    for year in archive_years(posts):
        year_posts = [post for post in posts if (post.year if int(post.year) > 2014 else "2014") == year]
        (ROOT / f"{year}index.htm").write_text(render_archive(year, year_posts, posts), encoding="utf-8")
    print(f"Generated {len(posts)} posts, {len(archive_years(posts))} archives, and index.html.")


def publish(args: argparse.Namespace) -> None:
    date = normalize_date(args.date)
    title = args.title.strip()
    slug = args.slug or f"{date}-{slugify_title(title)}"
    if args.content_file:
        content = Path(args.content_file).read_text(encoding="utf-8")
    else:
        content = args.content.strip()
    if not content:
        raise SystemExit("Post content is empty.")
    post_path = MD_DIR / f"{slug}.md"
    MD_DIR.mkdir(exist_ok=True)
    post_text = f"#### {date}\n## {title}\n\n{content.rstrip()}\n"
    post_path.write_text(post_text, encoding="utf-8")
    print(f"Wrote {post_path.relative_to(ROOT)}")
    rebuild(archive_old=False)


def main() -> None:
    parser = argparse.ArgumentParser(description="Publish and rebuild wangbinweb static pages.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    rebuild_parser = subparsers.add_parser("rebuild")
    rebuild_parser.add_argument("--archive-old", action="store_true")

    publish_parser = subparsers.add_parser("publish")
    publish_parser.add_argument("--date", required=True)
    publish_parser.add_argument("--title", required=True)
    publish_parser.add_argument("--slug")
    publish_parser.add_argument("--content", default="")
    publish_parser.add_argument("--content-file")

    args = parser.parse_args()
    if args.command == "rebuild":
        rebuild(archive_old=args.archive_old)
    elif args.command == "publish":
        publish(args)


if __name__ == "__main__":
    main()
