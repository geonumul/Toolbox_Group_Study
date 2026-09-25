# -*- coding: utf-8 -*-
"""참고 논문 덱(NP) Attention Is All You Need 회독 레슨 1~4쪽 생성기.
사용: python build_NP_001-004.py   출력: NP_001-004.json
손계산은 아래에서 파이썬으로 실제 계산해 assert 로 확인한다."""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "NP_001-004.json")


# ---------------- 손계산 확인 (계산하고 assert) ----------------
def softmax(a):
    m = max(a)
    e = [math.exp(x - m) for x in a]
    s = sum(e)
    return [v / s for v in e]


# 모델 크기 (논문 3.1, 3.2.2, 3.3)
D_MODEL, H, D_FF = 512, 8, 2048
D_K = D_MODEL // H
assert D_K == 64
assert D_FF == 4 * D_MODEL == 2048
assert math.sqrt(D_K) == 8.0

# 하위층 세기 (논문 3.1: 인코더 층마다 2개, 디코더 층마다 3개, N = 6)
N_LAYER = 6
ENC_SUB = N_LAYER * 2
DEC_SUB = N_LAYER * 3
assert ENC_SUB == 12 and DEC_SUB == 18 and ENC_SUB + DEC_SUB == 30

# 스케일드 닷프로덕트 손계산 (브리핑 5.3 과 같은 예)
RAW = [16.0, 8.0, 0.0]
SCALED = [v / math.sqrt(D_K) for v in RAW]
assert SCALED == [2.0, 1.0, 0.0]
AL = [round(v, 4) for v in softmax(SCALED)]
assert AL == [0.6652, 0.2447, 0.09]
assert abs(sum(softmax(SCALED)) - 1.0) < 1e-12
assert abs(sum(AL) - 1.0) < 2e-4  # 반올림한 값이라 딱 1 은 아니에요
AL_RAW = [round(v, 6) for v in softmax(RAW)]
assert AL_RAW == [0.999665, 0.000335, 0.0]
V3 = [[1.0, 0.0], [0.0, 2.0], [2.0, 2.0]]
OUT3 = [round(sum(AL[i] * V3[i][c] for i in range(3)), 4) for c in range(2)]
assert OUT3 == [0.8452, 0.6694]

# 각주 4: q 와 k 의 성분이 평균 0, 분산 1 이면 내적의 분산은 d_k
assert round(math.sqrt(D_K), 4) == 8.0
assert round(math.sqrt(D_MODEL), 2) == 22.63

# 초록의 학습 시간 (논문이 직접 적지 않은 값. 우리가 센 것이라고 밝히고 쓴다)
BIG_HOURS = 3.5 * 24
assert BIG_HOURS == 84.0
BIG_GPU_HOURS = BIG_HOURS * 8
assert BIG_GPU_HOURS == 672.0
assert round(12 * 8, 1) == 96  # base 는 12시간 x 8장 = 96 GPU 시간

# 초록의 BLEU 차이 (Table 2 의 최고 앙상블 26.36 과 비교)
assert round(28.4 - 26.36, 2) == 2.04


# ---------------- 용어 표기 ----------------
TRF = "**트랜스포머(Transformer)**"
ATT = "**어텐션(Attention)**"
SA = "**셀프 어텐션(Self-Attention)**"
CA = "**크로스 어텐션(Cross-Attention)**"
SDP = "**스케일드 닷프로덕트 어텐션(Scaled Dot-Product Attention)**"
MHA = "**멀티 헤드 어텐션(Multi-Head Attention (MHA))**"
HEAD = "**헤드(Head)**"
QRY = "**쿼리(Query)**"
KEY = "**키(Key)**"
VAL = "**밸류(Value)**"
ASC = "**어텐션 점수(Attention Score)**"
AW = "**어텐션 가중치(Attention Weight)**"
WSUM = "**가중합(Weighted Sum)**"
SMX = "**소프트맥스(Softmax)**"
DP = "**내적(Dot Product)**"
ENC = "**인코더(Encoder)**"
DEC = "**디코더(Decoder)**"
SUB = "**하위층(Sub-layer)**"
RES = "**잔차 연결(Residual Connection)**"
LN = "**층 정규화(Layer Normalization (LayerNorm))**"
FFN = "**위치별 피드포워드 신경망(Position-wise Feed-Forward Network (FFN))**"
PE = "**위치 인코딩(Positional Encoding)**"
EMB = "**임베딩(Embedding)**"
TOK = "**토큰(Token)**"
PARAM = "**파라미터(Parameter)**"
CM = "**인과 마스킹(Causal Masking)**"
AR = "**자기회귀(Autoregressive)**"
PAR = "**병렬화(Parallelization)**"
RNN = "**순환 신경망(Recurrent Neural Network (RNN))**"
LSTM = "**장단기 메모리(LSTM)**"
HS = "**은닉 상태(Hidden State)**"
CNN = "**합성곱 신경망(Convolutional Neural Network (CNN))**"
MT = "**기계 번역(Machine Translation (MT))**"
BLEU = "**블루 점수(BLEU)**"
SEQT = "**시퀀스 변환(Sequence Transduction)**"
MPL = "**최대 경로 길이(Maximum Path Length)**"
SEQOP = "**순차 연산 수(Sequential Operations)**"
CF = "**호환성 함수(Compatibility Function)**"
ADD = "**가산 어텐션(Additive Attention)**"
DPA = "**닷프로덕트 어텐션(Dot-Product Attention)**"
GRAD = "**기울기(Gradient)**"
CP = "**구성소 구문 분석(Constituency Parsing)**"
S2S = "**시퀀스-투-시퀀스(seq2seq)**"
LLM = "**대규모 언어 모델(Large Language Model (LLM))**"
BPE = "**바이트 쌍 인코딩(Byte Pair Encoding (BPE))**"

WHEN = "4주차 월요일 수업"

