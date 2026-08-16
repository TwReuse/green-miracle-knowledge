#!/usr/bin/env python3
"""Build and audit the rendered Green Miracle public MkDocs site."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import urljoin, urlparse
import xml.etree.ElementTree as ET

import yaml


SEVERITY_ORDER = {"critical": 0, "major": 1, "minor": 2}


@dataclass(frozen=True)
class Finding:
    severity: str
    rule: str
    subject: str
    message: str
    recommendation: str


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.lang = ""
        self.metas: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []
        self.headings: list[int] = []
        self.json_ld: list[str] = []
        self._div_depth = 0
        self._main_div_depth: int | None = None
        self._in_main_tag = False
        self._in_title = False
        self._in_json_ld = False
        self._json_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value or "" for key, value in attrs}
        tag = tag.lower()
        if tag == "html":
            self.lang = values.get("lang", "")
        elif tag == "div":
            self._div_depth += 1
            if values.get("role") == "main":
                self._main_div_depth = self._div_depth
        elif tag == "main":
            self._in_main_tag = True
        elif tag == "title":
            self._in_title = True
        elif tag == "meta":
            self.metas.append(values)
        elif tag == "link":
            self.links.append(values)
        elif re.fullmatch(r"h[1-6]", tag) and (self._main_div_depth is not None or self._in_main_tag):
            self.headings.append(int(tag[1]))
        elif tag == "script" and values.get("type", "").lower() == "application/ld+json":
            self._in_json_ld = True
            self._json_parts = []

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self._in_title = False
        elif tag == "div":
            if self._main_div_depth == self._div_depth:
                self._main_div_depth = None
            self._div_depth = max(0, self._div_depth - 1)
        elif tag == "main":
            self._in_main_tag = False
        elif tag == "script" and self._in_json_ld:
            self.json_ld.append("".join(self._json_parts).strip())
            self._in_json_ld = False
            self._json_parts = []

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data
        if self._in_json_ld:
            self._json_parts.append(data)

    def meta(self, key: str, value: str) -> list[str]:
        return [item.get("content", "").strip() for item in self.metas if item.get(key) == value]

    def canonical(self) -> list[str]:
        return [
            item.get("href", "").strip()
            for item in self.links
            if "canonical" in item.get("rel", "").lower().split()
        ]


def add(
    findings: list[Finding],
    severity: str,
    rule: str,
    subject: str,
    message: str,
    recommendation: str,
) -> None:
    findings.append(Finding(severity, rule, subject, message, recommendation))


def parse_frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    match = re.match(r"\A---\s*\r?\n(.*?)\r?\n---\s*(?:\r?\n|\Z)", text, re.S)
    if not match:
        return {}
    try:
        value = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}
    return value if isinstance(value, dict) else {}


def source_for_html(docs_dir: Path, relative_html: Path) -> Path:
    if relative_html.as_posix() == "index.html":
        return docs_dir / "index.md"
    if relative_html.name == "index.html":
        return docs_dir / relative_html.parent.with_suffix(".md")
    return docs_dir / relative_html.with_suffix(".md")


def expected_url(site_url: str, relative_html: Path) -> str:
    if relative_html.as_posix() == "index.html":
        route = ""
    elif relative_html.name == "index.html":
        route = relative_html.parent.as_posix().strip("/") + "/"
    else:
        route = relative_html.with_suffix("").as_posix()
    return urljoin(site_url.rstrip("/") + "/", route)


def validate_json_ld(
    parser: PageParser,
    canonical: str,
    title: str,
    description: str,
    subject: str,
    findings: list[Finding],
) -> None:
    if not parser.json_ld:
        add(findings, "major", "JSON_LD_MISSING", subject, "缺少 JSON-LD。", "輸出與可見內容一致的 WebPage 結構化資料。")
        return

    objects: list[dict[str, object]] = []
    for raw in parser.json_ld:
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as error:
            add(findings, "major", "JSON_LD_INVALID", subject, f"JSON-LD 無效：{error}", "修正 JSON 語法。")
            continue
        candidates = payload if isinstance(payload, list) else [payload]
        for candidate in candidates:
            if not isinstance(candidate, dict):
                continue
            graph = candidate.get("@graph")
            if isinstance(graph, list):
                objects.extend(item for item in graph if isinstance(item, dict))
            else:
                objects.append(candidate)

    web_pages = [item for item in objects if item.get("@type") == "WebPage"]
    if not web_pages:
        add(findings, "major", "WEBPAGE_SCHEMA_MISSING", subject, "JSON-LD 缺少 WebPage。", "加入與頁面 metadata 一致的 WebPage。")
        return
    page = web_pages[0]
    if page.get("url") != canonical:
        add(findings, "major", "SCHEMA_URL_MISMATCH", subject, "WebPage.url 與 canonical 不一致。", "使用頁面 canonical。")
    if page.get("name") != title:
        add(findings, "minor", "SCHEMA_NAME_MISMATCH", subject, "WebPage.name 與 SEO title 不一致。", "使用同一個核准標題來源。")
    if page.get("description") != description:
        add(findings, "minor", "SCHEMA_DESCRIPTION_MISMATCH", subject, "WebPage.description 與 meta description 不一致。", "使用同一個核准摘要來源。")


def audit(repo: Path, config_path: Path, site_dir: Path) -> tuple[dict[str, object], list[Finding]]:
    findings: list[Finding] = []
    config = yaml.safe_load(config_path.read_text(encoding="utf-8-sig")) or {}
    docs_dir = repo / str(config.get("docs_dir", "docs"))
    site_url = str(config.get("site_url", "")).strip()

    result = subprocess.run(
        [sys.executable, "-m", "mkdocs", "build", "--strict", "--config-file", str(config_path), "--site-dir", str(site_dir)],
        cwd=repo,
        text=True,
        capture_output=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        add(findings, "critical", "STRICT_BUILD_FAILED", str(config_path), "MkDocs strict build 失敗。", result.stdout + result.stderr)
        return {"build_passed": False, "pages": 0, "sitemap_urls": 0}, findings

    rows: list[dict[str, object]] = []
    for html_path in sorted(site_dir.rglob("index.html")):
        relative = html_path.relative_to(site_dir)
        subject = relative.as_posix()
        parser = PageParser()
        parser.feed(html_path.read_text(encoding="utf-8", errors="replace"))
        title = " ".join(parser.title.split())
        descriptions = parser.meta("name", "description")
        canonicals = parser.canonical()
        canonical = canonicals[0] if len(canonicals) == 1 else ""
        description = descriptions[0] if len(descriptions) == 1 else ""
        expected = expected_url(site_url, relative)
        source_path = source_for_html(docs_dir, relative)
        metadata = parse_frontmatter(source_path) if source_path.exists() else {}

        if not title:
            add(findings, "major", "TITLE_MISSING", subject, "缺少 HTML title。", "設定頁面 title。")
        elif len(title) > 70:
            add(findings, "minor", "TITLE_LONG", subject, f"title 長度為 {len(title)}。", "縮短並保留主要搜尋意圖。")
        if len(descriptions) != 1 or not description:
            add(findings, "major", "DESCRIPTION_INVALID", subject, "meta description 缺少、空白或重複輸出。", "為頁面設定唯一摘要。")
        elif len(description) < 30 or len(description) > 160:
            add(findings, "minor", "DESCRIPTION_LENGTH", subject, f"description 長度為 {len(description)}。", "確認摘要完整、具體且適合搜尋結果閱讀。")
        if len(canonicals) != 1:
            add(findings, "major", "CANONICAL_INVALID", subject, "canonical 缺少或重複輸出。", "每頁只輸出一個 canonical。")
        elif canonical != expected:
            add(findings, "major", "CANONICAL_MISMATCH", subject, f"canonical 應為 {expected}。", "修正正式 HTTPS 路徑。")
        if parser.lang not in {"zh_TW", "zh-TW", "zh_Hant_TW", "zh-Hant-TW"}:
            add(findings, "minor", "LANG_INVALID", subject, f"html lang 為 {parser.lang or '空白'}。", "設定繁體中文語系。")
        if parser.headings.count(1) != 1:
            add(findings, "major", "H1_COUNT", subject, f"H1 數量為 {parser.headings.count(1)}。", "每頁保留一個 H1。")
        for previous, current in zip(parser.headings, parser.headings[1:]):
            if current > previous + 1:
                add(findings, "minor", "HEADING_JUMP", subject, f"標題層級從 H{previous} 跳到 H{current}。", "依序使用標題層級。")
                break

        required_meta = [
            ("property", "og:title"),
            ("property", "og:description"),
            ("property", "og:url"),
            ("property", "og:site_name"),
            ("name", "twitter:card"),
            ("name", "twitter:title"),
            ("name", "twitter:description"),
        ]
        for key, value in required_meta:
            if len(parser.meta(key, value)) != 1:
                add(findings, "major", "SOCIAL_META_MISSING", subject, f"{value} 缺少或重複。", "由核准的 title、description 與 canonical 統一輸出。")

        if parser.meta("property", "og:title") != ([str(metadata.get("title"))] if metadata.get("title") else []):
            add(findings, "minor", "OG_TITLE_SOURCE", subject, "og:title 未沿用 frontmatter title。", "統一使用頁面 title。")
        if parser.meta("property", "og:description") != descriptions:
            add(findings, "minor", "OG_DESCRIPTION_MISMATCH", subject, "og:description 與 meta description 不一致。", "統一摘要來源。")
        if parser.meta("property", "og:url") != canonicals:
            add(findings, "minor", "OG_URL_MISMATCH", subject, "og:url 與 canonical 不一致。", "統一正式網址來源。")

        if not metadata.get("title") or not metadata.get("description"):
            add(findings, "major", "FRONTMATTER_SEO_MISSING", str(source_path.relative_to(repo)), "frontmatter 缺少 title 或 description。", "補上逐頁核准的搜尋標題與摘要。")
        if metadata.get("public") is not True or metadata.get("status") != "approved":
            add(findings, "major", "UNAPPROVED_PUBLIC_PAGE", str(source_path.relative_to(repo)), "建置頁面未同時符合 public: true 與 status: approved。", "完成核定或排除公開建置。")

        validate_json_ld(parser, canonical, str(metadata.get("title", "")), description, subject, findings)
        rows.append({"page": subject, "source": str(source_path.relative_to(repo)), "title": title, "description": description, "canonical": canonical})

    for field in ("title", "description", "canonical"):
        values = [str(row[field]) for row in rows if row[field]]
        for value, count in Counter(values).items():
            if count > 1:
                add(findings, "major", f"DUPLICATE_{field.upper()}", value, f"{field} 重複 {count} 次。", "為每頁設定唯一搜尋呈現。")

    sitemap_path = site_dir / "sitemap.xml"
    sitemap_urls: set[str] = set()
    if not sitemap_path.exists():
        add(findings, "major", "SITEMAP_MISSING", "sitemap.xml", "建置輸出缺少 sitemap。", "在站點根目錄產生 sitemap。")
    else:
        try:
            root = ET.parse(sitemap_path).getroot()
            sitemap_urls = {(node.text or "").strip() for node in root.findall(".//{*}loc") if (node.text or "").strip()}
        except ET.ParseError as error:
            add(findings, "major", "SITEMAP_INVALID", "sitemap.xml", f"sitemap XML 無效：{error}", "修正 sitemap。")
    canonical_urls = {str(row["canonical"]) for row in rows if row["canonical"]}
    if sitemap_urls != canonical_urls:
        add(findings, "major", "SITEMAP_SET_MISMATCH", "sitemap.xml", "sitemap URL 集合與公開 canonical 集合不一致。", "只列出所有核准公開頁的 canonical。")
    for url in sitemap_urls:
        if urlparse(url).scheme != "https":
            add(findings, "major", "SITEMAP_NOT_HTTPS", url, "sitemap 含非 HTTPS URL。", "改用正式 HTTPS canonical。")

    robots_path = site_dir / "robots.txt"
    if not robots_path.exists():
        add(findings, "major", "ROBOTS_MISSING", "robots.txt", "建置輸出缺少 robots.txt。", "建立爬取規則並指向 sitemap。")
    else:
        robots = robots_path.read_text(encoding="utf-8-sig", errors="replace")
        expected_sitemap = urljoin(site_url.rstrip("/") + "/", "sitemap.xml")
        if not re.search(r"(?im)^User-agent\s*:\s*\*\s*$", robots):
            add(findings, "major", "ROBOTS_USER_AGENT", "robots.txt", "缺少 User-agent: *。", "加入公開爬蟲規則。")
        if not re.search(rf"(?im)^Sitemap\s*:\s*{re.escape(expected_sitemap)}\s*$", robots):
            add(findings, "major", "ROBOTS_SITEMAP", "robots.txt", "Sitemap 宣告與 site_url 不一致。", f"設定 Sitemap: {expected_sitemap}")

    return {"build_passed": True, "pages": len(rows), "sitemap_urls": len(sitemap_urls), "rows": rows}, findings


def render_report(summary: dict[str, object], findings: list[Finding]) -> str:
    counts = Counter(item.severity for item in findings)
    lines = [
        "# 綠色奇蹟 SEO 稽核報告",
        "",
        "## 結論",
        "",
        f"- Strict build：{'通過' if summary.get('build_passed') else '失敗'}",
        f"- 頁面：{summary.get('pages', 0)}；sitemap：{summary.get('sitemap_urls', 0)}",
        f"- Findings：critical {counts['critical']}、major {counts['major']}、minor {counts['minor']}",
        "",
        "## Findings",
        "",
    ]
    if not findings:
        lines.append("沒有發現腳本可判定的問題；內容核定、Search Console 與正式站收錄仍須分別確認。")
    else:
        for item in sorted(findings, key=lambda value: (SEVERITY_ORDER[value.severity], value.rule, value.subject)):
            lines.extend([
                f"### [{item.severity.upper()}] {item.rule} — `{item.subject}`",
                "",
                item.message,
                "",
                f"建議：{item.recommendation}",
                "",
            ])
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".")
    parser.add_argument("--config", default="mkdocs.yml")
    parser.add_argument("--site-dir", default="build/seo-audit/site")
    parser.add_argument("--output")
    parser.add_argument("--json-output")
    parser.add_argument("--fail-on", choices=tuple(SEVERITY_ORDER), default="major")
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    config = (repo / args.config).resolve()
    site_dir = (repo / args.site_dir).resolve()
    summary, findings = audit(repo, config, site_dir)
    report = render_report(summary, findings)
    print(report, end="")

    if args.output:
        path = (repo / args.output).resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(report, encoding="utf-8")
    if args.json_output:
        path = (repo / args.json_output).resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps({"summary": summary, "findings": [asdict(item) for item in findings]}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    threshold = SEVERITY_ORDER[args.fail_on]
    return 1 if any(SEVERITY_ORDER[item.severity] <= threshold for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
