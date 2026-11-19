# CLAUDE.md — 阿柴教練跑步知識庫專案指引

@AGENTS.md

本專案以 [AGENTS.md](./AGENTS.md) 作為主要規則來源，簡報生成工作流細節拆存於 [.agents/workflows/topic-slides.md](./.agents/workflows/topic-slides.md)。使用 Claude Code 或其他 Coding Agent 時，請直接依循下列原則與上述文件執行：

1. **唯讀保護**：`raw/**` 與 `assets/style.css`、`assets/app.js`、`assets/shiba-logo.svg` 為唯讀，嚴禁更動既有原始筆記與共用樣式。
2. **命名與靜態技術棧**：所有 `<slug>` 限用 `^[a-z0-9-]+$`，全站保持純靜態 HTML/CSS/原生 JS 與相對路徑。
3. **簡報 Graph + Loop 分工**：各節點只讀取被授權的輸入檔；檢查關卡一律前移至證據卡與逐頁稿階段，HTML 渲染時禁止修改逐頁稿文案。
4. **腳本驗收取代口頭檢查**：修改完成後必須執行 `python scripts/check_slides_workflow.py`，確認 Gate 1 至 Gate 4 全部通過，並同步更新 `log.md` 與 `NOTES.md`。
