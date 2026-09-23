# 2강(N2) 회독 레슨 38~50쪽 생성기. 사용: python build_N2_038-050.py
# 범위: 네거티브 샘플링, Skip-gram vs CBOW, 떠오르는 의미 지도, 4부(세기, SVD, GloVe, 평가, 한계), 마무리
import json, math, os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "N2_038-050.json")
W, H = 1400, 788  # 슬라이드 PNG 크기

MANTRA = "글을 토큰으로 자르고, 토큰을 벡터로 바꾸고, 벡터로 다음 토큰을 맞혀요."

# ---------------- 손계산 확인 (Python assert) ----------------
def sig(x):
    return 1 / (1 + math.exp(-x))

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))

def norm(a):
    return math.sqrt(dot(a, a))

def cos(a, b):
    return dot(a, b) / (norm(a) * norm(b))

# (1) 시그모이드: 슬라이드 표 값
assert round(sig(0), 2) == 0.50 and round(sig(2), 2) == 0.88 and round(sig(-2), 2) == 0.12
assert round(sig(1), 2) == 0.73 and round(sig(-1), 2) == 0.27
# (2) 네거티브 샘플링 손실 한 번: 진짜 짝 내적 2, 가짜 짝 내적 0
vc, uo, uk = (1, 1), (1, 1), (1, -1)
assert dot(uo, vc) == 2 and dot(uk, vc) == 0
p_real = sig(dot(uo, vc))           # 0.881
p_fake_ok = sig(-dot(uk, vc))       # 0.5
J = -math.log(p_real) - math.log(p_fake_ok)
assert round(p_real, 3) == 0.881 and p_fake_ok == 0.5
assert round(-math.log(p_real), 3) == 0.127 and round(-math.log(0.5), 3) == 0.693 and round(J, 2) == 0.82
# 가짜 짝을 더 멀리 밀면(내적 -2) 벌점이 줄어요
J2 = -math.log(p_real) - math.log(sig(2))
assert round(J2, 2) == 0.25 and J2 < J
# (3) freq^(3/4): 81 번 대 1 번
assert round(81 ** 0.75) == 27 and 1 ** 0.75 == 1
assert round(81 / 82, 3) == 0.988 and round(27 / 28, 3) == 0.964
assert round(1 / 82, 3) == 0.012 and round(1 / 28, 3) == 0.036
# (4) 코사인 유사도
a, b = (3, 4), (4, 3)
assert dot(a, b) == 24 and norm(a) == 5 and norm(b) == 5 and round(cos(a, b), 2) == 0.96
assert cos((1, 0), (0, 1)) == 0
# (5) 유추: king - man + woman
man, woman, king, queen = (1, 1), (1, 3), (4, 1), (4, 3)
x = tuple(k - m + w for k, m, w in zip(king, man, woman))
assert x == (4, 3) == queen
assert round(cos(x, queen), 2) == 1.0 and round(cos(x, woman), 2) == 0.82 and round(cos(x, king), 2) == 0.92
assert woman[0] - man[0] == queen[0] - king[0] and woman[1] - man[1] == queen[1] - king[1] == 2
# (6) 동시 발생 행렬: 슬라이드 표의 숫자는 바로 옆(윈도우 1)만 센 것과 같아요
sents = [["I", "like", "deep", "learning"], ["I", "like", "NLP"], ["I", "enjoy", "flying"]]
def cooc(wsize):
    c = Counter()
    for s in sents:
        for i, w_ in enumerate(s):
            for j in range(max(0, i - wsize), min(len(s), i + wsize + 1)):
                if j != i:
                    c[(w_, s[j])] += 1
    return c
c1, c2 = cooc(1), cooc(2)
assert c1[("I", "like")] == 2 and c1[("I", "enjoy")] == 1 and c1[("I", "deep")] == 0
assert c2[("I", "deep")] == 1  # 윈도우 2 라면 I-deep 이 1 이 되어야 해요(표는 0)
assert len({w_ for s in sents for w_ in s}) == 7
# (7) GloVe 가중치 f(x), x_max = 100, alpha = 3/4
f = lambda v: (v / 100) ** 0.75 if v < 100 else 1.0
assert round(f(1), 3) == 0.032 and round(f(10), 3) == 0.178 and f(100) == 1.0 and f(250) == 1.0
# (8) 클리핑 min(X, 100), 로그
assert min(250, 100) == 100 and min(7, 100) == 7
assert round(math.log(100), 2) == 4.61 and round(math.log(1000), 2) == 6.91
# (9) 파라미터 수 느낌: 실습 word2vec 의 벡터 한 개 = 100 개 숫자
assert 2 * 300 * 100000 == 60_000_000

# ---------------- 용어 ----------------
# key: (ko, en, 본문 표기)
TERMS = {
    "ns": ("네거티브 샘플링", "Negative Sampling", None),
    "sig": ("시그모이드", "Sigmoid", None),
    "soft": ("소프트맥스", "Softmax", None),
    "dot": ("내적", "Dot Product", None),
    "cos": ("코사인 유사도", "Cosine Similarity", None),
    "sg": ("스킵그램", "Skip-gram", None),
    "cbow": ("연속 단어 주머니", "CBOW", "**CBOW(연속 단어 주머니)**"),
    "center": ("중심 단어", "Center Word", None),
    "context": ("문맥 단어", "Context Word", None),
    "window": ("윈도우", "Window", None),
    "w2v": ("워드투벡", "word2vec", "**word2vec**"),
    "wv": ("단어 벡터", "Word Vector", None),
    "emb": ("임베딩", "Embedding", None),
    "loss": ("손실 함수", "Loss Function", None),
    "obj": ("목적 함수", "Objective Function", None),
    "lik": ("우도", "Likelihood", None),
    "param": ("파라미터", "Parameter", None),
    "sgd": ("확률적 경사 하강법", "Stochastic Gradient Descent (SGD)", "**확률적 경사 하강법(SGD)**"),
    "bin": ("이진 분류", "Binary Classification", None),
    "corpus": ("말뭉치", "Corpus", None),
    "vocab": ("어휘", "Vocabulary", None),
    "oov": ("미등록 단어", "Out-of-Vocabulary (OOV)", "**미등록 단어(OOV)**"),
    "dist": ("분포 가설", "Distributional Hypothesis", None),
    "cooc": ("동시 발생 행렬", "Co-occurrence Matrix", None),
    "svd": ("특이값 분해", "Singular Value Decomposition (SVD)", "**특이값 분해(SVD)**"),
    "lsa": ("잠재 의미 분석", "Latent Semantic Analysis (LSA)", "**잠재 의미 분석(LSA)**"),
    "func": ("기능어", "Function Word", None),
    "glove": ("글로브", "GloVe", "**GloVe(글로브)**"),
    "wf": ("가중치 함수", "Weighting Function", None),
    "intr": ("내적 평가", "Intrinsic Evaluation", None),
    "extr": ("외적 평가", "Extrinsic Evaluation", None),
    "ana": ("단어 유추", "Word Analogy", None),
    "wsim": ("단어 유사도", "Word Similarity", None),
    "ner": ("개체명 인식", "Named Entity Recognition (NER)", "**개체명 인식(NER)**"),
    "cls": ("분류", "Classification", None),
    "poly": ("다의어", "Polysemy", None),
    "bias": ("편향", "Bias", None),
    "static": ("정적 단어 벡터", "Static Word Vector", None),
    "ctxemb": ("문맥 임베딩", "Contextual Embedding", None),
    "token": ("토큰", "Token", None),
    "tokz": ("토큰화", "Tokenization", None),
    "tokzr": ("토크나이저", "Tokenizer", None),
    "sub": ("서브워드", "Subword", None),
    "bpe": ("바이트 쌍 인코딩", "Byte Pair Encoding (BPE)", "**BPE(바이트 쌍 인코딩)**"),
    "fert": ("토큰 과다 분할", "Fertility", "**토큰 과다 분할(Fertility)**"),
    "gd": ("경사 하강법", "Gradient Descent", None),
}


def T(k):
    ko, en, disp = TERMS[k]
    if disp:
        return disp
    return f"**{ko}({en})**"


def EN(k):
    return TERMS[k][1]


