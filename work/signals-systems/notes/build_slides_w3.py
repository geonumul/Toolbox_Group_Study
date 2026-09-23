"""3주차 정리 슬라이드 생성 (덱 S3, 2장 선형 시불변(LTI) 시스템). 실행: python build_slides_w3.py
모든 숫자 답은 아래에서 Python 으로 계산하고 assert 로 확인한다."""
import json, math, os, re, sys
from xml.sax.saxutils import escape

import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "slides_w3.json")
DICT = os.path.join(HERE, "..", "rules", "용어사전.json")

# ---------------------------------------------------------------- 용어 표 (용어사전.json 표기 그대로)
TERMS = {}
for _t in json.load(open(DICT, encoding="utf-8")):
    _ko, _en = (_t.get("ko") or "").strip(), (_t.get("en") or "").strip()
    _key = _ko or _en
    if _key and _key not in TERMS:
        TERMS[_key] = (_ko, _en, _t.get("say", ""))


def josa(word, pair):
    """받침 있을 때/없을 때 조사 쌍 (은/는, 이/가, 을/를, 과/와, 으로/로, 이에요/예요, 이라고/라고)."""
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
        raise KeyError("모르는 용어 표시: " + key)
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


MANTRA1 = "신호는 시간에 따라 변하는 값, 시스템은 신호를 바꾸는 상자."
MANTRA2 = "LTI 시스템은 임펄스 응답 하나만 알면 된다. 출력은 뒤집고, 밀고, 곱하고, 더해서(컨볼루션) 구한다."
OUTSIDE = "다음 수업에서 배울 내용 (첫 퀴즈 범위 밖)"


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


def frm(head, tex, parts, whole):
    assert 2 <= len(parts) <= 6
    return {"kind": "formula", "head": head, "tex": tex,
            "parts": [{"sym": s, "say": w} for s, w in parts], "whole": whole}


def stp(head, given, steps, answer):
    assert 3 <= len(steps) <= 7, head
    d = {"kind": "steps", "head": head, "steps": list(steps), "answer": answer}
    if given:
        d["given"] = given
    return d


def cmp(head, cols, rows):
    assert 2 <= len(cols) <= 4 and 2 <= len(rows) <= 6
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
    return {"kind": "recap", "items": list(items)}


# ---------------------------------------------------------------- SVG 도우미 (클래스만)
W = 480
_TEXTS = []  # 현재 그림의 글자 상자 (겹침 검사)


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
    return '<circle cx="%g" cy="%g" r="%g" class="%s"/>' % (cx, cy, r, _c(c, b))


def L(x1, y1, x2, y2, c="e", b=0):
    return '<line x1="%g" y1="%g" x2="%g" y2="%g" class="%s"/>' % (
        round(x1, 1), round(y1, 1), round(x2, 1), round(y2, 1), _c(c, b))


def T(x, y, s, c="t", b=0, fs=15, a="middle", maxw=None):
    assert 14 <= fs <= 20
    w = tw(s, fs)
    left = x - w / 2 if a == "middle" else (x if a == "start" else x - w)
    assert left >= 1 and left + w <= W - 1, "화면 밖 글자 %r left=%.0f w=%.0f" % (s, left, w)
    assert y - fs * 0.8 >= 0, "위로 넘친 글자 %r" % s
    if maxw is not None:
        assert w <= maxw, "글자 넘침 %r %.0f>%s" % (s, w, maxw)
    _TEXTS.append((left, y - fs * 0.78, left + w, y + fs * 0.12, s))
    return '<text x="%g" y="%g" font-size="%d" text-anchor="%s" class="%s">%s</text>' % (
        round(x, 1), round(y, 1), fs, a, _c(c, b), escape(s))


def A(x1, y1, x2, y2, c="e2", b=0):
    dx, dy = x2 - x1, y2 - y1
    n = math.hypot(dx, dy)
    ux, uy = dx / n, dy / n
    bx, by = x2 - ux * 9, y2 - uy * 9
    px, py = -uy * 4.5, ux * 4.5
    head = '<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" class="%s"/>' % (
        x2, y2, bx + px, by + py, bx - px, by - py, _c("arrow", b))
    return L(x1, y1, bx, by, c, b) + head


def PL(pts_, c="e2", b=0):
    s = " ".join("%.1f,%.1f" % p for p in pts_)
    return '<polyline points="%s" fill="none" class="%s"/>' % (s, _c(c, b))


def PG(pts_, c="n3", b=0):
    s = " ".join("%.1f,%.1f" % p for p in pts_)
    return '<polygon points="%s" class="%s"/>' % (s, _c(c, b))


def BOX(x, y, w, h, label, c="box", b=0, fs=15, tc="tb"):
    return R(x, y, w, h, c, b) + T(x + w / 2, y + h / 2 + fs * 0.35, label, tc, b, fs, maxw=w - 4)


def ADDER(cx, cy, b=0, r=12):
    return C(cx, cy, r, "n", b) + L(cx - 6, cy, cx + 6, cy, "e", b) + L(cx, cy - 6, cx, cy + 6, "e", b)


def STEMS(ox, base, dx, vals, scale, b=0, line="e2", dot="n2", zero=True, nrange=None):
    """이산 신호 줄기 그림. vals: {n: 값}. ox 는 n=0 의 x 좌표."""
    out = []
    ns = nrange if nrange is not None else sorted(vals)
    for n in ns:
        v = vals.get(n, 0)
        x = ox + n * dx
        if abs(v) < 1e-12:
            if zero:
                out.append(C(x, base, 3, "n", b))
        else:
            top = base - v * scale
            out.append(L(x, base, x, top, line, b))
            out.append(C(x, top, 4, dot, b))
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


# ---------------------------------------------------------------- 단원 조립과 검사
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


MATH = re.compile(r"\$\$[\s\S]+?\$\$|\$[^$\n]+?\$")


def engine_check(uid, slides):
    """엔진 숫자 버그(공백 사이 숫자)와 $ 짝, 수식 안 한글을 미리 잡는다."""
    for s in slides:
        for k, v in s.items():
            if k == "svg":
                continue
            for t in _strings(v):
                if k in ("tex",) or (k == "parts"):
                    pass
                assert t.count("$") % 2 == 0 or k in ("tex",), "%s: $ 짝 %r" % (uid, t)
        for part in s.get("parts", []):
            assert "$" not in part["sym"]
        for t in _strings({k: v for k, v in s.items() if k not in ("tex", "parts")}):
            plain = MATH.sub(" X ", t)
            m = re.search(r"(?<= )\d+(?= )", plain)
            assert not m, "%s: 공백 사이 숫자 %r" % (uid, plain[max(0, m.start() - 20):m.end() + 10])
            for mm in MATH.finditer(t):
                assert not re.search("[가-힣]", mm.group(0)) or "\\text" in mm.group(0), "%s: 수식 안 한글 %r" % (uid, t)
        for part in s.get("parts", []):
            plain = MATH.sub(" X ", part["say"])
            m = re.search(r"(?<= )\d+(?= )", plain)
            assert not m, "%s: 공백 사이 숫자 %r" % (uid, part["say"])


def unit(uid, ttl, gl, terms, slides):
    slides = fill(slides)
    body = " ".join(_strings(slides))
    tl = []
    for key in terms:
        ko, en, say = TERMS[key]
        n = body.count(key)
        assert n >= 3, "%s: 용어 %s 가 %d번" % (uid, key, n)
        tl.append({"ko": ko, "en": en, "say": say})
    assert 4 <= len(tl) <= 10
    assert 10 <= len(slides) <= 18, "%s: 슬라이드 %d장" % (uid, len(slides))
    kinds = [s["kind"] for s in slides]
    assert kinds[0] == "title" and kinds[1] == "goal" and kinds[-1] == "recap", uid
    for need in ("analogy", "figure", "check"):
        assert need in kinds, (uid, need)
    assert 1 <= kinds.count("check") <= 3, uid
    names = ", ".join("%s(%s)" % (t["ko"], t["en"]) if t["ko"] else t["en"] for t in tl)
    slides[-1]["items"].append("오늘의 용어: " + names)
    assert 3 <= len(slides[-1]["items"]) <= 6
    engine_check(uid, slides)
    return {"id": uid, "title": ttl, "goal": fill(gl), "terms": tl, "slides": slides}


def conv(a, b):
    return [float(v) for v in np.convolve(np.array(a, float), np.array(b, float))]


def close(a, b, eps=1e-9):
    return all(abs(x - y) < eps for x, y in zip(a, b)) and len(a) == len(b)


UNITS = []

# ==== UNITS BELOW ====
# ================================================================ w3-1 복습: 복소 지수와 RC 회로 (p.3~8)
V_RC1 = 1 - math.exp(-1)
assert abs(V_RC1 - 0.632) < 5e-4 and abs(math.exp(-1) - 0.368) < 5e-4
_w0 = 3 * math.pi / 4
_m, _N = 3, 8
assert abs(_w0 - 2 * math.pi * _m / _N) < 1e-12 and math.gcd(_m, _N) == 1
assert abs(_m * 2 * math.pi / _w0 - 8) < 1e-12
assert abs(np.exp(1j * _w0 * 8) - 1) < 1e-12   # 8칸 뒤 같은 값


def fig_unit_circle():
    cx, cy, r = 130, 140, 95
    th = math.radians(40)
    px, py = cx + r * math.cos(th), cy - r * math.sin(th)
    circ = [(cx + r * math.cos(2 * math.pi * i / 72), cy - r * math.sin(2 * math.pi * i / 72)) for i in range(73)]
    return fig("단위원 위를 도는 점과 두 그림자", [
        L(20, cy, 250, cy), L(cx, 25, cx, 258),
        T(246, cy - 8, "Re", "tm", fs=14, a="end"), T(cx + 8, 38, "Im", "tm", fs=14, a="start"),
        PL(circ, "e"),
        L(cx, cy, px, py, "e2", 1), C(px, py, 6, "n2", 1),
        T(px + 10, py - 8, "e^(jωt)", "tb", 1, fs=15, a="start"),
        L(px, py, px, cy, "e", 2), L(px, py, cx, py, "e", 2),
        T(px - 4, cy + 20, "cos(ωt)", "t", 2, fs=14, a="end"),
        T(cx - 6, py + 5, "sin(ωt)", "t", 2, fs=14, a="end"),
        T(300, 95, "가로 그림자 = cos", "tb", 3, fs=15, a="start"),
        T(300, 118, "(실수부)", "tm", 3, fs=14, a="start"),
        T(300, 158, "세로 그림자 = sin", "tb", 3, fs=15, a="start"),
        T(300, 181, "(허수부)", "tm", 3, fs=14, a="start"),
        T(300, 225, "점이 돌면 출렁여요", "t", 3, fs=15, a="start")],
        r"[[단위원]] 위의 점 $e^{j\omega t}$ 를 옆에서 비추면 $\cos$, 아래에서 비추면 $\sin$ 이에요. 이게 [[오일러 공식|이에요/예요]].")


def fig_rc_charge():
    ox, oy, sx, sy = 50, 230, 75, 160
    curve = [(ox + t * sx, oy - (1 - math.exp(-t)) * sy) for t in np.linspace(0, 5, 101)]
    x1, y1 = ox + sx, oy - V_RC1 * sy
    return fig("RC 회로 충전 곡선 ($RC=1$, $v_s=1$)", [
        L(ox, oy, 460, oy), L(ox, oy, ox, 30),
        T(458, oy + 20, "t", "tm", fs=14, a="end"), T(ox + 8, 40, "v_c(t)", "tm", fs=14, a="start"),
        L(ox, oy - sy, 440, oy - sy, "e"), T(ox - 6, oy - sy + 5, "1", "tm", fs=14, a="end"),
        T(ox - 6, oy + 5, "0", "tm", fs=14, a="end"),
        PL(curve, "e2", 1),
        L(x1, oy, x1, y1, "e", 2), C(x1, y1, 5, "n2", 2),
        T(x1 + 12, y1 + 20, "t=1 에서 0.632", "tb", 2, fs=15, a="start"),
        T(x1, oy + 18, "1", "tm", 2, fs=14),
        T(320, 200, "전원 전압 1까지 차올라요", "t", 3, fs=15)],
        "[[RC 회로]]의 축전기 전압은 [[실수 지수 신호]] 모양 $1-e^{-t}$ 로 차오르다가 1에 다가가요.")


