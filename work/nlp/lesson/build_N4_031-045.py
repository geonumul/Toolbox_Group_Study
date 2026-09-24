# -*- coding: utf-8 -*-
"""4강(N4) Attention and the Transformer Architecture 회독 레슨 31~45쪽 생성기.
사용: python build_N4_031-045.py   출력: N4_031-045.json
손계산은 아래에서 numpy 로 실제 계산해 assert 로 확인한다."""
import json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "N4_031-045.json")


# ---------------- 손계산 확인 (numpy 로 계산하고 assert) ----------------
def softmax(a):
    a = np.asarray(a, dtype=float)
    e = np.exp(a - a.max(axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


# p.35, p.36 용 작은 셀프 어텐션 예 (토큰 3개, d_k = 4 라서 루트 d_k = 2)
DK = 4
assert math.sqrt(DK) == 2.0
q3 = np.array([1.0, 1.0, 1.0, 1.0])
K = np.array([[1.0, 1.0, 1.0, 1.0],
              [1.0, 1.0, 0.0, 0.0],
              [0.0, 0.0, 0.0, 0.0]])
raw = K @ q3
assert list(raw) == [4.0, 2.0, 0.0]
sc = raw / math.sqrt(DK)
assert list(sc) == [2.0, 1.0, 0.0]
al = softmax(sc)
assert [round(float(v), 4) for v in al] == [0.6652, 0.2447, 0.0900]
assert abs(float(al.sum()) - 1.0) < 1e-12
V = np.array([[2.0, 0.0], [0.0, 2.0], [1.0, 1.0]])
o3 = al @ V
assert [round(float(v), 4) for v in o3] == [1.4205, 0.5795]
# 본문은 소수 넷째 자리로 반올림한 가중치를 그대로 곱해서 보여 준다
al4 = np.array([round(float(v), 4) for v in al])
o3_4 = al4 @ V
assert [round(float(v), 4) for v in o3_4] == [1.4204, 0.5794]
# 스케일을 안 하면 같은 점수라도 훨씬 뾰족해져요
al_raw = softmax(raw)
assert [round(float(v), 4) for v in al_raw] == [0.8668, 0.1173, 0.0159]
assert round(float(al_raw.max()), 4) > round(float(al.max()), 4)

# p.37 행렬 모양 (shape)
n_tok, d_k, d_v = 5, 4, 3
Qm = np.zeros((n_tok, d_k))
Km = np.zeros((n_tok, d_k))
Vm = np.zeros((n_tok, d_v))
assert (Qm @ Km.T).shape == (n_tok, n_tok)
assert (softmax(Qm @ Km.T) @ Vm).shape == (n_tok, d_v)
assert Km.T.shape == (d_k, n_tok)

# p.38 차원이 커지면 점수가 퍼져요 (표준편차 = 루트 d_k)
sd = {d: round(math.sqrt(d), 2) for d in (8, 64, 512)}
assert sd == {8: 2.83, 64: 8.0, 512: 22.63}
big = np.array([20.0, 0.0, 1.0])
assert round(float(softmax(big).max()), 6) == 1.0
assert round(float(softmax(big / math.sqrt(512)).max()), 4) == 0.5420

# p.39 순열 등변성: 순서를 바꿔도 결과가 그대로 따라 바뀌어요
P = np.array([[0.0, 1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
Xs = np.array([[1.0, 0.0, 0.0, 1.0], [0.0, 1.0, 1.0, 0.0], [1.0, 1.0, 0.0, 0.0]])


def selfattn(X):
    S = (X @ X.T) / math.sqrt(X.shape[1])
    return softmax(S) @ X


assert np.allclose(selfattn(P @ Xs), P @ selfattn(Xs))

# p.40 사인 코사인 위치 인코딩 (d = 4)
def pe_row(pos, d=4):
    out = []
    for i in range(d // 2):
        ang = pos / (10000 ** (2 * i / d))
        out += [round(math.sin(ang), 4), round(math.cos(ang), 4)]
    return out


assert pe_row(0) == [0.0, 1.0, 0.0, 1.0]
assert pe_row(1) == [0.8415, 0.5403, 0.01, 1.0]
assert pe_row(2) == [0.9093, -0.4161, 0.02, 0.9998]
assert pe_row(3) == [0.1411, -0.99, 0.03, 0.9996]
# 같은 단어라도 자리가 다르면 더해진 값이 달라져요
w_dog = np.array([0.5, 0.5, 0.5, 0.5])
assert not np.allclose(w_dog + np.array(pe_row(0)), w_dog + np.array(pe_row(2)))

# p.42 FFN 파라미터 수 (d = 512, d_ff = 4d)
d_model = 512
d_ff = 4 * d_model
assert d_ff == 2048
w1 = d_model * d_ff
w2 = d_ff * d_model
assert w1 == 1048576 and w2 == 1048576
assert w1 + w2 == 2097152 == 8 * d_model * d_model
assert 4 * d_model * d_model == 1048576
assert (w1 + w2) == 2 * (4 * d_model * d_model)

# p.43 인과 마스킹: 미래 칸을 -무한으로 만들고 소프트맥스
S3 = np.array([[2.0, 1.0, 0.0], [1.0, 2.0, 1.0], [0.0, 1.0, 2.0]])
mask = np.tril(np.ones((3, 3)))
Sm = np.where(mask == 1, S3, -np.inf)
Am = softmax(Sm)
assert [round(float(v), 4) for v in Am[0]] == [1.0, 0.0, 0.0]
assert [round(float(v), 4) for v in Am[1]] == [0.2689, 0.7311, 0.0]
assert [round(float(v), 4) for v in Am[2]] == [0.0900, 0.2447, 0.6652]
assert all(abs(float(r.sum()) - 1.0) < 1e-12 for r in Am)
assert round(float(math.exp(-50)), 12) == 0.0

# p.32 경로 길이: chef 에서 was 까지
assert 6 > 1

# p.35 슬라이드에 찍힌 어텐션 가중치
w35 = [0.05, 0.10, 0.08, 0.62, 0.15]
assert round(sum(w35), 4) == 1.0 and max(w35) == 0.62 and w35.index(0.62) == 3

# p.44 미리 보기: 멀티 헤드의 d/h
assert 512 // 8 == 64

# ---------------- 용어 표기 ----------------
RNN = "**RNN(순환 신경망)**"
HS = "**은닉 상태(Hidden State)**"
VG = "**기울기 소실(Vanishing Gradient)**"
ENC = "**인코더(Encoder)**"
DEC = "**디코더(Decoder)**"
IB = "**정보 병목(Information Bottleneck)**"
ATT = "**어텐션(Attention)**"
SA = "**셀프 어텐션(Self-Attention)**"
CA = "**크로스 어텐션(Cross-Attention)**"
TRF = "**트랜스포머(Transformer)**"
CTX = "**문맥 벡터(Context Vector)**"
ASC = "**어텐션 점수(Attention Score)**"
AW = "**어텐션 가중치(Attention Weight)**"
WSUM = "**가중합(Weighted Sum)**"
SMX = "**소프트맥스(Softmax)**"
DP = "**내적(Dot Product)**"
QRY = "**쿼리(Query)**"
KEY = "**키(Key)**"
VAL = "**밸류(Value)**"
SDP = "**스케일드 닷프로덕트 어텐션(Scaled Dot-Product Attention)**"
PEQ = "**순열 등변성(Permutation Equivariance)**"
PE = "**위치 인코딩(Positional Encoding)**"
SPE = "**사인 코사인 위치 인코딩(Sinusoidal Positional Encoding)**"
ROPE = "**로프(RoPE)**"
FFN = "**위치별 피드포워드 신경망(Position-wise Feed-Forward Network (FFN))**"
CM = "**인과 마스킹(Causal Masking)**"
AR = "**자기회귀(Autoregressive)**"
PAR = "**병렬화(Parallelization)**"
MHA = "**멀티 헤드 어텐션(Multi-Head Attention (MHA))**"
RES = "**잔차 연결(Residual Connection)**"
LN = "**층 정규화(Layer Normalization (LayerNorm))**"
NL = "**비선형성(Nonlinearity)**"
RELU = "**렐루(ReLU)**"
MLP = "**MLP(다층 퍼셉트론)**"
EMB = "**임베딩(Embedding)**"
TOK = "**토큰(Token)**"
PARAM = "**파라미터(Parameter)**"
LM = "**언어 모델(Language Model (LM))**"
NTP = "**다음 토큰 예측(Next Token Prediction)**"
GRAD = "**기울기(Gradient)**"
BERT = "**버트(BERT)**"
GPT = "**지피티(GPT)**"
LLM = "**대규모 언어 모델(Large Language Model (LLM))**"
MT = "**기계 번역(Machine Translation (MT))**"

WHEN2 = "4주차 월요일 2교시"

GLOSSARY = [
    ("셀프 어텐션", "Self-Attention", "한 문장이 자기 자신을 바라보는 어텐션",
     "쿼리, 키, 밸류가 모두 같은 시퀀스에서 나와요. 모든 토큰이 모든 토큰에게 질문해요."),
    ("크로스 어텐션", "Cross-Attention", "쿼리는 한쪽 시퀀스, 키와 밸류는 다른 쪽 시퀀스에서 오는 어텐션",
     "Part 2 에서 배운 2015년 어텐션이 바로 이것이에요. 디코더가 인코더를 봐요."),
    ("어텐션", "Attention", "필요한 곳을 골라 보는 장치. 점수를 매기고 가중 평균을 내요",
     "점수, 소프트맥스, 가중합, 예측의 네 단계는 셀프 어텐션에서도 똑같아요."),
    ("쿼리", "Query", "지금 내가 무엇을 찾고 있는지를 담은 벡터",
     "셀프 어텐션에서는 토큰 자신의 입력 벡터에 W^Q 를 곱해서 만들어요."),
    ("키", "Key", "나는 이런 정보를 갖고 있다고 광고하는 검색용 이름표 벡터",
     "사전의 색인 같은 역할이에요. 쿼리와 키를 내적해서 점수를 만들어요."),
    ("밸류", "Value", "내가 선택되면 실제로 건네줄 내용 벡터",
     "가중합에 들어가는 것은 키가 아니라 밸류예요. 키와 밸류가 나뉜 것이 셀프 어텐션의 특징이에요."),
    ("스케일드 닷프로덕트 어텐션", "Scaled Dot-Product Attention", "내적 점수를 루트 d_k 로 나눈 뒤 소프트맥스를 쓰는 어텐션",
     "트랜스포머가 쓰는 방식이에요. 나누기 한 번이 학습을 살려요."),
    ("어텐션 점수", "Attention Score", "두 벡터가 얼마나 관련 있는지 나타낸 날것 숫자",
     "셀프 어텐션에서는 쿼리와 키의 내적을 루트 d_k 로 나눈 값이에요."),
    ("어텐션 가중치", "Attention Weight", "점수를 소프트맥스에 넣어 얻은, 합이 1 인 값들",
     "그 자리를 얼마나 볼지 정해요. 0 이상이고 한 줄을 다 더하면 1 이에요."),
    ("가중합", "Weighted Sum", "값마다 가중치를 곱해서 모두 더한 것",
     "밸류들의 가중합이 그 토큰의 새 표현이 돼요."),
    ("소프트맥스", "Softmax", "점수를 모두 더해 1 이 되는 확률 파이로 나누기",
     "각 점수에 exp 를 씌운 뒤 전체 합으로 나눠요. 점수가 크면 분포가 뾰족해져요."),
    ("내적", "Dot Product", "두 화살표가 얼마나 같은 쪽을 보는지 재는 곱셈",
     "같은 자리끼리 곱해서 모두 더해요. 셀프 어텐션의 점수가 바로 내적이에요."),
    ("문맥 벡터", "Context Vector", "이번에 필요한 만큼만 뽑아 만든 요약 벡터",
     "셀프 어텐션에서는 기호가 c_t 가 아니라 o_i 로 바뀌지만 정체는 같아요."),
    ("순열 등변성", "Permutation Equivariance", "입력 순서를 바꾸면 출력도 똑같이 순서만 바뀌는 성질",
     "셀프 어텐션이 순서를 전혀 모른다는 뜻이에요. 그래서 위치 인코딩이 필요해요."),
    ("위치 인코딩", "Positional Encoding", "몇 번째 자리인지를 알려 주는 벡터를 임베딩에 더해 주기",
     "셀프 어텐션의 배리어 1(순서 없음)을 고치는 부품이에요."),
    ("사인 코사인 위치 인코딩", "Sinusoidal Positional Encoding", "sin 과 cos 파도로 만든, 학습하지 않는 위치 벡터",
     "2017년 원래 논문이 쓴 방식이에요. 학습 파라미터가 0 개예요."),
    ("로프", "RoPE", "쿼리와 키를 위치에 비례한 각도만큼 회전시키는 위치 방식",
     "점수가 두 자리의 상대 거리 i - j 에만 의존하게 돼요. 요즘 LLM 이 거의 다 써요."),
    ("위치별 피드포워드 신경망", "Position-wise Feed-Forward Network (FFN)", "자리마다 똑같이 적용하는 2층짜리 작은 신경망",
     "배리어 2(비선형성 없음)를 고쳐요. 가운데 차원이 보통 4d 라서 파라미터가 많아요."),
    ("인과 마스킹", "Causal Masking", "미래 자리의 점수를 소프트맥스 전에 마이너스 무한으로 바꾸기",
     "배리어 3(미래를 훔쳐봄)을 고쳐요. 가중치가 정확히 0 이 돼요."),
    ("자기회귀", "Autoregressive", "앞에서 만든 토큰을 보고 다음 토큰을 하나씩 만드는 방식",
     "GPT 같은 모델이 이렇게 글을 써요. 그래서 미래를 보면 안 돼요."),
    ("병렬화", "Parallelization", "여러 계산을 한꺼번에 동시에 하기",
     "교수님이 패러럴이 핵심이라고 했어요. 셀프 어텐션은 행렬 곱 한 번으로 끝나요."),
    ("트랜스포머", "Transformer", "어텐션만으로 만든 요즘 언어 모델의 기본 블록",
     "셀프 어텐션에 위치 인코딩, FFN, 마스킹을 더하면 기본 뼈대가 돼요."),
    ("순환 신경망", "Recurrent Neural Network (RNN)", "한 단어씩 읽으며 메모장에 요약을 고쳐 쓰는 신경망",
     "셀프 어텐션은 이것을 아예 빼 버려요. 그래서 병렬 계산이 가능해요."),
    ("은닉 상태", "Hidden State", "지금까지 읽은 내용을 요약해 들고 다니는 숫자 벡터",
     "RNN 은 이것을 한 걸음씩 넘겨요. 셀프 어텐션은 한 번에 만들어요."),
    ("기울기 소실", "Vanishing Gradient", "귓속말 전달 게임처럼 기울기가 점점 희미해져 0 에 가까워지는 문제",
     "셀프 어텐션은 거리를 1 로 줄여서 이 문제를 비켜 가요."),
    ("기울기", "Gradient", "손실이 가장 빨리 커지는 방향과 그 가파름",
     "소프트맥스가 포화되면 기울기가 거의 0 이 돼서 학습이 멈춰요."),
    ("인코더", "Encoder", "입력 문장을 끝까지 읽어 자리마다 표현을 만드는 쪽",
     "인코더는 마스킹을 안 해서 앞뒤를 다 봐요."),
    ("디코더", "Decoder", "답 문장을 한 토큰씩 만들어 내는 쪽",
     "디코더는 인과 마스킹을 써서 미래를 못 보게 막아요."),
    ("정보 병목", "Information Bottleneck", "입력 전체가 고정 크기 벡터 하나를 지나가야 해서 생기는 막힘",
     "Part 1 에서 본 문제예요. 어텐션이 이것을 없앴어요."),
    ("임베딩", "Embedding", "토큰을 숫자 벡터로 바꾼 것. 단어의 지도 좌표",
     "위치 인코딩은 이 임베딩에 더해져요."),
    ("토큰", "Token", "글을 자른 레고 조각 하나",
     "셀프 어텐션에서 토큰 하나가 쿼리, 키, 밸류 세 역할을 동시에 해요."),
    ("파라미터", "Parameter", "학습하면서 바뀌는 숫자. 모델이 기억을 저장하는 자리",
     "W^Q, W^K, W^V 가 파라미터예요. 모든 자리에서 같은 것을 나눠 써요."),
    ("비선형성", "Nonlinearity", "곧은 직선이 아닌 구부러진 변환",
     "이것이 없으면 층을 아무리 쌓아도 결국 한 층과 같아요."),
    ("렐루", "ReLU", "음수는 0 으로 만들고 양수는 그대로 두는 함수",
     "FFN 가운데에 들어가서 비선형성을 만들어요. 3주차에 배웠어요."),
    ("다층 퍼셉트론", "Multi-Layer Perceptron (MLP)", "뉴런 층을 여러 겹 쌓은 가장 기본 신경망",
     "FFN 은 자리마다 똑같이 적용되는 2층짜리 MLP 예요."),
    ("언어 모델", "Language Model (LM)", "다음 토큰을 맞히는 모델",
     "언어 모델은 미래 토큰을 보면 안 돼요. 그래서 마스킹이 필요해요."),
    ("다음 토큰 예측", "Next Token Prediction", "지금까지의 토큰으로 바로 다음 토큰을 맞히기",
     "3주차에 교수님이 이게 거의 모든 걸 결정한다고 했어요."),
    ("멀티 헤드 어텐션", "Multi-Head Attention (MHA)", "전체 차원을 h 조각으로 나눠 여러 관점에서 동시에 어텐션하기",
     "Part 4 에서 배워요. 계산량은 늘지 않아요."),
    ("잔차 연결", "Residual Connection", "층의 입력을 층의 출력에 그대로 더해 주는 지름길",
     "Part 4 에서 배워요. 깊게 쌓아도 학습이 되게 해 줘요."),
    ("층 정규화", "Layer Normalization (LayerNorm)", "한 토큰의 숫자들을 평균 0, 분산 1 로 맞춰 주기",
     "Part 4 에서 배워요. 값이 폭주하지 않게 잡아 줘요."),
    ("버트", "BERT", "앞뒤를 다 보는 인코더 방식 언어 모델",
     "마스킹을 하지 않는 쪽이에요. 위치 벡터를 학습해서 써요."),
    ("지피티", "GPT", "앞만 보고 다음 토큰을 만드는 디코더 방식 언어 모델",
     "인과 마스킹을 쓰는 쪽이에요. 자기회귀로 글을 써요."),
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
    return {"kind": "prof", "when": WHEN2, "lines": list(lines)}


# ---------------- SVG 도우미 ----------------
def _c(cls, b):
    return f"{cls} b{b}" if b else cls


def SVG(*els, h=270):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 {h}">' + "".join(els) + "</svg>"


def TX(x, y, s, cls="t", size=15, anchor="middle", b=0):
    return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" class="{_c(cls, b)}">{s}</text>'


def R(x, y, w, h, cls="n", b=0):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" class="{_c(cls, b)}"/>'


def C(cx, cy, r, cls="n", b=0):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" class="{_c(cls, b)}"/>'


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
FIG_PATH = SVG(
    TX(240, 22, "거리가 n 에서 1 로", "tb", 16),
    *[BOX(14 + i * 76, 44, 68, 28, t, "n", "tl", 1, 12)
      for i, t in enumerate(["The", "chef", "who", "went", "was", "food"])],
    A(124, 90, 124 + 76 * 3, 90, "e", 2),
    TX(240, 112, "RNN: chef 에서 was 까지 리커런트 6 걸음", "t", 13, "middle", 2),
    A(124, 146, 352, 146, "e2", 3),
    TX(240, 168, "셀프 어텐션: chef 와 was 는 1 걸음", "tb", 13, "middle", 3),
    TX(240, 200, "걸음이 줄면 기울기가 덜 희미해져요", "t", 13, "middle", 4),
    TX(240, 224, "그리고 앞을 기다릴 필요가 없어 병렬 계산이 돼요", "tm", 12, "middle", 4),
)

FIG_QKV = SVG(
    TX(240, 22, "토큰 하나가 세 역할을 동시에", "tb", 16),
    BOX(180, 40, 120, 30, "x_i (입력 벡터)", "box", "tb", 1, 13),
    A(200, 76, 120, 106, "e2", 2), A(240, 76, 240, 106, "e2", 2), A(280, 76, 360, 106, "e2", 2),
    BOX(60, 108, 120, 30, "q = W^Q x", "box2", "tb", 2, 13),
    BOX(182, 108, 116, 30, "k = W^K x", "box2", "tb", 2, 13),
    BOX(300, 108, 120, 30, "v = W^V x", "box2", "tb", 2, 13),
    TX(120, 160, "무엇을 찾나", "t", 13, "middle", 3),
    TX(240, 160, "나는 이런 것", "t", 13, "middle", 3),
    TX(360, 160, "뽑히면 줄 내용", "t", 13, "middle", 3),
    TX(240, 196, "W^Q, W^K, W^V 세 행렬은 모든 자리가 함께 써요", "tb", 13, "middle", 4),
    TX(240, 220, "그래서 문장이 길어져도 파라미터가 늘지 않아요", "tm", 12, "middle", 4),
)

FIG_MASK = SVG(
    TX(240, 22, "인과 마스킹: 오른쪽 위를 지워요", "tb", 16),
    *[TX(60, 62 + r * 34, t, "t", 13, "end", 1) for r, t in enumerate(["1번", "2번", "3번"])],
    *[R(72 + c * 60, 46 + r * 34, 54, 26, "n" if c <= r else "n4", 1)
      for r in range(3) for c in range(3)],
    *[TX(99 + c * 60, 64 + r * 34, "볼 수 있음" if c <= r else "차단", "tl", 10, "middle", 2)
      for r in range(3) for c in range(3)],
    TX(240, 172, "미래 칸의 점수를 마이너스 무한으로 바꿔요", "tb", 13, "middle", 3),
    TX(240, 196, "소프트맥스를 지나면 그 칸 가중치가 정확히 0 이에요", "t", 13, "middle", 4),
    TX(240, 220, "인코더는 이 마스크를 안 써서 앞뒤를 다 봐요", "tm", 12, "middle", 4),
)

FIG_BLOCK = SVG(
    TX(240, 20, "최소 블록 쌓기", "tb", 16),
    BOX(110, 190, 260, 30, "입력 임베딩", "box", "tb", 1, 13),
    A(240, 188, 240, 166, "e2", 2),
    BOX(110, 136, 260, 30, "+ 위치 인코딩", "box2", "tb", 2, 13),
    TX(392, 156, "배리어 1", "tm", 11, "start", 2),
    A(240, 134, 240, 112, "e2", 3),
    BOX(110, 82, 260, 30, "마스크드 셀프 어텐션", "box2", "tb", 3, 13),
    TX(392, 102, "배리어 3", "tm", 11, "start", 3),
    A(240, 80, 240, 58, "e2", 4),
    BOX(110, 28, 260, 30, "위치별 FFN", "box2", "tb", 4, 13),
    TX(392, 48, "배리어 2", "tm", 11, "start", 4),
    TX(240, 244, "이 블록을 N 번 쌓으면 거의 트랜스포머예요", "tb", 13, "middle", 4),
)

FIG_MATMUL = SVG(
    TX(240, 22, "한 번의 행렬 곱으로 전부", "tb", 16),
    BOX(16, 50, 68, 54, "Q", "box2", "tb", 1, 14),
    TX(50, 118, "n x d_k", "tm", 11, "middle", 1),
    TX(96, 80, "x", "tb", 14, "middle", 1),
    BOX(108, 50, 68, 54, "K^T", "box2", "tb", 1, 14),
    TX(142, 118, "d_k x n", "tm", 11, "middle", 1),
    A(184, 78, 208, 78, "e2", 2),
    BOX(214, 50, 68, 54, "점수", "box", "tb", 2, 14),
    TX(248, 118, "n x n", "tm", 11, "middle", 2),
    A(290, 78, 314, 78, "e2", 3),
    BOX(320, 50, 68, 54, "A", "box2", "tb", 3, 14),
    TX(354, 118, "n x n, 줄 합 1", "tm", 11, "middle", 3),
    TX(404, 80, "x V", "tb", 14, "middle", 4),
    TX(240, 160, "결과 O 의 모양은 n x d_v 예요", "tb", 13, "middle", 4),
    TX(240, 186, "자리를 도는 for 문이 없어서 GPU 가 아주 잘해요", "t", 13, "middle", 4),
    TX(240, 212, "교수님: 패러럴이 핵심이에요", "tm", 12, "middle", 4),
)

FIG_SCALE = SVG(
    TX(240, 22, "루트 d_k 로 나누는 이유", "tb", 16),
    TX(120, 56, "나누기 전", "tb", 14),
    TX(360, 56, "나눈 뒤", "tb", 14),
    R(60, 70, 24, 80, "n4", 1), R(92, 146, 24, 4, "n4", 1), R(124, 148, 24, 2, "n4", 1),
    TX(120, 168, "한 칸에 거의 1", "t", 12, "middle", 2),
    R(300, 106, 24, 44, "n2", 3), R(332, 124, 24, 26, "n2", 3), R(364, 128, 24, 22, "n2", 3),
    TX(360, 168, "여러 칸을 골고루", "t", 12, "middle", 3),
    TX(240, 200, "점수가 퍼지면 소프트맥스가 포화되고 기울기가 사라져요", "tb", 13, "middle", 4),
    TX(240, 226, "d_k = 512 면 표준편차가 약 22.63 이에요", "tm", 12, "middle", 4),
)

FIG_PE = SVG(
    TX(240, 22, "같은 단어, 다른 자리", "tb", 16),
    BOX(40, 50, 130, 28, "dog 임베딩", "box", "tb", 1, 13),
    BOX(310, 50, 130, 28, "dog 임베딩", "box", "tb", 1, 13),
    TX(105, 100, "+ 자리 0 벡터", "t", 13, "middle", 2),
    TX(375, 100, "+ 자리 2 벡터", "t", 13, "middle", 2),
    BOX(40, 114, 130, 28, "(0, 1, 0, 1)", "box2", "tb", 3, 13),
    BOX(310, 114, 130, 28, "(0.9093, -0.4161, 0.02, 0.9998)", "box2", "tb", 3, 11),
    A(105, 148, 105, 174, "e2", 4), A(375, 148, 375, 174, "e2", 4),
    TX(105, 196, "첫 자리 dog", "tb", 13, "middle", 4),
    TX(375, 196, "셋째 자리 dog", "tb", 13, "middle", 4),
    TX(240, 228, "더한 값이 달라져서 순서가 살아나요", "t", 13, "middle", 4),
)

FIG_FFN = SVG(
    TX(240, 22, "어텐션은 옮기고, FFN 은 가공해요", "tb", 16),
    *[BOX(28 + i * 110, 170, 92, 28, f"x{i + 1}", "n", "tl", 1, 13) for i in range(4)],
    *[A(74 + i * 110, 168, 74 + i * 110, 142, "e2", 2) for i in range(4)],
    *[BOX(28 + i * 110, 112, 92, 28, "FFN", "box2", "tb", 2, 13) for i in range(4)],
    *[A(74 + i * 110, 110, 74 + i * 110, 84, "e2", 3) for i in range(4)],
    *[BOX(28 + i * 110, 54, 92, 28, f"h{i + 1}", "box", "tb", 3, 13) for i in range(4)],
    TX(240, 224, "네 개의 FFN 은 똑같은 가중치를 나눠 써요", "tb", 13, "middle", 4),
    TX(240, 248, "여기서는 자리끼리 섞이지 않아요", "tm", 12, "middle", 4),
    h=270,
)

S = []


def page(p, title, terms, p1, p2=(), p3=(), p4=()):
    S.append({"p": p, "title": title, "terms": list(terms),
              "pass1": list(p1), "pass2": list(p2), "pass3": list(p3), "pass4": list(p4)})


# ---------------------------------------------------------------- p.31
page(31, "Part 3 표지: Self-Attention", ["Self-Attention", "Attention", "Recurrent Neural Network (RNN)"],
     [say("세 번째 부분 표지예요. 제목은 3 Self-Attention 이에요.",
          f"작은 글씨는 remove the recurrence, keep the attention, 곧 {RNN} 을 빼고 {ATT} 만 남긴다는 뜻이에요.",
          f"여기서부터가 2017년 이야기이고 {SA}이 주인공이에요.")],
     [points("영어 부제의 뜻",
             "remove the recurrence = 순환(한 걸음씩 도는 것)을 없앤다",
             "keep the attention = 어텐션은 그대로 남긴다",
             f"곧 {RNN} 은 버리고 {ATT} 만으로 문장을 처리한다는 선언이에요",
             f"Part 2 에서 {ATT}이 {IB}을 없앴고, 이제 순환까지 없애요")],
     [prof("교수님: 여기서부터는 셀프 어텐션을 활용한 트랜스포머를 배워 보겠습니다.",
           "교수님: 이제 RNN 은 아예 빼 버리고 어텐션만 남기면 된다.",
           "교수님: 논문 제목이 Attention Is All You Need 예요. 어텐션만 있으면 된다는 거죠.")],
     [])

# ---------------------------------------------------------------- p.32
page(32, "순환이 정말 필요할까요", ["Self-Attention", "Attention", "Recurrent Neural Network (RNN)",
                          "Hidden State", "Vanishing Gradient", "Gradient", "Parallelization", "Token"],
     [say(f"질문 하나로 시작해요. {ATT}이 이미 출력과 입력을 직접 이어 줬어요.",
          f"그러면 {RNN} 은 아직 무슨 일을 하고 있을까요?",
          f"남은 일은 한 문장 안에서 {TOK}끼리 정보를 섞는 것뿐이에요.",
          "그런데 그것도 어텐션이 할 수 있어요. 문장이 자기 자신을 보게 하면 돼요."),
      analogy("줄 서서 전달하기 vs 다 같이 마주 보기",
              "교실에서 맨 앞 사람의 쪽지를 맨 뒤까지 옆 사람에게 차례로 넘기면 여섯 번을 거쳐요. 대신 모두가 동시에 서로를 바라보면 한 번에 끝나요.",
              ("옆 사람에게 차례로 넘기기", RNN),
              ("모두가 서로를 바라보기", SA),
              ("전달하다 희미해진 쪽지", VG))],
     [points("슬라이드 영어와 우리말 뜻",
             "Do We Even Need Recurrence? = 순환이 정말 필요하긴 할까?",
             "Attention already connects every output to every input directly = 어텐션은 이미 모든 출력을 모든 입력에 바로 이어 준다",
             "Its job is to mix information within a sequence = RNN 의 일은 한 시퀀스 안에서 정보를 섞는 것이다",
             "if we let a sequence attend to itself = 시퀀스가 자기 자신에 주목하게 하면",
             "the maximum path length drops from n to 1 = 가장 긴 경로가 n 에서 1 로 줄어든다"),
      compare("RNN 과 셀프 어텐션의 차이 한눈에",
              ["보는 점", "RNN", "셀프 어텐션"],
              ["두 단어 사이 거리", "떨어진 만큼 여러 걸음", "언제나 1 걸음"],
              ["계산 순서", "앞 자리가 끝나야 다음", "전부 동시에"],
              [IB, "어텐션으로 이미 해결됨", "어텐션으로 이미 해결됨"],
              ["기울기가 겪는 곱셈", "거리만큼 여러 번", "한 번"])],
     [look("슬라이드를 짚어 읽어요",
           (0.05, 0.19, 0.90, 0.06, "첫 점: 어텐션은 이미 모든 출력과 모든 입력을 직접 잇는다. 그럼 RNN 은 왜 필요한가."),
           (0.05, 0.25, 0.90, 0.06, "둘째 점: RNN 의 일은 한 시퀀스 안에서 정보를 섞는 것인데, 어텐션도 그 일을 할 수 있다."),
           (0.07, 0.54, 0.86, 0.09, "주황 상자 열한 개가 The chef who went to the stores was out of food 예요."),
           (0.17, 0.44, 0.50, 0.11, "위쪽 초록 화살표: 셀프 어텐션이면 chef 와 was 가 1 걸음이에요."),
           (0.17, 0.63, 0.50, 0.11, "아래쪽 빨간 화살표: RNN 이면 6 번의 리커런트 걸음을 거쳐야 해요."),
           (0.10, 0.78, 0.76, 0.05, "아래 글: 선형 거리, 기울기가 O(n) 번 곱셈을 견뎌야 함, 시퀀스 안 병렬 불가")),
      steps("경로 길이를 세어 봐요",
            ["문장은 The chef who went to the stores was out of food 예요",
             "chef 는 2번째, was 는 8번째 토큰이에요",
             f"RNN 은 chef 의 정보를 {HS}에 실어 한 칸씩 옮겨요",
             "who, went, to, the, stores 를 지나 was 에 닿으니 6 걸음이에요",
             "셀프 어텐션은 was 가 chef 를 바로 쳐다봐요. 1 걸음이에요"],
            f"6 걸음 vs 1 걸음. 곱셈 횟수가 줄어드니 {VG}이 훨씬 덜해요.",
            "chef 와 was 사이"),
      figure("거리가 n 에서 1 로", FIG_PATH, "위는 셀프 어텐션의 한 걸음, 아래는 RNN 의 여섯 걸음이에요.", 4),
      prof("교수님: RNN 이 하는 중요한 역할 중 하나가 한 시퀀스 안에서 단어들 사이에 정보를 전달하는 거였어요.",
           "교수님: 이 정보 교환 자체는 어텐션도 할 수가 있다는 거죠.",
           f"교수님: 시퀀스가 자기 자신을 바라보게 만드는 게 {SA}의 핵심 아이디어예요.",
           f"Part 2 의 {IB}에 이어, 이번에는 순환 자체를 없애는 이야기예요.",
           "교수님: 셀프 어텐션의 가장 큰 장점은 병렬로 계산할 수 있다는 거고, 이 패러럴이 핵심이에요.")],
     [check("RNN 에서 두 단어가 6 칸 떨어져 있으면 정보가 지나야 하는 걸음 수는?",
            ["1 걸음", "3 걸음", "6 걸음", "36 걸음"], 2,
            f"{RNN} 은 {HS}를 한 칸씩 넘기므로 떨어진 칸 수만큼 걸어요. 셀프 어텐션은 1 걸음이에요."),
      english("시험 답안 문장",
              "셀프 어텐션은 두 토큰 사이의 최대 경로 길이를 n 에서 1 로 줄여, 먼 거리 의존을 학습하기 쉽게 하고 병렬 계산을 가능하게 한다.",
              "핵심은 두 가지, 경로 길이 1 과 병렬화(parallelization)예요.",
              "n 에서 1, 이 한 줄만 외워도 절반은 맞아요."),
      warn("헷갈리기 쉬운 점",
           f"셀프 어텐션이 {VG}을 직접 고치는 게 아니에요. 거리를 1 로 줄여서 비켜 가는 거예요.",
           f"{PAR}는 한 시퀀스 안에서의 이야기예요. 배치끼리는 RNN 도 병렬로 돌릴 수 있어요.")])

# ---------------------------------------------------------------- p.33
page(33, "크로스 어텐션과 셀프 어텐션", ["Cross-Attention", "Self-Attention", "Query", "Key", "Value",
                              "Encoder", "Decoder", "Attention", "Token"],
     [say(f"이름을 정리하는 쪽이에요. Part 2 에서 배운 {ATT}에 이름을 붙여요.",
          f"{DEC}가 {ENC}를 바라본 것처럼 서로 다른 시퀀스를 보면 {CA}이에요.",
          f"한 시퀀스가 자기 자신을 보면 {SA}이에요.",
          "기계는 똑같아요. 벡터가 어디서 오느냐만 달라요."),
      analogy("남의 책 보기 vs 내 노트 다시 보기",
              "시험 공부를 할 때 옆 사람 노트를 빌려 보는 것과, 내가 쓴 노트를 처음부터 다시 훑어보는 것은 읽는 방법은 같고 대상만 달라요.",
              ("옆 사람 노트 보기", CA),
              ("내 노트 다시 보기", SA),
              ("읽는 방법 자체", "점수, 소프트맥스, 가중합의 세 단계"))],
     [points("슬라이드 영어와 우리말 뜻",
             "queries come from one sequence, keys and values from another = 쿼리는 한 시퀀스에서, 키와 밸류는 다른 시퀀스에서 온다",
             "That is 2장의 attention = 그것이 Part 2 의 어텐션이다",
             "queries, keys and values all come from the same sequence = 쿼리, 키, 밸류가 모두 같은 시퀀스에서 온다",
             "Every token asks every other token a question = 모든 토큰이 다른 모든 토큰에게 질문한다",
             "Same machinery, the only change is where the vectors come from = 기계는 같고 벡터가 어디서 오는지만 바뀐다"),
      compare("두 어텐션 비교",
              ["구분", CA, SA],
              ["쿼리", "디코더(만드는 쪽)", "같은 문장의 토큰"],
              ["키, 밸류", "인코더(읽는 쪽)", "같은 문장의 토큰"],
              ["쓰는 곳", "번역의 디코더 중간", "인코더와 디코더 둘 다"])],
     [look("슬라이드를 짚어 읽어요",
           (0.05, 0.19, 0.90, 0.06, "첫 점: 크로스 어텐션은 쿼리가 한 시퀀스, 키와 밸류가 다른 시퀀스에서 온다."),
           (0.05, 0.25, 0.90, 0.06, "둘째 점: 셀프 어텐션은 셋 다 같은 시퀀스에서 온다."),
           (0.10, 0.33, 0.38, 0.45, "왼쪽 그림: 초록 상자 s_t 하나가 아래 주황 상자 네 개를 향해 화살표를 쏴요."),
           (0.55, 0.33, 0.40, 0.45, "오른쪽 그림: 파란 상자들이 서로서로를 향해 화살표를 쏴요."),
           (0.22, 0.85, 0.56, 0.05, "아래 파란 글: 기계는 같고 벡터가 어디서 오는지만 바뀐다.")),
      prof("교수님: 챕터 2까지 배웠던 어텐션을 크로스 어텐션이라고 할게요.",
           "교수님: 인코더와 디코더를 크로스해서 어텐션을 보기 때문에 크로스 어텐션이라고 명명합니다.",
           "교수님: 셀프 어텐션은 한 시퀀스 안에서 모든 토큰들이 서로서로를 어텐션 하는 거예요.")],
     [check("쿼리는 디코더에서, 키와 밸류는 인코더에서 오는 어텐션의 이름은?",
            [CA, SA, "스케일드 닷프로덕트 어텐션", "멀티 헤드 어텐션"], 0,
            f"서로 다른 두 시퀀스를 가로질러 보기 때문에 {CA}이에요."),
      english("시험 답안 문장",
              "크로스 어텐션은 쿼리와 키, 밸류가 서로 다른 시퀀스에서 오고, 셀프 어텐션은 셋 다 같은 시퀀스에서 온다. 계산 방식은 동일하다.",
              "차이는 오직 벡터의 출처 한 가지예요.",
              "크로스는 가로지른다, 셀프는 자기 자신, 이름 그대로예요."),
      warn("헷갈리기 쉬운 점",
           f"{CA}이 더 어려운 게 아니에요. 오히려 먼저 나온 옛날 방식이에요.",
           f"{SA}도 {QRY}, {KEY}, {VAL} 세 가지를 그대로 써요. 새로운 계산이 아니에요.")])

# ---------------------------------------------------------------- p.34
page(34, "쿼리, 키, 밸류", ["Query", "Key", "Value", "Self-Attention", "Parameter", "Embedding",
                      "Token", "Dot Product", "Attention Score"],
     [say(f"{SA}의 심장이에요. {TOK} 하나가 세 역할을 동시에 해요.",
          f"{QRY}는 나는 무엇을 찾고 있나, {KEY}는 나는 이런 것이라고 광고하는 이름표,",
          f"{VAL}는 내가 뽑히면 실제로 건네줄 내용이에요.",
          "같은 입력 벡터에 서로 다른 행렬 세 개를 곱해서 만들어요."),
      analogy("도서관에서 책 찾기",
              "내가 찾는 주제를 머리에 떠올리고(질문), 책등에 붙은 제목을 훑어보고(이름표), 마음에 드는 책의 내용을 읽어요(내용).",
              ("내가 찾는 주제", QRY),
              ("책등의 제목", KEY),
              ("책 안의 내용", VAL))],
     [points("슬라이드 영어와 우리말 뜻",
             "Each token plays three roles at once = 각 토큰이 세 역할을 동시에 한다",
             "three learned linear maps of the same input vector = 같은 입력 벡터에 대한 학습된 선형 변환 셋",
             "Query, what am I looking for? = 쿼리, 나는 무엇을 찾고 있나",
             "Key, what do I advertise? = 키, 나는 무엇을 광고하나",
             "Value, what do I hand over if chosen? = 밸류, 뽑히면 무엇을 건네주나",
             "shared across all positions = 모든 자리가 함께 쓴다"),
      compare("세 역할의 쓰임새",
              ["역할", "질문", "어디에 쓰이나"],
              [QRY, "나는 무엇을 찾나", "점수 계산의 출발점"],
              [KEY, "나는 무엇을 광고하나", "점수 계산에서 쿼리와 내적"],
              [VAL, "뽑히면 무엇을 주나", "가중합에 들어가는 내용"])],
     [formula("세 벡터 만들기",
              r"q_i = W^Q x_i,\quad k_i = W^K x_i,\quad v_i = W^V x_i",
              [(r"x_i", f"i 번째 토큰의 입력 벡터, 곧 {EMB} 이에요"),
               (r"W^Q", "쿼리를 만드는 학습 가능한 행렬"),
               (r"W^K", "키를 만드는 학습 가능한 행렬"),
               (r"W^V", "밸류를 만드는 학습 가능한 행렬"),
               (r"q_i, k_i, v_i", "그 토큰의 쿼리, 키, 밸류 벡터")],
              f"입력 하나에서 세 벡터가 나와요. 세 행렬이 학습되는 {PARAM}예요."),
      figure("토큰 하나가 세 역할을 동시에", FIG_QKV, "같은 x 에 서로 다른 행렬 셋을 곱해요.", 4),
      look("슬라이드를 짚어 읽어요",
           (0.05, 0.19, 0.90, 0.05, "첫 점: 각 토큰이 세 역할을 동시에 하고, 같은 입력 벡터의 학습된 선형 변환으로 만든다."),
           (0.05, 0.25, 0.90, 0.05, "둘째 점: query 는 무엇을 찾나, key 는 무엇을 광고하나, value 는 무엇을 건네주나."),
           (0.23, 0.38, 0.54, 0.07, "위쪽 상자 다섯 개가 문장 Zuko made his uncle tea 예요."),
           (0.21, 0.48, 0.42, 0.16, "가운데 작은 식 세 줄이 q, k, v 를 만드는 공식이에요."),
           (0.12, 0.70, 0.76, 0.11, "아래 큰 글씨 세 식이 오늘 외워야 할 공식이에요."),
           (0.30, 0.86, 0.40, 0.04, "맨 아래: 세 행렬은 모든 자리가 공유한다.")),
      prof("교수님: 이 쿼리, 키, 밸류 3개의 컨셉을 이해해야 뒤에 트랜스포머를 이해할 수 있고 자연어 처리를 이해할 수 있어요.",
           "교수님: 키는 사전의 색인 같은 거예요. 나는 이런 정보를 갖고 있으니 나를 찾아봐라 하고 광고하는 게 키다.",
           "교수님: 중요한 점이 위치마다 이 행렬을 따로 만드는 게 아니고, 모든 토큰들이 공유하는 겁니다.")],
     [check(f"{WSUM}에 실제로 들어가는 벡터는 무엇인가요?",
            [QRY, KEY, VAL, "입력 임베딩 그대로"], 2,
            f"{KEY}는 점수를 만들 때만 쓰고, 실제로 더해지는 내용은 {VAL}예요."),
      exam("N4 Check Yourself",
           "Q1 (Part 2). What exactly is the difference between self-attention and the attention of 2장?",
           "셀프 어텐션과 Part 2 의 어텐션은 정확히 무엇이 다른가요?",
           ["Part 2 어텐션은 쿼리가 디코더, 키와 밸류가 인코더에서 왔어요",
            "셀프 어텐션은 쿼리, 키, 밸류가 모두 같은 시퀀스에서 나와요",
            "Part 2 에서는 키와 밸류가 사실 같은 h 였는데, 셀프 어텐션은 둘을 나눠요",
            "그리고 점수를 루트 d_k 로 나누는 스케일이 추가돼요"],
           "출처가 같은 시퀀스인지 다른 시퀀스인지, 그리고 키와 밸류를 나눴는지가 차이예요."),
      english("시험 답안 문장",
              "셀프 어텐션에서 각 토큰은 같은 입력 벡터에 W^Q, W^K, W^V 를 곱해 쿼리, 키, 밸류를 만들며, 이 세 행렬은 모든 위치가 공유한다.",
              "만드는 법 한 줄, 공유한다 한 줄이면 충분해요.",
              "Q 는 질문, K 는 이름표, V 는 내용. 세 글자로 외워요."),
      warn("헷갈리기 쉬운 점",
           f"{KEY}와 {VAL}는 다른 벡터예요. Part 2 어텐션에서는 둘이 같았을 뿐이에요.",
           "W^Q, W^K, W^V 는 토큰마다 다른 게 아니라 문장 전체가 같은 것을 써요.")])

# ---------------------------------------------------------------- p.35
page(35, "쿼리 하나를 따라가 보기", ["Self-Attention", "Query", "Key", "Value", "Attention Weight",
                            "Softmax", "Weighted Sum", "Context Vector", "Token", "Dot Product"],
     [say(f"{TOK} 하나를 골라 끝까지 따라가는 쪽이에요.",
          "his 라는 토큰의 쿼리를 모든 키와 비교하고, 소프트맥스를 쓰고, 밸류를 섞어요.",
          "그 결과가 his 의 새 벡터가 돼요. 이제 his 안에 uncle 의 정보가 들어 있어요.",
          "Part 2 의 세 단계와 완전히 같아요."),
      analogy("반 친구들에게 한 번씩 물어보기",
              "내가 궁금한 것을 들고 반 친구 다섯 명에게 차례로 묻고, 도움이 된 만큼 비중을 둬서 답을 하나로 합쳐요.",
              ("내 질문", QRY),
              ("친구들의 이름표", KEY),
              ("친구들의 대답", VAL),
              ("합쳐진 한 문장", CTX))],
     [points("슬라이드 영어와 우리말 뜻",
             "Take the query of one token = 토큰 하나의 쿼리를 가져온다",
             "score it against every key = 모든 키에 대해 점수를 매긴다",
             "softmax, and mix the values = 소프트맥스를 하고 밸류를 섞는다",
             "The result replaces that token's vector = 결과가 그 토큰의 벡터를 대신한다",
             "Every token gets rewritten as a blend of the tokens it cares about = 모든 토큰이 자기가 신경 쓴 토큰들의 혼합으로 다시 쓰인다"),
      steps("세 단계를 이름으로 확인해요",
            [f"1단계, q3 와 k1 ... k5 를 {DP}해서 점수를 만들어요",
             "2단계, 그 점수를 루트 d_k 로 나누고 소프트맥스에 넣어요",
             f"3단계, 나온 {AW}로 v1 ... v5 를 {WSUM}해요",
             f"결과 o3 는 Part 2 의 {CTX} 와 같은 것이에요"],
            f"Part 2 의 세 단계와 같아요. o3 가 바로 그때의 {CTX} 예요.")],
     [steps("어텐션 가중치를 슬라이드에서 읽어요",
            ["슬라이드의 막대 다섯 개가 0.05, 0.10, 0.08, 0.62, 0.15 예요",
             "다 더하면 0.05 + 0.10 + 0.08 + 0.62 + 0.15 = 1.00 이에요",
             "가장 큰 값은 네 번째인 0.62 이고, 네 번째 토큰은 uncle 이에요",
             "그래서 his 를 다시 쓸 때 uncle 의 내용을 가장 많이 가져와요"],
            "his 의 새 벡터 o3 는 uncle 쪽으로 크게 기울어요. his 가 uncle 을 꾸미니 자연스러워요.",
            "가중치 0.05, 0.10, 0.08, 0.62, 0.15"),
      formula("이 쪽의 두 식",
              r"\alpha_{ij} = \mathrm{softmax}_j\left(\frac{q_i^{\top} k_j}{\sqrt{d_k}}\right), \quad o_i = \sum_j \alpha_{ij} v_j",
              [(r"q_i^{\top} k_j", "i 번째 쿼리와 j 번째 키의 내적"),
               (r"\sqrt{d_k}", "키 벡터의 칸 수의 제곱근으로 나눠요"),
               (r"\alpha_{ij}", f"i 가 j 를 보는 {AW}"),
               (r"\sum_j", "모든 자리 j 에 대해 더해요"),
               (r"o_i", "i 번째 토큰의 새 표현")],
              f"위는 {SMX}, 아래는 {WSUM}이에요."),
      look("슬라이드를 짚어 읽어요",
           (0.05, 0.19, 0.90, 0.05, "첫 점: 한 토큰의 쿼리로 모든 키에 점수를 매기고, 소프트맥스하고, 밸류를 섞는다."),
           (0.05, 0.25, 0.90, 0.05, "둘째 점: 결과가 그 토큰의 벡터를 대신한다. his 가 uncle 의 정보를 갖게 된다."),
           (0.02, 0.34, 0.24, 0.10, "왼쪽 위 번호 1 상자 안의 식이 어텐션 가중치 공식이에요."),
           (0.15, 0.39, 0.55, 0.12, "파란 막대와 0.05, 0.10, 0.08, 0.62, 0.15 가 어텐션 가중치예요."),
           (0.15, 0.54, 0.55, 0.08, "초록 상자 v1 ... v5 가 밸류, 그 아래 주황 상자가 키예요."),
           (0.71, 0.53, 0.20, 0.17, "오른쪽 파란 o3 가 새 표현, 보라 q3 가 his 의 쿼리예요.")),
      prof("교수님: 히스가 봤을 때 엉클 위치의 웨이트가 0.62 로 가장 크게 나왔죠.",
           "교수님: 현재 히스를 표현할 때 엉클의 정보를 가장 많이 참고하고 있다는 거죠.",
           "교수님: 처음에는 인풋 x3 였는데, 셀프 어텐션 레이어를 지나면 각 토큰마다 새로운 표현 o3 가 나와요.")],
     [check("슬라이드에서 his 가 가장 크게 바라본 토큰은?",
            ["Zuko", "made", "uncle", "tea"], 2,
            f"네 번째 막대 0.62 가 uncle 자리예요. his 가 uncle 을 꾸미니 자연스러운 {AW}예요."),
      english("시험 답안 문장",
              "셀프 어텐션은 한 토큰의 쿼리를 모든 키와 비교해 점수를 만들고, 소프트맥스로 가중치를 얻은 뒤 밸류의 가중합으로 그 토큰의 새 표현을 만든다.",
              "점수, 소프트맥스, 가중합의 세 단계를 그대로 쓰면 돼요.",
              "Part 2 답안에서 인코더 상태만 밸류로 바꾸면 그대로예요."),
      warn("헷갈리기 쉬운 점",
           "자기 자신도 포함해서 점수를 매겨요. q3 는 k3 와도 내적해요.",
           "새 표현 o3 가 x3 를 완전히 갈아엎는 게 아니라, 다른 토큰의 정보가 섞인 새 벡터가 되는 거예요.")])

# ---------------------------------------------------------------- p.36
page(36, "셀프 어텐션의 식", ["Self-Attention", "Scaled Dot-Product Attention", "Attention Score",
                       "Attention Weight", "Softmax", "Weighted Sum", "Query", "Key", "Value", "Dot Product"],
     [say("Part 2 에서 본 네 줄이 그대로 돌아왔어요.",
          f"달라진 것은 q, k, v 가 모두 같은 시퀀스에서 온다는 것, 그리고 루트 d_k 로 나눈다는 것뿐이에요.",
          "슬라이드 아래 파란 상자의 한 줄이 오늘 가장 중요한 식이에요."),
      analogy("같은 옷, 다른 무늬",
              "Part 2 의 식과 여기 식은 같은 옷인데 무늬만 바꿔 입은 거예요.",
              ("옷", "점수, 소프트맥스, 가중합의 세 단계"),
              ("바뀐 무늬", "q, k, v 가 같은 시퀀스에서 온다"),
              ("새로 단 단추", "루트 d_k 로 나누기"))],
     [points("슬라이드 영어와 우리말 뜻",
             "The same four lines as 2장 = Part 2 와 같은 네 줄이다",
             "now with q, k, v all coming from the same sequence = 이제 q, k, v 가 모두 같은 시퀀스에서 온다",
             "plus one new factor we are about to justify = 그리고 곧 설명할 새 인자 하나가 더 있다",
             "(1) similarity scores = 유사도 점수",
             "(2) attention weights = 어텐션 가중치",
             "(3) weighted sum of values = 밸류의 가중합"),
      compare("세 식의 이름과 하는 일",
              ["번호", "이름", "하는 일"],
              ["(1)", ASC, "쿼리와 키를 내적하고 루트 d_k 로 나눠요"],
              ["(2)", AW, "소프트맥스로 합이 1 이 되게 만들어요"],
              ["(3)", "가중합", "밸류를 가중치만큼 섞어요"])],
     [formula("오늘 가장 중요한 한 줄",
              r"\mathrm{Attention}(Q,K,V) = \mathrm{softmax}\!\left(\frac{QK^{\top}}{\sqrt{d_k}}\right)V",
              [(r"Q", "쿼리들을 줄줄이 쌓은 행렬"),
               (r"K^{\top}", "키 행렬을 눕힌 것(전치)"),
               (r"QK^{\top}", "모든 쿼리와 모든 키의 내적을 한 번에"),
               (r"\sqrt{d_k}", "점수가 너무 커지지 않게 나눠 주는 값"),
               (r"\mathrm{softmax}", "줄마다 합이 1 이 되게"),
               (r"V", "밸류 행렬, 실제로 섞이는 내용")],
              f"이 한 줄이 {SDP}이에요. 시험에 나오면 이대로 쓰면 돼요."),
      steps("작은 숫자로 손계산을 해 봐요",
            ["d_k = 4 로 두면 루트 d_k = 2 예요",
             "q3 = (1, 1, 1, 1), k1 = (1, 1, 1, 1), k2 = (1, 1, 0, 0), k3 = (0, 0, 0, 0) 이라고 해요",
             "내적은 q3 와 k1 은 4, k2 는 2, k3 는 0 이에요",
             "루트 d_k = 2 로 나누면 점수가 2, 1, 0 이 돼요",
             "소프트맥스: exp(2) = 7.389, exp(1) = 2.718, exp(0) = 1, 합은 11.107 이에요",
             "각각 나누면 0.6652, 0.2447, 0.0900 이고 다 더하면 1 이에요",
             "밸류가 v1 = (2, 0), v2 = (0, 2), v3 = (1, 1) 이면",
             "o3 = 0.6652 x (2,0) + 0.2447 x (0,2) + 0.0900 x (1,1) = (1.4204, 0.5794) 예요"],
            "새 표현 o3 = (1.4204, 0.5794). v1 쪽으로 크게 기울었어요.",
            "d_k = 4, 쿼리 하나와 키 세 개"),
      look("슬라이드를 짚어 읽어요",
           (0.05, 0.19, 0.90, 0.05, "맨 위 한 줄: Part 2 와 같은 네 줄인데 q, k, v 가 같은 시퀀스에서 온다."),
           (0.18, 0.36, 0.20, 0.16, "왼쪽 식 (1) 이 유사도 점수 e_ij 예요."),
           (0.39, 0.36, 0.22, 0.16, "가운데 식 (2) 가 소프트맥스로 만든 어텐션 가중치 알파예요."),
           (0.62, 0.36, 0.20, 0.16, "오른쪽 식 (3) 이 밸류의 가중합 o_i 예요."),
           (0.25, 0.57, 0.47, 0.14, "파란 상자 안의 Attention(Q, K, V) 한 줄이 핵심이에요."),
           (0.34, 0.86, 0.32, 0.04, "맨 아래: 알아보겠어요? 이건 Part 2 가 옷만 갈아입은 것.")),
      prof("교수님: 스코어 계산하고, 소프트맥스 통해서 웨이트 만들고, 웨이티드 썸 하는 구조는 그대로예요.",
           "교수님: 다른 건 쿼리, 키, 밸류를 나눴다는 거랑 스케일드 닷 프로덕트로 루트 d_k 로 나눴다는 것뿐이에요.",
           "교수님: 트랜스포머 논문에서는 이 루트 d_k 때문에 스케일드 닷 프로덕트 어텐션이라고 표현을 해요.")],
     [check("Attention(Q, K, V) 식에서 소프트맥스 안에 들어가는 것은?",
            [r"$QK^{\top}/\sqrt{d_k}$", r"$QV^{\top}$", r"$K V^{\top}/\sqrt{d_k}$", r"$Q + K$"], 0,
            f"{QRY}와 {KEY}의 내적을 루트 d_k 로 나눈 것이 들어가요. {VAL}는 소프트맥스 밖에서 곱해져요."),
      exam("N4 Check Yourself",
           "Q3 (Part 2). Why divide by root d_k, and what goes wrong if you forget?",
           "왜 루트 d_k 로 나누나요? 안 나누면 무엇이 잘못되나요?",
           ["내적의 분산이 d_k 라서 차원이 크면 점수가 크게 퍼져요",
            "큰 점수를 소프트맥스에 넣으면 한 칸이 거의 1 이 되는 뾰족한 분포가 돼요",
            "포화된 소프트맥스는 기울기가 거의 0 이라 학습이 멈춰요",
            "루트 d_k 로 나누면 분산이 다시 1 이 돼요"],
           "분산을 1 로 되돌리기 위해서예요. 안 나누면 소프트맥스가 포화되어 기울기가 사라져요."),
      english("시험 답안 문장",
              "스케일드 닷프로덕트 어텐션은 쿼리와 키의 내적을 루트 d_k 로 나눈 뒤 소프트맥스를 취하고, 그 가중치로 밸류를 가중합한다.",
              "식 한 줄과 나누는 이유 한 줄을 같이 적어요.",
              "softmax(QK^T / 루트 d_k) V, 이 순서만 지키면 돼요."),
      warn("헷갈리기 쉬운 점",
           "K 를 전치(눕히기)해야 행렬 곱이 맞아요. Q 가 (n, d_k) 이고 K^T 가 (d_k, n) 이에요.",
           "나누는 것은 d_k 가 아니라 루트 d_k 예요.")])

# ---------------------------------------------------------------- p.37
page(37, "한꺼번에: 행렬 형태", ["Self-Attention", "Query", "Key", "Value", "Parallelization",
                         "Softmax", "Attention Weight", "Token"],
     [say("이제 토큰 하나가 아니라 문장 전체를 한 번에 계산해요.",
          "쿼리를 모두 쌓아 Q, 키를 모두 쌓아 K, 밸류를 모두 쌓아 V 라는 행렬을 만들어요.",
          "행렬 곱 세 번이면 끝이에요. 자리를 도는 반복문이 없어요.",
          f"이게 GPU 가 잘하는 모양이고 {PAR}의 정체예요."),
      analogy("한 명씩 vs 반 전체 한 번에",
              "성적표를 한 명씩 계산하면 오래 걸리지만, 표를 통째로 엑셀에 넣고 한 번에 계산하면 순식간이에요.",
              ("한 명씩 계산", RNN),
              ("표 통째로 한 번에", SA),
              ("엑셀", "GPU 의 행렬 곱"))],
     [points("슬라이드 영어와 우리말 뜻",
             "Stack all the queries into a matrix Q = 모든 쿼리를 쌓아 행렬 Q 를 만든다",
             "Three matrix multiplications and you are done = 행렬 곱 세 번이면 끝난다",
             "No loop over positions = 자리를 도는 반복문이 없다",
             "which is exactly why this runs so well on a GPU = 그래서 GPU 에서 아주 잘 돈다",
             "The whole sequence in one batched matmul = 시퀀스 전체가 한 번의 묶음 행렬 곱"),
      compare("모양(shape) 따라가기",
              ["무엇", "모양", "뜻"],
              ["Q", "n x d_k", "토큰 n 개, 쿼리 칸 수 d_k"],
              ["K 전치", "d_k x n", "곱셈이 맞게 눕힌 것"],
              ["점수", "n x n", "토큰끼리 다 비교한 표"],
              ["A", "n x n", "소프트맥스 뒤, 줄마다 합 1"],
              ["O", "n x d_v", "새 표현, 토큰마다 한 줄"])],
     [steps("모양이 맞는지 손으로 따라가 봐요",
            ["토큰이 5개이고 d_k = 4, d_v = 3 이라고 해요",
             "Q 는 (5, 4), K 는 (5, 4) 예요",
             "K 를 눕히면 K 전치는 (4, 5) 가 돼요",
             "(5, 4) 곱하기 (4, 5) 는 (5, 5) 예요. 가운데 4 가 사라져요",
             "소프트맥스는 모양을 바꾸지 않으니 A 도 (5, 5) 예요",
             "V 는 (5, 3) 이므로 (5, 5) 곱하기 (5, 3) 은 (5, 3) 이에요"],
            "최종 O 는 (5, 3). 토큰 하나당 새 표현 한 줄이에요.",
            "n = 5, d_k = 4, d_v = 3"),
      figure("한 번의 행렬 곱으로 전부", FIG_MATMUL, "Q 와 K 전치를 곱하고, 소프트맥스하고, V 를 곱해요.", 4),
      look("슬라이드를 짚어 읽어요",
           (0.05, 0.19, 0.90, 0.05, "첫 점: 쿼리, 키, 밸류를 각각 쌓아 행렬 곱 세 번이면 끝난다."),
           (0.05, 0.25, 0.90, 0.05, "둘째 점: 자리를 도는 반복문이 없어서 GPU 에서 잘 돌고 RNN 은 그렇지 못하다."),
           (0.24, 0.32, 0.47, 0.13, "파란 상자 안이 Attention(Q, K, V) 식이에요."),
           (0.09, 0.58, 0.76, 0.16, "가운데 그림이 Q x K 전치 -> 점수 -> A x V -> O 순서예요."),
           (0.09, 0.74, 0.76, 0.04, "상자 아래 작은 글씨가 각 행렬의 모양(n x d_k 등)이에요."),
           (0.49, 0.76, 0.18, 0.04, "A 아래 rows sum to 1 은 줄마다 합이 1 이라는 뜻이에요.")),
      prof("교수님: 모든 토큰의 쿼리를 쌓으면 행렬 Q 가 되고, 키를 쌓아 K, 밸류를 쌓아 V 를 만들 수 있어요.",
           "교수님: Q K 전치를 계산하면 바로 n 바이 n 스코어 매트릭스가 나와요.",
           "교수님: GPU 는 매트릭스를 올려놓고 포워드 백워드 치우는 걸 잘하기 때문에 병렬 연산을 아주 잘 활용할 수 있는 구조예요.",
           "교수님: RNN 은 t 를 처리하려면 t-1 까지 다 처리했어야 하는데, 얘는 앞에 있는 거랑 같이 처리할 수가 있다는 거죠."),
      bg("기초 다지기 3단원", "(a, b) 모양과 (b, c) 모양을 곱하면 (a, c) 가 돼요. 가운데 b 가 맞아야 곱할 수 있어요.",
         "전치(transpose)는 표를 눕혀서 행과 열을 바꾸는 것이에요.")],
     [check("토큰이 n 개일 때 점수 행렬의 모양은?",
            ["n x d_k", "n x n", "d_k x d_k", "n x d_v"], 1,
            "모든 토큰이 모든 토큰과 비교되므로 n 줄 n 칸짜리 정사각형 표가 나와요."),
      exam("N4 Check Yourself",
           "Q6 (Part 2, 일부). Why is attention O(n squared)?",
           "어텐션의 비용이 왜 n 의 제곱인가요?",
           ["점수 행렬이 n 줄 n 칸이에요",
            "칸 하나가 토큰 한 쌍의 점수라서 칸이 n x n 개예요",
            "그래서 계산도 메모리도 n 의 제곱으로 늘어요",
            "n = 512 면 262,144 칸인데 n = 128,000 이면 약 164억 칸이에요"],
           "점수 행렬이 n x n 이기 때문이에요. 자세한 이야기는 p.55 에서 해요."),
      english("시험 답안 문장",
              "셀프 어텐션은 Q, K, V 를 행렬로 쌓아 한 번의 행렬 곱으로 계산하므로 위치마다 순서대로 돌 필요가 없고, 따라서 GPU 에서 병렬 처리가 가능하다.",
              "병렬화가 가능한 이유를 반복문이 없다는 말로 설명해요.",
              "교수님이 패러럴이 핵심이라고 한 바로 그 부분이에요."),
      warn("헷갈리기 쉬운 점",
           "d_k 와 d_v 는 달라도 돼요. 점수는 d_k 로, 결과 칸 수는 d_v 로 정해져요.",
           f"{PAR}가 된다고 계산량이 줄어드는 건 아니에요. 동시에 할 뿐이에요.")])

# ---------------------------------------------------------------- p.38
page(38, "왜 루트 d_k 로 나눌까요", ["Scaled Dot-Product Attention", "Softmax", "Attention Score",
                             "Attention Weight", "Gradient", "Dot Product", "Self-Attention"],
     [say("오늘 유일하게 새로 생긴 나누기 한 번의 이유를 설명하는 쪽이에요.",
          "칸 수가 많아질수록 내적 값이 크게 퍼져요.",
          "점수가 크면 소프트맥스가 한 칸만 보는 뾰족한 모양이 되고, 그러면 기울기가 사라져요.",
          "루트 d_k 로 나누면 퍼짐이 다시 1 로 돌아와요."),
      analogy("확성기 볼륨 줄이기",
              "볼륨을 너무 키우면 제일 큰 소리만 들리고 나머지는 하나도 안 들려요. 볼륨을 적당히 낮추면 여러 소리를 함께 들을 수 있어요.",
              ("너무 큰 볼륨", "나누지 않은 큰 점수"),
              ("들리는 소리 하나", "뾰족한 소프트맥스"),
              ("볼륨 낮추기", "루트 d_k 로 나누기"))],
     [points("슬라이드 영어와 우리말 뜻",
             "If q and k have independent unit-variance entries = q 와 k 의 각 칸이 서로 독립이고 분산이 1 이면",
             "their dot product has variance d_k = 그 내적의 분산은 d_k 이다",
             "with d_k = 512 the scores are typically plus or minus 20 or more = d_k 가 512 면 점수가 보통 플러스마이너스 20 이상이다",
             "Huge scores make softmax nearly one-hot = 큰 점수는 소프트맥스를 거의 원-핫으로 만든다",
             "a saturated softmax has almost no gradient = 포화된 소프트맥스는 기울기가 거의 없다",
             "Dividing by root d_k puts the variance back to 1 = 루트 d_k 로 나누면 분산이 다시 1 이 된다"),
      compare("차원이 커지면 점수가 얼마나 퍼지나",
              ["d_k", "표준편차 = 루트 d_k", "점수 범위 느낌"],
              ["8", "2.83", "좁게 모여 있어요"],
              ["64", "8.0", "조금 퍼져요"],
              ["512", "22.63", "플러스마이너스 20 을 넘어요"])],
     [formula("내적의 분산",
              r"q \cdot k = \sum_{m=1}^{d_k} q_m k_m, \quad \mathrm{Var}(q \cdot k) = d_k \Rightarrow \mathrm{sd} = \sqrt{d_k}",
              [(r"q_m k_m", "같은 자리끼리 곱한 것"),
               (r"\sum_{m=1}^{d_k}", "칸 수 d_k 만큼 더해요"),
               (r"\mathrm{Var}", "얼마나 넓게 퍼지는지를 재는 값"),
               (r"\sqrt{d_k}", "퍼짐의 크기, 곧 표준편차")],
              "칸을 많이 더할수록 결과가 크게 흔들려요. 그래서 루트 d_k 로 나눠요."),
      steps("나누기 전과 후를 숫자로 비교해요",
            ["점수가 4, 2, 0 이라고 해 봐요",
             "그대로 소프트맥스하면 0.8668, 0.1173, 0.0159 예요. 첫 칸이 거의 다 가져가요",
             "d_k = 4 이므로 루트 d_k = 2 로 나누면 점수가 2, 1, 0 이 돼요",
             "다시 소프트맥스하면 0.6652, 0.2447, 0.0900 이에요",
             "가장 큰 값이 0.8668 에서 0.6652 로 내려가고 나머지가 살아났어요"],
            "나눠 주면 분포가 덜 뾰족해져요. 여러 자리를 함께 볼 수 있어요.",
            "점수 4, 2, 0"),
      steps("극단적인 경우도 봐요",
            ["점수가 20, 0, 1 이라고 해 봐요. d_k = 512 라면 흔한 크기예요",
             "그대로 소프트맥스하면 첫 칸이 거의 1, 나머지는 거의 0 이에요",
             "루트 512 는 약 22.63 이에요",
             "22.63 으로 나누면 점수가 약 0.88, 0, 0.04 가 돼요",
             "소프트맥스하면 0.5420, 0.2239, 0.2341 로 골고루 퍼져요"],
            "나누지 않으면 사실상 한 칸만 보는 셈이 돼요. 기울기도 거의 0 이에요.",
            "점수 20, 0, 1 과 d_k = 512"),
      look("슬라이드를 짚어 읽어요",
           (0.05, 0.19, 0.90, 0.09, "첫 점: q 와 k 의 칸이 독립이고 분산 1 이면 내적의 분산이 d_k 가 된다."),
           (0.05, 0.28, 0.90, 0.05, "둘째 점: 큰 점수는 소프트맥스를 거의 원-핫으로 만들고 기울기를 없앤다."),
           (0.22, 0.37, 0.26, 0.31, "왼쪽 그래프: d_k 가 8, 64, 512 로 커질수록 분포가 넓게 퍼져요."),
           (0.50, 0.37, 0.29, 0.31, "오른쪽 그래프: 빨강은 안 나눈 것, 초록은 나눈 것이에요."),
           (0.28, 0.72, 0.45, 0.09, "아래 식이 내적의 분산이 d_k 이고 표준편차가 루트 d_k 라는 뜻이에요.")),
      prof("교수님: q 와 k 의 각 성분이 평균 0, 분산 1 이고 서로 독립이라고 가정하면 내적의 분산이 d_k 가 돼요.",
           "교수님: 값이 너무 커지면 소프트맥스 특성상 큰 값에 너무 몰리게 돼요. 뾰족해지는 거죠.",
           "교수님: 그레디언트가 매우 작아져서 학습 효율이 매우 안 좋습니다.",
           "교수님: 이 슬라이드는 이해가 어렵다면 그냥 스코어 스케일이 너무 커지니까 줄여 준다고 봐도 괜찮아요."),
      bg("기초 다지기 6단원", f"{SMX}는 점수 차이를 exp 로 키워요. 점수 차이가 2 면 exp 차이는 약 7.4 배예요.",
         "그래서 점수 범위가 커질수록 분포가 훨씬 빨리 뾰족해져요.")],
     [check("루트 d_k 로 나누지 않으면 생기는 문제는?",
            ["소프트맥스가 포화되어 기울기가 거의 0 이 된다", "합이 1 이 되지 않는다",
             "행렬 곱의 모양이 맞지 않는다", "밸류가 음수가 된다"], 0,
            f"합은 {SMX}가 늘 1 로 만들어 줘요. 문제는 분포가 뾰족해져 {GRAD}가 사라지는 것이에요."),
      english("시험 답안 문장",
              "쿼리와 키의 내적은 분산이 d_k 이므로 차원이 크면 점수가 크게 퍼진다. 큰 점수는 소프트맥스를 포화시켜 기울기를 없애므로 루트 d_k 로 나누어 분산을 1 로 되돌린다.",
              "분산 d_k, 포화, 기울기 소멸의 세 낱말을 꼭 넣어요.",
              "분산이 d_k 니까 표준편차는 루트 d_k, 그래서 루트 d_k 로 나눈다.")

      ,
      warn("헷갈리기 쉬운 점",
           "d_k 로 나누는 게 아니라 루트 d_k 로 나눠요. 분산이 아니라 표준편차를 맞추는 거예요.",
           "나눈다고 점수의 순서가 바뀌지는 않아요. 순서는 그대로이고 간격만 좁아져요.")])

# ---------------------------------------------------------------- p.39
page(39, "아직 세 가지가 빠졌어요", ["Self-Attention", "Permutation Equivariance", "Positional Encoding",
                           "Position-wise Feed-Forward Network (FFN)", "Causal Masking",
                           "Nonlinearity", "Transformer", "Language Model (LM)"],
     [say(f"{SA}만으로는 아직 쌓을 수 있는 층이 아니에요.",
          "구멍이 세 개 있어요. 교수님이 배리어 3개라고 불렀어요.",
          "순서를 모른다, 비선형이 없다, 미래를 훔쳐본다.",
          f"이 세 구멍을 각각 한 부품으로 막으면 그게 {TRF} 블록이에요."),
      analogy("자전거에 빠진 세 부품",
              "바퀴만 있다고 자전거가 되지 않아요. 안장, 페달, 브레이크가 있어야 탈 수 있어요.",
              ("바퀴", SA),
              ("빠진 세 부품", "위치 인코딩, FFN, 인과 마스킹"),
              ("완성된 자전거", TRF))],
     [points("배리어 3개와 고치는 부품",
             f"배리어 1, 순서를 모른다 -> {PE}",
             f"배리어 2, 자리마다의 비선형 변환이 없다 -> {FFN}",
             f"배리어 3, 미래를 볼 수 있다 -> {CM}"),
      points("슬라이드 영어와 우리말 뜻",
             "Three Things Are Still Missing = 아직 세 가지가 빠졌다",
             "not a layer you can stack = 쌓을 수 있는 층이 아니다",
             "No notion of order = 순서 개념이 없다",
             "No elementwise nonlinearity = 칸마다의 비선형성이 없다",
             "It can peek at the future = 미래를 훔쳐볼 수 있다",
             "Barrier to fix, this is the whole design of the Transformer block = 배리어와 그 해결이 곧 트랜스포머 블록의 설계다"),
      compare("배리어와 부품 짝 맞추기",
              ["배리어", "무엇이 문제인가", "고치는 부품"],
              ["1. 순서 없음", "순서를 바꿔도 결과가 그대로 따라감", PE],
              ["2. 비선형 없음", "어텐션 층을 쌓아도 결국 선형 변환", FFN],
              ["3. 미래 훔쳐보기", "언어 모델 과제가 너무 쉬워져 버림", CM])],
     [formula("배리어 1 을 식으로",
              r"\mathrm{SelfAttn}(PX) = P\,\mathrm{SelfAttn}(X)",
              [(r"X", "토큰들을 쌓은 입력 행렬"),
               (r"P", "순서를 뒤섞는 연산(순열)"),
               (r"\mathrm{SelfAttn}(PX)", "먼저 섞고 나서 셀프 어텐션"),
               (r"P\,\mathrm{SelfAttn}(X)", "먼저 셀프 어텐션하고 나서 섞기")],
              f"두 결과가 같아요. 이 성질을 {PEQ}이라고 해요. 곧 순서를 전혀 모른다는 뜻이에요."),
      steps("순열 등변성을 숫자로 확인해요",
            ["토큰 3개짜리 입력 X 를 아무거나 하나 잡아요",
             "1번과 2번 토큰의 자리를 바꾸는 순열 P 를 준비해요",
             "먼저 자리를 바꾸고 셀프 어텐션을 해 봐요",
             "이번에는 셀프 어텐션을 먼저 하고 자리를 바꿔 봐요",
             "두 결과가 소수점까지 똑같아요"],
            "셀프 어텐션은 누가 먼저 왔는지를 전혀 모릅니다. 그래서 위치 인코딩이 필요해요.",
            "임의의 X 와 순열 P"),
      look("슬라이드를 짚어 읽어요",
           (0.05, 0.19, 0.90, 0.07, "맨 위 한 줄: 셀프 어텐션만으로는 쌓을 수 있는 층이 아니고 구조적 빈틈이 셋 있다."),
           (0.07, 0.32, 0.27, 0.33, "왼쪽 상자: 1. 순서 개념이 없다. 해결은 positional encoding."),
           (0.36, 0.32, 0.27, 0.33, "가운데 상자: 2. 칸마다 비선형이 없다. 해결은 position-wise feed-forward net."),
           (0.65, 0.32, 0.28, 0.33, "오른쪽 상자: 3. 미래를 볼 수 있다. 해결은 causal masking."),
           (0.18, 0.68, 0.64, 0.11, "아래 큰 식 SelfAttn(PX) = P SelfAttn(X) 가 배리어 1 의 증거예요.")),
      prof("교수님: 이 셀프 어텐션 여기까지만으로는 완벽한 트랜스포머 레이어가 아직 아니에요.",
           "교수님: 이 배리어 3개를 기억해 봅시다.",
           "교수님: 순서 정보 때문에 포지셔널 인코딩, 토큰별 비선형 변환 때문에 포지션 와이즈 피드 포워드, 미래 정보 차단 때문에 커즐 마스킹.",
           "교수님: 이 3개의 팬시한 방법을 추가해서 트랜스포머가 되는 거죠.")],
     [check("셀프 어텐션의 배리어 2 를 고치는 부품은?",
            [PE, FFN, CM, MHA], 1,
            f"비선형이 없다는 문제는 {FFN}이 막아요. {RELU} 가 그 안에 들어 있어요."),
      exam("N4 Check Yourself",
           "Q5 (Part 2). Name the three barriers of plain self-attention and the component that fixes each.",
           "맨 셀프 어텐션의 배리어 세 가지와 각각을 고치는 부품을 말해 보세요.",
           ["1. 순서를 모른다 -> 위치 인코딩(positional encoding)",
            "2. 칸마다 비선형이 없다 -> 위치별 FFN(position-wise feed-forward network)",
            "3. 미래를 볼 수 있다 -> 인과 마스킹(causal masking)",
            "이 셋을 더한 것이 트랜스포머 블록의 기본 뼈대예요"],
           "순서, 비선형, 미래. 그리고 위치 인코딩, FFN, 마스킹."),
      english("시험 답안 문장",
              "맨 셀프 어텐션은 순서 정보가 없고, 칸별 비선형이 없으며, 미래 토큰을 볼 수 있다. 각각 위치 인코딩, 위치별 FFN, 인과 마스킹으로 해결한다.",
              "배리어 세 개와 부품 세 개를 짝지어 한 문장으로 쓰면 만점이에요.",
              "순-비-미, 위-피-마 로 외워요."),
      warn("헷갈리기 쉬운 점",
           f"{PEQ}은 순서를 무시한다는 뜻이 아니라, 순서를 바꾸면 결과도 똑같이 따라 바뀐다는 뜻이에요. 결국 순서를 구별하지 못한다는 말이에요.",
           f"배리어 3 은 {LM}을 학습할 때의 문제예요. 인코더는 오히려 앞뒤를 다 봐도 괜찮아요.")])

# ---------------------------------------------------------------- p.40
page(40, "배리어 1: 위치 인코딩", ["Positional Encoding", "Sinusoidal Positional Encoding", "Embedding",
                           "Self-Attention", "Permutation Equivariance", "Token"],
     [say("dog bites man 과 man bites dog 는 단어가 똑같아요. 순서만 달라요.",
          f"그런데 {SA}은 순서를 몰라서 둘을 구별하지 못해요.",
          f"그래서 자리마다 벡터 하나를 만들어 {EMB} 에 더해 줘요. 그게 {PE}이에요.",
          "원래 논문은 sin 과 cos 파도로 그 벡터를 만들었어요."),
      analogy("같은 옷에 번호표 달기",
              "체육대회에서 똑같은 체육복을 입은 학생이 둘이면 누가 누군지 몰라요. 가슴에 1번, 3번 번호표를 붙이면 구별이 돼요.",
              ("똑같은 체육복", "같은 단어의 임베딩"),
              ("번호표", PE),
              ("붙인 뒤의 모습", "위치가 섞인 입력 벡터"))],
     [points("슬라이드 영어와 우리말 뜻",
             "dog bites man vs man bites dog = 개가 사람을 문다 vs 사람이 개를 문다",
             "Give every position a vector = 모든 자리에 벡터를 하나씩 준다",
             "add it to the token embedding before the first layer = 첫 층에 들어가기 전에 토큰 임베딩에 더한다",
             "Now identical words at different positions differ = 이제 같은 단어라도 자리가 다르면 달라진다",
             "sinusoids of geometrically spaced frequencies = 주파수가 기하적으로 벌어지는 사인 파도들",
             "Order is not in the mechanism, so we put it in the input = 순서가 기계 안에 없으니 입력에 넣는다"),
      compare("위치 인코딩을 넣기 전과 후",
              ["상황", "dog 가 1번 자리", "dog 가 3번 자리"],
              ["넣기 전", "같은 벡터", "같은 벡터"],
              ["넣은 후", "임베딩 + 1번 자리 벡터", "임베딩 + 3번 자리 벡터"])],
     [formula("사인 코사인 위치 인코딩",
              r"PE_{pos,\,2i} = \sin\!\left(\frac{pos}{10000^{2i/d}}\right), \quad PE_{pos,\,2i+1} = \cos\!\left(\frac{pos}{10000^{2i/d}}\right)",
              [(r"pos", "몇 번째 자리인지 (0, 1, 2, ...)"),
               (r"i", "벡터의 몇 번째 칸 쌍인지"),
               (r"d", "임베딩의 전체 칸 수"),
               (r"10000^{2i/d}", "칸마다 파도의 길이를 다르게 만드는 값"),
               (r"\sin", "짝수 칸에는 사인"),
               (r"\cos", "홀수 칸에는 코사인")],
              f"칸마다 파장이 다른 파도를 배치해서 자리마다 고유한 무늬를 만들어요. 이게 {SPE}이에요."),
      steps("위치 벡터를 직접 계산해 봐요 (d = 4)",
            ["d = 4 이면 칸이 네 개, 쌍은 두 개(i = 0, 1) 예요",
             "i = 0 이면 분모가 10000의 0제곱 = 1 이라 각도가 곧 pos 예요",
             "i = 1 이면 분모가 10000의 0.5제곱 = 100 이라 각도가 pos / 100 이에요",
             "자리 0: sin(0) = 0, cos(0) = 1, sin(0) = 0, cos(0) = 1 이라 (0, 1, 0, 1) 이에요",
             "자리 1: sin(1) = 0.8415, cos(1) = 0.5403, sin(0.01) = 0.01, cos(0.01) = 1.0",
             "자리 2: sin(2) = 0.9093, cos(2) = -0.4161, sin(0.02) = 0.02, cos(0.02) = 0.9998"],
            "자리마다 값이 다르니, 같은 dog 여도 1번 자리와 3번 자리의 입력이 달라져요.",
            "pos = 0, 1, 2 이고 d = 4"),
      figure("같은 단어, 다른 자리", FIG_PE, "dog 임베딩에 자리 벡터를 더하면 값이 달라져요.", 4),
      look("슬라이드를 짚어 읽어요",
           (0.05, 0.19, 0.90, 0.05, "첫 점: dog bites man 과 man bites dog 의 대비."),
           (0.05, 0.25, 0.90, 0.06, "둘째 점: 자리마다 벡터를 주고 첫 층 전에 임베딩에 더한다."),
           (0.05, 0.31, 0.90, 0.05, "셋째 점: 원래 선택은 주파수가 다른 사인 파도들이었다."),
           (0.21, 0.36, 0.28, 0.32, "왼쪽 히트맵: 가로가 칸, 세로가 자리예요. 자리마다 무늬가 달라요."),
           (0.50, 0.36, 0.28, 0.32, "오른쪽 그래프: 칸마다 파장이 다른 세 파도를 보여 줘요."),
           (0.20, 0.72, 0.58, 0.12, "파란 상자 안의 두 식이 외워야 할 위치 인코딩 공식이에요.")),
      prof("교수님: 위치 인코딩이 없으면 각 토큰이 몇 번째 위치에 있는지 알려 주는 장치가 없어요.",
           "교수님: 각 위치마다 서로 다른 포지션 벡터를 만들어서 단어 벡터에 더해 주는 거예요.",
           "교수님: 사인 코사인을 쓴 장점은 추가 학습 파라미터가 없다는 거예요.",
           "교수님: 사인 코사인 성질 때문에 두 위치 사이의 상대적인 거리 정보도 모델이 쉽게 활용할 수 있죠."),
      bg("기초 다지기 4단원", "10000의 0제곱은 1 이에요. 어떤 수든 0제곱은 1 이에요.",
         "sin 과 cos 은 -1 과 1 사이를 오가는 물결 모양 함수예요.")],
     [check("위치 인코딩은 언제 더해지나요?",
            ["첫 층에 들어가기 전, 토큰 임베딩에", "소프트맥스 다음에",
             "마지막 층 출력에", "밸류에만"], 0,
            f"입력 {EMB} 에 더해서 첫 층으로 보내요. 그래야 모든 층이 순서를 알 수 있어요."),
      english("시험 답안 문장",
              "셀프 어텐션은 순열 등변성 때문에 순서를 구별하지 못하므로, 자리마다 다른 위치 벡터를 만들어 토큰 임베딩에 더한다. 원래 논문은 파장이 다른 sin 과 cos 을 썼다.",
              "왜 필요한지, 어떻게 넣는지, 무엇으로 만드는지 세 조각을 다 적어요.",
              "순서는 기계 안에 없으니 입력에 넣는다, 이 한 줄이 요약이에요."),
      warn("헷갈리기 쉬운 점",
           "위치 인코딩은 이어 붙이는(concat) 게 아니라 더하는(add) 거예요.",
           f"{SPE}은 학습하지 않아요. 파라미터가 0 개예요.")])

# ---------------------------------------------------------------- p.41
page(41, "어떤 위치 인코딩을 쓸까요", ["Positional Encoding", "Sinusoidal Positional Encoding", "RoPE",
                             "BERT", "GPT", "Large Language Model (LLM)", "Query", "Key", "Parameter"],
     [say(f"{PE}을 만드는 방법이 크게 세 가지예요.",
          "고정된 sin 과 cos, 자리마다 학습하는 벡터, 그리고 회전 방식이에요.",
          f"요즘 {LLM} 은 거의 다 세 번째인 {ROPE} 를 써요.",
          "이번 주 범위는 첫 번째예요."),
      analogy("주소를 적는 세 가지 방법",
              "집 위치를 알려 줄 때 고정된 좌표를 쓰거나, 동네마다 붙인 번호를 외우거나, 여기서 몇 걸음 떨어졌는지를 말할 수 있어요.",
              ("고정 좌표", SPE),
              ("동네마다 붙인 번호", "학습하는 절대 위치 임베딩"),
              ("몇 걸음 떨어졌는지", ROPE))],
     [points("슬라이드 영어와 우리말 뜻",
             "Three families, and the field has largely converged on the third = 세 갈래가 있고 학계는 대체로 세 번째로 모였다",
             "Modern LLMs use RoPE = 요즘 대규모 언어 모델은 RoPE 를 쓴다",
             "it rotates q and k by an angle proportional to position = 위치에 비례한 각도로 q 와 k 를 회전시킨다",
             "the attention score depends only on the relative offset i minus j = 어텐션 점수가 상대 거리 i - j 에만 의존한다",
             "That is what lets context windows stretch = 그래서 문맥 창을 길게 늘일 수 있다"),
      compare("세 가지 위치 인코딩",
              ["방법", "무엇인가", "성질", "쓰는 곳"],
              ["Sinusoidal", "고정된 sin, cos 파도", "학습 파라미터가 아예 없음", "원래 트랜스포머"],
              ["Learned absolute", "자리마다 학습하는 벡터 하나", "학습 때 정한 길이를 넘지 못함", "BERT, GPT-2"],
              ["Relative / RoPE", "위치에 비례한 각도로 q, k 회전", "학습 길이를 훨씬 넘어서도 잘 됨", "T5, LLaMA, 대부분의 LLM"])],
     [look("슬라이드를 짚어 읽어요",
           (0.05, 0.19, 0.90, 0.05, "첫 점: 세 갈래가 있고 학계는 세 번째로 모였다."),
           (0.05, 0.25, 0.90, 0.07, "둘째 점: RoPE 는 q 와 k 를 위치에 비례해 회전시켜 상대 거리에만 의존하게 만든다."),
           (0.07, 0.42, 0.86, 0.05, "표 머리글: method, what it is, property, used by."),
           (0.07, 0.50, 0.86, 0.06, "첫 줄 Sinusoidal: 고정된 sin, cos 이고 파라미터가 아예 없어요."),
           (0.07, 0.59, 0.86, 0.06, "둘째 줄 Learned absolute: 자리마다 학습 벡터. 학습 길이를 넘지 못해요."),
           (0.07, 0.68, 0.86, 0.07, "셋째 줄 Relative / RoPE: 회전 방식. 학습 길이 밖으로도 잘 늘어나요.")),
      prof("교수님: 세 번째가 릴레이티브 포지션 계열이고 요새 현대 모델이에요. 제가 회사에 있을 때 가장 많이 했던 연구가 이거예요.",
           "교수님: 포지션 벡터를 임베딩에 더하는 대신 회전의 개념을 도입시키는 거예요.",
           "교수님: 회전시키면 q_i 와 k_j 의 내적에 상대적 거리 i - j 가 자연스럽게 들어가요.",
           "교수님: 요새 대부분의 LLM 은 그냥 RoPE 쓴다고 보시면 되겠습니다. 다만 이번 주까지는 첫 번째 사인 코사인 방식을 볼 거예요."),
      bg("기초 다지기 1단원", "벡터를 회전시킨다는 것은 화살표의 방향을 각도만큼 돌리는 것이에요.",
         "길이는 그대로 두고 방향만 바꾸기 때문에 크기가 변하지 않아요.")],
     [check("학습 파라미터가 하나도 없는 위치 인코딩은?",
            [SPE, "학습하는 절대 위치 임베딩", ROPE, "인과 마스킹"], 0,
            f"{SPE}은 식으로 값을 바로 계산하기 때문에 배울 것이 없어요."),
      english("시험 답안 문장",
              "사인 코사인 위치 인코딩은 파라미터가 없고, 학습형 절대 위치 임베딩은 학습한 길이를 넘지 못하며, RoPE 는 쿼리와 키를 위치에 비례해 회전시켜 상대 거리만으로 점수를 정하므로 긴 문맥으로 잘 늘어난다.",
              "세 가지를 한 문장에 성질과 함께 적어요.",
              "파라미터 없음 / 길이에 묶임 / 길이 밖으로 늘어남, 세 낱말이면 표가 다 떠올라요."),
      warn("헷갈리기 쉬운 점",
           f"{BERT} 와 {GPT} 는 사인 코사인이 아니라 학습형 절대 위치를 썼어요.",
           f"{ROPE} 는 더하기가 아니라 회전이에요. 더하는 방식과 구조가 달라요.")])

# ---------------------------------------------------------------- p.42
page(42, "배리어 2: 피드포워드 층", ["Position-wise Feed-Forward Network (FFN)", "Nonlinearity", "ReLU",
                            "Multi-Layer Perceptron (MLP)", "Parameter", "Attention", "Self-Attention", "Token"],
     [say(f"{SA} 뒤에 자리마다 똑같은 작은 신경망을 붙여요. 그게 {FFN}이에요.",
          f"같은 2층짜리 {MLP} 를 각 자리에 따로 적용해요. 자리끼리 섞이지 않아요.",
          f"역할 분담이에요. {ATT}은 정보를 옮기고, FFN 은 각 토큰을 가공해요.",
          "파라미터가 가장 많이 사는 곳이기도 해요."),
      analogy("택배와 공장",
              "택배가 물건을 이 집 저 집 옮겨 주고, 공장은 각 집에서 받은 재료를 가공해 새 물건을 만들어요.",
              ("택배", ATT),
              ("집집마다 있는 같은 공장", FFN),
              ("가공된 물건", "그 자리의 새 표현"))],
     [points("슬라이드 영어와 우리말 뜻",
             "Apply the same two-layer MLP to every position independently = 같은 2층 MLP 를 모든 자리에 따로 적용한다",
             "No mixing across positions happens here = 여기서는 자리끼리 섞이지 않는다",
             "Division of labour = 역할 분담",
             "attention moves information between tokens = 어텐션은 토큰 사이에서 정보를 옮긴다",
             "the FFN transforms each token = FFN 은 각 토큰을 변환한다",
             "It is also where most of the parameters live = 파라미터 대부분이 여기 산다",
             "d_ff is usually 4d = 가운데 차원은 보통 4d 이다"),
      compare("어텐션과 FFN 의 역할 분담",
              ["부품", "하는 일", "자리끼리 섞이나"],
              [ATT, "토큰 사이에서 정보를 옮겨요", "섞여요"],
              [FFN, f"각 토큰을 {MLP} 로 혼자서 가공해요", "안 섞여요"])],
     [formula("FFN 식",
              r"\mathrm{FFN}(x) = \max(0,\, xW_1 + b_1)W_2 + b_2, \quad W_1 \in \mathbb{R}^{d \times 4d}",
              [(r"x", "한 자리의 벡터 하나"),
               (r"W_1", "칸 수를 d 에서 4d 로 늘리는 행렬"),
               (r"\max(0, \cdot)", f"음수는 0 으로 만드는 {RELU}"),
               (r"W_2", f"다시 4d 에서 d 로 줄이는 행렬. 둘이 합쳐 {MLP} 한 개예요"),
               (r"b_1, b_2", "편향 항(bias term)")],
              f"넓혔다 좁히는 사다리꼴이에요. 가운데의 max(0, ...) 가 {NL}을 만들어요."),
      steps("파라미터 수를 세어 봐요 (d = 512)",
            ["d = 512 이면 d_ff = 4d = 2048 이에요",
             "W1 은 512 곱하기 2048 = 1,048,576 개예요",
             "W2 는 2048 곱하기 512 = 1,048,576 개예요",
             "둘을 더하면 2,097,152 개이고, 이는 8 곱하기 512의 제곱과 같아요",
             "어텐션의 W^Q, W^K, W^V, W^O 는 각각 512 x 512 라서 4 곱하기 512의 제곱 = 1,048,576 개예요",
             "그러니까 FFN 이 어텐션 쪽보다 파라미터가 두 배예요"],
            "FFN 이 8d 제곱, 어텐션 투영이 4d 제곱. 파라미터 대부분이 FFN 에 살아요.",
            "d = 512, d_ff = 2048"),
      figure("어텐션은 옮기고, FFN 은 가공해요", FIG_FFN, "네 자리에 똑같은 FFN 을 따로 적용해요.", 4),
      look("슬라이드를 짚어 읽어요",
           (0.05, 0.19, 0.90, 0.05, "첫 점: 같은 2층 MLP 를 자리마다 독립으로 적용하고, 여기서는 자리끼리 안 섞인다."),
           (0.05, 0.25, 0.90, 0.07, "둘째 점: 역할 분담과 d_ff 가 보통 4d 라는 사실."),
           (0.23, 0.39, 0.53, 0.07, "위쪽 파란 상자 h1 ... h4 가 FFN 을 지난 결과예요."),
           (0.23, 0.49, 0.53, 0.07, "가운데 보라 상자 네 개가 FFN 인데 shared weights 라고 적혀 있어요."),
           (0.23, 0.59, 0.53, 0.07, "아래 회색 상자 x1 ... x4 가 입력이에요."),
           (0.14, 0.72, 0.72, 0.09, "아래 큰 식이 FFN(x) = max(0, xW1 + b1)W2 + b2 예요.")),
      prof("교수님: 어텐션은 토큰과 토큰 사이에 정보를 주고받는 역할이고, FFN 은 모아 온 정보를 각 토큰에서 더 복잡하게 가공해 주는 역할이에요.",
           "교수님: 논리니어가 없다면 레이어를 깊게 쌓아 봤자 사실 큰 의미가 없는 거죠.",
           "교수님: d_ff 를 보통 4d 정도로 확장했다가 다시 줄이는 사다리꼴 FFN 을 써요.",
           "교수님: 두 행렬 합치면 8d 제곱이고 셀프 어텐션의 프로젝션들이 4d 제곱이니, 트랜스포머에서 FFN 이 차지하는 게 굉장히 커요."),
      bg("기초 다지기 9단원", f"{RELU} 는 음수를 0 으로 만들고 양수는 그대로 두는 함수예요.",
         "이런 구부러짐이 없으면 층을 몇 개 쌓아도 결국 직선 한 번과 같아요.")],
     [check("트랜스포머에서 파라미터가 가장 많이 있는 곳은?",
            ["어텐션 투영 행렬", FFN, "위치 인코딩", "층 정규화"], 1,
            "FFN 이 8d 제곱, 어텐션 투영이 4d 제곱이라 FFN 쪽이 두 배예요."),
      exam("N4 Check Yourself",
           "Q4 (Part 2). Where do most of a Transformer's parameters live, in attention or in the feed-forward layers?",
           "트랜스포머의 파라미터는 대부분 어디에 있나요, 어텐션인가요 피드포워드인가요?",
           ["어텐션의 W^Q, W^K, W^V, W^O 는 각각 d x d 라서 합이 4d 제곱이에요",
            "FFN 은 d x 4d 와 4d x d 두 개라서 합이 8d 제곱이에요",
            "8d 제곱이 4d 제곱의 두 배예요"],
           "피드포워드 쪽이에요. FFN 이 어텐션 투영의 약 두 배를 차지해요."),
      english("시험 답안 문장",
              "위치별 FFN 은 자리마다 동일한 2층 MLP 를 독립적으로 적용해 비선형 변환을 더하며, 가운데 차원이 4d 라서 트랜스포머 파라미터의 대부분을 차지한다.",
              "독립 적용, 비선형, 4d, 파라미터 대부분의 네 조각을 넣어요.",
              "어텐션은 통신, FFN 은 계산. 이 대비로 기억해요."),
      warn("헷갈리기 쉬운 점",
           "자리마다 따로 적용한다고 해서 가중치가 자리마다 다른 게 아니에요. 가중치는 하나를 함께 써요.",
           f"{FFN} 은 자리끼리 정보를 섞지 않아요. 섞는 일은 {ATT} 담당이에요.")])

# ---------------------------------------------------------------- p.43
page(43, "배리어 3: 미래 가리기", ["Causal Masking", "Autoregressive", "Language Model (LM)", "Softmax",
                           "Attention Score", "Attention Weight", "Encoder", "Decoder", "BERT", "GPT",
                           "Next Token Prediction"],
     [say(f"{AR} 방식 {LM}은 아직 만들지 않은 토큰을 보면 안 돼요. 보면 너무 쉬워져요.",
          f"그래서 미래 자리의 {ASC}를 {SMX} 전에 마이너스 무한으로 바꿔요.",
          "exp(마이너스 무한)이 0 이라서 그 칸의 가중치가 정확히 0 이 돼요.",
          f"{ENC}는 이 마스크를 쓰지 않고 앞뒤를 다 봐요."),
      analogy("시험지 뒷면 가리기",
              "시험을 보는데 답이 적힌 뒷면이 비쳐 보이면 실력이 늘지 않아요. 검은 종이로 덮어 버리면 앞면만 보고 풀게 돼요.",
              ("비쳐 보이는 답", "미래 토큰"),
              ("검은 종이로 덮기", CM),
              ("앞면만 보고 풀기", NTP))],
     [points("슬라이드 영어와 우리말 뜻",
             "A language model must not attend to tokens it has not produced yet = 언어 모델은 아직 만들지 않은 토큰에 주목하면 안 된다",
             "otherwise the task is trivial and the model learns nothing = 그러지 않으면 과제가 시시해지고 모델이 아무것도 배우지 못한다",
             "Set the scores for future positions to minus infinity before the softmax = 소프트맥스 전에 미래 자리의 점수를 마이너스 무한으로 둔다",
             "so those weights become exactly zero = 그래서 그 가중치가 정확히 0 이 된다",
             "Encoders skip this and look both ways = 인코더는 이걸 건너뛰고 양쪽을 본다",
             "One triangular mask separates BERT-style from GPT-style models = 삼각형 마스크 하나가 BERT 계열과 GPT 계열을 가른다"),
      compare("마스크를 쓰는 쪽과 안 쓰는 쪽",
              ["구분", "인코더 방식", "디코더 방식"],
              ["마스크", "안 써요", "인과 마스크를 써요"],
              ["보는 범위", "앞뒤 전부", "자기 자신과 과거만"],
              ["푸는 과제", "빈칸 맞히기", NTP],
              ["대표 모델", BERT, GPT])],
     [formula("마스크를 식으로",
              r"e_{ij} = \frac{q_i^{\top} k_j}{\sqrt{d_k}}\ (j \le i), \qquad e_{ij} = -\infty\ (j > i)",
              [(r"i", "지금 보고 있는 자리(쿼리 쪽)"),
               (r"j", "쳐다보는 대상 자리(키 쪽)"),
               (r"j \le i", "과거와 자기 자신은 그대로 둬요"),
               (r"j > i", "미래는 마이너스 무한으로 바꿔요"),
               (r"-\infty", "exp 를 씌우면 0 이 되는 값")],
              f"{SMX} 전에 바꿔야 해요. 뒤에 바꾸면 합이 1 이 아니게 돼요."),
      steps("마스크를 손으로 씌워 봐요",
            ["토큰 3개짜리 점수 표를 (2, 1, 0 / 1, 2, 1 / 0, 1, 2) 라고 해요",
             "1번 줄은 자기 자신만 봐요. 2번, 3번 칸을 마이너스 무한으로 바꿔요",
             "1번 줄 소프트맥스는 (1.0, 0, 0) 이에요. 볼 게 하나뿐이니까요",
             "2번 줄은 1번, 2번만 남겨요. 점수 (1, 2) 의 소프트맥스는 (0.2689, 0.7311) 이에요",
             "3번 줄은 다 볼 수 있어요. (0, 1, 2) 의 소프트맥스는 (0.0900, 0.2447, 0.6652) 예요",
             "모든 줄의 합이 정확히 1 이에요"],
            "아래 삼각형만 남고 위쪽은 전부 0 이에요. 그래서 삼각 마스크라고 불러요.",
            "3 x 3 점수 표"),
      figure("인과 마스킹: 오른쪽 위를 지워요", FIG_MASK, "아래 삼각형만 남기고 위는 차단해요.", 4),
      look("슬라이드를 짚어 읽어요",
           (0.05, 0.19, 0.90, 0.05, "첫 점: 언어 모델은 아직 만들지 않은 토큰을 보면 안 된다."),
           (0.05, 0.25, 0.90, 0.07, "둘째 점: 소프트맥스 전에 미래 점수를 마이너스 무한으로 둬서 가중치를 0 으로 만든다."),
           (0.23, 0.35, 0.19, 0.29, "왼쪽 표 Bidirectional (encoder): 칸이 꽉 차 있어요."),
           (0.50, 0.35, 0.19, 0.29, "오른쪽 표 Causal / masked (decoder): 오른쪽 위가 빗금이에요."),
           (0.69, 0.44, 0.12, 0.10, "오른쪽 설명: 소프트맥스 전에 점수를 마이너스 무한으로."),
           (0.18, 0.72, 0.64, 0.09, "아래 식이 j <= i 면 그대로, j > i 면 마이너스 무한이라는 뜻이에요.")),
      prof("교수님: 아무 조치도 취하지 않으면 현재 토큰이 자기보다 미래 토큰을 보고 정답 토큰까지 미리 봐 버린다는 거예요.",
           "교수님: 미래 j 가 i 보다 큰 어텐션 스코어는 마이너스 무한으로 바꿔 버립니다.",
           "교수님: 마이너스 무한은 exp 를 치면 거의 0 에 가까운 수이기 때문에 어텐션 웨이트가 0 이 된다.",
           "교수님: 0 이 된다는 건 그쪽 뒤에 있는 밸류를 전혀 보지 않게 된다는 거죠.")],
     [check("마스크는 언제 씌워야 하나요?",
            ["소프트맥스 전에", "소프트맥스 후에", "밸류를 곱한 뒤에", "순서는 상관없어요"], 0,
            f"{SMX} 후에 0 으로 만들면 남은 가중치들의 합이 1 이 아니게 돼요. 반드시 전에 해야 해요."),
      exam("N4 Check Yourself",
           "Q2 (Part 2). Why must the mask be applied before the softmax and not after?",
           "왜 마스크를 소프트맥스 전에 씌워야 하고 후에 씌우면 안 되나요?",
           ["소프트맥스는 남은 값들을 나눠서 합이 1 이 되게 만들어요",
            "전에 마이너스 무한을 넣으면 그 칸은 exp 가 0 이라 자연스럽게 빠지고, 나머지 합이 정확히 1 이에요",
            "후에 0 으로 지우면 이미 나눠 준 몫만큼이 사라져서 합이 1 보다 작아져요",
            "그러면 그 뒤의 가중합이 망가져요"],
           "소프트맥스 전에 넣어야 남은 가중치의 합이 정확히 1 이 되기 때문이에요."),
      english("시험 답안 문장",
              "인과 마스킹은 j 가 i 보다 큰 미래 자리의 점수를 소프트맥스 이전에 마이너스 무한으로 바꾸어, 소프트맥스 이후 그 가중치가 정확히 0 이 되게 한다.",
              "이전이라는 말과 정확히 0 이라는 말을 꼭 넣어요.",
              "삼각형 마스크, 아래만 남는다. 그림으로 외워요."),
      warn("헷갈리기 쉬운 점",
           "마스크는 0 을 곱하는 게 아니라 마이너스 무한을 더하는 것이에요.",
           f"자기 자신(j = i)은 볼 수 있어요. 가리는 것은 j > i 인 미래뿐이에요.",
           f"{AR} 생성에서만 필요해요. {NTP} 과제가 아니면 마스크를 안 써요.")])

# ---------------------------------------------------------------- p.44
page(44, "최소한의 블록", ["Transformer", "Self-Attention", "Positional Encoding",
                    "Position-wise Feed-Forward Network (FFN)", "Causal Masking", "Embedding",
                    "Multi-Head Attention (MHA)", "Residual Connection", "Layer Normalization (LayerNorm)"],
     [say("배리어 셋을 막았으니 이제 쌓을 수 있는 블록이 됐어요.",
          f"{EMB} 에 {PE}을 더하고, 마스크드 어텐션과 FFN 을 지나요.",
          "이 블록을 N 번 쌓으면 거의 트랜스포머예요.",
          "Part 4 에서 더할 셋은 깊게 쌓아도 학습되게 만드는 장치예요."),
      analogy("층층이 쌓는 케이크",
              "같은 모양의 케이크 시트를 몇 겹이든 똑같이 쌓을 수 있어요. 한 겹의 설계가 좋으면 몇 겹을 쌓아도 돼요.",
              ("케이크 시트 한 겹", "트랜스포머 블록 하나"),
              ("쌓은 겹 수", "N 개의 층"),
              ("시트 사이 크림", "잔차 연결과 층 정규화"))],
     [points("블록의 순서",
             f"1. 입력 {EMB}: 내용은 있지만 순서가 없어요",
             f"2. + {PE}: 배리어 1 을 고쳐요",
             f"3. 마스크드 {SA}: 배리어 3 을 고쳐요",
             f"4. 위치별 {FFN}: 배리어 2 를 고쳐요"),
      points("슬라이드 영어와 우리말 뜻",
             "Embeddings + positional encoding, masked self-attention, position-wise feed-forward = 임베딩에 위치 인코딩, 마스크드 셀프 어텐션, 위치별 피드포워드",
             "Stack it N times = N 번 쌓아라",
             "This already works = 이것만으로도 이미 동작한다",
             "What Part 4 adds is what makes it trainable at depth = Part 4 가 더하는 것은 깊이 쌓아도 학습되게 만드는 것이다",
             "Three barriers, three components, one stackable block = 배리어 셋, 부품 셋, 쌓을 수 있는 블록 하나"),
      points("이 블록이 결국 무엇이 되나요",
             f"이 블록을 아주 많이 쌓은 것이 {LLM} 이에요",
             f"교수님: 트랜스포머를 좀 크게 쌓으면 그게 {LLM} 이다 이렇게 보셔도 된다",
             "GPT 도 BERT 도 이 블록의 변형이에요")],
     [figure("최소 블록 쌓기", FIG_BLOCK, "아래에서 위로 임베딩, 위치 인코딩, 마스크드 셀프 어텐션, FFN 이에요.", 4),
      look("슬라이드를 짚어 읽어요",
           (0.05, 0.19, 0.90, 0.05, "첫 점: 임베딩에 위치 인코딩, 마스크드 셀프 어텐션, 위치별 피드포워드를 N 번 쌓아라."),
           (0.05, 0.25, 0.90, 0.05, "둘째 점: 이것만으로 이미 동작하고, Part 4 는 깊이를 견디게 만든다."),
           (0.19, 0.40, 0.36, 0.08, "맨 위 보라 상자 Position-wise feed-forward 가 배리어 2 를 고쳐요."),
           (0.19, 0.50, 0.36, 0.08, "주황 상자 Masked self-attention 이 배리어 3 을 고쳐요."),
           (0.19, 0.60, 0.36, 0.08, "파란 상자 + Positional encoding 이 배리어 1 을 고쳐요."),
           (0.19, 0.70, 0.36, 0.08, "맨 아래 회색 상자 Input embeddings 는 내용만 있고 순서가 없어요.")),
      prof("교수님: 인베딩의 위치를 모르기 때문에 포지셔널 인코딩을 더해 주고, 배리어 1 을 픽스해 줬죠.",
           "교수님: 각 토큰이 자신이 볼 수 있는 다른 토큰들의 정보를 가져와서 문맥이 반영된 새로운 표현으로 바꿔 주죠.",
           "교수님: 중간에 마스크로 미래의 토큰을 보지 않는 배리어 3 을 해결하고요.",
           "교수님: 여기까지가 트랜스포머의 기본 뼈대예요. 이렇게만 해도 트랜스포머라고 할 수 있어요."),
      steps("다음 쪽 미리 보기",
            ["Part 4 에서 세 가지를 더해요",
             f"{MHA}: 전체 차원 d 를 헤드 h 개로 나눠서 여러 관점으로 봐요. d = 512, h = 8 이면 헤드마다 64 칸이에요",
             f"{RES}: 층의 입력을 출력에 그대로 더해서 지름길을 만들어요",
             f"{LN}: 한 토큰의 숫자들을 평균 0, 분산 1 로 맞춰 줘요"],
            "이 셋은 성능과 학습 안정성을 위한 장치예요. 기본 뼈대는 이미 완성됐어요.")],
     [check("최소 블록에서 배리어 1(순서 없음)을 고치는 자리는 어디인가요?",
            ["입력 임베딩 바로 다음", "셀프 어텐션 다음", "FFN 다음", "블록 맨 위"], 0,
            f"{PE}은 첫 층에 들어가기 전, 곧 임베딩 바로 다음에 더해요."),
      english("시험 답안 문장",
              "최소 트랜스포머 블록은 입력 임베딩에 위치 인코딩을 더하고, 마스크드 셀프 어텐션을 지나, 위치별 피드포워드를 지나는 구조이며, 이를 N 번 쌓는다.",
              "네 칸을 아래에서 위로 순서대로 쓰면 돼요.",
              "임베딩 - 위치 - 어텐션 - FFN, 네 칸을 손으로 그려 보며 외워요."),
      warn("헷갈리기 쉬운 점",
           f"{PE}은 블록마다 더하는 게 아니라 맨 처음 한 번만 더해요.",
           f"{MHA} 가 없어도 동작은 해요. 다만 깊게 쌓으면 학습이 안 돼요.")])

# ---------------------------------------------------------------- p.45
page(45, "Part 4 표지: The Transformer", ["Transformer", "Multi-Head Attention (MHA)",
                                      "Residual Connection", "Layer Normalization (LayerNorm)"],
     [say("네 번째 부분 표지예요. 제목은 4 The Transformer 예요.",
          f"작은 글씨는 multi-head attention, residuals, LayerNorm, the full stack 이에요.",
          f"{MHA}, {RES}, {LN}, 그리고 전체 구조를 본다는 뜻이에요.")],
     [points("영어 부제의 뜻",
             f"multi-head attention = {MHA}",
             f"residuals = {RES}",
             f"LayerNorm = {LN}",
             "the full stack = 전체를 쌓아 올린 모습"),
      prof("교수님: 여기에 멀티 헤드 어텐션이랑 레지듀얼 커넥션 그리고 레이어 놈, 이렇게 3개의 팬시한 방법을 더 추가해서 배워 보도록 할게요.",
           "교수님: 이건 성능을 높이기 위한 방법이라고 보시면 돼요.",
           "교수님: 트랜스포머를 좀 크게 쌓으면 그게 LLM 이다 이렇게 보셔도 된다.")],
     [], [])

data = {"deck": "N4", "from": 31, "to": 45,
        "glossary": [{"ko": k, "en": e, "say": s, "more": m} for k, e, s, m in GLOSSARY],
        "slides": S}

raw = json.dumps(data, ensure_ascii=False, indent=1)
for ch in ("—", "–", "·", "・"):
    assert ch not in raw, ch
with open(OUT, "w", encoding="utf-8") as f:
    f.write(raw)
print("saved", OUT, len(S), "pages")
