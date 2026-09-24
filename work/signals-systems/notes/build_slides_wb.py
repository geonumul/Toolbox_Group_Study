"""신호및시스템 기초 다지기 슬라이드 생성: slides_wb.json (week b).
실행: python build_slides_wb.py   (저장소 어디서 실행해도 됨)
모든 숫자 예제는 이 파일 안에서 Python 으로 계산하고 assert 로 확인한다.
그림(SVG) 좌표도 여기서 계산한다. 글자끼리 겹치면 assert 로 멈춘다."""
import json, math, cmath, os, re, sys
from xml.sax.saxutils import escape
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "slides_wb.json")
GLOSS = os.path.join(HERE, "..", "rules", "용어사전.json")

# ---------------------------------------------------------------- 용어 (사전 표기 그대로)
TERMS = {t["ko"]: (t["en"], t["say"]) for t in json.load(open(GLOSS, encoding="utf-8"))}


def josa(word, pair):
    """받침에 맞는 조사: 은/는, 이/가, 을/를, 과/와, 으로/로, 이에요/예요, 이라고/라고."""
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
    else:
        has = False
    return a if has else b


def show(ko, p=""):
    if ko not in TERMS:
        raise KeyError("사전에 없는 용어: " + ko)
    return "**%s(%s)**" % (ko, TERMS[ko][0]) + (josa(ko, p) if p else "")


def fill(o):
    if isinstance(o, str):
        return re.sub(r"\[\[(.+?)(?:\|(.+?))?\]\]", lambda m: show(m.group(1), m.group(2) or ""), o)
    if isinstance(o, list):
        return [fill(x) for x in o]
    if isinstance(o, dict):
        return {k: (v if k == "svg" else fill(v)) for k, v in o.items()}
    return o


MANTRA = "신호는 시간에 따라 변하는 값, 시스템은 신호를 바꾸는 상자."
MANTRA_LTI = "LTI 시스템은 임펄스 응답 하나만 알면 된다. 출력은 뒤집고, 밀고, 곱하고, 더해서(컨볼루션) 구한다."


# ---------------------------------------------------------------- 슬라이드 도우미
def title(big, sub):
    assert len(big) <= 20, big
    return {"kind": "title", "big": big, "sub": sub}


def goal(*items):
    return {"kind": "goal", "items": list(items)}


def pts(head, *items):
    assert 2 <= len(items) <= 5, head
    return {"kind": "points", "head": head, "items": list(items)}


def ana(head, scene, *pairs):
    return {"kind": "analogy", "head": head, "scene": scene, "map": [list(p) for p in pairs]}


def fml(head, tex, parts, whole):
    return {"kind": "formula", "head": head, "tex": tex,
            "parts": [{"sym": s, "say": w} for s, w in parts], "whole": whole}


def stp(head, given, steps, answer):
    assert 3 <= len(steps) <= 7, head
    d = {"kind": "steps", "head": head, "steps": list(steps), "answer": answer}
    if given:
        d["given"] = given
    return d


def cmp(head, cols, rows):
    return {"kind": "compare", "head": head, "cols": list(cols), "rows": [list(r) for r in rows]}


def chk(q, choices, a, why):
    return {"kind": "check", "q": q, "choices": list(choices), "a": a, "why": why}


def warn(head, *items):
    return {"kind": "warn", "head": head, "items": list(items)}


def where(*items):
    return pts("이게 이 과목 어디에 나오나", *items)


def recap(*items):
    return {"kind": "recap", "items": list(items)}


# ---------------------------------------------------------------- SVG 도우미 (클래스만 사용)
W = 480
TEXTS = []  # 지금 그리는 그림의 글자 상자들 (겹침 검사용)


def tw(s, size):
    """글자 폭 대략 추정 (한글 1em, 영숫자 0.6em, 공백 0.3em)."""
    w = 0.0
    for ch in s:
        w += 0.3 if ch == " " else (1.0 if ord(ch) > 0x2E80 else 0.6)
    return w * size


def _c(c, b):
    return c + (" b%d" % b if b else "")


def R(x, y, w, h, c="box", b=0, rx=2):
    assert 0 <= rx <= 3
    return '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%g" class="%s"/>' % (x, y, w, h, rx, _c(c, b))


def C(cx, cy, r, c="n", b=0):
    return '<circle cx="%.1f" cy="%.1f" r="%g" class="%s"/>' % (cx, cy, r, _c(c, b))


def L(x1, y1, x2, y2, c="e", b=0):
    return '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="%s"/>' % (x1, y1, x2, y2, _c(c, b))


def T(x, y, s, c="t", b=0, fs=15, a="middle"):
    assert 14 <= fs <= 20
    w = tw(s, fs)
    left = x - w / 2 if a == "middle" else (x if a == "start" else x - w)
    assert left >= 1 and left + w <= W - 1, "화면 밖 글자 %r left=%.0f w=%.0f" % (s, left, w)
    assert y - fs * 0.8 >= 0 and y <= 300, "위아래 밖 글자 %r" % s
    box = (left, y - fs * 0.78, left + w, y + fs * 0.22, s)
    for o in TEXTS:
        if box[0] < o[2] - 1 and o[0] < box[2] - 1 and box[1] < o[3] - 1 and o[1] < box[3] - 1:
            raise AssertionError("글자 겹침 %r / %r" % (s, o[4]))
    TEXTS.append(box)
    return '<text x="%.1f" y="%.1f" font-size="%d" text-anchor="%s" class="%s">%s</text>' % (
        x, y, fs, a, _c(c, b), escape(s))


def A(x1, y1, x2, y2, c="e2", b=0, hd=9):
    dx, dy = x2 - x1, y2 - y1
    n = math.hypot(dx, dy)
    ux, uy = dx / n, dy / n
    bx, by = x2 - ux * hd, y2 - uy * hd
    px, py = -uy * 4.5, ux * 4.5
    head = '<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" class="%s"/>' % (
        x2, y2, bx + px, by + py, bx - px, by - py, _c("arrow", b))
    return L(x1, y1, bx, by, c, b) + head


def PL(p, c="e2", b=0):
    s = " ".join("%.1f,%.1f" % q for q in p)
    return '<polyline points="%s" fill="none" class="%s"/>' % (s, _c(c, b))


def PG(p, c="n3", b=0):
    s = " ".join("%.1f,%.1f" % q for q in p)
    return '<polygon points="%s" class="%s"/>' % (s, _c(c, b))


def fig(head, els, caption, h=270):
    svg = '<svg viewBox="0 0 480 %d" xmlns="http://www.w3.org/2000/svg">%s</svg>' % (h, "".join(els))
    TEXTS.clear()  # 다음 그림의 겹침 검사를 새로 시작
    bs = [int(m) for m in re.findall(r'class="[^"]*\bb(\d)\b', svg)]
    return {"kind": "figure", "head": head, "svg": svg, "caption": caption, "builds": max(bs) if bs else 1}


class Plot:
    """데이터 좌표 -> 화면 좌표. 칸(X, Y, Wd, Ht) 안에 x0..x1, y0..y1 을 그린다."""

    def __init__(s, x0, x1, y0, y1, X, Y, Wd, Ht):
        s.x0, s.x1, s.y0, s.y1, s.X, s.Y, s.Wd, s.Ht = x0, x1, y0, y1, X, Y, Wd, Ht

    def px(s, x):
        return s.X + (x - s.x0) / (s.x1 - s.x0) * s.Wd

    def py(s, y):
        return s.Y + s.Ht - (y - s.y0) / (s.y1 - s.y0) * s.Ht

    def axes(s, xl="t", yl="", xt=(), yt=(), b=0, xtl=None, ytl=None, yaxis=True, xty=None):
        out = [A(s.X - 4, s.py(0), s.X + s.Wd + 12, s.py(0), "e", b, 7)]
        if yaxis and s.x0 <= 0 <= s.x1:
            out.append(A(s.px(0), s.Y + s.Ht + 4, s.px(0), s.Y - 10, "e", b, 7))
            if yl:
                out.append(T(s.px(0) + 6, s.Y - 2, yl, "tm", b, 14, "start"))
        if xl:
            out.append(T(s.X + s.Wd + 14, s.py(0) - 6, xl, "tm", b, 14, "start"))
        for i, v in enumerate(xt):
            lab = xtl[i] if xtl else fmtn(v)
            out.append(L(s.px(v), s.py(0) - 3, s.px(v), s.py(0) + 3, "e", b))
            out.append(T(s.px(v), (s.py(0) + 18) if xty is None else xty, lab, "tm", b, 14))
        for i, v in enumerate(yt):
            lab = ytl[i] if ytl else fmtn(v)
            out.append(L(s.px(0) - 3, s.py(v), s.px(0) + 3, s.py(v), "e", b))
            out.append(T(s.px(0) - 7, s.py(v) + 5, lab, "tm", b, 14, "end"))
        return out

    def curve(s, f, a, bb, c="e2", b=0, n=160):
        return PL([(s.px(a + (bb - a) * i / n), s.py(f(a + (bb - a) * i / n))) for i in range(n + 1)], c, b)

    def line(s, p, c="e2", b=0):
        return PL([(s.px(x), s.py(y)) for x, y in p], c, b)

    def stems(s, ns, vals, c="n2", b=0, r=4):
        out = []
        for n_, v in zip(ns, vals):
            if abs(v) > 1e-12:
                out.append(L(s.px(n_), s.py(0), s.px(n_), s.py(v), "e2" if c == "n2" else "e", b))
            out.append(C(s.px(n_), s.py(v), r, c, b))
        return out

    def dot(s, x, y, c="n2", b=0, r=5):
        return C(s.px(x), s.py(y), r, c, b)


def fmtn(v):
    if abs(v - round(v)) < 1e-9:
        return str(int(round(v)))
    return ("%.2f" % v).rstrip("0")


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


def unit(uid, ttl, gl, terms, recall, slides):
    """terms: 이 단원 용어(ko). recall: 앞 단원에서 다시 부르는 용어(2개 이상, 본문에 나와야 함)."""
    slides = fill(slides)
    body = " ".join(_strings(slides))
    tl = []
    for ko in terms:
        en, say = TERMS[ko]
        n = body.count("**%s(%s)**" % (ko, en))
        assert n >= 3, "%s: 용어 %s 가 %d번" % (uid, ko, n)
        tl.append({"ko": ko, "en": en, "say": say})
    for ko in recall:
        assert body.count("**%s(%s)**" % (ko, TERMS[ko][0])) >= 1, "%s: 앞 단원 용어 %s 가 없음" % (uid, ko)
    assert uid == "wb-1" or len(recall) >= 2, uid
    assert 4 <= len(tl) <= 10
    assert 14 <= len(slides) <= 22, "%s: 슬라이드 %d장" % (uid, len(slides))
    kinds = [s["kind"] for s in slides]
    assert kinds[0] == "title" and kinds[1] == "goal" and kinds[-1] == "recap", uid
    assert slides[-2]["kind"] == "points" and slides[-2]["head"] == "이게 이 과목 어디에 나오나", uid
    for need in ("analogy", "figure", "check", "steps"):
        assert need in kinds, (uid, need)
    assert kinds.count("check") >= 2 and kinds.count("figure") >= 2, uid
    names = ", ".join("%s(%s)" % (t["ko"], t["en"]) for t in tl)
    slides[-1]["items"].append("오늘의 용어: " + names)
    return {"id": uid, "title": ttl, "goal": fill(gl), "terms": tl, "slides": slides}


UNITS = []


# ================================================================ wb-1 함수와 그래프 읽기
def x1(t):
    return t + 1


TAB1 = [(t, x1(t)) for t in range(4)]
assert TAB1 == [(0, 1), (1, 2), (2, 3), (3, 4)]
XN = {0: 1, 1: 2, 2: 1}  # 10단원에서 다시 쓰는 x[n]


def xn(n):
    return XN.get(n, 0)


assert [xn(n) for n in range(-1, 4)] == [0, 1, 2, 1, 0]
SQ = {n: n * n for n in range(-2, 4)}
assert SQ[-2] == 4 and SQ[3] == 9 and SQ[0] == 0
assert 3 * 2 - 1 == 5
# 샘플링: x(t)=2t, T=0.5 -> x[n] = x(0.5 n) = n
SAMP = [2 * (0.5 * n) for n in range(5)]
assert SAMP == [0, 1, 2, 3, 4]


def fig_w1_points():
    p = Plot(-0.5, 3.6, 0, 4.6, 50, 35, 290, 180)
    els = p.axes("t", "x(t)", xt=[1, 2, 3], yt=[1, 2, 3, 4])
    els.append(T(p.px(0) - 7, p.py(0) + 18, "0", "tm", 0, 14, "end"))
    for i, (t, v) in enumerate(TAB1):
        els.append(p.dot(t, v, "n2", 1))
        els.append(T(p.px(t) + 10, p.py(v) + 18, "(%d, %d)" % (t, v), "tb", 1, 14, "start"))
    els.append(p.line([(-0.5, 0.5), (3.6, 4.6)], "e2", 2))
    els.append(R(380, 40, 90, 150, "box"))
    els.append(T(405, 64, "t", "tb", 0, 15))
    els.append(T(447, 64, "x(t)", "tb", 0, 15))
    els.append(L(385, 72, 465, 72, "e"))
    for i, (t, v) in enumerate(TAB1):
        els.append(T(405, 96 + 26 * i, str(t), "t", 0, 15))
        els.append(T(447, 96 + 26 * i, str(v), "t", 0, 15))
    els.append(T(240, 262, "표의 점을 찍고(1), 선으로 이으면(2) 그래프", "tm", 2, 14))
    return els


def fig_w1_stems():
    p = Plot(-2.6, 4.6, 0, 2.6, 40, 50, 390, 160)
    els = p.axes("n", "x[n]", xt=[-2, -1, 1, 2, 3, 4], yt=[1, 2])
    els.append(T(p.px(0) - 7, p.py(0) + 18, "0", "tm", 0, 14, "end"))
    ns = list(range(-2, 5))
    els += p.stems(ns, [xn(n) for n in ns], "n2", 1)
    els.append(T(240, 262, "정수 칸마다 막대 하나: 사이 칸(0.5 같은 곳)은 없어요", "tm", 1, 14))
    return els


def fig_w1_sampling():
    p = Plot(-0.3, 2.3, 0, 4.9, 60, 40, 330, 180)
    els = p.axes("t", "", xt=[0.5, 1, 1.5, 2], yt=[1, 2, 3, 4])
    els.append(p.curve(lambda t: 2 * t, 0, 2.3, "e2", 1))
    els.append(T(p.px(2.25) - 6, p.py(4.5) - 4, "x(t) = 2t", "tb", 1, 15, "end"))
    for n in range(5):
        t = 0.5 * n
        els.append(L(p.px(t), p.py(0), p.px(t), p.py(2 * t), "e", 2))
        els.append(C(p.px(t), p.py(2 * t), 5, "n2", 2))
    els.append(T(430, 120, "T = 0.5", "tb", 2, 15))
    els.append(T(430, 145, "마다 뽑기", "t", 2, 15))
    els.append(T(240, 262, "뽑은 점만 모으면 x[n] = n (n = 0, 1, 2, 3, 4)", "tm", 3, 14))
    return els


UNITS.append(unit(
    "wb-1", "함수와 그래프 읽기",
    "$x(t)$, $x[n]$ 을 소리 내어 읽고, 숫자를 넣어 표를 만들고 점을 찍어 그래프를 그릴 수 있어요.",
    ["신호", "독립 변수", "연속시간 신호", "이산시간 신호", "샘플링"], [],
    [
        title("함수와 그래프 읽기", "괄호 안에 숫자를 넣으면 값이 하나 나와요"),
        goal("$x(t)$ 를 '엑스 오브 티' 라고 읽고, 숫자를 넣어 값을 구해요.",
             "표를 만들고 점을 찍어서 그래프를 그려요.",
             "[[연속시간 신호|와/과]] [[이산시간 신호|을/를]] 괄호 모양으로 구별해요."),
        ana("[[신호|은/는]] 시간마다 적어 둔 기록표예요",
            "매일 아침 체온을 재서 공책에 적어요. 1일째 36.5도, 2일째 36.8도처럼 날짜마다 값이 하나씩 있어요.",
            ["며칠째인지(날짜)", "[[독립 변수]], 보통 시간 $t$ 또는 칸 번호 $n$"],
            ["그날 적은 체온", "그 시간의 값 $x(t)$ 또는 $x[n]$"],
            ["공책 한 권 전체", "[[신호]] 하나, 이름은 $x$"]),
        pts("함수는 값을 돌려주는 규칙이에요",
            "함수는 숫자를 하나 넣으면 숫자 하나를 돌려주는 규칙이에요.",
            "$x(t)=t+1$ 은 '넣은 수에 1을 더해라' 라는 규칙이에요.",
            "$x(2)$ 는 $t$ 자리에 2를 넣으라는 뜻이에요. $x(2)=2+1=3$ 이에요.",
            "괄호 안의 $t$ 는 빈자리예요. 이 자리를 [[독립 변수|이라고/라고]] 해요."),
        fml("$x(t)$ 를 소리 내어 읽기", r"x(t) = t + 1",
            [("x", "[[신호]]의 이름. 엑스라고 읽어요"),
             ("(t)", "괄호 안은 [[독립 변수]]. 보통 시간(초)이에요"),
             ("t+1", "값을 만드는 규칙. 시간에 1을 더해요")],
            "엑스 오브 티는 티 더하기 일. 시각 $t$ 에서 이 [[신호]]의 값이 $t+1$ 이라는 뜻이에요."),
        stp("손계산 1: 표 만들기", "$x(t)=t+1$ 에 $t=0, 1, 2, 3$ 을 차례로 넣어요",
            ["$t=0$: $x(0)=0+1=1$",
             "$t=1$: $x(1)=1+1=2$",
             "$t=2$: $x(2)=2+1=3$",
             "$t=3$: $x(3)=3+1=4$",
             "표로 모으면 $(0,1), (1,2), (2,3), (3,4)$ 네 쌍이에요."],
            "(시간, 값) 쌍 네 개. 이제 이 쌍을 점으로 찍으면 그래프가 돼요."),
        fig("표에서 그래프로", fig_w1_points(),
            "가로축은 [[독립 변수]] $t$, 세로축은 값 $x(t)$ 예요. 점을 찍고 이으면 그래프예요."),
        pts("괄호 모양이 두 종류예요",
            "[[연속시간 신호|은/는]] 모든 순간에 값이 있어요. 둥근 괄호 $x(t)$ 로 써요.",
            "$t$ 는 실수라서 $t=0.5$, $t=1.25$ 어디서든 값이 있어요.",
            "[[이산시간 신호|은/는]] 정수 칸에서만 값이 있어요. 대괄호 $x[n]$ 으로 써요.",
            r"$n$ 은 $\dots,-1,0,1,2,\dots$ 같은 정수만 돼요. $x[0.5]$ 라는 칸은 없어요."),
        ana("선과 점",
            "주식 앱의 실시간 그래프는 끊김 없이 이어진 선이에요. 그런데 신문에 실리는 매일 종가는 하루에 점 하나뿐이에요.",
            ["끊김 없이 그린 선", "[[연속시간 신호]] $x(t)$"],
            ["하루 한 번 찍은 점(매일 종가)", "[[이산시간 신호]] $x[n]$"],
            ["며칠째인지(1일째, 2일째)", "정수 칸 번호 $n$"]),
        stp("손계산 2: 목록으로 준 $x[n]$ 읽기", "$x[n]$ 은 $n=0,1,2$ 에서 $1, 2, 1$ 이고 나머지 칸은 $0$",
            ["$n=-1$: 목록 밖이라 $x[-1]=0$",
             "$n=0$: 첫 값이라 $x[0]=1$",
             "$n=1$: 둘째 값이라 $x[1]=2$",
             "$n=2$: 셋째 값이라 $x[2]=1$",
             "$n=3$: 다시 목록 밖이라 $x[3]=0$"],
            "칸마다 높이 $0, 1, 2, 1, 0$ 인 막대. 이 신호는 10단원 컨볼루션에서 다시 만나요."),
        fig("[[이산시간 신호|은/는]] 막대(줄기)로 그려요", fig_w1_stems(),
            "정수 칸마다 세운 막대 끝의 동그라미가 값이에요. 칸 사이는 비어 있어요."),
        stp("손계산 3: 식으로 준 $x[n]$", "$x[n]=n^2$ ($n$ 제곱), $n=-2$ 부터 $3$ 까지",
            ["$n=-2$: $(-2)^2=4$. 음수도 제곱하면 양수예요.",
             "$n=-1$: $(-1)^2=1$",
             "$n=0$: $0^2=0$",
             "$n=1, 2, 3$: $1, 4, 9$"],
            "표: $4, 1, 0, 1, 4, 9$. 식이 있으면 목록 없이도 어느 칸이든 값을 구해요."),
        chk("$x(t)=3t-1$ 일 때 $x(2)$ 는?", ["$5$", "$6$", "$3$", "$7$"], 0,
            r"$t$ 자리에 2를 넣어요. $3\times 2-1=6-1=5$ 예요."),
        stp("손계산 4: [[샘플링]], 선에서 점 뽑기", "$x(t)=2t$ 에서 간격 $T=0.5$ 초마다 값을 뽑아요",
            ["규칙은 $x[n]=x(nT)$. $n$ 번째 점은 시각 $nT$ 의 값이에요.",
             "$n=0$: $x(0)=0$",
             r"$n=1$: $x(0.5)=2\times 0.5=1$",
             "$n=2$: $x(1)=2$, $n=3$: $x(1.5)=3$"],
            r"뽑은 값은 $0,1,2,3,\dots$ 즉 $x[n]=n$. [[샘플링]]으로 연속 선이 이산 점이 됐어요."),
        fig("[[샘플링]]: 연속 선에서 점만 뽑기", fig_w1_sampling(),
            "[[연속시간 신호]] $x(t)$ 에서 $T$ 마다 뽑으면 [[이산시간 신호]] $x[n]$ 이에요."),
        chk("대괄호로 $x[n]$ 이라고 쓰고, 정수 칸에서만 값이 있는 것은?",
            ["[[이산시간 신호]]", "[[연속시간 신호]]", "[[독립 변수]]", "[[샘플링]]"], 0,
            "[[이산시간 신호|은/는]] 정수 칸 $n$ 에서만 값이 있고 대괄호를 써요. 둥근 괄호는 [[연속시간 신호|예요/이에요]]."),
        warn("헷갈리기 쉬운 점",
             "$x(2)$ 는 '$x$ 곱하기 2' 가 아니에요. '$t$ 자리에 2를 넣은 값' 이에요.",
             "그래프의 가로축은 [[독립 변수]](시간), 세로축은 그때의 값이에요.",
             "주문: " + MANTRA),
        where("S2 p.4: 1장 첫 쪽. [[연속시간 신호]] $x(t)$ 와 [[이산시간 신호]] $x[n]$ 의 정의",
              "S2 p.17: $N$ 칸마다 같은 값이 반복되는 이산 주기 [[신호]] $x[n]$",
              r"S3 p.26 Example 2.1: $h[n]=[0\ 0\ 1\ 1\ 1\ 0\ 0]$ 처럼 목록으로 적은 신호",
              "시험 모양: 그래프나 목록을 보고 $x[1]$ 같은 값을 읽는 것이 모든 계산의 첫걸음이에요."),
        recap("$x(t)$ 는 '시각 $t$ 의 값'. 괄호 안에 숫자를 넣으면 값이 나와요.",
              "숫자를 넣어 표를 만들고, 점을 찍고, 이으면 그래프예요.",
              "둥근 괄호 $x(t)$ 는 연속, 대괄호 $x[n]$ 은 정수 칸만 있는 이산이에요.",
              "[[샘플링|은/는]] $x[n]=x(nT)$, 선에서 일정 간격으로 점을 뽑는 일이에요."),
    ]))