UNITS.append(unit(
    "w3-1", "복습: 복소 지수와 RC 회로",
    "[[복소 지수 신호]]를 '크기 변화 곱하기 회전'으로 설명하고, [[RC 회로|이/가]] 지수 모양으로 차오르는 까닭을 말할 수 있어요.",
    ["복소 지수 신호", "실수 지수 신호", "오일러 공식", "단위원", "RC 회로", "미분방정식", "단위 임펄스", "단위 계단"],
    [
        title("복소 지수와 RC 회로 복습", "2장에 들어가기 전 1장 되짚기 (p.3~8)"),
        goal("[[복소 지수 신호|이/가]] '커지거나 줄기' 곱하기 '돌기'라는 걸 말해요.",
             "[[RC 회로|이/가]] 왜 [[실수 지수 신호]] 모양으로 차오르는지 봐요.",
             "[[단위 임펄스|와/과]] [[단위 계단|을/를]] 다시 떠올려요. 오늘 내내 나와요."),
        pts("주문부터 한 번",
            MANTRA1,
            "2장은 이 상자 중 [[LTI 시스템|을/를]] 다뤄요. 그 전에 1장을 짧게 되짚어요.",
            "교수님이 수업 첫머리에 칠판으로 복습한 내용이에요(p.3~8)."),
        ana("원 위를 도는 점",
            "원 위를 일정한 빠르기로 도는 점이 있어요. 옆에서 비친 그림자는 좌우로, 아래에서 비친 그림자는 위아래로 흔들려요. 도는 동안 원 자체가 점점 커지거나 작아질 수도 있어요.",
            ["원 위를 도는 점", r"[[복소 지수 신호]] $e^{j\omega t}$"],
            ["가로 그림자", r"실수부 $\cos(\omega t)$"],
            ["세로 그림자", r"허수부 $\sin(\omega t)$"],
            ["원이 커지거나 작아짐", r"[[실수 지수 신호]] $e^{\sigma t}$"]),
        frm("복소 지수 = 크기 변화 × 회전 (p.3)",
            r"e^{(\sigma+j\omega)t}=e^{\sigma t}\,e^{j\omega t}",
            [(r"e", "자연상수 e, 약 2.718"),
             (r"\sigma", "시그마. 양수면 커지고 음수면 줄어드는 빠르기"),
             (r"j", "허수 단위 j, 제곱하면 -1"),
             (r"\omega", "오메가. 1초에 도는 각도(각주파수)"),
             (r"e^{\sigma t}", "커짐, 줄어듦 담당 (growth / decay)"),
             (r"e^{j\omega t}", "빙글빙글 돌기 담당 (rotation)")],
            "이 [[복소 지수 신호|은/는]] [[실수 지수 신호|이/가]] 정하는 크기에 회전을 곱한 신호예요."),
        frm("오일러 공식 (무조건 외우기)",
            r"e^{j\omega t}=\cos(\omega t)+j\sin(\omega t)",
            [(r"e^{j\omega t}", "[[단위원]] 위를 도는 점"),
             (r"\cos(\omega t)", "가로 그림자, 실수부"),
             (r"j\sin(\omega t)", "세로 그림자, 허수부 (j 가 붙음)")],
            "[[오일러 공식|은/는]] 교수님이 무조건 외우라고 한 식이에요. 증명은 외울 필요 없어요."),
        fig_unit_circle(),
        pts("허수부는 가짜가 아니에요 (p.3, p.6)",
            "슬라이드: 허수부는 실수부와 90도 어긋난 짝꿍(quadrature) 성분이에요.",
            r"그래프에는 실수부 $\cos$ 만 그려지지만, 허수부 덕분에 위아래로 출렁일 수 있어요.",
            r"칠판 예: 코일과 축전기만 있는 LC 회로를 풀면 $e^{\pm j\omega_0 t}$, $\omega_0=1/\sqrt{LC}$ 가 나와요.",
            "그래서 [[복소 지수 신호|은/는]] 수학 장난이 아니라 실제 회로의 답이에요."),
        pts("RC 회로 식 세우기 (칠판 필기, p.4~5)",
            "[[RC 회로|은/는]] 저항 R 과 축전기 C 를 이은 회로예요. 입력 $v_s(t)$, 출력 $v_c(t)$.",
            r"전압 나누기 $v_s=v_R+v_c$, 저항 $v_R=iR$, 축전기 $i=C\frac{dv_c}{dt}$.",
            r"합치면 $\frac{dv_c}{dt}+\frac{1}{RC}v_c=\frac{1}{RC}v_s$, 1차 [[미분방정식|이에요/예요]].",
            r"2장 p.75 에서 같은 모양 $\frac{dy}{dt}+ay=bx$, $a=b=\frac{1}{RC}$ 로 다시 나와요."),
        stp("손계산: 충전 곡선의 한 점", "$RC=1$, 전원 $v_s=1$, 처음 전압 $v_c(0)=0$",
            [r"풀이 결과: $v_c(t)=v_s\left(1-e^{-t/RC}\right)$ 예요.",
             "$t=1$ 을 넣으면 $1-e^{-1}$.",
             r"$e^{-1}\approx 0.368$ 이라서 $1-0.368=0.632$.",
             r"아주 오래 지나면 $e^{-t}\to 0$ 이라서 $v_c\to 1$, 전원 전압까지 차올라요."],
            r"$v_c(1)\approx 0.632$. [[실수 지수 신호]] 모양으로 차올라요. 전원을 끊으면 반대로 지수 모양으로 방전돼요."),
        fig_rc_charge(),
        warn("시험 범위 주의",
             "[[미분방정식]]을 적분 인자로 푸는 과정은 '알아두기만, 퀴즈나 시험에는 안 낸다'고 했어요(교수님).",
             "그래도 '[[RC 회로|은/는]] 지수 모양으로 차오른다'는 결과와 식 모양은 2.4절에서 다시 써요."),
        cmp("연속시간과 이산시간 복소 지수 (p.7, 표 1.1)", ["항목", r"연속시간 $e^{j\omega_0 t}$", r"이산시간 $e^{j\omega_0 n}$"], [
            [r"$\omega_0$ 가 다르면", "늘 다른 신호", r"$2\pi$ 배수만큼 다르면 같은 신호"],
            ["주기인가", r"어떤 $\omega_0$ 든 주기", r"$\omega_0=2\pi m/N$ 일 때만 주기"],
            ["기본 주기", r"$2\pi/\omega_0$", r"$m(2\pi/\omega_0)$"]]),
        stp("손계산: 이산시간 주기 찾기", r"$e^{j(3\pi/4)n}$",
            [r"$\omega_0=\frac{3\pi}{4}$ 를 $2\pi\cdot\frac{m}{N}$ 꼴로 써요: $\frac{3\pi}{4}=2\pi\cdot\frac{3}{8}$.",
             "$m=3$, $N=8$ 이고 공통 약수가 없어요.",
             r"기본 주기 $=m\cdot\frac{2\pi}{\omega_0}=3\cdot\frac{8}{3}=8$."],
            r"8칸마다 반복해요. $\omega_0=1$ 처럼 $\pi$ 가 없으면 이산시간에서는 주기가 아니에요."),
        pts("단위 임펄스와 단위 계단 (p.8)",
            r"[[단위 임펄스|은/는]] $n=0$ 에서만 1인 손뼉 한 번이에요: $\delta[n]$.",
            r"[[단위 계단|은/는]] $n\ge 0$ 부터 계속 1인 스위치 켜기예요: $u[n]$.",
            r"관계: $\delta[n]=u[n]-u[n-1]$, 거꾸로 $u[n]=\sum_{k=-\infty}^{n}\delta[k]$.",
            r"연속시간 $\delta(t)$ 의 화살표 옆 1은 높이가 아니라 넓이예요."),
        chk("[[오일러 공식|으로/로]] 맞는 것은?",
            [r"$e^{j\omega t}=\cos(\omega t)+j\sin(\omega t)$", r"$e^{j\omega t}=\sin(\omega t)+j\cos(\omega t)$",
             r"$e^{j\omega t}=\cos(\omega t)-\sin(\omega t)$", r"$e^{j\omega t}=e^{\omega t}$"], 0,
            r"가로 그림자가 $\cos$ (실수부), 세로 그림자가 $\sin$ (허수부)이에요."),
        chk("[[실수 지수 신호]]의 뜻은?",
            ["$Ce^{at}$ 에서 $C$ 와 $a$ 가 실수인 신호", "원 위를 도는 신호", "$n=0$ 에서만 1인 신호", "매일 같은 모양이 반복되는 신호"], 0,
            "2번은 [[복소 지수 신호]], 3번은 [[단위 임펄스]], 4번은 주기 신호예요."),
        recap(r"[[복소 지수 신호]] = [[실수 지수 신호]](크기) × 회전 $e^{j\omega t}$.",
              r"[[오일러 공식]]: [[단위원]] 위의 점, 가로 그림자 $\cos$, 세로 그림자 $\sin$.",
              "[[RC 회로|은/는]] 1차 [[미분방정식]], 답은 $1-e^{-t/RC}$ 로 차올라요. 푸는 과정은 시험 밖.",
              r"[[단위 임펄스]] $\delta[n]=u[n]-u[n-1]$, [[단위 계단]] $u[n]$ 은 누적 합."),
    ]))

# ================================================================ w3-2 임펄스로 신호 나타내기 (p.10~17, p.34~38)
X32 = {-1: 2.0, 0: 3.0, 1: 1.0}
_d = lambda n: 1.0 if n == 0 else 0.0
for _n in range(-3, 4):   # x[n] = 2d[n+1] + 3d[n] + d[n-1]
    assert X32.get(_n, 0.0) == 2 * _d(_n + 1) + 3 * _d(_n) + 1 * _d(_n - 1)
assert 2 * 0 + 3 * 1 + 1 * 0 == 3
_s25 = sum(k * 0.25 for k in range(4))
_s10 = sum(k * 0.1 for k in range(10))
assert abs(_s25 - 1.5) < 1e-12 and abs(_s25 * 0.25 - 0.375) < 1e-12
assert abs(_s10 - 4.5) < 1e-9 and abs(_s10 * 0.1 - 0.45) < 1e-9
_s1000 = sum(k * 0.001 for k in range(1000)) * 0.001
assert abs(_s1000 - 0.5) < 1e-3   # 정답 1/2 에 다가감
assert sum([7, 5, 9][k] * (1 if 2 - (k + 1) == 0 else 0) for k in range(3)) == 5  # sum x[k] d[2-k] = x[2] (x[1..3]=7,5,9 에서 x[2]=5)


def fig_decompose():
    ox, base, dx, sc = 100, 200, 35, 40
    els = [L(20, base, 185, base), T(40, 58, "x[n]", "tb", fs=15, a="start")]
    els.append(STEMS(ox, base, dx, X32, sc, nrange=range(-2, 3)))
    for n, v in X32.items():
        els.append(T(ox + n * dx + 12, base - v * sc + 2, "%g" % v, "t", fs=14, a="start"))
    for n in range(-2, 3):
        els.append(T(ox + n * dx, base + 20, str(n), "tm", fs=14))
    els.append(A(195, 140, 232, 140, "e2", 1))
    ox2, dx2, sc2 = 380, 30, 15
    rows = [(85, {-1: 2.0}, "2δ[n+1]"), (165, {0: 3.0}, "3δ[n]"), (245, {1: 1.0}, "δ[n-1]")]
    for i, (bs, vals, lab) in enumerate(rows, start=1):
        els.append(L(310, bs, 455, bs, "e", i))
        els.append(STEMS(ox2, bs, dx2, vals, sc2, b=i, nrange=range(-2, 3)))
        els.append(T(300, bs - 4, lab, "tb", i, fs=15, a="end"))
    return fig("신호 하나 = 손뼉 세 개의 합", els,
               "왼쪽 $x[n]$ 을 칸마다 떼어 내면 크기 2, 3, 1인 [[단위 임펄스]] 세 개가 돼요. 오른쪽 셋을 더하면 다시 왼쪽이에요.")


def fig_staircase():
    ox, oy, sx, sy = 50, 230, 80, 100
    f = lambda t: 1 + 0.5 * math.sin(1.2 * t)
    els = [L(ox, oy, 465, oy), L(ox, oy, ox, 30)]
    for k in range(10):
        t0 = k * 0.5
        hgt = f(t0) * sy
        els.append(R(ox + t0 * sx, oy - hgt, 0.5 * sx, hgt, "n3", 1, rx=0))
    curve = [(ox + t * sx, oy - f(t) * sy) for t in np.linspace(0, 5, 101)]
    els.append(PL(curve, "e2", 2))
    els.append(T(ox + 20, oy + 20, "Δ", "tb", 1, fs=15))
    els.append(T(460, oy + 20, "t", "tm", fs=14, a="end"))
    els.append(T(ox + 8, 44, "x(t)", "tm", fs=14, a="start"))
    els.append(T(300, 40, "막대 넓이 = x(kΔ) × Δ", "tb", 3, fs=15))
    els.append(T(300, 62, "Δ → 0 이면 합이 적분", "t", 3, fs=15))
    return fig("얇은 막대로 연속시간 신호 쌓기 (p.35)", els,
               r"폭 $\Delta$ 막대의 넓이를 모두 더하면 곡선 아래 넓이에 가까워져요. $\Delta\to 0$ 이면 [[적분|이에요/예요]].")


UNITS.append(unit(
    "w3-2", "임펄스로 신호 나타내기",
    "어떤 신호든 [[단위 임펄스]]의 합으로 쓰고, [[선형성|과/와]] [[시불변성]] 덕분에 출력이 [[임펄스 응답]]으로 정해지는 과정을 말할 수 있어요.",
    ["단위 임펄스", "선별 성질", "선형성", "시불변성", "중첩 원리", "임펄스 응답", "LTI 시스템", "적분"],
    [
        title("신호를 손뼉으로 쪼개기", "임펄스로 신호 나타내기 (p.10~17, p.34~38)"),
        goal("어떤 신호든 크기가 다른 [[단위 임펄스]]들의 합이라는 걸 말해요.",
             "[[선별 성질]] 식을 우리말로 읽어요.",
             "[[선형성|과/와]] [[시불변성]] 덕분에 [[임펄스 응답]] 하나로 출력을 쓰는 과정을 따라가요."),
        pts("앞 단원에서 이어서",
            "앞에서 본 [[단위 임펄스|은/는]] $n=0$ 에서만 1인 손뼉 한 번이었죠.",
            "[[단위 계단|은/는]] 스위치를 켜는 순간, 켠 뒤로 계속 1이었어요.",
            "주문: " + MANTRA1,
            "2장의 목표는 [[LTI 시스템]]의 출력을 쉽게 구하는 법이에요. 교수님: 오늘은 컨볼루션만 이해하면 다 돼요."),
        ana("손뼉 여러 번으로 만든 신호",
            "칸마다 손뼉을 한 번씩, 세기를 다르게 쳐요. 첫 칸은 약하게, 둘째 칸은 세게, 셋째 칸은 살짝 쳐요. 이 손뼉들을 차례로 모아 들으면 원래 신호가 돼요.",
            ["손뼉 한 번", r"[[단위 임펄스]] $\delta[n-k]$"],
            ["손뼉의 세기", "그 칸의 값 $x[k]$"],
            ["손뼉들을 모아 듣기", r"모두 더하기 $\sum_k$"]),
        fig_decompose(),
        stp("손계산: 신호를 손뼉으로 쓰기", "$x[-1]=2$, $x[0]=3$, $x[1]=1$, 나머지 칸은 0",
            [r"칸 $n=-1$: 왼쪽으로 1칸 옮긴 손뼉에 2를 곱해 $2\delta[n+1]$.",
             r"칸 $n=0$: $3\delta[n]$.",
             r"칸 $n=1$: $1\cdot\delta[n-1]$.",
             r"모두 더하면 $x[n]=2\delta[n+1]+3\delta[n]+\delta[n-1]$.",
             r"확인: $n=0$ 을 넣으면 $2\cdot 0+3\cdot 1+1\cdot 0=3=x[0]$."],
            "각 칸의 값이 그 칸 손뼉의 크기가 돼요. 이게 [[선별 성질|이에요/예요]]."),
        frm("선별 성질 (p.14)",
            r"x[n]=\sum_{k=-\infty}^{\infty} x[k]\,\delta[n-k]",
            [(r"x[n]", "우리가 나타내고 싶은 신호"),
             (r"\sum_{k=-\infty}^{\infty}", "시그마: k 를 음의 무한대부터 양의 무한대까지 바꾸며 모두 더해요"),
             (r"x[k]", "k 번째 칸의 실제 값(actual value), 손뼉의 세기"),
             (r"\delta[n-k]", "k 칸에서만 1인 손뼉, 시간 이동된 [[단위 임펄스]]")],
            "신호 = (칸의 값) × (그 칸의 손뼉)을 모두 더한 것. 이걸 [[선별 성질|이라고/라고]] 해요."),
        pts("선형 시스템에 넣으면 (p.15, p.20)",
            r"입력 $\delta[n-k]$ 에 대한 출력을 $h_k[n]$ 이라고 써요.",
            "[[선형성|은/는]] 더해 넣으면 더해 나오고 k배 넣으면 k배 나오는 성질, 즉 [[중첩 원리|예요/이에요]].",
            r"그래서 입력이 손뼉들의 합이면 출력은 메아리들의 합: $y[n]=\sum_k x[k]\,h_k[n]$.",
            "[[시불변성|이/가]] 없으면 $h_k[n]$ 모양이 칸마다 달라도 돼요(p.21 예)."),
        pts("시불변이면 메아리 하나로 끝 (p.16, p.22)",
            "[[시불변성|은/는]] 월요일에 해도 금요일에 해도 맛이 같은 레시피예요.",
            "늦게 친 손뼉의 메아리는 모양은 같고 늦게 나올 뿐: $h_k[n]=h[n-k]$.",
            "0번 칸의 메아리 $h_0[n]$ 만 알면 돼요. 이걸 그냥 $h[n]$, [[임펄스 응답|이라고/라고]] 불러요.",
            "주문: " + MANTRA2),
        frm("컨볼루션 합의 탄생 (p.17)",
            r"y[n]=\sum_{k=-\infty}^{\infty} x[k]\,h[n-k]=x[n]*h[n]",
            [(r"x[k]", "k 칸 손뼉의 세기"),
             (r"h[n-k]", "k 칸에서 시작한 메아리, [[임펄스 응답]]을 k 칸 민 것"),
             (r"*", "별표: 컨볼루션 기호. 곱하기가 아니에요"),
             (r"y[n]", "출력 신호")],
            "[[LTI 시스템]]의 출력 = 손뼉마다 찍은 메아리 도장의 합. CNN 의 커널이 $h$ 와 비슷한 역할이에요(교수님)."),
        pts("연속시간도 같은 생각 (p.34~37)",
            r"연속시간 신호는 폭 $\Delta$ 인 얇은 막대들로 거의 똑같이 쌓을 수 있어요.",
            r"막대 하나는 높이 $x(k\Delta)$, 폭 $\Delta$ 인 직사각형이에요. 넓이 1인 펄스 $\delta_\Delta$ 를 써요.",
            r"$\Delta$ 를 0으로 보내면 시그마 합이 [[적분|으로/로]] 바뀌어요.",
            "[[적분|은/는]] 그래프 아래 넓이를 구하는 계산이에요."),
        fig_staircase(),
        stp("손계산: 막대 합이 적분에 다가가요", r"$x(t)=t$ 를 $t=0$ 부터 1까지. 진짜 넓이는 삼각형 $\frac12$",
            [r"$\Delta=0.25$: 막대 높이 $0, 0.25, 0.5, 0.75$ 의 합 $1.5$, 곱하기 $\Delta$ 는 $0.375$.",
             r"$\Delta=0.1$: 높이 $0, 0.1, \dots, 0.9$ 의 합 $4.5$, 곱하기 $0.1$ 은 $0.45$.",
             r"$\Delta$ 가 작아질수록 $0.375\to 0.45\to$ 정답 $0.5$ 에 다가가요."],
            r"$\Delta\to 0$ 이면 막대 합이 [[적분|이/가]] 돼요. 그래서 연속시간은 시그마 대신 적분을 써요."),
        frm("연속시간 선별 성질 (p.37~38)",
            r"x(t)=\int_{-\infty}^{\infty} x(\tau)\,\delta(t-\tau)\,d\tau",
            [(r"\int_{-\infty}^{\infty}", "[[적분]]: 음의 무한대부터 양의 무한대까지 넓이를 더해요"),
             (r"x(\tau)", r"시각 타우($\tau$)에서의 신호 값"),
             (r"\delta(t-\tau)", r"$\tau=t$ 에서만 켜지는 넓이 1인 손뼉"),
             (r"d\tau", "아주 얇은 폭")],
            r"연속시간의 [[선별 성질]]: 손뼉이 있는 한 점 $\tau=t$ 의 값 $x(t)$ 만 골라내요."),
        chk(r"$x[1]=7$, $x[2]=5$, $x[3]=9$ 일 때 $\sum_k x[k]\,\delta[2-k]$ 는?",
            ["$5$", "$7$", "$21$", "$0$"], 0,
            r"$\delta[2-k]$ 는 $k=2$ 에서만 1이라서 $x[2]=5$ 만 남아요. [[선별 성질]]이 골라내요."),
        chk("[[임펄스 응답]]의 뜻은?",
            ["[[단위 임펄스]]를 넣었을 때 나오는 출력", "[[단위 계단]]을 넣었을 때 나오는 출력",
             "입력과 출력이 같은 시스템", "신호 크기의 제곱을 모두 더한 값"], 0,
            r"$\delta[n]$ 을 넣고 나온 $h[n]$ 이에요. 손뼉 한 번의 메아리예요."),
        warn("헷갈리기 쉬운 점",
             "p.14 슬라이드는 'Shifting Property'라고 적었지만 교재 이름은 Sifting(골라내기)이에요. 용어는 [[선별 성질|이에요/예요]].",
             r"[[선형성]]([[중첩 원리]])만 있으면 $y=\sum_k x[k]h_k[n]$ 까지예요. $h[n-k]$ 로 바꾸려면 [[시불변성|이/가]] 꼭 있어야 해요."),
        recap(r"어떤 신호든 [[단위 임펄스]]의 합: $x[n]=\sum_k x[k]\delta[n-k]$, [[선별 성질|이에요/예요]].",
              "[[선형성]]([[중첩 원리]])으로 출력은 메아리의 합, [[시불변성|으로/로]] 메아리가 모두 $h[n-k]$.",
              "그래서 [[LTI 시스템|은/는]] [[임펄스 응답]] 하나로 정해져요: $y=x*h$.",
              r"연속시간은 막대 폭 $\Delta\to 0$, 시그마가 [[적분|으로/로]] 바뀌어요."),
    ]))

