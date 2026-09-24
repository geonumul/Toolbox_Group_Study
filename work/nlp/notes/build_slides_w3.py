# -*- coding: utf-8 -*-
"""3주차 정리 슬라이드 (N3 Neural NLP Foundations) -> slides_w3.json
숫자는 모두 아래에서 Python 으로 계산하고 assert 로 확인한다."""
import json, math, pathlib

W = pathlib.Path(__file__).resolve().parent


def softmax(xs):
    m = max(xs)
    e = [math.exp(x - m) for x in xs]
    s = sum(e)
    return [v / s for v in e]


def matvec(M, v):
    return [sum(a * b for a, b in zip(row, v)) for row in M]


def matmat(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def relu(v):
    return [max(0.0, x) for x in v]


# ---------------------------------------------------------------- (1) 소프트맥스와 교차 엔트로피 (N3 p.7)
SC7 = [1.0, 3.0, 0.0]
E7 = [math.exp(x) for x in SC7]
P7 = softmax(SC7)
LOSS7 = -math.log(P7[1])
assert [round(e, 2) for e in E7] == [2.72, 20.09, 1.0]
assert round(sum(E7), 2) == 23.8
assert [round(p, 2) for p in P7] == [0.11, 0.84, 0.04]
assert round(LOSS7, 2) == 0.17
assert round(-math.log(0.9), 2) == 0.11 and round(-math.log(0.01), 2) == 4.61

# ---------------------------------------------------------------- (2) 창 벡터 길이 (N3 p.6)
assert 5 * 50 == 250 and 5 * 100 == 500

# ---------------------------------------------------------------- (3) 뉴런 손계산 (N3 p.9)
XN, WN, BN = [1.0, 2.0, 3.0], [0.5, -1.0, 0.5], 0.5
ZN = sum(a * b for a, b in zip(XN, WN)) + BN
XN2 = [1.0, 3.0, 1.0]
ZN2 = sum(a * b for a, b in zip(XN2, WN)) + BN
SIG = lambda z: 1 / (1 + math.exp(-z))
assert ZN == 0.5 and max(ZN, 0) == 0.5 and round(SIG(ZN), 2) == 0.62
assert ZN2 == -1.5 and max(ZN2, 0) == 0.0 and round(SIG(ZN2), 2) == 0.18
assert SIG(0) == 0.5 and round(SIG(4), 2) == 0.98 and round(SIG(-4), 2) == 0.02

# ---------------------------------------------------------------- (4) 층이 합쳐진다 (N3 p.11)
W1M, W2M, XV = [[1, 2], [0, 1]], [[1, 0], [1, 1]], [1, 1]
STEP1 = matvec(W1M, XV)
STEP2 = matvec(W2M, STEP1)
W21 = matmat(W2M, W1M)
assert STEP1 == [3, 1] and STEP2 == [3, 4]
assert W21 == [[1, 2], [1, 3]] and matvec(W21, XV) == [3, 4]
V1M = [[1, -2], [0, 1]]
assert matvec(V1M, XV) == [-1, 1]
assert matvec(W2M, relu(matvec(V1M, XV))) == [0, 1]
assert matvec(matmat(W2M, V1M), XV) == [-1, 0]

# ---------------------------------------------------------------- (5) MLP 파라미터 수 (N3 p.12)
MLP_P = 4 * 4 + 4 + 4 * 4 + 4 + 3 * 4
assert MLP_P == 52
assert 300 * 500 == 150000

# ---------------------------------------------------------------- (6) CNN 필터 (N3 p.13)
SENT = [0, 1, 0, 2, 3, -1]
FMAP = [SENT[i] + SENT[i + 1] + SENT[i + 2] for i in range(4)]
assert FMAP == [1, 3, 5, 4] and max(FMAP) == 5

# ---------------------------------------------------------------- (7) 미분과 연쇄 법칙 (N3 p.18, p.20)
assert 3 * 2 ** 2 == 12
NUDGE = (2.001 ** 3 - 2 ** 3) / 0.001
assert round(NUDGE, 3) == 12.006
assert round(2.001 ** 3, 9) == 8.012006001
CH_Z, CH_H = 3 * 1 + 1, (3 * 1 + 1) ** 2
assert CH_Z == 4 and CH_H == 16 and 2 * CH_Z * 3 == 24
NUDGE2 = ((3 * 1.001 + 1) ** 2 - 16) / 0.001
assert round(NUDGE2, 3) == 24.009
assert round((3 * 1.001 + 1) ** 2, 6) == 16.024009

# ---------------------------------------------------------------- (8) 야코비안 (N3 p.19)
assert [2 * 1, 3] == [2, 3]
JAC = [[1, 2, 0], [0, 0, 3]]
assert len(JAC) == 2 and len(JAC[0]) == 3

# ---------------------------------------------------------------- (9) 풀이 예 순전파와 역전파 (N3 p.22~24)
WE = [[1, 0, 1], [-1, 1, -2]]
XE, BE, UE = [1, 2, 3], [0, 1], [2, 3]
WX = matvec(WE, XE)
ZE = [a + b for a, b in zip(WX, BE)]
HE = relu(ZE)
SE = sum(a * b for a, b in zip(UE, HE))
assert WX == [4, -5] and ZE == [4, -4] and HE == [4, 0] and SE == 8
FP = [1 if z > 0 else 0 for z in ZE]
DELTA = [u * f for u, f in zip(UE, FP)]
DSDW = [[d * x for x in XE] for d in DELTA]
DSDX = [sum(WE[i][j] * DELTA[i] for i in range(2)) for j in range(3)]
assert FP == [1, 0] and DELTA == [2, 0]
assert DSDW == [[2, 4, 6], [0, 0, 0]] and DSDX == [2, 0, 2]
XNEW = [x - 0.1 * g for x, g in zip(XE, DSDX)]
ZNEW = [a + b for a, b in zip(matvec(WE, XNEW), BE)]
HNEW = relu(ZNEW)
SNEW = sum(a * b for a, b in zip(UE, HNEW))
assert XNEW == [0.8, 2.0, 2.8] and [round(z, 10) for z in ZNEW] == [3.6, -3.4]
assert round(SNEW, 10) == 7.2

# ---------------------------------------------------------------- (10) 노드 손계산 (N3 p.29, p.30)
assert 2 * (2 * 3) == 12 and 5 * 3 == 15
A_, B_, C_ = 1, 3, 2
Q_, R_ = A_ + B_, max(B_, C_)
assert Q_ == 4 and R_ == 3 and Q_ * R_ == 12
assert R_ == 3 and (R_ + Q_) == 7

# ---------------------------------------------------------------- (11) 수치 기울기 (N3 p.32)
f32 = lambda t: t ** 3 + 2 * t
NG = (f32(2.0001) - f32(1.9999)) / 0.0002
assert 3 * 2 ** 2 + 2 == 14 and round(NG, 4) == 14.0
assert round((3.1 ** 2 - 2.9 ** 2) / 0.2, 10) == 6.0

# ---------------------------------------------------------------- (12) 경사 하강법 한 걸음 (N3 p.17)
TH0, AL = 3.0, 0.1
TH1 = TH0 - AL * (2 * TH0)
assert TH1 == 2.4 and TH0 ** 2 == 9 and round(TH1 ** 2, 4) == 5.76

# ---------------------------------------------------------------- (13) 역전파 비용 (N3 p.31)
assert 1000000 * 1 // 86400 == 11

# ---------------------------------------------------------------- (14) n-gram (N3 p.38, p.39, p.40)
assert 400 / 1000 == 0.4 and 100 / 1000 == 0.1
assert 10000 ** 2 == 100000000 and 10000 ** 3 == 1000000000000
PATH = [0.31, 0.62, 0.57, 0.34, 0.41]
PR = 1.0
ACC = []
for p in PATH:
    PR *= p
    ACC.append(round(PR, 4))
assert ACC == [0.31, 0.1922, 0.1096, 0.0372, 0.0153]

# ---------------------------------------------------------------- (15) 퍼플렉서티 (N3 p.41, p.42)
INV = [2, 4, 8, 16]
PROD = 1
for v in INV:
    PROD *= v
PPL = PROD ** 0.25
JB = sum(math.log(v) for v in INV) / 4
assert PROD == 1024 and round(PPL, 2) == 5.66 and round(math.exp(JB), 2) == 5.66
assert round(JB, 3) == 1.733
assert round(math.log(10000), 2) == 9.21 and round(math.exp(math.log(10000))) == 10000
assert round((2 * 2) ** 0.5, 10) == 2.0 and round((4 ** 4) ** 0.25, 10) == 4.0

# ---------------------------------------------------------------- (16) 고정 윈도우 신경망 LM (N3 p.44)
assert round(1 - (0.42 + 0.21 + 0.09), 2) == 0.28

# ---------------------------------------------------------------- (17) RNN 과 기울기 (N3 p.50, p.52, p.53)
assert round(0.8 ** 20, 4) == 0.0115 and round(1.2 ** 20, 2) == 38.34
GVEC = (6.0, 8.0)
GN = math.hypot(*GVEC)
TAU = 5.0
GCLIP = tuple(TAU * g / GN for g in GVEC)
assert GN == 10.0 and GCLIP == (3.0, 4.0) and math.hypot(*GCLIP) == 5.0


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


SVG_WINDOW = (
    S0
    + '<text class="tm b1" x="240" y="42" font-size="14" text-anchor="middle">창(window) m = 2, 모두 다섯 단어</text>'
    + "".join(
        '<rect class="%s b1" x="%d" y="56" width="80" height="34"/>' % ("n2" if i == 2 else "n", 20 + 88 * i)
        for i in range(5))
    + "".join(
        '<text class="tl b1" x="%d" y="79" font-size="14" text-anchor="middle">%s</text>' % (60 + 88 * i, w)
        for i, w in enumerate(["event", "in", "Busan", "drew", "big"]))
    + "".join('<line class="e b2" x1="%d" y1="90" x2="240" y2="128"/>' % (60 + 88 * i) for i in range(5))
    + '<rect class="n3 b2" x="20" y="130" width="440" height="30"/>'
    + '<text class="tl b2" x="240" y="151" font-size="15" text-anchor="middle">이어 붙인 창 벡터 x, 길이 5d</text>'
    + '<line class="e2 b3" x1="240" y1="160" x2="240" y2="186"/><polygon class="arrow b3" points="240,192 235,182 245,182"/>'
    + '<rect class="box b3" x="140" y="194" width="200" height="32" rx="2"/>'
    + '<text class="tb b3" x="240" y="216" font-size="15" text-anchor="middle">분류기</text>'
    + '<text class="tm b3" x="240" y="252" font-size="14" text-anchor="middle">가운데 단어가 LOCATION 일 확률</text>'
    + '</svg>')

SVG_LINEAR = (
    S0
    + '<text class="tm b1" x="120" y="36" font-size="14" text-anchor="middle">직선 하나로는 못 갈라요</text>'
    + "".join('<circle class="n2 b1" cx="%d" cy="%d" r="13"/>' % (x, y)
              for x, y in [(60, 76), (180, 76), (60, 196), (180, 196)])
    + '<circle class="n4 b1" cx="120" cy="120" r="13"/><circle class="n4 b1" cx="120" cy="155" r="13"/>'
    + '<line class="e b2" x1="28" y1="184" x2="212" y2="92"/>'
    + '<text class="tm b2" x="120" y="232" font-size="14" text-anchor="middle">어떻게 그어도 실패해요</text>'
    + '<text class="tm b3" x="360" y="36" font-size="14" text-anchor="middle">휘어진 경계면 갈라져요</text>'
    + "".join('<circle class="n2 b3" cx="%d" cy="%d" r="13"/>' % (x, y)
              for x, y in [(300, 76), (420, 76), (300, 196), (420, 196)])
    + '<circle class="n4 b3" cx="360" cy="120" r="13"/><circle class="n4 b3" cx="360" cy="155" r="13"/>'
    + '<circle class="e2 b3" cx="360" cy="137" r="48" fill="none"/>'
    + '<text class="tm b3" x="360" y="232" font-size="14" text-anchor="middle">비선형성이 경계를 휘게 해요</text>'
    + '</svg>')

SVG_NEURON = (
    S0
    + "".join('<circle class="n b1" cx="34" cy="%d" r="16"/><text class="tl b1" x="34" y="%d" font-size="13" text-anchor="middle">%s</text>'
              % (70 + 60 * i, 75 + 60 * i, w) for i, w in enumerate(["x1", "x2", "x3"]))
    + "".join('<line class="e b2" x1="50" y1="%d" x2="148" y2="133"/>' % (70 + 60 * i) for i in range(3))
    + '<text class="tm b2" x="96" y="86" font-size="13" text-anchor="middle">w1</text>'
    + '<text class="tm b2" x="96" y="124" font-size="13" text-anchor="middle">w2</text>'
    + '<text class="tm b2" x="96" y="180" font-size="13" text-anchor="middle">w3</text>'
    + '<rect class="n3 b2" x="150" y="106" width="74" height="54" rx="2"/>'
    + '<text class="tl b2" x="187" y="139" font-size="17" text-anchor="middle">합 + b</text>'
    + '<text class="tm b2" x="187" y="184" font-size="13" text-anchor="middle">가중합에 편향 항</text>'
    + '<line class="e2 b3" x1="224" y1="133" x2="256" y2="133"/><polygon class="arrow b3" points="260,133 250,128 250,138"/>'
    + '<rect class="n2 b3" x="264" y="106" width="56" height="54" rx="2"/>'
    + '<text class="tl b3" x="292" y="142" font-size="20" text-anchor="middle">f</text>'
    + '<text class="tm b3" x="292" y="184" font-size="13" text-anchor="middle">활성화 함수</text>'
    + '<line class="e2 b4" x1="320" y1="133" x2="352" y2="133"/><polygon class="arrow b4" points="356,133 346,128 346,138"/>'
    + '<text class="tb b4" x="414" y="139" font-size="16" text-anchor="middle">h = f(z)</text>'
    + '<text class="tm b4" x="240" y="240" font-size="14" text-anchor="middle">z = w1x1 + w2x2 + w3x3 + b</text>'
    + '</svg>')

SVG_ACT = (
    S0
    + '<text class="tb b1" x="120" y="36" font-size="15" text-anchor="middle">시그모이드</text>'
    + '<line class="e b1" x1="26" y1="172" x2="214" y2="172"/><line class="e b1" x1="120" y1="58" x2="120" y2="192"/>'
    + '<polyline class="e2 b1" points="30,170 52,168 75,161 97,148 120,127 142,106 165,93 187,86 210,84" fill="none"/>'
    + '<text class="tm b1" x="120" y="212" font-size="13" text-anchor="middle">0 과 1 사이로 눌러 담아요</text>'
    + '<text class="tm b1" x="120" y="234" font-size="13" text-anchor="middle">양 끝에서 기울기가 거의 0</text>'
    + '<text class="tb b2" x="360" y="36" font-size="15" text-anchor="middle">ReLU</text>'
    + '<line class="e b2" x1="266" y1="172" x2="454" y2="172"/><line class="e b2" x1="348" y1="58" x2="348" y2="192"/>'
    + '<polyline class="e2 b2" points="270,172 348,172 440,80" fill="none"/>'
    + '<text class="tm b2" x="360" y="212" font-size="13" text-anchor="middle">음수는 0, 양수는 그대로</text>'
    + '<text class="tm b2" x="360" y="234" font-size="13" text-anchor="middle">양수 쪽 기울기는 늘 1</text>'
    + '</svg>')


def _mlp():
    cols = [(64, [62, 108, 154, 200]), (176, [62, 108, 154, 200]), (288, [62, 108, 154, 200]), (408, [85, 131, 177])]
    s = ""
    for b, (a, bb) in [(1, (cols[0], cols[1])), (2, (cols[1], cols[2])), (3, (cols[2], cols[3]))]:
        for y1 in a[1]:
            for y2 in bb[1]:
                s += '<line class="e b%d" x1="%d" y1="%d" x2="%d" y2="%d"/>' % (b, a[0] + 13, y1, bb[0] - 13, y2)
    for i, (x, ys) in enumerate(cols):
        cls = ["n", "n2", "n2", "n3"][i]
        bnum = [1, 1, 2, 3][i]
        for y in ys:
            s += '<circle class="%s b%d" cx="%d" cy="%d" r="13"/>' % (cls, bnum, x, y)
    for x, lab, bnum in [(64, "x", 1), (176, "h(1)", 1), (288, "h(2)", 2), (408, "y", 3)]:
        s += '<text class="tm b%d" x="%d" y="238" font-size="14" text-anchor="middle">%s</text>' % (bnum, x, lab)
    s += '<text class="tm b3" x="240" y="34" font-size="14" text-anchor="middle">입력 4, 은닉 4, 은닉 4, 출력 3</text>'
    return S0 + s + '</svg>'


SVG_MLP = _mlp()

SVG_CNN = (
    S0
    + "".join('<rect class="n b1" x="26" y="%d" width="86" height="26"/>' % (40 + 32 * i) for i in range(6))
    + "".join('<text class="tl b1" x="69" y="%d" font-size="13" text-anchor="middle">%s</text>' % (58 + 32 * i, w)
              for i, w in enumerate(["this", "movie", "was", "really", "great", "fun"]))
    + '<rect class="hl b2" x="20" y="66" width="98" height="90" rx="2" fill="none"/>'
    + '<text class="tm b2" x="69" y="248" font-size="13" text-anchor="middle">폭 3 필터가 한 칸씩 내려가요</text>'
    + "".join('<rect class="%s b2" x="196" y="%d" width="56" height="26"/>' % ("n2" if v == 5 else "n", 56 + 32 * i)
              for i, v in enumerate(FMAP))
    + "".join('<text class="tl b2" x="224" y="%d" font-size="14" text-anchor="middle">%d</text>' % (74 + 32 * i, v)
              for i, v in enumerate(FMAP))
    + '<text class="tm b2" x="224" y="44" font-size="13" text-anchor="middle">특징 맵</text>'
    + '<line class="e2 b3" x1="256" y1="120" x2="320" y2="120"/><polygon class="arrow b3" points="324,120 314,115 314,125"/>'
    + '<rect class="n2 b3" x="330" y="102" width="120" height="36"/>'
    + '<text class="tl b3" x="390" y="126" font-size="15" text-anchor="middle">최대 풀링 5</text>'
    + '<text class="tm b3" x="390" y="168" font-size="13" text-anchor="middle">was really great</text>'
    + '</svg>')

SVG_JAC = (
    S0
    + '<text class="tm b1" x="240" y="38" font-size="14" text-anchor="middle">같은 생각이 자라날 뿐이에요</text>'
    + '<rect class="n2 b1" x="40" y="110" width="44" height="44"/>'
    + '<text class="tl b1" x="62" y="139" font-size="16" text-anchor="middle">12</text>'
    + '<text class="tm b1" x="62" y="184" font-size="14" text-anchor="middle">미분</text>'
    + '<text class="tm b1" x="62" y="206" font-size="13" text-anchor="middle">숫자 하나</text>'
    + '<line class="e2 b2" x1="96" y1="132" x2="140" y2="132"/><polygon class="arrow b2" points="144,132 134,127 134,137"/>'
    + "".join('<rect class="n3 b2" x="176" y="%d" width="44" height="34"/>' % (90 + 36 * i) for i in range(3))
    + '<text class="tm b2" x="198" y="184" font-size="14" text-anchor="middle">기울기</text>'
    + '<text class="tm b2" x="198" y="206" font-size="13" text-anchor="middle">한 줄 벡터</text>'
    + '<line class="e2 b3" x1="232" y1="132" x2="276" y2="132"/><polygon class="arrow b3" points="280,132 270,127 270,137"/>'
    + "".join('<rect class="n b3" x="%d" y="%d" width="44" height="34"/>' % (312 + 46 * c, 108 + 36 * r)
              for r in range(2) for c in range(3))
    + '<text class="tm b3" x="381" y="204" font-size="14" text-anchor="middle">야코비안: 행 = 출력, 열 = 입력</text>'
    + '</svg>')

SVG_GEARS = (
    S0
    + '<rect class="n b1" x="24" y="106" width="86" height="52" rx="2"/>'
    + '<text class="tl b1" x="67" y="139" font-size="18" text-anchor="middle">x</text>'
    + '<line class="e2 b2" x1="110" y1="132" x2="168" y2="132"/><polygon class="arrow b2" points="172,132 162,127 162,137"/>'
    + '<text class="tb b2" x="140" y="112" font-size="15" text-anchor="middle">3배</text>'
    + '<rect class="n2 b2" x="176" y="106" width="86" height="52" rx="2"/>'
    + '<text class="tl b2" x="219" y="139" font-size="18" text-anchor="middle">z</text>'
    + '<line class="e2 b3" x1="262" y1="132" x2="320" y2="132"/><polygon class="arrow b3" points="324,132 314,127 314,137"/>'
    + '<text class="tb b3" x="292" y="112" font-size="15" text-anchor="middle">8배</text>'
    + '<rect class="n3 b3" x="328" y="106" width="86" height="52" rx="2"/>'
    + '<text class="tl b3" x="371" y="139" font-size="18" text-anchor="middle">h</text>'
    + '<text class="tb b3" x="240" y="208" font-size="16" text-anchor="middle">합치면 3 x 8 = 24 배</text>'
    + '<text class="tm b3" x="240" y="240" font-size="14" text-anchor="middle">맞물린 톱니바퀴처럼 곱해요</text>'
    + '</svg>')

SVG_LEGO = (
    S0
    + '<rect class="n b1" x="16" y="100" width="76" height="46" rx="2"/>'
    + '<text class="tl b1" x="54" y="129" font-size="17" text-anchor="middle">x</text>'
    + '<text class="tm b1" x="54" y="172" font-size="13" text-anchor="middle">n x 1</text>'
    + '<line class="e2 b2" x1="92" y1="123" x2="118" y2="123"/><polygon class="arrow b2" points="122,123 112,118 112,128"/>'
    + '<rect class="n2 b2" x="126" y="100" width="104" height="46" rx="2"/>'
    + '<text class="tl b2" x="178" y="129" font-size="15" text-anchor="middle">z = Wx + b</text>'
    + '<text class="tm b2" x="178" y="172" font-size="13" text-anchor="middle">m x 1</text>'
    + '<line class="e2 b3" x1="230" y1="123" x2="256" y2="123"/><polygon class="arrow b3" points="260,123 250,118 250,128"/>'
    + '<rect class="n3 b3" x="264" y="100" width="94" height="46" rx="2"/>'
    + '<text class="tl b3" x="311" y="129" font-size="15" text-anchor="middle">h = f(z)</text>'
    + '<text class="tm b3" x="311" y="172" font-size="13" text-anchor="middle">m x 1</text>'
    + '<line class="e2 b4" x1="358" y1="123" x2="384" y2="123"/><polygon class="arrow b4" points="388,123 378,118 378,128"/>'
    + '<rect class="n b4" x="392" y="100" width="72" height="46" rx="2"/>'
    + '<text class="tl b4" x="428" y="129" font-size="15" text-anchor="middle">s = uh</text>'
    + '<text class="tm b4" x="428" y="172" font-size="13" text-anchor="middle">숫자 하나</text>'
    + '<text class="tm b4" x="240" y="230" font-size="14" text-anchor="middle">레고 블록 네 개, 블록마다 미분 하나</text>'
    + '</svg>')

SVG_SHAPE3 = (
    S0
    + '<text class="tm b1" x="240" y="40" font-size="14" text-anchor="middle">크기를 적어 보면 식이 맞는지 알 수 있어요</text>'
    + '<rect class="n2 b1" x="40" y="86" width="32" height="76"/>'
    + '<text class="tm b1" x="56" y="184" font-size="14" text-anchor="middle">2 x 1</text>'
    + '<text class="t b1" x="92" y="130" font-size="18" text-anchor="middle">x</text>'
    + '<rect class="n3 b1" x="112" y="108" width="104" height="32"/>'
    + '<text class="tm b1" x="164" y="184" font-size="14" text-anchor="middle">1 x 3</text>'
    + '<line class="e2 b2" x1="224" y1="124" x2="254" y2="124"/><polygon class="arrow b2" points="258,124 248,119 248,129"/>'
    + '<rect class="n b2" x="268" y="86" width="104" height="76"/>'
    + '<text class="tm b2" x="320" y="184" font-size="14" text-anchor="middle">2 x 3</text>'
    + '<text class="tb b3" x="240" y="222" font-size="15" text-anchor="middle">W 와 크기가 같으면 통과</text>'
    + '<text class="tm b3" x="240" y="248" font-size="13" text-anchor="middle">가운데 숫자가 같아야 곱할 수 있어요</text>'
    + '</svg>')

SVG_GRAPH = (
    S0
    + '<rect class="n b1" x="14" y="58" width="52" height="30" rx="2"/><text class="tl b1" x="40" y="79" font-size="15" text-anchor="middle">x</text>'
    + '<rect class="n b1" x="14" y="138" width="52" height="30" rx="2"/><text class="tl b1" x="40" y="159" font-size="15" text-anchor="middle">W</text>'
    + '<line class="e b1" x1="66" y1="76" x2="93" y2="106"/><line class="e b1" x1="66" y1="150" x2="93" y2="126"/>'
    + '<circle class="n2 b1" cx="110" cy="116" r="18"/><text class="tl b1" x="110" y="122" font-size="16" text-anchor="middle">x</text>'
    + '<circle class="n2 b1" cx="190" cy="116" r="18"/><text class="tl b1" x="190" y="123" font-size="18" text-anchor="middle">+</text>'
    + '<rect class="n b1" x="164" y="186" width="52" height="28" rx="2"/><text class="tl b1" x="190" y="206" font-size="15" text-anchor="middle">b</text>'
    + '<line class="e b1" x1="190" y1="186" x2="190" y2="134"/>'
    + '<circle class="n3 b1" cx="270" cy="116" r="18"/><text class="tl b1" x="270" y="122" font-size="16" text-anchor="middle">f</text>'
    + '<circle class="n2 b1" cx="350" cy="116" r="18"/><text class="tl b1" x="350" y="122" font-size="15" text-anchor="middle">u</text>'
    + '<rect class="n b1" x="324" y="186" width="52" height="28" rx="2"/><text class="tl b1" x="350" y="206" font-size="15" text-anchor="middle">u</text>'
    + '<line class="e b1" x1="350" y1="186" x2="350" y2="134"/>'
    + '<line class="e b1" x1="128" y1="116" x2="172" y2="116"/><line class="e b1" x1="208" y1="116" x2="252" y2="116"/>'
    + '<line class="e b1" x1="288" y1="116" x2="332" y2="116"/><line class="e b1" x1="368" y1="116" x2="404" y2="116"/>'
    + '<rect class="n4 b2" x="408" y="98" width="60" height="36" rx="2"/><text class="tl b2" x="438" y="122" font-size="16" text-anchor="middle">s = 8</text>'
    + '<text class="tm b2" x="150" y="100" font-size="12" text-anchor="middle">[4, -5]</text>'
    + '<text class="tm b2" x="230" y="100" font-size="12" text-anchor="middle">[4, -4]</text>'
    + '<text class="tm b2" x="310" y="100" font-size="12" text-anchor="middle">[4, 0]</text>'
    + '<text class="tm b2" x="240" y="250" font-size="14" text-anchor="middle">순전파: 왼쪽에서 오른쪽으로 값을 구해요</text>'
    + '</svg>')

SVG_NODES = (
    S0
    + '<text class="tm b1" x="240" y="34" font-size="14" text-anchor="middle">뒤에서 온 기울기는 셋 다 2 예요</text>'
    + '<rect class="box b1" x="10" y="48" width="146" height="162" rx="2"/>'
    + '<text class="tb b1" x="83" y="80" font-size="18" text-anchor="middle">+</text>'
    + '<text class="t b1" x="83" y="114" font-size="15" text-anchor="middle">3 + 2 = 5</text>'
    + '<text class="tb b1" x="83" y="152" font-size="15" text-anchor="middle">뒤로 2, 2</text>'
    + '<text class="tm b1" x="83" y="186" font-size="13" text-anchor="middle">똑같이 나눠 줘요</text>'
    + '<rect class="box b2" x="167" y="48" width="146" height="162" rx="2"/>'
    + '<text class="tb b2" x="240" y="80" font-size="16" text-anchor="middle">max</text>'
    + '<text class="t b2" x="240" y="114" font-size="15" text-anchor="middle">max(3, 2) = 3</text>'
    + '<text class="tb b2" x="240" y="152" font-size="15" text-anchor="middle">뒤로 2, 0</text>'
    + '<text class="tm b2" x="240" y="186" font-size="13" text-anchor="middle">이긴 쪽에만 줘요</text>'
    + '<rect class="box b3" x="324" y="48" width="146" height="162" rx="2"/>'
    + '<text class="tb b3" x="397" y="80" font-size="18" text-anchor="middle">x</text>'
    + '<text class="t b3" x="397" y="114" font-size="15" text-anchor="middle">3 x 2 = 6</text>'
    + '<text class="tb b3" x="397" y="152" font-size="15" text-anchor="middle">뒤로 4, 6</text>'
    + '<text class="tm b3" x="397" y="186" font-size="13" text-anchor="middle">상대 값을 곱해요</text>'
    + '<text class="tm b3" x="240" y="242" font-size="14" text-anchor="middle">갈라졌던 길은 되돌아올 때 더해요</text>'
    + '</svg>')

SVG_LM = (
    S0
    + '<text class="tb b1" x="240" y="40" font-size="15" text-anchor="middle">the lecture will end at ___</text>'
    + '<line class="e b1" x1="30" y1="200" x2="450" y2="200"/>'
    + '<rect class="n2 b2" x="50" y="140" width="60" height="60"/>'
    + '<text class="t b2" x="80" y="132" font-size="14" text-anchor="middle">0.2</text>'
    + '<text class="tm b2" x="80" y="220" font-size="13" text-anchor="middle">9pm</text>'
    + '<rect class="n b2" x="140" y="170" width="60" height="30"/>'
    + '<text class="t b2" x="170" y="162" font-size="14" text-anchor="middle">0.1</text>'
    + '<text class="tm b2" x="170" y="220" font-size="13" text-anchor="middle">noon</text>'
    + '<rect class="n b2" x="230" y="185" width="60" height="15"/>'
    + '<text class="t b2" x="260" y="177" font-size="14" text-anchor="middle">0.05</text>'
    + '<text class="tm b2" x="260" y="220" font-size="13" text-anchor="middle">midnight</text>'
    + '<rect class="n3 b3" x="330" y="56" width="90" height="144"/>'
    + '<text class="t b3" x="375" y="48" font-size="14" text-anchor="middle">0.65</text>'
    + '<text class="tm b3" x="375" y="220" font-size="13" text-anchor="middle">나머지 후보</text>'
    + '<text class="tm b3" x="240" y="248" font-size="14" text-anchor="middle">모두 더하면 1 이에요</text>'
    + '</svg>')

SVG_NGRAM = (
    S0
    + '<rect class="box b1" x="18" y="50" width="240" height="40" rx="2"/>'
    + '<text class="tm b1" x="138" y="75" font-size="13" text-anchor="middle">as the proctor started the clock, the</text>'
    + '<text class="tm b2" x="138" y="112" font-size="13" text-anchor="middle">마르코프 가정으로 버려져요</text>'
    + '<rect class="n2 b1" x="272" y="50" width="190" height="40"/>'
    + '<text class="tl b1" x="367" y="75" font-size="13" text-anchor="middle">students opened their</text>'
    + '<text class="t b2" x="367" y="112" font-size="13" text-anchor="middle">이 3단어만 봐요</text>'
    + '<text class="tb b3" x="240" y="158" font-size="15" text-anchor="middle">count(students opened their) = 1,000</text>'
    + '<text class="t b3" x="140" y="196" font-size="15" text-anchor="middle">books 400 = 0.40</text>'
    + '<text class="t b3" x="345" y="196" font-size="15" text-anchor="middle">exams 100 = 0.10</text>'
    + '<text class="tm b3" x="240" y="238" font-size="14" text-anchor="middle">단서였던 proctor, clock 은 이미 버려졌어요</text>'
    + '</svg>')

SVG_PPL = (
    S0
    + '<text class="tm b1" x="240" y="44" font-size="14" text-anchor="middle">퍼플렉서티 눈금: 낮을수록 좋아요</text>'
    + '<line class="e b1" x1="40" y1="140" x2="450" y2="140"/>'
    + "".join('<line class="e b%d" x1="%d" y1="130" x2="%d" y2="150"/>' % (b, x, x)
              for b, x in [(1, 60), (2, 160), (2, 300), (3, 430)])
    + '<text class="tb b1" x="60" y="118" font-size="15" text-anchor="middle">1</text>'
    + '<text class="tm b1" x="60" y="176" font-size="13" text-anchor="middle">완벽한 모델</text>'
    + '<text class="tb b2" x="160" y="118" font-size="15" text-anchor="middle">5.7</text>'
    + '<text class="tm b2" x="160" y="176" font-size="13" text-anchor="middle">슬라이드 예제</text>'
    + '<text class="tb b2" x="300" y="118" font-size="15" text-anchor="middle">100</text>'
    + '<text class="tm b2" x="300" y="176" font-size="13" text-anchor="middle">좋은 n-gram</text>'
    + '<text class="tb b3" x="430" y="118" font-size="15" text-anchor="middle">10,000</text>'
    + '<text class="tm b3" x="430" y="176" font-size="13" text-anchor="middle">아무것도 모름</text>'
    + '<text class="tm b3" x="240" y="232" font-size="14" text-anchor="middle">1 보다 작을 수는 없어요</text>'
    + '</svg>')

SVG_FWLM = (
    S0
    + "".join('<rect class="n b1" x="%d" y="206" width="86" height="28"/>' % (28 + 106 * i) for i in range(4))
    + "".join('<text class="tl b1" x="%d" y="225" font-size="13" text-anchor="middle">%s</text>' % (71 + 106 * i, w)
              for i, w in enumerate(["the", "kids", "opened", "their"]))
    + "".join('<rect class="n2 b1" x="%d" y="164" width="86" height="28"/>' % (28 + 106 * i) for i in range(4))
    + "".join('<text class="tl b1" x="%d" y="183" font-size="13" text-anchor="middle">e%d</text>' % (71 + 106 * i, i + 1)
              for i in range(4))
    + "".join('<line class="e b2" x1="%d" y1="164" x2="240" y2="146"/>' % (71 + 106 * i) for i in range(4))
    + '<rect class="n3 b2" x="28" y="116" width="404" height="28"/>'
    + '<text class="tl b2" x="230" y="135" font-size="14" text-anchor="middle">e = [e1; e2; e3; e4]</text>'
    + '<rect class="n2 b2" x="150" y="74" width="180" height="30"/>'
    + '<text class="tl b2" x="240" y="95" font-size="14" text-anchor="middle">h = f(We + b)</text>'
    + '<rect class="n b3" x="128" y="32" width="224" height="30"/>'
    + '<text class="tl b3" x="240" y="53" font-size="14" text-anchor="middle">y = softmax(Uh), 어휘 전체</text>'
    + '<text class="tm b3" x="240" y="258" font-size="13" text-anchor="middle">books 0.42, presents 0.21, laptops 0.09</text>'
    + '</svg>')

SVG_RNN = (
    S0
    + "".join('<rect class="n2 b1" x="%d" y="110" width="76" height="38"/>' % (30 + 112 * i) for i in range(4))
    + "".join('<text class="tl b1" x="%d" y="135" font-size="15" text-anchor="middle">h</text>' % (68 + 112 * i)
              for i in range(4))
    + "".join('<line class="e2 b2" x1="%d" y1="129" x2="%d" y2="129"/><polygon class="arrow b2" points="%d,129 %d,124 %d,134"/>'
              % (106 + 112 * i, 138 + 112 * i, 142 + 112 * i, 132 + 112 * i, 132 + 112 * i) for i in range(3))
    + "".join('<text class="tm b2" x="%d" y="112" font-size="12" text-anchor="middle">Wh</text>' % (124 + 112 * i)
              for i in range(3))
    + "".join('<rect class="n b1" x="%d" y="192" width="76" height="28"/>' % (30 + 112 * i) for i in range(4))
    + "".join('<text class="tl b1" x="%d" y="211" font-size="13" text-anchor="middle">%s</text>' % (68 + 112 * i, w)
              for i, w in enumerate(["the", "kids", "opened", "their"]))
    + "".join('<line class="e b1" x1="%d" y1="192" x2="%d" y2="152"/>' % (68 + 112 * i, 68 + 112 * i) for i in range(4))
    + "".join('<rect class="n3 b3" x="%d" y="46" width="76" height="28"/>' % (30 + 112 * i) for i in range(4))
    + "".join('<text class="tl b3" x="%d" y="65" font-size="13" text-anchor="middle">y</text>' % (68 + 112 * i)
              for i in range(4))
    + "".join('<line class="e b3" x1="%d" y1="110" x2="%d" y2="76"/>' % (68 + 112 * i, 68 + 112 * i) for i in range(4))
    + '<text class="tm b3" x="240" y="250" font-size="14" text-anchor="middle">같은 Wh, We, U 를 매 걸음 다시 써요</text>'
    + '</svg>')

SVG_VANISH = (
    S0
    + '<text class="tm b1" x="240" y="38" font-size="14" text-anchor="middle">기울기가 시간을 거슬러 흐르며 희미해져요</text>'
    + "".join('<rect class="n2 b1" x="%d" y="82" width="70" height="36"/>' % (22 + 90 * i) for i in range(5))
    + "".join('<text class="tl b1" x="%d" y="106" font-size="14" text-anchor="middle">h%d</text>' % (57 + 90 * i, i + 1)
              for i in range(5))
    + "".join('<line class="e b1" x1="%d" y1="100" x2="%d" y2="100"/>' % (92 + 90 * i, 108 + 90 * i) for i in range(4))
    + "".join('<line class="e2 b2" x1="%d" y1="152" x2="%d" y2="152"/><polygon class="arrow b2" points="%d,152 %d,147 %d,157"/>'
              % (108 + 90 * i, 96 + 90 * i, 90 + 90 * i, 100 + 90 * i, 100 + 90 * i) for i in range(4))
    + "".join('<text class="%s b2" x="%d" y="186" font-size="%d" text-anchor="middle">%s</text>'
              % (c, 57 + 90 * i, sz, lab)
              for i, (c, sz, lab) in enumerate([("tb", 17, "큼"), ("tb", 15, "조금"), ("t", 14, "작음"), ("tm", 13, "더 작음"), ("tm", 12, "거의 0")]))
    + '<text class="tm b3" x="240" y="234" font-size="14" text-anchor="middle">1 보다 작은 수를 스무 번 곱하면 0.0115</text>'
    + '</svg>')

SVG_CLIP = (
    S0
    + '<rect class="box b1" x="20" y="56" width="200" height="130" rx="2"/>'
    + '<line class="e2 b1" x1="50" y1="172" x2="210" y2="70"/><polygon class="arrow b1" points="216,66 202,70 208,80"/>'
    + '<text class="tm b1" x="120" y="212" font-size="14" text-anchor="middle">폭발: 한 걸음이 너무 커요</text>'
    + '<rect class="box b2" x="260" y="56" width="200" height="130" rx="2"/>'
    + '<line class="e2 b2" x1="290" y1="172" x2="342" y2="139"/><polygon class="arrow b2" points="348,135 334,138 340,147"/>'
    + '<text class="tm b2" x="360" y="212" font-size="14" text-anchor="middle">클리핑: 방향은 그대로</text>'
    + '<text class="tb b3" x="240" y="248" font-size="15" text-anchor="middle">길이가 기준보다 크면 기준까지만 줄여요</text>'
    + '</svg>')

U = []

# ---------------------------------------------------------------- w3-1
t = [T("개체명 인식", "Named Entity Recognition (NER)", "글 속에서 사람, 기관, 장소 같은 이름을 찾아 종류를 붙이는 일이에요.",
       "3주차 내내 신경망을 설명할 때 쓰는 예제 과제예요. Busan 을 보면 장소(LOCATION)라고 붙여요."),
     T("분류", "Classification", "입력을 보고 정해진 여러 칸 중 어느 칸인지 고르는 일이에요."),
     T("윈도우", "Window", "가운데 단어 양옆으로 몇 단어씩 함께 보는 창이에요.",
       "m = 2 이면 앞 2개, 뒤 2개를 봐서 모두 5단어예요. 2주차 word2vec 에서도 나왔어요."),
     T("중심 단어", "Center Word", "창 한가운데에 있어 지금 판단하려는 단어예요."),
     T("소프트맥스", "Softmax", "점수를 모두 더해 1이 되는 확률 파이로 나누는 함수예요."),
     T("교차 엔트로피", "Cross-Entropy", "정답 칸에 준 확률의 -log 를 벌점으로 매기는 손실이에요."),
     T("선형 분류기", "Linear Classifier", "곧은 선 하나로만 무리를 가르는 분류기예요.")]
U.append({"id": "w3-1", "title": "이름 찾기 NER 과 선형의 한계", "goal": "창 분류가 무엇인지 말하고, 소프트맥스와 교차 엔트로피를 손으로 계산할 수 있어요.", "terms": t, "slides": [
    title("창으로 이름 찾기", "그리고 곧은 선의 한계"),
    goal("**개체명 인식(Named Entity Recognition (NER))** 과 창 **분류(Classification)**", "**소프트맥스(Softmax)** 와 **교차 엔트로피(Cross-Entropy)** 손계산", "왜 **선형 분류기(Linear Classifier)** 로는 부족한지"),
    pts("지난주에서 오늘로 (N3 p.4)", "지난주: 글을 **토큰(Token)** 으로 자르고 **단어 벡터(Word Vector)** 를 만들었어요",
        "지금까지 흐름은 글 → 토큰 → 벡터 → 물음표예요", "그 벡터를 받아 먹는 기계가 오늘의 신경망이에요",
        "주문 기억하죠. 글을 토큰으로 자르고, 토큰을 벡터로 바꾸고, 벡터로 다음 토큰을 맞혀요"),
    pts("붙잡고 갈 과제 (N3 p.6)", "**개체명 인식(Named Entity Recognition (NER))**: 글에서 이름을 찾아 종류를 붙여요",
        "사람(PERSON), 기관(ORGANIZATION), 장소(LOCATION) 같은 칸이 있어요",
        "한 단어만 보지 않고 **윈도우(Window)** 로 양옆을 함께 봐요", "가운데 **중심 단어(Center Word)** 가 지금 판단할 단어예요"),
    fig("창 분류가 흘러가는 길 (N3 p.6)", SVG_WINDOW, "다섯 단어의 **단어 벡터(Word Vector)** 를 이어 붙여 분류기에 넣어요", 3),
    steps("손계산: 창 벡터는 몇 칸일까", [
        "**윈도우(Window)** m = 2 면 **중심 단어(Center Word)** 앞 2개, 뒤 2개, 모두 5단어예요",
        "**단어 벡터(Word Vector)** 한 개가 d = 50 칸이라고 해요",
        "이어 붙이면 5 x 50 = 250 칸",
        "d = 100 이면 5 x 100 = 500 칸",
    ], "창 벡터 x 의 길이는 5d. d = 50 이면 250, d = 100 이면 500", "이어 붙이기(concatenate)는 그냥 옆으로 줄 세우는 거예요"),
    ana("점수를 확률 파이로, 틀리면 벌점", "모델이 칸마다 점수를 매기면 **소프트맥스(Softmax)** 가 확률 파이로 나눠요. 정답 칸 조각이 작으면 벌점을 크게 받아요.",
        [("칸마다 매긴 점수", "로짓, 곧 Wx 로 얻은 날것 점수"), ("모두 더해 1인 확률 파이", "**소프트맥스(Softmax)**"), ("틀린 만큼 받는 벌점", "**교차 엔트로피(Cross-Entropy)**")]),
    form("소프트맥스 분류기 (N3 p.7)", r"P(y \mid x) = \mathrm{softmax}(Wx)_y = \frac{\exp(W_y x)}{\sum_c \exp(W_c x)}",
         [(r"W", "가중치 행렬. 한 행이 **분류(Classification)** 칸 하나를 맡아요"),
          (r"W_y x", "정답 후보 y 칸의 점수"), (r"\exp(\cdot)", "점수를 늘 양수로 바꾸는 지수 함수"),
          (r"\sum_c", "모든 칸 c 의 값을 다 더하기"), (r"P(y \mid x)", "x 를 봤을 때 답이 y 일 확률")],
         "점수에 exp 를 씌우고 전체 합으로 나누면 다 더해서 1 인 확률이 돼요."),
    steps("손계산: 소프트맥스와 교차 엔트로피 (N3 p.7)", [
        "점수: PERSON 1, LOCATION 3, ORG 0 이고 정답은 LOCATION 이에요",
        "exp 를 씌우면 e¹ ≈ 2.72, e³ ≈ 20.09, e⁰ = 1, 합은 약 23.80",
        "확률: 2.72 ÷ 23.80 ≈ 0.11, 20.09 ÷ 23.80 ≈ 0.84, 1 ÷ 23.80 ≈ 0.04",
        "벌점은 정답 확률의 -log: -log(0.84) ≈ 0.17",
        "정답에 0.9 를 주면 0.11, 0.01 을 주면 4.61 로 확 뛰어요",
    ], "정답 확률 0.84 → **교차 엔트로피(Cross-Entropy)** 약 0.17", "로그는 자연로그(ln)를 써요"),
    pts("아직은 선형이에요 (N3 p.7, p.8)", "행렬 W 하나만 곱하니 이것은 **선형 분류기(Linear Classifier)** 예요",
        "곧은 선(초평면) 하나로만 무리를 갈라요", "그런데 말에는 곧은 선으로 못 가르는 짝이 많아요",
        "not bad 는 not 과 bad 를 그냥 더한 뜻이 아니에요"),
    fig("곧은 선이 지는 자리 (N3 p.8)", SVG_LINEAR, "가운데 무리를 바깥 무리와 직선 하나로는 못 갈라요. 휜 경계가 필요해요", 3),
    check("**윈도우(Window)** m = 2, d = 100 일 때 창 벡터의 길이는?",
          ["500", "100", "200", "250"], 0, "가운데 단어 + 양쪽 2개씩 = 5단어, 5 x 100 = 500 이에요."),
    check("**소프트맥스(Softmax)** 를 거치기 전의 점수에 대한 설명으로 맞는 것은?",
          ["음수도 나오고 확률이 아니에요", "항상 0 과 1 사이예요", "다 더하면 1 이에요", "항상 정수예요"], 0,
          "Wx 라서 음수도 나와요. 0 에서 1 사이, 합 1 은 **소프트맥스(Softmax)** 뒤의 성질이에요."),
    check("not bad 가 **선형 분류기(Linear Classifier)** 에게 어려운 까닭은?",
          ["두 단어가 합쳐질 때 뜻이 뒤집히는 상호작용이라서", "단어가 길어서", "사전에 없어서", "대문자라서"], 0,
          "not 이 뒤 단어에 따라 역할이 달라져요. 효과를 따로 더하는 방식으로는 못 잡아요."),
    warn("헷갈리기 쉬운 점", "**소프트맥스(Softmax)** 가 곧 **교차 엔트로피(Cross-Entropy)** 는 아니에요. 소프트맥스 뒤에 -log 를 붙인 것이에요.",
         "**개체명 인식(Named Entity Recognition (NER))** 도 단어마다 칸을 고르는 **분류(Classification)** 예요.",
         "창 벡터의 길이는 5 + d 가 아니라 5 x d 예요."),
    recap("**개체명 인식(Named Entity Recognition (NER))**: **윈도우(Window)** 로 **중심 단어(Center Word)** 를 **분류(Classification)**",
          "점수 → **소프트맥스(Softmax)** → 확률 → **교차 엔트로피(Cross-Entropy)** 벌점",
          "행렬 하나뿐이면 **선형 분류기(Linear Classifier)**, 곧은 경계만 그어요",
          "오늘의 용어: 개체명 인식(NER), 분류, 윈도우(Window), 중심 단어, 소프트맥스, 교차 엔트로피, 선형 분류기"),
]})

# ---------------------------------------------------------------- w3-2
t = [T("뉴런", "Neuron", "가중합에 편향 항을 더하고 활성화 함수를 통과시키는 작은 계산 단위예요.",
       "하나의 뉴런은 학습된 패턴 탐지기 하나예요. 식은 h = f(wᵀx + b) 예요."),
     T("가중합", "Weighted Sum", "입력마다 가중치를 곱해서 모두 더한 값이에요."),
     T("편향 항", "Bias Term", "가중합에 더하는 숫자 하나 b 예요. 사회적 편향과 다른 말이에요."),
     T("활성화 함수", "Activation Function", "가중합 결과 z 를 받아 휘어진 값 f(z) 로 바꾸는 함수예요."),
     T("렐루", "ReLU", "음수는 0 으로 끄고 양수는 그대로 통과시키는 함수 max(z, 0) 이에요."),
     T("시그모이드", "Sigmoid", "값을 0 과 1 사이로 눌러 담는 S자 함수예요."),
     T("비선형성", "Nonlinearity", "곧은 선이 아니게 휘게 만드는 성질이에요.")]
U.append({"id": "w3-2", "title": "뉴런과 활성화 함수", "goal": "뉴런 하나를 손으로 계산하고, 왜 비선형성이 꼭 필요한지 설명할 수 있어요.", "terms": t, "slides": [
    title("뉴런 한 장", "곱하고, 더하고, 휘기"),
    goal("**뉴런(Neuron)** 안에서 무슨 일이 일어나는지", "**렐루(ReLU)** 와 **시그모이드(Sigmoid)** 의 차이", "왜 **비선형성(Nonlinearity)** 이 선택이 아닌지"),
    ana("이름만 빌려 온 신경세포", "슬라이드 오른쪽에는 생물의 신경세포 그림이 있어요. 여러 신호를 받아 세기를 달리 더하고, 기준을 넘으면 내보내죠. 이름만 거기서 빌려 왔어요.",
        [("들어오는 신호", "입력 x"), ("연결의 세기", "가중치 w"), ("기준을 넘으면 내보냄", "**활성화 함수(Activation Function)** f")]),
    pts("뉴런이 하는 일 (N3 p.9)", "입력마다 가중치를 곱해 모두 더해요. 이것이 **가중합(Weighted Sum)**",
        "거기에 **편향 항(Bias Term)** b 를 더해 z 를 만들어요", "z 를 **활성화 함수(Activation Function)** f 에 넣어 h 를 내보내요",
        "슬라이드 말로 작고 배울 수 있는 패턴 탐지기 하나예요"),
    fig("뉴런 안의 순서 (N3 p.9)", SVG_NEURON, "곱하고 → 더하고 → **편향 항(Bias Term)** 더하고 → f 로 휘기", 4),
    form("뉴런의 식", r"h = f(\mathbf{w}^{\top}\mathbf{x} + b) = f\Big(\sum_{i=1}^{d} w_i x_i + b\Big)",
         [(r"\mathbf{w}^{\top}\mathbf{x}", "**가중합(Weighted Sum)**, 곧 짝끼리 곱해 더하기"),
          (r"b", "**편향 항(Bias Term)**. 켜지는 기준을 옮겨요"),
          (r"f", "**활성화 함수(Activation Function)**"), (r"h", "**뉴런(Neuron)** 의 출력")],
         "곱해서 더하고 b 를 더한 뒤 f 로 휘면 **뉴런(Neuron)** 하나의 출력이에요."),
    steps("손계산: 입력 세 개짜리 뉴런", [
        "x = [1, 2, 3], w = [0.5, -1, 0.5], b = 0.5",
        "**가중합(Weighted Sum)**: 0.5x1 + (-1)x2 + 0.5x3 = 0.5 - 2 + 1.5 = 0",
        "**편향 항(Bias Term)** 을 더해 z = 0 + 0.5 = 0.5",
        "**렐루(ReLU)**: max(0.5, 0) = 0.5",
        "**시그모이드(Sigmoid)**: 1 ÷ (1 + e^(-0.5)) ≈ 0.62",
    ], "z = 0.5, ReLU 출력 0.5, 시그모이드 출력 약 0.62", "x = [1, 3, 1] 이면 z = -1.5 라 ReLU 는 0, 시그모이드는 약 0.18"),
    fig("두 대표 선수 (N3 p.10)", SVG_ACT, "**시그모이드(Sigmoid)** 는 0 과 1 사이로 눌러 담고, **렐루(ReLU)** 는 음수만 꺼요", 2),
    cmp_("활성화 함수 메뉴 (N3 p.10)", ["함수", "출력 범위", "주로 쓰는 곳"],
         [["**시그모이드(Sigmoid)**", "0 에서 1", "확률, LSTM 게이트"],
          ["tanh", "-1 에서 1", "게이트, RNN 의 은닉 상태"],
          ["**렐루(ReLU)**", "0 에서 무한대", "안쪽 층의 기본 선택"],
          ["GELU", "ReLU 와 비슷", "트랜스포머(4주차)"]]),
    steps("손계산: 값을 넣어 보기", [
        "**렐루(ReLU)**: ReLU(-2) = 0, ReLU(0) = 0, ReLU(3) = 3",
        "**시그모이드(Sigmoid)**: σ(0) = 1 ÷ 2 = 0.5",
        "σ(4) ≈ 0.98, σ(-4) ≈ 0.02",
        "σ 는 4 에서 이미 1 에 붙어서 더 커져도 거의 안 변해요",
        "**렐루(ReLU)** 는 양수 쪽 기울기가 늘 1 이에요",
    ], "양 끝에서 시그모이드는 평평해지고, ReLU 는 양수 쪽이 계속 기울어 있어요", "교수님: ReLU 가 딥러닝에서 가장 중요한 함수 중 하나예요"),
    pts("비선형성은 선택이 아니에요 (N3 p.11)", "f 없이 선형층만 쌓으면 W₂(W₁x) = (W₂W₁)x 로 합쳐져요",
        "곧 층을 열 개 쌓아도 행렬 하나와 표현력이 같아요", "**비선형성(Nonlinearity)** 이 있어야 공간이 휘고 깊이가 뜻을 가져요",
        "보편 근사 정리: 은닉 뉴런이 충분하면 웬만한 함수를 흉내 낼 수 있어요"),
    steps("손계산: 정말 합쳐지는지 확인", [
        "W1 = [[1, 2], [0, 1]], W2 = [[1, 0], [1, 1]], x = [1, 1]",
        "한 층씩: W1x = [3, 1], 그다음 W2[3, 1] = [3, 4]",
        "먼저 합치기: W2W1 = [[1, 2], [1, 3]], 그 결과에 x 를 곱하면 [3, 4]",
        "사이에 **렐루(ReLU)** 를 끼우면: V1 = [[1, -2], [0, 1]], V1x = [-1, 1] → ReLU → [0, 1] → W2 → [0, 1]",
        "ReLU 없이 합치면 (W2V1)x = [-1, 0] 이라 답이 달라요",
    ], "f 가 없으면 두 층이 행렬 하나로 합쳐지고, f 를 끼우면 합쳐지지 않아요", "행렬 곱은 묶는 방법을 바꿔도 결과가 같아요"),
    check("x = [2, 1], w = [1, -3], b = 0 인 **뉴런(Neuron)** 에 **렐루(ReLU)** 를 쓰면 출력은?",
          ["0", "-1", "1", "5"], 0, "z = 1x2 + (-3)x1 + 0 = -1. 음수라서 **렐루(ReLU)** 가 0 으로 꺼요."),
    check("**활성화 함수(Activation Function)** 없이 선형층 열 개를 쌓으면?",
          ["선형층 한 개와 표현력이 같아요", "열 배 강해져요", "곡선 경계를 그릴 수 있어요", "학습이 열 배 빨라져요"], 0,
          "모두 곱하면 행렬 하나가 되어 **비선형성(Nonlinearity)** 이 전혀 생기지 않아요."),
    warn("헷갈리기 쉬운 점", "여기의 **편향 항(Bias Term)** b 는 사회적 편향(Bias)과 전혀 다른 말이에요.",
         "**시그모이드(Sigmoid)** 는 양 끝 기울기가 거의 0 이라 깊게 쌓으면 기울기가 사라져요.",
         "**렐루(ReLU)** 도 음수 쪽 기울기가 0 이라 뉴런이 꺼진 채 남을 수 있어요(dying ReLU)."),
    recap("**뉴런(Neuron)** = **가중합(Weighted Sum)** + **편향 항(Bias Term)** + **활성화 함수(Activation Function)**",
          "x = [1, 2, 3], w = [0.5, -1, 0.5], b = 0.5 → z = 0.5, ReLU 0.5, 시그모이드 0.62",
          "f 가 없으면 층이 합쳐져요. **비선형성(Nonlinearity)** 은 필수예요",
          "오늘의 용어: 뉴런(Neuron), 가중합, 편향 항, 활성화 함수, ReLU, 시그모이드(Sigmoid), 비선형성"),
]})

# ---------------------------------------------------------------- w3-3
t = [T("다층 퍼셉트론", "Multi-Layer Perceptron (MLP)", "뉴런 층을 여러 겹 쌓은 가장 기본 신경망이에요."),
     T("은닉층", "Hidden Layer", "입력과 출력 사이에 숨어 있는 중간 층이에요."),
     T("파라미터", "Parameter", "학습으로 정해지는 숫자들. 가중치와 편향 항이에요."),
     T("합성곱 신경망", "Convolutional Neural Network (CNN)", "작은 필터를 미끄러뜨려 부분 패턴을 찾는 신경망이에요."),
     T("합성곱 필터", "Convolution Filter", "문장을 따라 미끄러지며 짧은 패턴을 찾는 숫자 판이에요."),
     T("최대 풀링", "Max-pooling", "특징 맵에서 가장 큰 값 하나만 남기는 것이에요."),
     T("모양", "Shape", "벡터나 행렬이 몇 행 몇 열인지 적은 크기 정보예요.")]
U.append({"id": "w3-3", "title": "MLP 와 CNN, 그리고 shape", "goal": "MLP 의 파라미터 수와 W 의 shape 을 직접 셀 수 있어요.", "terms": t, "slides": [
    title("층을 쌓고, 필터를 밀고", "MLP 와 CNN"),
    goal("**다층 퍼셉트론(Multi-Layer Perceptron (MLP))** 의 식과 **파라미터(Parameter)** 수", "**합성곱 신경망(CNN)** 이 찾는 것", "W 의 **모양(Shape)** 규칙"),
    pts("층을 쌓으면 MLP (N3 p.12)", "**뉴런(Neuron)** 을 여러 개 모아 한 층, 그 층을 여러 겹 쌓아요",
        "가운데 층은 밖에서 안 보여서 **은닉층(Hidden Layer)** 이라고 불러요",
        "창 분류기 = **단어 벡터(Word Vector)** → **다층 퍼셉트론(Multi-Layer Perceptron (MLP))** → 장소일 확률",
        "교수님: 중요한 건 W 와 b 예요. 이걸 정하는 게 학습이에요"),
    fig("MLP 의 모양 (N3 p.12)", SVG_MLP, "입력 x → **은닉층(Hidden Layer)** 둘 → 출력. 선마다 가중치가 하나씩 있어요", 3),
    form("MLP 의 식 (N3 p.12)", r"h^{(1)} = f(W^{(1)}x + b^{(1)}),\quad h^{(2)} = f(W^{(2)}h^{(1)} + b^{(2)}),\quad \hat{y} = \mathrm{softmax}(U h^{(2)})",
         [(r"W^{(1)}, b^{(1)}", "첫 층의 가중치와 **편향 항(Bias Term)**"),
          (r"f", "**활성화 함수(Activation Function)**"),
          (r"h^{(1)}, h^{(2)}", "**은닉층(Hidden Layer)** 의 출력 벡터"),
          (r"U", "마지막 점수 행렬. 여기에는 b 가 없어요"),
          (r"\hat{y}", "칸마다의 확률")],
         "뉴런 계산 f(Wx + b) 를 층마다 되풀이하고 끝에 **소프트맥스(Softmax)** 를 붙여요."),
    steps("손계산: 파라미터 몇 개일까 (N3 p.12 그림)", [
        "입력 4, **은닉층(Hidden Layer)** 4, 은닉 4, 출력 3 이라고 해요",
        "입력 4 → 은닉 4: W(1) 은 4 x 4 = 16 개, b(1) 은 4 개",
        "은닉 4 → 은닉 4: W(2) 는 16 개, b(2) 는 4 개",
        "은닉 4 → 출력 3: U 는 3 x 4 = 12 개",
        "모두 더하면 16 + 4 + 16 + 4 + 12",
    ], "**파라미터(Parameter)** 52 개", "선 하나가 가중치 하나예요"),
    steps("손계산: W 의 shape (N3 p.15 Q2)", [
        "입력 창이 5단어 x 100차원이면 x 의 길이는 5 x 100 = 500",
        "**은닉층(Hidden Layer)** 이 300 개면 h(1) 의 길이는 300",
        "h(1) = f(W(1)x + b(1)) 이 되려면 W(1) 은 300행 500열",
        "가중치 개수는 300 x 500 = 150,000 개, b(1) 은 300 개",
    ], "W(1) 의 **모양(Shape)** 은 (300, 500). 행 = 출력 수, 열 = 입력 수", "교수님은 연결선 개수로 '500 곱하기 300' 이라고 말했어요"),
    ana("바로 앞 몇 단어만 보고 맞히기", "**합성곱 필터(Convolution Filter)** 는 문장 위를 한 칸씩 미끄러지며 붙어 있는 몇 단어만 봐요. 앞 몇 단어만 보는 n-gram 과 같은 눈이에요.",
        [("붙어 있는 세 단어", "폭 3 **합성곱 필터(Convolution Filter)**"), ("창마다 낸 값", "특징 맵"), ("가장 센 곳만 남기기", "**최대 풀링(Max-pooling)**")]),
    fig("필터가 미끄러져요 (N3 p.13, p.14)", SVG_CNN, "창마다 값 하나 → 특징 맵 → **최대 풀링(Max-pooling)** 으로 가장 큰 값만", 3),
    steps("손계산: 필터 한 개 돌려 보기", [
        "단어마다 숫자 하나로 줄여요: this 0, movie 1, was 0, really 2, great 3, fun -1",
        "**합성곱 필터(Convolution Filter)** 는 [1, 1, 1], 곧 세 값을 더하기",
        "this movie was: 0 + 1 + 0 = 1, movie was really: 1 + 0 + 2 = 3",
        "was really great: 0 + 2 + 3 = 5, really great fun: 2 + 3 - 1 = 4",
        "특징 맵 [1, 3, 5, 4], **최대 풀링(Max-pooling)** 하면 5",
    ], "가장 센 곳은 was really great 이고 값은 5 예요", "실제로는 단어마다 벡터이고 필터도 3 x d 판이에요. 모양만 본 예제예요"),
    cmp_("CNN 의 장점과 한계 (N3 p.14)", ["", "내용"],
         [["장점", "모든 창을 동시에 계산해서 빨라요"],
          ["장점", "**최대 풀링(Max-pooling)** 덕분에 위치와 상관없이 패턴을 잡아요"],
          ["장점", "감정이나 주제 같은 **분류(Classification)** 에 좋아요"],
          ["한계", "창 안만 봐서 멀리 떨어진 단어 사이 순서와 관계를 못 봐요"]]),
    pts("Check Yourself 1 (N3 p.15)", "Q1 활성화 없이 선형층 10개를 쌓으면 표현력은 어떤가요 → 선형 하나와 같아요",
        "Q2 은닉 300, 입력 5단어 x 100차원이면 W(1) 의 **모양(Shape)** 은 → (300, 500)",
        "Q3 폭 3 **합성곱 필터(Convolution Filter)** 가 세게 반응했다면 → 학습된 세 단어 패턴을 찾은 거예요",
        "Q4 **최대 풀링(Max-pooling)** 이 위치에 둔감한 까닭 → 최댓값만 남기고 어디였는지는 버려요"),
    check("W(1) 의 **모양(Shape)** 이 (3, 5) 일 때 입력 x 와 h(1) 의 길이는?",
          ["x 5, h(1) 3", "x 3, h(1) 5", "x 15, h(1) 1", "둘 다 5"], 0,
          "W 의 열 수 5 가 입력 길이, 행 수 3 이 **은닉층(Hidden Layer)** 뉴런 수예요."),
    check("**최대 풀링(Max-pooling)** 때문에 **합성곱 신경망(CNN)** 이 위치에 둔감해지는 까닭은?",
          ["가장 큰 값만 남기고 어디서 나왔는지는 버려서", "위치 정보를 따로 더해서", "필터 폭이 넓어서", "학습을 안 해서"], 0,
          "값이 앞에서 나왔든 뒤에서 나왔든 결과가 같아져요."),
    warn("헷갈리기 쉬운 점", "**다층 퍼셉트론(Multi-Layer Perceptron (MLP))** 의 줄임말 MLP 를 NLP 와 헷갈리지 마세요.",
         "슬라이드 식의 마지막 U 에는 **편향 항(Bias Term)** 이 없어요.",
         "위치에 둔감한 것은 장점이자 단점이에요. 순서가 중요할 때는 정보가 사라져요."),
    recap("**다층 퍼셉트론(Multi-Layer Perceptron (MLP))** = f(Wx + b) 를 층마다 반복, 끝에 **소프트맥스(Softmax)**",
          "입력 4, 은닉 4, 은닉 4, 출력 3 이면 **파라미터(Parameter)** 52 개. W 의 **모양(Shape)** 은 (출력 수, 입력 수)",
          "**합성곱 신경망(CNN)** 은 **합성곱 필터(Convolution Filter)** 와 **최대 풀링(Max-pooling)** 으로 패턴을 찾아요",
          "오늘의 용어: MLP, 은닉층, 파라미터, CNN, 합성곱 필터, 최대 풀링, 모양(Shape)"),
]})

# ---------------------------------------------------------------- w3-4
t = [T("기울기", "Gradient", "값을 조금 바꾸면 결과가 얼마나, 어느 쪽으로 바뀌는지 알려 주는 숫자 묶음이에요."),
     T("경사 하강법", "Gradient Descent", "안개 낀 산에서 발밑 기울기만 보고 한 걸음씩 내려가기예요."),
     T("학습률", "Learning Rate", "경사 하강법에서 한 걸음의 보폭이에요."),
     T("미분", "Derivative", "x 를 살짝 밀면 f 가 얼마나 움직이는지 나타내는 기울기예요."),
     T("야코비안", "Jacobian", "입력 여러 개, 출력 여러 개인 함수의 미분을 모아 놓은 표예요.",
       "출력이 m 개, 입력이 n 개면 m x n 행렬이에요. 행이 출력, 열이 입력이에요."),
     T("연쇄 법칙", "Chain Rule", "여러 단계를 거친 함수의 미분은 단계마다의 미분을 곱하면 된다는 규칙이에요."),
     T("역전파", "Backpropagation", "틀린 책임을 출력에서 입력 쪽으로 나눠 주며 모든 기울기를 구하는 방법이에요.")]
U.append({"id": "w3-4", "title": "기울기, 야코비안, 연쇄 법칙", "goal": "미분에서 야코비안까지 이어지는 생각을 잡고, 연쇄 법칙을 숫자로 쓸 수 있어요.", "terms": t, "slides": [
    title("발밑 기울기 구하기", "미분, 야코비안, 연쇄 법칙"),
    goal("**경사 하강법(Gradient Descent)** 의 한 걸음", "**미분(Derivative)** 에서 **야코비안(Jacobian)** 까지", "**연쇄 법칙(Chain Rule)** 을 숫자로 써 보기"),
    ana("안개 낀 산 내려가기", "안개 낀 산에서 발밑 **기울기(Gradient)** 만 보고 한 걸음씩 내려가요. 그런데 이번 산은 손잡이가 수만 개예요.",
        [("산의 높이", "**손실 함수(Loss Function)** J"), ("발밑 기울기", "**기울기(Gradient)**"), ("보폭", "**학습률(Learning Rate)** α"), ("수만 개의 손잡이", "W, b, 그리고 단어 벡터까지")]),
    form("업데이트 식 (N3 p.17)", r"\theta^{new} = \theta^{old} - \alpha \nabla_{\theta} J(\theta)",
         [(r"\theta^{old}", "지금 가진 **파라미터(Parameter)** 전부"),
          (r"\alpha", "**학습률(Learning Rate)**, 한 걸음의 보폭"),
          (r"\nabla_{\theta} J(\theta)", "벌점 J 를 θ 로 미분한 **기울기(Gradient)**. 오르막 방향이에요"),
          (r"-", "빼기라서 오르막의 반대, 곧 내리막으로 가요")],
         "2주차 word2vec 때와 똑같은 식이에요. 새로운 문제는 여러 층에서 이 화살표를 어떻게 계산하느냐예요."),
    steps("손계산: 한 걸음 내려가기", [
        "J(θ) = θ² 이고 지금 θ = 3, **학습률(Learning Rate)** α = 0.1 이라고 해요",
        "**미분(Derivative)**: θ² 를 미분하면 2θ, θ = 3 에서 6",
        "업데이트: 3 - 0.1 x 6 = 3 - 0.6 = 2.4",
        "벌점: 3² = 9 에서 2.4² = 5.76 으로 줄었어요",
    ], "θ = 2.4, 벌점 9 → 5.76. **기울기(Gradient)** 만 알면 한 걸음은 쉬워요", "**경사 하강법(Gradient Descent)** 한 걸음이에요"),
    pts("미분은 살짝 밀기 (N3 p.18)", "**미분(Derivative)** 은 딱 한 가지 질문이에요",
        "x 를 살짝 밀면 f 는 얼마나 움직일까요", "그 답이 그래프의 기울기예요",
        "뒤의 모든 행렬 식도 이 생각을 키운 것뿐이에요"),
    steps("손계산: 정말 그런지 밀어 보기", [
        "f(x) = x³ 이면 도함수는 3x², x = 2 에서 3 x 4 = 12",
        "x = 2 에서 f = 8, x = 2.001 에서 f = 8.012006001",
        "움직인 양: 8.012006001 - 8 = 0.012006001",
        "밀어 준 양으로 나누기: 0.012006001 ÷ 0.001 = 12.006",
    ], "12.006 은 공식이 준 12 와 거의 같아요", "더 작게 밀수록 진짜 기울기에 가까워져요"),
    fig("숫자 하나에서 표까지 (N3 p.19)", SVG_JAC, "**미분(Derivative)** → **기울기(Gradient)** 벡터 → **야코비안(Jacobian)** 표. 생각은 같아요", 3),
    cmp_("셋을 나란히 (N3 p.19)", ["", "입력", "출력", "미분의 생김새"],
         [["**미분(Derivative)**", "1 개", "1 개", "숫자 하나"],
          ["**기울기(Gradient)**", "n 개", "1 개", "숫자 n 개짜리 벡터"],
          ["**야코비안(Jacobian)**", "n 개", "m 개", "m x n 표"]]),
    steps("손계산: 기울기와 야코비안", [
        "f(x1, x2) = x1² + 3x2 를 점 (1, 2) 에서 구해요",
        "x1 만 밀기: 2x1 = 2, x2 만 밀기: 3 → **기울기(Gradient)** 는 [2, 3]",
        "F(x1, x2, x3) = (x1 + 2x2, 3x3) 은 입력 3 개, 출력 2 개예요",
        "1행: x1 로 1, x2 로 2, x3 로 0 / 2행: 0, 0, 3",
        "표로 쌓으면 [[1, 2, 0], [0, 0, 3]]",
    ], "**기울기(Gradient)** [2, 3], **야코비안(Jacobian)** 은 2 x 3 표", "행은 출력, 열은 입력이에요"),
    ana("맞물린 톱니바퀴", "첫 바퀴가 한 칸 돌면 둘째가 3칸, 둘째가 한 칸 돌면 셋째가 8칸 돌아요. 그러면 첫 바퀴에서 셋째까지는 3 곱하기 8 이에요.",
        [("바퀴 하나의 회전비", "한 단계의 **미분(Derivative)**"), ("회전비를 곱하기", "**연쇄 법칙(Chain Rule)**"), ("처음에서 끝까지의 비", "전체 미분 dh/dx")]),
    fig("3배와 8배를 곱하면 (N3 p.20)", SVG_GEARS, "x 가 z 를 3배로, z 가 h 를 8배로. 그러면 x 는 h 를 24배로 움직여요", 3),
    steps("손계산: 연쇄 법칙을 숫자로", [
        "z = 3x + 1, h = z², x = 1 이라고 해요",
        "순서대로 계산: z = 4, h = 16",
        "첫 계단 dz/dx = 3, 둘째 계단 dh/dz = 2z = 8",
        "곱하기: dh/dx = 8 x 3 = 24",
        "확인: x 를 1.001 로 밀면 h = 16.024009, 늘어난 양 ÷ 0.001 = 24.009",
    ], "dh/dx = 24. 밀어 본 값 24.009 와 거의 같아요", "**연쇄 법칙(Chain Rule)** 은 더하기가 아니라 곱하기예요"),
    cmp_("주머니 속 야코비안 네 개 (N3 p.21)", ["블록", "계산", "무엇으로 미분", "결과"],
         [["곱하기", "Wx", "x", "W"],
          ["더하기", "Wx + b", "b", "단위 행렬 I"],
          ["활성화", "h = f(z)", "z", "대각 행렬 diag(f'(z))"],
          ["점수", "s = uh", "h", "u 를 눕힌 것"]]),
    pts("교수님이 짚은 곳", "**연쇄 법칙(Chain Rule)** 이 가장 중요하다고 보시면 돼요",
        "**야코비안(Jacobian)** 네 가지는 암기할 필요는 없지만, 수식을 이해하려면 외워 두면 좋아요",
        "이 규칙 하나를 신경망 전체에 체계적으로 적용한 것이 **역전파(Backpropagation)** 예요"),
    check("입력이 3 개, 출력이 2 개인 함수의 **야코비안(Jacobian)** 크기는?",
          ["2 x 3", "3 x 2", "3 x 3", "2 x 2"], 0, "행은 출력 수 2, 열은 입력 수 3 이에요."),
    check("z = 2x, h = z³, x = 1 일 때 dh/dx 는?",
          ["24", "6", "12", "8"], 0, "z = 2, dh/dz = 3z² = 12, dz/dx = 2, 곱하면 24 예요."),
    warn("헷갈리기 쉬운 점", "한 경로 위의 단계는 곱하고, 여러 경로가 만나면 그때 더해요.",
         "손실 J 와 **야코비안(Jacobian)** J 는 글자가 같지만 다른 것이에요.",
         "**역전파(Backpropagation)** 는 기울기를 구하는 방법이고, 파라미터를 고치는 것은 **경사 하강법(Gradient Descent)** 이에요."),
    recap("학습 = **경사 하강법(Gradient Descent)**, 새 문제는 **기울기(Gradient)** 계산",
          "**미분(Derivative)** → **기울기(Gradient)** 벡터 → **야코비안(Jacobian)** 표, 같은 생각이 자란 것",
          "**연쇄 법칙(Chain Rule)**: 단계마다 미분을 곱해요. 3 x 8 = 24",
          "오늘의 용어: 기울기, 경사 하강법, 학습률, 미분, 야코비안(Jacobian), 연쇄 법칙, 역전파"),
]})

# ---------------------------------------------------------------- w3-5
t = [T("오차 신호", "Error Signal", "출력 쪽에서 거꾸로 흘러와 한 층에 도착한 기울기, 기호 δ 예요.",
       "3강 예에서는 δ = ∂s/∂z 예요. 한 번 구해 b, W, x 의 기울기에 모두 다시 써요."),
     T("연쇄 법칙", "Chain Rule", "단계마다의 미분을 곱하면 전체 미분이 된다는 규칙이에요."),
     T("외적", "Outer Product", "세로 벡터 곱하기 가로 벡터로 표를 만드는 곱이에요."),
     T("전치", "Transpose", "행과 열을 뒤바꾸는 것. 위첨자 T 로 표시해요."),
     T("모양", "Shape", "벡터나 행렬이 몇 행 몇 열인지 적은 크기 정보예요."),
     T("임베딩", "Embedding", "토큰을 벡터로 바꾼 것, 또는 그 벡터들의 표예요."),
     T("역전파", "Backpropagation", "틀린 책임을 뒤에서 앞으로 나눠 주며 기울기를 구하는 방법이에요.")]
U.append({"id": "w3-5", "title": "손으로 푸는 역전파: δ 와 shape", "goal": "δ 를 한 번 구해 세 기울기를 모두 쓰고, shape 으로 식을 검사할 수 있어요.", "terms": t, "slides": [
    title("델타 하나로 셋을", "역전파를 손으로"),
    goal("작은 신경망의 순전파 손계산", "**연쇄 법칙(Chain Rule)** 으로 얻는 **오차 신호(Error Signal)** δ 와 세 기울기", "**모양(Shape)** 으로 식이 맞는지 검사하기"),
    fig("레고 블록 네 개 (N3 p.22)", SVG_LEGO, "x → z = Wx + b → h = f(z) → s. 블록마다 자기 미분 하나를 갖고 있어요", 4),
    steps("손계산: 작은 숫자로 순전파", [
        "x = [1, 2, 3], W = [[1, 0, 1], [-1, 1, -2]], b = [0, 1], u = [2, 3], f 는 ReLU",
        "Wx: 1행 1 + 0 + 3 = 4, 2행 -1 + 2 - 6 = -5 → [4, -5]",
        "z = Wx + b = [4, -4]",
        "h = ReLU(z) = [4, 0] (음수는 0)",
        "s = uh = 2x4 + 3x0 = 8",
    ], "s = 8. 크기는 x (3 x 1), W (2 x 3), z, h, b, u (2 x 1), s 는 숫자 하나", "n = 3 입력 칸, m = 2 은닉 칸이에요"),
    ana("틀린 책임 나눠 주기", "반 전체 점수가 낮게 나왔어요. 담임이 조장에게 책임 몫을 한 번 알려 주면, 조장은 그 몫으로 조원들에게 다시 나눠 줘요.",
        [("담임이 알려 준 책임 몫", "**오차 신호(Error Signal)** δ"), ("같은 몫을 여러 조원에게 다시 씀", "δ 를 b, W, x 에 다시 쓰기"), ("뒤에서 앞으로 책임 전달", "**역전파(Backpropagation)**")]),
    pts("겹치는 부분에 이름 붙이기 (N3 p.23)", "∂s/∂b 는 **연쇄 법칙(Chain Rule)** 으로 세 조각을 곱해요",
        "∂s/∂W 를 구하면 앞의 두 조각이 똑같아요",
        "그 똑같은 부분에 이름을 붙여요. δ, 곧 **오차 신호(Error Signal)** 예요",
        "한 번 구해서 계속 다시 쓰는 것, 이것이 **역전파(Backpropagation)** 의 씨앗이에요"),
    steps("손계산: δ 와 b, W 의 기울기", [
        "앞 장 값 그대로: z = [4, -4], u = [2, 3], x = [1, 2, 3], f 는 ReLU",
        "ReLU 의 미분: 양수면 1, 음수면 0 → f'(z) = [1, 0]",
        "δ = u 와 f'(z) 를 같은 자리끼리 곱하기 = [2x1, 3x0] = [2, 0]",
        "∂s/∂b = δ = [2, 0]",
        "∂s/∂W = δ 와 x 의 **외적(Outer Product)**: 1행 2x[1,2,3] = [2,4,6], 2행 0x[1,2,3] = [0,0,0]",
    ], "δ = [2, 0], ∂s/∂b = [2, 0], ∂s/∂W = [[2, 4, 6], [0, 0, 0]]", "확인: b1 을 0.1 올리면 s 가 8 에서 8.2 로, 0.2 ÷ 0.1 = 2 예요"),
    form("세 기울기 한 줄에 (N3 p.23, p.24)", r"\frac{\partial s}{\partial b} = \delta,\qquad \frac{\partial s}{\partial W} = \delta^{\top} x^{\top},\qquad \frac{\partial s}{\partial x} = W^{\top}\delta^{\top}",
         [(r"\delta", "**오차 신호(Error Signal)**. z 까지 흘러온 기울기예요"),
          (r"\delta^{\top} x^{\top}", "세로 곱하기 가로, 곧 **외적(Outer Product)**"),
          (r"W^{\top}", "W 를 **전치(Transpose)** 한 것"),
          (r"\frac{\partial s}{\partial x}", "입력 **임베딩(Embedding)** 으로 흘러 들어가는 기울기")],
         "b 는 δ 그대로, W 는 δ 에 x 를, x 는 δ 에 W 를 붙여요. δ 하나를 셋이 나눠 써요."),
    steps("손계산: 단어 벡터의 기울기와 한 걸음", [
        "δ = [2, 0], W = [[1, 0, 1], [-1, 1, -2]]",
        "W 를 **전치(Transpose)** 해서 δ 를 곱해요: 1칸 1x2 + (-1)x0 = 2",
        "2칸 0x2 + 1x0 = 0, 3칸 1x2 + (-2)x0 = 2 → ∂s/∂x = [2, 0, 2]",
        "**학습률(Learning Rate)** 0.1 로 한 걸음: [1, 2, 3] - 0.1 x [2, 0, 2] = [0.8, 2, 2.8]",
        "새 x 로 다시 계산: z = [3.6, -3.4], h = [3.6, 0], s = 7.2",
    ], "∂s/∂x = [2, 0, 2]. 한 걸음 뒤 s 는 8 에서 7.2 로 줄었어요", "이렇게 입력 **임베딩(Embedding)** 도 함께 학습돼요"),
    fig("크기가 맞는지 보기 (N3 p.25)", SVG_SHAPE3, "세로 (2 x 1) 곱하기 가로 (1 x 3) 은 (2 x 3), 곧 W 와 같은 크기예요", 3),
    steps("손계산: shape 으로 틀린 식 잡기", [
        "실습 크기: x 5칸, W (3, 5), b, z, h, u 3칸, s 는 숫자 하나",
        "δ 는 z 와 같은 3칸이에요",
        "∂s/∂W = (3 x 1) 곱하기 (1 x 5) = (3, 5) → W 와 같아요. 통과",
        "∂s/∂x = (5 x 3) 곱하기 (3 x 1) = (5, 1) → x 와 같아요. 통과",
        "잘못 쓴 예: x(5 x 1) 곱하기 δ(1 x 3) = (5, 3) 이라 W(3, 5) 와 달라요",
    ], "크기만 적어 봐도 코드를 돌리기 전에 틀린 식을 잡아요", "곱셈 규칙: (a x b)(b x c) = (a x c). 가운데가 같아야 해요"),
    pts("장부 정리 규칙 하나 (N3 p.26)", "파라미터의 기울기는 파라미터와 같은 **모양(Shape)** 이에요",
        "W 가 3 x 5 면 ∂J/∂W 도 3 x 5, 곧 15 칸이에요",
        "칸마다 짝이 있어야 W ← W - α∂J/∂W 처럼 한 칸씩 뺄 수 있어요",
        "교수님: **전치(Transpose)** 위치를 외우기보다 shape 을 맞춘다고 생각하세요"),
    check("δ(델타)는 무엇의 미분일까요?",
          ["s 를 z 로 미분한 것", "s 를 b 로 미분한 것", "h 를 x 로 미분한 것", "W 를 x 로 미분한 것"], 0,
          "δ = ∂s/∂h 곱하기 ∂h/∂z = ∂s/∂z 예요. z 까지 흘러온 기울기예요."),
    check("W 가 (3, 5) 일 때 ∂J/∂W 의 **모양(Shape)** 은?",
          ["(3, 5)", "(5, 3)", "(3, 1)", "(1, 5)"], 0, "파라미터의 기울기는 파라미터와 같은 크기예요."),
    check("∂s/∂x 에서 δ 에 곱해지는 것은?",
          ["W", "x", "b", "u"], 0, "z = Wx + b 를 x 로 미분하면 W 라서 δ 에 W 가 붙어요."),
    warn("헷갈리기 쉬운 점", "∂s/∂W 에는 x 가, ∂s/∂x 에는 W 가 붙어요. 서로 맞바꿔 붙는 것이에요.",
         "미리 학습된 단어 벡터는 얼려 둘 수도 있어요. x 를 업데이트할지는 선택이에요.",
         "과제 2 는 이 세 기울기의 word2vec 판을 손으로 유도하라고 해요. 과제와 이어지는 부분이에요."),
    recap("**순전파(Forward Pass)**: x = [1,2,3] → z = [4,-4] → h = [4,0] → s = 8",
          "**오차 신호(Error Signal)** δ = [2, 0] 하나로 ∂s/∂b, ∂s/∂W, ∂s/∂x 를 모두 써요",
          "**전치(Transpose)** 는 **모양(Shape)** 을 맞추려고 붙어요. 기울기는 파라미터와 같은 크기",
          "오늘의 용어: 오차 신호, 연쇄 법칙, 외적(Outer Product), 전치(Transpose), 모양(Shape), �