GLOSS = {
    "ns": ("진짜 이웃 단어 하나와 아무렇게나 뽑은 가짜 단어 몇 개만 비교해서 빠르게 배우는 방법",
           "소프트맥스처럼 어휘 전체(10만 개)와 내적하지 않고, 진짜 짝 1개와 가짜 k개를 가려내는 이진 분류로 바꿔요. 가짜는 빈도의 3/4 제곱 비율로 뽑아요."),
    "sig": ("아무 숫자나 넣으면 0과 1 사이 값으로 바꿔 주는 S자 함수",
            "식은 1/(1+exp(-x)) 이고, 0을 넣으면 0.5, 2를 넣으면 약 0.88, -2를 넣으면 약 0.12가 나와요. '예일 확률' 하나를 낼 때 써요."),
    "soft": ("점수를 모두 더해 1이 되는 확률 파이로 나누는 함수",
             "exp(점수)를 모든 후보의 exp(점수) 합으로 나눠요. 분모에 어휘 전체가 들어가서 계산이 무거워요."),
    "dot": ("두 벡터의 같은 자리 숫자를 곱해서 모두 더한 값",
            "두 화살표가 같은 쪽을 볼수록 커져요. word2vec 에서는 두 단어가 이웃일 만한 정도를 나타내는 점수예요."),
    "cos": ("두 화살표가 얼마나 같은 쪽을 보는지를 -1~1 로 잰 값",
            "내적을 두 벡터 길이의 곱으로 나눠요. 1이면 같은 방향, 0이면 직각, -1이면 반대 방향이에요."),
    "sg": ("중심 단어 하나를 보고 주변 문맥 단어들을 맞히는 word2vec 방식",
           "P(문맥 단어 | 중심 단어)를 크게 해요. 드문 단어와 작은 데이터에 강하고, 이 수업과 논문의 기본값이에요."),
    "cbow": ("주변 문맥 단어들을 보고 가운데 중심 단어를 맞히는 word2vec 방식",
             "Continuous Bag of Words 의 줄임말이에요. 창 안의 문맥을 뭉쳐 한 번에 배우니 빠르고, 자주 나오는 단어에 강해요."),
    "center": ("지금 뜻을 배우고 있는 가운데 단어",
               "윈도우의 한가운데 있는 단어예요. 벡터 v_c 로 나타내요."),
    "context": ("중심 단어 주변 윈도우 안에 나온 이웃 단어",
                "벡터 u_o 로 나타내요. 분포 가설에 따라 이웃이 단어의 뜻을 알려 줘요."),
    "window": ("중심 단어 양옆으로 몇 칸까지 이웃으로 볼지 정한 창",
               "window=5 면 왼쪽 5칸, 오른쪽 5칸이 문맥이에요. 동시 발생 행렬을 셀 때도 같은 창을 써요."),
    "w2v": ("주변 단어를 맞히는 게임을 하며 단어 벡터를 배우는 방법",
            "2013년에 나온 방법으로, Skip-gram 과 CBOW 두 가지가 있어요. 보통 네거티브 샘플링과 함께 돌려요."),
    "wv": ("단어의 지도 좌표. 뜻이 비슷하면 가까이 살아요",
           "단어 하나를 숫자 목록(예 100개, 300개)으로 나타낸 것이에요. 원-핫 벡터와 달리 비슷한 정도를 숫자로 잴 수 있어요."),
    "emb": ("단어를 짧고 촘촘한 숫자 벡터로 바꿔 둔 것, 곧 단어의 지도 좌표",
            "학습으로 얻은 단어 벡터를 임베딩이라고도 불러요. GloVe 임베딩처럼 방법 이름을 붙여 부르기도 해요."),
    "loss": ("틀린 정도를 매기는 벌점",
             "학습은 이 벌점을 가장 줄이는 쪽으로 파라미터를 조금씩 고치는 일이에요."),
    "obj": ("학습이 줄이거나 키우려는 목표 식",
            "word2vec 에서는 J(θ)예요. 음의 로그 우도를 평균 낸 것이라 손실 함수처럼 줄여요."),
    "lik": ("지금 파라미터로 실제 데이터가 나올 확률을 모두 곱한 값",
            "우도를 키우는 것과 음의 로그 우도(NLL)를 줄이는 것은 같은 말이에요."),
    "param": ("학습으로 조금씩 고쳐 나가는 모델 속 숫자들",
              "word2vec 에서는 모든 단어의 u 벡터와 v 벡터를 모은 θ 예요."),
    "sgd": ("데이터 전체 대신 조금만 떼어 기울기를 어림하고 자주 한 걸음씩 가는 방법",
            "정확하지만 느린 것보다, 흔들리지만 빠른 쪽을 고르는 딥러닝의 기본 학습법이에요."),
    "bin": ("예, 아니오 둘 중 하나를 고르는 문제",
            "네거티브 샘플링은 '이 짝이 진짜 이웃인가?'를 예, 아니오로 가리는 이진 분류로 바꿔요. 시그모이드가 '예일 확률'을 내요."),
    "corpus": ("학습에 쓰는 글을 잔뜩 모아 둔 것",
               "실습에서는 네이버 영화 리뷰(NSMC) 말뭉치를 써요. 말뭉치에 없는 단어는 배울 수 없어요."),
    "vocab": ("레고 상자에 든 조각 종류 목록, 곧 모델이 아는 토큰 목록",
              "어휘 크기 |V| 가 10만이면 소프트맥스 분모에 10만 개 내적이 들어가요."),
    "oov": ("어휘 목록에 없어서 모델이 모르는 단어",
            "실습에서 영화 리뷰에 '김치'가 거의 안 나와 유사도를 못 구하고 OOV 가 떠요."),
    "dist": ("친구를 보면 그 사람을 안다. 주변 단어가 단어의 뜻을 알려 준다는 생각",
             "word2vec 과 동시 발생 행렬 모두 이 생각 위에 서 있어요."),
    "cooc": ("어떤 단어가 어떤 단어 옆에 몇 번 함께 나왔는지 센 표",
             "행이 대상 단어, 열이 문맥 단어예요. 어휘가 10만이면 10만 x 10만 표가 되고 대부분 0이에요."),
    "svd": ("큰 표를 세 행렬의 곱으로 쪼개서 중요한 방향 몇 개만 남기는 방법",
            "X ≈ U_k Σ_k V_k^T 처럼 위쪽 k 개 특이값만 남겨, 듬성듬성한 큰 벡터를 촘촘한 작은 벡터로 줄여요."),
    "lsa": ("단어-문서 표를 SVD 로 줄여 숨은 뜻 구조를 찾는 옛 방법",
            "세기로 벡터를 얻는 고전적인 길이에요. SVD 로 k 차원만 남겨요."),
    "func": ("the, of 처럼 문법 역할만 하고 뜻은 적은 단어",
             "거의 모든 문장에 나와서 그냥 세면 표를 온통 지배해요. 그래서 빼거나 줄이는 보정을 해요."),
    "glove": ("전체 말뭉치를 센 통계와 예측 학습을 합친 단어 벡터 방법",
              "Global Vectors 의 줄임말(2014)이에요. 두 단어 벡터의 내적이 함께 나온 횟수의 로그를 맞히도록 배워요. 수식은 시험에 내지 않는다고 했어요."),
    "wf": ("GloVe 에서 단어 짝 하나를 얼마나 믿을지 정하는 무게",
           "f(x) = (x/x_max)^α (x < x_max), 그 이상은 1. x_max = 100, α = 3/4 예요. 너무 흔한 짝이 지배하지 않게 막아요."),
    "intr": ("단어 벡터 자체를 바로 시험해 보는 평가",
             "단어 유추, 단어 유사도로 재요. 빠르고 어디가 문제인지 알려 주지만, 실제 성능과 이어지는지는 따로 보여야 해요."),
    "extr": ("단어 벡터를 실제 과제에 끼워 넣어 최종 성능을 재는 평가",
             "개체명 인식, 분류, 검색 같은 과제로 재요. 진짜 중요한 값이지만 느리고, 어디가 문제인지는 못 알려 줘요."),
    "ana": ("a 대 b 는 c 대 무엇? 을 벡터 셈으로 푸는 시험",
            "man : woman :: king : ? 이면 b - a + c 와 코사인 유사도가 가장 큰 단어를 골라요. 구글 유추 데이터는 19,544 문항이에요."),
    "wsim": ("사람이 매긴 두 단어의 비슷함 점수와 벡터의 코사인이 얼마나 같이 가는지 보는 시험",
             "WordSim-353 은 353 쌍이에요. 예 tiger-cat 7.35, tiger-tiger 10, stock-jaguar 0.92."),
    "ner": ("글에서 사람, 장소, 기관 같은 이름을 찾아 표시하는 과제",
            "외적 평가에 쓰는 실제 과제의 예예요."),
    "cls": ("글을 정해진 칸(긍정/부정 등) 중 하나로 나누는 과제",
            "외적 평가에서 단어 벡터를 넣어 성능을 재는 과제의 예예요."),
    "poly": ("한 단어가 여러 뜻을 가진 것",
             "'배'는 먹는 배, 타는 배, 몸의 배예요. 단어 하나에 벡터 하나라서 세 뜻이 뭉개진 평균이 돼요."),
    "bias": ("말뭉치에 스며 있는 사회적 치우침을 벡터가 그대로 배우는 것",
             "man : programmer :: woman : homemaker 가 실제 2016년 논문 제목이에요. 찾고 줄이는 연구는 있지만 뿌리는 아직 못 풀었어요."),
    "static": ("한 번 학습이 끝나면 문맥이 바뀌어도 그대로인 단어 벡터",
               "word2vec, GloVe 벡터가 여기에 들어가요. 그래서 다의어를 구별하지 못해요."),
    "ctxemb": ("같은 단어라도 문맥에 따라 벡터가 달라지는 임베딩",
               "다의어 문제의 해결책이에요. 5주차 BERT 에서 배워요."),
    "token": ("글을 자른 레고 조각 하나",
              "모델이 한 번에 받는 글 조각이에요. 단어일 수도, 서브워드일 수도 있어요."),
    "tokz": ("글을 토큰이라는 레고 조각으로 자르는 일",
             "주문의 첫 단계예요. 실습에서는 띄어쓰기로만 잘라서 '영화다', '영화였다'가 따로 어휘가 됐어요."),
    "tokzr": ("글을 토큰으로 잘라 주는 도구",
              "실습에서 한국어 BPE 토크나이저를 직접 학습해 봐요."),
    "sub": ("단어보다 작고 글자보다 큰 조각",
            "지금의 토큰은 단어도 글자도 아닌 서브워드예요."),
    "bpe": ("자주 붙어 다니는 두 조각을 한 조각으로 접착하기를 되풀이하는 토큰화 방법",
            "'세고, 합치기'를 반복해요. 과제 1 Part A 에서 한국어 토이 말뭉치로 해 봐요."),
    "fert": ("한 단어가 토큰 몇 개로 쪼개지는지, 곧 과다 분할 정도",
             "영어 중심 토크나이저는 한국어를 잘게 쪼개서 fertility 가 커요."),
    "gd": ("안개 낀 산에서 발밑 기울기만 보고 한 걸음씩 내려가기",
           "손실 함수가 줄어드는 쪽으로 파라미터를 조금씩 고쳐요. 보폭이 학습률이에요."),
}

# ---------------- SVG 도우미 (클래스만 사용) ----------------
def _b(b):
    return f" b{b}" if b else ""


def SVG(*els, h=270):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 {h}">' + "".join(els) + "</svg>"


def TX(x, y, s, cls="t", size=15, anchor="middle", b=0):
    return f'<text x="{x}" y="{y}" class="{cls}{_b(b)}" font-size="{size}" text-anchor="{anchor}">{s}</text>'


def L(x1, y1, x2, y2, cls="e", b=0):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{cls}{_b(b)}"/>'


def R(x, y, w, h, cls="n", b=0):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" class="{cls}{_b(b)}"/>'


def C(cx, cy, r, cls="n", b=0):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" class="{cls}{_b(b)}"/>'


def A(x1, y1, x2, y2, cls="e2", b=0):
    """화살표: 선 + 머리"""
    dx, dy = x2 - x1, y2 - y1
    d = math.hypot(dx, dy) or 1
    ux, uy = dx / d, dy / d
    bx, by = x2 - ux * 10, y2 - uy * 10
    px, py = -uy * 5, ux * 5
    pts = f"{x2:.1f},{y2:.1f} {bx + px:.1f},{by + py:.1f} {bx - px:.1f},{by - py:.1f}"
    return L(x1, y1, round(bx, 1), round(by, 1), cls, b) + f'<polygon points="{pts}" class="arrow{_b(b)}"/>'


def BOX(x, y, w, h, s, cls="box", tcls="tb", b=0, size=15):
    return R(x, y, w, h, cls, b) + TX(x + w / 2, y + h / 2 + size / 3, s, tcls, size, "middle", b)


# ---------------- 장면 도우미 ----------------
def say(*lines):
    return {"kind": "say", "lines": list(lines)}


def points(head, *items):
    return {"kind": "points", "head": head, "items": list(items)}


def analogy(head, scene, mp):
    return {"kind": "analogy", "head": head, "scene": scene, "map": mp}


def compare(head, cols, rows):
    return {"kind": "compare", "head": head, "cols": cols, "rows": rows}


def steps(head, st, answer, given=None):
    d = {"kind": "steps", "head": head, "steps": st, "answer": answer}
    if given:
        d["given"] = given
    return d


def formula(head, tex, parts, whole):
    return {"kind": "formula", "head": head, "tex": tex, "parts": [{"sym": s, "say": t} for s, t in parts], "whole": whole}


def figure(head, svg, caption, builds):
    return {"kind": "figure", "head": head, "svg": svg, "caption": caption, "builds": builds}


def check(q, choices, a, why):
    return {"kind": "check", "q": q, "choices": choices, "a": a, "why": why}


def english(head, en, ko, tip=None):
    d = {"kind": "english", "head": head, "en": en, "ko": ko}
    if tip:
        d["tip"] = tip
    return d


def warn(head, *items):
    return {"kind": "warn", "head": head, "items": list(items)}


def prof(when, *lines):
    return {"kind": "prof", "when": when, "lines": list(lines)}


def bg(src, *lines):
    return {"kind": "bg", "src": src, "lines": list(lines)}


def exam(src, q, qko, solve, answer):
    return {"kind": "exam", "src": src, "q": q, "qko": qko, "solve": solve, "answer": answer}


def box(x0, y0, x1, y1, s):
    """픽셀 좌표(1400x788) → 비율"""
    return {"x": round(x0 / W, 3), "y": round(y0 / H, 3), "w": round((x1 - x0) / W, 3), "h": round((y1 - y0) / H, 3), "say": s}


def look(head, *boxes):
    return {"kind": "look", "head": head, "boxes": list(boxes)}


MON2 = "2주차 월요일 2교시"
MON3 = "2주차 월요일 3교시 (실습)"

S = []

# ---------------- 그림 ----------------
FIG_NS = SVG(
    BOX(20, 110, 120, 44, "banking", "box2", "tb", 0, 16), TX(80, 176, "중심 단어", "tm", 14),
    BOX(320, 20, 140, 40, "crises", "n3", "tl", 1, 16), TX(390, 78, "진짜 이웃: 당기기", "tb", 14, "middle", 1),
    A(140, 120, 318, 44, "e2", 1),
    BOX(320, 110, 140, 34, "aardvark", "n4", "tl", 2, 15),
    BOX(320, 160, 140, 34, "pizza", "n4", "tl", 2, 15),
    BOX(320, 210, 140, 34, "the", "n4", "tl", 2, 15),
    A(140, 140, 318, 127, "e", 2), A(140, 145, 318, 177, "e", 2), A(140, 150, 318, 227, "e", 2),
    TX(240, 262, "무작위 가짜 k개: 밀어내기", "tb", 14, "middle", 2),
)

FIG_SGCB = SVG(
    TX(120, 22, "Skip-gram", "tb", 16), TX(360, 22, "CBOW", "tb", 16, "middle", 2), L(240, 10, 240, 262),
    BOX(10, 112, 90, 40, "banking", "box2", "tb", 1, 14),
    BOX(150, 40, 80, 30, "turning", "n3", "tl", 1, 13), BOX(150, 90, 80, 30, "into", "n3", "tl", 1, 13),
    BOX(150, 140, 80, 30, "crises", "n3", "tl", 1, 13), BOX(150, 190, 80, 30, "problems", "n3", "tl", 1, 13),
    A(100, 125, 148, 55, "e2", 1), A(100, 128, 148, 105, "e2", 1), A(100, 136, 148, 155, "e2", 1), A(100, 140, 148, 205, "e2", 1),
    TX(120, 252, "중심 → 문맥 맞히기", "tm", 14, "middle", 1),
    BOX(250, 40, 80, 30, "turning", "n3", "tl", 2, 13), BOX(250, 90, 80, 30, "into", "n3", "tl", 2, 13),
    BOX(250, 140, 80, 30, "crises", "n3", "tl", 2, 13), BOX(250, 190, 80, 30, "problems", "n3", "tl", 2, 13),
    BOX(380, 112, 90, 40, "banking", "box2", "tb", 2, 14),
    A(330, 55, 378, 125, "e2", 2), A(330, 105, 378, 128, "e2", 2), A(330, 155, 378, 136, "e2", 2), A(330, 205, 378, 140, "e2", 2),
    TX(360, 252, "문맥 → 중심 맞히기", "tm", 14, "middle", 2),
)

FIG_MAP = SVG(
    R(10, 30, 220, 200, "box"), TX(120, 22, "비슷한 단어는 가까이", "tb", 14),
    C(50, 80, 6, "n3", 1), TX(62, 85, "cat", "t", 14, "start", 1),
    C(80, 110, 6, "n3", 1), TX(92, 115, "고양이", "t", 14, "start", 1),
    C(160, 70, 6, "n2", 1), TX(172, 75, "pizza", "t", 14, "start", 1),
    C(150, 105, 6, "n2", 1), TX(162, 110, "kimchi", "t", 14, "start", 1),
    C(90, 185, 6, "n", 1), TX(102, 190, "happy", "t", 14, "start", 1),
    C(120, 205, 6, "n", 1), TX(132, 210, "기쁘다", "t", 14, "start", 1),
    R(250, 30, 220, 200, "box", 2), TX(360, 22, "king - man + woman", "tb", 14, "middle", 2),
    C(290, 190, 6, "n", 2), TX(290, 215, "man", "t", 14, "middle", 2),
    C(410, 200, 6, "n", 2), TX(410, 222, "woman", "t", 14, "middle", 2),
    C(310, 70, 6, "n2", 2), TX(310, 58, "king", "t", 14, "middle", 2),
    A(290, 190, 308, 78, "e2", 2), A(410, 200, 428, 88, "e2", 3),
    C(430, 80, 6, "n2", 3), TX(430, 66, "queen", "tb", 14, "middle", 3),
    TX(360, 260, "같은 화살표 = 같은 관계", "tm", 14, "middle", 3),
)