# ================================================================ w3-3 컨볼루션 합 (p.18~33)
def conv_dict(xd, hd):
    out = {}
    for k, xv in xd.items():
        for m, hv in hd.items():
            out[k + m] = out.get(k + m, 0.0) + xv * hv
    return out


X21 = {-2: 0, -1: 0, 0: 0.5, 1: 2, 2: 0, 3: 0, 4: 0}     # p.26 목록 [0 0 0.5 2 0 0 0], 맨 앞 칸 n=-2
H21 = {-2: 0, -1: 0, 0: 1, 1: 1, 2: 1, 3: 0, 4: 0}       # p.26 목록 [0 0 1 1 1 0 0]
Y21 = conv_dict(X21, H21)
assert [Y21.get(n, 0) for n in range(-2, 5)] == [0, 0, 0.5, 2.5, 2.5, 2, 0]
ECHO1 = {n: 0.5 * H21.get(n, 0) for n in range(-2, 5)}
ECHO2 = {n: 2 * H21.get(n - 1, 0) for n in range(-2, 5)}
assert all(ECHO1[n] + ECHO2[n] == Y21.get(n, 0) for n in range(-2, 5))
_y2 = sum(X21.get(k, 0) * H21.get(2 - k, 0) for k in range(-5, 6))
assert _y2 == 2.5 and [H21.get(2 - k, 0) for k in range(-1, 4)] == [0, 1, 1, 1, 0]
assert [k for k in range(-5, 6) if H21.get(-k, 0)] == [-2, -1, 0]
assert conv([1, 2, 3], [1, 1]) == [1, 3, 5, 3]
AL = 0.5
Y23 = [sum(AL ** k for k in range(n + 1)) for n in range(4)]
assert Y23 == [1, 1.5, 1.75, 1.875]
assert all(abs(Y23[n] - (1 - AL ** (n + 1)) / (1 - AL)) < 1e-12 for n in range(4))
assert abs((1 - 0.0625) / 0.5 - 1.875) < 1e-12 and 1 / (1 - AL) == 2
_x24 = {n: 1.0 for n in range(5)}
_h24 = {n: 1.2 ** n for n in range(7)}          # 그림처럼 커지는 h (alpha>1 의 예)
_y24 = conv_dict(_x24, _h24)
assert min(_y24) == 0 and max(_y24) == 10 and max(_y24, key=_y24.get) == 6
_y25 = lambda n: sum(2.0 ** k for k in range(-60, min(n, 0) + 1))
assert abs(_y25(0) - 2) < 1e-12 and abs(_y25(3) - 2) < 1e-12 and abs(_y25(-1) - 1) < 1e-12 and abs(_y25(-2) - 0.5) < 1e-12
_h07 = [0.7 ** n for n in range(6)]
_h13 = [1.3 ** n for n in range(6)]
assert _h07[1] == 0.7 and _h13[5] > 3.7


def fig_echo():
    ox, dx = 150, 45
    els = []
    rows = [(60, ECHO1, "0.5h[n]", 1), (150, ECHO2, "2h[n-1]", 2), (280, {n: Y21.get(n, 0) for n in range(-2, 5)}, "y[n]", 3)]
    for base, vals, lab, b in rows:
        els.append(L(45, base, 335, base, "e", b))
        els.append(STEMS(ox, base, dx, vals, 22, b=b, nrange=range(-2, 5)))
        els.append(T(348, base - 6, lab, "tb", b, fs=15, a="start"))
    for n in range(0, 4):
        v = Y21[n]
        els.append(T(ox + n * dx + 10, 280 - v * 22 - 4, "%g" % v, "t", 3, fs=14, a="start"))
    els.append(T(ox + 8, 44, "0.5", "t", 1, fs=14, a="start"))
    els.append(T(ox + dx + 10, 104, "2", "t", 2, fs=14, a="start"))
    for n in range(-2, 5):
        els.append(T(ox + n * dx, 297, str(n), "tm", fs=14))
    els.append(T(22, 108, "+", "tb", 2, fs=20))
    els.append(T(22, 222, "=", "tb", 3, fs=20))
    return fig("메아리 관점: 도장 두 개를 더해요 (Example 2.1)", els,
               "손뼉 $0.5$ 는 $0.5h[n]$, 1칸 늦은 손뼉 $2$ 는 $2h[n-1]$ 을 찍어요. 칸마다 더하면 $y[n]$ 이에요.", h=300)


def fig_flip():
    ox, dx = 200, 40
    els = [L(60, 95, 365, 95), L(60, 200, 365, 200)]
    els.append(T(20, 62, "x[k]", "tb", fs=15, a="start"))
    els.append(STEMS(ox, 95, dx, {0: 0.5, 1: 2}, 25, nrange=range(-3, 5)))
    els.append(T(ox - 22, 86, "0.5", "t", fs=14, a="end"))
    els.append(T(ox + dx + 22, 52, "2", "t", fs=14, a="start"))
    els.append(STEMS(ox, 200, dx, {-2: 1, -1: 1, 0: 1}, 40, b=1, line="e", dot="n", zero=False))
    els.append(T(372, 150, "h[-k] 뒤집기", "t", 1, fs=14, a="start"))
    els.append(STEMS(ox, 200, dx, {0: 1, 1: 1, 2: 1}, 40, b=2, zero=False))
    els.append(STEMS(ox, 200, dx, {}, 40, nrange=[-3, 3, 4]))
    els.append(T(372, 176, "h[2-k] 밀기", "tb", 2, fs=14, a="start"))
    for k in range(-3, 5):
        els.append(T(ox + k * dx, 219, str(k), "tm", fs=14))
    els.append(T(ox + 180, 240, "k", "tm", fs=14))
    els.append(R(ox - 16, 32, dx + 32, 176, "hl", 3))
    els.append(T(425, 40, "겹친 칸 곱하기", "tb", 3, fs=14))
    els.append(T(425, 64, "0.5×1 + 2×1", "t", 3, fs=14))
    els.append(T(425, 88, "= 2.5 = y[2]", "tb", 3, fs=15))
    return fig("뒤집고, 밀고, 곱하고, 더하기 ($n=2$)", els,
               "$h[k]$ 를 뒤집어 $h[-k]$, 2칸 밀어 $h[2-k]$. 네모 안에서 겹친 칸만 곱해 더하면 $y[2]=2.5$ 예요.")


UNITS.append(unit(
    "w3-3", "컨볼루션 합",
    "[[컨볼루션 합|을/를]] 메아리 관점과 뒤집고 미는 관점으로 손계산하고, Example 2.1 과 2.3 의 답을 낼 수 있어요.",
    ["임펄스 응답", "컨볼루션", "컨볼루션 합", "LTI 시스템", "시간 반전", "시간 이동", "등비급수", "단위 계단"],
    [
        title("컨볼루션 합 손으로 풀기", "뒤집고, 밀고, 곱하고, 더하기 (p.18~33)"),
        goal("[[컨볼루션 합|을/를]] 두 관점(메아리 더하기, 미끄러뜨리기)으로 계산해요.",
             "Example 2.1 의 $y[n]$ 표를 끝까지 채워요.",
             "Example 2.3 을 [[등비급수|으로/로]] 풀어요."),
        pts("앞 단원에서 이어서",
            "[[임펄스 응답]] $h[n]$ 은 손뼉 한 번의 메아리였죠.",
            r"[[LTI 시스템]]의 출력은 $y[n]=\sum_k x[k]\,h[n-k]=x[n]*h[n]$ 이었어요.",
            "주문: " + MANTRA2),
        ana("메아리 도장 찍기",
            "빈 방에서 손뼉을 치면 메아리가 울려요. 손뼉을 여러 번, 세기를 다르게 치면 메아리도 크기를 달리해 겹쳐요. 메아리 모양 도장을 손뼉 자리마다 크기만큼 찍고 겹친 도장을 모두 더하면, 방에서 들리는 소리가 돼요.",
            ["손뼉 한 칸", "입력 한 칸 $x[k]$"],
            ["메아리 모양 도장", "[[임펄스 응답]] $h[n-k]$"],
            ["겹친 도장 모두 더하기", "[[컨볼루션]] $y[n]$"]),
        pts("시스템의 신분증 h[n] (p.18~19)",
            "$n=0$ 에서 시스템을 한 번 톡 치고(kick) 나오는 출력을 보는 게 [[임펄스 응답|이에요/예요]].",
            "p.19: $y[n]=x[n]+0.5x[n-1]+0.25x[n-2]$ 의 $h[n]$ 은 $1, 0.5, 0.25$ 로 끝나요.",
            "$y[n]=x[n]+0.7y[n-1]$ 은 $0.7^n$ 으로 끝없이 줄고, $1.3$ 이면 $1.3^n$ 으로 끝없이 커져요.",
            "$h[n]$ 모양만 봐도 시스템 성질이 보여요. 차분방정식 계수와도 바로 이어져요(p.25)."),
        stp("Example 2.1: 메아리 관점 (p.26)", "$h[0]=h[1]=h[2]=1$, $x[0]=0.5$, $x[1]=2$, 나머지 0. 슬라이드 목록 맨 앞 칸이 $n=-2$",
            [r"입력은 손뼉 두 번: $x[n]=0.5\delta[n]+2\delta[n-1]$.",
             "첫 메아리 $0.5h[n]$: $n=0,1,2$ 에서 $0.5$.",
             "둘째 메아리 $2h[n-1]$: 1칸 늦게 $n=1,2,3$ 에서 $2$.",
             "칸별로 더해요: $y[0]=0.5$, $y[1]=0.5+2=2.5$, $y[2]=0.5+2=2.5$, $y[3]=2$.",
             "그 밖의 칸은 0이에요."],
            r"$y[n]=[0\ \ 0\ \ 0.5\ \ 2.5\ \ 2.5\ \ 2\ \ 0]$ ($n=-2$ 부터). 슬라이드 답과 같아요."),
        fig_echo(),
        cmp("Example 2.1 표로 정리", ["$n$", "$0.5h[n]$", "$2h[n-1]$", "$y[n]$"], [
            ["$0$", "$0.5$", "$0$", "$0.5$"],
            ["$1$", "$0.5$", "$2$", "$2.5$"],
            ["$2$", "$0.5$", "$2$", "$2.5$"],
            ["$3$", "$0$", "$2$", "$2$"],
            ["$4$", "$0$", "$0$", "$0$"]]),
        pts("계산 순서 4단계 (p.24)",
            "1. 뒤집기: $h[k]$ 를 $k=0$ 기준으로 좌우로 뒤집어 $h[-k]$. [[시간 반전|이에요/예요]].",
            "2. 밀기: $n$ 칸 옮겨 $h[n-k]$. [[시간 이동|이에요/예요]]. $n>0$ 이면 오른쪽!",
            r"3. 곱하기: 칸마다 $x[k]\,h[n-k]$.",
            "4. 더하기: 모든 $k$ 에 대해 더하면 $y[n]$ 한 칸이 완성돼요."),
        fig_flip(),
        stp("뒤집고 밀기로 y[2] 한 칸 구하기", "Example 2.1, $n=2$",
            ["뒤집기: $h[-k]$ 는 $k=-2,-1,0$ 에서 1.",
             "밀기: 오른쪽으로 2칸, $h[2-k]$ 는 $k=0,1,2$ 에서 1.",
             r"곱하기: $k=0$ 은 $0.5\times 1$, $k=1$ 은 $2\times 1$, $k=2$ 는 $0\times 1$.",
             "더하기: $0.5+2+0=2.5$."],
            "$y[2]=2.5$. 메아리 관점과 같은 답이에요."),
        stp("표 방법: 짧은 두 수열", "$x=[1,2,3]$, $h=[1,1]$ (둘 다 $n=0$ 부터)",
            [r"$x$ 의 각 칸이 $h$ 전체를 곱해요: $1\cdot[1,1]$, $2\cdot[1,1]$, $3\cdot[1,1]$.",
             "한 줄씩 1칸 늦춰 적어요: $[1,1,0,0]$, $[0,2,2,0]$, $[0,0,3,3]$.",
             "세로로 더해요: $[1,3,5,3]$.",
             "길이 확인: $3+2-1=4$칸."],
            "$y=[1,3,5,3]$ ($n=0$ 부터). 줄마다 메아리 도장 하나예요."),
        pts("두 관점 (p.27, 교수님: 둘 다 중요)",
            "관점 1: $k$ 를 먼저 고정. 손뼉 하나가 모든 출력 칸에 남기는 메아리를 구해 모두 더해요.",
            "관점 2: $n$ 을 먼저 고정. $h$ 를 뒤집어 밀어 가며 출력 한 칸씩 채워요(슬라이딩).",
            "두 관점은 같은 [[컨볼루션 합|을/를]] 다른 순서로 더할 뿐이에요.",
            "관점 2는 CNN 에서 필터를 밀어 가는 모습과 비슷해요(교수님)."),
        stp(r"Example 2.3 ($\alpha=0.5$) (p.29~31)", r"$h[n]=u[n]$ ([[단위 계단]]), $x[n]=\alpha^n u[n]$, $\alpha=0.5$",
            [r"$h[n-k]=u[n-k]$ 는 $k\le n$ 에서 1이라서 $y[n]=\sum_{k=0}^{n}\alpha^k$ ($n\ge 0$).",
             "$y[0]=1$, $y[1]=1+0.5=1.5$.",
             "$y[2]=1.5+0.25=1.75$, $y[3]=1.75+0.125=1.875$.",
             r"[[등비급수]] 공식 $\frac{1-\alpha^{n+1}}{1-\alpha}$: $n=3$ 이면 $\frac{1-0.0625}{0.5}=1.875$, 같아요.",
             "$n<0$ 이면 겹치는 칸이 없어 $y[n]=0$."],
            r"$y[n]=\left(\frac{1-\alpha^{n+1}}{1-\alpha}\right)u[n]$. $n$ 이 커지면 $\frac{1}{1-\alpha}=2$ 에 다가가요."),
        pts("Example 2.4, 2.5 (p.32~33)",
            r"2.4: $x$ 는 $0\le n\le 4$ 에서 1, $h=\alpha^n$ 은 $0\le n\le 6$. 겹치는 범위를 나눠 계산해요.",
            r"2.4 결과는 $0\le n\le 10$ 에서만 값이 있고, 그림에서 $n=6$ 일 때 가장 커요.",
            r"2.5: $x[n]=2^n u[-n]$, $h=u[n]$ ([[단위 계단]]). $y[0]=1+\frac12+\frac14+\cdots=2$, $n\ge 0$ 이면 계속 2, $n<0$ 이면 $2^{n+1}$.",
            "교수님: 범위 나누기가 핵심이니 과제든 퀴즈든 손계산을 연습해 보세요."),
        chk("Example 2.1 에서 $y[1]$ 은?", ["$0.5$", "$2$", "$2.5$", "$3$"], 2,
            r"$x[0]h[1]+x[1]h[0]=0.5\times 1+2\times 1=2.5$ 예요."),
        chk("[[컨볼루션 합|을/를]] 한 칸 구하는 순서로 맞는 것은?",
            ["뒤집고, 밀고, 곱하고, 더한다", "더하고, 곱하고, 밀고, 뒤집는다", "미분하고 적분한다", "두 신호를 칸끼리 곱하기만 한다"], 0,
            "[[시간 반전]] → [[시간 이동]] → 곱하기 → 더하기. 주문 그대로예요."),
        recap(r"[[LTI 시스템]]의 [[컨볼루션 합]] $y[n]=\sum_k x[k]h[n-k]$: 손뼉마다 메아리 도장을 찍어 더해요.",
              "순서: [[시간 반전]] → [[시간 이동]] → 곱하기 → 더하기. 별표 $*$ 는 곱하기가 아니라 [[컨볼루션|이에요/예요]].",
              r"Example 2.1: $y=[0.5,\ 2.5,\ 2.5,\ 2]$ ($n=0\sim 3$). 표 방법 $[1,2,3]*[1,1]=[1,3,5,3]$.",
              r"Example 2.3: [[단위 계단|과/와]] $0.5^n u[n]$ → $1, 1.5, 1.75, 1.875 \to 2$, [[등비급수|예요/이에요]]."),
    ]))

