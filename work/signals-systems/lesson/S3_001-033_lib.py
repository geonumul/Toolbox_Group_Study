# -*- coding: utf-8 -*-
# S3 1~33쪽 회독 레슨 도우미 (build_S3_001-033.py 가 가져다 쓴다)
import json, math, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
DICT = json.load(open(os.path.join(HERE, "..", "rules", "용어사전.json"), encoding="utf-8"))

# ---------------- 용어 ----------------
TERMS = {
    "signal": ("신호", "Signal"), "system": ("시스템", "System"),
    "dt": ("이산시간 신호", "Discrete-Time Signal"), "ct": ("연속시간 신호", "Continuous-Time Signal"),
    "realexp": ("실수 지수 신호", "Real Exponential Signal"), "cexp": ("복소 지수 신호", "Complex Exponential Signal"),
    "euler": ("오일러 공식", "Euler's Formula"), "ucircle": ("단위원", "Unit Circle"),
    "imag": ("허수 단위", "Imaginary Unit"), "cplane": ("복소평면", "Complex Plane"),
    "rc": ("RC 회로", "RC Circuit"), "de": ("미분방정식", "Differential Equation"),
    "dfe": ("차분방정식", "Difference Equation"), "ifac": ("적분 인자", "Integrating Factor"),
    "periodic": ("주기 신호", "Periodic Signal"), "fper": ("기본 주기", "Fundamental Period"),
    "angf": ("각주파수", "Angular Frequency"), "impulse": ("단위 임펄스", "Unit Impulse"),
    "step": ("단위 계단", "Unit Step"), "fdiff": ("1차 차분", "First Difference"),
    "rsum": ("누적 합", "Running Sum"), "sift": ("선별 성질", "Sifting Property"),
    "lti": ("LTI 시스템", "Linear Time-Invariant System"), "lin": ("선형성", "Linearity"),
    "ti": ("시불변성", "Time Invariance"), "sup": ("중첩 원리", "Superposition"),
    "add": ("가산성", "Additivity"), "hom": ("동차성", "Homogeneity"),
    "ir": ("임펄스 응답", "Impulse Response"), "conv": ("컨볼루션", "Convolution"),
    "csum": ("컨볼루션 합", "Convolution Sum"), "cint": ("컨볼루션 적분", "Convolution Integral"),
    "tshift": ("시간 이동", "Time Shift"), "trev": ("시간 반전", "Time Reversal"),
    "causal": ("인과성", "Causality"), "stab": ("안정성", "Stability"),
    "geo": ("등비급수", "Geometric Series"), "sigma": ("시그마 기호", "Summation"),
    "integral": ("적분", "Integral"), "deriv": ("미분", "Derivative"),
    "stepr": ("계단 응답", "Step Response"), "filter": ("필터", "Filter"),
}
NEW_TERMS = {"ifac": {"ko": "적분 인자", "en": "Integrating Factor",
    "say": "1차 선형 미분방정식 양변에 곱해서 왼쪽을 한 덩어리의 미분으로 만들어 주는 식",
    "more": "y' + p y = q 에 u = e^(∫p dx) 를 곱하면 (u y)' = u q 가 돼서 적분 한 번으로 풀려요. 3주차 복습용이고 퀴즈, 시험에는 안 나와요."}}

JOSA = {"은": ("은", "는"), "이": ("이", "가"), "을": ("을", "를"), "과": ("과", "와"),
        "으로": ("으로", "로"), "이라고": ("이라고", "라고"), "이에요": ("이에요", "예요"),
        "이고": ("이고", "고"), "이라서": ("이라서", "라서"), "이나": ("이나", "나"), "이죠": ("이죠", "죠")}


def _fin(key):
    ko, en = TERMS[key]
    c = (ko or en)[-1]
    if "가" <= c <= "힣":
        j = (ord(c) - 0xAC00) % 28
        return 0 if j == 0 else (2 if j == 8 else 1)
    return 0