# ================================================================ wb-2 그래프 옮기기, 뒤집기, 늘이기
def xs(t):
    """S2 p.9 의 x(t): 0~1 에서 1, 1~2 에서 1 에서 0 으로 내려가는 비탈, 나머지 0."""
    if 0 <= t <= 1:
        return 1.0
    if 1 < t <= 2:
        return 2.0 - t
    return 0.0


# x(t-2): 새 그래프 y(t) = x(t-2)
assert xs(2 - 2) == 1 and xs(3 - 2) == 1 and xs(4 - 2) == 0
# x(-t)
assert xs(-(-1)) == 1 and xs(-(-2)) == 0 and xs(-(1)) == 0
# x(2t)
assert xs(2 * 0.5) == 1 and xs(2 * 1) == 0 and xs(2 * 0.75) == 0.5
# x(-t+1): 원래 자리 0,1,2 -> 새 자리 1,0,-1
assert [1 - o for o in (0, 1, 2)] == [1, 0, -1]
assert xs(-1 + 1) == 1 and xs(-0 + 1) == 1 and xs(1 + 1) == 0
# S2 p.10 직사각형 -1..3 -> x(t-4) 는 3..7, x(t+2) 는 -3..1
assert (-1 + 4, 3 + 4) == (3, 7) and (-1 - 2, 3 - 2) == (-3, 1)
# 이산 척도: x[n] = [1,2,3] (n=0,1,2) -> y[n] = x[2n]
XD = {0: 1, 1: 2, 2: 3}
YD = {n: XD.get(2 * n, 0) for n in range(-2, 3)}
assert YD == {-2: 0, -1: 0, 0: 1, 1: 3, 2: 0}


def _shape(p, f, a, bb, c, b):
    return p.curve(f, a, bb, c, b, 240)


def fig_w2_base():
    p = Plot(-2.6, 4.6, 0, 1.5, 40, 60, 390, 140)
    els = p.axes("t", "x(t)", xt=[-2, -1, 1, 2, 3, 4], yt=[1])
    els.append(T(p.px(0) - 7, p.py(0) + 18, "0", "tm", 0, 14, "end"))
    els.append(_shape(p, xs, -2.6, 4.6, "e2", 1))
    for (t, v, nm) in [(0, 1, "A"), (1, 1, "B"), (2, 0, "C")]:
        els.append(p.dot(t, v, "n2", 2))
        els.append(T(p.px(t) + (12 if nm != "C" else 0), p.py(v) - 10 - (0 if nm != "C" else 4), nm, "tb", 2, 15))
    els.append(T(240, 250, "점 A(0, 1), B(1, 1), C(2, 0) 을 따라가며 옮겨 봐요", "tm", 2, 14))
    return els


def fig_w2_shift():
    p = Plot(-1.6, 5.6, 0, 1.6, 40, 55, 390, 140)
    els = p.axes("t", "", xt=[-1, 1, 2, 3, 4, 5], yt=[1])
    els.append(T(p.px(0) - 7, p.py(0) + 18, "0", "tm", 0, 14, "end"))
    els.append(_shape(p, xs, -1.6, 5.6, "e", 1))
    els.append(T(p.px(0.5), p.py(1) - 10, "x(t)", "t", 1, 15))
    els.append(_shape(p, lambda t: xs(t - 2), -1.6, 5.6, "e2", 2))
    els.append(T(p.px(2.9), p.py(1) - 10, "x(t-2)", "tb", 2, 15))
    els.append(A(p.px(0.4), p.py(1.3), p.px(2.4), p.py(1.3), "e2", 3))
    els.append(T(p.px(1.4), p.py(1.3) - 8, "오른쪽 2", "tb", 3, 15))
    els.append(T(240, 255, "빼기(t-2)인데 오른쪽으로! 늦게 틀었으니까요", "tm", 3, 14))
    return els


def fig_w2_flip():
    p = Plot(-2.8, 2.8, 0, 1.6, 40, 55, 390, 140)
    els = p.axes("t", "", xt=[-2, -1, 1, 2], yt=[])
    els.append(T(p.px(0) - 7, p.py(0) + 18, "0", "tm", 0, 14, "end"))
    els.append(_shape(p, xs, -2.8, 2.8, "e", 1))
    els.append(T(p.px(1.6), p.py(1) - 10, "x(t)", "t", 1, 15))
    els.append(_shape(p, lambda t: xs(-t), -2.8, 2.8, "e2", 2))
    els.append(T(p.px(-1.6), p.py(1) - 10, "x(-t)", "tb", 2, 15))
    els.append(T(240, 255, "t = 0 의 세로축을 거울로 삼아 좌우로 뒤집혀요", "tm", 2, 14))
    return els


def fig_w2_scale():
    p = Plot(-0.8, 3.0, 0, 1.6, 50, 55, 380, 140)
    els = p.axes("t", "", xt=[0.5, 1, 2], yt=[1])
    els.append(T(p.px(0) - 7, p.py(0) + 18, "0", "tm", 0, 14, "end"))
    els.append(_shape(p, xs, -0.8, 3.0, "e", 1))
    els.append(T(p.px(1.85), p.py(0.55), "x(t)", "t", 1, 15, "start"))
    els.append(_shape(p, lambda t: xs(2 * t), -0.8, 3.0, "e2", 2))
    els.append(T(p.px(0.5), p.py(1) - 10, "x(2t)", "tb", 2, 15))
    els.append(T(240, 255, "B 는 1 에서 0.5 로, C 는 2 에서 1 로: 절반으로 줄어요", "tm", 2, 14))
    return els


def fig_w2_dt():
    p1 = Plot(-2.6, 2.6, 0, 3.5, 30, 45, 190, 150)
    p2 = Plot(-2.6, 2.6, 0, 3.5, 260, 45, 190, 150)
    els = p1.axes("n", "x[n]", xt=[-2, -1, 1, 2], yt=[1, 2, 3])
    els += p1.stems(range(-2, 3), [XD.get(n, 0) for n in range(-2, 3)], "n2", 1)
    els += p2.axes("n", "x[2n]", xt=[-2, -1, 1, 2], yt=[1, 2, 3], b=2)
    els += p2.stems(range(-2, 3), [YD[n] for n in range(-2, 3)], "n2", 2)
    els.append(T(240, 250, "x[1] = 2 는 갈 곳이 없어서 사라져요", "tb", 3, 15))
    return els


UNITS.append(unit(
    "wb-2", "그래프 옮기기, 뒤집기, 늘이기",
    "$x(t-2)$, $x(-t)$, $x(2t)$ 의 그래프를 점 몇 개를 표로 따라가서 그리고, '빼면 오른쪽' 함정을 피할 수 있어요.",
    ["시간 이동", "지연", "앞당김", "시간 반전", "시간 척도 변환"],
    ["독립 변수", "연속시간 신호", "이산시간 신호"],
    [
        title("옮기기, 뒤집기, 늘이기", "괄호 안만 바꿨는데 그래프가 움직여요"),
        goal("$x(t-2)$ 가 오른쪽으로 가는 이유를 표로 설명해요.",
             "$x(-t)$, $x(2t)$ 를 점 따라가기로 그려요.",
             "[[시간 이동]], [[시간 반전]], [[시간 척도 변환|을/를]] 구별해요."),
        ana("영상 재생으로 생각해요",
            "같은 영상을 친구는 2초 늦게 틀었어요. 동생은 거꾸로 돌려 보고, 형은 2배속으로 봐요. 장면은 같고, 언제, 어느 방향, 얼마나 빨리 나오는지만 달라요.",
            ["늦게 틀기(지연)", "[[시간 이동]] $x(t-2)$, 오른쪽으로 옮겨져요"],
            ["거꾸로 재생", "[[시간 반전]] $x(-t)$"],
            ["2배속, 0.5배속", "[[시간 척도 변환]] $x(2t)$, $x(t/2)$"]),
        pts("바꾸는 것은 괄호 안뿐이에요",
            "앞 단원에서 괄호 안은 [[독립 변수]] 자리라고 했어요.",
            "그래프를 옮기고 뒤집고 늘이는 일은 모두 괄호 안을 바꿔서 해요.",
            "값(세로)은 그대로 두고, 그 값이 '언제' 나오는지만 바뀌어요.",
            "그래서 요령은 하나예요. 점 몇 개를 골라 새 자리를 표로 찾기."),
        fig("오늘 옮겨 볼 [[연속시간 신호]] $x(t)$", fig_w2_base(),
            "S2 p.9 의 $x(t)$ 예요. $0$ 부터 $1$ 까지 높이 $1$, 그다음 $2$ 까지 내려가요."),
        stp("손계산 1: $y(t)=x(t-2)$ 표로 따라가기", "$y(t)$ 는 '시각 $t$ 에 $x(t-2)$ 의 값을 보여 줘' 라는 뜻",
            ["$t=2$ 를 넣어요: $y(2)=x(2-2)=x(0)=1$. 점 A 가 $t=2$ 에 나와요.",
             "$t=3$: $y(3)=x(1)=1$. 점 B 는 $t=3$ 에 나와요.",
             "$t=4$: $y(4)=x(2)=0$. 점 C 는 $t=4$ 에 나와요.",
             "$t=0$: $y(0)=x(-2)=0$. 원래 A 자리에는 이제 아무것도 없어요."],
            "모든 점이 오른쪽으로 2칸. 모양은 그대로인 [[시간 이동|이에요/예요]]."),
        fig("[[지연]]: 빼면 오른쪽", fig_w2_shift(),
            "$x(t-2)$ 는 $x(t)$ 를 오른쪽으로 2만큼 옮긴 [[지연|이에요/예요]]."),
        warn("'빼면 오른쪽' 함정",
             "$t-2$ 에 빼기가 있어서 왼쪽으로 갈 것 같지만 오른쪽이에요.",
             "원래 $t=0$ 의 값을 보려면 $t-2=0$, 즉 $t=2$ 까지 기다려야 해요. 늦게 나오니 오른쪽이에요.",
             "교수님 강조: $x(t-t_0)$ 는 $t_0>0$ 이면 오른쪽. 부호가 중요하니 꼭 기억하래요."),
        pts("[[지연|과/와]] [[앞당김]]",
            "$x(t-t_0)$ 에서 $t_0>0$ 이면 오른쪽으로 가요. 늦게 나오니 [[지연|이에요/예요]].",
            "$x(t+1)$ 은 $t_0=-1$ 인 셈이라 왼쪽으로 1칸. 일찍 나오니 [[앞당김|이에요/예요]].",
            "둘 다 [[시간 이동|이고/이고]], 모든 점이 똑같은 거리만큼 움직여요."),
        chk("S2 p.10 의 직사각형 $x(t)$ 는 $-1$ 부터 $3$ 까지 있어요. $x(t-4)$ 는 어디부터 어디까지?",
            ["$3$ 부터 $7$ 까지", "$-5$ 부터 $-1$ 까지", "$-1$ 부터 $3$ 까지", "$-4$ 부터 $0$ 까지"], 0,
            "$t-4$ 는 빼기라서 오른쪽으로 4칸이에요. $-1+4=3$, $3+4=7$. 슬라이드 그림과 같아요."),
        stp("손계산 2: [[시간 반전]] $y(t)=x(-t)$", "괄호 안이 원래 자리와 같아지는 $t$ 를 찾아요",
            ["A 는 원래 0: $-t=0$ 이면 $t=0$. 제자리예요.",
             "B 는 원래 1: $-t=1$ 이면 $t=-1$. 확인: $y(-1)=x(1)=1$.",
             "C 는 원래 2: $-t=2$ 이면 $t=-2$. 확인: $y(-2)=x(2)=0$.",
             "$t=1$ 을 넣으면 $y(1)=x(-1)=0$. 오른쪽은 이제 비었어요."],
            "오른쪽에 있던 비탈이 왼쪽으로. $t=0$ 을 거울로 좌우가 뒤집혀요."),
        fig("[[시간 반전]]: 거꾸로 재생", fig_w2_flip(),
            "$x(-t)$ 는 세로축을 기준으로 좌우를 뒤집은 그래프예요."),
        stp("손계산 3: [[시간 척도 변환]] $y(t)=x(2t)$", "이번에도 괄호 안 $=$ 원래 자리",
            ["A: $2t=0$ 이면 $t=0$.",
             "B: $2t=1$ 이면 $t=0.5$. 확인: $y(0.5)=x(1)=1$.",
             "C: $2t=2$ 이면 $t=1$. 확인: $y(1)=x(2)=0$.",
             "모든 자리가 원래의 절반이 됐어요."],
            "가로로 절반으로 줄었어요. 2배속으로 틀면 같은 장면이 절반 시간에 끝나는 것과 같아요."),
        fig("[[시간 척도 변환]]: 2배속", fig_w2_scale(),
            "$x(2t)$ 는 가로로 줄고, $x(t/2)$ 는 가로로 2배 늘어나요."),
        fml("세 가지를 한 식으로 (S2 p.9)", r"y(t) = x(at+b)",
            [("a", "$|a|>1$ 이면 줄고, $0<|a|<1$ 이면 늘고, $a<0$ 이면 뒤집혀요"),
             ("b", "옮기는 양. 0이 아니면 [[시간 이동|이/가]] 섞여요"),
             ("at+b", "이 값이 원래 자리와 같아지는 $t$ 가 새 자리예요")],
            "괄호 안을 원래 점의 자리와 같다고 놓고 $t$ 를 풀면 새 자리가 나와요. 이것 하나로 다 풀려요."),
        stp("손계산 4: 섞인 것 $x(-t+1)$ (S2 p.13)", "괄호 안 $-t+1$ 이 원래 자리 $0, 1, 2$ 와 같아지는 $t$",
            ["A: $-t+1=0$ 이면 $t=1$.",
             "B: $-t+1=1$ 이면 $t=0$.",
             "C: $-t+1=2$ 이면 $t=-1$.",
             "높이 1인 평평한 부분은 $0$ 부터 $1$ 까지, 비탈은 $-1$ 부터 $0$ 까지예요."],
            "뒤집기와 옮기기가 섞여도 표 방법이면 한 번에 풀려요. S2 p.13 그림과 같아요."),
        stp("손계산 5: 이산 척도 $y[n]=x[2n]$ (S2 p.14)", "$x[n]$ 은 $n=0,1,2$ 에서 $1, 2, 3$",
            ["$n=0$: $y[0]=x[0]=1$",
             "$n=1$: $y[1]=x[2]=3$",
             "$n=2$: $y[2]=x[4]=0$",
             "$x[1]=2$ 를 보려면 $2n=1$, $n=0.5$ 여야 하는데 그런 칸은 없어요."],
            "[[이산시간 신호|은/는]] 줄이면 값이 빠져서 사라져요. S2 p.14: 'drops samples'."),
        fig("[[이산시간 신호]]의 척도 변환", fig_w2_dt(),
            "$x[2n]$ 은 짝수 칸만 남기고 당겨 와요. 홀수 칸 값은 버려져요."),
        chk("신호를 오른쪽으로 옮겨서 늦게 나오게 하는 것은?",
            ["[[지연]]", "[[앞당김]]", "[[시간 반전]]", "[[시간 척도 변환]]"], 0,
            "$x(t-t_0)$, $t_0>0$ 은 오른쪽으로 가는 [[지연|이에요/예요]]. 왼쪽은 [[앞당김|이에요/예요]]."),
        cmp("세 가지 변환 한눈에", ["변환", "식", "새 자리", "영상 비유"],
            [["[[시간 이동]]", "$x(t-2)$", "원래 $+2$", "2초 늦게 틀기"],
             ["[[시간 반전]]", "$x(-t)$", "원래에 $-1$ 곱하기", "거꾸로 재생"],
             ["[[시간 척도 변환]]", "$x(2t)$", r"원래 $\div 2$", "2배속"]]),
        where("S2 p.9: $y(t)=x(at+b)$, p.10: [[시간 이동]] $x(t-t_0)$ ($x(t-4)$ 는 오른쪽)",
              "S2 p.11 [[시간 반전]] $x(-t)$, p.12 [[시간 척도 변환]] $x(ct)$, p.13 연습 $x(-t+1)$",
              "S2 p.14 이산 $x[3n+6]$, p.86 1장 과제 1.21, 1.22 (변환한 그래프 그리기)",
              "S3 p.24 컨볼루션 1, 2단계: $h[-k]$ 로 뒤집고 $h[n-k]$ 로 밀기. 바로 이 단원 기술이에요.",
              "시험 모양: 그래프를 주고 $x(t-1)$, $x(-t+1)$ 같은 것을 그리게 해요."),
        recap("괄호 안을 원래 자리와 같게 놓고 $t$ 를 풀면 새 자리가 나와요.",
              "$x(t-2)$ 는 오른쪽 2칸([[지연]]), $x(t+1)$ 은 왼쪽 1칸([[앞당김]]). 빼면 오른쪽!",
              "$x(-t)$ 는 좌우 뒤집기, $x(2t)$ 는 가로로 절반 줄이기예요.",
              "이산 신호는 줄이면 값이 사라질 수 있어요."),
    ]))


# ================================================================ wb-3 각도, 라디안, 사인과 코사인
assert abs(90 * math.pi / 180 - math.pi / 2) < 1e-12
assert abs(60 * math.pi / 180 - math.pi / 3) < 1e-12
assert round(180 / math.pi, 1) == 57.3
UC = {0: (1, 0), 1: (0, 1), 2: (-1, 0), 3: (0, -1)}  # k * pi/2
for k, (c, s) in UC.items():
    assert abs(math.cos(k * math.pi / 2) - c) < 1e-12 and abs(math.sin(k * math.pi / 2) - s) < 1e-12
assert abs(math.cos(math.pi / 3) - 0.5) < 1e-12 and round(math.sin(math.pi / 3), 3) == 0.866
assert abs(2 * math.pi / 2 - math.pi) < 1e-12 and abs(2 * math.pi / 4 - math.pi / 2) < 1e-12
assert abs(2 * math.pi / math.pi - 2) < 1e-12
# 주파수: omega = 4 pi -> f = 2 Hz, T = 0.5
assert abs(4 * math.pi / (2 * math.pi) - 2) < 1e-12 and abs(1 / 2 - 0.5) < 1e-12
# 위상: cos(2t+1) = cos(2(t+0.5))
for t in (0.0, 0.3, 1.7):
    assert abs(math.cos(2 * t + 1) - math.cos(2 * (t + 0.5))) < 1e-12
assert round(math.cos(1), 3) == 0.540


