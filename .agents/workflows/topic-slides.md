---
description: 從阿柴教練 LLM Wiki 產生教學型翻頁 HTML 簡報的 Graph + Loop 工作流程（對應 /topic-slides）
---

# Workflow：`topic-slides`（Wiki → 教學型 HTML 簡報生產線）

本工作流程將「從 LLM Wiki 生成 12 頁教學型翻頁 HTML 簡報」拆成 **6 個節點（Nodes）與 4 道自動檢查關卡（Gates）**，關鍵節點內部嵌入單頁粒度的小圈 Loop，避免到最後渲染時才整份重跑。

## 一、Graph 總覽與退回路線（Rollback Edges）

```text
[Node 1: 檢索 Wiki] ──▶ (Gate 1: 覆蓋率與命名檢查) ──▶ [Node 2: 平行抽取證據卡]
       ▲                     │ 不足 >= 3 篇                    │
       │                     ▼                                 ▼
       │                 停止或補檢索                  [Node 3: 規劃教學大綱]
       │                                                       │
       └────────── 缺子題退回補檢索 ◀── (Gate 2: 結構、覆蓋率與人工確認)
                                                               │
                                                               ▼
       ┌────── 單頁忠實度/字數/因果未過（小圈 Loop <= 2 輪） ◀── [Node 4: 逐頁稿]
       │                                                       │
       └──────────────────────────────────────────────▶ (Gate 3: 前置綜合驗收)
                                                               │
                                                               ▼
                                                       [Node 5: 渲染 HTML]
                                                               │
                                   退回縮短對應頁 ◀──── (Gate 4: 渲染與溢出檢查)
                                                               │
                                                               ▼
                                                       [Node 6: 輸出交件與報告]
```

## 二、各節點權限邊界（只能看什麼、不能做什麼）

| 節點 / 關卡 | 輸入檔案（只能看） | 輸出檔案 | 禁止事項（不能做） | 失敗時處理 |
|---|---|---|---|---|
| **Node 1：檢索 Wiki** | `wiki/index.md`、`wiki/*.md` | `workflows/<topic>/sources.md` | 不得直接讀取外部網路資料硬湊 | 相關頁 `< 3` 篇立即停下 |
| **Node 2：證據卡（平行）** | **單篇** `wiki/<slug>.md` ＋ 對應 `raw/<file>.md` | `workflows/<topic>/cards/*.md` | **嚴禁**混入其他篇內容或外部常識；必列「精確數值白名單」與「禁用因果清單」 | 數值無法對應 `raw/` 時退回重抽該張卡 |
| **Node 3：大綱與 Gate 2** | `sources.md`、`cards/*.md` | `workflows/<topic>/outline.md` | 不得遺漏任何 1 篇已檢索核心 Wiki | 缺子題退回 Node 1；順序不順只改大綱 |
| **Node 4：逐頁稿與 Gate 3** | `outline.md` ＋ 該頁指派的 `cards/*.md` | `workflows/<topic>/drafts/slides-draft.md` | 禁止引用卡片白名單外的數字；禁止把同向變化寫成因果（CR-01）；字數超標時精簡，不得省略出處 | 哪一頁沒過 Gate 3，就用小圈 Loop **只修那一頁**（上限 2 輪） |
| **Node 5：渲染 HTML 與 Gate 4** | 已通過 Gate 3 的 `drafts/slides-draft.md` | `slides/<slug>/index.html`、`workflows/<topic>/deck.html` | **嚴禁在排版時順手修改任何一句文字、數字或結論** | 版面溢出時退回 Node 4 縮短該頁字數，不可偷改字 |
| **Node 6：交件與檢查報告** | 上述狀態檔與 `scripts/check_slides_workflow.py` 執行結果 | `workflows/<topic>/report.md` | 不得未執行腳本就宣告通過 | 逐項列出 Gate 1–4 實測紀錄 |

## 三、四道自動化檢查關卡（Shift-Left Check）

執行指令：

```bash
python scripts/check_slides_workflow.py
```

1. **Gate 1（來源與命名）**：確認 `raw/` 至少 5 篇、`wiki/` 頁面數與 `sources.md`、`cards/*.md` 數量對齊，且所有 `<slug>` 符合 `^[a-z0-9-]+$`。
2. **Gate 2（大綱與覆蓋率）**：確認 `outline.md` 頁數落在 8–15 頁區間，且全部 6 篇 Wiki 在大綱聯集內達到 100% 覆蓋。
3. **Gate 3（逐頁稿前置防呆 — Shift-Left）**：
   - 每頁必須標註真實存在的 `wiki/<slug>.md` 與 `raw/<file>.md`。
   - 嚴格檢查強因果詞紅旗（`導致`、`造成`、`使得`、`促使`、`證明`、`因為` 等）：特別在十八尖山路線數據頁，禁止出現違反 CR-01 的因果推論。
   - 視覺密度前置上限：每頁條列要點 `<= 5` 點、內文總字數 `<= 220` 字、表格 `<= 5x4` 格，避免進入 HTML 後才爆版。
   - 關鍵數值必須可在對應 `raw/` 檔案中對齊。
4. **Gate 4（HTML 渲染與出處連結）**：
   - 檢查 `slides/first-5k-guide/index.html` 實際包含 12 張 `.slide`、每張皆含 `.slide-source` 出處連結且指向真實存在的 `../../wiki/*.md`。
   - 檢查相對路徑資源（`../../assets/shiba-logo.svg`）存在，且單頁內文字數與元素未超過 16:9 舞台安全範圍。

## 四、停止條件與剎車機制

- 單頁小圈 Loop **最多修改 2 輪**，整條 Graph 跨關退回 **上限 3 輪**；超過上限仍無法通過則停止並交由人工介入。
- 若 `sources.md` 檢索到的相關 Wiki 少於 3 篇，直接停止生成簡報，先回頭擴充 `raw/` 與 `wiki/`，不可用模型自身知識硬湊。
