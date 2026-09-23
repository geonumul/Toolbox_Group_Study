# -*- coding: utf-8 -*-
# 신호및시스템 2주차(S2) 회독 레슨 1~30쪽 생성기. 사용: python build_S2_001-030.py
import json, math, cmath, os, re
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "S2_001-030.json")
DICT = json.load(open(os.path.join(HERE, "..", "rules", "용어사전.json"), encoding="utf-8"))
MANTRA = "신호는 시간에 따라 변하는 값, 시스템은 신호를 바꾸는 상자."
WHEN = "2주차 목요일 수업"

TERMS = {
    "sig": ("신호", "Signal"), "sys": ("시스템", "System"), "iv": ("독립 변수", "Independent Variable"),
    "ct": ("연속시간 신호", "Continuous-Time Signal"), "dt": ("이산시간 신호", "Discrete-Time Signal"),
    "samp": ("샘플링", "Sampling"), "energy": ("신호 에너지", "Signal Energy"),
    "avgp": ("평균 전력", "Average Power"), "instp": ("순간 전력", "Instantaneous Power"),
    "shift": ("시간 이동", "Time Shift"), "delay": ("지연", "Delay"), "adv": ("앞당김", "Advance"),
    "rev": ("시간 반전", "Time Reversal"), "scale": ("시간 척도 변환", "Time Scaling"),
    "periodic": ("주기 신호", "Periodic Signal"), "fund": ("기본 주기", "Fundamental Period"),
    "aper": ("비주기 신호", "Aperiodic Signal"), "even": ("짝수 신호", "Even Signal"),
    "odd": ("홀수 신호", "Odd Signal"), "eod": ("짝홀 분해", "Even-Odd Decomposition"),
    "cplx": ("복소수", "Complex Number"), "imag": ("허수 단위", "Imaginary Unit"),
    "cplane": ("복소평면", "Complex Plane"), "phase": ("위상", "Phase"), "ucirc": ("단위원", "Unit Circle"),
    "euler": ("오일러 공식", "Euler's Formula"), "taylor": ("테일러 급수", "Taylor Series"),
    "expf": ("지수함수", "Exponential Function"), "realexp": ("실수 지수 신호", "Real Exponential Signal"),
    "cexp": ("복소 지수 신호", "Complex Exponential Signal"), "sinus": ("사인파 신호", "Sinusoidal Signal"),
    "amp": ("진폭", "Amplitude"), "angf": ("각주파수", "Angular Frequency"), "freq": ("주파수", "Frequency"),
    "rad": ("라디안", "Radian"), "rc": ("RC 회로", "RC Circuit"), "imp": ("단위 임펄스", "Unit Impulse"),
    "sigma": ("시그마 기호", "Summation"), "integ": ("적분", "Integral"),
}
JOSA = {"은": ("은", "는"), "이": ("이", "가"), "을": ("을", "를"), "과": ("과", "와"),
        "이라고": ("이라고", "라고"), "이에요": ("이에요", "예요"), "이고": ("이고", "고"),
        "이나": ("이나", "나"), "이죠": ("이죠", "죠"), "이라는": ("이라는", "라는"), "이면": ("이면", "면")}


def _fin(key):
    c = TERMS[key][0][-1]
    j = (ord(c) - 0xAC00) % 28
    return 0 if j == 0 else (2 if j == 8 else 1)


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
    raise KeyError(key)


# ---------------- 장면 ----------------
PW, PH = 1400, 788  # 작성용 PNG 크기(PDF 960x540 과 같은 비율)


def say(*lines):
    return {"kind": "say", "lines": list(lines)}


def look(head, *boxes):
    out = []
    for x1, y1, x2, y2, s in boxes:
        out.append({"x": round(x1 / PW, 3), "y": round(y1 / PH, 3), "w": round((x2 - x1) / PW, 3),
                    "h": round((y2 - y1) / PH, 3), "say": s})
    return {"kind": "look", "head": head, "boxes": out}


def points(head, *items):
    return {"kind": "points", "head": head, "items": list(items)}


def analogy(head, scene, *pairs):
    return {"kind": "analogy", "head": head, "scene": scene, "map": [list(p) for p in pairs]}


def compare(head, cols, *rows):
    return {"kind": "compare", "head": head, "cols": list(cols), "rows": [list(r) for r in rows]}


def steps(head, stps, answer, given=None):
    d = {"kind": "steps", "head": head}
    if given:
        d["given"] = given
    d["steps"] = list(stps)
    d["answer"] = answer
    return d


def formula(head, tex, parts, whole):
    return {"kind": "formula", "head": head, "tex": tex,
            "parts": [{"sym": s, "say": w} for s, w in parts], "whole": whole}


def figure(head, svg, caption, builds):
    return {"kind": "figure", "head": head, "svg": svg, "caption": caption, "builds": builds}


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


def prof(*lines):
    return {"kind": "prof", "when": WHEN, "lines": list(lines)}


def recap(*items):
    return {"kind": "recap", "items": list(items)}


# ---------------- SVG ----------------
def _b(b):
    return f" b{b}" if b else ""


def TX(x, y, s, cls="t", fs=15, anc="middle", b=0):
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f'<text x="{x}" y="{y}" font-size="{fs}" text-anchor="{anc}" class="{cls}{_b(b)}">{s}</text>'


def R(x, y, w, h, cls="box", b=0, rx=2):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" class="{cls}{_b(b)}"/>'


def C(x, y, r, cls="n", b=0):
    return f'<circle cx="{x}" cy="{y}" r="{r}" class="{cls}{_b(b)}"/>'


def L(x1, y1, x2, y2, cls="e", b=0):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{cls}{_b(b)}"/>'


def PL(pts, cls="e2", b=0):
    s = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polyline points="{s}" fill="none" class="{cls}{_b(b)}"/>'


def A(x1, y1, x2, y2, cls="e2", b=0):
    ang = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 - 9 * math.cos(ang), y2 - 9 * math.sin(ang)
    px, py = -math.sin(ang) * 5, math.cos(ang) * 5
    pts = f"{x2:.0f},{y2:.0f} {hx + px:.0f},{hy + py:.0f} {hx - px:.0f},{hy - py:.0f}"
    return L(f"{x1:.0f}", f"{y1:.0f}", f"{hx:.0f}", f"{hy:.0f}", cls, b) + f'<polygon points="{pts}" class="arrow{_b(b)}"/>'


def SVG(*parts, h=270):
    return f'<svg viewBox="0 0 480 {h}" xmlns="http://www.w3.org/2000/svg">' + "".join(parts) + "</svg>"


class Ax:
    """수학 좌표 (x0..x1, y0..y1) 를 그림 좌표 (px0..px1, py0..py1) 로. py0 이 위쪽."""

    def __init__(s, px0, px1, py0, py1, x0, x1, y0, y1):
        s.px0, s.px1, s.py0, s.py1, s.x0, s.x1, s.y0, s.y1 = px0, px1, py0, py1, x0, x1, y0, y1

    def X(s, x):
        return round(s.px0 + (x - s.x0) / (s.x1 - s.x0) * (s.px1 - s.px0), 1)

    def Y(s, y):
        return round(s.py1 - (y - s.y0) / (s.y1 - s.y0) * (s.py1 - s.py0), 1)

    def axes(s, xl="t", b=0, yaxis=True):
        y = s.Y(0)
        out = A(s.px0, y, s.px1 + 8, y, "e", b) + TX(s.px1 + 4, y - 8, xl, "tm", 14, "middle", b)
        if yaxis and s.x0 <= 0 <= s.x1:
            out += L(s.X(0), s.py0, s.X(0), s.py1 + 4, "e", b)
        return out

    def tick(s, x, lab, b=0, dy=18):
        X, y = s.X(x), s.Y(0)
        return L(X, y - 3, X, y + 3, "e", b) + TX(X, y + dy, lab, "tm", 14, "middle", b)

    def curve(s, f, a, bb, cls="e2", b=0, n=160):
        return PL([(s.X(a + (bb - a) * i / n), s.Y(f(a + (bb - a) * i / n))) for i in range(n + 1)], cls, b)

    def poly(s, pts, cls="e2", b=0):
        return PL([(s.X(x), s.Y(y)) for x, y in pts], cls, b)

    def stem(s, n, v, b=0, cls="e2", dot="n2"):
        return L(s.X(n), s.Y(0), s.X(n), s.Y(v), cls, b) + C(s.X(n), s.Y(v), 4, dot, b)


# =====================================================================
# 손계산 확인 (모든 답을 여기서 계산하고 assert)
# =====================================================================
PI = math.pi
# p.4 샘플링: x(t) = 10 - t, 1초마다
assert [10 - n for n in range(4)] == [10, 9, 8, 7]
# p.5 v=2, R=1, [0,3]
v, Rr = 2, 1
assert v * v / Rr == 4 and 4 * 3 == 12 and 12 / (3 - 0) == 4
# p.6 이산시간 x[0..2] = 1,2,1
xd = [1, 2, 1]
assert sum(a * a for a in xd) == 6 and (2 - 0 + 1) == 3 and Fr(6, 3) == 2
assert (4 - 2 + 1) == 3  # 2,3,4 는 세 칸
assert sum(a * a for a in [1, -2, 1]) == 6 and (-2) ** 2 == 4


def pulseE(T):  # p.7 펄스 x(t)=2 (0<=t<=3) 의 -T~T 에너지
    return 4 * max(0, min(T, 3) - 0)


assert [pulseE(1), pulseE(2), pulseE(3), pulseE(10)] == [4, 8, 12, 12]
assert (2 * 1 + 1) * 16 == 48 and (2 * 10 + 1) * 16 == 336
# p.8 평균 전력
assert [round(12 / (2 * T), 3) for T in (10, 100, 1000)] == [0.6, 0.06, 0.006]
assert all((2 * N + 1) * 16 / (2 * N + 1) == 16 for N in (1, 10, 100))


def corners(a, b, pts=(0, 1, 2)):
    """y(t) = x(a t + b): x 의 모서리 s 는 t = (s - b)/a 로 간다"""
    return [Fr(s - b) / Fr(a) for s in pts]


assert corners(1, 1) == [-1, 0, 1]
assert corners(1, -1) == [1, 2, 3]
assert corners(2, 0) == [0, Fr(1, 2), 1]
assert corners(-1, 1) == [1, 0, -1]
assert corners(-1, 0) == [0, -1, -2]
assert corners(Fr(3, 2), 0) == [0, Fr(2, 3), Fr(4, 3)]
assert corners(Fr(3, 2), 1) == [Fr(-2, 3), 0, Fr(2, 3)]
assert corners(-2, 2) == [1, Fr(1, 2), 0]
assert [c - 1 for c in corners(Fr(3, 2), 0)] == [-1, Fr(-1, 3), Fr(1, 3)]  # 틀린 방법
assert [c / Fr(3, 2) for c in corners(1, 1)] == [Fr(-2, 3), 0, Fr(2, 3)]  # 먼저 옮기고 나누기
# p.10~12 직사각 [-1,3]
assert corners(1, -4, (-1, 3)) == [3, 7] and corners(1, 2, (-1, 3)) == [-3, 1] and corners(1, -5, (-1, 3)) == [4, 8]
assert corners(-1, 0, (-1, 3)) == [1, -3] and corners(-1, 0, (2, 5)) == [-2, -5]
assert corners(3, 0, (-1, 3)) == [Fr(-1, 3), 1] and 1 - Fr(-1, 3) == Fr(4, 3)
assert corners(Fr(2, 5), 0, (-1, 3)) == [Fr(-5, 2), Fr(15, 2)] and Fr(15, 2) - Fr(-5, 2) == 10
assert corners(2, 0, (-1, 3)) == [Fr(-1, 2), Fr(3, 2)]


def tri(m):  # p.14 삼각형 x[n] = 1 - |n|/3 (|n|<=3), 그림에서 읽은 값
    return Fr(3 - abs(m), 3) if abs(m) <= 3 else Fr(0)


assert {n: tri(3 * n + 6) for n in range(-4, 1)} == {-4: 0, -3: 0, -2: 1, -1: 0, 0: 0}
assert {n: tri(2 * n) for n in (-2, -1, 0, 1, 2)} == {-2: 0, -1: Fr(1, 3), 0: 1, 1: Fr(1, 3), 2: 0}
assert {n: tri(n + 6) for n in (-9, -8, -7, -6, -5, -4, -3)} == {-9: 0, -8: Fr(1, 3), -7: Fr(2, 3), -6: 1, -5: Fr(2, 3), -4: Fr(1, 3), -3: 0}
# p.15, 18 sin
assert abs(math.sin(1) - math.sin(1 + 2 * PI)) < 1e-12
assert abs(math.sin(PI / 2 + PI) - (-1)) < 1e-12
assert [round(math.sin(k * PI / 2), 9) + 0.0 for k in range(5)] == [0, 1, 0, -1, 0]
# p.17 cos(pi n / 4)
assert [round(math.cos(PI * n / 4), 2) + 0.0 for n in range(9)] == [1, 0.71, 0, -0.71, -1, -0.71, 0, 0.71, 1]
# p.19
assert math.cos(-1) == math.cos(1) and math.sin(-1) == -math.sin(1)
assert round(math.cos(1), 2) == 0.54 and round(math.sin(1), 2) == 0.84
# p.20 짝홀 분해: 내 예 x[n] = 1 (n>=0), 0 (n<0)
xs = {n: (1 if n >= 0 else 0) for n in range(-3, 4)}
xe = {n: Fr(xs[n] + xs[-n], 2) for n in xs}
xo = {n: Fr(xs[n] - xs[-n], 2) for n in xs}
assert xe[0] == 1 and xe[2] == Fr(1, 2) and xe[-2] == Fr(1, 2)
assert xo[0] == 0 and xo[2] == Fr(1, 2) and xo[-2] == Fr(-1, 2)
assert all(xe[n] + xo[n] == xs[n] for n in xs)
xsl = {n: (0 if n == 0 else (1 if n > 0 else -1)) for n in range(-3, 4)}  # 슬라이드의 x[n]
assert all(Fr(xsl[n] + xsl[-n], 2) == 0 and Fr(xsl[n] - xsl[-n], 2) == xsl[n] for n in xsl)
assert Fr(4 + 0, 2) == 2 and Fr(4 - 0, 2) == 2 and Fr(0 + 4, 2) == 2 and Fr(0 - 4, 2) == -2 and Fr(2 + 2, 2) == 2
# p.22
assert [round(math.exp(0.2 * t), 2) for t in (-10, 0, 10)] == [0.14, 1.0, 7.39]
assert round(math.exp(-0.2 * 10), 2) == 0.14
# p.23 w0=2 -> T = pi
assert abs(cmath.exp(2j * (0.7 + PI)) - cmath.exp(2j * 0.7)) < 1e-12
assert abs(cmath.exp(1j * PI) + 1) < 1e-12
# p.24 테일러
assert round(sum(1 / math.factorial(k) for k in range(5)), 3) == 2.708 and round(math.e, 3) == 2.718
assert round(1 - 0.5 ** 2 / 2 + 0.5 ** 4 / 24, 4) == 0.8776 and round(math.cos(0.5), 4) == 0.8776
assert (1j) ** 2 == -1 and (1j) ** 4 == 1
# p.25 오일러 값
E = lambda th: cmath.exp(1j * th)
assert abs(E(0) - 1) < 1e-12 and abs(E(PI / 2) - 1j) < 1e-12 and abs(E(PI) + 1) < 1e-12
assert abs(E(3 * PI / 2) + 1j) < 1e-12 and abs(E(-PI / 2) + 1j) < 1e-12 and abs(E(2 * PI) - 1) < 1e-12
assert round(E(PI / 4).real, 3) == 0.707 and round(E(PI / 4).imag, 3) == 0.707
w0 = 4 * PI
assert abs(2 * PI / w0 - 0.5) < 1e-12 and abs(w0 / (2 * PI) - 2) < 1e-12
# p.26 |e^{jw}| = 1
assert abs(math.cos(PI / 3) ** 2 + math.sin(PI / 3) ** 2 - 1) < 1e-12
assert round(math.cos(PI / 3) ** 2, 2) == 0.25 and round(math.sin(PI / 3) ** 2, 2) == 0.75
# p.27 cos(2t+1)
assert abs(2 * PI / 2 - PI) < 1e-12 and round(math.cos(1), 2) == 0.54
assert abs((3 * E(PI / 2)).real) < 1e-12 and abs((3 * E(PI / 2)).imag - 3) < 1e-12
# p.28 A=2, phi=pi/3
assert abs(2 * math.cos(PI / 3) - 1) < 1e-12 and abs(2 * PI / PI - 2) < 1e-12
# p.29 T=0.5 -> f=2, w=4pi ; y = 3 sin(2(x+1)) + 1 -> 주기 pi
assert 1 / 0.5 == 2 and abs(2 * PI * 2 - 4 * PI) < 1e-12 and abs(2 * PI / 2 - PI) < 1e-12
# p.30 w = 4, 2, 1
assert [round(2 * PI / w, 2) for w in (4, 2, 1)] == [1.57, 3.14, 6.28]


# =====================================================================
# 그림 (좌표는 Ax 로 계산)
# =====================================================================
def _ctdt():
    a1 = Ax(30, 210, 50, 215, 0, 10, 0, 1.2)
    a2 = Ax(265, 445, 50, 215, 0, 10, 0, 1.2)
    f = lambda t: 0.35 + 0.65 * math.exp(-0.35 * t) + 0.06 * math.sin(0.9 * t)
    out = [a1.axes("t"), TX(120, 28, "연속시간: 끊김 없는 선", "tb", 15), a1.curve(f, 0, 10),
           TX(120, 255, "x(t), 둥근 괄호", "tm", 14)]
    out += [a2.axes("n", 1), TX(355, 28, "이산시간: 띄엄띄엄 점", "tb", 15, "middle", 1)]
    out += [a2.stem(n, f(n), 1) for n in range(11)]
    out += [TX(355, 255, "x[n], 대괄호", "tm", 14, "middle", 1)]
    return SVG(*out)


FIG_CTDT = _ctdt()


def _energy():
    a1 = Ax(40, 205, 60, 205, -1, 4, 0, 4.6)
    a2 = Ax(280, 445, 60, 205, -1, 4, 0, 4.6)
    out = [a1.axes("t"), a1.poly([(-1, 0), (0, 0), (0, 2), (3, 2), (3, 0), (4, 0)]),
           a1.tick(3, "3"), TX(a1.X(0) - 6, a1.Y(2) + 5, "2", "tm", 14, "end"),
           TX(120, 35, "x(t) = 2 (0에서 3까지)", "tb", 15)]
    out += [R(a2.X(0), a2.Y(4), round(a2.X(3) - a2.X(0), 1), round(a2.Y(0) - a2.Y(4), 1), "n3", 1, 0),
            a2.axes("t", 1), a2.tick(3, "3", 1), TX(a2.X(0) - 6, a2.Y(4) + 5, "4", "tm", 14, "end", 1),
            TX(360, 35, "|x(t)|² = 4", "tb", 15, "middle", 1),
            TX(a2.X(1.5), a2.Y(2) + 5, "넓이 12", "tl", 16, "middle", 2),
            TX(240, 258, "에너지 = 4 × 3 = 12", "tb", 16, "middle", 2)]
    return SVG(*out)


