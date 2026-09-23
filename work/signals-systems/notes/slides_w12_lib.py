"""신호및시스템 1, 2주차 정리 슬라이드 공용 도우미 (build_slides_w1.py, build_slides_w2.py 가 불러 씀)."""
import json, math, os, re, sys
from xml.sax.saxutils import escape

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
DICT = os.path.join(HERE, "..", "rules", "용어사전.json")

# ---------------------------------------------------------------- 용어 표 (용어사전 표기 그대로)
TERMS = {}
for _t in json.load(open(DICT, encoding="utf-8")):
    _ko, _en = (_t.get("ko") or "").strip(), (_t.get("en") or "").strip()
    _key = _ko or _en
    if _key and _key not in TERMS:
        TERMS[_key] = (_ko, _en, _t.get("say", ""))


def josa(word, pair):
    """받침에 맞는 조사 (은/는, 이/가, 을/를, 과/와, 으로/로, 이에요/예요, 이라고/라고)."""
    x, y = pair.split("/")
    if x in ("은", "을", "과") or x[0] in "이으":
        a, b = x, y
    else:
        a, b = y, x
    ch = word.strip()[-1]
    ro = a == "으로"
    if "가" <= ch <= "힣":
        jong = (ord(ch) - 0xAC00) % 28
        has = jong != 0 and not (ro and jong == 8)
    elif ch.upper() in "LMNR":
        has = not (ro and ch.upper() in "LR")
    elif ch in "013678":
        has = not (ro and ch in "178")
    else:
        has = False
    return a if has else b


def show(key, p=""):
    if key not in TERMS:
        raise KeyError("모르는 용어: " + key)
    ko, en, _ = TERMS[key]
    name = "**%s(%s)**" % (ko, en) if ko and en else "**%s**" % (ko or en)
    return name + (josa(key, p) if p else "")


def fill(o):
    if isinstance(o, str):
        return re.sub(r"\[\[(.+?)(?:\|(.+?))?\]\]", lambda m: show(m.group(1), m.group(2) or ""), o)
    if isinstance(o, list):
        return [fill(x) for x in o]
    if isinstance(o, dict):
        return {k: (v if k == "svg" else fill(v)) for k, v in o.items()}
    return o


def S(s, **kw):
    """<<이름>> 자리에 값을 넣는다 (TeX 중괄호와 안 부딪히게)."""
    for k, v in kw.items():
        s = s.replace("<<%s>>" % k, str(v))
    assert "<<" not in s, s
    return s


def num(x, d=3):
    """보기 좋은 숫자 글자 (끝의 0 제거)."""
    if abs(x - round(x)) < 1e-9:
        return str(int(round(x)))
    s = ("%." + str(d) + "f") % x
    return s.rstrip("0").rstrip(".")


# ---------------------------------------------------------------- 슬라이드 도우미
def title(big, sub):
    assert len(big) <= 20, big
    return {"kind": "title", "big": big, "sub": sub}


def goal(*items):
    assert 2 <= len(items) <= 4
    return {"kind": "goal", "items": list(items)}


def pts(head, *items):
    assert 2 <= len(items) <= 5, head
    return {"kind": "points", "head": head, "items": list(items)}


def ana(head, scene, *pairs):
    assert 2 <= len(pairs) <= 4
    return {"kind": "analogy", "head": head, "scene": scene, "map": [list(p) for p in pairs]}


def fml(head, tex, parts, whole):
    assert 2 <= len(parts) <= 6, head
    return {"kind": "formula", "head": head, "tex": tex,
            "parts": [{"sym": s, "say": w} for s, w in parts], "whole": whole}


def stp(head, given, steps, answer):
    assert 3 <= len(steps) <= 7, head
    d = {"kind": "steps", "head": head, "steps": list(steps), "answer": answer}
    if given:
        d["given"] = given
    return d


def cmp(head, cols, rows):
    assert 2 <= len(cols) <= 4 and 2 <= len(rows) <= 6, head
    for r in rows:
        assert len(r) == len(cols), r
    return {"kind": "compare", "head": head, "cols": list(cols), "rows": [list(r) for r in rows]}


def chk(q, choices, a, why):
    assert 2 <= len(choices) <= 4 and 0 <= a < len(choices)
    return {"kind": "check", "q": q, "choices": list(choices), "a": a, "why": why}


def warn(head, *items):
    assert 1 <= len(items) <= 3
    return {"kind": "warn", "head": head, "items": list(items)}


def recap(*items):
    assert 3 <= len(items) <= 4
    return {"kind": "recap", "items": list(items)}


# ---------------------------------------------------------------- SVG 도우미 (클래스만)
W = 480
_TEXTS = []


def tw(s, size):
    w = 0.0
    for ch in s:
        w += 0.3 if ch == " " else (1.0 if ord(ch) > 0x2E80 else 0.6)
    return w * size


def _c(c, b):
    return c + (" b%d" % b if b else "")


