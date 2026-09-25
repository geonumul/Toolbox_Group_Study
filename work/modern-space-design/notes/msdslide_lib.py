# -*- coding: utf-8 -*-
"""근현대 공간디자인 정리 슬라이드 공용 도우미.

build_slides_w1.py ~ build_slides_w6.py 가 불러 쓴다.
규칙: work\\_rules\\00_공통_원칙.md, work\\_rules\\정리슬라이드_작성규칙.md,
      work\\modern-space-design\\rules\\과목정보.md

쓰는 법:

    import os, sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from msdslide_lib import *

    U = []
    U.append(unit("w1-1", "시대 배경", "이 단원을 마치면 ... 할 수 있어요",
                  ["계몽주의", "산업혁명"],
                  [title("시대 배경", "..."), goal("...", "..."), ..., recap("...", "...", "...")]))
    write(out("1"), "1", "1단원. 미술공예운동", U)

- 전문용어는 t("계몽주의") 로 써서 **계몽주어(English)** 모양을 만든다. 용어 표기는
  work\\modern-space-design\\terms\\<주차>.json 을 그대로 쓴다(새로 만들지 않는다).
- 단원 제목은 문제은행(bank\\legacy.json, bank\\u456.json)의 unit 문자열에서
  번호를 뗀 뒷부분과 똑같아야 한다. unit() 이 검사한다.
- SVG 는 클래스로만 꾸민다(fill, stroke, style, id, font-family, stroke-width 금지).
"""
import json, math, os, re, sys
from xml.sax.saxutils import escape

sys.stdout.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.dirname(HERE)
WEEKS = ("1", "2", "3", "4", "5", "6")

# 이 과목을 관통하는 주문. 단원마다 한 번은 불러 준다.
MANTRA = "기계 시대에 건축은 어떻게 생겨야 하나? 싫어 -> 새 장식 -> 정리 -> 없애."

# 금지 문자(긴 줄표, 짧은 줄표, 가운뎃점 두 가지). 이 파일에 글자를 직접 넣지 않으려고 코드 번호로 적는다.
BAD_CODES = {0x2014: "em dash", 0x2013: "en dash", 0x00B7: "가운뎃점", 0x30FB: "가운뎃점"}
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")
MAXLEN = 106  # 검사기가 110자를 넘으면 경고한다

# ---------------------------------------------------------------- 용어 사전 (표기 그대로)
TERMS = {}
for _w in WEEKS:
    for _t in json.load(open(os.path.join(WORK, "terms", _w + ".json"), encoding="utf-8")):
        _ko = (_t.get("ko") or "").strip()
        _en = (_t.get("en") or "").strip()
        _e = (_ko, _en, (_t.get("say") or "").strip(), (_t.get("more") or "").strip(), _w)
        for _k in (_ko, _en, (_ko + "(" + _en + ")") if (_ko and _en) else ""):
            if _k:
                TERMS.setdefault(_k, _e)


def t(key):
    """용어를 **한국어(English)** 모양으로. 영어 이름이 없으면 **한국어**."""
    if key not in TERMS:
        raise KeyError("용어 사전에 없는 말: %r (terms/<주차>.json 표기를 그대로 쓰세요)" % key)
    ko, en, _say, _more, _w = TERMS[key]
    if ko and en:
        return "**%s(%s)**" % (ko, en)
    return "**%s**" % (ko or en)


def term_name(key):
    ko, en, _say, _more, _w = TERMS[key]
    return "%s(%s)" % (ko, en) if (ko and en) else (ko or en)


def term_entry(key):
    ko, en, say, more, _w = TERMS[key]
    d = {"ko": ko, "en": en, "say": say}
    if more:
        d["more"] = more
    return d


def term_say(key):
    return TERMS[key][2]


# ---------------------------------------------------------------- 문제은행 단원 이름 (한 줄로 맞추기)
def _bank_tails():
    """{주차: {단원 제목: 문제은행 unit 문자열}}. 문제은행의 unit 이름에서 '1-2 ' 같은 번호를 뗀다."""
    out = {}
    d = os.path.join(WORK, "bank")
    for name in sorted(os.listdir(d)):
        if not name.endswith(".json"):
            continue
        for q in json.load(open(os.path.join(d, name), encoding="utf-8")):
            u = (q.get("unit") or "").strip()
            m = re.match(r"(\w+)-(\d+)\s+(.+)$", u)
            if not m:
                continue
            out.setdefault(m.group(1), {}).setdefault(m.group(3), set()).add(int(m.group(2)))
    return out


BANK = _bank_tails()
_USED = {}


# ---------------------------------------------------------------- 슬라이드 종류
def _chk_text(o, where):
    for s in _strings(o):
        assert len(s) <= MAXLEN, "%s: %d자로 너무 길어요 (%d자 넘김): %r" % (where, len(s), MAXLEN, s[:40])
        for code, nm in BAD_CODES.items():
            assert chr(code) not in s, "%s: 금지 문자 %s: %r" % (where, nm, s[:40])
        m = EMOJI.search(s)
        assert not m, "%s: 이모지 %r" % (where, m.group(0))
    return o