GLOSSARY = [
    ("트랜스포머", "Transformer", "어텐션만으로 만든 신경망 구조. 이 논문이 내놓은 모델이에요",
     "순환도 합성곱도 쓰지 않고 어텐션만 씁니다. 인코더 6층과 디코더 6층으로 되어 있어요."),
    ("어텐션", "Attention", "필요한 곳을 골라 보는 장치. 점수를 매기고 가중 평균을 내요",
     "논문은 쿼리와 키-밸류 쌍을 출력으로 보내는 함수라고 정의했어요."),
    ("셀프 어텐션", "Self-Attention", "한 문장이 자기 자신을 바라보는 어텐션",
     "쿼리, 키, 밸류가 모두 같은 자리에서 나와요. 논문 2장은 intra-attention 이라고도 부른다고 적었어요."),
    ("크로스 어텐션", "Cross-Attention", "쿼리는 디코더, 키와 밸류는 인코더에서 오는 어텐션",
     "논문은 이것을 encoder-decoder attention 이라고 불러요. 이름이 다를 뿐 같은 것이에요."),
    ("스케일드 닷프로덕트 어텐션", "Scaled Dot-Product Attention", "내적 점수를 루트 d_k 로 나눈 어텐션",
     "논문 3.2.1 의 이름이고 식 (1) 이 그 정의예요. 나누기 한 번이 학습을 살려요."),
    ("멀티 헤드 어텐션", "Multi-Head Attention (MHA)", "전체 차원을 h 조각으로 나눠 여러 관점에서 동시에 어텐션하기",
     "논문은 h = 8 을 썼고 헤드마다 64칸이에요. 계산량은 한 개짜리와 비슷해요."),
    ("헤드", "Head", "멀티 헤드 어텐션에서 한 관점을 맡은 작은 어텐션 하나",
     "헤드 하나가 d_k = d_v = 64 칸을 봐요. 8개를 이어 붙여 다시 512 칸이 돼요."),
    ("쿼리", "Query", "지금 내가 무엇을 찾고 있는지를 담은 벡터",
     "논문 3.2 는 어텐션을 쿼리와 키-밸류 쌍의 대응이라고 정의해요."),
    ("키", "Key", "나는 이런 정보를 갖고 있다고 광고하는 이름표 벡터",
     "쿼리와 키를 내적해서 점수를 만들어요. 사전의 색인 같은 역할이에요."),
    ("밸류", "Value", "내가 선택되면 실제로 건네줄 내용 벡터",
     "가중합에 실제로 들어가는 것은 키가 아니라 밸류예요."),
    ("어텐션 점수", "Attention Score", "두 벡터가 얼마나 관련 있는지 나타낸 날것 숫자",
     "논문에서는 쿼리와 키의 내적을 루트 d_k 로 나눈 값이에요."),
    ("어텐션 가중치", "Attention Weight", "점수를 소프트맥스에 넣어 얻은, 합이 1 인 값들",
     "논문 3.2 는 이것을 호환성 함수가 만든 weight 라고 불러요."),
    ("가중합", "Weighted Sum", "값마다 가중치를 곱해서 모두 더한 것",
     "논문의 정의 문장 The output is computed as a weighted sum of the values 가 이것이에요."),
    ("소프트맥스", "Softmax", "점수를 모두 더해 1 이 되는 확률 파이로 나누기",
     "각 점수에 exp 를 씌운 뒤 전체 합으로 나눠요. 점수가 크면 분포가 뾰족해져요."),
    ("내적", "Dot Product", "두 화살표가 얼마나 같은 쪽을 보는지 재는 곱셈",
     "같은 자리끼리 곱해서 모두 더해요. 논문의 점수가 바로 이것이에요."),
    ("인코더", "Encoder", "입력 문장을 끝까지 읽어 자리마다 표현을 만드는 쪽",
     "논문의 인코더는 N = 6 층이고 층마다 하위층이 둘이에요."),
    ("디코더", "Decoder", "답 문장을 한 토큰씩 만들어 내는 쪽",
     "논문의 디코더는 N = 6 층이고 층마다 하위층이 셋이에요."),
    ("하위층", "Sub-layer", "한 층 안에 들어 있는 더 작은 층 한 덩어리",
     "논문은 sub-layer 라고 적어요. 인코더 층은 2개, 디코더 층은 3개를 가져요."),
    ("잔차 연결", "Residual Connection", "층의 입력을 층의 출력에 그대로 더해 주는 지름길",
     "논문은 하위층마다 이것을 두르고 그다음에 층 정규화를 해요."),
    ("층 정규화", "Layer Normalization (LayerNorm)", "한 토큰의 숫자들을 평균 0, 분산 1 로 맞춰 주기",
     "논문의 식은 LayerNorm(x + Sublayer(x)) 이라 더한 뒤에 정규화해요."),
    ("위치별 피드포워드 신경망", "Position-wise Feed-Forward Network (FFN)", "자리마다 똑같이 적용하는 2층짜리 작은 신경망",
     "논문 3.3 의 부품이에요. 가운데 차원이 2048 이라 파라미터가 많아요."),
    ("위치 인코딩", "Positional Encoding", "몇 번째 자리인지를 알려 주는 벡터를 임베딩에 더해 주기",
     "논문은 인코더와 디코더 스택 맨 아래에서 딱 한 번 더해요."),
    ("임베딩", "Embedding", "토큰을 숫자 벡터로 바꾼 것. 단어의 지도 좌표",
     "논문의 임베딩 차원은 d_model = 512 예요. 위치 인코딩이 여기에 더해져요."),
    ("토큰", "Token", "글을 자른 레고 조각 하나",
     "논문은 BPE 로 자른 조각을 토큰으로 써요. 어휘가 약 37,000 개예요."),
    ("파라미터", "Parameter", "학습하면서 바뀌는 숫자. 모델이 기억을 저장하는 자리",
     "논문의 base 모델은 약 65 x 10^6 개를 가져요."),
    ("인과 마스킹", "Causal Masking", "미래 자리의 점수를 소프트맥스 전에 마이너스 무한으로 바꾸기",
     "논문 3.2.3 은 masking out (setting to 마이너스 무한) 이라고 적었어요."),
    ("자기회귀", "Autoregressive", "앞에서 만든 토큰을 보고 다음 토큰을 하나씩 만드는 방식",
     "논문 3장 첫 문단이 auto-regressive 라고 적은 성질이에요."),
    ("병렬화", "Parallelization", "여러 계산을 한꺼번에 동시에 하기",
     "논문이 순환을 버린 가장 큰 이유예요. 교수님도 패러럴이 핵심이라고 했어요."),
    ("순환 신경망", "Recurrent Neural Network (RNN)", "한 단어씩 읽으며 메모장에 요약을 고쳐 쓰는 신경망",
     "논문은 이것을 통째로 걷어냈어요. 한 걸음씩 가야 해서 병렬화가 막혀요."),
    ("장단기 메모리", "LSTM", "RNN 에 게이트를 달아 긴 문장을 덜 잊게 만든 모델",
     "논문 첫 문장이 state of the art 로 꼽은 것이 이것과 GRU 예요."),
    ("은닉 상태", "Hidden State", "지금까지 읽은 내용을 요약해 들고 다니는 숫자 벡터",
     "논문은 h_t 가 h_(t-1) 과 t 번째 입력의 함수라고 적었어요."),
    ("합성곱 신경망", "Convolutional Neural Network (CNN)", "가까운 이웃 몇 칸을 묶어서 보는 신경망",
     "논문 2장이 비교 대상으로 꼽은 ByteNet, ConvS2S 가 이것을 씁니다."),
    ("기계 번역", "Machine Translation (MT)", "한 언어 문장을 다른 언어 문장으로 바꾸는 과제",
     "논문의 주 실험이 WMT 2014 영어-독일어, 영어-프랑스어 번역이에요."),
    ("블루 점수", "BLEU", "기계 번역 결과가 사람 번역과 얼마나 겹치는지 재는 점수",
     "높을수록 좋아요. 논문은 영어-독일어에서 28.4 를 얻었어요."),
    ("시퀀스 변환", "Sequence Transduction", "줄줄이 늘어선 입력을 줄줄이 늘어선 출력으로 바꾸는 일",
     "논문 초록 첫 단어가 sequence transduction models 예요. 번역이 대표 예예요."),
    ("최대 경로 길이", "Maximum Path Length", "두 자리 사이에 신호가 지나가야 하는 가장 먼 걸음 수",
     "짧을수록 멀리 떨어진 단어끼리 배우기 쉬워요. 논문 Table 1 의 세 번째 칸이에요."),
    ("호환성 함수", "Compatibility Function", "쿼리와 키가 얼마나 어울리는지 점수로 매기는 함수",
     "논문 3.2 의 정의에 나오는 말이에요. 여기서는 그냥 내적이에요."),
    ("가산 어텐션", "Additive Attention", "작은 신경망으로 점수를 매기는 옛날 어텐션 방식",
     "은닉층 한 개짜리 피드포워드 신경망을 써요. 2015년 방식이에요."),
    ("닷프로덕트 어텐션", "Dot-Product Attention", "쿼리와 키를 그냥 내적해서 점수를 매기는 방식",
     "논문은 여기에 루트 d_k 나누기만 더했다고 적었어요."),
    ("기울기", "Gradient", "손실이 가장 빨리 커지는 방향과 그 가파름",
     "소프트맥스가 포화되면 기울기가 거의 0 이 돼서 학습이 멈춰요."),
    ("구성소 구문 분석", "Constituency Parsing", "문장을 구 단위 나무 구조로 쪼개는 과제",
     "논문이 번역 말고 하나 더 해 본 과제예요. 초록 마지막 문장에 나와요."),
    ("대규모 언어 모델", "Large Language Model (LLM)", "트랜스포머를 아주 크게 쌓은 언어 모델",
     "교수님: 트랜스포머를 좀 크게 쌓으면 그게 LLM 이다 이렇게 보셔도 된다."),
]


# ---------------- 장면 도우미 ----------------
def say(*lines):
    return {"kind": "say", "lines": list(lines)}


def look(head, *boxes):
    return {"kind": "look", "head": head,
            "boxes": [{"x": b[0], "y": b[1], "w": b[2], "h": b[3], "say": b[4]} for b in boxes]}


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
            "parts": [{"sym": s, "say": t} for s, t in parts], "whole": whole}


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


# ---------------- SVG 도우미 ----------------
def _c(cls, b):
    return f"{cls} b{b}" if b else cls


def SVG(*els, h=270):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 {h}">' + "".join(els) + "</svg>"


def TX(x, y, s, cls="t", size=15, anchor="middle", b=0):
    return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" class="{_c(cls, b)}">{s}</text>'


def R(x, y, w, h, cls="n", b=0):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" class="{_c(cls, b)}"/>'


def L(x1, y1, x2, y2, cls="e", b=0):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{_c(cls, b)}"/>'


def A(x1, y1, x2, y2, cls="e2", b=0):
    ang = math.atan2(y2 - y1, x2 - x1)
    s = 8
    p1 = (x2 - s * math.cos(ang) + s * 0.5 * math.sin(ang), y2 - s * math.sin(ang) - s * 0.5 * math.cos(ang))
    p2 = (x2 - s * math.cos(ang) - s * 0.5 * math.sin(ang), y2 - s * math.sin(ang) + s * 0.5 * math.cos(ang))
    lx, ly = x2 - s * 0.8 * math.cos(ang), y2 - s * 0.8 * math.sin(ang)
    pts = f"{x2},{y2} {p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return L(x1, y1, round(lx, 1), round(ly, 1), cls, b) + f'<polygon points="{pts}" class="{_c("arrow", b)}"/>'


