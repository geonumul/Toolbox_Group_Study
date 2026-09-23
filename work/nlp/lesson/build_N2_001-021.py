# 2강(N2) 회독 레슨 1~21쪽 생성기 (토큰화, 한국어 토큰화). 사용: python build_N2_001-021.py
# 출력: N2_001-021.json (같은 폴더)
import json, math, os, re, sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "N2_001-021.json")

MANTRA = "글을 토큰으로 자르고, 토큰을 벡터로 바꾸고, 벡터로 다음 토큰을 맞혀요."
W1 = "2주차 월요일 1교시"
W3 = "2주차 월요일 3교시 (실습)"

# =====================================================================
# 손계산 확인 (assert)
# =====================================================================
# p.6: 슬라이드의 바이트 EC 9E 90 EC 97 B0 는 사실 '자연' 두 글자다
assert "자연".encode("utf-8").hex(" ").upper() == "EC 9E 90 EC 97 B0"
assert "ChatGPT는".encode("utf-8")[:2].hex(" ").upper() == "43 68"
assert len("똑".encode("utf-8")) == 3 and len("C".encode("utf-8")) == 1

# p.8: 지프의 법칙 f = C / r, C = 10^6
C_ZIPF = 10 ** 6
assert C_ZIPF / 1 == 1_000_000 and C_ZIPF / 10 == 100_000 and C_ZIPF / 1000 == 1_000
assert C_ZIPF / 2 == 500_000

# p.9: 길이 5배 → 어텐션 계산 25배
assert 5 ** 2 == 25 and len("love") == 4 and len("I love NLP".split()) == 3


# p.12: BPE 손계산. 슬라이드 방식(</w> 를 마지막 글자에 붙임)과 실습 방식(</w> 따로) 둘 다 확인
def get_pair_counts(corpus):
    pairs = Counter()
    for word, freq in corpus.items():
        for i in range(len(word) - 1):
            pairs[(word[i], word[i + 1])] += freq
    return pairs


def merge_pair(corpus, pair):
    a, b = pair
    new = {}
    for word, freq in corpus.items():
        nw, i = [], 0
        while i < len(word):
            if i < len(word) - 1 and word[i] == a and word[i + 1] == b:
                nw.append(a + b)
                i += 2
            else:
                nw.append(word[i])
                i += 1
        new[tuple(nw)] = freq
    return new


def train_bpe(corpus, n):
    merges, counts = [], []
    for _ in range(n):
        p = get_pair_counts(corpus)
        best = max(p, key=p.get)
        merges.append(best)
        counts.append(p[best])
        corpus = merge_pair(corpus, best)
    return corpus, merges, counts


def bpe_tokenize(word, merges):
    sy = list(word) + ["</w>"]
    for a, b in merges:
        i = 0
        while i < len(sy) - 1:
            if sy[i] == a and sy[i + 1] == b:
                sy[i:i + 2] = [a + b]
            else:
                i += 1
    return sy


SLIDE = {("l", "o", "w</w>"): 5, ("l", "o", "w", "e", "r</w>"): 2,
         ("n", "e", "w", "e", "s", "t</w>"): 6, ("w", "i", "d", "e", "s", "t</w>"): 3}
assert sum(SLIDE.values()) == 16
p0 = get_pair_counts(SLIDE)
assert p0[("e", "s")] == 6 + 3 == 9 and p0[("s", "t</w>")] == 9
assert p0[("w", "e")] == 2 + 6 == 8 and p0[("l", "o")] == 5 + 2 == 7
assert p0[("n", "e")] == 6 and p0[("o", "w</w>")] == 5 and p0[("o", "w")] == 2
assert max(p0.values()) == 9
c1 = merge_pair(SLIDE, ("e", "s"))
p1 = get_pair_counts(c1)
assert p1[("es", "t</w>")] == 9 and max(p1.values()) == 9 and p1[("w", "e")] == 2
c2 = merge_pair(c1, ("es", "t</w>"))
p2 = get_pair_counts(c2)
assert p2[("l", "o")] == 7 and max(p2.values()) == 7
c3 = merge_pair(c2, ("l", "o"))
assert list(c3) == [("lo", "w</w>"), ("lo", "w", "e", "r</w>"), ("n", "e", "w", "est</w>"), ("w", "i", "d", "est</w>")]
p3 = get_pair_counts(c3)
# 슬라이드의 '...' 줄(low</w>, low e r</w>)은 빈도 순서 그대로가 아니다: 다음 1등은 6번짜리 쌍들
assert max(p3.values()) == 6 and p3[("lo", "w</w>")] == 5 and p3[("n", "e")] == 6 and p3[("w", "est</w>")] == 6
# 처음 어휘(글자 종류) 수
start_syms = sorted({s for w in SLIDE for s in w})
assert len(start_syms) == 11

LAB = {("l", "o", "w", "</w>"): 5, ("l", "o", "w", "e", "r", "</w>"): 2,
       ("n", "e", "w", "e", "s", "t", "</w>"): 6, ("w", "i", "d", "e", "s", "t", "</w>"): 3}
_, LAB_M, LAB_C = train_bpe(dict(LAB), 8)
assert LAB_M == [("e", "s"), ("es", "t"), ("est", "</w>"), ("l", "o"), ("lo", "w"),
                 ("n", "e"), ("ne", "w"), ("new", "est</w>")]
assert LAB_C == [9, 9, 9, 7, 7, 6, 6, 6]
assert bpe_tokenize("lowest", LAB_M) == ["low", "est</w>"]
assert bpe_tokenize("newer", LAB_M) == ["new", "e", "r", "</w>"]
assert bpe_tokenize("widow", LAB_M) == ["w", "i", "d", "o", "w", "</w>"]
# lowest 를 한 단계씩
_s = list("lowest") + ["</w>"]
assert len(_s) == 7


# p.14: 워드피스 점수(설명용 숫자) score = f(ab) / (f(a) f(b))
f_t, f_h, f_th = 1000, 1000, 400
f_q, f_u, f_qu = 300, 1000, 300
s_th = f_th / (f_t * f_h)
s_qu = f_qu / (f_q * f_u)
assert f_th > f_qu                      # BPE 는 th 를 먼저 붙인다
assert abs(s_th - 0.0004) < 1e-12 and abs(s_qu - 0.001) < 1e-12
assert s_qu > s_th and round(s_qu / s_th, 6) == 2.5   # 워드피스는 qu 를 먼저 붙인다

# p.15: 어휘 크기
assert 128 / 50 == 2.56 and 200 / 50 == 4

# p.17: 먹었겠더라 형태소 4개
assert ["먹", "었", "겠", "더라"] and "".join(["먹", "었", "겠", "더라"]) == "먹었겠더라"

# p.20: fertility 손계산
EN = "The weather is really nice today."
KO = "오늘은 날씨가 정말 좋네요."
assert len(EN.split()) == 6 and len(KO.split()) == 4
assert round(7 / 6, 2) == 1.17
assert 17 / 4 == 4.25 and 8 / 4 == 2.0
assert round(17 / 8, 2) == 2.12 and round(17 / 7, 2) == 2.43
assert 33 / 4 == 8.25 and 7 / 4 == 1.75
# 작은 예: '나는 학생이다' 가 [나, 는, 학생, 이다] 로 잘리면 4/2 = 2.0
assert 4 / len("나는 학생이다".split()) == 2.0
# p.21: 다국어 어휘 크기
assert 256 / 128 == 2


# =====================================================================
# 용어
# =====================================================================
# key: (ko, en(용어 사전 표기), 본문 괄호 안 표기, 받침) 받침 None 이면 ko 끝 글자로. 0 모음, 1 받침, 2 ㄹ받침
TERMS = {
    "nlp": ("자연어처리", "Natural Language Processing (NLP)", "NLP", None),
    "llm": ("대규모 언어 모델", "Large Language Model (LLM)", "LLM", None),
    "ntp": ("다음 토큰 예측", "Next Token Prediction", None, None),
    "wv": ("단어 벡터", "Word Vector", None, None),
    "tok": ("토큰", "Token", None, None),
    "tokid": ("토큰 ID", "Token ID", None, 0),
    "tokz": ("토큰화", "Tokenization", None, None),
    "tokr": ("토크나이저", "Tokenizer", None, None),
    "vocab": ("어휘", "Vocabulary", None, None),
    "corpus": ("말뭉치", "Corpus", None, None),
    "oov": ("미등록 단어", "Out-of-Vocabulary (OOV)", "OOV", None),
    "unk": ("미지 토큰", "[UNK]", None, None),
    "utf8": ("", "UTF-8", None, 2),
    "zipf": ("지프의 법칙", "Zipf's Law", None, None),
    "attn": ("어텐션", "Attention", None, None),
    "sub": ("서브워드", "Subword", None, None),
    "bpe": ("바이트 쌍 인코딩", "Byte Pair Encoding (BPE)", None, 0),
    "merge": ("병합 규칙", "Merge Rule", None, None),
    "blbpe": ("바이트 수준 BPE", "Byte-level BPE", None, 0),
    "wp": ("워드피스", "WordPiece", None, None),
    "uni": ("유니그램 토크나이저", "Unigram", None, None),
    "like": ("우도", "Likelihood", None, None),
    "spm": ("센텐스피스", "SentencePiece", None, None),
    "special": ("특수 토큰", "Special Token", None, None),
    "ctx": ("컨텍스트 창", "Context Window", None, None),
    "aggl": ("교착어", "Agglutinative Language", None, None),
    "morph": ("형태소", "Morpheme", None, None),
    "eojeol": ("어절", "", None, None),
    "analyzer": ("형태소 분석기", "Morphological Analyzer", None, None),
    "pos": ("품사 태그", "POS Tag", None, None),
    "fert": ("토큰 과다 분할", "Fertility", None, None),
}

GLOSS = {
    "nlp": ("컴퓨터가 사람 말을 알아듣고 만들어 내게 하는 분야",
            "글과 말을 컴퓨터가 다루게 하는 인공지능 분야예요. 요즘은 글을 토큰으로 자르고, 벡터로 바꾸고, 다음 토큰을 맞히는 흐름으로 풀어요."),
    "llm": ("아주 많은 글로 다음 토큰 맞히기를 배운 거대한 모델",
            "GPT, Claude, Llama, EXAONE 같은 모델이에요. 모두 서브워드 토큰으로 글을 잘라서 받아요."),
    "ntp": ("지금까지 나온 토큰을 보고 바로 다음 토큰을 맞히는 일",
            "현대 NLP 파이프라인의 마지막 화살표예요. 글 → 토큰 → 벡터 → 다음 토큰 예측."),
    "wv": ("단어 하나를 숫자 여러 개로 적은 지도 좌표",
           "뜻이 비슷한 단어는 가까운 좌표에 살게 만든 숫자 목록이에요. 2강 뒷부분(word2vec)에서 자세히 배워요."),
    "tok": ("모델이 글을 받는 가장 작은 조각, 레고 조각 하나",
            "단어일 수도, 글자일 수도, 그 사이 조각(서브워드)일 수도 있어요. 요즘 모델은 서브워드 조각을 써요."),
    "tokid": ("어휘 목록에서 그 토큰이 몇 번째인지 적은 번호",
              "신경망은 글자를 못 먹고 [8203, 318, ...] 같은 정수 번호 줄을 먹어요. 번호마다 벡터가 하나씩 붙어 있어요."),
    "tokz": ("글을 토큰 조각으로 자르는 일",
             "모든 NLP 시스템이 가장 먼저 내리는 결정이에요. 어떻게 자르느냐가 품질, 비용, 여러 언어 실력을 좌우해요."),
    "tokr": ("글 → 토큰 줄 → 번호 줄로 바꿔 주는 도구",
             "컴퓨터가 보는 바이트와 신경망이 먹는 번호 사이의 다리예요. 말뭉치로 학습해서 만들어요."),
    "vocab": ("레고 상자에 든 조각 종류 목록",
              "모델이 아는 토큰 전체 목록이에요. 목록에 없는 것은 원래 [UNK] 가 돼요. GPT-2 는 약 5만 개, GPT-4o 는 약 20만 개예요."),
    "corpus": ("학습에 쓰는 아주 큰 글 뭉치",
               "토크나이저도, 단어 벡터도 말뭉치를 보고 배워요. 말뭉치에 어떤 언어가 많은지가 결과를 바꿔요."),
    "oov": ("어휘 목록에 없는 단어",
            "단어 단위로 자르면 신조어, 오타, 이름이 전부 미등록 단어가 되어 [UNK] 로 뭉개져요."),
    "unk": ("'모르는 것' 이라는 뜻의 대체 토큰",
            "어휘에 없는 단어를 받으면 이 토큰 하나로 바꿔 버려요. 원래 뜻이 전부 사라져요."),
    "utf8": ("글자를 바이트 숫자로 바꾸는 세계 공통 약속",
             "영어 글자는 1바이트, 한글 한 글자는 3바이트가 돼요. 컴퓨터가 실제로 저장하는 것은 이 바이트예요."),
    "zipf": ("몇 개 단어만 아주 자주 나오고 대부분은 거의 안 나온다는 법칙",
             "빈도가 순위에 반비례해요(빈도 ∝ 1/순위). 그래서 어휘를 아무리 크게 해도 긴 꼬리가 잘려서 [UNK] 가 돼요."),
    "attn": ("문장 안의 토큰끼리 서로 얼마나 볼지 정하는 장치",
             "트랜스포머의 핵심이에요. 계산량이 길이의 제곱으로 늘어서, 토큰 줄이 길어지면 비용이 크게 늘어요."),
    "sub": ("단어와 글자 사이 크기의 조각",
            "자주 나오는 덩어리는 통째로, 드문 단어는 조각으로 잘라요. 미등록 단어가 없고, 길이도 적당하고, 조각에 뜻도 있어요."),
    "bpe": ("자주 붙어 다니는 두 조각을 한 조각으로 접착하기를 되풀이하는 방법",
            "글자에서 시작해서 가장 자주 붙어 나오는 쌍을 합치고 규칙을 적어요. 이것을 목표 어휘 크기까지 되풀이해요. 1994년 압축 방법을 2016년에 NLP로 가져왔어요."),
    "merge": ("'이 두 조각을 붙여라' 라는 접착 순서 한 줄",
              "BPE 가 배우는 것은 순서가 있는 병합 규칙 목록이에요. 그 목록이 곧 토크나이저예요. 새 글도 같은 순서로 다시 붙여요."),
    "blbpe": ("글자 대신 256가지 바이트에서 출발하는 BPE",
              "GPT-2 부터 표준이에요. 어떤 입력이든 바이트로 쪼갤 수 있어서 [UNK] 가 아예 생기지 않아요."),
    "wp": ("말뭉치를 가장 잘 설명하는 쌍을 붙이는 BERT 의 방법",
           "그냥 빈도가 아니라 우도를 가장 많이 올리는 쌍을 합쳐요. 뒤에 붙는 조각에는 ## 를 달아요(play + ##ing)."),
    "uni": ("큰 후보 목록에서 시작해 쓸모없는 조각을 깎아 내는 방법",
            "BPE 와 방향이 반대예요. 문장마다 확률이 가장 높은 자르기를 골라요."),
    "like": ("이 설명이 데이터를 얼마나 그럴듯하게 만드는지 재는 값",
             "워드피스는 합쳤을 때 말뭉치가 더 그럴듯해지는(우도가 오르는) 쌍을 골라요. 따로는 드문데 늘 붙어 나오는 쌍을 좋아해요."),
    "spm": ("BPE 나 유니그램을 담아 둔 토큰화 도구 모음",
            "띄어쓰기도 ▁ 기호 하나로 다뤄서, 띄어쓰기가 들쭉날쭉한 한국어, 일본어에 좋아요. 알고리즘 이름이 아니라 라이브러리예요."),
    "special": ("모델 행동을 바꾸는 스위치 같은 약속 토큰",
                "<|endoftext|>, [CLS], [SEP], 채팅 틀 토큰 같은 것이에요. 글 끝, 문장 경계, 대화 차례를 알려 줘요."),
    "ctx": ("모델이 한 번에 볼 수 있는 토큰 수의 한도",
            "API 요금과 이 한도는 모두 토큰 수로 세요. 같은 뜻을 적은 토큰으로 담을수록 싸고 더 많이 담아요."),
    "aggl": ("줄기에 문법 조각을 줄줄이 붙여 한 단어를 만드는 언어",
             "한국어, 일본어가 그래요. '먹었겠더라' 처럼 형태소 여러 개가 한 어절에 붙어서, 띄어쓰기로 자르면 어휘가 폭발해요."),
    "morph": ("뜻을 가진 가장 작은 말 조각",
              "'먹었겠더라' 는 먹-(먹다), -었-(과거), -겠-(추측), -더라(회상) 네 형태소예요."),
    "eojeol": ("띄어쓰기로 나뉘는 한국어 한 덩어리",
               "'자연어처리는' 처럼 단어에 조사, 어미가 붙은 덩어리예요. 한국어에서 '공백 단어' 는 곧 어절이에요."),
    "analyzer": ("언어 지식으로 어절을 형태소로 자르고 품사를 붙이는 도구",
                 "MeCab-ko, Kiwi, Okt, Komoran 이 대표예요. 깔끔하지만 규칙 기반이라 신조어에 약하고 실수가 뒤로 번져요."),
    "pos": ("형태소마다 붙이는 품사 이름표",
            "NNG(일반 명사), JX(보조사), VA(형용사), EF(종결 어미) 같은 표시예요."),
    "fert": ("단어 하나가 평균 몇 토큰으로 잘리는지 재는 값",
             "토큰 수 ÷ 공백 단어 수예요. 클수록 그 언어를 비싸게 다룬다는 뜻이에요. 영어 중심 토크나이저에서 한국어는 2~3배 커져요."),
}


