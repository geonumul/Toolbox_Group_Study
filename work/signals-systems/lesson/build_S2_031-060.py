# -*- coding: utf-8 -*-
# 신호및시스템 2주차(S2) 회독 레슨 31~60쪽 생성기.
# 사용: python build_S2_031-060.py  ->  S2_031-060.json
# 범위: 1.3 뒷부분(주기 복소 지수, 조화 관계, 일반 복소 지수, 이산시간 복소 지수),
#       1.4 단위 임펄스와 단위 계단, 1.5 시스템 시작(RC 회로, 자동차, 통장).
import json, math, cmath, os, re, sys
from fractions import Fraction

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "S2_031-060.json")
DICT = json.load(open(os.path.join(HERE, "..", "rules", "용어사전.json"), encoding="utf-8"))

MANTRA = "신호는 시간에 따라 변하는 값, 시스템은 신호를 바꾸는 상자."
WHEN = "2주차 목요일 수업"

# ---------------- 용어 ----------------
TERMS = {
    "sig": ("신호", "Signal"), "sys": ("시스템", "System"),
    "ct": ("연속시간 신호", "Continuous-Time Signal"), "dt": ("이산시간 신호", "Discrete-Time Signal"),
    "samp": ("샘플링", "Sampling"),
    "energy": ("신호 에너지", "Signal Energy"), "power": ("평균 전력", "Average Power"),
    "shift": ("시간 이동", "Time Shift"),
    "periodic": ("주기 신호", "Periodic Signal"), "fper": ("기본 주기", "Fundamental Period"),
    "aper": ("비주기 신호", "Aperiodic Signal"),
    "cnum": ("복소수", "Complex Number"), "imag": ("허수 단위", "Imaginary Unit"),
    "cplane": ("복소평면", "Complex Plane"), "phase": ("위상", "Phase"), "ucirc": ("단위원", "Unit Circle"),
    "euler": ("오일러 공식", "Euler's Formula"), "expf": ("지수함수", "Exponential Function"),
    "rexp": ("실수 지수 신호", "Real Exponential Signal"), "cexp": ("복소 지수 신호", "Complex Exponential Signal"),
    "sinus": ("사인파 신호", "Sinusoidal Signal"), "amp": ("진폭", "Amplitude"),
    "angf": ("각주파수", "Angular Frequency"), "rad": ("라디안", "Radian"),
    "harm": ("조화 관계 복소 지수", "Harmonically Related Complex Exponentials"),
    "damped": ("감쇠 사인파", "Damped Sinusoid"), "env": ("포락선", "Envelope"),
    "imp": ("단위 임펄스", "Unit Impulse"), "step": ("단위 계단", "Unit Step"),
    "rsum": ("누적 합", "Running Sum"), "fdiff": ("1차 차분", "First Difference"),
    "sift": ("선별 성질", "Sifting Property"), "superpos": ("중첩 원리", "Superposition"),
    "in": ("입력 신호", "Input Signal"), "out": ("출력 신호", "Output Signal"),
    "de": ("미분방정식", "Differential Equation"), "dfe": ("차분방정식", "Difference Equation"),
    "rc": ("RC 회로", "RC Circuit"), "order": ("시스템 차수", "Order"),
    "lin": ("선형성", "Linearity"), "ir": ("임펄스 응답", "Impulse Response"),
    "conv": ("컨볼루션", "Convolution"), "deconv": ("역컨볼루션", "Deconvolution"),
    "sigma": ("시그마 기호", "Summation"), "integ": ("적분", "Integral"), "deriv": ("미분", "Derivative"),
    "memory": ("기억성", "Memory"),
}

JOSA = {"은": ("은", "는"), "이": ("이", "가"), "을": ("을", "를"), "과": ("과", "와"),
        "으로": ("으로", "로"), "이에요": ("이에요", "예요"), "이고": ("이고", "고"),
        "이라고": ("이라고", "라고"), "이라서": ("이라서", "라서"), "이나": ("이나", "나"),
        "이죠": ("이죠", "죠"), "이라는": ("이라는", "라는")}


def _fin(key):
    c = TERMS[key][0][-1]
    if "가" <= c <= "힣":
        j = (ord(c) - 0xAC00) % 28
        return 0 if j == 0 else (2 if j == 8 else 1)
    return 1


def disp(key):
    ko, en = TERMS[key]
    return f"**{ko}({en})**"


def K(key, josa=""):
    s = disp(key)
    if not josa:
        return s
    f = _fin(key)
    if josa == "으로":
        return s + ("으로" if f == 1 else "로")
    if josa in JOSA:
        return s + (JOSA[josa][0] if f >= 1 else JOSA[josa][1])
    return s + josa


def gloss_entry(key):
    ko, en = TERMS[key]
    for d in DICT:
        if d.get("ko") == ko and d.get("en") == en:
            g = {"ko": ko, "en": en, "say": d["say"]}
            if d.get("more"):
                g["more"] = d["more"]
            return g
    raise KeyError(f"용어 사전에 없음: {ko} {en}")


# ---------------- 장면 ----------------
PW, PH = 1400, 788   # 작성용 PNG 크기 (PDF 960x540 과 같은 비율)


def say(*lines):
    return {"kind": "say", "lines": list(lines)}


def look(head, *boxes):
    """boxes: (x1, y1, x2, y2, 설명) 픽셀, 1400x788 PNG 기준"""
    out = []
    for x1, y1, x2, y2, s in boxes:
        out.append({"x": round(x1 / PW, 3), "y": round(y1 / PH, 3),
                    "w": round((x2 - x1) / PW, 3), "h": round((y2 - y1) / PH, 3), "say": s})
    return {"kind": "look", "head": head, "boxes": out}


def points(head, *items):
    return {"kind": "points", "head": head, "items": list(items)}


def analogy(head, scene, *pairs):
    return {"kind": "analogy", "head": head, "scene": scene, "map": [list(p) for p in pairs]}


def compare(head, cols, *rows):
    return {"kind": "compare", "head": head, "cols": list(cols), "rows": [list(r) for r in rows]}


def formula(head, tex, parts, whole):
    return {"kind": "formula", "head": head, "tex": tex,
            "parts": [{"sym": s, "say": t} for s, t in parts], "whole": whole}


def steps(head, stps, answer, given=None):
    d = {"kind": "steps", "head": head}
    if given:
        d["given"] = given
    d["steps"] = list(stps)
    d["answer"] = answer
    return d


def figure(head, svg, caption):
    mb = max([int(m) for m in re.findall(r"\bb(\d)\b", svg)] or [1])
    return {"kind": "figure", "head": head, "svg": svg, "caption": caption, "builds": mb}


def check(q, choices, a, why):
    return {"kind": "check", "q": q, "choices": list(choices), "a": a, "why": why}


def warn(head, *items):
    return {"kind": "warn", "head": head, "items": list(items)}


def exam(src, q, qko, solve, answer):
    return {"kind": "exam", "src": src, "q": q, "qko": qko, "solve": list(solve), "answer": answer}


def english(head, en, ko, tip=None):
    d = {"kind": "english", "head": head, "en": en, "ko": ko}
    if tip:
        d["tip"] = tip
    return d


def bg(src, *lines):
    return {"kind": "bg", "src": src, "lines": list(lines)}


def prof(*lines, when=WHEN):
    return {"kind": "prof", "when": when, "lines": list(lines)}


# ---------------- SVG ----------------
def _b(b):
    return f" b{b}" if b else ""


def _n(v):
    return f"{v:.1f}".rstrip("0").rstrip(".") if isinstance(v, float) else str(v)


def TX(x, y, s, cls="t", fs=15, anc="middle", b=0):
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f'<text x="{_n(x)}" y="{_n(y)}" font-size="{fs}" text-anchor="{anc}" class="{cls}{_b(b)}">{s}</text>'


def R(x, y, w, h, cls="box", b=0, rx=2):
    return f'<rect x="{_n(x)}" y="{_n(y)}" width="{_n(w)}" height="{_n(h)}" rx="{rx}" class="{cls}{_b(b)}"/>'


def C(x, y, r, cls="n", b=0):
    return f'<circle cx="{_n(x)}" cy="{_n(y)}" r="{_n(r)}" class="{cls}{_b(b)}"/>'


def L(x1, y1, x2, y2, cls="e", b=0):
    return f'<line x1="{_n(x1)}" y1="{_n(y1)}" x2="{_n(x2)}" y2="{_n(y2)}" class="{cls}{_b(b)}"/>'


def A(x1, y1, x2, y2, cls="e2", b=0):
    """화살표: 선 + 머리"""
    ang = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 - 9 * math.cos(ang), y2 - 9 * math.sin(ang)
    px, py = -math.sin(ang) * 5, math.cos(ang) * 5
    pts = f"{x2:.1f},{y2:.1f} {hx + px:.1f},{hy + py:.1f} {hx - px:.1f},{hy - py:.1f}"
    return L(x1, y1, round(hx, 1), round(hy, 1), cls, b) + f'<polygon points="{pts}" class="arrow{_b(b)}"/>'


def PL(pts, cls="e2", b=0):
    s = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polyline points="{s}" fill="none" class="{cls}{_b(b)}"/>'


