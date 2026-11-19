#!/usr/bin/env python3
"""
阿柴教練 LLM Wiki 與教學 HTML 簡報生產線自動化驗收腳本（Gate 1 – Gate 4）
對應規格：AGENTS.md v3 與 .agents/workflows/topic-slides.md
"""

from __future__ import annotations

import argparse
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parent.parent
SLUG_RE = re.compile(r"^[a-z0-9-]+$")
CAUSAL_RED_FLAGS = ("導致", "造成", "使得", "促使", "因此", "因為", "所以")
REQUIRED_GROUNDED_NUMBERS: Dict[str, List[str]] = {
    "01-run-walk-5k-notes.md": ["180 BPM", "60%", "70%", "20", "25"],
    "02-shibajianshan-tcx.md": ["6.649", "41 分 41 秒", "6:16", "173.4", "+11.50%", "4:10", "8:05", "13:37"],
    "03-cvs-nutrition-menu.md": ["85", "38.5", "285", "20", "13", "59"],
    "04-knee-and-warmup.md": ["10", "45", "10%"],
    "05-post-run-cooldown-and-hydration.md": ["120", "300", "500", "750", "0.5"],
    "06-first-5k-race-pacing-plan.md": ["35", "7:00", "7:15", "7:20", "6:50", "1.5", "4.0", "5.0"],
}


class SlideHTMLParser(HTMLParser):
    """解析簡報 HTML 內的 .slide 區塊、文字內容與所有連結/圖片相對路徑。"""

    def __init__(self) -> None:
        super().__init__()
        self.slides: List[Dict[str, object]] = []
        self._in_slide = False
        self._slide_depth = 0
        self._in_source = False
        self._source_depth = 0
        self._in_coach = False
        self._coach_depth = 0
        self._in_heading = False
        self._in_li = False
        self._in_tr = False
        self._skip_text = False
        self.asset_links: List[str] = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, str | None]]) -> None:
        attr_map = dict(attrs)
        cls = (attr_map.get("class") or "").split()

        for key in ("href", "src"):
            val = attr_map.get(key)
            if val and not val.startswith(("http://", "https://", "#", "mailto:")):
                self.asset_links.append(val)

        if tag in ("script", "style"):
            self._skip_text = True
            return

        if tag == "section" and "slide" in cls:
            self._in_slide = True
            self._slide_depth = 1
            self.slides.append({
                "text": [],
                "source_text": [],
                "source_links": [],
                "coach_text": [],
                "headings": [],
                "li_count": 0,
                "tr_count": 0,
            })
            return

        if not self._in_slide:
            return

        self._slide_depth += 1
        cur = self.slides[-1]

        if "slide-source" in cls:
            self._in_source = True
            self._source_depth = 1
        elif self._in_source:
            self._source_depth += 1

        if "coach-strip" in cls:
            self._in_coach = True
            self._coach_depth = 1
        elif self._in_coach:
            self._coach_depth += 1

        if tag in ("h1", "h2"):
            self._in_heading = True
        if tag == "li":
            cur["li_count"] = int(cur["li_count"]) + 1
        if tag == "tr":
            cur["tr_count"] = int(cur["tr_count"]) + 1
        if tag == "a" and self._in_source:
            href = attr_map.get("href") or ""
            if href:
                cur["source_links"].append(href)  # type: ignore[attr-defined]

    def handle_endtag(self, tag: str) -> None:
        if tag in ("script", "style"):
            self._skip_text = False
            return

        if not self._in_slide:
            return

        if tag in ("h1", "h2"):
            self._in_heading = False

        if self._in_source:
            self._source_depth -= 1
            if self._source_depth <= 0:
                self._in_source = False

        if self._in_coach:
            self._coach_depth -= 1
            if self._coach_depth <= 0:
                self._in_coach = False

        self._slide_depth -= 1
        if self._slide_depth <= 0:
            self._in_slide = False

    def handle_data(self, data: str) -> None:
        if self._skip_text or not self._in_slide:
            return
        clean = " ".join(data.split())
        if not clean:
            return
        cur = self.slides[-1]
        cur["text"].append(clean)  # type: ignore[attr-defined]
        if self._in_source:
            cur["source_text"].append(clean)  # type: ignore[attr-defined]
        if self._in_coach:
            cur["coach_text"].append(clean)  # type: ignore[attr-defined]
        if self._in_heading:
            cur["headings"].append(clean)  # type: ignore[attr-defined]