def BOX(x, y, w, h, s, cls="box", tcls="tb", b=0, size=14):
    return R(x, y, w, h, cls, b) + TX(x + w / 2, y + h / 2 + size * 0.35, s, tcls, size, "middle", b)


# ---- 그림들
FIG_ABS = SVG(
    TX(240, 22, "초록 한 문단이 말하는 네 가지", "tb", 16),
    BOX(40, 40, 400, 30, "1. 순환과 합성곱을 통째로 버렸다", "box2", "tb", 1, 13),
    BOX(40, 78, 400, 30, "2. 어텐션만으로 만든 새 구조, Transformer", "box2", "tb", 2, 13),
    BOX(40, 116, 400, 30, "3. 더 잘 번역하고 더 빨리 배운다", "box2", "tb", 3, 13),
    BOX(40, 154, 400, 30, "4. 구문 분석에도 잘 통한다", "box2", "tb", 4, 13),
    TX(240, 212, "영어-독일어 28.4, 영어-프랑스어 41.8 이 그 증거예요", "tb", 13, "middle", 4),
    TX(240, 236, "GPU 8장으로 3.5일이면 끝났다고 적었어요", "tm", 12, "middle", 4),
)

FIG_WHY = SVG(
    TX(240, 22, "한 걸음씩 vs 한꺼번에", "tb", 16),
    *[BOX(24 + i * 84, 46, 72, 28, t, "n", "tl", 1, 12)
      for i, t in enumerate(["x1", "x2", "x3", "x4", "x5"])],
    *[A(96 + i * 84, 60, 108 + i * 84, 60, "e", 2) for i in range(4)],
    TX(240, 96, "RNN: h1 을 만들어야 h2 를 만들 수 있어요", "t", 13, "middle", 2),
    TX(240, 118, "그래서 한 문장 안에서는 동시에 계산할 수 없어요", "tm", 12, "middle", 2),
    *[BOX(24 + i * 84, 140, 72, 28, t, "box2", "tb", 3, 12)
      for i, t in enumerate(["x1", "x2", "x3", "x4", "x5"])],
    *[A(60 + i * 84, 172, 240, 196, "e2", 3) for i in range(5)],
    BOX(150, 198, 180, 28, "한 번의 행렬 곱", "box", "tb", 4, 13),
    TX(240, 250, "트랜스포머: 다섯 자리를 한꺼번에 계산해요", "tb", 13, "middle", 4),
)

FIG_STACK = SVG(
    TX(240, 20, "인코더 6층, 디코더 6층", "tb", 16),
    TX(120, 44, "인코더 한 층", "tb", 13),
    BOX(30, 54, 180, 26, "2. 위치별 FFN", "box2", "tb", 1, 12),
    BOX(30, 86, 180, 26, "1. 멀티 헤드 셀프 어텐션", "box2", "tb", 1, 12),
    TX(120, 132, "하위층 2개", "tm", 12, "middle", 2),
    TX(360, 44, "디코더 한 층", "tb", 13),
    BOX(270, 54, 180, 26, "3. 위치별 FFN", "box", "tb", 1, 12),
    BOX(270, 86, 180, 26, "2. 크로스 어텐션", "box", "tb", 1, 12),
    BOX(270, 118, 180, 26, "1. 마스크드 셀프 어텐션", "box", "tb", 1, 12),
    TX(360, 164, "하위층 3개", "tm", 12, "middle", 2),
    TX(240, 196, "하위층마다 잔차 연결을 두르고 층 정규화를 해요", "tb", 13, "middle", 3),
    TX(240, 220, "LayerNorm(x + Sublayer(x)), 곧 더한 뒤에 정규화예요", "t", 13, "middle", 3),
    TX(240, 246, "하위층 전부 세면 6 x 2 + 6 x 3 = 30 개예요", "tm", 12, "middle", 4),
)

FIG_SDP = SVG(
    TX(240, 22, "식 (1) 을 왼쪽에서 오른쪽으로", "tb", 16),
    BOX(16, 54, 74, 34, "Q", "box2", "tb", 1, 14),
    BOX(100, 54, 74, 34, "K^T", "box2", "tb", 1, 14),
    A(176, 71, 200, 71, "e2", 2),
    BOX(206, 54, 84, 34, "내적 점수", "box", "tb", 2, 13),
    A(292, 71, 316, 71, "e2", 3),
    BOX(322, 54, 142, 34, "루트 d_k 로 나누기", "box", "tb", 3, 13),
    A(393, 92, 393, 116, "e2", 4),
    BOX(322, 120, 142, 34, "소프트맥스", "box2", "tb", 4, 13),
    A(316, 137, 292, 137, "e2", 4),
    BOX(206, 120, 84, 34, "V 와 곱", "box2", "tb", 4, 13),
    TX(240, 186, "d_k = 64 이면 루트 d_k = 8 이에요", "tb", 13, "middle", 4),
    TX(240, 210, "점수 16, 8, 0 을 8로 나누면 2, 1, 0 이 돼요", "t", 13, "middle", 4),
    TX(240, 234, "소프트맥스는 0.6652, 0.2447, 0.0900 이에요", "tm", 12, "middle", 4),
)

S = []


def page(p, title, terms, p1, p2=(), p3=(), p4=()):
    S.append({"p": p, "title": title, "terms": list(terms),
              "pass1": list(p1), "pass2": list(p2), "pass3": list(p3), "pass4": list(p4)})


