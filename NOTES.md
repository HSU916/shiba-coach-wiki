# 現況白板（NOTES.md）

## 目前進度
- 已依「先討論、後生成」完成 8 題需求訪談紀錄（`wiki/requirements-interview.md`），並將 `AGENTS.md` 升級至 v3（精簡於 12,000 字元內，簡報流程拆入 `.agents/workflows/topic-slides.md`）。
- 知識庫目前收錄滿 **6 篇**完整頁面（`raw/01`–`raw/06` 皆已納入）：
  1. `run-walk-5k`（訓練法）
  2. `hill-pacing`（路線數據）
  3. `cvs-recovery`（補給策略）
  4. `knee-and-warmup`（傷痛預防）
  5. `cooldown-and-hydration`（補給策略）
  6. `first-5k-pacing`（訓練法）
- 已透過 6 節點 4 關卡 Graph + Loop 工作流完成 12 頁教學型翻頁 HTML 簡報（`slides/first-5k-guide/index.html`），並建立可執行自動化檢查腳本 `scripts/check_slides_workflow.py`。

## 下一步待辦（給未來接手的 AI）
- 若要新增其他主題簡報（例如「十八尖山地形判讀專題簡報」），請以 `/topic-slides` 呼叫 `.agents/workflows/topic-slides.md`，在 `workflows/topic-<slug>/` 建立獨立狀態檔案並先過 Gate 1–3 再渲染 HTML。
- 新增知識頁前先確認 `raw/**` 與 `assets/style.css` 維持唯讀。