def check_gate_1(errors: List[str]) -> Tuple[List[str], int]:
    """[Gate 1] Wiki 篇數、Kebab-Case 命名、首頁卡片同步與規則檔長度檢查。"""
    raw_files = sorted((ROOT / "raw").glob("*.md"))
    if len(raw_files) < 5:
        errors.append(f"[Gate 1] raw/ 只有 {len(raw_files)} 篇，未達至少 5 篇要求。")

    pages_dirs = sorted([p.name for p in (ROOT / "pages").iterdir() if p.is_dir()])
    for slug in pages_dirs:
        if not SLUG_RE.match(slug):
            errors.append(f"[Gate 1] pages/{slug} 不符合 Kebab-Case 規範 ^[a-z0-9-]+$。")
        if not (ROOT / "wiki" / f"{slug}.md").exists():
            errors.append(f"[Gate 1] 缺少對應 wiki/{slug}.md。")
        if not (ROOT / "pages" / slug / "index.html").exists():
            errors.append(f"[Gate 1] 缺少 pages/{slug}/index.html。")

    # 檢查首頁卡片數與 pages/ 數量一致
    index_html = (ROOT / "index.html").read_text(encoding="utf-8")
    m = re.search(r"<!-- WIKI_CARDS_START -->(.*?)<!-- WIKI_CARDS_END -->", index_html, re.S)
    if not m:
        errors.append("[Gate 1] index.html 缺少 WIKI_CARDS_START / WIKI_CARDS_END 錨點。")
    else:
        cards_hrefs = re.findall(r'href="\./pages/([a-z0-9-]+)/index\.html"', m.group(1))
        if sorted(cards_hrefs) != pages_dirs:
            errors.append(f"[Gate 1] 首頁卡片 {cards_hrefs} 與 pages/ {pages_dirs} 不一致。")

    # 檢查 AGENTS.md 長度 < 12,000 字元
    agents_len = len((ROOT / "AGENTS.md").read_text(encoding="utf-8"))
    if agents_len >= 12000:
        errors.append(f"[Gate 1] AGENTS.md 長度 {agents_len} 字元超過 12,000 上限。")

    # 檢查每張 pages/*/index.html 相對路徑是否真實存在
    for slug in pages_dirs:
        page_path = ROOT / "pages" / slug / "index.html"
        content = page_path.read_text(encoding="utf-8")
        for ref in re.findall(r'(?:href|src)="([^"]+)"', content):
            if ref.startswith(("http://", "https://", "#")):
                continue
            target = (page_path.parent / ref).resolve()
            if not target.exists():
                errors.append(f"[Gate 1] pages/{slug}/index.html 失效相對路徑: {ref}")

    # 檢查證據卡與 sources.md
    wf_dir = ROOT / "workflows" / "topic-first-5k-guide"
    sources_md = (wf_dir / "sources.md").read_text(encoding="utf-8")
    cards = sorted((wf_dir / "cards").glob("*.md"))
    if len(cards) != len(pages_dirs):
        errors.append(f"[Gate 1] 證據卡數量 ({len(cards)}) 與 Wiki 主題數 ({len(pages_dirs)}) 不符。")
    for slug in pages_dirs:
        if f"wiki/{slug}.md" not in sources_md:
            errors.append(f"[Gate 1] sources.md 未納入 wiki/{slug}.md。")

    return pages_dirs, agents_len


def check_gate_2(pages_dirs: List[str], errors: List[str]) -> int:
    """[Gate 2] 檢查大綱頁數 (8-15 頁) 與 6 篇 Wiki 100% 覆蓋率。"""
    outline_text = (ROOT / "workflows" / "topic-first-5k-guide" / "outline.md").read_text(encoding="utf-8")
    slide_rows = re.findall(r"^\|\s*(\d{2})\s*\|", outline_text, re.M)
    if not (8 <= len(slide_rows) <= 15):
        errors.append(f"[Gate 2] outline.md 定義 {len(slide_rows)} 頁，未落在 8–15 頁區間。")

    for slug in pages_dirs:
        if slug not in outline_text:
            errors.append(f"[Gate 2] 大綱遺漏 Wiki 主題：{slug}（應退回 Node 1 或 Node 3 補齊）。")
    return len(slide_rows)


def parse_draft_slides(draft_text: str) -> List[Dict[str, str]]:
    """將 slides-draft.md 拆分為單頁字典列表。"""
    parts = re.split(r"(?=^## Slide \d{2}：)", draft_text, flags=re.M)
    slides = []
    for p in parts:
        p = p.strip()
        if not p.startswith("## Slide "):
            continue
        title_line = p.splitlines()[0]
        wiki_m = re.search(r"\*\*Wiki 出處\*\*：(.+)", p)
        raw_m = re.search(r"\*\*Raw 出處\*\*：(.+)", p)
        h_m = re.search(r"\*\*投影片標題\*\*：(.+)", p)
        sub_m = re.search(r"\*\*副標說明\*\*：(.+)", p)
        coach_m = re.search(r"\*\*阿柴教練一句話\*\*：(.+)", p)
        body_m = re.search(r"\*\*頁面內容\*\*：\s*\n(.*?)(?=\n-\s*\*\*阿柴教練一句話\*\*)", p, re.S)
        slides.append({
            "header": title_line,
            "wiki": wiki_m.group(1).strip() if wiki_m else "",
            "raw": raw_m.group(1).strip() if raw_m else "",
            "title": h_m.group(1).strip() if h_m else "",
            "subtitle": sub_m.group(1).strip() if sub_m else "",
            "body": body_m.group(1).strip() if body_m else "",
            "coach": coach_m.group(1).strip() if coach_m else "",
        })
    return slides