# ---------------------------------------------------------------- p.1
page(1, "제목과 초록: 논문 전체가 한 쪽에 들어 있어요",
     ["Transformer", "Attention", "Sequence Transduction", "Recurrent Neural Network (RNN)",
      "Convolutional Neural Network (CNN)", "Encoder", "Decoder", "Machine Translation (MT)",
      "BLEU", "Parallelization", "Constituency Parsing", "Self-Attention"],
     [say("논문의 첫 쪽이에요. 제목, 저자 여덟 명, 초록(Abstract)이 들어 있어요.",
          "제목 Attention Is All You Need 는 어텐션만 있으면 된다는 뜻이에요.",
          f"초록 한 문단에 이 논문의 주장이 다 들어 있어요. {TRF} 를 내놓겠다는 선언이에요.",
          "4주차 강의에서 배운 어텐션이 여기서 주인공이 돼요."),
      analogy("영화 예고편",
              "초록은 논문의 예고편이에요. 2분짜리 예고편만 봐도 어떤 영화인지 알 수 있는 것처럼, 초록만 읽어도 주장이 보여요.",
              ("예고편", "초록(Abstract)"),
              ("주인공", TRF),
              ("흥행 성적", BLEU),
              ("빼 버린 조연", RNN)),
      points("이 쪽에서 챙길 것 세 가지",
             f"논문이 무엇을 버렸는지: {RNN} 과 {CNN} 을 통째로 버렸어요",
             f"논문이 무엇을 남겼는지: {ATT} 하나만 남겼어요",
             f"논문이 내세운 증거: {MT} 성적과 학습 시간, 그리고 {CP}")],
     [points("초록의 영어와 우리말 뜻",
             f'"**sequence transduction models**" = {SEQT} 모델, 곧 번역처럼 줄을 줄로 바꾸는 모델',
             '"**dispensing with recurrence and convolutions entirely**" = 순환과 합성곱을 통째로 없앤다',
             '"**based solely on attention mechanisms**" = 오직 어텐션 장치에만 기댄다',
             '"**more parallelizable**" = 더 많이 동시에 계산할 수 있다',
             '"**state-of-the-art**" = 그때까지 나온 것 중 가장 좋은 성적'),
      compare("초록이 버린 것과 남긴 것",
              ["무엇", "초록의 표현", "우리말"],
              [RNN, "recurrence", "한 걸음씩 도는 구조를 없앴어요"],
              [CNN, "convolutions", "이웃 몇 칸 묶어 보는 구조도 없앴어요"],
              [ATT, "solely on attention", "이것 하나만 남겼어요"],
              [f"{ENC} 와 {DEC}", "encoder and decoder", "이 틀은 그대로 썼어요"]),
      steps("초록을 읽는 순서",
            ["1. 지금까지는 무엇이 최고였나: 복잡한 순환 또는 합성곱 신경망",
             f"2. 그런데 좋은 모델은 다 {ENC} 와 {DEC} 를 {ATT} 으로 이었다",
             f"3. 우리는 {ATT} 만으로 된 새 구조 {TRF} 를 낸다",
             "4. 증거 1: 영어-독일어 28.4, 영어-프랑스어 41.8",
             f"5. 증거 2: GPU 8장으로 3.5일, {PAR} 가 잘 된다",
             f"6. 증거 3: 번역 말고 {CP} 에도 잘 통한다"],
            "버린 것, 남긴 것, 증거 셋. 이 순서로 읽으면 초록이 한눈에 들어와요."),
      check("제목 Attention Is All You Need 가 뜻하는 것은?",
            ["어텐션만 있으면 된다", "어텐션이 필요 없다", "어텐션은 하나만 써라", "어텐션을 모두 모아라"], 0,
            f"{RNN} 도 {CNN} 도 없이 {ATT} 하나로 만들었다는 선언이에요.")],
     [look("첫 쪽을 짚어 읽어요",
           (0.18, 0.088, 0.64, 0.055, "맨 위 빨간 글씨는 표와 그림을 학술 목적으로 써도 된다는 구글의 허락 문구예요."),
           (0.33, 0.185, 0.34, 0.04, "제목 Attention Is All You Need. 어텐션만 있으면 된다는 뜻이에요."),
           (0.17, 0.29, 0.68, 0.17, "저자 여덟 명과 소속. 구글 브레인, 구글 리서치, 토론토대가 보여요."),
           (0.22, 0.49, 0.56, 0.25, "Abstract 본문. 이 한 문단이 논문 전체의 주장이에요."),
           (0.17, 0.745, 0.66, 0.145, "별표 각주. 여덟 명이 동등 기여이고 이름 순서는 무작위라고 적었어요."),
           (0.17, 0.895, 0.60, 0.028, "맨 아래 한 줄. NIPS 2017 학회에서 발표한 논문이에요.")),
      points("각주가 알려 주는 역할 분담 (논문 1쪽 별표 각주)",
             "Jakob 이 RNN 을 셀프 어텐션으로 바꾸자고 처음 제안했다고 적었어요",
             f"Noam 이 {SDP}, {MHA}, 그리고 파라미터 없는 위치 표현을 제안했다고 적었어요",
             "Ashish 와 Illia 가 첫 트랜스포머 모델을 설계하고 구현했다고 적었어요",
             "Listing order is random, 곧 저자 이름 순서에 서열이 없다는 뜻이에요"),
      compare("초록이 내놓은 숫자만 모으기",
              ["항목", "값", "어디 이야기인가"],
              [f"{BLEU} 영어-독일어", "28.4", "WMT 2014 번역 과제"],
              [f"{BLEU} 영어-프랑스어", "41.8", "단일 모델 최고 기록이라고 적음"],
              ["기존 최고보다", "2 BLEU 넘게", "앙상블까지 포함해서 비교"],
              ["학습 시간", "GPU 8장으로 3.5일", "big 모델 기준"]),
      steps("3.5일이 GPU 시간으로 얼마인지 직접 세어 봐요",
            ["3.5일 x 24시간 = 84시간이에요",
             "GPU 가 8장이니 84 x 8 = 672 GPU 시간이에요",
             "논문 5.2 의 base 모델은 12시간이니 12 x 8 = 96 GPU 시간이에요",
             "672 / 96 = 7 이라서 big 이 base 보다 7배 오래 걸렸어요"],
            "big 은 672 GPU 시간, base 는 96 GPU 시간이에요. 논문이 이 곱셈을 직접 적지는 않았어요.",
            "3.5일, GPU 8장"),
      prof("교수님: 이 논문은 인공지능 학과로서 매우 중요한 논문이에요.",
           "교수님: 무조건 꼭 읽어 보시는 걸 매우 추천합니다.",
           "교수님: 읽어서 이해하면 시험도 나중에 잘 볼 수 있어요."),
      figure("초록의 네 가지 주장", FIG_ABS, "버린 것, 남긴 것, 증거 둘로 나뉘어요.", 4)],
     [check("초록이 완전히 없앴다고 말한 두 가지는?",
            ["순환과 합성곱", "인코더와 디코더", "어텐션과 소프트맥스", "임베딩과 위치 인코딩"], 0,
            f"dispensing with recurrence and convolutions entirely 예요. {ENC} 와 {DEC} 는 그대로 남겼어요."),
      english("시험 답안 문장",
              "트랜스포머는 순환과 합성곱을 전부 없애고 어텐션만으로 만든 시퀀스 변환 모델로, 번역 품질과 학습 속도를 동시에 높였다.",
              "버린 것 둘, 남긴 것 하나, 좋아진 것 둘을 한 문장에 담아요.",
              "버리고, 남기고, 빨라졌다. 세 박자로 외워요."),
      warn("헷갈리기 쉬운 점",
           f"{ENC} 와 {DEC} 구조까지 버린 게 아니에요. 버린 것은 순환과 합성곱이에요.",
           "초록의 41.8 은 Table 2 와 같지만, 본문 6.1 은 41.0 이라고 적었어요. 논문 안이 어긋나 있어요.",
           "by over 2 BLEU 는 영어-독일어 이야기예요. 영어-프랑스어 이야기가 아니에요."),
      exam("예상 문제",
           "Attention Is All You Need 의 초록이 주장한 핵심 세 가지를 쓰시오.",
           "초록이 내세운 주장 세 가지를 적는 문제예요.",
           ["1. 순환과 합성곱을 완전히 버리고 어텐션만 쓴다",
            "2. 번역 품질이 더 좋다 (영어-독일어 28.4, 영어-프랑스어 41.8)",
            "3. 더 병렬화되고 학습 시간이 훨씬 짧다 (GPU 8장 3.5일)",
            "여유가 있으면 구성소 구문 분석에도 잘 통한다를 덧붙여요"],
           "어텐션만 쓴다, 더 정확하다, 더 빠르다. 이 셋이에요.")])