def title(big, sub):
    assert len(big) <= 20, "title big 은 20자 이내: %r" % big
    return _chk_text({"kind": "title", "big": big, "sub": sub}, "title")


def goal(*items):
    assert 2 <= len(items) <= 4, "goal items %d개 (2~4)" % len(items)
    return _chk_text({"kind": "goal", "items": list(items)}, "goal")


def pts(head, *items):
    assert 2 <= len(items) <= 5, "points items %d개 (2~5): %s" % (len(items), head)
    return _chk_text({"kind": "points", "head": head, "items": list(items)}, "points " + head)


def ana(head, scene, *pairs):
    assert 2 <= len(pairs) <= 4, "analogy map %d쌍 (2~4): %s" % (len(pairs), head)
    for p in pairs:
        assert len(p) == 2, "analogy map 은 [비유, 개념] 쌍: %r" % (p,)
    return _chk_text({"kind": "analogy", "head": head, "scene": scene,
                      "map": [list(p) for p in pairs]}, "analogy " + head)


def stp(head, given, steps, answer):
    assert 3 <= len(steps) <= 7, "steps %d개 (3~7): %s" % (len(steps), head)
    d = {"kind": "steps", "head": head, "steps": list(steps), "answer": answer}
    if given:
        d["given"] = given
    return _chk_text(d, "steps " + head)


def tbl(head, cols, rows):
    assert 2 <= len(cols) <= 4, "compare cols %d개 (2~4): %s" % (len(cols), head)
    assert 2 <= len(rows) <= 6, "compare rows %d개 (2~6): %s" % (len(rows), head)
    for r in rows:
        assert len(r) == len(cols), "행 칸 수가 열과 달라요: %r" % (r,)
    return _chk_text({"kind": "compare", "head": head, "cols": list(cols),
                      "rows": [list(r) for r in rows]}, "compare " + head)


def eng(head, en, ko, tip=None):
    """이 과목에서 english 는 '논술 답안에 쓸 문장'. en 에 외워 쓸 한국어 논술 문장."""
    d = {"kind": "english", "head": head, "en": en, "ko": ko}
    if tip:
        d["tip"] = tip
    return _chk_text(d, "english " + head)


def chk(q, choices, a, why):
    assert 2 <= len(choices) <= 4, "check choices %d개 (2~4)" % len(choices)
    assert isinstance(a, int) and 0 <= a < len(choices), "check 정답 인덱스"
    return _chk_text({"kind": "check", "q": q, "choices": list(choices), "a": a, "why": why}, "check")


def warn(head, *items):
    assert 1 <= len(items) <= 3, "warn items %d개 (1~3): %s" % (len(items), head)
    return _chk_text({"kind": "warn", "head": head, "items": list(items)}, "warn " + head)


def recap(*items):
    assert 3 <= len(items) <= 5, "recap items %d개 (용어 줄 빼고 3~5)" % len(items)
    return _chk_text({"kind": "recap", "items": list(items)}, "recap")


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
    assert 0 <= rx <= 3, "rx 는 0~3 (알약 상자 금지)"
    return '<rect x="%g" y="%g" width="%g" height="%g" rx="%g" class="%s"/>' % (
        x, y, w, h, rx, _c(c, b))


def C(cx, cy, r, c="n", b=0):
    return '<circle cx="%.1f" cy="%.1f" r="%g" class="%s"/>' % (cx, cy, r, _c(c, b))


def L(x1, y1, x2, y2, c="e", b=0):
    return '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="%s"/>' % (
        x1, y1, x2, y2, _c(c, b))


def TX(x, y, s, c="t", b=0, fs=14, a="middle", maxw=None):
    """글자. 화면 밖, 겹침을 fig() 가 잡도록 자리를 기록한다."""
    assert 14 <= fs <= 20, "font-size 는 14~20: %r" % s
    for code, nm in BAD_CODES.items():
        assert chr(code) not in s, "SVG 글자에 금지 문자 %s: %r" % (nm, s)
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


