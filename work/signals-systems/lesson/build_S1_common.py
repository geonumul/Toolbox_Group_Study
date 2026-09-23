# S1(1주차 OT) 회독 레슨 도우미 (build_S1_common.py): 용어 표기, 조사, 장면, SVG, 저장
# build_S1_001-028.py 가 가져다 쓴다.
import json, math, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
DICT = json.load(open(os.path.join(HERE, "..", "rules", "용어사전.json"), encoding="utf-8"))

MANTRA = "신호는 시간에 따라 변하는 값, 시스템은 신호를 바꾸는 상자."
MANTRA_LTI = ("LTI 시스템은 임펄스 응답 하나만 알면 된다. "
              "출력은 뒤집고, 밀고, 곱하고, 더해서(컨볼루션) 구한다.")

# key: (ko, en)
TERMS = {
    "signal": ("신호", "Signal"),
    "system": ("시스템", "System"),
    "indep": ("독립 변수", "Independent Variable"),
    "ct": ("연속시간 신호", "Continuous-Time Signal"),
    "dt": ("이산시간 신호", "Discrete-Time Signal"),
    "analog": ("아날로그 신호", "Analog Signal"),
    "digital": ("디지털 신호", "Digital Signal"),
    "sampling": ("샘플링", "Sampling"),
    "quant": ("양자화", "Quantization"),
    "coding": ("부호화", "Coding"),
    "samthm": ("샘플링 정리", "Sampling Theorem"),
    "fourier": ("푸리에 해석", "Fourier Analysis"),
    "fs": ("푸리에 급수", "Fourier Series"),
    "ft": ("푸리에 변환", "Fourier Transform"),
    "tdom": ("시간 영역", "Time Domain"),
    "fdom": ("주파수 영역", "Frequency Domain"),
    "filter": ("필터", "Filter"),
    "noise": ("잡음", "Noise"),
    "spectro": ("스펙트로그램", "Spectrogram"),
    "input": ("입력 신호", "Input Signal"),
    "output": ("출력 신호", "Output Signal"),
    "diffeq": ("미분방정식", "Differential Equation"),
    "diffce": ("차분방정식", "Difference Equation"),
    "rc": ("RC 회로", "RC Circuit"),
    "order": ("시스템 차수", "Order"),
    "lti": ("LTI 시스템", "Linear Time-Invariant System"),
    "lin": ("선형성", "Linearity"),
    "ti": ("시불변성", "Time Invariance"),
    "conv": ("컨볼루션", "Convolution"),
    "cnn": ("합성곱 신경망", "Convolutional Neural Network"),
    "euler": ("오일러 공식", "Euler's Formula"),
    "complex": ("복소수", "Complex Number"),
    "imag": ("허수 단위", "Imaginary Unit"),
    "sinus": ("사인파 신호", "Sinusoidal Signal"),
    "freq": ("주파수", "Frequency"),
    "series": ("직렬 연결", "Series Interconnection"),
    "mod": ("변조", "Modulation"),
    "demod": ("복조", "Demodulation"),
    "channel": ("채널", "Channel"),
    "impulse": ("단위 임펄스", "Unit Impulse"),
    "step": ("단위 계단", "Unit Step"),
    "deriv": ("미분", "Derivative"),
    "integ": ("적분", "Integral"),
    "expf": ("지수함수", "Exponential Function"),
    "shift": ("시간 이동", "Time Shift"),
    "rev": ("시간 반전", "Time Reversal"),
    "scale": ("시간 척도 변환", "Time Scaling"),
}

# 사전에 없는 새 용어 (보고서에 적는다)
NEW = {
    "fs": ("주기 신호를 여러 사인파의 합으로 나타내는 방법",
           "4~5주차(교재 3장)에 배워요. 반복되는 신호를 기본 주파수의 정수배 사인파들로 쪼개요."),
    "ft": ("주기가 없는 신호까지 여러 주파수의 사인파로 쪼개 보는 방법",
           "6~10주차(교재 4장, 5장)에 연속시간(CTFT), 이산시간(DTFT) 두 가지를 배워요."),
    "tdom": ("가로축을 시간으로 두고 신호를 보는 관점",
             "우리가 흔히 보는 파형 그래프 x(t)가 시간 영역이에요."),
    "fdom": ("신호 안에 어떤 주파수가 얼마나 들어 있는지로 보는 관점",
             "푸리에 변환으로 시간 영역 신호를 이쪽으로 옮겨 와요. 슬라이드에서는 X(ω)로 적어요."),
    "coding": ("양자화한 값을 0과 1의 비트로 바꿔 적는 일",
               "아날로그에서 디지털로 가는 마지막 단계예요. 컴퓨터는 이 비트만 저장해요."),
    "mod": ("보낼 신호를 멀리 보내기 좋은 모양으로 바꾸는 송신기의 일",
            "통신 사슬에서 송신기가 해요. 받는 쪽에서는 복조로 되돌려요."),
    "demod": ("변조된 신호에서 원래 신호를 되찾는 수신기의 일",
              "통신 사슬에서 수신기가 해요. 변조를 되돌리는 일이에요."),
    "channel": ("송신기에서 수신기까지 신호가 지나가는 통로",
                "공기, 전선 같은 길이에요. 통신에서는 여기서 잡음이 끼어들어요."),
    "cnn": ("층마다 컨볼루션 계산을 쓰는 인공신경망, 줄여서 CNN",
            "사진 인식에 많이 쓰여요. 이 과목 3주차에 배우는 컨볼루션이 바로 그 층 안의 계산이에요."),
}

JOSA = {
    "은": ("은", "는"), "이": ("이", "가"), "을": ("을", "를"), "과": ("과", "와"),
    "이에요": ("이에요", "예요"), "이나": ("이나", "나"), "이고": ("이고", "고"),
    "이라고": ("이라고", "라고"), "이라는": ("이라는", "라는"), "이죠": ("이죠", "죠"),
}


