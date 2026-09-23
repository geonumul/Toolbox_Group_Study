# 1강(N1) 회독 레슨 1~27쪽 생성기. 사용: python build_N1_001-027.py
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "N1_001-027.json")
WHEN = "1주차 월요일 OT"
W, H = 1400, 788

MANTRA = "글을 토큰으로 자르고, 토큰을 벡터로 바꾸고, 벡터로 다음 토큰을 맞혀요."
HIST = "규칙 → 통계 → word2vec → seq2seq, 어텐션 → 트랜스포머, 사전 학습 → LLM"

# key: (ko, en, 받침) 받침 None 이면 ko 마지막 글자로. 0 모음, 1 받침, 2 ㄹ받침
TERMS = {
    "nlp": ("자연어처리", "Natural Language Processing (NLP)", None),
    "nlu": ("자연어 이해", "Natural Language Understanding (NLU)", None),
    "nlg": ("자연어 생성", "Natural Language Generation (NLG)", None),
    "amb": ("중의성", "Ambiguity", None),
    "aggl": ("교착어", "Agglutinative Language", None),
    "morph": ("형태소", "Morpheme", None),
    "manal": ("형태소 분석기", "Morphological Analyzer", None),
    "corpus": ("말뭉치", "Corpus", None),
    "token": ("토큰", "Token", None),
    "tok": ("토큰화", "Tokenization", None),
    "ngram": ("엔그램", "n-gram", None),
    "lm": ("언어 모델", "Language Model (LM)", None),
    "w2v": ("워드투벡", "word2vec", None),
    "wv": ("단어 벡터", "Word Vector", None),
    "dh": ("분포 가설", "Distributional Hypothesis", None),
    "rnn": ("순환 신경망", "Recurrent Neural Network (RNN)", None),
    "lstm": ("장단기 메모리", "LSTM", None),
    "hid": ("은닉 상태", "Hidden State", None),
    "s2s": ("시퀀스-투-시퀀스", "seq2seq", None),
    "att": ("어텐션", "Attention", None),
    "tf": ("트랜스포머", "Transformer", None),
    "pre": ("사전 학습", "Pre-training", None),
    "post": ("사후 학습", "Post-training", None),
    "llm": ("대규모 언어 모델", "Large Language Model (LLM)", None),
    "param": ("파라미터", "Parameter", None),
    "cls": ("분류", "Classification", None),
    "ner": ("개체명 인식", "Named Entity Recognition (NER)", None),
    "cnn": ("합성곱 신경망", "Convolutional Neural Network (CNN)", None),
    "turing": ("튜링 테스트", "Turing Test", None),
    "eliza": ("엘리자", "ELIZA", None),
    "gib": ("조지타운-IBM 시연", "Georgetown-IBM Experiment", None),
    "mt": ("기계 번역", "Machine Translation (MT)", None),
    "alpac": ("ALPAC 보고서", "ALPAC Report", None),
    "dart": ("다트머스 워크숍", "Dartmouth Workshop", None),
    "ai": ("인공지능", "Artificial Intelligence (AI)", None),
    "rule": ("규칙 기반 방법", "Rule-based Approach", None),
    "stat": ("통계 기반 방법", "Statistical Approach", None),
    "noisy": ("잡음 채널 모델", "Noisy Channel Model", None),
    "nn": ("신경망", "Neural Network", None),
    "enc": ("인코더", "Encoder", None),
    "dec": ("디코더", "Decoder", None),
    "ft": ("미세 조정", "Fine-tuning", None),
    "scale": ("스케일링 법칙", "Scaling Laws", None),
    "icl": ("문맥 내 학습", "In-context Learning", None),
    "it": ("지시 학습", "Instruction Tuning", None),
    "rlhf": ("인간 피드백 강화 학습", "RLHF", None),
    "bert": ("", "BERT", 0),
    "gpt": ("", "GPT", 0),
    "chatgpt": ("", "ChatGPT", 0),
    "exaone": ("엑사원", "EXAONE", None),
    "prag": ("화용론", "Pragmatics", None),
    "ellip": ("생략", "Ellipsis", None),
    "ref": ("지시 대상", "Reference", None),
    "wino": ("위노그라드 스키마", "Winograd Schema", None),
    "hon": ("높임법", "Honorifics", None),
    "lowres": ("저자원 자연어처리", "Low-resource NLP", None),
    "seqlab": ("시퀀스 레이블링", "Sequence Labeling", None),
    "pos": ("품사 태깅", "Part-of-Speech Tagging (POS)", None),
    "senti": ("감성 분석", "Sentiment Analysis", None),
    "rag": ("검색 증강 생성", "Retrieval-Augmented Generation (RAG)", None),
    "agent": ("에이전트", "Agent", None),
    "torch": ("파이토치", "PyTorch", None),
    "hf": ("허깅 페이스", "Hugging Face", None),
    "tp": ("텀 프로젝트", "Term Project", None),
    "pa": ("프로그래밍 과제", "Programming Assignment", None),
}

JOSA = {"은": ("은", "는"), "이": ("이", "가"), "을": ("을", "를"), "과": ("과", "와"),
        "으로": ("으로", "로"), "이에요": ("이에요", "예요"), "이라는": ("이라는", "라는"),
        "이나": ("이나", "나"), "이고": ("이고", "고"), "이라고": ("이라고", "라고"), "이죠": ("이죠", "죠")}


def _fin(key):
    ko, en, f = TERMS[key]
    if f is not None:
        return f
    c = ko[-1]
    j = (ord(c) - 0xAC00) % 28
    return 0 if j == 0 else (2 if j == 8 else 1)


def K(key, josa=""):
    ko, en, _ = TERMS[key]
    s = f"**{ko}({en})**" if ko else f"**{en}**"
    if not josa:
        return s
    f = _fin(key)
    if josa == "으로":
        return s + ("로" if f in (0, 2) else "으로")
    a, b = JOSA[josa]
    return s + (a if f else b)


def E(*keys):
    return [TERMS[k][1] for k in keys]


# ---------- 장면 ----------
def say(*l): return {"kind": "say", "lines": list(l)}
def pts(h, *i): return {"kind": "points", "head": h, "items": list(i)}
def cmp(h, cols, rows): return {"kind": "compare", "head": h, "cols": cols, "rows": rows}
def ana(h, scene, m): return {"kind": "analogy", "head": h, "scene": scene, "map": m}
def chk(q, ch, a, why): return {"kind": "check", "q": q, "choices": ch, "a": a, "why": why}
def eng(h, en, ko, tip=None):
    d = {"kind": "english", "head": h, "en": en, "ko": ko}
    if tip: d["tip"] = tip
    return d
def warn(h, *i): return {"kind": "warn", "head": h, "items": list(i)}
def prof(*l): return {"kind": "prof", "when": WHEN, "lines": list(l)}
def bg(src, *l): return {"kind": "bg", "src": src, "lines": list(l)}
def steps(h, st, ans, given=None):
    d = {"kind": "steps", "head": h, "steps": st, "answer": ans}
    if given: d["given"] = given
    return d
def fig(h, svg, cap, b): return {"kind": "figure", "head": h, "svg": svg, "caption": cap, "builds": b}
def formula(h, tex, parts, whole): return {"kind": "formula", "head": h, "tex": tex, "parts": [{"sym": s, "say": t} for s, t in parts], "whole": whole}
def exam(src, q, qko, solve, ans): return {"kind": "exam", "src": src, "q": q, "qko": qko, "solve": solve, "answer": ans}
def bx(x1, y1, x2, y2, s):
    return {"x": round(x1 / W, 3), "y": round(y1 / H, 3), "w": round((x2 - x1) / W, 3), "h": round((y2 - y1) / H, 3), "say": s}
def look(h, *b): return {"kind": "look", "head": h, "boxes": list(b)}


# ---------- SVG ----------
def SVG(*els, h=270): return f'<svg viewBox="0 0 480 {h}" xmlns="http://www.w3.org/2000/svg">' + "".join(els) + "</svg>"
def _c(cls, b): return cls + (f" b{b}" if b else "")
def R(x, y, w, h, cls="n", b=0): return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="2" class="{_c(cls, b)}"/>'
def TX(x, y, s, cls="t", size=14, anchor="middle", b=0): return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" class="{_c(cls, b)}">{s}</text>'
def L(x1, y1, x2, y2, cls="e", b=0): return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{_c(cls, b)}"/>'
def AR(x1, y, x2, b=0):
    return L(x1, y, x2 - 8, y, "e2", b) + f'<polygon points="{x2},{y} {x2 - 9},{y - 5} {x2 - 9},{y + 5}" class="{_c("arrow", b)}"/>'


def FIG_TL(hi=None):
    labels = ["규칙", "통계", "워드투벡(word2vec)", "seq2seq + 어텐션", "트랜스포머 + 사전 학습", "LLM"]
    years = ["1950s~80s", "1990s~2000s", "2013", "2014~16", "2017~18", "2020~"]
    els = []
    for i in range(6):
        b = i // 2 + 1
        x, y = 110 + i * 28, 14 + i * 42
        els.append(TX(100, y + 21, years[i], "tm", 14, "end", b))
        els.append(R(x, y, 210, 32, "n2" if i == hi else "n", b))
        els.append(TX(x + 105, y + 21, labels[i], "tl", 14, "middle", b))
    return SVG(*els)


def tl_fig(hi, where):
    cap = "지금 보는 곳: " + where + ". 아래로 갈수록 사람 손 규칙은 줄고, 데이터에서 배우는 몫이 커져요." if where else "여섯 계단을 한 번에 외워요. 아래로 갈수록 데이터에서 배우는 몫이 커져요."
    return fig("NLP 역사 여섯 계단", FIG_TL(hi), cap, 3)


S = []


def page(p, title, terms, p1, p2=None, p3=None, p4=None):
    S.append({"p": p, "title": title, "terms": terms, "pass1": p1, "pass2": p2 or [], "pass3": p3 or [], "pass4": p4 or []})

# ================= 1부: 강의 계획 =================
page(1, "Natural Language Processing (표지)", E("nlp"), [
    say(f"{K('nlp')} 첫 시간이에요.",
        "2026년 2학기, 가톨릭대학교 인공지능학과 전공선택 과목이에요.",
        "이 과목의 주문을 먼저 들어 두세요.",
        MANTRA),
])

page(2, "Reminder", [], [
    say("수업 자료는 저작권 있는 그림이 들어 있어서 밖으로 퍼뜨리면 안 돼요.",
        "수강생 학습용으로만 쓰라고 하셨어요.",
        "화면이나 소리에 문제가 있으면 참지 말고 바로 말해 달라고 하셨어요."),
])

page(3, "Contents", E("nlp"), [
    say("1. Syllabus & Introduction: 수업이 어떻게 돌아가고 어떻게 평가되는지",
        f"2. What is NLP?: {K('nlp', '이')} 무엇이고 왜 어려운지",
        "3. A Brief History of NLP: 70년 역사를 다섯 막으로",
        "4. How Machines Read Text: 기계가 글을 읽는 법(다음 주 이야기)"),
    say("실제 오늘 덱의 4부는 교수님 연구실(MINT Lab) 소개로 끝나요.",
        "목차 4번 제목과 실제 4부가 달라도 놀라지 마세요."),
])

FIG_ROAD = SVG(
    TX(240, 40, "한 학기 로드맵", "tb", 16),
    R(10, 90, 100, 70, "n2", 1), TX(60, 120, "기초", "tl", 15, "middle", 1), TX(60, 144, "1~4주", "tl", 14, "middle", 1),
    AR(112, 125, 128, 2),
    R(130, 90, 100, 70, "n", 2), TX(180, 120, "LLM 학습", "tl", 15, "middle", 2), TX(180, 144, "5~7주", "tl", 14, "middle", 2),
    AR(232, 125, 248, 3),
    R(250, 90, 100, 70, "n", 3), TX(300, 120, "적응, 시스템", "tl", 15, "middle", 3), TX(300, 144, "9~11주", "tl", 14, "middle", 3),
    AR(352, 125, 368, 4),
    R(370, 90, 100, 70, "n", 4), TX(420, 120, "평가, 최전선", "tl", 15, "middle", 4), TX(420, 144, "12~14주", "tl", 14, "middle", 4),
    TX(240, 210, "8주: 텀 프로젝트 제안 발표", "tm", 14, "middle", 4),
    TX(240, 236, "16주: 기말고사 (중간고사는 없어요)", "tm", 14, "middle", 4),
)

page(4, "1. Syllabus | Course at a Glance", E("nlp", "token", "tok", "tf", "llm", "rag", "agent"), [
    say("이 쪽은 수업 소개 카드예요.",
        f"한 학기 동안 '{TERMS['token'][0]}이 뭐지?' 에서 출발해요.",
        f"끝에는 {K('llm')} 시스템을 만들고 평가하는 데까지 가요."),
], [
    cmp("슬라이드 영어, 우리말로", ["영어", "뜻"], [
        ["Course", "자연어처리, 06488-01, 전공선택 3학점 3시간"],
        ["When & where", "월요일 7~9교시, B345 강의실, 이론 + 실습"],
        ["What we cover", f"{K('tok')}부터 {K('tf')}, LLM 학습, RAG, 에이전트까지"],
        ["You need", "파이썬을 편하게 쓰기. 머신러닝, 딥러닝 기초는 있으면 도움"],
    ]),
    pts("처음 보는 이름 미리 맛보기",
        f"{K('token')}: 글을 컴퓨터가 다루는 작은 조각으로 자른 것(레고 조각)",
        f"{K('tf')}: 요즘 거의 모든 언어 모델의 뼈대(4주차)",
        f"{K('rag')}: 먼저 자료를 찾아 보고 답하게 하는 방법(10주차)",
        f"{K('agent')}: 도구를 쓰며 여러 단계 일을 해내는 LLM(11주차)"),
    chk("이 수업을 듣는 데 꼭 필요하다고 한 것은?", ["파이썬을 편하게 쓰기", "딥러닝 수업 이수", "언어학 전공"], 0,
        "슬라이드의 You need 는 comfortable Python 이에요. 머신러닝, 딥러닝 기초는 '있으면 도움' 이에요."),
], [
    look("슬라이드 짚어 읽기",
         bx(100, 152, 1080, 188, "Course: 자연어처리, 06488-01 분반, 전공선택, 3 credits / 3 hours"),
         bx(100, 203, 975, 238, "When & where: 월요일 7~9교시, B345. lecture + hands-on practice = 이론 + 실습"),
         bx(100, 338, 1060, 374, f"What we cover: {K('tok')}부터 Transformers, LLM training, RAG, agents 까지"),
         bx(100, 389, 1065, 424, "You need: comfortable Python. we build up the neural parts as we go = 신경망은 수업에서 차근차근"),
         bx(340, 678, 1065, 708, "한 학기: '토큰이 뭐지?' 에서 LLM 시스템을 만들고 평가하기까지")),
    prof("선수 과목은 딱히 없어요. 1, 2, 3, 4학년이 골고루 섞여 있어요.",
         "파이썬만 편하게 쓰면 실습, 과제, 팀 프로젝트에 큰 문제 없어요.",
         "머신러닝, 딥러닝을 들었으면 더 편하지만, 천천히 따라오면 돼요."),
], [
    chk("이 수업의 시간과 장소는?", ["월요일 7~9교시, B345", "화요일 1~3교시, B345", "월요일 1~3교시, N223"], 0,
        "When & where 줄: Monday 7~9교시, B345 예요. N223 은 교수님 연구실 번호예요."),
    warn("헷갈리기 쉬운 점",
         "선수 과목은 없지만 파이썬은 미리 익혀 두세요.",
         "교수님: '호기심과 파이썬을 다음 주까지 챙겨 오세요.'"),
])

