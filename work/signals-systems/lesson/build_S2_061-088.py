# S2(2주차 1장) 회독 레슨 61~88쪽 생성기. 사용: python build_S2_061-088.py
# 범위: 1.5 끝(시스템 차수, 연결), 1.6 시스템의 성질, 1장 과제(p.86~88)
import os, math, cmath
HERE = os.path.dirname(os.path.abspath(__file__))

# ===================== 도우미 =====================
import json, math, os, re

DICT = json.load(open(os.path.join(HERE, "..", "rules", "용어사전.json"), encoding="utf-8"))

MANTRA = "신호는 시간에 따라 변하는 값, 시스템은 신호를 바꾸는 상자."
MANTRA_LTI = "LTI 시스템은 임펄스 응답 하나만 알면 된다. 출력은 뒤집고, 밀고, 곱하고, 더해서(컨볼루션) 구한다."

TERMS = {
    "sig": ("신호", "Signal"),
    "sys": ("시스템", "System"),
    "inp": ("입력 신호", "Input Signal"),
    "out": ("출력 신호", "Output Signal"),
    "ct": ("연속시간 신호", "Continuous-Time Signal"),
    "dt": ("이산시간 신호", "Discrete-Time Signal"),
    "ode": ("미분방정식", "Differential Equation"),
    "dde": ("차분방정식", "Difference Equation"),
    "rc": ("RC 회로", "RC Circuit"),
    "order": ("시스템 차수", "Order"),
    "ser": ("직렬 연결", "Series Interconnection"),
    "par": ("병렬 연결", "Parallel Interconnection"),
    "fb": ("되먹임 연결", "Feedback Interconnection"),
    "mem": ("기억성", "Memory"),
    "memless": ("무기억 시스템", "Memoryless System"),
    "inv": ("가역성", "Invertibility"),
    "invsys": ("역시스템", "Inverse System"),
    "caus": ("인과성", "Causality"),
    "stab": ("안정성", "Stability"),
    "bibo": ("BIBO 안정", "Bounded-Input Bounded-Output"),
    "ti": ("시불변성", "Time Invariance"),
    "lin": ("선형성", "Linearity"),
    "add": ("가산성", "Additivity"),
    "homo": ("동차성", "Homogeneity"),
    "sup": ("중첩 원리", "Superposition"),
    "lti": ("LTI 시스템", "Linear Time-Invariant System"),
    "acc": ("누산기", "Accumulator"),
    "ma": ("이동 평균", "Moving Average"),
    "udelay": ("단위 지연", "Unit Delay"),
    "imp": ("단위 임펄스", "Unit Impulse"),
    "step": ("단위 계단", "Unit Step"),
    "shift": ("시간 이동", "Time Shift"),
    "delay": ("지연", "Delay"),
    "rev": ("시간 반전", "Time Reversal"),
    "scale": ("시간 척도 변환", "Time Scaling"),
    "per": ("주기 신호", "Periodic Signal"),
    "fp": ("기본 주기", "Fundamental Period"),
    "cexp": ("복소 지수 신호", "Complex Exponential Signal"),
    "sinus": ("정현파 신호", "Sinusoidal Signal"),
    "omega": ("각주파수", "Angular Frequency"),
    "euler": ("오일러 공식", "Euler's Formula"),
    "cplx": ("복소수", "Complex Number"),
    "jj": ("허수 단위", "Imaginary Unit"),
    "ir": ("임펄스 응답", "Impulse Response"),
    "conv": ("컨볼루션", "Convolution"),
    "incl": ("증분 선형 시스템", "Incrementally Linear System"),
    "zir": ("영입력 응답", "Zero-Input Response"),
}

# 사전에 없는 새 용어(보고서에 적는다)
NEW = {
    "incl": {"say": "선형 시스템에 늘 같은 값을 더해 준 시스템",
             "more": "y[n]=2x[n]+3 처럼 생긴 시스템이에요. 그 자체는 선형이 아니지만, 두 입력에 대한 출력의 차이는 선형처럼 움직여요."},
    "zir": {"say": "입력을 0으로 넣어도 나오는 출력",
            "more": "y[n]=2x[n]+3 에서는 입력이 0이어도 3이 나와요. 이 3을 영입력 응답 y0 라고 불러요."},
}

JOSA = {
    "은": ("은", "는"), "이": ("이", "가"), "을": ("을", "를"), "과": ("과", "와"),
    "으로": ("으로", "로"), "이라고": ("이라고", "라고"), "이라는": ("이라는", "라는"),
    "이에요": ("이에요", "예요"), "이나": ("이나", "나"), "이고": ("이고", "고"),
    "이죠": ("이죠", "죠"), "이라서": ("이라서", "라서"), "이란": ("이란", "란"),
    "이지만": ("이지만", "지만"), "이면": ("이면", "면"), "이랑": ("이랑", "랑"),
}


def _fin(key):
    c = TERMS[key][0][-1]
    jong = (ord(c) - 0xAC00) % 28
    return 0 if jong == 0 else (2 if jong == 8 else 1)


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
    if key in NEW:
        return {"ko": ko, "en": en, **NEW[key]}
    for d in DICT:
        if d.get("ko") == ko and d.get("en") == en:
            g = {"ko": ko, "en": en, "say": d["say"]}
            if d.get("more"):
                g["more"] = d["more"]
            return g
    raise KeyError(f"사전에 없음 {key}")


# ---------------- 장면 ----------------
PW, PH = 1400, 788  # 작성용 PNG 크기


def say(*lines):
    return {"kind": "say", "lines": list(lines)}


def look(head, *boxes):
    """boxes: (x1, y1, x2, y2, 설명) PNG 픽셀(1400x788) 기준"""
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
            "parts": [{"sym": s, "say": w} for s, w in parts], "whole": whole}


def steps(head, stps, answer, given=None):
    d = {"kind": "steps", "head": head}
    if given:
        d["given"] = given
    d["steps"] = list(stps)
    d["answer"] = answer
    return d


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


def prof(when, *lines):
    return {"kind": "prof", "when": when, "lines": list(lines)}


W2 = "2주차 목요일 수업"
W3 = "3주차 목요일 수업"


# ---------------- SVG ----------------
def _b(b):
    return f" b{b}" if b else ""


def _f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".") if isinstance(v, float) else str(v)


def TX(x, y, s, cls="t", fs=15, anc="middle", b=0):
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f'<text x="{_f(x)}" y="{_f(y)}" font-size="{fs}" text-anchor="{anc}" class="{cls}{_b(b)}">{s}</text>'


def R(x, y, w, h, cls="box", b=0, rx=2):
    return f'<rect x="{_f(x)}" y="{_f(y)}" width="{_f(w)}" height="{_f(h)}" rx="{rx}" class="{cls}{_b(b)}"/>'


def C(x, y, r, cls="n", b=0):
    return f'<circle cx="{_f(x)}" cy="{_f(y)}" r="{_f(r)}" class="{cls}{_b(b)}"/>'


def L(x1, y1, x2, y2, cls="e", b=0):
    return f'<line x1="{_f(x1)}" y1="{_f(y1)}" x2="{_f(x2)}" y2="{_f(y2)}" class="{cls}{_b(b)}"/>'


def PL(pts, cls="e2", b=0):
    s = " ".join(f"{_f(float(x))},{_f(float(y))}" for x, y in pts)
    return f'<polyline points="{s}" fill="none" class="{cls}{_b(b)}"/>'


def A(x1, y1, x2, y2, cls="e2", b=0):
    ang = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 - 9 * math.cos(ang), y2 - 9 * math.sin(ang)
    px, py = -math.sin(ang) * 5, math.cos(ang) * 5
    pts = f"{x2:.0f},{y2:.0f} {hx + px:.0f},{hy + py:.0f} {hx - px:.0f},{hy - py:.0f}"
    return L(x1, y1, round(hx), round(hy), cls, b) + f'<polygon points="{pts}" class="arrow{_b(b)}"/>'


