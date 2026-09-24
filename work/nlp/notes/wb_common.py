# -*- coding: utf-8 -*-
"""기초 다지기(week b) 단원 파일들이 함께 쓰는 도우미.
build_slides_wb.py 가 wb_units_1_4 / wb_units_5_7 / wb_units_8_10 을 불러 모아 slides_wb.json 을 만든다.

쓰는 법
  from wb_common import *
  add_terms({"이름": ("English", "아주 쉬운 한 문장")})   # 아래 TERMS 에 없는 용어만
  UNITS = [unit("wb-1", "제목", "이 단원을 마치면 ...", ["벡터", ...], ["앞 단원 용어", ...], [ ...슬라이드... ])]

글 안에서 용어는 [[벡터]] 로 적으면 **벡터(Vector)** 로 바뀐다. 조사가 필요하면 [[벡터|은/는]].
숫자는 반드시 이 파일들 안에서 Python 으로 계산하고 assert 로 확인한다.
"""
import json, math, os, re, sys
from xml.sax.saxutils import escape

sys.stdout.reconfigure(encoding="utf-8")

MANTRA = "글을 토큰으로 자르고, 토큰을 벡터로 바꾸고, 벡터로 다음 토큰을 맞혀요."

# ---------------------------------------------------------------- 용어 사전
# 과목정보.md 7절 표에 있는 용어는 en 표기를 그대로 쓴다 (사이트가 한 용어로 합친다).
TERMS = {
    # --- 기초 다지기에서 새로 만드는 용어
    "벡터": ("Vector", "숫자를 순서대로 늘어놓은 목록. 화살표 하나로 그릴 수 있어요"),
    "차원": ("Dimension", "벡터에 들어 있는 숫자 칸의 개수"),
    "스칼라": ("Scalar", "칸이 없는 숫자 하나"),
    "성분": ("Component", "벡터의 한 칸에 들어 있는 숫자"),
    "노름": ("Norm", "벡터 화살표의 길이"),
    "단위 벡터": ("Unit Vector", "길이가 정확히 1 인 벡터"),
    "행렬": ("Matrix", "숫자를 가로 세로 표로 늘어놓은 것"),
    "모양": ("Shape", "행이 몇 줄이고 열이 몇 칸인지"),
    "행렬 곱": ("Matrix Multiplication", "표와 표를 곱해서 새 표를 만드는 계산"),
    "전치": ("Transpose", "표를 눕혀서 행과 열을 바꾸는 것"),
    "지수 함수": ("Exponential Function", "exp 를 씌워 항상 양수로 만드는 함수"),
    "로그": ("Logarithm", "몇 번 곱했는지를 되묻는 함수"),
    "자연로그": ("Natural Logarithm", "밑이 e 인 로그. 코드에서 log 라고 하면 보통 이것"),
    "음의 로그": ("Negative Log", "로그에 마이너스를 붙인 것. 확률이 작을수록 커져요"),
    "확률": ("Probability", "일이 얼마나 자주 일어나는지를 0 과 1 사이 숫자로"),
    "조건부 확률": ("Conditional Probability", "무엇이 이미 주어졌을 때의 확률"),
    "확률 분포": ("Probability Distribution", "후보마다 확률을 붙여 둔 목록. 다 더하면 1"),
    "곱의 규칙": ("Product Rule", "여러 일이 잇따라 일어날 확률은 곱해서 구해요"),
    "함수": ("Function", "넣으면 하나가 나오는 상자"),
    "미분": ("Derivative", "살짝 움직였을 때 결과가 얼마나 바뀌는지"),
    "접선": ("Tangent Line", "곡선의 한 점에 살짝 붙인 직선"),
    "편미분": ("Partial Derivative", "다른 것은 고정하고 하나만 움직여 본 미분"),
    "미니배치": ("Minibatch", "전체가 아니라 몇 개만 묶어서 한 번에 보는 것"),
    "에폭": ("Epoch", "학습 데이터를 처음부터 끝까지 한 번 다 본 것"),
    "가중합": ("Weighted Sum", "값마다 가중치를 곱해서 모두 더한 것"),
    "편향 항": ("Bias Term", "가중합에 마지막으로 더해 주는 한 숫자"),
    "층": ("Layer", "뉴런을 한 줄로 모아 놓은 묶음"),
    "리스트": ("List", "파이썬에서 순서대로 담는 상자. 대괄호로 써요"),
    "튜플": ("Tuple", "한 번 만들면 못 바꾸는 목록. 소괄호로 써요"),
    "딕셔너리": ("Dictionary", "이름표(키)로 값을 꺼내는 파이썬 상자"),
    "반복문": ("For Loop", "같은 일을 목록의 원소마다 되풀이하기"),
    "함수 정의": ("Function Definition", "def 로 내가 쓸 계산에 이름을 붙이는 것"),
    "자동 미분": ("Automatic Differentiation (Autodiff)", "미분을 사람 대신 컴퓨터가 해 주는 기능"),

    # --- 과목정보 7절 표 (표기 그대로)
    "자연어처리": ("Natural Language Processing (NLP)", "컴퓨터가 사람 말을 다루게 하는 분야"),
    "토큰": ("Token", "글을 자른 레고 조각 하나"),
    "토큰화": ("Tokenization", "글을 토큰으로 자르는 일"),
    "토크나이저": ("Tokenizer", "글을 토큰으로 잘라 주는 도구"),
    "어휘": ("Vocabulary", "모델이 아는 토큰 종류 목록"),
    "말뭉치": ("Corpus", "학습에 쓰는 글을 잔뜩 모아 둔 것"),
    "원-핫 벡터": ("One-hot Vector", "자기 자리만 1 이고 나머지는 모두 0 인 벡터"),
    "단어 벡터": ("Word Vector", "단어의 지도 좌표. 뜻이 비슷하면 가까이 살아요"),
    "임베딩": ("Embedding", "토큰을 숫자 벡터로 바꾼 것"),
    "워드투벡": ("word2vec", "주변 문맥으로 단어의 뜻을 주는 방법"),
    "스킵그램": ("Skip-gram", "중심 단어로 주변 단어를 맞히는 방식"),
    "중심 단어": ("Center Word", "지금 기준이 되는 가운데 단어"),
    "문맥 단어": ("Context Word", "중심 단어 주변에 있는 단어"),
    "윈도우": ("Window", "중심 단어 양옆으로 몇 칸까지 볼지"),
    "코사인 유사도": ("Cosine Similarity", "두 화살표가 얼마나 같은 쪽을 보는지 0 과 1 사이로"),
    "내적": ("Dot Product", "같은 자리끼리 곱해서 모두 더하기"),
    "소프트맥스": ("Softmax", "점수를 모두 더해 1 이 되는 확률 파이로 나누기"),
    "교차 엔트로피": ("Cross-Entropy", "정답에 준 확률의 음의 로그를 벌점으로 쓰는 손실"),
    "손실 함수": ("Loss Function", "틀린 정도를 매기는 벌점"),
    "목적 함수": ("Objective Function", "학습이 줄이거나 키우려는 값"),
    "우도": ("Likelihood", "지금 모델이 이 데이터를 낼 확률"),
    "파라미터": ("Parameter", "학습하면서 바뀌는 숫자. 모델이 기억을 저장하는 자리"),
    "경사 하강법": ("Gradient Descent", "안개 낀 산에서 발밑 기울기만 보고 한 걸음씩 내려가기"),
    "확률적 경사 하강법": ("Stochastic Gradient Descent (SGD)", "전체가 아니라 조금만 보고 한 걸음 내려가기"),
    "학습률": ("Learning Rate", "한 걸음의 보폭"),
    "기울기": ("Gradient", "손실이 가장 빨리 커지는 방향과 그 가파름"),
    "연쇄 법칙": ("Chain Rule", "맞물린 톱니바퀴처럼 미분을 곱해 이어 붙이는 규칙"),
    "역전파": ("Backpropagation", "틀린 책임을 뒤에서 앞으로 나눠 주기"),
    "야코비안": ("Jacobian", "벡터를 벡터로 보내는 함수의 미분을 표로 모은 것"),
    "계산 그래프": ("Computation Graph", "계산을 동그라미와 화살표로 그린 그림"),
    "순전파": ("Forward Pass", "입력에서 출력까지 앞으로 한 번 계산하기"),
    "뉴런": ("Neuron", "여러 숫자를 가중합하고 구부려 하나로 내보내는 작은 계산 단위"),
    "활성화 함수": ("Activation Function", "가중합을 한 번 구부려 주는 함수"),
    "비선형성": ("Nonlinearity", "곧은 직선이 아닌 구부러진 변환"),
    "렐루": ("ReLU", "음수는 0 으로 만들고 양수는 그대로 두는 함수"),
    "시그모이드": ("Sigmoid", "어떤 수든 0 과 1 사이로 눌러 주는 S자 함수"),
    "다층 퍼셉트론": ("Multi-Layer Perceptron (MLP)", "뉴런 층을 여러 겹 쌓은 가장 기본 신경망"),
    "언어 모델": ("Language Model (LM)", "다음 토큰을 맞히는 모델"),
    "다음 토큰 예측": ("Next Token Prediction", "지금까지의 토큰으로 바로 다음 토큰을 맞히기"),
    "엔그램": ("n-gram", "바로 앞 몇 단어만 보고 다음 단어 맞히기"),
    "퍼플렉서티": ("Perplexity (PPL)", "다음 단어를 고를 때 헷갈리는 후보가 평균 몇 개인지"),
    "순환 신경망": ("Recurrent Neural Network (RNN)", "한 단어씩 읽으며 메모장에 요약을 고쳐 쓰는 신경망"),
    "은닉 상태": ("Hidden State", "지금까지 읽은 내용을 요약해 들고 다니는 숫자 벡터"),
    "어텐션": ("Attention", "필요한 곳을 골라 보는 장치"),
    "어텐션 점수": ("Attention Score", "두 벡터가 얼마나 관련 있는지 나타낸 날것 숫자"),
    "어텐션 가중치": ("Attention Weight", "점수를 소프트맥스에 넣어 얻은, 합이 1 인 값들"),
    "문맥 벡터": ("Context Vector", "필요한 만큼만 뽑아 만든 요약 벡터"),
    "쿼리": ("Query", "지금 내가 무엇을 찾고 있는지를 담은 벡터"),
    "키": ("Key", "나는 이런 정보를 갖고 있다고 광고하는 검색용 이름표 벡터"),
    "밸류": ("Value", "내가 선택되면 실제로 건네줄 내용 벡터"),
    "셀프 어텐션": ("Self-Attention", "한 문장이 자기 자신을 바라보는 어텐션"),
    "스케일드 닷프로덕트 어텐션": ("Scaled Dot-Product Attention", "내적 점수를 루트 d_k 로 나눈 뒤 소프트맥스를 쓰는 어텐션"),
    "멀티 헤드 어텐션": ("Multi-Head Attention (MHA)", "전체 차원을 h 조각으로 나눠 여러 관점에서 동시에 어텐션하기"),
    "위치별 피드포워드 신경망": ("Position-wise Feed-Forward Network (FFN)", "자리마다 똑같이 적용하는 2층짜리 작은 신경망"),
    "트랜스포머": ("Transformer", "어텐션만으로 만든 요즘 언어 모델의 기본 블록"),
    "대규모 언어 모델": ("Large Language Model (LLM)", "트랜스포머를 아주 크게 쌓은 언어 모델"),
    "텐서": ("Tensor", "PyTorch 가 쓰는 숫자 덩어리. 벡터와 행렬을 아우르는 말"),
    "기울기 소실": ("Vanishing Gradient", "귓속말 전달 게임에서 말이 점점 희미해지기"),
    "바이트 쌍 인코딩": ("Byte Pair Encoding (BPE)", "자주 붙어 다니는 두 조각을 한 조각으로 접착하기"),
    "분포 가설": ("Distributional Hypothesis", "친구를 보면 그 사람을 안다"),
}


