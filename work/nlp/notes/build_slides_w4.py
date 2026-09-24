# -*- coding: utf-8 -*-
"""4주차 정리 슬라이드 (N4 Attention and the Transformer Architecture) -> slides_w4.json
숫자는 모두 아래에서 실제로 계산하고 assert 로 확인한다."""
import json, math, pathlib

W = pathlib.Path(__file__).resolve().parent

# ---------------------------------------------------------------- 계산 검증
def softmax(xs):
    m = max(xs)
    e = [math.exp(x - m) for x in xs]
    s = sum(e)
    return [v / s for v in e]

# (1) 어텐션 점수 3.6 / 0.8 / 0.5 / 0.4 의 소프트맥스 (N4 p.21, p.23)
SC = [3.6, 0.8, 0.5, 0.4]
AL = softmax(SC)
assert [round(a, 2) for a in AL] == [0.87, 0.05, 0.04, 0.04]

# (2) 가중합으로 문맥 벡터 만들기 (가중치는 N4 p.19 의 0.62 / 0.14 / 0.12 / 0.12)
WTS = [0.62, 0.14, 0.12, 0.12]
HS = [(2.0, 0.0), (0.0, 2.0), (1.0, 1.0), (0.0, 0.0)]
CTX = (sum(w * h[0] for w, h in zip(WTS, HS)), sum(w * h[1] for w, h in zip(WTS, HS)))
assert abs(sum(WTS) - 1.0) < 1e-9 and (round(CTX[0], 2), round(CTX[1], 2)) == (1.36, 0.40)

# (3) 빔 서치 길이 정규화 (N4 p.13 그림의 점수)
B_LONG, B_SHORT = -2.5, -3.5
NL1, NL2 = B_LONG / 3, B_SHORT / 3
assert round(NL1, 3) == -0.833 and round(NL2, 3) == -1.167 and NL1 > NL2
PART2, PART3 = -1.6 / 2, -2.5 / 3
assert round(PART2, 3) == -0.8 and round(PART3, 3) == -0.833

# (4) sqrt(d_k) 스케일링 (N4 p.38)
assert round(math.sqrt(8), 2) == 2.83 and math.sqrt(64) == 8.0 and round(math.sqrt(512), 2) == 22.63
RAW = [24.0, 8.0, 16.0]
SCALED = [r / 8 for r in RAW]
P_RAW, P_SCALED = softmax(RAW), softmax(SCALED)
assert SCALED == [3.0, 1.0, 2.0]
assert round(P_SCALED[0], 3) == 0.665 and round(P_SCALED[1], 3) == 0.090 and round(P_SCALED[2], 3) == 0.245
assert round(P_RAW[0], 4) == 0.9997

# (5) 위치 인코딩 값 (N4 p.40), pos = 1, d = 4
PE10, PE11 = math.sin(1 / 10000 ** (0 / 4)), math.cos(1 / 10000 ** (0 / 4))
PE12, PE13 = math.sin(1 / 10000 ** (2 / 4)), math.cos(1 / 10000 ** (2 / 4))
assert round(PE10, 4) == 0.8415 and round(PE11, 4) == 0.5403
assert round(PE12, 4) == 0.0100 and round(PE13, 5) == 0.99995

# (6) 멀티 헤드와 FFN 파라미터 (N4 p.47, p.42)
D, H = 512, 8
DH = D // H
ATTN_P = 4 * D * D
FFN_P = 2 * D * (4 * D)
assert DH == 64 and ATTN_P == 1048576 and FFN_P == 2097152 and FFN_P // ATTN_P == 2

# (7) 층 정규화 손계산 (N4 p.50)
XS = [1.0, 2.0, 3.0, 4.0]
MU = sum(XS) / len(XS)
VAR = sum((x - MU) ** 2 for x in XS) / len(XS)
SD = math.sqrt(VAR)
LN = [(x - MU) / SD for x in XS]
assert MU == 2.5 and VAR == 1.25 and round(SD, 3) == 1.118
assert [round(v, 3) for v in LN] == [-1.342, -0.447, 0.447, 1.342]