FIG_COUNT = SVG(
    TX(240, 22, "말뭉치: I like deep learning / I like NLP / I enjoy flying", "tm", 13),
    TX(150, 52, "I", "tb", 14), TX(210, 52, "like", "tb", 14), TX(280, 52, "enjoy", "tb", 14), TX(360, 52, "flying", "tb", 14),
    TX(70, 88, "I", "tb", 14), TX(70, 128, "like", "tb", 14), TX(70, 168, "enjoy", "tb", 14),
    R(120, 64, 320, 120, "box"),
    TX(150, 90, "0", "t", 15, "middle", 1), TX(210, 90, "2", "tb", 16, "middle", 1), TX(280, 90, "1", "tb", 15, "middle", 1), TX(360, 90, "0", "t", 15, "middle", 1),
    TX(150, 130, "2", "tb", 16, "middle", 1), TX(210, 130, "0", "t", 15, "middle", 1), TX(280, 130, "0", "t", 15, "middle", 1), TX(360, 130, "0", "t", 15, "middle", 1),
    TX(150, 170, "1", "tb", 15, "middle", 1), TX(210, 170, "0", "t", 15, "middle", 1), TX(280, 170, "0", "t", 15, "middle", 1), TX(360, 170, "1", "tb", 15, "middle", 1),
    TX(240, 215, "한 번만 세면 표가 나와요", "tb", 15, "middle", 2),
    TX(240, 245, "어휘 10만이면 10만 x 10만, 거의 다 0", "tm", 14, "middle", 2),
)

FIG_SVD = SVG(
    R(20, 50, 150, 170, "n", 0), TX(95, 140, "X", "tl", 20), TX(95, 240, "10만 x 10만, 거의 0", "tm", 14),
    A(180, 135, 250, 135, "e2", 1), TX(215, 120, "SVD", "tb", 15, "middle", 1),
    R(270, 50, 40, 170, "n2", 1), TX(290, 140, "U_k", "tl", 14, "middle", 1),
    R(320, 110, 40, 40, "n3", 1), TX(340, 135, "Σ_k", "tl", 14, "middle", 1),
    R(370, 110, 100, 40, "n", 1), TX(420, 135, "V_k^T", "tl", 14, "middle", 1),
    TX(370, 240, "위쪽 k 개만 남겨 촘촘한 벡터", "tb", 14, "middle", 2),
    TX(370, 262, "car → k 차원 벡터", "tm", 14, "middle", 2),
)

FIG_GLOVE = SVG(
    BOX(20, 40, 180, 50, "세기 (통계)", "n3", "tl", 1, 16), TX(110, 110, "동시 발생 횟수 X_ij", "tm", 14, "middle", 1),
    BOX(280, 40, 180, 50, "예측 (학습)", "n3", "tl", 2, 16), TX(370, 110, "내적 w_i^T w_j", "tm", 14, "middle", 2),
    A(110, 125, 220, 175, "e2", 3), A(370, 125, 260, 175, "e2", 3),
    BOX(140, 180, 200, 50, "GloVe", "box2", "tb", 3, 18),
    TX(240, 255, "내적이 log(횟수)를 맞히게", "tb", 14, "middle", 3),
)

FIG_EVAL = SVG(
    BOX(170, 20, 140, 40, "단어 벡터", "box2", "tb", 0, 16),
    A(210, 60, 110, 110, "e2", 1), A(270, 60, 370, 110, "e2", 2),
    BOX(20, 112, 190, 40, "내적 평가", "n3", "tl", 1, 16),
    TX(115, 180, "유추, 유사도", "t", 14, "middle", 1), TX(115, 205, "빠르고 진단 가능", "tm", 14, "middle", 1), TX(115, 230, "실제 성능은 따로 증명", "tm", 14, "middle", 1),
    BOX(270, 112, 190, 40, "외적 평가", "n2", "tl", 2, 16),
    TX(365, 180, "NER, 분류, 검색", "t", 14, "middle", 2), TX(365, 205, "진짜 중요한 값", "tm", 14, "middle", 2), TX(365, 230, "느리고 원인은 모름", "tm", 14, "middle", 2),
    TX(240, 262, "둘 다 필요해요", "tb", 15, "middle", 3),
)

FIG_POLY = SVG(
    C(90, 60, 8, "n3", 1), TX(90, 40, "먹는 배 (pear)", "t", 14, "middle", 1),
    C(390, 60, 8, "n3", 1), TX(390, 40, "타는 배 (ship)", "t", 14, "middle", 1),
    C(240, 230, 8, "n3", 1), TX(240, 258, "몸의 배 (belly)", "t", 14, "middle", 1),
    L(90, 60, 240, 130, "e", 2), L(390, 60, 240, 130, "e", 2), L(240, 230, 240, 130, "e", 2),
    C(240, 130, 12, "n4", 2), TX(262, 135, "'배' 벡터 하나", "tb", 15, "start", 2),
    TX(262, 158, "세 뜻의 뭉개진 평균", "tm", 14, "start", 2),
)

# ================= p.38 =================
S.append({"p": 38, "title": "네거티브 샘플링: 소프트맥스를 고치는 방법",
 "terms": [EN(k) for k in ["ns", "soft", "sig", "dot", "vocab", "context", "center", "bin", "sg", "w2v", "obj", "loss", "window", "lik"]],
 "pass1": [
  say("앞에서 배운 " + T("soft") + "는 분모 계산이 너무 무거웠어요.",
      "10만 개 단어 모두와 점수를 매겨야 했거든요.",
      T("ns") + "은 '진짜 이웃 1개와 가짜 몇 개만 비교하자'는 해결책이에요."),
  analogy("10만 명 중 정답 고르기 → 진짜와 가짜 가리기",
          "반 친구 10만 명 사진을 다 보고 '이 사람 짝꿍은 누구?'를 고르려면 너무 오래 걸려요. 대신 진짜 짝꿍 사진 1장과 아무나 뽑은 사진 몇 장만 보고 '진짜야, 가짜야?'만 가리면 훨씬 빨라요.",
          [["10만 명 사진 전부 보기", "어휘 전체에 대한 " + T("soft")], ["진짜 짝꿍 1장", "진짜 " + T("context")], ["아무나 뽑은 몇 장", "무작위로 뽑은 가짜 k개"], ["진짜야, 가짜야?", T("bin")]]),
 ],
 "pass2": [
  compare("영어 문장 → 우리말 뜻", ["슬라이드 영어", "우리말 뜻"], [
   ["**Negative Sampling: The Fix for Softmax**", "네거티브 샘플링: 소프트맥스를 고치는 방법"],
   ["a dot product with the whole vocabulary", "어휘 전체와 내적을 해야 해요(분모 때문에)"],
   ["1 real context word vs k random fakes", "진짜 문맥 단어 1개 대 무작위 가짜 k개"],
   ["Push σ(u^T v) up for real pairs", "진짜 짝은 σ(u^T v)를 올려요"],
   ["Skip-gram + negative sampling = the word2vec everyone actually runs", "Skip-gram + 네거티브 샘플링이 모두가 실제로 돌리는 word2vec"]]),
  points("용어 하나씩",
   T("ns") + ": 진짜 이웃 1개와 가짜 k개만 가리는 빠른 학습법",
   T("sig") + ": 아무 숫자나 0과 1 사이로 바꾸는 S자 함수. '진짜일 확률' 하나를 내요",
   T("bin") + ": 예/아니오 둘 중 하나 고르기. 여기서는 '진짜 이웃인가?'",
   T("dot") + ": 두 벡터의 같은 자리끼리 곱해 더한 값. 이웃 점수예요"),
  steps("무엇이 무엇으로 이어지나", [
   T("soft") + " 분모: 중심 단어와 어휘 10만 개 전부 " + T("dot"),
   "너무 느려요 → 문제를 바꿔요",
   "진짜 이웃 1개: '진짜' 쪽 확률 σ(u^T v)를 올리기",
   "가짜 k개: '가짜' 쪽 확률 σ(-u^T v)를 올리기",
   "이 벌점을 줄이도록 " + T("param") + "(u, v 벡터)를 " + T("sgd") + "로 고쳐요",
   "한 번에 내적 k+1 번이면 끝"], "10만 번 내적 → 약 k+1 번 내적으로 줄어요"),
  check("네거티브 샘플링은 소프트맥스의 어떤 문제를 고치나요?",
        ["분모에 어휘 전체와의 내적이 들어가 계산이 너무 무겁다", "확률이 음수로 나온다", "단어 벡터의 차원이 너무 작다"], 0,
        T("soft") + " 분모는 어휘 전체(|V|)와 " + T("dot") + "을 해야 해서 무거워요. " + T("ns") + "은 진짜 1개와 가짜 k개만 봐요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
   box(80, 152, 1070, 190, "'That Σ over |V|': 소프트맥스 분모의 합이 어휘 전체예요. 창 하나마다 어휘 전체와 내적해야 해요."),
   box(80, 195, 1200, 232, "'Idea': 모두와 비교하지 말고, 진짜 문맥 단어 1개 대 가짜 k개의 이진 분류로 바꿔요."),
   box(350, 258, 1010, 385, "네거티브 샘플링의 목적 함수 J_t(θ). 앞 항은 진짜 짝, Σ 항은 가짜 k개예요."),
   box(80, 428, 945, 465, "진짜 짝은 σ(u^T v)를, 가짜는 σ(-u^T v)를 올려요. 가짜는 freq^(3/4) 비율로 뽑아요."),
   box(950, 395, 1365, 665, "시그모이드 σ(x) = 1/(1+exp(-x)) 그래프와 표: σ(0)=0.5, σ(2)=0.88, σ(-2)=0.12."),
   box(380, 680, 1025, 712, "Skip-gram + 네거티브 샘플링 = 모두가 실제로 돌리는 word2vec.")),
  formula("네거티브 샘플링 목적 함수 (창 하나, 중심 단어 c)",
   r"J_t(\theta) = -\log \sigma(u_o^\top v_c) - \sum_{k=1}^{K} \log \sigma(-u_k^\top v_c)",
   [(r"v_c", "중심 단어 c 의 벡터. 지금 배우는 단어의 지도 좌표"),
    (r"u_o", "진짜로 옆에 나온 문맥 단어 o 의 벡터"),
    (r"u_o^\top v_c", "두 벡터의 내적. 클수록 '이웃 같다'는 점수"),
    (r"\sigma(\cdot)", "시그모이드. 점수를 0~1 확률로 바꿔요"),
    (r"u_k,\ K", "무작위로 뽑은 가짜 단어 k 의 벡터, 가짜는 모두 K 개"),
    (r"\sigma(-u_k^\top v_c)", "가짜 짝이 '가짜'일 확률. 내적에 마이너스를 붙였어요")],
   "진짜 짝의 확률과 가짜 짝이 '가짜'일 확률을 모두 크게 만들면, 음의 로그라서 J 는 작아져요. 곧 " + T("loss") + "라는 벌점을 줄이는 쪽으로 배워요."),
  steps("손계산: 시그모이드와 벌점 한 번",
   ["진짜 짝 내적: u_o^T v_c = 1x1 + 1x1 = 2",
    "σ(2) = 1/(1+e^-2) ≈ 0.881 (슬라이드 표의 0.88)",
    "가짜 짝 내적: u_k^T v_c = 1x1 + (-1)x1 = 0 → σ(-0) = σ(0) = 0.5",
    "벌점 J = -log 0.881 - log 0.5 ≈ 0.127 + 0.693 = 0.82",
    "가짜를 더 밀어 내적이 -2 가 되면 σ(2)=0.881 이라 J ≈ 0.127 + 0.127 = 0.25 로 줄어요"],
   "J ≈ 0.82 → 가짜를 밀어내면 약 0.25",
   given="v_c = (1, 1), 진짜 u_o = (1, 1), 가짜 u_k = (1, -1), 가짜 1개(K=1), 자연로그"),
  steps("가짜는 어떻게 뽑나: 빈도의 3/4 제곱",
   ["말뭉치에서 the 가 81번, aardvark 가 1번 나왔다고 해요",
    "그냥 빈도대로면 the 가 뽑힐 확률 81/82 ≈ 0.988, aardvark 1/82 ≈ 0.012",
    "3/4 제곱: 81^(3/4) = 27, 1^(3/4) = 1",
    "이제 the 는 27/28 ≈ 0.964, aardvark 는 1/28 ≈ 0.036"],
   "흔한 단어는 조금 덜, 드문 단어는 조금 더(0.012 → 0.036) 뽑혀요",
   given="freq^(3/4) 는 슬라이드의 가짜 뽑기 규칙"),
  prof(MON2,
   "소프트맥스는 10만 개 중에서 정답 고르기라면, 네거티브 샘플링은 진짜 문맥 단어 하나와 아무거나 뽑아 온 k 개를 구분하기예요.",
   "그러면 분모가 10만 개가 아니라 k+1 개가 되고, 내적이 15번 정도로 줄어 수천 배 빨라진다고 했어요.",
   "가장 중요한 것: 우도를 높이려고 음의 로그 우도(NLL) 손실 함수를 가장 줄이는 방향으로 학습된다는 것."),
  bg("기초 다지기 4단원 (로그와 지수)",
     "exp(-x) 는 x 가 크면 0에 가까워져서 σ(x) 가 1에 가까워져요.",
     "-log(확률) 은 확률이 1에 가까우면 0에 가깝고, 작으면 커지는 벌점이에요."),
  say("실습에서는 N2L p.19 에서 gensim Word2Vec(sg=1, negative=10)으로 이걸 코드로 돌려요.",
      "sg=1 은 Skip-gram, negative=10 은 가짜 10개(k=10)라는 뜻이에요."),
 ],
 "pass4": [
  check("네거티브 샘플링 식에서 가짜 단어 항 σ(-u_k^T v_c) 를 크게 하면 무엇이 일어나나요?",
        ["가짜 단어 벡터와 중심 단어 벡터의 내적이 작아져 서로 멀어진다", "가짜 단어가 진짜 이웃이 된다", "어휘 크기가 줄어든다"], 0,
        "σ(-x) 가 커지려면 x = u_k^T v_c 가 작아(음수로) 져야 해요. 곧 가짜는 밀어내요."),
  check("σ(2) 에 가장 가까운 값은? (슬라이드 표)", ["0.12", "0.50", "0.88"], 2,
        T("sig") + " 표에서 x=2 일 때 0.88, x=0 일 때 0.50, x=-2 일 때 0.12 예요."),
  english("답안에 쓸 문장",
   "네거티브 샘플링(Negative Sampling)은 소프트맥스(Softmax) 분모의 어휘 전체 내적을 피하려고, 진짜 문맥 단어 1개와 무작위로 뽑은 가짜 단어 k개를 가려내는 이진 분류로 바꾼 방법이다.",
   "진짜 짝은 σ(u^T v)를, 가짜 짝은 σ(-u^T v)를 키우고, 가짜는 빈도의 3/4 제곱 비율로 뽑아요.",
   "소프트맥스 무거움 → 진짜 1 대 가짜 k → 시그모이드 → freq^(3/4)"),
  warn("헷갈리기 쉬운 점",
   "가짜 항에는 내적 앞에 마이너스가 붙어요: σ(-u_k^T v_c). 빼먹으면 가짜를 끌어당기는 식이 돼요.",
   "3/4 제곱은 드문 단어를 '조금 더' 뽑히게 해요. 흔한 단어를 아예 빼는 게 아니에요."),
 ]})