def add_terms(extra):
    """단원 파일이 자기에게 필요한 용어를 더할 때 쓴다. 이미 있으면 표기가 같은지 확인한다."""
    for ko, v in extra.items():
        if ko in TERMS:
            assert TERMS[ko][0] == v[0], "용어 표기 충돌: %s (%s vs %s)" % (ko, TERMS[ko][0], v[0])
        else:
            TERMS[ko] = v


# ---------------------------------------------------------------- 용어 쓰기
def josa(word, pair):
    """받침에 맞는 조사: 은/는, 이/가, 을/를, 과/와, 으로/로, 이에요/예요, 이라고/라고."""
    x, y = pair.split("/")
    if x in ("은", "을", "과") or x[0] in "이으":
        a, b = x, y
    else:
        a, b = y, x
    ch = word.strip()[-1]
    ro = a == "으로"
    if "가" <= ch <= "힣":
        jong = (ord(ch) - 0xAC00) % 28
        has = jong != 0 and not (ro and jong == 8)
    else:
        has = False
    return a if has else b


def show(ko, p=""):
    if ko not in TERMS:
        raise KeyError("사전에 없는 용어: " + ko + " (add_terms 로 먼저 넣어요)")
    return "**%s(%s)**" % (ko, TERMS[ko][0]) + (josa(ko, p) if p else "")