def _fin(key):
    ko, en, sh, f = TERMS[key]
    if f is not None:
        return f
    c = (ko or en)[-1]
    if "가" <= c <= "힣":
        j = (ord(c) - 0xAC00) % 28
        return 0 if j == 0 else (2 if j == 8 else 1)
    raise ValueError(key)


def disp(key):
    ko, en, sh, _ = TERMS[key]
    if key == "bpe":
        return "**BPE(바이트 쌍 인코딩)**"
    if key == "blbpe":
        return "**바이트 수준 BPE(Byte-level BPE)**"
    e = sh or en
    return f"**{ko}({e})**" if ko and e else f"**{ko or e}**"


JOSA = {"은": ("은", "는"), "이": ("이", "가"), "을": ("을", "를"), "과": ("과", "와"),
        "이에요": ("이에요", "예요"), "이라고": ("이라고", "라고"), "이라는": ("이라는", "라는"),
        "이고": ("이고", "고"), "이나": ("이나", "나"), "이죠": ("이죠", "죠"), "이라서": ("이라서", "라서"),
        "이란": ("이란", "란")}


NORM = {"는": "은", "가": "이", "를": "을", "와": "과", "로": "으로", "예요": "이에요",
        "라고": "이라고", "라는": "이라는", "고": "이고", "나": "이나", "다": "이다"}
JOSA["이다"] = ("이다", "다")


def K(key, josa=""):
    josa = NORM.get(josa, josa)
    s = disp(key)
    if not josa:
        return s
    if josa == "으로":
        return s + ("으로" if _fin(key) == 1 else "로")
    if josa in JOSA:
        return s + (JOSA[josa][0] if _fin(key) >= 1 else JOSA[josa][1])
    return s + josa


# =====================================================================
# 장면
# =====================================================================
PW, PH = 1400, 788


def say(*lines):
    return {"kind": "say", "lines": list(lines)}


def look(head, *boxes):
    out = []
    for x1, y1, x2, y2, s in boxes:
        out.append({"x": round(x1 / PW, 3), "y": round(y1 / PH, 3),
                    "w": round((x2 - x1) / PW, 3), "h": round((y2 - y1) / PH, 3), "say": s})
    return {"kind": "look", "head": head, "boxes": out}


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
            "parts": [{"sym": a, "say": b} for a, b in parts], "whole": whole}


def figure(head, svg, caption, builds):
    return {"kind": "figure", "head": head, "svg": svg, "caption": caption, "builds": builds}


def check(q, choices, a, why):
    return {"kind": "check", "q": q, "choices": list(choices), "a": a, "why": why}


def warn(head, *items):
    return {"kind": "warn", "head": head, "items": list(items)}


def english(head, en, ko, tip=None):
    d = {"kind": "english", "head": head, "en": en, "ko": ko}
    if tip:
        d["tip"] = tip
    return d


def prof(when, *lines):
    return {"kind": "prof", "when": when, "lines": list(lines)}


def bg(src, *lines):
    return {"kind": "bg", "src": src, "lines": list(lines)}


def exam(src, q, qko, solve, answer):
    return {"kind": "exam", "src": src, "q": q, "qko": qko, "solve": list(solve), "answer": answer}


# ---------------- SVG ----------------
def _b(b):
    return f" b{b}" if b else ""


def TX(x, y, s, cls="t", fs=15, anc="middle", b=0):
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f'<text x="{x}" y="{y}" font-size="{fs}" text-anchor="{anc}" class="{cls}{_b(b)}">{s}</text>'


def R(x, y, w, h, cls="box", b=0, rx=2):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" class="{cls}{_b(b)}"/>'


def L(x1, y1, x2, y2, cls="e", b=0):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{cls}{_b(b)}"/>'


def A(x1, y1, x2, y2, cls="e2", b=0):
    ang = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 - 9 * math.cos(ang), y2 - 9 * math.sin(ang)
    px, py = -math.sin(ang) * 5, math.cos(ang) * 5
    pts = f"{x2:.0f},{y2:.0f} {hx + px:.0f},{hy + py:.0f} {hx - px:.0f},{hy - py:.0f}"
    return L(x1, y1, f"{hx:.0f}", f"{hy:.0f}", cls, b) + f'<polygon points="{pts}" class="arrow{_b(b)}"/>'


