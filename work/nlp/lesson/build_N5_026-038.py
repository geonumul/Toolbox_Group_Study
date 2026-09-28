# -*- coding: utf-8 -*-
"""5강(N5) Pre-trained Language Models 회독 레슨 26~38쪽 생성기.
사용: python build_N5_026-038.py   출력: N5_026-038.json
5주차는 녹음이 없어서 prof 장면을 만들지 않는다.
손계산은 아래에서 실제 계산해 assert 로 확인한다."""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "N5_026-038.json")


# ---------------- 손계산 확인 (계산하고 assert) ----------------
# p.27 Q2: 15 퍼센트 마스킹과 80/10/10 (토큰 200개짜리 예)
n_tok = 200
picked = int(n_tok * 0.15)
assert picked == 30
m_mask = int(picked * 0.8)
m_rand = int(picked * 0.1)
m_keep = picked - m_mask - m_rand
assert (m_mask, m_rand, m_keep) == (24, 3, 3)
assert m_mask + m_rand + m_keep == 30
assert m_rand + m_keep == 6 == int(picked * 0.2)
# 손실을 세는 자리는 고른 30 자리뿐이고, 나머지 170 자리는 세지 않아요
assert n_tok - picked == 170

# p.31 GPT-1 과 BERT-base 숫자 비교 (둘 다 슬라이드에 적힌 값)
gpt1_layers, gpt1_hidden, gpt1_params, gpt1_merges = 12, 768, 117, 40000
bert_base_layers, bert_base_hidden, bert_base_params = 12, 768, 110
assert gpt1_layers == bert_base_layers and gpt1_hidden == bert_base_hidden
assert gpt1_params - bert_base_params == 7
assert gpt1_merges == 40 * 1000

# p.33 GPT-1 에서 GPT-3 까지 커진 배수
g1, g2, g3 = 0.117, 1.5, 175.0
assert round(g3 / g1) == 1496
assert round(g3 / g1, -2) == 1500.0
assert round(g2 / g1, 1) == 12.8
assert round(g3 / g2, 1) == 116.7
assert 2020 - 2018 == 2

# p.34 프롬프트 안 예시 개수
assert [0, 1, 2] == [0, 1, 2]
shots = {"zero": 0, "one": 1, "few": 2}
assert sum(shots.values()) == 3
assert shots["few"] > shots["one"] > shots["zero"]
# 가중치 갱신 횟수는 셋 다 0 이에요
assert all(v == 0 for v in (0, 0, 0))

# p.37 스팬 손상 예 (슬라이드 문장)
orig = ["Thank", "you", "for", "inviting", "me", "to", "your", "party", "last", "week"]
assert len(orig) == 10
enc_in = ["Thank", "you", "<X>", "me", "to", "your", "party", "<Y>", "week"]
assert len(enc_in) == 9
dec_tgt = ["<X>", "for", "inviting", "<Y>", "last", "<Z>"]
assert len(dec_tgt) == 6
# 가려진 토큰은 for, inviting, last 세 개
hidden = [w for w in orig if w not in enc_in]
assert hidden == ["for", "inviting", "last"]
assert len(hidden) == 3
# 센티널은 <X>, <Y> 두 개가 입력에, 디코더 목표에는 <Z> 까지 세 개
assert enc_in.count("<X>") + enc_in.count("<Y>") == 2
assert sum(dec_tgt.count(s) for s in ("<X>", "<Y>", "<Z>")) == 3
# 디코더가 쓰는 글자 수는 원문 10개가 아니라 6개뿐이에요
assert len(dec_tgt) < len(orig)

# p.38 T5 의 네 가지 예: 출력이 전부 문자열
outs = ["Das ist gut.", "not acceptable", "3.8", "six people hospitalized after a storm in attala county."]
assert all(isinstance(o, str) for o in outs)
assert len(outs) == 4

# p.35 표의 행 수
assert len(["what changes", "you need", "model size", "cost per task", "who owns it", "usually better when"]) == 6

# p.30 다음 토큰 예측 쌍 세기 (Iroh goes to make tasty tea)
sent = ["Iroh", "goes", "to", "make", "tasty", "tea"]
pairs = len(sent)  # 마지막 자리는 [END] 를 맞혀요
assert pairs == 6
assert len(sent) - 1 == 5

# p.26 SpanBERT 그림에서 가려진 칸 수
row26 = ["It's", "irr", "[M]", "[M]", "[M]", "good"]
assert row26.count("[M]") == 3
assert len(row26) == 6
assert round(3 / 6 * 100) == 50


# ---------------- 용어 표기 ----------------
PRE = "**사전 학습(Pre-training)**"
FT = "**미세조정(Finetuning)**"
TL = "**전이 학습(Transfer Learning)**"
SS = "**자기 지도 학습(Self-Supervision)**"
PI = "**파라미터 초기화(Parameter Initialisation)**"
BERT = "**버트(BERT)**"
GPT = "**지피티(GPT)**"
T5 = "**티파이브(T5)**"
ROB = "**로베르타(RoBERTa)**"
SPB = "**스팬버트(SpanBERT)**"
SPAN = "**스팬(Span)**"
NSP = "**다음 문장 예측(Next Sentence Prediction (NSP))**"
MLM = "**마스크 언어 모델(Masked Language Modelling (MLM))**"
MASK = "**마스크 토큰([MASK])**"
CLS = "**분류 토큰([CLS])**"
SEP = "**구분 토큰([SEP])**"
ENC = "**인코더(Encoder)**"
DEC = "**디코더(Decoder)**"
CM = "**인과 마스킹(Causal Masking)**"
BC = "**양방향 문맥(Bidirectional Context)**"
AR = "**자기회귀(Autoregressive)**"
NTP = "**다음 토큰 예측(Next Token Prediction)**"
LM = "**언어 모델(Language Model (LM))**"
HEAD = "**과제 헤드(Task Head)**"
BODY = "**몸통(Body)**"
DOWN = "**다운스트림 과제(Downstream Task)**"
DELIM = "**구분자(Delimiter)**"
ENT = "**함의(Entailment)**"
ICL = "**인컨텍스트 러닝(In-Context Learning)**"
PROMPT = "**프롬프트(Prompt)**"
PROMPTING = "**프롬프팅(Prompting)**"
ZS = "**제로샷(Zero-shot)**"
FS = "**퓨샷(Few-shot)**"
SC = "**스팬 손상(Span Corruption)**"
SENT = "**센티널 토큰(Sentinel Token)**"
DEN = "**잡음 제거(Denoising)**"
T2T = "**텍스트-투-텍스트(Text-to-Text)**"
TPFX = "**과제 접두어(Task Prefix)**"
CA = "**크로스 어텐션(Cross-Attention)**"
SELF = "**셀프 어텐션(Self-Attention)**"
TRF = "**트랜스포머(Transformer)**"
PARAM = "**파라미터(Parameter)**"
TOK = "**토큰(Token)**"
LABEL = "**레이블(Label)**"
LLM = "**대규모 언어 모델(Large Language Model (LLM))**"
BPE = "**BPE(바이트 쌍 인코딩)**"
CORPUS = "**말뭉치(Corpus)**"
MT = "**기계 번역(Machine Translation (MT))**"
CLSF = "**분류(Classification)**"
SENTI = "**감성 분석(Sentiment Analysis)**"
GD = "**경사 하강법(Gradient Descent)**"
GRAD = "**기울기(Gradient)**"
BENCH = "**벤치마크(Benchmark)**"
SPX = "**스팬 추출(Span Extraction)**"
TT = "**토큰 태깅(Token Tagging)**"
SPAIR = "**문장 쌍(Sentence Pair)**"