# ================================================================ w3-4 컨볼루션 적분 (p.39~49)
def _integrate(f, a, b, n=200000):
    t = np.linspace(a, b, n + 1)
    v = f(t)
    return float(np.sum((v[1:] + v[:-1]) / 2) * (b - a) / n)


Y26_1 = _integrate(lambda tau: np.exp(-tau), 0, 1)
assert abs(Y26_1 - (1 - math.exp(-1))) < 1e-9 and abs(Y26_1 - 0.632) < 5e-4
Y28 = lambda t: 0.5 * math.exp(2 * (t - 3)) if t < 3 else 0.5
assert abs(_integrate(lambda tau: np.exp(2 * tau), -40, -1) - Y28(2)) < 1e-8 and abs(Y28(2) - 0.068) < 5e-4
assert abs(_integrate(lambda tau: np.exp(2 * tau), -40, 0) - Y28(5)) < 1e-8 and Y28(5) == 0.5


def _y27(t, T=1.0):
    x = lambda tau: ((tau > 0) & (tau < T)).astype(float)
    h = lambda s: np.where((s > 0) & (s < 2 * T), s, 0.0)
    return _integrate(lambda tau: x(tau) * h(t - tau), -1, 4, 400000)


assert abs(_y27(0.5) - 0.125) < 1e-3 and abs(0.5 * 0.5 ** 2 - 0.125) < 1e-12
assert abs(_y27(1.5) - 1.0) < 1e-3 and abs(1 * 1.5 - 0.5 - 1.0) < 1e-12
assert abs(_y27(2.5) - 0.875) < 1e-3 and abs(-0.5 * 2.5 ** 2 + 2.5 + 1.5 - 0.875) < 1e-12
assert abs(_y27(3.5)) < 1e-3 and abs(_y27(-0.5)) < 1e-3


def fig_sliding():
    ox, oy, sx, sy = 150, 200, 60, 120
    tau = np.linspace(0, 4, 81)
    curve = [(ox, oy)] + [(ox + t * sx, oy - math.exp(-t) * sy) for t in tau]
    shade = [(ox, oy)] + [(ox + t * sx, oy - math.exp(-t) * sy) for t in np.linspace(0, 1, 21)] + [(ox + sx, oy)]
    els = [L(25, oy, 450, oy), L(ox, oy, ox, 40, "e")]
    els.append(PG(shade, "n3", 2))
    els.append(PL([(30, oy - sy), (ox + sx, oy - sy), (ox + sx, oy)], "e", 1))
    els.append(PL(curve, "e2"))
    els.append(T(250, 128, "x(τ) = e^(-τ)", "tb", fs=15, a="start"))
    els.append(T(40, 70, "h(1-τ)", "tb", 1, fs=15, a="start"))
    els.append(T(ox, oy + 18, "0", "tm", fs=14))
    els.append(T(ox + sx, oy + 18, "1", "tm", fs=14))
    els.append(T(445, oy + 18, "τ", "tm", fs=14))
    els.append(T(345, 40, "겹친 넓이 = y(1)", "tb", 2, fs=15))
    els.append(T(345, 64, "= 1 - e^(-1) ≈ 0.632", "t", 3, fs=15))
    els.append(A(215, 240, 262, 240, "e2", 3))
    els.append(T(272, 245, "t 가 커지면 도장이 오른쪽으로", "t", 3, fs=14, a="start"))
    return fig("도장 띠를 밀어 겹친 넓이 재기 (Example 2.6, $t=1$)", els,
               "뒤집고 민 [[단위 계단]] $h(1-\\tau)$ 와 $x(\\tau)=e^{-\\tau}$ 가 겹친 초록 넓이가 $y(1)\\approx 0.632$ 예요.")


def fig_ex28():
    ox, oy, sx, sy = 130, 220, 40, 240
    ts = np.linspace(-2, 6, 161)
    curve = [(ox + t * sx, oy - Y28(t) * sy) for t in ts]
    x2, y2 = ox + 2 * sx, oy - Y28(2) * sy
    x5, y5 = ox + 5 * sx, oy - Y28(5) * sy
    els = [L(40, oy, 400, oy), L(ox, oy, ox, 60)]
    els.append(T(ox - 6, oy - 0.5 * sy + 5, "1/2", "tm", fs=14, a="end"))
    els.append(L(ox, oy - 0.5 * sy, 390, oy - 0.5 * sy, "e"))
    els.append(PL(curve, "e2", 1))
    els.append(T(ox + 8, 72, "y(t)", "tm", fs=14, a="start"))
    els.append(L(ox + 3 * sx, oy, ox + 3 * sx, 80, "e", 3))
    els.append(T(ox + 3 * sx + 6, 78, "t=3 분기점", "tb", 3, fs=14, a="start"))
    els.append(C(x2, y2, 5, "n2", 2))
    els.append(T(140, 185, "y(2) ≈ 0.068", "t", 2, fs=14, a="start"))
    els.append(C(x5, y5, 5, "n2", 2))
    els.append(T(x5 + 8, y5 + 22, "y(5) = 0.5", "t", 2, fs=14, a="start"))
    for t in (0, 2, 3, 5):
        els.append(T(ox + t * sx, oy + 18, str(t), "tm", fs=14))
    els.append(T(415, oy + 18, "t", "tm", fs=14))
    return fig("Example 2.8 의 출력 $y(t)$", els,
               "$t<3$ 에서는 $\\frac12e^{2(t-3)}$ 로 올라가다가 $t=3$ 부터 $\\frac12$ 로 멈춰요.")


UNITS.append(unit(
    "w3-4", "컨볼루션 적분",
    "[[컨볼루션 적분]] 식을 우리말로 읽고, Example 2.6 과 2.8 을 쉬운 숫자로 계산할 수 있어요.",
    ["컨볼루션 적분", "적분", "연속시간 신호", "지수함수", "단위 계단", "임펄스 응답", "컨볼루션"],
    [
        title("컨볼루션 적분", "연속시간은 시그마 대신 적분 (p.39~49)"),
        goal("[[연속시간 신호]]의 [[컨볼루션 적분]] 식을 우리말로 읽어요.",
             "Example 2.6 을 $a=1$, $t=1$ 로 계산해요.",
             "Example 2.8 을 $t=2$, $t=5$ 에서 계산하고 범위 나누기를 익혀요."),
        pts("앞 단원에서 이어서",
            "앞에서 [[컨볼루션 합|은/는]] 뒤집고, 밀고, 곱하고, 더했죠.",
            "[[연속시간 신호|은/는]] 더하기가 [[적분|으로/로]] 바뀔 뿐 나머지는 같아요(p.40~42).",
            "교수님: 증명을 다 알 필요는 없고 '시그마가 적분으로 바뀐다'만 기억하면 돼요.",
            "교수님: 이산시간이 연속시간보다 훨씬 쉬우니 이산시간부터 확실히 해 두세요.",
            "주문: " + MANTRA2),
        ana("매끈한 도장 띠 밀기",
            "이번 도장은 칸칸이 떨어진 도장이 아니라 매끈한 띠 모양이에요. 뒤집은 띠를 왼쪽에서 오른쪽으로 천천히 밀어요. 띠가 입력 그래프와 겹친 부분의 넓이를 재면 그 순간의 출력이에요.",
            ["매끈한 도장 띠", "뒤집고 민 [[임펄스 응답]] $h(t-\\tau)$"],
            ["겹친 부분의 넓이", "[[적분]] $\\int x(\\tau)h(t-\\tau)\\,d\\tau$"],
            ["띠를 민 위치", "출력 시각 $t$"]),
        frm("컨볼루션 적분 (p.42)",
            r"y(t)=\int_{-\infty}^{\infty} x(\tau)\,h(t-\tau)\,d\tau=x(t)*h(t)",
            [(r"\tau", "타우: 적분하며 움직이는 시간 변수, 이산시간의 k 역할"),
             (r"x(\tau)", "입력"),
             (r"h(t-\tau)", "[[임펄스 응답]]을 뒤집고 t 만큼 민 것"),
             (r"d\tau", "아주 얇은 폭"),
             (r"\int_{-\infty}^{\infty}", "곱한 값의 넓이를 모두 더해요")],
            "[[컨볼루션 적분|은/는]] 겹친 곱의 넓이예요. 중첩 적분(superposition integral)이라고도 불러요."),
        pts("계산 순서는 그대로 (p.44)",
            "1. $h(\\tau)$ 를 뒤집어 $h(-\\tau)$.",
            "2. $t$ 만큼 밀어 $h(t-\\tau)$.",
            "3. $x(\\tau)$ 와 곱해요.",
            "4. $\\tau$ 에 대해 [[적분|하면/하면]] $y(t)$ 한 점이 나와요."),
        fig_sliding(),
        stp("Example 2.6 ($a=1$, $t=1$) (p.45~46)", "$x(t)=e^{-at}u(t)$, $h(t)=u(t)$, $a=1$",
            ["$h(1-\\tau)=u(1-\\tau)$ 는 $\\tau<1$ 에서 1이에요. 뒤집고 1만큼 민 [[단위 계단|이에요/예요]].",
             "$x(\\tau)=e^{-\\tau}$ 는 $\\tau>0$ 에서만 있는 줄어드는 [[지수함수|예요/이에요]]. 둘이 겹치는 곳은 $0<\\tau<1$.",
             "$y(1)=\\int_0^1 e^{-\\tau}\\,d\\tau=\\left[-e^{-\\tau}\\right]_0^1$.",
             "$=-e^{-1}+1=1-0.368=0.632$."],
            "$y(1)=1-e^{-1}\\approx 0.632$. 일반식은 $y(t)=\\frac1a\\left(1-e^{-at}\\right)u(t)$ 예요."),
        pts("Example 2.6 결과 읽기",
            "$t<0$ 이면 겹침이 없어서 $y(t)=0$.",
            "$t>0$ 이면 겹친 넓이가 커지지만, 늘어나는 폭은 점점 줄어요(교수님: 기울기가 줄어 포화).",
            "그래서 $\\frac1a$ 에 다가가며 멈춰요. 앞 단원 [[등비급수]] 예제(Example 2.3)와 닮은 모양이에요.",
            "[[지수함수]] $e^{-a\\tau}$ 가 줄어드는 신호라서 넓이가 끝없이 커지지 않아요."),
        stp("Example 2.8 ($t=2$, $t=5$) (p.49)", "$x(t)=e^{2t}u(-t)$, $h(t)=u(t-3)$",
            ["$h(t)$ 는 3만큼 늦춘 [[단위 계단|이에요/예요]]. 뒤집고 밀면 $h(t-\\tau)=u(t-\\tau-3)$, $\\tau<t-3$ 에서 1.",
             "$x(\\tau)=e^{2\\tau}$ 는 $\\tau<0$ 에서만 있어요. 두 범위가 겹치는 곳을 봐요.",
             "$t=2$: $t-3=-1<0$, 겹침은 $\\tau<-1$. $y(2)=\\int_{-\\infty}^{-1}e^{2\\tau}d\\tau=\\frac12e^{-2}\\approx 0.068$.",
             "$t=5$: $t-3=2\\ge 0$, 겹침은 $\\tau<0$ 전체. $y(5)=\\int_{-\\infty}^{0}e^{2\\tau}d\\tau=\\frac12$."],
            "$t<3$ 이면 $y(t)=\\frac12e^{2(t-3)}$, $t\\ge 3$ 이면 $y(t)=\\frac12$. 분기점은 $t=3$ 이에요."),
        fig_ex28(),
        pts("Example 2.7: 범위 나누기 (p.47~48)",
            "$x$ 는 $0<t<T$ 에서 1, $h$ 는 $0<t<2T$ 에서 $t$ (비스듬한 선).",
            "겹침 없음 → 조금 겹침 → 많이 겹침 → 빠져나감 → 다시 없음, 이렇게 구간을 나눠요.",
            "답: $0$, $\\frac12t^2$, $Tt-\\frac12T^2$, $-\\frac12t^2+Tt+\\frac32T^2$, $0$ (경계 $0, T, 2T, 3T$).",
            "교수님: 범위를 나누는 게 핵심이고 계산은 직접 연습해 보세요."),
        stp("Example 2.7 을 $T=1$ 로 확인", "각 구간 식에 $T=1$ 을 넣어요",
            ["$t=0.5$ 는 $0<t<T$ 구간: $\\frac12(0.5)^2=0.125$.",
             "$t=1.5$ 는 $T<t<2T$ 구간: $1\\times 1.5-\\frac12=1$.",
             "$t=2.5$ 는 $2T<t<3T$ 구간: $-\\frac12(6.25)+2.5+1.5=0.875$.",
             "$t=3.5$ 는 $3T<t$ 라서 다시 $0$."],
            "구간마다 다른 식을 써요. 값이 이어지는지(연속인지) 보면 검산이 돼요."),
        chk("Example 2.8 에서 $t=5$ 일 때 $y(t)$ 는?",
            ["$\\frac12$", "$\\frac12e^{-2}$", "$0$", "무한대"], 0,
            "$t\\ge 3$ 이면 겹침이 $\\tau<0$ 전체라서 $\\int_{-\\infty}^0 e^{2\\tau}d\\tau=\\frac12$ 예요."),
        chk("[[컨볼루션 적분]]의 뜻은?",
            ["연속시간 [[컨볼루션]]: 뒤집고 민 $h$ 와 $x$ 의 곱을 [[적분|한/한]] 넓이", "이산시간 칸끼리의 합",
             "신호를 좌우로 뒤집는 것", "임펄스 하나의 높이"], 0,
            "2번은 [[컨볼루션 합|이에요/예요]]. 연속시간에서는 합이 넓이([[적분]])로 바뀌어요."),
        warn("헷갈리기 쉬운 점",
             "적분 안에서 움직이는 변수는 $\\tau$, 결과의 시각은 $t$. 둘을 섞지 않아요.",
             "$h(t-\\tau)$ 는 $\\tau$ 축에서 뒤집힌 뒤 $t$ 만큼 오른쪽으로 가요. $t$ 가 커지면 띠가 오른쪽으로 밀려요.",
             "p.49 첫 식 $\\frac12e^{2(t-3)}$ 은 $t<3$ 일 때만 맞아요. 슬라이드에 조건이 빠져 있어요."),
        recap("[[컨볼루션 적분]] $y(t)=\\int x(\\tau)h(t-\\tau)d\\tau$: [[연속시간 신호]]에서는 합 대신 넓이.",
              "순서는 같아요: 뒤집고, 밀고, 곱하고, [[적분|해요/해요]].",
              "Example 2.6: $y(1)=1-e^{-1}\\approx 0.632$, [[지수함수]] 모양으로 $\\frac1a$ 에 포화.",
              "Example 2.8: $y(2)=\\frac12e^{-2}\\approx 0.068$, $y(5)=\\frac12$. 범위 나누기가 핵심."),
    ]))