def fill(o):
    if isinstance(o, str):
        return re.sub(r"\[\[(.+?)(?:\|(.+?))?\]\]", lambda m: show(m.group(1), m.group(2) or ""), o)
    if isinstance(o, list):
        return [fill(x) for x in o]
    if isinstance(o, dict):
        return {k: (v if k == "svg" else fill(v)) for k, v in o.items()}
    return o


# ---------------------------------------------------------------- 슬라이드 도우미
def title(big, sub):
    assert len(big) <= 20, big
    return {"kind": "title", "big": big, "sub": sub}


def goal(*items):
    assert 2 <= len(items) <= 4
    return {"kind": "goal", "items": list(items)}


def pts(head, *items):
    assert 2 <= len(items) <= 5, head
    return {"kind": "points", "head": head, "items": list(items)}


def ana(head, scene, *pairs):
    assert 2 <= len(pairs) <= 4, head
    return {"kind": "analogy", "head": head, "scene": scene, "map": [list(p) for p in pairs]}


def fml(head, tex, parts, whole):
    assert 2 <= len(parts) <= 6, head
    return {"kind": "formula", "head": head, "tex": tex,
            "parts": [{"sym": s, "say": w} for s, w in parts], "whole": whole}


def stp(head, given, steps, answer):
    assert 3 <= len(steps) <= 7, head
    d = {"kind": "steps", "head": head, "steps": list(steps), "answer": answer}
    if given:
        d["given"] = given
    return d