def check_gate_3(draft_text: str, errors: List[str], label: str = "Gate 3") -> List[Dict[str, str]]:
    """[Gate 3] 檢查逐頁稿出處、字數上限、因果紅旗與原始數據接地（Shift-Left）。"""
    slides = parse_draft_slides(draft_text)
    if not (8 <= len(slides) <= 15):
        errors.append(f"[{label}] 逐頁稿共 {len(slides)} 頁，未落在 8–15 頁規格範圍內。")

    # 確認全域數值皆能回溯至 raw/
    for raw_name, nums in REQUIRED_GROUNDED_NUMBERS.items():
        raw_content = (ROOT / "raw" / raw_name).read_text(encoding="utf-8")
        for num in nums:
            if num not in raw_content:
                errors.append(f"[{label}] raw/{raw_name} 找不到預期基準數值: {num}")
            if num not in draft_text:
                errors.append(f"[{label}] 逐頁稿遺漏關鍵數值 ({raw_name}): {num}")

    for idx, s in enumerate(slides, start=1):
        # 1. 出處檢查
        wiki_refs = re.findall(r"wiki/[a-z0-9-]+\.md", s["wiki"])
        if not wiki_refs:
            errors.append(f"[{label}] Slide {idx:02d} 缺少合法的 wiki/*.md 出處標註。")
        else:
            for wf in wiki_refs:
                if not (ROOT / wf).exists():
                    errors.append(f"[{label}] Slide {idx:02d} 引用的 Wiki 檔案不存在: {wf}")

        if not s["raw"]:
            errors.append(f"[{label}] Slide {idx:02d} 缺少 Raw 出處標註。")

        # 2. 視覺密度前置上限（字數 <= 220、要點 <= 5、表格列數 <= 5）
        core_text = f"{s['title']} {s['subtitle']} {s['body']} {s['coach']}"
        compact_len = len(re.sub(r"[\s|*`#\-]+", "", core_text))
        if compact_len > 220:
            errors.append(
                f"[{label}] Slide {idx:02d} 核心字數 {compact_len} 字超過 220 字上限（應單頁 Loop 精簡）。"
            )

        bullets = [line for line in s["body"].splitlines() if line.strip().startswith("- ")]
        table_rows = [line for line in s["body"].splitlines() if line.strip().startswith("|") and "---" not in line]
        if len(bullets) > 5:
            errors.append(f"[{label}] Slide {idx:02d} 要點數量 {len(bullets)} 超過 5 點上限。")
        if len(table_rows) > 5:
            errors.append(f"[{label}] Slide {idx:02d} 表格列數 {len(table_rows)} 超過 5 列上限。")

        # 3. 因果紅旗掃描（保護 CR-01 不被違反）
        for kw in CAUSAL_RED_FLAGS:
            if kw in core_text:
                errors.append(
                    f"[{label}] Slide {idx:02d} 偵測到強因果紅旗詞『{kw}』，請改為客觀關聯描述。"
                )

    return slides