FIG_ENERGY = _energy()


def _two():
    a1 = Ax(30, 205, 70, 200, -3, 6, 0, 5)
    a2 = Ax(270, 445, 70, 200, -3, 6, 0, 5)
    out = [a1.axes("t"), a1.poly([(-3, 0), (0, 0), (0, 2), (3, 2), (3, 0), (6, 0)]),
           TX(120, 40, "잠깐 켜졌다 꺼짐", "tb", 15), TX(120, 245, "에너지 유한, 전력 0", "tm", 14)]
    out += [a2.axes("n", 1)] + [a2.stem(n, 4, 1) for n in range(-3, 7)]
    out += [TX(360, 40, "늘 4인 신호", "tb", 15, "middle", 1), TX(360, 245, "전력 16, 에너지 무한", "tm", 14, "middle", 1)]
    return SVG(*out)


FIG_TWO = _two()


def _rect_rows(rows, h=270, x0=-5, x1=9):
    """rows: [(라벨, 왼쪽 끝, 오른쪽 끝, 눈금, 빌드)]. 높이 2 인 직사각 신호"""
    band = (h - 10) / len(rows)
    out = []
    for i, (lab, l, r, ticks, b) in enumerate(rows):
        top = 5 + band * i
        ax = Ax(95, 445, top + 14, top + band - 26, x0, x1, 0, 2.4)
        out += [TX(10, round(top + band / 2, 1), lab, "tb", 15, "start", b), ax.axes("t", b),
                ax.poly([(x0, 0), (l, 0), (l, 2), (r, 2), (r, 0), (x1, 0)], "e2", b)]
        out += [ax.tick(v, s, b) for v, s in ticks]
    return SVG(*out, h=h)


FIG_SHIFT = _rect_rows([("x(t)", -1, 3, [(-1, "-1"), (3, "3")], 0),
                        ("x(t-4)", 3, 7, [(3, "3"), (7, "7")], 1),
                        ("x(t+2)", -3, 1, [(-3, "-3"), (1, "1")], 2)], h=300)
FIG_REV = _rect_rows([("x(t)", -1, 3, [(-1, "-1"), (3, "3")], 0),
                      ("x(-t)", -3, 1, [(-3, "-3"), (1, "1")], 1)], x0=-5, x1=5)
FIG_SCALE = _rect_rows([("x(t)", -1, 3, [(-1, "-1"), (3, "3")], 0),
                        ("x(3t)", -1 / 3, 1, [(-1 / 3, "-1/3"), (1, "1")], 1),
                        ("x(t/2.5)", -2.5, 7.5, [(-2.5, "-2.5"), (7.5, "7.5")], 2)], h=300, x0=-4, x1=9)


def _trap_rows(rows, h=300):
    """rows: [(라벨, a, b, 눈금, 빌드)]. x(t): 0에서 1로 뛰고 1까지 1, 2에서 0 인 사다리꼴의 x(at+b)"""
    band = (h - 10) / len(rows)
    out = []
    for i, (lab, a, bb, ticks, b) in enumerate(rows):
        top = 5 + band * i
        ax = Ax(125, 445, top + 14, top + band - 26, -2.5, 2.8, 0, 1.3)
        c0, c1, c2 = [float(c) for c in corners(a, bb)]
        pts = [(-2.5, 0.0), (c0, 0.0), (c0, 1.0), (c1, 1.0), (c2, 0.0), (2.8, 0.0)]
        if a < 0:
            pts = [(-2.5, 0.0), (c2, 0.0), (c1, 1.0), (c0, 1.0), (c0, 0.0), (2.8, 0.0)]
        out += [TX(10, round(top + band / 2, 1), lab, "tb", 15, "start", b), ax.axes("t", b), ax.poly(pts, "e2", b)]
        out += [ax.tick(v, s, b) for v, s in ticks]
    return SVG(*out, h=h)


FIG_TRAP9 = _trap_rows([("x(t)", 1, 0, [(0, "0"), (1, "1"), (2, "2")], 0),
                        ("x(t+1)", 1, 1, [(-1, "-1"), (1, "1")], 1),
                        ("x(2t)", 2, 0, [(0.5, "0.5"), (1, "1")], 2)])
FIG_FLIP = _trap_rows([("x(t)", 1, 0, [(0, "0"), (1, "1"), (2, "2")], 0),
                       ("x(-t)", -1, 0, [(-2, "-2"), (-1, "-1"), (0, "0")], 1),
                       ("x(-t+1)", -1, 1, [(-1, "-1"), (0, "0"), (1, "1")], 2)])
FIG_CS = _trap_rows([("x(t)", 1, 0, [(0, "0"), (1, "1"), (2, "2")], 0),
                     ("x(3t/2)", 1.5, 0, [(2 / 3, "2/3"), (4 / 3, "4/3")], 1),
                     ("x(3t/2+1)", 1.5, 1, [(-2 / 3, "-2/3"), (2 / 3, "2/3")], 2)])


def _dttri():
    a1 = Ax(25, 215, 50, 200, -5, 5, 0, 1.25)
    a2 = Ax(265, 455, 50, 200, -5, 5, 0, 1.25)
    out = [a1.axes("n"), TX(120, 28, "x[n] 삼각형", "tb", 15)]
    out += [a1.stem(n, float(tri(n))) for n in range(-5, 6)]
    out += [a1.tick(-3, "-3"), a1.tick(3, "3")]
    out += [a2.axes("n", 1), TX(360, 28, "y[n] = x[3n+6]", "tb", 15, "middle", 1)]
    out += [a2.stem(n, float(tri(3 * n + 6)), 1) for n in range(-5, 6)]
    out += [a2.tick(-2, "-2", 1), TX(360, 255, "n = -2 에서만 1", "tm", 14, "middle", 2),
            TX(120, 255, "점 5개가 1개로", "tm", 14, "middle", 2)]
    return SVG(*out)


FIG_DTTRI = _dttri()


def _sin():
    ax = Ax(40, 445, 60, 220, 0, 15, -1.3, 1.3)
    x1, x2 = ax.X(PI / 2), ax.X(5 * PI / 2)
    return SVG(ax.axes("t"), ax.curve(math.sin, 0, 15), ax.tick(5, "5", 0, 36), ax.tick(10, "10", 0, 36),
               TX(32, ax.Y(1) + 5, "1", "tm", 14, "end"), TX(32, ax.Y(-1) + 5, "-1", "tm", 14, "end"),
               A(x1, 42, x2, 42, "e2", 1), A(x2, 42, x1, 42, "e2", 1),
               TX(round((x1 + x2) / 2, 1), 30, "T = 2π 마다 반복", "tb", 15, "middle", 1),
               TX(360, 262, "x(t) = sin t", "tm", 14))


FIG_SIN = _sin()


def _aper():
    a1 = Ax(30, 445, 35, 110, 0, 10, -1.2, 1.2)
    a2 = Ax(30, 445, 170, 245, 0, 10, -1.2, 1.2)
    return SVG(TX(30, 22, "주기 신호: 같은 모양이 끝없이", "tb", 15, "start"), a1.axes("t", yaxis=False),
               a1.curve(lambda t: math.sin(2 * PI * t / 2.5), 0, 10),
               TX(30, 157, "비주기 신호: 점점 빨라져요", "tb", 15, "start", 1), a2.axes("t", 1, yaxis=False),
               a2.curve(lambda t: math.sin(2 * PI * (0.25 * t + 0.03 * t * t)), 0, 10, "e2", 1, 300))


FIG_APER = _aper()


def _dtper():
    ax = Ax(30, 445, 55, 215, -9, 9, -1.3, 1.3)
    out = [ax.axes("n")] + [ax.stem(n, math.cos(PI * n / 4)) for n in range(-9, 10)]
    out += [ax.tick(-8, "-8", 0, 36), ax.tick(8, "8", 0, 36),
            A(ax.X(0), 35, ax.X(8), 35, "e2", 1), A(ax.X(8), 35, ax.X(0), 35, "e2", 1),
            TX(ax.X(4), 25, "N₀ = 8칸", "tb", 15, "middle", 1)]
    return SVG(*out)


FIG_DTPER = _dtper()


def _evenodd():
    a1 = Ax(20, 215, 60, 200, -7, 7, -1.3, 1.3)
    a2 = Ax(265, 455, 60, 200, -7, 7, -1.3, 1.3)
    return SVG(TX(120, 30, "짝수: cos t", "tb", 15), a1.axes("t"), a1.curve(math.cos, -7, 7),
               C(a1.X(0), a1.Y(1), 6, "hl"), TX(120, 250, "왼쪽 = 오른쪽 (거울)", "tm", 14),
               TX(360, 30, "홀수: sin t", "tb", 15, "middle", 1), a2.axes("t", 1), a2.curve(math.sin, -7, 7, "e2", 1),
               C(a2.X(0), a2.Y(0), 6, "hl", 1), TX(360, 250, "t = 0 에서 꼭 0", "tm", 14, "middle", 1))


FIG_EVENODD = _evenodd()


def _eodec():
    out = []
    for i, (lab, d, b) in enumerate([("x[n]", xs, 0), ("짝수 부분", xe, 1), ("홀수 부분", xo, 2)]):
        ax = Ax(15 + 158 * i, 140 + 158 * i, 60, 220, -3.6, 3.6, -1.2, 1.2)
        out += [TX(78 + 158 * i, 30, lab, "tb", 15, "middle", b), ax.axes("n", b)]
        out += [ax.stem(n, float(d[n]), b) for n in range(-3, 4)]
        out += [TX(78 + 158 * i, 258, ["0, 1, 1", "1/2, 1, 1/2", "-1/2, 0, 1/2"][i], "tm", 14, "middle", b)]
    return SVG(*out)


FIG_EODEC = _eodec()


def _exp():
    a1 = Ax(30, 205, 50, 215, -10, 10, 0, 8)
    a2 = Ax(270, 445, 50, 215, -10, 10, 0, 8)
    return SVG(TX(120, 28, "a > 0: 커져요", "tb", 15), a1.axes("t"), a1.curve(lambda t: math.exp(0.2 * t), -10, 10),
               a1.tick(10, "10"), a1.tick(-10, "-10"),
               TX(360, 28, "a < 0: 줄어요", "tb", 15, "middle", 1), a2.axes("t", 1),
               a2.curve(lambda t: math.exp(-0.2 * t), -10, 10, "e2", 1), a2.tick(10, "10", 1), a2.tick(-10, "-10", 1),
               TX(240, 262, "둘 다 t = 0 에서 C = 1", "tm", 14, "middle", 2))


FIG_EXP = _exp()


def _uc(extra=True):
    cx, cy, r = 240, 140, 95
    out = [A(110, cy, 380, cy, "e"), A(cx, 262, cx, 18, "e"), TX(392, cy + 5, "실수", "tm", 14, "start"),
           TX(cx - 10, 26, "허수", "tm", 14, "end"), C(cx, cy, r, "hl")]
    for th, lab, dx, dy, anc in [(0, "1", 12, 22, "start"), (PI / 2, "j", 10, -8, "start"),
                                 (PI, "-1", -12, 22, "end"), (3 * PI / 2, "-j", 10, 20, "start")]:
        x, y = round(cx + r * math.cos(th), 1), round(cy - r * math.sin(th), 1)
        out += [C(x, y, 6, "n2", 1), TX(round(x + dx, 1), round(y + dy, 1), lab, "tb", 16, anc, 1)]
    if extra:
        x, y = round(cx + r * math.cos(PI / 4), 1), round(cy - r * math.sin(PI / 4), 1)
        out += [L(cx, cy, x, y, "e2", 2), C(x, y, 6, "n4", 2), TX(round(x + 12, 1), round(y - 8, 1), "π/4 (45도)", "t", 14, "start", 2)]
    return SVG(*out)


FIG_UC = _uc()


def _spin():
    cx, cy, r = 90, 135, 65
    th0 = PI / 3
    px, py = round(cx + r * math.cos(th0), 1), round(cy - r * math.sin(th0), 1)
    ax = Ax(200, 450, cy - r, cy + r, 0, 2 * PI, -1, 1)
    return SVG(C(cx, cy, r, "hl"), L(15, cy, 165, cy, "e"), L(cx, 60, cx, 210, "e"),
               L(cx, cy, px, py, "e2"), C(px, py, 6, "n2"), TX(cx, 36, "원 위를 도는 점", "tb", 15),
               L(px, py, ax.X(th0), py, "e", 1), ax.axes("t", 1, yaxis=False),
               ax.curve(math.sin, 0, 2 * PI, "e2", 1), C(ax.X(th0), py, 5, "n2", 1),
               TX(330, 36, "높이를 시간 순서로 그리면 sin", "tb", 15, "middle", 1),
               L(px, py, px, cy, "e", 2), C(px, cy, 5, "n3", 2),
               TX(20, 255, "가로 그림자 = cos, 세로 높이 = sin", "tm", 14, "start", 2))


FIG_SPIN = _spin()


def _three():
    out = []
    for i, (w, lab) in enumerate([(4, "ω = 4, T ≈ 1.57"), (2, "ω = 2, T ≈ 3.14"), (1, "ω = 1, T ≈ 6.28")]):
        ax = Ax(20, 320, 15 + 88 * i, 75 + 88 * i, 0, 12, -1.2, 1.2)
        out += [ax.axes("t", i, yaxis=False), ax.curve(lambda t, w=w: math.cos(w * t), 0, 12, "e2", i, 300),
                TX(345, round(50 + 88 * i, 1), lab, "tb", 15, "start", i)]
    return SVG(*out)


FIG_THREE = _three()

S = []


# =====================================================================
# p.1 표지
# =====================================================================
S.append({"p": 1, "title": "2주차 표지: 1장 신호와 시스템",
 "pass1": [
  say("2주차는 교재 1장, '신호와 시스템'을 배우는 날이에요.",
      "1주차 OT에서 들은 큰 그림을 이제 그래프와 식으로 하나씩 만나요.",
      MANTRA),
  points("이 레슨(1~30쪽)에서 만날 것",
      f"끊김 없는 {K('ct')}, 띄엄띄엄 {K('dt')}",
      f"신호가 얼마나 센지 재는 {K('energy')}",
      f"신호를 옮기고, 뒤집고, 늘이는 법: {K('shift')}, {K('rev')}, {K('scale')}",
      f"반복하는 {K('periodic')}, 그리고 {K('euler')}"),
 ],
 "pass2": [
  say("제목 'Week 2. [Chapter 1] Signals and Systems'는 '2주차, 1장 신호와 시스템'이라는 뜻이에요.",
      f"{K('sig')}은 시간에 따라 변하면서 정보를 담은 값이에요.",
      f"{K('sys')}은 신호를 받아 다른 신호로 바꿔 내보내는 상자예요."),
  check("이 과목의 주문을 바르게 말한 것은?",
      ["신호는 상자, 시스템은 값", "신호는 시간에 따라 변하는 값, 시스템은 신호를 바꾸는 상자", "신호와 시스템은 같은 말"], 1,
      f"{K('sig')}은 값(기록표), {K('sys')}은 그 값을 바꾸는 상자예요. 과목 내내 이 주문을 반복해요."),
 ],
 "pass3": [
  look("표지에서 볼 곳",
      (85, 135, 615, 245, "과목 이름과 '2주차, 1장' 표시예요."),
      (85, 250, 270, 280, "2026년 가을 학기, 과목 번호 03145-03이에요."),
      (85, 490, 560, 565, "담당 교수님 소속, 인공지능학과예요.")),
  prof("오늘부터 본격적으로 신호및시스템을 시작해요.",
      "오늘 진도는 책 1장 1.1절부터 1.6절까지예요."),
  prof("굉장히 어려운 내용이니까 '나만 어렵나' 걱정하지 마세요.",
      "놓친 부분은 교재를 보며 차근차근 복습하면 금방 따라올 수 있어요."),
 ],
 "pass4": [
  points("시험과 이어지는 곳",
      "첫 퀴즈(5주차 시작) 범위는 1장 전체와 2장 안정성(S3 p.70)까지예요.",
      "교수님: 수업에서 다룬 예제와 과제만 복습하면 시간 안에 충분히 풀 수 있는 난이도예요.",
      "그래서 이 레슨의 손계산(3회독)과 시험 대비(4회독)를 꼭 풀어 보세요."),
 ]})

# =====================================================================
# p.2 Reminder
# =====================================================================
S.append({"p": 2, "title": "알림: 자료 배포 금지",
 "pass1": [say("수업 자료 안내 쪽이에요. 내용 공부는 다음 쪽부터예요.",
      "자료는 저작권이 있어서 다른 곳에 퍼뜨리면 안 돼요.")],
 "pass2": [points("두 가지 안내",
      "1번: 저작권이 있는 자료라 배포하지 말 것",
      "2번: 수업 중 영상이나 소리에 문제가 있으면 바로 알릴 것")],
 "pass3": [prof("자료는 다른 데 배포하지 말고 수업 내용 참고로만 써 주세요.",
      "수업 중에 비디오나 오디오 문제가 있으면 손 들고 알려 주세요.")],
 "pass4": []})

# =====================================================================
# p.3 목차
# =====================================================================
S.append({"p": 3, "title": "1장 목차: 여섯 절",
 "pass1": [
  say("1장은 여섯 덩어리예요. 앞의 셋은 신호 이야기, 뒤의 셋은 시스템 이야기예요.",
      f"이 레슨은 1절, 2절과 3절 앞부분까지 다뤄요.", MANTRA),
 ],
 "pass2": [
  points("여섯 절을 쉬운 말로",
      f"1.1 {K('ct','과')} {K('dt')} (4~8쪽)",
      f"1.2 {K('iv')} 바꾸기: 옮기기, 뒤집기, 늘이기, 주기, 짝홀 (9~20쪽)",
      f"1.3 지수 신호와 {K('sinus')} (21쪽부터)",
      f"1.4 {K('imp')}와 계단, 1.5 시스템, 1.6 시스템의 성질 (45쪽부터)"),
  check("1.2절 제목 'Transformations of the Independent Variable'에서 독립 변수는 보통 무엇일까요?",
      ["신호의 크기", "시간", "전압"], 1,
      f"{K('iv')}는 신호가 무엇에 따라 변하는지 정하는 변수예요. $x(t)$에서는 시간 $t$예요."),
 ],
 "pass3": [
  look("목차에서 볼 곳",
      (160, 150, 860, 225, "1절: 연속시간과 이산시간 신호. 4~8쪽이에요."),
      (160, 238, 860, 313, "2절: 독립 변수 변환. 9~20쪽이에요."),
      (160, 330, 860, 405, "3절: 지수 신호와 사인파 신호. 21쪽부터이고 이 레슨은 30쪽까지예요."),
      (160, 418, 860, 672, "4~6절: 단위 임펄스와 계단, 시스템, 시스템의 성질. 다른 레슨에서 이어져요.")),
  prof("오늘 배울 내용은 여섯 가지예요.", "책 1장 1절부터 6절까지를 오늘 진도로 잡았어요."),
 ],
 "pass4": []})

