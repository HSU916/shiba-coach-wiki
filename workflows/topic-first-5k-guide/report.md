# Node 6 產出：實際執行結果與檢查紀錄（`report.md`）

- 簡報主題：`從零跑完第一個 5K：阿柴教練新手指南`
- 成品位置：`slides/first-5k-guide/index.html`（共 12 頁）
- 驗收腳本：`scripts/check_slides_workflow.py`

---

## 一、三輪實際執行與退回修正紀錄

### 第 1 輪：初版流程（檢查關卡放在最後渲染後）
- **執行結果**：FAIL（共攔截 3 類問題，而且是做完整份 HTML 簡報後才發現，必須從最後一關退回前面重來）：
  1. **字數爆版與偷改文案**：第 6 頁原本塞了十八尖山統計與 4 段地形表，導致單頁高度超過 16:9 舞台；修正版面時模型容易順手改動原本寫好的數字或句子。
  2. **違反 CR-01 因果邊界**：草稿把「`6200m–6400m`（`-9.00%`）下坡配速 `4:10/km`」寫成「因為陡下坡導致配速變快」，忽略了緊接著的 `6400m–6600m`（`-10.20%`）反而放慢成 `8:05/km`。
  3. **覆蓋率與出處遺漏**：第 11 頁漏標 `wiki/cvs-recovery.md` 出處，且大綱漏掉第 5 篇 `cooldown-and-hydration.md`（覆蓋率 5/6）。

### 流程改進：把檢查關卡往前移（Shift-Left）
依照第二輪與 Gemini 討論的建議修改 Graph 設計：
1. 在 **Node 2（證據卡）** 先抽「精確數值白名單」與「CR-01 因果禁用提醒」，不讓模型到後面自己猜數字。
2. 在 **Gate 2（大綱）** 直接寫腳本檢查 6 篇 Wiki 是否 100% 納入，把單頁的十八尖山資料拆成第 6 頁（實測統計）與第 7 頁（上下坡對照與因果邊界）。
3. 在 **Gate 3（逐頁稿）** 提前加入字數密度上限（`<= 220` 字、要點 `<= 5`、表格 `<= 5x4`）、強因果連接詞紅旗掃描（`導致`、`造成`、`使得`、`促使`、`因此`、`因為`、`所以`）與 `raw/` 數值核對；同時在 **Node 5（HTML 渲染）** 鎖死文字內容，不准排版時偷改句子。

### 第 2 輪：套用 Shift-Left 關卡與單頁小圈 Loop
- **執行結果**：Gate 1 與 Gate 2 一次通過（6/6 篇 Wiki 覆蓋率 100%）。進入 Gate 3 執行 `python scripts/check_slides_workflow.py` 時，腳本馬上在 **逐頁稿階段** 抓出 12 頁文字普遍偏長（介於 225–328 字，超過 220 字門檻），以及時間寫法 `41:41` 與 `raw/02` 原文 `41 分 41 秒` 不一致。
- **修正方式（Node 4 單頁 Loop）**：不需重跑大綱與證據卡，只在 `drafts/slides-draft.md` 進行一輪單頁精簡（各頁壓縮至 220 字內並對齊 `41 分 41 秒`），再同步鎖定更新至 `slides/first-5k-guide/index.html`。

### 第 3 輪：最終驗收（Gate 1 – Gate 4 全過）
- **執行指令**：`python scripts/check_slides_workflow.py`（另加 `--self-test` 驗證腳本確實能抓錯）。
- **最終結論**：**PASS（0 錯誤）**，12 頁簡報全數通過字數上限、出處連結、數值接地、CR-01 因果邊界與相對路徑檢查。

---

## 二、終端機驗收輸出紀錄

### 1. 正式生產線全關卡驗收（`python scripts/check_slides_workflow.py`）

```text
=== 阿柴教練 LLM Wiki 與教學簡報工作流驗收結果 ===
- Gate 1 (Wiki & Kebab-Case & AGENTS.md): 6 篇 Wiki / AGENTS.md 3881 字元
- Gate 2 (Outline & 100% Coverage):       12 頁大綱，涵蓋 6/6 篇
- Gate 3 (Draft Shift-Left Check):        12 頁逐頁稿（出處／字數／因果／數值接地）
- Gate 4 (HTML Render & Lock Check):      12 張 HTML 投影片與相對路徑檢查

[PASS] Gate 1 至 Gate 4 全數通過！
```

### 2. 錯誤攔截自我測試（`python scripts/check_slides_workflow.py --self-test`）

```text
=== Self-Test：模擬第 1 輪典型錯誤樣本 ===
  [CAUGHT] [Self-Test Gate 3] 逐頁稿共 1 頁，未落在 8–15 頁規格範圍內。
  ...（省略 36 行關鍵數值遺漏檢查）...
  [CAUGHT] [Self-Test Gate 3] Slide 01 缺少合法的 wiki/*.md 出處標註。
  [CAUGHT] [Self-Test Gate 3] Slide 01 缺少 Raw 出處標註。
  [CAUGHT] [Self-Test Gate 3] Slide 01 核心字數 222 字超過 220 字上限（應單頁 Loop 精簡）。
  [CAUGHT] [Self-Test Gate 3] Slide 01 要點數量 6 超過 5 點上限。
  [CAUGHT] [Self-Test Gate 3] Slide 01 偵測到強因果紅旗詞『導致』，請改為客觀關聯描述。
  [CAUGHT] [Self-Test Gate 3] Slide 01 偵測到強因果紅旗詞『造成』，請改為客觀關聯描述。
  [CAUGHT] [Self-Test Gate 3] Slide 01 偵測到強因果紅旗詞『因為』，請改為客觀關聯描述。
  [CAUGHT] [Self-Test Gate 3] Slide 01 偵測到強因果紅旗詞『所以』，請改為客觀關聯描述。
Self-Test PASS：成功攔截 44 項模擬違規（缺出處、字數爆版、要點超標、因果紅旗、數值遺漏）。
```