page(5, "1. Syllabus | What This Course Is About", E("nlp", "tok", "att", "tf", "pre", "post", "rag", "agent", "torch", "hf"), [
    say(f"이 과목 = {K('nlp')} 기초 + 요즘 언어 모델이에요.",
        "그리고 모든 개념을 직접 코드로 돌려 봐요."),
    fig("한 학기 로드맵", FIG_ROAD, "기초 → LLM 학습 → 적응과 시스템 → 평가와 최전선 순서로 가요.", 4),
], [
    pts("슬라이드 핵심 문장 뜻",
        "**foundations of NLP + modern language models** = 자연어처리 기초 + 최신 언어 모델",
        f"**hands-on with PyTorch & Hugging Face** = {K('torch')}와 {K('hf')}로 직접 해 보기",
        "**Implementation first** = 구현이 먼저, 모든 개념에 직접 돌리는 코드가 붙어요"),
    cmp("강의 목표 4가지 (Goals)", ["영어 요지", "뜻"], [
        ["1. fundamental concepts", f"{K('nlp')}의 기본 개념과 방법 이해"],
        ["2. attention, Transformer, LM training", f"{K('att')}, {K('tf')} 구조, 언어 모델 학습 이해"],
        ["3. implement and fine-tune", "파이썬, 파이토치, 허깅 페이스로 직접 구현하고 미세 조정"],
        ["4. Korean & multilingual", "한국어와 여러 언어용 믿을 만한 시스템 설계, 평가"],
    ]),
    chk("강의 목표 4번에서 특히 챙기는 언어는?", ["한국어와 다국어", "파이썬만", "영어만"], 0,
        "Design and evaluate reliable NLP systems for Korean & multilingual applications 예요."),
], [
    look("슬라이드 짚어 읽기",
         bx(100, 152, 1080, 187, "This course = foundations of NLP + modern language models"),
         bx(100, 197, 1070, 262, f"Topics: {K('tok')}, 표현 학습, {K('att')}, {K('pre')}, {K('post')}, RAG, agents, 평가, 다국어, 책임 있는 AI"),
         bx(140, 352, 970, 500, "Goals 1~4: 이해 두 개, 구현 하나, 설계와 평가 하나"),
         bx(75, 560, 1350, 670, "네 칸: W1~4 기초, W5~7 LLM 학습, W9~11 PEFT, RAG, agents, W12~14 평가, 추론, 한국어 NLP"),
         bx(370, 692, 1035, 720, "Implementation first: 모든 개념에 직접 돌리는 코드")),
    prof("한 문장으로 요약하면, NLP 기초부터 최신 언어 모델까지",
         "파이토치와 허깅 페이스로 직접 만들어 보면서 배우는 수업이에요.",
         f"{K('tok')}부터 {K('agent')}까지 LLM 업계 기술 스택 전체를 한 학기에 훑어요."),
    pts("오늘 덱에서 이미 이름이 나오는 것",
        f"{K('pre')}: 라벨 없는 거대한 글로 먼저 언어를 익히기(5~6주차)",
        f"{K('post')}: 사전 학습 뒤 사람이 원하는 대로 다듬기(7주차)"),
], [
    chk("로드맵 네 칸의 순서로 맞는 것은?",
        ["기초 → LLM 학습 → 적응과 시스템 → 평가와 최전선", "LLM 학습 → 기초 → 평가 → 적응", "평가 → 기초 → 적응 → LLM 학습"], 0,
        "W1~4 Foundations, W5~7 Training LLMs, W9~11 Adaptation & systems, W12~14 Evaluation & frontiers 예요."),
    eng("강의 목표 한 줄", "이 수업은 자연어처리(NLP)의 기초 개념을 이해하고, 어텐션과 트랜스포머(Transformer), 언어 모델 학습을 이해하며, 파이토치와 허깅 페이스로 구현하고, 한국어와 다국어 시스템을 설계, 평가하는 것을 목표로 한다.",
        "이해 2개(기초, 트랜스포머) + 구현 1개 + 설계와 평가 1개", "이해, 이해, 구현, 평가 네 박자로 외워요."),
    warn("헷갈리기 쉬운 점", "로드맵에 8주차가 빠져 있어요. 8주차는 텀 프로젝트 제안 발표 주예요."),
])

page(6, "1. Syllabus | Weekly Plan (16 Weeks)", E("nlp", "llm", "tok", "wv", "cnn", "rnn", "lm", "att", "tf", "bert", "gpt", "pre", "post", "rlhf", "rag", "agent", "tp"), [
    say("16주 계획표예요.",
        "1~4주 기초, 5~7주 LLM 학습, 8주 팀 프로젝트 제안, 9~14주 최신 기술이에요.",
        "16주가 기말고사예요. 중간고사는 없어요!"),
], [
    cmp("큰 구간으로 보기", ["주", "무엇"], [
        ["1~4주", f"기초: {K('tok')}, {K('wv')}, 신경망, {K('att')}과 {K('tf')}"],
        ["5~7주", f"LLM 학습: {K('bert')}, {K('gpt')}, {K('pre')}, {K('post')}"],
        ["8주", f"{K('tp')} 제안 발표 (중간고사 대신)"],
        ["9~14주", f"적응, {K('rag')}, {K('agent')}, 평가, 추론, 한국어"],
        ["15~16주", "15주 보강, 16주 기말고사"],
    ]),
    chk("이 수업에 중간고사가 있나요?", ["없다. 8주차 텀 프로젝트 제안 발표로 대신한다", "있다. 8주차에 본다", "있다. 15주차에 본다"], 0,
        "No midterm, week 8 is your term-project proposal 이에요."),
], [
    look("표 짚어 읽기",
         bx(75, 212, 700, 432, "1~4주: 소개와 역사, 토큰화와 단어 벡터, CNN과 RNN과 언어 모델, 어텐션과 트랜스포머"),
         bx(75, 432, 700, 597, "5~7주: BERT, GPT, T5 / 사전 학습(휴강 표시) / 사후 학습 SFT, RLHF, DPO"),
         bx(75, 597, 700, 652, "8주: Term project, proposal"),
         bx(700, 212, 1330, 377, "9~11주: LoRA 같은 효율적 적응, 검색과 RAG, 에이전트와 도구 사용"),
         bx(700, 377, 1330, 542, "12~14주: LLM-as-a-judge 평가, 추론(CoT), 한국어와 다국어, 안전과 편향"),
         bx(290, 680, 1115, 710, "아래 줄: 중간고사 없음, 휴강한 주는 15주차에 보강")),
    cmp("1~8주 자세히 (우리 스터디는 1~3주)", ["주", "주제"], [
        ["1", "과목 소개, NLP 와 LLM 의 역사 (오늘)"],
        ["2", f"{K('tok', '과')} {K('wv')}, 한국어 서브워드"],
        ["3", f"신경망 기초: {K('cnn')}, {K('rnn')}, 언어 모델링"],
        ["4", f"{K('att')}과 {K('tf')} 구조"],
        ["5~6", f"사전 학습된 LM({K('bert')}, {K('gpt')}, T5), {K('pre')}의 데이터와 규모"],
        ["7~8", f"{K('post')}(SFT, {K('rlhf')}, DPO), 8주 {K('tp')} 제안"],
    ]),
    cmp("9~16주 자세히", ["주", "주제"], [
        ["9", "효율적 적응: 프롬프트, LoRA/QLoRA, 양자화"],
        ["10", f"검색과 {K('rag')}: 임베딩, 재순위, 근거 대기"],
        ["11", f"{K('agent')}와 도구 사용: 계획, 기억, 실패 복구"],
        ["12~13", "벤치마크와 평가(LLM-as-a-judge), 추론과 효율적 추론(CoT)"],
        ["14", "한국어와 다국어 NLP, 안전과 편향"],
        ["15~16", "15주 보강주, 16주 기말고사"],
    ]),
    prof("계획서에는 5주차가 휴강인데, 오늘(8월 31일)이 1주차가 되어서 이 표로는 6주차가 휴강이에요.",
         "개천절 대체 휴일 때문이고, 보강이 있어요.",
         "8주차에는 팀을 미리 짜서 각 팀이 어떤 주제로 할지 발표해요."),
], [
    chk("3주차 주제에 들어 있지 않은 것은?", [K("cnn"), K("rnn"), K("rag")], 2,
        f"3주차는 {K('cnn')}, {K('rnn')}, 언어 모델링이에요. RAG 는 10주차예요."),
    chk("8주차에 하는 일은?", ["텀 프로젝트 제안 발표", "중간고사", "기말고사"], 0, "Week 8 is your term-project proposal 이에요."),
    warn("헷갈리기 쉬운 점",
         "슬라이드 안에서 휴강 주 표기가 섞여 있어요. 표에는 6주차 칸에 '휴강 → W15 보강', 아래 줄과 15주차 칸에는 'W5' 라고 적혀 있어요.",
         "녹음 설명: 계획서 기준 5주차, 이 표 기준 6주차가 휴강(개천절 대체 휴일)이고 보강은 15주차예요."),
])

page(7, "1. Syllabus | Textbooks & Resources", E("tf", "nlp", "llm", "torch", "hf"), [
    say("교재와 도구 소개 쪽이에요.",
        "책을 다 살 필요는 없어요. 강의 자료와 실습 자료로 충분하다고 하셨어요."),
], [
    cmp("책 세 권 정리", ["구분", "책", "한 줄"], [
        ["Main textbook (교재)", "트랜스포머를 활용한 자연어 처리", "허깅 페이스 팀이 직접 쓴 책"],
        ["Secondary (부교재)", "밑바닥부터 만들면서 배우는 LLM", "모든 걸 직접 구현하는 정신을 따라요"],
        ["Reference (참고)", "자연어 처리를 위한 허깅페이스 트랜스포머 하드 트레이닝", "참고용"],
    ]),
    chk("실습(hands-on)은 어디에서 돌리나요?", ["Colab (무료 GPU)", "학교 서버", "개인 노트북만"], 0,
        "Tools 줄: hands-on work runs in Colab (free GPU) 예요."),
], [
    look("슬라이드 짚어 읽기",
         bx(100, 150, 1215, 215, f"주교재: 트랜스포머를 활용한 자연어 처리(Natural Language Processing with Transformers), {K('hf')} 팀의 책"),
         bx(100, 230, 915, 295, "부교재: 밑바닥부터 만들면서 배우는 LLM(Build a Large Language Model From Scratch)"),
         bx(100, 357, 1105, 390, "무료 고전: Jurafsky & Martin 의 Speech and Language Processing 3판, Stanford CS224N"),
         bx(100, 405, 1015, 438, f"도구: Python, {K('torch')}, Hugging Face transformers, 실습은 Colab"),
         bx(100, 452, 730, 485, "슬라이드와 공지: 사이버캠퍼스(LMS), 수업마다 올려요"),
         bx(260, 682, 1145, 710, "모든 책을 살 필요 없어요. 주교재 + 무료 자료면 충분")),
    prof("교재 순서대로 나가지 않아요. 올려 주는 강의 자료를 보며 진행해요.",
         "책을 꼭 살 필요는 없어요. PPT 슬라이드와 실습 자료로 충분하고, 어려울 때 참고하세요.",
         "파이썬 기본 문법만 알아도 강의와 실습에서 큰 문제 없어요."),
], [
    chk("강의 슬라이드와 공지는 어디에 올라오나요?", ["사이버캠퍼스(LMS)", "교수님 연구실 홈페이지", "카카오톡 단톡방"], 0,
        "Slides & notices: 사이버캠퍼스(LMS), posted after each class 예요. 출석 체크도 사이버캠퍼스로 한다고 하셨어요."),
])

FIG_SCORE = SVG(
    TX(240, 40, "성적 100점 나누기", "tb", 16),
    R(40, 80, 20, 60, "n"), TX(50, 70, "출석 5", "t", 14),
    R(60, 80, 160, 60, "n3"), TX(140, 116, "과제 40", "tl", 15),
    R(220, 80, 100, 60, "n2"), TX(270, 116, "팀 25", "tl", 15),
    R(320, 80, 120, 60, "n2"), TX(380, 116, "기말 30", "tl", 15),
    L(220, 165, 440, 165, "e2", 1), L(220, 155, 220, 165, "e2", 1), L(440, 155, 440, 165, "e2", 1),
    TX(330, 192, "텀 프로젝트 + 기말 = 55", "tb", 15, "middle", 1),
    TX(240, 240, "중간고사는 없어요", "tm", 14, "middle", 1),
)

assert 5 + 40 + 25 + 30 == 100
assert 25 + 30 == 55 and 55 > 40

