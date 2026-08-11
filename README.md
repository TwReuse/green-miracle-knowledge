# 綠色奇蹟服務傳承與永續共創

本 Repo 是「綠色奇蹟服務傳承與永續共創」網站及綠色奇蹟公益服務網協會對外知識的 SSOT（單一真實來源），服務以下用途：

- 官網、組織介紹、行銷與新聞素材。
- 董監事、工作人員、志工與合作夥伴教育訓練。
- 經核准的歷史、服務模式、成果口徑、合作方式與常見問答。
- 可供網站、簡報與 AI 工具引用的結構化公開知識。

官網建議以四字選單「永續共創」連入本網站。正式官網負責當期活動、照片、影片、回收、申請與捐款；本 Repo 負責保存服務歷程、年度變化、方法、證據、公益協作及下一個二十年的可能方向。

## 法人與治理定位

綠色奇蹟源自矽聯科技早期公益服務，創辦人同為邱勤文；綠色奇蹟已是獨立法人，因此本 Repo 由協會自己的治理與授權機制管理，不從屬於矽聯科技的公司治理 Repo。

- 矽聯科技文件只能作為歷史來源或合作關係證據。
- 協會的正式名稱、使命、服務、成果、募款、財務、個資與對外說法，由協會授權角色核定。
- 尚未核定的素材一律標示 `draft`、`review` 或 `blocked`，不得因存在 Repo 就視為可公開事實。

## 遠端代管定位

- 正式遠端：`https://github.com/TwReuse/green-miracle-knowledge`
- GitHub 組織與技術代管：矽聯科技 `TwReuse`
- Repo 管理人與知識治理負責人：Chinwen
- 法人內容權責：綠色奇蹟公益服務網協會

放在 `TwReuse` 代表目前由矽聯科技提供 GitHub 帳號、權限、CI（持續整合）及發布技術代管，不代表協會的內容、財務、會務、個資或品牌權責移轉給矽聯科技。

## 兩種使用介面

- `public-site/`：對外人讀內容。`mkdocs.yml` 只發布這個目錄。
- `knowledge-base/`：知識母稿、治理、來源、訓練與 AI 維護內容。資料可在 Repo 查閱，但不出現在公開網站。
- `registry/`：AI、網站、搜尋與自動化使用的機讀索引。
- `workbench/`：片段整理流程與頁面初審紀錄，不進任何公開網站導覽。
- `skills/`：寫作、初審與活動歸檔方法。

「不在公開網站」不是「機密」。Repo 本身是公開可讀；真正需要保密的 Notion 私密頁、個資、兒少資訊、後台逐筆明細、合約與內控資料仍不得放入本 Repo。

## 內容分層

- `public-site/`：寫手 Skill 依核定知識改寫的 Wiki／紀實對外文章。
- `knowledge-base/`：保存完整事實口徑、條件、例外、來源與上下文。
- `workbench/`：維護者的片段供應與頁面審查作業紀錄。
- `registry/`：供 AI、網站與工具使用的機讀索引，不作為一般讀者主入口。

## 本機預覽

```powershell
python -m pip install -r requirements.txt
python -m mkdocs serve
python -m mkdocs build --strict
```

知識工作台預覽：

```powershell
python -m mkdocs serve -f mkdocs.knowledge.yml -a 127.0.0.1:8774
python -m mkdocs build --strict -f mkdocs.knowledge.yml
```

## 目前狀態

`approved`：正式遠端 Repo 已建立，由 `TwReuse` 技術代管，Chinwen 統籌知識治理、方案、資料、隱私與發布決策。`main` 為公開基線；只有標示 `approved` 的內容可作為官網、簡報、教育訓練與 AI 的正式引用來源。

- 帳號或權限中斷時，由 `TwReuse` 組織管理者執行技術復原，但不因此取得協會內容核定權。
- 敏感或資安內容以 `service@reuse.org.tw` 私密通報，不得放入公開 Issue。
- 授權採分層管理；詳見 [LICENSE.md](LICENSE.md)。