# =====================================================================
# p.4 연속시간과 이산시간
# =====================================================================
S.append({"p": 4, "title": "1.1 연속시간 신호와 이산시간 신호",
 "pass1": [
  analogy("선으로 그린 기록, 점으로 찍은 기록",
      "체온을 기계가 끊김 없이 선으로 그리면 어느 순간이든 값이 있어요. 주식 종가는 하루에 한 번만 점으로 찍혀요.",
      ["끊김 없이 그린 선", K("ct")], ["하루 한 번 찍은 점(매일 종가)", K("dt")],
      ["시간마다 적어 둔 기록표", K("sig")]),
  figure("같은 모양, 두 가지 기록 방법", FIG_CTDT,
      "왼쪽은 모든 순간에 값이 있는 선, 오른쪽은 정수 칸마다 찍은 점이에요.", 1),
  say(f"{K('ct')}는 둥근 괄호 $x(t)$, {K('dt')}는 대괄호 $x[n]$으로 써요.", MANTRA),
 ],
 "pass2": [
  compare("둘을 구별해요", ["", "연속시간", "이산시간"],
      ["기호", "$x(t)$, 둥근 괄호", "$x[n]$, 대괄호"],
      ["독립 변수", "$t$, 모든 실수", "$n$, 정수만"],
      ["값이 있는 곳", "모든 순간", "$n=0, 1, 2$ 같은 칸"],
      ["다른 이름", "CT 신호", "DT 신호, 수열(시퀀스)"]),
  formula("슬라이드 아래 기호 읽기", r"t \in \mathbb{R} \;\to\; x(t), \qquad n \in \mathbb{Z} \;\to\; x[n]",
      [(r"t \in \mathbb{R}", "$t$는 실수 전체 중 하나, 즉 0.5도 3.14도 돼요"),
       (r"n \in \mathbb{Z}", "$n$은 정수 중 하나, 즉 $-1, 0, 1, 2$ 같은 수만 돼요"),
       (r"\to x(t)", "그 시각의 신호 값"),
       (r"x[0], x[1], \dots", "0번째, 1번째 칸의 값을 줄 세운 것")],
      f"{K('ct')}는 실수 시각마다, {K('dt')}는 정수 칸마다 값이 하나씩 있어요."),
  check("$x[2.5]$는 어떤 값일까요?",
      ["$x[2]$와 $x[3]$의 평균", "정의되지 않아요", "항상 0이에요"], 1,
      f"{K('dt')}는 정수 $n$에서만 값이 있어요. 2.5번째 칸은 아예 없어요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (85, 150, 790, 275, "연속시간은 모든 실수 t에서, 이산시간은 정수 n에서만 정의된다는 두 줄이에요."),
      (135, 300, 640, 630, "왼쪽: 매끈한 곡선 x(t). 0부터 10까지 어디든 값이 있어요."),
      (700, 300, 1250, 630, "오른쪽: 막대 끝의 점 x[n]. 0, 1, 2, ... 칸에만 값이 있어요."),
      (300, 635, 1190, 685, "아래 식: 실수 t를 넣으면 x(t), 정수 n을 넣으면 x[0], x[1], ... 이 나와요.")),
  steps(f"{K('samp')}으로 이산시간 신호 만들기",
      ["연속시간 신호를 $x(t)=10-t$ 라고 해요",
       "1초마다 값을 뽑아요. 즉 $x[n]=x(n)$ 이에요",
       "$x[0]=10-0=10$, $x[1]=10-1=9$",
       "$x[2]=8$, $x[3]=7$",
       "$t=0.5$ 같은 사이 값은 버려져요"],
      "$x[n]$ = 10, 9, 8, 7, ... 인 점들이 돼요. 선이 점으로 바뀌었어요.",
      "뽑는 간격 1초"),
  prof("이산시간 신호는 시퀀스라고도 불러요. 고등학교 때 배운 '수열'이에요.",
      f"이산시간 신호는 연속시간 신호를 {K('samp')}해서 얻기도 해요."),
  bg("기초 다지기 b-1 함수와 그래프 읽기",
      "$x(t)$는 '$t$를 넣으면 값이 하나 나오는 함수'예요.",
      "가로축이 시간, 세로축이 그 순간의 값이에요."),
 ],
 "pass4": [
  check("다음 중 이산시간 신호의 표기는?", ["$x(t)$", "$x[n]$", "$x\\{t\\}$"], 1,
      f"대괄호와 정수 $n$이면 {K('dt')}예요. 둥근 괄호 $x(t)$는 {K('ct')}예요."),
  warn("헷갈리기 쉬운 점",
      "이산시간은 '시간 축만' 띄엄띄엄이에요. 값(세로축)은 아무 실수나 될 수 있어요.",
      "값까지 계단처럼 몇 개로 정한 것은 디지털 신호라서 이산시간과 달라요."),
  english("답안 문장", "연속시간 신호 $x(t)$는 모든 실수 $t$에서 정의되고, 이산시간 신호 $x[n]$은 정수 $n$에서만 정의된다.",
      "괄호 모양과 독립 변수의 종류(실수, 정수)로 구별해요.", "둥근 괄호는 둥글게 이어진 선, 대괄호는 칸막이 친 점"),
 ]})

# =====================================================================
# p.5 에너지와 전력의 전기적 동기
# =====================================================================
S.append({"p": 5, "title": "1.1 신호 에너지와 전력: 전기에서 온 아이디어",
 "pass1": [
  say("신호가 얼마나 '센지' 하나의 숫자로 재고 싶어요.",
      f"그 방법을 전기에서 빌려 왔어요. 그래서 이름이 {K('energy','와')} {K('avgp')}이에요."),
  say("전구에 전압이 걸리면 순간순간 전기를 써요.",
      "그걸 시간 동안 모두 모으면 에너지, 시간으로 나누면 평균이에요."),
 ],
 "pass2": [
  formula(f"{K('instp')}: 한 순간에 쓰는 전기", r"p(t) = v(t)\,i(t) = \frac{1}{R}\,v^2(t)",
      [(r"p(t)", "시각 $t$의 전력(한 순간에 쓰는 전기의 양)"),
       (r"v(t)", "저항 양 끝의 전압"), (r"i(t)", "저항을 흐르는 전류"),
       (r"R", "저항 값"), (r"\frac{1}{R}v^2(t)", "옴의 법칙 $i=v/R$ 을 넣어 전압만으로 쓴 것")],
      "전력은 전압의 제곱에 비례해요. 이 '제곱'이 신호 에너지에서도 그대로 나와요."),
  formula("시간 동안 모두 모으면 에너지", r"\int_{t_1}^{t_2} p(t)\,dt = \int_{t_1}^{t_2} \frac{1}{R}\,v^2(t)\,dt",
      [(r"\int_{t_1}^{t_2}", f"{K('integ')}. $t_1$부터 $t_2$까지 그래프 아래 넓이를 구하라는 기호"),
       (r"p(t)\,dt", "아주 짧은 시간 $dt$ 동안 쓴 전기, 그것을 다 더해요")],
      "순간 전력을 구간 전체에서 넓이로 모은 것이 총 에너지예요."),
  compare("세 가지 양", ["이름", "뜻", "구하는 법"],
      [K("instp"), "한 순간의 세기", "$v^2/R$"],
      ["총 에너지", "구간 동안 모은 양", "$p(t)$의 넓이(적분)"],
      [K("avgp"), "구간 동안의 평균 세기", "총 에너지 ÷ 구간 길이"]),
  check("평균 전력은 총 에너지를 무엇으로 나눈 것인가요?", ["저항 $R$", "구간 길이 $t_2-t_1$", "전압 $v$"], 1,
      f"평균은 '모은 양 ÷ 걸린 시간'이에요. 그래서 {K('avgp')} = 총 에너지 ÷ $(t_2-t_1)$ 이에요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (85, 190, 620, 230, "저항 R에 걸린 순간 전력을 먼저 봐요."),
      (420, 245, 860, 340, "순간 전력 식: 전압 곱하기 전류 = 전압 제곱 나누기 R."),
      (85, 335, 880, 465, "총 에너지: 순간 전력을 t1부터 t2까지 적분(넓이)."),
      (85, 462, 1010, 590, "Average Energy라고 적힌 줄: 총 에너지를 (t2 - t1)로 나눈 것."),
      (85, 640, 1210, 690, "맨 아래 줄: 그렇게 나눈 값을 평균 전력(Average power)이라고 해요.")),
  steps("쉬운 숫자로: 전구 한 개",
      ["전압 $v=2$ V, 저항 $R=1$ Ω 이 0초부터 3초까지 그대로라고 해요",
       "순간 전력 $p=v^2/R=2^2/1=4$ W",
       "3초 동안 늘 4이니까 넓이는 가로 $3$ × 세로 $4$",
       "총 에너지 $=12$ J",
       "평균 전력 $=12\\div(3-0)=4$ W"],
      "총 에너지 12, 평균 전력 4예요. 늘 같은 세기면 평균도 그 세기예요."),
  prof("에너지는 신호의 '면적'이라고 생각하면 돼요.",
      "구간 에너지를 그 시간 길이로 나눠 주면 평균이 되고, 그것을 평균 파워라고 해요."),
  bg("기초 다지기 b-8 적분은 넓이, 미분은 기울기",
      f"{K('integ')} $\\int_a^b f(t)\\,dt$ 는 $a$부터 $b$까지 그래프 아래 넓이예요.",
      "직사각형이면 가로 × 세로로 바로 구해요."),
 ],
 "pass4": [
  warn("슬라이드 표기 주의",
      "가운데 줄 이름표는 'Average Energy'인데, 맨 아래 줄과 다음 쪽은 같은 식을 '평균 전력(average power)'이라고 불러요.",
      "시험에서는 '총 에너지를 구간 길이로 나눈 것 = 평균 전력'으로 쓰세요."),
  check("전압 $v=3$ V, 저항 $R=1$ Ω 일 때 순간 전력은?", ["3 W", "6 W", "9 W"], 2,
      "$p=v^2/R=3^2/1=9$ W 예요. 제곱을 잊지 마세요."),
 ]})

assert 3 ** 2 / 1 == 9

# =====================================================================
# p.6 유한 구간의 신호 에너지
# =====================================================================
S.append({"p": 6, "title": "1.1 유한 구간의 신호 에너지",
 "pass1": [
  say(f"{K('energy')}는 신호 크기를 제곱해서 모두 모은 값이에요.",
      "연속시간은 넓이로 모으고, 이산시간은 막대마다 더해서 모아요.",
      f"모은 것을 길이로 나누면 {K('avgp')}이에요."),
 ],
 "pass2": [
  formula(f"연속시간 {K('energy')}", r"E = \int_{t_1}^{t_2} |x(t)|^2\,dt",
      [(r"E", "에너지(Energy)"), (r"|x(t)|", "신호 값의 크기. 음수여도 양수로 바꿔요"),
       (r"|x(t)|^2", "크기의 제곱"), (r"\int_{t_1}^{t_2}\dots dt", f"{K('integ')}: $t_1$부터 $t_2$까지 넓이")],
      "크기 제곱 그래프의 넓이가 에너지예요."),
  formula(f"이산시간 {K('energy')}", r"E = \sum_{n=n_1}^{n_2} |x[n]|^2",
      [(r"\sum_{n=n_1}^{n_2}", f"{K('sigma')}: $n_1$번 칸부터 $n_2$번 칸까지 모두 더해요"),
       (r"|x[n]|^2", "칸마다 값의 크기를 제곱한 것")],
      "칸마다 제곱해서 모두 더한 것이 에너지예요."),
  compare("연속과 이산, 무엇이 다른가", ["", "연속시간", "이산시간"],
      ["모으는 법", f"{K('integ')} $\\int$", f"더하기 {K('sigma')} $\\sum$"],
      ["평균 낼 때 나누는 수", "$t_2-t_1$", "$n_2-n_1+1$"],
      ["나누는 수의 뜻", "구간의 길이", "칸의 개수"]),
  check("$|x(t)|$처럼 절댓값을 쓰는 까닭은?",
      ["계산을 어렵게 하려고", "음수 값이나 복소수 값도 크기로 재려고", "시간을 거꾸로 하려고"], 1,
      "신호가 아래로 내려가도 세기는 양수여야 해요. 슬라이드도 복소수 신호에도 된다고 적었어요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (85, 195, 1000, 365, "연속시간 신호 x(t)의 [t1, t2] 구간 총 에너지 식이에요."),
      (85, 380, 1060, 570, "이산시간 신호 x[n]의 [n1, n2] 구간 총 에너지 식이에요."),
      (85, 585, 1010, 625, "|x(t)|는 크기라서 복소수 신호에도 쓸 수 있어요."),
      (85, 635, 920, 680, "(t2 - t1) 또는 (n2 - n1 + 1)로 나누면 평균 전력 P예요.")),
  figure("넓이로 보는 에너지", FIG_ENERGY,
      "값 2를 제곱하면 4, 3초 동안이면 넓이 12가 에너지예요.", 2),
  steps("연속시간 손계산",
      ["$x(t)=2$ (0초에서 3초까지), 나머지는 0",
       "$|x(t)|^2=2^2=4$",
       "$E=\\int_0^3 4\\,dt$ = 가로 $3$ × 세로 $4$ = $12$",
       "평균 전력 $P=12\\div(3-0)=4$"],
      "$E=12$, $P=4$ 예요."),
  steps("이산시간 손계산",
      ["$x[0]=1$, $x[1]=2$, $x[2]=1$ 이고 $n_1=0$, $n_2=2$",
       "제곱: $1^2=1$, $2^2=4$, $1^2=1$",
       "$E=1+4+1=6$",
       "칸 수 $=2-0+1=3$칸",
       "$P=6\\div3=2$"],
      "$E=6$, $P=2$ 예요."),
  steps("왜 1을 더하나: 손가락으로 세기",
      ["$n_1=2$, $n_2=4$ 라고 해요",
       "칸은 $2, 3, 4$ 이렇게 세 개예요",
       "그런데 $4-2=2$ 라서 하나 모자라요",
       "양 끝을 둘 다 넣으니까 1을 더해요: $4-2+1=3$"],
      "이산시간은 $n_2-n_1+1$ 로 나눠요."),
  prof("신호가 아래로 가면 넓이가 음수가 되니까, 절댓값을 씌우고 제곱해서 진짜 세기를 나타내요.",
      "제곱 대신 절댓값 넓이만 써도 에너지로 쓸 수 있어요(L1). 슬라이드 식은 제곱(L2) 방식이에요."),
  prof("n1부터 n2까지 개수는 손가락으로 세 보면 돼요.", "2, 3, 4는 세 개니까 차이 2에 하나를 더해요."),
 ],
 "pass4": [
  exam("슬라이드 p.6 식 응용 (기출 아님)",
      "$x[0]=1$, $x[1]=-2$, $x[2]=1$ 일 때 $n=0$~$2$ 구간의 에너지와 평균 전력을 구하라.",
      "칸마다 제곱해서 더하고, 칸 수로 나눠요.",
      ["제곱: $1$, $(-2)^2=4$, $1$", "$E=1+4+1=6$", "칸 수 $=2-0+1=3$", "$P=6\\div3=2$"],
      "$E=6$, $P=2$"),
  warn("자주 틀리는 곳",
      "$x$를 그대로 더하면 안 돼요. $1+(-2)+1=0$ 이 되어 버려요. 꼭 $|x|^2$를 더해요.",
      "이산시간 평균은 $n_2-n_1$이 아니라 $n_2-n_1+1$로 나눠요."),
  check("$n_1=-1$, $n_2=3$ 이면 칸은 몇 개인가요?", ["4개", "5개", "3개"], 1,
      "$3-(-1)+1=5$ 개예요. -1, 0, 1, 2, 3을 세어 봐도 5개예요."),
 ]})
assert 3 - (-1) + 1 == 5

# =====================================================================
# p.7 무한 구간의 에너지
# =====================================================================
S.append({"p": 7, "title": "1.1 무한 구간의 에너지",
 "pass1": [
  say("이번에는 시간 전체, 즉 아주 먼 과거부터 아주 먼 미래까지 에너지를 모아요.",
      "잠깐 켜졌다 꺼지는 신호는 모아도 유한해요.",
      "끝없이 계속되는 신호는 모으면 무한히 커질 수 있어요."),
 ],
 "pass2": [
  formula(f"연속시간: 시간 전체의 {K('energy')}", r"E_\infty = \lim_{T\to\infty}\int_{-T}^{T}|x(t)|^2dt = \int_{-\infty}^{\infty}|x(t)|^2dt",
      [(r"E_\infty", "무한 구간 에너지. 슬라이드는 $E_c$ (c는 continuous)라고 썼어요"),
       (r"\int_{-T}^{T}", "$-T$부터 $T$까지 좌우 같은 폭으로 넓이를 구해요"),
       (r"\lim_{T\to\infty}", "그 폭 $T$를 끝없이 키웠을 때 다가가는 값"),
       (r"\int_{-\infty}^{\infty}", "그래서 결국 시간 전체의 넓이")],
      "폭을 점점 넓히며 넓이를 재고, 끝까지 넓힌 값을 에너지로 봐요."),
  formula("이산시간도 같아요", r"E_\infty = \lim_{N\to\infty}\sum_{n=-N}^{N}|x[n]|^2 = \sum_{n=-\infty}^{\infty}|x[n]|^2",
      [(r"\sum_{n=-N}^{N}", "$-N$번 칸부터 $N$번 칸까지 더하기"),
       (r"\lim_{N\to\infty}", "$N$을 끝없이 키우기")],
      "모든 칸의 제곱을 다 더한 것이에요. 슬라이드는 $E_d$ (d는 discrete)라고 썼어요."),
  check("더해도 끝이 없이 커지면(수렴하지 않으면) 에너지는?", ["0", "무한", "1"], 1,
      "슬라이드 마지막 줄: 합이나 적분이 수렴하지 않으면 그 신호의 에너지는 무한이에요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (110, 165, 1320, 250, "많은 신호에서 시간 전체 (-∞, ∞)의 에너지와 전력을 보고 싶다는 말이에요."),
      (390, 330, 1000, 420, "연속시간 E_c: -T~T 적분에서 T를 무한으로."),
      (390, 425, 1000, 540, "이산시간 E_d: -N~N 합에서 N을 무한으로."),
      (110, 560, 1190, 600, "수렴하지 않으면 에너지는 무한.")),
  steps("잠깐 켜진 신호: 폭을 넓혀 보기",
      ["$x(t)=2$ (0초에서 3초까지), 나머지 0. 제곱하면 4",
       "$T=1$: $-1$~$1$ 안에서 신호가 있는 곳은 0~1, 넓이 $4\\times1=4$",
       "$T=2$: 넓이 $4\\times2=8$",
       "$T=3$: 넓이 $4\\times3=12$",
       "$T=10$: 신호는 3초에서 끝나니까 그대로 12"],
      "폭을 아무리 넓혀도 12에서 멈춰요. $E_\\infty=12$, 유한해요."),
  steps("늘 켜진 신호: 폭을 넓혀 보기",
      ["모든 $n$에서 $x[n]=4$, 제곱하면 16",
       "$N=1$: 칸 3개, $3\\times16=48$",
       "$N=10$: 칸 21개, $21\\times16=336$",
       "$N$을 키울수록 끝없이 커져요"],
      "$E_\\infty=\\infty$ 예요."),
  prof("꼭 $-T$부터 $T$까지 잡아야 하나 물을 수 있는데, 이건 표기로 정한 정의라고 보면 돼요.",
      "리미트(lim)가 익숙하지 않으면 조금 복습해 두세요."),
 ],
 "pass4": [
  check("다음 중 에너지가 유한한 신호는?",
      ["모든 $n$에서 $x[n]=1$", "0초부터 5초까지만 1이고 나머지 0", "모든 $t$에서 $x(t)=\\sin t$"], 1,
      "잠깐만 켜진 신호는 넓이가 유한해요. 나머지 둘은 끝없이 이어져 에너지가 무한이에요."),
 ]})