def check_gate_4(draft_slides: List[Dict[str, str]], errors: List[str]) -> int:
    """[Gate 4] 檢查 HTML 簡報渲染頁數、出處連結有效性與文案鎖定一致性。"""
    slide_html_path = ROOT / "slides" / "first-5k-guide" / "index.html"
    html_text = slide_html_path.read_text(encoding="utf-8")

    parser = SlideHTMLParser()
    parser.feed(html_text)

    if len(parser.slides) != len(draft_slides):
        errors.append(
            f"[Gate 4] HTML 投影片數量 ({len(parser.slides)}) 與定稿逐頁稿 ({len(draft_slides)}) 不一致。"
        )

    # 檢查全部站內相對資源是否真實存在
    for link in sorted(set(parser.asset_links)):
        target = (slide_html_path.parent / link).resolve()
        if not target.exists():
            errors.append(f"[Gate 4] slides/first-5k-guide/index.html 失效資源路徑: {link}")

    # 檢查每張 slide 的出處、溢出風險與文案鎖定
    for idx, (hs, ds) in enumerate(zip(parser.slides, draft_slides), start=1):
        source_links = hs["source_links"]  # type: ignore[assignment]
        if not source_links:
            errors.append(f"[Gate 4] Slide {idx:02d} 底部缺少可點擊出處連結 (.slide-source)。")

        all_text = " ".join(hs["text"])  # type: ignore[arg-type]
        if "阿柴教練說：" not in all_text:
            errors.append(f"[Gate 4] Slide {idx:02d} 缺少阿柴教練提醒列。")

        # 文案鎖定比對：確保渲染時未擅自更改逐頁稿的「阿柴教練一句話」
        coach_rendered = " ".join(hs["coach_text"])  # type: ignore[arg-type]
        if ds["coach"] not in coach_rendered:
            errors.append(
                f"[Gate 4] Slide {idx:02d} 阿柴教練文案與定稿 slides-draft.md 不一致（排版時禁止偷改字）。"
            )

        # 單頁渲染文字總長度檢查（排除底部出處列與頁碼徽章，防止 1180x664 舞台核心文字過多）
        body_only_len = len(re.sub(r"\s+", "", all_text)) - len(re.sub(r"\s+", "", " ".join(hs["source_text"])))
        if body_only_len > 300:
            errors.append(
                f"[Gate 4] Slide {idx:02d} 渲染核心字元 {body_only_len} 過長，可能有 16:9 溢出風險（應退回 Node 4）。"
            )

    return len(parser.slides)


def run_self_test() -> int:
    """模擬第 1 輪未將檢查前移時的典型錯誤，驗證腳本確實能攔截問題。"""
    print("=== Self-Test：模擬第 1 輪典型錯誤樣本 ===")
    bad_draft = """
## Slide 01：測試漏出處與字數爆版與假因果

- **來源證據卡**：`cards/02-hill-pacing.md`
- **Wiki 出處**：尚未填寫
- **Raw 出處**：
- **投影片標題**：十八尖山下坡測試
- **副標說明**：因為下坡坡度變陡所以導致配速變快，這證明了坡度造成速度上升。
- **頁面內容**：
  - 要點 1：測試超多文字，重複填充內容以觸發單頁字數上限檢查，看看是否能順利攔截出問題的頁面並指明退回該頁重新精簡，而不是整份重跑浪費時間。這是一段刻意寫得很長很長用來測試超過兩百二十字的模擬段落，包含各種重複敘述與測試字串，確保長度確實超出兩百二十個中文字元門檻。
  - 要點 2：第二點。
  - 要點 3：第三點。
  - 要點 4：第四點。
  - 要點 5：第五點。
  - 要點 6：第六點（超過 5 點上限）。
- **阿柴教練一句話**：測試口號。
"""
    sim_errors: List[str] = []
    check_gate_3(bad_draft, sim_errors, label="Self-Test Gate 3")
    for err in sim_errors:
        print("  [CAUGHT]", err)
    if len(sim_errors) >= 5:
        print(f"Self-Test PASS：成功攔截 {len(sim_errors)} 項模擬違規（缺出處、字數爆版、要點超標、因果紅旗、數值遺漏）。")
        return 0
    print("Self-Test FAIL：未能攔截足夠的模擬違規。")
    return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="檢查阿柴教練 Wiki 與教學簡報工作流")
    parser.add_argument("--self-test", action="store_true", help="執行錯誤攔截自我測試")
    args = parser.parse_args()

    if args.self_test:
        return run_self_test()

    errors: List[str] = []
    pages_dirs, agents_len = check_gate_1(errors)
    outline_count = check_gate_2(pages_dirs, errors)
    draft_text = (ROOT / "workflows" / "topic-first-5k-guide" / "drafts" / "slides-draft.md").read_text(
        encoding="utf-8"
    )
    draft_slides = check_gate_3(draft_text, errors)
    html_count = check_gate_4(draft_slides, errors)

    print("=== 阿柴教練 LLM Wiki 與教學簡報工作流驗收結果 ===")
    print(f"- Gate 1 (Wiki & Kebab-Case & AGENTS.md): {len(pages_dirs)} 篇 Wiki / AGENTS.md {agents_len} 字元")
    print(f"- Gate 2 (Outline & 100% Coverage):       {outline_count} 頁大綱，涵蓋 {len(pages_dirs)}/{len(pages_dirs)} 篇")
    print(f"- Gate 3 (Draft Shift-Left Check):        {len(draft_slides)} 頁逐頁稿（出處／字數／因果／數值接地）")
    print(f"- Gate 4 (HTML Render & Lock Check):      {html_count} 張 HTML 投影片與相對路徑檢查")

    if errors:
        print("\n[FAIL] 發現以下問題：")
        for e in errors:
            print("  -", e)
        return 1

    print("\n[PASS] Gate 1 至 Gate 4 全數通過！")
    return 0


if __name__ == "__main__":
    sys.exit(main())
