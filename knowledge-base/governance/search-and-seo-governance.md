---
doc_id: GM-GOV-SEO-001
status: approved
owner_role: Chinwen
public: true
approved_by: Chinwen
approval_date: 2026-08-16
approval_evidence: owner-instruction-2026-08-16-green-miracle-seo-skill
last_reviewed: 2026-08-16
review_due: 2026-11-14
---

# 搜尋與 SEO 治理

本規範管理「綠色奇蹟服務傳承與永續共創」知識網站的搜尋呈現、索引範圍與發布查核。SEO 用來協助讀者找到正確資料，不改寫事實、不放大成果，也不取代內容核定。

## 網站分工

| 網站 | 正式權責 | 搜尋內容 |
| --- | --- | --- |
| `www.reuse.org.tw` | 當期回收、申請、捐款、活動、聯絡與法定公告 | 服務入口及當期資訊 |
| `docs.reuse.org.tw` | 服務歷程、再生方法、年度觀察、事實資料與引用說明 | 長期知識及可引用脈絡 |

兩站內容相近時，以讀者任務決定 canonical owner。當期辦理資訊連回官網；知識網站不複製可能變動的申請條件、金額、聯絡方式或活動狀態。

## 索引條件

公開頁進入 sitemap 前須同時符合：

- frontmatter 為 `public: true`、`status: approved`，核定證據可追溯；
- 內容未含個資、兒少識別、內控、私密來源或未授權素材；
- 頁面具備唯一 `title`、唯一 `description` 與 HTTPS canonical；
- 正文只有一個 H1，標題層級合理；
- 規劃中內容在正文及搜尋摘要中都明確標示狀態；
- 文章已通過公開內容審核與 MkDocs strict build。

核准的是「公開說明的版本」而非服務已上線的承諾。規劃中方向可以被搜尋，但標題、摘要與正文都要維持同一狀態口徑。

## 標題與摘要

- `title` 說明頁面主題；H1 與 title 語意一致，不必逐字相同。
- 主選單與內頁目錄以閱讀導覽為目的，名稱以 8 個可見字元內為主；SEO 標題不受選單短字數限制。
- `description` 直接說明讀者可取得的資料，使用具體名詞與服務情境，不放口號、內部管理要求或禁止清單。
- 每頁摘要必須獨立撰寫。30 至 90 個中文字可作為編輯參考，仍以完整、準確為優先。
- 關鍵字自然出現在標題、首段、段落與連結文字；不建立 `meta keywords`，不堆疊同義詞。

## Canonical、sitemap 與 robots

- canonical 一律使用 `https://docs.reuse.org.tw/` 的正式路徑。
- sitemap 只列出核准且允許公開索引的正式 canonical URL。
- `robots.txt` 提供爬取規則並指向正式 sitemap，不拿來處理重複內容或取代 noindex 決策。
- 路徑變更前先建立舊網址對照與轉址方案，避免既有引用失效。

## 社群與結構化資料

- Open Graph 與 Twitter 摘要沿用頁面 title、description 與 canonical，不另寫一套誇大文案。
- 首頁可標示 `Organization` 與 `WebSite`；內頁使用與可見內容一致的 `WebPage`。
- JSON-LD 不得包含正文沒有呈現的成果、合作、聯絡、服務狀態或承諾。
- 結構化資料通過語法檢查不代表搜尋引擎一定採用或提高排名。

## 作業與核定

日常 SEO 採單人作業治理，由 Chinwen 統籌內容、查核、核定與發布，並用來源、差異、自動驗證及 Git 紀錄維持可追溯性。

執行順序：

1. 盤點搜尋意圖、頁面角色與網站分工。
2. 執行 SEO 機械稽核與公開內容審核。
3. 修正來源 Markdown、MkDocs 設定或模板，不直接改建置輸出。
4. 完成 strict build、metadata、canonical、sitemap、robots 與 JSON-LD 驗證。
5. 核定後提交、發布，再檢查正式網址。
6. 需要時由站務負責人提交 Search Console sitemap 或重新檢索要求。

涉及法定事項、募款、財務、個資、兒少、品牌、合作聲明或第三方權利時，仍須取得相應權責或權利人的同意。

## 完成標誌

- 每個公開頁面有唯一且準確的搜尋呈現。
- 官網與知識網站沒有競爭同一個當期服務意圖。
- sitemap、robots、canonical 與結構化資料一致。
- 自動稽核沒有 critical 或 major finding。
- 搜尋改善沒有改變文章核定狀態或製造新事實。
