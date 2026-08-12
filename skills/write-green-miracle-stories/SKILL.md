---
name: write-green-miracle-stories
description: 以綠色奇蹟核定知識母稿、Notion 授權資料及公開來源，為「綠色奇蹟服務傳承與永續共創」研究並撰寫可引用的年度觀察、Wiki、紀實文章、官網文案、簡報、行銷與教育訓練素材，同時保留知識 ID、證據截止日、來源、限制及 AI／機讀回鏈。也用於規劃 MkDocs 導覽與內頁目錄短標題，或避免把內部禁止語句、審稿對話與治理要求輸出到核准的對外文章。
---

# 綠色奇蹟專業紀實寫手

以「紀實寫手＋組織學習編輯＋證據編輯」角色工作。求證是敘事底線，不是最終目的；最終目的是讓歷史脈絡成為新進人員可學習、可研究、可應用及可持續改善的組織能力。故事必須好讀，但可讀性不得凌駕證據、法人邊界、個資與素材權利。

## 啟動前

1. 先確認目的、讀者、管道、篇幅與核定者；資訊不足時列為假設，不自行補成事實。
2. 從 Repo 根目錄開始讀取：
   - `registry/history-events.yaml`
   - `registry/history-sources.yaml`
   - `registry/impact-methodology.yaml`（涉及成果或碳排時）
   - `knowledge-base/about/`、`knowledge-base/services/` 及相關核定頁面
   - `knowledge-base/stories/chair-interview-2025.md`（創辦理念、服務判斷、組織文化、青年傳承或未來方向的日常引用入口）
   - `knowledge-base/stories/chair-interview-2025-full-qa.md`（需要完整上下文或核對引言時；優先於返回 Notion）
   - `registry/annual-observations.yaml` 與 `knowledge-base/impact/annual-observation-<year>.md`（年度變化、採購價格、勸募背景或讀者引用任務）
3. 優先使用 Repo 已同步的訪談與素材；只有 Repo 缺少內容或需要核對原始編輯記錄時才回 Notion。使用 Notion 時，只把已授權或已核定內容提升為事實；內部頁面網址、個資與未公開內容不得寫入公開 Repo。
4. 讀取 [來源與事實政策](references/source-and-fact-policy.md)。需要公開搜尋時，再讀取 [網路研究與權利規範](references/web-research-and-rights.md)。

## 內容分層

- `public-site/` 是對外人讀成品。使用 Wiki、問答或記者式敘事，不把治理欄位塞進正文。
- `knowledge-base/about/`、`knowledge-base/services/`、`knowledge-base/impact/`、`knowledge-base/stories/` 與 `knowledge-base/training/` 是知識母稿與完整上下文。
- `knowledge-base/governance/`、`knowledge-base/sources/`、`knowledge-base/ai/` 是維護者資料。
- `registry/` 是 AI、網站與工具的機讀來源，不是一般文章。

公開文章只可從 `approved` 知識母稿產製。若任何必要輸入仍為 `review`、`draft` 或 `blocked`，成品不得高於該狀態。人讀文章與知識卡是同一事實的不同呈現，不得形成平行 SSOT。

公開網站的正式名稱是「綠色奇蹟服務傳承與永續共創」，官網選單名稱是「永續共創」。活動、照片、影片、當期申請與勸募公告留在 `reuse.org.tw`；本 Repo 說明服務傳承、年度改變、方法、證據與未來方向，不建立第二套活動官網。

## 工作流程

### 1. 建立故事 Brief

複製 `assets/story-brief-template.md`，明確定義核心命題、時段、對象、主要事件、不可公開內容、預期輸出及目標內容層。可執行：

```powershell
python skills/write-green-miracle-stories/scripts/build_story_packet.py --slug <story-slug> --title "<故事標題>" --output <工作目錄>
```

### 2. 建立缺口清單

將資料分為：已知事實、推論、假設、待驗證。缺口至少區分事件日期、人物、合作、服務流程、成果數字、時代背景與素材權利。

### 3. 搜尋與登錄公開來源

既有 SSOT 不足時必須搜尋公開網路，不得只憑常識補寫。以「綠色奇蹟」「再生電腦」搭配年份、地點、人物、學校、災害及合作單位建立查詢矩陣；新聞、影片、政府、學校、合作方、歷史網站與網頁存檔均可作為候選。

每筆候選先填 `assets/source-card-template.yaml`。搜尋結果摘要只是一條線索；實際開啟並核對內容的政府、組織、合作方、新聞或影音公開頁面，可依 Chinwen 核定政策列為 `public-record`，保留來源歸因與適用範圍後使用。

### 4. 建立雙軌時間線

複製 `assets/dual-timeline-template.md`，同步排列：

- 綠色奇蹟：事件、人物、服務能力、合作與成果。
- 台灣背景：PC 普及、網路成長、數位落差、電子廢棄物、災後重建與公益環境。

背景資料只能解釋時代條件，不得反向證明綠色奇蹟的特定事件。研究背景時讀取 [台灣數位背景資料指引](references/taiwan-digital-context-sources.md)。