def R(x, y, w, h, c="box", b=0, rx=2):
    assert 0 <= rx <= 3
    return '<rect x="%g" y="%g" width="%g" height="%g" rx="%g" class="%s"/>' % (x, y, w, h, rx, _c(c, b))


def C(cx, cy, r, c="n", b=0):
    return '<circle cx="%.1f" cy="%.1f" r="%g" class="%s"/>' % (cx, cy, r, _c(c, b))


def L(x1, y1, x2, y2, c="e", b=0):
    return '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="%s"/>' % (x1, y1, x2, y2, _c(c, b))


def T(x, y, s, c="t", b=0, fs=14, a="middle", maxw=None):
    assert 14 <= fs <= 20
    w = tw(s, fs)
    left = x - w / 2 if a == "middle" else (x if a == "start" else x - w)
    assert left >= 1 and left + w <= W - 1, "화면 밖 글자 %r left=%.0f w=%.0f" % (s, left, w)
    assert y - fs * 0.8 >= 0, "위로 넘친 글자 %r" % s
    if maxw is not None:
        assert w <= maxw, "글자 넘침 %r %.0f>%s" % (s, w, maxw)
    _TEXTS.append((left, y - fs * 0.78, left + w, y + fs * 0.12, s))
    return '<text x="%.1f" y="%.1f" font-size="%d" text-anchor="%s" class="%s">%s</text>' % (
        x, y, fs, a, _c(c, b), escape(s))


def A(x1, y1, x2, y2, c="e2", b=0, head=9):
    dx, dy = x2 - x1, y2 - y1
    n = math.hypot(dx, dy)
    ux, uy = dx / n, dy / n
    bx, by = x2 - ux * head, y2 - uy * head
    px, py = -uy * 4.5, ux * 4.5
    tip = '<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" class="%s"/>' % (
        x2, y2, bx + px, by + py, bx - px, by - py, _c("arrow", b))
    return L(x1, y1, bx, by, c, b) + tip


def PL(pts_, c="e2", b=0):
    s = " ".join("%.1f,%.1f" % p for p in pts_)
    return '<polyline points="%s" fill="none" class="%s"/>' % (s, _c(c, b))


def PG(pts_, c="n3", b=0):
    s = " ".join("%.1f,%.1f" % p for p in pts_)
    return '<polygon points="%s" class="%s"/>' % (s, _c(c, b))


def BOX(x, y, w, h, lines, c="box", b=0):
    out = [R(x, y, w, h, c, b)]
    total = sum(sz for _, sz, _ in lines) + 5 * (len(lines) - 1)
    assert total <= h - 4, "상자 높이 부족 %r" % (lines,)
    cy = y + (h - total) / 2
    for s, sz, cl in lines:
        cy += sz
        out.append(T(x + w / 2, round(cy - 2), s, cl, b, sz, maxw=w - 6))
        cy += 5
    return "".join(out)


class Plot:
    """데이터 좌표 → 화면 좌표. 신호 그래프(축, 눈금, 연속 곡선, 이산 막대)를 Python 으로 계산해서 그린다."""

    def __init__(self, x0, y0, w, h, xr, yr):
        self.x0, self.y0, self.w, self.h, self.xr, self.yr = x0, y0, w, h, xr, yr

    def X(self, x):
        return self.x0 + (x - self.xr[0]) / (self.xr[1] - self.xr[0]) * self.w

    def Y(self, y):
        return self.y0 + self.h - (y - self.yr[0]) / (self.yr[1] - self.yr[0]) * self.h

    def axes(self, xl="t", yl=None, xt=(), yt=(), b=0, yaxis=True, xlab_dy=17):
        out = []
        y0 = self.Y(0)
        out.append(L(self.x0, y0, self.x0 + self.w, y0, "e", b))
        out.append(T(self.x0 + self.w + 2, y0 + 5, xl, "tm", b, 14, "start"))
        if yaxis and self.xr[0] <= 0 <= self.xr[1]:
            x0 = self.X(0)
            out.append(L(x0, self.y0 - 4, x0, self.y0 + self.h + 6, "e", b))
            if yl:
                out.append(T(x0 + 5, self.y0 + 8, yl, "tm", b, 14, "start"))
        for v, lab in xt:
            xx = self.X(v)
            out.append(L(xx, y0 - 3, xx, y0 + 3, "e", b))
            if lab:
                out.append(T(xx, y0 + xlab_dy, lab, "tm", b, 14))
        for v, lab in yt:
            yy = self.Y(v)
            x0 = self.X(0) if self.xr[0] <= 0 <= self.xr[1] else self.x0
            out.append(L(x0 - 3, yy, x0 + 3, yy, "e", b))
            if lab:
                out.append(T(x0 - 6, yy + 5, lab, "tm", b, 14, "end"))
        return "".join(out)

    def line(self, data, c="e2", b=0):
        return PL([(self.X(x), self.Y(y)) for x, y in data], c, b)

    def curve(self, f, a, bnd, c="e2", b=0, n=160):
        return self.line([(a + (bnd - a) * i / n, f(a + (bnd - a) * i / n)) for i in range(n + 1)], c, b)

    def stems(self, pairs, c="e2", dot="n2", b=0, r=4):
        out = []
        for n, v in pairs:
            xx, yy = self.X(n), self.Y(v)
            if abs(v) > 1e-12:
                out.append(L(xx, self.Y(0), xx, yy, c, b))
            out.append(C(xx, yy, r, dot, b))
        return "".join(out)

    def impulse(self, t, area, c="e2", b=0, label=None, hscale=1.0):
        """연속시간 임펄스: 화살표 (높이는 넓이를 나타내는 표시일 뿐)."""
        xx = self.X(t)
        out = [A(xx, self.Y(0), xx, self.Y(area * hscale), c, b)]
        if label:
            yy = self.Y(area * hscale) + (-6 if area > 0 else 18)
            out.append(T(xx + 12, yy, label, "tb", b, 14, "start"))
        return "".join(out)


