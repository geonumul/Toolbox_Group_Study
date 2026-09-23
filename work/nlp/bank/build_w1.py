# -*- coding: utf-8 -*-
"""1주차 문제은행 (N1 강의 소개와 자연어처리의 역사) -> w1_basic.json, w1_hard.json
근거: 슬라이드 N1 (work/nlp/_src/N1.txt, png), 녹음 01주차_1_월_OT.txt. 계산은 assert.
"""
import json, pathlib

W = pathlib.Path(__file__).resolve().parent
U1, U2, U3, U4, U5, U6 = "1-1 강의 운영과 평가", "1-2 자연어처리란", "1-3 언어가 어려운 이유", "1-4 한국어 NLP", "1-5 역사: 시작, 규칙, 통계", "1-6 역사: 신경망에서 LLM 까지"
assert 5 + 40 + 25 + 30 == 100 and 25 + 30 == 55 and 40 + 30 == 70
assert 2022 - 1947 == 75 and 2017 - 2013 == 4


def mk(level, lst):
    out, cnt = [], {}
    for q in lst:
        t = q["type"]
        cnt[t] = cnt.get(t, 0) + 1
        q = dict(q)
        q["id"] = f"w1{level[0]}-{t}-{cnt[t]:03d}"
        q["part"] = "1"
        q["level"] = level
        out.append({k: q[k] for k in ["id", "type", "part", "level"] + [k for k in q if k not in ("id", "type", "part", "level")]})
    return out


def mcq(unit, slides, q, c, a, e, src=None):
    d = {"type": "mcq", "unit": unit, "slides": slides, "q": q, "c": c, "a": a, "e": e}
    if src:
        d["src"] = src
    return d


def ox(unit, slides, q, a, e, src=None):
    d = {"type": "ox", "unit": unit, "slides": slides, "q": q, "a": a, "e": e}
    if src:
        d["src"] = src
    return d


def short(unit, slides, q, a, e, src=None, num=False):
    d = {"type": "short", "unit": unit, "slides": slides, "q": q, "a": a, "e": e}
    if num:
        d["num"] = True
        d["tol"] = 0.01
    if src:
        d["src"] = src
    return d


def essay(unit, slides, q, answer, points, model, src=None):
    d = {"type": "essay", "unit": unit, "slides": slides, "q": q, "answer": answer, "points": points, "model": model}
    if src:
        d["src"] = src
    return d


def calc(unit, slides, q, qko, blanks, steps, answer, e, model):
    return {"type": "calc", "unit": unit, "slides": slides, "q": q, "qko": qko, "blanks": blanks, "steps": steps, "answer": answer, "e": e, "model": model}