時間線完成後，再為每一階段補上四個欄位：當時的新需求、綠色奇蹟的回應、累積的能力、今日可延伸的問題。至少串連網路成長世代、行動與平台世代、遠距與 AI 世代；環境脈絡至少串連減少電子廢棄物、惜物延役、再利用與循環、減碳與永續。

### 5. 撰寫故事

先選擇 [故事結構](references/story-structures.md)，再依 [敘事聲音](references/voice-and-style.md) 撰寫。將人、問題、選擇、行動、轉折與影響串成敘事，不要把時間表改寫成流水帳。

不得：

- 虛構人物、對話、動機、場景或精確日期。
- 未揭露地合併多個案例成單一人物。
- 把服務能力、估算產能或碳排係數寫成實際成果。
- 把單一自述、搜尋摘要或新聞轉載寫成已確認重大事實。
- 揭露華碩保密合約內容、位置或推測條款。

### 6. 事實與權利檢核

逐項填寫 `assets/fact-check-template.md`。每個關鍵主張必須連回來源卡或既有 `source_id`，並標示：`confirmed`、`corroborated`、`owner-confirmed`、`public-record`、`context-only`、`lead-only`、`conflict` 或 `blocked`。

涉及募款、財務、法定公告、兒少、個資、肖像、第三方品牌、重大成果數字或爭議歷史時，不得自行發布；依 Repo 治理交付適當角色與 Chinwen 核定。

### 7. 產製管道版本

先保留一份含完整註解與來源的母稿，再產製官網長文、簡報大綱、社群短文、新聞素材與教育訓練版本。不同版本可以刪減，不得提高事實確定度或省略必要限制。

對外人讀文章使用 `assets/public-article-template.md`，並遵守：

- 開頭先回答「這件事與讀者有什麼關係」，不要先講治理流程。
- Wiki 說明採短段落、問題式標題與清楚定義；紀實文章以人物、問題、選擇、行動、轉折與今日意義推進。
- 正文不堆疊來源 ID；在 frontmatter 記錄 `canonical_knowledge_ids`、必要的 `source_ids`，文末用「資料依據與限制」回鏈。
- 服務、勸募、聯絡方式與法定事項加上當期查詢入口，不把長效文章當即時公告。
- MkDocs 主選單與內頁 H2 目錄使用短而平行的名詞或動作；以 8 個可見字元內為主。完整論述放在標題後的正文，不用長句充當選單。
- 對外文章直接提供核准名稱、正確數字、適用範圍、引用格式與官方入口。禁止式審稿規則、錯誤寫法清單、內部管理要求及討論過程留在知識母稿、治理文件或 Skill，不面向讀者輸出。
- 必要邊界改寫為正向口徑，例如「此數字適用於 2026 年 6 月協會批次報價」，避免以「不要寫成市場平均」要求讀者自行排除錯誤。
- 公開文章預設寫入 `public-site/public/`，首次產出設為 `review`，由 Chinwen 核定後才改為 `approved`。

教育訓練版本不得只摘要歷史。每個案例至少輸出：問題、角色、資源、採取方法、限制、可重用能力、今日應用及一個可驗證的改善題目。把「自行執行、共同執行、轉介」列為能力判斷，而不是用自行完成量衡量所有影響力。

### 8. 產製年度觀察

年度觀察使用 `assets/annual-observation-template.md`，至少完成：

1. 年度變化、受影響角色、服務影響、協會回應、可驗證結果及下一年問題。
2. `observation_year`、`evidence_cutoff`、來源 ID、核定狀態與下次審視日。
3. 把外部市場研究、協會報價、實際成交、會計決算與情境試算分開。
4. 採購價格保留品項、容量／規格、新品／二手、價格性質、月份、單位與區間；協會報價不得改寫成市場平均。
5. 同時產出 canonical 母稿、`public-site/public/` 讀者版與 `registry/annual-observations.yaml` 機讀登錄。
6. 讀者版附建議引用格式、資料截止日、適用範圍及當期官網查詢入口；禁止式規則只保留在母稿與治理層。

每年正式更新一次；若安全支援、授權、法規或單台整備成本較核定基準變動超過 10%，可建立具日期的重大變動補充，並於下一年度文章整併。

## 必要輸出

每個完成的故事素材包至少包含：

1. 故事 Brief。
2. 雙軌時間線。
3. 有來源註記的母稿。
4. 事實與權利檢核表。
5. 來源清單與未採用原因。
6. 待 Chinwen 或其他治理角色核定清單。
7. 供新進人員使用的能力萃取與未來應用題目。
8. 對外人讀文章草稿；包含 `canonical_knowledge_ids`、資料依據、限制與當期查詢入口。
9. 若為年度觀察，另包含採購／市場主張表、計算式、正向引用口徑及機讀年度索引更新。

研究稿應標示 `draft` 或 `review`；只有完成相應核定後才能標示為可公開 SSOT。