def cmp_(head, cols, rows):
    assert 2 <= len(cols) <= 4 and 2 <= len(rows) <= 6, head
    for r in rows:
        assert len(r) == len(cols), (head, r)
    return {"kind": "compare", "head": head, "cols": list(cols), "rows": [list(r) for r in rows]}


def chk(q, choices, a, why):
    assert 2 <= len(choices) <= 4 and 0 <= a < len(choices), q
    return {"kind": "check", "q": q, "choices": list(choices), "a": a, "why": why}


def warn(head, *items):
    assert 1 <= len(items) <= 3, head
    return {"kind": "warn", "head": head, "items": list(items)}


def where(*items):
    """단원 recap 바로 앞에 넣는 '이게 이 과목 어디에 나오나' 슬라이드."""
    return pts("이게 이 과목 어디에 나오나", *items)


def recap(*items):
    assert 3 <= len(items) <= 5
    return {"kind": "recap", "items": list(items)}


# ---------------------------------------------------------------- SVG 도우미 (클래스만 사용)
W = 480
TEXTS = []   # 지금 그리는 그림의 글자 상자들 (겹침 검사용)


def tw(s, size):
    """글자 폭 대략 추정 (한글 1em, 영숫자 0.6em, 공백 0.3em)."""
    w = 0.0
    for ch in s:
        w += 0.3 if ch == " " else (1.0 if ord(ch) > 0x2E80 else 0.6)
    return w * size


def _c(c, b):
    return c + (" b%d" % b if b else "")


def R(x, y, w, h, c="box", b=0, rx=2):
    assert 0 <= rx <= 3
    return '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%g" class="%s"/>' % (x, y, w, h, rx, _c(c, b))


