#!/usr/bin/env python3
"""Create a governed Green Miracle story research packet from bundled templates."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import shutil
from pathlib import Path


def safe_slug(value: str) -> str:
    slug = re.sub(r"[^a-z0-9-]+", "-", value.strip().lower()).strip("-")
    if not slug:
        raise ValueError("slug must contain lowercase letters, digits, or hyphens")
    return slug


def render(source: Path, target: Path, values: dict[str, str]) -> None:
    text = source.read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    target.write_text(text, encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    slug = safe_slug(args.slug)
    packet = args.output.resolve() / slug
    if packet.exists() and any(packet.iterdir()):
        raise FileExistsError(f"refusing to overwrite non-empty directory: {packet}")
    packet.mkdir(parents=True, exist_ok=True)

    assets = Path(__file__).resolve().parent.parent / "assets"
    values = {"TITLE": args.title, "SLUG": slug, "DATE": dt.date.today().isoformat()}
    render(assets / "story-brief-template.md", packet / "01-story-brief.md", values)
    render(assets / "dual-timeline-template.md", packet / "02-dual-timeline.md", values)
    shutil.copyfile(assets / "source-card-template.yaml", packet / "03-source-cards.yaml")
    shutil.copyfile(assets / "fact-check-template.md", packet / "04-fact-check.md")
    (packet / "05-master-story.md").write_text(
        f"# {args.title}\n\n> status: draft\n\n## 故事正文\n\n## 來源註記\n",
        encoding="utf-8",
        newline="\n",
    )
    (packet / "06-approval-queue.md").write_text(
        "# 核定清單\n\n- [ ] Chinwen 一般知識與敘事口徑\n- [ ] 必要的方案／證據覆核\n- [ ] 必要的權利與隱私覆核\n- [ ] 必要的法人治理核定\n",
        encoding="utf-8",
        newline="\n",
    )
    public_values = {
        **values,
        "DOC_ID": "GM-PUBLIC-DRAFT-001",
        "STYLE": "journalistic-wiki",
    }
    render(
        assets / "public-article-template.md",
        packet / "07-public-article.md",
        public_values,
    )
    print(packet)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