def fig_w3_angles():
    cx, cy, r = 175, 128, 85
    els = [C(cx, cy, r, "e"), L(cx - r - 20, cy, cx + r + 20, cy), L(cx, cy + r + 12, cx, cy - r - 15)]
    for k, (lab, dx, dy, anc) in enumerate([("0 (0°)", 10, -8, "start"), ("π/2 (90°)", 8, -8, "start"),
                                            ("π (180°)", -10, -8, "end"), ("3π/2 (270°)", 10, 24, "start")]):
        x = cx + r * math.cos(k * math.pi / 2)
        y = cy - r * math.sin(k * math.pi / 2)
        els.append(C(x, y, 5, "n2", 1 + (k > 1)))
        els.append(T(x + dx, y + dy, lab, "tb", 1 + (k > 1), 15, anc))
    els.append(R(330, 50, 140, 170, "box"))
    rows = [("도", "라디안"), ("360°", "2π"), ("180°", "π"), ("90°", "π/2"), ("60°", "π/3"), ("45°", "π/4")]
    for i, (a, bb) in enumerate(rows):
        cl = "tb" if i == 0 else "t"
        els.append(T(368, 76 + 27 * i, a, cl, 3 if i else 0, 15))
        els.append(T(436, 76 + 27 * i, bb, cl, 3 if i else 0, 15))
    els.append(T(240, 262, "한 바퀴 = 360° = 2π 라디안", "tb", 3, 15))
    return els


def fig_w3_unit(theta=math.pi / 3):
    cx, cy, r = 190, 145, 100
    x, y = cx + r * math.cos(theta), cy - r * math.sin(theta)
    els = [C(cx, cy, r, "e"), L(cx - r - 20, cy, cx + r + 30, cy), L(cx, cy + r + 10, cx, cy - r - 15),
           T(cx + r + 8, cy + 18, "1", "tm", 0, 14, "start"), T(cx - 8, cy - r - 2, "1", "tm", 0, 14, "end")]
    els.append(L(cx, cy, x, y, "e2", 1))
    els.append(C(x, y, 6, "n2", 1))
    els.append(T(cx + 30, cy - 10, "θ", "tb", 1, 16))
    els.append(L(x, y, x, cy, "e", 2))
    els.append(L(cx, cy, x, cy, "e2", 2))
    els.append(T((cx + x) / 2, cy + 20, "cos θ", "tb", 2, 15))
    els.append(L(x, y, cx, y, "e", 3))
    els.append(T(cx - 8, y + 5, "sin θ", "tb", 3, 15, "end"))
    els.append(T(x + 10, y - 8, "(cos θ, sin θ)", "tb", 1, 15, "start"))
    els.append(T(390, 200, "θ = π/3 이면", "t", 3, 15))
    els.append(T(390, 224, "cos = 0.5, sin ≈ 0.87", "t", 3, 15))
    return els


def fig_w3_cos():
    p = Plot(0, 2 * math.pi + 0.4, -1.3, 1.3, 50, 40, 380, 190)
    els = p.axes("θ", "cos θ", xt=[math.pi / 2, math.pi, 3 * math.pi / 2, 2 * math.pi], yt=[1, -1],
                 xtl=["π/2", "π", "3π/2", "2π"], xty=246)
    els.append(p.curve(math.cos, 0, 2 * math.pi + 0.4, "e2", 1))
    for k in range(5):
        els.append(p.dot(k * math.pi / 2, math.cos(k * math.pi / 2), "n2", 2))
    els.append(T(p.px(math.pi), p.py(-1) + 24, "cos π = -1", "tb", 2, 14))
    els.append(T(240, 22, "0 에서 2π 까지 한 번 출렁이고 다시 반복", "tm", 2, 14))
    return els


def fig_w3_two():
    p = Plot(0, 2 * math.pi + 0.3, -1.3, 1.3, 50, 45, 380, 180)
    els = p.axes("t", "", xt=[math.pi, 2 * math.pi], yt=[1, -1], xtl=["π", "2π"], xty=242)
    els.append(p.curve(math.cos, 0, 2 * math.pi + 0.3, "e", 1))
    els.append(T(p.px(2 * math.pi) - 4, p.py(1) - 10, "cos t", "t", 1, 15, "end"))
    els.append(p.curve(lambda t: math.cos(2 * t), 0, 2 * math.pi + 0.3, "e2", 2))
    els.append(A(p.px(0), p.py(1.18), p.px(math.pi), p.py(1.18), "e2", 3, 7))
    els.append(T(p.px(math.pi / 2), p.py(1.18) - 7, "cos 2t 의 주기 π", "tb", 3, 14))
    els.append(T(240, 262, "ω 가 2배가 되면 주기는 절반: T = 2π/ω", "tm", 3, 14))
    return els


def fig_w3_phase():
    p = Plot(-1.0, 3.6, -1.3, 1.3, 50, 45, 380, 180)
    els = p.axes("t", "", xt=[-0.5, 1, 2, 3], yt=[], xty=242)
    els.append(p.curve(lambda t: math.cos(2 * t), -1.0, 3.6, "e", 1))
    els.append(T(p.px(math.pi) + 2, p.py(1) - 10, "cos 2t", "t", 1, 15))
    els.append(p.curve(lambda t: math.cos(2 * t + 1), -1.0, 3.6, "e2", 2))
    els.append(p.dot(-0.5, 1, "n2", 2))
    els.append(A(p.px(0), p.py(1.2), p.px(-0.5), p.py(1.2), "e2", 3, 7))
    els.append(T(p.px(0.2), p.py(1.2) - 6, "왼쪽 0.5", "tb", 3, 14, "start"))
    els.append(T(240, 262, "cos(2t+1) = cos(2(t+0.5)): 꼭대기가 0 에서 -0.5 로", "tm", 3, 14))
    return els


UNITS.append(unit(
    "wb-3", "각도, 라디안, 사인과 코사인",
    r"도와 라디안을 바꾸고, 단위원에서 cos, sin 값을 읽고, $\cos(\omega t+\phi)$ 의 주기, 진폭, 위상을 구할 수 있어요.",
    ["라디안", "단위원", "사인파 신호", "진폭", "주파수", "각주파수", "위상", "기본 주기"],
    ["시간 이동", "앞당김"],
    [
        title("각도, 라디안, 사인과 코사인", "원 위를 도는 점에서 출렁이는 파도가 나와요"),
        goal(r"도($^\circ$)와 [[라디안|을/를]] 바꿔요: $180^\circ=\pi$.",
             r"[[단위원]] 위의 점으로 $\cos$, $\sin$ 값을 읽어요.",
             r"$\cos(\omega t)$ 의 [[기본 주기]] $2\pi/\omega$, [[진폭]], [[위상|을/를]] 구해요."),
        pts("각도를 재는 두 가지 단위",
            r"한 바퀴를 360조각 낸 하나가 1도예요. 한 바퀴 $=360^\circ$.",
            r"이 과목은 [[라디안|을/를]] 써요. 한 바퀴 $=2\pi$ 라디안이에요.",
            r"$\pi$ 는 '파이', 약 $3.14$ 예요. 그래서 한 바퀴는 약 $6.28$ 라디안이에요.",
            r"반 바퀴 $180^\circ=\pi$, $1/4$ 바퀴 $90^\circ=\pi/2$ 예요."),
        fig("도와 [[라디안]] 짝 맞추기", fig_w3_angles(),
            r"오른쪽(0)에서 시작해 시계 반대 방향으로 돌아요. 위가 $\pi/2$, 왼쪽이 $\pi$ 예요."),
        stp("손계산 1: 도를 [[라디안|으로/로]]", r"규칙: 도 $\times\ \pi/180$ = 라디안",
            [r"$90^\circ$: $90\times\pi/180=\pi/2$",
             r"$60^\circ$: $60\times\pi/180=\pi/3$",
             r"$45^\circ$: $45\times\pi/180=\pi/4$",
             r"거꾸로 $1$ 라디안은 $180/\pi\approx 57.3^\circ$ 예요."],
            r"$180^\circ=\pi$ 하나만 외우면 나머지는 비례로 나와요."),
        ana("원 위를 도는 점",
            "반지름이 1인 원형 트랙을 한 사람이 일정한 빠르기로 돌아요. 그 사람의 가로 위치와 세로 위치를 계속 적으면 출렁이는 기록 두 개가 생겨요.",
            ["반지름 1인 원형 트랙", "[[단위원]]"],
            ["출발점(오른쪽)에서 돈 각도", r"각도 $\theta$, 단위는 [[라디안]]"],
            ["가로축에 비친 그림자(가로 위치)", r"$\cos\theta$"],
            ["세로축에 비친 그림자(세로 위치)", r"$\sin\theta$"]),
        fig(r"[[단위원]] 위의 점은 $(\cos\theta, \sin\theta)$", fig_w3_unit(),
            r"각도 $\theta$ 만큼 돈 점의 가로 좌표가 $\cos\theta$, 세로 좌표가 $\sin\theta$ 예요."),
        stp("손계산 2: 네 방향의 값", "[[단위원]]에서 점이 어디 있는지만 보면 돼요",
            [r"$\theta=0$: 오른쪽 끝 $(1,0)$. $\cos 0=1$, $\sin 0=0$",
             r"$\theta=\pi/2$: 맨 위 $(0,1)$. $\cos=0$, $\sin=1$",
             r"$\theta=\pi$: 왼쪽 끝 $(-1,0)$. $\cos\pi=-1$, $\sin\pi=0$",
             r"$\theta=3\pi/2$: 맨 아래 $(0,-1)$. $\cos=0$, $\sin=-1$",
             r"$\theta=2\pi$: 한 바퀴 돌아 다시 $(1,0)$"],
            "외우지 말고 원을 그려서 점 위치를 읽어요."),
        fig(r"가로 위치를 시간 순서로 펴면 $\cos$ 파도", fig_w3_cos(),
            r"이렇게 출렁이는 모양의 신호가 [[사인파 신호|이에요/예요]]. $\cos$ 도 $\sin$ 도 모두 사인파라고 불러요."),
        chk(r"$\cos\pi$ 의 값은?", ["$-1$", "$0$", "$1$", r"$\pi$"], 0,
            r"$\pi$ 는 반 바퀴. [[단위원]]의 왼쪽 끝 $(-1,0)$ 이라 가로 좌표 $\cos\pi=-1$ 이에요."),
        pts("시간에 따라 돌면 [[사인파 신호]]",
            r"각도가 시간에 비례해 커지면 $\theta=\omega t$ 예요.",
            r"$\omega$ 는 '오메가'. 1초에 몇 [[라디안]] 도는지인 [[각주파수|예요/이에요]].",
            r"한 바퀴($2\pi$) 돌면 제자리라서 값이 반복돼요.",
            "반복 간격 중 가장 짧은 것이 [[기본 주기]] $T_0$ 예요."),
        fml("[[기본 주기]] 구하는 식 (S2 p.25)", r"T_0 = \frac{2\pi}{\omega_0}",
            [("T_0", "[[기본 주기]]. 한 번 출렁이는 데 걸리는 시간(초)"),
             (r"2\pi", "한 바퀴 각도(라디안)"),
             (r"\omega_0", "[[각주파수]]. 1초에 도는 각도(rad/s)")],
            "티 제로는 이 파이 나누기 오메가 제로. 한 바퀴를 1초에 도는 각도로 나누면 한 바퀴 시간이에요."),
        stp("손계산 3: 주기 구하기", r"$T_0=2\pi/\omega_0$ 에 넣기만 하면 돼요",
            [r"$\cos(2t)$: $\omega_0=2$, $T_0=2\pi/2=\pi\approx 3.14$ 초",
             r"$\cos(4t)$: $\omega_0=4$, $T_0=2\pi/4=\pi/2$ (1장 과제 힌트와 같아요)",
             r"$\cos(\pi t)$: $\omega_0=\pi$, $T_0=2\pi/\pi=2$ 초"],
            "[[각주파수]]가 클수록 빨리 돌아서 [[기본 주기|이/가]] 짧아요."),
        fig(r"$\omega$ 가 2배면 주기는 절반", fig_w3_two(),
            r"$\cos t$ 는 $2\pi$ 마다, $\cos 2t$ 는 $\pi$ 마다 반복해요."),
        fml("[[사인파 신호]]의 모든 부품 (S2 p.27)", r"x(t) = A\cos(\omega_0 t + \phi)",
            [("A", "[[진폭]]. 가운데에서 위아래로 가장 멀리 가는 높이"),
             (r"\omega_0", r"[[각주파수]](rad/s). $\omega_0=2\pi f_0$"),
             (r"\phi", "[[위상]]. '파이'라고 읽어요. 출발 각도"),
             (r"f_0=\frac{\omega_0}{2\pi}", "[[주파수]](Hz). 1초에 몇 번 반복하는지, $1/T_0$")],
            r"에이 코사인 오메가 제로 티 더하기 파이. 높이 $A$, 빠르기 $\omega_0$, 출발 각도 $\phi$ 인 파도예요."),
        stp(r"손계산 4: $3\cos(2t+1)$ 해부하기", r"S2 p.27 의 $\cos(2t+1)$ 에 [[진폭]] 3을 붙였어요",
            ["[[진폭]] $A=3$. 파도는 $-3$ 과 $3$ 사이를 오가요.",
             r"[[각주파수]] $\omega_0=2$, [[기본 주기]] $T_0=2\pi/2=\pi$.",
             r"[[주파수]] $f_0=1/T_0=1/\pi\approx 0.32$ Hz.",
             r"[[위상]] $\phi=1$. $2t+1=2(t+0.5)$ 로 묶으면 $t+0.5$ 꼴이에요.",
             r"앞 단원 [[앞당김]]: $t+0.5$ 는 왼쪽으로 $0.5$. 즉 $\phi/\omega_0$ 만큼 옮겨요."],
            r"$A=3$, $T_0=\pi$, 왼쪽으로 $0.5$ 옮긴 $\cos$. [[위상|은/는]] 결국 [[시간 이동|이에요/예요]]."),
        fig("[[위상|은/는]] 파도를 옆으로 옮겨요", fig_w3_phase(),
            r"$\cos(2t+1)$ 의 꼭대기는 $t=-0.5$ 에 있어요. S2 p.29 그림의 $\phi/\omega$ 가 이 거리예요."),
        chk(r"$\cos(4t)$ 의 [[기본 주기|은/는]]?", [r"$\pi/2$", r"$4\pi$", r"$2\pi$", r"$\pi/4$"], 0,
            r"$T_0=2\pi/\omega_0=2\pi/4=\pi/2$ 예요."),
        chk(r"한 바퀴가 $2\pi$ 인 각도 단위는?", ["[[라디안]]", "[[주파수]]", "[[진폭]]", "[[위상]]"], 0,
            r"[[라디안|은/는]] 각도 단위예요. $180^\circ=\pi$ 라디안."),
        warn("헷갈리기 쉬운 점",
             r"$\cos$ 안의 수는 도가 아니라 [[라디안|이에요/예요]]. $\cos(1)$ 은 약 $57^\circ$ 의 코사인, 약 $0.54$ 예요.",
             r"[[각주파수]] $\omega$ (rad/s) 와 [[주파수]] $f$ (Hz) 는 달라요. $\omega=2\pi f$.",
             r"주기는 $2\pi/\omega$. $\omega$ 가 커지면 주기는 짧아져요."),
        where(r"S2 p.18: $\sin(t)$ 는 [[기본 주기]] $T_0=2\pi$ 로 반복",
              r"S2 p.25: $T=2\pi/\omega_0$, $\omega_0=2\pi/T$, $f_0=\omega_0/2\pi=1/T$",
              r"S2 p.27: $\cos(\omega_0 t+\phi)$, 예 $\cos(2t+1)$ 의 $T_0=\pi$. p.29: $A\cos(\omega t+\phi)$ 와 도는 점",
              r"S2 p.87 1장 과제(주기 구하기): 힌트 $T=2\pi/4$",
              r"시험 모양: '이 신호의 주기는?' 계산 문제. $2\pi/\omega$ 를 바로 써요."),
        recap(r"한 바퀴 $=360^\circ=2\pi$ [[라디안]], $180^\circ=\pi$.",
              r"[[단위원]] 위 점은 $(\cos\theta,\sin\theta)$. 오른쪽 $1$, 위 $j$ 방향은 다음 단원에서!",
              r"$A\cos(\omega_0 t+\phi)$: [[진폭]] $A$, [[각주파수]] $\omega_0$, [[위상]] $\phi$.",
              r"[[기본 주기]] $T_0=2\pi/\omega_0$, [[주파수]] $f_0=1/T_0$."),
    ]))


# ================================================================ wb-4 지수함수와 e
assert 2 ** 3 == 8 and 2 ** 0 == 1 and 2 ** -1 == 0.5
EN = {n: (1 + 1 / n) ** n for n in (1, 2, 10, 1000)}
assert EN[1] == 2 and EN[2] == 2.25 and round(EN[10], 3) == 2.594 and round(EN[1000], 3) == 2.717
assert round(math.e, 3) == 2.718
EUP = [round(math.exp(t), 2) for t in range(4)]
EDN = [round(math.exp(-t), 3) for t in range(4)]
assert EUP == [1.0, 2.72, 7.39, 20.09] and EDN == [1.0, 0.368, 0.135, 0.05]
LN2 = math.log(2)
assert round(LN2, 2) == 0.69 and round(math.exp(-0.69), 2) == 0.50
assert round(math.exp(-2 * LN2), 3) == 0.25 and round(math.exp(-3 * LN2), 3) == 0.125
assert round(2 * 0.69, 2) == 1.38 and round(3 * 0.69, 2) == 2.07
assert round(math.exp(0.2 * 10), 2) == 7.39 and round(math.exp(0.2 * -10), 3) == 0.135 and abs(math.exp(0.2 * 5) - math.e) < 1e-12
A05 = [0.5 ** n for n in range(4)]
AN05 = [(-0.5) ** n for n in range(4)]
assert A05 == [1, 0.5, 0.25, 0.125] and AN05 == [1, -0.5, 0.25, -0.125]
for n in range(6):
    assert abs(0.5 ** n - math.exp(-LN2 * n)) < 1e-12
assert round(LN2 / 2, 2) == 0.35
# 통장 잔고 1% 이자 (S2 p.60): 1.01 을 곱해 가기
BAL = [100 * 1.01 ** n for n in range(4)]
assert [round(b, 2) for b in BAL] == [100, 101, 102.01, 103.03]


def fig_w4_growdecay():
    p = Plot(-2.2, 2.2, 0, 8, 60, 35, 360, 180)
    els = p.axes("t", "", xt=[-2, -1, 1, 2], yt=[1, 2.72, 7.39], ytl=["1", "e", "e²"])
    els.append(p.curve(math.exp, -2.2, 2.05, "e2", 1))
    els.append(T(p.px(2.05) + 6, p.py(7.6), "e^t", "tb", 1, 15, "start"))
    els.append(p.curve(lambda t: math.exp(-t), -2.05, 2.2, "e", 2))
    els.append(T(p.px(-2.05) - 6, p.py(7.6), "e^-t", "tb", 2, 15, "end"))
    els.append(p.dot(0, 1, "n2", 3))
    els.append(T(p.px(0) + 10, p.py(1) - 10, "t = 0 에서 둘 다 1", "tb", 3, 14, "start"))
    els.append(T(240, 262, "a > 0 이면 폭발적으로 커지고, a < 0 이면 0 으로 잦아들어요", "tm", 3, 14))
    return els


def fig_w4_half():
    p = Plot(0, 3.3, 0, 1.15, 60, 35, 360, 190)
    els = p.axes("t", "e^-t", xt=[0.69, 1.39, 2.08], yt=[0.25, 0.5, 1])
    els.append(p.curve(lambda t: math.exp(-t), 0, 3.3, "e2", 1))
    for k, lab in [(1, "0.5"), (2, "0.25"), (3, "0.125")]:
        t = k * LN2
        els.append(L(p.px(t), p.py(0), p.px(t), p.py(math.exp(-t)), "e", 2))
        els.append(p.dot(t, math.exp(-t), "n2", 2))
        els.append(T(p.px(t) + 8, p.py(math.exp(-t)) - 8, lab, "tb", 2, 14, "start"))
    els.append(T(240, 262, "약 0.69 초 지날 때마다 절반, 또 절반", "tm", 2, 14))
    return els


def fig_w4_dt():
    p1 = Plot(-0.6, 5.6, -0.7, 1.2, 30, 45, 190, 170)
    p2 = Plot(-0.6, 5.6, -0.7, 1.2, 260, 45, 190, 170)
    els = p1.axes("n", "(0.5)^n", xt=[1, 2, 3, 4, 5], yt=[1], xty=232)
    els += p1.stems(range(6), [0.5 ** n for n in range(6)], "n2", 1)
    els += p2.axes("n", "(-0.5)^n", xt=[1, 2, 3, 4, 5], yt=[1], b=2, xty=232)
    els += p2.stems(range(6), [(-0.5) ** n for n in range(6)], "n2", 2)
    els.append(T(240, 262, "0 < α < 1 이면 줄고, 음수 α 면 부호가 번갈아 바뀌며 줄어요", "tm", 2, 14))
    return els


def fig_w4_damped():
    p = Plot(0, 10.5, -1.2, 1.2, 50, 40, 380, 190)
    els = p.axes("t", "", xt=[2, 4, 6, 8, 10], yt=[1, -1], xty=246)
    els.append(p.curve(lambda t: math.exp(-0.25 * t), 0, 10.5, "e", 1))
    els.append(p.curve(lambda t: -math.exp(-0.25 * t), 0, 10.5, "e", 1))
    els.append(T(p.px(1.0) + 12, p.py(1.08), "포락선 e^(-0.25t)", "tb", 1, 14, "start"))
    els.append(p.curve(lambda t: math.exp(-0.25 * t) * math.cos(3 * t), 0, 10.5, "e2", 2, 400))
    els.append(T(240, 262, "출렁임(cos)의 높이가 지수함수 틀 안에서 줄어요", "tm", 2, 14))
    return els


