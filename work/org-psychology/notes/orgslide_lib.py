"""조직심리학 정리 슬라이드 공용 도우미.

build_slides_w1.py, build_slides_w2.py, build_slides_w3.py 가 불러 쓴다.
규칙: work\\_rules\\정리슬라이드_작성규칙.md, work\\org-psychology\\rules\\과목정보.md
- 전문용어는 나올 때마다 t("모집") 로 써서 **모집(Recruitment)** 모양을 만든다.
- SVG 는 클래스로만 꾸민다(fill, stroke, style, id, font-family, stroke-width 금지).
"""
import json, math, os, re, sys
from xml.sax.saxutils import escape

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
DICT = os.path.join(HERE, "..", "rules", "용어사전.json")

MANTRA = "사람을 알아야 조직이 보이고, 조직을 알아야 사람이 보여요."

# ---------------------------------------------------------------- 용어 사전 (표기 그대로)
TERMS = {}
for _t in json.load(open(DICT, encoding="utf-8")):
    _ko = (_t.get("ko") or "").strip()
    _en = (_t.get("en") or "").strip()
    _key = _ko or _en
    if _key and _key not in TERMS:
        TERMS[_key] = (_ko, _en, (_t.get("say") or "").strip())


def t(key):
    """용어를 **한국어(English)** 모양으로. 영어 이름이 없으면 **한국어**."""
    if key not in TERMS:
        raise KeyError("용어 사전에 없는 말: %r" % key)
    ko, en, _ = TERMS[key]
    if ko and en:
        return "**%s(%s)**" % (ko, en)
    return "**%s**" % (ko or en)


def term_entry(key):
    ko, en, say = TERMS[key]
    return {"ko": ko, "en": en, "say": say}


def term_name(key):
    ko, en, _ = TERMS[key]
    if ko and en:
        return "%s(%s)" % (ko, en)
    return ko or en


# ---------------------------------------------------------------- 슬라이드 종류
def title(big, sub):
    assert len(big) <= 22, "title big 이 길어요: %r" % big
    return {"kind": "title", "big": big, "sub": sub}


def goal(*items):
    assert 2 <= len(items) <= 4, "goal items %d개" % len(items)
    return {"kind": "goal", "items": list(items)}


def pts(head, *items):
    assert 2 <= len(items) <= 5, "points items %d개 (%s)" % (len(items), head)
    return {"kind": "points", "head": head, "items": list(items)}


def ana(head, scene, *pairs):
    assert 2 <= len(pairs) <= 4, "analogy map %d쌍 (%s)" % (len(pairs), head)
    return {"kind": "analogy", "head": head, "scene": scene,
            "map": [list(p) for p in pairs]}


def stp(head, given, steps, answer):
    assert 3 <= len(steps) <= 7, "steps %d개 (%s)" % (len(steps), head)
    d = {"kind": "steps", "head": head, "steps": list(steps), "answer": answer}
    if given:
        d["given"] = given
    return d


def tbl(head, cols, rows):
    assert 2 <= len(cols) <= 4, "compare cols %d개 (%s)" % (len(cols), head)
    assert 2 <= len(rows) <= 6, "compare rows %d개 (%s)" % (len(rows), head)
    for r in rows:
        assert len(r) == len(cols), "행 칸 수가 열과 달라요: %r" % (r,)
    return {"kind": "compare", "head": head, "cols": list(cols),
            "rows": [list(r) for r in rows]}


def eng(head, en, ko, tip=None):
    d = {"kind": "english", "head": head, "en": en, "ko": ko}
    if tip:
        d["tip"] = tip
    return d


def chk(q, choices, a, why):
    assert 2 <= len(choices) <= 4, "check choices %d개" % len(choices)
    assert 0 <= a < len(choices)
    return {"kind": "check", "q": q, "choices": list(choices), "a": a, "why": why}


def warn(head, *items):
    assert 1 <= len(items) <= 3, "warn items %d개 (%s)" % (len(items), head)
    return {"kind": "warn", "head": head, "items": list(items)}


def recap(*items):
    assert 3 <= len(items) <= 5, "recap items %d개 (용어 줄 빼고 3~5)" % len(items)
    return {"kind": "recap", "items": list(items)}


# ---------------------------------------------------------------- SVG 도우미 (클래스만)
W = 480
_TEXTS = []


def _tw(s, size):
    w = 0.0
    for ch in s:
        if ch == " ":
            w += 0.32
        elif ord(ch) > 0x2E80:
            w += 1.0
        else:
            w += 0.56
    return w * size


def _c(c, b):
    return c + (" b%d" % b if b else "")


def R(x, y, w, h, c="box", b=0, rx=2):
    assert 0 <= rx <= 3, "rx 는 0~3"
    return '<rect x="%g" y="%g" width="%g" height="%g" rx="%g" class="%s"/>' % (
        x, y, w, h, rx, _c(c, b))


def C(cx, cy, r, c="n", b=0):
    return '<circle cx="%.1f" cy="%.1f" r="%g" class="%s"/>' % (cx, cy, r, _c(c, b))


def L(x1, y1, x2, y2, c="e", b=0):
    return '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="%s"/>' % (
        x1, y1, x2, y2, _c(c, b))