page(8, "1. Syllabus | Evaluation & Policies", E("pa", "tp", "torch", "tf", "rag", "agent", "chatgpt"), [
    say("성적은 출석 5, 과제 40, 텀 프로젝트 25, 기말고사 30 이에요.",
        "중간고사는 없어요."),
    fig("성적 막대", FIG_SCORE, "과제가 한 항목으로는 가장 크지만, 팀 프로젝트와 기말을 합치면 55로 더 커요.", 1),
], [
    cmp("네 칸, 우리말로", ["영어", "비율", "뜻"], [
        ["Attendance", "5%", "출석(2주차부터 체크)"],
        ["Programming assignments", "40%", f"{K('pa')}: 파이썬 코드 과제"],
        ["Term project", "25%", f"{K('tp')}: 팀 프로젝트, 8주 제안, 학기 말 결과와 보고서"],
        ["Final exam", "30%", "기말고사(16주)"],
    ]),
    pts("정책 문장 뜻",
        "**declare usage, write in your own words** = AI 도구를 썼으면 밝히고, 글은 자기 말로",
        "**start assignments early, ask questions earlier** = 과제는 일찍 시작하고, 질문은 더 일찍"),
    chk("한 항목으로 비중이 가장 큰 것은?", ["Programming assignments", "Final exam", "Term project"], 0,
        f"{K('pa')}가 40%로 가장 커요. 기말고사는 30%, 텀 프로젝트는 25%예요."),
], [
    look("슬라이드 짚어 읽기",
         bx(75, 162, 368, 305, "5% Attendance: 출석"),
         bx(401, 162, 695, 305, "40% Programming assignments: 프로그래밍 과제"),
         bx(728, 162, 1021, 305, "25% Term project: 텀 프로젝트(팀)"),
         bx(1054, 162, 1348, 305, "30% Final exam: 기말고사"),
         bx(100, 345, 1075, 405, f"과제 내용: {K('torch')}와 트랜스포머 구현, PEFT, RAG, 에이전트, 평가. 텀 프로젝트로 이어져요"),
         bx(100, 466, 1078, 498, f"AI 도구({K('chatgpt')}, Claude): 배우고 디버그하는 데 쓰되, 사용을 밝히고 자기 말로")),
    steps("비율 손계산", ["출석 5 + 과제 40 + 팀 25 + 기말 30 = 100", "팀 25 + 기말 30 = 55", "55 > 과제 40"],
          "합이 100이 맞고, 팀 프로젝트와 기말을 합친 55가 과제 40보다 커요."),
    prof("출석은 오늘은 없고 다음 주부터 해요.",
         "과제가 40%지만, 기말고사와 팀 프로젝트를 합친 55%가 더 크니 그쪽을 더 신경 써 주세요.",
         "ChatGPT, Claude 는 써도 되지만 썼다면 반드시 밝혀 주세요.",
         "통째로 AI 가 만든 걸 바로 내면 금방 티가 나요. 최대한 자기 언어로 쓰세요."),
    pts("그 밖의 안내", "장애학생 지원: 장애학생지원센터(02-2164-4699)", "텀 프로젝트: 8주차 제안 → 학기 말 최종 결과와 보고서"),
], [
    chk("기말고사와 텀 프로젝트 비중을 합치면?", ["55%", "40%", "70%"], 0, "30% + 25% = 55% 예요."),
    chk("AI 도구 정책으로 맞는 것은?", ["써도 되지만 사용을 밝히고 자기 말로 쓴다", "절대 쓰면 안 된다", "밝히지 않고 써도 된다"], 0,
        "AI tools: use them to learn and debug, declare usage, write in your own words 예요."),
    eng("평가 방식 한 줄", "평가는 출석 5%, 프로그래밍 과제 40%, 텀 프로젝트 25%, 기말고사 30%이며, 중간고사는 없고 8주차 텀 프로젝트 제안 발표로 대신한다.",
        "5, 40, 25, 30. 합 100.", "'오사이오 삼십' 처럼 5-40-25-30 순서로 소리 내 외워요."),
    warn("헷갈리기 쉬운 점", "한 항목으로는 과제(40%)가 가장 크지만, 교수님은 기말 + 팀(55%)을 더 신경 쓰라고 했어요."),
])

# ================= 2부: NLP 란 =================
page(9, "What is NLP? (구분)", E("nlp"), [
    say(f"2부: {K('nlp')}란 무엇인가.",
        "기계에게 사람 말을 읽고, 이해하고, 쓰게 가르치는 일이에요."),
])

FIG_NLU = SVG(
    R(10, 90, 120, 70, "n3"), TX(70, 122, "사람이 쓴 글", "tl", 15), TX(70, 146, "KTX 몇 시야?", "tl", 14),
    AR(132, 125, 178, 1), TX(155, 110, "NLU", "tb", 15, "middle", 1),
    R(180, 90, 120, 70, "n2", 1), TX(240, 122, "의미", "tl", 15, "middle", 1), TX(240, 146, "의도, 목적지, 날짜", "tl", 14, "middle", 1),
    AR(302, 125, 348, 2), TX(325, 110, "NLG", "tb", 15, "middle", 2),
    R(350, 90, 120, 70, "n", 2), TX(410, 122, "기계가 쓴 글", "tl", 15, "middle", 2), TX(410, 146, "첫 KTX 05:13", "tl", 14, "middle", 2),
    TX(155, 200, "이해: 글 → 뜻", "tm", 14, "middle", 1), TX(325, 225, "생성: 뜻 → 글", "tm", 14, "middle", 2),
)

page(10, "2. What is NLP? | Natural Language & NLP", E("nlp", "nlu", "nlg", "cls", "ner"), [
    say("자연어는 사람이 자라면서 자연스럽게 배우는 말이에요. 한국어, 영어처럼요.",
        "파이썬 같은 컴퓨터 언어는 자연어가 아니에요.",
        f"{K('nlp', '은')} 컴퓨터가 사람 말을 처리하고, 이해하고, 만들어 내게 하는 분야예요."),
    fig("두 방향, 한 분야", FIG_NLU, "글에서 뜻을 뽑는 쪽이 NLU, 뜻에서 글을 만드는 쪽이 NLG 예요.", 2),
], [
    cmp("NLU 와 NLG 구별", ["", K("nlu"), K("nlg")], [
        ["방향", "글 → 뜻 (in)", "뜻 → 글 (out)"],
        ["하는 일", "classify, extract, search, answer = 분류, 뽑기, 찾기, 답하기", "write, summarize, respond = 쓰기, 요약, 응답"],
        ["KTX 예", "의도 = 열차 시간표, 목적지 = 부산, 날짜 = 내일", "'내일 부산행 첫 KTX 는 05:13 입니다'"],
    ]),
    steps("KTX 질문이 처리되는 순서", [
        "사람이 씀: '내일 부산 가는 KTX 몇 시야?'",
        f"{K('nlu')}: 의도(Intent) = train_schedule, dest = 부산, date = 내일",
        f"{K('nlg')}: '내일 부산행 첫 KTX 는 05:13 입니다' 를 만들어요"],
        "NLU 로 뜻을 뽑고, NLG 로 답을 써요. 둘을 합친 것이 NLP 예요."),
    chk("'KTX 몇 시야?' 에서 목적지와 날짜를 뽑아내는 일은?", [K("nlu"), K("nlg")], 0,
        "글 → 뜻 방향이라 자연어 이해(NLU)예요."),
], [
    look("슬라이드 짚어 읽기",
         bx(100, 152, 1065, 187, "Natural language = 사람이 자라며 쓰는 말. not Python, not logic = 파이썬도 논리식도 아님"),
         bx(100, 198, 840, 232, "NLP: process, understand, and generate = 처리하고, 이해하고, 생성하기"),
         bx(68, 300, 372, 605, "TEXT, What people write: 사람이 쓴 질문"),
         bx(524, 300, 828, 605, "MEANING: Intent(의도), Entities(개체: 부산, 내일 같은 이름 붙은 것), Facts(사실)"),
         bx(988, 300, 1293, 605, "TEXT, What machines write: 기계가 쓴 답"),
         bx(280, 678, 1125, 708, "언어를 잘 다루는 기계는 똑똑해 보여요. 그래서 NLP 가 AI 의 한가운데 있어요")),
    pts("Entities 와 이어지는 용어",
        f"부산, 내일처럼 이름 붙은 것을 찾는 일을 {K('ner', '이라고')} 해요.",
        f"스팸인지 아닌지 가르는 일은 {K('cls')}예요. 둘 다 NLU 쪽 일이에요."),
    prof("자연어는 사람이 자라면서 자연스럽게 습득하는 언어로, 컴퓨터 언어와 대치되는 말이에요.",
         "파이썬이나 수학 기호처럼 사람이 설계한 언어는 문법이 명확해요. 자연어는 정반대예요.",
         "NLU 와 NLG 를 합쳐서 NLP 라고 해요."),
], [
    chk("NLP 와 NLU, NLG 의 관계로 맞는 것은?", ["NLP = NLU(이해) + NLG(생성)", "NLU = NLP + NLG", "NLG 는 NLP 와 관계없다"], 0,
        "Two directions, one field: 이해(NLU)가 들어가고 생성(NLG)이 나와요."),
    eng("NLP 정의", "자연어처리(NLP)는 컴퓨터가 사람의 언어를 처리, 이해, 생성하게 만드는 분야로, 글에서 의미를 뽑는 자연어 이해(NLU)와 의미에서 글을 만드는 자연어 생성(NLG)의 두 방향으로 이루어진다.",
        "처리, 이해, 생성 + NLU(in), NLG(out)", "U 는 Understanding(이해), G 는 Generation(생성)."),
    warn("헷갈리기 쉬운 점", "파이썬은 자연어가 아니에요. 사람이 설계한 인공 언어예요(not Python, not logic)."),
])

page(11, "2. What is NLP? | NLP Is Already Everywhere", E("nlp", "lm", "cls", "mt", "llm", "chatgpt"), [
    say(f"오늘 하루에도 {K('nlp', '을')} 열 번 넘게 썼어요.",
        "자판 자동 완성, 검색, 스팸 필터, 번역, 음성 비서, 챗봇 전부 NLP 예요."),
    ana("휴대폰 자판의 다음 단어 추천", "문자를 치다 보면 자판이 다음 단어를 미리 띄워 줘요. 앞 글을 보고 다음에 올 말을 맞히는 거예요.",
        [["자판의 다음 단어 추천", K("lm")], ["추천이 맞는지", "다음 토큰 맞히기"]]),
], [
    cmp("하루 시간표 속 NLP", ["시각", "장면", "NLP 속 이름"], [
        ["07:30", "자판 자동 완성, 오타 수정", K("lm")],
        ["08:10", "구글, 네이버 검색", "질의 이해, 순위, 요약 문장"],
        ["10:00", "스팸 메일 40통 삭제", f"텍스트 {K('cls')}기"],
        ["13:20", "파파고로 외국 메뉴 번역", f"신경망 {K('mt')}"],
        ["19:00", "'시리야', '헤이 구글'", "말 → 글 바꾼 뒤 NLP 가 뜻 파악"],
        ["23:00", f"{K('chatgpt')}, Claude 로 과제 도움", f"{K('llm')} (쓰면 밝히기)"],
    ]),
    chk("스팸 필터는 어떤 일을 하는 NLP 인가요?", [K("cls"), K("mt"), "음성 합성"], 0,
        "a text classifier at work: 글을 '스팸/정상' 라벨로 나누는 분류기예요."),
], [
    look("슬라이드 짚어 읽기",
         bx(100, 152, 890, 186, "07:30 자판이 다 치기 전에 자동 완성하고 오타를 고쳐요"),
         bx(100, 203, 1010, 237, "08:10 검색이 질문을 알아듣고 페이지 순위를 매기고 요약을 써요"),
         bx(100, 254, 895, 288, "10:00 스팸 필터: a text classifier at work"),
         bx(100, 306, 930, 340, "13:20 파파고: neural machine translation in your pocket"),
         bx(100, 357, 1220, 391, "19:00 음성 비서: speech becomes text, then NLP figures out what you meant"),
         bx(100, 408, 1040, 442, "23:00 ChatGPT / Claude: a large language model (declare it!)")),
    prof("5년 전쯤만 해도 먼 기술 같았는데, 지금 여러분은 매일 NLP 를 맞닥뜨려요.",
         "이 수업은 자연어처리가 어떻게 이루어지는지, 그 블랙박스를 열어 보는 수업이에요."),
], [
    chk("파파고 번역은 슬라이드에서 무엇이라고 불렀나요?", ["neural machine translation", "text classifier", "spam filter"], 0,
        f"신경망 {K('mt')}, 주머니 속 번역기예요."),
    warn("헷갈리기 쉬운 점", "(declare it!) 과제에 LLM 을 썼으면 밝혀야 해요. p.8 AI 도구 정책과 같은 말이에요."),
])

page(12, "2. What is NLP? | Why Is Language Hard? - Ambiguity", E("amb", "nlp"), [
    say(f"같은 글자가 여러 뜻을 가질 수 있어요. 이게 {K('amb')}이에요.".replace("이에요.", "이에요."),
        "'배' 는 먹는 배일까요, 타는 배일까요, 몸의 배일까요?",
        "사람은 눈치로 바로 알지만, 기계는 글자만 보고는 몰라요."),
], [
    cmp("중의성의 세 수준", ["수준", "예", "헷갈리는 점"], [
        ["Word level (단어)", "배, bank", "배 = 과일/탈것/신체, bank = 강둑/은행"],
        ["Structure level (구조)", "I saw a man with a telescope", "망원경을 든 사람이 누구?"],
        ["Spacing (띄어쓰기)", "아버지가방에들어가신다", "아버지가 방에 vs 아버지 가방에"],
    ]),
    pts("슬라이드 문장 뜻",
        "**humans disambiguate without noticing** = 사람은 모르는 사이에 중의성을 풀어요",
        f"**Ambiguity is THE core difficulty of NLP** = {K('amb', '이')} NLP 의 가장 핵심 난제예요",
        "**every era is a new answer to it** = 역사의 모든 시대가 이 문제에 대한 새 답이에요"),
    chk("'bank' 가 강둑도 되고 은행도 되는 것은 어느 수준의 중의성?", ["단어 수준", "구조 수준", "띄어쓰기"], 0,
        "한 단어가 여러 뜻을 가지니 Word level 이에요."),
], [
    look("슬라이드 짚어 읽기",
         bx(100, 152, 975, 187, "같은 문자열이 여러 뜻, 사람은 without noticing 풀어요"),
         bx(100, 195, 1005, 228, "Word level: 배(pear, boat, stomach), bank(river bank, money bank)"),
         bx(100, 237, 875, 270, "Structure level: I saw a man with a telescope"),
         bx(100, 279, 865, 312, "Spacing too: 아버지가 방에 vs 아버지 가방에"),
         bx(145, 370, 685, 610, "Reading 1: with a telescope 가 동사 saw 에 붙음 → 내가 망원경으로 봤어요"),
         bx(728, 370, 1265, 610, "Reading 2: with a telescope 가 명사 a man 에 붙음 → 그 남자가 망원경을 들고 있어요")),
    prof("같은 문자열이 여러 의미를 가질 수 있다는 게 중의성이에요.",
         "사람은 맥락(context) 속에서 무의식적으로 해소하지만, 기계는 이렇게만 봐서는 해소가 안 돼요.",
         "중의성이 NLP 의 원래 핵심 난제였고, 70년 역사는 각 시대 천재들의 답변 흐름이에요."),
], [
    chk("'I saw a man with a telescope' 는 어떤 중의성?", ["구조 수준", "단어 수준", "띄어쓰기"], 0,
        "with a telescope 가 saw 에 붙는지 a man 에 붙는지, 문장 구조가 두 가지로 읽혀요."),
    eng("중의성 정의", "중의성(Ambiguity)은 같은 문자열이 여러 의미로 해석될 수 있는 성질로, NLP의 핵심 난제다. 단어 수준(배, bank), 구조 수준(I saw a man with a telescope), 띄어쓰기(아버지가방에들어가신다)의 예가 있다.",
        "정의 한 줄 + 예 세 개", "단어, 구조, 띄어쓰기. '배, 망원경, 아버지 가방' 으로 외워요."),
    warn("헷갈리기 쉬운 점", "중의성은 한 시대의 문제가 아니에요. p.24 에서 '모든 막이 중의성에 대한 새 답' 이라고 다시 나와요."),
])