# =====================================================================
# p.8 무한 구간의 평균 전력, 두 부류
# =====================================================================
S.append({"p": 8, "title": "1.1 무한 구간의 평균 전력과 두 부류의 신호",
 "pass1": [
  figure("두 부류의 신호", FIG_TWO,
      "왼쪽은 에너지가 유한하고, 오른쪽은 평균 전력이 유한해요.", 1),
  say("잠깐 켜진 신호는 에너지가 유한하고, 오래 평균 내면 전력은 0이 돼요.",
      "늘 켜진 신호는 에너지가 무한이지만, 평균 전력은 유한해요."),
 ],
 "pass2": [
  formula(f"연속시간 {K('avgp')}", r"P_\infty = \lim_{T\to\infty}\frac{1}{2T}\int_{-T}^{T}|x(t)|^2dt",
      [(r"\int_{-T}^{T}|x(t)|^2dt", "$-T$~$T$ 구간의 에너지"),
       (r"\frac{1}{2T}", "구간 길이 $T-(-T)=2T$ 로 나누기"),
       (r"\lim_{T\to\infty}", "구간을 끝없이 넓히기")],
      "구간 에너지를 구간 길이로 나눈 평균을, 구간을 끝없이 넓혀서 본 값이에요."),
  formula(f"이산시간 {K('avgp')}", r"P_\infty = \lim_{N\to\infty}\frac{1}{2N+1}\sum_{n=-N}^{N}|x[n]|^2",
      [(r"2N+1", "$-N$부터 $N$까지 칸 수. $N-(-N)+1$ 이에요")],
      "칸 수로 나누는 점만 달라요. 앞 쪽의 $n_2-n_1+1$ 과 같은 원리예요."),
  compare("두 부류", ["", "1) 에너지 유한", "2) 평균 전력 유한"],
      ["에너지", "유한", "무한"], ["평균 전력", "0", "유한 (0보다 큼)"],
      ["예", "잠깐 켜진 펄스", "상수 신호, 사인파"]),
  check("에너지가 유한한 신호의 평균 전력은?", ["무한", "0", "에너지와 같아요"], 1,
      "유한한 에너지를 끝없이 긴 시간 $2T$로 나누면 0에 다가가요. 슬라이드의 $P=\\lim E/2T=0$ 이에요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (190, 250, 580, 340, "연속시간 평균 전력: 2T로 나눈 뒤 T를 무한으로."),
      (190, 350, 620, 450, "이산시간 평균 전력: 2N+1로 나눈 뒤 N을 무한으로."),
      (130, 480, 1100, 620, "두 부류: 1) 에너지 유한이면 평균 전력 0, 2) 평균 전력 유한이면 에너지 무한."),
      (130, 640, 1060, 680, "무한 시간 분석은 신호의 '꼬리'(끝없이 먼 곳에서의 모습)에 달려 있어요.")),
  steps("에너지 유한 → 평균 전력 0",
      ["앞 쪽의 펄스: $E=12$",
       "$T=10$: $12\\div20=0.6$",
       "$T=100$: $12\\div200=0.06$",
       "$T=1000$: $12\\div2000=0.006$"],
      "점점 0에 다가가요. $P_\\infty=0$ 이에요."),
  steps("상수 신호 $x[n]=4$: 평균 전력 16",
      ["칸마다 제곱 $4^2=16$",
       "$-N$~$N$ 에너지 $=(2N+1)\\times16$",
       "칸 수 $2N+1$로 나누면 16",
       "$N$이 커져도 늘 16"],
      "$P_\\infty=16$, 에너지는 무한이에요."),
  prof("예를 들어 모든 n에서 4인 상수 신호가 있으면, 어느 구간이든 평균 파워는 4의 제곱인 16이에요.",
      "그런데 모든 시간에서 16씩 계속 더해지니까 에너지는 무한이 돼요."),
  prof("사인처럼 반복되는 신호는 한 주기 에너지가 유한해도, 주기가 끝없이 반복되니까 전체 에너지는 무한이에요.",
      "대신 한 주기의 평균 파워가 계속 반복되니까 평균 파워는 유한해요."),
 ],
 "pass4": [
  prof("파워와 에너지는 사실 아주 중요한 개념은 아니에요. 이 정도만 알아 두면 돼요."),
  exam("교수님 수업 예 (기출 아님)", "모든 $n$에 대해 $x[n]=4$ 일 때 무한 구간 평균 전력과 에너지를 구하라.",
      "늘 4인 신호의 세기와 총량이에요.",
      ["칸마다 $|x[n]|^2=16$", "평균 전력: $(2N+1)\\times16\\div(2N+1)=16$", "에너지: 16씩 끝없이 더하니 무한"],
      "$P_\\infty=16$, $E_\\infty=\\infty$"),
  check("평균 전력이 0보다 큰 유한한 값이면 에너지는?", ["0", "유한", "무한"], 2,
      "평균이 0보다 큰 값이 끝없이 이어지니까 모두 모으면 무한이에요."),
 ]})


# =====================================================================
# p.9 y(t) = x(at + b)
# =====================================================================
S.append({"p": 9, "title": "1.2 독립 변수 변환: y(t) = x(at + b)",
 "pass1": [
  analogy("영상 재생 버튼 세 개",
      "같은 영상을 늦게 틀 수도, 거꾸로 틀 수도, 2배속이나 0.5배속으로 틀 수도 있어요. 영상 내용(모양)은 그대로예요.",
      ["늦게 틀기, 일찍 틀기", K("shift")], ["거꾸로 재생", K("rev")],
      ["2배속, 0.5배속", K("scale")], ["영상 내용", "신호의 모양"]),
  figure("같은 모양, 다른 자리", FIG_TRAP9, "x(t)를 왼쪽으로 옮기면 x(t+1), 좁히면 x(2t)예요.", 2),
 ],
 "pass2": [
  formula("모든 변환을 한 줄로", r"y(t) = x(at + b)",
      [(r"x(\cdot)", "원래 신호. 괄호 안에 넣는 값만 바꿔요"),
       (r"a", "늘이기, 줄이기, 뒤집기를 정해요"),
       (r"b", "옆으로 옮기기를 정해요"),
       (r"y(t)", "바뀐 새 신호")],
      f"{K('iv')} $t$ 자리에 $at+b$를 넣으면 옮기기, 뒤집기, 늘이기가 한꺼번에 돼요."),
  compare("a와 b가 하는 일 (슬라이드 맨 아래 줄)", ["조건", "무슨 일", "이름"],
      ["$b \\ne 0$", "0에서 옆으로 옮겨져요", K("shift")],
      ["$|a|>1$", "좁아져요(압축)", K("scale")],
      ["$0<|a|<1$", "넓어져요(늘림)", K("scale")],
      ["$a<0$", "좌우로 뒤집혀요", K("rev")]),
  check("$y(t)=x(-t)$ 에서 $a$와 $b$는?", ["$a=1$, $b=0$", "$a=-1$, $b=0$", "$a=0$, $b=-1$"], 1,
      f"$-t = (-1)t + 0$ 이에요. $a<0$ 이니 {K('rev')}예요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (540, 245, 860, 300, "핵심 식 y(t) = x(at + b)."),
      (300, 300, 690, 470, "원래 신호 x(t): 0에서 1로 뛰고, 1까지 1, 2에서 0."),
      (710, 300, 1100, 470, "x(t+1): 모양 그대로 왼쪽으로 1칸."),
      (300, 505, 690, 680, "x(t-1): 오른쪽으로 1칸."),
      (710, 505, 1100, 680, "x(2t): 폭이 절반으로."),
      (225, 700, 1180, 735, "a, b 조건별 효과 정리 줄.")),
  steps("모서리 점이 어디로 가나",
      ["$x(t)$의 모서리: $t=0, 1, 2$",
       "$x(t+1)$: 괄호 안이 0, 1, 2가 되려면 $t=-1, 0, 1$",
       "$x(t-1)$: $t-1=0, 1, 2$ 에서 $t=1, 2, 3$",
       "$x(2t)$: $2t=0, 1, 2$ 에서 $t=0, 0.5, 1$"],
      "괄호 안을 원래 모서리 값과 같게 두고 $t$를 풀면 새 모서리가 나와요."),
  prof("이번에는 조금 더 중요한 내용이에요. 신호를 시간에 따라 변환할 수 있어요.",
      "세 가지가 있어요. 시간 이동, 시간 반전, 시간 척도 변환이에요."),
  bg("기초 다지기 b-2 그래프 옮기기, 뒤집기, 늘이기",
      "함수 그래프를 옆으로 옮기고 뒤집고 늘이는 연습이 여기서 바로 쓰여요."),
 ],
 "pass4": [
  warn("헷갈리기 쉬운 점",
      "'b가 옮기는 양'은 $a=1$일 때만 그대로예요. $a\\ne1$이면 옮기는 양은 $b/a$예요(13쪽 레시피).",
      "슬라이드 머리말은 'Time-shift'라고 적혀 있지만, 이 쪽은 세 변환 전체를 묶어 보여 줘요."),
  check("$x(2t)$는 $x(t)$와 비교해 어떻게 되나요?", ["폭이 2배", "폭이 절반", "위아래로 2배"], 1,
      "$|a|=2>1$ 이라 압축돼요. 모서리 2가 1로 와요."),
 ]})

# =====================================================================
# p.10 시간 이동
# =====================================================================
S.append({"p": 10, "title": "1.2 시간 이동 x(t - t0)",
 "pass1": [
  analogy("늦게 틀기, 일찍 틀기",
      "같은 노래를 4초 늦게 틀면 모든 소리가 4초 뒤에 나와요. 2초 일찍 틀면 2초 앞에 나와요.",
      ["늦게 틀기", K("delay")], ["일찍 틀기", K("adv")], ["노래 내용은 그대로", "모양은 그대로"]),
  figure("옮겨도 모양은 그대로", FIG_SHIFT, "빼기(t-4)는 오른쪽, 더하기(t+2)는 왼쪽이에요.", 2),
 ],
 "pass2": [
  formula(K("shift"), r"x(t - t_0)",
      [(r"t_0", "옮기는 양"), (r"t_0>0", "오른쪽으로 가요: 늦어짐, 지연"),
       (r"t_0<0", "왼쪽으로 가요: 빨라짐, 앞당김")],
      "모양은 그대로, 모든 점이 $t_0$만큼 옆으로 움직여요."),
  compare("지연과 앞당김", ["", K("delay"), K("adv")],
      ["식", "$x(t-4)$", "$x(t+2)$"], ["방향", "오른쪽", "왼쪽"],
      ["슬라이드 예", "[-1, 3] → [3, 7]", "[-1, 3] → [-3, 1]"]),
  check("$x(t-3)$은 $x(t)$를 어느 쪽으로 옮긴 것인가요?", ["왼쪽으로 3", "오른쪽으로 3", "위로 3"], 1,
      f"빼기인데 오른쪽이에요. $t_0=3>0$ 이면 {K('delay')}예요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (85, 150, 1210, 245, "$t_0>0$ 이면 오른쪽(delay), $t_0<0$ 이면 왼쪽(advance)."),
      (110, 300, 480, 580, "x(t): -1부터 3까지 높이 2인 네모."),
      (520, 300, 880, 580, "x(t-4): 3부터 7까지. 오른쪽으로 4."),
      (925, 300, 1290, 580, "x(t+2): -3부터 1까지. 왼쪽으로 2."),
      (85, 630, 1030, 675, "모양은 안 바뀌고 모든 점이 t0만큼 움직여요.")),
  steps("대입해서 확인하기: $y(t)=x(t-4)$",
      ["$t=3$ 을 넣으면 $y(3)=x(3-4)=x(-1)$",
       "원래 신호의 왼쪽 끝 $-1$이 $t=3$으로 왔어요",
       "$t=7$ 을 넣으면 $y(7)=x(7-4)=x(3)$",
       "원래 오른쪽 끝 3이 $t=7$로 왔어요"],
      "새 구간은 [3, 7]. 오른쪽으로 4만큼 옮겨졌어요."),
  steps("$x(t+2)$ 모서리",
      ["괄호 안 $t+2$가 $-1$이 되려면 $t=-3$",
       "괄호 안 $t+2$가 3이 되려면 $t=1$"],
      "새 구간 [-3, 1], 왼쪽으로 2예요."),
  prof("시간 이동은 부호가 중요해요. 마이너스일 때 오른쪽으로 이동해요.",
      "헷갈리면 t에 값을 대입해 보세요. t에 3을 넣으면 x(-1)과 같아지죠."),
  prof("이산 신호에서도 완벽하게 똑같이 적용돼요. x[n - n0]도 똑같이 옮겨져요."),
 ],
 "pass4": [
  prof("부호가 헷갈리는데, $x(t-t_0)$은 $t_0>0$ 일 때 오른쪽으로 간다는 것을 꼭 기억하세요."),
  warn("시험 단골 함정",
      "$x(t-4)$를 '왼쪽으로 4'라고 쓰기 쉬워요. 빼기는 오른쪽(지연)이에요.",
      "확신이 없으면 끝점을 대입: 괄호 안이 원래 끝점 값이 되는 $t$를 풀어요."),
  check("$x(t)$가 [-1, 3]에서만 0이 아닐 때 $x(t-5)$가 0이 아닌 구간은?", ["[-6, -2]", "[4, 8]", "[-1, 3]"], 1,
      "$t-5=-1$ 에서 $t=4$, $t-5=3$ 에서 $t=8$ 이에요."),
  english("답안 문장", "$x(t-t_0)$는 $t_0>0$이면 $x(t)$를 오른쪽으로 $t_0$만큼 옮긴 지연 신호이고, $t_0<0$이면 왼쪽으로 옮긴 앞당김 신호이다.",
      "모양은 그대로, 위치만 바뀌어요.", "빼면 늦게(오른쪽), 더하면 일찍(왼쪽)"),
 ]})

# =====================================================================
# p.11 시간 반전
# =====================================================================
S.append({"p": 11, "title": "1.2 시간 반전 x(-t)",
 "pass1": [
  analogy("거꾸로 재생",
      "영상을 거꾸로 틀면 마지막 장면이 처음에 나와요. 그래프로는 세로축(t = 0)을 거울 삼아 좌우를 바꾼 모습이에요.",
      ["거꾸로 재생", K("rev")], ["거울", "$t=0$ 인 세로축"]),
  figure("좌우로 뒤집기", FIG_REV, "[-1, 3] 네모가 [-3, 1]로 뒤집혀요.", 1),
 ],
 "pass2": [
  formula(K("rev"), r"x(-t)",
      [(r"-t", "시간에 마이너스를 붙여요"), (r"t=0", "뒤집는 기준, 거울이에요")],
      "$t=0$을 기준으로 좌우를 바꾼 거울상이에요."),
  say("오른쪽에 있던 점은 왼쪽으로, 왼쪽에 있던 점은 오른쪽으로 가요.",
      "$t=0$ 위의 값은 그대로예요."),
  check("$x(t)$의 $t=2$ 값은 $x(-t)$에서 어디로 가나요?", ["$t=2$", "$t=-2$", "$t=0$"], 1,
      "$x(-t)$에 $t=-2$를 넣으면 $x(2)$가 돼요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (85, 150, 730, 245, "Time reversal: $t=0$ 을 기준으로 뒤집은 거울상."),
      (250, 325, 670, 600, "x(t): -1부터 3까지 높이 2."),
      (730, 325, 1150, 600, "x(-t): -3부터 1까지 높이 2.")),
  steps("대입해서 확인하기",
      ["$y(t)=x(-t)$ 에 $t=-3$ 을 넣으면 $y(-3)=x(3)$",
       "원래 오른쪽 끝 3이 $-3$으로 왔어요",
       "$t=1$ 을 넣으면 $y(1)=x(-1)$",
       "원래 왼쪽 끝 $-1$이 1로 왔어요"],
      "새 구간 [-3, 1]이에요."),
  prof("x(-t)는 y축 대칭이 돼요.", "t에 -3을 넣으면 x(3)과 같아지니까, 3에 있던 값이 -3으로 와요."),
 ],
 "pass4": [
  check("$x(t)$가 [2, 5]에서만 0이 아니면 $x(-t)$는?", ["[2, 5]", "[-5, -2]", "[-2, 5]"], 1,
      "끝점 2와 5가 각각 $-2$, $-5$로 가요. 작은 수부터 쓰면 [-5, -2]예요."),
  warn("주의", "뒤집는 기준은 늘 $t=0$이에요. 신호의 가운데가 기준이 아니에요."),
 ]})

