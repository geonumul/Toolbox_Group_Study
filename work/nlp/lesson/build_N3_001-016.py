# 3강(N3) Neural NLP Foundations 회독 레슨 1~16쪽 생성기. 사용: python build_N3_001-016.py
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "N3_001-016.json")

# ---------------- 손계산 확인 (assert) ----------------
def sigmoid(z):
    return 1 / (1 + math.exp(-z))

def relu(z):
    return max(0.0, z)

def matvec(M, v):
    return [sum(a * b for a, b in zip(row, v)) for row in M]

def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]

# p.7 소프트맥스와 교차 엔트로피: 점수 [PERSON 1, LOCATION 3, ORG 0]
sc = [1, 3, 0]
ex = [math.exp(s) for s in sc]
P = [e / sum(ex) for e in ex]
assert [round(p, 2) for p in P] == [0.11, 0.84, 0.04]
assert abs(sum(P) - 1) < 1e-12
assert round(-math.log(P[1]), 2) == 0.17
assert round(-math.log(0.9), 2) == 0.11 and round(-math.log(0.01), 2) == 4.61

# p.9 뉴런 하나: x=[1,2,3], w=[0.5,-1,0.5], b=0.5
x9, w9, b9 = [1, 2, 3], [0.5, -1, 0.5], 0.5
z9 = sum(a * b for a, b in zip(w9, x9)) + b9
assert z9 == 0.5
assert relu(z9) == 0.5 and round(sigmoid(z9), 2) == 0.62
# 입력만 바꾸면: x=[1,3,1] -> z = 0.5-3+0.5+0.5 = -1.5 -> ReLU 0
z9b = sum(a * b for a, b in zip(w9, [1, 3, 1])) + b9
assert z9b == -1.5 and relu(z9b) == 0 and round(sigmoid(z9b), 2) == 0.18

# p.10 ReLU 와 시그모이드 값
assert [relu(v) for v in [-2, 0, 3]] == [0, 0, 3]
assert sigmoid(0) == 0.5 and round(sigmoid(4), 2) == 0.98 and round(sigmoid(-4), 2) == 0.02

# p.11 선형층 두 개가 하나로 합쳐짐
W1 = [[1, 2], [0, 1]]
W2 = [[1, 0], [1, 1]]
xx = [1, 1]
assert matvec(W1, xx) == [3, 1]
assert matvec(W2, matvec(W1, xx)) == [3, 4]
W21 = matmul(W2, W1)
assert W21 == [[1, 2], [1, 3]]
assert matvec(W21, xx) == [3, 4]
# 사이에 ReLU 를 끼우면 달라짐
V1 = [[1, -2], [0, 1]]
hv = matvec(V1, xx)
assert hv == [-1, 1]
assert matvec(W2, [relu(v) for v in hv]) == [0, 1]
assert matvec(matmul(W2, V1), xx) == [-1, 0]

# p.12 그림 속 MLP 파라미터 세기: 4 -> 4 -> 4 -> 3 (U 는 편향 없음)
assert 4 * 4 + 4 + 4 * 4 + 4 + 3 * 4 == 52

# p.13, p.14 합성곱 손계산 (단어마다 숫자 하나로 줄인 장난감)
words = ["this", "movie", "was", "really", "great", "fun"]
vals = [0, 1, 0, 2, 3, -1]
fmap = [sum(vals[i:i + 3]) for i in range(len(vals) - 2)]
assert fmap == [1, 3, 5, 4]
assert max(fmap) == 5 and fmap.index(5) == 2  # was really great
assert max([5, 1, 0, 0]) == max([0, 0, 1, 5]) == 5

# p.15 Check Yourself Q2
assert 5 * 100 == 500
assert 300 * 500 == 150000 and 300 * 500 + 300 == 150300

# ---------------- 용어 표기 ----------------
NLP = "**NLP(자연어처리)**"
TOK = "**토큰(Token)**"
BPE = "**BPE(바이트 쌍 인코딩)**"
W2V = "**word2vec**"
WV = "**단어 벡터(Word Vector)**"
NN = "**신경망(Neural Network)**"
LM = "**언어 모델(Language Model)**"
NER = "**NER(개체명 인식)**"
CLS = "**분류(Classification)**"
WIN = "**윈도우(Window)**"
CW = "**중심 단어(Center Word)**"
SUP = "**지도 학습(Supervised Learning)**"
LAB = "**레이블(Label)**"
SMX = "**소프트맥스(Softmax)**"
CE = "**교차 엔트로피(Cross-Entropy)**"
LOSS = "**손실 함수(Loss Function)**"
LOGIT = "**로짓(Logit)**"
LINC = "**선형 분류기(Linear Classifier)**"
DB = "**결정 경계(Decision Boundary)**"
HYP = "**초평면(Hyperplane)**"
NONLIN = "**비선형성(Nonlinearity)**"
NEU = "**뉴런(Neuron)**"
WT = "**가중치(Weight)**"
BIAS = "**편향 항(Bias Term)**"
WS = "**가중합(Weighted Sum)**"
ACT = "**활성화 함수(Activation Function)**"
SIG = "**시그모이드(Sigmoid)**"
TANH = "**하이퍼볼릭 탄젠트(tanh)**"
RELU = "**ReLU(렐루)**"
GELU = "**GELU(겔루)**"
MLP = "**MLP(다층 퍼셉트론)**"
HID = "**은닉층(Hidden Layer)**"
PAR = "**파라미터(Parameter)**"
CNN = "**CNN(합성곱 신경망)**"
FIL = "**합성곱 필터(Convolution Filter)**"
FMAP = "**특징 맵(Feature Map)**"
POOL = "**최대 풀링(Max-pooling)**"
NG = "**n-gram(엔그램)**"
UAT = "**보편 근사 정리(Universal Approximation Theorem)**"
BP = "**역전파(Backpropagation)**"
RNN = "**RNN(순환 신경망)**"
GRAD = "**기울기(Gradient)**"
VG = "**기울기 소실(Vanishing Gradient)**"
TRF = "**트랜스포머(Transformer)**"
MAT = "**행렬(Matrix)**"
LOGREG = "**로지스틱 회귀(Logistic Regression)**"

MANTRA = "글을 토큰으로 자르고, 토큰을 벡터로 바꾸고, 벡터로 다음 토큰을 맞혀요."
WHEN = "3주차 월요일 1교시"

