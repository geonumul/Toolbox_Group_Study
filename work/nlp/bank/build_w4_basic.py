# -*- coding: utf-8 -*-
"""4주차(N4 Attention and the Transformer Architecture + N4L Lab 3) basic 문제은행 생성기.
출력: work/nlp/bank/w4_basic.json
계산 문항 정답은 아래에서 numpy/python 으로 실제 계산하고 assert 로 확인한다."""
import json, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "w4_basic.json")

U1 = "4-1 seq2seq 와 정보 병목"
U2 = "4-2 학습과 디코딩"
U3 = "4-3 어텐션 세 단계와 네 식"
U4 = "4-4 어텐션의 이득과 점수 함수"
U5 = "4-5 셀프 어텐션과 쿼리 키 밸류"
U6 = "4-6 스케일드 닷프로덕트와 세 배리어"
U7 = "4-7 위치 인코딩, FFN, 인과 마스킹"
U8 = "4-8 트랜스포머 블록과 그 대가"


# =====================================================================
# 계산 확인 (numpy)
# =====================================================================
def softmax(a):
    a = np.asarray(a, dtype=float)
    e = np.exp(a - a.max(axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


# C1 내적 점수
s_vec = np.array([1.0, 2.0])
H = np.array([[3.0, 0.3], [0.4, 0.2], [0.1, 0.2], [0.2, 0.1]])
C1 = H @ s_vec
assert [round(float(v), 2) for v in C1] == [3.6, 0.8, 0.5, 0.4]

# C2 소프트맥스
C2 = softmax([2.0, 1.0, 0.0])
assert [round(float(v), 4) for v in C2] == [0.6652, 0.2447, 0.0900]
assert round(float(C2.sum()), 10) == 1.0

# C3 가중합 (문맥 벡터)
w3 = np.array([0.5, 0.3, 0.2])
Hs = np.array([[2.0, 0.0], [0.0, 2.0], [1.0, 1.0]])
C3 = w3 @ Hs
assert [round(float(v), 4) for v in C3] == [1.2, 0.8]

# C4 루트 d_k 로 나누기
C4_raw, C4_dk = 12.0, 64
C4 = C4_raw / math.sqrt(C4_dk)
assert C4 == 1.5 and math.sqrt(64) == 8.0

# C5 shape
C5_n, C5_dk, C5_dv = 6, 8, 4
assert (np.zeros((C5_n, C5_dk)) @ np.zeros((C5_dk, C5_n))).shape == (6, 6)
assert (np.zeros((C5_n, C5_n)) @ np.zeros((C5_n, C5_dv))).shape == (6, 4)

# C6 멀티 헤드
C6_d, C6_h = 512, 8
assert C6_d // C6_h == 64
assert C6_h * (C6_d * (C6_d // C6_h)) == C6_d * C6_d == 262144

# C7 FFN 파라미터
C7_d = 512
C7_dff = 4 * C7_d
C7_w1 = C7_d * C7_dff
C7_w2 = C7_dff * C7_d
assert C7_dff == 2048 and C7_w1 == 1048576 and C7_w1 + C7_w2 == 2097152

# C8 n 제곱 비용
assert 512 ** 2 == 262144
assert 1024 ** 2 == 1048576
assert (1024 ** 2) / (512 ** 2) == 4.0

# C9 빔 서치 길이 정규화
capA = [-0.2, -0.5, -0.3]          # 3 토큰
capB = [-0.1, -0.4, -0.6, -0.5]    # 4 토큰
sumA, sumB = sum(capA), sum(capB)
assert round(sumA, 4) == -1.0 and round(sumB, 4) == -1.6
normA, normB = sumA / len(capA), sumB / len(capB)
assert round(normA, 4) == -0.3333 and round(normB, 4) == -0.4
assert sumA > sumB and normA > normB

# C10 위치 인코딩
def pe(pos, i, d):
    ang = pos / (10000 ** (2 * i / d))
    return round(math.sin(ang), 4), round(math.cos(ang), 4)


assert pe(0, 0, 4) == (0.0, 1.0)
assert pe(1, 0, 4) == (0.8415, 0.5403)
assert pe(1, 1, 4) == (0.01, 1.0)

bank = []
cnt = {}


def add(t, unit, slides, src=None, **kw):
    cnt[t] = cnt.get(t, 0) + 1
    item = {"id": f"w4b-{t}-{cnt[t]:03d}", "type": t, "part": "4", "level": "basic",
            "unit": unit, "slides": slides}
    if src:
        item["src"] = src
    item.update(kw)
    bank.append(item)


def mcq(unit, slides, q, c, a, e, src="예상"):
    add("mcq", unit, slides, src, q=q, c=c, a=a, e=e)


def ox(unit, slides, q, a, e, src="예상"):
    add("ox", unit, slides, src, q=q, a=a, e=e)


def short(unit, slides, q, a, e, src="예상", num=False, tol=None):
    kw = dict(q=q, a=a, e=e)
    if num:
        kw["num"] = True
        kw["tol"] = tol if tol is not None else 0.01
    add("short", unit, slides, src, **kw)


def essay(unit, slides, model, q, answer, points, src="예상"):
    add("essay", unit, slides, src, model=model, q=q, answer=answer, points=points)


def calc(unit, slides, model, q, qko, blanks, steps, answer, e, src="예상"):
    add("calc", unit, slides, src, model=model, q=q, qko=qko, blanks=blanks,
        steps=steps, answer=answer, e=e)


# =====================================================================
# MCQ (32)
# =====================================================================
mcq(U1, "N4 p.9",
    "**시퀀스-투-시퀀스 모델(Sequence-to-Sequence Model)** 의 구조로 가장 적절한 것은?",
    ["RNN 하나가 입력과 출력을 모두 처리한다",
     "**인코더(Encoder)** RNN 이 원문을 벡터 하나로 압축하고 **디코더(Decoder)** RNN 이 그 벡터를 조건으로 문장을 생성한다",
     "인코더가 문장을 만들고 디코더가 문장을 읽는다",
     "인코더와 디코더가 서로 다른 손실 함수로 따로 학습된다"],
    1,
    "슬라이드: 'Two RNNs. The encoder reads the source and compresses it into a vector. The decoder is a language model that generates the target, conditioned on that vector.' 손실은 하나이고 **종단간 학습(End-to-End)** 으로 함께 학습돼요.")

mcq(U1, "N4 p.16",
    "**정보 병목(Information Bottleneck)** 을 가장 잘 설명한 것은?",
    ["디코더가 너무 많은 단어를 본다",
     "원문의 모든 정보가 고정 크기 벡터 하나를 지나야 한다",
     "인코더의 층이 너무 얕다",
     "학습 데이터가 부족하다"],
    1,
    "슬라이드: 'Everything the decoder knows about the source has to fit in one fixed-size vector.' 20단어 문장과 200단어 문단이 같은 칸 수를 받아요.")

mcq(U1, "N4 p.16",
    "고정 크기 벡터 하나가 짧은 문장보다 긴 문장에서 더 문제가 되는 이유로 가장 적절한 것은?",
    ["긴 문장은 어휘가 더 어렵기 때문",
     "입력 길이가 늘어도 디코더로 전달되는 벡터의 크기가 그대로라 압축 손실이 커지기 때문",
     "긴 문장은 **토큰(Token)** 이 많아 학습 속도가 느리기 때문",
     "긴 문장은 **교사 강요(Teacher Forcing)** 를 쓸 수 없기 때문"],
    1,
    "교수님이 p.29 확인 문제 1번의 답으로 직접 말했어요. 10단어든 1000단어든 같은 크기 벡터 하나에 압축돼요.")

mcq(U1, "N4 p.8",
    "기계 번역의 시대 구분으로 옳은 것은?",
    ["1950~80년대 신경망, 1990~2010년대 규칙, 2014년 이후 통계",
     "1950~80년대 규칙과 사전, 1990~2010년대 통계 기반, 2014년 이후 신경망",
     "처음부터 끝까지 통계 기반이었다",
     "1990년대에 이미 **트랜스포머(Transformer)** 가 나왔다"],
    1,
    "슬라이드: rules -> statistics -> neural. 신경망 기계 번역은 2년 만에 수백 명이 10년간 만든 시스템을 이겼어요.")

mcq(U2, "N4 p.11",
    "**교사 강요(Teacher Forcing)** 의 정의로 가장 적절한 것은?",
    ["학습할 때 모델 자신의 예측을 다음 입력으로 넣는다",
     "학습할 때 정답 단어를 다음 입력으로 넣는다",
     "시험할 때 정답 단어를 넣는다",
     "정답을 아예 쓰지 않고 학습한다"],
    1,
    "슬라이드: 'we feed the decoder the true previous target word, not its own prediction.' 학습이 안정되고 시간 축으로 병렬화가 돼요.")

mcq(U2, "N4 p.11",
    "**노출 편향(Exposure Bias)** 이 생기는 이유로 가장 적절한 것은?",
    ["학습 데이터가 너무 많아서",
     "학습 때는 정답 앞부분을, 시험 때는 자기 출력 앞부분을 보기 때문",
     "**빔 서치(Beam Search)** 를 쓰기 때문",
     "**소프트맥스(Softmax)** 가 포화되기 때문"],
    1,
    "교사 강요의 부작용이에요. train on the gold prefix, test on your own prefix.")

mcq(U2, "N4 p.12-13",
    "**탐욕적 디코딩(Greedy Decoding)** 과 **빔 서치(Beam Search)** 의 차이로 옳은 것은?",
    ["탐욕적 디코딩은 매 단계 후보 k 개를 남기고, 빔 서치는 1개를 남긴다",
     "탐욕적 디코딩은 매 단계 가장 높은 것 하나, 빔 서치는 후보 k 개를 남긴다",
     "빔 서치는 모든 경우를 다 따져 보는 완전 탐색이다",
     "둘은 완전히 같은 알고리즘이다"],
    1,
    "슬라이드: 'Keep the k best partial hypotheses at every step instead of one.' 보통 k 는 5에서 10이고, 완전 탐색은 아니지만 아주 좋은 근사예요.")

mcq(U2, "N4 p.13",
    "**빔 서치(Beam Search)** 에서 **길이 정규화(Length Normalization)** 가 필요한 이유로 가장 적절한 것은?",
    ["로그 확률의 합이 길수록 커져서 긴 문장만 뽑히기 때문",
     "로그 확률의 합이 음수라 길수록 작아져서 짧은 문장이 과도하게 유리하기 때문",
     "확률의 곱이 1을 넘어가기 때문",
     "빔 크기가 커지면 계산이 느려지기 때문"],
    1,
    "교수님: 로그 확률 자체가 음수기 때문에 문장이 길어질수록 계속 작아지고, 짧은 문장을 과도하게 선호할 수 있어요. 그래서 길이로 나눠 줘요.")

mcq(U2, "N4 p.14",
    "**블루 점수(BLEU)** 에 대한 설명으로 옳지 않은 것은?",
    ["사람이 만든 참조 번역과 n-gram 겹침을 센다",
     "**간결성 페널티(Brevity Penalty)** 가 있어 짧게 말해서 이길 수 없다",
     "다른 단어를 쓴 좋은 번역도 항상 높은 점수를 받는다",
     "n 은 보통 1에서 4까지 쓴다"],
    2,
    "슬라이드: 'a good translation that uses different words scores badly, so BLEU rewards being ordinary.' 평범한 번역에 유리해요.")

mcq(U2, "N4 p.15",
    "인코더-디코더 구조를 번역 말고도 쓸 수 있는 조건으로 가장 적절한 것은?",
    ["입력과 출력이 모두 시퀀스이면 된다",
     "입력과 출력이 같은 언어여야 한다",
     "입력이 반드시 글이어야 한다",
     "출력 길이가 입력 길이와 같아야 한다"],
    0,
    "슬라이드: 'works whenever the input and the output are both sequences, and they need not be the same kind of sequence.'")

mcq(U3, "N4 p.18",
    "**어텐션(Attention)** 의 핵심 생각으로 가장 적절한 것은?",
    ["인코더의 마지막 상태만 더 크게 만든다",
     "디코더가 매 단계마다 모든 인코더 상태를 보고 지금 중요한 것을 고른다",
     "디코더를 여러 겹으로 쌓는다",
     "입력 문장을 짧게 자른다"],
    1,
    "슬라이드: 'At every decoder step, look at all the encoder states and decide which ones matter right now.' 요약을 매 단계 새로 만들어요.")

mcq(U3, "N4 p.24",
    "어텐션 네 단계의 순서로 옳은 것은?",
    ["소프트맥스 -> 점수 -> 가중합 -> 예측",
     "점수 -> 소프트맥스 -> 가중합 -> 예측",
     "점수 -> 가중합 -> 소프트맥스 -> 예측",
     "가중합 -> 점수 -> 소프트맥스 -> 예측"],
    1,
    "교수님: 첫 번째는 스코어, 두 번째는 소프트맥스로 노멀라이즈, 세 번째는 웨이티드 썸으로 컨텍스트 벡터, 마지막이 프레딕션. 이 네 단계가 어텐션에 가장 중요해요.")

mcq(U3, "N4 p.22",
    "어텐션 가중치의 합을 1 로 만들어 주는 단계는?",
    ["1단계 점수 계산", "2단계 **소프트맥스(Softmax)** 정규화", "3단계 가중합", "4단계 예측"],
    1,
    "교수님이 p.29 확인 문제 4번의 답으로 직접 말했어요. 점수는 합이 1 이 아니고, 소프트맥스가 1 로 만들어 줘요.")

mcq(U3, "N4 p.19",
    "**문맥 벡터(Context Vector)** 에 대한 설명으로 가장 적절한 것은?",
    ["인코더 상태들의 단순 평균이다",
     "인코더 상태들의 **가중합(Weighted Sum)** 이고 가중치는 매 단계 새로 계산된다",
     "인코더의 마지막 상태 하나이다",
     "디코더의 첫 상태이다"],
    1,
    "교수님: 그냥 평균 낸 게 아니라 중요도를 구해서 그 가중치를 곱해 더한 가중 평균이에요. 디코딩 스텝마다 계속 바뀌어요.")

mcq(U3, "N4 p.20",
    "파이썬 딕셔너리와 어텐션을 비교한 설명으로 옳은 것은?",
    ["둘 다 키 하나만 정확히 맞아야 값을 준다",
     "딕셔너리는 하드 룩업, 어텐션은 모든 키에 조금씩 맞아 값들이 섞이는 소프트 룩업이다",
     "어텐션은 키를 쓰지 않는다",
     "딕셔너리가 어텐션보다 더 유연하다"],
    1,
    "슬라이드: 'Attention does a soft lookup: the query matches every key to some degree, and you get a blend of all the values.'")

mcq(U4, "N4 p.25",
    "어텐션이 주는 네 가지 이득이 아닌 것은?",
    ["성능 향상", "병목 제거", "기울기 경로 단축", "학습 데이터 자동 생성"],
    3,
    "슬라이드의 네 가지는 performance, no bottleneck, shorter gradient paths, interpretability 예요.")

mcq(U4, "N4 p.26",
    "**정렬(Alignment)** 에 대한 설명으로 가장 적절한 것은?",
    ["통계 기반 번역은 정렬 모델이 필요 없었다",
     "어텐션은 번역을 배우다 보면 정렬을 덤으로 배운다",
     "정렬은 사람이 일일이 표시해 줘야 한다",
     "정렬은 **소프트맥스(Softmax)** 의 다른 이름이다"],
    1,
    "슬라이드: 'Attention learns alignment as a side effect of learning to translate. Nobody supervised it.'")

mcq(U4, "N4 p.27",
    "**트랜스포머(Transformer)** 가 쓰는 점수 함수로 옳은 것은?",
    ["Bahdanau 방식의 덧셈형 점수", "Luong 방식의 이중선형 점수",
     "스케일한 **내적(Dot Product)**", "코사인 유사도"],
    2,
    "교수님: 어텐션 하면 가장 유명한 게 바나두 어텐션인데, 트랜스포머에서는 다시 그냥 닷 프로덕트로 갑니다. 파라미터를 더 쓰지 않아요.")

mcq(U4, "N4 p.28",
    "번역이라는 맥락을 지운 어텐션의 일반 정의로 가장 적절한 것은?",
    ["값들과 쿼리가 주어지면, 쿼리에 따라 정해지는 가중치로 값들의 가중합을 만든다",
     "값들 중 가장 큰 것 하나를 고른다",
     "쿼리와 키를 이어 붙인다",
     "값들의 평균을 낸다"],
    0,
    "슬라이드: 'given a set of values and a query, attention computes a weighted sum of the values, where the weights depend on the query.'")

mcq(U5, "N4 p.33",
    "**셀프 어텐션(Self-Attention)** 과 **크로스 어텐션(Cross-Attention)** 의 차이로 옳은 것은?",
    ["계산 방식이 완전히 다르다",
     "쿼리, 키, 밸류가 같은 시퀀스에서 오면 셀프, 다른 시퀀스에서 오면 크로스이다",
     "셀프 어텐션에는 **소프트맥스(Softmax)** 가 없다",
     "크로스 어텐션은 **가중합(Weighted Sum)** 을 하지 않는다"],
    1,
    "슬라이드: 'Same machinery, the only change is where the vectors come from.' 계산은 똑같아요.")

mcq(U5, "N4 p.34",
    "**쿼리(Query)**, **키(Key)**, **밸류(Value)** 의 역할을 바르게 짝지은 것은?",
    ["쿼리는 광고, 키는 질문, 밸류는 내용",
     "쿼리는 질문, 키는 광고용 이름표, 밸류는 건네줄 내용",
     "쿼리는 내용, 키는 질문, 밸류는 광고",
     "셋 다 같은 벡터이다"],
    1,
    "교수님: 키는 나는 이런 정보를 갖고 있으니 나를 찾아봐라 하고 광고하는 것이고, 밸류는 내가 선택되면 실제로 전달할 정보예요.")

mcq(U5, "N4 p.34",
    "W^Q, W^K, W^V 에 대한 설명으로 옳은 것은?",
    ["토큰마다 서로 다른 행렬을 하나씩 만든다",
     "모든 자리가 같은 세 행렬을 함께 쓴다",
     "학습되지 않는 고정 행렬이다",
     "**위치 인코딩(Positional Encoding)** 을 만드는 행렬이다"],
    1,
    "교수님: 위치마다 이 매트릭스를 따로 만드는 건 아니고, 모든 토큰들이 공유하는 겁니다.")

mcq(U5, "N4 p.32",
    "**셀프 어텐션(Self-Attention)** 이 **RNN(순환 신경망)** 보다 좋은 점으로 가장 적절한 것은?",
    ["파라미터 수가 훨씬 적다",
     "두 토큰 사이의 최대 경로가 1 이고 모든 자리를 동시에 계산할 수 있다",
     "메모리를 훨씬 적게 쓴다",
     "**소프트맥스(Softmax)** 를 쓰지 않아도 된다"],
    1,
    "교수님: 셀프 어텐션의 가장 큰 장점은 병렬로 계산할 수 있다는 거고, 이 패러럴이 핵심이에요. 메모리는 오히려 n 제곱으로 늘어요.")

mcq(U5, "N4 p.37",
    "자기 자신에게 어텐션할 때 점수 행렬 $QK^{\\top}$ 의 모양은? (토큰 수 n)",
    ["$n \\times d_k$", "$n \\times n$", "$d_k \\times d_k$", "$n \\times d_v$"],
    1,
    "모든 토큰이 모든 토큰과 비교되므로 n 줄 n 칸짜리 정사각형이에요. 여기서 **이차 비용(Quadratic Cost)** 이 나와요.")

mcq(U6, "N4 p.38",
    "점수를 $\\sqrt{d_k}$ 로 나누는 이유로 가장 적절한 것은?",
    ["합을 1 로 만들기 위해",
     "점수의 분산이 $d_k$ 라서 커진 점수가 **소프트맥스(Softmax)** 를 포화시키고 **기울기(Gradient)** 를 없애기 때문",
     "행렬 곱의 모양을 맞추기 위해",
     "밸류를 양수로 만들기 위해"],
    1,
    "합은 소프트맥스가 알아서 1 로 만들어요. 문제는 분포가 뾰족해져 학습이 멈추는 것이에요.")

mcq(U6, "N4 p.39",
    "맨 **셀프 어텐션(Self-Attention)** 의 세 가지 배리어가 아닌 것은?",
    ["순서 정보가 없다", "칸마다의 **비선형성(Nonlinearity)** 이 없다",
     "미래 토큰을 볼 수 있다", "**가중합(Weighted Sum)** 의 합이 1 이 아니다"],
    3,
    "합이 1 인 것은 소프트맥스가 보장해요. 배리어는 순서, 비선형, 미래 셋이에요.")

mcq(U7, "N4 p.40",
    "**위치 인코딩(Positional Encoding)** 이 필요한 이유로 가장 적절한 것은?",
    ["셀프 어텐션이 **순열 등변성(Permutation Equivariance)** 을 가져 순서를 구별하지 못해서",
     "소프트맥스가 포화되어서",
     "파라미터가 너무 많아서",
     "밸류가 음수가 될 수 있어서"],
    0,
    "슬라이드의 식 SelfAttn(PX) = P SelfAttn(X) 가 그 증거예요. dog bites man 과 man bites dog 를 구별하지 못해요.")

mcq(U7, "N4 p.41",
    "학습 파라미터가 하나도 없는 위치 인코딩은?",
    ["**사인 코사인 위치 인코딩(Sinusoidal Positional Encoding)**", "학습형 절대 위치 임베딩",
     "**로프(RoPE)**", "**인과 마스킹(Causal Masking)**"],
    0,
    "슬라이드 표: Sinusoidal 은 no parameters at all. 학습형 절대 위치는 학습한 길이를 넘지 못해요.")

mcq(U7, "N4 p.42",
    "**위치별 피드포워드 신경망(Position-wise Feed-Forward Network (FFN))** 에 대한 설명으로 옳은 것은?",
    ["자리끼리 정보를 섞는다",
     "자리마다 같은 2층 **MLP(다층 퍼셉트론)** 를 독립적으로 적용한다",
     "자리마다 다른 가중치를 쓴다",
     "**어텐션(Attention)** 대신 쓰는 부품이다"],
    1,
    "슬라이드: 'Apply the same two-layer MLP to every position independently. No mixing across positions happens here.' 섞는 일은 어텐션 담당이에요.")

mcq(U7, "N4 p.43",
    "**인과 마스킹(Causal Masking)** 을 적용하는 시점으로 옳은 것은?",
    ["**소프트맥스(Softmax)** 전에 점수를 마이너스 무한으로 바꾼다",
     "소프트맥스 후에 가중치를 0 으로 바꾼다",
     "**가중합(Weighted Sum)** 을 한 뒤에 뺀다",
     "**위치 인코딩(Positional Encoding)** 을 더할 때 함께 한다"],
    0,
    "소프트맥스 후에 0 으로 지우면 남은 가중치의 합이 1 이 아니게 돼요. 반드시 전에 해야 해요.")

mcq(U8, "N4 p.47",
    "**멀티 헤드 어텐션(Multi-Head Attention (MHA))** 에 대한 설명으로 옳은 것은?",
    ["헤드를 h 개 쓰면 전체 차원이 h 배가 된다",
     "전체 차원 d 를 h 로 나눈 d/h 차원에서 각 헤드가 돌아 계산량이 거의 같다",
     "헤드마다 같은 W^Q, W^K, W^V 를 쓴다",
     "헤드가 많을수록 파라미터가 제곱으로 늘어난다"],
    1,
    "교수님: 헤드를 여러 개 쓴다고 전체 차원을 키우는 게 아니라 전체 차원을 h 로 나눠서 서로 다른 관점에서 본다, 계산 수는 똑같다.")

mcq(U8, "N4 p.49",
    "**잔차 연결(Residual Connection)** 의 효과로 가장 적절한 것은?",
    ["파라미터 수를 줄인다",
     "**항등 경로(Identity Path)** 가 생겨 깊은 층에서도 **기울기(Gradient)** 가 1층까지 닿는다",
     "메모리 사용량을 줄인다",
     "**소프트맥스(Softmax)** 를 더 뾰족하게 만든다"],
    1,
    "슬라이드: 'The identity path makes the Jacobian I + df/dx, so the gradient reaches layer 1 even in a 96-layer stack.'")

# =====================================================================
# OX (22)
# =====================================================================
ox(U1, "N4 p.6", "**RNN(순환 신경망)** 의 세 가지 문제는 먼 거리 의존, 순차 계산, 그리고 **정보 병목(Information Bottleneck)** 이다.",
   True, "슬라이드 p.6 이 세 가지를 나란히 적고 오늘 두 아이디어가 바로 이것을 공격한다고 해요.")

ox(U1, "N4 p.10", "seq2seq 의 디코더는 원문을 조건으로 받는 **조건부 언어 모델(Conditional Language Model)** 이다.",
   True, "슬라이드: 'The decoder is a language model that is conditioned on the source.'")

ox(U1, "N4 p.10", "seq2seq 는 인코더와 디코더를 서로 다른 손실로 따로따로 학습한다.",
   False, "하나의 손실, 한 번의 역전파로 함께 학습해요. 그것이 **종단간 학습(End-to-End)** 의 뜻이에요.")

ox(U2, "N4 p.12", "**탐욕적 디코딩(Greedy Decoding)** 은 앞에서 고른 단어를 나중에 되돌릴 수 있다.",
   False, "슬라이드: 'it cannot take anything back.' 앞의 잘못된 한 단어가 뒤를 모두 망쳐요.")

ox(U2, "N4 p.13", "**빔 크기(Beam Size)** k 가 1 이면 **탐욕적 디코딩(Greedy Decoding)** 과 같다.",
   True, "교수님이 p.29 확인 문제 3번의 답으로 직접 말했어요.")

ox(U2, "N4 p.13", "**빔 서치(Beam Search)** 는 가능한 모든 문장을 다 따져 보는 완전 탐색이다.",
   False, "슬라이드: 'Not exhaustive search, but a very good approximation for a tiny cost.'")

ox(U2, "N4 p.14", "**블루 점수(BLEU)** 의 **간결성 페널티(Brevity Penalty)** 는 모델이 짧게 말해서 점수를 얻는 것을 막는다.",
   True, "n-gram 겹침만 보면 짧게 말할수록 정밀도가 올라가서 페널티가 필요해요.")

ox(U3, "N4 p.19", "어텐션 가중치는 학습이 끝나면 고정되어 모든 디코딩 단계에서 같은 값을 쓴다.",
   False, "교수님: 이 가중치는 디코딩 스텝마다 계속 바뀌어요. 즉석에서 계산돼요.")

ox(U3, "N4 p.21", "어텐션 1단계에서 가장 단순한 점수 계산 방법은 **내적(Dot Product)** 이다.",
   True, "슬라이드: 'The simplest score is a dot product.'")

ox(U3, "N4 p.22", "**어텐션 점수(Attention Score)** 와 **어텐션 가중치(Attention Weight)** 는 같은 말이다.",
   False, "점수는 **소프트맥스(Softmax)** 이전의 날것 숫자이고, 가중치는 소프트맥스 이후 합이 1 인 값이에요.")

ox(U4, "N4 p.25", "어텐션은 **기울기 소실(Vanishing Gradient)** 문제를 직접 고치는 것이 아니라 짧은 길을 새로 내서 비켜 간다.",
   True, "슬라이드: 'the vanishing-gradient problem is bypassed, not patched.'")

ox(U4, "N4 p.25", "어텐션 가중치를 그림으로 보면 모델이 어디를 봤는지 알 수 있어 **해석 가능성(Interpretability)** 이 생긴다.",
   True, "슬라이드: 'The weights are a picture of what the model looked at, rare in deep learning, and free here.'")

ox(U5, "N4 p.32", "**셀프 어텐션(Self-Attention)** 에서 두 토큰 사이의 최대 경로 길이는 문장 길이 n 에 비례한다.",
   False, "언제나 1 이에요. 슬라이드: 'the maximum path length drops from n to 1.'")

ox(U5, "N4 p.35", "셀프 어텐션에서 한 토큰은 자기 자신에게도 **어텐션 점수(Attention Score)** 를 매긴다.",
   True, "교수님: q3 가 k1, k2, k3, k4, k5 와 다 계산합니다. 자기도 포함이에요.")

ox(U5, "N4 p.37", "행렬 형태로 계산하면 자리를 도는 반복문이 없어 GPU 에서 **병렬화(Parallelization)** 가 잘 된다.",
   True, "슬라이드: 'No loop over positions, which is exactly why this runs so well on a GPU.'")

ox(U6, "N4 p.38", "점수를 $d_k$ 로 나눈다.",
   False, "$\\sqrt{d_k}$ 로 나눠요. 분산이 $d_k$ 라서 표준편차인 $\\sqrt{d_k}$ 로 나눠야 분산이 1 로 돌아와요.")

ox(U6, "N4 p.39", "**순열 등변성(Permutation Equivariance)** 은 입력 순서를 바꾸면 출력도 똑같이 순서만 바뀐다는 뜻이다.",
   True, "식으로는 SelfAttn(PX) = P SelfAttn(X) 예요. 결국 순서를 구별하지 못한다는 뜻이에요.")

ox(U7, "N4 p.40", "**위치 인코딩(Positional Encoding)** 은 토큰 **임베딩(Embedding)** 에 이어 붙인다.",
   False, "더해요(add). 슬라이드: 'add it to the token embedding before the first layer.'")

ox(U7, "N4 p.42", "**위치별 피드포워드 신경망(Position-wise Feed-Forward Network (FFN))** 의 가운데 차원 d_ff 는 보통 4d 이다.",
   True, "슬라이드: 'd_ff is usually 4d.' 그래서 **파라미터(Parameter)** 대부분이 여기 살아요.")

ox(U7, "N4 p.43", "**인코더(Encoder)** 도 **인과 마스킹(Causal Masking)** 을 쓴다.",
   False, "슬라이드: 'Encoders skip this and look both ways.' 인코더는 앞뒤를 다 봐요.")

ox(U8, "N4 p.50", "**층 정규화(Layer Normalization (LayerNorm))** 는 배치나 토큰끼리 섞지 않아서 학습과 추론에서 똑같이 동작한다.",
   True, "슬라이드: 'it never mixes across tokens or across the batch, so it behaves identically at training and inference.'")

ox(U8, "N4 p.55", "**어텐션(Attention)** 의 계산과 메모리는 문장 길이에 비례해서 늘어난다.",
   False, "점수 행렬이 n x n 이라 문장 길이의 제곱으로 늘어요. **이차 비용(Quadratic Cost)** 이라고 해요.")

# =====================================================================
# SHORT (16)
# =====================================================================
short(U1, "N4 p.16", "원문의 모든 정보가 고정 크기 벡터 하나를 지나야 해서 생기는 문제를 무엇이라고 하나요?",
      ["정보 병목", "Information Bottleneck", "information bottleneck", "병목"],
      "슬라이드 p.16 의 제목이 The Information Bottleneck 이에요.")

short(U2, "N4 p.11", "학습과 시험의 입력이 달라서 생기는 어긋남을 무엇이라고 하나요?",
      ["노출 편향", "Exposure Bias", "exposure bias"],
      "**교사 강요(Teacher Forcing)** 의 부작용이에요.")

short(U2, "N4 p.13", "**빔 서치(Beam Search)** 에서 보통 쓰는 빔 크기 k 의 범위는?",
      ["5~10", "5에서 10", "5-10", "5 to 10"],
      "슬라이드: 'Typical k is 5 to 10.'")

short(U3, "N4 p.24", "어텐션 네 단계를 순서대로 쓰세요.",
      ["점수, 소프트맥스, 가중합, 예측", "score, softmax, weighted sum, predict",
       "스코어 소프트맥스 가중합 예측", "점수-소프트맥스-가중합-예측"],
      "교수님이 이 네 단계가 어텐션에 가장 중요하다고 했어요.")

short(U3, "N4 p.23", "인코더 상태들을 어텐션 가중치로 가중합한 결과 벡터의 이름은?",
      ["문맥 벡터", "Context Vector", "context vector", "컨텍스트 벡터"],
      "기호는 $c_t$ 예요. 셀프 어텐션에서는 $o_i$ 로 쓰기도 해요.")

short(U4, "N4 p.26", "어텐션이 따로 가르치지 않아도 덤으로 배우는, 원문 단어와 번역 단어를 이어 주는 것은?",
      ["정렬", "Alignment", "alignment"],
      "통계 기반 번역에서는 이것만 연구하는 분야가 따로 있었어요.")

short(U5, "N4 p.34", "셀프 어텐션에서 토큰 하나가 동시에 맡는 세 역할을 쓰세요.",
      ["쿼리, 키, 밸류", "Query, Key, Value", "query key value", "쿼리 키 밸류", "Q, K, V"],
      "교수님: 이 3개의 컨셉을 이해해야 뒤에 트랜스포머를 이해할 수 있어요.")

short(U5, "N4 p.36", "$\\mathrm{softmax}(QK^{\\top}/\\sqrt{d_k})V$ 라는 식으로 계산하는 어텐션의 이름은?",
      ["스케일드 닷프로덕트 어텐션", "Scaled Dot-Product Attention", "scaled dot-product attention",
       "스케일드 다트프로덕트 어텐션"],
      "교수님: 루트 d_k 가 영향을 주기 때문에 스케일드 닷 프로덕트 어텐션이라고 표현을 해요.")

short(U6, "N4 p.38", "$d_k$ 가 512 일 때 **내적(Dot Product)** 점수의 표준편차는 약 얼마인가요? (소수 둘째 자리)",
      ["22.63", "22.6"],
      "표준편차는 $\\sqrt{d_k}$ 이고 $\\sqrt{512}$ 는 약 22.63 이에요.", num=True, tol=0.05)

short(U6, "N4 p.39", "셀프 어텐션의 배리어 1(순서를 모른다)을 고치는 부품의 이름은?",
      ["위치 인코딩", "Positional Encoding", "positional encoding", "포지셔널 인코딩"],
      "배리어 2 는 FFN, 배리어 3 은 인과 마스킹이 고쳐요.")

short(U7, "N4 p.43", "미래 자리의 점수를 소프트맥스 전에 무엇으로 바꾸나요?",
      ["마이너스 무한", "-무한", "음의 무한대", "-inf", "minus infinity", "마이너스 무한대"],
      "exp 를 씌우면 0 이 되기 때문에 가중치가 정확히 0 이 돼요.")

short(U7, "N4 p.42", "$d = 512$ 일 때 FFN 의 가운데 차원 $d_{ff}$ 는 보통 얼마인가요?",
      ["2048", "2,048"],
      "$d_{ff}$ 는 보통 $4d$ 이므로 $4 \\times 512 = 2048$ 이에요.", num=True, tol=0.5)

short(U8, "N4 p.47", "$d = 512$, 헤드 수 $h = 8$ 일 때 헤드 하나가 쓰는 차원은?",
      ["64"],
      "$d/h = 512/8 = 64$ 예요. 슬라이드에 그대로 나와요.", num=True, tol=0.5)

short(U8, "N4 p.52", "**디코더(Decoder)** 블록에만 있고 **인코더(Encoder)** 블록에는 없는 두 서브층을 쓰세요.",
      ["마스크드 셀프 어텐션, 크로스 어텐션", "masked self-attention, cross-attention",
       "마스크드 셀프어텐션과 크로스 어텐션", "인과 마스킹된 셀프 어텐션, 크로스 어텐션"],
      "슬라이드: 'the same, plus a masked self-attention at the bottom and a cross-attention in the middle.'")

short(U8, "N4 p.56", "WMT14 영어에서 독일어 번역에서 Transformer big 의 BLEU 점수는?",
      ["28.4"],
      "슬라이드 막대그래프에 GNMT 24.6, ConvSeq2Seq 25.2, Transformer base 27.3, Transformer big 28.4 라고 찍혀 있어요.",
      num=True, tol=0.05)

short(U8, "N4 p.57", "슬라이드가 든 트랜스포머가 이긴 네 가지 성질을 쓰세요.",
      ["병렬성, 짧은 경로, 깔끔한 확장, 과제 무관",
       "parallelism, short paths, scales cleanly, task-agnostic",
       "병렬, 짧은 경로, 확장성, 과제 무관"],
      "슬라이드 네 상자가 Parallelism, Short paths, Scales cleanly, Task-agnostic 이에요.")

# =====================================================================
# ESSAY (10)
# =====================================================================
essay(U1, "N4 p.16", "information-bottleneck",
      "seq2seq 의 **정보 병목(Information Bottleneck)** 이 무엇이고 왜 긴 문장에서 더 나쁜지 설명하시오.",
      "seq2seq 에서 **디코더(Decoder)** 가 원문에 대해 아는 것은 **인코더(Encoder)** 가 만든 고정 크기 벡터 하나뿐이에요. "
      "이 벡터의 칸 수는 입력 길이와 상관없이 늘 같아요. "
      "그래서 20단어 문장과 200단어 문단이 같은 칸 수를 받아요. "
      "문장이 길수록 버려지는 정보가 많아지고 성능이 무너져요. "
      "해결은 디코더가 그 벡터 하나만 쓰도록 강요하지 않는 것, 곧 **어텐션(Attention)** 이에요.",
      ["디코더가 아는 것은 고정 크기 벡터 하나", "벡터 크기가 입력 길이와 무관",
       "긴 문장일수록 압축 손실이 큼", "성능이 문장 길이에 따라 무너짐",
       "해결책은 어텐션", "교수님이 확인 문제 1번 답으로 직접 말한 내용"])

essay(U2, "N4 p.11", "teacher-forcing-exposure-bias",
      "**교사 강요(Teacher Forcing)** 가 무엇이고 그 부작용인 **노출 편향(Exposure Bias)** 이 무엇인지 서술하시오.",
      "교사 강요는 학습할 때 디코더에 모델 자신의 예측 대신 정답 단어를 다음 입력으로 넣어 주는 방법이에요. "
      "학습이 안정되고 시간 축으로 병렬화할 수 있다는 장점이 있어요. "
      "그런데 시험할 때는 정답을 모르므로 모델이 직전에 만든 출력을 넣어야 해요. "
      "학습 때는 정답 앞부분, 시험 때는 자기 출력 앞부분을 보게 되어 둘이 어긋나요. "
      "이 어긋남을 노출 편향이라고 해요.",
      ["학습 때 정답 단어를 다음 입력으로", "학습이 안정되고 병렬 가능",
       "시험 때는 자기 출력을 넣어야 함", "학습과 시험의 입력 분포가 다름",
       "이 불일치가 노출 편향", "교수님이 확인 문제 2번 답으로 설명"])

essay(U2, "N4 p.13", "beam-length-normalization",
      "**빔 서치(Beam Search)** 에서 **길이 정규화(Length Normalization)** 가 왜 필요한지 설명하시오.",
      "빔 서치의 점수는 각 단계 로그 확률의 합이에요. "
      "확률은 0 과 1 사이이므로 로그 확률은 항상 음수예요. "
      "따라서 문장이 길수록 음수를 더 많이 더해 점수가 계속 작아져요. "
      "그대로 비교하면 짧은 문장이 과도하게 유리해져요. "
      "그래서 끝난 후보들의 점수를 토큰 수로 나눈 뒤 비교해요.",
      ["점수는 로그 확률의 합", "로그 확률은 음수",
       "길수록 점수가 작아짐", "짧은 문장을 과도하게 선호",
       "길이로 나눠서 비교", "교수님이 확인 문제 3번 답으로 설명"])

essay(U3, "N4 p.24", "four-attention-equations",
      "어텐션의 네 단계를 식과 함께 순서대로 서술하시오.",
      "1단계는 점수 계산이에요. 디코더 상태 $s_t$ 와 각 인코더 상태 $h_i$ 를 **내적(Dot Product)** 해서 $e_i$ 를 만들어요. "
      "2단계는 **소프트맥스(Softmax)** 정규화예요. $\\alpha = \\mathrm{softmax}(e)$ 로 합이 1 인 **어텐션 분포(Attention Distribution)** 를 만들어요. "
      "3단계는 **가중합(Weighted Sum)** 이에요. $c_t = \\sum_i \\alpha_i h_i$ 로 **문맥 벡터(Context Vector)** 를 만들어요. "
      "4단계는 예측이에요. $c_t$ 와 $s_t$ 를 이어 붙여 다음 단어를 예측해요. "
      "가중치의 합을 1 로 만들어 주는 것은 2단계예요.",
      ["1단계 점수, 내적", "2단계 소프트맥스 정규화",
       "3단계 가중합으로 문맥 벡터", "4단계 문맥 벡터와 디코더 상태로 예측",
       "합을 1 로 만드는 것은 2단계", "교수님이 이 네 단계가 가장 중요하다고 강조"])

essay(U4, "N4 p.25", "what-attention-buys",
      "어텐션이 주는 이득 네 가지를 쓰시오.",
      "첫째, 성능이에요. 어텐션을 붙인 신경망 기계 번역이 붙이지 않은 것을 곧바로, 특히 긴 문장에서 크게 이겼어요. "
      "둘째, 병목 제거예요. 디코더가 요약 벡터를 거치지 않고 원문을 직접 읽어요. "
      "셋째, 짧은 **기울기(Gradient)** 경로예요. 모든 출력에서 모든 입력으로 직접 길이 나서 **기울기 소실(Vanishing Gradient)** 을 비켜 가요. "
      "넷째, **해석 가능성(Interpretability)** 이에요. 가중치를 그림으로 보면 모델이 어디를 봤는지 알 수 있어요.",
      ["성능 향상, 특히 긴 문장", "정보 병목 제거",
       "기울기 경로 단축", "해석 가능성",
       "네 가지가 하나의 가중 평균에서 나옴", "딥러닝에서 해석 가능성은 드문 일"])

essay(U5, "N4 p.34", "query-key-value",
      "**쿼리(Query)**, **키(Key)**, **밸류(Value)** 가 각각 무엇인지 설명하고, 셀프 어텐션에서 어떻게 만드는지 서술하시오.",
      "쿼리는 지금 내가 무엇을 찾고 있는지를 담은 벡터예요. "
      "키는 나는 이런 정보를 갖고 있다고 다른 토큰에게 광고하는 검색용 이름표예요. "
      "밸류는 내가 선택되면 실제로 건네줄 내용이에요. "
      "셀프 어텐션에서는 같은 입력 벡터 $x_i$ 에 학습 가능한 행렬 $W^Q, W^K, W^V$ 를 각각 곱해 만들어요. "
      "이 세 행렬은 모든 자리가 함께 쓰므로 문장이 길어져도 **파라미터(Parameter)** 수가 늘지 않아요. "
      "점수는 쿼리와 키로 만들고, 실제로 섞이는 것은 밸류예요.",
      ["쿼리는 무엇을 찾는지", "키는 광고용 이름표",
       "밸류는 건네줄 내용", "같은 입력에 세 행렬을 곱해 만듦",
       "세 행렬은 모든 자리가 공유", "점수는 Q 와 K, 가중합은 V"])

essay(U6, "N4 p.38", "scaled-dot-product",
      "점수를 $\\sqrt{d_k}$ 로 나누는 이유와, 나누지 않으면 무엇이 잘못되는지 서술하시오.",
      "$q$ 와 $k$ 의 각 칸이 서로 독립이고 분산이 1 이면 **내적(Dot Product)** 의 분산은 $d_k$ 가 돼요. "
      "그래서 표준편차가 $\\sqrt{d_k}$ 이고, $d_k = 512$ 면 점수가 보통 플러스마이너스 20 을 넘어요. "
      "이렇게 큰 점수를 **소프트맥스(Softmax)** 에 넣으면 exp 때문에 차이가 크게 벌어져 거의 원-핫에 가까운 분포가 돼요. "
      "포화된 소프트맥스는 **기울기(Gradient)** 가 거의 0 이라 학습이 멈춰요. "
      "$\\sqrt{d_k}$ 로 나누면 분산이 다시 1 이 되어 분포가 적당히 부드러워져요.",
      ["내적의 분산이 $d_k$", "표준편차가 $\\sqrt{d_k}$",
       "큰 점수는 소프트맥스를 포화시킴", "포화되면 기울기가 거의 0",
       "학습이 멈춤", "나누면 분산이 1 로 돌아옴"])

essay(U6, "N4 p.39", "three-barriers",
      "맨 **셀프 어텐션(Self-Attention)** 의 세 가지 배리어와 각각을 고치는 부품을 쓰시오.",
      "배리어 1 은 순서 정보가 없다는 것이에요. **순열 등변성(Permutation Equivariance)** 때문에 순서를 바꿔도 결과가 그대로 따라가요. "
      "이것은 **위치 인코딩(Positional Encoding)** 으로 고쳐요. "
      "배리어 2 는 칸마다의 **비선형성(Nonlinearity)** 이 없다는 것이에요. 어텐션 층을 쌓아도 결국 선형 변환에 가까워요. "
      "이것은 **위치별 피드포워드 신경망(Position-wise Feed-Forward Network (FFN))** 으로 고쳐요. "
      "배리어 3 은 미래 토큰을 볼 수 있다는 것이에요. **언어 모델(Language Model (LM))** 과제가 시시해져요. "
      "이것은 **인과 마스킹(Causal Masking)** 으로 고쳐요.",
      ["배리어 1 순서 없음", "위치 인코딩으로 해결",
       "배리어 2 비선형 없음", "위치별 FFN 으로 해결",
       "배리어 3 미래를 봄", "인과 마스킹으로 해결",
       "교수님이 이 배리어 3개를 기억하라고 강조"])

essay(U7, "N4 p.42", "attention-vs-ffn",
      "**어텐션(Attention)** 과 **위치별 피드포워드 신경망(Position-wise Feed-Forward Network (FFN))** 의 역할 분담을 설명하시오.",
      "어텐션은 토큰과 토큰 사이에서 정보를 옮기는 일을 해요. 자리끼리 섞이는 곳은 여기뿐이에요. "
      "FFN 은 각 자리에서 받은 정보를 혼자서 가공하는 일을 해요. 자리끼리 섞지 않아요. "
      "FFN 은 자리마다 같은 2층 **MLP(다층 퍼셉트론)** 를 독립적으로 적용해요. "
      "가운데 차원 $d_{ff}$ 가 보통 $4d$ 라서 **파라미터(Parameter)** 대부분이 FFN 에 있어요. "
      "$d = 512$ 면 FFN 은 약 $8d^2$, 어텐션 투영은 약 $4d^2$ 로 FFN 쪽이 두 배예요.",
      ["어텐션은 토큰 사이 정보 이동", "FFN 은 각 토큰을 가공",
       "FFN 에서는 자리끼리 안 섞임", "같은 2층 MLP 를 자리마다 적용",
       "d_ff 는 보통 4d", "파라미터 대부분이 FFN"])

essay(U8, "N4 p.47-50", "mha-residual-layernorm",
      "**멀티 헤드 어텐션(Multi-Head Attention (MHA))**, **잔차 연결(Residual Connection)**, **층 정규화(Layer Normalization (LayerNorm))** 가 각각 하는 일을 쓰시오.",
      "멀티 헤드 어텐션은 전체 차원 $d$ 를 헤드 $h$ 개로 나누어 $d/h$ 차원에서 각각 어텐션을 하고 이어 붙인 뒤 $W^O$ 로 다시 섞어요. "
      "하나의 가중 평균으로는 한 가지 질문만 할 수 있는데, 단어는 문법, 의미, 지시 대상 같은 여러 질문을 동시에 해야 해서예요. "
      "잔차 연결은 서브층의 입력을 출력에 그대로 더해요. **항등 경로(Identity Path)** 가 생겨 깊은 층에서도 **기울기(Gradient)** 가 1층까지 닿아요. "
      "층 정규화는 한 토큰의 벡터를 평균 0, 분산 1 로 맞춘 뒤 학습되는 $\\gamma$ 와 $\\beta$ 로 다시 크기를 조절해요. "
      "토큰끼리도 배치끼리도 섞지 않아서 학습과 추론에서 똑같이 동작해요.",
      ["멀티 헤드는 d 를 h 로 나눠 여러 관점", "계산량과 파라미터는 거의 그대로",
       "잔차 연결은 입력을 출력에 더함", "항등 경로로 기울기가 1층까지",
       "층 정규화는 평균 0 분산 1", "감마와 베타로 재조정",
       "토큰끼리 배치끼리 섞지 않음"])

# =====================================================================
# CALC (10)
# =====================================================================
calc(U3, "N4 p.21", "attention-score-dot",
     "디코더 상태가 $s = (1, 2)$ 이고 인코더 상태가 $h_1 = (3.0, 0.3)$, $h_2 = (0.4, 0.2)$, $h_3 = (0.1, 0.2)$, $h_4 = (0.2, 0.1)$ 이다. "
     "**내적(Dot Product)** 으로 **어텐션 점수(Attention Score)** 네 개를 구하시오.",
     "같은 자리끼리 곱해서 더해요. 소수 둘째 자리까지 쓰세요.",
     [{"label": "e1", "ans": 3.6, "tol": 0.01}, {"label": "e2", "ans": 0.8, "tol": 0.01},
      {"label": "e3", "ans": 0.5, "tol": 0.01}, {"label": "e4", "ans": 0.4, "tol": 0.01}],
     ["점수 식은 $e_i = s^{\\top} h_i$ 예요",
      "$e_1 = 1 \\times 3.0 + 2 \\times 0.3 = 3.0 + 0.6 = 3.6$",
      "$e_2 = 1 \\times 0.4 + 2 \\times 0.2 = 0.4 + 0.4 = 0.8$",
      "$e_3 = 1 \\times 0.1 + 2 \\times 0.2 = 0.1 + 0.4 = 0.5$",
      "$e_4 = 1 \\times 0.2 + 2 \\times 0.1 = 0.2 + 0.2 = 0.4$"],
     "(3.6, 0.8, 0.5, 0.4)",
     "점수는 아직 합이 1 이 아니에요. 여기서 끝내지 말고 소프트맥스를 거쳐야 가중치가 돼요.")

calc(U3, "N4 p.22", "attention-softmax",
     "**어텐션 점수(Attention Score)** 가 $(2, 1, 0)$ 이다. **소프트맥스(Softmax)** 로 **어텐션 가중치(Attention Weight)** 를 구하시오. "
     "($e^2 = 7.389$, $e^1 = 2.718$, $e^0 = 1$)",
     "각 점수에 exp 를 씌우고 전체 합으로 나눠요. 소수 넷째 자리까지 쓰세요.",
     [{"label": "알파1", "ans": 0.6652, "tol": 0.001}, {"label": "알파2", "ans": 0.2447, "tol": 0.001},
      {"label": "알파3", "ans": 0.0900, "tol": 0.001}],
     ["$\\mathrm{softmax}(e)_i = \\exp(e_i) / \\sum_j \\exp(e_j)$ 예요",
      "분자는 각각 7.389, 2.718, 1 이에요",
      "합은 $7.389 + 2.718 + 1 = 11.107$ 이에요",
      "$7.389 / 11.107 = 0.6652$",
      "$2.718 / 11.107 = 0.2447$, $1 / 11.107 = 0.0900$"],
     "(0.6652, 0.2447, 0.0900), 합은 1",
     "합이 1 이 되는지 꼭 확인하세요. 안 되면 나눗셈을 틀린 거예요.")

calc(U3, "N4 p.23", "context-vector-weighted-sum",
     "**어텐션 가중치(Attention Weight)** 가 $(0.5, 0.3, 0.2)$ 이고 인코더 상태가 $h_1 = (2, 0)$, $h_2 = (0, 2)$, $h_3 = (1, 1)$ 이다. "
     "**문맥 벡터(Context Vector)** $c$ 를 구하시오.",
     "각 상태에 가중치를 곱해서 모두 더해요. 소수 둘째 자리까지 쓰세요.",
     [{"label": "c 첫 칸", "ans": 1.2, "tol": 0.01}, {"label": "c 둘째 칸", "ans": 0.8, "tol": 0.01}],
     ["$c = \\sum_i \\alpha_i h_i$ 예요",
      "첫 칸: $0.5 \\times 2 + 0.3 \\times 0 + 0.2 \\times 1 = 1.0 + 0 + 0.2 = 1.2$",
      "둘째 칸: $0.5 \\times 0 + 0.3 \\times 2 + 0.2 \\times 1 = 0 + 0.6 + 0.2 = 0.8$",
      "가중치 합이 1 이므로 결과는 세 상태의 가중 평균이에요"],
     "$c = (1.2, 0.8)$",
     "가중치를 곱하는 대상은 키가 아니라 상태(밸류)예요.")

calc(U6, "N4 p.38", "scale-by-sqrt-dk",
     "$d_k = 64$ 이고 $q^{\\top} k = 12$ 이다. **스케일드 닷프로덕트 어텐션(Scaled Dot-Product Attention)** 의 점수를 구하시오. "
     "또 $d_k = 512$ 일 때 나누는 값을 구하시오.",
     "$\\sqrt{d_k}$ 로 나눠요. 둘째 답은 소수 둘째 자리까지 쓰세요.",
     [{"label": "d_k=64 일 때 점수", "ans": 1.5, "tol": 0.01},
      {"label": "d_k=512 일 때 나누는 값", "ans": 22.63, "tol": 0.02}],
     ["점수 식은 $q^{\\top} k / \\sqrt{d_k}$ 예요",
      "$\\sqrt{64} = 8$ 이에요",
      "$12 / 8 = 1.5$",
      "$\\sqrt{512} = 22.63$ 이에요"],
     "점수 1.5, 나누는 값 약 22.63",
     "$d_k$ 로 나누면 $12/64 = 0.1875$ 가 되어 틀려요. 제곱근을 꼭 씌우세요.")

calc(U5, "N4 p.37", "attention-shapes",
     "토큰 수 $n = 6$, $d_k = 8$, $d_v = 4$ 이다. $QK^{\\top}$, 소프트맥스 뒤 $A$, 최종 출력 $O$ 의 행과 열 수를 구하시오.",
     "$(a, b)$ 와 $(b, c)$ 를 곱하면 $(a, c)$ 예요. 행 수와 열 수를 각각 쓰세요.",
     [{"label": "QK^T 의 행", "ans": 6}, {"label": "QK^T 의 열", "ans": 6},
      {"label": "O 의 행", "ans": 6}, {"label": "O 의 열", "ans": 4}],
     ["$Q$ 는 $(6, 8)$, $K$ 는 $(6, 8)$ 이에요",
      "$K^{\\top}$ 는 $(8, 6)$ 이에요",
      "$(6, 8) \\times (8, 6) = (6, 6)$ 이므로 점수는 $6 \\times 6$ 이에요",
      "소프트맥스는 모양을 바꾸지 않으므로 $A$ 도 $(6, 6)$ 이에요",
      "$V$ 가 $(6, 4)$ 이므로 $(6, 6) \\times (6, 4) = (6, 4)$ 예요"],
     "$QK^{\\top}$ 는 6 x 6, $O$ 는 6 x 4",
     "교수님: transpose 위치를 외우기보다 shape 을 맞춘다고 생각하세요.")

calc(U8, "N4 p.47", "multihead-dimension",
     "$d = 512$, 헤드 수 $h = 8$ 이다. 헤드 하나의 차원과, 헤드 전체의 쿼리 투영 파라미터 수를 구하시오. "
     "(헤드 하나의 $W^Q$ 는 $d \\times (d/h)$ 크기)",
     "차원은 $d/h$, 파라미터는 헤드마다 세어서 모두 더해요.",
     [{"label": "헤드 하나의 차원 d/h", "ans": 64},
      {"label": "헤드 8개의 W^Q 파라미터 수", "ans": 262144}],
     ["$d/h = 512 / 8 = 64$ 예요",
      "헤드 하나의 $W^Q$ 는 $512 \\times 64 = 32{,}768$ 개예요",
      "헤드가 8개이므로 $32{,}768 \\times 8 = 262{,}144$ 개예요",
      "이것은 $512 \\times 512 = 262{,}144$ 와 같아요"],
     "차원 64, 파라미터 262,144 개 (싱글 헤드와 같음)",
     "교수님: 헤드를 여러 개 쓴다고 계산량이 늘어나는 게 아니에요. 나눠서 볼 뿐이에요.")

calc(U7, "N4 p.42", "ffn-parameter-count",
     "$d = 512$ 이고 $d_{ff} = 4d$ 이다. **위치별 피드포워드 신경망(Position-wise Feed-Forward Network (FFN))** 의 $W_1$, $W_2$ 파라미터 수와 그 합을 구하시오. (편향 항 제외)",
     "$W_1$ 은 $d \\times d_{ff}$, $W_2$ 는 $d_{ff} \\times d$ 예요.",
     [{"label": "d_ff", "ans": 2048}, {"label": "W1 파라미터 수", "ans": 1048576},
      {"label": "W1 + W2 합", "ans": 2097152}],
     ["$d_{ff} = 4 \\times 512 = 2048$ 이에요",
      "$W_1$ 은 $512 \\times 2048 = 1{,}048{,}576$ 개예요",
      "$W_2$ 는 $2048 \\times 512 = 1{,}048{,}576$ 개예요",
      "합은 $2{,}097{,}152$ 개이고 이는 $8d^2$ 와 같아요"],
     "$d_{ff} = 2048$, $W_1 = 1{,}048{,}576$, 합 $2{,}097{,}152$ ($= 8d^2$)",
     "어텐션 투영 네 개는 $4d^2 = 1{,}048{,}576$ 이므로 FFN 이 두 배예요.")

calc(U8, "N4 p.55", "quadratic-cost",
     "**어텐션(Attention)** 점수 행렬은 $n \\times n$ 이다. $n = 512$ 와 $n = 1024$ 일 때 칸 수를 구하고, 길이를 2배로 늘리면 칸 수가 몇 배가 되는지 구하시오.",
     "칸 수는 $n^2$ 예요.",
     [{"label": "n=512 일 때 칸 수", "ans": 262144},
      {"label": "n=1024 일 때 칸 수", "ans": 1048576},
      {"label": "몇 배", "ans": 4}],
     ["$512^2 = 262{,}144$ 예요",
      "$1024^2 = 1{,}048{,}576$ 예요",
      "$1{,}048{,}576 / 262{,}144 = 4$ 배예요",
      "길이가 2배면 칸 수는 $2^2 = 4$ 배가 돼요"],
     "262,144 칸, 1,048,576 칸, 4배",
     "선형이 아니라 제곱이에요. 그래서 긴 문맥이 가장 큰 공학 문제예요.")

calc(U2, "N4 p.13", "beam-length-normalization-calc",
     "**빔 서치(Beam Search)** 후보 A 는 3토큰으로 로그 확률 $-0.2, -0.5, -0.3$ 이고, 후보 B 는 4토큰으로 $-0.1, -0.4, -0.6, -0.5$ 이다. "
     "합계 점수와 **길이 정규화(Length Normalization)** 점수를 각각 구하시오.",
     "합계는 그냥 더하고, 정규화 점수는 토큰 수로 나눠요. 소수 넷째 자리까지 쓰세요.",
     [{"label": "A 합계", "ans": -1.0, "tol": 0.001}, {"label": "B 합계", "ans": -1.6, "tol": 0.001},
      {"label": "A 정규화", "ans": -0.3333, "tol": 0.001}, {"label": "B 정규화", "ans": -0.4, "tol": 0.001}],
     ["A 합계: $-0.2 - 0.5 - 0.3 = -1.0$",
      "B 합계: $-0.1 - 0.4 - 0.6 - 0.5 = -1.6$",
      "A 정규화: $-1.0 / 3 = -0.3333$",
      "B 정규화: $-1.6 / 4 = -0.4$",
      "둘 다 A 가 더 높아요"],
     "합계 $-1.0$ 과 $-1.6$, 정규화 $-0.3333$ 과 $-0.4$. 둘 다 A 가 이겨요.",
     "로그 확률은 음수라서 길수록 합이 작아져요. 길이로 나눠야 공평해요.")

calc(U7, "N4 p.40", "sinusoidal-pe",
     "$d = 4$ 인 **사인 코사인 위치 인코딩(Sinusoidal Positional Encoding)** 에서 자리 $pos = 1$ 의 네 칸을 구하시오. "
     "($\\sin 1 = 0.8415$, $\\cos 1 = 0.5403$, $\\sin 0.01 = 0.0100$, $\\cos 0.01 = 1.0000$)",
     "짝수 칸은 sin, 홀수 칸은 cos 이고 각도는 $pos / 10000^{2i/d}$ 예요. 소수 넷째 자리까지 쓰세요.",
     [{"label": "0번 칸", "ans": 0.8415, "tol": 0.001}, {"label": "1번 칸", "ans": 0.5403, "tol": 0.001},
      {"label": "2번 칸", "ans": 0.0100, "tol": 0.001}, {"label": "3번 칸", "ans": 1.0000, "tol": 0.001}],
     ["$i = 0$ 이면 분모가 $10000^{0} = 1$ 이라 각도는 $1$ 이에요",
      "0번 칸은 $\\sin 1 = 0.8415$, 1번 칸은 $\\cos 1 = 0.5403$ 이에요",
      "$i = 1$ 이면 분모가 $10000^{0.5} = 100$ 이라 각도는 $0.01$ 이에요",
      "2번 칸은 $\\sin 0.01 = 0.0100$, 3번 칸은 $\\cos 0.01 = 1.0000$ 이에요"],
     "$(0.8415, 0.5403, 0.0100, 1.0000)$",
     "자리마다 각도가 달라져서 무늬가 달라져요. 학습하는 값이 아니라 계산하는 값이에요.")

# =====================================================================
raw = json.dumps(bank, ensure_ascii=False, indent=1)
for ch in ("—", "–", "·", "・"):
    assert ch not in raw, ch
with open(OUT, "w", encoding="utf-8") as f:
    f.write(raw)
print("saved", OUT, len(bank), "문항", cnt)
