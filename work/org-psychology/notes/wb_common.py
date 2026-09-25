# -*- coding: utf-8 -*-
"""기초 다지기(주차 b) 공용 부분.

- terms/b.json 의 새 기초 용어를 orgslide_lib.TERMS 에 넣어 준다
  (rules/용어사전.json 은 건드리지 않는다. 사전에 이미 있는 말은 그 표기를 그대로 쓴다).
- 단원마다 되풀이되는 그림 모양(막대, 점 그림, 종 모양 곡선, 흐름 상자)을 함수로 만든다.

wb_units_*.py 가 `from wb_common import *` 로 가져다 쓴다.
"""
import json, math, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import orgslide_lib as L0
from orgslide_lib import (HERE, MANTRA, t, term_name, title, goal, pts, ana, stp, tbl,
                          eng, chk, warn, recap, R, C, L, TX, A, PL, PG, BOX, fig,
                          clear, unit, write)

# ---------------------------------------------------------------- 새 기초 용어 넣기
TERMS_B = os.path.join(HERE, "..", "terms", "b.json")
_NEW = 0
for _e in json.load(open(TERMS_B, encoding="utf-8")):
    _ko = (_e.get("ko") or "").strip()
    _en = (_e.get("en") or "").strip()
    _key = _ko or _en
    assert _key, "이름 없는 용어"
    if _key in L0.TERMS:          # 용어사전에 이미 있으면 그 표기를 그대로 둔다
        continue
    L0.TERMS[_key] = (_ko, _en, (_e.get("say") or "").strip())
    _NEW += 1

WHERE = "이게 이 과목 어디에 나오나"


# ---------------------------------------------------------------- 그림 도우미
def bars(head, pairs, caption, hi=(), ymax=None, suffix="", base=200, note=None):
    """세로 막대 그림. pairs 는 [(이름, 값), ...]."""
    vals = [v for _, v in pairs]
    ymax = ymax or (max(vals) * 1.15 if max(vals) > 0 else 1)
    n = len(pairs)
    w = 430.0 / n
    els = [L(22, base, 462, base, "e", 1)]
    for i, (lab, v) in enumerate(pairs):
        x = 26 + i * w + w * 0.18
        bw = w * 0.64
        h = max(4.0, abs(v) / ymax * (base - 60))
        els.append(R(x, base - h, bw, h, "n2" if i in hi else "n3", 2))
        els.append(TX(x + bw / 2, base - h - 7, ("%s%s" % (v, suffix)), "tb", 3, 15))
        els.append(TX(x + bw / 2, base + 22, lab, "t", 1, 15, maxw=w - 2))
    if note:
        els.append(TX(240, base + 48, note, "tm", 3, 15))
    return fig(head, els, caption, h=270)


def dots(head, points, caption, xlab, ylab, hi=(), note=None):
    """점 그림(산포도). points 는 0~1 로 정규화된 (x, y) 목록."""
    x0, y0, x1, y1 = 70.0, 210.0, 450.0, 40.0
    els = [L(x0, y0, x1, y0, "e", 1), L(x0, y0, x0, y1, "e", 1),
           TX(260, 246, xlab, "t", 1, 15),
           TX(10, 30, ylab, "t", 1, 15, a="start")]
    for i, (px, py) in enumerate(points):
        cx = x0 + px * (x1 - x0)
        cy = y0 - py * (y0 - y1)
        els.append(C(cx, cy, 6, "n2" if i in hi else "n3", 2))
    if note:
        els.append(TX(260, 264, note, "tm", 3, 15))
    return fig(head, els, caption, h=270)


def bell(head, caption, marks=(), note=None, peak="가운데가 가장 두툼해요"):
    """종 모양 곡선 하나. marks 는 [(0~1 위치, 이름), ...] 세로 선."""
    x0, x1, base, top = 40.0, 440.0, 200.0, 50.0
    pts_ = []
    for k in range(41):
        u = k / 40.0
        z = (u - 0.5) * 6.0
        y = base - (base - top) * math.exp(-z * z / 2.0)
        pts_.append((x0 + u * (x1 - x0), y))
    els = [L(x0 - 12, base, x1 + 12, base, "e", 1), PL(pts_, "e2", 1),
           TX(240, 258, peak, "t", 1, 15)]
    for u, name in marks:
        x = x0 + u * (x1 - x0)
        z = (u - 0.5) * 6.0
        y = base - (base - top) * math.exp(-z * z / 2.0)
        els.append(L(x, base, x, y, "e", 2))
        els.append(TX(x, base + 22, name, "tb", 3, 15))
    if note:
        els.append(TX(240, 34, note, "tm", 3, 15))
    return fig(head, els, caption, h=270)


def flow(head, boxes, caption, cls=None, note=None, y=60, bh=70):
    """가로로 늘어선 상자와 화살표. boxes 는 [[줄1, 줄2], ...] (줄2 는 없어도 된다)."""
    n = len(boxes)
    gap = 16.0
    w = (460.0 - gap * (n - 1)) / n
    els = []
    for i, lines in enumerate(boxes):
        x = 10 + i * (w + gap)
        ls = [(s, 15, "tl") for s in lines if s]
        els.append(BOX(x, y, w, bh, ls, (cls[i] if cls else "box"), i + 1))
        if i:
            els.append(A(x - gap + 1, y + bh / 2, x - 3, y + bh / 2, "e2", i + 1))
    if note:
        els.append(TX(240, y + bh + 46, note, "tb", n + 1, 16))
    return fig(head, els, caption, h=270)


def stack(head, rows, caption, note=None):
    """세로로 쌓은 상자 3~4개. rows 는 [(글, 클래스), ...]."""
    els = []
    n = len(rows)
    bh = min(52.0, (196.0 - 12 * (n - 1)) / n)
    for i, (s, c) in enumerate(rows):
        y = 16 + i * (bh + 12)
        els.append(BOX(60, y, 360, bh, [(s, 16, "tl")], c, i + 1))
        if i:
            els.append(A(240, y - 11, 240, y - 2, "e2", i + 1))
    if note:
        els.append(TX(240, 250, note, "tm", n + 1, 15))
    return fig(head, els, caption, h=270)
