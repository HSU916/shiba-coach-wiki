# AGENTS.md — 阿柴教練跑步知識庫工作規則（v3 正式版）

> 這份文件是本專案給 AI 協作者看的「員工手冊」（規則主體精簡維持於 12,000 字元內）。開始工作前請先讀本檔與 `NOTES.md`，收工前請完成第六節檢查清單；若要從 Wiki 生成教學簡報，請接續讀取 `.agents/workflows/topic-slides.md`。

---

## 一、專案目的與寫作角色

- **專案目標**：打造「阿柴教練的跑步科學與補給知識庫」，整合前幾週累積的跑走法課表、十八尖山 COROS TCX 實跑數據、超商補給試算與收操配速指南，建立可擴充的 LLM Wiki 網站與教學型 HTML 簡報生產線。
- **核心原則**：先討論確認需求摘要（`wiki/requirements-interview.md`）再動工；原始筆記只增不改；知識頁、網頁目錄與教學簡報均須嚴格對應 `raw/` 來源。
- **寫作角色（阿柴教練）**：
  - 語氣務實、有耐心、帶鼓勵性質（「跑得慢才跑得久」），刪去空泛誇張的形容詞。
  - 所有數字必須對應 `raw/`，不自行編造食物價格、蛋白質克數或配速數據。
  - **資料判讀與衛教邊界**：配速與坡度同時變化時只描述觀察到的關聯，不下單一因果結論（CR-01）；不提供醫療診斷或復健處方，出現胸悶、頭暈或關節刺痛一律建議停跑就醫。

---

## 二、檔案讀寫權限矩陣（嚴格遵守）

| 路徑／檔案 | 權限 | 規則說明 |
|---|---|---|
| `raw/**` | **唯讀（READ-ONLY）** | 第一層原始素材區。**嚴禁**修改、重新命名、移動或刪除既有原始筆記；僅能新增來源檔。 |
| `assets/style.css`、`assets/app.js`、`assets/shiba-logo.svg` | **唯讀（READ-ONLY）** | 全站共用的樣式表、搜尋腳本與圖示。新增知識頁時禁止更改配色與共用程式。 |
| `wiki/*.md`、`wiki/index.md` | **讀寫（READ/WRITE）** | 第二層知識中樞。整理摘要、維護雙向連結、記錄需求訪談與索引表。 |
| `pages/<slug>/index.html` | **讀寫（READ/WRITE）** | 第三層靜態互動網頁。依照固定骨架生成新頁，並透過註解錨點更新前後頁導覽。 |
| `slides/<slug>/index.html` | **讀寫（READ/WRITE）** | 教學型 16:9 翻頁簡報成品。僅能依通過檢查的逐頁稿渲染，排版時禁止偷改文案。 |
| `workflows/<topic>/**` | **讀寫（READ/WRITE）** | 簡報工作流的狀態檔案區（`sources.md`、`cards/`、`outline.md`、`drafts/`、`report.md`）。 |
| `scripts/*.py` | **讀寫（READ/WRITE）** | 可執行的驗證與 Lint 腳本，用來取代口頭檢查。 |
| `index.html` | **局部寫入（PATCH ONLY）** | 首頁僅允許在 `<!-- WIKI_CARDS_START -->` 與 `<!-- WIKI_CARDS_END -->` 之間增補知識卡片，或調整簡報精選橫幅連結。 |
| `log.md` / `NOTES.md` | **只增 / 讀寫** | `log.md` 只增不刪；`NOTES.md` 每次收工更新為最新進度。 |

---

## 三、命名與網址規範（強制英文 Kebab-Case）

1. **字元限制**：所有 `wiki/<slug>.md`、`pages/<slug>/index.html` 與 `slides/<slug>/index.html` 的 `<slug>`，僅限小寫英文字母（`a-z`）、數字（`0-9`）與連字號（`-`），須符合 `^[a-z0-9-]+$`。
2. **禁止事項**：禁止在網址路徑使用中文、全形字元、空白、底線（`_`）或大寫英文字母。
3. **三處名稱對齊**：`wiki/<slug>.md`、`pages/<slug>/index.html` 與首頁卡片連結必須使用完全一致的 `<slug>`。

---