# ================= p.39 =================
S.append({"p": 39, "title": "네거티브 샘플링 그림: 당기고 밀기",
 "terms": [EN(k) for k in ["ns", "center", "context", "emb", "vocab", "wv", "w2v"]],
 "pass1": [
  figure("진짜 이웃은 당기고, 가짜는 밀어요", FIG_NS,
         "banking 옆에 실제로 나온 crises 는 가까이, 아무렇게나 뽑은 aardvark, pizza, the 는 멀리", 2),
  analogy("지도 좌표 옮기기",
          "단어마다 지도 위에 집이 있어요. banking 과 실제로 자주 어울리는 crises 는 집을 조금 가깝게, 우연히 뽑힌 pizza 는 조금 멀게 옮겨요. 이걸 수십억 번 되풀이하면 동네가 생겨요.",
          [["지도 위의 집 위치", T("wv")], ["자주 어울리는 이웃", "진짜 " + T("context")], ["우연히 뽑힌 남", "가짜(negative) 단어"]]),
 ],
 "pass2": [
  compare("영어 문장 → 우리말 뜻", ["슬라이드 영어", "우리말 뜻"], [
   ["Pull the real neighbor \"crises\" toward \"banking\"", "진짜 이웃 crises 를 banking 쪽으로 당겨요"],
   ["push the random words away", "무작위로 뽑은 단어는 밀어내요"],
   ["positive / negative", "진짜 짝 / 가짜 짝"],
   ["push closer / push apart in embedding space", "임베딩 공간에서 가깝게 / 멀게"],
   ["repeat a billion times", "이걸 수십억 번 되풀이해요"]]),
  points("용어 하나씩",
   T("center") + ": 지금 배우는 가운데 단어(banking)",
   T("context") + ": 창 안에 실제로 나온 이웃(crises)",
   T("emb") + ": 단어의 지도 좌표. '임베딩 공간'은 그 지도예요",
   T("ns") + ": 어휘 전체 대신 가짜 몇 개만 골라 밀어내요"),
  check("그림에서 crises 는 banking 에 대해 어떤 단어인가요?",
        ["실제로 옆에 나온 진짜 문맥 단어(positive)", "무작위로 뽑은 가짜 단어(negative)", "중심 단어"], 0,
        "초록 상자 crises 가 positive, 빨간 aardvark, pizza, the 가 negative 예요."),
 ],
 "pass3": [
  look("그림 짚어 읽기",
   box(222, 365, 455, 452, "banking (center word): 지금 배우는 중심 단어"),
   box(603, 283, 1070, 347, "crises (positive): 진짜 문맥 단어 → 임베딩 공간에서 가깝게"),
   box(603, 363, 1090, 530, "aardvark, pizza, the (negative): 무작위 가짜 단어 → 멀게"),
   box(225, 470, 486, 570, "모든 |V| 단어 대신 k-1 개 가짜와만 비교. 예 k=5 → 진짜 1 + 가짜 4"),
   box(330, 678, 1075, 710, "진짜 이웃은 당기고 무작위 단어는 밀기, 수십억 번 반복")),
  points("당기고 밀면 벡터가 어떻게 바뀌나",
   "당기기: banking 벡터와 crises 벡터의 " + T("dot") + "이 커져요 → 화살표가 같은 쪽을 봐요",
   "밀기: banking 과 pizza 의 내적이 작아져요 → 화살표가 다른 쪽을 봐요",
   "the 처럼 흔한 단어도 가짜로 뽑혀 밀려요. 흔할수록 자주 뽑혀요(3/4 제곱으로 조금 누그러뜨려요)"),
  prof(MON2,
   "뱅킹의 문맥 단어가 크라이시스였으면, 크라이시스의 확률 p 는 올리고,",
   "뱅킹과 아무 상관 없는 멀리 떨어진 단어를 아무거나 뽑아 와서 그 확률은 낮추는 방법이라고 설명했어요.",
   "이렇게 하면 word2vec 학습 자체가 굉장히 편해진다고 했어요."),
  bg("기초 다지기 2단원 (내적과 코사인 유사도)",
     "내적은 두 화살표가 같은 쪽을 볼수록 커져요. '당긴다' 는 내적을 키운다는 뜻이에요."),
 ],
 "pass4": [
  check("그림 속 상자처럼 k=5 라고 할 때 비교하는 단어는?", ["진짜 1 + 가짜 4", "진짜 5 + 가짜 0", "어휘 전체"], 0,
        "그림의 상자에 'k = 5 ⇒ 1 positive + 4 negative' 라고 적혀 있어요."),
  english("답안에 쓸 문장",
   "네거티브 샘플링은 중심 단어와 실제 문맥 단어의 벡터는 가깝게 당기고, 무작위로 뽑은 가짜 단어의 벡터는 멀리 밀어내는 과정을 반복한다.",
   "당기기 = 내적 키우기, 밀기 = 내적 줄이기.", "진짜는 당기고, 가짜는 민다"),
  warn("k 의 뜻이 두 쪽에서 달라요",
   "p.38 식은 진짜 1개 + 가짜 K개(Σ k=1..K)예요. p.39 그림 상자는 k 를 '전체 개수'로 써서 가짜가 k-1 개예요.",
   "시험에서는 '진짜 1개와 가짜 몇 개'라는 뜻만 정확히 쓰면 돼요. 실습의 negative=10 은 가짜 10개예요."),
 ]})

# ================= p.40 =================
S.append({"p": 40, "title": "Skip-gram 과 CBOW",
 "terms": [EN(k) for k in ["sg", "cbow", "center", "context", "window", "w2v", "corpus"]],
 "pass1": [
  figure("같은 가족, 반대 방향 화살표", FIG_SGCB,
         "Skip-gram 은 중심 단어로 이웃을, CBOW 는 이웃들로 중심 단어를 맞혀요", 2),
  say(T("w2v") + "에는 두 가지 방식이 있어요.",
      T("sg") + "은 가운데 단어로 주변을 맞히고, " + T("cbow") + "는 주변으로 가운데를 맞혀요.",
      "화살표 방향만 반대이고 기본 생각은 같아요."),
 ],
 "pass2": [
  compare("영어 문장 → 우리말 뜻", ["슬라이드 영어", "우리말 뜻"], [
   ["Skip-gram: predict context from center", "Skip-gram: 중심 단어로 문맥 단어 맞히기"],
   ["CBOW: predict center from context", "CBOW: 문맥 단어로 중심 단어 맞히기"],
   ["better for rare words & small data", "드문 단어, 작은 데이터에 더 좋아요"],
   ["faster, better for frequent words", "더 빠르고, 자주 나오는 단어에 더 좋아요"],
   ["Same family, opposite arrows", "같은 가족, 반대 화살표"]]),
  compare("두 방식 한눈에", ["항목", T("sg"), T("cbow")], [
   ["맞히는 것", "주변 " + T("context"), "가운데 " + T("center")],
   ["보는 것", "중심 단어 1개", "창 안의 문맥 단어들"],
   ["확률", "P(문맥 | 중심)", "P(중심 | 문맥)"],
   ["강점", "드문 단어, 작은 데이터", "빠름, 자주 나오는 단어"],
   ["이 수업", "기본값(논문도)", "비교용"]]),
  check("'turning, into, crises, problems 를 보고 banking 을 맞힌다'는 어느 방식인가요?",
        ["Skip-gram", "CBOW"], 1,
        "주변 " + T("context") + "로 가운데 " + T("center") + "를 맞히면 " + T("cbow") + "예요."),
 ],
 "pass3": [
  look("그림 짚어 읽기",
   box(212, 212, 662, 275, "Skip-gram: 중심 단어가 주어지면 주변 문맥 단어를 맞혀요."),
   box(242, 280, 622, 505, "banking(w_t)에서 problems(w_t-2), turning(w_t-1), into(w_t+1), crises(w_t+2)로 화살표 4개"),
   box(245, 518, 632, 585, "Maximize P(context word | center word): 창 안 문맥 단어마다 확률을 크게"),
   box(708, 212, 1158, 275, "CBOW: 주변 문맥 단어가 주어지면 중심 단어를 맞혀요."),
   box(738, 518, 1125, 585, "Maximize P(center word | context words): 문맥 전체로 중심 단어 확률을 크게"),
   box(105, 590, 1210, 625, "Skip-gram 은 드문 단어, 작은 데이터에 좋고 이 수업의 기본값. CBOW 는 빠르고 흔한 단어에 좋아요.")),
  prof(MON2,
   "Skip-gram 은 중심 단어 한 번으로 윈도우만큼 학습 스텝이 생기고, CBOW 는 윈도우를 뭉쳐서 한 번에 스텝이 생긴다고 했어요.",
   "그래서 데이터가 아주 많지 않으면 Skip-gram 이 유리하고, 말뭉치가 충분히 크고 자원이 넉넉하면 CBOW 가 더 좋은 성능을 보인다고 알려져 있다고 했어요.",
   "방향만 다를 뿐 word2vec 의 기본 개념은 같다고 했어요."),
  points("왜 Skip-gram 이 드문 단어에 강한가 (녹음 설명)",
   T("sg") + ": 중심 단어 하나가 나올 때마다 이웃 수만큼 학습 기회가 생겨요",
   T("cbow") + ": 이웃을 한데 뭉쳐 한 번만 배워요 → 빠르지만 드문 단어는 배울 기회가 적어요"),
  say("실습에서는 N2L p.19 에서 Word2Vec(..., sg=1) 로 Skip-gram 을 골라요. sg=0 이면 CBOW 예요."),
 ],
 "pass4": [
  check("말뭉치(Corpus)가 작고 드문 단어가 중요할 때 슬라이드가 권하는 방식은?", ["Skip-gram", "CBOW"], 0,
        "슬라이드: Skip-gram 은 better for rare words & small data."),
  english("답안에 쓸 문장",
   "Skip-gram 은 중심 단어로 주변 문맥 단어를 예측하고(P(문맥|중심)), CBOW 는 주변 문맥 단어로 중심 단어를 예측한다(P(중심|문맥)). Skip-gram 은 드문 단어와 작은 데이터에, CBOW 는 속도와 자주 나오는 단어에 유리하다.",
   "같은 word2vec 가족, 화살표만 반대.", "스킵은 가운데서 밖으로, CBOW 는 밖에서 가운데로"),
  warn("헷갈리기 쉬운 점",
   "CBOW 가 '더 좋은 방식'이라는 뜻이 아니에요. 빠르고 흔한 단어에 강할 뿐, 이 수업의 기본값은 Skip-gram 이에요.",
   "gensim 에서 sg=1 이 Skip-gram, sg=0 이 CBOW 예요. 숫자를 거꾸로 외우지 마세요."),
 ]})