UNITS.append(unit(
    "wb-4", "지수함수와 e",
    r"$e\approx 2.718$ 의 뜻을 알고, $e^{at}$ 와 $\alpha^n$ 이 커지는지 줄어드는지 표로 계산할 수 있어요.",
    ["지수함수", "실수 지수 신호", "감쇠 사인파", "포락선"],
    ["사인파 신호", "진폭", "이산시간 신호"],
    [
        title("지수함수와 e", "곱하기가 계속 쌓이면 폭발하거나 사라져요"),
        goal(r"$e\approx 2.718$ 이 어디서 오는지 손으로 확인해요.",
             "$e^{at}$ 는 $a>0$ 이면 커지고 $a<0$ 이면 줄어드는 것을 표로 봐요.",
             "$e^{-t}$ 가 약 $0.69$ 초마다 절반이 되는 것을 계산해요."),
        pts("거듭제곱부터 다시",
            r"$2^3=2\times 2\times 2=8$. 오른쪽 위 작은 수는 곱하는 횟수예요.",
            "$2^0=1$. 한 번도 안 곱하면 1이에요.",
            "$2^{-1}=1/2$. 지수가 음수면 나누기예요.",
            r"규칙: $a^m\times a^n=a^{m+n}$. 곱하면 지수끼리 더해요."),
        ana("통장 잔고와 폭주",
            "통장 잔고는 지난 입금이 쌓여 있어요. 매달 1% 이자가 붙으면 이번 달 잔고는 지난달 잔고의 1.01배예요. 곱하기가 매달 쌓이니 점점 빨리 불어나요.",
            ["매달 같은 비율(1.01배)을 곱하기", "[[지수함수]]: 같은 비율로 계속 곱해지는 값"],
            ["곱하는 수가 1보다 큼", "$a>0$: 커지는 쪽, 계속 두면 폭주"],
            ["곱하는 수가 1보다 작음", "$a<0$: 0으로 잦아드는 쪽"]),
        stp("손계산 1: 1% 이자 잔고 (S2 p.60 의 통장 예)", "처음 잔고 100, 매달 $1.01$ 배",
            ["0달: $100$",
             r"1달: $100\times 1.01=101$",
             r"2달: $101\times 1.01=102.01$",
             r"3달: $102.01\times 1.01\approx 103.03$"],
            r"$n$ 달 뒤 잔고는 $100\times 1.01^n$. 같은 비율 곱하기가 [[지수함수]]의 뼈대예요."),
        stp("손계산 2: 특별한 수 $e$ 찾기", "$(1+1/n)^n$ 에서 $n$ 을 점점 키워요",
            ["$n=1$: $(1+1)^1=2$",
             "$n=2$: $(1.5)^2=2.25$",
             r"$n=10$: $(1.1)^{10}\approx 2.594$",
             r"$n=1000$: $(1.001)^{1000}\approx 2.717$"],
            r"끝없이 키우면 $2.71828\dots$ 에 다가가요. 이 수를 $e$ 라고 불러요."),
        fml("[[지수함수]] $e^{at}$ 읽기 (S2 p.22)", r"x(t) = C e^{at}",
            [("C", "$t=0$ 일 때의 값. $e^0=1$ 이니까 $x(0)=C$"),
             ("e", "약 $2.718$ 인 정해진 수. '이' 라고 읽어요"),
             ("a", "커지는 빠르기. 양수면 커지고 음수면 줄어요"),
             ("t", "시간")],
            "엑스 오브 티는 씨 곱하기 이의 에이티 제곱. $C$ 와 $a$ 가 실수면 [[실수 지수 신호|예요/이에요]]."),
        stp("손계산 3: $e^t$ 와 $e^{-t}$ 표", "계산기 값을 반올림했어요",
            ["$t=0$: $e^0=1$, $e^{-0}=1$",
             r"$t=1$: $e^1\approx 2.72$, $e^{-1}\approx 0.368$",
             r"$t=2$: $e^2\approx 7.39$, $e^{-2}\approx 0.135$",
             r"$t=3$: $e^3\approx 20.09$, $e^{-3}\approx 0.050$"],
            "$e^t$ 는 1초마다 약 $2.72$ 배로 불고, $e^{-t}$ 는 1초마다 약 $0.37$ 배로 줄어요."),
        fig("커지는 [[지수함수]], 줄어드는 [[지수함수]]", fig_w4_growdecay(),
            "S2 p.22 의 growth($a>0$), decay($a<0$) 그림과 같은 모양이에요. 좌우 거울 사이예요."),
        stp("손계산 4: 절반이 되는 시간", r"$e^{0.69}\approx 2$ 라서 $e^{-0.69}\approx 0.5$ 예요",
            [r"$t=0.69$: $e^{-0.69}\approx 0.5$",
             r"$t=1.38$: 지수 규칙으로 $e^{-0.69}\times e^{-0.69}\approx 0.25$",
             r"$t=2.07$: 한 번 더 곱해 $\approx 0.125$",
             "$e^{-2t}$ 는 두 배 빨라서 약 $0.35$ 초마다 절반이에요."],
            "$e^{-t}$ 는 약 $0.69$ 초마다 절반이 돼요. 반으로, 또 반으로 줄지만 0이 되지는 않아요."),
        fig("반으로, 또 반으로", fig_w4_half(),
            "$e^{-t}$ 는 일정한 시간마다 같은 비율(절반)로 줄어요. 이것이 [[지수함수]]의 성질이에요."),
        chk("다음 중 시간이 갈수록 0으로 줄어드는 것은?", ["$e^{-3t}$", "$e^{3t}$", "$e^{0t}$", "$3e^{t}$"], 0,
            "$e^{at}$ 에서 $a$ 가 음수면 줄어요. $a=-3$ 인 $e^{-3t}$ 예요. $e^{0t}=1$ 은 그대로예요."),
        stp("손계산 5: S2 p.22 그래프 눈금 읽기", r"그림의 곡선은 $\exp(0.2t)=e^{0.2t}$",
            ["$t=0$: $e^0=1$. 두 곡선이 만나는 높이예요.",
             r"$t=5$: $e^{0.2\times 5}=e^1\approx 2.72$",
             r"$t=10$: $e^{2}\approx 7.39$. 그림 오른쪽 끝 높이와 같아요.",
             r"$t=-10$: $e^{-2}\approx 0.135$. 거의 바닥이에요."],
            "슬라이드 그래프의 숫자도 표로 직접 확인할 수 있어요."),
        pts(r"이산 버전: $x[n]=C\alpha^n$ (S2 p.38)",
            r"[[이산시간 신호|은/는]] 정수 칸마다 $\alpha$ (알파)를 한 번씩 곱해요.",
            r"$\alpha=0.5$: $1, 0.5, 0.25, 0.125, \dots$ 로 줄어요.",
            r"$\alpha=2$: $1, 2, 4, 8, \dots$ 로 커져요.",
            r"$\alpha=-0.5$: $1, -0.5, 0.25, -0.125$. 부호가 번갈아 바뀌며 줄어요.",
            r"S2 p.38: $\alpha=e^{\beta}$. 예를 들어 $0.5^n=e^{-0.69n}$ 이에요."),
        fig(r"$\alpha^n$ 막대 그림", fig_w4_dt(),
            r"S2 p.38 그림 (b), (c) 와 같은 모양이에요. $|\alpha|<1$ 이면 줄어요."),
        cmp("커질까 줄어들까", ["신호", "커지는 경우", "줄어드는 경우"],
            [["$e^{at}$ (연속)", "$a>0$", "$a<0$"],
             [r"$\alpha^n$ (이산)", r"$|\alpha|>1$", r"$|\alpha|<1$"],
             ["부호가 번갈아", "(연속에는 없음)", r"$\alpha$ 가 음수일 때"]]),
        fig("[[감쇠 사인파]]와 [[포락선]]", fig_w4_damped(),
            "[[사인파 신호]]에 $e^{-0.25t}$ 를 곱하면 [[진폭|이/가]] 줄어드는 [[감쇠 사인파|예요/이에요]]."),
        pts("[[감쇠 사인파]] 읽기 (S2 p.37)",
            r"$e^{-0.25t}\cos(3t)$ 는 곱하기 두 개예요.",
            r"$\cos(3t)$ 는 출렁임, $e^{-0.25t}$ 는 줄어드는 높이예요.",
            r"출렁임의 위아래 끝을 이은 바깥 선 $\pm e^{-0.25t}$ 가 [[포락선|이에요/예요]].",
            r"S2 p.37 그림의 점선 $\pm Ce^{rt}$ 가 바로 [[포락선|이에요/예요]]."),
        chk("출렁이는 신호의 위아래 끝을 이은 바깥 선을 뭐라고 하나요?",
            ["[[포락선]]", "[[감쇠 사인파]]", "[[실수 지수 신호]]", "[[진폭]]"], 0,
            "[[포락선|은/는]] 출렁임을 감싸는 선이에요. [[감쇠 사인파|은/는]] 그 안에서 출렁이는 신호 자체예요."),
        warn("헷갈리기 쉬운 점",
             "$e^{-t}$ 는 음수가 아니에요. 늘 양수이고 0에 가까워질 뿐이에요.",
             "$e^{at}$ 의 $a$ 부호가 커지는지 줄어드는지를 정해요. $C$ 는 처음 높이일 뿐이에요.",
             r"이산 $\alpha^n$ 은 $\alpha$ 크기가 1보다 작은지 큰지를 봐요."),
        where("S2 p.22: [[실수 지수 신호]] $Ce^{at}$, $a>0$ growth, $a<0$ decay",
              r"S2 p.37: [[감쇠 사인파]], 점선 [[포락선]] $\pm Ce^{rt}$. p.38: 이산 $C\alpha^n$, $\alpha=e^{\beta}$",
              r"S3 p.3: $e^{(\sigma+j\omega)t}=e^{\sigma t}e^{j\omega t}$. 앞쪽 $e^{\sigma t}$ 가 커짐, 줄어듦",
              r"S3 p.30, p.31 Example 2.3: $\alpha^n u[n]$. S3 p.46 Example 2.6: $\frac{1}{a}(1-e^{-at})$",
              "시험 모양: 신호가 커지는지, 줄어드는지, 주기적인지 고르는 문제의 바탕이에요."),
        recap(r"$e\approx 2.718$. $(1+1/n)^n$ 을 끝없이 키운 값이에요.",
              "$e^{at}$: $a>0$ 커짐, $a<0$ 줄어듦. $t=0$ 에서 늘 1이에요.",
              "$e^{-t}$ 는 약 $0.69$ 초마다 절반이 돼요.",
              r"이산 $\alpha^n$: $|\alpha|<1$ 이면 줄고, 음수 $\alpha$ 면 부호가 번갈아요."),
    ]))


# ================================================================ wb-5 복소수와 복소평면
j = 1j
assert j ** 2 == -1 and j ** 3 == -j and j ** 4 == 1
assert (3 + 2j) + (1 + 4j) == 4 + 6j
assert (1 + 2j) * (3 + 1j) == 1 + 7j
assert abs(3 + 4j) == 5 and abs(6 + 8j) == 10
assert (3 + 4j).conjugate() == 3 - 4j and (3 + 4j) * (3 - 4j) == 25
assert j * (3 + 4j) == -4 + 3j
assert round(abs(1 + 1j), 3) == 1.414 and abs(cmath.phase(1 + 1j) - math.pi / 4) < 1e-12
assert round(math.degrees(cmath.phase(3 + 4j)), 1) == 53.1
assert abs(2 * math.cos(math.pi / 3) - 1) < 1e-12 and round(2 * math.sin(math.pi / 3), 3) == 1.732


def _cplane(cx, cy, s, rng, b=0, re_lab=True):
    els = [A(cx - rng * s - 10, cy, cx + rng * s + 14, cy, "e", b, 7),
           A(cx, cy + rng * s + 10, cx, cy - rng * s - 14, "e", b, 7)]
    if re_lab:
        els.append(T(cx + rng * s + 16, cy - 6, "실수", "tm", b, 14, "start"))
        els.append(T(cx + 8, cy - rng * s - 6, "허수(j)", "tm", b, 14, "start"))
    return els


def fig_w5_point():
    cx, cy, s = 150, 215, 38
    els = _cplane(cx, cy, s, 4.4)
    for k in (1, 2, 3, 4):
        els.append(L(cx + k * s, cy - 3, cx + k * s, cy + 3))
        els.append(T(cx + k * s, cy + 18, str(k), "tm", 0, 14))
        els.append(L(cx - 3, cy - k * s, cx + 3, cy - k * s))
        els.append(T(cx - 8, cy - k * s + 5, str(k), "tm", 0, 14, "end"))
    x, y = cx + 3 * s, cy - 4 * s
    els.append(L(x, y, x, cy, "e", 1))
    els.append(L(x, y, cx, y, "e", 1))
    els.append(C(x, y, 6, "n2", 1))
    els.append(T(x + 10, y - 6, "3 + j4", "tb", 1, 16, "start"))
    els.append(L(cx, cy, x, y, "e2", 2))
    els.append(T(188, 118, "크기 5", "tb", 2, 15))
    els.append(T(cx + 34, cy - 8, "각도", "tb", 3, 14, "start"))
    els.append(T(390, 110, "가로 3 = 실수부", "t", 1, 15))
    els.append(T(390, 135, "세로 4 = 허수부", "t", 1, 15))
    els.append(T(390, 175, "3² + 4² = 25", "t", 2, 15))
    els.append(T(390, 200, "√25 = 5", "t", 2, 15))
    return els


def fig_w5_add():
    cx, cy, s = 70, 230, 32
    els = _cplane(cx, cy, s, 6.4, 0, False)
    a, bb, c = (3, 2), (1, 4), (4, 6)
    P = lambda q: (cx + q[0] * s, cy - q[1] * s)
    els.append(A(*P((0, 0)), *P(a), "e2", 1))
    els.append(T(P(a)[0] + 8, P(a)[1] + 16, "3 + j2", "tb", 1, 15, "start"))
    els.append(A(*P(a), *P(c), "e2", 2))
    els.append(T((P(a)[0] + P(c)[0]) / 2 + 12, (P(a)[1] + P(c)[1]) / 2 + 10, "+ (1 + j4)", "tb", 2, 15, "start"))
    els.append(C(*P(c), 6, "n2", 3))
    els.append(T(P(c)[0] + 10, P(c)[1] - 4, "4 + j6", "tb", 3, 16, "start"))
    els.append(T(360, 250, "가로끼리, 세로끼리 더해요", "tm", 3, 14))
    return els


def fig_w5_conj_rot():
    cx, cy, s = 240, 140, 24
    els = _cplane(cx, cy, s, 4.8, 0, False)
    P = lambda z: (cx + z.real * s, cy - z.imag * s)
    z = 3 + 4j
    els.append(L(cx, cy, *P(z), "e2", 1))
    els.append(C(*P(z), 6, "n2", 1))
    els.append(T(P(z)[0] + 10, P(z)[1] + 4, "z = 3 + j4", "tb", 1, 15, "start"))
    els.append(L(cx, cy, *P(z.conjugate()), "e", 2))
    els.append(C(*P(z.conjugate()), 6, "n3", 2))
    els.append(T(P(z.conjugate())[0] + 10, P(z.conjugate())[1] + 4, "켤레 3 - j4", "tb", 2, 15, "start"))
    w = 1j * z
    els.append(L(cx, cy, *P(w), "e2", 3))
    els.append(C(*P(w), 6, "n4", 3))
    els.append(T(P(w)[0] - 10, P(w)[1] - 4, "jz = -4 + j3", "tb", 3, 15, "end"))
    els.append(T(120, 262, "j 를 곱하면 90° 회전", "tm", 3, 14))
    els.append(T(370, 262, "켤레는 가로축 거울", "tm", 2, 14))
    return els


UNITS.append(unit(
    "wb-5", "복소수와 복소평면",
    "$a+jb$ 를 복소평면의 점으로 찍고, 더하기, 곱하기, 크기, 각도, 켤레를 손으로 계산할 수 있어요.",
    ["복소수", "허수 단위", "복소평면", "켤레 복소수"],
    ["라디안", "단위원", "위상"],
    [
        title("복소수와 복소평면", "수를 가로 한 줄에서 평면 전체로 넓혀요"),
        goal("[[허수 단위]] $j$ 와 $j^2=-1$ 을 알아요.",
             "[[복소수]] $a+jb$ 를 [[복소평면]]의 점으로 찍어요.",
             "더하기, 곱하기, 크기, 각도, [[켤레 복소수|을/를]] 손으로 계산해요."),
        pts("제곱해서 $-1$ 이 되는 수",
            "$2^2=4$, $(-2)^2=4$. 보통 수는 제곱하면 음수가 안 돼요.",
            "그래서 '제곱하면 $-1$' 인 새 수를 만들었어요. 이것이 [[허수 단위|예요/이에요]].",
            "수학책은 $i$ 로 쓰지만 이 과목은 $j$ 로 써요. 전류 $i$ 와 헷갈리지 않으려고요.",
            "$j^2=-1$ 하나만 기억하면 나머지 계산은 보통 식 계산과 같아요."),
        stp("손계산 1: $j$ 를 계속 곱하기", "$j^2=-1$ 만 써요",
            ["$j^1=j$",
             "$j^2=-1$",
             r"$j^3=j^2\times j=-j$",
             r"$j^4=j^2\times j^2=(-1)(-1)=1$"],
            "$j, -1, -j, 1$ 이 네 번마다 되풀이돼요. 곧 이것이 '90도씩 돌기' 라는 걸 봐요."),
        fml("[[복소수]]의 모양", r"z = a + jb",
            [("a", r"실수부. $\mathrm{Re}\{z\}$ 라고 써요"),
             ("b", r"허수부. $\mathrm{Im}\{z\}$ 라고 써요. $j$ 는 빼고 숫자만"),
             ("j", "[[허수 단위]]. $j^2=-1$")],
            "제트는 에이 더하기 제이 비. 실수 부분과 허수 부분을 한 쌍으로 가진 수가 [[복소수|예요/이에요]]."),
        ana("원 위를 도는 점을 위한 평면",
            "원 위를 일정한 빠르기로 도는 점을 떠올려요. 이 점의 위치는 가로 위치와 세로 위치 두 숫자로 적어야 해요.",
            ["점의 가로 위치", "실수부 $a$"],
            ["점의 세로 위치", "허수부 $b$ ($j$ 방향)"],
            ["점이 사는 평면", "[[복소평면]]: 가로축 실수, 세로축 허수"]),
        fig("[[복소평면]]에 $3+j4$ 찍기", fig_w5_point(),
            "가로로 3칸, 위로 4칸 간 점이에요. 원점까지 거리가 크기, 가로축과 이루는 각이 각도예요."),
        stp("손계산 2: 더하기", "$(3+j2)+(1+j4)$",
            ["실수부끼리: $3+1=4$",
             "허수부끼리: $2+4=6$",
             "합치면 $4+j6$"],
            "$4+j6$. 가로끼리, 세로끼리 따로 더해요."),
        fig("더하기는 화살표 이어 붙이기", fig_w5_add(),
            "첫 [[복소수]] 화살표 끝에 둘째 화살표를 이어 붙인 끝이 합이에요."),
        stp("손계산 3: 곱하기", "$(1+j2)(3+j)$",
            [r"괄호 풀기: $1\times 3+1\times j+j2\times 3+j2\times j$",
             "정리: $3+j+j6+2j^2$",
             "$j^2=-1$ 넣기: $2j^2=-2$",
             "실수부 $3-2=1$, 허수부 $1+6=7$"],
            "$1+j7$. 보통 괄호 풀기에 $j^2=-1$ 하나만 더했어요."),
        chk("$j^2$ 의 값은?", ["$-1$", "$1$", "$j$", "$-j$"], 0,
            "[[허수 단위]] $j$ 는 제곱하면 $-1$ 이 되도록 만든 수예요."),
        stp("손계산 4: 크기와 각도", "$z=3+j4$",
            ["크기 $|z|$ 는 원점에서 점까지 거리. 직각삼각형의 빗변이에요.",
             r"$|z|=\sqrt{3^2+4^2}=\sqrt{9+16}=\sqrt{25}=5$",
             r"각도는 가로축에서 잰 각. $3+j4$ 는 약 $53.1^\circ$, 약 $0.93$ [[라디안|이에요/예요]].",
             r"쉬운 예: $1+j$ 는 크기 $\sqrt 2\approx 1.414$, 각도 $45^\circ=\pi/4$."],
            "[[복소수|은/는]] (크기, 각도) 쌍으로도 적을 수 있어요. 각도를 [[위상|이라고/라고]]도 해요."),
        pts("극좌표: 크기와 각도로 쓰기 (S2 p.36)",
            r"크기 $r$, 각도 $\theta$ 인 점은 가로 $r\cos\theta$, 세로 $r\sin\theta$ 예요.",
            r"그래서 $z=r\cos\theta+jr\sin\theta$ 로 쓸 수 있어요.",
            r"예: $r=2$, $\theta=\pi/3$ 이면 $2\cos(\pi/3)+j2\sin(\pi/3)=1+j1.732$.",
            "$r=1$ 이면 점은 [[단위원]] 위에 있어요. 다음 단원 오일러 공식의 무대예요."),
        stp("손계산 5: [[켤레 복소수]]", "$z=3+j4$ 의 켤레 $z^*$",
            ["허수부 부호만 바꿔요: $z^*=3-j4$",
             "곱해 보기: $(3+j4)(3-j4)=9-j12+j12-16j^2$",
             "$-16j^2=+16$ 이라서 $9+16=25$",
             "$25=5^2=|z|^2$. 허수부가 사라졌어요."],
            "$z z^*=|z|^2$. [[켤레 복소수|과/와]] 곱하면 늘 크기의 제곱인 실수가 나와요."),
        stp("손계산 6: $j$ 를 곱하면?", r"$j\times(3+j4)$",
            ["괄호 풀기: $j3+j^2 4$",
             "$j^2=-1$: $j3-4$",
             "정리: $-4+j3$",
             r"크기는 $\sqrt{16+9}=5$ 그대로. 위치는 왼쪽 위로 돌았어요."],
            r"$j$ 곱하기는 크기는 그대로 두고 $90^\circ$ 돌리기예요."),
        fig("[[켤레 복소수|와/과]] $j$ 곱하기", fig_w5_conj_rot(),
            r"켤레는 가로축에 비친 거울상, $j$ 를 곱하면 시계 반대 방향으로 $90^\circ$ 회전이에요."),
        chk("$6+j8$ 의 크기는?", ["$10$", "$14$", "$48$", "$2$"], 0,
            r"$\sqrt{6^2+8^2}=\sqrt{36+64}=\sqrt{100}=10$ 이에요."),
        chk("$2-j5$ 의 [[켤레 복소수|은/는]]?", ["$2+j5$", "$-2+j5$", "$-2-j5$", "$5-j2$"], 0,
            "허수부 부호만 바꿔요. 실수부 2는 그대로예요."),
        warn("헷갈리기 쉬운 점",
             "허수부는 $j$ 를 뺀 숫자예요. $3+j4$ 의 허수부는 $j4$ 가 아니라 $4$ 예요.",
             r"크기는 $a+b$ 가 아니라 $\sqrt{a^2+b^2}$ 예요. $3+j4$ 의 크기는 $7$ 이 아니라 $5$.",
             "켤레는 실수부가 아니라 허수부의 부호만 바꿔요."),
        where("S2 p.21: $x(t)=Ce^{at}$, '$C$ 와 $a$ 는 일반적으로 [[복소수]]'",
              r"S2 p.6: $|x(t)|$ 는 크기. 복소 신호에도 써요. S2 p.26: $\mathrm{Re}\{z\}$, $\mathrm{Im}\{z\}$ 축의 [[복소평면]]",
              r"S2 p.35, 36: $C=|C|e^{j\phi}$, 극좌표 $x=r\cos\theta$, $y=r\sin\theta$",
              r"S2 p.84 Example 1.19: $y[n]=\mathrm{Re}\{x[n]\}$ 는 $j$ 배에서 선형이 깨져요",
              "시험 모양: 크기, [[위상]] 계산과 복소 지수 신호 문제의 바탕이에요."),
        recap("[[허수 단위]] $j$: $j^2=-1$. 이 과목은 $i$ 대신 $j$.",
              "$a+jb$ 는 [[복소평면]]의 점 $(a,b)$. 더하기는 따로따로 더하기.",
              r"크기 $\sqrt{a^2+b^2}$, 각도는 가로축에서 잰 각.",
              r"켤레 $a-jb$, $zz^*=|z|^2$. $j$ 곱하기는 $90^\circ$ 회전."),
    ]))