# ---------------------------------------------------------------- p.2
page(2, "1 Introduction 과 2 Background: 왜 순환을 버렸나",
     ["Recurrent Neural Network (RNN)", "LSTM", "Hidden State", "Parallelization", "Attention",
      "Self-Attention", "Transformer", "Encoder", "Decoder", "Convolutional Neural Network (CNN)",
      "Sequence Transduction", "Maximum Path Length", "Multi-Head Attention (MHA)",
      "Autoregressive", "Machine Translation (MT)", "Token"],
     [say(f"1장은 {RNN} 과 {LSTM} 이 왜 답답한지 말해요. 2장은 남들이 어떻게 풀려 했는지 말해요.",
          f"핵심 불만은 하나예요. {RNN} 은 앞 자리를 끝내야 뒤 자리를 계산할 수 있어요.",
          f"그래서 한 문장 안에서 {PAR} 가 막혀요. 문장이 길수록 더 답답해져요.",
          f"논문은 {ATT} 만 남기면 이 족쇄가 풀린다고 말해요."),
      analogy("줄 서서 쪽지 넘기기",
              "교실에서 맨 앞 사람이 쪽지를 뒤로 한 명씩 넘기면 사람 수만큼 시간이 걸려요. 대신 모두가 동시에 칠판을 보면 한 번에 끝나요.",
              ("한 명씩 넘기기", RNN),
              ("넘기면서 들고 있는 쪽지", HS),
              ("모두가 동시에 보기", SA),
              ("걸리는 시간이 확 줄기", PAR))],
     [points("1장의 영어와 우리말 뜻",
             '"**sequence of hidden states**" = 은닉 상태를 줄줄이 만든다',
             '"**This inherently sequential nature precludes parallelization**" = 이 차례차례 성질이 병렬화를 막는다',
             '"**without regard to their distance**" = 거리와 상관없이, 곧 멀리 있어도 바로 이어 준다',
             '"**eschewing recurrence**" = 순환을 피한다, 쓰지 않는다',
             '"**as little as twelve hours on eight P100 GPUs**" = P100 8장으로 열두 시간이면 된다'),
      points("2장의 영어와 우리말 뜻",
             '"**Self-attention, sometimes called intra-attention**" = 셀프 어텐션은 intra-attention 이라고도 부른다',
             '"**relating different positions of a single sequence**" = 한 시퀀스 안의 서로 다른 자리를 이어 준다',
             '"**reduced to a constant number of operations**" = 연산 수가 거리와 상관없이 일정해진다',
             '"**the first transduction model relying entirely on self-attention**" = 셀프 어텐션만으로 된 첫 모델',
             '"**auto-regressive**" = 앞에서 만든 것을 다시 입력으로 쓰는 방식'),
      compare(f"멀리 떨어진 두 단어를 잇는 걸음 수, 곧 {MPL}",
              ["모델", "걸음 수가 어떻게 늘어나나", "논문의 말"],
              ["ConvS2S", "거리에 비례해서 늘어나요", "linearly"],
              ["ByteNet", "거리의 로그만큼 늘어나요", "logarithmically"],
              [f"{RNN} 과 {LSTM}", "자리 수만큼 늘어나요", "2장에서는 값을 적지 않았어요"],
              [TRF, "거리와 상관없이 일정해요", "a constant number of operations"]),
      steps("RNN 이 왜 줄을 서야 하는지 한 줄씩",
            [f"1. t 번째 {HS} h_t 를 만들려면 h_(t-1) 이 있어야 해요",
             "2. h_(t-1) 을 만들려면 h_(t-2) 가 있어야 해요",
             "3. 그래서 h_1, h_2, h_3 순서대로만 만들 수 있어요",
             f"4. 자리 다섯 개면 다섯 번을 차례로 기다려야 해요. {PAR} 가 막혀요",
             "5. 논문은 이것을 fundamental constraint of sequential computation 이라고 불러요"],
            f"{RNN} 의 답답함은 느려서가 아니라 순서 때문이에요. 이게 1장의 핵심이에요."),
      check("논문이 말한 RNN 의 근본 제약은?",
            ["차례차례 계산해야 해서 병렬화가 막힌다", "파라미터가 너무 많다",
             "인코더가 없다", "소프트맥스를 못 쓴다"], 0,
            f"This inherently sequential nature precludes parallelization 이 그 문장이에요. {PAR} 가 막혀요.")],
     [look("1장을 짚어 읽어요",
           (0.17, 0.088, 0.25, 0.025, "1 Introduction 제목이에요."),
           (0.17, 0.123, 0.66, 0.072, "첫 문단: RNN, LSTM, GRU 가 그때까지 최고였다고 인정하고 시작해요."),
           (0.17, 0.20, 0.66, 0.112, "둘째 문단: h_t 를 h_(t-1) 과 입력으로 만든다, 그래서 병렬화가 막힌다."),
           (0.17, 0.318, 0.66, 0.055, "셋째 문단: 어텐션은 거리와 상관없이 이어 주지만, 대개 RNN 과 같이 쓴다."),
           (0.17, 0.38, 0.66, 0.062, "넷째 문단: 그래서 우리는 순환을 버린 트랜스포머를 낸다는 선언이에요."),
           (0.17, 0.458, 0.25, 0.025, "2 Background 제목이에요.")),
      look("2장과 3장 첫 문단을 짚어 읽어요",
           (0.17, 0.49, 0.66, 0.125, "합성곱을 쓴 Extended Neural GPU, ByteNet, ConvS2S 를 먼저 소개해요."),
           (0.17, 0.593, 0.66, 0.022, "여기가 Multi-Head Attention 을 처음 예고하는 줄이에요."),
           (0.17, 0.622, 0.66, 0.06, "셀프 어텐션은 intra-attention 이라고도 부른다고 적은 문단이에요."),
           (0.17, 0.70, 0.66, 0.04, "메모리 네트워크 이야기. 순환 어텐션을 쓴 선행 연구예요."),
           (0.17, 0.811, 0.32, 0.026, "3 Model Architecture 제목이에요."),
           (0.17, 0.848, 0.66, 0.075, "인코더가 x 를 z 로, 디코더가 z 에서 y 를 하나씩 만든다는 정의예요.")),
      formula("RNN 의 은닉 상태 사슬 (논문이 말로 적은 것을 식으로)",
              r"h_t = f(h_{t-1},\, x_t)",
              [(r"h_t", f"t 번째 자리의 {HS}"),
               (r"h_{t-1}", "바로 앞 자리의 은닉 상태"),
               (r"x_t", "t 번째 자리의 입력"),
               (r"f", "같은 가중치를 매 자리에서 다시 쓰는 함수")],
              "오른쪽에 h_(t-1) 이 있어서 앞을 끝내야 뒤를 계산해요. 논문이 말한 족쇄가 이것이에요."),
      formula("3장 첫 문단의 인코더 디코더 정의",
              r"(x_1,\dots,x_n) \xrightarrow{\ \text{enc}\ } (z_1,\dots,z_n) \xrightarrow{\ \text{dec}\ } (y_1,\dots,y_m)",
              [(r"(x_1,\dots,x_n)", f"입력 {TOK} n 개"),
               (r"(z_1,\dots,z_n)", f"{ENC} 가 만든 연속 표현 n 개, 개수가 같아요"),
               (r"(y_1,\dots,y_m)", f"{DEC} 가 만든 출력 토큰 m 개, 개수가 달라도 돼요"),
               (r"n, m", "입력 길이와 출력 길이. 번역이니 서로 달라요")],
              f"{DEC} 는 한 번에 하나씩 만들고, 만든 것을 다시 입력으로 넣어요. 이것이 {AR} 예요."),
      bg("기초 다지기 9단원 신경망이 뭔지",
         "신경망 한 층은 입력 벡터에 가중치를 곱하고 편향 항을 더한 뒤 활성화 함수를 지나요.",
         f"{RNN} 은 그 한 층을 자리마다 다시 쓰면서 {HS} 를 넘겨 줘요.",
         "같은 가중치를 다시 쓰니 문장이 길어져도 파라미터가 늘지 않아요. 대신 순서를 지켜야 해요."),
      points("2장이 인정하는 트랜스포머의 대가 (논문의 말)",
             '논문: "at the cost of reduced effective resolution due to averaging attention-weighted positions"',
             "여러 자리를 가중 평균으로 뭉개니 해상도가 떨어진다는 뜻이에요",
             f"논문은 이 손해를 {MHA} 로 막는다고 적었어요",
             "곧 멀티 헤드는 성능 장식이 아니라 잃은 해상도를 되찾는 부품이에요"),
      prof("교수님: 패러럴이 핵심이에요.",
           "교수님: 항상 병렬적으로 처리하고자 하는 파이프라인을 머릿속에 그려 달라.",
           "교수님: RNN 은 아예 빼 버리고 어텐션만 남기면 된다는 게 이 논문이에요.")],
     [check("논문 2장이 셀프 어텐션의 다른 이름이라고 적은 말은?",
            ["intra-attention", "cross-attention", "soft attention", "global attention"], 0,
            f"Self-attention, sometimes called intra-attention 이라고 적었어요. {SA} 와 같은 말이에요."),
      english("시험 답안 문장",
              "순환 신경망은 은닉 상태를 앞에서 뒤로 차례로 만들어야 해서 한 문장 안에서 병렬화가 불가능하고, 트랜스포머는 이 제약을 없앴다.",
              "왜 순환을 버렸냐고 물으면 병렬화 한 단어면 돼요.",
              "h_t 가 h_(t-1) 을 필요로 한다, 한 줄만 기억해요."),
      warn("헷갈리기 쉬운 점",
           f"{ATT} 자체는 2017년에 처음 나온 게 아니에요. 새로운 것은 순환 없이 어텐션만 쓴 것이에요.",
           f"2장은 {CNN} 계열(ByteNet, ConvS2S)이 이미 {PAR} 를 시도했다고 인정해요.",
           f"{MPL} 이라는 정식 이름은 2장에 아직 안 나와요. Table 1 과 4장(NP p.6)에서 나와요."),
      exam("예상 문제",
           "트랜스포머 이전의 순환 기반 모델이 가진 근본적 한계를 설명하시오.",
           "왜 순환을 버려야 했는지 쓰는 문제예요.",
           [f"1. {HS} h_t 가 h_(t-1) 에 의존해요",
            "2. 그래서 한 예제 안에서 자리들을 동시에 계산할 수 없어요",
            "3. 문장이 길어질수록 이 문제가 심해지고, 메모리 때문에 배치로 덮기도 어려워요",
            "4. 논문은 이것을 the fundamental constraint of sequential computation 이라고 불러요"],
           "은닉 상태의 순차 의존 때문에 병렬화가 막히는 것이 근본 한계예요.")])

