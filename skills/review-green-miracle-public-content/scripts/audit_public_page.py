#!/usr/bin/env python3
"""Run deterministic first-pass checks for Green Miracle public Markdown pages."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_FIELDS = (
    "doc_id",
    "status",
    "owner_role",
    "public",
    "content_layer",
    "page_type",
    "canonical_knowledge_ids",
    "last_reviewed",
    "review_due",
)
PAGE_TYPES = {"entry", "wiki", "story", "service", "impact", "activity-archive"}
INTERNAL_LINK = re.compile(r"\]\((?:\.\./)+(?:about|ai|governance|impact|services|sources|stories|training)/")
MARKDOWN_LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
REVERSE_DIRECTIVE = re.compile(
    r"不得|不應|不要|請勿|禁止|不可(?:將|把|改寫|直接|自行|對外|公開|引用|使用|推論|補寫|混稱)"
    r"|不能(?:直接|自行|預先|當作|稱為|視為|把|只|用)"
)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match:
            fields[match.group(1)] = match.group(2).strip()
    return fields, text[end + 5 :]


def add(items: list[dict[str, str]], code: str, message: str) -> None:
    items.append({"code": code, "message": message})


def audit(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8-sig")
    fields, body = parse_frontmatter(text)
    blockers: list[dict[str, str]] = []
    warnings: list[dict[str, str]] = []

    for key in REQUIRED_FIELDS:
        if not fields.get(key):
            add(blockers, f"META_{key.upper()}", f"缺少 front matter 欄位：{key}")

    page_type = fields.get("page_type", "").strip("'\"")
    if page_type and page_type not in PAGE_TYPES:
        add(blockers, "META_PAGE_TYPE", f"不支援的 page_type：{page_type}")
    if fields.get("public", "").lower() != "true":
        add(blockers, "META_PUBLIC", "公開頁面的 public 必須是 true")
    if fields.get("content_layer", "").strip("'\"") != "human-readable":
        add(blockers, "META_LAYER", "公開頁面的 content_layer 必須是 human-readable")

    h1_count = len(re.findall(r"(?m)^#\s+\S", body))
    if h1_count != 1:
        add(blockers, "STRUCT_H1", f"必須剛好有一個 H1，目前為 {h1_count}")
    if not re.search(r"(?m)^##\s+\S", body):
        add(warnings, "STRUCT_H2", "缺少 H2，讀者不易掃讀")
    for line_number, line in enumerate(body.splitlines(), start=1):
        match = re.match(r"^##\s+(.+?)\s*$", line)
        if not match:
            continue
        label = re.sub(r"\s*\{[^}]+\}\s*$", "", match.group(1))
        label = re.sub(r"^\d+[.)、]\s*", "", label)
        visible_length = len(re.findall(r"[A-Za-z0-9\u3400-\u9fff]", label))
        if visible_length > 8:
            add(
                warnings,
                "NAV_H2_LONG",
                f"第 {line_number} 行內頁目錄標題超過 8 個可見字元：{label}",
            )
    reverse_matches = sorted(set(REVERSE_DIRECTIVE.findall(body)))
    if reverse_matches:
        add(
            warnings,
            "PUBLIC_REVERSE_DIRECTIVE",
            "公開正文含禁止式審稿語句；請改成正確資料、適用範圍或可直接引用口徑",
        )
    if INTERNAL_LINK.search(body):
        add(blockers, "LINK_INTERNAL", "公開頁面連到不建置的內部維護路徑")

    relative_links = [
        link
        for link in MARKDOWN_LINK.findall(body)
        if not re.match(r"(?:https?://|mailto:|#)", link)
    ]
    for link in relative_links:
        target = (path.parent / link.split("#", 1)[0]).resolve()
        if link and not target.exists():
            add(blockers, "LINK_MISSING", f"相對連結不存在：{link}")

    if re.search(r"全台最大|全國最大|唯一", body) and "比較範圍" not in body:
        add(warnings, "CLAIM_SUPERLATIVE", "使用最大或唯一宣稱，但未說明比較範圍")
    if "notion.site" in body.lower() or "app.notion.com" in body.lower():
        add(blockers, "PRIVACY_NOTION", "公開頁面含 Notion 來源網址，須確認不是私密工作頁")

    if page_type == "entry":
        checks = {
            "ENTRY_POSITION": ("綠色奇蹟", "回收", "整修"),
            "ENTRY_RECYCLE": ("我要回收電腦", "reuse.org.tw"),
            "ENTRY_APPLY": ("我要申請再生電腦", "project.html"),
            "ENTRY_ROLE": ("角色指引",),
            "ENTRY_BOUNDARY": ("網站分工", "官網"),
            "ENTRY_HISTORY": ("2004", "2021"),
        }
        for code, needles in checks.items():
            if not all(needle in body for needle in needles):
                add(blockers, code, f"入口頁缺少：{'、'.join(needles)}")
        if "服務傳承" not in body and "知識庫" not in body:
            add(blockers, "ENTRY_LEGACY", "入口頁須說明服務傳承或知識保存定位")

    if page_type in {"entry", "service"} and "reuse.org.tw" not in body:
        add(blockers, "CURRENT_SERVICE", "入口或服務頁必須連回官網當期服務")

    if page_type == "activity-archive":
        activity_fields = ("event_date", "privacy_review", "rights_review")
        for key in activity_fields:
            if not fields.get(key):
                add(blockers, f"ACT_{key.upper()}", f"活動歸檔缺少：{key}")
        for heading in ("背景與目的", "參與角色與分工", "結果與口徑", "可傳承的經驗"):
            if heading not in body:
                add(blockers, "ACT_SECTION", f"活動歸檔缺少段落：{heading}")

    if fields.get("annual_observation", "").lower() == "true":
        for key in ("observation_year", "evidence_cutoff", "source_ids"):
            if not fields.get(key):
                add(blockers, f"ANNUAL_{key.upper()}", f"年度觀察缺少：{key}")
        for heading in ("年度變化", "協會回應", "引用資訊", "資料依據"):
            if heading not in body:
                add(blockers, "ANNUAL_SECTION", f"年度觀察缺少段落：{heading}")
        if ("報價" in body or "採購" in body) and not all(
            needle in body for needle in ("批次", "報價", "適用範圍")
        ):
            add(blockers, "ANNUAL_PRICE_SCOPE", "採購／報價內容須以正向文字標示批次與適用範圍")

    long_paragraphs = [
        p
        for p in re.split(r"\n\s*\n", body)
        if not p.lstrip().startswith(("#", "-", "|", ">", "```", "<")) and len(p) > 420
    ]
    if long_paragraphs:
        add(warnings, "READ_LONG_PARAGRAPH", f"有 {len(long_paragraphs)} 段超過 420 字，建議拆段")

    recommendation = "revise" if blockers else "ready-for-Chinwen-review"
    return {
        "page": str(path),
        "page_type": page_type or None,
        "blockers": blockers,
        "warnings": warnings,
        "recommendation": recommendation,
        "final_approver": "Chinwen",
        "note": "此工具只做初審，不得將頁面自行改為 approved。",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("page", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    if not args.page.is_file():
        print(f"ERROR: file not found: {args.page}", file=sys.stderr)
        return 2

    result = audit(args.page)
    if args.as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Page: {result['page']}")
        print(f"Recommendation: {result['recommendation']}")
        print("Final approver: Chinwen")
        for level in ("blockers", "warnings"):
            print(f"{level.title()}: {len(result[level])}")
            for item in result[level]:
                print(f"- [{item['code']}] {item['message']}")
        print(result["note"])
    return 1 if result["blockers"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
