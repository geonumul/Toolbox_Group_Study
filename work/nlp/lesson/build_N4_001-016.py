# -*- coding: utf-8 -*-
"""4강(N4) Attention and the Transformer Architecture 회독 레슨 1~16쪽 생성기.
사용: python build_N4_001-016.py   출력: N4_001-016.json
손계산은 아래에서 실제로 계산해 assert 로 확인한다."""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "N4_001-016.json")

# ---------------- 손계산 확인 (assert) ----------------
# p.7 탐색 공간: 어휘 V, 길이 T 이면 후보 문장이 V^T 개
V_, T_ = 32000, 10
assert V_ ** T_ == 1125899906842624000000000000000000000000000000
assert len(str(V_ ** T_)) == 46          # 46자리 수, 즉 10^45 급

# p.10 조건부 언어 모델의 손실: 각 시점 -log P(정답)
probs = [0.5, 0.25, 0.8, 0.1]
Jt = [-math.log(p) for p in probs]
assert [round(v, 3) for v in Jt] == [0.693, 1.386, 0.223, 2.303]
J = sum(Jt) / len(Jt)
assert round(J, 3) == 1.151
# 정답 확률이 1 이면 벌점 0, 0 에 가까우면 벌점이 아주 커요
assert -math.log(1.0) == 0.0 and round(-math.log(0.001), 2) == 6.91

# p.13 빔 서치 점수 (슬라이드 그림의 숫자)
beam = {"he": -0.7, "I": -1.3, "he hit": -1.6, "he struck": -2.3, "I was": -2.9,
        "I got": -3.6, "he hit me": -2.5, "I was hit": -3.5}
assert beam["he"] > beam["I"]                      # t=1 에서 he 가 더 높아요
assert beam["he hit"] > beam["he struck"]          # 같은 가지 안에서 he hit 이 높아요
assert beam["I was"] > beam["I got"]
assert beam["he hit me"] > beam["I was hit"]
# 길이 정규화 예: 짧은 가설과 긴 가설
short_sum, short_len = -2.5, 3
long_sum, long_len = -4.2, 6
assert short_sum > long_sum                                  # 합만 보면 짧은 쪽 승
assert round(short_sum / short_len, 3) == -0.833
assert round(long_sum / long_len, 3) == -0.700
assert long_sum / long_len > short_sum / short_len           # 길이로 나누면 긴 쪽 승

# p.14 BLEU 의 n-gram 정밀도 (슬라이드 예문)
ref = "the cat is on the mat".split()
out = "the cat the cat on the mat".split()


def ngrams(ws, n):
    return [tuple(ws[i:i + n]) for i in range(len(ws) - n + 1)]


def clipped_precision(n):
    from collections import Counter
    c_out, c_ref = Counter(ngrams(out, n)), Counter(ngrams(ref, n))
    hit = sum(min(v, c_ref[g]) for g, v in c_out.items())
    return hit, len(ngrams(out, n))


assert clipped_precision(2) == (3, 6) and round(3 / 6, 2) == 0.50
assert clipped_precision(3) == (1, 5) and round(1 / 5, 2) == 0.20
assert clipped_precision(4) == (0, 4) and 0 / 4 == 0.0
assert clipped_precision(1) == (5, 7) and round(5 / 7, 2) == 0.71   # 슬라이드는 0.86
# 4-gram 정밀도가 0 이면 곱이 0 이라 BLEU 도 0 이에요
assert 0.86 * 0.50 * 0.20 * 0.0 == 0.0
assert len(out) == 7 and len(ref) == 6      # 출력이 더 기니까 간결성 페널티는 안 걸려요

# p.16 정보 병목: 문장 길이가 달라도 벡터 칸 수는 그대로
assert 20 * 0 + 512 == 512 and 200 * 0 + 512 == 512

# p.12 탐욕적 디코딩: 매 순간 가장 큰 것만 고르면 전체 최댓값을 놓칠 수 있어요
step1 = {"he": 0.6, "I": 0.4}
paths = {"he hit": 0.6 * 0.3, "he struck": 0.6 * 0.2, "I was": 0.4 * 0.9, "I got": 0.4 * 0.1}
assert max(step1, key=step1.get) == "he"
assert round(paths["he hit"], 3) == 0.18 and round(paths["I was"], 3) == 0.36
assert max(paths, key=paths.get) == "I was"     # 전체로는 I was 가 더 좋은데 탐욕은 못 골라요

# ---------------- 용어 표기 ----------------
NLP = "**자연어처리(Natural Language Processing (NLP))**"
TOK = "**토큰(Token)**"
VOC = "**어휘(Vocabulary)**"
RNN = "**RNN(순환 신경망)**"
HS = "**은닉 상태(Hidden State)**"
VG = "**기울기 소실(Vanishing Gradient)**"
S2S = "**시퀀스-투-시퀀스 모델(Sequence-to-Sequence Model)**"
ENC = "**인코더(Encoder)**"
DEC = "**디코더(Decoder)**"
MT = "**기계 번역(Machine Translation (MT))**"
NMT = "**신경망 기계 번역(Neural Machine Translation (NMT))**"
LM = "**언어 모델(Language Model (LM))**"
CLM = "**조건부 언어 모델(Conditional Language Model)**"
CE = "**교차 엔트로피(Cross-Entropy)**"
LOSS = "**손실 함수(Loss Function)**"
E2E = "**종단간 학습(End-to-End)**"
TF = "**교사 강요(Teacher Forcing)**"
EB = "**노출 편향(Exposure Bias)**"
INF = "**추론(Inference)**"
GD = "**탐욕적 디코딩(Greedy Decoding)**"
BS = "**빔 서치(Beam Search)**"
BSZ = "**빔 크기(Beam Size)**"
LNORM = "**길이 정규화(Length Normalization)**"
BLEU = "**블루 점수(BLEU)**"
BP = "**간결성 페널티(Brevity Penalty)**"
NG = "**n-gram(엔그램)**"
IB = "**정보 병목(Information Bottleneck)**"
ATT = "**어텐션(Attention)**"
SA = "**셀프 어텐션(Self-Attention)**"
TRF = "**트랜스포머(Transformer)**"
BPG = "**역전파(Backpropagation)**"
PAR = "**병렬화(Parallelization)**"
NTP = "**다음 토큰 예측(Next Token Prediction)**"
LLM = "**LLM(대규모 언어 모델)**"
GRAD = "**기울기(Gradient)**"
BPTT = "**시간 역전파(Backpropagation Through Time (BPTT))**"

MANTRA = "글을 토큰으로 자르고, 토큰을 벡터로 바꾸고, 벡터로 다음 토큰을 맞혀요."
WHEN = "4주차 월요일 1교시"