page(13, "2. What is NLP? | Why Is Language Hard? - Part 2", E("ref", "wino", "prag", "ellip", "lowres", "amb"), [
    say("말을 이해하려면 글자만으로는 부족해요.",
        "앞뒤 맥락과 세상에 대한 상식(세상 지식)이 있어야 해요."),
], [
    cmp("어려움 다섯 가지", ["이름", "예", "왜 어려운가"], [
        [K("ref"), "The trophy didn't fit in the suitcase because it was too big.", "it 이 무엇인지 세상 지식으로 풀어야 해요"],
        [K("prag"), "'잘~한다'", "칭찬일까, 비꼼일까? 같은 말, 반대 뜻"],
        [K("ellip"), "'밥 먹었어?'", "주어도 목적어도 없어요. 한국어는 맥락이 주는 건 빼요"],
        ["변하는 언어", "갓생, 억텐", "신조어가 매달 생기고 모델이 따라가야 해요"],
        [K("lowres"), "지구의 7,000개 넘는 언어", "대부분 데이터가 거의 없어요"],
    ]),
    chk("'잘~한다' 가 칭찬인지 비꼼인지 가리는 문제는?", [K("prag"), K("ellip"), K("ref")], 0,
        "같은 말이 상황에 따라 반대 뜻이 되는 건 화용론(Pragmatics) 문제예요."),
], [
    look("슬라이드 짚어 읽기",
         bx(100, 152, 1000, 220, f"Reference: it 은 무엇? big → small 로 바꾸면 답이 뒤집혀요. {K('wino')} 모양"),
         bx(100, 235, 935, 268, "Pragmatics: praise or sarcasm = 칭찬 또는 비꼼"),
         bx(100, 285, 1003, 318, "Ellipsis: no subject, no object = 주어도 목적어도 없음"),
         bx(100, 335, 1072, 368, "Language never sits still: 신조어가 매달, 모델은 따라가야"),
         bx(100, 385, 870, 418, "7,000+ languages: 대부분 데이터가 거의 없음(low-resource NLP)"),
         bx(270, 678, 1135, 708, "언어 이해에는 맥락과 세상 지식이 필요, 페이지 위 단어만으로는 안 돼요")),
    steps("트로피 문장 풀어 보기", [
        "'트로피가 여행 가방에 안 들어갔다, 그것이 너무 커서' → 그것 = 트로피",
        "big 을 small 로: '그것이 너무 작아서' → 그것 = 여행 가방",
        "단어 하나 바뀌었는데 지시 대상이 뒤집혀요",
        "'큰 것은 안 들어가고, 작은 가방엔 안 들어간다' 는 세상 지식이 있어야 풀려요"],
        f"이런 모양의 문제를 {K('wino', '이라고')} 불러요."),
    prof("이걸 풀려면 문법만 필요한 게 아니라 세상 지식이 필요해요.",
         "한국어는 특히 생략이 심해요. '밥 먹었어?' 에는 주어도 목적어도 없어요.",
         "7천 개가 넘는 언어가 다 데이터가 많지 않아서, 저자원 NLP 라는 연구 분야가 따로 있어요."),
], [
    chk("'The trophy didn't fit in the suitcase because it was too small.' 에서 it 은?", ["the suitcase (여행 가방)", "the trophy (트로피)", "알 수 없다"], 0,
        "작아서 안 들어간 것은 가방이에요. big 일 때는 트로피예요."),
    eng("언어 이해에 필요한 것", "언어를 이해하려면 단어뿐 아니라 맥락과 세상 지식이 필요하다. 예: 지시 대상(Reference, 트로피와 가방), 화용론(Pragmatics, 잘~한다), 생략(Ellipsis, 밥 먹었어?), 신조어, 저자원 언어(Low-resource NLP).",
        "맥락 + 세상 지식", "'지시, 화용, 생략, 신조어, 저자원' 다섯 개."),
    warn("헷갈리기 쉬운 점", f"{K('wino')}는 big/small 한 단어로 it 이 가리키는 대상이 바뀌는 문장 모양이에요. 문법이 아니라 세상 지식 테스트예요."),
])

FIG_MORPH = SVG(
    TX(240, 36, "한국어는 조각을 붙여 한 단어", "tb", 16),
    R(40, 60, 80, 44, "n3"), TX(80, 88, "먹-", "tl", 16),
    R(150, 60, 80, 44, "n3"), TX(190, 88, "-었-", "tl", 16),
    R(260, 60, 80, 44, "n3"), TX(300, 88, "-겠-", "tl", 16),
    R(370, 60, 80, 44, "n3"), TX(410, 88, "-더라", "tl", 16),
    TX(135, 88, "+", "tb", 16), TX(245, 88, "+", "tb", 16), TX(355, 88, "+", "tb", 16),
    L(240, 110, 240, 150, "e2", 1), f'<polygon points="240,160 235,150 245,150" class="arrow b1"/>',
    R(160, 165, 160, 50, "n2", 1), TX(240, 197, "먹었겠더라", "tl", 18, "middle", 1),
    TX(240, 245, "형태소 4개 → 한 단어", "tm", 14, "middle", 1),
)

page(14, "2. What is NLP? | Korean NLP Has Its Own Challenges", E("aggl", "morph", "manal", "hon", "ellip", "llm", "exaone"), [
    say(f"한국어는 {K('aggl')}예요.",
        "어간에 작은 조각을 착착 붙여 한 단어를 만들어요."),
    fig("먹었겠더라 만들기", FIG_MORPH, "뜻을 가진 작은 조각(형태소) 네 개가 붙어 한 단어가 돼요.", 1),
], [
    pts("슬라이드 문장 뜻",
        "**Korean is agglutinative** = 한국어는 교착어예요",
        f"**one word, many morphemes** = 한 단어 안에 {K('morph')}가 여러 개",
        "**morphological analysis matters** = 형태소 분석이 중요해요",
        "**Korean needs native attention** = 한국어는 한국어에 맞춘 관심이 필요해요"),
    cmp("한국어가 어려운 네 가지", ["어려움", "예"], [
        [K("aggl"), "먹- + -었- + -겠- + -더라 → 먹었겠더라"],
        ["띄어쓰기가 들쭉날쭉", "아버지가방에... 띄어쓰기가 뜻을 바꿔요"],
        [K("hon"), "먹어 / 드세요 / 잡수세요: 같은 사실, 다른 사회적 뜻"],
        ["어순 자유, 주어 자주 생략", "모델이 먼저 보는 영어와 달라요"],
    ]),
    chk("'먹었겠더라' 는 형태소 몇 개가 붙은 단어인가요?", ["4개", "2개", "1개"], 0, "먹-, -었-, -겠-, -더라 네 개예요."),
], [
    look("슬라이드 짚어 읽기",
         bx(100, 152, 1105, 186, f"{K('aggl')}: 먹- + -었- + -겠- + -더라 → 먹었겠더라"),
         bx(100, 190, 1025, 220, "영어 단어는 형태가 몇 개, 한국어 동사는 수천 개 → 형태소 분석이 중요"),
         bx(100, 235, 1025, 268, "Spacing is unreliable: 실제 글의 띄어쓰기는 믿기 어렵고, 뜻도 바꿔요"),
         bx(100, 285, 890, 318, f"{K('hon')}: 먹어 / 드세요 / 잡수세요"),
         bx(100, 335, 1060, 368, "어순이 자유롭고 주어를 자주 빼요"),
         bx(268, 678, 1138, 708, f"한국어 LLM({K('exaone')}, HyperCLOVA X)이 따로 있는 이유")),
    pts("형태소 분석을 누가 하나",
        f"단어를 {K('morph')}로 쪼개는 도구가 {K('manal')}예요.",
        "2주차 토큰화 시간에 한국어를 어떻게 자르는지 다시 만나요."),
    warn("헷갈리기 쉬운 점", f"{K('morph')}는 조각, {K('manal')}는 그 조각으로 쪼개 주는 도구예요."),
    prof("영어는 굴절어라고 하고, 한국어는 교착어예요.",
         "영어 동사는 변화형이 많지 않은데, 한국어 동사는 수천 가지 형태가 가능해서 형태소 분석이 중요해요. 2주차에 해 볼 예정이에요.",
         "대부분 모델은 영어부터 배우는데 한국어는 구조가 많이 달라요.",
         "그래서 네이버 하이퍼클로바, LG 엑사원 같은 한국어 LLM 이 따로 있었어요."),
], [
    chk("'먹어 / 드세요 / 잡수세요' 가 보여 주는 한국어 특징은?", [K("hon"), K("aggl"), "띄어쓰기"], 0,
        "같은 사실을 말하지만 사회적 뜻(높임)이 달라요."),
    eng("한국어 NLP 의 어려움", "한국어는 교착어라 한 단어에 형태소가 여럿 붙으므로(먹었겠더라) 형태소 분석이 중요하다. 또 띄어쓰기가 불규칙하고, 높임법이 있고, 주어를 자주 뺀다.",
        "교착어, 띄어쓰기, 높임법, 어순과 생략", "'붙이고, 띄우고, 높이고, 빼고' 네 동작으로 외워요."),
    warn("헷갈리기 쉬운 점", "교착어(한국어)의 짝은 굴절어(영어)예요. '굴절어' 는 슬라이드가 아니라 교수님 설명에 나온 말이에요."),
])

page(15, "2. What is NLP? | The NLP Task Landscape", E("cls", "senti", "seqlab", "pos", "ner", "mt", "llm", "token"), [
    say("NLP 로 하는 일은 크게 다섯 가지 모양이에요.",
        f"요즘은 {K('llm')} 하나가 프롬프트 한 번으로 이걸 다 해요."),
], [
    cmp("다섯 가지 태스크", ["태스크", "예", "입력 → 출력"], [
        [K("cls"), f"스팸, {K('senti')}, 주제", "글 → 라벨 하나"],
        [K("seqlab"), f"{K('pos')}, {K('ner')}", f"{K('token')}마다 → 태그 하나"],
        ["Text-to-text", f"{K('mt')}, 요약", "글 → 새 글"],
        ["Retrieval & QA", "맞는 문서 찾기, 답 뽑거나 쓰기", "질문 → 문서 → 답"],
        ["Dialogue & generation", "챗봇, 글쓰기 도우미", "맥락 → 응답"],
    ]),
    chk("글 전체에 라벨 하나를 붙이는 태스크는?", [K("cls"), K("seqlab"), "Text-to-text"], 0, "text → label 이에요."),
], [
    look("슬라이드 짚어 읽기",
         bx(100, 152, 655, 186, "Classification: spam, sentiment, topic, text → label"),
         bx(100, 202, 865, 236, "Sequence labeling: part-of-speech, named entities, every token → a tag"),
         bx(100, 252, 718, 286, "Text-to-text: translation, summarization, text → new text"),
         bx(100, 301, 915, 335, "Retrieval & QA: 맞는 문서를 찾고 답을 뽑거나 지어요"),
         bx(100, 351, 872, 385, "Dialogue & generation: context → response"),
         bx(100, 406, 805, 440, "2026 twist: LLM 하나가 프롬프트 한 번으로 전부")),
    prof("예전엔 태스크마다 모델을 따로 만들었는데, LLM 시대엔 프롬프트 하나로 '딸깍' 하면 다 돼요.",
         "그럼 왜 NLP 를 배우나? 엔지니어는 시스템을 만들고, 평가하고, 고장 나면 고치는 사람이에요.",
         "그러려면 NLP 와 LLM 이 어떻게 동작하고 뭐가 문제인지 알아야 해요. 그걸 위해 이 수업이 있어요."),
], [
    chk(f"문장 속 {K('token')}마다 품사를 붙이는 일은?", [K("seqlab"), K("cls"), "Text-to-text"], 0,
        "every token → a tag 가 시퀀스 레이블링이에요. 품사 태깅, 개체명 인식이 여기에 들어가요."),
    chk("번역과 요약은 어떤 모양?", ["Text-to-text", "Classification", "Sequence labeling"], 0, "text → new text 예요."),
    eng("NLP 태스크 지도", "NLP 태스크는 분류(글 → 라벨), 시퀀스 레이블링(토큰마다 태그: 품사, 개체명), 텍스트-투-텍스트(번역, 요약), 검색과 질의응답, 대화와 생성으로 나뉘며, 지금은 LLM 하나가 프롬프트로 모두 수행한다.",
        "입력 → 출력 모양으로 구별", "라벨 하나, 태그 여러 개, 새 글, 찾아서 답, 응답."),
    warn("헷갈리기 쉬운 점", "LLM 이 다 해 줘도 '부품을 아는 엔지니어가 전체를 만들고, 평가하고, 고쳐요' 가 슬라이드 결론이에요."),
])

# ================= 3부: 역사 =================
page(16, "A Brief History of NLP (구분)", E("nlp", "rule", "stat", "nn", "pre", "llm"), [
    say(f"3부: {K('nlp')} 70년 역사, 다섯 막이에요.",
        "규칙 → 통계 → 신경망 → 사전 학습 → LLM",
        "이 레슨에서는 여섯 계단 주문으로 외워요.",
        HIST),
    tl_fig(None, ""),
])

