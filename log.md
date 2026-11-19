# 工作日誌（log.md）

## [2026-11-14] init | 建立初版 AGENTS.md 與前三篇知識頁
- 建立三層架構：`raw/`、`wiki/`、`pages/`，並建立全站共用樣式 `assets/style.css`。
- 收錄前三篇原始素材並產出知識頁與互動工具：`run-walk-5k`、`hill-pacing`、`cvs-recovery`。
- 更新 `wiki/index.md` 與根目錄 `index.html`。

## [2026-11-14] update | 依 Gemini 討論補強 AGENTS.md 防呆與權限矩陣
- 新增第二節「檔案讀寫權限矩陣」，明確將 `raw/**`、`assets/style.css` 設為唯讀。
- 新增第三節「英文 Kebab-Case 檔名規範」正反例與第六節「收工前 6 項強制檢查清單」。
- 於各子頁底部 `<nav class="pager">` 加入 `PREV_LINK_START` 與 `NEXT_LINK_START` 註解錨點。

## [2026-11-14] ingest | 新增第 4 篇知識頁：跑前動態暖身與跑者膝預防 (knee-and-warmup)
- 收錄 `raw/04-knee-and-warmup.md`（不更動既有 `raw/01`–`03`）。
- 生成 `wiki/knee-and-warmup.md` 與 `pages/knee-and-warmup/index.html`（含暖身與膝蓋負荷檢核小工具）。
- 雙向更新 `run-walk-5k`、`hill-pacing` 延伸閱讀，將 `cvs-recovery` 下一篇連結指向 `knee-and-warmup`，並更新 `wiki/index.md` 與根目錄 `index.html`。

## [2026-11-19] discuss-and-upgrade | 需求訪談定案與 AGENTS.md v3 升級（第 10 週）
- 依「先討論、後生成」流程與網頁版 Gemini 討論後完成 8 題需求訪談紀錄（`wiki/requirements-interview.md`）。
- 將 `AGENTS.md` 升級至 v3 精簡版，並把簡報 Graph + Loop 細則拆出至 `.agents/workflows/topic-slides.md`。

## [2026-11-19] ingest | 擴充第 5、6 篇知識頁（cooldown-and-hydration、first-5k-pacing）
- 新增唯讀素材 `raw/05-post-run-cooldown-and-hydration.md` 與 `raw/06-first-5k-race-pacing-plan.md`（維持 `raw/01`–`04` 完好不變）。
- 依 SOP 生成對應 `wiki/` 摘要頁、`pages/` 互動網頁，並更新全站 6 篇雙向連結、`wiki/index.md` 與首頁 6 張卡片。

## [2026-11-19] workflow-build | 完成 12 頁教學 HTML 簡報與 Shift-Left 自動檢查腳本
- 執行 6 節點 4 關卡工作流產出 `workflows/topic-first-5k-guide/` 狀態檔與 12 頁翻頁簡報 `slides/first-5k-guide/index.html`。
- 依第 1 輪失敗經驗將覆蓋率、字數密度與 CR-01 因果禁令檢查前移至 Gate 2／Gate 3，實作 `scripts/check_slides_workflow.py` 驗證全過。