# ================================================================ w3-5 컨볼루션의 성질 (p.50~58)
_xm = {0: -1.0}                       # x[n] = -delta[n]
_lti = lambda x, n: x.get(n, 0) + x.get(n - 1, 0)
_sq = lambda x, n: (x.get(n, 0) + x.get(n - 1, 0)) ** 2
_mx = lambda x, n: max(x.get(n, 0), x.get(n - 1, 0))
_dl = {0: 1.0}
assert [_lti(_dl, n) for n in (0, 1, 2)] == [_sq(_dl, n) for n in (0, 1, 2)] == [_mx(_dl, n) for n in (0, 1, 2)] == [1, 1, 0]
assert [_lti(_xm, n) for n in (0, 1)] == [-1, -1]
assert [_sq(_xm, n) for n in (0, 1)] == [1, 1]
assert [_mx(_xm, n) for n in (0, 1)] == [0, 0]
assert conv([1, 2], [1, 1, 1]) == conv([1, 1, 1], [1, 2]) == [1, 3, 3, 2]
_h1, _h2 = [1, 1], [1, -1]
assert [a + b for a, b in zip(_h1, _h2)] == [2, 0]
assert conv([1, 2], [2, 0]) == [2, 4, 0]
assert conv([1, 2], _h1) == [1, 3, 2] and conv([1, 2], _h2) == [1, 1, -2]
assert [a + b for a, b in zip(conv([1, 2], _h1), conv([1, 2], _h2))] == [2, 4, 0]
assert conv(conv([1, 2], _h1), _h2) == [1, 2, -1, -2]
assert conv(_h1, _h2) == [1, 0, -1] and conv([1, 2], conv(_h1, _h2)) == [1, 2, -1, -2]
_y1 = lambda n: (1 - 0.5 ** (n + 1)) / 0.5 if n >= 0 else 0.0
_y2 = lambda n: 2.0 ** (n + 1) if n <= 0 else 2.0
assert _y1(0) + _y2(0) == 3 and abs(_y1(60) + _y2(60) - 4) < 1e-12
assert _y1(-1) + _y2(-1) == 1 and _y1(-2) + _y2(-2) == 0.5
assert (2 * 3) ** 2 == 36 and 2 * (3 ** 2) == 18


def fig_par_ser():
    els = [T(20, 18, "병렬 연결 = 분배 법칙", "tb", 1, fs=15, a="start")]
    els += [T(20, 85, "x[n]", "t", 1, fs=15, a="start"), L(56, 80, 80, 80, "e", 1), L(80, 50, 80, 110, "e", 1),
            A(80, 50, 113, 50, "e", 1), A(80, 110, 113, 110, "e", 1),
            BOX(113, 35, 72, 30, "h1[n]", "box", 1), BOX(113, 95, 72, 30, "h2[n]", "box", 1),
            L(185, 50, 215, 50, "e", 1), A(215, 50, 215, 67, "e", 1),
            L(185, 110, 215, 110, "e", 1), A(215, 110, 215, 93, "e", 1),
            ADDER(215, 80, 1), A(227, 80, 262, 80, "e2", 1), T(268, 85, "y[n]", "t", 1, fs=15, a="start"),
            T(318, 87, "=", "tb", 2, fs=20), BOX(336, 64, 128, 32, "h1[n] + h2[n]", "box2", 2, fs=15)]
    els += [T(20, 160, "직렬 연결 = 결합 법칙", "tb", 3, fs=15, a="start"),
            T(20, 220, "x[n]", "t", 3, fs=15, a="start"), A(56, 215, 85, 215, "e", 3),
            BOX(85, 200, 66, 30, "h1[n]", "box", 3), A(151, 215, 177, 215, "e", 3),
            BOX(177, 200, 66, 30, "h2[n]", "box", 3), A(243, 215, 264, 215, "e2", 3),
            T(268, 220, "y[n]", "t", 3, fs=15, a="start"),
            T(318, 222, "=", "tb", 4, fs=20), BOX(336, 199, 128, 32, "h1[n] * h2[n]", "box2", 4, fs=15),
            T(400, 262, "순서를 바꿔도 같아요", "tm", 4, fs=14)]
    return fig("병렬은 더하기, 직렬은 컨볼루션", els,
               "[[병렬 연결|은/는]] $h_1+h_2$ 상자 하나, [[직렬 연결|은/는]] $h_1*h_2$ 상자 하나와 같아요. LTI 일 때만이에요.")


UNITS.append(unit(
    "w3-5", "컨볼루션의 성질",
    "[[교환 법칙]], [[분배 법칙]], [[결합 법칙|을/를]] 작은 수열로 확인하고, [[병렬 연결|과/와]] [[직렬 연결|을/를]] 상자 하나로 바꿀 수 있어요.",
    ["교환 법칙", "분배 법칙", "결합 법칙", "병렬 연결", "직렬 연결", "컨볼루션", "임펄스 응답", "선형성"],
    [
        title("컨볼루션의 세 법칙", "교환, 분배, 결합 (p.50~58)"),
        goal("[[임펄스 응답|이/가]] 시스템을 다 말해 주는 건 LTI 일 때뿐임을 말해요.",
             "[[교환 법칙]], [[분배 법칙]], [[결합 법칙|을/를]] 작은 수열로 확인해요.",
             "[[병렬 연결|과/와]] [[직렬 연결|을/를]] 상자 하나로 바꿔요."),
        pts("앞 단원에서 이어서",
            "앞에서 [[컨볼루션 합|과/와]] [[컨볼루션 적분|을/를]] 손으로 계산했죠.",
            "이번에는 [[컨볼루션]] 계산 자체가 가진 성질이에요. 이산, 연속 둘 다 똑같이 성립해요.",
            "주문: " + MANTRA2),
        pts("LTI 일 때만 h 가 전부 (p.50~51)",
            "$h[n]=1$ ($n=0,1$) 인 LTI 시스템은 $y[n]=x[n]+x[n-1]$ 하나로 정해져요.",
            "그런데 $(x[n]+x[n-1])^2$ 과 $\\max(x[n],x[n-1])$ 도 [[임펄스 응답|이/가]] 똑같아요.",
            "이 둘은 [[선형성|이/가]] 없어요. 그래서 $h$ 만 보고는 어떤 시스템인지 몰라요.",
            "결론: $h$ 로 시스템을 대표하려면 반드시 LTI 여야 해요(교수님)."),
        stp("손계산: 같은 h, 다른 출력", "입력 $x[n]=-\\delta[n]$ (크기 $-1$ 인 손뼉)",
            ["LTI $x[n]+x[n-1]$: $y[0]=-1$, $y[1]=-1$.",
             "제곱 시스템: $y[0]=(-1)^2=1$, $y[1]=1$.",
             "max 시스템: $y[0]=\\max(-1,0)=0$, $y[1]=\\max(0,-1)=0$."],
            "[[임펄스 응답|은/는]] 셋 다 같은데 출력은 셋 다 달라요. [[선형성|이/가]] 없으면 $h$ 로 설명이 안 돼요."),
        ana("메아리 도장의 순서",
            "메아리 도장 두 개를 차례로 찍어도, 순서를 바꿔 찍어도 마지막 무늬는 같아요. 두 도장을 따로 찍어 결과를 더해도, 두 도장을 합친 도장 하나로 찍은 것과 같아요.",
            ["도장 순서 바꾸기", "[[교환 법칙]], [[결합 법칙]]"],
            ["따로 찍고 더하기", "[[분배 법칙]], [[병렬 연결]]"],
            ["도장을 차례로 찍기", "[[직렬 연결]]"]),
        frm("교환 법칙 (p.52~53)",
            r"x[n]*h[n]=h[n]*x[n]=\sum_{k=-\infty}^{\infty}h[k]\,x[n-k]",
            [(r"x[n]*h[n]", "입력을 두고 $h$ 를 뒤집어 밀기"),
             (r"h[n]*x[n]", "$h$ 를 두고 입력을 뒤집어 밀기"),
             (r"n-k=r", "바꿔 부르기(치환) 한 번이면 두 식이 같아져요")],
            "[[교환 법칙]]: 시그마 안이 곱하기라서 순서를 바꿔도 같아요(교수님). 더 쉬운 쪽을 뒤집으면 돼요."),
        stp("손계산: 교환 법칙", "$x=[1,2]$, $h=[1,1,1]$ (둘 다 $n=0$ 부터)",
            ["$x*h$: $1\\cdot[1,1,1]$ 과 한 칸 늦춘 $2\\cdot[1,1,1]$ 을 더하면 $[1,3,3,2]$.",
             "$h*x$: $[1,2]$ 를 세 줄, 한 칸씩 늦춰 더해도 $[1,3,3,2]$.",
             "두 결과가 칸마다 같아요."],
            "[[교환 법칙]] 확인: $x*h=h*x=[1,3,3,2]$."),
        frm("분배 법칙 (p.54)",
            r"x[n]*\big(h_1[n]+h_2[n]\big)=x[n]*h_1[n]+x[n]*h_2[n]",
            [(r"h_1+h_2", "두 시스템을 [[병렬 연결|한/한]] 뒤 출력을 더한 것"),
             (r"x*h_1", "첫째 가지의 출력 $y_1$"),
             (r"x*h_2", "둘째 가지의 출력 $y_2$")],
            "[[분배 법칙]]: 어려운 $h$ 를 쉬운 두 개로 쪼개 따로 풀고 더해도 돼요(교수님)."),
        stp("손계산: 분배 법칙", "$x=[1,2]$, $h_1=[1,1]$, $h_2=[1,-1]$",
            ["왼쪽: $h_1+h_2=[2,0]$, $x*(h_1+h_2)=[2,4,0]$.",
             "오른쪽: $x*h_1=[1,3,2]$, $x*h_2=[1,1,-2]$.",
             "더하면 $[1+1,\\ 3+1,\\ 2-2]=[2,4,0]$."],
            "양쪽이 같아요. [[병렬 연결|은/는]] $h_1+h_2$ 하나로 바꿀 수 있어요."),
        stp("손계산: 결합 법칙", "같은 $x=[1,2]$, $h_1=[1,1]$, $h_2=[1,-1]$",
            ["먼저 $x*h_1=[1,3,2]$, 그다음 $[1,3,2]*[1,-1]=[1,2,-1,-2]$.",
             "먼저 $h_1*h_2=[1,0,-1]$, 그다음 $x*[1,0,-1]=[1,2,-1,-2]$.",
             "괄호 위치가 달라도 답이 같아요."],
            "[[결합 법칙]]: [[직렬 연결|은/는]] $h_1*h_2$ 상자 하나와 같고, [[교환 법칙|까지/까지]] 쓰면 순서도 바꿀 수 있어요."),
        fig_par_ser(),
        pts("Example 2.10: 쪼개서 풀기 (p.56~57)",
            "$x[n]=0.5^nu[n]+2^nu[-n]$ 는 모든 칸에 값이 있어 한 번에 풀기 어려워요. $h[n]=u[n]$.",
            "[[분배 법칙|으로/로]] 둘로 쪼개요: $y_1=(0.5^nu[n])*u[n]$, $y_2=(2^nu[-n])*u[n]$.",
            "$y_1$ 은 Example 2.3, $y_2$ 는 Example 2.5 답을 그대로 가져와요.",
            "$y[0]=1+2=3$, $y[-1]=1$, $n$ 이 커지면 $2+2=4$ 에 다가가요(그림과 같아요)."),
        stp("LTI 가 아니면 순서가 중요 (p.58)", "$y_1=2x$ (2배), $y_2=x^2$ (제곱), 입력 $x=3$",
            ["2배 먼저, 제곱 나중: $2\\times 3=6$, $6^2=36$.",
             "제곱 먼저, 2배 나중: $3^2=9$, $2\\times 9=18$.",
             "36과 18, 결과가 달라요."],
            "제곱 시스템은 [[선형성|이/가]] 없어서 LTI 가 아니에요. 그래서 [[직렬 연결]] 순서를 바꿀 수 없어요."),
        chk("[[병렬 연결|된/된]] $h_1$, $h_2$ 를 상자 하나로 바꾸면?",
            ["$h_1+h_2$", "$h_1*h_2$", "$h_1-h_2$", "$h_1$ 만 남는다"], 0,
            "[[분배 법칙|이에요/예요]]. $h_1*h_2$ 는 [[직렬 연결|이에요/예요]]."),
        chk("[[결합 법칙]]을 나타낸 식은?",
            ["$(x*h_1)*h_2=x*(h_1*h_2)$", "$x*h=h*x$", "$x*(h_1+h_2)=x*h_1+x*h_2$", "$x*\\delta=x$"], 0,
            "2번은 [[교환 법칙]], 3번은 [[분배 법칙]], 4번은 항등 시스템이에요."),
        warn("슬라이드 오류와 헷갈리는 점",
             "p.55 제목은 Distributive 인데 식과 그림은 [[결합 법칙]]([[직렬 연결]])이에요. 연속시간 식도 양쪽이 똑같이 적혀 있어요.",
             "p.56~57 의 둘째 식 $y_1[n]=x_1[n]*h[n]$ 은 $y_2[n]=x_2[n]*h[n]$ 의 오타예요.",
             "수업 중에도 분배와 결합 이름이 한 번 바뀌어 불렸다가 고쳐졌어요. 분배 = 병렬(더하기), 결합 = 직렬(차례로)."),
        recap("[[교환 법칙]] $x*h=h*x$: 더 쉬운 쪽을 뒤집어요.",
              "[[분배 법칙]] = [[병렬 연결]]: $h_1+h_2$ 상자 하나. 어려운 입력도 쪼개서 풀어요.",
              "[[결합 법칙]] = [[직렬 연결]]: $h_1*h_2$ 상자 하나, 순서 바꿔도 같아요.",
              "모두 LTI 일 때만. [[선형성|이/가]] 없으면 [[임펄스 응답|으로/로]] 시스템을 설명할 수 없어요."),
    ]))