# ================= p.41 =================
S.append({"p": 41, "title": "무엇이 떠오르나: 의미의 지도",
 "terms": [EN(k) for k in ["wv", "emb", "w2v", "ana", "dot", "cos", "sg", "param", "corpus", "tokzr", "oov"]],
 "pass1": [
  figure("문맥만 맞혔는데 의미 지도가 생겼어요", FIG_MAP,
         "왼쪽: 비슷한 단어끼리 모여요. 오른쪽: king 에서 man 을 빼고 woman 을 더하면 queen 근처", 3),
  analogy("단어의 지도 좌표",
          "지도에서 동물 단어는 한 동네, 음식 단어는 다른 동네에 모여 살아요. 그리고 '남자 집 → 왕 집' 으로 가는 길과 '여자 집 → 여왕 집' 으로 가는 길이 같은 방향, 같은 길이예요.",
          [["지도 위 집의 위치", T("wv")], ["같은 동네", "뜻이 비슷한 단어"], ["같은 방향의 길", "같은 관계(왕족 방향)"]]),
 ],
 "pass2": [
  compare("영어 문장 → 우리말 뜻", ["슬라이드 영어", "우리말 뜻"], [
   ["We only asked for \"context prediction\"", "우리는 '문맥 맞히기'만 시켰어요"],
   ["and got a map of meaning in vector space", "그런데 벡터 공간에 의미의 지도가 생겼어요"],
   ["similar words end up close together", "비슷한 단어는 결국 가까이 모여요"],
   ["king - man + woman ≈ queen", "왕 - 남자 + 여자 ≈ 여왕"],
   ["arithmetic on meaning, learned from raw text", "의미로 하는 셈, 날 글에서 배운 것"]]),
  points("무엇이 떠올랐나",
   "모임: cat, dog, 고양이, 강아지 / pizza, kimchi, 사과 / happy, glad, 기쁘다",
   "방향: man → king 화살표와 woman → queen 화살표가 거의 평행해요(royalty direction)",
   "사람은 뜻을 알려 주지 않았어요. " + T("param") + " θ(모든 단어 벡터)를 문맥 맞히기로만 고쳤을 뿐이에요",
   T("ana") + ": 이런 벡터 셈으로 'man 대 woman 은 king 대 ?' 를 풀어요"),
  check("'의미 지도'는 어떻게 생겼나요?",
        ["사람이 단어 뜻을 하나하나 알려 줘서", "문맥 단어를 맞히도록 학습만 시켰더니 저절로", "사전(WordNet)을 복사해서"], 1,
        "슬라이드: We only asked for context prediction. 뜻은 알려 주지 않았어요."),
 ],
 "pass3": [
  look("그림 짚어 읽기",
   box(80, 152, 925, 190, "'문맥 맞히기'만 시켰는데 벡터 공간에 의미 지도가 생겼어요."),
   box(160, 255, 680, 550, "비슷한 단어끼리 가까이: 동물(파랑), 음식(주황), 기쁨(초록). 한국어와 영어가 같은 동네에"),
   box(720, 255, 1240, 550, "king - man + woman ≈ queen: 두 빨간 화살표가 같은 '왕족 방향'"),
   box(340, 678, 1062, 710, "의미로 하는 셈, 날 글에서 배운 것")),
  steps("손계산: 2차원 장난감 벡터로 king - man + woman",
   ["king - man = (4-1, 1-1) = (3, 0)",
    "(3, 0) + woman = (3+1, 0+3) = (4, 3)",
    "(4, 3) 은 queen = (4, 3) 과 똑같아요 → 코사인 1.00",
    "비교: (4,3) 과 woman (1,3) 의 코사인 = 13 / (5 x √10) ≈ 0.82",
    "비교: (4,3) 과 king (4,1) 의 코사인 = 19 / (5 x √17) ≈ 0.92 → 가장 가까운 건 queen"],
   "king - man + woman = (4, 3) = queen",
   given="man = (1, 1), woman = (1, 3), king = (4, 1), queen = (4, 3). 둘째 칸이 '여성 방향'"),
  prof(MON2,
   "뜻을 알려 주지 않고 문맥 단어 기준으로 우도를 높이는 방향으로만 θ 를 조금씩 고쳤는데, 비슷한 것끼리 클러스터가 생긴다고 했어요.",
   "king 에는 '남자이면서 통치자'라는 개념이 녹아 있어서, 의미로 산수 계산이 가능해졌다고 했어요.",
   "실습 스포일러로, 실습에서 해 보면 마음처럼 안 될 것이라고 미리 말했어요."),
  prof(MON3,
   "실습(띄어쓰기로만 자른 영화 리뷰)에서 왕 - 남자 + 여자 를 해 보니 이상한 단어가 나왔어요.",
   "이유: 띄어쓰기로만 해서 " + T("tokz") + "가 나빴고, 말뭉치가 너무 적었기 때문이라고 했어요.",
   "여왕이 나오려면 " + T("bpe") + " " + T("tokzr") + "를 잘 짜고, 큰 말뭉치로 학습해야 한다고 했어요."),
  say("실습에서는 N2L p.23 에서 most_similar(positive=[\"여자\", \"왕\"], negative=[\"남자\"]) 로 이 셈을 해 봐요.",
      "N2L p.25 에서는 PCA 로 60 개 단어를 2차원에 찍어 모이는지 봐요."),
 ],
 "pass4": [
  check("king - man + woman 을 장난감 벡터 man=(1,1), woman=(1,3), king=(4,1) 로 계산하면?",
        ["(4, 3)", "(2, 3)", "(6, 5)"], 0,
        "(4,1) - (1,1) + (1,3) = (4, 3). 같은 자리끼리 빼고 더해요."),
  english("답안에 쓸 문장",
   "word2vec 은 문맥 단어 예측만 학습했는데도 비슷한 단어가 가까이 모이고, king - man + woman ≈ queen 처럼 의미 관계가 일정한 벡터 차이로 나타난다.",
   "문맥 맞히기 → 의미 지도(모임 + 방향).", "모이고, 평행하다"),
  warn("헷갈리기 쉬운 점",
   "결과는 queen 과 '정확히 같다'가 아니라 '가장 가깝다(≈)'예요. 실제로는 코사인 유사도가 가장 큰 단어를 골라요.",
   "작은 말뭉치, 나쁜 " + T("tokz") + "로는 실습처럼 엉뚱한 답이 나와요. 말뭉치에 없는 단어는 " + T("oov") + "라 셈조차 못 해요."),
 ]})

# ================= p.42 =================
S.append({"p": 42, "title": "4부 구분: 세기, GloVe, 평가",
 "terms": [EN(k) for k in ["cooc", "glove", "intr", "extr", "wv"]],
 "pass1": [
  say("4부예요: 'Counting, GloVe & Evaluation'.",
      "벡터로 가는 또 다른 길(세기, " + T("glove") + ")과,",
      "만든 " + T("wv") + "가 좋은지 재는 법(" + T("intr") + ", " + T("extr") + ")을 배워요.",
      "교수님은 이 부분은 '가볍게 들으면 된다'고 했어요."),
 ],
 "pass2": [], "pass3": [], "pass4": []})

# ================= p.43 =================
S.append({"p": 43, "title": "그냥 세면 안 될까?",
 "terms": [EN(k) for k in ["cooc", "corpus", "window", "w2v", "dist", "vocab", "context"]],
 "pass1": [
  figure("말뭉치를 한 번 세면 표가 나와요", FIG_COUNT,
         "옆에 함께 나온 횟수를 센 동시 발생 행렬. 정보는 같지만 모양이 불편해요", 2),
  say(T("w2v") + "는 " + T("corpus") + "를 수십 바퀴 돌며 맞히기 게임을 해요.",
      "'그냥 한 번 세면 되지 않나?' 라는 반론에서 나온 게 " + T("cooc") + "이에요."),
 ],
 "pass2": [
  compare("영어 문장 → 우리말 뜻", ["슬라이드 영어", "우리말 뜻"], [
   ["Isn't looping over the corpus dozens of times weird?", "말뭉치를 수십 번 도는 건 이상하지 않나요?"],
   ["Why not just count co-occurrences once?", "함께 나온 횟수를 한 번만 세면 안 되나요?"],
   ["Each entry (i, j) counts how often word i and word j appear within a context window", "(i, j) 칸 = 단어 i 와 j 가 한 창 안에 함께 나온 횟수"],
   ["The matrix is symmetric", "표는 대각선 기준으로 대칭이에요((i,j) = (j,i))"],
   ["the same information, in a very inconvenient shape", "같은 정보, 매우 불편한 모양"]]),
  points("용어 하나씩",
   T("cooc") + ": 행 = 대상 단어, 열 = 문맥 단어, 칸 = 함께 나온 횟수",
   T("window") + ": 몇 칸 옆까지 '함께 나왔다'고 볼지 정하는 창",
   T("dist") + ": 친구를 보면 그 사람을 안다. 세기도 예측도 이 생각에서 출발해요"),
  check("표에서 I 행, like 열의 값 2 는 무슨 뜻인가요?",
        ["I 와 like 가 창 안에서 함께 나온 횟수가 2번", "like 가 말뭉치에 2번 나왔다", "I 가 2번째 단어다"], 0,
        "(i, j) 칸은 두 단어가 한 " + T("window") + " 안에 함께 나온 횟수예요. 'I like' 가 두 문장에 나와요."),
 ],
 "pass3": [
  look("표 짚어 읽기",
   box(80, 152, 1035, 190, "말뭉치를 수십 번 도는 대신 한 번만 세면 안 될까?"),
   box(403, 222, 960, 268, "말뭉치: I like deep learning / I like NLP / I enjoy flying (세 문장)"),
   box(318, 300, 818, 628, "7 x 7 표: 행 = 대상 단어, 열 = 문맥 단어. 진할수록 많이 함께 나옴"),
   box(893, 358, 1060, 568, "(i, j) = 창 안에서 함께 나온 횟수(예 window size = 2). 표는 대칭"),
   box(333, 678, 1072, 710, "같은 정보, 매우 불편한 모양")),
  steps("손으로 세어 보기 (바로 옆 단어만)",
   ["문장 1 'I like deep learning': I-like, like-deep, deep-learning",
    "문장 2 'I like NLP': I-like, like-NLP",
    "문장 3 'I enjoy flying': I-enjoy, enjoy-flying",
    "I-like 는 문장 1, 2 에서 → 2번, I-enjoy 는 1번",
    "단어 종류: I, like, enjoy, deep, learning, NLP, flying → 7개라 7 x 7 표"],
   "I 행 = [0, 2, 1, 0, 0, 0, 0] (슬라이드 표와 같아요)"),
  prof(MON2,
   "어휘가 10만이면 행이 10만, 열도 거의 10만이 돼야 한다고 했어요.",
   "피자와 뱅킹이 한 창 안에 함께 나올 일은 거의 없어서 그 칸은 0이에요.",
   "그래서 10만 x 10만 표가 거의 다 0인 희소한(sparse) 행렬이 된다, 이게 '불편한 모양'이에요."),
  bg("기초 다지기 3단원 (행렬과 행렬 곱, shape)",
     "행렬은 표 모양 숫자예요. 이 표의 shape 은 (어휘 크기, 어휘 크기) 예요."),
 ],
 "pass4": [
  check("어휘가 10만 개일 때 동시 발생 행렬의 문제로 가장 알맞은 것은?",
        ["10만 x 10만으로 매우 크고 대부분 0이다", "음수가 너무 많다", "대칭이 아니다"], 0,
        "같은 정보를 담지만 크고 희소해서 '불편한 모양'이에요."),
  english("답안에 쓸 문장",
   "동시 발생 행렬(Co-occurrence Matrix)은 말뭉치에서 두 단어가 윈도우 안에 함께 나온 횟수를 센 표로, word2vec 과 같은 정보를 담지만 어휘 크기 x 어휘 크기로 매우 크고 희소하다.",
   "세기도 분포 가설에서 출발해요.", "같은 정보, 불편한 모양"),
  warn("슬라이드 표의 창 크기",
   "설명 상자에는 '예 window size = 2' 라고 적혀 있지만, 표의 숫자는 바로 옆 단어(창 1)만 센 값과 같아요.",
   "창을 2로 세면 I-deep 이 1 이 되어야 하는데 표는 0이에요. 시험에서 직접 셀 때는 문제에 준 창 크기를 따르세요."),
 ]})

