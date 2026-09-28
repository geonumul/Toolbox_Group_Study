# -*- coding: utf-8 -*-
"""5강(N5) Pre-trained Language Models 회독 레슨 14~25쪽 생성기.
사용: python build_N5_014-025.py   출력: N5_014-025.json
5주차는 녹음이 아직 없어서 prof 장면을 만들지 않는다.
손계산은 아래에서 실제로 계산해 assert 로 확인한다."""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "N5_014-025.json")


# ---------------- 손계산 확인 (assert) ----------------
# p.14 막대그래프 (단위: 10억 단어)
bars = {"GPT-1": 0.8, "BERT": 3.3, "RoBERTa": 30.0, "GPT-3": 300.0}
assert round(bars["GPT-3"] / bars["GPT-1"]) == 375
assert 300 <= round(bars["GPT-3"] / bars["GPT-1"]) <= 400

# p.22 BERT 학습 데이터 합 (0.8B + 2.5B = 3.3B, p.14 막대와 같다)
assert round(0.8 + 2.5, 1) == 3.3 == bars["BERT"]

# p.19, p.20 마스킹 계산
n_tokens = 1000
chosen = int(n_tokens * 0.15)
assert chosen == 150
to_mask = int(chosen * 0.8)
to_random = int(chosen * 0.1)
to_keep = chosen - to_mask - to_random
assert (to_mask, to_random, to_keep) == (120, 15, 15)
assert to_mask + to_random + to_keep == chosen == 150
# 손실을 세는 자리는 고른 자리 전부
assert chosen == 150 and n_tokens - chosen == 850

# 100 토큰짜리 문장이면
assert int(100 * 0.15) == 15
assert int(15 * 0.8) == 12 and int(15 * 0.1) == 1 and 15 - 12 - 1 == 2

# p.22 BERT-base 와 BERT-large
base = {"layers": 12, "hidden": 768, "heads": 12, "params": 110}
large = {"layers": 24, "hidden": 1024, "heads": 16, "params": 340}
assert large["layers"] // base["layers"] == 2
assert round(large["params"] / base["params"], 1) == 3.1
assert base["hidden"] // base["heads"] == 64
assert large["hidden"] // large["heads"] == 64
assert 64 * 12 == 768 and 64 * 16 == 1024

# p.22 사전 학습 비용
assert 64 * 4 == 256  # TPU 칩 x 일

# p.24 GLUE 평균 (Devlin et al., Table 1)
glue = {"BiLSTM+ELMo": 71.0, "OpenAI GPT": 75.1, "BERT base": 79.6, "BERT large": 82.1}
assert round(glue["BERT large"] - glue["BiLSTM+ELMo"], 1) == 11.1
assert round(glue["BERT large"] - glue["OpenAI GPT"], 1) == 7.0
assert round(glue["BERT large"] - glue["BERT base"], 1) == 2.5
assert round(glue["BERT base"] - glue["OpenAI GPT"], 1) == 4.5

# p.23 네 가지 과제 모양
shapes = ["single sentence", "sentence pair", "token tagging", "span extraction"]
assert len(shapes) == 4

# p.17 세 구조
arch = ["encoder", "encoder-decoder", "decoder"]
assert len(arch) == 3

# ---------------- 용어 표기 ----------------
PT = "**사전 학습(Pre-training)**"
FT = "**미세조정(Finetuning)**"
TL = "**전이 학습(Transfer Learning)**"
SS = "**자기 지도 학습(Self-Supervision)**"
SL = "**지도 학습(Supervised Learning)**"
LB = "**레이블(Label)**"
CORP = "**말뭉치(Corpus)**"
MEMO = "**암기(Memorization)**"
WK = "**사실 지식(World Knowledge)**"
BIAS = "**편향(Bias)**"
LLM = "**LLM(대규모 언어 모델)**"
BERT = "**BERT(버트)**"
GPT = "**GPT(지피티)**"
T5 = "**T5(티파이브)**"
ROBERTA = "**RoBERTa(로베르타)**"
ENC = "**인코더(Encoder)**"
DEC = "**디코더(Decoder)**"
TRF = "**트랜스포머(Transformer)**"
SA = "**셀프 어텐션(Self-Attention)**"
ATT = "**어텐션(Attention)**"
CM = "**인과 마스킹(Causal Masking)**"
AR = "**자기회귀(Autoregressive)**"
BC = "**양방향 문맥(Bidirectional Context)**"
MLM = "**마스크 언어 모델(Masked Language Modelling (MLM))**"
MASK = "**마스크 토큰([MASK])**"
CLS = "**분류 토큰([CLS])**"
SEP = "**구분 토큰([SEP])**"
NSP = "**다음 문장 예측(Next Sentence Prediction (NSP))**"
SPC = "**스팬 손상(Span Corruption)**"
SPAN = "**스팬(Span)**"
DEN = "**잡음 제거(Denoising)**"
NTP = "**다음 토큰 예측(Next Token Prediction)**"
LM = "**언어 모델(Language Model (LM))**"
LOSS = "**손실 함수(Loss Function)**"
TOK = "**토큰(Token)**"
PARAM = "**파라미터(Parameter)**"
HEAD = "**헤드(Head)**"
TH = "**과제 헤드(Task Head)**"
BODY = "**몸통(Body)**"
DT = "**다운스트림 과제(Downstream Task)**"
SPAIR = "**문장 쌍(Sentence Pair)**"
TT = "**토큰 태깅(Token Tagging)**"
POS = "**품사 태깅(Part-of-Speech Tagging (POS))**"
SPX = "**스팬 추출(Span Extraction)**"
EQA = "**추출형 질의응답(Extractive QA)**"
ENT = "**함의(Entailment)**"
GLUE = "**GLUE(글루)**"
BENCH = "**벤치마크(Benchmark)**"
NER = "**개체명 인식(Named Entity Recognition (NER))**"
SENT = "**감성 분석(Sentiment Analysis)**"
CLSF = "**분류(Classification)**"
EMB = "**임베딩(Embedding)**"
HID = "**은닉 차원(Hidden Size)**"