# ================================================================ w3-6 기억성, 가역성, 인과성 (p.59~67)
assert [3 * v for v in [1, 2, 3]] == [3, 6, 9]
assert conv([1, 2, 3], [0, 1]) == [0, 1, 2, 3]
_xa = [1, 2, 3, 0]
_ya = [float(v) for v in np.cumsum(_xa)]
assert _ya == [1, 3, 6, 6]
_wa = [_ya[0]] + [_ya[i] - _ya[i - 1] for i in range(1, 4)]
assert _wa == [1, 2, 3, 0]
assert conv([1] * 6, [1, -1])[:6] == [1, 0, 0, 0, 0, 0]     # u[n] * (d[n] - d[n-1]) = d[n]
_causal = lambda h: all(v == 0 for n, v in h.items() if n < 0)
assert _causal({1: 1}) and not _causal({-1: 1}) and _causal({n: 1 for n in range(0, 20)})
assert _causal({0: 1, 1: -1}) and not _causal({-2: 1})


def fig_acc_diff():
    els = [T(14, 65, "x[n]", "tb", fs=15, a="start"), A(50, 60, 75, 60, "e"),
           BOX(75, 40, 110, 40, "누산기", "box", 1), T(130, 100, "h = u[n]", "tm", 1, fs=14),
           A(185, 60, 245, 60, "e2", 1), T(215, 50, "y[n]", "t", 1, fs=14),
           BOX(245, 40, 110, 40, "1차 차분", "box", 2), T(300, 100, "δ[n] - δ[n-1]", "tm", 2, fs=14),
           A(355, 60, 400, 60, "e2", 2), T(405, 65, "x[n]", "tb", 2, fs=15, a="start"),
           T(240, 150, "u[n] * (δ[n] - δ[n-1]) = δ[n]", "tb", 3, fs=15),
           T(14, 205, "x[n]", "tb", 3, fs=15, a="start"), A(50, 200, 120, 200, "e", 3),
           BOX(120, 180, 240, 40, "δ[n]  항등 시스템", "box2", 3),
           A(360, 200, 400, 200, "e2", 3), T(405, 205, "x[n]", "tb", 3, fs=15, a="start"),
           T(240, 250, "되돌리기 버튼을 누른 것처럼 원래대로", "tm", 3, fs=14)]
    return fig("누산기 뒤에 1차 차분을 붙이면 (Example 2.12)", els,
               "[[누산기|이/가]] 쌓은 것을 [[1차 차분|이/가]] 한 칸씩 풀어서 원래 입력이 나와요. 둘은 서로의 [[역시스템|이에요/예요]].")


def fig_causal():
    ox, dx = 200, 40
    els = [R(ox - 3.5 * dx, 36, 3 * dx, 192, "hl", 1), T(ox - 2 * dx, 28, "n<0 칸", "tb", 1, fs=14)]
    for base in (110, 220):
        els.append(L(60, base, 330, base))
    els.append(STEMS(ox, 110, dx, {1: 1}, 50, b=2, nrange=range(-3, 4)))
    els.append(T(340, 80, "h = δ[n-1]", "tb", 2, fs=15, a="start"))
    els.append(T(340, 102, "인과 (O)", "t", 2, fs=15, a="start"))
    els.append(STEMS(ox, 220, dx, {-1: 1}, 50, b=3, dot="n4", nrange=range(-3, 4)))
    els.append(T(340, 190, "h = δ[n+1]", "tb", 3, fs=15, a="start"))
    els.append(T(340, 212, "비인과 (X)", "t", 3, fs=15, a="start"))
    for n in range(-3, 4):
        els.append(T(ox + n * dx, 240, str(n), "tm", fs=14))
    els.append(T(ox + 2 * dx, 262, "n", "tm", fs=14))
    return fig("음수 칸이 비어 있어야 인과", els,
               "빨간 네모(음수 칸)에 $h$ 가 하나라도 있으면 미래 입력을 써요. 위는 인과, 아래는 인과가 아니에요.")


UNITS.append(unit(
    "w3-6", "기억성, 가역성, 인과성",
    "[[임펄스 응답]] 모양만 보고 [[기억성]], [[가역성]], [[인과성|을/를]] 판정하고, [[누산기|와/과]] [[1차 차분|이/가]] 서로 [[역시스템]]인 것을 표로 보일 수 있어요.",
    ["기억성", "무기억 시스템", "가역성", "역시스템", "항등 시스템", "누산기", "1차 차분", "인과성"],
    [
        title("기억, 되돌리기, 미래 금지", "h 로 시스템 성질 읽기 (p.59~67)"),
        goal("[[무기억 시스템]]의 $h$ 모양 $k\\delta[n]$ 을 말해요.",
             "[[누산기|와/과]] [[1차 차분|이/가]] 서로 [[역시스템]]인 걸 표로 확인해요.",
             "[[인과성]] 조건 $h[n]=0$ ($n<0$) 으로 시스템을 판정해요."),
        pts("앞 단원에서 이어서",
            "앞에서 [[임펄스 응답|이/가]] [[LTI 시스템|을/를]] 완전히 대표한다고 했죠(LTI 일 때만).",
            "그래서 1장에서 배운 시스템 성질도 $h$ 모양만 보면 알 수 있어요.",
            "교수님: '$h$ 가 어떤 특성을 가지면 LTI 도 그 특성을 갖는다.' 이게 2.3절의 핵심이에요."),
        ana("통장, 되돌리기, 내일 주가",
            "통장 잔고는 지난 입금이 모두 쌓인 결과라서 기억이 있어요. 잘못 친 글은 Ctrl+Z 로 되돌리고, 내일 주가는 오늘 아무도 몰라요.",
            ["통장 잔고", "[[기억성]]: 지난 입력이 필요"],
            ["Ctrl+Z 되돌리기", "[[가역성]]: [[역시스템|이/가]] 있음"],
            ["내일 주가를 모름", "[[인과성]]: 미래 입력은 안 씀"]),
        pts("기억성 (p.59)",
            "[[무기억 시스템|은/는]] 출력이 같은 순간의 입력에만 달려요: $y[n]=kx[n]$.",
            "LTI 에서 이건 $h[n]=k\\delta[n]$ 일 때뿐이에요. $n=0$ 말고는 전부 0.",
            "$h$ 가 $n\\ne 0$ 인 칸에 하나라도 값이 있으면 [[기억성|이/가]] 있어요.",
            "실제 공학 시스템은 대부분 $x[n-1]$, $y[n-1]$ 같은 지난 값을 써요."),
        stp("손계산: 기억이 있나 없나", "입력 $x=[1,2,3]$ ($n=0$ 부터)",
            ["$h=3\\delta[n]$: $y=[3,6,9]$. 같은 칸 값을 3배 했을 뿐 → [[무기억 시스템|이에요/예요]].",
             "$h=\\delta[n-1]$: $y[n]=x[n-1]$, $y=[0,1,2,3]$. 한 칸 전 값을 써요.",
             "그래서 $\\delta[n-1]$ 시스템은 [[기억성|이/가]] 있어요."],
            "$h$ 가 $n=0$ 한 점에만 있으면 무기억, 다른 칸에도 있으면 기억이 있어요."),
        pts("항등 시스템 (p.62)",
            "$k=1$ 이면 $h=\\delta[n]$, 입력이 그대로 나와요. 이게 [[항등 시스템|이에요/예요]].",
            "$x[n]*\\delta[n]=x[n]$. 앞 단원 [[선별 성질|과/와]] 같은 말이에요.",
            "[[항등 시스템|은/는]] 다음 슬라이드 [[가역성]]의 기준점이 돼요."),
        frm("가역성: 이어 붙이면 항등 (p.60~61)",
            r"h[n]*h_i[n]=\delta[n]",
            [(r"h[n]", "원래 시스템"),
             (r"h_i[n]", "[[역시스템]]의 [[임펄스 응답]] (i 는 inverse)"),
             (r"*", "[[직렬 연결]] = 컨볼루션"),
             (r"\delta[n]", "[[항등 시스템]]: 입력이 그대로 나옴")],
            "[[가역성]]: 뒤에 붙여 [[항등 시스템|이/가]] 되게 하는 $h_i$ 가 있으면 되돌릴 수 있어요. 제어, 잡음 제거에 써요."),
        pts("Example 2.11: 늦춘 걸 당기기 (p.63)",
            "$h(t)=\\delta(t-t_0)$ 는 신호를 $t_0$ 만큼 늦춰요: $x(t)*\\delta(t-t_0)=x(t-t_0)$.",
            "되돌리려면 $t_0$ 만큼 당기면 돼요: $h_1(t)=\\delta(t+t_0)$.",
            "$\\delta(t-t_0)*\\delta(t+t_0)=\\delta(t)$, 이어 붙이면 [[항등 시스템|이에요/예요]]."),
        stp("손계산: 누산기와 1차 차분 (Example 2.12)", "[[누산기]] $h=u[n]$: $y[n]=\\sum_{k=-\\infty}^{n}x[k]$, 입력 $x=[1,2,3,0]$",
            ["쌓기: $y[0]=1$, $y[1]=1+2=3$, $y[2]=3+3=6$, $y[3]=6+0=6$.",
             "[[1차 차분]] $w[n]=y[n]-y[n-1]$: $w[0]=1-0=1$, $w[1]=3-1=2$.",
             "$w[2]=6-3=3$, $w[3]=6-6=0$.",
             "$w=[1,2,3,0]$, 처음 입력으로 돌아왔어요."],
            "[[1차 차분]] $h_1[n]=\\delta[n]-\\delta[n-1]$ 이 [[누산기]]의 [[역시스템|이에요/예요]]."),
        fig_acc_diff(),
        pts("인과성 (p.66)",
            "[[인과성]]: 출력이 지금과 과거 입력에만 달려요. 미래는 보지 않아요.",
            "$y[n]$ 이 $k>n$ 인 $x[k]$ 를 쓰지 않으려면 $h[n]=0$ ($n<0$) 이어야 해요.",
            "그러면 합은 $\\sum_{k=-\\infty}^{n}$, 적분은 $\\int_{-\\infty}^{t}$ 까지로 줄어요.",
            "손뼉을 치기 전에는 메아리가 없어야 한다는 뜻이에요."),
        stp("손계산: 인과인가 아닌가", "세 시스템의 $h$",
            ["$h=\\delta[n-1]$: $h[-1]=0$, 음수 칸이 모두 0이라서 인과.",
             "$h=\\delta[n+1]$: $h[-1]=1\\ne 0$ → 인과가 아님. $y[n]=x[n+1]$, 다음 칸 값을 미리 써요.",
             "$h=u[n]$ ([[누산기]]): $n<0$ 에서 모두 0이라서 인과."],
            "음수 칸 $h[-1], h[-2], \\dots$ 가 모두 0인지 보면 [[인과성]] 판정 끝이에요."),
        fig_causal(),
        pts("역시스템도 인과여야 (p.67)",
            "[[누산기|와/과]] 그 역시스템 [[1차 차분|은/는]] 둘 다 인과예요.",
            "역시스템은 보통 인과여야 해요. 인과가 아니면 미래를 알아야 해서 만들기 어려워요.",
            "Example 2.11 의 당기는 시스템 $\\delta(t+t_0)$ 는 $t=-t_0<0$ 에 값이 있어 인과가 아니에요."),
        chk("$h[n]=\\delta[n+2]$ 인 LTI 시스템에 대해 맞는 것은?",
            ["인과가 아니다", "인과이다", "무기억이다", "항등 시스템이다"], 0,
            "$h[-2]=1\\ne 0$ 이라서 2칸 뒤 입력(미래)을 써요. [[인과성|이/가]] 없어요."),
        chk("[[역시스템]]의 뜻은?",
            ["원래 시스템 뒤에 붙이면 입력을 그대로 돌려주는 시스템", "입력을 2배로 키우는 시스템",
             "지금까지의 입력을 모두 더하는 시스템", "미래 입력을 쓰지 않는 시스템"], 0,
            "3번은 [[누산기]], 4번은 [[인과성|이에요/예요]]. 역시스템이 있으면 [[가역성|이/가]] 있어요."),
        recap("[[무기억 시스템]] ⇔ $h[n]=k\\delta[n]$. 다른 칸에 값이 있으면 [[기억성]] 있음.",
              "[[가역성]]: $h*h_i=\\delta$, 이어 붙이면 [[항등 시스템]]. [[누산기]] $u[n]$ 의 [[역시스템|은/는]] [[1차 차분]] $\\delta[n]-\\delta[n-1]$.",
              "[[인과성]] ⇔ $h[n]=0$ ($n<0$). 손뼉 전에는 메아리가 없어야 해요.",
              "모두 LTI 에서 $h$ 하나로 판정해요."),
    ]))

# ================================================================ w3-7 안정성 (p.68~70)
_ps = [sum(0.5 ** k for k in range(n + 1)) for n in range(4)]
assert _ps == [1, 1.5, 1.75, 1.875]
assert abs(sum(0.5 ** k for k in range(200)) - 2) < 1e-12 and 1 / (1 - 0.5) == 2
assert abs(3 + (-5)) == 2 and abs(3) + abs(-5) == 8 and 2 <= 8
assert 1 * 2 == 2                                   # |x|<=1 이면 |y| <= 1 x 2
assert [sum(1 for k in range(n + 1)) for n in range(4)] == [1, 2, 3, 4]   # u[n] 의 누적 합 n+1
assert conv([1] * 5, [1] * 5)[:5] == [1, 2, 3, 4, 5]                    # x=u 넣으면 y[n]=n+1
assert abs(1 / (1 - 0.7) - 3.333) < 1e-3