def fig(head, els, caption, h=270):
    global _TEXTS
    boxes, _TEXTS = _TEXTS, []
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b_ = boxes[i], boxes[j]
            if a[0] < b_[2] - 1 and b_[0] < a[2] - 1 and a[1] < b_[3] - 1 and b_[1] < a[3] - 1:
                raise AssertionError("겹치는 글자 %r / %r (%s)" % (a[4], b_[4], head))
    for bx in boxes:
        assert bx[3] <= h, "아래로 넘친 글자 %r" % bx[4]
    svg = '<svg viewBox="0 0 480 %d" xmlns="http://www.w3.org/2000/svg">%s</svg>' % (h, "".join(els))
    bs = [int(m) for m in re.findall(r'class="[^"]*\bb(\d)\b', svg)]
    return {"kind": "figure", "head": head, "svg": svg, "caption": caption, "builds": max(bs) if bs else 1}


def _strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, list):
        for x in o:
            yield from _strings(x)
    elif isinstance(o, dict):
        for k, v in o.items():
            if k != "svg":
                yield from _strings(v)


def unit(uid, ttl, gl, terms, slides, recall=()):
    slides = fill(slides)
    body = " ".join(_strings(slides))
    low = body.lower()
    tl = []
    assert 4 <= len(terms) <= 10, uid
    bad = []
    for key in terms:
        ko, en, say = TERMS[key]
        n = max(low.count(ko.lower()) if ko else 0, low.count(en.lower()) if en else 0)
        if n < 3:
            bad.append("용어 %s %d번" % (key, n))
        tl.append({"ko": ko, "en": en, "say": say})
    for key in recall:
        if show(key) not in body:
            bad.append("앞 단원 용어 %s 안 부름" % key)
    assert not bad, "%s: %s" % (uid, ", ".join(bad))
    assert len(recall) >= 2 or uid.endswith("-1") and uid.startswith("w1"), uid
    assert 10 <= len(slides) <= 18, "%s: 슬라이드 %d장" % (uid, len(slides))
    kinds = [s["kind"] for s in slides]
    assert kinds[0] == "title" and kinds[1] == "goal" and kinds[-1] == "recap", uid
    for need in ("analogy", "figure"):
        assert need in kinds, (uid, need)
    assert 1 <= kinds.count("check") <= 3, uid
    names = ", ".join("%s(%s)" % (t["ko"], t["en"]) if t["ko"] and t["en"] else (t["ko"] or t["en"]) for t in tl)
    slides[-1]["items"].append("오늘의 용어: " + names)
    return {"id": uid, "title": ttl, "goal": fill(gl), "terms": tl, "slides": slides}


BAD = ("—", "–", "·", "・")


def write(path, week, ttl, units):
    d = {"week": week, "title": ttl, "units": units}
    txt = json.dumps(d, ensure_ascii=False, indent=1)
    for ch in BAD:
        assert ch not in txt, "금지 문자 %r" % ch
    # 엔진 숫자 버그: 수식 밖에서 공백 사이에 낀 숫자
    badn = []

    def _plain(o, key=""):
        if isinstance(o, str):
            if key not in ("tex", "sym", "svg"):
                yield o
        elif isinstance(o, list):
            for x in o:
                yield from _plain(x, key)
        elif isinstance(o, dict):
            for k, v in o.items():
                yield from _plain(v, k)

    for s in _plain(d):
        plain = re.sub(r"\$[^$\n]+?\$", " X ", s)
        if re.search(r"(?<= )\d+(?= )", plain):
            badn.append(s)
    for s in badn:
        print("공백 사이 숫자:", s)
    assert not badn
    with open(path, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    n = sum(len(u["slides"]) for u in units)
    print("%s: 단원 %d개, 슬라이드 %d장" % (os.path.basename(path), len(units), n))