# =====================================================================
# p.12 시간 척도 변환
# =====================================================================
S.append({"p": 12, "title": "1.2 시간 척도 변환 x(ct)",
 "pass1": [
  analogy("빨리 감기, 느리게 보기",
      "영상을 3배속으로 틀면 같은 장면이 3배 짧은 시간에 끝나요. 0.5배속이면 2배 길어져요.",
      ["3배속", "$x(3t)$: 좁아짐"], ["느리게 재생", "$x(t/2.5)$: 넓어짐"], ["재생 속도 조절", K("scale")]),
  figure("좁히기와 늘이기", FIG_SCALE, "폭 4짜리 네모가 3배 좁아지거나 2.5배 넓어져요.", 2),
 ],
 "pass2": [
  formula(K("scale"), r"x(ct)",
      [(r"c>1", "좁아져요(압축). 폭이 $1/c$ 배"), (r"0<c<1", "넓어져요(늘림). 폭이 $1/c$ 배"),
       (r"t/c", "원래 점 $t$가 옮겨 가는 자리")],
      "$c$가 클수록 빨리 재생한 것처럼 좁아져요."),
  compare("c 에 따라", ["", "$c>1$", "$0<c<1$"],
      ["모양", "압축", "늘림"], ["슬라이드 예", "$x(3t)$", "$x(t/2.5)$"],
      ["폭 4의 변화", "$4/3$", "10"]),
  check("$x(0.5t)$는?", ["폭이 절반", "폭이 2배", "그대로"], 1,
      "$c=0.5<1$ 이라 늘어나요. 폭은 $1/0.5=2$ 배예요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (85, 150, 870, 245, "$c>1$ 이면 $c$배 압축, $0<c<1$ 이면 $1/c$배 늘림."),
      (160, 300, 460, 640, "(i) x(t): -1부터 3까지, 폭 W = 4."),
      (470, 300, 740, 640, "(ii) x(3t): -1/3부터 1까지. 1은 3/3에서 왔다고 적혀 있어요."),
      (750, 300, 1085, 640, "(iii) x(t/2.5): -2.5부터 7.5까지. -1/(1/2.5), 3/(1/2.5)."),
      (85, 670, 1210, 710, "주의: 점은 t/c 로 옮겨가요. 끝점이 어디로 가는지 늘 확인.")),
  steps("$x(3t)$ 끝점",
      ["괄호 안 $3t=-1$ 에서 $t=-1/3$",
       "괄호 안 $3t=3$ 에서 $t=1$",
       "폭: $1-(-1/3)=4/3$"],
      "폭 4가 $4/3$으로, 3배 좁아졌어요."),
  steps("$x(t/2.5)$ 끝점",
      ["$c=1/2.5=0.4$",
       "$0.4t=-1$ 에서 $t=-2.5$",
       "$0.4t=3$ 에서 $t=7.5$",
       "폭: $7.5-(-2.5)=10$"],
      "폭 4가 10으로, 2.5배 넓어졌어요."),
  prof("특히 c가 1보다 클 때, 커지면 커질수록 좁아진다. 이 개념만 알고 가시면 돼요.",
      "t에 -1/3을 넣으면 x(-1)과 같아지고, 1을 넣으면 x(3)과 같아져요."),
 ],
 "pass4": [
  warn("헷갈리기 쉬운 점",
      "$x(2t)$를 '2배 넓어진다'로 착각하기 쉬워요. 반대로 절반으로 좁아져요.",
      "끝점은 곱하는 게 아니라 나눠요: 새 끝점 = 원래 끝점 ÷ $c$."),
  check("$x(t)$가 [-1, 3]에서만 0이 아니면 $x(2t)$는?", ["[-2, 6]", "[-0.5, 1.5]", "[-1, 3]"], 1,
      "$-1\\div2=-0.5$, $3\\div2=1.5$ 예요."),
 ]})


# =====================================================================
# p.13 변환 예제와 레시피
# =====================================================================
S.append({"p": 13, "title": "1.2 변환 예제: x(t+1), x(-t+1), x(3t/2), x(3t/2+1)",
 "pass1": [
  say("옮기기, 뒤집기, 늘이기가 한꺼번에 섞여 나오면 순서를 정해서 하나씩 해요.",
      "순서는 '먼저 뒤집기와 늘이기, 그다음 옮기기'예요."),
  points("레시피를 쉬운 말로",
      "1단계: 괄호 안을 $a$로 묶어요",
      f"2단계: $a$를 보고 뒤집고({K('rev')}) 늘이거나 줄여요({K('scale')})",
      f"3단계: 묶인 괄호 안의 수만큼 옆으로 옮겨요({K('shift')})"),
 ],
 "pass2": [
  formula("레시피 식", r"x(at+b) = x\!\left(a\left(t+\frac{b}{a}\right)\right)",
      [(r"a", "먼저 처리: 음수면 뒤집고, 크기만큼 늘이거나 줄여요"),
       (r"t+\frac{b}{a}", "그다음 처리: $-b/a$ 쪽으로 옮겨요"),
       (r"-\frac{b}{a}", "옮기는 양과 방향. 양수면 오른쪽, 음수면 왼쪽")],
      "$a$로 묶은 뒤, ① $a$로 뒤집기와 늘이기 ② $-b/a$ 만큼 옮기기."),
  steps("$x(-t+1)$에 레시피 쓰기",
      ["$a=-1$ 로 묶기: $x(-(t-1))$",
       "① $a=-1$: 크기 1이라 늘이기는 없고, 뒤집기만 해요: $x(-t)$",
       "② 괄호 안이 $t-1$ 이니 오른쪽으로 1"],
      "뒤집은 다음 오른쪽으로 1만큼 옮기면 돼요."),
  check("$x(3t/2+1)$을 $a$로 묶으면?", ["$x(\\tfrac32(t+1))$", "$x(\\tfrac32(t+\\tfrac23))$", "$x(\\tfrac32 t)+1$"], 1,
      "$b/a = 1\\div\\tfrac32=\\tfrac23$ 이에요. 그래서 압축 뒤 왼쪽으로 $2/3$ 옮겨요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (150, 215, 410, 360, "원래 x(t): 0에서 1로 뛰고, 1까지 1, 2에서 0으로 내려가요."),
      (470, 215, 730, 360, "x(t+1): -1에서 뛰고, 0까지 1, 1에서 0."),
      (790, 215, 1050, 360, "x(-t+1): -1에서 올라가서 0부터 1까지 1, 1에서 뚝 떨어져요."),
      (305, 410, 570, 560, "x(3t/2): 0에서 뛰고, 2/3까지 1, 4/3에서 0."),
      (625, 410, 890, 560, "x(3t/2+1): -2/3에서 뛰고, 0까지 1, 2/3에서 0."),
      (190, 590, 1195, 725, "레시피: ① a로 뒤집기, 늘이기 ② -b/a 만큼 옮기기.")),
  steps("모서리 추적 공식",
      ["원래 모서리 $s=0, 1, 2$ (0에서 뛰고, 1까지 평평, 2에서 0)",
       "새 신호 $x(at+b)$ 에서 괄호 안 $at+b=s$ 가 되는 $t$를 찾아요",
       "풀면 $t=(s-b)/a$",
       "$x(t+1)$: $a=1$, $b=1$ 이면 $t=-1, 0, 1$"],
      "모서리 세 개만 옮기면 그래프가 그려져요."),
  steps("$x(-t+1)$ 모서리",
      ["$a=-1$, $b=1$",
       "$s=0$ (뛰는 곳): $t=(0-1)/(-1)=1$",
       "$s=1$ (평평 끝): $t=(1-1)/(-1)=0$",
       "$s=2$ (0이 되는 곳): $t=(2-1)/(-1)=-1$"],
      "$-1$에서 올라가 0~1 평평, 1에서 뚝. 슬라이드 그림과 같아요."),
  figure("뒤집고 나서 옮기기", FIG_FLIP, "x(t) → x(-t) (뒤집기) → x(-t+1) (오른쪽 1).", 2),
  steps("$x(3t/2)$와 $x(3t/2+1)$ 모서리",
      ["$x(3t/2)$: $a=3/2$, $b=0$ → $t=0, 2/3, 4/3$",
       "$x(3t/2+1)$: $a=3/2$, $b=1$",
       "$s=0$: $t=(0-1)\\div\\tfrac32=-2/3$",
       "$s=1$: $t=0$, $s=2$: $t=2/3$"],
      "압축 뒤 왼쪽으로 $2/3$ 옮긴 모양이에요."),
  figure("줄이고 나서 옮기기", FIG_CS, "x(t) → x(3t/2) (2/3배 폭) → x(3t/2+1) (왼쪽 2/3).", 2),
  prof("가장 쉬운 레시피는 a로 먼저 묶는 거예요. 스케일이나 플립, 즉 a를 먼저 신경 쓰고 그다음에 시프트를 보면 편해요.",
      "x(-t+1)은 a가 -1이라 압축은 없고 뒤집기만 한 뒤, 오른쪽으로 1만큼 옮기면 돼요."),
 ],
 "pass4": [
  exam("슬라이드 p.13 예제 응용 (기출 아님)",
      "같은 x(t)에 대해 x(-2t+2)를 그려라.",
      "뒤집고, 절반으로 좁히고, 옮긴 모양을 모서리로 구해요.",
      ["$a=-2$, $b=2$, 모서리 $t=(s-2)/(-2)$",
       "$s=0$: $t=1$ (여기서 뚝 떨어짐)",
       "$s=1$: $t=1/2$ (평평한 끝)",
       "$s=2$: $t=0$ (0에서 시작해 올라감)"],
      "0에서 1/2까지 올라가고, 1/2부터 1까지 1, $t=1$에서 0으로 떨어져요."),
  warn("자주 틀리는 순서",
      "$x(3t/2)$를 그린 뒤 $b=1$ 만큼 왼쪽으로 옮기면 모서리가 $-1, -1/3, 1/3$ 이 되어 틀려요.",
      "늘이기 다음에 옮길 때는 $b$가 아니라 $b/a=2/3$ 만큼 옮겨요.",
      "반대로 먼저 $x(t+1)$로 옮긴 뒤 $t$ 자리에 $3t/2$를 넣어 모서리를 $\\tfrac32$로 나눠도 같은 답이 나와요."),
  check("$x(2t-4)$는 $x(2t)$를 어떻게 옮긴 것인가요?", ["오른쪽 4", "오른쪽 2", "왼쪽 2"], 1,
      "$x(2(t-2))$ 라서 오른쪽으로 $b/a$ 크기 $4/2=2$ 만큼이에요."),
 ]})

# =====================================================================
# p.14 이산시간 예제 y[n] = x[3n+6]
# =====================================================================
S.append({"p": 14, "title": "1.2 이산시간 예제: y[n] = x[3n + 6]",
 "pass1": [
  say(f"{K('dt')}에서도 옮기기, 뒤집기, 늘이기는 똑같이 해요.",
      "다만 줄이면(압축) 칸 사이 점들이 사라져요. 정수 칸에만 값이 있으니까요."),
  figure("점이 사라지는 압축", FIG_DTTRI, "삼각형 점 여러 개 중 $n=-2$ 하나만 남아요.", 2),
 ],
 "pass2": [
  formula("이 문제의 식", r"y[n] = x[3n+6] = x[3(n+2)]",
      [(r"3n", "3칸마다 하나씩만 골라요(압축)"), (r"+6", "옆으로 옮기기"),
       (r"3(n+2)", "3으로 묶으면 왼쪽으로 2")],
      "3배 압축하고 왼쪽으로 2만큼 옮기는데, 이산시간이라 점이 빠져요."),
  compare("두 가지 풀이 (슬라이드)", ["", "방법 1", "방법 2"],
      ["하는 일", "먼저 6칸 옮기고 3칸마다 하나 고르기", "$n$을 직접 넣어 보기"],
      ["장점", "그림으로 이해", "실수가 적어요"]),
  check("이산시간에서 $x[3n]$처럼 압축하면?", ["점이 더 생겨요", "일부 점이 사라져요", "아무 변화 없어요"], 1,
      "정수 $n$만 쓰니까 $3n$은 3의 배수 칸만 골라요. 나머지 칸 값은 버려져요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (85, 150, 820, 190, "삼각형 x[n]에 대해 y[n] = x[3n + 6]을 구하는 문제."),
      (85, 200, 1240, 295, "방법 1(6 옮기고 3칸마다), 방법 2(직접 대입)."),
      (215, 360, 670, 630, "x[n]: n = 0에서 1, 그림상 ±1에서 약 2/3, ±2에서 약 1/3, ±3에서 0."),
      (730, 360, 1180, 630, "y[n]: n = -2 에서만 1."),
      (85, 650, 1330, 690, "$3n+6=0$ 이 되는 $n=-2$ 만 남아 $y[n]=\delta[n+2]$. 이산시간 척도 변환은 샘플을 버려요.")),
  steps("방법 2: 직접 넣어 보기",
      ["$x[m]$이 0이 아닌 곳은 $m=-2, -1, 0, 1, 2$",
       "$n=-4$: $3n+6=-6$, $x[-6]=0$",
       "$n=-3$: $3n+6=-3$, $x[-3]=0$",
       "$n=-2$: $3n+6=0$, $x[0]=1$",
       "$n=-1$: $3n+6=3$, $x[3]=0$ / $n=0$: $x[6]=0$"],
      "$y[-2]=1$, 나머지는 0이에요."),
  steps("방법 1: 먼저 옮기고 고르기",
      ["$w[n]=x[n+6]$: 삼각형을 왼쪽으로 6, 가운데가 $n=-6$",
       "$w$가 0이 아닌 칸: $-8$~$-4$",
       "$y[n]=w[3n]$: 3의 배수 칸($-9, -6, -3$)만 골라요",
       "그중 0이 아닌 것은 $w[-6]=1$ 하나, 그 칸은 $n=-2$"],
      "같은 답 $y[n]=\\delta[n+2]$ 이에요."),
  say(f"$\\delta[n+2]$는 $n=-2$ 에서만 1인 {K('imp')}예요.", "45쪽(1.4절)에서 자세히 배워요."),
  prof("이산 신호는 정수에서만 값이 찍히니까, 폭이 3분의 1로 줄면 사이 값들이 날아가요.",
      "그래서 이산 신호에서의 타임 스케일링은 샘플을 드롭하는 효과가 있어요. 꼭 기억해 두세요."),
 ],
 "pass4": [
  exam("슬라이드 p.14 예제 응용 (기출 아님)",
      "같은 삼각형 x[n]에 대해 y[n] = x[2n]을 구하라.",
      "짝수 칸만 골라요.",
      ["$n=-1$: $x[-2]=1/3$", "$n=0$: $x[0]=1$", "$n=1$: $x[2]=1/3$", "$n=\\pm2$: $x[\\pm4]=0$"],
      "$y[-1]=1/3$, $y[0]=1$, $y[1]=1/3$, 나머지 0. 홀수 칸 값은 사라져요."),
  warn("연속시간과 다른 점",
      "연속시간 $x(3t)$는 모양이 그대로 좁아지지만, 이산시간 $x[3n]$은 점이 버려져 모양이 달라져요.",
      "버려진 값은 $y[n]$만 보고는 되찾을 수 없어요."),
 ]})

# =====================================================================
# p.15 주기 신호
# =====================================================================
S.append({"p": 15, "title": "1.2 주기 신호 x(t) = x(t + T)",
 "pass1": [
  analogy("매일 같은 시간표",
      "학교 시간표는 매주 똑같이 반복돼요. 한 주 뒤로 옮겨 놓아도 시간표는 그대로예요.",
      ["반복되는 시간표", K("periodic")], ["한 주(반복 간격)", "주기 $T$"]),
  figure("sin t 는 2π마다 반복", FIG_SIN, "봉우리에서 다음 봉우리까지가 한 주기예요.", 1),
 ],
 "pass2": [
  formula(f"{K('periodic')}의 정의", r"x(t) = x(t+T)",
      [(r"T", "반복 간격(주기)"), (r"x(t+T)", "$T$만큼 옮긴 신호"),
       (r"=", "모든 $t$에서 같아야 해요")],
      f"$T$만큼 {K('shift')}해도 그대로인 신호가 주기 신호예요."),
  say("주기는 여러 개예요. $T$가 주기면 $2T$, $3T$도 주기예요.",
      f"그중 가장 작은 양수를 {K('fund')}라고 해요."),
  check("$x(t)=x(t+T)$가 성립하려면?", ["어느 한 $t$에서만", "모든 $t$에서", "$t=0$에서만"], 1,
      "모든 시각에서 같아야 주기 신호예요. 다음 쪽에서 더 강조해요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (85, 150, 1050, 245, "x(t)가 T만큼 시간 이동해도 안 바뀌면 주기 T인 주기 신호."),
      (545, 265, 890, 375, "정의 식 x(t) = x(t + T)."),
      (275, 380, 1160, 690, "x(t) = sin t, 봉우리 간격 T = 2π.")),
  steps("sin 으로 확인하기",
      ["$t=\\pi/2$: $\\sin(\\pi/2)=1$",
       "$2\\pi$ 뒤: $\\sin(\\pi/2+2\\pi)=\\sin(5\\pi/2)=1$, 같아요",
       "$\\pi$ 뒤는? $\\sin(\\pi/2+\\pi)=-1$, 달라요",
       "그래서 $\\pi$는 주기가 아니고, $2\\pi$는 주기예요"],
      "sin t 의 주기는 $2\\pi$ (약 6.28)예요."),
  prof("주기는 t가 2π여도, 4π여도, 6π여도 성립해요. 주기는 여러 개가 될 수 있어요.",
      "그중 가장 작은 양수 값을 기본 주기(fundamental period)라고 해요."),
  bg("기초 다지기 b-3 각도, 라디안, 사인과 코사인",
      f"각도 $2\\pi$ {K('rad')}은 원 한 바퀴(360도)예요.", "sin 은 한 바퀴 돌 때마다 같은 값으로 돌아와요."),
 ],
 "pass4": [
  check("sin t 에 대해 $T=4\\pi$도 주기인가요?", ["예, 주기예요", "아니요"], 0,
      f"$2\\pi$의 2배라서 주기예요. 다만 {K('fund')}는 가장 작은 $2\\pi$예요."),
 ]})

assert Fr(4, 2) == 2 and corners(2, -4, (0,)) == [2]

# =====================================================================
# p.16 모든 t, 정수 배, 비주기
# =====================================================================
S.append({"p": 16, "title": "1.2 주기성은 모든 t 에서, 그리고 비주기 신호",
 "pass1": [
  figure("주기와 비주기", FIG_APER, "위는 끝없이 같은 모양, 아래는 점점 빨라져서 반복이 아니에요.", 1),
  say(f"한동안 반복처럼 보여도 나중에 모양이 바뀌면 {K('aper')}예요.",
      f"진짜 {K('periodic')}는 처음부터 끝까지 똑같이 반복해요."),
 ],
 "pass2": [
  formula("정수 배도 모두 주기", r"x(t) = x(t+nT), \quad n = 1, 2, 3, \dots",
      [(r"nT", "주기 $T$를 $n$번 더한 간격"), (r"n=1,2,3,\dots", "자연수 아무거나")],
      "$T$만큼 옮겨도 같으면, 두 번, 세 번 옮겨도 같아요."),
  compare("구별하기", ["", K("periodic"), K("aper")],
      ["반복", "모든 $t$에서 끝없이", "한동안만, 또는 전혀"],
      ["슬라이드 그림", "가운데 (g(t)를 T0마다 반복)", "오른쪽 (점점 촘촘해짐)"]),
  check("처음 1초 동안은 반복하다가 그 뒤 모양이 바뀌는 신호는?", [K("periodic"), K("aper")], 1,
      "모든 $t$에서 반복하지 않으니 비주기 신호예요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (85, 150, 1070, 245, "모든 t에서 x(t) = x(t+T)이면 모든 정수 n에 대해 x(t) = x(t + nT)."),
      (395, 262, 990, 318, "식: n = 1, 2, 3, ..."),
      (220, 355, 510, 600, "g(t): $t=0$ 근처에 볼록한 산 하나."),
      (540, 355, 860, 600, "periodic: g(t)를 T0마다 반복해 붙인 주기 신호."),
      (870, 355, 1180, 600, "aperiodic: 0.5 이후 점점 촘촘해져 반복이 아님."),
      (85, 630, 1290, 675, "한동안 반복처럼 보여도 바뀌면 비주기.")),
  steps("정수 배 확인",
      ["sin t 의 주기 $T=2\\pi$",
       "$n=3$: $3T=6\\pi$",
       "$\\sin(1+6\\pi)=\\sin(1)$, 같아요"],
      "주기의 정수 배는 모두 주기예요."),
  prof("딱 봐도 주기적이지 않은 신호는 앞에 a를 붙여서 aperiodic 이라고 해요.",
      "주기의 자연수 배는 무조건 같은 값을 가져요."),
 ],
 "pass4": [
  warn("헷갈리기 쉬운 점", "'잠깐 반복'은 주기 신호가 아니에요. 정의는 '모든 $t$'예요.",
      "오른쪽 그림처럼 처음 몇 번 같은 모양이어도 뒤에서 바뀌면 비주기예요."),
 ]})