B = [
    # ---- 1-1
    mcq(U1, "N1 p.8", "이 과목의 성적 구성으로 옳은 것은?", ["출석 5%, 과제 40%, 텀 프로젝트 25%, 기말고사 30%", "출석 10%, 과제 30%, 중간 30%, 기말 30%", "과제 40%, 중간고사 30%, 기말고사 30%", "출석 5%, 과제 25%, 텀 프로젝트 40%, 기말고사 30%"], 0,
        "슬라이드 p.8: Attendance 5%, Programming assignments 40%, Term project 25%, Final exam 30%. 중간고사는 없어요.", "강조"),
    mcq(U1, "N1 p.6", "중간고사가 없는 대신 8주차에 하는 것은?", ["텀 프로젝트 제안 발표", "퀴즈", "과제 1 제출", "보강"], 0, "p.6: No midterm, week 8 is your term-project proposal."),
    mcq(U1, "N1 p.5", "강의 목표로 슬라이드에 나오지 않는 것은?", ["음성 합성 모델을 처음부터 설계", "NLP 기본 개념과 방법 이해", "어텐션, 트랜스포머, 언어 모델 학습 이해", "Python, PyTorch, Hugging Face 로 구현하고 미세 조정"], 0,
        "p.5 목표 네 가지는 기본 개념 이해, 어텐션과 트랜스포머와 LM 학습 이해, 구현과 미세 조정, 한국어와 다국어 NLP 시스템 설계와 평가예요. 음성 합성은 없어요."),
    mcq(U1, "N1 p.5", "W1~4 '기초' 덩어리에서 다루는 것은?", ["토큰, 벡터, 어텐션, 트랜스포머", "PEFT, RAG, 에이전트", "사전 학습, 사후 학습, 정렬", "벤치마크, 추론, 한국어 NLP"], 0, "p.5: Foundations W1-4 tokens, vectors, attention & Transformer."),
    mcq(U1, "N1 p.7", "실습 환경으로 슬라이드가 말한 것은?", ["Colab (무료 GPU)", "개인 서버", "Excel", "MATLAB"], 0, "p.7: hands-on work runs in Colab (free GPU)."),
    mcq(U1, "N1 p.8", "AI 도구(ChatGPT, Claude) 사용 규칙으로 옳은 것은?", ["배우고 디버깅하는 데 쓰되, 사용을 밝히고 내 말로 쓴다", "절대 쓰면 안 된다", "쓰되 밝힐 필요는 없다", "과제는 AI 가 쓴 그대로 내도 된다"], 0, "p.8: use them to learn and debug, declare usage, write in your own words."),
    # ---- 1-2
    mcq(U2, "N1 p.10", "자연어(natural language)의 예가 아닌 것은?", ["Python", "한국어", "영어", "일본어"], 0, "p.10: 자연어는 사람이 자라며 쓰는 말이고 Python, 논리식은 아니에요."),
    mcq(U2, "N1 p.10", "글에서 의도, 대상, 사실 같은 뜻을 알아내는 쪽은?", ["NLU", "NLG", "OCR", "TTS"], 0, "NLU(자연어 이해)는 글 → 뜻, NLG 는 뜻 → 글이에요."),
    mcq(U2, "N1 p.10", "NLG(자연어 생성)가 하는 일로 알맞은 것은?", ["요약하기", "스팸 분류", "개체명 추출", "검색 순위 매기기"], 0, "p.10: NLG 는 write, summarize, respond. 분류와 추출은 NLU 쪽이에요."),
    mcq(U2, "N1 p.11", "슬라이드의 '하루 동안 쓰는 NLP' 에서 스팸 필터는 어떤 기술의 예로 나왔나요?", ["텍스트 분류기", "기계 번역", "음성 인식", "대규모 언어 모델"], 0, "p.11: the spam filter silently deletes 40 junk mails, a text classifier at work."),
    mcq(U2, "N1 p.15", "품사 태깅, 개체명 인식처럼 토큰마다 태그를 붙이는 과제는?", ["시퀀스 라벨링", "분류", "텍스트-투-텍스트", "검색"], 0, "p.15: Sequence labeling, every token → a tag."),
    mcq(U2, "N1 p.15", "번역과 요약은 어떤 과제 유형?", ["텍스트-투-텍스트", "분류", "시퀀스 라벨링", "검색과 QA"], 0, "p.15: Text-to-text, text → new text."),
    mcq(U2, "N1 p.15", "슬라이드가 말한 '2026 년의 반전' 은?", ["LLM 하나가 프롬프트 하나로 모든 과제를 한다", "NLP 과제가 사라졌다", "규칙 기반이 돌아왔다", "번역이 불가능해졌다"], 0, "p.15: one LLM now does ALL of these from a single prompt."),
    # ---- 1-3
    mcq(U3, "N1 p.12", "슬라이드가 NLP 의 핵심 어려움(THE core difficulty)이라고 한 것은?", ["중의성", "속도", "저장 공간", "맞춤법"], 0, "p.12: Ambiguity is THE core difficulty of NLP.", "강조"),
    mcq(U3, "N1 p.12", "'I saw a man with a telescope' 는 어떤 층의 중의성?", ["구조", "단어", "띄어쓰기", "화용"], 0, "망원경을 누가 들었는지, 문장 구조가 두 가지로 읽혀요."),
    mcq(U3, "N1 p.12", "'배' 가 과일, 배, 몸의 배로 읽히는 것은?", ["단어 수준 중의성", "구조 중의성", "생략", "지시어 문제"], 0, "p.12 Word level 예예요. 영어 bank 도 같아요."),
    mcq(U3, "N1 p.13", "'잘~한다' 가 칭찬일 수도 비꼼일 수도 있는 문제는?", ["화용론(Pragmatics)", "지시어(Reference)", "생략(Ellipsis)", "형태소"], 0, "p.13: Pragmatics, identical words, opposite meanings."),
    mcq(U3, "N1 p.13", "'밥 먹었어?' 가 보여 주는 한국어의 특징은?", ["생략", "높임법", "교착어", "띄어쓰기"], 0, "p.13: Ellipsis, no subject, no object."),
    mcq(U3, "N1 p.13", "트로피와 가방 문장에서 big 을 small 로 바꾸면 생기는 일은?", ["'it' 이 가리키는 대상이 바뀐다", "문장이 틀린다", "번역이 불가능해진다", "아무 변화 없다"], 0, "p.13: swap big → small and the answer flips. 세상 지식이 필요해요 (Winograd)."),
    # ---- 1-4
    mcq(U4, "N1 p.14", "한국어를 가리키는 말로 슬라이드에 나온 것은?", ["교착어(agglutinative)", "고립어", "굴절어", "포합어"], 0, "p.14: Korean is agglutinative."),
    mcq(U4, "N1 p.14", "'먹었겠더라' 를 먹-, -었-, -겠-, -더라 로 나누면 각각을 무엇이라 하나요?", ["형태소", "문장", "토큰 ID", "어휘 크기"], 0, "뜻을 가진 가장 작은 조각이 형태소예요."),
    mcq(U4, "N1 p.14", "먹어 / 드세요 / 잡수세요 가 보여 주는 것은?", ["높임법", "띄어쓰기", "생략", "중의성"], 0, "p.14 Honorifics: same fact, different social meaning."),
    mcq(U4, "N1 p.14", "한국어 LLM(EXAONE, HyperCLOVA X)이 따로 있는 까닭으로 슬라이드가 든 것은?", ["한국어는 한국어에 맞춘 주의가 필요해서", "영어 모델이 불법이라서", "한국어 데이터가 가장 많아서", "GPU 가 달라서"], 0, "p.14: Korean needs native attention."),
    # ---- 1-5
    mcq(U5, "N1 p.17", "1947 년 Warren Weaver 가 상상한 기계 번역은 무엇에 비유되었나요?", ["암호 풀기", "그림 그리기", "음악 연주", "체스"], 0, "'이건 영어인데 이상한 기호로 암호화됐을 뿐, 이제 해독하겠다.' 기계 번역을 code-breaking 으로 봤어요."),
    mcq(U5, "N1 p.17", "1954 년 Georgetown-IBM 시연의 내용은?", ["러시아어 60문장을 영어로 번역", "첫 챗봇 공개", "AI 라는 이름 붙이기", "n-gram 발표"], 0, "p.17: 60 Russian sentences → English, '5년 안에 해결' 이라 했지만 그렇지 않았어요."),
    mcq(U5, "N1 p.17", "인공지능(Artificial Intelligence)이라는 이름이 생긴 사건은?", ["1956 Dartmouth 여름 워크숍", "1950 Turing 논문", "1966 ELIZA", "2017 트랜스포머"], 0, "p.17: the field gets its name."),
    mcq(U5, "N1 p.18", "1966 년 MIT 의 첫 챗봇 ELIZA 는 어떤 방식이었나요?", ["약 200개 패턴 매칭 규칙", "신경망", "통계 번역", "트랜스포머"], 0, "p.18: ~200 pattern-matching rules playing a psychotherapist."),
    mcq(U5, "N1 p.19", "통계 시대의 뿌리로 슬라이드가 든 것은?", ["Shannon 1948 잡음 채널 모델", "ELIZA", "Firth 1957", "BERT"], 0, "p.19: communication as probability, the noisy channel model."),
    mcq(U5, "N1 p.19", "Jelinek 의 유명한 말이 뜻하는 것은?", ["규칙(언어학)보다 데이터가 성능을 올렸다", "언어학이 가장 중요하다", "통계는 쓸모없다", "번역은 불가능하다"], 0, "'Every time I fire a linguist, the performance goes up'. 데이터가 규칙을 이긴 시대예요."),
    mcq(U5, "N1 p.19", "2막 통계의 한계로 슬라이드가 든 것은?", ["cat 과 kitten 이 관련 있다는 것을 세기만으로는 모른다", "데이터가 없다", "계산이 너무 빠르다", "규칙이 너무 적다"], 0, "counts cannot see that cat and kitten are related, no notion of meaning."),
    # ---- 1-6
    mcq(U6, "N1 p.20", "'You shall know a word by the company it keeps' 를 한 사람과 해는?", ["Firth, 1957", "Turing, 1950", "Shannon, 1948", "Weaver, 1947"], 0, "p.20: Distributional hypothesis (Firth, 1957)."),
    mcq(U6, "N1 p.21", "seq2seq(2014)에서 원문을 압축하는 부분은?", ["인코더", "디코더", "어텐션", "토크나이저"], 0, "encoder compresses the source, decoder writes the target."),
    mcq(U6, "N1 p.21", "어텐션(2015)이 한 일은?", ["디코더가 필요할 때 원문을 다시 돌아보게 했다", "단어를 벡터로 만들었다", "규칙을 없앴다", "GPU 를 만들었다"], 0, "p.21: attention lets the decoder glance back at the source as needed."),
    mcq(U6, "N1 p.22", "트랜스포머가 GPU 에서 크게 키우기 좋은 까닭은?", ["모든 단어를 병렬로 처리해서", "순환이 있어서", "규칙을 써서", "데이터가 적어서"], 0, "p.22: processes all words in parallel → scales beautifully on GPUs."),
    mcq(U6, "N1 p.22", "2018 년 '한 생각의 두 반쪽' 이라고 한 두 모델은?", ["BERT 와 GPT", "ELIZA 와 SHRDLU", "word2vec 과 GloVe", "RNN 과 LSTM"], 0, "p.22: 2018 BERT & GPT, two halves of one idea."),
    mcq(U6, "N1 p.23", "GPT-3(2020)의 특징으로 슬라이드가 든 것은?", ["프롬프트에 예시 몇 개만 보여 주면 과제를 한다(in-context learning)", "라벨 달린 데이터만으로 학습", "규칙 200개", "음성만 처리"], 0, "p.23: in-context learning."),
    mcq(U6, "N1 p.23", "ChatGPT(2022)에 더해진 것으로 슬라이드가 든 것은?", ["instruction tuning 과 RLHF", "n-gram", "형태소 분석기", "SHRDLU"], 0, "p.23: + instruction tuning + RLHF → 100M users in two months."),
    mcq(U6, "N1 p.24", "70 년 역사의 공통 패턴으로 슬라이드가 말한 것은?", ["막이 바뀔수록 사람이 적는 지식은 줄고 데이터에서 배우는 것은 늘었다", "규칙이 점점 늘었다", "데이터가 점점 줄었다", "중의성 문제가 해결되었다"], 0, "p.24: Each act hard-codes less human knowledge and learns more from data. 중의성이라는 핵심 어려움은 그대로예요."),
]
OX_B = [
    ox(U1, "N1 p.6", "이 과목에는 중간고사가 있다.", False, "No midterm. 8주차는 텀 프로젝트 제안이에요."),
    ox(U1, "N1 p.8", "프로그래밍 과제는 성적의 40% 이다.", True, "p.8: Programming assignments 40%."),
    ox(U1, "N1 p.8", "기말고사는 성적의 25% 이다.", False, "기말고사는 30%, 텀 프로젝트가 25% 예요."),
    ox(U1, "N1 p.8", "AI 도구를 쓰면 사용 사실을 밝혀야 한다.", True, "p.8: declare usage, write in your own words."),
    ox(U2, "N1 p.10", "Python 은 자연어의 한 종류이다.", False, "p.10: not Python, not logic."),
    ox(U2, "N1 p.10", "NLU 는 글에서 뜻을 알아내고, NLG 는 글을 만들어 낸다.", True, "understanding in, generation out."),
    ox(U2, "N1 p.15", "감정 분석은 글 → 라벨 모양의 분류 과제이다.", True, "p.15: Classification, spam, sentiment, topic."),
    ox(U2, "N1 p.15", "개체명 인식은 텍스트-투-텍스트 과제이다.", False, "개체명 인식은 토큰마다 태그를 붙이는 시퀀스 라벨링이에요."),
    ox(U3, "N1 p.12", "사람도 중의성을 풀 때 늘 의식적으로 고민한다.", False, "p.12: humans disambiguate without noticing."),
    ox(U3, "N1 p.12", "'아버지가방에들어가신다' 는 띄어쓰기에 따라 뜻이 달라지는 예이다.", True, "아버지가 방에 / 아버지 가방에."),
    ox(U3, "N1 p.13", "지구에는 7,000 개 넘는 언어가 있고 대부분 데이터가 풍부하다.", False, "대부분 데이터가 거의 없어요(low-resource NLP)."),
    ox(U3, "N1 p.13", "갓생, 억텐 같은 새 말이 계속 생기는 것도 NLP 를 어렵게 한다.", True, "Language never sits still."),
    ox(U4, "N1 p.14", "한국어 동사는 영어 동사보다 모양이 훨씬 적다.", False, "영어는 몇 가지, 한국어 동사는 수천 가지 모양이에요."),
    ox(U4, "N1 p.14", "실제 한국어 글에서는 띄어쓰기가 잘 지켜지지 않을 때가 많다.", True, "Spacing is unreliable in real text."),
    ox(U4, "N1 p.14", "한국어는 어순이 자유롭고 주어를 자주 뺀다.", True, "Flexible word order, frequent subject drop."),
    ox(U5, "N1 p.17", "1950 년 Alan Turing 은 대화를 지능의 시험으로 제안했다.", True, "Can machines think? conversation becomes the test."),
    ox(U5, "N1 p.18", "ALPAC 보고서 뒤 미국의 기계 번역 지원은 더 늘었다.", False, "US funding frozen for a decade."),
    ox(U5, "N1 p.19", "n-gram 언어 모델은 앞 단어들로 다음 단어의 확률을 센다.", True, "P(next word | previous words)."),
    ox(U6, "N1 p.20", "word2vec 은 라벨이 달린 데이터가 꼭 필요하다.", False, "learned from raw text, no labels needed."),
    ox(U6, "N1 p.22", "트랜스포머는 순환(recurrence)을 핵심으로 쓴다.", False, "attention everywhere, no recurrence."),
    ox(U6, "N1 p.21", "2016 년 구글 번역은 신경망 번역으로 바뀌었다.", True, "p.21."),
    ox(U6, "N1 p.23", "ChatGPT 는 두 달 만에 사용자 1억 명에 이르렀다.", True, "100M users in two months, fastest ever."),
]
SH_B = [
    short(U1, "N1 p.8", "이 과목의 기말고사 비율은 몇 % 인가요? (숫자만)", ["30"], "Final exam 30%.", num=True),
    short(U1, "N1 p.6", "중간고사 대신 8주차에 발표하는 것은? (두 단어)", ["텀 프로젝트 제안", "텀프로젝트 제안", "프로젝트 제안", "term project proposal"], "p.6."),
    short(U2, "N1 p.10", "글 → 뜻 쪽, 자연어 '이해' 의 영어 줄임말은?", ["NLU", "Natural Language Understanding"], "Natural Language Understanding."),
    short(U2, "N1 p.10", "뜻 → 글 쪽, 자연어 '생성' 의 영어 줄임말은?", ["NLG", "Natural Language Generation"], "Natural Language Generation."),
    short(U3, "N1 p.12", "같은 글이 여러 뜻을 가지는 성질, NLP 의 핵심 어려움은?", ["중의성", "Ambiguity", "모호성"], "p.12."),
    short(U3, "N1 p.13", "주어와 목적어를 문맥에 맡기고 빼는 현상은?", ["생략", "Ellipsis"], "'밥 먹었어?'"),
    short(U4, "N1 p.14", "뜻을 가진 가장 작은 말 조각은?", ["형태소", "Morpheme"], "먹-, -었-, -겠-, -더라."),
    short(U4, "N1 p.14", "낱말 뒤에 조각을 붙여 뜻을 만드는 한국어 같은 언어 유형은?", ["교착어", "agglutinative", "Agglutinative Language", "첨가어"], "p.14."),
    short(U5, "N1 p.18", "1966 년 MIT 의 첫 챗봇 이름은?", ["ELIZA", "엘리자"], "p.18."),
    short(U5, "N1 p.17", "인공지능이라는 이름이 생긴 1956 년 워크숍의 장소(대학) 이름은?", ["Dartmouth", "다트머스"], "p.17."),
    short(U5, "N1 p.19", "앞 n-1 개 단어로 다음 단어 확률을 세는 통계 언어 모델은?", ["n-gram", "엔그램", "ngram"], "p.19."),
    short(U6, "N1 p.20", "2013 년 단어마다 벡터를 날 글에서 배운 방법은?", ["word2vec", "워드투벡"], "p.20."),
    short(U6, "N1 p.22", "2017 년 'Attention Is All You Need' 에서 나온 모델은?", ["Transformer", "트랜스포머"], "p.22."),
    short(U6, "N1 p.21", "인코더가 원문을 압축하고 디코더가 새 글을 쓰는 2014 년 구조는?", ["seq2seq", "sequence to sequence", "시퀀스 투 시퀀스"], "p.21."),
    short(U6, "N1 p.23", "파라미터, 데이터, 계산을 늘리면 성능이 예측대로 좋아진다는 법칙은?", ["스케일링 법칙", "Scaling Laws", "scaling law"], "p.23."),
]
ES_B = [
    essay(U2, "N1 p.10", "NLU 와 NLG 의 차이를 예를 들어 설명하시오.", "NLU(자연어 이해)는 글을 받아 의도, 대상, 사실 같은 뜻을 알아내는 쪽이고 NLG(자연어 생성)는 뜻에서 새 글을 만들어 내는 쪽이다. 예를 들어 '내일 부산 가는 KTX 몇 시야?' 에서 의도=열차 시간, 목적지=부산, 날짜=내일을 뽑는 것은 NLU, '내일 부산행 첫 KTX 는 05:13 입니다' 를 쓰는 것은 NLG 이다.",
          ["NLU 는 글 → 뜻", "NLG 는 뜻 → 글", "NLU 예: 분류, 추출, 검색, 답", "NLG 예: 쓰기, 요약, 응답", "KTX 예시나 비슷한 예"], "NLU 와 NLG"),
    essay(U3, "N1 p.12-13", "자연어처리가 어려운 까닭을 중의성 중심으로 세 가지 예를 들어 설명하시오.", "같은 글이 여러 뜻을 가질 수 있는 중의성이 NLP 의 핵심 어려움이다. 단어 수준에서 '배' 는 과일, 배, 몸의 배가 될 수 있고, 구조 수준에서 'I saw a man with a telescope' 는 망원경을 든 사람이 둘로 읽히며, 띄어쓰기에 따라 '아버지가방에들어가신다' 의 뜻이 바뀐다. 이 밖에 지시어, 화용, 생략도 문맥과 세상 지식이 있어야 풀린다.",
          ["중의성이 핵심", "단어 중의성 예", "구조 중의성 예", "띄어쓰기 예", "문맥과 세상 지식 필요"], "중의성", "강조"),
    essay(U4, "N1 p.14", "한국어 NLP 가 어려운 까닭을 네 가지 쓰시오.", "첫째, 한국어는 교착어라서 한 어절에 형태소가 여러 개 붙고 동사가 수천 가지 모양이 되어 형태소 분석이 중요하다. 둘째, 실제 글에서 띄어쓰기가 잘 지켜지지 않고 띄어쓰기에 따라 뜻이 바뀐다. 셋째, 높임법 때문에 같은 사실도 여러 모양으로 말한다. 넷째, 어순이 자유롭고 주어를 자주 뺀다.",
          ["교착어", "형태소 분석 중요", "띄어쓰기", "높임법", "자유 어순과 주어 생략"], "한국어 NLP"),
    essay(U5, "N1 p.18-19", "1막 규칙 시대와 2막 통계 시대를 비교하고 각 시대의 교훈을 쓰시오.", "1막(1950~80년대)은 사람이 손으로 규칙과 문법을 만들었고 ELIZA, SHRDLU 가 대표다. 교훈은 언어를 손으로 다 적을 수 없고 규칙책은 끝없이 커져도 깨진다는 것이다. 2막(1990~2000년대)은 큰 말뭉치에서 패턴을 세는 n-gram 같은 통계 방법을 썼다. 교훈은 데이터가 규칙을 이기지만 단어를 세는 것은 이해가 아니라는 것이다(cat 과 kitten 의 관계를 모름).",
          ["규칙: 사람이 손으로 규칙", "ELIZA 등 예", "규칙 시대 교훈", "통계: 말뭉치에서 셈, n-gram", "통계 교훈: 데이터가 이김", "세기는 이해가 아님"], "규칙과 통계"),
    essay(U6, "N1 p.20-23", "word2vec 부터 LLM 까지의 흐름을 연도와 함께 설명하시오.", "2013 년 word2vec 은 날 글에서 단어 벡터를 배워 cat 과 kitten 을 이웃으로 만들었다. 2014 년 seq2seq 는 인코더와 디코더로 번역하고 2015 년 어텐션이 디코더가 원문을 다시 보게 했다. 2017 년 트랜스포머는 순환 없이 어텐션만 써서 병렬로 크게 키울 수 있었고, 2018 년 BERT 와 GPT 가 사전 학습 후 적응하는 방법을 열었다. 2020 년 GPT-3 는 스케일링과 in-context learning 을, 2022 년 ChatGPT 는 instruction tuning 과 RLHF 로 대중화를 이뤘다.",
          ["word2vec 2013", "seq2seq 2014", "어텐션 2015", "트랜스포머 2017", "BERT, GPT 2018 사전 학습", "GPT-3 2020", "ChatGPT 2022"], "신경망 NLP 흐름"),
    essay(U6, "N1 p.24", "70 년 NLP 역사를 관통하는 패턴 두 가지를 쓰시오.", "첫째, 막이 바뀔수록 사람이 적어 넣는 지식은 줄고 데이터에서 배우는 것은 늘었다(규칙 → 통계 → 신경망 → 사전 학습 → LLM). 둘째, 모든 막은 중의성이라는 같은 핵심 어려움에 대한 새 답이었다.",
          ["사람이 적는 지식 감소", "데이터에서 배우는 것 증가", "다섯 막 순서", "중의성에 대한 새 답"], "역사의 패턴"),
]
CALC_B = [
    calc(U1, "N1 p.8", "성적이 출석 5%, 과제 40%, 텀 프로젝트 25%, 기말고사 30% 일 때 텀 프로젝트와 기말고사를 합친 비율(%)은?", "두 항목을 더해요.",
         [{"label": "합(%)", "ans": 55, "tol": 0}], ["텀 프로젝트 25%", "기말고사 30%", "25 + 30 = 55"], "55%", "과제 40% 와 섞지 않게 조심해요. 교수님은 이 55% 를 더 신경 쓰라고 했어요.", "성적 비율"),
]