def _fin(key):
    ko, en = TERMS[key]
    c = (ko or en)[-1]
    if "가" <= c <= "힣":
        j = (ord(c) - 0xAC00) % 28
        return 0 if j == 0 else (2 if j == 8 else 1)
    raise ValueError(key)


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
        return {"ko": ko, "en": en, "say": NEW[key][0], "more": NEW[key][1]}
    for d in DICT:
        if d.get("ko") == ko and d.get("en") == en:
            g = {"ko": ko, "en": en, "say": d["say"]}
            if d.get("more"):
                g["more"] = d["more"]
            return g
    raise KeyError(f"사전에 없음: {key}")


# ---------------- 장면 ----------------
def say(*lines):
    return {"kind": "say", "lines": list(lines)}


def bx(x, y, w, h, s, pad=0.006):
    """PDF 에서 뽑은 비율 좌표(x, y, w, h)에 조금 여유를 준다."""
    x0, y0 = max(0.0, x - pad), max(0.0, y - pad)
    x1, y1 = min(1.0, x + w + pad), min(1.0, y + h + pad)
    return {"x": round(x0, 3), "y": round(y0, 3), "w": round(x1 - x0, 3), "h": round(y1 - y0, 3), "say": s}


def px(x1, y1, x2, y2, s):
    """1400x990 그림의 픽셀 좌표"""
    return {"x": round(x1 / 1400, 3), "y": round(y1 / 990, 3),
            "w": round((x2 - x1) / 1400, 3), "h": round((y2 - y1) / 990, 3), "say": s}


def look(head, *boxes):
    return {"kind": "look", "head": head, "boxes": list(boxes)}


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
            "parts": [{"sym": a, "say": b} for a, b in parts], "whole": whole}


def figure(head, svg, caption, builds):
    return {"kind": "figure", "head": head, "svg": svg, "caption": caption, "builds": builds}


def check(q, choices, a, why):
    return {"kind": "check", "q": q, "choices": list(choices), "a": a, "why": why}


def warn(head, *items):
    return {"kind": "warn", "head": head, "items": list(items)}


def english(head, en, ko, tip=None):
    d = {"kind": "english", "head": head, "en": en, "ko": ko}
    if tip:
        d["tip"] = tip
    return d


def bg(src, *lines):
    return {"kind": "bg", "src": src, "lines": list(lines)}


def prof(when, *lines):
    return {"kind": "prof", "when": when, "lines": list(lines)}


def exam(src, q, qko, solve, answer):
    return {"kind": "exam", "src": src, "q": q, "qko": qko, "solve": list(solve), "answer": answer}


def recap(*items):
    return {"kind": "recap", "items": list(items)}


# ---------------- SVG ----------------
def _b(b):
    return f" b{b}" if b else ""


def TX(x, y, s, cls="t", fs=15, anc="middle", b=0):
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f'<text x="{x:g}" y="{y:g}" font-size="{fs}" text-anchor="{anc}" class="{cls}{_b(b)}">{s}</text>'


def R(x, y, w, h, cls="box", b=0, rx=2):
    return f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{h:g}" rx="{rx}" class="{cls}{_b(b)}"/>'


def C(x, y, r, cls="n", b=0):
    return f'<circle cx="{x:g}" cy="{y:g}" r="{r:g}" class="{cls}{_b(b)}"/>'


def L(x1, y1, x2, y2, cls="e", b=0):
    return f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" class="{cls}{_b(b)}"/>'


def PL(pts, cls="e2", b=0):
    s = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'<polyline points="{s}" fill="none" class="{cls}{_b(b)}"/>'


def A(x1, y1, x2, y2, cls="e2", b=0):
    ang = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 - 9 * math.cos(ang), y2 - 9 * math.sin(ang)
    qx, qy = -math.sin(ang) * 5, math.cos(ang) * 5
    pts = f"{x2:.0f},{y2:.0f} {hx + qx:.0f},{hy + qy:.0f} {hx - qx:.0f},{hy - qy:.0f}"
    return L(x1, y1, round(hx, 1), round(hy, 1), cls, b) + f'<polygon points="{pts}" class="arrow{_b(b)}"/>'


def BOX(x, y, w, h, label, cls="box", tcls="tb", b=0, fs=15, dy=0):
    return R(x, y, w, h, cls, b) + TX(x + w / 2, y + h / 2 + fs // 3 + 1 + dy, label, tcls, fs, "middle", b)


def STEM(x, y0, y1, cls="e2", dot="n2", b=0, r=3.5):
    return L(x, y0, x, y1, cls, b) + C(x, y1, r, dot, b)


def SVG(*parts, h=270):
    return f'<svg viewBox="0 0 480 {h}" xmlns="http://www.w3.org/2000/svg">' + "".join(parts) + "</svg>"


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


def build(path, deck, lo, hi, slides):
    keys = []
    for s in slides:
        body = " ".join(_text([s.get(f"pass{i}", []) for i in range(1, 5)]))
        terms = []
        for key in TERMS:
            if disp(key) in body:
                terms.append(TERMS[key][1])
                if key not in keys:
                    keys.append(key)
        s["terms"] = terms
    out = {"deck": deck, "from": lo, "to": hi,
           "glossary": [gloss_entry(k) for k in keys],
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
                        if len(re.sub(r"\*\*", "", ln)) > 80:
                            print(f"  긴 줄 p.{s['p']} pass{i}: {ln[:40]}...")
    with open(path, "w", encoding="utf-8") as fp:
        fp.write(raw)
    print(f"저장 {path}: 쪽 {len(slides)}, 용어 {len(keys)}")
    return out