# ================================================================ wb-6 오일러 공식과 회전
E = lambda th: cmath.exp(1j * th)
for th, want in [(0, 1), (math.pi / 2, 1j), (math.pi, -1), (3 * math.pi / 2, -1j), (2 * math.pi, 1)]:
    assert abs(E(th) - want) < 1e-12
assert abs(E(math.pi) + 1) < 1e-12
z4 = E(math.pi / 4)
assert round(z4.real, 3) == 0.707 and round(z4.imag, 3) == 0.707
for th in (0.3, 1.0, 2.5):
    assert abs(abs(E(th)) - 1) < 1e-12
    assert abs((E(th) + E(-th)) / 2 - math.cos(th)) < 1e-12
    assert abs((E(th) - E(-th)) / 2j - math.sin(th)) < 1e-12
z3 = E(math.pi / 3)
assert round(z3.real, 3) == 0.5 and round(z3.imag, 3) == 0.866
assert abs(1 * E(math.pi / 2) - 1j) < 1e-12 and abs(1j * E(math.pi / 2) + 1) < 1e-12
# 도는 점: omega0 = pi/2, t = 0..4
ROT = [E(math.pi / 2 * t) for t in range(5)]
for got, want in zip(ROT, [1, 1j, -1, -1j, 1]):
    assert abs(got - want) < 1e-12
assert abs(2 * math.pi / (math.pi / 2) - 4) < 1e-12
# 극형식: 1 + j = sqrt2 e^{j pi/4}
assert abs(math.sqrt(2) * E(math.pi / 4) - (1 + 1j)) < 1e-12
# 곱하면 크기는 곱하고 각도는 더하기
assert abs(2 * E(0.5) * 3 * E(0.7) - 6 * E(1.2)) < 1e-12


def fig_w6_circle():
    cx, cy, r = 200, 140, 95
    els = [C(cx, cy, r, "e"), A(cx - r - 25, cy, cx + r + 30, cy, "e", 0, 7), A(cx, cy + r + 20, cx, cy - r - 25, "e", 0, 7),
           T(cx + r + 34, cy + 5, "Re", "tm", 0, 14, "start"), T(cx - 8, cy - r - 14, "Im", "tm", 0, 14, "end")]
    pts_ = [(0, "e^(j0) = 1", 10, -10, "start"), (math.pi / 2, "e^(jπ/2) = j", 10, -8, "start"),
            (math.pi, "e^(jπ) = -1", -10, -10, "end"), (3 * math.pi / 2, "e^(j3π/2) = -j", 10, 18, "start")]
    for k, (th, lab, dx, dy, anc) in enumerate(pts_):
        x, y = cx + r * math.cos(th), cy - r * math.sin(th)
        els.append(C(x, y, 6, "n2", k + 1))
        els.append(T(x + dx, y + dy, lab, "tb", k + 1, 15, anc))
    return els


def fig_w6_shadow():
    cx, cy, r = 95, 140, 70
    th = math.pi / 3
    x, y = cx + r * math.cos(th), cy - r * math.sin(th)
    els = [C(cx, cy, r, "e"), L(cx - r - 10, cy, cx + r + 10, cy), L(cx, cy + r + 10, cx, cy - r - 10)]
    els.append(L(cx, cy, x, y, "e2", 1))
    els.append(C(x, y, 6, "n2", 1))
    els.append(T(cx, cy + r + 30, "e^(jωt) 가 돌아요", "tb", 1, 14))
    p = Plot(0, 2 * math.pi + 0.3, -1.25, 1.25, 215, 140 - 87.5, 235, 175)
    els.append(L(210, 140, 460, 140))
    els.append(p.curve(math.sin, 0, 2 * math.pi + 0.3, "e2", 2))
    els.append(L(x, y, p.px(th), p.py(math.sin(th)), "e", 2))
    els.append(C(p.px(th), p.py(math.sin(th)), 5, "n2", 2))
    els.append(T(p.px(4.6), p.py(-1) + 28, "세로 위치 = sin ωt", "tb", 2, 14))
    els.append(T(p.px(4.4), 38, "가로 위치는 cos ωt", "t", 3, 14))
    return els


def fig_w6_sum():
    cx, cy, s = 150, 140, 90
    els = _cplane(cx, cy, s, 1.2, 0, False)
    P = lambda z: (cx + z.real * s, cy - z.imag * s)
    a, bb = E(math.pi / 3), E(-math.pi / 3)
    els.append(L(cx, cy, *P(a), "e2", 1))
    els.append(C(*P(a), 6, "n2", 1))
    els.append(T(P(a)[0] + 10, P(a)[1] - 4, "e^(jπ/3)", "tb", 1, 15, "start"))
    els.append(L(cx, cy, *P(bb), "e2", 2))
    els.append(C(*P(bb), 6, "n3", 2))
    els.append(T(P(bb)[0] + 10, P(bb)[1] + 14, "e^(-jπ/3)", "tb", 2, 15, "start"))
    els.append(C(*P(0.5 + 0j), 6, "n4", 3))
    els.append(T(P(0.5)[0] - 8, cy + 22, "0.5", "tb", 3, 15))
    els.append(T(370, 110, "위아래가 상쇄돼요", "t", 3, 15))
    els.append(T(370, 140, "(합) ÷ 2 = 0.5", "tb", 3, 15))
    els.append(T(370, 170, "= cos(π/3)", "tb", 3, 15))
    return els


def fig_w6_spiral():
    p = Plot(-1.35, 1.35, -1.25, 1.25, 40, 20, 260, 240)
    els = [L(p.px(-1.35), p.py(0), p.px(1.35), p.py(0)), L(p.px(0), p.py(-1.25), p.px(0), p.py(1.25))]
    ptsg = [cmath.exp((-0.12 + 1j) * t) for t in np.linspace(0, 16, 500)]
    els.append(PL([(p.px(z.real), p.py(z.imag)) for z in ptsg], "e2", 1))
    els.append(C(p.px(1), p.py(0), 5, "n2", 1))
    els.append(T(p.px(1.02), p.py(0) + 22, "출발", "tb", 1, 14, "start"))
    els.append(T(400, 60, "e^(σt): 줄어듦", "tb", 2, 14))
    els.append(T(400, 85, "e^(jωt): 돌기", "tb", 2, 14))
    els.append(T(400, 110, "합치면 소용돌이", "t", 2, 14))
    return els


UNITS.append(unit(
    "wb-6", "오일러 공식과 회전",
    r"오일러 공식 $e^{j\theta}=\cos\theta+j\sin\theta$ 를 단위원 위 도는 점으로 읽고, $e^{j\pi}=-1$ 같은 값을 손으로 구할 수 있어요.",
    ["오일러 공식", "복소 지수 신호", "주기 신호", "테일러 급수"],
    ["단위원", "복소수", "복소평면", "각주파수", "지수함수"],
    [
        title("오일러 공식과 회전", "지수함수와 원 위를 도는 점이 한 식으로"),
        goal(r"[[오일러 공식]] $e^{j\theta}=\cos\theta+j\sin\theta$ 를 소리 내어 읽어요.",
             r"$e^{j\pi/2}=j$, $e^{j\pi}=-1$ 을 [[단위원]]에서 읽어요.",
             r"$e^{j\theta}$ 를 곱하면 $\theta$ 만큼 돈다는 것을 계산해요."),
        fml("[[오일러 공식]] (S2 p.23)", r"e^{j\theta} = \cos\theta + j\sin\theta",
            [(r"e^{j\theta}", "이의 제이 세타 제곱. [[지수함수]]에 $j$ 가 들어간 것"),
             (r"\cos\theta", "실수부: 가로 위치"),
             (r"j\sin\theta", "허수부: 세로 위치"),
             (r"\theta", "각도([[라디안]])")],
            "이의 제이 세타는 코사인 세타 더하기 제이 사인 세타. 교수님: 이 공식은 무조건 외우세요(증명은 안 외워도 돼요)."),
        ana("원 위를 일정한 빠르기로 도는 점",
            r"반지름 1인 원 위의 점이 시계 반대 방향으로 돌아요. 각도가 $\theta$ 일 때 점의 가로 위치가 $\cos\theta$, 세로 위치가 $\sin\theta$ 예요.",
            ["반지름 1인 원", r"[[단위원]]: $|e^{j\theta}|=1$"],
            ["점의 위치(가로, 세로)", r"[[복소수]] $\cos\theta+j\sin\theta$"],
            ["그 위치를 한 기호로", r"$e^{j\theta}$ ([[오일러 공식]])"],
            ["일정한 빠르기로 계속 돌기", r"[[복소 지수 신호]] $e^{j\omega_0 t}$"]),
        stp("손계산 1: 네 방향 값 (S2 p.25)", "3단원 값 표를 [[오일러 공식]]에 넣어요",
            [r"$\theta=0$: $\cos 0+j\sin 0=1+j0=1$",
             r"$\theta=\pi/2$: $0+j1=j$",
             r"$\theta=\pi$: $-1+j0=-1$",
             r"$\theta=3\pi/2$: $0+j(-1)=-j$"],
            r"$e^{j0}=1$, $e^{j\pi/2}=j$, $e^{j\pi}=-1$, $e^{j3\pi/2}=-j$. S2 p.25 의 원 그림 그대로예요."),
        fig("[[단위원]] 위의 네 점", fig_w6_circle(),
            r"$e^{j\theta}$ 는 늘 [[단위원]] 위에 있고, $\theta$ 가 그 각도예요 (S2 p.26)."),
        pts(r"유명한 한 줄: $e^{j\pi}+1=0$",
            r"$e^{j\pi}=-1$ 이니까 양쪽에 1을 더하면 $e^{j\pi}+1=0$.",
            "S2 p.23 오른쪽 상자의 Euler's Identity 예요.",
            "뜻은 간단해요. 반 바퀴 돈 점은 왼쪽 끝 $-1$ 에 있어요."),
        stp(r"손계산 2: $e^{j\pi/4}=?$ (S2 p.25 질문)", r"$\pi/4=45^\circ$",
            [r"[[오일러 공식]]: $e^{j\pi/4}=\cos(\pi/4)+j\sin(\pi/4)$",
             r"$45^\circ$ 에서는 가로 세로가 같아요: 둘 다 $\sqrt2/2\approx 0.707$",
             r"$e^{j\pi/4}\approx 0.707+j0.707$",
             r"크기 확인: $0.707^2+0.707^2\approx 0.5+0.5=1$"],
            r"$e^{j\pi/4}=\frac{\sqrt2}{2}+j\frac{\sqrt2}{2}$. [[단위원]] 위, 대각선 방향 점이에요."),
        chk(r"$e^{j\pi}$ 의 값은?", ["$-1$", "$1$", "$j$", "$0$"], 0,
            r"$\cos\pi+j\sin\pi=-1+j0=-1$. 반 바퀴 돈 점은 왼쪽 끝이에요."),
        pts("곱하면 각도가 더해져요",
            "[[지수함수]] 규칙 $e^a e^b=e^{a+b}$ 가 여기서도 통해요.",
            r"$e^{j\alpha}\times e^{j\beta}=e^{j(\alpha+\beta)}$. 각도끼리 더해요.",
            r"그래서 어떤 [[복소수]]에 $e^{j\theta}$ 를 곱하면 $\theta$ 만큼 돌아요.",
            r"5단원의 '$j$ 곱하기 $=90^\circ$ 회전' 은 $j=e^{j\pi/2}$ 이기 때문이에요."),
        stp("손계산 3: 돌리기", r"$e^{j\pi/2}=j$ 를 두 번 곱해요",
            [r"$1\times e^{j\pi/2}=j$: $0$ 에서 $\pi/2$ 로 돌았어요.",
             r"$j\times e^{j\pi/2}=j\times j=-1$: 다시 $\pi/2$ 돌아 $\pi$.",
             r"각도로 쓰면 $e^{j\pi/2}e^{j\pi/2}=e^{j\pi}=-1$. 같은 답이에요.",
             r"크기가 다르면: $2e^{j0.5}\times 3e^{j0.7}=6e^{j1.2}$. 크기는 곱하고 각도는 더해요."],
            "[[오일러 공식]] 덕분에 [[복소수]] 곱하기가 '크기 곱하기, 각도 더하기' 로 쉬워져요."),
        stp(r"손계산 4: 도는 점 $e^{j\omega_0 t}$", r"[[각주파수]] $\omega_0=\pi/2$ (1초에 $1/4$ 바퀴)",
            ["$t=0$: $e^{j0}=1$",
             r"$t=1$: $e^{j\pi/2}=j$",
             r"$t=2$: $e^{j\pi}=-1$, $t=3$: $e^{j3\pi/2}=-j$",
             r"$t=4$: $e^{j2\pi}=1$. 제자리예요.",
             r"주기 확인: $T_0=2\pi/\omega_0=2\pi/(\pi/2)=4$"],
            "4초마다 제자리로 오는 [[주기 신호|예요/이에요]]. 이 도는 점이 [[복소 지수 신호|예요/이에요]]."),
        fig("도는 점의 그림자가 사인파 (S2 p.29)", fig_w6_shadow(),
            r"도는 점 $e^{j\omega t}$ 의 세로 위치를 시간 순서로 펴면 $\sin\omega t$, 가로 위치는 $\cos\omega t$ 예요."),
        fml("거꾸로: cos 을 $e$ 두 개로 (S2 p.34)", r"\cos\theta = \frac{e^{j\theta}+e^{-j\theta}}{2}",
            [(r"e^{j\theta}", r"시계 반대로 $\theta$ 돈 점"),
             (r"e^{-j\theta}", r"시계 방향으로 $\theta$ 돈 점. 앞 점의 [[켤레 복소수]]"),
             (r"\frac{\cdots}{2}", "둘을 더하면 세로(허수)가 상쇄. 반으로 나눠요")],
            "코사인 세타는 이의 제이 세타 더하기 이의 마이너스 제이 세타, 나누기 2. sin 은 빼고 $2j$ 로 나눠요."),
        stp(r"손계산 5: $\theta=\pi/3$ 으로 확인", r"$e^{\pm j\pi/3}=0.5\pm j0.866$",
            [r"$e^{j\pi/3}=0.5+j0.866$",
             r"$e^{-j\pi/3}=0.5-j0.866$",
             "더하면 허수부 $0.866-0.866=0$. 합은 $1$",
             r"$1\div 2=0.5$. 그리고 $\cos(\pi/3)=0.5$. 맞아요!"],
            "서로 반대로 도는 두 점을 더하면 가로 성분만 남아요. 그게 cos 이에요."),
        fig("반대로 도는 두 점의 합", fig_w6_sum(),
            r"$e^{j\theta}$ 와 $e^{-j\theta}$ 는 가로축 거울상이라 세로가 상쇄돼요."),
        fig(r"$e^{(\sigma+j\omega)t}$: 줄면서 돌기 (S3 p.3)", fig_w6_spiral(),
            r"앞쪽 $e^{\sigma t}$ 는 크기([[지수함수]]), 뒤쪽 $e^{j\omega t}$ 는 회전이에요. $\sigma<0$ 이면 안으로 말려요."),
        chk(r"$e^{j3\pi/2}$ 의 값은?", ["$-j$", "$j$", "$-1$", "$1$"], 0,
            r"$3\pi/2$ 는 $3/4$ 바퀴, [[단위원]]의 맨 아래예요. $\cos=0$, $\sin=-1$ 이라 $-j$."),
        chk(r"$e^{j\theta}=\cos\theta+j\sin\theta$ 를 뭐라고 하나요?",
            ["[[오일러 공식]]", "[[테일러 급수]]", "[[주기 신호]]", "[[복소평면]]"], 0,
            "[[오일러 공식|이에요/예요]]. S2 p.24 는 이것을 [[테일러 급수]]로 보이지만, 증명은 외우지 않아도 돼요."),
        warn("헷갈리기 쉬운 점",
             r"$e^{j\theta}$ 의 크기는 $\theta$ 가 뭐든 늘 1이에요. 커지거나 줄지 않고 돌기만 해요.",
             r"$e^{-j\theta}$ 는 반대 방향으로 돈 점이지 음수가 아니에요.",
             "S2 p.23, p.24 는 허수 단위를 $i$ 로 적었어요. 수업 표기 $j$ 와 같은 것이에요."),
        where(r"S2 p.23: [[오일러 공식]] $e^{j\omega_0 t}=\cos\omega_0 t+j\sin\omega_0 t$, 주기 $T=2\pi/\omega_0$",
              r"S2 p.24: [[테일러 급수]]로 본 유도(외울 필요 없음). p.25, 26: $e^{j\pi/2}=j$, [[단위원]]",
              r"S2 p.29: 도는 점과 사인파. p.34: $\cos\theta=(e^{j\theta}+e^{-j\theta})/2$, Example 1.5",
              r"S3 p.3: $e^{(\sigma+j\omega)t}=e^{\sigma t}e^{j\omega t}$, 성장/감쇠 곱하기 회전",
              r"시험 모양: [[오일러 공식]] 쓰기, $e^{j\pi}$ 같은 값, [[복소 지수 신호]]의 주기 구하기."),
        recap(r"[[오일러 공식]] $e^{j\theta}=\cos\theta+j\sin\theta$. 무조건 외워요.",
              r"$e^{j\theta}$ 는 [[단위원]] 위 각도 $\theta$ 인 점. $e^{j\pi/2}=j$, $e^{j\pi}=-1$.",
              r"$e^{j\theta}$ 를 곱하면 $\theta$ 만큼 회전. 크기는 곱하고 각도는 더해요.",
              r"$\cos\theta=(e^{j\theta}+e^{-j\theta})/2$. $e^{j\omega_0 t}$ 는 주기 $2\pi/\omega_0$ 인 [[주기 신호|예요/이에요]]."),
    ]))