H = [
    mcq(U1, "N1 p.8, OT 녹음", "교수님이 OT 에서 '더 신경 써 달라' 고 한 쪽과 그 까닭은?", ["기말고사와 팀 프로젝트, 합치면 55% 로 과제 40% 보다 커서", "과제, 한 항목으로 가장 커서", "출석, 매주 있어서", "중간고사, 가장 먼저라서"], 0, "OT 녹음: 과제는 40% 지만 기말고사와 팀 프로젝트 합 55% 가 더 크니 그쪽을 더 신경 써 달라.", "강조"),
    mcq(U2, "N1 p.10", "'내일 부산 가는 KTX 몇 시야?' 에 답하는 시스템의 흐름으로 옳은 것은?", ["NLU 로 의도와 목적지, 날짜를 뽑고 NLG 로 안내문을 쓴다", "NLG 로 의도를 뽑고 NLU 로 안내문을 쓴다", "번역만 한다", "분류만 한다"], 0, "글 → 뜻(NLU), 뜻 → 글(NLG)."),
    mcq(U2, "N1 p.15", "슬라이드가 LLM 시대에도 부품을 이해하는 엔지니어가 필요하다고 한 까닭은?", ["전체 시스템을 만들고, 평가하고, 고치는 사람이 그들이라서", "LLM 이 과제를 못 해서", "규칙이 필요해서", "GPU 가 부족해서"], 0, "p.15: the engineers who understand the parts are the ones who build, evaluate, and fix the whole."),
    mcq(U3, "N1 p.13", "트로피-가방 문장(Winograd)이 보여 주는 가장 중요한 점은?", ["단어만으로 부족하고 세상 지식이 필요하다", "띄어쓰기가 중요하다", "번역은 불가능하다", "영어는 쉽다"], 0, "big/small 하나로 답이 뒤집혀서, 크기에 대한 세상 지식이 있어야 풀려요."),
    mcq(U3, "N1 p.12-13", "다음 중 '같은 글자, 다른 의도' 에 가장 가까운 것은?", ["잘~한다 (칭찬 / 비꼼)", "배 (과일 / 배)", "아버지가방에", "밥 먹었어?"], 0, "글자 뜻은 같은데 상황 속 의도가 반대인 것은 화용론이에요. 배는 단어 중의성이에요."),
    mcq(U4, "N1 p.14", "영어 중심 모델로 한국어를 다룰 때 형태소 분석이 특히 중요한 까닭은?", ["한 어절에 형태소가 여러 개 붙어 동사 모양이 수천 가지라서", "한국어는 단어가 적어서", "한국어는 띄어쓰기가 완벽해서", "높임법이 없어서"], 0, "교착어라서 한 어절이 여러 형태소로 이뤄져요."),
    mcq(U5, "N1 p.17-18", "시간 순서로 옳은 것은?", ["Weaver 메모 → Turing → Georgetown-IBM → Dartmouth → ELIZA", "Turing → Weaver → Dartmouth → Georgetown-IBM → ELIZA", "ELIZA → Weaver → Turing → Dartmouth → Georgetown-IBM", "Georgetown-IBM → Weaver → Turing → ELIZA → Dartmouth"], 0, "1947, 1950, 1954, 1956, 1966 순서예요."),
    mcq(U5, "N1 p.19", "통계 기계 번역이 IBM 에서 배운 데이터는?", ["의회 문장 쌍 수백만 개", "사람이 쓴 규칙 200개", "위키 문서 한 개", "음성 파일"], 0, "p.19: millions of parliament sentence pairs."),
    mcq(U5, "N1 p.18-20", "각 시대의 벽과 다음 시대의 답이 바르게 짝지어진 것은?", ["통계는 뜻을 모름 → word2vec 이 cat 과 kitten 을 이웃으로", "규칙이 너무 적음 → 통계", "벡터가 너무 큼 → 규칙", "데이터가 너무 많음 → ELIZA"], 0, "p.19 의 벽(no notion of meaning)을 p.20 에서 'The statistical wall falls' 라고 해요."),
    mcq(U6, "N1 p.21-22", "RNN seq2seq 와 트랜스포머의 차이로 옳은 것은?", ["RNN 은 단어를 차례로 읽고, 트랜스포머는 순환 없이 병렬로 처리한다", "트랜스포머가 단어를 하나씩 읽는다", "둘 다 규칙 기반이다", "RNN 은 어텐션만 쓴다"], 0, "p.21 RNN read word by word, p.22 no recurrence, parallel."),
    mcq(U6, "N1 p.22", "'NLP 의 ImageNet 순간' 이 뜻하는 것은?", ["언어를 한 번 배우고 어디서나 다시 쓴다(사전 학습 후 적응)", "이미지 처리로 넘어갔다", "라벨 데이터가 더 필요해졌다", "번역이 끝났다"], 0, "learn language once, reuse it everywhere."),
    mcq(U6, "N1 p.23", "5막 LLM 의 흐름을 바르게 이은 것은?", ["스케일링 법칙 → GPT-3 in-context learning → ChatGPT 의 instruction tuning 과 RLHF", "RLHF → n-gram → ELIZA", "word2vec → ELIZA → GPT-3", "SHRDLU → BERT → ALPAC"], 0, "p.23 순서예요."),
    mcq(U6, "N1 p.24", "Neural LM(Bengio 2003)처럼 막의 경계에 걸친 사건이 보여 주는 것은?", ["시대 구분은 대략적인 흐름이고 기술은 겹쳐 발전한다", "슬라이드가 틀렸다", "Bengio 는 규칙 시대 사람이다", "신경망은 2013 년에 처음 나왔다"], 0, "p.24 표에서 2003 년 신경망 LM 이 통계 막 칸에 있어요. 흐름은 겹쳐요."),
    mcq(U1, "N1 p.6", "슬라이드 p.6 의 휴강 표시에서 헷갈리는 점은?", ["표는 6주차에 휴강을, 아래 문구와 15주차는 W5 보강을 적었다", "휴강이 없다", "보강이 16주차다", "8주차가 휴강이다"], 0, "표(6주차 휴강 → W15 보강)와 아래 문구(W5)가 달라요. 공지를 확인해요."),
    mcq(U2, "N1 p.11", "음성 비서(시리야, 헤이 구글)에서 NLP 가 맡는 부분은?", ["말을 글로 바꾼 뒤 무슨 뜻인지 알아내는 부분", "마이크 하드웨어", "배터리 관리", "화면 밝기"], 0, "p.11: speech becomes text, then NLP figures out what you meant."),
]
OX_H = [
    ox(U1, "N1 p.8", "한 항목만 보면 과제가 가장 크지만, 기말고사와 텀 프로젝트를 합치면 과제보다 크다.", True, "40% < 25% + 30% = 55%.", "강조"),
    ox(U2, "N1 p.10", "번역은 NLU 만 필요하고 NLG 는 필요 없다.", False, "원문을 이해(NLU)하고 새 글을 써야(NLG) 해요."),
    ox(U3, "N1 p.13", "Winograd 문장에서 big 을 small 로 바꿔도 'it' 이 가리키는 대상은 같다.", False, "답이 뒤집혀요."),
    ox(U3, "N1 p.12", "중의성은 트랜스포머가 나오면서 완전히 해결되었다.", False, "p.24: the core difficulty never changed. 모든 막이 새 답일 뿐이에요."),
    ox(U4, "N1 p.14", "높임법은 같은 사실에 다른 사회적 뜻을 담는다.", True, "same fact, different social meaning."),
    ox(U5, "N1 p.17", "Georgetown-IBM 시연 때 '5년 안에 해결' 이라던 기계 번역은 실제로 5년 안에 해결되었다.", False, "…not quite. 1966 ALPAC 보고서가 어렵다고 했어요."),
    ox(U5, "N1 p.19", "통계 시대에도 스팸 필터, 품사 태거, 음성 인식, 검색 같은 제품이 조용히 쓰였다.", True, "Statistics quietly ships."),
    ox(U6, "N1 p.20", "Seoul - Korea + Japan ≈ Tokyo 는 단어 벡터의 방향에 뜻이 담긴다는 예이다.", True, "Directions carry meaning."),
    ox(U6, "N1 p.24", "역사가 흐를수록 사람이 손으로 적어 넣는 지식이 늘었다.", False, "줄었어요. 데이터에서 배우는 것이 늘었어요."),
    ox(U6, "N1 p.23", "EXAONE, HyperCLOVA X 는 슬라이드가 든 한국어 LLM 이다.", True, "p.23."),
]
SH_H = [
    short(U1, "N1 p.8", "과제 비율(%)에서 기말고사 비율(%)을 빼면? (숫자)", ["10"], "40 - 30 = 10.", num=True),
    short(U3, "N1 p.13", "트로피-가방처럼 대명사가 가리키는 대상을 세상 지식으로 풀어야 하는 문장 모음의 이름(사람 이름)은?", ["Winograd", "위노그라드", "Winograd Schema"], "p.13."),
    short(U3, "N1 p.13", "데이터가 거의 없는 언어를 다루는 NLP 를 영어로 무엇이라 하나요?", ["low-resource NLP", "low-resource", "저자원 NLP", "저자원"], "p.13."),
    short(U5, "N1 p.19", "통신을 확률로 본 Shannon 의 1948 년 모델 이름은?", ["잡음 채널 모델", "noisy channel model", "noisy channel"], "p.19."),
    short(U5, "N1 p.18", "기계 번역 지원을 10년 동결시킨 1966 년 보고서는?", ["ALPAC", "ALPAC report", "알팩"], "p.18."),
    short(U6, "N1 p.23", "GPT-3 에서 프롬프트에 예시 몇 개를 보여 주어 과제를 하게 하는 능력은?", ["in-context learning", "인컨텍스트 학습", "문맥 내 학습"], "p.23."),
    short(U6, "N1 p.23", "ChatGPT 에 더해진, 사람 피드백으로 하는 강화 학습의 줄임말은?", ["RLHF"], "p.23."),
    short(U6, "N1 p.20", "'단어는 함께 다니는 단어로 안다' 는 생각의 이름은?", ["분포 가설", "distributional hypothesis"], "p.20."),
]
ES_H = [
    essay(U3, "N1 p.12-13, p.24", "'모든 시대가 중의성에 대한 새 답이었다' 는 말을 규칙, 통계, 신경망 시대를 예로 들어 설명하시오.", "중의성은 NLP 의 핵심 어려움이고 시대마다 다르게 답했다. 규칙 시대는 사람이 규칙으로 뜻을 정하려 했지만 예외가 끝없었다. 통계 시대는 말뭉치에서 앞뒤 단어를 세어 가장 그럴듯한 뜻을 골랐지만 뜻 자체는 몰랐다. 신경망 시대는 단어를 벡터로 나타내고 문맥에서 뜻을 배우게 해 비슷한 단어를 이웃으로 만들었고, 트랜스포머와 LLM 은 더 넓은 문맥을 보게 했다.",
          ["중의성이 핵심 어려움", "규칙의 답과 한계", "통계의 답과 한계", "신경망: 벡터와 문맥", "트랜스포머, LLM 은 넓은 문맥"], "중의성과 역사", "강조"),
    essay(U6, "N1 p.21-22", "RNN 기반 seq2seq 와 트랜스포머를 비교하시오.", "RNN 기반 seq2seq(2014)는 인코더가 원문을 단어 하나씩 읽어 압축하고 디코더가 번역문을 쓰며, 2015 년 어텐션으로 디코더가 원문을 다시 볼 수 있게 되었다. 트랜스포머(2017)는 순환을 없애고 어디서나 어텐션을 써서 모든 단어를 병렬로 처리하므로 GPU 에서 크게 키우기 좋다. 이것이 사전 학습 시대를 열었다.",
          ["seq2seq 인코더 디코더", "RNN 은 차례로 읽음", "어텐션 2015", "트랜스포머 순환 없음", "병렬 처리, GPU 확장", "사전 학습으로 이어짐"], "seq2seq 와 트랜스포머"),
    essay(U4, "N1 p.14, p.23", "한국어 LLM 이 따로 개발되는 까닭을 한국어의 특징과 연결해 서술하시오.", "한국어는 교착어라서 한 어절에 형태소가 여러 개 붙고 동사 모양이 수천 가지이며, 띄어쓰기가 불안정하고 높임법, 자유 어순, 주어 생략이 많다. 영어 중심으로 학습한 모델은 이런 특징을 잘 다루지 못하므로 한국어에 맞춘 주의가 필요하다. 그래서 EXAONE, HyperCLOVA X 같은 한국어 LLM 이 만들어진다.",
          ["교착어와 형태소", "띄어쓰기", "높임법", "어순과 생략", "영어 중심 모델의 한계", "EXAONE, HyperCLOVA X"], "한국어 LLM"),
    essay(U1, "N1 p.4-8", "이 과목의 목표와 평가 방식을 요약하고, 시험 준비에서 우선할 것을 쓰시오.", "이 과목은 토큰화부터 트랜스포머, LLM 학습, RAG, 에이전트까지 다루며 NLP 기본 개념, 어텐션과 트랜스포머, 구현과 미세 조정, 한국어 NLP 시스템 설계와 평가를 목표로 한다. 평가는 출석 5%, 프로그래밍 과제 40%, 텀 프로젝트 25%, 기말고사 30% 이고 중간고사는 없다. 교수님은 텀 프로젝트와 기말고사 합 55% 를 더 신경 쓰라고 했다.",
          ["다루는 범위", "목표", "비율 네 가지", "중간고사 없음", "55% 강조"], "과목 운영", "강조"),
    essay(U2, "N1 p.15", "NLP 과제 다섯 가지를 입력과 출력 모양과 함께 쓰시오.", "분류는 글 → 라벨(스팸, 감정), 시퀀스 라벨링은 토큰마다 → 태그(품사, 개체명), 텍스트-투-텍스트는 글 → 새 글(번역, 요약), 검색과 질의응답은 알맞은 문서를 찾아 답을 뽑거나 쓰고, 대화와 생성은 문맥 → 응답(챗봇, 글쓰기 도우미)이다.",
          ["분류", "시퀀스 라벨링", "텍스트-투-텍스트", "검색과 QA", "대화와 생성", "입출력 모양"], "NLP 과제"),
]
CALC_H = [
    calc(U5, "N1 p.17, p.23", "Weaver 의 기계 번역 메모(1947)부터 ChatGPT(2022)까지 몇 년인가?", "두 연도의 차를 구해요.",
         [{"label": "햇수", "ans": 75, "tol": 0}], ["ChatGPT 2022", "Weaver 메모 1947", "2022 - 1947 = 75"], "75년", "Turing(1950)과 헷갈리지 않게 해요.", "연도 계산"),
    calc(U6, "N1 p.20, p.22", "word2vec(2013)에서 트랜스포머(2017)까지 몇 년인가?", "두 연도의 차.",
         [{"label": "햇수", "ans": 4, "tol": 0}], ["트랜스포머 2017", "word2vec 2013", "2017 - 2013 = 4"], "4년", "seq2seq(2014)와 어텐션(2015)이 그 사이에 있어요.", "연도 계산"),
]

basic = mk("basic", B + OX_B + SH_B + ES_B + CALC_B)
hard = mk("hard", H + OX_H + SH_H + ES_H + CALC_H)
for name, arr in (("w1_basic.json", basic), ("w1_hard.json", hard)):
    raw = json.dumps(arr, ensure_ascii=False, indent=1)
    for ch in ("—", "–", "·"):
        assert ch not in raw
    (W / name).write_text(raw, encoding="utf-8")
    print(name, len(arr))
