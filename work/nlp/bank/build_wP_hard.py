# -*- coding: utf-8 -*-
"""참고 논문 주차(NP Attention Is All You Need, Vaswani et al. 2017) hard 문제은행 생성기.
출력: work/nlp/bank/wP_hard.json
hard 는 개념 두세 개를 엮거나, 비슷한 것을 구별하거나, 사례에 적용하거나, "왜" 를 묻는다.
사실은 논문에서만 가져온다. 4주차 강의 슬라이드와 다른 대목은 해설에서 그 차이를 밝힌다.
계산 문항 정답은 아래에서 파이썬으로 실제 계산하고 assert 로 확인한다."""
import json, math, os
import optshuffle

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "wP_hard.json")

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


# C1 스케일을 하지 않았을 때와 했을 때
RAW = [16.0, 8.0, 0.0]
NOSCALE = softmax(RAW)
assert [round(v, 6) for v in NOSCALE] == [0.999665, 0.000335, 0.000000]
SCALED = softmax([r / 8.0 for r in RAW])
assert [round(v, 4) for v in SCALED] == [0.6652, 0.2447, 0.0900]
assert math.sqrt(64) == 8.0

# C2 위치 인코딩 pos = 2 (d_model = 4)
def pe_row(pos, d=4):
    out = []
    for i in range(d // 2):
        ang = pos / (10000 ** (2 * i / d))
        out.append(round(math.sin(ang), 4))
        out.append(round(math.cos(ang), 4))
    return out


assert pe_row(2) == [0.9093, -0.4161, 0.02, 0.9998]
assert pe_row(1) == [0.8415, 0.5403, 0.01, 1.0]

# C3 Table 1 손계산 (d = 512)
D = 512
assert 512 ** 2 * D == 512 * D ** 2 == 134217728
assert 1000 ** 2 * D == 512000000
assert 1000 * D ** 2 == 262144000
assert round((1000 ** 2 * D) / (1000 * D ** 2), 2) == 1.95

# C4 학습률 식 (3)
def lrate(step, dm=512, warm=4000):
    return dm ** -0.5 * min(step ** -0.5, step * warm ** -1.5)


assert round(512 ** -0.5, 6) == 0.044194
assert round(lrate(4000), 6) == 0.000699
assert round(lrate(16000), 6) == 0.000349
assert round(lrate(4000) / lrate(16000), 3) == 2.0

# C5 FLOPs 검산 (big 모델)
SEC = 3.5 * 86400
assert SEC == 302400.0
GPU_SEC = SEC * 8
assert GPU_SEC == 2419200.0
FLOPS = GPU_SEC * 9.5e12
assert round(FLOPS / 1e19, 2) == 2.30

# C6 BLEU 차이
assert round(28.4 - 26.36, 2) == 2.04
assert round(25.8 - 24.9, 2) == 0.9
assert round(41.8 - 41.29, 2) == 0.51

bank = []
cnt = {}


def add(t, unit, slides, src=None, **kw):
    cnt[t] = cnt.get(t, 0) + 1
    item = {"id": "wPh-%s-%03d" % (t, cnt[t]), "type": t, "part": "P", "level": "hard",
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
# MCQ (15)
# =====================================================================
mcq(U1, "NP p.1",
    "초록의 'improving over the existing best results, including ensembles, by over 2 BLEU' 가 뜻하는 바로 "
    "가장 적절한 것은?",
    ["단일 모델뿐 아니라 여러 모델을 합친 **앙상블(Ensemble)** 까지 포함한 기존 최고 기록을 2 BLEU 넘게 앞섰다는 뜻",
     "**앙상블(Ensemble)** 을 뺀 단일 모델 최고 기록만 2 BLEU 넘게 앞섰다는 뜻",
     "트랜스포머 **앙상블(Ensemble)** 이 트랜스포머 단일 모델을 2 BLEU 앞섰다는 뜻",
     "기존 최고 기록과의 차이가 2 BLEU 안쪽이라는 뜻"],
    0,
    "6.1 도 'outperforms the best previously reported models (including ensembles) by more than 2.0 BLEU' 라고 "
    "다시 적었어요. Table 2 에서 기존 최고는 ConvS2S Ensemble 의 26.36 이고 $28.4 - 26.36 = 2.04$ 라 '2.0 넘게' 예요. "
    "앙상블을 뺀 단일 모델 최고는 MoE 의 26.03 이라 차이가 오히려 더 커요.")

mcq(U1, "NP p.1",
    "논문 첫 쪽 각주에서 scaled dot-product attention, multi-head attention, parameter-free position "
    "representation 을 제안한 사람으로 옳은 것은?",
    ["Noam Shazeer", "Jakob Uszkoreit", "Ashish Vaswani", "Aidan N. Gomez"],
    0,
    "각주: 'Noam proposed scaled dot-product attention, multi-head attention and the parameter-free position "
    "representation.' parameter-free position representation 은 학습 파라미터가 없는 사인 코사인 "
    "**위치 인코딩(Positional Encoding)** 을 가리켜요. Jakob 은 RNN 을 셀프 어텐션으로 바꾸자고 제안한 사람이라 "
    "가장 헷갈려요.")

mcq(U2, "NP p.2",
    "논문이 트랜스포머를 두고 '첫(the first)' 이라고 말한 범위로 옳은 것은?",
    ["sequence-aligned RNN 이나 합성곱 없이 **셀프 어텐션(Self-Attention)** 만으로 입력과 출력의 표현을 계산하는 "
     "첫 **시퀀스 변환(Sequence Transduction)** 모델",
     "셀프 어텐션이라는 개념을 처음 만들어 낸 모델",
     "인코더-디코더 구조를 처음 쓴 모델",
     "**어텐션(Attention)** 을 처음 쓴 기계 번역 모델"],
    0,
    "원문: 'To the best of our knowledge, however, the Transformer is the first transduction model relying "
    "entirely on self-attention to compute representations of its input and output without using "
    "sequence-aligned RNNs or convolution.' 셀프 어텐션 자체는 독해, 요약 같은 과제에 이미 쓰였다고 같은 절에 "
    "적혀 있고, 논문도 'To the best of our knowledge' 라는 단서를 달았어요.")

mcq(U3, "NP p.3",
    "Figure 1 의 Add & Norm 블록이 하는 일을 논문 3.1 에 맞게 설명한 것은?",
    ["**하위층(Sub-layer)** 의 출력을 하위층의 입력에 먼저 더하고, 그 결과에 **층 정규화(Layer Normalization (LayerNorm))** 를 건다",
     "**하위층(Sub-layer)** 의 입력에 먼저 **층 정규화(Layer Normalization (LayerNorm))** 를 걸고, 그 결과를 하위층에 넣는다",
     "**하위층(Sub-layer)** 의 출력에 **층 정규화(Layer Normalization (LayerNorm))** 를 건 다음 하위층의 입력을 더한다",
     "**하위층(Sub-layer)** 의 출력과 입력을 각각 정규화한 뒤 이어 붙인다"],
    0,
    r"원문 식은 $\mathrm{LayerNorm}(x + \mathrm{Sublayer}(x))$ 예요. 더하기가 먼저이고 정규화가 나중이에요. "
    r"두 번째 보기가 4주차 강의 슬라이드 p.51 이 소개한 Pre-LN 인데, 그 방식은 이 논문에 없어요. "
    r"세 번째 보기는 잔차를 정규화 밖에서 더하는 또 다른 변형이라 역시 논문과 달라요.")

mcq(U3, "NP p.3",
    "논문 설정대로 인코더 6층과 디코더 6층을 쌓았을 때, 모델 전체의 멀티 헤드 어텐션 하위층은 모두 몇 개인가?",
    ["12개", "18개", "24개", "36개"],
    1,
    "인코더 한 층에는 멀티 헤드 어텐션 하위층이 1개라서 $1 \\times 6 = 6$ 개예요. "
    "디코더 한 층에는 마스킹된 셀프 어텐션과 encoder-decoder attention 두 개가 있어 $2 \\times 6 = 12$ 개예요. "
    "합하면 18개예요. **위치별 피드포워드 신경망(Position-wise Feed-Forward Network (FFN))** 하위층 12개는 따로 세요.")

mcq(U4, "NP p.4",
    "Figure 2 왼쪽 그림에서 Mask (opt.) 가 들어가는 자리로 옳은 것은?",
    ["Scale 다음, SoftMax 앞",
     "SoftMax 다음, 두 번째 MatMul 앞",
     "첫 번째 MatMul 앞",
     "두 번째 MatMul 다음"],
    0,
    "Figure 2 왼쪽은 아래에서 위로 MatMul, Scale, Mask (opt.), SoftMax, MatMul 순서예요. "
    "3.2.3 도 'masking out (setting to $-\\infty$) all values in the input of the softmax' 라고 적어 "
    "소프트맥스에 들어가기 전이라고 밝혔어요. 소프트맥스 뒤에서 막으면 가중치의 합이 1 이 되지 않아요.")

mcq(U4, "NP p.4-9",
    r"$d_k$ 의 크기에 대한 논문의 서술을 바르게 엮은 것은?",
    [r"3.2.1 은 $d_k$ 가 크면 내적이 커져 **소프트맥스(Softmax)** 가 포화된다고 추측했고, Table 3 (B) 는 $d_k$ 를 "
     r"16 이나 32 로 줄이면 품질이 나빠진다는 것을 실험으로 보였다",
     r"$d_k$ 는 크면 클수록 좋다고 적었다",
     r"$d_k$ 를 줄이면 품질이 좋아진다는 것을 실험으로 보였다",
     r"$d_k$ 의 크기는 성능과 관계가 없다고 적었다"],
    0,
    r"두 곳을 같이 읽어야 해요. 스케일링은 $d_k$ 가 클 때 생기는 부작용을 다루는 장치이고, "
    r"Table 3 (B) 는 $d_k = 16$ 일 때 PPL 5.16, BLEU 25.1, $d_k = 32$ 일 때 5.01, 25.4 로 "
    r"base($d_k = 64$, 4.92, 25.8)보다 나빴어요. 그래서 논문은 '호환성을 정하는 일이 쉽지 않다' 고 적었어요.")

mcq(U5, "NP p.5",
    "논문의 계산량 고정 규칙을 따라 $d_{model} = 512$ 에서 헤드를 16개로 늘리면 $d_k$ 는 얼마가 되는가?",
    ["16", "32", "64", "128"],
    1,
    r"$d_k = d_v = d_{model}/h = 512/16 = 32$ 예요. Table 3 (A) 의 $h = 16$ 줄도 $d_k = d_v = 32$ 로 적혀 있어요. "
    r"헤드를 늘린다고 전체 차원이 커지는 것이 아니라 같은 512 를 더 잘게 나눠 쓰는 것이에요.")

mcq(U5, "NP p.5",
    "'각 위치가 자기 자리까지 포함해 앞쪽 위치만 볼 수 있다' 에 해당하는 어텐션과 그 까닭으로 옳은 것은?",
    ["디코더 셀프 어텐션이고, **자기회귀(Autoregressive)** 성질을 지키려고 왼쪽으로만 정보가 흐르게 막기 때문",
     "인코더 셀프 어텐션이고, 입력 문장은 이미 다 알고 있어 **자기회귀(Autoregressive)** 를 지킬 필요가 없기 때문",
     "encoder-decoder attention 이고, **쿼리(Query)** 가 디코더에서 오기 때문",
     "디코더 셀프 어텐션이고, **이차 비용(Quadratic Cost)** 을 줄이기 위해서"],
    0,
    "원문: 'self-attention layers in the decoder allow each position in the decoder to attend to all positions "
    "in the decoder up to and including that position. We need to prevent leftward information flow in the "
    "decoder to preserve the auto-regressive property.' 인코더 셀프 어텐션은 앞뒤를 모두 볼 수 있고, "
    "마스킹의 목적은 계산량 절약이 아니에요.")

mcq(U6, "NP p.6",
    "논문이 학습하는 위치 임베딩 대신 사인 코사인 방식을 고르며 든 근거와 그 서술 방식으로 옳은 것은?",
    [r"고정된 간격 $k$ 에 대해 $PE_{pos+k}$ 가 $PE_{pos}$ 의 선형 함수로 표현된다는 점을 들며 'we hypothesized' 라고 적었다",
     "상대 위치를 배울 수 있다는 것을 정리로 증명해서 적었다",
     "학습하는 위치 임베딩보다 BLEU 가 크게 높았기 때문이라고 적었다",
     "계산이 훨씬 빠르기 때문이라고 적었다"],
    0,
    r"원문: 'We chose this function because we hypothesized it would allow the model to easily learn to attend "
    r"by relative positions, since for any fixed offset $k$, $PE_{pos+k}$ can be represented as a linear "
    r"function of $PE_{pos}$.' 또 긴 문장으로 외삽할 수 있을지 모른다('may allow')는 이유도 들었는데 둘 다 추측이에요. "
    r"Table 3 (E) 에서 성능은 거의 같았으니 성능 때문에 고른 것이 아니에요.")

mcq(U7, "NP p.6-7",
    r"$d = 512$ 이고 문장 길이가 $n = 1000$ 일 때, Table 1 의 층당 복잡도로 따진 결과로 옳은 것은?",
    [r"$n$ 이 $d$ 보다 크므로 순환 층이 셀프 어텐션 층보다 싸다",
     r"$n$ 이 $d$ 보다 크므로 셀프 어텐션 층이 순환 층보다 싸다",
     r"$n$ 과 $d$ 에 상관없이 셀프 어텐션이 언제나 싸다",
     r"$n$ 과 $d$ 에 상관없이 순환이 언제나 싸다"],
    0,
    r"논문: 'self-attention layers are faster than recurrent layers when the sequence length $n$ is smaller "
    r"than the representation dimensionality $d$.' $n = 1000$ 이면 $n^2 d = 512{,}000{,}000$ 이고 "
    r"$n d^2 = 262{,}144{,}000$ 이라 순환 쪽이 약 1.95배 싸요. 갈림길은 $n = d = 512$ 예요.")

mcq(U7, "NP p.7",
    "논문이 **해석 가능성(Interpretability)** 을 다룬 방식으로 가장 적절한 것은?",
    ["'As side benefit, self-attention could yield more interpretable models' 라고 곁가지 이득이자 가능성으로 적고, "
     "부록의 그림을 예로 들었다",
     "셀프 어텐션이 언제나 해석 가능한 모델을 만든다고 단정했다",
     "해석 가능성을 4장의 비교 기준 세 가지 가운데 하나로 넣었다",
     "어텐션 가중치가 곧 문장의 문법 구조라는 것을 증명했다"],
    0,
    "4장의 비교 기준 세 가지는 계산 복잡도, 최소 순차 연산 수, 최대 경로 길이이고 해석 가능성은 거기에 들어가지 않아요. "
    "부록 그림 설명도 'apparently involved in anaphora resolution', 'seems related to the structure of the "
    "sentence' 처럼 단정하지 않는 말로 적혀 있어요.")

mcq(U8, "NP p.7",
    "warmup 구간이 끝난 뒤 학습률이 스텝 수의 역제곱근에 비례한다면, 스텝 수가 4배가 될 때 학습률은 어떻게 되는가?",
    ["2배가 된다", "절반이 된다", "4분의 1이 된다", "그대로다"],
    1,
    r"역제곱근이라 4배의 제곱근인 2 로 나눠요. 실제로 식 (3) 으로 계산하면 4000 스텝에서 0.000699, "
    r"16000 스텝에서 0.000349 로 정확히 절반이에요. 4분의 1이 되는 것은 역수에 비례할 때예요.")

mcq(U8, "NP p.8",
    "논문 5.4 가 적은 residual dropout 을 거는 자리로 옳은 것은?",
    ["각 하위층의 출력에(입력과 더해 정규화하기 전에), 그리고 인코더와 디코더 양쪽에서 임베딩과 위치 인코딩의 합에",
     "각 하위층의 출력에만, 그것도 정규화를 마친 다음에",
     "어텐션 가중치 행렬에만",
     "임베딩과 위치 인코딩의 합에만"],
    0,
    "원문: 'We apply dropout to the output of each sub-layer, before it is added to the sub-layer input and "
    "normalized. In addition, we apply dropout to the sums of the embeddings and the positional encodings in "
    "both the encoder and decoder stacks.' 거는 시점이 더하고 정규화하기 '전' 이라는 점과, 자리가 두 군데라는 점이 "
    "모두 중요해요.")

mcq(U9, "NP p.1",
    "English-to-French big 모델의 BLEU 점수가 논문에 적힌 방식으로 옳은 것은?",
    ["초록과 Table 2 는 41.8 이라고 적었는데 6.1 본문은 41.0 이라고 적어 논문 안에서 어긋난다",
     "세 곳 모두 41.8 로 같다",
     "세 곳 모두 41.0 으로 같다",
     "초록만 41.0 이고 Table 2 와 6.1 본문은 41.8 이다"],
    0,
    "초록은 'a new single-model state-of-the-art BLEU score of 41.8', Table 2 의 Transformer (big) EN-FR 칸도 41.8 "
    "인데, 6.1 본문은 'our big model achieves a BLEU score of 41.0' 이에요. 논문 자체가 어긋나 있어요. "
    "시험에는 초록과 Table 2 의 41.8 을 쓰세요.")

# =====================================================================
# OX (10, 절반이 거짓)
# =====================================================================
ox(U1, "NP p.1",
   "논문 초록은 트랜스포머가 **앙상블(Ensemble)** 을 뺀 단일 모델 최고 기록만 넘어섰다고 적었어요.",
   False,
   "English-to-German 에 대해서는 'improving over the existing best results, including ensembles, by over "
   "2 BLEU' 라고 적어 앙상블까지 포함해 넘었다고 밝혔어요. English-to-French 를 두고만 'single-model "
   "state-of-the-art' 라는 표현을 썼어요. 두 과제의 표현이 다르다는 점이 함정이에요.")

ox(U2, "NP p.2",
   "논문 1 Introduction 은 그때까지의 **어텐션(Attention)** 이 몇몇 경우를 빼면 대부분 순환 신경망과 함께 쓰였다고 적었어요.",
   True,
   "원문: 'In all but a few cases, however, such attention mechanisms are used in conjunction with a recurrent "
   "network.' 그래서 순환을 아예 빼겠다는 이 논문의 제안이 새로운 것이 돼요.")

ox(U3, "NP p.3",
   "디코더의 마스킹과 출력 임베딩을 한 자리 미루는 것이 함께 작용해서, 위치 $i$ 의 예측이 $i$ 보다 앞선 위치의 "
   "알려진 출력에만 기대게 돼요.",
   True,
   "원문: 'This masking, combined with fact that the output embeddings are offset by one position, ensures that "
   "the predictions for position $i$ can depend only on the known outputs at positions less than $i$.' "
   "Figure 1 의 Outputs (shifted right) 가 바로 이 한 자리 밀기예요. 마스킹 하나만으로 되는 것이 아니에요.")

ox(U4, "NP p.4",
   "논문은 **가산 어텐션(Additive Attention)** 이 **닷프로덕트 어텐션(Dot-Product Attention)** 보다 실제 구현에서 "
   "더 빠르고 메모리도 아낀다고 적었어요.",
   False,
   "방향이 반대예요. 원문은 'dot-product attention is much faster and more space-efficient in practice' 예요. "
   "가산 어텐션이 나은 것은 스케일링을 하지 않은 상태에서 $d_k$ 가 클 때의 품질이에요. 두 이야기를 섞지 마세요.")

ox(U5, "NP p.5",
   "인코더의 **셀프 어텐션(Self-Attention)** 에서 각 위치는 인코더 앞 층의 모든 위치에 주목할 수 있어요.",
   True,
   "원문: 'Each position in the encoder can attend to all positions in the previous layer of the encoder.' "
   "앞쪽만 볼 수 있는 것은 디코더 셀프 어텐션이에요.")

ox(U6, "NP p.6",
   "논문은 사인 코사인 방식이 학습하는 위치 임베딩보다 BLEU 가 뚜렷하게 높아서 사인 코사인을 골랐다고 적었어요.",
   False,
   "두 방식의 결과는 거의 같았어요(Table 3 (E), PPL 4.92, BLEU 25.7). 논문이 사인 코사인을 고른 까닭은 "
   "'it may allow the model to extrapolate to sequence lengths longer than the ones encountered during "
   "training' 이라는 추측이었어요. 성능 때문이 아니에요.")

ox(U7, "NP p.7",
   "논문은 **제한된 셀프 어텐션(Restricted Self-Attention)** 을 앞으로 더 살펴보겠다고만 적었고, 이 논문에서 "
   "실제로 실험하지는 않았어요.",
   True,
   "원문: 'We plan to investigate this approach further in future work.' Table 1 에는 복잡도 줄이 들어 있지만 "
   "성능 실험은 없어요. 표에 있다고 해서 실험했다고 넘겨짚지 마세요.")

ox(U8, "NP p.7-8",
   "논문 5.4 는 정칙화를 두 가지 쓴다고 적었고, 소제목도 Residual Dropout 과 Label Smoothing 둘이에요.",
   False,
   "소제목이 둘인 것은 맞지만, 논문이 적은 문장은 'We employ three types of regularization during training' "
   "이에요. 세 가지라고 적어 놓고 소제목은 둘만 달아 놓은 대목이라 논문 안에서 수가 맞지 않아요. "
   "드롭아웃이 하위층 출력과 임베딩 합, 두 자리에 걸린다는 점을 따로 센 것으로 읽을 수 있어요.")

ox(U9, "NP p.8",
   "논문은 base 모델은 마지막 체크포인트 5개를, big 모델은 마지막 20개를 평균해서 썼다고 적었어요.",
   True,
   "원문: 'For the base models, we used a single model obtained by averaging the last 5 checkpoints, which were "
   "written at 10-minute intervals. For the big models, we averaged the last 20 checkpoints.' "
   "다만 Table 3 의 모델 변형 실험에서는 체크포인트 평균을 쓰지 않았어요.")

ox(U9, "NP p.8",
   "English-to-French 로 학습한 big 모델은 $P_{drop} = 0.3$ 을 썼어요.",
   False,
   "원문: 'The Transformer (big) model trained for English-to-French used dropout rate $P_{drop} = 0.1$, "
   "instead of 0.3.' Table 3 의 big 줄에 적힌 0.3 은 English-to-German 쪽 설정이에요.")

# =====================================================================
# SHORT (8)
# =====================================================================
short(U2, "NP p.2",
      "논문 1 Introduction 이 P100 GPU 8장으로 새 최고 기록에 이를 수 있다고 적은 학습 시간을 시간 단위 숫자로 쓰시오.",
      ["12", "12시간", "twelve hours"],
      "원문: 'after being trained for as little as twelve hours on eight P100 GPUs.' "
      "5.2 절의 base 모델 학습 시간(100,000 스텝, 12시간)과 같은 이야기예요. 3.5일은 big 모델 쪽이에요.",
      num=True, tol=0.5)

short(U3, "NP p.3",
      "논문에 따른 디코더 한 층의 **하위층(Sub-layer)** 개수를 숫자로 쓰시오.",
      ["3", "3개", "세 개"],
      "마스킹된 멀티 헤드 셀프 어텐션, 인코더 스택 출력을 보는 멀티 헤드 어텐션, 위치별 FFN 이렇게 셋이에요. "
      "인코더 한 층은 둘이에요.",
      num=True, tol=0.5)

short(U4, "NP p.4",
      r"쿼리가 $n$ 개, 키가 $n$ 개일 때 식 (1) 에서 소프트맥스를 거치기 전 $QK^{T}$ 의 모양을 쓰시오.",
      ["n x n", "nxn", "(n, n)", "n by n", "n X n", "n*n"],
      r"$Q$ 는 $(n, d_k)$, $K^{T}$ 는 $(d_k, n)$ 이므로 곱하면 $(n, n)$ 이에요. "
      r"소프트맥스는 모양을 바꾸지 않고, $V$ 가 $(n, d_v)$ 이므로 최종 출력은 $(n, d_v)$ 가 돼요.")

short(U5, "NP p.5",
      "논문 3.2.3 의 세 가지 쓰임 가운데, 쿼리와 키와 밸류가 서로 다른 곳에서 오는 것은 어느 것인지 쓰시오.",
      ["encoder-decoder attention", "인코더-디코더 어텐션", "크로스 어텐션", "cross-attention",
       "encoder decoder attention"],
      "encoder-decoder attention 만 쿼리가 앞 디코더 층에서, 키와 밸류가 인코더 스택의 출력에서 와요. "
      "나머지 둘은 셀프 어텐션이라 셋이 모두 같은 곳에서 와요.")

short(U6, "NP p.6",
      "**위치 인코딩(Positional Encoding)** 을 임베딩에 더할 수 있으려면 둘의 무엇이 같아야 하는지 쓰시오.",
      ["차원", "d_model", "dimension", "차원(d_model)", "벡터 차원", "512"],
      "원문: 'The positional encodings have the same dimension $d_{model}$ as the embeddings, so that the two "
      "can be summed.' 차원이 같아야 더할 수 있어요. 이어 붙이는 것이 아니라 더한다는 점도 함께 기억하세요.")

short(U7, "NP p.6",
      "Table 1 의 가운데 열 Sequential Operations 는 논문이 든 세 가지 기준 가운데 무엇을 재는 것인지 쓰시오.",
      ["병렬화할 수 있는 계산량", "병렬화", "parallelization", "병렬화 가능성", "최소 순차 연산 수",
       "병렬화 가능한 계산량"],
      "원문: 'Another is the amount of computation that can be parallelized, as measured by the minimum number "
      "of sequential operations required.' 줄을 서서 해야 하는 계산이 적을수록 병렬화가 잘 되는 것이에요.")

short(U8, "NP p.7",
      "논문의 학습률 식 (3) 에서 학습률이 가장 커지는 스텝 수를 쓰시오.",
      ["4000", "4000 스텝", "warmup_steps"],
      r"식 (3) 은 $\min(\mathrm{step}^{-0.5}, \mathrm{step} \cdot \mathrm{warmup}^{-1.5})$ 라서, "
      r"두 항이 같아지는 step = warmup_steps = 4000 에서 꼭대기를 찍어요. 그 값은 0.000699 예요.",
      num=True, tol=1)

short(U9, "NP p.9",
      "Table 3 (A) 에서 헤드가 하나일 때 가장 좋은 설정보다 BLEU 가 얼마나 낮았는지 쓰시오.",
      ["0.9", "0.9 BLEU"],
      "원문: 'single-head attention is 0.9 BLEU worse than the best setting.' "
      "표에서 $h = 1$ 은 24.9 이고 가장 좋은 설정은 25.8 이라 $25.8 - 24.9 = 0.9$ 예요.",
      num=True, tol=0.05)

# =====================================================================
# ESSAY (5)
# =====================================================================
essay(U4, "NP p.4", "no-scaling-consequence",
      r"점수를 $\sqrt{d_k}$ 로 나누지 않으면 어떤 일이 생기는지 논문 각주 4 와 엮어 설명하고, 이 설명이 논문에서 "
      r"어떤 지위인지 밝히시오.",
      r"각주 4 는 $q$ 와 $k$ 의 각 성분이 평균 0, 분산 1 인 독립 확률변수라면 **내적(Dot Product)** 의 분산이 "
      r"$d_k$ 가 된다고 했어요. "
      r"곧 $d_k$ 가 커질수록 점수가 크게 흔들리고, 그 큰 점수를 **소프트맥스(Softmax)** 에 넣으면 분포가 거의 "
      r"한 자리에 몰려요. "
      r"논문은 이때 소프트맥스가 **기울기(Gradient)** 가 아주 작은 영역으로 밀린다고 적었어요. "
      r"그래서 표준편차인 $\sqrt{d_k}$ 로 나누어 점수의 크기를 되돌려 놓아요. "
      r"다만 논문은 이 대목을 'We suspect' 라고 적었어요. 증명한 사실이 아니라 저자들의 추측이에요. "
      r"실험 근거로 든 것은 '스케일링 없는 닷프로덕트는 $d_k$ 가 클 때 가산 어텐션보다 못하다' 는 선행 연구 결과예요.",
      [r"각주 4 의 가정은 평균 0, 분산 1", r"내적의 분산이 $d_k$",
       r"$d_k$ 가 크면 점수가 크게 흔들림", "소프트맥스가 거의 한 자리에 몰림",
       "기울기가 아주 작아져 학습이 어려워짐", r"$\sqrt{d_k}$ 로 나누어 크기를 되돌림",
       "논문은 'We suspect' 라고 적은 추측", "선행 연구 결과가 근거"])

essay(U5, "NP p.5", "why-multi-head",
      "**멀티 헤드 어텐션(Multi-Head Attention (MHA))** 이 단일 헤드보다 나은 까닭을 논문 문장에 근거해 설명하고, "
      "헤드를 8개로 늘려도 계산 비용이 비슷한 까닭을 서술하시오.",
      "논문은 멀티 헤드가 서로 다른 **표현 부분공간(Representation Subspace)** 의 정보에, 그것도 서로 다른 위치에서 "
      "동시에 주목하게 해 준다고 적었어요. "
      "헤드가 하나면 가중 평균을 내는 과정에서 그런 여러 갈래가 뭉개진다고 했어요('averaging inhibits this'). "
      "계산 비용이 비슷한 까닭은 헤드 수를 늘리면서 전체 차원을 키우는 것이 아니라 나눠 쓰기 때문이에요. "
      "$d_k = d_v = d_{model}/h = 512/8 = 64$ 라서 헤드 하나가 다루는 차원이 그만큼 작아져요. "
      "논문도 'Due to the reduced dimension of each head, the total computational cost is similar to that of "
      "single-head attention with full dimensionality' 라고 적었어요. "
      "실제로 Table 3 (A) 는 계산량을 고정한 채 헤드 수만 바꿔 본 실험이고, 헤드가 하나면 BLEU 가 0.9 낮았어요.",
      ["서로 다른 표현 부분공간에 동시에 주목", "서로 다른 위치에서 함께 봄",
       "헤드가 하나면 평균 때문에 막힘", "전체 차원을 키우지 않고 나눠 씀",
       r"$d_k = d_v = d_{model}/h = 64$", "총 계산 비용이 단일 헤드와 비슷",
       "Table 3 (A) 는 계산량을 고정한 실험", "단일 헤드는 BLEU 0.9 낮음"])

essay(U6, "NP p.6", "paper-vs-lecture-position",
      "논문이 위치 정보를 다루는 방식을 4주차 강의 슬라이드와 비교해 서술하시오.",
      "논문은 순환도 합성곱도 없어서 순서를 쓸 방법이 없다고만 적었고, 그 성질에 따로 이름을 붙이지 않았어요. "
      "4주차 슬라이드는 같은 성질을 **순열 등변성(Permutation Equivariance)** 이라고 부르고 '배리어 3개' 로 정리했는데, "
      "그 이름은 논문에 없어요. "
      "논문이 비교한 방식은 **사인 코사인 위치 인코딩(Sinusoidal Positional Encoding)** 과 학습하는 위치 임베딩 둘뿐이고, "
      "Table 3 (E) 에서 결과가 거의 같았어요. "
      "4주차 슬라이드는 여기에 RoPE 까지 소개하는데, RoPE 도 논문에 없는 뒷날 이야기예요. "
      "시험에서 '논문에 따르면' 이라고 물으면 이름도 방식도 논문이 적은 범위로만 답해야 해요.",
      ["논문은 순서 성질에 이름을 붙이지 않음", "순열 등변성은 슬라이드의 이름",
       "논문이 비교한 방식은 사인 코사인과 학습 임베딩 둘뿐", "Table 3 (E) 결과는 거의 같음",
       "RoPE 는 논문에 없음", "논문의 선택 이유는 외삽 가능성이라는 추측",
       "'논문에 따르면' 물음에는 논문 범위로만 답하기"])

essay(U7, "NP p.6-7", "self-attention-vs-recurrent-case",
      "Table 1 을 근거로 셀프 어텐션이 순환 층보다 유리한 경우와 불리한 경우를 수치를 들어 서술하시오.",
      r"셀프 어텐션의 층당 복잡도는 $O(n^2 \cdot d)$, 순환은 $O(n \cdot d^2)$ 라서 $n$ 과 $d$ 의 크기가 갈림길이에요. "
      r"$d = 512$, $n = 100$ 이면 각각 $5{,}120{,}000$ 과 $26{,}214{,}400$ 이라 셀프 어텐션이 약 5.12배 싸요. "
      r"$n = 512$ 면 둘 다 $134{,}217{,}728$ 로 같아지고, $n = 1000$ 이면 $512{,}000{,}000$ 대 $262{,}144{,}000$ 으로 "
      r"셀프 어텐션이 약 1.95배 비싸져요. "
      "다만 **순차 연산 수(Sequential Operations)** 와 **최대 경로 길이(Maximum Path Length)** 는 길이와 상관없이 "
      "셀프 어텐션이 $O(1)$, 순환이 $O(n)$ 이라 이 두 기준에서는 언제나 셀프 어텐션이 유리해요. "
      "논문은 기계 번역이 쓰는 word-piece 나 byte-pair 표현에서는 대개 $n < d$ 라고 적었어요. "
      r"$n$ 이 아주 커지면 이웃 $r$ 칸만 보는 **제한된 셀프 어텐션(Restricted Self-Attention)** 을 쓸 수 있지만, "
      r"그러면 최대 경로 길이가 $O(n/r)$ 로 늘어나요.",
      [r"갈림길은 $n$ 과 $d$ 의 크기", r"$n = 100$ 이면 5,120,000 대 26,214,400",
       r"$n = 512$ 에서 둘 다 134,217,728", r"$n = 1000$ 이면 셀프 어텐션이 약 1.95배 비쌈",
       "순차 연산 수와 경로 길이는 언제나 셀프 어텐션이 유리", "번역에서는 대개 $n < d$",
       r"제한하면 경로 길이가 $O(n/r)$ 로 늘어남"])

essay(U9, "NP p.8-10", "how-to-read-tables",
      "논문 6장의 Table 2, Table 3, Table 4 가 각각 무엇을 보이려는 표인지 설명하고, 읽을 때 주의할 점을 쓰시오.",
      "Table 2 는 newstest2014 에서의 BLEU 와 학습 비용(FLOPs)을 다른 모델과 견주어, 더 좋은 점수를 훨씬 적은 비용으로 "
      "얻었다는 것을 보여 줘요. big 모델이 EN-DE 28.4, EN-FR 41.8 이에요. "
      "Table 3 은 base 모델의 부품을 하나씩 바꿔 본 **모델 변형 실험(Model Variations)** 이고, 수치는 newstest2013 "
      "개발 집합이에요. "
      "Table 4 는 **구성소 구문 분석(Constituency Parsing)** 으로 옮겨도 잘 된다는 것을 보여 주고, WSJ only 91.3, "
      "준지도 92.7 이에요. "
      "주의할 점은 첫째, Table 2 와 Table 3 은 평가 집합이 달라서 25.8 과 27.3 을 바로 비교하면 안 된다는 것이에요. "
      "둘째, Table 3 의 퍼플렉서티는 per-wordpiece 라서 단어 단위 퍼플렉서티와 견줄 수 없다고 표 설명에 적혀 있어요. "
      "셋째, EN-FR big 점수는 초록과 Table 2 가 41.8, 6.1 본문이 41.0 이라 논문 자체가 어긋나 있으니 41.8 을 쓰세요.",
      ["Table 2 는 BLEU 와 학습 비용 비교", "big 은 EN-DE 28.4, EN-FR 41.8",
       "Table 3 은 부품을 바꿔 본 모델 변형 실험", "Table 3 은 newstest2013 개발 집합",
       "Table 4 는 구문 분석으로의 일반화, 91.3 과 92.7", "평가 집합이 달라 25.8 과 27.3 은 직접 비교 불가",
       "퍼플렉서티는 per-wordpiece", "EN-FR 41.8 과 41.0 이 어긋남, 41.8 을 쓴다"])

# =====================================================================
# CALC (6)
# =====================================================================
calc(U4, "NP p.4", "softmax-without-scaling",
     r"한 쿼리와 세 키의 **내적(Dot Product)** 원점수가 $(16, 8, 0)$ 이다. $\sqrt{d_k}$ 로 나누지 않고 그대로 "
     r"**소프트맥스(Softmax)** 를 씌웠을 때의 가중치와, $d_k = 64$ 로 나눈 뒤의 첫 번째 가중치를 각각 구하시오. "
     r"($e^{16} = 8886110$, $e^{8} = 2981.0$, $e^{0} = 1$)",
     "스케일을 하지 않으면 분포가 얼마나 한쪽으로 쏠리는지 보는 문제예요. 소수 넷째 자리까지 쓰세요.",
     [{"label": "스케일 없이 가중치 1", "ans": 0.9997, "tol": 0.00015},
      {"label": "스케일 없이 가중치 2", "ans": 0.0003, "tol": 0.00015},
      {"label": "스케일 없이 가중치 3", "ans": 0.0000, "tol": 0.00015},
      {"label": "스케일한 뒤 가중치 1", "ans": 0.6652, "tol": 0.001}],
     [r"스케일이 없으면 $\mathrm{softmax}(16, 8, 0)$ 을 그대로 계산해요",
      r"분자는 $8886110$, $2981.0$, $1$ 이고 합은 약 $8889092$ 예요",
      r"$8886110/8889092 = 0.999665$, $2981.0/8889092 = 0.000335$, $1/8889092 = 0.000000$ 이에요",
      r"$\sqrt{64} = 8$ 로 나누면 점수가 $(2, 1, 0)$ 이 되고 가중치는 $(0.6652, 0.2447, 0.0900)$ 이에요"],
     r"스케일 없이 $(0.9997, 0.0003, 0.0000)$, 스케일하면 첫 가중치가 $0.6652$",
     r"스케일이 없으면 거의 원-핫이 되어 한 자리만 보고 나머지는 버리게 돼요. 이때 **기울기(Gradient)** 가 거의 0 이라 "
     r"학습이 어려워진다는 것이 논문의 추측('We suspect')이에요.")

calc(U6, "NP p.6", "sinusoidal-pe-pos2",
     r"$d_{model} = 4$ 로 줄인 **사인 코사인 위치 인코딩(Sinusoidal Positional Encoding)** 에서 $pos = 2$ 의 네 칸을 "
     r"구하시오. ($\sin 2 = 0.9093$, $\cos 2 = -0.4161$, $\sin 0.02 = 0.0200$, $\cos 0.02 = 0.9998$)",
     r"각도는 $pos / 10000^{2i/d_{model}}$ 이고 짝수 칸이 sin, 홀수 칸이 cos 이에요. 소수 넷째 자리까지 쓰세요.",
     [{"label": "0 번째 칸", "ans": 0.9093, "tol": 0.001},
      {"label": "1 번째 칸", "ans": -0.4161, "tol": 0.001},
      {"label": "2 번째 칸", "ans": 0.0200, "tol": 0.001},
      {"label": "3 번째 칸", "ans": 0.9998, "tol": 0.001}],
     [r"$i = 0$ 이면 분모가 $10000^{0} = 1$ 이라 각도는 $pos = 2$ 예요",
      r"앞 두 칸은 $\sin 2 = 0.9093$, $\cos 2 = -0.4161$ 이에요",
      r"$i = 1$ 이면 분모가 $10000^{2/4} = 100$ 이라 각도는 $2/100 = 0.02$ 예요",
      r"뒤 두 칸은 $\sin 0.02 = 0.0200$, $\cos 0.02 = 0.9998$ 이에요"],
     r"$(0.9093, -0.4161, 0.0200, 0.9998)$",
     r"값이 음수가 될 수 있다는 점을 놓치기 쉬워요. $pos = 1$ 의 $(0.8415, 0.5403, 0.0100, 1.0000)$ 과 견주면 "
     r"앞쪽 칸은 빠르게, 뒤쪽 칸은 아주 느리게 변하는 것이 보여요.")

calc(U7, "NP p.6-7", "table1-tie-and-long",
     r"Table 1 에서 셀프 어텐션은 $O(n^2 \cdot d)$, 순환은 $O(n \cdot d^2)$ 이다. $d = 512$ 일 때 두 값이 같아지는 "
     r"$n = 512$ 에서의 공통 값과, $n = 1000$ 일 때 두 값, 그리고 순환 대비 셀프 어텐션의 배수를 구하시오.",
     r"$O$ 안의 식에 숫자를 그대로 넣어요. 배수는 소수 둘째 자리까지 쓰세요.",
     [{"label": "n=512 일 때 공통 값", "ans": 134217728},
      {"label": "n=1000 일 때 n^2 d", "ans": 512000000},
      {"label": "n=1000 일 때 n d^2", "ans": 262144000},
      {"label": "셀프 어텐션이 순환의 몇 배", "ans": 1.95, "tol": 0.01}],
     [r"$n = d$ 이면 $n^2 d = n \cdot d^2$ 가 되어 값이 같아져요",
      r"$512^2 \times 512 = 512 \times 512^2 = 134{,}217{,}728$ 이에요",
      r"$n = 1000$: $1000^2 \times 512 = 512{,}000{,}000$",
      r"$n = 1000$: $1000 \times 512^2 = 262{,}144{,}000$",
      r"$512{,}000{,}000 / 262{,}144{,}000 = 1.95$ 배예요"],
     r"공통 값 $134{,}217{,}728$, $n = 1000$ 에서 $512{,}000{,}000$ 대 $262{,}144{,}000$, 약 1.95배",
     r"$n = d$ 가 갈림길이에요. $n$ 이 $d$ 보다 작으면 셀프 어텐션이 싸고, 크면 비싸져요. "
     r"논문이 '$n$ 이 $d$ 보다 작을 때' 라는 단서를 붙인 까닭이 여기 있어요.")

calc(U8, "NP p.7", "warmup-learning-rate",
     r"논문 식 (3) 은 $lrate = d_{model}^{-0.5} \cdot \min(step^{-0.5}, step \cdot warmup^{-1.5})$ 이고 "
     r"$d_{model} = 512$, $warmup = 4000$ 이다. $d_{model}^{-0.5}$ 의 값과 step 4000, step 16000 에서의 학습률을 "
     r"구하시오.",
     "학습률이 꼭대기를 찍는 지점과 그 뒤 줄어드는 모양을 보는 문제예요. 소수 여섯째 자리까지 쓰세요.",
     [{"label": "d_model^(-0.5)", "ans": 0.044194, "tol": 0.0005},
      {"label": "step 4000 의 학습률", "ans": 0.000699, "tol": 0.00001},
      {"label": "step 16000 의 학습률", "ans": 0.000349, "tol": 0.00001}],
     [r"$512^{-0.5} = 1/\sqrt{512} = 0.044194$ 예요",
      r"step 4000 에서 $step^{-0.5} = 4000^{-0.5} = 0.015811$ 이고 $step \cdot warmup^{-1.5}$ 도 같은 값이라 "
      r"두 항이 만나요",
      r"$0.044194 \times 0.015811 = 0.000699$ 로 여기가 꼭대기예요",
      r"step 16000 에서는 $16000^{-0.5} = 0.007906$ 이라 $0.044194 \times 0.007906 = 0.000349$ 예요",
      r"스텝이 4배가 되면 학습률은 절반이 돼요"],
     r"$0.044194$, step 4000 에서 $0.000699$(최고), step 16000 에서 $0.000349$",
     "warmup 안에서는 학습률이 선형으로 오르고, warmup 을 지나면 역제곱근으로 줄어요. "
     "두 항 가운데 작은 쪽을 고른다는 점을 놓치면 꼭대기 지점을 틀려요.")

calc(U9, "NP p.7-8", "flops-check",
     r"논문은 학습 FLOPs 를 '학습 시간 x GPU 수 x GPU 한 장의 연산 능력' 으로 어림했다. big 모델은 P100 8장으로 "
     r"3.5일 학습했고 각주 5 는 P100 을 9.5 TFLOPS($9.5 \times 10^{12}$)로 잡았다. 초 단위 학습 시간, GPU 초, "
     r"그리고 총 FLOPs 를 $10^{19}$ 단위로 구하시오.",
     r"하루는 86,400초예요. 마지막 칸은 $10^{19}$ 을 단위로 소수 둘째 자리까지 쓰세요.",
     [{"label": "학습 시간(초)", "ans": 302400},
      {"label": "GPU 초", "ans": 2419200},
      {"label": "총 FLOPs (10^19 단위)", "ans": 2.30, "tol": 0.05}],
     [r"$3.5 \times 86{,}400 = 302{,}400$ 초예요",
      r"GPU 가 8장이므로 $302{,}400 \times 8 = 2{,}419{,}200$ GPU 초예요",
      r"$2{,}419{,}200 \times 9.5 \times 10^{12} = 2.298 \times 10^{19}$ 예요",
      r"$10^{19}$ 단위로 2.30 이고, Table 2 의 $2.3 \times 10^{19}$ 과 맞아요"],
     r"$302{,}400$ 초, $2{,}419{,}200$ GPU 초, 약 $2.3 \times 10^{19}$ FLOPs",
     "GPU 수를 빼먹으면 값이 8분의 1이 돼요. base 모델로 같은 계산을 하면 "
     "$12 \\times 3600 \\times 8 \\times 9.5 \\times 10^{12} = 3.28 \\times 10^{18}$ 이라 "
     "Table 2 의 $3.3 \\times 10^{18}$ 과 맞아요.")

calc(U9, "NP p.8-9", "bleu-gaps",
     "Table 2 와 Table 3 의 수치로 다음 차이를 구하시오. (1) big 모델 EN-DE 28.4 와 ConvS2S Ensemble 26.36 의 차이, "
     "(2) Table 3 (A) 에서 base 25.8 과 단일 헤드 24.9 의 차이, (3) big 모델 EN-FR 41.8 과 ConvS2S Ensemble 41.29 의 차이.",
     "표에서 두 수를 찾아 빼기만 하면 돼요. 소수 둘째 자리까지 쓰세요.",
     [{"label": "(1) EN-DE 차이", "ans": 2.04, "tol": 0.01},
      {"label": "(2) 헤드 수 차이", "ans": 0.9, "tol": 0.01},
      {"label": "(3) EN-FR 차이", "ans": 0.51, "tol": 0.01}],
     ["(1) $28.4 - 26.36 = 2.04$ 라서 논문이 'by more than 2.0 BLEU' 라고 적었어요",
      "(2) $25.8 - 24.9 = 0.9$ 라서 논문이 'single-head attention is 0.9 BLEU worse' 라고 적었어요",
      "(3) $41.8 - 41.29 = 0.51$ 이에요",
      "(1)과 (3)은 newstest2014, (2)는 newstest2013 개발 집합의 수치라 서로 섞으면 안 돼요"],
     "2.04, 0.9, 0.51",
     "논문 본문의 표현('more than 2.0 BLEU', '0.9 BLEU worse')이 어느 두 수에서 나온 것인지 짚을 수 있어야 해요. "
     "EN-FR 은 6.1 본문이 41.0 이라고 적어 논문 안에서 어긋나는데, Table 2 와 초록의 41.8 을 씁니다.")

# =====================================================================
# ------------------------------------------------- 보기 자리 섞기와 id 고정
optshuffle.shuffle_bank(bank)
IDS = [
    "wPh-mcq-001", "wPh-mcq-002", "wPh-mcq-003", "wPh-mcq-004", "wPh-mcq-005",
    "wPh-mcq-006", "wPh-mcq-007", "wPh-mcq-008", "wPh-mcq-009", "wPh-mcq-010",
    "wPh-mcq-011", "wPh-mcq-012", "wPh-mcq-013", "wPh-mcq-014", "wPh-mcq-015",
    "wPh-ox-001", "wPh-ox-002", "wPh-ox-003", "wPh-ox-004", "wPh-ox-005",
    "wPh-ox-006", "wPh-ox-007", "wPh-ox-008", "wPh-ox-009", "wPh-ox-010",
    "wPh-short-001", "wPh-short-002", "wPh-short-003", "wPh-short-004",
    "wPh-short-005", "wPh-short-006", "wPh-short-007", "wPh-short-008",
    "wPh-essay-001", "wPh-essay-002", "wPh-essay-003", "wPh-essay-004", "wPh-essay-005",
    "wPh-calc-001", "wPh-calc-002", "wPh-calc-003", "wPh-calc-004", "wPh-calc-005",
    "wPh-calc-006",
]
optshuffle.check_ids(bank, IDS)

raw = json.dumps(bank, ensure_ascii=False, indent=1)
for ch in ("—", "–", "·", "・"):
    assert ch not in raw, ch
n_false = sum(1 for it in bank if it["type"] == "ox" and it["a"] is False)
assert n_false == 5, n_false
with open(OUT, "w", encoding="utf-8") as f:
    f.write(raw)
print("saved", OUT, len(bank), "문항", cnt, "ox false", n_false)