# ================= p.44 =================
S.append({"p": 44, "title": "세기에서 벡터로: SVD 와 보정 요령",
 "terms": [EN(k) for k in ["svd", "lsa", "cooc", "func", "wv", "w2v", "vocab"]],
 "pass1": [
  figure("큰 표를 쪼개 작은 벡터로", FIG_SVD,
         "특이값 분해로 거대한 표에서 중요한 방향 k 개만 남겨요", 2),
  analogy("지도 좌표로 줄이기",
          "10만 칸짜리 긴 주소(대부분 0)는 쓰기 불편해요. 중요한 방향 몇 개만 골라 '위도, 경도' 같은 짧은 좌표로 바꾸면 지도에 찍을 수 있어요.",
          [["10만 칸짜리 긴 주소", T("cooc") + "의 한 행"], ["중요한 방향 몇 개", "위쪽 k 개 특이값"], ["짧은 좌표", "촘촘한 " + T("wv")]]),
 ],
 "pass2": [
  compare("영어 문장 → 우리말 뜻", ["슬라이드 영어", "우리말 뜻"], [
   ["run SVD on the co-occurrence matrix X, keep the top k dims", "표 X 에 SVD 를 하고 위쪽 k 차원만 남겨요"],
   ["dense low-dim vectors", "촘촘한 저차원 벡터"],
   ["function words (the, of) dominate everything", "the, of 같은 기능어가 모든 걸 지배해요"],
   ["counting vs prediction: two camps running in parallel until 2014", "세기 대 예측: 2014년까지 나란히 달린 두 진영"],
   ["Counting works too, once you beat the counts into shape", "세기도 돼요, 숫자를 잘 다듬기만 하면"]]),
  points("용어 하나씩",
   T("svd") + ": 큰 표를 세 행렬(U, Σ, V)로 쪼개고 중요한 k 개만 남기기",
   T("lsa") + ": 이 고전적인 세기 + SVD 가족의 이름",
   T("func") + ": the, of 처럼 뜻은 적고 어디에나 나오는 단어",
   "sparse(희소) → dense(촘촘): 0 이 가득한 긴 벡터 → 짧고 꽉 찬 벡터"),
  check("그냥 센 숫자(raw counts)가 잘 안 되는 이유로 슬라이드가 든 것은?",
        ["the, of 같은 기능어가 모든 걸 지배해서", "숫자가 음수여서", "표가 너무 작아서"], 0,
        T("func") + "는 모든 문장에 나와서 어떤 단어 행을 봐도 크게 세어져요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
   box(80, 155, 1300, 190, "고전적인 길(LSA 가족): 표 X 에 SVD, 위쪽 k 차원 → 촘촘한 저차원 벡터"),
   box(80, 202, 890, 237, "그냥 센 숫자는 잘 안 돼요: 기능어(the, of)가 모든 걸 지배"),
   box(80, 250, 1125, 285, "보정: 횟수에 로그, min(X, 100) 으로 자르기, 기능어 무시, 가까운 단어에 더 큰 무게"),
   box(80, 298, 1010, 333, "잘 하면 괜찮은 벡터(COALS 등), 선형 의미 패턴도 나타나요"),
   box(80, 346, 970, 381, "세기 대 예측: 2014년까지 나란히 달린 두 진영"),
   box(378, 388, 995, 680, "X_ij = 문서 j 에 단어 i 가 나온 횟수(단어-문서 행렬). X ≈ U_k Σ_k V_k^T. car, automobile 이 k 차원 벡터로")),
  formula("잘린 SVD (슬라이드 상자)",
   r"X \approx U_k \Sigma_k V_k^\top",
   [(r"X", "센 숫자 표. 상자에서는 단어-문서 행렬(X_ij = 문서 j 의 단어 i 횟수)"),
    (r"U_k", "단어마다 k 개 숫자를 가진 행렬 → 이 행이 단어 벡터가 돼요"),
    (r"\Sigma_k", "중요도(특이값) 위쪽 k 개를 대각선에 둔 행렬"),
    (r"V_k^\top", "문서(또는 문맥) 쪽 k 차원 행렬"),
    (r"\approx", "완전히 같지 않고 '비슷하게' 되살려요. 나머지는 버렸으니까요")],
   "큰 표를 중요한 방향 k 개로만 요약하면, 희소한 긴 벡터가 촘촘한 짧은 벡터로 바뀌어요."),
  steps("보정 요령 두 개를 숫자로",
   ["clip: min(X, 100). the 와 함께 250번 → min(250, 100) = 100",
    "드문 짝 7번 → min(7, 100) = 7 (그대로)",
    "log: log 100 ≈ 4.61, log 1000 ≈ 6.91",
    "횟수는 10배 차이인데 로그로는 약 2.3 차이뿐 → 흔한 짝이 덜 지배해요"],
   "자르고 로그를 씌우면 기능어의 큰 숫자가 누그러져요"),
  prof(MON2,
   "SVD 는 표를 U, 시그마, V 세 행렬로 쪼개고, 가운데 시그마에 유의미한 정보가 담겨 있다고 가정한다고 했어요.",
   "그래서 숨은 의미를 표현하는 잠재 의미 분석(LSA)이라고도 한다고 했어요.",
   "the 는 모든 문장에 나와 계속 세어지니, 100번 넘으면 100에서 자르고 로그를 씌워 보정한다고 했어요."),
  bg("기초 다지기 3단원 (행렬과 행렬 곱, shape)",
     "(10만, 10만) 표를 (10만, k) 행렬로 바꾸면, 단어 하나가 k 개 숫자로 줄어요."),
 ],
 "pass4": [
  check("SVD 로 얻는 벡터의 특징은?", ["희소하고 긴 벡터", "촘촘하고 짧은(저차원) 벡터", "원-핫 벡터"], 1,
        "슬라이드: dense low-dim vectors. 위쪽 k 차원만 남겨요."),
  english("답안에 쓸 문장",
   "고전적인 세기 방법(LSA)은 동시 발생 행렬에 특이값 분해(SVD)를 적용해 위쪽 k 개 차원만 남겨 촘촘한 저차원 단어 벡터를 얻으며, 기능어가 지배하는 문제는 로그, min(X,100) 클리핑, 기능어 제거 등으로 보정한다.",
   "세기 + SVD + 보정. 이 가족 이름이 " + T("lsa") + "예요.", "센다 → 쪼갠다 → 다듬는다"),
  warn("헷갈리기 쉬운 점",
   "슬라이드 윗글은 동시 발생 행렬(단어 x 단어)에, 아래 상자는 단어-문서 행렬(단어 x 문서)에 SVD 를 해요. 둘 다 '센 표를 SVD 로 줄인다'는 같은 생각이에요.",
   "세기 방식(" + T("lsa") + ")도 잘 다듬으면 선형 의미 패턴(방향)이 나와요. 예측 방식만의 특권이 아니에요."),
 ]})

# ================= p.45 =================
S.append({"p": 45, "title": "GloVe: 두 길의 장점을 합치다",
 "terms": [EN(k) for k in ["glove", "cooc", "dot", "wf", "w2v", "corpus", "loss", "emb"]],
 "pass1": [
  figure("세기 + 예측 = GloVe", FIG_GLOVE,
         "전체 말뭉치를 센 통계와, 내적으로 맞히는 학습을 한 식에 합쳐요", 3),
  say(T("glove") + "는 '세기' 길과 '예측' 길을 합친 방법이에요.",
      "두 단어 벡터의 " + T("dot") + "이 함께 나온 횟수(의 로그)를 맞히도록 배워요.",
      "교수님은 수식은 시험에 내지 않겠다고 했어요. 개념만 잡아요."),
 ],
 "pass2": [
  compare("영어 문장 → 우리말 뜻", ["슬라이드 영어", "우리말 뜻"], [
   ["GloVe: Global Vectors (Pennington, Socher & Manning 2014)", "전체(글로벌) 통계를 쓰는 벡터, 2014년"],
   ["meaning components live in ratios of co-occurrence probabilities", "의미 성분은 함께 나올 확률의 '비율'에 들어 있어요"],
   ["make the dot product predict the log count", "내적이 횟수의 로그를 맞히게 해요"],
   ["Global statistics (counting) + trained optimization (prediction)", "전체 통계(세기) + 학습(예측)"],
   ["practically tied in quality", "word2vec 과 품질은 사실상 비슷해요"]]),
  points("ice / steam 비율 이야기 (뜻만)",
   "ice(얼음)는 solid(고체)와, steam(증기)은 gas(기체)와 자주 함께 나와요",
   "그래서 'solid 와 함께 나올 확률'을 ice 와 steam 사이에서 나눈 비율이 둘을 가르는 의미 성분이에요",
   T("glove") + "는 이 비율 정보가 벡터에 담기도록 설계했어요"),
  check("GloVe 에서 '세기'에 해당하는 것은?",
        ["전체 말뭉치에서 센 동시 발생 횟수 X_ij", "무작위로 뽑은 가짜 단어", "CBOW 의 문맥 평균"], 0,
        T("glove") + "는 먼저 말뭉치 전체에서 " + T("cooc") + "을 세고, 그 로그를 내적으로 맞혀요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
   box(80, 152, 710, 190, "GloVe (Pennington, Socher & Manning 2014): Global Vectors"),
   box(80, 195, 1330, 258, "Insight: 의미 성분은 동시 발생 확률의 비율에. ice/steam 을 가르는 건 solid, gas 와의 비율"),
   box(220, 330, 895, 470, "GloVe 목적 함수 J. 괄호 안은 예측, log X_ij 는 관찰"),
   box(290, 470, 870, 555, "f(X_ij) = 얼마나 믿을까? / 괄호 속 = 예측 / log X_ij = 관찰"),
   box(1045, 295, 1305, 492, "가중치 함수 f(x): x < x_max 면 (x/x_max)^α, 아니면 1. x_max = 100, α = 3/4"),
   box(270, 678, 1130, 710, "word2vec 과 GloVe: 2013~2018 NLP 표준 재료, 품질은 사실상 비슷")),
  formula("GloVe 목적 함수 (참고용, 시험 X)",
   r"J = \sum_{i,j=1}^{V} f(X_{ij}) \left( w_i^\top \tilde{w}_j + b_i + \tilde{b}_j - \log X_{ij} \right)^2",
   [(r"X_{ij}", "단어 i 와 j 가 함께 나온 횟수(세기, 관찰)"),
    (r"w_i^\top \tilde{w}_j", "두 단어 벡터의 내적(예측)"),
    (r"b_i,\ \tilde{b}_j", "단어마다 붙는 고정값(편향 항). the 처럼 그냥 자주 나오는 정도를 흡수"),
    (r"\log X_{ij}", "관찰: 횟수에 로그를 씌운 값"),
    (r"(\ \cdot\ )^2", "예측 - 관찰 차이의 제곱 = 벌점(" + T("loss") + ")"),
    (r"f(X_{ij})", "이 짝을 얼마나 믿을지 정하는 가중치 함수")],
   "예측(내적)이 관찰(log 횟수)에 가까워지도록 벌점을 줄이되, 짝마다 f 로 믿는 정도를 달리해요."),
  steps("가중치 함수 f 맛보기 (참고)",
   ["f(1) = (1/100)^(3/4) ≈ 0.032 → 한 번 나온 짝은 거의 안 믿어요",
    "f(10) = (10/100)^(3/4) ≈ 0.178",
    "f(100) = 1, f(250) = 1 → 100 이상은 똑같이 1 로 잘라요",
    "그래서 너무 흔한 짝이 벌점을 혼자 지배하지 못해요"],
   "드문 짝은 적게, 흔한 짝도 1 까지만 믿어요",
   given="x_max = 100, α = 3/4 (슬라이드 값)"),
  prof(MON2,
   "지금 내용은 여러분이 100% 이해할 거라고 생각하지 않는다, 굉장히 어려운 거고 수업은 하겠지만 시험에 내거나 그러지는 않겠다고 했어요.",
   "f 쪽이 세기(카운팅), 괄호 안이 word2vec 같은 예측이고, 괄호 안은 '관찰 빼기 예측' 모양이라고 설명했어요.",
   "2014년에 나와 2019년 BERT 전까지 거의 모든 NLP 에서 많이 썼고, 요즘은 많이 안 쓰인다고 했어요."),
 ],
 "pass4": [
  check("GloVe 에 대해 맞는 것은?",
        ["세기(전체 통계)와 예측(학습)을 합친 방법이다", "문맥 단어를 하나도 쓰지 않는다", "word2vec 보다 품질이 훨씬 나쁘다"], 0,
        "슬라이드: Global statistics (counting) + trained optimization (prediction). 품질은 word2vec 과 사실상 비슷해요."),
  english("답안에 쓸 문장",
   "GloVe 는 말뭉치 전체의 동시 발생 통계(세기)와 학습 기반 최적화(예측)를 결합해, 두 단어 벡터의 내적이 동시 발생 횟수의 로그를 예측하도록 학습하는 단어 벡터 방법이다.",
   "세기 + 예측, 내적 ≈ log 횟수.", "Global Vectors = 전체 통계 + 내적 예측"),
  warn("시험 범위 주의",
   "교수님: GloVe 수식은 '시험에 내거나 그러지는 않겠습니다'. 식을 외우기보다 '세기 + 예측을 합쳤다', '내적이 log 횟수를 맞힌다' 는 개념만 확실히 해요.",
   "가중치 함수 f 의 α = 3/4 와 네거티브 샘플링의 freq^(3/4) 는 다른 곳에 쓰인 숫자예요. 섞지 마세요."),
 ]})

# ================= p.46 =================
S.append({"p": 46, "title": "GloVe 공간의 모습",
 "terms": [EN(k) for k in ["glove", "wv", "ana", "emb", "w2v"]],
 "pass1": [
  say("학습된 " + T("glove") + " 공간에서는 같은 관계가 같은 화살표로 나타나요.",
      "man → woman, king → queen, brother → sister, sir → madam 이 모두 평행해요.",
      "뜻이 지도 위의 '방향'이 된 거예요."),
  analogy("지도 위의 같은 길",
          "여러 동네에서 '남자 집에서 여자 집으로 가는 길'을 그리면, 방향과 길이가 거의 같아요. 성별이라는 뜻 하나가 지도 위의 일정한 걸음 하나가 된 거예요.",
          [["집 위치", T("wv")], ["같은 방향, 같은 길이의 걸음", "일정한 벡터 차이(성별 성분)"]]),
 ],
 "pass2": [
  compare("영어 문장 → 우리말 뜻", ["슬라이드 영어", "우리말 뜻"], [
   ["one semantic relation = one consistent vector difference", "의미 관계 하나 = 일정한 벡터 차이 하나"],
   ["one meaning component (gender)", "의미 성분 하나(성별)"],
   ["Semantic and syntactic regularities", "의미 규칙과 문법 규칙"],
   ["captured as pure geometry", "순수한 기하(모양)로 담겼어요"]]),
  points("용어 하나씩",
   "의미 관계(semantic): 남자-여자, 수도-나라 같은 뜻의 관계",
   "문법 관계(syntactic): slow-slower-slowest 같은 비교급, 동사 시제 같은 형태 관계",
   T("ana") + ": 이 평행한 화살표 덕분에 벡터 셈으로 풀 수 있어요"),
  check("그림에서 네 개의 점선 화살표가 거의 평행하다는 것은 무슨 뜻인가요?",
        ["성별이라는 같은 관계가 같은 벡터 차이로 나타난다", "네 단어 쌍의 뜻이 모두 같다", "벡터 길이가 모두 0이다"], 0,
        "one semantic relation = one consistent vector difference."),
 ],
 "pass3": [
  look("그림 짚어 읽기",
   box(80, 152, 875, 190, "학습된 공간에서 의미 관계 하나 = 일정한 벡터 차이 하나"),
   box(238, 258, 1120, 282, "의미 성분 하나(성별) = 일정한 벡터 차이 (GloVe 식 시각화)"),
   box(320, 300, 1020, 560, "sir→madam, king→queen, brother→sister, man→woman: 방향과 길이가 거의 같아요"),
   box(400, 678, 1005, 710, "의미 규칙과 문법 규칙이 순수한 기하로")),
  steps("평행하다 = 차이가 같다 (장난감 벡터)",
   ["woman - man = (1-1, 3-1) = (0, 2)",
    "queen - king = (4-4, 3-1) = (0, 2)",
    "두 차이가 같아요 → 화살표가 평행하고 길이도 같아요",
    "그래서 king + (woman - man) = queen 이 돼요"],
   "성별 성분 = (0, 2) 한 걸음",
   given="p.41 과 같은 man=(1,1), woman=(1,3), king=(4,1), queen=(4,3)"),
  prof(MON2,
   "man → woman, king → queen, brother → sister 가 같은 의미 관계인데 화살표 방향과 길이가 거의 같다고 했어요.",
   "slow, slower, slowest 같은 비교급 방향, 동사 시제 방향도 GloVe 벡터로 그려 보면 굉장히 평행하게 나타난다고 했어요."),
  bg("기초 다지기 1단원 (숫자 목록, 벡터)",
     "벡터 빼기는 같은 자리끼리 빼요. 두 점의 차이 벡터가 '한 점에서 다른 점으로 가는 화살표'예요."),
 ],
 "pass4": [
  check("다음 중 문법 관계(syntactic regularity)의 예는?", ["slow - slower - slowest", "king - queen", "Seoul - Korea"], 0,
        "비교급, 시제 같은 형태 관계가 문법 관계예요. king-queen 은 의미 관계예요."),
  english("답안에 쓸 문장",
   "학습된 GloVe 공간에서는 하나의 의미 관계가 일정한 벡터 차이로 나타나, man→woman 과 king→queen 같은 화살표가 거의 평행하다.",
   "관계 = 방향.", "같은 관계, 같은 화살표"),
  warn("헷갈리기 쉬운 점",
   "이 성질은 GloVe 만의 것이 아니에요. p.41 의 word2vec 에서도 같은 king - man + woman ≈ queen 이 나왔어요."),
 ]})