def fig_stab():
    ox, dx, sc = 60, 34, 70
    els = [L(45, 110, 310, 110), L(45, 230, 310, 230)]
    els.append(STEMS(ox, 110, dx, {n: 0.5 ** n for n in range(8)}, sc, b=1))
    els.append(T(322, 60, "h = 0.5^n u[n]", "tb", 1, fs=15, a="start"))
    els.append(T(322, 84, "다 더하면 2", "t", 1, fs=15, a="start"))
    els.append(T(322, 108, "안정", "tb", 1, fs=15, a="start"))
    els.append(T(ox, 138, "누적: 1, 1.5, 1.75, 1.875, ... → 2", "tm", 3, fs=14, a="start"))
    els.append(STEMS(ox, 230, dx, {n: 1.0 for n in range(8)}, sc, b=2, dot="n4"))
    els.append(T(322, 180, "h = u[n]", "tb", 2, fs=15, a="start"))
    els.append(T(322, 204, "다 더하면 ∞", "t", 2, fs=15, a="start"))
    els.append(T(322, 228, "불안정", "tb", 2, fs=15, a="start"))
    els.append(T(ox, 258, "누적: 1, 2, 3, 4, ... → ∞", "tm", 3, fs=14, a="start"))
    return fig("크기를 모두 더해 보기", els,
               "위는 [[절대 합 가능|이라서/이라서]] 안정, 아래 [[누산기]] $u[n]$ 은 합이 끝없이 커져 불안정이에요.")


UNITS.append(unit(
    "w3-7", "안정성",
    "[[BIBO 안정]]의 뜻과 LTI 안정 조건 $\\sum|h[k]|<\\infty$ 를 말하고, $0.5^nu[n]$ 과 $u[n]$ 을 판정할 수 있어요.",
    ["안정성", "BIBO 안정", "절대 합 가능", "절대 적분 가능", "삼각 부등식", "적분기", "누산기", "임펄스 응답"],
    [
        title("안정성: 폭주하지 않기", "절대 합 가능 조건 (p.68~70)"),
        goal("[[BIBO 안정]]의 뜻을 말해요.",
             "LTI 안정 조건 $\\sum|h[k]|<\\infty$ 를 [[삼각 부등식|으로/로]] 이해해요.",
             "$0.5^nu[n]$ 은 안정, [[누산기]] $u[n]$ 은 불안정인 걸 계산해요."),
        pts("앞 단원에서 이어서",
            "앞에서 [[인과성|은/는]] $h$ 의 음수 칸을, [[기억성|은/는]] $n\\ne 0$ 칸을 봤죠.",
            "이번 [[안정성|은/는]] $h$ 의 크기를 전부 더한 값을 봐요.",
            "여전히 [[임펄스 응답]] 하나로 판정해요. 주문: " + MANTRA2),
        ana("적당히 넣으면 적당히",
            "시스템에 적당한 크기의 신호를 넣으면 적당한 크기의 신호가 나와야 정상이에요. 조금 넣었을 뿐인데 출력이 끝없이 커지며 폭주하면 불안정한 시스템이에요.",
            ["적당히 넣기", "크기가 제한된 입력 $|x[n]|<B$"],
            ["적당히 나옴", "출력도 제한됨: [[BIBO 안정]]"],
            ["조금 넣었는데 폭주", "불안정: [[안정성|이/가]] 없음"]),
        frm("출력 크기의 한계 (p.68)",
            r"|y[n]|\le\sum_{k=-\infty}^{\infty}|h[k]|\,|x[n-k]|\le B\sum_{k=-\infty}^{\infty}|h[k]|",
            [(r"|\cdot|", "절댓값: 부호를 떼고 크기만 봐요"),
             (r"B", "입력 크기의 상한(bound). 모든 $n$ 에서 $|x[n]|<B$"),
             (r"\le", "왼쪽이 오른쪽보다 크지 않다"),
             (r"\sum|h[k]|", "메아리 크기를 모두 더한 값")],
            "[[삼각 부등식]] 덕분에 출력 크기는 $B\\times$(메아리 크기의 합)을 넘지 못해요."),
        stp("손계산: 삼각 부등식", "두 수 $3$ 과 $-5$",
            ["합의 크기: $|3+(-5)|=|-2|=2$.",
             "크기의 합: $|3|+|-5|=3+5=8$.",
             "$2\\le 8$. 합의 크기는 크기의 합보다 크지 않아요."],
            "[[삼각 부등식]] $|a+b|\\le|a|+|b|$. 부호가 달라 서로 지우면 합이 작아질 뿐이에요."),
        frm("LTI 안정 조건 (p.69)",
            r"\sum_{k=-\infty}^{\infty}|h[k]|<\infty",
            [(r"\sum_{k=-\infty}^{\infty}|h[k]|", "[[임펄스 응답]] 크기를 모든 칸에서 더한 값"),
             (r"<\infty", "무한대보다 작다, 즉 유한한 수"),
             (r"\int_{-\infty}^{\infty}|h(\tau)|\,d\tau<\infty", "연속시간 버전: [[절대 적분 가능]]")],
            "이산시간 LTI 는 $h$ 가 [[절대 합 가능|일/일]] 때, 그리고 그때만(필요충분) [[BIBO 안정|이에요/예요]]."),
        stp("손계산: $h[n]=0.5^nu[n]$", "입력은 $|x[n]|\\le 1$",
            ["크기를 차례로 더해요: $1$, $1+0.5=1.5$, $1.75$, $1.875$, ...",
             "[[등비급수]] 무한합: $\\frac{1}{1-0.5}=2$.",
             "$2<\\infty$ 라서 [[절대 합 가능]], 따라서 안정.",
             "출력은 $|y|\\le 1\\times 2=2$ 를 절대 넘지 않아요."],
            "$\\sum|h|=2$, [[안정성|이/가]] 있어요."),
        stp("손계산: $h[n]=u[n]$ ([[누산기]])", "Example 2.13 (p.70)",
            ["크기 합: $1, 2, 3, 4, \\dots$ 끝없이 커져요. $\\sum|h|=\\infty$.",
             "실제로 크기 1인 입력 $x=u[n]$ 을 넣으면 $y[n]=n+1$, 끝없이 커져요.",
             "제한된 입력에 끝없는 출력이 나왔으니 불안정."],
            "[[누산기|와/과]] 연속시간 [[적분기|은/는]] 둘 다 불안정해요. $\\int|u(\\tau-t_0)|d\\tau=\\infty$."),
        fig_stab(),
        pts("Example 2.13: 시간만 미는 시스템 (p.69)",
            "$h[n]=\\delta[n-n_0]$: $\\sum|h[k]|=1<\\infty$, 안정.",
            "$h(t)=\\delta(t-t_0)$: $\\int|h(\\tau)|d\\tau=1<\\infty$, [[절대 적분 가능|이라서/이라서]] 안정.",
            "시간만 미는 시스템은 크기를 바꾸지 않으니 제한된 입력이면 출력도 제한돼요."),
        cmp("안정 판정 한 장 정리", ["$h$", "크기 합", "판정"], [
            ["$\\delta[n-n_0]$ (시간 이동)", "$1$", "안정"],
            ["$0.5^nu[n]$", "$2$", "안정"],
            ["$u[n]$ ([[누산기]])", "$\\infty$", "불안정"],
            ["$u(t-t_0)$ ([[적분기]])", "$\\infty$", "불안정"]]),
        pts("p.19 그림 다시 보기",
            "$y[n]=x[n]+0.7y[n-1]$ 의 $h=0.7^nu[n]$: 크기 합 $\\frac{1}{1-0.7}\\approx 3.33$, 안정.",
            "$y[n]=x[n]+1.3y[n-1]$ 의 $h=1.3^nu[n]$: 끝없이 커져서 불안정.",
            "p.19 에 적힌 stable, unstable 판정과 같아요."),
        pts("첫 퀴즈 범위는 여기까지",
            "첫 퀴즈: 추석 휴강 다음 수업 시작 때 20~30분.",
            "범위: 1장 전체 + 2장 슬라이드 62번(이 사이트 p.70, 안정성)까지.",
            "교수님: 수업에서 다룬 예제와 과제만 복습하면 충분히 풀 수 있게 낸다. 늦게 오면 시간을 더 주지 않는다."),
        chk("$h[n]=0.5^nu[n]$ 일 때 $\\sum|h[k]|$ 는?", ["$1$", "$2$", "$0.5$", "무한대"], 1,
            "$1+0.5+0.25+\\cdots=\\frac{1}{1-0.5}=2$ 예요. 유한하니 안정이에요."),
        chk("[[BIBO 안정]]의 뜻은?",
            ["크기가 제한된 입력에는 늘 크기가 제한된 출력이 나온다", "입력과 출력이 늘 같다",
             "미래 입력을 쓰지 않는다", "출력만 보고 입력을 알아낼 수 있다"], 0,
            "2번은 항등 시스템, 3번은 [[인과성]], 4번은 [[가역성|이에요/예요]]."),
        warn("헷갈리기 쉬운 점",
             "조건은 $h$ 의 절댓값 합이에요. 그냥 더하면 +와 -가 지워져 잘못 판정할 수 있어요.",
             "[[BIBO 안정|은/는]] '모든' 제한된 입력에 대해 출력이 제한되어야 해요. 폭주하는 입력이 하나라도 있으면 불안정."),
        recap("[[안정성]]([[BIBO 안정]]): 제한된 입력 → 제한된 출력.",
              "LTI 는 $\\sum|h[k]|<\\infty$ ([[절대 합 가능]]), 연속시간은 $\\int|h|<\\infty$ ([[절대 적분 가능]]).",
              "근거는 [[삼각 부등식]]: $|y|\\le B\\sum|h|$.",
              "$0.5^nu[n]$ 은 합 $2$ 로 안정, 시간 이동은 합 $1$ 로 안정, [[누산기]]와 [[적분기]]는 불안정. 퀴즈 범위 끝(p.70)."),
    ]))

# ================================================================ w3-8 계단 응답 (p.71~74)
H8 = [1, 0.5, 0.25, 0, 0, 0]
S8 = [float(v) for v in np.cumsum(H8)]
assert S8 == [1, 1.5, 1.75, 1.75, 1.75, 1.75]
assert [S8[0]] + [S8[i] - S8[i - 1] for i in range(1, 6)] == H8
assert conv(H8, [1] * 6)[:6] == S8                      # s = h * u
_s1 = _integrate(lambda tau: np.exp(-tau), 0, 1)
assert abs(_s1 - (1 - math.exp(-1))) < 1e-9 and abs(_s1 - Y26_1) < 1e-12   # Example 2.6 (a=1) 과 같은 값
_ds = ((1 - math.exp(-(1 + 1e-6))) - (1 - math.exp(-(1 - 1e-6)))) / 2e-6
assert abs(_ds - math.exp(-1)) < 1e-6                     # ds/dt = h(t)


def fig_step():
    ox, dx, sc = 70, 45, 60
    els = [L(50, 110, 310, 110), L(50, 240, 310, 240)]
    els.append(STEMS(ox, 110, dx, dict(enumerate(H8)), sc, b=1))
    els.append(T(325, 80, "h[n]", "tb", 1, fs=15, a="start"))
    els.append(T(325, 102, "1, 0.5, 0.25", "t", 1, fs=14, a="start"))
    els.append(STEMS(ox, 240, dx, dict(enumerate(S8)), sc, b=2))
    els.append(T(325, 190, "s[n] = 누적 합", "tb", 2, fs=15, a="start"))
    els.append(T(325, 212, "1, 1.5, 1.75, ...", "t", 2, fs=14, a="start"))
    for n in range(6):
        els.append(T(ox + n * dx, 258, str(n), "tm", fs=14))
    return fig("임펄스 응답을 쌓으면 계단 응답", els,
               "[[임펄스 응답]] $h[n]$ 을 처음부터 차례로 더하면 [[계단 응답]] $s[n]$ 이에요. $1\\to 1.5\\to 1.75$ 에서 멈춰요.")


UNITS.append(unit(
    "w3-8", "계단 응답",
    "[[계단 응답|이/가]] [[임펄스 응답]]의 [[누적 합|이고/이고]], 거꾸로 [[임펄스 응답|이/가]] [[계단 응답]]의 [[1차 차분|이라는/이라는]] 관계를 숫자로 보일 수 있어요.",
    ["계단 응답", "단위 계단", "누적 합", "1차 차분", "임펄스 응답", "미분", "적분"],
    [
        title("계단 응답", "스위치를 켰을 때의 출력 (p.71~74)"),
        goal("[[계단 응답]] $s[n]$ 이 [[임펄스 응답]]의 [[누적 합|이라는/이라는]] 걸 말해요.",
             "거꾸로 $h[n]=s[n]-s[n-1]$, [[1차 차분|으로/로]] 되돌려요.",
             "연속시간은 [[적분|과/와]] [[미분|으로/로]] 바뀌는 걸 봐요."),
        warn(OUTSIDE,
             "p.71~74 는 3주차 수업에서 아직 하지 않았어요. 다음 수업에서 할 예정이에요.",
             "교수님: '유닛 스텝 리스폰스가 꽤 중요하다.' 퀴즈 범위는 아니지만 미리 봐 두면 좋아요."),
        pts("앞 단원에서 이어서",
            "[[단위 계단|은/는]] 스위치를 켜는 순간, 켠 뒤로 계속 1이에요.",
            "앞에서 [[누산기]] $h=u[n]$ 은 입력을 계속 쌓는 시스템이었고, [[1차 차분|이/가]] 그 역시스템이었죠.",
            "[[교환 법칙|으로/로]] 넣는 것과 시스템을 바꿔 볼 수 있다는 것도 배웠어요."),
        ana("스위치를 켜 두면 메아리가 쌓여요",
            "스위치를 켜 두면 칸마다 손뼉을 한 번씩 계속 치는 것과 같아요. 칸마다 새 메아리가 생겨 겹겹이 쌓이니, 들리는 소리는 메아리를 처음부터 지금까지 모두 더한 값이에요.",
            ["스위치 켜기", "[[단위 계단]] $u[n]$ 입력"],
            ["쌓인 메아리 소리", "[[계단 응답]] $s[n]$"],
            ["메아리를 처음부터 더하기", "[[누적 합]] $\\sum_{k\\le n}h[k]$"]),
        frm("계단 응답 = 임펄스 응답의 누적 합 (p.71, p.73)",
            r"s[n]=u[n]*h[n]=h[n]*u[n]=\sum_{k=-\infty}^{n}h[k]",
            [(r"s[n]", "[[계단 응답]]: 입력이 $u[n]$ 일 때의 출력"),
             (r"u[n]*h[n]", "[[단위 계단|을/를]] 시스템 $h$ 에 넣음"),
             (r"h[n]*u[n]", "[[교환 법칙]]: $h$ 를 [[누산기]] $u$ 에 넣은 것과 같음"),
             (r"\sum_{k=-\infty}^{n}h[k]", "$h$ 를 처음부터 $n$ 칸까지 더함, [[누적 합]]")],
            "[[계단 응답|은/는]] [[임펄스 응답]]의 [[누적 합|이에요/예요]]."),
        frm("거꾸로: 1차 차분 (p.71)",
            r"h[n]=s[n]-s[n-1]",
            [(r"s[n]", "지금 칸의 [[계단 응답]]"),
             (r"s[n-1]", "한 칸 전의 [[계단 응답]]"),
             (r"s[n]-s[n-1]", "지금 칸에서 새로 더해진 양")],
            "[[임펄스 응답|은/는]] [[계단 응답]]의 [[1차 차분|이에요/예요]]. $\\delta[n]=u[n]-u[n-1]$ 과 같은 모양이에요."),
        stp("손계산: 쌓고 되돌리기", "p.19 의 $h[n]$: $h[0]=1$, $h[1]=0.5$, $h[2]=0.25$, 나머지 0",
            ["$s[0]=1$.",
             "$s[1]=1+0.5=1.5$.",
             "$s[2]=1.5+0.25=1.75$, 그 뒤로는 더할 게 없어 계속 $1.75$.",
             "되돌리기: $s[1]-s[0]=0.5$, $s[2]-s[1]=0.25$, $s[3]-s[2]=0$. $h$ 가 그대로 나와요."],
            "$s=[1,\\ 1.5,\\ 1.75,\\ 1.75,\\dots]$. [[누적 합|과/와]] [[1차 차분|은/는]] 서로 되돌리는 관계예요."),
        fig_step(),
        pts("연속시간 (p.72)",
            "$s(t)=u(t)*h(t)=\\int_{-\\infty}^{t}h(\\tau)\\,d\\tau$: [[임펄스 응답|을/를]] [[적분|으로/로]] 쌓아요(running integral).",
            "$h(t)=\\frac{ds(t)}{dt}$: [[계단 응답|을/를]] [[미분|하면/하면]] 임펄스 응답이에요.",
            "이산시간의 합과 차가 연속시간에서는 [[적분|과/와]] [[미분|으로/로]] 바뀌어요."),
        stp("손계산: 연속시간 계단 응답", "$h(t)=e^{-t}u(t)$",
            ["$s(t)=\\int_0^t e^{-\\tau}d\\tau=1-e^{-t}$ ($t>0$).",
             "$s(1)=1-e^{-1}\\approx 0.632$.",
             "Example 2.6 ($a=1$) 과 같은 답이에요. 입력과 $h$ 를 바꿔도 되는 [[교환 법칙]] 덕분이에요.",
             "되돌리기: $\\frac{d}{dt}\\left(1-e^{-t}\\right)=e^{-t}=h(t)$."],
            "[[적분|하면/하면]] [[계단 응답]], [[미분|하면/하면]] 다시 [[임펄스 응답|이에요/예요]]."),
        pts("p.74 그림: 계단 응답으로 보는 것",
            "입력이 계단처럼 바뀌면 출력은 올라가며 조금 흔들리다가 새 값 $V_2$ 근처(오차 띠)에 자리 잡아요.",
            "자리 잡기까지 걸린 시간을 settling time 이라고 적어 두었어요.",
            "그래서 [[계단 응답|은/는]] 시스템이 얼마나 빨리, 얼마나 흔들리며 반응하는지 보여 줘요."),
        chk("$h=[1,\\ 0.5,\\ 0.25]$ ($n=0$ 부터) 일 때 $s[2]$ 는?", ["$1.75$", "$0.25$", "$1.5$", "$2$"], 0,
            "$s[2]=h[0]+h[1]+h[2]=1+0.5+0.25=1.75$ 예요."),
        chk("[[계단 응답]]의 뜻은?",
            ["[[단위 계단|을/를]] 넣었을 때 나오는 출력", "[[단위 임펄스|을/를]] 넣었을 때 나오는 출력",
             "출력이 계단처럼 끊기는 시스템", "입력의 [[1차 차분]]"], 0,
            "2번은 [[임펄스 응답|이에요/예요]]. 둘은 [[누적 합|과/와]] 차분으로 이어져요."),
        recap("[[계단 응답]] $s[n]=u[n]*h[n]=\\sum_{k\\le n}h[k]$: [[임펄스 응답]]의 [[누적 합]].",
              "거꾸로 $h[n]=s[n]-s[n-1]$, [[1차 차분|이에요/예요]].",
              "연속시간: $s(t)=\\int_{-\\infty}^{t}h$ ([[적분]]), $h=\\frac{ds}{dt}$ ([[미분]]).",
              "다음 수업 내용, 첫 퀴즈 범위 밖. 그래도 교수님이 꽤 중요하다고 했어요."),
    ]))

