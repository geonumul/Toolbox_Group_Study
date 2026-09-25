# -*- coding: utf-8 -*-
"""참고 논문 덱(NP) Attention Is All You Need 회독 레슨 5~9쪽 생성기.
사용: python build_NP_005-009.py   출력: NP_005-009.json
손계산은 아래에서 파이썬으로 실제 계산해 assert 로 확인한다."""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "NP_005-009.json")


# ---------------- 손계산 확인 (계산하고 assert) ----------------
D_MODEL, H, D_FF = 512, 8, 2048
D_K = D_V = D_MODEL // H
assert D_K == 64 and D_V == 64
assert D_FF == 4 * D_MODEL == 2048
assert math.sqrt(D_K) == 8.0

# 3.2.2 멀티 헤드 파라미터 수 (논문이 직접 적지 않은 값. 우리가 센 것이라고 밝힌다)
WQ_ONE_HEAD = D_MODEL * D_K
assert WQ_ONE_HEAD == 32768
PER_HEAD = 3 * WQ_ONE_HEAD
assert PER_HEAD == 98304
ALL_HEADS = H * PER_HEAD
assert ALL_HEADS == 786432 == 3 * D_MODEL * D_MODEL
WO = (H * D_V) * D_MODEL
assert WO == 262144 == D_MODEL * D_MODEL
MHA_TOTAL = ALL_HEADS + WO
assert MHA_TOTAL == 1048576 == 4 * D_MODEL * D_MODEL

# 3.3 FFN 파라미터 수
W1 = D_MODEL * D_FF
W2 = D_FF * D_MODEL
assert W1 == W2 == 1048576
FFN_TOTAL = W1 + W2
assert FFN_TOTAL == 2097152 == 2 * D_MODEL * D_FF
assert 2048 + 512 == 2560  # 편향 항 b1 과 b2 의 개수

# 스택 전체 (어림)
ENC_LAYER = MHA_TOTAL + FFN_TOTAL
assert ENC_LAYER == 3145728
DEC_LAYER = 2 * MHA_TOTAL + FFN_TOTAL
assert DEC_LAYER == 4194304
assert ENC_LAYER * 6 == 18874368
assert DEC_LAYER * 6 == 25165824
VOCAB = 37000
EMB_PARAMS = VOCAB * D_MODEL
assert EMB_PARAMS == 18944000
TOTAL = ENC_LAYER * 6 + DEC_LAYER * 6 + EMB_PARAMS
assert TOTAL == 62984192
assert round(TOTAL / 1e6, 2) == 62.98  # 논문 Table 3 의 65 와 가깝지만 같지는 않아요

# Table 1 손계산 (d = 512)
def sa_cost(n, d=D_MODEL):
    return n * n * d


def rnn_cost(n, d=D_MODEL):
    return n * d * d


assert sa_cost(100) == 5120000 and rnn_cost(100) == 26214400
assert round(rnn_cost(100) / sa_cost(100), 2) == 5.12
assert sa_cost(512) == rnn_cost(512) == 134217728
assert sa_cost(1000) == 512000000 and rnn_cost(1000) == 262144000
assert round(sa_cost(1000) / rnn_cost(1000), 2) == 1.95