GLOSSARY = [
    ("자연어처리", "Natural Language Processing (NLP)", "컴퓨터가 사람의 말과 글을 다루게 하는 분야",
     "글을 토큰으로 자르고, 벡터로 바꾸고, 그 벡터로 뜻을 맞히거나 다음 말을 만들어요."),
    ("토큰", "Token", "글을 자른 레고 조각 하나",
     "모델이 읽는 가장 작은 단위예요. 단어일 수도, 단어의 조각(서브워드)일 수도 있어요."),
    ("바이트 쌍 인코딩", "Byte Pair Encoding (BPE)", "자주 붙어 다니는 두 조각을 한 조각으로 접착하는 토큰화 방법",
     "2주차에 배운 서브워드 토큰화예요. 가장 자주 나오는 쌍을 계속 합쳐 어휘를 만들어요."),
    ("워드투벡", "word2vec", "주변 단어를 맞히면서 단어의 지도 좌표를 배우는 방법",
     "2주차의 핵심이에요. 친구(주변 단어)를 보면 그 단어를 안다는 생각으로 단어 벡터를 학습해요."),
    ("단어 벡터", "Word Vector", "단어의 지도 좌표. 뜻이 비슷하면 가까이 살아요",
     "숫자 여러 개를 줄 세운 것이에요. 3주차에는 이 벡터가 신경망의 입력이 돼요."),
    ("신경망", "Neural Network", "뉴런을 여러 층 쌓아 벡터를 받아 답을 내는 계산 기계",
     "가중합, 편향 항, 활성화 함수를 층마다 반복해요. 가중치와 편향은 학습으로 정해져요."),
    ("언어 모델", "Language Model (LM)", "휴대폰 자판의 다음 단어 추천처럼 다음 토큰을 맞히는 모델",
     "3주차 뒷부분(Part 3, 4)에서 자세히 배워요. GPT 같은 모델도 결국 언어 모델이에요."),
    ("개체명 인식", "Named Entity Recognition (NER)", "글 속에서 사람, 기관, 장소 같은 이름을 찾아 종류를 붙이는 일",
     "3주차에서 신경망을 설명할 때 계속 쓰는 예제 과제예요. 'Busan' 은 장소(LOCATION)라고 붙여요."),
    ("분류", "Classification", "입력을 보고 정해진 여러 칸 중 어느 칸인지 고르는 일",
     "칸 하나하나를 클래스라고 불러요. NER 은 단어마다 사람, 장소 같은 클래스를 고르는 분류예요."),
    ("윈도우", "Window", "가운데 단어 양옆으로 몇 단어씩 함께 보는 창",
     "m=2 이면 가운데 단어 앞 2개, 뒤 2개를 봐서 모두 5단어예요. 2주차 word2vec 에서도 나왔어요."),
    ("중심 단어", "Center Word", "윈도우 한가운데에 있어 지금 판단하려는 단어",
     "NER 창 분류에서는 이 단어가 장소인지를 묻고, 양옆 단어는 힌트로 써요."),
    ("지도 학습", "Supervised Learning", "문제와 정답을 짝으로 주고 배우게 하는 방법",
     "학습 자료가 (입력 x, 정답 y) 짝으로 되어 있어요. 모델은 정답을 맞히도록 가중치를 고쳐요."),
    ("레이블", "Label", "입력에 붙여 둔 정답 이름표",
     "'Busan' 에 LOCATION 을 붙여 두는 식이에요. 지도 학습의 y 가 레이블이에요."),
    ("소프트맥스", "Softmax", "점수를 모두 더해 1이 되는 확률 파이로 나누기",
     "각 점수에 exp 를 씌운 뒤 전체 합으로 나눠요. 결과는 0과 1 사이이고 다 더하면 1이에요."),
    ("교차 엔트로피", "Cross-Entropy", "정답 칸에 준 확률의 -log 를 벌점으로 매기는 손실",
     "정답 확률이 1에 가까우면 벌점이 0에 가깝고, 0에 가까우면 벌점이 크게 올라가요. 소프트맥스 + NLL 이에요."),
    ("손실 함수", "Loss Function", "틀린 정도를 매기는 벌점",
     "학습은 이 벌점이 작아지는 쪽으로 가중치를 조금씩 고치는 일이에요. 기호는 J(θ) 로 써요."),
    ("로짓", "Logit", "소프트맥스에 넣기 전의 날것 점수",
     "Wx 로 얻은 점수라서 음수도 양수도 될 수 있어요. 확률이 아니에요. 스코어(score)라고도 불러요."),
    ("선형 분류기", "Linear Classifier", "곧은 선(평면) 하나로만 두 무리를 가르는 분류기",
     "가중치 행렬 W 하나만 곱하는 모델이에요. 소프트맥스 분류기(로지스틱 회귀)도 선형 분류기예요."),
    ("결정 경계", "Decision Boundary", "분류기가 '여기부터는 A, 저기부터는 B' 라고 긋는 경계선",
     "선형 분류기의 결정 경계는 곧은 선이고, 비선형성이 있으면 휘어진 곡선이 될 수 있어요."),
    ("초평면", "Hyperplane", "n차원 공간을 둘로 가르는 n-1차원의 평평한 판",
     "2차원이면 선, 3차원이면 면이에요. 선형 분류기가 긋는 경계가 초평면이에요."),
    ("비선형성", "Nonlinearity", "곧은 선이 아니게 휘게 만드는 성질",
     "뉴런의 가중합 뒤에 활성화 함수를 거치게 해서 넣어요. 이게 없으면 층을 쌓아도 행렬 하나와 같아요."),
    ("뉴런", "Neuron", "가중합 + 편향 항을 계산하고 활성화 함수를 통과시키는 작은 계산 단위",
     "하나의 뉴런은 학습된 패턴 탐지기 하나예요. 식은 h = f(wᵀx + b) 예요."),
    ("가중치", "Weight", "입력마다 얼마나 중요하게 볼지 곱하는 숫자",
     "뉴런 여러 개의 가중치를 모으면 행렬 W 가 돼요. 학습으로 정해지는 파라미터예요."),
    ("편향 항", "Bias Term", "가중합에 더하는 숫자 하나 b",
     "입력이 모두 0이어도 뉴런이 켜지는 기준을 옮겨 줘요. 사회적 편향(Bias)과 다른 말이에요."),
    ("가중합", "Weighted Sum", "입력마다 가중치를 곱해서 모두 더한 값",
     "w₁x₁ + w₂x₂ + ... 이에요. 여기에 편향 항 b 를 더한 z = wᵀx + b 를 아핀 변환이라고도 불러요."),
    ("활성화 함수", "Activation Function", "가중합 결과 z 를 받아 휘어진 값 f(z) 로 바꾸는 함수",
     "시그모이드, tanh, ReLU, GELU 가 대표예요. 신경망에 비선형성을 넣는 부품이에요."),
    ("시그모이드", "Sigmoid", "어떤 수든 0과 1 사이로 눌러 주는 S자 함수",
     "f(z) = 1 / (1 + e^(-z)) 예요. 확률이나 LSTM 의 게이트처럼 0~1 값이 필요할 때 써요."),
    ("하이퍼볼릭 탄젠트", "tanh", "어떤 수든 -1과 1 사이로 눌러 주는 S자 함수",
     "시그모이드와 모양이 비슷하지만 가운데가 0이에요. 양 끝으로 가면 기울기가 거의 0이 돼요."),
    ("렐루", "ReLU", "음수는 0으로 끄고 양수는 그대로 통과시키는 함수",
     "f(z) = max(z, 0) 이에요. 싸고 빠르고 성능이 좋아서 딥러닝의 일꾼(workhorse)이라고 불러요."),
    ("겔루", "GELU", "ReLU 를 부드럽게 다듬은 활성화 함수",
     "0 근처에서 뚝 자르지 않고 부드럽게 변해요. 트랜스포머에서 주로 써요(4주차에 다시 나와요)."),
    ("다층 퍼셉트론", "Multi-Layer Perceptron (MLP)", "뉴런 층을 여러 겹 쌓은 가장 기본 신경망",
     "h(1) = f(W(1)x + b(1)), h(2) = f(W(2)h(1) + b(2)), ŷ = softmax(U h(2)) 처럼 같은 계산을 반복해요."),
    ("은닉층", "Hidden Layer", "입력과 출력 사이에 숨어 있는 중간 층",
     "밖에서는 입력과 출력만 보이고 가운데 계산은 안 보여서 '숨은(hidden)' 층이라고 불러요."),
    ("파라미터", "Parameter", "학습으로 정해지는 숫자들(가중치와 편향 항)",
     "처음에는 무작위로 시작하고, 손실 함수를 줄이는 쪽으로 조금씩 고쳐요. 모아서 θ 라고 써요."),
    ("합성곱 신경망", "Convolutional Neural Network (CNN)", "작은 필터를 미끄러뜨리며 부분 패턴을 찾는 신경망",
     "글에서는 단어 몇 개짜리 창을 훑어 n-gram 패턴을 찾아요. 모든 창을 한꺼번에(병렬로) 계산해서 빨라요."),
    ("합성곱 필터", "Convolution Filter", "문장을 따라 미끄러지며 작은 패턴을 찾는 숫자 판",
     "폭 3짜리 필터는 연속된 세 단어(trigram) 패턴 탐지기예요. 같은 필터를 문장 전체에 다시 써요."),
    ("특징 맵", "Feature Map", "필터가 창마다 낸 값을 줄 세운 결과",
     "창 하나마다 값 하나가 나와요. 값이 크면 그 자리에 필터가 찾는 패턴이 있다는 뜻이에요."),
    ("최대 풀링", "Max-pooling", "특징 맵에서 가장 큰 값 하나만 남기기",
     "'이 패턴이 문장 어디에서든 나왔나?' 를 묻는 것이라서, 어디서 나왔는지는 버려요."),
    ("엔그램", "n-gram", "바로 붙어 있는 단어 n개 묶음",
     "2개면 bigram, 3개면 trigram 이에요. 3주차 Part 3 에서 n-gram 언어 모델로 다시 나와요."),
    ("보편 근사 정리", "Universal Approximation Theorem", "은닉 뉴런이 충분하면 웬만한 함수는 다 흉내 낼 수 있다는 정리",
     "비선형 활성화 함수가 있을 때 성립해요. 그래서 비선형성이 있는 신경망이 강력해요."),
    ("역전파", "Backpropagation", "틀린 책임을 뒤에서 앞으로 나눠 주기",
     "손실 함수의 기울기를 출력 쪽에서 입력 쪽으로 연쇄 법칙으로 계산해요. 3주차 Part 2 의 주제예요."),
    ("순환 신경망", "Recurrent Neural Network (RNN)", "한 단어씩 읽으며 메모장(은닉 상태)에 요약을 고쳐 쓰는 사람",
     "기억을 가진 읽는 사람(a reader with memory)이에요. 3주차 Part 4 에서 배워요."),
    ("기울기", "Gradient", "손실이 가장 빨리 커지는 방향과 그 가파름",
     "학습은 기울기의 반대 방향으로 한 걸음씩 내려가요. 안개 낀 산의 발밑 기울기예요."),
    ("기울기 소실", "Vanishing Gradient", "귓속말 전달 게임에서 말이 점점 희미해지듯 기울기가 0으로 사라지는 문제",
     "시그모이드, tanh 는 양 끝에서 기울기가 거의 0이라 층이 깊어지면 앞쪽 층까지 기울기가 잘 안 가요."),
    ("트랜스포머", "Transformer", "어텐션으로 문장을 한꺼번에 보는 요즘 언어 모델의 기본 구조",
     "4주차에 배워요. 활성화 함수로 GELU 를 많이 써요."),
    ("행렬", "Matrix", "숫자를 가로세로 표 모양으로 늘어놓은 것",
     "shape 은 (행 수, 열 수)로 써요. (3,5) 행렬에 길이 5 벡터를 곱하면 길이 3 벡터가 나와요."),
    ("로지스틱 회귀", "Logistic Regression", "점수를 확률로 바꿔 분류하는 가장 단순한 선형 분류기",
     "클래스가 여러 개면 소프트맥스 회귀라고도 해요. 행렬 W 하나만 곱하므로 선형이에요."),
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

def TX(x, y, s, cls="t", size=16, anchor="middle", b=0):
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

def BOX(x, y, w, h, s, cls="box", tcls="tb", b=0, size=15):
    return R(x, y, w, h, cls, b) + TX(x + w / 2, y + h / 2 + size * 0.35, s, tcls, size, "middle", b)

def NODE(cx, cy, r, s, cls="n", b=0, size=14):
    return C(cx, cy, r, cls, b) + TX(cx, cy + size * 0.35, s, "tl", size, "middle", b)

def PL(pts, cls="e2", b=0):
    return f'<polyline points="{pts}" fill="none" class="{_c(cls, b)}"/>'

# p.4 파이프라인
FIG_PIPE = SVG(
    BOX(10, 100, 80, 44, "글", "box", "tb", 0, 16), A(92, 122, 118, 122),
    BOX(120, 100, 80, 44, "토큰", "box", "tb", 0, 16), A(202, 122, 228, 122),
    BOX(230, 100, 80, 44, "벡터", "box2", "tb", 0, 16), A(312, 122, 338, 122, "e2", 1),
    BOX(340, 100, 130, 44, "???", "box2", "tb", 1, 18),
    TX(270, 60, "지난주(2주차)까지", "tm", 14, "middle"),
    TX(405, 186, "오늘: 신경망", "tb", 16, "middle", 2),
    TX(405, 210, "벡터를 먹는 기계", "tm", 14, "middle", 2),
    TX(240, 250, "다음 목표: 다음 토큰 맞히기(언어 모델)", "tm", 14, "middle", 3),
)

# p.6 NER 창 분류
_w6 = ["the", "launch", "event", "in", "Busan", "drew", "big", "crowds"]
_els6 = []
for i, w in enumerate(_w6):
    x = 6 + i * 59
    cls = "n4" if w == "Busan" else ("n3" if 2 <= i <= 6 else "n")
    b = 0 if w == "Busan" or not (2 <= i <= 6) else 1
    _els6.append(R(x, 40, 54, 34, cls, 0 if cls == "n" else b))
    _els6.append(TX(x + 27, 62, w, "tl", 13))
for i in range(2, 7):
    _els6.append(L(6 + i * 59 + 27, 76, 240, 140, "e", 1))
FIG_WINDOW = SVG(
    TX(240, 24, "윈도우 m=2: 가운데 단어 앞 2개 + 뒤 2개", "tb", 15),
    *_els6,
    BOX(80, 142, 320, 40, "event, in, Busan, drew, big 벡터 이어 붙이기", "box2", "tb", 2, 14),
    A(240, 184, 240, 214, "e2", 3),
    BOX(110, 216, 260, 40, "분류기: Busan 은 장소일 확률?", "box", "tb", 3, 14),
)

# p.8 직선의 한계 (네 무리)
def _cluster(cx, cy, cls, b):
    return "".join(C(cx + dx, cy + dy, 5, cls, b) for dx, dy in [(-14, -6), (0, -12), (12, -4), (-6, 8), (10, 10), (0, 0)])

FIG_LINE = SVG(
    R(20, 20, 440, 230, "box"),
    _cluster(110, 80, "n4", 0), _cluster(370, 80, "n2", 0),
    _cluster(110, 195, "n2", 0), _cluster(370, 195, "n4", 0),
    L(30, 60, 450, 215, "e2", 1), TX(430, 245, "직선: 어떻게 그어도 실패", "tb", 14, "end", 1),
    PL("20,115 80,150 150,170 220,200 280,250", "hl", 2),
    PL("190,20 250,55 320,110 390,140 460,160", "hl", 2),
    TX(30, 240, "곡선 두 개면 갈라져요", "tb", 14, "start", 2),
)

# p.9 뉴런 하나: x=[1,2,3], w=[0.5,-1,0.5], b=0.5
x9, w9, b9 = [1, 2, 3], [0.5, -1, 0.5], 0.5
z9 = sum(a * b for a, b in zip(w9, x9)) + b9
assert z9 == 0.5
assert relu(z9) == 0.5 and round(sigmoid(z9), 2) == 0.62
# 입력만 바꾸면: x=[1,3,1] -> z = 0.5-3+0.5+0.5 = -1.5 -> ReLU 0
z9b = sum(a * b for a, b in zip(w9, [1, 3, 1])) + b9
assert z9b == -1.5 and relu(z9b) == 0 and round(sigmoid(z9b), 2) == 0.18

# p.10 ReLU 와 시그모이드 값
assert [relu(v) for v in [-2, 0, 3]] == [0, 0, 3]
assert sigmoid(0) == 0.5 and round(sigmoid(4), 2) == 0.98 and round(sigmoid(-4), 2) == 0.02

# p.11 선형층 두 개가 하나로 합쳐짐
W1 = [[1, 2], [0, 1]]
W2 = [[1, 0], [1, 1]]
xx = [1, 1]
assert matvec(W1, xx) == [3, 1]
assert matvec(W2, matvec(W1, xx)) == [3, 4]
W21 = matmul(W2, W1)
assert W21 == [[1, 2], [1, 3]]
assert matvec(W21, xx) == [3, 4]
# 사이에 ReLU 를 끼우면 달라짐
V1 = [[1, -2], [0, 1]]
hv = matvec(V1, xx)
assert hv == [-1, 1]
assert matvec(W2, [relu(v) for v in hv]) == [0, 1]
assert matvec(matmul(W2, V1), xx) == [-1, 0]

# p.12 그림 속 MLP 파라미터 세기: 4 -> 4 -> 4 -> 3 (U 는 편향 없음)
assert 4 * 4 + 4 + 4 * 4 + 4 + 3 * 4 == 52

# p.13, p.14 합성곱 손계산 (단어마다 숫자 하나로 줄인 장난감)
words = ["this", "movie", "was", "really", "great", "fun"]
vals = [0, 1, 0, 2, 3, -1]
fmap = [sum(vals[i:i + 3]) for i in range(len(vals) - 2)]
assert fmap == [1, 3, 5, 4]
assert max(fmap) == 5 and fmap.index(5) == 2  # was really great
assert max([5, 1, 0, 0]) == max([0, 0, 1, 5]) == 5

# p.15 Check Yourself Q2
assert 5 * 100 == 500
assert 300 * 500 == 150000 and 300 * 500 + 300 == 150300

# ---------------- 용어 표기 ----------------
NLP = "**NLP(자연어처리)**"
TOK = "**토큰(Token)**"
BPE = "**BPE(바이트 쌍 인코딩)**"
W2V = "**word2vec**"
WV = "**단어 벡터(Word Vector)**"
NN = "**신경망(Neural Network)**"
LM = "**언어 모델(Language Model)**"
NER = "**NER(개체명 인식)**"
CLS = "**분류(Classification)**"
WIN = "**윈도우(Window)**"
CW = "**중심 단어(Center Word)**"
SUP = "**지도 학습(Supervised Learning)**"
LAB = "**레이블(Label)**"
SMX = "**소프트맥스(Softmax)**"
CE = "**교차 엔트로피(Cross-Entropy)**"
LOSS = "**손실 함수(Loss Function)**"
LOGIT = "**로짓(Logit)**"
LINC = "**선형 분류기(Linear Classifier)**"
DB = "**결정 경계(Decision Boundary)**"
HYP = "**초평면(Hyperplane)**"
NONLIN = "**비선형성(Nonlinearity)**"
NEU = "**뉴런(Neuron)**"
WT = "**가중치(Weight)**"
BIAS = "**편향 항(Bias Term)**"
WS = "**가중합(Weighted Sum)**"
ACT = "**활성화 함수(Activation Function)**"
SIG = "**시그모이드(Sigmoid)**"
TANH = "**하이퍼볼릭 탄젠트(tanh)**"
RELU = "**ReLU(렐루)**"
GELU = "**GELU(겔루)**"
MLP = "**MLP(다층 퍼셉트론)**"
HID = "**은닉층(Hidden Layer)**"
PAR = "**파라미터(Parameter)**"
CNN = "**CNN(합성곱 신경망)**"
FIL = "**합성곱 필터(Convolution Filter)**"
FMAP = "**특징 맵(Feature Map)**"
POOL = "**최대 풀링(Max-pooling)**"
NG = "**n-gram(엔그램)**"
UAT = "**보편 근사 정리(Universal Approximation Theorem)**"
BP = "**역전파(Backpropagation)**"
RNN = "**RNN(순환 신경망)**"
GRAD = "**기울기(Gradient)**"
VG = "**기울기 소실(Vanishing Gradient)**"
TRF = "**트랜스포머(Transformer)**"
MAT = "**행렬(Matrix)**"
LOGREG = "**로지스틱 회귀(Logistic Regression)**"

MANTRA = "글을 토큰으로 자르고, 토큰을 벡터로 바꾸고, 벡터로 다음 토큰을 맞혀요."
WHEN = "3주차 월요일 1교시"

GLOSSARY = [
    ("자연어처리", "Natural Language Processing (NLP)", "컴퓨터가 사람의 말과 글을 다루게 하는 분야",
     "글을 토큰으로 자르고, 벡터로 바꾸고, 그 벡터로 뜻을 맞히거나 다음 말을 만들어요."),
    ("토큰", "Token", "글을 자른 레고 조각 하나",
     "모델이 읽는 가장 작은 단위예요. 단어일 수도, 단어의 조각(서브워드)일 수도 있어요."),
    ("바이트 쌍 인코딩", "Byte Pair Encoding (BPE)", "자주 붙어 다니는 두 조각을 한 조각으로 접착하는 토큰화 방법",
     "2주차에 배운 서브워드 토큰화예요. 가장 자주 나오는 쌍을 계속 합쳐 어휘를 만들어요."),
    ("워드투벡", "word2vec", "주변 단어를 맞히면서 단어의 지도 좌표를 배우는 방법",
     "2주차의 핵심이에요. 친구(주변 단어)를 보면 그 단어를 안다는 생각으로 단어 벡터를 학습해요."),
    ("단어 벡터", "Word Vector", "단어의 지도 좌표. 뜻이 비슷하면 가까이 살아요",
     "숫자 여러 개를 줄 세운 것이에요. 3주차에는 이 벡터가 신경망의 입력이 돼요."),
    ("신경망", "Neural Network", "뉴런을 여러 층 쌓아 벡터를 받아 답을 내는 계산 기계",
     "가중합, 편향 항, 활성화 함수를 층마다 반복해요. 가중치와 편향은 학습으로 정해져요."),
    ("언어 모델", "Language Model (LM)", "휴대폰 자판의 다음 단어 추천처럼 다음 토큰을 맞히는 모델",
     "3주차 뒷부분(Part 3, 4)에서 자세히 배워요. GPT 같은 모델도 결국 언어 모델이에요."),
    ("개체명 인식", "Named Entity Recognition (NER)", "글 속에서 사람, 기관, 장소 같은 이름을 찾아 종류를 붙이는 일",
     "3주차에서 신경망을 설명할 때 계속 쓰는 예제 과제예요. 'Busan' 은 장소(LOCATION)라고 붙여요."),
    ("분류", "Classification", "입력을 보고 정해진 여러 칸 중 어느 칸인지 고르는 일",
     "칸 하나하나를 클래스라고 불러요. NER 은 단어마다 사람, 장소 같은 클래스를 고르는 분류예요."),
    ("윈도우", "Window", "가운데 단어 양옆으로 몇 단어씩 함께 보는 창",
     "m=2 이면 가운데 단어 앞 2개, 뒤 2개를 봐서 모두 5단어예요. 2주차 word2vec 에서도 나왔어요."),
    ("중심 단어", "Center Word", "윈도우 한가운데에 있어 지금 판단하려는 단어",
     "NER 창 분류에서는 이 단어가 장소인지를 묻고, 양옆 단어는 힌트로 써요."),
    ("지도 학습", "Supervised Learning", "문제와 정답을 짝으로 주고 배우게 하는 방법",
     "학습 자료가 (입력 x, 정답 y) 짝으로 되어 있어요. 모델은 정답을 맞히도록 가중치를 고쳐요."),
    ("레이블", "Label", "입력에 붙여 둔 정답 이름표",
     "'Busan' 에 LOCATION 을 붙여 두는 식이에요. 지도 학습의 y 가 레이블이에요."),
    ("소프트맥스", "Softmax", "점수를 모두 더해 1이 되는 확률 파이로 나누기",
     "각 점수에 exp 를 씌운 뒤 전체 합으로 나눠요. 결과는 0과 1 사이이고 다 더하면 1이에요."),
    ("교차 엔트로피", "Cross-Entropy", "정답 칸에 준 확률의 -log 를 벌점으로 매기는 손실",
     "정답 확률이 1에 가까우면 벌점이 0에 가깝고, 0에 가까우면 벌점이 크게 올라가요. 소프트맥스 + NLL 이에요."),
    ("손실 함수", "Loss Function", "틀린 정도를 매기는 벌점",
     "학습은 이 벌점이 작아지는 쪽으로 가중치를 조금씩 고치는 일이에요. 기호는 J(θ) 로 써요."),
    ("로짓", "Logit", "소프트맥스에 넣기 전의 날것 점수",
     "Wx 로 얻은 점수라서 음수도 양수도 될 수 있어요. 확률이 아니에요. 스코어(score)라고도 불러요."),
    ("선형 분류기", "Linear Classifier", "곧은 선(평면) 하나로만 두 무리를 가르는 분류기",
     "가중치 행렬 W 하나만 곱하는 모델이에요. 소프트맥스 분류기(로지스틱 회귀)도 선형 분류기예요."),
    ("결정 경계", "Decision Boundary", "분류기가 '여기부터는 A, 저기부터는 B' 라고 긋는 경계선",
     "선형 분류기의 결정 경계는 곧은 선이고, 비선형성이 있으면 휘어진 곡선이 될 수 있어요."),
    ("초평면", "Hyperplane", "n차원 공간을 둘로 가르는 n-1차원의 평평한 판",
     "2차원이면 선, 3차원이면 면이에요. 선형 분류기가 긋는 경계가 초평면이에요."),
    ("비선형성", "Nonlinearity", "곧은 선이 아니게 휘게 만드는 성질",
     "뉴런의 가중합 뒤에 활성화 함수를 거치게 해서 넣어요. 이게 없으면 층을 쌓아도 행렬 하나와 같아요."),
    ("뉴런", "Neuron", "가중합 + 편향 항을 계산하고 활성화 함수를 통과시키는 작은 계산 단위",
     "하나의 뉴런은 학습된 패턴 탐지기 하나예요. 식은 h = f(wᵀx + b) 예요."),
    ("가중치", "Weight", "입력마다 얼마나 중요하게 볼지 곱하는 숫자",
     "뉴런 여러 개의 가중치를 모으면 행렬 W 가 돼요. 학습으로 정해지는 파라미터예요."),
    ("편향 항", "Bias Term", "가중합에 더하는 숫자 하나 b",
     "입력이 모두 0이어도 뉴런이 켜지는 기준을 옮겨 줘요. 사회적 편향(Bias)과 다른 말이에요."),
    ("가중합", "Weighted Sum", "입력마다 가중치를 곱해서 모두 더한 값",
     "w₁x₁ + w₂x₂ + ... 이에요. 여기에 편향 항 b 를 더한 z = wᵀx + b 를 아핀 변환이라고도 불러요."),
    ("활성화 함수", "Activation Function", "가중합 결과 z 를 받아 휘어진 값 f(z) 로 바꾸는 함수",
     "시그모이드, tanh, ReLU, GELU 가 대표예요. 신경망에 비선형성을 넣는 부품이에요."),
    ("시그모이드", "Sigmoid", "어떤 수든 0과 1 사이로 눌러 주는 S자 함수",
     "f(z) = 1 / (1 + e^(-z)) 예요. 확률이나 LSTM 의 게이트처럼 0~1 값이 필요할 때 써요."),
    ("하이퍼볼릭 탄젠트", "tanh", "어떤 수든 -1과 1 사이로 눌러 주는 S자 함수",
     "시그모이드와 모양이 비슷하지만 가운데가 0이에요. 양 끝으로 가면 기울기가 거의 0이 돼요."),
    ("렐루", "ReLU", "음수는 0으로 끄고 양수는 그대로 통과시키는 함수",
     "f(z) = max(z, 0) 이에요. 싸고 빠르고 성능이 좋아서 딥러닝의 일꾼(workhorse)이라고 불러요."),
    ("겔루", "GELU", "ReLU 를 부드럽게 다듬은 활성화 함수",
     "0 근처에서 뚝 자르지 않고 부드럽게 변해요. 트랜스포머에서 주로 써요(4주차에 다시 나와요)."),
    ("다층 퍼셉트론", "Multi-Layer Perceptron (MLP)", "뉴런 층을 여러 겹 쌓은 가장 기본 신경망",
     "h(1) = f(W(1)x + b(1)), h(2) = f(W(2)h(1) + b(2)), ŷ = softmax(U h(2)) 처럼 같은 계산을 반복해요."),
    ("은닉층", "Hidden Layer", "입력과 출력 사이에 숨어 있는 중간 층",
     "밖에서는 입력과 출력만 보이고 가운데 계산은 안 보여서 '숨은(hidden)' 층이라고 불러요."),
    ("파라미터", "Parameter", "학습으로 정해지는 숫자들(가중치와 편향 항)",
     "처음에는 무작위로 시작하고, 손실 함수를 줄이는 쪽으로 조금씩 고쳐요. 모아서 θ 라고 써요."),
    ("합성곱 신경망", "Convolutional Neural Network (CNN)", "작은 필터를 미끄러뜨리며 부분 패턴을 찾는 신경망",
     "글에서는 단어 몇 개짜리 창을 훑어 n-gram 패턴을 찾아요. 모든 창을 한꺼번에(병렬로) 계산해서 빨라요."),
    ("합성곱 필터", "Convolution Filter", "문장을 따라 미끄러지며 작은 패턴을 찾는 숫자 판",
     "폭 3짜리 필터는 연속된 세 단어(trigram) 패턴 탐지기예요. 같은 필터를 문장 전체에 다시 써요."),
    ("특징 맵", "Feature Map", "필터가 창마다 낸 값을 줄 세운 결과",
     "창 하나마다 값 하나가 나와요. 값이 크면 그 자리에 필터가 찾는 패턴이 있다는 뜻이에요."),
    ("최대 풀링", "Max-pooling", "특징 맵에서 가장 큰 값 하나만 남기기",
     "'이 패턴이 문장 어디에서든 나왔나?' 를 묻는 것이라서, 어디서 나왔는지는 버려요."),
    ("엔그램", "n-gram", "바로 붙어 있는 단어 n개 묶음",
     "2개면 bigram, 3개면 trigram 이에요. 3주차 Part 3 에서 n-gram 언어 모델로 다시 나와요."),
    ("보편 근사 정리", "Universal Approximation Theorem", "은닉 뉴런이 충분하면 웬만한 함수는 다 흉내 낼 수 있다는 정리",
     "비선형 활성화 함수가 있을 때 성립해요. 그래서 비선형성이 있는 신경망이 강력해요."),
    ("역전파", "Backpropagation", "틀린 책임을 뒤에서 앞으로 나눠 주기",
     "손실 함수의 기울기를 출력 쪽에서 입력 쪽으로 연쇄 법칙으로 계산해요. 3주차 Part 2 의 주제예요."),
    ("순환 신경망", "Recurrent Neural Network (RNN)", "한 단어씩 읽으며 메모장(은닉 상태)에 요약을 고쳐 쓰는 사람",
     "기억을 가진 읽는 사람(a reader with memory)이에요. 3주차 Part 4 에서 배워요."),
    ("기울기", "Gradient", "손실이 가장 빨리 커지는 방향과 그 가파름",
     "학습은 기울기의 반대 방향으로 한 걸음씩 내려가요. 안개 낀 산의 발밑 기울기예요."),
    ("기울기 소실", "Vanishing Gradient", "귓속말 전달 게임에서 말이 점점 희미해지듯 기울기가 0으로 사라지는 문제",
     "시그모이드, tanh 는 양 끝에서 기울기가 거의 0이라 층이 깊어지면 앞쪽 층까지 기울기가 잘 안 가요."),
    ("트랜스포머", "Transformer", "어텐션으로 문장을 한꺼번에 보는 요즘 언어 모델의 기본 구조",
     "4주차에 배워요. 활성화 함수로 GELU 를 많이 써요."),
    ("행렬", "Matrix", "숫자를 가로세로 표 모양으로 늘어놓은 것",
     "shape 은 (행 수, 열 수)로 써요. (3,5) 행렬에 길이 5 벡터를 곱하면 길이 3 벡터가 나와요."),
    ("로지스틱 회귀", "Logistic Regression", "점수를 확률로 바꿔 분류하는 가장 단순한 선형 분류기",
     "클래스가 여러 개면 소프트맥스 회귀라고도 해요. 행렬 W 하나만 곱하므로 선형이에요."),
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

def TX(x, y, s, cls="t", size=16, anchor="middle", b=0):
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

def BOX(x, y, w, h, s, cls="box", tcls="tb", b=0, size=15):
    return R(x, y, w, h, cls, b) + TX(x + w / 2, y + h / 2 + size * 0.35, s, tcls, size, "middle", b)

def NODE(cx, cy, r, s, cls="n", b=0, size=14):
    return C(cx, cy, r, cls, b) + TX(cx, cy + size * 0.35, s, "tl", size, "middle", b)

def PL(pts, cls="e2", b=0):
    return f'<polyline points="{pts}" fill="none" class="{_c(cls, b)}"/>'

# p.4 파이프라인
FIG_PIPE = SVG(
    BOX(10, 100, 80, 44, "글", "box", "tb", 0, 16), A(92, 122, 118, 122),
    BOX(120, 100, 80, 44, "토큰", "box", "tb", 0, 16), A(202, 122, 228, 122),
    BOX(230, 100, 80, 44, "벡터", "box2", "tb", 0, 16), A(312, 122, 338, 122, "e2", 1),
    BOX(340, 100, 130, 44, "???", "box2", "tb", 1, 18),
    TX(270, 60, "지난주(2주차)까지", "tm", 14, "middle"),
    TX(405, 186, "오늘: 신경망", "tb", 16, "middle", 2),
    TX(405, 210, "벡터를 먹는 기계", "tm", 14, "middle", 2),
    TX(240, 250, "다음 목표: 다음 토큰 맞히기(언어 모델)", "tm", 14, "middle", 3),
)

# p.6 NER 창 분류
_w6 = ["the", "launch", "event", "in", "Busan", "drew", "big", "crowds"]
_els6 = []
for i, w in enumerate(_w6):
    x = 6 + i * 59
    cls = "n4" if w == "Busan" else ("n3" if 2 <= i <= 6 else "n")
    b = 0 if w == "Busan" or not (2 <= i <= 6) else 1
    _els6.append(R(x, 40, 54, 34, cls, 0 if cls == "n" else b))
    _els6.append(TX(x + 27, 62, w, "tl", 13))
for i in range(2, 7):
    _els6.append(L(6 + i * 59 + 27, 76, 240, 140, "e", 1))
FIG_WINDOW = SVG(
    TX(240, 24, "윈도우 m=2: 가운데 단어 앞 2개 + 뒤 2개", "tb", 15),
    *_els6,
    BOX(80, 142, 320, 40, "event, in, Busan, drew, big 벡터 이어 붙이기", "box2", "tb", 2, 14),
    A(240, 184, 240, 214, "e2", 3),
    BOX(110, 216, 260, 40, "분류기: Busan 은 장소일 확률?", "box", "tb", 3, 14),
)

# p.8 직선의 한계 (네 무리)
def _cluster(cx, cy, cls, b):
    return "".join(C(cx + dx, cy + dy, 5, cls, b) for dx, dy in [(-14, -6), (0, -12), (12, -4), (-6, 8), (10, 10), (0, 0)])

FIG_LINE = SVG(
    R(20, 20, 440, 230, "box"),
    _cluster(110, 80, "n4", 0), _cluster(370, 80, "n2", 0),
    _cluster(110, 195, "n2", 0), _cluster(370, 195, "n4", 0),
    TX(240, 140, "빨강 두 무리, 파랑 두 무리가 엇갈려 있어요", "tm", 14),
    L(30, 60, 450, 215, "e2", 1), TX(430, 245, "직선: 어떻게 그어도 실패", "tb", 14, "end", 1),
    PL("30,140 90,125 160,140 200,110 240,60 280,110 330,140 400,125 450,140", "hl", 2),
    TX(40, 40, "곡선이면 가를 수 있어요", "tb", 14, "start", 2),
)

# p.9 뉴런 하나
FIG_NEURON = SVG(
    NODE(40, 60, 18, "x1", "n"), NODE(40, 130, 18, "x2", "n"), NODE(40, 200, 18, "x3", "n"),
    L(58, 64, 172, 124, "e", 1), L(58, 130, 172, 132, "e", 1), L(58, 196, 172, 140, "e", 1),
    TX(115, 80, "w1", "tm", 14, "middle", 1), TX(115, 124, "w2", "tm", 14, "middle", 1), TX(115, 186, "w3", "tm", 14, "middle", 1),
    NODE(210, 132, 38, "합 + b", "n2", 1, 15),
    NODE(210, 232, 14, "1", "n3", 2, 13), L(210, 218, 210, 170, "e", 2), TX(222, 200, "b", "tm", 14, "start", 2),
    A(248, 132, 300, 132, "e2", 3), TX(274, 122, "z", "tb", 15, "middle", 3),
    BOX(302, 110, 60, 44, "f", "box2", "tb", 3, 18),
    A(364, 132, 410, 132, "e2", 4), TX(440, 138, "h", "tb", 18, "middle", 4),
    TX(210, 30, "가중합 + 편향 항", "tb", 14, "middle", 1), TX(332, 196, "활성화 함수", "tb", 14, "middle", 3),
)

# p.10 ReLU 와 시그모이드 모양
FIG_ACT = SVG(
    TX(120, 24, "시그모이드", "tb", 16), TX(360, 24, "ReLU", "tb", 16, "middle", 1),
    L(20, 150, 220, 150, "e"), L(120, 50, 120, 240, "e"),
    TX(128, 66, "1", "tm", 14, "start"), TX(128, 148, "0", "tm", 14, "start"),
    L(20, 70, 220, 70, "e"),
    PL("20,149 60,147 90,138 105,125 120,110 135,95 150,82 180,73 220,71", "e2"),
    TX(120, 262, "0과 1 사이로 눌러요", "tm", 14),
    L(260, 200, 460, 200, "e", 1), L(360, 50, 360, 240, "e", 1),
    PL("260,200 360,200 450,70", "e2", 1),
    TX(300, 190, "음수는 0", "tm", 14, "middle", 2), TX(300, 100, "양수는 그대로", "tm", 14, "middle", 2),
    TX(360, 262, "max(z, 0)", "tm", 14, "middle", 1),
)

# p.11 층이 합쳐짐
FIG_COLLAPSE = SVG(
    TX(240, 26, "활성화 함수 없이 쌓으면", "tb", 16),
    TX(30, 78, "x", "tb", 18), A(42, 72, 88, 72), BOX(90, 50, 80, 44, "W1", "box", "tb", 0, 16),
    A(172, 72, 218, 72), BOX(220, 50, 80, 44, "W2", "box", "tb", 0, 16), A(302, 72, 348, 72), TX(362, 78, "y", "tb", 18),
    TX(240, 126, "= 똑같아요 =", "tb", 16, "middle", 1),
    TX(30, 176, "x", "tb", 18, "middle", 1), A(42, 170, 128, 170, "e2", 1),
    BOX(130, 148, 170, 44, "W2W1 (행렬 하나)", "box2", "tb", 1, 15), A(302, 170, 348, 170, "e2", 1), TX(362, 176, "y", "tb", 18, "middle", 1),
    TX(240, 236, "사이에 f 를 끼우면 한 행렬로 못 합쳐요", "tb", 15, "middle", 2),
    TX(240, 260, "선형 섞기 → 휘기 → 선형 섞기 → 휘기", "tm", 14, "middle", 2),
)

# p.12 MLP
def _col(x, n, cls, b, top=60, gap=46):
    return [C(x, top + i * gap, 14, cls, b) for i in range(n)]

_mlp = []
_ys4 = [60 + i * 46 for i in range(4)]
_ys3 = [83, 129, 175]
for (xa, ya_list, xb, yb_list, b) in [(60, _ys4, 180, _ys4, 1), (180, _ys4, 300, _ys4, 2), (300, _ys4, 420, _ys3, 3)]:
    for ya in ya_list:
        for yb in yb_list:
            _mlp.append(L(xa + 14, ya, xb - 14, yb, "e", b))
FIG_MLP = SVG(
    *_mlp,
    *_col(60, 4, "n", 0), *_col(180, 4, "n4", 1), *_col(300, 4, "n4", 2),
    *[C(420, y, 14, "n2", 3) for y in _ys3],
    TX(60, 250, "입력 x", "tb", 14), TX(180, 250, "은닉 h(1)", "tb", 14, "middle", 1),
    TX(300, 250, "은닉 h(2)", "tb", 14, "middle", 2), TX(420, 250, "출력 ŷ", "tb", 14, "middle", 3),
    TX(120, 34, "W(1), b(1)", "tm", 14, "middle", 1), TX(240, 34, "W(2), b(2)", "tm", 14, "middle", 2),
    TX(360, 34, "U", "tm", 14, "middle", 3),
)

# p.13 합성곱 필터가 미끄러지기
_els13 = []
for i, w in enumerate(words):
    y = 30 + i * 36
    _els13.append(TX(62, y + 22, w, "t", 14, "end"))
    _els13.append(R(72, y + 4, 110, 28, "n"))
    _els13.append(TX(127, y + 23, str(vals[i]), "tl", 14))
FIG_CONV = SVG(
    *_els13,
    R(66, 30, 122, 108, "hl", 1), TX(198, 88, "필터 폭 3", "tb", 14, "start", 1),
    A(190, 104, 280, 104, "e2", 2),
    *[BOX(290, 36 + i * 40, 60, 32, str(v), "box2" if v == 5 else "box", "tb", 2, 15) for i, v in enumerate(fmap)],
    TX(320, 216, "특징 맵", "tb", 14, "middle", 2),
    A(354, 132, 400, 132, "e2", 3), BOX(404, 112, 62, 40, "5", "box2", "tb", 3, 18),
    TX(435, 176, "최대 풀링", "tb", 14, "middle", 3),
    TX(240, 262, "단어마다 숫자 하나로 줄인 장난감이에요 (실제는 벡터)", "tm", 13),
)

# p.14 위치가 달라도 최대 풀링 값은 같아요
def _fm(y, vs, b):
    out = []
    for i, v in enumerate(vs):
        out.append(BOX(40 + i * 60, y, 52, 34, str(v), "box2" if v == 5 else "box", "tb", b, 15))
    return "".join(out)

FIG_POOL = SVG(
    TX(20, 30, "문장 앞에 패턴이 있을 때", "tb", 14, "start"),
    _fm(44, [5, 1, 0, 0], 0), A(290, 61, 350, 61), BOX(356, 44, 60, 34, "5", "box2", "tb", 0, 16),
    TX(20, 132, "문장 뒤에 패턴이 있을 때", "tb", 14, "start", 1),
    _fm(146, [0, 0, 1, 5], 1), A(290, 163, 350, 163, "e2", 1), BOX(356, 146, 60, 34, "5", "box2", "tb", 1, 16),
    TX(240, 236, "최대 풀링 결과가 똑같이 5: 어디서 나왔는지는 버려요", "tb", 14, "middle", 2),
    TX(240, 260, "'어디서든 나왔나?' 만 남아요", "tm", 14, "middle", 2),
)

# ---------------- 쪽 ----------------
S = []

# p.1 표지
S.append({"p": 1, "title": "표지: 3강 Neural NLP Foundations", "terms": ["Natural Language Processing (NLP)", "Neural Network"],
    "pass1": [say(
        "3주차 강의 제목은 'Neural NLP Foundations' 예요.",
        f"뜻은 '신경망으로 하는 {NLP}의 기초' 예요.",
        f"과목 주문 기억하죠? {MANTRA}",
        f"오늘은 벡터를 받아 먹는 기계, {NN}을 만들어요.")],
    "pass2": [], "pass3": [], "pass4": []})

# p.2 Reminder
S.append({"p": 2, "title": "Reminder: 자료 배포 금지", "terms": ["Natural Language Processing (NLP)"],
    "pass1": [say(
        "안내 쪽이에요. 저작권이 있는 자료라 밖으로 퍼뜨리면 안 돼요.",
        f"{NLP} 수업 자료 전체에 똑같이 적용돼요.",
        "영상이나 소리에 문제가 있으면 바로 말해 달라는 부탁도 있어요.")],
    "pass2": [], "pass3": [], "pass4": []})

# p.3 목차
S.append({"p": 3, "title": "목차: 오늘 배울 네 부분", "terms": ["Neural Network", "Backpropagation", "Language Model (LM)", "Recurrent Neural Network (RNN)"],
    "pass1": [points("오늘 배울 네 부분",
        f"1. Neural Network Foundations: {NEU} 하나에서 깊은 {NN}까지 (이 파일)",
        f"2. Backpropagation: {BP}, 신경망이 배우는 방법",
        f"3. Language Modeling, the n-gram Era: 다음 단어를 세어서 맞히던 {LM}",
        f"4. Neural Language Models and RNNs: 기억을 가진 {RNN}")],
    "pass2": [], "pass3": [], "pass4": []})

# p.4 Recap
S.append({"p": 4, "title": "Recap: 지난주와 오늘", "terms": ["Byte Pair Encoding (BPE)", "word2vec", "Word Vector", "Neural Network", "Language Model (LM)", "Backpropagation"],
    "pass1": [
        say(f"지난주에는 글을 {TOK}으로 자르고({BPE}), {W2V}로 벡터를 만들었어요.",
            "그런데 벡터를 만들어 놓고 끝이 아니에요. 그 벡터를 먹고 답을 내는 기계가 필요해요.",
            f"그 기계가 오늘의 {NN}이에요."),
        figure("지금까지의 흐름과 오늘 채울 칸", FIG_PIPE, f"글 → 토큰 → 벡터 → ??? 의 빈칸을 {NN}으로 채워요.", 3),
    ],
    "pass2": [
        compare("슬라이드 영어 → 우리말 뜻", ["슬라이드 영어", "우리말 뜻"],
            ["meaning as vectors, learned by predicting neighbors", f"뜻을 벡터로, 이웃 단어를 맞히며 배워요({W2V})"],
            ["something has to consume those vectors", "그 벡터를 받아 먹을 무언가가 필요해요"],
            ["the machine that eats vectors", f"벡터를 먹는 기계 = {NN}"],
            ["the task that will carry us to GPT", f"GPT 까지 데려갈 과제 = 언어 모델링({LM})"],
            ["how does a network compute? how does it learn?", "신경망은 어떻게 계산하나? 어떻게 배우나?"]),
        points("오늘의 두 질문",
            f"계산: {NN}은 벡터를 받아 어떻게 답을 내나요? (Part 1, 이 파일)",
            f"학습: 좋은 {WT}는 어떻게 찾나요? ({BP}, Part 2)"),
        check("오늘 신경망이 입력으로 받는 것은 무엇인가요?",
            ["글자 그대로의 문장", "지난주에 만든 단어 벡터", "정답 레이블만"], 1,
            f"{W2V} 등으로 만든 {WV}가 {NN}의 입력이에요. 모델은 글을 직접 읽지 못해요."),
    ],
    "pass3": [
        look("슬라이드 짚어 읽기",
            (0.06, 0.195, 0.8, 0.045, f"'Last week': 지난주는 {BPE} 토큰화와 {W2V} 였어요."),
            (0.06, 0.255, 0.74, 0.045, "'text → tokens → vectors → ???': 벡터 다음 칸이 아직 비어 있어요."),
            (0.06, 0.315, 0.9, 0.045, f"'Today': 벡터를 먹는 기계({NN})와, GPT 까지 이어질 과제 언어 모델링({LM})."),
            (0.06, 0.375, 0.47, 0.045, "'New format': 이제부터 이론 2시간(쉬는 시간 포함) + 실습 1시간."),
            (0.06, 0.435, 0.8, 0.045, "'Assignment 2 goes out': 과제 2가 나가요. 15%, word2vec 기울기 + 구현, 7주차 마감.")),
        prof("오늘은 이론을 2시간 정도, 실습을 1시간 정도 해요.",
            "오늘 좀 큰 과제가 하나 나가고, 한 달쯤 뒤 10월 7일까지 내면 돼요.",
            f"과제 2에 {BP} 부분이 있어서 수업을 잘 들으면 어렵지 않게 할 수 있을 거예요."),
    ],
    "pass4": [
        warn("헷갈리기 쉬운 점",
            "과제 2 마감을 슬라이드는 'due W7'(7주차), 교수님은 '10월 7일' 이라고 말했어요. 공지를 꼭 확인해요.",
            f"과제 2는 {W2V}의 {GRAD} 계산과 구현이에요. 오늘 Part 2 {BP}와 이어지는 부분이에요.",
            f"지난주 {BPE}는 토큰을 만드는 쪽, {W2V}는 벡터를 만드는 쪽이에요. 둘을 섞지 않아요."),
    ]})

# p.5 Part 1 구분
S.append({"p": 5, "title": "Part 1: Neural Network Foundations", "terms": ["Neural Network", "Neuron"],
    "pass1": [say(
        "Part 1 시작이에요. 부제는 'from a single neuron to deep networks' 예요.",
        f"뜻: {NEU} 하나에서 시작해 깊은 {NN}까지 가 봐요.")],
    "pass2": [], "pass3": [], "pass4": []})

# p.6 NER
S.append({"p": 6, "title": "붙잡을 과제: NER", "terms": ["Named Entity Recognition (NER)", "Classification", "Window", "Center Word", "Word Vector"],
    "pass1": [
        say(f"기계를 만들기 전에 붙잡고 갈 예제 과제를 하나 정해요. {NER}이에요.",
            "글 속에서 사람, 기관, 장소 같은 이름을 찾아 종류를 붙이는 일이에요.",
            "예: 'Busan' 을 보면 '이건 장소(LOCATION)' 라고 붙여요."),
        figure("가운데 단어를 양옆 단어와 함께 보기", FIG_WINDOW,
            f"{CW} Busan 과 양옆 두 단어씩, 모두 다섯 단어의 {WV}를 이어 붙여 분류기에 넣어요.", 3),
    ],
    "pass2": [
        compare("슬라이드 영어 → 우리말 뜻", ["슬라이드 영어", "우리말 뜻"],
            ["A Task to Hold Onto", "(설명하는 동안) 붙잡고 갈 과제"],
            ["find and classify names in text", "글에서 이름을 찾아 종류를 가르기"],
            ["classify each word using its context window", f"단어마다 주변 {WIN}를 보고 {CLS}하기"],
            ["Concatenated word vectors in, a decision out", "이어 붙인 단어 벡터가 들어가고, 판정 하나가 나와요"],
            ["now we need the classifier", "이제 분류기(가운데 상자)를 만들어야 해요"]),
        points("이 쪽 용어 하나하나",
            f"{NER}: 이름을 찾아 사람, 기관, 장소 같은 종류를 붙이는 일",
            f"{CLS}: 정해진 여러 칸(클래스) 중 하나를 고르는 일. {NER}도 단어마다 {CLS}해요.",
            f"{WIN}: {CW} 양옆으로 몇 단어씩 함께 보는 창. m=2 면 양쪽 2개씩이에요.",
            f"{CW}: 지금 판단하려는 가운데 단어(여기서는 Busan)"),
        steps("창 분류가 흘러가는 순서", [
            "문장에서 판단할 단어(Busan)를 고르고 양옆 두 단어씩 잡아요",
            f"다섯 단어 각각의 {WV}(길이 d)를 꺼내요",
            "다섯 벡터를 옆으로 이어 붙여 길이 5d 벡터 하나를 만들어요",
            "분류기가 'Busan 이 장소일 확률' 을 내요"],
            "단어 벡터 이어 붙이기 → 분류기 → 확률 하나"),
        check(f"{NER}에서 'Busan' 에 붙을 알맞은 종류는?",
            ["PERSON(사람)", "LOCATION(장소)", "ORGANIZATION(기관)"], 1,
            "부산은 장소 이름이라 LOCATION 이에요. 사람 이름이면 PERSON 을 붙여요."),
    ],
    "pass3": [
        look("슬라이드 짚어 읽기",
            (0.06, 0.195, 0.64, 0.045, f"'named entity recognition (NER)': 오늘 계속 쓸 예제 과제 {NER}."),
            (0.32, 0.38, 0.27, 0.045, "'window (m = 2) around the center word': 가운데 단어 둘레 창, 양쪽 2단어씩."),
            (0.452, 0.44, 0.07, 0.078, f"Busan: 판단할 {CW}. 주황색으로 칠해져 있어요."),
            (0.275, 0.615, 0.36, 0.083, "x_window: 다섯 단어 벡터를 이어 붙인 것. 길이가 5d 예요."),
            (0.34, 0.76, 0.32, 0.045, "'P(center word is a LOCATION)': 가운데 단어가 장소일 확률.")),
        formula("창 벡터의 모양", r"x_{\text{window}} = [\,x_{\text{event}}\;\; x_{\text{in}}\;\; x_{\text{Busan}}\;\; x_{\text{drew}}\;\; x_{\text{big}}\,] \in \mathbb{R}^{5d}", [
            (r"x_{\text{Busan}}", f"Busan 의 {WV}. 길이 d"),
            (r"[\;\cdots\;]", "다섯 벡터를 옆으로 줄 세워 이어 붙이기"),
            (r"\mathbb{R}^{5d}", "숫자 5d 개짜리 벡터라는 뜻. d=100 이면 500개")],
            "창 안 다섯 단어의 벡터를 이어 붙여 긴 벡터 하나로 만들어요."),
        prof("부산이 나오면 위치구나, 사람 이름이 나오면 사람 이름이구나, 이렇게 태그를 달아 주는 게 NER 이에요.",
            "한 단어만 보고 바로 맞히는 게 아니라 주변 컨텍스트 윈도우와 함께 봐요.",
            "지난주에 만든 워드 벡터가 여기서 입력으로 쓰여요."),
        bg("기초 다지기 1단원", "벡터는 숫자를 줄 세운 것이고, 줄 선 숫자 개수가 차원이에요.",
            "길이 d 벡터 다섯 개를 이어 붙이면 길이 5d 벡터가 돼요."),
    ],
    "pass4": [
        check("단어 벡터가 d=50 차원이고 윈도우 m=2 일 때 x_window 의 길이는?",
            ["50", "100", "250", "500"], 2,
            "가운데 단어 + 양쪽 2개씩 = 5단어, 5 × 50 = 250이에요."),
        english("외워 쓸 답안 문장",
            f"창 기반 {NER}은 {CW}와 양옆 단어의 벡터를 이어 붙여 분류기로 종류를 {CLS}한다.",
            "창(window) → 이어 붙이기(concatenate) → 분류기 → 확률.",
            "'창, 이어 붙이기, 분류기' 세 낱말을 순서대로 외워요."),
    ]})

# p.7 분류의 기본 세팅
S.append({"p": 7, "title": "분류의 기본 세팅", "terms": ["Supervised Learning", "Label", "Softmax", "Logit", "Cross-Entropy", "Loss Function", "Logistic Regression", "Matrix", "Classification"],
    "pass1": [
        say(f"분류기의 가장 단순한 모양부터 봐요. 이건 {SUP}이에요.",
            f"문제(입력)와 정답({LAB})을 짝으로 잔뜩 주고 배우게 해요."),
        analogy("점수를 확률로, 틀리면 벌점",
            f"모델이 칸마다 점수를 매기면 {SMX}가 확률 파이로 나눠요. 정답 칸 조각이 작으면 벌점을 크게 받아요.",
            ["칸마다 매긴 점수", f"{LOGIT}"], ["모두 더해 1인 확률 파이", f"{SMX}"], ["틀린 만큼 받는 벌점", f"{LOSS}({CE})"]),
    ],
    "pass2": [
        compare("슬라이드 영어 → 우리말 뜻", ["슬라이드 영어", "우리말 뜻"],
            ["Supervised learning: pairs {x, y}", f"{SUP}: (입력, 정답) 짝으로 배우기"],
            ["scores for every class, squashed into probabilities", "클래스마다 점수를 매겨 확률로 눌러 담기"],
            ["Train by making the true class likely", "정답 클래스의 확률이 커지도록 학습"],
            ["softmax + NLL, week 2's friend", f"{SMX} + 음의 로그 우도(NLL), 2주차에 본 친구"],
            ["just logistic regression, a LINEAR machine", f"그냥 {LOGREG}, 즉 선형 기계예요"]),
        points("이 쪽 용어 하나하나",
            f"{SUP}: 입력 x 와 정답 {LAB} y 를 짝으로 주고 배우게 하는 방법",
            f"{LOGIT}: Wx 로 얻은 날것 점수. 음수도 될 수 있고 확률이 아니에요.",
            f"{SMX}: {LOGIT}을 0~1 사이, 합이 1인 확률로 바꿔요.",
            f"{CE}: 정답 칸 확률의 -log 를 평균 낸 {LOSS}예요."),
        steps("분류기 한 번 돌리기", [
            f"입력 x 에 {MAT} W 를 곱해 클래스마다 {LOGIT}(점수)을 얻어요",
            f"{SMX}로 점수를 확률로 바꿔요",
            "정답 클래스의 확률을 봐요",
            f"그 확률의 -log 가 벌점, 즉 {CE} {LOSS}예요",
            "벌점이 줄어드는 쪽으로 W 를 고쳐요"],
            "점수 → 확률 → 벌점 → W 고치기"),
        check(f"{LOGIT}(점수)에 대한 설명으로 맞는 것은?",
            ["항상 0과 1 사이다", "음수도 나올 수 있고 확률이 아니다", "다 더하면 1이다"], 1,
            f"{LOGIT}은 Wx 라서 음수도 나와요. 0~1, 합 1 은 {SMX}를 통과한 뒤의 성질이에요."),
    ],
    "pass3": [
        look("슬라이드 짚어 읽기",
            (0.06, 0.195, 0.56, 0.045, f"'a training set of pairs {{x_i, y_i}}': 입력과 정답 {LAB}의 짝 모음."),
            (0.245, 0.335, 0.465, 0.165, f"{SMX} 분류기 식. 정답 칸 점수의 exp 를 모든 칸 exp 합으로 나눠요."),
            (0.06, 0.56, 0.64, 0.045, f"'cross-entropy loss (softmax + NLL)': {CE}는 {SMX} 뒤에 음의 로그를 붙인 것."),
            (0.29, 0.67, 0.4, 0.12, "J(θ): 학습 자료 N개에서 정답 확률의 -log 를 평균 낸 값."),
            (0.32, 0.855, 0.37, 0.045, f"'just logistic regression, a LINEAR machine': 아직은 선형인 {LOGREG}.")),
        formula(f"{SMX} 분류기", r"P(y \mid x) = \mathrm{softmax}(Wx)_y = \frac{\exp(W_y x)}{\sum_c \exp(W_c x)}", [
            (r"W", f"가중치 {MAT}. 한 줄(행)이 클래스 하나를 맡아요"),
            (r"W_y x", f"정답 후보 y 칸의 점수({LOGIT})"),
            (r"\exp(\cdot)", "점수를 늘 양수로 바꾸는 지수 함수"),
            (r"\sum_c", "모든 클래스 c 의 값을 다 더하기"),
            (r"P(y \mid x)", "x 를 봤을 때 답이 y 일 확률")],
            f"점수에 exp 를 씌우고 전체 합으로 나누면 합이 1인 확률이 돼요."),
        formula(f"{CE} {LOSS}", r"J(\theta) = \frac{1}{N}\sum_{i=1}^{N} -\log P(y_i \mid x_i)", [
            (r"\theta", f"모든 {PAR}(여기서는 W)"),
            (r"P(y_i \mid x_i)", f"i번째 문제에서 정답 {LAB}에 준 확률"),
            (r"-\log", "확률이 작을수록 크게 커지는 벌점"),
            (r"\frac{1}{N}\sum", "문제 N개의 벌점 평균")],
            "정답에 준 확률의 -log 를 평균 내요. 이 값을 줄이는 게 학습이에요."),
        steps(f"손계산: {SMX}와 {CE}", [
            "점수: PERSON 1, LOCATION 3, ORG 0 (정답은 LOCATION)",
            "exp: e¹ ≈ 2.72, e³ ≈ 20.09, e⁰ = 1, 합 ≈ 23.80",
            "확률: 2.72/23.80 ≈ 0.11, 20.09/23.80 ≈ 0.84, 1/23.80 ≈ 0.04",
            "벌점: -log(0.84) ≈ 0.17",
            "비교: 정답에 0.9 를 주면 -log 0.9 ≈ 0.11, 0.01 을 주면 -log 0.01 ≈ 4.61"],
            "정답 확률 0.84 → 벌점 약 0.17. 정답 확률이 작을수록 벌점이 크게 뛰어요.",
            "로그는 자연로그(ln) 예요."),
        prof("Wx 로 얻은 값을 로짓 혹은 스코어라고 해요. 이 점수 자체는 확률이 아니고 음수도 나올 수 있어요.",
            "정답이 로케이션일 때 로케이션에 0.9 를 주면 잘한 것, 0.01 을 주면 굉장히 잘못한 거예요.",
            "소프트맥스와 NLL 을 같이 한 걸 크로스 엔트로피 로스라고 해요.",
            "중요한 건 W 가 단 하나의 행렬로 표현된다는 것, 즉 모델이 선형이라는 거예요."),
        bg("기초 다지기 6단원", f"{SMX}는 점수 → 확률, {CE}는 정답 확률의 -log 를 벌점으로 쓰는 것이에요.",
            "로그와 exp 가 낯설면 기초 다지기 4단원을 먼저 봐요."),
    ],
    "pass4": [
        check(f"정답 클래스에 준 확률이 0.01 에서 0.9 로 올라가면 {CE}는?",
            ["커진다", "작아진다", "변하지 않는다"], 1,
            "-log 0.01 ≈ 4.61, -log 0.9 ≈ 0.11 이라 벌점이 작아져요."),
        english("외워 쓸 답안 문장",
            f"{SMX} 분류기는 {LOGIT}(Wx)을 확률로 바꾸고, {CE} {LOSS}는 정답 클래스 확률의 음의 로그를 평균 낸 값이다.",
            f"W 가 {MAT} 하나뿐이라 이 분류기는 선형({LOGREG})이다.",
            "점수 → 확률 → -log 평균, 세 단계로 외워요."),
        warn("헷갈리기 쉬운 점",
            f"{SMX}가 곧 {CE}는 아니에요. {SMX} + NLL(-log) = {CE}예요.",
            f"{LOGREG}는 이름에 '회귀' 가 있지만 {CLS} 모델이에요."),
    ]})

# p.8 직선의 한계
S.append({"p": 8, "title": "선형의 한계", "terms": ["Linear Classifier", "Hyperplane", "Decision Boundary", "Nonlinearity"],
    "pass1": [
        say(f"지금까지 만든 분류기는 {LINC}예요. 곧은 선 하나로만 무리를 갈라요.",
            "그런데 곧은 선 하나로는 못 가르는 모양이 있어요."),
        figure("곧은 선으로는 못 가르는 배치", FIG_LINE,
            f"빨강 두 무리와 파랑 두 무리가 엇갈려 있으면 직선은 실패해요. 휘어진 {DB}가 필요해요.", 2),
    ],
    "pass2": [
        compare("슬라이드 영어 → 우리말 뜻", ["슬라이드 영어", "우리말 뜻"],
            ["The Limit of Linear", "선형의 한계"],
            ["can only draw a straight line (hyperplane)", f"곧은 선({HYP})만 그을 수 있어요"],
            ["a LINE cannot separate these", "선 하나로는 이것들을 못 갈라요"],
            ["a CURVED boundary can, we need nonlinearity", f"휘어진 경계면 돼요, {NONLIN}이 필요해요"],
            ["\"not bad\" is not the sum of \"not\" and \"bad\"", "'not bad' 는 'not' 과 'bad' 를 그냥 더한 뜻이 아니에요"]),
        points("이 쪽 용어 하나하나",
            f"{LINC}: {MAT} W 하나만 곱하는 분류기. 경계가 곧아요.",
            f"{DB}: 'A 쪽, B 쪽' 을 가르는 경계선",
            f"{HYP}: 곧은 경계. 2차원이면 선, 3차원이면 면이에요.",
            f"{NONLIN}: 경계를 휘게 만드는 성질"),
        check(f"{LINC}의 {DB} 모양은?",
            ["항상 곧은 선(평면)", "원하는 대로 휘어진 곡선", "점 하나"], 0,
            f"{LINC}는 {HYP}, 즉 곧은 경계만 그을 수 있어요."),
    ],
    "pass3": [
        look("슬라이드 짚어 읽기",
            (0.06, 0.195, 0.55, 0.045, f"'only draw a straight line (hyperplane)': {LINC}는 {HYP}만 그어요."),
            (0.115, 0.285, 0.385, 0.45, "왼쪽: 빨강이 왼위, 오른아래, 파랑이 오른위, 왼아래. 빨간 점선 하나로는 못 갈라요."),
            (0.53, 0.285, 0.39, 0.45, f"오른쪽: 초록 곡선이면 갈라져요. 그래서 {NONLIN}이 필요해요."),
            (0.22, 0.855, 0.57, 0.045, "'not bad': 'not' 이 뒤 단어에 따라 역할이 바뀌는 상호작용이에요.")),
        prof("왼쪽 그림은 XOR 같은 패턴이에요. 어떻게 직선을 그어도 파란색과 빨간색을 완벽히 못 갈라요.",
            "good 은 긍정, bad 는 부정인데 not 이 붙으면 not good 은 부정, not bad 는 오히려 긍정이 돼요.",
            "not 이 늘 같은 값을 더하는 게 아니라 뒤 단어에 따라 역할이 달라져요.",
            "이런 피처 사이 상호작용을 표현하게 해 주는 게 비선형 활성화를 가진 뉴런이에요."),
        points("말과 그림을 짝지으면",
            "왼쪽 그림처럼, 'not' 과 'bad' 를 따로 더해서는 'not bad' 의 긍정을 못 맞혀요.",
            "두 특징이 함께 있을 때 뜻이 뒤집히는 걸 상호작용(interaction)이라고 해요.",
            f"상호작용을 잡으려면 휘어진 {DB}, 즉 {NONLIN}이 필요해요."),
    ],
    "pass4": [
        check("'not bad' 가 선형 모델에게 어려운 까닭은?",
            ["단어가 너무 길어서", "두 단어가 합쳐질 때 뜻이 뒤집히는 상호작용이라서", "사전에 없는 단어라서"], 1,
            f"'not' 이 뒤 단어에 따라 역할이 바뀌어요. 효과를 따로 더하는 {LINC}로는 못 잡아요."),
        english("외워 쓸 답안 문장",
            f"{LINC}는 {HYP}만 그어서 XOR 배치나 'not bad' 같은 상호작용을 못 잡으므로 {NONLIN}이 필요하다.",
            "곧은 선의 한계 → 휘어진 경계 → 비선형성.", None),
    ]})

# p.9 뉴런
S.append({"p": 9, "title": "뉴런 하나", "terms": ["Neuron", "Weight", "Weighted Sum", "Bias Term", "Activation Function", "Nonlinearity", "ReLU", "Sigmoid"],
    "pass1": [
        say(f"{NN}의 벽돌 한 장이 {NEU}이에요.",
            f"{NEU}은 입력마다 중요도를 곱해 더하고, 마지막에 한 번 휘어서 내보내요.",
            "슬라이드 말로는 '작고 배울 수 있는 패턴 탐지기' 예요."),
        figure(f"{NEU} 하나가 하는 일", FIG_NEURON,
            f"입력 × {WT}를 더하고({WS}) {BIAS} b 를 더한 z 를 {ACT} f 에 통과시켜 h 를 내요.", 4),
    ],
    "pass2": [
        compare("슬라이드 영어 → 우리말 뜻", ["슬라이드 영어", "우리말 뜻"],
            ["weighted sum + bias, passed through a nonlinearity", f"{WS} + {BIAS}, 그다음 {NONLIN} 통과"],
            ["weighted sum (affine transform)", f"{WS}(아핀 변환): wᵀx + b"],
            ["loosely inspired by biology", "생물의 신경세포에서 느슨하게 따온 이름"],
            ["a tiny, learnable feature detector", "작고, 배울 수 있는 특징 탐지기"],
            ["One neuron = one learned pattern detector", f"{NEU} 하나 = 학습된 패턴 탐지기 하나"]),
        points("이 쪽 용어 하나하나",
            f"{WT}: 입력마다 얼마나 중요하게 볼지 곱하는 숫자 w",
            f"{WS}: 입력 × {WT}를 모두 더한 값",
            f"{BIAS}: 더해 주는 숫자 b. 켜지는 기준을 옮겨요.",
            f"{ACT}: z 를 휘어진 값 f(z) 로 바꾸는 함수. {NONLIN}을 넣는 부품이에요."),
        steps(f"{NEU} 안의 순서", [
            "입력 x₁, x₂, ..., x_d 가 들어와요",
            f"각 입력에 {WT} w 를 곱해요",
            f"모두 더하고 {BIAS} b 를 더해 z 를 얻어요",
            f"z 를 {ACT} f 에 넣어 h = f(z) 를 내보내요"],
            "곱하고 → 더하고 → b 더하고 → 휘기"),
        check(f"{NEU}에서 {BIAS} b 는 언제 더하나요?",
            [f"{ACT}를 통과한 뒤", f"{WS}에 더한 뒤 {ACT}에 넣기 전", "입력에 곱하기 전"], 1,
            f"z = wᵀx + b 를 먼저 만들고, 그 z 를 {ACT}에 넣어요."),
    ],
    "pass3": [
        look("슬라이드 짚어 읽기",
            (0.19, 0.26, 0.05, 0.37, "x₁ ... x_d: 입력 벡터의 숫자들. 선마다 w₁ ... w_d 가 붙어 있어요."),
            (0.36, 0.33, 0.125, 0.19, f"Σ wᵢxᵢ + b: {WS}에 {BIAS}를 더한 것. 아래 'weighted sum (affine transform)'."),
            (0.40, 0.54, 0.045, 0.105, f"아래 '1' 과 b: 늘 1인 입력에 b 를 곱해 더한다고 그린 {BIAS}."),
            (0.535, 0.375, 0.105, 0.1, f"f( ): {ACT}. 아래에 'nonlinearity' 라고 적혀 있어요."),
            (0.69, 0.395, 0.145, 0.1, "h = f(wᵀx + b): 뉴런의 출력(output)."),
            (0.69, 0.515, 0.25, 0.345, "생물 신경세포 그림. 이름만 따왔고 실제로는 작은 특징 탐지기예요.")),
        formula(f"{NEU}의 식", r"h = f(\mathbf{w}^{\top}\mathbf{x} + b) = f\Big(\sum_{i=1}^{d} w_i x_i + b\Big)", [
            (r"\mathbf{x}", "입력 벡터 (숫자 d 개)"),
            (r"\mathbf{w}", f"{WT} 벡터 (입력마다 하나)"),
            (r"\mathbf{w}^{\top}\mathbf{x}", f"{WS}: 짝끼리 곱해서 더하기(내적)"),
            (r"b", f"{BIAS}"),
            (r"f", f"{ACT}"),
            (r"h", "뉴런의 출력")],
            f"곱해서 더하고 b 를 더한 뒤 f 로 휘면 {NEU} 하나의 출력이에요."),
        steps(f"손계산: 입력 3개짜리 {NEU}", [
            "z = 0.5×1 + (-1)×2 + 0.5×3 + 0.5",
            "= 0.5 - 2 + 1.5 + 0.5 = 0.5",
            f"{RELU}: max(0.5, 0) = 0.5",
            f"{SIG}: 1/(1+e^(-0.5)) ≈ 0.62",
            "입력이 x = [1, 3, 1] 이면 z = -1.5 → ReLU 0 (꺼짐), 시그모이드 ≈ 0.18"],
            "z = 0.5, ReLU 출력 0.5, 시그모이드 출력 약 0.62",
            "x = [1, 2, 3], w = [0.5, -1, 0.5], b = 0.5"),
        prof("입력마다 가중치를 곱하는데, 어떤 입력은 중요하게 보고 어떤 입력은 덜 중요하게 봐요.",
            "w 를 곱하고 b 를 더하는 건 아핀 변환이라고도 부르는 선형 계산 하나예요.",
            "뉴런 하나가 하는 일은 입력을 적절히 조합해 패턴 하나를 찾는 거예요.",
            "여러 뉴런의 w 를 모아 놓은 게 앞에서 본 큰 행렬 W 예요."),
        bg("기초 다지기 9단원", f"{NEU} = {WS} + {BIAS} + {ACT}. 층, 순전파 이야기가 이어져요.",
            "wᵀx 는 내적이에요. 곱해서 더하기가 낯설면 기초 다지기 2단원을 봐요."),
    ],
    "pass4": [
        check(f"x = [2, 1], w = [1, -3], b = 0 인 {NEU}에 {RELU}를 쓰면 출력은?",
            ["-1", "0", "1", "5"], 1,
            "z = 1×2 + (-3)×1 + 0 = -1. 음수라서 ReLU 는 0으로 꺼요."),
        english("외워 쓸 답안 문장",
            f"{NEU}은 {WS}에 {BIAS}를 더한 z 를 {ACT}에 통과시켜 h = f(wᵀx + b) 를 낸다.",
            "곱하기 → 더하기 → b → f.", "식 h = f(wᵀx + b) 하나로 외워요."),
        warn("헷갈리기 쉬운 점",
            f"여기의 {BIAS}(b)는 사회적 편향(Bias)과 전혀 다른 말이에요.",
            f"{ACT}를 빼면 {NEU}은 그냥 선형 계산이에요. 비선형은 f 에서만 생겨요."),
    ]})

# p.10 활성화 함수 메뉴
S.append({"p": 10, "title": "비선형 함수 메뉴", "terms": ["Activation Function", "Sigmoid", "tanh", "ReLU", "GELU", "Transformer", "Vanishing Gradient", "Gradient", "Nonlinearity"],
    "pass1": [
        say(f"{NEU} 끝의 f 자리에 넣을 {ACT}의 메뉴판이에요.",
            f"옛날부터 쓰던 S자 {SIG}, 요즘 기본인 {RELU}, {TRF}가 쓰는 {GELU}가 있어요."),
        figure("두 대표 선수의 모양", FIG_ACT,
            f"{SIG}는 0~1 로 눌러 주고, {RELU}는 음수를 0으로 끄고 양수는 그대로 보내요.", 2),
    ],
    "pass2": [
        compare("슬라이드 영어 → 우리말 뜻", ["슬라이드 영어", "우리말 뜻"],
            ["sigmoid/tanh: classic, squashing", f"{SIG}, {TANH}: 오래된 S자, 값을 눌러 담아요"],
            ["still used for probabilities and gates", "지금도 확률과 게이트(LSTM)에 써요"],
            ["ReLU: max(0, x), cheap, trains fast, the workhorse", f"{RELU}: 계산이 싸고 학습이 빠른 딥러닝의 일꾼"],
            ["GELU: smooth ReLU, what Transformers use", f"{GELU}: 부드러운 ReLU, {TRF}가 써요"],
            ["ReLU/GELU inside, sigmoid only when you need a probability", "안쪽 층은 ReLU/GELU, 확률이 필요할 때만 시그모이드"]),
        compare("네 함수 구별하기", ["함수", "출력 범위", "주로 쓰는 곳"],
            [f"{SIG}", "0 ~ 1", "확률, 게이트"],
            [f"{TANH}", "-1 ~ 1", "게이트, 실습 N3L p.3 의 h = tanh(z)"],
            [f"{RELU}", "0 ~ 무한대", "안쪽 층의 기본 선택"],
            [f"{GELU}", "대략 -0.17 ~ 무한대 (ReLU 와 비슷)", f"{TRF}"]),
        check(f"확률처럼 0과 1 사이 값이 필요할 때 쓰는 {ACT}는?",
            [f"{RELU}", f"{SIG}", f"{GELU}"], 1,
            f"{SIG}의 출력은 늘 0과 1 사이라 확률이나 게이트에 딱 맞아요."),
    ],
    "pass3": [
        look("슬라이드 짚어 읽기",
            (0.065, 0.4, 0.145, 0.35, f"Logistic('sigmoid'): f(z) = 1/(1+e^(-z)). 0~1 S자 곡선."),
            (0.21, 0.4, 0.13, 0.35, f"tanh: -1~1 S자. {SIG}와 모양이 비슷해요."),
            (0.505, 0.39, 0.14, 0.36, f"ReLU(Rectified Linear Unit): f(z) = max(z, 0). 꺾인 직선."),
            (0.66, 0.385, 0.135, 0.365, "Leaky / Parametric ReLU: 음수 쪽에도 작은 기울기(αz)를 남겨요."),
            (0.8, 0.39, 0.155, 0.36, f"GELU(Gaussian Error Linear Unit): 0 근처가 부드러운 ReLU."),
            (0.23, 0.855, 0.55, 0.045, "'Default advice': 안쪽은 ReLU/GELU, 확률이 필요할 때만 sigmoid.")),
        formula(f"{SIG}와 {RELU}", r"\sigma(z) = \frac{1}{1 + e^{-z}}, \qquad \mathrm{ReLU}(z) = \max(z, 0)", [
            (r"\sigma(z)", f"{SIG}. 늘 0과 1 사이"),
            (r"e^{-z}", "z 가 크면 0에 가까워져서 σ 가 1에 가까워져요"),
            (r"\max(z, 0)", "z 와 0 중 큰 쪽. 음수면 0, 양수면 z 그대로"),
            (r"z", f"{NEU}의 {WS} + {BIAS} 값")],
            f"{SIG}는 눌러 담고, {RELU}는 음수만 꺼요."),
        steps("손계산: 값 넣어 보기", [
            "ReLU(-2) = 0, ReLU(0) = 0, ReLU(3) = 3",
            "σ(0) = 1/(1+1) = 0.5",
            "σ(4) ≈ 0.98, σ(-4) ≈ 0.02",
            "σ 는 4 에서 이미 1 가까이 붙어서, 더 커져도 거의 안 변해요(기울기 거의 0)",
            "ReLU 는 양수 쪽 기울기가 늘 1이에요"],
            "양 끝에서 시그모이드는 평평해지고, ReLU 는 양수 쪽이 계속 기울어 있어요."),
        prof("시그모이드는 0에서 1, tanh 는 -1에서 1 사이 값을 가져요. 시그모이드는 확률이나 LSTM 게이트에 써요.",
            "딥러닝에서 가장 중요한 함수 중 하나가 ReLU 예요. 음수면 0으로 끄고 양수면 기울기 1로 그대로 보내요.",
            "시그모이드, tanh 는 양 끝에서 기울기가 거의 0이라 깊이 쌓으면 기울기가 사라지는 문제가 생겨요.",
            "ReLU 를 썼을 때 가장 성능이 좋았고, LLM 이전 대부분의 모델은 ReLU 를 썼어요."),
        prof("ReLU 는 음수에서 기울기가 0이라 계속 꺼져 버리는 현상(dying ReLU)이 있어요.",
            "그래서 음수도 조금 보내 주는 Leaky ReLU, 부드럽게 변하는 GELU 가 나왔어요.",
            "기억할 것: 시그모이드는 확률이나 게이트, ReLU 는 단순하고 효과적인 기본 선택, GELU 는 트랜스포머."),
    ],
    "pass4": [
        check(f"{SIG}, {TANH}를 깊게 쌓을 때 생기는 문제로 교수님이 말한 것은?",
            [f"{VG}", "어휘가 너무 커지는 문제", "토큰이 잘게 쪼개지는 문제"], 0,
            f"양 끝에서 {GRAD}가 거의 0이라, 층이 깊으면 {GRAD}가 앞쪽까지 잘 안 가요. 이것이 {VG}예요."),
        check(f"{RELU}의 약점으로 맞는 것은?",
            ["출력이 늘 0~1 이다", "음수 입력에서 기울기가 0이라 뉴런이 꺼진 채 남을 수 있다", "계산이 매우 비싸다"], 1,
            "음수 쪽 기울기가 0이라 계속 꺼지는 현상이 있어요. 그래서 Leaky ReLU, GELU 가 나왔어요."),
        english("외워 쓸 답안 문장",
            f"{RELU}는 싸고 {VG}가 적어 기본으로, {SIG}는 확률과 게이트에, {GELU}는 {TRF}에 쓴다.",
            "ReLU = 기본, 시그모이드 = 확률/게이트, GELU = 트랜스포머.",
            "교수님이 '기억해야 할 것' 이라고 짚은 세 줄이에요."),
    ]})

# p.11 비선형성이 꼭 필요한 이유
S.append({"p": 11, "title": "비선형성은 선택이 아니다", "terms": ["Nonlinearity", "Matrix", "Activation Function", "Hyperplane", "Decision Boundary", "Universal Approximation Theorem", "Neural Network"],
    "pass1": [
        say(f"{ACT}를 빼고 층만 여러 개 쌓으면 어떻게 될까요?",
            f"놀랍게도 층 여러 개가 {MAT} 하나와 똑같아져요. 깊게 쌓은 보람이 없어요.",
            f"그래서 {NONLIN}은 넣어도 되고 안 넣어도 되는 게 아니라 꼭 넣어야 해요."),
        figure("선형층 두 개 = 선형층 하나", FIG_COLLAPSE,
            f"W1, W2 를 이어 곱하면 W2W1 이라는 {MAT} 하나가 돼요. 사이에 f 를 끼워야 합쳐지지 않아요.", 2),
    ],
    "pass2": [
        compare("슬라이드 영어 → 우리말 뜻", ["슬라이드 영어", "우리말 뜻"],
            ["Why Nonlinearity Is Not Optional", f"왜 {NONLIN}은 선택이 아닌가"],
            ["stacked linear layers collapse into one affine map", "쌓은 선형층은 변환 하나로 무너져 합쳐져요"],
            ["depth buys nothing", "깊게 쌓아도 얻는 게 없어요"],
            ["linear mix → bend → linear mix → bend", "선형으로 섞고 → 휘고 → 섞고 → 휘기"],
            ["No f, no deep learning", "f 가 없으면 딥러닝도 없어요"]),
        points("이 쪽 용어 하나하나",
            f"{MAT}: 숫자를 표 모양으로 늘어놓은 것. 선형층 하나가 {MAT} 하나예요.",
            f"{NONLIN}: 곧은 변환 사이에서 공간을 휘게 하는 성질. f 가 만들어요.",
            f"{UAT}: 은닉 뉴런이 충분하면 웬만한 함수는 다 흉내 낼 수 있다는 정리"),
        steps("오른쪽 그림(With nonlinearity) 흐름", [
            "Input space: 곧은 격자(입력 공간)",
            "선형층이 공간을 섞고, 돌리고, 늘이고, 줄여요",
            "f 가 격자를 휘어요(After nonlinearity: grid is bent)",
            f"휜 공간에서는 동그란 {DB}도 만들 수 있어요"],
            "섞기와 휘기를 반복할수록 더 복잡한 경계를 표현해요."),
        check(f"{ACT} 없이 선형층 10개를 쌓으면?",
            ["선형층 1개와 표현력이 같다", "10배 강해진다", "곡선 경계를 그릴 수 있다"], 0,
            f"모두 곱하면 {MAT} 하나가 돼서 선형층 1개와 같아요."),
    ],
    "pass3": [
        look("슬라이드 짚어 읽기",
            (0.08, 0.2, 0.36, 0.075, "'Without nonlinearity': 쌓은 선형층이 변환 하나로 합쳐져요."),
            (0.15, 0.42, 0.21, 0.1, "W₂(W₁x) = (W₂W₁)x, 'depth buys nothing': 깊이가 소용없어요."),
            (0.11, 0.55, 0.33, 0.24, "왼쪽 아래: 선형층을 여러 개 써도 결국 곧은 경계 하나."),
            (0.53, 0.405, 0.28, 0.1, "W₂ f(W₁x + b₁) + b₂: 가운데 f 가 끼어 있어요. 선형 섞기 → 휘기."),
            (0.485, 0.54, 0.38, 0.26, "격자가 휘고(After nonlinearity), 동그란 결정 경계가 생겨요."),
            (0.21, 0.815, 0.59, 0.045, f"'Universal approximation Theorem': {UAT}. (슬라이드의 'funciton' 은 function 오타)")),
        formula("층이 합쳐지는 식", r"W_2(W_1 x) = (W_2 W_1)\,x = W' x", [
            (r"W_1, W_2", "선형층 두 개의 가중치 행렬"),
            (r"W_2 W_1", "행렬끼리 먼저 곱할 수 있어요(결합 법칙)"),
            (r"W'", f"곱한 결과, 새 {MAT} 하나"),
            (r"x", "입력 벡터")],
            f"f 없이 쌓은 층은 {MAT} 하나 W' 로 바꿔 쓸 수 있어요. 층 수가 의미 없어져요."),
        steps("손계산: 작은 행렬로 확인하기", [
            "W1 = [[1, 2], [0, 1]], W2 = [[1, 0], [1, 1]], x = [1, 1]",
            "한 층씩: W1x = [3, 1], 그다음 W2[3, 1] = [3, 4]",
            "먼저 합치기: W2W1 = [[1, 2], [1, 3]], (W2W1)x = [3, 4]",
            "두 방법의 답이 똑같아요 → 두 층 = 행렬 하나",
            "사이에 ReLU: V1 = [[1, -2], [0, 1]] 이면 V1x = [-1, 1] → ReLU → [0, 1] → W2 → [0, 1]",
            "ReLU 없이 합치면 (W2V1)x = [-1, 0]. 답이 달라져서 하나로 못 합쳐요"],
            "f 가 없으면 층이 합쳐지고, f 를 끼우면 합쳐지지 않아요."),
        prof("w1 과 w2 를 먼저 곱하든 따로 곱하든, 결국 w1 과 w2 를 곱한 하나의 선형 변환이에요.",
            "레이어를 2개 쌓았는데 큰 레이어 하나를 쌓은 것과 같은 결과가 나와요. 논리니어티가 없으면 깊게 쌓는 의미가 없어요.",
            "직관적으로 선형층은 공간을 섞고 회전하고 늘리고 줄이고, 비선형은 그 공간을 접거나 구부려요."),
        prof("하이퍼플레인은 n차원이면 n-1차원이에요. 2차원이면 선, 3차원이면 면이에요.",
            "2차원에서 선으로 못 가르던 점들도, 높이를 더해 빨간 점은 높이, 파란 점은 낮게 보내면 면 하나로 갈라요.",
            "중간에 비선형을 끼는 게 이렇게 차원을 올리거나, 2차원에서 경계를 휘게 해 주는 거예요."),
        bg("기초 다지기 3단원, 9단원", "행렬 곱은 앞 행렬의 행과 뒤 벡터(열)를 곱해 더하는 계산이에요.",
            f"9단원: 왜 비선형이 필요한지, {NEU}과 층 이야기가 있어요."),
    ],
    "pass4": [
        check("W₂(W₁x) = (W₂W₁)x 가 말해 주는 것은?",
            ["f 없이 쌓은 선형층은 행렬 하나와 같다", "행렬 곱은 순서를 바꿔도 된다", "층이 많을수록 늘 좋다"], 0,
            "곱을 묶는 방법(결합)이 자유로워서 층 둘이 행렬 하나로 합쳐져요. 곱하는 순서(W₂W₁ ≠ W₁W₂)를 바꿔도 된다는 뜻은 아니에요."),
        english("외워 쓸 답안 문장",
            f"{ACT} 없이 선형층을 쌓으면 W₂(W₁x) = (W₂W₁)x 처럼 {MAT} 하나로 합쳐져 깊이의 이점이 없으므로 층 사이에 {NONLIN}이 반드시 필요하다.",
            "No f, no deep learning.", "'합쳐진다(collapse)' 한 단어로 기억해요."),
        warn("헷갈리기 쉬운 점",
            "슬라이드 오른쪽 식에는 b 가 있어요. b 가 있어도 f 가 없으면 여전히 변환 하나(affine)로 합쳐져요.",
            f"{UAT}은 '뉴런이 충분히 많으면' 이라는 조건이 붙어요. 아무 신경망이나 다 된다는 뜻이 아니에요."),
    ]})

# p.12 MLP
S.append({"p": 12, "title": "다층 퍼셉트론(MLP)", "terms": ["Multi-Layer Perceptron (MLP)", "Hidden Layer", "Parameter", "Softmax", "Named Entity Recognition (NER)", "Matrix", "Neuron", "Weight", "Bias Term"],
    "pass1": [
        say(f"{NEU}을 여러 개 모아 한 층을 만들고, 그 층을 여러 겹 쌓으면 {MLP}이에요.",
            f"가운데 층은 밖에서 안 보여서 {HID}이라고 불러요."),
        figure(f"{MLP}의 모양", FIG_MLP,
            f"입력 x → {HID} h(1) → {HID} h(2) → 출력 ŷ. 선마다 {WT}가 하나씩 있어요.", 3),
    ],
    "pass2": [
        compare("슬라이드 영어 → 우리말 뜻", ["슬라이드 영어", "우리말 뜻"],
            ["Stack neuron layers", f"{NEU} 층을 쌓아요"],
            ["input x / hidden h / output ŷ", f"입력 / {HID} / 출력"],
            ["word vectors → MLP → P(location), that simple", f"단어 벡터 → {MLP} → 장소일 확률, 그렇게 간단해요"],
            ["How can we determine W & b? Training network!", "W 와 b 는 어떻게 정하나요? 신경망을 학습시켜서요!"]),
        points("이 쪽 용어 하나하나",
            f"{MLP}: {NEU} 층을 여러 겹 쌓은 기본 신경망",
            f"{HID}: 입력과 출력 사이의 숨은 층. 슬라이드에 두 개(h(1), h(2))",
            f"{PAR}: 학습으로 정하는 숫자들. 여기서는 W(1), b(1), W(2), b(2), U"),
        steps(f"{MLP} 순전파 순서", [
            f"h(1) = f(W(1)x + b(1)): 첫 {HID}",
            f"h(2) = f(W(2)h(1) + b(2)): 둘째 {HID}",
            f"ŷ = softmax(U h(2)): 출력 확률",
            f"{NER}이면 x 는 창 벡터, ŷ 에서 LOCATION 확률을 읽어요"],
            "선형 변환 → f → 선형 변환 → f → softmax"),
        check(f"{MLP}에서 {HID}이라는 이름이 붙은 까닭은?",
            ["숫자가 비밀번호라서", "입력과 출력 사이에 있어 밖에서 안 보여서", "학습하지 않아서"], 1,
            "밖에서는 입력과 출력만 보여요. 가운데 계산은 숨어 있어서 hidden 이에요."),
    ],
    "pass3": [
        look("슬라이드 짚어 읽기",
            (0.22, 0.195, 0.52, 0.05, "맨 위 식: 층마다 f(Wx + b) 꼴을 반복하고, 마지막에 softmax(U h(2))."),
            (0.205, 0.36, 0.06, 0.39, "input x: 파란 입력 x₁ ... x₄"),
            (0.385, 0.36, 0.06, 0.39, f"hidden h(1): 첫 {HID}. 위에 W(1), b(1)"),
            (0.558, 0.36, 0.06, 0.39, f"hidden h(2): 둘째 {HID}. 위에 W(2), b(2)"),
            (0.735, 0.37, 0.06, 0.38, "output ŷ: 출력 3개. 위에 U"),
            (0.245, 0.86, 0.51, 0.075, "NER 창 분류기 = 단어 벡터 → MLP → P(location). W, b 는 학습으로!")),
        formula(f"{MLP}의 식", r"h^{(1)} = f(W^{(1)}x + b^{(1)}),\; h^{(2)} = f(W^{(2)}h^{(1)} + b^{(2)}),\; \hat{y} = \mathrm{softmax}(U h^{(2)})", [
            (r"W^{(1)}, b^{(1)}", f"첫 층의 가중치 {MAT}와 {BIAS}"),
            (r"f", f"{ACT}(예: ReLU)"),
            (r"h^{(1)}, h^{(2)}", f"{HID}의 출력 벡터"),
            (r"U", "마지막 점수 행렬(여기서는 b 없음)"),
            (r"\hat{y}", "클래스별 확률")],
            f"뉴런 계산 f(Wx + b) 를 층마다 되풀이하고 끝에 {SMX}를 붙여요."),
        steps("손계산: 그림 속 파라미터 세기", [
            "입력 4 → 은닉 4: W(1) 은 4×4 = 16개, b(1) 4개",
            "은닉 4 → 은닉 4: W(2) 16개, b(2) 4개",
            "은닉 4 → 출력 3: U 는 3×4 = 12개",
            "모두 더하면 16 + 4 + 16 + 4 + 12"],
            "파라미터 52개",
            "슬라이드 그림: 입력 4, 은닉 4, 은닉 4, 출력 3"),
        prof("MLP 는 w 를 곱하고 b 를 더하고 활성화 f 를 통과시키는 뉴런 계산 하나를 계속 반복하면 돼요.",
            "손글씨 0~9 를 분류한다면 마지막 층의 클래스 수는 10개예요.",
            "중요한 건 W 와 b 예요. 이걸 정하는 게 학습(트레이닝) 과정이에요.",
            "W 와 b 는 처음에 랜덤으로 시작해서 3을 넣어도 7이 나올 수 있지만, 학습으로 3이 나오게 맞춰요."),
        points("실습과 이어져요 (N3L p.3)",
            "실습에서는 N3L p.3 에서 이걸 코드로 짜고 x, W, b, z, h, s 의 shape 을 찍어 봐요.",
            "x: (5,) 입력 5개 / W: (3, 5) 은닉 뉴런 3개, 입력 5개 / b: (3,)",
            "z = W @ x + b: (3,) / h = tanh(z): (3,) / s = u @ h: 숫자 하나(스칼라)",
            f"W 의 shape 은 (출력 뉴런 수, 입력 수)예요. 이 규칙이 p.15 문제 2의 열쇠예요."),
        bg("기초 다지기 3단원", "(3,5) 행렬 @ 길이 5 벡터 → 길이 3 벡터. 앞 행렬의 열 수와 벡터 길이가 같아야 곱할 수 있어요.",
            "기초 다지기 10단원에 PyTorch 의 @, shape 읽는 법이 있어요."),
    ],
    "pass4": [
        check("W(1) 의 shape 이 (3, 5) 일 때, 입력 x 와 첫 은닉층 h(1) 의 길이는?",
            ["x 3, h(1) 5", "x 5, h(1) 3", "x 15, h(1) 1"], 1,
            "W(1)x 에서 W 의 열 수 5 = 입력 길이, 행 수 3 = 은닉 뉴런 수예요."),
        english("외워 쓸 답안 문장",
            f"{MLP}은 h = f(Wx + b) 를 층마다 반복하고 마지막에 {SMX}로 클래스 확률을 내며, W 와 b 는 학습으로 정해지는 {PAR}다.",
            "층 = f(Wx + b), 끝 = softmax, W 와 b 는 학습.", None),
        warn("헷갈리기 쉬운 점",
            f"{MLP}의 줄임말을 {NLP}와 헷갈리지 않아요. 녹음 받아쓰기에도 'NLP' 로 잘못 적혀 있어요.",
            "슬라이드 식에서 마지막 U 에는 b 가 없어요. 그림 위에도 'U' 만 적혀 있어요."),
    ]})

# p.13 CNN (1)
S.append({"p": 13, "title": "글을 위한 CNN (1): 아이디어", "terms": ["Convolutional Neural Network (CNN)", "Convolution Filter", "Feature Map", "Max-pooling", "n-gram", "Word Vector", "Window"],
    "pass1": [
        say(f"또 하나의 신경망, {CNN}이에요.",
            f"작은 {FIL}가 문장 위를 한 칸씩 미끄러지며 짧은 패턴을 찾아요.",
            "폭 3짜리 필터라면 연속된 세 단어를 한 번에 봐요."),
        figure("필터가 미끄러지며 값을 내요", FIG_CONV,
            f"창마다 값 하나 → {FMAP} → 가장 큰 값만 남기기({POOL}).", 3),
    ],
    "pass2": [
        compare("슬라이드 영어 → 우리말 뜻", ["슬라이드 영어", "우리말 뜻"],
            ["A convolution filter = a small pattern detector", f"{FIL} = 작은 패턴 탐지기"],
            ["slides along the sentence", "문장을 따라 미끄러져요"],
            ["feature map (one value per window)", f"{FMAP}: 창마다 값 하나"],
            ["strongest n-gram signal in the sentence", f"문장 안에서 가장 센 {NG} 신호"],
            ["A filter of width 3 is a learned trigram detector", "폭 3 필터 = 학습된 세 단어(trigram) 탐지기"]),
        points("이 쪽 용어 하나하나",
            f"{CNN}: {FIL}를 미끄러뜨려 부분 패턴을 찾는 신경망",
            f"{FIL}: 폭(단어 수) × 단어 벡터 차원 크기의 숫자 판. 창과 곱해 값 하나를 내요.",
            f"{FMAP}: 창마다 나온 값을 줄 세운 것",
            f"{NG}: 붙어 있는 n 단어. 폭 3이면 trigram, 폭 2면 bigram"),
        steps("필터가 도는 순서", [
            "this movie was → 값 하나",
            "한 칸 내려 movie was really → 값 하나",
            "was really great → 값 하나 (가장 큼)",
            f"이렇게 모은 값들이 {FMAP}",
            f"{POOL}: 가장 큰 값 하나만 남겨요"],
            "창마다 값 → 특징 맵 → 최댓값"),
        check(f"폭 3짜리 {FIL}가 찾는 것은?",
            ["문장 전체의 길이", "연속된 세 단어의 패턴(trigram)", "단어 하나의 철자"], 1,
            f"폭 3이면 붙어 있는 세 단어를 한 번에 봐요. 그래서 학습된 trigram({NG}) 탐지기예요."),
    ],
    "pass3": [
        look("슬라이드 짚어 읽기",
            (0.08, 0.2, 0.53, 0.04, "'A convolution filter = a small pattern detector that slides along the sentence'."),
            (0.1, 0.33, 0.08, 0.4, f"왼쪽: this ... fun 여섯 단어. 줄마다 {WV}(그림은 d = 4)."),
            (0.18, 0.45, 0.29, 0.17, "빨간 점선: 폭 3 필터가 movie, was, really 세 줄을 덮고 있어요."),
            (0.588, 0.4, 0.07, 0.32, f"feature map: 창마다 값 하나. 진한 칸이 가장 센 반응."),
            (0.762, 0.5, 0.105, 0.215, "max-pool: 가장 센 n-gram 신호 하나만 남겨요."),
            (0.695, 0.18, 0.285, 0.24, "Yoon Kim(2014) 'Convolutional Neural Networks for Sentence Classification'. 인용 22357회.")),
        steps("손계산: 필터 한 개 돌려 보기", [
            "단어마다 숫자 하나로 줄여요: this 0, movie 1, was 0, really 2, great 3, fun -1",
            "필터 [1, 1, 1] (세 값을 더하기)",
            "this movie was: 0+1+0 = 1 / movie was really: 1+0+2 = 3",
            "was really great: 0+2+3 = 5 / really great fun: 2+3-1 = 4",
            "특징 맵 [1, 3, 5, 4], 최대 풀링 → 5"],
            "가장 센 곳은 'was really great' (값 5)",
            "실제로는 단어마다 벡터이고 필터도 3 × d 숫자 판이에요. 계산 모양만 본 장난감이에요."),
        prof("컨볼루션은 정해진 필터 모양 하나가 움직이면서 값들을 얻어내는 거예요.",
            "윈도우 3짜리면 세 단어에 곱해서 값 하나, 한 칸 내려서 또 하나, 이렇게 진행돼요.",
            "같은 필터를 문장 전체에 반복해서 재활용한다는 게 특징이에요.",
            "텍스트 CNN 은 한국인 Yoon Kim 의 논문이고, 교수님이 존경하는 대작이라고 소개했어요."),
    ],
    "pass4": [
        check(f"{CNN}에서 같은 {FIL}를 문장의 모든 위치에 쓰는 것에 대한 설명으로 맞는 것은?",
            ["위치마다 다른 필터를 새로 만든다", "한 필터를 모든 창에 다시 써서 같은 패턴을 어디서든 찾는다", "필터는 한 위치에서만 쓴다"], 1,
            "같은 필터를 재활용해요. 그래서 같은 패턴이 문장 어디에 있든 똑같이 반응해요."),
        english("외워 쓸 답안 문장",
            f"글에 쓰는 {CNN}은 폭 k 의 {FIL}를 문장 위로 미끄러뜨려 창마다 값을 내 {FMAP}을 만들며, 폭 3 필터는 학습된 trigram 탐지기다.",
            "필터 → 특징 맵 → 최대 풀링.", None),
    ]})

# p.14 CNN (2)
S.append({"p": 14, "title": "글을 위한 CNN (2): 왜, 어디에", "terms": ["Max-pooling", "Feature Map", "Convolution Filter", "n-gram", "Classification", "Convolutional Neural Network (CNN)", "Recurrent Neural Network (RNN)"],
    "pass1": [
        say(f"{POOL}은 '이 패턴이 문장 어디에서든 나왔나?' 만 물어요.",
            f"그래서 {CNN}은 빠르고 {CLS}에 강하지만, 멀리 떨어진 단어 사이 관계는 못 봐요.",
            f"그 약점을 채울 게 Part 4 의 {RNN}이에요."),
        figure("어디서 나왔든 결과는 같아요", FIG_POOL,
            f"패턴이 앞에 있든 뒤에 있든 {POOL} 결과는 5로 같아요.", 2),
    ],
    "pass2": [
        compare("슬라이드 영어 → 우리말 뜻", ["슬라이드 영어", "우리말 뜻"],
            ["did this pattern appear ANYWHERE?", "이 패턴이 어디에서든 나왔나?"],
            ["a bank of learned n-gram detectors", f"학습된 {NG} 탐지기 묶음"],
            ["fast, position-independent, great for classification", f"빠르고, 위치에 상관없고, {CLS}에 좋아요"],
            ["local view only, no long-range order", "가까운 곳만 봐요, 먼 순서는 못 봐요"],
            ["CNN = parallel n-gram detectors, RNN = a reader with memory", f"{CNN} = 병렬 n-gram 탐지기, {RNN} = 기억을 가진 독자"]),
        compare(f"{CNN}의 장점과 한계", ["", "내용"],
            ["장점", "모든 창을 동시에 계산해서 빨라요(병렬)"],
            ["장점", f"위치와 상관없이 패턴을 잡아요({POOL} 덕분)"],
            ["장점", f"감정, 주제 같은 {CLS}에 좋아요"],
            ["한계", "창 안(가까운 곳)만 봐서 먼 단어 사이 순서와 관계를 못 봐요"]),
        check(f"{CNN}의 한계로 슬라이드가 든 것은?",
            ["계산이 너무 느리다", "가까운 곳만 봐서 먼 거리 순서를 못 잡는다", f"{CLS}에 쓸 수 없다"], 1,
            f"'local view only, no long-range order'. 그래서 순서가 중요한 일에는 {RNN}(recurrence)을 쓰려고 해요."),
    ],
    "pass3": [
        look("슬라이드 짚어 읽기",
            (0.06, 0.505, 0.65, 0.045, f"'Max-pooling: keep the strongest response': 가장 센 반응만 남겨요."),
            (0.06, 0.56, 0.63, 0.045, f"'filters of widths 2-5': 폭 2~5 필터 여러 개 = {NG} 탐지기 묶음 → 그 위에 분류기."),
            (0.06, 0.615, 0.66, 0.045, "'Strengths': 빠름(모든 창 병렬), 위치 무관, 분류에 강함."),
            (0.06, 0.67, 0.7, 0.045, f"'Limits': 가까운 곳만, 먼 순서 못 봄. 순서에는 recurrence({RNN}, Part 4)."),
            (0.06, 0.725, 0.79, 0.045, "'used in production for years': 감정, 주제 분류에 몇 년간 실제로 쓰였어요."),
            (0.255, 0.855, 0.5, 0.045, "'CNN = parallel n-gram detectors, RNN = a reader with memory'.")),
        prof("필터는 숫자들의 모음이라 여러 개가 있을 수 있고, 필터마다 값이 하나씩 나와요.",
            "이미지로 치면 엣지만 남기는 필터처럼, 필터마다 맡은 역할이 달라요.",
            "폭이 3이면 트리그램, 2면 바이그램. 이 필터 뱅크로 여러 피처를 얻어 판단해요.",
            "단점은 윈도우만 봐서 로컬 컨텍스트만 본다는 것. 멀리 떨어진 두 단어의 관계는 거의 못 잡아요."),
        prof("문장을 왼쪽부터 읽으며 지금까지 본 정보를 계속 기억할 수 있느냐가 중요한 이슈예요.",
            "그 아이디어가 리커런스(recurrence), 반복된다, 재귀적이라는 뜻이에요. 뒤에서 RNN 으로 배워요."),
        steps("필터 뱅크로 분류하기", [
            "폭 2, 3, 4, 5 필터를 여러 개 준비해요",
            f"필터마다 문장을 훑어 {FMAP}을 만들어요",
            f"필터마다 {POOL}으로 숫자 하나씩 남겨요",
            "그 숫자들을 모아 벡터 하나로 만들고, 그 위의 분류기가 감정이나 주제를 골라요"],
            f"필터 개수만큼 숫자가 모여 분류기의 입력이 돼요."),
    ],
    "pass4": [
        check(f"{POOL} 때문에 {CNN}이 구절의 위치에 둔감해지는 까닭은?",
            ["위치 정보를 따로 더해서", "가장 큰 값 하나만 남기고 그 값이 어디서 나왔는지는 버려서", "필터 폭이 넓어서"], 1,
            "최댓값만 남으니 문장 앞에서 나왔든 뒤에서 나왔든 결과가 같아요."),
        english("외워 쓸 답안 문장",
            f"{CNN}은 {FIL}로 {NG} 패턴을 병렬로 찾아 {CLS}에 강하지만 먼 거리 순서는 못 잡는다.",
            "장점 셋(빠름, 위치 무관, 분류) + 한계 하나(로컬만).", None),
        warn("헷갈리기 쉬운 점",
            f"'위치에 둔감' 은 장점이자 단점이에요. 어디서 나왔는지 필요할 때는 정보가 사라져요.",
            f"{CNN} = 병렬 n-gram 탐지기, {RNN} = 기억을 가진 독자. 두 줄을 짝으로 외워요."),
    ]})

# p.15 Check Yourself
S.append({"p": 15, "title": "Check Yourself: Part 1 확인 문제", "terms": ["Activation Function", "Matrix", "Hidden Layer", "Convolution Filter", "Max-pooling", "n-gram", "Parameter"],
    "pass1": [
        say("Part 1 을 스스로 확인하는 교수님의 문제 네 개예요.",
            "60초 생각하고 옆 사람과 이야기해 보라는 쪽이에요.",
            "슬라이드 아래: 'Q1, Q2 가 바로 풀리면 Part 2 로 갈 준비가 된 거예요.'"),
    ],
    "pass2": [
        compare("네 문제 우리말 뜻", ["문제", "우리말 뜻"],
            ["Q1", f"{ACT} 없이 선형층 10개를 쌓으면 표현력이 어떤가?"],
            ["Q2", f"{HID} 300개, 입력 창이 5단어 × 100차원이면 W(1) 의 shape 은?"],
            ["Q3", f"폭 3 {FIL}가 강하게 반응했다. 어떤 패턴을 잡은 걸까?"],
            ["Q4", f"{POOL}이 왜 구절의 위치(WHERE)에 둔감하게 만드나?"]),
        points("어느 쪽을 다시 보면 되나",
            "Q1 → p.11 (층이 합쳐짐)",
            "Q2 → p.6 (창 벡터 5d), p.12 (W 의 shape)",
            "Q3 → p.13 (trigram 탐지기)",
            "Q4 → p.14 (최대 풀링)"),
    ],
    "pass3": [
        look("슬라이드 짚어 읽기",
            (0.075, 0.2, 0.64, 0.045, "Q1: 'stack 10 linear layers with no activation', 'How expressive?'"),
            (0.075, 0.265, 0.8, 0.045, "Q2: '300 units', '5 words × 100 dims', 'shape of W(1)?'"),
            (0.075, 0.33, 0.58, 0.045, "Q3: 'A width-3 CNN filter fires strongly': 세게 반응했다."),
            (0.075, 0.395, 0.6, 0.045, "Q4: 'insensitive to WHERE a phrase occurs': 위치에 둔감."),
            (0.34, 0.855, 0.32, 0.045, "'If Q1 and Q2 feel instant, you are ready for part 2'.")),
        prof("1번: 선형층을 쌓아도 활성화가 없으면 하나의 선형 변환으로 합쳐져요. 깊어졌지만 표현력은 선형 모델이에요.",
            "2번: 5단어 × 100차원이면 입력 x 는 500개 숫자, 히든 300개와 모두 이으려면 500 곱하기 300 만큼 필요해요.",
            "3번: 연속된 세 단어의 특정 패턴, 학습된 트리그램 패턴을 감지한 거예요.",
            "4번: 맥스 풀링은 가장 큰 값 하나만 남기고 나머지 정보는 다 버려요."),
        steps("Q2 shape 차근차근", [
            "입력 x: 5단어 × 100차원 = 500 → x 의 shape (500,)",
            "은닉 h(1): 300개 → (300,)",
            "h(1) = f(W(1)x + b(1)) 이므로 W(1) 은 (300, 500): 행 = 출력 수, 열 = 입력 수",
            "가중치 개수 300 × 500 = 150,000, 편향 항 b(1) 은 (300,) 300개"],
            "W(1) 의 shape (300, 500)",
            "실습 N3L p.3 의 W (3, 5) 도 같은 규칙(은닉 3, 입력 5)이에요."),
        bg("기초 다지기 3단원", "(300, 500) 행렬 @ (500,) 벡터 → (300,) 벡터. 가운데 500 끼리 맞아야 곱할 수 있어요.",
            "'shape 을 맞춘다' 는 생각은 Part 2 역전파에서도 계속 써요."),
    ],
    "pass4": [
        exam("N3 Check Yourself 1",
            "Q1. I stack 10 linear layers with no activation in between. How expressive is the result?",
            f"{ACT} 없이 선형층 10개를 쌓으면 얼마나 표현력이 있나?",
            ["선형층 하나는 행렬 곱 W 하나예요",
             "W₁₀(...(W₂(W₁x))) = (W₁₀...W₂W₁)x 로 묶을 수 있어요",
             f"결국 {MAT} 하나(선형 변환 하나)와 같아요",
             "그래서 곧은 경계만 그릴 수 있어요"],
            "선형층 하나와 같은 표현력(여전히 선형 모델). 깊이가 아무 이득이 없다."),
        exam("N3 Check Yourself 1",
            "Q2. My hidden layer has 300 units and the input window is 5 words × 100 dims. What is the shape of W(1)?",
            f"{HID} 300개, 입력 창 5단어 × 100차원일 때 W(1) 의 shape 은?",
            ["입력 x 길이 = 5 × 100 = 500",
             "h(1) 길이 = 300",
             "h(1) = f(W(1)x + b(1)) 에서 W(1)x 가 길이 300이 되려면 W(1) 은 300행 500열",
             "가중치 수는 300 × 500 = 150,000개 (교수님은 '500 곱하기 300' 이라고 개수로 설명)"],
            "W(1) ∈ ℝ^(300×500), 즉 shape (300, 500)"),
        exam("N3 Check Yourself 1",
            "Q3. A width-3 CNN filter fires strongly. What kind of pattern did it just detect?",
            f"폭 3 {FIL}가 강하게 반응했다. 무엇을 찾은 걸까?",
            ["폭 3 = 연속된 세 단어를 한 번에 봐요",
             "필터 값과 세 단어 벡터가 잘 맞으면 큰 값이 나와요",
             f"그러니 필터가 배운 세 단어 {NG}(trigram) 패턴이 거기 있다는 뜻이에요"],
            "학습된 trigram 패턴(연속된 세 단어의 특정 패턴, 예: 'was really great')"),
        exam("N3 Check Yourself 1",
            "Q4. Why does max-pooling make the CNN insensitive to WHERE a phrase occurs?",
            f"{POOL}이 왜 구절이 나온 위치에 둔감하게 만드나?",
            ["필터가 모든 위치에서 같은 값으로 계산해 특징 맵을 만들어요",
             f"{POOL}은 그중 가장 큰 값 하나만 남겨요",
             "그 값이 몇 번째 창에서 나왔는지는 버려요",
             "그래서 구절이 앞에 있든 뒤에 있든 결과가 같아요"],
            "최댓값 하나만 남기고 위치 정보를 버리기 때문('어디서든 나왔나?' 만 묻는다)"),
        warn("헷갈리기 쉬운 점",
            "Q2 에서 교수님은 '500 곱하기 300' 이라고 연결선 개수로 말했어요. shape 을 쓸 때는 식 W(1)x 에 맞춰 (300, 500) 으로 써요.",
            "편향 항 b(1) 의 shape 은 (300,) 이에요. W(1) 과 헷갈리지 않아요."),
    ]})

# p.16 Part 2 구분
S.append({"p": 16, "title": "Part 2: Backpropagation", "terms": ["Backpropagation", "Gradient"],
    "pass1": [say(
        f"Part 2 시작이에요. 제목은 {BP}이에요.",
        f"부제 'how the gradients actually get computed' 는 '{GRAD}를 실제로 어떻게 계산하나' 예요.",
        "Part 1 에서 남은 질문, 'W 와 b 는 어떻게 정하나?' 의 답이 여기서 나와요.")],
    "pass2": [], "pass3": [], "pass4": []})

data = {"deck": "N3", "from": 1, "to": 16,
        "glossary": [{"ko": k, "en": e, "say": s, "more": m} for k, e, s, m in GLOSSARY],
        "slides": S}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
print("saved", OUT, len(S), "pages")
