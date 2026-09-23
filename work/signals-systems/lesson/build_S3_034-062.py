# -*- coding: utf-8 -*-
# S3 (3주차, 2장 LTI Systems) 회독 레슨 PDF 34~62쪽 생성기. 사용: python build_S3_034-062.py
import json, math, os, re, sys
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "S3_034-062.json")
DICT = json.load(open(os.path.join(HERE, "..", "rules", "용어사전.json"), encoding="utf-8"))

# ---------------- 용어 ----------------
TERMS = {
    "sig": ("신호", "Signal"), "sys": ("시스템", "System"),
    "ct": ("연속시간 신호", "Continuous-Time Signal"), "dt": ("이산시간 신호", "Discrete-Time Signal"),
    "imp": ("단위 임펄스", "Unit Impulse"), "step": ("단위 계단", "Unit Step"),
    "sift": ("선별 성질", "Sifting Property"), "ir": ("임펄스 응답", "Impulse Response"),
    "conv": ("컨볼루션", "Convolution"), "csum": ("컨볼루션 합", "Convolution Sum"),
    "cint": ("컨볼루션 적분", "Convolution Integral"),
    "lti": ("LTI 시스템", "Linear Time-Invariant System"),
    "lin": ("선형성", "Linearity"), "ti": ("시불변성", "Time Invariance"), "sup": ("중첩 원리", "Superposition"),
    "integ": ("적분", "Integral"), "summ": ("시그마 기호", "Summation"),
    "comm": ("교환 법칙", "Commutative Property"), "dist": ("분배 법칙", "Distributive Property"),
    "assoc": ("결합 법칙", "Associative Property"),
    "par": ("병렬 연결", "Parallel Interconnection"), "ser": ("직렬 연결", "Series Interconnection"),
    "mem": ("기억성", "Memory"), "memless": ("무기억 시스템", "Memoryless System"),
    "inv": ("가역성", "Invertibility"), "invsys": ("역시스템", "Inverse System"), "ident": ("항등 시스템", "Identity System"),
    "shift": ("시간 이동", "Time Shift"), "rev": ("시간 반전", "Time Reversal"),
    "expf": ("지수함수", "Exponential Function"), "geo": ("등비급수", "Geometric Series"),
    "filt": ("필터", "Filter"), "noise": ("잡음", "Noise"), "deriv": ("미분", "Derivative"),
}


def disp(key):
    ko, en = TERMS[key]
    return f"**{ko}({en})**"


JOSA = {"은": ("은", "는"), "이": ("이", "가"), "을": ("을", "를"), "과": ("과", "와"),
        "이에요": ("이에요", "예요"), "이고": ("이고", "고"), "이나": ("이나", "나"), "이죠": ("이죠", "죠"),
        "이라는": ("이라는", "라는"), "이라고": ("이라고", "라고"), "이랑": ("이랑", "랑")}


def K(key, josa=""):
    s = disp(key)
    if not josa:
        return s
    c = TERMS[key][0][-1]
    jong = (ord(c) - 0xAC00) % 28
    if josa == "으로":
        return s + ("로" if jong in (0, 8) else "으로")
    if josa in JOSA:
        return s + (JOSA[josa][0] if jong else JOSA[josa][1])
    return s + josa


PH = re.compile(r"\[\[(\w+)(?::([^\]]+))?\]\]")


def T(o):
    if isinstance(o, str):
        return PH.sub(lambda m: K(m.group(1), m.group(2) or ""), o)
    if isinstance(o, list):
        return [T(x) for x in o]
    if isinstance(o, dict):
        return {k: (v if k in ("svg", "tex", "sym") else T(v)) for k, v in o.items()}
    return o


def gloss_entry(key):
    ko, en = TERMS[key]
    for d in DICT:
        if d.get("ko") == ko and d.get("en") == en:
            g = {"ko": ko, "en": en, "say": d["say"]}
            if d.get("more"):
                g["more"] = d["more"]
            return g
    raise KeyError(key)


M1 = "[[sig:은]] 시간에 따라 변하는 값, [[sys:은]] 신호를 바꾸는 상자예요."
M2a = "[[lti:은]] [[ir]] 하나만 알면 돼요."
M2b = "출력은 뒤집고, 밀고, 곱하고, 더해서([[conv]]) 구해요."
WHEN = "3주차 목요일 수업"
B8 = "기초 다지기 b-8 적분은 넓이, 미분은 기울기"

# ---------------- 장면 ----------------
def say(*l): return {"kind": "say", "lines": list(l)}
def points(h, *i): return {"kind": "points", "head": h, "items": list(i)}
def analogy(h, sc, *p): return {"kind": "analogy", "head": h, "scene": sc, "map": [list(x) for x in p]}
def compare(h, cols, *rows): return {"kind": "compare", "head": h, "cols": list(cols), "rows": [list(r) for r in rows]}
def formula(h, tex, parts, whole): return {"kind": "formula", "head": h, "tex": tex, "parts": [{"sym": a, "say": b} for a, b in parts], "whole": whole}
def figure(h, svg, cap, b): return {"kind": "figure", "head": h, "svg": svg, "caption": cap, "builds": b}
def check(q, ch, a, why): return {"kind": "check", "q": q, "choices": list(ch), "a": a, "why": why}
def warn(h, *i): return {"kind": "warn", "head": h, "items": list(i)}
def bg(src, *l): return {"kind": "bg", "src": src, "lines": list(l)}
def prof(*l): return {"kind": "prof", "when": WHEN, "lines": list(l)}
def recap(*i): return {"kind": "recap", "items": list(i)}


def steps(h, st, ans, given=None):
    d = {"kind": "steps", "head": h}
    if given:
        d["given"] = given
    d["steps"] = list(st)
    d["answer"] = ans
    return d


def english(h, en, ko, tip=None):
    d = {"kind": "english", "head": h, "en": en, "ko": ko}
    if tip:
        d["tip"] = tip
    return d


def exam(src, q, qko, solve, ans):
    return {"kind": "exam", "src": src, "q": q, "qko": qko, "solve": list(solve), "answer": ans}


def look(h, *boxes):
    return {"kind": "look", "head": h,
            "boxes": [{"x": x, "y": y, "w": w, "h": hh, "say": s} for x, y, w, hh, s in boxes]}


def num_int(f, a, b, n=200001):
    x = np.linspace(a, b, n)
    y = f(x)
    return float(np.sum((y[1:] + y[:-1]) / 2 * np.diff(x)))


# ---------------- SVG ----------------
def _b(b): return f" b{b}" if b else ""


def TX(x, y, s, cls="t", fs=15, anc="middle", b=0):
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f'<text x="{x:.0f}" y="{y:.0f}" font-size="{fs}" text-anchor="{anc}" class="{cls}{_b(b)}">{s}</text>'


def R(x, y, w, h, cls="box", b=0, rx=2):
    return f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{rx}" class="{cls}{_b(b)}"/>'


def C(x, y, r, cls="n", b=0):
    return f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" class="{cls}{_b(b)}"/>'


def L(x1, y1, x2, y2, cls="e", b=0):
    return f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" class="{cls}{_b(b)}"/>'


def A(x1, y1, x2, y2, cls="e", b=0):
    ang = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 - 9 * math.cos(ang), y2 - 9 * math.sin(ang)
    px, py = -math.sin(ang) * 5, math.cos(ang) * 5
    pts = f"{x2:.0f},{y2:.0f} {hx + px:.0f},{hy + py:.0f} {hx - px:.0f},{hy - py:.0f}"
    return L(x1, y1, hx, hy, cls, b) + f'<polygon points="{pts}" class="arrow{_b(b)}"/>'


def PL(pts, cls="e2", b=0):
    s = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polyline points="{s}" fill="none" class="{cls}{_b(b)}"/>'


def PG(pts, cls="n3", b=0):
    s = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polygon points="{s}" class="{cls}{_b(b)}"/>'


