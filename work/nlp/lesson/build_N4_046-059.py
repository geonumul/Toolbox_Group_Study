# -*- coding: utf-8 -*-
"""4강(N4) Attention and the Transformer Architecture 회독 레슨 46~59쪽 생성기.
사용: python build_N4_046-059.py   출력: N4_046-059.json
4장 The Transformer: 멀티 헤드, 잔차 연결, LayerNorm, Pre-LN/Post-LN,
인코더/디코더 블록, 크로스 어텐션, 전체 구조, 이차 비용, WMT 결과,
왜 이겼나, Check Yourself Part 2, 마무리.
손계산은 아래에서 실제로 계산해 assert 로 확인한다."""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "N4_046-059.json")


# ---------------- 손계산 확인 (assert) ----------------

# p.46 슬라이드의 예문 토큰
SENT = ["The", "chef", "who", "ran", "to", "the", "store", "was", "tired"]
assert len(SENT) == 9
assert SENT[7] == "was" and SENT[1] == "chef" and SENT[6] == "store"

# p.47, p.48 원 논문 숫자: d = 512, h = 8, 헤드마다 d/h = 64
d_model = 512
h = 8
d_head = d_model // h
assert d_head == 64
assert d_head * h == d_model

# 헤드 하나의 W^Q 는 (d, d/h) 짜리 표
per_head_wq = d_model * d_head
assert per_head_wq == 32768

# 멀티 헤드의 Q, K, V 프로젝션 전체
mha_qkv = 3 * h * per_head_wq
assert mha_qkv == 786432

# 폭이 d 인 싱글 헤드 하나의 Q, K, V 프로젝션
single_qkv = 3 * d_model * d_model
assert single_qkv == 786432
assert mha_qkv == single_qkv          # 완전히 같아요

# 출력 프로젝션 W^O 와 멀티 헤드 전체
w_o = d_model * d_model
assert w_o == 262144
mha_total = mha_qkv + w_o
assert mha_total == 1048576
assert mha_total == 4 * d_model * d_model
assert round(mha_total / 10000) == 105   # 약 105만 개

# p.58 4번: FFN 의 파라미터 (d_ff = 4d)
d_ff = 4 * d_model
assert d_ff == 2048
ffn_total = d_model * d_ff + d_ff * d_model
assert ffn_total == 2097152
assert round(ffn_total / 10000) == 210   # 약 210만 개
assert ffn_total == 2 * mha_total        # FFN 이 어텐션의 정확히 두 배

# p.49 잔차 연결: 기울기가 곱해져 내려가는 모습
f_prime = 0.5
L10 = 10
without_res = f_prime ** L10
assert round(without_res, 7) == 0.0009766
assert abs(without_res - 1 / 1024) < 1e-15
deep96 = f_prime ** 96
assert deep96 < 1e-28
with_res10 = (1 + f_prime) ** L10
assert round(with_res10, 2) == 57.67
assert 1.0 ** 96 == 1.0                  # 항등 경로만 따라가면 1 이에요

# p.50 LayerNorm 손계산
xs = [2.0, 4.0, 4.0, 10.0]
mu = sum(xs) / len(xs)
assert mu == 5.0
var = sum((x - mu) ** 2 for x in xs) / len(xs)
assert var == 9.0
sd = math.sqrt(var)
assert sd == 3.0
z = [(x - mu) / sd for x in xs]
assert [round(v, 3) for v in z] == [-1.0, -0.333, -0.333, 1.667]
assert abs(sum(z)) < 1e-12
assert abs(sum(v * v for v in z) / len(z) - 1.0) < 1e-12
gamma, beta = 2.0, 1.0
y_ln = [gamma * v + beta for v in z]
assert [round(v, 3) for v in y_ln] == [-1.0, 0.333, 0.333, 4.333]

