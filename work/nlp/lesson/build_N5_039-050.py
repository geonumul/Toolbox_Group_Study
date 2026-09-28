# -*- coding: utf-8 -*-
"""5강(N5) Pre-trained Language Models 회독 레슨 39~50쪽 생성기.
사용: python build_N5_039-050.py   출력: N5_039-050.json
5주차는 녹음이 없어서 prof 장면을 만들지 않는다.
손계산은 아래에서 실제 계산해 assert 로 확인한다."""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "N5_039-050.json")


# ---------------- 손계산 확인 (계산하고 assert) ----------------
# p.42 일곱 가지와 신뢰도 세 등급
taught = [("syntax", "reliable"), ("coreference", "reliable"),
          ("lexical semantics", "reliable"), ("sentiment", "reliable"),
          ("world knowledge", "patchy"), ("a little arithmetic", "patchy"),
          ("bias", "unwanted")]
assert len(taught) == 7
assert sum(1 for _, g in taught if g == "reliable") == 4
assert sum(1 for _, g in taught if g == "patchy") == 2
assert sum(1 for _, g in taught if g == "unwanted") == 1
assert 4 + 2 + 1 == 7

# p.44 미세조정 걸음 수 (Lab 4 설정: 학습 15,000건, 배치 32, 에폭 2)
n_train, batch, epochs = 15000, 32, 2
steps_per_epoch = math.ceil(n_train / batch)
assert steps_per_epoch == 469
total_steps = steps_per_epoch * epochs
assert total_steps == 938
# 실습 노트북 N5L p.20 의 코드가 warmup_steps=max(1, int(0.1 * total_steps)) 라서 버림이다.
# 슬라이드는 "처음 약 10 퍼센트" 라고만 적었지만, Lab 4 설정으로 세는 곳이라 노트북 규칙을 따른다.
warm = int(0.10 * total_steps)
assert warm == 93
assert abs(total_steps * 0.10 - 93.8) < 1e-9
# 학습률: 미세조정 2e-5 는 사전 학습보다 100배 작다고 슬라이드가 말해요
ft_lr = 2e-5
assert round(ft_lr * 100, 10) == 0.002
assert 5e-5 / 2e-5 == 2.5

# p.46 PEFT 로 움직이는 파라미터 수 (BERT-base 110M 의 약 1 퍼센트)
total_w = 110_000_000
trainable = round(total_w * 0.01)
assert trainable == 1_100_000
frozen = total_w - trainable
assert frozen == 108_900_000
assert round(frozen / total_w * 100, 1) == 99.0

# p.45 레이블 수와 정확도 (Lab 4 에 저장된 출력)
acc = {500: 80.50, 2000: 84.18, 15000: 87.40}
assert round(acc[2000] - acc[500], 2) == 3.68
assert round(acc[15000] - acc[2000], 2) == 3.22
assert acc[2000] / acc[500] > 1
assert 2000 / 500 == 4.0
assert 15000 / 2000 == 7.5
# 레이블을 4배 늘렸을 때 3.68 오르고, 7.5배 늘렸을 때 3.22 올라요 (수확 체감)
assert round(acc[15000] - acc[500], 2) == 6.90
# 우연 수준과의 거리
assert round(acc[500] - 49.7, 1) == 30.8

# p.47 GPT-3 의 파라미터와 토큰
params_b, tokens_b = 175, 300
assert round(tokens_b / params_b, 2) == 1.71
assert round(175 / 70, 1) == 2.5
# 로그 눈금 한 칸은 10배
assert 10 ** 1 == 10 and 10 ** 2 == 100
assert math.log10(1000) == 3.0

# p.48 네 가지 이유
reasons = ["One expensive step, reused forever", "Labels stop being the bottleneck",
           "One architecture for every task", "It keeps getting better with scale"]
assert len(reasons) == 4

# p.50 세 구조와 세 목적 함수
arch = {"encoder": "masked LM", "encoder-decoder": "span corruption", "decoder": "next-token prediction"}
assert len(arch) == 3
assert sorted(arch) == ["decoder", "encoder", "encoder-decoder"]

# p.49 여섯 문제
assert len([1, 2, 3, 4, 5, 6]) == 6
# 4번 문제의 레이블 수
assert 800 < 2000 and 800 > 500


# ---------------- 용어 표기 ----------------
PRE = "**사전 학습(Pre-training)**"
FT = "**미세조정(Finetuning)**"
TL = "**전이 학습(Transfer Learning)**"
SS = "**자기 지도 학습(Self-Supervision)**"
SL = "**지도 학습(Supervised Learning)**"
PI = "**파라미터 초기화(Parameter Initialisation)**"
BERT = "**버트(BERT)**"
GPT = "**지피티(GPT)**"
T5 = "**티파이브(T5)**"
ENC = "**인코더(Encoder)**"
DEC = "**디코더(Decoder)**"
CM = "**인과 마스킹(Causal Masking)**"
BC = "**양방향 문맥(Bidirectional Context)**"
AR = "**자기회귀(Autoregressive)**"
NTP = "**다음 토큰 예측(Next Token Prediction)**"
MLM = "**마스크 언어 모델(Masked Language Modelling (MLM))**"
SC = "**스팬 손상(Span Corruption)**"
DEN = "**잡음 제거(Denoising)**"
LM = "**언어 모델(Language Model (LM))**"
HEAD = "**과제 헤드(Task Head)**"
BODY = "**몸통(Body)**"
DOWN = "**다운스트림 과제(Downstream Task)**"
ICL = "**인컨텍스트 러닝(In-Context Learning)**"
PROMPT = "**프롬프트(Prompt)**"
PROMPTING = "**프롬프팅(Prompting)**"
FS = "**퓨샷(Few-shot)**"
CBQA = "**클로즈드북 질의응답(Closed-book QA)**"
EQA = "**추출형 질의응답(Extractive QA)**"
WK = "**사실 지식(World Knowledge)**"
MEMZ = "**암기(Memorization)**"
BIAS = "**편향(Bias)**"
LR = "**학습률(Learning Rate)**"
EPOCH = "**에폭(Epoch)**"
BS = "**배치 크기(Batch Size)**"
WARM = "**워밍업(Warmup)**"
OVF = "**과적합(Overfitting)**"
PEFT = "**파라미터 효율적 미세조정(Parameter-efficient Finetuning (PEFT))**"
LORA = "**로라(LoRA)**"
ADAPT = "**어댑터(Adapter)**"
FREEZE = "**동결(Freezing)**"
SCALE = "**스케일링 법칙(Scaling Laws)**"
LABEL = "**레이블(Label)**"
PARAM = "**파라미터(Parameter)**"
TOK = "**토큰(Token)**"
LLM = "**대규모 언어 모델(Large Language Model (LLM))**"
TRF = "**트랜스포머(Transformer)**"
LOSS = "**손실 함수(Loss Function)**"
GD = "**경사 하강법(Gradient Descent)**"
GRAD = "**기울기(Gradient)**"
T2T = "**텍스트-투-텍스트(Text-to-Text)**"
CLSF = "**분류(Classification)**"
MT = "**기계 번역(Machine Translation (MT))**"
CORPUS = "**말뭉치(Corpus)**"
SENTI = "**감성 분석(Sentiment Analysis)**"
NSMC = "**NSMC(Naver Sentiment Movie Corpus)**"
HF = "**허깅페이스(Hugging Face)**"
TRAINER = "**트레이너(Trainer)**"
ACC = "**정확도(Accuracy)**"
F1 = "**F1 점수(F1 Score)**"
EA = "**오류 분석(Error Analysis)**"
DR = "**수확 체감(Diminishing Returns)**"
LC = "**학습 곡선(Learning Curve)**"
CHANCE = "**우연 수준(Chance Level)**"
PROBE = "**선형 프로빙(Linear Probing)**"