def BOX(x, y, w, h, label, cls="box", tcls="tb", b=0, fs=15):
    return R(x, y, w, h, cls, b) + TX(x + w / 2, y + h / 2 + fs // 3 + 1, label, tcls, fs, "middle", b)


def SVG(*parts, h=270):
    return f'<svg viewBox="0 0 480 {h}" xmlns="http://www.w3.org/2000/svg">' + "".join(parts) + "</svg>"


class Plot:
    """수학 좌표 -> SVG 좌표 변환. ox, oy: 원점 픽셀, sx, sy: 1 단위당 픽셀"""
    def __init__(self, ox, oy, sx, sy):
        self.ox, self.oy, self.sx, self.sy = ox, oy, sx, sy

    def X(self, t):
        return self.ox + t * self.sx

    def Y(self, v):
        return self.oy - v * self.sy

    def axes(self, t0, t1, v0, v1, xl="t", yl="", b=0, fs=15):
        out = [A(self.X(t0), self.oy, self.X(t1) + 12, self.oy, "e", b)]
        if v1 > v0:
            out.append(L(self.ox, self.Y(v0), self.ox, self.Y(v1), "e", b))
        out.append(TX(self.X(t1) + 16, self.oy + 5, xl, "tm", fs, "start", b))
        if yl:
            out.append(TX(self.ox + 6, self.Y(v1) + 4, yl, "tm", fs, "start", b))
        return "".join(out)

    def curve(self, f, t0, t1, n=240, cls="e2", b=0):
        pts = [(self.X(t0 + (t1 - t0) * i / n), self.Y(f(t0 + (t1 - t0) * i / n))) for i in range(n + 1)]
        return PL(pts, cls, b)

    def stems(self, ns, vals, cls="n2", b=0, r=3.5, lcls="e"):
        out = []
        for n, v in zip(ns, vals):
            x, y = self.X(n), self.Y(v)
            if abs(v) > 1e-9:
                out.append(L(x, self.oy, x, y, lcls, b))
            out.append(C(x, y, r, cls, b))
        return "".join(out)

    def impulse(self, t, area, h_px, label, cls="e2", b=0, fs=15, lab_dx=10):
        """임펄스 화살표. 높이는 그림용(h_px 픽셀, 음수면 아래로)"""
        x = self.X(t)
        y2 = self.oy - h_px
        ly = y2 - 6 if h_px > 0 else y2 + 18
        return A(x, self.oy, x, y2, cls, b) + TX(x + lab_dx, ly, label, "tb", fs, "start", b)


def fmt(v, d=3):
    s = f"{v:.{d}f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


# =====================================================================
# 그림 (좌표는 모두 Python 으로 계산)
# =====================================================================
PI = math.pi

# p.31 한 주기 에너지: 높이 1 직사각형이 주기마다 쌓임
_p = Plot(40, 200, 60, 100)
FIG_ENERGY = SVG(
    _p.axes(0, 6.3, 0, 1.35, "t", ""),
    TX(40, 60, "|x(t)|² = 1 (크기 제곱이 늘 1)", "tb", 15, "start"),
    L(_p.X(0), _p.Y(1), _p.X(6), _p.Y(1), "e2"),
    R(_p.X(0), _p.Y(1), 2 * 60, 100, "n3", 1), TX(_p.X(1), 158, "넓이 T0", "tl", 15, "middle", 1),
    R(_p.X(2), _p.Y(1), 2 * 60, 100, "n", 2), TX(_p.X(3), 158, "T0", "tl", 15, "middle", 2),
    R(_p.X(4), _p.Y(1), 2 * 60, 100, "n", 2), TX(_p.X(5), 158, "T0", "tl", 15, "middle", 2),
    TX(_p.X(0), 222, "0", "tm", 14), TX(_p.X(2), 222, "T0", "tm", 14), TX(_p.X(4), 222, "2T0", "tm", 14),
    TX(_p.X(6), 222, "3T0", "tm", 14),
    TX(440, 85, "끝없이 쌓여요", "tm", 14, "end", 2),
    TX(240, 258, "한 주기 평균 전력 = T0 ÷ T0 = 1", "tb", 15, "middle", 3),
)

# p.32 단위원 위를 도는 점
_cx, _cy, _r = 240, 140, 95
_a60 = (_cx + _r * math.cos(PI / 3), _cy - _r * math.sin(PI / 3))
FIG_CIRCLE = SVG(
    A(120, _cy, 372, _cy, "e"), A(_cx, 255, _cx, 26, "e"),
    TX(376, _cy + 5, "실수", "tm", 14, "start"), TX(_cx + 8, 32, "허수", "tm", 14, "start"),
    C(_cx, _cy, _r, "hl"),
    C(_cx + _r, _cy, 6, "n2", 1), TX(_cx + _r + 8, _cy + 20, "시작: 1", "tb", 14, "start", 1),
    L(_cx, _cy, *_a60, "e2", 2), C(*_a60, 6, "n2", 2),
    TX(_a60[0] + 10, _a60[1] - 6, "시간이 가면 돌아요", "tb", 14, "start", 2),
    TX(_cx + 22, _cy - 10, "ωt", "t", 15, "start", 2),
    C(_cx, _cy - _r, 4, "n3", 3), C(_cx - _r, _cy, 4, "n3", 3), C(_cx, _cy + _r, 4, "n3", 3),
    TX(_cx - _r - 8, _cy - 8, "-1", "tm", 14, "end", 3),
    TX(20, 262, "한 바퀴(2π) 돌면 제자리", "tb", 15, "start", 3),
)

# p.33 조화 관계: k=1 은 T0 동안 1바퀴, k=2 는 2바퀴
_p = Plot(40, 135, 400 / (2 * PI), 45)
FIG_HARM = SVG(
    _p.axes(0, 2 * PI, -1.25, 1.25, "t"),
    L(40, 30, 70, 30, "e2", 1), TX(76, 35, "k = 1: 한 바퀴", "tb", 15, "start", 1),
    L(250, 30, 280, 30, "e", 2), TX(286, 35, "k = 2: 두 바퀴", "tb", 15, "start", 2),
    _p.curve(lambda t: math.cos(t), 0, 2 * PI, cls="e2", b=1),
    _p.curve(lambda t: math.cos(2 * t), 0, 2 * PI, cls="e", b=2),
    TX(_p.X(0), 212, "0", "tm", 14), TX(_p.X(2 * PI), 212, "T0", "tm", 14),
    L(_p.X(2 * PI), 80, _p.X(2 * PI), 192, "hl", 3),
    TX(240, 250, "T0가 끝나면 둘 다 제자리에 모여요", "tb", 15, "middle", 3),
)

# p.34 |x(t)| = 2|cos(0.5t)|
_p = Plot(40 + PI * 400 / (8 * PI), 200, 400 / (8 * PI), 70)
FIG_RECT = SVG(
    _p.axes(-PI, 7 * PI, 0, 2.3, "t", "|x(t)|"),
    _p.curve(lambda t: 2 * abs(math.cos(0.5 * t)), -PI, 7 * PI, n=400, cls="e2", b=1),
    TX(_p.ox - 14, _p.Y(2) + 5, "2", "tm", 14, "end"),
    TX(_p.X(0), 222, "0", "tm", 14), TX(_p.X(2 * PI), 222, "2π", "tm", 14),
    TX(_p.X(4 * PI), 222, "4π", "tm", 14), TX(_p.X(6 * PI), 222, "6π", "tm", 14),
    C(_p.X(PI), 200, 5, "n4", 2), C(_p.X(3 * PI), 200, 5, "n4", 2), C(_p.X(5 * PI), 200, 5, "n4", 2),
    TX(20, 258, "0이 되는 곳: π, 3π, 5π, ...", "tb", 15, "start", 2),
    TX(470, 258, "2π마다 반복", "tb", 15, "end", 3),
)

# p.36 직교좌표와 극좌표: r=2, 60도 -> (1, 1.73)
_o = (110, 225)
_s = 90
_P = (_o[0] + _s * 2 * math.cos(PI / 3), _o[1] - _s * 2 * math.sin(PI / 3))
FIG_POLAR = SVG(
    A(_o[0] - 20, _o[1], 440, _o[1], "e"), A(_o[0], _o[1] + 15, _o[0], 22, "e"),
    TX(444, _o[1] + 5, "x", "tm", 15, "start"), TX(_o[0] + 8, 30, "y", "tm", 15, "start"),
    L(*_o, *_P, "e2", 1), C(*_P, 6, "n2", 1),
    TX(_P[0] + 10, _P[1] - 4, "P", "tb", 15, "start", 1),
    TX((_o[0] + _P[0]) / 2 - 10, (_o[1] + _P[1]) / 2, "r = 2", "tb", 15, "end", 1),
    TX(_o[0] + 34, _o[1] - 10, "θ = 60°", "t", 14, "start", 1),
    L(_P[0], _P[1], _P[0], _o[1], "e", 2), L(_o[0], _P[1], _P[0], _P[1], "e", 2),
    TX(_P[0], _o[1] + 22, "x = r cos θ = 1", "t", 14, "middle", 2),
    TX(_P[0] + 8, (_P[1] + _o[1]) / 2 + 5, "y = r sin θ = 1.73", "t", 14, "start", 2),
    TX(285, 60, "극좌표: (r, θ) = (2, 60°)", "tb", 14, "start", 3),
    TX(285, 85, "직교좌표: (x, y) = (1, 1.73)", "tb", 14, "start", 3),
)

# p.37 감쇠 사인파와 포락선
_p = Plot(40, 135, 65, 95)
FIG_ENV = SVG(
    _p.axes(0, 6.1, -1.1, 1.1, "t"),
    _p.curve(lambda t: math.exp(-0.4 * t) * math.cos(2 * PI * t), 0, 6, n=480, cls="e2", b=1),
    _p.curve(lambda t: math.exp(-0.4 * t), 0, 6, cls="hl", b=2),
    _p.curve(lambda t: -math.exp(-0.4 * t), 0, 6, cls="hl", b=2),
    TX(120, 30, "포락선: 바깥을 감싼 선", "tb", 15, "start", 2),
    TX(300, 250, "r < 0 이면 점점 줄어요", "tb", 15, "middle", 3),
)

# p.38 이산시간 실수 지수: 왼쪽 alpha=1.25, 오른쪽 alpha=0.6
_pl = Plot(40, 210, 23, 30)
_pr = Plot(275, 210, 23, 140)
FIG_DTEXP = SVG(
    _pl.axes(-0.5, 7.3, 0, 0, "n"), _pr.axes(-0.5, 7.3, 0, 0, "n"),
    _pl.stems(range(8), [1.25 ** n for n in range(8)], b=1),
    _pr.stems(range(8), [0.6 ** n for n in range(8)], "n3", b=2),
    TX(125, 32, "1보다 큰 수를 곱하면", "tb", 15, "middle", 1),
    TX(125, 52, "점점 커져요", "t", 14, "middle", 1),
    TX(360, 32, "1보다 작은 수를 곱하면", "tb", 15, "middle", 2),
    TX(360, 52, "점점 작아져요", "t", 14, "middle", 2),
)

# p.38 alpha = -0.5
_p = Plot(60, 140, 55, 100)
_alt = [(-0.5) ** n for n in range(7)]
FIG_DTALT = SVG(
    _p.axes(-0.5, 6.4, -0.7, 1.15, "n"),
    _p.stems(range(7), _alt, b=1),
    TX(_p.X(0) + 10, _p.Y(1) + 5, "1", "tb", 14, "start", 2),
    TX(_p.X(1) + 10, _p.Y(-0.5) + 5, "-0.5", "tb", 14, "start", 2),
    TX(_p.X(2) + 10, _p.Y(0.25) - 2, "0.25", "tb", 14, "start", 2),
    TX(_p.X(3) + 10, _p.Y(-0.125) + 14, "-0.125", "tb", 14, "start", 2),
    TX(240, 255, "부호가 번갈아 바뀌면서 줄어요", "tb", 15, "middle", 3),
)

# p.39 cos(2 pi n / 8)
_p = Plot(40, 130, 24, 80)
FIG_DTCOS = SVG(
    _p.axes(-0.5, 16.3, -1.1, 1.1, "n"),
    _p.curve(lambda t: math.cos(2 * PI * t / 8), 0, 16, cls="e", b=2),
    _p.stems(range(17), [math.cos(2 * PI * n / 8) for n in range(17)], b=1),
    L(_p.X(0), 232, _p.X(8), 232, "e2", 3), L(_p.X(0), 225, _p.X(0), 239, "e2", 3),
    L(_p.X(8), 225, _p.X(8), 239, "e2", 3),
    TX(_p.X(4), 258, "8칸마다 같은 모양", "tb", 15, "middle", 3),
    TX(470, 30, "곡선 위에 정수 칸마다 점", "tm", 14, "end", 2),
)

# p.40 줄어드는 이산시간 사인파
_p = Plot(40, 135, 24, 100)
FIG_DTDAMP = SVG(
    _p.axes(-0.5, 16.3, -1.1, 1.1, "n"),
    _p.stems(range(17), [0.85 ** n * math.cos(PI * n / 4) for n in range(17)], b=1),
    _p.curve(lambda t: 0.85 ** t, 0, 16, cls="hl", b=2),
    _p.curve(lambda t: -(0.85 ** t), 0, 16, cls="hl", b=2),
    TX(470, 30, "포락선 ±|α|ⁿ", "tb", 15, "end", 2),
    TX(240, 258, "|α| < 1: 출렁이며 줄어요", "tb", 15, "middle", 3),
)

# p.41 8칸마다 제자리: e^{j(2pi/8)n}
_cx, _cy, _r = 240, 128, 82
_c8 = []
for n in range(8):
    a = 2 * PI * n / 8
    px, py = _cx + _r * math.cos(a), _cy - _r * math.sin(a)
    lx, ly = _cx + (_r + 28) * math.cos(a), _cy - (_r + 24) * math.sin(a) + 5
    bb = 1 if n < 4 else 2
    _c8.append(C(px, py, 6, "n2" if n == 0 else "n3", bb) + TX(lx, ly, f"n={n}", "tb", 14, "middle", bb))
FIG_CIRC8 = SVG(
    L(_cx - _r - 6, _cy, _cx + _r + 6, _cy, "e"), L(_cx, _cy + _r + 6, _cx, _cy - _r - 6, "e"), C(_cx, _cy, _r, "hl"),
    *_c8,
    TX(20, 268, "n=8에서 다시 n=0 자리: 주기 N = 8", "tb", 15, "start", 3),
    h=280,
)

# p.42 omega0 = 0, pi/2, pi
_rows = []
for i, (w, lab) in enumerate([(0, "ω0 = 0"), (PI / 2, "ω0 = π/2"), (PI, "ω0 = π")]):
    p = Plot(130, 55 + 85 * i, 26, 25)
    _rows.append(TX(12, p.oy + 5, lab, "tb", 15, "start", i + 1) + p.axes(-0.5, 12.3, 0, 0, "n", b=i + 1)
                 + p.stems(range(13), [math.cos(w * n) for n in range(13)], "n2" if i == 2 else "n3", b=i + 1, r=3))
FIG_FAST = SVG(*_rows, TX(240, 290, "π에서 +1, -1이 번갈아: 가장 빨라요", "tb", 15, "middle", 3), h=300)

# p.44 N=4 조화 관계: phi_k[1] = e^{jk pi/2}
_cx, _cy, _r = 240, 135, 85
_lab4 = [("k=0", 22, 20, "start"), ("k=1", 10, -8, "start"), ("k=2", -12, 20, "end"), ("k=3", 10, 22, "start")]
_c4 = []
for k in range(4):
    a = PI / 2 * k
    px, py = _cx + _r * math.cos(a), _cy - _r * math.sin(a)
    t, dx, dy, anc = _lab4[k]
    _c4.append(C(px, py, 6, "n2", 1) + TX(px + dx, py + dy, t, "tb", 15, anc, 1))
FIG_CIRC4 = SVG(
    A(110, _cy, 370, _cy, "e"), A(_cx, 250, _cx, 25, "e"), C(_cx, _cy, _r, "hl"),
    *_c4,
    TX(_cx + _r + 22, _cy - 12, "k=4도 여기", "tb", 15, "start", 2),
    TX(20, 262, "서로 다른 것은 k=0, 1, 2, 3 네 개뿐", "tb", 15, "start", 3),
)

# p.45 delta[n]
_p = Plot(240, 190, 36, 120)
FIG_DELTA = SVG(
    _p.axes(-5.5, 5.3, 0, 1.3, "n", "δ[n]"),
    _p.stems(range(-5, 6), [1 if n == 0 else 0 for n in range(-5, 6)], b=1),
    TX(_p.X(0), 212, "0", "tm", 14), TX(_p.X(0) - 8, _p.Y(1) + 5, "1", "tb", 14, "end", 1),
    TX(_p.X(0) + 14, _p.Y(1) + 5, "손뼉 한 번", "tb", 15, "start", 2),
    TX(240, 255, "나머지 칸은 모두 0", "tm", 15, "middle", 2),
)

# p.45 3 delta[n-2]
_p = Plot(160, 200, 40, 45)
FIG_DSHIFT = SVG(
    _p.axes(-3.5, 6.3, 0, 3.4, "n", "3δ[n-2]"),
    _p.stems(range(-3, 7), [3 if n == 2 else 0 for n in range(-3, 7)], b=1),
    TX(_p.X(0), 222, "0", "tm", 14), TX(_p.X(2), 222, "2", "tm", 14),
    TX(_p.X(2) + 12, _p.Y(3) + 5, "높이 3", "tb", 15, "start", 2),
    TX(240, 258, "2칸 오른쪽으로 옮기고, 3배", "tb", 15, "middle", 2),
)

# p.46 u[n]
_p = Plot(200, 190, 28, 110)
FIG_STEP = SVG(
    _p.axes(-5.5, 7.3, 0, 1.3, "n", "u[n]"),
    _p.stems(range(-5, 0), [0] * 5, "n3", b=1),
    _p.stems(range(0, 8), [1] * 8, b=2),
    TX(_p.X(0), 212, "0", "tm", 14),
    TX(_p.X(-3), 150, "켜기 전: 0", "tb", 15, "middle", 1),
    TX(_p.X(4), 55, "켠 뒤로 계속 1", "tb", 15, "middle", 2),
)

# p.46 u[n] - u[n-1] = delta[n]
_ud = []
for i, (lab, f) in enumerate([("u[n]", lambda n: 1 if n >= 0 else 0),
                              ("u[n-1]", lambda n: 1 if n >= 1 else 0),
                              ("빼면 δ[n]", lambda n: (1 if n >= 0 else 0) - (1 if n >= 1 else 0))]):
    p = Plot(250, 75 + 85 * i, 32, 45)
    ns = list(range(-3, 6))
    _ud.append(TX(12, p.oy - 12, lab, "tb", 15, "start", i + 1) + p.axes(-3.5, 5.3, 0, 0, "n", b=i + 1)
               + p.stems(ns, [f(n) for n in ns], "n2" if i == 2 else "n3", b=i + 1)
               + TX(p.X(0), p.oy + 18, "0", "tm", 14, "middle", i + 1))
FIG_UDIFF = SVG(*_ud, h=300)

# p.47 누적 합: 지금 n 까지 더하기
_rs = []
for i, (n_now, res) in enumerate([(-2, "합 = 0"), (3, "합 = 1")]):
    p = Plot(240, 110 + 120 * i, 28, 50)
    ns = list(range(-6, 7))
    _rs.append(p.axes(-6.5, 6.3, 0, 0, "m", b=i + 1)
               + p.stems(ns, [1 if n == 0 else 0 for n in ns], b=i + 1)
               + L(p.X(-6.5), p.oy - 68, p.X(n_now), p.oy - 68, "e2", i + 1)
               + L(p.X(n_now), p.oy - 75, p.X(n_now), p.oy + 8, "e", i + 1)
               + TX(p.X(n_now), p.oy + 24, f"n={n_now}", "tb", 14, "middle", i + 1)
               + TX(12, p.oy - 78, f"지금 n={n_now}까지 더하면", "t", 14, "start", i + 1)
               + TX(470, p.oy - 30, res, "tb", 16, "end", i + 1))
FIG_RSUM = SVG(*_rs, h=270)

# p.48 늦은 손뼉들을 모으면 계단
_p = Plot(70, 190, 40, 110)
_dk = [_p.stems([k], [1], "n2", b=min(k + 1, 4)) for k in range(0, 9)]
FIG_DSUM = SVG(
    _p.axes(-0.8, 9.3, 0, 0, "n"),
    *_dk,
    TX(_p.X(0), 212, "k=0", "tb", 14, "middle", 1), TX(_p.X(1), 232, "k=1", "tb", 14, "middle", 2),
    TX(_p.X(2), 212, "k=2", "tb", 14, "middle", 3),
    TX(_p.X(6), 45, "모두 모으면 u[n]", "tb", 16, "middle", 4),
    TX(20, 262, "δ[n-k]: k칸 늦게 치는 손뼉", "t", 15, "start", 1),
)

# p.49 x[n] delta[n-2] = x[2] delta[n-2]
_xs = list(range(-2, 4))
_xv = [n * n + 1 for n in _xs]
_p1 = Plot(210, 150, 40, 11)
_p2 = Plot(210, 250, 40, 11)
FIG_SAMP = SVG(
    TX(12, 40, "x[n] = n² + 1", "tb", 15, "start", 1),
    _p1.axes(-2.5, 4.3, 0, 0, "n", b=1), _p1.stems(_xs, _xv, "n3", b=1),
    TX(12, 200, "x[n]δ[n-2]", "tb", 15, "start", 2),
    _p2.axes(-2.5, 4.3, 0, 0, "n", b=2), _p2.stems(_xs, [v if n == 2 else 0 for n, v in zip(_xs, _xv)], b=2),
    C(_p1.X(2), _p1.Y(5), 11, "hl", 2), TX(_p2.X(2) + 12, _p2.Y(5) + 5, "5", "tb", 15, "start", 2),
    TX(_p1.X(3) + 12, _p1.Y(10) + 10, "10", "tm", 14, "start", 1),
    TX(_p1.X(2), _p1.oy + 18, "2", "tm", 14, "middle", 1), TX(_p2.X(2), _p2.oy + 18, "2", "tm", 14, "middle", 2),
    h=280,
)

# p.50 delta(t) 화살표
_p = Plot(150, 205, 60, 1)
FIG_DCT = SVG(
    _p.axes(-2, 4.5, 0, 0, "t"),
    _p.impulse(0, 1, 120, "1", b=1), TX(_p.X(0), 225, "0", "tm", 14),
    _p.impulse(3, 3, 120, "3", b=2), TX(_p.X(3), 225, "3", "tm", 14, "middle", 2),
    TX(240, 40, "숫자는 높이가 아니라 넓이예요", "tb", 15, "middle", 3),
    TX(_p.X(0) - 12, 150, "δ(t)", "t", 15, "end", 1), TX(_p.X(3) - 12, 150, "3δ(t-3)", "t", 15, "end", 2),
)

# p.51 폭 Delta, 높이 1/Delta: 넓이는 늘 1
_dd = []
for i, dlt in enumerate([1, 0.5, 0.25]):
    x0 = 40 + 150 * i
    w, h = 80 * dlt, 40 / dlt
    _dd.append(L(x0 - 10, 225, x0 + 110, 225, "e", i + 1) + R(x0, 225 - h, w, h, "n3", i + 1, 0)
               + TX(x0 + w + 6, 225 - h + 14, f"높이 {fmt(1 / dlt)}", "tb", 15, "start", i + 1)
               + TX(x0 + 45, 246, f"폭 Δ={fmt(dlt)}", "t", 14, "middle", i + 1))
FIG_DDELTA = SVG(*_dd, TX(240, 272, "폭 x 높이 = 넓이는 늘 1", "tb", 16, "middle", 3), h=285)

# p.52 u(t)
_p = Plot(230, 190, 60, 110)
FIG_UCT = SVG(
    _p.axes(-3.4, 3.6, 0, 1.3, "t", "u(t)"),
    L(_p.X(-3.4), _p.oy, _p.X(0), _p.oy, "e2", 1),
    L(_p.X(0), _p.Y(1), _p.X(3.4), _p.Y(1), "e2", 2),
    TX(_p.X(0), 212, "0", "tm", 14), TX(_p.X(0) - 8, _p.Y(1) + 5, "1", "tm", 14, "end"),
    TX(_p.X(-1.8), 170, "켜기 전 0", "tb", 15, "middle", 1),
    TX(_p.X(1.7), _p.Y(1) - 14, "켠 뒤로 계속 1", "tb", 15, "middle", 2),
    TX(240, 255, "t=0에서 스위치를 켜요", "tm", 15, "middle", 2),
)

# p.53 x(t) delta_Delta(t)
_p = Plot(120, 225, 45, 30)
_xf = lambda t: 3 + 0.6 * math.sin(1.1 * t + 0.4) + 0.3 * math.sin(2.3 * t)
FIG_XDELTA = SVG(
    _p.axes(-2, 7, 0, 0, "t"),
    _p.curve(_xf, -2, 7, cls="e2", b=1), TX(_p.X(6.2), _p.Y(_xf(6.2)) - 10, "x(t)", "tb", 15, "middle", 1),
    R(_p.X(0), 60, 18, _p.oy - 60, "n3", 2, 0), TX(_p.X(0) + 24, 70, "δΔ(t): 폭 Δ, 높이 1/Δ", "tb", 15, "start", 2),
    C(_p.X(0), _p.Y(_xf(0)), 6, "n2", 3), TX(_p.X(0) - 8, _p.Y(_xf(0)) - 14, "x(0)", "tb", 15, "end", 3),
    TX(240, 262, "좁은 칸 안의 x 값만 남아요", "tb", 15, "middle", 3),
)

# p.54 점프마다 임펄스
_p1 = Plot(70, 105, 62, 22)
_p2 = Plot(70, 195, 62, 1)
_seg = [(-0.8, 0), (1, 0), (1, 2), (2, 2), (2, -1), (4, -1), (4, 1), (5.6, 1)]
FIG_JUMP = SVG(
    TX(12, 45, "x(t)", "tb", 15, "start", 1),
    _p1.axes(-0.8, 5.6, 0, 0, "t", b=1),
    PL([(_p1.X(t), _p1.Y(v)) for t, v in _seg], "e2", 1),
    TX(_p1.X(1.5), _p1.Y(2) - 8, "2", "tm", 14, "middle", 1), TX(_p1.X(3), _p1.Y(-1) + 18, "-1", "tm", 14, "middle", 1),
    TX(_p1.X(4.8), _p1.Y(1) - 8, "1", "tm", 14, "middle", 1),
    TX(12, 160, "미분", "tb", 15, "start", 2),
    _p2.axes(-0.8, 5.6, 0, 0, "t", b=2),
    _p2.impulse(1, 2, 40, "+2", b=2), _p2.impulse(2, -3, -60, "-3", "e2", 2),
    _p2.impulse(4, 2, 40, "+2", b=2),
    TX(_p2.X(1), 215, "t=1", "t", 14, "middle", 2), TX(_p2.X(2) - 10, 185, "t=2", "t", 14, "end", 2),
    TX(_p2.X(4), 215, "t=4", "t", 14, "middle", 2),
    TX(470, 292, "끊긴 곳마다 점프 크기의 화살표", "tb", 15, "end", 3),
    h=300,
)

# p.55 시스템 상자
FIG_SYS = SVG(
    TX(40, 72, "x(t)", "tb", 16, "middle", 1), A(62, 67, 160, 67, "e2", 1),
    BOX(160, 42, 160, 50, "연속시간 시스템", "box2", "tb", 1),
    A(320, 67, 418, 67, "e2", 1), TX(440, 72, "y(t)", "tb", 16, "middle", 1),
    TX(40, 172, "x[n]", "tb", 16, "middle", 2), A(62, 167, 160, 167, "e2", 2),
    BOX(160, 142, 160, 50, "이산시간 시스템", "box2", "tb", 2),
    A(320, 167, 418, 167, "e2", 2), TX(440, 172, "y[n]", "tb", 16, "middle", 2),
    TX(240, 250, "신호가 들어가면 다른 신호가 나와요", "tb", 15, "middle", 3),
)

# p.56 손뼉과 메아리
_p = Plot(330, 150, 26, 55)
FIG_ECHO = SVG(
    L(20, 150, 150, 150, "e", 1), A(60, 150, 60, 70, "e2", 1),
    TX(85, 200, "손뼉(임펄스)", "tb", 15, "middle", 1),
    A(155, 150, 185, 150, "e", 2), BOX(185, 120, 110, 60, "시스템", "box2", "tb", 2),
    A(295, 150, 325, 150, "e", 2),
    L(330, 150, 468, 150, "e", 3),
    _p.curve(lambda t: math.exp(-0.55 * t) * math.sin(2.2 * t) * 1.3, 0, 5.2, cls="e2", b=3),
    TX(398, 215, "메아리 h(t)", "tb", 15, "middle", 3),
    TX(240, 258, "임펄스를 넣었을 때의 출력 = 임펄스 응답", "t", 15, "middle", 3),
)

# p.57 컨볼루션과 역컨볼루션
FIG_CONV = SVG(
    BOX(10, 110, 120, 50, "뇌 활동 x(t)", "box", "tb", 1, 15),
    A(130, 135, 175, 135, "e2", 1), BOX(175, 110, 130, 50, "뇌파 장비", "box2", "tb", 1, 15),
    A(305, 135, 350, 135, "e2", 1), BOX(350, 110, 120, 50, "기록 y(t)", "box", "tb", 1, 15),
    A(70, 80, 410, 80, "e2", 2), TX(240, 62, "컨볼루션: 앞으로 계산", "tb", 15, "middle", 2),
    A(410, 195, 70, 195, "e2", 3), TX(240, 228, "역컨볼루션: 거꾸로 되찾기", "tb", 15, "middle", 3),
)

# p.58 RC 회로: 전원을 켜면 축전기 전압이 천천히 따라옴 (RC = 1 예시)
_p = Plot(60, 205, 70, 130)
FIG_RC = SVG(
    _p.axes(-0.6, 5.4, 0, 1.25, "t"),
    L(_p.X(-0.6), _p.oy, _p.X(0), _p.oy, "e", 1), L(_p.X(0), _p.oy, _p.X(0), _p.Y(1), "e", 1),
    L(_p.X(0), _p.Y(1), _p.X(5.3), _p.Y(1), "e", 1),
    TX(_p.X(0) + 12, _p.Y(1) - 12, "입력: 전원 전압(갑자기 켬)", "tb", 15, "start", 1),
    _p.curve(lambda t: 1 - math.exp(-t), 0, 5.3, cls="e2", b=2),
    TX(_p.X(1.6), _p.Y(0.35), "출력: 축전기 전압", "tb", 15, "start", 2),
    TX(_p.X(1.6), _p.Y(0.35) + 20, "(천천히 따라와요)", "t", 14, "start", 2),
)

# p.59 자동차
FIG_CAR = SVG(
    L(30, 180, 450, 180, "e", 1), BOX(190, 120, 100, 60, "m", "box2", "tb", 1, 18),
    A(200, 95, 280, 95, "e", 1), TX(240, 82, "속도 v(t)", "tb", 15, "middle", 1),
    A(290, 150, 440, 150, "e2", 2), TX(365, 138, "엔진 힘 f(t)", "tb", 15, "middle", 2),
    A(190, 150, 40, 150, "e2", 3), TX(115, 138, "마찰 ρv(t)", "tb", 15, "middle", 3),
    TX(240, 235, "입력 f(t) → 출력 v(t)", "tb", 16, "middle", 4),
)

# p.60 통장: 매달 100만 원 입금, 이자 1%
_bal = []
_y = 0.0
for n in range(4):
    _y = 100 + 1.01 * _y
    _bal.append(_y)
_bars = []
for n, v in enumerate(_bal):
    x = 60 + 105 * n
    h = v * 0.4
    _bars.append(R(x, 220 - h, 60, h, "n3", n + 1, 0) + TX(x + 30, 214 - h, fmt(v, 2), "tb", 15, "middle", n + 1)
                 + TX(x + 30, 242, f"n={n}", "t", 14, "middle", n + 1))
FIG_BANK = SVG(L(40, 220, 460, 220, "e"), TX(20, 30, "잔고 y[n] (만 원)", "tb", 15, "start"), *_bars, h=270)


# =====================================================================
# 쪽 내용
# =====================================================================
S = []

# ---------------------------------------------------------------------
# p.31 (슬라이드 29) 주기 복소 지수: 에너지는 무한, 평균 전력은 유한
# ---------------------------------------------------------------------
_T0 = 2 * PI / PI                      # e^{j pi t} 의 주기
assert abs(_T0 - 2) < 1e-12
assert all(abs(abs(cmath.exp(1j * PI * t)) - 1) < 1e-12 for t in (0, 0.3, 1.7))
_E1 = 1 * _T0
assert _E1 == 2 and _E1 / _T0 == 1 and (3 * _E1) / (3 * _T0) == 1
assert abs(abs(cmath.exp(1j * 3 * 0.77)) ** 2 - 1) < 1e-12

S.append({"p": 31, "title": "주기 복소 지수: 에너지는 무한, 평균 전력은 유한",
 "pass1": [
  say("이 쪽은 빙글빙글 도는 신호가 가진 '양'을 재는 이야기예요.",
      K("cexp", "은") + " 원 위를 일정한 빠르기로 도는 점이라고 했죠.",
      "이 점은 영원히 돌아요. 그래서 모두 합친 양은 끝이 없어요.",
      "하지만 한 바퀴마다 쓰는 양은 늘 똑같아요."),
  analogy("매일 같은 시간표가 반복되는 하루",
      "매일 같은 시간표로 사는 사람이 평생 쓰는 시간은 끝이 없어요. 하지만 하루에 쓰는 시간은 늘 24시간이에요.",
      ("평생 쓰는 시간을 모두 더한 것", K("energy") + ": 끝이 없음(무한대)"),
      ("하루에 쓰는 시간", K("power") + ": 늘 같은 값"),
      ("매일 반복되는 하루", K("periodic") + "의 한 주기")),
 ],
 "pass2": [
  formula("한 주기 동안의 에너지",
      r"E_{period}=\int_0^{T_0}\left|e^{j\omega_0 t}\right|^2dt=\int_0^{T_0}1\,dt=T_0",
      [(r"E_{period}", "한 주기 동안 모은 에너지"),
       (r"\int_0^{T_0}\cdots dt", "0초부터 한 주기 끝($T_0$초)까지 그래프 아래 넓이를 구하라는 뜻(" + K("integ") + ")"),
       (r"\left|e^{j\omega_0 t}\right|^2", "도는 점의 크기를 제곱한 것. 반지름이 1인 원 위라서 늘 1"),
       (r"T_0", "높이 1, 폭 $T_0$인 직사각형 넓이 = $T_0$")],
      "한 주기 에너지는 '높이 1짜리 직사각형의 넓이'라서 $T_0$예요."),
  formula("평균 전력과 전체 에너지",
      r"P_{period}=\frac{1}{T_0}E_{period}=1,\qquad E_\infty=\infty",
      [(r"P_{period}", "한 주기 평균 전력: 에너지를 시간으로 나눈 값"),
       (r"\frac{1}{T_0}E_{period}", "$T_0$를 $T_0$로 나누니 1"),
       (r"E_\infty=\infty", "주기가 끝없이 이어지니 모두 더하면 무한대")],
      "모두 더하면 무한대지만, 시간으로 나눈 평균은 늘 1이에요."),
  compare("에너지와 평균 전력 구별", ["", K("energy"), K("power")],
      ["뜻", "크기 제곱을 모두 더한 양", "그 양을 걸린 시간으로 나눈 값"],
      ["한 주기", "$T_0$", "$1$"],
      ["끝없이 볼 때", "$\\infty$ (무한대)", "$1$"]),
  check("주기적인 " + K("cexp") + "에 대해 맞는 말은?",
      ["총 에너지도 평균 전력도 유한하다", "총 에너지는 무한대, 평균 전력은 유한하다",
       "총 에너지는 유한, 평균 전력은 무한대다"], 1,
      "한 바퀴마다 같은 양이 끝없이 쌓여서 총 에너지는 무한대예요. 시간으로 나누면 1로 일정해요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (150, 250, 1140, 330, "첫 줄: 주기 신호, 특히 복소 지수와 사인파는 총 에너지는 무한, 평균 전력은 유한이라는 말이에요."),
      (150, 370, 560, 412, "그래서 한 주기 동안의 에너지만 따로 생각해 보자는 말이에요."),
      (150, 440, 450, 635, "왼쪽 식: 크기 제곱이 1이라 한 주기 에너지는 $T_0$예요."),
      (495, 460, 770, 635, "오른쪽 식: 끝없이 보면 에너지는 무한대, 한 주기 평균 전력은 1이에요."),
      (795, 428, 1147, 665, "회색 상자: " + K("euler") + "과 오일러 항등식. 여기서는 $i$로 썼지만 이 과목은 $j$를 써요.")),
  bg("기초 다지기 b-8 적분은 넓이, 미분은 기울기",
      "적분 기호 $\\int$는 '그래프 아래 넓이를 구하라'고 읽으면 돼요.",
      "그래프 높이가 1로 평평하면, 넓이는 그냥 폭과 같아요.",
      "그래서 높이 1인 그래프를 $0$부터 $T_0$까지 적분하면 $T_0$예요."),
  steps("쉬운 숫자로: $x(t)=e^{j\\pi t}$",
      ["각주파수는 $\\pi$예요. 한 바퀴($2\\pi$) 도는 시간은 $T_0=2\\pi\\div\\pi=2$초예요.",
       "도는 점의 크기는 늘 $|e^{j\\pi t}|=1$, 제곱해도 $1$이에요.",
       "한 주기 에너지: 높이 $1$ $\\times$ 폭 $2$ = $2$예요.",
       "한 주기 평균 전력: $2\\div 2=1$이에요.",
       "세 주기를 보면 에너지 $6$, 평균 전력은 $6\\div 6=1$로 그대로예요."],
      "주기를 끝없이 늘리면 에너지는 무한대, 평균 전력은 계속 $1$이에요.",
      given="$x(t)=e^{j\\pi t}$, 크기 제곱은 늘 $1$"),
  figure("높이 1짜리 직사각형이 주기마다 쌓여요", FIG_ENERGY,
      "한 주기 넓이는 $T_0$. 끝없이 쌓이니 에너지는 무한대, 나눈 평균은 1이에요."),
  prof("에너지 부분은 엄청 중요한 부분은 아니라고 하셨어요.",
      "크기 제곱이 왜 1인지는 식이 복잡하니, 1이라고 그냥 외워 두라고 하셨어요.",
      "한 주기 평균 전력이 1이고 주기가 계속 반복되니, 끝없이 봐도 평균 전력은 1이라고 설명하셨어요."),
 ],
 "pass4": [
  check("$x(t)=e^{j3t}$의 평균 전력은 얼마일까요?", ["$0$", "$1$", "$3$", "무한대"], 1,
      "크기가 늘 1이라 제곱도 1이에요. 각주파수 3과 상관없이 평균 전력은 1이에요."),
  warn("헷갈리기 쉬운 점",
      "회색 상자의 $i$는 " + K("imag") + "예요. 교재와 이 과목은 같은 뜻으로 $j$를 써요.",
      "에너지가 무한대라고 이상한 신호가 아니에요. 이런 신호는 " + K("power") + "으로 크기를 재요.",
      "교수님이 이 부분은 엄청 중요하지는 않다고 하셨으니, 결론 한 줄만 확실히 기억해요."),
  english("시험 답안에 쓸 문장",
      "주기 복소 지수 신호는 크기가 항상 1이므로 한 주기 에너지는 $T_0$이고, 총 에너지는 무한대, 평균 전력은 1이다.",
      "크기 $1$ → 제곱 $1$ → 한 주기 넓이 $T_0$ → 끝없이 쌓여 무한대, 나누면 $1$.",
      "'에너지 무한, 전력 1' 여섯 글자로 외워요."),
 ]})

# ---------------------------------------------------------------------
# p.32 (슬라이드 30) 복소 지수의 주기 조건
# ---------------------------------------------------------------------
assert abs(2 * PI / 2 - PI) < 1e-12
assert abs(cmath.exp(1j * 2 * (0.4 + PI)) - cmath.exp(1j * 2 * 0.4)) < 1e-12
assert abs(2 * PI / 3 - 2.094) < 1e-3
assert abs(math.cos(3 * (0.4 + 2 * PI / 3)) - math.cos(3 * 0.4)) < 1e-12
assert abs(2 * PI / 4 - PI / 2) < 1e-12
assert abs(2 * PI / (2 * PI / 5) - 5) < 1e-12

S.append({"p": 32, "title": "복소 지수는 언제 제자리로 돌아올까: 주기 조건",
 "pass1": [
  say("원 위를 빙글빙글 도는 점은 언제 제자리로 돌아올까요?",
      "딱 한 바퀴를 다 돌았을 때예요. 그 걸린 시간이 주기예요.",
      "빨리 도는 점은 금방 돌아오고, 느리게 도는 점은 오래 걸려요."),
  figure("원 위를 도는 점", FIG_CIRCLE,
      "" + K("cplane") + " 위 원을 도는 점. 한 바퀴(2π)를 돌면 다시 시작 자리예요."),
 ],
 "pass2": [
  formula("주기라는 말을 식으로",
      r"x(t+T_0)=x(t)\;\Rightarrow\; e^{j\omega(t+T_0)}=e^{j\omega t}\;\Rightarrow\; e^{j\omega T_0}=1",
      [(r"x(t+T_0)=x(t)", "$T_0$만큼 뒤에 봐도 값이 같다 = 주기가 $T_0$"),
       (r"e^{j\omega(t+T_0)}", "지수의 덧셈은 곱셈으로 나뉘어서 $e^{j\omega t}e^{j\omega T_0}$"),
       (r"e^{j\omega T_0}=1", "양쪽이 같으려면 뒤에 곱한 것이 1이어야 해요")],
      "$T_0$ 동안 돈 각도 $\\omega T_0$만큼 가서 다시 1의 자리에 있어야 주기예요."),
  formula("주기 조건과 기본 각주파수",
      r"\omega T_0=2\pi K,\quad \omega_0=\frac{2\pi}{T_0},\quad \omega=K\omega_0",
      [(r"\omega T_0=2\pi K", "$T_0$ 동안 돈 각도가 한 바퀴($2\\pi$)의 정수배"),
       (r"K=0,\pm1,\pm2,\dots", "정수. 몇 바퀴를 돌았는지"),
       (r"\omega_0=\frac{2\pi}{T_0}", "$T_0$ 동안 딱 한 바퀴 도는 빠르기: 기본 " + K("angf")),
       (r"\omega=K\omega_0", "주기가 $T_0$가 되는 각주파수는 $\\omega_0$의 정수배")],
      "한 바퀴가 $2\\pi$ " + K("rad") + "이라서, 도는 각도가 $2\\pi$의 정수배일 때 제자리예요."),
  compare("빨리 돌수록 주기가 짧아요", [K("angf") + " $\\omega$", K("fper") + " $T_0=2\\pi/\\omega$"],
      ["$\\omega=1$", "$2\\pi\\approx 6.28$초"],
      ["$\\omega=2$", "$\\pi\\approx 3.14$초"],
      ["$\\omega=4$", "$\\pi/2\\approx 1.57$초"]),
  check("$e^{j\\omega T_0}=1$이 되려면 $\\omega T_0$는 어떤 값이어야 할까요?",
      ["$\\pi$의 정수배", "$2\\pi$의 정수배", "항상 $1$"], 1,
      "단위원 위에서 1의 자리로 돌아오려면 한 바퀴($2\\pi$)의 정수배만큼 돌아야 해요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (140, 243, 545, 310, K("cexp") + " $x(t)=e^{j\\omega t}$를 생각해요."),
      (140, 318, 480, 380, "주기가 $T_0$라는 뜻: $T_0$만큼 밀어도 똑같다."),
      (140, 385, 600, 450, "그러려면 $e^{j\\omega T_0}=1$이어야 해요. 지수의 덧셈이 곱셈으로 나뉜 결과예요."),
      (240, 480, 660, 532, "파란 상자: 주기 조건 $\\omega T_0=2\\pi K$."),
      (140, 545, 660, 710, "기본 각주파수 $\\omega_0=2\\pi/T_0$로 두면, $\\omega$는 $\\omega_0$의 정수배여야 해요.")),
  bg("기초 다지기 b-6 오일러 공식과 회전",
      "$e^{j\\theta}$는 " + K("ucirc") + " 위, 각도 $\\theta$ 자리에 있는 점이에요.",
      "$\\theta=2\\pi$면 한 바퀴를 돌아 1의 자리로 돌아와요. 그래서 $e^{j2\\pi}=1$이에요.",
      "$e^{j4\\pi}=1$, $e^{j6\\pi}=1$도 모두 1이에요. 두 바퀴, 세 바퀴니까요."),
  steps("$e^{j2t}$의 " + K("fper") + " 구하기",
      ["각주파수는 $\\omega=2$예요. 1초에 $2$ " + K("rad") + "씩 돌아요.",
       "한 바퀴($2\\pi$)를 돌려면 $2\\times T_0=2\\pi$가 되어야 해요.",
       "그래서 $T_0=2\\pi\\div 2=\\pi\\approx 3.14$초예요.",
       "확인: $e^{j2(t+\\pi)}=e^{j2t}e^{j2\\pi}=e^{j2t}\\times 1$. 똑같아요."],
      "$T_0=\\pi$"),
  steps("$\\cos(3t)$의 " + K("fper") + " 구하기",
      ["$\\cos$ 안의 $t$ 앞 숫자가 각주파수예요: $\\omega=3$.",
       "한 바퀴를 돌 때까지: $3\\times T_0=2\\pi$.",
       "그래서 $T_0=2\\pi/3\\approx 2.09$초예요.",
       "확인: $\\cos(3(t+2\\pi/3))=\\cos(3t+2\\pi)=\\cos(3t)$."],
      "$T_0=2\\pi/3$"),
  prof("주기라면 $x(t+T_0)=x(t)$가 되어야 하고, 지수에서는 위의 덧셈이 곱셈으로 바뀌니 $e^{j\\omega T_0}$가 1이어야 한다고 하셨어요.",
      "유닛 서클에서 $2\\pi$만큼 돌았을 때가 제자리라서, $\\omega T_0$가 $2\\pi$의 정수배면 된다고 설명하셨어요.",
      "각주파수로 말하니 어려워 보이지만, 주기로 보면 그렇게 어려운 내용이 아니라고 하셨어요."),
 ],
 "pass4": [
  check("$e^{j4t}$의 " + K("fper") + "는?", ["$4$", "$\\pi/2$", "$2\\pi$", "$\\pi/4$"], 1,
      "$T_0=2\\pi/\\omega=2\\pi/4=\\pi/2$예요."),
  exam("연습 문제 (p.32 주기 조건)",
      "Find the fundamental period of $x(t)=e^{j(2\\pi/5)t}$.",
      "$x(t)=e^{j(2\\pi/5)t}$의 기본 주기를 구하세요.",
      ["각주파수를 읽어요: $\\omega=2\\pi/5$.",
       "기본 주기 공식: $T_0=2\\pi/\\omega$.",
       "$T_0=2\\pi\\div(2\\pi/5)=5$."],
      "$T_0=5$"),
  warn("헷갈리기 쉬운 점",
      "$\\omega$는 이 신호의 각주파수, $\\omega_0$는 '딱 한 바퀴'짜리 기본 각주파수예요. 슬라이드 아래 상자는 $\\omega$가 $\\omega_0$의 정수배라는 말이에요.",
      "$K=0$이면 $\\omega=0$, 신호는 늘 1인 상수예요. 이때 기본 주기는 정해지지 않아요(p.43 표)."),
  english("시험 답안에 쓸 문장",
      "$e^{j\\omega_0 t}$는 $\\omega_0 T_0=2\\pi$일 때 제자리로 돌아오므로 기본 주기는 $T_0=2\\pi/|\\omega_0|$이다.",
      "주기 = 한 바퀴($2\\pi$) ÷ 도는 빠르기($\\omega_0$).",
      "'한 바퀴 나누기 빠르기'로 외워요."),
 ]})

# ---------------------------------------------------------------------
# p.33 (슬라이드 31) 조화 관계 복소 지수 (연속시간)
# ---------------------------------------------------------------------
_w0 = 2.0
_T0 = 2 * PI / _w0
assert abs(_T0 - PI) < 1e-12
for _k in (2, 3):
    _Tk = 2 * PI / (_k * _w0)
    assert abs(_T0 / _Tk - _k) < 1e-12
assert abs(2 * PI / 4 - PI / 2) < 1e-12 and abs(2 * PI / 6 - PI / 3) < 1e-12

S.append({"p": 33, "title": "조화 관계 복소 지수: 기본 빠르기의 정수배",
 "pass1": [
  say("원 위를 도는 점을 여러 개 준비해요.",
      "첫째 점이 한 바퀴 도는 동안, 둘째 점은 두 바퀴, 셋째 점은 세 바퀴를 돌아요.",
      "그래서 첫째 점이 한 바퀴를 마치면 모든 점이 같이 제자리에 모여요.",
      "이런 점들의 모음을 " + K("harm") + "라고 해요."),
  figure("한 바퀴, 두 바퀴", FIG_HARM,
      "기본 주기 동안 k=1은 한 번, k=2는 두 번 출렁이고, 끝에서 둘 다 제자리예요."),
 ],
 "pass2": [
  formula("조화 관계 복소 지수의 정의",
      r"\phi_k(t)=e^{jk\omega_0 t},\quad k=0,\pm1,\pm2,\dots",
      [(r"\phi_k(t)", "k번째 신호. $\\phi$는 '파이'라고 읽어요"),
       (r"\omega_0", "기본 " + K("angf") + " (첫째 점의 빠르기)"),
       (r"k\omega_0", "기본 빠르기의 k배로 도는 점"),
       (r"k=0", "$e^0=1$, 늘 1인 상수 신호")],
      "기본 빠르기 $\\omega_0$의 정수배로 도는 " + K("cexp") + "들의 모음이에요."),
  compare("k에 따라 달라지는 것", ["k", "각주파수", K("fper")],
      ["$0$", "$0$", "없음(상수 1)"],
      ["$\\pm1$", "$\\omega_0$", "$T_0$"],
      ["$\\pm2$", "$2\\omega_0$", "$T_0/2$"],
      ["$\\pm3$", "$3\\omega_0$", "$T_0/3$"]),
  check("$\\phi_3(t)$는 길이 $T_0$ 동안 몇 바퀴를 돌까요?", ["1바퀴", "3바퀴", "1/3바퀴"], 1,
      "기본 주기가 $T_0/3$이니 $T_0$ 동안 3번 돌아요. $|k|$번 돈다고 기억해요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (140, 240, 700, 350, "정의: 기본 각주파수 $\\omega_0$의 정수배 주파수를 가진 복소 지수들 $\\phi_k(t)=e^{jk\\omega_0 t}$."),
      (140, 360, 500, 420, "$k=0$이면 $\\phi_0(t)=1$, 상수 신호예요."),
      (140, 430, 500, 550, "$k\\neq 0$이면 기본 각주파수 $|k|\\omega_0$, 기본 주기 $T_0/|k|$예요."),
      (140, 555, 700, 710, "그래서 $T_0$도 여전히 주기이고, $T_0$ 동안 $|k|$번 돌아요."),
      (780, 300, 1290, 650, "그래프: 파란 점선 k=1(기본), 주황 점선 k=2(2배음). 검은 선은 이런 것들이 섞인 복잡한 신호 예시예요.")),
  steps("$\\omega_0=2$일 때 k번째 신호",
      ["기본 주기: $T_0=2\\pi/2=\\pi$예요.",
       "$k=2$: 각주파수 $4$, 기본 주기 $2\\pi/4=\\pi/2$예요.",
       "$T_0=\\pi$ 동안 몇 번? $\\pi\\div(\\pi/2)=2$번이에요.",
       "$k=3$: 각주파수 $6$, 기본 주기 $\\pi/3$, $T_0$ 동안 $3$번이에요."],
      "k번째 신호는 $T_0$ 동안 정확히 $|k|$번 돌고 제자리예요.",
      given="$\\phi_k(t)=e^{jk2t}$"),
  prof("하모닉은 같은 모양인데 주기만 좁혀진 세트라고 하셨어요.",
      "이상하게 생긴 신호도 기본 신호와 그 하모닉들의 합으로 표현할 수 있고, 이건 나중에 배운다고 하셨어요.",
      "k가 2면 주기가 절반으로 줄지만, k=1의 주기 안에 k=2도 딱 맞아떨어진다고 설명하셨어요."),
  bg("기초 다지기 b-3 각도, 라디안, 사인과 코사인",
      "각주파수가 2배면 같은 시간에 2배 많이 돌아요.",
      "그래서 주기는 절반이 돼요. 각주파수와 주기는 반비례예요."),
 ],
 "pass4": [
  check("$k=-2$일 때 $\\phi_{-2}(t)$의 기본 주기는?", ["$-T_0/2$", "$T_0/2$", "$2T_0$"], 1,
      "기본 주기는 $T_0/|k|$라서 절댓값을 써요. 주기는 음수가 아니에요."),
  warn("헷갈리기 쉬운 점",
      "'주기'와 '" + K("fper") + "'는 달라요. $\\phi_2$의 기본 주기는 $T_0/2$지만, $T_0$도 주기 중 하나예요.",
      "$k=0$인 $\\phi_0=1$도 모음에 들어가요. 상수 신호예요."),
  english("시험 답안에 쓸 문장",
      "조화 관계 복소 지수 $\\phi_k(t)=e^{jk\\omega_0 t}$는 기본 각주파수가 $|k|\\omega_0$, 기본 주기가 $T_0/|k|$이며, 모두 $T_0$를 주기로 가진다.",
      "k배 빨리 돌면 주기는 1/k, 그래도 $T_0$마다 다 같이 제자리.",
      "'k배 빠르게, k번 돌고, 다 같이 제자리'."),
 ]})

# ---------------------------------------------------------------------
# p.34 (슬라이드 32) 예제 x(t) = e^{j2t} + e^{j3t}
# ---------------------------------------------------------------------
for _t in (0.0, 0.7, 2.3, PI, 5.1):
    _x = cmath.exp(2j * _t) + cmath.exp(3j * _t)
    assert abs(_x - 2 * cmath.exp(2.5j * _t) * math.cos(0.5 * _t)) < 1e-12
    assert abs(abs(_x) - 2 * abs(math.cos(0.5 * _t))) < 1e-12
assert abs(2 * abs(math.cos(0.5 * PI))) < 1e-12 and abs(2 * abs(math.cos(0.5 * 2 * PI)) - 2) < 1e-12
assert 2.5 - 0.5 == 2 and 2.5 + 0.5 == 3

S.append({"p": 34, "title": "예제: 도는 점 두 개를 더하면",
 "pass1": [
  say("빠르기가 다른 도는 점 두 개를 더하면 어떤 모양이 될까요?",
      "두 점이 같은 쪽에 있으면 크게, 반대쪽에 있으면 작게 합쳐져요.",
      "그래서 합친 크기가 커졌다 작아졌다를 반복해요. 이 쪽은 그 예제예요."),
  say("수업에서는 시간 관계로 이 쪽을 넘어갔어요.",
      "그래도 " + K("euler") + "을 연습하기 좋은 예제라서 가볍게 봐요."),
 ],
 "pass2": [
  formula("오일러 공식으로 cos, sin 뽑기",
      r"\cos\theta=\frac{e^{j\theta}+e^{-j\theta}}{2},\qquad \sin\theta=\frac{e^{j\theta}-e^{-j\theta}}{2j}",
      [(r"e^{j\theta}+e^{-j\theta}", "위로 도는 점과 아래로 도는 점을 더하면 허수 부분이 지워져요"),
       (r"\frac{\cdots}{2}", "둘을 더하면 $2\\cos\\theta$라서 2로 나눠요"),
       (r"\frac{\cdots}{2j}", "빼면 $2j\\sin\\theta$라서 $2j$로 나눠요")],
      "cos은 두 복소 지수의 평균, sin은 두 복소 지수의 차이를 $2j$로 나눈 것이에요."),
  formula("예제를 한 줄로",
      r"x(t)=e^{j2t}+e^{j3t}=e^{j2.5t}\left(e^{-j0.5t}+e^{j0.5t}\right)=2e^{j2.5t}\cos(0.5t)",
      [(r"e^{j2.5t}", "2와 3의 가운데 빠르기 2.5를 앞으로 꺼냈어요"),
       (r"e^{-j0.5t}+e^{j0.5t}", "위의 cos 공식 모양: $2\\cos(0.5t)$"),
       (r"|x(t)|=2|\cos(0.5t)|", "$e^{j2.5t}$의 크기는 1이라서 크기는 $2|\\cos(0.5t)|$")],
      "두 점을 더한 신호의 크기는 $2|\\cos(0.5t)|$예요."),
  check("$\\cos\\theta$를 복소 지수로 바르게 쓴 것은?",
      ["$e^{j\\theta}+e^{-j\\theta}$", "$\\frac{e^{j\\theta}+e^{-j\\theta}}{2}$", "$\\frac{e^{j\\theta}-e^{-j\\theta}}{2j}$"], 1,
      "더해서 2로 나누면 cos, 빼서 $2j$로 나누면 sin이에요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (320, 255, 565, 310, "예제: $x(t)=e^{j2t}+e^{j3t}$"),
      (230, 355, 600, 525, "Euler's form: 가운데 빠르기 $e^{j2.5t}$를 앞으로 빼고, 괄호 안을 $2\\cos(0.5t)$로 바꿨어요."),
      (230, 550, 515, 655, "Magnitude(크기): $|x(t)|=2|\\cos(0.5t)|$"),
      (680, 255, 1185, 470, "크기 그래프: 높이 2, $2\\pi$마다 반복돼요. 교재 Figure 1.22, 전파 정류된 사인파라는 이름이에요."),
      (695, 528, 1148, 662, "오른쪽 아래 상자: " + K("euler") + "에서 cos, sin을 뽑아내는 식이에요.")),
  steps("크기를 손으로 확인하기",
      ["가운데 빠르기: $(2+3)\\div 2=2.5$, 차이의 절반: $0.5$.",
       "$e^{j2t}=e^{j2.5t}e^{-j0.5t}$, $e^{j3t}=e^{j2.5t}e^{j0.5t}$로 나눠 써요.",
       "괄호 안: $e^{-j0.5t}+e^{j0.5t}=2\\cos(0.5t)$.",
       "$t=0$: $|x|=2|\\cos 0|=2$. 두 점이 같은 자리에서 출발해요.",
       "$t=\\pi$: $|x|=2|\\cos(\\pi/2)|=0$. 두 점이 정반대라 지워져요.",
       "$t=2\\pi$: $|x|=2|\\cos\\pi|=2$. 다시 최대예요."],
      "$|x(t)|=2|\\cos(0.5t)|$, 최대 2, 0이 되는 곳 $t=\\pi, 3\\pi, \\dots$"),
  figure("크기 |x(t)| 그래프", FIG_RECT,
      "위로 볼록한 봉우리가 $2\\pi$마다 반복돼요. $\\pi$, $3\\pi$에서 0이에요."),
  prof("교수님은 수업 시간에 이 쪽(슬라이드 32)은 넘어가겠다고 하셨어요.",
      "그러니 계산 흐름만 따라가 보고, 오일러 공식 자체를 확실히 익히는 데 집중해요."),
 ],
 "pass4": [
  exam("교재 Example 1.5 (p.34)",
      "For $x(t)=e^{j2t}+e^{j3t}$, find $|x(t)|$ and the first positive $t$ where $|x(t)|=0$.",
      "두 복소 지수의 합의 크기를 구하고, 크기가 처음으로 0이 되는 양수 $t$를 찾으세요.",
      ["가운데 빠르기 $2.5$를 묶어요: $x(t)=e^{j2.5t}(e^{-j0.5t}+e^{j0.5t})$.",
       "괄호 안은 $2\\cos(0.5t)$, 앞의 $e^{j2.5t}$는 크기 1이에요.",
       "$|x(t)|=2|\\cos(0.5t)|$.",
       "$\\cos(0.5t)=0$이 처음 되는 곳: $0.5t=\\pi/2$, $t=\\pi$."],
      "$|x(t)|=2|\\cos(0.5t)|$, 처음 0이 되는 곳은 $t=\\pi$"),
  warn("헷갈리기 쉬운 점",
      "그래프 세로축은 $x(t)$가 아니라 크기 $|x(t)|$예요. 그래서 아래로 내려가지 않아요.",
      "$|e^{j2.5t}|=1$이라서 크기 계산에서 빠져요. 복소 지수 하나의 크기는 늘 1이에요."),
 ]})

# ---------------------------------------------------------------------
# p.35 (슬라이드 33) 일반 복소 지수: C 는 극좌표, a 는 직교좌표
# ---------------------------------------------------------------------
_C = 2 * cmath.exp(1j * PI / 3)
_a = -0.5 + 3j
for _t in (0.0, 0.8, 2.0):
    _lhs = _C * cmath.exp(_a * _t)
    _rhs = 2 * math.exp(-0.5 * _t) * cmath.exp(1j * (3 * _t + PI / 3))
    assert abs(_lhs - _rhs) < 1e-12
assert abs(abs(_C * cmath.exp(_a * 2)) - 2 * math.exp(-1)) < 1e-12 and abs(2 * math.exp(-1) - 0.74) < 0.005
# 슬라이드 식 e^{j(w0+phi)t} 는 t=2 에서 다르다 (오타 확인)
assert abs(cmath.exp(1j * (3 + PI / 3) * 2) - cmath.exp(1j * (3 * 2 + PI / 3))) > 0.1

S.append({"p": 35, "title": "일반 복소 지수: C와 a가 모두 복소수일 때",
 "pass1": [
  say("지금까지는 앞에 곱하는 수와 지수의 수가 간단한 경우만 봤어요.",
      "이제 둘 다 " + K("cnum") + "인, 가장 일반적인 " + K("cexp") + "를 봐요.",
      "결과를 먼저 말하면: 원 위를 도는 점인데, 원이 점점 커지거나 작아져요."),
  analogy("원 위를 도는 점, 그런데 원 크기가 변해요",
      "도는 점이 한 바퀴 돌 때마다 원이 조금씩 줄어들면 소용돌이처럼 안으로 말려 들어가요.",
      ("도는 빠르기", "지수의 허수 부분"),
      ("원이 커지거나 줄어드는 빠르기", "지수의 실수 부분"),
      ("출발할 때의 크기와 각도", "앞에 곱한 복소수의 크기와 각도")),
 ],
 "pass2": [
  formula("C는 극좌표, a는 직교좌표로",
      r"C=|C|e^{j\phi},\qquad a=r+j\omega_0",
      [(r"|C|", "C의 크기(원점에서 거리)"),
       (r"e^{j\phi}", "C의 각도 $\\phi$. 출발 각도, " + K("phase")),
       (r"r", "a의 실수 부분: 커지거나 줄어드는 빠르기"),
       (r"j\omega_0", "a의 허수 부분: 도는 빠르기")],
      "C는 '크기와 각도'로, a는 '실수 부분과 허수 부분'으로 나눠 적어요."),
  formula("둘을 합치면 (바르게 고친 식)",
      r"Ce^{at}=|C|e^{j\phi}e^{(r+j\omega_0)t}=|C|e^{rt}e^{j(\omega_0 t+\phi)}",
      [(r"|C|e^{rt}", "크기 부분: 시간에 따라 커지거나 줄어요"),
       (r"e^{j(\omega_0 t+\phi)}", "각도 부분: 각도 $\\phi$에서 출발해 $\\omega_0$ 빠르기로 돌아요")],
      "크기는 $|C|e^{rt}$, 도는 각도는 $\\omega_0 t+\\phi$예요."),
  compare("극좌표와 직교좌표", ["", "극좌표(polar)", "직교좌표(rectangular)"],
      ["적는 것", "크기와 각도", "실수 부분과 허수 부분"],
      ["모양", "$|C|e^{j\\phi}$", "$r+j\\omega_0$"],
      ["이 쪽에서", "$C$를 적을 때", "$a$를 적을 때"]),
  check("$a=r+j\\omega_0$에서 신호가 커지거나 줄어드는 것을 정하는 것은?", ["$r$", "$\\omega_0$", "$\\phi$"], 0,
      "실수 부분 $r$은 $e^{rt}$가 되어 크기를 바꿔요. $\\omega_0$는 도는 빠르기예요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (140, 228, 645, 268, "General Complex Exponential Signals: 가장 일반적인 복소 지수 신호"),
      (140, 290, 905, 330, "지금까지는 실수 지수와 주기 복소 지수(사인파)만 봤어요."),
      (140, 352, 645, 392, "이제 $C$도 " + K("cnum") + "일 수 있어요."),
      (140, 415, 850, 455, "C는 극좌표(polar form), a는 직교좌표(rectangular form)로 적어요."),
      (190, 510, 370, 625, "$C=|C|e^{j\\phi}$, $a=r+j\\omega_0$"),
      (515, 525, 1105, 605, "둘을 넣고 정리한 식. 맨 오른쪽 지수는 $j(\\omega_0 t+\\phi)$가 맞아요(pass4 참고).")),
  bg("기초 다지기 b-4 지수함수와 e",
      "$e^{A+B}=e^Ae^B$: 지수의 덧셈은 곱셈으로 나뉘어요.",
      "그래서 $e^{(r+j\\omega_0)t}=e^{rt}e^{j\\omega_0 t}$로 나눌 수 있어요.",
      "$e^{rt}$는 보통 수라서 크기를, $e^{j\\omega_0 t}$는 크기 1로 돌기만 해요."),
  steps("쉬운 숫자로 합쳐 보기",
      ["$C=2e^{j\\pi/3}$: 크기 $2$, 출발 각도 $\\pi/3$(60도).",
       "$a=-0.5+j3$: $r=-0.5$, $\\omega_0=3$.",
       "합치면 $Ce^{at}=2e^{-0.5t}e^{j(3t+\\pi/3)}$.",
       "$t=0$일 때 크기: $2e^{0}=2$.",
       "$t=2$일 때 크기: $2e^{-1}\\approx 0.74$. 점점 줄어요."],
      "크기는 $2e^{-0.5t}$로 줄고, 각도는 $3t+\\pi/3$으로 돌아요."),
  prof("왜 C는 극좌표, a는 직교좌표로 쓰냐고 물으면, 사실 둘 다 어느 쪽으로도 표현할 수 있다고 하셨어요.",
      "대입하면 $rt$는 앞으로 나오고 $j$가 붙은 부분만 묶인다고 설명하셨어요.",
      "r이 0이면(순수 허수) 사인파, r이 있으면 r에 따라 그래프가 바뀐다고 하셨어요."),
 ],
 "pass4": [
  warn("슬라이드 식의 오타",
      "슬라이드 맨 오른쪽 $e^{j(\\omega_0+\\phi)t}$는 $e^{j(\\omega_0 t+\\phi)}$가 맞아요. $\\phi$에는 $t$가 곱해지지 않아요.",
      "왜냐하면 $e^{j\\phi}$는 처음부터 곱해진 고정된 각도라서, 시간과 함께 늘지 않기 때문이에요.",
      "다음 쪽(p.37) 식도 같은 모양으로 적혀 있으니 똑같이 고쳐 읽어요."),
  check("$C=3e^{j\\pi/4}$, $a=j2$일 때 $Ce^{at}$의 크기는?", ["$3$으로 일정", "$3e^{2t}$", "$2$로 일정"], 0,
      "$r=0$이라 $e^{rt}=1$이에요. 크기는 $|C|=3$으로 일정하고, 돌기만 해요."),
  english("시험 답안에 쓸 문장",
      "$C=|C|e^{j\\phi}$, $a=r+j\\omega_0$이면 $Ce^{at}=|C|e^{rt}e^{j(\\omega_0 t+\\phi)}$이며, $r$은 크기의 증가/감소를, $\\omega_0$는 회전 속도를 정한다.",
      "실수 부분 r → 크기, 허수 부분 $\\omega_0$ → 도는 빠르기.",
      "'r은 크기, 오메가는 회전'."),
 ]})

# ---------------------------------------------------------------------
# p.36 (슬라이드 34) 극좌표와 직교좌표
# ---------------------------------------------------------------------
assert abs(2 * math.cos(PI / 3) - 1) < 1e-12 and abs(2 * math.sin(PI / 3) - 1.732) < 1e-3
assert abs(abs(1 + 1j) - 1.414) < 1e-3 and abs(cmath.phase(1 + 1j) - PI / 4) < 1e-12
assert abs(abs(3j) - 3) < 1e-12 and abs(cmath.phase(3j) - PI / 2) < 1e-12

S.append({"p": 36, "title": "한 점을 적는 두 가지 방법: 직교좌표와 극좌표",
 "pass1": [
  say("평면 위 한 점의 자리를 말하는 방법은 두 가지예요.",
      "하나: 가로로 몇, 세로로 몇. 이것이 직교좌표예요.",
      "둘: 원점에서 거리 몇, 각도 몇. 이것이 극좌표예요.",
      "같은 점을 다르게 말할 뿐이라서, 서로 바꿀 수 있어요."),
  figure("같은 점, 두 가지 주소", FIG_POLAR,
      "P는 거리 2, 각도 60도. 가로 1, 세로 약 1.73이라고 해도 같은 점이에요."),
 ],
 "pass2": [
  formula("극좌표 → 직교좌표",
      r"x=r\cos\theta,\qquad y=r\sin\theta",
      [(r"r", "원점에서 점까지 거리(반지름)"),
       (r"\theta", "가로축에서 잰 각도. '세타'라고 읽어요"),
       (r"r\cos\theta", "그림자를 가로축에 내린 길이 = x"),
       (r"r\sin\theta", "그림자를 세로축에 내린 길이 = y")],
      "거리와 각도를 알면 cos, sin으로 가로, 세로를 구해요."),
  compare("두 좌표계", ["", "직교좌표", "극좌표"],
      ["적는 것", "$(x, y)$", "$(r, \\theta)$"],
      ["복소수로", "$x+jy$", "$re^{j\\theta}$"],
      ["편한 때", "더하기, 빼기", "곱하기, 돌리기"]),
  check("극좌표 $(r,\\theta)$에서 $r$은 무엇일까요?", ["가로 길이", "원점에서의 거리", "각도"], 1,
      "$r$은 원점에서 점까지의 거리예요. 각도는 $\\theta$예요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (140, 215, 610, 252, "일반 복소 지수 신호를 이해하려고 좌표 두 가지를 복습하는 쪽이에요."),
      (175, 440, 345, 545, "앞 쪽의 $C=|C|e^{j\\phi}$(극좌표), $a=r+j\\omega_0$(직교좌표)"),
      (590, 325, 900, 425, "Rectangular Coordinates: 점 P를 $(x, y)$로 적어요."),
      (590, 425, 790, 610, "원점에서 거리 $r$, 각도 $\\theta$: 극좌표예요."),
      (795, 495, 1045, 600, "$y=r\\sin\\theta$, 그리고 Polar Coordinates 이름표"),
      (625, 612, 800, 652, "$x=r\\cos\\theta$")),
  steps("극좌표 ↔ 직교좌표 손계산",
      ["$r=2$, $\\theta=60°$: $x=2\\cos 60°=2\\times 0.5=1$.",
       "$y=2\\sin 60°\\approx 2\\times 0.866=1.73$.",
       "거꾸로 $1+j1$: 거리 $r=\\sqrt{1^2+1^2}=\\sqrt2\\approx 1.41$.",
       "각도: 가로와 세로가 같으니 $45°$, 즉 $\\pi/4$예요."],
      "$(2, 60°)=(1, 1.73)$, 그리고 $1+j1=\\sqrt2 e^{j\\pi/4}$"),
  bg("기초 다지기 b-5 복소수와 복소평면",
      K("cplane") + "은 가로축이 실수, 세로축이 허수인 평면이에요.",
      K("cnum") + " $x+jy$는 이 평면 위의 한 점이에요. $j$는 " + K("imag") + "예요.",
      "그 점을 극좌표로 적으면 $re^{j\\theta}$예요."),
  prof("극좌표계와 직교좌표계는 표현만 다를 뿐 서로 왔다 갔다 할 수 있다고 하셨어요.",
      "점 $(x, y)$를 거리 r, 각도 θ로 보면 $x=r\\cos\\theta$, $y=r\\sin\\theta$라고 설명하셨어요."),
 ],
 "pass4": [
  warn("헷갈리기 쉬운 점",
      "이 그림의 $r$은 '거리(반지름)'예요. 앞 쪽 $a=r+j\\omega_0$의 $r$(커지고 줄어드는 빠르기)과 글자만 같고 뜻이 달라요.",
      "각도는 도(°)로도, " + K("rad") + "으로도 적어요. $60°=\\pi/3$, $90°=\\pi/2$예요."),
  check("점 $3j$(가로 0, 세로 3)를 극좌표로 쓰면?", ["$3e^{j0}$", "$3e^{j\\pi/2}$", "$3e^{j\\pi}$"], 1,
      "거리는 3, 세로축 위쪽이니 각도는 $90°=\\pi/2$예요."),
  english("시험 답안에 쓸 문장",
      "복소수는 직교좌표 $x+jy$ 또는 극좌표 $re^{j\\theta}$로 나타낼 수 있으며, $x=r\\cos\\theta$, $y=r\\sin\\theta$로 서로 바꾼다.",
      "거리와 각도 ↔ 가로와 세로.",
      "'가로는 cos, 세로는 sin'."),
 ]})

# ---------------------------------------------------------------------
# p.37 (슬라이드 35) 감쇠 사인파와 포락선
# ---------------------------------------------------------------------
_env = [math.exp(-0.5 * t) for t in (0, 1, 2)]
assert abs(_env[0] - 1) < 1e-12 and abs(_env[1] - 0.607) < 1e-3 and abs(_env[2] - 0.368) < 1e-3
assert all(abs(math.exp(-0.5 * t) * math.cos(2 * PI * t) - math.exp(-0.5 * t)) < 1e-12 for t in (0, 1, 2))
_Ct, _rt = 2.0, 0.3
assert abs(_Ct * math.exp(_rt * 2) - 3.644) < 1e-3

S.append({"p": 37, "title": "감쇠 사인파와 포락선",
 "pass1": [
  say("출렁이는 신호가 점점 커지거나, 점점 작아지는 모양이에요.",
      "바깥을 감싼 점선이 출렁임의 크기를 정해요.",
      "점점 작아지며 출렁이는 신호를 " + K("damped") + "라고 해요."),
  figure("출렁이며 줄어드는 신호", FIG_ENV,
      "파란 선은 출렁이고, 노란 선(" + K("env") + ")이 크기를 가둬요."),
 ],
 "pass2": [
  formula("오일러 공식으로 풀어 쓰기 (바르게 고친 식)",
      r"Ce^{at}=|C|e^{rt}\cos(\omega_0 t+\phi)+j|C|e^{rt}\sin(\omega_0 t+\phi)",
      [(r"|C|e^{rt}", K("env") + ": 출렁임의 크기를 정하는 바깥 선"),
       (r"\cos(\omega_0 t+\phi)", "실수 부분의 출렁임"),
       (r"j\sin(\omega_0 t+\phi)", "허수 부분의 출렁임"),
       (r"r", "양수면 커지고, 음수면 줄어요")],
      "바깥 선 $|C|e^{rt}$ 안에서 cos, sin이 위아래로 오가요."),
  compare("r의 부호에 따라", ["r", "포락선 $|C|e^{rt}$", "신호 모양"],
      ["$r>0$", "점점 커져요", "출렁이며 커지는 신호"],
      ["$r=0$", "평평해요", "보통 " + K("sinus")],
      ["$r<0$", "점점 줄어요", K("damped")]),
  check("출렁이는 신호의 위아래 끝을 이은 바깥 선의 이름은?", [K("amp"), K("env"), K("phase")], 1,
      "영어 envelope는 '봉투'라는 뜻이에요. 신호를 봉투처럼 감싸는 선이에요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (120, 255, 690, 325, "오일러 관계를 쓰면 이 신호들은 감쇠 사인파(damped sinusoids)라는 말이에요."),
      (70, 355, 545, 405, "앞 쪽에서 합친 식"),
      (70, 445, 925, 505, "실수 부분은 cos, 허수 부분은 sin으로 나눈 식이에요."),
      (965, 265, 1370, 455, "위 그래프: 실수부(Re). 점선 $\\pm Ce^{\\alpha t}$ 안에서 커지며 출렁여요($r>0$)."),
      (965, 460, 1370, 640, "아래 그래프: 점선 $\\pm Ce^{-\\alpha t}$ 안에서 줄어들며 출렁여요($r<0$).")),
  steps("포락선 값 손계산",
      ["신호: $x(t)=e^{-0.5t}\\cos(2\\pi t)$. 포락선은 $e^{-0.5t}$예요.",
       "$t=0$: 포락선 $e^{0}=1$.",
       "$t=1$: 포락선 $e^{-0.5}\\approx 0.61$.",
       "$t=2$: 포락선 $e^{-1}\\approx 0.37$.",
       "$t$가 정수면 $\\cos(2\\pi t)=1$이라 신호가 포락선에 딱 닿아요."],
      "포락선 $1\\to 0.61\\to 0.37$, 신호는 그 안에서 출렁이며 줄어요.",
      given="$|C|=1$, $r=-0.5$, $\\omega_0=2\\pi$"),
  prof("r이 0보다 크면 커지는(growing) 지수, 작으면 줄어드는(decay) 지수가 된다고 하셨어요.",
      "신호를 가두는 점선을 한국말로 포락선, 영어로 envelope라고 하고, envelope는 '봉투'라는 뜻이라고 하셨어요.",
      "앞부분 $|C|e^{rt}$가 포락선이 되고, 뒷부분 사인과 코사인이 위아래로 오르내린다고 설명하셨어요."),
  prof("시간이 갈수록 줄어드는 신호를 damped signal(감쇠 신호)이라고도 부른다고 하셨어요.",
      when="2주차 목요일 수업 (둘째 시간 시작)"),
 ],
 "pass4": [
  warn("헷갈리기 쉬운 점",
      "슬라이드 식의 $\\cos((\\omega_0+\\phi)t)$는 $\\cos(\\omega_0 t+\\phi)$가 맞아요. p.35와 같은 오타예요.",
      "그래프의 $\\alpha$는 식의 $r$과 같은 역할이에요. 그림 출처가 달라서 글자가 달라요.",
      "그래프는 실수 부분(Re)만 그린 것이에요. 복소 신호 전체를 한 그림에 그릴 수는 없어요."),
  check("$x(t)=2e^{0.3t}\\cos(5t)$는 어떤 모양일까요?", ["출렁이며 커진다", "출렁이며 줄어든다", "크기가 일정하다"], 0,
      "$r=0.3>0$이라 포락선 $2e^{0.3t}$가 커져요. 예: $t=2$에서 $2e^{0.6}\\approx 3.64$."),
  english("시험 답안에 쓸 문장",
      "일반 복소 지수 신호의 실수부는 $|C|e^{rt}\\cos(\\omega_0 t+\\phi)$로, $r>0$이면 증가, $r<0$이면 감쇠하는 사인파이며 $|C|e^{rt}$가 포락선이다.",
      "포락선 = 바깥 봉투, 안에서 사인파가 출렁임.",
      "'r 부호가 커질지 줄지를 정한다'."),
 ]})

# ---------------------------------------------------------------------
# p.38 (슬라이드 36) 이산시간 실수 지수 C alpha^n
# ---------------------------------------------------------------------
assert [0.5 ** n for n in range(4)] == [1, 0.5, 0.25, 0.125]
assert [(-0.5) ** n for n in range(4)] == [1, -0.5, 0.25, -0.125]
assert [2 ** n for n in range(4)] == [1, 2, 4, 8]
assert [(-2) ** n for n in range(4)] == [1, -2, 4, -8]
assert abs(math.exp(math.log(0.5)) - 0.5) < 1e-12

S.append({"p": 38, "title": "이산시간 실수 지수 신호",
 "pass1": [
  say("이제 " + K("dt") + "로 넘어가요. 하루 한 번 찍은 점으로 된 신호예요.",
      "매일 같은 수를 곱해 가면 점들이 어떻게 될까요?",
      "1보다 큰 수를 곱하면 점점 커지고, 1보다 작은 수를 곱하면 점점 작아져요."),
  figure("매일 같은 수를 곱하기", FIG_DTEXP,
      "왼쪽은 매일 1.25를, 오른쪽은 매일 0.6을 곱한 점들이에요."),
 ],
 "pass2": [
  formula("이산시간 실수 지수 신호",
      r"x[n]=C\alpha^n=Ce^{\beta n},\qquad \alpha=e^{\beta}",
      [(r"x[n]", "n번째 칸의 값. 대괄호는 정수 칸이라는 표시"),
       (r"C", "출발 값($n=0$일 때 값)"),
       (r"\alpha^n", "$\\alpha$('알파')를 n번 곱한 것"),
       (r"\alpha=e^{\beta}", "같은 신호를 $e$의 거듭제곱으로 쓰는 방법")],
      "출발 값 C에 매 칸 $\\alpha$를 곱해 가는 " + K("rexp") + "예요."),
  compare("α에 따라 네 가지 모양", ["α", "모양", "슬라이드"],
      ["$\\alpha>1$", "점점 커져요", "(a)"],
      ["$0<\\alpha<1$", "점점 작아져요", "(b)"],
      ["$-1<\\alpha<0$", "부호가 번갈아, 작아져요", "(c)"],
      ["$\\alpha<-1$", "부호가 번갈아, 커져요", "(d)"]),
  check("$\\alpha=0.8$이면 $x[n]=\\alpha^n$은 어떻게 될까요?", ["점점 커진다", "점점 작아진다", "부호가 번갈아 바뀐다"], 1,
      "$0$과 $1$ 사이 수를 계속 곱하면 작아져요. 음수가 아니라 부호는 안 바뀌어요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (190, 200, 665, 390, "실수 지수 신호: $x[n]=C\\alpha^n$ 또는 $Ce^{\\beta n}$, 그리고 $\\alpha=e^{\\beta}$"),
      (715, 195, 1065, 315, "(a) $\\alpha>1$: 오른쪽으로 갈수록 커져요."),
      (715, 315, 1065, 425, "(b) $0<\\alpha<1$: 오른쪽으로 갈수록 작아져요."),
      (715, 425, 1065, 525, "(c) $-1<\\alpha<0$: 위아래 번갈아 찍히며 작아져요."),
      (715, 525, 1065, 625, "(d) $\\alpha<-1$: 위아래 번갈아 찍히며 커져요."),
      (740, 635, 1045, 700, "그림 설명: 네 경우의 $\\alpha$ 범위")),
  steps("쉬운 숫자로 값 적기 ($C=1$)",
      ["$\\alpha=0.5$: $n=0,1,2,3$ → $1, 0.5, 0.25, 0.125$. 점점 작아져요.",
       "$\\alpha=2$: → $1, 2, 4, 8$. 점점 커져요.",
       "$\\alpha=-0.5$: → $1, -0.5, 0.25, -0.125$. 홀수 칸은 음수예요.",
       "$\\alpha=-2$: → $1, -2, 4, -8$. 번갈아 가며 커져요."],
      "크기는 $|\\alpha|$가, 부호가 바뀌는지는 $\\alpha$가 음수인지가 정해요."),
  figure("α = -0.5일 때", FIG_DTALT,
      "음수를 곱하면 한 칸마다 부호가 바뀌어요. 크기는 절반씩 줄어요."),
  prof("이산시간에서는 $Ce^{\\beta n}$보다 $C\\alpha^n$ 꼴로 더 많이 쓴다고 하셨어요. 둘 다 맞는 표현이에요.",
      "$\\alpha$가 음수면 홀수일 때 음수, 짝수일 때 양수로 찍히며 진동한다고 설명하셨어요.",
      "연속시간처럼 그린 다음 정수 칸만 콕콕 찍으면 이산시간 신호라고 봐도 이해에 큰 무리가 없다고 하셨어요."),
 ],
 "pass4": [
  check("$x[n]=(-2)^n$은 네 그림 중 어느 것일까요?", ["(a)", "(b)", "(c)", "(d)"], 3,
      "$\\alpha=-2<-1$이라 부호가 번갈아 바뀌며 커져요: $1, -2, 4, -8$."),
  warn("헷갈리기 쉬운 점",
      "실수 $\\beta$로 만든 $e^{\\beta}$는 늘 양수예요. 그래서 음수 $\\alpha$는 보통 $C\\alpha^n$ 꼴로 적어요.",
      "$\\alpha^0=1$이라서 $n=0$ 칸의 값은 언제나 $C$예요."),
  english("시험 답안에 쓸 문장",
      "이산시간 실수 지수 신호 $x[n]=C\\alpha^n$은 $|\\alpha|>1$이면 증가, $|\\alpha|<1$이면 감소하며, $\\alpha<0$이면 부호가 번갈아 바뀐다.",
      "크기는 $|\\alpha|$, 부호 교대는 $\\alpha$의 부호.",
      "'절댓값은 크기, 음수면 번갈아'."),
 ]})

# ---------------------------------------------------------------------
# p.39 (슬라이드 37) 이산시간 사인파
# ---------------------------------------------------------------------
_v = [math.cos(2 * PI * n / 12) for n in range(4)]
assert abs(_v[0] - 1) < 1e-12 and abs(_v[1] - 0.866) < 1e-3 and abs(_v[2] - 0.5) < 1e-12 and abs(_v[3]) < 1e-12
assert abs(math.cos(2 * PI * 12 / 12) - 1) < 1e-12
for _n in range(5):
    _A, _ph, _w = 3.0, 0.4, 0.9
    _lhs = _A * math.cos(_w * _n + _ph)
    _rhs = _A / 2 * cmath.exp(1j * _ph) * cmath.exp(1j * _w * _n) + _A / 2 * cmath.exp(-1j * _ph) * cmath.exp(-1j * _w * _n)
    assert abs(_lhs - _rhs) < 1e-12

S.append({"p": 39, "title": "이산시간 사인파 신호",
 "pass1": [
  say("이산시간 " + K("sinus") + "는 코사인 곡선 위에 정수 칸마다 점을 찍은 모양이에요.",
      "하루 한 번 온도를 적으면, 매끈한 곡선 대신 점들이 남는 것과 같아요.",
      "점들만 봐도 곡선의 모양이 보이죠."),
  figure("곡선 위에 찍은 점", FIG_DTCOS,
      "코사인 곡선 위 정수 칸마다 점. 8칸마다 같은 모양이에요."),
 ],
 "pass2": [
  formula("이산시간 복소 지수와 사인파",
      r"x[n]=e^{j\omega_0 n}=\cos\omega_0 n+j\sin\omega_0 n",
      [(r"e^{j\omega_0 n}", "한 칸 갈 때마다 각도 $\\omega_0$만큼 도는 점"),
       (r"\cos\omega_0 n", "그 점을 가로축에 비춘 그림자(실수 부분)"),
       (r"\sin\omega_0 n", "세로축에 비춘 그림자(허수 부분)")],
      "연속시간과 똑같이 " + K("euler") + "이 성립해요. $t$ 대신 정수 $n$일 뿐이에요."),
  formula("사인파를 복소 지수 두 개로",
      r"A\cos(\omega_0 n+\phi)=\frac{A}{2}e^{j\phi}e^{j\omega_0 n}+\frac{A}{2}e^{-j\phi}e^{-j\omega_0 n}",
      [(r"A", K("amp") + ": 가장 높이 가는 값"),
       (r"\phi", K("phase") + ": 출발 각도"),
       (r"\frac{A}{2}e^{\pm j\cdots}", "반대로 도는 두 점을 절반씩 더하면 cos이 돼요")],
      "cos은 서로 반대로 도는 두 복소 지수의 평균이에요(p.34와 같은 공식)."),
  check("$e^{j\\omega_0 n}$의 실수 부분은?", ["$\\sin\\omega_0 n$", "$\\cos\\omega_0 n$", "$\\omega_0 n$"], 1,
      "오일러 공식에서 실수 부분은 cos, 허수 부분은 sin이에요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (120, 248, 615, 350, "Sinusoidal signals: $x[n]=e^{j\\omega_0 n}$과 $x[n]=A\\cos(\\omega_0 n+\\phi)$"),
      (200, 405, 510, 445, K("euler") + ": cos와 sin으로 나누기"),
      (115, 505, 610, 575, "cos을 두 복소 지수의 합으로 쓰기"),
      (645, 225, 1340, 365, "$\\cos(2\\pi n/12)$: 12칸마다 반복"),
      (645, 370, 1340, 510, "$\\cos(8\\pi n/31)$: 반복은 하지만 모양이 조금 불규칙해 보여요"),
      (645, 515, 1340, 655, "$\\cos(n/6)$: 매끈해 보이지만 사실 주기가 없어요(p.41)")),
  steps("$\\cos(2\\pi n/12)$ 값 손계산",
      ["$n=0$: $\\cos 0=1$.",
       "$n=1$: $\\cos(\\pi/6)\\approx 0.866$.",
       "$n=2$: $\\cos(\\pi/3)=0.5$.",
       "$n=3$: $\\cos(\\pi/2)=0$.",
       "$n=12$: $\\cos(2\\pi)=1$. 다시 처음 값이에요."],
      "12칸마다 같은 값이 돌아와요: 기본 주기 $N=12$"),
  prof("사인파를 익스포넨셜로 표현하는 것도 가능하지만 중요하지 않으니 넘어간다고 하셨어요.",
      "각주파수에 $\\pi$가 들어가느냐 아니냐에 따라 특징이 나뉘고, 뒤에서 설명한다고 하셨어요."),
 ],
 "pass4": [
  check("세 그래프 중 주기가 없는 것은?", ["$\\cos(2\\pi n/12)$", "$\\cos(8\\pi n/31)$", "$\\cos(n/6)$"], 2,
      "$\\cos(n/6)$은 각주파수에 $\\pi$가 없어서 정수 칸이 딱 한 바퀴에 맞지 않아요. 이유는 p.41에서 봐요."),
  warn("헷갈리기 쉬운 점",
      "그림이 부드러워 보인다고 주기가 있는 게 아니에요. $\\cos(n/6)$은 연속시간이라면 주기 $12\\pi$지만, 이산시간에서는 주기가 없어요.",
      "슬라이드의 세 그래프는 모두 실수 신호 $\\cos$예요."),
 ]})

# ---------------------------------------------------------------------
# p.40 (슬라이드 38) 이산시간 일반 복소 지수
# ---------------------------------------------------------------------
_re = [round((0.9 ** n) * math.cos(PI * n / 2), 6) for n in range(5)]
assert _re == [1.0, 0.0, -0.81, 0.0, 0.6561]
for _n in range(6):
    _C, _alpha = 2 * cmath.exp(0.3j), 1.1 * cmath.exp(0.7j)
    _z = _C * _alpha ** _n
    assert abs(_z.real - 2 * 1.1 ** _n * math.cos(0.7 * _n + 0.3)) < 1e-9

S.append({"p": 40, "title": "이산시간 일반 복소 지수: 출렁이며 커지거나 줄어요",
 "pass1": [
  say("이산시간에서도 출렁이며 커지거나 줄어드는 신호가 있어요.",
      "매 칸 같은 각도만큼 돌면서, 같은 비율로 크기가 변해요.",
      "크기 비율이 1보다 크면 커지고, 1보다 작으면 줄어들어요."),
  figure("출렁이며 줄어드는 점들", FIG_DTDAMP,
      "노란 선(" + K("env") + ") 안에서 점들이 출렁이며 줄어요."),
 ],
 "pass2": [
  formula("C와 α를 둘 다 극좌표로",
      r"C=|C|e^{j\theta},\qquad \alpha=|\alpha|e^{j\omega_0}",
      [(r"|C|", "출발 크기"), (r"\theta", "출발 각도(" + K("phase") + ")"),
       (r"|\alpha|", "한 칸마다 크기에 곱하는 비율"),
       (r"\omega_0", "한 칸마다 도는 각도")],
      "C도 α도 '크기와 각도'로 적어요."),
  formula("풀어 쓴 결과",
      r"C\alpha^n=|C||\alpha|^n\cos(\omega_0 n+\theta)+j|C||\alpha|^n\sin(\omega_0 n+\theta)",
      [(r"|C||\alpha|^n", K("env") + ": 크기가 매 칸 $|\\alpha|$배"),
       (r"\cos(\omega_0 n+\theta)", "실수 부분의 출렁임"),
       (r"\sin(\omega_0 n+\theta)", "허수 부분의 출렁임")],
      "연속시간의 $|C|e^{rt}$ 자리에 $|C||\\alpha|^n$이 들어간 모양이에요."),
  compare("|α|에 따라", ["$|\\alpha|$", "모양"],
      ["$|\\alpha|>1$", "출렁이며 커져요 (a)"],
      ["$|\\alpha|=1$", K("sinus") + " (크기 일정)"],
      ["$|\\alpha|<1$", "출렁이며 줄어요 (b)"]),
  check("$|\\alpha|=1$이면 $C\\alpha^n$은 어떤 신호일까요?", ["커지는 신호", "크기가 일정한 사인파", "줄어드는 신호"], 1,
      "$1^n=1$이라 포락선이 평평해요. 그냥 출렁이기만 해요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (160, 222, 625, 265, "General Complex Exponential Signals (이산시간)"),
      (280, 325, 425, 375, "$C=|C|e^{j\\theta}$: C를 극좌표로"),
      (280, 415, 425, 470, "$\\alpha=|\\alpha|e^{j\\omega_0}$: 빨간 원은 $|\\alpha|$, 이것이 그래프 모양을 정해요."),
      (140, 530, 630, 585, "풀어 쓴 결과: 크기 $|C||\\alpha|^n$, 출렁임 cos와 sin"),
      (635, 200, 1070, 425, "(a) $|\\alpha|>1$: 커지는 이산시간 사인파"),
      (635, 430, 1070, 700, "(b) $|\\alpha|<1$: 줄어드는 이산시간 사인파")),
  steps("쉬운 숫자로 실수 부분 적기",
      ["$C=1$, $\\alpha=0.9e^{j\\pi/2}$: 크기 비율 $0.9$, 한 칸에 $90°$씩 돌아요.",
       "실수 부분 $=0.9^n\\cos(\\pi n/2)$예요.",
       "$n=0$: $1\\times 1=1$. $n=1$: $0.9\\times 0=0$.",
       "$n=2$: $0.81\\times(-1)=-0.81$. $n=3$: $0$.",
       "$n=4$: $0.6561\\times 1=0.6561$."],
      "$1, 0, -0.81, 0, 0.6561$: 출렁이며 줄어요.",
      given="$|\\alpha|=0.9<1$"),
  prof("이산시간에서는 보통 C와 α를 둘 다 극좌표(폴라 폼)로 쓰는 게 일반적인 약속이라고 하셨어요.",
      "직교좌표로 써도 틀린 건 아니고, 신호를 이해하고 그리기 쉬워서 이렇게 쓴다고 하셨어요.",
      "|α|가 정확히 1이면 사인파가 되고, 줄어드는 신호는 damped signal이라고도 부른다고 하셨어요."),
 ],
 "pass4": [
  check("$C\\alpha^n$에서 $|\\alpha|=1.2$, $\\omega_0=\\pi/3$이면?", ["출렁이며 커진다", "출렁이며 줄어든다", "출렁이지 않고 커지기만 한다"], 0,
      "$|\\alpha|>1$이라 포락선이 커지고, $\\omega_0\\neq 0$이라 출렁여요."),
  warn("헷갈리기 쉬운 점",
      "여기서 $\\theta$는 C의 각도(" + K("phase") + "), $\\omega_0$는 α의 각도예요. 연속시간 식의 $\\phi$, $\\omega_0$와 같은 역할이에요.",
      "연속시간은 $r$의 부호(양수/음수)로, 이산시간은 $|\\alpha|$가 1보다 큰지 작은지로 커짐/줄어듦을 판단해요."),
  english("시험 답안에 쓸 문장",
      "$C=|C|e^{j\\theta}$, $\\alpha=|\\alpha|e^{j\\omega_0}$이면 $C\\alpha^n$의 실수부는 $|C||\\alpha|^n\\cos(\\omega_0 n+\\theta)$로, $|\\alpha|>1$이면 증가, $|\\alpha|<1$이면 감쇠하는 사인파이다.",
      "연속은 r의 부호, 이산은 $|\\alpha|$와 $1$ 비교.",
      "'이산은 1과 비교'."),
 ]})

# ---------------------------------------------------------------------
# p.41 (슬라이드 39) 이산시간 복소 지수의 주기 성질
# ---------------------------------------------------------------------
assert Fraction(1, 8) == Fraction(1, 8) and Fraction(3, 8).denominator == 8
assert abs(cmath.exp(1j * (2 * PI / 8) * 8) - 1) < 1e-12
assert all(abs(cmath.exp(1j * (2 * PI / 8) * n) - 1) > 0.1 for n in range(1, 8))
assert abs(cmath.exp(1j * (3 * PI / 4) * 8) - 1) < 1e-12
assert all(abs(cmath.exp(1j * (3 * PI / 4) * n) - 1) > 0.1 for n in range(1, 8))
assert min(abs(cmath.exp(1j * n) - 1) for n in range(1, 2000)) > 1e-6   # cos(n) 은 정확히 돌아오지 않음 (n=710 이 가장 가깝지만 같지 않음)

S.append({"p": 41, "title": "이산시간 복소 지수의 주기 성질",
 "pass1": [
  say("연속시간에서 도는 점은 언제나 주기가 있었어요.",
      "이산시간은 하루 한 번만 사진을 찍는 것과 같아요.",
      "찍힌 점이 정확히 처음 자리로 돌아와야만 주기가 생겨요.",
      "그래서 이산시간에서는 주기가 없는 경우도 있어요."),
  figure("8칸마다 제자리", FIG_CIRC8,
      "한 칸에 1/8바퀴씩 돌면, 8칸 뒤에 정확히 처음 자리예요."),
 ],
 "pass2": [
  formula("이산시간 주기 조건",
      r"e^{j\omega_0(n+N)}=e^{j\omega_0 n}\;\Rightarrow\; e^{j\omega_0 N}=1\;\Rightarrow\; \omega_0 N=2\pi m",
      [(r"N", "주기. 반드시 양의 정수(칸 수)"),
       (r"e^{j\omega_0 N}=1", "N칸 가서 1의 자리로 돌아와야 해요"),
       (r"m", "그동안 돈 바퀴 수(정수)")],
      "N칸 동안 돈 각도가 한 바퀴의 정수배여야 주기가 있어요."),
  formula("판정 규칙",
      r"\frac{\omega_0}{2\pi}=\frac{m}{N}\quad(\text{유리수})",
      [(r"\frac{\omega_0}{2\pi}", "한 칸에 몇 바퀴 도는지"),
       (r"\frac{m}{N}", "정수 나누기 정수 = 분수(유리수)")],
      "$\\omega_0/2\\pi$가 분수로 딱 떨어지면 주기가 있고, 아니면 " + K("aper") + "예요."),
  compare("주기가 있을까?", ["신호", "$\\omega_0/2\\pi$", "주기"],
      ["$e^{j(2\\pi/8)n}$", "$1/8$", "있음, $N=8$"],
      ["$e^{j(3\\pi/4)n}$", "$3/8$", "있음, $N=8$"],
      ["$\\cos(n)$", "$1/2\\pi$ (분수 아님)", "없음"]),
  check("이산시간 $e^{j\\omega_0 n}$이 주기를 가질 조건은?",
      ["$\\omega_0$가 정수", "$\\omega_0/2\\pi$가 유리수(분수)", "항상 주기적"], 1,
      "정수 칸 N 동안 한 바퀴의 정수배를 돌아야 하니, $\\omega_0/2\\pi=m/N$ 꼴이어야 해요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (110, 198, 1120, 242, "이산시간 복소 지수의 주기 성질 두 가지"),
      (110, 265, 460, 305, "(1) 진동의 빠르기. 아래 빈칸은 교수님이 수업에서 판서로 채운 곳이에요."),
      (100, 560, 720, 700, "결론 1: $\\omega_0$는 길이 $2\\pi$인 구간 안에서만 고르면 된다(다음 쪽)."),
      (760, 265, 1285, 330, "(2) 이산시간 복소 지수의 주기성"),
      (800, 395, 1345, 510, "주기 조건: N은 $2\\pi/\\omega_0$의 정수배여야 해요."),
      (805, 570, 1345, 695, "결론 2: $\\omega_0/2\\pi$가 유리수면 주기적, 아니면 주기 없음.")),
  steps("주기 판정 세 가지",
      ["$e^{j(2\\pi/8)n}$: $\\omega_0/2\\pi=1/8$. 분수라서 주기 있음, $N=8$.",
       "$e^{j(3\\pi/4)n}$: $(3\\pi/4)/2\\pi=3/8$. 주기 있음, $N=8$ (그동안 3바퀴).",
       "$\\cos(n)$: $\\omega_0=1$, $1/2\\pi$는 $\\pi$가 남아서 분수가 아니에요.",
       "그래서 $\\cos(n)$은 몇 칸을 가도 정확히 처음 값으로 돌아오지 않아요."],
      "앞의 둘은 $N=8$, $\\cos(n)$은 주기 없음"),
  prof("(1) 아래를 일부러 비워 두었고, 정리된 교수용 버전이 있으면 나중에 올려 주겠다고 하셨어요.",
      "헬리콥터 영상 예: 카메라는 1초에 60장씩 찍는 이산 신호라서, 프로펠러가 1초에 60바퀴 돌면 멈춘 것처럼 보인다고 하셨어요.",
      "120바퀴, 180바퀴로 더 빨라져도 찍힌 영상은 같다고, 이것이 $\\omega_0$에 $2\\pi$를 더해도 같은 이유라고 하셨어요."),
  prof("연속시간은 $t$가 실수라 어떤 값에도 도달하지만, 이산시간은 $n$이 정수라 $12\\pi$ 같은 자리를 찍을 수 없다고 하셨어요.",
      "그래서 cos 안에 $\\pi$가 들어 있지 않으면 이산시간에서는 주기가 없다고 정리하셨어요."),
 ],
 "pass4": [
  exam("그림 예시: 슬라이드 37번 (p.39, p.41)",
      "Is $x[n]=\\cos(n/6)$ periodic? If so, find its fundamental period.",
      "$\\cos(n/6)$이 주기 신호인지 판정하고, 주기가 있으면 구하세요.",
      ["각주파수를 읽어요: $\\omega_0=1/6$.",
       "$\\omega_0/2\\pi=1/(12\\pi)$를 계산해요.",
       "$\\pi$가 남아서 정수/정수 꼴(유리수)이 아니에요.",
       "그래서 어떤 양의 정수 N으로도 $\\omega_0 N=2\\pi m$을 만들 수 없어요."],
      "주기 없음(" + K("aper") + "). 연속시간 $\\cos(t/6)$은 주기 $12\\pi$지만 이산시간은 아니에요."),
  warn("슬라이드 글자 오타",
      "'we eed only'는 'we need only', 'frequency integral'은 'frequency interval'(구간)이 맞아요.",
      "(1) 아래 빈칸은 오류가 아니라 교수님이 수업에서 채운 곳이에요. 내용은 다음 쪽 p.42에 그림으로 있어요."),
  english("시험 답안에 쓸 문장",
      "이산시간 복소 지수 $e^{j\\omega_0 n}$은 $\\omega_0/2\\pi$가 유리수 $m/N$일 때만 주기적이고, 그렇지 않으면 주기적이지 않다.",
      "n이 정수라서, 한 바퀴의 정수배에 정확히 떨어져야 해요.",
      "'오메가 나누기 2파이가 분수면 주기'."),
 ]})

# ---------------------------------------------------------------------
# p.42 (슬라이드 40) omega0 에 2 pi 를 더해도 같다, pi 에서 가장 빠르다
# ---------------------------------------------------------------------
for _n in range(-5, 6):
    assert abs(cmath.exp(1j * (0.7 + 2 * PI) * _n) - cmath.exp(1j * 0.7 * _n)) < 1e-9
    assert abs(cmath.exp(1j * PI * _n) - (-1) ** _n) < 1e-9
assert [round(math.cos(3 * PI / 2 * n), 9) + 0.0 for n in range(4)] == [1.0, 0.0, -1.0, 0.0]
assert [round(math.cos(PI / 2 * n), 9) + 0.0 for n in range(4)] == [1.0, 0.0, -1.0, 0.0]
assert all(abs(math.cos(15 * PI / 8 * n) - math.cos(PI / 8 * n)) < 1e-9 for n in range(10))

S.append({"p": 42, "title": "각주파수를 올려도 π에서 가장 빨라요",
 "pass1": [
  say("연속시간에서는 빨리 돌수록 신호가 계속 빨라졌어요.",
      K("dt", "은") + " 조금 달라요. 점이 가장 빨리 바뀌는 때가 따로 있어요.",
      "한 칸에 반 바퀴씩 돌 때가 가장 빨라요. 그보다 더 돌면 다시 느려 보여요."),
  figure("느림에서 가장 빠름까지", FIG_FAST,
      "위에서 아래로 갈수록 점이 빨리 바뀌어요. 맨 아래는 +1, -1이 번갈아요."),
 ],
 "pass2": [
  formula("2π를 더해도 같은 신호",
      r"e^{j(\omega_0+2\pi)n}=e^{j2\pi n}e^{j\omega_0 n}=e^{j\omega_0 n}",
      [(r"e^{j2\pi n}", "n이 정수라서 늘 한 바퀴의 정수배, 그래서 늘 1"),
       (r"e^{j\omega_0 n}", "결국 원래 신호와 같아요")],
      "각주파수에 $2\\pi$를 더해도 이산시간 신호는 그대로예요."),
  formula("가장 빠른 신호",
      r"e^{j\pi n}=\left(e^{j\pi}\right)^n=(-1)^n",
      [(r"e^{j\pi}=-1", K("ucirc") + "에서 반 바퀴 돈 자리는 -1"),
       (r"(-1)^n", "$1, -1, 1, -1, \\dots$ 한 칸마다 부호가 바뀌어요")],
      "한 칸마다 반대편으로 뛰니, 이보다 빨리 바뀔 수는 없어요."),
  compare("ω0에 따른 빠르기", ["$\\omega_0$", "보이는 빠르기"],
      ["$0$", "변화 없음(상수)"],
      ["$\\pi/8$, $\\pi/2$", "점점 빨라져요"],
      ["$\\pi$", "가장 빨라요"],
      ["$3\\pi/2$, $15\\pi/8$", "다시 느려져요"],
      ["$2\\pi$", "$0$과 같아요"]),
  check("이산시간 " + K("cexp") + " $e^{j\\omega_0 n}$이 가장 빠르게 바뀌는 " + K("angf") + " $\\omega_0$는? ($0$부터 $2\\pi$ 사이)",
      ["$\\pi/2$", "$\\pi$", "$2\\pi$"], 1,
      "$\\omega_0=\\pi$면 $(-1)^n$, 한 칸마다 부호가 바뀌어 가장 빨라요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (200, 212, 720, 268, "$\\omega_0$에 $2\\pi$를 더해도 같은 신호"),
      (840, 212, 1200, 268, "$e^{j\\pi n}=(-1)^n$: 가장 빠른 신호"),
      (170, 270, 505, 465, "$\\omega_0=0$: 늘 1인 상수"),
      (530, 270, 870, 465, "$\\omega_0=\\pi/8$: 천천히 출렁"),
      (880, 270, 1225, 465, "$\\omega_0=\\pi/2$: 1, 0, -1, 0으로 빨라짐"),
      (170, 470, 1225, 665, "아래 줄: $\\pi$에서 가장 빠르고, $3\\pi/2$와 $15\\pi/8$은 다시 느려져요.")),
  steps("같아 보이는 이유 손계산 (실수 부분)",
      ["$\\omega_0=\\pi/2$: $\\cos(\\pi n/2)$ → $n=0,1,2,3$에서 $1, 0, -1, 0$.",
       "$\\omega_0=3\\pi/2$: $\\cos(3\\pi n/2)$ → $1, 0, -1, 0$. 똑같아요.",
       "이유: $3\\pi/2=-\\pi/2+2\\pi$. $2\\pi$를 빼면 $-\\pi/2$, 반대로 도는 $\\pi/2$예요.",
       "같은 방법으로 $15\\pi/8=-\\pi/8+2\\pi$라서 $\\pi/8$처럼 느려 보여요."],
      "$\\pi$를 넘으면 반대 방향으로 천천히 도는 것과 같아 보여요."),
  steps("$\\omega_0=\\pi$일 때 값",
      ["$e^{j\\pi}=-1$이에요(반 바퀴).",
       "$n=0$: $1$. $n=1$: $-1$. $n=2$: $1$. $n=3$: $-1$.",
       "한 칸마다 반대편으로 뛰어요."],
      "$(-1)^n$: 이산시간에서 가장 빠른 신호"),
  prof("$\\omega_0=\\pi$일 때 1, -1이 번갈아 찍히는 게 가장 짧은 주기, 가장 높은 주파수라고 하셨어요.",
      "0 근처가 가장 느리게 변하는 신호, $\\pi$ 근처가 가장 빠르게 변하는 신호라고 하셨어요.",
      "그래서 보통 $-\\pi$에서 $\\pi$ 사이만 생각하면 된다고 정리하셨어요."),
 ],
 "pass4": [
  check("$e^{j(9\\pi/4)n}$과 같은 신호는?", ["$e^{j(\\pi/4)n}$", "$e^{j(9\\pi/4)n}$과 같은 것은 없다", "$e^{j\\pi n}$"], 0,
      "$9\\pi/4=\\pi/4+2\\pi$예요. $2\\pi$를 빼도 같은 신호라서 $e^{j(\\pi/4)n}$과 같아요."),
  warn("헷갈리기 쉬운 점",
      "연속시간 $e^{j\\omega_0 t}$는 $\\omega_0$가 클수록 계속 빨라지고, 모두 다른 신호예요.",
      "이산시간은 $2\\pi$마다 같은 신호가 반복되고, $\\pi$에서 가장 빨라요.",
      "슬라이드 여섯 그림은 실수 부분 $\\cos(\\omega_0 n)$을 그린 것이에요."),
  english("시험 답안에 쓸 문장",
      "이산시간 복소 지수는 $e^{j(\\omega_0+2\\pi)n}=e^{j\\omega_0 n}$이므로 각주파수가 $2\\pi$ 주기로 반복되며, $\\omega_0=\\pi$에서 가장 빠르게 진동한다.",
      "n이 정수라 $e^{j2\\pi n}=1$. 가장 빠른 것은 $(-1)^n$.",
      "'2파이마다 같고, 파이에서 최고'."),
 ]})

# ---------------------------------------------------------------------
# p.43 (슬라이드 41) 연속시간과 이산시간 복소 지수 비교 (TABLE 1.1)
# ---------------------------------------------------------------------
_w = 3 * PI / 4
assert abs(2 * PI / _w - 8 / 3) < 1e-12
_f = Fraction(3, 8)
assert _f.numerator == 3 and _f.denominator == 8
assert abs(_w / 3 - PI / 4) < 1e-12 and abs(3 * (2 * PI / _w) - 8) < 1e-12
assert Fraction(4, 31).denominator == 31 and abs(8 * PI / 31 / (2 * PI) - 4 / 31) < 1e-12
assert Fraction(6, 16) == Fraction(3, 8)

S.append({"p": 43, "title": "연속시간과 이산시간 복소 지수 비교",
 "pass1": [
  compare("선과 점, 무엇이 다를까", ["", "연속시간 (끊김 없는 선)", "이산시간 (하루 한 번 찍은 점)"],
      ["빠르기가 다르면", "늘 다른 신호", "한 바퀴만큼 차이 나면 같은 신호"],
      ["주기", "언제나 있어요", "조건이 맞을 때만 있어요"]),
  say("같은 도는 점인데, 선으로 보느냐 점으로 보느냐에 따라 성질이 달라져요.",
      "이 쪽은 지금까지 본 차이를 표 하나로 정리한 쪽이에요."),
 ],
 "pass2": [
  formula("표 왼쪽의 유도",
      r"e^{j\omega_0(n+N)}=e^{j\omega_0 n}\Rightarrow e^{j\omega_0 N}=1\Rightarrow \omega_0 N=2\pi m\Rightarrow \frac{\omega_0}{2\pi}=\frac{m}{N}",
      [(r"N", "주기(양의 정수)"), (r"m", "N칸 동안 돈 바퀴 수"),
       (r"\frac{m}{N}", "기약분수로 적은 한 칸당 바퀴 수")],
      "p.41의 주기 조건을 한 줄로 이은 것이에요."),
  compare("TABLE 1.1 풀어 읽기", ["", "$e^{j\\omega_0 t}$ (연속)", "$e^{j\\omega_0 n}$ (이산)"],
      ["서로 다른 신호?", "$\\omega_0$가 다르면 다른 신호", "$2\\pi$ 차이 나는 $\\omega_0$는 같은 신호"],
      ["주기성", "어떤 $\\omega_0$든 주기적", "$\\omega_0=2\\pi m/N$일 때만 주기적"],
      ["기본 주파수", "$\\omega_0$", "$\\omega_0/m$"],
      ["" + K("fper"), "$\\omega_0\\neq 0$: $2\\pi/\\omega_0$", "$\\omega_0\\neq 0$: $m(2\\pi/\\omega_0)$"]),
  check("연속시간 $e^{j\\omega_0 t}$에 대해 맞는 말은?",
      ["$\\omega_0$에 $2\\pi$를 더하면 같은 신호", "어떤 $\\omega_0$든 주기적", "$\\omega_0/2\\pi$가 유리수일 때만 주기적"], 1,
      "연속시간은 $t$가 실수라 언제나 한 바퀴 지점에 도달해요. 나머지 둘은 이산시간 이야기예요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (110, 255, 365, 615, "왼쪽: 주기 조건을 풀어 $\\omega_0/2\\pi=m/N$에 도착"),
      (410, 215, 1350, 258, "TABLE 1.1: $e^{j\\omega_0 t}$와 $e^{j\\omega_0 n}$ 비교"),
      (405, 305, 1350, 378, "첫 줄: 연속은 늘 다른 신호, 이산은 $2\\pi$ 차이면 같은 신호"),
      (405, 380, 1350, 425, "둘째 줄: 연속은 늘 주기적, 이산은 $\\omega_0=2\\pi m/N$일 때만"),
      (405, 425, 1350, 472, "셋째 줄: 기본 주파수. 이산은 $\\omega_0/m$"),
      (405, 475, 1350, 640, "넷째 줄: 기본 주기. 별표는 m과 N이 공약수가 없다는 조건")),
  steps("$\\omega_0=3\\pi/4$로 표 채우기",
      ["연속 $e^{j(3\\pi/4)t}$: 기본 주기 $2\\pi\\div(3\\pi/4)=8/3\\approx 2.67$초.",
       "이산 $e^{j(3\\pi/4)n}$: $\\omega_0/2\\pi=3/8$, 그래서 $m=3$, $N=8$.",
       "이산 기본 주파수: $\\omega_0/m=(3\\pi/4)/3=\\pi/4$.",
       "이산 기본 주기: $m(2\\pi/\\omega_0)=3\\times 8/3=8$칸.",
       "뜻: 8칸 가는 동안 3바퀴를 돌고 제자리예요."],
      "연속은 $8/3$초, 이산은 $8$칸"),
  prof("$\\cos(8\\pi n/31)$의 예: 연속이라면 $31/4$마다 반복이지만, $31/4$는 정수가 아니라 찍을 수 없고, 4번을 가야 31이 되어 주기가 31이라고 하셨어요.",
      "m이 4라는 것은 연속시간으로 치면 4번 반복할 만큼 지나야 한 주기가 된다는 뜻이라고 설명하셨어요.",
      "표의 기본 주파수 줄(펀더멘털 프리퀀시)은 그냥 넘어가도 된다고 하셨어요."),
 ],
 "pass4": [
  exam("그림 예시: 슬라이드 37번 (p.39, p.43)",
      "Find the fundamental period of $x[n]=\\cos(8\\pi n/31)$.",
      "$\\cos(8\\pi n/31)$의 기본 주기를 구하세요.",
      ["$\\omega_0=8\\pi/31$이에요.",
       "$\\omega_0/2\\pi=(8\\pi/31)\\div 2\\pi=4/31$.",
       "4와 31은 공약수가 없으니 $m=4$, $N=31$.",
       "확인: $m(2\\pi/\\omega_0)=4\\times 31/4=31$."],
      "$N=31$ (그동안 4바퀴)"),
  warn("헷갈리기 쉬운 점",
      "표의 별표: $m/N$은 기약분수여야 해요. $6/16$이면 먼저 $3/8$로 줄여서 $N=8$이에요.",
      "이산시간 기본 주기는 $2\\pi/\\omega_0$가 아니에요. 그 값이 정수가 아닐 수 있어서 $m$배를 해요."),
  check("$e^{j(6\\pi/8)n}$의 기본 주기는?", ["$16$", "$8$", "$8/3$"], 1,
      "$\\omega_0/2\\pi=6/16=3/8$로 줄이면 $N=8$이에요."),
 ]})

# ---------------------------------------------------------------------
# p.44 (슬라이드 42) 이산시간 조화 관계 복소 지수: N 개뿐
# ---------------------------------------------------------------------
_N = 4
_phi = lambda k, n: cmath.exp(1j * k * 2 * PI / _N * n)
assert abs(_phi(1, 1) - 1j) < 1e-12 and abs(_phi(5, 1) - 1j) < 1e-12 and abs(_phi(2, 1) + 1) < 1e-12
assert all(abs(_phi(k + _N, n) - _phi(k, n)) < 1e-9 for k in range(-3, 5) for n in range(-4, 9))
assert all(abs(_phi(k, n + _N) - _phi(k, n)) < 1e-9 for k in range(4) for n in range(6))
_distinct = {tuple(round(_phi(k, n).real, 6) + 1j * round(_phi(k, n).imag, 6) for n in range(_N)) for k in range(-8, 9)}
assert len(_distinct) == _N

S.append({"p": 44, "title": "이산시간 조화 관계 복소 지수: 딱 N개",
 "pass1": [
  say("연속시간의 " + K("harm") + "는 끝없이 많았어요.",
      "이산시간에서는 딱 N개뿐이에요.",
      "N번째부터는 앞에 나온 것과 똑같아지기 때문이에요."),
  figure("N = 4일 때", FIG_CIRC4,
      "한 칸 뒤의 자리: k=0, 1, 2, 3은 모두 다르고, k=4는 k=0과 같아요."),
 ],
 "pass2": [
  formula("이산시간 조화 관계 복소 지수",
      r"\phi_k[n]=e^{jk\frac{2\pi}{N}n},\quad \omega_0=\frac{2\pi}{N}",
      [(r"\frac{2\pi}{N}", "기본 각주파수: N칸에 한 바퀴"),
       (r"k", "몇 배 빠르기인지(정수)"),
       (r"\phi_k[n+N]=\phi_k[n]", "모두 N칸마다 반복(주기 N)")],
      "N칸에 한 바퀴 도는 기본 점의 정수배 빠르기 모음이에요."),
  formula("k에 N을 더하면 같은 신호",
      r"\phi_{k+N}[n]=e^{jk\frac{2\pi}{N}n}e^{j2\pi n}=\phi_k[n]",
      [(r"e^{j2\pi n}", "n이 정수라 늘 1"),
       (r"\phi_{k+N}=\phi_k", "번호가 N만큼 차이 나면 같은 신호")],
      "그래서 서로 다른 것은 $k=0, 1, \\dots, N-1$의 N개뿐이에요."),
  compare("연속시간과 이산시간의 조화 관계 모음", ["", "연속시간", "이산시간"],
      ["식", "$e^{jk\\omega_0 t}$", "$e^{jk(2\\pi/N)n}$"],
      ["서로 다른 신호 수", "무한히 많음", "딱 N개"]),
  check("$N=8$일 때 서로 다른 이산시간 조화 관계 복소 지수는 몇 개일까요?", ["4개", "8개", "무한히 많다"], 1,
      "$k$와 $k+8$이 같은 신호라서, $k=0$부터 $7$까지 8개뿐이에요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (190, 240, 605, 335, "정의: $\\phi_k[n]=e^{jk(2\\pi/N)n}$, $k=0,\\pm1,\\pm2,\\dots$"),
      (190, 340, 605, 420, "기본 각주파수 $\\omega_0=2\\pi/N$"),
      (190, 425, 605, 505, "모든 $\\phi_k[n]$은 주기 N: $\\phi_k[n+N]=\\phi_k[n]$"),
      (190, 520, 605, 715, "이산시간 주파수의 주기성: $2\\pi$ 차이 나는 주파수는 같은 신호"),
      (625, 240, 1000, 545, "Harmonics repeat every N: $\\phi_{k+N}[n]=\\phi_k[n]$"),
      (612, 565, 1000, 712, "Key Result: 서로 다른 것은 N개, $k=0,1,\\dots,N-1$로 고르면 돼요.")),
  steps("N = 4로 확인하기 ($n=1$일 때 값)",
      ["$\\phi_k[1]=e^{jk\\pi/2}$: 한 칸에 $k\\times 90°$ 돈 자리예요.",
       "$\\phi_1[1]=e^{j\\pi/2}=j$, $\\phi_2[1]=e^{j\\pi}=-1$.",
       "$\\phi_5[1]=e^{j5\\pi/2}=e^{j\\pi/2}e^{j2\\pi}=j$. $\\phi_1$과 같아요.",
       "$\\phi_4[1]=e^{j2\\pi}=1=\\phi_0[1]$."],
      "서로 다른 것은 $\\phi_0, \\phi_1, \\phi_2, \\phi_3$ 네 개뿐이에요."),
  prof("연속시간에서는 k마다 모두 다른 유니크한 신호라서 모음의 원소가 무한히 많다고 하셨어요.",
      "이산시간은 N을 더하면 원래로 돌아와서 $\\phi_0$부터 $\\phi_{N-1}$까지 N개만 모음에 들어간다고 하셨어요.",
      "조금 어려운 내용이니, 집에서 차근차근 복습하고 교재를 읽으면 이해될 거라고 격려하셨어요."),
 ],
 "pass4": [
  warn("헷갈리기 쉬운 점",
      "$\\phi_k[n+N]=\\phi_k[n]$은 시간 n 쪽 반복, $\\phi_{k+N}[n]=\\phi_k[n]$은 번호 k 쪽 반복이에요. 둘 다 간격이 N이에요.",
      "연속시간 조화 관계 모음(p.33)은 k가 달라지면 늘 다른 신호예요."),
  check("$N=6$일 때 $\\phi_7[n]$과 같은 신호는?", ["$\\phi_1[n]$", "$\\phi_6[n]$", "$\\phi_7[n]$과 같은 것은 없다"], 0,
      "$7=1+6$이라 $\\phi_7=\\phi_1$이에요."),
  english("시험 답안에 쓸 문장",
      "이산시간 조화 관계 복소 지수 $\\phi_k[n]=e^{jk(2\\pi/N)n}$은 $\\phi_{k+N}[n]=\\phi_k[n]$이므로 서로 다른 신호는 N개뿐이다.",
      "번호가 N 차이 나면 $e^{j2\\pi n}=1$이 곱해질 뿐이라 같은 신호.",
      "'이산 하모닉은 N개'."),
 ]})


# ---------------------------------------------------------------------
# p.45 (슬라이드 43) 이산시간 단위 임펄스
# ---------------------------------------------------------------------
delta = lambda n: 1 if n == 0 else 0
u = lambda n: 1 if n >= 0 else 0
assert [delta(n) for n in range(-2, 3)] == [0, 0, 1, 0, 0]
assert [3 * delta(n - 2) for n in range(0, 5)] == [0, 0, 3, 0, 0]

S.append({"p": 45, "title": "이산시간 단위 임펄스 δ[n]",
 "pass1": [
  analogy("손뼉 한 번",
      "조용한 방에서 딱 한 번 손뼉을 쳐요. 그 순간만 소리가 나고, 앞뒤로는 조용해요.",
      ("손뼉을 친 그 순간", "$n=0$ 칸: 값 1"),
      ("앞뒤의 조용한 시간", "나머지 칸: 값 0"),
      ("손뼉 한 번", K("imp") + " $\\delta[n]$")),
  figure("손뼉 한 번 신호", FIG_DELTA,
      "가운데 한 칸만 1이고, 나머지는 모두 0이에요."),
 ],
 "pass2": [
  formula("단위 임펄스의 정의",
      r"\delta[n]=\begin{cases}0, & n\neq 0\\ 1, & n=0\end{cases}",
      [(r"\delta[n]", "'델타 n'이라고 읽어요. " + K("imp")),
       (r"n\neq 0", "0이 아닌 모든 칸에서는 0"),
       (r"n=0", "딱 0번 칸에서만 1")],
      "0번 칸에서만 1인, 가장 짧은 톡 신호예요."),
  points("왜 중요할까",
      "슬라이드: 다른 신호를 분석하는 기본 단위(basis)로 쓰여요.",
      "어떤 " + K("dt") + "도 크기를 바꾸고 옮긴 임펄스를 모아서 만들 수 있어요(3주차에 자세히).",
      "그래서 " + K("sys") + "에 손뼉 한 번을 넣어 보는 실험이 아주 중요해져요."),
  check(K("imp") + " $\\delta[n]$에서 $\\delta[3]$의 값은?", ["$0$", "$1$", "$3$"], 0,
      "$\\delta[n]$은 $n=0$에서만 1이에요. 3번 칸은 0이에요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (110, 162, 935, 208, "1.4 이산시간 단위 임펄스와 단위 계단"),
      (200, 228, 715, 268, "이산 단위 임펄스 신호(unit impulse signal)의 정의"),
      (205, 288, 535, 392, "$n\\neq 0$이면 0, $n=0$이면 1"),
      (200, 408, 720, 452, "다른 신호를 분석하는 기본 단위(basis)로 쓸모 있어요."),
      (210, 520, 810, 652, "그림: 0번 칸에만 높이 1인 막대, 나머지는 점(0)")),
  steps("임펄스 값 표로 적기",
      ["$\\delta[n]$: $n=-2,-1,0,1,2$ → $0, 0, 1, 0, 0$.",
       "$3\\delta[n-2]$: 괄호 안이 0이 되는 곳은 $n=2$예요.",
       "그래서 $n=2$에서만 $3\\times 1=3$, 나머지는 0이에요.",
       "$n=0,1,2,3,4$ → $0, 0, 3, 0, 0$."],
      "$3\\delta[n-2]$는 2번 칸에만 높이 3"),
  figure("3δ[n-2]", FIG_DSHIFT,
      "2칸 오른쪽으로 옮기고(" + K("shift") + "), 높이를 3배로 한 임펄스예요."),
  prof("단위 임펄스와 단위 계단은 연속시간이 조금 어려워서, 교재 순서대로 이산시간을 먼저 배운다고 하셨어요.",
      "그냥 0이다가 0에서만 1이 찍히고 다시 0, '별 게 없죠'라고 하셨어요.",
      "기호 $\\delta$는 '델타'라고 읽는다고 하셨어요."),
  bg("기초 다지기 b-9 단위 계단과 단위 임펄스",
      "$\\delta[n-2]$는 $\\delta[n]$을 오른쪽으로 2칸 옮긴 것이에요.",
      "괄호 안이 0이 되는 칸을 찾으면 막대 위치를 바로 알 수 있어요."),
 ],
 "pass4": [
  check("$\\delta[n+1]$의 막대는 어디에 있을까요?", ["$n=1$", "$n=-1$", "$n=0$"], 1,
      "괄호 안 $n+1=0$이 되는 곳은 $n=-1$이에요. $+$면 왼쪽으로 옮겨져요."),
  warn("헷갈리기 쉬운 점",
      "이산시간 $\\delta[n]$의 높이는 정확히 1이에요. 연속시간 $\\delta(t)$와는 달라요(p.50).",
      "$\\delta[n-n_0]$은 오른쪽으로 $n_0$칸 옮긴 것이에요. 부호를 조심해요."),
  english("시험 답안에 쓸 문장",
      "이산시간 단위 임펄스 $\\delta[n]$은 $n=0$에서 1, 그 밖의 모든 $n$에서 0인 신호로, 다른 신호를 분석하는 기본 단위로 쓰인다.",
      "0번 칸에서만 1.",
      "'0에서만 1'."),
 ]})

# ---------------------------------------------------------------------
# p.46 (슬라이드 44) 이산시간 단위 계단, 1차 차분
# ---------------------------------------------------------------------
_ns = [-1, 0, 1, 2]
assert [u(n) for n in _ns] == [0, 1, 1, 1] and [u(n - 1) for n in _ns] == [0, 0, 1, 1]
assert [u(n) - u(n - 1) for n in _ns] == [delta(n) for n in _ns] == [0, 1, 0, 0]
assert all(u(n) - u(n - 1) == delta(n) for n in range(-20, 21))
assert all(u(n - 3) - u(n - 4) == delta(n - 3) for n in range(-10, 11))

S.append({"p": 46, "title": "이산시간 단위 계단 u[n]과 1차 차분",
 "pass1": [
  analogy("스위치를 켜는 순간",
      "0번 칸에서 불 스위치를 켜요. 켜기 전에는 꺼져 있고, 켠 뒤로는 계속 켜져 있어요.",
      ("켜기 전", "$n<0$: 값 0"),
      ("켜는 순간부터 계속", "$n\\geq 0$: 값 1"),
      ("스위치 켜기", K("step") + " $u[n]$")),
  figure("스위치를 켠 신호", FIG_STEP,
      "0번 칸부터 계속 1이에요. 계단처럼 한 번 올라가요."),
 ],
 "pass2": [
  formula("단위 계단의 정의",
      r"u[n]=\begin{cases}0, & n<0\\ 1, & n\geq 0\end{cases}",
      [(r"u[n]", "'유 n'이라고 읽어요. 영어 unit step의 u"),
       (r"n<0", "음수 칸에서는 0"),
       (r"n\geq 0", "0번 칸을 포함해 그 뒤로 모두 1")],
      "0번 칸부터 계속 1인 신호예요."),
  formula("임펄스 = 계단의 1차 차분",
      r"\delta[n]=u[n]-u[n-1]",
      [(r"u[n-1]", "계단을 오른쪽으로 1칸 옮긴 것"),
       (r"u[n]-u[n-1]", "지금 값에서 바로 앞 칸 값을 뺀 것: " + K("fdiff"))],
      "계단에서 한 칸 늦은 계단을 빼면, 달라지는 곳은 0번 칸 하나뿐이라 임펄스가 남아요."),
  compare("임펄스와 계단", ["", K("imp"), K("step")],
      ["기호", "$\\delta[n]$", "$u[n]$"],
      ["값이 1인 곳", "$n=0$ 한 칸", "$n\\geq 0$ 모두"],
      ["비유", "손뼉 한 번", "스위치 켜기"]),
  check(K("fdiff") + "란 무엇일까요?", ["지금 값 + 바로 앞 값", "지금 값 - 바로 앞 값", "처음부터 지금까지 합"], 1,
      "1차 차분은 $x[n]-x[n-1]$, 한 칸 사이의 변화량이에요. 처음부터의 합은 " + K("rsum") + "이에요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (150, 158, 930, 198, "이산시간 단위 임펄스와 단위 계단"),
      (205, 222, 670, 262, "이산 단위 계단 신호(unit step signal)의 정의"),
      (205, 275, 530, 368, "$n<0$이면 0, $n\\geq 0$이면 1"),
      (805, 262, 1335, 372, "그림: 0번 칸부터 높이 1인 막대가 계속"),
      (205, 395, 720, 440, "계단도 다른 신호를 분석하는 기본 단위(basis)"),
      (205, 458, 1125, 558, "임펄스는 계단의 " + K("fdiff") + ": $\\delta[n]=u[n]-u[n-1]$")),
  steps("u[n] - u[n-1] 표로 계산",
      ["$n=-1$: $u[-1]-u[-2]=0-0=0$.",
       "$n=0$: $u[0]-u[-1]=1-0=1$.",
       "$n=1$: $u[1]-u[0]=1-1=0$.",
       "$n=2$: $u[2]-u[1]=1-1=0$."],
      "$0, 1, 0, 0$: 바로 $\\delta[n]$이에요."),
  figure("계단 빼기 한 칸 늦은 계단", FIG_UDIFF,
      "위 두 줄을 칸마다 빼면, 0번 칸만 1이 남아요."),
  prof("0보다 작을 때는 0, 0부터는 계속 1이 찍혀서 계단 같으니 계단 함수(step function)라고 부른다고 하셨어요.",
      "$u[n-1]$은 오른쪽으로 1만큼 옮긴 것이고, 헷갈리면 n에 숫자를 넣어 보라고 하셨어요($n=0$이면 $u[-1]=0$).",
      "빼면 0에서만 차이가 나서 임펄스가 되고, 이것을 first difference, 연속시간에서는 미분(derivative)이라고 부른다고 하셨어요."),
 ],
 "pass4": [
  check("$u[n-3]-u[n-4]$는 어떤 신호일까요?", ["$\\delta[n]$", "$\\delta[n-3]$", "$\\delta[n-4]$"], 1,
      "3칸 늦은 계단에서 4칸 늦은 계단을 빼면, 3번 칸만 1이 남아요."),
  warn("헷갈리기 쉬운 점",
      "$u[0]=1$이에요. 0번 칸부터 켜져 있어요. 0인 것은 음수 칸뿐이에요.",
      "$u[n-1]$은 오른쪽(늦게)으로 옮긴 것이에요. 괄호 안 빼기는 오른쪽이라는 것, 꼭 기억해요."),
  english("시험 답안에 쓸 문장",
      "단위 계단 $u[n]$은 $n\\geq 0$에서 1, $n<0$에서 0이며, 단위 임펄스는 단위 계단의 1차 차분 $\\delta[n]=u[n]-u[n-1]$이다.",
      "계단 - 한 칸 늦은 계단 = 임펄스.",
      "'계단 빼기 늦은 계단은 손뼉'."),
 ]})

# ---------------------------------------------------------------------
# p.47 (슬라이드 45) 누적 합: u[n] = sum_{m=-inf}^{n} delta[m]
# ---------------------------------------------------------------------
rsum = lambda n: sum(delta(m) for m in range(-50, n + 1))
assert rsum(-2) == 0 and rsum(0) == 1 and rsum(3) == 1
assert all(rsum(n) == u(n) for n in range(-10, 11))
_x = [1, 2, 3]
_acc = [sum(_x[:i + 1]) for i in range(3)]
assert _acc == [1, 3, 6]

S.append({"p": 47, "title": "단위 계단은 단위 임펄스의 누적 합",
 "pass1": [
  say("손뼉 소리를 '처음부터 지금까지 몇 번 들었나' 세어 봐요.",
      "손뼉을 치기 전에는 0번이에요.",
      "손뼉을 한 번 친 뒤로는 언제 세어도 1번이에요.",
      "그래서 세어 둔 횟수는 스위치를 켠 모양, 곧 계단이 돼요."),
  figure("지금까지 더하면", FIG_RSUM,
      "지금이 손뼉 전이면 합은 0, 손뼉 뒤면 합은 1이에요."),
 ],
 "pass2": [
  formula("누적 합으로 계단 만들기",
      r"u[n]=\sum_{m=-\infty}^{n}\delta[m]",
      [(r"\sum", K("sigma") + ": 차례로 더하라는 뜻"),
       (r"m=-\infty", "아주 먼 과거 칸부터"),
       (r"n", "지금 칸까지"),
       (r"\delta[m]", "더할 값: 0번 칸에서만 1")],
      "먼 과거부터 지금까지 임펄스를 더한 것이 계단이에요. 이것을 " + K("rsum") + "이라고 해요."),
  compare("뺄셈과 덧셈은 짝", ["", "계단 → 임펄스", "임펄스 → 계단"],
      ["방법", K("fdiff") + " (빼기)", K("rsum") + " (더하기)"],
      ["식", "$u[n]-u[n-1]$", "$\\sum_{m=-\\infty}^{n}\\delta[m]$"],
      ["연속시간에서는", K("deriv"), K("integ")]),
  check(K("rsum") + "의 뜻은?", ["처음부터 지금까지의 값을 모두 더한 것", "지금 값에서 앞 값을 뺀 것", "지금 값 하나"], 0,
      "running sum, 달려가며 더한 합이에요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (150, 158, 920, 200, "이산시간 단위 임펄스와 단위 계단"),
      (200, 222, 1035, 262, "단위 계단은 단위 임펄스의 running sum(적분 같은 것)"),
      (325, 340, 725, 488, "(a) 지금 n이 음수: 더하는 구간에 임펄스가 없어서 합은 0"),
      (330, 500, 725, 655, "(b) 지금 n이 양수: 구간에 0번 칸 임펄스가 들어와 합은 1"),
      (735, 530, 935, 598, "$u[n]=\\sum_{m=-\\infty}^{n}\\delta[m]$"),
      (735, 610, 940, 660, "Figure 1.30: (a) $n<0$, (b) $n>0$")),
  steps("누적 합 손계산",
      ["$u[-2]$: $m=\\dots,-3,-2$까지 더해요. $\\delta$는 모두 $0$ → 합 $0$.",
       "$u[0]$: $m=0$까지. $\\delta[0]=1$이 들어와서 합 $1$.",
       "$u[3]$: $m=3$까지. 1은 0번 칸 한 번뿐 → 합 $1$."],
      "$u[-2]=0$, $u[0]=1$, $u[3]=1$"),
  steps("임펄스가 아닌 신호의 누적 합",
      ["입력 $x[0]=1$, $x[1]=2$, $x[2]=3$ (나머지 0).",
       "$n=0$까지 합: $1$.",
       "$n=1$까지 합: $1+2=3$.",
       "$n=2$까지 합: $3+3=6$."],
      "누적 합은 $1, 3, 6$. 매번 앞의 합에 새 값을 더해요."),
  prof("마이너스 무한부터 지금의 나까지 쭉 더해 오는 것이 running sum이라고 하셨어요.",
      "통장 예: 0번 칸에서 100만 원이 한 번 입금되면, 그 뒤 잔고는 언제 봐도 계속 100만 원이라고 설명하셨어요.",
      "이산시간은 임펄스가 딱 1로 찍히니 쉽다고 하셨어요."),
  bg("기초 다지기 b-7 시그마로 더하기",
      "$\\sum_{m=a}^{b}$는 'm을 a부터 b까지 하나씩 바꾸며 더하라'는 뜻이에요.",
      "아래 숫자가 시작, 위 숫자가 끝이에요."),
 ],
 "pass4": [
  check("$\\sum_{m=-\\infty}^{5}\\delta[m]$의 값은?", ["$0$", "$1$", "$5$"], 1,
      "0번 칸의 1이 더해지는 구간 안에 들어 있어요. 다른 칸은 0이라 합은 1이에요."),
  warn("헷갈리기 쉬운 점",
      "m은 더하는 동안 움직이는 칸 번호, n은 '지금'이에요. 합의 끝이 n이라서 결과는 n의 함수예요.",
      "누적 합(더하기)과 " + K("fdiff") + "(빼기)는 서로 되돌리는 짝이에요."),
  english("시험 답안에 쓸 문장",
      "단위 계단은 단위 임펄스의 누적 합이다: $u[n]=\\sum_{m=-\\infty}^{n}\\delta[m]$.",
      "과거부터 지금까지 손뼉 수 = $0$ 또는 $1$.",
      "'빼면 임펄스, 더하면 계단'."),
 ]})

# ---------------------------------------------------------------------
# p.48 (슬라이드 46) u[n] = sum_{k=0}^{inf} delta[n-k]
# ---------------------------------------------------------------------
rsum2 = lambda n: sum(delta(n - k) for k in range(0, 60))
assert rsum2(2) == 1 and rsum2(-1) == 0 and all(rsum2(n) == u(n) for n in range(-10, 30))
assert [k for k in range(0, 60) if delta(2 - k)] == [2]

S.append({"p": 48, "title": "계단은 늦은 손뼉들의 합",
 "pass1": [
  say("같은 계단을 다른 방법으로 만들어 봐요.",
      "0번 칸에 손뼉, 1번 칸에 손뼉, 2번 칸에 손뼉... 계속 쳐요.",
      "이 손뼉들을 모두 모으면 0번 칸부터 계속 1인 계단이 돼요."),
  figure("늦게 치는 손뼉을 모으면", FIG_DSUM,
      "k칸 늦은 손뼉들을 하나씩 더하면 계단 모양이 돼요."),
 ],
 "pass2": [
  formula("늦은 임펄스들의 합",
      r"u[n]=\sum_{k=0}^{\infty}\delta[n-k]",
      [(r"\sum_{k=0}^{\infty}", K("sigma") + ": k를 0부터 끝없이 바꾸며 더해요"),
       (r"\delta[n-k]", "k칸 늦게(오른쪽으로 k칸 " + K("shift") + ") 치는 손뼉"),
       (r"k=0", "0칸 늦은 손뼉부터"),
       (r"\infty", "끝없이 모두")],
      "0칸, 1칸, 2칸... 늦은 손뼉을 모두 더하면 계단이에요."),
  compare("계단을 만드는 두 가지 방법", ["", "p.47", "p.48"],
      ["식", "$\\sum_{m=-\\infty}^{n}\\delta[m]$", "$\\sum_{k=0}^{\\infty}\\delta[n-k]$"],
      ["느낌", "왼쪽(과거)부터 지금까지 더하기", "늦은 손뼉들을 모두 겹치기"]),
  check("$\\delta[n-2]$는 어떤 신호일까요?", ["2번 칸에만 1", "-2번 칸에만 1", "2번 칸부터 계속 1"], 0,
      "괄호 안 $n-2=0$인 $n=2$에서만 1이에요. 2칸 늦은 손뼉이에요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (150, 155, 920, 195, "이산시간 단위 임펄스와 단위 계단"),
      (200, 218, 1035, 258, "앞 쪽과 같은 누적 합을 다른 변수로 쓴 것"),
      (345, 310, 720, 480, "(a) $n<0$: $\\delta[n-k]$의 막대가 더하는 구간($k\\geq 0$) 밖이라 합 0"),
      (345, 510, 720, 685, "(b) $n>0$: 막대가 구간 안이라 합 1"),
      (785, 532, 975, 598, "$u[n]=\\sum_{k=0}^{\\infty}\\delta[n-k]$"),
      (735, 638, 1000, 688, "Figure 1.31: (a) $n<0$, (b) $n>0$")),
  steps("변수 바꾸기와 손계산",
      ["앞 쪽 식에서 $k=n-m$으로 바꿔요.",
       "$m=-\\infty$이면 $k=\\infty$, $m=n$이면 $k=0$이 돼요.",
       "더하는 순서는 바꿔도 되니 $\\sum_{k=0}^{\\infty}\\delta[n-k]$예요.",
       "$u[2]$: $\\delta[2]+\\delta[1]+\\delta[0]+\\dots$ 중 $k=2$일 때 $\\delta[0]=1$ → 합 $1$.",
       "$u[-1]$: $\\delta[-1-k]$는 $k\\geq 0$에서 한 번도 0번 칸이 안 돼요 → 합 $0$."],
      "$u[2]=1$, $u[-1]=0$"),
  prof("k를 n 빼기 m으로 치환하면, 이번에는 오른쪽에서 더해 오는 느낌이라고 하셨어요.",
      "이 식은 지연된 임펄스들의 합(superposition of delayed impulses)이라서 나중에 의미가 있다고 하셨어요.",
      "지금 당장은 알아둘 필요는 없고, 앞 쪽처럼 왼쪽부터 더해 오는 방식이 이해하기 더 쉽다고 하셨어요."),
  bg("기초 다지기 b-9 단위 계단과 단위 임펄스",
      "여러 신호를 겹쳐 더하는 것을 " + K("superpos") + "라고 해요.",
      "늦은 손뼉을 " + K("superpos") + "로 모으는 생각은 3주차 " + K("conv") + "의 출발점이에요."),
 ],
 "pass4": [
  check("$\\sum_{k=0}^{\\infty}\\delta[n-k]$에서 $n=-3$일 때 값은?", ["$0$", "$1$", "$3$"], 0,
      "$k\\geq 0$이면 $-3-k$는 늘 음수라 0번 칸이 될 수 없어요. 합은 0이에요."),
  warn("헷갈리기 쉬운 점",
      "$\\delta[n-k]$는 k칸 늦은 손뼉이에요. k가 0부터라서 음수 칸의 손뼉은 없어요.",
      "교수님이 이 치환은 지금 꼭 알 필요는 없다고 하셨으니, '늦은 손뼉들의 " + K("superpos") + "' 그림만 기억해요."),
  english("시험 답안에 쓸 문장",
      "단위 계단은 지연된 단위 임펄스들의 합으로도 쓸 수 있다: $u[n]=\\sum_{k=0}^{\\infty}\\delta[n-k]$.",
      "0칸, 1칸, 2칸... 늦은 손뼉을 모두 모으면 계단.",
      "'늦은 손뼉 모으기'."),
 ]})

# ---------------------------------------------------------------------
# p.49 (슬라이드 47) 임펄스로 한 칸 값 뽑기 (샘플링)
# ---------------------------------------------------------------------
xsq = lambda n: n * n + 1
assert [xsq(n) * delta(n - 2) for n in (1, 2, 3)] == [0, 5, 0]
assert sum(xsq(n) * delta(n - 2) for n in range(-20, 21)) == 5
assert all(xsq(n) * delta(n) == xsq(0) * delta(n) for n in range(-5, 6))
_x2 = lambda n: 2.0 ** n
assert _x2(-1) == 0.5

S.append({"p": 49, "title": "임펄스를 곱하면 한 칸 값만 남아요",
 "pass1": [
  say("어떤 신호에 손뼉 한 번 신호를 곱해 봐요.",
      "손뼉이 없는 칸은 0을 곱하니 모두 0이 돼요.",
      "손뼉이 있는 칸만 원래 값이 남아요.",
      "사진을 딱 한 장 찍어서 그 순간 값만 뽑는 것과 같아요."),
 ],
 "pass2": [
  formula("0번 칸 값 뽑기",
      r"x[n]\delta[n]=x[0]\delta[n]",
      [(r"x[n]\delta[n]", "신호와 임펄스를 칸마다 곱한 것"),
       (r"x[0]", "0번 칸의 값(숫자 하나)"),
       (r"x[0]\delta[n]", "0번 칸에만 높이 $x[0]$인 막대")],
      "임펄스를 곱하면 0번 칸 값만 남아요."),
  formula("아무 칸이나 뽑기",
      r"x[n]\delta[n-n_0]=x[n_0]\delta[n-n_0]",
      [(r"\delta[n-n_0]", "$n_0$칸으로 옮긴 손뼉(" + K("shift") + ")"),
       (r"x[n_0]", "$n_0$번 칸의 값")],
      "옮긴 임펄스를 곱하면 그 칸의 값을 뽑아요. 이것을 " + K("samp") + ", " + K("sift") + "이라고 해요."),
  check("$x[n]\\delta[n-4]$는?", ["$x[4]\\delta[n-4]$", "$x[0]\\delta[n]$", "$x[n-4]$"], 0,
      "$\\delta[n-4]$는 4번 칸에만 1이라서 4번 칸 값 $x[4]$만 남아요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (150, 165, 975, 208, "이산시간 단위 임펄스와 단위 계단"),
      (205, 228, 1200, 270, "단위 임펄스로 신호의 $n=0$ 값을 뽑을(sample) 수 있어요."),
      (235, 292, 480, 332, "$x[n]\\delta[n]=x[0]\\delta[n]$"),
      (205, 358, 420, 398, "$n=n_0$에서 뽑기"),
      (240, 432, 595, 472, "$x[n]\\delta[n-n_0]=x[n_0]\\delta[n-n_0]$")),
  steps("쉬운 숫자로 뽑기",
      ["신호: $x[n]=n^2+1$. 그러면 $x[2]=2^2+1=5$.",
       "$\\delta[n-2]$는 2번 칸에만 1이에요.",
       "$n=1$: $x[1]\\times 0=0$. $n=2$: $5\\times 1=5$. $n=3$: $x[3]\\times 0=0$.",
       "그래서 $x[n]\\delta[n-2]=5\\delta[n-2]$예요.",
       "모든 칸을 더하면 $\\sum_n x[n]\\delta[n-2]=5$: 값 하나를 골라냈어요."],
      "$x[n]\\delta[n-2]=x[2]\\delta[n-2]=5\\delta[n-2]$"),
  figure("곱하면 2번 칸만 남아요", FIG_SAMP,
      "위: $x[n]=n^2+1$. 아래: 임펄스를 곱한 결과, 2번 칸의 5만 남아요."),
  prof("$x[n]\\delta[n]$에서 n에 0이 아닌 것을 넣으면 $\\delta$ 때문에 0이 되니, 결국 $x[0]\\delta[n]$과 같다고 하셨어요.",
      "임펄스를 통해 $x[0]$ 값을 샘플링해 오는 느낌이라고 하셨어요.",
      "원래는 모든 n을 봐야 하는데, 임펄스를 곱하면 원하는 한 값만 뽑아 올 수 있다고 설명하셨어요."),
 ],
 "pass4": [
  exam("연습 문제 (p.49 샘플링 식)",
      "Simplify $x[n]\\delta[n+1]$ for $x[n]=2^n$.",
      "$x[n]=2^n$일 때 $x[n]\\delta[n+1]$을 간단히 하세요.",
      ["$\\delta[n+1]$은 괄호 안이 0인 $n=-1$에만 1이에요.",
       "$x[-1]=2^{-1}=0.5$예요.",
       "그래서 $x[n]\\delta[n+1]=x[-1]\\delta[n+1]$."],
      "$0.5\\,\\delta[n+1]$"),
  warn("헷갈리기 쉬운 점",
      "결과 $x[0]\\delta[n]$은 숫자가 아니라 신호예요(한 칸에만 값이 있는 신호). 숫자 $x[0]$을 얻으려면 모든 칸을 더해요.",
      "$x[n_0]$은 상수라서 n이 바뀌어도 그대로예요. 움직이는 것은 $\\delta[n-n_0]$뿐이에요."),
  english("시험 답안에 쓸 문장",
      "단위 임펄스를 곱하면 한 점의 값만 남는다: $x[n]\\delta[n-n_0]=x[n_0]\\delta[n-n_0]$ (샘플링 성질).",
      "임펄스가 있는 칸만 살아남아요.",
      "'곱하면 그 칸만'."),
 ]})

# ---------------------------------------------------------------------
# p.50 (슬라이드 48) 연속시간 단위 임펄스 delta(t)
# ---------------------------------------------------------------------
_dx = 1e-4
assert abs(sum((1 / 0.01 if 0 <= i * _dx < 0.01 else 0) * _dx for i in range(0, 1000)) - 1) < 1e-6

S.append({"p": 50, "title": "연속시간 단위 임펄스 δ(t)",
 "pass1": [
  say("연속시간에서도 손뼉 한 번 신호가 있어요.",
      "그런데 연속시간 손뼉은 아주 특별해요. 폭은 0, 높이는 끝없이 높아요.",
      "대신 넓이가 딱 1이에요. 그래서 그림에서는 화살표로 그려요."),
  figure("화살표로 그리는 손뼉", FIG_DCT,
      "화살표 옆 숫자는 높이가 아니라 넓이예요."),
 ],
 "pass2": [
  formula("연속시간 단위 임펄스",
      r"\delta(t)=\begin{cases}0, & t\neq 0\\ \infty, & t=0\end{cases},\qquad \int_{-\infty}^{\infty}\delta(t)\,dt=1",
      [(r"\delta(t)", "둥근 괄호: 연속시간 " + K("imp")),
       (r"\infty", "0에서의 높이는 끝이 없어요(무한대)"),
       (r"\int\delta(t)\,dt=1", "넓이는 1이에요")],
      "0에서만 무한히 높고 넓이가 1인, 폭 없는 톡이에요."),
  compare("이산시간과 연속시간의 임펄스", ["", "$\\delta[n]$ (이산)", "$\\delta(t)$ (연속)"],
      ["0에서의 값", "$1$", "무한대"],
      ["1이라는 숫자의 뜻", "높이", "넓이"],
      ["그림", "점 달린 막대", "화살표"]),
  check("$\\delta(t)$ 그림의 화살표 옆에 적힌 1은 무엇일까요?", ["높이", "넓이", "시간"], 1,
      "$\\delta(t)$의 높이는 무한대라 적을 수 없어요. 그래서 넓이 1을 옆에 적어요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (160, 158, 950, 200, "연속시간 단위 계단과 단위 임펄스"),
      (210, 222, 730, 258, "연속 단위 임펄스 신호의 정의"),
      (215, 262, 525, 358, "$t\\neq 0$이면 0, $t=0$이면 무한대"),
      (210, 392, 610, 432, "$t=0$에서 끊겨 있어요(불연속)."),
      (210, 452, 865, 492, "화살표는 실제 값이 아니라 넓이를 나타내요."),
      (965, 255, 1230, 412, "그림: 0에 세운 화살표, 옆의 1은 넓이")),
  steps("크기를 바꾼 임펄스",
      ["$\\delta(t)$의 넓이는 $1$이에요.",
       "$3\\delta(t)$는 모든 곳에 3을 곱했으니 넓이가 $3\\times 1=3$이에요.",
       "그림에서는 화살표 옆에 $3$이라고 적어요.",
       "$3\\delta(t-3)$은 그 화살표를 $t=3$으로 옮긴 것이에요."],
      "화살표 옆 숫자 = 넓이 = 임펄스 앞에 곱한 수"),
  prof("0에서 무한이 되어야 하고 나머지는 0이어야 하는데, 이렇게 보면 이해하기 어렵다고 하셨어요.",
      "옆에 적힌 숫자 $1$ 때문에 높이가 1이라고 착각하는 사람이 많은데, 값은 무한대이고 넓이가 1임을 표시한 것이라고 강조하셨어요.",
      "크기를 바꾼 임펄스(scaled impulse)는 화살표 옆에 k라고 표시하고, 넓이가 k라고 하셨어요."),
 ],
 "pass4": [
  check("$5\\delta(t-2)$를 그림으로 그리면?",
      ["$t=5$에 높이 2인 막대", "$t=2$에 옆에 5라고 적은 화살표", "$t=-2$에 옆에 5라고 적은 화살표"], 1,
      "괄호 안이 0인 $t=2$에 화살표, 넓이 5를 옆에 적어요."),
  warn("헷갈리기 쉬운 점",
      "화살표 옆 1은 높이가 아니라 넓이예요. 교수님이 특히 많이 착각한다고 짚으신 부분이에요.",
      "$\\delta[n]$(높이 1)과 $\\delta(t)$(높이 무한대, 넓이 1)는 괄호 모양으로 구별해요."),
  english("시험 답안에 쓸 문장",
      "연속시간 단위 임펄스 $\\delta(t)$는 $t\\neq 0$에서 0이고 넓이가 1인 신호로, 화살표로 그리며 화살표 옆 숫자는 넓이를 뜻한다.",
      "높이는 무한대, 넓이는 1.",
      "'화살표 옆은 넓이'."),
 ]})

# ---------------------------------------------------------------------
# p.51 (슬라이드 49) 비탈길 u_Delta 와 좁은 직사각형 delta_Delta
# ---------------------------------------------------------------------
for _d in (1, 0.5, 0.1, 0.01):
    assert abs(_d * (1 / _d) - 1) < 1e-12
assert [fmt(1 / d) for d in (1, 0.5, 0.1, 0.01)] == ["1", "2", "10", "100"]

S.append({"p": 51, "title": "δ(t)는 좁아지는 직사각형의 끝",
 "pass1": [
  say("스위치를 켜는 계단은 한순간에 뚝 올라가요.",
      "이것을 아주 짧은 비탈길로 바꿔 보면, 오르는 동안의 기울기가 좁은 직사각형이 돼요.",
      "비탈을 점점 짧게 하면 직사각형은 좁고 높아지다가, 결국 손뼉(임펄스)이 돼요."),
  figure("좁아질수록 높아져요", FIG_DDELTA,
      "폭이 절반이면 높이는 2배. 넓이는 늘 1이에요."),
 ],
 "pass2": [
  formula("계단과 임펄스의 관계 (연속시간)",
      r"u(t)=\int_{-\infty}^{t}\delta(\tau)\,d\tau,\qquad \delta(t)=\frac{du(t)}{dt}",
      [(r"\int_{-\infty}^{t}", "먼 과거부터 지금 t까지 넓이를 모아요(" + K("integ") + ")"),
       (r"\tau", "'타우'. 적분하는 동안 움직이는 시간 변수"),
       (r"\frac{du(t)}{dt}", "계단의 기울기(" + K("deriv") + ")")],
      "계단은 임펄스를 모은 것, 임펄스는 계단의 기울기예요. 이산시간의 누적 합, 1차 차분과 짝이에요."),
  formula("근사로 이해하기",
      r"\delta_\Delta(t)=\frac{du_\Delta(t)}{dt},\qquad \delta(t)=\lim_{\Delta\to 0}\delta_\Delta(t)",
      [(r"u_\Delta(t)", "0에서 Δ 동안 비탈로 올라가는 계단"),
       (r"\delta_\Delta(t)", "그 비탈의 기울기: 폭 Δ, 높이 1/Δ인 직사각형"),
       (r"\lim_{\Delta\to 0}", "Δ를 0에 한없이 가깝게 줄인다는 뜻")],
      "직사각형을 한없이 좁게 하면 $\\delta(t)$예요."),
  check("$\\delta_\\Delta(t)$의 높이는?", ["$\\Delta$", "$1/\\Delta$", "$1$"], 1,
      "Δ 시간 동안 1만큼 올라가니 기울기는 $1/\\Delta$예요. 폭 Δ x 높이 1/Δ = 넓이 1."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (190, 225, 370, 282, "$u(t)=\\int_{-\\infty}^{t}\\delta(\\tau)d\\tau$: 계단은 임펄스의 적분"),
      (420, 225, 565, 282, "$\\delta(t)=du(t)/dt$: 임펄스는 계단의 미분"),
      (420, 325, 580, 485, "$\\delta_\\Delta=du_\\Delta/dt$, 그리고 Δ를 0으로 보내면 $\\delta(t)$"),
      (728, 245, 1025, 455, "Figure 1.33: 0에서 Δ까지 비탈로 오르는 $u_\\Delta(t)$"),
      (1040, 278, 1255, 455, "Figure 1.34: 그 기울기 $\\delta_\\Delta(t)$, 높이 1/Δ인 직사각형"),
      (1030, 508, 1285, 658, "Δ를 0으로 보낸 끝: $\\delta(t)$ 화살표")),
  steps("폭과 높이 손계산",
      ["$\\Delta=1$: 높이 $1/1=1$, 넓이 $1\\times 1=1$.",
       "$\\Delta=0.5$: 높이 $1/0.5=2$, 넓이 $0.5\\times 2=1$.",
       "$\\Delta=0.1$: 높이 $10$, 넓이 $0.1\\times 10=1$.",
       "$\\Delta=0.01$: 높이 $100$, 넓이 $1$."],
      "폭은 0으로, 높이는 무한대로, 넓이는 늘 1: 이것이 $\\delta(t)$예요."),
  bg("기초 다지기 b-8 적분은 넓이, 미분은 기울기",
      "기울기 = 올라간 높이 ÷ 걸린 시간이에요.",
      "Δ 시간에 1만큼 오르면 기울기는 $1/\\Delta$예요.",
      "그래서 비탈의 미분은 높이 $1/\\Delta$인 직사각형이에요."),
  prof("계단은 0에서 끊겨 있어서(불연속) 미분이 안 된다고 하셨어요. 그래서 $u_\\Delta$로 근사한다고 하셨어요.",
      "Δ 동안 1만큼 올라오려면 넓이가 1이어야 하니 높이가 1/Δ가 된다고 설명하셨어요.",
      "Δ를 0으로 보내면 폭은 줄고 높이는 커지고 넓이는 1을 유지해서, 결국 화살표로 그린다고 하셨어요."),
 ],
 "pass4": [
  check("$\\Delta=0.2$일 때 $\\delta_\\Delta(t)$의 높이는?", ["$0.2$", "$2$", "$5$"], 2,
      "높이 $=1/\\Delta=1/0.2=5$예요. 넓이는 $0.2\\times 5=1$."),
  warn("헷갈리기 쉬운 점",
      "$\\delta(t)=du/dt$는 보통의 미분이 아니에요. 끊긴 계단을 비탈로 근사해서 얻은 '약속'이에요.",
      "$\\tau$(타우)는 적분할 때 쓰는 이름표 변수예요. 결과는 끝점 t의 함수예요."),
  english("시험 답안에 쓸 문장",
      "연속시간에서 단위 계단은 단위 임펄스의 적분 $u(t)=\\int_{-\\infty}^{t}\\delta(\\tau)d\\tau$이고, 단위 임펄스는 단위 계단의 미분 $\\delta(t)=du(t)/dt$이다.",
      "이산의 누적 합/1차 차분 ↔ 연속의 적분/미분.",
      "'이산은 더하고 빼고, 연속은 적분하고 미분'."),
 ]})

# ---------------------------------------------------------------------
# p.52 (슬라이드 50) 연속시간 단위 계단 u(t) 와 누적 적분
# ---------------------------------------------------------------------
_run = lambda t: 1 if t > 0 else 0     # 넓이 1 인 임펄스를 지났는지
assert _run(-1) == 0 and _run(2) == 1 and _run(100) == 1

S.append({"p": 52, "title": "연속시간 단위 계단 u(t)와 누적 적분",
 "pass1": [
  analogy("스위치를 켜는 순간 (연속시간)",
      "시계가 0초를 가리키는 순간 스위치를 켜요. 그 전은 꺼짐, 그 뒤로는 계속 켜짐이에요.",
      ("0초 전", "$u(t)=0$"),
      ("0초 뒤 계속", "$u(t)=1$"),
      ("스위치 켜기", K("step") + " $u(t)$")),
  figure("끊김 없는 선으로 그린 계단", FIG_UCT,
      "0에서 한 번 올라가고 그 뒤로 계속 1이에요."),
 ],
 "pass2": [
  formula("연속시간 단위 계단",
      r"u(t)=\int_{-\infty}^{t}\delta(\tau)\,d\tau=\begin{cases}0, & t<0\\ 1, & t>0\end{cases}",
      [(r"\int_{-\infty}^{t}\delta(\tau)\,d\tau", "먼 과거부터 지금까지 임펄스 넓이를 모은 것"),
       (r"t<0", "아직 0의 화살표를 못 만났어요: 0"),
       (r"t>0", "넓이 1짜리 화살표를 지나왔어요: 1")],
      "지금까지 모은 넓이가 계단 값이에요. 이산시간의 " + K("rsum") + " 대신 누적 " + K("integ") + "이에요."),
  compare("이산시간과 연속시간의 계단", ["", "$u[n]$ (이산)", "$u(t)$ (연속)"],
      ["만드는 법", K("rsum") + " $\\sum$", "누적 적분 $\\int$"],
      ["0에서의 값", "$u[0]=1$", "정하지 않음(끊긴 곳)"]),
  check("$u(t)=\\int_{-\\infty}^{t}\\delta(\\tau)d\\tau$에서 $t=-1$이면?", ["$0$", "$1$", "무한대"], 0,
      "적분 구간이 0에 닿지 않아 화살표를 만나지 못했어요. 모은 넓이는 0이에요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (130, 150, 870, 192, "연속시간 단위 계단과 단위 임펄스"),
      (175, 208, 628, 242, "연속 단위 계단 신호의 정의"),
      (268, 258, 560, 322, "누적 적분으로 쓴 정의"),
      (268, 335, 550, 422, "$t<0$이면 0, $t>0$이면 1"),
      (238, 472, 540, 648, "$u(t)$ 그래프"),
      (845, 222, 1218, 692, "Figure 1.37: (a) $t<0$이면 구간에 화살표 없음, (b) $t>0$이면 화살표 포함")),
  steps("누적 적분 손계산",
      ["$u(-1)$: $-\\infty$부터 $-1$까지. 0의 화살표를 못 만나요 → 넓이 $0$.",
       "$u(2)$: $2$까지. 0의 화살표(넓이 1)를 지나요 → $1$.",
       "$u(100)$: 더 가도 다른 화살표는 없어요 → 계속 $1$."],
      "$u(-1)=0$, $u(2)=1$, $u(100)=1$"),
  prof("연속시간 단위 계단은 0에 구멍이 뚫려 있어서, $t=0$에서는 정의가 안 된다(불연속)고 주의를 주셨어요.",
      "이번에는 더해 오는 게 아니라 적분(running integral)의 개념이라고 하셨어요.",
      "교재에 있는, 오른쪽에서 적분해 오는 다른 형태는 조금 어려울 것 같아서 스킵한다고 하셨어요."),
 ],
 "pass4": [
  check("다음 중 맞는 것은?", ["$u(t)$는 $t=0$에서 1로 정해져 있다", "$u[n]$은 $n=0$에서 1이다", "$u[n]$은 $n=0$에서 0이다"], 1,
      "이산시간 $u[0]=1$은 정의에 있어요. 연속시간 $u(t)$는 $t=0$ 값을 정하지 않았어요."),
  warn("헷갈리기 쉬운 점",
      "슬라이드 식은 $t<0$과 $t>0$만 적혀 있어요. $t=0$이 빠진 것은 오타가 아니라 일부러 정하지 않은 거예요.",
      "그림의 점선 구간(Interval of integration)이 0의 화살표를 포함하느냐가 답을 정해요."),
  english("시험 답안에 쓸 문장",
      "연속시간 단위 계단은 단위 임펄스의 누적 적분으로, $t<0$에서 0, $t>0$에서 1이며 $t=0$에서 불연속이다.",
      "지금까지 모은 임펄스 넓이 = $0$ 또는 $1$.",
      "'모은 넓이가 계단'."),
 ]})

# ---------------------------------------------------------------------
# p.53 (슬라이드 51) x(t) delta(t) = x(0) delta(t)
# ---------------------------------------------------------------------
_lin = lambda t: t + 3
_D = 0.1
_avg = sum(_lin(i * _D / 1000) for i in range(1000)) / 1000
assert abs(_avg - 3.05) < 1e-3
assert abs(math.cos(PI * 1) + 1) < 1e-12

S.append({"p": 53, "title": "연속시간에서도 임펄스를 곱하면 한 점 값만",
 "pass1": [
  say("연속시간에서도 손뼉과 곱하면 그 순간 값만 남아요.",
      "좁은 직사각형 안쪽에서만 곱한 값이 살아남아요.",
      "직사각형이 아주 좁으면, 그 안의 값은 거의 0초의 값 하나예요."),
  figure("좁은 칸 안의 값만", FIG_XDELTA,
      "좁은 칸 밖은 0을 곱해 사라지고, 칸 안의 $x(0)$ 근처 값만 남아요."),
 ],
 "pass2": [
  formula("연속시간 샘플링",
      r"x(t)\delta(t)=x(0)\delta(t)",
      [(r"x(t)\delta_\Delta(t)", "먼저 좁은 직사각형과 곱해요"),
       (r"x(0)", "직사각형이 아주 좁으면 그 안의 x는 거의 $x(0)$"),
       (r"x(0)\delta(t)", "넓이가 $x(0)$인 임펄스")],
      "임펄스를 곱하면 0초의 값 $x(0)$만 남아요. 이산시간과 같은 " + K("sift") + "이에요."),
  compare("샘플링 식 비교", ["", "이산시간", "연속시간"],
      ["식", "$x[n]\\delta[n]=x[0]\\delta[n]$", "$x(t)\\delta(t)=x(0)\\delta(t)$"],
      ["남는 것", "높이 $x[0]$인 막대", "넓이 $x(0)$인 화살표"]),
  check("$x(t)\\delta(t)$와 같은 것은?", ["$x(t)$", "$x(0)\\delta(t)$", "$\\delta(t)$"], 1,
      "$\\delta(t)$는 0에서만 0이 아니라서, $x$도 0에서의 값만 의미가 있어요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (160, 222, 375, 268, "먼저 좁은 직사각형 $\\delta_\\Delta(t)$와 곱한 $x_1(t)$"),
      (265, 275, 475, 408, "Δ를 0으로 보내면 $\\delta(t)$"),
      (160, 418, 385, 458, "결과: $x(t)\\delta(t)=x(0)\\delta(t)$"),
      (585, 262, 1015, 452, "Figure 1.39 (a): 신호 x(t)와 좁은 직사각형"),
      (578, 505, 1015, 700, "(b) 확대: 칸 안의 x는 거의 $x(0)$로 평평해요"),
      (1025, 612, 1310, 698, "그림 설명: 두 함수의 곱")),
  steps("쉬운 숫자로: $x(t)=t+3$",
      ["$x(0)=0+3=3$이에요.",
       "$\\Delta=0.1$: 칸 $[0, 0.1]$ 안의 x는 3에서 3.1, 평균 약 $3.05$.",
       "곱의 넓이 $\\approx$ 평균 $3.05\\times$ 높이 $10\\times$ 폭 $0.1=3.05$.",
       "Δ를 더 줄이면 평균이 3에 가까워져요.",
       "그래서 $x(t)\\delta(t)=3\\delta(t)$예요."],
      "$x(t)\\delta(t)=x(0)\\delta(t)=3\\delta(t)$"),
  prof("무한대를 곱한다는 개념 자체가 애매해서, 좁은 직사각형($\\delta_\\Delta$)으로 해석한다고 하셨어요.",
      "Δ가 아주 작으면 그 구간에서 x는 거의 $x(0)$이라서, 이산시간처럼 샘플링 효과를 볼 수 있다고 하셨어요."),
 ],
 "pass4": [
  check("$x(t)=\\cos(\\pi t)$일 때 $x(t)\\delta(t-1)$은?", ["$\\delta(t-1)$", "$-\\delta(t-1)$", "$\\cos(\\pi t)$"], 1,
      "옮긴 임펄스도 같은 원리예요. $x(1)=\\cos\\pi=-1$이라 $-\\delta(t-1)$이에요."),
  warn("헷갈리기 쉬운 점",
      "결과는 숫자 $x(0)$가 아니라, 넓이가 $x(0)$인 임펄스 신호예요.",
      "슬라이드는 $t=0$만 보였지만, 옮긴 임펄스 $\\delta(t-t_0)$도 똑같이 $x(t_0)$을 뽑아요."),
  english("시험 답안에 쓸 문장",
      "연속시간에서도 $x(t)\\delta(t)=x(0)\\delta(t)$이며, 이는 폭 Δ인 직사각형 $\\delta_\\Delta(t)$를 곱한 뒤 Δ를 0으로 보낸 결과로 이해한다.",
      "좁은 칸 안의 x는 거의 $x(0)$.",
      "'연속도 곱하면 한 점'."),
 ]})

# ---------------------------------------------------------------------
# p.54 (슬라이드 52) 끊긴 곳마다 임펄스
# ---------------------------------------------------------------------
_xs = lambda t: 0 if t < 1 else (2 if t < 2 else (-1 if t < 4 else 1))
_jumps = {1: _xs(1) - _xs(0.999), 2: _xs(2) - _xs(1.999), 4: _xs(4) - _xs(3.999)}
assert _jumps == {1: 2, 2: -3, 4: 2}
assert sum(v for k, v in _jumps.items() if k <= 3) == _xs(3) == -1
assert sum(_jumps.values()) == _xs(5) == 1

S.append({"p": 54, "title": "끊긴 곳마다 임펄스: 미분과 복원",
 "pass1": [
  say("계단처럼 뚝뚝 끊기는 신호를 생각해요.",
      "이 신호의 변화 빠르기(미분)를 보면, 평평한 곳은 0이고 끊긴 곳에서만 손뼉(임펄스)이 생겨요.",
      "손뼉의 크기는 뛰어오른(또는 떨어진) 높이와 같아요.",
      "손뼉 몇 개만 알면, 다시 모아서 원래 신호를 되살릴 수 있어요."),
  figure("끊긴 곳마다 화살표", FIG_JUMP,
      "위는 계단 신호, 아래는 그 미분. 점프 크기만큼의 화살표가 생겨요."),
 ],
 "pass2": [
  formula("점프를 임펄스로",
      r"\dot{x}(t)=2\delta(t-1)-3\delta(t-2)+2\delta(t-4)",
      [(r"\dot{x}(t)", "x 위의 점: x의 " + K("deriv") + "(변화 빠르기)"),
       (r"2\delta(t-1)", "$t=1$에서 2만큼 뛰어올라요"),
       (r"-3\delta(t-2)", "$t=2$에서 3만큼 떨어져요"),
       (r"2\delta(t-4)", "$t=4$에서 다시 2만큼 올라요")],
      "끊긴 곳마다, 점프 크기를 넓이로 가진 임펄스가 생겨요."),
  formula("누적 적분으로 되살리기",
      r"x(t)=\int_0^{t}\dot{x}(\tau)\,d\tau",
      [(r"\int_0^{t}", "0초부터 지금까지 모아요"),
       (r"\dot{x}(\tau)", "지금까지 만난 화살표들")],
      "지금까지 만난 화살표 넓이를 모두 더하면 지금의 값이에요."),
  check("신호가 $t=3$에서 1에서 4로 뛰어오르면, 미분에는 무엇이 생길까요?",
      ["$t=3$에 넓이 3인 임펄스", "$t=3$에 넓이 4인 임펄스", "$t=4$에 넓이 1인 임펄스"], 0,
      "점프 크기는 $4-1=3$이에요. 그 크기의 임펄스가 $t=3$에 생겨요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (80, 148, 1310, 198, "끊긴 x(t)에서는 점프마다 그 크기만큼의 임펄스가 미분에 생겨요."),
      (80, 198, 880, 242, "그리고 미분을 누적 적분하면 x(t)가 되살아나요."),
      (115, 320, 470, 600, "왼쪽: x(t). $0\\to 2\\to -1\\to 1$로 계단처럼 변해요."),
      (520, 310, 880, 600, "가운데: 미분. $t=1$에 +2, $t=2$에 -3, $t=4$에 +2 화살표"),
      (925, 320, 1285, 600, "오른쪽: 화살표를 모아 되살린 신호. 왼쪽과 똑같아요."),
      (550, 610, 840, 700, "되살리는 식: $x(t)=\\int_0^t\\dot{x}(\\tau)d\\tau$")),
  steps("점프와 되살리기 손계산",
      ["$t=1$: $0\\to 2$, 점프 $+2$.",
       "$t=2$: $2\\to -1$, 점프 $-1-2=-3$.",
       "$t=4$: $-1\\to 1$, 점프 $+2$.",
       "$x(3)$ 되살리기: 3초까지 만난 화살표 $2+(-3)=-1$.",
       "$x(5)$ 되살리기: $2-3+2=1$."],
      "점프 $+2, -3, +2$. $x(3)=-1$, $x(5)=1$로 원래 값과 같아요."),
  prof("계단 함수를 도함수(미분)로 보면 2만큼 올리고, 3만큼 내리고, 다시 2만큼 올리는 화살표가 된다고 하셨어요.",
      "화살표 몇 개로 신호를 나타낼 수 있어서 정보를 조금만 저장해도 되고, 적분하면 원래 신호가 복원된다고 하셨어요.",
      "이것이 임펄스가 가진 중요한 의미 중 하나라고 강조하셨어요."),
 ],
 "pass4": [
  exam("연습 문제 (p.54 점프와 임펄스)",
      "Find $\\dot{x}(t)$ for $x(t)=3u(t)-3u(t-2)$.",
      "$x(t)=3u(t)-3u(t-2)$를 미분하세요.",
      ["$x(t)$는 $t=0$에서 3으로 올라가고, $t=2$에서 0으로 내려오는 직사각형이에요.",
       "$t=0$ 점프: $+3$ → $3\\delta(t)$.",
       "$t=2$ 점프: $-3$ → $-3\\delta(t-2)$.",
       "평평한 곳의 미분은 0이에요."],
      "$\\dot{x}(t)=3\\delta(t)-3\\delta(t-2)$"),
  warn("헷갈리기 쉬운 점",
      "화살표 옆 숫자는 점프한 높이(나중 값 - 이전 값)예요. 떨어지면 음수라서 아래로 그려요.",
      "$\\dot{x}$의 점은 '시간으로 미분했다'는 표시예요. 곱하기 점이 아니에요."),
  english("시험 답안에 쓸 문장",
      "불연속인 신호를 미분하면 각 불연속점에 점프 크기만큼의 임펄스가 생기고, 그 미분을 누적 적분하면 원래 신호가 복원된다.",
      "끊긴 곳 = 화살표, 화살표 모으기 = 원래 신호.",
      "'점프는 임펄스'."),
 ]})

# ---------------------------------------------------------------------
# p.55 (슬라이드 53) 1.5 연속시간과 이산시간 시스템
# ---------------------------------------------------------------------
assert 2 * 3 == 6 and [2 * v for v in (1, -2, 5)] == [2, -4, 10]

S.append({"p": 55, "title": "1.5 시스템: 신호를 바꾸는 상자",
 "pass1": [
  analogy("목소리 변조기",
      "마이크에 목소리를 넣으면 로봇 목소리가 나오는 변조기가 있어요. 넣은 것과 나온 것이 둘 다 소리(신호)예요.",
      ("넣는 목소리", K("in") + " x"),
      ("나오는 로봇 목소리", K("out") + " y"),
      ("변조기 상자", K("sys"))),
  figure("연속시간 상자와 이산시간 상자", FIG_SYS,
      "선 신호를 바꾸면 연속시간 시스템, 점 신호를 바꾸면 이산시간 시스템이에요."),
  say(MANTRA,
      "지금까지는 신호를 배웠고, 이제부터는 상자를 배워요."),
 ],
 "pass2": [
  points("슬라이드 문장 풀어 읽기",
      K("sys") + "은 " + K("sig") + "를 입력으로 받아 다른 신호로 바꿔요.",
      "선형 시스템(" + K("lin") + "을 가진 시스템)은 과학 대부분에서 아주 중요해요.",
      "이유 1: 식으로 딱 떨어지는 답(closed form solution)이 있는 경우가 많아요.",
      "이유 2: 이론적인 분석이 훨씬 쉬워져요.",
      "이유 3: 선형이 아닌 시스템도 아주 작게 흔들릴 때는 선형처럼 볼 수 있어요(linearization, 선형화)."),
  compare("두 종류의 시스템", ["", "연속시간 시스템", "이산시간 시스템"],
      ["입력", "$x(t)$", "$x[n]$"],
      ["출력", "$y(t)$", "$y[n]$"],
      ["예", "RC 회로, 자동차(p.58, p.59)", "통장 잔고(p.60)"]),
  check(K("sys") + "에 대한 설명으로 맞는 것은?",
      ["신호를 받아 다른 신호로 바꿔 내보낸다", "신호만 있고 출력은 없다", "숫자 하나를 내보낸다"], 0,
      "시스템은 입력 신호 → 출력 신호로 바꾸는 상자예요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (110, 148, 545, 188, "간단한 시스템의 예"),
      (165, 210, 1035, 250, "시스템은 신호를 입력으로 받아 다른 신호로 바꿔요."),
      (165, 268, 860, 308, "선형 시스템은 과학 대부분에서 아주 중요한 역할을 해요."),
      (215, 328, 1240, 472, "세 가지 이유: 딱 떨어지는 답, 쉬운 분석, 작은 흔들림에서의 선형화"),
      (270, 528, 815, 690, "블록 그림: $x(t)\\to$ 연속시간 상자 $\\to y(t)$, $x[n]\\to$ 이산시간 상자 $\\to y[n]$")),
  steps("아주 간단한 시스템: 2배 상자",
      ["규칙: $y(t)=2x(t)$. 들어온 값을 2배로 내보내요.",
       "입력이 $3$이면 출력은 $2\\times 3=6$.",
       "입력이 $1, -2, 5$로 변하면 출력은 $2, -4, 10$.",
       "입력 신호가 바뀌면, 출력 신호도 규칙대로 바뀌어요."],
      "상자의 규칙(식)을 알면 어떤 입력에도 출력을 구할 수 있어요."),
  prof("1.5와 1.6은 수식이 거의 없어서 개념을 이해하면 되고, 조금 쉬울 거라고 하셨어요.",
      "인풋과 아웃풋이 있으면 그 안의 블랙박스는 모두 시스템이라고 볼 수 있다고 하셨어요.",
      "지금까지는 신호만 다뤘고, 1.5와 1.6은 시스템을 다룬다고 하셨어요."),
 ],
 "pass4": [
  check("다음 중 " + K("sys") + "의 예가 아닌 것은?",
      ["입력 전압을 받아 축전기 전압을 내는 회로", "지난달 잔고와 입금으로 이번 달 잔고를 내는 통장", "그냥 적혀 있는 체온 기록표 하나"], 2,
      "체온 기록표는 " + K("sig") + "예요. 시스템은 신호를 받아 신호로 바꾸는 상자예요."),
  warn("헷갈리기 쉬운 점",
      "신호와 시스템을 구별해요. 신호는 시간에 따라 변하는 값, 시스템은 그 값을 바꾸는 규칙(상자)이에요.",
      "linearization(선형화): 비선형 시스템도 아주 작은 흔들림 근처에서는 선형처럼 다룰 수 있다는 뜻이에요."),
  english("시험 답안에 쓸 문장",
      "시스템은 입력 신호를 받아 다른 출력 신호로 변환하는 것이며, 입력과 출력이 연속시간이면 연속시간 시스템, 이산시간이면 이산시간 시스템이다.",
      "상자 안이 무엇이든 입력 → 출력이면 시스템.",
      "'" + MANTRA + "'"),
 ]})

# ---------------------------------------------------------------------
# p.56 (슬라이드 54) 임펄스를 넣으면 h(t), 아무 입력이나 넣어도 출력
# ---------------------------------------------------------------------
S.append({"p": 56, "title": "시스템 예: 손뼉을 넣으면 메아리가 나와요",
 "pass1": [
  analogy("빈 방의 메아리",
      "빈 방에서 손뼉을 한 번 치면 '짝' 소리 뒤에 메아리가 울리다 사라져요. 방이라는 상자가 손뼉을 메아리로 바꾼 거예요.",
      ("손뼉 한 번", K("imp")),
      ("빈 방", "선형 " + K("sys")),
      ("울리는 메아리", K("ir") + " $h(t)$")),
  figure("손뼉 → 방 → 메아리", FIG_ECHO,
      "임펄스를 넣었을 때 나오는 출력을 " + K("ir") + "이라고 해요."),
 ],
 "pass2": [
  points("슬라이드의 두 줄",
      "위 줄: 임펄스(impulse in)를 넣으면 $h(t)$가 나와요(h(t) out).",
      "아래 줄: 아무렇게나 흔들리는 입력(arbitrary input)을 넣어도 어떤 출력(output)이 나와요.",
      "두 줄 모두 같은 상자 '선형 시스템 $h(t)$'예요.",
      "Linear는 " + K("lin", "을") + " 가진다는 뜻이에요. 1.6에서 자세히 배워요."),
  compare("입력과 출력", ["줄", K("in"), K("out")],
      ["위", "손뼉 한 번($\\delta(t)$)", K("ir") + " $h(t)$"],
      ["아래", "마구 흔들리는 신호", "부드럽게 바뀐 신호"]),
  check(K("ir") + " $h(t)$는 무엇일까요?", ["시스템에 넣는 입력", "임펄스를 넣었을 때 나오는 출력", "아무 입력의 출력"], 1,
      "손뼉(임펄스)을 넣었을 때 울리는 메아리가 $h(t)$예요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (110, 150, 1240, 240, "간단한 시스템 예: 시스템은 신호를 받아 다른 신호로 바꿔요."),
      (175, 262, 495, 385, "impulse in: 짧은 화살표 하나(손뼉)"),
      (555, 348, 812, 442, "Linear system $h(t)$: 선형 시스템 상자"),
      (905, 262, 1225, 405, "h(t) out: 출렁이다 가라앉는 메아리"),
      (175, 480, 495, 638, "arbitrary input: 마구 흔들리는 입력"),
      (905, 480, 1225, 638, "output: 같은 상자를 지나 부드러워진 출력")),
  prof("임펄스가 들어왔을 때 오른쪽 $h(t)$ 같은 것이 나오는 것도 시스템이라고 하셨어요.",
      "임의의 입력이 들어와 어떤 출력으로 변형되는 것도 모두 시스템이고, 시스템이라는 개념 자체는 '별 게 없다'고 하셨어요."),
  bg("기초 다지기 b-10 손으로 하는 컨볼루션",
      "3주차(2장)에서: 선형이고 시불변인 상자는 메아리 $h$ 하나만 알면 모든 출력을 구해요.",
      "입력의 한 칸 한 칸마다 메아리 도장을 크기만큼 찍고, 겹친 도장을 모두 더해요. 이것이 " + K("conv") + "이에요."),
 ],
 "pass4": [
  check("같은 상자에 손뼉 대신 아무 신호나 넣으면?", ["출력이 없다", "그 신호에 맞는 다른 출력이 나온다", "항상 $h(t)$가 나온다"], 1,
      "$h(t)$는 임펄스를 넣었을 때의 출력일 뿐이에요. 입력이 바뀌면 출력도 바뀌어요."),
  warn("헷갈리기 쉬운 점",
      "$h(t)$는 입력이 아니라 출력(임펄스를 넣었을 때의 출력)이에요.",
      "그런데 이 상자를 대표하는 이름으로도 $h(t)$를 써요. 그만큼 중요한 출력이라서예요."),
  english("시험 답안에 쓸 문장",
      "선형 시스템에 단위 임펄스를 입력했을 때의 출력을 임펄스 응답 $h(t)$라고 한다.",
      "손뼉을 넣었을 때의 메아리.",
      "'임펄스 넣으면 h'."),
 ]})

# ---------------------------------------------------------------------
# p.57 (슬라이드 55) 뇌파 예: 컨볼루션과 역컨볼루션
# ---------------------------------------------------------------------
S.append({"p": 57, "title": "시스템 예: 뇌파 장비, 컨볼루션과 역컨볼루션",
 "pass1": [
  say("뇌 속 신경 활동이 입력, 뇌파 장비(증폭기와 필터)가 " + K("sys") + ", 기록된 뇌파가 출력이에요.",
      "입력에서 출력을 계산하는 것을 " + K("conv") + "이라고 해요.",
      "거꾸로, 기록에서 원래 뇌 활동을 되찾는 것을 " + K("deconv") + "이라고 해요."),
  figure("앞으로 계산, 거꾸로 되찾기", FIG_CONV,
      "위 화살표는 컨볼루션, 아래 화살표는 역컨볼루션이에요."),
 ],
 "pass2": [
  compare("두 방향", ["", K("conv"), K("deconv")],
      ["방향", "입력 → 출력", "출력 → 입력"],
      ["이 쪽의 예", "뇌 활동으로 기록을 계산", "기록에서 뇌 활동을 되찾기"],
      ["배우는 때", "2장(3주차)", "용어만 알아 두기"]),
  check(K("deconv") + "이란?", ["입력으로 출력을 계산하는 것", "섞인 출력에서 원래 입력을 되찾는 것", "신호를 두 배로 키우는 것"], 1,
      "컨볼루션을 거꾸로 되돌리는 일이에요. 슬라이드 표현으로 'undoing it'이에요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (200, 350, 430, 500, "neural activity $x(t)$: 뇌 속 신경 활동(입력)"),
      (535, 378, 855, 492, "EEG system: 증폭기 + 필터, 뇌파 장비(시스템)"),
      (965, 350, 1195, 500, "recorded output $y(t)$: 기록된 출력"),
      (600, 308, 790, 342, "convolution →: 앞으로 가는 계산"),
      (600, 540, 800, 576, "← deconvolution: 거꾸로 되찾기"),
      (80, 632, 910, 670, "앞 방향은 컨볼루션, 되돌리기는 역컨볼루션(2장 용어)")),
  points("그림에서 볼 점",
      "입력(파란 선)은 잘게 떨리는데, 출력(주황 선)은 더 부드러워요.",
      "장비의 필터가 빠른 떨림을 걸러 냈기 때문이에요.",
      "이렇게 입력을 출력으로 바꾸는 규칙을 알면, 반대로 되돌리는 생각도 할 수 있어요."),
  bg("기초 다지기 b-10 손으로 하는 컨볼루션",
      K("conv") + "은 '손뼉마다 메아리 도장을 크기만큼 찍고, 겹친 도장을 모두 더하기'예요.",
      "자세한 계산은 3주차 2장에서 배워요."),
 ],
 "pass4": [
  warn("헷갈리기 쉬운 점",
      "상자 안의 $\\delta(t)$ 표기는 헷갈리기 쉬워요. 보통 시스템은 " + K("ir") + " $h(t)$로 나타내요. 여기서는 '어떤 응답을 가진 뇌파 장비' 정도로 읽어요.",
      "이 쪽의 컨볼루션, 역컨볼루션은 2장에서 쓸 용어를 미리 보여 주는 것이에요(슬라이드 표현: 2장 vocabulary)."),
  check("뇌파 기록 $y(t)$만 가지고 원래 신경 활동 $x(t)$를 추정하는 일은?", [K("conv"), K("deconv"), K("samp")], 1,
      "출력에서 입력으로 거꾸로 가는 것이 역컨볼루션이에요."),
  english("시험 답안에 쓸 문장",
      "입력 신호가 시스템을 거쳐 출력이 되는 계산을 컨볼루션, 출력에서 원래 입력을 되찾는 것을 역컨볼루션이라고 한다.",
      "앞으로는 컨볼루션, 거꾸로는 역컨볼루션.",
      "'앞 컨, 뒤 역컨'."),
 ]})

# ---------------------------------------------------------------------
# p.58 (슬라이드 56) RC 회로: 1차 선형 미분방정식
# ---------------------------------------------------------------------
_R, _Cc, _vs, _vc = 2.0, 0.5, 5.0, 3.0
_i = (_vs - _vc) / _R
_dv = _i / _Cc
assert _i == 1.0 and _dv == 2.0 and 1 / (_R * _Cc) == 1.0
assert _dv + (1 / (_R * _Cc)) * _vc == (1 / (_R * _Cc)) * _vs

S.append({"p": 58, "title": "시스템 예: RC 회로",
 "pass1": [
  say("1주차에 본 " + K("rc") + "도 " + K("sys") + "이에요.",
      "전원 전압이 입력, 축전기(C)에 걸리는 전압이 출력이에요.",
      "전원을 갑자기 켜도, 축전기 전압은 천천히 따라 올라가요."),
  figure("갑자기 켜도 천천히 따라와요", FIG_RC,
      "입력은 계단처럼 확 올라가지만, 출력은 곡선으로 천천히 올라가요."),
 ],
 "pass2": [
  formula("RC 회로의 식",
      r"i(t)=\frac{v_s(t)-v_c(t)}{R}=C\frac{dv_c(t)}{dt}\;\Rightarrow\;\frac{dv_c(t)}{dt}+\frac{1}{RC}v_c(t)=\frac{1}{RC}v_s(t)",
      [(r"v_s(t)", "전원(source) 전압: " + K("in")),
       (r"v_c(t)", "축전기(capacitor) 전압: " + K("out")),
       (r"\frac{v_s-v_c}{R}", "저항 R에 걸린 전압 ÷ R = 흐르는 전류"),
       (r"C\frac{dv_c}{dt}", "축전기로 들어가는 전류 = C x 전압이 변하는 빠르기"),
       (r"\frac{1}{RC}", "얼마나 빨리 따라오는지 정하는 수")],
      "출력의 변화 빠르기(" + K("deriv") + ")가 들어 있는 식, 곧 " + K("de") + "이에요."),
  points("first-order linear differential equation 풀어 읽기",
      "differential equation: " + K("de") + ", 미분이 들어 있는 식이에요.",
      "first-order: 미분이 한 번까지만 들어 있어요. " + K("order", "이") + " 1이에요.",
      "linear: 선형. 출력과 그 미분이 1제곱으로만, 더하기로만 들어 있어요."),
  check("RC 회로 식에서 가장 깊은 미분은 $dv_c/dt$ 한 번이에요. 이 식의 차수는?", ["0차", "1차", "2차"], 1,
      "미분이 한 번까지만 들어 있으니 1차(first-order) 미분방정식이에요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (110, 148, 975, 195, "1주차 친구: 전원 전압을 넣으면 축전기 전압이 나와요."),
      (268, 248, 675, 332, "전류 두 가지 표현: 저항 쪽 $(v_s-v_c)/R$ = 축전기 쪽 $C\\,dv_c/dt$"),
      (730, 248, 1125, 332, "정리한 식: $dv_c/dt+(1/RC)v_c=(1/RC)v_s$"),
      (668, 340, 1222, 388, "1차 선형 미분방정식(first-order linear differential equation)"),
      (525, 438, 805, 665, "회로: 전원 $v_s(t)$, 저항 R, 축전기 C, 전류 $i(t)$")),
  steps("쉬운 숫자로 한 순간 계산",
      ["$R=2$, $C=0.5$, 지금 $v_s=5$, $v_c=3$이라고 해요.",
       "전류: $i=(5-3)\\div 2=1$.",
       "축전기 전압이 오르는 빠르기: $dv_c/dt=i\\div C=1\\div 0.5=2$.",
       "$1/RC=1/(2\\times 0.5)=1$이에요.",
       "식 확인: $2+1\\times 3=5=1\\times 5$. 양쪽이 같아요."],
      "지금 이 순간 $v_c$는 1초에 2씩 오르는 빠르기예요.",
      given="$v_c$가 $v_s$보다 작으면 전류가 흘러 $v_c$가 올라가요"),
  prof("전원이 0에서 갑자기 툭 켜지면, 축전기 전압은 바로 따라오지 않고 천천히 따라온다고 하셨어요.",
      "따라오는 정도를 R(과 C)이 정하고, 미분방정식을 풀면 그 수식을 구할 수 있다고 하셨어요.",
      "RC 회로도 입력이 주어지면 출력이 나오는 하나의 시스템이라고 하셨어요."),
  prof("다음 주 복습에서, 1차 미분방정식 푸는 법은 알아 두면 되고 퀴즈나 시험에는 내지 않는다고 하셨어요.",
      when="3주차 목요일 수업"),
 ],
 "pass4": [
  check("RC 회로를 시스템으로 볼 때 입력과 출력은?",
      ["입력 축전기 전압, 출력 전원 전압", "입력 전원 전압, 출력 축전기 전압", "입력 전류, 출력 저항"], 1,
      "슬라이드 첫 줄: source voltage in, capacitor voltage out."),
  warn("헷갈리기 쉬운 점",
      "C는 두 가지로 쓰여요. 회로의 축전기 이름 C, 그리고 축전기 용량 값 C예요. 앞 절의 복소수 $C$와는 상관없어요.",
      "식을 푸는 방법(적분 인자)은 시험에 안 나온다고 하셨어요. 입력, 출력, 1차라는 것에 집중해요."),
  english("시험 답안에 쓸 문장",
      "RC 회로는 전원 전압 $v_s(t)$를 입력, 축전기 전압 $v_c(t)$를 출력으로 하는 연속시간 시스템이며 1차 선형 미분방정식으로 표현된다.",
      "입력 $v_s$, 출력 $v_c$, 1차 미분방정식.",
      "'RC는 1차 미방'."),
 ]})

# ---------------------------------------------------------------------
# p.59 (슬라이드 57) 자동차: 같은 모양의 식
# ---------------------------------------------------------------------
_m, _rho, _f, _vv = 1000.0, 50.0, 500.0, 5.0
_acc2 = (_f - _rho * _vv) / _m
assert _acc2 == 0.25 and _rho / _m == 0.05 and 1 / _m == 0.001
assert abs(_acc2 + (_rho / _m) * _vv - _f / _m) < 1e-12

S.append({"p": 59, "title": "시스템 예: 자동차도 RC 회로와 같은 식",
 "pass1": [
  say("자동차도 " + K("sys") + "이에요. 엔진 힘이 입력, 속도가 출력이에요.",
      "앞으로는 엔진이 밀고, 뒤로는 마찰이 잡아당겨요.",
      "놀랍게도 이 식은 " + K("rc") + "와 모양이 똑같아요."),
  figure("엔진 힘과 마찰", FIG_CAR,
      "엔진 힘 f(t)가 들어가면 속도 v(t)가 나오는 상자예요."),
 ],
 "pass2": [
  formula("자동차의 식",
      r"\frac{dv(t)}{dt}=\frac{1}{m}\left[f(t)-\rho v(t)\right]\;\Rightarrow\;\frac{dv(t)}{dt}+\frac{\rho}{m}v(t)=\frac{1}{m}f(t)",
      [(r"v(t)", "속도: " + K("out")),
       (r"f(t)", "엔진 힘: " + K("in")),
       (r"\rho v(t)", "마찰: 빠를수록 커져요. $\\rho$는 '로'라고 읽어요"),
       (r"m", "자동차 질량"),
       (r"\frac{dv}{dt}", "속도가 변하는 빠르기(가속도)")],
      "알짜 힘 ÷ 질량 = 속도 변화. 이것도 1차 선형 " + K("de") + "이에요."),
  compare("RC 회로와 자동차는 같은 모양", ["", K("rc"), "자동차"],
      ["출력", "$v_c(t)$", "$v(t)$"],
      ["입력", "$v_s(t)$", "$f(t)$"],
      ["왼쪽 계수", "$1/RC$", "$\\rho/m$"],
      ["오른쪽 계수", "$1/RC$", "$1/m$"]),
  check("자동차 시스템의 입력은?", ["속도 $v(t)$", "엔진 힘 $f(t)$", "질량 $m$"], 1,
      "엔진 힘을 넣으면 속도가 나와요. 질량은 상자 안의 고정된 값이에요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (315, 172, 765, 290, "자동차 그림: 앞으로 힘 f, 뒤로 마찰 $\\rho v$"),
      (395, 292, 1008, 432, "힘 그림: 질량 m, 속도 $v(t)$, 마찰 $\\rho v(t)$, 엔진 힘 $f(t)$"),
      (340, 478, 700, 568, "뉴턴 법칙: 속도 변화 = (엔진 힘 - 마찰) ÷ 질량"),
      (730, 478, 1060, 568, "정리하면 RC 회로와 같은 모양의 식"),
      (85, 605, 1150, 652, "자동차와 RC 회로가 같은 식을 따른다: 이것이 시스템으로 보는 힘이에요.")),
  steps("쉬운 숫자로 가속도 계산",
      ["$m=1000$, $\\rho=50$, 엔진 힘 $f=500$, 지금 속도 $v=5$라고 해요.",
       "마찰: $\\rho v=50\\times 5=250$.",
       "알짜 힘: $500-250=250$.",
       "속도 변화 빠르기: $250\\div 1000=0.25$.",
       "식 확인: $0.25+0.05\\times 5=0.5=500\\div 1000$."],
      "지금 속도는 1초에 0.25씩 빨라지는 중이에요."),
  prof("마찰 계수에 속력이 곱해져 마찰력이 생기고, 앞으로는 엔진에 의한 힘이 생긴다고 하셨어요.",
      "RC 회로 식과 똑같이 1차 미분방정식이고, 웬만한 물리 시스템은 1차 미분방정식을 따른다고 하셨어요.",
      "2차 시스템(예: RLC 회로)도 나중에 중요하게 다룬다고 하셨어요."),
 ],
 "pass4": [
  check("자동차 식과 RC 회로 식이 같은 모양이라는 것이 주는 교훈은?",
      ["자동차는 전기로 움직인다", "겉모습이 달라도 같은 시스템 식으로 분석할 수 있다", "마찰은 없어도 된다"], 1,
      "슬라이드: that is the power of the system view. 시스템으로 보면 하나의 방법으로 여러 문제를 풀어요."),
  warn("헷갈리기 쉬운 점",
      "$\\rho$(로)는 여기서 마찰 계수예요. 밀도가 아니에요.",
      "오른쪽 계수는 RC 회로는 $1/RC$, 자동차는 $1/m$으로 달라요. '모양'이 같다는 뜻이에요."),
  english("시험 답안에 쓸 문장",
      "자동차의 속도 $v(t)$와 엔진 힘 $f(t)$의 관계는 $dv/dt+(\\rho/m)v=(1/m)f$로, RC 회로와 같은 1차 선형 미분방정식이다.",
      "다른 물리 현상도 같은 시스템 식으로 묶여요.",
      "'차도 RC도 1차'."),
 ]})

# ---------------------------------------------------------------------
# p.60 (슬라이드 58) 통장 잔고: 1차 선형 차분방정식
# ---------------------------------------------------------------------
_y = 0.0
_ys = []
for _xn in (100, 100, 100):
    _y = _xn + 1.01 * _y
    _ys.append(round(_y, 4))
assert _ys == [100.0, 201.0, 303.01]
_y = 1000.0
_ys2 = []
for _xn in (0, 0, 0):
    _y = _xn + 1.01 * _y
    _ys2.append(round(_y, 4))
assert _ys2 == [1010.0, 1020.1, 1030.301]
_y = 0.0
_ys3 = []
for _xn in (200, 0, 100):
    _y = _xn + 1.01 * _y
    _ys3.append(round(_y, 4))
assert _ys3 == [200.0, 202.0, 304.02]
assert [round(v, 2) for v in _bal] == [100.0, 201.0, 303.01, 406.04]

S.append({"p": 60, "title": "시스템 예: 통장 잔고, 1차 차분방정식",
 "pass1": [
  analogy("통장 잔고",
      "이번 달 잔고는 지난달 잔고에 이자 1%를 붙이고, 이번 달에 넣은 돈을 더한 거예요. 통장은 지난 입금을 모두 기억하고 있어요.",
      ("이번 달에 넣은 돈", K("in") + " $x[n]$"),
      ("이번 달 잔고", K("out") + " $y[n]$"),
      ("지난달 잔고를 기억해 쓰는 것", K("memory"))),
  figure("매달 100만 원씩 넣으면", FIG_BANK,
      "지난달 잔고에 이자가 붙고 새 입금이 더해져 잔고가 쌓여요."),
 ],
 "pass2": [
  formula("통장 잔고의 식",
      r"y[n]=x[n]+1.01\,y[n-1]",
      [(r"y[n]", "n번째 달의 잔고: " + K("out")),
       (r"x[n]", "n번째 달에 넣은 돈(입금 - 출금): " + K("in")),
       (r"y[n-1]", "지난달 잔고: 한 칸 전의 출력"),
       (r"1.01", "이자 1%: 지난달 잔고의 1.01배")],
      "이번 달 잔고 = 이번 달 입금 + 지난달 잔고의 1.01배. 한 칸 전 값이 들어간 " + K("dfe") + "이에요."),
  compare("미분방정식과 차분방정식", ["", K("de"), K("dfe")],
      ["쓰는 곳", "연속시간 시스템 (RC 회로, 자동차)", "이산시간 시스템 (통장)"],
      ["들어 있는 것", "미분 $dy/dt$", "한 칸 전 값 $y[n-1]$"],
      ["1차라는 뜻", "미분이 한 번까지", "한 칸 전까지만"]),
  check("$y[n]=x[n]+1.01y[n-1]$에서 $y[n-1]$은 무엇일까요?", ["다음 달 잔고", "지난달 잔고", "이번 달 입금"], 1,
      "n-1은 한 칸(한 달) 전이에요. 지난달 잔고를 기억해서 써요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (110, 148, 975, 195, "매달 잔고 $y[n]$, 매달 순입금 $x[n]$, 이자 1%"),
      (410, 252, 990, 318, "$y[n]=x[n]+1.01\\,y[n-1]$"),
      (110, 362, 565, 405, "1차 선형 차분방정식(first-order linear difference equation)")),
  steps("3달 동안 잔고 계산 (단위: 만 원)",
      ["처음 잔고 $y[-1]=0$, 매달 $x[n]=100$을 넣어요.",
       "$n=0$: $y[0]=100+1.01\\times 0=100$.",
       "$n=1$: $y[1]=100+1.01\\times 100=100+101=201$.",
       "$n=2$: $y[2]=100+1.01\\times 201=100+203.01=303.01$."],
      "$100\\to 201\\to 303.01$ (만 원)"),
  steps("입금 없이 이자만 붙으면",
      ["처음 잔고 $y[-1]=1000$, 입금 $x[n]=0$.",
       "$y[0]=1.01\\times 1000=1010$.",
       "$y[1]=1.01\\times 1010=1020.1$.",
       "$y[2]=1.01\\times 1020.1=1030.301$."],
      "입금이 없어도 지난달 값을 기억해서 계속 불어나요."),
  prof("이 예는 1주차에 봤던 것이고, 지난달 통장 잔고에 1% 복리를 붙이고 이번 달 입금을 더하는 것도 하나의 시스템이라고 하셨어요."),
  prof("시스템 성질에서, 출력을 내는 데 과거 값이 필요하면 메모리(" + K("memory") + ")가 있는 시스템이라고 하셨어요.",
      when="2주차 목요일 수업 (1.6 시스템의 성질)"),
 ],
 "pass4": [
  exam("연습 문제 (p.60 통장 차분방정식)",
      "With $y[-1]=0$ and $x[0]=200$, $x[1]=0$, $x[2]=100$, find $y[2]$ for $y[n]=x[n]+1.01y[n-1]$.",
      "처음 잔고 0, 입금이 200, 0, 100(만 원)일 때 $y[2]$를 구하세요.",
      ["$y[0]=200+1.01\\times 0=200$.",
       "$y[1]=0+1.01\\times 200=202$.",
       "$y[2]=100+1.01\\times 202=100+204.02=304.02$."],
      "$y[2]=304.02$ (만 원)"),
  warn("헷갈리기 쉬운 점",
      "$x[n]$은 '순' 입금이에요(입금 - 출금). 돈을 빼면 음수예요.",
      "이자가 붙는 것은 지난달 잔고 $y[n-1]$이에요. 이번 달 입금 $x[n]$에는 이번 달 이자가 붙지 않아요.",
      "$y[n]$ 계산에 $y[n-1]$이 필요하니 처음 값($y[-1]$)을 꼭 정해야 해요."),
  english("시험 답안에 쓸 문장",
      "통장 잔고 $y[n]=x[n]+1.01y[n-1]$은 입력 $x[n]$, 출력 $y[n]$인 이산시간 시스템이며 1차 선형 차분방정식으로 표현된다.",
      "연속시간의 미분방정식 자리에 이산시간은 차분방정식.",
      "'통장은 1차 차방'."),
 ]})


# =====================================================================
# 저장
# =====================================================================
BAD = [chr(0x2014), chr(0x2013), chr(0xB7), chr(0x30FB)]


def _text(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, list):
        for x in o:
            yield from _text(x)
    elif isinstance(o, dict):
        for k, v in o.items():
            if k != "svg":
                yield from _text(v)


def build():
    gl_keys = []
    for s in S:
        body = " ".join(_text([s.get(f"pass{i}", []) for i in range(1, 5)]))
        terms = []
        for key in TERMS:
            if disp(key) in body:
                terms.append(TERMS[key][1])
                if key not in gl_keys:
                    gl_keys.append(key)
        s["terms"] = terms
    out = {"deck": "S2", "from": 31, "to": 60,
           "glossary": [gloss_entry(k) for k in gl_keys],
           "slides": [{"p": s["p"], "title": s["title"], "terms": s["terms"],
                       **{f"pass{i}": s.get(f"pass{i}", []) for i in range(1, 5)}} for s in S]}
    raw = json.dumps(out, ensure_ascii=False, indent=1)
    for ch in BAD:
        if ch in raw:
            i = raw.index(ch)
            raise ValueError(f"금지 문자 {ch!r}: {raw[max(0, i - 60):i + 10]}")
    ps = [s["p"] for s in S]
    assert ps == list(range(31, 61)), ps
    with open(OUT, "w", encoding="utf-8") as fp:
        fp.write(raw)
    print(f"저장 {OUT}: 쪽 {len(S)}, 용어 {len(gl_keys)}")


if __name__ == "__main__":
    build()