GLOSSARY = [
    ("자연어처리", "Natural Language Processing (NLP)", "컴퓨터가 사람의 말과 글을 다루게 하는 분야",
     "글을 토큰으로 자르고, 벡터로 바꾸고, 그 벡터로 다음 토큰을 맞혀요."),
    ("토큰", "Token", "글을 자른 레고 조각 하나",
     "모델이 읽는 가장 작은 단위예요. 단어일 수도, 단어의 조각(서브워드)일 수도 있어요."),
    ("어휘", "Vocabulary", "모델이 아는 토큰 종류의 목록",
     "어휘 크기를 V 라고 써요. 매 자리마다 V 개 후보 중 하나를 고르는 셈이에요."),
    ("순환 신경망", "Recurrent Neural Network (RNN)", "한 단어씩 읽으며 메모장에 요약을 고쳐 쓰는 신경망",
     "3주차에 배웠어요. 시점마다 같은 가중치를 다시 써서 은닉 상태를 갱신해요."),
    ("은닉 상태", "Hidden State", "지금까지 읽은 내용을 요약해 들고 다니는 숫자 벡터, 곧 메모장",
     "RNN 이 한 토큰을 읽을 때마다 새로 계산해요. 기호는 h 로 써요."),
    ("기울기 소실", "Vanishing Gradient", "귓속말 전달 게임처럼 기울기가 점점 희미해져 0 에 가까워지는 문제",
     "RNN 에서 먼 과거까지 학습 신호가 잘 가지 않는 이유예요. 어텐션이 이 문제를 비켜 가요."),
    ("시간 역전파", "Backpropagation Through Time (BPTT)", "시점마다 펼친 RNN 위에서 뒤에서 앞으로 역전파하기",
     "먼 과거로 갈수록 곱셈이 여러 번 쌓여서 기울기가 작아지거나 커져요."),
    ("시퀀스-투-시퀀스 모델", "Sequence-to-Sequence Model", "줄줄이 들어온 것을 읽고 줄줄이 내놓는 모델 틀",
     "인코더와 디코더 두 부분으로 되어 있어요. 번역, 요약, 대화, 음성 인식에 모두 써요."),
    ("인코더", "Encoder", "입력 문장을 끝까지 읽어 요약을 만드는 쪽",
     "2014년 원래 구조에서는 인코더가 RNN 이었고, 마지막 은닉 상태가 요약 벡터였어요."),
    ("디코더", "Decoder", "요약을 받아 답 문장을 한 토큰씩 만들어 내는 쪽",
     "디코더는 입력에 조건이 걸린 언어 모델이에요. 그래서 조건부 언어 모델이라고 불러요."),
    ("기계 번역", "Machine Translation (MT)", "한 언어 문장을 다른 언어 문장으로 바꾸는 과제",
     "4주차 내내 예제로 쓰는 과제예요. 입력 x 를 보고 출력 y 를 만들어요."),
    ("신경망 기계 번역", "Neural Machine Translation (NMT)", "신경망 하나로 통째로 학습하는 번역 방식",
     "2014년에 등장했어요. 2년 만에 수백 명이 십 년간 만든 통계 기반 시스템을 앞질렀어요."),
    ("언어 모델", "Language Model (LM)", "휴대폰 자판의 다음 단어 추천처럼 다음 토큰을 맞히는 모델",
     "3주차에 배웠어요. 문장의 확률을 조각조각 곱으로 나눠 써요."),
    ("조건부 언어 모델", "Conditional Language Model", "입력 문장 x 를 조건으로 붙인 언어 모델",
     "P(y|x) = P(y1|x) P(y2|y1, x) ... 처럼 매 자리마다 x 가 조건으로 계속 붙어요."),
    ("다음 토큰 예측", "Next Token Prediction", "지금까지의 토큰으로 바로 다음 토큰을 맞히는 과제",
     "교수님: 지금까지 토큰으로 다음 토큰을 예측하는 이것이 거의 모든 걸 결정해요."),
    ("교차 엔트로피", "Cross-Entropy", "정답 토큰에 준 확률의 -log 를 벌점으로 매기는 손실",
     "정답 확률이 1 이면 벌점 0, 0 에 가까우면 벌점이 아주 커져요."),
    ("손실 함수", "Loss Function", "틀린 정도를 매기는 벌점",
     "학습은 이 벌점이 작아지는 쪽으로 파라미터를 조금씩 고치는 일이에요."),
    ("종단간 학습", "End-to-End", "여러 부품을 따로 만들지 않고 하나의 신경망을 한 번에 학습하는 방식",
     "손실 하나를 정하고 역전파 한 번으로 디코더, 다리, 인코더까지 전부 고쳐요."),
    ("역전파", "Backpropagation", "틀린 책임을 뒤에서 앞으로 나눠 주기",
     "3주차 주제였어요. 손실의 기울기를 출력 쪽에서 입력 쪽으로 연쇄 법칙으로 계산해요."),
    ("교사 강요", "Teacher Forcing", "학습할 때 모델의 예측 대신 정답 단어를 다음 입력으로 넣어 주기",
     "선생님이 정답을 옆에서 알려 주는 셈이에요. 학습이 안정되고 시점끼리 병렬로 돌아가요."),
    ("노출 편향", "Exposure Bias", "학습 때는 정답을 보고, 시험 때는 자기 출력만 보는 데서 오는 어긋남",
     "교사 강요의 부작용이에요. 학습 환경과 실제 생성 환경이 달라서 생겨요."),
    ("추론", "Inference", "학습이 끝난 모델로 실제로 답을 만들어 보는 일",
     "이때는 정답을 모르니까 모델이 직전에 만든 토큰을 다음 입력으로 넣어요."),
    ("탐욕적 디코딩", "Greedy Decoding", "매 순간 확률이 가장 높은 토큰 하나만 고르기",
     "빠르고 단순하지만 한 번 잘못 고르면 되돌릴 수 없어요."),
    ("빔 서치", "Beam Search", "매 단계에서 좋은 후보 k 개를 남겨 두고 함께 넓히기",
     "탐욕의 단점을 줄여요. 전부 탐색하지는 않지만 꽤 좋은 근사예요."),
    ("빔 크기", "Beam Size", "빔 서치가 남겨 두는 후보 개수 k",
     "보통 5에서 10 을 써요. k = 1 이면 탐욕적 디코딩과 같아요."),
    ("길이 정규화", "Length Normalization", "끝난 후보들의 점수를 길이로 나눠서 비교하기",
     "로그 확률을 더하면 길수록 점수가 낮아져서, 나누지 않으면 짧은 문장만 뽑혀요."),
    ("블루 점수", "BLEU", "사람이 쓴 정답 문장과 n-gram 이 얼마나 겹치는지로 매기는 번역 점수",
     "1에서 4까지의 n-gram 정밀도를 곱하고, 너무 짧은 번역에는 페널티를 줘요."),
    ("간결성 페널티", "Brevity Penalty", "번역이 정답보다 너무 짧으면 점수를 깎는 항",
     "짧게 말해서 정밀도만 올리는 꼼수를 막아요."),
    ("엔그램", "n-gram", "바로 붙어 있는 토큰 n개 묶음",
     "2개면 bigram, 3개면 trigram 이에요. BLEU 는 1에서 4까지를 봐요."),
    ("정보 병목", "Information Bottleneck", "입력 전체가 고정 크기 벡터 하나를 지나가야 해서 생기는 막힘",
     "20단어 문장이든 200단어 문단이든 같은 칸 수의 벡터에 욱여넣어야 해요."),
    ("어텐션", "Attention", "필요한 곳을 골라 보는 장치. 점수를 매기고 가중 평균을 내요",
     "2015년에 나왔어요. 디코더가 매 단계마다 입력의 모든 자리를 다시 봐요."),
    ("셀프 어텐션", "Self-Attention", "한 문장이 자기 자신을 바라보는 어텐션",
     "2017년 트랜스포머의 핵심이에요. RNN 을 아예 빼 버려요."),
    ("트랜스포머", "Transformer", "어텐션만으로 만든 요즘 언어 모델의 기본 블록",
     "교수님: 이 트랜스포머를 좀 크게 쌓으면 그게 LLM 이에요."),
    ("대규모 언어 모델", "Large Language Model (LLM)", "트랜스포머 블록을 아주 많이 쌓아 크게 학습한 언어 모델",
     "ChatGPT 같은 모델이에요. 비전 트랜스포머까지 대부분 이 구조 위에 있어요."),
    ("병렬화", "Parallelization", "여러 계산을 한꺼번에 동시에 하기",
     "GPU 는 큰 행렬 곱을 한 번에 잘해요. 교수님: 패러럴이 핵심이에요."),
    ("기울기", "Gradient", "손실이 가장 빨리 커지는 방향과 그 가파름",
     "학습은 기울기의 반대 방향으로 한 걸음씩 내려가요."),
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
FIG_TODAY = SVG(
    TX(240, 26, "오늘 가는 길", "tb", 16),
    BOX(8, 50, 104, 40, "RNN 의 한계", "box", "tb", 1, 13),
    TX(60, 108, "1 먼 거리", "tm", 12, "middle", 1), TX(60, 126, "2 순차 계산", "tm", 12, "middle", 1),
    TX(60, 144, "3 정보 병목", "tm", 12, "middle", 1),
    A(114, 70, 144, 70, "e2", 2),
    BOX(146, 50, 104, 40, "어텐션 2015", "box2", "tb", 2, 13),
    TX(198, 108, "입력을 다시", "tm", 12, "middle", 2), TX(198, 126, "직접 본다", "tm", 12, "middle", 2),
    A(252, 70, 282, 70, "e2", 3),
    BOX(284, 50, 104, 40, "셀프 어텐션 2017", "box2", "tb", 3, 12),
    TX(336, 108, "RNN 을 뺀다", "tm", 12, "middle", 3), TX(336, 126, "병렬로 계산", "tm", 12, "middle", 3),
    A(390, 70, 420, 70, "e2", 4),
    BOX(392, 50, 80, 40, "트랜스포머", "box2", "tb", 4, 13),
    TX(432, 108, "= LLM 의", "tm", 12, "middle", 4), TX(432, 126, "기본 블록", "tm", 12, "middle", 4),
    L(10, 176, 470, 176, "e", 4),
    TX(240, 200, "문제 → 해결 → 새 문제 → 해결 의 순서예요", "t", 14, "middle", 4),
    TX(240, 226, "주문: " + "글을 토큰으로 자르고, 벡터로 바꾸고, 다음 토큰을 맞혀요", "tm", 12, "middle", 4),
)

FIG_ENCDEC = SVG(
    TX(240, 24, "RNN 두 개를 벡터 하나로 붙인 것", "tb", 15),
    R(14, 60, 46, 34, "n", 1), R(64, 60, 46, 34, "n", 1), R(114, 60, 46, 34, "n", 1), R(164, 60, 46, 34, "n", 1),
    TX(37, 82, "il", "tl", 12, "middle", 1), TX(87, 82, "a", "tl", 12, "middle", 1),
    TX(137, 82, "m'", "tl", 12, "middle", 1), TX(187, 82, "entarte", "tl", 11, "middle", 1),
    L(60, 77, 64, 77, "e", 1), L(110, 77, 114, 77, "e", 1), L(160, 77, 164, 77, "e", 1),
    TX(112, 116, "인코더 RNN: 왼쪽부터 한 단어씩 읽어요", "tm", 12, "middle", 1),
    A(212, 77, 250, 77, "e2", 2),
    TX(231, 60, "encoding", "tb", 12, "middle", 2),
    R(254, 60, 46, 34, "n2", 3), R(304, 60, 46, 34, "n2", 3), R(354, 60, 46, 34, "n2", 3), R(404, 60, 46, 34, "n2", 3),
    TX(277, 82, "he", "tl", 12, "middle", 3), TX(327, 82, "hit", "tl", 12, "middle", 3),
    TX(377, 82, "me", "tl", 12, "middle", 3), TX(427, 82, "...", "tl", 12, "middle", 3),
    L(300, 77, 304, 77, "e", 3), L(350, 77, 354, 77, "e", 3), L(400, 77, 404, 77, "e", 3),
    TX(352, 116, "디코더 RNN: 한 토큰씩 만들어요", "tm", 12, "middle", 3),
    R(200, 150, 80, 30, "n4", 4), TX(240, 170, "벡터 하나", "tl", 13, "middle", 4),
    TX(240, 202, "입력의 모든 정보가 이 칸을 지나가야 해요", "t", 13, "middle", 4),
    TX(240, 226, "여기가 정보 병목(Information Bottleneck)", "tb", 13, "middle", 4),
)

FIG_GREEDY = SVG(
    TX(240, 24, "탐욕은 되돌릴 수 없어요", "tb", 15),
    BOX(20, 54, 70, 32, "he 0.6", "box2", "tb", 1, 13),
    BOX(20, 104, 70, 32, "I 0.4", "box", "tm", 1, 13),
    A(92, 70, 128, 60, "e2", 2), A(92, 70, 128, 108, "e", 2),
    BOX(130, 44, 80, 32, "hit 0.3", "box", "tm", 2, 12),
    BOX(130, 92, 80, 32, "struck 0.2", "box", "tm", 2, 12),
    A(92, 120, 128, 156, "e", 3), A(92, 120, 128, 196, "e", 3),
    BOX(130, 140, 80, 32, "was 0.9", "box2", "tb", 3, 12),
    BOX(130, 188, 80, 32, "got 0.1", "box", "tm", 3, 12),
    TX(300, 60, "he hit = 0.6 x 0.3 = 0.18", "t", 13, "middle", 4),
    TX(300, 86, "I was  = 0.4 x 0.9 = 0.36", "tb", 13, "middle", 4),
    TX(300, 130, "탐욕은 첫 칸에서 he 를 골라", "tm", 12, "middle", 4),
    TX(300, 150, "I was 로 가는 길을 아예 잃어요", "tm", 12, "middle", 4),
    TX(300, 186, "빔 서치는 he 와 I 를", "t", 13, "middle", 5),
    TX(300, 206, "둘 다 들고 가요", "t", 13, "middle", 5),
)

FIG_BOTTLE = SVG(
    TX(240, 24, "문장이 길어도 통로는 그대로", "tb", 15),
    R(20, 50, 130, 26, "n", 1), TX(85, 68, "20단어 문장", "tl", 12, "middle", 1),
    R(20, 140, 200, 26, "n", 2), TX(120, 158, "200단어 문단", "tl", 12, "middle", 2),
    A(152, 63, 236, 100, "e2", 3), A(222, 153, 236, 110, "e2", 3),
    R(238, 88, 60, 30, "n4", 3), TX(268, 108, "512칸", "tl", 12, "middle", 3),
    A(300, 103, 340, 103, "e2", 4),
    R(342, 82, 120, 42, "box2", 4), TX(402, 108, "디코더", "tb", 14, "middle", 4),
    TX(240, 196, "칸 수가 같으니 긴 문장일수록 더 많이 버려요", "t", 13, "middle", 4),
    TX(240, 222, "성능이 문장 길이에 따라 무너지는 이유예요", "tm", 12, "middle", 4),
)

S = []


def page(p, title, terms, p1, p2=(), p3=(), p4=()):
    S.append({"p": p, "title": title, "terms": list(terms),
              "pass1": list(p1), "pass2": list(p2), "pass3": list(p3), "pass4": list(p4)})


# ---------------------------------------------------------------- p.1
page(1, "표지: 4주차 Attention and the Transformer Architecture", ["Attention", "Transformer"],
     [say("4주차 강의 표지예요. 제목은 Week 4. Attention and the Transformer Architecture 예요.",
          f"우리말로 '{ATT}과 {TRF} 구조' 라는 뜻이에요.",
          "오늘 배우는 것이 요즘 인공지능의 뼈대예요.")],
     [], [],
     [])

# ---------------------------------------------------------------- p.2
page(2, "Reminder: 자료 배포 금지 안내", [],
     [say("매주 나오는 안내 쪽이에요. 강의 자료에 저작권이 있으니 밖에 배포하지 말라는 뜻이에요.",
          "화면이나 소리에 문제가 있으면 바로 알려 달라는 내용도 있어요.")],
     [], [], [])

# ---------------------------------------------------------------- p.3
page(3, "Contents: 오늘의 네 부분", ["Sequence-to-Sequence Model", "Attention", "Self-Attention", "Transformer"],
     [say("오늘 수업은 네 부분이에요. 앞부분이 다음 부분의 문제를 만들어 주는 순서예요."),
      points("네 부분을 한 줄씩",
             f"1. Sequence-to-Sequence and its Bottleneck = {S2S}과 그 병목",
             f"2. Attention = {ATT}. 오늘의 메인이에요",
             f"3. Self-Attention = {SA}. RNN 을 아예 빼요",
             f"4. The Transformer = {TRF}. 진짜 블록을 조립해요")],
     [compare("영어 제목과 우리말 뜻",
              ["영어", "우리말"],
              ["Sequence-to-Sequence", "줄줄이 들어와 줄줄이 나가는 구조"],
              ["Bottleneck", "병목, 좁은 통로"],
              ["Attention", "주목하기, 어디를 볼지 정하기"],
              ["Self-Attention", "자기 자신에게 주목하기"])],
     [prof("교수님: 오늘 수업이 끝날 때면 여러분이 트랜스포머를 이해하고, 라지 랭귀지 모델이 어떻게 되는지 알아볼 수 있게 될 거예요.",
           f"교수님: 사실상 이 {TRF}를 좀 크게 쌓으면 그게 {LLM}이다, 이렇게 보셔도 돼요.")],
     [])

# ---------------------------------------------------------------- p.4
page(4, "지난주 복습과 오늘 할 일", ["Recurrent Neural Network (RNN)", "Vanishing Gradient", "Attention", "Self-Attention", "Parallelization"],
     [say(f"지난주에 신경망, {BPG}, {LM}, 그리고 {RNN}까지 배웠어요.",
          f"멈춰 선 자리는 {VG}이었어요. {RNN}은 먼 거리 정보를 나르지 못하고, 병렬 계산도 안 돼요.",
          f"오늘은 그걸 정확히 고치는 두 아이디어, {ATT}(2015)과 {SA}(2017)을 배워요."),
      figure("오늘 가는 길", FIG_TODAY, "문제가 생기면 부품을 하나 더하는 식으로 트랜스포머까지 가요.", 4)],
     [compare("슬라이드 영어와 우리말 뜻",
              ["영어 원문", "뜻"],
              ["Last week: neural networks, backpropagation, language modeling, RNNs", "지난주에 배운 네 가지"],
              ["Where we stopped: vanishing gradients", f"멈춘 자리는 {VG}"],
              ["an RNN cannot carry information across a long distance", "RNN 은 먼 거리로 정보를 못 나른다"],
              ["and it cannot be parallelised", f"그리고 {PAR}도 안 된다"],
              ["By the end: you should be able to draw the Transformer block from memory",
               "수업이 끝나면 트랜스포머 블록을 외워서 그릴 수 있어야 한다"]),
      points("맨 아래 한 줄의 뜻",
             "From 'read it all, then speak' to 'look back at every word, every step'",
             "'다 읽고 나서 말하기' 에서 '매 단계마다 모든 단어를 다시 보기' 로 바뀐다는 뜻이에요.",
             f"이게 {ATT}의 한 줄 요약이에요.")],
     [look("슬라이드를 짚어 읽어요",
           (0.05, 0.19, 0.90, 0.07, "Last week 줄: 지난주에 배운 네 가지를 늘어놨어요."),
           (0.05, 0.26, 0.90, 0.09, f"Where we stopped 줄: {VG} 때문에 멈췄다는 뜻이에요."),
           (0.05, 0.36, 0.90, 0.07, f"Today 줄: 오늘 배울 두 아이디어가 {ATT}(2015)과 {SA}(2017)이에요."),
           (0.05, 0.43, 0.90, 0.07, "By the end 줄: 트랜스포머 블록을 외워서 그릴 수 있어야 한다는 목표예요."),
           (0.05, 0.50, 0.90, 0.07, "Also today 줄: 팀 프로젝트 안내. 4인 1조, 자유 주제, 다음 주까지 팀을 알려 달라는 뜻이에요.")),
      prof("교수님: RNN 은 이전 정보를 은닉 상태에 담아 전달하지만, 시퀀스가 길어질수록 먼 거리 정보를 전달하기 어려워요.",
           f"교수님: 두 번째는 계산을 순서대로 해야 한다는 거예요. t 번째를 계산하려면 t-1 이 먼저 끝나야 해요.",
           "교수님: 컴퓨터 사이언스를 하시는 분들은 순차 계산을 늘 경계하고, 병렬 파이프라인을 머릿속에 그려 주세요."),
      bg("기초 다지기 7단원", f"{VG}은 1보다 작은 수를 여러 번 곱하는 것과 같아요. 0.5를 열 번 곱하면 0.001 이 돼요.",
         f"그래서 {BPTT}로 먼 과거까지 거슬러 갈수록 학습 신호가 거의 사라져요.")],
     [check("오늘 배우는 두 아이디어가 고치려는 RNN 의 약점 두 가지는?",
            ["먼 거리 정보 전달과 순차 계산", "어휘 크기와 토큰화", "과적합과 정규화", "학습률과 배치 크기"], 0,
            f"슬라이드가 vanishing gradients 와 cannot be parallelised 라고 적었어요. {VG}과 {PAR} 불가예요."),
      english("답안 문장",
              f"{RNN}은 먼 거리 의존을 다루기 어렵고 순차 계산이라 병렬화가 안 되는데, {ATT}과 {SA}이 이 두 약점을 각각 해결한다.",
              "어텐션은 먼 거리를 직접 잇고, 셀프 어텐션은 순서를 없애 병렬 계산을 가능하게 해요.",
              "'먼 거리 + 병렬' 두 단어만 기억하면 4주차 전체가 따라와요."),
      warn("헷갈리기 쉬운 점",
           f"{ATT}은 2015년, {SA}(트랜스포머)은 2017년이에요. 두 해를 바꿔 쓰지 않아요.")])

# ---------------------------------------------------------------- p.5
page(5, "Part 1 구분 슬라이드: Sequence-to-Sequence and its Bottleneck",
     ["Sequence-to-Sequence Model", "Machine Translation (MT)", "Encoder", "Decoder"],
     [say(f"Part 1 이 시작돼요. 제목은 {S2S}과 그 병목이에요.",
          f"부제 'machine translation, the encoder-decoder, how to decode' 는 {MT}, {ENC}와 {DEC}, 그리고 디코딩 방법이라는 뜻이에요.")],
     [], [], [])

# ---------------------------------------------------------------- p.6
page(6, "지난주에 멈춘 자리: RNN 의 세 가지 문제", ["Recurrent Neural Network (RNN)", "Hidden State", "Vanishing Gradient", "Information Bottleneck", "Parallelization"],
     [say(f"{RNN}은 줄줄이 들어온 것을 한 걸음씩 읽으며 {HS}에 요약을 들고 다녀요.",
          "여기에는 못 풀었던 문제가 둘, 그리고 오늘 새로 보는 문제가 하나 더 있어요."),
      points("문제 세 가지를 아주 쉽게",
             "1. 멀리 있는 단어끼리 서로 닿기 어려워요",
             "2. 앞 계산이 끝나야 뒤 계산을 할 수 있어요",
             "3. 입력 전체가 벡터 하나에 다 들어가야 해요")],
     [compare("슬라이드 영어와 우리말 뜻",
              ["영어 원문", "뜻"],
              ["Long-range dependency + Vanishing Gradients", f"먼 거리 의존과 {VG}"],
              ["Sequential Calculation", "순차 계산, 앞에서 뒤로 한 칸씩"],
              ["NEW Information Bottleneck", f"새 문제인 {IB}"],
              ["All information from the input sequence must fit into ONE vector",
               "입력의 모든 정보가 벡터 하나에 들어가야 한다"]),
      points("세 문제와 오늘의 처방",
             f"먼 거리 문제 → {ATT}이 입력의 모든 자리를 직접 이어 줘요",
             f"순차 계산 문제 → {SA}이 한꺼번에 계산하게 해 줘요({PAR})",
             f"{IB} → {ATT}이 매 단계마다 새 요약을 만들어 줘요")],
     [look("슬라이드를 짚어 읽어요",
           (0.05, 0.19, 0.90, 0.06, "첫 줄: RNN 은 한 스텝씩 읽고 은닉 상태를 들고 다닌다는 복습이에요."),
           (0.05, 0.28, 0.90, 0.09, "(1) 먼 거리 의존과 기울기 소실. 지난주에 배운 문제예요."),
           (0.05, 0.40, 0.90, 0.06, "(2) 순차 계산. 이것도 지난주 문제예요."),
           (0.05, 0.47, 0.90, 0.08, "(3) NEW 표시가 붙은 정보 병목. 오늘 새로 보는 문제예요."),
           (0.05, 0.60, 0.90, 0.07, "맨 아래: 오늘의 두 아이디어가 정확히 이 셋을 겨냥한다는 안내예요.")),
      prof("교수님: t 번째 은닉 상태를 계산하려면 t-1 번째가 필요해서, 하나씩 처리해야 하는 순차 계산 자체가 좋지 않아요.",
           f"교수님: 인코더에서 긴 영어 문장을 다 읽은 다음 한국어 첫 토큰을 시작하는데, 그 모든 정보가 {HS} 하나에 담겨야 해요.")],
     [check("슬라이드가 NEW 라고 표시한 새 문제는?",
            ["정보 병목", "기울기 소실", "순차 계산", "과적합"], 0,
            f"(3) 에 NEW 가 붙어 있어요. 입력 전체가 벡터 하나에 들어가야 하는 {IB}이에요."),
      warn("헷갈리기 쉬운 점",
           f"{VG}과 {IB}은 다른 문제예요. 앞은 학습 신호가 사라지는 문제, 뒤는 정보를 담을 칸이 모자라는 문제예요.")])

# ---------------------------------------------------------------- p.7
page(7, "오늘의 과제: 기계 번역", ["Machine Translation (MT)", "Vocabulary", "Token", "Language Model (LM)"],
     [say(f"오늘 계속 쓸 예제 과제는 {MT}이에요.",
          "입력 문장 x 를 보고, 다른 언어의 출력 문장 y 를 만드는 일이에요."),
      analogy("번역은 두 가지 일을 동시에 해요",
              "아주 넓은 도서관에서 '가장 좋은 답 문장' 을 찾는 일이에요. 좋은지 판단하는 눈도 있어야 하고, 넓은 서가를 뒤지는 발도 있어야 해요.",
              ("좋은 답인지 판단하는 눈", f"확률 모델 P(y|x), 곧 {LM}"),
              ("넓은 서가를 뒤지는 발", "탐색(search), 곧 디코딩 방법"),
              ("서가가 끝없이 넓다", "가능한 y 가 사실상 무한히 많다"))],
     [compare("슬라이드 영어와 우리말 뜻",
              ["영어 원문", "뜻"],
              ["given a source sentence x, produce a target sentence y", "원문 x 가 주어지면 목표 문장 y 를 만든다"],
              ["Formally we want argmax P(y|x)", "식으로는 P(y|x) 를 가장 크게 하는 y 를 찾는다"],
              ["the space of possible y is infinite", "가능한 y 의 공간이 사실상 무한하다"],
              ["so we will have to search it", "그래서 탐색을 해야 한다"]),
      points("argmax 라는 기호",
             "argmax 는 '가장 큰 값을 주는 것' 을 뜻해요. max 는 값 자체, argmax 는 그 값을 만든 후보예요.",
             "argmax P(y|x) 는 확률이 가장 높은 문장 y 를 고른다는 말이에요.")],
     [steps("후보 문장이 얼마나 많을까요",
            [f"{VOC} 크기 V = 32,000 이라고 해요(요즘 모델에서 흔한 크기예요)",
             f"길이가 딱 10개 {TOK}이라고 못 박아도, 자리마다 32,000 가지예요",
             "후보 수 = 32,000을 10번 곱한 수 = 32,000^10",
             "이 수는 46자리 수예요. 10의 45제곱 정도예요",
             "게다가 길이도 정해져 있지 않으니 진짜 후보는 더 많아요"],
            "그래서 전부 확인하는 것은 불가능하고, 똑똑한 탐색(디코딩)이 필요해요."),
      prof("교수님: y 의 공간이 사실상 거의 무한해요. 길이도 정해져 있지 않고, 자리마다 어휘 수만큼 후보가 있으니까요.",
           "교수님: 그래서 좋은 확률 모델을 만드는 문제이면서, 동시에 거대한 탐색 공간에서 좋은 문장을 찾는 탐색 문제이기도 해요."),
      bg("기초 다지기 5단원", "P(y|x) 는 'x 가 주어졌을 때 y 가 나올 확률' 이라고 읽어요. 세로줄은 '주어졌을 때' 예요.")],
     [check("argmax P(y|x) 가 뜻하는 것은?",
            ["확률이 가장 높은 문장 y 를 고르기", "확률의 최댓값 자체", "x 의 확률을 구하기", "y 의 길이를 정하기"], 0,
            "argmax 는 값이 아니라 그 값을 만드는 후보를 가리켜요."),
      english("답안 문장",
              f"{MT}은 P(y|x) 를 최대로 하는 목표 문장 y 를 찾는 문제이고, 후보 문장 공간이 사실상 무한해서 좋은 확률 모델과 효율적인 탐색이 함께 필요하다.",
              "모델(판단)과 디코딩(탐색) 두 축으로 나눠 적으면 점수가 잘 나와요.")])

# ---------------------------------------------------------------- p.8
page(8, "번역의 역사: 규칙에서 통계로, 다시 신경망으로", ["Machine Translation (MT)", "Neural Machine Translation (NMT)", "BLEU"],
     [say("번역의 역사는 자연어처리 전체의 역사와 모양이 같아요.",
          "사람이 규칙을 적던 시대에서, 말뭉치 통계를 세던 시대로, 다시 신경망 하나로 통째로 배우는 시대로 왔어요."),
      compare("세 시대",
              ["시기", "방식", "한 줄 설명"],
              ["1950s-80s", "규칙 기반", "사람이 문법 규칙과 이중 언어 사전을 직접 만들었어요"],
              ["1990s-2010s", "통계 기반(SMT)", "말뭉치에서 P(x|y) 와 P(y) 를 세어 배웠어요"],
              ["2014-", f"{NMT}", "신경망 하나를 종단간으로 학습해요"])],
     [points("슬라이드 영어에서 꼭 아는 단어",
             "hand-written rules = 사람이 손으로 쓴 규칙",
             "bilingual dictionaries = 두 언어 사전",
             "parallel corpora = 같은 뜻의 두 언어 문장 쌍 말뭉치",
             "phrase tables, reranking, feature engineering = 통계 번역이 따로따로 만들던 부품들",
             "trained end-to-end = 처음부터 끝까지 한 번에 학습"),
      points("한 줄 교훈",
             "슬라이드 맨 아래: replace a pipeline with one learned model",
             "여러 부품을 이어 붙인 파이프라인을 학습된 모델 하나로 바꾼다는 뜻이에요.",
             "2주차 word2vec, 3주차 신경망에서도 나온 같은 이야기예요.")],
     [look("슬라이드를 짚어 읽어요",
           (0.05, 0.19, 0.90, 0.06, "1950s-80s: 규칙과 사전의 시대예요."),
           (0.05, 0.26, 0.90, 0.10, "1990s-2010s: 통계 기반. 정렬 모델, 구문 표, 재순위화 같은 부품이 따로따로 있었어요."),
           (0.05, 0.38, 0.90, 0.10, "2014-: 신경망 기계 번역. 2년 만에 수백 명이 십 년간 만든 시스템을 앞질렀어요."),
           (0.05, 0.86, 0.90, 0.06, "맨 아래 한 줄: 파이프라인을 학습된 모델 하나로 바꾼다.")),
      prof("교수님: 규칙 기반의 가장 큰 단점은 예외가 생겼을 때 아주 취약하다는 거예요.",
           "교수님: 구글도 네이버 파파고도 원래 통계 기반이었는데, 2015~2016년쯤 신경망 방식으로 바꿨어요.",
           f"교수님: 그래프의 세로축 점수가 {BLEU}인데, 높으면 번역이 잘 된 거라고 보면 돼요(뒤에서 다시 설명해요).")],
     [check("슬라이드가 말하는 '계속 반복되는 교훈' 은?",
            ["파이프라인을 학습된 모델 하나로 바꾼다", "규칙을 더 정교하게 쓴다", "사전을 더 크게 만든다", "말뭉치를 줄인다"], 0,
            "replace a pipeline with one learned model 이 맨 아래 한 줄이에요."),
      warn("헷갈리기 쉬운 점",
           f"{NMT}이 등장한 해는 2014년, 어텐션은 2015년, 트랜스포머는 2017년이에요. 세 해가 자주 섞여요.")])

# ---------------------------------------------------------------- p.9
page(9, "인코더 디코더 구조", ["Encoder", "Decoder", "Recurrent Neural Network (RNN)", "Hidden State", "Sequence-to-Sequence Model"],
     [say(f"{S2S}의 기본 모양이에요. {RNN} 두 개를 벡터 하나로 붙였어요.",
          f"{ENC}는 입력을 끝까지 읽어 요약을 만들고, {DEC}는 그 요약을 받아 답을 한 토큰씩 만들어요."),
      figure("인코더와 디코더", FIG_ENCDEC, "왼쪽이 인코더, 오른쪽이 디코더, 가운데 파란 화살표가 요약 벡터예요.", 4),
      analogy("통역사 두 명",
              "첫 번째 사람이 프랑스어 문장을 끝까지 다 듣고 쪽지 한 장에 요약을 적어 건네요. 두 번째 사람은 그 쪽지만 보고 영어로 말해요.",
              ("끝까지 듣는 사람", ENC),
              ("쪽지 한 장", "요약 벡터(encoding)"),
              ("쪽지만 보고 말하는 사람", DEC))],
     [compare("슬라이드 영어와 우리말 뜻",
              ["영어 원문", "뜻"],
              ["Two RNNs", "RNN 두 개"],
              ["The encoder reads the source and compresses it into a vector", "인코더가 원문을 읽어 벡터 하나로 압축한다"],
              ["The decoder is a language model that generates the target", "디코더는 목표 문장을 만드는 언어 모델이다"],
              ["conditioned on that vector", "그 벡터를 조건으로 하여"]),
      points("그림 속 낱말",
             "source sentence (input) = 원문, 곧 입력 문장",
             "target sentence (output) = 목표 문장, 곧 출력 문장",
             "encoding = 인코더의 마지막 은닉 상태, 곧 요약 벡터",
             "<s> = 문장 시작을 알리는 특별한 토큰이에요")],
     [look("슬라이드를 짚어 읽어요",
           (0.05, 0.19, 0.90, 0.09, "위쪽 두 줄: 인코더는 읽어서 압축하고, 디코더는 그 벡터를 조건으로 생성한다는 설명이에요."),
           (0.06, 0.50, 0.32, 0.22, "왼쪽 주황 상자들: 인코더 RNN. il a m' entarte 를 한 단어씩 읽어요."),
           (0.33, 0.53, 0.09, 0.10, "파란 화살표와 encoding 글자: 여기서 요약 벡터가 디코더로 넘어가요."),
           (0.41, 0.38, 0.52, 0.35, "오른쪽 초록 상자들: 디코더 RNN. <s> 부터 시작해 he hit me with a pie 를 만들어요.")),
      prof("교수님: 핵심은 RNN 2개를 왼쪽과 오른쪽에 연결한다는 거예요. 왼쪽이 인코더, 오른쪽이 디코더예요.",
           "교수님: 이 벡터 하나가 굉장히 중요한 정보를 담고 있겠죠. 모든 원문 정보를 다 담고 있어야 해요.",
           "교수님: 번역의 특징은 문장을 전부 다 입력받은 다음에 번역을 시작한다는 거예요."),
      points("슬라이드 맨 아래 출처",
             "Sutskever et al. 2014, Cho et al. 2014 가 이 구조를 제안한 논문이에요.",
             "'two RNNs, glued at one vector' 는 'RNN 두 개를 벡터 하나로 붙였다' 는 뜻이에요.")],
     [check("인코더의 출력이 디코더로 넘어가는 통로는?",
            ["마지막 은닉 상태 벡터 하나", "입력 문장 전체", "어휘 목록", "손실 함수"], 0,
            f"그림의 encoding 이 인코더의 마지막 {HS}이고, 이것이 유일한 통로예요. 여기가 나중에 병목이 돼요."),
      english("답안 문장",
              f"{S2S}은 {ENC} RNN 이 입력 문장을 읽어 고정 크기 벡터 하나로 압축한다. {DEC} RNN 은 그 벡터를 조건으로 목표 문장을 한 토큰씩 생성한다.",
              "'두 RNN + 벡터 하나' 라는 뼈대를 먼저 쓰고 세부를 붙여요.")])

# ---------------------------------------------------------------- p.10
page(10, "디코더는 조건부 언어 모델", ["Conditional Language Model", "Language Model (LM)", "Cross-Entropy", "Loss Function", "End-to-End", "Backpropagation"],
     [say(f"{DEC}는 그냥 {LM}인데, 입력 문장 x 라는 조건이 하나 더 붙은 거예요.",
          f"그래서 {CLM}이라고 불러요. 하는 일은 3주차의 {NTP} 그대로예요.",
          "학습은 3주차에 배운 교차 엔트로피 그대로예요."),
      analogy("조건이 붙은 자판 추천",
              "휴대폰 자판이 다음 단어를 추천할 때, 원래는 내가 쓴 앞부분만 봐요. 번역기는 거기에 '원문' 이라는 조건이 하나 더 붙어요.",
              ("내가 쓴 앞부분", "앞서 만든 토큰들 y1 ... y(t-1)"),
              ("원문이라는 조건", "입력 문장 x"),
              ("추천 목록", "다음 토큰의 확률 분포"))],
     [formula("문장 확률을 쪼개는 식",
              r"P(y \mid x) = P(y_1 \mid x)\, P(y_2 \mid y_1, x)\, P(y_3 \mid y_1, y_2, x) \cdots P(y_T \mid y_1, \dots, y_{T-1}, x)",
              [(r"P(y \mid x)", "원문 x 를 봤을 때 답 문장 y 전체가 나올 확률"),
               (r"P(y_1 \mid x)", "첫 토큰은 x 만 보고 정해요"),
               (r"P(y_2 \mid y_1, x)", "두 번째는 x 와 이미 만든 y1 을 보고 정해요"),
               (r"\cdots", "끝까지 같은 방식으로 이어져요"),
               (r"y_T", "마지막 T 번째 토큰")],
              f"매 자리마다 x 가 조건으로 계속 붙는 것, 이게 {CLM}이에요."),
      points("슬라이드 영어와 우리말 뜻",
             "conditioned on the source = 원문을 조건으로 삼아서",
             "factorises the same way an LM does = 언어 모델과 똑같은 방식으로 쪼개진다",
             "ordinary cross-entropy on the target tokens = 목표 토큰에 대한 평범한 교차 엔트로피",
             "the gradient flows all the way back = 기울기가 끝까지 거슬러 흐른다"),
      points("3주차와 이어지는 점",
             f"3주차에서 배운 {NTP}과 계산이 똑같아요. 조건 x 하나가 더 붙었을 뿐이에요.",
             f"교수님: {NTP}이 거의 모든 걸 결정한다, GPT 도 다 결국 이거다.",
             f"그래서 {LM}을 이해하면 번역 모델도 바로 이해돼요.")],
     [formula("학습 손실",
              r"J = \frac{1}{T}\sum_{t=1}^{T} J_t, \qquad J_t = -\log P(y_t^{*} \mid y_{<t}^{*}, x)",
              [(r"J_t", "t 번째 자리의 벌점"),
               (r"y_t^{*}", "t 번째 자리의 정답 토큰(별표가 정답이라는 표시예요)"),
               (r"y_{<t}^{*}", "t 보다 앞의 정답 토큰들"),
               (r"-\log", "정답에 준 확률이 작을수록 커지는 벌점"),
               (r"\frac{1}{T}\sum", "모든 자리의 벌점을 더해 자리 수로 나눈 평균")],
              f"{CE} 그대로예요. 3주차 {LOSS}와 같은 식이에요."),
      steps("벌점을 손으로 계산해 봐요",
            ["네 자리의 정답 확률이 각각 0.5, 0.25, 0.8, 0.1 이라고 해요",
             "J1 = -log(0.5) = 0.693",
             "J2 = -log(0.25) = 1.386",
             "J3 = -log(0.8) = 0.223",
             "J4 = -log(0.1) = 2.303",
             "합 = 4.605, 자리 수 4 로 나누면 1.151"],
            "평균 벌점 J = 1.151 이에요. 정답 확률이 클수록 벌점이 작아요.",
            "정답 확률 0.5, 0.25, 0.8, 0.1 (자연로그를 써요)"),
      look("슬라이드를 짚어 읽어요",
           (0.05, 0.19, 0.90, 0.06, "첫 줄: 디코더는 원문에 조건이 걸린 언어 모델이라는 설명이에요."),
           (0.05, 0.25, 0.90, 0.09, "둘째 줄: 학습은 평범한 교차 엔트로피, 기울기는 디코더, 다리, 인코더까지 흐른다."),
           (0.16, 0.45, 0.70, 0.09, "위 식: 문장 확률을 자리별 확률의 곱으로 쪼갠 식이에요."),
           (0.34, 0.58, 0.36, 0.10, "아래 식: 자리별 벌점 J_t 와 그 평균 J 예요."),
           (0.24, 0.85, 0.52, 0.06, f"맨 아래: one model, one loss, one backward pass 가 {E2E}의 뜻이에요.")),
      prof("교수님: 매 단계마다 원문 x 가 추가 조건으로 들어간다는 게 기존 언어 모델과 다른 점이에요.",
           f"교수님: 끝까지 만들고 나서 한 번에 기울기가 업데이트되는 구조를 {E2E}라고 해요.")],
     [check("J_t 의 값이 가장 큰 경우는?",
            ["정답 토큰에 준 확률이 0.01 일 때", "0.9 일 때", "0.5 일 때", "1.0 일 때"], 0,
            "-log(0.01) = 4.61 로 가장 커요. 정답에 준 확률이 작을수록 벌점이 커져요."),
      english("답안 문장",
              f"{S2S}의 디코더는 원문 x 를 조건으로 하는 언어 모델이므로 P(y|x) 를 자리별 조건부 확률의 곱으로 쪼갤 수 있고, 학습 손실은 정답 토큰에 대한 교차 엔트로피의 평균이다.",
              f"'조건이 붙은 언어 모델 + 교차 엔트로피 + {E2E}' 세 마디로 외워요."),
      warn("헷갈리기 쉬운 점",
           "곱으로 쓴 식은 확률, 합으로 쓴 식은 손실이에요. 로그를 씌우면 곱이 합으로 바뀌어요.",
           "별표가 붙은 y* 는 정답 토큰이라는 뜻이에요. 모델이 만든 토큰이 아니에요.")])

# ---------------------------------------------------------------- p.11
page(11, "학습 방법: 교사 강요", ["Teacher Forcing", "Exposure Bias", "Inference", "Cross-Entropy", "Loss Function"],
     [say(f"학습할 때는 {TF}를 써요. 모델이 뭐라고 예측했든, 다음 입력으로는 정답 단어를 넣어 줘요.",
          "선생님이 옆에서 정답을 계속 알려 주는 것과 같아서 이런 이름이에요."),
      analogy("받아쓰기 연습",
              "받아쓰기를 하다가 한 글자 틀려도 선생님이 바로 정답을 알려 주고 다음 글자로 넘어가요. 그래야 뒤쪽 연습도 제대로 할 수 있어요.",
              ("선생님이 알려 주는 정답", "정답 토큰을 다음 입력으로 넣기"),
              ("한 글자 틀려도 계속 진도", "각 자리의 벌점만 따로 매기기"),
              ("실전에서는 알려 주는 사람이 없다", EB))],
     [compare("슬라이드 영어와 우리말 뜻",
              ["영어 원문", "뜻"],
              ["we feed the decoder the true previous target word", "디코더에 직전의 진짜 정답 단어를 넣어 준다"],
              ["not its own prediction", "모델 자신의 예측이 아니라"],
              ["it keeps training stable and parallel over time steps", "학습이 안정되고 시점끼리 병렬로 돌아간다"],
              ["at test time the model only ever sees its own output", "시험 때는 모델이 자기 출력만 본다"],
              ["this mismatch is called exposure bias", f"이 어긋남을 {EB}이라고 한다"]),
      points("왜 학습이 병렬이 되나요",
             "정답 문장을 이미 알고 있으니, 모든 자리의 입력을 처음부터 다 알 수 있어요.",
             "그래서 자리마다 기다릴 필요 없이 한꺼번에 계산할 수 있어요.",
             f"반대로 {INF} 때는 앞 토큰을 만들어야 다음 입력이 정해지니 순차적이에요.")],
     [look("슬라이드를 짚어 읽어요",
           (0.05, 0.19, 0.90, 0.06, "첫 줄: 학습 때는 진짜 정답 단어를 넣는다는 정의예요."),
           (0.05, 0.25, 0.90, 0.09, "Why 와 The catch: 왜 쓰는지, 그리고 대가가 무엇인지예요."),
           (0.21, 0.42, 0.58, 0.09, "gold targets 줄: 위쪽의 he hit me with a pie <e> 가 정답이에요."),
           (0.21, 0.45, 0.58, 0.09, "per-step loss 줄: 자리마다 J1 ... J7 벌점을 따로 매겨요."),
           (0.21, 0.63, 0.58, 0.09, "fed back in 줄: 아래쪽 입력이 모델 예측이 아니라 정답 단어예요."),
           (0.25, 0.75, 0.50, 0.07, "식 J = (1/T) 합 J_t 와 backprop 이 인코더까지 흐른다는 설명이에요.")),
      prof("교수님: 가장 자연스러운 방법은 모델이 방금 예측한 단어를 다음 입력으로 넣는 건데, 학습 초반에는 모델이 잘 못하겠죠.",
           "교수님: 그래서 각 토큰마다 지도 학습 형식으로 정답을 주는 걸 교사 강요라고 해요.",
           "교수님: 학습 환경과 테스트 환경이 다른 이 어긋남을 익스포저 바이어스라고 합니다."),
      bg("배경 지식", "강화 학습은 문장을 다 만든 뒤 마지막에 보상을 줘요. 그래서 어느 토큰이 잘했는지 알기 어려워요.",
         "교사 강요는 자리마다 바로 벌점을 줄 수 있어서 학습이 훨씬 빠르고 안정적이에요.")],
     [check("교사 강요의 대가로 생기는 문제는?",
            ["노출 편향", "기울기 폭발", "과적합", "정보 병목"], 0,
            f"학습 때는 정답을, 시험 때는 자기 출력을 본다는 어긋남이 {EB}이에요."),
      exam("N4 Check Yourself",
           "Q2. In teacher forcing, what exactly is different between training time and test time?",
           f"{TF}에서 학습할 때와 시험할 때가 정확히 무엇이 다른가?",
           ["학습할 때는 정답 토큰(gold token)을 다음 입력으로 넣을 수 있어요",
            "시험(추론)할 때는 정답을 모르니까 모델이 직전에 만든 토큰을 넣어야 해요",
            "그래서 디코더가 보는 앞부분이 학습과 시험에서 달라져요",
            f"이 어긋남을 {EB}이라고 불러요"],
           "다음 입력이 학습에서는 정답 토큰, 시험에서는 모델 자신의 출력이라는 점이 다르다(노출 편향)."),
      english("답안 문장",
              f"{TF}는 학습 시 디코더의 다음 입력으로 정답 토큰을 넣어 학습을 안정적이고 병렬적으로 만든다. 추론 시에는 모델 자신의 출력만 보므로 학습과 추론이 어긋나는 {EB}이 생긴다.",
              "장점(안정, 병렬)과 단점(노출 편향)을 반드시 함께 써요.")])

# ---------------------------------------------------------------- p.12
page(12, "디코딩 1: 탐욕적 디코딩", ["Greedy Decoding", "Inference", "Beam Search"],
     [say(f"이제 학습이 끝난 모델로 문장을 만들어요. 이걸 {INF}이라고 해요.",
          f"가장 단순한 방법이 {GD}이에요. 매 순간 확률이 가장 높은 토큰 하나만 골라요."),
      figure("탐욕은 되돌릴 수 없어요", FIG_GREEDY, "첫 칸에서 확률이 높은 he 를 고르면 더 좋은 I was 길을 영영 잃어요.", 5),
      analogy("갈림길에서 눈앞만 보기",
              "산에서 갈림길마다 지금 당장 더 편해 보이는 쪽으로만 가요. 나중에 막다른 길이 나와도 되돌아갈 수 없어요.",
              ("지금 당장 편한 쪽", "그 자리에서 확률이 가장 높은 토큰"),
              ("되돌아갈 수 없음", "한 번 고르면 취소 못 함"),
              ("전체로는 더 좋은 길", "전체 문장 확률이 더 높은 다른 후보"))],
     [compare("슬라이드 영어와 우리말 뜻",
              ["영어 원문", "뜻"],
              ["At each step take the single most likely word", "매 단계마다 가장 그럴듯한 단어 하나를 고른다"],
              ["Fast, and often fine", "빠르고, 대개는 괜찮다"],
              ["it cannot take anything back", "아무것도 되돌릴 수 없다"],
              ["one confident wrong word early on poisons everything that follows",
               "앞에서 자신 있게 틀린 단어 하나가 뒤 전체를 망친다"],
              ["one path through an exponentially large tree", "기하급수적으로 큰 나무에서 길 하나만 따라가기"]),
      points("greedy 라는 단어",
             "greedy 는 '욕심 많은, 탐욕스러운' 이라는 뜻이에요.",
             "알고리즘 수업에서 말하는 그 탐욕 알고리즘과 같은 생각이에요.",
             "지금 이 순간 제일 좋아 보이는 것만 고르는 방식이에요.")],
     [steps("탐욕이 놓치는 예를 손으로",
            ["첫 자리 확률: he 0.6, I 0.4 → 탐욕은 he 를 골라요",
             "he 뒤: hit 0.3, struck 0.2",
             "I 뒤: was 0.9, got 0.1",
             "he hit 의 전체 확률 = 0.6 x 0.3 = 0.18",
             "I was 의 전체 확률 = 0.4 x 0.9 = 0.36",
             "전체로 보면 I was 가 두 배나 좋은데, 탐욕은 그 길을 아예 못 봐요"],
            "국소적으로 최선이 전체적으로 최선을 보장하지 않아요.",
            "첫 자리 he 0.6 / I 0.4, 둘째 자리 위와 같음"),
      look("슬라이드를 짚어 읽어요",
           (0.05, 0.19, 0.90, 0.06, "첫 줄: 매 단계 가장 그럴듯한 단어 하나를 고른다. 빠르고 대개 괜찮다."),
           (0.05, 0.24, 0.90, 0.06, "둘째 줄: 되돌릴 수 없다. 앞에서 틀리면 뒤가 다 망가진다."),
           (0.06, 0.50, 0.90, 0.13, "가운데 상자들: he hit 까지는 초록(좋음)인데 a 부터 빨강으로 바뀌어요."),
           (0.23, 0.65, 0.56, 0.06, "빨간 글씨: 3단계에서 a 를 골랐지만 좋은 이어짐은 me with a pie 였어요."),
           (0.20, 0.73, 0.60, 0.06, "그래서 여러 후보를 함께 탐색하자는 제안으로 이어져요.")),
      prof("교수님: 매 순간은 좋은 선택이지만, 우리가 원하는 건 전체 P(y|x) 를 높이는 거예요.",
           "교수님: 로컬 베스트가 글로벌 베스트를 보장하지 않는다는 건 너무 자명하죠.")],
     [check("탐욕적 디코딩의 가장 큰 약점은?",
            ["한 번 고른 토큰을 되돌릴 수 없다", "계산이 너무 느리다", "어휘가 커야 한다", "학습이 불안정하다"], 0,
            "슬라이드 문장 it cannot take anything back 이 그대로 답이에요."),
      warn("헷갈리기 쉬운 점",
           f"{GD}는 '나쁜 방법' 이 아니에요. 빠르고 대개 괜찮아서 요즘 {LLM}에서도 많이 써요.")])

# ---------------------------------------------------------------- p.13
page(13, "디코딩 2: 빔 서치", ["Beam Search", "Beam Size", "Length Normalization", "Greedy Decoding"],
     [say(f"{BS}는 후보 하나 대신 좋은 후보 k 개를 함께 들고 가요.",
          f"이 k 를 {BSZ}라고 해요. 보통 5에서 10 을 써요."),
      analogy("등산로 여러 개를 함께 살피기",
              "갈림길마다 길 하나만 고르지 않고, 지금까지 가장 유망한 두 길을 계속 들고 가면서 비교해요.",
              ("들고 가는 길 개수", BSZ),
              ("지금까지의 점수", "로그 확률의 합"),
              ("길이 하나만 남을 때", "k = 1, 곧 탐욕적 디코딩"))],
     [compare("슬라이드 영어와 우리말 뜻",
              ["영어 원문", "뜻"],
              ["Keep the k best partial hypotheses at every step", "매 단계마다 가장 좋은 부분 후보 k 개를 남긴다"],
              ["Typical k is 5 to 10", "보통 k 는 5에서 10"],
              ["Score is a sum of log-probabilities", "점수는 로그 확률의 합이다"],
              ["longer sequences score lower", "길수록 점수가 낮아진다"],
              ["divide by length before comparing finished hypotheses",
               f"끝난 후보를 비교하기 전에 길이로 나눈다({LNORM})"]),
      formula("부분 후보의 점수",
              r"\text{score}(y_{1:t}) = \sum_{i=1}^{t} \log P(y_i \mid y_{<i}, x)",
              [(r"\log P", "각 자리에서 고른 토큰의 확률에 로그를 씌운 값"),
               (r"\sum", "지금까지 고른 토큰들의 로그 확률을 모두 더해요"),
               (r"y_{1:t}", "첫 토큰부터 t 번째까지의 부분 문장")],
              "확률은 1보다 작으니 로그는 음수예요. 그래서 길어질수록 점수가 계속 내려가요.")],
     [look("슬라이드의 나무를 짚어 읽어요",
           (0.05, 0.19, 0.90, 0.06, "첫 줄: 매 단계 k 개를 남긴다, 보통 5에서 10."),
           (0.05, 0.24, 0.90, 0.06, "둘째 줄: 점수는 로그 확률의 합, 길면 낮아지니 길이로 나눠 비교한다."),
           (0.17, 0.53, 0.09, 0.07, "<s> 0.0 에서 출발해요."),
           (0.28, 0.45, 0.10, 0.20, "t=1: he -0.7 과 I -1.3 두 개를 남겨요(k=2)."),
           (0.40, 0.40, 0.12, 0.30, "t=2: he hit -1.6 과 I was -2.9 가 살아남고, 점선 상자는 버려요."),
           (0.54, 0.40, 0.14, 0.28, "t=3: he hit me -2.5 와 I was hit -3.5."),
           (0.66, 0.40, 0.16, 0.28, "오른쪽 범례: 파랑은 살아남음, 점선은 버림, 초록은 다음으로 넓힘."),
           (0.17, 0.72, 0.66, 0.09, "아래 상자: 부분 후보의 점수는 로그 확률의 합이라는 식이에요.")),
      steps("길이 정규화가 왜 필요한가요",
            ["끝난 후보 A: 토큰 3개, 로그 확률 합 -2.5",
             "끝난 후보 B: 토큰 6개, 로그 확률 합 -4.2",
             "합만 비교하면 -2.5 > -4.2 이므로 짧은 A 가 이겨요",
             "길이로 나누면 A 는 -2.5 / 3 = -0.833",
             "B 는 -4.2 / 6 = -0.700",
             "-0.700 > -0.833 이므로 이번에는 B 가 이겨요"],
            "길이로 나누지 않으면 짧은 문장만 계속 뽑혀요. 그래서 길이 정규화를 해요.",
            "후보 A(길이 3, 합 -2.5), 후보 B(길이 6, 합 -4.2)"),
      prof("교수님: 보통 빔은 5에서 10 정도를 많이 쓰고, 그림에서는 k 를 2로 둔 거예요.",
           "교수님: 로그 확률이 음수라 길이가 길어질수록 점수가 계속 낮아져요. 그래서 길이 정규화를 해요.",
           "교수님: 빔 서치는 빔 크기를 2, 3만 해도 확실히 그리디보다 훨씬 오래 걸려요. 항상 좋은 건 아니고 트레이드 오프가 있어요."),
      bg("배경 지식", "로그 확률을 쓰는 이유는 아주 작은 확률을 여러 번 곱하면 컴퓨터에서 0 으로 내려앉기 때문이에요.",
         "곱을 로그로 바꾸면 합이 되고, 숫자가 안정돼요(기초 다지기 4단원).")],
     [exam("N4 Check Yourself",
           "Q3. Beam search with k = 1 is the same as which algorithm? And why must we normalise by length?",
           f"{BSZ} k = 1 인 {BS}는 어떤 알고리즘과 같고, 왜 {LNORM}가 필요한가?",
           ["k = 1 이면 매 단계마다 후보를 하나만 남겨요",
            f"그건 매 순간 최고만 고르는 {GD}와 똑같아요",
            "점수는 로그 확률의 합이고 로그 확률은 음수예요",
            "그래서 문장이 길어질수록 점수가 계속 작아져요",
            "나누지 않으면 짧은 문장만 뽑히니까 길이로 나눠 비교해요"],
           "k = 1 은 탐욕적 디코딩과 같다. 로그 확률의 합이 길이에 따라 계속 작아져 짧은 문장을 과도하게 선호하므로 길이로 나눈다."),
      check("k = 2 인 빔 서치가 매 단계에서 하는 일은?",
            ["후보마다 다음 토큰을 뽑아 점수순으로 2개만 남긴다", "항상 가장 높은 1개만 남긴다",
             "모든 후보를 끝까지 남긴다", "무작위로 2개를 고른다"], 0,
            "빔 크기만큼만 남기고 나머지는 가지치기(pruning)해요."),
      warn("헷갈리기 쉬운 점",
           "슬라이드 그림은 교수님이 '조금 단순화시켰다' 고 한 그림이에요. 점수만 보면 he struck(-2.3)이 I was(-2.9)보다 높은데, 그림은 가지마다 하나씩 남겼어요.",
           "원래 빔 서치 논문에는 남기는 수 n 과 뽑는 수 k 가 따로 있어요. 수업에서는 둘을 같다고 보고 k 하나로 설명해요.")])

# ---------------------------------------------------------------- p.14
page(14, "번역 평가: BLEU", ["BLEU", "n-gram", "Brevity Penalty", "Machine Translation (MT)"],
     [say(f"만들어 낸 번역이 좋은지 어떻게 재나요. 가장 많이 쓰인 점수가 {BLEU}예요.",
          f"사람이 쓴 정답 문장(reference)과 {NG}이 얼마나 겹치는지를 세요."),
      analogy("답안지와 모범답안 겹쳐 보기",
              "모범답안과 내 답안을 겹쳐 놓고, 한 단어짜리, 두 단어짜리, 세 단어짜리, 네 단어짜리 표현이 각각 얼마나 똑같이 나왔는지 세요.",
              ("모범답안", "reference, 곧 사람이 만든 정답 번역"),
              ("내 답안", "output, 곧 모델의 번역"),
              ("겹친 표현 세기", f"{NG} 정밀도 n = 1 에서 4"),
              ("너무 짧게 써서 점수 따는 꼼수 막기", BP))],
     [compare("슬라이드 영어와 우리말 뜻",
              ["영어 원문", "뜻"],
              ["compares the model output against one or more human references",
               "모델 출력을 사람이 만든 정답 하나 이상과 비교한다"],
              ["counting overlapping n-grams (n = 1...4)", "겹치는 n-gram 을 n = 1 에서 4 까지 센다"],
              ["with a brevity penalty so the model cannot win by saying less",
               "짧게 말해서 이기지 못하도록 간결성 페널티를 둔다"],
              ["a good translation that uses different words scores badly",
               "다른 말로 잘 옮긴 번역도 점수가 나쁘게 나온다"],
              ["BLEU rewards being ordinary", "BLEU 는 평범한 번역에 상을 준다"]),
      points("슬라이드의 예문",
             "reference: the cat is on the mat",
             "output: the cat the cat on the mat",
             "1-gram 은 많이 겹치는데 4-gram 은 하나도 안 겹쳐요.",
             "슬라이드 막대: 0.86, 0.50, 0.20, 0.00")],
     [steps("2-gram 정밀도를 손으로 세어 봐요",
            ["출력의 2-gram: the cat / cat the / the cat / cat on / on the / the mat → 6개",
             "정답의 2-gram: the cat / cat is / is on / on the / the mat → 5개",
             "the cat 은 정답에 1번뿐이라 출력에 2번 나와도 1번만 인정해요",
             "맞은 것: the cat 1개, on the 1개, the mat 1개 = 3개",
             "2-gram 정밀도 = 3 / 6 = 0.50"],
            "슬라이드 막대의 0.50 과 같아요.",
            "reference: the cat is on the mat / output: the cat the cat on the mat"),
      steps("3-gram 과 4-gram 도 세어 봐요",
            ["출력의 3-gram: the cat the / cat the cat / the cat on / cat on the / on the mat → 5개",
             "정답의 3-gram: the cat is / cat is on / is on the / on the mat → 4개",
             "맞은 것: on the mat 1개 → 1 / 5 = 0.20",
             "출력의 4-gram: the cat the cat / cat the cat on / the cat on the / cat on the mat → 4개",
             "정답의 4-gram 중 같은 것이 하나도 없어요 → 0 / 4 = 0.00"],
            "3-gram 0.20, 4-gram 0.00. BLEU 는 네 정밀도를 곱하므로 하나가 0 이면 전체가 0 이에요."),
      look("슬라이드를 짚어 읽어요",
           (0.05, 0.19, 0.90, 0.07, "정의 줄: 정답과 겹치는 n-gram 을 세고 간결성 페널티를 붙인다."),
           (0.05, 0.28, 0.90, 0.09, "Example 줄: 슬라이드가 든 예문과 그 결과예요."),
           (0.05, 0.38, 0.90, 0.06, "It is useful but imperfect: 쓸모 있지만 완벽하지 않다는 경고예요."),
           (0.17, 0.52, 0.48, 0.18, "가운데 상자: 위가 reference, 아래가 output 이에요."),
           (0.68, 0.45, 0.24, 0.25, "오른쪽 막대: n-gram 정밀도 0.86, 0.50, 0.20, 0.00."),
           (0.23, 0.73, 0.54, 0.05, "설명: 유니그램은 괜찮아 보여도 4-gram 은 아니다, BLEU 는 정밀도를 곱하므로 반복이 벌을 받는다.")),
      prof("교수님: 블루는 레퍼런스 기반 점수라서 사람이 만든 정답 문장이 꼭 하나 필요해요.",
           "교수님: 모델이 짧은 문장만 내서 정밀도를 높이는 걸 막기 위해 너무 짧은 번역에 페널티를 주는 항이 있어요.",
           "교수님: 요새는 좀 오래된 지표지만 이미지 캡셔닝 같은 데서는 아직도 쓰이니 알아 두면 좋아요.")],
     [check("BLEU 에서 4-gram 정밀도가 0 이면 어떻게 되나요?",
            ["네 정밀도를 곱하므로 BLEU 가 0 이 된다", "1-gram 점수만 쓴다", "간결성 페널티가 사라진다", "점수가 오히려 올라간다"], 0,
            "슬라이드: BLEU multiplies the precisions. 하나가 0 이면 곱이 0 이에요."),
      english("답안 문장",
              f"{BLEU}는 모델 번역과 정답 번역 사이에서 1-gram 부터 4-gram 까지의 겹침을 재고, 짧은 번역을 막으려고 {BP}를 곱한다. 뜻이 같아도 표현이 다르면 점수가 낮은 한계가 있다.",
              "정의(겹침) + 페널티(짧음 방지) + 한계(표현 다양성) 세 마디를 꼭 넣어요."),
      warn("헷갈리기 쉬운 점",
           "슬라이드의 1-gram 값은 0.86(6/7)이에요. 중복을 정답에 나온 횟수까지만 세는 규칙을 cat 에도 적용하면 5/7 = 0.71 이 돼요. 시험에서는 슬라이드 숫자를 기준으로 삼아요.",
           f"{BLEU}가 높다고 언제나 번역이 더 좋은 건 아니에요. 다른 낱말로 잘 옮기면 오히려 점수가 낮아져요.")])

# ---------------------------------------------------------------- p.15
page(15, "인코더 디코더는 번역만을 위한 것이 아니에요", ["Sequence-to-Sequence Model", "Encoder", "Decoder"],
     [say(f"{S2S}은 특정 과제 이름이 아니라 틀(프레임워크) 이름이에요.",
          "입력도 줄줄이, 출력도 줄줄이면 무엇이든 같은 구조로 풀 수 있어요."),
      compare("슬라이드의 다섯 가지 예",
              ["과제", "인코더가 읽는 것", "디코더가 쓰는 것"],
              ["Machine translation(번역)", "원문 문장", "목표 문장"],
              ["Summarization(요약)", "긴 문서", "짧은 요약"],
              ["Dialogue(대화)", "앞선 대화들", "다음 차례의 말"],
              ["Speech recognition(음성 인식)", "소리 신호", "글로 받아쓴 것"],
              ["Code generation(코드 생성)", "자연어로 쓴 요구", "프로그램 코드"])],
     [points("슬라이드 영어와 우리말 뜻",
             "The same architecture works whenever the input and the output are both sequences = 입력과 출력이 모두 시퀀스면 같은 구조가 통한다",
             "they need not be the same kind of sequence = 같은 종류의 시퀀스일 필요도 없다",
             "Learn the pattern once, reuse it for the rest of the course = 한 번 배워 두면 이 수업 내내 다시 쓴다"),
      points("같은 종류가 아니어도 된다는 말",
             "음성 인식은 소리가 들어가고 글이 나와요.",
             "코드 생성은 우리말 요구가 들어가고 파이썬 코드가 나와요.",
             "들어가는 것과 나오는 것의 모양(modality)이 달라도 괜찮아요.")],
     [look("슬라이드의 표를 짚어 읽어요",
           (0.05, 0.19, 0.90, 0.08, "위 줄: 입력과 출력이 모두 시퀀스이면 같은 구조가 통한다."),
           (0.06, 0.37, 0.24, 0.06, "왼쪽 열이 과제 이름이에요."),
           (0.28, 0.37, 0.36, 0.06, "가운데 주황 상자가 인코더가 읽는 것이에요."),
           (0.64, 0.37, 0.30, 0.06, "오른쪽 초록 상자가 디코더가 쓰는 것이에요."),
           (0.06, 0.44, 0.88, 0.30, "다섯 줄: 번역, 요약, 대화, 음성 인식, 코드 생성이에요.")),
      prof("교수님: 기억해야 될 건 시퀀스 투 시퀀스는 개별 태스크가 아니라 인코더 디코더를 갖는 공통 패턴의 프레임워크라는 점이에요.",
           "교수님: 입력과 출력이 꼭 같은 모달리티일 필요는 없어요.")],
     [check("다음 중 seq2seq 로 풀 수 있는 과제가 아닌 것은?",
            ["이미지 한 장을 고양이인지 개인지 분류하기", "긴 문서를 요약하기", "소리를 글로 받아쓰기", "자연어 설명으로 코드 만들기"], 0,
            "분류는 출력이 시퀀스가 아니라 칸 하나예요. 나머지 셋은 출력이 시퀀스라서 seq2seq 예요."),
      english("답안 문장",
              f"{S2S}은 입력과 출력이 모두 시퀀스인 모든 문제에 쓰이는 {ENC}, {DEC} 틀이다. 번역, 요약, 대화, 음성 인식, 코드 생성에 같은 구조가 다시 쓰인다.",
              "과제 다섯 개를 외워 두면 나열형 문제에 그대로 써요.")])

# ---------------------------------------------------------------- p.16
page(16, "정보 병목", ["Information Bottleneck", "Encoder", "Decoder", "Hidden State", "Attention"],
     [say(f"이제 Part 1 의 결론이에요. {S2S}의 진짜 약점은 {IB}이에요.",
          f"{DEC}가 원문에 대해 아는 모든 것이 고정 크기 벡터 하나에 들어가야 해요."),
      figure("문장이 길어도 통로는 그대로", FIG_BOTTLE, "20단어든 200단어든 같은 칸 수의 벡터를 지나가야 해요.", 4),
      analogy("좁은 문 하나",
              "큰 강당에 사람이 20명이든 200명이든, 나가는 문은 똑같이 하나뿐이에요. 사람이 많을수록 더 많이 밀리고 못 나가는 사람이 생겨요.",
              ("강당 안 사람 수", "입력 문장의 길이"),
              ("문 하나", "고정 크기 요약 벡터"),
              ("못 나간 사람", "버려진 정보"))],
     [compare("슬라이드 영어와 우리말 뜻",
              ["영어 원문", "뜻"],
              ["Everything the decoder knows about the source has to fit in one fixed-size vector",
               "디코더가 원문에 대해 아는 모든 것이 고정 크기 벡터 하나에 들어가야 한다"],
              ["A 20-word sentence and a 200-word paragraph get the same number of dimensions",
               "20단어 문장과 200단어 문단이 같은 개수의 차원을 받는다"],
              ["performance duly collapses as sentences get longer", "문장이 길어질수록 성능이 그대로 무너진다"],
              ["stop forcing the decoder to use only that vector", "디코더가 그 벡터만 쓰도록 강요하지 말자"]),
      points("fixed-size 라는 말",
             "fixed-size vector 는 '칸 수가 정해진 벡터' 예요. 예를 들어 512칸이면 언제나 512칸이에요.",
             "입력이 길어져도 칸이 늘지 않아요. 그래서 긴 입력일수록 더 많이 버려야 해요.")],
     [look("슬라이드를 짚어 읽어요",
           (0.05, 0.19, 0.90, 0.06, "첫 줄: 디코더가 아는 모든 것이 고정 크기 벡터 하나에 들어가야 한다."),
           (0.05, 0.25, 0.90, 0.09, "둘째 줄: 20단어든 200단어든 차원이 같아서 길면 성능이 무너진다."),
           (0.05, 0.33, 0.90, 0.06, "셋째 줄: 해결은 거의 자명하다. 그 벡터만 쓰도록 강요하지 않는 것."),
           (0.09, 0.46, 0.26, 0.10, "빨간 글씨: 하나의 고정 벡터가 원문 전체를 날라야 한다는 경고예요."),
           (0.33, 0.56, 0.08, 0.09, "빨간 느낌표 자리가 바로 병목이에요.")),
      prof("교수님: 인코더는 굉장히 많은 정보를 갖고 있는데, 디코더로 전달되는 통로가 딱 하나의 고정 크기 벡터라는 게 정보 병목의 가장 큰 문제예요.",
           "교수님: 입력이 짧으면 어느 정도 되겠지만, 문장이 길어질수록 기억해야 할 정보가 훨씬 많아져요.",
           f"교수님: 이걸 해결하기 위해서 {ATT}이라는 기법을 배워 보겠습니다.")],
     [exam("N4 Check Yourself",
           "Q1. Why does a fixed-size encoder vector hurt long sentences more than short ones?",
           "고정 크기 인코더 벡터는 왜 짧은 문장보다 긴 문장에서 더 해로운가?",
           "입력이 10단어든 1000단어든 디코더로 가는 통로는 같은 크기의 벡터 하나예요".split("\n") + [
            "긴 문장일수록 담아야 할 정보(등장인물, 단어 뜻, 문장 구조)가 훨씬 많아요",
            "칸 수는 그대로인데 담을 게 늘어나니 잃어버리는 정보가 커져요",
            "그래서 문장이 길어질수록 번역 성능이 급격히 떨어져요"],
           "입력 길이와 상관없이 통로가 같은 크기라서, 긴 문장일수록 압축 과정에서 잃는 정보가 커지기 때문이다."),
      english("답안 문장",
              f"{S2S}에서 {ENC}의 정보는 고정 크기 벡터 하나로만 {DEC}에 전달된다. 그래서 문장이 길어질수록 압축 손실이 커지는 {IB}이 생긴다.",
              "'고정 크기 + 유일한 통로 + 길수록 손실' 세 조각을 꼭 넣어요."),
      warn("헷갈리기 쉬운 점",
           f"{IB}은 파라미터가 부족해서 생기는 문제가 아니에요. 통로의 크기가 입력 길이에 따라 늘지 않는 게 문제예요.")])

data = {"deck": "N4", "from": 1, "to": 16,
        "glossary": [{"ko": k, "en": e, "say": s, "more": m} for k, e, s, m in GLOSSARY],
        "slides": S}

raw = json.dumps(data, ensure_ascii=False, indent=1)
for ch in ("—", "–", "·", "・"):
    assert ch not in raw, ch
with open(OUT, "w", encoding="utf-8") as f:
    f.write(raw)
print("saved", OUT, len(S), "pages")