## 四、技術棧、頁面骨架與教學簡報規範

### 4.1 技術棧與相對路徑
- **零 Build Step**：全站僅用純 HTML、CSS 與原生 JS，禁止引入 React、Vue、Vite 或 Tailwind CLI。
- **相對路徑**：部署於 GitHub Pages 子目錄時，子頁統一使用相對路徑（如 `../../assets/style.css`），不可寫死 `/` 根路徑。

### 4.2 互動網頁（`pages/<slug>/index.html`）固定骨架
依序具備：頂部導覽列（`header.topbar`）→ 文章標頭（`section.article-head`）→ 核心觀念卡片（`section.section-card`）→ 互動小工具（`section.tool-card`）→ 阿柴教練提醒（`section.coach-box`）→ 延伸閱讀交叉連結（`.cross-links`）→ 上下篇導覽（`nav.pager`，必含 `PREV_LINK_START` 與 `NEXT_LINK_START` 註解錨點）。

### 4.3 教學型 HTML 簡報（`slides/<slug>/index.html`）規格
- 採 16:9 舞台（`1180px × 664px`）自動等比縮放設計，無垂直捲軸，支援鍵盤 `←` / `→` / `Space` 與底部導覽圓點翻頁。
- 每頁底部必須保留出處列（`.slide-source`），清楚標明並連回對應 `wiki/<slug>.md` 與 `raw/<file>.md`。
- 版面密度須在進入 HTML 前於逐頁稿階段驗收完畢（每頁要點 ≤ 5 點、內文 ≤ 220 字、表格 ≤ 5×4 格）；排版階段發現溢出須退回 `drafts/` 縮短文字，**不得**在渲染階段直接修改文字。

---

## 五、標準作業流程（Operations SOP）

### 5.1 收錄新內容（Ingest & Build Page）
讀取 `raw/` 新檔（唯讀不改）→ 撰寫 `wiki/<slug>.md` → 更新關聯頁雙向連結 → 更新 `wiki/index.md` → 建立 `pages/<slug>/index.html` → 更新首頁 `WIKI_CARDS_START` 區塊與前一頁 `NEXT_LINK` 錨點 → 寫入 `log.md` 與 `NOTES.md`。

### 5.2 查詢與回寫（Query）
先讀 `wiki/index.md` 定位主題，再讀對應 `wiki/<slug>.md` 彙整答案；跨篇分析確認後存成新頁。

### 5.3 定期健檢（Lint）
檢查無孤兒頁面、跨頁數據一致、所有內部 `href` / `src` 相對路徑存在且無 404。

### 5.4 教學簡報 Graph + Loop 工作流（詳細規定見 `.agents/workflows/topic-slides.md`）
採 6 節點 4 關卡生產線：`檢索 Wiki (sources.md)` → `[Gate 1]` → `平行證據卡 (cards/*.md)` → `規劃大綱 (outline.md)` → `[Gate 2]` → `單頁小圈寫逐頁稿 (drafts/slides-draft.md)` → `[Gate 3: 出處／數值白名單／因果紅旗／字數密度]` → `渲染簡報 (slides/)` → `[Gate 4: 渲染與溢出檢查]` → `產出報告 (report.md)`。

---

## 六、收工前強制檢查清單（Definition of Done）

每次擴充 Wiki、修改網頁或生成簡報後，在回報完成前必須核對：

- [ ] **1. 唯讀保護**：`raw/**` 既有檔案與 `assets/style.css` 未被修改或刪除。
- [ ] **2. 檔名合規**：所有新頁面與簡報的 `<slug>` 符合 `^[a-z0-9-]+$`。
- [ ] **3. 首頁與索引同步**：`wiki/index.md` 與 `index.html` 卡片數量及 `pages/` 子資料夾數量一致。
- [ ] **4. 雙向連結與導覽錨點**：新舊頁面延伸閱讀互連，且 `PREV_LINK` / `NEXT_LINK` 完整串接。
- [ ] **5. 簡報與工作流腳本驗收**：執行 `python scripts/check_slides_workflow.py` 確認 Gate 1–4 全部通過（不是口頭「檢查一下」）。
- [ ] **6. 工作紀錄更新**：`log.md` 與 `NOTES.md` 已記錄最新執行狀態。