page(17, "3. History of NLP | The Very Beginning (1947-1956)", E("mt", "turing", "gib", "dart", "ai", "nlp"), [
    say("NLP 이야기는 2차 대전 직후 암호 해독에서 시작해요.",
        "다른 나라 말을 '이상한 기호로 적힌 암호' 처럼 보고 풀려고 했어요.",
        "역사 주문: " + HIST),
], [
    steps("시작 네 장면 (1947 → 1956)", [
        f"1947 워런 위버(Warren Weaver): 번역 = 암호 풀기. {K('mt')}의 출발점",
        f"1950 앨런 튜링(Alan Turing): '기계가 생각할 수 있나?' → 대화로 지능을 시험, {K('turing')}",
        f"1954 {K('gib')}: 러시아어 60문장 → 영어",
        f"1956 {K('dart')}: 이 분야 이름 {K('ai', '이')} 생겨요"],
        "암호 해독 → 대화 시험 → 번역 시연 → 인공지능이라는 이름."),
    pts("슬라이드 영어 뜻",
        "**This is really written in English, but coded in strange symbols** = 사실 영어로 쓰였는데 이상한 기호로 암호화됐을 뿐",
        "**machine translation imagined as code-breaking** = 기계 번역을 암호 풀기로 상상",
        "**conversation becomes the test of intelligence** = 대화가 지능의 시험이 돼요",
        "**solved within 5 years (...not quite)** = 5년 안에 해결(...은 아니었죠)"),
    chk("1947년 워런 위버는 번역을 무엇처럼 생각했나요?", ["암호 풀기", "그림 그리기", "계산기 두드리기"], 0,
        "machine translation imagined as code-breaking 이에요."),
], [
    look("슬라이드 짚어 읽기",
         bx(100, 152, 893, 215, "1947 Warren Weaver: 암호 풀기로서의 기계 번역"),
         bx(100, 225, 965, 258, f"1950 Alan Turing, 'Can machines think?': {K('turing')}"),
         bx(100, 267, 1090, 300, "1954 Georgetown-IBM demo: 60 Russian sentences → English, '5년 안에 해결'"),
         bx(100, 309, 910, 342, f"1956 Dartmouth summer workshop: 이름이 {K('ai', '으로')}"),
         bx(213, 388, 596, 645, "1954 뉴스 영상: 'ELECTRONIC BRAIN Translates RUSSIAN to ENGLISH'"),
         bx(720, 388, 1043, 645, "1956 다트머스 워크숍 사람들. 맨 오른쪽이 섀넌(Shannon)")),
    cmp("연도, 사람, 기억할 말", ["연도", "누가 / 무엇", "기억할 말"], [
        ["1947", "Warren Weaver", "번역 = 암호 해독"],
        ["1950", "Alan Turing", "Can machines think? 대화 = 지능 시험"],
        ["1954", "Georgetown-IBM 시연", "러시아어 60문장, 5년 장담"],
        ["1956", "Dartmouth 워크숍", "Artificial Intelligence 라는 이름"],
    ]),
    prof("2차 대전 때 암호 해독에 많은 수학자가 활약했어요. 47년 워런 위버가 러시아어는 이상한 기호로 암호화된 영어라고 했어요.",
         "튜링 테스트도 사람과의 대화로 지능을 평가하니, 이것도 자연어처리에 대한 평가예요.",
         "54년 연구자들은 5년이면 번역이 다 풀린다고 장담했지만, 70년 지난 지금도 번역은 완벽하지 않아요.",
         "다트머스 사진 맨 오른쪽이 섀넌이에요. 뒤(2막)에서 다시 나와요."),
], [
    chk("1954년 조지타운-IBM 시연에서 번역한 것은?", ["러시아어 60문장을 영어로", "영어 60문장을 프랑스어로", "러시아어 600문장을 영어로"], 0,
        f"{K('gib')}: 60 Russian sentences → English 예요."),
    chk("'Artificial Intelligence' 라는 이름이 생긴 사건은?", ["1956 다트머스 워크숍", "1950 튜링의 논문", "1966 ALPAC 보고서"], 0,
        f"1956 {K('dart')}에서 이 분야가 이름을 얻었어요."),
    eng("시작 네 장면", "1947 위버(번역 = 암호 해독), 1950 튜링(Can machines think?, 튜링 테스트), 1954 조지타운-IBM 시연(러시아어 60문장 → 영어), 1956 다트머스 워크숍(인공지능이라는 이름).",
        "47, 50, 54, 56", "'암호, 대화, 번역, 이름' 순서예요."),
    warn("헷갈리기 쉬운 점", "'5년 안에 해결' 장담은 틀렸어요(not quite). 연도는 47 → 50 → 54 → 56 오름차순."),
])

page(18, "3. History of NLP | Act 1 - Rules (1950s-1980s)", E("rule", "eliza", "alpac", "mt", "ai"), [
    say(f"1막은 {K('rule')}이에요.",
        "사람이 '이런 말이 오면 이렇게 답해' 라는 규칙을 손으로 써요.",
        "하지만 말은 너무 다양해서 규칙집은 끝없이 늘어나고, 그래도 깨져요."),
    tl_fig(0, "1막, 규칙"),
], [
    pts("슬라이드 영어 뜻",
        "**the first chatbot** = 최초의 챗봇",
        "**~200 pattern-matching rules playing a psychotherapist** = 약 200개 패턴 규칙으로 심리 상담사 흉내",
        "**MT far harder than promised** = 기계 번역은 약속보다 훨씬 어려웠다",
        "**you cannot write language down by hand** = 언어를 손으로 다 적을 수는 없다"),
    steps(f"{K('eliza')}의 비밀(the whole trick)", [
        "YOU: Men are all alike. → ELIZA: IN WHAT WAY",
        "키워드 찾기(keyword spotting): 'alike' 가 보이면 정해진 답 'IN WHAT WAY'",
        "되돌려 주기(reflection template): my ___ → YOUR ___",
        "규칙 약 200개, 뜻도 기억도 없음(no meaning, no memory)"],
        "그런데도 사람들은 ELIZA 에게 속마음을 털어놨어요."),
    chk(f"{K('eliza')}는 문장의 뜻을 이해했나요?", ["아니요, 패턴 규칙으로 답했을 뿐이에요", "네, 뜻을 이해했어요"], 0,
        "~200 rules, no meaning, no memory 예요."),
], [
    look("슬라이드 짚어 읽기",
         bx(100, 152, 985, 186, f"1966 {K('eliza')} (MIT): 최초의 챗봇, 약 200개 패턴 규칙"),
         bx(100, 195, 902, 228, f"1966 {K('alpac')}: 기계 번역이 훨씬 어렵다, 미국 지원 10년 동결"),
         bx(100, 237, 1140, 270, "1970s~80s: 손으로 만든 문법과 지식 체계(SHRDLU, unification grammars)"),
         bx(140, 342, 813, 628, "ELIZA 대화: Well, my boyfriend made me come here. → YOUR BOYFRIEND MADE YOU COME HERE"),
         bx(848, 362, 1275, 597, "the whole trick: 키워드, 되돌려 주기, 규칙 200개, 그래도 사람들이 털어놓음"),
         bx(250, 682, 1156, 710, "1막의 교훈: 규칙집은 끝없이 자라고 그래도 깨져요")),
    cmp("1막 연표", ["연도", "이름", "무엇", "결과"], [
        ["1966", "ELIZA (MIT)", "패턴 규칙 약 200개 챗봇, 심리 상담사 역할", "사람들이 진지하게 고민을 털어놓음"],
        ["1966", "ALPAC report", "기계 번역 평가 보고서", "미국 연구 지원 10년 동결"],
        ["1970s~80s", "SHRDLU, unification grammars", "손으로 만든 문법과 지식 체계", "점점 더 형식적, 그래도 한계"],
    ]),
    prof("신기하게도 사람들이 엘리자에게 굉장히 진지하게 고민을 털어놨대요.",
         "연구자에겐 정부 과제 펀딩이 가장 중요한데, ALPAC 보고서로 미국 정부 펀딩이 10년 동안 끊겨 거의 AI 겨울이 왔어요.",
         "언어는 살아 있어서 규칙집은 끊임없이 자라고, 예외는 항상 더 많아요. 그래서 규칙의 시대는 저물어요."),
], [
    chk("1966년 ALPAC 보고서의 결과는?", ["미국의 기계 번역 연구 지원이 약 10년 동결", "최초의 챗봇 탄생", "Transformer 발표"], 0,
        "MT far harder than promised, US funding frozen for a decade 예요."),
    chk(f"{K('eliza')}가 쓴 규칙은 약 몇 개?", ["약 200개", "약 2개", "약 200만 개"], 0, "~200 pattern-matching rules 예요."),
    eng("1막 요약", "1막 규칙(1950s~80s): 1966 ELIZA(규칙 약 200개 챗봇), 1966 ALPAC 보고서(지원 10년 동결), 70~80년대 SHRDLU. 교훈: 언어는 손으로 다 못 적는다.",
        "1966 두 개 + 70~80년대 문법", "ELIZA 와 ALPAC 은 같은 해 1966."),
    warn("헷갈리기 쉬운 점", "ELIZA 와 ALPAC 은 둘 다 1966년이에요.", "ELIZA 는 이해가 아니라 흉내예요. '사람들이 믿었다' 와 '이해했다' 는 달라요."),
])

from fractions import Fraction
TOY = ["나는 밥을 먹었다", "나는 밥을 샀다", "나는 빵을 먹었다"]
_after = [s.split()[1] for s in TOY if s.split()[0] == "나는"]
assert Fraction(_after.count("밥을"), len(_after)) == Fraction(2, 3)

page(19, "3. History of NLP | Act 2 - Statistics (1990s-2000s)", E("stat", "noisy", "corpus", "ngram", "lm", "mt", "pos"), [
    say(f"2막은 {K('stat')}이에요.",
        f"규칙을 쓰지 말고, 아주 많은 글({K('corpus')})에서 패턴을 세요."),
    ana("바로 앞 몇 단어만 보고 맞히기", "'나는 밥을' 다음에 올 말을 맞힐 때, 많은 글에서 '나는 밥을' 뒤에 무엇이 자주 왔는지 세어 봐요.",
        [["바로 앞 몇 단어", K("ngram")], ["다음 말 맞히기", K("lm")], ["많이 세어 본 글", K("corpus")]]),
    tl_fig(1, "2막, 통계"),
], [
    pts("슬라이드 영어 뜻",
        "**communication as probability** = 통신을 확률로 보기",
        "**Stop writing rules, count patterns in large corpora** = 규칙 그만 쓰고 큰 말뭉치에서 패턴을 세라",
        "**Every time I fire a linguist, the performance goes up** = 언어학자를 해고할 때마다 성능이 오른다",
        "**counts cannot see that cat and kitten are related** = 세기만 해서는 cat 과 kitten 이 비슷한 줄 몰라요"),
    steps("2막의 흐름", [
        f"뿌리: 1948 섀넌(Shannon)의 {K('noisy')}, 정보 이론",
        f"방법: 말뭉치에서 세기, {K('ngram')} LM = P(다음 단어 | 앞 단어들)",
        "IBM: 의회 회의록 수백만 문장 쌍으로 프랑스어-영어 번역을 배움",
        "성과: 스팸 필터, 품사 태거, 음성 인식, 검색",
        "벽: 뜻(meaning)이라는 개념이 없음"],
        "데이터가 규칙을 이겼지만, 단어를 세는 것은 이해가 아니었어요."),
    chk("2막(통계)이 부딪힌 벽은?", ["cat 과 kitten 이 비슷하다는 걸 모름", "규칙이 너무 적음", "GPU 가 없음"], 0,
        "counts cannot see that 'cat' and 'kitten' are related, no notion of meaning 이에요."),
], [
    look("슬라이드 짚어 읽기",
         bx(100, 152, 1108, 186, f"뿌리: Shannon 1948, {K('noisy')}(정보 이론)"),
         bx(100, 192, 1040, 226, "count patterns in large corpora: n-gram LM = P(next word | previous words)"),
         bx(100, 232, 920, 297, "IBM 의 프랑스어-영어 통계 번역, Jelinek 의 악명 높은 한마디"),
         bx(100, 305, 1095, 370, "스팸 필터, POS 태거, 음성 인식, 검색으로 조용히 퍼짐. 벽: 뜻 개념 없음"),
         bx(435, 450, 962, 640, "잡음 채널: 정보원 → 송신기 → (잡음) → 수신기 → 목적지"),
         bx(328, 686, 1078, 714, "2막의 교훈: 데이터가 규칙을 이긴다, 하지만 세기는 이해가 아니다")),
    formula(f"{K('ngram')} 언어 모델", r"P(\text{next word} \mid \text{previous words})",
            [(r"P(\cdot)", "확률, 0~1 사이 숫자"), (r"\text{next word}", "다음에 올 단어"), (r"\mid", "'~이 주어졌을 때'"), (r"\text{previous words}", "바로 앞 단어 몇 개")],
            "앞 단어 몇 개를 보고 다음 단어가 나올 확률을 세어서 정해요."),
    steps("아주 작은 말뭉치로 세어 보기", [
        "말뭉치 3문장: '나는 밥을 먹었다', '나는 밥을 샀다', '나는 빵을 먹었다'",
        "'나는' 다음 단어: 밥을, 밥을, 빵을 (3번)",
        "그중 '밥을' 은 2번",
        "P(밥을 | 나는) = 2 / 3"],
        "P(밥을 | 나는) = 2/3, 약 0.67 이에요. 이것이 2-gram 세기예요.", "연습용으로 만든 예예요."),
    bg("기초 다지기 5단원", "P(A | B) 는 'B 가 주어졌을 때 A 의 확률' 이에요.", "빈도로 세어서 확률을 구하는 법은 기초 다지기 5단원에 있어요."),
    prof("n-gram 은 n 개씩 붙어 있는 단어 묶음이에요. 1-gram 은 단어 하나, 2-gram 은 두 단어예요.",
         "n-gram 으로 빈도를 세서 확률을 구하는 건 3주차에 직접 만들어 볼게요.",
         "IBM 은 불어와 영어를 같이 쓰는 캐나다 의회 회의록으로 번역을 학습시켰어요.",
         "통계에는 벽이 있어요. cat 과 kitty 가 비슷한 말이라는 개념 자체가 없어요."),
], [
    chk("2막의 뿌리가 된 섀넌(1948)의 아이디어는?", [K("noisy"), "최초의 챗봇", "단어 벡터"], 0,
        "communication as probability, the noisy channel model 이에요. 통계 번역과 음성 인식의 설계도예요."),
    chk("Jelinek 의 말 'Every time I fire a linguist, the performance goes up' 이 뜻하는 것은?",
        ["사람이 쓴 규칙보다 데이터 통계가 더 잘 된다", "언어학자가 꼭 필요하다", "규칙을 더 많이 써야 한다"], 0,
        "통계 시대의 분위기(데이터가 규칙을 이긴다)를 보여 주는 악명 높은 말이에요."),
    eng("2막 요약", "2막 통계(1990s~2000s): 섀넌(1948) 잡음 채널이 뿌리, 말뭉치에서 세는 n-gram LM 과 IBM 통계 번역. 한계: 뜻을 모른다(cat, kitten).",
        "섀넌 1948 + 세기 + IBM + 벽", "교훈: data beats rules, but counting is not understanding."),
    warn("헷갈리기 쉬운 점", "섀넌 1948 은 2막의 '뿌리' 예요. 2막 자체는 1990s~2000s 예요.", "1956 다트머스 사진 맨 오른쪽의 그 섀넌이에요."),
])

