# 3강(N3) 회독 레슨 34~43쪽 생성기. 사용: python build_N3_034-043.py
# 범위: 3부 언어 모델링(과제, 일상 속 LM, n-gram, 예제, 세기의 한계, 생성, 퍼플렉서티, 예제), 4부 구분 쪽
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "N3_034-043.json")
W, H = 1400, 788  # 슬라이드 PNG 크기

MANTRA = "글을 토큰으로 자르고, 토큰을 벡터로 바꾸고, 벡터로 다음 토큰을 맞혀요."

# ---------------- 손계산 확인 (Python assert) ----------------
# p.35 다음 단어 확률 분포: 슬라이드의 세 후보와 나머지
dist = {"9pm": 0.2, "noon": 0.1, "midnight": 0.05}
rest = 1 - sum(dist.values())
assert round(rest, 2) == 0.65
# 확률의 연쇄 법칙 (예시 숫자): 0.1 x 0.5 x 0.2
assert round(0.1 * 0.5 * 0.2, 4) == 0.01

# p.37 n-gram: x^(t) ... x^(t-n+2) 는 n-1 개 단어
for n in (2, 3, 4, 5):
    t = 10
    assert len(range(t - n + 2, t + 1)) == n - 1

# p.38 슬라이드 예제: count(students opened their)=1000, books 400, exams 100
c_ctx, c_books, c_exams = 1000, 400, 100
assert c_books / c_ctx == 0.40 and c_exams / c_ctx == 0.10
# 예시: 300 번이면 0.30
assert 300 / c_ctx == 0.30
# 0 번 나온 이어짐(예시) → 확률 0, 곱하면 문장 전체가 0
p_zero = 0 / c_ctx
assert p_zero == 0 and 0.4 * 0.5 * p_zero == 0
# 분모가 0 이면 나눌 수 없음
try:
    _ = 0 / 0
    raise AssertionError
except ZeroDivisionError:
    pass

# p.39 가능한 조합 수: 어휘 1만 개일 때
V10k = 10_000
assert V10k ** 2 == 10 ** 8 and V10k ** 3 == 10 ** 12

# p.40 트라이그램 생성 경로의 확률 (슬라이드 숫자)
path = [0.31, 0.62, 0.57, 0.34, 0.41]
pp = 1.0
for v in path:
    pp *= v
assert round(pp, 4) == 0.0153
# 각 상자에서 뽑힌 단어는 모두 1등 후보
boxes40 = [[0.31, 0.15, 0.12, 0.08], [0.62, 0.21, 0.04, 0.03], [0.57, 0.09, 0.06, 0.04], [0.34, 0.28, 0.18, 0.07], [0.41, 0.19, 0.12, 0.07]]
assert all(b[0] == max(b) for b in boxes40)

# p.41 균등 분포: 1만 개 → PPL 1만
J_uni = -math.log(1 / V10k)
assert round(math.exp(J_uni)) == 10_000
# 실습 N3L p.12: loss 3.254 → ppl 25.9, loss 4.183 → 65.6
assert round(math.exp(3.254), 1) == 25.9 and round(math.exp(4.183), 1) == 65.6

# p.42 슬라이드 예제: 1/2, 1/4, 1/8, 1/16
probs42 = [1 / 2, 1 / 4, 1 / 8, 1 / 16]
prod_inv = 1
for p_ in probs42:
    prod_inv *= 1 / p_
assert prod_inv == 1024
ppl42 = prod_inv ** (1 / 4)
assert abs(ppl42 - 2 ** 2.5) < 1e-9 and round(ppl42, 2) == 5.66 and round(ppl42, 1) == 5.7
J42 = sum(-math.log(p_) for p_ in probs42) / 4
assert abs(J42 - 2.5 * math.log(2)) < 1e-12 and round(J42, 3) == 1.733
assert abs(math.exp(J42) - ppl42) < 1e-9
# 완벽한 모델: 모두 확률 1 → PPL 1
assert math.exp(sum(-math.log(1.0) for _ in range(4)) / 4) == 1.0
# 연습: 1/2, 1/2 → PPL 2
assert round((2 * 2) ** (1 / 2), 6) == 2.0
# 연습: 1/4 네 번 → PPL 4
assert round((4 ** 4) ** (1 / 4), 6) == 4.0

# ---------------- 용어 ----------------
TERMS = {
    "lm": ("언어 모델", "Language Model (LM)", "**언어 모델(LM)**"),
    "ntp": ("다음 토큰 예측", "Next Token Prediction", None),
    "dist": ("확률 분포", "Probability Distribution", None),
    "cprob": ("조건부 확률", "Conditional Probability", None),
    "pchain": ("확률의 연쇄 법칙", "Chain Rule of Probability", None),
    "llm": ("대규모 언어 모델", "Large Language Model (LLM)", "**대규모 언어 모델(LLM)**"),
    "ngram": ("엔그램", "n-gram", "**n-gram(엔그램)**"),
    "markov": ("마르코프 가정", "Markov Assumption", None),
    "corpus": ("말뭉치", "Corpus", None),
    "vocab": ("어휘", "Vocabulary", None),
    "token": ("토큰", "Token", None),
    "tokzr": ("토크나이저", "Tokenizer", None),
    "sparse": ("희소성 문제", "Sparsity Problem", None),
    "smooth": ("스무딩", "Smoothing", None),
    "backoff": ("백오프", "Back-off", None),
    "onehot": ("원-핫 벡터", "One-hot Vector", None),
    "emb": ("임베딩", "Embedding", None),
    "sample": ("샘플링", "Sampling", None),
    "temp": ("샘플링 온도", "Temperature", None),
    "ppl": ("퍼플렉서티", "Perplexity (PPL)", "**퍼플렉서티(PPL)**"),
    "ce": ("교차 엔트로피", "Cross-Entropy", None),
    "loss": ("손실 함수", "Loss Function", None),
    "soft": ("소프트맥스", "Softmax", None),
    "geo": ("기하 평균", "Geometric Mean", None),
    "fwlm": ("고정 윈도우 신경망 언어 모델", "Fixed-window Neural LM", None),
    "rnn": ("순환 신경망", "Recurrent Neural Network (RNN)", "**RNN(순환 신경망)**"),
    "hidden": ("은닉 상태", "Hidden State", None),
}


def T(k):
    ko, en, disp = TERMS[k]
    if disp:
        return disp
    return f"**{ko}({en})**"


def EN(k):
    return TERMS[k][1]