# p.55 이차 비용
n1, n2 = 512, 128000
assert n1 * n1 == 262144
assert n2 * n2 == 16384000000
assert n2 // n1 == 250
assert (n2 // n1) ** 2 == 62500
assert (n2 * n2) // (n1 * n1) == 62500
# RNN 은 n 에 비례, 셀프 어텐션은 n 제곱에 비례
rnn_work = n1 * d_model
att_work = n1 * n1 * d_model
assert rnn_work == 262144
assert att_work == 134217728
assert att_work // rnn_work == 512

# p.56 WMT 2014 영어 -> 독일어 결과 (슬라이드 막대 값)
bleu = [("GNMT (RNN)", 24.6), ("ConvSeq2Seq (CNN)", 25.2),
        ("Transformer base", 27.3), ("Transformer big", 28.4)]
cost = [("GNMT (RNN)", 96), ("ConvSeq2Seq (CNN)", 175),
        ("Transformer base", 3.3), ("Transformer big", 8.3)]
assert len(bleu) == 4 and len(cost) == 4
assert round(28.4 - 24.6, 1) == 3.8
assert round(96 / 3.3, 1) == 29.1
assert round(175 / 8.3, 1) == 21.1
assert round(96 / 8.3, 1) == 11.6
assert max(v for _, v in bleu) == 28.4
assert min(v for _, v in cost) == 3.3

# p.57 네 가지 성질
props = ["Parallelism", "Short paths", "Scales cleanly", "Task-agnostic"]
assert len(props) == 4

# p.58 Check Yourself Part 2 는 여섯 문제
assert len([1, 2, 3, 4, 5, 6]) == 6

# p.52 서브층 수: 인코더 블록 2개, 디코더 블록 3개
assert 2 + 1 == 3

# 깊이: BERT 12층, 슬라이드가 말한 96층
assert 12 * 8 == 96


# ---------------- 용어 표기 ----------------
MHA = "**멀티 헤드 어텐션(Multi-Head Attention (MHA))**"
HEAD = "**헤드(Head)**"
RES = "**잔차 연결(Residual Connection)**"
LN = "**LayerNorm(층 정규화)**"
IDP = "**항등 경로(Identity Path)**"
QC = "**이차 비용(Quadratic Cost)**"
CA = "**크로스 어텐션(Cross-Attention)**"
SA = "**셀프 어텐션(Self-Attention)**"
TRF = "**트랜스포머(Transformer)**"
ENC = "**인코더(Encoder)**"
DEC = "**디코더(Decoder)**"
QRY = "**쿼리(Query)**"
KEY = "**키(Key)**"
VAL = "**밸류(Value)**"
SDPA = "**스케일드 닷프로덕트 어텐션(Scaled Dot-Product Attention)**"
PE = "**위치 인코딩(Positional Encoding)**"
FFN = "**FFN(위치별 피드포워드 신경망)**"
CM = "**인과 마스킹(Causal Masking)**"
PEQ = "**순열 등변성(Permutation Equivariance)**"
SMX = "**소프트맥스(Softmax)**"
ATT = "**어텐션(Attention)**"
ASC = "**어텐션 점수(Attention Score)**"
AW = "**어텐션 가중치(Attention Weight)**"
WSUM = "**가중합(Weighted Sum)**"
DP = "**내적(Dot Product)**"
CTX = "**문맥 벡터(Context Vector)**"
IB = "**정보 병목(Information Bottleneck)**"
GRAD = "**기울기(Gradient)**"
VG = "**기울기 소실(Vanishing Gradient)**"
EG = "**기울기 폭발(Exploding Gradient)**"
JAC = "**야코비안(Jacobian)**"
PARAM = "**파라미터(Parameter)**"
PAR = "**병렬화(Parallelization)**"
RNN = "**RNN(순환 신경망)**"
LSTM = "**LSTM(장단기 메모리)**"
CNN = "**CNN(합성곱 신경망)**"
MT = "**기계 번역(Machine Translation (MT))**"
BLEU = "**BLEU(블루 점수)**"
LLM = "**LLM(대규모 언어 모델)**"
BERT = "**BERT(버트)**"
GPT = "**GPT(지피티)**"
EMB = "**임베딩(Embedding)**"
TOK = "**토큰(Token)**"
LR = "**학습률(Learning Rate)**"
HS = "**은닉 상태(Hidden State)**"
S2S = "**시퀀스-투-시퀀스 모델(Sequence-to-Sequence Model)**"
PRE = "**사전 학습(Pre-training)**"

WHEN2 = "4주차 월요일 2교시"

GLOSSARY = [
    ("멀티 헤드 어텐션", "Multi-Head Attention (MHA)",
     "어텐션 하나를 h 개로 쪼개서 서로 다른 관점으로 동시에 보는 것",
     "각 헤드는 d/h 차원에서 따로 어텐션을 하고, 결과를 옆으로 이어 붙인 뒤 W^O 로 섞어요."),
    ("헤드", "Head", "어텐션을 한 번 보는 행위 하나",
     "헤드마다 자기만의 W^Q, W^K, W^V 를 가져서 문법, 가까운 문맥처럼 서로 다른 것을 봐요."),
    ("잔차 연결", "Residual Connection", "서브층의 입력을 출력에 그대로 더해 주는 지름길",
     "층은 전체를 배우지 않고 '얼마나 바꿀지' 만 배우면 돼요. 깊게 쌓을 때 가장 중요한 장치예요."),
    ("층 정규화", "Layer Normalization (LayerNorm)",
     "토큰 하나의 숫자들을 평균 0, 분산 1 로 맞춘 뒤 감마와 베타로 다시 늘리기",
     "배치나 다른 토큰과 섞지 않아서 학습 때와 추론 때가 똑같이 동작해요."),
    ("항등 경로", "Identity Path", "아무 계산도 하지 않고 그대로 지나가는 길",
     "야코비안이 I + 함수의 미분이 되어서, 기울기가 곱해져도 1 이 남아요."),
    ("이차 비용", "Quadratic Cost", "길이가 2배면 일이 4배가 되는 비용",
     "셀프 어텐션은 n x n 점수 표를 만들기 때문에 계산과 메모리가 n 의 제곱으로 커져요."),
    ("크로스 어텐션", "Cross-Attention", "쿼리는 디코더에서, 키와 밸류는 인코더에서 가져오는 어텐션",
     "2015년 어텐션을 Q/K/V 표기로 다시 쓴 것이에요. 인코더와 디코더를 이어 줘요."),
    ("셀프 어텐션", "Self-Attention", "한 문장이 자기 자신을 바라보는 어텐션",
     "쿼리, 키, 밸류가 모두 같은 시퀀스에서 나와요. 모든 위치를 한꺼번에 계산해요."),
    ("트랜스포머", "Transformer", "어텐션만으로 만든 요즘 언어 모델의 기본 블록",
     "셀프 어텐션에 멀티 헤드, 잔차 연결, LayerNorm 을 더해 깊게 쌓을 수 있게 만든 구조예요."),
    ("인코더", "Encoder", "입력 문장을 끝까지 읽어 자리마다 은닉 상태를 남기는 쪽",
     "트랜스포머 인코더 블록은 마스크가 없어서 양방향으로 문장 전체를 봐요."),
    ("디코더", "Decoder", "요약을 받아 답 문장을 한 토큰씩 만들어 내는 쪽",
     "트랜스포머 디코더 블록에는 마스킹된 셀프 어텐션과 크로스 어텐션이 더 들어가요."),
    ("쿼리", "Query", "지금 내가 무엇을 찾고 있는지를 담은 벡터",
     "크로스 어텐션에서는 디코더 쪽에서 나와요. 쿼리가 바뀌면 어디를 볼지가 바뀌어요."),
    ("키", "Key", "나는 이런 정보를 갖고 있다고 광고하는 검색용 이름표 벡터",
     "쿼리와 키를 비교해서 점수를 만들어요. 크로스 어텐션에서는 인코더 쪽에서 나와요."),
    ("밸류", "Value", "내가 선택되면 실제로 건네줄 내용 벡터",
     "가중합에 들어가는 것은 키가 아니라 밸류예요. 키와 짝을 이뤄 같은 쪽에서 나와요."),
    ("스케일드 닷프로덕트 어텐션", "Scaled Dot-Product Attention",
     "내적으로 점수를 내고 루트 d_k 로 나눈 뒤 소프트맥스를 씌우는 어텐션",
     "루트 d_k 로 나누지 않으면 점수가 너무 커져서 소프트맥스가 거의 원-핫이 돼요."),
    ("위치 인코딩", "Positional Encoding", "몇 번째 자리인지를 알려 주는 숫자를 더해 주는 것",
     "셀프 어텐션은 순서를 모르기 때문에 필요해요. 원 논문은 사인과 코사인 함수를 썼어요."),
    ("위치별 피드포워드 신경망", "Position-wise Feed-Forward Network (FFN)",
     "토큰 하나하나에 똑같이 적용하는 작은 2층 신경망",
     "속 차원을 4d 로 넓혔다 다시 줄여요. 트랜스포머 파라미터의 대부분이 여기에 있어요."),
    ("인과 마스킹", "Causal Masking", "아직 나오지 않은 뒤쪽 토큰을 못 보게 가리기",
     "소프트맥스를 씌우기 전에 점수를 음의 무한대로 바꿔서 가중치가 0 이 되게 해요."),
    ("순열 등변성", "Permutation Equivariance", "토큰 순서를 섞어도 결과가 그대로 따라 섞이는 성질",
     "셀프 어텐션이 순서를 모른다는 뜻이에요. 그래서 위치 인코딩이 필요해요."),
    ("소프트맥스", "Softmax", "점수를 모두 더해 1 이 되는 확률 파이로 나누기",
     "각 점수에 exp 를 씌운 뒤 전체 합으로 나눠요. 2주차부터 계속 나왔어요."),
    ("어텐션", "Attention", "필요한 곳을 골라 보는 장치. 점수를 매기고 가중 평균을 내요",
     "점수, 소프트맥스, 가중합, 예측의 네 단계로 기억해요."),
    ("어텐션 점수", "Attention Score", "두 자리가 얼마나 관련 있는지 나타낸 날것 숫자",
     "쿼리와 키의 내적으로 구해요. 합이 1 이 아니라서 그대로는 가중치로 못 써요."),
    ("어텐션 가중치", "Attention Weight", "어텐션 분포의 각 칸 값. 그 자리를 얼마나 볼지 정해요",
     "모두 0 이상이고 다 더하면 1 이에요. 헤드마다 다른 가중치가 나와요."),
    ("가중합", "Weighted Sum", "값마다 가중치를 곱해서 모두 더한 것",
     "가중치의 합이 1 이면 가중 평균이에요. 어텐션의 세 번째 단계예요."),
    ("내적", "Dot Product", "두 화살표가 얼마나 같은 쪽을 보는지 재는 곱셈",
     "같은 자리끼리 곱해서 모두 더해요. 어텐션 점수를 만드는 방법이에요."),
    ("문맥 벡터", "Context Vector", "이번 단계에 필요한 만큼만 뽑아 만든 요약 벡터",
     "밸류들의 가중 평균이에요. 크로스 어텐션에서도 똑같이 만들어져요."),
    ("정보 병목", "Information Bottleneck", "입력 전체가 고정 크기 벡터 하나를 지나가야 해서 생기는 막힘",
     "어텐션이 이 병목을 없앴어요. 1장에서 본 seq2seq 의 가장 큰 약점이에요."),
    ("기울기", "Gradient", "손실이 가장 빨리 커지는 방향과 그 가파름",
     "잔차 연결은 기울기가 지나갈 고속도로를 하나 깔아 줘요."),
    ("기울기 소실", "Vanishing Gradient", "귓속말 전달 게임처럼 기울기가 점점 희미해져 0 에 가까워지는 문제",
     "층을 깊게 쌓을수록 심해져요. 잔차 연결이 이것을 막아 줘요."),
    ("기울기 폭발", "Exploding Gradient", "기울기가 곱해지다 너무 커져서 학습이 터지는 문제",
     "기울기 소실의 반대쪽 문제예요. 잔차 연결과 LayerNorm 이 함께 잡아 줘요."),
    ("야코비안", "Jacobian", "벡터를 벡터로 보내는 함수의 미분을 표로 적은 것",
     "잔차 연결이 있으면 야코비안이 I + 함수의 미분 모양이 돼요. 3주차에 나왔어요."),
    ("파라미터", "Parameter", "학습하면서 값이 바뀌는 모델 속의 숫자들",
     "가중치 행렬과 편향 항이 다 파라미터예요. 개수를 세면 모델 크기가 나와요."),
    ("병렬화", "Parallelization", "여러 계산을 한꺼번에 동시에 하기",
     "트랜스포머가 이긴 첫 번째 이유예요. 모든 위치를 한 번의 행렬 곱으로 처리해요."),
    ("순환 신경망", "Recurrent Neural Network (RNN)", "한 단어씩 읽으며 메모장에 요약을 고쳐 쓰는 신경망",
     "순서대로 계산해야 해서 병렬화가 안 돼요. 트랜스포머에는 더 이상 없어요."),
    ("장단기 메모리", "LSTM", "게이트를 달아 기억을 오래 들고 가게 만든 RNN",
     "트랜스포머가 나오기 전까지 가장 강한 시퀀스 모델이었어요."),
    ("합성곱 신경망", "Convolutional Neural Network (CNN)", "작은 필터를 훑으며 무늬를 찾아내는 신경망",
     "헤드를 CNN 의 필터 여러 개에 비유할 수 있어요. WMT 비교 표에도 나와요."),
    ("기계 번역", "Machine Translation (MT)", "한 언어 문장을 다른 언어 문장으로 바꾸는 과제",
     "트랜스포머는 원래 기계 번역을 위해 2017년에 나왔어요."),
    ("블루 점수", "BLEU", "번역문이 사람 번역과 n-gram 이 얼마나 겹치는지 재는 점수",
     "높을수록 좋아요. WMT 2014 영어 독일어에서 트랜스포머가 28.4 를 냈어요."),
    ("대규모 언어 모델", "Large Language Model (LLM)", "트랜스포머 블록을 아주 많이 쌓아 크게 학습한 언어 모델",
     "교수님 말로 '트랜스포머를 좀 크게 쌓으면 그게 LLM' 이에요."),
    ("버트", "BERT", "인코더 블록만 12층 쌓아 만든 사전 학습 모델",
     "헤드가 실제로 무엇을 배우는지도 BERT 로 많이 연구됐어요."),
    ("지피티", "GPT", "디코더 블록만 쌓아 다음 토큰을 예측하게 만든 모델",
     "트랜스포머 블록이 그대로 쓰여요. 5주차에 배워요."),
    ("임베딩", "Embedding", "단어의 지도 좌표. 토큰 하나를 숫자 벡터로 바꾼 것",
     "트랜스포머의 맨 아래에서 위치 인코딩과 더해져요."),
    ("토큰", "Token", "글을 자른 가장 작은 조각 하나",
     "레고 조각이에요. 트랜스포머는 토큰 n 개를 한꺼번에 처리해요."),
    ("학습률", "Learning Rate", "한 걸음의 보폭",
     "Post-LN 은 처음에 보폭을 천천히 키우는 워밍업이 없으면 학습이 터져요."),
    ("시퀀스-투-시퀀스 모델", "Sequence-to-Sequence Model", "입력 문장을 읽고 출력 문장을 쓰는 큰 틀",
     "인코더와 디코더 두 부분으로 되어 있어요. 1장에서 배웠어요."),
    ("사전 학습", "Pre-training", "아주 많은 글로 미리 크게 학습해 두는 단계",
     "다음 주에 배워요. 블록은 그대로이고 학습 데이터만 커져요."),
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


def prof(*lines, when=WHEN2):
    return {"kind": "prof", "when": when, "lines": list(lines)}


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


# ---- p.46 한 헤드는 한 번에 한 곳만
FIG_ONEHEAD = SVG(
    TX(240, 20, "한 번의 가중 평균은 한 가지 질문이에요", "tb", 15),
    TX(60, 52, "질문 자리", "tm", 12),
    TX(150, 52, "chef", "tm", 12), TX(240, 52, "store", "tm", 12), TX(330, 52, "was", "tm", 12),
    TX(60, 86, "헤드 1개", "tb", 13, "start", 1),
    R(120, 72, 60, 20, "n", 1), R(210, 72, 60, 20, "n", 1), R(300, 72, 60, 20, "n2", 1),
    TX(400, 86, "한 줄만 있어요", "tm", 12, "middle", 1),
    L(20, 110, 460, 110, "e", 2),
    TX(60, 148, "헤드 A", "tb", 13, "start", 2),
    R(120, 134, 60, 20, "n2", 2), R(210, 134, 60, 20, "n", 2), R(300, 134, 60, 20, "n", 2),
    TX(410, 148, "문법을 봐요", "tm", 12, "middle", 2),
    TX(60, 184, "헤드 B", "tb", 13, "start", 3),
    R(120, 170, 60, 20, "n", 3), R(210, 170, 60, 20, "n3", 3), R(300, 170, 60, 20, "n3", 3),
    TX(410, 184, "가까운 문맥을 봐요", "tm", 12, "middle", 3),
    R(20, 212, 440, 30, "box2", 4),
    TX(240, 232, "한 단어는 동시에 여러 질문을 갖고 있어요", "tb", 14, "middle", 4),
)

# ---- p.47 멀티 헤드의 흐름
FIG_MHA = SVG(
    TX(240, 20, "쪼개고, 각자 보고, 이어 붙이고, 섞어요", "tb", 15),
    BOX(16, 108, 56, 40, "X", "n", "tl", 1),
    TX(44, 166, "n x 512", "tm", 11, "middle", 1),
    R(100, 44, 96, 34, "n3", 2), TX(148, 66, "W1 Q K V", "tl", 12, "middle", 2),
    R(100, 110, 96, 34, "n3", 2), TX(148, 132, "W2 Q K V", "tl", 12, "middle", 2),
    R(100, 176, 96, 34, "n3", 2), TX(148, 198, "W8 Q K V", "tl", 12, "middle", 2),
    A(74, 122, 96, 62, "e", 2), A(74, 128, 96, 128, "e", 2), A(74, 134, 96, 194, "e", 2),
    BOX(214, 44, 76, 34, "헤드 1", "n2", "tl", 3, 13),
    BOX(214, 110, 76, 34, "헤드 2", "n2", "tl", 3, 13),
    BOX(214, 176, 76, 34, "헤드 8", "n2", "tl", 3, 13),
    TX(252, 100, "n x 64", "tm", 11, "middle", 3),
    A(198, 61, 212, 61, "e", 3), A(198, 127, 212, 127, "e", 3), A(198, 193, 212, 193, "e", 3),
    BOX(316, 92, 60, 72, "concat", "n", "tl", 4, 13),
    A(292, 61, 314, 110, "e2", 4), A(292, 127, 314, 128, "e2", 4), A(292, 193, 314, 148, "e2", 4),
    BOX(396, 108, 60, 40, "W^O", "n4", "tl", 5, 14),
    A(378, 128, 394, 128, "e2", 5),
    TX(240, 246, "다시 n x 512 로 돌아와요. 계산량은 그대로예요", "tb", 14, "middle", 5),
)

# ---- p.49 잔차 연결
FIG_RES = SVG(
    TX(240, 20, "기울기에게 고속도로를 깔아 줘요", "tb", 15),
    TX(56, 66, "잔차 없음", "tb", 13, "start", 1),
    BOX(140, 48, 52, 30, "f1", "n", "tl", 1, 13),
    BOX(212, 48, 52, 30, "f2", "n", "tl", 1, 13),
    BOX(284, 48, 52, 30, "f3", "n", "tl", 1, 13),
    BOX(356, 48, 52, 30, "f4", "n", "tl", 1, 13),
    A(192, 63, 210, 63, "e", 1), A(264, 63, 282, 63, "e", 1), A(336, 63, 354, 63, "e", 1),
    TX(240, 96, "기울기가 네 상자를 모두 통과해야 해요", "tm", 12, "middle", 1),
    L(20, 112, 460, 112, "e", 2),
    TX(56, 162, "잔차 있음", "tb", 13, "start", 2),
    BOX(140, 144, 52, 30, "f1", "n2", "tl", 2, 13),
    BOX(212, 144, 52, 30, "f2", "n2", "tl", 2, 13),
    BOX(284, 144, 52, 30, "f3", "n2", "tl", 2, 13),
    BOX(356, 144, 52, 30, "f4", "n2", "tl", 2, 13),
    A(192, 159, 210, 159, "e", 2), A(264, 159, 282, 159, "e", 2), A(336, 159, 354, 159, "e", 2),
    A(140, 132, 264, 132, "e2", 3), A(284, 132, 408, 132, "e2", 3),
    TX(240, 196, "위로 건너뛰는 길이 따로 있어요", "t", 13, "middle", 3),
    R(20, 212, 440, 32, "box2", 4),
    TX(240, 233, "x(l) = x(l-1) + Sublayer(x(l-1))", "tb", 15, "middle", 4),
)

# ---- p.50 LayerNorm
FIG_LN = SVG(
    TX(120, 20, "정규화 전", "tb", 14),
    TX(360, 20, "정규화 후", "tb", 14),
    L(40, 140, 220, 140, "e", 1),
    R(50, 84, 22, 56, "n", 1), R(80, 56, 22, 84, "n", 1), R(110, 100, 22, 40, "n", 1),
    R(140, 68, 22, 72, "n", 1), R(170, 112, 22, 28, "n", 1), R(200, 44, 22, 96, "n", 1),
    TX(130, 160, "평균이 한쪽으로 치우쳤어요", "tm", 12, "middle", 1),
    A(232, 96, 258, 96, "e2", 2),
    L(280, 96, 460, 96, "e", 2),
    R(290, 70, 22, 26, "n2", 2), R(320, 56, 22, 40, "n2", 2), R(350, 96, 22, 22, "n2", 2),
    R(380, 66, 22, 30, "n2", 2), R(410, 96, 22, 34, "n2", 2), R(440, 50, 22, 46, "n2", 2),
    TX(370, 152, "평균 0, 분산 1 이 됐어요", "tm", 12, "middle", 2),
    R(20, 184, 440, 28, "box2", 3),
    TX(240, 203, "토큰 하나의 숫자들만 가지고 계산해요", "tb", 14, "middle", 3),
    TX(240, 236, "다른 토큰과도, 배치와도 섞지 않아요", "t", 13, "middle", 4),
    TX(240, 258, "그래서 학습 때와 추론 때가 똑같아요", "t", 13, "middle", 4),
)

# ---- p.51 Pre-LN 과 Post-LN
FIG_PRELN = SVG(
    TX(120, 22, "Post-LN (2017 원 논문)", "tb", 14),
    TX(360, 22, "Pre-LN (요즘 방식)", "tb", 14),
    BOX(76, 180, 100, 28, "서브층", "n3", "tl", 1, 13),
    TX(126, 232, "x", "tm", 13, "middle", 1),
    A(126, 226, 126, 210, "e", 1),
    BOX(76, 136, 100, 26, "더하기", "n", "tl", 1, 13),
    A(126, 178, 126, 164, "e", 1),
    L(40, 222, 40, 149, "e2", 2), A(40, 149, 74, 149, "e2", 2),
    BOX(76, 92, 100, 28, "LayerNorm", "n2", "tl", 2, 12),
    A(126, 134, 126, 122, "e", 2),
    TX(126, 74, "LN(x + f(x))", "tb", 13, "middle", 2),
    L(240, 40, 240, 250, "e", 3),
    BOX(316, 180, 100, 28, "LayerNorm", "n2", "tl", 3, 12),
    TX(366, 232, "x", "tm", 13, "middle", 3),
    A(366, 226, 366, 210, "e", 3),
    BOX(316, 136, 100, 28, "서브층", "n3", "tl", 3, 13),
    A(366, 178, 366, 166, "e", 3),
    BOX(316, 96, 100, 26, "더하기", "n", "tl", 4, 13),
    A(366, 134, 366, 124, "e", 4),
    L(286, 222, 286, 109, "e2", 4), A(286, 109, 314, 109, "e2", 4),
    TX(366, 74, "x + f(LN(x))", "tb", 13, "middle", 4),
)

# ---- p.52 인코더 블록과 디코더 블록
FIG_BLOCKS = SVG(
    TX(112, 20, "인코더 블록", "tb", 14),
    BOX(24, 178, 176, 26, "멀티 헤드 셀프 어텐션", "n2", "tl", 1, 12),
    BOX(24, 144, 176, 26, "Add and Norm", "n", "tl", 1, 12),
    BOX(24, 110, 176, 26, "피드포워드", "n3", "tl", 1, 12),
    BOX(24, 76, 176, 26, "Add and Norm", "n", "tl", 1, 12),
    TX(112, 220, "양방향. 원문 전체를 봐요", "tm", 12, "middle", 1),
    L(240, 34, 240, 250, "e", 2),
    TX(368, 20, "디코더 블록", "tb", 14),
    BOX(280, 212, 176, 24, "마스킹된 셀프 어텐션", "n2", "tl", 2, 12),
    BOX(280, 182, 176, 24, "Add and Norm", "n", "tl", 2, 12),
    BOX(280, 152, 176, 24, "크로스 어텐션", "n4", "tl", 3, 12),
    BOX(280, 122, 176, 24, "Add and Norm", "n", "tl", 3, 12),
    BOX(280, 92, 176, 24, "피드포워드", "n3", "tl", 3, 12),
    BOX(280, 62, 176, 24, "Add and Norm", "n", "tl", 3, 12),
    TX(368, 254, "인과적. 자기가 쓴 것까지만 봐요", "tm", 12, "middle", 4),
)

# ---- p.53 크로스 어텐션
FIG_CROSS = SVG(
    TX(240, 20, "쿼리는 디코더, 키와 밸류는 인코더", "tb", 15),
    BOX(20, 46, 180, 30, "인코더 출력 H", "box", "tb", 1, 13),
    TX(110, 92, "원문 문장 전체", "tm", 12, "middle", 1),
    BOX(280, 46, 180, 30, "디코더 상태 S", "box2", "tb", 1, 13),
    TX(370, 92, "지금까지 쓴 번역문", "tm", 12, "middle", 1),
    BOX(20, 108, 84, 28, "K = H W^K", "n3", "tl", 2, 12),
    BOX(116, 108, 84, 28, "V = H W^V", "n3", "tl", 2, 12),
    A(80, 78, 62, 106, "e", 2), A(140, 78, 158, 106, "e", 2),
    BOX(320, 108, 96, 28, "Q = S W^Q", "n2", "tl", 2, 12),
    A(370, 78, 368, 106, "e2", 2),
    BOX(120, 170, 240, 32, "Attention(Q, K, V)", "n4", "tl", 3, 14),
    A(62, 138, 170, 168, "e", 3), A(158, 138, 220, 168, "e", 3), A(368, 138, 310, 168, "e2", 3),
    TX(240, 232, "2장에서 배운 2015년 어텐션 그대로예요", "tb", 14, "middle", 4),
    TX(240, 256, "표기만 Q, K, V 로 바뀌었어요", "t", 13, "middle", 4),
)

# ---- p.54 전체 구조
FIG_FULL = SVG(
    TX(110, 18, "인코더 x N", "tb", 14),
    BOX(20, 208, 172, 24, "입력 임베딩 + 위치 인코딩", "n", "tl", 1, 11),
    BOX(20, 178, 172, 24, "멀티 헤드 셀프 어텐션", "n2", "tl", 1, 11),
    BOX(20, 148, 172, 24, "Add and Norm", "n", "tl", 1, 11),
    BOX(20, 118, 172, 24, "피드포워드", "n3", "tl", 1, 11),
    BOX(20, 88, 172, 24, "Add and Norm", "n", "tl", 1, 11),
    TX(110, 252, "원문 문장", "tm", 12, "middle", 1),
    TX(370, 18, "디코더 x N", "tb", 14),
    BOX(284, 208, 172, 24, "출력 임베딩 + 위치 인코딩", "n", "tl", 2, 11),
    BOX(284, 178, 172, 24, "마스킹된 셀프 어텐션", "n2", "tl", 2, 11),
    BOX(284, 148, 172, 24, "멀티 헤드 크로스 어텐션", "n4", "tl", 2, 11),
    BOX(284, 118, 172, 24, "피드포워드", "n3", "tl", 2, 11),
    BOX(284, 88, 172, 24, "Add and Norm", "n", "tl", 2, 11),
    TX(370, 252, "지금까지 쓴 번역문", "tm", 12, "middle", 2),
    A(194, 100, 282, 152, "e2", 3),
    TX(240, 126, "키와 밸류", "tm", 11, "middle", 3),
    BOX(284, 50, 172, 24, "Linear + Softmax", "box2", "tb", 4, 12),
    A(370, 86, 370, 76, "e", 4),
    TX(370, 38, "다음 토큰 확률", "tm", 12, "middle", 4),
)

# ---- p.55 이차 비용
FIG_QUAD = SVG(
    TX(240, 20, "길이가 2배면 점수 표는 4배예요", "tb", 15),
    TX(80, 48, "n = 2", "tb", 13),
    R(40, 60, 30, 30, "n2", 1), R(72, 60, 30, 30, "n2", 1),
    R(40, 92, 30, 30, "n2", 1), R(72, 92, 30, 30, "n2", 1),
    TX(72, 142, "칸 4개", "tm", 12, "middle", 1),
    TX(230, 48, "n = 4", "tb", 13, "middle", 2),
    R(166, 60, 30, 30, "n2", 2), R(198, 60, 30, 30, "n2", 2), R(230, 60, 30, 30, "n2", 2), R(262, 60, 30, 30, "n2", 2),
    R(166, 92, 30, 30, "n2", 2), R(198, 92, 30, 30, "n2", 2), R(230, 92, 30, 30, "n2", 2), R(262, 92, 30, 30, "n2", 2),
    R(166, 124, 30, 30, "n2", 2), R(198, 124, 30, 30, "n2", 2), R(230, 124, 30, 30, "n2", 2), R(262, 124, 30, 30, "n2", 2),
    R(166, 156, 30, 30, "n2", 2), R(198, 156, 30, 30, "n2", 2), R(230, 156, 30, 30, "n2", 2), R(262, 156, 30, 30, "n2", 2),
    TX(230, 206, "칸 16개", "tm", 12, "middle", 2),
    TX(390, 80, "길이 2배", "t", 13, "middle", 3),
    TX(390, 104, "칸 4배", "tb", 15, "middle", 3),
    R(320, 128, 140, 52, "box2", 3),
    TX(390, 150, "n = 512 이면 26만 칸", "t", 12, "middle", 3),
    TX(390, 170, "n = 128000 이면 164억 칸", "tb", 12, "middle", 3),
    TX(240, 238, "계산도 메모리도 n 의 제곱으로 늘어나요", "tb", 14, "middle", 4),
)

# ---- p.57 네 가지 성질
FIG_WHY = SVG(
    TX(240, 22, "트랜스포머가 이긴 네 가지 이유", "tb", 15),
    R(16, 48, 104, 90, "box2", 1),
    TX(68, 74, "병렬화", "tb", 14, "middle", 1),
    TX(68, 100, "모든 자리를", "t", 12, "middle", 1),
    TX(68, 118, "한꺼번에", "t", 12, "middle", 1),
    R(136, 48, 104, 90, "box2", 2),
    TX(188, 74, "짧은 경로", "tb", 14, "middle", 2),
    TX(188, 100, "어떤 두 토큰도", "t", 12, "middle", 2),
    TX(188, 118, "한 층에서 만나요", "t", 12, "middle", 2),
    R(256, 48, 104, 90, "box2", 3),
    TX(308, 74, "잘 쌓여요", "tb", 14, "middle", 3),
    TX(308, 100, "같은 블록을", "t", 12, "middle", 3),
    TX(308, 118, "12층, 96층", "t", 12, "middle", 3),
    R(376, 48, 104, 90, "box2", 4),
    TX(428, 74, "과제 무관", "tb", 14, "middle", 4),
    TX(428, 100, "글, 그림, 소리", "t", 12, "middle", 4),
    TX(428, 118, "같은 블록", "t", 12, "middle", 4),
    L(20, 162, 460, 162, "e", 5),
    TX(240, 190, "같은 블록이 BERT, GPT, ViT, AlphaFold 가 됐어요", "tb", 14, "middle", 5),
    TX(240, 222, "2017년에는 번역용이었는데", "t", 13, "middle", 5),
    TX(240, 244, "지금은 AI 거의 전부를 돌려요", "t", 13, "middle", 5),
)

# ---- p.59 오늘 배운 것 한 장
FIG_WRAP = SVG(
    TX(240, 20, "오늘 하루를 한 줄로 이으면", "tb", 15),
    BOX(16, 48, 104, 34, "seq2seq", "box", "tb", 1, 13),
    TX(68, 100, "벡터 하나가", "tm", 12, "middle", 1),
    TX(68, 118, "병목이에요", "tm", 12, "middle", 1),
    A(124, 65, 148, 65, "e2", 2),
    BOX(152, 48, 104, 34, "어텐션", "box", "tb", 2, 13),
    TX(204, 100, "점수 소프트맥스", "tm", 12, "middle", 2),
    TX(204, 118, "가중합", "tm", 12, "middle", 2),
    A(260, 65, 284, 65, "e2", 3),
    BOX(288, 48, 104, 34, "셀프 어텐션", "box", "tb", 3, 13),
    TX(340, 100, "Q K V 가 모두", "tm", 12, "middle", 3),
    TX(340, 118, "같은 문장에서", "tm", 12, "middle", 3),
    R(16, 150, 448, 44, "box2", 4),
    TX(240, 170, "트랜스포머 = 셀프 어텐션 + 멀티 헤드", "tb", 14, "middle", 4),
    TX(240, 188, "+ 잔차 연결 + LayerNorm", "tb", 14, "middle", 4),
    TX(240, 224, "값은 n 제곱 비용으로 치러요", "t", 13, "middle", 5),
    TX(240, 248, "다음 주는 사전 학습이에요", "tb", 14, "middle", 5),
)

S = []


def page(p, title, terms, p1, p2=(), p3=(), p4=()):
    S.append({"p": p, "title": title, "terms": list(terms),
              "pass1": list(p1), "pass2": list(p2), "pass3": list(p3), "pass4": list(p4)})


# ---------------------------------------------------------------- p.46
page(46, "헤드 하나로는 부족해요",
     ["Multi-Head Attention (MHA)", "Head", "Self-Attention", "Attention Weight",
      "Query", "Weighted Sum", "Attention", "Convolutional Neural Network (CNN)"],
     [say(f"4장 {TRF}가 시작됐어요. 여기서 성능을 올리는 장치 세 개를 더해요.",
          f"첫 번째가 {MHA}이에요.",
          f"{SA}을 한 번만 하면 한 가지 방향으로만 평균을 낼 수 있어요."),
      figure("한 헤드는 한 곳만 봐요", FIG_ONEHEAD,
             "빨간 줄은 헤드 하나. 아래 두 줄은 헤드를 나눠서 서로 다른 곳을 본 모습이에요.", 4),
      analogy("사진 한 장에 필터 여러 장",
              "같은 사진을 볼 때 어떤 필터는 윤곽선을 찾고, 어떤 필터는 색이 바뀌는 곳을 찾아요. 필터마다 역할이 달라요.",
              ("필터 한 장", "헤드 한 개"),
              ("윤곽선을 찾는 필터", "문법 관계를 보는 헤드"),
              ("색 변화를 찾는 필터", "가까운 문맥을 보는 헤드"))],
     [compare("슬라이드 영어와 우리말 뜻",
              ["영어 원문", "뜻"],
              ["One attention distribution can only average one way",
               "어텐션 분포 하나는 한 가지 방향으로만 평균을 낸다"],
              ["But a word usually needs several different things at once",
               "그런데 한 단어는 보통 여러 가지를 동시에 필요로 한다"],
              ["its syntactic subject, the nearby modifiers",
               "그 단어의 문법상 주어, 가까이 붙은 꾸밈말"],
              ["the coreferent pronoun, the topic of the paragraph",
               "같은 대상을 가리키는 대명사, 문단의 주제"],
              ["One head can only look in one place at a time",
               "헤드 하나는 한 번에 한 곳만 볼 수 있다"]),
      points("용어 하나씩",
             f"{HEAD}: {ATT}을 한 번 보는 행위 하나예요",
             f"{MHA}: 그 행위를 h 개로 나눠서 동시에 하는 것이에요",
             f"{AW}: 그 자리를 얼마나 볼지 정하는 0 이상의 숫자, 다 더하면 1 이에요"),
      check(f"{HEAD}가 하나뿐이면 무엇이 문제인가요",
            ["한 가지 방향으로만 평균을 낼 수 있어요", "계산이 너무 느려요",
             "문장이 짧아져요", "소프트맥스를 못 써요"], 0,
            "슬라이드 첫 줄이 바로 그 말이에요. One attention distribution can only average one way.")],
     [look("슬라이드를 짚어 읽어요",
           (0.06, 0.196, 0.80, 0.040, "첫 점: 어텐션 분포 하나는 한 방향으로만 평균을 낸다."),
           (0.06, 0.244, 0.80, 0.040, "둘째 점: 주어, 꾸밈말, 대명사, 문단 주제를 한꺼번에 필요로 한다."),
           (0.23, 0.354, 0.47, 0.038, "그림 제목: 헤드 하나는 한 번에 한 곳만 본다."),
           (0.09, 0.490, 0.84, 0.056, "single head 줄: 빨간 막대가 was 한 곳에만 서 있어요."),
           (0.09, 0.585, 0.84, 0.053, "head A: syntax 줄. 문법을 보는 헤드는 chef 에 서 있어요."),
           (0.09, 0.675, 0.84, 0.053, "head B: local 줄. 가까운 문맥을 보는 헤드는 store 와 was 에 서 있어요.")),
      points("예문을 한 번 읽어요",
             "The chef who ran to the store was tired, 토큰이 9개예요",
             f"지금 {QRY}는 여덟 번째 토큰 was 예요",
             "was 의 주어는 멀리 있는 chef 예요. 이건 문법 관계예요",
             "동시에 바로 앞 store 도 봐야 해요. 이건 가까운 문맥이에요",
             "한 줄짜리 가중치로는 두 가지를 동시에 못 해요"),
      prof("교수님: 헤드는 그야말로 어텐션을 보는 행위 하나라고 보시면 돼요.",
           "교수님: CNN 에서 컨볼루션 필터 하나하나가 하는 역할이 있잖아요. 헤드도 그런 필터 여러 개처럼 생각하세요.",
           "교수님: 헤드 A 는 문법 관계, 헤드 B 는 가까운 문맥, 헤드 C 는 의미를 보게 나눌 수 있어요."),
      bg("기초 다지기 6단원",
         f"{SMX}는 점수를 모두 더해 1 이 되는 확률로 바꿔 줘요.",
         f"그래서 {AW}는 언제나 한 줄에서 합이 1 이에요.",
         "합이 1 인 줄이 하나뿐이면, 한 곳을 크게 보면 다른 곳은 작아질 수밖에 없어요.")],
     [check("슬라이드의 예문에서 was 의 문법상 주어는 무엇인가요",
            ["chef", "store", "who", "tired"], 0,
            "The chef ... was tired 이니까 주어는 chef 예요. 그래서 head A: syntax 가 chef 를 봐요."),
      english("답안 문장",
              f"{ATT} 분포 하나는 한 가지 방향으로만 {WSUM}을 만들 수 있는데, 한 단어는 문법 관계와 가까운 문맥과 의미를 동시에 필요로 하므로 {HEAD}를 여러 개 둔다.",
              "한 문장으로 '왜 헤드가 여러 개인가' 를 설명할 수 있어야 해요.",
              "한 질문에 한 평균, 여러 질문에는 여러 헤드 로 외워요."),
      warn("헷갈리기 쉬운 점",
           f"{HEAD}가 여러 개라고 해서 {ATT}을 여러 번 반복하는 게 아니에요. 한 번에 나눠서 같이 해요.",
           f"{CNN}의 필터 비유는 이해를 돕는 비유예요. 계산 방식이 같다는 뜻은 아니에요.")])

# ---------------------------------------------------------------- p.47
page(47, "멀티 헤드 어텐션의 계산",
     ["Multi-Head Attention (MHA)", "Head", "Query", "Key", "Value", "Self-Attention",
      "Parameter", "Transformer", "Scaled Dot-Product Attention"],
     [say(f"{MHA}이 어떻게 계산되는지 그림으로 봐요.",
          "쪼개고, 각자 어텐션 하고, 옆으로 이어 붙이고, 마지막에 한 번 섞어요.",
          "네 단어로 split, attend, concatenate, project 예요."),
      figure("쪼개고 각자 보고 이어 붙여요", FIG_MHA,
             "같은 입력 X 를 헤드마다 자기 W^Q, W^K, W^V 로 줄여서 봐요. 결과를 이어 붙이고 W^O 로 섞어요.", 5),
      points("한 줄 요약",
             f"{MHA}은 {SA} 하나를 h 조각으로 나눈 것이에요",
             "원 논문은 d = 512, h = 8, 그래서 헤드마다 64차원이에요")],
     [compare("슬라이드 영어와 우리말 뜻",
              ["영어 원문", "뜻"],
              ["Project Q, K, V into h lower-dimensional subspaces",
               "Q, K, V 를 더 낮은 차원의 공간 h 개로 투영한다"],
              ["run attention in each independently",
               "각 공간에서 어텐션을 따로 돌린다"],
              ["concatenate, and project back",
               "옆으로 이어 붙이고, 다시 원래 차원으로 투영한다"],
              ["Original paper: d = 512, h = 8, so each head works in 64 dimensions",
               "원 논문은 d = 512, h = 8 이라 헤드마다 64차원에서 일한다"],
              ["h heads, each in d/h dimensions, then one shared output projection",
               "헤드 h 개, 각자 d/h 차원, 그다음 공유 출력 투영 하나"]),
      points("용어 하나씩",
             f"{QRY}: 내가 무엇을 찾는지 담은 벡터. X 에 W^Q 를 곱해 만들어요",
             f"{KEY}: 나는 이런 정보가 있다고 광고하는 이름표. X 에 W^K 를 곱해요",
             f"{VAL}: 뽑히면 실제로 건네줄 내용. X 에 W^V 를 곱해요",
             f"{PARAM}: 학습하면서 값이 바뀌는 숫자들. 여기서는 W^Q, W^K, W^V, W^O 예요"),
      steps("split, attend, concatenate, project 를 순서대로",
            ["입력 X 는 토큰 n 개가 각자 512칸을 가진 표예요",
             "헤드 i 는 자기만의 W^Q, W^K, W^V 로 X 를 64칸으로 줄여요",
             f"줄어든 64칸에서 {SDPA}을 그대로 해요",
             "헤드마다 n x 64 짜리 결과가 나와요",
             "8개를 옆으로 이어 붙이면 64 x 8 = 512, 원래 폭으로 돌아와요",
             "마지막에 W^O 를 곱해서 헤드들의 정보를 섞어 줘요"],
            "결과는 다시 n x 512. 겉모양은 셀프 어텐션 한 번과 똑같아요.",
            "d = 512, h = 8")],
     [look("슬라이드를 짚어 읽어요",
           (0.06, 0.197, 0.84, 0.036, "첫 점: Q, K, V 를 h 개의 낮은 차원 공간으로 투영해 따로 어텐션."),
           (0.06, 0.247, 0.50, 0.034, "둘째 점: 원 논문 d = 512, h = 8, 헤드마다 64차원."),
           (0.13, 0.485, 0.08, 0.078, "왼쪽 회색 상자가 입력 X 예요. n x d 라고 적혀 있어요."),
           (0.26, 0.370, 0.24, 0.290, "가운데 세 줄이 헤드마다의 W^Q, W^K, W^V 예요. 번호가 1, 2, 3."),
           (0.51, 0.367, 0.11, 0.297, "head 1, head 2, head 3 상자. 오른쪽 위에 each head: n x d/h."),
           (0.69, 0.449, 0.08, 0.146, "concat 상자에서 이어 붙이고, 그 오른쪽 진한 상자가 W^O 예요.")),
      formula("멀티 헤드 어텐션의 식",
              r"\mathrm{MultiHead}(X)=\mathrm{Concat}(\mathrm{head}_1,\dots,\mathrm{head}_h)\,W^{O}",
              [(r"X", "입력. 토큰 n 개가 각자 d 칸을 가진 표예요"),
               (r"\mathrm{head}_i", f"i 번째 {HEAD}의 결과. n x (d/h) 짜리예요"),
               (r"\mathrm{Concat}", "결과들을 옆으로 이어 붙이기. 폭이 다시 d 가 돼요"),
               (r"W^{O}", "마지막에 한 번 곱해서 헤드들의 정보를 섞어 주는 표"),
               (r"h", "헤드 개수. 원 논문은 8 이에요")],
              "헤드마다 따로 본 결과를 이어 붙이고 W^O 로 한 번 섞으면 멀티 헤드 어텐션이에요."),
      formula("헤드 하나의 식",
              r"\mathrm{head}_i=\mathrm{Attention}(XW_i^{Q},\,XW_i^{K},\,XW_i^{V}),\quad W_i^{Q}\in\mathbb{R}^{d\times d/h}",
              [(r"XW_i^{Q}", "헤드 i 의 쿼리. X 를 자기 W^Q 로 64칸까지 줄인 것"),
               (r"XW_i^{K}", "헤드 i 의 키. 같은 X 인데 다른 표를 곱해요"),
               (r"XW_i^{V}", "헤드 i 의 밸류"),
               (r"\mathbb{R}^{d\times d/h}", "W^Q 의 크기. 512줄 x 64칸 이라는 뜻이에요"),
               (r"i", "헤드 번호. 1부터 h 까지예요")],
              "헤드마다 다른 W 를 써서 같은 문장을 다른 각도로 봐요."),
      prof("교수님: 각 헤드는 X 를 보긴 보는데, 자기들만의 W^Q, W^K, W^V 로 자기만의 Q, K, V 를 만듭니다.",
           "교수님: 중요한 점은 각각의 헤드가 서로 다른 행렬을 쓴다는 거예요.",
           "교수님: 마지막 W^O 는 헤드들의 정보를 혼합해 주는 믹싱, 블렌딩 역할이라고 생각하세요."),
      bg("기초 다지기 3단원",
         "(n, 512) 짜리 표에 (512, 64) 짜리 표를 곱하면 (n, 64) 가 나와요.",
         "이어 붙이기는 표를 옆으로 붙여 칸 수를 늘리는 것이에요.",
         "64칸짜리 8개를 붙이면 512칸이 돼요. 숫자가 딱 맞아요."),
      points("실습과 이어지는 곳",
             "Lab 3 Part 4 에서 트랜스포머 블록을 직접 만들어요",
             f"Part 5 에서는 실제 {HEAD}들이 무엇을 보는지 그림으로 확인해요",
             "교수님이 수업에서 건너뛴 부분이라 혼자 복습하라고 했어요")],
     [check("d = 512, h = 8 일 때 헤드 하나가 다루는 차원은",
            ["64", "512", "8", "4096"], 0,
            "512 를 8 로 나눈 64 예요. 헤드 수를 늘리면 헤드마다의 차원은 줄어들어요."),
      check(f"{MHA}에서 마지막에 W^O 를 곱하는 이유는",
            ["이어 붙인 헤드들의 정보를 섞어 주려고", "차원을 8배로 늘리려고",
             "소프트맥스를 한 번 더 씌우려고", "마스킹을 하려고"], 0,
            "교수님 말: W^O 는 헤드들의 정보를 혼합해 주는 믹싱, 블렌딩 역할이에요."),
      english("답안 문장",
              f"{MHA}은 Q, K, V 를 h 개의 d/h 차원 공간에서 {ATT}한 뒤, 이어 붙이고 W^O 를 곱한다.",
              "split, attend, concatenate, project 네 단어를 그대로 문장으로 풀면 돼요.",
              "쪼개기, 각자 보기, 이어 붙이기, 섞기 로 외워요."),
      warn("헷갈리기 쉬운 점",
           f"{HEAD} 개수를 늘려도 전체 차원 d 는 그대로예요. d 를 h 배로 키우는 게 아니에요.",
           f"헤드마다 {QRY}, {KEY}, {VAL}를 만드는 표가 따로 있어요. 같은 표를 나눠 쓰는 게 아니에요.")])

# ---------------------------------------------------------------- p.48
page(48, "멀티 헤드는 공짜예요",
     ["Multi-Head Attention (MHA)", "Head", "Parameter", "Query", "Key", "Value",
      "BERT", "Self-Attention", "Position-wise Feed-Forward Network (FFN)"],
     [say(f"{MHA}의 가장 놀라운 점이에요.",
          "헤드를 8개로 늘려도 계산량과 파라미터 수가 전혀 늘지 않아요.",
          "차원을 나눠 쓰기 때문이에요. 서로 다른 관점 8개가 사실상 공짜예요."),
      analogis := analogy("한 시간을 나눠 쓰기",
                          "공부 한 시간을 한 과목에만 쓸 수도 있고, 8과목에 7분 30초씩 나눠 쓸 수도 있어요. 쓰는 시간 총합은 똑같아요.",
                          ("전체 한 시간", "전체 차원 d = 512"),
                          ("과목 하나", "헤드 하나"),
                          ("과목마다 7분 30초", "헤드마다 64차원")),
      points("한 줄 요약",
             f"{HEAD} 수 h 를 늘려도 총 {PARAM} 수는 그대로예요",
             "그래서 h > 1 을 쓸지 말지는 아무도 논쟁하지 않아요")],
     [compare("슬라이드 영어와 우리말 뜻",
              ["영어 원문", "뜻"],
              ["Because each head uses d/h dimensions",
               "각 헤드가 d/h 차원만 쓰기 때문에"],
              ["the total compute and the total parameter count are the same",
               "전체 계산량과 전체 파라미터 수가 똑같다"],
              ["as a single head of full width",
               "폭이 전부인 헤드 하나를 쓸 때와"],
              ["So h different views are, in effect, free",
               "그래서 h 개의 다른 관점이 사실상 공짜다"],
              ["Free capacity is rare in deep learning",
               "딥러닝에서 공짜로 얻는 능력은 드물다"]),
      points(f"{HEAD}들이 실제로 배우는 것 (슬라이드, BERT 연구)",
             "어떤 헤드는 바로 앞 토큰이나 바로 뒤 토큰을 따라가요",
             "어떤 헤드는 문법상 걸리는 관계를 따라가요",
             "어떤 헤드는 드물게 나오는 단어를 가리켜요",
             "놀랄 만큼 많은 헤드가 거의 아무것도 안 배워서 잘라내도 돼요"),
      check(f"{MHA}에서 h 를 8로 늘리면 계산량은",
            ["거의 그대로예요", "8배가 돼요", "64배가 돼요", "8분의 1이 돼요"], 0,
            "헤드마다 차원이 d/h 로 줄어들기 때문에 총합이 같아요.")],
     [look("슬라이드를 짚어 읽어요",
           (0.06, 0.197, 0.87, 0.071, "첫 점: 각 헤드가 d/h 차원을 쓰므로 전체 계산량과 파라미터 수가 같다."),
           (0.06, 0.285, 0.30, 0.032, "둘째 점: 그래서 h 개의 다른 관점은 사실상 공짜다."),
           (0.06, 0.332, 0.87, 0.067, "셋째 점: BERT 로 연구한 헤드들의 역할. 마지막은 잘라내도 되는 헤드."),
           (0.12, 0.607, 0.76, 0.070, "가운데 식: head_i = Attention(XW^Q, XW^K, XW^V), W^Q 는 d x d/h."),
           (0.26, 0.863, 0.48, 0.030, "맨 아래: 공짜로 얻는 능력은 드물다, 그래서 h > 1 은 논쟁거리가 아니다.")),
      steps("파라미터 수를 직접 세어 봐요 (싱글 헤드)",
            ["d = 512 인 헤드 하나를 쓴다고 해요",
             "W^Q 는 512줄 x 512칸이라 512 x 512 = 262144 개",
             "W^K, W^V 도 똑같이 262144 개씩",
             "셋을 더하면 3 x 262144 = 786432 개",
             "출력 표 W^O 도 512 x 512 = 262144 개",
             "전부 더하면 786432 + 262144 = 1048576 개"],
            "싱글 헤드 어텐션의 파라미터는 약 105만 개예요.",
            "d = 512"),
      steps("파라미터 수를 직접 세어 봐요 (헤드 8개)",
            ["헤드 하나의 W^Q 는 512줄 x 64칸이라 512 x 64 = 32768 개",
             "헤드 하나에 W^Q, W^K, W^V 가 있으니 3 x 32768 = 98304 개",
             "헤드가 8개니까 8 x 98304 = 786432 개",
             "싱글 헤드의 786432 와 정확히 같아요",
             "W^O 도 똑같이 512 x 512 = 262144 개",
             "합치면 786432 + 262144 = 1048576 개"],
            "헤드 8개도 약 105만 개. 싱글 헤드와 한 개도 다르지 않아요.",
            "d = 512, h = 8, d/h = 64"),
      prof("교수님: 512를 다 처리하는 게 아니라 8개 헤드가 각각 512 나누기 8 로 차원을 확 줄여서 계산합니다.",
           "교수님: 헤드를 여러 번 했다고 계산량이 더 많아지는 건 아니에요. 계산 수는 똑같다.",
           "교수님: 다만 헤드가 너무 많아지면 차원이 너무 줄어서 표현력이 약해져요. 4나 8 정도가 적당합니다."),
      bg("기초 다지기 3단원",
         "행렬의 파라미터 수는 줄 수 x 칸 수예요.",
         "512 x 64 = 32768 이고, 이것을 8번 더하면 512 x 512 = 262144 와 같아요.",
         "나눠서 여러 번 하나, 한 번에 크게 하나 숫자의 총합은 같아요.")],
     [check("헤드 8개짜리와 싱글 헤드의 파라미터 수를 비교하면",
            ["똑같아요", "헤드 8개가 8배 많아요", "헤드 8개가 8분의 1이에요", "헤드 8개가 2배 많아요"], 0,
            "둘 다 약 105만 개예요. 512 x 64 x 8 = 512 x 512 이기 때문이에요."),
      check(f"{BERT} 연구가 밝힌 {HEAD}들의 모습이 아닌 것은",
            ["모든 헤드가 똑같이 중요해요", "앞뒤 토큰을 따라가는 헤드가 있어요",
             "문법 관계를 따라가는 헤드가 있어요", "거의 안 배워서 잘라내도 되는 헤드가 많아요"], 0,
            "슬라이드는 반대로 말해요. 놀랄 만큼 많은 헤드가 거의 아무것도 안 배워요."),
      english("답안 문장",
              f"각 {HEAD}가 d/h 차원만 쓰기 때문에 h 개의 헤드를 써도 총 계산량과 총 {PARAM} 수가 폭 d 짜리 헤드 하나와 같아서, 서로 다른 관점을 사실상 공짜로 얻는다.",
              "d/h 로 나눠 쓴다는 점이 핵심이에요.",
              "나눠서 쓰니까 총합은 그대로 로 외워요."),
      warn("헷갈리기 쉬운 점",
           f"공짜인 것은 {PARAM} 수와 계산량이에요. {HEAD}를 늘리면 헤드 하나의 표현력은 줄어들어요.",
           f"이 쪽 파라미터 수는 {ATT} 부분만 센 거예요. {FFN}은 이보다 두 배 많아요.")])

# ---------------------------------------------------------------- p.49
page(49, "잔차 연결",
     ["Residual Connection", "Identity Path", "Gradient", "Vanishing Gradient",
      "Exploding Gradient", "Jacobian", "Transformer", "BERT", "Parameter"],
     [say(f"두 번째 장치는 {RES}이에요.",
          "서브층의 입력을 그 출력에 그냥 더해 줘요. 한 줄이면 끝나는 장치예요.",
          "그러면 층은 전체를 배울 필요가 없고 '얼마나 바꿀지' 만 배우면 돼요."),
      figure("기울기에게 고속도로를 깔아 줘요", FIG_RES,
             "위는 잔차가 없어서 기울기가 상자를 다 통과해야 해요. 아래는 건너뛰는 길이 따로 있어요.", 4),
      analogy("지도 위의 고속도로",
              "시내 길로만 가면 신호등마다 서느라 힘이 빠져요. 옆에 고속도로가 하나 있으면 멀리까지 그대로 갈 수 있어요.",
              ("신호등이 많은 시내 길", "서브층을 하나하나 지나가는 길"),
              ("옆에 난 고속도로", "항등 경로"),
              ("멀리까지 힘이 남아 있음", "1층까지 기울기가 살아서 도착함"))],
     [compare("슬라이드 영어와 우리말 뜻",
              ["영어 원문", "뜻"],
              ["Add the input of a sublayer to its output",
               "서브층의 입력을 그 출력에 더한다"],
              ["The layer then only has to learn the change",
               "그러면 층은 바뀌는 만큼만 배우면 된다"],
              ["not the whole mapping", "전체 대응 관계를 배우는 게 아니라"],
              ["The identity path makes the Jacobian I + df/dx",
               "항등 경로가 야코비안을 I + 함수의 미분으로 만든다"],
              ["the gradient reaches layer 1 even in a 96-layer stack",
               "96층을 쌓아도 기울기가 1층까지 닿는다"],
              ["Without this, deep Transformers simply do not train",
               "이것이 없으면 깊은 트랜스포머는 아예 학습되지 않는다"]),
      points("용어 하나씩",
             f"{RES}: 서브층의 입력을 출력에 그대로 더해 주는 지름길이에요",
             f"{IDP}: 아무 계산도 안 하고 그냥 지나가는 길이에요",
             f"{JAC}: 벡터를 벡터로 보내는 함수의 미분을 표로 적은 것이에요",
             f"{VG}: 기울기가 곱해지다 0 에 가까워지는 문제예요"),
      steps("무엇이 달라지는지 한 줄씩",
            ["원래는 서브층 하나를 지나면 x(l) = f(x(l-1)) 이에요",
             "잔차를 붙이면 x(l) = x(l-1) + f(x(l-1)) 이 돼요",
             "f 는 이제 '완성된 값' 이 아니라 '고칠 양' 만 만들면 돼요",
             "f 가 아무것도 안 해도 입력이 그대로 위로 올라가요",
             "그래서 층을 많이 쌓아도 최소한 망가지지는 않아요"],
            "잔차 연결은 x + f(x). 더하기 하나가 전부예요.")],
     [look("슬라이드를 짚어 읽어요",
           (0.06, 0.197, 0.80, 0.036, "첫 점: 서브층 입력을 출력에 더하면 층은 바뀌는 양만 배우면 된다."),
           (0.06, 0.243, 0.80, 0.070, "둘째 점: 항등 경로가 야코비안을 I + df/dx 로 만들어 96층에서도 학습된다."),
           (0.12, 0.440, 0.73, 0.053, "without residual 줄: f1 에서 f4 까지 한 줄로만 이어져 있어요."),
           (0.12, 0.513, 0.73, 0.044, "가운데 초록 곡선이 건너뛰는 잔차 경로예요."),
           (0.12, 0.561, 0.73, 0.056, "with residual 줄: 오른쪽 식이 x(l) = x(l-1) + f(x(l-1)) 이에요."),
           (0.14, 0.721, 0.72, 0.076, "큰 식: x(l) = x(l-1) + Sublayer(x(l-1)).")),
      formula("잔차 연결의 식",
              r"x_{\ell}=x_{\ell-1}+\mathrm{Sublayer}(x_{\ell-1})",
              [(r"x_{\ell-1}", "이 서브층에 들어온 값"),
               (r"\mathrm{Sublayer}", "셀프 어텐션이나 피드포워드 같은 서브층"),
               (r"+", "여기 이 더하기 하나가 잔차 연결의 전부예요"),
               (r"x_{\ell}", "서브층을 지난 뒤의 값")],
              "들어온 값을 그대로 더해 주니, 서브층은 고칠 양만 만들면 돼요."),
      steps("기울기가 얼마나 남는지 손으로 세어 봐요",
            ["층마다 미분이 0.5 라고 해 봐요. 곱해지면서 내려가요",
             "잔차가 없으면 10층을 지나면 0.5 를 열 번 곱해요",
             "0.5 의 10제곱 = 0.0009766, 1024분의 1 이에요",
             "96층이면 0.5 를 96번 곱해서 거의 0 이 돼요",
             "잔차가 있으면 층마다 1 + 0.5 = 1.5 가 돼요",
             "항등 경로만 따라가는 길은 1 을 96번 곱해도 그대로 1 이에요"],
            "잔차가 없으면 1024분의 1, 있으면 최소한 1 이 남아요. 기울기가 죽지 않아요.",
            "층마다 미분 0.5, 층 수 10과 96"),
      prof("교수님: 그레이디언트가 쭉 흐를 때 계속 쌓으면 베니싱하거나 익스플로딩 하는 경우가 있죠.",
           "교수님: 그래서 하이웨이 패스를 하나 그냥 해서 더해주는 거예요.",
           "교수님: 아이덴티티 경로를 통해 기울기가 직접 전달되는 통로가 있어서 훨씬 안정적입니다.",
           "교수님: BERT 는 12개의 레이어를 쌓는단 말이죠. 깊은 트랜스포머 학습이 편해진 게 잔차 연결이에요."),
      bg("기초 다지기 7단원",
         "연쇄 법칙은 맞물린 톱니바퀴예요. 층을 지날 때마다 미분이 곱해져요.",
         "1보다 작은 수를 계속 곱하면 0 으로 가고, 1보다 큰 수를 계속 곱하면 폭발해요.",
         f"더하기가 하나 있으면 미분에 1 이 남아서 {VG}과 {EG}을 둘 다 눌러 줘요.")],
     [check(f"{RES}이 없으면 깊은 {TRF}는",
            ["아예 학습이 안 돼요", "조금 느려질 뿐이에요", "파라미터가 늘어나요", "문장이 짧아져요"], 0,
            "슬라이드: Without this, deep Transformers simply do not train."),
      check(f"{RES}이 있을 때 {JAC}의 모양은",
            ["I + 함수의 미분", "함수의 미분만", "0", "함수의 미분의 제곱"], 0,
            "항등 경로 때문에 단위 행렬 I 가 더해져요. 그래서 기울기가 살아남아요."),
      exam("예상 문제",
           "잔차 연결이 깊은 신경망 학습에 도움이 되는 이유를 야코비안으로 설명하시오.",
           "왜 더하기 하나가 그렇게 중요한지 수식으로 설명해 보세요.",
           ["잔차가 없으면 x(l) = f(x(l-1)) 이라 야코비안은 함수의 미분 하나뿐이에요",
            "층을 지날 때마다 이 미분이 곱해져서 1보다 작으면 0 으로 사라져요",
            "잔차를 붙이면 x(l) = x(l-1) + f(x(l-1)) 이 돼요",
            "야코비안이 I + 함수의 미분이 되어서 항상 1 이 섞여 있어요",
            "그래서 96층을 쌓아도 기울기가 1층까지 닿아요"],
           "항등 경로가 야코비안에 I 를 더해 주어서 기울기 소실을 막아요."),
      english("답안 문장",
              f"{RES} 덕분에 {JAC}이 I + 함수의 미분이 되어, 96층에서도 {GRAD}가 1층까지 닿는다.",
              "입력을 더한다, 변화량만 배운다, 야코비안에 I 가 생긴다 세 가지를 쓰면 돼요.",
              "더하기 하나 = 고속도로 하나 로 외워요."),
      warn("헷갈리기 쉬운 점",
           f"{RES}은 새로 배우는 {PARAM}가 없어요. 더하기일 뿐이라 공짜예요.",
           "더하려면 입력과 출력의 칸 수가 같아야 해요. 그래서 트랜스포머는 층마다 폭을 d 로 유지해요.")])

# ---------------------------------------------------------------- p.50
page(50, "층 정규화 LayerNorm",
     ["Layer Normalization (LayerNorm)", "Parameter", "Token", "Gradient",
      "Residual Connection", "Transformer", "Exploding Gradient"],
     [say(f"세 번째 장치는 {LN}이에요.",
          f"{TOK} 하나가 가진 숫자들을 평균 0, 분산 1 로 맞춰 줘요.",
          "그러면 값이 너무 커지거나 작아지지 않아서 학습이 안정돼요."),
      figure("들쭉날쭉한 숫자를 가지런히", FIG_LN,
             "왼쪽은 크기가 제각각이고 평균이 치우쳐 있어요. 오른쪽은 평균 0, 분산 1 로 맞춘 모습이에요.", 4),
      analogy("반마다 다른 시험을 같은 자로 재기",
              "A반 시험은 평균 80점, B반 시험은 평균 40점이면 점수를 그대로 비교할 수 없어요. 반 평균과 퍼진 정도로 나눠서 같은 자로 만들어요.",
              ("한 반의 점수들", "토큰 하나의 숫자들"),
              ("반 평균으로 빼기", "평균 0 으로 옮기기"),
              ("퍼진 정도로 나누기", "분산 1 로 맞추기"))],
     [compare("슬라이드 영어와 우리말 뜻",
              ["영어 원문", "뜻"],
              ["Normalise each token's feature vector to mean 0 and variance 1",
               "각 토큰의 특징 벡터를 평균 0, 분산 1 로 정규화한다"],
              ["then rescale with learned gamma and beta",
               "그다음 학습한 감마와 베타로 다시 크기를 조절한다"],
              ["Note what it does not do", "무엇을 하지 않는지도 보라"],
              ["it never mixes across tokens or across the batch",
               "토큰끼리도, 배치끼리도 절대 섞지 않는다"],
              ["so it behaves identically at training and inference",
               "그래서 학습 때와 추론 때가 똑같이 동작한다"],
              ["Keeps activations in a sane range so the residual stream does not explode",
               "값을 제정신인 범위로 유지해서 잔차 흐름이 터지지 않게 한다"]),
      points("용어 하나씩",
             f"{LN}: 토큰 하나의 숫자들만 가지고 평균 0, 분산 1 로 맞추는 것이에요",
             "평균: 다 더해서 개수로 나눈 값이에요. 기호는 뮤예요",
             "분산: 평균에서 얼마나 떨어져 있는지의 제곱 평균이에요. 기호는 시그마 제곱이에요",
             f"감마와 베타: 다시 늘리고 옮기는 {PARAM}예요. 모델이 학습으로 정해요"),
      check(f"{LN}은 무엇을 섞지 않나요",
            ["다른 토큰이나 다른 문장과 섞지 않아요", "자기 숫자끼리 섞지 않아요",
             "감마와 베타를 섞지 않아요", "층끼리 섞지 않아요"], 0,
            "토큰 하나 안에서만 계산해요. 그래서 문장 길이가 달라져도 똑같이 동작해요.")],
     [look("슬라이드를 짚어 읽어요",
           (0.06, 0.199, 0.85, 0.032, "첫 점: 토큰의 특징 벡터를 평균 0, 분산 1 로. 감마와 베타로 다시 조절."),
           (0.06, 0.244, 0.85, 0.068, "둘째 점: 토큰끼리도 배치끼리도 섞지 않아서 학습과 추론이 같다."),
           (0.19, 0.348, 0.27, 0.285, "왼쪽 그래프 before: 평균 3.7, 표준편차 1.9. 빨간 점선이 평균이에요."),
           (0.56, 0.348, 0.28, 0.285, "오른쪽 after: 평균 0, 표준편차 1. 0 을 중심으로 위아래로 갈려요."),
           (0.27, 0.664, 0.50, 0.026, "작은 글씨: 두 그래프의 눈금이 다르다는 점에 주의하라고 적혀 있어요."),
           (0.14, 0.721, 0.72, 0.082, "아래 식: LN(x) = 감마 곱하기 (x - 뮤) 나누기 루트(시그마제곱 + 입실론) + 베타.")),
      formula("LayerNorm 의 식",
              r"\mathrm{LN}(x)=\gamma\odot\frac{x-\mu}{\sqrt{\sigma^{2}+\varepsilon}}+\beta,\qquad \mu=\frac{1}{d}\sum_{m}x_{m}",
              [(r"x", "토큰 하나의 숫자 d 개"),
               (r"\mu", "그 d 개의 평균. 다 더해서 d 로 나눈 값"),
               (r"\sigma^{2}", "그 d 개의 분산. 평균에서 떨어진 거리의 제곱 평균"),
               (r"\varepsilon", "0 으로 나누는 것을 막는 아주 작은 수"),
               (r"\gamma", "칸마다 다시 늘려 주는 학습 파라미터"),
               (r"\beta", "칸마다 다시 옮겨 주는 학습 파라미터"),
               (r"\odot", "같은 자리끼리 곱하기")],
              "평균을 빼고 퍼진 정도로 나눈 뒤, 감마로 늘리고 베타로 옮겨요."),
      steps("숫자 네 개로 직접 해 봐요",
            ["토큰 하나의 숫자가 2, 4, 4, 10 이라고 해요",
             "평균은 (2 + 4 + 4 + 10) 나누기 4 = 5 예요",
             "평균에서 뺀 값은 -3, -1, -1, 5 예요",
             "제곱해서 평균: (9 + 1 + 1 + 25) 나누기 4 = 9, 이게 분산이에요",
             "분산 9 의 제곱근은 3 이에요. 이것으로 나눠요",
             "결과는 -1, -0.333, -0.333, 1.667 이에요"],
            "평균은 0, 분산은 1 이 됐어요. 감마 2, 베타 1 이면 -1, 0.333, 0.333, 4.333 이 돼요.",
            "x = (2, 4, 4, 10)"),
      prof("교수님: 배치 놈과 다르게 레이어 놈은 각 d 차원만 정규화해 주는 거예요.",
           "교수님: 평균 뮤와 분산을 구한 다음 평균 0, 분산 1 로 맞춰 주고 감마와 베타를 곱해 줍니다.",
           "교수님: 학습할 때랑 추론할 때 들어오는 토큰 정보가 많이 다르잖아요. 그걸 정규화해 주는 거예요.",
           "교수님: 정규화를 깊게 다루지는 않을게요. 이해가 어려우면 이런 게 있다고 보셔도 됩니다."),
      bg("기초 다지기 1단원",
         "벡터는 숫자를 한 줄로 늘어놓은 것이에요. 여기서는 토큰 하나가 가진 512개 숫자예요.",
         "평균을 빼면 중심이 0 으로 옮겨지고, 표준편차로 나누면 퍼진 폭이 1 이 돼요.",
         "512개를 모두 이렇게 바꿔도 서로의 순위는 그대로예요.")],
     [check("다음 중 LayerNorm 의 설명으로 틀린 것은",
            ["배치 안의 여러 문장 통계를 함께 써요", "토큰 하나의 숫자들만 써요",
             "감마와 베타는 학습으로 정해져요", "문장 길이가 달라져도 똑같이 동작해요"], 0,
            "배치와 섞지 않는다는 것이 LayerNorm 의 핵심이에요."),
      check("x = (2, 4, 4, 10) 을 정규화하면 첫 값은",
            ["-1", "0", "1", "-3"], 0,
            "평균 5, 표준편차 3 이니까 (2 - 5) 나누기 3 = -1 이에요."),
      english("답안 문장",
              f"{LN}은 각 {TOK}의 특징 벡터를 평균 0, 분산 1 로 정규화한 뒤 학습된 감마와 베타로 다시 조절하며, 다른 토큰이나 배치와 섞지 않아 학습과 추론에서 동일하게 동작한다.",
              "무엇을 하는지와 무엇을 하지 않는지를 같이 써야 만점이에요.",
              "토큰 하나 안에서만 = 길이가 달라도 안전 으로 외워요."),
      warn("헷갈리기 쉬운 점",
           f"{LN}은 {RES}을 대신하는 게 아니에요. 둘은 함께 쓰여요.",
           "정규화한 뒤 감마와 베타로 다시 늘리는 단계를 빼먹으면 안 돼요. 표현력이 사라져요.",
           "슬라이드의 왼쪽과 오른쪽 그래프는 눈금이 달라요. 막대 높이를 직접 비교하면 안 돼요.")])

# ---------------------------------------------------------------- p.51
page(51, "Pre-LN 과 Post-LN",
     ["Layer Normalization (LayerNorm)", "Residual Connection", "Transformer",
      "Large Language Model (LLM)", "Learning Rate", "Gradient"],
     [say(f"{LN}을 어디에 두느냐로 두 가지 방식이 나뉘어요.",
          "더한 다음에 두면 Post-LN, 서브층에 넣기 전에 두면 Pre-LN 이에요.",
          "2017년 원 논문은 Post-LN 이고, 요즘 모델은 대부분 Pre-LN 이에요."),
      figure("더하기 전인가, 더한 다음인가", FIG_PRELN,
             "왼쪽 Post-LN 은 더한 다음 정규화해요. 오른쪽 Pre-LN 은 먼저 정규화하고 서브층에 넣어요.", 4),
      analogy("빨래를 언제 개나요",
              "빨래를 개서 바구니에 넣을 수도 있고, 바구니에 다 모은 다음에 갤 수도 있어요. 순서만 바뀌는데 바구니가 훨씬 깔끔해져요.",
              ("바구니", "잔차 경로"),
              ("먼저 개고 넣기", "Pre-LN"),
              ("모은 다음에 개기", "Post-LN"))],
     [compare("슬라이드 영어와 우리말 뜻",
              ["영어 원문", "뜻"],
              ["The 2017 paper normalised after the residual addition",
               "2017년 논문은 잔차를 더한 뒤에 정규화했다"],
              ["It works, but needs a careful learning-rate warmup",
               "되기는 되는데 조심스러운 학습률 워밍업이 필요하다"],
              ["or training diverges", "아니면 학습이 발산한다"],
              ["Putting LayerNorm before the sublayer keeps the residual path completely clean",
               "LayerNorm 을 서브층 앞에 두면 잔차 경로가 완전히 깨끗해진다"],
              ["Every modern LLM does this", "요즘 LLM 은 다 이렇게 한다"],
              ["A two-line change that made 100-layer stacks routine",
               "두 줄 바꿔서 100층 쌓기를 평범한 일로 만든 변화"]),
      compare("두 방식 비교",
              ["", "Post-LN", "Pre-LN"],
              ["식", "LN(x + f(x))", "x + f(LN(x))"],
              ["정규화 위치", "더한 다음", "서브층에 넣기 전"],
              ["잔차 경로", "정규화를 거쳐요", "손대지 않아 깨끗해요"],
              ["쓰는 곳", "2017년 원 논문", f"요즘 {LLM} 들"],
              ["주의", "학습률 워밍업이 꼭 필요해요", "그대로 깊게 쌓기 쉬워요"]),
      points("용어 하나씩",
             f"{LR}: 한 걸음의 보폭이에요. 3주차에 배웠어요",
             "워밍업: 처음에는 보폭을 아주 작게 시작해 서서히 키우는 것이에요",
             "발산: 손실이 줄지 않고 커져서 학습이 터지는 것이에요")],
     [look("슬라이드를 짚어 읽어요",
           (0.06, 0.187, 0.83, 0.066, "첫 점: 2017년 논문은 잔차를 더한 뒤 정규화. 워밍업이 없으면 발산."),
           (0.06, 0.276, 0.78, 0.028, "둘째 점: LayerNorm 을 앞에 두면 잔차 경로가 깨끗하다. 요즘 LLM 이 다 이 방식."),
           (0.21, 0.399, 0.27, 0.405, "왼쪽 상자 Post-LN: x 에서 서브층, 더하기, 그 위에 LayerNorm."),
           (0.28, 0.430, 0.14, 0.035, "왼쪽 위 식 LN(x + f(x)) 이 Post-LN 이에요."),
           (0.49, 0.399, 0.26, 0.405, "오른쪽 Pre-LN: x 에서 LayerNorm, 서브층, 그다음 더하기."),
           (0.57, 0.430, 0.14, 0.035, "오른쪽 위 식 x + f(LN(x)) 가 Pre-LN 이에요.")),
      formula("두 방식의 식",
              r"\text{Post-LN: } \mathrm{LN}\big(x+f(x)\big)\qquad \text{Pre-LN: } x+f\big(\mathrm{LN}(x)\big)",
              [(r"x", "이 서브층에 들어온 값"),
               (r"f", "서브층. 셀프 어텐션이거나 피드포워드예요"),
               (r"\mathrm{LN}", "층 정규화"),
               (r"x+f(\mathrm{LN}(x))", "Pre-LN. 바깥의 x 가 아무것도 안 거치고 그대로 남아요")],
              "Pre-LN 은 더해지는 x 가 손대지 않은 값이라 잔차 경로가 완전히 깨끗해요."),
      prof("교수님: 2017년 제가 설명하고 있는 트랜스포머에서는 이 Post-LN 방법을 사용했어요.",
           "교수님: 여러 실험을 했을 때 Pre-LN 이 좋다는 게 많이 밝혀져서 요즘 LLM 은 대부분 Pre-LN 을 써요.",
           "교수님: 사실 최근에는 RMSNorm 같은 것도 많이 쓰거든요. 그래서 '다 쓴다' 보다는 '흔하다' 로 봐 주세요.",
           "교수님: 트랜스포머에서는 Post-LN 이 쓰였다, 이 정도로만 보면 될 것 같아요."),
      bg("기초 다지기 8단원",
         f"{LR}은 경사 하강법의 보폭이에요. 크면 빨리 가지만 튕겨 나갈 수 있어요.",
         "워밍업은 처음 몇백 걸음 동안 보폭을 0 에서부터 천천히 키우는 방법이에요.",
         "Post-LN 은 이 워밍업 없이 큰 보폭으로 시작하면 바로 학습이 터져요.")],
     [check("2017년 원 논문이 쓴 방식은",
            ["Post-LN", "Pre-LN", "둘 다", "둘 다 아님"], 0,
            "원 논문은 잔차를 더한 다음 정규화하는 Post-LN 이에요. 요즘은 Pre-LN 이 흔해요."),
      check("Pre-LN 의 장점은",
            ["잔차 경로가 정규화를 안 거쳐 깨끗해요", "파라미터가 줄어요",
             "계산이 절반이 돼요", "마스킹이 필요 없어요"], 0,
            "슬라이드: keeps the residual path completely clean."),
      english("답안 문장",
              f"Post-LN 은 {RES}을 더한 뒤 정규화해 LN(x + f(x)) 이고, Pre-LN 은 x + f(LN(x)) 이다.",
              "두 식을 그대로 쓸 수 있으면 끝이에요.",
              "Post 는 더한 뒤, Pre 는 넣기 전 으로 외워요."),
      warn("헷갈리기 쉬운 점",
           "Pre 와 Post 는 서브층 기준이에요. Pre-LN 은 서브층 앞, Post-LN 은 잔차 더하기 뒤예요.",
           f"교수님이 직접 말을 완화했어요. 모든 {LLM}이 Pre-LN 인 것은 아니고, 흔하다는 뜻이에요.")])

# ---------------------------------------------------------------- p.52
page(52, "인코더 블록과 디코더 블록",
     ["Encoder", "Decoder", "Self-Attention", "Multi-Head Attention (MHA)",
      "Residual Connection", "Layer Normalization (LayerNorm)",
      "Position-wise Feed-Forward Network (FFN)", "Causal Masking", "Cross-Attention",
      "Transformer", "Token"],
     [say("이제 배운 부품을 조립해요. 블록은 딱 두 종류예요.",
          f"{ENC} 블록은 {SA}과 피드포워드 두 층이에요.",
          f"{DEC} 블록은 거기에 마스킹과 {CA}이 더 붙어요."),
      figure("블록 두 개가 전부예요", FIG_BLOCKS,
             "왼쪽 인코더 블록은 서브층 2개, 오른쪽 디코더 블록은 서브층 3개예요.", 4),
      points("한 줄 요약",
             f"{ENC} 블록: 셀프 어텐션 -> Add & Norm -> 피드포워드 -> Add & Norm",
             f"{DEC} 블록: 위에다 마스킹된 셀프 어텐션과 {CA}을 더한 것")],
     [compare("슬라이드 영어와 우리말 뜻",
              ["영어 원문", "뜻"],
              ["Encoder block: self-attention, Add & Norm, feed-forward, Add & Norm",
               "인코더 블록은 셀프 어텐션, 더하고 정규화, 피드포워드, 더하고 정규화"],
              ["Bidirectional", "양방향이다. 앞뒤를 다 본다"],
              ["Decoder block: the same, plus a masked self-attention at the bottom",
               "디코더 블록은 같은데 아래에 마스킹된 셀프 어텐션이 더 있다"],
              ["and a cross-attention in the middle",
               "그리고 가운데에 크로스 어텐션이 있다"],
              ["bidirectional, sees the whole source",
               "양방향, 원문 전체를 본다"],
              ["causal, sees only what it has written",
               "인과적, 자기가 써 놓은 것만 본다"]),
      points("Add & Norm 이 무슨 뜻인가요",
             f"Add 는 {RES}이에요. 서브층 입력을 출력에 더해요",
             f"Norm 은 {LN}이에요. 더한 값을 평균 0, 분산 1 로 맞춰요",
             "즉 Add & Norm 한 칸은 앞에서 배운 두 장치를 한 번에 적은 것이에요"),
      steps("인코더 블록을 순서대로 지나가 봐요",
            [f"{TOK} n 개가 각각 d 칸을 가진 표가 들어와요",
             f"{MHA}로 서로를 봐요. 마스크가 없어서 앞뒤를 다 봐요",
             "Add & Norm: 입력을 더하고 정규화해요",
             f"{FFN}이 토큰마다 따로 깊게 처리해요",
             "Add & Norm 을 한 번 더 해요",
             "나온 표를 다음 블록에 그대로 넘겨요"],
            "인코더 블록은 서브층 2개. 이것을 N 번 쌓아요."),
      check(f"{DEC} 블록에만 있고 {ENC} 블록에는 없는 것은",
            ["마스킹된 셀프 어텐션과 크로스 어텐션", "피드포워드", "Add & Norm", "잔차 연결"], 0,
            "인코더는 미래 토큰을 봐도 상관없어서 마스크가 없어요.")],
     [look("슬라이드를 짚어 읽어요",
           (0.06, 0.199, 0.65, 0.032, "첫 점: 인코더 블록은 셀프 어텐션, Add & Norm, 피드포워드, Add & Norm."),
           (0.06, 0.248, 0.73, 0.032, "둘째 점: 디코더 블록은 여기에 마스킹과 크로스 어텐션이 더 붙는다."),
           (0.07, 0.500, 0.34, 0.310, "왼쪽 주황 점선 상자가 인코더 블록. 맨 아래가 멀티 헤드 셀프 어텐션."),
           (0.07, 0.790, 0.34, 0.028, "인코더 아래 글씨: bidirectional, 원문 전체를 본다."),
           (0.50, 0.592, 0.30, 0.047, "디코더 가운데 초록 상자가 CROSS-attention 이에요."),
           (0.50, 0.725, 0.30, 0.049, "디코더 맨 아래가 MASKED self-attention 이에요.")),
      compare("두 블록의 서브층을 세어 봐요",
              ["블록", "서브층", "마스크", "보는 범위"],
              ["인코더 블록", "셀프 어텐션, 피드포워드 (2개)", "없어요", "원문 전체"],
              ["디코더 블록", "마스킹 셀프, 크로스, 피드포워드 (3개)", "맨 아래에 있어요", "자기가 쓴 것까지"]),
      prof("교수님: 인코더 쪽은 미래의 토큰을 봐도 상관이 없단 말이죠. 그래서 마스크가 없고요.",
           "교수님: 인코더는 양방향 셀프 어텐션, 디코더는 마스킹 셀프 어텐션 형태다.",
           "교수님: 번역할 때 I love you 에 대한 정보가 있어야 디코더가 생성해 나갈 거 아니에요.",
           "교수님: 그래서 인코더에 있는 정보를 끌어오는 크로스 어텐션을 해 줍니다."),
      bg("기초 다지기 9단원",
         f"{FFN}은 뉴런 층 두 개짜리 아주 작은 신경망이에요.",
         "속 차원을 4d 로 넓혔다가 다시 d 로 줄여요. 그 사이에 비선형 함수가 들어가요.",
         "토큰마다 따로 적용하기 때문에 순서와 아무 상관이 없어요.")],
     [check("인코더 블록이 양방향인 이유는",
            ["원문은 미래 토큰을 봐도 되니까", "계산이 빨라서", "파라미터가 적어서", "마스크를 못 만들어서"], 0,
            "교수님: 인코더 쪽은 미래의 토큰을 봐도 상관이 없어서 마스크가 없어요."),
      exam("예상 문제",
           "트랜스포머 인코더 블록과 디코더 블록의 구성을 각각 쓰고 차이를 설명하시오.",
           "블록 두 개를 아래에서 위로 그대로 적어 보세요.",
           ["인코더 블록: 멀티 헤드 셀프 어텐션 -> Add & Norm -> 피드포워드 -> Add & Norm",
            "디코더 블록: 마스킹된 셀프 어텐션 -> Add & Norm -> 크로스 어텐션 -> Add & Norm -> 피드포워드 -> Add & Norm",
            "차이 1: 디코더는 맨 아래에 인과 마스킹이 있어요",
            "차이 2: 디코더 가운데에 크로스 어텐션이 있어요",
            "인코더는 양방향, 디코더는 인과적이에요"],
           "서브층이 인코더는 2개, 디코더는 3개예요."),
      english("답안 문장",
              f"{ENC} 블록은 서브층 2개로 양방향, {DEC} 블록은 마스킹 {SA}과 {CA}을 더한 서브층 3개예요.",
              "서브층 개수와 마스크 유무를 반드시 함께 써요.",
              "인코더 2층, 디코더 3층 으로 외워요."),
      warn("헷갈리기 쉬운 점",
           f"Add & Norm 은 새 부품이 아니에요. {RES}과 {LN}을 한 칸에 적은 것이에요.",
           f"{CM}은 디코더 맨 아래 셀프 어텐션에만 걸려요. 크로스 어텐션에는 걸지 않아요.")])

# ---------------------------------------------------------------- p.53
page(53, "크로스 어텐션이 둘을 잇는다",
     ["Cross-Attention", "Self-Attention", "Query", "Key", "Value", "Encoder", "Decoder",
      "Attention", "Context Vector", "Machine Translation (MT)", "Information Bottleneck",
      "Dot Product"],
     [say(f"{DEC} 블록 가운데 서브층이 {CA}이에요.",
          f"{QRY}는 디코더에서 나오고, {KEY}와 {VAL}는 인코더 출력에서 가져와요.",
          "2장에서 배운 2015년 어텐션이 그대로 돌아온 거예요. 원이 여기서 닫혀요."),
      figure("쿼리는 디코더, 키와 밸류는 인코더", FIG_CROSS,
             "왼쪽 인코더 출력에서 K 와 V 를, 오른쪽 디코더 상태에서 Q 를 만들어 어텐션해요.", 4),
      analogy("시험 볼 때 교과서 다시 펼치기",
              "2장에서 쓴 비유 그대로예요. 답을 한 줄 쓸 때마다 교과서에서 필요한 쪽을 다시 펼쳐 봐요.",
              ("지금 쓰고 있는 답", "디코더 상태에서 만든 쿼리"),
              ("교과서의 쪽 번호", "인코더 출력에서 만든 키"),
              ("그 쪽에 적힌 내용", "인코더 출력에서 만든 밸류"))],
     [compare("슬라이드 영어와 우리말 뜻",
              ["영어 원문", "뜻"],
              ["In the decoder's middle sublayer the queries come from the decoder",
               "디코더의 가운데 서브층에서 쿼리는 디코더에서 온다"],
              ["but the keys and values come from the encoder output",
               "그런데 키와 밸류는 인코더 출력에서 온다"],
              ["This is literally the 2015 attention of section 2",
               "이것은 말 그대로 2장의 2015년 어텐션이다"],
              ["rewritten in Q / K / V notation", "Q / K / V 표기로 다시 쓴 것뿐이다"],
              ["The circle closes here", "원이 여기서 닫힌다"],
              ["Self-attention looks inward, cross-attention looks across",
               "셀프 어텐션은 안을 보고, 크로스 어텐션은 건너편을 본다"]),
      compare("셀프 어텐션과 크로스 어텐션",
              ["", "셀프 어텐션", "크로스 어텐션"],
              ["쿼리 출처", "같은 시퀀스", "디코더"],
              ["키, 밸류 출처", "같은 시퀀스", "인코더 출력"],
              ["보는 방향", "자기 안쪽", "건너편"],
              ["계산 방법", "같아요", "같아요"]),
      points("용어 하나씩",
             f"{CA}: 쿼리와 키, 밸류가 서로 다른 쪽에서 나오는 어텐션이에요",
             f"{SA}: 쿼리, 키, 밸류가 모두 같은 시퀀스에서 나오는 어텐션이에요",
             f"{CTX}: 밸류들의 가중 평균. 여기서도 똑같이 만들어져요")],
     [look("슬라이드를 짚어 읽어요",
           (0.06, 0.199, 0.85, 0.032, "첫 점: 쿼리는 디코더에서, 키와 밸류는 인코더 출력에서 온다."),
           (0.06, 0.248, 0.75, 0.032, "둘째 점: 이것이 바로 2장의 2015년 어텐션이다. 원이 여기서 닫힌다."),
           (0.14, 0.358, 0.27, 0.066, "왼쪽 위 주황 상자: Encoder output H, 위 글씨는 원문 문장 전체."),
           (0.60, 0.358, 0.26, 0.066, "오른쪽 위 초록 상자: Decoder state S, 지금까지 만든 번역문."),
           (0.14, 0.484, 0.27, 0.058, "왼쪽 아래 두 상자: K = H W^K 와 V = H W^V."),
           (0.34, 0.605, 0.32, 0.063, "가운데 파란 상자 Attention(Q, K, V) 로 세 화살표가 모여요.")),
      formula("크로스 어텐션의 Q, K, V",
              r"Q=S\,W^{Q}\ \text{(decoder)},\qquad K=H\,W^{K},\ V=H\,W^{V}\ \text{(encoder)}",
              [(r"S", "디코더 상태. 지금까지 쓴 번역문의 표현이에요"),
               (r"H", "인코더 출력. 원문 문장 전체의 표현이에요"),
               (r"Q=S\,W^{Q}", "쿼리는 디코더 쪽에서 만들어요"),
               (r"K=H\,W^{K}", "키는 인코더 쪽에서 만들어요"),
               (r"V=H\,W^{V}", "밸류도 인코더 쪽에서 만들어요")],
              "Q 만 디코더, K 와 V 는 인코더. 이 한 가지가 셀프 어텐션과의 유일한 차이예요."),
      prof("교수님: 크로스 어텐션은 쿼리는 디코더 상태에서 나오고 키랑 밸류는 인코더 출력에서 가져옵니다.",
           "교수님: 2장에서 배운 그 개념이죠. 인코더와 디코더 블록을 연결해 주는 게 크로스 어텐션입니다.",
           "교수님: 셀프 어텐션은 쿼리 키 밸류가 각각의 시퀀스에서 따로따로 나옵니다.",
           "교수님: 계산 방법은 같다, 다만 Q, K, V 가 어디서 나오냐에 차이가 있다."),
      bg("기초 다지기 2단원",
         f"{ATT} 계산은 {DP}으로 점수를 내고, 소프트맥스로 합을 1 로 만들고, 가중합을 하는 것이에요.",
         "크로스 어텐션도 이 순서가 똑같아요. 재료를 어디서 가져오는지만 달라요.",
         "그래서 새로 외울 계산이 하나도 없어요.")],
     [check(f"{CA}에서 {KEY}와 {VAL}가 나오는 곳은",
            ["인코더 출력", "디코더 상태", "임베딩 층", "출력 소프트맥스"], 0,
            "쿼리만 디코더에서 나와요. 키와 밸류는 인코더 출력에서 나와요."),
      exam("예상 문제",
           "셀프 어텐션과 크로스 어텐션의 차이를 Q, K, V 의 출처로 설명하시오.",
           "계산은 같고 재료만 다르다는 점을 써 보세요.",
           ["두 어텐션 모두 점수, 소프트맥스, 가중합 계산은 완전히 같아요",
            "셀프 어텐션은 Q, K, V 가 모두 같은 시퀀스에서 나와요",
            "크로스 어텐션은 Q 가 디코더, K 와 V 가 인코더 출력에서 나와요",
            "그래서 셀프는 안쪽을, 크로스는 건너편을 봐요"],
           "차이는 오직 Q, K, V 를 어디서 만드는가입니다."),
      english("답안 문장",
              f"{CA}은 {QRY}가 {DEC}, {KEY}와 {VAL}가 {ENC}에서 나온다는 점만 다르다.",
              f"계산은 2장에서 {IB}을 없앤 그 {ATT}과 똑같아요. 출처만 달라요.",
              "Q 는 디코더, K 와 V 는 인코더 로 외워요."),
      warn("헷갈리기 쉬운 점",
           f"{CA}은 새로운 계산이 아니에요. {MT}에서 쓰던 2015년 어텐션 그대로예요.",
           "키와 밸류는 항상 같은 쪽에서 나와요. 키만 인코더, 밸류만 디코더 같은 건 없어요.")])

# ---------------------------------------------------------------- p.54
page(54, "트랜스포머 전체 구조",
     ["Transformer", "Encoder", "Decoder", "Positional Encoding", "Embedding",
      "Multi-Head Attention (MHA)", "Cross-Attention", "Causal Masking", "Softmax",
      "Position-wise Feed-Forward Network (FFN)", "Residual Connection",
      "Layer Normalization (LayerNorm)", "Self-Attention"],
     [say(f"오늘 배운 모든 부품이 이 한 장에 다 들어 있어요.",
          "슬라이드의 모든 상자가 우리가 지난 몇 시간 동안 만든 것들이에요.",
          "슬라이드가 시키는 것은 하나예요. 노트를 덮고 이 그림을 다시 그려 보세요."),
      figure("전체 구조 한 장", FIG_FULL,
             "왼쪽이 인코더 N 층, 오른쪽이 디코더 N 층. 인코더 출력이 크로스 어텐션의 키와 밸류로 건너가요.", 4),
      points("한 줄 요약",
             f"아래에서 위로: {EMB} + {PE} -> 블록 N 번 -> Linear + {SMX}",
             "그리기 시험이 바로 이 쪽이에요")],
     [steps("아래에서 위로 한 칸씩 읽어요 (인코더)",
            [f"입력 {EMB}에 {PE}를 더해요. 순서를 알려 주는 단계예요",
             f"{MHA} {SA}. 마스크가 없어요",
             f"Add & Norm ({RES} + {LN})",
             f"{FFN}",
             "Add & Norm 을 한 번 더",
             "이 블록을 N 번 반복하고, 마지막 출력을 디코더로 보내요"],
            "인코더 출력 H 가 크로스 어텐션의 키와 밸류가 돼요."),
      steps("아래에서 위로 한 칸씩 읽어요 (디코더)",
            [f"출력 {EMB}에 {PE}를 더해요",
             f"마스킹된 {MHA} {SA}. {CM}이 걸려요",
             "Add & Norm",
             f"멀티 헤드 {CA}. 키와 밸류는 인코더에서 와요",
             "Add & Norm, 그다음 피드포워드, 다시 Add & Norm",
             f"맨 위에서 Linear 를 지나 {SMX}로 다음 토큰의 확률을 내요"],
            "디코더는 블록 N 번을 지나 마지막에 어휘 크기의 확률을 만들어요."),
      compare("슬라이드 영어와 우리말 뜻",
              ["영어 원문", "뜻"],
              ["Every box on this diagram is something we built in the last hours",
               "이 그림의 모든 상자는 지난 몇 시간 동안 우리가 만든 것이다"],
              ["Encoder x N", "인코더 블록을 N 번 쌓는다"],
              ["keys and values from the encoder",
               "키와 밸류는 인코더에서 온다"],
              ["Close your notes and try to redraw this",
               "노트를 덮고 이것을 다시 그려 보라"],
              ["that is the test", "그것이 바로 시험이다"])],
     [look("슬라이드를 짚어 읽어요",
           (0.06, 0.199, 0.50, 0.032, "첫 점: 이 그림의 모든 상자를 오늘 다 만들었다."),
           (0.25, 0.481, 0.23, 0.285, "왼쪽 주황 점선이 인코더 스택. 맨 아래가 입력 임베딩 + 위치 인코딩."),
           (0.52, 0.367, 0.24, 0.399, "오른쪽 초록 점선이 디코더 스택. 맨 아래가 출력 임베딩 + 위치 인코딩."),
           (0.39, 0.418, 0.09, 0.044, "가운데 초록 화살표에 keys and values from the encoder 라고 적혀 있어요."),
           (0.53, 0.308, 0.21, 0.032, "디코더 맨 위 진한 상자가 Linear + softmax 예요."),
           (0.79, 0.491, 0.17, 0.410, "오른쪽 작은 그림이 2017년 원 논문의 그림이에요.")),
      points("상자마다 어디서 배웠는지",
             f"{PE}: 셀프 어텐션이 순서를 몰라서 넣었어요",
             f"마스킹된 {SA}: 미래를 못 보게 하려고 넣었어요",
             f"{FFN}: 토큰마다 깊은 비선형 처리를 하려고 넣었어요",
             f"{MHA}, {RES}, {LN}: 오늘 4장에서 더한 세 가지예요",
             f"{CA}: 인코더 정보를 디코더로 끌어오려고 넣었어요"),
      prof("교수님: 이제 진짜 다 배웠습니다. 지금까지 배운 구성 요소들을 트랜스포머 블록으로 조립해 보면.",
           "교수님: 오늘 배운 인코더와 디코더를 구성하는 모든 요소들이 다 이 슬라이드에 있어요.",
           "교수님: 이 슬라이드를 배우기 위해서 지금까지 달려왔다고 보시면 될 것 같습니다.",
           "교수님: Attention Is All You Need 논문은 무조건 꼭 읽어 보시길 매우 추천드립니다."),
      bg("기초 다지기 10단원",
         "Linear 는 행렬 곱 한 번이에요. d 칸을 어휘 크기 칸으로 바꿔요.",
         f"그 위에 {SMX}를 씌우면 어휘의 각 토큰이 나올 확률이 돼요.",
         "3주차 언어 모델에서 본 마지막 단계와 똑같아요.")],
     [check("인코더 출력이 디코더에서 맡는 역할은",
            ["크로스 어텐션의 키와 밸류", "디코더의 쿼리", "위치 인코딩", "소프트맥스의 입력"], 0,
            "슬라이드의 초록 화살표에 keys and values from the encoder 라고 적혀 있어요."),
      exam("예상 문제",
           "트랜스포머 전체 구조를 아래에서 위로 그리시오.",
           "인코더 쪽과 디코더 쪽을 나란히 그리고 화살표를 하나 그으면 돼요.",
           ["양쪽 맨 아래에 임베딩 + 위치 인코딩을 그려요",
            "인코더: 멀티 헤드 셀프 어텐션, Add & Norm, 피드포워드, Add & Norm",
            "디코더: 마스킹된 셀프 어텐션, Add & Norm, 크로스 어텐션, Add & Norm, 피드포워드, Add & Norm",
            "인코더 맨 위에서 디코더 크로스 어텐션으로 화살표를 긋고 키와 밸류라고 적어요",
            "두 스택 옆에 x N 을 적고, 디코더 위에 Linear + softmax 를 올려요"],
           "이 그림을 혼자 그릴 수 있으면 4강은 끝난 거예요."),
      english("답안 문장",
              f"{TRF}는 {EMB}와 {PE} 위에 {ENC} 블록과 {DEC} 블록을 N 개씩 쌓은 구조이다.",
              f"맨 위에서 Linear 와 {SMX}로 다음 토큰 확률을 내요. 구조를 한 문장에 담아 보세요.",
              "임베딩, 블록 N개, Linear + softmax 세 덩어리로 외워요."),
      warn("헷갈리기 쉬운 점",
           "x N 은 같은 블록을 N 개 쌓는다는 뜻이에요. 같은 블록을 N 번 돌리는 게 아니라 서로 다른 N 개예요.",
           f"{PE}는 맨 아래에서 한 번만 더해요. 블록마다 다시 더하지 않아요.")])

# ---------------------------------------------------------------- p.55
page(55, "치러야 할 값, 이차 비용",
     ["Quadratic Cost", "Self-Attention", "Attention Score", "Parallelization",
      "Recurrent Neural Network (RNN)", "Convolutional Neural Network (CNN)",
      "Large Language Model (LLM)", "Token", "Query", "Key", "Dot Product"],
     [say(f"좋은 것만 있는 방법은 없어요. {TRF}가 치르는 값이 이것이에요.",
          f"{SA}은 n 개의 토큰이 서로를 다 봐야 해서 n x n 짜리 점수 표를 만들어요.",
          f"그래서 계산도 메모리도 길이의 제곱으로 커져요. 이것이 {QC}이에요."),
      figure("길이가 2배면 표는 4배", FIG_QUAD,
             "n = 2 이면 칸이 4개, n = 4 이면 칸이 16개. 길이가 2배가 되면 칸은 4배가 돼요.", 4),
      analogy("반 친구들 악수하기",
              "10명이면 서로 악수하는 짝이 얼마 안 되는데, 100명이 되면 훨씬 더 많이 늘어나요. 사람 수가 10배면 악수는 100배쯤이에요.",
              ("한 사람", "토큰 하나"),
              ("악수 한 번", "어텐션 점수 한 칸"),
              ("사람이 늘면 악수는 제곱으로", "길이가 늘면 비용은 제곱으로"))],
     [compare("슬라이드 영어와 우리말 뜻",
              ["영어 원문", "뜻"],
              ["The score matrix is n x n",
               "점수 행렬이 n 곱하기 n 이다"],
              ["so both compute and memory grow with the square of the sequence length",
               "그래서 계산도 메모리도 길이의 제곱으로 자란다"],
              ["At n = 512 this is cheap", "n = 512 에서는 싸다"],
              ["At n = 128,000 it is the single biggest engineering problem in LLMs",
               "n = 128,000 에서는 LLM 최대의 공학 문제다"],
              ["FlashAttention, sliding windows, linear attention and state-space models",
               "FlashAttention, 슬라이딩 윈도우, 선형 어텐션, 상태공간 모델"],
              ["all attack exactly this", "모두 정확히 이 문제를 공격한다"]),
      points("용어 하나씩",
             f"{QC}: 길이가 2배면 일이 4배가 되는 비용. {LLM} 최대의 공학 문제예요",
             f"{ASC}: {QRY}와 {KEY}의 {DP}으로 만든 날것 숫자예요",
             "O(n 제곱): 길이 n 에 대해 제곱으로 자란다는 표시예요",
             f"{PAR}: 여러 계산을 한꺼번에 하기. 이건 트랜스포머가 얻은 것이에요"),
      check("셀프 어텐션의 점수 표 크기는",
            ["n x n", "n x d", "d x d", "n x 1"], 0,
            "모든 쿼리가 모든 키와 만나야 하니까 n 줄 n 칸이에요.")],
     [look("슬라이드를 짚어 읽어요",
           (0.06, 0.199, 0.68, 0.032, "첫 점: 점수 행렬이 n x n 이라 계산도 메모리도 제곱으로 커진다."),
           (0.06, 0.244, 0.87, 0.068, "둘째 점: n = 512 는 싸고 n = 128,000 은 LLM 최대의 공학 문제."),
           (0.11, 0.348, 0.33, 0.361, "왼쪽 그래프: 초록은 RNN 의 O(n x d), 빨강은 어텐션의 O(n 제곱)."),
           (0.52, 0.386, 0.36, 0.253, "오른쪽 표: RNN, CNN, 셀프 어텐션의 경로 길이, 순차 연산, 층당 계산량."),
           (0.52, 0.600, 0.36, 0.040, "셀프 어텐션 줄: 경로 길이 O(1), 순차 연산 O(1), 계산 O(n 제곱 x d)."),
           (0.14, 0.747, 0.72, 0.057, "아래 식: scores 가 n x n 이라 계산은 O(n 제곱 d), 메모리는 O(n 제곱).")),
      compare("슬라이드 표를 그대로 읽어요",
              ["모델", "최대 경로 길이", "순차 연산", "층당 계산량"],
              ["RNN", "O(n)", "O(n)", "O(n x d 제곱)"],
              ["CNN (폭 k)", "O(n / k)", "O(1)", "O(k x n x d 제곱)"],
              ["셀프 어텐션", "O(1)", "O(1)", "O(n 제곱 x d)"]),
      steps("n = 512 와 n = 128000 을 직접 세어 봐요",
            ["n = 512 이면 점수 표 칸 수는 512 x 512 = 262144 개",
             "약 26만 개예요. 요즘 GPU 에는 아무것도 아니에요",
             "n = 128000 이면 128000 x 128000 이에요",
             "= 16,384,000,000 개, 약 164억 칸이에요",
             "길이는 128000 나누기 512 = 250배 늘었을 뿐인데",
             "칸 수는 250 의 제곱 = 62500배가 됐어요"],
            "길이 250배에 비용은 62500배. 이것이 이차 비용이에요.",
            "n = 512 와 n = 128000"),
      steps("RNN 과 비교해 봐요 (d = 512)",
            ["RNN 은 자리마다 한 번씩만 계산해요. n x d = 512 x 512 = 262144",
             "셀프 어텐션은 n 제곱 x d = 512 x 512 x 512 = 134217728",
             "나누면 134217728 나누기 262144 = 512 배예요",
             "대신 RNN 은 순차 연산이 O(n) 이라 512번을 줄 서서 기다려요",
             "셀프 어텐션의 순차 연산은 O(1) 이라 한 번에 끝나요"],
            "계산량은 더 쓰지만 기다리는 횟수는 훨씬 적어요. 이게 맞바꾸기예요.",
            "n = 512, d = 512"),
      prof("교수님: 이 세상에 노 프리 런치라고 하는데, 진짜 그냥 좋은 방향으로만 가는 건 없어요.",
           "교수님: 병렬로 가면 시간 복잡도는 확 줄어들지만 메모리는 훨씬 더 많이 써야 해요.",
           "교수님: RNN 은 O(n) 메모리면 되는데 어텐션은 n 제곱이 필요하니까요.",
           "교수님: 512 토큰은 금방 되는데, 128k 짜리 긴 소설을 다 넣으면 메모리도 계산도 엄청나게 커집니다."),
      bg("기초 다지기 3단원",
         "n x n 표는 줄이 n 개, 칸이 n 개인 표예요. 칸 수는 n 곱하기 n 이에요.",
         "n 이 2배가 되면 줄도 2배, 칸도 2배라서 전체는 4배가 돼요.",
         "이것이 '제곱으로 자란다' 는 말의 뜻이에요.")],
     [check("길이가 250배 늘어나면 어텐션 점수 표의 칸 수는",
            ["62500배", "250배", "500배", "그대로"], 0,
            "250 의 제곱이 62500 이에요. 128000 나누기 512 가 250 이에요."),
      check(f"{QC} 문제를 푸는 연구로 슬라이드가 든 것이 아닌 것은",
            ["교사 강요", "FlashAttention", "슬라이딩 윈도우", "선형 어텐션"], 0,
            "교사 강요는 학습 방법이에요. 슬라이드가 든 것은 FlashAttention, 슬라이딩 윈도우, 선형 어텐션, 상태공간 모델이에요."),
      english("답안 문장",
              f"{SA}은 n 개의 {QRY}가 n 개의 {KEY}와 모두 비교되어 n x n 표를 만들어 {QC}이 된다.",
              f"계산은 O(n 제곱 x d), 메모리는 O(n 제곱) 이에요. {ASC} 표가 n x n 이라서예요.",
              "n 개가 n 개를 다 본다 = n 제곱 으로 외워요."),
      warn("헷갈리기 쉬운 점",
           f"{PAR}는 얻은 것이고 {QC}은 잃은 것이에요. 맞바꾸기예요.",
           "RNN 이 무조건 더 싼 게 아니에요. RNN 은 순차 연산 O(n) 때문에 시간이 오래 걸려요.")])

# ---------------------------------------------------------------- p.56
page(56, "정말 잘 됐나요, WMT 결과",
     ["Transformer", "BLEU", "Machine Translation (MT)", "Recurrent Neural Network (RNN)",
      "Convolutional Neural Network (CNN)", "Parallelization"],
     [say(f"2017년 {TRF} 논문이 낸 {MT} 성적이에요.",
          "WMT 2014 영어에서 독일어로 번역하는 과제예요.",
          "이전 방법을 모두 이겼고, 학습 비용은 훨씬 적었어요."),
      compare("WMT 2014 영어 -> 독일어 결과 (슬라이드 막대)",
              ["모델", "BLEU (높을수록 좋음)", "학습 비용 (GPU 일수)"],
              ["GNMT (RNN)", "24.6", "96"],
              ["ConvSeq2Seq (CNN)", "25.2", "175"],
              ["Transformer base", "27.3", "3.3"],
              ["Transformer big", "28.4", "8.3"]),
      points("한 줄 요약",
             f"{BLEU}는 24.6 에서 28.4 로 올랐어요",
             "학습 비용은 96 GPU 일에서 3.3 GPU 일로 줄었어요",
             "더 좋으면서 동시에 더 쌌기 때문에 1년 만에 판이 바뀌었어요")],
     [compare("슬라이드 영어와 우리말 뜻",
              ["영어 원문", "뜻"],
              ["WMT 2014 English to German", "WMT 2014 영어에서 독일어로"],
              ["the Transformer beat every previous system, including large ensembles",
               "트랜스포머가 큰 앙상블까지 포함해 이전 시스템을 모두 이겼다"],
              ["and trained in a fraction of the time",
               "게다가 학습 시간은 아주 일부밖에 안 걸렸다"],
              ["The cost column is the part people underestimated",
               "사람들이 과소평가한 것은 비용 쪽이다"],
              ["cheaper training means more experiments, which means faster progress",
               "학습이 싸면 실험을 더 많이 하고, 그러면 더 빨리 발전한다"]),
      points("용어 하나씩",
             f"{BLEU}: 번역문이 사람 번역과 n-gram 이 얼마나 겹치는지 재는 점수예요",
             "앙상블: 모델 여러 개의 답을 합쳐서 쓰는 방법이에요",
             "GPU 일수: GPU 한 대를 하루 돌린 것을 1 로 세는 학습 비용 단위예요"),
      check(f"{BLEU}는 높을수록 어떤가요",
            ["좋아요", "나빠요", "상관없어요", "0 이 제일 좋아요"], 0,
            "사람 번역과 많이 겹칠수록 높아요. 2주차와 이번 주에 계속 나왔어요.")],
     [look("슬라이드를 짚어 읽어요",
           (0.06, 0.199, 0.87, 0.070, "첫 점: 큰 앙상블까지 다 이겼고, 학습 시간은 아주 일부였다."),
           (0.06, 0.287, 0.87, 0.029, "둘째 점: 사람들이 과소평가한 것은 비용 쪽이다."),
           (0.10, 0.386, 0.35, 0.399, "왼쪽 막대: BLEU 24.6, 25.2, 27.3, 28.4. 진한 두 개가 트랜스포머."),
           (0.52, 0.386, 0.41, 0.399, "오른쪽 막대: 학습 비용 96, 175, 3.3, 8.3 GPU 일. 세로축이 로그예요."),
           (0.25, 0.863, 0.50, 0.030, "맨 아래: 더 좋고 동시에 더 쌌다, 그래서 1년 만에 분야가 옮겨 갔다.")),
      steps("숫자로 차이를 세어 봐요",
            ["BLEU 는 GNMT 24.6 에서 Transformer big 28.4 로 올랐어요",
             "차이는 28.4 빼기 24.6 = 3.8 점이에요",
             "학습 비용은 GNMT 96 GPU 일, Transformer base 3.3 GPU 일이에요",
             "96 나누기 3.3 = 약 29.1 배 싸요",
             "ConvSeq2Seq 175 와 Transformer big 8.3 을 비교하면 약 21.1 배예요",
             "GNMT 96 과 Transformer big 8.3 을 비교하면 약 11.6 배예요"],
            "점수는 3.8 점 올리면서 비용은 20배에서 30배 줄였어요.",
            "슬라이드 막대의 숫자"),
      prof("교수님: 기존 RNN 이나 CNN 기반이 24, 25 이렇게 됐는데 트랜스포머가 27, 28까지 올렸어요.",
           "교수님: 초창기 트랜스포머 치고는 이 정도면 꽤 큰 차이로 올린 거예요.",
           "교수님: RNN 은 토큰을 순서대로 처리해야 하는데 트랜스포머는 시퀀스 전체를 큰 행렬 연산으로 한꺼번에 처리해요.",
           "교수님: 그래서 계산 비용이 줄어들 수 있다는 거죠."),
      bg("기초 다지기 5단원",
         f"{BLEU}는 0 에서 100 사이 점수예요. 사람 번역과 n-gram 이 겹치는 비율로 계산해요.",
         "번역 과제에서 1점만 올려도 큰 차이라고 봐요.",
         "그래서 3.8 점 차이는 아주 큰 격차예요.")],
     [check("Transformer base 의 학습 비용은 GNMT 의 몇 분의 1쯤인가요",
            ["약 29분의 1", "약 2분의 1", "약 3배", "같아요"], 0,
            "96 나누기 3.3 = 약 29.1 이에요."),
      exam("예상 문제",
           "WMT 2014 영어 독일어 결과에서 트랜스포머가 중요한 이유를 두 가지로 쓰시오.",
           "점수와 비용, 두 축을 같이 봐야 해요.",
           ["첫째, 성능이 올랐어요. BLEU 24.6 에서 28.4 로 3.8 점 올랐어요",
            "둘째, 학습 비용이 줄었어요. 96 GPU 일에서 3.3 GPU 일로 약 29배 줄었어요",
            "큰 앙상블 모델까지 이겼다는 점도 함께 써요",
            "싸지면 실험을 더 많이 할 수 있고, 그래서 발전이 빨라져요"],
           "더 좋으면서 동시에 더 싸다는 점이 분야를 1년 만에 바꾼 이유예요."),
      english("답안 문장",
              f"{TRF}는 WMT 2014 영어 독일어에서 {BLEU} 28.4 로 이전 방법을 모두 이겼다.",
              f"{RNN} 기반은 24.6, {CNN} 기반은 25.2 였어요. 비용도 96 에서 3.3 GPU 일로 줄었어요.",
              "24.6, 25.2, 27.3, 28.4 를 순서대로 외워요."),
      warn("헷갈리기 쉬운 점",
           "오른쪽 비용 그래프의 세로축은 로그예요. 막대 길이를 그대로 비율로 읽으면 안 돼요.",
           f"{BLEU}는 높을수록 좋고, 학습 비용은 낮을수록 좋아요. 방향이 반대예요.")])

# ---------------------------------------------------------------- p.57
page(57, "트랜스포머가 이긴 이유 네 가지",
     ["Transformer", "LSTM", "Parallelization", "Self-Attention", "BERT", "GPT",
      "Token", "Recurrent Neural Network (RNN)"],
     [say(f"{TRF}가 {LSTM}보다 똑똑해 보이는 구조는 아니에요.",
          "이긴 이유는 네 가지 성질이 서로 곱해져서 커졌기 때문이에요.",
          "병렬화, 짧은 경로, 잘 쌓임, 과제와 무관함. 이 네 개예요."),
      figure("네 가지 성질", FIG_WHY,
             "슬라이드의 네 상자를 그대로 옮긴 것이에요. 아래는 같은 블록이 어디까지 갔는지예요.", 5),
      points("한 줄 요약",
             f"{PAR}: 모든 자리를 한꺼번에 계산해요",
             "짧은 경로: 어떤 두 토큰도 한 층에서 만나요",
             "잘 쌓임: 똑같은 블록을 12층이나 96층으로",
             "과제 무관: 글, 그림, 소리, 단백질까지 같은 블록")],
     [compare("슬라이드 영어와 우리말 뜻",
              ["영어 원문", "뜻"],
              ["The architecture is not obviously smarter than an LSTM",
               "이 구조가 LSTM 보다 딱히 똑똑한 것은 아니다"],
              ["It won because of four properties that compound",
               "네 가지 성질이 서로 곱해지며 커져서 이겼다"],
              ["Parallelism: all positions are computed at once",
               "병렬성: 모든 자리가 한꺼번에 계산된다"],
              ["Short paths: any two tokens meet in a single layer",
               "짧은 경로: 어떤 두 토큰도 한 층 안에서 만난다"],
              ["Scales cleanly: one uniform block, stacked 12x or 96x",
               "깔끔한 확장: 똑같은 블록 하나를 12번이나 96번 쌓는다"],
              ["Task-agnostic: text, vision, audio, proteins, same block",
               "과제 무관: 글, 시각, 소리, 단백질에 같은 블록"]),
      points("용어 하나씩",
             f"{PAR}: 여러 계산을 한꺼번에 동시에 하기예요",
             f"{LSTM}: 게이트를 달아 기억을 오래 들고 가게 만든 {RNN}이에요",
             "compound: 이자가 불어나듯 서로 곱해져서 효과가 커진다는 뜻이에요"),
      check("네 가지 성질에 들어가지 않는 것은",
            ["메모리를 적게 쓴다", "병렬화", "짧은 경로", "과제와 무관"], 0,
            "메모리는 오히려 이차 비용 때문에 더 써요. 이건 값을 치르는 쪽이에요.")],
     [look("슬라이드를 짚어 읽어요",
           (0.06, 0.199, 0.75, 0.032, "첫 점: LSTM 보다 딱히 똑똑하지는 않은데 네 성질이 겹쳐서 이겼다."),
           (0.07, 0.415, 0.21, 0.249, "첫 상자 Parallelism: 모든 자리가 한꺼번에 계산된다."),
           (0.29, 0.415, 0.21, 0.249, "둘째 상자 Short paths: 어떤 두 토큰도 한 층에서 만난다."),
           (0.51, 0.415, 0.21, 0.249, "셋째 상자 Scales cleanly: 같은 블록을 12번이나 96번 쌓는다."),
           (0.72, 0.415, 0.21, 0.249, "넷째 상자 Task-agnostic: 글, 시각, 소리, 단백질에 같은 블록."),
           (0.09, 0.694, 0.82, 0.030, "아래 글씨: 같은 블록이 BERT(2018), GPT(2018-), ViT(2020), AlphaFold(2021) 가 됐다.")),
      compare("네 가지 성질과 그 근거",
              ["성질", "왜 그런가"],
              ["병렬화", "RNN 처럼 앞 계산을 기다리지 않고 한 번의 행렬 곱으로 처리해요"],
              ["짧은 경로", "셀프 어텐션은 최대 경로 길이가 O(1) 이에요"],
              ["잘 쌓임", "잔차 연결과 LayerNorm 덕분에 깊게 쌓아도 학습돼요"],
              ["과제 무관", "토큰 시퀀스로 바꿀 수 있으면 무엇이든 같은 블록을 써요"]),
      prof("교수님: 첫 번째는 병렬화고요. RNN 처럼 앞 토큰의 계산을 기다리지 않아도 됩니다.",
           "교수님: 두 번째는 짧은 경로죠. 멀리 떨어진 두 토큰도 한 레이어 안에서 직접 연결됩니다.",
           "교수님: 세 번째는 확장성이에요. 트랜스포머 블록이 레고 블록처럼 생겨서 계속 쌓을 수 있어요.",
           "교수님: 네 번째는 태스크 어그노스틱. 어그노스틱은 상관이 없다는 뜻이에요."),
      bg("기초 다지기 10단원",
         "GPU 는 큰 행렬 곱 하나를 아주 빠르게 해요. 대신 순서대로 하나씩 하는 일은 느려요.",
         f"{TRF}는 문장 전체를 큰 행렬 곱으로 만들어서 GPU 의 장점에 딱 맞아요.",
         "그래서 GPU 가 좋아질수록 트랜스포머가 더 유리해졌어요.")],
     [check("슬라이드가 든 같은 블록의 후손이 아닌 것은",
            ["word2vec", "BERT", "GPT", "AlphaFold"], 0,
            "word2vec 은 2주차에 배운 단어 벡터 방법이에요. 트랜스포머 이전이에요."),
      exam("예상 문제",
           "트랜스포머가 널리 쓰이게 된 네 가지 성질을 쓰고 각각 설명하시오.",
           "네 개를 이름과 한 줄 설명으로 적으면 돼요.",
           ["병렬화: 모든 위치를 한꺼번에 계산해서 GPU 를 잘 쓴다",
            "짧은 경로: 아무리 멀리 떨어진 두 토큰도 한 층에서 직접 연결된다",
            "확장성: 똑같은 블록을 12층, 96층으로 깔끔하게 쌓을 수 있다",
            "과제 무관: 글, 그림, 소리, 단백질까지 같은 블록으로 처리한다"],
           "이 네 가지가 서로 곱해지며 커져서 트랜스포머가 이겼어요."),
      english("답안 문장",
              f"{TRF}가 이긴 이유는 {PAR}, 짧은 경로, 깔끔한 확장성, 과제 무관성 네 가지이다.",
              f"두 {TOK}가 한 층에서 만나고, 같은 블록을 12층이나 96층으로 쌓을 수 있어요.",
              "병렬, 짧은 경로, 확장, 무관 네 글자씩 끊어 외워요."),
      warn("헷갈리기 쉬운 점",
           f"{TRF}가 {LSTM}보다 '똑똑해서' 이긴 게 아니에요. 슬라이드가 직접 아니라고 말해요.",
           "과제 무관은 아무 데이터나 바로 넣어도 된다는 뜻이 아니에요. 토큰 시퀀스로 바꿀 수 있으면 같은 블록을 쓴다는 뜻이에요.")])

# ---------------------------------------------------------------- p.58
page(58, "Check Yourself 2: 스스로 확인하기",
     ["Self-Attention", "Cross-Attention", "Causal Masking", "Softmax",
      "Scaled Dot-Product Attention", "Position-wise Feed-Forward Network (FFN)",
      "Parameter", "Permutation Equivariance", "Positional Encoding", "Quadratic Cost",
      "Query", "Key", "Value", "Attention Score", "Multi-Head Attention (MHA)"],
     [say("4장까지 다 들었는지 확인하는 쪽이에요. 여섯 문제예요.",
          "교수님이 수업에서 여섯 개 답을 하나하나 말해 주었어요.",
          "시험 대비 1순위 쪽이에요. 여섯 개를 말로 설명할 수 있으면 4강은 끝이에요."),
      points("여섯 문제를 우리말로",
             f"1. {SA}과 2장의 어텐션은 정확히 무엇이 다른가",
             f"2. 마스크는 왜 {SMX} 앞에 걸어야 하는가",
             "3. 왜 루트 d_k 로 나누는가, 안 나누면 무엇이 잘못되는가",
             f"4. {TRF}의 {PARAM}는 어텐션과 {FFN} 중 어디에 더 많은가",
             f"5. 순수 {SA}의 세 가지 벽과 각각의 해결책은",
             f"6. 어텐션은 왜 O(n 제곱) 인가, 피하려는 연구 한 줄기를 들어라")],
     [compare("슬라이드 영어와 우리말 뜻",
              ["영어 원문", "뜻"],
              ["What exactly is the difference between self-attention and the attention of section 2",
               "셀프 어텐션과 2장의 어텐션은 정확히 무엇이 다른가"],
              ["Why must the mask be applied before the softmax and not after",
               "왜 마스크를 소프트맥스 뒤가 아니라 앞에 걸어야 하는가"],
              ["Why divide by the square root of d_k, and what goes wrong if you forget",
               "왜 루트 d_k 로 나누고, 잊으면 무엇이 잘못되는가"],
              ["Where do most of a Transformer's parameters live",
               "트랜스포머의 파라미터는 대부분 어디에 있는가"],
              ["Name the three barriers of plain self-attention and the component that fixes each",
               "순수 셀프 어텐션의 세 가지 벽과 각각을 고치는 부품을 대라"],
              ["Why is attention O(n squared), and name one line of work that tries to avoid it",
               "어텐션은 왜 O(n 제곱) 인가, 이를 피하려는 연구 한 줄기를 대라"])],
     [look("슬라이드의 여섯 문제를 짚어 읽어요",
           (0.06, 0.211, 0.60, 0.034, "1번: 셀프 어텐션과 2장 어텐션의 차이. p.53 에서 답을 봤어요."),
           (0.06, 0.276, 0.52, 0.034, "2번: 마스크를 왜 소프트맥스 앞에 거는가."),
           (0.06, 0.339, 0.46, 0.034, "3번: 왜 루트 d_k 로 나누는가."),
           (0.06, 0.403, 0.69, 0.034, "4번: 파라미터가 어텐션에 많은가 피드포워드에 많은가."),
           (0.06, 0.468, 0.62, 0.034, "5번: 순수 셀프 어텐션의 세 가지 벽과 해결책."),
           (0.06, 0.532, 0.53, 0.034, "6번: 어텐션이 O(n 제곱) 인 이유와 피하려는 연구.")),
      steps("4번 답을 숫자로 확인해 봐요",
            ["어텐션 쪽: W^Q, W^K, W^V, W^O 네 개예요",
             "d = 512 이면 4 x 512 x 512 = 1048576, 약 105만 개",
             "FFN 은 속 차원을 4d = 2048 로 넓혔다 줄여요",
             "올라가는 표: 512 x 2048 = 1048576",
             "내려오는 표: 2048 x 512 = 1048576, 합쳐서 2097152",
             "약 210만 개. 어텐션의 정확히 두 배예요"],
            "FFN 이 어텐션보다 파라미터가 더 많아요. 두 배예요.",
            "d = 512, d_ff = 4d = 2048"),
      prof("교수님(1번): 계산 방법은 같다. 다만 쿼리 키 밸류가 어디서 나오냐에 차이가 있다.",
           "교수님(2번): 마스크는 점수를 음의 무한대로 바꾸는 것이고, 소프트맥스를 쳤을 때 0 이 되게 하려는 거니까 당연히 앞이죠.",
           "교수님(3번): d_k 가 커지면 점수의 분산이 커지고, 소프트맥스가 거의 원-핫이 돼서 기울기가 작아져요.",
           "교수님(4번): 이 논문에서는 d_ff 를 4d 로 설정했으니까 FFN 이 어텐션 프로젝션보다 훨씬 많습니다."),
      prof("교수님(5번): 첫째는 순서를 모른다, 그래서 위치 인코딩. 원 논문은 사인 코사인을 씁니다.",
           "교수님(5번): 둘째는 각 토큰을 깊게 비선형 처리하는 부분이 부족하다, 그래서 위에 FFN 을 둡니다.",
           "교수님(5번): 셋째는 미래 토큰을 봐 버릴 수 있다, 그래서 인과 마스킹을 했다.",
           "교수님(6번): n 개의 쿼리와 n 개의 키가 전부 비교돼야 해서 n x n 을 계산해야 합니다.")],
     [exam("N4 Check Yourself",
           "Q1 ~ Q3 (Part 2)",
           "교수님이 수업에서 말해 준 답을 한 줄씩 정리해요.",
           [f"1. 계산은 똑같고, {QRY}, {KEY}, {VAL}가 어디서 나오는지만 달라요",
            f"1. 2장의 {CA}은 Q 가 디코더, K 와 V 가 인코더. {SA}은 셋 다 같은 시퀀스",
            f"2. {CM}은 {ASC}를 음의 무한대로 바꾸는 것이라, {SMX} 뒤에 하면 이미 0 이 아닌 값이 섞여요",
            "2. 소프트맥스 앞에 걸어야 그 자리의 가중치가 정확히 0 이 돼요",
            "3. d_k 가 커지면 내적 점수의 분산이 커져서 소프트맥스가 거의 원-핫이 돼요",
            "3. 그러면 기울기가 작아지고 표현력도 약해져요. 그래서 루트 d_k 로 나눠 스케일을 맞춰요"],
           "1번은 Q, K, V 의 출처, 2번은 0 을 만들기 위해, 3번은 분산을 맞추기 위해예요."),
      exam("N4 Check Yourself",
           "Q4 ~ Q6 (Part 2)",
           "나머지 세 문제의 답이에요.",
           [f"4. {FFN}이 어텐션보다 많아요. d_ff 를 4d 로 잡기 때문이에요",
            "4. d = 512 면 어텐션 약 105만 개, FFN 약 210만 개로 두 배예요",
            f"5. 벽 1은 순서를 모름({PEQ}) -> {PE}",
            f"5. 벽 2는 토큰별 비선형 처리 부족 -> {FFN}",
            f"5. 벽 3은 미래 토큰을 봄 -> {CM}",
            f"6. n 개 쿼리가 n 개 키와 전부 비교돼서 n x n 이에요. 슬라이딩 윈도우 어텐션 같은 연구가 있어요"],
           "5번 세 벽은 순서, 비선형, 미래 엿보기. 해결은 위치 인코딩, FFN, 마스킹이에요."),
      check("마스크를 소프트맥스 뒤에 걸면 무엇이 잘못되나요",
            ["가중치 합이 1 이 안 되고 미래 정보가 이미 섞여요", "계산이 느려져요",
             "파라미터가 늘어나요", "아무 문제 없어요"], 0,
            "교수님: 음의 무한대로 바꾸는 이유가 소프트맥스를 쳤을 때 0 이 되게 하려는 거니까 당연히 앞에 해야죠."),
      check(f"{TRF}의 {PARAM}가 더 많은 쪽은",
            [f"{FFN}", "어텐션 프로젝션", "위치 인코딩", "LayerNorm 의 감마와 베타"], 0,
            "d_ff = 4d 이기 때문에 FFN 이 어텐션의 두 배예요. 교수님이 직접 답한 문제예요."),
      english("답안 문장",
              f"{SA}의 세 벽은 순서, 비선형, 미래 엿보기. 답은 {PE}, {FFN}, {CM}.",
              "5번은 세 쌍을 짝지어 외우면 그대로 답안이 돼요.",
              "순서-위치, 깊이-FFN, 미래-마스크 로 외워요."),
      warn("시험에 나올 만한 곳",
           "Check Yourself 는 교수님이 직접 낸 문제이고, 여섯 개 답을 수업에서 다 말해 줬어요.",
           "슬라이드 맨 아래가 말해요. 블록을 외워서 그릴 수 있으면 실습 준비가 된 거예요.",
           "3번의 '분산이 커진다' 와 4번의 '4d' 는 숫자로 물어볼 수 있어요.")])

# ---------------------------------------------------------------- p.59
page(59, "마무리: 오늘 배운 것, Lab 3, 팀 프로젝트",
     ["Sequence-to-Sequence Model", "Information Bottleneck", "Attention", "Softmax",
      "Weighted Sum", "Self-Attention", "Query", "Key", "Value",
      "Scaled Dot-Product Attention", "Positional Encoding",
      "Position-wise Feed-Forward Network (FFN)", "Causal Masking",
      "Transformer", "Multi-Head Attention (MHA)", "Residual Connection",
      "Layer Normalization (LayerNorm)", "Quadratic Cost", "Pre-training",
      "Recurrent Neural Network (RNN)", "Encoder", "Decoder"],
     [say("오늘 하루를 네 줄로 정리하는 쪽이에요.",
          f"{S2S}, {ATT}, {SA}, {TRF} 순서로 달려왔어요.",
          f"그리고 Lab 3 과 팀 프로젝트 안내, 다음 주 {PRE} 예고가 있어요."),
      figure("오늘 하루를 한 줄로", FIG_WRAP,
             "병목을 어텐션이 풀고, 어텐션이 셀프 어텐션이 되고, 거기에 세 장치를 더해 트랜스포머가 됐어요.", 5),
      points("네 줄 요약",
             f"{S2S}: RNN 두 개와 다리 벡터 하나, 그 벡터가 {IB}이에요",
             f"{ATT}: 점수 -> {SMX} -> {WSUM}으로 {CTX}를 만들어요",
             f"{SA}: 한 시퀀스에서 Q, K, V 를 만들고 {SDPA}을 써요",
             f"{TRF}: {MHA} + {RES} + {LN}, 값은 O(n 제곱)")],
     [compare("슬라이드 영어와 우리말 뜻",
              ["영어 원문", "뜻"],
              ["Seq2Seq: two RNNs, one bridge vector, and that vector is a bottleneck",
               "seq2seq 은 RNN 두 개와 다리 벡터 하나인데 그 벡터가 병목이다"],
              ["Attention: score, softmax, weighted sum, removes the bottleneck",
               "어텐션은 점수, 소프트맥스, 가중합이고 병목을 없앤다"],
              ["learns alignment for free", "정렬을 공짜로 배운다"],
              ["Self-attention: Q/K/V from one sequence, scaled dot product",
               "셀프 어텐션은 한 시퀀스에서 Q/K/V 를 만들고 스케일드 내적을 쓴다"],
              ["needs positional encoding, an FFN and a mask",
               "위치 인코딩, FFN, 마스크가 필요하다"],
              ["Transformer: multi-head + residual + LayerNorm, O(n squared) is the price",
               "트랜스포머는 멀티 헤드 + 잔차 + LayerNorm 이고 값은 n 제곱이다"]),
      points("Lab 3 과 팀 프로젝트",
             "Lab 3 (1시간): NumPy 와 PyTorch 로 셀프 어텐션을 바닥부터 만들어요",
             f"Q/K/V, 마스크, {MHA}, 실제 어텐션 지도 보기까지 해요",
             "팀 프로젝트: 4명 한 조를 만들고 조원과 한 줄짜리 주제를 다음 주까지 보내요"),
      points("다음 주 예고",
             f"다음 주 주제는 {PRE}이에요",
             "블록은 오늘 것과 똑같고, 모든 것에 대해 학습시켜요",
             "슬라이드 표현으로 the same block, trained on everything 이에요")],
     [look("슬라이드를 짚어 읽어요",
           (0.06, 0.211, 0.55, 0.034, "첫 줄 Seq2Seq: RNN 두 개, 다리 벡터 하나, 그게 병목이다."),
           (0.06, 0.276, 0.70, 0.034, "둘째 줄 Attention: 점수, 소프트맥스, 가중합. 병목 제거, 정렬 학습."),
           (0.06, 0.339, 0.78, 0.034, "셋째 줄 Self-attention: Q/K/V, 스케일드 내적, 위치 인코딩과 FFN 과 마스크."),
           (0.06, 0.403, 0.70, 0.034, "넷째 줄 Transformer: 멀티 헤드 + 잔차 + LayerNorm, O(n 제곱) 이 값."),
           (0.06, 0.468, 0.87, 0.082, "다섯째 줄 Lab 3: NumPy 와 PyTorch 로 셀프 어텐션을 바닥부터."),
           (0.06, 0.586, 0.68, 0.034, "여섯째 줄 Project: 4인 조를 만들고 조원과 한 줄 주제를 다음 주까지.")),
      compare("네 챕터를 한 표로",
              ["챕터", "핵심", "남은 문제"],
              ["1. seq2seq", "인코더 RNN 과 디코더 RNN", "고정 크기 벡터가 정보 병목"],
              ["2. 어텐션", "점수, 소프트맥스, 가중합", "아직 RNN 이라 순차 계산"],
              ["3. 셀프 어텐션", "Q, K, V 가 한 시퀀스에서, 병렬 계산", f"{PEQ}, 비선형, 미래 엿보기"],
              ["4. 트랜스포머", "멀티 헤드, 잔차, LayerNorm", "O(n 제곱) 이차 비용"]),
      prof("교수님: 인코더 RNN 이 고정 크기 벡터 하나로 정보를 다 전달하는 병목을 어텐션이 해결해 줬고요.",
           "교수님: 어텐션에서 셀프 어텐션으로 나아가서 병렬적인 개념을 적용했고요.",
           "교수님: 마지막으로 멀티 헤드 어텐션이랑 잔차, 레이어 놈까지 배워봤습니다.",
           "교수님: 트랜스포머라는 개념을 완벽하게 다 설명을 드렸습니다."),
      prof("교수님: 이 Attention Is All You Need 논문은 인공지능 학과로서 매우 중요한 논문입니다.",
           "교수님: 회사 면접에서 가장 기억에 남는 논문이 뭐냐고 물으면 저는 이 논문을 추천할 수 있어요.",
           "교수님: 읽어서 이해를 하면 제 수업도 이해가 되고 시험도 나중에 잘 볼 수 있어요.",
           "교수님: 실습은 풀 코드 아웃풋까지 찍어서 올려놨으니 복습을 나중에 해 보시면 좋겠습니다."),
      prof("교수님(팀 프로젝트): 4인 1조, 자유 주제로 숏 페이퍼 한 편 쓰는 느낌입니다.",
           "교수님: 문제 정의, 가설과 메인 실험 하나, 추가 분석 최소 3개 이상, 리미테이션으로 구성해요.",
           "교수님: 메인 실험 하나에 최소 3개 이상 분석을 해주셔야 좋은 점수를 받습니다.",
           "교수님: 리미테이션은 약점을 숨기는 부분이 아니라 실험을 얼마나 잘 이해했는지 보여 주는 항목이에요.",
           when="4주차 월요일 3교시")],
     [check(f"오늘 {TRF}에 더한 세 가지 장치는",
            [f"{MHA}, {RES}, {LN}",
             "위치 인코딩, FFN, 마스크",
             "쿼리, 키, 밸류",
             "점수, 소프트맥스, 가중합"], 0,
            "4장에서 더한 세 가지예요. 두 번째 보기는 3장에서 더한 것이에요."),
      check("다음 주에 배울 주제는",
            [f"{PRE}", "토큰화", "빔 서치", "경사 하강법"], 0,
            "슬라이드 맨 아래: Next week: pretraining, the same block, trained on everything."),
      exam("예상 문제",
           "seq2seq 에서 트랜스포머까지의 발전 과정을 네 단계로 설명하시오.",
           "오늘 배운 순서를 그대로 쓰면 돼요.",
           ["1단계 seq2seq: 인코더 RNN 과 디코더 RNN, 고정 크기 벡터 하나가 정보 병목이었어요",
            "2단계 어텐션: 점수, 소프트맥스, 가중합으로 병목을 없애고 정렬도 공짜로 배웠어요",
            "3단계 셀프 어텐션: Q, K, V 를 한 시퀀스에서 만들어 병렬 계산이 가능해졌어요",
            "3단계의 세 가지 벽은 위치 인코딩, FFN, 인과 마스킹으로 막았어요",
            "4단계 트랜스포머: 멀티 헤드, 잔차 연결, LayerNorm 을 더해 깊게 쌓을 수 있게 됐어요"],
           "병목 -> 어텐션 -> 셀프 어텐션 -> 트랜스포머. 값은 O(n 제곱) 이에요."),
      english("답안 문장",
              f"{TRF}는 {SA}에 세 장치를 더해 깊게 쌓을 수 있게 만든 구조이다.",
              f"세 장치는 {MHA}, {RES}, {LN} 이에요.",
              f"얻은 것은 병렬, 치른 값은 {QC}. 이렇게 짝으로 외워요."),
      warn("잊지 말 것",
           "팀 프로젝트는 4명 한 조이고, 조원과 한 줄 주제를 다음 주까지 보내야 해요.",
           "Lab 3 은 수업에서 건너뛰었어요. 교수님이 출력까지 찍어 올려놨으니 혼자 복습하세요.",
           "Attention Is All You Need 논문을 꼭 읽어 보라고 교수님이 여러 번 강조했어요.")])

data = {"deck": "N4", "from": 46, "to": 59,
        "glossary": [{"ko": k, "en": e, "say": s, "more": m} for k, e, s, m in GLOSSARY],
        "slides": S}

raw = json.dumps(data, ensure_ascii=False, indent=1)
for ch in ("—", "–", "·", "・"):
    assert ch not in raw, ch
with open(OUT, "w", encoding="utf-8") as f:
    f.write(raw)
print("saved", OUT, len(S), "pages")
