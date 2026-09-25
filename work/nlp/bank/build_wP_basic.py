# -*- coding: utf-8 -*-
"""참고 논문 주차(NP Attention Is All You Need, Vaswani et al. 2017) basic 문제은행 생성기.
출력: work/nlp/bank/wP_basic.json
사실은 논문(work/nlp/_src/NP.txt 와 png/NP/pNNN.png)에서만 가져온다. 뒤에 나온 논문
(BERT, RoPE, Pre-LN 등)의 지식은 섞지 않는다. 4주차 강의 슬라이드와 다른 대목은
해설에서 "논문은 ..., 4주차 슬라이드는 ..." 으로 밝힌다.
계산 문항 정답은 아래에서 파이썬으로 실제 계산하고 assert 로 확인한다."""
import json, math, os
import optshuffle

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "wP_basic.json")

U1 = "P-1 초록과 논문의 주장"
U2 = "P-2 1 Introduction 과 2 Background"
U3 = "P-3 3.1 인코더와 디코더 스택"
U4 = "P-4 3.2.1 스케일드 닷프로덕트 어텐션"
U5 = "P-5 3.2.2 멀티 헤드와 3.2.3 세 가지 쓰임"
U6 = "P-6 3.3 FFN, 3.4 임베딩, 3.5 위치 인코딩"
U7 = "P-7 4 Why Self-Attention 과 Table 1"
U8 = "P-8 5 Training 설정"
U9 = "P-9 6 Results, 7 Conclusion, 어텐션 그림"


# =====================================================================
# 계산 확인 (표준 라이브러리만 쓴다)
# =====================================================================
def softmax(xs):
    m = max(xs)
    e = [math.exp(x - m) for x in xs]
    s = sum(e)
    return [v / s for v in e]


# C1 스케일드 닷프로덕트: d_k = 64, 원점수 [16, 8, 0]
DK = 64
assert math.sqrt(DK) == 8.0
RAW = [16.0, 8.0, 0.0]
SCALED = [r / math.sqrt(DK) for r in RAW]
assert SCALED == [2.0, 1.0, 0.0]
W = softmax(SCALED)
assert [round(v, 4) for v in W] == [0.6652, 0.2447, 0.0900]
assert round(sum(W), 10) == 1.0

# C2 가중합 (반올림한 가중치로 계산한다)
WR = [0.6652, 0.2447, 0.0900]
V = [[1.0, 0.0], [0.0, 2.0], [2.0, 2.0]]
CTX = [sum(WR[i] * V[i][j] for i in range(3)) for j in range(2)]
assert [round(v, 4) for v in CTX] == [0.8452, 0.6694]

# C3 스케일을 하지 않았을 때
WNO = softmax(RAW)
assert [round(v, 6) for v in WNO] == [0.999665, 0.000335, 0.000000]

