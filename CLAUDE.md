# CLAUDE.md — 阿柴教練跑步知識庫專案指引

本專案以 [AGENTS.md](./AGENTS.md) 作為完整規則來源；使用 Claude Code 或其他支援 `CLAUDE.md` 的 Agent 時，請直接依循下列核心規範執行（完整細節與範本請同步參閱 `AGENTS.md`）。

## 核心約束摘要
1. **三層架構與唯讀保護**：
   - `raw/**` 為唯讀原始筆記區，**嚴禁**修改或刪除既有檔案。
   - `assets/style.css`、`assets/app.js`、`assets/shiba-logo.svg` 為全站唯讀基準檔，不可擅自改動配色或架構。
   - 更新工作僅寫入 `wiki/`、`pages/<slug>/index.html`、`index.html`（限 `<!-- WIKI_CARDS_START -->` 區間內）、`log.md`（只增不刪）與 `NOTES.md`。
2. **命名規範（Kebab-Case）**：
   - `<slug>` 僅限小寫英文、數字與連字號（`^[a-z0-9-]+$`），禁止中文與底線，三處（`wiki/<slug>.md`、`pages/<slug>/index.html`、首頁連結）須完全一致。
3. **純靜態與相對路徑**：
   - 不可引入 React/Vite 等需要編譯的依賴；所有頁面連結使用相對路徑（如 `../../assets/style.css`），確保 GitHub Pages 子目錄部署正常。
4. **收工必檢**：
   - 完成任何新頁面時，務必同步更新 `wiki/index.md`、首頁卡片、雙向「延伸閱讀」、前一頁 `<!-- NEXT_LINK_START -->` 錨點、`log.md` 與 `NOTES.md`，並確認 `raw/` 內容完好無損。