# ================================================================ wb-7 시그마로 더하기
assert sum(range(1, 5)) == 10 and sum(2 * k for k in range(4)) == 12
assert sum(k * k for k in range(1, 4)) == 14
assert sum(XN.values()) == 4 and sum(v * v for v in XN.values()) == 6
ACC = {n: sum(xn(k) for k in range(-5, n + 1)) for n in range(-1, 5)}
assert ACC == {-1: 0, 0: 1, 1: 3, 2: 4, 3: 4, 4: 4}
GS = [sum(0.5 ** k for k in range(m + 1)) for m in range(5)]
assert GS == [1, 1.5, 1.75, 1.875, 1.9375]
assert (1 - 0.5 ** 4) / (1 - 0.5) == 1.875 and 0.5 ** 4 == 0.0625
assert 1 / (1 - 0.5) == 2
assert abs(sum(0.5 ** k for k in range(60)) - 2) < 1e-12


def fig_w7_expand():
    els = [T(240, 40, "∑ (k = 1 부터 4 까지) k", "tb", 0, 17)]
    for i, k in enumerate(range(1, 5)):
        x = 70 + 100 * i
        els.append(R(x - 32, 80, 64, 50, "box2" if i == 0 else "box", 1 + (i > 0)))
        els.append(T(x, 101, "k = %d" % k, "tm", 1 + (i > 0), 14))
        els.append(T(x, 122, str(k), "tb", 1 + (i > 0), 18))
        if i < 3:
            els.append(T(x + 50, 112, "+", "tb", 2, 18))
    els.append(A(240, 140, 240, 185, "e2", 3))
    els.append(T(240, 215, "1 + 2 + 3 + 4 = 10", "tb", 3, 18))
    els.append(T(240, 255, "k 를 1 씩 늘리며 값을 하나씩 꺼내 더해요", "tm", 3, 14))
    return els


def fig_w7_acc():
    p1 = Plot(-1.6, 4.6, 0, 4.6, 30, 45, 190, 170)
    p2 = Plot(-1.6, 4.6, 0, 4.6, 260, 45, 190, 170)
    ns = list(range(-1, 5))
    els = p1.axes("n", "x[n]", xt=[1, 2, 3, 4], yt=[1, 2, 4])
    els += p1.stems(ns, [xn(n) for n in ns], "n2", 1)
    els += p2.axes("n", "y[n] 누적", xt=[1, 2, 3, 4], yt=[1, 3, 4], b=2)
    els += p2.stems(ns, [ACC[n] for n in ns], "n2", 2)
    els.append(T(240, 262, "y[n] = 처음부터 n 번째 칸까지 x 를 모두 더한 값", "tm", 2, 14))
    return els


def fig_w7_geo():
    p = Plot(-0.5, 5.5, 0, 2.3, 60, 35, 360, 195)
    els = p.axes("", "", xt=[0, 1, 2, 3, 4], yt=[], xtl=["1개", "2개", "3개", "4개", "5개"], yaxis=False)
    els.append(L(p.X - 4, p.py(0), p.X - 4, p.Y - 5))
    els.append(T(p.X - 10, p.py(1) + 5, "1", "tm", 0, 14, "end"))
    els.append(T(p.X - 10, p.py(2) + 5, "2", "tm", 0, 14, "end"))
    for m, v in enumerate(GS):
        els.append(R(p.px(m) - 16, p.py(v), 32, p.py(0) - p.py(v), "n", 1))
        els.append(T(p.px(m), p.py(v) + 20, fmtn(v), "tb", 1, 14))
    els.append(L(p.X, p.py(2), p.X + p.Wd, p.py(2), "e2", 2))
    els.append(T(p.X + 4, p.py(2) - 8, "끝없이 더하면 2", "tb", 2, 14, "start"))
    return els


UNITS.append(unit(
    "wb-7", "시그마로 더하기",
    "시그마 기호를 항 하나하나로 풀어 쓰고, 누산기, 신호 에너지, 등비급수 합을 손으로 계산할 수 있어요.",
    ["시그마 기호", "등비급수", "누산기", "신호 에너지"],
    ["이산시간 신호", "지수함수", "신호"],
    [
        title("시그마로 더하기", "긴 덧셈을 한 글자로 줄여 써요"),
        goal("[[시그마 기호]]를 'k 가 1부터 4까지' 처럼 읽고 항마다 풀어 써요.",
             "[[누산기|와/과]] [[신호 에너지]] 같은 합을 손으로 계산해요.",
             r"[[등비급수]] 공식을 $\alpha=0.5$ 로 직접 확인해요."),
        fml("[[시그마 기호]] 읽기", r"\sum_{k=1}^{4} k",
            [(r"\sum", "'시그마'. 그리스 글자 S, 모두 더하라는 뜻"),
             ("k=1", "아래: $k$ 를 1부터 시작"),
             ("4", "위: 4까지(4도 포함)"),
             ("k", "오른쪽: 매번 더할 것")],
            "시그마, 케이는 일부터 사까지, 케이. 즉 $1+2+3+4$ 예요."),
        fig("풀어 쓰면 보통 덧셈", fig_w7_expand(),
            "[[시그마 기호|은/는]] $k$ 에 1, 2, 3, 4를 차례로 넣은 값을 모두 더하라는 약속이에요."),
        stp("손계산 1: 풀어 쓰고 더하기", "두 개를 풀어요",
            [r"$\sum_{k=1}^{4}k=1+2+3+4=10$",
             r"$\sum_{k=0}^{3}2k$: $k=0,1,2,3$ 을 넣으면 $0+2+4+6$",
             "$0+2+4+6=12$",
             "$k=0$ 부터 $3$ 까지는 항이 4개예요. 시작 칸도 세요."],
            "$10$ 과 $12$. 풀어 쓰기만 하면 [[시그마 기호|은/는]] 무섭지 않아요."),
        pts("$k$ 는 이름표일 뿐이에요",
            r"$\sum_{k=1}^{4}k$ 와 $\sum_{m=1}^{4}m$ 은 같은 값 10이에요.",
            "$k$, $m$ 은 '지금 몇 번째' 를 가리키는 이름표예요.",
            "[[이산시간 신호]] $x[k]$ 를 더할 때도 $k$ 는 칸 번호 이름표예요.",
            "S3 의 컨볼루션 식에서 $k$ 로 더하고 $n$ 은 고정인 것도 같은 이야기예요."),
        ana("통장 잔고 = 처음부터 지금까지의 합",
            "통장 잔고는 지난 입금이 쌓인 값이에요. 매달 입금액을 적은 기록표가 있으면, 이번 달 잔고는 처음부터 이번 달까지의 입금을 모두 더한 값이에요.",
            ["매달 입금액 기록표", "입력 [[신호]] $x[k]$"],
            ["처음부터 이번 달까지 모두 더하기", r"$\sum_{k=-\infty}^{n}x[k]$"],
            ["이번 달 잔고", "[[누산기]]의 출력 $y[n]$"]),
        stp("손계산 2: [[누산기]] (S2 p.70)", r"$x[n]$ 은 $n=0,1,2$ 에서 $1,2,1$. $y[n]=\sum_{k=-\infty}^{n}x[k]$",
            [r"$-\infty$ 는 '마이너스 무한대', 즉 맨 처음부터라는 뜻. 0번 칸 전은 모두 0이에요.",
             "$y[-1]=0$, $y[0]=1$",
             "$y[1]=1+2=3$",
             "$y[2]=1+2+1=4$, $y[3]=4$ (더할 새 값이 없어요)"],
            r"$y=0,1,3,4,4,\dots$ 잔고처럼 쌓이고, 입금이 끝나면 그대로 남아요."),
        fig("[[누산기]]의 입력과 출력", fig_w7_acc(),
            "왼쪽 입력을 처음부터 쌓아 더한 것이 오른쪽 출력이에요."),
        stp("손계산 3: [[신호 에너지]] (S2 p.6)", r"$E=\sum_{n}|x[n]|^2$, $x=[1,2,1]$",
            ["$|x[n]|^2$ 는 값의 크기를 제곱한 것",
             "$n=0$: $1^2=1$, $n=1$: $2^2=4$, $n=2$: $1^2=1$",
             "나머지 칸은 0이라 더해도 그대로",
             "$E=1+4+1=6$"],
            "[[신호 에너지|은/는]] $6$. [[시그마 기호]]로 칸마다 제곱해서 더했어요."),
        chk(r"$\sum_{k=1}^{3}k^2$ 의 값은?", ["$14$", "$6$", "$9$", "$36$"], 0,
            "$1+4+9=14$ 예요. 먼저 제곱하고 그다음 더해요."),
        fml("[[등비급수]]: 같은 비율로 곱해지는 수들의 합", r"\sum_{k=0}^{n}\alpha^{k} = \frac{1-\alpha^{n+1}}{1-\alpha}",
            [(r"\alpha^{k}", r"$1, \alpha, \alpha^2, \dots$ 같은 비율 $\alpha$ 로 곱해지는 항"),
             (r"\sum_{k=0}^{n}", "$k=0$ 부터 $n$ 까지, 항 $n+1$ 개"),
             (r"\frac{1-\alpha^{n+1}}{1-\alpha}", r"하나하나 더하지 않고 한 번에 구하는 공식 ($\alpha\neq 1$)")],
            r"4단원 [[지수함수]]의 이산 버전 $\alpha^n$ 을 차례로 더한 것이에요. S3 p.30 Example 2.3 에 그대로 나와요."),
        stp(r"손계산 4: $\alpha=0.5$, $n=3$ 으로 확인", "직접 더하기와 공식을 비교해요",
            ["직접: $1+0.5+0.25+0.125=1.875$",
             r"공식: $\alpha^{n+1}=0.5^4=0.0625$",
             "$(1-0.0625)/(1-0.5)=0.9375/0.5=1.875$",
             "두 값이 같아요."],
            "$1.875$. [[등비급수]] 공식이 맞는 걸 손으로 확인했어요."),
        stp("손계산 5: 공식은 왜 맞을까", r"$S=1+\alpha+\alpha^2+\alpha^3$",
            [r"양쪽에 $\alpha$ 를 곱해요: $\alpha S=\alpha+\alpha^2+\alpha^3+\alpha^4$",
             r"$S-\alpha S$: 가운데 항들이 모두 지워져요",
             r"남는 것: $S-\alpha S=1-\alpha^4$",
             r"$S(1-\alpha)=1-\alpha^4$ 이니까 $S=(1-\alpha^4)/(1-\alpha)$"],
            "밀어서 빼면 거의 다 지워진다는 요령이에요. $n$ 이 달라도 똑같아요."),
        fig("끝없이 더해도 2를 넘지 않아요", fig_w7_geo(),
            r"$1, 1.5, 1.75, 1.875, 1.9375, \dots$ 로 2에 다가가요. $|\alpha|<1$ 이면 $\alpha^{n+1}$ 이 0으로 줄기 때문이에요."),
        chk(r"$\sum_{k=0}^{\infty}0.5^k$ 의 값은?", ["$2$", "$1$", r"$\infty$", "$0.5$"], 0,
            r"$1/(1-\alpha)=1/(1-0.5)=2$. S3 p.31 그림의 점선 높이 $1/(1-\alpha)$ 가 바로 이 값이에요."),
        chk(r"여러 항을 차례로 더하라는 기호 $\sum$ 는?", ["[[시그마 기호]]", "[[등비급수]]", "[[누산기]]", "[[신호 에너지]]"], 0,
            "[[시그마 기호|예요/이에요]]. [[등비급수|은/는]] 그 기호로 적는 특별한 합의 이름이에요."),
        warn("헷갈리기 쉬운 점",
             r"위아래 숫자도 포함해요. $\sum_{k=0}^{3}$ 은 항이 3개가 아니라 4개예요.",
             r"무한 [[등비급수]] $1/(1-\alpha)$ 는 $|\alpha|<1$ 일 때만 써요. $\alpha=2$ 면 끝없이 커져요.",
             "$|x[n]|^2$ 는 더하기 전에 칸마다 제곱해요. 다 더한 뒤 제곱하면 틀려요."),
        where(r"S2 p.6: [[신호 에너지]] $E=\sum_{n=n_1}^{n_2}|x[n]|^2$",
              r"S2 p.47: $u[n]=\sum_{m=-\infty}^{n}\delta[m]$. S2 p.70: [[누산기]] $y[n]=\sum_{k\le n}x[k]$",
              r"S3 p.14: $x[n]=\sum_k x[k]\delta[n-k]$. S3 p.22: 컨볼루션 합 $\sum_k x[k]h[n-k]$",
              r"S3 p.30, p.31 Example 2.3: $\sum_{k=0}^{n}\alpha^k=(1-\alpha^{n+1})/(1-\alpha)$, 끝 높이 $1/(1-\alpha)$",
              "S3 p.64 Example 2.12: $h[n]=u[n]$ 이면 [[누산기]]. 시험에서 이 합들을 손으로 계산해요."),
        recap("[[시그마 기호]]는 아래 시작부터 위 끝까지 넣어서 모두 더하기예요.",
              "[[누산기]]: 처음부터 지금까지의 합. $x=[1,2,1]$ 이면 $1,3,4,4$.",
              "[[신호 에너지]]: 칸마다 제곱해서 더하기. $x=[1,2,1]$ 이면 $6$.",
              r"[[등비급수]]: $\sum_{k=0}^{n}\alpha^k=\frac{1-\alpha^{n+1}}{1-\alpha}$, 끝없이 더하면 $\frac{1}{1-\alpha}$."),
    ]))


# ================================================================ wb-8 적분은 넓이, 미분은 기울기
def riemann(f, a, bb, n):
    d = (bb - a) / n
    return sum(f(a + i * d) for i in range(n)) * d


def integ(f, a, bb, n=20000):
    d = (bb - a) / n
    return sum(f(a + (i + 0.5) * d) for i in range(n)) * d


assert 3 * 2 == 6 and abs(integ(lambda t: 3, 0, 2) - 6) < 1e-9
assert abs(integ(lambda t: t, 0, 2) - 2) < 1e-9 and 0.5 * 2 * 2 == 2
assert riemann(lambda t: t, 0, 2, 4) == 1.5 and riemann(lambda t: t, 0, 2, 8) == 1.75
assert abs(integ(math.sin, 0, 2 * math.pi)) < 1e-9
for Tt, want in [(1, 0.632), (2, 0.865)]:
    assert round(1 - math.exp(-Tt), 3) == want and abs(integ(lambda t: math.exp(-t), 0, Tt) - (1 - math.exp(-Tt))) < 1e-8
assert 2 * 3 == 6
assert ((2 * 3 + 1) - (2 * 1 + 1)) / (3 - 1) == 2
assert round((1.01 ** 2 - 1) / 0.01, 2) == 2.01
assert (5 * 3 - 2 - (5 * 1 - 2)) / 2 == 5


def xj(t):
    """S2 p.54 의 계단 신호: 1 전 0, 1~2 에서 2, 2~4 에서 -1, 4 뒤 1."""
    if t < 1:
        return 0
    if t < 2:
        return 2
    if t < 4:
        return -1
    return 1


JUMPS = {t0: xj(t0 + 1e-9) - xj(t0 - 1e-9) for t0 in (1, 2, 4)}
assert JUMPS == {1: 2, 2: -3, 4: 2}


def fig_w8_rect():
    p = Plot(-0.5, 3.2, 0, 4, 50, 35, 300, 190)
    els = p.axes("t", "x(t)", xt=[1, 2, 3], yt=[])
    els.append(p.line([(-0.5, 3), (3.2, 3)], "e2", 1))
    els.append(R(p.px(0), p.py(3), p.px(2) - p.px(0), p.py(0) - p.py(3), "n3", 2, 0))
    els.append(T(p.px(1), p.py(1.5) + 5, "넓이 6", "tb", 2, 18))
    els.append(T(p.px(1), p.py(3) - 10, "높이 3", "t", 2, 14))
    els.append(T(415, 110, "∫ (0~2) 3 dt", "tb", 3, 15))
    els.append(T(415, 135, "= 3 × 2", "tb", 3, 15))
    els.append(T(415, 160, "= 6", "tb", 3, 15))
    return els


def fig_w8_tri():
    p = Plot(-0.3, 2.5, 0, 2.5, 50, 35, 270, 190)
    els = p.axes("t", "", xt=[1, 2], yt=[1, 2])
    els.append(p.line([(-0.3, -0.0), (0, 0), (2.4, 2.4)], "e2", 1))
    els.append(T(p.px(2.4) - 6, p.py(2.4) + 4, "x(t) = t", "tb", 1, 14, "end"))
    for i in range(4):
        a = 0.5 * i
        els.append(R(p.px(a), p.py(a), p.px(a + 0.5) - p.px(a), p.py(0) - p.py(a), "n", 2, 0))
    els.append(PG([(p.px(0), p.py(0)), (p.px(2), p.py(2)), (p.px(2), p.py(0))], "n3", 3))
    els.append(T(398, 90, "얇은 사각형 합", "t", 2, 14))
    els.append(T(398, 112, "폭 0.5: 1.5", "t", 2, 14))
    els.append(T(398, 134, "폭 0.25: 1.75", "t", 2, 14))
    els.append(T(398, 170, "삼각형 넓이", "tb", 3, 15))
    els.append(T(398, 194, "½ × 2 × 2 = 2", "tb", 3, 15))
    return els


def fig_w8_exp():
    p = Plot(-0.2, 3.3, 0, 1.2, 50, 35, 270, 190)
    els = p.axes("t", "e^-t", xt=[1, 2, 3], yt=[1])
    area = [(p.px(0), p.py(0))] + [(p.px(2 * i / 60), p.py(math.exp(-2 * i / 60))) for i in range(61)] + [(p.px(2), p.py(0))]
    els.append(PG(area, "n3", 2))
    els.append(p.curve(lambda t: math.exp(-t), 0, 3.3, "e2", 1))
    els.append(T(p.px(0.75), p.py(0.25), "0.865", "tb", 2, 16))
    els.append(T(400, 90, "0 부터 T 까지 넓이", "t", 3, 14))
    els.append(T(400, 115, "= 1 - e^(-T)", "tb", 3, 15))
    els.append(T(400, 150, "T = 2: 0.865", "t", 3, 14))
    els.append(T(400, 175, "T 가 커지면 1", "t", 3, 14))
    return els


def fig_w8_slope():
    p = Plot(-0.3, 4, 0, 9.5, 60, 30, 300, 200)
    els = p.axes("t", "x(t)", xt=[1, 3], yt=[3, 7])
    els.append(p.line([(-0.3, 0.4), (4, 9)], "e2", 1))
    els.append(p.dot(1, 3, "n2", 1))
    els.append(p.dot(3, 7, "n2", 1))
    els.append(L(p.px(1), p.py(3), p.px(3), p.py(3), "e", 2))
    els.append(L(p.px(3), p.py(3), p.px(3), p.py(7), "e", 2))
    els.append(T(p.px(2), p.py(3) + 20, "옆으로 2", "tb", 2, 14))
    els.append(T(p.px(3) + 8, p.py(5), "위로 4", "tb", 2, 14, "start"))
    els.append(T(420, 110, "x(t) = 2t + 1", "t", 3, 15))
    els.append(T(420, 140, "기울기 = 4 ÷ 2", "tb", 3, 15))
    els.append(T(420, 165, "= 2", "tb", 3, 15))
    return els


def fig_w8_jump():
    p1 = Plot(-0.3, 5.2, -1.6, 2.6, 30, 40, 190, 170)
    p2 = Plot(-0.3, 5.2, -3.6, 2.6, 260, 40, 190, 170)
    els = p1.axes("t", "x(t)", xt=[1, 2, 4], yt=[2, -1])
    seg = [(-0.3, 0), (1, 0), (1, 2), (2, 2), (2, -1), (4, -1), (4, 1), (5.2, 1)]
    els.append(p1.line(seg, "e2", 1))
    els += p2.axes("t", "", xt=[1, 4], yt=[2, -3], b=2)
    for t0, v in JUMPS.items():
        els.append(A(p2.px(t0), p2.py(0), p2.px(t0), p2.py(v), "e2", 2, 8))
        els.append(T(p2.px(t0) + 8, p2.py(v) + (12 if v > 0 else -2), "%+d" % v, "tb", 2, 14, "start"))
    els.append(T(p2.px(2) - 6, p2.py(0) - 8, "2", "tm", 2, 14, "end"))
    els.append(T(240, 262, "평평하면 기울기 0, 뛰는 곳마다 뛴 높이만큼의 톡(임펄스)", "tm", 2, 14))
    return els