# =====================================================================
# p.17 이산시간 주기 신호 예
# =====================================================================
S.append({"p": 17, "title": "1.2 주기 신호 예 1: 이산시간 (N = 8)",
 "pass1": [
  say(f"{K('dt')}도 같은 무늬가 일정한 칸마다 반복되면 {K('periodic')}예요.",
      "이 예는 8칸마다 같은 무늬가 반복돼요."),
  figure("8칸마다 반복", FIG_DTPER, "0번 칸의 무늬가 8번, -8번 칸에서 다시 나와요.", 1),
 ],
 "pass2": [
  formula("이산시간 주기", r"x[n] = x[n+N]",
      [(r"N", "반복 칸 수. 정수예요"), (r"N_0", f"가장 작은 양의 $N$, {K('fund')}")],
      "모든 $n$에서 $N$칸 옮겨도 그대로면 주기 신호예요."),
  compare("기본 주기 기호", ["", "연속시간", "이산시간"], ["기호", "$T_0$", "$N_0$"], ["단위", "시간(실수)", "칸 수(정수)"]),
  check("이산시간 주기 $N$이 될 수 있는 것은?", ["2.5", "8", "$\\pi$"], 1, "$n$이 정수라서 $N$도 정수여야 해요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (85, 160, 840, 200, "예 1: 이산시간 주기 신호."),
      (85, 215, 1250, 265, "무늬가 N칸마다 반복."),
      (235, 295, 1170, 570, "x[n] (N = 8): 0, 8, -8 에서 1."),
      (85, 595, 700, 640, "그런 N 중 가장 작은 것이 기본 주기 N0.")),
  steps("그림 값 읽기 (그림은 $\\cos(\\pi n/4)$ 값과 맞아요)",
      ["$n=0$: 1, $n=1$: 약 0.71, $n=2$: 0",
       "$n=3$: 약 $-0.71$, $n=4$: $-1$",
       "$n=5$~$7$: $-0.71$, 0, 0.71",
       "$n=8$: 다시 1, 무늬가 처음으로 돌아왔어요"],
      "8칸마다 반복, $N_0=8$ 이에요. 16칸도 주기지만 기본 주기는 8이에요."),
  prof("예를 들어 삼지창 모양이 0, 1, 2번 칸 다음 3, 4, 5번 칸에서 그대로 반복되면 주기는 3이에요.",
      "그럼 6도, 9도, 12도 주기가 될 수 있고, 가장 작은 양수 주기를 기본 주기 N0 라고 해요."),
  prof("교재 표기는 연속시간 기본 주기를 T0, 이산시간을 N0 로 써요."),
 ],
 "pass4": [
  check("주기가 3인 이산시간 신호에서 주기가 아닌 것은?", ["6", "9", "4"], 2, "3의 배수만 주기예요. 4는 아니에요."),
 ]})

# =====================================================================
# p.18 sin(t) 기본 주기 2π
# =====================================================================
S.append({"p": 18, "title": "1.2 주기 신호 예 2: 연속시간 sin(t)",
 "pass1": [
  say("sin t 는 한 번 오르내리는 데 $2\\pi$만큼 걸려요. 약 6.28이에요.",
      f"그래서 {K('fund')}는 $T_0=2\\pi$예요."),
 ],
 "pass2": [
  formula(f"sin t 의 {K('fund')}", r"T_0 = 2\pi \approx 6.28",
      [(r"T_0", "기본 주기"), (r"2\pi", f"한 바퀴를 {K('rad')}으로 쓴 값")],
      "시간이 $2\\pi$ 지날 때마다 같은 모양이 나와요."),
  check("그림의 $-6\\pi$부터 $6\\pi$ 사이에는 주기가 몇 번 들어 있나요?", ["3번", "6번", "12번"], 1,
      "폭 $12\\pi$를 주기 $2\\pi$로 나누면 6번이에요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (85, 150, 885, 195, "예 2: 연속시간."),
      (85, 220, 1010, 265, "x(t) = sin(t)는 기본 주기 T0 = 2π로 반복."),
      (215, 320, 1180, 610, "-6π부터 6π까지, 2π마다 같은 물결.")),
  steps("한 주기 따라가기",
      ["$\\sin 0=0$", "$\\sin(\\pi/2)=1$ (꼭대기)", "$\\sin\\pi=0$", "$\\sin(3\\pi/2)=-1$ (바닥)", "$\\sin 2\\pi=0$, 처음으로"],
      "$0 \\to 1 \\to 0 \\to -1 \\to 0$ 이 한 주기예요."),
  prof("사인은 2π가 기본 주기가 돼요."),
 ],
 "pass4": [
  check("sin t 의 기본 주기는?", ["$\\pi$", "$2\\pi$", "$4\\pi$"], 1, "$\\pi$ 뒤에는 부호가 반대라 주기가 아니에요."),
 ]})
assert abs(12 * PI / (2 * PI) - 6) < 1e-12

# =====================================================================
# p.19 짝수와 홀수 신호
# =====================================================================
S.append({"p": 19, "title": "1.2 짝수 신호와 홀수 신호",
 "pass1": [
  analogy("데칼코마니와 반 바퀴",
      "종이를 접어 물감을 찍으면 좌우가 똑같아요(데칼코마니). 어떤 그림은 가운데 점을 핀으로 꽂고 반 바퀴 돌려도 똑같아요.",
      ["세로축 거울 데칼코마니", K("even")], ["원점 중심 반 바퀴", K("odd")]),
  figure("cos 은 짝수, sin 은 홀수", FIG_EVENODD, "짝수는 좌우 거울, 홀수는 원점을 지나며 뒤집혀요.", 1),
 ],
 "pass2": [
  formula(K("even"), r"x(-t) = x(t)", [(r"x(-t)", f"{K('rev')}한 신호"), (r"= x(t)", "원래와 같아요")],
      "뒤집어도 그대로인 신호예요. 대표는 cos 이에요."),
  formula(K("odd"), r"x(-t) = -x(t)", [(r"-x(t)", "원래 신호를 위아래로 뒤집은 것")],
      "좌우로 뒤집으면 위아래까지 뒤집히는 신호예요. 대표는 sin 이에요."),
  compare("짝수와 홀수", ["", K("even"), K("odd")],
      ["대칭", "세로축 대칭", "원점 대칭"], ["$t=0$ 값", "아무 값이나", "꼭 0"], ["대표", "$\\cos t$", "$\\sin t$"]),
  check("$x(-t)=-x(t)$ 인 신호는?", [K("even"), K("odd")], 1, "마이너스가 붙으면 홀수(원점 대칭)예요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (200, 315, 430, 370, "짝수 신호 정의 x(-t) = x(t)."),
      (495, 255, 1060, 440, "짝수 그림: $t=0$ 을 기준으로 좌우 같아요."),
      (200, 570, 445, 625, "홀수 신호 정의 x(-t) = -x(t)."),
      (495, 510, 1060, 700, "홀수라고 붙은 그림: $t=0$ 에서 값이 약 0.75로 꼭대기예요. 홀수라면 0이어야 해요.")),
  steps("숫자로 확인",
      ["$\\cos(1)\\approx0.54$, $\\cos(-1)\\approx0.54$ → 같아요, 짝수",
       "$\\sin(1)\\approx0.84$, $\\sin(-1)\\approx-0.84$ → 부호만 반대, 홀수"],
      "cos 은 짝수, sin 은 홀수예요."),
  steps("홀수 신호는 왜 $t=0$에서 0인가",
      ["홀수 정의에 $t=0$을 넣어요: $x(-0)=-x(0)$",
       "$-0=0$ 이니 $x(0)=-x(0)$",
       "양변에 $x(0)$을 더하면 $2x(0)=0$"],
      "$x(0)=0$. 홀수 신호는 반드시 원점을 지나요."),
  prof("홀수 함수(기함수) 그림이 좀 잘못됐네요. 원점 대칭이라 0에서 0을 지나야 해요.",
      "사인 함수가 대표적인 홀수 함수이고, 코사인이 대표적인 짝수 함수예요."),
 ],
 "pass4": [
  warn("슬라이드 그림 오류 (교수님도 수업에서 인정)",
      "아래 '홀수' 그림은 $t=0$에서 꼭대기라서 실제로는 짝수 모양이에요.",
      "홀수 신호는 $t=0$에서 꼭 0이어야 해요. sin t 모양을 떠올리세요."),
  check("$x(t)=t^2$ 은?", [K("even"), K("odd"), "둘 다 아님"], 0, "$(-t)^2=t^2$ 이니 짝수예요."),
  english("답안 문장", "짝수 신호는 $x(-t)=x(t)$를, 홀수 신호는 $x(-t)=-x(t)$를 만족하며, 홀수 신호는 $x(0)=0$이다.",
      "대칭 기준: 짝수는 세로축, 홀수는 원점.", "cos 은 짝(짝꿍 거울), sin 은 홀(원점 돌리기)"),
 ]})

# =====================================================================
# p.20 짝홀 분해
# =====================================================================
S.append({"p": 20, "title": "1.2 짝홀 분해 (Even-Odd Decomposition)",
 "pass1": [
  say(f"어떤 신호든 짝수 부분 하나와 홀수 부분 하나의 합으로 나눌 수 있어요. 이것이 {K('eod')}예요.",
      "나누는 방법은 딱 한 가지뿐이에요."),
  figure("나누어 보기", FIG_EODEC, "왼쪽 신호 = 가운데 짝수 부분 + 오른쪽 홀수 부분.", 2),
 ],
 "pass2": [
  formula("짝수 부분", r"x_e[n] = \frac{1}{2}\left(x[n] + x[-n]\right)",
      [(r"x_e", "e 는 even, 짝수 부분"), (r"x[-n]", "뒤집은 신호"), (r"\frac12(\dots)", "원래와 뒤집은 것의 평균")],
      "원래와 거울상의 평균이라 좌우 대칭이 돼요."),
  formula("홀수 부분", r"x_o[n] = \frac{1}{2}\left(x[n] - x[-n]\right)",
      [(r"x_o", "o 는 odd, 홀수 부분"), (r"x[n]-x[-n]", "원래에서 거울상을 뺀 것")],
      "원래와 거울상의 차이의 절반이에요."),
  formula("다시 더하면 원래 신호", r"x[n] = x_e[n] + x_o[n]",
      [(r"+", "두 부분을 더하면 $x[-n]$ 항이 지워져요")], "짝수 부분 + 홀수 부분 = 원래 신호예요."),
  check("짝수 신호 $x$의 홀수 부분은?", ["$x$ 자신", "0", "$-x$"], 1,
      "짝수면 $x[-n]=x[n]$ 이라 $x_o=\\tfrac12(x[n]-x[n])=0$ 이에요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (110, 285, 470, 360, "짝수 부분 식."), (515, 285, 865, 360, "홀수 부분 식."), (945, 295, 1245, 345, "두 부분의 합 = x[n]."),
      (95, 385, 460, 640, "x_e[n] 그림: 음수 쪽 0, 양수 쪽 1. 가로축 눈금 2가 두 번 적혀 있어요."),
      (500, 385, 870, 640, "x_o[n] 그림: 음수 쪽 -1, 0에서 0, 양수 쪽 1."),
      (905, 385, 1275, 640, "x[n] 그림: 음수 쪽 -1, 0에서 0, 양수 쪽 1.")),
  steps("식이 나오는 과정 (교수님 유도)",
      ["$x[n]=x_e[n]+x_o[n]$ 이라고 둬요",
       "$n$ 대신 $-n$: $x[-n]=x_e[-n]+x_o[-n]=x_e[n]-x_o[n]$",
       "두 식을 더하면 $x[n]+x[-n]=2x_e[n]$",
       "두 식을 빼면 $x[n]-x[-n]=2x_o[n]$"],
      "2로 나누면 슬라이드의 두 식이 나와요."),
  steps("쉬운 예: $x[n]=1$ ($n\\ge0$), $x[n]=0$ ($n<0$)",
      ["$n=2$: $x[2]=1$, $x[-2]=0$",
       "$x_e[2]=\\tfrac12(1+0)=\\tfrac12$, $x_o[2]=\\tfrac12(1-0)=\\tfrac12$",
       "$n=-2$: $x_e[-2]=\\tfrac12$, $x_o[-2]=\\tfrac12(0-1)=-\\tfrac12$",
       "$n=0$: $x_e[0]=\\tfrac12(1+1)=1$, $x_o[0]=0$",
       "확인: $x_e[2]+x_o[2]=1$, $x_e[-2]+x_o[-2]=0$"],
      "짝수 부분은 1/2 (가운데만 1), 홀수 부분은 $\\pm1/2$ 예요."),
  steps("슬라이드의 $x[n]$ ($-1, 0, 1$ 모양)을 나누면",
      ["$n=1$: $x[1]=1$, $x[-1]=-1$",
       "$x_e[1]=\\tfrac12(1+(-1))=0$",
       "$x_o[1]=\\tfrac12(1-(-1))=1$"],
      "짝수 부분은 모두 0, 홀수 부분은 $x[n]$ 그대로예요. 이 $x[n]$은 원래 홀수 신호예요."),
  prof("짝수, 홀수 함수로 이루어져 있다고 가정하고 x[-n]을 넣어 두 식을 더하면 짝수 부분이 나와요.",
      "그런데 이 예시 신호는 사실 홀수 함수네요. 예시를 잘못 그려 놨어요."),
 ],
 "pass4": [
  warn("슬라이드 그림 주의",
      "슬라이드의 $x[n]$은 그 자체로 홀수 신호라서 짝수 부분은 0이어야 해요.",
      "그런데 $x_e[n]$ 그림은 양수 쪽만 1이라 좌우 대칭도 아니고, $x_e+x_o=x$ 도 맞지 않아요. 식을 믿으세요."),
  exam("슬라이드 p.20 식 응용 (기출 아님)", "$x[-1]=0$, $x[0]=2$, $x[1]=4$ 일 때 $n=1$, $n=-1$ 에서의 짝수 부분과 홀수 부분을 구하라.",
      "원래 값과 뒤집은 값의 평균, 차이의 절반이에요.",
      ["$x_e[1]=\\tfrac12(4+0)=2$, $x_o[1]=\\tfrac12(4-0)=2$",
       "$x_e[-1]=\\tfrac12(0+4)=2$, $x_o[-1]=\\tfrac12(0-4)=-2$",
       "확인: $2+2=4=x[1]$, $2+(-2)=0=x[-1]$"],
      "$x_e[\\pm1]=2$, $x_o[1]=2$, $x_o[-1]=-2$"),
  check("홀수 부분 $x_o[0]$은 언제나?", ["1", "0", "$x[0]$"], 1, "$x_o[0]=\\tfrac12(x[0]-x[0])=0$ 이에요."),
 ]})


# =====================================================================
# p.21 연속시간 복소 지수 신호
# =====================================================================
S.append({"p": 21, "title": "1.3 연속시간 복소 지수 신호 x(t) = Ce^{at}",
 "pass1": [
  say(f"지수 신호와 {K('sinus')}는 현실 신호를 잘 닮았고, 다른 신호를 만드는 기본 재료예요.",
      f"이 둘을 한 식으로 묶은 것이 {K('cexp')}예요.",
      "여기서부터 조금 어려워져요. 천천히 따라와요."),
 ],
 "pass2": [
  formula(K("cexp"), r"x(t) = C e^{at}",
      [(r"e", "약 2.718인 특별한 수"), (r"e^{at}", f"{K('expf')}. 시간이 지나면 일정한 비율로 커지거나 줄어요"),
       (r"C", "앞에 곱하는 수(처음 크기)"), (r"a", "변하는 빠르기와 방향을 정하는 수")],
      f"$C$와 $a$는 일반적으로 {K('cplx')}예요. 어떤 수냐에 따라 모양이 달라져요."),
  compare("$a$가 어떤 수인가에 따라 (다음 쪽들 미리 보기)", ["$a$", "모양", "쪽"],
      ["실수", "커지거나 줄어드는 곡선", "22쪽"], ["순허수 $j\\omega_0$", "출렁이는 사인파", "23쪽부터"],
      ["일반 복소수", "커지거나 줄면서 출렁임", "뒤쪽 레슨"]),
  check(f"{K('cexp')}에서 $C$와 $a$는 일반적으로?", ["정수", "실수만", "복소수"], 2, "슬라이드: In general, C and a are complex numbers."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (110, 240, 1230, 320, "지수와 사인 신호는 현실 신호의 특징이고, 다른 신호의 기본 재료(building block)예요."),
      (110, 350, 760, 460, "일반적인 복소 지수 신호 x(t) = Ce^{at}."),
      (110, 485, 630, 525, "C와 a는 일반적으로 복소수.")),
  steps("가장 쉬운 경우 $a=0$",
      ["$C=2$, $a=0$ 이라고 해요", "$e^{0\\cdot t}=e^0=1$", "$x(t)=2\\times1=2$"],
      "모든 시각에서 2인 상수 신호예요."),
  bg("기초 다지기 b-4 지수함수와 e",
      "$e^0=1$, $e^1\\approx2.718$, $e^{-1}\\approx0.368$ 이에요.", "지수가 0이면 항상 1이에요."),
  bg("기초 다지기 b-5 복소수와 복소평면",
      f"{K('cplx')}는 $a+jb$ 꼴이고, {K('imag')} $j$는 제곱하면 $-1$이에요."),
  prof("여기서부터 복소 지수 신호가 나와서 살짝 어려워질 수 있으니 조금 집중해 주세요.",
      "이렇게 생긴 신호가 있다고 가정하고 시작하는 거예요. C와 a는 둘 다 복소수가 될 수 있어요."),
 ],
 "pass4": [
  check("$x(t)=5e^{0t}$는?", ["항상 5인 상수", "커지는 곡선", "출렁이는 파"], 0, "$e^0=1$ 이니 $5\\times1=5$ 예요."),
 ]})