page(20, "3. History of NLP | Act 3 - word2vec (2013)", E("w2v", "wv", "dh", "stat"), [
    say(f"3막의 첫 장면은 {K('w2v')}(2013)이에요.",
        "모든 단어를 숫자 목록(벡터), 곧 지도 위 좌표로 바꿔요."),
    ana("단어의 지도 좌표", "뜻이 비슷한 단어는 지도에서 가까이 살아요. 개, 고양이는 동물 동네에, 피자, 김치는 음식 동네에 모여요.",
        [["지도 위 좌표", K("wv")], ["가까이 사는 이웃", "뜻이 비슷한 단어"]]),
    ana("친구를 보면 그 사람을 안다", "어떤 단어 옆에 늘 어떤 단어들이 오는지 보면, 그 단어의 뜻을 짐작할 수 있어요.",
        [["친구들", "주변 단어(문맥)"], ["그 사람을 안다", K("dh")]]),
], [
    pts("슬라이드 영어 뜻",
        "**every word becomes a vector, learned from raw text** = 모든 단어가 벡터가 되고, 날 글에서 배워요",
        "**no labels needed** = 사람이 정답표를 달 필요가 없어요",
        "**You shall know a word by the company it keeps** = 단어는 어울리는 친구로 안다 (Firth, 1957)",
        "**Directions carry meaning** = 방향이 뜻을 담아요"),
    cmp("2막 통계 vs 3막 word2vec", ["", K("stat"), K("w2v")], [
        ["단어를 다루는 법", "횟수를 셈", "벡터(좌표)로 바꿈"],
        ["cat 과 kitten", "관계를 모름", "드디어 이웃이 됨"],
        ["라벨", "필요 없음(세기)", "필요 없음(날 글로 학습)"],
    ]),
    chk(f"{K('dh')}을 한 문장으로 말하면?", ["단어는 어울리는 친구(주변 단어)로 안다", "단어는 글자 수로 안다", "단어는 사전 순서로 안다"], 0,
        "You shall know a word by the company it keeps (Firth, 1957) 예요."),
], [
    look("슬라이드 짚어 읽기",
         bx(100, 152, 980, 186, f"{K('w2v')} (2013): 모든 단어가 벡터, 라벨 없이 날 글에서"),
         bx(100, 194, 950, 228, "Distributional hypothesis: Firth, 1957 의 한 문장"),
         bx(100, 236, 968, 270, "king - man + woman ≈ queen, Seoul - Korea + Japan ≈ Tokyo"),
         bx(208, 340, 728, 624, "similar meaning → nearby vectors: 동물, 음식, 감정끼리 모여요"),
         bx(740, 340, 1192, 624, "man → king 과 woman → queen 화살표가 나란해요(royalty direction)"),
         bx(405, 682, 1000, 710, "통계의 벽이 무너짐: cat 과 kitten 이 드디어 이웃")),
    formula("뜻의 덧셈 뺄셈", r"\vec{king} - \vec{man} + \vec{woman} \approx \vec{queen}",
            [(r"\vec{king}", "king 의 좌표(벡터)"), (r"- \vec{man}", "남자 쪽 성질을 빼고"), (r"+ \vec{woman}", "여자 쪽 성질을 더하면"), (r"\approx \vec{queen}", "queen 좌표 근처에 도착")],
            "방향이 뜻을 담아서, 좌표를 빼고 더하면 뜻의 산수가 돼요."),
    bg("기초 다지기 1단원", "벡터는 숫자 목록이고, 화살표나 지도 좌표로 그릴 수 있어요.", "두 좌표를 빼면 '어느 쪽으로 얼마나' 라는 방향이 나와요."),
    prof("모든 단어를 벡터로 표현해 보자는 아이디어가 대성공을 해요. 라벨 없이 날 텍스트만 학습해요.",
         "비슷한 맥락에 나타나는 단어가 비슷한 벡터를 갖게 하자는 거예요.",
         "항상 다 되는 건 아니지만, 의미에 대한 산수가 가능해졌어요.",
         "벡터를 직접 만들어 보는 건 2주차 word2vec 시간에 해요."),
    pts("과제와 이어지는 부분", "word2vec 은 2주차 강의(N2)와 실습(Lab 0-1)에서 자세히 배우고, 과제 1과 이어져요."),
], [
    chk("'Seoul - Korea + Japan' 은 무엇에 가까울까요?", ["Tokyo", "Seoul", "Korea"], 0, "나라의 수도 방향이 같아서 Tokyo 근처에 도착해요."),
    chk("분포 가설 문장을 말한 사람과 연도는?", ["Firth, 1957", "Shannon, 1948", "Turing, 1950"], 0,
        "Firth 1957 이에요. word2vec(2013)보다 훨씬 오래된 생각이에요."),
    eng("3막 word2vec 요약", "word2vec(2013)은 라벨 없이 단어를 벡터로 배운다. 분포 가설(Firth 1957)에 따라 문맥이 비슷하면 가깝고, king - man + woman ≈ queen 처럼 방향이 뜻을 담는다.",
        "벡터 + 분포 가설 + 뜻의 산수", "통계의 벽(cat, kitten)을 넘었다고 이어서 외워요."),
    warn("헷갈리기 쉬운 점", "word2vec 은 2013년, 분포 가설 문장은 Firth 1957년이에요. 두 연도를 섞지 마세요.",
         "≈ 는 '딱 같다' 가 아니라 '가장 가깝다' 예요. 교수님도 '항상 다 되는 건 아니다' 라고 했어요."),
])

assert abs(0.06 + 0.10 + 0.84 - 1.0) < 1e-9

page(21, "3. History of NLP | Act 3 - seq2seq & Attention (2014-16)", E("rnn", "lstm", "hid", "s2s", "enc", "dec", "att", "mt", "nn"), [
    say(f"3막 두 번째 장면: 문장을 한 단어씩 읽는 {K('nn')}이에요.",
        f"번역기는 {K('enc')}가 원문을 읽고, {K('dec')}가 번역문을 써요."),
    ana("한 단어씩 읽으며 메모장을 고쳐 쓰는 사람", "책을 한 단어씩 읽으면서, 지금까지 내용을 메모장에 짧게 요약해 고쳐 써요. 다 읽으면 메모장 하나가 남아요.",
        [["한 단어씩 읽는 사람", K("rnn")], ["메모장", K("hid")]]),
    tl_fig(3, "3막, seq2seq 와 어텐션"),
], [
    pts("용어 하나씩",
        f"{K('rnn')}, {K('lstm')}: 단어를 하나씩 읽으며 기억(memory)을 들고 가는 신경망",
        f"그 기억(메모장)을 {K('hid', '이라고')} 해요",
        f"{K('s2s')}(2014): 문장(순서열)을 받아 다른 문장을 내놓는 구조",
        f"{K('enc')}: 원문을 읽고 압축해요(reads & compresses the source)",
        f"{K('dec')}: 번역문을 한 단어씩 써요(writes the target word by word)",
        f"{K('att')}(2015): 디코더가 필요할 때 원문을 다시 흘끗 봐요(glance back)"),
    steps("'나는 너를 사랑해' → 'I love you'", [
        "인코더가 나는, 너를, 사랑해 를 읽으며 h1, h2, h3 를 만들어요",
        "요약(context)이 디코더로 넘어가요",
        "디코더가 s1 에서 I, s2 에서 love, s3 에서 you 를 써요",
        "love 를 쓸 때 어텐션이 원문 중 어디를 볼지 정해요"],
        "원문 전체를 한 번에 외우지 않고, 필요할 때 다시 봐요."),
    chk(f"{K('att')}이 하는 일은?", ["디코더가 원문 중 지금 중요한 단어를 다시 보게 함", "문장을 한 단어씩 읽음", "단어를 셈"], 0,
        "which source word matters right now? 가 어텐션의 질문이에요."),
], [
    look("슬라이드 짚어 읽기",
         bx(100, 152, 860, 186, "RNN / LSTM: 한 단어씩 읽으며 기억을 들고 가는 신경망"),
         bx(100, 195, 855, 258, "seq2seq (2014): 인코더가 압축, 디코더가 씀. attention (2015): 원문을 다시 봄"),
         bx(495, 348, 895, 372, "attention: 'which source word matters right now?' 지금 어느 원문 단어가 중요?"),
         bx(250, 425, 635, 590, "인코더 h1 나는, h2 너를, h3 사랑해. 위 숫자 0.06, 0.10, 0.84 는 주목 비율"),
         bx(760, 395, 1145, 590, "디코더 s1, s2, s3 가 I, love, you 를 한 단어씩"),
         bx(370, 648, 1035, 672, "2016: 구글 번역이 하룻밤에 신경망으로, 사용자가 느낄 만큼 품질 점프")),
    steps("어텐션 숫자 읽기", [
        "love 를 쓰는 s2 에서 원문 세 단어에 비율을 나눠 줘요",
        "나는 0.06, 너를 0.10, 사랑해 0.84",
        "0.06 + 0.10 + 0.84 = 1.00",
        "가장 큰 0.84 → 사랑해 에 가장 주목"],
        "love 를 쓸 때 '사랑해' 를 가장 많이 봐요. 비율을 다 더하면 1 이에요."),
    prof("RNN, LSTM 도 사실 1990년대 논문이지만 한동안 크게 성공하지 못했어요.",
         "2014년 구글에서 기계 번역을 위해 seq2seq 가 나와요.",
         "예전엔 문장 전체를 벡터 하나에 우겨 넣다 보니, 다음 토큰을 만들 때 앞을 기억하기 어려웠어요.",
         "어텐션은 다음 토큰을 만들 때 앞 문장에 다시 접근해 어디에 주목할지 봐요. 그래서 이름이 attention 이에요."),
    pts("다음에 어디서 다시 만나나", "RNN 과 언어 모델은 3주차(N3), 어텐션은 4주차에 자세히 배워요."),
], [
    chk("2016년에 일어난 일은?", ["구글 번역이 신경망 방식으로 바뀜", "word2vec 발표", "ChatGPT 공개"], 0,
        "Google Translate switches to neural overnight 이에요."),
    chk("seq2seq 에서 원문을 읽고 압축하는 쪽은?", [K("enc"), K("dec"), K("att")], 0, "encoder, reads & compresses the source 예요."),
    eng("3막 seq2seq 와 어텐션 요약", "RNN/LSTM 은 한 단어씩 읽는 신경망이다. seq2seq(2014)는 인코더가 압축, 디코더가 쓰고, 어텐션(2015)은 원문을 다시 보게 한다. 2016 구글 번역 전환.",
        "2014 seq2seq, 2015 attention, 2016 구글 번역", "교훈: 단어를 벡터로 두고, 규칙은 신경망이 배우게 하라."),
    warn("헷갈리기 쉬운 점", "슬라이드에서 3막은 두 쪽이에요(word2vec, seq2seq 와 어텐션).",
         "seq2seq 2014, 어텐션 2015, 구글 번역 전환 2016. 한 해씩 차례로 외워요."),
])

page(22, "3. History of NLP | Act 4 - Transformers & Pretraining", E("tf", "att", "rnn", "pre", "ft", "lm", "bert", "gpt", "senti", "ner"), [
    say(f"4막: 2017년 {K('tf')}가 나와요. 어텐션만으로 만든 신경망이에요.",
        f"그리고 새 요리법: 웹 전체로 한 번 {K('pre')}하고, 일마다 싸게 맞춰 써요."),
    tl_fig(4, "4막, 트랜스포머와 사전 학습"),
], [
    pts("슬라이드 영어 뜻",
        "**Attention Is All You Need** = 어텐션만 있으면 된다 (2017 논문 제목)",
        "**no recurrence** = RNN 처럼 한 단어씩 돌지 않아요",
        "**processes all words in parallel → scales beautifully on GPUs** = 모든 단어를 한꺼번에 처리 → GPU 로 크게 키우기 좋아요",
        "**pretrain once, adapt cheaply** = 한 번 사전 학습, 싸게 맞춰 쓰기"),
    steps("새 요리법 순서", [
        "재료: 웹 전체(책, 위키, 코드), 라벨 필요 없음",
        f"{K('pre')}: 빠진 단어 맞히기(predict the missing word)",
        "결과: 사전 학습된 언어 모델(Pretrained Language Model) 하나",
        f"{K('ft')}: 작은 데이터(+ small data)로 일마다 맞추기"],
        "모델 하나 → 모든 일(one model → every task)."),
    chk(f"{K('tf')}가 크게 키우기 좋은 까닭은?", ["모든 단어를 병렬로 처리해서 GPU 에 잘 맞음", "단어를 하나씩 순서대로 읽어서", "규칙을 손으로 써서"], 0,
        "processes all words in parallel, that is the whole trick 이에요."),
], [
    look("슬라이드 짚어 읽기",
         bx(100, 152, 970, 215, "2017 'Attention Is All You Need': 어텐션만, 순환 없음, 병렬 처리가 비결"),
         bx(100, 225, 948, 260, "새 요리법: 라벨 없는 웹 전체로 pretrain once → adapt cheaply"),
         bx(150, 390, 405, 578, "the whole web: books, wiki, code. no labels needed"),
         bx(553, 410, 825, 545, "Pretrained Language Model: 빠진 단어 맞히기로 배운 모델"),
         bx(760, 330, 1252, 578, f"fine-tuning: 감성 분석, 질의응답, 번역, 개체명 각각 + small data"),
         bx(215, 678, 1190, 708, "2018 BERT & GPT: 한 아이디어의 두 반쪽. NLP 의 ImageNet moment")),
    cmp(f"{K('rnn')} vs {K('tf')}", ["", "RNN / LSTM", K("tf")], [
        ["읽는 법", "한 단어씩 순서대로", "모든 단어를 한꺼번에(병렬)"],
        ["핵심 부품", "순환(recurrence)", f"{K('att')}만"],
        ["GPU 로 키우기", "어려움", "아주 잘 됨"],
    ]),
    prof("2017년에 제목부터 도발적인 논문이 나와요. 어텐션만 있으면 된다는 뜻이죠.",
         "하나씩 보던 어텐션을 셀프 어텐션으로 확장했어요.",
         "꽤 중요하고 오래 다뤄야 할 내용이라 4주차나 5주차쯤 다룰게요.",
         "2017년이면 공학에서 아주 오래된 건 아니지만, 우리에겐 꽤 오래된 논문처럼 느껴져요."),
    pts("ImageNet moment 란", f"2018 {K('bert')}와 {K('gpt')}: 언어를 한 번 배워 두고 어디서나 다시 써요(learn language once, reuse it everywhere).",
        f"예: {K('senti')}, 질의응답, 번역, {K('ner')}을 작은 데이터로 맞춰요."),
], [
    chk("BERT 와 GPT 가 나온 해는?", ["2018", "2013", "2022"], 0, "2018 BERT & GPT, two halves of one idea 예요."),
    chk("사전 학습 데이터에 필요한 것은?", ["라벨 없는 많은 글", "사람이 단 정답 라벨", "손으로 쓴 규칙"], 0, "pretrain once on the whole unlabeled web, no labels needed 예요."),
    eng("4막 요약", "4막: 트랜스포머(2017)는 순환 없이 어텐션만 써서 병렬 처리한다. 라벨 없는 웹으로 사전 학습, 작은 데이터로 미세 조정하는 방식이 BERT, GPT(2018)로 자리 잡았다.",
        "2017 트랜스포머 + 2018 사전 학습(BERT, GPT)", "'한 번 배워 어디서나' 가 ImageNet moment."),
    warn("헷갈리기 쉬운 점", "사전 학습은 라벨이 없고, 미세 조정은 작은 라벨 데이터를 써요.",
         "p.16 부제목과 p.24 표에서는 트랜스포머를 '4막 Pretraining' 에 넣어요."),
])

