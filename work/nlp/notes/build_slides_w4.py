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
        % (("n2", 2) if c <= r else ("n4", 3), 96 + 48 * c, 70 + 34 * r)
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

U = []