# ---------------------------------------------------------------- p.3
page(3, "Figure 1 전체 구조와 3.1 인코더 디코더 스택",
     ["Transformer", "Encoder", "Decoder", "Sub-layer", "Multi-Head Attention (MHA)",
      "Self-Attention", "Cross-Attention", "Position-wise Feed-Forward Network (FFN)",
      "Residual Connection", "Layer Normalization (LayerNorm)", "Causal Masking", "Autoregressive",
      "Embedding", "Positional Encoding", "Softmax", "Attention", "Query", "Key", "Value",
      "Weighted Sum", "Compatibility Function", "Parameter", "Token", "Large Language Model (LLM)"],
     [say("이 쪽에 논문에서 가장 유명한 그림 Figure 1 이 있어요.",
          f"왼쪽이 {ENC}, 오른쪽이 {DEC} 예요. 둘 다 같은 층을 6번 쌓았어요.",
          f"3.1 은 그 층 안에 무엇이 들어 있는지 말로 설명해요. 핵심 낱말은 {SUB} 이에요.",
          f"이 그림을 크게 키우면 요즘 {LLM} 이 돼요."),
      analogy("2층으로 나뉜 공장",
              "왼쪽 공장은 재료를 다듬어 놓고, 오른쪽 공장은 그걸 받아서 제품을 하나씩 내보내요. 두 공장 모두 같은 작업대를 여섯 번 반복해요.",
              ("재료를 다듬는 공장", ENC),
              ("제품을 내보내는 공장", DEC),
              ("같은 작업대 여섯 번", "N = 6 층"),
              ("작업대 안의 작업 하나", SUB)),
      figure("인코더 층과 디코더 층 속 들여다보기", FIG_STACK, "디코더 층에만 하위층이 하나 더 있어요.", 4)],
     [points("3.1 의 영어와 우리말 뜻",
             '"**a stack of N = 6 identical layers**" = 똑같이 생긴 층 6개를 쌓은 더미',
             '"**Each layer has two sub-layers**" = 층 하나에 하위층이 둘이다 (인코더 이야기)',
             '"**the decoder inserts a third sub-layer**" = 디코더는 하위층을 하나 더 끼워 넣는다',
             '"**LayerNorm(x + Sublayer(x))**" = 입력 x 를 결과에 더한 뒤 층 정규화를 한다',
             '"**prevent positions from attending to subsequent positions**" = 뒤 자리를 보지 못하게 막는다',
             '"**output embeddings are offset by one position**" = 출력 임베딩을 한 칸 밀어 넣는다'),
      points("3.2 첫 문단의 어텐션 정의",
             '"**mapping a query and a set of key-value pairs to an output**" = 쿼리와 키-밸류 쌍들을 출력으로 보내기',
             '"**the query, keys, values, and output are all vectors**" = 넷 다 벡터다',
             f'"**computed as a weighted sum of the values**" = 밸류의 {WSUM} 으로 계산한다',
             f'"**a compatibility function of the query with the corresponding key**" = 쿼리와 짝 키의 {CF} 가 가중치를 만든다'),
      compare("인코더 층과 디코더 층의 차이",
              ["", ENC, DEC],
              ["층 수", "N = 6", "N = 6"],
              [SUB, "2개", "3개"],
              ["첫 하위층", f"{MHA} ({SA})", f"마스크드 {MHA}"],
              ["가운데 하위층", "없어요", f"{CA} (인코더 출력을 봄)"],
              ["마지막 하위층", FFN, FFN],
              ["미래를 보나", "앞뒤 다 봐요", f"{CM} 으로 막아요"]),
      steps("Figure 1 을 아래에서 위로 읽어요 (왼쪽 인코더)",
            [f"1. 맨 아래 Inputs 가 들어와서 Input Embedding 으로 {EMB} 이 돼요",
             f"2. 동그라미 더하기 표시에서 {PE} 을 더해요. 여기서 딱 한 번만 더해요",
             f"3. Multi-Head Attention 하위층을 지나요. 이게 {SA} 이에요",
             f"4. Add & Norm 에서 {RES} 로 입력을 더하고 {LN} 를 해요",
             f"5. Feed Forward 하위층, 곧 {FFN} 을 지나요",
             "6. 다시 Add & Norm. 여기까지가 한 층이고, 이것을 Nx 만큼 반복해요"],
            f"임베딩 더하기 위치, 어텐션, FFN. 한 층은 이 뼈대예요."),
      check("디코더 층에만 있고 인코더 층에는 없는 하위층은?",
            [CA, FFN, SA, LN], 0,
            f"논문은 이것을 encoder-decoder attention 이라고 불러요. 강의에서 배운 {CA} 와 같은 것이에요.")],
     [look("Figure 1 을 짚어 봐요",
           (0.355, 0.24, 0.145, 0.15, "왼쪽 회색 덩어리가 인코더 한 층이에요. 상자가 둘이라 하위층이 둘이에요."),
           (0.50, 0.175, 0.14, 0.215, "오른쪽 덩어리가 디코더 한 층이에요. 상자가 셋이라 하위층이 셋이에요."),
           (0.52, 0.322, 0.09, 0.043, "Masked Multi-Head Attention. 미래를 못 보게 막은 셀프 어텐션이에요."),
           (0.50, 0.252, 0.13, 0.036, "가운데 Multi-Head Attention. 화살표가 왼쪽 인코더에서 와요. 크로스 어텐션이에요."),
           (0.32, 0.39, 0.30, 0.062, "Positional Encoding 이 Input Embedding 에 더해지는 자리예요."),
           (0.643, 0.277, 0.035, 0.02, "Nx 표시. 논문은 N = 6 이라고 값을 못박았어요.")),
      look("3.1 과 3.2 본문을 짚어 읽어요",
           (0.34, 0.512, 0.31, 0.02, "Figure 1 캡션: The Transformer - model architecture."),
           (0.17, 0.612, 0.30, 0.025, "3.1 Encoder and Decoder Stacks 제목이에요."),
           (0.17, 0.638, 0.66, 0.10, "Encoder 문단. N = 6, 하위층 둘, LayerNorm(x + Sublayer(x)), d_model = 512."),
           (0.17, 0.748, 0.66, 0.10, "Decoder 문단. 하위층 셋, 마스킹, 출력 임베딩을 한 칸 밀기."),
           (0.17, 0.863, 0.20, 0.025, "3.2 Attention 제목이에요."),
           (0.17, 0.888, 0.66, 0.035, "어텐션을 쿼리와 키-밸류 쌍을 출력으로 보내는 함수라고 정의해요.")),
      formula("하위층 하나를 감싸는 식",
              r"\mathrm{LayerNorm}\bigl(x + \mathrm{Sublayer}(x)\bigr)",
              [(r"x", "하위층에 들어온 입력 벡터"),
               (r"\mathrm{Sublayer}(x)", f"그 {SUB} 이 실제로 한 계산"),
               (r"x + \mathrm{Sublayer}(x)", f"{RES}. 입력을 결과에 그대로 더해요"),
               (r"\mathrm{LayerNorm}", f"{LN}. 더한 값을 평균 0, 분산 1 로 맞춰요")],
              f"더한 뒤에 정규화하는 이 순서를 Post-LN 이라고 불러요. 논문은 이 순서만 썼어요."),
      steps("하위층이 모두 몇 개인지 직접 세어 봐요",
            [f"1. {ENC} 는 층마다 {SUB} 이 2개, 층이 6개예요",
             "2. 6 x 2 = 12 개예요",
             f"3. {DEC} 는 층마다 {SUB} 이 3개, 층이 6개예요",
             "4. 6 x 3 = 18 개예요",
             "5. 다 더하면 12 + 18 = 30 개예요",
             f"6. {SUB} 마다 {RES} 와 {LN} 가 하나씩 붙으니 LayerNorm 도 30개예요"],
            f"{SUB} 30개, {LN} 30개예요. 논문이 이 개수를 직접 적지는 않았고 우리가 센 것이에요.",
            "N = 6, 인코더 하위층 2, 디코더 하위층 3"),
      compare("논문과 4주차 강의 슬라이드가 다른 점",
              ["무엇", "논문 (NP p.3)", "4주차 슬라이드 (N4)"],
              ["층 수 N", "N = 6 이라고 못박아요", "p.52 는 Stack it N times 라고만 해요"],
              [f"{LN} 자리", "Post-LN, 곧 더한 뒤 정규화", "p.51 은 Pre-LN 과 비교하고 요즘은 Pre-LN 이라고 해요"],
              ["어텐션 설명 순서", f"처음부터 {QRY}, {KEY}, {VAL} 로 설명", "p.19-23 은 디코더 상태 s 와 인코더 상태 h 로 먼저 설명"],
              [f"{CA} 이름", "encoder-decoder attention", f"p.53 은 {CA} 이라고 불러요"]),
      bg("기초 다지기 3단원 행렬과 행렬 곱, shape",
         f"{EMB} 하나가 512칸짜리 벡터예요. 문장에 {TOK} 이 n 개면 입력은 (n, 512) 모양의 표예요.",
         f"모든 {SUB} 의 출력도 (n, 512) 로 같아요. 그래야 {RES} 로 더할 수 있어요.",
         "논문이 to facilitate these residual connections 라고 적은 이유가 이것이에요."),
      prof("교수님: 오늘 수업이 끝날 때면 트랜스포머를 이해하고, 라지 랭귀지 모델이 어떻게 되는지 알아볼 수 있는 게 목표예요.",
           "교수님: 트랜스포머를 좀 크게 쌓으면 그게 LLM 이다 이렇게 보셔도 됩니다.",
           "교수님: 여기까지가 트랜스포머의 기본 뼈대예요.")],
     [check("논문이 쓴 식 LayerNorm(x + Sublayer(x)) 이 뜻하는 순서는?",
            ["하위층 계산 후 입력을 더하고 마지막에 정규화", "정규화 후 하위층 계산",
             "정규화만 하고 더하지 않음", "하위층 계산만 하고 정규화 없음"], 0,
            f"{RES} 로 더한 다음 {LN} 를 해요. 이것을 Post-LN 이라고 불러요."),
      check("모든 하위층과 임베딩 층의 출력 차원을 512 로 맞춘 이유는?",
            [f"{RES} 로 더하려면 모양이 같아야 해서", "소프트맥스를 쓰려고",
             "어휘 크기가 512 라서", "GPU 가 512만 지원해서"], 0,
            "논문은 to facilitate these residual connections 라고 적었어요. 더하려면 shape 이 같아야 해요."),
      english("시험 답안 문장",
              "인코더 층은 멀티 헤드 셀프 어텐션과 위치별 피드포워드 두 하위층으로, 디코더 층은 여기에 인코더 출력을 보는 크로스 어텐션을 더한 세 하위층으로 이루어진다.",
              "2개와 3개, 그리고 더해진 하나가 무엇인지가 답이에요.",
              "인코더 2, 디코더 3, 차이는 크로스 어텐션. 숫자로 외워요."),
      warn("헷갈리기 쉬운 점",
           f"{PE} 은 층마다 더하는 게 아니라 스택 맨 아래에서 딱 한 번만 더해요.",
           f"{CM} 은 {DEC} 의 첫 하위층에만 있어요. {CA} 에는 없어요.",
           "논문에는 Pre-LN 이라는 말이 없어요. 강의 p.51 의 Pre-LN 은 나중 이야기예요.",
           f"{LLM} 이라는 말도 논문에는 없어요. 교수님이 이해를 돕느라 덧붙인 말이에요."),
      exam("예상 문제",
           "트랜스포머 인코더 층과 디코더 층의 하위층 구성을 각각 쓰고, 하위층마다 공통으로 붙는 두 장치를 쓰시오.",
           "층 안의 부품을 나열하고, 모든 하위층에 붙는 두 가지를 쓰는 문제예요.",
           [f"1. {ENC} 층: 멀티 헤드 {SA} 다음에 FFN (하위층 2개)",
            f"2. {DEC} 층: 마스크드 {SA}, 그다음 {CA}, 그다음 FFN",
            "3. 그래서 디코더 층의 하위층은 3개예요",
            f"4. 모든 {SUB} 에 {RES} 와 {LN} 가 붙어요",
            "5. 식으로 쓰면 LayerNorm(x + Sublayer(x)) 예요"],
           "인코더 2개, 디코더 3개, 공통 장치는 잔차 연결과 층 정규화예요.")])

