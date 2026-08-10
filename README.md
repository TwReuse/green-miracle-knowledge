# 綠色奇蹟公開知識庫

本 Repo 規劃作為綠色奇蹟公益服務網協會對外知識的 SSOT（單一真實來源），服務以下用途：

- 官網、組織介紹、行銷與新聞素材。
- 董監事、工作人員、志工與合作夥伴教育訓練。
- 經核准的歷史、服務模式、成果口徑、合作方式與常見問答。
- 可供網站、簡報與 AI 工具引用的結構化公開知識。

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

## 閱讀入口

- [知識站首頁](docs/index.md)
- [法人定位與歷史關係](docs/about/identity-and-history.md)
- [NPO 角色與核定權責](docs/governance/roles-and-approval.md)
- [矽聯代管與法人權責](docs/governance/hosting-and-custodianship.md)
- [公開與非公開資料邊界](docs/governance/public-private-boundary.md)
- [內容發布生命週期](docs/governance/publication-lifecycle.md)
- [教育訓練入口](docs/training/index.md)
- [二十年經驗傳承與應用](docs/training/learning-from-20-years.md)
- [來源登錄](docs/sources/source-register.md)
- [Repo 目錄與內容架構](docs/repository-architecture.md)

## 本機預覽

```powershell
python -m pip install -r requirements.txt
python -m mkdocs serve
python -m mkdocs build --strict
```

## 目前狀態

`approved`：正式遠端 Repo 已建立，由 `TwReuse` 技術代管，Chinwen 統籌知識治理、方案、資料、隱私與發布決策。`main` 為公開基線；只有標示 `approved` 的內容可作為官網、簡報、教育訓練與 AI 的正式引用來源。

- 帳號或權限中斷時，由 `TwReuse` 組織管理者執行技術復原，但不因此取得協會內容核定權。
- 敏感或資安內容以 `service@reuse.org.tw` 私密通報，不得放入公開 Issue。
- 授權採分層管理；詳見 [LICENSE.md](LICENSE.md)。