# C4 파라미터 수 (논문이 직접 적지 않은 값. 우리가 직접 세어 본 것)
DM, H, DFF = 512, 8, 2048
assert DM // H == 64
WQ_HEAD = DM * (DM // H)
assert WQ_HEAD == 32768
MHA = 4 * DM * DM
assert MHA == 1048576
FFN1 = DM * DFF
FFN2 = DFF * DM
assert FFN1 == 1048576 and FFN1 + FFN2 == 2097152
ENC_LAYER = MHA + FFN1 + FFN2
assert ENC_LAYER == 3145728
assert DFF // DM == 4

# C5 Table 1 손계산 (d = 512)
D = 512
assert 100 ** 2 * D == 5120000
assert 100 * D ** 2 == 26214400
assert round((100 * D ** 2) / (100 ** 2 * D), 2) == 5.12
assert 512 ** 2 * D == 512 * D ** 2 == 134217728
assert 1000 ** 2 * D == 512000000
assert 1000 * D ** 2 == 262144000

# C6 위치 인코딩 (d_model = 4)
def pe_row(pos, d=4):
    out = []
    for i in range(d // 2):
        ang = pos / (10000 ** (2 * i / d))
        out.append(round(math.sin(ang), 4))
        out.append(round(math.cos(ang), 4))
    return out


assert pe_row(0) == [0.0, 1.0, 0.0, 1.0]
assert pe_row(1) == [0.8415, 0.5403, 0.01, 1.0]
assert pe_row(2) == [0.9093, -0.4161, 0.02, 0.9998]

bank = []
cnt = {}


def add(t, unit, slides, src=None, **kw):
    cnt[t] = cnt.get(t, 0) + 1
    item = {"id": "wPb-%s-%03d" % (t, cnt[t]), "type": t, "part": "P", "level": "basic",
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
# MCQ (30)
# =====================================================================
mcq(U1, "NP p.1",
    "논문 초록(Abstract)이 제안한 **트랜스포머(Transformer)** 의 핵심 주장으로 가장 적절한 것은?",
    ["순환(recurrence)과 합성곱(convolution)을 완전히 걷어내고 **어텐션(Attention)** 만으로 세운 구조이다",
     "**순환 신경망(Recurrent Neural Network (RNN))** 에 어텐션을 덧붙여 성능을 올린 구조이다",
     "**합성곱 신경망(Convolutional Neural Network (CNN))** 에 어텐션을 덧붙여 성능을 올린 구조이다",
     "어텐션을 쓰지 않고 순환만으로 세운 구조이다"],
    0,
    "초록 원문은 'a new simple network architecture, the Transformer, based solely on attention mechanisms, "
    "dispensing with recurrence and convolutions entirely' 예요. "
    "어텐션을 덧붙인 구조는 초록이 기존 모델을 설명한 말('The best performing models also connect the encoder and decoder "
    "through an attention mechanism')이라 가장 헷갈리지만 정답이 아니에요.")

mcq(U1, "NP p.1",
    "초록이 적은 WMT 2014 English-to-German 번역 과제의 BLEU 점수로 옳은 것은?",
    ["23.75", "26.36", "28.4", "41.8"],
    2,
    "초록: 'Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task.' "
    "41.8 은 같은 초록의 English-to-French 점수이고, 26.36 은 Table 2 의 ConvS2S Ensemble 점수예요.")

mcq(U1, "NP p.1",
    "초록이 밝힌 English-to-French 모델의 학습 기간과 장비로 옳은 것은?",
    ["GPU 8장으로 3.5일", "GPU 8장으로 12시간", "GPU 16장으로 3.5일", "GPU 8장으로 100시간"],
    0,
    "초록: 'after training for 3.5 days on eight GPUs'. "
    "12시간은 1 Introduction 이 base 모델을 두고 한 말('as little as twelve hours on eight P100 GPUs')이라 헷갈리기 쉬워요.")

mcq(U2, "NP p.2",
    "논문 1 Introduction 이 **순환 신경망(Recurrent Neural Network (RNN))** 의 근본 한계로 든 것은?",
    ["**은닉 상태(Hidden State)** 의 차원이 너무 작다",
     "위치를 따라 차례로 계산해야 해서 한 학습 예제 안에서 **병렬화(Parallelization)** 가 막힌다",
     "**어텐션(Attention)** 을 함께 쓸 수 없다",
     "문장이 길어지면 **파라미터(Parameter)** 수가 같이 늘어난다"],
    1,
    "원문: 'This inherently sequential nature precludes parallelization within training examples.' "
    "메모리 제약 때문에 예제끼리 묶는 배칭도 제한된다고 덧붙였어요. "
    "파라미터가 늘어난다는 말은 논문에 없어요. RNN 은 같은 파라미터를 재사용해요.")

mcq(U2, "NP p.2",
    "논문 2 Background 가 적은, 멀리 떨어진 두 위치의 신호를 잇는 데 드는 연산 수의 증가 방식으로 옳은 것은?",
    ["ConvS2S 는 로그로, ByteNet 은 선형으로 늘고 트랜스포머는 상수이다",
     "ConvS2S 는 선형으로, ByteNet 은 로그로 늘고 트랜스포머는 상수이다",
     "셋 다 거리에 비례해 선형으로 늘어난다",
     "ConvS2S 는 상수, ByteNet 은 선형, 트랜스포머는 로그이다"],
    1,
    "원문: 'linearly for ConvS2S and logarithmically for ByteNet ... In the Transformer this is reduced to a "
    "constant number of operations.' 두 모델의 짝을 바꿔 놓은 보기가 가장 헷갈려요.")

mcq(U2, "NP p.2",
    "트랜스포머가 연산 수를 상수로 줄이면서 치른 대가와 그 대책으로 논문이 적은 것은?",
    ["어텐션 가중 평균 때문에 유효 해상도가 떨어지고, **멀티 헤드 어텐션(Multi-Head Attention (MHA))** 으로 이를 상쇄한다",
     "메모리가 늘어나고, **드롭아웃(Dropout)** 으로 이를 상쇄한다",
     "학습이 느려지고, **워밍업(Warmup)** 으로 이를 상쇄한다",
     "순서 정보가 사라지고, **잔차 연결(Residual Connection)** 으로 이를 상쇄한다"],
    0,
    "원문: 'albeit at the cost of reduced effective resolution due to averaging attention-weighted positions, "
    "an effect we counteract with Multi-Head Attention.' "
    "순서 정보가 사라지는 문제는 3.5 절의 **위치 인코딩(Positional Encoding)** 이 맡으므로 다른 이야기예요.")

mcq(U3, "NP p.3",
    "논문이 못박은 인코더와 디코더의 층 수 $N$ 으로 옳은 것은?",
    ["$N = 4$", "$N = 6$", "$N = 8$", "$N = 12$"],
    1,
    "원문: 'The encoder is composed of a stack of $N = 6$ identical layers.' 디코더도 'also composed of a stack of "
    "$N = 6$ identical layers' 예요. 4주차 강의 슬라이드는 N 을 정하지 않고 'Stack it N times' 라고만 했지만, "
    "논문은 6 으로 못박았어요. $N = 8$ 은 Table 3 의 (C) 행에서 시험해 본 값이에요.")

mcq(U3, "NP p.3",
    "논문에 따른 인코더 한 층의 **하위층(Sub-layer)** 구성으로 옳은 것은?",
    ["멀티 헤드 **셀프 어텐션(Self-Attention)** 하나와 **위치별 피드포워드 신경망(Position-wise Feed-Forward Network (FFN))** 하나, 모두 둘",
     "멀티 헤드 **셀프 어텐션(Self-Attention)** 하나, 인코더-디코더 어텐션 하나, **위치별 피드포워드 신경망(Position-wise Feed-Forward Network (FFN))** 하나, 모두 셋",
     "**위치별 피드포워드 신경망(Position-wise Feed-Forward Network (FFN))** 만 둘",
     "멀티 헤드 **셀프 어텐션(Self-Attention)** 만 둘"],
    0,
    "원문: 'Each layer has two sub-layers. The first is a multi-head self-attention mechanism, and the second is "
    "a simple, position-wise fully connected feed-forward network.' "
    "하위층이 셋인 것은 인코더가 아니라 디코더예요.")

mcq(U3, "NP p.3",
    "논문이 적은 각 **하위층(Sub-layer)** 의 출력 식으로 옳은 것은?",
    [r"$x + \mathrm{LayerNorm}(\mathrm{Sublayer}(x))$",
     r"$\mathrm{LayerNorm}(x + \mathrm{Sublayer}(x))$",
     r"$\mathrm{Sublayer}(\mathrm{LayerNorm}(x))$",
     r"$\mathrm{LayerNorm}(\mathrm{Sublayer}(x))$"],
    1,
    "원문: 'the output of each sub-layer is LayerNorm(x + Sublayer(x))'. "
    "먼저 **잔차 연결(Residual Connection)** 로 더하고, 그다음에 **층 정규화(Layer Normalization (LayerNorm))** 를 해요. "
    "정규화를 먼저 하고 더하는 보기는 4주차 슬라이드가 소개한 Pre-LN 쪽 이야기이고 이 논문에는 없어요.")

mcq(U4, "NP p.4",
    "논문 식 (1) 의 **스케일드 닷프로덕트 어텐션(Scaled Dot-Product Attention)** 으로 옳은 것은?",
    [r"$\mathrm{softmax}(QK^{T}/\sqrt{d_k})V$",
     r"$\mathrm{softmax}(QK^{T}/d_k)V$",
     r"$\mathrm{softmax}(QK^{T}V/\sqrt{d_k})$",
     r"$\mathrm{softmax}(Q^{T}K/\sqrt{d_k})V$"],
    0,
    r"식 (1) 은 $\mathrm{Attention}(Q, K, V) = \mathrm{softmax}(QK^{T}/\sqrt{d_k})V$ 예요. "
    r"나누는 값은 $d_k$ 가 아니라 $\sqrt{d_k}$ 이고, $V$ 는 소프트맥스 안이 아니라 밖에서 곱해요.")

mcq(U4, "NP p.4",
    "논문이 **내적(Dot Product)** 점수를 나누는 값으로 옳은 것은?",
    [r"$d_k$", r"$\sqrt{d_k}$", r"$d_{model}$", r"$\sqrt{d_{model}}$"],
    1,
    r"3.2.1: 'divide each by $\sqrt{d_k}$'. base 모델은 $d_k = 64$ 라서 나누는 값이 8 이에요. "
    r"4주차 강의 슬라이드는 $d_k = 512$ 로 예를 들었지만, 논문 기준으로 512 는 $d_{model}$ 이고 헤드 하나의 $d_k$ 는 64 예요.")

mcq(U4, "NP p.4",
    "**가산 어텐션(Additive Attention)** 과 **닷프로덕트 어텐션(Dot-Product Attention)** 의 차이로 옳은 것은?",
    ["가산 어텐션은 은닉층이 하나인 피드포워드 신경망으로 **호환성 함수(Compatibility Function)** 를 계산한다",
     "가산 어텐션은 **쿼리(Query)** 와 **키(Key)** 를 그냥 **내적(Dot Product)** 해서 점수를 만든다",
     "닷프로덕트 어텐션은 은닉층이 둘인 신경망을 써서 점수를 만든다",
     "둘은 이론적 복잡도도 실제 속도도 완전히 같다"],
    0,
    "원문: 'Additive attention computes the compatibility function using a feed-forward network with a single "
    "hidden layer.' 이론적 복잡도는 비슷하지만, 실제로는 닷프로덕트 쪽이 최적화된 행렬곱으로 구현돼 더 빠르고 메모리도 아껴요. "
    "그래서 '완전히 같다' 는 보기는 앞 절반만 맞아요.")

mcq(U4, "NP p.4",
    r"점수를 $\sqrt{d_k}$ 로 나누는 까닭을 논문이 적은 방식으로 가장 적절한 것은?",
    [r"'We suspect' 라고 적어, $d_k$ 가 크면 내적이 커져 **소프트맥스(Softmax)** 가 **기울기(Gradient)** 가 아주 작은 영역으로 밀린다고 추측했다",
     "실험으로 증명했다고 단정해서 적었다",
     "이미 증명된 정리를 인용해서 적었다",
     "까닭을 전혀 적지 않고 값만 적었다"],
    0,
    r"원문: 'We suspect that for large values of $d_k$, the dot products grow large in magnitude, pushing the "
    r"softmax function into regions where it has extremely small gradients.' "
    r"논문이 단정하지 않고 추측이라고 밝힌 대목이에요. 각주 4 의 분산 계산은 왜 커지는지를 보여 주는 예시일 뿐 증명이 아니에요.")

mcq(U5, "NP p.5",
    "논문 base 모델의 헤드 수 $h$ 와 $d_k$, $d_v$ 로 옳은 것은?",
    ["$h = 8$, $d_k = d_v = 64$", "$h = 8$, $d_k = d_v = 512$",
     "$h = 16$, $d_k = d_v = 64$", "$h = 6$, $d_k = d_v = 64$"],
    0,
    r"원문: 'we employ $h = 8$ parallel attention layers, or heads. For each of these we use "
    r"$d_k = d_v = d_{model}/h = 64$.' $h = 16$ 은 Table 3 의 big 모델 설정이고, 그때 $d_k$ 는 64 가 아니에요.")

mcq(U5, "NP p.5",
    "**멀티 헤드 어텐션(Multi-Head Attention (MHA))** 의 출력 투영 $W^O$ 의 크기로 옳은 것은?",
    ["$h d_v \\times d_{model}$", "$d_{model} \\times d_k$",
     "$d_{model} \\times h d_v$", "$d_k \\times d_v$"],
    0,
    r"원문: '$W^O \in \mathbb{R}^{h d_v \times d_{model}}$'. 헤드들을 이어 붙인 $h d_v$ 차원을 다시 $d_{model}$ 로 되돌려요. "
    r"$d_{model} \times d_k$ 는 헤드 하나의 $W_i^Q$ 크기라서 가장 헷갈려요.")

mcq(U5, "NP p.5",
    "논문 3.2.3 의 encoder-decoder attention 층에서 쿼리, 키, 밸류의 출처로 옳은 것은?",
    ["**쿼리(Query)** 는 앞 디코더 층에서, **키(Key)** 와 **밸류(Value)** 는 인코더 스택의 출력에서 온다",
     "**쿼리(Query)**, **키(Key)**, **밸류(Value)** 가 모두 인코더 스택의 출력에서 온다",
     "**쿼리(Query)** 는 인코더 스택의 출력에서, **키(Key)** 와 **밸류(Value)** 는 앞 디코더 층에서 온다",
     "**쿼리(Query)**, **키(Key)**, **밸류(Value)** 가 모두 앞 디코더 층에서 온다"],
    0,
    "원문: 'the queries come from the previous decoder layer, and the memory keys and values come from the output "
    "of the encoder.' 셋이 모두 같은 곳에서 오는 것은 **셀프 어텐션(Self-Attention)** 이에요.")

mcq(U5, "NP p.5",
    "디코더 셀프 어텐션에서 뒤쪽 위치를 보지 못하게 막는 구현 방식으로 옳은 것은?",
    [r"**소프트맥스(Softmax)** 입력에서 허용되지 않는 연결의 값을 $-\infty$ 로 바꾼다",
     "**소프트맥스(Softmax)** 를 거친 뒤의 **어텐션 가중치(Attention Weight)** 를 0 으로 바꾼다",
     "**키(Key)** 행렬에서 뒤쪽 열을 아예 지운다",
     "디코더에서는 **어텐션(Attention)** 을 건너뛰고 FFN 만 쓴다"],
    0,
    r"원문: 'masking out (setting to $-\infty$) all values in the input of the softmax which correspond to illegal "
    r"connections.' 마스킹은 소프트맥스 앞에서 해요. 소프트맥스 뒤에 0 을 넣으면 가중치의 합이 1 이 되지 않아요.")

mcq(U6, "NP p.5",
    "논문 식 (2) 의 **위치별 피드포워드 신경망(Position-wise Feed-Forward Network (FFN))** 으로 옳은 것은?",
    [r"$\max(0, xW_1 + b_1)W_2 + b_2$",
     r"$\max(0, xW_1W_2 + b_1)$",
     r"$xW_1 + \max(0, W_2 + b_2)$",
     r"$\mathrm{softmax}(xW_1 + b_1)W_2 + b_2$"],
    0,
    r"식 (2) 는 $\mathrm{FFN}(x) = \max(0, xW_1 + b_1)W_2 + b_2$ 예요. "
    r"가운데 활성화는 **소프트맥스(Softmax)** 가 아니라 **렐루(ReLU)** 이고, 선형 변환이 두 번 들어가요.")

mcq(U6, "NP p.5",
    "논문이 FFN 을 달리 표현한 말로 옳은 것은?",
    ["커널 크기가 1 인 **합성곱(Convolution)** 두 번",
     "커널 크기가 3 인 합성곱 두 번",
     "**순환 신경망(Recurrent Neural Network (RNN))** 한 층",
     "헤드가 하나인 어텐션 한 층"],
    0,
    "원문: 'Another way of describing this is as two convolutions with kernel size 1.' "
    "커널이 1 이라 자리끼리 섞이지 않고 각 위치에 따로따로 같은 변환이 걸려요. "
    "같은 층 안에서는 모든 자리에 같은 파라미터를 쓰지만 층이 달라지면 다른 파라미터를 써요.")

mcq(U6, "NP p.5",
    "논문 3.4 Embeddings and Softmax 의 내용으로 옳은 것은?",
    [r"두 임베딩 층과 소프트맥스 앞 선형 변환이 같은 가중치 행렬을 공유하고, 임베딩 층에서는 그 가중치에 $\sqrt{d_{model}}$ 을 곱한다",
     "두 임베딩 층은 서로 다른 행렬을 쓰고 소프트맥스 앞 선형 변환만 그중 하나와 공유한다",
     r"세 자리가 가중치를 공유하고, 임베딩 층에서는 가중치에 $d_{model}$ 을 곱한다",
     "임베딩은 학습하지 않고 고정한 값을 쓴다"],
    0,
    r"원문: 'we share the same weight matrix between the two embedding layers and the pre-softmax linear "
    r"transformation ... In the embedding layers, we multiply those weights by $\sqrt{d_{model}}$.' "
    r"곱하는 값은 $d_{model}$ 이 아니라 $\sqrt{d_{model}}$ 이라 세 번째 보기가 가장 헷갈려요.")

mcq(U6, "NP p.6",
    "**사인 코사인 위치 인코딩(Sinusoidal Positional Encoding)** 의 파장에 대한 논문 서술로 옳은 것은?",
    [r"$2\pi$ 에서 $10000 \cdot 2\pi$ 까지 등비수열을 이룬다",
     r"$2\pi$ 에서 $512 \cdot 2\pi$ 까지 등차수열을 이룬다",
     "모든 차원이 같은 파장을 쓴다",
     r"$0$ 에서 $2\pi$ 까지 등비수열을 이룬다"],
    0,
    r"원문: 'The wavelengths form a geometric progression from $2\pi$ to $10000 \cdot 2\pi$.' "
    r"등차가 아니라 등비이고, 차원마다 파장이 달라요. 논문이 $10000 \cdot 2\pi$ 라고 적은 것은 어림한 표현이에요.")

mcq(U7, "NP p.6",
    "Table 1 에서 Self-Attention 행의 층당 복잡도, **순차 연산 수(Sequential Operations)**, "
    "**최대 경로 길이(Maximum Path Length)** 로 옳은 것은?",
    [r"층당 복잡도 $O(n^2 \cdot d)$, 순차 연산 수 $O(1)$, 최대 경로 길이 $O(1)$",
     r"층당 복잡도 $O(n \cdot d^2)$, 순차 연산 수 $O(1)$, 최대 경로 길이 $O(1)$",
     r"층당 복잡도 $O(n^2 \cdot d)$, 순차 연산 수 $O(n)$, 최대 경로 길이 $O(n)$",
     r"층당 복잡도 $O(k \cdot n \cdot d^2)$, 순차 연산 수 $O(1)$, 최대 경로 길이 $O(\log_k(n))$"],
    0,
    r"Table 1 의 Self-Attention 행은 $O(n^2 \cdot d)$, $O(1)$, $O(1)$ 이에요. "
    r"$O(n \cdot d^2)$ 와 $O(n)$ 은 Recurrent 행, $O(k \cdot n \cdot d^2)$ 는 Convolutional 행이에요.")

mcq(U7, "NP p.6",
    "Table 1 에서 Recurrent 층의 **순차 연산 수(Sequential Operations)** 로 옳은 것은?",
    [r"$O(1)$", r"$O(n)$", r"$O(n^2)$", r"$O(\log_k(n))$"],
    1,
    r"Recurrent 행만 순차 연산 수가 $O(n)$ 이에요. 나머지 세 행은 모두 $O(1)$ 이라서 병렬로 한 번에 계산할 수 있어요. "
    r"$O(\log_k(n))$ 은 Convolutional 행의 최대 경로 길이 칸이에요.")

mcq(U7, "NP p.6",
    "논문 4 Why Self-Attention 이 층 종류를 비교한 세 가지 기준(desiderata)으로 옳은 것은?",
    ["층당 총 계산 복잡도, 병렬화할 수 있는 계산량(최소 순차 연산 수), 장거리 의존성의 경로 길이",
     "파라미터 수, 학습 시간, 메모리 사용량",
     "BLEU, **퍼플렉서티(Perplexity (PPL))**, F1 점수",
     "층 수, 헤드 수, **어휘(Vocabulary)** 크기"],
    0,
    "원문: 'Motivating our use of self-attention we consider three desiderata.' 세 가지는 총 계산 복잡도, "
    "병렬화 가능한 계산량, 경로 길이예요. BLEU 와 퍼플렉서티는 6장 결과에서 쓰는 성능 지표이지 4장의 비교 기준이 아니에요.")

mcq(U8, "NP p.7",
    "논문이 쓴 **아담(Adam)** 의 하이퍼파라미터로 옳은 것은?",
    [r"$\beta_1 = 0.9$, $\beta_2 = 0.98$, $\epsilon = 10^{-9}$",
     r"$\beta_1 = 0.9$, $\beta_2 = 0.999$, $\epsilon = 10^{-8}$",
     r"$\beta_1 = 0.98$, $\beta_2 = 0.9$, $\epsilon = 10^{-9}$",
     r"$\beta_1 = 0.9$, $\beta_2 = 0.98$, $\epsilon = 10^{-6}$"],
    0,
    r"원문: 'We used the Adam optimizer with $\beta_1 = 0.9$, $\beta_2 = 0.98$ and $\epsilon = 10^{-9}$.' "
    r"$\beta_2 = 0.999$ 나 $\epsilon = 10^{-8}$ 은 논문에 없는 값이에요. 두 수를 서로 바꿔 놓은 보기도 조심하세요.")

mcq(U8, "NP p.7",
    "논문의 학습률 식 (3) 에서 warmup_steps 값으로 옳은 것은?",
    ["1000", "2000", "4000", "8000"],
    2,
    "원문: 'We used warmup_steps = 4000.' 이 스텝까지는 학습률이 선형으로 오르고, 그 뒤에는 스텝 수의 역제곱근에 "
    "비례해 줄어들어요. 그래서 학습률이 가장 높은 지점이 바로 4000 스텝이에요.")

mcq(U8, "NP p.8",
    r"**라벨 스무딩(Label Smoothing)** $\epsilon_{ls} = 0.1$ 이 **퍼플렉서티(Perplexity (PPL))**, 정확도, BLEU 에 "
    r"미치는 효과로 논문이 적은 것은?",
    ["퍼플렉서티는 나빠지지만 정확도와 BLEU 는 좋아진다",
     "퍼플렉서티도 정확도도 BLEU 도 모두 좋아진다",
     "퍼플렉서티는 좋아지지만 BLEU 는 나빠진다",
     "세 가지 모두 거의 변하지 않는다"],
    0,
    "원문: 'This hurts perplexity, as the model learns to be more unsure, but improves accuracy and BLEU score.' "
    "모델이 정답을 100% 라고 말하지 않도록 배우기 때문에 퍼플렉서티는 나빠져요. 좋아지는 쪽과 나빠지는 쪽을 뒤집은 보기를 조심하세요.")

mcq(U9, "NP p.8",
    "논문이 번역 실험의 추론에 쓴 **빔 크기(Beam Size)** 와 길이 페널티, 최대 출력 길이로 옳은 것은?",
    [r"빔 크기 4, 길이 페널티 $\alpha = 0.6$, 최대 출력 길이는 입력 길이 + 50",
     r"빔 크기 21, 길이 페널티 $\alpha = 0.3$, 최대 출력 길이는 입력 길이 + 50",
     r"빔 크기 4, 길이 페널티 $\alpha = 0.3$, 최대 출력 길이는 입력 길이 + 300",
     r"빔 크기 10, 길이 페널티 $\alpha = 0.6$, 최대 출력 길이는 입력 길이 + 100"],
    0,
    r"6.1 원문: 'We used beam search with a beam size of 4 and length penalty $\alpha = 0.6$ ... maximum output "
    r"length during inference to input length + 50.' 빔 크기 21 과 $\alpha = 0.3$, 입력 길이 + 300 은 6.3 의 "
    r"**구성소 구문 분석(Constituency Parsing)** 설정이라 가장 헷갈려요.")

mcq(U9, "NP p.9",
    "Table 3 의 (E) 행이 보여 준 결과로 옳은 것은?",
    ["사인 코사인 대신 학습하는 위치 임베딩을 써도 base 와 거의 같았다",
     "학습하는 위치 임베딩이 base 보다 BLEU 가 2 이상 높았다",
     "학습하는 위치 임베딩을 쓰면 학습이 발산했다",
     "위치 정보를 아예 빼도 성능이 그대로였다"],
    0,
    "원문: 'In row (E) we replace our sinusoidal positional encoding with learned positional embeddings, and "
    "observe nearly identical results to the base model.' (E) 는 PPL 4.92, BLEU 25.7 로 base(4.92, 25.8)와 거의 같아요. "
    "위치 정보를 아예 뺀 실험은 논문에 없어요.")

mcq(U9, "NP p.14",
    "논문 Figure 4 에 대한 설명으로 옳은 것은?",
    ["layer 5 of 6 의 두 헤드가 'its' 의 지시 대상을 찾는 것처럼 보인다고 적었다",
     "디코더에서 마스킹이 어떻게 걸리는지를 그림으로 보여 준다",
     "인코더-디코더 어텐션이 두 언어의 단어를 짝지어 주는 모습을 보여 준다",
     "한 층 안의 모든 헤드가 똑같은 일을 한다는 것을 보여 준다"],
    0,
    "원문: 'Two attention heads, also in layer 5 of 6, apparently involved in anaphora resolution ... Isolated "
    "attentions from just the word its for attention heads 5 and 6.' 논문은 'apparently' 라고 적어 단정하지 않았어요. "
    "헤드가 서로 다른 일을 배웠다는 예는 Figure 5 라서 마지막 보기는 반대예요.")

# =====================================================================
# OX (20, 절반이 거짓)
# =====================================================================
ox(U1, "NP p.1",
   "논문 초록은 트랜스포머가 품질이 더 좋으면서 병렬화하기도 쉽고 학습 시간도 훨씬 적게 든다고 적었어요.",
   True,
   "원문: 'these models to be superior in quality while being more parallelizable and requiring significantly "
   "less time to train.' 세 가지를 한 문장에 같이 적었어요.")

ox(U1, "NP p.1",
   "논문 초록은 트랜스포머를 기계 번역에만 적용했고 다른 과제에는 적용하지 않았다고 적었어요.",
   False,
   "초록 마지막 문장은 'We show that the Transformer generalizes well to other tasks by applying it successfully "
   "to English constituency parsing both with large and limited training data' 예요. "
   "**구성소 구문 분석(Constituency Parsing)** 실험이 6.3 절과 Table 4 에 있어요.")

ox(U2, "NP p.2",
   "논문 2 Background 는 **셀프 어텐션(Self-Attention)** 을 intra-attention 이라고도 부른다고 적으면서, "
   "셀프 어텐션 자체를 이 논문이 처음 제안했다고 밝혔어요.",
   False,
   "논문은 셀프 어텐션이 독해, 요약, 함의 판단 같은 과제에 이미 성공적으로 쓰였다고 적었어요. "
   "논문이 '처음' 이라고 말한 것은 셀프 어텐션 자체가 아니라, 순환이나 합성곱 없이 셀프 어텐션만으로 "
   "입력과 출력의 표현을 계산하는 **시퀀스 변환(Sequence Transduction)** 모델이라는 점이에요.")

ox(U2, "NP p.2",
   "논문 1 Introduction 은 트랜스포머가 P100 GPU 8장으로 열두 시간 정도만 학습해도 번역 품질에서 새로운 최고 기록에 "
   "이를 수 있다고 적었어요.",
   True,
   "원문: 'can reach a new state of the art in translation quality after being trained for as little as twelve "
   "hours on eight P100 GPUs.' 5.2 절의 base 모델 학습 시간 12시간과 같은 이야기예요.")

ox(U3, "NP p.3",
   "논문에서 모든 **하위층(Sub-layer)** 과 임베딩 층의 출력 차원은 $d_{model} = 512$ 로 같고, 그 까닭은 "
   "**잔차 연결(Residual Connection)** 을 쉽게 하기 위해서예요.",
   True,
   "원문: 'To facilitate these residual connections, all sub-layers in the model, as well as the embedding "
   "layers, produce outputs of dimension $d_{model} = 512$.' 더하려면 모양이 같아야 하니까요.")

ox(U3, "NP p.3",
   r"논문은 하위층의 출력을 $x + \mathrm{LayerNorm}(\mathrm{Sublayer}(x))$ 라고 적어서, 정규화를 한 뒤에 입력을 더해요.",
   False,
   r"논문이 적은 식은 $\mathrm{LayerNorm}(x + \mathrm{Sublayer}(x))$ 예요. 먼저 더하고 그다음에 정규화하는 순서라서 "
   r"괄호 자리가 반대예요. 정규화를 먼저 하는 방식은 4주차 슬라이드가 소개한 Pre-LN 이고 논문에는 없어요.")

ox(U4, "NP p.4",
   "논문은 **닷프로덕트 어텐션(Dot-Product Attention)** 이 **가산 어텐션(Additive Attention)** 과 이론적 복잡도는 "
   "비슷하지만 실제로는 더 빠르고 메모리도 아낀다고 적었어요.",
   True,
   "원문: 'While the two are similar in theoretical complexity, dot-product attention is much faster and more "
   "space-efficient in practice, since it can be implemented using highly optimized matrix multiplication code.'")

ox(U4, "NP p.4",
   r"논문 각주 4 는 $q$ 와 $k$ 의 각 성분이 평균 0, 분산 1 인 독립 확률변수이면 내적 $q \cdot k$ 의 분산이 "
   r"$\sqrt{d_k}$ 가 된다고 적었어요.",
   False,
   r"각주 4 가 적은 분산은 $\sqrt{d_k}$ 가 아니라 $d_k$ 예요. 분산이 $d_k$ 라서 표준편차가 $\sqrt{d_k}$ 가 되고, "
   r"그래서 점수를 $\sqrt{d_k}$ 로 나눠 준다는 이야기로 이어져요.")

ox(U4, "NP p.4",
   r"$d_k$ 가 작을 때는 두 어텐션의 성능이 비슷하지만, $d_k$ 가 커지면 스케일링 없는 닷프로덕트보다 가산 어텐션이 "
   r"낫다고 논문이 적었어요.",
   True,
   r"원문: 'While for small values of $d_k$ the two mechanisms perform similarly, additive attention outperforms "
   r"dot product attention without scaling for larger values of $d_k$.' 이것이 스케일링을 넣은 출발점이에요.")

ox(U5, "NP p.5",
   "논문은 헤드를 8개 쓰면 단일 헤드보다 전체 계산 비용이 약 8배가 된다고 적었어요.",
   False,
   "원문: 'Due to the reduced dimension of each head, the total computational cost is similar to that of "
   "single-head attention with full dimensionality.' 차원을 $h$ 로 나눠서 보기 때문에 비용이 비슷해요. "
   "헤드를 늘린다고 전체 차원을 키우는 것이 아니에요.")

ox(U5, "NP p.5",
   "논문은 멀티 헤드가 서로 다른 **표현 부분공간(Representation Subspace)** 의 정보에 동시에 주목하게 해 주고, "
   "헤드가 하나면 평균 때문에 그것이 막힌다고 적었어요.",
   True,
   "원문: 'Multi-head attention allows the model to jointly attend to information from different representation "
   "subspaces at different positions. With a single attention head, averaging inhibits this.' "
   "헤드가 실제로 무엇을 배우는지에 대한 연구는 논문 밖 이야기예요.")

ox(U6, "NP p.6",
   "논문은 **위치 인코딩(Positional Encoding)** 을 입력 임베딩에 더한다고 적었고, 더할 수 있도록 위치 인코딩의 "
   "차원을 임베딩과 같은 $d_{model}$ 로 맞췄어요.",
   True,
   "원문: 'we add positional encodings to the input embeddings at the bottoms of the encoder and decoder stacks. "
   "The positional encodings have the same dimension $d_{model}$ as the embeddings, so that the two can be summed.' "
   "곱하는 것이 아니라 더해요.")

ox(U6, "NP p.6",
   "논문은 순서 정보가 없는 성질에 **순열 등변성(Permutation Equivariance)** 이라는 이름을 붙여 설명했어요.",
   False,
   "논문은 이름을 붙이지 않고 'in order for the model to make use of the order of the sequence' 라고만 적었어요. "
   "순열 등변성이라는 말은 4주차 강의 슬라이드에서 쓴 이름이고 논문에는 없어요. "
   "논문이 적은 이유는 'our model contains no recurrence and no convolution' 이에요.")

ox(U7, "NP p.7",
   "논문은 문장 길이 $n$ 이 표현 차원 $d$ 보다 작을 때 셀프 어텐션 층이 순환 층보다 빠르다고 적었고, 기계 번역이 쓰는 "
   "word-piece 나 byte-pair 표현에서는 대개 그렇다고 덧붙였어요.",
   True,
   "원문: 'self-attention layers are faster than recurrent layers when the sequence length $n$ is smaller than "
   "the representation dimensionality $d$, which is most often the case with sentence representations used by "
   "state-of-the-art models in machine translations.'")

ox(U7, "NP p.6",
   r"Table 1 에서 **제한된 셀프 어텐션(Restricted Self-Attention)** 의 **최대 경로 길이(Maximum Path Length)** 는 $O(1)$ 이에요.",
   False,
   r"Table 1 의 Self-Attention (restricted) 행은 층당 복잡도 $O(r \cdot n \cdot d)$, 순차 연산 수 $O(1)$, "
   r"최대 경로 길이 $O(n/r)$ 예요. $O(1)$ 은 제한하지 않은 셀프 어텐션 쪽이에요. 가까운 $r$ 칸만 보면 값이 싸지는 대신 "
   r"먼 자리까지 가는 걸음 수가 늘어나요.")

ox(U8, "NP p.7",
   "논문은 학습 배치를 비슷한 길이끼리 묶었고, 한 배치에 원문 토큰 약 25,000개와 번역문 토큰 약 25,000개가 들어가게 했어요.",
   True,
   "원문: 'Sentence pairs were batched together by approximate sequence length. Each training batch contained a "
   "set of sentence pairs containing approximately 25000 source tokens and 25000 target tokens.' "
   "문장 수가 아니라 토큰 수로 배치 크기를 맞췄다는 점이 중요해요.")

ox(U8, "NP p.7",
   "논문은 base 모델을 300,000 스텝, big 모델을 100,000 스텝 학습했다고 적었어요.",
   False,
   "두 수가 서로 바뀌었어요. base 는 한 스텝 약 0.4초로 100,000 스텝(12시간), big 은 한 스텝 1.0초로 300,000 스텝"
   "(3.5일)이에요.")

ox(U9, "NP p.9",
   "논문 6.2 는 Table 3 의 실험에서 빔 서치는 썼지만 **체크포인트 평균(Checkpoint Averaging)** 은 쓰지 않았다고 적었어요.",
   True,
   "원문: 'We used beam search as described in the previous section, but no checkpoint averaging.' "
   "그래서 Table 3 의 base 줄 BLEU 25.8 은 Table 2 의 27.3 과 바로 비교할 수 없어요. 평가 집합도 newstest2013 으로 달라요.")

ox(U9, "NP p.9",
   "논문 Table 3 의 (A) 행 실험은 헤드 수를 바꾸면서 전체 계산량도 함께 늘렸어요.",
   False,
   "원문: 'we vary the number of attention heads and the attention key and value dimensions, keeping the amount "
   "of computation constant.' 계산량을 고정한 채 헤드 수만 바꿨어요. 그래서 $h = 1$ 일 때 $d_k = d_v = 512$ 로 커져요.")

ox(U9, "NP p.10",
   "논문 6.3 은 WSJ 40K 문장만 쓴 트랜스포머가 Dyer et al. (2016) 의 generative 모델보다도 높은 F1 을 얻었다고 적었어요.",
   False,
   "Table 4 에서 Transformer (4 layers) WSJ only 는 91.3 이고, Dyer et al. (2016) generative 는 93.3 이에요. "
   "논문은 'yielding better results than all previously reported models with the exception of the Recurrent "
   "Neural Network Grammar' 라고 적어, 그 모델만은 못 넘었다고 밝혔어요.")

# =====================================================================
# SHORT (15)
# =====================================================================
short(U1, "NP p.1",
      "논문 초록이 적은 WMT 2014 English-to-French 단일 모델의 BLEU 점수를 쓰시오.",
      ["41.8", "41.8 BLEU"],
      "초록과 Table 2 는 41.8 이라고 적었어요. 다만 6.1 본문은 같은 모델을 'a BLEU score of 41.0' 이라고 적어서 "
      "논문 자체가 어긋나 있어요. 시험에는 초록과 Table 2 의 41.8 을 쓰세요.",
      num=True, tol=0.05)

short(U1, "NP p.1",
      "이 논문이 발표된 학회 이름을 쓰시오.",
      ["NIPS 2017", "NIPS", "Neural Information Processing Systems", "신경정보처리시스템 학회",
       "31st Conference on Neural Information Processing Systems"],
      "쪽 아래에 '31st Conference on Neural Information Processing Systems (NIPS 2017), Long Beach, CA, USA' "
      "라고 적혀 있어요. 저자는 8명이고 별표 각주에 'Equal contribution. Listing order is random' 이라고 밝혔어요.")

short(U2, "NP p.2",
      "논문 2 Background 가 **셀프 어텐션(Self-Attention)** 의 다른 이름으로 적은 말을 영어로 쓰시오.",
      ["intra-attention", "intra attention", "intraattention", "인트라 어텐션"],
      "원문: 'Self-attention, sometimes called intra-attention is an attention mechanism relating different "
      "positions of a single sequence in order to compute a representation of the sequence.' "
      "한 문장 안의 서로 다른 위치를 잇는다는 뜻이에요.")

short(U2, "NP p.2",
      "논문 3 Model Architecture 첫 문단이 적은, 디코더가 앞서 만든 기호를 다시 입력으로 받아 한 번에 하나씩 "
      "만들어 내는 성질을 쓰시오.",
      ["자기회귀", "auto-regressive", "autoregressive", "auto regressive", "자기회귀(auto-regressive)"],
      "원문: 'At each step the model is auto-regressive, consuming the previously generated symbols as additional "
      "input when generating the next.' 이 성질을 지키려고 디코더 셀프 어텐션에 마스킹을 걸어요.")

short(U3, "NP p.3",
      "디코더 층이 인코더 층보다 하나 더 갖는 **하위층(Sub-layer)** 이 무엇인지 쓰시오.",
      ["인코더 스택의 출력에 대한 멀티 헤드 어텐션", "인코더-디코더 어텐션", "encoder-decoder attention",
       "크로스 어텐션", "cross-attention", "multi-head attention over the output of the encoder stack"],
      "원문: 'the decoder inserts a third sub-layer, which performs multi-head attention over the output of the "
      "encoder stack.' 논문은 3.2.3 에서 이 층을 encoder-decoder attention 이라고 불러요.")

short(U3, "NP p.3",
      "논문이 적은 $d_{model}$ 의 값을 쓰시오.",
      ["512"],
      "원문: 'all sub-layers in the model, as well as the embedding layers, produce outputs of dimension "
      "$d_{model} = 512$.' 헤드 하나의 $d_k$ 인 64 와 헷갈리지 마세요.",
      num=True, tol=0.5)

short(U4, "NP p.4",
      r"$d_k = 64$ 일 때 논문이 **어텐션 점수(Attention Score)** 를 나누는 값을 숫자로 쓰시오.",
      ["8"],
      r"$\sqrt{d_k} = \sqrt{64} = 8$ 이에요. $d_k$ 로 나누면 64 가 되어 틀려요. 제곱근을 꼭 씌우세요.",
      num=True, tol=0.01)

short(U5, "NP p.5",
      "논문 3.2.3 이 든 어텐션의 세 가지 쓰임 중, 인코더 안에서 키와 밸류와 쿼리가 모두 같은 곳에서 오는 것을 "
      "무엇이라 하는지 쓰시오.",
      ["인코더 셀프 어텐션", "셀프 어텐션", "self-attention", "encoder self-attention", "self attention"],
      "원문: 'In a self-attention layer all of the keys, values and queries come from the same place, in this "
      "case, the output of the previous layer in the encoder.' 각 위치가 앞 층의 모든 위치를 볼 수 있어요.")

short(U5, "NP p.5",
      "논문이 디코더에서 leftward information flow 를 막아야 한다고 한 까닭은 무엇을 지키기 위해서인지 쓰시오.",
      ["자기회귀 성질", "auto-regressive property", "자기회귀", "auto-regressive", "autoregressive"],
      "원문: 'We need to prevent leftward information flow in the decoder to preserve the auto-regressive "
      "property.' 아직 만들지 않은 뒤쪽 토큰을 미리 보면 다음 토큰 예측 과제가 성립하지 않아요.")

short(U6, "NP p.5",
      "논문이 적은 $d_{ff}$ 의 값을 쓰시오.",
      ["2048"],
      "원문: 'the inner-layer has dimensionality $d_{ff} = 2048$.' 논문은 값을 못박았고, "
      "4주차 강의 슬라이드는 '$d_{ff}$ is usually 4d' 라고 비율로 말했어요. $512 \\times 4 = 2048$ 이라 같은 말이에요.",
      num=True, tol=0.5)

short(U6, "NP p.6",
      "논문이 사인 코사인 위치 인코딩 말고 함께 실험해 본 다른 방식은 무엇인지 쓰시오.",
      ["학습하는 위치 임베딩", "learned positional embeddings", "학습 위치 임베딩", "positional embedding",
       "학습되는 위치 임베딩"],
      "원문: 'We also experimented with using learned positional embeddings instead, and found that the two "
      "versions produced nearly identical results (see Table 3 row (E)).' "
      "논문이 비교한 것은 이 둘뿐이에요. RoPE 는 논문에 없는 뒷날 이야기예요.")

short(U7, "NP p.7",
      "논문 4장이 말한, 이웃 $r$ 칸만 보게 제한한 셀프 어텐션의 **최대 경로 길이(Maximum Path Length)** 를 쓰시오.",
      ["O(n/r)", "O(n / r)", "n/r", "오 n/r"],
      "원문: 'This would increase the maximum path length to $O(n/r)$.' "
      "논문은 이 방식을 'We plan to investigate this approach further in future work' 라고만 적었고 실험하지는 않았어요.")

short(U7, "NP p.7",
      "논문은 **합성곱(Convolution)** 층이 순환 층보다 대략 몇 배 비싸다고 적었는지 기호로 쓰시오.",
      ["k", "커널 크기 k", "kernel size k", "k배", "k 배"],
      "원문: 'Convolutional layers are generally more expensive than recurrent layers, by a factor of $k$.' "
      "$k$ 는 합성곱의 커널 크기예요. 분리 합성곱을 쓰면 비용이 많이 내려간다고 덧붙였어요.")

short(U8, "NP p.7",
      "논문이 base 모델에 쓴 residual dropout 의 비율 $P_{drop}$ 을 쓰시오.",
      ["0.1"],
      "원문: 'For the base model, we use a rate of $P_{drop} = 0.1$.' big 모델은 0.3 을 썼지만, "
      "English-to-French big 모델만은 0.3 대신 0.1 을 썼다고 6.1 에 적혀 있어요.",
      num=True, tol=0.001)

short(U9, "NP p.13-15",
      "논문 Figure 3, 4, 5 가 모두 보여 준 어텐션은 몇 번째 층의 것인지 숫자로 쓰시오.",
      ["5", "layer 5", "layer 5 of 6", "5층"],
      "세 그림 모두 'layer 5 of 6' 이라고 적혀 있어요. 여섯 층 가운데 다섯째 층의 인코더 셀프 어텐션이에요.",
      num=True, tol=0.01)

# =====================================================================
# ESSAY (6)
# =====================================================================
essay(U3, "NP p.3", "encoder-decoder-stack",
      "논문 3.1 에 따라 인코더 층과 디코더 층의 구조를 비교해 설명하시오.",
      "인코더와 디코더 모두 똑같은 층을 $N = 6$ 개 쌓아요. "
      "인코더 한 층은 멀티 헤드 **셀프 어텐션(Self-Attention)** 과 **위치별 피드포워드 신경망(Position-wise Feed-Forward Network (FFN))**, "
      "이렇게 **하위층(Sub-layer)** 두 개로 되어 있어요. "
      "디코더 한 층은 여기에 인코더 스택의 출력을 보는 멀티 헤드 어텐션 하위층이 하나 더 붙어 모두 세 개예요. "
      "모든 하위층에는 **잔차 연결(Residual Connection)** 을 두르고 그다음 **층 정규화(Layer Normalization (LayerNorm))** 를 해서 "
      "출력이 $\\mathrm{LayerNorm}(x + \\mathrm{Sublayer}(x))$ 가 돼요. "
      "디코더의 셀프 어텐션은 뒤쪽 위치를 보지 못하게 고쳐 두었고, 출력 임베딩을 한 자리 미루어 놓아 위치 $i$ 의 예측이 "
      "$i$ 보다 앞선 위치의 출력에만 기대게 해요.",
      ["인코더와 디코더 모두 $N = 6$", "인코더 층은 하위층 2개",
       "디코더 층은 하위층 3개", "추가된 것은 인코더 출력을 보는 멀티 헤드 어텐션",
       "잔차 연결 뒤에 층 정규화", "$\\mathrm{LayerNorm}(x + \\mathrm{Sublayer}(x))$ 형태",
       "디코더 셀프 어텐션은 뒤쪽을 못 봄", "출력 임베딩을 한 자리 미룸"])

essay(U4, "NP p.4", "scaled-dot-product-why",
      r"논문 식 (1) 의 계산 순서를 쓰고, 점수를 $\sqrt{d_k}$ 로 나누는 까닭을 논문이 어떻게 적었는지 서술하시오.",
      "먼저 쿼리와 모든 키의 **내적(Dot Product)** 으로 점수를 구해요. "
      r"그다음 각 점수를 $\sqrt{d_k}$ 로 나누고, **소프트맥스(Softmax)** 를 씌워 밸류에 걸 가중치를 얻어요. "
      "마지막으로 그 가중치로 밸류의 **가중합(Weighted Sum)** 을 만들어요. "
      r"나누는 까닭에 대해 논문은 'We suspect' 라고 적어, $d_k$ 가 크면 내적이 커져 소프트맥스가 **기울기(Gradient)** 가 "
      r"아주 작은 영역으로 밀린다고 추측했어요. "
      r"각주 4 는 $q$ 와 $k$ 의 성분이 평균 0, 분산 1 이면 내적의 분산이 $d_k$ 가 된다는 예시를 들었어요. "
      r"그래서 표준편차인 $\sqrt{d_k}$ 로 나누어 점수의 크기를 되돌려 놓아요.",
      ["점수는 쿼리와 키의 내적", r"$\sqrt{d_k}$ 로 나눔",
       "소프트맥스로 가중치", "밸류의 가중합이 출력",
       "논문은 'We suspect' 라고 적은 추측", "큰 내적은 소프트맥스를 기울기가 작은 영역으로 밀어냄",
       r"각주 4 의 분산은 $d_k$", r"$d_k = 64$ 이면 나누는 값은 8"])

essay(U5, "NP p.5", "three-applications-of-attention",
      "논문 3.2.3 이 든 트랜스포머의 어텐션 세 가지 쓰임을 각각 설명하시오.",
      "첫째는 encoder-decoder attention 이에요. **쿼리(Query)** 는 앞 디코더 층에서 오고 **키(Key)** 와 **밸류(Value)** 는 "
      "인코더 스택의 출력에서 와서, 디코더의 모든 위치가 입력 문장의 모든 위치를 볼 수 있어요. "
      "둘째는 인코더의 **셀프 어텐션(Self-Attention)** 이에요. 키와 밸류와 쿼리가 모두 같은 곳, 곧 인코더 앞 층의 출력에서 와요. "
      "각 위치가 앞 층의 모든 위치를 볼 수 있어요. "
      "셋째는 디코더의 셀프 어텐션이에요. 각 위치가 자기 자리까지 포함해 앞쪽 위치만 볼 수 있어요. "
      "**자기회귀(Autoregressive)** 성질을 지키려고 왼쪽으로만 정보가 흐르게 막아야 해서, 소프트맥스에 들어가기 전 값 가운데 "
      "허용되지 않는 연결을 $-\\infty$ 로 바꿔요.",
      ["encoder-decoder attention 은 쿼리가 디코더, 키와 밸류가 인코더",
       "디코더의 모든 위치가 입력 전체를 봄", "인코더 셀프 어텐션은 셋이 모두 같은 곳",
       "각 위치가 앞 층의 모든 위치를 봄", "디코더 셀프 어텐션은 자기 자리까지만",
       "자기회귀 성질을 지키기 위해", "소프트맥스 앞에서 $-\\infty$ 로 마스킹"])

essay(U6, "NP p.6", "positional-encoding-why",
      "논문이 **위치 인코딩(Positional Encoding)** 을 넣는 까닭과 사인 코사인 방식을 고른 까닭을 서술하시오.",
      "트랜스포머에는 순환도 합성곱도 없어서, 그대로 두면 모델이 토큰의 순서를 쓸 방법이 없어요. "
      "그래서 상대 위치나 절대 위치에 대한 정보를 넣어 주어야 하고, 인코더와 디코더 스택 맨 아래에서 입력 임베딩에 "
      "위치 인코딩을 더해요. 더할 수 있도록 차원을 $d_{model}$ 로 맞췄어요. "
      "값은 차원마다 주기가 다른 사인과 코사인으로 만들고, 파장은 $2\\pi$ 에서 $10000 \\cdot 2\\pi$ 까지 등비수열을 이뤄요. "
      "논문은 고정된 간격 $k$ 에 대해 $PE_{pos+k}$ 가 $PE_{pos}$ 의 선형 함수로 표현되므로 상대 위치로 주목하기 쉬울 것이라고 "
      "'we hypothesized' 라고 적었어요. 이것은 단정이 아니라 가설이에요. "
      "학습하는 위치 임베딩과 비교해 결과는 거의 같았지만, 학습 때 본 것보다 긴 문장으로 외삽할 수 있을지도 모른다는 이유로 "
      "사인 코사인 쪽을 골랐다고 적었어요. 이 역시 'may allow' 라는 추측이에요.",
      ["순환도 합성곱도 없어 순서 정보가 없음", "입력 임베딩에 더함(곱하지 않음)",
       "차원을 $d_{model}$ 로 맞춤", "차원마다 주기가 다른 사인과 코사인",
       "파장은 $2\\pi$ 에서 $10000 \\cdot 2\\pi$ 까지 등비", "$PE_{pos+k}$ 가 $PE_{pos}$ 의 선형 함수",
       "상대 위치 주장은 논문의 가설(hypothesized)", "학습 임베딩과 결과는 거의 같음",
       "외삽 가능성은 추측(may allow)"])

essay(U7, "NP p.6-7", "table1-three-criteria",
      "Table 1 의 세 가지 비교 기준을 쓰고, 셀프 어텐션이 순환 층보다 유리한 조건을 서술하시오.",
      "세 기준은 층당 총 계산 복잡도, 병렬화할 수 있는 계산량(최소 **순차 연산 수(Sequential Operations)**), "
      "그리고 장거리 의존성의 **최대 경로 길이(Maximum Path Length)** 예요. "
      r"셀프 어텐션은 $O(n^2 \cdot d)$, $O(1)$, $O(1)$ 이고 순환은 $O(n \cdot d^2)$, $O(n)$, $O(n)$ 이에요. "
      "곧 셀프 어텐션은 모든 자리를 상수 번의 순차 연산으로 잇지만, 순환은 $n$ 번을 줄 서서 계산해야 해요. "
      "계산량만 보면 문장 길이 $n$ 이 표현 차원 $d$ 보다 작을 때 셀프 어텐션이 더 싸요. "
      "논문은 기계 번역이 쓰는 word-piece 나 byte-pair 표현에서는 대개 그 조건이 맞는다고 적었어요. "
      "반대로 $n$ 이 $d$ 보다 커지면 셀프 어텐션 쪽이 비싸지고, 그때는 이웃 $r$ 칸만 보는 "
      "**제한된 셀프 어텐션(Restricted Self-Attention)** 을 쓸 수 있지만 경로 길이가 $O(n/r)$ 로 늘어요.",
      ["기준 1 층당 계산 복잡도", "기준 2 최소 순차 연산 수(병렬화)",
       "기준 3 최대 경로 길이", r"셀프 어텐션 $O(n^2 \cdot d)$, $O(1)$, $O(1)$",
       r"순환 $O(n \cdot d^2)$, $O(n)$, $O(n)$", "$n < d$ 일 때 셀프 어텐션이 더 싸다",
       "word-piece, byte-pair 표현에서는 대개 그렇다", "제한하면 경로 길이가 $O(n/r)$"])

essay(U9, "NP p.9", "table3-model-variations",
      "Table 3 의 (A)부터 (E)까지에서 논문이 얻은 결론을 정리하시오.",
      "(A) 는 계산량을 고정한 채 헤드 수만 바꾼 실험이에요. 헤드가 하나면 가장 좋은 설정보다 BLEU 가 0.9 낮았고, "
      "헤드가 너무 많아도(32개) 품질이 떨어졌어요. "
      r"(B) 는 $d_k$ 를 줄이면 품질이 나빠진다는 것을 보였고, 논문은 **호환성 함수(Compatibility Function)** 를 정하는 일이 "
      "쉽지 않아서 내적보다 더 정교한 함수가 도움이 될 수도 있다고 적었어요. 이것은 추측이에요. "
      "(C) 는 모델이 클수록 좋다는 것을 보였어요. $N$, $d_{model}$, $d_{ff}$ 를 키우면 대체로 좋아져요. "
      "(D) 는 **드롭아웃(Dropout)** 과 **라벨 스무딩(Label Smoothing)** 이 **과적합(Over-fitting)** 을 막는 데 도움이 된다는 것을 보였어요. "
      "(E) 는 사인 코사인 대신 학습하는 위치 임베딩을 써도 base 와 거의 같은 결과가 나온다는 것을 보였어요.",
      ["(A) 계산량 고정, 헤드 수만 변경", "단일 헤드는 0.9 BLEU 낮음, 헤드가 너무 많아도 나빠짐",
       r"(B) $d_k$ 를 줄이면 품질 저하", "더 정교한 호환성 함수 제안은 논문의 추측",
       "(C) 큰 모델이 더 좋다", "(D) 드롭아웃과 라벨 스무딩이 과적합을 막는다",
       "(E) 학습 위치 임베딩도 거의 같다", "모든 수치는 newstest2013 개발 집합"])

# =====================================================================
# CALC (6)
# =====================================================================
calc(U4, "NP p.4", "scaled-dot-product-softmax",
     r"$d_k = 64$ 이고 한 쿼리와 세 키의 **내적(Dot Product)** 원점수가 $(16, 8, 0)$ 이다. "
     r"논문 식 (1) 에 따라 나누는 값, 스케일한 점수, **소프트맥스(Softmax)** 를 거친 "
     r"**어텐션 가중치(Attention Weight)** 를 구하시오. ($e^2 = 7.389$, $e^1 = 2.718$, $e^0 = 1$)",
     r"$\sqrt{d_k}$ 로 나눈 다음 소프트맥스를 씌워요. 가중치는 소수 넷째 자리까지 쓰세요.",
     [{"label": "나누는 값", "ans": 8, "tol": 0.01},
      {"label": "스케일한 점수 1", "ans": 2.0, "tol": 0.01},
      {"label": "스케일한 점수 2", "ans": 1.0, "tol": 0.01},
      {"label": "스케일한 점수 3", "ans": 0.0, "tol": 0.01},
      {"label": "가중치 1", "ans": 0.6652, "tol": 0.001},
      {"label": "가중치 2", "ans": 0.2447, "tol": 0.001},
      {"label": "가중치 3", "ans": 0.0900, "tol": 0.001}],
     [r"식은 $\mathrm{softmax}(QK^{T}/\sqrt{d_k})V$ 예요",
      r"$\sqrt{d_k} = \sqrt{64} = 8$ 이에요",
      r"$16/8 = 2$, $8/8 = 1$, $0/8 = 0$ 이라 스케일한 점수는 $(2, 1, 0)$ 이에요",
      r"$\exp$ 를 씌우면 $7.389$, $2.718$, $1$ 이고 합은 $11.107$ 이에요",
      r"$7.389/11.107 pprox 0.6652$, $2.718/11.107 = 0.2447$, $1/11.107 = 0.0900$ 이에요." + "(준 어림값으로 나누면 0.66526 이라 0.6653 으로 써도 정답이에요. 어림 없이 계산한 정확한 값이 0.66524 라서 0.6652 로 적어 둡니다)"],
     r"나누는 값 8, 점수 $(2, 1, 0)$, 가중치 $(0.6652, 0.2447, 0.0900)$",
     r"$d_k$ 로 나누면 $(0.25, 0.125, 0)$ 이 되어 틀려요. 제곱근을 꼭 씌우세요. 가중치의 합이 1 인지도 확인하세요.")

calc(U4, "NP p.4", "attention-weighted-sum",
     r"**어텐션 가중치(Attention Weight)** 가 $(0.6652, 0.2447, 0.0900)$ 이고 밸류 행렬이 "
     r"$V = \begin{bmatrix} 1 & 0 \\ 0 & 2 \\ 2 & 2 \end{bmatrix}$ 이다. 어텐션 출력을 구하시오.",
     "각 밸류 행에 가중치를 곱해 모두 더해요. 소수 넷째 자리까지 쓰세요.",
     [{"label": "출력 첫 칸", "ans": 0.8452, "tol": 0.002},
      {"label": "출력 둘째 칸", "ans": 0.6694, "tol": 0.002}],
     [r"식 (1) 의 마지막 곱은 $\mathrm{softmax}(\cdot)V$ 이고, 이는 밸류의 **가중합(Weighted Sum)** 이에요",
      r"첫 칸: $0.6652 \times 1 + 0.2447 \times 0 + 0.0900 \times 2 = 0.6652 + 0 + 0.1800 = 0.8452$",
      r"둘째 칸: $0.6652 \times 0 + 0.2447 \times 2 + 0.0900 \times 2 = 0 + 0.4894 + 0.1800 = 0.6694$",
      r"가중치의 합이 1 이므로 결과는 세 밸류의 가중 평균이에요"],
     r"출력은 $(0.8452, 0.6694)$",
     "가중치를 곱하는 대상은 키가 아니라 밸류예요. 점수 계산에만 키를 쓰고, 실제로 섞이는 것은 밸류예요.")

calc(U5, "NP p.5", "multihead-parameter-count",
     r"논문 base 설정은 $d_{model} = 512$, $h = 8$ 이다. 헤드 하나의 차원 $d_k$, 헤드 하나의 $W_i^Q$ 파라미터 수, "
     r"그리고 $W^Q$, $W^K$, $W^V$, $W^O$ 를 모두 합친 **멀티 헤드 어텐션(Multi-Head Attention (MHA))** "
     r"**하위층(Sub-layer)** 의 파라미터 수를 구하시오. (편향 항은 빼고 센다)",
     r"$d_k = d_{model}/h$ 이고, 헤드 하나의 $W_i^Q$ 는 $d_{model} \times d_k$ 예요. 정수로 쓰세요.",
     [{"label": "d_k", "ans": 64},
      {"label": "헤드 하나의 W^Q 파라미터 수", "ans": 32768},
      {"label": "멀티 헤드 하위층 합계", "ans": 1048576}],
     [r"$d_k = d_v = d_{model}/h = 512/8 = 64$ 예요",
      r"헤드 하나의 $W_i^Q$ 는 $512 \times 64 = 32{,}768$ 개예요",
      r"$Q$, $K$, $V$ 각각 헤드 8개씩이므로 $3 \times 8 \times 32{,}768 = 786{,}432$ 개예요",
      r"$W^O$ 는 $(h d_v) \times d_{model} = 512 \times 512 = 262{,}144$ 개예요",
      r"합치면 $786{,}432 + 262{,}144 = 1{,}048{,}576 = 4 \times 512 \times 512$ 예요"],
     r"$d_k = 64$, 헤드 하나의 $W_i^Q$ 는 32,768개, 하위층 합계는 1,048,576개",
     "이 값은 논문이 직접 적은 수가 아니라 논문이 준 크기로 우리가 직접 세어 본 것이에요. "
     "헤드를 8개로 나눠도 합계가 $4 \\times 512 \\times 512$ 인 것은 차원을 나눠 쓰기 때문이에요.")

calc(U6, "NP p.5", "ffn-and-layer-parameter-count",
     r"논문 base 설정은 $d_{model} = 512$, $d_{ff} = 2048$ 이다. $d_{ff}$ 가 $d_{model}$ 의 몇 배인지, "
     r"$W_1$ 의 파라미터 수, $W_1 + W_2$ 의 합, 그리고 멀티 헤드 하위층 1,048,576개를 더한 인코더 한 층의 "
     r"파라미터 수를 구하시오. (편향 항은 빼고 센다)",
     r"$W_1$ 은 $d_{model} \times d_{ff}$, $W_2$ 는 $d_{ff} \times d_{model}$ 이에요. 정수로 쓰세요.",
     [{"label": "d_ff 는 d_model 의 몇 배", "ans": 4},
      {"label": "W1 파라미터 수", "ans": 1048576},
      {"label": "W1 + W2", "ans": 2097152},
      {"label": "인코더 한 층 합계", "ans": 3145728}],
     [r"$d_{ff}/d_{model} = 2048/512 = 4$ 배예요",
      r"$W_1$ 은 $512 \times 2048 = 1{,}048{,}576$ 개예요",
      r"$W_2$ 는 $2048 \times 512 = 1{,}048{,}576$ 개라 합은 $2{,}097{,}152$ 개예요",
      r"인코더 한 층 $= 1{,}048{,}576 + 2{,}097{,}152 = 3{,}145{,}728$ 개예요"],
     r"4배, $W_1$ 은 1,048,576개, 합은 2,097,152개, 인코더 한 층은 3,145,728개",
     "논문은 $d_{ff} = 2048$ 이라고 값을 못박았고, 4주차 슬라이드는 '보통 $4d$' 라고 비율로 말했어요. "
     "여기 파라미터 수는 논문이 적은 값이 아니라 우리가 직접 세어 본 어림이에요. 편향 항과 LayerNorm 은 빼고 셌어요.")

calc(U6, "NP p.6", "sinusoidal-pe-values",
     r"$d_{model} = 4$ 로 줄인 **사인 코사인 위치 인코딩(Sinusoidal Positional Encoding)** 에서 $pos = 1$ 의 네 칸과 "
     r"$pos = 0$ 의 앞 두 칸을 구하시오. ($\sin 1 = 0.8415$, $\cos 1 = 0.5403$, $\sin 0.01 = 0.0100$, $\cos 0.01 = 1.0000$)",
     r"짝수 칸은 sin, 홀수 칸은 cos 이고 각도는 $pos / 10000^{2i/d_{model}}$ 예요. 소수 넷째 자리까지 쓰세요.",
     [{"label": "pos 1 의 0 번째 칸", "ans": 0.8415, "tol": 0.001},
      {"label": "pos 1 의 1 번째 칸", "ans": 0.5403, "tol": 0.001},
      {"label": "pos 1 의 2 번째 칸", "ans": 0.0100, "tol": 0.001},
      {"label": "pos 1 의 3 번째 칸", "ans": 1.0000, "tol": 0.001},
      {"label": "pos 0 의 0 번째 칸", "ans": 0.0, "tol": 0.001},
      {"label": "pos 0 의 1 번째 칸", "ans": 1.0, "tol": 0.001}],
     [r"식은 $PE_{(pos, 2i)} = \sin(pos/10000^{2i/d_{model}})$, $PE_{(pos, 2i+1)} = \cos(pos/10000^{2i/d_{model}})$ 예요",
      r"$i = 0$ 이면 분모가 $10000^{0} = 1$ 이라 각도는 그대로 $pos$ 예요",
      r"$pos = 1$ 의 앞 두 칸은 $\sin 1 = 0.8415$, $\cos 1 = 0.5403$ 이에요",
      r"$i = 1$ 이면 분모가 $10000^{2/4} = 100$ 이라 각도는 $1/100 = 0.01$ 이에요",
      r"뒤 두 칸은 $\sin 0.01 = 0.0100$, $\cos 0.01 = 1.0000$ 이에요",
      r"$pos = 0$ 이면 각도가 모두 0 이라 $\sin 0 = 0$, $\cos 0 = 1$ 이에요"],
     r"$pos = 1$ 은 $(0.8415, 0.5403, 0.0100, 1.0000)$, $pos = 0$ 의 앞 두 칸은 $(0.0, 1.0)$",
     "학습하는 값이 아니라 식으로 계산하는 값이에요. 자리마다 각도가 달라져서 무늬가 달라져요. "
     "$i$ 는 차원 쌍의 번호이지 칸 번호가 아니라는 점을 조심하세요.")

calc(U7, "NP p.6-7", "table1-cost-n100",
     r"Table 1 에서 셀프 어텐션의 층당 복잡도는 $O(n^2 \cdot d)$, 순환의 층당 복잡도는 $O(n \cdot d^2)$ 이다. "
     r"$d = 512$, $n = 100$ 일 때 두 값을 계산하고, 순환이 셀프 어텐션의 몇 배인지 구하시오.",
     r"$O$ 안의 식에 숫자를 그대로 넣어 비교해요. 배수는 소수 둘째 자리까지 쓰세요.",
     [{"label": "n^2 d", "ans": 5120000},
      {"label": "n d^2", "ans": 26214400},
      {"label": "몇 배", "ans": 5.12, "tol": 0.01}],
     [r"셀프 어텐션: $n^2 d = 100^2 \times 512 = 10{,}000 \times 512 = 5{,}120{,}000$",
      r"순환: $n d^2 = 100 \times 512^2 = 100 \times 262{,}144 = 26{,}214{,}400$",
      r"$26{,}214{,}400 / 5{,}120{,}000 = 5.12$ 배예요",
      r"$n = 100$ 은 $d = 512$ 보다 작으므로 논문 말대로 셀프 어텐션이 더 싸요"],
     r"$5{,}120{,}000$ 과 $26{,}214{,}400$, 순환이 약 5.12배 비싸다",
     r"$n$ 과 $d$ 의 자리를 바꿔 넣지 마세요. 갈림길은 $n = d$ 이고, $n$ 이 $d$ 보다 커지면 반대로 셀프 어텐션이 비싸져요.")

# =====================================================================
# ------------------------------------------------- 보기 자리 섞기와 id 고정
optshuffle.shuffle_bank(bank)
IDS = [
    "wPb-mcq-001", "wPb-mcq-002", "wPb-mcq-003", "wPb-mcq-004", "wPb-mcq-005", "wPb-mcq-006",
    "wPb-mcq-007", "wPb-mcq-008", "wPb-mcq-009", "wPb-mcq-010", "wPb-mcq-011", "wPb-mcq-012",
    "wPb-mcq-013", "wPb-mcq-014", "wPb-mcq-015", "wPb-mcq-016", "wPb-mcq-017", "wPb-mcq-018",
    "wPb-mcq-019", "wPb-mcq-020", "wPb-mcq-021", "wPb-mcq-022", "wPb-mcq-023", "wPb-mcq-024",
    "wPb-mcq-025", "wPb-mcq-026", "wPb-mcq-027", "wPb-mcq-028", "wPb-mcq-029", "wPb-mcq-030",
    "wPb-ox-001", "wPb-ox-002", "wPb-ox-003", "wPb-ox-004", "wPb-ox-005", "wPb-ox-006",
    "wPb-ox-007", "wPb-ox-008", "wPb-ox-009", "wPb-ox-010", "wPb-ox-011", "wPb-ox-012",
    "wPb-ox-013", "wPb-ox-014", "wPb-ox-015", "wPb-ox-016", "wPb-ox-017", "wPb-ox-018",
    "wPb-ox-019", "wPb-ox-020",
    "wPb-short-001", "wPb-short-002", "wPb-short-003", "wPb-short-004", "wPb-short-005",
    "wPb-short-006", "wPb-short-007", "wPb-short-008", "wPb-short-009", "wPb-short-010",
    "wPb-short-011", "wPb-short-012", "wPb-short-013", "wPb-short-014", "wPb-short-015",
    "wPb-essay-001", "wPb-essay-002", "wPb-essay-003", "wPb-essay-004", "wPb-essay-005",
    "wPb-essay-006",
    "wPb-calc-001", "wPb-calc-002", "wPb-calc-003", "wPb-calc-004", "wPb-calc-005", "wPb-calc-006",
]
optshuffle.check_ids(bank, IDS)

raw = json.dumps(bank, ensure_ascii=False, indent=1)
for ch in ("—", "–", "·", "・"):
    assert ch not in raw, ch
for it in bank:
    if it["type"] == "ox":
        assert isinstance(it["a"], bool)
n_false = sum(1 for it in bank if it["type"] == "ox" and it["a"] is False)
assert n_false == 10, n_false
with open(OUT, "w", encoding="utf-8") as f:
    f.write(raw)
print("saved", OUT, len(bank), "문항", cnt, "ox false", n_false)