def PATH(d, c="e", b=0):
    return '<path d="%s" fill="none" class="%s"/>' % (d, _c(c, b))


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
    assert 200 <= h <= 300, "높이는 200~300"
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a_, b_ = boxes[i], boxes[j]
            if a_[0] < b_[2] - 1 and b_[0] < a_[2] - 1 and a_[1] < b_[3] - 1 and b_[1] < a_[3] - 1:
                raise AssertionError("겹치는 글자 %r / %r (%s)" % (a_[4], b_[4], head))
    for bx in boxes:
        assert bx[3] <= h, "아래로 넘친 글자 %r (%s)" % (bx[4], head)
    svg = '<svg viewBox="0 0 480 %d" xmlns="http://www.w3.org/2000/svg">%s</svg>' % (h, "".join(els))
    for bad in ('id="', 'style="', 'stroke-width', 'font-family', 'fill="#', 'stroke="#'):
        assert bad not in svg, "SVG 에 %s 를 쓰면 안 돼요 (%s)" % (bad, head)
    bs = [int(m) for m in re.findall(r'class="[^"]*\bb(\d)\b', svg)]
    d = {"kind": "figure", "head": head, "svg": svg, "caption": caption,
         "builds": max(bs) if bs else 1}
    return _chk_text(d, "figure " + head)


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
    """단원 하나. uid 는 w<주차>-<번호>, ttl 은 문제은행 unit 이름에서 번호를 뗀 뒷부분."""
    m = re.fullmatch(r"w(\w+?)-(\d+)", uid)
    assert m, "단원 id 는 w<주차>-<번호>: %r" % uid
    week, num = m.group(1), int(m.group(2))
    tails = BANK.get(week, {})
    assert ttl in tails, ("%s: 단원 제목 %r 이 문제은행에 없어요. 쓸 수 있는 이름: %s"
                          % (uid, ttl, ", ".join(sorted(tails))))
    _USED.setdefault(week, set()).add(ttl)
    if num not in tails[ttl]:
        print("  알림 %s: 문제은행은 %r 을 %s번으로 부릅니다(슬라이드 번호는 %d)."
              % (uid, ttl, ", ".join(str(x) for x in sorted(tails[ttl])), num))

    assert 4 <= len(terms) <= 10, "%s: terms %d개 (4~10)" % (uid, len(terms))
    assert len(set(terms)) == len(terms), "%s: terms 에 같은 용어가 두 번" % uid
    assert 10 <= len(slides) <= 18, "%s: 슬라이드 %d장 (10~18)" % (uid, len(slides))
    kinds = [s["kind"] for s in slides]
    assert kinds[0] == "title", "%s: 첫 장은 title" % uid
    assert kinds[1] == "goal", "%s: 둘째 장은 goal" % uid
    assert kinds[-1] == "recap", "%s: 마지막 장은 recap" % uid
    for need in ("analogy", "figure", "check"):
        assert need in kinds, "%s: %s 슬라이드가 없어요" % (uid, need)
    assert 1 <= kinds.count("check") <= 3, "%s: check %d장 (1~3)" % (uid, kinds.count("check"))
    assert kinds.count("recap") == 1, "%s: recap 은 마지막 한 장만" % uid

    body = " ".join(_strings(slides))
    low = body.lower()
    bad = []
    tl = []
    for key in terms:
        if key not in TERMS:
            raise KeyError("%s: 용어 사전에 없는 말 %r" % (uid, key))
        ko, en, say, more, _w = TERMS[key]
        n = max(low.count(ko.lower()) if ko else 0, low.count(en.lower()) if en else 0)
        if n < 3:
            bad.append("용어 %r 가 슬라이드 글에 %d번 (3번 이상)" % (key, n))
        tl.append(term_entry(key))
    for key in recall:
        if term_name(key) not in body:
            bad.append("앞 단원 용어 %r 를 다시 부르지 않았어요" % key)
    assert not bad, "%s: %s" % (uid, ", ".join(bad))
    assert len(recall) >= 2 or uid == "w1-1", "%s: 앞 단원 용어를 2개 이상 다시 불러요" % uid
    # check 중 한 장은 용어 뜻을 묻는다
    qs = " ".join(s.get("q", "") + " " + " ".join(s.get("choices", []))
                  for s in slides if s["kind"] == "check")
    assert any(term_name(k).split("(")[0] in qs for k in terms), "%s: 용어 뜻을 묻는 check 가 없어요" % uid

    names = ", ".join(term_name(k) for k in terms)
    items = list(slides[-1]["items"]) + ["오늘의 용어: " + names]
    assert len(items) <= 6, "%s: recap 줄이 너무 많아요" % uid
    slides[-1] = dict(slides[-1], items=items)
    return {"id": uid, "title": ttl, "goal": gl, "terms": tl, "slides": slides}


def out(week):
    return os.path.join(HERE, "slides_w%s.json" % week)


def write(path, week, ttl, units):
    assert units, "단원이 없어요"
    for i, u in enumerate(units, 1):
        assert u["id"] == "w%s-%d" % (week, i), "단원 순서와 id 가 안 맞아요: %s" % u["id"]
    d = {"week": week, "title": ttl, "units": units}
    txt = json.dumps(d, ensure_ascii=False, indent=1)
    for code, nm in BAD_CODES.items():
        assert chr(code) not in txt, "금지 문자 %s 가 들어 있어요" % nm
    m = EMOJI.search(txt)
    assert not m, "이모지 문자 %r" % m.group(0)
    assert "전남일" not in txt, "교수님 이름을 쓰지 않아요"
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(txt)
    nsl = sum(len(u["slides"]) for u in units)
    print("%s: 단원 %d개, 슬라이드 %d장" % (os.path.basename(path), len(units), nsl))
    left = sorted(set(BANK.get(week, {})) - _USED.get(week, set()))
    if left:
        print("  단원으로 만들지 않은 문제은행 이름: " + ", ".join(left))