def TX(x, y, s, c="t", b=0, fs=14, a="middle", maxw=None):
    assert 14 <= fs <= 20, "font-size 는 14~20: %r" % s
    w = _tw(s, fs)
    left = x - w / 2 if a == "middle" else (x if a == "start" else x - w)
    assert left >= 1 and left + w <= W - 1, "화면 밖 글자 %r left=%.0f w=%.0f" % (s, left, w)
    assert y - fs * 0.8 >= 0, "위로 넘친 글자 %r" % s
    if maxw is not None:
        assert w <= maxw, "상자 밖으로 넘친 글자 %r (%.0f > %s)" % (s, w, maxw)
    _TEXTS.append((left, y - fs * 0.80, left + w, y + fs * 0.16, s))
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


def PL(points, c="e2", b=0):
    s = " ".join("%.1f,%.1f" % p for p in points)
    return '<polyline points="%s" fill="none" class="%s"/>' % (s, _c(c, b))


def PG(points, c="n3", b=0):
    s = " ".join("%.1f,%.1f" % p for p in points)
    return '<polygon points="%s" class="%s"/>' % (s, _c(c, b))


def BOX(x, y, w, h, lines, c="box", b=0):
    """lines: [(글자, 크기, 클래스), ...] 를 상자 가운데에 세로로 쌓는다."""
    out = [R(x, y, w, h, c, b)]
    total = sum(sz for _, sz, _ in lines) + 5 * (len(lines) - 1)
    assert total <= h - 4, "상자 높이가 모자라요 %r" % (lines,)
    cy = y + (h - total) / 2
    for s, sz, cl in lines:
        cy += sz
        out.append(TX(x + w / 2, round(cy - 2), s, cl, b, sz, maxw=w - 6))
        cy += 5
    return "".join(out)


def fig(head, els, caption, h=270):
    """겹치는 글자, 화면 밖 글자를 검사하고 figure 슬라이드를 만든다."""
    global _TEXTS
    boxes, _TEXTS = _TEXTS, []
    assert 200 <= h <= 300, "높이는 300까지"
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a_, b_ = boxes[i], boxes[j]
            if a_[0] < b_[2] - 1 and b_[0] < a_[2] - 1 and a_[1] < b_[3] - 1 and b_[1] < a_[3] - 1:
                raise AssertionError("겹치는 글자 %r / %r (%s)" % (a_[4], b_[4], head))
    for bx in boxes:
        assert bx[3] <= h, "아래로 넘친 글자 %r (%s)" % (bx[4], head)
    svg = '<svg viewBox="0 0 480 %d" xmlns="http://www.w3.org/2000/svg">%s</svg>' % (h, "".join(els))
    bs = [int(m) for m in re.findall(r'class="[^"]*\bb(\d)\b', svg)]
    return {"kind": "figure", "head": head, "svg": svg, "caption": caption,
            "builds": max(bs) if bs else 1}


def clear():
    """figure 를 만들지 않고 버릴 때 글자 목록을 비운다."""
    global _TEXTS
    _TEXTS = []


# ---------------------------------------------------------------- 단원
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
    assert 4 <= len(terms) <= 10, "%s: terms %d개" % (uid, len(terms))
    assert 10 <= len(slides) <= 18, "%s: 슬라이드 %d장" % (uid, len(slides))
    kinds = [s["kind"] for s in slides]
    assert kinds[0] == "title", "%s: 첫 장은 title" % uid
    assert kinds[1] == "goal", "%s: 둘째 장은 goal" % uid
    assert kinds[-1] == "recap", "%s: 마지막 장은 recap" % uid
    for need in ("analogy", "figure", "check"):
        assert need in kinds, "%s: %s 슬라이드 없음" % (uid, need)
    assert 1 <= kinds.count("check") <= 4, "%s: check %d장" % (uid, kinds.count("check"))

    body = " ".join(_strings(slides))
    low = body.lower()
    bad = []
    tl = []
    for key in terms:
        ko, en, say = TERMS[key]
        n = max(low.count(ko.lower()) if ko else 0, low.count(en.lower()) if en else 0)
        if n < 3:
            bad.append("용어 '%s' 가 %d번" % (key, n))
        tl.append({"ko": ko, "en": en, "say": say})
    for key in recall:
        if term_name(key) not in body:
            bad.append("앞 단원 용어 '%s' 를 다시 부르지 않음" % key)
    assert not bad, "%s: %s" % (uid, ", ".join(bad))

    names = ", ".join(term_name(k) for k in terms)
    slides[-1]["items"].append("오늘의 용어: " + names)
    assert len(slides[-1]["items"]) <= 6
    return {"id": uid, "title": ttl, "goal": gl, "terms": tl, "slides": slides}


BAD_CHARS = {"—": "em dash", "–": "en dash", "·": "가운뎃점", "・": "가운뎃점"}
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")


def write(path, week, ttl, units):
    d = {"week": week, "title": ttl, "units": units}
    txt = json.dumps(d, ensure_ascii=False, indent=1)
    for ch, name in BAD_CHARS.items():
        assert ch not in txt, "금지 문자 %s 가 들어 있어요" % name
    m = EMOJI.search(txt)
    assert not m, "이모지 문자 %r" % m.group(0)
    assert "정지희" not in txt, "교수님 이름을 쓰지 않아요"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    nsl = sum(len(u["slides"]) for u in units)
    print("%s: 단원 %d개, 슬라이드 %d장" % (os.path.basename(path), len(units), nsl))