def C(cx, cy, r, c="n", b=0):
    return '<circle cx="%.1f" cy="%.1f" r="%g" class="%s"/>' % (cx, cy, r, _c(c, b))


def L(x1, y1, x2, y2, c="e", b=0):
    return '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="%s"/>' % (x1, y1, x2, y2, _c(c, b))


def T(x, y, s, c="t", b=0, fs=15, a="middle"):
    """글자. 화면 밖으로 나가거나 다른 글자와 겹치면 assert 로 멈춘다."""
    assert 14 <= fs <= 20
    w = tw(s, fs)
    left = x - w / 2 if a == "middle" else (x if a == "start" else x - w)
    assert left >= 1 and left + w <= W - 1, "화면 밖 글자 %r left=%.0f w=%.0f" % (s, left, w)
    assert y - fs * 0.8 >= 0 and y <= 300, "위아래 밖 글자 %r" % s
    box = (left, y - fs * 0.78, left + w, y + fs * 0.22, s)
    for o in TEXTS:
        if box[0] < o[2] - 1 and o[0] < box[2] - 1 and box[1] < o[3] - 1 and o[1] < box[3] - 1:
            raise AssertionError("글자 겹침 %r / %r" % (s, o[4]))
    TEXTS.append(box)
    return '<text x="%.1f" y="%.1f" font-size="%d" text-anchor="%s" class="%s">%s</text>' % (
        x, y, fs, a, _c(c, b), escape(s))


def A(x1, y1, x2, y2, c="e2", b=0, hd=9):
    dx, dy = x2 - x1, y2 - y1
    n = math.hypot(dx, dy)
    ux, uy = dx / n, dy / n
    bx, by = x2 - ux * hd, y2 - uy * hd
    px, py = -uy * 4.5, ux * 4.5
    head = '<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" class="%s"/>' % (
        x2, y2, bx + px, by + py, bx - px, by - py, _c("arrow", b))
    return L(x1, y1, bx, by, c, b) + head


def PL(p, c="e2", b=0):
    s = " ".join("%.1f,%.1f" % q for q in p)
    return '<polyline points="%s" fill="none" class="%s"/>' % (s, _c(c, b))


def PG(p, c="n3", b=0):
    s = " ".join("%.1f,%.1f" % q for q in p)
    return '<polygon points="%s" class="%s"/>' % (s, _c(c, b))


def BOX(x, y, w, h, s, c="box", tc="tb", b=0, fs=15):
    return R(x, y, w, h, c, b) + T(x + w / 2, y + h / 2 + fs * 0.35, s, tc, b, fs)


def fig(head, els, caption, h=270):
    svg = '<svg viewBox="0 0 480 %d" xmlns="http://www.w3.org/2000/svg">%s</svg>' % (h, "".join(els))
    TEXTS.clear()   # 다음 그림의 겹침 검사를 새로 시작
    bs = [int(m) for m in re.findall(r'class="[^"]*\bb(\d)\b', svg)]
    return {"kind": "figure", "head": head, "svg": svg, "caption": caption, "builds": max(bs) if bs else 1}