def disp(key):
    ko, en = TERMS[key]
    return f"**{ko}({en})**"


def K(key, josa=""):
    s = disp(key)
    if not josa:
        return s
    if josa in JOSA:
        f = _fin(key)
        if josa == "으로":
            return s + ("으로" if f == 1 else "로")
        return s + (JOSA[josa][0] if f >= 1 else JOSA[josa][1])
    return s + josa


TOK = re.compile(r"@(\w+)(?:\|([^@]*))?@")


def tr(o, key=None):
    if isinstance(o, str):
        if key in ("svg", "tex", "sym"):
            return o
        return TOK.sub(lambda m: K(m.group(1), m.group(2) or ""), o)
    if isinstance(o, list):
        return [tr(x, key) for x in o]
    if isinstance(o, dict):
        return {k: tr(v, k) for k, v in o.items()}
    return o


M1 = "주문: 신호는 시간에 따라 변하는 값, 시스템은 신호를 바꾸는 상자."
M2a = "주문: LTI 시스템은 임펄스 응답 하나만 알면 된다."
M2b = "출력은 뒤집고, 밀고, 곱하고, 더해서(컨볼루션) 구한다."
WHEN = "3주차 목요일 수업"


# ---------------- 장면 ----------------
def say(*l): return {"kind": "say", "lines": list(l)}
def points(h, *i): return {"kind": "points", "head": h, "items": list(i)}
def analogy(h, scene, *pairs): return {"kind": "analogy", "head": h, "scene": scene, "map": [list(p) for p in pairs]}


def compare(h, cols, *rows):
    for r in rows:
        assert len(r) == len(cols), r
    return {"kind": "compare", "head": h, "cols": list(cols), "rows": [list(r) for r in rows]}


def formula(h, tex, parts, whole):
    return {"kind": "formula", "head": h, "tex": tex, "parts": [{"sym": s, "say": t} for s, t in parts], "whole": whole}


def steps(h, st, ans, given=None):
    d = {"kind": "steps", "head": h}
    if given:
        d["given"] = given
    d["steps"] = list(st)
    d["answer"] = ans
    return d


def figure(h, svg, cap):
    mb = max([int(x) for x in re.findall(r"\bb(\d)\b", svg)] or [1])
    return {"kind": "figure", "head": h, "svg": svg, "caption": cap, "builds": mb}


def check(q, ch, a, why): return {"kind": "check", "q": q, "choices": list(ch), "a": a, "why": why}
def warn(h, *i): return {"kind": "warn", "head": h, "items": list(i)}
def exam(src, q, qko, solve, ans): return {"kind": "exam", "src": src, "q": q, "qko": qko, "solve": list(solve), "answer": ans}


def english(h, en, ko, tip=None):
    d = {"kind": "english", "head": h, "en": en, "ko": ko}
    if tip:
        d["tip"] = tip
    return d


def bg(src, *l): return {"kind": "bg", "src": src, "lines": list(l)}
def prof(*l): return {"kind": "prof", "when": WHEN, "lines": list(l)}
def recap(*i): return {"kind": "recap", "items": list(i)}


PW, PH = 1400, 788


def look(h, *boxes):
    """boxes: (x, y, w, h, 설명) 비율 또는 ('px', x1, y1, x2, y2, 설명) 1400x788 픽셀"""
    out = []
    for b in boxes:
        if b[0] == "px":
            _, x1, y1, x2, y2, s = b
            b = (x1 / PW, y1 / PH, (x2 - x1) / PW, (y2 - y1) / PH, s)
        x, y, w, hh, s = b
        out.append({"x": round(x, 3), "y": round(y, 3), "w": round(w, 3), "h": round(hh, 3), "say": s})
    return {"kind": "look", "head": h, "boxes": out}


# ---------------- SVG ----------------
def _b(b): return f" b{b}" if b else ""


