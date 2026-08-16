---
name: green-miracle-seo-auditor
description: Audit, improve, and validate SEO for the Green Miracle MkDocs knowledge site at docs.reuse.org.tw. Use when Codex is asked to review or repair page titles, descriptions, canonical URLs, robots.txt, sitemap output, Open Graph metadata, structured data, heading structure, duplicate metadata, search visibility, or SEO readiness before publishing Green Miracle public articles.
---

# 綠色奇蹟 SEO 稽核

協助讀者找到正確、可引用的綠色奇蹟知識，同時維持官網分工、事實證據與公開核定邊界。

## 必讀資料

開始實質查核或修改前讀取：

- `knowledge-base/governance/search-and-seo-governance.md`
- `skills/review-green-miracle-public-content/SKILL.md`
- `skills/review-green-miracle-public-content/references/review-standard.md`
- `mkdocs.yml`

涉及服務狀態、成果數據、歷史、兒少、募款或合作聲明時，再讀取對應知識母稿、registry 與來源登錄。需要最新官網資料時，查核 `https://www.reuse.org.tw/`，不要從知識網站反推當期服務。

## 工作流程

1. 先檢查分支、upstream 與未提交檔案，保留不屬於本次任務的工作。
2. 判斷任務屬於唯讀稽核、內容改善、技術修正或發布驗證；唯讀要求不得擴張成修改或發布。
3. 確認目標讀者、搜尋意圖、官網／知識站分工、文章狀態與核定證據。
4. 執行基準稽核：

   ```powershell
   $env:PYTHONUTF8='1'
   python .agents/skills/green-miracle-seo-auditor/scripts/audit_green_miracle_seo.py `
     --repo . `
     --site-dir build/seo-audit/site `
     --output build/seo-audit/report.md `
     --json-output build/seo-audit/report.json `
     --fail-on major
   ```

5. 將 finding 追到來源 Markdown、`mkdocs.yml`、模板或治理資料，採取最小且可驗證的修正。
6. 修改文章時，同步執行公開內容 Skill 的逐頁查核；正文只提供讀者可採用的資料，不放審稿命令、repo 管理要求或禁止清單。
7. 重跑稽核與 strict build，清楚列出仍待核定、外部權利或正式站發布的事項。

## 修正原則

- title、description、H1、選單與 canonical 語意一致，但不要求逐字重複。
- 主選單與內頁 H2 目錄以 8 個可見字元內為主；較完整的 SEO 標題放在 frontmatter。
- 每頁摘要獨立、具體且受正文支持，不加入誇大成果、未證實數字或服務保證。
- 規劃中內容在標題、摘要、正文與結構化資料維持相同狀態口徑。
- 當期回收、申請、捐款、活動及聯絡資訊以官網為準；知識站保留服務歷程、方法、年度觀察與引用資料。
- 不新增 `meta keywords`，不以 robots.txt 處理 canonical 問題，不為追求關鍵字重複段落。
- 不自行建立核定證據、改寫 `approved` 狀態、提交 Search Console、Commit、Push 或發布；除非使用者明確要求。

## 驗證

每次實作至少執行：

```powershell
$env:PYTHONUTF8='1'
python -m mkdocs build --strict --config-file mkdocs.yml --site-dir build/public
python .agents/skills/green-miracle-seo-auditor/scripts/audit_green_miracle_seo.py --repo . --site-dir build/seo-audit/site --fail-on major
git diff --check
```

對每個異動的公開 Markdown 頁面再執行：

```powershell
python -X utf8 skills/review-green-miracle-public-content/scripts/audit_public_page.py public-site/public/<page>.md
```

使用者要求檢查正式站時，另驗證 `https://docs.reuse.org.tw/robots.txt`、`sitemap.xml` 與代表頁面，並把正式站證據和本機建置結果分開報告。

## 輸出

以 `PASS`、`PASS_WITH_WARNINGS` 或 `BLOCKED` 開頭，列出：

1. 查核頁面與搜尋意圖；
2. 已完成或建議的修正；
3. 執行過的驗證與結果；
4. 仍待 Chinwen 或其他權責核定的事項；
5. 異動檔案、提交與發布狀態。