UNITS.append(unit(
    "wb-8", "적분은 넓이, 미분은 기울기",
    "적분을 그래프 아래 넓이로, 미분을 기울기로 읽고, 사각형, 삼각형 넓이와 기울기를 손으로 계산할 수 있어요.",
    ["적분", "미분", "적분기", "미분방정식"],
    ["시그마 기호", "누산기", "지수함수", "연속시간 신호"],
    [
        title("적분은 넓이, 미분은 기울기", "미적분을 몰라도 그림으로 읽을 수 있어요"),
        goal(r"[[적분]] 기호 $\int$ 를 '어디부터 어디까지의 넓이' 로 읽어요.",
             "사각형, 삼각형 넓이로 [[적분|을/를]] 손계산해요.",
             "[[미분|은/는]] 기울기, 계단의 [[미분|은/는]] 톡(임펄스)이라는 느낌을 잡아요."),
        pts(r"$\sum$ 의 연속 버전이 $\int$ 예요",
            "앞 단원 [[시그마 기호|은/는]] 정수 칸마다 값을 더했어요.",
            "[[연속시간 신호|은/는]] 칸이 없고 끊김 없이 이어져요.",
            "그래서 아주 얇게 잘라 모두 더하는 [[적분|을/를]] 써요. 결과는 그래프 아래 넓이예요.",
            r"$\int$ 는 합(Sum)의 S 를 길게 늘인 모양이에요. '인테그랄' 이라고 읽어요."),
        fml("[[적분]] 읽기", r"\int_{0}^{2} 3\,dt",
            [(r"\int", "'인테그랄'. 얇게 잘라 모두 더해라"),
             ("0", "아래: 시작 시각 0"),
             ("2", "위: 끝 시각 2"),
             ("3", "그때그때의 높이, $x(t)=3$"),
             ("dt", "아주 얇은 폭. '디 티'")],
            "인테그랄 영부터 이까지 삼 디티. 높이 3인 그래프 아래, $t=0$ 부터 $2$ 까지의 넓이예요."),
        stp("손계산 1: 사각형 넓이", r"$\int_0^2 3\,dt$",
            ["그래프 $x(t)=3$ 은 높이 3인 가로줄이에요.",
             "$0$ 부터 $2$ 까지 자르면 가로 2, 세로 3인 사각형.",
             r"넓이 $=$ 가로 $\times$ 세로 $=2\times 3=6$"],
            r"$\int_0^2 3\,dt=6$ 이에요."),
        fig("[[적분|은/는]] 넓이", fig_w8_rect(),
            "높이 3, 폭 2인 사각형 넓이가 곧 [[적분]] 값 6이에요."),
        stp("손계산 2: 삼각형 넓이", r"$\int_0^2 t\,dt$",
            ["$x(t)=t$ 는 $(0,0)$ 에서 $(2,2)$ 로 올라가는 직선이에요.",
             "그 아래는 밑변 2, 높이 2인 삼각형.",
             r"삼각형 넓이 $=\frac12\times 2\times 2=2$",
             "얇은 사각형으로 어림: 폭 $0.5$ 면 $1.5$, 폭 $0.25$ 면 $1.75$. 얇을수록 2에 다가가요."],
            r"$\int_0^2 t\,dt=2$. 얇게 자를수록 정확해지는 것이 [[적분]]의 아이디어예요."),
        fig("얇은 사각형을 모으면 넓이", fig_w8_tri(),
            r"S3 p.36, p.37 도 같은 생각이에요. 폭 $\Delta$ 를 0으로 줄이면 합이 [[적분|이/가]] 돼요."),
        pts("가로축 아래는 빼요",
            "그래프가 가로축 아래로 가면 그 넓이는 음수로 쳐요.",
            r"예: $\sin t$ 를 $0$ 부터 $2\pi$ 까지 [[적분|하면/하면]] 위 넓이와 아래 넓이가 같아서 0이에요.",
            "그래서 [[적분|은/는]] '넓이의 합' 이라기보다 '위는 더하고 아래는 뺀 합' 이에요."),
        stp("손계산 3: $e^{-t}$ 아래 넓이 (알려진 결과 쓰기)", r"공식 $\int_0^T e^{-t}\,dt=1-e^{-T}$ 를 그대로 써요",
            ["이 공식은 증명 없이 결과만 가져와요. 4단원 $e^{-t}$ 표를 써요.",
             r"$T=1$: $1-e^{-1}\approx 1-0.368=0.632$",
             r"$T=2$: $1-e^{-2}\approx 1-0.135=0.865$",
             r"$T$ 가 아주 크면 $e^{-T}\to 0$ 이라서 넓이는 1에 다가가요."],
            "넓이는 $0.632$, $0.865$, 그리고 끝없이 가면 $1$. 줄어드는 [[지수함수]] 아래 넓이는 유한해요."),
        fig("줄어드는 곡선 아래 넓이", fig_w8_exp(),
            r"S3 p.46 Example 2.6 의 $\frac{1}{a}(1-e^{-at})$ 에서 $a=1$ 인 경우와 같은 모양이에요."),
        ana("통장 잔고와 [[적분기]]",
            "통장 잔고는 지난 입금이 모두 쌓인 값이에요. 입금이 끊김 없이 흘러 들어온다면, 잔고는 처음부터 지금까지 들어온 양의 넓이예요.",
            ["끊김 없이 흘러 들어오는 입금", "입력 $x(t)$"],
            ["지금까지 쌓인 잔고", r"$y(t)=\int_{-\infty}^{t}x(\tau)\,d\tau$"],
            ["잔고를 계산해 주는 기계", "[[적분기]], [[누산기]]의 연속 버전"]),
        stp("손계산 4: [[적분기]]에 높이 1을 계속 넣으면", "$t=0$ 부터 높이 1인 입력이 계속 들어와요",
            [r"$t=1$: 넓이 $1\times 1=1$",
             r"$t=2$: 넓이 $1\times 2=2$",
             "$t=10$: 넓이 $10$",
             "$t$ 가 커지는 만큼 출력도 끝없이 커져요."],
            "유한한 입력인데 출력이 끝없이 커져요. S3 p.70 Example 2.13: [[적분기|은/는]] 불안정해요."),
        stp("손계산 5: [[미분|은/는]] 기울기", "$x(t)=2t+1$",
            ["$t=1$ 에서 $x=3$, $t=3$ 에서 $x=7$",
             "옆으로 $3-1=2$ 가는 동안 위로 $7-3=4$",
             r"기울기 $=4\div 2=2$",
             r"곡선 $t^2$ 도 아주 가까이서 보면 직선: $(1.01^2-1)/0.01=2.01\approx 2$"],
            "[[미분|은/는]] 어느 순간의 변화 속도, 기울기예요. $2t+1$ 은 어디서나 2예요."),
        fig("기울기 = 위로 간 양 ÷ 옆으로 간 양", fig_w8_slope(),
            "가파를수록 [[미분]] 값이 커요. 평평하면 0, 내려가면 음수예요."),
        stp("손계산 6: 뛰는 곳의 [[미분]] (S2 p.54)", "$t<1$ 에서 $0$, $1<t<2$ 에서 $2$, $2<t<4$ 에서 $-1$, $t>4$ 에서 $1$",
            ["평평한 곳은 기울기 0이에요.",
             "$t=1$: 0에서 2로 순식간에 뛰어요. 뛴 높이 $+2$",
             "$t=2$: 2에서 $-1$ 로. 뛴 높이 $-3$",
             "$t=4$: $-1$ 에서 1로. 뛴 높이 $+2$"],
            "눈 깜짝할 사이(시간 0초)에 뛰었으니 기울기는 무한대. 그래서 뛴 높이만큼의 '톡'(임펄스) $2, -3, 2$ 가 생겨요."),
        fig("뛰는 곳의 [[미분|은/는]] 톡", fig_w8_jump(),
            "왼쪽 $x(t)$ 를 [[미분|하면/하면]] 오른쪽처럼 뛴 곳에만 화살표가 서요. S2 p.54 그림과 같아요."),
        chk(r"$\int_0^3 2\,dt$ 의 값은?", ["$6$", "$5$", "$2$", "$3$"], 0,
            r"높이 2, 폭 3인 사각형 넓이 $2\times 3=6$ 이에요."),
        chk("어느 순간의 변화 속도, 즉 기울기를 뜻하는 말은?", ["[[미분]]", "[[적분]]", "[[적분기]]", "[[시그마 기호]]"], 0,
            "[[미분|은/는]] 기울기, [[적분|은/는]] 넓이예요. $x(t)=5t-2$ 의 [[미분|은/는]] 어디서나 5예요."),
        pts("[[미분방정식]] 한 줄 소개",
            "변화율([[미분]])이 들어 있는 방정식이 [[미분방정식|이에요/예요]].",
            "S2 p.58: RC 회로의 축전기 전압은 1차 선형 [[미분방정식|으로/로]] 적혀요.",
            "S3 p.4, p.5 에서 푸는 법을 복습했지만, 교수님은 '퀴즈나 시험에 내지는 않는다' 고 했어요."),
        where(r"S2 p.5, 6: 연속 [[신호]]의 에너지 $E=\int_{t_1}^{t_2}|x(t)|^2dt$",
              r"S2 p.51, 52: $u(t)=\int_{-\infty}^{t}\delta(\tau)d\tau$, $\delta(t)=du(t)/dt$. p.54: 뛰는 곳마다 임펄스",
              r"S3 p.37: $x(t)=\int x(\tau)\delta(t-\tau)d\tau$. p.40: 컨볼루션 [[적분]]",
              r"S3 p.46 Example 2.6: $\int_0^t e^{-a\tau}d\tau=\frac1a(1-e^{-at})$. p.70: [[적분기]] 불안정",
              "S2 p.58, S3 p.4: [[미분방정식]] (시험 출제는 안 한다고 함)"),
        recap(r"[[적분|은/는]] 그래프 아래 넓이. $\int_0^2 3\,dt=6$, $\int_0^2 t\,dt=2$.",
              r"가로축 아래 넓이는 빼요. $\int_0^T e^{-t}dt=1-e^{-T}$ 는 결과만 써요.",
              "[[미분|은/는]] 기울기. 평평하면 0, 뛰는 곳은 뛴 높이만큼의 톡.",
              "[[적분기|은/는]] 처음부터 지금까지의 넓이를 내보내요. 높이 1을 계속 넣으면 끝없이 커져요."),
    ]))


# ================================================================ wb-9 단위 계단과 단위 임펄스
def dlt(n):
    return 1 if n == 0 else 0


def stp_u(n):
    return 1 if n >= 0 else 0


NS = list(range(-2, 4))
assert [dlt(n) for n in NS] == [0, 0, 1, 0, 0, 0]
assert [stp_u(n) for n in NS] == [0, 0, 1, 1, 1, 1]
assert [dlt(n - 2) for n in NS] == [0, 0, 0, 0, 1, 0]
assert [stp_u(n - 1) for n in NS] == [0, 0, 0, 1, 1, 1]
for n in range(-5, 6):
    assert dlt(n) == stp_u(n) - stp_u(n - 1)
    assert stp_u(n) == sum(dlt(m) for m in range(-10, n + 1))
    assert stp_u(n) == sum(dlt(n - k) for k in range(0, 20))
# x[n] delta[n-1] = x[1] delta[n-1], 선별
SAM = [xn(n) * dlt(n - 1) for n in range(-1, 4)]
assert SAM == [0, 0, 2, 0, 0] and sum(xn(n) * dlt(n - 1) for n in range(-5, 6)) == xn(1) == 2
for n in range(-3, 6):
    assert xn(n) == 1 * dlt(n) + 2 * dlt(n - 1) + 1 * dlt(n - 2)
# 연속: 폭 D, 높이 1/D 인 펄스의 넓이는 늘 1
for D in (1, 0.5, 0.25, 0.1):
    assert abs(D * (1 / D) - 1) < 1e-12
assert 1 / 0.5 == 2 and 1 / 0.25 == 4 and round(1 / 0.1) == 10


def fig_w9_two():
    p1 = Plot(-2.6, 3.6, 0, 1.5, 30, 50, 190, 150)
    p2 = Plot(-2.6, 3.6, 0, 1.5, 260, 50, 190, 150)
    ns = list(range(-2, 4))
    els = p1.axes("n", "δ[n]", xt=[-2, -1, 1, 2, 3], yt=[1])
    els += p1.stems(ns, [dlt(n) for n in ns], "n2", 1)
    els += p2.axes("n", "u[n]", xt=[-2, -1, 1, 2, 3], yt=[1], b=2)
    els += p2.stems(ns, [stp_u(n) for n in ns], "n2", 2)
    els.append(T(p2.px(3.6) - 4, p2.py(1) - 12, "…", "tb", 2, 16, "end"))
    els.append(T(125, 250, "손뼉 한 번", "tb", 1, 15))
    els.append(T(355, 250, "스위치 켜고 계속", "tb", 2, 15))
    return els


def fig_w9_diff():
    ps = [Plot(-2.6, 3.6, 0, 1.4, 150, 20 + 88 * i, 300, 55) for i in range(3)]
    ns = list(range(-2, 4))
    rows = [("u[n]", [stp_u(n) for n in ns]), ("u[n-1]", [stp_u(n - 1) for n in ns]),
            ("빼면 δ[n]", [dlt(n) for n in ns])]
    els = []
    for i, (lab, vals) in enumerate(rows):
        p = ps[i]
        els.append(L(p.X, p.py(0), p.X + p.Wd, p.py(0), "e", i + 1))
        els.append(T(20, p.py(0) - 10, lab, "tb", i + 1, 15, "start"))
        els += p.stems(ns, vals, "n2", i + 1)
        if i == 2:
            els.append(T(p.px(0), p.py(0) + 18, "0", "tm", 3, 14))
    return els


def fig_w9_decomp():
    ps = [Plot(-1.6, 3.6, 0, 2.4, 170, 10 + 68 * i, 280, 48) for i in range(4)]
    ns = list(range(-1, 4))
    rows = [("1 δ[n]", [dlt(n) for n in ns]), ("2 δ[n-1]", [2 * dlt(n - 1) for n in ns]),
            ("1 δ[n-2]", [dlt(n - 2) for n in ns]), ("합 = x[n]", [xn(n) for n in ns])]
    els = []
    for i, (lab, vals) in enumerate(rows):
        p = ps[i]
        els.append(L(p.X, p.py(0), p.X + p.Wd, p.py(0), "e", min(i + 1, 4)))
        els.append(T(20, p.py(0) - 8, lab, "tb", min(i + 1, 4), 15, "start"))
        els += p.stems(ns, vals, "n2" if i < 3 else "n3", min(i + 1, 4))
    for k in range(3):
        els.append(T(ps[3].px(k), ps[3].py(0) + 17, str(k), "tm", 4, 14))
    return els


def fig_w9_pulse():
    p = Plot(-0.6, 2.2, 0, 4.6, 50, 30, 270, 200)
    els = p.axes("t", "", xt=[0.5, 1], yt=[1, 2, 4])
    for k, (D, b) in enumerate([(1, 1), (0.5, 2), (0.25, 3)]):
        els.append(R(p.px(0), p.py(1 / D), p.px(D) - p.px(0), p.py(0) - p.py(1 / D), "n" if b < 3 else "n3", b, 0))
    els.append(A(p.px(1.6), p.py(0), p.px(1.6), p.py(1.6), "e2", 4, 9))
    els.append(T(p.px(1.6), p.py(1.6) - 8, "δ(t)", "tb", 4, 15))
    els.append(T(408, 90, "폭 1 × 높이 1", "t", 1, 14))
    els.append(T(408, 114, "폭 0.5 × 높이 2", "t", 2, 14))
    els.append(T(408, 138, "폭 0.25 × 높이 4", "t", 3, 14))
    els.append(T(408, 170, "넓이는 늘 1", "tb", 3, 15))
    els.append(T(408, 200, "폭 → 0: 화살표", "tb", 4, 14))
    return els


UNITS.append(unit(
    "wb-9", "단위 계단과 단위 임펄스",
    "u[n], δ[n], u(t), δ(t) 를 표와 그림으로 그리고, δ[n] = u[n] - u[n-1], u[n] = δ의 누적 합, x[n]δ[n-k] = x[k]δ[n-k] 를 손으로 확인할 수 있어요.",
    ["단위 임펄스", "단위 계단", "누적 합", "1차 차분", "선별 성질"],
    ["지연", "누산기", "적분", "미분", "시그마 기호"],
    [
        title("단위 계단과 단위 임펄스", "손뼉 한 번과 스위치 켜기"),
        goal(r"[[단위 임펄스]] $\delta[n]$ 와 [[단위 계단]] $u[n]$ 을 표로 그려요.",
             r"$\delta[n]=u[n]-u[n-1]$ 과 $u[n]$ 은 $\delta$ 의 [[누적 합|이라는/이라는]] 것을 확인해요.",
             r"$x[n]\delta[n-k]=x[k]\delta[n-k]$ 로 한 칸의 값을 골라내요."),
        ana("손뼉과 스위치",
            "빈 방에서 손뼉을 딱 한 번 치면 그 순간에만 소리가 나요. 스위치는 켜는 순간부터 계속 켜져 있어요.",
            ["손뼉 한 번(아주 짧은 톡)", r"[[단위 임펄스]] $\delta[n]$, $\delta(t)$"],
            ["스위치를 켜는 순간, 그 뒤로 계속 켜짐", "[[단위 계단]] $u[n]$, $u(t)$"],
            ["켜는 순간의 변화", "계단이 뛰는 곳 = 톡"]),
        fml("[[단위 임펄스]] (S2 p.45)", r"\delta[n] = \begin{cases} 1, & n = 0 \\ 0, & n \neq 0 \end{cases}",
            [(r"\delta", "'델타'. 그리스 글자 d"),
             ("n=0", "$n=0$ 인 칸에서만 1"),
             (r"n\neq 0", "나머지 모든 칸에서는 0")],
            "델타 엔은 엔이 0일 때 1, 아닐 때 0. 딱 한 칸만 1인 가장 간단한 신호예요."),
        fml("[[단위 계단]] (S2 p.46)", r"u[n] = \begin{cases} 0, & n < 0 \\ 1, & n \ge 0 \end{cases}",
            [("u", "unit step 의 u"),
             ("n<0", "0보다 앞 칸은 모두 0"),
             (r"n\ge 0", "0번 칸부터는 쭉 1. $u[0]=1$ 이에요")],
            "유 엔은 엔이 영보다 작으면 영, 영 이상이면 일. 0번 칸에서 켜지는 스위치예요."),
        stp("손계산 1: 표로 쓰기", "$n=-2$ 부터 $3$ 까지",
            [r"$\delta[n]$: $0, 0, 1, 0, 0, 0$ ($n=0$ 에서만 1)",
             "$u[n]$: $0, 0, 1, 1, 1, 1$ ($n=0$ 부터 1)",
             r"$\delta[n-2]$: 2단원 '빼면 오른쪽'. $n=2$ 에서만 1",
             "$u[n-1]$: $n=1$ 부터 1인 계단. 한 칸 [[지연|이에요/예요]]."],
            "모양을 외우기보다 표에 숫자를 넣어 보는 습관이 가장 안전해요."),
        fig("[[단위 임펄스|와/과]] [[단위 계단]]", fig_w9_two(),
            "왼쪽은 0번 칸에만 막대 하나, 오른쪽은 0번 칸부터 끝없이 높이 1이에요."),
        chk(r"$\delta[3]$ 의 값은?", ["$0$", "$1$", "$3$", r"$\infty$"], 0,
            r"[[단위 임펄스]] $\delta[n]$ 은 $n=0$ 에서만 1이고 $n=3$ 에서는 0이에요."),
        stp("손계산 2: $u[n]-u[n-1]$ ([[1차 차분]])", "지금 값에서 바로 앞 칸 값을 빼요",
            ["$n=-1$: $u[-1]-u[-2]=0-0=0$",
             "$n=0$: $u[0]-u[-1]=1-0=1$",
             "$n=1$: $u[1]-u[0]=1-1=0$",
             "$n=2$: $u[2]-u[1]=1-1=0$"],
            r"결과는 $0, 1, 0, 0$. 즉 $\delta[n]=u[n]-u[n-1]$. [[단위 임펄스|은/는]] 계단의 [[1차 차분|이에요/예요]]."),
        fig("계단에서 한 칸 늦은 계단을 빼면", fig_w9_diff(),
            "켜지는 0번 칸만 남아요. 8단원의 '뛰는 곳의 [[미분|은/는]] 톡' 의 이산 버전이에요."),
        stp(r"손계산 3: $\delta$ 의 [[누적 합]] (S2 p.47)", r"$u[n]=\sum_{m=-\infty}^{n}\delta[m]$",
            [r"7단원 [[누산기]]처럼 [[시그마 기호|으로/로]] 처음부터 $n$ 까지 $\delta$ 를 더해요.",
             "$n=-1$: 아직 0번 칸이 안 나와서 합은 0",
             "$n=0$: 0번 칸의 1이 들어와서 합은 1",
             "$n=3$: 그 뒤로는 0만 더해지니 계속 1"],
            r"$0, 1, 1, 1, \dots$ 바로 $u[n]$. 계단은 임펄스의 [[누적 합|이에요/예요]]."),
        cmp("서로 오가는 두 길", ["방향", "이산", "연속"],
            [["계단 → 임펄스", "[[1차 차분]] $u[n]-u[n-1]$", "[[미분]] $du(t)/dt$"],
             ["임펄스 → 계단", r"[[누적 합]] $\sum_{m\le n}\delta[m]$", r"[[적분]] $\int_{-\infty}^{t}\delta(\tau)d\tau$"]]),
        stp("손계산 4: 한 칸 골라내기 (S2 p.49)", r"$x=[1,2,1]$ ($n=0,1,2$) 에 $\delta[n-1]$ 을 곱해요",
            [r"$\delta[n-1]$ 은 $n=1$ 에서만 1, 나머지 0",
             r"$n=1$: $x[1]\times 1=2$",
             r"다른 칸: $x[n]\times 0=0$",
             r"그래서 $x[n]\delta[n-1]=2\delta[n-1]=x[1]\delta[n-1]$"],
            "곱하면 1번 칸 값만 남아요. 모든 칸을 더하면 $x[1]=2$ 하나. 이것이 [[선별 성질|이에요/예요]]."),
        stp("손계산 5: 신호를 임펄스로 쪼개기 (S3 p.13, 14)", "$x=[1,2,1]$",
            [r"0번 칸 값 1: $1\cdot\delta[n]$",
             r"1번 칸 값 2: $2\cdot\delta[n-1]$",
             r"2번 칸 값 1: $1\cdot\delta[n-2]$",
             r"모두 더하면 $x[n]=\delta[n]+2\delta[n-1]+\delta[n-2]$"],
            r"어떤 신호든 '크기 곱하기 옮긴 임펄스' 의 합이에요: $x[n]=\sum_k x[k]\delta[n-k]$."),
        fig("신호 = 임펄스 도장의 합", fig_w9_decomp(),
            "칸마다 그 칸 값만큼 키운 [[단위 임펄스|을/를]] 세우고 모두 더하면 원래 신호예요.", 300),
        pts(r"연속 버전: $u(t)$ 와 $\delta(t)$ (S2 p.50~52)",
            "$u(t)$: $t<0$ 이면 0, $t>0$ 이면 1. 연속 [[단위 계단|이에요/예요]].",
            r"$\delta(t)$: $t=0$ 에서만 있는 아주 짧은 톡. 그림은 화살표예요.",
            "화살표 옆 1은 높이가 아니라 넓이예요 (S2 p.50: 'area, rather than actual value').",
            r"$\delta(t)=du(t)/dt$, $u(t)=\int_{-\infty}^{t}\delta(\tau)d\tau$ (S2 p.51)."),
        stp("손계산 6: 폭을 줄이는 펄스 (S2 p.51)", r"폭 $\Delta$, 높이 $1/\Delta$ 인 사각형 $\delta_\Delta(t)$",
            [r"$\Delta=1$: 높이 1, 넓이 $1\times 1=1$",
             r"$\Delta=0.5$: 높이 2, 넓이 $0.5\times 2=1$",
             r"$\Delta=0.25$: 높이 4, 넓이 1",
             r"$\Delta=0.1$: 높이 10, 넓이 1"],
            r"폭이 0에 가까워질수록 높이는 끝없이 커지지만 넓이는 늘 1. 그 끝이 $\delta(t)$ 예요."),
        fig("넓이 1은 그대로, 폭만 줄여요", fig_w9_pulse(),
            r"[[단위 임펄스]] $\delta(t)$ 는 폭 0, 넓이 1인 톡이라 화살표로 그려요."),
        chk("처음부터 지금까지의 값을 모두 더한 것을 뭐라고 하나요?",
            ["[[누적 합]]", "[[1차 차분]]", "[[선별 성질]]", "[[단위 계단]]"], 0,
            r"[[누적 합|이에요/예요]]. $\delta$ 의 [[누적 합|이/가]] [[단위 계단]] $u[n]$ 이에요."),
        warn("헷갈리기 쉬운 점",
             r"$\delta[n]$ 은 높이 1이지만, $\delta(t)$ 의 1은 높이가 아니라 넓이예요.",
             r"$\delta[n-2]$ 는 $n=2$ 에 있어요. 빼면 오른쪽!",
             r"$x[n]\delta[n-k]$ 는 $x[k]\delta[n-k]$. $x[n]$ 전체가 아니라 $k$ 번 칸 값 하나만 남아요."),
        where(r"S2 p.45: $\delta[n]$. p.46: $u[n]$, $\delta[n]=u[n]-u[n-1]$ ([[1차 차분]])",
              r"S2 p.47, 48: $u[n]=\sum_{m=-\infty}^{n}\delta[m]=\sum_{k=0}^{\infty}\delta[n-k]$. p.49: $x[n]\delta[n-n_0]=x[n_0]\delta[n-n_0]$",
              r"S2 p.50~53: $\delta(t)$, $u(t)$, $x(t)\delta(t)=x(0)\delta(t)$. S3 p.8 에서 다시 복습",
              r"S3 p.14: $x[n]=\sum_k x[k]\delta[n-k]$. S3 p.37: 연속 [[선별 성질]] $\int x(\tau)\delta(t-\tau)d\tau$",
              r"시험 모양: 정의 쓰기, 표 채우기, $u$ 와 $\delta$ 사이 관계식 고르기."),
        recap(r"[[단위 임펄스]] $\delta[n]$: 0번 칸만 1. [[단위 계단]] $u[n]$: 0번 칸부터 쭉 1.",
              r"$\delta[n]=u[n]-u[n-1]$, $u[n]=\sum_{m\le n}\delta[m]$.",
              r"$x[n]\delta[n-k]=x[k]\delta[n-k]$, 그래서 $x[n]=\sum_k x[k]\delta[n-k]$.",
              r"$\delta(t)$ 는 넓이 1인 톡(화살표), $\delta(t)=du/dt$."),
    ]))