# ================================================================ w3-9 미분, 차분방정식과 블록 다이어그램 (p.75~92)
def _rec(a1, x, n_max):
    y, prev = [], 0.0                      # 초기 휴지: y[-1] = 0
    for n in range(n_max + 1):
        cur = a1 * prev + x(n)
        y.append(cur)
        prev = cur
    return y


H9 = _rec(0.5, lambda n: 1.0 if n == 0 else 0.0, 4)
assert H9 == [1, 0.5, 0.25, 0.125, 0.0625] and all(abs(H9[n] - 0.5 ** n) < 1e-15 for n in range(5))
_bank = _rec(1.01, lambda n: 100.0 if n == 0 else 0.0, 2)
assert abs(_bank[0] - 100) < 1e-9 and abs(_bank[1] - 101) < 1e-9 and abs(_bank[2] - 102.01) < 1e-9
assert abs(0.5 ** 20) < 1e-5 and 1.01 ** 500 > 100    # a1=0.5 는 줄고(안정), 1.01 은 커짐(불안정)
assert abs(_rec(0.5, lambda n: 1.0, 3)[3] - 1.875) < 1e-12   # 계단 입력이면 Example 2.3 과 같은 값


def fig_elements():
    els = [T(20, 26, "덧셈기", "tb", 1, fs=15, a="start"),
           T(20, 65, "x1[n]", "t", 1, fs=15, a="start"), A(68, 60, 177, 60, "e", 1),
           T(190, 18, "x2[n]", "t", 1, fs=14), A(190, 24, 190, 47, "e", 1), ADDER(190, 60, 1),
           A(202, 60, 298, 60, "e2", 1), T(306, 65, "x1[n] + x2[n]", "t", 1, fs=15, a="start"),
           T(20, 112, "곱셈기(게인)", "tb", 2, fs=15, a="start"),
           T(20, 150, "x[n]", "t", 2, fs=15, a="start"), A(60, 145, 298, 145, "e2", 2),
           T(180, 136, "a", "tb", 2, fs=16), T(306, 150, "a x[n]", "t", 2, fs=15, a="start"),
           T(20, 192, "단위 지연", "tb", 3, fs=15, a="start"),
           T(20, 230, "x[n]", "t", 3, fs=15, a="start"), A(60, 225, 160, 225, "e", 3),
           BOX(160, 207, 56, 36, "D", "box2", 3, fs=16), A(216, 225, 298, 225, "e2", 3),
           T(306, 230, "x[n-1]", "t", 3, fs=15, a="start")]
    return fig("블록 세 가지 (p.83)", els,
               "[[블록 다이어그램|은/는]] 덧셈기, 곱셈기, [[단위 지연]] D 세 가지로 그려요.")


def fig_block():
    els = [T(14, 95, "x[n]", "tb", 1, fs=15, a="start"), A(52, 90, 137, 90, "e2", 1),
           T(95, 80, "b = 1", "t", 1, fs=14), ADDER(150, 90, 1),
           A(162, 90, 418, 90, "e2", 1), T(424, 95, "y[n]", "tb", 1, fs=15, a="start"),
           C(330, 90, 3, "n2", 2), A(330, 90, 330, 138, "e", 2),
           BOX(305, 138, 50, 36, "D", "box2", 2, fs=16), L(330, 174, 330, 214, "e", 2),
           T(338, 202, "y[n-1]", "t", 2, fs=14, a="start"),
           L(330, 214, 150, 214, "e2", 3), A(150, 214, 150, 103, "e2", 3),
           T(240, 206, "× 0.5  (-a)", "tb", 3, fs=15),
           T(240, 256, "y[n] = x[n] + 0.5 y[n-1]", "tb", 4, fs=16)]
    return fig("$y[n]=0.5y[n-1]+x[n]$ 의 블록 다이어그램 (p.84 모양)", els,
               "출력을 D 로 한 칸 늦추고 $0.5$ 를 곱해 입력에 다시 더해요. 이게 [[되먹임 연결|이에요/예요]].")


UNITS.append(unit(
    "w3-9", "미분, 차분방정식과 블록 다이어그램",
    "[[선형 상수계수 차분방정식|을/를]] [[초기 휴지 조건|에서/에서]] 한 칸씩 풀어 [[임펄스 응답|을/를]] 구하고, [[블록 다이어그램|으로/로]] 그릴 수 있어요.",
    ["선형 상수계수 미분방정식", "선형 상수계수 차분방정식", "초기 휴지 조건", "블록 다이어그램", "단위 지연", "시스템 차수", "되먹임 연결", "차분방정식"],
    [
        title("차분방정식과 블록 그림", "2.4절 미리 보기 (p.75~92)"),
        goal("[[선형 상수계수 미분방정식|과/와]] [[선형 상수계수 차분방정식|을/를]] 구별해요.",
             "[[초기 휴지 조건|에서/에서]] $y[n]=0.5y[n-1]+x[n]$ 의 [[임펄스 응답|을/를]] 한 칸씩 구해요.",
             "덧셈기, 곱셈기, [[단위 지연|으로/로]] [[블록 다이어그램|을/를]] 그려요."),
        warn(OUTSIDE,
             "p.75~92 는 3주차에 아직 수업하지 않았어요. 다음 수업에서 할 예정이에요.",
             "2.5절은 '어렵고 중요하지 않아서' 수업하지 않는다고 했어요(교수님).",
             "p.89~92 과제 슬라이드(2.21, 2.23, 2.28, 2.31)는 2장을 마친 뒤 낼 예정이었고, 이번 주에는 과제가 없다고 했어요."),
        ana("통장 잔고",
            "통장 잔고는 어제 잔고에 이자가 붙고 오늘 입금이 더해져 정해져요. 오늘 잔고를 알려면 어제 잔고를 기억해야 해요.",
            ["어제 잔고", "한 칸 전 출력 $y[n-1]$"],
            ["오늘 입금", "입력 $x[n]$"],
            ["어제 잔고에 비율을 곱해 더하기", "[[선형 상수계수 차분방정식]]"]),
        pts("식으로 시스템 쓰기 (p.75, p.79)",
            "연속시간: $\\frac{dy}{dt}+ay=bx$ 같은 [[선형 상수계수 미분방정식|이에요/예요]]. [[RC 회로|은/는]] $a=b=\\frac{1}{RC}$.",
            "이산시간: $y[n]+ay[n-1]=bx[n]$ 같은 [[선형 상수계수 차분방정식|이에요/예요]]. 통장은 $a=-1.01$, $b=1$.",
            "일반형 $\\sum_{k=0}^{N}a_ky[n-k]=\\sum_{k=0}^{M}b_kx[n-k]$ 에서 $N$ 이 [[시스템 차수|예요/이에요]].",
            "미분이나 지난 칸이 들어 있으면 기억이 있는 시스템이에요."),
        frm("한 칸씩 차례로 풀기 (p.81)",
            r"y[n]=\frac{1}{a_0}\left\{\sum_{k=0}^{M}b_kx[n-k]-\sum_{k=1}^{N}a_ky[n-k]\right\}",
            [(r"a_0", "지금 칸 $y[n]$ 앞의 계수"),
             (r"\sum_{k=0}^{M}b_kx[n-k]", "지금과 지난 입력에 계수를 곱해 더한 것"),
             (r"\sum_{k=1}^{N}a_ky[n-k]", "지난 출력에 계수를 곱해 더한 것 (최대 $N$ 칸 전, [[시스템 차수]])")],
            "지난 출력을 알면 [[차분방정식|을/를]] 앞에서부터 한 칸씩(재귀적으로) 풀 수 있어요."),
        pts("초기 휴지 조건 (p.77, p.81)",
            "[[초기 휴지 조건]]: 입력이 들어오기 전에는 출력도 0이에요.",
            "인과 시스템이 되려면 이 조건이 필요해요. 그래서 $y[-1]=0$ 에서 출발해요.",
            "보조 조건이 없으면 [[차분방정식]]의 답이 하나로 정해지지 않아요(p.77)."),
        stp("손계산: 임펄스 응답 한 칸씩 (Example 2.15)", "$y[n]=0.5y[n-1]+x[n]$, $x=\\delta[n]$, [[초기 휴지 조건]] $y[-1]=0$",
            ["$y[0]=0.5\\times 0+1=1$.",
             "$y[1]=0.5\\times 1+0=0.5$.",
             "$y[2]=0.5\\times 0.5=0.25$, $y[3]=0.5\\times 0.25=0.125$.",
             "$y[4]=0.5\\times 0.125=0.0625$."],
            "$h[n]=0.5^nu[n]$. Example 2.15 ($K=1$) 와 같아요. 끝없이 이어지는 [[임펄스 응답|이에요/예요]]."),
        fig_elements(),
        fig_block(),
        stp("손계산: 통장 계좌 (p.79)", "$a=-1.01$, $b=1$ → $y[n]=1.01y[n-1]+x[n]$, 처음에 $100$ 입금 ($x=100\\delta[n]$)",
            ["$y[0]=100$.",
             "$y[1]=1.01\\times 100=101$.",
             "$y[2]=1.01\\times 101=102.01$.",
             "칸마다 $1.01$ 배씩 끝없이 커져요."],
            "$h[n]=1.01^nu[n]$ 은 합이 끝없이 커져서 [[안정성]] 기준으로는 불안정이에요."),
        pts("연속시간 블록 (p.85~88)",
            "연속시간은 D 자리에 미분기(p.86)나 [[적분기]](p.88)를 써요.",
            "p.88: $y(t)=\\int_{-\\infty}^{t}[bx(\\tau)-ay(\\tau)]\\,d\\tau$, 적분기와 $-a$ [[되먹임 연결|으로/로]] 그려요.",
            "이산이든 연속이든 [[블록 다이어그램|은/는]] 덧셈기, 곱셈기, 지연(또는 적분기)의 조합이에요."),
        warn("슬라이드 오류 주의 (p.80)",
             "p.80 은 $a_1>0$ 이면 불안정이라고 적었지만, $y[n]=Aa_1^n$ 은 $a_1=0.5$ 처럼 양수여도 줄어들어요.",
             "이산시간은 $|a_1|<1$ 이면 줄어서 안정, $|a_1|>1$ 이면 커져서 불안정이에요. 영어 교재로 한 번 확인해 보세요.",
             "연속시간(p.76)의 $Ae^{a_1t}$ 는 $a_1>0$ 이면 커지고 $a_1<0$ 이면 줄어서 슬라이드 설명이 맞아요."),
        chk("$y[n]=0.5y[n-1]+x[n]$, [[초기 휴지 조건]], $x=\\delta[n]$ 일 때 $y[3]$ 은?",
            ["$0.125$", "$0.5$", "$0.25$", "$1$"], 0,
            "$1\\to 0.5\\to 0.25\\to 0.125$, 칸마다 $0.5$ 배예요."),
        chk("[[단위 지연]] 상자 D 가 하는 일은?",
            ["입력을 한 칸 늦춰 내보낸다", "두 신호를 더한다", "입력에 상수를 곱한다", "입력을 적분한다"], 0,
            "2번은 덧셈기, 3번은 곱셈기(게인), 4번은 [[적분기|예요/이에요]]."),
        recap("[[선형 상수계수 미분방정식]] (연속, 예: [[RC 회로]]), [[선형 상수계수 차분방정식]] (이산, 예: 통장).",
              "[[초기 휴지 조건]] $y[-1]=0$ 에서 한 칸씩: $h=1, 0.5, 0.25, 0.125, 0.0625$.",
              "[[블록 다이어그램]]: 덧셈기, 곱셈기, [[단위 지연]] D. 출력을 되돌리면 [[되먹임 연결]].",
              "다음 수업 내용, 첫 퀴즈 범위 밖. [[시스템 차수|은/는]] 가장 깊은 지연 수 $N$."),
    ]))

# ==== END OF UNITS ====


def main():
    assert [u["id"] for u in UNITS] == ["w3-%d" % i for i in range(1, 10)]
    data = {"week": "3", "title": "3주차. 2장 선형 시불변(LTI) 시스템", "units": UNITS}
    raw = json.dumps(data, ensure_ascii=False, indent=1)
    for bad in ("\u2014", "\u2013", "\u00b7", "\u30fb"):
        assert bad not in raw, bad
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(raw)
    print("단원 %d개, 슬라이드 %d장 -> %s" % (len(UNITS), sum(len(u["slides"]) for u in UNITS), OUT))
    for u in UNITS:
        print(" ", u["id"], u["title"], len(u["slides"]), "장, 용어", len(u["terms"]))


if __name__ == "__main__":
    main()