def BOX(x, y, w, h, label, cls="box", tcls="tb", b=0, fs=15):
    return R(x, y, w, h, cls, b) + TX(x + w / 2, y + h / 2 + fs // 3 + 1, label, tcls, fs, "middle", b)


def SVG(*parts, h=270):
    return f'<svg viewBox="0 0 480 {h}" xmlns="http://www.w3.org/2000/svg">' + "".join(parts) + "</svg>"


class Plot:
    """값 좌표 -> 픽셀. (x0,x1) 값 범위를 (px0,px1) 픽셀로, (y0,y1) 을 (py0 아래, py1 위) 로"""

    def __init__(self, xr, yr, pxr, pyr):
        self.xr, self.yr, self.pxr, self.pyr = xr, yr, pxr, pyr

    def X(self, x):
        (a, b), (p, q) = self.xr, self.pxr
        return p + (x - a) / (b - a) * (q - p)

    def Y(self, y):
        (a, b), (p, q) = self.yr, self.pyr
        return p + (y - a) / (b - a) * (q - p)

    def axes(self, xlab="t", b=0):
        y0 = self.Y(0)
        x0 = self.X(0) if self.xr[0] <= 0 <= self.xr[1] else self.pxr[0]
        return (L(self.pxr[0] - 6, y0, self.pxr[1] + 8, y0, "e", b)
                + L(x0, self.pyr[0] + 4, x0, self.pyr[1] - 6, "e", b)
                + TX(self.pxr[1] + 12, y0 + 5, xlab, "tm", 14, "start", b))

    def curve(self, f, a, bnd, n=80, cls="e2", b=0):
        pts = [(self.X(a + (bnd - a) * i / n), self.Y(f(a + (bnd - a) * i / n))) for i in range(n + 1)]
        return PL(pts, cls, b)

    def poly(self, pts, cls="e2", b=0):
        return PL([(self.X(x), self.Y(y)) for x, y in pts], cls, b)

    def stem(self, n, v, cls="n2", b=0, r=4):
        return L(self.X(n), self.Y(0), self.X(n), self.Y(v), "e2", b) + C(self.X(n), self.Y(v), r, cls, b)

    def xtick(self, x, lab, b=0, dy=18):
        return L(self.X(x), self.Y(0) - 3, self.X(x), self.Y(0) + 3, "e", b) + TX(self.X(x), self.Y(0) + dy, lab, "tm", 14, "middle", b)

    def ytick(self, y, lab, b=0):
        x0 = self.X(0) if self.xr[0] <= 0 <= self.xr[1] else self.pxr[0]
        return L(x0 - 3, self.Y(y), x0 + 3, self.Y(y), "e", b) + TX(x0 - 6, self.Y(y) + 5, lab, "tm", 14, "end", b)


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


_MATH = re.compile(r"\$[^$\n]+?\$")
_LONE = re.compile(r"(?<= )(\d+)(?= )")


def _wrapnum(s):
    """엔진 숫자 버그 피하기: 수식 밖에서 공백 사이에 홀로 선 숫자를 $..$ 로 감싼다"""
    out, last = [], 0
    for m in _MATH.finditer(s):
        out.append(_LONE.sub(r"$\1$", s[last:m.start()]))
        out.append(m.group(0))
        last = m.end()
    out.append(_LONE.sub(r"$\1$", s[last:]))
    return "".join(out)


def _fixnums(o, key=""):
    if isinstance(o, str):
        return o if key in ("svg", "tex", "sym") else _wrapnum(o)
    if isinstance(o, list):
        return [_fixnums(x, key) for x in o]
    if isinstance(o, dict):
        return {k: _fixnums(v, k) for k, v in o.items()}
    return o


def build(path, deck, lo, hi, slides):
    slides = [_fixnums(s) for s in slides]
    gl_keys = []
    for s in slides:
        body = " ".join(_text([s.get(f"pass{i}", []) for i in range(1, 5)]))
        terms = []
        for key in TERMS:
            if disp(key) in body:
                terms.append(TERMS[key][1])
                if key not in gl_keys:
                    gl_keys.append(key)
        s["terms"] = terms
    out = {"deck": deck, "from": lo, "to": hi,
           "glossary": [gloss_entry(k) for k in gl_keys],
           "slides": [{"p": s["p"], "title": s["title"], "terms": s["terms"],
                       **{f"pass{i}": s.get(f"pass{i}", []) for i in range(1, 5)}} for s in slides]}
    raw = json.dumps(out, ensure_ascii=False, indent=1)
    for ch in BAD:
        if ch in raw:
            i = raw.index(ch)
            raise ValueError(f"금지 문자 {ch!r}: {raw[max(0, i - 40):i + 10]}")
    for s in out["slides"]:
        for i in range(1, 5):
            for f in s[f"pass{i}"]:
                if f["kind"] in ("say", "prof", "bg"):
                    for ln in f["lines"]:
                        if len(re.sub(r"\*\*|\$[^$]*\$", "", ln)) > 80:
                            print(f"  긴 줄 p.{s['p']} pass{i}: {ln[:40]}...")
    with open(path, "w", encoding="utf-8") as fp:
        fp.write(raw)
    print(f"저장 {path}: 쪽 {len(slides)}, 용어 {len(gl_keys)}")
    return out

OUT = os.path.join(HERE, "S2_061-088.json")

# =====================================================================
# 손계산 확인 (모든 숫자 답은 여기서 계산하고 assert)
# =====================================================================
# p.62 이산 1차 시스템 (1+ak)y[n] - y[n-1] = k u[n-1], a = k = 1
def dt_first(a, k, N):
    y = [0.0]
    for n in range(1, N):
        y.append((y[-1] + k * (1 if n - 1 >= 0 else 0)) / (1 + a * k))
    return y
Y62 = dt_first(1, 1, 8)
assert Y62[:5] == [0.0, 0.5, 0.75, 0.875, 0.9375]
assert abs(dt_first(1, 1, 60)[-1] - 1) < 1e-9          # 끝값 1/a = 1
assert abs(dt_first(2, 1, 80)[-1] - 0.5) < 1e-9        # a = 2 이면 끝값 1/2
# p.63 직렬, 병렬, 되먹임
assert 2 * 3 == 6 and 2 + 3 == 5
fb = []
prev = 0.0
for n in range(4):
    x = 1.0 if n == 0 else 0.0
    prev = x + 0.5 * prev
    fb.append(prev)
assert fb == [1.0, 0.5, 0.25, 0.125]
# p.64 무기억 식, 누산기, 지연
f64 = lambda x: (2 * x - x * x) ** 2
assert f64(3) == 9 and f64(1) == 1 and f64(2) == 0
X = [1, 2, 3]
ACC = [sum(X[:i + 1]) for i in range(3)]
assert ACC == [1, 3, 6]
# p.65 y[n] = y[n-1] + 2x[n-1] + x[n], x = 임펄스
y65, yp, xp = [], 0, 0
for n in range(4):
    x = 1 if n == 0 else 0
    yp = yp + 2 * xp + x
    xp = x
    y65.append(yp)
assert y65 == [1, 3, 3, 3]
# p.67 2배와 0.5배, 제곱
assert 2 * 3 == 6 and 0.5 * 6 == 3 and (-2) ** 2 == 2 ** 2 == 4
# p.68 누산기의 역시스템은 1차 차분
W68 = [ACC[0]] + [ACC[i] - ACC[i - 1] for i in range(1, 3)]
assert W68 == [1, 2, 3]
# p.70 중심 이동 평균 M = 1
X70 = [3, 6, 9, 12]
assert (X70[0] + X70[1] + X70[2]) / 3 == 6 and (X70[1] + X70[2] + X70[3]) / 3 == 9
assert 2 * 1 + 1 == 3 and 2 * 3 + 1 == 7        # 2M+1 칸 수
# p.72 통장 y[n] = x[n] + 1.01 y[n-1]
bank = []
prev = 0.0
for n in range(3):
    prev = 1 + 1.01 * prev
    bank.append(round(prev, 4))
assert bank == [1.0, 2.01, 3.0301]
assert round(1.01 ** 100, 3) == 2.705 and round(1.01 ** 500) == 145 and round(1.01 ** 1000) == 20959
# p.73 누산기에 단위 계단: y[n] = n+1, e^x 의 범위, ln 이 내려가는 모습
assert sum(1 for k in range(0, 100)) == 100
assert round(math.exp(-2), 3) == 0.135 and round(math.exp(2), 3) == 7.389
assert round(math.log(0.001), 1) == -6.9 and round(math.log(1e-6), 1) == -13.8
assert abs(math.cos(123.4)) <= 1
# p.75 y[n] = n x[n]
delta = lambda n: 1 if n == 0 else 0
for n in range(-3, 4):
    assert n * delta(n) == 0                         # 임펄스 넣으면 출력 0
    assert n * delta(n - 1) == delta(n - 1)          # 한 칸 민 임펄스 넣으면 출력 delta[n-1]
# p.76 y(t) = x(2t)
x76 = lambda t: 1 if -2 <= t <= 2 else 0
y2_76 = lambda t: x76(2 * t - 2)                     # x1(t-2) 를 넣은 출력
y1s_76 = lambda t: x76(2 * (t - 2))                  # y1(t-2)
assert [t for t in [i / 4 for i in range(-8, 20)] if y2_76(t)] == [i / 4 for i in range(0, 9)]
assert [t for t in [i / 4 for i in range(-8, 20)] if y1s_76(t)] == [i / 4 for i in range(4, 13)]
# p.79 y=3x, 3x^2, 3x+2 에 x1=1, x2=2
for f, ok in ((lambda x: 3 * x, True), (lambda x: 3 * x * x, False), (lambda x: 3 * x + 2, False)):
    assert (f(1 + 2) == f(1) + f(2)) == ok
assert 3 * 3 == 9 and 3 * 9 == 27 and 3 + 12 == 15 and 3 * 3 + 2 == 11 and 5 + 8 == 13
assert 3 * 0 + 2 == 2
# p.82 y = t x(t): 가산 + 척도(a=2, b=3, t=4 에서 x1=1, x2=2)
assert 4 * (2 * 1 + 3 * 2) == 2 * 4 * 1 + 3 * 4 * 2 == 32
u = lambda t: 1 if t >= 0 else 0
assert 2 * u(2 - 1) == 2 and (2 - 1) * u(2 - 1) == 1   # 시불변 아님
# p.83 y = x^2
assert (1 + 2) ** 2 == 9 and 1 ** 2 + 2 ** 2 == 5 and 2 * 1 * 2 == 4
assert (2 * 3) ** 2 == 36 and 2 * 3 ** 2 == 18
# p.84 Re{x}
x1 = 3 + 4j
assert (1j * x1) == -4 + 3j and (1j * x1).real == -4 and 1j * x1.real == 3j
assert (x1 + (1 - 2j)).real == x1.real + (1 - 2j).real == 4
# p.85 y = 2x + 3
assert 2 * 1 + 3 == 5 and 2 * 4 + 3 == 11 and 11 - 5 == 2 * (4 - 1) == 6

# ---------- p.86 과제 1.21 (연속) ----------
def x21(t):
    if -2 < t < -1: return t + 1
    if -1 < t < 0: return 1
    if 0 < t < 1: return 2
    if 1 < t < 2: return 2 - t
    return 0
def near(a, b): return abs(a - b) < 1e-9
for t in [-0.5, 0.25, 0.5, 1.5, 2.5, 2.75]:          # (a) x(t-1)
    want = t if -1 < t < 0 else 1 if 0 < t < 1 else 2 if 1 < t < 2 else 3 - t if 2 < t < 3 else 0
    assert near(x21(t - 1), want)
for t in [0.25, 0.5, 1.5, 2.5, 3.25, 3.75]:          # (b) x(2-t)
    want = t if 0 < t < 1 else 2 if 1 < t < 2 else 1 if 2 < t < 3 else 3 - t if 3 < t < 4 else 0
    assert near(x21(2 - t), want)
for t in [-1.4, -1.2, -0.75, -0.25, 0.1, 0.4]:        # (c) x(2t+1)
    want = 2 * t + 2 if -1.5 < t < -1 else 1 if -1 < t < -0.5 else 2 if -0.5 < t < 0 else 1 - 2 * t if 0 < t < 0.5 else 0
    assert near(x21(2 * t + 1), want)
for t in [4.5, 5.5, 7, 9, 10.5, 11.5]:                # (d) x(4 - t/2)
    want = t / 2 - 2 if 4 < t < 6 else 2 if 6 < t < 8 else 1 if 8 < t < 10 else 5 - t / 2 if 10 < t < 12 else 0
    assert near(x21(4 - t / 2), want)
for t in [0.5, 1.25, 1.75, 2.5, -0.5]:                # (e) [x(t)+x(-t)]u(t)
    want = 3 if 0 < t < 1 else 3 - 2 * t if 1 < t < 2 else 0
    assert near((x21(t) + x21(-t)) * (1 if t > 0 else 0), want)
assert near(x21(-1.5), -0.5) and near(x21(1.5), 0.5)  # (f) 두 임펄스 크기 -1/2, -1/2
# ---------- p.86 과제 1.22 (이산) ----------
XN = {-4: -1, -3: -0.5, -2: 0.5, -1: 1, 0: 1, 1: 1, 2: 1, 3: 0.5}
xn = lambda n: XN.get(n, 0)
R22 = range(-12, 13)
nz = lambda g: {n: g(n) for n in R22 if g(n) != 0}
assert nz(lambda n: xn(n - 4)) == {0: -1, 1: -0.5, 2: 0.5, 3: 1, 4: 1, 5: 1, 6: 1, 7: 0.5}
assert nz(lambda n: xn(3 - n)) == {0: 0.5, 1: 1, 2: 1, 3: 1, 4: 1, 5: 0.5, 6: -0.5, 7: -1}
assert nz(lambda n: xn(3 * n)) == {-1: -0.5, 0: 1, 1: 0.5}
assert nz(lambda n: xn(3 * n + 1)) == {-1: 0.5, 0: 1}
assert nz(lambda n: xn(n) * (1 if 3 - n >= 0 else 0)) == nz(xn)
assert nz(lambda n: xn(n - 2) * (1 if n == 2 else 0)) == {2: 1}
assert nz(lambda n: 0.5 * xn(n) + 0.5 * (-1) ** n * xn(n)) == {-4: -1, -2: 0.5, 0: 1, 2: 1}
assert nz(lambda n: xn((n - 1) ** 2)) == {0: 1, 1: 1, 2: 1}
# ---------- p.87 과제 1.25 주기 ----------
def is_period(f, T, pts=40):
    return all(abs(f(t + T) - f(t)) < 1e-9 for t in [0.137 * i for i in range(pts)])
fa = lambda t: 3 * math.cos(4 * t + math.pi / 3)
fb_ = lambda t: cmath.exp(1j * (math.pi * t - 1))
fc = lambda t: math.cos(2 * t - math.pi / 3) ** 2
assert is_period(fa, math.pi / 2) and not is_period(fa, math.pi / 4)
assert is_period(fb_, 2) and not is_period(fb_, 1)
assert is_period(fc, math.pi / 2) and not is_period(fc, math.pi / 4)
assert all(abs(fc(t) - (1 + math.cos(4 * t - 2 * math.pi / 3)) / 2) < 1e-12 for t in [0.1 * i for i in range(30)])
assert round(2 * math.pi / 4, 4) == round(math.pi / 2, 4) == 1.5708 and 2 * math.pi / math.pi == 2
# ---------- p.88 과제 1.31 ----------
tri = lambda t: 2 * t if 0 <= t <= 1 else 2 * (2 - t) if 1 < t <= 2 else 0   # y1(t)
x1r = lambda t: 1 if 0 <= t < 2 else 0
x2r = lambda t: 1 if 0 <= t < 2 else -1 if 2 <= t < 4 else 0
x3r = lambda t: 1 if -1 <= t < 0 else 2 if 0 <= t < 1 else 1 if 1 <= t < 2 else 0
for t in [i / 8 for i in range(-16, 40)]:
    assert x2r(t) == x1r(t) - x1r(t - 2)
    assert x3r(t) == x1r(t) + x1r(t + 1)
y2 = lambda t: tri(t) - tri(t - 2)
y3 = lambda t: tri(t) + tri(t + 1)
assert y2(1) == 2 and y2(3) == -2 and y2(2) == 0 and y2(4) == 0
assert y3(-1) == 0 and y3(0) == 2 and y3(0.5) == 2 and y3(1) == 2 and y3(2) == 0 and y3(-0.5) == 1 and y3(1.5) == 1

# =====================================================================
# 그림
# =====================================================================
def fig_dtstep():
    top = Plot((-0.5, 8.5), (0, 1.2), (60, 440), (112, 30))
    bot = Plot((-0.5, 8.5), (0, 1.2), (60, 440), (245, 155))
    p = [TX(20, 22, "입력: 스위치를 켠 모양", "tb", 15, "start"), top.axes("n")]
    for n in range(9):
        p.append(top.stem(n, 1 if n >= 1 else 0, "n3") if n >= 1 else C(top.X(n), top.Y(0), 4, "n3"))
    p.append(top.ytick(1, "1"))
    p.append(TX(20, 150, "출력: 천천히 따라가요", "tb", 15, "start", 1))
    p.append(bot.axes("n", 1))
    for n in range(9):
        v = Y62[n] if n < len(Y62) else dt_first(1, 1, 9)[n]
        p.append(bot.stem(n, v, "n2", 1) if v else C(bot.X(n), bot.Y(0), 4, "n2", 1))
    p.append(bot.ytick(1, "1", 1))
    for n in (0, 1, 2, 4, 8):
        p.append(bot.xtick(n, str(n), 1, 20))
    p.append(L(bot.X(-0.3), bot.Y(1), bot.X(8.4), bot.Y(1), "hl", 2))
    p.append(TX(300, 146, "끝값 1에 가까워져요", "tm", 14, "start", 2))
    return SVG(*p)


def fig_conn():
    p = [TX(20, 24, "직렬", "tb", 16, "start"),
         TX(40, 72, "x", "t", 16), A(52, 67, 92, 67, "e2"), BOX(94, 47, 70, 40, "×2", "box", "tb", 0, 16),
         A(164, 67, 204, 67, "e2"), BOX(206, 47, 70, 40, "×3", "box", "tb", 0, 16),
         A(276, 67, 316, 67, "e2"), TX(322, 73, "6x", "tb", 16, "start"),
         TX(390, 73, "곱해져요", "tm", 14, "start"),
         TX(20, 128, "병렬", "tb", 16, "start", 1),
         TX(40, 196, "x", "t", 16, "middle", 1), L(52, 191, 80, 191, "e2", 1),
         L(80, 160, 80, 222, "e2", 1), A(80, 160, 118, 160, "e2", 1), A(80, 222, 118, 222, "e2", 1),
         BOX(120, 140, 70, 40, "×2", "box", "tb", 1, 16), BOX(120, 202, 70, 40, "×3", "box", "tb", 1, 16),
         A(190, 160, 238, 186, "e2", 1), A(190, 222, 238, 196, "e2", 1),
         C(252, 191, 14, "n", 1), TX(252, 197, "+", "tl", 18, "middle", 1),
         A(266, 191, 306, 191, "e2", 1), TX(312, 197, "5x", "tb", 16, "start", 1),
         TX(360, 197, "더해져요", "tm", 14, "start", 1)]
    return SVG(*p)


def fig_feedback():
    p = [TX(30, 86, "x[n]", "t", 16), A(52, 80, 104, 80, "e2"),
         C(120, 80, 15, "n"), TX(120, 86, "+", "tl", 18),
         A(135, 80, 330, 80, "e2"), TX(360, 86, "y[n]", "tb", 16),
         L(260, 80, 260, 190, "e2", 1), A(260, 190, 226, 190, "e2", 1),
         BOX(120, 168, 104, 44, "×0.5, 한 칸 늦게", "box2", "tb", 1, 14),
         A(120, 168, 120, 97, "e2", 1),
         TX(240, 248, "출력이 한 칸 늦게 다시 입력 쪽으로 돌아와요", "tm", 14, "middle", 1)]
    return SVG(*p)


def fig_memory():
    xs = [70, 150, 230, 310, 390]
    labs = ["n-3", "n-2", "n-1", "n", "n+1"]
    p = [L(40, 120, 440, 120, "e")]
    for x, lab in zip(xs, labs):
        p.append(C(x, 120, 16, "n"))
        p.append(TX(x, 158, lab, "tm", 14))
    p += [TX(240, 34, "출력 y[n] 을 만들 때 어느 칸을 보나요?", "tb", 15),
          C(310, 120, 16, "n2", 1), TX(310, 82, "지금 칸만", "tb", 15, "middle", 1),
          TX(240, 205, "지금 칸만 보면 무기억", "t", 15, "middle", 1),
          R(52, 98, 276, 44, "hl", 2), C(70, 120, 16, "n3", 2), C(150, 120, 16, "n3", 2), C(230, 120, 16, "n3", 2),
          TX(240, 240, "지난 칸도 보면 기억이 있어요(누산기, 지연)", "t", 15, "middle", 2)]
    return SVG(*p)


def fig_inverse():
    p = [TX(36, 106, "x = 3", "tb", 16), A(66, 100, 100, 100, "e2"),
         BOX(102, 76, 90, 48, "×2", "box", "tb", 0, 17), A(192, 100, 236, 100, "e2"),
         TX(262, 106, "y = 6", "tb", 16), A(290, 100, 316, 100, "e2", 1),
         BOX(318, 76, 90, 48, "×0.5", "box2", "tb", 1, 17), A(408, 100, 440, 100, "e2", 1),
         TX(456, 106, "3", "tb", 17, "middle", 1),
         TX(147, 150, "시스템 T", "tm", 14), TX(363, 150, "역시스템", "tm", 14, "middle", 1),
         TX(240, 214, "처음 넣은 값 3이 그대로 돌아와요", "t", 16, "middle", 2)]
    return SVG(*p)


def fig_square():
    pl = Plot((-2.6, 2.6), (0, 6.2), (90, 390), (240, 30))
    p = [pl.axes("x"), pl.curve(lambda x: x * x, -2.45, 2.45, 60, "e2"),
         L(pl.X(-2), pl.Y(4), pl.X(2), pl.Y(4), "e", 1),
         L(pl.X(-2), pl.Y(0), pl.X(-2), pl.Y(4), "e", 1), L(pl.X(2), pl.Y(0), pl.X(2), pl.Y(4), "e", 1),
         C(pl.X(-2), pl.Y(4), 6, "n4", 1), C(pl.X(2), pl.Y(4), 6, "n4", 1),
         pl.xtick(-2, "-2", 1), pl.xtick(2, "2", 1),
         TX(pl.X(0) + 8, pl.Y(4) - 10, "출력 4", "tb", 15, "start", 1),
         TX(240, 22, "y = x 제곱", "tb", 15, "middle"),
         TX(420, 150, "4만 보고는", "tm", 14, "middle", 2), TX(420, 170, "2인지 -2인지", "tm", 14, "middle", 2),
         TX(420, 190, "몰라요", "tm", 14, "middle", 2)]
    return SVG(*p)


def fig_causal():
    p = [A(30, 130, 455, 130, "e"), TX(455, 156, "시간", "tm", 14, "end"),
         C(240, 130, 9, "n2"), TX(240, 104, "지금", "tb", 15),
         TX(120, 170, "과거", "tm", 15), TX(360, 170, "미래", "tm", 15),
         R(40, 116, 190, 28, "hl", 1), TX(135, 212, "과거와 지금만 보면 인과", "t", 15, "middle", 1),
         C(330, 130, 9, "n4", 2), A(250, 60, 322, 118, "e2", 2), TX(250, 50, "w(t)=x(t+3): 3초 뒤를 봐야 해요", "tb", 15, "middle", 2),
         TX(360, 245, "미래를 보면 비인과", "t", 15, "middle", 2)]
    return SVG(*p)


def fig_ma():
    pl = Plot((-0.5, 8.5), (0, 13), (40, 440), (200, 40))
    xv = [3, 6, 9, 12, 7, 5, 8, 10, 6]
    p = [pl.axes("n")]
    for n, v in enumerate(xv):
        p.append(pl.stem(n, v, "n"))
    p += [R(pl.X(2.5), 30, pl.X(5.5) - pl.X(2.5), 176, "hl", 1),
          TX(pl.X(4), 226, "n", "tb", 15, "middle", 1),
          TX(pl.X(3), 226, "n-1", "tm", 14, "middle", 1), TX(pl.X(5), 226, "n+1", "tm", 14, "middle", 1),
          TX(240, 258, "창문 3칸의 평균: 오른쪽 n+1 은 미래 칸이에요", "t", 15, "middle", 2),
          C(pl.X(5), pl.Y(5), 7, "n4", 2)]
    return SVG(*p)


def fig_bowl():
    arc = lambda cx, cy, r, a0, a1, up: [(cx + r * math.cos(math.radians(a)), cy + (r * math.sin(math.radians(a)) if not up else -r * math.sin(math.radians(a)))) for a in range(a0, a1 + 1, 5)]
    p = [TX(120, 30, "안정", "tb", 16), PL(arc(120, 90, 80, 0, 180, False), "e"),
         C(120, 160, 10, "n2"), TX(120, 210, "톡 쳐도 바닥으로 돌아와요", "t", 14),
         TX(360, 30, "불안정", "tb", 16, "middle", 1), PL(arc(360, 180, 80, 0, 180, True), "e", 1),
         C(360, 90, 10, "n4", 1), A(372, 96, 440, 170, "e2", 2), TX(360, 222, "톡 치면 굴러떨어져요", "t", 14, "middle", 1),
         TX(240, 258, "입력(톡)이 작아도 출력이 끝없이 커지면 불안정", "tm", 14, "middle", 2)]
    return SVG(*p)


def fig_acc_unstable():
    top = Plot((-0.5, 9.5), (0, 1.3), (60, 440), (95, 40))
    bot = Plot((-0.5, 9.5), (0, 10.5), (60, 440), (245, 130))
    p = [TX(20, 26, "입력: 단위 계단(늘 1, 유계)", "tb", 15, "start"), top.axes("n")]
    for n in range(10):
        p.append(top.stem(n, 1, "n3"))
    p.append(TX(20, 124, "누산기 출력: 1, 2, 3, ... 끝없이", "tb", 15, "start", 1))
    p.append(bot.axes("n", 1))
    for n in range(10):
        p.append(bot.stem(n, n + 1, "n4", 1))
    return SVG(*p)


def _ring(t, t0):
    if t < t0: return 0.0
    s = t - t0
    return math.exp(-0.9 * s) * math.sin(3.2 * s)


def fig_ti():
    top = Plot((0, 10), (-0.8, 1.2), (40, 440), (110, 30))
    bot = Plot((0, 10), (-0.8, 1.2), (40, 440), (240, 160))
    p = [top.axes("t"), top.poly([(0, 0), (1, 0), (1, 1), (1.3, 1), (1.3, 0), (10, 0)], "e"),
         top.curve(lambda t: _ring(t, 1.3), 0, 10, 120, "e2"), TX(470, 40, "월요일", "tb", 15, "end"),
         bot.axes("t", 1), bot.poly([(0, 0), (5, 0), (5, 1), (5.3, 1), (5.3, 0), (10, 0)], "e", 1),
         bot.curve(lambda t: _ring(t, 5.3), 0, 10, 120, "e2", 1), TX(470, 170, "금요일", "tb", 15, "end", 1),
         TX(240, 144, "입력을 늦게 넣으면 출력도 똑같은 모양으로 늦게", "tm", 14, "middle", 1)]
    return SVG(*p)


def fig_x2t():
    pl = Plot((-0.5, 4.8), (0, 1.6), (40, 440), (220, 70))
    p = [pl.axes("t")]
    for v in range(0, 5):
        p.append(pl.xtick(v, str(v)))
    p += [pl.poly([(0, 0), (0, 1), (2, 1), (2, 0)], "e2", 1),
          TX(pl.X(0.5), pl.Y(0.45), "y2", "tb", 15, "middle", 1),
          TX(20, 26, "실선: 입력을 먼저 민 출력 y2", "tb", 14, "start", 1),
          pl.poly([(1, 0), (1, 1.3), (3, 1.3), (3, 0)], "hl", 2),
          TX(pl.X(3.15), pl.Y(0.6), "y1(t-2)", "tb", 15, "start", 2),
          TX(20, 48, "점선: 출력을 민 y1(t-2)", "tb", 14, "start", 2),
          TX(240, 262, "구간 [0, 2] 와 [1, 3]: 다르니까 시불변이 아니에요", "t", 14, "middle", 3)]
    return SVG(*p)


def fig_lin():
    pl = Plot((-1.6, 1.6), (-5, 8), (70, 410), (250, 20))
    p = [pl.axes("x"), pl.curve(lambda x: 3 * x, -1.6, 1.6, 2, "e2"),
         TX(pl.X(1.45), pl.Y(4.35) + 22, "3x", "tb", 15, "start"),
         pl.curve(lambda x: 3 * x + 2, -1.6, 1.6, 2, "e", 1), TX(pl.X(1.05), pl.Y(5.15) - 8, "3x+2", "tb", 15, "end", 1),
         C(pl.X(0), pl.Y(2), 6, "n4", 1), TX(pl.X(0) - 10, pl.Y(2) - 14, "0 넣어도 2", "tm", 14, "end", 1),
         pl.curve(lambda x: 3 * x * x, -1.6, 1.6, 60, "hl", 2), TX(pl.X(-1.55), pl.Y(7.2), "3x 제곱", "tb", 15, "start", 2),
         C(pl.X(0), pl.Y(0), 5, "n2")]
    return SVG(*p)


def fig_sup():
    def pulse(pl, t0):
        return pl.poly([(0, 0), (t0, 0), (t0, 1), (t0 + 0.3, 1), (t0 + 0.3, 0), (6, 0)], "e")
    rows = []
    for i, (ts, lab, b) in enumerate((([1], "x1", 0), ([3.5], "x2", 1), ([1, 3.5], "x1+x2", 2))):
        yb = 70 + i * 80
        pin = Plot((0, 6), (-0.8, 1.2), (60, 200), (yb, yb - 50))
        pout = Plot((0, 6), (-0.8, 1.2), (290, 450), (yb, yb - 50))
        pts = [(0, 0)]
        for t0 in ts:
            pts += [(t0, 0), (t0, 1), (t0 + 0.3, 1), (t0 + 0.3, 0)]
        pts.append((6, 0))
        rows.append(pin.poly(pts, "e", b))
        rows.append(pout.curve(lambda t: sum(_ring(t, t0 + 0.3) for t0 in ts), 0, 6, 120, "e2", b))
        rows.append(TX(24, yb - 14, lab, "tb", 14, "middle", b))
        rows.append(A(215, yb - 20, 275, yb - 20, "e", b))
    rows.append(TX(245, 262, "합을 넣으면 출력도 두 메아리의 합", "t", 15, "middle", 2))
    return SVG(*rows)


def fig_hw21():
    pl = Plot((-3, 4), (-1.4, 2.4), (40, 450), (220, 30))
    p = [pl.axes("t")]
    for v in (-2, -1, 1, 2, 3):
        p.append(pl.xtick(v, str(v), 0, 80))
    p += [pl.ytick(2, "2"), pl.ytick(-1, "-1"),
          pl.poly([(-3, 0), (-2, 0), (-2, -1), (-1, 0), (-1, 1), (0, 1), (0, 2), (1, 2), (1, 1), (2, 0), (3.8, 0)], "e"),
          TX(80, 262, "x(t): 원래 모양", "tm", 14, "start"),
          pl.poly([(-3, 0), (-1, 0), (-1, -1), (0, 0), (0, 1), (1, 1), (1, 2), (2, 2), (2, 1), (3, 0), (3.8, 0)], "e2", 1),
          TX(460, 262, "x(t-1): 오른쪽으로 1칸", "tb", 14, "end", 1)]
    return SVG(*p)


def fig_hw22():
    top = Plot((-5.5, 8.5), (-1.2, 1.2), (40, 450), (95, 15))
    bot = Plot((-5.5, 8.5), (-1.2, 1.2), (40, 450), (230, 150))
    p = [top.axes("n"), TX(460, 44, "x[n]", "tb", 15, "end")]
    for n in range(-5, 9):
        v = xn(n)
        p.append(top.stem(n, v, "n") if v else C(top.X(n), top.Y(0), 3, "n"))
    for n in (-4, 0, 3):
        p.append(top.xtick(n, str(n), 0, 56))
    p += [bot.axes("n", 1), TX(40, 168, "x[3-n]", "tb", 15, "start", 1)]
    for n in range(-5, 9):
        v = xn(3 - n)
        p.append(bot.stem(n, v, "n2", 1) if v else C(bot.X(n), bot.Y(0), 3, "n2", 1))
    for n in (0, 5, 7):
        p.append(bot.xtick(n, str(n), 1, 56))
    return SVG(*p, h=270)


def fig_hw31():
    top = Plot((-1.5, 4.5), (-2.4, 2.4), (50, 450), (125, 15))
    bot = Plot((-1.5, 4.5), (0, 2.4), (50, 450), (240, 160))
    p = [top.axes("t"), top.poly([(-1.5, 0), (0, 0), (1, 2), (2, 0), (3, -2), (4, 0), (4.5, 0)], "e2"),
         TX(470, 30, "y2 = y1(t) - y1(t-2)", "tb", 14, "end")]
    for v, dy in ((1, 18), (3, -8), (4, 18)):
        p.append(top.xtick(v, str(v), 0, dy))
    p += [bot.axes("t", 1), bot.poly([(-1.5, 0), (-1, 0), (0, 2), (1, 2), (2, 0), (4.5, 0)], "e2", 1),
          TX(470, 150, "y3 = y1(t) + y1(t+1)", "tb", 14, "end", 1)]
    for v in (-1, 0, 1, 2):
        p.append(bot.xtick(v, str(v), 1, 20))
    p.append(bot.ytick(2, "2", 1))
    return SVG(*p)


FIG = {k: f() for k, f in (("dtstep", fig_dtstep), ("conn", fig_conn), ("fb", fig_feedback), ("mem", fig_memory),
                           ("inv", fig_inverse), ("sq", fig_square), ("caus", fig_causal), ("ma", fig_ma),
                           ("bowl", fig_bowl), ("accu", fig_acc_unstable), ("ti", fig_ti), ("x2t", fig_x2t),
                           ("lin", fig_lin), ("sup", fig_sup), ("hw21", fig_hw21), ("hw22", fig_hw22),
                           ("hw31", fig_hw31))}

if __name__ == "__main__" and os.environ.get("S2_061_FIGS"):
    d = os.environ["S2_061_FIGS"]
    for k, s in FIG.items():
        open(os.path.join(d, f"{k}.svg"), "w", encoding="utf-8").write(s)
    print("그림", len(FIG))
    raise SystemExit

# =====================================================================
# 쪽 내용
# =====================================================================
S = []

# ---------------- p.61 시스템 차수 ----------------
S.append({"p": 61, "title": "시스템 차수와 2차 시스템",
 "pass1": [
  say("앞에서 시스템을 식으로 적는 법을 봤어요. 이번 쪽은 그 식의 '등급' 이야기예요.",
      MANTRA,
      f"상자 안의 식이 얼마나 복잡한지를 {K('order')}라고 불러요."),
  points("이 쪽의 한 가지",
      f"{K('sys','은')} **차수**와 **매개변수**(식 속 숫자 a, b, c)로 설명해요.",
      "차수가 높을수록 출력이 더 다양하게 움직일 수 있어요.",
      f"용수철에 매단 추, RLC 회로, 자동차 정속 주행 장치가 모두 2차예요. {K('rc')}는 1차예요."),
 ],
 "pass2": [
  formula("2차 시스템 식 읽기", r"a\frac{d^2y(t)}{dt^2}+b\frac{dy(t)}{dt}+c\,y(t)=x(t)",
      [(r"\frac{d^2y(t)}{dt^2}", "디 투 와이 디 티 제곱: 출력을 두 번 미분한 것, 변화의 변화"),
       (r"\frac{dy(t)}{dt}", "디 와이 디 티: 출력이 얼마나 빨리 변하는지(기울기)"),
       (r"c\,y(t)", "출력 그 자체에 숫자 c 를 곱한 것"),
       (r"x(t)", f"오른쪽은 {K('inp')}"),
       (r"a,\ b,\ c", "매개변수: 이 시스템의 성격을 정하는 숫자")],
      f"가장 많이 미분한 횟수가 2번이라서 2차 {K('ode')}, 즉 {K('order')}가 2예요."),
  compare(f"{K('order')}를 세는 법", ["종류", "무엇을 세나요", "예"],
      [f"{K('ct')}", "가장 많이 미분한 횟수", "두 번 미분이 있으면 2차"],
      [f"{K('dt')}", "가장 멀리 거슬러 간 칸(지연)", "y[n-2] 까지 있으면 2차"]),
  check(f"{K('order')}는 무엇으로 정하나요?",
      ["식에 나온 숫자 a, b, c 의 크기", "가장 높은 미분 횟수(또는 가장 깊은 지연)", "입력 신호의 크기"], 1,
      "슬라이드: order = highest derivative (or deepest delay). 숫자 a, b, c 는 매개변수예요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (85, 145, 1215, 190, f"{K('sys','은')} 차수(order)와 매개변수(parameters)로 설명한다는 문장이에요."),
      (440, 258, 955, 360, f"2차 {K('ode')}예요. 두 번 미분한 항이 가장 높아요."),
      (85, 415, 1110, 452, "차수 = 가장 높은 미분(또는 가장 깊은 지연). 움직임이 얼마나 풍부할 수 있는지 정해요."),
      (85, 462, 915, 498, "용수철-추-댐퍼, RLC 회로, 정속 주행 장치가 모두 2차라는 예시예요.")),
  steps(f"{K('order')} 세기 연습",
      [r"$\frac{dy}{dt}+2y=x$: 가장 높은 미분이 1번이에요. 그래서 1차.",
       r"$3\frac{d^2y}{dt^2}+\frac{dy}{dt}+y=x$: 두 번 미분이 있어요. 그래서 2차.",
       r"$y[n]-0.5y[n-1]=x[n]$: 한 칸 전 $y[n-1]$ 까지 가요. 그래서 1차.",
       r"$y[n]+y[n-1]+y[n-2]=x[n]$: 두 칸 전까지 가요. 그래서 2차."],
      f"{K('ode')}는 미분 횟수, {K('dde')}은 가장 먼 과거 칸 수를 세요."),
  prof(W2, "RC 회로, RL 회로는 1차 미분방정식이고 RLC 회로는 2차라고 했어요.",
      "웬만한 물리 시스템은 1차 미분방정식을 따른다고 했어요.",
      "2차 시스템도 나중에 굉장히 중요하게 다룰 거라고 했어요."),
  bg("기초 다지기 b-8 적분은 넓이, 미분은 기울기",
      r"미분 $\frac{dy}{dt}$ 는 그래프의 기울기, 즉 얼마나 빨리 변하는지예요.",
      "두 번 미분은 기울기가 또 얼마나 변하는지, 자동차로 치면 가속도예요."),
 ],
 "pass4": [
  check(r"$y[n]-y[n-1]+0.25y[n-2]=x[n]$ 의 차수는?", ["1차", "2차", "3차"], 1,
      r"가장 먼 과거가 $y[n-2]$ 라서 두 칸 지연, 2차예요."),
  warn("헷갈리기 쉬운 점",
      "차수는 식에 나온 숫자(a, b, c)의 크기가 아니에요. 미분 횟수 또는 지연 칸 수예요.",
      f"$y^2$ 처럼 제곱이 있다고 2차가 되는 게 아니에요. {K('order')}는 미분 횟수로 세요."),
 ]})

# ---------------- p.62 출력의 움직임은 시스템이 정한다 ----------------
S.append({"p": 62, "title": "입력은 스위치, 모양은 시스템이 만든다",
 "pass1": [
  say("스위치를 탁 켜면 입력은 바로 1이 돼요.",
      "그런데 출력은 곡선을 그리며 천천히 1에 다가가요.",
      f"이 곡선 모양은 입력이 아니라 {K('sys','이')} 만든 거예요."),
  figure("입력은 한 번에, 출력은 천천히", FIG["dtstep"],
      f"{K('step')} 입력(위)과 1차 {K('dt')} 시스템의 출력(아래)", 2),
 ],
 "pass2": [
  points("문장 풀어 읽기",
      "The dynamics of the output: 출력이 시간에 따라 움직이는 모양",
      "are determined by the dynamics of the system: 시스템의 성질이 정해요",
      "if the input signal has no dynamics: 입력에 움직임이 없다면(켠 뒤 계속 1)"),
  formula("연속시간 1차 시스템", r"\frac{dy(t)}{dt}+a\,y(t)=u(t-1)",
      [(r"\frac{dy(t)}{dt}", "출력의 기울기"), (r"a", "시스템의 성격을 정하는 숫자"),
       (r"u(t-1)", f"{K('step')}을 1만큼 늦춘 입력: $t=1$ 에 스위치를 켜요")],
      f"1차 {K('ode')}예요. 입력은 $t=1$ 부터 늘 1이에요."),
  formula("이산시간 1차 시스템", r"(1+ak)\,y[n]-y[n-1]=k\,u[n-1]",
      [(r"y[n-1]", "한 칸 전 출력(기억)"), (r"u[n-1]", f"한 칸 늦춘 {K('step')}"),
       (r"a,\ k", "시스템 숫자")],
      f"1차 {K('dde')}예요. 한 칸 전 출력을 보며 조금씩 따라가요."),
  check("그래프에서 출력이 곡선으로 천천히 오르는 이유는?",
      ["입력이 천천히 올라서", "시스템이 그렇게 반응해서", "그래프를 잘못 그려서"], 1,
      "입력은 한 번에 1이 돼요. 곡선 모양은 시스템의 성질이에요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (85, 150, 1315, 236, "입력에 움직임이 없으면 출력의 움직임은 시스템이 정한다는 문장이에요."),
      (312, 252, 590, 315, f"연속시간 1차 {K('sys')}. 입력은 $u(t-1)$ 이에요."),
      (675, 252, 1086, 315, f"이산시간 1차 {K('sys')}. 입력은 $u[n-1]$ 이에요."),
      (185, 360, 690, 687, "파랑은 입력 계단, 주황은 출력. 출력이 곡선으로 1에 다가가요."),
      (700, 360, 1214, 687, "이산시간 출력. 점들이 한 칸씩 1에 다가가요.")),
  steps("이산시간 식을 쉬운 숫자로 손계산 ($a=1$, $k=1$)",
      [r"식을 $y[n]$ 에 대해 풀면 $y[n]=\frac{y[n-1]+k\,u[n-1]}{1+ak}=\frac{y[n-1]+u[n-1]}{2}$ 예요.",
       r"$n=0$: 아직 스위치 전이라 $y[0]=0$.",
       r"$n=1$: $y[1]=\frac{0+1}{2}=0.5$",
       r"$n=2$: $y[2]=\frac{0.5+1}{2}=0.75$",
       r"$n=3$: $y[3]=\frac{0.75+1}{2}=0.875$, $n=4$ 이면 $0.9375$"],
      "0, 0.5, 0.75, 0.875, 0.9375 ... 이렇게 1에 점점 가까워져요.",
      given=r"$(1+ak)y[n]-y[n-1]=k\,u[n-1]$"),
  steps("끝값은 왜 1일까요?",
      ["오래 지나면 출력이 더 변하지 않아요. 그 값을 $y$ 라고 해요.",
       r"그러면 $y[n]=y[n-1]=y$, $u=1$ 이라서 $(1+ak)y-y=k$ 예요.",
       r"정리하면 $ak\,y=k$, 즉 $y=\frac{1}{a}$ 예요.",
       r"$a=1$ 이면 끝값 1, $a=2$ 이면 끝값 0.5예요."],
      "끝값 $1/a$ 도 시스템 숫자 a 가 정해요. 입력은 그냥 1일 뿐이에요."),
  bg("기초 다지기 b-9 단위 계단과 단위 임펄스",
      "$u(t)$ 는 $t=0$ 에서 켜져서 계속 1인 스위치 신호예요.",
      "$u(t-1)$ 은 오른쪽으로 1만큼 밀려서 $t=1$ 에 켜져요."),
 ],
 "pass4": [
  warn("헷갈리기 쉬운 점",
      "그래프의 이산시간 점은 $n=2$ 부터 올라가는 것처럼 그려져 있어요.",
      "식대로 손계산하면 $y[1]=k/(1+ak)$ 라서 $n=1$ 부터 값이 생겨요. 그림과 식이 한 칸 어긋나 보이니 식을 따르세요.",
      "시험에서는 모양(천천히 1/a 로 다가감)과 손계산 방법을 기억하면 돼요."),
  check("$a=1$, $k=1$ 일 때 $y[2]$ 는? (시작 $y[0]=0$)", ["0.5", "0.75", "1"], 1,
      "$y[1]=0.5$, $y[2]=(0.5+1)/2=0.75$ 예요."),
 ]})

# ---------------- p.63 시스템 연결 ----------------
S.append({"p": 63, "title": "시스템 연결: 직렬, 병렬, 되먹임",
 "pass1": [
  say("복잡한 시스템도 알고 보면 간단한 상자들을 이어 붙인 거예요.",
      "줄줄이 잇거나, 나란히 놓거나, 뒤로 돌려 이어요.",
      MANTRA),
  figure("상자 잇는 두 가지 기본 방법", FIG["conn"],
      f"{K('ser','은')} 차례로 거치고, {K('par','은')} 나눠 갔다가 더해요.", 1),
 ],
 "pass2": [
  compare("세 가지 연결", ["연결", "모양", "쉬운 말"],
      [f"{K('ser')}", "상자1 → 상자2", "앞 상자 출력이 뒤 상자 입력(cascade)"],
      [f"{K('par')}", "둘로 나눠 → 각자 → 더하기", "같은 입력을 두 상자가 받고 결과를 더함"],
      [f"{K('fb')}", "출력이 다시 입력 쪽으로", "내 결과가 다음 계산에 다시 들어옴"]),
  points("슬라이드 그림 네 개",
      "series (cascade): 직렬",
      "parallel: 병렬, 동그라미 + 는 더하기",
      "series-parallel: 직렬과 병렬을 섞은 것",
      "feedback: 되먹임. System 2 가 출력을 다시 앞으로 보내요"),
  check("출력이 다시 입력 쪽으로 돌아와 더해지는 연결은?",
      [f"{K('ser')}", f"{K('par')}", f"{K('fb')}"], 2,
      "출력이 되돌아오는 길이 있으면 되먹임(feedback)이에요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (150, 262, 560, 365, f"{K('ser')}. 입력이 System 1, System 2 를 차례로 지나요."),
      (175, 425, 535, 590, f"{K('par')}. 둘로 나뉘어 각자 지나고 + 에서 더해져요."),
      (640, 262, 1215, 435, "직렬과 병렬을 섞은 연결이에요. 1, 2 직렬과 3 이 병렬, 그 뒤에 4."),
      (660, 470, 1035, 658, f"{K('fb')}. System 2 가 출력을 앞으로 되돌려 보내요."),
      (85, 668, 1030, 705, f"{K('rc')} 자체도 저항과 축전기의 되먹임 연결이라는 문장이에요.")),
  steps("쉬운 숫자로 직렬과 병렬",
      ["상자1은 '2배', 상자2는 '3배' 하는 시스템이라고 해요.",
       "직렬: $x=1$ 이 상자1을 지나 2, 다시 상자2를 지나 6이 돼요. 곱해져요.",
       "병렬: $x=1$ 이 상자1에서 2, 상자2에서 3. 더하면 5예요.",
       "그래서 직렬은 $6x$, 병렬은 $5x$ 인 상자 하나와 똑같아요."],
      f"{K('ser','은')} 곱, {K('par','은')} 합으로 합쳐져요(곱하기 상자일 때)."),
  figure(f"{K('fb')} 예: $y[n]=x[n]+0.5\\,y[n-1]$", FIG["fb"],
      "출력의 절반이 한 칸 늦게 다시 더해져요.", 1),
  steps("되먹임 손계산 (입력은 $n=0$ 에 한 번 톡, 1)",
      [r"$n=0$: $y[0]=1+0.5\times 0=1$",
       r"$n=1$: 입력 0. $y[1]=0+0.5\times 1=0.5$",
       r"$n=2$: $y[2]=0.5\times 0.5=0.25$",
       r"$n=3$: $y[3]=0.125$"],
      "한 번 톡 친 입력이 되먹임 때문에 1, 0.5, 0.25, 0.125 로 계속 울려요."),
  prof(W2, "우리가 회로를 직렬 연결, 병렬 연결로 표현하듯 시스템도 그렇게 된다고 했어요.",
      "주의해서 볼 것은 피드백이라고 했어요. 이번 시간 값에 직전 시간의 값이 들어올 수 있다는 뜻이에요."),
 ],
 "pass4": [
  check("상자1 '2배', 상자2 '3배' 를 병렬로 이으면 $x=4$ 의 출력은?", ["24", "20", "7"], 1,
      r"$2\times4+3\times4=8+12=20$ 이에요. 직렬이면 24예요."),
  english("답안 문장",
      "직렬 연결은 앞 시스템의 출력이 뒤 시스템의 입력이 되고, 병렬 연결은 같은 입력을 받은 두 시스템의 출력을 더하며, 되먹임 연결은 출력이 다시 입력 쪽으로 돌아와 더해진다.",
      "직렬은 차례로, 병렬은 나눠서 더하기, 되먹임은 되돌아오기.",
      "직렬 = 줄 서기, 병렬 = 나란히, 되먹임 = 돌아오기"),
 ]})

# ---------------- p.64 기억성 ----------------
S.append({"p": 64, "title": "기억성: 무기억 시스템과 기억 있는 시스템",
 "pass1": [
  say("이제 1.6절, 시스템의 성질 여섯 가지를 봐요.",
      f"첫째는 {K('mem')}이에요. 시스템이 지난 일을 기억하느냐예요.",
      "지금 입력만 보고 답하면 기억이 없고, 지난 입력도 쓰면 기억이 있어요."),
  analogy("통장 잔고", "통장 잔고는 오늘 입금만이 아니라 지난 입금이 모두 쌓인 값이에요.",
      ["지난 입금이 쌓인 잔고", f"기억 있는 시스템({K('acc')})"],
      ["지금 넣은 돈만 보는 계산", f"{K('memless')}"]),
 ],
 "pass2": [
  compare("기억 있나, 없나", ["시스템", "출력이 보는 입력", "판정"],
      [r"$y[n]=(2x[n]-x^2[n])^2$", "지금 칸 x[n] 만", f"{K('memless')}"],
      [r"$y[n]=\sum_{k=-\infty}^{n}x[k]$", "처음부터 지금까지 전부", f"기억 있음({K('acc')})"],
      [r"$y[n]=x[n-1]$", "한 칸 전 x[n-1]", f"기억 있음({K('delay')})"]),
  formula(f"{K('acc')} 식 읽기", r"y[n]=\sum_{k=-\infty}^{n}x[k]",
      [(r"\sum", "시그마: 다 더하라는 기호"), (r"k=-\infty", "아주 먼 과거 칸부터"),
       (r"n", "지금 칸까지"), (r"x[k]", "각 칸의 입력")],
      "처음부터 지금까지 입력을 모두 더한 값이 출력이에요. 적분기(integrator), 합산기(summer)라고도 해요."),
  figure("출력이 어느 칸을 보나요?", FIG["mem"], "지금 칸만 보면 무기억, 지난 칸도 보면 기억 있음", 2),
  check(f"$y[n]=x[n-1]$ 은 {K('memless')}인가요?", ["예", "아니요"], 1,
      "한 칸 전 입력을 기억해 두었다가 내보내야 해서 기억이 있어요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (110, 150, 630, 195, "기억이 있는 시스템과 없는 시스템(Systems with and without Memory)."),
      (195, 215, 1305, 300, f"{K('memless')}의 정의: 같은 시각의 값에만 의존해요."),
      (205, 322, 500, 368, "무기억 예. 복잡해 보여도 전부 지금 칸 x[n] 뿐이에요."),
      (195, 388, 1020, 494, f"기억 있는 예: {K('acc')}. 과거 입력을 모두 더해요."),
      (195, 505, 850, 600, f"또 다른 기억 있는 예: {K('delay')} $y[n]=x[n-1]$.")),
  steps("무기억 식에 숫자 넣기: $y[n]=(2x[n]-x^2[n])^2$",
      [r"$x[n]=3$: $2\times3-3^2=6-9=-3$, 제곱하면 9.",
       "$x[n]=1$: $2-1=1$, 제곱하면 1.",
       "$x[n]=2$: $4-4=0$, 제곱하면 0.",
       "어느 경우든 지금 칸의 값 하나만 있으면 답이 나와요."],
      f"그래서 식이 복잡해도 {K('memless')}이에요."),
  steps(f"{K('acc')} 손계산 (입력 1, 2, 3 이 $n=0,1,2$ 에)",
      ["$y[0]=x[0]=1$", "$y[1]=x[0]+x[1]=1+2=3$", "$y[2]=1+2+3=6$",
       "$y[2]$ 를 구하려면 $x[0]$, $x[1]$ 을 기억하고 있어야 해요."],
      "출력 1, 3, 6. 지난 입력이 쌓이니까 기억이 있어요."),
  prof(W2, "y[n] 의 오른쪽에 x[n] 만 나오면 메모리리스, 과거가 나오면 메모리가 있는 거라고 했어요.",
      "식이 굉장히 복잡해 보여도 현재 값만으로 정해지면 메모리가 없다고 했어요."),
 ],
 "pass4": [
  warn("슬라이드 문장 주의",
      "정의 문장에 'dependent on the output at only that same time' 이라고 적혀 있어요.",
      "뜻으로는 output(출력)이 아니라 **input(입력)** 이에요. 같은 시각의 입력에만 의존하면 무기억이에요.",
      "교재도 입력으로 정의해요. 답안에는 '같은 시각의 입력' 이라고 쓰세요."),
  check(f"다음 중 {K('memless')}은?", ["$y[n]=x[n]+x[n-1]$", "$y(t)=5x(t)^3$", r"$y[n]=\sum_{k=-\infty}^{n}x[k]$"], 1,
      "$5x(t)^3$ 은 지금 시각의 x 만 써요. 나머지는 지난 입력을 써요."),
  english("답안 문장",
      "시스템의 출력이 각 시각에서 그 시각의 입력에만 의존하면 무기억 시스템이고, 다른 시각(과거)의 입력이 필요하면 기억이 있는 시스템이다.",
      "지금 입력만 → 무기억, 지난 입력도 → 기억 있음.",
      "오른쪽에 x[n] 만 있나 보기"),
 ]})

# ---------------- p.65 기억과 RNN ----------------
S.append({"p": 65, "title": "기억이 뜻하는 것, 그리고 RNN",
 "pass1": [
  say(f"{K('mem','을')} 한 번 더 봐요.",
      "기억이란 지금이 아닌 다른 시각의 입력 정보를 시스템 안에 잡아 두는 장치예요.",
      "AI 에서도 같은 생각이 나와요. 앞 내용을 기억하는 신경망이 있어요."),
  analogy("통장 잔고 다시", "이번 달 잔고는 지난달 잔고에 이번 입금을 더한 값이에요.",
      ["지난달 잔고 y[n-1]", "시스템이 기억하는 과거 출력"],
      ["이번 달 입금 x[n]", f"지금 {K('inp')}"]),
 ],
 "pass2": [
  compare("두 신경망", ["", "순환 신경망(RNN)", "순전파 신경망(Feed-Forward)"],
      ["그림", "동그라미에 자기 자신으로 돌아오는 화살표", "왼쪽에서 오른쪽으로만"],
      ["기억", "있음(앞 결과가 다시 들어옴)", "없음"],
      ["닮은 시스템", f"{K('fb')}, 기억 있는 시스템", f"{K('memless')}"]),
  formula("기억 있는 시스템 예", r"y[n]=y[n-1]+2x[n-1]+x[n]",
      [(r"y[n-1]", "한 칸 전 출력(기억)"), (r"x[n-1]", "한 칸 전 입력(기억)"), (r"x[n]", "지금 입력")],
      f"지난 출력과 지난 입력을 써서 기억이 있어요. 이런 식을 {K('dde')}이라고 해요."),
  check("RNN 그림에서 동그라미로 되돌아오는 작은 화살표는 무엇을 뜻하나요?",
      ["기억(앞 결과를 다시 씀)", "더하기", "잡음"], 0,
      "자기 자신으로 돌아오는 길이 기억 역할을 해요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (195, 215, 1300, 300, "기억이란 현재가 아닌 시각의 입력 정보를 잡아 두는 장치라는 정의예요."),
      (90, 335, 330, 670, "순환 신경망(Recurrent Neural Network). 동그라미 위 화살표가 자기에게 돌아와요."),
      (365, 400, 600, 670, "순전파 신경망(Feed-Forward). 돌아오는 길이 없어요."),
      (695, 450, 1255, 495, "기억 있는 시스템의 식이에요.")),
  steps("$y[n]=y[n-1]+2x[n-1]+x[n]$ 손계산 (입력은 $n=0$ 에만 1)",
      [r"$n=0$: $y[0]=0+2\times0+1=1$",
       r"$n=1$: $y[1]=y[0]+2x[0]+x[1]=1+2+0=3$",
       r"$n=2$: $y[2]=3+0+0=3$",
       "입력은 끝났는데 출력은 3을 계속 기억해요."],
      "출력 1, 3, 3, 3. 과거를 기억하는 시스템이에요."),
  prof(W2, "리커런트(순환) 신경망은 메모리가 필요하고 피드포워드는 필요 없다고 했어요.",
      "어려운 건 없다고, 과거 입력이 필요하냐 아니냐로 쉽게 판단한다고 했어요."),
 ],
 "pass4": [
  check(r"$y[n]=0.9\,y[n-1]+x[n]$ 은 기억이 있나요?", ["있다", "없다"], 0,
      f"지난 출력 y[n-1] 을 써서 기억이 있어요. 이 모양은 {K('fb')}이기도 해요."),
 ]})

# ---------------- p.66 가역성 ----------------
S.append({"p": 66, "title": "가역성과 역시스템",
 "pass1": [
  say(f"둘째 성질은 {K('inv')}이에요.",
      "출력만 보고 원래 입력을 되찾을 수 있으면 가역이에요.",
      f"되찾아 주는 상자를 {K('invsys')}이라고 불러요."),
  analogy("되돌리기 버튼", "글을 고친 뒤 Ctrl+Z 를 누르면 고치기 전으로 돌아가요.",
      ["글 고치기", f"{K('sys')} T"], ["Ctrl+Z", f"{K('invsys')}"], ["원래 글로 돌아옴", "z(t) = x(t)"]),
 ],
 "pass2": [
  points("정의 두 줄",
      "가역(invertible): 서로 다른 입력은 서로 다른 출력을 만든다.",
      f"가역이면, 원래 시스템 뒤에 직렬로 이어서 처음 입력을 그대로 돌려주는 {K('invsys')}이 있다.",
      "행렬의 역행렬과 비슷한 생각이라고 적혀 있어요."),
  formula("역시스템 식 읽기", r"z(t)=\mathbf{T}^{-1}y(t)=\mathbf{T}^{-1}\mathbf{T}x(t)=x(t)",
      [(r"\mathbf{T}", f"원래 {K('sys')}"), (r"\mathbf{T}^{-1}", "티 인버스: 역시스템"),
       (r"y(t)=\mathbf{T}x(t)", "원래 시스템의 출력"), (r"z(t)=x(t)", "최종 출력이 처음 입력과 같다")],
      "T 를 지나고 T 인버스를 지나면 처음 입력으로 돌아와요."),
  check(f"{K('inv')}의 조건은?", ["모든 입력이 같은 출력을 낸다", "서로 다른 입력은 서로 다른 출력을 낸다", "출력이 항상 0이다"], 1,
      "출력이 겹치지 않아야 거꾸로 따라갈 수 있어요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (180, 215, 1250, 300, "가역의 정의: 다른 입력은 다른 출력으로(distinct inputs lead to distinct outputs)."),
      (180, 318, 1250, 400, f"가역이면 {K('invsys')}이 있어서 직렬로 이으면 처음 입력이 나와요."),
      (185, 460, 470, 660, "식으로: T 인버스에 T 를 곱하면 원래 x(t)."),
      (580, 500, 1235, 630, "그림으로: x(t) → System T → y(t) → System T 인버스 → z(t)=x(t).")),
  figure("2배 상자와 역시스템", FIG["inv"], "2배 한 것을 0.5배 하면 처음 값으로 돌아와요.", 2),
  prof(W2, "역시스템이 되려면 1대1 대응이 돼야 한다고 했어요.",
      "입력과 출력이 1대1 이어야 다시 돌려서 원래 입력을 복원할 수 있다는 뜻이에요."),
 ],
 "pass4": [
  english("답안 문장",
      "서로 다른 입력이 항상 서로 다른 출력을 만들면 그 시스템은 가역이며, 원래 시스템 뒤에 직렬로 연결했을 때 처음 입력을 그대로 내놓는 역시스템이 존재한다.",
      "1대1 이면 가역, 역시스템을 직렬로 붙이면 z = x.",
      "다른 입력 → 다른 출력"),
 ]})

# ---------------- p.67 가역 예시 ----------------
S.append({"p": 67, "title": "가역인 예와 가역이 아닌 예",
 "pass1": [
  say("2배 하는 상자는 0.5배 하면 되돌릴 수 있어요.",
      "제곱하는 상자는 되돌릴 수 없어요. 부호를 잃어버리거든요.",
      f"그래서 앞은 {K('inv','이')} 있고, 뒤는 없어요."),
  figure("제곱은 부호를 지워요", FIG["sq"], "2를 넣어도, -2를 넣어도 출력은 4예요.", 2),
 ],
 "pass2": [
  compare("세 시스템", ["시스템", "되돌릴 수 있나", "이유"],
      ["$y(t)=2x(t)$", "예", r"$w(t)=0.5\,y(t)$ 로 원래 x 복원"],
      ["$y(t)=x^2(t)$", "아니요", "출력만 보고 입력의 부호를 알 수 없음"],
      ["$y[n]=0$", "아니요", "어떤 입력이든 출력이 0이라 구별 불가"]),
  points(f"{K('inv','이')} 쓰이는 곳",
      "암호화와 복호화: 잠근 것을 정확히 되풀어야 해요.",
      "시스템 제어: 원하는 기준 신호를 입력으로 삼아요."),
  check("$y(t)=x^2(t)$ 가 가역이 아닌 이유는?", ["출력이 너무 커서", "입력의 부호를 알 수 없어서", "미분이 있어서"], 1,
      "3과 -3 모두 9가 돼서 9만 보고는 둘 중 무엇인지 몰라요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (185, 215, 780, 350, "가역 예: $y(t)=2x(t)$. $w(t)=0.5y(t)$ 가 x(t) 를 되찾아요."),
      (185, 370, 1060, 560, "가역이 아닌 예: $x^2(t)$ 와 $y[n]=0$."),
      (185, 580, 750, 715, "가역성이 설계 원리로 쓰이는 곳: 암호화, 제어."),
      (835, 235, 1305, 420, "왼쪽 직선은 한 출력에 한 입력, 오른쪽 포물선은 한 출력(점선)에 입력 둘.")),
  steps("숫자로 확인",
      ["$y=2x$: $x=3$ 이면 $y=6$. 0.5배 하면 3. 되돌아와요.",
       "$y=x^2$: $x=2$ 이면 4, $x=-2$ 여도 4.",
       "출력 4만 받은 역시스템은 2와 -2 중 무엇을 내야 할지 몰라요.",
       "$y[n]=0$: 무엇을 넣어도 0이니 더 몰라요."],
      "1대1 이 깨지면 가역이 아니에요."),
  prof(W2, "y(t)=2x(t) 에 1/2 을 곱하는 시스템을 이으면 x 로 돌아오니 가역성이 있다고 했어요."),
 ],
 "pass4": [
  check("다음 중 가역인 시스템은?", ["$y(t)=x^2(t)$", "$y[n]=0$", "$y(t)=3x(t)+2$"], 2,
      "$x=(y-2)/3$ 으로 되돌릴 수 있어요. 3x+2 는 선형은 아니지만 가역이에요."),
  warn("헷갈리기 쉬운 점",
      "가역이 아닌 것을 보이려면 '같은 출력을 내는 서로 다른 두 입력' 하나만 찾으면 돼요(예: 2와 -2).",
      f"{K('inv','과')} {K('lin','은')} 다른 성질이에요. 3x+2 는 가역이지만 선형이 아니에요."),
 ]})

# ---------------- p.68 역시스템 그림 ----------------
S.append({"p": 68, "title": "역시스템 그림 세 가지 (Figure 1.45)",
 "pass1": [
  say(f"이 쪽은 {K('invsys','을')} 그림으로 다시 보여 줘요.",
      "시스템 뒤에 역시스템을 이으면 처음 신호가 그대로 나와요.",
      f"특히 {K('acc')}의 역시스템이 무엇인지가 핵심이에요."),
 ],
 "pass2": [
  compare("Figure 1.45 세 줄", ["", "시스템", "역시스템"],
      ["(a)", "일반 시스템", "일반 역시스템, $w[n]=x[n]$"],
      ["(b)", "$y(t)=2x(t)$", r"$w(t)=\frac{1}{2}y(t)$"],
      ["(c)", f"{K('acc')}", "$w[n]=y[n]-y[n-1]$"]),
  formula(f"{K('acc')}의 역시스템", r"w[n]=y[n]-y[n-1]",
      [(r"y[n]", "지금까지의 합"), (r"y[n-1]", "한 칸 전까지의 합"), (r"w[n]", "차이 = 지금 칸의 입력")],
      "지금까지 합에서 어제까지 합을 빼면 오늘 들어온 값만 남아요. 이것을 1차 차분이라고 해요."),
  check(f"{K('acc')}의 역시스템은?", ["$w[n]=y[n]+y[n-1]$", "$w[n]=y[n]-y[n-1]$", "$w[n]=2y[n]$"], 1,
      "누적 합에서 한 칸 전 누적 합을 빼면 원래 입력이에요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (230, 180, 1125, 270, f"위쪽 큰 그림: System T 뒤에 {K('invsys')} T 인버스, 끝은 z(t)=x(t)."),
      (420, 365, 785, 445, "(a) 일반적인 모양."),
      (425, 470, 780, 540, "(b) 2배와 1/2배."),
      (420, 575, 895, 650, f"(c) {K('acc','와')} 그 역시스템(1차 차분).")),
  steps("(c) 를 숫자로 확인 (입력 1, 2, 3)",
      [f"{K('acc')} 출력: $y[0]=1$, $y[1]=3$, $y[2]=6$",
       "$w[0]=y[0]-y[-1]=1-0=1$",
       "$w[1]=3-1=2$", "$w[2]=6-3=3$"],
      "w 가 1, 2, 3 으로 처음 입력과 똑같아요."),
  analogy("통장으로 보면", "잔고 기록만 있어도 이번 달 잔고에서 지난달 잔고를 빼면 이번 달 입금액을 알 수 있어요.",
      ["잔고", "누산기 출력 y[n]"], ["이번 달 - 지난달", "역시스템 w[n]"], ["이번 달 입금", "원래 입력 x[n]"]),
 ],
 "pass4": [
  exam("교재 Figure 1.45 (p.68)", "Find the inverse of the accumulator y[n] = sum_{k=-inf}^{n} x[k].",
      "누산기의 역시스템을 구하고 숫자로 확인하세요.",
      ["누산기는 $y[n]=y[n-1]+x[n]$ 과 같아요(어제까지 합 + 오늘).",
       "그래서 $x[n]=y[n]-y[n-1]$ 이에요.",
       "입력 1, 2, 3 → y 는 1, 3, 6 → 차분하면 1, 2, 3."],
      "$w[n]=y[n]-y[n-1]$ (1차 차분)"),
 ]})

# ---------------- p.69 인과성 ----------------
S.append({"p": 69, "title": "인과성: 미래를 미리 보지 않는 시스템",
 "pass1": [
  say(f"셋째 성질은 {K('caus')}이에요.",
      "지금의 출력이 지금과 과거의 입력만으로 정해지면 인과 시스템이에요.",
      "미래 입력을 미리 봐야 하면 비인과예요."),
  analogy("내일 주가를 모르는 사람", "오늘 투자를 정할 때 우리는 어제와 오늘 주가만 알고 내일 주가는 몰라요.",
      ["어제, 오늘 주가", "과거와 현재 입력"], ["내일 주가", "미래 입력"],
      ["내일을 모르고 결정하는 사람", "인과 시스템"]),
 ],
 "pass2": [
  points("정의 풀어 읽기",
      "causal(인과): 어느 시각의 출력이든 현재와 과거 값에만 의존해요.",
      "non-anticipative(미리 보지 않는): 출력이 입력의 미래 값을 미리 알지 않아요.",
      "그림의 $w(t)=x(t+3)$ 은 3초 뒤 입력이 지금 필요해서 비인과예요."),
  figure("과거, 지금, 미래", FIG["caus"], "과거와 지금만 보면 인과, 미래를 보면 비인과", 2),
  compare(f"{K('mem','과')} {K('caus')} 구별", ["성질", "묻는 것", "예"],
      [f"{K('mem')}", "지금 말고 다른 시각을 보나?", "$x[n-1]$ 을 보면 기억 있음"],
      [f"{K('caus')}", "미래를 보나?", "$x[n+1]$ 을 보면 비인과"]),
  check("$w(t)=x(t+3)$ 은 인과인가요?", ["인과", "비인과"], 1,
      "$t=0$ 의 출력에 $x(3)$, 즉 3초 뒤 입력이 필요해요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (145, 200, 1125, 275, "인과의 정의: 출력이 현재와 과거 값에만 의존해요."),
      (145, 290, 1125, 370, "미리 보지 않는(non-anticipative) 시스템이라고도 불러요."),
      (335, 385, 1150, 525, "위: 입력 x(t)."),
      (335, 530, 1150, 690, "아래: $w(t)=x(t+3)$. 빨간 글씨 '3초 뒤 미래 입력이 필요해요'.")),
  steps("$w(t)=x(t+3)$ 을 한 시각씩 확인",
      [r"$t=0$ 일 때 $w(0)=x(3)$: 3초 뒤 값이 필요해요.",
       r"$t=5$ 일 때 $w(5)=x(8)$: 역시 3초 뒤.",
       "어느 시각이든 미래를 봐야 하니 비인과예요.",
       r"반대로 $x(t-3)$ 이면 3초 전 값이라 인과예요."],
      "괄호 안이 $t$ 보다 크면 미래를 보는 거예요."),
  prof(W2, "인과성은 내 시스템이 미래는 안 보고 현재 혹은 과거에만 의존하는 것이라고 했어요.",
      "대부분의 시스템은 인과성이 있다고 했어요."),
 ],
 "pass4": [
  warn("슬라이드 문장 주의",
      "정의 문장에 'values of the output at only the present and past' 라고 적혀 있어요.",
      "뜻으로는 **입력(input)** 의 현재와 과거 값이에요. 바로 아래 문장도 '입력의 미래 값을 미리 알지 않는다' 고 해요.",
      "답안에는 '출력이 현재와 과거의 입력에만 의존' 이라고 쓰세요."),
  english("답안 문장",
      "인과 시스템은 어느 시각의 출력이 그 시각과 그 이전의 입력에만 의존하고 미래의 입력에는 의존하지 않는 시스템이다.",
      "현재 + 과거 입력만 → 인과. 미래 입력 필요 → 비인과.",
      "괄호 안 시각이 t(또는 n)보다 큰 적이 있나 보기"),
 ]})

# ---------------- p.70 누산기와 이동 평균 ----------------
S.append({"p": 70, "title": "누산기는 인과, 중심 이동 평균은 비인과",
 "pass1": [
  say(f"{K('acc')}는 처음부터 지금까지 더하니 미래를 보지 않아요. 인과예요.",
      f"{K('ma')}은 내 양옆을 같이 보고 평균 내요.",
      "오른쪽 옆은 미래 칸이라서 비인과예요."),
  figure("창문 3칸 평균", FIG["ma"], "가운데 n 을 구하려면 오른쪽 n+1(미래)도 필요해요.", 2),
 ],
 "pass2": [
  formula(f"중심 {K('ma')} 식 읽기", r"y[n]=\frac{1}{2M+1}\sum_{k=-M}^{M}x[n-k]",
      [(r"2M+1", "창문의 칸 수: 왼쪽 M칸 + 가운데 1칸 + 오른쪽 M칸"),
       (r"\sum_{k=-M}^{M}", "k 를 -M 부터 M 까지 바꾸며 더해요"),
       (r"x[n-k]", "k=-M 이면 x[n+M] (미래), k=M 이면 x[n-M] (과거)"),
       (r"\frac{1}{2M+1}", "칸 수로 나눠서 평균")],
      "내 앞뒤 M칸씩, 모두 2M+1 칸의 평균이에요."),
  compare("두 시스템", ["시스템", "보는 칸", "인과?"],
      [f"{K('acc')}", "처음부터 지금 n 까지", "인과"],
      [f"중심 {K('ma')}", "n-M 부터 n+M 까지", "비인과(x[n+1] ... x[n+M] 필요)"]),
  check("$M=1$ 인 중심 이동 평균은 몇 칸의 평균인가요?", ["2칸", "3칸", "4칸"], 1,
      "$2M+1=3$, 즉 n-1, n, n+1 세 칸이에요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (85, 150, 960, 192, f"{K('acc')}: 인과(과거와 현재만)."),
      (85, 198, 1050, 245, f"중심 {K('ma')}: 비인과(x[n+1] 부터 x[n+M] 까지 필요)."),
      (145, 280, 760, 360, "왼쪽은 누산기 식, 오른쪽은 이동 평균 식."),
      (975, 325, 1345, 440, "왼쪽 화살표는 과거(Past), 가운데 x[n] 이 현재(Present), 오른쪽이 미래(Future)."),
      (85, 405, 985, 690, "파랑은 들쭉날쭉한 원래 데이터, 주황은 M=3 이동 평균. 부드러워졌어요.")),
  steps("$M=1$ 중심 이동 평균 손계산 (입력 3, 6, 9, 12 가 $n=0,1,2,3$)",
      [r"$y[1]=\frac{x[0]+x[1]+x[2]}{3}=\frac{3+6+9}{3}=6$",
       r"$y[2]=\frac{6+9+12}{3}=9$",
       r"$y[1]$ 을 구하는 순간 $x[2]$ 가 필요해요. $n=1$ 에서 보면 미래 값이에요.",
       "실시간으로는 못 하고, 이미 다 녹화된 데이터에서는 할 수 있어요."],
      "평균은 부드럽게 만들지만 미래 칸이 필요해서 비인과예요."),
  steps("슬라이드 그래프의 M=3",
      [r"$2M+1=2\times3+1=7$ 칸의 평균이에요.",
       "내 앞 3칸, 나, 내 뒤 3칸을 더해 7로 나눠요.",
       "칸이 많을수록 더 부드러워지고, 미래도 3칸이나 봐요."],
      "M=3 이면 창문 7칸이에요."),
  prof(W2, "이미 찍힌 영상을 부드럽게 만들 때는 내가 보는 점 양쪽 점을 보고 처리할 수 있다고 했어요.",
      "무빙 에버리지처럼 양옆 윈도우를 보고 미래 n+1 값까지 끌어오면 넌코절(비인과)이라고 했어요."),
 ],
 "pass4": [
  check(r"$y[n]=\frac{1}{3}(x[n]+x[n-1]+x[n-2])$ 는 인과인가요?", ["인과", "비인과"], 0,
      "지금과 과거 두 칸만 봐요. 창문을 과거 쪽에만 두면 인과 이동 평균이 돼요."),
  exam("슬라이드 예제 정리 (p.70)", "Is the centered moving average causal? Is the accumulator causal?",
      "중심 이동 평균과 누산기가 인과인지 판단하세요.",
      ["누산기: $y[n]$ 에 $x[k]$, $k\\le n$ 만 들어가요. 미래 없음 → 인과.",
       "중심 이동 평균: $k=-M$ 일 때 $x[n+M]$ 이 들어가요.",
       "$M\\ge1$ 이면 미래 입력이 필요 → 비인과."],
      "누산기는 인과, 중심 이동 평균은 비인과"),
 ]})

# ---------------- p.71 BIBO 안정 ----------------
S.append({"p": 71, "title": "안정성: BIBO 안정",
 "pass1": [
  say(f"넷째 성질은 {K('stab')}이에요.",
      "적당한 크기의 입력을 넣었을 때 출력도 적당한 크기에 머물면 안정이에요.",
      "조금 넣었는데 출력이 끝없이 커지면 불안정이에요."),
  figure("그릇 속 공과 언덕 위 공", FIG["bowl"], "톡 쳐도 돌아오면 안정, 굴러떨어지면 불안정", 2),
 ],
 "pass2": [
  points(f"{K('bibo')} 이름 풀기",
      "Bounded Input: 크기에 한계가 있는 입력(유계 입력)",
      "Bounded Output: 크기에 한계가 있는 출력(유계 출력)",
      "유계 입력이면 언제나 유계 출력이 나오는 시스템이 안정이에요."),
  formula("안정의 식", r"\forall x:\ |x|<U\ \rightarrow\ |y|<V",
      [(r"\forall x", "포 올 엑스: 모든 입력 x 에 대해"), (r"|x|<U", "입력의 크기가 어떤 한계 U 보다 작으면"),
       (r"\rightarrow", "그러면"), (r"|y|<V", "출력의 크기도 어떤 한계 V 보다 작다")],
      "모든 유계 입력에 대해 출력도 유계면 BIBO 안정이에요."),
  check(f"{K('bibo')}의 뜻은?", ["출력이 항상 0이다", "유계 입력이면 출력도 유계다", "입력이 없으면 출력도 없다"], 1,
      "Bounded-Input Bounded-Output: 한계 있는 입력이면 한계 있는 출력."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (145, 150, 780, 190, f"{K('bibo')}(Bounded Input-Bounded Output) Stability."),
      (195, 205, 1245, 285, "안정 시스템은 작은 입력에 대한 응답이 발산하지 않아요."),
      (195, 305, 1245, 390, "입력이 유계면 출력도 유계여야 안정이라는 문장이에요."),
      (195, 405, 465, 452, "기호로 쓴 정의: 모든 x 에 대해 |x|<U 이면 |y|<V."),
      (545, 375, 800, 715, "안정: 그릇 바닥의 공은 톡 쳐도 흔들리다 제자리로(시간은 아래로)."),
      (860, 375, 1140, 715, "불안정: 언덕 꼭대기 공은 톡 치면 무한히 멀어져요.")),
  prof(W2, "그릇 안의 공은 톡 쳐도 위치가 그 안에서 바운드된다고 했어요.",
      "언덕 위 공은 톡 치면 위치가 계속 떨어져 무한히 가니 언스테이블이라고 했어요.",
      "안정성은 정의에 따라 여러 가지인데 이 수업은 BIBO 안정을 본다고 했어요."),
  bg("기초 다지기 b-1 함수와 그래프 읽기",
      "|x| 는 절댓값, 부호를 떼고 크기만 본 값이에요. $|-3|=3$.",
      "'유계' 는 그래프가 위아래로 어떤 선을 넘지 않는다는 뜻이에요."),
 ],
 "pass4": [
  english("답안 문장",
      "BIBO 안정 시스템은 크기가 유한한(유계인) 모든 입력에 대해 출력의 크기도 유한하게(유계로) 유지되는 시스템이다.",
      "유계 입력 → 유계 출력.",
      "B-I-B-O: 입력 한계 있으면 출력 한계 있음"),
 ]})

# ---------------- p.72 안정 보이기, 불안정 보이기 ----------------
S.append({"p": 72, "title": "안정은 모든 입력, 불안정은 반례 하나",
 "pass1": [
  say(f"{K('stab','을')} 보이는 일과 불안정을 보이는 일은 무게가 달라요.",
      "안정이라고 하려면 모든 입력에 대해 따져야 해요.",
      "불안정이라고 하려면 출력이 폭주하는 입력 하나만 찾으면 돼요."),
  analogy("복리 통장", "매달 잔고에 1%가 붙는 통장은 입금을 조금만 해도 잔고가 끝없이 불어나요.",
      ["매달 붙는 1% 이자", "1.01 을 곱하는 되먹임"], ["끝없이 커지는 잔고", "유계가 아닌 출력"],
      ["조금씩 하는 입금", "유계 입력"]),
 ],
 "pass2": [
  formula("통장 시스템", r"y[n]=x[n]+1.01\,y[n-1]",
      [(r"y[n]", "이번 달 잔고"), (r"x[n]", "이번 달 입금"), (r"1.01\,y[n-1]", "지난달 잔고에 1% 이자를 붙인 것")],
      f"1.01 을 곱하는 {K('fb')} 때문에 출력이 끝없이 커져요. 불안정이에요."),
  compare("보이는 방법", ["보이고 싶은 것", "해야 할 일"],
      ["안정", "모든 유계 입력에 대해 출력이 유계임을 보이기"],
      ["불안정", "출력이 무한히 커지는 유계 입력 하나(반례) 찾기"]),
  check("불안정을 보이려면 무엇이 필요한가요?", ["모든 입력으로 실험", "반례 하나", "입력이 없을 때의 출력"], 1,
      "출력이 폭주하는 유계 입력 하나면 충분해요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (245, 225, 1100, 265, "안정을 보이려면 모든 입력 신호에 대해 해야 해요."),
      (245, 293, 1060, 335, "불안정을 보이려면 반례 하나만 찾으면 돼요."),
      (245, 360, 1220, 480, "은행 통장 이산시간 시스템 식이에요."),
      (245, 500, 1220, 545, "1.01 곱 때문에 한없이 커져요. 불안정해요.")),
  steps("매달 1씩 입금하면 (유계 입력: 늘 1)",
      [r"$y[0]=1$",
       r"$y[1]=1+1.01\times1=2.01$",
       r"$y[2]=1+1.01\times2.01=3.0301$",
       "입력은 늘 1인데 출력은 멈추지 않고 커져요."],
      "유계 입력인데 출력은 한계 없이 커져요. 반례 하나로 불안정 확인."),
  steps("한 번만 1을 입금해도 (입력은 $n=0$ 에만 1)",
      [r"$y[n]=1.01^n$ 이 돼요. 매달 1.01배.",
       r"$1.01^{100}\approx2.705$",
       r"$1.01^{500}\approx145$",
       r"$1.01^{1000}\approx20959$"],
      "천천히지만 끝없이 커지니 불안정이에요."),
  prof(W2, "통장 예는 돈이 계속 늘어나서 인풋이 바운드되어도 아웃풋은 바운드되지 않는다고 했어요.",
      "그래서 언스테이블한 시스템이라고 했어요."),
 ],
 "pass4": [
  check(r"$y[n]=x[n]+0.5\,y[n-1]$ 에 늘 1을 넣으면 출력은?", ["끝없이 커진다", "2에 가까워지며 유계", "0이 된다"], 1,
      "1, 1.5, 1.75, ... 로 2에 다가가요. 곱하는 수가 1보다 작으면 폭주하지 않아요."),
  warn("헷갈리기 쉬운 점",
      "통장 출력이 '천천히' 커진다고 안정이 아니에요. 한계 없이 커지면 불안정이에요.",
      "안정을 보일 때 입력 몇 개로 실험해 보는 것만으로는 부족해요. 모든 유계 입력을 다뤄야 해요."),
 ]})

# ---------------- p.73 안정 그림과 퀵 퀴즈 ----------------
S.append({"p": 73, "title": "여섯 가지 응답 모양과 퀵 퀴즈",
 "pass1": [
  say("같은 계단 입력을 넣었을 때 시스템마다 출력 모양이 달라요.",
      "제자리를 찾으면 안정, 끝없이 커지면 불안정이에요.",
      "아래 퀵 퀴즈로 여러 시스템의 안정성을 판정해 봐요."),
  compare("여섯 칸 그림", ["이름", "모양", "판정"],
      ["settles", "곡선으로 올라가 멈춤", "안정"],
      ["damped", "흔들리다 잦아듦", "안정"],
      ["oscillates", "같은 크기로 계속 흔들림", "경계(marginal)"],
      ["grows", "끝없이 커짐", "불안정"],
      ["grows + osc.", "흔들리며 점점 커짐", "불안정"]),
 ],
 "pass2": [
  compare("퀵 퀴즈 답과 이유", ["시스템", "판정", "이유"],
      [f"{K('delay')} $y[n]=x[n-1]$", "안정", "입력 크기 그대로 한 칸 늦게"],
      [f"{K('acc')}", "불안정", "늘 1을 넣으면 1, 2, 3, ... 끝없이"],
      ["$y=\\cos(x)$", "안정", "cos 는 늘 -1 과 1 사이"],
      ["$y=\\ln(x)$", "불안정", "x 가 0에 다가가면 끝없이 작아짐"],
      ["$y=e^x$", "안정", "입력이 유계면 출력도 유계"]),
  figure(f"{K('acc')}에 {K('step')}을 넣으면", FIG["accu"], "입력은 늘 1인데 출력은 끝없이 커져요.", 1),
  check("늘 1인 입력을 누산기에 넣었을 때 $n=99$ 의 출력은?", ["1", "99", "100"], 2,
      "$y[n]=n+1$ 이라 $y[99]=100$. 계속 커지니 불안정이에요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (170, 195, 510, 365, "입력: 유계 계단(bounded step)."),
      (530, 195, 1225, 365, "안정: 제자리를 찾거나(settles) 흔들리다 잦아들어요(damped)."),
      (170, 380, 510, 548, "경계(marginal): 같은 크기로 계속 흔들려요."),
      (530, 380, 1225, 548, "불안정: 커지거나(grows), 흔들리며 커져요."),
      (85, 620, 1290, 710, "퀵 퀴즈: 지연 안정, 누산기 불안정, cos 안정, ln 불안정, e 의 x제곱은 생각해 보기!")),
  steps("$y=e^x$ 는 안정일까? (think! 의 답)",
      ["입력이 유계라고 해요. 예를 들어 늘 $-2<x<2$.",
       r"$e^x$ 는 x 가 클수록 커지는 함수라서 $e^{-2}<y<e^{2}$ 예요.",
       r"$e^{-2}\approx0.135$, $e^{2}\approx7.389$",
       "출력도 이 사이에 갇혀 있어요. 유계예요."],
      "유계 입력 → 유계 출력이라서 $e^x$ 는 안정이에요."),
  steps("$y=\\ln(x)$ 가 불안정한 이유",
      [r"입력 $x=0.001$ 이면 $\ln(0.001)\approx-6.9$",
       r"$x=0.000001$ 이면 $\ln\approx-13.8$",
       "입력은 0과 1 사이로 작게 갇혀 있는데 출력은 아래로 끝없이 내려가요."],
      "유계 입력인데 출력이 유계가 아니라 불안정이에요."),
  prof(W2, "y 가 e 의 x(t) 제곱인 시스템은 스테이블하다고 했어요.",
      "x 를 -B 에서 B 사이로 바운드시키면 y 는 e 의 -B 제곱과 e 의 B 제곱 사이에서 바운드된다고 설명했어요."),
  bg("기초 다지기 b-4 지수함수와 e",
      "$e\\approx2.718$ 이에요. $e^x$ 는 x 가 커지면 커지고, 작아지면 0에 다가가요.",
      "ln 은 e 의 지수를 거꾸로 찾는 함수예요. $\\ln(e^2)=2$."),
 ],
 "pass4": [
  check("$y(t)=\\cos(x(t))$ 는 BIBO 안정인가요?", ["안정", "불안정"], 0,
      "어떤 입력이든 cos 값은 -1 과 1 사이라서 출력이 늘 유계예요."),
  check("누산기가 불안정한 이유로 알맞은 것은?", ["입력이 유계가 아니라서", "늘 1인 유계 입력에도 출력이 끝없이 커져서", "미래를 봐서"], 1,
      "단위 계단 하나가 반례예요."),
  warn("헷갈리기 쉬운 점",
      "$e^x$ 는 '끝없이 커지는 함수' 라서 불안정이라고 착각하기 쉬워요. 입력이 유계면 출력도 유계라서 안정이에요.",
      "안정은 함수 모양이 아니라 '유계 입력 → 유계 출력' 인지로 판정해요."),
  prof(W2, "여기까지 성질 1, 2, 3, 4(기억, 가역, 인과, 안정)는 시스템이 이런 특성을 가질 수 있다 정도로 보면 된다고 했어요.",
      "어렵지 않고 중요하지는 않다고, 뒤의 시불변성과 선형성이 주요하다고 했어요."),
 ]})

# ---------------- p.74 시불변성 ----------------
S.append({"p": 74, "title": "시불변성: 언제 해도 같은 결과",
 "pass1": [
  say(f"다섯째 성질은 {K('ti')}이에요. 교수님이 주요하다고 한 성질이에요.",
      "같은 입력을 오늘 넣든 내일 넣든 결과가 같은 모양으로 나오면 시불변이에요.",
      "입력을 늦게 넣으면 출력도 그만큼 늦게 나올 뿐이에요."),
  analogy("같은 레시피", "같은 레시피로 월요일에 요리해도, 금요일에 요리해도 맛이 똑같아요.",
      ["레시피", f"{K('sys')}"], ["요리하는 요일", "입력을 넣는 시각"], ["똑같은 맛", "같은 모양의 출력(시각만 밀림)"]),
  figure("월요일과 금요일", FIG["ti"], "입력이 밀리면 출력도 똑같이 밀려요.", 1),
 ],
 "pass2": [
  formula("시불변의 식", r"x(t)\rightarrow y(t)\ \Longrightarrow\ x(t-t_0)\rightarrow y(t-t_0)",
      [(r"x(t)\rightarrow y(t)", "입력 x 를 넣으면 출력 y 가 나온다"),
       (r"x(t-t_0)", f"입력을 $t_0$ 만큼 늦춰 넣으면({K('shift')})"),
       (r"y(t-t_0)", "출력도 똑같이 $t_0$ 만큼 늦게 나온다")],
      "이산시간도 같아요: $x[n-n_0]\\rightarrow y[n-n_0]$."),
  points("정의 두 줄",
      "시스템의 동작과 특성이 시간에 따라 고정되어 있다(fixed over time).",
      "같은 입력을 다른 시각에 넣어도 입출력 실험 결과가 같아야 한다."),
  check(f"{K('ti')}의 뜻은?", ["출력이 시간에 따라 변하지 않는다", "입력을 밀면 출력도 같은 만큼 밀린다", "입력이 없으면 출력도 없다"], 1,
      "출력이 일정하다는 뜻이 아니라, 시스템의 규칙이 시간에 따라 안 바뀐다는 뜻이에요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (150, 185, 890, 222, "시불변: 동작과 특성이 시간에 대해 고정."),
      (175, 230, 1000, 295, "같은 입력을 다른 시각에 넣어도 같은 결과를 기대해요."),
      (510, 320, 890, 440, "연속시간, 이산시간 식. 입력이 밀리면 출력도 같은 만큼 밀려요."),
      (245, 385, 1150, 540, "위: 입력 펄스(파랑)와 출력(주황)."),
      (245, 545, 1150, 700, "아래: 입력을 $t_0$ 만큼 밀었더니 출력도 똑같은 $t_0$ 만큼 밀렸어요.")),
  steps("시불변 확인하는 순서 (시험에서 늘 이 순서)",
      ["1단계: 입력을 먼저 밀어서 시스템에 넣어요. $x(t-t_0)$ 를 넣은 출력을 구해요.",
       "2단계: 원래 출력 $y(t)$ 를 구한 뒤 그 결과를 밀어요. $y(t-t_0)$.",
       "3단계: 두 결과를 비교해요.",
       "같으면 시불변, 하나라도 다르면 시변(time-varying)이에요."],
      "'먼저 밀고 넣기' 와 '넣고 나서 밀기' 가 같으면 시불변."),
  prof(W2, "앞으로 계속 LTI 시스템을 볼 텐데 그중 TI 를 담당하는 게 타임 인베리언트라고 했어요.",
      "인풋이 시프트됐을 때 아웃풋도 그대로 시프트돼야 타임 인베리언트라고 했어요."),
  bg("기초 다지기 b-2 그래프 옮기기, 뒤집기, 늘이기",
      "$x(t-2)$ 는 그래프를 오른쪽으로 2만큼 옮긴 거예요.",
      "빼기인데 오른쪽으로 간다는 점, 교수님이 꼭 기억하라고 한 부분이에요."),
 ],
 "pass4": [
  english("답안 문장",
      "시불변 시스템은 입력을 시간 t0 만큼 이동시키면 출력도 똑같이 t0 만큼 이동할 뿐 모양이 변하지 않는 시스템이다. 즉 x(t) → y(t) 이면 x(t - t0) → y(t - t0) 이다.",
      "입력 이동 → 출력도 같은 만큼 이동.",
      "먼저 밀고 넣기 = 넣고 나서 밀기"),
 ]})

# ---------------- p.75 sin(x) 와 n x[n] ----------------
S.append({"p": 75, "title": "시불변 예 sin(x(t)), 시변 예 n x[n]",
 "pass1": [
  say("두 시스템을 비교해요.",
      "$y(t)=\\sin(x(t))$ 는 언제 넣어도 같은 규칙이라 시불변이에요.",
      "$y[n]=n\\,x[n]$ 은 시각 n 에 따라 곱하는 수가 바뀌어서 시변이에요."),
  analogy("레시피가 바뀌는 식당", "요일마다 소금 양이 바뀌는 레시피라면 같은 재료도 요일마다 맛이 달라요.",
      ["요일마다 바뀌는 소금 양", "시각 n 을 곱하는 부분"], ["맛이 달라짐", f"시변, {K('ti')} 없음"]),
 ],
 "pass2": [
  compare("두 시스템", ["시스템", "곱하는 수", "판정"],
      ["$y(t)=\\sin(x(t))$", "시각과 상관없이 같은 규칙", "시불변"],
      ["$y[n]=n\\,x[n]$", "시각 n 자체(시스템 매개변수가 시간에 따라 변함)", "시변"]),
  points("슬라이드의 대입 확인",
      f"$x_1[n]=\\delta[n]$ ({K('imp')})을 넣으면 $y_1[n]=0$",
      "$x_2[n]=\\delta[n-1]$ 을 넣으면 $y_2[n]=\\delta[n-1]$",
      "입력은 한 칸 밀렸는데 출력은 0을 민 0이 아니에요. 그래서 시변."),
  check("$y[n]=n\\,x[n]$ 이 시변인 이유는?", ["입력을 제곱해서", "입력에 곱하는 수가 시각 n 에 따라 바뀌어서", "미래를 봐서"], 1,
      "슬라이드: 입력에 곱해지는 시스템 매개변수가 시간에 따라 변해요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (150, 215, 640, 300, "시불변인 연속시간 시스템 $y(t)=\\sin(x(t))$."),
      (150, 325, 790, 362, "시간 이동에 대해 변하지 않아요. $x_2(t)=x_1(t-t_0)$ 로 확인."),
      (150, 380, 625, 465, "시변인 이산시간 시스템 $y[n]=n\\,x[n]$."),
      (150, 490, 1195, 565, "입력에 곱하는 매개변수가 시간에 따라 변한다는 설명."),
      (180, 585, 590, 665, f"대입 확인: {K('imp')}과 한 칸 민 임펄스.")),
  steps("$y(t)=\\sin(x(t))$ 시불변 확인",
      [r"1단계(먼저 밀고 넣기): $x_2(t)=x_1(t-t_0)$ 를 넣으면 $y_2(t)=\sin(x_1(t-t_0))$",
       r"2단계(넣고 나서 밀기): $y_1(t)=\sin(x_1(t))$ 를 밀면 $y_1(t-t_0)=\sin(x_1(t-t_0))$",
       "3단계: 두 식이 똑같아요."],
      "그래서 시불변이에요."),
  steps("$y[n]=n\\,x[n]$ 시변 확인 (슬라이드의 대입)",
      [r"$x_1[n]=\delta[n]$: 1은 $n=0$ 에만 있어요. $y_1[n]=n\delta[n]$ 이고 $n=0$ 에서 $0\times1=0$. 그래서 $y_1[n]=0$.",
       r"먼저 밀고 넣기: $x_2[n]=\delta[n-1]$, 1은 $n=1$ 에. $y_2[n]=1\times\delta[n-1]=\delta[n-1]$.",
       r"넣고 나서 밀기: $y_1[n-1]=0$.",
       r"$\delta[n-1]\ne0$ 이라 두 결과가 달라요."],
      "먼저 밀고 넣기와 넣고 나서 밀기가 달라서 시변이에요."),
  prof(W2, "y[n]=n x[n] 에서 x[n-n0] 를 넣으면 n x[n-n0] 인데, y[n-n0] 는 (n-n0) x[n-n0] 라서 둘이 다르다고 했어요.",
      "그래서 타임 인베리언트가 아니라 타임 베링(시변) 시스템이라고 했어요."),
 ],
 "pass4": [
  exam("슬라이드 예제 (p.75)", "Show that y[n] = n x[n] is time-varying.",
      "y[n]=n x[n] 이 시변임을 보이세요.",
      [r"입력을 $n_0$ 밀어 넣으면 출력은 $n\,x[n-n_0]$.",
       r"원래 출력을 $n_0$ 밀면 $(n-n_0)\,x[n-n_0]$.",
       r"$n_0\ne0$ 이면 두 식이 달라요.",
       r"반례: $\delta[n]\rightarrow0$, $\delta[n-1]\rightarrow\delta[n-1]\ne0$."],
      "시변(time-varying)"),
  check("$y(t)=\\sin(x(t))$ 에 대해 맞는 것은?", ["시불변", "시변"], 0,
      "t 가 식 밖에 따로 나오지 않고 입력에만 규칙을 적용해요."),
 ]})

# ---------------- p.76 y(t)=x(2t) ----------------
S.append({"p": 76, "title": "시간 척도 변환 y(t)=x(2t) 는 시불변일까?",
 "pass1": [
  say(f"2배속 재생 시스템 $y(t)=x(2t)$ 를 봐요. {K('scale')}이에요.",
      "영상을 2배속으로 틀면 모든 장면이 반으로 짧아지죠.",
      "늦게 튼 영상도 2배속 하면 시작 시각까지 반으로 당겨져서 모양이 어긋나요."),
  analogy("2배속 재생", "10초에 시작하는 장면을 2배속으로 틀면 5초에 시작해요. 늦춘 만큼이 절반만 남아요.",
      ["2배속 재생", "$y(t)=x(2t)$"], ["장면 시작을 늦추기", "입력 이동 $x(t-2)$"],
      ["늦춘 시간도 반으로 줄어듦", f"{K('ti')}이 깨짐"]),
 ],
 "pass2": [
  points("슬라이드 그림 다섯 개",
      "(a) $x_1(t)$: -2 부터 2 까지 높이 1인 사각형",
      "(b) $y_1(t)=x_1(2t)$: -1 부터 1 까지로 줄어요",
      "(c) $x_2(t)=x_1(t-2)$: 입력을 2 밀어서 0 부터 4",
      "(d) $y_2(t)=x_2(2t)$: 0 부터 2",
      "(e) $y_1(t-2)$: 출력을 2 밀어서 1 부터 3"),
  figure("(d) 와 (e) 비교", FIG["x2t"], "먼저 밀고 넣기 [0, 2] 와 넣고 나서 밀기 [1, 3] 이 달라요.", 3),
  check("(d) $y_2(t)$ 와 (e) $y_1(t-2)$ 가 다르다는 것은?", ["시불변이다", "시불변이 아니다", "선형이 아니다"], 1,
      "입력을 민 결과와 출력을 민 결과가 다르면 시불변이 아니에요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (135, 180, 660, 390, "질문: 시간 척도 시스템 $y(t)=x(2t)$ 는 시불변인가?"),
      (815, 180, 1230, 325, "(a) 입력 -2~2, (b) 출력 -1~1."),
      (815, 355, 1230, 500, "(c) 입력을 2 민 x2 는 0~4, (d) 그 출력 y2 는 0~2."),
      (925, 530, 1120, 675, "(e) 원래 출력을 2 민 것은 1~3. (d) 와 달라요.")),
  steps("구간 끝점을 직접 계산",
      [r"(d) $y_2(t)=x_2(2t)=x_1(2t-2)$. $x_1$ 은 괄호 안이 -2~2 일 때 1.",
       r"$2t-2=-2$ 에서 $t=0$, $2t-2=2$ 에서 $t=2$. 그래서 $y_2$ 는 0~2.",
       r"(e) $y_1(t-2)=x_1(2(t-2))=x_1(2t-4)$. $2t-4=-2$ 에서 $t=1$, $2t-4=2$ 에서 $t=3$.",
       r"그래서 $y_1(t-2)$ 는 1~3.",
       r"핵심 차이: $x_1(2t-2)$ 와 $x_1(2t-4)$. 입력의 2 밀기가 출력에서는 1 밀기로 줄었어요."],
      "0~2 와 1~3 이 달라서 $y(t)=x(2t)$ 는 시불변이 아니에요."),
  prof(W2, "타임 스케일링을 하면 폭이 두 배 좁아져서 -2~2 가 -1~1 이 된다고 했어요.",
      "x1 을 2 만큼 옮기면 0~4 가 되고, 그걸 시스템에 넣으면 0~2 인데 y1(t-2) 는 1~3 이라 둘이 다르다고 했어요.",
      "표정들이 안 좋다며 한 번 더 설명했을 만큼 헷갈리는 예제예요."),
 ],
 "pass4": [
  exam("교재 예제, 슬라이드 (p.76)", "Is the time scaling system y(t) = x(2t) time-invariant?",
      "y(t)=x(2t) 가 시불변인지 판정하세요.",
      [r"먼저 밀고 넣기: $x(t-t_0)$ 를 넣으면 $x(2t-t_0)$.",
       r"넣고 나서 밀기: $y(t-t_0)=x(2(t-t_0))=x(2t-2t_0)$.",
       r"$t_0\ne0$ 이면 $2t-t_0\ne2t-2t_0$.",
       "슬라이드 반례: 사각형 입력에서 0~2 와 1~3 으로 달라요."],
      "시불변이 아니다(시변)"),
  warn("헷갈리기 쉬운 점",
      r"$x(2t)$ 에 $t_0$ 밀기를 넣을 때 $x(2t-t_0)$ 와 $x(2t-2t_0)$ 를 헷갈리지 마세요. t 자리에 $t-t_0$ 를 넣는 쪽은 출력 밀기예요.",
      f"{K('scale')} 시스템은 {K('lin')}은 만족해요. 선형인데 시불변은 아닌 예로도 쓸 수 있어요."),
 ]})

# ---------------- p.77 선형성 ----------------
S.append({"p": 77, "title": "선형성: 가장 중요한 성질",
 "pass1": [
  say(f"여섯째, 마지막 성질은 {K('lin')}이에요.",
      "슬라이드는 시스템이 가질 수 있는 가장 중요한 성질이라고 해요.",
      "선형이면 복잡한 응답을 쉬운 응답들의 합으로 나눠 풀 수 있어요."),
  analogy("정직한 계산기", "두 배 넣으면 두 배가 나오고, 둘을 섞어 넣으면 결과도 섞여 나오는 정직한 계산기예요.",
      ["두 배 넣으면 두 배", f"척도({K('homo')})"], ["섞어 넣으면 섞여 나옴", f"{K('add')}"],
      ["정직한 계산기", f"{K('lin')}이 있는 시스템"]),
 ],
 "pass2": [
  formula("선형의 두 조건", r"a\,x_1(t)+b\,x_2(t)\ \rightarrow\ a\,y_1(t)+b\,y_2(t)",
      [(r"x_1\rightarrow y_1,\ x_2\rightarrow y_2", "각각 넣었을 때의 출력을 알고 있을 때"),
       (r"x_1+x_2\rightarrow y_1+y_2", f"{K('add')}: 합을 넣으면 출력도 합"),
       (r"a\,x_1\rightarrow a\,y_1", f"척도, {K('homo')}: a 배 넣으면 a 배. a 는 {K('cplx')}도 돼요"),
       (r"a,\ b", "아무 상수")],
      "두 조건을 합친 것이 이 식이에요. 둘 다 만족해야 선형이에요."),
  compare("선형처럼 보이는 그래프와 아닌 그래프", ["그래프", "선형?"],
      ["원점을 지나는 직선(오른쪽 위 점선)", "선형"],
      ["끝에서 꺾여 평평해짐(포화)", "아님"],
      ["곡선으로 휘어짐", "아님"],
      ["평행사변형 고리(오갈 때 다른 길)", "아님"]),
  check(f"{K('lin')}의 두 조건은?", ["가산성과 척도(동차성)", "인과성과 안정성", "기억성과 가역성"], 0,
      "Additive 와 Scaling, 둘 다 만족해야 해요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (185, 190, 850, 225, "시스템이 가질 수 있는 가장 중요한 성질이 선형성."),
      (185, 235, 1040, 300, f"응답을 더 쉬운 응답들의 합으로 분석할 수 있게 해 줘요({K('conv')})."),
      (185, 320, 1040, 460, "단순하게는 직선(원점을 지나는)으로 상상할 수 있어요."),
      (225, 415, 790, 550, "가산(Additive), 척도(Scaling, a 는 복소수), 합친 식(Combined)."),
      (560, 580, 1040, 700, "선형이 아닌 입출력 그래프 세 개.")),
  steps("$y=3x$ 로 두 조건 확인 ($x_1=1$, $x_2=2$)",
      ["각각: $y_1=3$, $y_2=6$",
       "가산: $x_1+x_2=3$ 을 넣으면 $9$. $y_1+y_2=3+6=9$. 같아요.",
       "척도: $a=2$ 배 한 $2x_1=2$ 를 넣으면 6. $2y_1=6$. 같아요.",
       "둘 다 통과."],
      "$y=3x$ 는 선형이에요."),
  bg("기초 다지기 b-10 손으로 하는 컨볼루션",
      f"슬라이드의 '(convolution)' 은 다음 주 2장의 {K('conv')}를 미리 말한 거예요.",
      f"선형이면 입력을 작은 조각으로 나눠 조각별 응답을 더하면 돼요. 이게 {K('conv')}의 출발점이에요."),
 ],
 "pass4": [
  english("답안 문장",
      "선형 시스템은 가산성(x1+x2 → y1+y2)과 동차성(ax → ay)을 모두 만족하는 시스템이며, 합쳐서 ax1+bx2 → ay1+by2 로 쓴다.",
      "가산성 + 동차성 = 선형성(중첩).",
      "더하면 더해지고, 곱하면 곱해진다"),
  warn("헷갈리기 쉬운 점",
      "그래프로 보면 선형은 '원점을 지나는' 직선이에요. 직선이어도 원점을 안 지나면(3x+2) 선형이 아니에요.",
      "척도의 a 는 실수뿐 아니라 복소수도 포함해요($a\\in\\mathbb{C}$). p.84 예제에서 중요해요."),
 ]})

# ---------------- p.78 가산성과 동차성 그림 ----------------
S.append({"p": 78, "title": "가산성과 동차성 그림",
 "pass1": [
  say(f"{K('lin','을')} 이루는 두 조건을 그림으로 봐요.",
      f"왼쪽은 {K('add')}: 따로 넣은 결과를 더한 것 = 합쳐 넣은 결과.",
      f"오른쪽은 {K('homo')}: k 배 넣으면 출력도 k 배."),
 ],
 "pass2": [
  compare("두 그림", ["", "가산성(FIGURE 5-3)", "동차성(FIGURE 5-2)"],
      ["IF", "$x_1[n]\\rightarrow y_1[n]$, $x_2[n]\\rightarrow y_2[n]$", "$x[n]\\rightarrow y[n]$"],
      ["THEN", "$x_1[n]+x_2[n]\\rightarrow y_1[n]+y_2[n]$", "$k\\,x[n]\\rightarrow k\\,y[n]$"],
      ["한 줄 뜻", "더한 신호가 서로 간섭 없이 통과", "크기를 바꾸면 출력 크기도 똑같이"]),
  check(f"{K('homo')}을 뜻하는 것은?", ["$x_1+x_2\\rightarrow y_1+y_2$", "$k\\,x\\rightarrow k\\,y$", "$x(t-t_0)\\rightarrow y(t-t_0)$"], 1,
      "세 번째는 시불변이에요. 헷갈리지 마세요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (85, 150, 1290, 195, "x1 → y1, x2 → y2 이면 합은 합으로, k 배는 k 배로 가야 한다는 문장."),
      (155, 215, 625, 640, f"{K('add')}: 위 두 줄이 IF, 아래 줄이 THEN."),
      (155, 648, 625, 712, "그림 설명: 더한 신호가 서로 간섭하지 않고 통과하면 가산적."),
      (680, 265, 1215, 590, f"{K('homo')}: 입력을 k 배 하면 출력도 k 배."),
      (680, 595, 1215, 685, "그림 설명: 입력의 크기 변화가 출력에 똑같이 나타나면 동차적.")),
  prof(W3, "3주차 복습: 리니어는 슈퍼 포지션이 되는 것이고, 에디티비티와 스케일링 두 가지를 모두 가져야 한다고 했어요.",
      "ax1 + bx2 가 같은 시스템에서 ay1 + by2 로 가면 슈퍼 포지션이 되고 이게 리니어라고 했어요."),
  prof(W2, "스케일링은 호모지니어티(동차성)라고도 부른다고 했어요."),
 ],
 "pass4": [
  check(f"{K('add')}만 만족하고 동차성이 깨지면 선형인가요?", ["선형이다", "선형이 아니다"], 1,
      "둘 다 만족해야 선형이에요. p.84 의 Re{x} 가 그런 예예요."),
 ]})

# ---------------- p.79 y=3x, 3x^2, 3x+2 ----------------
S.append({"p": 79, "title": "선형 판정 예: 3x, 3x제곱, 3x+2",
 "pass1": [
  say("세 시스템 중 선형은 하나뿐이에요.",
      "$y=3x$ 는 정직한 계산기, 선형이에요.",
      "제곱이 들어가거나, 늘 2를 더해 주면 선형이 깨져요."),
  figure("세 그래프", FIG["lin"], "원점을 지나는 직선 3x 만 선형이에요.", 2),
 ],
 "pass2": [
  compare("세 시스템 한눈에", ["시스템", "판정", "슬라이드의 이유"],
      ["$y=3x(t)$", "선형", "가산성과 척도 모두 성립"],
      ["$y=3x^2(t)$", "비선형", "제곱이 가산성을 깨요"],
      ["$y=3x(t)+2$", "비선형", "척도가 깨져요: 0을 넣으면 0이 나와야 하는데 2가 나와요"]),
  points("0 넣어 보기 요령",
      f"{K('lin','이')} 있으면 0을 넣었을 때 반드시 0이 나와요(0배 척도).",
      "$3x+2$ 는 0을 넣으면 2. 그 자리에서 탈락이에요.",
      "단, 0이 나온다고 선형이 확정되진 않아요($3x^2$ 도 0을 넣으면 0)."),
  check("$y(t)=3x(t)+2$ 는?", ["선형", "비선형"], 1,
      "직선처럼 보여도 +2 때문에 0 입력에 0이 안 나와요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (218, 195, 1170, 250, "세 시스템: 3x 는 체크, 나머지 둘은 X."),
      (85, 295, 950, 340, "3x: 가산성과 척도 모두 성립, 선형."),
      (85, 355, 910, 400, "3x제곱: 제곱이 가산성을 깨서 비선형."),
      (85, 415, 1320, 460, "3x+2: 0 입력에 2가 나와 척도가 깨져서 비선형.")),
  steps("$x_1=1$, $x_2=2$ 로 가산성 시험",
      ["$y=3x$: $y_1=3$, $y_2=6$. 합 입력 3 → 9. $3+6=9$ 같음.",
       "$y=3x^2$: $y_1=3$, $y_2=12$. 합 입력 3 → $3\\times9=27$. $3+12=15$ 달라요.",
       "$y=3x+2$: $y_1=5$, $y_2=8$. 합 입력 3 → 11. $5+8=13$ 달라요.",
       "$3x+2$ 에서 차이 2는 '+2' 가 두 번 더해져서 생겨요."],
      "가산성은 3x 만 통과해요."),
  steps("$y=3x+2$ 의 다른 성질도 확인",
      ["기억: 지금 x 만 써요 → 무기억.", "인과: 미래 안 봄 → 인과.",
       "안정: $|x|<U$ 이면 $|y|\\le3U+2$ → 안정.",
       "시불변: $x(t-t_0)$ 넣으면 $3x(t-t_0)+2=y(t-t_0)$ → 시불변.",
       "선형: 위처럼 탈락 → 비선형."],
      "시불변이지만 선형이 아니에요. 두 성질은 따로 봐야 해요."),
  prof(W2, "3x 는 x1+x2 를 넣으면 y1+y2 와 같고, a 를 곱해도 ay1 이 되니 리니어라고 했어요.",
      "3x+2 는 둘을 더하면 3x1+3x2+4 가 돼서 2가 더 붙으니 가산성에서 탈락이라고 했어요.",
      "선형식처럼 생겨서 리니어일 것 같지만 실제로는 논리니어라고 강조했어요."),
 ],
 "pass4": [
  exam("슬라이드 예제 (p.79)", "Determine whether y = 3x(t), y = 3x^2(t), y = 3x(t) + 2 are linear.",
      "세 시스템이 선형인지 판정하세요.",
      [r"$3x$: $3(ax_1+bx_2)=a(3x_1)+b(3x_2)$ → 선형.",
       r"$3x^2$: $3(x_1+x_2)^2=3x_1^2+6x_1x_2+3x_2^2\ne3x_1^2+3x_2^2$ → 비선형.",
       r"$3x+2$: $3(x_1+x_2)+2\ne(3x_1+2)+(3x_2+2)$, 또 0 입력 → 2 → 비선형."],
      "3x 만 선형, 3x제곱과 3x+2 는 비선형"),
  warn("시험 함정",
      "$y=3x+2$ 는 선형이 아니에요. 그래프가 직선이라 선형이라고 쓰기 쉬워요.",
      "빠른 판별: 0을 넣어 0이 안 나오면 바로 비선형."),
  english("답안 문장",
      "y(t) = 3x(t) + 2 는 입력이 0일 때 출력이 2가 되어 동차성이 성립하지 않으므로(가산성도 성립하지 않음) 선형 시스템이 아니다.",
      "0 입력 → 0 출력이 아니면 비선형.",
      "상수를 더하면 비선형"),
 ]})

# ---------------- p.80 중첩 원리 ----------------
S.append({"p": 80, "title": "중첩 원리: 쉬운 조각으로 나눠 풀기",
 "pass1": [
  say("복잡한 입력도 쉬운 신호 여러 개를 더한 것으로 볼 수 있어요.",
      "선형 시스템이면 조각마다 출력을 구해서 똑같이 더하면 끝이에요.",
      f"이것을 {K('sup')}라고 해요."),
  analogy("정직한 계산기로 나눠 계산", "큰 계산을 작은 계산 여러 개로 나눠 하고 결과를 더해도 같은 답이 나와요.",
      ["작은 계산들", "쉬운 입력 조각 $x_k[n]$"], ["작은 답을 더하기", "출력 조각 $y_k[n]$ 의 합"]),
 ],
 "pass2": [
  formula("입력을 조각으로", r"x[n]=\sum_k a_k x_k[n]=a_1x_1[n]+a_2x_2[n]+a_3x_3[n]+\cdots",
      [(r"x_k[n]", "쉬운 기본 신호(basis) 조각"), (r"a_k", "각 조각에 곱한 크기"), (r"\sum_k", "조각을 모두 더함")],
      "입력을 쉬운 조각들의 선형 합으로 써요."),
  formula("출력도 조각으로", r"y[n]=\sum_k a_k y_k[n]=a_1y_1[n]+a_2y_2[n]+\cdots",
      [(r"y_k[n]", "조각 $x_k$ 하나를 넣었을 때의 출력"), (r"a_k", "입력과 똑같은 크기를 곱함")],
      f"선형이면 출력도 같은 크기로 더한 것. 이것이 {K('sup')}예요."),
  check(f"{K('sup')}가 성립하는 시스템은?", ["모든 시스템", "선형 시스템", "인과 시스템"], 1,
      "연속시간, 이산시간 모두 선형 시스템에서 성립해요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (125, 230, 1300, 275, "입력 x[n] 이 더 쉬운 신호 $x_k[n]$ 들의 선형 합이라고 하면"),
      (160, 290, 875, 340, "입력 식."),
      (160, 415, 880, 465, "선형 시스템의 응답: 같은 크기로 출력 조각들을 더한 것."),
      (160, 480, 1300, 570, "쉬운 신호에 대한 반응을 알면 복잡한 신호의 반응을 선형 합으로 구할 수 있다는 기본 생각."),
      (160, 590, 1290, 630, "이것이 중첩 원리. 연속시간과 이산시간 선형 시스템 모두 성립.")),
  steps("쉬운 숫자로 중첩 ($y=3x$, 조각 $x_1=1$, $x_2=2$, $a_1=4$, $a_2=5$)",
      [r"입력 $x=4\times1+5\times2=14$",
       r"조각 출력: $y_1=3$, $y_2=6$",
       r"중첩: $4\times3+5\times6=12+30=42$",
       r"직접 계산: $3\times14=42$. 같아요."],
      "조각별로 풀어 더해도 한 번에 푼 것과 같아요."),
  bg("기초 다지기 b-7 시그마로 더하기",
      "$\\sum_k$ 는 k 를 바꿔 가며 모두 더하라는 기호예요.",
      "$\\sum_{k=1}^{3}k=1+2+3=6$ 처럼 읽어요."),
 ],
 "pass4": [
  prof(W3, "3주차에 모든 이산시간 신호를 시프트된 임펄스들의 선형 합으로 표현할 수 있다고 했어요.",
      "그래서 선형 시스템의 출력이 임펄스 응답들의 합으로 표현된다고 했어요. 이 쪽의 중첩이 그 출발점이에요."),
  say(f"다음 주 2장에서 이 생각이 {K('lti')}와 {K('conv')}로 이어져요.",
      MANTRA_LTI),
 ]})

# ---------------- p.81 연속, 이산 중첩 ----------------
S.append({"p": 81, "title": "연속시간과 이산시간의 중첩 원리",
 "pass1": [
  say("짧은 펄스 두 개를 따로 넣으면 메아리가 하나씩 생겨요.",
      "두 펄스를 한꺼번에 넣으면 두 메아리가 그대로 더해져 나와요.",
      "선형 시스템에서는 연속시간이든 이산시간이든 이렇게 돼요."),
  figure("펄스 둘, 메아리 둘", FIG["sup"], "합을 넣으면 출력도 합", 2),
 ],
 "pass2": [
  compare(f"두 가지 {K('sup')}", ["", "연속시간", "이산시간"],
      ["식", "$ax_1(t)+bx_2(t)\\rightarrow ay_1(t)+by_2(t)$", "$ax_1[n]+bx_2[n]\\rightarrow ay_1[n]+by_2[n]$"],
      ["변수", "t (둥근 괄호)", "n (대괄호)"],
      ["성립 조건", "선형 시스템", "선형 시스템"]),
  check("세 번째 줄 그림에서 출력이 두 메아리의 합인 이유는?", ["시스템이 선형이라서", "입력이 같아서", "시간이 멈춰서"], 0,
      "선형이면 합을 넣은 출력이 출력들의 합이에요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (120, 185, 655, 280, "연속시간 중첩 원리 식."),
      (710, 185, 1280, 280, "이산시간 중첩 원리 식."),
      (275, 315, 1075, 375, "첫째 줄: x1 → y1."),
      (275, 410, 1075, 460, "둘째 줄: x2 → y2."),
      (275, 505, 1075, 560, "셋째 줄: x1+x2 → y1+y2. 두 메아리가 겹쳐 나와요."),
      (85, 590, 790, 640, "선형 시스템이면 연속, 이산 모두 참.")),
  steps("그림을 시불변과 함께 읽기",
      [f"짧은 펄스는 {K('imp')}(손뼉 한 번)을 닮았어요. x2 는 x1 과 같은 펄스를 늦게 넣은 거예요.",
       "그림에서 y2 도 y1 과 같은 모양이 늦게 나와요. 시불변 덕분이에요.",
       "그래서 선형 + 시불변이면 펄스 하나의 메아리만 알면 모든 입력의 출력을 알 수 있어요."],
      f"이것이 {K('lti')}가 강력한 이유예요."),
 ],
 "pass4": [
  check("중첩 원리 식 $ax_1+bx_2\\rightarrow ay_1+by_2$ 가 담고 있는 두 조건은?", ["가산성과 동차성", "인과성과 기억성", "시불변성과 안정성"], 0,
      "더하기(가산)와 상수배(동차)를 한 식에 담았어요."),
 ]})

# ---------------- p.82 y = t x(t) ----------------
S.append({"p": 82, "title": "y(t)=t x(t): 선형이지만 시변",
 "pass1": [
  say("$y(t)=t\\,x(t)$ 는 입력에 시각 t 를 곱하는 시스템이에요.",
      "선형이지만 시불변은 아니에요.",
      f"{K('lin','과')} {K('ti','은')} 서로 따로 노는 성질이라는 예예요."),
 ],
 "pass2": [
  formula("선형 확인 식", r"t\,(ax_1(t)+bx_2(t))=a\,t x_1(t)+b\,t x_2(t)=a y_1+b y_2",
      [(r"t\,(ax_1+bx_2)", "섞은 입력을 넣은 출력"), (r"a\,tx_1+b\,tx_2", "괄호를 풀어요(분배)"),
       (r"ay_1+by_2", "각 출력을 같은 비율로 섞은 것")],
      f"양쪽이 같아서 {K('sup')}가 성립, 선형이에요."),
  points("슬라이드 결론",
      "LINEAR: 선형이다.",
      "even though it is time-varying (Non TI): 시변인데도.",
      "linearity and TI are independent properties: 선형성과 시불변성은 서로 독립."),
  check("$y(t)=t\\,x(t)$ 에 대해 맞는 것은?", ["선형, 시불변", "선형, 시변", "비선형, 시불변"], 1,
      "곱하는 t 가 시각마다 달라져서 시변, 하지만 중첩은 성립해서 선형이에요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (595, 195, 800, 245, "시스템 $y(t)=t\\,x(t)$."),
      (85, 285, 1240, 345, "섞은 입력을 넣고 풀면 $ay_1+by_2$ 가 돼서 체크."),
      (85, 355, 1280, 450, "선형이다. 시변인데도. 선형성과 시불변성은 독립.")),
  steps("숫자로 선형 확인 ($t=4$, $x_1(4)=1$, $x_2(4)=2$, $a=2$, $b=3$)",
      [r"섞은 입력: $2\times1+3\times2=8$. 출력 $4\times8=32$.",
       r"따로: $y_1=4\times1=4$, $y_2=4\times2=8$.",
       r"섞은 출력: $2\times4+3\times8=8+24=32$.",
       "같아요. 선형."],
      "어느 t 에서든 이렇게 맞아요."),
  steps("숫자로 시변 확인 (입력 $u(t)$, 1만큼 밀기)",
      [r"원래: $x_1=u(t)$ → $y_1(t)=t\,u(t)$",
       r"먼저 밀고 넣기: $x_2=u(t-1)$ → $y_2(t)=t\,u(t-1)$. $t=2$ 에서 $2\times1=2$.",
       r"넣고 나서 밀기: $y_1(t-1)=(t-1)\,u(t-1)$. $t=2$ 에서 $1\times1=1$.",
       "2와 1, 달라요. 시변."],
      "선형이지만 시불변이 아니에요."),
  steps("나머지 성질도 확인",
      ["기억: 지금 x(t) 만 써요 → 무기억.",
       "인과: 미래 안 봄 → 인과.",
       "안정: $x(t)=1$ (유계) 을 넣으면 $y=t$ 가 끝없이 커져요 → 불안정."],
      "무기억, 인과, 불안정, 선형, 시변."),
  prof(W2, "t x(t) 는 리니어한데 타임 인베리언트는 아닌 시스템이라고 했어요.",
      "리니어하다고 해서 항상 타임 인베리언트한 건 아니고, 반대도 마찬가지라고 했어요."),
 ],
 "pass4": [
  exam("슬라이드 예제 (p.82)", "Is y(t) = t x(t) linear? Is it time-invariant?",
      "t x(t) 가 선형인지, 시불변인지 판정하세요.",
      [r"선형: $t(ax_1+bx_2)=a\,tx_1+b\,tx_2=ay_1+by_2$ → 선형.",
       r"시불변: 밀고 넣기 $t\,x(t-t_0)$, 넣고 밀기 $(t-t_0)\,x(t-t_0)$.",
       r"$t_0\ne0$ 이면 달라요 → 시변."],
      "선형이지만 시변"),
  english("답안 문장",
      "선형성과 시불변성은 서로 독립인 성질이다. 예를 들어 y(t) = t x(t) 는 선형이지만 시변이고, y(t) = x²(t) 는 시불변이지만 비선형이다.",
      "선형 ≠ 시불변. 따로 판정.",
      "t 가 식 밖에 곱해지면 시변 의심"),
 ]})

# ---------------- p.83 y = x^2 ----------------
S.append({"p": 83, "title": "y(t)=x²(t): 교차항 때문에 비선형",
 "pass1": [
  say("제곱하는 시스템은 선형이 아니에요.",
      "두 입력을 더해서 제곱하면, 따로 제곱해 더한 것보다 덤이 더 붙어요.",
      "그 덤, 교차항이 범인이에요."),
 ],
 "pass2": [
  formula("가산성 확인", r"(x_1+x_2)^2=x_1^2+2x_1x_2+x_2^2\ \ne\ x_1^2+x_2^2",
      [(r"(x_1+x_2)^2", "합을 넣은 출력"), (r"x_1^2+x_2^2", "따로 넣은 출력의 합"),
       (r"2x_1x_2", "교차항(cross-term): 여기서 차이가 나요")],
      "교차항 $2x_1x_2$ 때문에 가산성이 깨져요. 비선형."),
  check("$y=x^2$ 의 가산성을 깨는 항은?", ["$x_1^2$", "$2x_1x_2$", "$x_2^2$"], 1,
      "슬라이드: the cross-term $2x_1x_2$ is the culprit."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (610, 195, 790, 245, "시스템 $y(t)=x^2(t)$."),
      (85, 285, 1090, 345, "가산성 확인: 전개하면 교차항이 생겨서 X."),
      (85, 355, 935, 400, "비선형. 교차항 $2x_1x_2$ 가 범인.")),
  steps("숫자로 ($x_1=1$, $x_2=2$)",
      [r"합 입력 3 → $3^2=9$",
       r"따로: $1^2+2^2=1+4=5$",
       r"차이 $9-5=4$ 는 교차항 $2\times1\times2=4$",
       r"척도도 확인: $2\times3=6$ 을 넣으면 36, 그런데 $2\times9=18$. 역시 달라요."],
      "가산성도 척도도 깨져요. 비선형."),
  steps("나머지 성질",
      ["기억: 무기억.  인과: 인과.",
       "안정: $|x|<U$ 이면 $y<U^2$ → 안정.",
       r"시불변: $x(t-t_0)$ 넣으면 $x^2(t-t_0)=y(t-t_0)$ → 시불변.",
       "가역: 2와 -2 가 같은 4 → 가역 아님."],
      "시불변이지만 비선형. p.82 와 반대 짝이에요."),
  prof(W2, "x 제곱 t 는 TI 는 맞는데 L 은 아니라고 정리했어요.",
      "L 도 TI 도 아닌 예로는 t 곱하기 x 제곱 t 같은 것이 있다고 했어요."),
 ],
 "pass4": [
  compare("교수님 정리: L 과 TI 네 칸", ["시스템", "선형", "시불변"],
      ["$y=3x(t)$", "O", "O (LTI)"],
      ["$y=t\\,x(t)$", "O", "X"],
      ["$y=x^2(t)$", "X", "O"],
      ["$y=t\\,x^2(t)$", "X", "X"]),
  check("$y(t)=t\\,x^2(t)$ 는?", ["선형이고 시불변", "선형도 시불변도 아님", "선형만"], 1,
      "제곱 때문에 비선형, t 곱 때문에 시변이에요."),
 ]})

# ---------------- p.84 Example 1.19 Re{x} ----------------
S.append({"p": 84, "title": "Example 1.19: y[n]=Re{x[n]} 는 선형일까?",
 "pass1": [
  say(f"입력이 {K('cplx')}일 때 실수 부분만 꺼내는 시스템이에요.",
      "더하기는 잘 통과하고, 실수를 곱하는 것도 통과해요.",
      "그런데 허수 j 를 곱하면 깨져요. 그래서 선형이 아니에요."),
 ],
 "pass2": [
  formula("입력을 실수부와 허수부로", r"x_1[n]=r[n]+j\,s[n]",
      [(r"r[n]", "실수 부분"), (r"s[n]", "허수 부분의 크기"), (r"j", f"{K('jj')}, $j^2=-1$"),
       (r"\mathrm{Re}\{x_1[n]\}=r[n]", "Re 는 실수 부분만 꺼내요")],
      "그래서 $y_1[n]=r[n]$ 이에요."),
  formula("j 를 곱해 보기", r"x_2=jx_1\Rightarrow y_2=\mathrm{Re}\{jr-s\}=-s\ \ne\ jy_1=jr",
      [(r"jx_1=j(r+js)=jr-s", "$j\\times j=-1$ 이라 $js\\times j=-s$"),
       (r"y_2=-s", "실수 부분은 $-s$"), (r"jy_1=jr", "척도가 맞으려면 나와야 할 값")],
      "$-s$ 와 $jr$ 가 달라서 척도(동차성)가 깨져요."),
  check("Example 1.19 에서 선형이 아닌 이유는?", ["가산성이 깨져서", "복소수 상수 j 로 척도가 깨져서", "미래를 봐서"], 1,
      "가산성과 실수 척도는 되지만, 선형성은 복소수 상수까지 허용해요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (85, 150, 740, 192, "교재 Example 1.19: Re{x[n]} 는 선형인가? (슬라이드 제목의 Examle 은 Example 오타)"),
      (85, 210, 1175, 248, "가산성과 실수 척도는 되지만 선형성은 복소수 상수도 허용한다는 문장."),
      (553, 268, 840, 315, "시스템: 실수 부분 꺼내기."),
      (60, 350, 1335, 405, "j 를 곱한 입력의 출력 $-s$ 는 $jy_1=jr$ 과 달라요."),
      (85, 455, 970, 495, "j 척도 실패 → 복소수 기준으로 선형이 아님.")),
  steps("숫자로 ($x_1=3+4j$)",
      [r"$y_1=\mathrm{Re}\{3+4j\}=3$",
       r"$x_2=jx_1=j(3+4j)=3j+4j^2=3j-4=-4+3j$",
       r"$y_2=\mathrm{Re}\{-4+3j\}=-4$",
       r"척도라면 $jy_1=3j$ 여야 하는데 $-4$. 달라요."],
      "j 척도가 깨져서 비선형이에요."),
  steps("가산성은 되는지 확인 ($x_1=3+4j$, $x_2=1-2j$)",
      [r"합 $=4+2j$, 실수부 4",
       r"따로: $3+1=4$",
       "같아요. 가산성은 성립해요."],
      "가산성만으로는 선형이 아니에요. 척도까지 필요해요."),
  bg("기초 다지기 b-5 복소수와 복소평면",
      f"{K('cplx')}는 실수부와 허수부로 이루어져요. $3+4j$ 의 실수부는 3, 허수부는 4.",
      f"{K('jj')} j 는 $j^2=-1$ 인 수예요. 교수님과 교재는 i 대신 j 를 써요."),
 ],
 "pass4": [
  exam("교재 Example 1.19 (p.84)", "Is y[n] = Re{x[n]} linear?",
      "실수부를 꺼내는 시스템이 선형인지 판정하세요.",
      [r"가산성: $\mathrm{Re}\{x_1+x_2\}=\mathrm{Re}\{x_1\}+\mathrm{Re}\{x_2\}$ 성립.",
       r"실수 a 척도: $\mathrm{Re}\{ax\}=a\,\mathrm{Re}\{x\}$ 성립.",
       r"복소수 j 척도: $x_1=r+js$ 이면 $\mathrm{Re}\{jx_1\}=-s\ne j\,r$.",
       "선형성은 복소수 상수도 허용하므로 조건이 깨져요."],
      "선형이 아니다(복소수 상수 기준)"),
  warn("헷갈리기 쉬운 점",
      "가산성만 보고 선형이라고 결론 내면 틀려요. 척도, 특히 복소수 상수까지 확인하세요.",
      "p.77 의 $a\\in\\mathbb{C}$ 가 바로 이 예제를 위한 조건이에요."),
 ]})

# ---------------- p.85 Example 1.20 증분 선형 ----------------
S.append({"p": 85, "title": "Example 1.20: 증분 선형 시스템 y[n]=2x[n]+3",
 "pass1": [
  say("$y[n]=2x[n]+3$ 은 3x+2 와 같은 모양이라 선형이 아니에요.",
      "하지만 '선형 시스템 + 늘 더해지는 3' 으로 나눠 볼 수 있어요.",
      f"이런 시스템을 {K('incl')}이라고 해요."),
 ],
 "pass2": [
  compare("두 조각으로 나누기", ["조각", "식", "이름"],
      ["선형 부분", "$x[n]\\rightarrow2x[n]$", "선형 시스템(Linear system)"],
      ["늘 더해지는 부분", "$y_0[n]=3$", f"{K('zir')}(Zero-input response)"],
      ["합친 것", "$y[n]=2x[n]+3$", f"{K('incl')}"]),
  points(f"{K('zir')}이란",
      "입력을 0으로 넣었을 때 나오는 출력이에요.",
      "$y[n]=2\\times0+3=3$, 그래서 $y_0[n]=3$.",
      "선형 시스템이라면 영입력 응답은 0이어야 해요."),
  check("$y[n]=2x[n]+3$ 의 영입력 응답은?", ["0", "2", "3"], 2,
      "입력 0을 넣으면 3이 나와요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (200, 210, 360, 240, "교재 Example 1.20."),
      (200, 245, 1190, 320, "$y[n]=2x[n]+3$ 은 선형 시스템 $x\\rightarrow2x$ 와 3의 합(두 시스템의 중첩)."),
      (170, 335, 870, 380, f"증분 선형 시스템, {K('zir')} $y_0[n]=3$."),
      (70, 405, 700, 625, "Figure 1.48: 선형 시스템 출력에 $y_0$ 를 더하는 구조."),
      (740, 560, 1295, 635, "두 입력에 대한 출력의 차이는 선형이에요.")),
  steps("차이는 선형 ($x_1=1$, $x_2=4$)",
      [r"$y_1=2\times1+3=5$, $y_2=2\times4+3=11$",
       r"출력 차이 $11-5=6$",
       r"입력 차이 $4-1=3$, 2배 하면 6",
       r"식으로: $y_1-y_2=2x_1+3-(2x_2+3)=2(x_1-x_2)$. 3이 지워져요."],
      "출력의 차이는 입력의 차이에 대해 선형이에요. 그래서 '증분' 선형."),
  prof(W2, "영입력(제로 인풋)으로 3이 붙는 이 시스템을 인크리멘탈 리니어 시스템이라고 부른다고 했어요.",
      "3 만 아니었으면 리니어 시스템이고, 두 입력에 대한 응답의 차이는 리니어하다고 했어요.",
      "집에서 곰곰이 생각해 보면 무슨 말인지 알 거라고 했어요."),
 ],
 "pass4": [
  check("증분 선형 시스템 $y[n]=2x[n]+3$ 은 선형인가요?", ["선형이다", "선형이 아니다"], 1,
      "이름에 '선형' 이 들어가도 그 자체는 선형이 아니에요. 0 입력에 3이 나와요."),
  compare("여섯 성질 한눈에 정리(1장 예제들)", ["시스템", "기억", "인과", "안정", "시불변", "선형"],
      ["$y[n]=x[n-1]$ 지연", "있음", "O", "O", "O", "O"],
      ["누산기", "있음", "O", "X", "O", "O"],
      ["$y[n]=n\\,x[n]$", "없음", "O", "X", "X", "O"],
      ["$y(t)=x(2t)$", "있음", "X", "O", "X", "O"],
      ["$y=3x+2$", "없음", "O", "O", "O", "X"],
      ["$y[n]=x[-n]$", "있음", "X", "O", "X", "O"]),
  exam("성질 판정 연습 (1장 범위)", "Check memory, causality, stability, time invariance and linearity of y[n] = x[-n].",
      f"$y[n]=x[-n]$ ({K('rev')})의 성질을 모두 판정하세요.",
      [r"기억/인과: $n=-1$ 이면 $y[-1]=x[1]$, 미래 입력 → 비인과. $n=1$ 이면 $y[1]=x[-1]$, 과거 → 기억 있음.",
       r"안정: $|x|<U$ 이면 $|y|<U$ → 안정.",
       r"시불변: 밀고 넣기 $x[-n-n_0]$, 넣고 밀기 $y[n-n_0]=x[-n+n_0]$ → 다름 → 시변.",
       r"선형: $ax_1[-n]+bx_2[-n]=ay_1+by_2$ → 선형.",
       r"가역: 한 번 더 뒤집으면 원래 → 가역."],
      "기억 있음, 비인과, 안정, 시변, 선형, 가역"),
  warn("시험 함정",
      f"{K('rev')} $y[n]=x[-n]$ 은 $n\\ge0$ 만 보면 과거만 쓰는 것 같아 인과라고 착각해요. 음수 n 에서 미래를 봐요.",
      "$y(t)=x(2t)$ 도 $t>0$ 이면 $x(2t)$ 가 미래라 비인과, 그리고 시불변이 아니에요."),
 ]})

# ---------------- p.86 과제 1.21, 1.22 ----------------
S.append({"p": 86, "title": "1장 과제: 변환된 신호 그리기 (1.21, 1.22)",
 "pass1": [
  say("여기부터 세 쪽은 1장 과제예요. 슬라이드 번호로 84~86번이에요.",
      f"첫 과제는 그래프를 {K('shift')}, {K('rev')}, {K('scale')}해서 다시 그리는 연습이에요.",
      "영상 재생 비유 그대로예요: 늦게 틀기, 거꾸로 틀기, 2배속."),
  figure("원래 신호와 1만큼 늦춘 신호", FIG["hw21"], "x(t-1) 은 모든 꺾인 점이 오른쪽으로 1칸", 1),
 ],
 "pass2": [
  points("원래 신호 읽기 (Figure P1.21, 연속)",
      "$-2<t<-1$: -1 에서 0 으로 올라가는 비스듬한 선($x=t+1$)",
      "$-1<t<0$: 높이 1",
      "$0<t<1$: 높이 2",
      "$1<t<2$: 1 에서 0 으로 내려가는 선($x=2-t$), 나머지 0"),
  points("원래 신호 읽기 (Figure P1.22, 이산)",
      "$x[-4]=-1$, $x[-3]=-\\frac{1}{2}$, $x[-2]=\\frac{1}{2}$",
      "$x[-1]=x[0]=x[1]=x[2]=1$",
      "$x[3]=\\frac{1}{2}$, 나머지는 0"),
  steps("그리는 요령 (괄호 안을 원래 구간에 맞추기)",
      ["원래 신호에서 모양이 바뀌는 구간 끝점을 적어요(-2, -1, 0, 1, 2).",
       "괄호 안 식 = 끝점 으로 두고 t 를 풀어요. 예: $2-t=-2$ 이면 $t=4$.",
       "구간마다 새 t 구간을 구해서 같은 모양(값)을 옮겨 그려요.",
       "뒤집기(-t)가 있으면 순서가 반대로 돼요."],
      "괄호 안을 끝점에 맞추면 헷갈리지 않아요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (110, 220, 480, 620, "Figure P1.21: 연속시간 신호 x(t)."),
      (545, 170, 1255, 270, "문제 1.21: (a)~(f) 여섯 신호 그리기."),
      (545, 270, 1255, 390, "문제 1.22: (a)~(h) 여덟 신호 그리기."),
      (495, 470, 850, 620, "Figure P1.22: 이산시간 신호 x[n].")),
  figure("1.22 (b) 뒤집고 밀기: $x[3-n]$", FIG["hw22"], "위는 x[n], 아래는 x[3-n]. 순서가 거꾸로 되고 오른쪽으로 옮겨져요.", 1),
  steps("1.22 (b) $x[3-n]$ 한 칸씩",
      [r"$n=0$: $x[3]=\frac{1}{2}$",
       r"$n=1,2,3,4$: $x[2], x[1], x[0], x[-1]$ 모두 1",
       r"$n=5$: $x[-2]=\frac{1}{2}$, $n=6$: $x[-3]=-\frac{1}{2}$, $n=7$: $x[-4]=-1$",
       "나머지 n 은 0"],
      r"$x[3-n]$ 은 0~7 에 $\frac{1}{2},1,1,1,1,\frac{1}{2},-\frac{1}{2},-1$."),
  prof(W2, "마지막 3개 슬라이드(84, 85, 86)는 과제라고 했어요.",
      "다음 주 수업 시작 전까지 풀어서 제출하라고 했고, 목적은 이해했는지 보려는 것이라고 했어요."),
 ],
 "pass4": [
  exam("1장 과제 1.21 (a)(b) (p.86)", "Sketch x(t-1) and x(2-t).",
      "x(t-1) 과 x(2-t) 를 그리세요.",
      [r"(a) 오른쪽으로 1: $-1<t<0$ 에서 -1→0 선($x=t$), $0<t<1$ 에서 1, $1<t<2$ 에서 2, $2<t<3$ 에서 1→0 선($3-t$).",
       r"(b) $x(2-t)=x(-(t-2))$: 뒤집고 오른쪽으로 2.",
       r"(b) 구간: $0<t<1$ 에서 0→1 선($x=t$), $1<t<2$ 에서 2, $2<t<3$ 에서 1, $3<t<4$ 에서 0→-1 선($3-t$)."],
      "(a) -1~3 에 걸친 원래 모양, (b) 0~4 에 걸친 거꾸로 모양"),
  exam("1장 과제 1.21 (c)(d) (p.86)", "Sketch x(2t+1) and x(4 - t/2).",
      "x(2t+1) 과 x(4 - t/2) 를 그리세요.",
      [r"(c) $2t+1$ 을 끝점 -2, -1, 0, 1, 2 에 맞추면 $t=-1.5, -1, -0.5, 0, 0.5$.",
       r"(c) $-1.5<t<-1$: -1→0 선, $-1<t<-0.5$: 1, $-0.5<t<0$: 2, $0<t<0.5$: 1→0 선.",
       r"(d) $4-t/2$ 를 끝점에 맞추면 $t=12, 10, 8, 6, 4$ (순서가 뒤집혀요).",
       r"(d) $4<t<6$: 0→1 선, $6<t<8$: 2, $8<t<10$: 1, $10<t<12$: 0→-1 선."],
      "(c) 폭 절반, -1.5~0.5 / (d) 뒤집고 폭 2배, 4~12"),
  exam("1장 과제 1.21 (e)(f) (p.86)", "Sketch [x(t) + x(-t)]u(t) and x(t)[δ(t + 3/2) - δ(t - 3/2)].",
      "(e) 와 (f) 를 그리세요.",
      [r"(e) $t>0$ 만 남겨요. $0<t<1$: $x(t)=2$, $x(-t)=1$, 합 3.",
       r"(e) $1<t<2$: $(2-t)+(1-t)=3-2t$, 1에서 -1 로 내려가는 선. $t>2$ 는 0.",
       r"(f) 임펄스 자리의 x 값만 남아요: $x(-\frac{3}{2})=-\frac{1}{2}$, $x(\frac{3}{2})=\frac{1}{2}$.",
       r"(f) $-\frac{1}{2}\delta(t+\frac{3}{2})-\frac{1}{2}\delta(t-\frac{3}{2})$"],
      "(e) 0~1 에서 3, 1~2 에서 3-2t / (f) ±3/2 에 크기 -1/2 임펄스 두 개"),
  exam("1장 과제 1.22 (a)(c)(d) (p.86)", "Sketch x[n-4], x[3n], x[3n+1].",
      "x[n-4], x[3n], x[3n+1] 을 그리세요.",
      [r"(a) 오른쪽으로 4칸: $n=0$ 부터 $-1, -\frac{1}{2}, \frac{1}{2}, 1, 1, 1, 1, \frac{1}{2}$ ($n=7$ 까지).",
       r"(c) $x[3n]$: $n=-1$ 이면 $x[-3]=-\frac{1}{2}$, $n=0$ 이면 1, $n=1$ 이면 $x[3]=\frac{1}{2}$. 나머지 0.",
       r"(d) $x[3n+1]$: $n=-1$ 이면 $x[-2]=\frac{1}{2}$, $n=0$ 이면 $x[1]=1$, $n=1$ 이면 $x[4]=0$."],
      "(c) 세 칸마다 하나씩만 뽑혀요(나머지는 버려짐)"),
  exam("1장 과제 1.22 (e)(f)(g)(h) (p.86)", "Sketch x[n]u[3-n], x[n-2]δ[n-2], (1/2)x[n]+(1/2)(-1)^n x[n], x[(n-1)^2].",
      "나머지 네 신호를 그리세요.",
      [r"(e) $u[3-n]$ 은 $n\le3$ 에서 1. x 는 원래 $n\le3$ 에만 값이 있어서 그대로 $x[n]$.",
       r"(f) $n=2$ 에서만 남아요: $x[0]\delta[n-2]=\delta[n-2]$.",
       r"(g) n 이 짝수면 $\frac{1}{2}x+\frac{1}{2}x=x$, 홀수면 0. 남는 것: $n=-4$: -1, $n=-2$: $\frac{1}{2}$, $n=0$: 1, $n=2$: 1.",
       r"(h) $n=1$ 이면 $x[0]=1$, $n=0,2$ 이면 $x[1]=1$, $n=-1,3$ 이면 $x[4]=0$. 그래서 $n=0,1,2$ 에서 1."],
      "(e) x[n], (f) δ[n-2], (g) 짝수 칸만, (h) n=0,1,2 에서 1"),
  warn("헷갈리기 쉬운 점",
      r"$x(2-t)$ 를 '왼쪽으로 2' 라고 하면 틀려요. $x(-(t-2))$ 로 보고 뒤집은 뒤 오른쪽으로 2.",
      r"$x[3n]$ 처럼 이산시간 압축은 버려지는 칸이 있어요. 연속시간처럼 모양이 그대로 줄지 않아요.",
      r"$x(4-t/2)$ 는 순서 주의: 먼저 $x(-(t-8)/2)$ 로 바꿔 보면 뒤집고, 2배로 늘리고, 오른쪽으로 8이에요."),
 ]})

# ---------------- p.87 과제 1.25 주기 ----------------
S.append({"p": 87, "title": "1장 과제: 주기성 (1.25)",
 "pass1": [
  say(f"두 번째 과제는 신호가 {K('per')}인지, 그렇다면 {K('fp')}가 얼마인지 구하는 거예요.",
      "매일 같은 시간표가 반복되는 하루처럼, 몇 초마다 똑같이 반복되는지 찾아요.",
      "X 표시된 (d)(e)(f) 는 이번 과제에서 빠진 문제예요."),
 ],
 "pass2": [
  formula("이번 주 도구", r"T_0=\frac{2\pi}{|\omega_0|}",
      [(r"\omega_0", K('omega') + r": cos 이나 $e^{j\omega_0 t}$ 에서 t 앞에 곱해진 수"),
       (r"2\pi", "한 바퀴(라디안)"), (r"T_0", f"{K('fp')}: 한 바퀴 도는 데 걸리는 시간")],
      "t 앞의 수를 찾아서 2파이를 그 수로 나누면 기본 주기예요."),
  points("슬라이드 힌트",
      "(a) $T=2\\pi/4$",
      f"(b) {K('cexp')}: 연속시간에서는 늘 주기적",
      "(c) cos 을 먼저 제곱해서 정리하기"),
  check("$\\cos(4t)$ 의 기본 주기는?", ["$\\pi/4$", "$\\pi/2$", "$2\\pi$"], 1,
      f"$2\\pi/4=\\pi/2$ 예요. {K('per')}의 기본 주기는 2파이를 {K('omega')}로 나눠요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (215, 255, 1225, 330, "문제 1.25: 연속시간 신호가 주기적인지, 그렇다면 기본 주기를 구하기."),
      (215, 322, 640, 400, "(a) $3\\cos(4t+\\frac{\\pi}{3})$, (c) cos 제곱."),
      (640, 310, 1000, 352, "(b) $e^{j(\\pi t-1)}$."),
      (285, 355, 1060, 460, "빨간 X: (d)(e)(f) 는 이번 과제에서 제외."),
      (85, 560, 1250, 640, "힌트와 이번 주 도구: 오메가0 → 2파이/오메가0, 가장 작은 공통 주기 확인.")),
  steps("(a) $x(t)=3\\cos(4t+\\frac{\\pi}{3})$",
      [K('omega') + r" $\omega_0=4$ 예요(t 앞의 수). 앞의 3(진폭)과 $\frac{\pi}{3}$(위상)은 주기와 상관없어요.",
       r"$T_0=\frac{2\pi}{4}=\frac{\pi}{2}\approx1.5708$",
       r"Python 확인: $\frac{\pi}{2}$ 뒤 값이 같고, $\frac{\pi}{4}$ 뒤는 달라요."],
      r"주기적, $T_0=\frac{\pi}{2}$"),
  steps("(b) $x(t)=e^{j(\\pi t-1)}$",
      [r"$e^{j(\pi t-1)}=e^{-j}\,e^{j\pi t}$ 예요. $e^{-j}$ 는 고정된 수라 모양에 영향 없음.",
       r"$\omega_0=\pi$ 라서 $T_0=\frac{2\pi}{\pi}=2$",
       f"{K('euler')}로 보면 $\\cos(\\pi t-1)+j\\sin(\\pi t-1)$, 둘 다 주기 2예요."],
      f"주기적, $T_0=2$. {K('cexp')}는 연속시간에서 늘 주기적이에요."),
  steps("(c) $x(t)=[\\cos(2t-\\frac{\\pi}{3})]^2$",
      [r"공식 $\cos^2\theta=\frac{1+\cos2\theta}{2}$ 를 써요.",
       r"$x(t)=\frac{1}{2}+\frac{1}{2}\cos(4t-\frac{2\pi}{3})$",
       r"이제 $\omega_0=4$ 라서 $T_0=\frac{2\pi}{4}=\frac{\pi}{2}$",
       r"원래 cos 의 주기 $\pi$ 가 아니라 절반인 $\frac{\pi}{2}$ 예요. 제곱하면 음수 부분이 양수로 뒤집혀 두 배 자주 반복돼요."],
      r"주기적, $T_0=\frac{\pi}{2}$"),
  bg("기초 다지기 b-3 각도, 라디안, 사인과 코사인",
      "cos 은 $2\\pi$ (한 바퀴)마다 같은 값을 반복해요.",
      "$\\cos(4t)$ 는 t 가 $\\frac{\\pi}{2}$ 만 가도 안쪽이 $2\\pi$ 가 돼서 한 바퀴를 돌아요."),
 ],
 "pass4": [
  exam("1장 과제 1.25 (a) (p.87)", "Is x(t) = 3cos(4t + π/3) periodic? If so, find its fundamental period.",
      "3cos(4t+π/3) 의 기본 주기를 구하세요.",
      [r"$\omega_0=4$", r"$T_0=2\pi/4=\pi/2$", "진폭 3, 위상 π/3 은 주기에 영향 없음"],
      "주기적, 기본 주기 π/2"),
  exam("1장 과제 1.25 (b) (p.87)", "Is x(t) = e^{j(πt - 1)} periodic? If so, find its fundamental period.",
      "e^{j(πt-1)} 의 기본 주기를 구하세요.",
      [r"$e^{j(\pi t-1)}=e^{-j}e^{j\pi t}$", r"$\omega_0=\pi$", r"$T_0=2\pi/\pi=2$",
       f"{K('cexp')}는 연속시간에서 늘 주기적(ω0 가 0이 아니면)", f"{K('euler')}로 풀면 cos 과 sin 의 합, 둘 다 주기 2"],
      "주기적, 기본 주기 2"),
  exam("1장 과제 1.25 (c) (p.87)", "Is x(t) = [cos(2t - π/3)]^2 periodic? If so, find its fundamental period.",
      "cos 제곱 신호의 기본 주기를 구하세요.",
      [r"$\cos^2\theta=\frac{1+\cos2\theta}{2}$", r"$x(t)=\frac{1}{2}+\frac{1}{2}\cos(4t-\frac{2\pi}{3})$",
       r"상수 $\frac{1}{2}$ 는 주기에 영향 없음", r"$T_0=2\pi/4=\pi/2$"],
      "주기적, 기본 주기 π/2"),
  warn("헷갈리기 쉬운 점",
      r"(c) 를 $\cos(2t)$ 만 보고 주기 $\pi$ 라고 쓰면 틀려요. 제곱하면 주기가 절반($\frac{\pi}{2}$)이 돼요.",
      "기본 주기는 '가장 작은' 양의 주기예요. π 도 반복 주기이긴 하지만 기본 주기는 아니에요.",
      f"(d)(e)(f) 는 슬라이드에서 X 로 지운 문제라 이번 과제 범위가 아니에요. 세 문제 모두 {K('per')}예요."),
 ]})

# ---------------- p.88 과제 1.31 LTI 의 힘 ----------------
S.append({"p": 88, "title": "1장 과제: LTI 의 힘 (1.31)",
 "pass1": [
  say(f"마지막 과제는 {K('lin','과')} {K('ti')}이 왜 강력한지 보여 줘요.",
      "입력 하나에 대한 출력만 알면, 그 입력을 밀고 더해 만든 다른 입력의 출력도 바로 알아요.",
      MANTRA_LTI),
  figure("과제 답 미리 보기", FIG["hw31"], "위: (a) 의 답 y2, 아래: (b) 의 답 y3", 1),
 ],
 "pass2": [
  points("주어진 것 (Figure P1.31)",
      "(a) $x_1(t)$: 0 부터 2 까지 높이 1인 사각형",
      "(b) $y_1(t)$: 0 에서 올라가 $t=1$ 에서 2, $t=2$ 에서 0인 삼각형",
      "(c) $x_2(t)$: 0~2 에서 1, 2~4 에서 -1",
      "(d) $x_3(t)$: -1~0 에서 1, 0~1 에서 2, 1~2 에서 1"),
  analogy("레시피 두 개 합치기", f"{K('lti','은')} 정직한 계산기(선형)이면서 언제 해도 같은 레시피(시불변)예요.",
      ["입력을 밀면 출력도 밀림", f"{K('ti')}"], ["입력을 더하면 출력도 더해짐", f"{K('lin')}"],
      ["x1 의 응답 y1 하나", "다른 입력의 응답을 모두 만드는 재료"]),
  check("$x_2(t)$ 를 $x_1$ 으로 쓰면?", ["$x_1(t)+x_1(t-2)$", "$x_1(t)-x_1(t-2)$", "$2x_1(t)$"], 1,
      "0~2 에서 +1, 2~4 에서 -1 이니 원래 사각형에서 2만큼 민 사각형을 빼요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
      (60, 150, 855, 335, f"문제 1.31 설명: {K('lti')}의 응답 하나를 알면 다른 많은 입력의 응답을 바로 구할 수 있어요."),
      (60, 335, 855, 470, "(a) x2 의 응답, (b) x3 의 응답을 구하고 그리기."),
      (860, 330, 1045, 485, "(a) 입력 x1: 0~2 사각형."),
      (1105, 330, 1310, 485, "(b) 응답 y1: 꼭대기 2인 삼각형."),
      (850, 505, 1045, 665, "(c) 입력 x2."),
      (1105, 505, 1310, 665, "(d) 입력 x3.")),
  steps("(a) $x_2$ 의 응답",
      [r"$x_2(t)=x_1(t)-x_1(t-2)$ (확인: 0~2 는 1, 2~4 는 $0-1=-1$)",
       r"시불변: $x_1(t-2)$ 의 응답은 $y_1(t-2)$",
       r"선형: $y_2(t)=y_1(t)-y_1(t-2)$",
       r"$y_1$: 0→(1, 2)→2 에서 0인 삼각형. $y_1(t-2)$: 2→(3, 2)→4 인 삼각형.",
       r"그래서 $y_2$: $t=1$ 에서 2, $t=2$ 에서 0, $t=3$ 에서 -2, $t=4$ 에서 0."],
      "위로 뾰족한 삼각형(0~2) 다음 아래로 뾰족한 삼각형(2~4)"),
  steps("(b) $x_3$ 의 응답",
      [r"$x_3(t)=x_1(t)+x_1(t+1)$ (확인: -1~0 은 1, 0~1 은 $1+1=2$, 1~2 는 1)",
       r"$y_3(t)=y_1(t)+y_1(t+1)$, $y_1(t+1)$ 은 -1~1 삼각형(꼭대기 $t=0$ 에서 2)",
       r"$t=-1$: 0, $t=-0.5$: $1+0=1$, $t=0$: $2+0=2$",
       r"$t=0.5$: $1+1=2$, $t=1$: $0+2=2$, $t=1.5$: 1, $t=2$: 0"],
      "-1 에서 올라가 0~1 은 높이 2로 평평, 2에서 0이 되는 사다리꼴"),
  prof(W2, "우리가 앞으로 다룰 것은 리니어이면서 타임 인베리언트인 LTI 시스템이라고 했어요."),
  prof(W3, "3주차부터 2장에서 LTI 시스템을 다룬다고 했어요. 이 과제가 그 예고편이에요."),
 ],
 "pass4": [
  exam("1장 과제 1.31 (a) (p.88)", "An LTI system maps x1(t) to y1(t). Find and sketch the response to x2(t).",
      "x1 → y1 인 LTI 시스템에 x2 를 넣은 출력을 구하세요.",
      [r"$x_2(t)=x_1(t)-x_1(t-2)$", r"선형 + 시불변 → $y_2(t)=y_1(t)-y_1(t-2)$",
       r"꼭짓점: $(0,0),(1,2),(2,0),(3,-2),(4,0)$"],
      "y2(t) = y1(t) - y1(t-2): 0~2 위 삼각형, 2~4 아래 삼각형"),
  exam("1장 과제 1.31 (b) (p.88)", "Find and sketch the response of the same system to x3(t).",
      "같은 시스템에 x3 를 넣은 출력을 구하세요.",
      [r"$x_3(t)=x_1(t)+x_1(t+1)$", r"$y_3(t)=y_1(t)+y_1(t+1)$",
       r"꼭짓점: $(-1,0),(0,2),(1,2),(2,0)$"],
      "y3(t) = y1(t) + y1(t+1): -1~2 에 걸친 사다리꼴, 0~1 에서 높이 2"),
  warn("헷갈리기 쉬운 점",
      r"$x_1(t+1)$ 은 왼쪽으로 1이에요(더하기는 왼쪽). 그래서 응답도 $y_1(t+1)$, 왼쪽으로 1.",
      "선형만 있고 시불변이 없으면 $x_1(t-2)$ 의 응답을 $y_1(t-2)$ 로 쓸 수 없어요. 두 성질이 모두 필요해요."),
  english("답안 문장",
      "LTI 시스템에서는 입력을 x1 의 이동과 상수배의 합으로 나타내면, 출력도 y1 을 똑같이 이동하고 상수배하여 더한 것이 된다.",
      "선형 → 더하기, 곱하기 유지. 시불변 → 밀기 유지.",
      "입력을 조각내듯 출력도 조각낸다"),
 ]})

build(OUT, "S2", 61, 88, S)