class Plot:
    """데이터 좌표 -> 화면 좌표. 칸(X, Y, Wd, Ht) 안에 x0..x1, y0..y1 을 그린다."""

    def __init__(s, x0, x1, y0, y1, X, Y, Wd, Ht):
        s.x0, s.x1, s.y0, s.y1, s.X, s.Y, s.Wd, s.Ht = x0, x1, y0, y1, X, Y, Wd, Ht

    def px(s, x):
        return s.X + (x - s.x0) / (s.x1 - s.x0) * s.Wd

    def py(s, y):
        return s.Y + s.Ht - (y - s.y0) / (s.y1 - s.y0) * s.Ht

    def axes(s, xl="x", yl="y", xt=(), yt=(), b=0, xtl=None, ytl=None):
        out = [A(s.X - 4, s.py(0), s.X + s.Wd + 12, s.py(0), "e", b, 7)]
        if s.x0 <= 0 <= s.x1:
            out.append(A(s.px(0), s.Y + s.Ht + 4, s.px(0), s.Y - 10, "e", b, 7))
            if yl:
                out.append(T(s.px(0) + 6, s.Y - 2, yl, "tm", b, 14, "start"))
        if xl:
            out.append(T(s.X + s.Wd + 14, s.py(0) - 6, xl, "tm", b, 14, "start"))
        for i, v in enumerate(xt):
            lab = xtl[i] if xtl else fmtn(v)
            out.append(L(s.px(v), s.py(0) - 3, s.px(v), s.py(0) + 3, "e", b))
            out.append(T(s.px(v), s.py(0) + 18, lab, "tm", b, 14))
        for i, v in enumerate(yt):
            lab = ytl[i] if ytl else fmtn(v)
            out.append(L(s.px(0) - 3, s.py(v), s.px(0) + 3, s.py(v), "e", b))
            out.append(T(s.px(0) - 7, s.py(v) + 5, lab, "tm", b, 14, "end"))
        return out

    def curve(s, f, a, bb, c="e2", b=0, n=160):
        return PL([(s.px(a + (bb - a) * i / n), s.py(f(a + (bb - a) * i / n))) for i in range(n + 1)], c, b)

    def line(s, p, c="e2", b=0):
        return PL([(s.px(x), s.py(y)) for x, y in p], c, b)

    def bars(s, xs, vals, c="n2", b=0, w=14):
        out = []
        for x_, v in zip(xs, vals):
            out.append(R(s.px(x_) - w / 2, s.py(max(v, 0)), w, abs(s.py(v) - s.py(0)), c, b))
        return out

    def dot(s, x, y, c="n2", b=0, r=5):
        return C(s.px(x), s.py(y), r, c, b)


def fmtn(v):
    if abs(v - round(v)) < 1e-9:
        return str(int(round(v)))
    return ("%.2f" % v).rstrip("0").rstrip(".")


# ---------------------------------------------------------------- 단원 만들기
def _strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, list):
        for x in o:
            yield from _strings(x)
    elif isinstance(o, dict):
        for k, v in o.items():
            if k != "svg":
                yield from _strings(v)


def unit(uid, ttl, gl, terms, recall, slides):
    """terms: 이 단원 용어(ko) 4~10개, 본문에 3번 이상 나와야 한다.
    recall: 앞 단원에서 다시 부르는 용어 2개 이상 (wb-1 은 없어도 된다)."""
    slides = fill(slides)
    body = " ".join(_strings(slides))
    tl = []
    for ko in terms:
        en, say = TERMS[ko]
        n = body.count("**%s(%s)**" % (ko, en))
        assert n >= 3, "%s: 용어 %s 가 %d번 (3번 이상)" % (uid, ko, n)
        tl.append({"ko": ko, "en": en, "say": say})
    for ko in recall:
        assert body.count("**%s(%s)**" % (ko, TERMS[ko][0])) >= 1, "%s: 앞 단원 용어 %s 가 본문에 없음" % (uid, ko)
    assert uid == "wb-1" or len(recall) >= 2, "%s: 앞 단원 용어 2개 이상" % uid
    assert 4 <= len(tl) <= 10, "%s: 용어 %d개" % (uid, len(tl))
    assert 14 <= len(slides) <= 22, "%s: 슬라이드 %d장 (14~22)" % (uid, len(slides))
    assert slides[0]["kind"] == "title" and slides[1]["kind"] == "goal", uid
    assert slides[-1]["kind"] == "recap", uid
    assert slides[-2]["kind"] == "points" and slides[-2]["head"] == "이게 이 과목 어디에 나오나", \
        "%s: recap 바로 앞은 where(...) 슬라이드" % uid
    kinds = [s["kind"] for s in slides]
    for need in ("analogy", "figure", "check"):
        assert need in kinds, "%s: %s 슬라이드 없음" % (uid, need)
    for s in slides:
        for t in _strings(s):
            assert "—" not in t and "–" not in t and "·" not in t and "・" not in t, \
                "%s: 금지 문자 %r" % (uid, t[:40])
            if s["kind"] != "formula":
                assert t.count("$") % 2 == 0, "%s: $ 짝 안 맞음 %r" % (uid, t[:40])
    return {"id": uid, "title": ttl, "goal": gl, "terms": tl, "slides": slides}