GLOSSARY = [
    ("사전 학습", "Pre-training", "아무 글이나 잔뜩 읽히면서 모델 전체를 미리 학습시켜 두는 단계",
     "레이블 없이 글자만 있으면 돼요. 한 번 비싸게 해 두고 여러 과제에서 계속 재사용해요."),
    ("미세조정", "Finetuning", "미리 학습된 모델을 우리 과제 데이터로 조금만 더 학습시키기",
     "학습률을 사전 학습보다 100배 작게 써요. 에폭도 2에서 4 정도면 충분해요."),
    ("전이 학습", "Transfer Learning", "한 곳에서 배운 것을 다른 과제로 옮겨 쓰기",
     "사전 학습과 미세조정을 묶어 부르는 큰 이름이에요."),
    ("자기 지도 학습", "Self-Supervision", "사람이 답을 달아 주지 않고 글 자체에서 답을 만들어 쓰는 학습",
     "레이블이 병목이 아니게 만들어 준 장치예요. 글은 공짜고 레이블은 비싸요."),
    ("지도 학습", "Supervised Learning", "사람이 달아 준 정답을 보고 배우는 학습",
     "미세조정 단계가 여기에 들어가요. 그래서 레이블이 필요해요."),
    ("파라미터 초기화", "Parameter Initialisation", "학습을 시작할 때 가중치를 어떤 값에서 출발시킬지 정하는 일",
     "사전 학습은 과제가 아니라 경사 하강법의 출발점을 고르는 일이에요."),
    ("버트", "BERT", "앞뒤를 다 보는 인코더 방식 사전 학습 모델",
     "고정된 분류 과제에는 지금도 가장 싸고 좋은 답이에요. Lab 4 에서 한국어 BERT 를 써요."),
    ("지피티", "GPT", "앞만 보고 다음 토큰을 만드는 디코더 방식 사전 학습 모델",
     "자유로운 글을 써야 할 때 고르는 쪽이에요."),
    ("티파이브", "T5", "인코더와 디코더를 둘 다 쓰고 모든 과제를 글로 주고받는 모델",
     "입력을 고쳐 쓴 글이 출력일 때 어울려요. 번역과 요약이 대표예요."),
    ("인코더", "Encoder", "입력 문장을 앞뒤로 다 읽어 자리마다 표현을 만드는 쪽",
     "출력이 레이블이나 태그일 때 고르는 쪽이에요."),
    ("디코더", "Decoder", "답 문장을 한 토큰씩 만들어 내는 쪽",
     "멈출 때까지 계속 쓸 수 있어서 자유로운 글에 어울려요."),
    ("인과 마스킹", "Causal Masking", "미래 자리의 어텐션 점수를 소프트맥스 전에 막아 버리기",
     "4주차 N4 p.43 에서 배웠어요. GPT 가 글을 쓸 수 있는 이유예요."),
    ("양방향 문맥", "Bidirectional Context", "한 토큰이 왼쪽과 오른쪽을 모두 볼 수 있는 상태",
     "BERT 의 성질이에요. 이 때문에 BERT 는 이어 쓰기를 못해요."),
    ("자기회귀", "Autoregressive", "자기가 만든 토큰을 다시 입력으로 넣어 다음 토큰을 만드는 방식",
     "이 방식이라야 멈출 때까지 글을 이어 쓸 수 있어요."),
    ("다음 토큰 예측", "Next Token Prediction", "지금까지의 토큰으로 바로 다음 토큰을 맞히기",
     "디코더의 사전 학습 목적 함수예요. 3주차 RNN 언어 모델과 같아요."),
    ("마스크 언어 모델", "Masked Language Modelling (MLM)", "빈칸 채우기 시험지. 가린 자리의 원래 단어를 맞히기",
     "인코더의 사전 학습 목적 함수예요."),
    ("스팬 손상", "Span Corruption", "이어진 덩어리를 통째로 지우고 디코더가 그 덩어리만 다시 쓰게 하는 게임",
     "인코더 디코더의 사전 학습 목적 함수예요. 잡음 제거 계열이에요."),
    ("잡음 제거", "Denoising", "일부러 망가뜨린 글을 원래대로 되돌리게 시키는 학습",
     "빈칸 채우기도 스팬 손상도 이 큰 이름 아래에 들어가요."),
    ("언어 모델", "Language Model (LM)", "다음 단어를 맞히는 모델. 휴대폰 자판의 다음 단어 추천 같은 것",
     "디코더는 이것이 될 수 있고 인코더는 될 수 없어요."),
    ("과제 헤드", "Task Head", "같은 몸통 위에 갈아 끼우는 공구 날 같은 작은 출력 층",
     "미세조정을 시작할 때 이 부분만 무작위에서 출발해요. 그래서 워밍업이 필요해요."),
    ("몸통", "Body", "내려받아 그대로 쓰는 사전 학습된 본체",
     "PEFT 는 이 몸통을 얼리고 작은 부품만 학습시켜요."),
    ("다운스트림 과제", "Downstream Task", "사전 학습이 끝난 모델을 가져다 푸는 우리 진짜 과제",
     "감성 분석, 개체명 인식, 질의응답 같은 것이 여기에 들어가요."),
    ("인컨텍스트 러닝", "In-Context Learning", "시험지 맨 위에 예시 두세 개를 적어 주면 그대로 따라 푸는 것",
     "가중치는 전혀 바뀌지 않아요. 기울기 걸음이 하나도 없어요."),
    ("프롬프트", "Prompt", "모델에게 넣어 주는 입력 글 전체",
     "프롬프팅에서는 이것 하나가 우리가 가진 전부예요."),
    ("클로즈드북 질의응답", "Closed-book QA", "본문을 하나도 주지 않고 질문만 던지는 질의응답",
     "모델이 사전 학습 때 흡수한 것만으로 답해요. 가끔 맞고 가끔 틀려요."),
    ("추출형 질의응답", "Extractive QA", "주어진 본문 안에서 답이 되는 구간을 찾아 가리키는 질의응답",
     "본문을 함께 주니까 오픈북 시험에 가까워요."),
    ("사실 지식", "World Knowledge", "세상에 대한 사실. 어느 도시가 어느 주에 있는지 같은 것",
     "사전 학습이 가르치기는 하는데 군데군데 비어 있어요."),
    ("암기", "Memorization", "일반화가 아니라 학습 문서를 글자 그대로 외워 두는 것",
     "전화번호 같은 것을 그대로 뱉을 수 있어서 개인정보 문제가 돼요."),
    ("편향", "Bias", "인터넷 글에 들어 있던 사람에 대한 치우친 생각까지 배워 버리는 것",
     "슬라이드는 이것을 원하지 않는 것(unwanted)으로 분류했어요."),
    ("학습률", "Learning Rate", "경사 하강법에서 한 걸음의 보폭",
     "미세조정에서는 2e-5 에서 5e-5 를 써요. 사전 학습보다 100배 작아요."),
    ("에폭", "Epoch", "학습 데이터 전체를 한 번 다 도는 것",
     "미세조정은 2에서 4 에폭이면 충분해요. 더 돌면 과적합이 나요."),
    ("배치 크기", "Batch Size", "한 번에 묶어서 처리하는 데이터 개수",
     "미세조정에서는 16 또는 32 를 쓰고, 메모리에 들어가는 만큼 정해요."),
    ("워밍업", "Warmup", "처음 몇 걸음 동안 학습률을 0 에서 목표까지 천천히 올리기",
     "전체 걸음의 처음 약 10 퍼센트를 써요. 헤드가 무작위에서 출발하기 때문이에요."),
    ("과적합", "Overfitting", "학습 데이터만 잘 맞히고 새 데이터에는 못 맞히게 되는 것",
     "에폭을 너무 많이 돌면 생겨요."),
    ("파라미터 효율적 미세조정", "Parameter-efficient Finetuning (PEFT)",
     "사전 학습된 몸통을 얼려 두고 작은 부품만 학습시키는 방법",
     "전체 가중치의 약 1 퍼센트만 움직여요. GPU 한 장으로 아주 큰 모델도 다룰 수 있어요."),
    ("로라", "LoRA", "PEFT 의 대표 방법. 작은 덧붙임 행렬만 학습시켜요",
     "몸통은 그대로 두고 작은 패치만 저장하면 돼요."),
    ("어댑터", "Adapter", "얼린 몸통 사이사이에 끼워 넣는 작고 학습 가능한 부품",
     "과제마다 이 부품 하나씩만 따로 저장해요."),
    ("동결", "Freezing", "가중치를 학습에서 빼고 그대로 두기",
     "PEFT 는 몸통을 동결하고 작은 부품만 움직여요."),
    ("스케일링 법칙", "Scaling Laws", "계산을 늘리면 손실이 얼마나 줄어드는지 예측 가능한 관계",
     "로그-로그 그림에서 직선으로 보여요. 작은 모델로 큰 모델을 예측할 수 있어요."),
    ("레이블", "Label", "사람이 달아 준 정답 표",
     "레이블은 비싸고 글은 공짜예요. 그래서 이 패러다임이 이겼어요."),
    ("파라미터", "Parameter", "학습하면서 바뀌는 숫자. 모델이 아는 것을 저장하는 자리",
     "BERT-base 는 1억 1000만 개, GPT-3 은 1750억 개예요."),
    ("토큰", "Token", "글을 자른 레고 조각 하나",
     "스케일링에서는 파라미터 수와 함께 토큰 수가 같이 중요해요."),
    ("대규모 언어 모델", "Large Language Model (LLM)", "트랜스포머를 아주 크게 쌓은 언어 모델",
     "GPT-3 이 1750억 파라미터, 3000억 토큰으로 학습됐어요."),
    ("트랜스포머", "Transformer", "어텐션만으로 만든 요즘 언어 모델의 기본 블록",
     "5주차의 세 구조가 전부 같은 이 블록을 써요."),
    ("손실 함수", "Loss Function", "틀린 정도를 매기는 벌점",
     "스케일링 법칙 그림의 세로축이 바로 이 값이에요."),
    ("경사 하강법", "Gradient Descent", "안개 낀 산에서 발밑 기울기만 보고 한 걸음씩 내려가기",
     "미세조정은 좋은 출발점 근처에서 아주 작은 보폭으로 걷는 일이에요."),
    ("기울기", "Gradient", "손실이 가장 빨리 커지는 방향과 그 가파름",
     "인컨텍스트 러닝은 이 걸음을 한 번도 밟지 않아요."),
    ("텍스트-투-텍스트", "Text-to-Text", "모든 과제의 입력도 글, 출력도 글로 맞추는 방식",
     "T5 가 쓰는 방식이에요."),
    ("분류", "Classification", "입력에 이름표 하나를 붙이는 과제",
     "고정된 분류 과제라면 작은 인코더가 지금도 가장 싸고 좋아요."),
    ("기계 번역", "Machine Translation (MT)", "한 언어의 글을 다른 언어의 글로 바꾸기",
     "입력도 글, 출력도 글이라 인코더 디코더가 어울려요."),
    ("말뭉치", "Corpus", "학습에 쓰는 글 더미",
     "Lab 4 에서 쓰는 NSMC 도 말뭉치예요."),
    ("감성 분석", "Sentiment Analysis", "글이 긍정인지 부정인지 맞히기",
     "Lab 4 에서 한국어 영화 리뷰로 해 봐요."),
    ("NSMC", "NSMC (Naver Sentiment Movie Corpus)", "한국어 영화 리뷰에 긍정 부정 표가 달린 데이터",
     "Lab 4 가 이것으로 한국어 BERT 를 미세조정해요."),
    ("허깅페이스", "Hugging Face", "사전 학습 모델과 데이터를 내려받아 쓰는 라이브러리이자 저장소",
     "Lab 4 는 이곳의 Trainer 를 써요."),
    ("트레이너", "Trainer", "학습 반복문을 대신 돌려 주는 허깅페이스의 도구",
     "학습률, 에폭, 배치 크기를 넣어 주면 나머지를 알아서 해요."),
    ("정확도", "Accuracy", "전체 중에 맞힌 비율",
     "Lab 4 의 전체 미세조정 정확도는 87.4 퍼센트였어요."),
    ("오류 분석", "Error Analysis", "틀린 예를 직접 들여다보며 무엇이 문제인지 찾기",
     "Lab 4 의 마지막 단계예요."),
    ("수확 체감", "Diminishing Returns", "더 넣을수록 얻는 이득이 점점 줄어드는 현상",
     "레이블을 늘릴수록 정확도 상승폭이 작아져요."),
    ("학습 곡선", "Learning Curve", "데이터 양에 따라 성능이 어떻게 변하는지 그린 그림",
     "N5 p.45 의 두 곡선이 바로 이것이에요."),
    ("우연 수준", "Chance Level", "아무렇게나 찍었을 때 나오는 성능",
     "긍정 부정 두 가지면 약 50 퍼센트예요."),
    ("선형 프로빙", "Linear Probing", "몸통을 얼린 채 그 위에 아주 단순한 분류기만 얹어 보는 방법",
     "사전 학습된 표현이 얼마나 쓸모 있는지 재는 방법이에요."),
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


def PL(pts, cls="e2", b=0):
    return f'<polyline points="{pts}" fill="none" class="{_c(cls, b)}"/>'


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
FIG_QA = SVG(
    TX(240, 20, "책을 펴고 보는 시험과 덮고 보는 시험", "tb", 15),
    BOX(12, 40, 190, 34, "질문 + 본문", "box", "tb", 1, 13),
    TX(107, 90, "오픈북 질의응답", "tm", 12, "middle", 1),
    A(208, 57, 250, 57, "e2", 1),
    BOX(256, 40, 78, 34, "T5", "box", "tb", 1, 15),
    A(340, 57, 382, 57, "e2", 1),
    TX(432, 52, "본문에서", "t", 12, "middle", 1),
    TX(432, 70, "답을 찾아 읽어요", "t", 12, "middle", 1),
    BOX(12, 130, 190, 34, "질문만, 본문 없음", "box2", "tb", 2, 13),
    TX(107, 180, "클로즈드북 질의응답", "tm", 12, "middle", 2),
    A(208, 147, 250, 147, "e2", 2),
    BOX(256, 130, 78, 34, "T5", "box2", "tb", 2, 15),
    A(340, 147, 382, 147, "e2", 3),
    TX(432, 142, "외운 것에서", "tb", 12, "middle", 3),
    TX(432, 160, "답을 꺼내요", "tb", 12, "middle", 3),
    TX(240, 220, "사전 학습은 언어만 가르친 게 아니었어요", "tb", 13, "middle", 4),
    TX(240, 244, "사실도 잔뜩 저장했어요. 다만 믿을 만하지는 않아요", "tm", 12, "middle", 4),
)

FIG_PICK = SVG(
    TX(240, 20, "출력 모양을 보고 고르기", "tb", 15),
    BOX(10, 40, 140, 34, "레이블이나 태그", "n", "tl", 1, 12),
    A(154, 57, 196, 57, "e2", 1),
    BOX(202, 40, 110, 34, "인코더", "box", "tb", 1, 14),
    TX(400, 62, "BERT, KLUE-BERT", "tm", 12, "middle", 1),
    BOX(10, 96, 140, 34, "입력을 고쳐 쓴 글", "n", "tl", 2, 12),
    A(154, 113, 196, 113, "e2", 2),
    BOX(202, 96, 110, 34, "인코더 디코더", "box", "tb", 2, 13),
    TX(400, 118, "T5, BART, mT5", "tm", 12, "middle", 2),
    BOX(10, 152, 140, 34, "자유로운 글", "n", "tl", 3, 12),
    A(154, 169, 196, 169, "e2", 3),
    BOX(202, 152, 110, 34, "디코더", "box2", "tb", 3, 14),
    TX(400, 174, "GPT, LLaMA, Qwen", "tm", 12, "middle", 3),
    TX(240, 218, "2026년에는 디코더가 흔해요", "tb", 13, "middle", 4),
    TX(240, 242, "그래도 고정된 분류라면 1억짜리 인코더가 더 싸고 좋아요", "t", 12, "middle", 4),
)

FIG_TAUGHT = SVG(
    TX(240, 20, "빈칸들이 가르친 것", "tb", 15),
    *[R(14, 36 + i * 26, 8, 16, "n2", 1) for i in range(4)],
    *[TX(30, 49 + i * 26, t, "tb", 12, "start", 1)
      for i, t in enumerate(["문법(syntax)", "가리킴(coreference)", "낱말 뜻(lexical semantics)", "감정(sentiment)"])],
    *[R(14, 144 + i * 26, 8, 16, "n3", 2) for i in range(2)],
    *[TX(30, 157 + i * 26, t, "tb", 12, "start", 2)
      for i, t in enumerate(["사실 지식(world knowledge)", "조금의 계산(arithmetic)"])],
    R(14, 196, 8, 16, "n4", 3),
    TX(30, 209, "편향(bias)", "tb", 12, "start", 3),
    TX(300, 49, "믿을 만해요", "t", 12, "start", 1),
    TX(300, 157, "군데군데 비어요", "t", 12, "start", 2),
    TX(300, 209, "원하지 않는 것", "t", 12, "start", 3),
    TX(240, 244, "네 개는 믿을 만, 두 개는 군데군데, 하나는 원치 않는 것", "tb", 13, "middle", 4),
)

FIG_MEM = SVG(
    TX(240, 22, "일반화만 하는 게 아니라 외우기도 해요", "tb", 15),
    BOX(16, 50, 190, 40, "내 전화번호는 ...", "n", "tl", 1, 13),
    TX(111, 106, "학습 데이터에 있던 글", "tm", 11, "middle", 1),
    A(214, 70, 262, 70, "e2", 2),
    BOX(268, 50, 196, 40, "... 실제 그 번호", "box2", "tb", 2, 13),
    TX(366, 106, "학습 문서에서 글자 그대로", "tm", 11, "middle", 2),
    R(24, 136, 432, 62, "box", 3),
    TX(240, 160, "멤버십 추론: 어떤 문서가 학습에 쓰였는지 알아낼 수 있어요", "t", 12, "middle", 3),
    TX(240, 184, "학습에만 썼다는 말이 개인정보 보장이 되지 않아요", "tb", 12, "middle", 4),
    TX(240, 226, "암기는 일반화가 아니에요. 그대로 복사해 둔 거예요", "tb", 13, "middle", 4),
)

FIG_RECIPE = SVG(
    TX(240, 20, "미세조정 레시피 네 숫자", "tb", 15),
    R(14, 36, 8, 18, "n2", 1),
    TX(30, 50, "학습률", "tb", 13, "start", 1),
    TX(180, 50, "2e-5 에서 5e-5", "tb", 13, "start", 1),
    TX(330, 50, "사전 학습보다 100배 작게", "tm", 11, "start", 1),
    R(14, 72, 8, 18, "n3", 2),
    TX(30, 86, "에폭", "tb", 13, "start", 2),
    TX(180, 86, "2 에서 4", "tb", 13, "start", 2),
    TX(330, 86, "더 돌면 과적합", "tm", 11, "start", 2),
    R(14, 108, 8, 18, "n3", 3),
    TX(30, 122, "배치 크기", "tb", 13, "start", 3),
    TX(180, 122, "16 또는 32", "tb", 13, "start", 3),
    TX(330, 122, "메모리에 들어가는 만큼", "tm", 11, "start", 3),
    R(14, 144, 8, 18, "n2", 4),
    TX(30, 158, "워밍업", "tb", 13, "start", 4),
    TX(180, 158, "처음 약 10 퍼센트", "tb", 13, "start", 4),
    TX(330, 158, "헤드가 잡음에서 출발", "tm", 11, "start", 4),
    R(24, 184, 432, 44, "box2", 4),
    TX(240, 202, "가장 흔한 실수는 사전 학습 학습률을 그대로 쓰는 것", "tb", 13, "middle", 4),
    TX(240, 220, "모델이 알던 것을 전부 지워 버려요", "t", 12, "middle", 4),
)

FIG_CURVE = SVG(
    TX(240, 20, "레이블이 적을 때 차이가 가장 커요", "tb", 15),
    L(52, 200, 440, 200, "e", 1),
    L(52, 40, 52, 200, "e", 1),
    TX(40, 48, "높음", "tm", 11, "end", 1),
    TX(40, 198, "낮음", "tm", 11, "end", 1),
    TX(246, 222, "레이블 개수 (왼쪽이 적음)", "tm", 11, "middle", 1),
    PL("62,150 130,140 200,106 270,72 340,58 420,56", "e2", 2),
    TX(300, 46, "사전 학습 + 미세조정", "tb", 12, "middle", 2),
    PL("62,194 130,192 200,186 270,172 340,128 420,74", "e", 3),
    TX(150, 178, "처음부터 학습", "tm", 12, "middle", 3),
    L(150, 150, 150, 192, "e2", 4),
    TX(158, 172, "여기 차이가 가장 커요", "tb", 12, "start", 4),
    TX(240, 252, "진짜 프로젝트는 대개 수백에서 수천 개 자리에 있어요", "t", 12, "middle", 4),
)

FIG_PEFT = SVG(
    TX(240, 20, "모든 가중치를 움직일 필요는 없어요", "tb", 15),
    TX(120, 44, "전체 미세조정", "tb", 13, "middle", 1),
    *[R(30 + c * 20, 56 + r * 20, 16, 14, "n2", 1) for r in range(4) for c in range(9)],
    TX(120, 156, "1억 1000만 개가 전부 움직여요", "tm", 11, "middle", 1),
    A(224, 100, 252, 100, "e2", 2),
    TX(360, 44, "LoRA 와 어댑터", "tb", 13, "middle", 2),
    *[R(268 + c * 20, 56 + r * 20, 16, 14, "n", 2) for r in range(4) for c in range(8)],
    *[R(428, 56 + r * 20, 16, 14, "n3", 3) for r in range(4)],
    TX(360, 156, "약 1 퍼센트만 움직여요", "tm", 11, "middle", 3),
    TX(240, 196, "같은 몸통을 얼려 두고 작은 패치 하나만 학습해요", "tb", 13, "middle", 4),
    TX(240, 222, "GPU 한 장으로 여러 과제를 각각 저장할 수 있어요", "t", 12, "middle", 4),
    TX(240, 248, "110M 의 1 퍼센트면 약 110만 개예요", "tm", 12, "middle", 4),
)

FIG_SCALING = SVG(
    TX(240, 20, "로그-로그 그림에서 직선", "tb", 15),
    L(56, 190, 440, 190, "e", 1),
    L(56, 44, 56, 190, "e", 1),
    TX(44, 52, "높음", "tm", 11, "end", 1),
    TX(44, 188, "낮음", "tm", 11, "end", 1),
    TX(30, 124, "손실", "tb", 12, "middle", 1),
    TX(248, 212, "학습 계산량 (로그 눈금)", "tm", 11, "middle", 1),
    L(70, 56, 424, 172, "e2", 2),
    TX(300, 92, "직선이에요", "tb", 13, "middle", 2),
    TX(240, 236, "작은 모델 몇 개로 큰 모델의 손실을 미리 알 수 있어요", "tb", 13, "middle", 3),
    TX(240, 260, "GPT-3 은 1750억 파라미터, 3000억 토큰이었어요", "tm", 12, "middle", 4),
)

FIG_WON = SVG(
    TX(240, 20, "이 방식이 이긴 네 가지 이유", "tb", 15),
    R(10, 38, 110, 92, "box", 1),
    TX(65, 60, "비싼 한 걸음", "tb", 12, "middle", 1),
    TX(65, 82, "한 번만", "t", 11, "middle", 1),
    TX(65, 108, "쓰기는 여러 번", "tm", 11, "middle", 1),
    R(130, 38, 110, 92, "box", 2),
    TX(185, 60, "레이블이", "tb", 12, "middle", 2),
    TX(185, 82, "병목이 아니게", "t", 11, "middle", 2),
    TX(185, 108, "글은 공짜예요", "tm", 11, "middle", 2),
    R(250, 38, 110, 92, "box", 3),
    TX(305, 60, "한 구조로", "tb", 12, "middle", 3),
    TX(305, 82, "모든 과제", "t", 11, "middle", 3),
    TX(305, 108, "헤드만 바꿔요", "tm", 11, "middle", 3),
    R(370, 38, 100, 92, "box", 4),
    TX(420, 60, "키우면", "tb", 12, "middle", 4),
    TX(420, 82, "계속 좋아져요", "t", 11, "middle", 4),
    TX(420, 108, "같은 레시피로", "tm", 11, "middle", 4),
    TX(240, 172, "영리한 알고리즘이 있어서 이긴 게 아니에요", "tb", 13, "middle", 4),
    TX(240, 198, "비용과 재사용이 맞아떨어져서 이겼어요", "t", 13, "middle", 4),
    TX(240, 228, "이 과목에서 앞으로 쓸 모델은 전부 사전 학습된 것이에요", "tm", 12, "middle", 4),
)

FIG_WRAP = SVG(
    TX(240, 20, "5주차를 한 줄로", "tb", 15),
    BOX(10, 40, 460, 30, "왜 사전 학습하나: 레이블은 비싸고 글은 공짜", "box", "tb", 1, 13),
    A(240, 72, 240, 90, "e2", 2),
    BOX(10, 94, 460, 30, "패러다임: 사전 학습은 파라미터 초기화", "box", "tb", 2, 13),
    A(240, 126, 240, 144, "e2", 3),
    BOX(10, 148, 148, 34, "인코더 + 빈칸", "box2", "tb", 3, 12),
    BOX(166, 148, 148, 34, "인코더 디코더 + 스팬", "box2", "tb", 3, 11),
    BOX(322, 148, 148, 34, "디코더 + 다음 토큰", "box2", "tb", 3, 12),
    A(240, 184, 240, 202, "e2", 4),
    BOX(10, 206, 460, 30, "무엇이 학습되나: 문법과 뜻은 잘, 사실은 군데군데, 편향도 함께", "box", "tb", 4, 12),
    TX(240, 258, "Lab 4 에서 한국어 BERT 를 직접 미세조정해요", "tm", 12, "middle", 4),
)

S = []


def page(p, title, terms, p1, p2=(), p3=(), p4=()):
    S.append({"p": p, "title": title, "terms": list(terms),
              "pass1": list(p1), "pass2": list(p2), "pass3": list(p3), "pass4": list(p4)})


# ---------------------------------------------------------------- p.39
page(39, "지식 베이스가 된 모델",
     ["Closed-book QA", "Extractive QA", "T5", "World Knowledge", "Pre-training",
      "Memorization", "Decoder", "Encoder", "Token"],
     [say(f"{PRE}의 이상한 부작용 하나를 보는 쪽이에요.",
          f"본문을 하나도 주지 않고 질문만 던져도 모델이 답을 해요. 이것이 {CBQA} 예요.",
          f"{PRE} 때 흡수한 {WK}에서 꺼내 쓰는 거예요. 다만 가끔만 맞아요."),
      analogy("책을 펴고 보는 시험과 덮고 보는 시험",
              "본문을 함께 주면 오픈북 시험이에요. 본문을 치우고 질문만 주면 덮고 보는 시험이 돼요. 외운 것만으로 답해야 해요.",
              ("본문을 함께 주는 시험", EQA),
              ("본문 없이 질문만", CBQA),
              ("머릿속에 외워 둔 사실", WK))],
     [points("슬라이드 영어와 우리말 뜻",
             "The Model as a Knowledge Base = 지식 베이스가 된 모델",
             "Closed-book QA: ask a question with no passage attached = 본문 없이 질문만 던지는 질의응답",
             "The model answers from what it absorbed during pretraining = 사전 학습 때 흡수한 것에서 답한다",
             "sometimes correctly = 가끔은 맞게",
             "question + the passage that contains the answer = 질문 + 답이 들어 있는 본문",
             "pretraining did not only teach language = 사전 학습은 언어만 가르친 것이 아니다"),
      compare("두 가지 질의응답",
              ["보는 점", "오픈북", f"클로즈드북({CBQA})"],
              ["입력", "질문 + 본문", "질문만"],
              ["답을 어디서 찾나", "본문 안에서", "모델이 외운 것에서"],
              ["N5 p.23 의 모양", "스팬 추출", "글로 답 쓰기"],
              ["믿을 만한가", "본문이 근거가 됨", "근거가 없어 불안정"])],
     [look("슬라이드를 짚어 읽어요",
           (0.060, 0.198, 0.870, 0.055, "부제: 본문 없이 질문만 던져요. 사전 학습 때 흡수한 것으로 답해요."),
           (0.118, 0.419, 0.302, 0.077, "위 회색 상자 open-book QA. 아래 작은 글이 질문 + 답이 든 본문이에요."),
           (0.118, 0.623, 0.302, 0.072, "아래 보라 상자 closed-book QA. 작은 글이 질문만, 본문은 전혀 없음이에요."),
           (0.504, 0.419, 0.146, 0.276, "가운데는 둘 다 같은 T5 예요. 모델이 달라진 게 아니에요."),
           (0.754, 0.419, 0.180, 0.100, "위 오른쪽: 본문에서 답을 읽어 내요."),
           (0.750, 0.620, 0.190, 0.080, "아래 오른쪽: 기억하는 것에서 답해요.")),
      figure("펴고 보는 시험과 덮고 보는 시험", FIG_QA,
             "모델은 같고 입력만 달라요. 본문이 없으면 외운 것에 기대야 해요.", 4),
      points("왜 이것이 이상한 일인지",
             f"원래 {PRE}은 빈칸을 채우거나 다음 {TOK}을 맞히는 게임이었어요",
             "사실을 외우라고 시킨 적이 한 번도 없어요",
             "그런데 글 안에 사실이 많이 들어 있어서 저절로 저장됐어요",
             f"슬라이드 기울임 글: 언어만 가르친 게 아니라 사실도 잔뜩 저장했고 그것이 믿을 만하지 않다고 적혀 있어요",
             f"이 이야기는 N5 p.42 의 {WK} 과 N5 p.43 의 {MEMZ} 으로 이어져요"),
      bg("이 과목 안에서 이어 보기",
         f"N5 p.23 의 네 가지 과제 모양 중 {EQA} 는 본문을 함께 줘요.",
         f"{CBQA} 는 본문이 없으니 그 모양으로는 풀 수 없어요.",
         f"그래서 {T5} 처럼 글을 써 낼 수 있는 모델이 필요해요.")],
     [check(f"{CBQA} 의 입력은",
            ["질문만", "질문 + 본문", "본문만", "레이블 붙은 데이터"], 0,
            "슬라이드 그대로 question only, no passage at all 이에요."),
      check("슬라이드가 클로즈드북 답에 대해 붙인 단서는",
            ["가끔만 맞아요", "언제나 맞아요", "언제나 틀려요", "본문보다 정확해요"], 0,
            "sometimes correctly 와 unreliably 라고 두 번 적어 뒀어요."),
      english("시험 답안 문장",
              f"{CBQA} 는 본문 없이 질문만 주고 모델이 {PRE} 때 흡수한 {WK}으로 답하게 하는 방식이다.",
              "사실을 외우라고 시킨 적이 없는데도 저절로 저장됐다는 점이 핵심이에요.",
              "덮고 보는 시험. 이 한 마디로 외워요."),
      warn("헷갈리기 쉬운 점",
           f"모델이 지식 베이스라는 말은 비유예요. 근거를 함께 내주지 않아서 검증이 안 돼요.",
           f"{CBQA} 가 잘된다고 {PRE}이 사실을 정확히 배웠다는 뜻은 아니에요.",
           "슬라이드 오른쪽 아래 번호는 37 / 48 이지만 우리 번호로는 N5 p.39 예요.")])

# ---------------------------------------------------------------- p.40
page(40, "무엇을 고를까",
     ["Encoder", "Decoder", "T5", "BERT", "GPT", "Classification", "Machine Translation (MT)",
      "Parameter", "Finetuning", "Downstream Task", "Text-to-Text", "Label"],
     [say("세 구조 중 무엇을 고를지 정하는 쪽이에요.",
          "기준은 딱 하나예요. 내 출력이 어떤 모양인지 보는 거예요.",
          "유행을 보지 말라고 슬라이드가 못 박아 두었어요."),
      analogy("출력 모양에 맞는 연장 고르기",
              "이름표를 붙일 일이면 스탬프, 글을 고쳐 쓸 일이면 편집용 연필, 백지에 계속 써 나갈 일이면 만년필을 골라요.",
              ("이름표 스탬프", ENC),
              ("고쳐 쓰는 연필", "인코더 디코더"),
              ("계속 쓰는 만년필", DEC))],
     [points("슬라이드 영어와 우리말 뜻",
             "Which One Should You Reach For? = 무엇에 손을 뻗어야 하나",
             "Look at the shape of your output, not at what is fashionable = 유행이 아니라 출력 모양을 보라",
             "a label or a tag = 레이블이나 태그 하나",
             "a rewritten version of the input = 입력을 고쳐 쓴 글",
             "free-form text = 자유로운 글",
             "you keep writing until you stop = 멈출 때까지 계속 쓴다"),
      compare("슬라이드 표 그대로",
              ["내 출력이", "무엇을 쓰나", "예시 모델", "왜"],
              [f"{LABEL} 이나 태그", ENC, "BERT, KLUE-BERT", "입력 전체가 한 번에 필요해요"],
              ["입력을 고쳐 쓴 글", "인코더 디코더", "T5, BART, mT5", "입력과 출력이 서로 다른 글이에요"],
              ["자유로운 글", DEC, "GPT, LLaMA, Qwen", "멈출 때까지 계속 써요"])],
     [look("슬라이드를 짚어 읽어요",
           (0.060, 0.198, 0.420, 0.040, "부제: 유행이 아니라 출력 모양을 보세요."),
           (0.109, 0.394, 0.792, 0.048, "표 머리 네 칸: 내 출력, 무엇을 쓰나, 예시 모델, 왜."),
           (0.109, 0.468, 0.792, 0.042, "첫 줄: 레이블이나 태그면 인코더. 입력 전체가 한 번에 필요해요."),
           (0.109, 0.532, 0.792, 0.076, "둘째 줄: 입력을 고쳐 쓴 글이면 인코더 디코더."),
           (0.109, 0.632, 0.792, 0.042, "셋째 줄: 자유로운 글이면 디코더."),
           (0.090, 0.720, 0.830, 0.036, "아래 굵은 글: 2026년엔 디코더가 흔하지만 고정 분류는 1억짜리 인코더가 더 싸고 좋아요.")),
      figure("출력 모양을 보고 고르기", FIG_PICK,
             "세 줄 중 어디에 내 과제가 들어가는지만 보면 돼요.", 4),
      steps("우리 과제로 골라 봐요",
            [f"한국어 영화 리뷰가 긍정인지 부정인지 맞히는 과제예요",
             f"출력은 {LABEL} 하나예요. 글이 아니에요",
             "표 첫 줄에 해당해요",
             f"그러면 {ENC}를 고르고, 예시 모델은 BERT 나 KLUE-BERT 예요",
             f"슬라이드 아래 줄도 같은 말을 해요. 고정된 {CLSF} 는 1억짜리 인코더가 더 싸고 좋아요"],
            f"한국어 {BERT} 를 {FT}하면 돼요. 이것이 바로 Lab 4 가 하는 일이에요.",
            "출력이 긍정 또는 부정"),
      points("표에 나온 모델 이름들",
             "BERT 와 KLUE-BERT 는 인코더예요. KLUE-BERT 는 한국어용이에요",
             f"T5, BART, mT5 는 인코더 디코더예요. mT5 는 여러 언어용 {T5} 예요",
             "GPT, LLaMA, Qwen 은 디코더예요",
             "이 이름들은 이 과목에서 자세히 배우지는 않아요. 어느 칸에 들어가는지만 알면 돼요",
             f"{MT} 과 요약은 둘째 줄, 채팅처럼 자유로운 답은 셋째 줄이에요",
             f"{DEC}가 셋째 줄인 이유는 {CM} 때문에 {AR}로 계속 쓸 수 있어서예요")],
     [check("출력이 레이블 하나일 때 슬라이드가 권하는 구조는",
            [ENC, DEC, "인코더 디코더", "셋 다 안 됨"], 0,
            "표 첫 줄이에요. 입력 전체가 한 번에 필요하기 때문이에요."),
      check("슬라이드가 말한 2026년의 상황은",
            ["디코더가 흔하지만 고정 분류는 작은 인코더가 더 낫다",
             "인코더가 사라졌다", "디코더는 분류를 못 한다", "셋 다 똑같다"], 0,
            "in 2026 decoders dominate, but for a fixed classification task a 110M encoder is still the cheaper, better answer 예요."),
      english("시험 답안 문장",
              f"출력이 {LABEL} 이면 {ENC}, 입력을 고쳐 쓴 글이면 인코더 디코더, 자유로운 글이면 {DEC}를 고른다.",
              "기준은 유행이 아니라 출력 모양이에요. 세 줄을 그대로 외우면 돼요.",
              "레이블은 인코더, 고쳐 쓰기는 둘 다, 자유 글은 디코더."),
      warn("헷갈리기 쉬운 점",
           f"{DEC}가 흔하다고 해서 언제나 더 좋은 것은 아니에요. 슬라이드가 직접 아니라고 말해요.",
           f"{T2T} 방식이면 분류도 글로 낼 수 있지만, 그것이 더 싸다는 뜻은 아니에요.",
           f"{DOWN}의 출력 모양이 기준이에요. 입력 모양이 아니에요.")])

# ---------------------------------------------------------------- p.41
page(41, "4부 표지: 사전 학습된 것을 쓰기",
     ["Pre-training", "Finetuning", "Parameter", "Parameter-efficient Finetuning (PEFT)"],
     [say("네 번째 부분 표지예요. 제목은 4 Using What Was Pretrained 예요.",
          "작은 글씨는 what the weights know, and how to move them 이에요.",
          f"가중치가 무엇을 알고 있는지, 그리고 그것을 어떻게 움직이는지를 본다는 뜻이에요.",
          f"{FT} 실전 레시피와 {PEFT} 가 여기에 나와요.")],
     [], [], [])

# ---------------------------------------------------------------- p.42
page(42, "사전 학습은 실제로 무엇을 가르쳤나",
     ["Pre-training", "World Knowledge", "Bias", "Self-Supervision", "Token",
      "Masked Language Modelling (MLM)", "Corpus", "Memorization", "Label"],
     [say(f"{PRE}이 실제로 무엇을 가르쳤는지 되짚는 쪽이에요.",
          "강의 앞부분에서 봤던 빈칸들을 다시 가져와요.",
          "빈칸 하나하나가 모델이 배워야 했던 것을 이름 붙여 줘요. 그리고 다 똑같이 잘 배운 건 아니에요."),
      analogy("아무 책이나 잔뜩 읽어 둔 신입",
              "신입이 책을 잔뜩 읽었어요. 문법과 말버릇은 확실히 익혔는데, 세상 사실은 아는 것도 있고 모르는 것도 있고, 책에 있던 편견까지 같이 배웠어요.",
              ("확실히 익힌 문법과 말버릇", "믿을 만한 것"),
              ("아는 것도 모르는 것도 있는 사실", WK),
              ("같이 배워 버린 편견", BIAS))],
     [points("슬라이드 영어와 우리말 뜻",
             "What Did Pretraining Actually Teach? = 사전 학습이 실제로 무엇을 가르쳤나",
             "Go back to the blanks from the start of the lecture = 강의 앞부분의 빈칸들로 돌아가라",
             "Each one names something the model had to learn = 빈칸마다 모델이 배워야 했던 것에 이름이 붙는다",
             "they are not all learned equally well = 다 똑같이 잘 배운 것은 아니다",
             "how much to trust it: reliable, patchy, unwanted = 얼마나 믿을까: 믿을 만함, 군데군데, 원치 않음"),
      compare("일곱 가지와 그 예",
              ["무엇을 배웠나", "슬라이드의 빈칸 예", "얼마나 믿을까"],
              ["문법(syntax)", "I put ___ fork down → a, the", "믿을 만함"],
              ["가리킴(coreference)", "checking traffic over ___ shoulder → her", "믿을 만함"],
              ["낱말 뜻(lexical semantics)", "fish, turtles, seals and ___ → whales", "믿을 만함"],
              ["감정(sentiment)", "the movie was ___ → terrible", "믿을 만함"],
              [WK, "Stanford is in ___, California → Palo Alto", "군데군데"],
              ["조금의 계산", "1, 1, 2, 3, 5, 8, 13, ___ → 자주 틀림", "군데군데"],
              [BIAS, "사람에 대해 인터넷이 믿는 것 그대로", "원치 않음"])],
     [look("슬라이드를 짚어 읽어요",
           (0.060, 0.198, 0.870, 0.055, "부제: 강의 앞부분의 빈칸들로 돌아가요. 다 똑같이 잘 배운 건 아니에요."),
           (0.110, 0.390, 0.150, 0.210, "왼쪽 위 초록 네 줄: 문법, 가리킴, 낱말 뜻, 감정."),
           (0.110, 0.600, 0.160, 0.110, "왼쪽 아래 주황과 빨강: 사실 지식, 조금의 계산, 편향."),
           (0.350, 0.390, 0.260, 0.210, "가운데에 빈칸 예가 있어요. 밑줄 자리에 들어갈 답까지 적혀 있어요."),
           (0.350, 0.650, 0.300, 0.040, "1, 1, 2, 3, 5, 8, 13 다음을 물으면 자주 틀려요."),
           (0.330, 0.765, 0.400, 0.040, "맨 아래 범례: 초록은 믿을 만함, 주황은 군데군데, 빨강은 원치 않음.")),
      figure("빈칸들이 가르친 것", FIG_TAUGHT,
             "일곱 가지를 세 등급으로 나눠 놓았어요.", 4),
      steps("등급별로 몇 개인지 세어 봐요",
            ["믿을 만한 것은 문법, 가리킴, 낱말 뜻, 감정 네 개예요",
             "군데군데인 것은 사실 지식과 조금의 계산 두 개예요",
             "원하지 않는 것은 편향 하나예요",
             "4 + 2 + 1 = 7 개예요",
             "곧 일곱 개 중 셋은 그대로 믿으면 안 돼요"],
            "믿을 만한 것 4, 군데군데 2, 원치 않는 것 1 이에요.",
            "일곱 항목, 세 등급"),
      points("각 빈칸이 요구하는 것",
             "I put ___ fork down 은 a 나 the 를 넣는 문제라 문법을 알아야 해요",
             "checking traffic over ___ shoulder 는 앞에 나온 사람을 가리켜야 해요",
             "fish, turtles, seals and ___ 은 같은 무리의 낱말을 알아야 해요",
             "the movie was ___ 는 글의 감정을 읽어야 해요",
             f"Stanford is in ___, California 는 {WK}이 있어야 해요",
             f"이 빈칸들은 사람이 {LABEL} 을 달아 준 것이 아니에요. 전부 {SS}이에요")],
     [check("슬라이드가 군데군데(patchy)로 분류한 것은",
            [f"{WK} 과 조금의 계산", "문법과 감정", "낱말 뜻과 가리킴", "편향"], 0,
            "주황색 두 줄이 world knowledge 와 a little arithmetic 이에요."),
      check("슬라이드가 원하지 않는 것(unwanted)으로 분류한 것은",
            [BIAS, "문법", "감정", "낱말 뜻"], 0,
            "빨간 줄 하나가 bias 예요. 인터넷이 사람에 대해 믿는 것을 그대로 배워요."),
      english("시험 답안 문장",
              f"{PRE}은 문법과 낱말 뜻과 감정을 믿을 만하게 가르치지만 {WK}과 계산은 군데군데이고 {BIAS}까지 함께 배운다.",
              "세 등급으로 나눠 쓰는 것이 답안 형태예요.",
              "잘 배운 것 넷, 어설픈 것 둘, 나쁜 것 하나."),
      warn("헷갈리기 쉬운 점",
           f"{MLM} 의 빈칸은 학습 문제였어요. 이 쪽의 빈칸은 그 문제를 다시 꺼내 분석한 것이에요.",
           "coreference 는 이 과목에서 따로 배우지 않았어요. 앞에 나온 말을 가리키는 관계를 뜻해요.",
           f"{CORPUS}에 있던 것이 그대로 모델에 들어간다는 점이 다음 쪽 {MEMZ} 이야기로 이어져요.")])

# ---------------------------------------------------------------- p.43
page(43, "외우기도 해요",
     ["Memorization", "Pre-training", "Corpus", "Bias", "Parameter", "Label",
      "Large Language Model (LLM)", "World Knowledge"],
     [say(f"모델이 저장한 것 중 일부는 일반화가 아니에요.",
          f"학습 문서를 글자 그대로 복사해 둔 것이에요. 이것을 {MEMZ} 이라고 해요.",
          "그래서 개인정보 문제가 생겨요."),
      analogy("이해한 것과 그냥 외운 것",
              "시험 공부를 할 때 원리를 이해해서 응용하는 것과, 답안을 통째로 외워 두는 것은 달라요. 모델도 둘 다 해요.",
              ("원리를 이해해 응용하기", "일반화"),
              ("답안을 통째로 외우기", MEMZ),
              ("외운 답안을 그대로 뱉기", "전화번호 예"))],
     [points("슬라이드 영어와 우리말 뜻",
             "It Also Remembers = 외우기도 한다",
             "not a generalisation at all = 일반화가 전혀 아니다",
             "a verbatim copy of a training document = 학습 문서를 글자 그대로 복사한 것",
             "a prompt from the training data = 학습 데이터에 있던 글로 만든 프롬프트",
             "membership inference = 멤버십 추론, 어떤 문서가 학습에 쓰였는지 알아내기",
             "we only trained on it is not a privacy guarantee = 학습에만 썼다는 말이 개인정보 보장이 되지 않는다"),
      compare("일반화와 암기",
              ["보는 점", "일반화", MEMZ],
              ["저장한 것", "규칙과 경향", "문서 그대로"],
              ["새 입력에", "응용이 돼요", "그대로 튀어나와요"],
              ["좋은가", "우리가 원하는 것", "위험할 수 있어요"],
              ["예", "문법, 낱말 뜻", "전화번호, 주소"])],
     [look("슬라이드를 짚어 읽어요",
           (0.060, 0.198, 0.720, 0.040, "부제: 모델이 저장한 것 중 일부는 일반화가 아니라 글자 그대로의 복사예요."),
           (0.118, 0.441, 0.336, 0.105, "왼쪽 회색 상자: 내 전화번호는 으로 시작하는 프롬프트예요."),
           (0.118, 0.555, 0.336, 0.035, "아래 작은 글: 그 프롬프트가 학습 데이터에서 나왔어요."),
           (0.541, 0.441, 0.336, 0.105, "오른쪽 빨간 상자: 실제 그 번호가 그대로 나와요."),
           (0.541, 0.555, 0.336, 0.035, "작은 글: 진짜 문서에서 글자 그대로 나온 것이에요."),
           (0.156, 0.614, 0.687, 0.100, "아래 상자: 멤버십 추론과 학습에만 썼다는 말이 보장이 아니라는 결론.")),
      figure("외우기도 해요", FIG_MEM,
             "프롬프트 하나로 학습 문서가 그대로 나올 수 있어요.", 4),
      points("멤버십 추론이 무엇인지",
             "어떤 문서가 학습 데이터에 들어 있었는지 바깥에서 알아내는 것이에요",
             "모델이 그 문서에 유난히 자신 있게 반응하면 단서가 돼요",
             f"이 과목에서 자세히 다루지는 않아요. 결론만 기억하면 돼요",
             "학습에만 썼으니 괜찮다는 말이 개인정보 보장이 되지 않아요",
             f"N5 p.49 의 6번 문제가 바로 이 이야기를 물어요"),
      points("N5 p.42 와 이어 보기",
             f"앞 쪽에서 {PRE}이 문법과 뜻은 잘 배우고 {WK}은 군데군데라고 했어요",
             f"이 쪽은 거기에 하나를 더해요. 일부는 아예 통째로 외워 둔다는 것이에요",
             f"{BIAS}도 {MEMZ} 도 모두 {CORPUS}에서 그대로 온 것이에요",
             f"곧 데이터를 무엇으로 채우느냐가 그대로 모델에 남아요",
             f"이것이 N5 p.15 의 법과 윤리 문제와 이어져요")],
     [check(f"{MEMZ} 이 만드는 문제로 슬라이드가 든 것은",
            ["개인정보", "속도", "메모리 부족", "토큰 수 초과"], 0,
            "a privacy guarantee 라는 표현이 아래 상자에 있어요."),
      check("멤버십 추론이 뜻하는 것은",
            ["어떤 문서가 학습에 쓰였는지 알아내는 것",
             "모델 크기를 재는 것", "정확도를 재는 것", "레이블을 다는 것"], 0,
            "you can often tell whether a given document was in the training set 이에요."),
      english("시험 답안 문장",
              f"{PRE} 모델은 일반화뿐 아니라 학습 문서를 글자 그대로 {MEMZ} 하기도 하여 개인정보 문제가 될 수 있다.",
              "멤버십 추론까지 한 줄 덧붙이면 더 좋아요.",
              "외운다, 그대로 나온다, 그래서 위험하다."),
      warn("헷갈리기 쉬운 점",
           f"{MEMZ} 은 과적합과 다른 말이에요. 여기서는 학습 문서를 그대로 저장했다는 뜻이에요.",
           f"모든 {PARAM}가 암기에 쓰인다는 뜻이 아니에요. 일부가 그렇다는 것이에요.",
           f"{LLM} 이 클수록 더 많이 외운다는 값은 슬라이드에 없어요. 숫자를 지어내지 마세요.")])

# ---------------------------------------------------------------- p.44
page(44, "미세조정 레시피",
     ["Finetuning", "Learning Rate", "Epoch", "Batch Size", "Warmup", "Overfitting",
      "Pre-training", "Task Head", "Gradient Descent", "Parameter Initialisation", "Trainer"],
     [say(f"{FT}을 실제로 어떻게 하는지 알려 주는 쪽이에요.",
          "슬라이드가 못 박아요. 연구 과제가 아니라 숫자 네 개면 끝이에요.",
          "그리고 잘못되는 가장 흔한 길은 너무 빨리 움직이는 것이에요."),
      points("Devlin 등이 권하는 네 숫자",
             f"{LR}: 2e-5 에서 5e-5",
             f"{EPOCH}: 2 에서 4",
             f"{BS}: 16 또는 32",
             f"{WARM}: 전체 걸음의 처음 약 10 퍼센트")],
     [points("슬라이드 영어와 우리말 뜻",
             "The Finetuning Recipe = 미세조정 레시피",
             "Finetuning is not a research project = 미세조정은 연구 과제가 아니다",
             "Four numbers = 숫자 네 개",
             "the main way to get it wrong is to move too fast = 잘못되는 주된 길은 너무 빨리 움직이는 것",
             "100x smaller than pretraining = 사전 학습보다 100배 작다",
             "more than that and it overfits = 그보다 많이 돌리면 과적합이 난다",
             "the head starts from noise = 헤드는 잡음에서 출발한다"),
      compare("네 숫자와 그 이유",
              ["무엇", "값", "왜 그런가"],
              [LR, "2e-5 에서 5e-5", f"{PRE}보다 100배 작아요"],
              [EPOCH, "2 에서 4", f"더 돌면 {OVF}이 나요"],
              [BS, "16 또는 32", "메모리에 들어가는 만큼이에요"],
              [WARM, "처음 약 10 퍼센트 걸음", f"{HEAD}가 무작위에서 출발하기 때문이에요"])],
     [look("슬라이드를 짚어 읽어요",
           (0.060, 0.198, 0.720, 0.040, "부제: 연구 과제가 아니에요. 숫자 네 개이고, 망치는 길은 너무 빨리 움직이는 것이에요."),
           (0.110, 0.388, 0.180, 0.030, "Devlin et al. recommend: 곧 BERT 논문 저자들이 권하는 값이에요."),
           (0.110, 0.425, 0.560, 0.060, "첫 줄 learning rate: 2e-5 에서 5e-5, 사전 학습보다 100배 작아요."),
           (0.110, 0.490, 0.560, 0.060, "둘째 줄 epochs: 2 에서 4, 더 돌면 과적합이에요."),
           (0.110, 0.555, 0.560, 0.125, "셋째 줄 batch size 16 또는 32, 넷째 줄 warmup 처음 약 10 퍼센트."),
           (0.156, 0.688, 0.687, 0.062, "빨간 상자: 가장 흔한 실수는 사전 학습 학습률을 그대로 쓰는 것이에요.")),
      steps("Lab 4 설정으로 걸음 수를 계산해 봐요",
            ["학습 데이터가 15,000건이고 배치 크기가 32 예요",
             "한 에폭의 걸음 수는 15000 / 32 = 468.75 예요",
             "남는 것을 한 걸음으로 세면 469 걸음이에요",
             "에폭이 2 이므로 469 x 2 = 938 걸음이에요",
             "워밍업은 처음 약 10 퍼센트이니 938 x 0.1 = 93.8 이에요",
             "실습 노트북 N5L p.20 은 int 로 버려서 93 걸음을 써요"],
            "전체 938 걸음, 워밍업 93 걸음이에요.",
            "학습 15,000건, 배치 32, 에폭 2, 워밍업 10 퍼센트"),
      steps("사전 학습 학습률이 왜 위험한지 숫자로 봐요",
            [f"{FT} {LR}은 2e-5 예요",
             "슬라이드가 이것이 사전 학습보다 100배 작다고 적었어요",
             "그러면 사전 학습 학습률은 2e-5 x 100 = 2e-3 정도예요",
             "2e-3 은 2e-5 보다 100배 큰 보폭이에요",
             f"{GD}에서 보폭이 100배면 첫 걸음에 아주 멀리 가 버려요",
             "슬라이드 표현대로 모델이 알던 것을 전부 지워 버려요"],
            "보폭이 100배 크면 좋은 출발점에서 너무 멀리 튕겨 나가요.",
            "2e-5 대 2e-3"),
      figure("네 숫자와 한 가지 경고", FIG_RECIPE,
             "네 줄을 그대로 외우면 실전에서 바로 쓸 수 있어요.", 4),
      points(f"{WARM}이 왜 필요한지",
             f"{BODY}은 사전 학습된 좋은 값에서 출발해요",
             f"그런데 {HEAD}는 무작위 잡음에서 출발해요",
             "처음부터 큰 보폭으로 걸으면 잡음이 몸통까지 망쳐요",
             f"그래서 처음 10 퍼센트는 {GD}의 보폭을 0 에서 천천히 올려요",
             f"슬라이드 표현이 the head starts from noise 예요")],
     [check(f"{FT} {LR}로 슬라이드가 권한 값은",
            ["2e-5 에서 5e-5", "2e-3 에서 5e-3", "0.1 에서 0.5", "1e-8 에서 1e-7"], 0,
            "learning rate 줄에 2e-5 에서 5e-5 라고 적혀 있고 사전 학습보다 100배 작다고 했어요."),
      check(f"{EPOCH}을 2에서 4 로 제한하는 이유는",
            [f"더 돌면 {OVF}이 나기 때문", "메모리가 모자라서",
             "워밍업 때문에", "배치 크기 때문에"], 0,
            "more than that and it overfits 라고 적혀 있어요."),
      english("시험 답안 문장",
              f"{FT} 레시피는 {LR} 2e-5 에서 5e-5, {EPOCH} 2 에서 4 이다.",
              f"{BS}는 16 또는 32, {WARM}은 처음 약 10 퍼센트예요. 가장 흔한 실수는 사전 학습 학습률을 그대로 쓰는 것이에요.",
              "2e-5, 2에서 4, 16이나 32, 10 퍼센트. 네 숫자만 외워요."),
      warn("헷갈리기 쉬운 점",
           "2e-5 는 0.00002 예요. e-5 를 지수로 읽는 데 익숙해지세요.",
           f"{BS}는 성능을 결정하는 값이 아니라 메모리에 맞추는 값이에요.",
           f"슬라이드 원본은 2e-5 와 5e-5 사이, 2 와 4 사이를 en dash 로 적었어요. 우리는 에서 로 바꿔 적어요.")])

# ---------------------------------------------------------------- p.45
page(45, "레이블은 얼마나 필요한가",
     ["Label", "Pre-training", "Finetuning", "Learning Curve", "Diminishing Returns",
      "Accuracy", "Supervised Learning", "Chance Level", "NSMC (Naver Sentiment Movie Corpus)",
      "Sentiment Analysis", "Transfer Learning"],
     [say(f"{FT}에 {LABEL} 이 몇 개나 필요한지 보는 쪽이에요.",
          f"슬라이드 그림은 {LC} 두 개예요. 생각보다 적어도 꽤 멀리 갈 수 있어요.",
          f"그리고 {PRE}의 이득은 데이터가 적을 때 가장 커요."),
      analogy("이미 읽어 둔 신입과 아무것도 모르는 신입",
              "책을 잔뜩 읽어 둔 신입은 사례 몇백 개만 보여 줘도 일을 해요. 아무것도 모르는 신입은 사례 수만 개를 봐야 겨우 따라와요.",
              ("읽어 둔 신입", f"{PRE} + {FT}"),
              ("아무것도 모르는 신입", "처음부터 학습"),
              ("보여 준 사례 수", LABEL))],
     [points("슬라이드 영어와 우리말 뜻",
             "How Much Labelled Data Do You Need? = 레이블 붙은 데이터가 얼마나 필요한가",
             "Less than you think = 생각보다 적다",
             "pretraining buys you data = 사전 학습이 데이터를 사 준다",
             "a few hundred labels already get you a long way = 수백 개만으로도 꽤 멀리 간다",
             "the curves converge = 두 곡선은 결국 만난다",
             "but you will not have enough = 그런데 그만큼 모으지는 못한다",
             "schematic, not measured = 개념 그림이지 실제로 잰 값이 아니다"),
      compare("두 곡선이 말하는 것",
              ["레이블 수", f"{PRE} + {FT}", "처음부터 학습"],
              ["수백 개", "벌써 꽤 높아요", "거의 우연 수준이에요"],
              ["수천 개", "많이 올라요", "조금 올라요"],
              ["수만 개", "거의 평평해져요", "따라붙기 시작해요"],
              ["현실", "여기까지는 대개 가능", "이만큼 모으기 어려움"])],
     [look("슬라이드를 짚어 읽어요",
           (0.060, 0.198, 0.860, 0.055, "부제: 생각보다 적어요. 사전 학습의 이득은 수백에서 수천 개 자리에서 가장 커요."),
           (0.200, 0.380, 0.180, 0.032, "그림 위 작은 글: schematic, 곧 개념 그림이지 실제 측정값이 아니에요."),
           (0.068, 0.400, 0.410, 0.320, "초록 실선이 사전 학습 + 미세조정, 회색 점선이 처음부터 학습이에요."),
           (0.514, 0.400, 0.400, 0.075, "오른쪽 첫 항목: 사전 학습이 데이터를 사 줘요. 수백 개면 꽤 멀리 가요."),
           (0.514, 0.530, 0.400, 0.075, "둘째 항목: 레이블이 충분하면 곡선이 만나요. 다만 그만큼 못 모아요."),
           (0.514, 0.690, 0.360, 0.036, "맨 아래: 진짜 곡선은 Lab 4 에서 봐요.")),
      figure(f"{LC} 두 개", FIG_CURVE,
             "왼쪽 끝, 곧 레이블이 적을 때 세로 간격이 가장 커요.", 4),
      steps("Lab 4 에 저장된 진짜 숫자로 확인해 봐요",
            [f"{NSMC} 로 한국어 {BERT} 를 {FT}한 결과예요",
             f"{LABEL} 500개일 때 {ACC} 80.50 퍼센트예요",
             "2,000개일 때 84.18 퍼센트예요. 500개보다 3.68 올랐어요",
             "15,000개일 때 87.40 퍼센트예요. 2,000개보다 3.22 올랐어요",
             f"긍정 부정 두 가지니까 {CHANCE}은 약 50 퍼센트예요. 500개로도 30 이상 올라간 거예요",
             f"늘릴수록 오르는 폭이 줄어요. 이것이 {DR} 이에요"],
            f"수백 개만으로도 80 퍼센트를 넘어요. 그다음은 {DR} 이에요.",
            "레이블 500, 2,000, 15,000"),
      points("왜 데이터가 적을 때 차이가 큰지",
             f"{PRE}이 이미 문법과 낱말 뜻을 가르쳐 뒀어요",
             f"그래서 {FT}은 긍정과 부정을 가르는 방법만 배우면 돼요",
             "처음부터 학습하는 모델은 언어 자체를 레이블로 배워야 해요",
             f"언어를 {LABEL} 로 배우려면 예가 아주 많이 필요해요",
             f"슬라이드 표현대로 {PRE}이 데이터를 사 주는 셈이에요")],
     [check("슬라이드가 말한 사전 학습의 이득이 가장 큰 구간은",
            ["수백에서 수천 개", "수만 개", "수십만 개", "레이블이 0개일 때"], 0,
            "the gain is largest exactly where real projects live: small datasets 예요."),
      check(f"{LABEL} 을 아주 많이 모으면 어떻게 되나요",
            ["두 곡선이 만나요", "처음부터 학습이 더 좋아져요",
             "사전 학습 곡선이 내려가요", "아무 변화가 없어요"], 0,
            "the curves converge 예요. 다만 슬라이드가 곧바로 but you will not have enough 라고 덧붙여요."),
      english("시험 답안 문장",
              f"{PRE}의 이득은 {LABEL} 이 적을 때 가장 크고, 수백 개만으로도 상당한 {ACC}에 도달한다.",
              f"레이블이 아주 많아지면 처음부터 학습한 모델이 따라붙지만 현실에서는 그만큼 모으기 어려워요.",
              "적을 때 크다, 많으면 만난다. 두 마디로 외워요."),
      warn("헷갈리기 쉬운 점",
           f"슬라이드의 {LC}은 개념 그림이에요. schematic, not measured 라고 위에 적혀 있어요.",
           f"처음부터 학습한 쪽이 왼쪽 끝에서 {CHANCE}에 가까운 것도 그림이 그렇게 그려졌을 뿐이에요.",
           "위 계산에 쓴 숫자는 Lab 4 노트북에 저장된 출력이에요. 슬라이드 그림의 값이 아니에요.",
           f"Lab 4 노트북은 본문 글과 출력 숫자가 조금 달라요. 81.9 와 87.5 가 아니라 출력의 81.8 과 87.4 를 따라요.")])

# ---------------------------------------------------------------- p.46
page(46, "모든 가중치를 움직일 필요는 없어요",
     ["Parameter-efficient Finetuning (PEFT)", "LoRA", "Adapter", "Freezing",
      "Body", "Finetuning", "Parameter", "Pre-training", "Task Head", "Linear Probing"],
     [say(f"{FT}을 싸게 하는 방법을 보는 쪽이에요. 이름이 {PEFT} 예요.",
          f"{PRE}된 {BODY}을 얼려 두고 작은 부품만 학습시켜요.",
          "움직이는 가중치는 전체의 약 1 퍼센트예요."),
      analogy("옷을 통째로 고치지 않고 패치만 덧대기",
              "옷 전체를 다시 재봉하는 대신 작은 패치 하나만 덧대요. 옷은 그대로 두고 패치만 여러 장 만들어 두면 상황마다 갈아 붙일 수 있어요.",
              ("그대로 두는 옷", f"{FREEZE}된 {BODY}"),
              ("덧대는 작은 패치", ADAPT),
              ("패치를 여러 장 만들기", "과제마다 하나씩"))],
     [points("슬라이드 영어와 우리말 뜻",
             "You Need Not Move Every Weight = 모든 가중치를 움직일 필요는 없다",
             "PEFT = Parameter-efficient finetuning, 파라미터를 아끼는 미세조정",
             "freezes the pretrained body = 사전 학습된 몸통을 얼린다",
             "trains a small adapter instead = 대신 작은 어댑터를 학습시킨다",
             "about 1% of the weights = 가중치의 약 1 퍼센트",
             "a tiny trainable patch = 아주 작고 학습 가능한 패치",
             "one GPU, many tasks, one checkpoint each = GPU 한 장, 과제 여럿, 과제마다 저장본 하나"),
      compare("전체 미세조정과 PEFT",
              ["보는 점", f"전체 {FT}", PEFT],
              ["움직이는 가중치", "전부 (1억 1000만 개)", "약 1 퍼센트"],
              [BODY, "함께 학습", FREEZE],
              ["과제마다 저장할 것", "모델 전체", "작은 패치 하나"],
              ["필요한 GPU", "더 큰 것", "소비자용 한 장으로도"])],
     [look("슬라이드를 짚어 읽어요",
           (0.060, 0.198, 0.870, 0.040, "부제: PEFT 는 사전 학습된 몸통을 얼리고 작은 어댑터만 학습해요."),
           (0.131, 0.447, 0.337, 0.199, "왼쪽 파란 격자: 전체 미세조정. 모든 칸이 파랗게 움직여요."),
           (0.532, 0.447, 0.338, 0.199, "오른쪽 격자: 회색 칸은 얼어 있고 오른쪽 끝 초록 줄만 학습해요."),
           (0.814, 0.477, 0.023, 0.139, "초록 칸이 학습되는 약 1 퍼센트예요."),
           (0.120, 0.655, 0.760, 0.030, "격자 아래 설명: 왼쪽은 1억 1000만 개 전부, 오른쪽은 약 1 퍼센트."),
           (0.150, 0.700, 0.700, 0.070, "아래 두 줄: 같은 몸통에 작은 패치 하나, GPU 한 장으로 여러 과제.")),
      steps(f"{PEFT} 로 움직이는 {PARAM} 수를 계산해 봐요",
            ["BERT-base 의 전체 가중치는 1억 1000만 개예요 (N5 p.22)",
             "슬라이드가 약 1 퍼센트만 움직인다고 적었어요",
             "110,000,000 x 0.01 = 1,100,000 개예요",
             "곧 약 110만 개만 학습해요",
             "나머지 108,900,000 개, 곧 99 퍼센트는 얼어 있어요",
             "저장할 파일도 110만 개짜리 하나면 돼요"],
            "약 110만 개만 움직이고 나머지 99 퍼센트는 그대로예요.",
            "110M 의 1 퍼센트"),
      figure("패치만 갈아 붙이기", FIG_PEFT,
             "왼쪽은 전부 움직이고 오른쪽은 오른쪽 끝 줄만 움직여요.", 4),
      points(f"{LORA} 와 {ADAPT} 의 차이",
             f"{ADAPT} 는 얼린 층 사이사이에 작은 부품을 끼워 넣어요",
             f"{LORA} 는 기존 가중치 옆에 작은 덧붙임을 두고 그것만 학습해요",
             "슬라이드는 둘을 LoRA / adapters 로 묶어 적었어요",
             "이 과목에서 수식까지 들어가지는 않아요. 아이디어만 기억하면 돼요",
             f"{BODY}을 얼린다는 점은 둘 다 같아요"),
      bg("이어지는 개념",
         f"{FREEZE}만 하고 아주 단순한 분류기를 얹어 보는 것을 {PROBE} 이라고 해요.",
         f"Lab 4 에서 얼린 BERT 위에 로지스틱 회귀를 얹어 81.8 퍼센트가 나왔어요.",
         f"전체 {FT}은 87.4 퍼센트였어요. 몸통을 움직이면 더 좋아져요.")],
     [check(f"{PEFT} 가 학습하는 가중치의 비율은",
            ["약 1 퍼센트", "약 10 퍼센트", "약 50 퍼센트", "100 퍼센트"], 0,
            "슬라이드에 about 1% of the weights 라고 두 번 적혀 있어요."),
      check(f"{PEFT} 에서 {BODY}은 어떻게 되나요",
            [FREEZE, "함께 학습", "삭제", "무작위 초기화"], 0,
            "freezes the pretrained body 예요. 얼려 두고 작은 부품만 학습해요."),
      english("시험 답안 문장",
              f"{PEFT} 는 {BODY}을 {FREEZE} 하고 약 1 퍼센트만 학습하는 방법이다.",
              f"{LORA} 와 {ADAPT} 가 대표예요. GPU 한 장으로 과제마다 작은 저장본 하나씩 만들 수 있어요.",
              "얼리고, 1 퍼센트만, 패치로 저장. 세 마디로 외워요."),
      warn("헷갈리기 쉬운 점",
           f"{PEFT} 는 모델을 작게 만드는 것이 아니에요. 학습하는 부분만 작아요.",
           f"추론할 때는 여전히 전체 {PARAM}가 필요해요.",
           f"{PROBE} 과도 달라요. 프로빙은 몸통을 아예 안 건드리고 위에만 얹어 보는 것이에요.")])

# ---------------------------------------------------------------- p.47
page(47, "왜 크게 만드나",
     ["Scaling Laws", "Loss Function", "Parameter", "Token", "Large Language Model (LLM)",
      "Pre-training", "Corpus", "Transformer", "GPT"],
     [say("사람들이 왜 계속 모델을 키웠는지 설명하는 쪽이에요.",
          f"이유는 하나예요. {LOSS} 값이 예측 가능하게 줄어들기 때문이에요.",
          f"이 관계를 {SCALE} 이라고 불러요."),
      analogy("다음 시험 점수를 미리 아는 공부법",
              "공부 시간을 두 배, 네 배로 늘려 보고 점수를 적어 두면, 열여섯 배로 늘렸을 때 점수가 얼마가 될지 그림에서 읽어 낼 수 있어요.",
              ("공부 시간", "학습 계산량"),
              ("시험 점수", LOSS),
              ("그림에서 읽어 내기", SCALE))],
     [points("슬라이드 영어와 우리말 뜻",
             "Why Scale? = 왜 크게 만드나",
             "the loss curve is predictable = 손실 곡선이 예측 가능하다",
             "You can forecast a large model's performance from small ones = 작은 모델들로 큰 모델의 성능을 예측할 수 있다",
             "the curve is a straight line on a log-log plot = 로그-로그 그림에서 직선이다",
             "GPT-3: 175B parameters, 300B tokens = GPT-3 은 파라미터 1750억, 토큰 3000억",
             "that was the wrong split of the budget = 예산을 잘못 나눈 것이었다",
             "a 70B model trained on far more tokens beat it = 700억짜리를 훨씬 많은 토큰으로 학습한 쪽이 이겼다"),
      compare("두 가지 예산 나누기",
              ["모델", PARAM, TOK, "결과"],
              ["GPT-3 (2020)", "1750억", "3000억", "그때는 최고였어요"],
              ["나중의 700억 모델", "700억", "훨씬 더 많이", "이겼어요"],
              ["교훈", "크기만이 답은 아니에요", "크기와 데이터가 함께", "둘의 균형이 중요해요"])],
     [look("슬라이드를 짚어 읽어요",
           (0.060, 0.198, 0.860, 0.055, "부제: 손실 곡선이 예측 가능해요. 작은 모델로 큰 모델을 미리 알 수 있어요."),
           (0.165, 0.372, 0.290, 0.034, "그림 제목: 계산을 늘리면 손실이 예측 가능하게 낮아져요."),
           (0.068, 0.395, 0.410, 0.330, "파란 직선. 가로세로가 모두 로그 눈금이라 직선으로 보여요."),
           (0.552, 0.462, 0.360, 0.070, "오른쪽 첫 항목: 로그-로그에서 직선, 그래서 예측이 가능해요."),
           (0.552, 0.540, 0.380, 0.070, "둘째 항목: GPT-3 은 1750억 파라미터, 3000억 토큰이었어요."),
           (0.552, 0.620, 0.400, 0.070, "셋째 항목: 700억 모델을 훨씬 많은 토큰으로 학습한 쪽이 이겼어요.")),
      figure("로그-로그에서 직선", FIG_SCALING,
             "직선이라서 왼쪽 몇 점만 찍어 보면 오른쪽 끝을 예측할 수 있어요.", 4),
      steps("토큰과 파라미터의 비를 계산해 봐요",
            ["GPT-3 은 파라미터 1750억 개, 학습 토큰 3000억 개예요",
             "300 / 175 = 약 1.71 이에요",
             "곧 파라미터 하나당 토큰 약 1.7 개로 학습한 셈이에요",
             "나중 연구는 이 비가 너무 낮다고 봤어요",
             "파라미터를 175에서 70으로 줄이면 175 / 70 = 2.5 배 작아져요",
             "그만큼 아낀 계산을 토큰 쪽에 더 쓰니 더 좋아졌어요"],
            "크기와 데이터의 균형 문제예요. 크기만 키우는 것이 답이 아니었어요.",
            "1750억 파라미터, 3000억 토큰"),
      points("로그-로그 그림이 무엇인지",
             "가로축도 세로축도 10배마다 한 칸씩 가는 눈금이에요",
             "보통 눈금이면 이 곡선은 처음에 뚝 떨어지고 뒤는 거의 평평해 보여요",
             "로그 눈금으로 그리면 그것이 깔끔한 직선이 돼요",
             f"직선이면 자를 대고 오른쪽으로 늘여서 큰 모델의 {LOSS} 을 읽을 수 있어요",
             f"N5 p.33 의 GPT 크기 그림에도 같은 로그 눈금이 쓰였어요",
             f"여기서 키우는 것은 {TRF} 블록의 층 수와 폭이에요. 블록 자체는 4주차 것 그대로예요"),
      bg("기초 다지기 4단원",
         "로그는 몇 배인지를 덧셈으로 바꿔 주는 도구예요.",
         "10을 네 번 곱하면 10000 이고 로그로는 4 예요.",
         "그래서 10배 차이가 그림에서 같은 간격이 돼요.")],
     [check(f"{SCALE} 이 유용한 이유로 슬라이드가 든 것은",
            ["작은 모델로 큰 모델의 손실을 예측할 수 있어서",
             "학습이 빨라져서", "레이블이 필요 없어져서", "메모리를 아껴서"], 0,
            "You can forecast a large model's performance from small ones 예요."),
      check("GPT-3 의 파라미터와 토큰 수는",
            ["1750억 파라미터, 3000억 토큰", "700억 파라미터, 3000억 토큰",
             "1750억 파라미터, 1750억 토큰", "110M 파라미터, 3.3B 토큰"], 0,
            "오른쪽 둘째 항목에 175B parameters, 300B tokens 라고 적혀 있어요."),
      english("시험 답안 문장",
              f"{SCALE} 은 로그-로그 그림에서 {LOSS} 이 직선으로 줄어드는 관계로, 작은 모델로 큰 모델을 예측할 수 있게 한다.",
              f"다만 크기만 키우는 것이 답은 아니고 {PARAM}와 {TOK} 수의 균형이 중요해요.",
              "직선이라 예측된다, 크기와 데이터는 짝이다."),
      warn("헷갈리기 쉬운 점",
           "그림의 세로축은 손실이에요. 낮을수록 좋아요. 성능 곡선이 아니에요.",
           "700억 모델이 쓴 토큰 수는 슬라이드에 숫자로 적혀 있지 않아요. 훨씬 많다고만 적혀 있어요.",
           f"슬라이드가 다음 시간에 제대로 다시 다룬다고 적어 뒀어요. 여기서는 개념만 잡아요.")])

# ---------------------------------------------------------------- p.48
page(48, "이 패러다임이 이긴 이유",
     ["Pre-training", "Finetuning", "Label", "Self-Supervision", "Task Head",
      "Body", "Scaling Laws", "Transfer Learning", "Downstream Task", "Corpus"],
     [say("5주차의 결론에 해당하는 쪽이에요.",
          "이 방식이 이긴 것은 영리한 알고리즘 덕분이 아니에요.",
          "비용과 재사용이 맞아떨어졌기 때문이에요. 네 가지 이유가 상자 네 개로 적혀 있어요."),
      points("네 가지 이유",
             f"비싼 한 걸음을 한 번만 하고 계속 재사용해요",
             f"{LABEL} 이 더 이상 병목이 아니에요",
             f"한 구조로 모든 과제를 해요. {HEAD} 만 바꿔요",
             "키우면 같은 레시피로 계속 좋아져요")],
     [points("슬라이드 영어와 우리말 뜻",
             "Why This Paradigm Won = 왜 이 방식이 이겼나",
             "Nothing here is a clever algorithm = 여기에 영리한 알고리즘은 하나도 없다",
             "It won because of how the costs and the reuse work out = 비용과 재사용이 맞아떨어져서 이겼다",
             "One expensive step, reused forever = 비싼 한 걸음, 영원히 재사용",
             "Labels stop being the bottleneck = 레이블이 더는 병목이 아니다",
             "raw text is free, annotation is not = 날것의 글은 공짜, 표 붙이기는 아니다",
             "swap the head, keep the body = 헤드를 바꾸고 몸통은 그대로"),
      compare("네 상자를 한 표로",
              ["이유", "무슨 뜻인가", "어느 쪽에서 나왔나"],
              ["비싼 한 걸음, 영원히 재사용", f"{PRE}은 한 번, {FT}은 여러 번", "N5 p.13"],
              [f"{LABEL} 이 병목이 아니게", f"글은 공짜, 표 붙이기는 비쌈", "N5 p.12"],
              ["한 구조로 모든 과제", f"{HEAD} 만 바꾸고 {BODY}은 그대로", "N5 p.23"],
              ["키우면 계속 좋아짐", "같은 레시피, 크기만 크게", "N5 p.47"])],
     [look("슬라이드를 짚어 읽어요",
           (0.060, 0.198, 0.640, 0.040, "부제: 영리한 알고리즘은 없어요. 비용과 재사용이 맞아떨어져서 이겼어요."),
           (0.075, 0.426, 0.197, 0.245, "첫 상자: 비싼 한 걸음을 한 번만. 사전 학습 한 번, 미세조정 여러 번."),
           (0.293, 0.426, 0.197, 0.245, "둘째 상자: 레이블이 병목이 아니게. 날것의 글은 공짜예요."),
           (0.510, 0.426, 0.197, 0.245, "셋째 상자: 한 구조로 모든 과제. 헤드를 바꾸고 몸통은 그대로."),
           (0.727, 0.426, 0.197, 0.245, "넷째 상자: 키우면 계속 좋아져요. 같은 레시피로 크기만 크게."),
           (0.230, 0.690, 0.540, 0.036, "아래 굵은 글: 이 과목에서 앞으로 쓸 모델은 전부 사전 학습된 것이에요.")),
      figure("네 가지 이유", FIG_WON,
             "네 상자를 순서대로 읽으면 5주차 전체가 한 번에 정리돼요.", 4),
      points("네 이유가 어디서 나왔는지 되짚기",
             f"첫째는 N5 p.13 의 {PRE} 한 번, {FT} 여러 번 이야기예요",
             f"둘째는 N5 p.12 의 {SS} 이야기예요. 글 자체가 답이 돼요",
             f"셋째는 N5 p.23 의 네 가지 과제 모양 이야기예요. {BODY}은 그대로예요",
             f"넷째는 N5 p.47 의 {SCALE} 이야기예요",
             f"넷을 묶으면 이 과목이 말하는 {TL} 의 전부예요"),
      steps("비용이 어떻게 나뉘는지 따져 봐요",
            [f"{PRE}은 TPU 칩 64개로 4일이 걸렸어요 (N5 p.22)",
             "이것은 한 번만 하고, 우리는 결과만 내려받아요",
             f"{FT}은 GPU 한 장으로 몇 분에서 몇 시간이면 끝나요",
             f"우리가 치르는 값은 뒤 절반뿐이에요",
             f"그래서 {DOWN}가 늘어날수록 이 방식이 더 유리해져요"],
            "비싼 절반은 한 번, 싼 절반은 여러 번. 이것이 이긴 이유예요.",
            "사전 학습 비용과 미세조정 비용")],
     [check("슬라이드가 이 방식이 이긴 이유로 든 것이 아닌 것은",
            ["영리한 새 알고리즘", "비싼 한 걸음의 재사용",
             f"{LABEL} 병목이 사라진 것", "크기를 키우면 계속 좋아지는 것"], 0,
            "Nothing here is a clever algorithm 이라고 첫 줄에 못 박아 두었어요."),
      check("swap the head, keep the body 의 뜻은",
            [f"{HEAD} 만 바꾸고 {BODY}은 그대로 쓴다",
             "몸통만 바꾸고 헤드는 그대로 쓴다",
             "둘 다 새로 만든다", "둘 다 얼린다"], 0,
            "N5 p.23 에서 본 네 가지 과제 모양 이야기와 같은 말이에요."),
      english("시험 답안 문장",
              f"{PRE} 방식이 이긴 이유는 비싼 한 걸음의 재사용, {LABEL} 병목 해소, 한 구조로 모든 과제, 규모에 따른 지속 향상 네 가지이다.",
              f"영리한 알고리즘 때문이 아니라 비용과 재사용 구조 때문이라고 슬라이드가 못 박았어요.",
              "재사용, 레이블, 한 구조, 규모. 네 낱말로 외워요."),
      warn("헷갈리기 쉬운 점",
           f"{SS}이 {LABEL} 을 아예 없앤 것은 아니에요. {FT}에는 여전히 레이블이 필요해요.",
           "한 구조로 모든 과제라는 말은 아무 데이터나 그대로 넣어도 된다는 뜻이 아니에요.",
           f"이 네 가지는 서술형 문제로 나오기 좋아요. 근거 쪽까지 함께 외워 두세요.")])

# ---------------------------------------------------------------- p.49
page(49, "Check Yourself Part 2: 스스로 확인하기",
     ["Encoder", "Decoder", "Masked Language Modelling (MLM)", "Span Corruption",
      "Next Token Prediction", "BERT", "GPT", "Causal Masking", "Autoregressive",
      "In-Context Learning", "Prompt", "Gradient", "Label", "Finetuning",
      "Learning Rate", "Pre-training", "Memorization", "Classification",
      "Bidirectional Context", "Parameter"],
     [say("후반부를 다 들었는지 확인하는 쪽이에요. 교수님이 직접 낸 문제 여섯 개예요.",
          "5주차는 수업 녹음이 없어요. 그래서 답은 슬라이드 본문에서 근거를 찾아 정리했어요.",
          "근거가 된 쪽 번호를 풀이마다 적어 두었으니 그 쪽으로 돌아가 확인해 보세요."),
      points("여섯 문제를 우리말로",
             "1. 인코더, 디코더, 인코더 디코더의 사전 학습 목적 함수를 각각 대라",
             f"2. {GPT} 는 글을 쓸 수 있는데 {BERT} 는 왜 못 하나",
             f"3. {ICL} 에서 정확히 무엇이 학습되나",
             "4. 한국어 리뷰 800개와 Colab GPU 한 장이 있다. 어떤 모델을 고르고 왜인가",
             f"5. {FT} {LR}은 왜 {PRE} 학습률보다 훨씬 작은가",
             "6. 사전 학습 모델이 개인정보 문제가 될 수 있는 이유 하나를 대라")],
     [compare("슬라이드 영어와 우리말 뜻",
              ["영어 원문", "뜻"],
              ["Encoder, decoder, encoder-decoder: name the pretraining objective for each.",
               "세 구조 각각의 사전 학습 목적 함수를 대라"],
              ["Why can GPT generate text while BERT cannot?",
               "GPT 는 글을 만들 수 있는데 BERT 는 왜 못 하는가"],
              ["What exactly is learned during in-context learning?",
               "인컨텍스트 러닝 동안 정확히 무엇이 학습되는가"],
              ["You have 800 labelled Korean reviews and one Colab GPU. Which model do you pick, and why?",
               "레이블 붙은 한국어 리뷰 800개와 Colab GPU 한 장이 있다. 어떤 모델을 고르고 왜인가"],
              ["Why is the finetuning learning rate so much smaller than the pretraining one?",
               "미세조정 학습률은 왜 사전 학습 학습률보다 훨씬 작은가"],
              ["Give one reason a pretrained model can be a privacy problem.",
               "사전 학습 모델이 개인정보 문제가 될 수 있는 이유 하나를 대라"])],
     [look("여섯 문제를 짚어 읽어요",
           (0.06, 0.209, 0.56, 0.036, "1번: 세 구조의 목적 함수. 근거는 N5 p.17 과 p.50 이에요."),
           (0.06, 0.274, 0.35, 0.036, "2번: GPT 는 쓰고 BERT 는 못 쓰는 이유. 근거는 N5 p.25 와 p.30 이에요."),
           (0.06, 0.337, 0.38, 0.036, "3번: 인컨텍스트 러닝에서 학습되는 것. 근거는 N5 p.34 예요."),
           (0.06, 0.402, 0.68, 0.036, "4번: 리뷰 800개와 Colab GPU. 근거는 N5 p.35, p.40, p.45 예요."),
           (0.06, 0.467, 0.55, 0.036, "5번: 미세조정 학습률이 작은 이유. 근거는 N5 p.44 예요."),
           (0.06, 0.532, 0.45, 0.036, "6번: 개인정보 문제. 근거는 N5 p.43 이에요.")),
      steps("4번을 수업에서 배운 값으로 미리 계산해 봐요",
            ["레이블이 800개예요. 수백 개 자리이지 수만 개 자리가 아니에요",
             "N5 p.45 가 말해요. 이 구간에서 사전 학습의 이득이 가장 커요",
             "출력은 긍정 또는 부정 레이블 하나예요",
             "N5 p.40 표 첫 줄에 따라 인코더를 골라요",
             "N5 p.35 표에 따르면 미세조정은 1억 개 모델부터 되고 GPU 한 장이면 돼요",
             "Lab 4 에서 레이블 500개로도 80.50 퍼센트가 나왔어요"],
            "한국어 BERT 를 미세조정하는 것이 답이에요. Lab 4 가 그 일이에요.",
            "레이블 800개, Colab GPU 한 장")],
     [exam("N5 Check Yourself",
           "1. Encoder, decoder, encoder-decoder: name the pretraining objective for each.",
           "세 구조 각각의 사전 학습 목적 함수를 대세요.",
           ["근거 쪽은 N5 p.17 과 N5 p.50 요약 줄이에요",
            f"{ENC}는 {MLM} 이에요. 15 퍼센트를 가리고 원래 단어를 맞혀요",
            f"인코더 디코더는 {SC} 이에요. 슬라이드는 denoising 이라고도 적었어요",
            f"{DEC}는 {NTP} 이에요. 3주차 RNN 언어 모델과 같아요",
            "왜 이렇게 갈리는지도 한 줄 덧붙이면 좋아요",
            "쓸 수 있는 마스크가 무엇을 볼 수 있는지를 정하고, 그것이 가능한 목적 함수를 정해요"],
           f"{ENC}는 {MLM} 이고, 인코더 디코더는 {SC} 이에요."),
      exam("N5 Check Yourself",
           "2. Why can GPT generate text while BERT cannot?",
           f"{GPT} 는 글을 쓸 수 있는데 {BERT} 는 왜 못 하나요?",
           ["근거 쪽은 N5 p.25 와 N5 p.30 이에요",
            f"{GPT} 는 {CM} 아래에서 {NTP}으로 학습됐어요",
            f"그래서 자기가 만든 {TOK}을 다시 입력에 넣어 계속 쓸 수 있어요. 이것이 {AR} 이에요",
            f"{BERT} 는 {BC}으로 빈칸을 채우게 학습됐어요",
            "N5 p.25 표현대로 한 번에 한 빈칸이고, 계속 써 나갈 자연스러운 방법이 없어요",
            "그래서 자유로운 글이 필요하면 디코더를 써야 해요"],
           f"{GPT} 는 {NTP}과 {AR} 구조라 이어 쓸 수 있고, {BERT} 는 빈칸 채우기라 이어 쓸 길이 없어요."),
      exam("N5 Check Yourself",
           "3. What exactly is learned during in-context learning?",
           f"{ICL} 동안 정확히 무엇이 학습되나요?",
           ["근거 쪽은 N5 p.34 예요",
            "슬라이드 굵은 글: the weights never change 예요",
            f"곧 {PARAM} 는 하나도 바뀌지 않아요. {GRAD} 걸음도 0 이에요",
            f"바뀌는 것은 {PROMPT} 에 들어간 글뿐이에요",
            "예시는 다음 토큰의 확률 분포를 한쪽으로 기울일 뿐이에요",
            "그래서 엄밀히 말하면 학습되는 것은 아무것도 없어요"],
           "가중치 관점에서 학습되는 것은 없어요. 예시가 다음 토큰 분포를 조건 지을 뿐이에요."),
      exam("N5 Check Yourself",
           "4. You have 800 labelled Korean reviews and one Colab GPU. Which model do you pick, and why?",
           "레이블 붙은 한국어 리뷰 800개와 Colab GPU 한 장이 있어요. 어떤 모델을 고를까요?",
           ["근거 쪽은 N5 p.35, N5 p.40, N5 p.45 예요",
            f"출력이 긍정 또는 부정 {LABEL} 하나이므로 N5 p.40 표 첫 줄, 곧 {ENC} 예요",
            "예시 모델은 BERT 나 KLUE-BERT 처럼 한국어 인코더예요",
            f"N5 p.35 표에 따르면 {FT}은 1억 개 모델부터 되고 GPU 한 장이면 돼요",
            "N5 p.45 에 따르면 수백 개 레이블 구간이 사전 학습의 이득이 가장 큰 자리예요",
            f"N5 p.40 아래 줄도 고정된 {CLSF} 에는 1억짜리 인코더가 더 싸고 좋다고 했어요"],
           f"한국어 {BERT} 를 {FT}해요. 출력이 레이블 하나이고 데이터가 적고 GPU 가 한 장이기 때문이에요."),
      exam("N5 Check Yourself",
           "5. Why is the finetuning learning rate so much smaller than the pretraining one?",
           f"{FT} {LR}은 왜 {PRE} 학습률보다 훨씬 작을까요?",
           ["근거 쪽은 N5 p.44 예요",
            "슬라이드가 2e-5 에서 5e-5 를 권하고 사전 학습보다 100배 작다고 적었어요",
            f"{PRE}은 무작위에서 출발하니 크게 움직여야 해요",
            f"{FT}은 이미 좋은 출발점에 있으니 조금만 움직이면 돼요",
            "슬라이드 빨간 상자: 사전 학습 학습률을 그대로 쓰면 모델이 알던 것을 전부 지워 버려요",
            "곧 큰 보폭 한 걸음이 사전 학습이 심어 둔 것을 밀어내 버려요"],
           "좋은 출발점 근처에서 조금만 움직여야 하기 때문이에요. 큰 보폭은 배운 것을 지워 버려요."),
      exam("N5 Check Yourself",
           "6. Give one reason a pretrained model can be a privacy problem.",
           "사전 학습 모델이 개인정보 문제가 될 수 있는 이유를 하나 대세요.",
           ["근거 쪽은 N5 p.43 이에요",
            f"모델은 일반화만 하는 게 아니라 학습 문서를 글자 그대로 {MEMZ} 하기도 해요",
            "슬라이드 예: 내 전화번호는 으로 시작하는 프롬프트에 실제 번호가 그대로 나와요",
            "또 멤버십 추론으로 어떤 문서가 학습에 쓰였는지 알아낼 수도 있어요",
            "슬라이드 결론: 학습에만 썼다는 말이 개인정보 보장이 되지 않아요",
            "둘 중 하나만 써도 답이 돼요"],
           f"학습 문서를 글자 그대로 {MEMZ} 해서 그대로 뱉을 수 있기 때문이에요."),
      check("인코더 디코더의 사전 학습 목적 함수는",
            [SC, MLM, NTP, "다음 문장 예측"], 0,
            f"N5 p.17 의 가운데 상자에 span corruption ({DEN}) 이라고 적혀 있어요."),
      english("시험 답안 문장",
              f"{ENC}는 {MLM}, {DEC}는 {NTP}으로 사전 학습한다.",
              f"인코더 디코더는 {SC} 이에요. 1번 답이자 5주차 전체의 뼈대예요.",
              "빈칸은 인코더, 덩어리는 둘 다, 다음 토큰은 디코더."),
      warn("이 쪽을 쓸 때 주의할 점",
           "Check Yourself 는 교수님이 직접 낸 문제라 시험 대비 1순위예요.",
           "5주차는 녹음이 없어서 교수님이 답을 말해 준 기록이 없어요. 위 풀이는 슬라이드 근거로 세운 답이에요.",
           "4번처럼 상황을 주고 고르게 하는 문제는 이유를 두 개 이상 써야 점수가 나와요.")])

# ---------------------------------------------------------------- p.50
page(50, "마무리: 요약, Lab 4, 과제 3",
     ["Pre-training", "Self-Supervision", "Label", "Parameter Initialisation",
      "Finetuning", "Encoder", "Decoder", "Masked Language Modelling (MLM)",
      "Span Corruption", "Next Token Prediction", "BERT", "GPT", "T5",
      "World Knowledge", "Bias", "Memorization", "NSMC (Naver Sentiment Movie Corpus)",
      "Hugging Face", "Trainer", "Error Analysis", "Sentiment Analysis", "Scaling Laws"],
     [say("5주차를 일곱 줄로 정리하는 쪽이에요.",
          f"왜 {PRE}을 하는지, 패러다임이 무엇인지, 세 구조가 무엇인지, 무엇이 학습되는지예요.",
          "그리고 Lab 4 와 과제 3 안내, 다음 시간 예고가 있어요."),
      points("일곱 줄 요약",
             f"왜 사전 학습하나: {LABEL} 은 비싸고 날것의 글은 공짜예요",
             f"패러다임: {PRE}은 {PI} 예요. 한 번 하고 여러 번 {FT}해요",
             f"세 구조: {ENC}+빈칸, 인코더 디코더+{SC}, {DEC}+다음 토큰",
             f"무엇이 학습되나: 문법과 뜻은 잘, 사실은 군데군데, {BIAS}와 통째 복사도 함께")],
     [points("슬라이드 영어와 우리말 뜻",
             "Why pretrain: labels are expensive, raw text is free = 레이블은 비싸고 날것의 글은 공짜다",
             "self-supervision turns the internet into a training set = 자기 지도 학습이 인터넷을 학습 데이터로 바꾼다",
             "pretraining is parameter initialisation = 사전 학습은 파라미터 초기화다",
             "Pretrain once, finetune many times = 한 번 사전 학습하고 여러 번 미세조정한다",
             "syntax and semantics reliably, facts patchily = 문법과 의미는 믿을 만하게, 사실은 군데군데",
             "biases and verbatim text too = 편향과 글자 그대로의 글도 함께",
             "finetune a Korean BERT on NSMC with the HF Trainer = 허깅페이스 트레이너로 NSMC 에서 한국어 BERT 를 미세조정한다"),
      compare("세 구조와 세 목적 함수 (외울 표)",
              ["구조", "사전 학습 목적 함수", "대표 모델"],
              [ENC, MLM, BERT],
              ["인코더 디코더", SC, T5],
              [DEC, NTP, GPT])],
     [look("일곱 줄을 짚어 읽어요",
           (0.060, 0.207, 0.690, 0.036, "첫 줄 Why pretrain: 레이블은 비싸고 글은 공짜, 자기 지도 학습이 인터넷을 데이터로 바꿔요."),
           (0.060, 0.268, 0.580, 0.036, "둘째 줄 The paradigm: 사전 학습은 파라미터 초기화. 한 번 하고 여러 번 미세조정."),
           (0.060, 0.329, 0.860, 0.036, "셋째 줄 Three architectures: 세 구조와 세 목적 함수가 한 줄에 다 들어 있어요."),
           (0.060, 0.390, 0.640, 0.036, "넷째 줄 What gets pretrained: 문법과 의미는 잘, 사실은 군데군데, 편향과 통째 복사도."),
           (0.060, 0.452, 0.630, 0.036, "다섯째 줄 Lab 4 (1h): 허깅페이스 트레이너로 NSMC 에서 한국어 BERT 미세조정."),
           (0.060, 0.513, 0.480, 0.036, "여섯째 줄: 과제 3 이 오늘 나가고 8주차까지예요.")),
      figure("5주차를 한 줄로", FIG_WRAP,
             "위에서 아래로 읽으면 5주차 전체가 한 번에 정리돼요.", 4),
      points("Lab 4 안내 (실습 덱은 N5L 이에요)",
             f"Lab 4 는 1시간짜리이고 {NSMC} 로 한국어 {BERT} 를 {FT}해요",
             f"{HF} 의 {TRAINER} 를 써요. 학습 반복문을 대신 돌려 줘요",
             f"평가와 {EA} 까지 해요. 틀린 리뷰를 직접 들여다봐요",
             f"과제는 {SENTI} 이에요. 긍정인지 부정인지 맞히는 일이에요",
             "쪽마다 코드를 읽는 회독은 실습 덱 N5L 에서 해요"),
      points("세 구조를 마지막으로 한 번 더",
             f"{ENC}는 {BC}을 봐요. 그래서 빈칸 채우기를 해요",
             f"{DEC}는 {CM} 때문에 앞만 봐요. 그래서 다음 토큰 예측을 해요",
             f"인코더 디코더는 둘을 이어 붙였고 {SC}, 곧 {DEN} 게임으로 학습해요",
             f"셋 다 같은 {TRF} 블록을 써요. 다른 것은 마스크와 목적 함수뿐이에요",
             f"{T5} 는 여기에 {T2T} 를 더해 {MT} 도 요약도 같은 형식으로 풀어요"),
      points("과제 3 과 다음 시간",
             "과제 3 이 오늘 나가고 8주차까지예요. 자세한 내용은 수업 뒤 강의 페이지에 올라와요",
             "슬라이드에 적힌 것은 여기까지예요. 점수 비중은 적혀 있지 않아요",
             f"다음 시간 예고: 사전 학습 데이터 파이프라인, {SCALE}, 긴 학습을 안정적으로 유지하기",
             f"N5 p.47 에서 다음에 제대로 다시 다룬다고 한 것이 바로 {SCALE} 이에요")],
     [check("슬라이드 요약이 말한 세 구조와 목적 함수의 짝으로 맞는 것은",
            [f"{ENC}+빈칸, 인코더 디코더+{SC}, {DEC}+다음 토큰",
             f"{ENC}+다음 토큰, {DEC}+빈칸, 인코더 디코더+{SC}",
             "셋 다 빈칸 채우기",
             "셋 다 다음 토큰 예측"], 0,
            "Three architectures 줄에 encoder + masked LM (BERT), encoder-decoder + span corruption (T5), decoder + next-token prediction (GPT) 라고 적혀 있어요."),
      check("Lab 4 에서 하는 일은",
            [f"{NSMC} 로 한국어 {BERT} 미세조정", "GPT-3 사전 학습",
             "T5 로 번역", "토크나이저 만들기"], 0,
            "finetune a Korean BERT on NSMC with the HF Trainer 예요. 실습 덱은 N5L 이에요."),
      english("시험 답안 문장",
              f"{PRE}은 {PI}이며, 한 번 하고 여러 번 {FT}한다.",
              f"{ENC}는 빈칸 채우기, 인코더 디코더는 {SC}, {DEC}는 다음 토큰 예측이에요. {EA} 까지가 Lab 4 예요.",
              "왜, 무엇으로, 무엇이. 세 물음으로 나눠 외워요."),
      warn("잊지 말 것",
           "과제 3 은 오늘 나가고 8주차까지예요. 자세한 내용은 강의 페이지에서 확인하세요.",
           f"슬라이드 세 번째 줄의 구분 기호는 원본에 가운뎃점이 있어요. 우리는 쉼표로 적어요.",
           f"{MEMZ} 과 {BIAS}도 사전 학습이 가르친 것에 들어간다는 점을 요약에서 빠뜨리지 마세요.")])

data = {"deck": "N5", "from": 39, "to": 50,
        "glossary": [{"ko": k, "en": e, "say": s, "more": m} for k, e, s, m in GLOSSARY],
        "slides": S}

raw = json.dumps(data, ensure_ascii=False, indent=1)
for ch in ("—", "–", "·", "・"):
    assert ch not in raw, ch
with open(OUT, "w", encoding="utf-8") as f:
    f.write(raw)
print("saved", OUT, len(S), "pages")