# (8) 이차 비용 (N4 p.55)
N1, N2 = 512, 128000
assert N1 ** 2 == 262144 and N2 ** 2 == 16384000000 and (N2 // N1) ** 2 == 62500

# (9) WMT14 결과 (N4 p.56)
assert round(27.3 - 24.6, 1) == 2.7 and round(96 / 3.3, 1) == 29.1


def T(ko, en, say, more=""):
    d = {"ko": ko, "en": en, "say": say}
    if more:
        d["more"] = more
    return d


def title(big, sub): return {"kind": "title", "big": big, "sub": sub}
def goal(*items): return {"kind": "goal", "items": list(items)}
def pts(head, *items): return {"kind": "points", "head": head, "items": list(items)}
def ana(head, scene, pairs): return {"kind": "analogy", "head": head, "scene": scene, "map": [list(p) for p in pairs]}
def fig(head, svg, caption, builds): return {"kind": "figure", "head": head, "svg": svg, "caption": caption, "builds": builds}
def cmp_(head, cols, rows): return {"kind": "compare", "head": head, "cols": cols, "rows": rows}
def check(q, choices, a, why): return {"kind": "check", "q": q, "choices": choices, "a": a, "why": why}
def warn(head, *items): return {"kind": "warn", "head": head, "items": list(items)}
def recap(*items): return {"kind": "recap", "items": list(items)}


def eng(head, en, ko, tip=None):
    d = {"kind": "english", "head": head, "en": en, "ko": ko}
    if tip:
        d["tip"] = tip
    return d


def steps(head, st, answer, given=None):
    d = {"kind": "steps", "head": head, "steps": st, "answer": answer}
    if given:
        d["given"] = given
    return d


def form(head, tex, parts, whole):
    return {"kind": "formula", "head": head, "tex": tex, "parts": [{"sym": s, "say": t} for s, t in parts], "whole": whole}


S0 = '<svg viewBox="0 0 480 270" xmlns="http://www.w3.org/2000/svg">'

# ---------------------------------------------------------------- 그림
SVG_ENCDEC = (
    S0
    + '<text class="tm b1" x="114" y="46" font-size="14" text-anchor="middle">인코더 Encoder</text>'
    + '<rect class="n b1" x="20" y="80" width="38" height="34"/>'
    + '<rect class="n b1" x="70" y="80" width="38" height="34"/>'
    + '<rect class="n b1" x="120" y="80" width="38" height="34"/>'
    + '<rect class="n b1" x="170" y="80" width="38" height="34"/>'
    + '<line class="e b1" x1="58" y1="97" x2="70" y2="97"/>'
    + '<line class="e b1" x1="108" y1="97" x2="120" y2="97"/>'
    + '<line class="e b1" x1="158" y1="97" x2="170" y2="97"/>'
    + '<text class="tm b1" x="39" y="134" font-size="13" text-anchor="middle">il</text>'
    + '<text class="tm b1" x="89" y="134" font-size="13" text-anchor="middle">a</text>'
    + '<text class="tm b1" x="139" y="134" font-size="13" text-anchor="middle">m</text>'
    + '<text class="tm b1" x="189" y="134" font-size="13" text-anchor="middle">entarte</text>'
    + '<rect class="n2 b2" x="220" y="80" width="42" height="34"/>'
    + '<text class="tl b2" x="241" y="103" font-size="15" text-anchor="middle">h</text>'
    + '<line class="e2 b2" x1="208" y1="97" x2="220" y2="97"/>'
    + '<polygon class="arrow b2" points="220,97 212,92 212,102"/>'
    + '<text class="tm b3" x="376" y="46" font-size="14" text-anchor="middle">디코더 Decoder</text>'
    + '<rect class="n3 b3" x="282" y="80" width="38" height="34"/>'
    + '<rect class="n3 b3" x="332" y="80" width="38" height="34"/>'
    + '<rect class="n3 b3" x="382" y="80" width="38" height="34"/>'
    + '<rect class="n3 b3" x="432" y="80" width="38" height="34"/>'
    + '<line class="e2 b3" x1="262" y1="97" x2="282" y2="97"/>'
    + '<polygon class="arrow b3" points="282,97 274,92 274,102"/>'
    + '<line class="e b3" x1="320" y1="97" x2="332" y2="97"/>'
    + '<line class="e b3" x1="370" y1="97" x2="382" y2="97"/>'
    + '<line class="e b3" x1="420" y1="97" x2="432" y2="97"/>'
    + '<text class="tm b3" x="301" y="70" font-size="13" text-anchor="middle">he</text>'
    + '<text class="tm b3" x="351" y="70" font-size="13" text-anchor="middle">hit</text>'
    + '<text class="tm b3" x="401" y="70" font-size="13" text-anchor="middle">me</text>'
    + '<text class="tm b3" x="451" y="70" font-size="13" text-anchor="middle">pie</text>'
    + '<text class="t b4" x="240" y="180" font-size="15" text-anchor="middle">벡터 하나가 소스 문장 전체를 옮겨요</text>'
    + '<text class="tm b4" x="240" y="212" font-size="14" text-anchor="middle">그 하나가 바로 정보 병목이에요</text>'
    + '</svg>')

SVG_BEAM = (
    S0
    + '<rect class="n b1" x="10" y="120" width="56" height="28"/>'
    + '<text class="tl b1" x="38" y="139" font-size="13" text-anchor="middle">시작 0.0</text>'
    + '<line class="e b1" x1="66" y1="130" x2="96" y2="96"/><line class="e b1" x1="66" y1="138" x2="96" y2="176"/>'
    + '<rect class="n2 b1" x="96" y="76" width="86" height="28"/>'
    + '<text class="tl b1" x="139" y="95" font-size="13" text-anchor="middle">he -0.7</text>'
    + '<rect class="n2 b1" x="96" y="166" width="86" height="28"/>'
    + '<text class="tl b1" x="139" y="185" font-size="13" text-anchor="middle">I -1.3</text>'
    + '<line class="e b2" x1="182" y1="86" x2="212" y2="62"/><line class="e b2" x1="182" y1="96" x2="212" y2="106"/>'
    + '<line class="e b2" x1="182" y1="176" x2="212" y2="166"/><line class="e b2" x1="182" y1="186" x2="212" y2="210"/>'
    + '<rect class="n2 b2" x="212" y="46" width="96" height="28"/>'
    + '<text class="tl b2" x="260" y="65" font-size="13" text-anchor="middle">he hit -1.6</text>'
    + '<rect class="n4 b2" x="212" y="92" width="96" height="28"/>'
    + '<text class="tl b2" x="260" y="111" font-size="13" text-anchor="middle">he struck -2.3</text>'
    + '<rect class="n2 b2" x="212" y="152" width="96" height="28"/>'
    + '<text class="tl b2" x="260" y="171" font-size="13" text-anchor="middle">I was -2.9</text>'
    + '<rect class="n4 b2" x="212" y="196" width="96" height="28"/>'
    + '<text class="tl b2" x="260" y="215" font-size="13" text-anchor="middle">I got -3.6</text>'
    + '<line class="e2 b3" x1="308" y1="60" x2="336" y2="60"/><line class="e2 b3" x1="308" y1="166" x2="336" y2="166"/>'
    + '<rect class="n3 b3" x="336" y="46" width="110" height="28"/>'
    + '<text class="tl b3" x="391" y="65" font-size="13" text-anchor="middle">he hit me -2.5</text>'
    + '<rect class="n3 b3" x="336" y="152" width="110" height="28"/>'
    + '<text class="tl b3" x="391" y="171" font-size="13" text-anchor="middle">I was hit -3.5</text>'
    + '<text class="tm b3" x="240" y="252" font-size="14" text-anchor="middle">빔 크기 k = 2, 점수는 로그 확률의 합, 흐린 상자는 버려진 후보</text>'
    + '</svg>')

SVG_BOTTLE = (
    S0
    + '<text class="tm b1" x="60" y="34" font-size="14" text-anchor="middle">어텐션 없음</text>'
    + '<rect class="n b1" x="20" y="48" width="26" height="26"/><rect class="n b1" x="52" y="48" width="26" height="26"/>'
    + '<rect class="n b1" x="84" y="48" width="26" height="26"/><rect class="n b1" x="116" y="48" width="26" height="26"/>'
    + '<line class="e b1" x1="142" y1="61" x2="200" y2="61"/>'
    + '<rect class="n4 b1" x="200" y="46" width="34" height="30"/>'
    + '<text class="tl b1" x="217" y="67" font-size="13" text-anchor="middle">h</text>'
    + '<line class="e b1" x1="234" y1="61" x2="300" y2="61"/><polygon class="arrow b1" points="300,61 292,56 292,66"/>'
    + '<rect class="n3 b1" x="300" y="46" width="90" height="30"/>'
    + '<text class="tl b1" x="345" y="67" font-size="13" text-anchor="middle">디코더</text>'
    + '<text class="tm b1" x="240" y="100" font-size="13" text-anchor="middle">통로가 벡터 하나뿐이라 긴 문장이 무너져요</text>'
    + '<text class="tm b2" x="60" y="146" font-size="14" text-anchor="middle">어텐션 있음</text>'
    + '<rect class="n b2" x="20" y="160" width="26" height="26"/><rect class="n b2" x="52" y="160" width="26" height="26"/>'
    + '<rect class="n b2" x="84" y="160" width="26" height="26"/><rect class="n b2" x="116" y="160" width="26" height="26"/>'
    + '<line class="e2 b3" x1="33" y1="186" x2="330" y2="176"/><line class="e2 b3" x1="65" y1="186" x2="330" y2="178"/>'
    + '<line class="e2 b3" x1="97" y1="186" x2="330" y2="180"/><line class="e2 b3" x1="129" y1="186" x2="330" y2="182"/>'
    + '<rect class="n3 b2" x="330" y="160" width="90" height="30"/>'
    + '<text class="tl b2" x="375" y="181" font-size="13" text-anchor="middle">디코더</text>'
    + '<text class="tm b3" x="240" y="226" font-size="14" text-anchor="middle">매 걸음마다 소스의 모든 자리를 직접 봐요</text>'
    + '</svg>')

SVG_FOUR = (
    S0
    + '<text class="tb b1" x="24" y="34" font-size="15">1 점수</text>'
    + '<text class="t b1" x="150" y="34" font-size="15">3.6</text><text class="t b1" x="230" y="34" font-size="15">0.8</text>'
    + '<text class="t b1" x="310" y="34" font-size="15">0.5</text><text class="t b1" x="390" y="34" font-size="15">0.4</text>'
    + '<text class="tb b2" x="24" y="84" font-size="15">2 소프트맥스</text>'
    + '<rect class="n2 b2" x="150" y="56" width="34" height="34"/><rect class="n b2" x="230" y="86" width="34" height="4"/>'
    + '<rect class="n b2" x="310" y="87" width="34" height="3"/><rect class="n b2" x="390" y="87" width="34" height="3"/>'
    + '<text class="t b2" x="167" y="108" font-size="14" text-anchor="middle">0.87</text>'
    + '<text class="tm b2" x="247" y="108" font-size="14" text-anchor="middle">0.05</text>'
    + '<text class="tm b2" x="327" y="108" font-size="14" text-anchor="middle">0.04</text>'
    + '<text class="tm b2" x="407" y="108" font-size="14" text-anchor="middle">0.04</text>'
    + '<text class="tb b3" x="24" y="158" font-size="15">3 가중합</text>'
    + '<line class="e2 b3" x1="167" y1="118" x2="300" y2="148"/><line class="e2 b3" x1="247" y1="118" x2="300" y2="150"/>'
    + '<line class="e2 b3" x1="327" y1="118" x2="310" y2="150"/><line class="e2 b3" x1="407" y1="118" x2="320" y2="150"/>'
    + '<rect class="n2 b3" x="300" y="140" width="110" height="30"/>'
    + '<text class="tl b3" x="355" y="161" font-size="14" text-anchor="middle">문맥 벡터 c</text>'
    + '<text class="tb b4" x="24" y="216" font-size="15">4 예측</text>'
    + '<line class="e2 b4" x1="355" y1="170" x2="355" y2="200"/><polygon class="arrow b4" points="355,206 350,196 360,196"/>'
    + '<rect class="n3 b4" x="300" y="206" width="110" height="30"/>'
    + '<text class="tl b4" x="355" y="227" font-size="14" text-anchor="middle">다음 단어</text>'
    + '<text class="tm b4" x="140" y="252" font-size="14" text-anchor="middle">점수, 정규화, 섞기, 예측</text>'
    + '</svg>')

SVG_ALIGN = (
    S0
    + '<text class="tm b1" x="240" y="30" font-size="14" text-anchor="middle">소스 단어 (키)</text>'
    + '<text class="tm b1" x="150" y="52" font-size="13" text-anchor="middle">il</text>'
    + '<text class="tm b1" x="200" y="52" font-size="13" text-anchor="middle">a</text>'
    + '<text class="tm b1" x="250" y="52" font-size="13" text-anchor="middle">m</text>'
    + '<text class="tm b1" x="300" y="52" font-size="13" text-anchor="middle">entarte</text>'
    + '<text class="tm b1" x="100" y="86" font-size="13" text-anchor="end">he</text>'
    + '<text class="tm b1" x="100" y="126" font-size="13" text-anchor="end">hit</text>'
    + '<text class="tm b1" x="100" y="166" font-size="13" text-anchor="end">me</text>'
    + '<text class="tm b1" x="100" y="206" font-size="13" text-anchor="end">pie</text>'
    + '<rect class="n2 b2" x="130" y="62" width="40" height="34"/><rect class="n b1" x="180" y="62" width="40" height="34"/>'
    + '<rect class="n b1" x="230" y="62" width="40" height="34"/><rect class="n b1" x="280" y="62" width="40" height="34"/>'
    + '<rect class="n b1" x="130" y="102" width="40" height="34"/><rect class="n b1" x="180" y="102" width="40" height="34"/>'
    + '<rect class="n2 b2" x="230" y="102" width="40" height="34"/><rect class="n b1" x="280" y="102" width="40" height="34"/>'
    + '<rect class="n b1" x="130" y="142" width="40" height="34"/><rect class="n2 b2" x="180" y="142" width="40" height="34"/>'
    + '<rect class="n b1" x="230" y="142" width="40" height="34"/><rect class="n b1" x="280" y="142" width="40" height="34"/>'
    + '<rect class="n b1" x="130" y="182" width="40" height="34"/><rect class="n b1" x="180" y="182" width="40" height="34"/>'
    + '<rect class="n b1" x="230" y="182" width="40" height="34"/><rect class="n2 b2" x="280" y="182" width="40" height="34"/>'
    + '<text class="tm b3" x="240" y="246" font-size="14" text-anchor="middle">진한 칸이 어텐션 가중치가 큰 곳, 아무도 안 가르쳐 준 정렬이에요</text>'
    + '</svg>')

SVG_QKV = (
    S0
    + '<rect class="n b1" x="20" y="40" width="60" height="30"/><text class="tl b1" x="50" y="61" font-size="13" text-anchor="middle">Zuko</text>'
    + '<rect class="n b1" x="90" y="40" width="60" height="30"/><text class="tl b1" x="120" y="61" font-size="13" text-anchor="middle">made</text>'
    + '<rect class="n2 b1" x="160" y="40" width="60" height="30"/><text class="tl b1" x="190" y="61" font-size="13" text-anchor="middle">his</text>'
    + '<rect class="n b1" x="230" y="40" width="60" height="30"/><text class="tl b1" x="260" y="61" font-size="13" text-anchor="middle">uncle</text>'
    + '<rect class="n b1" x="300" y="40" width="60" height="30"/><text class="tl b1" x="330" y="61" font-size="13" text-anchor="middle">tea</text>'
    + '<line class="e2 b2" x1="190" y1="70" x2="120" y2="112"/><line class="e2 b2" x1="190" y1="70" x2="240" y2="112"/>'
    + '<line class="e2 b2" x1="190" y1="70" x2="360" y2="112"/>'
    + '<rect class="n2 b2" x="60" y="112" width="120" height="32"/>'
    + '<text class="tl b2" x="120" y="134" font-size="14" text-anchor="middle">q = WQ x</text>'
    + '<rect class="n3 b2" x="180" y="112" width="120" height="32"/>'
    + '<text class="tl b2" x="240" y="134" font-size="14" text-anchor="middle">k = WK x</text>'
    + '<rect class="n b2" x="300" y="112" width="120" height="32"/>'
    + '<text class="tl b2" x="360" y="134" font-size="14" text-anchor="middle">v = WV x</text>'
    + '<text class="t b3" x="120" y="176" font-size="14" text-anchor="middle">무엇을 찾나</text>'
    + '<text class="t b3" x="240" y="176" font-size="14" text-anchor="middle">무엇을 내걸까</text>'
    + '<text class="t b3" x="360" y="176" font-size="14" text-anchor="middle">무엇을 건네나</text>'
    + '<text class="tm b3" x="240" y="220" font-size="14" text-anchor="middle">한 토큰이 세 역할을 동시에 맡아요</text>'
    + '<text class="tm b3" x="240" y="246" font-size="14" text-anchor="middle">행렬 세 개는 모든 자리에서 똑같이 다시 써요</text>'
    + '</svg>')

SVG_SHAPE = (
    S0
    + '<rect class="n2 b1" x="20" y="60" width="72" height="60"/><text class="tl b1" x="56" y="96" font-size="16" text-anchor="middle">Q</text>'
    + '<text class="tm b1" x="56" y="138" font-size="13" text-anchor="middle">n x dk</text>'
    + '<text class="t b1" x="104" y="96" font-size="16" text-anchor="middle">x</text>'
    + '<rect class="n3 b1" x="118" y="60" width="72" height="60"/><text class="tl b1" x="154" y="96" font-size="16" text-anchor="middle">KT</text>'
    + '<text class="tm b1" x="154" y="138" font-size="13" text-anchor="middle">dk x n</text>'
    + '<line class="e2 b2" x1="196" y1="90" x2="216" y2="90"/><polygon class="arrow b2" points="216,90 208,85 208,95"/>'
    + '<rect class="n b2" x="222" y="60" width="72" height="60"/><text class="tl b2" x="258" y="96" font-size="14" text-anchor="middle">점수</text>'
    + '<text class="tm b2" x="258" y="138" font-size="13" text-anchor="middle">n x n</text>'
    + '<line class="e2 b3" x1="300" y1="90" x2="320" y2="90"/><polygon class="arrow b3" points="320,90 312,85 312,95"/>'
    + '<rect class="n2 b3" x="326" y="60" width="72" height="60"/><text class="tl b3" x="362" y="96" font-size="16" text-anchor="middle">A</text>'
    + '<text class="tm b3" x="362" y="138" font-size="13" text-anchor="middle">행 합 1</text>'
    + '<text class="t b4" x="180" y="192" font-size="15" text-anchor="middle">A x V</text>'
    + '<line class="e2 b4" x1="204" y1="187" x2="228" y2="187"/><polygon class="arrow b4" points="228,187 220,182 220,192"/>'
    + '<rect class="n3 b4" x="234" y="166" width="90" height="34"/>'
    + '<text class="tl b4" x="279" y="189" font-size="14" text-anchor="middle">O (n x dv)</text>'
    + '<text class="tm b4" x="240" y="240" font-size="14" text-anchor="middle">자리마다 도는 반복문이 없어서 GPU 가 한 번에 계산해요</text>'
    + '</svg>')

SVG_BARRIER = (
    S0
    + '<rect class="box b1" x="14" y="40" width="144" height="92" rx="2"/>'
    + '<text class="tb b1" x="86" y="68" font-size="14" text-anchor="middle">1 순서를 몰라요</text>'
    + '<text class="tm b1" x="86" y="96" font-size="13" text-anchor="middle">섞어도 결과가 같아요</text>'
    + '<text class="tm b1" x="86" y="118" font-size="13" text-anchor="middle">순열 등변성</text>'
    + '<rect class="box b1" x="168" y="40" width="144" height="92" rx="2"/>'
    + '<text class="tb b1" x="240" y="68" font-size="14" text-anchor="middle">2 비선형이 없어요</text>'
    + '<text class="tm b1" x="240" y="96" font-size="13" text-anchor="middle">평균만 다시 낼 뿐</text>'
    + '<text class="tm b1" x="240" y="118" font-size="13" text-anchor="middle">쌓아도 선형에 가까워요</text>'
    + '<rect class="box b1" x="322" y="40" width="144" height="92" rx="2"/>'
    + '<text class="tb b1" x="394" y="68" font-size="14" text-anchor="middle">3 미래를 봐요</text>'
    + '<text class="tm b1" x="394" y="96" font-size="13" text-anchor="middle">아직 안 쓴 토큰까지</text>'
    + '<text class="tm b1" x="394" y="118" font-size="13" text-anchor="middle">문제가 시시해져요</text>'
    + '<line class="e2 b2" x1="86" y1="136" x2="86" y2="162"/><polygon class="arrow b2" points="86,168 81,158 91,158"/>'
    + '<line class="e2 b2" x1="240" y1="136" x2="240" y2="162"/><polygon class="arrow b2" points="240,168 235,158 245,158"/>'
    + '<line class="e2 b2" x1="394" y1="136" x2="394" y2="162"/><polygon class="arrow b2" points="394,168 389,158 399,158"/>'
    + '<rect class="n2 b3" x="14" y="176" width="144" height="46"/>'
    + '<text class="tl b3" x="86" y="205" font-size="14" text-anchor="middle">위치 인코딩</text>'
    + '<rect class="n2 b3" x="168" y="176" width="144" height="46"/>'
    + '<text class="tl b3" x="240" y="198" font-size="13" text-anchor="middle">위치별 피드포워드</text>'
    + '<text class="tl b3" x="240" y="216" font-size="13" text-anchor="middle">신경망 FFN</text>'
    + '<rect class="n2 b3" x="322" y="176" width="144" height="46"/>'
    + '<text class="tl b3" x="394" y="205" font-size="14" text-anchor="middle">인과 마스킹</text>'
    + '<text class="tm b3" x="240" y="250" font-size="14" text-anchor="middle">장벽 셋, 부품 셋, 쌓을 수 있는 블록 하나</text>'
    + '</svg>')

SVG_MASK = (
    S0
    + '<text class="tm b1" x="240" y="32" font-size="14" text-anchor="middle">행 = 지금 보는 토큰, 열 = 바라보는 토큰</text>'
    + '<text class="tm b1" x="118" y="60" font-size="13" text-anchor="middle">The</text>'
    + '<text class="tm b1" x="166" y="60" font-size="13" text-anchor="middle">chef</text>'
    + '<text class="tm b1" x="214" y="60" font-size="13" text-anchor="middle">who</text>'
    + '<text class="tm b1" x="262" y="60" font-size="13" text-anchor="middle">made</text>'
    + '<text class="tm b1" x="310" y="60" font-size="13" text-anchor="middle">tea</text>'
    + "".join(
        '<text class="tm b1" x="88" y="%d" font-size="13" text-anchor="end">%s</text>'
        % (92 + 34 * i, w) for i, w in enumerate(["The", "chef", "who", "made", "tea"]))
    + "".join(
        '<rect class="%s b%d" x="%d" y="%d" width="44" height="30"/>'
        % ((("n2", 2) if c <= r else ("n4", 3)) + (96 + 48 * c, 70 + 34 * r))
        for r in range(5) for c in range(5))
    + '<text class="tm b3" x="240" y="252" font-size="14" text-anchor="middle">오른쪽 위 삼각형은 소프트맥스 전에 -무한대로 막아요</text>'
    + '</svg>')

SVG_MHA = (
    S0
    + '<rect class="n b1" x="16" y="106" width="70" height="44"/>'
    + '<text class="tl b1" x="51" y="133" font-size="14" text-anchor="middle">X (n x d)</text>'
    + '<line class="e2 b2" x1="86" y1="120" x2="130" y2="66"/><line class="e2 b2" x1="86" y1="128" x2="130" y2="128"/>'
    + '<line class="e2 b2" x1="86" y1="136" x2="130" y2="190"/>'
    + '<rect class="n2 b2" x="130" y="48" width="130" height="36"/>'
    + '<text class="tl b2" x="195" y="71" font-size="13" text-anchor="middle">헤드 1 (d/h 차원)</text>'
    + '<rect class="n2 b2" x="130" y="110" width="130" height="36"/>'
    + '<text class="tl b2" x="195" y="133" font-size="13" text-anchor="middle">헤드 2 (d/h 차원)</text>'
    + '<rect class="n2 b2" x="130" y="172" width="130" height="36"/>'
    + '<text class="tl b2" x="195" y="195" font-size="13" text-anchor="middle">헤드 h (d/h 차원)</text>'
    + '<line class="e2 b3" x1="260" y1="66" x2="300" y2="120"/><line class="e2 b3" x1="260" y1="128" x2="300" y2="128"/>'
    + '<line class="e2 b3" x1="260" y1="190" x2="300" y2="136"/>'
    + '<rect class="n3 b3" x="300" y="106" width="60" height="44"/>'
    + '<text class="tl b3" x="330" y="133" font-size="13" text-anchor="middle">이어 붙임</text>'
    + '<line class="e2 b4" x1="360" y1="128" x2="392" y2="128"/><polygon class="arrow b4" points="392,128 384,123 384,133"/>'
    + '<rect class="n2 b4" x="398" y="106" width="60" height="44"/>'
    + '<text class="tl b4" x="428" y="133" font-size="15" text-anchor="middle">WO</text>'
    + '<text class="tm b4" x="240" y="244" font-size="14" text-anchor="middle">헤드마다 d/h 차원이라 전체 계산량과 파라미터 수는 그대로예요</text>'
    + '</svg>')

SVG_LN = (
    S0
    + '<text class="tb b1" x="120" y="36" font-size="15" text-anchor="middle">Post-LN (2017 논문)</text>'
    + '<rect class="n b1" x="60" y="164" width="120" height="32"/>'
    + '<text class="tl b1" x="120" y="186" font-size="13" text-anchor="middle">부분층</text>'
    + '<line class="e b1" x1="120" y1="164" x2="120" y2="140"/>'
    + '<rect class="n3 b1" x="60" y="108" width="120" height="30"/>'
    + '<text class="tl b1" x="120" y="129" font-size="13" text-anchor="middle">더하기</text>'
    + '<rect class="n2 b1" x="60" y="60" width="120" height="32"/>'
    + '<text class="tl b1" x="120" y="82" font-size="13" text-anchor="middle">층 정규화</text>'
    + '<line class="e b1" x1="120" y1="108" x2="120" y2="92"/>'
    + '<line class="e2 b1" x1="40" y1="212" x2="40" y2="123"/><line class="e2 b1" x1="40" y1="123" x2="60" y2="123"/>'
    + '<text class="tm b1" x="120" y="232" font-size="13" text-anchor="middle">잔차 길에 정규화가 끼어요</text>'
    + '<text class="tb b2" x="352" y="36" font-size="15" text-anchor="middle">Pre-LN (요즘 LLM)</text>'
    + '<rect class="n2 b2" x="292" y="164" width="120" height="32"/>'
    + '<text class="tl b2" x="352" y="186" font-size="13" text-anchor="middle">층 정규화</text>'
    + '<rect class="n b2" x="292" y="108" width="120" height="32"/>'
    + '<text class="tl b2" x="352" y="130" font-size="13" text-anchor="middle">부분층</text>'
    + '<line class="e b2" x1="352" y1="164" x2="352" y2="140"/>'
    + '<rect class="n3 b2" x="292" y="60" width="120" height="30"/>'
    + '<text class="tl b2" x="352" y="81" font-size="13" text-anchor="middle">더하기</text>'
    + '<line class="e b2" x1="352" y1="108" x2="352" y2="90"/>'
    + '<line class="e2 b2" x1="272" y1="212" x2="272" y2="75"/><line class="e2 b2" x1="272" y1="75" x2="292" y2="75"/>'
    + '<text class="tm b2" x="352" y="232" font-size="13" text-anchor="middle">잔차 길이 깨끗하게 뚫려요</text>'
    + '</svg>')

SVG_FULL = (
    S0
    + '<text class="tm b1" x="104" y="30" font-size="14" text-anchor="middle">인코더 x N</text>'
    + '<rect class="n b1" x="24" y="200" width="160" height="30"/>'
    + '<text class="tl b1" x="104" y="220" font-size="12" text-anchor="middle">입력 임베딩 + 위치 인코딩</text>'
    + '<rect class="n2 b1" x="24" y="156" width="160" height="30"/>'
    + '<text class="tl b1" x="104" y="176" font-size="12" text-anchor="middle">멀티 헤드 셀프 어텐션</text>'
    + '<rect class="n3 b1" x="24" y="120" width="160" height="26"/>'
    + '<text class="tl b1" x="104" y="138" font-size="12" text-anchor="middle">더하기와 정규화</text>'
    + '<rect class="n b1" x="24" y="84" width="160" height="26"/>'
    + '<text class="tl b1" x="104" y="102" font-size="12" text-anchor="middle">피드포워드</text>'
    + '<rect class="n3 b1" x="24" y="48" width="160" height="26"/>'
    + '<text class="tl b1" x="104" y="66" font-size="12" text-anchor="middle">더하기와 정규화</text>'
    + '<text class="tm b2" x="376" y="30" font-size="14" text-anchor="middle">디코더 x N</text>'
    + '<rect class="n b2" x="296" y="200" width="160" height="30"/>'
    + '<text class="tl b2" x="376" y="220" font-size="12" text-anchor="middle">출력 임베딩 + 위치 인코딩</text>'
    + '<rect class="n2 b2" x="296" y="156" width="160" height="30"/>'
    + '<text class="tl b2" x="376" y="176" font-size="12" text-anchor="middle">마스크 셀프 어텐션</text>'
    + '<rect class="n4 b3" x="296" y="112" width="160" height="30"/>'
    + '<text class="tl b3" x="376" y="132" font-size="12" text-anchor="middle">크로스 어텐션</text>'
    + '<rect class="n b2" x="296" y="72" width="160" height="26"/>'
    + '<text class="tl b2" x="376" y="90" font-size="12" text-anchor="middle">피드포워드</text>'
    + '<rect class="n3 b2" x="296" y="40" width="160" height="26"/>'
    + '<text class="tl b2" x="376" y="58" font-size="12" text-anchor="middle">선형 + 소프트맥스</text>'
    + '<line class="e2 b3" x1="184" y1="61" x2="240" y2="61"/><line class="e2 b3" x1="240" y1="61" x2="240" y2="127"/>'
    + '<line class="e2 b3" x1="240" y1="127" x2="296" y2="127"/><polygon class="arrow b3" points="296,127 288,122 288,132"/>'
    + '<text class="tm b3" x="240" y="252" font-size="13" text-anchor="middle">키와 밸류는 인코더에서, 쿼리는 디코더에서 와요</text>'
    + '</svg>')

SVG_BLEU = (
    S0
    + '<text class="tm b1" x="240" y="30" font-size="14" text-anchor="middle">WMT14 영어에서 독일어, BLEU 점수</text>'
    + '<line class="e b1" x1="40" y1="200" x2="450" y2="200"/>'
    + '<rect class="n b1" x="60" y="140" width="60" height="60"/>'
    + '<text class="t b1" x="90" y="132" font-size="14" text-anchor="middle">24.6</text>'
    + '<text class="tm b1" x="90" y="220" font-size="13" text-anchor="middle">GNMT</text>'
    + '<text class="tm b1" x="90" y="238" font-size="12" text-anchor="middle">RNN</text>'
    + '<rect class="n b1" x="160" y="128" width="60" height="72"/>'
    + '<text class="t b1" x="190" y="120" font-size="14" text-anchor="middle">25.2</text>'
    + '<text class="tm b1" x="190" y="220" font-size="13" text-anchor="middle">ConvS2S</text>'
    + '<text class="tm b1" x="190" y="238" font-size="12" text-anchor="middle">CNN</text>'
    + '<rect class="n2 b2" x="260" y="86" width="60" height="114"/>'
    + '<text class="tb b2" x="290" y="78" font-size="14" text-anchor="middle">27.3</text>'
    + '<text class="tm b2" x="290" y="220" font-size="13" text-anchor="middle">Transformer</text>'
    + '<text class="tm b2" x="290" y="238" font-size="12" text-anchor="middle">base</text>'
    + '<rect class="n2 b3" x="360" y="64" width="60" height="136"/>'
    + '<text class="tb b3" x="390" y="56" font-size="14" text-anchor="middle">28.4</text>'
    + '<text class="tm b3" x="390" y="220" font-size="13" text-anchor="middle">Transformer</text>'
    + '<text class="tm b3" x="390" y="238" font-size="12" text-anchor="middle">big</text>'
    + '</svg>')

SVG_QUAD = (
    S0
    + '<text class="tm b1" x="110" y="34" font-size="14" text-anchor="middle">토큰 4개, 짝은 4 x 4 = 16</text>'
    + "".join(
        '<rect class="n b1" x="%d" y="%d" width="26" height="26"/>' % (40 + 30 * c, 50 + 30 * r)
        for r in range(4) for c in range(4))
    + '<text class="tb b2" x="350" y="84" font-size="15" text-anchor="middle">n = 512</text>'
    + '<rect class="n2 b2" x="320" y="96" width="60" height="16"/>'
    + '<text class="t b2" x="350" y="132" font-size="14" text-anchor="middle">262,144 칸</text>'
    + '<text class="tb b3" x="350" y="172" font-size="15" text-anchor="middle">n = 128,000</text>'
    + '<rect class="n4 b3" x="260" y="184" width="200" height="16"/>'
    + '<text class="t b3" x="350" y="220" font-size="14" text-anchor="middle">약 164억 칸</text>'
    + '<text class="tm b3" x="150" y="250" font-size="14" text-anchor="middle">길이 250배면 칸은 62,500배</text>'
    + '</svg>')

assert round(N2 ** 2 / 1e8, 2) == 163.84

U = []

# ---------------------------------------------------------------- w4-1
t = [T("기계 번역", "Machine Translation (MT)", "컴퓨터로 한 언어의 문장을 다른 언어로 옮기는 일이에요.",
       "원문 x 가 주어졌을 때 가장 그럴듯한 번역문 y 를 찾는 문제로 적어요."),
     T("시퀀스-투-시퀀스", "seq2seq", "줄줄이 들어와서 줄줄이 나가는 구조예요.",
       "읽는 쪽과 쓰는 쪽, 신경망 두 개를 이어 붙여 만들어요. 2014년에 나왔어요."),
     T("인코더", "Encoder", "원문을 끝까지 읽어 벡터 하나로 압축하는 쪽이에요."),
     T("디코더", "Decoder", "압축된 벡터를 받아 목표 언어 문장을 한 토큰씩 써 내려가는 쪽이에요."),
     T("조건부 언어 모델", "Conditional Language Model", "원문이라는 조건이 하나 더 붙은 언어 모델이에요.",
       "휴대폰 자판 추천에 '원문' 이라는 힌트가 하나 더 붙은 것이라고 보면 돼요."),
     T("정보 병목", "Information Bottleneck", "원문 전체가 벡터 하나에 다 들어가야 해서 생기는 막힘이에요.",
       "20단어 문장도 200단어 문단도 같은 칸 수에 담아야 해요. 문장이 길수록 무너져요.")]
U.append({"id": "w4-1", "title": "seq2seq 와 정보 병목", "goal": "인코더와 디코더가 무엇을 하는지, 왜 벡터 하나가 병목이 되는지 말할 수 있어요.", "terms": t, "slides": [
    title("seq2seq 와 병목", "읽는 신경망 하나, 쓰는 신경망 하나"),
    goal("**기계 번역(Machine Translation (MT))** 이 어떤 문제인지", "**인코더(Encoder)** 와 **디코더(Decoder)** 가 하는 일", "**정보 병목(Information Bottleneck)** 이 무엇인지"),
    pts("지난주에서 오늘로 (N4 p.4, p.6)", "지난주 **순환 신경망(RNN)** 은 한 걸음씩 읽으며 기억을 들고 다녔어요",
        "못 푼 문제 1: 멀리 떨어진 말이 안 닿아요(**기울기 소실(Vanishing Gradient)**)", "못 푼 문제 2: 차례로만 계산해서 느려요",
        "새 문제 3: 원문 전부가 벡터 하나에 담겨야 해요(**정보 병목(Information Bottleneck)**)"),
    ana("통역사 두 명", "첫 번째 사람이 프랑스어 문장을 끝까지 듣고 쪽지 한 장에 요약을 적어 건네요. 두 번째 사람은 그 쪽지만 보고 영어로 말해요.",
        [("끝까지 듣는 사람", "**인코더(Encoder)**"), ("쪽지 한 장", "요약 벡터"), ("쪽지만 보고 말하는 사람", "**디코더(Decoder)**")]),
    pts("과제: 기계 번역 (N4 p.7)", "원문 x 를 주면 다른 언어의 문장 y 를 만들어요",
        "수식으로는 $\\arg\\max_y P(y \\mid x)$, 곧 가장 그럴듯한 y 찾기", "가능한 y 가 사실상 무한히 많아서 찾아다녀야 해요(디코딩)"),
    cmp_("한 과제, 세 시대 (N4 p.8)", ["때", "방법"], [["1950s~80s", "사람이 쓴 규칙과 이중 언어 사전"],
                                                 ["1990s~2010s", "통계 **기계 번역(Machine Translation (MT))**: 정렬 모델, 구 테이블, 재순위"],
                                                 ["2014~", "신경망 번역: **시퀀스-투-시퀀스(seq2seq)** 하나를 통째로 학습"]]),
    fig("인코더와 디코더, 그 사이의 벡터 하나", SVG_ENCDEC, "**인코더(Encoder)** 가 il a m entarte 를 읽어 h 로 압축하고, **디코더(Decoder)** 가 he hit me pie 를 써요", 4),
    form("디코더는 조건부 언어 모델", r"P(y \mid x) = \prod_{t=1}^{T} P\left(y_t \mid y_1, \ldots, y_{t-1},\; x\right)",
         [(r"x", "원문. 이것이 '조건' 이에요"), (r"y_t", "지금 만들 t 번째 토큰"),
          (r"y_1, \ldots, y_{t-1}", "앞에서 이미 만든 토큰들"), (r"\prod", "한 토큰씩의 확률을 모두 곱하기")],
         "3주차의 **언어 모델(Language Model (LM))** 식에 원문 x 가 조건으로 하나 더 붙은 것이에요. 그래서 **조건부 언어 모델(Conditional Language Model)** 이라고 불러요."),
    pts("종단간 학습 (N4 p.10)", "학습은 목표 문장 토큰에 대한 **교차 엔트로피(Cross-Entropy)** 하나뿐이에요",
        "**기울기(Gradient)** 가 **디코더(Decoder)**, 다리 벡터, **인코더(Encoder)** 까지 한 번에 흘러가요", "모델 하나, 손실 하나, 역방향 한 번. 이것이 종단간(end-to-end) 이에요"),
    pts("번역만이 아니에요 (N4 p.15)", "입력도 출력도 줄줄이면 같은 구조를 그대로 써요",
        "요약(긴 글 → 짧은 글), 대화(문맥 → 응답), 코드 생성, 음성 인식", "**시퀀스-투-시퀀스(seq2seq)** 패턴을 한 번 익혀 학기 내내 다시 써요"),
    fig("병목이 있을 때와 없을 때", SVG_BOTTLE, "벡터 하나로만 통하면 긴 문장이 무너져요. 어텐션은 소스의 모든 자리를 직접 봐요", 3),
    check("**디코더(Decoder)** 를 '조건부' 언어 모델이라고 부르는 까닭은?",
          ["원문 x 가 조건으로 붙어서", "확률을 안 쓰기 때문에", "토큰을 거꾸로 만들어서", "학습을 두 번 해서"], 0,
          "앞에서 만든 토큰만이 아니라 **인코더(Encoder)** 가 읽은 원문 x 까지 조건으로 보고 다음 토큰을 골라요."),
    check("**정보 병목(Information Bottleneck)** 이 특히 긴 문장에서 아픈 까닭은?",
          ["길든 짧든 같은 크기 벡터 하나에 담아야 해서", "긴 문장은 단어가 어려워서", "**디코더(Decoder)** 가 느려서", "학습 데이터가 없어서"], 0,
          "20단어도 200단어도 같은 칸 수예요. 담을 것이 많아질수록 버려지는 정보가 생겨요."),
    warn("헷갈리기 쉬운 점", "**인코더(Encoder)** 와 **디코더(Decoder)** 는 둘 다 신경망이에요. 한쪽만 신경망인 게 아니에요.",
         "**정보 병목(Information Bottleneck)** 은 2주차 **미등록 단어(OOV)** 문제와 다른 이야기예요.",
         "'종단간' 은 부품을 따로 학습하지 않고 하나로 학습한다는 뜻이에요."),
    recap("**기계 번역(Machine Translation (MT))**: 원문 x 에서 번역문 y 를 찾는 문제",
          "**시퀀스-투-시퀀스(seq2seq)** = **인코더(Encoder)** + **디코더(Decoder)**, 디코더는 **조건부 언어 모델(Conditional Language Model)**",
          "다리 벡터 하나가 **정보 병목(Information Bottleneck)**, 오늘의 어텐션이 이것을 풀어요",
          "오늘의 용어: 기계 번역(MT), seq2seq, 인코더(Encoder), 디코더(Decoder), 조건부 언어 모델, 정보 병목"),
]})

# ---------------------------------------------------------------- w4-2
t = [T("교사 강요", "Teacher Forcing", "학습할 때 모델이 만든 토큰 대신 정답 토큰을 다음 입력으로 넣어 주는 것이에요."),
     T("노출 편향", "Exposure Bias", "학습 때는 정답만 보고, 시험 때는 자기 출력만 보게 되는 차이예요."),
     T("탐욕적 디코딩", "Greedy Decoding", "매 걸음 가장 확률 높은 토큰 하나만 고르는 방법이에요."),
     T("빔 서치", "Beam Search", "걸음마다 가장 좋은 후보 k 개를 함께 들고 가는 방법이에요."),
     T("빔 크기", "Beam Size", "함께 들고 가는 후보의 개수 k 예요. 보통 5에서 10 이에요."),
     T("길이 정규화", "Length Normalization", "점수를 길이로 나눠 짧은 문장이 유리해지는 것을 막는 것이에요."),
     T("블루 점수", "BLEU", "사람 번역과 겹치는 n-gram 을 세어 번역을 채점하는 자동 지표예요.")]
U.append({"id": "w4-2", "title": "디코딩: 교사 강요에서 빔 서치까지", "goal": "학습과 추론의 차이, 탐욕과 빔 서치의 차이를 숫자로 설명할 수 있어요.", "terms": t, "slides": [
    title("어떻게 써 내려갈까", "교사 강요, 탐욕, 빔 서치, 그리고 채점"),
    goal("**교사 강요(Teacher Forcing)** 와 **노출 편향(Exposure Bias)**", "**탐욕적 디코딩(Greedy Decoding)** 과 **빔 서치(Beam Search)** 의 차이", "**길이 정규화(Length Normalization)** 를 왜 하는지"),
    ana("받아쓰기 연습", "받아쓰기를 하다 한 글자 틀려도 선생님이 바로 정답을 알려 주고 다음 글자로 넘어가요. 그래야 뒤쪽 연습도 제대로 돼요.",
        [("선생님이 알려 주는 정답", "**교사 강요(Teacher Forcing)**"), ("틀려도 계속 진도", "자리마다 벌점만 따로 매기기"), ("실전에는 알려 줄 사람이 없음", "**노출 편향(Exposure Bias)**")]),
    pts("학습 때 (N4 p.11)", "**교사 강요(Teacher Forcing)**: 모델의 예측 대신 진짜 이전 목표 단어를 넣어요",
        "좋은 점: 학습이 안정되고 시간 방향으로 한꺼번에 계산할 수 있어요", "나쁜 점: 시험 때는 자기 출력만 보게 돼요. 이 차이가 **노출 편향(Exposure Bias)** 이에요"),
    ana("갈림길에서 눈앞만 보기", "산에서 갈림길마다 지금 당장 편해 보이는 쪽으로만 가요. 나중에 막다른 길이 나와도 되돌아갈 수 없어요.",
        [("지금 당장 편한 쪽", "확률이 가장 높은 토큰 하나"), ("되돌아갈 수 없음", "**탐욕적 디코딩(Greedy Decoding)**"), ("전체로 더 좋은 길", "전체 확률이 더 높은 다른 후보")]),
    pts("추론 1: 탐욕 (N4 p.12)", "**탐욕적 디코딩(Greedy Decoding)**: 매 걸음 1등 토큰 하나만 고르고 끝",
        "빠르고, 웬만하면 괜찮아요", "문제: 앞에서 자신 있게 고른 한 단어가 틀리면 뒤가 전부 망가져요"),
    fig("빔 서치 한 그루 (N4 p.13)", SVG_BEAM, "**빔 크기(Beam Size)** k = 2. 걸음마다 점수 상위 두 갈래만 남기고 나머지는 잘라요", 3),
    steps("손계산: 길이로 나눠 비교하기", [
        "끝난 후보 둘: 'he hit me' 점수 -2.5, 'I was hit' 점수 -3.5",
        "둘 다 3단어라 -2.5 ÷ 3 = -0.833, -3.5 ÷ 3 = -1.167",
        "-0.833 이 -1.167 보다 커요. 그래서 'he hit me' 가 이겨요",
        "길이가 다르면 왜 필요한지: 'he hit' (2단어) 점수 -1.6 → -1.6 ÷ 2 = -0.8",
        "'he hit me' (3단어) -2.5 ÷ 3 = -0.833. 나누기 전에는 -1.6 이 더 높아 보였어요",
    ], "**길이 정규화(Length Normalization)** 없이 그냥 합만 보면 짧은 문장이 늘 이겨요", "점수는 로그 확률의 합이라 더할수록 작아져요"),
    pts("빔 서치의 트레이드 오프", "**빔 크기(Beam Size)** k 가 크면 더 넓게 찾지만 계산이 늘어요. 보통 5에서 10",
        "k = 1 이면 **탐욕적 디코딩(Greedy Decoding)** 과 똑같아요", "교수님: 항상 **빔 서치(Beam Search)** 가 좋은 건 아니고 트레이드 오프가 있다는 정도는 기억해 달라"),
    ana("답안지와 모범답안 겹쳐 보기", "모범답안과 내 답안을 겹쳐 놓고 한 단어, 두 단어, 세 단어, 네 단어짜리 표현이 얼마나 똑같이 나왔는지 세요.",
        [("모범답안", "사람이 만든 정답 번역"), ("겹친 표현 세기", "**n-gram(n-gram)** 정밀도 n = 1 에서 4"), ("짧게 써서 점수 따는 꼼수 막기", "**간결성 페널티(Brevity Penalty)**")]),
    cmp_("**블루 점수(BLEU)** 의 두 얼굴 (N4 p.14)", ["", "내용"],
         [["재는 법", "사람 번역과 겹치는 n = 1에서 4 까지의 묶음을 세요"], ["꼼수 막기", "너무 짧게 쓰면 **간결성 페널티(Brevity Penalty)** 로 깎여요"],
          ["예", "정답 the cat is on the mat, 출력 the cat the cat on the mat"], ["한계", "다른 낱말을 쓴 좋은 번역은 점수가 낮아요"],
          ["교훈", "모든 지표는 대리 지표예요. 무엇을 못 보는지 알고 써요"]]),
    check("**빔 크기(Beam Size)** k = 1 인 **빔 서치(Beam Search)** 는 무엇과 같은가요?",
          ["**탐욕적 디코딩(Greedy Decoding)**", "무작위 뽑기", "완전 탐색", "**길이 정규화(Length Normalization)**"], 0,
          "후보를 하나만 들고 가면 매 걸음 1등만 고르는 것과 똑같아요."),
    check("끝난 후보를 비교하기 전에 길이로 나누는 까닭은?",
          ["로그 확률의 합이라 길수록 점수가 낮아져서", "계산이 빨라져서", "**블루 점수(BLEU)** 가 높아져서", "**교사 강요(Teacher Forcing)** 때문에"], 0,
          "음수인 로그 확률을 계속 더하니 긴 문장이 불리해요. 그래서 **길이 정규화(Length Normalization)** 를 해요."),
    warn("헷갈리기 쉬운 점", "**교사 강요(Teacher Forcing)** 는 학습 때만 해요. 추론 때는 자기 출력을 다시 넣어요.",
         "**빔 서치(Beam Search)** 는 완전 탐색이 아니라 아주 좋은 근사예요.",
         "**블루 점수(BLEU)** 는 높을수록 좋고, 3주차의 **퍼플렉서티(Perplexity (PPL))** 는 낮을수록 좋아요."),
    recap("**교사 강요(Teacher Forcing)** 로 배우고, 그 차이가 **노출 편향(Exposure Bias)**",
          "**탐욕적 디코딩(Greedy Decoding)** 은 k = 1, **빔 서치(Beam Search)** 는 **빔 크기(Beam Size)** k 개를 들고 가기",
          "끝난 후보는 **길이 정규화(Length Normalization)** 뒤에 비교, 채점은 **블루 점수(BLEU)**",
          "오늘의 용어: 교사 강요, 노출 편향, 탐욕적 디코딩, 빔 서치, 빔 크기, 길이 정규화, BLEU"),
]})

# ---------------------------------------------------------------- w4-3
t = [T("어텐션", "Attention", "필요할 때 원문을 다시 돌아보게 해 주는 방법이에요.",
       "매 걸음 소스의 모든 자리에 점수를 매기고, 그 비율로 섞어 새 요약을 만들어요."),
     T("어텐션 점수", "Attention Score", "지금 쓰려는 자리와 소스 각 자리가 얼마나 관련 있는지 나타내는 날것 숫자예요."),
     T("어텐션 분포", "Attention Distribution", "점수를 소프트맥스로 눌러 만든, 다 더하면 1인 확률 목록이에요."),
     T("문맥 벡터", "Context Vector", "소스 상태들을 가중치대로 섞어 만든 벡터 하나예요."),
     T("가중합", "Weighted Sum", "각 값에 비중을 곱해서 모두 더한 것이에요."),
     T("소프트맥스", "Softmax", "점수를 모두 더해 1이 되는 확률 파이로 나누는 함수예요.")]
U.append({"id": "w4-3", "title": "어텐션: 네 줄로 끝나는 생각", "goal": "점수, 정규화, 섞기, 예측 네 단계를 숫자로 따라 할 수 있어요.", "terms": t, "slides": [
    title("어텐션 네 줄", "점수, 정규화, 섞기, 예측"),
    goal("**어텐션(Attention)** 의 핵심 생각 한 줄", "**어텐션 점수(Attention Score)** 에서 **문맥 벡터(Context Vector)** 까지", "소프트맥스와 가중합을 손으로 해 보기"),
    ana("시험 볼 때 교과서 다시 펼치기", "요약 노트 한 장만 들고 시험을 보는 대신, 문제마다 교과서를 펼쳐 필요한 쪽만 다시 읽는 거예요.",
        [("요약 노트 한 장", "**정보 병목(Information Bottleneck)** 이 되는 벡터"), ("문제마다 교과서를 펼침", "걸음마다 소스 전부를 다시 보기"), ("필요한 쪽만 오래 읽음", "관련 있는 자리에 큰 **어텐션 가중치(Attention Weight)**")]),
    pts("핵심 생각 (N4 p.18)", "**디코더(Decoder)** 걸음마다 **인코더(Encoder)** 상태를 전부 보고 지금 중요한 것을 골라요",
        "요약 벡터 하나에 매달리지 않고, 걸음마다 새 요약을 만들어요", "출력의 모든 자리에서 입력의 모든 단어로 직통 연결이 생겨요"),
    ana("성적의 가중 평균", "과목마다 학점이 다르면 그냥 평균이 아니라 학점을 곱해서 더해요. 중요한 과목이 성적에 더 많이 반영되죠.",
        [("과목 점수", "**인코더(Encoder)** 상태"), ("과목 학점 비중", "**어텐션 가중치(Attention Weight)**"), ("최종 평점", "**문맥 벡터(Context Vector)**")]),
    fig("네 단계 한 장에 (N4 p.19, p.21, p.23)", SVG_FOUR, "점수 → **소프트맥스(Softmax)** → **가중합(Weighted Sum)** → 다음 단어 예측", 4),
    form("어텐션 네 줄 (N4 p.24)", r"e_i = s^{\top} h_i,\quad \alpha = \mathrm{softmax}(e),\quad c = \sum_i \alpha_i h_i,\quad \hat{y} = \mathrm{softmax}(U\tilde{s})",
         [(r"e_i", "**어텐션 점수(Attention Score)**. 가장 단순한 것은 내적이에요"),
          (r"\alpha", "**어텐션 분포(Attention Distribution)**. 다 더하면 1 이에요"),
          (r"c = \sum_i \alpha_i h_i", "**가중합(Weighted Sum)** 으로 만든 **문맥 벡터(Context Vector)**"),
          (r"\tilde{s}", "문맥 벡터와 디코더 상태를 이어 붙여 만든 것"),
          (r"\hat{y}", "다음 단어의 확률")],
         "점수를 내고, 확률로 눌러 담고, 그 비율로 섞고, 예측해요. 교수님: 이 네 단계가 **어텐션(Attention)** 에서 가장 중요해요."),
    steps("손계산 1: 점수를 확률로 (N4 p.19, p.21)", [
        "**어텐션 점수(Attention Score)** 네 개: 3.6, 0.8, 0.5, 0.4",
        "**소프트맥스(Softmax)** 는 각 점수에 exp 를 씌우고 전체 합으로 나눠요",
        "exp(3.6) ≈ 36.6, exp(0.8) ≈ 2.23, exp(0.5) ≈ 1.65, exp(0.4) ≈ 1.49",
        "합 ≈ 41.97 로 나누면 0.87, 0.05, 0.04, 0.04",
        "더해서 1 이 되는지 확인: 0.87 + 0.05 + 0.04 + 0.04 = 1.00",
    ], "**어텐션 분포(Attention Distribution)** = 0.87, 0.05, 0.04, 0.04. 첫 단어에 거의 다 집중해요", "슬라이드 그림의 네 점수를 그대로 썼어요"),
    steps("손계산 2: 가중합으로 문맥 벡터 (N4 p.19)", [
        "**어텐션 가중치(Attention Weight)**: 0.62, 0.14, 0.12, 0.12 (합은 1)",
        "소스 상태를 아주 작게: h1 = (2, 0), h2 = (0, 2), h3 = (1, 1), h4 = (0, 0)",
        "첫 칸: 0.62x2 + 0.14x0 + 0.12x1 + 0.12x0 = 1.24 + 0.12 = 1.36",
        "둘째 칸: 0.62x0 + 0.14x2 + 0.12x1 + 0.12x0 = 0.28 + 0.12 = 0.40",
        "**문맥 벡터(Context Vector)** = (1.36, 0.40). 소스 상태 하나와 크기가 같아요",
    ], "c = (1.36, 0.40). **가중합(Weighted Sum)** 은 곱해서 더하기, 그게 전부예요", "가중치는 슬라이드 숫자, 상태는 손으로 풀기 위한 작은 값이에요"),
    pts("뾰족한 가중치와 평평한 가중치 (N4 p.19)", "뾰족하면 '여기를 봐' 라는 뜻이에요", "평평하면 '다 조금씩 중요해' 라는 뜻이에요",
        "고르게 주면 그냥 평균(mean pooling)이고, 배운 비중을 쓰면 **어텐션(Attention)** 이에요"),
    check("**소프트맥스(Softmax)** 를 거친 뒤 네 수를 모두 더하면?",
          ["1", "0", "점수의 합", "4"], 0, "**어텐션 분포(Attention Distribution)** 는 확률이라 다 더하면 1 이에요."),
    check("**문맥 벡터(Context Vector)** 는 어떻게 만들어지나요?",
          ["소스 상태들의 **가중합(Weighted Sum)**", "소스 상태 중 가장 큰 것", "점수들의 평균", "디코더 상태 그 자체"], 0,
          "각 상태에 **어텐션 가중치(Attention Weight)** 를 곱해 모두 더해요."),
    warn("헷갈리기 쉬운 점", "**어텐션 점수(Attention Score)** 는 확률이 아니에요. 음수도 나와요. 확률은 **소프트맥스(Softmax)** 뒤예요.",
         "**문맥 벡터(Context Vector)** 는 걸음마다 새로 만들어요. 한 번 만들고 끝이 아니에요.",
         "여기서 더하는 것은 벡터예요. 칸마다 따로 더해요."),
    recap("**어텐션(Attention)** 네 줄: 점수, **소프트맥스(Softmax)**, **가중합(Weighted Sum)**, 예측",
          "3.6, 0.8, 0.5, 0.4 → 0.87, 0.05, 0.04, 0.04", "가중치 0.62, 0.14, 0.12, 0.12 로 섞으면 **문맥 벡터(Context Vector)** (1.36, 0.40)",
          "오늘의 용어: 어텐션(Attention), 어텐션 점수, 어텐션 분포, 문맥 벡터, 가중합, 소프트맥스"),
]})

# ---------------------------------------------------------------- w4-4
t = [T("정렬", "Alignment", "원문의 어느 단어가 번역문의 어느 단어를 만들었는지 짝지은 것이에요."),
     T("해석 가능성", "Interpretability", "모델이 무엇을 보고 그렇게 했는지 사람이 들여다볼 수 있는 성질이에요."),
     T("어텐션 가중치", "Attention Weight", "소스 각 자리에 얼마만큼 주의를 줄지 정한 0에서 1 사이 비중이에요."),
     T("쿼리", "Query", "지금 무엇을 찾고 있는지 나타내는 벡터예요."),
     T("밸류", "Value", "뽑히면 건네줄 내용에 해당하는 벡터예요."),
     T("내적", "Dot Product", "두 벡터를 짝끼리 곱해 모두 더한 값. 같은 쪽을 볼수록 커져요.")]
U.append({"id": "w4-4", "title": "어텐션이 주는 네 가지와 정렬", "goal": "어텐션의 이득 네 가지를 들고, 점수 함수 세 가지를 구별할 수 있어요.", "terms": t, "slides": [
    title("어텐션이 주는 것", "성능, 병목 해소, 짧은 길, 그리고 들여다보기"),
    goal("**어텐션(Attention)** 의 이득 네 가지", "**정렬(Alignment)** 이 공짜로 배워지는 이야기", "점수 함수 세 가지와 일반적인 정의"),
    pts("네 가지 이득 (N4 p.25)", "1 성능: 어텐션을 붙이자마자 좋아졌고, 긴 문장에서 특히 컸어요",
        "2 병목 없음: **디코더(Decoder)** 가 요약을 거치지 않고 소스를 직접 읽어요",
        "3 짧은 기울기 길: 출력의 모든 자리에서 입력까지 직통이라 **기울기 소실(Vanishing Gradient)** 을 비켜 가요",
        "4 **해석 가능성(Interpretability)**: **어텐션 가중치(Attention Weight)** 가 모델이 본 곳의 그림이 돼요"),
    fig("가중치 표가 곧 정렬 그림 (N4 p.26)", SVG_ALIGN, "행은 만들 단어, 열은 소스 단어. 진한 칸이 **어텐션 가중치(Attention Weight)** 가 큰 곳이에요", 3),
    ana("아무도 안 가르친 짝 맞추기", "영어와 우리말 문장 쌍을 아주 많이 보다 보면, 누가 알려 주지 않아도 you 와 '너를' 이 늘 함께 나온다는 것을 저절로 알게 돼요.",
        [("많은 문장 쌍", "번역 학습 데이터"), ("저절로 알게 되는 짝", "**정렬(Alignment)**"), ("아무도 안 알려 줌", "정렬을 따로 가르치지 않음")]),
    pts("정렬은 부산물 (N4 p.26)", "통계 **기계 번역(Machine Translation (MT))** 은 **정렬(Alignment)** 모델을 따로 만들었어요. 그 자체가 연구 분야였어요",
        "**어텐션(Attention)** 은 번역을 배우다 보니 **정렬(Alignment)** 을 덤으로 배웠어요", "아무도 감독하지 않았어요. 슬라이드 말로 Alignment Learned for Free"),
    cmp_("점수 내는 세 가지 방법 (N4 p.27)", ["이름", "식", "성질"],
         [["내적", "$s^{\\top} h$", "가장 싸요. 대신 두 벡터 크기가 같아야 해요"],
          ["쌍선형 (Luong)", "$s^{\\top} W h$", "배우는 행렬 W 를 끼워 넣어요"],
          ["덧셈형 (Bahdanau)", "작은 MLP", "표현력은 크고 계산은 비싸요"],
          ["**트랜스포머(Transformer)**", "**내적(Dot Product)** 을 쓰되 나눠요", "왜 나누는지는 다음 단원에서"]]),
    pts("어텐션의 일반적인 정의 (N4 p.28)", "번역을 지우고 보면 정의가 아주 넓어져요",
        "값들의 묶음과 **쿼리(Query)** 하나가 있을 때, 값들의 **가중합(Weighted Sum)** 을 만드는 일이에요",
        "비중은 **쿼리(Query)** 가 정해요. 곧 질문이 무엇을 뽑아낼지 고르는 거예요"),
    ana("같은 자료, 다른 질문", "같은 책 한 권을 두고 '주인공은 누구지?' 라고 물을 때와 '배경은 어디지?' 라고 물을 때, 밑줄 치는 부분이 달라져요.",
        [("책 내용", "**밸류(Value)** 들"), ("지금 던지는 질문", "**쿼리(Query)**"), ("밑줄 친 곳을 모은 요약", "**문맥 벡터(Context Vector)**")]),
    eng("외워 쓸 한 줄", "어텐션은 값들의 묶음과 쿼리(Query)가 주어졌을 때, 쿼리에 따라 정해지는 가중치로 값들의 가중합을 만드는 일반적인 기법이다.",
        "번역을 지운 정의예요. 뒤의 셀프 어텐션도 이 정의 안에 들어가요.", "'값 묶음 + 쿼리 → 가중합' 세 낱말로 외워요"),
    pts("Check Yourself 1 (N4 p.29)", "1 고정 크기 벡터가 왜 긴 문장에서 더 아픈가요",
        "2 **교사 강요(Teacher Forcing)** 에서 학습 때와 시험 때가 정확히 무엇이 다른가요",
        "3 k = 1 인 **빔 서치(Beam Search)** 는 무엇과 같고, 왜 길이로 나누나요",
        "4 어텐션 네 줄을 외워서 쓰고, 어느 줄이 합을 1 로 만드나요",
        "5 직통 연결이 **기울기(Gradient)** 에 왜 좋은가요"),
    check("**해석 가능성(Interpretability)** 이 어텐션의 이득인 까닭은?",
          ["**어텐션 가중치(Attention Weight)** 를 보면 모델이 어디를 봤는지 알 수 있어서", "계산이 빨라서", "파라미터가 적어서", "학습 데이터가 적게 들어서"], 0,
          "가중치 표를 그리면 **정렬(Alignment)** 그림이 돼요. 딥러닝에서는 드문 공짜 선물이에요."),
    check("가장 싸지만 두 벡터의 크기가 같아야 하는 점수 함수는?",
          ["**내적(Dot Product)**", "쌍선형(Luong)", "덧셈형(Bahdanau)", "**소프트맥스(Softmax)**"], 0,
          "**내적(Dot Product)** 은 짝끼리 곱해 더하니 칸 수가 같아야 해요."),
    warn("헷갈리기 쉬운 점", "**정렬(Alignment)** 은 따로 배우는 것이 아니라 번역을 배우다 생긴 부산물이에요.",
         "**어텐션 가중치(Attention Weight)** 그림은 참고 자료예요. 모델의 속마음을 완전히 설명해 주지는 않아요.",
         "**쿼리(Query)** 와 **밸류(Value)** 는 다음 단원에서 정식으로 다시 정의해요."),
    recap("이득 넷: 성능, 병목 해소, 짧은 **기울기(Gradient)** 길, **해석 가능성(Interpretability)**",
          "**정렬(Alignment)** 은 감독 없이 공짜로 배워져요", "점수 셋: **내적(Dot Product)**, 쌍선형, 덧셈형. 트랜스포머는 내적을 써요",
          "오늘의 용어: 정렬(Alignment), 해석 가능성, 어텐션 가중치, 쿼리(Query), 밸류(Value), 내적(Dot Product)"),
]})

# ---------------------------------------------------------------- w4-5
t = [T("셀프 어텐션", "Self-Attention", "한 문장이 자기 자신에게 어텐션을 거는 것이에요.",
       "쿼리, 키, 밸류가 모두 같은 문장에서 나와요. 토큰마다 서로에게 질문을 던져요."),
     T("크로스 어텐션", "Cross-Attention", "쿼리는 한쪽 문장, 키와 밸류는 다른 문장에서 오는 어텐션이에요."),
     T("쿼리", "Query", "내가 지금 무엇을 찾는지 적은 벡터예요."),
     T("키", "Key", "내가 무엇을 내걸고 있는지 적은 벡터예요."),
     T("밸류", "Value", "내가 뽑히면 건네줄 내용이에요."),
     T("순환 신경망", "Recurrent Neural Network (RNN)", "한 토큰씩 읽으며 메모장에 요약을 고쳐 쓰는 신경망이에요.")]
U.append({"id": "w4-5", "title": "셀프 어텐션과 쿼리, 키, 밸류", "goal": "셀프 어텐션과 크로스 어텐션을 구별하고, Q K V 가 무엇인지 말할 수 있어요.", "terms": t, "slides": [
    title("자기 자신에게 묻기", "쿼리, 키, 밸류 세 낱말"),
    goal("**순환 신경망(RNN)** 이 왜 없어도 되는지", "**셀프 어텐션(Self-Attention)** 과 **크로스 어텐션(Cross-Attention)** 의 차이", "**쿼리(Query)**, **키(Key)**, **밸류(Value)** 의 뜻"),
    pts("순환이 꼭 필요할까 (N4 p.32)", "**어텐션(Attention)** 은 이미 출력과 입력을 직통으로 이어 줘요",
        "그러면 **순환 신경망(RNN)** 이 남아서 하는 일은 무엇일까요", "한 문장 안에서 정보를 섞는 일이에요. 그건 어텐션도 할 수 있어요",
        "순환을 없애면 두 자리 사이 최대 거리가 n 에서 1 로 줄어요"),
    cmp_("크로스와 셀프 (N4 p.33)", ["", "**쿼리(Query)**", "**키(Key)** 와 **밸류(Value)**"],
         [["**크로스 어텐션(Cross-Attention)**", "디코더 문장", "인코더 문장"],
          ["**셀프 어텐션(Self-Attention)**", "같은 문장", "같은 문장"],
          ["달라지는 것", "벡터가 어디서 오는지뿐", "계산 방법은 똑같아요"]]),
    ana("도서관에서 책 찾기", "딱 한 권만 빌려 오는 대신, 관련 있는 책 네 권을 모두 훑어보고 중요한 책을 더 오래 읽어 노트 한 장으로 정리해 오는 거예요.",
        [("찾고 싶은 주제", "**쿼리(Query)**"), ("책등에 붙은 제목", "**키(Key)**"), ("책 속 내용", "**밸류(Value)**"), ("정리한 노트 한 장", "**문맥 벡터(Context Vector)**")]),
    fig("한 토큰이 맡는 세 역할 (N4 p.34)", SVG_QKV, "같은 입력 벡터에서 배운 행렬 세 개로 **쿼리(Query)**, **키(Key)**, **밸류(Value)** 를 만들어요", 3),
    form("세 역할을 만드는 식", r"q_i = W^{Q} x_i,\qquad k_i = W^{K} x_i,\qquad v_i = W^{V} x_i",
         [(r"x_i", "i 번째 토큰의 입력 벡터"), (r"W^{Q}", "**쿼리(Query)** 를 만드는 배운 행렬"),
          (r"W^{K}", "**키(Key)** 를 만드는 배운 행렬"), (r"W^{V}", "**밸류(Value)** 를 만드는 배운 행렬")],
         "행렬 세 개는 모든 자리에서 똑같이 다시 써요. 그래서 문장이 길어져도 **파라미터(Parameter)** 가 늘지 않아요."),
    steps("한 쿼리를 따라가 보기 (N4 p.35)", [
        "문장: Zuko made his uncle tea. 지금 볼 토큰은 his",
        "his 의 **쿼리(Query)** 를 모든 토큰의 **키(Key)** 와 **내적(Dot Product)** 해서 점수를 내요",
        "**소프트맥스(Softmax)** 로 눌러 합이 1 인 가중치를 만들어요",
        "그 가중치로 모든 토큰의 **밸류(Value)** 를 **가중합(Weighted Sum)** 해요",
        "결과가 his 자리의 새 벡터가 돼요. uncle 쪽 가중치가 컸다면 his 가 uncle 정보를 품어요",
    ], "토큰마다 자기가 신경 쓴 토큰들의 섞음으로 다시 쓰여요", "3단계는 2절의 점수, 정규화, 섞기와 똑같아요"),
    pts("교수님이 짚은 곳", "교수님: 이 세 개념(**쿼리(Query)**, **키(Key)**, **밸류(Value)**)을 이해해야 트랜스포머를 이해할 수 있어요",
        "슬라이드 p.20 의 비유: 파이썬 사전은 키 하나가 딱 맞으면 값 하나를 줘요",
        "**어텐션(Attention)** 은 모든 **키(Key)** 에 조금씩 맞고, 값들을 섞어서 줘요"),
    check("**셀프 어텐션(Self-Attention)** 이 **크로스 어텐션(Cross-Attention)** 과 다른 점은?",
          ["Q, K, V 가 모두 같은 문장에서 온다", "소프트맥스를 안 쓴다", "가중합을 안 한다", "점수를 안 낸다"], 0,
          "계산은 똑같고, 벡터가 어디서 오는지만 달라요."),
    check("한 토큰이 '내가 무엇을 내걸고 있는지' 를 적은 벡터는?",
          ["**키(Key)**", "**쿼리(Query)**", "**밸류(Value)**", "**문맥 벡터(Context Vector)**"], 0,
          "**키(Key)** 는 간판이에요. **쿼리(Query)** 는 찾는 것, **밸류(Value)** 는 건네줄 내용이에요."),
    warn("헷갈리기 쉬운 점", "한 토큰이 **쿼리(Query)**, **키(Key)**, **밸류(Value)** 세 역할을 동시에 맡아요. 셋 중 하나가 아니에요.",
         "**셀프 어텐션(Self-Attention)** 도 자기 자신을 포함해서 봐요.",
         "행렬 세 개는 위치마다 다른 게 아니라 모든 위치가 같은 것을 써요."),
    recap("**순환 신경망(RNN)** 이 하던 '문장 안 섞기' 를 어텐션이 대신해요",
          "**셀프 어텐션(Self-Attention)** 은 Q, K, V 가 같은 문장, **크로스 어텐션(Cross-Attention)** 은 다른 문장",
          "**쿼리(Query)** 무엇을 찾나, **키(Key)** 무엇을 내거나, **밸류(Value)** 무엇을 건네나",
          "오늘의 용어: 셀프 어텐션, 크로스 어텐션, 쿼리(Query), 키(Key), 밸류(Value), RNN"),
]})

# ---------------------------------------------------------------- w4-6
t = [T("스케일드 닷프로덕트 어텐션", "Scaled Dot-Product Attention", "내적 점수를 루트 d_k 로 나눈 뒤 소프트맥스를 하는 어텐션이에요."),
     T("병렬화", "Parallelization", "자리마다 차례로 기다리지 않고 한꺼번에 계산하는 것이에요."),
     T("내적", "Dot Product", "두 벡터를 짝끼리 곱해 모두 더한 값이에요."),
     T("소프트맥스", "Softmax", "점수를 모두 더해 1이 되는 확률 파이로 나누는 함수예요."),
     T("텐서", "Tensor", "숫자를 여러 줄, 여러 칸으로 담은 묶음이에요. shape 으로 크기를 읽어요.")]
U.append({"id": "w4-6", "title": "행렬 한 번에, 그리고 루트 d_k", "goal": "Q K V 행렬 곱의 shape 을 따라가고, 왜 루트 d_k 로 나누는지 설명할 수 있어요.", "terms": t, "slides": [
    title("한꺼번에 계산하기", "행렬 세 번 곱하면 끝"),
    goal("행렬 형태 **스케일드 닷프로덕트 어텐션(Scaled Dot-Product Attention)** 식", "Q, K, V **텐서(Tensor)** 와 점수 행렬의 shape", "왜 루트 d_k 로 나누는지"),
    ana("점수를 확률 파이로 나누기", "**소프트맥스(Softmax)** 는 점수를 모두 더해 1이 되는 확률 파이로 나눠요. 그런데 한 점수만 엄청나게 크면 파이 한 조각이 거의 전부를 차지해요.",
        [("파이 한 조각이 거의 전부", "가중치가 거의 0 아니면 1"), ("나머지 조각이 0 에 가까움", "**기울기(Gradient)** 가 거의 사라짐"), ("점수를 미리 작게 줄이기", "루트 d_k 로 나누기")]),
    fig("Q K V 를 따라가는 shape (N4 p.37)", SVG_SHAPE, "$QK^{\\top}$ 가 n x n 점수, **소프트맥스(Softmax)** 뒤 A, 그리고 $AV$ 가 출력 O 예요", 4),
    form("한 줄로 쓴 어텐션 (N4 p.37)", r"\mathrm{Attention}(Q, K, V) = \mathrm{softmax}\!\left(\frac{QK^{\top}}{\sqrt{d_k}}\right) V",
         [(r"Q", "**쿼리(Query)** 를 세로로 쌓은 행렬. n x d_k"), (r"K^{\top}", "**키(Key)** 행렬을 눕힌 것. d_k x n"),
          (r"QK^{\top}", "자리끼리의 **내적(Dot Product)** 점수. n x n"), (r"\sqrt{d_k}", "점수를 적당한 크기로 줄이는 나눗셈"),
          (r"\mathrm{softmax}", "행마다 합이 1 이 되게 눌러 담기"), (r"V", "**밸류(Value)** 행렬. n x d_v")],
         "자리마다 도는 반복문이 없어요. 행렬 곱 세 번이면 문장 전체가 한 번에 끝나요."),
    steps("shape 따라가기", [
        "토큰 n = 4, d_k = 8, d_v = 8 이라고 해요",
        "Q 는 (4, 8), K 는 (4, 8) 이라 $K^{\\top}$ 는 (8, 4)",
        "$QK^{\\top}$ 는 (4, 8) x (8, 4) = (4, 4). 가운데 8 끼리 맞아요",
        "**소프트맥스(Softmax)** 를 행마다 걸면 A 도 (4, 4), 행 합은 1",
        "$AV$ 는 (4, 4) x (4, 8) = (4, 8). 입력과 같은 자리 수, 같은 칸 수예요",
    ], "출력 **텐서(Tensor)** O 의 shape 은 (n, d_v) = (4, 8)", "shape 은 (행, 열) 로 읽어요. 3주차 shape 맞추기와 같은 요령이에요"),
    pts("왜 이게 빠른가 (N4 p.37)", "**순환 신경망(RNN)** 은 t 번째를 구하려면 t-1 을 기다려야 해요",
        "**셀프 어텐션(Self-Attention)** 은 자리마다 기다릴 것이 없어요", "그래서 GPU 가 한 번에 계산해요. 이것이 **병렬화(Parallelization)** 예요",
        "교수님: 패러럴이 핵심이에요. 병렬로 처리하는 파이프라인을 늘 머릿속에 그려 주세요"),
    pts("점수가 커지면 생기는 일 (N4 p.38)", "q 와 k 의 칸이 서로 무관하고 분산이 1 이면, **내적(Dot Product)** 의 분산은 d_k 가 돼요",
        "d_k = 512 면 점수가 보통 플러스마이너스 20 쯤까지 벌어져요", "그런 점수에 **소프트맥스(Softmax)** 를 걸면 거의 원-핫이 되고 **기울기(Gradient)** 가 거의 0 이에요"),
    steps("손계산: 나누기 전과 뒤", [
        "d_k = 64 라고 하면 루트 64 = 8 이에요",
        "점수가 24, 8, 16 이라고 해 봐요",
        "그냥 **소프트맥스(Softmax)**: 가장 큰 칸이 약 0.9997 로 거의 1 이에요",
        "8 로 나누면 3, 1, 2 가 돼요",
        "이제 **소프트맥스(Softmax)**: 약 0.665, 0.090, 0.245 로 부드러워요",
    ], "나누기 전 0.9997 → 나눈 뒤 0.665. 기울기가 살아 있어요", "루트 8 ≈ 2.83, 루트 64 = 8, 루트 512 ≈ 22.63"),
    check("$QK^{\\top}$ 의 shape 은? (토큰 n 개, 차원 d_k)",
          ["n x n", "n x d_k", "d_k x d_k", "1 x n"], 0, "자리마다 자리마다의 점수라서 n x n 이에요. 행 합이 1 이 되게 눌러 담아요."),
    check("루트 d_k 로 나누지 않으면 무슨 일이 생기나요?",
          ["점수가 커져 **소프트맥스(Softmax)** 가 포화되고 기울기가 사라져요", "계산이 느려져요", "shape 이 안 맞아요", "값이 음수가 돼요"], 0,
          "슬라이드 말로 a saturated softmax has almost no gradient 예요."),
    warn("헷갈리기 쉬운 점", "나누는 것은 d_k 가 아니라 루트 d_k 예요.",
         "d_k 는 **쿼리(Query)** 와 **키(Key)** 의 칸 수, d_v 는 **밸류(Value)** 의 칸 수예요. 같을 수도 다를 수도 있어요.",
         "코드에서 막히면 **텐서(Tensor)** 의 shape 부터 찍어 봐요. 3주차에서 배운 그 요령이에요."),
    recap("**스케일드 닷프로덕트 어텐션(Scaled Dot-Product Attention)**: 내적, 루트 d_k 로 나누기, 소프트맥스, 가중합",
          "shape: (n, d_k) x (d_k, n) = (n, n), 그다음 (n, n) x (n, d_v) = (n, d_v)",
          "반복문이 없어서 **병렬화(Parallelization)** 가 돼요. 교수님이 핵심이라고 한 부분이에요",
          "오늘의 용어: 스케일드 닷프로덕트 어텐션, 병렬화, 내적(Dot Product), 소프트맥스, 텐서(Tensor)"),
]})

# ---------------------------------------------------------------- w4-7
t = [T("순열 등변성", "Permutation Equivariance", "입력 순서를 섞으면 출력도 똑같이 섞일 뿐, 내용은 그대로인 성질이에요.",
       "셀프 어텐션은 순서를 모른다는 뜻이에요. 그래서 위치 정보를 따로 넣어 줘야 해요."),
     T("위치 인코딩", "Positional Encoding", "자리마다 벡터를 하나씩 만들어 토큰 벡터에 더해 주는 것이에요."),
     T("사인 코사인 위치 인코딩", "Sinusoidal Positional Encoding", "사인과 코사인 물결로 자리 벡터를 만드는 원래 방식이에요."),
     T("로프", "RoPE", "쿼리와 키를 자리에 비례해 돌려 상대 거리만 남기는 요즘 방식이에요."),
     T("위치별 피드포워드 신경망", "Position-wise Feed-Forward Network (FFN)", "자리마다 따로 거는 두 층짜리 MLP 예요."),
     T("인과 마스킹", "Causal Masking", "아직 만들지 않은 뒤쪽 토큰을 못 보게 막는 것이에요."),
     T("자기회귀", "Autoregressive", "앞에서 만든 것을 다시 넣어 다음 것을 만드는 방식이에요.")]
U.append({"id": "w4-7", "title": "장벽 셋과 부품 셋", "goal": "셀프 어텐션의 구멍 세 개와 그것을 메우는 부품 세 개를 짝지을 수 있어요.", "terms": t, "slides": [
    title("장벽 셋, 부품 셋", "순서, 비선형, 미래 가리기"),
    goal("**순열 등변성(Permutation Equivariance)** 이 왜 문제인지", "**위치 인코딩(Positional Encoding)** 과 **위치별 피드포워드 신경망(FFN)**", "**인과 마스킹(Causal Masking)** 이 하는 일"),
    fig("장벽 셋과 그 처방 (N4 p.39)", SVG_BARRIER, "순서를 모름 → **위치 인코딩(Positional Encoding)**, 비선형 없음 → FFN, 미래를 봄 → **인과 마스킹(Causal Masking)**", 3),
    pts("장벽 1: 순서를 몰라요 (N4 p.40)", "dog bites man 과 man bites dog 를 셀프 어텐션은 똑같이 봐요",
        "입력을 섞으면 출력도 똑같이 섞일 뿐이에요. 이것이 **순열 등변성(Permutation Equivariance)** 이에요",
        "처방: 자리마다 벡터를 만들어 첫 층 전에 토큰 벡터에 더해요. 곧 **위치 인코딩(Positional Encoding)**"),
    form("사인 코사인 위치 인코딩 (N4 p.40)", r"PE_{pos,\,2i} = \sin\!\left(\frac{pos}{10000^{2i/d}}\right),\qquad PE_{pos,\,2i+1} = \cos\!\left(\frac{pos}{10000^{2i/d}}\right)",
         [(r"pos", "몇 번째 자리인지"), (r"i", "벡터의 몇 번째 짝인지"), (r"d", "벡터의 칸 수"),
          (r"10000^{2i/d}", "짝마다 물결의 길이를 다르게 하는 값")],
         "칸마다 길이가 다른 물결을 만들어 자리를 표시해요. 이것이 **사인 코사인 위치 인코딩(Sinusoidal Positional Encoding)** 이에요."),
    steps("손계산: pos = 1, d = 4 일 때", [
        "첫 짝 i = 0: 나누는 값은 $10000^{0} = 1$",
        "sin(1 ÷ 1) = sin(1) ≈ 0.8415, cos(1) ≈ 0.5403",
        "둘째 짝 i = 1: 나누는 값은 $10000^{2/4} = 100$",
        "sin(1 ÷ 100) = sin(0.01) ≈ 0.0100, cos(0.01) ≈ 0.99995",
        "앞 짝은 빨리 흔들리고 뒤 짝은 거의 안 움직여요",
    ], "자리 1 의 벡터는 약 (0.8415, 0.5403, 0.0100, 0.99995)", "각도는 라디안으로 계산해요"),
    cmp_("위치 정보를 넣는 세 가지 (N4 p.41)", ["방식", "설명"],
         [["**사인 코사인 위치 인코딩(Sinusoidal Positional Encoding)**", "2017년 원래 방식. 물결로 자리를 표시해요"],
          ["학습된 위치 임베딩", "자리마다 **임베딩(Embedding)** 을 배우게 해요"],
          ["**로프(RoPE)**", "q 와 k 를 자리에 비례해 돌려요. 점수가 상대 거리 i - j 에만 달려요"],
          ["요즘 흐름", "큰 모델은 대부분 **로프(RoPE)**. 문맥 창을 길게 늘이기 좋아요"]]),
    pts("장벽 2: 비선형이 없어요 (N4 p.42)", "어텐션만 쌓으면 값을 다시 평균 내는 일만 되풀이해요. 거의 선형이에요",
        "처방: 자리마다 따로 두 층짜리 MLP 를 걸어요. **위치별 피드포워드 신경망(FFN)** 이에요",
        "역할 나누기: 어텐션은 토큰 사이로 정보를 옮기고, FFN 은 토큰 하나를 바꿔요",
        "여기에 **파라미터(Parameter)** 가 가장 많이 살아요. 가운데 칸 수는 보통 4d 예요"),
    steps("손계산: FFN 파라미터가 왜 많은가", [
        "d = 512, 가운데 칸 수 d_ff = 4 x 512 = 2048",
        "첫 층 가중치: 512 x 2048 = 1,048,576 개",
        "둘째 층 가중치: 2048 x 512 = 1,048,576 개",
        "합치면 2,097,152 개",
        "어텐션 쪽 네 행렬은 4 x 512 x 512 = 1,048,576 개",
    ], "**위치별 피드포워드 신경망(FFN)** 이 어텐션의 약 2배예요", "편향 항은 빼고 가중치만 셌어요"),
    fig("미래를 가리는 삼각형 (N4 p.43)", SVG_MASK, "행은 지금 보는 토큰, 열은 바라보는 토큰. 오른쪽 위는 **소프트맥스(Softmax)** 전에 막아요", 3),
    ana("자판이 미리 답을 알면 시시해요", "휴대폰 자판이 다음 단어를 추천할 때, 아직 내가 치지도 않은 뒷글자를 미리 알고 있다면 추천 문제가 전혀 어렵지 않겠죠.",
        [("아직 안 친 뒷글자", "아직 만들지 않은 미래 토큰"), ("미리 알면 시시함", "과제가 사소해져 배울 것이 없음"), ("못 보게 가리기", "**인과 마스킹(Causal Masking)**")]),
    pts("장벽 3: 미래를 봐요 (N4 p.43)", "**언어 모델(Language Model (LM))** 이 아직 안 만든 토큰을 보면 안 돼요",
        "처방: 뒤쪽 자리 점수를 **소프트맥스(Softmax)** 전에 마이너스 무한대로 두면 가중치가 정확히 0 이 돼요",
        "이렇게 앞만 보며 하나씩 만드는 방식을 **자기회귀(Autoregressive)** 라고 해요. GPT 가 **자기회귀(Autoregressive)** 예요",
        "인코더는 이 가리개를 쓰지 않고 양쪽을 다 봐요. 삼각형 하나가 BERT 식과 GPT 식을 갈라요"),
    pts("최소 블록 (N4 p.44)", "임베딩 + **위치 인코딩(Positional Encoding)** → 마스크 **셀프 어텐션(Self-Attention)** → FFN",
        "이것을 N 번 쌓으면 이미 돌아가요", "다음 단원의 멀티 헤드, 잔차, 정규화는 깊게 쌓아도 학습되게 만드는 장치예요"),
    check("**인과 마스킹(Causal Masking)** 을 소프트맥스 뒤가 아니라 앞에 거는 까닭은?",
          ["앞에서 막아야 가중치가 정확히 0 이 되고 합이 1 로 맞아서", "계산이 빨라서", "shape 때문에", "기울기가 커져서"], 0,
          "뒤에서 0 으로 만들면 남은 가중치의 합이 1 이 아니게 돼요."),
    check("**위치별 피드포워드 신경망(FFN)** 이 하는 일은?",
          ["자리마다 따로 걸어 토큰 하나를 바꿔요", "토큰끼리 정보를 섞어요", "순서를 알려 줘요", "미래를 가려요"], 0,
          "어텐션이 옮기고 FFN 이 계산해요. FFN 은 자리를 가로질러 섞지 않아요."),
    warn("헷갈리기 쉬운 점", "**위치 인코딩(Positional Encoding)** 은 곱하는 게 아니라 더해요. 그리고 첫 층 전에 한 번 더해요.",
         "**순열 등변성(Permutation Equivariance)** 은 '순서를 무시한다' 가 아니라 '섞으면 똑같이 섞여 나온다' 예요.",
         "**인과 마스킹(Causal Masking)** 은 디코더 쪽 이야기예요. 인코더는 양쪽을 봐요."),
    recap("장벽 셋: 순서 모름, 비선형 없음, 미래를 봄",
          "부품 셋: **위치 인코딩(Positional Encoding)**, **위치별 피드포워드 신경망(FFN)**, **인과 마스킹(Causal Masking)**",
          "pos = 1, d = 4 면 (0.8415, 0.5403, 0.0100, 0.99995). 요즘 큰 모델은 **로프(RoPE)** 를 써요",
          "오늘의 용어: 순열 등변성, 위치 인코딩, 사인 코사인 위치 인코딩, RoPE, FFN, 인과 마스킹, 자기회귀"),
]})

# ---------------------------------------------------------------- w4-8
t = [T("멀티 헤드 어텐션", "Multi-Head Attention (MHA)", "어텐션을 여러 개로 나눠 서로 다른 관점에서 보게 하는 것이에요."),
     T("헤드", "Head", "따로 어텐션을 한 번 돌리는 작은 어텐션 하나예요."),
     T("셀프 어텐션", "Self-Attention", "한 문장이 자기 자신에게 거는 어텐션이에요."),
     T("어텐션 분포", "Attention Distribution", "점수를 소프트맥스로 눌러 만든, 다 더하면 1인 가중치 목록이에요."),
     T("파라미터", "Parameter", "학습으로 정해지는 숫자들. 가중치와 편향 항이에요.")]
U.append({"id": "w4-8", "title": "멀티 헤드 어텐션", "goal": "헤드를 여러 개 쓰는 까닭과 계산량이 왜 그대로인지 숫자로 말할 수 있어요.", "terms": t, "slides": [
    title("헤드를 여러 개", "질문 하나로는 부족해요"),
    goal("왜 **헤드(Head)** 하나로는 부족한지", "**셀프 어텐션(Self-Attention)** 을 나눈 **멀티 헤드 어텐션(Multi-Head Attention (MHA))** 의 구조", "왜 계산량과 파라미터 수가 그대로인지"),
    pts("한 헤드의 한계 (N4 p.46)", "**어텐션 분포(Attention Distribution)** 하나는 한 가지 방식으로만 평균을 내요",
        "그런데 한 단어는 보통 여러 가지를 동시에 봐야 해요", "문법상 주어, 가까운 꾸밈말, 같은 것을 가리키는 대명사, 문단의 주제",
        "질문이 여러 개니까 **셀프 어텐션(Self-Attention)** 을 **헤드(Head)** 여러 개로 나눠서 해요"),
    ana("같은 자료, 다른 질문", "같은 책 한 권을 두고 '주인공은 누구지?' 라고 물을 때와 '배경은 어디지?' 라고 물을 때, 밑줄 치는 부분이 달라져요.",
        [("책 내용", "**밸류(Value)** 들"), ("서로 다른 질문 여러 개", "여러 **헤드(Head)**"), ("밑줄 친 곳들을 모아 정리", "이어 붙인 뒤 한 번 더 곱하기")]),
    fig("헤드로 나누고 다시 합치기 (N4 p.47)", SVG_MHA, "전체 차원 d 를 h 로 나눠 **헤드(Head)** 마다 d/h 칸씩 쓰고, 이어 붙여 $W^{O}$ 로 되돌려요", 4),
    form("멀티 헤드 어텐션", r"\mathrm{MHA}(X) = \mathrm{Concat}(\mathrm{head}_1, \ldots, \mathrm{head}_h)\, W^{O}",
         [(r"\mathrm{head}_j", "j 번째 **헤드(Head)**. d/h 칸에서 어텐션을 한 번 돌려요"),
          (r"h", "**헤드(Head)** 의 개수"), (r"\mathrm{Concat}", "결과들을 옆으로 이어 붙이기"),
          (r"W^{O}", "이어 붙인 것을 원래 칸 수로 되돌리는 행렬")],
         "낮은 차원 여러 곳에서 따로 보고, 이어 붙여 한 번에 섞어요."),
    steps("손계산: 헤드 하나의 칸 수", [
        "원래 논문: d = 512, **헤드(Head)** 수 h = 8",
        "헤드 하나가 쓰는 칸 수는 d ÷ h = 512 ÷ 8 = 64",
        "헤드 8 개의 칸을 다 더하면 8 x 64 = 512",
        "곧 전체 칸 수는 그대로예요. 나눠 쓴 것뿐이에요",
    ], "헤드 하나가 64 칸. 전체 512 칸은 변하지 않아요", "d = 512, h = 8 은 슬라이드에 적힌 값이에요"),
    steps("손계산: 파라미터 수가 왜 그대로인가", [
        "어텐션의 행렬은 $W^{Q}, W^{K}, W^{V}, W^{O}$ 네 개예요",
        "각각 d x d = 512 x 512 = 262,144 개",
        "네 개 합: 4 x 262,144 = 1,048,576 개",
        "헤드를 8 개로 쪼개도 조각들을 합치면 같은 d x d 라서 개수가 같아요",
        "참고: FFN 쪽은 2 x 512 x 2048 = 2,097,152 개로 약 2배예요",
    ], "헤드를 늘려도 **파라미터(Parameter)** 수는 1,048,576 개 그대로예요", "편향 항은 빼고 가중치만 셌어요"),
    pts("헤드가 실제로 배우는 것 (N4 p.48)", "BERT 를 뜯어본 연구들이 있어요",
        "앞 토큰이나 뒤 토큰만 따라가는 헤드", "문법 관계를 따라가는 헤드, 드문 단어를 가리키는 헤드",
        "거의 아무것도 안 배워서 떼어 내도 되는 헤드도 꽤 많아요"),
    pts("교수님이 짚은 곳", "헤드를 여러 개 쓴다고 전체 차원을 키우는 게 아니에요",
        "전체 차원을 h 로 나눠서 서로 다른 관점으로 보는 거예요", "계산 수는 똑같아요. 그래서 h > 1 은 다툴 일이 없어요"),
    check("d = 512, **헤드(Head)** 8 개일 때 헤드 하나의 차원은?",
          ["64", "512", "4096", "8"], 0, "512 ÷ 8 = 64 예요. 8 x 64 를 더하면 다시 512 가 돼요."),
    check("**멀티 헤드 어텐션(Multi-Head Attention (MHA))** 이 '공짜' 라고 하는 까닭은?",
          ["차원을 나눠 쓰므로 전체 계산량과 **파라미터(Parameter)** 수가 같아서", "헤드마다 학습을 안 해서", "소프트맥스를 한 번만 해서", "행렬이 하나라서"], 0,
          "헤드마다 d/h 칸만 쓰니 합쳐도 원래와 같아요. 관점만 여러 개 얻어요."),
    warn("헷갈리기 쉬운 점", "**헤드(Head)** 를 늘려도 차원이 커지는 게 아니에요. 나눠 쓰는 거예요.",
         "이어 붙인 뒤 $W^{O}$ 를 한 번 더 곱해요. 이어 붙이고 끝이 아니에요.",
         "헤드마다 하는 일은 그냥 **셀프 어텐션(Self-Attention)** 한 번이에요. 새 계산이 아니에요."),
    recap("한 **어텐션 분포(Attention Distribution)** 는 질문 하나뿐. 단어는 질문이 여럿이에요",
          "d 를 h 로 나눠 **헤드(Head)** 마다 d/h 칸. d = 512, h = 8 이면 64 칸",
          "**파라미터(Parameter)** 는 4 x d x d = 1,048,576 개로 그대로예요",
          "오늘의 용어: 멀티 헤드 어텐션(MHA), 헤드(Head), 셀프 어텐션, 어텐션 분포, 파라미터"),
]})

# ---------------------------------------------------------------- w4-9
t = [T("잔차 연결", "Residual Connection", "부분층의 입력을 출력에 그대로 더해 주는 지름길이에요."),
     T("항등 경로", "Identity Path", "아무것도 하지 않고 값을 그대로 지나가게 하는 길이에요."),
     T("층 정규화", "Layer Normalization (LayerNorm)", "토큰 하나의 숫자들을 평균 0, 분산 1 로 맞추는 것이에요."),
     T("야코비안", "Jacobian", "입력 여러 개, 출력 여러 개인 함수의 미분을 모은 표예요."),
     T("크로스 어텐션", "Cross-Attention", "쿼리는 디코더, 키와 밸류는 인코더에서 오는 어텐션이에요."),
     T("인코더", "Encoder", "입력을 양쪽으로 다 보며 읽는 쪽이에요."),
     T("디코더", "Decoder", "앞만 보며 출력을 한 토큰씩 만드는 쪽이에요.")]
U.append({"id": "w4-9", "title": "잔차 연결, 층 정규화, 전체 블록", "goal": "잔차와 층 정규화가 왜 필요한지 말하고, 전체 구조를 그릴 수 있어요.", "terms": t, "slides": [
    title("깊게 쌓으려면", "지름길과 자 맞추기"),
    goal("**잔차 연결(Residual Connection)** 이 기울기에 하는 일", "**층 정규화(Layer Normalization (LayerNorm))** 손계산", "**인코더(Encoder)** 블록과 **디코더(Decoder)** 블록"),
    ana("귓속말 전달 게임", "**기울기 소실(Vanishing Gradient)** 은 귓속말 전달 게임에서 말이 점점 희미해지는 것과 같아요. 그런데 맨 앞사람에게 직접 이어진 전화선이 하나 더 있다면 말이 또렷하게 닿아요.",
        [("점점 희미해지는 귓속말", "층을 지날수록 줄어드는 **기울기(Gradient)**"), ("직접 이어진 전화선", "**잔차 연결(Residual Connection)** 의 **항등 경로(Identity Path)**"), ("또렷하게 닿음", "96층을 쌓아도 1층까지 도달")]),
    pts("잔차 연결 (N4 p.49)", "부분층의 입력을 그 출력에 그대로 더해요. 식으로 x + f(x) 예요",
        "그러면 층은 '전부' 가 아니라 '바뀌는 부분' 만 배우면 돼요",
        "**야코비안(Jacobian)** 이 I + ∂f/∂x 가 되어서 I 라는 지름길이 늘 남아요",
        "이것이 없으면 깊은 **트랜스포머(Transformer)** 는 아예 학습이 안 돼요"),
    form("잔차 연결의 야코비안", r"y = x + f(x) \;\Longrightarrow\; \frac{\partial y}{\partial x} = I + \frac{\partial f}{\partial x}",
         [(r"x", "부분층의 입력"), (r"f(x)", "어텐션이나 FFN 이 만든 변화분"),
          (r"I", "단위 행렬. 3주차에서 본 '곱해도 그대로' 인 행렬이에요"), (r"\frac{\partial f}{\partial x}", "부분층 자체의 **야코비안(Jacobian)**")],
         "곱해도 그대로인 I 가 늘 더해져 있어서, 부분층이 기울기를 줄여도 **항등 경로(Identity Path)** 로 신호가 지나가요."),
    fig("정규화를 어디에 둘까 (N4 p.51)", SVG_LN, "2017년 논문은 더한 뒤에(Post-LN), 요즘 큰 모델은 부분층 앞에(Pre-LN) 둬요", 2),
    steps("손계산: 층 정규화 (N4 p.50)", [
        "토큰 하나의 숫자가 1, 2, 3, 4 라고 해요",
        "평균: (1 + 2 + 3 + 4) ÷ 4 = 2.5",
        "분산: ((1.5)² + (0.5)² + (0.5)² + (1.5)²) ÷ 4 = 5 ÷ 4 = 1.25",
        "표준편차: 루트 1.25 ≈ 1.118",
        "각 값에서 2.5 를 빼고 1.118 로 나누면 -1.342, -0.447, 0.447, 1.342",
    ], "평균 0, 분산 1 로 맞춰졌어요. 여기에 배운 감마와 베타를 곱하고 더해요", "분산은 칸 수 4 로 나눴어요"),
    pts("층 정규화가 안 하는 일 (N4 p.50)", "토큰끼리 섞지 않아요. 배치끼리도 섞지 않아요",
        "그래서 학습 때와 추론 때가 똑같이 동작해요", "문장 길이가 달라도 그대로 쓸 수 있어요",
        "**층 정규화(Layer Normalization (LayerNorm))** 는 잔차 줄기의 값이 터지지 않게 지켜 줘요"),
    cmp_("Post-LN 과 Pre-LN (N4 p.51)", ["", "Post-LN", "Pre-LN"],
         [["둔 자리", "더한 뒤", "부분층 앞"], ["나온 때", "2017년 논문", "요즘 큰 모델"],
          ["학습", "학습률 준비 운동이 꼭 필요", "잔차 길이 깨끗해서 잘 돼요"]]),
    pts("두 블록 (N4 p.52)", "**인코더(Encoder)** 블록: 셀프 어텐션 → 더하기와 정규화 → FFN → 더하기와 정규화. 양쪽을 다 봐요",
        "**디코더(Decoder)** 블록: 아래에 마스크 셀프 어텐션, 가운데에 **크로스 어텐션(Cross-Attention)**, 그 위에 FFN",
        "블록 두 종류, 부분층 네 개 또는 여섯 개. 그것이 모델의 전부예요"),
    fig("전체 구조 한 장 (N4 p.54)", SVG_FULL, "**크로스 어텐션(Cross-Attention)** 의 키와 밸류는 **인코더(Encoder)**, 쿼리는 **디코더(Decoder)** 에서 와요", 3),
    pts("원이 닫히는 자리 (N4 p.53)", "**디코더(Decoder)** 가운데 부분층이 바로 2절의 2015년 **어텐션(Attention)** 이에요",
        "이름만 **쿼리(Query)**, **키(Key)**, **밸류(Value)** 로 바꿔 쓴 것뿐이에요",
        "셀프 어텐션은 안을 보고, **크로스 어텐션(Cross-Attention)** 은 건너편을 봐요"),
    check("**잔차 연결(Residual Connection)** 이 깊은 모델에 중요한 까닭은?",
          ["**야코비안(Jacobian)** 에 I 가 남아 기울기가 앞층까지 닿아서", "파라미터가 줄어서", "계산이 빨라서", "정규화를 대신해서"], 0,
          "I + ∂f/∂x 에서 I 는 늘 1 배로 지나가는 **항등 경로(Identity Path)** 예요."),
    check("**층 정규화(Layer Normalization (LayerNorm))** 가 섞는 범위는?",
          ["토큰 하나의 칸들끼리만", "토큰끼리", "배치 전체", "문장 전체"], 0,
          "토큰 하나의 벡터를 그 안에서만 평균 0, 분산 1 로 맞춰요."),
    warn("헷갈리기 쉬운 점", "1, 2, 3, 4 의 분산은 4 로 나눈 1.25 예요. 3 으로 나누는 표본 분산이 아니에요.",
         "**크로스 어텐션(Cross-Attention)** 은 **디코더(Decoder)** 에만 있어요. **인코더(Encoder)** 에는 없어요.",
         "Pre-LN 과 Post-LN 은 성능이 아니라 학습 안정성 이야기예요."),
    recap("**잔차 연결(Residual Connection)**: y = x + f(x), **야코비안(Jacobian)** 에 I 가 남아요",
          "**층 정규화(Layer Normalization (LayerNorm))**: 1, 2, 3, 4 → -1.342, -0.447, 0.447, 1.342",
          "**인코더(Encoder)** 블록은 부분층 둘, **디코더(Decoder)** 블록은 셋(**크로스 어텐션(Cross-Attention)** 포함)",
          "오늘의 용어: 잔차 연결, 항등 경로, 층 정규화(LayerNorm), 야코비안, 크로스 어텐션, 인코더, 디코더"),
]})

# ---------------------------------------------------------------- w4-10
t = [T("이차 비용", "Quadratic Cost", "길이가 2배면 계산과 메모리가 4배가 되는 성질이에요."),
     T("트랜스포머", "Transformer", "순환 없이 어텐션만으로 쌓은 구조예요. 2017년 논문에서 나왔어요."),
     T("대규모 언어 모델", "Large Language Model (LLM)", "아주 큰 언어 모델. 교수님 말로 트랜스포머를 크게 쌓은 것이에요."),
     T("병렬화", "Parallelization", "자리마다 기다리지 않고 한꺼번에 계산하는 것이에요."),
     T("블루 점수", "BLEU", "사람 번역과 겹치는 n-gram 을 세어 번역을 채점하는 지표예요."),
     T("어텐션", "Attention", "필요한 곳을 골라 보게 해 주는 방법이에요.")]
U.append({"id": "w4-10", "title": "값을 치르는 곳, 그리고 왜 이겼나", "goal": "이차 비용을 숫자로 설명하고, 트랜스포머가 이긴 네 가지 까닭을 말할 수 있어요.", "terms": t, "slides": [
    title("모든 이점에는 청구서", "n 제곱이라는 값"),
    goal("**이차 비용(Quadratic Cost)** 이 무엇인지", "WMT14 결과가 보여 준 것", "**트랜스포머(Transformer)** 가 이긴 네 가지 까닭"),
    ana("레고 조각들이 서로 악수하기", "**토큰(Token)** 을 레고 조각이라고 했죠. 조각 n 개가 서로 한 번씩 악수하면 악수 횟수는 n 곱하기 n 이에요.",
        [("레고 조각 하나", "**토큰(Token)** 하나"), ("모든 짝이 한 번씩 악수", "점수 행렬의 한 칸"), ("악수 횟수 n x n", "**이차 비용(Quadratic Cost)**")]),
    fig("길이가 늘면 칸은 제곱으로 (N4 p.55)", SVG_QUAD, "점수 행렬은 n x n 이라 길이가 250배면 칸은 62,500배가 돼요", 3),
    pts("청구서 (N4 p.55)", "점수 행렬이 n x n 이라 계산도 메모리도 길이의 제곱으로 커져요",
        "n = 512 면 아직 싸요", "n = 128,000 이면 **대규모 언어 모델(Large Language Model (LLM))** 의 가장 큰 공학 문제가 돼요",
        "FlashAttention, 슬라이딩 윈도우, 선형 어텐션, 상태 공간 모델이 모두 이것을 노려요"),
    steps("손계산: n 제곱 비교", [
        "n = 512 일 때 점수 행렬 칸 수: 512 x 512 = 262,144",
        "n = 128,000 일 때: 128,000 x 128,000 = 16,384,000,000 (약 164억)",
        "길이 비율: 128,000 ÷ 512 = 250 배",
        "칸 비율: 250 x 250 = 62,500 배",
        "길이가 250배인데 비용은 62,500배예요",
    ], "**이차 비용(Quadratic Cost)** = 길이가 k 배면 비용은 k 제곱 배", "칸 수만 센 것이고 실제 메모리는 자료형에 따라 더 들어요"),
    pts("교수님이 짚은 곳", "세상에 공짜 점심은 없어요(no free lunch)",
        "**병렬화(Parallelization)** 로 빨라지는 대신 메모리가 n 제곱으로 늘어요", "좋은 쪽으로만 가는 길은 없다는 이야기예요"),
    fig("WMT14 영어에서 독일어 (N4 p.56)", SVG_BLEU, "GNMT 24.6, ConvS2S 25.2, **트랜스포머(Transformer)** base 27.3, big 28.4", 3),
    steps("손계산: 얼마나 좋아지고 얼마나 싸졌나", [
        "**블루 점수(BLEU)**: **트랜스포머(Transformer)** base 27.3, GNMT 24.6",
        "차이: 27.3 - 24.6 = 2.7 점",
        "학습 비용(GPU 일수): GNMT 96, 트랜스포머 base 3.3",
        "비율: 96 ÷ 3.3 ≈ 29.1 배",
        "더 좋은데 약 29배 싸요",
    ], "점수는 2.7 오르고 비용은 약 29배 줄었어요", "슬라이드 막대 그래프의 숫자를 그대로 읽었어요"),
    cmp_("왜 이겼나 (N4 p.57)", ["성질", "뜻"],
         [["**병렬화(Parallelization)**", "모든 자리를 한 번에 계산해요"],
          ["짧은 길", "어느 두 토큰이든 한 층에서 만나요"],
          ["깔끔한 확장", "똑같은 블록을 12번이고 96번이고 쌓아요"],
          ["과제를 안 가림", "글, 그림, 소리, 단백질까지 같은 블록"]]),
    pts("그 뒤로 (N4 p.57)", "같은 블록이 BERT(2018), GPT(2018부터), ViT(2020), AlphaFold(2021)가 됐어요",
        "2017년에 번역용으로 설계했는데 지금은 거의 모든 AI 가 이것으로 돌아가요",
        "교수님: **트랜스포머(Transformer)** 를 좀 크게 쌓으면 그게 **대규모 언어 모델(Large Language Model (LLM))** 이라고 봐도 돼요"),
    pts("Check Yourself 2 (N4 p.58)", "1 **셀프 어텐션(Self-Attention)** 과 2절 어텐션의 차이는 무엇인가요",
        "2 마스크를 왜 **소프트맥스(Softmax)** 앞에 걸어야 하나요",
        "3 왜 루트 d_k 로 나누고, 안 나누면 무엇이 잘못되나요",
        "4 **파라미터(Parameter)** 는 어텐션과 FFN 중 어디에 더 많은가요",
        "5 장벽 셋과 처방 셋을 말해 보세요. 6 왜 n 제곱이고, 피하려는 연구를 하나 들어 보세요"),
    eng("외워 쓸 한 줄", "트랜스포머는 순환 없이 셀프 어텐션만으로 문장을 처리해 모든 자리를 병렬로 계산하지만, 점수 행렬이 n x n 이라 길이의 제곱에 비례하는 비용을 치른다.",
        "이점과 청구서를 한 문장에 담았어요.", "'병렬로 빠르다, 대신 n 제곱' 으로 외워요"),
    check("문장 길이가 2배가 되면 어텐션의 계산과 메모리는?",
          ["약 4배", "약 2배", "그대로", "약 절반"], 0, "n x n 이라 2 x 2 = 4 배예요. 이것이 **이차 비용(Quadratic Cost)** 이에요."),
    check("**트랜스포머(Transformer)** 가 이긴 까닭으로 슬라이드가 들지 않은 것은?",
          ["파라미터가 아주 적어서", "**병렬화(Parallelization)**", "두 토큰이 한 층에서 만나서", "같은 블록을 깊게 쌓을 수 있어서"], 0,
          "슬라이드가 든 네 가지는 병렬, 짧은 길, 깔끔한 확장, 과제를 안 가림이에요."),
    warn("헷갈리기 쉬운 점", "**블루 점수(BLEU)** 27.3 과 24.6 의 차이 2.7 은 퍼센트가 아니라 점수 차예요.",
         "GPU 일수 96 과 3.3 은 학습 비용이에요. 추론 속도가 아니에요.",
         "**이차 비용(Quadratic Cost)** 은 층 수가 아니라 문장 길이 n 에 대한 이야기예요."),
    recap("점수 행렬이 n x n 이라 **이차 비용(Quadratic Cost)**. 250배 길면 62,500배",
          "WMT14: **블루 점수(BLEU)** 27.3 대 24.6, 비용은 약 29배 싸요",
          "이긴 까닭 넷: **병렬화(Parallelization)**, 짧은 길, 깔끔한 확장, 과제를 안 가림",
          "오늘의 용어: 이차 비용, 트랜스포머(Transformer), 대규모 언어 모델(LLM), 병렬화, BLEU, 어텐션(Attention)"),
]})

d = {"week": "4", "title": "4주차. 어텐션과 트랜스포머 구조", "units": U}
raw = json.dumps(d, ensure_ascii=False, indent=1)
for ch in ("—", "–", "·", "・"):
    assert ch not in raw, ch
(W / "slides_w4.json").write_text(raw, encoding="utf-8")
print("ok", len(U), sum(len(u["slides"]) for u in U))