def TX(x, y, s, cls="t", fs=15, anc="middle", b=0):
    s = str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f'<text x="{x:.0f}" y="{y:.0f}" font-size="{fs}" text-anchor="{anc}" class="{cls}{_b(b)}">{s}</text>'


def R(x, y, w, h, cls="box", b=0, rx=2):
    return f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{rx}" class="{cls}{_b(b)}"/>'


def C(x, y, r, cls="n", b=0): return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" class="{cls}{_b(b)}"/>'
def L(x1, y1, x2, y2, cls="e", b=0): return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="{cls}{_b(b)}"/>'


def A(x1, y1, x2, y2, cls="e2", b=0):
    ang = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 - 9 * math.cos(ang), y2 - 9 * math.sin(ang)
    px, py = -math.sin(ang) * 5, math.cos(ang) * 5
    return L(x1, y1, hx, hy, cls, b) + f'<polygon points="{x2:.0f},{y2:.0f} {hx + px:.0f},{hy + py:.0f} {hx - px:.0f},{hy - py:.0f}" class="arrow{_b(b)}"/>'


def PL(pts, cls="e2", b=0):
    return f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" class="{cls}{_b(b)}"/>'


def BOX(x, y, w, h, label, cls="box", tcls="tb", b=0, fs=15):
    return R(x, y, w, h, cls, b) + TX(x + w / 2, y + h / 2 + fs // 3 + 1, label, tcls, fs, "middle", b)


def SVG(*parts, h=270): return f'<svg viewBox="0 0 480 {h}" xmlns="http://www.w3.org/2000/svg">' + "".join(parts) + "</svg>"


def fmtv(v):
    if abs(v - round(v)) < 1e-9:
        return str(int(round(v)))
    return f"{v:g}"


def STEM(ox, oy, dx, sc, ns, vals, b=0, cls="e2", dot="n2", vlab=True, nlab=True, labs=None):
    """ns: n 목록(연속 정수), vals: 값. ox 는 ns[0] 의 x 좌표."""
    P = []
    X = lambda n: ox + (n - ns[0]) * dx
    P.append(L(X(ns[0]) - dx * 0.6, oy, X(ns[-1]) + dx * 0.6, oy, "e", b))
    for i, (n, v) in enumerate(zip(ns, vals)):
        x = X(n)
        y = oy - v * sc
        if abs(v) > 1e-12:
            P.append(L(x, oy, x, y, cls, b))
            P.append(C(x, y, 4, dot, b))
            if vlab:
                lab = labs[i] if labs else fmtv(v)
                if lab:
                    P.append(TX(x, y - 7 if v > 0 else y + 17, lab, "tb", 14, "middle", b))
        else:
            P.append(C(x, oy, 3, "n", b))
        if nlab:
            P.append(TX(x, oy + 17 if v >= 0 else oy - 7, fmtv(n), "tm", 14, "middle", b))
    return "".join(P)


def conv(x, h):
    """x, h: dict n->v"""
    y = {}
    for k, xv in x.items():
        for m, hv in h.items():
            y[k + m] = y.get(k + m, 0) + xv * hv
    return y


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


def gloss_entry(key):
    if key in NEW_TERMS:
        return NEW_TERMS[key]
    ko, en = TERMS[key]
    for d in DICT:
        if d.get("ko") == ko and d.get("en") == en:
            g = {"ko": ko, "en": en, "say": d["say"]}
            if d.get("more"):
                g["more"] = d["more"]
            return g
    raise KeyError(f"용어 사전에 없음: {key}")


def build(path, deck, lo, hi, slides):
    slides = [tr(s) for s in slides]
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
    left = TOK.findall(raw)
    assert not [t for t in left if t[0] in TERMS], left
    with open(path, "w", encoding="utf-8") as fp:
        fp.write(raw)
    print(f"저장 {path}: 쪽 {len(slides)}, 용어 {len(gl_keys)}")
    return out
