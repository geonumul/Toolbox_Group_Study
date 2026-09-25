# -*- coding: utf-8 -*-
"""자연어처리 subject.json 생성"""
import json, pathlib
W = pathlib.Path(__file__).resolve().parent
PDF = "../../01_수업자료/자연어처리/강의자료/"
cfg = {
    "slug": "nlp",
    "name": "자연어처리",
    "brand": "자연어처리 회독",
    "key": "sdt_nlp_v1",
    "eyebrow": "자연어처리 2026-2학기",
    "intro": "수학이나 머신러닝을 몰라도 괜찮아요. 기초 다지기에서 벡터, 확률, 신경망, 파이썬을 먼저 익히고, 주차 순서대로 강의와 실습을 봐요. 영어 슬라이드는 한국어로 풀어 주고, 영어 용어는 뜻과 함께 계속 반복해요.",
    "pathLabel": "기초, 주차별 강의와 실습, 시험",
    "examLabel": "기말고사",
    "mockDesc": "기말고사 형식은 아직 공지가 없어요. 객관식, O/X, 단답, 서술, 계산, 코드 읽기를 골고루 섞었어요. 먼저 오답노트에서 틀린 것을 다시 풀고 오면 좋아요.",
    "bgLabel": "기초 다지기 복습",
    "sentLabel": "시험 답안에 쓸 문장",
    "weeks": [
        {"id": "b", "short": "기초 다지기", "title": "벡터, 확률, 신경망, 파이썬 처음부터", "deck": None,
         "topics": "벡터와 행렬, 내적과 코사인 유사도, 로그와 지수, 확률과 조건부 확률, 소프트맥스, 함수와 미분, 경사 하강법, 신경망이 뭔지, 손실 함수, 파이썬과 PyTorch 기초"},
        {"id": "1", "short": "1주차", "title": "강의 소개와 자연어처리의 역사", "deck": "N1",
         "topics": "강의 운영과 평가, 자연어처리란, 언어가 어려운 이유(중의성), 규칙 기반에서 통계, 신경망, 트랜스포머, LLM까지의 역사"},
        {"id": "2", "short": "2주차", "title": "토큰화와 단어 벡터", "deck": "N2",
         "topics": "토큰화(Tokenization), BPE, 한국어 토큰화와 fertility, 원-핫 벡터와 분포 가설, word2vec(skip-gram, 소프트맥스, 네거티브 샘플링), 카운트 기반과 GloVe, 단어 벡터 평가"},
        {"id": "2L", "short": "2주차 실습", "title": "Lab 0-1 토큰화와 단어 벡터 코드 읽기", "deck": "N2L",
         "topics": "Colab과 GPU, 텐서, Hugging Face pipeline, BPE 직접 구현, fertility 재기, 한국어 토크나이저 학습, word2vec 학습과 유사도, 유추, PCA 그림"},
        {"id": "3", "short": "3주차", "title": "신경망 기초와 언어 모델", "deck": "N3",
         "topics": "뉴런과 층, 활성화 함수(ReLU), 행렬로 쓰는 신경망, 경사 하강법, 연쇄 법칙과 역전파, 계산 그래프, 언어 모델과 다음 토큰 예측, n-gram, perplexity, 고정 윈도우 신경망 LM, RNN, 기울기 소실과 LSTM"},
        {"id": "3L", "short": "3주차 실습", "title": "Lab 2 신경망과 RNN 언어 모델 코드 읽기", "deck": "N3L",
         "topics": "shape 찍어 보기, autograd, 문자 단위 RNN 언어 모델, 학습 루프, 텍스트 생성, perplexity, 토크나이저 바꾸기"},
        {"id": "4", "short": "4주차", "title": "어텐션과 트랜스포머 구조", "deck": "N4",
         "topics": "고정 벡터 병목, 어텐션, Query/Key/Value, 셀프 어텐션, 스케일드 닷프로덕트, 멀티헤드, 위치 인코딩, 잔차 연결과 층 정규화, 인코더와 디코더, 마스킹"},
        {"id": "4L", "short": "4주차 실습", "title": "Lab 3 셀프 어텐션 직접 만들기 코드 읽기", "deck": "N4L",
         "topics": "Q, K, V 만들기, 점수와 스케일링, 소프트맥스, 가중합, 마스킹, 멀티헤드, 트랜스포머 블록"},
        {"id": "P", "short": "참고 논문", "title": "논문 Attention Is All You Need 문단별 읽기", "deck": "NP",
         "topics": "교수님이 4주차에 꼭 읽으라고 한 논문(Vaswani et al. 2017). 초록부터 결론까지 문단 하나하나를 4주차 슬라이드와 짝지어 읽어요. 인코더 디코더 스택, 스케일드 닷프로덕트, 멀티 헤드, 위치별 FFN, 위치 인코딩, Why Self-Attention 표, 학습 설정, BLEU 결과와 ablation"},
    ],
    "decks": {
        "N1": {"title": "1강 Course Introduction and History of NLP", "week": "1", "pdf": PDF + "01주차_Course Introduction and History of NLP.pdf"},
        "N2": {"title": "2강 Tokenization and Word Vectors", "week": "2", "pdf": PDF + "02주차_Tokenization and Word Vectors.pdf"},
        "N2L": {"title": "Lab 0-1 Tokenization and Word Vectors (코드)", "week": "2L"},
        "N3": {"title": "3강 Neural NLP Foundations", "week": "3", "pdf": PDF + "03주차_Neural NLP Foundations.pdf"},
        "N3L": {"title": "Lab 2 Neural Nets and RNN Language Models (코드)", "week": "3L"},
        "N4": {"title": "4강 Attention and the Transformer Architecture", "week": "4", "pdf": PDF + "04주차_Attention and the Transformer Architecture.pdf"},
        "N4L": {"title": "Lab 3 Self-Attention from Scratch (코드)", "week": "4L"},
        "NP": {"title": "참고 논문 Attention Is All You Need (Vaswani et al. 2017)", "week": "P", "pdf": "../../01_수업자료/자연어처리/기출과참고/참고_Attention Is All You Need.pdf"},
    },
    "prereq": {},
    "passes": [
        {"n": 1, "t": "큰 그림", "d": "수학 없이, 이 슬라이드(실습 칸)가 무슨 이야기인지만"},
        {"n": 2, "t": "흐름과 뜻", "d": "영어 용어 하나하나의 뜻과, 무엇이 무엇으로 이어지는지"},
        {"n": 3, "t": "자세히", "d": "슬라이드를 짚으며 식, 숫자, 예시, 교수님 설명까지. 실습은 코드 한 줄씩"},
        {"n": 4, "t": "시험", "d": "확인 퀴즈, 시험에 나올 포인트, 외워 쓸 답안 문장, 헷갈리는 점"},
    ],
    "mock": {"mcq": 20, "ox": 8, "short": 6, "essay": 3, "calc": 3},
    "examsNav": "직접 해보기",
    "examsDesc": "Colab 에서 빈칸을 채우며 손으로 해 보는 연습 노트북",
    "tipsNav": "답안 팁",
}
(W / "subject.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=1), encoding="utf-8")
print("ok")