def BOX(x, y, w, h, label, cls="box", tcls="tb", b=0, fs=15):
    return R(x, y, w, h, cls, b) + TX(x + w / 2, y + h / 2 + fs // 3 + 1, label, tcls, fs, "middle", b)


def SVG(*parts, h=270):
    return f'<svg viewBox="0 0 480 {h}" xmlns="http://www.w3.org/2000/svg">' + "".join(parts) + "</svg>"


def BLOCKS(x, y, labels, cls="n", b=0, h=30, fs=14, gap=4, wch=13, pad=14):
    """레고 조각 줄: 글자 수에 맞춰 폭을 정한다."""
    out = []
    for lab in labels:
        w = max(26, len(lab) * wch + pad)
        out.append(R(x, y, w, h, cls, b))
        out.append(TX(x + w / 2, y + h / 2 + fs // 3 + 1, lab, "tl", fs, "middle", b))
        x += w + gap
    return "".join(out)


# ---------------- 그림 ----------------
FIG_PIPE = SVG(
    BOX(10, 110, 80, 44, "글", "n", "tl", 0, 16),
    A(92, 132, 122, 132, "e2", 1),
    BOX(124, 110, 90, 44, "토큰", "n2", "tl", 1, 16),
    A(216, 132, 246, 132, "e2", 2),
    BOX(248, 110, 90, 44, "벡터", "n2", "tl", 2, 16),
    A(340, 132, 370, 132, "e", 3),
    BOX(372, 110, 100, 44, "다음 토큰", "n3", "tl", 3, 15),
    TX(169, 90, "1부, 2부", "tb", 14, "middle", 1),
    TX(293, 90, "3부, 4부", "tb", 14, "middle", 2),
    TX(422, 90, "뒤 주차", "tm", 14, "middle", 3),
    R(118, 170, 226, 40, "hl", 2),
    TX(231, 196, "오늘 만드는 화살표 두 개", "tb", 15, "middle", 2),
    TX(240, 245, "어떻게 자를까? → 무슨 숫자로 바꿀까?", "t", 15, "middle", 3),
)

FIG_ZIPF = SVG(
    L(40, 230, 460, 230), L(40, 230, 40, 20),
    TX(250, 258, "순위 (많이 나오는 단어부터)", "tm", 14),
    R(55, 30, 26, 200, "n2"), R(89, 130, 26, 100, "n2"), R(123, 163, 26, 67, "n2"),
    R(157, 180, 26, 50, "n2"), R(191, 190, 26, 40, "n2"),
    TX(68, 24, "the", "tb", 14), TX(102, 124, "of", "tb", 14), TX(136, 157, "to", "tb", 14),
    R(225, 197, 14, 33, "n", 1), R(243, 205, 14, 25, "n", 1), R(261, 210, 14, 20, "n", 1),
    R(279, 214, 14, 16, "n", 1), R(297, 217, 14, 13, "n", 1), R(315, 219, 14, 11, "n", 1),
    R(333, 221, 14, 9, "n4", 2), R(351, 223, 14, 7, "n4", 2), R(369, 224, 14, 6, "n4", 2),
    R(387, 225, 14, 5, "n4", 2), R(405, 226, 14, 4, "n4", 2), R(423, 226, 14, 4, "n4", 2),
    L(328, 60, 328, 232, "e2", 2),
    TX(320, 80, "어휘 한도", "tb", 14, "end", 2),
    TX(446, 120, "잘린 꼬리", "tb", 15, "end", 2),
    TX(446, 142, "→ 전부 [UNK]", "t", 14, "end", 2),
    TX(250, 60, "머리: 몇 개 단어가 대부분", "t", 14, "middle", 0),
)

FIG_THREE = SVG(
    TX(10, 40, "단어", "tb", 16, "start"),
    BLOCKS(90, 20, ["unbelievable"], "n4", 0, wch=12),
    TX(260, 40, "통째로 하나: 새 단어면 [UNK]", "tm", 14, "start"),
    TX(10, 120, "글자", "tb", 16, "start", 1),
    BLOCKS(90, 100, list("unbelievable"), "n", 1, wch=10, pad=8, gap=3),
    TX(90, 152, "12조각: 줄이 길고 조각에 뜻이 없어요", "tm", 14, "start", 1),
    TX(10, 210, "서브워드", "tb", 16, "start", 2),
    BLOCKS(90, 190, ["un", "believ", "able"], "n2", 2, wch=12),
    TX(90, 244, "3조각: 뜻 있는 조각, 적당한 길이", "tb", 14, "start", 2),
)

FIG_BPE = SVG(
    TX(10, 30, "처음", "tb", 15, "start"),
    BLOCKS(80, 12, ["n", "e", "w", "e", "s", "t</w>"], "n", 0, wch=11),
    TX(10, 90, "병합 1", "tb", 15, "start", 1),
    BLOCKS(80, 72, ["n", "e", "w", "es", "t</w>"], "n", 1, wch=11),
    TX(330, 92, "e + s (9번)", "t", 14, "start", 1),
    TX(10, 150, "병합 2", "tb", 15, "start", 2),
    BLOCKS(80, 132, ["n", "e", "w", "est</w>"], "n", 2, wch=11),
    TX(330, 152, "es + t</w> (9번)", "t", 14, "start", 2),
    TX(10, 210, "병합 3", "tb", 15, "start", 3),
    BLOCKS(80, 192, ["lo", "w</w>"], "n2", 3, wch=11),
    TX(330, 212, "l + o (7번)", "t", 14, "start", 3),
    TX(240, 258, "자주 붙어 다니는 두 조각을 접착해요", "tm", 14, "middle", 3),
)

FIG_MORPH = SVG(
    TX(240, 36, "먹었겠더라 = 어절 하나", "tb", 17),
    BLOCKS(60, 70, ["먹-"], "n2", 1, h=44, fs=17, wch=20, pad=40),
    BLOCKS(152, 70, ["-었-"], "n3", 2, h=44, fs=17, wch=16, pad=40),
    BLOCKS(248, 70, ["-겠-"], "n3", 3, h=44, fs=17, wch=16, pad=40),
    BLOCKS(344, 70, ["-더라"], "n3", 4, h=44, fs=17, wch=16, pad=36),
    TX(100, 140, "먹다(줄기)", "t", 14, "middle", 1),
    TX(196, 140, "과거", "t", 14, "middle", 2),
    TX(292, 140, "추측", "t", 14, "middle", 3),
    TX(386, 140, "회상", "t", 14, "middle", 4),
    TX(240, 200, "형태소 4개가 한 덩어리로 붙어 있어요", "tb", 15, "middle", 4),
    TX(240, 232, "먹었더라, 먹겠더라... 모두 다른 '단어' 가 돼요", "tm", 14, "middle", 4),
)

FIG_FERT = SVG(
    L(150, 20, 150, 230),
    TX(140, 55, "영어 문장", "t", 14, "end"), R(150, 38, 7 * 16, 28, "n"), TX(150 + 7 * 16 + 8, 58, "7", "tb", 15, "start"),
    TX(140, 115, "한국어, 영어 중심", "t", 14, "end", 1), R(150, 98, 17 * 16, 28, "n4", 1), TX(150 + 17 * 16 + 8, 118, "17", "tb", 15, "start", 1),
    TX(140, 175, "한국어, 한국어 맞춤", "t", 14, "end", 2), R(150, 158, 8 * 16, 28, "n2", 2), TX(150 + 8 * 16 + 8, 178, "8", "tb", 15, "start", 2),
    TX(300, 225, "토큰 수 (같은 뜻의 문장)", "tm", 14, "middle"),
    TX(240, 258, "같은 뜻인데 한국어 사용자가 2배 넘게 내요", "tb", 15, "middle", 2),
)


# =====================================================================
# 쪽
# =====================================================================
S = []

# p.1 표지
S.append({"p": 1, "title": "2강 표지: Tokenization and Word Vectors",
 "pass1": [
  say("2강 제목은 '토큰화와 단어 벡터' 예요.",
      f"글을 조각내는 {K('tokz','과')}, 조각을 숫자로 바꾸는 {K('wv','가')} 오늘의 두 주인공이에요.",
      "지난주에 역사를 훑었다면, 오늘부터 진짜 기술 이야기가 시작돼요.",
      MANTRA),
 ], "pass2": [], "pass3": [], "pass4": []})

# p.2 Reminder
S.append({"p": 2, "title": "Reminder (안내)",
 "pass1": [
  say("수업 안내 쪽이에요. 공부할 내용은 없어요.",
      "1. 저작권이 있으니 자료를 밖에 퍼뜨리지 말아 달라는 부탁이에요.",
      "2. 화면이나 소리에 문제가 있으면 바로 말해 달라는 부탁이에요."),
 ], "pass2": [], "pass3": [], "pass4": []})

# p.3 목차
S.append({"p": 3, "title": "2강 목차 (Contents)",
 "pass1": [
  points("2강의 네 덩어리",
      f"1. From Text to Tokens: 글을 어떤 크기의 {K('tok','으로')} 자를지 (오늘 이 레슨)",
      f"2. Korean Tokenization: {K('aggl','인')} 한국어는 왜 따로 다루는지 (오늘 이 레슨)",
      f"3. word2vec: 잘라 낸 토큰을 뜻이 담긴 {K('wv','로')} 바꾸기",
      "4. Counting, GloVe & Evaluation: 세어서 만드는 방법, GloVe, 평가 방법"),
  say("이 레슨(1~21쪽)은 앞의 두 덩어리, 즉 자르기 이야기만 다뤄요.",
      "3, 4 덩어리는 22쪽부터 이어져요."),
 ], "pass2": [], "pass3": [], "pass4": []})

# p.4 Recap
S.append({"p": 4, "title": "Recap: 지난주와 오늘",
 "pass1": [
  say("지난주에는 70년 NLP 역사를 봤어요.",
      f"규칙 → 통계 → 신경망 → 사전 학습 → {K('llm')} 순서로 바뀌어 왔어요.",
      "그 끝에 요즘 모델이 쓰는 흐름 하나가 남았어요.",
      MANTRA),
  figure("현대 파이프라인과 오늘 만드는 부분", FIG_PIPE,
      "글 → 토큰 → 벡터 → 다음 토큰. 오늘은 앞 화살표 두 개를 만들어요.", 3),
 ],
 "pass2": [
  compare("슬라이드 영어 문장 → 우리말 뜻", ["영어 원문", "우리말 뜻"],
      ["NLP = making computers understand & generate human language", f"{K('nlp','는')} 컴퓨터가 사람 말을 이해하고 만들어 내게 하는 일"],
      ["text → tokens → vectors → predict the next token", f"글 → {K('tok')} → 벡터 → {K('ntp')}"],
      ["Today we build the first two arrows", "오늘은 앞의 화살표 두 개를 만들어요"],
      ["what is the unit of text?", "글을 어떤 단위로 자를까?"],
      ["what numbers should a token become?", "토큰을 어떤 숫자로 바꿀까?"]),
  steps("파이프라인이 이어지는 순서",
      [f"글을 조각으로 잘라요: {K('tokz')}",
       f"조각마다 번호를 붙이고 숫자 목록으로 바꿔요: {K('wv')}",
       f"숫자로 다음 조각을 맞혀요: {K('ntp')}",
       "틀린 만큼 벌점을 매겨 고쳐요(뒤 주차에서 배워요)"],
      "오늘은 1번과 2번이에요."),
  check("오늘 수업이 만드는 '앞의 두 화살표' 는 무엇일까요?",
      ["글 → 토큰, 토큰 → 벡터", "벡터 → 다음 토큰, 다음 토큰 → 글", "규칙 → 통계, 통계 → 신경망"], 0,
      f"오늘은 글을 {K('tok','으로')} 자르는 법과 토큰을 숫자(벡터)로 바꾸는 법을 배워요."),
 ],
 "pass3": [
  look("Recap 쪽에서 볼 곳",
      (85, 155, 1025, 222, "Last week: 지난주 요약. NLP 는 사람 말을 이해하고 생성하는 일, 70년 동안 규칙 → 통계 → 신경망 → 사전 학습 → LLM 으로 왔어요."),
      (85, 238, 995, 272, f"The modern pipeline: 글 → {K('tok')} → vectors → predict the next token. 과목 전체의 뼈대예요."),
      (85, 288, 1135, 322, "Today we build the first two arrows: (1) 글을 어떻게 자를지, (2) 토큰을 어떻게 숫자로 바꿀지."),
      (85, 337, 1190, 372, "Also today: 쉬는 시간 뒤 첫 Colab 실습, 그리고 과제 1(Assignment 1)이 나가요. 다음 주까지예요."),
      (300, 680, 1105, 706, "오늘의 두 질문: 글의 단위는 무엇인가, 토큰은 어떤 숫자가 되어야 하는가.")),
  prof(W1,
      "지난주 말한 현대 파이프라인은 말뭉치(코퍼스)의 글을 토큰으로 바꿔 다음 토큰을 예측하는 방식이에요.",
      "오늘은 그 앞쪽, 글을 토큰으로 바꾸고 토큰을 벡터로 바꾸는 부분을 해요.",
      "규칙을 손으로 적기보다 데이터에서 모델이 스스로 배우게 하는 쪽(데이터 드리븐)으로 발전해 왔다고 했어요."),
  prof(W3,
      "과제 1은 5점짜리예요. Part A 는 한국어로 된 작은 말뭉치에 BPE 를 돌려 보는 코딩(1점)이에요.",
      "Part A 는 AI 도구를 써도 되지만, 썼다면 어떤 도구인지 꼭 밝혀야 해요.",
      "뒤의 질문 두 개(각 2점)는 AI 없이 자기 말로 써요. 다음 주 수업 전(2시 59분)까지 내요."),
 ],
 "pass4": [
  check("현대 NLP 파이프라인의 순서로 맞는 것은?",
      ["글 → 벡터 → 토큰 → 다음 토큰 예측", "글 → 토큰 → 벡터 → 다음 토큰 예측", "토큰 → 글 → 벡터 → 다음 토큰 예측"], 1,
      f"먼저 자르고({K('tokz')}), 그다음 숫자로 바꾸고, 마지막에 {K('ntp','을')} 해요."),
  english("답안 문장: 오늘의 두 질문",
      f"파이프라인은 글 → {K('tok')} → 벡터 → 다음 토큰 예측이고, 2강은 앞의 두 단계(자르기, 숫자로 바꾸기)를 다룬다.",
      "파이프라인 네 칸과 오늘 맡은 두 칸(토큰화, 단어 표현)을 함께 쓰면 돼요.",
      "주문 한 줄을 떠올리면 순서가 저절로 나와요: 자르고, 바꾸고, 맞혀요."),
 ]})

# p.5 1부 구분
S.append({"p": 5, "title": "1부 From Text to Tokens (구분 쪽)",
 "pass1": [
  say("여기서부터 1부예요. 제목은 '글에서 토큰으로' 예요.",
      "부제는 'what is the unit of text?', 글의 단위는 무엇인가예요.",
      f"단어로 자를까, 글자로 자를까, 그 사이로 자를까를 차례로 따져 봐요.",
      f"끝에는 요즘 모든 모델이 쓰는 {K('bpe','를')} 만나요."),
 ], "pass2": [], "pass3": [], "pass4": []})

# p.6 Models Don't Read
S.append({"p": 6, "title": "Models Don't Read: 모델은 글을 읽지 못해요",
 "pass1": [
  say("컴퓨터는 사람 글자를 그대로 읽지 못해요.",
      "컴퓨터가 실제로 보는 것은 바이트라는 숫자 덩어리예요.",
      "신경망이 먹는 것은 정해진 목록 속 번호 줄이에요.",
      f"글과 번호 사이를 이어 주는 다리가 {K('tokr','예요')}."),
  analogy("레고로 생각하기",
      "레고 상자 안에 조각 종류 목록이 있고, 조각마다 번호가 붙어 있어요. 글을 조각으로 나누면 번호 줄이 돼요.",
      ["레고 조각 하나", K("tok")],
      ["상자 속 조각 종류 목록", K("vocab")],
      ["조각 번호", K("tokid")],
      ["글을 조각으로 나누는 기계", K("tokr")]),
 ],
 "pass2": [
  compare("슬라이드 영어 → 우리말", ["영어 원문", "우리말 뜻"],
      ["Models Don't Read", "모델은 글을 읽지 못해요"],
      ["What a computer actually sees: bytes", "컴퓨터가 실제로 보는 것은 바이트예요"],
      ["What a neural network actually eats: integer IDs from a fixed vocabulary", f"신경망이 먹는 것은 정해진 {K('vocab')} 속 정수 번호예요"],
      ["The bridge between them is the tokenizer", f"둘 사이의 다리가 {K('tokr','예요')}"],
      ["what goes into the vocabulary?", "어휘 목록에 무엇을 넣을까?"]),
  steps("토크나이저가 하는 일",
      ["글: ChatGPT는 똑똑해",
       f"{K('tok')} 줄로 자르기: [조각, 조각, 조각, ...]",
       f"{K('tokid')} 줄로 바꾸기: [8203, 318, 15339, ...]",
       "번호마다 붙은 숫자 목록(벡터)을 꺼내 신경망에 넣기"],
      "글 → 토큰 줄 → 번호 줄. 이 두 화살표가 토크나이저예요."),
  check(f"신경망이 실제로 받는 입력은 무엇일까요?",
      ["사람이 쓴 글자 그대로", "정해진 어휘 목록 속 정수 번호 줄", "소리 파형"], 1,
      f"신경망은 {K('tokid')} 줄을 받아요. 글을 번호로 바꾸는 것이 {K('tokr')}의 일이에요."),
 ],
 "pass3": [
  look("Models Don't Read 쪽에서 볼 곳",
      (85, 155, 1120, 190, f"bytes: 컴퓨터가 보는 것은 바이트예요. 글자를 바이트로 바꾸는 약속이 {K('utf8','예요')}."),
      (85, 203, 1205, 237, f"integer IDs from a fixed vocabulary: 신경망은 고정된 {K('vocab')}의 정수 번호 [8203, 318, ...] 를 먹어요."),
      (85, 251, 945, 285, f"The bridge ... is the tokenizer: 글 → 토큰 줄 → ID 줄. 이 다리가 {K('tokr','예요')}."),
      (85, 299, 1120, 333, "The design question: 어휘에 무엇을 넣을까? 단어? 글자? 그 사이?"),
      (85, 347, 785, 380, "이 선택 하나가 모델 품질, 비용, 여러 언어 실력을 정해요."),
      (310, 680, 1095, 706, f"{K('tokz','은')} 모든 NLP 시스템의 첫 결정이고, 생각보다 어려워요.")),
  prof(W1,
      "컴퓨터는 사람이 읽고 쓰는 말을 그대로 받아들이지 못해요. UTF-8 바이트나 0과 1만 알아요.",
      "그래서 글을 컴퓨터가 이해하는 토큰으로 바꾸는 일이 아주 중요해요.",
      "토큰마다 ID 를 주고, ID 마다 벡터를 둬요. 64차원이면 숫자 64개가 토큰 하나를 나타내요.",
      "어휘집에 어떤 토큰을 모아 둘지가 토큰화의 가장 중요한 쟁점이에요."),
  bg("기초 다지기 1단원 (숫자 목록, 벡터)",
      "벡터는 숫자를 한 줄로 늘어놓은 목록이에요.",
      "64차원 벡터는 숫자 64개짜리 목록이에요.",
      "토큰 번호로 이 목록을 꺼내 쓰는 것이 단어 표현의 시작이에요."),
 ],
 "pass4": [
  warn("헷갈리기 쉬운 점: 슬라이드의 바이트 예",
      "슬라이드는 \"ChatGPT는 똑똑해\" = EC 9E 90 EC 97 B0 ... 라고 적었어요.",
      "그런데 EC 9E 90 EC 97 B0 은 실제로 '자연' 두 글자의 UTF-8 바이트예요. \"ChatGPT는\" 은 43 68 ... 로 시작해요.",
      "뜻('컴퓨터는 바이트를 본다')만 기억하면 돼요. 영어 글자는 1바이트, 한글 한 글자는 3바이트예요."),
  check("토크나이저의 역할로 가장 알맞은 것은?",
      ["벡터로 다음 토큰을 맞힌다", "글을 토큰 줄로 자르고 토큰 ID 줄로 바꾼다", "틀린 정도에 벌점을 매긴다"], 1,
      f"{K('tokr','는')} 글 → 토큰 → ID 의 다리예요. 다음 토큰 맞히기는 모델이 해요."),
  english("답안 문장: 토크나이저",
      f"신경망은 고정된 {K('vocab')}의 정수 ID 만 받으므로, 글을 토큰 줄과 ID 줄로 바꾸는 {K('tokr','가')} 필요하다.",
      "컴퓨터는 바이트를 보고 신경망은 정수 ID 를 먹어요. 어휘에 무엇을 넣을지가 품질, 비용, 다국어 능력을 좌우해요."),
 ]})

# p.7 Option 1 Words
S.append({"p": 7, "title": "Option 1: 단어로 자르기 (Words)",
 "pass1": [
  say("첫 번째 방법은 가장 자연스러워 보여요. 띄어쓰기로 자르는 거예요.",
      "\"I love NLP\" 는 [I, love, NLP] 세 조각이 돼요.",
      "그런데 이 방법은 실제 세상에서 금방 무너져요. 문제가 세 가지예요."),
  points("단어로 자르면 생기는 문제 세 가지",
      f"처음 보는 단어는 전부 '모름' 이 돼요: {K('oov')}",
      "run, runs, running, ran 이 다 다른 조각이라 목록이 터져요",
      "unbelievable 과 believe 가 아무 상관 없는 번호가 돼요"),
 ],
 "pass2": [
  compare("세 문제를 영어 → 우리말로", ["영어 원문", "우리말 뜻", "예"],
      ["OOV (out-of-vocabulary)", f"{K('oov')}: 목록에 없는 단어", "갓생, 억텐, 야르, ChatGPT"],
      ["vocabulary explosion", f"{K('vocab')} 폭발: 모양만 다른 단어가 전부 따로", "run / runs / running / ran"],
      ["lost structure", "구조를 잃음: 단어끼리의 친척 관계가 사라짐", "unbelievable 과 believe"]),
  points("용어 뜻 풀기",
      f"{K('oov')}: 어휘 목록에 없는 단어예요. 신조어, 오타, 사람 이름이 대표예요.",
      f"{K('unk')}: 모르는 단어를 대신하는 토큰이에요. 들어가는 순간 원래 뜻이 사라져요.",
      "morphology-rich language: 단어 모양이 많이 바뀌는 언어예요. 한국어가 그래요."),
  check("\"갓생\" 이 2012년에 만든 단어 목록에 없어서 [UNK] 가 되는 문제를 무엇이라 할까요?",
      ["미등록 단어(OOV)", "어휘 폭발", "구조를 잃음"], 0,
      f"목록에 없는 단어가 들어오는 문제가 {K('oov','예요')}. 그 단어는 {K('unk','로')} 바뀌어요."),
 ],
 "pass3": [
  look("Option 1 쪽에서 볼 곳",
      (85, 155, 945, 190, "split on spaces: 띄어쓰기로 자르기. \"I love NLP\" → [I, love, NLP]"),
      (85, 200, 1310, 267, f"Problem 1, OOV: 목록에 없으면 {K('unk','가')} 돼요. 새 단어, 오타, 이름이 다 죽어요. 갓생, 억텐, 야르, ChatGPT 는 2012년 목록에 없었어요."),
      (85, 282, 1320, 345, "Problem 2, vocabulary explosion: run/runs/running/ran 이 다 따로예요. 모양이 많이 바뀌는 언어에는 재앙이에요."),
      (85, 360, 1015, 394, "Problem 3, lost structure: unbelievable 과 believe 가 완전히 남남인 ID 가 돼요."),
      (385, 680, 1020, 706, "단어 단위는 자연스러워 보이지만 현실에서 바로 깨져요.")),
  prof(W1,
      "영어는 굴절어라서 단어 자체가 모양을 바꿔요(과거형 같은 것).",
      "한국어, 일본어처럼 어근에 조사가 붙어 단어가 되는 언어는 교착어예요. 이런 언어에서 문제가 훨씬 심해요.",
      "unbelievable 과 believe 는 뜻이 아주 가까운데, 공백으로 자르면 서로 파생 관계라는 정보가 통째로 사라져요."),
  compare("어휘 폭발을 숫자로 느껴 보기", ["단어 모양", "단어 단위 조각 수", "서브워드로 자르면"],
      ["run, runs, running, ran", "4개가 모두 따로", "run 을 나눠 쓰고 뒤 조각만 바뀜"],
      ["unbelievable, believe", "2개, 관계 없음", "believ 조각을 함께 씀"]),
 ],
 "pass4": [
  check("단어 단위 토큰화의 문제가 아닌 것은?",
      ["미등록 단어가 [UNK] 가 된다", "어휘가 폭발한다", "토큰 줄이 너무 길어진다", "단어 사이 구조가 사라진다"], 2,
      "토큰 줄이 길어지는 것은 글자 단위의 문제예요(9쪽). 단어 단위는 오히려 줄이 짧아요."),
  english("답안 문장: 단어 단위의 세 문제",
      f"단어 단위는 ① 새 단어가 {K('unk','가')} 되는 OOV, ② 어휘 폭발, ③ 단어 사이 구조 손실 문제가 있다.",
      "① 신조어, 오타, 이름이 [UNK], ② run/runs/running 이 모두 따로, ③ unbelievable 과 believe 가 남남이 돼요."),
 ]})

# p.8 Zipf
S.append({"p": 8, "title": "The Long Tail: 지프의 법칙 (Zipf's Law)",
 "pass1": [
  say("말뭉치 속 단어를 많이 나오는 순서로 세워 보면 모양이 늘 같아요.",
      "the, of, to 같은 몇 개 단어가 엄청 많이 나와요.",
      "나머지 수만 개 단어는 한두 번만 나와요. 이것을 긴 꼬리라고 해요.",
      f"이 규칙이 {K('zipf','이에요')}."),
  figure("머리는 짧고 꼬리는 길어요", FIG_ZIPF,
      "어휘 한도를 어디에 긋든 오른쪽 꼬리는 잘려서 [UNK] 가 돼요.", 2),
 ],
 "pass2": [
  compare("슬라이드 영어 → 우리말", ["영어 원문", "우리말 뜻"],
      ["frequency ∝ 1/rank", "빈도는 순위에 반비례해요"],
      ["a handful of words dominate the corpus", f"몇 안 되는 단어가 {K('corpus','를')} 휩쓸어요"],
      ["most words barely appear", "대부분 단어는 거의 안 나와요"],
      ["the cut tail all becomes [UNK]", "잘린 꼬리는 전부 [UNK] 가 돼요"],
      ["the vocabulary must be built, not listed", "어휘는 나열이 아니라 만들어 내야 해요"]),
  points("용어 뜻 풀기",
      f"{K('corpus')}: 학습에 쓰는 큰 글 뭉치예요.",
      f"{K('zipf')}: 순위가 2배 뒤로 가면 빈도는 절반쯤이 되는 규칙이에요.",
      "long tail(긴 꼬리): 한두 번만 나오는 수많은 단어 무리예요."),
  check("지프의 법칙에 따르면 어휘를 아주 크게 만들면 어떻게 될까요?",
      ["모든 단어가 들어가서 [UNK] 가 사라진다", "그래도 꼬리가 잘려 [UNK] 가 남는다", "빈도가 모두 같아진다"], 1,
      f"언어는 다 나열할 수 없어요. 어휘를 늘려도 꼬리는 계속 남아요. 그래서 단어 목록 대신 조각을 만들어야 해요."),
 ],
 "pass3": [
  look("Zipf 쪽에서 볼 곳",
      (85, 153, 1125, 188, "Zipf's law: frequency ∝ 1/rank. 몇 단어가 말뭉치를 지배하고 대부분은 거의 안 나와요."),
      (85, 196, 1000, 231, "어휘를 아무리 크게 해도 꼬리가 잘리고, 잘린 꼬리는 모두 [UNK] 예요."),
      (320, 280, 625, 325, "head: the, of, to... 몇 단어가 어디에나 있어요. 왼쪽 위 10^6 근처예요."),
      (805, 428, 1110, 555, "the long tail: 수만 개 단어가 한두 번만 나와요. 오른쪽 아래 끝이에요."),
      (180, 262, 1125, 640, "두 축 모두 로그 눈금이에요. 그래서 반비례 관계가 곧은 직선으로 보여요."),
      (350, 680, 1055, 706, "언어는 다 나열할 수 없어요. 어휘는 나열하는 게 아니라 만들어야 해요.")),
  formula("지프의 법칙을 식으로", r"f(r) \propto \frac{1}{r}",
      [(r"f(r)", "순위가 r 인 단어의 빈도(나온 횟수)"),
       (r"r", "순위. 가장 많이 나오는 단어가 1등"),
       (r"\propto", "'비례한다'. 한쪽이 2배면 다른 쪽도 같은 비율로 바뀜"),
       (r"\frac{1}{r}", "순위가 커질수록 빈도가 작아짐(반비례)")],
      "순위가 10배 뒤로 가면 빈도는 10분의 1이 돼요."),
  steps("손계산: 1등이 100만 번 나올 때",
      ["식을 f(r) = 1,000,000 / r 로 둬요(그래프의 1등이 약 10^6)",
       "2등: 1,000,000 / 2 = 500,000 번",
       "10등: 1,000,000 / 10 = 100,000 번",
       "1000등: 1,000,000 / 1000 = 1,000 번",
       "순위가 수만 등이면 몇십 번, 그 뒤는 한두 번으로 떨어져요"],
      "순위 10배마다 빈도가 10분의 1. 로그-로그 그래프에서 직선이에요."),
  prof(W1,
      "단어 빈도를 순위대로 늘어놓으면 로그-로그 그래프에서 직선이 나와요.",
      "이 법칙은 띄어쓰기로 단어를 구분하는 방식에 대한 사형 선고 같은 거예요.",
      "10만 개짜리 어휘든 100만 개짜리 어휘든 꼬리는 계속 남고, 잘린 꼬리는 언노운 토큰이 돼요."),
  bg("기초 다지기 4단원 (로그와 지수)",
      "로그 눈금은 1, 10, 100, 1000 이 같은 간격으로 놓이는 눈금이에요.",
      "반비례 곡선을 두 축 모두 로그로 그리면 기울기 -1 인 직선이 돼요."),
 ],
 "pass4": [
  check("지프의 법칙에서 1등 단어가 100만 번 나오면 100등 단어는 약 몇 번 나올까요?",
      ["1만 번", "10만 번", "100번", "99만 번"], 0,
      "f = 1,000,000 / 100 = 10,000 번이에요. 순위에 반비례해요."),
  english("답안 문장: 지프의 법칙과 단어 단위",
      f"{K('zipf')}에 따라 빈도는 순위에 반비례하므로, 어휘를 키워도 긴 꼬리가 잘려 [UNK] 가 된다.",
      "몇 단어가 말뭉치를 지배하고 대부분은 드물어요. 그래서 어휘는 나열하는 대신 데이터로 만들어야 해요."),
 ]})

# p.9 Option 2 Characters
S.append({"p": 9, "title": "Option 2: 글자로 자르기 (Characters)",
 "pass1": [
  say("두 번째 방법은 반대쪽 끝이에요. 글자 하나하나로 잘라요.",
      "\"love\" 는 [l, o, v, e] 네 조각이 돼요.",
      f"글자로 쓰면 어떤 단어든 쓸 수 있어서 {K('oov','가')} 사라져요.",
      "대신 줄이 길어지고, 조각 하나에 뜻이 없어요."),
  compare("단어로 자르기 vs 글자로 자르기", ["", "단어", "글자"],
      ["조각 종류 수", "엄청 많음", "몇백 개"],
      ["모르는 단어", "[UNK] 가 됨", "절대 안 생김"],
      ["줄 길이", "짧음", "아주 김"],
      ["조각의 뜻", "있음", "없음"]),
 ],
 "pass2": [
  compare("슬라이드 영어 → 우리말", ["영어 원문", "우리말 뜻"],
      ["tiny vocabulary (a few hundred)", "어휘가 아주 작아요(몇백 개)"],
      ["OOV is impossible by construction", "만드는 방식 자체로 미등록 단어가 불가능해요"],
      ["sequences get long", "토큰 줄이 길어져요"],
      ["the unit is meaningless", "조각 하나에 뜻이 없어요"],
      ["re-learn how to assemble meaning out of letters", "글자로 뜻을 조립하는 법부터 다시 배워야 해요"]),
  points("용어 뜻 풀기",
      "sequence(시퀀스): 모델에 들어가는 토큰 줄이에요. 길이는 토큰 개수예요.",
      f"{K('attn')}: 문장 속 토큰끼리 서로 얼마나 볼지 정하는 장치예요. 뒤 주차에 배워요.",
      "attention compute: 어텐션 계산량이에요. 토큰 줄 길이의 제곱으로 늘어요."),
  check("글자 단위 토큰화의 장점은?",
      ["조각마다 뜻이 뚜렷하다", "미등록 단어가 생기지 않는다", "토큰 줄이 짧다"], 1,
      "글자만 있으면 어떤 단어든 쓸 수 있어서 OOV 가 원리상 생길 수 없어요."),
 ],
 "pass3": [
  look("Option 2 쪽에서 볼 곳",
      (85, 155, 775, 190, "The opposite extreme: 반대쪽 끝, 글자 단위. \"love\" → [l, o, v, e]"),
      (85, 203, 905, 237, f"Pros: 어휘가 몇백 개로 아주 작고, {K('oov','는')} 만드는 방식상 불가능해요."),
      (85, 250, 1055, 285, f"Con 1: 줄이 길어져요. 5배 긴 글이면 나중에 {K('attn')} 계산이 5² = 25배예요."),
      (85, 298, 785, 366, "Con 2: 'l' 과 'o' 는 아무 뜻도 없어요. 모델이 글자로 뜻을 조립하는 법부터 다시 배워야 해요."),
      (350, 680, 1055, 706, "글자는 OOV 를 풀지만 줄 길이와 뜻 없는 조각으로 값을 치러요.")),
  steps("손계산: 줄이 5배 길면 어텐션은 몇 배?",
      [f"{K('attn')} 계산량은 토큰 줄 길이 n 의 제곱(n²)에 비례해요",
       "단어 단위 길이를 n, 글자 단위 길이를 5n 이라 해요",
       "단어 단위: n² , 글자 단위: (5n)² = 25n²",
       "25n² ÷ n² = 25"],
      "25배. 길이 5배 → 계산 25배예요."),
  steps("손계산: 조각 수 세기",
      ["\"I love NLP\" 를 단어로 자르면 [I, love, NLP] 3조각",
       "\"love\" 한 단어만 글자로 자르면 [l, o, v, e] 4조각",
       "\"unbelievable\" 을 글자로 자르면 12조각, 단어로 자르면 1조각"],
      "같은 글인데 글자 단위는 조각이 몇 배로 늘어요."),
  prof(W1,
      "영어는 알파벳 26자면 모든 걸 쓸 수 있어요. 여러 언어를 담아도 수백 개 토큰이면 충분해요.",
      "트랜스포머의 셀프 어텐션은 시퀀스 길이의 제곱으로 계산 비용이 들어요. 그래서 줄이 길어지는 건 바람직하지 않아요.",
      "단어는 너무 크게 자른 것이고, 글자는 너무 작게 자른 거예요."),
 ],
 "pass4": [
  check("단어 단위로 100토큰인 글이 글자 단위로 500토큰이 되었어요. 어텐션 계산은 대략 몇 배?",
      ["5배", "10배", "25배", "500배"], 2,
      "길이가 5배이고 계산은 길이의 제곱에 비례하니 5² = 25배예요."),
  english("답안 문장: 글자 단위의 장단점",
      f"글자 단위는 어휘가 작고 OOV 가 없지만, 줄이 길어 {K('attn')} 계산이 늘고 조각에 뜻이 없다.",
      "길이 5배면 어텐션 계산은 25배예요. 모델은 글자로 뜻을 다시 조립해야 해요."),
  warn("헷갈리기 쉬운 점",
      "글자 단위의 장점은 'OOV 가 없다' 예요. '뜻이 풍부하다' 가 아니에요.",
      "25배는 5의 제곱이에요. 5 × 5 이지 5 + 5 가 아니에요."),
 ]})

# p.10 Option 3 Subwords
S.append({"p": 10, "title": "Option 3: 서브워드로 자르기 (Subwords)",
 "pass1": [
  say("단어는 너무 크고 글자는 너무 작았어요. 답은 그 사이예요.",
      f"자주 나오는 덩어리는 통째로 두고, 드문 단어는 조각으로 나눠요. 이것이 {K('sub','예요')}.",
      "unbelievable 은 un + believ + able 로 잘려요.",
      "요즘 모든 LLM 이 이 방법을 써요."),
  figure("같은 단어를 세 가지로 잘라 보기", FIG_THREE,
      "단어는 너무 크고, 글자는 너무 작고, 서브워드는 알맞아요.", 2),
 ],
 "pass2": [
  compare("슬라이드 영어 → 우리말", ["영어 원문", "우리말 뜻"],
      ["frequent chunks stay whole, rare words break into pieces", "자주 나오는 덩어리는 통째로, 드문 단어는 조각으로"],
      ["unseen \"Kyzylorda\" still spellable from pieces", "처음 보는 지명도 조각을 이어서 쓸 수 있어요"],
      ["No OOV + reasonable sequence length + meaningful units", "OOV 없음 + 적당한 길이 + 뜻 있는 조각"],
      ["who decides which pieces enter the vocabulary?", "어떤 조각을 어휘에 넣을지 누가 정할까?"],
      ["Let the data decide!", "데이터가 정하게 해요!"]),
  compare("세 방법 한눈에", ["", "단어", "글자", f"서브워드"],
      ["OOV", "생김", "없음", "없음"],
      ["줄 길이", "짧음", "아주 김", "적당함"],
      ["조각의 뜻", "있음", "없음", "있음"]),
  check("서브워드 방식이 한 번에 얻는 세 가지가 아닌 것은?",
      ["미등록 단어 없음", "적당한 줄 길이", "뜻 있는 조각", "사람이 손으로 쓴 규칙"], 3,
      "서브워드는 규칙을 손으로 쓰지 않고 데이터가 조각을 정하게 해요."),
 ],
 "pass3": [
  look("Option 3 쪽에서 볼 곳",
      (85, 155, 930, 190, f"The modern answer: 자주 나오는 덩어리는 통째로, 드문 단어는 조각으로. 이것이 {K('sub','예요')}."),
      (85, 200, 1070, 237, "unbelievable → un + believ + able, 자연어처리는 → 자연어 + 처리 + 는"),
      (85, 250, 1060, 285, "자주 나오는 \"the\", \"안녕하세요\" 는 한 토큰. 처음 보는 \"Kyzylorda\" 도 조각으로 쓸 수 있어요."),
      (85, 298, 910, 333, "No OOV + reasonable sequence length + meaningful units. 세 가지를 한꺼번에."),
      (85, 346, 1075, 381, "남은 질문: 어떤 조각을 어휘에 넣을지 누가 정하나? 데이터가 정해요!"),
      (340, 680, 1065, 706, f"GPT, Claude, Llama, EXAONE 등 모든 현대 {K('llm','이')} 서브워드로 잘라요.")),
  prof(W1,
      "단어는 너무 크게, 글자는 너무 작게 자른 거라면 답은 서브워드예요. 모든 토끼를 다 잡는 거예요.",
      "가장 중요한 질문은 어떤 조각을 어휘에 넣어 단어를 표현할 거냐예요.",
      "규칙으로 정하지 않고, 아주 큰 말뭉치에서 데이터가 스스로 조각을 정하게 해요. 그 알고리즘이 오늘 배우는 BPE 예요."),
  points("앞 쪽과 이어 보기",
      f"7쪽 단어 단위의 {K('oov')} 문제 → 서브워드는 조각으로 이어 쓰니 해결",
      "9쪽 글자 단위의 긴 줄 문제 → 자주 나오는 덩어리는 통째라 해결",
      "9쪽 뜻 없는 조각 문제 → un, able 같은 조각에는 뜻이 있어 해결"),
 ],
 "pass4": [
  check("\"Let the data decide!\" 가 뜻하는 것은?",
      ["언어학자가 조각 목록을 손으로 정한다", "말뭉치에서 자주 나오는 조각을 세어 어휘를 정한다", "글자 26개만 쓴다"], 1,
      f"서브워드 어휘는 {K('corpus','를')} 세어서 만들어요. 그 대표 방법이 11쪽 {K('bpe','예요')}."),
  english("답안 문장: 서브워드",
      f"{K('sub')}는 자주 나오는 덩어리는 통째로, 드문 단어는 조각으로 나눠 세 장점을 함께 얻는다.",
      "세 장점: OOV 없음, 적당한 줄 길이, 뜻 있는 조각. 어떤 조각을 넣을지는 데이터가 정해요."),
 ]})

# p.11 BPE algorithm
S.append({"p": 11, "title": "BPE: 알고리즘 (The Algorithm)",
 "pass1": [
  say(f"데이터가 조각을 정하는 대표 방법이 {K('bpe','예요')}.",
      "글자에서 시작해서, 가장 자주 붙어 나오는 두 조각을 한 조각으로 붙여요.",
      "붙일 때마다 '무엇을 붙였는지' 한 줄 적어요.",
      "목표 크기가 될 때까지 되풀이해요. 세고, 붙이고, 또 세고, 붙이고."),
  analogy("레고 접착하기",
      "레고 조각을 한 줄로 늘어놓고 가장 자주 나란히 있는 두 조각을 접착제로 붙여요. 접착 순서를 공책에 적어 두고, 또 되풀이해요.",
      ["낱개 레고 조각", "글자(또는 바이트)"],
      ["가장 자주 나란히 있는 두 조각", "가장 흔한 이웃 쌍"],
      ["접착해서 생긴 큰 조각", "새 토큰"],
      ["공책에 적은 접착 순서", K("merge")]),
 ],
 "pass2": [
  compare("슬라이드 네 단계 영어 → 우리말", ["단계", "영어 원문", "우리말 뜻"],
      ["1", "Initialize the vocabulary with characters (or bytes)", "어휘를 글자(또는 바이트)로 시작해요"],
      ["2", "Find the most frequent adjacent pair", "가장 자주 나오는 이웃 쌍을 찾아요"],
      ["3", "Merge that pair into a new token; record the merge rule", "그 쌍을 새 토큰으로 붙이고 규칙을 적어요"],
      ["4", "Repeat 2-3 until the vocabulary reaches the target size", "목표 어휘 크기가 될 때까지 2~3을 되풀이해요"]),
  points("용어 뜻 풀기",
      f"{K('bpe')}: 원래 1994년 압축 방법이에요. 2016년 Sennrich 등이 NLP 로 가져왔어요.",
      "adjacent pair(이웃 쌍): 바로 옆에 붙어 있는 두 조각이에요.",
      f"{K('merge')}: 'a 와 b 를 붙여라' 한 줄이에요. 순서가 중요해요.",
      "target size(목표 크기): 멈추는 조건이에요. 어휘 크기나 병합 횟수로 정해요."),
  check("BPE 가 학습해서 남기는 것, 곧 토크나이저 그 자체는?",
      ["단어 사전", "순서가 있는 병합 규칙 목록", "문법 규칙 책"], 1,
      f"\"that list IS the tokenizer\". 순서 있는 {K('merge')} 목록이 곧 {K('tokr','예요')}."),
 ],
 "pass3": [
  look("BPE 알고리즘 쪽에서 볼 곳",
      (85, 155, 970, 190, f"Byte-Pair Encoding (Sennrich et al. 2016): {K('bpe')}. 원래는 1994년 압축 알고리즘이에요."),
      (110, 200, 760, 238, "1. 어휘를 글자(또는 바이트)로 시작해요."),
      (110, 245, 760, 283, f"2. {K('corpus')}에서 가장 자주 나오는 이웃 쌍을 찾아요."),
      (110, 290, 760, 328, "3. 그 쌍을 새 토큰으로 합치고 병합 규칙을 기록해요."),
      (110, 336, 760, 370, "4. 목표 어휘 크기가 될 때까지 2~3을 되풀이해요."),
      (85, 385, 905, 419, f"배우는 것은 순서 있는 {K('merge')} 목록이고, 그 목록이 곧 토크나이저예요.")),
  prof(W1,
      "BPE 는 원래 1994년 데이터 압축 알고리즘이에요. 2016년 기계 번역에 들어왔고, 그 뒤 거의 모든 모델의 표준이 됐어요.",
      "원하는 어휘 크기가 될 때까지, 또는 병합 횟수를 미리 정해 두고 거기까지 되풀이해요.",
      "영원히 계속하면 결국 단어 단위가 돼요. 종료 조건이 있어서 중간의 서브워드가 되는 거예요."),
  steps("BPE 한 바퀴를 말로",
      ["모든 단어를 글자로 쪼개고, 단어 끝에 </w> 표시를 붙여요",
       "이웃 쌍마다 몇 번 나오는지 세요(단어 빈도만큼 곱해서)",
       "1등 쌍을 골라 말뭉치 전체에서 한 조각으로 붙여요",
       "병합 규칙 목록 끝에 그 쌍을 적어요",
       "목표 크기가 아니면 두 번째 줄로 돌아가요"],
      "세기 → 붙이기 → 적기 → 되풀이. 다음 쪽에서 직접 손으로 해요."),
  say("실습 N2L p.10 에서 쌍 세기(get_pair_counts)를 코드로 짜요.",
      "N2L p.11 에서 붙이기(merge_pair), N2L p.12 에서 되풀이(train_bpe)를 짜요.",
      "과제 1 Part A 도 이 알고리즘을 한국어 말뭉치에 돌리는 거예요. 과제와 이어지는 부분이에요."),
 ],
 "pass4": [
  check("BPE 의 두 번째 단계에서 찾는 것은?",
      ["가장 긴 단어", "가장 자주 나오는 이웃 토큰 쌍", "가장 드문 글자"], 1,
      "most frequent adjacent pair. 빈도가 가장 큰 이웃 쌍을 찾아 붙여요."),
  english("답안 문장: BPE 알고리즘",
      f"{K('bpe')}는 글자에서 시작해 가장 자주 나오는 이웃 쌍을 병합하고 규칙을 기록하기를 목표 크기까지 반복한다.",
      "① 글자(바이트)로 시작, ② 1등 이웃 쌍 찾기, ③ 병합하고 규칙 기록, ④ 반복. 순서 있는 병합 규칙 목록이 곧 토크나이저예요."),
  warn("헷갈리기 쉬운 점",
      "BPE 는 언어학 지식을 쓰지 않아요. 오직 '세고 붙이기' 예요.",
      "병합 규칙은 순서가 있어요. 새 글을 자를 때도 배운 순서 그대로 적용해요(13쪽)."),
 ]})

# p.12 BPE worked example
S.append({"p": 12, "title": "BPE: 손으로 풀어 보기 (Worked Example)",
 "pass1": [
  say(f"작은 {K('corpus')}로 {K('bpe','를')} 직접 돌려 봐요.",
      "low 5번, lower 2번, newest 6번, widest 3번, 모두 16단어예요.",
      f"처음엔 모두 글자로 쪼개 놓고, 가장 자주 붙어 있는 쌍부터 접착해요. 접착 순서가 {K('merge','이에요')}."),
  figure("접착이 한 번씩 일어나는 모습", FIG_BPE,
      "e+s → es, es+t</w> → est</w>, l+o → lo. 자주 붙는 조각부터 한 조각이 돼요.", 3),
 ],
 "pass2": [
  compare("슬라이드 영어 → 우리말", ["영어 원문", "우리말 뜻"],
      ["Toy corpus", "연습용 작은 말뭉치"],
      ["</w> marks end-of-word", "</w> 는 '단어 끝' 표시예요"],
      ["vocab = characters", "처음 어휘 = 글자들"],
      ["\"e s\" appears 9× → merge into \"es\"", "e s 가 9번 나오니 es 로 붙여요"],
      ["keep merging → frequent chunks become single tokens", "계속 붙이면 자주 나오는 덩어리가 한 토큰이 돼요"]),
  points("</w> 는 왜 붙일까?",
      "단어가 끝났다는 표시예요.",
      "그래야 단어 끝의 est(newest 의 끝)와 단어 중간의 est 를 구별할 수 있어요.",
      "슬라이드는 </w> 를 마지막 글자에 붙여 't</w>' 처럼 한 조각으로 적었어요."),
  check("처음 상태에서 'e s' 쌍은 몇 번 나올까요?",
      ["6번", "3번", "9번", "16번"], 2,
      "newest(6번)와 widest(3번)에 한 번씩 있으니 6 + 3 = 9번이에요."),
 ],
 "pass3": [
  look("Worked Example 쪽에서 볼 곳",
      (85, 155, 1040, 190, "Toy corpus: low ×5, lower ×2, newest ×6, widest ×3. </w> 는 단어 끝 표시예요."),
      (105, 265, 1100, 322, "start: 모두 글자로 쪼갠 상태. vocab = characters."),
      (105, 338, 1150, 393, "merge 1: \"e s\" 가 9번 → es 로 붙여요."),
      (105, 408, 1160, 463, "merge 2: \"es t\" 가 9번 → est 로 붙여요(정확히는 es + t</w>)."),
      (105, 479, 1140, 534, "merge 3: \"l o\" 가 7번 → lo 로 붙여요."),
      (105, 550, 1300, 605, "...: 계속 붙이면 자주 나오는 덩어리가 한 토큰이 돼요. 이 줄은 모양만 보여 준 거예요.")),
  steps("손계산 1: 처음 이웃 쌍 세기 (단어 빈도만큼 곱해서)",
      ["low ×5 = l o w</w>: (l,o) 5, (o,w</w>) 5",
       "lower ×2 = l o w e r</w>: (l,o) 2, (o,w) 2, (w,e) 2, (e,r</w>) 2",
       "newest ×6 = n e w e s t</w>: (n,e) 6, (e,w) 6, (w,e) 6, (e,s) 6, (s,t</w>) 6",
       "widest ×3 = w i d e s t</w>: (w,i) 3, (i,d) 3, (d,e) 3, (e,s) 3, (s,t</w>) 3",
       "합치기: (e,s) 9, (s,t</w>) 9, (w,e) 8, (l,o) 7, (n,e) 6, (e,w) 6, (o,w</w>) 5"],
      "1등은 9번으로 (e,s) 와 (s,t</w>) 가 동점이에요. 슬라이드는 (e,s) 를 골랐어요.",
      given="말뭉치 16단어, 처음 어휘는 글자 11종"),
  steps("손계산 2: 병합 세 번 따라가기",
      ["병합 1: e + s → es (9번). newest = n e w es t</w>, widest = w i d es t</w>",
       "다시 세기: (es, t</w>) 9번이 1등. (w,e) 는 lower 에만 남아 2번",
       "병합 2: es + t</w> → est</w> (9번). newest = n e w est</w>",
       "다시 세기: (l,o) 7번이 1등(low 5 + lower 2)",
       "병합 3: l + o → lo (7번). low = lo w</w>, lower = lo w e r</w>",
       "다시 세기: (n,e), (e,w), (w,est</w>) 가 6번, (lo,w</w>) 가 5번"],
      f"{K('merge')} 3줄: (e,s), (es,t</w>), (l,o). 여기서 멈추면 이것이 {K('tokr')}예요."),
  prof(W1,
      "es 가 9번으로 가장 많아요. st 도 똑같이 9번으로 가장 많아요.",
      "무엇을 먼저 고를지는 동점 규칙(tie-breaking)을 아무거나 정해도 돼요. 보통은 알파벳 순이에요.",
      "종료 조건 없이 계속 붙이면 결국 low, lower 처럼 단어 4개만 남아 단어 단위와 똑같아져요.",
      "est 가 최상급 접미사라고 아무도 알려 주지 않았는데, 많이 나왔다는 데이터만으로 알고리즘이 est 를 한 토큰으로 만들어요."),
  prof(W3,
      "실습 코드에서는 </w> 를 따로 한 조각으로 둬요. 그래서 병합 1 es, 병합 2 est, 병합 3 est 와 </w> 를 합치기가 나와요.",
      "그다음 l 과 o, lo 와 w 를 합치는 식으로 병합 규칙이 쌓여요. 이 코퍼스는 과제에서도 이런 식으로 나올 거예요."),
  compare("실습 방식(</w> 따로)으로 8번 병합하면", ["순서", "붙인 쌍", "횟수"],
      ["1", "e + s → es", "9"], ["2", "es + t → est", "9"], ["3", "est + </w> → est</w>", "9"],
      ["4", "l + o → lo", "7"], ["5", "lo + w → low", "7"], ["6", "n + e → ne", "6"]),
  say("표 뒤로 7번째 ne + w → new (6번), 8번째 new + est</w> → newest</w> (6번)이 이어져요.",
      "실습 N2L p.12 에서 이 과정을 train_bpe 코드로 짜요. 출력이 이 표와 같아요.",
      "N2L p.9 가 이 말뭉치, p.10 이 쌍 세기, p.11 이 붙이기예요."),
 ],
 "pass4": [
  exam("예상 문제 (BPE 손계산)",
      "Corpus: low ×5, lower ×2, newest ×6, widest ×3 (with </w>). Give the first three merges and their counts.",
      "이 말뭉치에 BPE 를 돌릴 때 처음 세 번의 병합과 각 횟수를 쓰세요.",
      ["글자로 쪼개요: l o w</w>, l o w e r</w>, n e w e s t</w>, w i d e s t</w>",
       "쌍을 빈도만큼 곱해 세요: (e,s) 9, (s,t</w>) 9, (w,e) 8, (l,o) 7 ...",
       "병합 1: e+s → es (9). 동점 (s,t</w>) 는 규칙에 따라 뒤로",
       "다시 세면 (es,t</w>) 9 → 병합 2: est</w> (9)",
       "다시 세면 (l,o) 7 → 병합 3: lo (7)"],
      "es (9) → est (9) → lo (7)"),
  check("병합 1 (e+s) 뒤에 (w,e) 쌍은 몇 번 남을까요?",
      ["8번", "6번", "2번", "0번"], 2,
      "newest 의 w e 는 e 가 es 로 붙어 w es 가 됐어요. lower 의 w e 만 남아 2번이에요."),
  warn("헷갈리기 쉬운 점",
      "쌍은 단어 빈도만큼 곱해서 세요. newest 가 6번 나오면 그 안의 쌍도 6번이에요.",
      "처음에 (w,e) 는 8번으로 (l,o) 7번보다 많아요. 하지만 병합 1 뒤에는 2번으로 줄어요. 매번 다시 세야 해요.",
      "슬라이드 마지막 '...' 줄(low</w>, low e r</w>)은 빈도 순서를 그대로 따른 결과가 아니라 모양을 보여 준 줄이에요. 엄격히 따르면 병합 4는 6번짜리 쌍이에요."),
 ]})

# p.13 Applying BPE, Byte-level BPE
S.append({"p": 13, "title": "BPE 적용하기와 바이트 수준 BPE (Byte-Level BPE)",
 "pass1": [
  say("BPE 를 다 배웠으면, 새 글은 어떻게 자를까요?",
      "새 단어를 글자로 쪼갠 뒤, 배운 병합 규칙을 배운 순서대로 다시 붙여요.",
      "처음 보는 lowest 도 low + est 로 잘 잘려요."),
  say(f"GPT-2 부터는 글자 대신 256가지 바이트에서 시작해요. 이것이 {K('blbpe','예요')}.",
      "이모지든 한자든 오타든 모든 입력은 바이트라서, [UNK] 가 아예 생길 수 없어요."),
 ],
 "pass2": [
  compare("슬라이드 영어 → 우리말", ["영어 원문", "우리말 뜻"],
      ["At inference", "학습이 끝난 뒤 실제로 쓸 때"],
      ["replay the learned merges in the same order", "배운 병합 규칙을 같은 순서로 다시 적용해요"],
      ["unseen words still work", "처음 보는 단어도 잘 잘려요"],
      ["start from the 256 bytes instead of characters", "글자 대신 256개 바이트에서 시작해요"],
      ["UNK simply cannot exist", "[UNK] 가 아예 있을 수 없어요"]),
  compare("글자 BPE vs 바이트 수준 BPE", ["", "글자에서 시작", "바이트에서 시작"],
      ["처음 어휘", "말뭉치에 나온 글자들", "256가지 바이트"],
      ["처음 보는 글자(이모지 등)", "[UNK] 가 될 수 있음", "바이트로 쪼개면 됨"],
      ["쓰는 곳", "11~12쪽 예제", "GPT-2, GPT-4o, Llama, Claude 계열"]),
  check("바이트 수준 BPE 에서 [UNK] 가 생기지 않는 까닭은?",
      ["어휘가 아주 커서", "어떤 입력이든 256가지 바이트로 나타낼 수 있어서", "영어만 받아서"], 1,
      f"모든 글은 결국 바이트예요. 256가지 바이트가 처음부터 {K('vocab')}에 다 있으니 모르는 조각이 없어요."),
 ],
 "pass3": [
  look("Applying BPE 쪽에서 볼 곳",
      (85, 155, 1075, 220, "At inference: 새 글을 글자로 쪼개고 배운 병합을 같은 순서로 다시 적용해요. lowest → (es) → (est) → (lo) → low + est."),
      (85, 235, 980, 269, f"Byte-level BPE (GPT-2 부터 표준): 글자 대신 256개 바이트에서 시작해요. {K('blbpe')}."),
      (85, 284, 885, 318, "이모지, 한자, 아랍 문자, 오타: 무엇이든 바이트라서 UNK 가 존재할 수 없어요."),
      (85, 332, 785, 366, "GPT-4o, Llama, Claude 모두 바이트 수준 BPE 계열 토크나이저를 써요."),
      (340, 680, 1065, 706, "데이터로 한 번 학습하면, 앞으로 올 모든 언어의 모든 글을 자를 수 있어요.")),
  steps("손계산: 처음 보는 lowest 자르기 (실습 방식 병합 규칙)",
      ["글자로 쪼개기: l o w e s t </w>",
       "규칙 1 (e,s): l o w es t </w>",
       "규칙 2 (es,t): l o w est </w>",
       "규칙 3 (est,</w>): l o w est</w>",
       "규칙 4 (l,o): lo w est</w>",
       "규칙 5 (lo,w): low est</w>. 규칙 6~8 은 붙일 쌍이 없어요"],
      "lowest → low + est</w>. 학습 때 없던 단어도 [UNK] 없이 잘려요.",
      given="병합 규칙 순서: (e,s), (es,t), (est,</w>), (l,o), (lo,w), (n,e), (ne,w), (new,est</w>)"),
  steps("같은 규칙으로 두 단어 더",
      ["newer: n e w e r </w> → 규칙 6 (n,e) → ne w e r </w> → 규칙 7 (ne,w) → new e r </w>",
       "e 와 r 을 붙이는 규칙은 없어요. 그래서 new, e, r, </w> 로 남아요",
       "widow: w i d o w </w> 에 맞는 규칙이 하나도 없어요",
       "그래서 w, i, d, o, w, </w> 글자 그대로 남아요"],
      "newer → new + e + r, widow → 글자 6조각. 모르는 조각은 글자로 떨어질 뿐 [UNK] 가 아니에요."),
  prof(W1,
      "학습이란 몇 번째 병합에서 무엇을 붙일지 정해 두는 거예요. 새 단어가 오면 그 규칙 순서를 그대로 적용해요.",
      "GPT-2 는 글자가 아니라 256바이트 단위로 쪼개서 시작해요.",
      "시작 단위, 병합 규칙, 동점 규칙은 구현마다 다르지만, 최소 단위로 쪼갠 뒤 병합 규칙을 쌓는 뼈대는 같아요."),
  prof(W3,
      "실습에서 GPT-2 로 한국어를 자르면 이상한 글자들이 보여요. 오류가 아니에요.",
      "GPT-2 토크나이저는 바이트 수준이라 한글을 바이트 중간에서 잘라요. 이어 붙여 디코딩하면 한국어가 돼요."),
  say("실습 N2L p.13 에서 이 과정을 bpe_tokenize 코드로 짜요. lowest, newer, widow 를 그대로 넣어 봐요.",
      "N2L p.14 에서 GPT-2 의 바이트 수준 BPE 가 한국어를 어떻게 자르는지 직접 봐요."),
 ],
 "pass4": [
  check("학습한 병합 규칙으로 새 단어를 자를 때 규칙은 어떤 순서로 적용할까요?",
      ["빈도가 낮은 규칙부터", "배운 순서 그대로", "아무 순서나"], 1,
      "replay the learned merges in the same order. 학습 때 적은 순서 그대로 적용해요."),
  check("GPT-2 에서 표준이 된 바이트 수준 BPE 의 출발 어휘 크기는?",
      ["26", "256", "50,000", "128,000"], 1,
      "256가지 바이트에서 시작해요. 5만은 GPT-2 의 최종 어휘 크기예요(15쪽)."),
  english("답안 문장: 바이트 수준 BPE",
      f"{K('blbpe')}는 256개 바이트에서 시작하므로 어떤 입력이든 표현할 수 있어 [UNK] 가 생기지 않는다.",
      "이모지, 한자, 오타도 바이트예요. 새 글은 쪼갠 뒤 학습된 병합 규칙을 같은 순서로 적용해요."),
 ]})

# p.14 WordPiece & Unigram
S.append({"p": 14, "title": "WordPiece 와 Unigram",
 "pass1": [
  say("BPE 말고도 서브워드를 만드는 방법이 두 가지 더 있어요.",
      f"{K('wp','는')} 그냥 많이 붙는 쌍 대신, 말뭉치를 가장 잘 설명하는 쌍을 붙여요.",
      f"{K('uni','는')} 거꾸로, 큰 목록에서 시작해 쓸모없는 조각을 깎아 내요.",
      "세 방법 모두 생각은 하나예요. 자주 나오는 덩어리가 토큰이 된다."),
  compare("세 가지 요리법", ["방법", "출발", "하는 일"],
      ["BPE", "작은 조각", "자주 붙는 쌍을 붙이기"],
      ["WordPiece", "작은 조각", "말뭉치를 잘 설명하는 쌍 붙이기"],
      ["Unigram", "큰 후보 목록", "덜 쓸모 있는 조각 깎기"]),
 ],
 "pass2": [
  compare("슬라이드 영어 → 우리말", ["영어 원문", "우리말 뜻"],
      ["merge the pair that most increases corpus likelihood, not raw frequency", "그냥 빈도가 아니라 말뭉치 우도를 가장 많이 올리는 쌍을 붙여요"],
      ["continuation pieces get ##", "단어 뒤에 이어 붙는 조각에는 ## 를 달아요"],
      ["start big, prune the least useful pieces", "크게 시작해서 가장 덜 쓸모 있는 조각을 쳐내요"],
      ["treats whitespace as just another symbol (▁)", "띄어쓰기도 ▁ 라는 기호 하나로 다뤄요"],
      ["three recipes, one philosophy", "요리법은 셋, 생각은 하나"]),
  points("용어 뜻 풀기",
      f"{K('wp')}: BERT 가 쓰는 방법이에요. playing → play + ##ing.",
      f"{K('like')}: 이렇게 합치면 말뭉치가 얼마나 그럴듯해지는지 재는 값이에요.",
      f"{K('uni')}: 문장마다 확률이 가장 높은 자르기를 골라요. 확률로 보는 방법이에요.",
      f"{K('spm')}: 띄어쓰기를 ▁ 로 다루는 도구예요. 한국어, 일본어처럼 띄어쓰기가 들쭉날쭉한 언어에 좋아요."),
  check("큰 후보 어휘에서 시작해 덜 쓸모 있는 조각을 줄여 나가는 방법은?",
      ["BPE", "WordPiece", "Unigram"], 2,
      f"{K('uni','는')} 크게 시작해서 깎아 내요. BPE, WordPiece 는 작게 시작해서 붙여요."),
 ],
 "pass3": [
  look("WordPiece & Unigram 쪽에서 볼 곳",
      (85, 153, 1290, 218, f"WordPiece (BERT): 빈도가 아니라 {K('like')}를 가장 많이 올리는 쌍을 합쳐요. 이어지는 조각엔 ##. playing → play + ##ing"),
      (85, 230, 910, 293, "Unigram LM: 반대로 크게 시작해 가장 덜 쓸모 있는 조각을 쳐내요. 문장마다 확률이 가장 높은 자르기를 골라요."),
      (85, 305, 1240, 368, f"SentencePiece: 띄어쓰기를 ▁ 기호로 다뤄요. 띄어쓰기가 불안정한 한국어, 일본어에 좋아요."),
      (85, 380, 945, 413, "실전 감각: 세 방법 모두 '자주 나오는 덩어리가 토큰이 된다' 는 한 철학이에요."),
      (95, 448, 1305, 592, "표: BPE 는 작게 시작 → 자주 나오는 쌍 합치기, WordPiece 는 작게 시작 → 말뭉치를 잘 설명하는 점수로 합치기, Unigram 은 큰 후보 → 덜 쓸모 있는 조각 제거.")),
  prof(W1,
      "우도를 높인다는 건 빈도와 거의 비슷하지만, 따로 나오는 횟수(사전 개념)를 함께 봐요.",
      "t 와 h 가 각각 천 번씩 나오면 th 도 꽤 많겠죠. q 는 적게 나오는데 qu 는 거의 늘 붙어 나와요.",
      "점수는 '붙어 나온 횟수 ÷ (a 횟수 × b 횟수)' 예요. 적게 나오는데도 붙어 나오는 쌍을 더 우선해요.",
      "이 설명은 PPT 에 넣지 않고 말로만 했어요. 개념만 알면 돼요."),
  formula("워드피스 점수 (교수님 말로 설명한 식)", r"\mathrm{score}(a,b) = \frac{f(ab)}{f(a) \times f(b)}",
      [(r"f(ab)", "a 와 b 가 붙어서 나온 횟수"),
       (r"f(a)", "a 가 나온 전체 횟수"),
       (r"f(b)", "b 가 나온 전체 횟수"),
       (r"\frac{\cdot}{f(a) \times f(b)}", "원래 흔한 조각이면 점수를 깎아요")],
      "따로는 드문데 늘 붙어 다니는 쌍일수록 점수가 높아요."),
  steps("손계산: BPE 와 워드피스가 다른 쌍을 고르는 예 (설명용 숫자)",
      ["t 1000번, h 1000번, th 400번 / q 300번, u 1000번, qu 300번이라고 해요",
       "BPE 는 붙은 횟수만 봐요: th 400 > qu 300 → th 를 먼저 붙여요",
       "워드피스 th: 400 ÷ (1000 × 1000) = 0.0004",
       "워드피스 qu: 300 ÷ (300 × 1000) = 0.001",
       "0.001 > 0.0004 → 워드피스는 qu 를 먼저 붙여요(2.5배 높음)"],
      "BPE 는 th, 워드피스는 qu. q 는 거의 늘 u 와 붙어 다니니까요.",
      given="t, h 1000번과 q 300번은 교수님 예, 나머지는 설명을 위해 채운 숫자"),
  prof(W1,
      "SentencePiece 는 알고리즘이 아니라 BPE, 유니그램 같은 방법을 구현해 둔 라이브러리예요.",
      "세 방법의 공통 목표는 같아요. 글자보다 줄을 짧게, 단어보다 새 단어에 유연하게, 알맞은 서브워드 단위를 찾는 거예요."),
 ],
 "pass4": [
  check("다음 중 짝이 틀린 것은?",
      ["BPE: 자주 나오는 쌍을 반복해서 합친다", "WordPiece: 우도를 가장 많이 올리는 쌍을 합친다",
       "Unigram: 글자에서 시작해 쌍을 합친다", "SentencePiece: 띄어쓰기를 ▁ 기호로 다룬다"], 2,
      "Unigram 은 큰 후보 목록에서 시작해 덜 쓸모 있는 조각을 지워요. 합치는 방향이 아니에요."),
  check("BERT 의 WordPiece 로 playing 을 자르면?",
      ["play + ing", "play + ##ing", "##play + ing"], 1,
      "단어 뒤에 이어지는 조각에 ## 를 달아요. play + ##ing."),
  english("답안 문장: 세 서브워드 방법 비교",
      "BPE 는 빈도로 병합하고, WordPiece 는 우도를 가장 높이는 쌍을 병합하며, Unigram 은 큰 어휘에서 조각을 제거한다.",
      "BPE, WordPiece 는 작게 시작해 붙이고, Unigram 은 크게 시작해 깎아요. 셋 다 '자주 나오는 덩어리가 토큰' 이에요."),
  warn("헷갈리기 쉬운 점",
      "SentencePiece 는 네 번째 알고리즘이 아니라 도구(라이브러리)예요. 안에 BPE 나 Unigram 이 들어 있어요.",
      "워드피스 점수식은 슬라이드에 없고 교수님이 말로 설명한 거예요. 개념(드문데 늘 붙는 쌍 우대)을 기억해요."),
 ]})

# p.15 Tokenizers in the Wild
S.append({"p": 15, "title": "Tokenizers in the Wild: 실제 토크나이저",
 "pass1": [
  say("실제 모델의 토크나이저는 어떤 모습일까요?",
      "어휘 목록은 점점 커지고 있어요. 더 많은 언어를 담으려고요.",
      "토큰은 곧 돈이에요. 요금을 토큰 수로 매겨요.",
      f"{K('llm')}의 이상한 실수 절반은 토큰 때문이에요."),
  points("이 쪽의 네 가지 이야기",
      f"{K('vocab')} 크기: GPT-2 → Llama 3 → GPT-4o 로 커져요",
      f"{K('special')}: 모델 행동을 바꾸는 스위치 조각",
      "토큰 = 돈: 효율 좋은 토크나이저가 곧 싼 모델",
      "토큰 = 사각지대: 글자를 못 봐서 생기는 실수"),
 ],
 "pass2": [
  compare("슬라이드 영어 → 우리말", ["영어 원문", "우리말 뜻"],
      ["growing to embrace more languages", "더 많은 언어를 품으려고 커지고 있어요"],
      ["switches that steer model behavior", "모델 행동을 조종하는 스위치예요"],
      ["tokenizer efficiency is cost", "토크나이저 효율이 곧 비용이에요"],
      ["the model sees str + awberry, never letters", "모델은 str + awberry 를 볼 뿐 글자를 보지 않아요"],
      ["tokenizer artifacts", "토크나이저가 만든 부작용"]),
  points("용어 뜻 풀기",
      f"{K('special')}: <|endoftext|>(글 끝), [CLS], [SEP](BERT 의 문장 표시), 채팅 틀 토큰 같은 약속 조각이에요.",
      f"{K('ctx')}: 모델이 한 번에 볼 수 있는 토큰 수 한도예요. 이것도 토큰으로 세요.",
      "API pricing(API 요금): 입력, 출력 토큰 수에 따라 돈을 내요."),
  check("\"strawberry 에 r 이 몇 개?\" 를 LLM 이 틀리기 쉬운 까닭은?",
      ["영어를 몰라서", "글자가 아니라 str + awberry 같은 토큰으로 보기 때문에", "숫자를 못 세서"], 1,
      f"모델은 {K('tok')} 단위로 봐요. 글자 하나하나는 토큰 안에 숨어 있어요."),
 ],
 "pass3": [
  look("Tokenizers in the Wild 쪽에서 볼 곳",
      (85, 153, 1140, 188, f"Real vocabulary sizes: GPT-2 50k → Llama 3 128k → GPT-4o 약 200k. 더 많은 언어를 품으려고 커져요."),
      (85, 199, 1110, 233, f"{K('special')}: <|endoftext|>, [CLS], [SEP], 채팅 틀 토큰. 모델 행동을 조종하는 스위치예요."),
      (85, 243, 1090, 278, f"Tokens = money: API 요금과 {K('ctx')} 한도 모두 토큰으로 세요. 효율이 곧 비용이에요."),
      (85, 288, 1210, 351, "Tokens = blind spots: strawberry 의 r 개수를 틀리는 이유, 모델은 str + awberry 만 봐요. 숫자도 12345 → 123 + 45 처럼 이상하게 잘려요."),
      (380, 680, 1025, 706, "인터넷에서 보는 'LLM 의 이상한 실패' 절반은 토크나이저 부작용이에요.")),
  steps("손계산: 어휘 크기 비교",
      ["GPT-2 약 50k(5만), Llama 3 약 128k(12만 8천), GPT-4o 약 200k(20만)",
       "Llama 3 ÷ GPT-2 = 128 ÷ 50 = 2.56배",
       "GPT-4o ÷ GPT-2 = 200 ÷ 50 = 4배"],
      "몇 년 사이 어휘가 약 4배로 커졌어요. 여러 언어를 담기 위해서예요."),
  prof(W1,
      "어휘 크기는 GPT-2 의 5만에서 요즘 거의 20만 수준까지 커졌어요. 다국어를 잘 담기 위해서예요.",
      "EXAONE 도 버전이 갈수록 지원 언어가 늘었고, 언어가 늘면 어휘가 커질 수밖에 없어요.",
      "LLM 에서는 모든 것이 돈이에요. 같은 성능이면 토큰을 적게 쓰는 게 이득이에요. 너무 잘게 쪼개면 토큰이 늘어 돈이 많이 들어요."),
  prof(W1,
      "strawberry 의 r 개수를 세게 해서 모델을 시험하는 사람들이 있었어요.",
      "철자 단위로 봤으면 쉬운 일인데, str 과 awberry 처럼 쪼개면 그 안의 글자를 찾기 어려워요.",
      "생각을 많이 하는 요즘 모델도 구조적으로 어려운 문제예요. 다만 최신 모델은 이제 대부분 풀어요."),
 ],
 "pass4": [
  check("슬라이드에 나온 어휘 크기 순서로 맞는 것은?",
      ["GPT-2 200k → Llama 3 128k → GPT-4o 50k", "GPT-2 50k → Llama 3 128k → GPT-4o 약 200k", "모두 256"], 1,
      "GPT-2 50k → Llama 3 128k → GPT-4o 약 200k. 256 은 바이트 수준 BPE 의 출발 어휘예요."),
  english("답안 문장: 토큰 = 돈, 토큰 = 사각지대",
      f"요금과 {K('ctx')} 한도가 토큰 수로 계산되므로 토크나이저 효율이 곧 비용이다.",
      "또 모델은 글자가 아니라 토큰(str + awberry)을 봐서 글자 세기, 자릿수 계산(12345 → 123 + 45)을 틀려요."),
  warn("헷갈리기 쉬운 점",
      "어휘가 크면 같은 글을 더 적은 토큰으로 담을 수 있지만, 어휘 표(임베딩)도 그만큼 커져요. 슬라이드의 요점은 '다국어를 담으려고 커진다' 예요.",
      "[CLS], [SEP] 는 BERT 계열, <|endoftext|> 는 GPT 계열의 특수 토큰이에요."),
 ]})

# p.16 2부 구분
S.append({"p": 16, "title": "2부 Korean Tokenization (구분 쪽)",
 "pass1": [
  say("여기서부터 2부, 한국어 토큰화예요.",
      f"부제는 '{K('aggl')}를 서브워드로 자르기' 예요.",
      "방금 배운 도구를 한국어에 들이대면 무슨 일이 생기는지 봐요.",
      "형태소 분석기, 한국어 BPE, 토큰이 몇 배로 늘어나는 문제까지 가요."),
 ], "pass2": [], "pass3": [], "pass4": []})

# p.17 Korean Is Agglutinative
S.append({"p": 17, "title": "한국어는 교착어 (Korean Is Agglutinative)",
 "pass1": [
  say(f"한국어는 {K('aggl','예요')}.",
      "줄기 뒤에 문법 조각을 줄줄이 붙여서 한 덩어리를 만들어요.",
      "'먹었겠더라' 한 덩어리 안에 뜻 조각이 네 개나 들어 있어요.",
      "그래서 띄어쓰기로 자르면 최악이에요."),
  figure("먹었겠더라를 뜻 조각으로", FIG_MORPH,
      "먹- + -었- + -겠- + -더라. 영어라면 서너 단어가 필요한 뜻이 한 어절에 붙어 있어요.", 4),
 ],
 "pass2": [
  compare("슬라이드 영어 → 우리말", ["영어 원문", "우리말 뜻"],
      ["Korean is agglutinative", "한국어는 교착어예요"],
      ["grammatical morphemes stack onto a stem to form one word (어절)", "문법 형태소가 줄기 위에 쌓여 한 어절이 돼요"],
      ["Splitting on spaces is the worst case", "띄어쓰기로 자르기가 최악이에요"],
      ["four morphemes glued into one word", "형태소 네 개가 한 단어로 붙었어요"],
      ["the unit problem is far worse in Korean", "단위 문제가 한국어에서 훨씬 심해요"]),
  points("용어 뜻 풀기",
      f"{K('aggl')}: 줄기에 조사, 어미 같은 문법 조각을 붙여 단어를 만드는 언어예요. 한국어, 일본어.",
      f"{K('morph')}: 뜻을 가진 가장 작은 말 조각이에요. 먹-, -었-, -겠-, -더라.",
      f"{K('eojeol')}: 띄어쓰기로 나뉜 한 덩어리예요. '먹었겠더라' 가 어절 하나예요.",
      "stem(어간): 뜻의 줄기예요. '먹-' 이에요."),
  check("'먹었겠더라' 에서 '-겠-' 이 나타내는 뜻은?",
      ["과거", "추측", "회상"], 1,
      "-었- 은 과거(past), -겠- 은 추측(conjecture), -더라 는 회상(retrospective)이에요."),
 ],
 "pass3": [
  look("Korean Is Agglutinative 쪽에서 볼 곳",
      (85, 153, 1015, 188, f"Korean is agglutinative: 문법 {K('morph')}가 줄기에 쌓여 한 어절이 돼요."),
      (85, 196, 1115, 231, "띄어쓰기로 자르면 최악: 먹었겠더라 / 먹었더라 / 먹겠더라 ... 모두 다른 '단어' 가 돼요."),
      (175, 335, 1160, 490, "먹- eat(어간), -었- past(과거), -겠- conjecture(추측), -더라 retrospective(회상). 뜻: \"(그가) 먹었을 것이더라\""),
      (315, 538, 1085, 562, "형태소 네 개가 한 단어로 붙었어요. 영어라면 서너 단어가 필요해요."),
      (295, 680, 1110, 706, "지난주 예고가 오늘의 본론이에요. 단위 문제가 한국어에서 훨씬 심해요.")),
  prof(W1,
      "영어는 굴절어, 한국어는 교착어예요. 교착어는 어간에 형태소가 붙어서 어절이 돼요.",
      "먹었겠더라는 공백으로 보면 한 단어지만, 뜻이 담긴 형태소 네 개가 붙어 있어요. 영어라면 서너 단어예요.",
      "그래서 한국어, 일본어 같은 교착어를 공백 단위로 자르면 거의 재앙이에요.",
      "동사 하나가 수천 가지로 활용돼서, 굴절어(영어, 라틴어, 독일어)보다 어휘 폭발이 훨씬 심해요."),
  compare("띄어쓰기로 잘랐을 때 vs 형태소로 봤을 때", ["어절", "띄어쓰기 단위", "형태소"],
      ["먹었겠더라", "새 단어 1개", "먹 + 었 + 겠 + 더라"],
      ["먹었더라", "또 다른 새 단어", "먹 + 었 + 더라"],
      ["먹겠더라", "또 다른 새 단어", "먹 + 겠 + 더라"]),
  say("세 어절은 띄어쓰기로는 단어 3개가 따로 필요해요.",
      "형태소로 보면 먹, 었, 겠, 더라 네 조각만 돌려 쓰면 돼요.",
      "7쪽의 '어휘 폭발' 이 한국어에서 이렇게 훨씬 커져요."),
 ],
 "pass4": [
  check("'먹었겠더라' 는 형태소 몇 개로 이루어져 있다고 슬라이드가 말할까요?",
      ["2개", "3개", "4개", "5개"], 2,
      "먹- + -었- + -겠- + -더라, 네 개예요. 글자 수(5자)와 헷갈리지 마세요."),
  english("답안 문장: 한국어가 교착어라서 생기는 문제",
      f"한국어는 {K('aggl','로')} 어간에 형태소가 붙어 한 어절이 되므로, 띄어쓰기로 자르면 어휘가 폭발한다.",
      "예: 먹었겠더라 = 먹-(어간) + -었-(과거) + -겠-(추측) + -더라(회상). 활용형마다 다른 단어가 돼요."),
  warn("헷갈리기 쉬운 점",
      "교착어(agglutinative)는 한국어, 일본어예요. 영어는 굴절어(단어 모양 자체가 바뀜)예요.",
      "한국어에서 '공백 단어' 는 사실 어절이에요. 어절 하나에 형태소가 여러 개예요."),
 ]})

# p.18 Morphological Analyzers
S.append({"p": 18, "title": "Route 1: 형태소 분석기 (Morphological Analyzers)",
 "pass1": [
  say("한국어를 자르는 첫 번째 길은 형태소 분석기예요.",
      "언어 지식으로 어절을 뜻 조각(형태소)으로 자르고, 조각마다 품사 이름표를 붙여요.",
      "깔끔하지만 규칙으로 움직여서, 규칙의 약점을 그대로 가져요."),
  compare("형태소 분석기의 좋은 점과 아쉬운 점", ["좋은 점", "아쉬운 점"],
      ["언어학적으로 깔끔한 조각", "앞에서 틀리면 뒤 단계까지 번짐"],
      ["조사, 어미를 정확히 분리", "신조어, 줄임말에 약함"],
      ["검색, 분류에 강함", "사전을 계속 손봐야 함"]),
 ],
 "pass2": [
  compare("슬라이드 영어 → 우리말", ["영어 원문", "우리말 뜻"],
      ["use linguistic knowledge to split words into morphemes + POS tags", "언어 지식으로 단어를 형태소로 자르고 품사 태그를 붙여요"],
      ["the classic workhorses of Korean NLP", "한국어 NLP 의 오래된 일꾼들이에요"],
      ["analyzer mistakes propagate into every later stage", "분석기 실수가 뒤 모든 단계로 번져요"],
      ["dictionaries need maintenance", "사전을 계속 관리해야 해요"],
      ["a rule-based system with rule-based weaknesses", "규칙 기반이라 규칙 기반의 약점이 있어요"]),
  points("용어 뜻 풀기",
      f"{K('analyzer')}: MeCab-ko, Kiwi, Okt, Komoran 같은 도구예요.",
      f"{K('pos')}: 조각마다 붙는 품사 이름표예요. NNG 일반 명사, JX 보조사, VA 형용사, EF 종결 어미.",
      "propagate(번지다): 앞 단계의 실수가 뒤 단계로 그대로 옮겨 가는 거예요."),
  check("형태소 분석기의 약점으로 알맞은 것은?",
      ["조사를 정확히 못 나눈다", "신조어에 약하고 사전을 계속 손봐야 한다", "토큰이 글자보다 길다"], 1,
      "규칙과 사전으로 움직여서, 사전에 없는 신조어에 약하고 관리가 필요해요."),
 ],
 "pass3": [
  look("Morphological Analyzers 쪽에서 볼 곳",
      (85, 153, 1200, 220, f"{K('analyzer')}: 언어 지식으로 형태소 + {K('pos')}. 자연어처리는 재미있다 → 자연어/NNG + 처리/NNG + 는/JX + 재미있/VA + 다/EF"),
      (85, 232, 880, 267, "Tools: MeCab-ko, Kiwi, Okt, Komoran. 한국어 NLP 의 오래된 일꾼들이에요."),
      (85, 280, 1065, 315, "Pros: 언어학적으로 깔끔한 단위, 조사/어미를 정확히 분리, 검색과 분류에 강해요."),
      (85, 327, 1290, 362, "Cons: 실수가 뒤 모든 단계로 번지고, 신조어에 약하고, 사전 관리가 필요해요."),
      (345, 680, 1060, 706, "언어학적으로 아름답지만, 규칙 기반이라 규칙 기반의 약점이 있어요.")),
  steps("예문을 형태소로 나눠 읽기",
      ["자연어처리는 재미있다 → 어절 2개",
       "자연어/NNG: 일반 명사",
       "처리/NNG: 일반 명사",
       "는/JX: 보조사",
       "재미있/VA: 형용사 줄기, 다/EF: 문장을 끝내는 어미"],
      "어절 2개가 형태소 5개로 나뉘어요."),
  prof(W1,
      "그래서 한국어는 형태소를 나누는 게 중요하고, 형태소 분석기를 많이 써요. MeCab, Kiwi 같은 것이 한국어 NLP 의 20년 표준이었어요.",
      "조사와 어미가 정확히 분리되고, 지금도 검색 엔진에서 MeCab 을 쓰는 곳이 있을 만큼 강력해요.",
      "하지만 미리 정해 둔 규칙으로 나누는 규칙 기반이라, 하나가 틀리면 뒤로 번지고 신조어나 구어체에 약해요."),
  bg("1강 NLP 역사 (규칙 → 통계 → 신경망)",
      "1강에서 규칙 기반 방법은 손으로 규칙을 계속 붙여야 해서 한계가 있었다고 했어요.",
      "형태소 분석기도 같은 약점을 가져요. 새 말이 나오면 사전에 넣기 전까지 못 알아봐요."),
 ],
 "pass4": [
  check("'는/JX' 에서 JX 는 무엇일까요?",
      ["일반 명사", "보조사", "형용사", "종결 어미"], 1,
      "NNG 일반 명사, JX 보조사, VA 형용사, EF 종결 어미예요."),
  english("답안 문장: 형태소 분석기의 장단점",
      f"{K('analyzer')}는 조사, 어미를 정확히 나누지만, 규칙 기반이라 오류 전파와 신조어에 약하다.",
      "도구: MeCab-ko, Kiwi, Okt, Komoran. 장점은 깔끔함, 검색 분류에 강함. 단점은 오류 전파, 신조어, 사전 관리예요."),
 ]})

# p.19 Subwords on Korean
S.append({"p": 19, "title": "Route 2: 한국어에 서브워드 (Subwords on Korean)",
 "pass1": [
  say("두 번째 길은 언어학을 잊고, 한국어 말뭉치에 BPE 를 그대로 돌리는 거예요.",
      "놀랍게도 꽤 잘 돼요.",
      "자주 쓰는 '안녕하세요' 는 통째로 한 토큰, 활용형은 줄기와 어미 근처에서 저절로 잘려요.",
      "단, 데이터가 한국어일 때만이에요."),
  analogy("레고 접착을 한국어 상자로",
      "한국어 레고 상자에서 자주 붙어 다니는 조각을 접착하면, 한국어에 맞는 큰 조각이 저절로 생겨요. 영어 상자로 접착하면 한국어 조각은 부스러기로 남아요.",
      ["한국어 레고 상자", "한국어 말뭉치"],
      ["저절로 생긴 큰 조각 '안녕하세요'", "자주 나와서 통째로 된 토큰"],
      ["영어 상자에 섞인 한국어 부스러기", "바이트 부스러기로 잘린 한국어"]),
 ],
 "pass2": [
  compare("슬라이드 영어 → 우리말", ["영어 원문", "우리말 뜻"],
      ["It works, surprisingly well", "놀랄 만큼 잘 돼요"],
      ["inflections split near stem/ending boundaries on their own", "활용형이 줄기/어미 경계 근처에서 저절로 잘려요"],
      ["Choice of starting unit: syllables, jamo, bytes", "시작 단위 고르기: 음절, 자모, 바이트"],
      ["shreds Korean into byte crumbs", "한국어를 바이트 부스러기로 찢어요"],
      ["only if the data is Korean", "데이터가 한국어일 때만이에요"]),
  compare("시작 단위 세 가지", ["시작 단위", "예", "특징"],
      ["음절", "가, 각, 간", "실전 표준"],
      ["자모", "ㄱ, ㅏ", "한 글자가 2~3토큰으로 부서질 수 있음"],
      ["바이트", "한 글자 = 3바이트", "한 글자가 2~3토큰으로 부서질 수 있음"]),
  check("한국어에 BPE 를 돌릴 때 실전 표준인 시작 단위는?",
      ["음절", "자모", "바이트"], 0,
      "음절에서 시작하는 게 실전 표준이에요. 자모나 바이트는 한 글자를 2~3조각으로 부술 수 있어요."),
 ],
 "pass3": [
  look("Subwords on Korean 쪽에서 볼 곳",
      (85, 153, 848, 188, f"한국어 {K('corpus')}에 그냥 BPE 를 돌리면? 놀랄 만큼 잘 돼요."),
      (85, 200, 1105, 235, "자주 쓰는 단어(안녕하세요)는 통째로, 활용형은 줄기/어미 경계 근처에서 저절로 잘려요."),
      (85, 248, 980, 313, "시작 단위: 음절(가, 각, 간), 자모(ㄱ, ㅏ), 바이트. 음절 시작이 실전 표준이고, 자모/바이트는 한 글자를 2~3토큰으로 부술 수 있어요."),
      (85, 327, 1135, 362, "주의: 영어가 많은 데이터로 학습한 토크나이저는 한국어를 바이트 부스러기로 찢어요(다음 쪽)."),
      (270, 680, 1135, 706, "BPE 는 언어학을 몰라도, 데이터가 한국어면 한국어를 배워요. 데이터가 한국어일 때만요.")),
  steps("손계산: 한 글자가 몇 바이트일까",
      [f"{K('utf8')}에서 영어 글자 하나는 1바이트예요(C → 43)",
       "한글 한 글자는 3바이트예요('자' → EC 9E 90)",
       "그래서 바이트에서 시작하면 한글 한 글자가 최대 3조각이 될 수 있어요",
       "학습이 덜 된 글자는 그 바이트들이 붙지 못한 채 2~3토큰으로 남아요"],
      "음절에서 시작하면 한 글자 = 적어도 한 조각이라 부서지지 않아요."),
  prof(W1,
      "형태소 분석기처럼 언어학 개념을 다 잊고, 한국어 코퍼스에 BPE 를 그대로 넣으면 꽤 잘 돼요.",
      "현재 거의 모든 LLM 은 형태소 분석을 거치지 않고, 어떤 언어든 BPE 로 처리한다고 보면 돼요.",
      "안녕하세요가 통째로 한 토큰이 될지, 쪼개질지는 BPE 를 학습한 코퍼스에 따라 달라져요.",
      "시작 단위(음절, 자모, 바이트)는 엔지니어링 선택이에요. 영어 위주 코퍼스에 한국어가 조금 끼어 있으면 결과가 안 좋아요."),
 ],
 "pass4": [
  check("영어 중심 데이터로 학습한 토크나이저가 한국어를 다루면 어떻게 될까요?",
      ["한국어가 더 짧게 잘린다", "한국어가 바이트 부스러기로 잘게 찢어진다", "[UNK] 만 나온다"], 1,
      f"한국어 조각을 거의 배우지 못해서 바이트 조각으로 잘게 쪼개요. 그래서 {K('fert','가')} 커져요(다음 쪽)."),
  english("답안 문장: 한국어에 BPE",
      f"{K('bpe')}는 한국어 {K('corpus')}로 학습하면 한국어를 잘 자르지만, 영어 중심 데이터면 바이트 조각으로 쪼갠다.",
      "시작 단위는 음절이 실전 표준이에요(자모, 바이트는 한 글자를 2~3토큰으로 부술 수 있어요)."),
 ]})

# p.20 Fertility
S.append({"p": 20, "title": "토큰 과다 분할 문제 (The Fertility Problem)",
 "pass1": [
  say(f"같은 뜻의 문장인데 한국어가 토큰을 2~3배 더 써요. 이것을 재는 값이 {K('fert','예요')}.",
      "영어 문장은 7토큰인데, 영어 중심 토크나이저로 한국어를 자르면 17토큰이에요.",
      "한국어 맞춤 토크나이저로 자르면 8토큰이면 돼요."),
  figure("같은 뜻, 다른 토큰 수", FIG_FERT,
      "영어 7, 한국어(영어 중심) 17, 한국어(한국어 맞춤) 8. 토큰은 돈이에요.", 2),
 ],
 "pass2": [
  compare("슬라이드 영어 → 우리말", ["영어 원문", "우리말 뜻"],
      ["Fertility = average tokens per word", "단어 하나가 평균 몇 토큰이 되는지"],
      ["how \"expensively\" a tokenizer treats a language", "토크나이저가 그 언어를 얼마나 '비싸게' 다루는지"],
      ["Korean pays 2-3× more tokens", "한국어가 토큰을 2~3배 더 내요"],
      ["Korean users pay double", "한국어 사용자는 두 배를 내요"],
      ["this is why Korean tokenizers exist", "그래서 한국어 토크나이저가 있어요"]),
  points("용어 뜻 풀기",
      f"{K('fert')}: 토큰 수 ÷ 단어 수예요. 작을수록 효율적이에요.",
      "English-centric tokenizer: 영어가 대부분인 데이터로 학습한 토크나이저예요.",
      "Korean-optimized tokenizer: 한국어 데이터로 학습한 토크나이저예요.",
      f"same context window: 같은 {K('ctx')}에 한국어는 절반만 담겨요."),
  check("fertility 가 클수록 무슨 뜻일까요?",
      ["그 언어를 싸고 효율적으로 다룬다", "그 언어를 비싸게(토큰을 많이 써서) 다룬다", "어휘가 작다"], 1,
      "단어당 토큰이 많을수록 같은 문장에 돈과 컨텍스트를 더 써요. 높으면 안 좋은 거예요."),
 ],
 "pass3": [
  look("Fertility 쪽에서 볼 곳",
      (85, 153, 935, 188, f"{K('fert')} = 단어당 평균 토큰 수. 토크나이저가 그 언어를 얼마나 비싸게 다루는지예요."),
      (85, 196, 745, 231, "같은 뜻, 같은 문장인데 한국어가 2~3배 토큰을 더 써요."),
      (210, 322, 810, 372, "English \"The weather is really nice today.\" → 7 토큰"),
      (210, 398, 1205, 448, "한국어를 영어 중심 토크나이저로: \"오늘은 날씨가 정말 좋네요.\" → 17 토큰"),
      (210, 473, 850, 523, "한국어를 한국어 맞춤 토크나이저로 → 8 토큰"),
      (262, 680, 1145, 706, "같은 API, 같은 컨텍스트 창인데 한국어 사용자는 두 배를 내요. 그래서 한국어 토크나이저가 있어요.")),
  formula("fertility 식", r"\mathrm{fertility} = \frac{\text{토큰 수}}{\text{단어 수}}",
      [(r"\text{토큰 수}", "토크나이저가 자른 조각 개수"),
       (r"\text{단어 수}", "띄어쓰기로 나눈 단어(한국어는 어절) 개수"),
       (r"\mathrm{fertility}", "단어 하나당 평균 토큰 수. 1에 가까울수록 효율적")],
      "실습 코드도 len(tokenize(s)) / len(s.split()) 로 똑같이 계산해요."),
  steps("손계산: 슬라이드 숫자로 fertility 구하기",
      ["영어 문장 단어 수: The / weather / is / really / nice / today. → 6개",
       "영어: 7 ÷ 6 = 약 1.17",
       "한국어 어절 수: 오늘은 / 날씨가 / 정말 / 좋네요. → 4개",
       "영어 중심 토크나이저: 17 ÷ 4 = 4.25",
       "한국어 맞춤 토크나이저: 8 ÷ 4 = 2.0",
       "한국어 두 토크나이저 비교: 17 ÷ 8 = 약 2.1배"],
      "같은 한국어 문장이 영어 중심 토크나이저에서 2배 넘게 비싸요. 영어 문장(7)과 비교하면 17 ÷ 7 = 약 2.4배예요."),
  steps("작은 예로 한 번 더",
      ["문장: 나는 학생이다 → 띄어쓰기 단어 2개",
       "어떤 토크나이저가 [나, 는, 학생, 이다] 로 자르면 토큰 4개",
       "fertility = 4 ÷ 2 = 2.0",
       "같은 문장을 [나는, 학생이다] 로 자르면 2 ÷ 2 = 1.0"],
      "조각이 잘수록 fertility 가 커져요.",
      given="설명을 위해 만든 자르기 예예요"),
  prof(W1,
      "fertility 는 어절 하나가 평균 몇 토큰이 되는지, 한마디로 토크나이저가 이 문장을 얼마나 비싸게 다루는지예요.",
      "영어 위주로 BPE 를 돌린 토크나이저는 영어 문장을 7토큰으로 자르는데, 같은 뜻의 한국어는 17토큰이에요. 말뭉치에 한국어가 적어서예요.",
      "BPE 는 만능이 아니에요. BPE 를 학습하는 데이터가 어떻게 구성됐는지가 매우 중요해요.",
      "하이퍼클로바, EXAONE 처럼 한국 기업이 자체 토크나이저를 만드는 이유에도 이 fertility 가 있어요."),
  prof(W3,
      "실습에서 GPT-2 로 '오늘은 날씨가 정말 좋네요' 를 자르면 무려 33토큰이 나왔어요.",
      "한국어로 학습한 KoGPT-2 는 같은 문장을 훨씬 적게 잘라요. 한국어 fertility 가 높으면 안 좋은 거예요.",
      "같은 BPE 알고리즘이라도 어떤 코퍼스로 학습했느냐에 따라 fertility 가 달라져요."),
  say("실습 N2L p.14 에서 GPT-2 와 KoGPT-2 로 같은 두 문장을 잘라 토큰 수를 비교해요.",
      "N2L p.15 에서 fertility 함수를 짜서 이 쪽의 손계산을 코드로 해요."),
 ],
 "pass4": [
  exam("예상 문제 (fertility 계산)",
      "\"오늘은 날씨가 정말 좋네요.\" is split into 17 tokens by an English-centric tokenizer and 8 by a Korean tokenizer. Compute the fertility of each.",
      "같은 한국어 문장이 영어 중심 토크나이저로 17토큰, 한국어 토크나이저로 8토큰일 때 각각의 fertility 를 구하세요.",
      ["fertility = 토큰 수 ÷ 단어(어절) 수",
       "어절 수: 오늘은, 날씨가, 정말, 좋네요 → 4",
       "영어 중심: 17 ÷ 4 = 4.25",
       "한국어: 8 ÷ 4 = 2.0",
       "한국어 토크나이저가 약 2.1배 효율적"],
      "4.25 와 2.0"),
  check("영어 문장 \"The weather is really nice today.\" 가 7토큰일 때 fertility 는 약 얼마?",
      ["0.86", "1.17", "7", "4.25"], 1,
      "단어가 6개이니 7 ÷ 6 = 약 1.17이에요."),
  english("답안 문장: fertility",
      f"{K('fert','는')} 단어당 평균 토큰 수로, 토크나이저가 한 언어를 얼마나 비싸게 다루는지 나타낸다.",
      "영어 중심 토크나이저에서 한국어는 2~3배 토큰을 써서 비용과 컨텍스트 창을 더 써요. 그래서 한국어 토크나이저가 필요해요."),
  warn("헷갈리기 쉬운 점",
      "fertility 는 클수록 나빠요. '비옥하다' 는 영어 뜻 때문에 좋은 것으로 착각하기 쉬워요.",
      "슬라이드 그래프는 17토큰, 교수님이 실습에서 GPT-2 로 직접 돌린 결과는 33토큰이었어요. 토크나이저가 달라서 숫자가 달라요. 시험에는 주어진 숫자로 계산해요."),
 ]})

# p.21 What Korean Models Actually Do
S.append({"p": 21, "title": "한국어 모델은 실제로 어떻게 하나 (What Korean Models Actually Do)",
 "pass1": [
  say("그럼 실제 한국어 모델은 어떻게 자를까요? 요리법이 세 가지예요.",
      "1. 한국어가 많은 말뭉치로 자기만의 BPE 를 학습해요(가장 흔해요).",
      "2. 형태소 분석기로 먼저 자르고, 그 위에 BPE 를 돌려요(둘을 섞은 방법).",
      "3. 여러 언어 모델은 어휘를 아주 크게 늘려 언어마다 몫을 나눠 줘요."),
  compare("세 가지 요리법", ["요리법", "하는 일", "한 줄 특징"],
      ["1", "한국어 비중 큰 말뭉치로 BPE/Unigram 학습", "가장 흔한 답"],
      ["2", "형태소 분석기로 먼저 자르고 BPE", "두 길을 섞은 방법"],
      ["3", "어휘를 128k~256k 로 키움", "언어마다 몫을 나눔"]),
 ],
 "pass2": [
  compare("슬라이드 영어 → 우리말", ["영어 원문", "우리말 뜻"],
      ["train your own BPE/Unigram on a Korean-heavy corpus", "한국어가 많은 말뭉치로 자기 BPE/Unigram 을 학습"],
      ["morpheme-aware subwords", "형태소를 아는 서브워드"],
      ["cutting particle/ending boundaries first helps BPE learn cleaner pieces", "조사/어미 경계를 먼저 자르면 BPE 가 더 깔끔한 조각을 배워요"],
      ["grow the vocab (128k-256k) so each language gets its share", "어휘를 키워 언어마다 자기 몫을 가져요"],
      ["an engineering choice you will make", "여러분이 내릴 공학적 선택이에요"]),
  steps("요리법 2 (섞은 방법)의 순서",
      [f"{K('analyzer')}로 어절을 형태소로 먼저 자르기",
       "조사, 어미 경계가 미리 나뉜 상태가 됨",
       f"그 위에서 {K('bpe')}로 자주 붙는 조각 합치기",
       "결과: 경계가 깔끔한 서브워드 조각"],
      "언어학(형태소)과 통계(BPE)를 함께 쓰는 방법이에요."),
  check("형태소 분석기로 먼저 나눈 뒤 BPE 를 돌리는 방법은 몇 번 요리법일까요?",
      ["1번", "2번", "3번"], 1,
      "Recipe 2, morpheme-aware subwords 예요. 18쪽 길과 19쪽 길을 섞은 거예요."),
 ],
 "pass3": [
  look("What Korean Models Actually Do 쪽에서 볼 곳",
      (85, 153, 1068, 188, "Recipe 1: 한국어 비중이 큰 말뭉치로 자기 BPE/Unigram 을 학습해요. 가장 흔한 답이에요."),
      (85, 200, 1175, 266, "Recipe 2: 형태소를 아는 서브워드. 분석기로 먼저 자르고 BPE. 조사/어미 경계를 먼저 자르면 더 깔끔한 조각을 배워요."),
      (85, 280, 1015, 315, "Recipe 3: 다국어 모델은 어휘를 128k~256k 로 키워 언어마다 몫을 줘요."),
      (85, 327, 1045, 362, f"Today's lab: HF tokenizers 로 한국어 BPE {K('tokr','를')} 직접 학습하고 fertility 를 재요."),
      (300, 680, 1105, 706, "한국어 토큰화는 다 풀린 문제가 아니라, 여러분이 내릴 공학적 선택이에요.")),
  prof(W1,
      "EXAONE, HyperCLOVA X, Solar 같은 한국어 모델에는 레시피가 세 가지 정도 있어요.",
      "두 번째 하이브리드는 형태소 분석기로 먼저 잘라 놓고 BPE 를 돌리는 거예요. 언어학과 통계의 협업 같은 느낌이에요.",
      "세 번째는 어휘를 크게 잡고 영어 몇 %, 한국어 몇 % 처럼 언어마다 지분을 나눠 BPE 를 돌려요. 양으로 승부 보는 거예요.",
      "한국어 토큰화는 문제라기보다 엔지니어링 선택이에요. 한국어에 치중하면 영어 효율이 떨어질 수 있어요."),
  prof(W3,
      "실습에서 NSMC 영화 리뷰 글로 어휘 크기 8천짜리 BPE 토크나이저를 학습했어요.",
      "그걸로 '오늘은 날씨가 정말 좋네요' 를 자르니 7토큰이 됐어요. GPT-2 는 33토큰이었어요.",
      "큰 회사들은 영화 리뷰가 아니라 훨씬 큰 말뭉치로 학습해서 훨씬 좋은 토크나이저를 만들어요."),
  steps("실습 결과로 fertility 비교 (교수님이 말한 토큰 수)",
      ["문장 어절 수: 4",
       "GPT-2: 33 ÷ 4 = 8.25",
       "우리가 NSMC 로 학습한 한국어 BPE: 7 ÷ 4 = 1.75",
       "33 ÷ 7 = 약 4.7배 차이"],
      "한국어 데이터로 조금만 학습해도 fertility 가 크게 줄어요."),
  say("실습 N2L p.16 에서 NSMC 데이터를 불러오고, N2L p.17 에서 어휘 8000 짜리 BPE 를 학습해요.",
      "N2L p.18 에서 우리 토크나이저와 GPT-2 를 같은 문장으로 비교해요. 요리법 1을 직접 해 보는 거예요."),
 ],
 "pass4": [
  check("다국어 모델이 어휘를 128k~256k 로 키우는 까닭은?",
      ["영어만 더 잘하려고", "언어마다 자기 몫의 토큰을 주려고", "형태소 분석기를 없애려고"], 1,
      "Recipe 3. 어휘를 키워 각 언어가 자기 몫(share)을 갖게 해요."),
  english("답안 문장: 한국어 모델의 토큰화 요리법",
      "한국어 모델은 ① 한국어 말뭉치로 직접 학습, ② 형태소 분석 뒤 BPE, ③ 어휘 키우기 중에서 고른다.",
      "①이 가장 흔해요. ②는 두 길을 섞은 방법, ③은 128k~256k 로 언어마다 몫을 줘요. 정답이 아니라 공학적 선택이에요."),
  warn("헷갈리기 쉬운 점",
      "요리법 2는 형태소 분석기만 쓰는 게 아니라 '분석기로 먼저 자르고 그다음 BPE' 예요.",
      "한국어에만 맞추면 영어 효율이 떨어질 수 있어요. 그래서 '공학적 선택' 이라고 해요."),
 ]})


# =====================================================================
# 저장
# =====================================================================
BAD = [chr(0x2014), chr(0x2013), chr(0xB7), chr(0x30FB)]


def _text(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, list):
        for x in o:
            yield from _text(x)
    elif isinstance(o, dict):
        for k, v in o.items():
            if k != "svg":
                yield from _text(v)


def main():
    gl_keys = []
    for s in S:
        body = " ".join(_text([s.get(f"pass{i}", []) for i in range(1, 5)]))
        terms = []
        for key in TERMS:
            if disp(key) in body:
                ko, en, _, _ = TERMS[key]
                terms.append(en or ko)
                if key not in gl_keys:
                    gl_keys.append(key)
        s["terms"] = terms
    glossary = []
    for k in gl_keys:
        ko, en, _, _ = TERMS[k]
        say_, more = GLOSS[k]
        glossary.append({"ko": ko, "en": en, "say": say_, "more": more})
    out = {"deck": "N2", "from": 1, "to": 21, "glossary": glossary,
           "slides": [{"p": s["p"], "title": s["title"], "terms": s["terms"],
                       **{f"pass{i}": s.get(f"pass{i}", []) for i in range(1, 5)}} for s in S]}
    raw = json.dumps(out, ensure_ascii=False, indent=1)
    for ch in BAD:
        if ch in raw:
            i = raw.index(ch)
            raise ValueError(f"금지 문자 {ch!r}: {raw[max(0, i - 40):i + 10]}")
    for s in out["slides"]:
        for i in range(1, 5):
            for f in s[f"pass{i}"]:
                if f["kind"] in ("say", "prof", "bg"):
                    for ln in f["lines"]:
                        if len(ln.replace("**", "")) > 90:
                            print(f"  긴 줄 p.{s['p']} pass{i}: {ln[:40]}...")
    missing = [k for k in TERMS if k not in gl_keys]
    if missing:
        print("  본문에 안 나온 용어:", missing)
    with open(OUT, "w", encoding="utf-8") as fp:
        fp.write(raw)
    print(f"저장 {OUT}: 쪽 {len(S)}, 용어 {len(glossary)}")


if __name__ == "__main__":
    main()
