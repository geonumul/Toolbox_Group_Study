# -*- coding: utf-8 -*-
"""실습 노트북을 '쪽'으로 나누고 쪽마다 노트북 모양 그림을 만든다 (실습 덱 N2L, N3L).

사용: python work/nlp/labs/build_lab_pages.py [--no-img]
  쪽 나누기: 코드 셀 하나 = 한 쪽 (바로 앞 설명 셀들을 같이 붙임). 긴 소개 설명 셀과 끝 정리 설명 셀은 따로 한 쪽.
출력
  work/nlp/labs/<덱>_pages.json   [{"p", "title", "cells": [{"n": 셀 번호, "type", "src", "out"}]}]  (레슨 작성용)
  work/nlp/_src/png/<덱>/pNNN.png  (가로 1400px, 작성용)
  subjects/nlp/img/<덱>/pNNN.jpg   (가로 1000px, 사이트용)
그림은 헤드리스 Chrome 으로 찍는다 (사용자 창을 띄우지 않고, 따로 둔 프로필 폴더 사용).
"""
import html, json, os, pathlib, re, subprocess, sys, tempfile

import markdown
from PIL import Image
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import PythonLexer

sys.stdout.reconfigure(encoding="utf-8")
W = pathlib.Path(__file__).resolve().parent.parent
ROOT = W.parent.parent
SRC = ROOT.parent.parent / "01_수업자료" / "자연어처리" / "코드와과제"
LABS = {
    "N2L": SRC / "02주차" / "Lab0-1_Tokenization and Word Vectors_full.ipynb",
    "N3L": SRC / "03주차" / "Lab2_Neural Nets and RNN Language Models.ipynb",
    "N4L": SRC / "04주차" / "Lab3_Self-Attention from Scratch_Full.ipynb",
}
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
FONT = ROOT.parent.parent / "02_작업" / "그래프신경망" / "번역" / "_tools" / "fonts"
TMP = pathlib.Path(os.environ.get("NLP_LAB_TMP") or tempfile.gettempdir()) / "nlp_lab_pages"


def cell_out(c):
    t = ""
    for o in c.get("outputs", []):
        if "text" in o:
            t += "".join(o["text"])
        elif "data" in o:
            d = o["data"]
            if "text/plain" in d:
                t += "".join(d["text/plain"]) + "\n"
            if "image/png" in d:
                t += "[그림 출력]\n"
    return t.rstrip()


def split_pages(nb):
    cells = [{"n": i, "type": c["cell_type"], "src": "".join(c["source"]).rstrip(), "out": cell_out(c) if c["cell_type"] == "code" else ""}
             for i, c in enumerate(nb["cells"], 1)]
    cells = [c for c in cells if c["src"].strip()]
    pages, pend = [], []
    for c in cells:
        if c["type"] == "markdown":
            long_intro = c["src"].lstrip().startswith("# ") or len(c["src"].splitlines()) >= 14
            if long_intro:
                if pend:
                    pages.append(pend)
                    pend = []
                pages.append([c])
            else:
                pend.append(c)
        else:
            pages.append(pend + [c])
            pend = []
    if pend:
        pages.append(pend)
    out = []
    for i, pg in enumerate(pages, 1):
        title = ""
        for c in pg:
            if c["type"] == "markdown":
                hs = re.findall(r"^#{1,4}\s+(.+)$", c["src"], re.M)
                if hs:
                    title = hs[-1]
        if not title:
            code = next((c for c in pg if c["type"] == "code"), None)
            first = code["src"].splitlines()[0] if code else pg[0]["src"].splitlines()[0]
            title = first.lstrip("# ").strip()
        out.append({"p": i, "title": re.sub(r"[*`]", "", title)[:80], "cells": pg})
    return out


CSS = """
@font-face{font-family:Pret;src:url('FONTDIR/Pretendard-Regular.ttf')}
@font-face{font-family:Pret;font-weight:700;src:url('FONTDIR/Pretendard-Bold.ttf')}
html,body{margin:0;background:#fff}
body{width:1400px;box-sizing:border-box;padding:34px 44px 40px;font-family:Pret,'Malgun Gothic',sans-serif;color:#1f2328;font-size:24px;line-height:1.5}
.top{display:flex;justify-content:space-between;color:#6b7280;font-size:19px;border-bottom:2px solid #e5e7eb;padding-bottom:8px;margin-bottom:18px}
.md h1{font-size:34px;margin:6px 0 12px}.md h2{font-size:30px;margin:6px 0 10px}.md h3{font-size:27px;margin:6px 0 8px}
.md p{margin:8px 0}.md hr{display:none}.md blockquote{margin:10px 0;padding:6px 16px;border-left:5px solid #cbd5e1;color:#374151;background:#f8fafc}
.md table{border-collapse:collapse;margin:10px 0;font-size:21px}.md td,.md th{border:1px solid #d1d5db;padding:5px 10px;text-align:left}
.md code{font-family:Consolas,'Malgun Gothic',monospace;background:#f3f4f6;padding:1px 5px;border-radius:3px;font-size:.92em}
.cell{display:flex;margin:14px 0}.cn{width:78px;flex:none;color:#2563eb;font-family:Consolas,monospace;font-size:19px;padding-top:12px}
.cb{flex:1;min-width:0}
.src{background:#f6f8fa;border:1px solid #e1e4e8;border-radius:4px;padding:10px 12px;font-family:Consolas,'Malgun Gothic',monospace;font-size:21px;line-height:1.42;white-space:pre-wrap;word-break:break-all}
.src .ln{display:inline-block;width:38px;color:#9ca3af;user-select:none}
.out{margin-top:6px;padding:8px 12px;font-family:Consolas,'Malgun Gothic',monospace;font-size:19px;line-height:1.38;white-space:pre-wrap;word-break:break-all;color:#111;border-left:4px solid #d1d5db;max-height:none}
.outl{font-size:16px;color:#6b7280;font-family:Pret,sans-serif;margin-top:8px}
""" + HtmlFormatter(style="friendly").get_style_defs(".src")