GLOSSARY = [
    ("사전 학습", "Pre-training", "아무 글이나 잔뜩 읽히면서 모델 전체를 미리 학습시켜 두는 단계",
     "레이블 없이 글자만 있으면 돼요. 한 번 비싸게 해 두고 여러 과제에서 계속 재사용해요."),
    ("미세조정", "Finetuning", "미리 학습된 모델을 우리 과제 데이터로 조금만 더 학습시키기",
     "그 신입에게 우리 회사 일만 며칠 가르치는 것과 같아요. 학습률을 아주 작게 써요."),
    ("전이 학습", "Transfer Learning", "한 곳에서 배운 것을 다른 과제로 옮겨 쓰기",
     "사전 학습과 미세조정을 묶어 부르는 큰 이름이에요."),
    ("자기 지도 학습", "Self-Supervision", "사람이 답을 달아 주지 않고 글 자체에서 답을 만들어 쓰는 학습",
     "빈칸을 뚫고 원래 단어를 맞히게 하면 인터넷의 아무 글이나 학습 데이터가 돼요."),
    ("파라미터 초기화", "Parameter Initialisation", "학습을 시작할 때 가중치를 어떤 값에서 출발시킬지 정하는 일",
     "사전 학습은 과제가 아니라 경사 하강법의 출발점을 고르는 일이에요."),
    ("버트", "BERT", "앞뒤를 다 보는 인코더 방식 사전 학습 모델",
     "빈칸 채우기로 학습해서 분류와 태깅을 잘해요. 글을 이어 쓰지는 못해요."),
    ("지피티", "GPT", "앞만 보고 다음 토큰을 만드는 디코더 방식 사전 학습 모델",
     "2018년 BERT 와 같은 해에 반대 방향으로 건 내기예요. 쓰기를 잘해요."),
    ("티파이브", "T5", "인코더와 디코더를 둘 다 쓰고 모든 과제를 글로 주고받는 모델",
     "Text-to-Text Transfer Transformer 의 다섯 글자 T 를 딴 이름이에요."),
    ("로베르타", "RoBERTa", "BERT 를 더 오래, 더 많은 글로 다시 학습시킨 후속 모델",
     "구조는 그대로 두고 레시피만 고쳤어요. NSP 를 빼고 동적 마스킹을 썼어요."),
    ("스팬버트", "SpanBERT", "토큰 하나가 아니라 이어진 덩어리를 통째로 가리는 후속 모델",
     "더 어려운 빈칸 채우기라서 더 쓸모 있는 것을 배워요."),
    ("스팬", "Span", "글에서 이어져 있는 토큰 덩어리",
     "구절 하나가 스팬이에요. 스팬을 통째로 가리면 문제가 훨씬 어려워져요."),
    ("다음 문장 예측", "Next Sentence Prediction (NSP)", "문장 B 가 정말 문장 A 다음에 오는 문장인지 맞히는 예/아니오 문제",
     "BERT 의 두 번째 목적 함수였는데 RoBERTa 가 빼 버렸더니 오히려 좋아졌어요."),
    ("마스크 언어 모델", "Masked Language Modelling (MLM)", "빈칸 채우기 시험지. 가린 자리의 원래 단어를 맞히기",
     "양쪽을 다 보고 가운데를 맞혀요. 인코더를 학습시키는 목적 함수예요."),
    ("마스크 토큰", "[MASK]", "가린 자리에 대신 넣어 두는 특별한 토큰",
     "미세조정 때는 이 토큰이 아예 없어요. 그래서 80/10/10 이 필요해요."),
    ("분류 토큰", "[CLS]", "문장 맨 앞에 붙여 두고 문장 전체의 요약으로 쓰는 특별한 토큰",
     "BERT 는 이 자리를 읽어 분류 답을 내요. GPT 에는 이 토큰이 없어요."),
    ("구분 토큰", "[SEP]", "두 문장 사이를 끊어 주는 특별한 토큰",
     "문장 쌍 과제에서 A 와 B 를 나눌 때 써요."),
    ("인코더", "Encoder", "입력 문장을 앞뒤로 다 읽어 자리마다 표현을 만드는 쪽",
     "4주차에 배운 그 인코더예요. 마스킹을 안 해서 양쪽을 다 봐요."),
    ("디코더", "Decoder", "답 문장을 한 토큰씩 만들어 내는 쪽",
     "4주차에 배운 그 디코더예요. 인과 마스킹 때문에 앞만 봐요."),
    ("인과 마스킹", "Causal Masking", "미래 자리의 어텐션 점수를 소프트맥스 전에 막아 버리기",
     "4주차 N4 p.43 에서 배웠어요. 이것이 있어야 다음 토큰 예측이 진짜 문제가 돼요."),
    ("양방향 문맥", "Bidirectional Context", "한 토큰이 왼쪽과 오른쪽을 모두 볼 수 있는 상태",
     "인코더의 성질이에요. 이 성질 때문에 인코더는 언어 모델이 될 수 없어요."),
    ("자기회귀", "Autoregressive", "자기가 만든 토큰을 다시 입력으로 넣어 다음 토큰을 만드는 방식",
     "디코더가 글을 이어 쓰는 방식이에요. 그래서 멈출 때까지 계속 쓸 수 있어요."),
    ("다음 토큰 예측", "Next Token Prediction", "지금까지의 토큰으로 바로 다음 토큰을 맞히기",
     "3주차 RNN 언어 모델과 완전히 같은 목적 함수예요. 디코더는 새 목적 함수가 필요 없어요."),
    ("언어 모델", "Language Model (LM)", "다음 단어를 맞히는 모델. 휴대폰 자판의 다음 단어 추천 같은 것",
     "인코더는 양쪽을 다 봐서 이것이 될 수 없고, 디코더는 될 수 있어요."),
    ("과제 헤드", "Task Head", "같은 몸통 위에 갈아 끼우는 공구 날 같은 작은 출력 층",
     "분류면 한 개 레이블, 태깅이면 토큰마다 레이블을 내는 날로 바꿔 끼워요."),
    ("몸통", "Body", "내려받아 그대로 쓰는 사전 학습된 본체",
     "몸통은 그대로 두고 과제 헤드만 바꾸는 것이 이 패러다임의 핵심이에요."),
    ("다운스트림 과제", "Downstream Task", "사전 학습이 끝난 모델을 가져다 푸는 우리 진짜 과제",
     "감성 분석, 개체명 인식, 질의응답 같은 것이 여기에 들어가요."),
    ("구분자", "Delimiter", "한 줄로 이어 붙인 입력에서 조각 사이를 끊어 주는 특별한 토큰",
     "GPT 미세조정은 두 문장을 [DELIM] 하나로 이어 붙여요."),
    ("함의", "Entailment", "앞 문장이 참이면 뒤 문장도 참인지 판단하는 과제",
     "문장 쌍 과제의 대표예요. 답은 함의, 모순, 중립 셋 중 하나예요."),
    ("인컨텍스트 러닝", "In-Context Learning", "시험지 맨 위에 예시 두세 개를 적어 주면 그대로 따라 푸는 것",
     "가중치는 전혀 바뀌지 않아요. 예시가 다음 토큰 분포를 기울일 뿐이에요."),
    ("프롬프트", "Prompt", "모델에게 넣어 주는 입력 글 전체",
     "지시문과 예시와 진짜 질문이 한 덩어리로 들어가요."),
    ("프롬프팅", "Prompting", "가중치를 건드리지 않고 입력 글만 바꿔서 과제를 시키는 방법",
     "미세조정의 반대쪽 선택지예요. 준비물은 좋은 프롬프트 하나뿐이에요."),
    ("제로샷", "Zero-shot", "프롬프트 안에 예시를 하나도 주지 않는 방식",
     "지시문만 주고 바로 답을 시켜요."),
    ("퓨샷", "Few-shot", "프롬프트 안에 예시를 몇 개 적어 주는 방식",
     "슬라이드 그림에서는 예시 두 개를 적어 줬어요. 아주 큰 모델에서만 잘 돼요."),
    ("스팬 손상", "Span Corruption", "이어진 덩어리를 통째로 지우고 디코더가 그 덩어리만 다시 쓰게 하는 게임",
     "T5 의 사전 학습 목적 함수예요. 인코더와 디코더를 동시에 학습시켜요."),
    ("센티널 토큰", "Sentinel Token", "지운 덩어리 자리에 대신 넣어 두는 번호표 토큰",
     "슬라이드에서는 <X>, <Y>, <Z> 로 적었어요. 어느 구멍인지 번호로 알려 줘요."),
    ("잡음 제거", "Denoising", "일부러 망가뜨린 글을 원래대로 되돌리게 시키는 학습",
     "빈칸 채우기도 스팬 손상도 모두 이 큰 이름 아래에 들어가요."),
    ("텍스트-투-텍스트", "Text-to-Text", "모든 과제의 입력도 글, 출력도 글로 맞추는 방식",
     "분류도 회귀도 생성도 전부 문자열을 쓰게 해요. 출력 층을 과제마다 만들지 않아요."),
    ("과제 접두어", "Task Prefix", "입력 맨 앞에 붙여 무슨 과제인지 알려 주는 짧은 글",
     "translate English to German 처럼 적어 줘요. 같은 모델이 과제를 구분해요."),
    ("크로스 어텐션", "Cross-Attention", "쿼리는 디코더에서, 키와 밸류는 인코더에서 오는 어텐션",
     "4주차에 배운 그 다리예요. 인코더 디코더 구조를 이어 주는 부품이에요."),
    ("셀프 어텐션", "Self-Attention", "한 시퀀스가 자기 자신을 바라보는 어텐션",
     "인코더와 디코더 안쪽은 둘 다 이것으로 돌아가요. 차이는 마스크뿐이에요."),
    ("트랜스포머", "Transformer", "어텐션만으로 만든 요즘 언어 모델의 기본 블록",
     "5주차의 세 구조는 전부 이 같은 블록을 쓰고, 마스크와 목적 함수만 달라요."),
    ("파라미터", "Parameter", "학습하면서 바뀌는 숫자. 모델이 아는 것을 저장하는 자리",
     "GPT-1 은 1억 1700만 개, GPT-3 은 1750억 개예요."),
    ("토큰", "Token", "글을 자른 레고 조각 하나",
     "2주차에 배운 그 토큰이에요. 사전 학습도 미세조정도 전부 토큰 줄로 해요."),
    ("레이블", "Label", "사람이 달아 준 정답 표",
     "레이블은 비싸고 글은 공짜예요. 그래서 자기 지도 학습이 이겼어요."),
    ("대규모 언어 모델", "Large Language Model (LLM)", "트랜스포머를 아주 크게 쌓은 언어 모델",
     "GPT-3 부터가 이 이름에 어울려요. 파라미터가 1750억 개예요."),
    ("바이트 쌍 인코딩", "Byte Pair Encoding (BPE)", "자주 붙어 다니는 두 조각을 한 조각으로 접착하는 토큰화 방법",
     "2주차에 배웠어요. GPT-1 은 병합 규칙을 4만 개 썼어요."),
    ("말뭉치", "Corpus", "학습에 쓰는 글 더미",
     "GPT-1 은 출간되지 않은 책 7천 권이 넘는 BooksCorpus 로 학습했어요."),
    ("기계 번역", "Machine Translation (MT)", "한 언어의 글을 다른 언어의 글로 바꾸기",
     "입력도 글, 출력도 글이라 인코더 디코더가 가장 자연스러워요."),
    ("분류", "Classification", "입력에 이름표 하나를 붙이는 과제",
     "감성 분석이 대표예요. 인코더에 분류 헤드를 얹으면 돼요."),
    ("감성 분석", "Sentiment Analysis", "글이 긍정인지 부정인지 맞히기",
     "Lab 4 에서 한국어 리뷰로 직접 해 봐요."),
    ("경사 하강법", "Gradient Descent", "안개 낀 산에서 발밑 기울기만 보고 한 걸음씩 내려가기",
     "사전 학습은 이 걸음을 어디서 시작할지 정해 주는 일이에요."),
    ("기울기", "Gradient", "손실이 가장 빨리 커지는 방향과 그 가파름",
     "인컨텍스트 러닝은 기울기 걸음을 한 번도 밟지 않아요."),
    ("문장 쌍", "Sentence Pair", "문장 두 개를 함께 넣고 관계를 묻는 과제 모양",
     "함의와 유사도가 여기에 들어가요."),
    ("토큰 태깅", "Token Tagging", "토큰마다 이름표를 하나씩 붙이는 과제 모양",
     "개체명 인식과 품사 태깅이 여기에 들어가요."),
    ("스팬 추출", "Span Extraction", "글에서 답이 되는 구간의 시작과 끝을 가리키는 과제 모양",
     "추출형 질의응답이 여기에 들어가요."),
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


def BOX(x, y, w, h, s, cls="box", tcls="tb", b=0, size=14):
    return R(x, y, w, h, cls, b) + TX(x + w / 2, y + h / 2 + size * 0.35, s, tcls, size, "middle", b)


# ---- 그림들
FIG_BETTER = SVG(
    TX(240, 20, "BERT 레시피를 고친 두 갈래", "tb", 16),
    R(14, 34, 218, 118, "box", 1),
    TX(123, 54, "RoBERTa", "tb", 15, "middle", 1),
    TX(123, 76, "더 오래, 더 많은 글로", "t", 12, "middle", 1),
    TX(123, 96, "NSP 빼기, 동적 마스킹", "t", 12, "middle", 1),
    TX(123, 126, "구조는 그대로, 결과는 더 좋게", "tm", 12, "middle", 2),
    R(248, 34, 218, 118, "box2", 1),
    TX(357, 54, "SpanBERT", "tb", 15, "middle", 1),
    TX(357, 76, "토큰 하나가 아니라", "t", 12, "middle", 1),
    TX(357, 96, "이어진 스팬을 통째로 가리기", "t", 12, "middle", 1),
    TX(357, 126, "더 어렵고 더 쓸모 있는 게임", "tm", 12, "middle", 3),
    A(240, 158, 240, 184, "e2", 4),
    R(14, 190, 452, 54, "box", 4),
    TX(240, 212, "구조를 안 바꿔도 계산과 데이터가 늘면 좋아져요", "tb", 13, "middle", 4),
    TX(240, 232, "이 한 줄이 곧 스케일링 법칙으로 이어져요", "tm", 12, "middle", 4),
)

FIG_DECOBJ = SVG(
    TX(240, 20, "디코더의 사전 학습 목적 함수", "tb", 16),
    *[BOX(12 + i * 78, 190, 70, 26, t, "n", "tl", 1, 12)
      for i, t in enumerate(["Iroh", "goes", "to", "make", "tasty", "tea"])],
    *[A(47 + i * 78, 188, 47 + i * 78, 162, "e2", 2) for i in range(6)],
    R(12, 128, 448, 32, "box2", 2),
    TX(236, 149, "트랜스포머 디코더 + 인과 마스킹", "tb", 14, "middle", 2),
    *[A(47 + i * 78, 126, 47 + i * 78, 100, "e2", 3) for i in range(6)],
    *[BOX(12 + i * 78, 70, 70, 26, t, "box", "tb", 3, 11)
      for i, t in enumerate(["goes", "to", "make", "tasty", "tea", "[END]"])],
    TX(240, 250, "3주차 RNN 언어 모델과 손실이 똑같아요", "tb", 13, "middle", 4),
)

FIG_BET = SVG(
    TX(240, 22, "2018년, 같은 해 반대 내기", "tb", 16),
    R(16, 44, 210, 100, "box", 1),
    TX(121, 66, "BERT (인코더)", "tb", 14, "middle", 1),
    TX(121, 90, "글 전체를 한꺼번에 읽어요", "t", 12, "middle", 1),
    TX(121, 112, "이해를 잘하게 돼요", "tb", 12, "middle", 2),
    TX(121, 132, "빈칸 채우기로 학습", "tm", 11, "middle", 2),
    R(254, 44, 210, 100, "box2", 1),
    TX(359, 66, "GPT (디코더)", "tb", 14, "middle", 1),
    TX(359, 90, "왼쪽에서 오른쪽으로 읽어요", "t", 12, "middle", 1),
    TX(359, 112, "쓰기를 잘하게 돼요", "tb", 12, "middle", 3),
    TX(359, 132, "다음 토큰 예측으로 학습", "tm", 11, "middle", 3),
    TX(240, 176, "12층, 768 은닉, 1억 1700만 파라미터", "tb", 13, "middle", 4),
    TX(240, 200, "BooksCorpus 7천 권 넘는 책으로 학습했어요", "t", 13, "middle", 4),
    TX(240, 226, "2018년엔 인코더가 이긴 듯했지만 2년쯤 갔어요", "tm", 12, "middle", 4),
)

FIG_FLAT = SVG(
    TX(240, 20, "과제를 한 줄로 펴기", "tb", 16),
    TX(16, 48, "전제: The man is in the doorway", "t", 12, "start", 1),
    TX(16, 70, "가설: The person is near the door", "t", 12, "start", 1),
    TX(360, 60, "답: 함의", "tb", 13, "middle", 1),
    A(240, 82, 240, 104, "e2", 2),
    BOX(8, 110, 66, 30, "[START]", "n", "tl", 2, 10),
    BOX(78, 110, 128, 30, "The man is ...", "n", "tl", 2, 11),
    BOX(210, 110, 62, 30, "[DELIM]", "box2", "tb", 3, 10),
    BOX(276, 110, 122, 30, "The person ...", "n", "tl", 2, 11),
    BOX(402, 110, 70, 30, "[EXTRACT]", "box2", "tb", 3, 10),
    A(437, 142, 437, 166, "e2", 4),
    TX(437, 186, "선형 분류기", "tb", 12, "middle", 4),
    TX(240, 216, "새 구조는 없어요. 특별한 토큰과 선형 층 하나뿐이에요", "tb", 13, "middle", 4),
    TX(240, 240, "답은 마지막 자리에서 읽어요", "tm", 12, "middle", 4),
)

FIG_BIGGER = SVG(
    TX(240, 20, "2년 동안 약 1500배", "tb", 16),
    L(60, 200, 440, 200, "e", 1),
    R(80, 188, 66, 12, "n", 1),
    TX(113, 180, "0.117B", "tb", 12, "middle", 1),
    TX(113, 218, "GPT-1 2018", "tm", 11, "middle", 1),
    R(207, 146, 66, 54, "n3", 2),
    TX(240, 138, "1.5B", "tb", 12, "middle", 2),
    TX(240, 218, "GPT-2 2019", "tm", 11, "middle", 2),
    R(334, 62, 66, 138, "n2", 3),
    TX(367, 54, "175B", "tb", 12, "middle", 3),
    TX(367, 218, "GPT-3 2020", "tm", 11, "middle", 3),
    TX(240, 244, "구조는 그대로, 파라미터와 글의 양만 늘렸어요", "tb", 13, "middle", 4),
)

FIG_ICL = SVG(
    TX(240, 20, "가르치되 학습시키지는 않기", "tb", 16),
    R(10, 34, 148, 120, "box", 1),
    TX(84, 54, "zero-shot", "tb", 14, "middle", 1),
    TX(84, 80, "Translate to Korean:", "t", 11, "middle", 1),
    TX(84, 100, "cheese →  ?", "tb", 12, "middle", 1),
    TX(84, 140, "예시 0개", "tm", 11, "middle", 1),
    R(166, 34, 148, 120, "box", 2),
    TX(240, 54, "one-shot", "tb", 14, "middle", 2),
    TX(240, 78, "sea otter → 해달", "t", 11, "middle", 2),
    TX(240, 100, "cheese →  ?", "tb", 12, "middle", 2),
    TX(240, 140, "예시 1개", "tm", 11, "middle", 2),
    R(322, 34, 148, 120, "box2", 3),
    TX(396, 54, "few-shot", "tb", 14, "middle", 3),
    TX(396, 76, "sea otter → 해달", "t", 11, "middle", 3),
    TX(396, 94, "plush giraffe → 봉제 기린", "t", 10, "middle", 3),
    TX(396, 114, "cheese →  ?", "tb", 12, "middle", 3),
    TX(396, 140, "예시 2개", "tm", 11, "middle", 3),
    TX(240, 190, "가중치는 한 번도 바뀌지 않아요", "tb", 14, "middle", 4),
    TX(240, 214, "예시는 다음 토큰 분포를 기울일 뿐이에요", "t", 13, "middle", 4),
    TX(240, 238, "아주 큰 모델에서만 되기 시작해요", "tm", 12, "middle", 4),
)

FIG_TWOWAY = SVG(
    TX(240, 20, "사전 학습 모델을 쓰는 두 길", "tb", 16),
    R(14, 36, 214, 96, "box", 1),
    TX(121, 58, "미세조정", "tb", 15, "middle", 1),
    TX(121, 82, "가중치가 바뀌어요", "t", 12, "middle", 1),
    TX(121, 104, "레이블과 GPU 가 필요해요", "t", 12, "middle", 2),
    TX(121, 124, "끝나면 가중치를 내가 가져요", "tm", 11, "middle", 2),
    R(252, 36, 214, 96, "box2", 1),
    TX(359, 58, "프롬프팅", "tb", 15, "middle", 1),
    TX(359, 82, "입력 글만 바뀌어요", "t", 12, "middle", 1),
    TX(359, 104, "좋은 프롬프트가 필요해요", "t", 12, "middle", 3),
    TX(359, 124, "끝나면 문자열 하나가 남아요", "tm", 11, "middle", 3),
    TX(240, 166, "데이터가 있고 과제가 고정이면 미세조정", "tb", 13, "middle", 4),
    TX(240, 190, "데이터가 없거나 과제가 많으면 프롬프팅", "tb", 13, "middle", 4),
    TX(240, 220, "Lab 4 는 왼쪽 길이에요. 한국어 BERT 를 직접 미세조정해요", "tm", 12, "middle", 4),
)

FIG_ENCDEC = SVG(
    TX(240, 20, "읽기는 BERT 처럼, 쓰기는 GPT 처럼", "tb", 16),
    R(20, 60, 170, 74, "box", 1),
    TX(105, 88, "인코더", "tb", 15, "middle", 1),
    TX(105, 110, "양방향", "t", 12, "middle", 1),
    TX(105, 150, "입력 전체를 읽어요", "tm", 11, "middle", 1),
    A(196, 96, 248, 96, "e2", 2),
    TX(222, 84, "크로스 어텐션", "tb", 11, "middle", 2),
    R(254, 60, 170, 74, "box2", 3),
    TX(339, 88, "디코더", "tb", 15, "middle", 3),
    TX(339, 110, "인과 마스킹", "t", 12, "middle", 3),
    TX(339, 150, "한 토큰씩 써요", "tm", 11, "middle", 3),
    TX(240, 192, "번역, 요약처럼 입력도 글이고 출력도 글일 때 자연스러워요", "tb", 13, "middle", 4),
    TX(240, 218, "4주차에 이미 만들었어요. 남은 질문은 어떻게 사전 학습하느냐였어요", "t", 12, "middle", 4),
    TX(240, 242, "그냥 언어 모델로 학습하면 인코더가 아까워요", "tm", 12, "middle", 4),
)

FIG_SPANC = SVG(
    TX(240, 20, "덩어리를 통째로 지우기", "tb", 16),
    TX(12, 54, "원문", "tm", 12, "start", 1),
    *[BOX(60 + i * 72, 38, 66, 24, t, "n", "tl", 1, 10)
      for i, t in enumerate(["Thank you", "for", "inviting", "me to your", "party last", "week"])],
    A(240, 68, 240, 90, "e2", 2),
    TX(12, 116, "인코더 입력", "tm", 11, "start", 2),
    *[BOX(96 + i * 72, 100, 66, 24, t, "n" if not t.startswith("&lt;") else "n2", "tl", 2, 10)
      for i, t in enumerate(["Thank you", "&lt;X&gt;", "me to your", "party", "&lt;Y&gt;"])],
    A(240, 130, 240, 152, "e2", 3),
    TX(12, 178, "디코더 목표", "tm", 11, "start", 3),
    *[BOX(96 + i * 72, 162, 66, 24, t, "box2" if t.startswith("&lt;") else "n", "tl", 3, 10)
      for i, t in enumerate(["&lt;X&gt;", "for inviting", "&lt;Y&gt;", "last", "&lt;Z&gt;"])],
    TX(240, 216, "디코더는 빠진 덩어리만 다시 써요", "tb", 13, "middle", 4),
    TX(240, 240, "인코더와 디코더를 한 번에 학습시켜요", "tm", 12, "middle", 4),
)

FIG_T2T = SVG(
    TX(240, 20, "모든 과제가 글 들어가고 글 나오기", "tb", 16),
    *[BOX(8, 40 + i * 44, 168, 32, t, "box", "tl", 1, 10)
      for i, t in enumerate(["translate English to German:",
                             "cola sentence:",
                             "stsb sentence1: ... sentence2:",
                             "summarize: ..."])],
    *[A(180, 56 + i * 44, 210, 120, "e2", 2) for i in range(4)],
    BOX(212, 104, 56, 32, "T5", "box2", "tb", 2, 16),
    *[A(270, 120, 300, 56 + i * 44, "e2", 3) for i in range(4)],
    *[BOX(304, 40 + i * 44, 168, 32, t, "box", "tl", 3, 10)
      for i, t in enumerate(["Das ist gut.", "not acceptable", "3.8",
                             "six people hospitalized ..."])],
    TX(240, 236, "분류도 회귀도 생성도 전부 문자열이 돼요", "tb", 13, "middle", 4),
    TX(240, 258, "과제마다 출력 층을 따로 만들지 않아요", "tm", 12, "middle", 4),
    h=270,
)

S = []


def page(p, title, terms, p1, p2=(), p3=(), p4=()):
    S.append({"p": p, "title": title, "terms": list(terms),
              "pass1": list(p1), "pass2": list(p2), "pass3": list(p3), "pass4": list(p4)})


# ---------------------------------------------------------------- p.26
page(26, "더 나은 BERT: RoBERTa 와 SpanBERT",
     ["RoBERTa", "SpanBERT", "BERT", "Span", "Next Sentence Prediction (NSP)",
      "Masked Language Modelling (MLM)", "[MASK]", "Pre-training", "Token", "Corpus"],
     [say(f"{BERT} 다음에 나온 후속 연구 두 개를 보는 쪽이에요.",
          f"{ROB} 는 레시피만 고쳤고, {SPB} 는 가리는 방법을 바꿨어요.",
          "둘 다 구조(모델 생김새)는 그대로 두었어요. 바꾼 것은 학습 방법뿐이에요."),
      analogy("빈칸 채우기 시험지를 더 어렵게",
              "같은 시험지를 더 오래 풀게 하면 성적이 오르고, 한 글자 대신 한 구절을 통째로 비우면 훨씬 어려운 시험이 돼요.",
              ("같은 시험지를 더 오래 풀기", ROB),
              ("한 구절을 통째로 비우기", SPB),
              ("빈칸 채우기 시험지", MLM))],
     [points("슬라이드 영어와 우리말 뜻",
             "Better BERTs = 더 나은 BERT 들",
             "the BERT recipe was under-trained = BERT 는 덜 학습된 상태였다",
             "a harder masking game teaches more = 더 어려운 가리기 게임이 더 많이 가르친다",
             "same architecture, better result = 구조는 같은데 결과는 더 좋다",
             "mask whole spans, not single tokens = 토큰 하나가 아니라 스팬을 통째로 가려라"),
      compare("두 후속 모델을 한 표로",
              ["보는 점", ROB, SPB],
              ["바꾼 것", "학습 시간, 데이터 양, 목적 함수 구성", "가리는 단위"],
              ["구조", "그대로", "그대로"],
              [NSP, "빼 버림", "슬라이드에 언급 없음"],
              ["가리는 단위", f"{TOK} 하나", f"이어진 {SPAN} 통째로"],
              ["슬라이드 결론", "같은 구조, 더 좋은 결과", "더 어렵고 더 쓸모 있는 게임"])],
     [look("슬라이드를 짚어 읽어요",
           (0.055, 0.198, 0.79, 0.040, "부제: 두 후속 연구가 BERT 레시피는 덜 학습됐고, 더 어려운 가리기가 더 가르친다고 보였어요."),
           (0.056, 0.334, 0.464, 0.402, f"왼쪽 주황 상자가 {ROB} 예요. 네 가지를 바꿨어요."),
           (0.100, 0.415, 0.400, 0.180, "네 줄: 훨씬 오래 학습, 훨씬 많은 글, NSP 제거, 동적 마스킹."),
           (0.536, 0.334, 0.400, 0.402, f"오른쪽 보라 상자가 {SPB} 예요. 스팬을 통째로 가려요."),
           (0.568, 0.496, 0.339, 0.052, "토큰 여섯 칸 중 가운데 세 칸이 [M] 이에요. 한 구절이 통째로 사라졌어요."),
           (0.050, 0.762, 0.890, 0.100, "아래 파란 띠: 구조를 바꾸지 않아도 계산과 데이터가 늘면 사전 학습이 좋아져요.")),
      points(f"{ROB} 가 바꾼 네 가지",
             "train much longer = 훨씬 오래 학습해요. 계산을 더 씁니다",
             f"use much more text = 훨씬 많은 {CORPUS}를 씁니다",
             f"drop Next Sentence Prediction = {NSP} 을 아예 뺐어요",
             "use dynamic masking = 매번 새로 무작위 자리를 가려요",
             "결과는 same architecture, better result 예요"),
      steps("동적 마스킹이 무엇이 다른지 세어 봐요",
            [f"원래 {BERT} 는 데이터를 만들 때 가릴 자리를 미리 정해 두었어요",
             "그러면 같은 문장은 매번 같은 자리가 가려져요",
             f"{ROB} 는 문장을 넣을 때마다 가릴 자리를 새로 뽑아요",
             f"같은 문장이라도 볼 때마다 다른 {MASK} 자리가 생겨요",
             "그래서 같은 글로도 더 많은 문제를 만들어 낼 수 있어요"],
            "동적 마스킹은 같은 데이터에서 문제를 더 많이 뽑아 쓰는 방법이에요.",
            "new random masks every time"),
      figure("두 갈래를 한 그림으로", FIG_BETTER,
             "왼쪽은 레시피를 고친 쪽, 오른쪽은 문제를 어렵게 만든 쪽이에요.", 4),
      bg("이 과목 안에서 이어 보기",
         f"가리는 단위 이야기는 N5 p.19-20 의 15 퍼센트 규칙에서 이어져요.",
         f"{SPAN} 을 통째로 가리는 생각은 N5 p.37 의 {SC} 으로 다시 나와요.",
         "아래 파란 띠가 말하는 스케일링 법칙은 N5 p.47 에서 다시 만나요.")],
     [check(f"{ROB} 가 뺀 목적 함수는 무엇인가요",
            [NSP, MLM, NTP, SC], 0,
            f"슬라이드 세 번째 줄에 drop Next Sentence Prediction (NSP) 라고 적혀 있어요."),
      check(f"{SPB} 가 {BERT} 와 다른 점은",
            ["이어진 스팬을 통째로 가려요", "층을 두 배로 쌓아요",
             "인과 마스킹을 써요", "레이블을 사람이 달아 줘요"], 0,
            f"mask whole spans, not single tokens 이에요. 구조는 그대로예요."),
      english("시험 답안 문장",
              f"{ROB} 는 구조를 그대로 두고 더 오래, 더 많은 글로 학습하고 {NSP} 을 빼고 동적 마스킹을 써서 {BERT} 를 이겼다.",
              f"{SPB} 는 가리는 단위를 {TOK} 하나에서 이어진 {SPAN} 으로 바꿔 더 어려운 문제를 냈어요.",
              "로베르타는 레시피, 스팬버트는 문제. 이렇게 두 글자로 갈라 외워요."),
      warn("헷갈리기 쉬운 점",
           "둘 다 구조를 바꾼 것이 아니에요. 층 수도 은닉 차원도 그대로예요.",
           f"{ROB} 가 {NSP} 을 뺐다고 해서 NSP 가 언제나 해롭다는 뜻은 아니에요. 다른 것도 함께 바뀌었어요.",
           "SpanBERT 의 [M] 은 그림에서 줄인 표기예요. 정식 이름은 [MASK] 예요.")])

# ---------------------------------------------------------------- p.27
page(27, "Check Yourself Part 1: 스스로 확인하기",
     ["Encoder", "Next Token Prediction", "Bidirectional Context", "[MASK]",
      "Masked Language Modelling (MLM)", "Pre-training", "Parameter Initialisation",
      "Finetuning", "Task Head", "Body", "Sentence Pair", "Token Tagging",
      "Span Extraction", "Sentiment Analysis", "RoBERTa", "Next Sentence Prediction (NSP)",
      "Gradient Descent", "Entailment"],
     [say("전반부를 다 들었는지 확인하는 쪽이에요. 교수님이 직접 낸 문제 다섯 개예요.",
          "5주차는 수업 녹음이 없어요. 그래서 답은 슬라이드 본문에서 근거를 찾아 정리했어요.",
          "근거가 된 쪽 번호를 풀이마다 적어 두었으니 그 쪽으로 돌아가 확인해 보세요."),
      points("다섯 문제를 우리말로",
             f"1. {ENC}는 왜 {NTP}으로 사전 학습할 수 없나",
             f"2. 고른 15 퍼센트의 80 / 10 / 10 조각에 각각 무슨 일이 일어나고 왜 그런가",
             "3. 사전 학습은 파라미터 초기화다 라는 말이 실제로 무슨 뜻인가",
             "4. 네 가지 미세조정 과제 모양과 각각의 과제 하나씩을 대라",
             f"5. {ROB} 가 {NSP} 을 빼고 더 좋아졌다. 어블레이션 표를 어떻게 읽어야 한다는 뜻인가")],
     [compare("슬라이드 영어와 우리말 뜻",
              ["영어 원문", "뜻"],
              ["Why can an encoder not be pretrained with next-token prediction?",
               "인코더는 왜 다음 토큰 예측으로 사전 학습할 수 없는가"],
              ["Of the 15% of tokens BERT selects, what happens to each 80 / 10 / 10 slice",
               "BERT 가 고른 토큰 15 퍼센트의 80 / 10 / 10 조각에 각각 무슨 일이 생기는가"],
              ["What does pretraining is parameter initialisation actually mean?",
               "사전 학습은 파라미터 초기화다 라는 말이 정확히 무슨 뜻인가"],
              ["Name the four finetuning shapes and one task for each.",
               "네 가지 미세조정 모양과 각각의 과제 하나를 대라"],
              ["What does that tell you about how to read a paper's ablation table?",
               "그것이 논문의 어블레이션 표를 읽는 법에 대해 무엇을 말해 주는가"])],
     [look("다섯 문제를 짚어 읽어요",
           (0.06, 0.212, 0.52, 0.036, "1번: 인코더를 다음 토큰 예측으로 사전 학습할 수 없는 이유. 근거는 N5 p.18 이에요."),
           (0.06, 0.279, 0.64, 0.036, "2번: 15 퍼센트의 80 / 10 / 10. 근거는 N5 p.19 와 p.20 이에요."),
           (0.06, 0.347, 0.48, 0.036, "3번: 사전 학습은 파라미터 초기화다. 근거는 N5 p.13 이에요."),
           (0.06, 0.415, 0.42, 0.036, "4번: 네 가지 과제 모양. 근거는 N5 p.23 이에요."),
           (0.06, 0.482, 0.85, 0.036, "5번: RoBERTa 와 어블레이션 표 읽기. 근거는 N5 p.21 과 p.26 이에요.")),
      steps("2번을 숫자로 미리 풀어 봐요",
            ["토큰 200개짜리 글을 넣었다고 해요",
             "15 퍼센트를 고르면 200 x 0.15 = 30 자리예요",
             "그중 80 퍼센트는 30 x 0.8 = 24 자리이고 [MASK] 로 바뀌어요",
             "10 퍼센트는 30 x 0.1 = 3 자리이고 아무 토큰으로 바뀌어요",
             "남은 3 자리는 그대로 두어요. 24 + 3 + 3 = 30 이에요",
             "손실은 고른 30 자리에서만 세요. 나머지 170 자리는 세지 않아요"],
            "24 / 3 / 3 이고, 세 경우 모두 원래 단어를 맞혀야 해요.",
            "토큰 200개, 15 퍼센트 마스킹, 80/10/10")],
     [exam("N5 Check Yourself",
           "1. Why can an encoder not be pretrained with next-token prediction?",
           f"{ENC}는 왜 {NTP}으로 사전 학습할 수 없나요?",
           [f"근거 쪽은 N5 p.18 이에요. 제목이 Why an Encoder Cannot Be a Language Model 이에요",
            f"{ENC}는 마스크를 걸지 않아서 모든 토큰이 모든 토큰을 봐요. 이것이 {BC}이에요",
            "그러면 다음 단어가 이미 입력 안에 보여요. 슬라이드 빨간 상자: the answer is in the input",
            "정답을 보고 정답을 쓰는 셈이라 슬라이드 표현대로 The model learns nothing 이에요",
            f"그래서 {ENC}에는 다른 게임이 필요해요. 입력 일부를 가리고 되살리는 {MLM}이에요"],
           f"{BC} 때문에 정답이 입력에 이미 보이기 때문이에요. 그래서 대신 {MLM}을 써요."),
      exam("N5 Check Yourself",
           "2. Of the 15% of tokens BERT selects, what happens to each 80 / 10 / 10 slice, and why?",
           "고른 15 퍼센트의 80 / 10 / 10 조각에 각각 무슨 일이 일어나고, 왜 그렇게 하나요?",
           ["근거 쪽은 N5 p.19 와 p.20 이에요",
            f"먼저 전체 {TOK}의 15 퍼센트를 무작위로 골라요. 200개면 30 자리예요",
            f"고른 자리의 80 퍼센트(24 자리)는 {MASK} 으로 바꿔요",
            "10 퍼센트(3 자리)는 아무 토큰으로 바꾸고, 10 퍼센트(3 자리)는 그대로 둬요",
            "세 경우 모두 원래 단어를 맞혀야 해요. 손실은 고른 자리에서만 세요",
            f"왜냐고요? 슬라이드 아래 글대로 {FT} 때는 [MASK] 가 하나도 없어요. 그 표시에 기대면 안 돼요"],
           f"24 / 3 / 3 으로 나누고 셋 다 원래 단어를 맞혀요. {MASK} 이 보일 때만 일하는 버릇을 막으려는 장치예요."),
      exam("N5 Check Yourself",
           "3. What does pretraining is parameter initialisation actually mean?",
           f"{PRE}은 {PI}다 라는 말이 실제로 무슨 뜻인가요?",
           ["근거 쪽은 N5 p.13 이에요. 제목이 The Pretrain to Finetune Paradigm 이에요",
            f"슬라이드 첫 줄: {PRE}은 과제가 아니라 {GD}이 어디서 시작할지 고르는 방법이다",
            "보통은 가중치를 무작위로 두고 시작해요. 그러면 언어를 하나도 모르는 곳에서 출발해요",
            "사전 학습된 가중치를 내려받으면 이미 언어를 아는 곳에서 출발해요",
            "그림 가운데 화살표에 the weights, parameter initialisation 이라고 적혀 있어요",
            "비싼 앞 절반은 남이 한 번 해 두고, 우리는 뒤 절반만 여러 번 해요"],
           f"무작위 출발점 대신 이미 언어를 아는 출발점에서 {GD}을 시작한다는 뜻이에요."),
      exam("N5 Check Yourself",
           "4. Name the four finetuning shapes and one task for each.",
           "네 가지 미세조정 과제 모양과 각각의 과제 하나를 대세요.",
           ["근거 쪽은 N5 p.23 이에요. 제목이 One Encoder, Four Task Shapes 예요",
            f"모양 1 단일 문장: {SENTI} 이나 주제 분류. 답 하나를 내요",
            f"모양 2 {SPAIR}: {ENT} 이나 유사도. 역시 답 하나를 내요",
            f"모양 3 {TT}: 개체명 인식이나 품사 태깅. 토큰마다 답을 내요",
            f"모양 4 {SPX}: 추출형 질의응답. 시작과 끝 두 자리를 가리켜요",
            f"슬라이드 아래 글: {BODY}은 언제나 같은 가중치이고 {HEAD}만 고르면 돼요"],
           f"단일 문장, {SPAIR}, {TT}, {SPX} 네 가지이고 {BODY}은 그대로예요."),
      exam("N5 Check Yourself",
           "5. RoBERTa removed NSP and got better results. What does that tell you about how to read a paper's ablation table?",
           f"{ROB} 가 {NSP} 을 빼고 더 좋아졌어요. 어블레이션 표를 어떻게 읽으라는 뜻일까요?",
           ["근거 쪽은 N5 p.21 과 p.26 이에요",
            f"{BERT} 논문은 {NSP} 이 도움이 된다고 보고했어요 (N5 p.21)",
            f"{ROB} 는 그것을 빼고, 동시에 더 오래, 더 많은 글로 학습했어요 (N5 p.26)",
            "곧 한 번에 한 가지만 바뀐 것이 아니에요. 학습 시간과 데이터 양도 같이 바뀌었어요",
            "어블레이션 표의 한 줄은 그 논문의 나머지 설정이 고정되어 있을 때만 그 부품의 값을 말해 줘요",
            "N5 p.26 아래 파란 띠도 같은 말을 해요. 계산과 데이터만 늘려도 결과가 좋아져요"],
           "어블레이션 결과는 그 설정 안에서만 참이에요. 다른 조건이 함께 바뀌면 원인을 한 가지로 못 잘라요."),
      check(f"{PRE}이 {PI}라는 말의 뜻으로 가장 가까운 것은",
            [f"{GD}의 출발점을 언어를 아는 곳으로 옮기는 것",
             "학습률을 0 으로 두는 것",
             "레이블을 사람이 달아 주는 것",
             "모델 구조를 새로 설계하는 것"], 0,
            "N5 p.13 의 첫 줄 그대로예요. 사전 학습은 과제가 아니라 출발점을 고르는 일이에요."),
      english("시험 답안 문장",
              f"{ENC}는 {BC} 때문에 정답이 입력에 보이므로 {NTP}으로 학습할 수 없다.",
              f"그래서 대신 {MLM}을 써요. 1번 답을 한 문장으로 만든 것이에요.",
              "보인다 - 배울 게 없다 - 그래서 가린다. 세 박자로 외워요."),
      warn("이 쪽을 쓸 때 주의할 점",
           "Check Yourself 는 교수님이 직접 낸 문제라 시험 대비 1순위예요.",
           "5주차는 녹음이 없어서 교수님이 답을 말해 준 기록이 없어요. 위 풀이는 슬라이드 근거로 세운 답이에요.",
           "2번은 숫자를 물을 수 있어요. 80 / 10 / 10 과 손실을 세는 자리를 꼭 함께 외워요.")])

# ---------------------------------------------------------------- p.28
page(28, "10분 쉬는 시간", ["Pre-training", "BERT", "GPT", "T5"],
     [say("쉬는 시간 쪽이에요. 10분 쉬어 갑니다.",
          f"작은 글씨는 half-time, 곧 지금까지가 절반이라는 뜻이에요. 왜 {PRE}을 하는지와 {BERT} 가 그것을 어떻게 하는지를 봤어요.",
          f"아래 줄 Coming up 은 다음 차례 예고예요. 남은 두 구조 {GPT} 와 {T5}, 그리고 그냥 아주 크게 만들면 무슨 일이 생기는지예요.")],
     [], [], [])

# ---------------------------------------------------------------- p.29
page(29, "3부 표지: 디코더와 인코더 디코더",
     ["Decoder", "Encoder", "GPT", "T5", "In-Context Learning", "Gradient"],
     [say("세 번째 부분 표지예요. 제목은 3 Decoders and Encoder-Decoders 예요.",
          f"작은 글씨는 GPT, T5, and learning without gradients 예요.",
          f"{GPT} 와 {T5} 를 보고, {GRAD} 걸음 없이 배우는 {ICL} 까지 간다는 뜻이에요.",
          f"2부는 {ENC} 였어요. 이제 {DEC} 쪽 길을 봅니다.")],
     [], [], [])

# ---------------------------------------------------------------- p.30
page(30, "디코더: 이미 아는 그 목적 함수",
     ["Decoder", "Next Token Prediction", "Language Model (LM)", "Causal Masking",
      "Transformer", "Self-Supervision", "Pre-training", "Token", "Autoregressive",
      "Encoder", "Masked Language Modelling (MLM)"],
     [say(f"{DEC}를 사전 학습하는 방법을 보는 쪽이에요. 놀랍게도 새 목적 함수가 없어요.",
          f"3주차에 RNN {LM}을 학습시킨 그 방법 그대로예요.",
          "주문을 다시 외워요. 글을 토큰으로 자르고, 토큰을 벡터로 바꾸고, 벡터로 다음 토큰을 맞혀요."),
      analogy("휴대폰 자판의 다음 단어 추천",
              "자판이 지금까지 친 글자를 보고 다음 단어를 추천해요. 추천이 틀리면 조금씩 고쳐 가요. 디코더 사전 학습이 딱 이 일이에요.",
              ("지금까지 친 글자", "앞쪽 토큰들"),
              ("추천한 다음 단어", NTP),
              ("추천이 틀린 정도", "손실"))],
     [points("슬라이드 영어와 우리말 뜻",
             "Decoders: The Objective You Already Know = 디코더, 이미 아는 그 목적 함수",
             "A decoder is pretrained exactly the way you trained your RNN language model in Week 3 = 디코더는 3주차 RNN 언어 모델과 똑같이 사전 학습된다",
             "predict the next token, one position at a time = 한 자리씩 다음 토큰을 맞힌다",
             f"same loss as the RNN LM you built in W3 = 3주차에 만든 RNN {LM}과 손실이 같다",
             "no new objective needed = 새 목적 함수가 필요 없다"),
      compare("인코더와 디코더의 목적 함수",
              ["보는 점", ENC, DEC],
              ["볼 수 있는 범위", "앞뒤 전부", "앞만 (인과 마스킹)"],
              ["목적 함수", MLM, NTP],
              ["학습할 때 쓰는 자리", "가린 자리만", "모든 자리"],
              ["잘하게 되는 일", "이해, 분류, 태깅", "이어 쓰기"])],
     [look("슬라이드를 짚어 읽어요",
           (0.060, 0.198, 0.870, 0.055, "부제: 디코더는 3주차 RNN 언어 모델과 똑같은 방식으로 사전 학습돼요."),
           (0.146, 0.663, 0.629, 0.066, "아래 회색 줄이 입력이에요. Iroh goes to make tasty tea 여섯 칸이에요."),
           (0.136, 0.540, 0.650, 0.068, "가운데 보라 띠: Transformer Decoder, causal mask. 인과 마스킹이 걸려 있어요."),
           (0.146, 0.426, 0.629, 0.066, "위 보라 줄이 예측이에요. goes, to, make, tasty, tea, [END] 로 한 칸씩 밀려 있어요."),
           (0.804, 0.470, 0.150, 0.145, "오른쪽 초록 상자: 3주차에 만든 RNN 언어 모델과 손실이 같아요."),
           (0.130, 0.775, 0.730, 0.040, "아래 기울임 글: 새 목적 함수가 필요 없어요. 언어 모델 학습법 그대로예요.")),
      figure("한 칸씩 밀린 예측", FIG_DECOBJ,
             "입력이 한 칸 밀려 정답이 돼요. 그래서 정답을 따로 만들 필요가 없어요.", 4),
      steps("한 문장이 만드는 문제 수를 세어 봐요",
            ["문장은 Iroh goes to make tasty tea 여섯 토큰이에요",
             "1번 자리 Iroh 를 보고 goes 를 맞혀요",
             "2번 자리까지 보고 to, 3번까지 보고 make, 4번까지 보고 tasty 를 맞혀요",
             "5번까지 보고 tea, 6번까지 보고 [END] 를 맞혀요",
             "한 문장에서 문제가 6개 나와요. 사람이 답을 달아 준 것이 하나도 없어요"],
            f"토큰 n 개짜리 문장은 문제 n 개를 공짜로 줘요. 이것이 {SS}이에요.",
            "Iroh goes to make tasty tea"),
      points("4주차와 이어 붙이기",
             f"N4 p.43 에서 배운 {CM}이 이것을 가능하게 해요",
             "미래 칸의 점수를 막지 않으면 정답이 입력에 보여서 문제가 안 돼요",
             f"N3 p.34-36 과 p.46-47 의 {NTP}이 여기서 그대로 다시 나와요",
             f"바뀐 것은 몸통이 RNN 에서 {TRF} {DEC}로 바뀐 것뿐이에요",
             f"{DEC}는 이렇게 학습해서 {AR}로 글을 이어 쓸 수 있게 돼요"),
      bg("기초 다지기 6단원",
         "손실은 정답 토큰의 확률에 로그를 씌우고 음수를 붙인 값이에요.",
         "이것을 교차 엔트로피라고 불러요. N2 p.33 과 N3 p.41 에서 봤어요.",
         "정답 확률이 1 에 가까우면 벌점이 0 에 가까워져요.")],
     [check(f"{DEC}의 사전 학습 목적 함수는 무엇인가요",
            [NTP, MLM, NSP, SC], 0,
            "슬라이드 그대로 predict the next token 이에요. 3주차 RNN 언어 모델과 같아요."),
      check(f"{DEC}가 미래 토큰을 못 보게 막는 장치는",
            [CM, "위치 인코딩", "층 정규화", "잔차 연결"], 0,
            f"N4 p.43 에서 배운 {CM}이에요. 이것이 없으면 정답이 입력에 보여요."),
      english("시험 답안 문장",
              f"{DEC}는 {CM} 아래에서 한 자리씩 맞히는 {NTP}으로 사전 학습된다.",
              f"3주차 RNN {LM}의 목적 함수와 같아요. 새 목적 함수가 없다는 점, 인과 마스킹이 전제라는 점을 꼭 넣어요.",
              "같은 손실, 다른 몸통. 이렇게 한 줄로 외워요."),
      warn("헷갈리기 쉬운 점",
           f"{DEC}는 {MASK} 을 쓰지 않아요. 가리는 것이 아니라 아예 보지 못하게 막는 거예요.",
           f"{MLM}은 가린 자리에서만 손실을 세지만 {NTP}은 모든 자리에서 손실을 세요.",
           "그림의 출력이 한 칸 밀려 있는 것이 핵심이에요. 같은 자리에 같은 단어를 쓰는 게 아니에요.")])

# ---------------------------------------------------------------- p.31
page(31, "GPT(2018): 디코더 쪽 길",
     ["GPT", "BERT", "Decoder", "Encoder", "Parameter", "Byte Pair Encoding (BPE)",
      "Corpus", "Next Token Prediction", "Bidirectional Context", "Pre-training", "Token"],
     [say(f"{GPT} 의 첫 번째 모델 이야기예요. {BERT} 와 같은 2018년에 나왔어요.",
          "같은 해에 정반대 방향으로 건 내기였어요.",
          f"{BERT} 는 전부 읽고 이해를 잘하기로, {GPT} 는 왼쪽에서 오른쪽으로 읽고 쓰기를 잘하기로 했어요."),
      analogy("같은 해, 반대 내기",
              "한 팀은 시험 문제를 다 펼쳐 놓고 푸는 연습을 했고, 다른 팀은 다음 문장을 계속 이어 쓰는 연습을 했어요. 2018년에는 앞 팀이 이긴 듯했어요.",
              ("문제를 다 펼쳐 놓고 풀기", BERT),
              ("다음 문장을 이어 쓰기", GPT),
              ("펼쳐 놓고 보는 눈", BC))],
     [points("슬라이드 영어와 우리말 뜻",
             "The Decoder Route = 디코더 쪽 길",
             "The same year as BERT, the opposite bet = BERT 와 같은 해, 반대 방향의 내기",
             "read left to right = 왼쪽에서 오른쪽으로 읽는다",
             "become good at writing rather than at understanding = 이해보다 쓰기를 잘하게 된다",
             "in 2018 the encoder bet looked like the winner = 2018년에는 인코더 쪽 내기가 이긴 듯 보였다",
             "that lasted about two years = 그것이 2년쯤 갔다"),
      compare("두 내기를 한 표로",
              ["보는 점", f"{BERT} ({ENC})", f"{GPT} ({DEC})"],
              ["읽는 방향", "앞뒤 전부", "왼쪽에서 오른쪽"],
              ["잘하게 되는 일", "이해", "쓰기"],
              ["학습 방법", MLM, NTP],
              ["나온 해", "2018", "2018"])],
     [look("슬라이드를 짚어 읽어요",
           (0.060, 0.198, 0.820, 0.040, "부제: BERT 와 같은 해, 반대 내기. 왼쪽에서 오른쪽으로 읽고 쓰기를 잘하게 되자."),
           (0.131, 0.445, 0.464, 0.099, "보라 상자 네 개: 12 층, 1억 1700만 파라미터, 은닉 768, BPE 병합 4만 개."),
           (0.130, 0.575, 0.500, 0.035, "trained on: BooksCorpus, 출간되지 않은 책 7천 권이 넘어요."),
           (0.265, 0.610, 0.360, 0.030, "작은 글씨: 길고 이어진 산문이 먼 거리 구조를 가르쳐요."),
           (0.632, 0.419, 0.279, 0.274, "오른쪽 회색 상자: 같은 해, 반대 내기. BERT 는 이해, GPT 는 쓰기."),
           (0.240, 0.720, 0.520, 0.035, "아래 기울임 글: 2018년엔 인코더 쪽이 이긴 듯했지만 2년쯤 갔어요.")),
      steps(f"{GPT} 와 {BERT} 의 숫자를 나란히 놓아 봐요",
            ["GPT-1 은 층 12, 은닉 768, 파라미터 1억 1700만 개예요",
             "BERT-base 는 층 12, 은닉 768, 파라미터 1억 1000만 개예요 (N5 p.22)",
             "층과 은닉 차원은 완전히 같아요",
             "파라미터는 117 - 110 = 7 로 700만 개 차이예요",
             f"곧 크기가 아니라 마스크와 목적 함수가 둘을 갈라요"],
            "덩치는 거의 같고 보는 방향만 달라요. 그 차이가 잘하는 일을 갈랐어요.",
            "GPT-1 117M, BERT-base 110M"),
      points(f"{BPE} 와 {CORPUS} 이야기",
             f"슬라이드의 40k BPE merges 는 병합 규칙 4만 개를 뜻해요. {BPE} 는 2주차에 배웠어요",
             f"자주 붙어 다니는 두 조각을 한 조각으로 붙이는 그 방법이에요",
             f"{CORPUS}는 BooksCorpus 예요. 출간되지 않은 책이 7천 권 넘게 들어 있어요",
             "슬라이드가 이유를 적어 뒀어요. 길고 이어진 산문이 먼 거리 구조를 가르쳐 준다는 것이에요",
             "짧은 글 조각만 모으면 긴 문맥을 배우기 어렵다는 뜻이에요"),
      figure("같은 해 반대 내기", FIG_BET,
             "덩치는 비슷한데 보는 방향이 달라서 잘하는 일이 갈렸어요.", 4)],
     [check("GPT-1 의 파라미터 수는",
            ["117M", "110M", "340M", "175B"], 0,
            "슬라이드 두 번째 상자에 117M parameters 라고 적혀 있어요. BERT-base 는 110M 이에요."),
      check(f"{GPT} 가 학습한 {CORPUS}는",
            ["BooksCorpus", "English Wikipedia", "GLUE", "NSMC"], 0,
            "trained on BooksCorpus, over 7,000 unpublished books 라고 적혀 있어요."),
      english("시험 답안 문장",
              f"{GPT}(2018)는 12층 768 은닉 1억 1700만 {PARAM}의 {DEC} 모델이다.",
              f"BooksCorpus 로 {NTP} 학습했어요. {BERT} 는 앞뒤 전부, {GPT} 는 왼쪽에서 오른쪽이에요.",
              "12, 768, 117M, 그리고 BPE 병합 4만. 네 숫자를 묶어 외워요."),
      warn("헷갈리기 쉬운 점",
           "슬라이드 오른쪽 아래 번호는 29 / 48 이지만 우리 번호로는 N5 p.31 이에요.",
           f"{GPT} 가 2018년에 졌다는 뜻이 아니에요. 그때는 인코더가 이긴 듯 보였을 뿐이에요.",
           f"{BPE} 병합 4만 개는 어휘 크기와 비슷한 말이지만 같은 수는 아니에요.")])

# ---------------------------------------------------------------- p.32
page(32, "디코더를 미세조정하기",
     ["Decoder", "Finetuning", "[CLS]", "Delimiter", "Entailment", "Task Head",
      "Body", "Downstream Task", "Token", "Classification", "GPT", "BERT",
      "Sentence Pair", "Parameter Initialisation"],
     [say(f"{DEC}를 우리 과제에 맞추는 방법을 보는 쪽이에요.",
          f"{BERT} 에는 {CLS} 가 있었지만 {GPT} 에는 없어요. 둘째 입력 줄도 없어요.",
          f"대신 과제를 한 줄로 쭉 펴서 넣고 마지막 자리에서 답을 읽어요."),
      analogy("공구 날을 갈아 끼우는 대신 재료를 한 줄로 펴기",
              "인코더는 몸통 위에 날만 갈아 끼웠어요. 디코더는 날을 바꾸는 대신 재료를 한 줄로 길게 펴서 기계에 밀어 넣어요.",
              ("갈아 끼우는 공구 날", HEAD),
              ("한 줄로 편 재료", "구분자로 이어 붙인 토큰 줄"),
              ("기계 본체", BODY))],
     [points("슬라이드 영어와 우리말 뜻",
             "Finetuning a Decoder = 디코더를 미세조정하기",
             "There is no [CLS] token and no second stream = [CLS] 토큰도 없고 둘째 입력 줄도 없다",
             "You flatten the task into one token sequence = 과제를 한 줄짜리 토큰 줄로 편다",
             "with special delimiters = 특별한 구분자를 끼워서",
             "read the answer off the last position = 마지막 자리에서 답을 읽는다",
             "no new architecture = 새 구조는 없다"),
      compare("같은 과제, 두 가지 미세조정 방법",
              ["보는 점", f"{BERT} 방식", f"{GPT} 방식"],
              ["답을 읽는 자리", CLS, "마지막 자리"],
              ["문장 두 개 넣는 법", f"{SEP} 로 나눠 두 줄처럼", f"{DELIM} 하나로 이어 한 줄로"],
              ["위에 얹는 것", HEAD, "선형 분류기 한 층"],
              ["바뀌는 것", "몸통 + 헤드", "몸통 + 선형 층"])],
     [look("슬라이드를 짚어 읽어요",
           (0.060, 0.198, 0.880, 0.055, "부제: [CLS] 도 둘째 줄도 없어요. 한 줄로 펴서 마지막 자리에서 답을 읽어요."),
           (0.100, 0.427, 0.450, 0.110, "과제는 natural language inference 예요. 전제와 가설 두 문장이 주어져요."),
           (0.660, 0.470, 0.130, 0.060, "정답 후보는 함의, 모순, 중립 셋이에요. 여기서는 함의예요."),
           (0.330, 0.575, 0.340, 0.035, "가운데 굵은 글: 디코더를 위한 한 줄짜리 토큰 줄."),
           (0.093, 0.618, 0.771, 0.058, "[START], 전제, [DELIM], 가설, [EXTRACT] 다섯 칸으로 이어 붙였어요."),
           (0.762, 0.676, 0.150, 0.060, "[EXTRACT] 자리 위에 선형 분류기를 얹어 답을 읽어요.")),
      figure("과제를 한 줄로 펴기", FIG_FLAT,
             "구분자를 끼워 한 줄로 만들고, 마지막 자리 위에 선형 층 하나만 올려요.", 4),
      points(f"{ENT} 과제가 무엇인지",
             "슬라이드의 natural language inference 는 두 문장의 관계를 묻는 과제예요",
             "전제: The man is in the doorway (그 남자는 문간에 있다)",
             "가설: The person is near the door (그 사람은 문 가까이에 있다)",
             f"전제가 참이면 가설도 참이므로 답은 {ENT} 이에요",
             "나머지 후보는 모순(contradiction)과 중립(neutral)이에요",
             f"이것은 N5 p.23 의 네 모양 중 {SPAIR} 자리에 들어가요"),
      steps("특별한 토큰 세 개가 하는 일",
            ["[START] 는 줄의 시작을 알려요",
             f"[DELIM] 은 전제와 가설 사이를 끊어요. 이것이 {DELIM} 이에요",
             "[EXTRACT] 는 줄의 끝이자 답을 읽을 자리예요",
             f"{BERT} 의 {SEP} 와 역할이 비슷하지만 이름이 달라요",
             f"{BODY}은 사전 학습된 것을 그대로 쓰고, 선형 층 하나만 새로 얹어요. 이것이 {TL} 이에요"],
            "새 구조는 없어요. 특별한 토큰 몇 개와 선형 층 하나면 끝이에요.",
            "[START], [DELIM], [EXTRACT]")],
     [check(f"{GPT} 미세조정에서 답을 읽는 자리는",
            ["마지막 자리 [EXTRACT]", CLS, "첫 번째 자리", "가운데 자리"], 0,
            "슬라이드 그대로 read the answer off the last position 이에요."),
      check(f"{GPT} 에 {CLS} 가 없는 이유로 알맞은 것은",
            ["디코더는 앞만 보므로 마지막 자리가 문장 전체를 본 자리예요",
             "디코더는 토큰을 쓰지 않아요",
             "CLS 는 T5 전용이에요",
             "파라미터를 아끼려고 뺐어요"], 0,
            "앞만 보는 구조에서는 마지막 자리가 앞의 모든 토큰을 본 유일한 자리예요."),
      english("시험 답안 문장",
              f"{DEC} {FT}은 과제를 {DELIM} 로 이어 붙인 한 줄 토큰 줄로 펴고, 마지막 자리 위에 선형 층 하나만 올려 답을 읽는다.",
              f"새 구조가 없다는 점이 핵심이에요. {BODY}은 그대로 두고 {PI}만 이어받아요.",
              "펴고, 끊고, 마지막에서 읽는다. 세 동사로 외워요."),
      warn("헷갈리기 쉬운 점",
           f"{DELIM} 는 {SEP} 와 역할이 비슷하지만 이름과 구조가 달라요. 시험에서 바꿔 쓰지 마세요.",
           f"{DOWN}를 한 줄로 편다고 해서 {CLSF} 가 생성으로 바뀌는 것은 아니에요. 답은 여전히 레이블 하나예요.",
           "슬라이드 문장의 contradiction 과 neutral 사이 기호는 원본에 가운뎃점이 있어요. 우리는 쉼표로 적어요.")])

# ---------------------------------------------------------------- p.33
page(33, "그다음엔 그냥 크게 만들었어요",
     ["GPT", "Parameter", "Large Language Model (LLM)", "In-Context Learning",
      "Prompt", "Finetuning", "Downstream Task", "Transformer", "Pre-training", "Autoregressive"],
     [say(f"GPT-1 에서 GPT-3 까지 무엇이 바뀌었는지 보는 쪽이에요.",
          "답은 거의 아무것도 안 바뀌었다는 것이에요. 구조 이야기가 아니에요.",
          f"바뀐 것은 {PARAM} 수와 글의 양뿐이에요."),
      points("세 모델의 크기",
             "GPT-1 (2018): 1억 1700만 개, 그림에는 0.117B 로 적혀 있어요",
             "GPT-2 (2019): 15억 개, 그림에는 1.5B 로 적혀 있어요",
             "GPT-3 (2020): 1750억 개, 그림에는 175B 로 적혀 있어요",
             f"이쯤 되면 {LLM} 이라고 부를 만해요")],
     [points("슬라이드 영어와 우리말 뜻",
             "Then They Just Made It Bigger = 그다음엔 그냥 크게 만들었다",
             "not a story about architecture = 구조에 대한 이야기가 아니다",
             "Almost nothing changed except the number of parameters and the amount of text = 파라미터 수와 글의 양 말고는 거의 아무것도 안 바뀌었다",
             "two years, 1500x more parameters = 2년 동안 파라미터 1500배",
             "the model starts doing tasks it was never finetuned on = 미세조정한 적 없는 과제를 하기 시작한다",
             "you describe the task in the prompt = 프롬프트에 과제를 설명한다"),
      compare("무엇이 달라졌나",
              ["모델", PARAM, "쓰는 방법"],
              ["GPT-1 (2018)", "0.117B", f"{PRE} 뒤 과제마다 {FT}"],
              ["GPT-2 (2019)", "1.5B", "미세조정한 적 없는 과제도 해내기 시작"],
              ["GPT-3 (2020)", "175B", f"{PROMPT} 에 과제를 설명, 기울기 걸음 0"])],
     [look("슬라이드를 짚어 읽어요",
           (0.060, 0.198, 0.880, 0.055, "부제: 구조 이야기가 아니에요. 파라미터 수와 글의 양만 바뀌었어요."),
           (0.166, 0.380, 0.300, 0.038, "그림 제목: 2년 동안 파라미터 1500배."),
           (0.068, 0.420, 0.410, 0.290, "막대 세 개. 세로축이 로그라서 175B 막대가 그나마 그려져요."),
           (0.554, 0.400, 0.360, 0.038, "오른쪽 제목: 그동안 무엇이 바뀌었나."),
           (0.554, 0.460, 0.400, 0.230, "GPT-1 은 과제마다 미세조정, GPT-2 는 안 배운 과제도 수행, GPT-3 은 프롬프트로 지시."),
           (0.554, 0.705, 0.380, 0.035, "기울임 글: 구조는 아무것도 안 바뀌었고 크기만 바뀌었어요.")),
      steps("1500배를 직접 계산해 봐요",
            ["GPT-1 은 0.117B, GPT-3 은 175B 예요",
             "175 / 0.117 을 계산해요",
             "175 / 0.117 = 약 1495.7 이에요",
             "반올림하면 약 1500 배예요. 슬라이드 제목의 1500x 와 같아요",
             "중간 단계도 보면 1.5 / 0.117 = 약 12.8 배, 175 / 1.5 = 약 116.7 배예요"],
            "2018년에서 2020년까지 2년 만에 약 1500배가 됐어요.",
            "0.117B, 1.5B, 175B"),
      figure("2년 동안 약 1500배", FIG_BIGGER,
             "막대 높이는 로그 눈금이에요. 실제 차이는 그림보다 훨씬 커요.", 4),
      points("로그 눈금이 무엇인지",
             "세로축에 10의 -1승, 10의 0승, 10의 1승, 10의 2승이 적혀 있어요",
             "한 칸 올라갈 때마다 10배가 된다는 뜻이에요",
             "0.117 과 175 를 같은 그림에 그리려면 이렇게 해야 해요",
             "보통 눈금이면 GPT-1 막대는 보이지도 않아요",
             f"같은 로그 눈금이 N5 p.47 의 스케일링 법칙 그림에도 나와요"),
      bg("기초 다지기 4단원",
         "로그는 몇 배인지를 덧셈으로 바꿔 주는 도구예요.",
         "10을 세 번 곱하면 1000 이고, 로그로는 3 이에요.",
         "그래서 10배 차이가 그림에서는 같은 간격이 돼요.")],
     [check("GPT-1 에서 GPT-3 까지 파라미터는 약 몇 배가 됐나요",
            ["약 1500배", "약 15배", "약 150배", "약 15000배"], 0,
            "175 / 0.117 = 약 1495.7 이고 슬라이드 제목은 1500x 라고 적었어요."),
      check("GPT-1 에서 GPT-3 사이에 바뀐 것으로 슬라이드가 든 것은",
            [f"{PARAM} 수와 글의 양", "어텐션 방식", "토크나이저 종류", "손실 함수"], 0,
            "Almost nothing changed except the number of parameters and the amount of text 예요."),
      english("시험 답안 문장",
              f"GPT-1 에서 GPT-3 까지 {TRF} 구조는 거의 그대로이고 {PARAM} 수와 학습 글의 양만 약 1500배로 커졌다.",
              f"크기만 키웠더니 {FT} 없이 {DOWN}를 하기 시작했다는 것이 이 쪽의 핵심이에요.",
              "0.117, 1.5, 175. 세 숫자를 묶어 외워요."),
      warn("헷갈리기 쉬운 점",
           "1500배는 파라미터 수 이야기예요. 성능이 1500배 좋아졌다는 뜻이 아니에요.",
           f"GPT-2 가 {FT} 없이 과제를 한다는 말은 {AR} 생성으로 답을 만들어 낸다는 뜻이에요.",
           "그림의 세로축은 로그 눈금이에요. 막대 높이를 그대로 비율로 읽으면 안 돼요.")])

# ---------------------------------------------------------------- p.34
page(34, "인컨텍스트 러닝",
     ["In-Context Learning", "Prompt", "Zero-shot", "Few-shot", "Gradient",
      "Parameter", "Finetuning", "Token", "Large Language Model (LLM)", "GPT"],
     [say(f"{ICL} 을 보는 쪽이에요. 이름이 길지만 하는 일은 아주 단순해요.",
          f"{PROMPT} 안에 예시를 몇 개 적어 주면 모델이 그대로 따라 해요.",
          f"{GRAD} 걸음도 없고 가중치 갱신도 전혀 없어요."),
      analogy("시험지 맨 위에 예시 문제 두세 개",
              "시험지 맨 위에 풀이가 적힌 예시 문제 두세 개를 붙여 줬어요. 학생은 그것을 보고 아래 문제를 풀어요. 하지만 머릿속이 바뀌지는 않아요.",
              ("맨 위의 예시 문제", "프롬프트 안 예시"),
              ("아래 진짜 문제", "우리가 풀게 하려는 질문"),
              ("머릿속이 바뀌지 않음", "가중치가 그대로"))],
     [points("슬라이드 영어와 우리말 뜻",
             "In-Context Learning = 문맥 안에서 배우기",
             "Give the model a few examples inside the prompt = 프롬프트 안에 예시 몇 개를 준다",
             "with no gradient steps and no weight updates at all = 기울기 걸음도 가중치 갱신도 전혀 없이",
             "the weights never change = 가중치는 절대 바뀌지 않는다",
             "the examples only condition the next-token distribution = 예시는 다음 토큰 분포를 기울일 뿐이다",
             "this only starts working at very large scale = 아주 큰 규모에서만 되기 시작한다"),
      compare("예시를 몇 개 주느냐",
              ["이름", "프롬프트 안 예시 수", "슬라이드 예"],
              [ZS, "0개", "Translate to Korean: cheese →"],
              ["원샷(one-shot)", "1개", "sea otter → 해달 을 보여 준 뒤 cheese →"],
              [FS, "2개", "sea otter, plush giraffe 를 보여 준 뒤 cheese →"])],
     [look("슬라이드를 짚어 읽어요",
           (0.060, 0.198, 0.880, 0.040, "부제: 프롬프트 안에 예시 몇 개를 주면 과제를 해내요. 기울기 걸음이 없어요."),
           (0.066, 0.381, 0.273, 0.305, "왼쪽 파란 상자 zero-shot: 지시문만 있고 예시는 0개예요."),
           (0.363, 0.381, 0.264, 0.305, "가운데 초록 상자 one-shot: 예시가 1개예요."),
           (0.654, 0.381, 0.269, 0.305, "오른쪽 보라 상자 few-shot: 예시가 2개예요."),
           (0.140, 0.715, 0.720, 0.032, "굵은 글: 가중치는 절대 안 바뀌고 예시는 다음 토큰 분포를 기울일 뿐이에요."),
           (0.220, 0.760, 0.560, 0.030, "기울임 글: 아주 큰 규모에서만 되기 시작하고 왜 그런지는 아무도 잘 몰라요.")),
      figure("가르치되 학습시키지는 않기", FIG_ICL,
             "예시 수만 다를 뿐 모델도 가중치도 그대로예요.", 4),
      steps("무엇이 바뀌고 무엇이 안 바뀌는지 세어 봐요",
            [f"{ZS} 은 예시 0개, 원샷은 1개, {FS} 은 2개예요. 합하면 3개",
             f"세 경우 모두 {GRAD} 걸음 수는 0 이에요",
             f"세 경우 모두 바뀐 {PARAM} 개수도 0 이에요",
             f"바뀐 것은 {PROMPT} 에 들어간 {TOK}의 개수뿐이에요",
             "그래서 슬라이드가 learning without gradients 라고 부르는 거예요"],
            "바뀌는 것은 입력 글뿐이에요. 모델 안쪽은 하나도 안 움직여요.",
            "예시 0개, 1개, 2개"),
      points("왜 이 이름이 헷갈리는지",
             f"{ICL} 에는 learning 이 들어 있지만 학습(가중치 갱신)이 아니에요",
             "슬라이드가 직접 말해요. the weights never change 예요",
             "예시는 다음 토큰의 확률 분포를 한쪽으로 기울일 뿐이에요",
             f"{FT}과 가장 크게 다른 점이 바로 이것이에요",
             "그리고 작은 모델에서는 잘 안 돼요. 아주 큰 규모에서만 되기 시작해요")],
     [check(f"{ICL} 에서 바뀌는 것은",
            [PROMPT, PARAM, "학습률", "층 수"], 0,
            "슬라이드 굵은 글: the weights never change. 바뀌는 것은 입력 글뿐이에요."),
      check(f"{FS} 의 뜻으로 알맞은 것은",
            ["프롬프트 안에 예시를 몇 개 적어 주는 방식",
             "데이터를 몇 개만 써서 미세조정하는 방식",
             "층을 몇 개만 학습하는 방식",
             "에폭을 몇 번만 도는 방식"], 0,
            "예시가 프롬프트 안에 들어갈 뿐 학습은 하지 않아요."),
      english("시험 답안 문장",
              f"{ICL} 은 {PROMPT} 안에 예시를 넣어 과제를 시키는 것으로, {GRAD} 걸음이나 가중치 갱신이 전혀 없고 예시는 다음 토큰 분포를 조건 지을 뿐이다.",
              f"학습이라는 말이 들어가지만 {PARAM}는 하나도 안 움직여요.",
              "이름에 러닝이 있어도 러닝이 아니다. 이렇게 외워요."),
      warn("헷갈리기 쉬운 점",
           f"{ZS} 과 {FS} 은 데이터 양 이야기가 아니라 프롬프트 안 예시 수 이야기예요.",
           f"{ICL} 은 {FT}의 한 종류가 아니에요. 가중치를 건드리지 않아요.",
           f"작은 모델에서는 잘 안 돼요. 슬라이드가 {LLM} 규모에서만 시작된다고 적어 뒀어요.")])

# ---------------------------------------------------------------- p.35
page(35, "프롬프팅이냐 미세조정이냐",
     ["Prompting", "Finetuning", "Prompt", "Label", "Parameter", "Pre-training",
      "In-Context Learning", "BERT", "Sentiment Analysis", "Downstream Task",
      "Task Head", "Body", "Transfer Learning", "Classification"],
     [say(f"사전 학습된 모델을 쓰는 두 가지 길을 나란히 놓고 보는 쪽이에요.",
          f"{FT}과 {PROMPTING} 이에요. 둘 다 {PRE} 모델을 써요.",
          "다른 것은 무엇이 바뀌는지, 무엇이 필요한지, 끝나면 무엇이 내 손에 남는지예요."),
      analogy("신입에게 일을 시키는 두 방법",
              "아무 책이나 잔뜩 읽어 둔 신입이 있어요. 우리 회사 일만 며칠 따로 가르칠 수도 있고, 그냥 업무 지시서를 아주 잘 써서 건넬 수도 있어요.",
              ("며칠 따로 가르치기", FT),
              ("업무 지시서를 잘 쓰기", PROMPTING),
              ("책을 잔뜩 읽어 둔 신입", PRE))],
     [points("슬라이드 영어와 우리말 뜻",
             "Prompting or Finetuning? = 프롬프팅이냐 미세조정이냐",
             "Both use a pretrained model = 둘 다 사전 학습된 모델을 쓴다",
             "They differ in what changes, what you need, and what you end up owning = 무엇이 바뀌는지, 무엇이 필요한지, 무엇을 갖게 되는지가 다르다",
             "you keep the weights = 가중치를 내가 갖는다",
             "you keep a string = 문자열 하나를 갖는다",
             "Lab 4 does the left-hand column = Lab 4 는 왼쪽 칸을 한다"),
      compare("슬라이드 표 여섯 줄 그대로",
              ["보는 점", FT, PROMPTING],
              ["무엇이 바뀌나", "가중치", "입력 글만"],
              ["필요한 것", f"{LABEL} 붙은 데이터 + GPU", f"좋은 {PROMPT}"],
              ["모델 크기", "1억 개(100M)부터 됨", "수십억 개가 필요함"],
              ["과제당 비용", "학습 한 번", "처음 드는 비용 없음"],
              ["누가 갖나", "가중치를 내가 가짐", "문자열 하나를 가짐"],
              ["더 나은 경우", "데이터가 있고 과제가 고정일 때", "데이터가 없거나 과제가 많을 때"])],
     [look("슬라이드를 짚어 읽어요",
           (0.060, 0.198, 0.720, 0.040, "부제: 둘 다 사전 학습 모델을 써요. 다른 것은 바뀌는 것과 필요한 것과 남는 것이에요."),
           (0.109, 0.369, 0.792, 0.048, "표 머리: 왼쪽은 finetuning, 오른쪽은 prompting 이에요."),
           (0.109, 0.435, 0.792, 0.060, "you need 줄: 레이블 붙은 데이터와 GPU 대 좋은 프롬프트."),
           (0.109, 0.530, 0.792, 0.060, "model size 줄: 100M 부터 되는 쪽과 수십억 개가 필요한 쪽."),
           (0.109, 0.630, 0.792, 0.095, "who owns it 과 usually better when 두 줄이 실전 선택 기준이에요."),
           (0.220, 0.740, 0.560, 0.034, "아래 굵은 글: Lab 4 는 왼쪽 칸이에요. 한국어 BERT 를 직접 미세조정해요.")),
      figure("두 길을 한 그림으로", FIG_TWOWAY,
             "왼쪽은 가중치가 움직이고 오른쪽은 글만 움직여요.", 4),
      points("표를 실전 기준으로 다시 읽기",
             f"우리에게 {LABEL} 데이터가 있으면 {FT}이 유리해요",
             f"과제가 하나로 고정이면 {FT}이 유리해요. 한 번 학습하고 계속 써요",
             f"데이터가 없거나 과제가 자주 바뀌면 {PROMPTING} 이 유리해요",
             f"다만 {PROMPTING} 은 모델이 아주 커야 잘 돼요. 이것이 {ICL} 이야기와 이어져요",
             f"작은 {BERT} 로 {CLSF} 하나만 잘하면 될 때는 {FT}이 훨씬 싸요"),
      steps("무엇을 갖게 되는지 따져 봐요",
            [f"{FT}을 하면 학습이 끝난 가중치 파일이 남아요",
             "그 파일은 내 컴퓨터에 두고 계속 쓸 수 있어요",
             f"{PROMPTING} 을 하면 잘 쓴 {PROMPT} 문자열 하나가 남아요",
             "모델 자체는 남의 것이고, 모델이 바뀌면 프롬프트도 다시 맞춰야 해요",
             f"슬라이드가 you keep the weights 와 you keep a string 으로 대비했어요"],
            "가중치를 갖느냐 문자열을 갖느냐. 이것이 소유의 차이예요.",
            "who owns it 줄")],
     [check("데이터가 없고 과제가 여러 개일 때 슬라이드가 권하는 쪽은",
            [PROMPTING, FT, "처음부터 학습", "구조 변경"], 0,
            "표 마지막 줄 usually better when: you have no data, or many tasks 예요."),
      check(f"{FT}이 필요로 하는 것으로 슬라이드가 적은 것은",
            [f"{LABEL} 붙은 데이터와 GPU", "수십억 파라미터 모델", "좋은 프롬프트", "아무것도 필요 없음"], 0,
            "you need 줄에 labelled data + a GPU 라고 적혀 있어요."),
      english("시험 답안 문장",
              f"{FT}은 가중치를 바꾸고 {LABEL} 데이터와 GPU 가 필요하다. {PROMPTING} 은 입력 글만 바꾼다.",
              f"둘 다 {PRE} 모델을 쓰는 {TL} 이에요. 바뀌는 것, 필요한 것, 남는 것을 나눠 쓰면 좋아요.",
              "바뀌는 것, 필요한 것, 남는 것. 세 칸으로 외워요."),
      warn("헷갈리기 쉬운 점",
           f"{PROMPTING} 이 공짜라는 뜻이 아니에요. 처음 드는 비용이 없다는 뜻이고 부를 때마다 비용이 들어요.",
           f"{FT}은 {BODY}만 건드리는 것이 아니라 {HEAD}도 함께 학습해요.",
           "표의 100M 은 1억 개예요. BERT-base 가 딱 이 크기예요.")])

# ---------------------------------------------------------------- p.36
page(36, "인코더 디코더: 세 번째 선택지",
     ["Encoder", "Decoder", "Cross-Attention", "Machine Translation (MT)",
      "Span Corruption", "Denoising", "Causal Masking", "Bidirectional Context",
      "T5", "BERT", "GPT", "Language Model (LM)", "Self-Attention", "Pre-training"],
     [say("세 번째 구조를 보는 쪽이에요. 인코더와 디코더를 둘 다 쓰는 구조예요.",
          f"이것은 새 구조가 아니에요. 여러분이 4주차에 이미 만들었어요.",
          "4주차에서 인코더는 양쪽을 다 보고 디코더는 앞만 본다고 배웠죠. 그 구분이 여기서 값을 해요."),
      analogy("읽는 사람과 쓰는 사람이 따로",
              "한 사람이 원문을 처음부터 끝까지 꼼꼼히 읽고, 옆 사람이 그 사람에게 계속 물어보면서 번역문을 한 단어씩 써 내려가요.",
              ("원문을 다 읽는 사람", ENC),
              ("한 단어씩 쓰는 사람", DEC),
              ("옆 사람에게 물어보기", CA))],
     [points("슬라이드 영어와 우리말 뜻",
             "Encoder-Decoders: The Third Option = 인코더 디코더, 세 번째 선택지",
             "You built one of these in Week 4 = 여러분은 4주차에 이것을 하나 만들었다",
             "The open question was never the architecture = 열려 있던 질문은 구조가 아니었다",
             "it was what objective to pretrain it with = 무슨 목적 함수로 사전 학습하느냐였다",
             "read like BERT, write like GPT = BERT 처럼 읽고 GPT 처럼 쓴다",
             "plain language modelling wastes the encoder = 그냥 언어 모델로 학습하면 인코더가 아깝다"),
      compare("세 구조를 한 표로 (N5 p.17 과 이어짐)",
              ["구조", "볼 수 있는 범위", "사전 학습 목적 함수", "대표 모델"],
              [ENC, "앞뒤 전부", MLM, BERT],
              ["인코더 디코더", "읽을 땐 앞뒤, 쓸 땐 앞만", SC, T5],
              [DEC, "앞만", NTP, GPT])],
     [look("슬라이드를 짚어 읽어요",
           (0.060, 0.198, 0.860, 0.040, "부제: 4주차에 이미 만들었어요. 열린 질문은 구조가 아니라 목적 함수였어요."),
           (0.131, 0.437, 0.232, 0.165, "왼쪽 파란 상자: 인코더, 양방향. 아래 글은 입력 전체를 읽는다는 뜻이에요."),
           (0.368, 0.470, 0.071, 0.057, "가운데 초록 화살표에 cross-attention 이라고 적혀 있어요."),
           (0.446, 0.437, 0.234, 0.165, "오른쪽 보라 상자: 디코더, 인과. 아래 글은 한 토큰씩 쓴다는 뜻이에요."),
           (0.716, 0.426, 0.191, 0.216, "초록 상자 natural for: 번역, 요약, 입력도 글이고 출력도 글인 과제."),
           (0.200, 0.675, 0.600, 0.070, "아래 두 줄: 4주차에 만들었다, 그냥 언어 모델로 학습하면 인코더가 아깝다.")),
      figure("읽기는 BERT 처럼, 쓰기는 GPT 처럼", FIG_ENCDEC,
             "왼쪽은 양방향으로 읽고 오른쪽은 인과 마스킹으로 한 토큰씩 써요.", 4),
      points("4주차와 정확히 어디서 이어지는지",
             f"N4 p.52-53 에서 {ENC}와 {DEC}를 나눠 배웠어요. 그 구분이 여기서 값을 해요",
             f"{ENC}는 마스크가 없어서 {BC}을 봐요. 그래서 {BERT} 가 됐어요",
             f"{DEC}는 {CM}이 걸려서 앞만 봐요. 그래서 {GPT} 가 됐어요",
             f"둘을 이어 붙이면 이 쪽의 인코더 디코더가 되고 그것이 {T5} 예요",
             f"두 쪽을 잇는 다리가 {CA}이에요. N4 p.21-23 의 어텐션 네 단계 그대로예요",
             f"인코더 디코더 스택의 원본 그림은 논문 덱 NP p.3 에서 원문으로 봐요"),
      points("왜 목적 함수가 문제였는지",
             f"{ENC}와 {DEC}를 붙여 놓고 그냥 {LM}처럼 다음 토큰만 맞히게 하면",
             "디코더만 열심히 일하고 인코더는 별로 배울 것이 없어요",
             "슬라이드 표현이 plain language modelling wastes the encoder 예요",
             f"그래서 Raffel 등이 더 나은 게임을 찾았어요. 그것이 {SC}이에요",
             f"{SC}은 {DEN} 계열이에요. 망가뜨린 글을 되돌리게 시켜요"),
      bg("4주차 복습 카드",
         f"{SELF}은 한 시퀀스가 자기 자신을 보는 어텐션이에요.",
         f"{CA}은 쿼리가 디코더, 키와 밸류가 인코더에서 와요.",
         "인코더와 디코더는 같은 블록을 쓰고 마스크만 달라요.")],
     [check("인코더 디코더가 가장 자연스러운 과제는",
            [f"{MT} 과 요약", "감성 분류", "품사 태깅", "다음 단어 추천"], 0,
            "슬라이드 초록 상자에 translation, summarisation 이 적혀 있어요. 입력도 글, 출력도 글이에요."),
      check("인코더 디코더에서 두 쪽을 이어 주는 부품은",
            [CA, SELF, CM, "층 정규화"], 0,
            f"슬라이드 가운데 화살표에 cross-attention 이라고 적혀 있어요. N4 에서 배운 그 다리예요."),
      english("시험 답안 문장",
              f"인코더 디코더는 {ENC}가 {BC}으로 읽고 {DEC}가 한 토큰씩 쓰며 둘을 {CA}이 잇는다.",
              f"{SC}으로 사전 학습해요. 4주차의 구분이 {BERT} 와 {GPT} 로 갈렸고 둘을 합친 것이 이 구조예요.",
              "읽기는 BERT, 쓰기는 GPT. 이 한 줄로 외워요."),
      warn("헷갈리기 쉬운 점",
           f"인코더 디코더는 새 구조가 아니에요. 4주차에 이미 만든 것이에요.",
           f"{CA}과 {SELF}을 섞지 마세요. 크로스는 두 시퀀스, 셀프는 한 시퀀스예요.",
           f"{ENC} 쪽에는 {CM}이 없어요. 인과 마스킹은 {DEC} 쪽에만 걸려요.")])

# ---------------------------------------------------------------- p.37
page(37, "T5: 스팬 손상",
     ["T5", "Span Corruption", "Span", "Sentinel Token", "Denoising", "Encoder",
      "Decoder", "Masked Language Modelling (MLM)", "SpanBERT", "Token",
      "Self-Supervision", "Pre-training"],
     [say(f"{T5} 가 쓰는 사전 학습 게임을 보는 쪽이에요. 이름이 {SC}이에요.",
          f"{TOK} 하나를 가리는 대신 이어진 덩어리를 통째로 지워요.",
          f"그리고 지운 자리마다 번호표를 붙여요. 그 번호표가 {SENT} 이에요."),
      analogy("빈칸 채우기 시험지를 통째 지우기로",
              "한 글자씩 비운 시험지 대신 구절을 통째로 지우고 번호를 붙여요. 학생은 번호별로 빠진 구절만 다시 써 내면 돼요.",
              ("구절을 통째로 지우기", SC),
              ("지운 자리의 번호표", SENT),
              ("번호별로 빠진 구절만 쓰기", "디코더가 하는 일"))],
     [points("슬라이드 영어와 우리말 뜻",
             "T5: Span Corruption = T5 의 스팬 손상",
             "Delete whole spans = 스팬을 통째로 지운다",
             "replace each with a unique sentinel = 지운 자리마다 서로 다른 번호표를 넣는다",
             "make the decoder write the missing pieces back out = 디코더가 빠진 조각만 다시 쓰게 한다",
             "harder than masking one token = 토큰 하나 가리기보다 어렵다",
             "it trains the encoder and the decoder at the same time = 인코더와 디코더를 동시에 학습시킨다"),
      steps("슬라이드 예를 한 단계씩 따라가요",
            ["원문은 Thank you for inviting me to your party last week 열 단어예요",
             "for inviting 을 통째로 지우고 그 자리에 <X> 를 넣어요",
             "last 를 지우고 그 자리에 <Y> 를 넣어요",
             "인코더 입력은 Thank you <X> me to your party <Y> week 가 돼요",
             "디코더 목표는 <X> for inviting <Y> last <Z> 예요",
             "<Z> 는 끝을 알리는 번호표예요"],
            "지운 것은 for, inviting, last 세 단어이고 디코더는 그것만 써요.",
            "Thank you for inviting me to your party last week")],
     [look("슬라이드를 짚어 읽어요",
           (0.060, 0.198, 0.790, 0.040, "부제: 스팬을 통째로 지우고 번호표로 바꾼 뒤 디코더가 빠진 조각을 씁니다."),
           (0.212, 0.369, 0.654, 0.057, "첫 줄 original: 원문 열 단어가 그대로 있어요."),
           (0.212, 0.471, 0.597, 0.056, "둘째 줄 encoder input: <X> 와 <Y> 두 개의 주황 칸이 보여요."),
           (0.212, 0.582, 0.402, 0.056, "셋째 줄 decoder target: <X> for inviting <Y> last <Z> 예요."),
           (0.654, 0.578, 0.135, 0.057, "오른쪽 글: 디코더는 빠진 스팬만 다시 써요."),
           (0.190, 0.688, 0.620, 0.032, "아래 기울임 글: 한 토큰 가리기보다 어렵고 인코더와 디코더를 동시에 학습시켜요.")),
      figure("덩어리를 통째로 지우기", FIG_SPANC,
             "인코더는 구멍 뚫린 글을 읽고, 디코더는 구멍만 채워 써요.", 4),
      steps("디코더가 쓰는 길이를 세어 봐요",
            ["원문은 10 단어예요",
             "인코더 입력은 9 칸이에요. 세 단어가 빠지고 번호표 두 개가 들어갔어요",
             "디코더 목표는 <X> for inviting <Y> last <Z> 로 6 칸이에요",
             "디코더는 원문 전체를 다시 쓰지 않아요. 빠진 부분만 써요",
             "그래서 같은 계산으로 더 많은 문장을 볼 수 있어요"],
            "디코더는 10 칸이 아니라 6 칸만 써요. 빠진 조각만 쓰는 것이 핵심이에요.",
            "원문 10, 인코더 입력 9, 디코더 목표 6"),
      compare(f"{MLM} 과 {SC} 비교",
              ["보는 점", f"{MLM} ({BERT})", f"{SC} ({T5})"],
              ["가리는 단위", f"{TOK} 하나", f"이어진 {SPAN}"],
              ["누가 답을 쓰나", "인코더 위의 출력 층", DEC],
              ["답의 길이", "가린 자리 수만큼", "빠진 조각만"],
              ["학습되는 쪽", "인코더만", "인코더와 디코더 둘 다"]),
      points("이름 정리",
             f"{SC}은 {DEN} 계열의 한 방법이에요",
             f"N5 p.17 슬라이드에도 span corruption (denoising) 이라고 함께 적혀 있어요",
             f"{SPB} 도 스팬을 가렸지만 그쪽은 {ENC} 하나짜리였어요",
             f"{T5} 는 {ENC}와 {DEC}를 둘 다 두고 스팬을 가려요",
             f"셋 다 사람이 답을 달지 않으니 모두 {SS}이에요")],
     [check(f"{SENT} 의 역할은",
            ["지운 자리가 어디였는지 번호로 알려 줘요",
             "문장의 끝을 알려 줘요",
             "문장을 둘로 나눠 줘요",
             "정답 레이블을 담아 둬요"], 0,
            "슬라이드 표현이 replace each with a unique sentinel 이에요. 구멍마다 서로 다른 번호표예요."),
      check(f"{SC}이 {MLM} 보다 나은 점으로 슬라이드가 든 것은",
            [f"{ENC}와 {DEC}를 동시에 학습시켜요",
             "파라미터가 적어요",
             "레이블이 필요 없어요",
             "계산이 더 빨라요"], 0,
            "아래 기울임 글에 it trains the encoder and the decoder at the same time 이라고 적혀 있어요."),
      english("시험 답안 문장",
              f"{SC}은 {SPAN} 을 통째로 지워 {SENT} 으로 바꾸고 디코더가 빠진 조각만 쓰게 하는 게임이다.",
              f"{DEN} 계열이고, {MLM} 과 달리 {ENC}와 {DEC}를 동시에 학습시켜요.",
              "지우고, 번호 붙이고, 그것만 쓴다. 세 단계로 외워요."),
      warn("헷갈리기 쉬운 점",
           f"{DEC}는 원문 전체를 다시 쓰지 않아요. 빠진 조각과 번호표만 써요.",
           f"{SENT} 은 {MASK} 과 달라요. 번호가 달려 있어서 어느 구멍인지 구별돼요.",
           f"{SPB} 도 스팬을 가리지만 그것은 {ENC} 만 있는 모델이에요. {T5} 와 섞지 마세요.")])

# ---------------------------------------------------------------- p.38
page(38, "모든 것이 텍스트-투-텍스트",
     ["T5", "Text-to-Text", "Task Prefix", "Task Head", "Body", "Classification",
      "Machine Translation (MT)", "Downstream Task", "Transfer Learning",
      "BERT", "Label", "Span Corruption"],
     [say(f"{T5} 의 두 번째 아이디어를 보는 쪽이에요.",
          f"과제마다 출력 층을 따로 만드는 일을 그만두자는 것이에요.",
          f"대신 입력 맨 앞에 {TPFX} 를 붙이고 답을 문자열로 쓰게 해요."),
      analogy("공구 날을 아예 없애기",
              "지금까지는 과제마다 날을 갈아 끼웠어요. 이번에는 날을 없애고 기계에게 말로 지시해요. 번역해라, 점수를 매겨라, 요약해라.",
              ("갈아 끼우던 공구 날", HEAD),
              ("말로 하는 지시", TPFX),
              ("기계가 말로 내놓는 답", T2T))],
     [points("슬라이드 영어와 우리말 뜻",
             "Everything Is Text-to-Text = 모든 것이 글 들어가고 글 나오기",
             "stop having task-specific output layers = 과제 전용 출력 층을 그만 쓰자",
             "Put a task prefix in the input = 입력에 과제 접두어를 넣어라",
             "make the model write the answer as a string = 답을 문자열로 쓰게 하라",
             "classification, regression and generation all become text-to-text = 분류도 회귀도 생성도 전부 글이 된다",
             "T5 : Text-to-Text Transfer Transformer = T 다섯 개를 딴 이름이에요"),
      compare("슬라이드의 네 가지 예",
              ["입력 앞에 붙인 과제 접두어", "무슨 과제인가", "모델이 쓴 답"],
              ["translate English to German:", MT, "Das ist gut."],
              ["cola sentence:", "문장이 문법에 맞는지 판정", "not acceptable"],
              ["stsb sentence1: ... sentence2:", "두 문장이 얼마나 비슷한지 점수", "3.8"],
              ["summarize:", "요약", "six people hospitalized after a storm ..."])],
     [look("슬라이드를 짚어 읽어요",
           (0.060, 0.198, 0.870, 0.055, "부제: 과제 전용 출력 층을 그만 쓰고, 접두어를 붙여 답을 문자열로 쓰게 해요."),
           (0.189, 0.366, 0.215, 0.403, "왼쪽 네 상자가 입력이에요. 굵은 글자가 전부 과제 접두어예요."),
           (0.454, 0.502, 0.067, 0.083, "가운데 T5 하나가 네 과제를 모두 받아요."),
           (0.582, 0.366, 0.161, 0.377, "오른쪽 네 상자가 출력이에요. 넷 다 문자열이에요."),
           (0.300, 0.805, 0.400, 0.030, "아래 굵은 글: 분류도 회귀도 생성도 전부 텍스트-투-텍스트가 돼요."),
           (0.270, 0.865, 0.460, 0.045, "맨 아래: T5 는 Text-to-Text Transfer Transformer 의 T 다섯 개예요.")),
      figure("글 들어가고 글 나오기", FIG_T2T,
             "가운데 모델은 하나뿐이고 과제는 접두어로 구별해요.", 4),
      points("세 번째 예가 왜 놀라운지",
             "stsb 는 두 문장이 얼마나 비슷한지를 점수로 매기는 과제예요",
             "보통은 숫자를 내놓는 회귀 문제라서 전용 출력 층이 필요해요",
             f"{T5} 는 그냥 3.8 이라는 문자열을 써요",
             "곧 숫자도 글자로 적어 버리는 거예요",
             f"그래서 슬라이드가 분류도 회귀도 생성도 전부 {T2T} 가 된다고 적었어요",
             f"어느 쪽이든 {PRE} 가중치를 이어 쓰는 {TL} 이라는 점은 같아요"),
      compare(f"{BERT} 방식과 {T5} 방식",
              ["보는 점", f"{BERT} ({HEAD} 방식)", f"{T5} ({T2T} 방식)"],
              ["과제 구분", "과제마다 다른 헤드", TPFX],
              ["출력 모양", f"{LABEL} 번호나 점수", "문자열"],
              [BODY, "그대로 재사용", "그대로 재사용"],
              ["새 과제를 더할 때", "새 헤드를 만들어야 함", "접두어만 새로 적으면 됨"])],
     [check(f"{TPFX} 가 하는 일은",
            ["입력 맨 앞에서 무슨 과제인지 알려 줘요",
             "출력 길이를 정해 줘요",
             "학습률을 정해 줘요",
             "토큰을 가려 줘요"], 0,
            "Put a task prefix in the input 이에요. 같은 모델이 접두어로 과제를 구별해요."),
      check(f"{T2T} 방식에서 두 문장 유사도 점수 3.8 은 어떻게 나오나요",
            ["문자열 3.8 을 그대로 써요", "회귀 층이 숫자를 내요",
             "분류 헤드가 레이블을 내요", "점수를 반올림해서 레이블로 바꿔요"], 0,
            "슬라이드 세 번째 예의 출력이 3.8 이라는 문자열이에요. 회귀도 글로 바꿔 버려요."),
      english("시험 답안 문장",
              f"{T2T} 방식은 출력 층을 없애고 {TPFX} 를 붙여 모든 답을 문자열로 쓰게 한다.",
              f"{CLSF} 와 회귀와 생성을 한 형식으로 통일해요. {HEAD} 를 바꿔 끼우던 {BERT} 방식과 대비해서 써요.",
              "접두어 하나로 과제 구분, 답은 언제나 글자. 두 줄로 외워요."),
      warn("헷갈리기 쉬운 점",
           f"{T2T} 는 {SC}과 다른 이야기예요. 하나는 쓰는 방법, 하나는 사전 학습 게임이에요.",
           f"{TPFX} 는 {PROMPT} 와 비슷해 보이지만 {T5} 는 그 형식으로 실제 {FT}을 해요.",
           "cola 와 stsb 는 GLUE 안의 과제 이름이에요. 이 과목에서 따로 배우지는 않았어요.")])

data = {"deck": "N5", "from": 26, "to": 38,
        "glossary": [{"ko": k, "en": e, "say": s, "more": m} for k, e, s, m in GLOSSARY],
        "slides": S}

raw = json.dumps(data, ensure_ascii=False, indent=1)
for ch in ("—", "–", "·", "・"):
    assert ch not in raw, ch
with open(OUT, "w", encoding="utf-8") as f:
    f.write(raw)
print("saved", OUT, len(S), "pages")