_ratio = 540 / 0.094
assert 5700 <= _ratio < 5800 and 2022 - 2018 == 4

page(23, "3. History of NLP | Act 5 - LLMs (2020-now)", E("llm", "scale", "param", "gpt", "icl", "chatgpt", "it", "rlhf", "exaone", "bert", "cls"), [
    say(f"5막: {K('llm')}의 시대예요(2020~지금).",
        "크게 키울수록 좋아진다는 걸 알고, 계속 키웠어요.",
        "그러자 예시 몇 개만 보여 줘도 일을 해내는 모델이 나왔어요."),
    tl_fig(5, "5막, LLM"),
], [
    pts("용어 하나씩",
        f"{K('scale')}: {K('param')} + 데이터 + 계산량을 늘리면 예측 가능하게 좋아져요",
        f"{K('icl')}: 프롬프트에 예시 몇 개만 넣으면 그 일을 해요({K('gpt')}-3, 2020)",
        f"{K('it')}: '이렇게 해 줘' 같은 지시를 따르게 학습",
        f"{K('rlhf')}: 사람이 더 좋다고 고른 답 쪽으로 다듬기"),
    steps("5막 흐름", [
        f"{K('scale')}: 크게 키우면 좋아진다",
        "GPT-3 (2020): 문맥 내 학습",
        f"{K('chatgpt')} (2022): + 지시 학습 + RLHF → 두 달 만에 사용자 1억 명",
        f"2023~26: GPT-4, Claude, Gemini, Llama, 한국어 LLM({K('exaone')}, HyperCLOVA X, SKT-A.X, SOLAR)"],
        "NLP 가 연구실 주제에서 사회의 기반 시설(infrastructure)이 됐어요."),
    chk("GPT-3 가 보여 준 '프롬프트에 예시 몇 개만 넣으면 일을 한다' 는 능력은?", [K("icl"), K("rlhf"), K("scale")], 0,
        "show a few examples in the prompt and it does the task, in-context learning 이에요."),
], [
    look("슬라이드 짚어 읽기",
         bx(100, 152, 940, 186, "Scaling laws: 파라미터 + 데이터 + 계산 → 예측 가능하게 좋아짐"),
         bx(100, 192, 992, 226, "GPT-3 (2020): in-context learning"),
         bx(100, 233, 965, 266, "ChatGPT (2022): + instruction tuning + RLHF → 두 달에 1억 명, 역대 최고 속도"),
         bx(100, 274, 1146, 307, "2023~26: GPT-4, Claude, Gemini, Llama, 한국어 LLM EXAONE, HyperCLOVA X, SKT-A.X, SOLAR"),
         bx(180, 380, 820, 640, "파라미터 그래프(로그 눈금): ELMo 0.094B → PaLM 540B, 4년에 약 5,700배"),
         bx(820, 380, 1212, 636, "2023~: 최전선 모델 크기는 비공개, 계산량은 계속 늘어요")),
    cmp("그래프 속 모델 크기", ["모델", "해", f"{K('param')} 수"], [
        ["ELMo", "2018", "0.094B (약 9,400만)"],
        [f"{K('bert')}-Large", "2018", "0.34B"],
        ["GPT-2", "2019", "1.5B"],
        ["T5-11B", "2019", "11B"],
        ["GPT-3", "2020", "175B"],
        ["Gopher / PaLM", "2021 / 2022", "280B / 540B"],
    ]),
    steps("'약 5,700배' 확인", ["B 는 billion, 10억이에요", "PaLM 540B / ELMo 0.094B = 약 5,745", "2018 → 2022 = 4년"],
          "4년 만에 약 5,700배 커졌어요(~5,700x in 4 years)."),
    bg("기초 다지기 4단원", "그래프 세로축은 로그 눈금이에요. 한 칸 올라갈 때마다 10배예요.", "그래서 직선처럼 보여도 실제로는 엄청 빠르게 커지는 거예요."),
    prof("ChatGPT 가 2022년 11월에 나와요. 두 달 만에 1억 명, 역사상 가장 빠른 서비스 성장이에요.",
         "예전엔 스팸 필터를 만들려면 스팸 데이터를 모아 학습시켰는데, GPT-3 부터는 프롬프트에 예시 몇 개만 주면 돼요. 퓨샷 러닝, 인컨텍스트 러닝이라고 해요.",
         "왜 이런 능력이 갑자기 생겼는지는 아직 완벽한 해석이 없어요.",
         "네이버 하이퍼클로바 X, LG 엑사원, 업스테이지 솔라 등이 발전했고, 요즘은 에이전트로 확장 중이에요."),
], [
    chk("ChatGPT(2022)에 더해진 두 가지는?", ["지시 학습과 RLHF", "규칙과 사전", "n-gram 과 word2vec"], 0,
        f"+ instruction tuning + RLHF 예요. {K('it', '과')} {K('rlhf', '으로')} 사람 말을 잘 따르게 했어요."),
    chk("ChatGPT 가 사용자 1억 명을 모은 기간은?", ["두 달", "두 해", "두 주"], 0, "100M users in two months, fastest ever 예요."),
    eng("5막 요약", "5막 LLM: 스케일링 법칙으로 모델을 키웠고, GPT-3(2020)는 문맥 내 학습을, ChatGPT(2022)는 지시 학습과 RLHF 로 두 달에 1억 명을 보였다.",
        "스케일링 → GPT-3 → ChatGPT → 2023~26", "20 GPT-3, 22 ChatGPT 두 해 차이."),
    warn("헷갈리기 쉬운 점", "GPT-3 는 2020, ChatGPT 는 2022 예요.", "문맥 내 학습은 모델을 다시 학습시키지 않고 프롬프트의 예시만으로 해요."),
])

page(24, "3. History of NLP | 70 Years on One Slide", E("rule", "stat", "nn", "pre", "llm", "amb", "turing", "eliza", "w2v", "s2s", "att", "tf", "bert", "gpt", "chatgpt", "agent"), [
    say("70년을 한 장에 담은 쪽이에요.",
        "막이 갈수록 사람이 손으로 넣는 지식은 줄고, 데이터에서 배우는 건 늘어요.",
        "그리고 모든 막은 중의성에 대한 새 답이에요."),
    tl_fig(None, ""),
], [
    pts("슬라이드 영어 뜻",
        "**hard-codes less human knowledge and learns more from data** = 사람 지식은 덜 박아 넣고, 데이터에서 더 배워요",
        f"**Every act is a new answer to ambiguity** = 모든 막이 {K('amb')}에 대한 새 답",
        "**this course walks the whole arc** = 이 수업은 이 흐름 전체를 걸어가요"),
    cmp("다섯 막 한눈에", ["막", "이름", "대표 장면"], [
        ["1막", K("rule"), f"1950 {K('turing')}, 1966 {K('eliza')}"],
        ["2막", K("stat"), "1990s IBM 통계 번역, n-gram LM, 2003 Neural LM (Bengio)"],
        ["3막", K("nn"), f"2013 {K('w2v')}, 2014~15 {K('s2s')} + {K('att')}"],
        ["4막", K("pre"), f"2017 {K('tf')}, 2018 {K('bert')} / {K('gpt')}"],
        ["5막", K("llm"), f"2020 GPT-3, 2022 {K('chatgpt')}, 2024~26 멀티모달, 추론, {K('agent')}"],
    ]),
    chk("막이 갈수록 어떻게 바뀌나요?", ["사람 손 지식은 줄고 데이터 학습은 늘어요", "사람 손 규칙이 늘어요", "데이터가 줄어요"], 0,
        "Each act hard-codes less human knowledge and learns more from data 예요."),
], [
    look("타임라인 짚어 읽기",
         bx(116, 257, 320, 578, f"Act 1 Rules: 1950 {K('turing')}, 1966 {K('eliza')}(first chatbot)"),
         bx(326, 257, 530, 578, "Act 2 Statistics: 1990s IBM statistical MT, n-gram LMs, 2003 Neural LM (Bengio)"),
         bx(537, 257, 741, 578, f"Act 3 Neural nets: 2013 {K('w2v')}, 2014~15 seq2seq + attention"),
         bx(747, 257, 951, 578, f"Act 4 Pretraining: 2017 {K('tf')}, 2018 BERT / GPT"),
         bx(957, 257, 1267, 578, f"Act 5 LLMs: 2020 GPT-3(in-context), 2022 {K('chatgpt')}, 2024~26 multimodal, reasoning, agents"),
         bx(100, 625, 825, 658, "Every act is a new answer to ambiguity: 핵심 난제는 그대로")),
    cmp("연표 전체 (연도 → 사건)", ["연도", "사건"], [
        ["1947 / 1950 / 1954 / 1956", "위버 번역 = 암호, 튜링 테스트, 조지타운-IBM, 다트머스(AI 이름)"],
        ["1966", "ELIZA, ALPAC 보고서"],
        ["1948 뿌리 / 1990s / 2003", "섀넌 잡음 채널, IBM 통계 번역과 n-gram, Bengio 신경망 LM"],
        ["2013 / 2014 / 2015 / 2016", "word2vec, seq2seq, attention, 구글 번역 신경망 전환"],
        ["2017 / 2018", "Transformer, BERT 와 GPT"],
        ["2020 / 2022 / 2023~26", "GPT-3, ChatGPT, GPT-4, Claude, Gemini, Llama, EXAONE, 에이전트"],
    ]),
    prof("처음에는 규칙으로 처리하려다 이건 아니다 싶어 통계로 넘어왔고, 이후에는 데이터 기반으로 쭉 왔어요.",
         "NLP 뿐 아니라 모든 인공지능이 패턴을 통해 기계가 인간 지능을 따라 하게 하자는 것이고, 데이터 드리븐으로 해결한 역사예요.",
         "다음 주는 토큰화와 단어 벡터예요. ChatGPT 같은 모델이 문장을 어떤 단위로 쪼개 보는지, 한국어와 영어가 뭐가 다른지 배워요."),
], [
    exam("예상 문제", "다음 사건을 일어난 순서대로 나열하시오. (가) ChatGPT (나) ELIZA (다) word2vec (라) Transformer (마) IBM 통계 번역",
         "다섯 사건의 연도를 떠올려 옛날부터 줄 세우기",
         ["ELIZA = 1966 (1막)", "IBM 통계 번역 = 1990s (2막)", "word2vec = 2013 (3막)", "Transformer = 2017 (4막)", "ChatGPT = 2022 (5막)"],
         "(나) → (마) → (다) → (라) → (가)"),
    chk("2017 Transformer 는 p.24 표에서 몇 막에 있나요?", ["4막 Pretraining", "3막 Neural nets", "5막 LLMs"], 0,
        "Act 4 Pretraining 칸에 Transformer(2017)와 BERT / GPT(2018)가 있어요."),
    chk("2003년 'Neural LM (Bengio)' 는 표에서 어느 칸?", ["2막 Statistics", "3막 Neural nets", "1막 Rules"], 0,
        "이름엔 Neural 이 있지만 표에서는 2막 Statistics 칸의 2003 이에요."),
    eng("70년 한 줄 주문", "NLP 역사는 규칙 → 통계 → word2vec → seq2seq, 어텐션 → 트랜스포머, 사전 학습 → LLM 으로 흘러왔고, 막이 갈수록 사람이 넣는 지식은 줄고 데이터에서 배우는 몫은 늘었으며, 모든 막은 중의성에 대한 새 답이다.",
        "여섯 계단 + 공통점 두 개", "여섯 계단을 소리 내서 세 번 읽어요."),
    warn("헷갈리기 쉬운 점", "p.16 은 다섯 막(규칙 → 통계 → 신경망 → 사전 학습 → LLM), 이 레슨의 주문은 여섯 계단이에요. 3막 신경망을 word2vec 과 seq2seq 두 계단으로 나눴을 뿐이에요."),
])

# ================= 4부: MINT Lab =================
page(25, "MINT Lab (구분)", [], [
    say("4부: 교수님 연구실 MINT Lab 소개예요.",
        "시험과는 거리가 멀어요. 가볍게 넘어가요."),
])

page(26, "4. MINT Lab | What We Do", E("llm", "rag", "exaone"), [
    say("MINT 는 Machine Intelligence, Natural language, Trustworthiness 의 앞 글자예요.",
        "2026년에 새로 생긴 인공지능학과 연구실이에요."),
], [
    pts("연구 주제 네 칸",
        f"{K('llm')}: 긴 문맥에서도 안정적인 최전선 한국어 LLM",
        f"{K('rag')}: 찾아 온 근거를 모델이 정말 쓰게 하기, 한국어 RAG",
        "LLM 평가와 견고성: LLM-as-a-judge 의 숨은 편향, 믿을 수 있는 평가 설계",
        "개인화와 기억: 모델이 내 취향을 언제 적용하고 언제 참아야 하나"),
], [
    look("슬라이드 짚어 읽기",
         bx(100, 152, 1095, 186, "MINT = Machine Intelligence, Natural language, Trustworthiness"),
         bx(75, 293, 1332, 592, "네 칸: LLM, RAG, LLM 평가와 견고성, 개인화와 기억"),
         bx(278, 628, 1128, 656, f"최근 성과: EMNLP 2026, CIKM 2026, EACL 2026 Findings, {K('exaone')} 기술 보고서"),
         bx(462, 678, 944, 706, "이 수업 9~14주 = 연구실의 매일 연구 주제")),
    prof("LLM 을 다루고 개발하던 쪽에서 와서 LLM 연구를 많이 해 볼 생각이에요.",
         "RAG(검색 증강 생성), 신뢰할 수 있는 AI 평가와 벤치마크, 한국어 중심 AI, 에이전트 연구도 하려고 해요."),
])