def BOX(x, y, w, h, label, b=0, fs=15, cls="box"):
    return R(x, y, w, h, cls, b) + TX(x + w / 2, y + h / 2 + fs // 3 + 1, label, "tb", fs, "middle", b)


def SVG(*parts, h=270):
    return f'<svg viewBox="0 0 480 {h}" xmlns="http://www.w3.org/2000/svg">' + "".join(parts) + "</svg>"


class Ax:
    def __init__(s, x0, x1, t0, t1, base, sc):
        s.x0, s.x1, s.t0, s.t1, s.base, s.sc = x0, x1, t0, t1, base, sc

    def X(s, t): return s.x0 + (t - s.t0) / (s.t1 - s.t0) * (s.x1 - s.x0)
    def Y(s, v): return s.base - v * s.sc
    def P(s, t, v): return (s.X(t), s.Y(v))

    def curve(s, f, a, b, n=60):
        return [s.P(a + (b - a) * i / n, f(a + (b - a) * i / n)) for i in range(n + 1)]

    def area(s, f, a, b, n=60):
        return [s.P(a, 0)] + s.curve(f, a, b, n) + [s.P(b, 0)]

    def axis(s, lab="", b=0):
        out = A(s.x0 - 5, s.base, s.x1 + 8, s.base, "e", b)
        if lab:
            out += TX(s.x1 + 6, s.base + 18, lab, "tm", 14, "end", b)
        return out

    def tick(s, t, lab, b=0, dy=18):
        return L(s.X(t), s.base - 4, s.X(t), s.base + 4, "e", b) + TX(s.X(t), s.base + dy, lab, "tm", 14, "middle", b)


# p.35 계단 근사
def fig_stair():
    f = lambda t: 0.55 + 0.35 * math.sin(t)
    out = []
    for (x0, x1, d, b, tt, cap) in ((25, 225, 1.0, 1, "칸 폭 Δ = 1", "계단이 거칠어요"),
                                    (260, 460, 0.25, 2, "칸 폭 Δ = 0.25", "곡선과 거의 같아요")):
        ax = Ax(x0, x1, 0, 6, 205, 150)
        out.append(TX((x0 + x1) / 2, 28, tt, "tb", 15, "middle", b))
        k = 0.0
        while k < 6 - 1e-9:
            out.append(R(ax.X(k), ax.Y(f(k)), ax.X(k + d) - ax.X(k), f(k) * 150, "n3", b, 0))
            k += d
        out.append(PL(ax.curve(f, 0, 6), "e2"))
        out.append(ax.axis("t"))
        out.append(TX((x0 + x1) / 2, 250, cap, "tm", 14, "middle", b))
    return SVG(*out), 2


# p.36 얇은 펄스
def fig_pulse():
    ax = Ax(60, 440, -0.5, 2.2, 235, 45)
    out = [ax.axis("t"), L(ax.X(0), 240, ax.X(0), 20, "e"), TX(ax.X(0) - 8, 255, "0", "tm", 14, "end")]
    for d, cls, b, ly in ((1, "n", 1, 175), (0.5, "n3", 2, 128), (0.25, "n2", 3, 38)):
        h = 1 / d
        out.append(R(ax.X(0), ax.Y(h), ax.X(d) - ax.X(0), h * 45, cls, b, 0))
        out.append(TX(ax.X(d) + 10, ly, f"폭 {d}, 높이 {h:g}, 넓이 1", "t", 14, "start", b))
    return SVG(*out), 3


# p.38 선별 성질
def fig_sift():
    ax = Ax(30, 450, 0, 6, 225, 140)
    f = lambda t: 0.55 + 0.3 * math.cos(t)
    t = 4.0
    out = [ax.axis("τ"), PL(ax.curve(f, 0, 6), "e2"), TX(40, 40, "x(τ)", "tb", 15, "start"),
           A(ax.X(t), ax.base, ax.X(t), 45, "e2", 1), TX(ax.X(t) + 10, 55, "δ(t - τ)", "t", 15, "start", 1),
           ax.tick(t, "τ = t", 1),
           C(ax.X(t), ax.Y(f(t)), 6, "n2", 2), TX(ax.X(t) - 12, ax.Y(f(t)) + 30, "x(t)만 남아요", "tb", 15, "end", 2)]
    return SVG(*out), 2


# p.39 메아리
def fig_echo():
    top = Ax(30, 450, 0, 6, 95, 55)
    bot = Ax(30, 450, 0, 6, 255, 90)
    pul = [(0.5, 1.0), (1.5, 0.6), (2.5, 0.8)]
    h = lambda t: math.exp(-t) if t >= 0 else 0.0
    out = [top.axis("t"), TX(300, 30, "입력: 얇은 펄스 세 개", "tb", 15, "start")]
    for c, a in pul:
        out.append(R(top.X(c), top.Y(a), top.X(c + 0.2) - top.X(c), a * 55, "n3", 0, 0))
    out.append(bot.axis("t"))
    for c, a in pul:
        out.append(PL(bot.curve(lambda t, c=c, a=a: a * h(t - c), c, 6), "e", 1))
    tot = lambda t: sum(a * h(t - c) for c, a in pul)
    out.append(PL(bot.curve(tot, 0, 6, 240), "e2", 2))
    out.append(TX(300, 160, "가는 선: 펄스마다 메아리", "t", 14, "start", 1))
    out.append(TX(300, 185, "굵은 선: 모두 더한 출력", "tb", 14, "start", 2))
    return SVG(*out, h=280), 2


# p.44 뒤집고 밀고 곱하고 넓이
def fig_flip():
    out = []
    t = 1.5
    hh = lambda u: (1 - u / 2) if 0 <= u <= 2 else 0.0
    pan = [(15, 10, "1) h(τ)", 1), (250, 10, "2) 뒤집기 h(-τ)", 2), (15, 150, "3) t만큼 밀기 h(t-τ)", 3),
           (250, 150, "4) x(τ)와 곱한 넓이", 4)]
    for ox, oy, tt, b in pan:
        ax = Ax(ox + 10, ox + 205, -3, 3, oy + 100, 60)
        out += [TX(ox + 10, oy + 18, tt, "tb", 15, "start", b), ax.axis("τ", b), ax.tick(0, "0", b)]
        if b == 1:
            out.append(PL([ax.P(0, 0), ax.P(0, 1), ax.P(2, 0)], "e2", b))
        elif b == 2:
            out.append(PL([ax.P(-2, 0), ax.P(0, 1), ax.P(0, 0)], "e2", b))
        else:
            if b == 4:
                out.append(PL([ax.P(0, 0), ax.P(0, 1), ax.P(3, 1), ax.P(3, 0)], "e", b))
                out.append(PG([ax.P(0, 0), ax.P(0, hh(t)), ax.P(t, hh(0)), ax.P(t, 0)], "n3", b))
                out.append(TX(ax.X(2.3), oy + 55, "x(τ)", "t", 14, "middle", b))
            out.append(PL([ax.P(t - 2, 0), ax.P(t, 1), ax.P(t, 0)], "e2", b))
            out.append(TX(ax.X(t) + 4, ax.base + 18, "t", "tm", 14, "start", b))
    out.append(TX(355, 292, "색칠한 넓이 = y(t)", "tb", 15, "middle", 4))
    return SVG(*out, h=300), 4


# p.45 예제 2.6 겹침
def fig_ex26():
    out = []
    f = lambda u: math.exp(-u)
    for base, t, b, lab in ((125, -1.0, 0, "t < 0: 안 겹쳐요"), (275, 1.5, 1, "t > 0: 0부터 t까지 겹쳐요")):
        ax = Ax(30, 450, -3, 4, base, 80)
        out += [ax.axis("τ", b), ax.tick(0, "0", b)]
        if b:
            out.append(PG(ax.area(f, 0, t), "n3", b))
        out.append(PL([ax.P(0, 0)] + ax.curve(f, 0, 4), "e2", b))
        out.append(PL([ax.P(-3, 1), ax.P(t, 1), ax.P(t, 0)], "e", b))
        out.append(TX(ax.X(t) + (4 if t > 0 else -4), base + 18, "t", "tm", 14, "start" if t > 0 else "end", b))
        out.append(TX(ax.X(-2.9), base - 90, "h(t-τ)", "t", 14, "start", b))
        out.append(TX(270, base - 95, lab, "tb", 15, "start", b))
        out.append(TX(ax.X(2.2), base - 25, "x(τ)", "t", 14, "start", b))
    return SVG(*out, h=300), 1


# p.46 y(t) = 1 - e^{-t}
def fig_ex26y():
    ax = Ax(50, 450, 0, 5, 240, 180)
    f = lambda t: 1 - math.exp(-t)
    out = [ax.axis("t"), L(50, 245, 50, 30, "e"), TX(56, 35, "y(t)", "tm", 14, "start"),
           L(50, ax.Y(1), 450, ax.Y(1), "e"), TX(440, ax.Y(1) - 8, "1/a = 1", "tm", 14, "end"),
           PL(ax.curve(f, 0, 5), "e2"), ax.tick(1, "1"), ax.tick(2, "2")]
    out += [C(ax.X(1), ax.Y(f(1)), 5, "n2", 1), TX(ax.X(1) + 10, ax.Y(f(1)) + 26, "y(1) ≈ 0.632", "tb", 15, "start", 1),
            C(ax.X(2), ax.Y(f(2)), 5, "n2", 2), TX(ax.X(2) + 10, ax.Y(f(2)) + 26, "y(2) ≈ 0.865", "tb", 15, "start", 2)]
    return SVG(*out), 2


# p.47 예제 2.7 (T=1, t=1.5)
def fig_ex27():
    ax = Ax(30, 450, -1, 3.2, 225, 80)
    t = 1.5
    out = [ax.axis("τ"), ax.tick(-0.5, "t-2T"), ax.tick(0, "0"), ax.tick(1, "T"), ax.tick(1.5, "t"),
           PG([ax.P(0, 0), ax.P(0, t), ax.P(1, t - 1), ax.P(1, 0)], "n3", 1),
           PL([ax.P(0, 0), ax.P(0, 1), ax.P(1, 1), ax.P(1, 0)], "e"),
           PL([ax.P(-0.5, 0), ax.P(-0.5, 2), ax.P(1.5, 0)], "e2"),
           TX(ax.X(-0.5) + 8, ax.Y(2) + 4, "h(t-τ), 높이 2T", "t", 14, "start"),
           TX(ax.X(1) + 8, ax.Y(1) - 20, "x(τ), 높이 1", "t", 14, "start"),
           TX(300, 40, "T = 1, t = 1.5", "tb", 15, "start"),
           TX(300, 65, "겹친 넓이 = y(1.5) = 1", "tb", 15, "start", 1)]
    return SVG(*out), 1


def y27(t, T=1.0):
    if t < 0 or t > 3 * T:
        return 0.0
    if t < T:
        return 0.5 * t * t
    if t < 2 * T:
        return T * t - 0.5 * T * T
    return -0.5 * t * t + T * t + 1.5 * T * T


def fig_ex27y():
    ax = Ax(50, 450, 0, 3.6, 240, 110)
    out = [ax.axis("t"), L(50, 245, 50, 40, "e"), TX(56, 45, "y(t), T = 1", "tm", 14, "start"),
           PL(ax.curve(y27, 0, 3.6, 180), "e2"), ax.tick(1, "T"), ax.tick(2, "2T"), ax.tick(3, "3T")]
    for t in (0.5, 1.5, 2.5):
        out.append(C(ax.X(t), ax.Y(y27(t)), 5, "n2", 1))
    out += [TX(ax.X(0.5) - 4, ax.Y(y27(0.5)) - 12, "0.125", "t", 14, "middle", 1),
            TX(ax.X(1.5) - 10, ax.Y(y27(1.5)) - 8, "1", "t", 14, "end", 1),
            TX(ax.X(2.5) + 10, ax.Y(y27(2.5)) + 4, "0.875", "t", 14, "start", 1),
            C(ax.X(2), ax.Y(1.5), 5, "n4", 2), TX(ax.X(2), ax.Y(1.5) - 14, "최대 1.5 (t = 2T)", "tb", 15, "middle", 2)]
    return SVG(*out), 2


# p.49 예제 2.8
def fig_ex28():
    out = []
    f = lambda u: math.exp(2 * u) if u <= 0 else 0.0
    for base, t, b, lab in ((125, 2.0, 1, "t = 2: 넓이 ≈ 0.068"), (275, 5.0, 2, "t = 5: 넓이 = 0.5")):
        ax = Ax(30, 450, -4, 3, base, 85)
        e = t - 3
        out += [ax.axis("τ", b), ax.tick(0, "0", b, 18), ax.tick(e, "t-3", b, 34)]
        out.append(PG(ax.area(f, -4, min(e, 0)), "n3", b))
        out.append(PL(ax.curve(f, -4, 0) + [ax.P(0, 0), ax.P(3, 0)], "e2", b))
        out.append(PL([ax.P(-4, 1), ax.P(e, 1), ax.P(e, 0)], "e", b))
        out.append(TX(300, base - 70, lab, "tb", 15, "start", b))
        out.append(TX(300, base - 45, "가는 선: h(t-τ)", "tm", 14, "start", b))
    return SVG(*out, h=300), 2


def fig_ex28y():
    ax = Ax(50, 450, -1, 6, 230, 300)
    g = lambda t: 0.5 * math.exp(2 * (t - 3)) if t <= 3 else 0.5
    out = [ax.axis("t"), L(ax.X(0), 235, ax.X(0), 40, "e"), TX(ax.X(0) + 6, 45, "y(t)", "tm", 14, "start"),
           PL(ax.curve(g, -1, 6, 140), "e2"), ax.tick(3, "3"), ax.tick(0, "0"),
           L(ax.X(0), ax.Y(0.5), ax.X(6), ax.Y(0.5), "e"), TX(ax.X(6), ax.Y(0.5) - 8, "1/2", "tm", 14, "end"),
           C(ax.X(2), ax.Y(g(2)), 5, "n2", 1), TX(ax.X(2) - 6, ax.Y(g(2)) - 14, "y(2) ≈ 0.068", "t", 14, "end", 1),
           C(ax.X(5), ax.Y(0.5), 5, "n2", 1), TX(ax.X(5), ax.Y(0.5) + 26, "y(5) = 0.5", "t", 14, "middle", 1),
           TX(ax.X(3), 70, "t = 3 이 분기점", "tb", 15, "middle", 1)]
    return SVG(*out), 1


def chain(y, items, b=0, x0=15):
    """items: ("in", 라벨) / ("box", 라벨, 폭) 차례. 화살표로 잇는다."""
    out, x = [], x0
    for it in items:
        if it[0] == "lab":
            out.append(TX(x, y + 5, it[1], "t", 15, "start", b))
            x += it[2]
        elif it[0] == "arr":
            out.append(A(x, y, x + it[1], y, "e", b))
            x += it[1]
        else:
            w = it[2]
            out.append(BOX(x, y - 20, w, 40, it[1], b))
            x += w
    return out


# p.43 블록
def fig_block():
    out = chain(70, [("lab", "δ(t)", 42), ("arr", 50), ("box", "LTI 시스템", 130), ("arr", 50), ("lab", "h(t): 메아리", 0)])
    out += chain(190, [("lab", "x(t)", 42), ("arr", 50), ("box", "h(t)", 130), ("arr", 50), ("lab", "y(t) = x(t)*h(t)", 0)], 1)
    out.append(TX(240, 140, "그래서 상자 이름을 h(t)로 불러요", "tm", 14, "middle", 1))
    return SVG(*out), 1


# p.51 같은 h, 다른 시스템
def fig_nonlin():
    out = [TX(30, 125, "δ[n]", "tb", 15, "middle")]
    labs = ["x[n] + x[n-1]", "(x[n] + x[n-1])²", "max(x[n], x[n-1])"]
    for i, lab in enumerate(labs):
        yc = 45 + i * 85
        out.append(A(55, 125, 110, yc, "e", i + 1 if i else 0))
        out.append(BOX(110, yc - 22, 200, 44, lab, i + 1 if i else 0, 15))
        out.append(A(310, yc, 350, yc, "e", i + 1 if i else 0))
        for k in range(2):
            x = 375 + k * 30
            out += [L(x, yc + 18, x, yc - 12, "e2", i + 1 if i else 0), C(x, yc - 12, 4, "n2", i + 1 if i else 0)]
        out.append(TX(440, yc + 5, "1, 1", "t", 14, "start", i + 1 if i else 0))
    out.append(TX(240, 268, "셋 다 h[n] = 1, 1 이 나와요", "tm", 14, "middle", 2))
    return SVG(*out, h=280), 2


# p.53 교환
def fig_swap():
    out = chain(80, [("lab", "x(t)", 45), ("arr", 60), ("box", "h(t)", 120), ("arr", 60), ("lab", "y(t)", 0)])
    out += chain(190, [("lab", "h(t)", 45), ("arr", 60), ("box", "x(t)", 120), ("arr", 60), ("lab", "y(t)", 0)], 1)
    out.append(TX(240, 140, "자리를 바꿔도 출력은 같아요", "tm", 14, "middle", 1))
    return SVG(*out), 1


# p.54 병렬
def fig_par():
    out = [TX(15, 95, "x(t)", "t", 15, "start"), L(52, 90, 90, 90), L(90, 45, 90, 135),
           A(90, 45, 130, 45), A(90, 135, 130, 135),
           BOX(130, 25, 90, 40, "h1(t)"), BOX(130, 115, 90, 40, "h2(t)"),
           L(220, 45, 270, 45), A(270, 45, 270, 76), L(220, 135, 270, 135), A(270, 135, 270, 104),
           C(270, 90, 14, "n"), TX(270, 96, "+", "tb", 18), A(284, 90, 340, 90), TX(348, 95, "y(t)", "t", 15, "start"),
           TX(240, 30, "y1", "tm", 14, "start"), TX(240, 125, "y2", "tm", 14, "start")]
    out += chain(230, [("lab", "x(t)", 45), ("arr", 50), ("box", "h1(t) + h2(t)", 170), ("arr", 50), ("lab", "y(t)", 0)], 1)
    out.append(TX(240, 185, "위 두 갈래 = 아래 상자 하나", "tb", 15, "middle", 1))
    return SVG(*out, h=270), 1


# p.55, p.58 직렬
def fig_ser():
    out = chain(45, [("lab", "x", 25), ("arr", 40), ("box", "h1", 80), ("arr", 50), ("box", "h2", 80), ("arr", 40), ("lab", "y", 0)])
    out += chain(135, [("lab", "x", 25), ("arr", 40), ("box", "h2", 80), ("arr", 50), ("box", "h1", 80), ("arr", 40), ("lab", "y", 0)], 1)
    out += chain(225, [("lab", "x", 25), ("arr", 40), ("box", "h1 * h2", 210), ("arr", 40), ("lab", "y", 0)], 2)
    out += [TX(460, 95, "순서를 바꿔도 같아요", "tm", 14, "end", 1), TX(460, 185, "하나로 합쳐도 같아요", "tm", 14, "end", 2)]
    return SVG(*out), 2


def stems(ax, vals, n0, cls="e2", b=0, labels=True, vlabels=None):
    out = []
    for i, v in enumerate(vals):
        n = n0 + i
        out += [L(ax.X(n), ax.base, ax.X(n), ax.Y(v), cls, b), C(ax.X(n), ax.Y(v), 4, "n2", b)]
        if labels:
            out.append(TX(ax.X(n), ax.base + 18, str(n), "tm", 14, "middle", b))
        if vlabels and vlabels[i]:
            out.append(TX(ax.X(n), ax.Y(v) - 10, vlabels[i], "t", 14, "middle", b))
    return out


# p.57 예제 2.10 그래프
def y210(n):
    y1 = (1 - 0.5 ** (n + 1)) / (1 - 0.5) if n >= 0 else 0.0
    y2 = 2.0 ** (n + 1) if n <= 0 else 2.0
    return y1 + y2


def fig_y210():
    ax = Ax(40, 440, -3.5, 7.5, 235, 45)
    ns = list(range(-3, 8))
    vl = ["1/4", "1/2", "1", "3", "3.5", "3.75", "", "", "", "", ""]
    out = [ax.axis("n"), L(ax.X(-3.5), ax.Y(4), ax.X(7.5), ax.Y(4), "e"), TX(ax.X(7.5), ax.Y(4) - 8, "4에 다가가요", "tm", 14, "end")]
    out += stems(ax, [y210(n) for n in ns], -3, vlabels=vl)
    return SVG(*out), 1


# p.59 무기억
def fig_mem():
    a1 = Ax(30, 220, -2.5, 3.5, 220, 45)
    a2 = Ax(260, 450, -2.5, 3.5, 220, 45)
    out = [a1.axis("n"), TX(125, 30, "무기억: h[n] = 3δ[n]", "tb", 15)] + stems(a1, [0, 0, 3, 0, 0, 0], -2)
    out += [a2.axis("n", 1), TX(355, 30, "기억 있음: h = 1, 1", "tb", 15, "middle", 1)] + stems(a2, [0, 0, 1, 1, 0, 0], -2, b=1)
    out += [TX(125, 262, "n = 0 한 칸만", "tm", 14), TX(355, 262, "n = 1 에도 메아리", "tm", 14, "middle", 1)]
    return SVG(*out, h=275), 1


# p.60 가역
def fig_inv():
    out = chain(70, [("lab", "x(t)", 40), ("arr", 35), ("box", "h(t)", 80), ("arr", 55), ("box", "h1(t)", 80), ("arr", 35), ("lab", "x(t)", 0)])
    out.append(TX(208, 55, "y(t)", "tm", 14, "middle"))
    out += chain(200, [("lab", "x(t)", 40), ("arr", 50), ("box", "항등 시스템 δ(t)", 200), ("arr", 50), ("lab", "x(t)", 0)], 1)
    out.append(TX(240, 140, "두 상자를 합치면 h * h1 = δ", "tb", 15, "middle", 1))
    return SVG(*out), 1


# p.62 항등
def fig_ident():
    a1 = Ax(20, 160, -0.5, 3, 200, 35)
    a2 = Ax(320, 460, -0.5, 3, 200, 35)
    out = [a1.axis("n"), a2.axis("n", 1), BOX(190, 140, 100, 44, "δ[n]"), A(165, 162, 190, 162), A(290, 162, 318, 162, "e", 1)]
    out += stems(a1, [1, 2, 3], 0) + stems(a2, [1, 2, 3], 0, b=1)
    out += [TX(90, 40, "입력 1, 2, 3", "tb", 15), TX(390, 40, "출력 1, 2, 3", "tb", 15, "middle", 1)]
    return SVG(*out), 1


# =====================================================================
# 손계산 확인 (모든 숫자 답은 여기서 계산하고 assert)
# =====================================================================
# 막대 합 -> 적분 (f(x)=x, 0~1)
def left_sum(d):
    k = np.arange(0, 1 - 1e-12, d)
    return float(np.sum(k * d))
assert abs(left_sum(0.25) - 0.375) < 1e-9 and abs(left_sum(0.1) - 0.45) < 1e-9 and abs(left_sum(0.01) - 0.495) < 1e-9
assert abs(num_int(lambda x: x, 0, 1) - 0.5) < 1e-9
# 얇은 펄스 넓이는 늘 1
for d in (1, 0.5, 0.2):
    assert abs((1 / d) * d - 1) < 1e-12
assert abs(0.9 * (1 / 0.2) * 0.2 - 0.9) < 1e-12
assert math.floor(0.5 / 0.2) == 2
# 선별 성질: x(τ)=τ²+1, t=2, 폭 0.001 펄스로 근사
dd = 0.001
sift_val = num_int(lambda u: (u ** 2 + 1) / dd, 2 - dd, 2, 2001)
assert abs(sift_val - 5) < 0.01
# 메아리 두 개 더하기
assert abs(1 * 0.3 + 0.5 * 0.6 - 0.6) < 1e-12
# p.44 그림 숫자: h 삼각형(1-u/2), x 네모 0~3, t=1.5
flip_area = num_int(lambda u: np.where((u >= 0) & (u <= 3), 1.0, 0.0) * np.where((1.5 - u >= 0) & (1.5 - u <= 2), 1 - (1.5 - u) / 2, 0.0), -1, 4)
assert abs(flip_area - 0.9375) < 1e-3 and abs((0.25 + 1) / 2 * 1.5 - 0.9375) < 1e-12
# 예제 2.6
def y26(t, a):
    return (1 / a) * (1 - math.exp(-a * t)) if t > 0 else 0.0
for a, t in ((1, 1), (1, 2), (2, 1)):
    nm = num_int(lambda u: np.exp(-a * u), 0, t)
    assert abs(nm - y26(t, a)) < 1e-6
assert round(y26(1, 1), 3) == 0.632 and round(y26(2, 1), 3) == 0.865 and round(y26(1, 2), 3) == 0.432
assert round(math.exp(-1), 3) == 0.368 and round(math.exp(-2), 3) == 0.135
# 예제 2.7 (T=1)
def y27num(t):
    return num_int(lambda u: np.where((u > 0) & (u < 1), 1.0, 0.0) * np.where((t - u > 0) & (t - u < 2), t - u, 0.0), -1, 4)
for t, v in ((0.5, 0.125), (1.5, 1.0), (2.0, 1.5), (2.5, 0.875), (3.5, 0.0)):
    assert abs(y27(t) - v) < 1e-12 and abs(y27num(t) - v) < 2e-3
assert abs((1.5 + 0.5) / 2 * 1 - 1.0) < 1e-12 and abs((2 + 1.5) / 2 * 0.5 - 0.875) < 1e-12 and abs(0.5 * 0.5 * 0.5 - 0.125) < 1e-12
# 예제 2.8
def y28(t):
    return 0.5 * math.exp(2 * (t - 3)) if t <= 3 else 0.5
for t in (2, 5):
    nm = num_int(lambda u: np.exp(2 * u) * np.where(u < 0, 1.0, 0.0) * np.where(t - u - 3 > 0, 1.0, 0.0), -30, 6, 400001)
    assert abs(nm - y28(t)) < 1e-4
assert round(y28(2), 3) == 0.068 and y28(5) == 0.5 and abs(y28(3) - 0.5) < 1e-12
# 이산 예: 교환, 분배, 결합
x_, h1_, h2_ = [1, 2], [1, 1], [1, -1]
cv = lambda a, b: [int(v) for v in np.convolve(a, b)]
assert cv(x_, h1_) == [1, 3, 2] == cv(h1_, x_)
assert cv(x_, h2_) == [1, 1, -2]
assert [a + b for a, b in zip(cv(x_, h1_), cv(x_, h2_))] == [2, 4, 0] == cv(x_, [2, 0])
assert cv(h1_, h2_) == [1, 0, -1] and cv(cv(x_, h1_), h2_) == [1, 2, -1, -2] == cv(x_, cv(h1_, h2_)) == cv(cv(x_, h2_), h1_)
# 비선형 세 시스템 (x[-1]=0)
def run(sysf, x, n=3):
    xx = lambda k: x[k] if 0 <= k < len(x) else 0
    return [sysf(xx(k), xx(k - 1)) for k in range(n)]
T1 = lambda a, b: a + b
T2 = lambda a, b: (a + b) ** 2
T3 = lambda a, b: max(a, b)
for f in (T1, T2, T3):
    assert run(f, [1])[:2] == [1, 1]
assert run(T1, [1, 2]) == [1, 3, 2] and run(T2, [1, 2]) == [1, 9, 4] and run(T3, [1, 2]) == [1, 2, 2]
assert (2 * 3) ** 2 == 36 and 2 * 3 ** 2 == 18
# 무기억, 항등, 역
assert cv([1, 2, 3], [3]) == [3, 6, 9] and cv([1, 2, 3], [1, 1]) == [1, 3, 5, 3] and cv([1, 2, 3], [1]) == [1, 2, 3]
assert float(np.convolve([2], [0.5])[0]) == 1.0
# 예제 2.10: 잘린 수열로 직접 컨볼루션
nn = np.arange(-60, 61)
xx = np.where(nn >= 0, 0.5 ** np.clip(nn, 0, None), 0) + np.where(nn <= 0, 2.0 ** np.clip(nn, None, 0), 0)
def ydirect(n):
    return float(np.sum(xx[nn <= n]))  # h = u[n] 이면 y[n] = n 까지 누적 합
for n in range(-3, 8):
    assert abs(ydirect(n) - y210(n)) < 1e-9
assert [y210(n) for n in (-3, -2, -1, 0, 1, 2)] == [0.25, 0.5, 1.0, 3.0, 3.5, 3.75]
assert abs(sum(0.5 ** k for k in range(200)) - 2) < 1e-12

S = []
FS, FSB = fig_stair()
FP, FPB = fig_pulse()
FSF, FSFB = fig_sift()
FE, FEB = fig_echo()

# ---------------- p.34 ----------------
S.append({"p": 34, "title": "2.2 연속시간 LTI 시스템: 컨볼루션 적분을 시작해요",
 "pass1": [
  say("여기서부터 2.2절이에요. 지금까지는 점으로 된 [[dt]]에서 [[csum:을]] 했어요.",
      "이제 끊김 없는 선, 곧 [[ct]]에서도 똑같은 일을 해요.",
      "선을 아주 얇은 막대로 잘게 쪼개면, 점처럼 다룰 수 있거든요."),
  analogy("점에서 선으로",
      "하루 한 번 찍은 종가(점)와 끊김 없이 그린 주가 선을 떠올려요. 점을 아주 촘촘히 찍으면 선과 거의 같아져요.",
      ["하루 한 번 찍은 점", "[[dt]] $x[n]$"], ["끊김 없이 그린 선", "[[ct]] $x(t)$"],
      ["점을 아주 촘촘히 찍기", "얇은 펄스로 쪼개고 폭을 0으로 줄이기"]),
 ],
 "pass2": [
  points("이 쪽 네 줄을 쉬운 말로",
      "이번에는 [[conv]] 이론을 연속 시스템에 쓰는 법을 배워요.",
      "이산과 연속의 관계를 보면 가장 쉽게 이해돼요.",
      "이산의 [[csum:은]] [[sift]] 덕분이었어요. 입력을 크기 바꾸고 옮긴 [[imp]]의 합으로 썼죠.",
      "연속 신호는 '아주 얇은 펄스의 극한'으로 생각해서 같은 일을 해요."),
  compare("이산과 연속, 무엇이 바뀌나", ["", "이산시간", "연속시간"],
      ["신호", "$x[n]$ (점)", "$x(t)$ (선)"],
      ["재료", "[[imp]] $\\delta[n]$", "얇은 펄스, 끝내 $\\delta(t)$"],
      ["모으는 법", "[[summ]] $\\sum$", "[[integ]] $\\int$"],
      ["결과", "[[csum]]", "[[cint]]"]),
  check("연속시간으로 오면 [[csum]]의 시그마 $\\sum$ 는 무엇으로 바뀔까요?",
      ["곱하기", "[[integ]] $\\int$", "[[deriv]]"], 1,
      "[[summ]] 대신 [[integ:이]] 들어가요. 더하는 칸이 한없이 얇아지면 합이 넓이가 되거든요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (0.064, 0.177, 0.611, 0.035, "소제목: 연속시간 신호를 임펄스로 나타내기예요."),
      (0.107, 0.234, 0.827, 0.033, "[[conv]] 이론을 연속 시스템(continuous systems)에 쓰겠다는 선언이에요."),
      (0.107, 0.288, 0.821, 0.076, "이산과 연속 시스템의 관계로 보면 가장 쉽대요."),
      (0.107, 0.386, 0.787, 0.077, "이산 [[csum:은]] 선별 원리(sifting principle)에 기대요. 입력 = 크기 바꾸고 옮긴 임펄스의 합."),
      (0.107, 0.484, 0.807, 0.033, "연속 신호는 '한없이 얇은 펄스의 극한'으로 보면 같은 방법이 통해요.")),
  prof("이산시간이 연속시간에 비하면 '진짜 100배 쉽다'고 하셨어요.",
       "그래도 결론은 같대요: 시그마로 쓰던 것이 연속에서는 모두 인티그럴(적분)로 바뀐다.",
       "중간의 증명 과정까지 다 알 필요는 없고, 결과 식을 기억하면 된다고 하셨어요."),
  bg("S3 p.10~17 임펄스로 신호 나타내기",
     "앞에서 $x[n]=\\sum_k x[k]\\,\\delta[n-k]$ 를 봤어요.",
     "점 하나하나를 '높이 $x[k]$ 짜리 손뼉'으로 본 식이에요.",
     "오늘은 이 식의 연속시간 버전을 만들어요."),
 ],
 "pass4": [
  warn("헷갈리기 쉬운 점",
      "이산 $\\delta[n]$ 은 높이 1인 점이에요.",
      "연속 $\\delta(t)$ 는 높이 1이 아니라, 폭이 0에 가깝고 넓이가 1인 펄스예요."),
  prof("첫 퀴즈(5주차 수업 시작)는 1장 전체와 2장 슬라이드 62번(PDF p.70)까지라고 하셨어요.",
       "이 쪽부터 p.62까지는 모두 퀴즈 범위 안이에요.",
       "수업에서 다룬 예제와 과제만 복습하면 시간 안에 충분히 푼대요."),
 ]})

# ---------------- p.35 ----------------
S.append({"p": 35, "title": "연속 신호를 얇은 펄스로 쪼개기 (그림)",
 "pass1": [
  say("왼쪽 그림은 빨간 곡선을 파란 계단으로 흉내 낸 모습이에요.",
      "계단 한 칸이 얇은 펄스 하나예요.",
      "칸을 좁히면 계단이 곡선과 거의 똑같아져요."),
  figure("칸이 좁을수록 곡선에 가까워요", FS, "왼쪽은 칸 폭 1, 오른쪽은 칸 폭 0.25예요.", FSB),
 ],
 "pass2": [
  points("그림 속 기호 읽기",
      "$\\Delta$ 는 '델타'라고 읽고, 계단 한 칸의 폭이에요. 슬라이드 그림은 $\\Delta=0.2$예요.",
      "$x(k\\Delta)$ 는 k번째 칸 왼쪽 끝에서 잰 곡선 높이예요.",
      "아래 세 칸 그림은 그 계단에서 한 칸씩만 떼어 낸 모습이에요."),
  formula("오른쪽 식: 합이 적분이 돼요",
      r"\text{Area}=\int_0^{x_m} f(x)\,dx=\lim_{\Delta x\to 0}\sum_{i=1}^{N} f_i(x)\,\Delta x",
      [(r"\sum_{i=1}^{N} f_i(x)\,\Delta x", "막대 N개의 넓이(높이 곱하기 폭)를 모두 더하기"),
       (r"\lim_{\Delta x\to 0}", "막대 폭을 0에 한없이 가깝게 줄이면"),
       (r"\int_0^{x_m} f(x)\,dx", "곡선 아래 넓이, 곧 [[integ]]")],
      "얇은 막대 넓이의 합에서 폭을 0으로 보내면 곡선 아래 넓이([[integ]])가 돼요."),
  check("계단 폭 $\\Delta$ 를 점점 줄이면 어떻게 될까요?",
      ["계단이 곡선에서 멀어져요", "계단이 곡선과 거의 같아져요", "아무 변화가 없어요"], 1,
      "칸이 좁을수록 곡선을 촘촘히 따라가요. 그 극한이 원래 [[ct]]예요."),
 ],
 "pass3": [
  look("그림 짚어 읽기",
      (0.18, 0.24, 0.24, 0.14, "빨간 곡선 $x(t)$ 와 파란 계단 근사예요. 칸 폭 $\\Delta=0.2$."),
      (0.18, 0.39, 0.24, 0.43, "계단에서 칸 하나씩 떼어 낸 펄스 세 개예요. 폭 0.2짜리 네모예요."),
      (0.52, 0.37, 0.34, 0.2, "오른쪽 위: 막대 합(왼쪽)이 폭을 줄이면 곡선 아래 넓이(오른쪽)가 된다는 그림."),
      (0.55, 0.62, 0.27, 0.1, "그래서 넓이 $=\\int f\\,dx=\\lim\\sum f\\,\\Delta x$ 예요.")),
  bg(B8,
     "[[integ:은]] 그래프 아래 넓이를 구하는 계산이에요.",
     "얇은 막대 넓이를 다 더하고, 막대를 한없이 얇게 하면 그게 적분이에요.",
     "앞으로 적분이 나오면 '겹치는 부분의 넓이'라고 읽으면 돼요."),
  steps("막대 합이 적분으로 가는 것을 숫자로",
      ["$\\Delta=0.25$: 막대 4개, 높이 $0, 0.25, 0.5, 0.75$",
       "넓이 합 $=(0+0.25+0.5+0.75)\\times0.25=0.375$",
       "$\\Delta=0.1$: 합 $=0.45$",
       "$\\Delta=0.01$: 합 $=0.495$",
       "폭이 작아질수록 진짜 넓이 $0.5$ 에 다가가요"],
      "$\\lim\\sum=\\int_0^1 x\\,dx=0.5$",
      "$f(x)=x$ 를 $x=0$ 부터 $1$ 까지. 진짜 넓이는 삼각형이라 $\\frac12\\times1\\times1=0.5$"),
  prof("적분의 개념은 '미소 구간에 대한 넓이(에어리어)'라고 하셨어요.",
       "네모들의 합에서 네모를 점점 얇게 하면 곡선 밑 넓이가 되고, 그걸 적분 기호로 쓴대요."),
 ],
 "pass4": [
  warn("그림 제목 읽을 때",
      "그림 제목 $x(-2\\Delta t)\\,\\delta_\\Delta(t+2\\Delta)\\Delta$ 에서 $\\Delta t$ 는 칸 폭 $\\Delta$ 와 같은 뜻으로 쓰였어요.",
      "즉 $x(-2\\Delta)$, 곧 왼쪽으로 두 칸 간 곳의 곡선 높이예요."),
  check("계단 근사에서 k번째 칸의 높이는?",
      ["$x(k\\Delta)$", "$k\\Delta$", "$1/\\Delta$"], 0,
      "k번째 칸 왼쪽 끝 $t=k\\Delta$ 에서 잰 곡선 높이 $x(k\\Delta)$ 예요."),
 ]})

# ---------------- p.36 ----------------
S.append({"p": 36, "title": "얇은 펄스 δΔ(t)와 계단 근사식",
 "pass1": [
  say("이 쪽은 계단 한 칸을 수학 모양으로 적어요.",
      "폭은 아주 좁고, 넓이는 딱 1인 막대를 하나 만들어요.",
      "이 막대에 곡선 높이를 곱해 줄줄이 이어 붙이면 계단 전체가 돼요."),
  figure("폭이 좁아지면 키가 커져요", FP, "폭 1, 0.5, 0.25인 펄스. 넓이는 모두 1이에요.", FPB),
 ],
 "pass2": [
  formula("얇은 펄스의 정의",
      r"\delta_\Delta(t)=\begin{cases}\frac{1}{\Delta} & 0\le t<\Delta\\ 0 & \text{otherwise}\end{cases}",
      [(r"\delta_\Delta(t)", "'델타 델타 t': 폭이 $\\Delta$ 인 얇은 펄스"),
       (r"\frac{1}{\Delta}", "높이는 델타분의 1"),
       (r"0\le t<\Delta", "0부터 $\\Delta$ 직전까지만 켜져요"),
       (r"\text{otherwise}", "나머지 시간은 0")],
      "폭 $\\Delta$ 곱하기 높이 $1/\\Delta$ 는 넓이 1. 그래서 슬라이드가 'unit integral(적분값 1)'이라고 해요."),
  formula("계단 근사식",
      r"\hat{x}(t)=\sum_{k=-\infty}^{\infty} x(k\Delta)\,\delta_\Delta(t-k\Delta)\,\Delta",
      [(r"\hat{x}(t)", "'엑스 햇 t': 계단으로 흉내 낸 신호"),
       (r"\sum_{k=-\infty}^{\infty}", "k를 모든 정수로 바꿔 가며 더하기([[summ]])"),
       (r"x(k\Delta)", "k번째 칸의 곡선 높이"),
       (r"\delta_\Delta(t-k\Delta)\,\Delta", "k번째 칸으로 옮긴 펄스에 $\\Delta$ 를 곱해 높이를 1로 맞춘 것")],
      "칸마다 '높이 $x(k\\Delta)$ 짜리 네모'를 놓고 모두 더하면 계단 신호예요."),
  check("$\\delta_\\Delta(t)$ 의 넓이는?", ["$\\Delta$", "1", "$1/\\Delta$"], 1,
      "폭 $\\Delta$, 높이 $1/\\Delta$ 라서 곱하면 늘 1이에요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (0.107, 0.234, 0.802, 0.076, "앞에서 본 것처럼 연속 신호는 얇고 늦춘 펄스들의 합으로 근사할 수 있대요."),
      (0.176, 0.337, 0.401, 0.123, "펄스 정의와 그림이에요. 0에서 $\\Delta$ 까지 높이 $1/\\Delta$."),
      (0.107, 0.496, 0.509, 0.033, "이 네모는 넓이(적분값)가 1이라는 설명이에요."),
      (0.35, 0.551, 0.192, 0.09, "계단 근사식 $\\hat{x}(t)$ 예요.")),
  steps("폭을 바꿔도 넓이는 1",
      ["$\\Delta=1$: 높이 $1$, 넓이 $1\\times1=1$",
       "$\\Delta=0.5$: 높이 $2$, 넓이 $0.5\\times2=1$",
       "$\\Delta=0.2$ (슬라이드 그림): 높이 $5$, 넓이 $0.2\\times5=1$"],
      "폭이 좁아질수록 키가 커져서 넓이는 늘 1이에요."),
  steps("한 칸의 높이 확인",
      ["$\\Delta=0.2$, $k=2$ 칸은 $0.4\\le t<0.6$ 이에요.",
       "$x(0.4)=0.9$ 라고 해 봐요.",
       "칸 높이 $=x(0.4)\\times\\frac{1}{0.2}\\times0.2$",
       "$=0.9\\times5\\times0.2=0.9$"],
      "끝의 $\\Delta$ 덕분에 칸 높이가 곡선 높이 $0.9$ 와 같아져요."),
  prof("연속시간에서는 높이가 $1/\\Delta$ 인 네모 신호를 먼저 생각했다고 설명하셨어요.",
       "여기에 $\\Delta$ 를 곱하면 높이가 1이 되고, $x(k\\Delta)$ 를 곱하면 그 칸의 넓이가 된대요."),
 ],
 "pass4": [
  warn("헷갈리기 쉬운 점",
      "$\\delta_\\Delta(t)$ 는 폭 $\\Delta$ 인 진짜 네모, $\\delta(t)$ 는 $\\Delta\\to0$ 의 극한이에요.",
      "근사식 끝의 $\\Delta$ 를 빠뜨리기 쉬워요."),
  check("근사식 끝에 $\\Delta$ 를 곱하는 이유는?",
      ["펄스 높이 $1/\\Delta$ 를 1로 맞추려고", "신호를 오른쪽으로 옮기려고", "k를 세려고"], 0,
      "$\\frac{1}{\\Delta}\\times\\Delta=1$ 이라서, 칸 높이가 $x(k\\Delta)$ 그대로 돼요."),
 ]})

# ---------------- p.37 ----------------
S.append({"p": 37, "title": "Δ→0: 합이 적분이 되고 선별 성질이 나와요",
 "pass1": [
  say("계단 칸을 한없이 얇게 하면 계단이 원래 곡선과 똑같아져요.",
      "그때 더하기(시그마)는 넓이 구하기([[integ]])로 바뀌어요.",
      "이렇게 나온 식을 [[sift]]이라고 불러요. 한 순간의 값만 골라낸다는 뜻이에요."),
  analogy("손뼉으로 선 만들기",
      "크기가 다른 손뼉을 아주 촘촘히, 끊김 없이 치면 부드러운 소리 곡선이 돼요.",
      ["손뼉 한 번", "[[imp]] $\\delta(t-\\tau)$"], ["그 손뼉의 크기", "그 순간의 값 $x(\\tau)$"],
      ["끊김 없이 모두 모으기", "[[integ]] $\\int d\\tau$"]),
 ],
 "pass2": [
  formula("연속시간의 [[sift]]",
      r"x(t)=\int_{-\infty}^{\infty} x(\tau)\,\delta(t-\tau)\,d\tau",
      [(r"\int_{-\infty}^{\infty}", "마이너스 무한대부터 무한대까지 [[integ]](넓이 모으기)"),
       (r"x(\tau)", "'엑스 타우': 입력 시간 $\\tau$ 에서의 신호 값"),
       (r"\delta(t-\tau)", "$\\tau$ 가 $t$ 와 같을 때만 켜지는 [[imp]]"),
       (r"d\tau", "'디 타우': 한없이 얇아진 칸 폭 ($\\Delta$ 가 바뀐 것)")],
      "모든 $\\tau$ 에서 '값 곱하기 손뼉'을 모으면 $t$ 한 곳의 값 $x(t)$ 만 남아요."),
  compare("합에서 적분으로 바뀌는 것", ["계단 근사식", "$\\Delta\\to0$ 이후"],
      ["$k\\Delta$", "$\\tau$"], ["$\\Delta$", "$d\\tau$"], ["$\\sum_k$", "$\\int d\\tau$"],
      ["$\\delta_\\Delta$", "$\\delta$"]),
  check("[[sift]]의 영어 sift 는 무슨 뜻일까요?",
      ["체로 거르다, 골라내다", "밀다", "뒤집다"], 0,
      "여러 값 중에서 $\\tau=t$ 인 값 하나만 체로 걸러 내듯 골라낸다는 뜻이에요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (0.107, 0.234, 0.472, 0.033, "어느 $t$ 에서든 켜져 있는 펄스는 딱 하나뿐이래요."),
      (0.244, 0.288, 0.217, 0.095, "그래서 $\\Delta\\to0$ 극한을 취하면 근사가 아니라 진짜 $x(t)$ 가 돼요."),
      (0.27, 0.44, 0.165, 0.08, "합이 적분으로 바뀐 식이에요."),
      (0.107, 0.528, 0.661, 0.076, "이것이 연속시간 임펄스의 [[sift]]. $\\delta(t-\\tau)$ 가 무한히 많대요."),
      (0.787, 0.255, 0.164, 0.567, "(b) τ 축 위의 펄스는 $t-\\Delta$ 부터 $t$ 까지. (c) $x(\\tau)$ 를 곱한 빗금 넓이.")),
  bg(B8,
     "$\\int$ 기호는 길게 늘인 S예요. 합(Sum)에서 왔어요.",
     "그래서 '[[integ]] = 한없이 얇은 막대의 합 = 넓이'라고 읽어요."),
  steps("'한 칸만 켜진다'를 숫자로",
      ["$\\Delta=0.2$ 이면 칸은 $[0,0.2)$, $[0.2,0.4)$, $[0.4,0.6)$ 처럼 나뉘어요.",
       "$t=0.5$ 는 $k=2$ 칸 $[0.4,\\,0.6)$ 안에만 있어요.",
       "그래서 $\\hat{x}(0.5)=x(0.4)$ 예요.",
       "$\\Delta\\to0$ 이면 칸 왼쪽 끝이 $t$ 에 붙어서 $x(t)$ 와 같아져요."],
      "$\\hat{x}(0.5)=x(0.4)$, 극한에서는 $x(t)$"),
  prof("칠판에서 $\\Delta$ 간격으로 쪼개고, 네모 넓이를 $x(k\\Delta)\\times\\Delta$ 로 계산하셨어요.",
       "$\\Delta$ 가 0으로 가면 $\\Delta$ 는 $d\\tau$ 로, $k\\Delta$ 는 $\\tau$ 로 바뀌며 합이 적분이 된대요.",
       "'과정은 어렵지만 생긴 건 거의 똑같다, 시그마만 인티그럴로 바뀐다'고 하셨어요."),
 ],
 "pass4": [
  english("답안에 쓸 문장",
      "연속시간 신호는 $x(t)=\\int_{-\\infty}^{\\infty}x(\\tau)\\delta(t-\\tau)d\\tau$ 처럼 임펄스들의 적분으로 나타낼 수 있고, 이를 선별 성질이라 한다.",
      "계단 근사식에서 $\\Delta\\to0$ 으로 보낸 결과예요.",
      "'값 곱하기 델타를 적분하면 그 점의 값'"),
  check("$\\int_{-\\infty}^{\\infty} x(\\tau)\\,\\delta(t-\\tau)\\,d\\tau$ 의 값은?",
      ["$x(t)$", "$x(0)$", "1"], 0,
      "[[sift]]이에요. $\\tau=t$ 한 곳의 값만 남아요."),
 ]})

# ---------------- p.38 ----------------
S.append({"p": 38, "title": "δ(t)로 선별 성질을 바로 보이기",
 "pass1": [
  say("이 쪽은 같은 결론을 [[imp]] $\\delta(t)$ 로 곧바로 보여 줘요.",
      "손뼉은 한 순간에만 소리가 나요. 그래서 곱하면 그 순간 값만 남아요.",
      "그걸 적분하면 $x(t)$ 하나가 골라져요."),
  figure("손뼉이 값 하나를 골라요", FSF, "τ = t 에만 서 있는 화살표가 그 점의 값만 남겨요.", FSFB),
 ],
 "pass2": [
  formula("[[imp]] $\\delta$ 의 두 성질",
      r"\delta(t-\tau)=0\ \ (t\ne\tau),\qquad \int_{-\infty}^{\infty}\delta(t-\tau)\,d\tau=1",
      [(r"\delta(t-\tau)=0\ \ (t\ne\tau)", "$\\tau$ 가 $t$ 가 아니면 0 (한 순간에만 켜짐)"),
       (r"\int_{-\infty}^{\infty}\delta(t-\tau)\,d\tau=1", "전체 넓이([[integ]])는 1")],
      "딱 한 점에만 있고 넓이는 1인 것이 [[imp]]예요."),
  steps("유도 세 줄 읽기",
      ["$\\tau\\ne t$ 에서는 $\\delta$ 가 0이라 곱 $x(\\tau)\\delta(t-\\tau)$ 도 0이에요.",
       "살아 있는 곳은 $\\tau=t$ 뿐이라 $x(\\tau)$ 를 $x(t)$ 로 바꿔 써도 돼요.",
       "$x(t)$ 는 $\\tau$ 와 상관없는 상수라 적분 밖으로 나와요.",
       "남은 적분은 넓이 1이라 $x(t)\\times1=x(t)$"],
      "$\\int x(\\tau)\\delta(t-\\tau)d\\tau=x(t)$"),
  check("$\\tau\\ne t$ 일 때 $x(\\tau)\\,\\delta(t-\\tau)$ 는 얼마일까요?",
      ["0", "$x(t)$", "1"], 0, "[[imp]]가 0이라 곱도 0이에요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (0.107, 0.234, 0.574, 0.076, "[[imp]] $\\delta(t)$ 로 바로 [[sift:을]] 유도할 수도 있었대요."),
      (0.179, 0.352, 0.161, 0.112, "$\\delta$ 의 두 성질: 한 점 밖에서 0, 넓이 1."),
      (0.179, 0.569, 0.323, 0.277, "유도: 곱이 한 점에서만 살아서 $x(t)$ 가 밖으로 나오고, 남은 넓이가 1."),
      (0.703, 0.5, 0.2, 0.17, "(b) τ 축에서 $\\tau=t$ 에 선 화살표, 높이(넓이) 1."),
      (0.703, 0.7, 0.2, 0.18, "(c) 곱하면 화살표 크기가 $x(t)$ 가 돼요.")),
  steps("숫자로 해 보기",
      ["$x(\\tau)=\\tau^2+1$, $t=2$ 라고 해요.",
       "$\\int(\\tau^2+1)\\,\\delta(2-\\tau)\\,d\\tau$ 는 $\\tau=2$ 값만 골라요.",
       "$2^2+1=5$",
       "폭 0.001인 얇은 펄스로 넓이를 직접 구해도 약 $5$ 가 나와요."],
      "$5$"),
  prof("이산 임펄스는 쉬웠대요. 0에서 1이 찍히면 끝이죠.",
       "연속에서는 '수직으로 쏙 올라가는' 값이 함수가 될 수 없어서, 얇은 네모의 극한으로 정의했다고 하셨어요.",
       "0에서만 무한이고 나머지는 0인데, 대신 넓이를 1로 써 주는 느낌이래요."),
 ],
 "pass4": [
  warn("헷갈리기 쉬운 점",
      "$x(t)$ 는 적분 밖으로 나올 수 있지만 $x(\\tau)$ 는 그대로는 못 나와요.",
      "$\\tau=t$ 에서만 살아 있으니 $x(\\tau)$ 를 $x(t)$ 로 바꾼 뒤에야 밖으로 빼요."),
  check("$\\int_{-\\infty}^{\\infty} e^{\\tau}\\,\\delta(t-\\tau)\\,d\\tau$ 는?",
      ["$e^{t}$", "$e^{0}=1$", "0"], 0, "[[sift]]로 $\\tau=t$ 값 $e^{t}$ 만 남아요."),
 ]})

# ---------------- p.39 ----------------
S.append({"p": 39, "title": "펄스마다 응답, 그리고 중첩",
 "pass1": [
  say("이제 계단 모양 입력을 [[sys]]에 넣어요.",
      "칸 하나하나, 곧 얇은 펄스 하나하나가 저마다 메아리를 만들어요.",
      "메아리들을 크기대로 모두 더하면 출력이 돼요."),
  analogy("메아리 도장 찍기",
      "빈 방에서 크기가 다른 손뼉을 차례로 치면, 손뼉마다 메아리가 울리고 귀에는 메아리들이 겹쳐 들려요.",
      ["손뼉 한 번(얇은 펄스)", "$\\delta_\\Delta(t-k\\Delta)$"], ["그 손뼉의 메아리", "$\\hat{h}_{k\\Delta}(t)$"],
      ["메아리 크기", "$x(k\\Delta)\\,\\Delta$"], ["귀에 들리는 전체 소리", "출력 $\\hat{y}(t)$"]),
 ],
 "pass2": [
  formula("출력 근사식",
      r"\hat{y}(t)=\sum_{k=-\infty}^{\infty} x(k\Delta)\,\hat{h}_{k\Delta}(t)\,\Delta",
      [(r"\hat{h}_{k\Delta}(t)", "'에이치 햇': k번째 칸 펄스 $\\delta_\\Delta(t-k\\Delta)$ 를 넣었을 때 나온 응답"),
       (r"x(k\Delta)\,\Delta", "그 펄스에 곱해진 크기"),
       (r"\sum_{k}", "모두 더하기: [[sup]]")],
      "입력 조각의 합을 넣으면 응답 조각의 합이 나와요. [[lin]] 덕분이에요."),
  points("[[sup]] 다시 보기",
      "여러 입력을 더해 넣으면, 각각의 출력을 더한 것이 나와요.",
      "k배 넣으면 k배 나와요.",
      "이 둘이 [[lin]]이라서, 선형 [[sys]]에서만 이렇게 쪼개 더할 수 있어요."),
  check("$\\hat{y}(t)$ 를 펄스 응답의 합으로 쓸 수 있는 이유는?",
      ["[[lin]](중첩 원리)", "인과성", "주기성"], 0,
      "슬라이드도 'linear system's output is the superposition'이라고 써요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (0.107, 0.234, 0.825, 0.08, "입력은 크기 바꾸고 옮긴 펄스 $\\delta_\\Delta(t-k\\Delta)$ 의 합으로 근사돼요."),
      (0.35, 0.326, 0.192, 0.09, "앞 쪽의 계단 근사식 그대로예요."),
      (0.107, 0.43, 0.847, 0.08, "선형 시스템 출력 $\\hat{y}$ 는 응답 $\\hat{h}_{k\\Delta}(t)$ 들의 [[sup]]래요."),
      (0.175, 0.56, 0.27, 0.3, "(a) 곡선 $x(t)$ 와 계단 $\\hat{x}(t)$, 그리고 $\\hat{y}$ 식."),
      (0.53, 0.56, 0.25, 0.335, "(c)(d) 펄스 하나를 넣으면(왼쪽) 메아리 하나가 나와요(오른쪽).")),
  figure("펄스마다 메아리, 모두 더하면 출력", FE, "위: 입력 펄스 세 개. 아래: 메아리 세 개와 그 합.", FEB),
  steps("한 시점에서 메아리 두 개 더하기",
      ["펄스 두 개의 크기: $x(0)\\Delta=1$, $x(\\Delta)\\Delta=0.5$",
       "어떤 시점 $t$ 에서 메아리 높이: $\\hat{h}_0(t)=0.3$, $\\hat{h}_\\Delta(t)=0.6$",
       "$\\hat{y}(t)=1\\times0.3+0.5\\times0.6$",
       "$=0.3+0.3=0.6$"],
      "$\\hat{y}(t)=0.6$"),
  prof("이산에서 $\\delta[n]$ 이 $h[n]$ 으로 가면 $x[n]$ 은 $x[n]*h[n]$ 으로 갔죠.",
       "연속도 똑같대요. $\\delta(t)$ 가 $h(t)$ 로 가면 $x(t)$ 는 $x(t)*h(t)$ 로 간다고 하셨어요."),
 ],
 "pass4": [
  warn("아직 LTI 는 안 썼어요",
      "여기서 $\\hat{h}_{k\\Delta}(t)$ 는 칸마다 모양이 다를 수 있어요. [[lin]]만 썼거든요.",
      "메아리 모양이 모두 같다는 것은 p.42에서 [[ti:을]] 쓰면서 나와요."),
  check("$\\hat{h}_{k\\Delta}(t)$ 는 무엇에 대한 응답일까요?",
      ["$\\delta_\\Delta(t-k\\Delta)$", "$x(t)$", "$u(t)$"], 0,
      "k번째 칸으로 옮긴 얇은 펄스를 넣었을 때의 출력이에요."),
 ]})

# ---------------- p.40 ----------------
S.append({"p": 40, "title": "Δ→0: 메아리 합이 적분이 돼요",
 "pass1": [
  say("칸 폭을 0으로 줄이면 메아리 합이 부드러운 출력 곡선이 돼요.",
      "그림 (e)는 계단 입력과 들쭉날쭉한 출력, (f)는 매끈한 입력과 매끈한 출력이에요.",
      "오른쪽 그림의 빗금 한 줄이 메아리 하나의 몫이에요."),
 ],
 "pass2": [
  formula("극한을 취한 출력",
      r"y(t)=\lim_{\Delta\to0}\sum_{k=-\infty}^{\infty}x(k\Delta)\,\hat{h}_{k\Delta}(t)\,\Delta=\int_{-\infty}^{\infty}x(\tau)\,h_\tau(t)\,d\tau",
      [(r"\lim_{\Delta\to0}", "칸 폭을 0에 한없이 가깝게"),
       (r"h_\tau(t)", "입력 시간 $\\tau$ 에 친 손뼉의 메아리(아직 $\\tau$ 마다 따로)"),
       (r"x(\tau)\,d\tau", "그 손뼉의 크기 곱하기 아주 얇은 폭")],
      "p.37과 같은 규칙($k\\Delta\\to\\tau$, $\\Delta\\to d\\tau$)으로 합이 [[integ:이]] 됐어요."),
  check("$\\Delta\\to0$ 에서 $\\hat{h}_{k\\Delta}(t)$ 는 무엇이 될까요?",
      ["$h_\\tau(t)$", "$x(t)$", "$\\delta(t)$"], 0, "$k\\Delta$ 가 $\\tau$ 로 바뀌니까 $h_\\tau(t)$ 예요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (0.16, 0.3, 0.3, 0.19, "극한 식. 합이 적분 $\\int x(\\tau)h_\\tau(t)d\\tau$ 로 바뀌어요."),
      (0.15, 0.51, 0.31, 0.17, "(e) 계단 입력 $\\hat{x}$ 와 그 출력 $\\hat{y}$ 예요."),
      (0.15, 0.68, 0.31, 0.17, "(f) $\\Delta\\to0$: 진짜 입력 $x$ 와 진짜 출력 $y$ 예요."),
      (0.54, 0.52, 0.3, 0.31, "가로축이 τ 인 곡선 $x(\\tau)h_\\tau(t)$. 빗금 막대 넓이 $=x(k\\Delta)h_{k\\Delta}(t)\\Delta$.")),
  bg(B8,
     "[[integ]] = 곡선 아래 넓이예요.",
     "오른쪽 그림에서 빗금 막대를 모두 모은 넓이가 $y(t)$ 한 개의 값이에요."),
  prof("연속시간은 증명이 조금 어려울 수 있다고 하셨어요.",
       "'증명이 이해가 안 되면 식만 보셔도 괜찮다'고 하셨어요."),
 ],
 "pass4": [
  warn("그림 읽을 때",
      "오른쪽 그림의 가로축은 $t$ 가 아니라 $\\tau$ (입력 시간)예요.",
      "그 곡선 아래 전체 넓이가 출력 $y(t)$ 의 값 딱 하나예요."),
  check("오른쪽 그림에서 곡선 아래 전체 넓이는 무엇일까요?",
      ["어떤 한 시점의 출력 $y(t)$", "입력 $x(t)$ 전체", "[[imp]]의 넓이 1"], 0,
      "$y(t)=\\int x(\\tau)h_\\tau(t)d\\tau$ 이니 넓이가 곧 $y(t)$ 예요."),
 ]})

# ---------------- p.41 ----------------
S.append({"p": 41, "title": "근사에서 정확한 식으로 (그림 정리)",
 "pass1": [
  say("이 쪽은 앞 세 쪽을 그림 한 장으로 정리해요.",
      "왼쪽 열은 입력을 칸마다 쪼갠 펄스, 오른쪽 열은 각 펄스의 메아리예요.",
      "아래로 갈수록 '계단 합'이 '매끈한 적분'이 돼요."),
 ],
 "pass2": [
  points("그림 다섯 줄 읽기",
      "1줄: 곡선 $x(t)$ 와 계단 $\\hat{x}(t)$",
      "2줄: $x(0)\\delta_\\Delta(t)\\Delta$ 를 넣으면 $x(0)\\hat{h}_0(t)\\Delta$",
      "3줄: $x(\\Delta)\\delta_\\Delta(t-\\Delta)\\Delta$ 를 넣으면 $x(\\Delta)\\hat{h}_\\Delta(t)\\Delta$",
      "4줄: 계단 입력 전체 → 메아리 합 $\\hat{y}(t)$",
      "5줄: 매끈한 $x(t)$ → 매끈한 $y(t)=\\int x(\\tau)h_\\tau(t)d\\tau$"),
  check("그림 마지막 줄(매끈한 입력과 출력)을 나타내는 식은?",
      ["$\\hat{y}(t)=\\sum_k x(k\\Delta)\\hat{h}_{k\\Delta}(t)\\Delta$", "$y(t)=\\int x(\\tau)h_\\tau(t)d\\tau$"], 1,
      "칸 폭이 0이 된 뒤라서 합이 아니라 [[integ]]이에요."),
 ],
 "pass3": [
  look("그림 짚어 읽기",
      (0.286, 0.285, 0.16, 0.1, "맨 위: 곡선과 계단 근사."),
      (0.286, 0.4, 0.33, 0.2, "펄스 두 개와 각각의 응답. 늦게 친 펄스는 응답도 늦게 시작해요."),
      (0.636, 0.4, 0.21, 0.13, "$\\delta_\\Delta(t-k\\Delta)$ 를 넣으면 $\\hat{h}_{k\\Delta}(t)$ 가 나온다는 화살표."),
      (0.286, 0.62, 0.33, 0.24, "아래 두 줄: 계단 합 $\\hat{y}$ 와 극한 $y$."),
      (0.636, 0.64, 0.21, 0.19, "오른쪽 두 식: 합 버전과 적분 버전.")),
  prof("넓이 접근으로 합이 적분으로 바뀌는 근사 과정은 '한번 읽어보시면 된다'고 하셨어요.",
       "'그 과정을 전부 증명까지 알아두실 필요는 없다'고 하셨어요."),
 ],
 "pass4": [
  check("그림에서 펄스를 늦게 넣으면 응답은?",
      ["그만큼 늦게 시작해요", "더 일찍 시작해요", "사라져요"], 0,
      "시간을 늦추면 출력도 늦게 나와요. 다음 쪽에서 이것을 [[ti]]으로 정리해요."),
 ]})

FB, FBB = fig_block()
FF, FFB = fig_flip()
F26, F26B = fig_ex26()
F26Y, F26YB = fig_ex26y()
F27, F27B = fig_ex27()
F27Y, F27YB = fig_ex27y()
F28, F28B = fig_ex28()
F28Y, F28YB = fig_ex28y()

# ---------------- p.42 ----------------
S.append({"p": 42, "title": "LTI면 메아리는 모두 같은 모양: 컨볼루션 적분",
 "pass1": [
  say("[[ti]] 덕분에, 언제 친 손뼉이든 메아리 모양은 똑같고 늦게 시작할 뿐이에요.",
      "그래서 메아리 하나 $h(t)$ 만 알면 돼요.", M2a, M2b),
  analogy("요일과 상관없는 레시피",
      "월요일에 해도 금요일에 해도 맛이 같은 레시피처럼, $\\tau$ 초에 친 손뼉의 메아리는 0초 메아리를 $\\tau$ 만큼 늦춘 것이에요.",
      ["0초에 친 손뼉의 메아리", "$h(t)$"], ["$\\tau$ 초에 친 손뼉의 메아리", "$h(t-\\tau)$"],
      ["요일이 달라도 같은 맛", "[[ti]]"]),
 ],
 "pass2": [
  formula("[[cint]]",
      r"y(t)=\int_{-\infty}^{\infty}x(\tau)\,h(t-\tau)\,d\tau=x(t)*h(t)",
      [(r"x(\tau)", "입력 시간 $\\tau$ 의 입력 값(손뼉 크기)"),
       (r"h(t-\tau)", "그 손뼉이 지금 $t$ 에 남긴 메아리 높이"),
       (r"d\tau", "한없이 얇은 폭"),
       (r"*", "[[conv]] 기호(곱하기가 아니에요)")],
      "모든 $\\tau$ 에서 '손뼉 크기 곱하기 메아리'를 모아 넓이를 구하면 $y(t)$ 예요."),
  compare("합과 적분 나란히", ["", "[[csum]]", "[[cint]]"],
      ["식", "$\\sum_k x[k]h[n-k]$", "$\\int x(\\tau)h(t-\\tau)d\\tau$"],
      ["입력 시간", "$k$", "$\\tau$"],
      ["다른 이름", "superposition sum", "superposition integral"],
      ["짧게", "$x[n]*h[n]$", "$x(t)*h(t)$"]),
  check("[[cint]]의 다른 이름은?",
      ["superposition integral (중첩 적분)", "Fourier integral", "running sum"], 0,
      "슬라이드: 'convolution integral or the superposition integral'."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (0.107, 0.234, 0.712, 0.08, "선형이면서 시불변이면 모든 응답은 그냥 시간 이동한 모양: $h_\\tau(t)=h(t-\\tau)$."),
      (0.107, 0.326, 0.424, 0.14, "그래서 LTI의 [[conv:은]] 이 적분으로 정의돼요."),
      (0.107, 0.463, 0.569, 0.033, "이름: convolution integral 또는 superposition integral."),
      (0.107, 0.517, 0.4, 0.075, "대수 기호로는 $y(t)=x(t)*h(t)$.")),
  bg("기초 다지기 b-2 그래프 옮기기, 뒤집기, 늘이기",
     "$h(t-\\tau)$ 는 $h(t)$ 를 $\\tau$ 만큼 오른쪽으로 옮긴 것이에요. [[shift]]예요.",
     "영상으로 치면 $\\tau$ 초 늦게 튼 것이에요."),
  prof("이산의 $\\sum_k x[k]h[n-k]$ 에서 합이 적분으로 바뀌면 $\\int x(\\tau)h(t-\\tau)d\\tau$ 이고, 이게 연속시간 컨볼루션의 정의래요.",
       "'$h$ 만 잘 알면 모든 입력에 대해 컨볼루션만 취하면 $y$ 가 된다'고 하셨어요."),
 ],
 "pass4": [
  english("답안에 쓸 문장",
      "LTI 시스템의 출력은 입력과 임펄스 응답의 컨볼루션 적분 $y(t)=\\int_{-\\infty}^{\\infty}x(\\tau)h(t-\\tau)d\\tau=x(t)*h(t)$ 로 구한다.",
      "시불변이라 $h_\\tau(t)=h(t-\\tau)$, 선형이라 응답의 합(적분)이 출력이에요.",
      "'x 는 타우, h 는 t 빼기 타우'"),
  warn("헷갈리기 쉬운 점",
      "$*$ 는 곱하기가 아니라 [[conv]]예요.",
      "$h_\\tau(t)=h(t-\\tau)$ 는 [[ti]]이 있을 때만이에요. 선형이기만 하면 $\\tau$ 마다 메아리 모양이 다를 수 있어요."),
  check("$h_\\tau(t)=h(t-\\tau)$ 로 쓸 수 있게 해 주는 성질은?",
      ["[[ti]]", "인과성", "안정성"], 0, "늦게 넣으면 모양 그대로 늦게 나오는 성질이에요."),
 ]})

# ---------------- p.43 ----------------
S.append({"p": 43, "title": "임펄스 응답 h(t)와 선형 컨볼루션 (블록 그림)",
 "pass1": [
  say("위 상자: 손뼉 $\\delta(t)$ 를 넣었더니 메아리 $h(t)$ 가 나왔어요.",
      "그래서 아래처럼 상자 이름을 아예 $h(t)$ 라고 붙여요.",
      "어떤 $x(t)$ 를 넣어도 출력은 $x(t)*h(t)$ 예요."),
  figure("손뼉의 메아리가 상자의 이름", FB, "위: 임펄스를 넣어 h를 얻어요. 아래: 그 h로 모든 출력을 구해요.", FBB),
 ],
 "pass2": [
  points("그림 읽기",
      "빨간 동그라미 $h(t)$: [[ir]]",
      "'LTI system with impulse response $h(t)$': 상자를 $h(t)$ 로 부르는 이유예요.",
      "빨간 상자 'Linear convolution': $y(t)\\equiv h(t)*x(t)$. $\\equiv$ 는 '이렇게 정한다'는 뜻이에요."),
  check("상자 안에 $h(t)$ 하나만 적어도 되는 이유는?",
      ["LTI라서 h가 시스템을 완전히 정하니까", "h가 입력이라서", "그림을 줄이려고"], 0,
      "[[lti:은]] [[ir]] 하나로 모든 입력의 출력이 정해져요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (0.19, 0.27, 0.44, 0.17, "$\\delta(t)$ 를 LTI 시스템에 넣은 출력이 [[ir]] $h(t)$ 예요."),
      (0.19, 0.45, 0.45, 0.15, "그래서 이 시스템을 '[[ir]]가 $h(t)$ 인 LTI 시스템'이라 불러요."),
      (0.22, 0.67, 0.3, 0.16, "선형 [[conv]]의 정의 상자예요.")),
  prof("'$h$ 가 결정되면 시스템이 결정된다'고 하셨어요.",
       "시스템이 결정된다는 건 어떤 입력이 들어와도 출력 모양이 정해진다는 뜻이래요.",
       "그래서 상자 안에 $h$ 를 써서 시스템을 나타내는 표현이 뒤에도 나온대요."),
 ],
 "pass4": [
  warn("순서가 바뀌어 보여도",
      "빨간 상자는 $h(t)*x(t)$ 로 썼지만 적분은 $x(\\tau)h(t-\\tau)$ 예요.",
      "p.52의 [[comm]] 덕분에 둘은 같은 값이에요."),
  check("[[ir]] $h(t)$ 의 정의는?",
      ["$\\delta(t)$ 를 넣었을 때의 출력", "$u(t)$ 를 넣었을 때의 출력", "입력 신호"], 0,
      "[[imp]]를 넣었을 때의 출력이에요. 계단을 넣은 출력은 계단 응답(다음 범위)이에요."),
 ]})

# ---------------- p.44 ----------------
S.append({"p": 44, "title": "컨볼루션 적분 계산법: 뒤집고, 밀고, 곱하고, 넓이",
 "pass1": [
  say("특정 $t$ 하나에서 $y(t)$ 를 구하는 순서가 이 쪽의 주인공이에요.",
      "$h$ 를 뒤집고, $t$ 만큼 밀고, $x$ 와 곱하고, 겹친 넓이를 구해요.", M2a, M2b),
  figure("네 단계를 그림으로", FF, "h를 뒤집어 t만큼 민 뒤 x(τ)와 곱해 색칠한 넓이가 y(t)예요.", FFB),
 ],
 "pass2": [
  steps("네 단계 순서",
      ["τ 축에 $h(\\tau)$ 를 그려요.",
       "좌우로 뒤집어 $h(-\\tau)$ 를 만들어요. [[rev]]예요.",
       "$t$ 만큼 오른쪽으로 밀어 $h(t-\\tau)$ 를 만들어요. [[shift]]예요.",
       "$x(\\tau)$ 와 곱해요.",
       "곱한 그래프 아래 넓이([[integ]])가 $y(t)$ 예요."],
      "$t$ 를 바꿔 가며 반복하면 $y(t)$ 그래프 전체가 나와요."),
  compare("이산과 연속의 계산", ["", "[[csum]]", "[[cint]]"],
      ["뒤집고 밀기", "$h[n-k]$", "$h(t-\\tau)$"],
      ["곱하기", "칸마다 $x[k]h[n-k]$", "점마다 $x(\\tau)h(t-\\tau)$"],
      ["모으기", "칸 값을 더하기", "겹친 넓이 구하기"]),
  check("$h(t-\\tau)$ 를 만드는 순서로 맞는 것은?",
      ["좌우로 뒤집고 $t$ 만큼 오른쪽으로 밀기", "위아래로 뒤집기", "$t$ 만큼 왼쪽으로 밀기만"], 0,
      "$h(t-\\tau)=h(-(\\tau-t))$: 뒤집은 $h(-\\tau)$ 를 $t$ 만큼 오른쪽으로 옮긴 것이에요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (0.107, 0.234, 0.837, 0.076, "정해진 $t$ 에서: $h(t-\\tau)$ 를 구해 $x(\\tau)$ 와 곱하고 $\\tau$ 에 대해 적분하면 $y(t)$."),
      (0.3, 0.365, 0.37, 0.16, "위: 입력 F(파랑 네모)와 [[ir]] G(주황 비탈)."),
      (0.3, 0.53, 0.37, 0.14, "가운데: 뒤집힌 G가 왼쪽에서 밀려와 F와 겹치는 장면."),
      (0.3, 0.68, 0.37, 0.14, "아래: 겹친 넓이가 출력으로 한 점씩 그려져요.")),
  bg(B8,
     "적분 = 겹치는 부분의 넓이예요.",
     "두 그래프가 안 겹치면 곱이 0이라 넓이도 0이에요.",
     "많이 겹칠수록 넓이, 곧 출력이 커져요."),
  steps("그림 숫자로 넓이 구하기",
      ["$h(\\tau)=1-\\tau/2$ ($0\\le\\tau\\le2$), $x(\\tau)=1$ ($0\\le\\tau\\le3$), $t=1.5$",
       "$h(1.5-\\tau)$ 는 $-0.5\\le\\tau\\le1.5$ 에서 켜져요.",
       "$x$ 와 겹치는 곳: $0\\le\\tau\\le1.5$",
       "그 구간의 곱은 $\\tau=0$ 에서 $0.25$, $\\tau=1.5$ 에서 $1$ 인 사다리꼴",
       "넓이 $=\\frac{0.25+1}{2}\\times1.5=0.9375$"],
      "$y(1.5)=0.9375$"),
  prof("$h$ 를 필터처럼 생각해서 뒤집고 옮긴 뒤 곱한다고 하셨어요.",
       "CNN에서 필터를 움직여 가며 피처 맵을 만든 것처럼, 밀어 가며(슬라이딩) 출력을 구한대요."),
 ],
 "pass4": [
  warn("헷갈리기 쉬운 점",
      "움직이는 것은 $h(t-\\tau)$ 쪽이고, $x(\\tau)$ 는 제자리에 있어요.",
      "$h(t-\\tau)$ 는 $t>0$ 이면 오른쪽으로 가요. 1장의 '$x(t-t_0)$ 는 오른쪽' 규칙과 같아요."),
  check("$t$ 가 커질 때 $h(t-\\tau)$ 는 어디로 움직일까요?",
      ["오른쪽", "왼쪽", "움직이지 않아요"], 0, "뒤집힌 $h$ 가 왼쪽에서 오른쪽으로 밀려와요."),
 ]})

# ---------------- p.45 ----------------
S.append({"p": 45, "title": "예제 2.6 (1) 겹치는 구간 찾기",
 "pass1": [
  say("예제 2.6: 입력은 점점 줄어드는 곡선, [[sys:은]] 켜면 계속 켜져 있는 스위치 모양 $h$ 예요.",
      "$t$ 가 0보다 작으면 둘이 안 겹쳐서 출력은 0이에요.",
      "$t$ 가 0보다 크면 0부터 $t$ 까지 겹쳐요."),
  figure("밀어 보면 겹치는 곳이 보여요", F26, "위: t가 음수면 안 겹쳐요. 아래: t가 양수면 0부터 t까지 겹쳐요.", F26B),
 ],
 "pass2": [
  formula("예제의 입력과 [[ir]]",
      r"x(t)=e^{-at}u(t),\ a>0,\qquad h(t)=u(t)",
      [(r"e^{-at}", "'e 의 마이너스 at 제곱': 시간이 갈수록 줄어드는 [[expf]]"),
       (r"u(t)", "[[step]]: 0부터 켜지는 스위치"),
       (r"a>0", "a는 양수, 줄어드는 빠르기")],
      "입력은 0에서 1로 시작해 줄어드는 곡선, [[ir]]는 0부터 계속 1이에요."),
  formula("곱한 것",
      r"x(\tau)h(t-\tau)=\begin{cases}e^{-a\tau} & 0<\tau<t\\ 0 & \text{otherwise}\end{cases}",
      [(r"0<\tau", "$x(\\tau)$ 는 $\\tau>0$ 에서만 켜져요"),
       (r"\tau<t", "$h(t-\\tau)=u(t-\\tau)$ 는 $\\tau<t$ 에서만 1"),
       (r"e^{-a\tau}", "둘 다 켜진 곳에서는 $e^{-a\\tau}\\times1$")],
      "겹치는 구간은 $0<\\tau<t$ 이고, 그 구간이 있으려면 $t>0$ 이어야 해요."),
  check("$t<0$ 일 때 $y(t)$ 는?", ["0", "$1/a$", "1"], 0,
      "안 겹치니 곱이 0, 넓이도 0이에요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (0.151, 0.334, 0.496, 0.105, "예제 2.6: $x(t)=e^{-at}u(t)$, $a>0$, $h(t)=u(t)$."),
      (0.209, 0.566, 0.271, 0.105, "$t>0$ 일 때 곱은 $0<\\tau<t$ 에서 $e^{-a\\tau}$, 나머지 0."),
      (0.728, 0.27, 0.204, 0.18, "$h(\\tau)=u(\\tau)$: 0부터 1."),
      (0.728, 0.46, 0.204, 0.12, "$x(\\tau)$: 1에서 시작해 줄어드는 곡선."),
      (0.728, 0.6, 0.204, 0.13, "$t<0$: 뒤집어 민 $h(t-\\tau)$ 가 $t$ 에서 끝나 $x$ 와 안 겹쳐요."),
      (0.728, 0.74, 0.204, 0.13, "$t>0$: 0부터 $t$ 까지 겹쳐요.")),
  steps("겹치는 구간 찾기",
      ["$u(t-\\tau)$ 는 $t-\\tau>0$, 곧 $\\tau<t$ 에서 1이에요.",
       "$x(\\tau)$ 는 $\\tau>0$ 에서만 값이 있어요.",
       "둘 다 켜진 곳: $0<\\tau<t$",
       "$t<0$ 이면 그런 $\\tau$ 가 없어요. 그래서 $y(t)=0$"],
      "$t>0$ 일 때 겹침 구간은 $0<\\tau<t$"),
  bg("기초 다지기 b-4 지수함수와 e",
     "$e^{-\\tau}$ 는 $\\tau=0$ 에서 $1$, $\\tau=1$ 에서 약 $0.368$, $\\tau=2$ 에서 약 $0.135$ 예요.",
     "$e$ 는 약 $2.718$ 인 수예요."),
  prof("$t$ 가 0보다 작으면 겹치는 넓이가 하나도 없어서 적분해도 0이래요.",
       "$t$ 가 0보다 커지는 순간 조금 겹치고, 갈수록 겹치는 넓이가 커진대요.",
       "그런데 커지는 폭은 점점 줄어들어서 결국 포화(세츄레이션)된다고 하셨어요."),
 ],
 "pass4": [
  warn("헷갈리기 쉬운 점",
      "적분 변수는 $\\tau$ 이고 $t$ 는 고정된 숫자처럼 다뤄요.",
      "겹침 구간의 끝이 $t$ 라서 답에 $t$ 가 들어가요."),
  check("$t=2$ 일 때 겹치는 구간은?",
      ["$0<\\tau<2$", "$-2<\\tau<0$", "$\\tau>2$"], 0, "$0<\\tau<t$ 에 $t=2$ 를 넣어요."),
 ]})

# ---------------- p.46 ----------------
S.append({"p": 46, "title": "예제 2.6 (2) 넓이 계산과 답",
 "pass1": [
  say("겹친 부분의 넓이가 곧 출력이에요.",
      "처음엔 빨리 늘다가 점점 천천히 늘어서 $1/a$ 에 가까워져요."),
  figure("출력은 1/a 로 차올라요", F26Y, "a = 1 인 경우. y(1), y(2)를 점으로 찍었어요.", F26YB),
 ],
 "pass2": [
  formula("넓이 계산",
      r"y(t)=\int_0^t e^{-a\tau}\,d\tau=-\frac{1}{a}e^{-a\tau}\Big|_0^t=\frac{1}{a}\left(1-e^{-at}\right)",
      [(r"\int_0^t", "0부터 $t$ 까지의 넓이([[integ]])"),
       (r"-\frac{1}{a}e^{-a\tau}", "[[deriv]]하면 $e^{-a\\tau}$ 가 되는 함수(넓이를 재는 함수)"),
       (r"\Big|_0^t", "$t$ 를 넣은 값에서 0을 넣은 값을 빼요")],
      "$(-\\frac1a e^{-at})-(-\\frac1a)=\\frac1a(1-e^{-at})$ 예요."),
  formula("모든 t에 대한 답",
      r"y(t)=\frac{1}{a}\left(1-e^{-at}\right)u(t)",
      [(r"\frac{1}{a}\left(1-e^{-at}\right)", "$t>0$ 에서의 넓이"),
       (r"u(t)", "$t<0$ 에서는 0이라서 [[step]]을 곱해 한 줄로 써요")],
      "0에서 시작해 $1/a$ 로 차오르는 곡선이에요."),
  check("$t$ 가 아주 커지면 $y(t)$ 는?", ["$1/a$", "0", "무한대"], 0,
      "$e^{-at}$ 가 0으로 가서 $\\frac1a(1-0)=\\frac1a$ 예요."),
 ],
 "pass3": [
  bg(B8,
     "적분 = 겹치는 부분의 넓이예요.",
     "공식처럼 써도 돼요: $\\int e^{c\\tau}d\\tau=\\frac{1}{c}e^{c\\tau}$",
     "여기서는 $c=-a$ 라서 $-\\frac{1}{a}e^{-a\\tau}$ 가 나와요."),
  steps("$a=1$, $t=1$ 손계산",
      ["겹침 구간: $0<\\tau<1$",
       "넓이 함수: $-e^{-\\tau}$",
       "$(-e^{-1})-(-e^{0})=1-e^{-1}$",
       "$e^{-1}\\approx0.368$ 이니 $1-0.368=0.632$"],
      "$y(1)\\approx0.632$"),
  steps("$a=1$, $t=2$ 손계산",
      ["겹침 구간: $0<\\tau<2$",
       "$(-e^{-2})-(-e^{0})=1-e^{-2}$",
       "$e^{-2}\\approx0.135$ 이니 $1-0.135=0.865$"],
      "$y(2)\\approx0.865$ ($t=1$ 보다 크지만, 늘어난 폭은 줄었어요)"),
  steps("일반 공식 확인",
      ["공식 $\\frac1a(1-e^{-at})$ 에 $a=1$, $t=1$: $0.632$",
       "$a=1$, $t=2$: $0.865$",
       "$a=2$, $t=1$: $\\frac12(1-e^{-2})\\approx0.432$",
       "Python으로 구간을 잘게 쪼개 넓이를 더해도 세 값이 똑같이 나와요."],
      "$y(t)=\\frac1a(1-e^{-at})u(t)$ 가 맞아요."),
  look("슬라이드 짚어 읽기",
      (0.212, 0.366, 0.222, 0.135, "$t>0$ 에서 적분 계산. 넓이 함수에 $t$ 와 0을 넣어 빼요."),
      (0.151, 0.541, 0.2, 0.11, "모든 $t$: $u(t)$ 를 붙인 답."),
      (0.613, 0.326, 0.3, 0.344, "그래프: 0에서 시작해 점선 $1/a$ 로 다가가요.")),
  prof("컨볼루션 개념만 이해하면 나머지는 사실상 단순한 적분 산수라고 하셨어요."),
 ],
 "pass4": [
  exam("교재 Example 2.6 (p.45~46), 연습 문제",
      "$x(t)=e^{-at}u(t)$ ($a>0$), $h(t)=u(t)$ 일 때 $y(t)=x(t)*h(t)$ 를 구하라.",
      "줄어드는 곡선을 켜진 스위치 모양 시스템에 넣은 출력을 구해요.",
      ["$h$ 를 뒤집어 $t$ 만큼 밀면 $\\tau<t$ 에서 1",
       "$t<0$: 안 겹침, $y=0$",
       "$t>0$: 겹침 $0<\\tau<t$, $y=\\int_0^t e^{-a\\tau}d\\tau$",
       "$=\\frac1a(1-e^{-at})$"],
      "$y(t)=\\frac1a(1-e^{-at})u(t)$"),
  warn("헷갈리기 쉬운 점",
      "끝에 $u(t)$ 를 빼먹지 마세요. $t<0$ 에서 0이라는 정보예요.",
      "$t\\to\\infty$ 극한은 1이 아니라 $1/a$ 예요."),
  check("$a=1$, $t=1$ 일 때 $y(t)$ 는?", ["약 $0.632$", "약 $0.368$", "$1$"], 0,
      "$1-e^{-1}\\approx1-0.368=0.632$"),
 ]})

# ---------------- p.47 ----------------
S.append({"p": 47, "title": "예제 2.7 (1) 범위를 다섯 개로 나누기",
 "pass1": [
  say("예제 2.7: 네모 입력과 비스듬한 비탈 모양 $h$ 예요.",
      "$h$ 를 뒤집어 왼쪽에서 오른쪽으로 밀면 겹침이 '없음, 조금, 많이, 조금, 없음'으로 바뀌어요.",
      "그래서 $t$ 의 범위를 다섯 개로 나눠요."),
  figure("한 순간을 멈춰 본 모습", F27, "T = 1, t = 1.5 일 때. 색칠한 곳이 겹친 넓이예요.", F27B),
 ],
 "pass2": [
  formula("예제의 입력과 [[ir]]",
      r"x(t)=\begin{cases}1 & 0<t<T\\ 0 & \text{otherwise}\end{cases},\qquad h(t)=\begin{cases}t & 0<t<2T\\ 0 & \text{otherwise}\end{cases}",
      [(r"x(t)", "높이 1, 길이 T인 네모"),
       (r"h(t)=t", "0부터 2T까지 기울기 1로 올라가는 비탈(끝에서 뚝 떨어짐)"),
       (r"T", "길이를 나타내는 양수 상수")],
      "뒤집은 $h(t-\\tau)$ 는 $\\tau=t-2T$ 에서 높이 2T, $\\tau=t$ 에서 높이 0인 비탈이에요."),
  compare("다섯 경우", ["t 범위", "겹침", "y(t)"],
      ["$t<0$", "없음", "$0$"],
      ["$0<t<T$", "일부 ($0$ ~ $t$)", "$\\frac12t^2$"],
      ["$T<t<2T$", "x 전체 ($0$ ~ $T$)", "$Tt-\\frac12T^2$"],
      ["$2T<t<3T$", "일부 ($t-2T$ ~ $T$)", "$-\\frac12t^2+Tt+\\frac32T^2$"],
      ["$t>3T$", "없음", "$0$"]),
  check("겹침이 전혀 없는 범위를 모두 고르면?",
      ["$t<0$ 과 $t>3T$", "$0<t<T$", "$T<t<2T$"], 0,
      "비탈이 네모에 닿기 전($t<0$)과 다 지나간 뒤($t>3T$)예요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기 (왼쪽)",
      (0.13, 0.32, 0.17, 0.14, "입력 네모와 [[ir]] 비탈의 정의."),
      (0.075, 0.62, 0.265, 0.175, "다섯 범위로 나눈 답 $y(t)$."),
      (0.39, 0.35, 0.255, 0.1, "$x(\\tau)$: 0부터 T까지 높이 1.")),
  look("슬라이드 짚어 읽기 (오른쪽)",
      (0.39, 0.49, 0.255, 0.16, "$t<0$: 비탈이 네모 왼쪽에 있어 안 겹쳐요."),
      (0.39, 0.67, 0.255, 0.16, "$0<t<T$: 비탈 끝이 네모 안으로 조금 들어왔어요."),
      (0.69, 0.32, 0.255, 0.15, "$T<t<2T$: 네모 전체가 비탈 아래에 있어요."),
      (0.69, 0.5, 0.255, 0.15, "$2T<t<3T$: 비탈 왼쪽 끝 $t-2T$ 가 네모 안으로 들어와 빠져나가는 중."),
      (0.69, 0.67, 0.255, 0.16, "$t>3T$: 다 지나가서 안 겹쳐요.")),
  bg(B8, "적분 = 겹치는 부분의 넓이예요.",
     "여기서는 곱한 그래프가 삼각형이나 사다리꼴이라 넓이 공식으로도 구할 수 있어요."),
  steps("$T=1$, $t=1.5$ 겹친 넓이",
      ["$h(t-\\tau)=t-\\tau$ 는 $t-2<\\tau<t$, 곧 $-0.5<\\tau<1.5$ 에서 켜져요.",
       "$x$ 는 $0<\\tau<1$ 이라 겹침은 $0<\\tau<1$",
       "곱 $=1.5-\\tau$: $\\tau=0$ 에서 $1.5$, $\\tau=1$ 에서 $0.5$ 인 사다리꼴",
       "넓이 $=\\frac{1.5+0.5}{2}\\times1=1$"],
      "$y(1.5)=1$. 공식 $Tt-\\frac12T^2=1.5-0.5=1$ 과 같아요."),
  prof("겹침이 '노 오버랩, 파셜 오버랩, 풀 오버랩, 다시 파셜, 다시 노 오버랩'으로 바뀐다고 하셨어요.",
       "'컨볼루션을 계산할 때는 이렇게 범위를 나눠야 된다'고 강조하셨어요."),
 ],
 "pass4": [
  warn("경계 찾는 요령",
      "뒤집은 비탈의 양 끝 $t-2T$, $t$ 가 네모의 양 끝 $0$, $T$ 를 지나는 순간이 경계예요.",
      "$t=0$, $t=T$, $t-2T=0$ ($t=2T$), $t-2T=T$ ($t=3T$). 그래서 경계는 $0, T, 2T, 3T$."),
  check("예제 2.7에서 범위 경계가 아닌 것은?", ["$t=4T$", "$t=T$", "$t=2T$"], 0,
      "경계는 $0, T, 2T, 3T$ 네 곳이에요."),
 ]})

# ---------------- p.48 ----------------
S.append({"p": 48, "title": "예제 2.7 (2) 곱한 모양과 y(t) 그래프",
 "pass1": [
  say("각 범위에서 곱한 그래프 모양 (a)(b)(c)와 결과 $y(t)$ 예요.",
      "$y(t)$ 는 0에서 시작해 $2T$ 에서 가장 높고, $3T$ 에서 다시 0이 돼요."),
  figure("y(t)는 올랐다 내려와요", F27Y, "T = 1. 점은 t = 0.5, 1.5, 2.5 에서의 값이에요.", F27YB),
 ],
 "pass2": [
  points("(a)(b)(c) 읽기",
      "(a) $0<t<T$: $0$ 부터 $t$ 까지 삼각형, 높이 $t$. 넓이 $\\frac12t^2$",
      "(b) $T<t<2T$: $0$ 부터 $T$ 까지 사다리꼴, 높이 $t$ 와 $t-T$",
      "(c) $2T<t<3T$: $t-2T$ 부터 $T$ 까지 사다리꼴, 높이 $2T$ 와 $t-T$"),
  check("(b) 범위의 넓이 $Tt-\\frac12T^2$ 를 사다리꼴 공식으로 쓰면?",
      ["$\\frac{t+(t-T)}{2}\\times T$", "$\\frac12t^2$", "$t\\times2T$"], 0,
      "윗변 $t$, 아랫변 $t-T$, 높이(폭) $T$ 인 사다리꼴이에요. 펼치면 $Tt-\\frac12T^2$."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (0.405, 0.28, 0.23, 0.14, "(a) $0<t<T$: 곱한 모양이 삼각형."),
      (0.405, 0.47, 0.23, 0.15, "(b) $T<t<2T$: 네모 폭 전체의 사다리꼴."),
      (0.405, 0.67, 0.23, 0.17, "(c) $2T<t<3T$: 빠져나가는 중의 사다리꼴."),
      (0.715, 0.44, 0.22, 0.21, "결과 $y(t)$: $0$ 에서 $3T$ 까지만 값이 있어요.")),
  steps("$T=1$ 로 세 점 손계산",
      ["$t=0.5$ (a): 삼각형 $\\frac12\\times0.5\\times0.5=0.125$",
       "$t=1.5$ (b): 사다리꼴 $\\frac{1.5+0.5}{2}\\times1=1$",
       "$t=2.5$ (c): 겹침 $0.5<\\tau<1$, 높이 $2$ 와 $1.5$ 라서 $\\frac{2+1.5}{2}\\times0.5=0.875$",
       "공식 확인: $-\\frac12(2.5)^2+2.5+1.5=0.875$"],
      "$y(0.5)=0.125$, $y(1.5)=1$, $y(2.5)=0.875$"),
  steps("가장 높은 곳",
      ["$t=2T$ 에서 (b)와 (c) 공식이 만나요.",
       "$T\\cdot2T-\\frac12T^2=\\frac32T^2$",
       "$T=1$ 이면 $1.5$"],
      "최댓값 $\\frac32T^2$ ($t=2T$)"),
  prof("이 계산은 '수학적인 산술이라 직접 해 보시면 된다, 어렵지 않다'고 하셨어요.",
       "예제 2.7도 연습해 보라고 하셨어요."),
 ],
 "pass4": [
  exam("교재 Example 2.7 (p.47~48), 연습 문제",
      "$T=1$ 일 때 예제 2.7의 $y(2.5)$ 를 구하라.",
      "네모 입력과 비탈 [[ir]]의 [[conv]]를 한 점에서 구해요.",
      ["$2T<t<3T$ 범위라 겹침은 $t-2<\\tau<1$, 곧 $0.5<\\tau<1$",
       "곱은 $t-\\tau=2.5-\\tau$: 양 끝 높이 $2$, $1.5$",
       "넓이 $=\\frac{2+1.5}{2}\\times0.5=0.875$"],
      "$y(2.5)=0.875$"),
  warn("그림 읽을 때",
      "(a)(b)(c)의 세로축은 곱 $x(\\tau)h(t-\\tau)$, 가로축은 $\\tau$ 예요.",
      "오른쪽 $y(t)$ 그래프만 가로축이 $t$ 예요."),
  check("예제 2.7의 $y(t)$ 가 가장 큰 때는?", ["$t=2T$", "$t=T$", "$t=3T$"], 0,
      "네모 전체가 비탈의 가장 높은 쪽과 겹칠 때예요. 값은 $\\frac32T^2$."),
 ]})

# ---------------- p.49 ----------------
S.append({"p": 49, "title": "예제 2.8: t = 3 이 분기점",
 "pass1": [
  say("예제 2.8: 입력은 왼쪽(과거)에만 있는 곡선, $h$ 는 3초 늦게 켜지는 스위치예요.",
      "뒤집어 민 스위치의 끝이 $t-3$ 에 있어서, $t=3$ 을 기준으로 식이 달라져요."),
  figure("스위치 끝이 어디냐에 따라", F28, "위: t = 2 이면 끝이 -1. 아래: t = 5 이면 입력 전체가 겹쳐요.", F28B),
 ],
 "pass2": [
  formula("예제의 입력과 [[ir]]",
      r"x(t)=e^{2t}u(-t),\qquad h(t)=u(t-3)",
      [(r"u(-t)", "[[step]]을 좌우로 뒤집은 것: $t\\le0$ 에서만 1"),
       (r"e^{2t}", "$t$ 가 음수로 갈수록 0에 가까워지는 [[expf]], $t=0$ 에서 1"),
       (r"u(t-3)", "3초 늦게 켜지는 스위치([[shift]])")],
      "$h(t-\\tau)=u(t-3-\\tau)$ 는 $\\tau<t-3$ 에서 1이에요."),
  compare("두 경우", ["경우", "겹침", "y(t)"],
      ["$t\\le3$ ($t-3\\le0$)", "$-\\infty<\\tau<t-3$", "$\\frac12e^{2(t-3)}$"],
      ["$t>3$", "$-\\infty<\\tau<0$", "$\\frac12$"]),
  check("예제 2.8의 분기점은?", ["$t=3$", "$t=0$", "$t=-3$"], 0,
      "스위치 끝 $t-3$ 이 입력 끝 0을 지나는 순간, $t-3=0$ 이에요."),
 ],
 "pass3": [
  bg(B8, "적분 = 겹치는 부분의 넓이예요.",
     "이번에는 왼쪽 끝이 $-\\infty$ 예요. 곡선이 빠르게 0으로 줄어서 넓이는 유한해요.",
     "$\\int e^{2\\tau}d\\tau=\\frac12e^{2\\tau}$, 그리고 $\\tau\\to-\\infty$ 에서 $e^{2\\tau}\\to0$."),
  steps("$t=2$ ($t\\le3$ 경우)",
      ["스위치 끝: $t-3=-1$, 그래서 $h(2-\\tau)$ 는 $\\tau<-1$ 에서 1",
       "$x$ 는 $\\tau<0$ 에서 $e^{2\\tau}$ 라서 겹침은 $\\tau<-1$",
       "넓이 $=\\frac12e^{2\\tau}\\Big|_{-\\infty}^{-1}=\\frac12e^{-2}-0$",
       "$\\approx0.5\\times0.135=0.068$"],
      "$y(2)\\approx0.068$ (공식 $\\frac12e^{2(2-3)}$ 과 같아요)"),
  steps("$t=5$ ($t>3$ 경우)",
      ["스위치 끝: $t-3=2$, 그래서 $\\tau<2$ 에서 1",
       "그런데 $x$ 는 $\\tau<0$ 에서만 있어서 겹침은 $\\tau<0$",
       "넓이 $=\\frac12e^{2\\tau}\\Big|_{-\\infty}^{0}=\\frac12e^{0}-0=\\frac12$"],
      "$y(5)=0.5$"),
  figure("y(t) 전체 모양", F28Y, "t = 3 까지 차오르다가 그 뒤로 1/2로 평평해요.", F28YB),
  look("슬라이드 짚어 읽기",
      (0.249, 0.322, 0.11, 0.07, "입력 $e^{2t}u(-t)$ 와 [[ir]] $u(t-3)$."),
      (0.208, 0.486, 0.183, 0.08, "$t-3<0$ 일 때: 넓이가 $\\frac12e^{2(t-3)}$."),
      (0.13, 0.572, 0.516, 0.076, "$t-3\\ge0$ 이면 곱은 $-\\infty<\\tau<0$ 에서 살아 있대요."),
      (0.234, 0.669, 0.14, 0.07, "그때 넓이는 $\\frac12$."),
      (0.678, 0.43, 0.207, 0.2, "(a) 뒤집어 민 스위치: 끝이 $t-3$."),
      (0.678, 0.68, 0.207, 0.2, "(b) 결과: $t=3$ 까지 올라가고 그 뒤로 $\\frac12$.")),
  prof("$h(t)=u(t-3)$ 은 $u(t)$ 를 3만큼 오른쪽으로 옮긴 것이라고 하셨어요.",
       "뒤집고 $t$ 만큼 옮기면 끝이 $t-3$ 이 되고, '$t-3$ 이 0이 되는 $t=3$ 이 분기점'이래요.",
       "분기점 앞과 뒤에서 식이 따로 나온다고 하셨어요."),
 ],
 "pass4": [
  exam("교재 Example 2.8 (p.49), 연습 문제",
      "$x(t)=e^{2t}u(-t)$, $h(t)=u(t-3)$ 일 때 $y(t)$ 를 구하고 $y(2)$, $y(5)$ 를 구하라.",
      "과거에만 있는 입력을 3초 늦은 스위치에 넣은 출력이에요.",
      ["$h(t-\\tau)=1$ 인 곳: $\\tau<t-3$",
       "$t\\le3$: $y=\\int_{-\\infty}^{t-3}e^{2\\tau}d\\tau=\\frac12e^{2(t-3)}$",
       "$t>3$: $y=\\int_{-\\infty}^{0}e^{2\\tau}d\\tau=\\frac12$",
       "$y(2)=\\frac12e^{-2}\\approx0.068$, $y(5)=0.5$"],
      "$y(t)=\\frac12e^{2(t-3)}$ ($t\\le3$), $\\frac12$ ($t>3$). $y(2)\\approx0.068$, $y(5)=0.5$"),
  warn("슬라이드에서 조심할 곳",
      "첫 식 $\\int_{-\\infty}^{t-3}$ 옆에 '$t-3<0$ 일 때'라는 조건이 빠져 있어요. 이 식은 $t\\le3$ 에서만 맞아요.",
      "$t=3$ 에서 두 식 모두 $\\frac12$ 라서 그래프가 끊기지 않고 이어져요."),
  check("예제 2.8에서 $y(3)$ 은?", ["$\\frac12$", "0", "$\\frac12e^{-6}$"], 0,
      "$\\frac12e^{2(3-3)}=\\frac12e^0=\\frac12$"),
 ]})

# @@END@@

# ---------------- 저장 ----------------
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


slides, used = [], []
for s in S:
    s2 = T(s)
    body = " ".join(_text([s2.get(f"pass{i}", []) for i in range(1, 5)]))
    terms = []
    for key in TERMS:
        if disp(key) in body:
            terms.append(TERMS[key][1])
            if key not in used:
                used.append(key)
    slides.append({"p": s2["p"], "title": s2["title"], "terms": terms,
                   **{f"pass{i}": s2.get(f"pass{i}", []) for i in range(1, 5)}})
out = {"deck": "S3", "from": 34, "to": 62, "glossary": [gloss_entry(k) for k in used], "slides": slides}
raw = json.dumps(out, ensure_ascii=False, indent=1)
for ch in BAD:
    if ch in raw:
        i = raw.index(ch)
        raise ValueError(f"금지 문자 {ch!r}: {raw[max(0, i - 40):i + 10]}")
allbody = " ".join(_text(slides)).lower()
for k in used:
    ko, en = TERMS[k]
    c = max(allbody.count(ko.lower()), allbody.count(en.lower()))
    if c < 3:
        print("  용어 3번 미만:", ko, c)
with open(OUT, "w", encoding="utf-8") as fp:
    fp.write(raw)
print(f"저장 {OUT}: 쪽 {len(slides)}, 용어 {len(used)}")
