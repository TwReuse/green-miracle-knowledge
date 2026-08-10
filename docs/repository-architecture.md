---
doc_id: GM-REPO-001
status: draft
owner_role: Chinwen
public: true
last_reviewed: 2026-08-09
review_due: 2026-11-07
---

# Repo 應如何安排知識、教材與公開素材

## 建議名稱

正式名稱採用 `TwReuse/green-miracle-knowledge`，定位為綠色奇蹟公開知識的 SSOT（單一真實來源）。

不建議使用：

- `green-miracle-website`：會誤以為只服務網站。
- `green-miracle-handbook`：會低估資料、行銷與對外 SSOT 用途。
- `sl_green-miracle-*`：容易被解讀成矽聯產品或公司內部專案。
- `green-miracle-docs`：可用，但不如 `knowledge` 能涵蓋結構化資料、教材與內容資產。

## 建議目錄

```text
green-miracle-knowledge/
├─ README.md                         # 公開入口、定位與代管聲明
├─ GOVERNANCE.md                     # NPO 知識治理章程
├─ CONTRIBUTING.md                   # 提案、來源與核定規則
├─ SECURITY.md                       # 私密通報與禁止公開資料
├─ LICENSE.md                        # 文件、程式碼與素材授權
├─ repository-profile.yaml           # Repo、權限、分支與發布設定
├─ mkdocs.yml                        # 公開知識站導覽
├─ docs/
│  ├─ about/                         # 法人、歷史、使命與品牌定位
│  ├─ services/                      # 回收、整修、媒合、交付與 FAQ
│  ├─ impact/                        # 成果、方法、年度報告與更正
│  ├─ stories/                       # 已授權案例與人物故事
│  ├─ partners/                      # 合作方式與核准夥伴描述
│  ├─ training/                      # 新成員、志工與發布訓練
│  ├─ governance/                    # 權責、代管、隱私與發布流程
│  └─ sources/                       # 可公開來源與證據導覽
├─ registry/
│  ├─ public-knowledge.yaml          # 知識庫基本設定與公開規則
│  ├─ sources.yaml                   # 來源、版本、權威層級
│  ├─ claims.yaml                    # 數字與對外宣稱核定狀態
│  ├─ assets.yaml                    # 可公開照片、Logo、影片與權利
│  └─ releases.yaml                  # 官網、簡報、行銷引用版本
├─ assets/public/                    # 僅放已核准公開的視覺素材
├─ templates/                        # 簡報、貼文、新聞與訓練模板
├─ tools/                            # 索引產製、連結與敏感資料檢查
└─ .github/                          # CI、PR 範本與 CODEOWNERS
```

## 內容分層

| 層次 | 權威內容 | 主要使用者 |
|---|---|---|
| `docs/` | 人可閱讀的核定說明與教材 | 團隊、志工、社會大眾、媒體 |
| `registry/` | 系統可讀的 ID、來源、狀態及版本 | 網站、簡報產製、AI、稽核工具 |
| `assets/public/` | 已核准公開且有權利紀錄的素材 | 網站、行銷、簡報 |
| `templates/` | 從核准知識重組的標準輸出 | 內容、教育與對外溝通人員 |
| 私密營運系統 | 個資、設備、財務、合約與內部證據 | 協會授權人員；不進公開 Repo |

## 分階段建立

### 第一階段

沿用目前已建立的 `docs/`、`registry/public-knowledge.yaml`、治理文件、教育訓練及 MkDocs 站，建立遠端 Repo 與 Pages。

### 第二階段

把來源、宣稱、素材與發布紀錄拆成獨立 YAML，加入自動索引、期限提醒及敏感字詞檢查。

### 第三階段

讓官網、標準簡報、行銷模板及 AI 助理依知識 ID 與 Release 版本引用，形成可追溯的跨載體內容供應鏈。

## 風險

- 同一份內容同時在 Notion、Repo、網站與簡報人工維護，可能形成多個版本。
- 公開素材若沒有授權清單，容易誤用人物、兒少、Logo 或第三方著作。
- Chinwen 是單一管理人時，存在帳號與營運持續風險。
- `TwReuse` 組織名稱可能讓外界誤認法人從屬，因此公開入口必須持續顯示代管聲明。

## 維運注意事項

Notion 可保留為草稿與協作工作區，但 `main` 分支的 `approved` 版本才是對外 SSOT。網站、行銷、簡報與教育教材應記錄使用的知識 ID、Release 或 commit。