# ================================================================ wb-10 손으로 하는 컨볼루션
XC = [1, 2, 1]
HC = [1, 1]
YC = list(np.convolve(XC, HC))
assert YC == [1, 3, 3, 1] and len(YC) == len(XC) + len(HC) - 1
assert sum(YC) == sum(XC) * sum(HC) == 8
assert list(np.convolve(HC, XC)) == YC
STAMPS = [[XC[k] * (HC[n - k] if 0 <= n - k < len(HC) else 0) for n in range(4)] for k in range(3)]
assert STAMPS == [[1, 1, 0, 0], [0, 2, 2, 0], [0, 0, 1, 1]]
assert [sum(col) for col in zip(*STAMPS)] == YC


def xc(k):
    return XC[k] if 0 <= k < len(XC) else 0


def hc(k):
    return HC[k] if 0 <= k < len(HC) else 0


def yc(n):
    return sum(xc(k) * hc(n - k) for k in range(-5, 10))


assert [yc(n) for n in range(-1, 5)] == [0, 1, 3, 3, 1, 0]
assert [hc(1 - k) for k in range(-1, 4)] == [0, 1, 1, 0, 0]
assert [xc(k) * hc(1 - k) for k in range(-1, 4)] == [0, 1, 2, 0, 0]
# S3 p.26 Example 2.1: h = [1,1,1] (n=0,1,2), x = 0.5 delta[n] + 2 delta[n-1]
Y21 = list(np.convolve([0.5, 2], [1, 1, 1]))
assert Y21 == [0.5, 2.5, 2.5, 2.0]
# 항등: h = delta 이면 y = x
assert list(np.convolve(XC, [1])) == XC


def fig_w10_stamp():
    ps = [Plot(-1.6, 4.6, 0, 3.4, 190, 10 + 68 * i, 270, 48) for i in range(4)]
    ns = list(range(-1, 5))
    rows = [("x[0]=1: 1 h[n]", STAMPS[0]), ("x[1]=2: 2 h[n-1]", STAMPS[1]),
            ("x[2]=1: 1 h[n-2]", STAMPS[2]), ("다 더하면 y[n]", YC)]
    els = []
    for i, (lab, vals) in enumerate(rows):
        p = ps[i]
        full = [vals[n] if 0 <= n < 4 else 0 for n in ns]
        els.append(L(p.X, p.py(0), p.X + p.Wd, p.py(0), "e", i + 1))
        els.append(T(12, p.py(0) - 8, lab, "tb", i + 1, 15, "start"))
        els += p.stems(ns, full, "n2" if i < 3 else "n3", i + 1)
        for n, v in zip(ns, full):
            if v:
                els.append(T(p.px(n) + 10, p.py(v) + 4, str(v), "tm", i + 1, 14, "start"))
    for n in range(4):
        els.append(T(ps[3].px(n), ps[3].py(0) + 17, str(n), "tm", 4, 14))
    return els


def fig_w10_table():
    ks = list(range(-1, 4))
    x0, dx = 200, 55
    els = [T(x0 - 120, 40, "k", "tb", 0, 16)]
    for i, k in enumerate(ks):
        els.append(T(x0 + dx * i, 40, str(k), "tb", 0, 16))
    rows = [("x[k]", [xc(k) for k in ks], 1), ("h[-k] 뒤집기", [hc(-k) for k in ks], 2),
            ("h[1-k] 밀기", [hc(1 - k) for k in ks], 3), ("곱하기", [xc(k) * hc(1 - k) for k in ks], 4)]
    for r, (lab, vals, b) in enumerate(rows):
        y = 82 + 42 * r
        els.append(T(x0 - 120, y, lab, "tb" if r != 1 else "t", b, 15))
        for i, v in enumerate(vals):
            if r == 3 and v:
                els.append(R(x0 + dx * i - 18, y - 20, 36, 28, "n3", b))
            els.append(T(x0 + dx * i, y, str(v), "tb" if v else "tm", b, 16))
    els.append(L(40, 55, 460, 55, "e"))
    els.append(T(260, 262, "더하기: 0 + 1 + 2 + 0 + 0 = 3 = y[1]", "tb", 5, 16))
    return els


def fig_w10_result():
    p = Plot(-1.6, 4.6, 0, 3.6, 40, 35, 260, 190)
    els = p.axes("n", "y[n]", xt=[-1, 1, 2, 3, 4], yt=[1, 3])
    els.append(T(p.px(0) - 7, p.py(0) + 18, "0", "tm", 0, 14, "end"))
    els += p.stems(range(-1, 5), [yc(n) for n in range(-1, 5)], "n2", 1)
    els.append(T(398, 120, "y = [1, 3, 3, 1]", "tb", 2, 14))
    els.append(T(398, 146, "길이 3 + 2 - 1 = 4", "t", 2, 14))
    els.append(T(398, 172, "합 8 = 4 × 2", "t", 2, 14))
    return els


UNITS.append(unit(
    "wb-10", "손으로 하는 컨볼루션",
    "x = [1, 2, 1], h = [1, 1] 의 컨볼루션을 도장 찍기와 뒤집고 밀고 곱하고 더하기 두 방법으로 손계산하고, numpy 로 확인할 수 있어요.",
    ["컨볼루션", "컨볼루션 합", "임펄스 응답", "LTI 시스템", "교환 법칙"],
    ["단위 임펄스", "시간 반전", "지연", "선별 성질", "시그마 기호"],
    [
        title("손으로 하는 컨볼루션", "뒤집고, 밀고, 곱하고, 더하기"),
        goal("[[임펄스 응답]] $h[n]$ 이 무엇인지 말해요.",
             "$x=[1,2,1]$, $h=[1,1]$ 의 [[컨볼루션|을/를]] 도장 찍기로 구해요.",
             "뒤집고, 밀고, 곱하고, 더하는 표로 같은 답을 확인해요."),
        ana("메아리 도장",
            "빈 방에서 손뼉을 한 번 치면 메아리가 울려요. 손뼉을 여러 번, 세기를 바꿔 치면 손뼉마다 메아리가 그 세기만큼 생기고, 겹친 메아리가 모두 더해져서 들려요.",
            ["손뼉 한 번에 울리는 메아리", "[[임펄스 응답]] $h[n]$"],
            ["입력의 한 칸 한 칸(세기가 다른 손뼉)", r"$x[k]\delta[n-k]$"],
            ["메아리 도장을 크기만큼 찍고 모두 더하기", "[[컨볼루션]] $y=x*h$"]),
        pts("[[LTI 시스템]]이 뭐였죠",
            "선형: 두 배 넣으면 두 배, 둘을 섞어 넣으면 결과도 섞여 나오는 정직한 계산기.",
            "시불변: 월요일에 해도 금요일에 해도 맛이 똑같은 레시피. 늦게 넣으면 늦게 나와요([[지연]]).",
            "둘 다 가진 시스템이 [[LTI 시스템|이에요/예요]] (S3 p.22).",
            "주문: " + MANTRA_LTI),
        pts("[[임펄스 응답]] $h[n]$ (S3 p.15)",
            r"[[단위 임펄스]] $\delta[n]$ 을 시스템에 넣었을 때 나오는 출력이 [[임펄스 응답|이에요/예요]].",
            r"시불변이라 $\delta[n-k]$ 를 넣으면 $h[n-k]$ 가 나와요. 모양 그대로 $k$ 칸 늦게.",
            r"선형이라 $x[k]\delta[n-k]$ 를 넣으면 $x[k]h[n-k]$ 가 나와요. 크기만큼 키워서.",
            r"9단원: $x[n]=\sum_k x[k]\delta[n-k]$. 그러니 출력은 $\sum_k x[k]h[n-k]$ 예요."),
        fml("[[컨볼루션 합]] (S3 p.22)", r"y[n] = \sum_{k=-\infty}^{\infty} x[k]\,h[n-k] = x[n]*h[n]",
            [("x[k]", "입력의 $k$ 번 칸 값(손뼉 세기)"),
             ("h[n-k]", "$k$ 칸 늦게 시작한 메아리"),
             (r"\sum_{k}", "[[시그마 기호]]: 모든 $k$ 에 대해 더하기"),
             ("*", "별표는 곱하기가 아니라 [[컨볼루션]] 기호")],
            "와이 엔은 시그마 엑스 케이 곱하기 에이치 엔 마이너스 케이. [[LTI 시스템]]의 출력은 이 [[컨볼루션 합|으로/로]] 나와요."),
        stp("손계산 1: 도장 찍기 (S3 p.27 첫째 관점)", "$x=[1,2,1]$, $h=[1,1]$, 둘 다 0번 칸부터",
            [r"$x[0]=1$: 도장 $1\cdot h[n]$ 을 0번 칸부터 → $[1,1,0,0]$",
             r"$x[1]=2$: 도장 $2\cdot h[n-1]$ 을 1번 칸부터 → $[0,2,2,0]$",
             r"$x[2]=1$: 도장 $1\cdot h[n-2]$ 를 2번 칸부터 → $[0,0,1,1]$",
             r"칸마다 세로로 더해요: $[1+0+0,\ 1+2+0,\ 0+2+1,\ 0+0+1]$"],
            "$y=[1,3,3,1]$ ($n=0,1,2,3$). 이게 [[컨볼루션|이에요/예요]]."),
        fig("메아리 도장 세 개를 더하기", fig_w10_stamp(),
            "위 세 줄이 칸마다 찍은 도장, 맨 아래가 합 $y[n]$ 이에요. $k$ 를 고정하고 모든 $k$ 를 더하는 관점이에요.", 300),
        chk("$x=[1,2,1]$, $h=[1,1]$ 일 때 $y[1]$ 은?", ["$3$", "$2$", "$1$", "$4$"], 0,
            "1번 칸에는 첫 도장의 1과 둘째 도장의 2가 겹쳐서 $1+2=3$ 이에요."),
        pts("둘째 방법: 뒤집고, 밀고, 곱하고, 더하기 (S3 p.24)",
            "1. 뒤집기: $h[k]$ 를 $h[-k]$ 로. 2단원 [[시간 반전|이에요/예요]].",
            "2. 밀기: $h[n-k]$ 는 $h[-k]$ 를 오른쪽으로 $n$ 칸. 빼면 오른쪽!",
            r"3. 곱하기: 칸마다 $x[k]\times h[n-k]$",
            "4. 더하기: 곱한 값을 모든 $k$ 에 대해 더하면 $y[n]$ 하나"),
        fig("$n=1$ 일 때의 표", fig_w10_table(),
            "$h$ 를 뒤집고 1칸 민 줄을 $x[k]$ 아래에 두고, 세로로 곱해서 더해요. 답은 $y[1]=3$."),
        stp("손계산 2: 표로 모든 $n$ 구하기", "뒤집은 $h[n-k]$ 는 $k=n-1$, $k=n$ 두 칸에 1",
            [r"$n=0$: 겹치는 칸 $k=0$ 하나. $x[0]\cdot 1=1$",
             "$n=1$: 겹치는 칸은 $k=0$ 과 $k=1$. 곱해서 더하면 $1+2=3$",
             "$n=2$: 겹치는 칸은 $k=1$ 과 $k=2$. 곱해서 더하면 $2+1=3$",
             "$n=3$: 겹치는 칸은 $k=2$ 하나. 값은 $1$",
             "$n=-1$ 이나 $n=4$: 겹치는 칸이 없어 $0$"],
            "$y=[1,3,3,1]$. 도장 방법과 똑같아요. $n$ 을 고정하고 $k$ 로 더하는 관점이에요."),
        fig("출력 $y[n]$", fig_w10_result(),
            "결과 길이는 $3+2-1=4$ 칸. 합은 $x$ 의 합 $4$ 곱하기 $h$ 의 합 $2$, 즉 8이에요."),
        stp("손계산 3: 컴퓨터로 확인", "Python 의 numpy",
            ["import numpy as np",
             "np.convolve([1, 2, 1], [1, 1])",
             "결과: array([1, 3, 3, 1])",
             r"길이 검사: $3+2-1=4$. 합 검사: $1+3+3+1=8=4\times 2$"],
            "손계산과 같아요. 시험장에서는 길이 검사와 합 검사로 스스로 확인해요."),
        stp("손계산 4: S3 p.26 Example 2.1", "$h=[1,1,1]$ ($n=0,1,2$), $x[0]=0.5$, $x[1]=2$",
            [r"도장 1: $0.5\cdot h[n]=[0.5,0.5,0.5,0]$",
             r"도장 2: $2\cdot h[n-1]=[0,2,2,2]$",
             r"칸마다 더하기: $[0.5,\ 2.5,\ 2.5,\ 2]$",
             r"슬라이드 답 $y=[0\ 0\ 0.5\ 2.5\ 2.5\ 2\ 0]$ 과 같아요 (앞의 $0$ 두 칸은 $n<0$)."],
            "$y[n]=0.5h[n]+2h[n-1]$. 교과서 예제도 도장 찍기로 바로 풀려요."),
        stp("손계산 5: 순서 바꾸기 ([[교환 법칙]])", "$h*x$: 이번엔 $h$ 의 칸마다 $x$ 도장",
            [r"$h[0]=1$: $1\cdot x[n]=[1,2,1,0]$",
             r"$h[1]=1$: $1\cdot x[n-1]=[0,1,2,1]$",
             "더하기: $[1,3,3,1]$",
             "$x*h$ 와 같아요 (S3 p.52)."],
            "$x*h=h*x$. [[컨볼루션|은/는]] [[교환 법칙|이/가]] 성립해서 편한 쪽을 도장으로 써요."),
        chk("길이 3인 $x$ 와 길이 2인 $h$ 를 [[컨볼루션]]하면 결과 길이는?", ["$4$", "$5$", "$6$", "$3$"], 0,
            "길이 $=3+2-1=4$. 마지막 도장이 $h$ 길이만큼 삐져나오기 때문이에요."),
        chk("[[단위 임펄스]]를 넣었을 때 나오는 출력 $h[n]$ 을 뭐라고 하나요?",
            ["[[임펄스 응답]]", "[[컨볼루션 합]]", "[[교환 법칙]]", "[[선별 성질]]"], 0,
            "[[임펄스 응답|이에요/예요]]. 이것 하나로 모든 출력을 [[컨볼루션]]으로 구해요."),
        warn("헷갈리기 쉬운 점",
             "표 방법에서는 $h$ 를 꼭 뒤집어요. 도장 방법은 뒤집지 않아도 같은 답이 나와요.",
             "$y$ 의 첫 칸은 $x$ 의 첫 칸 번호 $+$ $h$ 의 첫 칸 번호예요. 여기서는 $0+0=0$.",
             "$*$ 는 곱하기가 아니에요. $[1,2,1]*[1,1]$ 은 $[1,2,0]$ 이 아니라 $[1,3,3,1]$."),
        where(r"S3 p.14, 15: $x[n]=\sum_k x[k]\delta[n-k]$, $\delta[n]$ 을 넣은 출력이 [[임펄스 응답]] $h[n]$",
              r"S3 p.22: [[컨볼루션 합]] $y[n]=\sum_k x[k]h[n-k]=x[n]*h[n]$. p.24: 뒤집고 밀고 곱하고 더하는 4단계",
              "S3 p.26 Example 2.1, p.27 두 관점(도장 / 뒤집고 밀기), p.28~33 Example 2.2 ~ 2.5",
              "S3 p.40: 연속 버전 컨볼루션 적분. p.52: [[교환 법칙]] $x*h=h*x$",
              "교수님: 컨볼루션 손계산은 과제든 퀴즈든 연습해 보라. 첫 퀴즈 범위는 S3 p.70 까지."),
        recap(r"[[임펄스 응답]] $h[n]$: $\delta[n]$ 을 넣었을 때의 출력, 메아리.",
              r"도장 찍기: 칸마다 $x[k]\cdot h[n-k]$ 를 찍고 세로로 더하기.",
              "표 방법: 뒤집고, 밀고, 곱하고, 더하기. $[1,2,1]*[1,1]=[1,3,3,1]$.",
              "검사: 길이 $=$ 길이 합 $-1$, 합 $=$ 두 합의 곱. [[교환 법칙]] $x*h=h*x$."),
    ]))


# ================================================================ 저장
DATA = {"week": "b", "title": "기초 다지기. 신호및시스템에 필요한 수학 처음부터", "units": UNITS}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(DATA, f, ensure_ascii=False, indent=1)
print("저장:", OUT)
print("단원", len(UNITS), "슬라이드", sum(len(u["slides"]) for u in UNITS),
      "그림", sum(1 for u in UNITS for s in u["slides"] if s["kind"] == "figure"))
for u in UNITS:
    print(" ", u["id"], u["title"], len(u["slides"]), "장, 용어", len(u["terms"]))