def code_html(src):
    hl = highlight(src, PythonLexer(), HtmlFormatter(nowrap=True, style="friendly"))
    lines = hl.rstrip("\n").split("\n")
    return "\n".join(f'<span class="ln">{i}</span>{l}' for i, l in enumerate(lines, 1))


def page_html(deck, title, pg, total):
    body = [f'<div class="top"><span>{html.escape(title)}</span><span>{deck}  {pg["p"]} / {total}</span></div>']
    for c in pg["cells"]:
        if c["type"] == "markdown":
            src, prev = [], ""
            for ln in c["src"].split("\n"):   # 목록 앞에 빈 줄이 없으면 markdown 이 목록으로 안 읽는다
                if re.match(r"\s*(\d+\.|[-*])\s", ln) and prev.strip() and not re.match(r"\s*(\d+\.|[-*])\s", prev):
                    src.append("")
                src.append(ln)
                prev = ln
            body.append('<div class="md">' + markdown.markdown("\n".join(src), extensions=["tables"]) + "</div>")
        else:
            out = c["out"]
            if len(out.splitlines()) > 26:
                ls = out.splitlines()
                out = "\n".join(ls[:24]) + f"\n... (출력 {len(ls) - 24}줄 더)"
            o = (f'<div class="outl">실행 결과 (강의 노트북에 저장된 출력)</div><div class="out">{html.escape(out)}</div>' if out else "")
            body.append(f'<div class="cell"><div class="cn">셀 {c["n"]}</div><div class="cb"><div class="src">{code_html(c["src"])}</div>{o}</div></div>')
    css = CSS.replace("FONTDIR", FONT.as_uri())
    return '<!doctype html><html><head><meta charset="utf-8"><style>' + css + '</style></head><body>' + "".join(body) + '</body></html>'


def shoot(htmlfile, png):
    prof = TMP / "chrome_profile"
    prof.mkdir(parents=True, exist_ok=True)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--user-data-dir={prof}", "--no-first-run",
                    "--force-device-scale-factor=1", "--window-size=1400,4000", f"--screenshot={png}", htmlfile.as_uri()],
                   check=True, capture_output=True, timeout=120)
    im = Image.open(png).convert("RGB")
    g = im.convert("L")
    w, h = g.size
    px = g.load()
    bottom = h - 1
    while bottom > 50 and all(px[x, bottom] > 250 for x in range(0, w, 7)):
        bottom -= 1
    return im.crop((0, 0, w, min(h, bottom + 34)))


def main(img=True, only=None):
    """only: 만들 덱 이름 목록 (없으면 전부). 예 python build_lab_pages.py N4L"""
    TMP.mkdir(parents=True, exist_ok=True)
    for deck, f in LABS.items():
        if only and deck not in only:
            continue
        nb = json.loads(f.read_text(encoding="utf-8"))
        pages = split_pages(nb)
        (W / "labs" / f"{deck}_pages.json").write_text(json.dumps({"deck": deck, "file": f.name, "pages": pages}, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{deck}: {len(pages)}쪽 ({f.name})")
        if not img:
            continue
        site = ROOT / "subjects" / "nlp" / "img" / deck
        pngd = W / "_src" / "png" / deck
        site.mkdir(parents=True, exist_ok=True)
        pngd.mkdir(parents=True, exist_ok=True)
        for pg in pages:
            hf = TMP / f"{deck}_p{pg['p']:03d}.html"
            hf.write_text(page_html(deck, pg["title"], pg, len(pages)), encoding="utf-8")
            raw = TMP / f"{deck}_p{pg['p']:03d}_raw.png"
            im = shoot(hf, raw)
            im.save(pngd / f"p{pg['p']:03d}.png")
            im.resize((1000, round(im.size[1] * 1000 / im.size[0])), Image.LANCZOS).save(site / f"p{pg['p']:03d}.jpg", quality=80)
        print(f"  그림 {len(pages)}장 -> {site}")


if __name__ == "__main__":
    main("--no-img" not in sys.argv, [a for a in sys.argv[1:] if a in LABS])
