# -*- coding: utf-8 -*-
"""조직심리학 회독 레슨 공통 도우미. build_O*_*.py 가 불러 쓴다.

look 상자 좌표는 PDF 글자 층에서 계산한다: rg(쪽, x0, y0, x1, y1) 은 그 네모(쪽 비율) 안에
가운데가 들어가는 글 줄들을 모두 덮는 상자를 돌려준다. 글자 층에 없는 그림 속 글자는 fixed 좌표를 쓴다.
"""
import json, os, re, sys

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
W_DIR = os.path.join(ROOT, "work", "org-psychology")
DICT = os.path.join(W_DIR, "rules", "용어사전.json")
BAD = "—–·・"

_cfg = json.load(open(os.path.join(W_DIR, "subject.json"), encoding="utf-8"))
_docs = {}


def _doc(deck):
    if deck not in _docs:
        _docs[deck] = fitz.open(os.path.normpath(os.path.join(ROOT, _cfg["decks"][deck]["pdf"])))
    return _docs[deck]


_lines = {}


def lines(deck, p):
    key = (deck, p)
    if key not in _lines:
        pg = _doc(deck)[p - 1]
        W, H = pg.rect.width, pg.rect.height
        out = []
        for b in pg.get_text("dict")["blocks"]:
            if b["type"] != 0:
                continue
            for ln in b["lines"]:
                t = "".join(s["text"] for s in ln["spans"]).strip()
                if not t:
                    continue
                x0, y0, x1, y1 = ln["bbox"]
                cx, cy = (x0 + x1) / 2 / W, (y0 + y1) / 2 / H
                if cy < 0.09 and cx > 0.62:      # 오른쪽 위 머리글
                    continue
                out.append((x0 / W, y0 / H, x1 / W, y1 / H, t))
        _lines[key] = out
    return _lines[key]


def rg(deck, p, x0, y0, x1, y1, pad=0.008):
    """네모 안에 가운데가 들어가는 글 줄을 모두 덮는 상자 (x, y, w, h)"""
    hit = [l for l in lines(deck, p) if x0 <= (l[0] + l[2]) / 2 <= x1 and y0 <= (l[1] + l[3]) / 2 <= y1]
    if not hit:
        raise SystemExit(f"{deck} p.{p}: 네모 {x0, y0, x1, y1} 안에 글 줄이 없어요")
    a = max(0, min(l[0] for l in hit) - pad)
    b = max(0, min(l[1] for l in hit) - pad)
    c = min(1, max(l[2] for l in hit) + pad)
    d = min(1, max(l[3] for l in hit) + pad)
    return (round(a, 3), round(b, 3), round(c - a, 3), round(d - b, 3))


# ---------- 장면 도우미 ----------
def say(*l):
    return {"kind": "say", "lines": list(l)}


def pts(head, *items):
    return {"kind": "points", "head": head, "items": list(items)}


def ana(head, scene, pairs):
    return {"kind": "analogy", "head": head, "scene": scene, "map": [list(x) for x in pairs]}


def fig(head, svg, caption, builds=1):
    return {"kind": "figure", "head": head, "svg": svg, "caption": caption, "builds": builds}


def cmp(head, cols, rows):
    return {"kind": "compare", "head": head, "cols": list(cols), "rows": [list(r) for r in rows]}


def steps(head, st, answer, given=None):
    d = {"kind": "steps", "head": head, "steps": list(st), "answer": answer}
    if given:
        d["given"] = given
    return d


def chk(q, choices, a, why):
    return {"kind": "check", "q": q, "choices": list(choices), "a": a, "why": why}


def bg(src, *l):
    return {"kind": "bg", "src": src, "lines": list(l)}


def prof(when, *l):
    return {"kind": "prof", "when": when, "lines": list(l)}


def eng(head, en, ko, tip=None):
    d = {"kind": "english", "head": head, "en": en, "ko": ko}
    if tip:
        d["tip"] = tip
    return d


def warn(head, *items):
    return {"kind": "warn", "head": head, "items": list(items)}


class Deck:
    """deck = Deck("O2"); deck.look(p, head, (region, say), ...)  region 은 rg 인자 (x0, y0, x1, y1) 또는 ("fix", x, y, w, h)"""

    def __init__(self, deck):
        self.deck = deck

    def box(self, p, reg):
        if reg[0] == "fix":
            return tuple(round(v, 3) for v in reg[1:])
        return rg(self.deck, p, *reg)

    def look(self, p, head, *parts):
        bs = []
        for reg, s in parts:
            x, y, w, h = self.box(p, reg)
            bs.append({"x": x, "y": y, "w": w, "h": h, "say": s})
        assert 1 <= len(bs) <= 6, (p, head, len(bs))
        return {"kind": "look", "head": head, "boxes": bs}


def load_dict():
    return json.load(open(DICT, encoding="utf-8"))


def write_lesson(deck, lo, hi, slides, extra_gloss=()):
    """쪽 목록을 검사하고 glossary 를 붙여 저장한다. glossary 는 용어사전에서 이 범위 글에 나오는 용어 + extra_gloss"""
    dic = load_dict()
    body = json.dumps(slides, ensure_ascii=False)
    used = set()
    for s in slides:
        used.update(t.lower() for t in s.get("terms", []))
    gl = []
    for g in dic:
        key = (g["en"] or g["ko"]).lower()
        if key in used:
            gl.append({k: g[k] for k in ("ko", "en", "say", "more") if g.get(k) is not None})
    have = {(g["en"] or g["ko"]).lower() for g in gl}
    for g in extra_gloss:
        if (g["en"] or g["ko"]).lower() not in have:
            gl.append(g)
    known = {(g["en"] or g["ko"]).lower() for g in dic} | {(g["en"] or g["ko"]).lower() for g in extra_gloss}
    miss = sorted(used - known)
    if miss:
        raise SystemExit(f"terms 에 사전에 없는 용어: {miss}")
    out = {"deck": deck, "from": lo, "to": hi, "glossary": gl, "slides": slides}
    raw = json.dumps(out, ensure_ascii=False, indent=1)
    for c in BAD:
        if c in raw:
            i = raw.index(c)
            raise SystemExit(f"금지 문자 {c!r}: ...{raw[max(0, i - 40):i + 10]}")
    path = os.path.join(HERE, f"{deck}_{lo:03d}-{hi:03d}.json")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(raw)
    print("저장", path, len(slides), "쪽, 용어", len(gl))


def T(*names):
    """terms 목록: 용어사전의 en(없으면 ko)"""
    dic = load_dict()
    idx = {}
    for g in dic:
        for k in (g["ko"], g["en"]):
            if k:
                idx[k.lower()] = (g["en"] or g["ko"])
    out = []
    for n in names:
        if n.lower() not in idx:
            raise SystemExit(f"용어사전에 없는 용어: {n}")
        out.append(idx[n.lower()])
    return out


def dump(deck, pages):
    """작성용: 쪽의 글 줄 좌표 보기"""
    sys.stdout.reconfigure(encoding="utf-8")
    for p in pages:
        print(f"== {deck} p.{p}")
        for x0, y0, x1, y1, t in sorted(lines(deck, p), key=lambda l: (round(l[1], 2), l[0])):
            print(f"  x{x0:.2f}-{x1:.2f} y{y0:.3f}-{y1:.3f} {t[:70]}")


if __name__ == "__main__":
    dump(sys.argv[1], [int(x) for x in sys.argv[2].split(",")])
