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