# ================= p.47 =================
S.append({"p": 47, "title": "단어 벡터 평가하기",
 "terms": [EN(k) for k in ["intr", "extr", "ana", "wsim", "ner", "cls", "wv", "emb"]],
 "pass1": [
  figure("평가의 두 길", FIG_EVAL,
         "벡터 자체를 바로 보는 내적 평가, 실제 과제에 넣어 보는 외적 평가", 3),
  compare("한 줄 비교", ["", T("intr"), T("extr")], [
   ["무엇을", "벡터 자체", "실제 과제 성능"],
   ["예", "유추, 유사도", T("ner") + ", 분류, 검색"],
   ["장점", "빠르고 문제 위치를 알려 줌", "진짜 중요한 값"],
   ["약점", "실제 성능과의 연결은 따로 증명", "느리고 어디가 문제인지 모름"]]),
 ],
 "pass2": [
  compare("영어 문장 → 우리말 뜻", ["슬라이드 영어", "우리말 뜻"], [
   ["The great dichotomy of NLP evaluation", "NLP 평가의 큰 두 갈래"],
   ["Intrinsic: evaluate the intermediate artifact itself", "내적: 중간 산출물(벡터) 자체를 평가"],
   ["Extrinsic: plug the vectors into a real task", "외적: 벡터를 실제 과제에 끼워 넣어 평가"],
   ["Evidence of good vectors = plausible intrinsics + real extrinsic gains", "좋은 벡터의 증거 = 그럴듯한 내적 결과 + 실제 외적 향상"],
   ["Fast-but-indirect vs slow-but-real, you always need both", "빠르지만 간접 대 느리지만 진짜, 늘 둘 다 필요"]]),
  points("용어 하나씩",
   T("intr") + ": 유추, 유사도처럼 벡터만 가지고 바로 재기",
   T("extr") + ": 벡터를 과제 모델에 넣어 최종 점수 재기",
   T("ner") + ": 글에서 사람, 장소 같은 이름 찾기",
   T("cls") + ": 글을 긍정/부정 같은 칸으로 나누기"),
  check("단어 벡터를 감정 분류 모델에 넣고 정확도가 올랐는지 보는 것은?", ["내적 평가", "외적 평가"], 1,
        "실제 과제(" + T("cls") + ")에 끼워 최종 성능을 재면 " + T("extr") + "예요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
   box(80, 155, 855, 190, "NLP 평가의 큰 두 갈래: 한 학기 내내 다시 쓰는 틀"),
   box(80, 200, 885, 270, "Intrinsic: 중간 산출물 자체(유추, 유사도). 빠르고 진단적, 실제 성능과의 연결은 따로 증명"),
   box(80, 280, 1150, 348, "Extrinsic: 실제 과제(NER, 분류, 검색)에 넣어 최종 성능. 진짜 중요하지만 느리고 문제 위치를 모름"),
   box(80, 360, 795, 395, "좋은 벡터의 증거 = 그럴듯한 내적 결과 + 실제 외적 향상"),
   box(430, 678, 975, 710, "빠르지만 간접 대 느리지만 진짜: 늘 둘 다 필요")),
  prof(MON2,
   "NLP 에서는 평가(evaluation)가 굉장히 중요하다고 했어요.",
   "내적 평가: king - man + woman 이 정말 queen 이 되면 임베딩이 잘 학습됐다고 보는 것.",
   "외적 평가: 그 벡터로 실제 문서 분류 같은 다운스트림 과제 성능이 좋은지 보는 것.",
   "뭐가 더 중요하냐 하면 '당연히 둘 다 중요합니다' 라고 했어요."),
  points("왜 둘 다 필요한가",
   "내적만 좋고 외적이 그대로면: 유추 문제만 잘 풀고 " + T("ner") + " 같은 실제 과제엔 도움이 안 되는 벡터일 수 있어요",
   "외적만 보면: 점수가 나빠도 벡터 탓인지 과제 모델 탓인지 몰라요",
   "그래서 둘을 함께 보여야 '좋은 벡터'라는 증거가 돼요"),
 ],
 "pass4": [
  check("외적 평가(Extrinsic Evaluation)의 약점으로 맞는 것은?",
        ["느리고, 문제가 어디에 있는지 알려 주지 못한다", "실제 성능과 아무 상관이 없다", "유추 문제만 풀 수 있다"], 0,
        "슬라이드: slow, and it can't tell you WHERE the problem is."),
  check("교수님이 내적 평가와 외적 평가 중 무엇이 더 중요하다고 했나요?",
        ["내적 평가", "외적 평가", "둘 다 중요"], 2, "녹음: '당연히 둘 다 중요합니다'."),
  english("답안에 쓸 문장",
   "내적 평가(Intrinsic Evaluation)는 유추, 유사도로 벡터 자체를 빠르게 진단하고, 외적 평가(Extrinsic Evaluation)는 NER, 분류 같은 실제 과제 성능을 재며, 둘 다 필요하다.",
   "빠르지만 간접 vs 느리지만 진짜.", "내적 = 벡터 자체, 외적 = 실제 과제"),
  warn("헷갈리기 쉬운 이름",
   "여기서 '내적 평가'의 '내적'은 Intrinsic(안쪽의)이에요. 벡터 곱셈의 " + T("dot") + "과 이름만 같고 다른 말이에요."),
 ]})

# ================= p.48 =================
S.append({"p": 48, "title": "내적 평가: 유추와 유사도",
 "terms": [EN(k) for k in ["intr", "ana", "wsim", "cos", "dot", "wv", "oov", "corpus", "tokz", "w2v"]],
 "pass1": [
  say(T("intr") + "의 대표 두 가지예요.",
      T("ana") + ": 'man 대 woman 은 king 대 ?' 를 벡터 셈으로 풀기.",
      T("wsim") + ": 사람이 매긴 비슷함 점수와 벡터의 비슷함이 같이 가는지 보기."),
  analogy("화살표가 같은 쪽을 보는지",
          "두 단어의 지도 좌표를 화살표로 그렸을 때 같은 쪽을 보면 비슷한 단어예요. 사람이 '호랑이와 고양이는 꽤 비슷해' 라고 한 쌍에서 화살표도 같은 쪽을 보면 좋은 벡터예요.",
          [["화살표가 같은 쪽을 보는 정도", T("cos")], ["사람이 매긴 비슷함 점수", "WordSim-353 점수(0~10)"]]),
 ],
 "pass2": [
  compare("영어 문장 → 우리말 뜻", ["슬라이드 영어", "우리말 뜻"], [
   ["Word analogy: a : b :: c : ?", "단어 유추: a 대 b 는 c 대 무엇?"],
   ["argmax cos(x, b - a + c)", "b - a + c 와 코사인이 가장 큰 단어 x 를 골라요"],
   ["correlation between human similarity ratings and vector cosine", "사람의 비슷함 점수와 벡터 코사인의 상관"],
   ["Korean counterparts exist too, we run in the lab", "한국어판도 있고, 실습에서 돌려요"],
   ["Assignment 1: you will run exactly these evaluations on your own vectors", "과제 1: 여러분 벡터로 바로 이 평가를 해요"]]),
  points("용어 하나씩",
   T("ana") + ": a : b :: c : ? 꼴의 문제",
   T("cos") + ": 두 화살표가 같은 쪽을 보는 정도, -1 ~ 1",
   "argmax: 값이 가장 큰 것을 고르라는 뜻",
   "상관(correlation): 한쪽이 크면 다른 쪽도 큰지 같이 움직이는 정도"),
  check("man : woman :: king : ? 에서 계산하는 벡터 b - a + c 는?",
        ["woman - man + king", "man - woman + king", "king - woman - man"], 0,
        "a = man, b = woman, c = king 이라 b - a + c = woman - man + king 이에요. p.41 의 king - man + woman 과 같아요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
   box(80, 152, 1015, 190, "단어 유추 a : b :: c : ? → argmax cos(x, b - a + c)"),
   box(155, 192, 1040, 218, "구글 유추 데이터: 의미(수도-나라 등) + 문법(비교급 등), 19,544 문항"),
   box(80, 232, 925, 268, "단어 유사도: 사람의 비슷함 점수와 벡터 코사인의 상관"),
   box(155, 270, 825, 298, "WordSim-353: tiger-cat 7.35, tiger-tiger 10, stock-jaguar 0.92, 353 쌍"),
   box(80, 310, 975, 346, "한국어판도 있어요(WordSim-353-ko, 한국어 유추). 실습에서 돌려요"),
   box(365, 678, 1040, 710, "과제 1: 여러분 벡터로 바로 이 평가를 해요")),
  formula("유추 풀이 규칙",
   r"x^* = \arg\max_{x} \cos(x,\ b - a + c)",
   [(r"a, b, c", "문제에 준 세 단어. man : woman :: king : ? 이면 a=man, b=woman, c=king"),
    (r"b - a + c", "관계(b - a)를 c 에 더한 목표 벡터"),
    (r"\cos(x, \cdot)", "후보 단어 x 의 벡터와 목표 벡터의 코사인 유사도"),
    (r"\arg\max_x", "코사인이 가장 큰 x 를 답으로 골라요")],
   "관계 화살표를 c 에 붙여 도착한 곳과 가장 같은 쪽을 보는 단어가 답이에요."),
  steps("손계산: 코사인 유사도",
   ["내적: 3x4 + 4x3 = 24",
    "길이: |a| = √(9+16) = 5, |b| = √(16+9) = 5",
    "cos = 24 / (5 x 5) = 0.96 → 거의 같은 쪽",
    "비교: (1,0) 과 (0,1) 은 내적 0 → cos = 0 (직각, 상관없음)"],
   "cos((3,4), (4,3)) = 0.96",
   given="a = (3, 4), b = (4, 3)"),
  steps("손계산: 유추 답 고르기",
   ["목표 = woman - man + king = (1,3) - (1,1) + (4,1) = (4, 3)",
    "후보 queen (4,3): cos = 1.00",
    "후보 king (4,1): cos ≈ 0.92, 후보 woman (1,3): cos ≈ 0.82",
    "가장 큰 queen 을 답으로 골라요"],
   "man : woman :: king : queen",
   given="man=(1,1), woman=(1,3), king=(4,1), queen=(4,3)"),
  prof(MON2,
   "WordSim-353 같은 데이터는 사람들에게 tiger 와 cat 이 얼마나 비슷한지 점수를 매기게 한 것이라고 했어요.",
   "사람 점수와 벡터 코사인의 상관을 피어슨 상관계수 같은 것으로 잰다고 했어요.",
   "다만 유사도 방식이 아주 좋은 방식은 아닐 수 있다고 덧붙였어요."),
  prof(MON3,
   "실습에서 영화-드라마 코사인 유사도는 0.568 로 조금 높은 편이었어요.",
   "영화-김치는 말뭉치(영화 리뷰)에 김치가 없어 " + T("oov") + "가 떴다고 했어요.",
   "좋은 벡터에는 토크나이저가 중요하고, 말뭉치가 커야 한다고 정리했어요."),
  say("실습에서는 N2L p.20 most_similar(이웃), p.21 similarity(유사도), p.23 왕 - 남자 + 여자(유추)로 이 평가를 해 봐요.",
      "p.22 에서는 단어가 어휘에 있는지와 몇 번 나왔는지(count)를 확인해요."),
  bg("기초 다지기 2단원 (내적과 코사인 유사도)",
     "cos = 내적 / (길이 x 길이). 길이는 각 숫자를 제곱해 더한 뒤 루트예요."),
 ],
 "pass4": [
  exam("예상 문제",
   "a = (3, 4), b = (4, 3) 의 코사인 유사도를 구하시오.",
   "두 화살표가 얼마나 같은 쪽을 보는지 숫자로 구해요.",
   ["내적 a^T b = 3x4 + 4x3 = 24", "|a| = 5, |b| = 5", "cos = 24 / 25 = 0.96"], "0.96"),
  check("WordSim-353 에서 사람이 매긴 점수가 가장 낮은 쌍은? (슬라이드)",
        ["tiger-cat", "tiger-tiger", "stock-jaguar"], 2,
        "tiger-tiger 10, tiger-cat 7.35, stock-jaguar 0.92 예요."),
  english("답안에 쓸 문장",
   "단어 유추(Word Analogy)는 a : b :: c : ? 에서 b - a + c 와 코사인 유사도가 가장 큰 단어를 고르는 평가이고, 단어 유사도 평가는 사람의 유사도 점수와 벡터 코사인 유사도의 상관을 잰다.",
   "유추 = 벡터 셈 + argmax cos, 유사도 = 사람 점수와의 상관.", "b - a + c, 그리고 상관"),
  warn("헷갈리기 쉬운 점",
   "b - a + c 의 순서: man : woman :: king : ? 이면 woman - man + king 이에요. a 를 빼고 b 를 더해요.",
   "유사도 평가는 코사인 값 자체가 아니라, 사람 점수와 '같이 움직이는지(상관)'를 봐요.",
   "과제와 이어지는 부분: 과제 1 에서 여러분 벡터로 이 평가를 한다고 슬라이드에 적혀 있어요."),
 ]})