page(27, "4. MINT Lab | 함께할 학생을 찾습니다", [], [
    say("대학원생과 학부연구생을 찾는다는 안내예요.",
        "9~14주 내용이 재밌다면 이메일로 연락하라고 하셨어요. 준비 없이 커피챗 환영이에요."),
], [], [
    prof("신임이라 지금 당장은 인건비와 장비가 넉넉하지 않아서, 9월에 바로 연구를 시작하긴 어려워요.",
         "연구실(N223)은 정리 중이라 추석 이후쯤 입주할 것 같아요. 그때까지는 카페 같은 데서 얘기해요.",
         "저학년이어도 괜찮아요. 관심과 열정이 제일 중요해요.",
         "수업 질문, 진로 상담(기업에 가고 싶다 등)도 언제든 이메일로 환영해요."),
])

# ================= 용어 풀이 =================
GL = {
    "nlp": ("컴퓨터가 사람 말을 처리하고, 이해하고, 만들어 내게 하는 분야", "자연어 이해(NLU)와 자연어 생성(NLG) 두 방향을 합친 말이에요. 말을 잘 다루는 기계가 똑똑해 보여서 AI 의 한가운데 있어요."),
    "nlu": ("글에서 뜻(의도, 개체, 사실)을 뽑아내는 쪽", "분류, 정보 뽑기, 검색, 질문에 답하기가 여기에 들어가요. 방향은 글 → 뜻이에요."),
    "nlg": ("뜻에서 새 글을 만들어 내는 쪽", "글쓰기, 요약, 응답이 여기에 들어가요. 방향은 뜻 → 글이에요."),
    "amb": ("같은 글자가 여러 뜻으로 읽히는 성질", "단어(배, bank), 구조(I saw a man with a telescope), 띄어쓰기(아버지가방에) 수준이 있어요. NLP 의 핵심 난제예요."),
    "aggl": ("어간에 작은 조각을 붙여 한 단어를 만드는 언어, 한국어가 대표", "먹- + -었- + -겠- + -더라 → 먹었겠더라처럼요. 그래서 한국어 동사는 형태가 수천 가지예요."),
    "morph": ("뜻을 가진 가장 작은 말의 조각", "먹었겠더라는 먹-, -었-, -겠-, -더라 네 형태소로 이루어져요."),
    "manal": ("단어를 형태소로 쪼개 주는 도구", "한국어는 형태소가 많이 붙어서 형태소 분석이 특히 중요해요. 2주차 토큰화와 이어져요."),
    "corpus": ("컴퓨터가 배우려고 모아 둔 아주 많은 글 묶음", "통계 시대(2막)부터 말뭉치에서 패턴을 세는 방식이 중심이 됐어요."),
    "token": ("글을 컴퓨터가 다루는 작은 조각으로 자른 것", "레고 조각에 비유해요. 단어일 수도, 단어 조각일 수도 있어요. 2주차에 자세히 배워요."),
    "tok": ("글을 토큰으로 자르는 일", "과목 주문의 첫 단계예요. 2주차 주제예요."),
    "ngram": ("바로 앞 몇 단어만 보고 다음 단어를 맞히는 세기 방법", "n 개씩 붙은 단어 묶음을 말해요. 1-gram 은 한 단어, 2-gram 은 두 단어. 3주차에 직접 만들어요."),
    "lm": ("다음에 올 단어(토큰)를 맞히는 모델", "휴대폰 자판의 다음 단어 추천과 같아요. P(다음 단어 | 앞 단어들)을 계산해요."),
    "w2v": ("단어를 벡터(지도 좌표)로 바꾸는 2013년 방법", "라벨 없이 날 글에서, 주변 단어로 뜻을 배워요. king - man + woman ≈ queen 같은 뜻의 산수가 돼요."),
    "wv": ("단어를 숫자 목록으로 나타낸 것, 단어의 지도 좌표", "뜻이 비슷한 단어는 가까운 벡터가 돼요."),
    "dh": ("'친구를 보면 그 사람을 안다' 처럼, 주변 단어로 단어 뜻을 안다는 생각", "Firth(1957)의 'You shall know a word by the company it keeps' 가 대표 문장이에요."),
    "rnn": ("문장을 한 단어씩 읽으며 메모장(은닉 상태)을 고쳐 쓰는 신경망", "매 단계 같은 부품을 다시 써요. 3주차에 자세히 배워요."),
    "lstm": ("RNN 을 고쳐서 긴 문장도 더 잘 기억하게 한 신경망", "게이트로 무엇을 기억하고 잊을지 정해요. 1990년대에 나왔어요."),
    "hid": ("RNN 이 지금까지 읽은 내용을 요약해 들고 있는 메모장", "한 단어를 읽을 때마다 새로 고쳐 써요."),
    "s2s": ("문장을 받아 다른 문장을 내놓는 구조(2014)", "인코더가 원문을 압축하고 디코더가 결과 문장을 써요. 기계 번역에서 나왔어요."),
    "att": ("결과를 만들 때 입력 중 지금 중요한 부분에 주목하는 방법", "2015년 seq2seq 번역에서 나왔고, 2017년 트랜스포머의 핵심이 됐어요. 4주차 주제예요."),
    "tf": ("어텐션만으로 만든 신경망 구조(2017)", "순환 없이 모든 단어를 병렬로 처리해서 GPU 로 크게 키우기 좋아요. 요즘 LLM 의 뼈대예요."),
    "pre": ("라벨 없는 거대한 글로 먼저 언어를 익히는 단계", "한 번 사전 학습한 모델을 여러 일에 싸게 맞춰 써요. BERT, GPT(2018)가 대표예요."),
    "post": ("사전 학습 뒤 사람이 원하는 대로 모델을 다듬는 단계", "지시 학습, RLHF 같은 방법이 들어가요. 7주차 주제예요."),
    "llm": ("아주 많은 글로 학습한 아주 큰 언어 모델", "ChatGPT, Claude, EXAONE 같은 모델이에요. 프롬프트 하나로 여러 NLP 일을 해요."),
    "param": ("모델이 학습하며 스스로 맞춰 가는 숫자들", "개수가 모델 크기예요. GPT-3 는 175B(1,750억) 개예요."),
    "cls": ("글 하나에 라벨 하나를 붙이는 일", "스팸/정상, 긍정/부정, 주제 가르기가 대표예요."),
    "ner": ("글 속에서 사람, 장소, 날짜 같은 이름 붙은 것을 찾는 일", "토큰마다 태그를 붙이는 시퀀스 레이블링의 한 종류예요."),
    "cnn": ("작은 창을 밀며 특징을 잡는 신경망", "이미지에서 유명하지만 글에도 써요. 3주차에 나와요."),
    "turing": ("기계와 대화해 보고 사람인지 기계인지 가리는 지능 시험", "1950년 앨런 튜링이 'Can machines think?' 를 물으며 제안했어요."),
    "eliza": ("1966년 MIT 의 최초 챗봇", "패턴 규칙 약 200개로 심리 상담사를 흉내 냈어요. 뜻도 기억도 없었지만 사람들은 속마음을 털어놨어요."),
    "gib": ("1954년 러시아어 60문장을 영어로 번역해 보인 시연", "'5년 안에 번역 해결' 을 장담했지만 틀렸어요."),
    "mt": ("컴퓨터가 한 언어를 다른 언어로 옮기는 일", "1947 위버의 '번역 = 암호 풀기' 에서 시작해 2016년 구글 번역의 신경망 전환까지 이어져요."),
    "alpac": ("1966년 기계 번역이 약속보다 훨씬 어렵다고 결론 낸 미국 보고서", "그 뒤 미국 연구 지원이 약 10년 동안 끊겨 'AI 겨울' 이 왔어요."),
    "dart": ("1956년 여름, 인공지능이라는 이름이 생긴 모임", "사진 맨 오른쪽이 섀넌이에요."),
    "ai": ("사람처럼 생각하고 배우는 기계를 만드는 분야", "1956년 다트머스 워크숍에서 이름이 생겼어요."),
    "rule": ("사람이 규칙을 손으로 써서 말을 처리하는 방법(1막)", "ELIZA, SHRDLU 가 예예요. 언어는 규칙으로 다 적을 수 없어서 한계에 부딪혔어요."),
    "stat": ("규칙 대신 많은 글에서 패턴을 세어 확률로 처리하는 방법(2막)", "n-gram, IBM 통계 번역이 대표예요. 뜻을 모른다는 벽이 있었어요."),
    "noisy": ("잡음 낀 통로를 지나 망가진 메시지를 확률로 원래대로 되돌리는 생각", "섀넌(1948)의 정보 이론에서 나왔고, 통계 번역과 음성 인식의 설계도가 됐어요."),
    "nn": ("숫자를 여러 층으로 계산하며 데이터에서 규칙을 배우는 모델", "3막부터 NLP 의 주인공이에요. 기초 다지기 9단원에서 자세히 봐요."),
    "enc": ("원문을 읽고 요약(압축)하는 부분", "seq2seq 에서 원문 쪽을 맡아요."),
    "dec": ("요약을 받아 결과 문장을 한 단어씩 쓰는 부분", "seq2seq 에서 번역문 쪽을 맡아요. 어텐션으로 원문을 다시 봐요."),
    "ft": ("사전 학습한 모델을 작은 데이터로 특정 일에 맞추는 것", "감성 분석, 질의응답, 번역 같은 일마다 적은 데이터만 있으면 돼요."),
    "scale": ("파라미터, 데이터, 계산을 늘리면 성능이 예측 가능하게 좋아진다는 법칙", "그래서 모델을 계속 키웠고, 4년에 약 5,700배 커졌어요."),
    "icl": ("모델을 다시 학습시키지 않고 프롬프트 속 예시만 보고 일을 해내는 능력", "GPT-3(2020)가 보여 줬어요. 예시 몇 개를 주는 퓨샷 방식이 대표예요."),
    "it": ("지시문을 따르도록 모델을 추가로 학습시키는 것", "ChatGPT(2022)가 RLHF 와 함께 썼어요."),
    "rlhf": ("사람이 더 좋다고 고른 답 쪽으로 모델을 다듬는 방법", "Reinforcement Learning from Human Feedback 의 줄임말이에요. 사후 학습의 한 방법이에요."),
    "bert": ("2018년 나온 사전 학습 언어 모델", "GPT 와 함께 '한 번 배워 어디서나 쓰기' 시대를 연 두 반쪽이에요. 5주차에 배워요."),
    "gpt": ("2018년부터 나온 다음 단어를 맞히며 사전 학습한 언어 모델 계열", "GPT-3(2020)는 문맥 내 학습을, ChatGPT(2022)는 대화 서비스를 보여 줬어요."),
    "chatgpt": ("2022년 11월 공개된 대화형 LLM 서비스", "지시 학습과 RLHF 를 더했고, 두 달 만에 사용자 1억 명을 모았어요."),
    "exaone": ("LG AI연구원의 한국어 대규모 언어 모델", "교수님이 개발에 참여했다고 소개한 모델이에요. HyperCLOVA X 와 함께 한국어 LLM 의 예예요."),
    "prag": ("같은 말이 상황에 따라 다른 뜻이 되는 것을 다루는 분야", "'잘~한다' 가 칭찬인지 비꼼인지 가리는 문제예요."),
    "ellip": ("문장에서 맥락으로 알 수 있는 말을 빼는 것", "'밥 먹었어?' 에는 주어도 목적어도 없어요. 한국어에 특히 많아요."),
    "ref": ("'그것', 'it' 같은 말이 가리키는 대상", "트로피 문장처럼 세상 지식이 있어야 찾을 수 있을 때가 많아요."),
    "wino": ("한 단어만 바꾸면 it 이 가리키는 대상이 뒤집히는 문장 시험", "big 이면 트로피, small 이면 가방. 문법이 아니라 세상 지식을 시험해요."),
    "hon": ("말하는 상대에 따라 높여 말하는 한국어 문법", "먹어 / 드세요 / 잡수세요는 같은 사실, 다른 사회적 뜻이에요."),
    "lowres": ("데이터가 아주 적은 언어를 다루는 NLP", "지구의 7,000개 넘는 언어 대부분이 여기에 들어가요."),
    "seqlab": ("문장 속 토큰마다 태그를 하나씩 붙이는 일", "품사 태깅, 개체명 인식이 대표예요."),
    "pos": ("단어마다 명사, 동사 같은 품사를 붙이는 일", "시퀀스 레이블링의 대표 예예요. 통계 시대에도 쓰였어요."),
    "senti": ("글이 긍정인지 부정인지 가리는 일", "분류의 대표 예예요."),
    "rag": ("먼저 관련 자료를 찾아 오고, 그걸 근거로 답을 만들게 하는 방법", "10주차 주제예요. 교수님 연구실의 주요 연구 주제이기도 해요."),
    "agent": ("도구를 쓰고 계획을 세워 여러 단계 일을 해내는 LLM 시스템", "11주차 주제예요."),
    "torch": ("신경망을 만들고 학습시키는 파이썬 도구", "이 수업의 실습 도구예요."),
    "hf": ("사전 학습된 모델을 쉽게 받아 쓰게 해 주는 도구와 모임", "transformers 라이브러리를 만들었고, 주교재도 이 팀이 썼어요."),
    "tp": ("팀으로 한 학기 동안 하는 프로젝트", "성적의 25%예요. 8주차에 제안 발표, 학기 말에 결과와 보고서를 내요."),
    "pa": ("파이썬으로 직접 코드를 짜는 과제", "성적의 40%예요. 파이토치, 트랜스포머 구현, RAG, 에이전트, 평가가 들어가요."),
}
assert set(GL) == set(TERMS), set(TERMS) ^ set(GL)
GLOSSARY = [{"ko": TERMS[k][0], "en": TERMS[k][1], "say": s, "more": m} for k, (s, m) in GL.items()]

# ================= 검사, 저장 =================
import re
BAD = "—–·・"
_all = json.dumps({"g": GLOSSARY, "s": S}, ensure_ascii=False)
for ch in BAD:
    assert ch not in _all, ch

# 조사 검사: **ko(en)** 뒤 조사가 ko 받침과 맞는지
_rev = {}
for k, (ko, en, f) in TERMS.items():
    _rev[f"**{ko}({en})**" if ko else f"**{en}**"] = k
PAIRS = [("은", "는"), ("이", "가"), ("을", "를"), ("과", "와"), ("이에요", "예요")]
_errs = []
for disp, k in _rev.items():
    f = _fin(k)
    for m in re.finditer(re.escape(disp) + r"(으로|로|이에요|예요|은|는|이|가|을|를|과|와)(?=[\s,.)'?]|$)", _all):
        j = m.group(1)
        if j in ("으로", "로"):
            ok = (j == "로") == (f in (0, 2))
        else:
            ok = any((j == a and f) or (j == b and not f) for a, b in PAIRS)
        if not ok:
            _errs.append(disp + j)
assert not _errs, sorted(set(_errs))

json.dump({"deck": "N1", "from": 1, "to": 27, "glossary": GLOSSARY, "slides": S},
          open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("wrote", OUT, len(S), "pages,", len(GLOSSARY), "terms")