# ---------------------------------------------------------------- p.4
page(4, "Figure 2 와 3.2.1 스케일드 닷프로덕트 어텐션 (식 1)",
     ["Scaled Dot-Product Attention", "Attention", "Query", "Key", "Value", "Dot Product",
      "Softmax", "Attention Score", "Attention Weight", "Weighted Sum", "Additive Attention",
      "Dot-Product Attention", "Compatibility Function", "Gradient", "Multi-Head Attention (MHA)",
      "Head", "Causal Masking", "Parameter", "Transformer", "Self-Attention"],
     [say(f"이 쪽에 논문의 가장 중요한 식 (1) 이 있어요. 이름이 {SDP} 이에요.",
          "Figure 2 는 그 식을 그림으로 그린 거예요. 왼쪽이 식 (1), 오른쪽이 멀티 헤드예요.",
          f"이름을 뜯어 보면 답이 나와요. 닷프로덕트는 {DP}, 스케일드는 루트 d_k 로 나눈다는 뜻이에요.",
          f"4주차 강의 p.36 에서 배운 그 한 줄이 여기 원문으로 있어요."),
      analogy("점수를 반으로 접어서 보기",
              "시험 점수가 1600점 만점이면 차이가 너무 벌어져 보여요. 100점 만점으로 환산하면 차이가 알맞게 보여요. 루트 d_k 로 나누는 게 이 환산이에요.",
              ("1600점 만점 원점수", f"나누기 전 {ASC}"),
              ("100점 만점 환산", "루트 d_k 로 나눈 점수"),
              ("1등만 다 가져가는 상황", f"포화된 {SMX}"),
              ("등수가 골고루 보이는 상황", f"알맞게 퍼진 {AW}")),
      points("이 쪽에서 챙길 것",
             f"식 (1) 한 줄: Attention(Q, K, V) = softmax(QK^T / 루트 d_k) V",
             f"왜 나누는지: 안 나누면 {SMX} 가 포화되고 {GRAD} 가 사라져요",
             f"{ADD} 과 {DPA} 을 비교한 문단",
             "각주 4: 내적의 분산이 d_k 가 된다는 계산")],
     [points("3.2.1 의 영어와 우리말 뜻",
             f'"**Scaled Dot-Product Attention**" = {DP} 점수를 루트 d_k 로 나눈 어텐션',
             '"**queries and keys of dimension d_k, and values of dimension d_v**" = 쿼리와 키는 d_k 칸, 밸류는 d_v 칸',
             '"**divide each by root d_k, and apply a softmax**" = 각각을 루트 d_k 로 나누고 소프트맥스를 쓴다',
             '"**packed together into a matrix Q**" = 쿼리들을 한 행렬로 묶어 한꺼번에 계산한다',
             '"**the scaling factor of 1 / root d_k**" = 1 을 루트 d_k 로 나눈 배율',
             '"**extremely small gradients**" = 기울기가 아주 작아진다, 곧 학습이 멈춘다'),
      compare("두 가지 옛 어텐션 방식 비교 (논문 3.2.1)",
              ["", ADD, DPA],
              ["점수 만드는 법", "은닉층 1개짜리 작은 신경망", f"{QRY} 와 {KEY} 를 그냥 {DP}"],
              ["이론상 복잡도", "비슷해요", "비슷해요"],
              ["실제 속도", "느려요", "훨씬 빨라요"],
              ["실제 메모리", "많이 써요", "적게 써요"],
              ["이유", "신경망을 한 번 더 돌려야 해요", "잘 최적화된 행렬 곱 코드를 쓸 수 있어요"],
              ["d_k 가 클 때", "더 잘 나왔어요", f"나누지 않으면 나빠져요"]),
      steps("식 (1) 을 왼쪽부터 순서대로 읽어요",
            [f"1. Q 와 K^T 를 곱해요. 모든 {QRY} 와 모든 {KEY} 의 {DP} 이 한 번에 나와요",
             "2. 그 결과를 루트 d_k 로 나눠요. 이게 Scale 이에요",
             f"3. (디코더면) 미래 칸을 마이너스 무한으로 바꿔요. 이게 {CM} 이고 Figure 2 의 Mask (opt.) 예요",
             f"4. {SMX} 를 줄마다 써서 합이 1 인 {AW} 를 만들어요",
             f"5. 그 가중치로 V 를 곱해요. 이게 {WSUM} 이에요"],
            f"곱하고, 나누고, (가리고), 소프트맥스하고, 다시 곱해요. 다섯 걸음이에요."),
      check("Scaled Dot-Product Attention 에서 scaled 가 가리키는 것은?",
            ["루트 d_k 로 나누는 것", "소프트맥스를 쓰는 것",
             "밸류를 곱하는 것", "헤드를 나누는 것"], 0,
            f"논문은 the scaling factor of 1 / root d_k 라고 적었어요. 이 나누기 때문에 이름이 scaled 예요."),
      figure("식 (1) 의 흐름", FIG_SDP, "곱하기, 나누기, 소프트맥스, 다시 곱하기예요.", 4)],
     [look("Figure 2 를 짚어 봐요",
           (0.24, 0.085, 0.20, 0.02, "왼쪽 그림 제목 Scaled Dot-Product Attention 이에요."),
           (0.28, 0.115, 0.12, 0.17, "왼쪽 탑. 아래부터 MatMul, Scale, Mask (opt.), SoftMax, MatMul 순서예요."),
           (0.28, 0.263, 0.11, 0.022, "맨 아래 입력 이름표 Q, K, V 예요. V 만 옆으로 돌아 위 MatMul 로 가요."),
           (0.59, 0.085, 0.15, 0.02, "오른쪽 그림 제목 Multi-Head Attention 이에요."),
           (0.56, 0.113, 0.21, 0.15, "오른쪽 탑. Linear 셋 → Scaled Dot-Product Attention → Concat → Linear."),
           (0.74, 0.193, 0.035, 0.022, "작은 h 표시. 같은 어텐션을 h 개 겹쳐 놓았다는 뜻이에요.")),
      look("3.2.1 본문과 식 (1) 을 짚어 읽어요",
           (0.17, 0.345, 0.66, 0.03, "Figure 2 캡션. 오른쪽은 여러 어텐션 층이 나란히 돈다고 적었어요."),
           (0.17, 0.442, 0.32, 0.022, "3.2.1 Scaled Dot-Product Attention 제목이에요."),
           (0.17, 0.468, 0.66, 0.06, "입력은 d_k 짜리 쿼리와 키, d_v 짜리 밸류라고 적은 문단이에요."),
           (0.35, 0.585, 0.30, 0.032, "식 (1) 이에요. 논문에서 가장 자주 인용되는 한 줄이에요."),
           (0.17, 0.625, 0.66, 0.08, "가산 어텐션과 닷프로덕트 어텐션을 비교하는 문단이에요."),
           (0.17, 0.717, 0.66, 0.068, "We suspect 로 시작하는 문단. 논문이 추측이라고 직접 밝힌 대목이에요.")),
      formula("식 (1) 스케일드 닷프로덕트 어텐션",
              r"\mathrm{Attention}(Q,K,V) = \mathrm{softmax}\!\left(\frac{QK^{T}}{\sqrt{d_k}}\right)V",
              [(r"Q", f"{QRY} 들을 줄줄이 쌓은 행렬"),
               (r"K^{T}", f"{KEY} 행렬을 눕힌 것(전치)"),
               (r"QK^{T}", f"모든 쿼리와 모든 키의 {DP} 을 한 번에"),
               (r"\sqrt{d_k}", "키 한 개의 칸 수 d_k 의 제곱근. 논문은 64 를 썼어요"),
               (r"\mathrm{softmax}", f"줄마다 합이 1 이 되게 만드는 {SMX}"),
               (r"V", f"{VAL} 행렬. 실제로 섞이는 내용")],
              f"이 한 줄이 논문의 식 (1) 이에요. 시험에 나오면 이대로 쓰면 돼요."),
      steps("루트 d_k 로 나누는 손계산",
            ["1. 논문의 base 모델은 헤드 하나가 d_k = 64 예요",
             "2. 루트 64 = 8 이에요",
             f"3. {DP} 원점수가 16, 8, 0 이라고 해 봐요",
             "4. 8로 나누면 2, 1, 0 이 돼요",
             "5. exp(2) = 7.389, exp(1) = 2.718, exp(0) = 1, 합은 11.107 이에요",
             "6. 각각 나누면 0.6652, 0.2447, 0.0900 이고 다 더하면 1 이에요"],
            f"{AW} 는 0.6652, 0.2447, 0.0900 이에요. 1등이 크지만 2, 3등도 살아 있어요.",
            "d_k = 64, 원점수 16, 8, 0"),
      steps("안 나누면 어떻게 되는지 비교",
            ["1. 나누지 않은 16, 8, 0 을 그대로 소프트맥스에 넣어 봐요",
             "2. 결과는 0.999665, 0.000335, 0.000000 이에요",
             "3. 거의 1등이 다 가져가는 원-핫 모양이에요",
             f"4. 이렇게 포화되면 {GRAD} 가 거의 0 이라 학습이 안 돼요",
             f"5. {VAL} 가 (1, 0), (0, 2), (2, 2) 라면 나눈 쪽 {WSUM} 은 (0.8452, 0.6694) 예요",
             "6. 안 나눈 쪽은 거의 (1, 0) 이 되어 버려요. 2등과 3등이 사라져요"],
            "나누기 한 번이 분포를 살려요. 논문이 이 나누기 하나로 이름까지 붙인 이유예요.",
            "원점수 16, 8, 0 / V = (1,0), (0,2), (2,2)"),
      points("각주 4 가 말하는 것 (논문 4쪽 아래)",
             '논문: "assume that the components of q and k are independent random variables with mean 0 and variance 1"',
             "그러면 두 벡터의 내적은 평균 0, 분산 d_k 가 돼요",
             "분산이 d_k 면 표준편차는 루트 d_k 예요. d_k = 64 면 8, d_k = 512 면 약 22.63 이에요",
             "루트 d_k 로 나누면 표준편차가 다시 1 로 돌아와요. 그래서 이 값으로 나눠요"),
      compare("논문과 4주차 강의 슬라이드가 다른 점",
              ["무엇", "논문 (NP p.4)", "4주차 슬라이드 (N4)"],
              ["d_k 예시", "d_k = 64, 곧 헤드 하나의 차원", "p.38 은 d_k = 512 로 예를 들어요"],
              ["512 의 정체", "512 는 d_model 이에요", "p.38 은 그 512 를 d_k 라고 불러요"],
              ["어텐션 단계 수", f"{CF} → 가중치 → {WSUM} 세 단계", "p.21-24 는 점수, 소프트맥스, 가중합, 예측 네 단계"],
              ["부르는 이름", f"{CF} 이라고 부름", f"그냥 {ASC} 라고 부름"]),
      bg("기초 다지기 2단원 내적과 코사인 유사도",
         f"{DP} 은 같은 자리끼리 곱해서 모두 더하는 계산이에요. (1,2,3) 과 (4,5,6) 이면 4 + 10 + 18 = 32 예요.",
         "칸 수가 많아질수록 더하는 항이 많아져서 값이 저절로 커져요. 그래서 나눠 줘야 해요.",
         "기초 다지기 6단원 소프트맥스도 같이 보면 왜 포화가 문제인지 보여요."),
      prof("교수님: 스코어 계산하고, 소프트맥스로 노멀라이즈하고, 웨이티드 썸으로 컨텍스트 벡터를 만들고, 예측해요.",
           "교수님: 이 네 단계가 어텐션에 가장 중요한 거다.",
           "교수님: 이 쿼리, 키, 밸류 3개의 컨셉을 이해해야 뒤에 트랜스포머를 이해할 수 있어요.")],
     [check("논문이 루트 d_k 로 나누는 이유로 든 것은?",
            [f"내적이 커지면 소프트맥스가 포화되어 {GRAD} 가 아주 작아져서",
             "밸류의 크기를 맞추려고", "헤드 수를 맞추려고", "메모리를 아끼려고"], 0,
            "pushing the softmax function into regions where it has extremely small gradients 가 논문의 문장이에요."),
      check("d_k = 64 일 때 나누는 값은?",
            ["8", "64", "4096", "22.63"], 0,
            "루트 64 = 8 이에요. 강의 p.38 의 512 는 d_model 이라 헤드 하나의 d_k 와 달라요."),
      english("시험 답안 문장",
              "스케일드 닷프로덕트 어텐션은 쿼리와 키의 내적을 루트 d_k 로 나눈 뒤 소프트맥스를 취해 가중치를 얻고, 그 가중치로 밸류를 가중합한다.",
              "나누기, 소프트맥스, 가중합 세 마디를 순서대로 쓰면 돼요.",
              "식 (1) 을 그대로 적고 그 아래 한 줄로 풀어 쓰면 안전해요."),
      warn("헷갈리기 쉬운 점",
           f"논문은 We suspect 라고 적었어요. 왜 커지는지는 단정이 아니라 논문의 추측이에요.",
           "d_k 는 헤드 하나의 차원 64 예요. d_model 512 를 넣어 계산하면 틀려요.",
           f"{SMX} 는 줄 단위로 계산해요. 행렬 전체를 한꺼번에 1 로 만드는 게 아니에요.",
           "Figure 2 의 Mask (opt.) 는 선택 사항 표시예요. 인코더에서는 쓰지 않아요."),
      exam("예상 문제",
           "Attention(Q, K, V) 식을 쓰고, 루트 d_k 로 나누는 이유를 설명하시오.",
           "식 하나 쓰고 나누는 이유를 대는 문제예요.",
           ["1. 식 (1) 을 그대로 써요: softmax(QK^T / 루트 d_k) V",
            "2. d_k 가 크면 내적의 분산이 d_k 가 되어 점수가 크게 벌어져요 (각주 4)",
            f"3. 점수가 크면 {SMX} 가 거의 원-핫이 되고 {GRAD} 가 사라져요",
            "4. 루트 d_k 로 나누면 분산이 1 로 돌아와 분포가 알맞게 퍼져요",
            "5. 예: 16, 8, 0 을 8로 나누면 2, 1, 0 이고 소프트맥스는 0.6652, 0.2447, 0.0900 이에요"],
           "분산 d_k 를 되돌려 소프트맥스 포화와 기울기 소실을 막기 위해서예요.")])

data = {"deck": "NP", "from": 1, "to": 4,
        "glossary": [{"ko": k, "en": e, "say": s, "more": m} for k, e, s, m in GLOSSARY],
        "slides": S}

raw = json.dumps(data, ensure_ascii=False, indent=1)
for ch in ("—", "–", "·", "・"):
    assert ch not in raw, ch
with open(OUT, "w", encoding="utf-8") as f:
    f.write(raw)
print("saved", OUT, len(S), "pages")