# ================= p.49 =================
S.append({"p": 49, "title": "한계: 다의어와 편향",
 "terms": [EN(k) for k in ["poly", "bias", "static", "ctxemb", "wv", "corpus", "emb", "w2v"]],
 "pass1": [
  figure("'배' 벡터 하나에 세 뜻", FIG_POLY,
         "단어 하나에 벡터 하나라서, 여러 뜻이 뭉개진 평균이 돼요", 2),
  say("단어 벡터에는 두 가지 한계가 있어요.",
      "하나, " + T("poly") + ": '배' 처럼 뜻이 여럿이어도 벡터는 하나예요.",
      "둘, " + T("bias") + ": " + T("corpus") + "에 섞인 사회적 치우침까지 배워요."),
 ],
 "pass2": [
  compare("영어 문장 → 우리말 뜻", ["슬라이드 영어", "우리말 뜻"], [
   ["ONE vector per word", "단어 하나에 벡터 하나"],
   ["its vector is a mushy average", "그 벡터는 뭉개진 평균"],
   ["the fix is context-dependent vectors: contextual embeddings (BERT, week 5)", "해결책: 문맥에 따라 바뀌는 벡터(5주차 BERT)"],
   ["vectors learn the corpus, including the social biases soaked into it", "벡터는 말뭉치를 배워요, 스며든 사회적 편향까지"],
   ["Detection & mitigation are active research; the root problem is unsolved", "찾기와 줄이기는 연구 중, 뿌리는 아직 못 풀었어요"]]),
  points("용어 하나씩",
   T("poly") + ": 한 단어에 여러 뜻(배 = pear, ship, belly)",
   T("static") + ": 학습이 끝나면 문맥이 바뀌어도 그대로인 벡터(word2vec, GloVe)",
   T("ctxemb") + ": 문맥에 따라 벡터가 바뀌는 임베딩(5주차 BERT)",
   T("bias") + ": 말뭉치 속 사회적 치우침을 벡터가 그대로 배우는 것"),
  check("다의어 문제의 해결책으로 슬라이드가 든 것은?",
        ["문맥에 따라 바뀌는 벡터(문맥 임베딩, BERT)", "벡터 차원 늘리기", "네거티브 샘플링의 k 늘리기"], 0,
        "the fix is context-dependent vectors, contextual embeddings (BERT, week 5)."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
   box(80, 152, 1225, 190, "한계 1 다의어: 단어 하나에 벡터 하나. '배'는 배(과일), 배(선박), 배(신체). 벡터는 뭉개진 평균"),
   box(155, 192, 875, 220, "해결책: 문맥에 따라 바뀌는 벡터, 문맥 임베딩(BERT, 5주차)"),
   box(80, 232, 1012, 270, "한계 2 편향: man : programmer :: woman : homemaker, 실제 2016년 논문 제목"),
   box(155, 272, 772, 300, "벡터는 말뭉치를 배워요, 스며든 사회적 편향까지"),
   box(80, 315, 850, 350, "찾기와 줄이기는 활발한 연구 중, 뿌리 문제는 아직 못 풀었어요"),
   box(378, 678, 1028, 710, "벡터는 말뭉치를 배워요, 쓸모 있는 패턴도 못난 패턴도")),
  prof(MON2,
   "이 단어 벡터들은 한 번 θ 가 결정되면 더 이상 바뀌지 않는 정적 단어 벡터라고 했어요.",
   "'배'가 먹는 배인지, 몸의 배인지, 바다에 뜬 배인지는 주변 문맥이 정하는데, 정적 벡터로는 그게 어렵다고 했어요.",
   "편향은 알고리즘 문제가 아니라 말뭉치에 기반해 배우기 때문에 생긴다, 옛 말뭉치의 성 편향 때문에 woman 에 homemaker 가 나올 수 있다고 했어요."),
  points("정리: 두 한계의 원인",
   T("poly") + " → 원인: 단어마다 벡터가 딱 하나(정적) → 해결: " + T("ctxemb"),
   T("bias") + " → 원인: 말뭉치를 그대로 배움 → 찾고 줄이는 연구 중, 뿌리는 미해결"),
 ],
 "pass4": [
  check("man : programmer :: woman : homemaker 예시가 보여 주는 한계는?", ["다의어", "편향", "미등록 단어"], 1,
        "말뭉치에 스며든 사회적 " + T("bias") + "을 벡터가 그대로 배운 예예요."),
  english("답안에 쓸 문장",
   "정적 단어 벡터는 단어마다 벡터가 하나뿐이라 다의어(Polysemy)의 여러 뜻이 평균으로 뭉개지고(해결: BERT 같은 문맥 임베딩), 말뭉치를 그대로 배우므로 사회적 편향(Bias)까지 학습한다.",
   "한 단어 한 벡터 → 다의어, 말뭉치 그대로 → 편향.", "배는 하나, 편향은 말뭉치 탓"),
  warn("헷갈리기 쉬운 점",
   "여기서 편향(Bias)은 사회적 치우침이에요. GloVe 식의 b_i 같은 '편향 항(bias term)'과 다른 말이에요.",
   "편향은 '찾기와 줄이기 연구가 있다' 까지이고, '이미 해결됐다'가 아니에요."),
 ]})

# ================= p.50 =================
S.append({"p": 50, "title": "마무리: 요약, 실습, 과제 1",
 "terms": [EN(k) for k in ["token", "sub", "bpe", "fert", "w2v", "soft", "sgd", "ns", "dist", "tokzr", "wv"]],
 "pass1": [
  say("오늘의 주문: " + MANTRA,
      "첫 단계가 " + T("tokz") + ", 둘째 단계가 단어 벡터 만들기예요.",
      "오늘은 앞 두 단계를 배웠어요. 글을 " + T("token") + "으로 자르기, 토큰을 " + T("wv") + "로 바꾸기.",
      "쉬는 시간 뒤 Colab 실습, 그리고 과제 1 이 나와요."),
  points("오늘 한 줄씩",
   "토큰: 단어도 글자도 아닌 " + T("sub") + ". " + T("bpe") + "는 '세고 합치기' 반복. 한국어는 " + T("fert") + "가 문제",
   "벡터: 뜻 = 문맥의 분포 → " + T("w2v") + " = 창 예측 + 소프트맥스 + SGD + 네거티브 샘플링",
   "한 줄 요약: (관찰 - 기대) 만큼 " + T("param") + "를 당기고 밀면 의미 지도가 생겨요",
   "학습은 " + T("sgd") + "로 벌점을 조금씩 줄이는 일이에요"),
 ],
 "pass2": [
  compare("영어 문장 → 우리말 뜻", ["슬라이드 영어", "우리말 뜻"], [
   ["Tokens: not words, not characters, subwords", "토큰: 단어도 글자도 아닌 서브워드"],
   ["meaning = distribution of contexts", "뜻 = 문맥의 분포"],
   ["pull and push by (observed - expected)", "(관찰 - 기대)만큼 당기고 밀기"],
   ["Lab, right after the break", "쉬는 시간 바로 뒤 실습"],
   ["Assignment 1 out today (word vectors, 5%), due before next Monday's class", "과제 1 오늘 나옴(5%), 다음 주 월요일 수업 전까지"]]),
  steps("word2vec 을 만드는 네 재료", [
   "창 예측: " + T("center") + "로 " + T("context") + " 맞히기",
   T("soft") + ": 점수를 확률 파이로",
   T("sgd") + ": 조금씩 떼어 자주 한 걸음",
   T("ns") + ": 소프트맥스 분모를 진짜 1 + 가짜 k 로 줄이기"], "넷을 합치면 모두가 실제로 돌리는 word2vec"),
  check("슬라이드의 '한 줄 요약'에서 당기고 미는 기준은?",
        ["관찰 - 기대 (observed - expected)", "어휘 크기", "토큰 수"], 0,
        "p.37 의 기울기 식처럼 '본 것 - 기대한 것' 만큼 벡터를 고쳐요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
   box(80, 155, 1270, 190, "토큰: 서브워드. BPE = '세고 합치기' 반복. 한국어는 fertility 가 문제"),
   box(80, 202, 1285, 238, "벡터: 뜻 = 문맥 분포 → word2vec = 창 예측 + softmax + SGD + negative sampling"),
   box(80, 250, 1060, 285, "한 줄 요약: (observed - expected) 만큼 당기고 밀면 의미 지도가 생겨요"),
   box(80, 298, 1370, 333, "실습: Colab 시작 → BPE 직접 만들기 → 한국어 토크나이저 학습 → word2vec 실험"),
   box(80, 346, 915, 381, "과제 1 오늘 배포(단어 벡터, 5%), 다음 주 월요일 수업 전까지"),
   box(372, 678, 1033, 710, "15분 뒤 Colab 에서, 오늘 배운 게 모두 코드가 돼요")),
  prof(MON2,
   "오늘 정리: 단어로 자르면 안 좋고 글자로 자르면 또 안 좋아서 결국 서브워드로 쪼갰다는 게 첫 포인트.",
   "두 번째는 토큰을 벡터로 어떻게 나타내느냐, word2vec 은 관찰 마이너스 예측으로 당길 건 당기고 밀 건 민다는 것.",
   "과제 1 은 성적의 5% 정도이고 굉장히 쉽다, 다음 주 수업 전까지 내면 된다고 했어요."),
  prof(MON3,
   "과제 1 은 5점짜리예요. Part A 는 한국어 토이 말뭉치로 " + T("bpe") + "를 해 보는 코딩(1점), AI 도구를 써도 되지만 썼다면 어떤 도구인지 꼭 밝혀야 해요.",
   "Part B 는 수업 내용 질문 2개(각 2점, 모두 4점), AI 도구 없이 자기 말로 써요.",
   "노트북에 답을 채워 사이버 캠퍼스에 다음 주 수업 전(2시 59분)까지 내요."),
  points("실습(N2L)과 짝 맞추기",
   "N2L p.19: gensim Word2Vec(vector_size=100, window=5, min_count=5, sg=1, negative=10)",
   "N2L p.20 most_similar(이웃), p.21 similarity(유사도), p.22 어휘에 있는지와 count",
   "N2L p.23 왕 - 남자 + 여자(유추), p.24~25 PCA 로 60개 단어를 2차원 지도에"),
 ],
 "pass4": [
  check("과제 1 에 대해 녹음과 맞는 것은?",
        ["Part A(BPE 코딩)는 AI 도구를 써도 되지만 사용을 밝혀야 한다", "Part B 질문도 AI 로 써서 내면 된다", "과제 1 은 20점짜리다"], 0,
        "Part A 는 AI 도구 사용 가능(명시 필수), Part B 는 AI 없이 자기 말로. 과제는 5점이에요."),
  english("답안에 쓸 문장",
   "word2vec 은 분포 가설에 따라 중심 단어로 윈도우 안 문맥 단어를 예측하며, 소프트맥스 확률과 SGD 로 학습하고 네거티브 샘플링으로 계산을 줄인다. 결과적으로 (관찰 - 기대)만큼 벡터를 당기고 밀어 의미 지도가 생긴다.",
   "오늘 벡터 파트 전체를 두 문장으로.", "창 예측, 소프트맥스, SGD, 네거티브 샘플링"),
  warn("헷갈리기 쉬운 점",
   "과제 1 은 슬라이드에 '(word vectors, 5%)' 라고 적혀 있지만, 녹음 설명으로는 Part A 가 BPE 코딩이에요. 토큰화와 벡터 둘 다 복습해 두세요.",
   "성적 비중: 과제보다 기말고사와 팀 프로젝트(합쳐 55%)가 더 커요."),
 ]})

# ---------------- glossary ----------------
used = []
for s in S:
    for t in s["terms"]:
        if t not in used:
            used.append(t)
by_en = {v[1]: k for k, v in TERMS.items()}
glossary = []
for en in used:
    k = by_en[en]
    ko = TERMS[k][0]
    sy, more = GLOSS[k]
    glossary.append({"ko": ko, "en": en, "say": sy, "more": more})

out = {"deck": "N2", "from": 38, "to": 50, "glossary": glossary, "slides": S}
with open(OUT, "w", encoding="utf-8") as fp:
    json.dump(out, fp, ensure_ascii=False, indent=1)
print("저장:", OUT, "쪽", len(S), "용어", len(glossary))