GLOSS = {
    "lm": ("휴대폰 자판의 다음 단어 추천처럼, 앞 글을 보고 다음 단어의 확률을 내는 모델",
           "지금까지의 단어 x(1)~x(t)가 주어졌을 때 다음 단어 x(t+1)의 확률 분포를 내요. 같은 말로, 어떤 글이든 그 글 전체의 확률을 매길 수 있어요."),
    "ntp": ("지금까지 나온 토큰을 보고 바로 다음 토큰을 맞히는 일",
            "교수님이 'GPT 도 다 결국 이거다'라고 한 핵심 과제예요. 맞히고, 붙이고, 또 맞히기를 반복하면 글이 써져요."),
    "dist": ("가능한 후보마다 확률을 붙여 둔 목록. 모두 더하면 1",
             "언어 모델이 내는 다음 단어 확률 분포는 후보가 어휘 크기만큼 있어요. 예 {9pm: 0.2, noon: 0.1, midnight: 0.05, ...}."),
    "cprob": ("무엇이 이미 주어졌을 때 다른 일이 일어날 확률",
              "P(A | B) 는 'B 가 주어졌을 때 A 의 확률'이라고 읽어요. 언어 모델은 앞 단어들이 주어졌을 때 다음 단어의 조건부 확률을 내요."),
    "pchain": ("글 전체의 확률을 '한 단어씩 다음 단어 확률'의 곱으로 쪼개는 규칙",
               "P(x1, ..., xT) = P(x1) x P(x2|x1) x P(x3|x1,x2) x ... 이에요. 미분의 연쇄 법칙(Chain Rule)과는 다른 규칙이에요."),
    "llm": ("아주 큰 언어 모델. ChatGPT 같은 것",
            "Large Language Model 의 줄임말이에요. 가운데 두 글자 LM 이 바로 오늘 배우는 언어 모델이에요. 여전히 다음 토큰 예측으로 학습해요."),
    "ngram": ("바로 붙어 있는 단어 n개 묶음. 바로 앞 몇 단어만 보고 다음 단어 맞히기",
              "딥러닝 이전의 언어 모델이에요. 앞의 n-1 개 단어만 남기고, 큰 말뭉치에서 횟수를 세어 확률을 구해요. 4-gram 이면 앞 3단어를 봐요."),
    "markov": ("다음 단어는 바로 앞 n-1 개 단어에만 달려 있다고 치는 가정",
               "그보다 앞의 단어는 아무리 중요해도 버려요. n-gram 언어 모델이 세기만으로 확률을 구할 수 있게 해 주지만, 먼 문맥을 잃어요."),
    "corpus": ("학습에 쓰는 글을 잔뜩 모아 둔 것",
               "n-gram 은 말뭉치에서 단어 묶음이 몇 번 나왔는지 세어 확률을 구해요. 말뭉치에 없는 묶음은 0번이에요."),
    "vocab": ("레고 상자에 든 조각 종류 목록, 곧 모델이 아는 토큰 목록",
              "다음 단어 후보의 수가 곧 어휘 크기예요. 모든 후보에 똑같이 확률을 주면 퍼플렉서티가 어휘 크기와 같아져요."),
    "token": ("글을 자른 레고 조각 하나",
              "언어 모델은 토큰 하나씩 다음 것을 맞혀요. 토큰을 글자로 자르냐 서브워드로 자르냐에 따라 퍼플렉서티 숫자가 달라져요."),
    "tokzr": ("글을 토큰으로 잘라 주는 도구",
              "퍼플렉서티는 같은 토크나이저를 쓴 모델끼리만 비교할 수 있어요. 실습 N3L p.18~26 에서 직접 확인해요."),
    "sparse": ("세어 보려는 단어 묶음이 말뭉치에 거의 안 나와서 횟수가 0 투성이인 문제",
               "분자가 0이면 확률이 0이 되고, 분모가 0이면 아예 나눌 수가 없어요. n 이 커질수록 심해져서 실제로는 n ≤ 5 를 써요."),
    "smooth": ("한 번도 못 본 묶음에도 아주 작은 확률을 나눠 주는 보정",
               "분자가 0이라서 확률이 0이 되는 문제를 고치는 방법이에요(슬라이드: fix: smoothing)."),
    "backoff": ("긴 문맥으로 못 세면 더 짧은 문맥으로 물러나 세는 방법",
                "분모(앞 문맥)가 말뭉치에 한 번도 없을 때 쓰는 고치기예요. 예 4-gram 이 안 되면 3-gram 으로요."),
    "onehot": ("단어마다 자기 자리만 1이고 나머지는 모두 0인 벡터",
               "두 단어 벡터의 내적이 늘 0이라 비슷함을 전혀 나타내지 못해요. n-gram 의 '유사도 없음'도 같은 병이에요."),
    "emb": ("단어의 지도 좌표. 뜻이 비슷하면 가까이 살아요",
            "단어를 짧고 촘촘한 숫자 벡터로 바꾼 것이에요. 신경망 언어 모델은 임베딩 덕분에 'their'와 'her'처럼 비슷한 단어가 정보를 나눠 가져요."),
    "sample": ("확률 분포에 따라 제비뽑기처럼 후보 하나를 뽑는 것",
               "확률이 큰 후보가 더 자주 뽑히지만 늘 1등만 뽑히지는 않아요. 뽑고, 붙이고, 반복하면 언어 모델이 글을 써요."),
    "temp": ("샘플링을 얼마나 과감하게 할지 정하는 손잡이",
             "점수를 온도로 나눈 뒤 소프트맥스를 해요. 낮으면(0.5) 무난한 1등 위주, 높으면(1.5) 엉뚱한 후보도 자주 뽑혀요."),
    "ppl": ("다음 단어를 고를 때 헷갈리는 후보가 평균 몇 개인지",
            "PPL = exp(교차 엔트로피 손실)이에요. 낮을수록 좋고, 최저는 1, 모든 단어에 똑같은 확률이면 어휘 크기 V 가 돼요."),
    "ce": ("정답 단어에 준 확률의 -log 를 벌점으로 쓰는 손실",
           "정답 확률이 1에 가까우면 벌점이 0에 가깝고, 작을수록 벌점이 커요. 소프트맥스에 음의 로그 우도(NLL)를 붙인 것이에요."),
    "loss": ("틀린 정도를 매기는 벌점",
             "언어 모델은 매 위치에서 정답 다음 단어에 대한 교차 엔트로피 벌점을 받고, 그 평균 J 를 줄이도록 배워요."),
    "soft": ("점수를 모두 더해 1이 되는 확률 파이로 나누는 함수",
             "신경망 언어 모델은 마지막에 어휘 크기만큼의 점수를 소프트맥스로 확률 분포로 바꿔요."),
    "geo": ("곱해서 개수만큼 제곱근을 씌운 평균",
            "숫자 T 개를 모두 곱한 뒤 1/T 제곱을 해요. 퍼플렉서티는 '정답 확률의 역수'의 기하 평균이에요."),
    "fwlm": ("앞의 정해진 몇 단어만 임베딩으로 바꿔 신경망에 넣고 다음 단어를 맞히는 모델",
             "n-gram 과 달리 임베딩 덕분에 비슷한 단어끼리 정보를 나눠요. 하지만 창(윈도우) 크기가 여전히 고정이에요. 4부 첫 쪽(p.44)에서 봐요."),
    "rnn": ("한 단어씩 읽으며 메모장(은닉 상태)에 요약을 고쳐 쓰는 신경망",
            "매 시점에 같은 가중치를 되풀이해서 써요. 그래서 문장이 길어져도 파라미터 수가 늘지 않아요. 4부의 주인공이에요."),
    "hidden": ("RNN 이 지금까지 읽은 내용을 적어 두는 메모장",
               "h(t) 로 써요. 새 단어를 읽을 때마다 이전 메모 h(t-1)와 새 단어를 섞어 고쳐 써요."),
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


MON2 = "3주차 월요일 2교시"
MON3 = "3주차 월요일 3교시"

S = []

# ---------------- 그림 ----------------
FIG_LM = SVG(
    BOX(20, 20, 440, 40, "the lecture will end at ____", "box2", "tb", 0, 16),
    A(240, 62, 240, 88, "e2", 1),
    TX(40, 115, "9pm", "t", 15, "start", 1), R(140, 101, 120, 18, "n2", 1), TX(270, 115, "0.2", "tb", 14, "start", 1),
    TX(40, 150, "noon", "t", 15, "start", 1), R(140, 136, 60, 18, "n3", 1), TX(210, 150, "0.1", "tb", 14, "start", 1),
    TX(40, 185, "midnight", "t", 15, "start", 1), R(140, 171, 30, 18, "n3", 1), TX(180, 185, "0.05", "tb", 14, "start", 1),
    TX(40, 220, "나머지 전부", "tm", 14, "start", 2), R(140, 206, 300, 18, "n", 2), TX(290, 220, "0.65", "tl", 14, "middle", 2),
    TX(240, 258, "모든 후보(어휘 크기만큼)의 확률을 더하면 1", "tb", 15, "middle", 2),
)

WORDS38 = ["proctor", "clock", "students", "opened", "their", "?"]
_f38 = []
for i, w_ in enumerate(WORDS38):
    x = 10 + i * 78
    if i < 2:
        _f38.append(BOX(x, 70, 70, 40, w_, "n", "tm", 0, 14))
    elif i < 5:
        _f38.append(BOX(x, 70, 70, 40, w_, "n2", "tl", 1, 14))
    else:
        _f38.append(BOX(x, 70, 70, 40, w_, "box2", "tb", 1, 16))
FIG_NG = SVG(
    TX(240, 30, "4-gram: 앞 3단어만 보고 다음 단어 맞히기", "tb", 15),
    *_f38,
    TX(85, 140, "버림 (Markov 가정)", "tm", 14, "middle", 2),
    L(10, 150, 158, 150, "e", 2),
    TX(283, 140, "이 3단어만 봐요", "tb", 14, "middle", 1),
    TX(240, 190, "count(students opened their books) = 400", "t", 14, "middle", 2),
    TX(240, 215, "÷ count(students opened their) = 1000", "t", 14, "middle", 2),
    TX(240, 250, "P(books | ...) = 0.40", "tb", 16, "middle", 2),
)

FIG_WALLS = SVG(
    TX(240, 26, "세기(counting)가 부딪히는 벽", "tb", 16),
    BOX(15, 60, 140, 110, "", "n4", "tl", 1, 14), TX(85, 105, "희소성", "tl", 16, "middle", 1), TX(85, 135, "0번 → 확률 0", "tl", 13, "middle", 1),
    BOX(170, 60, 140, 110, "", "n4", "tl", 2, 14), TX(240, 105, "저장 공간", "tl", 16, "middle", 2), TX(240, 135, "묶음마다 횟수", "tl", 13, "middle", 2),
    BOX(325, 60, 140, 110, "", "n4", "tl", 3, 14), TX(395, 105, "유사도 없음", "tl", 16, "middle", 3), TX(395, 135, "their ≠ her", "tl", 13, "middle", 3),
    TX(240, 210, "+ 앞 n-1 단어 밖은 안 보임", "tm", 15, "middle", 3),
    TX(240, 245, "신경망 언어 모델이 벽을 허물어요", "tb", 15, "middle", 3),
)

FIG_GEN = SVG(
    BOX(160, 20, 160, 44, "확률 분포 만들기", "box2", "tb", 0, 15),
    BOX(320, 150, 140, 44, "하나 뽑기", "n3", "tl", 1, 15),
    BOX(20, 150, 140, 44, "뒤에 붙이기", "n3", "tl", 2, 15),
    A(300, 66, 380, 146, "e2", 1), A(318, 172, 164, 172, "e2", 2), A(100, 146, 180, 66, "e2", 3),
    TX(240, 120, "되풀이", "tb", 16, "middle", 3),
    TX(240, 235, "today the → price → of → gold → is → shiny", "t", 14, "middle", 3),
    TX(240, 260, "ChatGPT 도 같은 고리, 모델 실력만 달라요", "tm", 14, "middle", 3),
)

_c1 = [BOX(30, 110, 60, 40, "정답", "n2", "tl", 1, 14)]
_c2 = [R(170 + (i % 3) * 45, 90 + (i // 3) * 45, 38, 38, "n3", 2) for i in range(6)]
_c3 = [R(330 + (i % 6) * 22, 80 + (i // 6) * 22, 18, 18, "n", 3) for i in range(30)]
FIG_PPL = SVG(
    TX(240, 26, "퍼플렉서티 = 헷갈리는 후보가 평균 몇 개?", "tb", 15),
    *_c1, TX(60, 200, "PPL = 1", "tb", 15, "middle", 1), TX(60, 222, "완벽한 모델", "tm", 13, "middle", 1),
    *_c2, TX(236, 200, "PPL ≈ 5.7", "tb", 15, "middle", 2), TX(236, 222, "약 6개 중 고르기", "tm", 13, "middle", 2),
    *_c3, TX(395, 200, "PPL = V", "tb", 15, "middle", 3), TX(395, 222, "모두 같은 확률", "tm", 13, "middle", 3),
    TX(240, 258, "낮을수록 좋아요", "tb", 15, "middle", 3),
)

# ================= p.34 =================
S.append({"p": 34, "title": "3부 구분: 언어 모델링",
 "terms": [EN(k) for k in ["lm", "ntp", "ngram", "ppl"]],
 "pass1": [
  say("3부 **언어 모델링(Language Modeling)**이 시작돼요. 부제는 '다음 단어를 맞히는 일'이에요.",
      "주문의 마지막 조각 '벡터로 다음 토큰을 맞혀요'가 바로 이 부분이에요.",
      "배울 것: " + T("lm") + ", " + T("ngram") + ", 그리고 모델을 재는 자 " + T("ppl") + ".",
      "교수님은 이 " + T("ntp") + "가 자연어처리의 알파부터 오메가라고 했어요."),
 ],
 "pass2": [], "pass3": [], "pass4": []})

# ================= p.35 =================
S.append({"p": 35, "title": "언어 모델링이라는 과제",
 "terms": [EN(k) for k in ["lm", "ntp", "dist", "cprob", "pchain", "vocab", "token", "llm", "corpus"]],
 "pass1": [
  say("주문을 다시 불러요: " + MANTRA,
      "오늘은 마지막 조각, '다음 토큰을 맞히기'를 배워요.",
      T("lm") + "은 앞 글을 보고 다음에 올 단어를 맞히는 모델이에요."),
  analogy("휴대폰 자판의 다음 단어 추천",
          "휴대폰에 '오늘 수업은 몇 시에'까지 치면 자판 위에 '끝나요', '시작해요' 같은 추천이 떠요. 앞 글을 보고 다음 단어 후보마다 가능성을 매긴 거예요.",
          [["자판의 추천 단어", "다음 단어 후보"], ["추천 순서(가능성)", "후보마다 붙은 확률"], ["추천 기능 자체", T("lm")]]),
  figure("빈칸 뒤에 올 단어마다 확률을 붙여요", FIG_LM,
         "'the lecture will end at' 뒤에 9pm 0.2, noon 0.1, midnight 0.05, 나머지 후보가 0.65", 2),
 ],
 "pass2": [
  compare("영어 문장 → 우리말 뜻", ["슬라이드 영어", "우리말 뜻"], [
   ["**Language Modeling: The Task**", "언어 모델링이라는 과제"],
   ["given a prefix, predict a probability distribution over the next word", "앞부분이 주어지면, 다음 단어의 확률 분포를 내요"],
   ["assigns a probability to any piece of text", "어떤 글이든 그 글 전체의 확률을 매겨요"],
   ["chain rule of probability", "확률의 연쇄 법칙(한 단어씩 확률을 곱하기)"],
   ["One innocent-looking task, it will carry us all the way to GPT", "순해 보이는 이 과제 하나가 GPT 까지 이어져요"]]),
  points("용어 하나씩",
   T("lm") + ": 앞 단어들을 보고 다음 단어의 확률을 내는 모델",
   T("ntp") + ": 지금까지의 토큰으로 바로 다음 토큰 맞히기. 언어 모델이 하는 일 그 자체",
   T("dist") + ": 후보마다 확률을 붙인 목록. 모두 더하면 1",
   T("cprob") + ": 'B 가 주어졌을 때 A 의 확률' P(A | B). 앞 단어가 주어졌을 때 다음 단어의 확률",
   T("pchain") + ": 글 전체 확률 = 한 단어씩의 조건부 확률을 모두 곱한 것"),
  steps("무엇이 무엇으로 이어지나", [
   "앞부분(prefix) 'the lecture will end at' 이 들어와요",
   T("lm") + "이 " + T("vocab") + "의 모든 후보에 확률을 붙여요",
   "그게 다음 단어의 " + T("dist") + "예요: 9pm 0.2, noon 0.1, ...",
   "한 단어씩 이 확률을 곱해 가면 글 전체의 확률도 나와요(" + T("pchain") + ")"],
   "다음 단어 확률을 낼 수 있으면, 글 전체의 확률도 낼 수 있어요"),
  check("언어 모델(Language Model)이 내는 것은?",
        ["다음 단어 후보마다 붙은 확률(확률 분포)", "문장의 문법 오류 목록", "단어의 뜻풀이"], 0,
        T("lm") + "은 앞부분이 주어지면 다음 단어의 " + T("dist") + "를 내요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
   box(85, 155, 960, 188, "'given a prefix, predict a probability distribution over the next word': 앞부분 → 다음 단어 확률 분포"),
   box(105, 190, 1065, 218, "예: 'the lecture will end at ___' → {9pm: 0.2, noon: 0.1, midnight: 0.05, ...}"),
   box(85, 228, 1015, 260, "같은 말로: 어떤 글이든 확률을 매기는 모델(확률의 연쇄 법칙)"),
   box(270, 335, 585, 415, "왼쪽 식: x(1)~x(t)가 주어졌을 때 다음 단어 x(t+1)의 조건부 확률"),
   box(655, 325, 1130, 420, "오른쪽 식: 글 전체 확률 = 각 단어의 '앞 단어들이 주어졌을 때' 확률을 모두 곱한 것"),
   box(415, 678, 990, 708, "순해 보이는 과제 하나가 GPT 까지 이어져요")),
  formula("다음 단어의 확률 (언어 모델이 내는 것)",
   r"P\left(x^{(t+1)} \mid x^{(t)}, \ldots, x^{(1)}\right)",
   [(r"x^{(1)}, \ldots, x^{(t)}", "지금까지 나온 단어(토큰) t 개. 위 첨자 (t)는 '몇 번째 자리'라는 뜻"),
    (r"x^{(t+1)}", "바로 다음 자리에 올 단어. 맞히려는 것"),
    (r"\mid", "'~가 주어졌을 때'라고 읽어요. 조건부 확률 표시"),
    (r"P(\cdot)", "어휘의 후보마다 이 값을 내면 확률 분포가 돼요. 모두 더하면 1")],
   "지금까지의 단어들이 주어졌을 때, 다음 단어가 무엇일지 후보마다 확률을 내는 것이 " + T("lm") + "이에요."),
  formula("확률의 연쇄 법칙: 글 전체의 확률",
   r"P\left(x^{(1)}, \ldots, x^{(T)}\right) = \prod_{t=1}^{T} P\left(x^{(t)} \mid x^{(<t)}\right)",
   [(r"P(x^{(1)}, \ldots, x^{(T)})", "T 개 단어로 된 글 전체가 나올 확률"),
    (r"\prod_{t=1}^{T}", "t = 1 부터 T 까지 모두 곱하라는 기호(파이)"),
    (r"x^{(<t)}", "t 번째보다 앞에 나온 모든 단어"),
    (r"P(x^{(t)} \mid x^{(<t)})", "앞 단어들이 주어졌을 때 t 번째 단어의 확률. 언어 모델이 매번 내는 값")],
   "글 전체 확률은 '다음 단어 확률'을 한 단어씩 곱한 것이에요. 그래서 다음 단어만 잘 맞히면 글 전체의 확률도 매길 수 있어요."),
  steps("손계산: 확률 분포와 연쇄 법칙",
   ["슬라이드 후보: 9pm 0.2 + noon 0.1 + midnight 0.05 = 0.35",
    "확률 분포는 모두 더해 1이어야 하니, 나머지 후보들이 1 - 0.35 = 0.65 를 나눠 가져요",
    "예시 숫자로 연쇄 법칙: P(첫 단어) = 0.1, P(둘째 | 첫) = 0.5, P(셋째 | 첫, 둘째) = 0.2",
    "세 단어 글 전체의 확률 = 0.1 x 0.5 x 0.2 = 0.01"],
   "나머지 후보 몫 0.65, 예시 글의 확률 0.01",
   given="앞 두 줄은 슬라이드 숫자, 뒤 두 줄은 설명용 예시 숫자"),
  prof(MON2,
   "자연어처리에서는 랭귀지 모델링이라는 태스크가 거의 알파부터 오메가라고 보면 된다고 했어요.",
   "후보는 몇 개일까요? 쌓아 놓은 어휘(vocab) 개수만큼 있고, 모두 더하면 1이라고 했어요.",
   "\"지금까지 토큰으로 다음 토큰을 예측하는 next token prediction 이 거의 모든 걸 결정한다, GPT 도 다 결국 이거다.\""),
  bg("기초 다지기 5단원 (확률 기초)",
     "P(A | B) 는 조건부 확률, 'B 가 주어졌을 때 A 의 확률'이에요.",
     "곱의 규칙: P(A, B) = P(A) x P(B | A). 이걸 여러 번 이으면 연쇄 법칙이 돼요."),
  say("실습에서는 N3L p.9 에서 입력 x 를 한 칸 민 것을 정답 y 로 만들어요('shifted by one').",
      "곧 모든 자리에서 '다음 글자 맞히기'를 시키는 거예요."),
 ],
 "pass4": [
  check("언어 모델의 다음 단어 후보는 모두 몇 개인가요? (녹음 설명)",
        ["어휘(Vocabulary) 크기만큼", "항상 10개", "앞 문장 길이만큼"], 0,
        "교수님: 후보는 쌓아 놓은 " + T("vocab") + " 개수만큼이고, 모두의 확률을 더하면 1이에요."),
  english("답안에 쓸 문장",
   "언어 모델(Language Model)은 앞의 단어들 x(1)~x(t)가 주어졌을 때 다음 단어 x(t+1)의 조건부 확률 분포를 예측하는 모델이며, 확률의 연쇄 법칙으로 글 전체의 확률도 매길 수 있다.",
   "다음 단어 확률 = 언어 모델, 그 곱 = 글 전체 확률.", "앞부분 → 다음 단어 분포 → 곱하면 문장 확률"),
  warn("헷갈리기 쉬운 점",
   T("pchain") + "은 확률을 곱으로 쪼개는 규칙이에요. 2부 역전파의 연쇄 법칙(Chain Rule, 미분)과 이름만 같아요.",
   "확률 분포의 합은 늘 1이에요. 슬라이드에 보이는 세 후보(0.35)가 전부가 아니에요."),
 ]})

# ================= p.36 =================
S.append({"p": 36, "title": "매일 쓰는 언어 모델",
 "terms": [EN(k) for k in ["lm", "llm", "ntp", "token", "sample"]],
 "pass1": [
  say("사실 여러분은 이미 " + T("lm") + "을 매일 쓰고 있어요.",
      "휴대폰 자판, 검색창, 음성 인식, 그리고 ChatGPT 까지요."),
  points("언어 모델이 숨어 있는 곳",
   "휴대폰 자판 자동 완성: 다음 단어 후보를 줄 세워요",
   "검색어 추천: '자연어처리' 뒤에 강의, 책, 예제",
   "음성 인식과 번역: 비슷한 후보 중 더 자연스러운 쪽 고르기",
   "ChatGPT: 아주 큰 " + T("lm") + "이 다음 토큰을 계속 뽑는 것"),
 ],
 "pass2": [
  compare("영어 문장 → 우리말 뜻", ["슬라이드 영어", "우리말 뜻"], [
   ["**You Use One Every Day**", "여러분은 매일 하나씩 써요"],
   ["Keyboard autocomplete: ranks your next word as you type", "자판 자동 완성: 치는 동안 다음 단어를 줄 세워요"],
   ["Search suggestions: that's a LM over queries", "검색어 추천: 검색어에 대한 언어 모델이에요"],
   ["choosing between similar-sounding outputs", "비슷하게 들리는 후보 중 고르기"],
   ["sampling the next token again and again, that's the whole trick", "다음 토큰을 거듭 뽑는 것, 그게 비결의 전부예요"],
   ["LLM = Large Language Model", "LLM = 대규모 언어 모델. 가운데 LM 이 오늘 주제"]]),
  points("용어 하나씩",
   T("llm") + ": 아주 큰 언어 모델. 가운데 두 글자 LM 이 오늘 배우는 것",
   T("sample") + ": 확률 분포에서 제비뽑기처럼 후보 하나를 뽑기",
   T("ntp") + ": ChatGPT 도 결국 다음 토큰 맞히기를 되풀이해요"),
  check("LLM 의 가운데 두 글자 LM 은 무엇의 줄임말인가요?",
        ["Language Model (언어 모델)", "Linear Map", "Loss Minimum"], 0,
        T("llm") + " = Large " + T("lm") + ". 가운데가 오늘의 주제예요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
   box(85, 158, 720, 188, "Keyboard autocomplete: 치는 동안 다음 단어 후보를 줄 세워요"),
   box(85, 200, 955, 232, "Search suggestions: '자연어처리 ...' → 강의, 책, 예제. 검색어에 대한 언어 모델"),
   box(85, 244, 1295, 274, "Speech recognition & translation: 비슷하게 들리는 후보 중 무엇이 더 그럴듯한지 언어 모델에게 묻기"),
   box(85, 287, 1150, 318, "ChatGPT & friends: 아주 큰 LM 이 다음 토큰을 거듭 뽑기, 'that's the whole trick'"),
   box(360, 678, 1050, 708, "LLM = Large Language Model, 가운데 글자가 오늘 주제")),
  prof(MON2,
   "음성 인식도 헷갈려요. '아'라고 했는지 '야'라고 했는지, 지금까지 나온 단어를 보고 더 그럴듯한 쪽을 고르는 데 언어 모델이 도움을 준다고 했어요.",
   "번역에서도 더 자연스러운 토큰을 고르는 데 언어 모델이 역할을 한다고 했어요.",
   "추론(inference)은 예측하고, 붙이고, 붙인 것에서 또 예측하고 붙이는 것. LLM 같은 거대한 트랜스포머도 여전히 다음 토큰 예측으로 학습된다고 했어요."),
  points("다시 말하면",
   "네 가지 모두 '앞 글을 보고 다음(또는 더 그럴듯한) 것 고르기'예요",
   "ChatGPT 는 " + T("sample") + "로 다음 " + T("token") + "을 하나 뽑아 붙이고, 또 뽑아 붙여요",
   "그래서 오늘 배우는 작은 언어 모델과 ChatGPT 는 같은 고리를 돌아요(p.40 에서 다시 봐요)"),
  say("실습에서는 N3L p.15 의 generate 함수가 이 '뽑고 붙이기' 고리를 코드로 보여 줘요."),
 ],
 "pass4": [
  check("음성 인식에서 언어 모델은 어떤 일을 돕나요?",
        ["비슷하게 들리는 후보 중 문맥상 더 그럴듯한 것을 고른다", "소리의 크기를 키운다", "말하는 사람의 이름을 맞힌다"], 0,
        "슬라이드: choosing between similar-sounding outputs = asking a LM which is more plausible."),
  english("답안에 쓸 문장",
   "ChatGPT 같은 대규모 언어 모델(LLM)도 앞의 토큰들을 보고 다음 토큰의 확률 분포를 낸 뒤 하나를 샘플링해 붙이는 일을 반복하는 언어 모델(LM)이다.",
   "LLM 의 비결 = 다음 토큰 예측의 반복.", "뽑고, 붙이고, 또 뽑기"),
  warn("헷갈리기 쉬운 점",
   "검색어 추천, 자판 자동 완성은 '다른 기술'이 아니라 모두 " + T("lm") + "의 예예요.",
   "LLM 이 크다고 원리가 다른 게 아니에요. 원리는 " + T("ntp") + " 그대로예요."),
 ]})

# ================= p.37 =================
S.append({"p": 37, "title": "n-gram 언어 모델",
 "terms": [EN(k) for k in ["ngram", "markov", "corpus", "lm", "cprob", "ntp"]],
 "pass1": [
  analogy("바로 앞 몇 단어만 보고 맞히기",
          "기억력이 짧은 친구가 끝말을 이어요. 이 친구는 바로 앞 세 단어만 기억하고 그 전은 잊어버려요. 그리고 '예전에 이 세 단어 뒤에 무엇이 몇 번 나왔더라?'를 떠올려 가장 많이 나온 것을 말해요.",
          [["바로 앞 세 단어만 기억", T("markov")], ["세 단어 + 다음 단어 묶음", T("ngram") + " (여기서는 4-gram)"], ["예전에 몇 번 나왔나 떠올리기", T("corpus") + "에서 횟수 세기"]]),
  say("딥러닝 이전의 " + T("lm") + "이 바로 이 " + T("ngram") + " 모델이에요.",
      "규칙은 딱 두 가지예요: 앞 몇 단어만 보고, 큰 글 모음에서 세어 본다."),
 ],
 "pass2": [
  compare("영어 문장 → 우리말 뜻", ["슬라이드 영어", "우리말 뜻"], [
   ["**n-gram Language Models**", "n-gram 언어 모델"],
   ["The pre-deep-learning answer", "딥러닝 이전의 답"],
   ["n-gram = a chunk of n consecutive words", "n-gram = 연달아 붙은 단어 n개 묶음"],
   ["Markov assumption: the next word depends only on the previous n-1 words", "마르코프 가정: 다음 단어는 앞 n-1 개 단어에만 달려 있다"],
   ["Then just COUNT in a big corpus", "그다음엔 큰 말뭉치에서 그냥 세요"]]),
  points("용어 하나씩",
   T("ngram") + ": 연달아 붙은 단어 n개 묶음. 2개면 bigram, 3개면 trigram, 4개면 4-gram",
   T("markov") + ": 앞 n-1 개만 남기고 나머지 과거는 신경 쓰지 않기",
   T("corpus") + ": 횟수를 세는 큰 글 모음",
   "세기(COUNT): '앞 n-1 단어 + 다음 단어' 묶음 수 ÷ '앞 n-1 단어' 묶음 수"),
  check("4-gram 모델은 다음 단어를 맞힐 때 앞의 몇 단어를 보나요?", ["3단어", "4단어", "문장 전체"], 0,
        "n-gram 은 앞 n-1 개를 봐요. 4-gram 이면 앞 3단어 + 맞힐 1단어 = 4단어 묶음이에요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
   box(85, 155, 815, 185, "'The pre-deep-learning answer': 딥러닝 이전의 답. n-gram = 연달은 n 단어 묶음"),
   box(85, 198, 860, 228, "'Markov assumption': 다음 단어는 앞 n-1 개 단어에만 달려 있다고 쳐요"),
   box(275, 310, 1015, 368, "근사 식: 앞 단어 전부 대신 앞 n-1 개만 조건으로 남겨요"),
   box(520, 395, 1070, 430, "'keep only the last n-1 words': 마지막 n-1 단어만 남기기"),
   box(140, 525, 1255, 628, "세기: count(students opened their w) ÷ count(students opened their)"),
   box(395, 678, 1010, 708, "1주차 2막(통계 시대)의 실제 식이 이것이에요")),
  formula("마르코프 가정: n-gram 근사",
   r"P\left(x^{(t+1)} \mid x^{(t)}, \ldots, x^{(1)}\right) \approx P\left(x^{(t+1)} \mid x^{(t)}, \ldots, x^{(t-n+2)}\right)",
   [(r"x^{(t)}, \ldots, x^{(1)}", "왼쪽: 지금까지 나온 모든 단어"),
    (r"\approx", "'거의 같다고 친다'. 가정으로 바꿔치기"),
    (r"x^{(t)}, \ldots, x^{(t-n+2)}", "오른쪽: 바로 앞 n-1 개 단어만 남긴 것"),
    (r"n", "묶음 크기. 4-gram 이면 n = 4, 앞 3단어를 봐요")],
   "먼 과거는 버리고 바로 앞 n-1 개 단어만 보고 다음 단어의 확률을 정한다는 가정이에요."),
  formula("세어서 확률 구하기 (슬라이드 예)",
   r"P(w \mid \text{students opened their}) \approx \frac{\mathrm{count}(\text{students opened their } w)}{\mathrm{count}(\text{students opened their})}",
   [(r"w", "다음에 올 후보 단어 하나(books, exams, ...)"),
    (r"\mathrm{count}(\text{students opened their } w)", "분자: 4단어 묶음이 말뭉치에 나온 횟수"),
    (r"\mathrm{count}(\text{students opened their})", "분모: 앞 3단어 묶음이 나온 횟수")],
   "'앞 3단어 뒤에 w 가 온 횟수'를 '앞 3단어가 나온 횟수'로 나누면 확률이에요. 학습이 아니라 세기예요."),
  steps("n-1 이 맞는지 세어 보기",
   ["식의 오른쪽은 x^(t) 부터 x^(t-n+2) 까지예요",
    "개수 = t - (t-n+2) + 1 = n - 1",
    "n = 4 이면 x^(t), x^(t-1), x^(t-2) 의 3개",
    "n = 2(bigram) 이면 바로 앞 1단어만"],
   "n-gram 은 앞 n-1 개 단어를 조건으로 봐요"),
  prof(MON2,
   "엔그램은 말 그대로 연속된 n 개의 단어 묶음이에요. students opened their books 4개면 4그램, books 를 떼면 3그램(트라이그램)이라고 했어요.",
   "마르코프 과정은 과거는 신경 쓰지 않고 현재만 보겠다는 것, 그래서 내 엔그램만 보고 다음 단어를 예측한다고 했어요.",
   "딥러닝 이전이라 카운팅 기법, 통계 기법이에요. 코퍼스에서 4개씩 묶어 다 모은 다음 개수를 구해요."),
  bg("기초 다지기 5단원 (확률 기초)",
     "빈도로 확률 세기: 조건이 된 경우의 수 중에서 원하는 일이 일어난 비율이에요.",
     "P(w | 앞 단어) = (앞 단어 뒤에 w 가 온 횟수) ÷ (앞 단어가 나온 횟수)."),
 ],
 "pass4": [
  check("n-gram 언어 모델이 확률을 구하는 방법은?",
        ["말뭉치에서 단어 묶음이 나온 횟수를 세어 나눈다", "경사 하강법으로 임베딩을 학습한다", "사람이 확률을 직접 적어 넣는다"], 0,
        "슬라이드: Then just COUNT in a big corpus. 학습이 아니라 세기예요."),
  english("답안에 쓸 문장",
   "n-gram 언어 모델은 마르코프 가정(Markov Assumption)에 따라 다음 단어가 앞 n-1 개 단어에만 달려 있다고 보고, 말뭉치(Corpus)에서 n-gram 과 (n-1)-gram 의 횟수를 세어 그 비율로 조건부 확률을 구한다.",
   "앞 n-1 개만 보기 + 세어서 나누기.", "마르코프로 자르고, 세어서 나눈다"),
  warn("헷갈리기 쉬운 점",
   "n-gram 의 n 은 '묶음 전체 크기'예요. 조건으로 보는 앞 단어는 n-1 개예요(4-gram → 앞 3단어).",
   "분모는 '앞 n-1 단어 묶음'의 횟수예요. 전체 단어 수로 나누지 않아요."),
 ]})

# ================= p.38 =================
S.append({"p": 38, "title": "n-gram 예제: 시험 감독관 문장",
 "terms": [EN(k) for k in ["ngram", "markov", "corpus", "cprob", "lm", "rnn"]],
 "pass1": [
  say("'as the proctor started the clock, the students opened their ___'",
      "proctor 는 시험 감독관이에요. 감독관이 시계를 켰으니 빈칸은 exams(시험지)가 어울려요.",
      "그런데 4-gram 모델은 앞 3단어 'students opened their'만 봐요."),
  figure("앞 3단어만 남기고 나머지는 버려요", FIG_NG,
         "proctor, clock 은 버려지고, students opened their 뒤에 books 가 400/1000 = 0.40", 2),
 ],
 "pass2": [
  compare("영어 문장 → 우리말 뜻", ["슬라이드 영어", "우리말 뜻"], [
   ["**n-gram, a Worked Example**", "n-gram 풀어 본 예제"],
   ["4-gram model, so we keep the last 3 words and throw the rest away", "4-gram 이라 마지막 3단어만 남기고 나머지는 버려요"],
   ["discarded by the Markov assumption", "마르코프 가정 때문에 버려진 부분"],
   ["condition on these 3 words", "이 3단어를 조건으로 봐요"],
   ["that context was thrown away", "그 문맥(proctor, clock)이 버려졌어요"],
   ["The model is not wrong, it was FORCED to forget the words that mattered", "모델이 틀린 게 아니라, 중요한 단어를 잊도록 강요당했어요"]]),
  steps("무엇이 무엇으로 이어지나", [
   T("markov") + ": 4-gram 이니 앞 3단어 students opened their 만 남겨요",
   T("corpus") + "에서 셉니다: students opened their 1,000번",
   "그 뒤에 books 400번, exams 100번",
   "books 0.40 > exams 0.10 → 모델은 books 를 골라요",
   "하지만 버려진 proctor, clock 은 exams 를 가리켰어요"],
   "중요한 단서가 3단어 밖에 있으면 n-gram 은 볼 수 없어요"),
  check("이 예제에서 n-gram 모델이 exams 대신 books 를 고르는 까닭은?",
        ["proctor, clock 같은 단서가 3단어 밖이라 버려졌기 때문", "books 라는 단어가 어휘에 없어서", "계산 실수 때문"], 0,
        "슬라이드: 모델은 틀린 게 아니라 중요한 단어를 잊도록 강요당했어요(" + T("markov") + ")."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
   box(125, 285, 765, 338, "회색 단어들: as the proctor started the clock, the. 마르코프 가정으로 버려져요"),
   box(765, 285, 1110, 338, "주황 상자 3개: students opened their. 이 3단어만 조건으로 봐요"),
   box(215, 400, 830, 432, "count(students opened their) = 1,000"),
   box(215, 440, 1025, 512, "books 400 → P = 0.40, exams 100 → P = 0.10"),
   box(215, 538, 1095, 568, "하지만 proctor 와 clock 때문에 exams 가 더 나은 답이었어요, 그 문맥이 버려졌어요")),
  steps("손계산: 슬라이드 숫자 그대로",
   ["분모: count(students opened their) = 1,000",
    "P(books | students opened their) = 400 ÷ 1,000 = 0.40",
    "P(exams | students opened their) = 100 ÷ 1,000 = 0.10",
    "연습: 어떤 단어가 300번이었다면 300 ÷ 1,000 = 0.30"],
   "books 0.40, exams 0.10 → n-gram 은 books 를 더 그럴듯하다고 봐요",
   given="4-gram, 앞 3단어 students opened their"),
  steps("손계산: 한 번도 못 본 묶음이면 (예시)",
   ["예시로 students opened their laptops 가 말뭉치에 0번이라고 해요",
    "P(laptops | students opened their) = 0 ÷ 1,000 = 0",
    "글 전체 확률은 한 단어씩의 확률을 곱해요(p.35 연쇄 법칙)",
    "곱 속에 0이 하나라도 있으면: 0.4 x 0.5 x 0 = 0",
    "앞 3단어 자체가 0번이면 0 ÷ 0, 나눌 수가 없어요"],
   "분자 0 → 확률 0(문장 전체 0), 분모 0 → 계산 불가. 다음 쪽의 희소성 문제예요",
   given="laptops 횟수와 0.4, 0.5 는 설명용 예시 숫자"),
  prof(MON2,
   "앞 문장에 proctor(시험 감독관)나 clock(시간) 같은 단서가 있으니 사실 books 보다 exams 가 나올 가능성이 더 높아야 한다고 했어요.",
   "n-gram 통계 기반은 마르코프 가정 때문에 앞 정보를 전혀 보지 못해서, 필요한 정보가 멀리 있으면 강제로 잊어버린다고 했어요.",
   "그래서 '앞 문맥을 버리지 않고 계속 기억하며 읽을 수 있을까?'가 뒤의 시퀀스 모델(" + T("rnn") + ")로 이어진다고 했어요."),
  bg("기초 다지기 5단원 (확률 기초)",
     "0을 곱하면 무엇이든 0이에요. 곱으로 만든 확률은 한 조각만 0이어도 전체가 0이 돼요.",
     "0으로 나누기는 정의되지 않아요. 조건이 한 번도 없으면 조건부 확률을 셀 수 없어요."),
 ],
 "pass4": [
  check("count(students opened their) = 1,000, count(students opened their exams) = 100 일 때 P(exams | students opened their) 는?",
        ["0.10", "0.40", "100"], 0,
        "100 ÷ 1,000 = 0.10. 분모는 앞 3단어 묶음의 횟수예요."),
  english("답안에 쓸 문장",
   "4-gram 모델은 마르코프 가정에 따라 앞 3단어만 조건으로 보기 때문에, 그보다 앞에 있는 중요한 문맥(예: proctor, clock)을 강제로 버리게 되어 books(0.40)를 exams(0.10)보다 높게 예측한다.",
   "모델이 틀린 게 아니라 잊도록 강요당한 것.", "400/1000 = 0.40, 100/1000 = 0.10"),
  warn("헷갈리기 쉬운 점",
   "녹음에서는 books 확률이 '0.45'처럼 들리지만 슬라이드 계산은 400 ÷ 1,000 = 0.40 이에요. 시험에서는 계산대로 0.40.",
   "n-gram 이 '틀렸다'가 아니라 마르코프 가정 때문에 '볼 수 없었다'가 슬라이드의 요점이에요."),
 ]})

# ================= p.39 =================
S.append({"p": 39, "title": "세기가 부딪히는 벽",
 "terms": [EN(k) for k in ["sparse", "smooth", "backoff", "ngram", "corpus", "onehot", "emb", "markov", "lm"]],
 "pass1": [
  figure("세기만으로는 넘기 힘든 세 개의 벽", FIG_WALLS,
         "희소성, 저장 공간, 유사도 없음. 그리고 앞 n-1 단어 밖은 보이지 않아요", 3),
  say(T("ngram") + "은 세기만 하니 간단하지만, 벽이 세 개 있어요.",
      "안 나온 건 0, 셀 게 너무 많고, 비슷한 단어를 몰라요.",
      "4부의 " + T("fwlm") + "이 " + T("emb") + " 덕분에 이 벽을 허물어요."),
 ],
 "pass2": [
  compare("영어 문장 → 우리말 뜻", ["슬라이드 영어", "우리말 뜻"], [
   ["**Where Counting Breaks**", "세기가 부서지는 곳"],
   ["Sparsity: numerator never seen → probability 0 (fix: smoothing)", "희소성: 분자를 못 봤으면 확률 0 (고치기: 스무딩)"],
   ["denominator never seen → cannot condition at all (fix: back off)", "분모를 못 봤으면 조건을 걸 수조차 없음 (고치기: 더 짧은 문맥으로 백오프)"],
   ["it gets WORSE as n grows, in practice n ≤ 5", "n 이 커질수록 심해져서 실제로는 n ≤ 5"],
   ["Storage: grows with corpus × n", "저장: 말뭉치 크기와 n 에 따라 불어나요"],
   ["Blindness: no notion of similarity", "눈멂: 비슷함이라는 개념이 없어요"],
   ["Discarded context: everything beyond n-1 words is invisible", "버려진 문맥: n-1 단어 밖은 아무리 중요해도 안 보여요"]]),
  points("용어 하나씩",
   T("sparse") + ": 셀 묶음이 거의 안 나와서 0 투성이인 문제",
   T("smooth") + ": 못 본 묶음에도 아주 작은 확률을 나눠 주기(분자 0 고치기)",
   T("backoff") + ": 긴 문맥으로 못 세면 더 짧은 문맥으로 물러나기(분모 0 고치기)",
   "저장(Storage): 본 적 있는 n-gram 마다 횟수를 적어 둬야 해요",
   "유사도 없음: 'opened their'와 'opened her'는 횟수를 전혀 나누지 않아요. " + T("onehot") + "과 같은 병"),
  check("분모(앞 문맥)가 말뭉치에 한 번도 없을 때 슬라이드가 말하는 고치기는?",
        ["더 짧은 문맥으로 물러나기(Back-off)", "스무딩(Smoothing)", "n 을 더 키우기"], 0,
        "분자 0 → " + T("smooth") + ", 분모 0 → " + T("backoff") + ". n 을 키우면 오히려 더 나빠져요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
   box(85, 155, 1295, 218, "Sparsity: 분자 0 → 확률 0(스무딩), 분모 0 → 조건 불가(더 짧은 문맥으로 백오프)"),
   box(160, 222, 605, 252, "n 이 커질수록 나빠져요. 실제로는 n ≤ 5"),
   box(85, 265, 940, 298, "Storage: 본 n-gram 마다 횟수 저장, 말뭉치 x n 으로 불어나요"),
   box(85, 310, 1255, 342, "Blindness: 'opened their'와 'opened her'가 횟수를 안 나눠요. 2주차의 그 병(비슷함 없음)"),
   box(85, 355, 935, 388, "Discarded context: n-1 단어 밖은 아무리 중요해도 안 보여요"),
   box(275, 678, 1135, 708, "세 벽: 희소성, 저장, 유사도. 오늘 신경망 언어 모델이 둘을 허물어요")),
  steps("왜 n 이 커질수록 나빠지나 (가능한 조합 수)",
   ["어휘가 1만 개라고 해요",
    "앞 1단어 문맥의 종류: 1만 가지",
    "2단어 묶음의 종류: 1만 x 1만 = 1억 가지",
    "3단어 묶음의 종류: 1만^3 = 1조 가지",
    "말뭉치가 아무리 커도 1조 가지를 다 보기는 어려워요 → 대부분 0번"],
   "n 이 1 늘 때마다 조합이 어휘 크기 배로 늘어요. 그래서 희소성이 심해지고 실제로는 n ≤ 5",
   given="어휘 1만 개는 설명용 숫자"),
  prof(MON2,
   "스튜던츠 오픈드 데어라는 문장 자체도 많이 안 나오고, 그 뒤 단어도 개수가 많지 않아서 어휘 대부분에 대해 값이 거의 다 0이라고 했어요.",
   "스무딩이나 더 짧은 문맥으로 가는 백오프로 개선할 수는 있지만 아주 좋은 방법은 아니라고 했어요.",
   "opened their, opened her, opened his 는 의미상 똑같은데 n-gram 은 완전 별개 항목이라 정보를 공유하지 못한다, '말로 하면 입 아플 정도로 안 좋은 점이 많다'고 했어요."),
  bg("기초 다지기 1단원 (벡터, 원-핫 벡터 맛보기)",
     T("onehot") + "끼리는 내적이 늘 0이라 비슷함을 모른다는 게 2주차의 병이었어요.",
     "n-gram 이 their 와 her 를 남남으로 보는 것도 같은 병이에요. 해결책은 " + T("emb") + "(단어의 지도 좌표)예요."),
 ],
 "pass4": [
  check("슬라이드가 말하는 n-gram 의 세 벽이 아닌 것은?",
        ["학습 속도가 너무 빠르다", "희소성(Sparsity)", "저장 공간(Storage)", "유사도 없음(Similarity)"], 0,
        "세 벽은 sparsity, storage, similarity 예요. n-gram 은 학습이 아니라 세기라서 빠르기는 문제가 아니에요."),
  english("답안에 쓸 문장",
   "n-gram 언어 모델에는 희소성 문제(Sparsity Problem), 저장 공간 문제, 유사도 없음의 세 벽과, n-1 단어 밖 문맥을 볼 수 없다는 한계가 있다.",
   "벽 셋 + 버려진 문맥.", "희소, 저장, 유사도 + 문맥"),
  warn("헷갈리기 쉬운 점",
   "분자 0 → " + T("smooth") + ", 분모 0 → " + T("backoff") + ". 짝을 바꿔 외우지 마세요.",
   "n 을 키우면 문맥은 길어지지만 희소성과 저장이 더 나빠져요. 그래서 실제로는 n ≤ 5 예요.",
   "유사도 없음의 뿌리는 단어를 " + T("onehot") + "처럼 남남으로 다루는 것, 해결은 " + T("emb") + "이에요."),
 ]})

# ================= p.40 =================
S.append({"p": 40, "title": "n-gram 언어 모델로 글 쓰기",
 "terms": [EN(k) for k in ["lm", "sample", "ngram", "dist", "temp", "llm", "rnn", "soft"]],
 "pass1": [
  figure("만들고, 뽑고, 붙이고, 되풀이", FIG_GEN,
         "확률 분포에서 하나를 뽑아 뒤에 붙이고 다시 분포를 만들어요. ChatGPT 도 같은 고리예요", 3),
  analogy("자판 추천 단어를 계속 누르기",
          "휴대폰 자판에서 추천 단어 하나를 누르면 또 새 추천이 떠요. 그걸 또 누르고, 또 누르면 문장이 저절로 써져요. 다만 추천이 바로 앞 두 단어만 보고 뜬다면 문장이 점점 산으로 가요.",
          [["추천 단어 누르기", T("sample") + " 후 붙이기"], ["또 뜨는 새 추천", "새 " + T("dist")], ["앞 두 단어만 보는 추천", "trigram " + T("lm")]]),
 ],
 "pass2": [
  compare("영어 문장 → 우리말 뜻", ["슬라이드 영어", "우리말 뜻"], [
   ["**Generating with an n-gram LM**", "n-gram 언어 모델로 글 생성하기"],
   ["A LM is also a text generator: sample from the distribution, append, repeat", "언어 모델은 글 생성기이기도 해요: 분포에서 뽑고, 붙이고, 반복"],
   ["trigram LM: condition on the last 2 words", "trigram 언어 모델: 마지막 2단어를 조건으로"],
   ["locally grammatical but globally incoherent", "가까이 보면 문법이 맞지만 전체로 보면 앞뒤가 안 맞아요"],
   ["Same sampling loop as ChatGPT, the model quality is the only difference", "ChatGPT 와 같은 뽑기 고리, 다른 건 모델 실력뿐"]]),
  steps("생성 고리 한 바퀴씩", [
   "시작: today the",
   "마지막 2단어 today the → 분포 {price 0.31, news 0.15, ...} → price 뽑기",
   "the price → {of 0.62, ...} → of, price of → gold, of gold → is",
   "gold is → {shiny 0.41, high 0.19, rising 0.12, ...} → shiny",
   "결과: today the price of gold is \"shiny\""],
   "한 칸씩은 자연스럽지만 전체 문장은 어색해요"),
  points("용어 하나씩",
   T("sample") + ": 분포에 따라 제비뽑기. 확률이 크면 자주 뽑히지만 늘 1등은 아니에요",
   "locally grammatical: 이웃 단어끼리는 문법이 맞아요",
   "globally incoherent: 문장 전체로는 앞뒤가 안 맞아요"),
  check("n-gram 언어 모델로 만든 글의 특징은?",
        ["가까이 보면 자연스럽지만 전체로는 앞뒤가 안 맞는다", "문법이 늘 틀린다", "항상 같은 문장만 나온다"], 0,
        "슬라이드: locally grammatical but globally incoherent. 짧은 기억 때문이에요."),
 ],
 "pass3": [
  look("그림 짚어 읽기",
   box(85, 155, 835, 185, "'A LM is also a text generator': 분포에서 뽑고, 붙이고, 반복"),
   box(305, 212, 985, 242, "trigram LM: 마지막 2단어를 조건으로 → 다음 단어 뽑기 → 반복"),
   box(215, 268, 555, 468, "today the → price 0.31, news 0.15 ... / the price → of 0.62, is 0.21 ..."),
   box(765, 268, 1095, 468, "of gold → is 0.34 ... / gold is → shiny 0.41, high 0.19 ..."),
   box(465, 492, 840, 525, "결과: today the price of gold is \"shiny\""),
   box(85, 585, 900, 615, "문법은 이웃끼리 맞지만 전체는 어색. 짧은 기억이 드러나요")),
  steps("손계산: 이 경로가 뽑힐 확률 (슬라이드 숫자)",
   ["각 상자에서 뽑힌 단어의 확률: price 0.31, of 0.62, gold 0.57, is 0.34, shiny 0.41",
    "연쇄 법칙대로 모두 곱해요: 0.31 x 0.62 = 0.1922",
    "x 0.57 = 0.1096, x 0.34 = 0.0372, x 0.41 = 0.0153",
    "재미있는 점: 다섯 번 모두 그 상자의 1등 후보가 뽑혔어요"],
   "'today the' 뒤에 이 다섯 단어가 이어질 확률 ≈ 0.0153 (약 1.5%)",
   given="trigram, 시작 today the"),
  prof(MON2,
   "today the price of gold is 까지는 굉장히 자연스러운데, 앞이 price 였으니 gold is 다음에는 expected 같은 게 오면 좋겠죠.",
   "그런데 gold is shiny 라는 trigram 자체는 어색하지 않아요. 금은 빛날 수 있죠. 하지만 전부 붙이면 이상해진다고 했어요.",
   "로컬 플루언시는 챙길 수 있지만 롱 레인지 코히어런스(글로벌 플루언시)는 챙길 수 없다고 했어요. 이건 세기 기법과 상관없이 짧은 문맥의 문제예요."),
  say("실습에서는 N3L p.15 generate 가 '분포 → 하나 뽑기(torch.multinomial) → 다시 넣기'를 되풀이해요.",
      "N3L p.16 은 " + T("temp") + "를 0.5, 1.0, 1.5 로 바꿔 봐요. 낮으면 무난하고, 1.5 면 글자가 엉망이 돼요."),
  bg("기초 다지기 6단원 (소프트맥스와 교차 엔트로피)",
     "실습의 온도는 점수(logits)를 온도로 나눈 뒤 " + T("soft") + "를 해요.",
     "온도가 작으면 1등 확률이 더 커지고, 크면 확률이 고르게 퍼져요."),
 ],
 "pass4": [
  check("슬라이드의 trigram 예시에서 다음 단어를 정할 때 보는 것은?",
        ["바로 앞 2단어", "바로 앞 3단어", "문장 전체"], 0,
        "trigram = 3단어 묶음이니 조건은 앞 2단어예요(today the → price)."),
  check("샘플링 온도(Temperature)를 1.5 처럼 높이면?",
        ["엉뚱한 후보도 자주 뽑혀 글이 엉망이 되기 쉽다", "늘 1등만 뽑힌다", "모델이 다시 학습된다"], 0,
        "실습 N3L p.16: 온도가 높을수록 확률이 고르게 퍼져 과감하게 뽑아요."),
  english("답안에 쓸 문장",
   "언어 모델은 다음 단어의 확률 분포에서 하나를 샘플링(Sampling)해 붙이고 다시 예측하는 과정을 반복해 글을 생성한다. n-gram 은 앞 n-1 단어만 기억하므로 결과가 국소적으로는 문법적이지만 전체적으로는 일관성이 없다.",
   "뽑고, 붙이고, 반복 + 짧은 기억의 한계.", "locally grammatical, globally incoherent"),
  warn("헷갈리기 쉬운 점",
   "슬라이드 아래 줄은 'the 3-word memory shows'라고 하지만 그림은 trigram(앞 2단어 조건)이에요. trigram 은 묶음 3단어, 조건 2단어라고 기억해요.",
   "샘플링은 1등만 고르는 게 아니에요. 이 예에서는 우연히 매번 1등이 뽑혔을 뿐이에요."),
 ]})

# ================= p.41 =================
S.append({"p": 41, "title": "언어 모델 재기: 퍼플렉서티",
 "terms": [EN(k) for k in ["ppl", "ce", "loss", "geo", "vocab", "lm", "ngram", "llm", "soft"]],
 "pass1": [
  analogy("헷갈리는 후보가 평균 몇 개?",
          "퀴즈에서 보기가 2개면 덜 헷갈리고, 100개면 많이 헷갈려요. 언어 모델이 다음 단어를 고를 때 '평균 몇 개 보기 사이에서 헷갈리는 정도인지'를 숫자 하나로 나타낸 게 퍼플렉서티예요.",
          [["퀴즈 보기 수", T("ppl")], ["보기가 적을수록 쉬움", "낮을수록 좋은 모델"], ["보기 1개(정답만)", "PPL = 1, 완벽한 모델"]]),
  say(T("ppl") + "는 언어 모델의 성적표 숫자예요. 낮을수록 좋아요.",
      "어휘 1만 개에 아무렇게나 찍으면 1만, 좋은 n-gram 은 100 쯤, 요즘 LLM 은 10 아래(예시)."),
 ],
 "pass2": [
  compare("영어 문장 → 우리말 뜻", ["슬라이드 영어", "우리말 뜻"], [
   ["**Measuring LMs, Perplexity**", "언어 모델 재기: 퍼플렉서티"],
   ["Perplexity = exp(cross-entropy loss)", "퍼플렉서티 = exp(교차 엔트로피 손실)"],
   ["geometric-mean inverse probability", "정답 확률의 역수를 기하 평균한 것"],
   ["as confused as a fair choice among PPL words", "PPL 개 단어 중에서 공평하게 찍는 것만큼 헷갈려요"],
   ["uniform over 10k words → PPL 10,000", "1만 단어에 똑같은 확률 → PPL 10,000"],
   ["it drops out of the SAME cross-entropy loss we already train with", "이미 학습에 쓰는 바로 그 교차 엔트로피 손실에서 나와요"]]),
  points("용어 하나씩",
   T("ppl") + ": 다음 단어를 고를 때 헷갈리는 후보가 평균 몇 개인지. 낮을수록 좋아요",
   T("ce") + ": 정답 단어 확률의 -log. 정답 확률이 클수록 작아요",
   T("loss") + " J: 매 위치의 교차 엔트로피를 평균 낸 것",
   T("geo") + ": 모두 곱하고 개수만큼 제곱근. 더해서 나누는 평균과 달라요"),
  steps("무엇이 무엇으로 이어지나", [
   "매 위치에서 정답 다음 단어에 모델이 준 확률 P 를 봐요",
   "벌점 -log P 를 매겨요(" + T("ce") + ")",
   "위치마다의 벌점을 평균 내면 J",
   "exp(J) 를 하면 " + T("ppl"),
   "학습도 같은 " + T("loss") + " J 를 줄여요. 그래서 학습이 잘 되면 PPL 도 내려가요"],
   "PPL = exp(평균 교차 엔트로피)"),
  check("퍼플렉서티(PPL)는 어느 쪽이 더 좋은 모델인가요?", ["낮을수록 좋다", "높을수록 좋다", "1000 에 가까울수록 좋다"], 0,
        "슬라이드: lower is better. PPL 이 낮으면 헷갈리는 후보가 적다는 뜻이에요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
   box(85, 155, 1045, 185, "'Perplexity = exp(cross-entropy loss)': 정답 확률 역수의 기하 평균"),
   box(245, 265, 845, 368, "PPL = exp(J) = 각 위치 1/P 를 곱해 1/T 제곱"),
   box(895, 290, 1155, 340, "(lower is better): 낮을수록 좋아요"),
   box(85, 410, 955, 442, "Intuition: 평균적으로 PPL 개 단어 중 공평하게 찍는 만큼 헷갈려요"),
   box(160, 446, 1010, 476, "1만 단어 균등 → 10,000, 좋은 n-gram ≈ 100, 요즘 LLM < 10 (예시)"),
   box(85, 486, 1000, 518, "이미 학습에 쓰는 같은 교차 엔트로피 손실에서 나와요")),
  formula("퍼플렉서티 식",
   r"\mathrm{PPL} = \exp(J) = \prod_{t=1}^{T} \left( \frac{1}{P\left(x^{(t+1)} \mid x^{(\le t)}\right)} \right)^{1/T}",
   [(r"P(x^{(t+1)} \mid x^{(\le t)})", "t 번째까지 보고, 실제 정답 다음 단어에 모델이 준 확률"),
    (r"\frac{1}{P}", "그 확률의 역수. 확률 1/4 이면 4(후보 4개 중 찍는 느낌)"),
    (r"\prod_{t=1}^{T}", "T 개 위치 모두 곱하기"),
    (r"(\cdot)^{1/T}", "T 제곱근. 곱한 것의 평균(기하 평균)"),
    (r"J", "교차 엔트로피 손실의 평균")],
   "정답 확률의 역수를 기하 평균한 것이 퍼플렉서티이고, 이는 평균 교차 엔트로피 J 에 exp 를 씌운 것과 같아요."),
  formula("J: 위치마다의 손실을 평균 내기",
   r"J = \frac{1}{T} \sum_{t=1}^{T} -\log P\left(x^{(t+1)} \mid x^{(\le t)}\right)",
   [(r"-\log P", "정답 단어 확률의 음의 로그. 한 위치의 교차 엔트로피 벌점"),
    (r"\sum_{t=1}^{T}", "T 개 위치의 벌점을 모두 더하기"),
    (r"\frac{1}{T}", "위치 수로 나눠 평균"),
    (r"J", "평균 벌점. 학습이 줄이는 바로 그 손실")],
   "학습 때 줄이는 손실 J 에 exp 만 씌우면 퍼플렉서티예요. 그래서 따로 계산할 게 거의 없어요."),
  steps("손계산: 아무것도 모르는 모델",
   ["어휘 V = 10,000, 모든 단어에 똑같이 1/10,000",
    "위치마다 벌점 -log(1/10,000) = log 10,000 ≈ 9.21",
    "평균 J 도 9.21 (모든 위치가 같으니까)",
    "PPL = exp(9.21) = 10,000"],
   "균등 분포면 PPL = 어휘 크기 V (슬라이드의 10,000)",
   given="자연로그 사용"),
  prof(MON2,
   "소프트맥스에 음의 로그 우도(NLL)를 붙이면 크로스 엔트로피. 정답이 gold 일 때 gold 의 확률이 높을수록 로스가 떨어지고, 이상한 단어의 확률이 높으면 올라가요.",
   "그 크로스 엔트로피 로스에 익스포넨셜을 취하면 바로 PPL 이라고 했어요.",
   "PPL 이 100 이면 모델이 매 순간 대략 100 개 후보에서 하나를 고를 정도의 불확실성, 낮으면 낮을수록 좋다고 했어요."),
  bg("기초 다지기 4단원, 6단원 (로그와 지수, 교차 엔트로피)",
     "exp 와 log 는 서로 되돌리는 짝이에요. exp(log 10,000) = 10,000.",
     "로그는 곱을 합으로 바꿔요. 그래서 '곱의 T 제곱근'이 'log 합의 평균'의 exp 가 돼요."),
  say("실습에서는 N3L p.17 에서 PPL = exp(평균 loss)를 직접 계산해요. 글자 모델은 25.92, 어휘 V = 1945 보다 훨씬 낮아요.",
      "N3L p.12 학습 출력도 같아요: loss 3.254 → exp(3.254) ≈ 25.9."),
 ],
 "pass4": [
  check("교차 엔트로피 손실 평균 J 와 퍼플렉서티의 관계는?", ["PPL = exp(J)", "PPL = log(J)", "PPL = 1/J"], 0,
        "슬라이드: Perplexity = exp(cross-entropy loss)."),
  english("답안에 쓸 문장",
   "퍼플렉서티(Perplexity)는 정답 다음 단어 확률의 역수를 기하 평균한 값으로, 평균 교차 엔트로피 손실 J 에 exp 를 씌운 것(PPL = exp(J))과 같다. 모델이 평균적으로 몇 개 후보 사이에서 헷갈리는지를 뜻하며 낮을수록 좋다.",
   "PPL = exp(J), 곧 손실 함수(Loss Function) 평균의 exp. 낮을수록 좋음, 균등이면 V.", "역수의 기하 평균 = exp(평균 -log P)"),
  warn("헷갈리기 쉬운 점",
   "정확도(accuracy)는 높을수록 좋지만 " + T("ppl") + "는 낮을수록 좋아요. 방향을 거꾸로 쓰지 마세요.",
   "기하 평균이에요. 1/P 들을 더해서 나누는 산술 평균이 아니에요."),
 ]})

# ================= p.42 =================
S.append({"p": 42, "title": "퍼플렉서티 예제와 주의점",
 "terms": [EN(k) for k in ["ppl", "geo", "vocab", "tokzr", "token", "ce", "lm"]],
 "pass1": [
  figure("PPL 1, 약 5.7, V", FIG_PPL,
         "완벽하면 1, 이 예제는 약 6개 중 고르는 정도(5.7), 아무것도 모르면 어휘 크기 V", 3),
  say("모델이 the, cat, sat, down 에 1/2, 1/4, 1/8, 1/16 확률을 줬어요.",
      "계산하면 " + T("ppl") + " ≈ 5.7, '약 6개 중에서 찍는 만큼 헷갈린다'예요.",
      "단, 같은 " + T("tokzr") + "를 쓴 모델끼리만 비교할 수 있어요."),
 ],
 "pass2": [
  compare("영어 문장 → 우리말 뜻", ["슬라이드 영어", "우리말 뜻"], [
   ["**Perplexity, a Worked Example**", "퍼플렉서티 풀어 본 예제"],
   ["assigns these probabilities to the TRUE next words", "실제 정답 다음 단어에 이런 확률을 줬어요"],
   ["as confused as guessing uniformly among ~6 words", "약 6개 단어 중 공평하게 찍는 만큼 헷갈려요"],
   ["Sanity anchors", "상식 기준점(말이 되는지 확인하는 값)"],
   ["uniform over V words → PPL = V, perfect model → PPL = 1, PPL < 1 is impossible", "균등이면 V, 완벽하면 1, 1 보다 작을 수는 없어요"],
   ["only comparable across models that share the SAME vocabulary & tokenizer", "같은 어휘와 같은 토크나이저를 쓴 모델끼리만 비교할 수 있어요"]]),
  points("기준점 세 개",
   "모든 단어에 똑같은 확률(균등) → PPL = 어휘 크기 V",
   "정답에 늘 확률 1 → PPL = 1 (가장 낮은 값)",
   "PPL < 1 은 불가능: 확률은 1 을 넘을 수 없으니 1/P ≥ 1"),
  check("완벽한 모델(정답에 늘 확률 1)의 퍼플렉서티는?", ["1", "0", "어휘 크기 V"], 0,
        "1/1 = 1 을 몇 번 곱해도 1 이에요. 그래서 PPL 의 최솟값은 1 이에요."),
 ],
 "pass3": [
  look("슬라이드 짚어 읽기",
   box(225, 195, 985, 225, "모델이 4단어 문장의 실제 정답 단어들에 준 확률"),
   box(300, 262, 1000, 358, "the 1/2, cat 1/4, sat 1/8, down 1/16"),
   box(225, 370, 810, 408, "PPL = (2 x 4 x 8 x 16)^(1/4) = 1024^(1/4) = 2^2.5 ≈ 5.7"),
   box(225, 430, 865, 458, "'평균적으로 약 6개 중 공평하게 찍는 만큼 헷갈려요'"),
   box(85, 488, 1150, 522, "기준점: 균등이면 V, 완벽하면 1, 1 미만은 불가능"),
   box(85, 532, 1125, 565, "주의: 같은 어휘, 같은 토크나이저를 쓴 모델끼리만 비교 가능")),
  steps("손계산: 슬라이드 예제 (역수의 기하 평균)",
   ["정답 확률의 역수: 1/(1/2) = 2, 4, 8, 16",
    "모두 곱하기: 2 x 4 x 8 x 16 = 1024",
    "단어가 4개라 1/4 제곱(네제곱근): 1024^(1/4)",
    "1024 = 2^10 이므로 (2^10)^(1/4) = 2^2.5",
    "2^2.5 = 4 x √2 ≈ 5.66 ≈ 5.7"],
   "PPL ≈ 5.7 → 약 6개 후보 중에서 고르는 정도로 헷갈려요",
   given="the 1/2, cat 1/4, sat 1/8, down 1/16"),
  steps("같은 답을 exp(J) 로 (p.41 식)",
   ["위치마다 벌점 -log P: log 2, log 4, log 8, log 16",
    "합 = log(2 x 4 x 8 x 16) = log 1024 = 10 log 2",
    "평균 J = 10 log 2 ÷ 4 = 2.5 log 2 ≈ 1.733",
    "PPL = exp(1.733) ≈ 5.66"],
   "두 길이 같은 답(≈ 5.7)을 줘요: 로그가 곱을 합으로 바꾸기 때문",
   given="자연로그 사용"),
  prof(MON2,
   "퍼플렉서티는 정답 확률들의 역수를 곱한 다음 단어 수만큼 제곱근을 취하면 된다고 했어요.",
   "5.7 이면 모델이 평균적으로 매 순간 5개나 6개 후보 중에서 토큰을 하나 고르는 정도의 불확실성이라고 했어요.",
   "가장 낮은 값은 1, 퍼플렉서티는 1 보다 작을 수 없고 낮을수록 좋다고 했어요."),
  prof(MON3,
   "퍼플렉서티 비교가 의미 있으려면 같은 평가 데이터, 같은 어휘(vocab), 같은 토크나이저여야 한다고 했어요.",
   "한 모델은 글자 단위, 다른 모델은 서브워드 단위로 자르면 PPL 숫자를 그대로 비교해 '이게 더 나쁘다'고 볼 수 없다고 했어요."),
  points("실습에서 직접 보는 함정 (N3L p.18~26)",
   "N3L p.19: 같은 말뭉치 727,466 글자 → 서브워드 390,136 토큰, 예측 한 번이 평균 1.9 글자",
   "N3L p.25: 글자 모델 PPL 27.48 (글자당), 서브워드 모델 PPL 299.07 (토큰당). 겉보기엔 글자 모델 압승",
   "같은 자로 재면(bits per character) 글자 4.78, 서브워드 4.30 → 오히려 서브워드가 더 좋아요",
   "N3L p.26 교훈: PPL 은 '예측 단위 하나당'이라, 논문의 PPL 을 볼 때 '어떤 단위, 어떤 토크나이저?'부터 물어요"),
  bg("기초 다지기 4단원 (로그와 지수)",
     "2^10 = 1024, 그 네제곱근은 2^(10/4) = 2^2.5 예요. 지수끼리 곱하고 나누면 돼요.",
     "log(a x b) = log a + log b. 그래서 역수의 곱이 벌점의 합으로 바뀌어요."),
 ],
 "pass4": [
  check("정답 확률이 1/2, 1/2 인 2단어 문장의 퍼플렉서티는?", ["2", "4", "1"], 0,
        "역수 2 x 2 = 4, 두 단어라 제곱근 → √4 = 2. 늘 두 후보 중 찍는 만큼 헷갈려요."),
  check("정답 확률이 네 번 모두 1/4 이면 퍼플렉서티는?", ["4", "16", "256"], 0,
        "(4 x 4 x 4 x 4)^(1/4) = 4. 모든 위치 확률이 같으면 PPL 은 그 역수예요."),
  english("답안에 쓸 문장",
   "퍼플렉서티는 1 이상이며(완벽한 모델이면 1, 균등 분포면 어휘 크기 V), 같은 평가 데이터, 같은 어휘, 같은 토크나이저를 쓴 모델끼리만 비교할 수 있다.",
   "기준점 1과 V, 그리고 비교 조건.", "1 ≤ PPL ≤ (균등이면 V), 같은 데이터, 어휘, 토크나이저"),
  warn("헷갈리기 쉬운 점",
   "PPL 은 '예측 단위(토큰) 하나당' 값이에요. 글자 모델의 PPL 27 이 서브워드 모델의 PPL 299 보다 좋다는 뜻이 아니에요(실습 N3L p.25).",
   "(2 x 4 x 8 x 16) 을 4로 나누지 말고 네제곱근을 해요. 산술 평균 (2+4+8+16)/4 = 7.5 는 틀린 답이에요."),
 ]})

# ================= p.43 =================
S.append({"p": 43, "title": "4부 구분: 신경망 언어 모델과 RNN",
 "terms": [EN(k) for k in ["fwlm", "rnn", "hidden", "lm", "ngram"]],
 "pass1": [
  say("4부 **신경망 언어 모델과 RNN** 이 시작돼요. 부제는 '언어 모델에게 기억을 주기'예요.",
      "먼저 " + T("fwlm") + "으로 n-gram 의 벽을 허물고,",
      "다음으로 " + T("rnn") + "이 한 단어씩 읽으며 " + T("hidden") + "(메모장)를 고쳐 써요.",
      "짧은 기억 때문에 생긴 p.38 의 exams 문제를 기억해 두세요."),
  points("4부에서 만날 것",
   T("fwlm") + ": 앞 몇 단어를 " + T("emb") + "으로 바꿔 신경망에 넣기",
   T("rnn") + ": 같은 가중치로 한 단어씩, " + T("hidden") + "에 요약을 이어 적기",
   "RNN 의 약점(기울기 소실)과 그 처방(클리핑, 게이트, 어텐션 예고)"),
 ],
 "pass2": [], "pass3": [], "pass4": []})

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

out = {"deck": "N3", "from": 34, "to": 43, "glossary": glossary, "slides": S}
with open(OUT, "w", encoding="utf-8") as fp:
    json.dump(out, fp, ensure_ascii=False, indent=1)
print("저장:", OUT, "쪽", len(S), "용어", len(glossary))