# =====================================================================
# p.22 실수 지수 신호
# =====================================================================
S.append({"p": 22, "title": "1.3 실수 지수 신호: C 와 a 가 실수",
 "pass1": [
  figure("커지는 지수, 줄어드는 지수", FIG_EXP, "a가 양수면 점점 커지고, 음수면 점점 줄어요.", 2),
  say(f"$C$와 $a$가 모두 실수면 {K('realexp')}예요.", "시간이 지나며 폭발하듯 커지거나, 0으로 조용히 줄어들어요."),
 ],
 "pass2": [
  formula(K("realexp"), r"x(t) = C e^{at},\quad C, a \in \mathbb{R}",
      [(r"a>0", "커져요(증가, growth)"), (r"a<0", "줄어요(감쇠, decay)"), (r"a=0", "상수 $C$"),
       (r"C>0", "그래프가 가로축 위쪽")],
      "$a$의 부호가 커질지 줄어들지를 정해요."),
  compare("$a$의 부호", ["$a$", "모양", "현실 예"],
      ["$a>0$", "점점 빨리 커짐", "평형에서 멀어지는 시스템"], ["$a<0$", "0으로 줄어듦", f"{K('rc')} 방전, 흔들림이 잦아듦"],
      ["$a=0$", "그대로 $C$", "상수 신호"]),
  check("$x(t)=3e^{-2t}$는?", ["커져요", "줄어요", "그대로예요"], 1, "$a=-2<0$ 이라 감쇠예요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (100, 200, 740, 240, "실수 지수 신호: C와 a가 실수."),
      (170, 360, 560, 690, "왼쪽: a > 0, C > 0, 지수 증가. 세로축 이름 exp(0.2t)."),
      (580, 360, 980, 690, "오른쪽: a < 0, C > 0, 지수 감쇠. 세로축 이름도 exp(0.2t)라고 적혀 있어요.")),
  steps("$e^{0.2t}$ 값 (왼쪽 그림)",
      ["$t=-10$: $e^{-2}\\approx0.14$", "$t=0$: $e^0=1$", "$t=10$: $e^{2}\\approx7.39$"],
      "그림에서 오른쪽 끝이 8에 가까이 가는 것과 맞아요."),
  steps("$e^{-0.2t}$ 값 (오른쪽 그림)",
      ["$t=-10$: $e^{2}\\approx7.39$", "$t=0$: 1", "$t=10$: $e^{-2}\\approx0.14$"],
      "왼쪽 그림을 좌우로 뒤집은 모양이에요. 사실 $e^{-0.2t}$는 $e^{0.2t}$의 시간 반전이에요."),
  say(f"{K('rc')}에서 축전기에 모인 전기가 빠져나갈 때도 이런 {K('expf')} 모양으로 줄어들어요.",
      f"그래서 감쇠하는 {K('realexp')}는 {K('rc')} 같은 시스템을 설명할 때 자주 나와요."),
  prof("a가 0보다 작으면 시간이 흐를수록 신호가 약해지는 감쇠 신호예요. RC 회로처럼 저항이나 마찰이 있으면 에너지가 약해져요.",
      "a가 0이면 C 값에 상관없이 상수 신호가 돼요."),
 ],
 "pass4": [
  warn("그림 이름표", "오른쪽 감쇠 그림의 세로축도 'exp(0.2t)'라고 적혀 있지만, 모양으로 보면 $e^{-0.2t}$예요."),
  check("$C=-1$, $a=0.5$ 이면 그래프는?", ["가로축 아래에서 아래로 점점 멀어져요", "위로 커져요", "0으로 줄어요"], 0,
      "$e^{0.5t}$는 커지는데 $C=-1$을 곱해 아래쪽(음수)으로 커져요."),
 ]})

# =====================================================================
# p.23 순허수 a, 오일러 공식, 주기성
# =====================================================================
S.append({"p": 23, "title": "1.3 주기 복소 지수 신호와 오일러 공식",
 "pass1": [
  analogy("원 위를 도는 점",
      "원 위를 일정한 빠르기로 도는 점을 떠올려요. 한 바퀴 돌면 제자리로 와서 같은 일이 반복돼요.",
      ["원 위를 도는 점", "$e^{j\\omega_0 t}$"], ["점의 가로 위치", "cos"], ["점의 세로 높이", "sin"], ["한 바퀴 시간", "주기 $T$"]),
  say(f"$a$가 허수이면 신호는 원을 도는 점이 돼요. 이걸 풀어 주는 식이 {K('euler')}예요.",
      f"교수님이 {K('euler','은')} 무조건 외우라고 했어요."),
 ],
 "pass2": [
  formula(K("euler"), r"e^{j\omega_0 t} = \cos\omega_0 t + j\sin\omega_0 t",
      [(r"j", f"{K('imag')}. $j^2=-1$ 이에요"), (r"\omega_0", f"{K('angf')}, 도는 빠르기"),
       (r"\cos\omega_0 t", "실수 부분(가로 위치)"), (r"j\sin\omega_0 t", "허수 부분(세로 높이)")],
      "허수 지수는 cos 과 sin 의 합이에요."),
  formula("왜 주기 신호인가", r"e^{j\omega_0 (t+T)} = \cos\omega_0 (t+T) + j\sin\omega_0 (t+T) = e^{j\omega_0 t}",
      [(r"t+T", "시간을 $T$만큼 옮겨요"), (r"T = 2\pi/\omega_0", "이만큼 옮기면 각도가 $2\\pi$ 늘어 한 바퀴")],
      f"cos, sin 이 반복하니 $e^{{j\\omega_0 t}}$도 {K('periodic')}예요. 주기 $T=2\\pi/\\omega_0$."),
  compare("i 와 j", ["", "수학", "이 과목(전기공학)"], ["허수 단위", "$i$", "$j$"], ["까닭", "보통 표기", "전류 $i$와 헷갈리지 않게"]),
  check(f"{K('euler')}를 바르게 쓴 것은?", ["$e^{j\\theta}=\\sin\\theta+j\\cos\\theta$", "$e^{j\\theta}=\\cos\\theta+j\\sin\\theta$", "$e^{j\\theta}=\\cos\\theta\\sin\\theta$"], 1,
      "cos 이 실수 부분, sin 이 허수 부분이에요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (175, 255, 735, 355, "a가 순허수(jω0)일 때 x(t) = Ce^{jω0t}."),
      (175, 375, 735, 475, "오일러 관계로 cos ω0t + j sin ω0t 로 풀어요."),
      (175, 500, 735, 630, "t 대신 t+T를 넣어도 같아서 주기 신호."),
      (755, 262, 1128, 578, "상자: 오일러 공식(i 로 표기)과 오일러 항등식 $e^{i\pi}+1=0$."),
      (780, 635, 1000, 680, "주기 T = 2π/ω0.")),
  steps("쉬운 숫자로 주기 확인: $\\omega_0=2$",
      ["$T=2\\pi/\\omega_0=2\\pi/2=\\pi$",
       "$e^{j2(t+\\pi)}=e^{j2t}\\,e^{j2\\pi}$",
       "$e^{j2\\pi}=\\cos2\\pi+j\\sin2\\pi=1+0j=1$",
       "그래서 $e^{j2(t+\\pi)}=e^{j2t}$"],
      "$\\omega_0=2$ 이면 주기는 $\\pi$예요."),
  steps("상자 아래 식, 오일러 항등식",
      ["$\\theta=\\pi$ 를 넣어요", "$e^{j\\pi}=\\cos\\pi+j\\sin\\pi=-1+0j=-1$", "양변에 1을 더하면 $e^{j\\pi}+1=0$"],
      "오일러 항등식은 오일러 공식에 $\\pi$를 넣은 것뿐이에요."),
  prof("여기서부터는 이 과목을 이해하려면 무조건 이해해야 하는 부분이에요.",
      "이 박스의 오일러 공식은 무조건 외워 두세요. 아래 식(항등식)은 아직 몰라도 돼요."),
  bg("기초 다지기 b-6 오일러 공식과 회전",
      "$e^{j\\theta}$는 각도 $\\theta$만큼 돈 단위원 위의 점이에요.", "$\\theta$가 커지면 점이 시계 반대 방향으로 돌아요."),
 ],
 "pass4": [
  prof("오일러 공식 e^{jφ} = cos φ + j sin φ 는 증명은 몰라도 되지만 공식은 무조건 외워야 해요."),
  english("외울 식", "$e^{j\\theta}=\\cos\\theta+j\\sin\\theta$ 이고, 따라서 $e^{j\\omega_0 t}$는 주기 $T_0=2\\pi/\\omega_0$인 주기 신호이다.",
      "지수(회전)와 사인파를 잇는 다리예요.", "코-플-제-사: cos 더하기 j sin"),
  warn("표기 주의", "슬라이드 오른쪽 상자는 수학식 그대로 $i$를 썼어요. 이 과목에서는 같은 것을 $j$로 써요."),
  check("$e^{j\\omega_0 t}$에서 $\\omega_0=4$ 이면 주기는?", ["$\\pi/2$", "$2\\pi$", "$4\\pi$"], 0, "$2\\pi/4=\\pi/2$ 예요."),
 ]})
assert abs(2 * PI / 4 - PI / 2) < 1e-12

# =====================================================================
# p.24 테일러 급수로 본 오일러 공식
# =====================================================================
S.append({"p": 24, "title": "1.3 오일러 공식은 어디서 왔나: 테일러 급수",
 "pass1": [
  say(f"이 쪽은 {K('euler')}가 왜 맞는지 보여 주는 증명이에요.",
      "교수님: 증명은 외울 필요 없어요. 공식만 꼭 외우세요."),
  points("증명 줄거리 세 줄",
      f"$e^x$, $\\cos x$, $\\sin x$ 를 모두 1, $x$, $x^2$, ... 의 합으로 풀어 써요({K('taylor')})",
      "$e^x$의 $x$ 자리에 $jx$를 넣어요",
      "짝수 번째 항은 cos, 홀수 번째 항은 j sin 이 돼요"),
 ],
 "pass2": [
  formula(f"{K('taylor')}로 쓴 $e^x$", r"e^x = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \frac{x^4}{4!} + \cdots",
      [(r"n!", "팩토리얼. $3!=3\\times2\\times1=6$"), (r"\cdots", "끝없이 계속 더해요"),
       (r"\frac{x^n}{n!}", "항 하나. 뒤로 갈수록 아주 작아져요")],
      "함수를 거듭제곱들의 합으로 바꿔 쓴 거예요."),
  formula("cos 과 sin 도", r"\cos x = 1 - \frac{x^2}{2!} + \frac{x^4}{4!} - \cdots,\quad \sin x = x - \frac{x^3}{3!} + \frac{x^5}{5!} - \cdots",
      [(r"\cos x", "짝수 제곱만, 부호가 번갈아"), (r"\sin x", "홀수 제곱만, 부호가 번갈아")],
      "cos 은 짝수 차수, sin 은 홀수 차수 항만 가져요."),
  check("증명에서 시험 전에 꼭 외울 것은?", ["테일러 급수 전개 전부", "$e^{jx}=\\cos x+j\\sin x$ 결과", "팩토리얼 표"], 1,
      "교수님: 증명은 외울 필요 없고 오일러 공식은 무조건 외워요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (110, 190, 600, 265, "오일러 공식의 출처: 테일러 급수."),
      (125, 280, 990, 360, "sin x 의 급수."), (125, 375, 990, 455, "cos x 의 급수."),
      (125, 475, 700, 550, "e^x 의 급수."), (125, 570, 700, 610, "x 대신 ix 를 넣어요(i = √-1)."),
      (125, 620, 700, 705, "e^{ix} 의 급수.")),
  steps("급수가 정말 맞나: $e^1$",
      ["$1+1=2$", "$+\\tfrac{1}{2!}=+0.5$ → 2.5", "$+\\tfrac{1}{3!}\\approx+0.1667$ → 2.667",
       "$+\\tfrac{1}{4!}\\approx+0.0417$ → 2.708", "진짜 $e\\approx2.718$ 에 다가가요"],
      "항을 더할수록 정확해져요."),
  steps("$j$의 거듭제곱",
      ["$j^1=j$", "$j^2=-1$", "$j^3=j^2\\cdot j=-j$", "$j^4=(j^2)^2=1$, 다시 처음으로"],
      "4번마다 반복해요: $j, -1, -j, 1$."),
  steps("$e^{jx}$ 를 두 무리로 나누기",
      ["$e^{jx}=1+jx+\\frac{(jx)^2}{2!}+\\frac{(jx)^3}{3!}+\\frac{(jx)^4}{4!}+\\cdots$",
       "짝수 항: $1-\\frac{x^2}{2!}+\\frac{x^4}{4!}-\\cdots=\\cos x$",
       "홀수 항: $jx-j\\frac{x^3}{3!}+\\cdots=j(x-\\frac{x^3}{3!}+\\cdots)=j\\sin x$",
       "합치면 $e^{jx}=\\cos x+j\\sin x$"],
      f"{K('euler')}가 나왔어요."),
  prof("테일러 급수는 어떤 함수든 다항식의 합으로 표현하는 거예요. 무한히 더하면 오차가 0으로 줄어 등호가 성립해요.",
      "좀 어렵죠. 증명까지 외울 필요는 없는데, 오일러 공식은 무조건 외워 두셔야 해요."),
 ],
 "pass4": [
  warn("시험 대비 요점", "증명 과정(급수 전개)은 외우지 않아도 돼요.", "결과 $e^{j\\theta}=\\cos\\theta+j\\sin\\theta$는 꼭 외워요."),
  check("$j^3$은?", ["$j$", "$-1$", "$-j$"], 2, "$j^3=j^2\\cdot j=-1\\cdot j=-j$ 예요."),
 ]})
assert (1j) ** 3 == -1j

# =====================================================================
# p.25 주기, 각주파수, 주파수
# =====================================================================
S.append({"p": 25, "title": "1.3 주기, 각주파수, 주파수",
 "pass1": [
  figure("단위원 위의 네 점", FIG_UC, "각도 0, π/2, π, 3π/2 에서 값이 1, j, -1, -j 예요.", 2),
  say("점이 원을 한 바퀴 도는 시간이 주기, 1초에 도는 각도가 각주파수, 1초에 도는 바퀴 수가 주파수예요."),
 ],
 "pass2": [
  formula("주기", r"T = \frac{2\pi}{\omega_0}", [(r"2\pi", "한 바퀴 각도"), (r"\omega_0", "1초에 도는 각도")],
      "한 바퀴를 빠르기로 나누면 한 바퀴 걸리는 시간이에요."),
  formula(K("angf"), r"\omega_0 = \frac{2\pi}{T}", [(r"\omega_0", "단위 rad/s, 1초에 몇 라디안")],
      "한 바퀴 각도를 한 바퀴 시간으로 나눠요."),
  formula(K("freq"), r"f_0 = \frac{\omega_0}{2\pi} = \frac{1}{T}", [(r"f_0", "1초에 몇 바퀴(몇 번 반복), 단위 Hz")],
      "주기의 역수예요."),
  compare("세 가지 구별", ["이름", "기호", "단위", "뜻"],
      ["주기", "$T$", "초(s)", "한 번 반복 시간"], [K("angf"), "$\\omega_0$", "rad/s", "1초에 도는 각도"],
      [K("freq"), "$f_0$", "Hz", "1초에 반복 횟수"]),
  check("$\\omega_0=2\\pi f_0$ 에서 $f_0=1$ Hz 이면 $\\omega_0$는?", ["1 rad/s", "$2\\pi$ rad/s", "$\\pi$ rad/s"], 1, "$2\\pi\\times1=2\\pi$ 예요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (215, 255, 650, 370, "e^{jω0t} = cos + j sin, 그리고 Ae^{j(ω0t+φ)} = Ae^{jφ}e^{jω0t}."),
      (215, 405, 480, 490, "주기 T = 2π/ω0."), (215, 490, 650, 570, "각주파수 ω0 = 2π/T. 단위가 (rad)로 적혀 있어요."),
      (215, 575, 640, 650, "주파수 f0 = ω0/2π = 1/T (Hz)."),
      (700, 255, 1170, 625, "단위원: e^{j0}=1, e^{jπ/2}=j, e^{jπ}=-1, e^{j3π/2}=-j."),
      (835, 660, 975, 705, "질문: e^{jπ/4}는?")),
  steps("오일러 공식으로 네 점 확인",
      ["$e^{j0}=\\cos0+j\\sin0=1$", "$e^{j\\pi/2}=\\cos\\frac{\\pi}{2}+j\\sin\\frac{\\pi}{2}=0+j=j$",
       "$e^{j\\pi}=-1+0j=-1$", "$e^{j3\\pi/2}=0-j=-j$", "$e^{j2\\pi}=1$, 한 바퀴 돌아 처음으로"],
      "각도를 넣고 cos, sin 값만 읽으면 돼요."),
  steps("슬라이드 질문 $e^{j\\pi/4}$",
      ["$\\pi/4$는 45도", "$\\cos45^\\circ=\\sin45^\\circ=\\frac{\\sqrt2}{2}\\approx0.707$",
       "$e^{j\\pi/4}=\\frac{\\sqrt2}{2}+j\\frac{\\sqrt2}{2}$"],
      "약 $0.707+0.707j$, 1과 $j$의 딱 가운데 점이에요."),
  steps("$T$, $\\omega_0$, $f_0$ 손계산: $\\omega_0=4\\pi$",
      ["$T=2\\pi/4\\pi=0.5$ 초", "$f_0=4\\pi/2\\pi=2$ Hz", "확인: $1/T=1/0.5=2$"],
      "0.5초에 한 바퀴, 1초에 두 바퀴예요."),
  say("$Ae^{j(\\omega_0 t+\\phi)}=Ae^{j\\phi}e^{j\\omega_0 t}$ 는 지수법칙 $e^{a+b}=e^ae^b$ 로 나눈 거예요.",
      f"$\\phi$는 {K('phase')}, 출발 각도예요."),
  prof("j가 i예요. 전기공학에서는 전류를 i로 쓰니까 헷갈리지 않게 허수를 j로 많이 써요.",
      "t가 0이면 실수 부분 1, 허수 부분 0이라 (1, 0)에 찍혀요. 90도, 즉 π/2면 (0, 1)이에요."),
  prof("여기 각주파수 단위가 좀 잘못 쓰여 있는데, rad/s(라디안 퍼 세컨드)가 맞아요.",
      "주파수 개념은 뒤에서 다시 나오니 지금은 알아만 두세요."),
 ],
 "pass4": [
  warn("슬라이드 표기 오류 (교수님 정정)", "'Angular frequency (rad)'라고 적혀 있지만 단위는 rad/s 예요. $\\omega_0 t$가 라디안이 되려면 $\\omega_0$는 rad/s 여야 해요."),
  exam("슬라이드 p.25 질문 (기출 아님)", "e^{jπ/4} 를 a + jb 꼴로 쓰라.", "각도 45도의 cos, sin 값을 읽어요.",
      ["오일러: $e^{j\\pi/4}=\\cos\\frac{\\pi}{4}+j\\sin\\frac{\\pi}{4}$", "$\\cos\\frac{\\pi}{4}=\\sin\\frac{\\pi}{4}=\\frac{\\sqrt2}{2}$"],
      "$\\frac{\\sqrt2}{2}+j\\frac{\\sqrt2}{2}\\approx0.707+0.707j$"),
  check("주기 $T=0.25$ 초이면 주파수는?", ["0.25 Hz", "4 Hz", "$8\\pi$ Hz"], 1, "$f_0=1/T=1/0.25=4$ Hz 예요."),
 ]})