GLOSSARY = [
    ("사전 학습", "Pre-training", "아무 글이나 잔뜩 읽히면서 모델 전체를 미리 학습시켜 두는 단계",
     "레이블 없이 글자만 있으면 돼요. BERT 는 TPU 칩 64개로 4일 걸렸어요."),
    ("미세조정", "Finetuning", "이미 학습된 모델을 내 과제 데이터로 조금만 더 학습시키는 단계",
     "GPU 한 장으로 몇 분에서 몇 시간이면 끝나요. 우리가 실습에서 할 일이에요."),
    ("전이 학습", "Transfer Learning", "한 곳에서 배운 것을 다른 과제로 옮겨 쓰는 것",
     "사전 학습된 몸통을 여러 과제로 옮겨 쓰는 것이 전이 학습이에요."),
    ("자기 지도 학습", "Self-Supervision", "사람이 답을 적어 주지 않아도 글 자체가 답이 되어 주는 학습",
     "빈칸 채우기와 다음 토큰 예측이 대표적인 방법이에요."),
    ("지도 학습", "Supervised Learning", "사람이 붙여 준 정답을 보고 배우는 보통의 학습",
     "미세조정 단계가 지도 학습이에요. 레이블이 수천 개쯤 필요해요."),
    ("레이블", "Label", "이 입력의 정답이 무엇인지 적어 둔 것",
     "다음 문장 예측에서는 IsNext 와 NotNext 두 가지가 레이블이에요."),
    ("말뭉치", "Corpus", "모아 놓은 글 더미",
     "BERT 는 BooksCorpus 8억 단어와 English Wikipedia 25억 단어로 학습했어요."),
    ("암기", "Memorization", "모델이 학습 글을 통째로 외워 그대로 다시 뱉어 내는 일",
     "일반화가 아니라 복사예요. 개인 정보가 섞여 있으면 문제가 커져요."),
    ("편향", "Bias", "글 속에 있던 치우친 생각이 모델에도 그대로 남는 것",
     "여기서 말하는 편향은 사회적 편향이에요. 신경망의 bias 항과는 다른 말이에요."),
    ("사실 지식", "World Knowledge", "세상에 대해 알고 있어야 채울 수 있는 정보",
     "사전 학습 글에 들어 있던 사실이 가중치 안에 남아요."),
    ("대규모 언어 모델", "Large Language Model (LLM)", "트랜스포머를 아주 크게 쌓아 만든 요즘 언어 모델",
     "GPT-3 이 대표예요. 학습 글이 3000억 단어까지 늘었어요."),
    ("버트", "BERT", "문장 양쪽을 다 보고 빈칸을 채우도록 사전 학습한 인코더 모델",
     "Bi-Directional Encoder Representations from Transformers 의 줄임말이에요. 2018년 Devlin 등이 냈어요."),
    ("지피티", "GPT", "앞만 보고 다음 토큰을 맞히도록 사전 학습한 디코더 모델",
     "BERT 와 같은 해에 반대 방향으로 건 내기예요. 글쓰기에 강해요."),
    ("티파이브", "T5", "인코더와 디코더를 모두 쓰고 스팬 손상으로 사전 학습한 모델",
     "Text-to-Text Transfer Transformer 의 줄임말이에요. 3단원에서 자세히 배워요."),
    ("로베르타", "RoBERTa", "BERT 를 더 오래, 더 많은 글로 다시 학습시킨 개선판",
     "다음 문장 예측을 빼고 더 좋은 점수를 냈어요."),
    ("인코더", "Encoder", "입력 문장을 양쪽 다 보면서 읽어 내는 쪽",
     "BERT 가 인코더예요. 분류, 태깅, 검색에 강하고 글쓰기는 못 해요."),
    ("디코더", "Decoder", "앞만 보면서 한 토큰씩 써 내려가는 쪽",
     "GPT 가 디코더예요. 인과 마스킹 때문에 뒤를 못 봐요."),
    ("트랜스포머", "Transformer", "어텐션만으로 만든 요즘 언어 모델의 기본 블록",
     "4주차에 조립했어요. 5주차에서는 이 블록 전체를 사전 학습해요."),
    ("셀프 어텐션", "Self-Attention", "한 문장이 자기 자신을 바라보는 어텐션",
     "4주차의 핵심이었어요. 마스크를 어떻게 씌우느냐가 인코더와 디코더를 가릅니다."),
    ("어텐션", "Attention", "필요한 곳을 골라 보는 장치. 점수를 매기고 가중 평균을 내요",
     "4주차의 주인공이었어요. 문맥을 읽는 힘이 여기서 나와요."),
    ("인과 마스킹", "Causal Masking", "지금 자리보다 뒤에 있는 토큰을 못 보게 가려 두는 것",
     "4주차 N4 p.43 에서 배웠어요. 디코더가 미래를 훔쳐보지 못하게 막아요."),
    ("자기회귀", "Autoregressive", "자기가 만든 앞부분을 다시 입력으로 넣으며 한 토큰씩 이어 가는 방식",
     "디코더가 글을 쓰는 방식이에요. 인코더는 이렇게 못 해요."),
    ("양방향 문맥", "Bidirectional Context", "앞과 뒤를 동시에 보고 판단하는 것",
     "인코더의 장점이에요. 빈칸을 채우려면 양쪽이 다 필요해요."),
    ("마스크 언어 모델", "Masked Language Modelling (MLM)", "토큰 일부를 가리고 원래 무엇이었는지 맞히게 하는 학습",
     "BERT 의 사전 학습 목적 함수예요. 토큰의 15 퍼센트를 골라요."),
    ("마스크 토큰", "[MASK]", "가려진 자리라는 뜻의 특별한 토큰",
     "고른 토큰의 80 퍼센트가 이것으로 바뀌어요. 미세조정 때는 나오지 않아요."),
    ("분류 토큰", "[CLS]", "문장 맨 앞에 붙여 두고 문장 전체의 요약으로 쓰는 특별한 토큰",
     "이 자리 위에 분류용 헤드를 얹어요."),
    ("구분 토큰", "[SEP]", "문장과 문장 사이를 나눠 주는 특별한 토큰",
     "문장 쌍 과제에서 A 와 B 를 가르는 표시예요."),
    ("다음 문장 예측", "Next Sentence Prediction (NSP)", "문장 B 가 정말 문장 A 다음에 오는 문장인지 맞히는 과제",
     "BERT 의 두 번째 목적 함수였어요. RoBERTa 가 빼 버렸어요."),
    ("스팬", "Span", "토큰 여러 개가 이어진 한 덩어리",
     "낱말 하나가 아니라 구절 단위예요."),
    ("스팬 손상", "Span Corruption", "이어진 덩어리를 통째로 지우고 되살리게 하는 학습",
     "T5 의 사전 학습 목적 함수예요. 3단원에서 자세히 배워요."),
    ("잡음 제거", "Denoising", "망가뜨린 입력을 원래대로 되돌리게 하는 학습 방식",
     "스팬 손상이 잡음 제거의 한 가지예요."),
    ("다음 토큰 예측", "Next Token Prediction", "앞을 보고 바로 다음 토큰이 무엇일지 맞히는 과제",
     "디코더의 사전 학습 목적 함수예요. 3주차 언어 모델과 같아요."),
    ("언어 모델", "Language Model (LM)", "다음 토큰을 맞히는 모델",
     "3주차에 배웠어요. 인코더는 이 모양으로 학습할 수 없어요."),
    ("손실 함수", "Loss Function", "틀린 정도를 매기는 벌점",
     "마스크 언어 모델에서는 가려진 자리에서만 벌점을 세요."),
    ("토큰", "Token", "글을 자른 조각. 레고 조각 하나라고 생각하면 돼요",
     "2주차에 배웠어요. BERT 는 워드피스로 자른 토큰을 써요."),
    ("파라미터", "Parameter", "모델이 학습하면서 값을 고쳐 나가는 숫자들",
     "BERT-base 는 1억 1천만 개, BERT-large 는 3억 4천만 개예요."),
    ("헤드", "Head", "멀티 헤드 어텐션에서 서로 다른 관점으로 보는 한 갈래",
     "BERT-base 는 12개, BERT-large 는 16개예요. 4주차에 배웠어요."),
    ("과제 헤드", "Task Head", "같은 몸통 위에 갈아 끼우는 작은 출력층",
     "분류면 분류용, 태깅이면 태깅용으로 바꿔 끼워요."),
    ("몸통", "Body", "과제가 바뀌어도 그대로 쓰는 사전 학습된 본체",
     "내려받은 가중치를 그대로 써요. 네 가지 과제 모양에서 몸통은 늘 같아요."),
    ("다운스트림 과제", "Downstream Task", "사전 학습 뒤에 실제로 풀고 싶은 우리 과제",
     "감성 분석, 개체명 인식, 질의응답 같은 것이에요."),
    ("문장 쌍", "Sentence Pair", "문장 두 개를 함께 넣어 관계를 묻는 과제 모양",
     "함의와 유사도가 여기에 들어가요. [SEP] 로 두 문장을 갈라요."),
    ("토큰 태깅", "Token Tagging", "토큰마다 딱지를 하나씩 붙이는 과제 모양",
     "개체명 인식과 품사 태깅이 여기에 들어가요."),
    ("품사 태깅", "Part-of-Speech Tagging (POS)", "낱말마다 명사인지 동사인지 표시하는 과제",
     "토큰 태깅의 대표 예예요."),
    ("스팬 추출", "Span Extraction", "글 속에서 답이 되는 구간의 시작과 끝을 찍는 과제 모양",
     "포인터 두 개, 곧 시작과 끝을 맞혀요."),
    ("추출형 질의응답", "Extractive QA", "주어진 글 안에서 답이 되는 구간을 찾아내는 질의응답",
     "답을 새로 쓰는 것이 아니라 글에서 오려 내요."),
    ("함의", "Entailment", "앞 문장이 참이면 뒤 문장도 참인지 따지는 관계",
     "문장 쌍 과제의 대표예요. GLUE 의 QNLI, RTE 가 이것이에요."),
    ("글루", "GLUE", "영어 이해 과제 아홉 개를 묶어 놓은 벤치마크",
     "General Language Understanding Evaluation 이에요. BERT 가 아홉 개를 한 번에 이겼어요."),
    ("벤치마크", "Benchmark", "모델끼리 실력을 견주는 공통 시험지",
     "같은 데이터, 같은 방식으로 재야 비교가 돼요."),
    ("개체명 인식", "Named Entity Recognition (NER)", "글 속에서 사람, 장소, 회사 이름을 찾아 표시하는 과제",
     "토큰 태깅 모양이에요."),
    ("감성 분석", "Sentiment Analysis", "글이 긍정인지 부정인지 가려내는 과제",
     "문장 하나 모양이에요. 이번 주 실습에서 직접 해 봐요."),
    ("분류", "Classification", "입력 하나에 정답 딱지 하나를 붙이는 과제",
     "인코더가 가장 잘하는 일이에요."),
    ("임베딩", "Embedding", "토큰을 숫자 벡터로 바꿔 주는 표",
     "검색용 문장 벡터를 만들 때도 인코더의 출력을 써요."),
    ("은닉 차원", "Hidden Size", "토큰 하나를 나타내는 벡터의 길이",
     "BERT-base 는 768, BERT-large 는 1024 예요. 헤드 수로 나누면 헤드 하나의 크기가 나와요."),
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


def grid(x0, y0, cell, rows, cols, filled, cls_on, cls_off, b):
    """마스크 격자. filled(r, c) 가 참이면 칠한다."""
    out = []
    for r in range(rows):
        for c in range(cols):
            cl = cls_on if filled(r, c) else cls_off
            out.append(R(x0 + c * cell, y0 + r * cell, cell - 1, cell - 1, cl, b))
    return "".join(out)


# ---- p.14 학습 글의 양
FIG_DATA = SVG(
    TX(240, 22, "4년 만에 글이 400배 늘었어요", "tb", 15),
    L(40, 190, 450, 190, "e", 1),
    R(60, 172, 54, 18, "n", 1), TX(87, 186, "0.8", "tl", 11, "middle", 1),
    TX(87, 208, "GPT-1", "tm", 11, "middle", 1), TX(87, 224, "BooksCorpus", "tm", 10, "middle", 1),
    R(160, 142, 54, 48, "n3", 2), TX(187, 172, "3.3", "tl", 11, "middle", 2),
    TX(187, 208, "BERT", "tm", 11, "middle", 2), TX(187, 224, "위키백과 추가", "tm", 10, "middle", 2),
    R(260, 100, 54, 90, "n3", 3), TX(287, 150, "30", "tl", 11, "middle", 3),
    TX(287, 208, "RoBERTa", "tm", 11, "middle", 3), TX(287, 224, "웹 글 추가", "tm", 10, "middle", 3),
    R(360, 52, 54, 138, "n2", 4), TX(387, 126, "300", "tl", 12, "middle", 4),
    TX(387, 208, "GPT-3", "tm", 11, "middle", 4), TX(387, 224, "CommonCrawl", "tm", 10, "middle", 4),
    TX(40, 44, "단위: 10억 단어", "tm", 11, "start", 1),
    TX(240, 250, "0.8 에서 300 으로, 약 375배예요", "tb", 14, "middle", 4),
)

# ---- p.17 세 구조 세 목적 함수
FIG_3ARCH = SVG(
    TX(240, 20, "세 구조, 세 가지 사전 학습 목적 함수", "tb", 15),
    R(14, 34, 146, 200, "box", 1), TX(87, 54, "인코더", "tb", 14, "middle", 1),
    grid(52, 64, 14, 5, 5, lambda r, c: True, "n2", "n", 1),
    TX(87, 156, "문장 전체를 양쪽 다 봐요", "t", 12, "middle", 1),
    TX(87, 182, "마스크 언어 모델", "tb", 13, "middle", 1),
    TX(87, 206, "BERT, RoBERTa", "tm", 11, "middle", 1),
    TX(87, 224, "분류, 태깅, 검색", "tm", 11, "middle", 1),
    R(167, 34, 146, 200, "box", 2), TX(240, 54, "인코더 디코더", "tb", 14, "middle", 2),
    grid(205, 64, 14, 5, 5, lambda r, c: c <= r, "n3", "n", 2),
    TX(240, 156, "읽을 때는 양쪽, 쓸 때는 앞에서", "t", 11, "middle", 2),
    TX(240, 182, "스팬 손상(잡음 제거)", "tb", 13, "middle", 2),
    TX(240, 206, "T5, BART, mT5", "tm", 11, "middle", 2),
    TX(240, 224, "번역, 요약", "tm", 11, "middle", 2),
    R(320, 34, 146, 200, "box", 3), TX(393, 54, "디코더", "tb", 14, "middle", 3),
    grid(358, 64, 14, 5, 5, lambda r, c: c <= r, "n4", "n", 3),
    TX(393, 156, "앞에 나온 것만 봐요", "t", 12, "middle", 3),
    TX(393, 182, "다음 토큰 예측", "tb", 13, "middle", 3),
    TX(393, 206, "GPT, LLaMA, Qwen", "tm", 11, "middle", 3),
    TX(393, 224, "무엇이든 생성", "tm", 11, "middle", 3),
    TX(240, 256, "어떤 마스크로 학습했느냐가 잘하는 일을 정해요", "tb", 14, "middle", 3),
)

# ---- p.18 인코더는 언어 모델이 될 수 없어요
FIG_NOLM = SVG(
    TX(240, 20, "인코더는 언어 모델로 학습할 수 없어요", "tb", 15),
    R(16, 96, 62, 30, "n", 1), TX(47, 116, "the", "tl", 12, "middle", 1),
    R(86, 96, 62, 30, "n", 1), TX(117, 116, "cat", "tl", 12, "middle", 1),
    R(156, 96, 62, 30, "n2", 1), TX(187, 116, "sat", "tl", 12, "middle", 1),
    R(226, 96, 62, 30, "n", 1), TX(257, 116, "on", "tl", 12, "middle", 1),
    R(296, 96, 62, 30, "n", 1), TX(327, 116, "the", "tl", 12, "middle", 1),
    R(366, 96, 62, 30, "n", 1), TX(397, 116, "mat", "tl", 12, "middle", 1),
    A(47, 90, 180, 92, "e", 2), A(117, 90, 183, 92, "e", 2),
    A(257, 90, 194, 92, "e", 2), A(327, 90, 197, 92, "e", 2), A(397, 90, 200, 92, "e", 2),
    TX(187, 148, "sat 을 맞혀 보세요", "tb", 13, "middle", 2),
    TX(240, 60, "양방향 어텐션: 모든 토큰이 서로를 봐요", "t", 12, "middle", 2),
    R(40, 172, 400, 40, "box2", 3),
    TX(240, 190, "그런데 sat 은 입력 안에 그대로 보여요", "tb", 13, "middle", 3),
    TX(240, 206, "정답이 보이면 배울 것이 없어요", "tb", 13, "middle", 3),
    TX(240, 240, "그래서 인코더는 다른 놀이가 필요해요: 가리고 되살리기", "t", 13, "middle", 3),
)

# ---- p.19 마스크 언어 모델
FIG_MLM = SVG(
    TX(240, 20, "15 퍼센트를 가리고 되돌려 놓기", "tb", 15),
    R(92, 40, 80, 28, "n2", 3), TX(132, 59, "went", "tl", 12, "middle", 3),
    R(300, 40, 80, 28, "n2", 3), TX(340, 59, "store", "tl", 12, "middle", 3),
    A(132, 96, 132, 72, "e2", 3), A(340, 96, 340, 72, "e2", 3),
    R(40, 100, 380, 36, "box2", 2), TX(230, 123, "트랜스포머 인코더", "tb", 14, "middle", 2),
    TX(450, 118, "가려진 자리에서만", "tm", 10, "middle", 3), TX(450, 132, "손실을 세요", "tm", 10, "middle", 3),
    R(40, 164, 66, 30, "n", 1), TX(73, 184, "I", "tl", 12, "middle", 1),
    R(114, 164, 90, 30, "n4", 1), TX(159, 184, "[MASK]", "tl", 12, "middle", 1),
    R(212, 164, 66, 30, "n", 1), TX(245, 184, "to", "tl", 12, "middle", 1),
    R(286, 164, 66, 30, "n", 1), TX(319, 184, "the", "tl", 12, "middle", 1),
    R(360, 164, 90, 30, "n4", 1), TX(405, 184, "[MASK]", "tl", 12, "middle", 1),
    A(73, 160, 73, 140, "e", 2), A(159, 160, 159, 140, "e", 2), A(245, 160, 245, 140, "e", 2),
    A(319, 160, 319, 140, "e", 2), A(405, 160, 405, 140, "e", 2),
    TX(240, 224, "빈칸을 채우려면 양쪽을 다 써야 해요", "tb", 14, "middle", 3),
    TX(240, 250, "그래서 양방향 뜻이 생겨요", "t", 13, "middle", 3),
)

# ---- p.20 80/10/10
FIG_801010 = SVG(
    TX(240, 20, "고른 토큰이 전부 [MASK] 가 되지는 않아요", "tb", 15),
    R(160, 38, 160, 30, "box", 1), TX(240, 58, "토큰의 15 퍼센트를 고름", "tb", 13, "middle", 1),
    A(230, 70, 96, 100, "e", 2), A(240, 70, 240, 100, "e", 2), A(250, 70, 384, 100, "e", 2),
    R(16, 104, 152, 78, "n4", 2), TX(92, 126, "80 퍼센트", "tb", 14, "middle", 2),
    TX(92, 146, "[MASK] 로 바꿈", "tl", 12, "middle", 2), TX(92, 168, "I [MASK] to the store", "tl", 11, "middle", 2),
    R(176, 104, 128, 78, "n4", 3), TX(240, 126, "10 퍼센트", "tb", 14, "middle", 3),
    TX(240, 146, "아무 토큰으로 바꿈", "tl", 12, "middle", 3), TX(240, 168, "I pizza to the store", "tl", 11, "middle", 3),
    R(312, 104, 152, 78, "n2", 4), TX(388, 126, "10 퍼센트", "tb", 14, "middle", 4),
    TX(388, 146, "그대로 둠", "tl", 12, "middle", 4), TX(388, 168, "I went to the store", "tl", 11, "middle", 4),
    R(40, 196, 400, 30, "box2", 5),
    TX(240, 216, "세 경우 모두 원래 낱말을 맞혀야 해요", "tb", 14, "middle", 5),
    TX(240, 248, "미세조정 때는 [MASK] 가 없으니 그것에 기대면 안 되니까요", "t", 12, "middle", 5),
)

# ---- p.23 한 인코더, 네 가지 과제 모양
FIG_SHAPES = SVG(
    TX(240, 20, "몸통은 하나, 헤드만 갈아 끼워요", "tb", 15),
    R(8, 36, 112, 180, "box", 1), TX(64, 56, "문장 하나", "tb", 13, "middle", 1),
    TX(64, 74, "감성, 주제", "tm", 11, "middle", 1),
    R(24, 88, 34, 22, "n2", 1), TX(41, 104, "헤드", "tl", 10, "middle", 1),
    TX(90, 104, "딱지 하나", "tm", 10, "middle", 1),
    R(16, 130, 96, 24, "n3", 1), TX(64, 147, "사전 학습 인코더", "tl", 10, "middle", 1),
    TX(64, 176, "[CLS] this movie", "tm", 10, "middle", 1),
    R(128, 36, 112, 180, "box", 2), TX(184, 56, "문장 쌍", "tb", 13, "middle", 2),
    TX(184, 74, "함의, 유사도", "tm", 11, "middle", 2),
    R(144, 88, 34, 22, "n2", 2), TX(161, 104, "헤드", "tl", 10, "middle", 2),
    TX(210, 104, "딱지 하나", "tm", 10, "middle", 2),
    R(136, 130, 96, 24, "n3", 2), TX(184, 147, "사전 학습 인코더", "tl", 10, "middle", 2),
    TX(184, 176, "[CLS] A [SEP] B", "tm", 10, "middle", 2),
    R(248, 36, 112, 180, "box", 3), TX(304, 56, "토큰 태깅", "tb", 13, "middle", 3),
    TX(304, 74, "개체명, 품사", "tm", 11, "middle", 3),
    R(258, 88, 20, 22, "n2", 3), R(282, 88, 20, 22, "n2", 3),
    R(306, 88, 20, 22, "n2", 3), R(330, 88, 20, 22, "n2", 3),
    TX(304, 122, "토큰마다 딱지 하나", "tm", 10, "middle", 3),
    R(256, 130, 96, 24, "n3", 3), TX(304, 147, "사전 학습 인코더", "tl", 10, "middle", 3),
    TX(304, 176, "[CLS] 서울 은 크다", "tm", 10, "middle", 3),
    R(368, 36, 112, 180, "box", 4), TX(424, 56, "스팬 추출", "tb", 13, "middle", 4),
    TX(424, 74, "추출형 질의응답", "tm", 11, "middle", 4),
    R(382, 88, 34, 22, "n2", 4), TX(399, 104, "시작", "tl", 10, "middle", 4),
    R(432, 88, 34, 22, "n2", 4), TX(449, 104, "끝", "tl", 10, "middle", 4),
    R(376, 130, 96, 24, "n3", 4), TX(424, 147, "사전 학습 인코더", "tl", 10, "middle", 4),
    TX(424, 176, "[CLS] 질문 [SEP] 글", "tm", 10, "middle", 4),
    R(40, 230, 400, 30, "box2", 4),
    TX(240, 250, "몸통은 늘 같은 내려받은 가중치예요", "tb", 14, "middle", 4),
)

S = []


def page(p, title, terms, p1, p2=(), p3=(), p4=()):
    S.append({"p": p, "title": title, "terms": list(terms),
              "pass1": list(p1), "pass2": list(p2), "pass3": list(p3), "pass4": list(p4)})


# ---------------------------------------------------------------- p.14
page(14, "글은 어디서 오나요",
     ["Corpus", "Pre-training", "BERT", "GPT", "RoBERTa", "Large Language Model (LLM)",
      "Label", "Self-Supervision", "Token"],
     [say(f"{PT}에 쓰는 글은 책, 위키백과, 그리고 인터넷 전체에서 와요.",
          "4년 사이에 글의 양이 약 400배 늘었어요.",
          f"{LB}을 안 붙여도 되니 글을 모으는 것만이 일이에요."),
      figure("4년, 400배", FIG_DATA, "막대 높이가 로그 눈금이라 한 칸이 10배예요.", 4)],
     [compare("슬라이드 영어와 우리말 뜻",
              ["영어 원문", "뜻"],
              ["Where Does the Data Come From?", "데이터는 어디서 오나요"],
              ["Books, Wikipedia, and then the open web", "책, 위키백과, 그다음은 열린 웹"],
              ["The amount of text grew about four hundred times in four years",
               "글의 양이 4년 만에 약 400배 늘었다"],
              ["four years, four hundred times more text", "4년, 400배 더 많은 글"],
              ["the recipe stopped being public around 2022", "2022년쯤부터 방법이 공개되지 않게 되었다"]),
      points("막대 네 개를 왼쪽부터",
             f"{GPT}-1: BooksCorpus, 8억 단어(0.8B)예요.",
             f"{BERT}: 거기에 위키백과를 더해 33억 단어(3.3B)예요.",
             f"{ROBERTA}: 웹 글을 더해 300억 단어(30B)예요.",
             f"{GPT}-3: CommonCrawl 로 3000억 단어(300B)예요. 대표적인 {LLM} 이에요."),
      points("오른쪽 목록이 알려 주는 것",
             f"{BERT}: BooksCorpus + English Wikipedia 예요.",
             f"{GPT}-1: BooksCorpus, 책 7000권이 넘는 {CORP}예요.",
             f"{GPT}-3: CommonCrawl, WebText, Wikipedia, 그리고 책 묶음 둘이에요.",
             "GPT-3.5 이후: undisclosed, 곧 공개하지 않는다는 뜻이에요.")],
     [look("슬라이드를 짚어 읽어요",
           (0.05, 0.19, 0.83, 0.05, "윗글: 책, 위키백과, 열린 웹. 4년 만에 약 400배."),
           (0.12, 0.36, 0.33, 0.04, "막대그래프 제목: 4년, 400배 더 많은 글."),
           (0.07, 0.39, 0.44, 0.31, "세로축이 log 눈금이에요. 한 칸 올라갈 때마다 10배예요."),
           (0.12, 0.40, 0.33, 0.28, "막대 위 숫자 0.8, 3.3, 30, 300 이 10억 단어 단위예요."),
           (0.53, 0.37, 0.36, 0.20, "오른쪽: BERT 와 GPT-1 이 쓴 말뭉치가 적혀 있어요."),
           (0.53, 0.58, 0.36, 0.14, "GPT-3 은 CommonCrawl 등이고, GPT-3.5 이후는 공개되지 않아요.")),
      steps("400배가 맞는지 계산해 봐요",
            ["가장 작은 막대는 GPT-1 의 0.8 (10억 단어 단위)이에요",
             "가장 큰 막대는 GPT-3 의 300 이에요",
             "300 나누기 0.8 을 해요",
             "300 / 0.8 = 375 예요",
             "슬라이드는 이것을 약 400배라고 적었어요"],
            "375배. 슬라이드의 'about four hundred times' 와 맞아요.",
            "0.8B 와 300B"),
      points("로그 눈금이 뭔가요",
             "세로축 눈금이 1, 10, 100, 1000 처럼 10배씩 뛰는 눈금이에요.",
             "값 차이가 아주 클 때 한 그림에 담으려고 써요.",
             f"0.8 과 300 은 375배 차이라서 보통 눈금으로는 막대가 안 보여요.",
             f"{SS} 덕분에 이만큼 큰 {CORP}도 {LB} 없이 쓸 수 있어요.")],
     [check("GPT-3 의 학습 글은 몇 단어라고 적혀 있나요?",
            ["3000억 단어", "300억 단어", "33억 단어", "8억 단어"], 0,
            "막대 위 숫자가 300 이고 단위가 10억 단어예요. 곧 3000억 단어예요."),
      english("답안 문장",
              f"{PT} {CORP}는 책과 위키백과에서 열린 웹으로 넓어졌고, 4년 만에 약 400배로 늘었다.",
              "'책 -> 위키백과 -> 웹' 순서와 '400배' 두 가지만 외워도 돼요."),
      warn("헷갈리기 쉬운 점",
           f"막대 높이는 로그 눈금이에요. 막대가 두 배로 보여도 실제로는 10배 차이일 수 있어요.",
           f"{TOK} 수가 아니라 단어 수로 적힌 숫자예요.")])

# ---------------------------------------------------------------- p.15
page(15, "그 데이터에는 대가가 따라와요",
     ["Corpus", "Memorization", "Bias", "Pre-training", "Label", "Self-Supervision",
      "World Knowledge", "Large Language Model (LLM)"],
     [say("인터넷에 있었다는 말과 학습에 써도 된다는 말은 같은 말이 아니에요.",
          "아직 답이 정해지지 않은 법과 윤리 문제예요.",
          "슬라이드는 문제를 세 가지로 나눠 놓았어요.")],
     [compare("슬라이드 영어와 우리말 뜻",
              ["영어 원문", "뜻"],
              ["The Data Has Consequences", "데이터에는 대가가 따른다"],
              ["'It was on the internet' and 'we were allowed to train on it'",
               "'인터넷에 있었다' 와 '학습에 써도 된다'"],
              ["are not the same sentence", "는 같은 말이 아니다"],
              ["an open legal and ethical question, not a settled one",
               "아직 열려 있는 법적, 윤리적 문제이지 정리된 문제가 아니다"]),
      points("세 카드의 뜻",
             f"Copyright(저작권): BooksCorpus 는 긁어모은 전자책이었어요. 누가 동의했나요.",
             f"Memorisation({MEMO}): 모델이 학습 글을 그대로 다시 뱉을 수 있어요. 개인 정보도요.",
             f"Bias({BIAS}): 글에 들어 있던 것은 무엇이든 모델에 남아요."),
      points("PII 가 뭔가요",
             "Personally Identifiable Information, 곧 개인을 알아볼 수 있는 정보예요.",
             "이름, 전화번호, 주소 같은 것이에요.",
             f"{CORP}에 섞여 들어가면 {MEMO}를 통해 다시 나올 수 있어요.")],
     [look("슬라이드를 짚어 읽어요",
           (0.05, 0.19, 0.90, 0.10, "윗글: '인터넷에 있었다' 와 '학습에 써도 된다' 는 같은 말이 아니다."),
           (0.09, 0.45, 0.27, 0.24, "첫 카드 Copyright. 긁어모은 전자책에 누가 동의했느냐는 물음이에요."),
           (0.37, 0.45, 0.27, 0.24, "둘째 카드 Memorisation. 학습 글을 그대로 재현할 수 있어요."),
           (0.65, 0.45, 0.27, 0.24, "셋째 카드 Bias. 글에 있던 치우침이 모델에 그대로 남아요."),
           (0.26, 0.70, 0.48, 0.04, "맨 아래 기울임 글이 이 쪽의 한 줄 요약이에요.")),
      points("왜 이 문제가 5주차에 나오나요",
             f"{SS}은 인터넷 글을 전부 학습 데이터로 바꿔 주었어요. 그게 힘이자 문제예요.",
             f"{LB}을 안 붙여도 된다는 말은 '아무 글이나 써도 된다' 는 말이 아니에요.",
             f"{LLM} 이 커질수록 {CORP}도 커지고 문제도 커져요."),
      bg("기초 다지기 5단원", f"{MEMO}와 일반화는 달라요.",
         "일반화는 규칙을 배우는 것이고, 암기는 본 것을 그대로 저장하는 것이에요.",
         f"{PT} 중에는 둘 다 일어나요. N5 p.43 에서 다시 다뤄요."),
      points("이 쪽과 이어지는 곳",
             f"{PT}이 무엇을 가르치는지는 N5 p.42 에서 정리해요.",
             f"{MEMO} 문제는 N5 p.43 에서 더 자세히 봐요.",
             f"{BIAS}은 2주차 N2 p.49 에서 단어 벡터의 사회적 {BIAS}으로 이미 한 번 나왔어요.",
             f"글 안에 있던 {WK}도 함께 들어와요. 좋은 것과 나쁜 것이 같이 와요.",
             f"{WK}은 N5 p.42 에서 사전 학습이 가르친 것으로 다시 나와요.")],
     [check("슬라이드가 든 세 가지 문제는?",
            ["저작권, 암기, 편향", "속도, 비용, 정확도",
             "토큰화, 임베딩, 어텐션", "과적합, 과소적합, 정규화"], 0,
            "Copyright, Memorisation, Bias 세 카드예요."),
      english("답안 문장",
              f"{PT} {CORP}에는 저작권, {MEMO}, {BIAS} 문제가 따라오며, 아직 정리되지 않은 법적, 윤리적 문제다.",
              "세 낱말 '저작권, 암기, 편향' 을 순서대로 외워요."),
      warn("헷갈리기 쉬운 점",
           f"여기서 {BIAS}은 사회적 치우침을 말해요. 신경망의 bias 항(편향 항)과 다른 말이에요.",
           "슬라이드는 이 문제에 답을 주지 않아요. 열린 문제라고만 말해요.")])

# ---------------------------------------------------------------- p.16
page(16, "2단원 구역 표지: Encoders: BERT",
     ["Encoder", "BERT", "Bidirectional Context", "Masked Language Modelling (MLM)"],
     [say("2단원이 시작돼요. 제목은 Encoders: BERT 예요.",
          f"{ENC} 쪽 이야기, 곧 {BERT} 예요.",
          f"부제 bidirectional context and the masked language model 은",
          f"'{BC}과 {MLM}' 이라는 뜻이에요.")],
     [], [], [])

# ---------------------------------------------------------------- p.17
page(17, "세 구조, 세 가지 목적 함수",
     ["Encoder", "Decoder", "Transformer", "Self-Attention", "Causal Masking",
      "Masked Language Modelling (MLM)", "Span Corruption", "Span", "Denoising",
      "Next Token Prediction", "BERT", "GPT", "T5", "RoBERTa", "Bidirectional Context",
      "Large Language Model (LLM)", "Classification", "Token Tagging"],
     [say("4주차에서 인코더는 양쪽을 다 보고 디코더는 앞만 본다고 배웠죠.",
          f"그 차이가 5주차에서 {BERT}와 {GPT}로 갈려요. 이 쪽이 바로 그 갈림길이에요.",
          f"학습할 때 씌운 마스크가 볼 수 있는 것을 정하고, 볼 수 있는 것이 목적 함수를 정해요."),
      figure("세 구조 한눈에", FIG_3ARCH, "격자가 마스크예요. 꽉 찬 격자는 다 보이는 것, 계단 격자는 앞만 보이는 것이에요.", 3)],
     [compare("세 구조를 한 표로",
              ["구조", "볼 수 있는 것", "사전 학습 목적 함수", "대표 모델"],
              [f"{ENC}", f"문장 전체, {BC}", f"{MLM}", "BERT, RoBERTa, KLUE-BERT"],
              ["인코더 디코더", "읽을 때는 양쪽, 쓸 때는 앞만", f"{SPC}({DEN})", "T5, BART, mT5"],
              [f"{DEC}", f"앞에 나온 것만, {CM}", f"{NTP}", "GPT, LLaMA, Qwen"]),
      points("슬라이드 영어와 우리말 뜻",
             "The mask you use during pretraining decides what the model can see = 사전 학습에 쓴 마스크가 모델이 볼 수 있는 것을 정한다",
             "which decides what objective is even possible = 그것이 어떤 목적 함수가 가능한지를 정한다",
             "which decides what the model is good at = 그것이 모델이 무엇을 잘하는지를 정한다",
             "the mask you train with decides what the model is good for = 학습에 쓴 마스크가 쓸모를 정한다"),
      points("맨 아래 줄의 쓸모",
             f"{ENC}: classify, tag, retrieve, 곧 {CLSF}, {TT}, 검색이에요.",
             "인코더 디코더: translate, summarise, 곧 번역과 요약이에요.",
             f"{DEC}: generate anything, 곧 무엇이든 생성이에요. 요즘 {LLM} 이 여기에 있어요.")],
     [look("슬라이드를 짚어 읽어요",
           (0.05, 0.19, 0.90, 0.10, "윗글: 마스크가 볼 수 있는 것을, 볼 수 있는 것이 목적 함수를, 목적 함수가 잘하는 일을 정한다."),
           (0.17, 0.34, 0.20, 0.06, "왼쪽 파란 칸이 인코더예요."),
           (0.17, 0.40, 0.20, 0.11, "격자가 꽉 차 있어요. 모든 토큰이 모든 토큰을 본다는 뜻이에요."),
           (0.58, 0.40, 0.20, 0.11, "오른쪽 보라 칸의 격자는 계단 모양이에요. 뒤쪽이 비어 있죠. 인과 마스킹이에요."),
           (0.38, 0.40, 0.20, 0.11, "가운데는 격자가 둘이에요. 인코더 쪽은 꽉 차고 디코더 쪽은 계단이에요."),
           (0.17, 0.63, 0.61, 0.10, "가운데 줄이 사전 학습 목적 함수예요. 마스크 언어 모델, 스팬 손상, 다음 토큰 예측.")),
      points("4주차 어디를 다시 보면 되나요",
             f"{ENC} 블록과 {DEC} 블록의 갈림길: N4 p.52-53 이에요. 오늘 그것이 값을 하는 자리예요.",
             f"{CM}: N4 p.43 이에요. 계단 격자가 바로 그 그림이에요.",
             f"{SA}과 마스크가 어떻게 만나는지: N4 p.40-43 이에요.",
             "인코더 디코더 스택의 원문 그림은 논문 덱 NP p.3 에서 봐요. 여기서는 되풀이하지 않아요."),
      points("각 목적 함수를 한 줄로",
             f"{MLM}: 토큰 일부를 가리고 원래 낱말을 맞혀요. N5 p.19 에서 자세히 봐요.",
             f"{SPC}: 이어진 {SPAN}을 통째로 지우고 되살려요. {DEN}의 한 가지예요. N5 p.37 에서 봐요.",
             f"{NTP}: 앞을 보고 다음 토큰을 맞혀요. 3주차에 배운 그대로예요. N5 p.30 에서 봐요."),
      bg("기초 다지기 3단원", "마스크 격자는 가로세로 모두 토큰 자리예요.",
         "r 번째 줄 c 번째 칸이 칠해져 있으면, r 번 토큰이 c 번 토큰을 볼 수 있다는 뜻이에요.",
         "꽉 찬 격자는 전부 보임, 아래 삼각형만 칠해진 격자는 앞만 보임이에요.")],
     [check("인코더의 사전 학습 목적 함수는?",
            ["마스크 언어 모델", "다음 토큰 예측", "스팬 손상", "다음 문장 예측만"], 0,
            "슬라이드 인코더 칸에 masked language modelling 이라고 적혀 있어요."),
      check("계단 모양 마스크 격자를 쓰는 구조는?",
            ["디코더", "인코더", "임베딩 층", "과제 헤드"], 0,
            f"뒤를 못 보게 막는 것이 {CM}이고, 디코더가 씁니다. 4주차 N4 p.43 에서 배웠어요."),
      english("답안 문장",
              f"{ENC}는 {MLM}으로 {PT}한다.",
              f"인코더 디코더는 {SPC}, {DEC}는 {NTP}으로 해요.",
              "세 구조와 세 목적 함수를 짝지어 한 줄로 외워요. 시험에 나오기 딱 좋은 표예요."),
      warn("헷갈리기 쉬운 점",
           f"구조가 달라서 목적 함수가 다른 게 아니에요. 마스크가 달라서 가능한 목적 함수가 달라져요.",
           f"KLUE-BERT 는 한국어 {BERT}예요. {ROBERTA}와 함께 인코더 쪽 대표로 적혀 있어요.")])

# ---------------------------------------------------------------- p.18
page(18, "인코더는 왜 언어 모델이 될 수 없나요",
     ["Encoder", "Decoder", "Language Model (LM)", "Next Token Prediction", "Causal Masking",
      "Self-Attention", "Bidirectional Context", "Autoregressive", "Masked Language Modelling (MLM)",
      "Token", "BERT", "GPT", "Loss Function"],
     [say(f"{ENC}는 모든 토큰이 모든 토큰을 봐요. 이게 {BC}이에요.",
          f"그런데 그러면 '다음 낱말 맞히기' 가 문제가 되지 않아요. 답이 이미 입력에 보여요.",
          f"그래서 {ENC}는 다른 놀이가 필요해요."),
      analogy("휴대폰 자판의 다음 낱말 추천",
              "자판 추천은 지금까지 친 글자만 보고 다음 낱말을 골라요. 그런데 다음 낱말이 화면에 이미 떠 있다면 추천이 의미가 없죠.",
              ("지금까지 친 글자만 보임", f"{DEC}의 {CM}"),
              ("다음 낱말이 이미 화면에 보임", f"{ENC}의 {BC}"),
              ("추천이 의미가 없어짐", f"{ENC}로는 {NTP}을 학습할 수 없음")),
      figure("정답이 입력에 보여요", FIG_NOLM, "sat 을 맞히라고 해도 sat 이 입력에 그대로 있어요.", 3)],
     [compare("슬라이드 영어와 우리말 뜻",
              ["영어 원문", "뜻"],
              ["If every token can attend to every other token", "모든 토큰이 다른 모든 토큰을 볼 수 있다면"],
              ["'predict the next word' is not a task", "'다음 낱말 맞히기' 는 과제가 되지 않는다"],
              ["the answer is already visible in the input", "답이 이미 입력에 보인다"],
              ["The model learns nothing", "모델이 아무것도 배우지 않는다"],
              ["so encoders need a different game: hide part of the input, then reconstruct it",
               "그래서 인코더는 다른 놀이가 필요하다. 입력 일부를 가리고 되살리기"]),
      points("4주차 인과 마스킹과 무엇이 다른가요",
             f"{CM}(N4 p.43): 뒤쪽을 아예 못 보게 막아요. 그래서 {NTP}이 진짜 문제가 돼요.",
             f"{MLM}: 뒤쪽은 보이지만 가운데 한 자리를 [MASK] 로 바꿔 숨겨요.",
             f"앞의 것은 '방향' 을 막는 마스크, 뒤의 것은 '자리' 를 가리는 마스크예요. 이름이 비슷하지만 다른 일이에요."),
      points("그림을 짚어 읽어요",
             "the, cat, sat, on, the, mat 여섯 토큰이 나란히 있어요.",
             "화살표가 sat 으로 모여요. 앞뒤 토큰이 모두 sat 을 본다는 뜻이에요.",
             f"그런데 sat 자체도 입력에 들어 있어요. 그래서 {LOSS}가 0 으로 쉽게 내려가요.")],
     [look("슬라이드를 짚어 읽어요",
           (0.05, 0.19, 0.90, 0.05, "윗글: 모든 토큰이 서로를 보면 다음 낱말 맞히기는 과제가 되지 않는다."),
           (0.16, 0.33, 0.58, 0.06, "큰 제목과 부제: 양방향 어텐션, 모든 토큰이 서로를 본다."),
           (0.13, 0.53, 0.48, 0.07, "여섯 토큰 상자. 가운데 sat 만 빨간 테두리예요."),
           (0.27, 0.47, 0.34, 0.06, "휘어진 화살표들이 앞뒤 토큰에서 sat 으로 들어와요."),
           (0.63, 0.47, 0.28, 0.20, "오른쪽 빨간 상자: 답이 입력에 있어서 모델이 아무것도 배우지 않는다."),
           (0.24, 0.72, 0.52, 0.04, "맨 아래: 인코더는 다른 놀이가 필요하다. 가리고 되살리기.")),
      points("자기회귀와 비교해요",
             f"{AR}는 자기가 만든 앞부분을 다시 넣으며 한 토큰씩 이어 가는 방식이에요.",
             f"{DEC}({GPT})가 이렇게 글을 써요. {CM} 덕분에 가능해요.",
             f"{ENC}({BERT})는 {AR}가 아니에요. 빈칸을 한 번에 채우고 끝이에요."),
       bg("기초 다지기 6단원", f"{LOSS}는 틀린 정도를 매기는 벌점이에요.",
          "정답이 입력에 보이면 모델은 그 자리를 그대로 복사만 해도 벌점이 0 이 돼요.",
          "벌점이 0 이면 가중치가 움직이지 않아요. 곧 아무것도 배우지 않아요.")],
     [check("인코더를 다음 토큰 예측으로 학습시키면 어떻게 되나요?",
            ["정답이 입력에 보여서 아무것도 배우지 않아요", "학습이 아주 느려져요",
             "메모리가 모자라요", "토큰화가 틀려요"], 0,
            "the answer is already visible in the input. The model learns nothing."),
      check("BERT 의 마스킹과 4주차의 인과 마스킹의 차이는?",
            ["인과 마스킹은 뒤쪽 방향을 막고, BERT 는 특정 자리를 가린다",
             "둘은 같은 것이다",
             "인과 마스킹은 학습에만, BERT 마스킹은 추론에만 쓴다",
             "인과 마스킹은 토큰을 지우고 BERT 는 문장을 지운다"], 0,
            "N4 p.43 의 인과 마스킹은 미래 방향을 막아요. BERT 는 뒤를 보게 두고 가운데 자리를 [MASK] 로 바꿔요."),
      english("답안 문장",
              f"{ENC}는 {BC}이라 다음 낱말이 입력에 보이므로 {NTP}으로 학습할 수 없다.",
              f"그래서 일부를 가리고 되살리는 {MLM}을 대신 써요.",
              "'답이 보인다 -> 과제가 안 된다 -> 가리고 되살린다' 세 걸음이에요."),
      warn("헷갈리기 쉬운 점",
           f"{ENC}가 못한다는 것은 {LM}으로 '학습' 하는 것이에요. 문장을 이해하는 일은 아주 잘해요.",
           f"{MLM}도 넓게 보면 {LM}의 한 종류예요. 다만 {NTP}은 아니에요.")])

# ---------------------------------------------------------------- p.19
page(19, "마스크 언어 모델",
     ["Masked Language Modelling (MLM)", "[MASK]", "Token", "Encoder", "BERT",
      "Bidirectional Context", "Loss Function", "Self-Supervision", "Label",
      "Transformer", "Pre-training"],
     [say(f"{BERT}의 학습 방법이에요. {TOK}의 15 퍼센트를 {MASK}로 바꾸고 되돌려 놓게 해요.",
          f"{LOSS}는 가려진 자리에서만 세요. 나머지 자리는 벌점을 안 매겨요.",
          f"{BERT}는 Bi-Directional Encoder Representations from Transformers 의 줄임말이에요."),
      analogy("빈칸 채우기 시험지",
              "국어 시험의 빈칸 채우기와 똑같아요. 앞뒤를 다 읽어야 가운데가 채워지고, 채점은 빈칸 자리만 해요.",
              ("빈칸 뚫린 시험지", f"{MASK}로 바뀐 {TOK} 자리"),
              ("앞뒤를 다 읽고 고르기", BC),
              ("빈칸 자리만 채점", f"가려진 자리에서만 {LOSS}를 셈")),
      figure("가리고 되돌려 놓기", FIG_MLM, "I [MASK] to the [MASK] 에서 went 와 store 를 되살려요.", 3)],
     [compare("슬라이드 영어와 우리말 뜻",
              ["영어 원문", "뜻"],
              ["Replace 15% of the tokens with [MASK]", "토큰의 15 퍼센트를 [MASK] 로 바꾼다"],
              ["and train the model to put them back", "그리고 모델이 그것을 되돌려 놓게 학습시킨다"],
              ["The loss is computed only on the masked positions", "손실은 가려진 자리에서만 계산한다"],
              ["hide 15% of the tokens, then put them back", "토큰의 15 퍼센트를 숨기고 되돌려 놓기"],
              ["to fill a blank the model has to use both sides",
               "빈칸을 채우려면 모델은 양쪽을 다 써야 한다"]),
      points("BERT 라는 이름 풀이",
             "Bi-Directional = 양방향, 곧 앞뒤를 다 본다는 뜻이에요.",
             "Encoder Representations = 인코더가 만든 표현(벡터)이라는 뜻이에요.",
             "from Transformers = 트랜스포머에서 나왔다는 뜻이에요.",
             f"이름 전체가 이미 '양방향 {ENC}' 라고 말하고 있어요."),
      points("그림을 아래부터 위로",
             f"맨 아래 input: I, {MASK}, to, the, {MASK} 다섯 자리예요.",
             f"가운데: {TRF} {ENC}가 다섯 자리를 한꺼번에 읽어요.",
             "맨 위 predict: 가려졌던 두 자리에서만 went 와 store 를 내놓아요.",
             f"오른쪽 글: loss only on the masked positions, 곧 가려진 자리에서만 {LOSS}를 세요.")],
     [look("슬라이드를 짚어 읽어요",
           (0.05, 0.19, 0.87, 0.10, "윗글: 토큰의 15 퍼센트를 [MASK] 로 바꾸고 되돌려 놓게 한다. 손실은 가려진 자리에서만."),
           (0.24, 0.33, 0.52, 0.05, "큰 제목: 토큰의 15 퍼센트를 숨기고 되돌려 놓기."),
           (0.34, 0.43, 0.09, 0.06, "맨 위 초록 상자 went. 가려졌던 자리의 정답이에요."),
           (0.24, 0.53, 0.48, 0.07, "가운데 파란 띠가 트랜스포머 인코더예요. 다섯 자리를 한꺼번에 읽어요."),
           (0.25, 0.63, 0.47, 0.07, "맨 아래 입력. 주황 상자 둘이 [MASK] 예요."),
           (0.73, 0.53, 0.10, 0.06, "오른쪽 글: 손실은 가려진 자리에서만 계산해요."),
           (0.16, 0.81, 0.68, 0.05, "맨 아래 줄이 BERT 이름 풀이예요.")),
      steps("100 토큰짜리 문장이면 몇 자리가 가려지나요",
            ["문장의 토큰 수가 100 개라고 해요",
             "15 퍼센트를 골라요. 100 x 0.15 = 15 자리예요",
             "이 15 자리에서만 벌점을 세요",
             "나머지 100 - 15 = 85 자리는 벌점을 안 세요",
             "그래서 한 문장에서 배우는 문제가 15 개인 셈이에요"],
            f"15 자리. 이것이 '{LOSS}는 가려진 자리에서만' 의 뜻이에요.",
            "토큰 100 개, 15 퍼센트"),
      points("왜 하필 양쪽을 다 보나요",
             "I ___ to the store 에서 빈칸을 채우려면 뒤의 store 를 봐야 해요.",
             "앞의 I 만 보면 went, drove, walked 어느 것이든 되니까요.",
             f"그래서 {MLM}이 {BC}을 가르쳐요. 이것이 {ENC}의 힘이에요."),
      bg("기초 다지기 6단원", f"{LOSS}는 정답 확률의 -log 를 벌점으로 매겨요(교차 엔트로피).",
         f"가려진 자리에서만 센다는 말은, 그 자리의 소프트맥스 출력만 벌점 계산에 넣는다는 뜻이에요.")],
     [check("마스크 언어 모델에서 손실을 계산하는 자리는?",
            ["가려진 자리에서만", "모든 자리에서", "마지막 자리에서만", "[CLS] 자리에서만"], 0,
            "The loss is computed only on the masked positions."),
      english("답안 문장",
              f"{MLM}은 {TOK}의 15 퍼센트를 {MASK}로 바꾸고 원래 낱말을 맞히게 한다.",
              f"{LOSS}는 가려진 자리에서만 계산해요.",
              "'15 퍼센트 + 되돌려 놓기 + 가려진 자리에서만' 세 조각이에요."),
      exam("예상 문제",
           "Why does masked language modelling force the model to use both left and right context?",
           f"{MLM}이 왜 앞뒤 문맥을 모두 쓰게 만드는지 설명하세요.",
           [f"가려지는 자리가 문장 어디에나 올 수 있어요.",
            "가운데가 가려지면 앞만 봐서는 후보가 너무 많아요.",
            "뒤쪽 낱말이 힌트를 주기 때문에 뒤도 봐야 해요.",
            f"그래서 {ENC}의 {BC}이 꼭 필요해요."],
           f"빈칸이 문장 가운데에 오기 때문에 앞뒤를 모두 봐야 맞힐 수 있고, 그래서 {MLM}이 {BC}을 학습시킨다."),
      warn("헷갈리기 쉬운 점",
           f"15 퍼센트는 '고르는 비율' 이에요. 고른 것이 전부 {MASK}가 되는 것은 아니에요.",
           "그 이야기가 바로 다음 쪽의 80/10/10 이에요.")])

# ---------------------------------------------------------------- p.20
page(20, "80/10/10 요령",
     ["[MASK]", "Token", "Masked Language Modelling (MLM)", "Finetuning", "Pre-training",
      "Loss Function", "BERT", "Label", "Encoder"],
     [say(f"고른 15 퍼센트가 전부 {MASK}로 바뀌지는 않아요.",
          f"80 퍼센트만 {MASK}가 되고, 10 퍼센트는 아무 {TOK}으로, 10 퍼센트는 그대로 둬요.",
          "세 경우 모두 원래 낱말을 맞혀야 해요."),
      figure("고른 토큰이 가는 세 갈래", FIG_801010,
             "80 퍼센트는 [MASK], 10 퍼센트는 무작위 토큰, 10 퍼센트는 그대로예요.", 5)],
     [compare("슬라이드 영어와 우리말 뜻",
              ["영어 원문", "뜻"],
              ["Of the 15% chosen, only 80% actually become [MASK]",
               "고른 15 퍼센트 중 실제로 [MASK] 가 되는 것은 80 퍼센트뿐이다"],
              ["The other 20% look untouched", "나머지 20 퍼센트는 손대지 않은 것처럼 보인다"],
              ["but the model must still predict them", "그런데 모델은 여전히 그것을 맞혀야 한다"],
              ["in all three cases the model must still predict the original word",
               "세 경우 모두 원래 낱말을 맞혀야 한다"],
              ["at finetuning time there are no [MASK] tokens",
               "미세조정 때는 [MASK] 토큰이 없다"]),
      points("세 갈래를 슬라이드 예문으로",
             f"80 퍼센트: {MASK}로 바꿔요. I [MASK] to the store 가 돼요.",
             "10 퍼센트: 아무 토큰으로 바꿔요. I pizza to the store 가 돼요.",
             "10 퍼센트: 그대로 둬요. I went to the store 그대로예요.",
             "셋 다 정답은 went 예요."),
      points("왜 이런 번거로운 일을 하나요",
             f"{PT} 때는 {MASK}가 있지만 {FT} 때는 없어요.",
             f"{MASK}만 보고 일하도록 배우면 {FT}에서 갑자기 낯선 입력을 만나요.",
             f"그래서 멀쩡해 보이는 자리도 의심하도록 가르치는 거예요.")],
     [look("슬라이드를 짚어 읽어요",
           (0.05, 0.19, 0.90, 0.05, "윗글: 고른 15 퍼센트 중 80 퍼센트만 [MASK] 가 되고 나머지 20 퍼센트는 멀쩡해 보인다."),
           (0.32, 0.32, 0.36, 0.04, "큰 제목: 고른 토큰이 전부 [MASK] 가 되지는 않는다."),
           (0.38, 0.38, 0.24, 0.06, "맨 위 회색 상자: 토큰의 15 퍼센트를 고른다."),
           (0.10, 0.49, 0.24, 0.19, "왼쪽 80 퍼센트: [MASK] 로 바꾼다. 예문 I [MASK] to the store."),
           (0.38, 0.49, 0.24, 0.19, "가운데 10 퍼센트: 아무 토큰으로 바꾼다. 예문 I pizza to the store."),
           (0.65, 0.49, 0.24, 0.19, "오른쪽 10 퍼센트: 그대로 둔다. 예문 I went to the store.")),
      steps("토큰 1000 개짜리 글이면 몇 개씩인가요",
            ["전체 토큰이 1000 개예요",
             "먼저 15 퍼센트를 골라요. 1000 x 0.15 = 150 개예요",
             "그중 80 퍼센트가 [MASK] 예요. 150 x 0.8 = 120 개예요",
             "10 퍼센트가 무작위 토큰이에요. 150 x 0.1 = 15 개예요",
             "남은 10 퍼센트는 그대로예요. 150 - 120 - 15 = 15 개예요",
             "손실을 세는 자리는 120 + 15 + 15 = 150 개 전부예요"],
            f"120 / 15 / 15. {LOSS}는 고른 150 자리 전부에서 세요.",
            "토큰 1000 개, 15 퍼센트, 80/10/10"),
      points("한 번 더 정리해요",
             f"15 퍼센트는 '고르는' 비율이고, 80/10/10 은 '고른 것을 어떻게 바꾸는지' 예요.",
             f"{MASK}로 바뀌지 않은 30 개도 정답을 맞혀야 해요.",
             f"그래서 {ENC}는 모든 자리를 늘 제대로 읽으려고 애써요.")],
     [check("고른 토큰 중 아무 토큰으로 바뀌는 비율은?",
            ["10 퍼센트", "80 퍼센트", "15 퍼센트", "20 퍼센트"], 0,
            "80 / 10 / 10 중 가운데가 replace with a random token 이에요."),
      check("80/10/10 을 쓰는 이유로 맞는 것은?",
            ["미세조정 때는 [MASK] 가 없어서 그것에만 기대면 안 되니까",
             "학습 속도를 올리려고", "메모리를 아끼려고", "토큰화를 쉽게 하려고"], 0,
            "at finetuning time there are no [MASK] tokens - the model must not rely on seeing one."),
      english("답안 문장",
              f"고른 15 퍼센트 중 80 퍼센트는 {MASK}로, 10 퍼센트는 무작위 {TOK}으로 바꾸고 10 퍼센트는 그대로 두며, 세 경우 모두 원래 낱말을 맞혀야 한다.",
              "'80/10/10, 셋 다 원래 낱말' 이 답안의 뼈대예요."),
      warn("헷갈리기 쉬운 점",
           f"80/10/10 은 전체 {TOK}의 비율이 아니라 고른 15 퍼센트 안에서의 비율이에요.",
           f"전체로 보면 {MASK}가 되는 것은 15 x 0.8 = 12 퍼센트예요.")])

# ---------------------------------------------------------------- p.21
page(21, "두 번째 목적 함수: 다음 문장 예측",
     ["Next Sentence Prediction (NSP)", "[CLS]", "[SEP]", "BERT", "RoBERTa", "Label",
      "Supervised Learning", "Masked Language Modelling (MLM)", "Sentence Pair",
      "Self-Supervision", "Pre-training", "Encoder"],
     [say(f"{BERT}는 {MLM} 말고 하나를 더 학습했어요.",
          f"문장 B 가 정말 문장 A 다음에 오는 문장인지 맞히는 {NSP}이에요.",
          "문장과 문장 사이의 관계를 가르치려는 생각이었어요."),
      points("두 가지 답만 있어요",
             f"IsNext: 문장 B 가 문장 A 바로 다음 문장이에요.",
             f"NotNext: 문장 B 는 아무 데서나 가져온 문장이에요.",
             f"답이 둘뿐이니 {LB}이 IsNext 와 NotNext 두 가지예요.")],
     [compare("슬라이드 영어와 우리말 뜻",
              ["영어 원문", "뜻"],
              ["BERT also trained on a binary task", "BERT 는 이지선다 과제로도 학습했다"],
              ["does sentence B actually follow sentence A?", "문장 B 가 정말 문장 A 다음에 오는가"],
              ["The idea was to teach discourse-level relations", "문장 사이의 관계를 가르치려는 생각이었다"],
              ["RoBERTa later removed it and did better", "RoBERTa 가 나중에 그것을 빼고 더 잘했다"],
              ["not every good idea survives an ablation",
               "좋아 보이는 생각이 전부 제거 실험을 견디지는 않는다"]),
      points("슬라이드 예문 두 줄",
             f"{CLS} the man went to the store {SEP} + he bought a gallon of milk {SEP} -> IsNext",
             f"{CLS} the man went to the store {SEP} + penguins are flightless birds {SEP} -> NotNext",
             f"{CLS}는 맨 앞에 붙는 요약 자리, {SEP}는 문장을 가르는 표시예요."),
      points("ablation 이 뭔가요",
             "제거 실험이에요. 어떤 부분을 빼 보고 성능이 어떻게 되는지 재는 것이에요.",
             f"{ROBERTA}가 {NSP}을 빼 봤더니 오히려 더 좋았어요.",
             "곧 그 부분이 도움이 안 되었다는 뜻이에요.")],
     [look("슬라이드를 짚어 읽어요",
           (0.05, 0.19, 0.88, 0.05, "윗글: BERT 는 문장 B 가 문장 A 다음에 오는지 맞히는 이지선다 과제로도 학습했다."),
           (0.23, 0.31, 0.54, 0.04, "큰 제목: 두 번째 목적 함수, 문장 B 가 문장 A 를 따라오나요."),
           (0.10, 0.42, 0.38, 0.07, "왼쪽 회색 상자가 문장 A 예요. [CLS] 로 시작해 [SEP] 로 끝나요."),
           (0.48, 0.42, 0.30, 0.07, "가운데 초록 상자가 문장 B 예요. 정답은 IsNext."),
           (0.48, 0.54, 0.30, 0.07, "아래 줄의 빨간 문장 B 는 관계없는 문장이라 NotNext 예요."),
           (0.10, 0.64, 0.82, 0.12, "맨 아래 파란 상자: RoBERTa 가 이것을 빼고 더 잘했다는 말이에요.")),
      points("자기 지도 학습이 맞나요",
             f"맞아요. IsNext 와 NotNext {LB}을 사람이 붙이지 않아요.",
             f"문서에서 이어진 두 문장을 뽑으면 IsNext, 아무 데서나 뽑으면 NotNext 예요.",
             f"그래서 {NSP}도 {SS}이에요. {PT}은 전부 이 방식이에요."),
      points("이 쪽이 시험에 나오는 이유",
             f"'{PT}의 목적 함수를 말하라' 는 문제에서 {BERT}는 두 개라고 답해야 해요.",
             f"{MLM}과 {NSP} 두 개예요.",
             f"그리고 {ROBERTA}가 {NSP}을 뺐다는 사실까지 붙이면 좋아요. N5 p.26 에서 다시 나와요.")],
     [check("RoBERTa 가 NSP 를 빼고 얻은 결과는?",
            ["더 좋아졌다", "더 나빠졌다", "똑같았다", "학습이 안 되었다"], 0,
            "RoBERTa later removed it and did better. 제거 실험을 읽는 법을 알려 주는 예예요."),
      english("답안 문장",
              f"{BERT}는 {MLM}과 {NSP} 두 가지 목적 함수로 학습했다.",
              f"{NSP}은 문장 B 가 문장 A 다음에 오는지 맞히는 과제예요.",
              f"{BERT}의 목적 함수는 두 개라는 점을 꼭 적어요."),
      warn("헷갈리기 쉬운 점",
           f"{NSP}은 {SL}처럼 보이지만 사람이 {LB}을 붙이지 않아요. 문서 순서가 곧 정답이에요.",
           f"{NSP}은 문장을 이어 쓰는 과제가 아니에요. 이어지는지 아닌지 맞히는 {SPAIR} 과제예요.")])

# ---------------------------------------------------------------- p.22
page(22, "숫자로 보는 BERT",
     ["BERT", "Parameter", "Head", "Hidden Size", "Corpus", "Pre-training", "Finetuning",
      "Transfer Learning", "Supervised Learning", "Transformer", "Encoder", "Token"],
     [say(f"{BERT}는 크기가 두 가지예요. base 와 large 예요.",
          f"{CORP}는 수십억 단어, {PT}에는 TPU 칩 64개로 4일이 걸렸어요.",
          f"우리는 이 앞 절반을 절대 다시 하지 않아요. 그럴 필요도 없어요."),
      points("표를 한 줄로",
             f"BERT-base: 층 12, {HID} 768, {HEAD} 12, {PARAM} 110M 이에요.",
             f"BERT-large: 층 24, {HID} 1024, {HEAD} 16, {PARAM} 340M 이에요.",
             f"우리가 실습에서 쓰는 것은 base 크기예요.")],
     [compare("BERT-base 와 BERT-large",
              ["항목", "BERT-base", "BERT-large"],
              ["층(layers)", "12", "24"],
              [f"{HID}(hidden)", "768", "1024"],
              [f"{HEAD}(heads)", "12", "16"],
              [f"{PARAM}(parameters)", "110M", "340M"]),
      points("슬라이드 영어와 우리말 뜻",
             "Two sizes, a few billion words, and four days on 64 TPUs = 두 가지 크기, 수십억 단어, 64개 TPU 로 4일",
             "You will never repeat the first half = 앞 절반은 절대 다시 하지 않는다",
             "and you never need to = 그럴 필요도 없다",
             "pretrain once, finetune many times = 한 번 사전 학습, 여러 번 미세조정",
             "you download the first half and only pay for the second = 앞 절반은 내려받고 뒤 절반만 치른다"),
      points("비용 두 줄",
             f"{PT} 비용: TPU 칩 64개로 4일이에요. GPU 한 장으로 할 일이 아니에요.",
             f"{FT} 비용: GPU 한 장으로 몇 분에서 몇 시간이에요. 우리가 실습에서 할 일이에요.",
             f"이 비용 차이가 {TL}이 이긴 이유예요.",
             f"앞 절반을 내려받아 쓰는 것, 그게 {TL}이에요.")],
     [look("슬라이드를 짚어 읽어요",
           (0.05, 0.19, 0.82, 0.05, "윗글: 두 가지 크기, 수십억 단어, 64개 TPU 로 4일. 앞 절반은 다시 하지 않는다."),
           (0.30, 0.33, 0.40, 0.05, "표 제목에 Devlin et al., 2018 이라고 출처가 적혀 있어요."),
           (0.13, 0.39, 0.56, 0.05, "표 머리: layers, hidden, heads, parameters."),
           (0.13, 0.46, 0.56, 0.09, "BERT-base 는 12 / 768 / 12 / 110M, BERT-large 는 24 / 1024 / 16 / 340M."),
           (0.13, 0.58, 0.56, 0.13, "아래 세 줄: 학습 데이터, 사전 학습 비용, 미세조정 비용이에요."),
           (0.72, 0.44, 0.19, 0.20, "오른쪽 초록 상자: 한 번 사전 학습, 여러 번 미세조정.")),
      steps("두 크기를 손으로 비교해 봐요",
            ["층은 12 에서 24 로 늘었어요. 24 / 12 = 2 배예요",
             f"{HID}은 768 에서 1024 로 늘었어요",
             f"{HEAD}는 12 에서 16 으로 늘었어요",
             f"{HEAD} 하나가 맡는 크기는 768 / 12 = 64 예요",
             "large 도 1024 / 16 = 64 로 똑같아요",
             f"{PARAM}는 110M 에서 340M 으로 약 3.1 배예요"],
            f"층은 2배, {PARAM}는 약 3.1배. {HEAD} 하나의 크기 64 는 그대로예요.",
            "base 12 / 768 / 12 / 110M, large 24 / 1024 / 16 / 340M"),
      steps("학습 데이터를 더해 봐요",
            ["BooksCorpus 가 8억 단어(0.8B)예요",
             "English Wikipedia 가 25억 단어(2.5B)예요",
             "0.8 + 2.5 = 3.3 이에요",
             "곧 33억 단어예요",
             "N5 p.14 막대그래프의 BERT 막대 3.3 과 같은 숫자예요"],
            f"33억 단어. 앞 쪽 그래프와 이어져요.",
            "0.8B + 2.5B"),
      bg("기초 다지기 3단원", f"{HID} 768 은 {TOK} 하나를 길이 768 짜리 숫자 목록으로 나타낸다는 뜻이에요.",
         f"{HEAD} 12 는 그 768 을 12 갈래로 나눠 서로 다른 관점에서 본다는 뜻이에요(4주차 N4 p.47).",
         f"층 12 는 {TRF} {ENC} 블록을 12 겹 쌓았다는 뜻이에요.")],
     [check("BERT-base 의 파라미터 수는?",
            ["110M", "340M", "768", "64"], 0,
            "표의 parameters 칸이 110M 이에요. 1억 1천만 개예요."),
      check("BERT-large 에서 헤드 하나가 맡는 크기는?",
            ["64", "16", "1024", "768"], 0,
            f"{HID} 1024 를 {HEAD} 16 으로 나누면 64 예요. base 도 768 / 12 = 64 로 같아요."),
      english("답안 문장",
              f"BERT-base 는 층 12, {HID} 768, {HEAD} 12, {PARAM} 110M 이고 BERT-large 는 24, 1024, 16, 340M 이다.",
              "'12-768-12-110M' 과 '24-1024-16-340M' 을 숫자 줄로 외워요."),
      warn("헷갈리기 쉬운 점",
           f"{PT} 비용과 {FT} 비용을 바꿔 적지 않게 조심해요. TPU 4일은 {PT} 쪽이에요.",
           f"{FT}은 {SL}이라 {LB}이 필요해요. {PT}은 아니에요.")])

# ---------------------------------------------------------------- p.23
page(23, "한 인코더, 네 가지 과제 모양",
     ["Encoder", "Task Head", "Body", "Downstream Task", "[CLS]", "[SEP]",
      "Sentence Pair", "Token Tagging", "Part-of-Speech Tagging (POS)", "Span Extraction",
      "Extractive QA", "Entailment", "Named Entity Recognition (NER)", "Sentiment Analysis",
      "Classification", "Finetuning", "Label", "Embedding", "Supervised Learning"],
     [say("거의 모든 자연어 과제는 네 가지 모양 중 하나예요.",
          f"{BODY}은 늘 같고, 위에 무엇을 얹을지만 고르면 돼요.",
          f"그 위에 얹는 것이 {TH}예요."),
      analogy("같은 몸통에 갈아 끼우는 공구 날",
              "전동 드릴 하나에 드라이버 날, 드릴 날, 사포 날을 갈아 끼우는 것과 같아요. 본체는 그대로예요.",
              ("드릴 본체", f"{PT}된 {ENC} {BODY}"),
              ("갈아 끼우는 날", TH),
              ("날 종류 네 가지", "문장 하나, 문장 쌍, 토큰 태깅, 스팬 추출")),
      figure("네 가지 과제 모양", FIG_SHAPES, "네 칸 모두 아래쪽 인코더는 같고 위쪽 색칠된 부분만 달라요.", 4)],
     [compare("네 가지 모양",
              ["모양", "출력", "대표 과제"],
              ["문장 하나(single sentence)", f"{LB} 하나", f"{SENT}, 주제 {CLSF}"],
              [f"{SPAIR}(sentence pair)", f"{LB} 하나", f"{ENT}, 유사도"],
              [f"{TT}(token tagging)", f"{TOK}마다 {LB} 하나", f"{NER}, {POS}"],
              [f"{SPX}(span extraction)", "포인터 둘(시작, 끝)", EQA]),
      points("슬라이드 영어와 우리말 뜻",
             "Almost every NLP task is one of four shapes = 거의 모든 자연어 과제는 네 모양 중 하나다",
             "The body stays the same = 몸통은 그대로다",
             "you only choose what to put on top = 위에 무엇을 얹을지만 고른다",
             "only the coloured part is new = 색칠된 부분만 새것이다",
             "the body is always the same downloaded weights = 몸통은 늘 같은 내려받은 가중치다"),
      points("특별한 토큰 둘",
             f"{CLS}: 맨 앞에 붙여 두고 문장 전체의 요약으로 써요. 문장 하나와 {SPAIR} 과제에서 이 자리 위에 {TH}를 얹어요.",
             f"{SEP}: 문장과 문장 사이를 갈라요. {SPAIR}와 {EQA}에서 써요.",
             f"둘 다 N5 p.21 의 {NSP} 예문에서 이미 봤어요.")],
     [look("슬라이드를 짚어 읽어요",
           (0.05, 0.19, 0.80, 0.05, "윗글: 거의 모든 과제는 네 모양 중 하나이고, 몸통은 같고 위에 얹을 것만 고른다."),
           (0.06, 0.33, 0.20, 0.32, "첫째 칸 문장 하나. 감성과 주제. [CLS] 위에 헤드 하나, 딱지 하나."),
           (0.27, 0.33, 0.21, 0.32, "둘째 칸 문장 쌍. 함의와 유사도. [SEP] 로 A 와 B 를 갈라요."),
           (0.49, 0.33, 0.21, 0.32, "셋째 칸 토큰 태깅. 개체명과 품사. 토큰마다 딱지가 하나씩이에요."),
           (0.71, 0.33, 0.21, 0.32, "넷째 칸 스팬 추출. 추출형 질의응답. 포인터 둘, 시작과 끝이에요."),
           (0.20, 0.79, 0.60, 0.04, "맨 아래: 몸통은 늘 같은 내려받은 가중치, 헤드만 고른다.")),
      points("네 모양을 실제 과제로 바꿔 보면",
             f"문장 하나: 영화평이 긍정인지 부정인지({SENT}). 이번 주 실습이 이 모양이에요.",
             f"{SPAIR}: 앞 문장이 참이면 뒤 문장도 참인지({ENT}).",
             f"{TT}: 서울은 장소, 은은 조사({NER}, {POS}).",
             f"{SPX}: 글에서 답이 되는 구간의 시작과 끝을 찍어요({EQA})."),
      points("검색은 왜 따로인가요",
             f"검색은 {TH} 없이 {ENC} 출력을 그대로 {EMB}으로 써요.",
             "두 문장의 벡터가 가까우면 비슷한 문장이에요.",
             f"이 쓸모는 N5 p.25 에서 다시 나와요."),
      bg("기초 다지기 9단원", f"{TH}는 보통 선형층 하나예요.",
         f"{HID} 768 짜리 벡터를 받아 {LB} 수만큼의 점수를 내놓아요.",
         f"긍정, 부정 두 가지면 768 x 2 + 2 개의 {PARAM}뿐이에요. 몸통에 비하면 아주 작아요.")],
     [check("추출형 질의응답의 과제 모양은?",
            ["스팬 추출", "문장 하나", "문장 쌍", "토큰 태깅"], 0,
            "슬라이드 넷째 칸이 span extraction, extractive QA 이고 포인터 둘을 써요."),
      check("네 가지 모양에서 바뀌지 않는 것은?",
            ["사전 학습된 몸통", "과제 헤드", "레이블의 개수", "입력 문장의 개수"], 0,
            "the body is always the same downloaded weights - you only choose the head."),
      english("답안 문장",
              f"네 가지 과제 모양은 문장 하나, {SPAIR}, {TT}, {SPX}이다.",
              f"{BODY}은 그대로 두고 {TH}만 바꿔요.",
              "네 모양 이름을 순서대로 외우고 과제 하나씩 붙여 두면 좋아요."),
      warn("헷갈리기 쉬운 점",
           f"{TT}은 {TOK}마다 답이 하나씩이고, {SPX}은 문장 전체에서 시작과 끝 두 자리만 찍어요.",
           f"{SL}이라 네 모양 모두 {LB}이 필요해요. 다만 수천 개면 충분해요.")])

# ---------------------------------------------------------------- p.24
page(24, "순위표를 바꿔 놓았어요",
     ["GLUE", "Benchmark", "BERT", "GPT", "Finetuning", "Entailment", "Sentiment Analysis",
      "Sentence Pair", "Classification", "Encoder", "Downstream Task", "Pre-training"],
     [say(f"{BERT}는 {BENCH} 하나를 이긴 것이 아니에요.",
          f"같은 방법으로 아홉 개를 한꺼번에 이겼어요.",
          "그래서 분야 전체가 방식을 바꿨어요."),
      points("막대 네 개를 왼쪽부터",
             f"BiLSTM + ELMo: {GLUE} 평균 71.0 이에요.",
             f"OpenAI {GPT}: 75.1 이에요.",
             f"{BERT} base: 79.6 이에요.",
             f"{BERT} large: 82.1 이에요.")],
     [compare("슬라이드 영어와 우리말 뜻",
              ["영어 원문", "뜻"],
              ["It Changed the Leaderboards", "순위표를 바꿔 놓았다"],
              ["BERT did not win one benchmark", "BERT 는 벤치마크 하나를 이긴 것이 아니다"],
              ["it won nine at once, with the same recipe", "같은 방법으로 아홉 개를 한꺼번에 이겼다"],
              ["That is what made the field switch", "그것이 분야 전체를 바꾸게 만들었다"],
              ["the same finetuning recipe for all of them", "아홉 개 모두 같은 미세조정 방법"]),
      points("GLUE 아홉 과제가 뭔가요",
             f"SST-2: {SENT}이에요.",
             "CoLA: 이 문장이 문법에 맞나요.",
             f"MRPC / QQP: 바꿔 쓴 문장인지 가려내요({SPAIR} 모양이에요).",
             "STS-B: 두 문장이 얼마나 비슷한가요.",
             f"QNLI / RTE: 자연어 추론, 곧 {ENT} 관계를 따져요."),
      points("이 그림이 말하는 것",
             f"{GLUE}는 영어 이해 과제를 묶어 놓은 {BENCH}예요.",
             f"막대 하나가 아홉 과제의 평균 점수예요.",
             f"같은 {FT} 방법으로 아홉 개를 다 했다는 것이 진짜 뉴스예요.")],
     [look("슬라이드를 짚어 읽어요",
           (0.05, 0.19, 0.80, 0.05, "윗글: 벤치마크 하나가 아니라 아홉 개를 한 번에, 같은 방법으로 이겼다."),
           (0.16, 0.35, 0.29, 0.04, "그래프 제목: GLUE, 2018, Devlin et al., Table 1 이 출처예요."),
           (0.07, 0.39, 0.44, 0.31, "세로축이 GLUE average, 곧 아홉 과제의 평균 점수예요."),
           (0.12, 0.40, 0.38, 0.28, "막대 위 숫자 71.0, 75.1, 79.6, 82.1 이 네 모델의 점수예요."),
           (0.58, 0.37, 0.32, 0.20, "오른쪽 위: 한 모델, 아홉 과제. SST-2, CoLA, MRPC/QQP 가 보여요."),
           (0.58, 0.58, 0.32, 0.15, "아래: STS-B 와 QNLI/RTE, 그리고 모두 같은 미세조정 방법이라는 말이에요.")),
      steps("점수 차이를 계산해 봐요",
            ["BiLSTM + ELMo 는 71.0 이에요",
             "BERT large 는 82.1 이에요",
             "82.1 - 71.0 = 11.1 점 차이예요",
             f"OpenAI {GPT} 75.1 과 비교하면 82.1 - 75.1 = 7.0 점이에요",
             "BERT base 79.6 에서 large 82.1 로는 2.5 점 올랐어요"],
            "11.1 점. 한 해 만에 이만큼 뛰는 일은 드물어요.",
            "71.0 / 75.1 / 79.6 / 82.1"),
      points("왜 GPT 보다 높았을까요",
             f"{GLUE}는 대부분 이해 과제예요. 분류와 {SPAIR} 판단이 많아요.",
             f"{ENC}는 앞뒤를 다 보니 이해 과제에 유리해요.",
             f"반대로 글쓰기가 필요한 {DT}라면 {GPT} 쪽이 유리해요. N5 p.25 에서 봐요.")],
     [check("BERT large 의 GLUE 평균 점수는?",
            ["82.1", "79.6", "75.1", "71.0"], 0,
            "막대 위 숫자가 82.1 이에요. 가장 오른쪽 진한 막대예요."),
      english("답안 문장",
              f"{BERT}는 같은 {FT} 방법으로 {GLUE} 아홉 과제를 한꺼번에 이겼고, 그것이 분야 전체를 {PT} 방식으로 바꿨다.",
              "'아홉 개를 한 번에, 같은 방법으로' 를 꼭 넣어요."),
      warn("헷갈리기 쉬운 점",
           f"{GLUE} 평균 82.1 은 사람 점수가 아니라 아홉 과제의 평균이에요.",
           f"과제마다 {TH}는 달랐어요. 같은 것은 {BODY}과 {FT} 방법이에요.")])

# ---------------------------------------------------------------- p.25
page(25, "사전 학습된 인코더가 못 하는 것",
     ["Encoder", "Decoder", "[MASK]", "Autoregressive", "Classification", "Token Tagging",
      "Part-of-Speech Tagging (POS)", "Named Entity Recognition (NER)", "Embedding",
      "Sentiment Analysis", "GPT", "BERT", "Masked Language Modelling (MLM)",
      "Next Token Prediction", "Task Head", "Downstream Task"],
     [say(f"{ENC}는 빈칸 하나를 채우는 데까지예요.",
          f"이어서 다음 낱말을 쓰고, 또 그다음을 쓰는 길이 없어요.",
          f"출력이 자유로운 글이라면 {ENC}는 잘못 고른 도구예요."),
      analogy("빈칸 채우기 시험지",
              "빈칸 채우기 시험지는 빈칸만 채우고 끝나요. 그 아래에 이야기를 이어 쓰라는 칸은 없어요.",
              ("빈칸 하나 채우고 끝", f"{ENC}의 {MLM}"),
              ("이야기를 계속 이어 쓰기", f"{DEC}의 {NTP}"),
              ("시험지를 잘못 고른 것", f"글쓰기 {DT}에 {ENC}를 쓰는 일"))],
     [compare("슬라이드 영어와 우리말 뜻",
              ["영어 원문", "뜻"],
              ["An encoder fills in a blank", "인코더는 빈칸을 채운다"],
              ["It has no natural way to keep writing", "계속 써 나갈 자연스러운 방법이 없다"],
              ["so if your output is free-form text, this is the wrong tool",
               "출력이 자유로운 글이라면 이것은 잘못된 도구다"],
              ["one blank, one shot", "빈칸 하나, 한 번뿐"],
              ["pick the architecture that matches the shape of your output",
               "출력의 모양에 맞는 구조를 고르라"]),
      points("오른쪽 네 줄을 한 줄씩",
             f"{CLSF}: {SENT}, 주제, 의도 파악. 잘해요.",
             f"{TT}: {NER}, {POS}. 잘해요.",
             f"검색과 유사도: 검색용 {EMB}을 만들어요. 잘해요.",
             f"생성: 못 해요. {DEC}를 쓰라고 적혀 있어요."),
      points("왼쪽 그림의 예문",
             f"Iroh goes to {MASK} tasty tea 에서 빈칸을 채우면 make, brew, craft 가 나와요.",
             "그런데 거기서 끝이에요. 그다음 문장을 이어 쓸 수 없어요.",
             f"이것이 one blank, one shot, 곧 빈칸 하나에 한 번이라는 말이에요.")],
     [look("슬라이드를 짚어 읽어요",
           (0.05, 0.19, 0.85, 0.05, "윗글: 인코더는 빈칸을 채울 뿐 계속 써 나갈 방법이 없다."),
           (0.34, 0.33, 0.32, 0.05, "큰 제목: 사전 학습된 인코더가 못 하는 것."),
           (0.11, 0.45, 0.39, 0.06, "파란 상자가 사전 학습된 인코더예요."),
           (0.11, 0.52, 0.39, 0.07, "아래 토큰 줄에서 주황 [MASK] 한 자리만 채워요."),
           (0.17, 0.66, 0.30, 0.07, "빨간 글: 계속 이어 쓸 자연스러운 방법이 없다."),
           (0.56, 0.37, 0.34, 0.30, "오른쪽: 분류, 태깅, 검색은 체크 표시, 생성만 가위표예요.")),
      points("왜 이어 쓸 수 없나요",
             f"{ENC}는 {AR}가 아니에요. 자기 출력을 다시 입력으로 넣는 구조가 아니에요.",
             f"{MLM}으로 학습했으니 '다음 자리' 라는 개념 자체가 없어요.",
             f"{DEC}는 {CM} 덕분에 한 자리씩 이어 붙일 수 있어요(N4 p.43)."),
      points("그래서 무엇을 고르나요",
             f"출력이 딱지 하나면 {ENC}({BERT})예요.",
             f"출력이 자유로운 글이면 {DEC}({GPT})예요.",
             f"출력이 입력 글을 바꾼 글(번역, 요약)이면 인코더 디코더예요.",
             "슬라이드 맨 아래 한 줄이 그대로 이 말이에요. N5 p.40 에서 다시 정리해요."),
      bg("기초 다지기 9단원", f"{TH}는 {ENC} 위에 얹는 작은 출력층이에요.",
         "딱지를 고르는 일에는 잘 맞지만, 글을 쭉 써 내려가는 일에는 맞지 않아요.",
         "글을 쓰려면 한 토큰을 낸 뒤 그것을 다시 입력으로 받는 구조가 필요해요.")],
     [check("자유로운 글을 만들어야 할 때 골라야 하는 구조는?",
            ["디코더", "인코더", "과제 헤드", "임베딩 층"], 0,
            "슬라이드 오른쪽 generation 줄에 use a decoder instead 라고 적혀 있어요."),
      check("사전 학습된 인코더가 잘하는 일이 아닌 것은?",
            ["자유로운 글 생성", "분류", "토큰 태깅", "검색용 임베딩"], 0,
            "체크 표시 셋은 classification, tagging, retrieval 이고 generation 만 가위표예요."),
      english("답안 문장",
              f"{ENC}는 빈칸을 한 번 채울 뿐 {AR}로 이어 쓸 수 없으므로, 생성 과제에는 {DEC}를 써야 한다.",
              "'빈칸 하나, 한 번뿐' 이라는 슬라이드 말을 그대로 써도 좋아요."),
      warn("헷갈리기 쉬운 점",
           f"{ENC}가 약한 모델이라는 뜻이 아니에요. {CLSF}와 {TT}에서는 {DEC}보다 나을 때가 많아요.",
           "출력의 모양에 맞는 구조를 고르라는 것이 이 쪽의 결론이에요.")])

data = {"deck": "N5", "from": 14, "to": 25,
        "glossary": [{"ko": k, "en": e, "say": s, "more": m} for k, e, s, m in GLOSSARY],
        "slides": S}

raw = json.dumps(data, ensure_ascii=False, indent=1)
for ch in ("—", "–", "·", "・"):
    assert ch not in raw, ch
with open(OUT, "w", encoding="utf-8") as f:
    f.write(raw)
print("saved", OUT, len(S), "pages")