# 3.5 위치 인코딩 손계산 (장난감 d_model = 4)
def pe_row(pos, dm=4):
    out = []
    for i in range(dm // 2):
        ang = pos / (10000 ** (2 * i / dm))
        out += [round(math.sin(ang), 4), round(math.cos(ang), 4)]
    return out


assert pe_row(0) == [0.0, 1.0, 0.0, 1.0]
assert pe_row(1) == [0.8415, 0.5403, 0.01, 1.0]
assert pe_row(2) == [0.9093, -0.4161, 0.02, 0.9998]
assert pe_row(3) == [0.1411, -0.99, 0.03, 0.9996]
assert round(2 * math.pi, 4) == 6.2832
assert round(10000 ** (510 / 512), 1) == 9646.6
assert 10000 ** 0 == 1

# 5.2 학습 시간 검산
assert 100000 * 0.4 == 40000.0
assert round(40000 / 3600, 1) == 11.1  # 논문은 12시간이라고 적었어요
assert round(300000 * 1.0 / 86400, 2) == 3.47  # 논문은 3.5일이라고 적었어요

# 5.3 학습률 식 (3) 손계산, warmup_steps = 4000
WARMUP = 4000


def lrate(step, warmup=WARMUP, dm=D_MODEL):
    return dm ** -0.5 * min(step ** -0.5, step * warmup ** -1.5)


assert round(D_MODEL ** -0.5, 6) == 0.044194
assert round(WARMUP ** -0.5, 6) == 0.015811
assert round(lrate(1000), 6) == 0.000175
assert round(lrate(2000), 6) == 0.000349
assert round(lrate(4000), 6) == 0.000699
assert round(lrate(8000), 6) == 0.000494
assert round(lrate(16000), 6) == 0.000349
assert round(lrate(100000), 6) == 0.00014
assert round(lrate(16000), 6) == round(lrate(2000), 6)  # 4000 을 기준으로 좌우가 만나요
assert round(lrate(4000) / lrate(16000), 2) == 2.0  # 스텝 4배에 학습률 절반

# 6.1 과 Table 2 검산
assert round(28.4 - 26.36, 2) == 2.04
FLOPS_BIG = 3.5 * 86400 * 8 * 9.5e12
assert round(FLOPS_BIG / 1e19, 2) == 2.30
FLOPS_BASE = 12 * 3600 * 8 * 9.5e12
assert round(FLOPS_BASE / 1e18, 2) == 3.28

# Table 3 검산
assert round(25.8 - 24.9, 1) == 0.9
assert round(26.4 - 25.8, 1) == 0.6
assert 213 // 65 == 3


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
RELU = "**렐루(ReLU)**"
PE = "**위치 인코딩(Positional Encoding)**"
SPE = "**사인 코사인 위치 인코딩(Sinusoidal Positional Encoding)**"
ROPE = "**로프(RoPE)**"
PEQ = "**순열 등변성(Permutation Equivariance)**"
EMB = "**임베딩(Embedding)**"
TOK = "**토큰(Token)**"
PARAM = "**파라미터(Parameter)**"
CM = "**인과 마스킹(Causal Masking)**"
AR = "**자기회귀(Autoregressive)**"
PAR = "**병렬화(Parallelization)**"
QC = "**이차 비용(Quadratic Cost)**"
RNN = "**순환 신경망(Recurrent Neural Network (RNN))**"
CNN = "**합성곱 신경망(Convolutional Neural Network (CNN))**"
MT = "**기계 번역(Machine Translation (MT))**"
BLEU = "**블루 점수(BLEU)**"
PPL = "**퍼플렉서티(Perplexity (PPL))**"
BEAM = "**빔 서치(Beam Search)**"
LNORM = "**길이 정규화(Length Normalization)**"
BPE = "**바이트 쌍 인코딩(Byte Pair Encoding (BPE))**"
WP = "**워드피스(WordPiece)**"
VOC = "**어휘(Vocabulary)**"
MPL = "**최대 경로 길이(Maximum Path Length)**"
SEQOP = "**순차 연산 수(Sequential Operations)**"
RSUB = "**표현 부분공간(Representation Subspace)**"
RSA = "**제한된 셀프 어텐션(Restricted Self-Attention)**"
DROP = "**드롭아웃(Dropout)**"
LS = "**라벨 스무딩(Label Smoothing)**"
ADAM = "**아담(Adam)**"
WARM = "**워밍업(Warmup)**"
CKPT = "**체크포인트 평균(Checkpoint Averaging)**"
CP = "**구성소 구문 분석(Constituency Parsing)**"
MV = "**모델 변형 실험(Model Variations)**"
OVF = "**과적합(Over-fitting)**"
ENS = "**앙상블(Ensemble)**"
FLOPS = "**부동소수점 연산량(FLOPs)**"
LR = "**학습률(Learning Rate)**"
GRAD = "**기울기(Gradient)**"
INTP = "**해석 가능성(Interpretability)**"
S2S = "**시퀀스-투-시퀀스(seq2seq)**"

WHEN = "4주차 월요일 수업"

GLOSSARY = [
    ("트랜스포머", "Transformer", "어텐션만으로 만든 신경망 구조. 이 논문이 내놓은 모델이에요",
     "인코더 6층과 디코더 6층을 쌓았어요. base 모델의 파라미터는 약 65 x 10^6 개예요."),
    ("어텐션", "Attention", "필요한 곳을 골라 보는 장치. 점수를 매기고 가중 평균을 내요",
     "논문은 이것을 세 가지 자리에서 쓴다고 3.2.3 에 적었어요."),
    ("셀프 어텐션", "Self-Attention", "한 문장이 자기 자신을 바라보는 어텐션",
     "쿼리, 키, 밸류가 모두 앞 층 출력 한 곳에서 나와요."),
    ("크로스 어텐션", "Cross-Attention", "쿼리는 디코더, 키와 밸류는 인코더에서 오는 어텐션",
     "논문은 encoder-decoder attention 이라고 불러요. 이름만 다른 같은 것이에요."),
    ("멀티 헤드 어텐션", "Multi-Head Attention (MHA)", "전체 차원을 h 조각으로 나눠 여러 관점에서 동시에 어텐션하기",
     "논문은 h = 8, d_k = d_v = 64 를 썼어요. 계산량은 한 개짜리와 비슷해요."),
    ("헤드", "Head", "멀티 헤드 어텐션에서 한 관점을 맡은 작은 어텐션 하나",
     "헤드 하나가 64칸을 봐요. 8개를 이어 붙여 다시 512칸이 돼요."),
    ("표현 부분공간", "Representation Subspace", "전체 차원을 조각내어 만든 작은 관점 하나",
     "논문은 different representation subspaces at different positions 라고 적었어요."),
    ("스케일드 닷프로덕트 어텐션", "Scaled Dot-Product Attention", "내적 점수를 루트 d_k 로 나눈 어텐션",
     "헤드 하나가 이 계산을 해요. 멀티 헤드는 이것을 h 개 나란히 돌려요."),
    ("쿼리", "Query", "지금 내가 무엇을 찾고 있는지를 담은 벡터",
     "크로스 어텐션에서는 디코더에서 나와요."),
    ("키", "Key", "나는 이런 정보를 갖고 있다고 광고하는 이름표 벡터",
     "크로스 어텐션에서는 인코더 출력에서 나와요. 논문은 memory keys 라고 불러요."),
    ("밸류", "Value", "내가 선택되면 실제로 건네줄 내용 벡터",
     "가중합에 실제로 들어가는 것은 밸류예요. 논문의 d_v 는 64 예요."),
    ("어텐션 가중치", "Attention Weight", "점수를 소프트맥스에 넣어 얻은, 합이 1 인 값들",
     "논문 부록의 어텐션 그림이 이 값을 선 굵기로 그린 것이에요."),
    ("가중합", "Weighted Sum", "값마다 가중치를 곱해서 모두 더한 것",
     "어텐션의 마지막 단계예요. 결과가 그 자리의 새 표현이 돼요."),
    ("소프트맥스", "Softmax", "점수를 모두 더해 1 이 되는 확률 파이로 나누기",
     "논문 3.4 는 디코더 출력을 소프트맥스로 다음 토큰 확률로 바꾼다고 적었어요."),
    ("내적", "Dot Product", "두 화살표가 얼마나 같은 쪽을 보는지 재는 곱셈",
     "논문 6.2 는 내적보다 더 정교한 호환성 함수가 나을 수도 있다고 적었어요."),
    ("인코더", "Encoder", "입력 문장을 끝까지 읽어 자리마다 표현을 만드는 쪽",
     "인코더의 셀프 어텐션은 마스킹을 하지 않아 앞뒤를 다 봐요."),
    ("디코더", "Decoder", "답 문장을 한 토큰씩 만들어 내는 쪽",
     "디코더의 셀프 어텐션은 자기 자리까지만 봐요. 미래는 막아요."),
    ("하위층", "Sub-layer", "한 층 안에 들어 있는 더 작은 층 한 덩어리",
     "논문 5.4 는 하위층 출력마다 드롭아웃을 쓴다고 적었어요."),
    ("잔차 연결", "Residual Connection", "층의 입력을 층의 출력에 그대로 더해 주는 지름길",
     "드롭아웃은 이 더하기 직전에 걸려요."),
    ("층 정규화", "Layer Normalization (LayerNorm)", "한 토큰의 숫자들을 평균 0, 분산 1 로 맞춰 주기",
     "논문은 더한 다음에 정규화하는 순서만 썼어요."),
    ("위치별 피드포워드 신경망", "Position-wise Feed-Forward Network (FFN)", "자리마다 똑같이 적용하는 2층짜리 작은 신경망",
     "식 (2) 가 정의예요. d_model 512, 가운데 d_ff 2048 이에요."),
    ("렐루", "ReLU", "음수는 0 으로 만들고 양수는 그대로 두는 함수",
     "식 (2) 의 max(0, ...) 가 바로 이것이에요. 3주차에 배웠어요."),
    ("위치 인코딩", "Positional Encoding", "몇 번째 자리인지를 알려 주는 벡터를 임베딩에 더해 주기",
     "논문 3.5 의 부품이에요. 인코더와 디코더 스택 맨 아래에서 한 번 더해요."),
    ("사인 코사인 위치 인코딩", "Sinusoidal Positional Encoding", "sin 과 cos 파도로 만든, 학습하지 않는 위치 벡터",
     "짝수 칸은 sin, 홀수 칸은 cos 이에요. 학습 파라미터가 0 개예요."),
    ("순열 등변성", "Permutation Equivariance", "입력 순서를 바꾸면 출력도 똑같이 순서만 바뀌는 성질",
     "4주차 슬라이드의 말이에요. 논문은 이 이름을 쓰지 않아요."),
    ("로프", "RoPE", "쿼리와 키를 위치에 비례한 각도만큼 회전시키는 위치 방식",
     "4주차 슬라이드 p.41 에 나와요. 2017년 논문에는 없어요."),
    ("임베딩", "Embedding", "토큰을 숫자 벡터로 바꾼 것. 단어의 지도 좌표",
     "논문 3.4 는 두 임베딩 층과 소프트맥스 앞 선형 변환이 같은 행렬을 쓴다고 적었어요."),
    ("토큰", "Token", "글을 자른 레고 조각 하나",
     "논문의 배치는 원문 약 25,000 토큰, 번역문 약 25,000 토큰이에요."),
    ("파라미터", "Parameter", "학습하면서 바뀌는 숫자. 모델이 기억을 저장하는 자리",
     "Table 3 의 params 칸이 이 개수예요. base 는 65, big 은 213 (백만 단위)이에요."),
    ("인과 마스킹", "Causal Masking", "미래 자리의 점수를 소프트맥스 전에 마이너스 무한으로 바꾸기",
     "논문 3.2.3 은 이것을 leftward information flow 를 막는 장치라고 적었어요."),
    ("자기회귀", "Autoregressive", "앞에서 만든 토큰을 보고 다음 토큰을 하나씩 만드는 방식",
     "마스킹은 이 성질을 지키려고 넣은 것이에요."),
    ("병렬화", "Parallelization", "여러 계산을 한꺼번에 동시에 하기",
     "Table 1 의 순차 연산 수가 이것을 재는 잣대예요."),
    ("이차 비용", "Quadratic Cost", "길이 n 이 두 배가 되면 비용이 네 배가 되는 것",
     "셀프 어텐션의 복잡도 O(n^2 x d) 가 이것이에요. 긴 글에서 아파요."),
    ("순환 신경망", "Recurrent Neural Network (RNN)", "한 단어씩 읽으며 메모장에 요약을 고쳐 쓰는 신경망",
     "Table 1 에서 순차 연산 수가 O(n) 인 유일한 줄이에요."),
    ("합성곱 신경망", "Convolutional Neural Network (CNN)", "가까운 이웃 몇 칸을 묶어서 보는 신경망",
     "커널 k 가 n 보다 작으면 한 층으로는 모든 쌍을 잇지 못해요."),
    ("최대 경로 길이", "Maximum Path Length", "두 자리 사이에 신호가 지나가야 하는 가장 먼 걸음 수",
     "Table 1 의 마지막 칸이에요. 셀프 어텐션만 O(1) 이에요."),
    ("순차 연산 수", "Sequential Operations", "줄을 서서 차례로 해야만 하는 계산의 개수",
     "Table 1 의 가운데 칸이에요. 적을수록 병렬화가 잘 돼요."),
    ("제한된 셀프 어텐션", "Restricted Self-Attention", "가까운 이웃 r 칸만 보게 제한한 셀프 어텐션",
     "Table 1 의 마지막 줄이에요. 논문은 앞으로 해 보겠다고만 적었어요."),
    ("해석 가능성", "Interpretability", "모델이 왜 그렇게 답했는지 사람이 들여다볼 수 있는 정도",
     "논문은 어텐션 가중치를 보면 헤드가 무엇을 배웠는지 보인다고 적었어요."),
    ("기계 번역", "Machine Translation (MT)", "한 언어 문장을 다른 언어 문장으로 바꾸는 과제",
     "WMT 2014 영어-독일어와 영어-프랑스어가 논문의 주 실험이에요."),
    ("블루 점수", "BLEU", "기계 번역 결과가 사람 번역과 얼마나 겹치는지 재는 점수",
     "높을수록 좋아요. Table 2 와 Table 3 의 주 지표예요."),
    ("퍼플렉서티", "Perplexity (PPL)", "다음 토큰을 고를 때 헷갈리는 후보가 평균 몇 개인지",
     "낮을수록 좋아요. Table 3 의 PPL 은 워드피스 단위라 단어 단위와 비교하면 안 돼요."),
    ("빔 서치", "Beam Search", "후보 문장 여러 개를 동시에 끌고 가며 가장 좋은 것을 고르는 방법",
     "논문은 빔 크기 4 를 썼어요. 구문 분석에서는 21 을 썼어요."),
    ("길이 정규화", "Length Normalization", "긴 문장이 손해 보지 않게 점수를 길이로 눌러 주기",
     "논문은 length penalty alpha = 0.6 이라고 적었어요."),
    ("바이트 쌍 인코딩", "Byte Pair Encoding (BPE)", "자주 붙어 다니는 두 조각을 한 조각으로 접착하는 토큰화",
     "영어-독일어에서 원문과 번역문이 어휘 약 37,000 개를 함께 썼어요."),
    ("워드피스", "WordPiece", "BPE 와 비슷하게 단어를 조각으로 자르는 토큰화 방법",
     "영어-프랑스어는 어휘 32,000 개짜리 워드피스를 썼어요."),
    ("어휘", "Vocabulary", "모델이 아는 토큰 종류 목록",
     "공유 어휘를 쓰면 원문과 번역문이 같은 임베딩 표를 나눠 써요."),
    ("드롭아웃", "Dropout", "학습할 때 일부 값을 무작위로 꺼서 과적합을 막는 방법",
     "논문의 base 는 P_drop = 0.1 이에요. big 은 0.3 이지만 영어-프랑스어만 0.1 이에요."),
    ("라벨 스무딩", "Label Smoothing", "정답을 100%로 두지 않고 살짝 흐리게 만들어 학습하는 방법",
     "eps_ls = 0.1 이에요. 퍼플렉서티는 나빠지지만 BLEU 는 좋아져요."),
    ("과적합", "Over-fitting", "학습 데이터만 외워 버려서 새 데이터에 약해지는 것",
     "논문 6.2 는 드롭아웃이 이것을 막는 데 아주 도움이 된다고 적었어요."),
    ("아담", "Adam", "요즘 가장 많이 쓰는 학습 방법 중 하나",
     "논문은 beta1 = 0.9, beta2 = 0.98, epsilon = 10^-9 을 썼어요."),
    ("워밍업", "Warmup", "학습 초반에 학습률을 0에서부터 천천히 올리는 구간",
     "논문은 warmup_steps = 4000 을 썼어요. 4000 스텝에서 학습률이 가장 높아요."),
    ("학습률", "Learning Rate", "한 걸음에 얼마나 크게 움직일지 정하는 값",
     "식 (3) 이 스텝마다 이 값을 정해요. 올렸다가 역제곱근으로 내려요."),
    ("기울기", "Gradient", "손실이 가장 빨리 커지는 방향과 그 가파름",
     "학습률과 곱해져서 파라미터를 고치는 크기를 정해요."),
    ("체크포인트 평균", "Checkpoint Averaging", "마지막 저장본 여러 개의 가중치를 평균 내서 한 모델로 쓰기",
     "base 는 마지막 5개, big 은 마지막 20개를 평균했어요."),
    ("앙상블", "Ensemble", "여러 모델의 답을 합쳐서 성능을 올리는 방법",
     "Table 2 의 Ensemble 줄들이 이것이에요. 트랜스포머는 단일 모델로 이것들을 이겼어요."),
    ("부동소수점 연산량", "FLOPs", "학습에 들어간 계산의 총량을 재는 단위",
     "논문은 학습 시간 x GPU 수 x GPU 성능으로 어림했다고 적었어요."),
    ("모델 변형 실험", "Model Variations", "한 부품씩 바꿔 보며 성능이 어떻게 변하는지 재는 실험",
     "Table 3 의 (A)부터 (E)까지가 이것이에요. 논문의 6.2 제목이기도 해요."),
    ("구성소 구문 분석", "Constituency Parsing", "문장을 구 단위 나무 구조로 쪼개는 과제",
     "논문이 번역 말고 하나 더 해 본 과제예요. 6.3 에 나와요."),
    ("시퀀스-투-시퀀스", "seq2seq", "입력 줄을 받아 출력 줄을 만드는 인코더 디코더 모델",
     "논문 3.2.3 은 크로스 어텐션이 이 모델들의 어텐션을 흉내 낸 것이라고 적었어요."),
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
FIG_MH = SVG(
    TX(240, 22, "512 칸을 8 조각으로 나눠요", "tb", 16),
    BOX(60, 42, 360, 28, "d_model = 512", "box", "tb", 1, 14),
    *[A(90 + i * 43, 74, 90 + i * 43, 96, "e2", 2) for i in range(8)],
    *[R(68 + i * 43, 98, 38, 26, "box2", 2) for i in range(8)],
    *[TX(87 + i * 43, 116, f"h{i + 1}", "tb", 11, "middle", 2) for i in range(8)],
    TX(240, 144, "헤드 하나가 512 / 8 = 64 칸이에요", "tb", 13, "middle", 3),
    *[A(87 + i * 43, 154, 240, 176, "e", 4) for i in range(8)],
    BOX(120, 178, 240, 28, "이어 붙이면 다시 512 칸", "box", "tb", 4, 13),
    TX(240, 232, "그다음 W^O 를 한 번 곱해요", "t", 13, "middle", 4),
    TX(240, 256, "전체 차원을 키우는 게 아니라 나누는 거예요", "tm", 12, "middle", 4),
)

FIG_PE = SVG(
    TX(240, 22, "자리마다 다른 숫자 묶음", "tb", 16),
    TX(60, 52, "자리", "tb", 13, "middle", 1),
    TX(250, 52, "d_model = 4 일 때 위치 벡터", "tb", 13, "middle", 1),
    *[TX(60, 84 + i * 30, t, "t", 13, "middle", 2) for i, t in enumerate(["pos 0", "pos 1", "pos 2", "pos 3"])],
    *[R(110, 68 + i * 30, 280, 22, "box2" if i % 2 else "box", 2) for i in range(4)],
    TX(250, 84, "0.0, 1.0, 0.0, 1.0", "tb", 12, "middle", 3),
    TX(250, 114, "0.8415, 0.5403, 0.0100, 1.0", "tb", 12, "middle", 3),
    TX(250, 144, "0.9093, -0.4161, 0.0200, 0.9998", "tb", 12, "middle", 3),
    TX(250, 174, "0.1411, -0.9900, 0.0300, 0.9996", "tb", 12, "middle", 3),
    TX(240, 212, "앞 두 칸은 빠르게 흔들리고 뒤 두 칸은 아주 천천히 변해요", "tb", 13, "middle", 4),
    TX(240, 236, "이 묶음을 토큰 임베딩에 그냥 더해요", "tm", 12, "middle", 4),
)

FIG_LR = SVG(
    TX(240, 22, "식 (3) 학습률: 올렸다가 내려요", "tb", 16),
    L(50, 200, 440, 200, "e", 1),
    L(50, 200, 50, 50, "e", 1),
    TX(40, 60, "높음", "tm", 11, "end", 1),
    TX(40, 198, "0", "tm", 11, "end", 1),
    R(80, 175, 20, 25, "n2", 2), R(110, 150, 20, 50, "n2", 2), R(140, 125, 20, 75, "n2", 2),
    R(170, 100, 20, 100, "n2", 2),
    R(200, 71, 20, 129, "n4", 3),
    R(240, 108, 20, 92, "n", 4), R(270, 125, 20, 75, "n", 4), R(300, 137, 20, 63, "n", 4),
    R(330, 146, 20, 54, "n", 4), R(360, 153, 20, 47, "n", 4), R(390, 159, 20, 41, "n", 4),
    TX(210, 216, "4000 스텝", "tm", 11, "middle", 3),
    TX(240, 240, "4000 까지는 직선으로 오르고 뒤로는 역제곱근으로 내려요", "tb", 13, "middle", 4),
    TX(240, 262, "최고점은 0.000699 예요", "tm", 12, "middle", 4),
    h=280,
)

FIG_T2 = SVG(
    TX(240, 22, "영어-독일어 BLEU 막대", "tb", 16),
    *[TX(96, 60 + i * 34, t, "t", 12, "end", 1)
      for i, t in enumerate(["ByteNet 23.75", "GNMT+RL 24.6", "ConvS2S ens 26.36", "base 27.3", "big 28.4"])],
    R(106, 46 + 0 * 34, 138, 20, "n", 1),
    R(106, 46 + 1 * 34, 153, 20, "n", 1),
    R(106, 46 + 2 * 34, 214, 20, "n2", 2),
    R(106, 46 + 3 * 34, 250, 20, "box", 3),
    R(106, 46 + 4 * 34, 268, 20, "box2", 4),
    TX(240, 208, "28.4 - 26.36 = 2.04 라서 2.0 BLEU 넘게 앞섰다고 적었어요", "tb", 13, "middle", 4),
    TX(240, 232, "base 27.3 도 앙상블 26.36 보다 높아요", "tm", 12, "middle", 4),
)

FIG_T3 = SVG(
    TX(240, 22, "헤드 수를 바꿨을 때 (Table 3 A)", "tb", 16),
    *[TX(70 + i * 90, 52, t, "tb", 13, "middle", 1)
      for i, t in enumerate(["h = 1", "h = 4", "h = 8", "h = 16", "h = 32"])],
    R(44 + 0 * 90, 150, 52, 40, "n4", 2),
    R(44 + 1 * 90, 126, 52, 64, "n2", 2),
    R(44 + 2 * 90, 116, 52, 74, "box", 3),
    R(44 + 3 * 90, 116, 52, 74, "box", 3),
    R(44 + 4 * 90, 128, 52, 62, "n2", 3),
    *[TX(70 + i * 90, 208, t, "t", 12, "middle", 3)
      for i, t in enumerate(["24.9", "25.5", "25.8", "25.8", "25.4"])],
    TX(240, 236, "하나면 0.9 낮고, 너무 많아도 떨어져요", "tb", 13, "middle", 4),
    TX(240, 258, "계산량은 다섯 경우 모두 같게 맞췄어요", "tm", 12, "middle", 4),
    h=280,
)

S = []


def page(p, title, terms, p1, p2=(), p3=(), p4=()):
    S.append({"p": p, "title": title, "terms": list(terms),
              "pass1": list(p1), "pass2": list(p2), "pass3": list(p3), "pass4": list(p4)})


# ---------------------------------------------------------------- p.5
page(5, "멀티 헤드, 어텐션의 세 가지 쓰임, FFN (식 2), 임베딩",
     ["Multi-Head Attention (MHA)", "Head", "Representation Subspace", "Scaled Dot-Product Attention",
      "Self-Attention", "Cross-Attention", "Attention", "Query", "Key", "Value", "Encoder", "Decoder",
      "Causal Masking", "Autoregressive", "Position-wise Feed-Forward Network (FFN)", "ReLU",
      "Embedding", "Softmax", "Parameter", "Token", "Sub-layer", "seq2seq", "Weighted Sum",
      "Attention Weight", "Layer Normalization (LayerNorm)", "Dot Product", "Parallelization"],
     [say(f"이 쪽에 부품 세 개가 몰려 있어요. 첫째가 {MHA} 예요.",
          "둘째는 어텐션을 쓰는 세 자리, 셋째는 FFN 이에요.",
          f"{MHA} 의 한 줄 요약은 이거예요. 차원을 키우는 게 아니라 512 칸을 8 조각으로 나눠요.",
          f"{FFN} 은 자리마다 똑같이 도는 아주 작은 2층 신경망이에요."),
      analogy("한 장면을 여러 사람이 다른 눈으로 보기",
              "같은 경기를 보면서 한 명은 공만, 한 명은 수비수만, 한 명은 심판만 봐요. 각자 본 것을 합치면 경기 전체가 보여요.",
              ("각자 맡은 눈", HEAD),
              ("각자가 보는 좁은 시야", RSUB),
              ("여덟 명이 동시에 본다", MHA),
              ("본 것을 합치는 회의", "Concat 한 뒤 W^O 곱하기")),
      points("이 쪽의 부품 셋",
             f"{MHA}: h = 8, 헤드마다 d_k = d_v = 64",
             f"어텐션의 세 자리 가운데 하나가 {CA} 이에요",
             f"나머지 둘은 {ENC} 와 {DEC} 안의 {SA} 이에요",
             f"{FFN}: 식 (2), d_model 512 에서 2048 로 늘렸다가 다시 512 로")],
     [points("3.2.2 의 영어와 우리말 뜻",
             '"**linearly project ... h times with different, learned linear projections**" = 서로 다른 학습된 선형 변환으로 h 번 투영한다',
             '"**perform the attention function in parallel**" = 어텐션을 나란히 동시에 돌린다',
             '"**concatenated and once again projected**" = 이어 붙인 뒤 한 번 더 투영한다',
             f'"**different representation subspaces**" = 서로 다른 {RSUB}',
             '"**With a single attention head, averaging inhibits this**" = 헤드가 하나면 평균이 이것을 방해한다',
             '"**the total computational cost is similar**" = 전체 계산 비용은 비슷하다'),
      points("3.2.3 과 3.3, 3.4 의 영어와 우리말 뜻",
             '"**encoder-decoder attention**" = 인코더와 디코더를 잇는 어텐션, 곧 크로스 어텐션',
             '"**the memory keys and values come from the output of the encoder**" = 키와 밸류는 인코더 출력에서 온다',
             '"**prevent leftward information flow**" = 왼쪽으로 정보가 새는 것을 막는다',
             f'"**to preserve the auto-regressive property**" = {AR} 성질을 지키려고',
             '"**applied to each position separately and identically**" = 자리마다 따로, 그러나 똑같이 적용한다',
             '"**two convolutions with kernel size 1**" = 커널 크기 1 짜리 합성곱 둘이라고 볼 수도 있다',
             '"**we share the same weight matrix**" = 같은 가중치 행렬을 함께 쓴다'),
      compare("어텐션을 쓰는 세 자리 (논문 3.2.3)",
              ["자리", QRY, f"{KEY} 와 {VAL}", "미래를 보나"],
              [f"{CA}", DEC, ENC, "막지 않아요"],
              [f"{ENC} 의 {SA}", "앞 층 출력", "앞 층 출력", "앞뒤 다 봐요"],
              [f"{DEC} 의 {SA}", "앞 층 출력", "앞 층 출력", f"{CM} 으로 막아요"]),
      steps("멀티 헤드의 순서 다섯 걸음",
            [f"1. {QRY}, {KEY}, {VAL} 를 헤드마다 다른 행렬로 곱해 64칸으로 줄여요",
             f"2. 헤드 8개가 각자 {SDP} 을 나란히 계산해요. {PAR} 가 되는 대목이에요",
             f"3. 헤드 안에서는 {AW} 를 만들고 그 가중치로 {WSUM} 을 해요",
             "4. 결과 8개(각 64칸)를 옆으로 이어 붙이면 512칸이 돼요",
             "5. 마지막에 W^O 를 한 번 곱해 512칸으로 내보내요"],
            "나누고, 각자 보고, 이어 붙이고, 한 번 섞어요."),
      check("멀티 헤드 어텐션에서 헤드 8개를 쓰면 전체 차원은?",
            ["512 그대로예요", "512 x 8 = 4096 이에요", "64 로 줄어요", "정해지지 않아요"], 0,
            f"{HEAD} 하나가 64칸이고 8개를 이어 붙이면 다시 512칸이에요. 키우는 게 아니라 나누는 거예요.")],
     [look("3.2.2 의 나머지를 짚어 읽어요",
           (0.17, 0.095, 0.66, 0.03, "첫 두 줄. 헤드들의 결과를 이어 붙이고 한 번 더 투영한다는 설명이에요."),
           (0.17, 0.127, 0.66, 0.032, "멀티 헤드를 쓰는 이유 문단. 서로 다른 표현 부분공간을 동시에 본다."),
           (0.29, 0.182, 0.44, 0.042, "MultiHead 식과 head_i 식이에요. 번호는 없지만 시험에 나올 수 있어요."),
           (0.17, 0.258, 0.66, 0.032, "투영 행렬들의 크기를 적은 줄. W^O 만 (h x d_v) x d_model 이에요."),
           (0.17, 0.296, 0.66, 0.04, "h = 8, d_k = d_v = 512 / 8 = 64 라고 못박은 문단이에요."),
           (0.17, 0.354, 0.36, 0.025, "3.2.3 Applications of Attention in our Model 제목이에요.")),
      look("3.2.3, 3.3, 3.4 를 짚어 읽어요",
           (0.21, 0.402, 0.62, 0.072, "첫 점. 쿼리는 디코더, 키와 밸류는 인코더에서 온다는 크로스 어텐션이에요."),
           (0.21, 0.488, 0.62, 0.05, "둘째 점. 인코더의 셀프 어텐션. 셋 다 앞 층 출력 한 곳에서 나와요."),
           (0.21, 0.54, 0.62, 0.071, "셋째 점. 디코더 셀프 어텐션. 마스킹으로 왼쪽 정보 흐름을 막아요."),
           (0.17, 0.632, 0.36, 0.025, "3.3 Position-wise Feed-Forward Networks 제목이에요."),
           (0.35, 0.715, 0.30, 0.03, "식 (2) FFN(x) = max(0, x W1 + b1) W2 + b2 예요."),
           (0.17, 0.813, 0.30, 0.026, "3.4 Embeddings and Softmax 제목이에요.")),
      formula("멀티 헤드 어텐션의 두 줄",
              r"\mathrm{MultiHead}(Q,K,V) = \mathrm{Concat}(\mathrm{head}_1,\dots,\mathrm{head}_h)W^{O},\quad "
              r"\mathrm{head}_i = \mathrm{Attention}(QW^{Q}_i,\, KW^{K}_i,\, VW^{V}_i)",
              [(r"h", f"{HEAD} 의 개수. 논문은 8 을 썼어요"),
               (r"W^{Q}_i, W^{K}_i", "i 번째 헤드용 투영 행렬. 크기는 512 x 64"),
               (r"W^{V}_i", "밸류용 투영 행렬. 크기는 512 x 64"),
               (r"\mathrm{Concat}", "헤드 8개의 결과를 옆으로 이어 붙이기"),
               (r"W^{O}", "이어 붙인 512칸을 다시 512칸으로 섞는 행렬")],
              f"헤드마다 따로 {SDP} 으로 {WSUM} 을 구한 뒤, 합쳐서 한 번 더 섞어요."),
      formula("식 (2) 위치별 피드포워드 신경망",
              r"\mathrm{FFN}(x) = \max(0,\, xW_1 + b_1)W_2 + b_2",
              [(r"x", "한 자리의 512칸짜리 벡터 하나"),
               (r"W_1, b_1", "512 를 2048 로 늘리는 행렬과 편향 항"),
               (r"\max(0,\cdot)", f"{RELU}. 음수는 0, 양수는 그대로"),
               (r"W_2, b_2", "2048 을 다시 512 로 줄이는 행렬과 편향 항")],
              f"자리마다 따로 돌지만 가중치는 같아요. 다만 층이 바뀌면 가중치도 바뀌어요."),
      steps("파라미터 수를 직접 세어 봐요 (논문이 적지 않은 값)",
            [f"1. 헤드 하나의 W^Q 는 512 x 64 = 32,768 개예요",
             "2. 헤드 하나에 Q, K, V 셋이니 3 x 32,768 = 98,304 개예요",
             "3. 헤드가 8개니 8 x 98,304 = 786,432 개, 곧 3 x 512 x 512 예요",
             "4. W^O 는 512 x 512 = 262,144 개예요",
             f"5. {MHA} {SUB} 합계는 786,432 + 262,144 = 1,048,576 개, 곧 4 x 512 x 512 예요",
             "6. FFN 은 512 x 2048 = 1,048,576 에 2048 x 512 = 1,048,576 을 더해 2,097,152 개예요"],
            f"{MHA} 는 약 1.05M, FFN 은 약 2.10M 이에요. FFN 이 정확히 두 배나 무거워요.",
            "d_model = 512, h = 8, d_ff = 2048"),
      steps("스택 전체 파라미터를 어림해 봐요",
            [f"1. {ENC} 한 층 = 1,048,576 + 2,097,152 = 3,145,728 개예요",
             "2. 6층이면 18,874,368 개예요",
             f"3. {DEC} 한 층은 {MHA} 가 둘이라 2 x 1,048,576 + 2,097,152 = 4,194,304 개예요",
             "4. 6층이면 25,165,824 개예요",
             "5. 공유 임베딩은 37,000 x 512 = 18,944,000 개예요",
             "6. 다 더하면 62,984,192 개, 약 62.98M 이에요",
             f"7. {LN} 의 감마와 베타, 그리고 편향 항은 빼고 센 값이에요"],
            "논문 Table 3 의 65 x 10^6 과 비슷하지만 딱 맞지는 않아요. 어림이라서 그래요.",
            "인코더 6층, 디코더 6층, 공유 어휘 37,000"),
      compare("논문과 4주차 강의 슬라이드가 다른 점",
              ["무엇", "논문 (NP p.5)", "4주차 슬라이드 (N4)"],
              ["d_ff", "d_ff = 2048 이라고 값을 못박아요", "p.42 는 d_ff is usually 4d 라고 비율로 말해요"],
              [f"{MHA} 이유", f"{RSUB} 을 동시에 본다고만 적어요", "p.46-48 은 헤드가 실제로 무엇을 배우는지까지 말해요"],
              ["헤드가 배우는 것", "부록의 그림 몇 장이 전부예요", "p.48 의 BERT 연구 이야기는 논문 밖이에요"],
              [f"{CA} 이름", "encoder-decoder attention", "p.53 은 크로스 어텐션이라고 불러요"]),
      bg("기초 다지기 3단원 행렬과 행렬 곱, shape",
         "512칸 벡터에 512 x 64 행렬을 곱하면 64칸 벡터가 나와요. 이게 헤드로 줄이는 계산이에요.",
         "64칸짜리 8개를 옆으로 이어 붙이면 64 x 8 = 512칸이에요. 원래 크기로 돌아와요.",
         f"{RES} 로 더하려면 들어온 것과 나가는 것이 둘 다 512칸이어야 해요."),
      prof("교수님: 헤드를 여러 개 쓴다고 전체 차원을 키우는 게 아니에요.",
           "교수님: 전체 차원을 h 로 나눠서 서로 다른 관점에서 보는 거예요.",
           "교수님: 계산 수는 똑같아요."),
      figure("512 칸을 8 조각으로", FIG_MH, "나누고, 각자 보고, 다시 붙여요.", 4)],
     [check("논문이 FFN 을 달리 표현한 말은?",
            ["커널 크기 1 인 합성곱 둘", "어텐션 하나", "잔차 연결 둘", "층 정규화 둘"], 0,
            "two convolutions with kernel size 1 이라고 적었어요. 자리끼리 섞지 않는다는 뜻이에요."),
      check("논문 3.4 가 같은 가중치 행렬을 함께 쓴다고 적은 셋은?",
            ["입력 임베딩, 출력 임베딩, 소프트맥스 앞 선형 변환",
             "W^Q, W^K, W^V", "인코더, 디코더, FFN", "세 가지 어텐션"], 0,
            f"{EMB} 표 하나를 세 군데가 나눠 써요. 임베딩 층에서는 여기에 루트 d_model 을 곱해요."),
      english("시험 답안 문장",
              "멀티 헤드 어텐션은 d_model 을 h 개로 나눠 헤드마다 d_model/h 차원에서 어텐션을 따로 계산한 뒤 이어 붙이고 W^O 로 한 번 더 투영한다.",
              "나눈다, 따로 계산한다, 이어 붙인다, 다시 섞는다. 네 마디예요.",
              "512 / 8 = 64 라는 숫자를 꼭 같이 써 주세요."),
      warn("헷갈리기 쉬운 점",
           f"{HEAD} 를 늘려도 전체 계산량은 거의 그대로예요. 차원을 나누기 때문이에요.",
           f"{FFN} 은 자리끼리 섞지 않아요. 섞는 일은 {ATT} 만 해요.",
           f"식 (2) 의 max(0, ...) 는 {RELU} 예요. 다른 활성화 함수가 아니에요.",
           f"{CM} 은 {AR} 성질을 지키려고 쓰는 것이지 속도 때문이 아니에요.",
           "우리가 센 62.98M 은 논문의 65 x 10^6 과 달라요. 어림이라고 꼭 밝히세요."),
      exam("예상 문제",
           "h = 8, d_model = 512 일 때 멀티 헤드 어텐션 한 하위층의 파라미터 수를 구하고, 같은 층의 FFN 과 비교하시오.",
           "행렬 크기를 곱해서 개수를 세는 계산 문제예요.",
           ["1. 헤드 하나의 d_k = d_v = 512 / 8 = 64 예요",
            "2. W^Q, W^K, W^V 를 다 합치면 3 x 512 x 512 = 786,432 개예요",
            "3. W^O 는 512 x 512 = 262,144 개예요",
            "4. 합이 4 x 512 x 512 = 1,048,576 개예요",
            "5. FFN 은 2 x 512 x 2048 = 2,097,152 개예요",
            "6. FFN 이 멀티 헤드의 정확히 두 배예요"],
           "멀티 헤드 약 1.05M, FFN 약 2.10M 으로 FFN 이 두 배예요. 편향 항은 뺀 값이에요.")])

# ---------------------------------------------------------------- p.6
page(6, "Table 1 층 종류별 비용과 3.5 위치 인코딩",
     ["Self-Attention", "Recurrent Neural Network (RNN)", "Convolutional Neural Network (CNN)",
      "Restricted Self-Attention", "Maximum Path Length", "Sequential Operations", "Quadratic Cost",
      "Parallelization", "Positional Encoding", "Sinusoidal Positional Encoding", "Embedding",
      "Permutation Equivariance", "RoPE", "Token", "Parameter", "Encoder", "Decoder", "Attention",
      "Transformer"],
     [say(f"이 쪽 위쪽에 Table 1 이 있어요. {SA} 이 {RNN} 보다 왜 나은지 한 표로 보여 줘요.",
          f"{CNN} 과도 비교해요. 잣대는 세 가지예요.",
          f"층당 비용, {SEQOP}, 그리고 {MPL} 이에요.",
          f"아래쪽 3.5 는 {PE} 이에요. 순서를 모르는 모델에 순서를 넣어 주는 부품이에요.",
          f"논문은 sin 과 cos 파도로 위치를 만들었어요. 이름이 {SPE} 이에요."),
      analogy("아파트 층 사이를 오가는 방법",
              "계단은 한 층씩 올라가야 하고, 엘리베이터는 몇 층이든 한 번에 가요. 대신 엘리베이터는 건물이 커질수록 설치비가 훅 뛰어요.",
              ("한 층씩 계단", RNN),
              ("한 번에 가는 엘리베이터", SA),
              ("몇 걸음 걸리나", MPL),
              ("커질수록 뛰는 설치비", QC)),
      points("이 쪽에서 챙길 것",
             f"Table 1 의 세 칸: 층당 비용, {SEQOP}, {MPL}",
             f"{SA} 만 {SEQOP} 와 {MPL} 이 둘 다 O(1) 이에요",
             f"{SPE} 의 두 식과 그 값",
             f"논문은 {PEQ} 이라는 이름을 쓰지 않아요")],
     [points("Table 1 의 영어와 우리말 뜻",
             f'"**Complexity per Layer**" = 층 하나를 지나는 데 드는 계산량',
             f'"**Sequential Operations**" = {SEQOP}, 줄 서서 해야 하는 계산의 수',
             f'"**Maximum Path Length**" = {MPL}, 두 자리를 잇는 가장 먼 걸음 수',
             '"**n is the sequence length**" = n 은 시퀀스 길이(토큰 개수)',
             '"**d is the representation dimension**" = d 는 표현 차원, 곧 512',
             '"**r the size of the neighborhood**" = r 은 이웃 크기, 몇 칸까지 볼지'),
      points("3.5 의 영어와 우리말 뜻",
             '"**in order for the model to make use of the order of the sequence**" = 모델이 순서를 쓸 수 있게 하려고',
             '"**inject some information about the relative or absolute position**" = 상대 또는 절대 위치 정보를 넣어 준다',
             '"**at the bottoms of the encoder and decoder stacks**" = 인코더와 디코더 더미의 맨 아래에서',
             '"**sine and cosine functions of different frequencies**" = 주파수가 다른 sin 과 cos 함수들',
             '"**wavelengths form a geometric progression**" = 파장이 등비수열을 이룬다',
             '"**extrapolate to sequence lengths longer**" = 학습 때보다 긴 문장으로 뻗어 나간다'),
      compare("Table 1 을 우리말로 옮기면",
              ["층 종류", "층당 비용", SEQOP, MPL],
              [SA, "O(n^2 x d)", "O(1)", "O(1)"],
              ["Recurrent", "O(n x d^2)", "O(n)", "O(n)"],
              ["Convolutional", "O(k x n x d^2)", "O(1)", "O(log_k(n))"],
              [f"{SA} (restricted)", "O(r x n x d)", "O(1)", "O(n/r)"]),
      steps("3.5 를 순서대로 읽어요",
            [f"1. 우리 모델에는 순환도 합성곱도 없어요. 그래서 순서를 몰라요",
             f"2. 그러니 위치 정보를 {EMB} 에 더해 넣어야 해요",
             f"3. 위치 벡터는 {EMB} 과 칸 수가 같아야 더할 수 있어요. 둘 다 512칸이에요",
             "4. 방법은 여러 가지인데 우리는 sin 과 cos 을 골랐어요",
             "5. 학습해서 만드는 위치 임베딩도 해 봤는데 결과가 거의 같았어요 (Table 3 의 (E))"],
            f"순서가 없으니 넣어 준다, 더할 수 있게 칸 수를 맞춘다. 이 두 줄이 3.5 의 뼈대예요."),
      check("Table 1 에서 셀프 어텐션만 가진 장점은?",
            [f"{SEQOP} 와 {MPL} 이 둘 다 O(1)",
             "층당 비용이 가장 싸다", "파라미터가 가장 적다", "메모리를 가장 적게 쓴다"], 0,
            f"두 칸이 모두 O(1) 인 줄은 {SA} 뿐이에요. 대신 층당 비용은 n 제곱이에요.")],
     [look("Table 1 을 짚어 봐요",
           (0.17, 0.088, 0.66, 0.055, "Table 1 캡션. n 은 길이, d 는 차원, k 는 커널 크기, r 은 이웃 크기예요."),
           (0.19, 0.143, 0.61, 0.032, "표 머리글. 층 종류, 층당 복잡도, 순차 연산 수, 최대 경로 길이예요."),
           (0.19, 0.176, 0.61, 0.014, "Self-Attention 줄. O(n^2 x d), O(1), O(1) 이에요."),
           (0.19, 0.191, 0.61, 0.014, "Recurrent 줄. O(n x d^2), O(n), O(n) 이에요."),
           (0.19, 0.206, 0.61, 0.014, "Convolutional 줄. O(k x n x d^2), O(1), O(log_k(n)) 이에요."),
           (0.19, 0.221, 0.61, 0.015, "Self-Attention (restricted) 줄. O(r x n x d), O(1), O(n/r) 이에요.")),
      look("3.5 위치 인코딩을 짚어 읽어요",
           (0.17, 0.27, 0.30, 0.025, "3.5 Positional Encoding 제목이에요."),
           (0.17, 0.296, 0.66, 0.078, "순환도 합성곱도 없으니 순서 정보를 넣어 줘야 한다는 문단이에요."),
           (0.36, 0.425, 0.28, 0.045, "사인 코사인 위치 인코딩 식 두 줄이에요. 짝수 칸은 sin, 홀수 칸은 cos."),
           (0.17, 0.478, 0.66, 0.066, "파장이 2 pi 에서 10000 x 2 pi 까지 등비로 늘어난다고 적은 문단이에요."),
           (0.17, 0.552, 0.66, 0.058, "학습 위치 임베딩과 거의 같았고, 외삽을 기대해 사인 코사인을 골랐다는 문단."),
           (0.17, 0.63, 0.30, 0.025, "4 Why Self-Attention 제목이에요.")),
      formula("사인 코사인 위치 인코딩의 두 식",
              r"PE_{(pos,\,2i)} = \sin\!\left(\frac{pos}{10000^{2i/d_{model}}}\right),\quad "
              r"PE_{(pos,\,2i+1)} = \cos\!\left(\frac{pos}{10000^{2i/d_{model}}}\right)",
              [(r"pos", f"몇 번째 자리인지. 첫 {TOK} 이 0 이에요"),
               (r"i", "칸 번호의 절반. 0, 1, 2, ... 로 올라가요"),
               (r"2i", "짝수 번째 칸에는 sin 을 넣어요"),
               (r"2i+1", "홀수 번째 칸에는 cos 을 넣어요"),
               (r"10000^{2i/d_{model}}", "뒤 칸으로 갈수록 커지는 나눗수. 그래서 파도가 느려져요"),
               (r"d_{model}", "512. 위치 벡터도 512칸이라 임베딩에 그냥 더할 수 있어요")],
              f"학습하는 값이 하나도 없어요. 계산만 하면 나오는 고정 표예요."),
      steps("장난감 예로 손계산 (d_model = 4 로 줄여서)",
            ["1. d_model = 4 면 i 는 0 과 1 두 개예요",
             "2. i = 0 이면 나눗수가 10000^0 = 1 이라 그냥 sin(pos), cos(pos) 예요",
             "3. i = 1 이면 나눗수가 10000^(2/4) = 100 이라 sin(pos/100), cos(pos/100) 이에요",
             "4. pos = 0: sin 0 = 0, cos 0 = 1 이니 (0.0, 1.0, 0.0, 1.0) 이에요",
             "5. pos = 1: (0.8415, 0.5403, 0.0100, 1.0) 이에요",
             "6. pos = 2: (0.9093, -0.4161, 0.0200, 0.9998) 이에요",
             "7. pos = 3: (0.1411, -0.9900, 0.0300, 0.9996) 이에요"],
            "앞 두 칸은 빠르게 흔들리고 뒤 두 칸은 아주 천천히 변해요. 그래서 가까운 자리끼리 비슷해요.",
            "d_model = 4, pos = 0, 1, 2, 3"),
      steps("Table 1 의 갈림길을 숫자로 확인 (d = 512)",
            [f"1. {SA} 은 n^2 x d, {RNN} 은 n x d^2 예요",
             "2. n = 100 이면 100 x 100 x 512 = 5,120,000 대 100 x 512 x 512 = 26,214,400 이에요",
             "3. 셀프 어텐션이 약 5.12배 싸요",
             "4. n = 512 면 둘 다 134,217,728 로 똑같아요. 여기가 갈림길이에요",
             "5. n = 1000 이면 512,000,000 대 262,144,000 이라 셀프 어텐션이 약 1.95배 비싸요",
             "6. 논문 문장 그대로 n 이 d 보다 작을 때만 셀프 어텐션이 빨라요"],
            f"갈림길은 n = d 예요. 논문은 문장이 보통 512 토큰보다 짧으니 괜찮다고 봤어요.",
            "d = 512, n = 100 / 512 / 1000"),
      compare("논문과 4주차 강의 슬라이드가 다른 점",
              ["무엇", "논문 (NP p.6)", "4주차 슬라이드 (N4)"],
              ["순서 문제의 이름", "이름을 붙이지 않아요", f"p.39 는 {PEQ} 이라고 불러요"],
              ["위치 방식 종류", f"{SPE} 과 학습 임베딩 둘만 비교", f"p.41 은 {ROPE} 까지 소개해요"],
              [ROPE, "논문에 아예 없어요", "p.41 은 요즘 LLM 이 거의 다 쓴다고 해요"],
              [QC, "4장에서 장점 설명의 일부로만 다뤄요", "p.55 는 The Price 라고 크게 다뤄요"]),
      bg("기초 다지기 4단원 로그와 지수",
         "10000^(2i/512) 는 i 가 커질수록 빠르게 커지는 지수예요. i = 0 이면 1, i = 255 면 약 9646.6 이에요.",
         "나눗수가 커지면 sin 안의 값이 작아져서 파도가 아주 천천히 흔들려요.",
         "Table 1 의 log_k(n) 도 로그예요. k 칸씩 묶어 올라가면 n 을 덮는 데 log_k(n) 층이 필요해요."),
      prof("교수님: 인베딩의 위치를 모르기 때문에 포지셔널 인코딩을 더해 주는 거예요.",
           "교수님: 이 배리어 3개를 기억해 봅시다.",
           "교수님: 병렬로 빨라지는 대신 메모리가 n 제곱이에요. 이 세상에 데스 노 프리 런치예요.")],
     [check("논문이 사인 코사인을 고른 이유로 적은 것은?",
            ["학습 때보다 긴 문장으로 뻗어 나갈 수 있을지도 몰라서",
             "성능이 확실히 더 좋아서", "파라미터가 필요해서", "계산이 더 느려서"], 0,
            "it may allow the model to extrapolate 라고 적었어요. may 라서 논문도 단정하지 않았어요."),
      check("Table 1 에서 셀프 어텐션의 층당 비용은?",
            ["O(n^2 x d)", "O(n x d^2)", "O(k x n x d^2)", "O(r x n x d)"], 0,
            f"길이 n 이 두 배면 비용이 네 배예요. 이것을 {QC} 이라고 불러요."),
      english("시험 답안 문장",
              "셀프 어텐션은 순차 연산 수와 최대 경로 길이가 모두 O(1) 이라 병렬화와 장거리 의존 학습에 유리하지만, 층당 비용이 O(n 제곱 x d) 로 길이에 민감하다.",
              "장점 두 개와 대가 하나를 한 문장에 담아요.",
              "O(1), O(1), 그리고 n 제곱. 세 숫자로 외워요."),
      warn("헷갈리기 쉬운 점",
           "논문은 we hypothesized, may allow 라고 적었어요. 사인 코사인의 장점은 증명이 아니라 추측이에요.",
           "파장이 2 pi 에서 10000 x 2 pi 라는 말은 어림이에요. 마지막 짝은 10000^(510/512) = 9646.6 배예요.",
           f"{PEQ} 과 {ROPE} 는 강의 슬라이드의 말이에요. 논문에는 없어요.",
           f"{RSA} 은 Table 1 에 줄만 있고 실제 실험은 안 했어요. 논문은 future work 라고 적었어요."),
      exam("예상 문제",
           "트랜스포머에 위치 인코딩이 필요한 이유와, 논문이 쓴 사인 코사인 방식을 설명하시오.",
           "왜 필요한지와 어떻게 만드는지를 쓰는 문제예요.",
           [f"1. 순환도 합성곱도 없어서 {ATT} 자체는 자리 순서를 전혀 몰라요",
            f"2. 그래서 자리마다 다른 벡터를 만들어 {EMB} 에 더해요",
            "3. 짝수 칸은 sin(pos / 10000^(2i/d_model)), 홀수 칸은 같은 값의 cos 이에요",
            "4. 위치 벡터도 512칸이라 임베딩에 그대로 더할 수 있어요",
            "5. 학습 파라미터가 0 개이고, 학습 때보다 긴 문장에도 값을 계산할 수 있어요"],
           "순서 정보가 없어서 넣어 주는 것이고, 주파수가 다른 sin 과 cos 으로 만들어 임베딩에 더해요.")])

# ---------------------------------------------------------------- p.7
page(7, "4장 마무리와 5 Training 설정 (식 3)",
     ["Self-Attention", "Restricted Self-Attention", "Convolutional Neural Network (CNN)",
      "Recurrent Neural Network (RNN)", "Maximum Path Length", "Interpretability", "Head",
      "Attention Weight", "Byte Pair Encoding (BPE)", "WordPiece", "Vocabulary", "Token",
      "Machine Translation (MT)", "Adam", "Warmup", "Learning Rate", "Gradient", "Parameter",
      "Position-wise Feed-Forward Network (FFN)", "Quadratic Cost", "Dropout"],
     [say("이 쪽은 두 토막이에요. 위쪽은 4장 마무리, 아래쪽은 5장 학습 설정이에요.",
          f"4장 마무리는 {CNN} 과 비교하고, {INTP} 이라는 덤을 말해요.",
          "5장은 실제로 어떤 데이터로 어떤 기계에서 얼마나 오래 돌렸는지를 적어요.",
          f"그리고 식 (3), 곧 {LR} 을 스텝마다 바꾸는 공식이 나와요."),
      analogy("요리 레시피의 뒷장",
              "앞장은 무슨 요리인지 설명하고, 뒷장은 오븐 온도와 굽는 시간을 정확히 적어요. 5장이 그 뒷장이에요.",
              ("재료", "WMT 2014 데이터"),
              ("오븐", "P100 GPU 8장"),
              ("굽는 시간", "base 12시간, big 3.5일"),
              ("불 조절", f"식 (3) 의 {LR}")),
      points("이 쪽에서 챙길 것",
             f"n 이 d 보다 작을 때만 {SA} 이 더 빠르다는 조건",
             f"{RSA} 은 아이디어만 적고 실험은 안 했어요",
             "데이터 숫자: 450만 문장 쌍, 어휘 약 37,000, 배치 약 25,000 토큰",
             f"식 (3) 과 warmup_steps = 4000")],
     [points("4장 마무리의 영어와 우리말 뜻",
             '"**when the sequence length n is smaller than the representation dimensionality d**" = 길이 n 이 차원 d 보다 작을 때',
             '"**restricted to considering only a neighborhood of size r**" = 이웃 r 칸만 보게 제한한다',
             '"**We plan to investigate this approach further in future work**" = 이건 앞으로 해 보겠다는 말이에요',
             '"**Separable convolutions ... decrease the complexity considerably**" = 분리 합성곱은 비용을 꽤 낮춘다',
             '"**self-attention could yield more interpretable models**" = 더 들여다보기 쉬운 모델이 될 수도 있다'),
      points("5장의 영어와 우리말 뜻",
             '"**about 4.5 million sentence pairs**" = 문장 쌍 약 450만 개',
             '"**shared source-target vocabulary of about 37000 tokens**" = 원문과 번역문이 함께 쓰는 어휘 약 37,000개',
             '"**batched together by approximate sequence length**" = 길이가 비슷한 문장끼리 묶어서 배치를 만든다',
             '"**one machine with 8 NVIDIA P100 GPUs**" = P100 8장이 달린 기계 한 대',
             '"**increasing the learning rate linearly for the first warmup_steps**" = 처음 warmup 구간은 직선으로 올린다',
             '"**inverse square root of the step number**" = 스텝 수의 역제곱근에 비례해 내린다'),
      compare("두 번역 과제의 데이터 설정 (논문 5.1)",
              ["", "영어-독일어", "영어-프랑스어"],
              ["문장 수", "약 450만 쌍", "3600만 문장"],
              ["토큰화", BPE, WP],
              [VOC, "약 37,000 (공유)", "32,000"],
              ["배치", "원문 약 25,000 토큰", "번역문 약 25,000 토큰"]),
      steps("학습 설정을 순서대로",
            [f"1. 데이터를 {BPE} 나 {WP} 로 잘라 {TOK} 으로 바꿔요",
             "2. 길이가 비슷한 문장끼리 묶어 배치를 만들어요",
             "3. P100 8장이 달린 기계 한 대에 올려요",
             f"4. {ADAM} 으로 학습해요. beta1 0.9, beta2 0.98, epsilon 10^-9 이에요",
             f"5. {LR} 은 고정이 아니라 식 (3) 으로 스텝마다 바꿔요",
             "6. base 는 10만 스텝 12시간, big 은 30만 스텝 3.5일이에요"],
            f"데이터, 배치, 기계, 옵티마이저, {LR}, 스텝 수. 이 여섯 가지가 5장의 전부예요."),
      check("논문이 warmup_steps 로 쓴 값은?",
            ["4000", "400", "40000", "100000"], 0,
            f"{WARM} 4000 스텝까지는 {LR} 을 직선으로 올리고, 그 뒤로는 역제곱근으로 내려요.")],
     [look("4장 마무리와 5.1 을 짚어 읽어요",
           (0.17, 0.092, 0.66, 0.08, "n 이 d 보다 작으면 셀프 어텐션이 빠르다, 그리고 제한된 셀프 어텐션 이야기예요."),
           (0.17, 0.184, 0.66, 0.105, "합성곱 이야기. 커널 k 가 n 보다 작으면 한 층으로 모든 쌍을 못 이어요."),
           (0.17, 0.302, 0.66, 0.052, "해석 가능성 이야기. 헤드마다 다른 일을 배우는 것 같다고 적었어요."),
           (0.17, 0.381, 0.17, 0.025, "5 Training 제목이에요."),
           (0.17, 0.447, 0.33, 0.025, "5.1 Training Data and Batching 제목이에요."),
           (0.17, 0.474, 0.66, 0.095, "데이터 문단. 450만 문장 쌍, 어휘 약 37,000, 배치 약 25,000 토큰이에요.")),
      look("5.2 와 5.3 을 짚어 읽어요",
           (0.17, 0.594, 0.30, 0.025, "5.2 Hardware and Schedule 제목이에요."),
           (0.17, 0.624, 0.66, 0.07, "P100 8장, base 는 0.4초 x 10만 스텝 12시간, big 은 1.0초 x 30만 스텝 3.5일."),
           (0.17, 0.703, 0.17, 0.025, "5.3 Optimizer 제목이에요."),
           (0.17, 0.729, 0.66, 0.04, "Adam 의 beta1 0.9, beta2 0.98, epsilon 10^-9 을 적은 줄이에요."),
           (0.26, 0.785, 0.48, 0.03, "식 (3) 학습률 공식이에요. 두 항 중 작은 쪽을 골라요."),
           (0.17, 0.815, 0.66, 0.06, "warmup_steps = 4000. 처음엔 올리고 뒤엔 역제곱근으로 내려요.")),
      formula("식 (3) 학습률 스케줄",
              r"lrate = d_{model}^{-0.5} \cdot \min\!\left(step\_num^{-0.5},\ step\_num \cdot warmup\_steps^{-1.5}\right)",
              [(r"d_{model}^{-0.5}", "512 의 역제곱근. 0.044194 라는 고정 배율이에요"),
               (r"step\_num", "지금이 몇 번째 학습 스텝인지"),
               (r"step\_num^{-0.5}", "스텝이 커질수록 작아지는 항. 내려가는 쪽이에요"),
               (r"step\_num \cdot warmup\_steps^{-1.5}", "스텝에 비례해 커지는 항. 올라가는 쪽이에요"),
               (r"\min", "둘 중 작은 쪽을 골라요. 그래서 산 모양이 돼요"),
               (r"warmup\_steps", f"{WARM} 구간 길이. 논문은 4000 을 썼어요")],
              f"4000 스텝에서 두 항이 같아져요. 거기가 {LR} 의 꼭대기예요."),
      steps("식 (3) 을 스텝마다 계산해 봐요",
            ["1. 512^(-0.5) = 0.044194 예요. 이 값은 끝까지 안 바뀌어요",
             "2. step 1000: 올라가는 항이 1000 x 4000^(-1.5) = 0.003953 으로 더 작아요. lrate = 0.000175",
             "3. step 2000: lrate = 0.000349 예요. 1000 일 때의 딱 두 배예요",
             "4. step 4000: 두 항이 4000^(-0.5) = 0.015811 로 같아져요. lrate = 0.000699 로 최고점이에요",
             "5. step 8000: 내려가는 항만 남아요. lrate = 0.000494 예요",
             "6. step 16000: lrate = 0.000349 예요. 4000 일 때의 절반이에요",
             "7. step 100000: lrate = 0.000140 까지 내려와요"],
            "스텝이 4배가 되면 학습률은 절반이 돼요. 역제곱근이라서 그래요.",
            "d_model = 512, warmup_steps = 4000"),
      steps("5.2 의 학습 시간을 검산해 봐요",
            ["1. base 는 한 스텝 0.4초, 10만 스텝이에요",
             "2. 100,000 x 0.4 = 40,000초예요",
             "3. 40,000 / 3600 = 11.1시간인데 논문은 12시간이라고 적었어요",
             "4. big 은 한 스텝 1.0초, 30만 스텝이에요",
             "5. 300,000초 / 86,400 = 3.47일인데 논문은 3.5일이라고 적었어요",
             "6. 둘 다 논문이 반올림해서 적은 것으로 보여요"],
            "검산 값 11.1시간과 3.47일이에요. 논문의 12시간, 3.5일과 조금 달라요.",
            "base 0.4초 x 100K, big 1.0초 x 300K"),
      compare("논문과 4주차 강의 슬라이드가 다른 점",
              ["무엇", "논문 (NP p.7)", "4주차 슬라이드 (N4)"],
              [QC, "n 이 d 보다 작으면 괜찮다고만 해요", "p.55 는 오늘날 가장 큰 공학 문제라고 해요"],
              [f"{LR} 워밍업", "5.3 에 식으로만 적어요", "p.51 은 Post-LN 이라 워밍업이 꼭 필요하다고 설명해요"],
              [INTP, "could yield 라고 조심스럽게 적어요", "p.48 은 헤드 연구 결과를 구체적으로 말해요"]),
      bg("기초 다지기 8단원 경사 하강법과 손실",
         f"{GRAD} 은 어느 쪽으로 가야 손실이 줄어드는지 알려 주는 방향이에요.",
         f"{LR} 은 한 걸음의 보폭이에요. {GRAD} 에 이 보폭을 곱해서 파라미터를 고쳐요.",
         f"{ADAM} 은 방향과 보폭을 자동으로 조절해 주는 경사 하강법의 한 종류예요.",
         "식 (3) 은 그 위에 다시 보폭을 스텝마다 바꾸는 규칙을 얹은 거예요."),
      prof("교수님: 이 세상에 데스 노 프리 런치, 진짜 그냥 좋은 방향으로만 가는 건 없어요.",
           "교수님: 병렬로 빨라지는 대신 메모리가 n 제곱이에요.",
           "교수님: 패러럴이 핵심이에요. 항상 병렬로 처리하는 파이프라인을 머릿속에 그려 주세요."),
      figure("식 (3) 학습률의 산 모양", FIG_LR, "4000 스텝에서 꼭대기를 찍고 내려와요.", 4)],
     [check("식 (3) 에서 학습률이 가장 높아지는 지점은?",
            ["step_num = warmup_steps = 4000", "step_num = 1", "step_num = 100000", "학습이 끝날 때"], 0,
            "두 항이 같아지는 자리가 꼭대기예요. 그 값은 0.000699 예요."),
      check("논문이 배치를 만드는 방식으로 적은 것은?",
            ["길이가 비슷한 문장끼리 묶었다", "무작위로 묶었다",
             "한 문장씩 넣었다", "언어별로 나눴다"], 0,
            "batched together by approximate sequence length 예요. 빈칸 채우기를 줄이려고 그래요."),
      english("시험 답안 문장",
              "학습률은 warmup_steps 까지 선형으로 올린 뒤 스텝 수의 역제곱근에 비례해 낮추며, 논문은 warmup_steps 를 4000 으로 두었다.",
              "올린다, 내린다, 4000. 세 마디면 충분해요.",
              "산 모양 그래프를 손으로 그려 보면 바로 외워져요."),
      warn("헷갈리기 쉬운 점",
           f"{RSA} 은 Table 1 에만 있고 실제로 돌린 실험이 아니에요. 논문이 future work 라고 적었어요.",
           f"{INTP} 은 could yield, appear to 라고 적었어요. 논문도 단정하지 않은 관찰이에요.",
           "37,000 은 영어-독일어 공유 어휘예요. 영어-프랑스어는 32,000 워드피스예요.",
           f"{LR} 식의 min 은 최솟값을 고르는 것이지 최댓값이 아니에요."),
      exam("예상 문제",
           "논문 식 (3) 의 학습률 스케줄을 쓰고, 왜 이런 모양으로 만들었는지 설명하시오.",
           "식을 쓰고 모양을 설명하는 문제예요.",
           ["1. lrate = d_model^(-0.5) x min(step^(-0.5), step x warmup^(-1.5)) 이에요",
            "2. 처음에는 두 번째 항이 작아서 스텝에 비례해 직선으로 올라가요",
            "3. warmup_steps 를 넘으면 첫 항이 작아져서 역제곱근으로 내려가요",
            "4. 논문은 warmup_steps = 4000 을 썼고 그 지점이 최고점 0.000699 예요",
            f"5. 초반에 {LR} 이 크면 학습이 흔들려서 천천히 올리는 것이에요"],
           "올렸다가 내리는 산 모양이고, 꼭대기가 warmup_steps = 4000 이에요.")])

# ---------------------------------------------------------------- p.8
page(8, "Table 2 BLEU 와 학습 비용, 정칙화, 6.1 번역 결과",
     ["BLEU", "Machine Translation (MT)", "FLOPs", "Ensemble", "Dropout", "Label Smoothing",
      "Perplexity (PPL)", "Beam Search", "Length Normalization", "Checkpoint Averaging",
      "Sub-layer", "Residual Connection", "Embedding", "Positional Encoding", "Transformer",
      "Parameter", "Over-fitting", "Model Variations"],
     [say(f"이 쪽 위에 Table 2 가 있어요. {MT} 성적표이자 영수증이에요.",
          f"왼쪽 두 칸은 {BLEU}, 오른쪽 두 칸은 학습에 든 {FLOPS} 예요.",
          "아래쪽은 정칙화 두 가지와 6.1 번역 결과 이야기예요.",
          "여기서 논문 안이 서로 어긋나는 대목이 딱 하나 나와요. 꼭 짚고 갈게요."),
      analogy("성적표와 영수증을 나란히",
              "같은 점수를 받아도 학원비를 10분의 1만 쓴 쪽이 더 잘한 거예요. Table 2 는 점수와 비용을 나란히 놓은 표예요.",
              ("점수", BLEU),
              ("학원비", FLOPS),
              ("여러 명이 같이 푼 답", ENS),
              ("혼자 푼 답", "트랜스포머 단일 모델")),
      points("이 쪽에서 챙길 것",
             f"Transformer (big) 은 영어-독일어 28.4, 영어-프랑스어 41.8",
             f"학습 비용은 2.3 x 10^19 {FLOPS} 로 경쟁자들보다 훨씬 싸요",
             f"정칙화 둘: {DROP} P_drop = 0.1, {LS} eps_ls = 0.1",
             "본문 6.1 과 Table 2 의 영어-프랑스어 값이 서로 달라요")],
     [points("Table 2 와 6.1 의 영어와 우리말 뜻",
             '"**at a fraction of the training cost**" = 학습 비용의 몇 분의 1 로',
             '"**outperforms the best previously reported models (including ensembles)**" = 앙상블까지 포함해 기존 최고를 이긴다',
             '"**by more than 2.0 BLEU**" = 2.0 BLEU 넘게 앞선다',
             '"**averaging the last 5 checkpoints**" = 마지막 체크포인트 5개를 평균한다',
             '"**beam size of 4 and length penalty alpha = 0.6**" = 빔 크기 4, 길이 페널티 0.6',
             '"**terminate early when possible**" = 가능하면 일찍 끝낸다'),
      points("5.4 정칙화의 영어와 우리말 뜻",
             '"**We employ three types of regularization**" = 정칙화를 세 가지 쓴다',
             '"**dropout to the output of each sub-layer, before it is added**" = 하위층 출력에, 더하기 전에 드롭아웃',
             '"**to the sums of the embeddings and the positional encodings**" = 임베딩과 위치 인코딩을 더한 값에도',
             '"**label smoothing of value eps_ls = 0.1**" = 라벨 스무딩 값 0.1',
             '"**This hurts perplexity ... but improves accuracy and BLEU score**" = 퍼플렉서티는 나빠지지만 정확도와 BLEU 는 좋아진다'),
      compare("Table 2 의 주요 줄만 뽑으면",
              ["모델", "영어-독일어", "영어-프랑스어", "영어-독일어 비용"],
              ["GNMT + RL", "24.6", "39.92", "2.3 x 10^19"],
              ["ConvS2S", "25.16", "40.46", "9.6 x 10^18"],
              [f"ConvS2S {ENS}", "26.36", "41.29", "7.7 x 10^19"],
              ["Transformer (base)", "27.3", "38.1", "3.3 x 10^18"],
              ["Transformer (big)", "28.4", "41.8", "2.3 x 10^19"]),
      steps("추론(번역을 실제로 만들 때) 설정",
            [f"1. base 는 마지막 {CKPT} 5개, big 은 20개를 평균해서 한 모델로 써요",
             "2. 체크포인트는 10분 간격으로 저장했어요",
             f"3. {BEAM} 의 빔 크기는 4 예요",
             f"4. {LNORM} 에 해당하는 length penalty alpha = 0.6 을 썼어요",
             "5. 최대 출력 길이는 입력 길이 + 50 이고, 가능하면 일찍 멈춰요"],
            f"평균 내고, {BEAM} 로 찾고, 길이로 눌러 주기. 이게 추론 설정이에요."),
      check("논문이 말한 라벨 스무딩의 효과는?",
            [f"{PPL} 는 나빠지지만 정확도와 {BLEU} 는 좋아진다",
             "둘 다 좋아진다", "둘 다 나빠진다", f"{PPL} 만 좋아진다"], 0,
            "hurts perplexity ... but improves accuracy and BLEU score 가 논문의 문장이에요.")],
     [look("Table 2 를 짚어 봐요",
           (0.17, 0.086, 0.66, 0.032, "Table 2 캡션. newstest2014 에서 BLEU 와 학습 비용을 비교한 표예요."),
           (0.21, 0.122, 0.58, 0.038, "머리글. 왼쪽이 BLEU, 오른쪽이 학습 비용 FLOPs 예요."),
           (0.21, 0.16, 0.58, 0.072, "단일 모델들. ByteNet 23.75, GNMT+RL 24.6, ConvS2S 25.16, MoE 26.03."),
           (0.21, 0.233, 0.58, 0.042, "앙상블들. 가장 높은 것이 ConvS2S Ensemble 26.36 이에요."),
           (0.21, 0.277, 0.58, 0.014, "Transformer (base model) 줄. 27.3 과 38.1, 비용 3.3 x 10^18."),
           (0.21, 0.292, 0.58, 0.016, "Transformer (big) 줄. 28.4 와 41.8, 비용 2.3 x 10^19.")),
      look("5.4 와 6.1 을 짚어 읽어요",
           (0.17, 0.344, 0.66, 0.055, "Residual Dropout 문단. 하위층 출력과 임베딩 + 위치 인코딩 합에 써요."),
           (0.17, 0.418, 0.66, 0.03, "Label Smoothing 문단. 퍼플렉서티는 나빠지고 BLEU 는 좋아진다고 적었어요."),
           (0.17, 0.468, 0.16, 0.025, "6 Results 제목이에요."),
           (0.17, 0.53, 0.66, 0.078, "영어-독일어 문단. 앙상블까지 이겨서 2.0 BLEU 넘게 앞섰다고 적었어요."),
           (0.17, 0.624, 0.66, 0.05, "영어-프랑스어 문단. 여기서는 41.0 이라고 적었어요. Table 2 와 달라요."),
           (0.17, 0.748, 0.66, 0.058, "FLOPs 를 학습 시간 x GPU 수 x GPU 성능으로 어림했다고 적은 문단이에요.")),
      steps("2.0 BLEU 넘게 앞섰다는 말을 검산",
            [f"1. 기존 최고는 ConvS2S {ENS} 의 26.36 이에요",
             "2. Transformer (big) 은 28.4 예요",
             "3. 28.4 - 26.36 = 2.04 예요",
             "4. 그래서 논문이 by more than 2.0 BLEU 라고 적었어요",
             f"5. base 모델 27.3 도 {ENS} 26.36 보다 높아요"],
            "차이는 2.04 예요. 단일 모델 하나가 앙상블을 이긴 것이라 더 의미가 커요.",
            "ConvS2S Ensemble 26.36, Transformer (big) 28.4"),
      steps("학습 비용 2.3 x 10^19 을 검산해 봐요",
            ["1. 각주 5 는 P100 한 장을 9.5 TFLOPS 로 어림했다고 적었어요",
             "2. big 은 3.5일 동안 GPU 8장을 썼어요",
             "3. 3.5 x 86,400 = 302,400초예요",
             "4. 302,400 x 8 x 9.5 x 10^12 = 2.298 x 10^19 이에요",
             "5. Table 2 의 2.3 x 10^19 과 맞아요",
             "6. base 는 12 x 3600 x 8 x 9.5 x 10^12 = 3.28 x 10^18 이라 3.3 x 10^18 과 맞아요"],
            f"{FLOPS} 는 학습 시간 x GPU 수 x GPU 성능으로 만든 어림값이에요. 계산이 실제로 맞아요.",
            "P100 9.5 TFLOPS, GPU 8장, 3.5일"),
      compare("정칙화 두 가지 (논문 5.4)",
              ["이름", "값", "어디에 거나", "효과"],
              [DROP, "P_drop = 0.1", f"{SUB} 출력, 그리고 임베딩 + 위치 인코딩 합", f"{OVF} 을 막아요"],
              [LS, "eps_ls = 0.1", "정답 라벨", f"{PPL} 는 나빠지고 {BLEU} 는 좋아져요"]),
      bg("기초 다지기 6단원 소프트맥스와 교차 엔트로피",
         f"{LS} 은 정답 확률을 1.0 이 아니라 0.9 쯤으로 두고 나머지를 다른 토큰에 조금씩 나눠 줘요.",
         f"모델이 덜 확신하게 되니 {PPL} 는 나빠져요. 정답 확률을 낮췄으니 당연해요.",
         f"대신 지나친 확신이 줄어서 실제 번역 품질, 곧 {BLEU} 는 좋아졌어요."),
      prof("교수님: 항상 빔 서치가 좋은 건 아니에요.",
           "교수님: 트레이드 오프가 있다는 것 정도는 기억해 달라.",
           "교수님: 이 논문은 읽어서 이해하면 시험도 나중에 잘 볼 수 있어요.")],
     [check("Transformer (base) 의 영어-독일어 학습 비용은?",
            ["3.3 x 10^18", "2.3 x 10^19", "9.6 x 10^18", "1.8 x 10^20"], 0,
            f"Table 2 에서 가장 작은 값이에요. 성적은 27.3 으로 {ENS} 들보다 높아요."),
      english("시험 답안 문장",
              "Transformer (big) 은 영어-독일어 newstest2014 에서 BLEU 28.4 로 기존 앙상블보다 2.0 넘게 앞섰고, 학습 비용은 2.3 x 10의 19제곱 FLOPs 에 그쳤다.",
              "점수와 비용을 한 문장에 같이 써야 논문의 주장이 살아요.",
              "28.4, 2.04 차이, 2.3 x 10^19. 숫자 셋을 외워요."),
      warn("논문 안이 서로 어긋나는 대목",
           "초록과 Table 2 는 영어-프랑스어 big 을 41.8 이라고 적었어요.",
           "그런데 6.1 본문은 achieves a BLEU score of 41.0 이라고 적었어요.",
           "논문 자체가 어긋나 있어요. 시험에는 초록과 Table 2 의 41.8 을 쓰세요.",
           "그리고 영어-프랑스어 big 만 P_drop 을 0.3 대신 0.1 로 썼어요."),
      warn("헷갈리기 쉬운 점",
           f"{FLOPS} 값은 실제로 잰 게 아니라 시간 x GPU 수 x 성능으로 어림한 값이에요.",
           "Table 2 의 비용 칸에서 base 는 영어-독일어 칸만 있고 영어-프랑스어 칸은 비어 있어요.",
           f"{DROP} 은 {RES} 로 더하기 전에 걸려요. {LN} 를 지난 뒤가 아니에요.",
           f"{LNORM} 의 alpha = 0.6 은 값이 클수록 긴 문장을 덜 손해 보게 해요.",
           f"{CKPT} 은 모델 여러 개를 돌리는 {ENS} 과 달라요. 가중치를 평균해 한 모델로 써요."),
      exam("예상 문제",
           "논문이 Table 2 에서 BLEU 와 함께 학습 비용을 나란히 보여 준 이유를 설명하시오.",
           "왜 점수만 안 보여 주고 비용도 같이 보여 줬는지 묻는 문제예요.",
           ["1. 논문의 주장이 더 잘한다 가 아니라 더 잘하면서 더 싸다 이기 때문이에요",
            f"2. Transformer (base) 는 3.3 x 10^18 {FLOPS} 로 {ENS} 들보다 높은 27.3 을 냈어요",
            "3. big 도 2.3 x 10^19 로 GNMT + RL 단일 모델과 같은 비용이에요",
            "4. 순환을 없애 병렬 계산이 되기 때문에 같은 시간에 더 많이 학습할 수 있어요"],
           "품질과 비용을 같이 보여야 어텐션만 쓴 구조의 이점이 드러나기 때문이에요.")])

# ---------------------------------------------------------------- p.9
page(9, "Table 3 모델 변형 실험과 6.3 구문 분석 시작",
     ["Model Variations", "Head", "Multi-Head Attention (MHA)", "Perplexity (PPL)", "BLEU",
      "Parameter", "Dropout", "Label Smoothing", "Over-fitting", "Positional Encoding",
      "Sinusoidal Positional Encoding", "Embedding", "Byte Pair Encoding (BPE)", "WordPiece",
      "Vocabulary", "Constituency Parsing", "Beam Search", "Dot Product", "Transformer",
      "Recurrent Neural Network (RNN)", "seq2seq"],
     [say(f"이 쪽 위에 Table 3 이 있어요. 부품을 하나씩 바꿔 보며 성능을 잰 표예요.",
          f"논문은 이 실험의 이름을 {MV} 이라고 붙였어요.",
          "줄마다 (A), (B), (C), (D), (E) 라는 꼬리표가 붙어 있어요.",
          f"아래 6.3 은 번역 말고 {CP} 도 해 봤다는 이야기예요."),
      analogy("라면에서 재료 하나씩 빼 보기",
              "계란만 빼고, 파만 빼고, 물만 늘려 보면서 맛이 어떻게 변하는지 봐요. 무엇이 중요한 재료인지 알 수 있어요.",
              ("기본 라면", "base 모델"),
              ("재료 하나만 바꾸기", MV),
              ("맛 점수", BLEU),
              ("헷갈린 정도", PPL)),
      points("Table 3 의 다섯 블록",
             f"(A) {HEAD} 개수만 1, 4, 8, 16, 32 로 바꿔요",
             "(B) 키 차원 d_k 만 16, 32 로 줄여요",
             "(C) 층 수와 차원을 키우거나 줄여요",
             f"(D) {DROP} 과 {LS} 값을 바꿔요",
             f"(E) {SPE} 대신 학습 위치 {EMB} 을 써요")],
     [points("6.2 와 Table 3 의 영어와 우리말 뜻",
             '"**Variations on the Transformer architecture**" = 트랜스포머 구조를 이리저리 바꿔 본 것',
             '"**Unlisted values are identical to those of the base model**" = 빈칸은 base 와 같다는 뜻',
             '"**keeping the amount of computation constant**" = 계산량은 그대로 두고',
             '"**single-head attention is 0.9 BLEU worse**" = 헤드가 하나면 0.9 BLEU 나쁘다',
             '"**quality also drops off with too many heads**" = 헤드가 너무 많아도 떨어진다',
             '"**dropout is very helpful in avoiding over-fitting**" = 드롭아웃이 과적합을 막는 데 큰 도움이 된다',
             '"**per-wordpiece ... should not be compared to per-word perplexities**" = 워드피스 단위라 단어 단위와 비교하면 안 된다'),
      points("6.3 첫 부분의 영어와 우리말 뜻",
             '"**generalize to other tasks**" = 다른 과제에도 통하는지 본다',
             '"**the output is subject to strong structural constraints**" = 출력이 꼭 지켜야 할 구조가 있다',
             '"**significantly longer than the input**" = 출력이 입력보다 훨씬 길다',
             '"**RNN sequence-to-sequence models have not been able to attain state-of-the-art**" = RNN seq2seq 는 최고 성적을 못 냈다',
             '"**about 40K training sentences**" = 학습 문장 약 4만 개',
             '"**semi-supervised setting ... approximately 17M sentences**" = 준지도 설정에서는 약 1700만 문장'),
      compare("Table 3 의 base 줄 읽기",
              ["칸", "값", "뜻"],
              ["N", "6", "층을 6개 쌓았어요"],
              ["d_model / d_ff", "512 / 2048", "표현 차원과 FFN 가운데 차원"],
              ["h / d_k / d_v", "8 / 64 / 64", f"{HEAD} 8개, 헤드마다 64칸"],
              ["P_drop / eps_ls", "0.1 / 0.1", f"{DROP} 과 {LS} 값"],
              ["train steps", "100K", "10만 스텝 학습"],
              ["PPL / BLEU / params", "4.92 / 25.8 / 65", f"{PPL}, {BLEU}, 백만 단위 {PARAM}"]),
      steps("Table 3 을 읽는 요령",
            ["1. 먼저 맨 위 base 줄의 값을 외워요",
             "2. 아래 줄들은 빈칸이 많은데, 빈칸은 base 와 같다는 뜻이에요",
             "3. 그래서 값이 적힌 칸만 바뀐 부품이에요",
             f"4. 오른쪽 세 칸 {PPL}, {BLEU}, params 를 base 와 비교해요",
             "5. PPL 은 낮을수록, BLEU 는 높을수록 좋아요"],
            "빈칸은 base 와 같다. 이 한 줄만 알면 Table 3 이 읽혀요."),
      check("Table 3 에서 빈칸이 뜻하는 것은?",
            ["base 모델과 같은 값", "0 이라는 뜻", "실험을 안 했다는 뜻", "측정 실패"], 0,
            "Unlisted values are identical to those of the base model 이라고 캡션에 적혀 있어요.")],
     [look("Table 3 의 base 와 (A), (B), (C) 를 짚어 봐요",
           (0.17, 0.086, 0.66, 0.058, "Table 3 캡션. newstest2013 개발셋이고 PPL 은 워드피스 기준이에요."),
           (0.18, 0.164, 0.65, 0.03, "머리글. N, d_model, d_ff, h, d_k, d_v, P_drop, eps_ls, 스텝, PPL, BLEU, params."),
           (0.18, 0.196, 0.65, 0.014, "base 줄. 6, 512, 2048, 8, 64, 64, 0.1, 0.1, 100K, 4.92, 25.8, 65."),
           (0.18, 0.212, 0.65, 0.055, "(A) 블록. 계산량을 고정한 채 헤드 수만 1, 4, 16, 32 로 바꿨어요."),
           (0.18, 0.266, 0.65, 0.026, "(B) 블록. d_k 만 16, 32 로 줄였더니 둘 다 나빠졌어요."),
           (0.18, 0.296, 0.65, 0.10, "(C) 블록. 층 수 N 과 차원 d_model, d_ff 를 키우거나 줄인 실험이에요.")),
      look("Table 3 의 (D), (E), big 과 6.2 본문",
           (0.18, 0.397, 0.65, 0.057, "(D) 블록. 드롭아웃과 라벨 스무딩을 0.0 이나 0.2 로 바꾼 실험이에요."),
           (0.18, 0.456, 0.65, 0.014, "(E) 줄. 사인 코사인 대신 학습 위치 임베딩을 써도 4.92 와 25.7 로 거의 같아요."),
           (0.18, 0.472, 0.65, 0.016, "big 줄. 4.33, 26.4, 파라미터 213 백만이에요."),
           (0.17, 0.557, 0.66, 0.045, "(A) 설명. 헤드 하나면 0.9 BLEU 나쁘고, 너무 많아도 떨어진다고 적었어요."),
           (0.17, 0.607, 0.66, 0.08, "(B)부터 (E) 설명. d_k 를 줄이면 나빠지고, 크면 좋고, 드롭아웃이 과적합을 막아요."),
           (0.17, 0.706, 0.32, 0.026, "6.3 English Constituency Parsing 제목이에요.")),
      compare("Table 3 (A) 헤드 수만 바꾼 결과",
              ["h", "d_k = d_v", PPL, BLEU],
              ["1", "512", "5.29", "24.9"],
              ["4", "128", "5.00", "25.5"],
              ["8 (base)", "64", "4.92", "25.8"],
              ["16", "32", "4.91", "25.8"],
              ["32", "16", "5.01", "25.4"]),
      compare("Table 3 (B), (C), (D), (E) 에서 꼭 볼 줄",
              ["줄", "바꾼 것", PPL, BLEU],
              ["(B)", "d_k = 16", "5.16", "25.1"],
              ["(C)", "N = 2", "6.11", "23.7"],
              ["(C)", "d_ff = 4096", "4.75", "26.2"],
              ["(D)", "P_drop = 0.0", "5.77", "24.6"],
              ["(D)", "eps_ls = 0.2", "5.47", "25.7"],
              ["(E)", "학습 위치 임베딩", "4.92", "25.7"],
              ["big", "d_model 1024, h 16", "4.33", "26.4"]),
      steps("헤드 하나가 0.9 나쁘다는 말을 검산",
            ["1. 가장 좋은 설정은 h = 8 과 h = 16 의 25.8 이에요",
             "2. h = 1 일 때는 24.9 예요",
             "3. 25.8 - 24.9 = 0.9 예요",
             "4. 그래서 single-head attention is 0.9 BLEU worse 라고 적었어요",
             "5. 그런데 h = 32 도 25.4 로 떨어져요. 많다고 좋은 게 아니에요"],
            f"{HEAD} 는 8이나 16 쯤이 좋아요. 계산량은 다섯 경우 모두 같게 맞췄어요.",
            "h = 1 은 24.9, h = 8 은 25.8"),
      points("(B) 가 남긴 논문의 추측",
             '논문: "determining compatibility is not easy"',
             f'논문: "a more sophisticated compatibility function than {DP} may be beneficial"',
             "곧 내적보다 더 정교한 점수 함수가 나을 수도 있다는 말이에요",
             "may be 라고 적었으니 논문도 단정하지 않은 추측이에요"),
      bg("기초 다지기 6단원 소프트맥스와 교차 엔트로피",
         f"{PPL} 는 교차 엔트로피에 exp 를 씌운 값이에요. 다음 토큰 후보가 평균 몇 개나 헷갈리는지예요.",
         f"Table 3 의 {PPL} 는 {WP} 조각 단위로 잰 값이에요.",
         "단어 단위로 잰 다른 논문의 수치와 나란히 놓고 비교하면 안 된다고 캡션이 못박았어요."),
      prof("교수님: 헤드를 여러 개 쓴다고 전체 차원을 키우는 게 아니에요.",
           "교수님: 전체 차원을 h 로 나눠서 서로 다른 관점에서 보는 거예요.",
           "교수님: 계산 수는 똑같아요."),
      figure("헤드 수와 BLEU", FIG_T3, "하나도 나쁘고 너무 많아도 나빠요.", 4)],
     [check("Table 3 (E) 가 보여 준 것은?",
            ["학습 위치 임베딩을 써도 결과가 거의 같다", "사인 코사인이 훨씬 좋다",
             "위치 인코딩이 필요 없다", "두 방식을 같이 써야 한다"], 0,
            f"4.92 와 25.7 로 base 와 거의 같아요. 논문은 nearly identical results 라고 적었어요."),
      check("Table 3 에서 드롭아웃을 0.0 으로 두면?",
            ["PPL 5.77, BLEU 24.6 으로 나빠진다", "성능이 좋아진다",
             "변화가 없다", "파라미터가 줄어든다"], 0,
            f"논문은 {DROP} 이 {OVF} 을 막는 데 아주 도움이 된다고 적었어요."),
      english("시험 답안 문장",
              "Table 3 은 부품을 하나씩 바꾼 실험으로, 헤드가 하나면 0.9 BLEU 나빠지고 드롭아웃을 빼면 과적합으로 성능이 떨어지며, 위치 인코딩은 사인 코사인이든 학습이든 거의 같았다.",
              "헤드, 드롭아웃, 위치 인코딩 세 가지 결론만 기억하면 돼요.",
              "0.9 / 과적합 / 거의 같음. 세 낱말로 외워요."),
      warn("헷갈리기 쉬운 점",
           "흔히 ablation 이라고 부르는 실험이지만 논문은 Model Variations 라고만 적었어요.",
           f"(A) 는 계산량을 고정한 채 {HEAD} 수만 바꾼 거예요. 모델을 키운 실험이 아니에요.",
           f"Table 3 의 {PPL} 는 {WP} 단위라 다른 논문의 단어 단위 값과 비교하면 안 돼요.",
           "Table 3 은 newstest2013 개발셋이고 Table 2 는 newstest2014 예요. 표가 서로 달라요.",
           f"(E) 결과를 보면 {SPE} 이 성능 때문에 뽑힌 게 아니에요. 긴 문장 기대 때문이었어요."),
      exam("예상 문제",
           "Table 3 의 (A) 행이 보여 주는 결론과, 그 실험이 공정한 비교인 이유를 쓰시오.",
           "헤드 수 실험의 결론과 설계를 묻는 문제예요.",
           ["1. h = 1 은 BLEU 24.9, h = 8 은 25.8 이라 차이가 0.9 예요",
            "2. h = 16 도 25.8 이지만 h = 32 는 25.4 로 다시 떨어져요",
            "3. 결론은 헤드가 하나면 나쁘고 너무 많아도 나쁘다는 것이에요",
            "4. d_k = d_v = d_model / h 로 맞춰서 계산량을 고정했기 때문에 공정해요",
            "5. h = 1 일 때 d_k = 512, h = 32 일 때 d_k = 16 인 것이 그 증거예요"],
           "헤드는 적당히 여러 개가 좋고, 차원을 나눠 계산량을 고정했기에 공정한 비교예요.")])

data = {"deck": "NP", "from": 5, "to": 9,
        "glossary": [{"ko": k, "en": e, "say": s, "more": m} for k, e, s, m in GLOSSARY],
        "slides": S}

raw = json.dumps(data, ensure_ascii=False, indent=1)
for ch in ("—", "–", "·", "・"):
    assert ch not in raw, ch
with open(OUT, "w", encoding="utf-8") as f:
    f.write(raw)
print("saved", OUT, len(S), "pages")