assert 1 / 0.25 == 4 and 2 * PI * 1 == 2 * PI


# =====================================================================
# p.26 단위원
# =====================================================================
S.append({"p": 26, "title": "1.3 단위원: e^{jω} 가 사는 곳",
 "pass1": [
  analogy("원 위의 점 하나",
      "반지름 1인 원 위에 점이 하나 있어요. 각도만 알려 주면 점의 자리가 정해져요.",
      ["반지름 1인 원", K("ucirc")], ["각도", "$\\omega$"], ["원 위의 점", "$e^{j\\omega}$"]),
  say(f"$e^{{j\\omega}}$는 언제나 {K('ucirc')} 위의 한 점이에요. $\\omega$는 그 점의 각도예요."),
 ],
 "pass2": [
  points("그림 속 말 읽기",
      f"z-plane: {K('cplane')}. 가로 Re는 실수 부분, 세로 Im은 허수 부분",
      "$|z|=1$: 원점에서 거리가 1, 즉 단위원",
      "$\\omega$: 가로축(오른쪽)에서 시계 반대 방향으로 잰 각도",
      "$\\omega=\\pi$ 와 $\\omega=-\\pi$ 는 같은 점 $-1$"),
  check("$e^{j\\omega}$의 크기 $|e^{j\\omega}|$는?", ["$\\omega$", "1", "0"], 1, "단위원 위의 점이라 원점까지 거리는 늘 1이에요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (110, 190, 1110, 275, "e^{jω}는 늘 복소평면 단위원 위의 점, ω는 각도."),
      (520, 330, 660, 390, "ω = π/2 → j (위)."), (430, 530, 590, 590, "ω = π = -π → -1 (왼쪽)."),
      (870, 525, 1000, 585, "$\\omega=0$ → $1$ (오른쪽)."), (520, 640, 660, 700, "ω = -π/2 → -j (아래)."),
      (840, 360, 1010, 440, "일반 각도 ω의 점 z = e^{jω}.")),
  steps("크기가 늘 1인 까닭 ($\\omega=\\pi/3$ 예)",
      ["점의 좌표는 $(\\cos\\omega, \\sin\\omega)$",
       "$\\cos(\\pi/3)=0.5$, 제곱 0.25", "$\\sin(\\pi/3)\\approx0.866$, 제곱 0.75",
       "거리의 제곱 $=0.25+0.75=1$"],
      "$\\cos^2+\\sin^2=1$ 이라 어떤 각도든 거리는 1이에요."),
  steps("음수 각도",
      ["$\\omega=-\\pi/2$: 시계 방향으로 90도", "$e^{-j\\pi/2}=\\cos(-\\frac{\\pi}{2})+j\\sin(-\\frac{\\pi}{2})=0-j$"],
      "$-j$, 즉 $e^{j3\\pi/2}$와 같은 점이에요."),
  prof("이 슬라이드는 신호가 아니라, 복소수를 각도로 나타내는 표현을 설명하려는 슬라이드예요.",
      "각이 0라디안이면 (1, 0)에 찍혀요."),
 ],
 "pass4": [
  check("$e^{j2\\pi}$는 어느 점인가요?", ["1", "$-1$", "$j$"], 0, "한 바퀴 돌아 출발점 1로 돌아와요."),
  warn("주의", "각도 단위는 도(degree)가 아니라 라디안이에요. $\\pi/2$가 90도예요."),
 ]})

# =====================================================================
# p.27 사인파 신호, 실수 부분과 허수 부분
# =====================================================================
S.append({"p": 27, "title": "1.3 사인파 신호와 Re, Im",
 "pass1": [
  say(f"복소 지수와 아주 가까운 친구가 {K('sinus')}예요. cos 모양으로 출렁여요.",
      "복소 지수에서 실수 부분만 꺼내면 cos, 허수 부분만 꺼내면 sin 이에요."),
 ],
 "pass2": [
  formula(K("sinus"), r"x(t) = \cos(\omega_0 t + \phi),\quad \omega_0 = 2\pi f_0",
      [(r"\omega_0", f"{K('angf')}. 클수록 빨리 출렁여요"), (r"\phi", f"{K('phase')}. 출발 각도"),
       (r"f_0", f"{K('freq')}, 1초에 몇 번")],
      "각도 $\\omega_0 t+\\phi$의 cos 값이 시간에 따라 출렁이는 신호예요."),
  formula("복소 지수에서 꺼내기", r"A\cos(\omega_0 t+\phi) = A\,\mathrm{Re}\{e^{j(\omega_0 t+\phi)}\},\quad A\sin(\omega_0 t+\phi) = A\,\mathrm{Im}\{e^{j(\omega_0 t+\phi)}\}",
      [(r"\mathrm{Re}\{\cdot\}", "실수 부분만 꺼내기"), (r"\mathrm{Im}\{\cdot\}", "허수 부분만 꺼내기(j는 떼고)"),
       (r"A", f"{K('amp')}")],
      "오일러 공식의 cos 쪽이 실수 부분, sin 쪽이 허수 부분이라서예요."),
  check("$\\mathrm{Im}\\{e^{j\\theta}\\}$는?", ["$\\cos\\theta$", "$\\sin\\theta$", "$j\\sin\\theta$"], 1, "허수 부분은 $j$를 뗀 $\\sin\\theta$ 예요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (135, 270, 740, 395, "사인파 신호 x(t) = cos(ω0t + φ), ω0 = 2πf0."),
      (160, 420, 740, 600, "A cos 은 Re, A sin 은 Im 으로 복소 지수에서 꺼낼 수 있어요."),
      (740, 290, 1270, 640, "예: cos(2t + 1) 그래프. $t=0$ 값이 cos(1)."),
      (890, 640, 1080, 680, "T0 = 2π/ω0 = π.")),
  steps("그래프 예 $\\cos(2t+1)$",
      ["$\\omega_0=2$", "$T_0=2\\pi/2=\\pi\\approx3.14$", "$t=0$: $\\cos(1)\\approx0.54$",
       "그림에서 바닥과 바닥 사이도 약 3.14"],
      "주기 $\\pi$, 출발 값 약 0.54예요."),
  steps("Re, Im 손계산: $A=3$, $\\omega_0 t+\\phi=\\pi/2$ 인 순간",
      ["$3e^{j\\pi/2}=3(\\cos\\frac{\\pi}{2}+j\\sin\\frac{\\pi}{2})=3(0+j)=3j$",
       "Re 는 0, 즉 $3\\cos\\frac{\\pi}{2}=0$", "Im 은 3, 즉 $3\\sin\\frac{\\pi}{2}=3$"],
      "cos 쪽 값과 sin 쪽 값이 각각 Re, Im 으로 나와요."),
  prof("Re는 실수 부분을 꺼내는 함수, Im은 허수 부분을 꺼내는 함수예요.",
      "cos 도 sin 도 모두 지수 신호로 쓸 수 있어요. 둘은 사실 같은 것을 표현한다고 볼 수 있어요."),
 ],
 "pass4": [
  check("$x(t)=\\cos(4t+1)$ 의 주기는?", ["$\\pi/2$", "$4\\pi$", "1"], 0, "$T_0=2\\pi/4=\\pi/2$ 예요."),
  english("답안 문장", "$A\\cos(\\omega_0 t+\\phi)=A\\,\\mathrm{Re}\\{e^{j(\\omega_0 t+\\phi)}\\}$ 이고 주기는 $T_0=2\\pi/\\omega_0$이다.",
      "사인파는 복소 지수의 실수 부분이에요.", "Re 는 cos, Im 은 sin"),
 ]})

# =====================================================================
# p.28 원과 A cos(ω0 t + φ)
# =====================================================================
S.append({"p": 28, "title": "1.3 단위원과 사인파 x(t) = A cos(ω0 t + φ)",
 "pass1": [
  analogy("점과 그림자",
      "원 위를 도는 점에 빛을 비추면 가로축에 그림자가 생겨요. 그림자는 왔다 갔다 출렁여요.",
      ["원 위를 도는 점", "$e^{j\\phi}$"], ["가로 그림자 위치", "$\\cos\\phi$"], ["세로 높이", "$\\sin\\phi$"]),
 ],
 "pass2": [
  points("그림 읽기",
      "왼쪽: 각도 $\\phi$의 점. 가로 길이 $\\cos\\phi$, 세로 길이 $\\sin\\phi$",
      f"오른쪽: 최고 높이가 $A$({K('amp')})인 출렁임",
      "$t=0$ 에서 값 $A\\cos\\phi$: 출발 각도가 $\\phi$라서",
      "봉우리 사이 간격 $T_0=2\\pi/\\omega_0$"),
  check("$x(t)=A\\cos(\\omega_0 t+\\phi)$에서 $t=0$ 값은?", ["$A$", "$A\\cos\\phi$", "0"], 1, "$t=0$ 을 넣으면 $A\\cos\\phi$ 예요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (170, 265, 590, 640, "단위원 위 각도 φ의 점: e^{jφ} = cos φ + i sin φ (i 로 표기)."),
      (630, 255, 1245, 660, "A cos(ω0t + φ) 그래프: 높이 A, $t=0$ 값 $A\cos\phi$, 주기 $T_0=2\pi/\omega_0$.")),
  steps("쉬운 숫자: $A=2$, $\\phi=\\pi/3$, $\\omega_0=\\pi$",
      ["$t=0$ 값: $2\\cos(\\pi/3)=2\\times0.5=1$", "최고 높이: 2", "주기: $2\\pi/\\pi=2$ 초"],
      "1에서 출발해 높이 2로 출렁이고 2초마다 반복해요."),
  bg("기초 다지기 b-3 각도, 라디안, 사인과 코사인", "$\\cos(\\pi/3)=0.5$, $\\sin(\\pi/3)\\approx0.866$ 이에요."),
 ],
 "pass4": [
  warn("그림의 위상 부호",
      "식대로라면 $\\phi>0$ 일 때 $t=0$ 직후 값은 내려가요. 그림은 올라가니 $\\phi$가 음수인 경우로 보면 맞아요.",
      "위상 부호는 그림보다 식으로 확인하세요(다음 쪽 참고)."),
 ]})

# =====================================================================
# p.29 원을 돌면 사인파
# =====================================================================
S.append({"p": 29, "title": "1.3 원을 도는 점이 그리는 사인파",
 "pass1": [
  figure("도는 점의 높이 = sin", FIG_SPIN, "점이 원을 돌 때 높이를 시간 순서로 그리면 사인파예요.", 2),
  say("원을 빨리 돌수록 파도가 촘촘해져요.", f"도는 빠르기가 {K('angf')} $\\omega$예요."),
 ],
 "pass2": [
  formula("세 양의 관계", r"\omega = \frac{2\pi}{T} = 2\pi f,\quad T = \frac{1}{f} = \frac{2\pi}{\omega},\quad f = \frac{1}{T} = \frac{\omega}{2\pi}",
      [(r"\omega", K("angf")), (r"T", "주기"), (r"f", K("freq"))], "하나를 알면 나머지 둘이 나와요."),
  compare("$y=A\\sin(B(x+C))+D$ 의 네 글자 (오른쪽 아래 그림)", ["글자", "하는 일", "그림 이름표"],
      ["A", "위아래 높이", "Amplitude"], ["B", "주기 $2\\pi/B$ 를 정함", "Period"],
      ["C", "옆으로 옮김", "Phase Shift Left"], ["D", "통째로 위아래 이동", "Vertical Shift"]),
  check("$B$가 커지면?", ["주기가 길어져요", "주기가 짧아져요", "높이가 커져요"], 1, "주기 $2\\pi/B$ 라서 $B$가 크면 짧아져요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (240, 255, 880, 540, "왼쪽 원 위의 점(각도 φ, 빠르기 ω)과 오른쪽 A cos(ωt + φ) 파형. 봉우리 옆에 φ/ω 표시."),
      (905, 275, 1110, 475, "ω = 2π/T = 2πf, T = 1/f = 2π/ω, f = 1/T = ω/2π."),
      (865, 495, 1110, 640, "A sin(B(x + C)) + D: 진폭, 주기, 위상 이동, 세로 이동."),
      (85, 670, 1040, 705, "원을 ω로 돌면 세로 그림자가 사인파를 그려요.")),
  steps("주기에서 나머지 구하기: $T=0.5$ 초",
      ["$f=1/0.5=2$ Hz", "$\\omega=2\\pi f=4\\pi$ rad/s", "확인: $2\\pi/\\omega=2\\pi/4\\pi=0.5$"],
      "$f=2$, $\\omega=4\\pi$ 예요."),
  steps("$y=3\\sin(2(x+1))+1$ 읽기",
      ["$A=3$: 높이 3", "$B=2$: 주기 $2\\pi/2=\\pi$", "$C=1$: 왼쪽으로 1", "$D=1$: 위로 1"],
      "진폭 3, 주기 $\\pi$, 왼쪽 1, 위로 1이에요."),
  prof("사인 앞의 A는 진폭(amplitude)이라 높낮이를 정해요. B는 앞에서 배운 스케일링처럼 폭, 즉 주기를 정해요.",
      "C는 시프트, D는 함수 전체를 위아래로 띄우는 오프셋이에요. 개념적으로 이해하면 돼요."),
 ],
 "pass4": [
  warn("부호 주의 (그림과 식이 어긋나 보이는 곳)",
      "$A\\cos(\\omega t+\\phi)=A\\cos(\\omega(t+\\phi/\\omega))$ 라서 $\\phi>0$ 이면 왼쪽으로 $\\phi/\\omega$ 옮겨져요(오른쪽 아래 그림 'Phase Shift Left'와 같아요).",
      "그런데 가운데 그림은 봉우리를 $t=+\\phi/\\omega$ 에 그렸어요. 이것은 $\\cos(\\omega t-\\phi)$ 모양이에요.",
      "시험에서는 식으로 판단하세요. 교수님 강조: 시간 이동은 부호가 중요해요."),
  check("$\\cos(t+\\pi/2)$는 $\\cos t$를 어느 쪽으로 옮긴 것인가요?", ["오른쪽 $\\pi/2$", "왼쪽 $\\pi/2$"], 1, "더하기는 왼쪽(앞당김)이에요. 10쪽 시간 이동과 같아요."),
 ]})

# =====================================================================
# p.30 세 사인파
# =====================================================================
S.append({"p": 30, "title": "1.3 각주파수가 다른 세 사인파",
 "pass1": [
  figure("빠르기가 다른 세 파도", FIG_THREE, "ω가 클수록 촘촘하고 주기가 짧아요.", 2),
  say(f"{K('angf')}가 클수록 빨리 출렁이고, 주기는 짧아져요."),
 ],
 "pass2": [
  formula("ω 와 T 는 반비례", r"T = \frac{2\pi}{\omega}", [(r"\omega\uparrow", "분모가 커지면"), (r"T\downarrow", "주기는 작아져요")],
      "빨리 돌면 한 바퀴 시간이 짧아요."),
  points("슬라이드 결론", "$\\omega_1>\\omega_2>\\omega_3$ 이면 $T_1<T_2<T_3$", "주파수가 낮아질수록 파도가 느슨해져요"),
  check("$\\omega$가 2배가 되면 주기는?", ["2배", "절반", "그대로"], 1, "$T=2\\pi/\\omega$ 라서 절반이에요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (320, 255, 830, 385, "x1(t) = cos ω1t: 가장 촘촘."), (320, 390, 830, 515, "x2(t) = cos ω2t: 중간."),
      (320, 520, 830, 645, "x3(t) = cos ω3t: 가장 느슨."), (840, 435, 965, 475, "ω1 > ω2 > ω3, T1 < T2 < T3."),
      (85, 675, 920, 715, "주파수가 줄어드는 세 사인파.")),
  steps("$\\omega=4, 2, 1$ 로 계산",
      ["$\\omega_1=4$: $T_1=2\\pi/4\\approx1.57$", "$\\omega_2=2$: $T_2=2\\pi/2\\approx3.14$", "$\\omega_3=1$: $T_3=2\\pi\\approx6.28$"],
      "$T_1<T_2<T_3$, 슬라이드 결론과 같아요."),
  prof("오메가가 커지면 커질수록 t가 조금만 가도 2π가 금방 차니까 주기가 좁아져요.",
      "오메가가 작을수록 주기가 길어진 그래프가 돼요."),
 ],
 "pass4": [
  check("$\\cos3t$, $\\cos t$, $\\cos5t$ 중 주기가 가장 긴 것은?", ["$\\cos3t$", "$\\cos t$", "$\\cos5t$"], 1, "$\\omega$가 가장 작은 $\\cos t$ 가 주기 $2\\pi$로 가장 길어요."),
  recap(f"{K('ct')}는 $x(t)$, {K('dt')}는 $x[n]$. 에너지는 $|x|^2$를 모은 것",
        f"$x(t-t_0)$는 $t_0>0$ 이면 오른쪽({K('delay')}). 부호 꼭 기억",
        "섞인 변환은 $a$로 묶어 ① 뒤집기, 늘이기 ② $-b/a$ 옮기기",
        f"{K('euler')}: $e^{{j\\theta}}=\\cos\\theta+j\\sin\\theta$ 는 무조건 외우기",
        "$T=2\\pi/\\omega_0$, $f_0=1/T$, $\\omega$가 크면 주기가 짧아요"),
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
    gl = []
    for s in S:
        body = " ".join(_text([s.get(f"pass{i}", []) for i in range(1, 5)]))
        terms = []
        for key in TERMS:
            if disp(key) in body:
                terms.append(TERMS[key][1])
                if key not in gl:
                    gl.append(key)
        s["terms"] = terms
    out = {"deck": "S2", "from": 1, "to": 30, "glossary": [gloss_entry(k) for k in gl],
           "slides": [{"p": s["p"], "title": s["title"], "terms": s["terms"],
                       **{f"pass{i}": s.get(f"pass{i}", []) for i in range(1, 5)}} for s in S]}
    raw = json.dumps(out, ensure_ascii=False, indent=1)
    for ch in BAD:
        if ch in raw:
            i = raw.index(ch)
            raise ValueError(f"금지 문자 {ch!r}: {raw[max(0, i - 40):i + 10]}")
    assert [s["p"] for s in out["slides"]] == list(range(1, 31))
    with open(OUT, "w", encoding="utf-8") as fp:
        fp.write(raw)
    print(f"저장 {OUT}: 쪽 {len(S)}, 용어 {len(gl)}")


if __name__ == "__main__":
    build()
