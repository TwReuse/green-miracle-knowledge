---
doc_id: GM-PUBLIC-CITE-001
status: review
owner_role: Chinwen
public: true
content_layer: human-readable
canonical_knowledge_ids: [GM-PUB-001, GM-GOV-003, GM-AI-CARD-INDEX-001]
last_reviewed: 2026-08-10
review_due: 2026-11-08
---

# 如何引用這個知識庫

## 一般文章、報導與簡報

優先引用「公開閱讀」區的文章，並標示：

> 資料來源：社團法人綠色奇蹟公益服務網協會，《文章標題》，綠色奇蹟公開知識庫，v1.0.0，查閱日期。

若文章內容被刪節、重組或交由 AI 改寫，請註明「經整理／改寫」，不要暗示協會為改寫後的內容背書。

## AI 與網站整合

AI 不應直接從所有 Markdown 頁面自由拼接答案。建議依序使用：

1. `registry/ai-knowledge-cards.yaml` 中狀態為 `approved` 的卡片。
2. 卡片所列的核定主題文件與限制。
3. 公開閱讀文章，作為較自然的說明文字。
4. 當期服務、勸募與法定事項，回到官網或正式文件即時確認。

`draft`、`review`、`blocked` 內容不能成為正式預設答案。AI 必須區分已知事實、推論、假設、待驗證與建議，並保留來源版本。

## 哪些內容不能直接拿來用

- 人物、兒少、個案、照片、影音、Logo 與第三方著作，須另外確認權利。
- 個資、設備序號、物流明細、內部財務、合約與資安資訊不得從本 Repo 推論或補寫。
- 產能、申請量、回收量、完成交付與合作轉介不能直接相加。
- 本知識庫不取代當期申請、客服、勸募、稅務或法律確認。
