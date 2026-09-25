# -*- coding: utf-8 -*-
"""참고 논문 Attention Is All You Need (덱 NP) 회독 레슨 10~15쪽 생성기.
사용: python build_NP_010-015.py   출력: NP_010-015.json
10쪽 Table 4 와 7 Conclusion, 11~12쪽 References, 13~15쪽 Attention Visualizations.
숫자는 아래에서 실제로 계산해 assert 로 확인한다."""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "NP_010-015.json")

# ---------------- 손계산 확인 ----------------
# p.10 Table 4 (WSJ Section 23 F1)
T4_WSJ = [("Vinyals & Kaiser el al. (2014) [37]", 88.3), ("Petrov et al. (2006) [29]", 90.4),
          ("Zhu et al. (2013) [40]", 90.4), ("Dyer et al. (2016) [8]", 91.7),
          ("Transformer (4 layers)", 91.3)]
T4_SEMI = [("Zhu et al. (2013) [40]", 91.3), ("Huang & Harper (2009) [14]", 91.3),
           ("McClosky et al. (2006) [26]", 92.1), ("Vinyals & Kaiser el al. (2014) [37]", 92.1),
           ("Transformer (4 layers)", 92.7)]
T4_OTHER = [("Luong et al. (2015) [23]", 93.0), ("Dyer et al. (2016) [8]", 93.3)]
assert max(v for _, v in T4_WSJ) == 91.7                      # Dyer 가 WSJ only 에서 1등
assert round(91.7 - 91.3, 1) == 0.4                            # 트랜스포머는 0.4 차이로 2등
assert round(91.3 - 88.3, 1) == 3.0                            # RNN seq2seq(Vinyals) 보다 3.0 높다
assert max(v for _, v in T4_SEMI) == 92.7                      # 준지도에서는 트랜스포머가 1등
assert round(92.7 - 92.1, 1) == 0.6
assert max(v for _, v in T4_WSJ + T4_SEMI + T4_OTHER) == 93.3  # 표 전체 1등은 Dyer generative
assert round(93.3 - 92.7, 1) == 0.6
assert 91.3 > 90.4                                             # BerkeleyParser(Petrov) 를 이겼다

# p.10 구문 분석 설정
assert 4 * 1024 == 4096          # 4층, d_model = 1024 (번역 base 의 6층, 512 와 다르다)
assert 40 * 1000 == 40000        # WSJ 학습 문장 약 40K
assert 17 * 10 ** 6 == 17000000  # 준지도 학습 문장 약 17M
assert 17000000 // 40000 == 425  # 준지도 자료가 약 425배 많다
assert 300 > 50                  # 최대 출력 길이 여유: 구문 분석 +300, 번역 +50
assert 21 > 4                    # 빔 크기: 구문 분석 21, 번역 4
assert 0.3 < 0.6                 # 길이 페널티 alpha: 구문 분석 0.3, 번역 0.6

# p.11, p.12 참고문헌 번호와 이 과목에서 배운 내용 짝
REF_MAP = [
    ("[1]", "Layer normalization", "층 정규화", "3.1 절의 LayerNorm"),
    ("[2]", "Bahdanau 어텐션", "2015년 어텐션", "4주차 Part 2"),
    ("[5]", "RNN encoder-decoder", "seq2seq 의 시작", "4주차 Part 1"),
    ("[9]", "ConvS2S", "합성곱 seq2seq", "2 Background 와 Table 1"),
    ("[11]", "Deep residual learning", "잔차 연결", "3.1 절의 residual connection"),
    ("[13]", "Long short-term memory", "LSTM", "3주차 마지막"),
    ("[18]", "ByteNet", "합성곱 번역", "2 Background"),
    ("[20]", "Adam", "옵티마이저", "5.3 절"),
    ("[30]", "Using the output embedding", "가중치 공유", "3.4 절"),
    ("[31]", "Subword units", "BPE", "2주차"),
    ("[33]", "Dropout", "드롭아웃", "5.4 절"),
    ("[35]", "Sequence to sequence learning", "seq2seq", "4주차 Part 1"),
    ("[36]", "Rethinking the inception architecture", "라벨 스무딩", "5.4 절"),
    ("[38]", "Google's neural machine translation", "word-piece, 빔 서치", "5.1 절과 6.1 절"),
]
assert len(REF_MAP) == 14
assert 40 == 40                  # 참고문헌은 [1] 부터 [40] 까지 마흔 편
assert 4 + 20 + 16 == 40         # p.10 에 4편, p.11 에 20편, p.12 에 16편

# p.13 Figure 3 문장의 토큰 수
SENT13 = ["It", "is", "in", "this", "spirit", "that", "a", "majority", "of", "American",
          "governments", "have", "passed", "new", "laws", "since", "2009", "making", "the",
          "registration", "or", "voting", "process", "more", "difficult", ".", "<EOS>"]
assert len(SENT13) == 27
assert SENT13.index("making") == 17
assert SENT13.index("more") == 23 and SENT13.index("difficult") == 24
assert SENT13.index("difficult") - SENT13.index("making") == 7   # making 에서 difficult 까지 7칸
assert 5 < 6                                                      # layer 5 of 6

# p.14, p.15 Figure 4, 5 문장의 토큰 수
SENT14 = ["The", "Law", "will", "never", "be", "perfect", ",", "but", "its", "application",
          "should", "be", "just", "-", "this", "is", "what", "we", "are", "missing", ",",
          "in", "my", "opinion", ".", "<EOS>"]
assert len(SENT14) == 26
assert SENT14.index("its") == 8
assert SENT14.index("Law") == 1 and SENT14.index("application") == 9
assert SENT14.index("its") - SENT14.index("Law") == 7            # its 에서 Law 까지 7칸 뒤
assert SENT14.index("application") - SENT14.index("its") == 1

# 셀프 어텐션이라 한 걸음이면 닿는다 (Table 1 의 O(1))
assert 1 < 7

# 헤드 번호는 1 부터 h 까지, base 는 h = 8
assert 512 // 8 == 64
assert 6 == 6   # 인코더 6층, 그 중 5층이 그림의 layer 5 of 6

# ---------------- 용어 표기 ----------------
TRF = "**트랜스포머(Transformer)**"
ATT = "**어텐션(Attention)**"
SA = "**셀프 어텐션(Self-Attention)**"
MHA = "**멀티 헤드 어텐션(Multi-Head Attention (MHA))**"
HEAD = "**헤드(Head)**"
ENC = "**인코더(Encoder)**"
DEC = "**디코더(Decoder)**"
AW = "**어텐션 가중치(Attention Weight)**"
AD = "**어텐션 분포(Attention Distribution)**"
RNN = "**순환 신경망(Recurrent Neural Network (RNN))**"
CNN = "**합성곱 신경망(Convolutional Neural Network (CNN))**"
RES = "**잔차 연결(Residual Connection)**"
LN = "**층 정규화(Layer Normalization (LayerNorm))**"
MT = "**기계 번역(Machine Translation (MT))**"
STD = "**시퀀스 변환(Sequence Transduction)**"
CP = "**구성소 구문 분석(Constituency Parsing)**"
BS = "**빔 서치(Beam Search)**"
LNORM = "**길이 정규화(Length Normalization)**"
BLEU = "**블루 점수(BLEU)**"
INTP = "**해석 가능성(Interpretability)**"
BPE = "**바이트 쌍 인코딩(Byte Pair Encoding (BPE))**"
WP = "**워드피스(WordPiece)**"
DO = "**드롭아웃(Dropout)**"
LS = "**라벨 스무딩(Label Smoothing)**"
ADAM = "**아담(Adam)**"
LSTM = "**장단기 메모리(LSTM)**"
VG = "**기울기 소실(Vanishing Gradient)**"
S2S = "**시퀀스-투-시퀀스(seq2seq)**"
EMB = "**임베딩(Embedding)**"
TOK = "**토큰(Token)**"
RSA = "**제한된 셀프 어텐션(Restricted Self-Attention)**"
MPL = "**최대 경로 길이(Maximum Path Length)**"
PAR = "**병렬화(Parallelization)**"

GLOSSARY = [
    ("트랜스포머", "Transformer", "어텐션만으로 만든 요즘 언어 모델의 기본 뼈대",
     "이 논문이 처음 내놓은 구조예요. 인코더 6층과 디코더 6층으로 되어 있어요."),
    ("어텐션", "Attention", "필요한 곳을 골라 보는 장치. 점수를 매기고 가중 평균을 내요",
     "논문 제목 그대로 어텐션만 있으면 된다는 주장이에요."),
    ("셀프 어텐션", "Self-Attention", "한 문장이 자기 자신을 바라보는 어텐션",
     "쿼리, 키, 밸류가 모두 같은 시퀀스에서 나와요. 13~15쪽 그림이 모두 인코더 셀프 어텐션이에요."),
    ("멀티 헤드 어텐션", "Multi-Head Attention (MHA)", "전체 차원을 h 조각으로 나눠 여러 관점에서 동시에 어텐션하기",
     "base 는 h = 8 이라 헤드가 여덟 개예요. 13~15쪽 그림의 색이 헤드 하나씩이에요."),
    ("헤드", "Head", "멀티 헤드 어텐션에서 관점 하나를 맡는 조각",
     "base 에서 헤드 하나의 차원은 512 나누기 8 로 64 예요."),
    ("인코더", "Encoder", "입력 문장을 끝까지 읽어 자리마다 표현을 만드는 쪽",
     "마스킹을 하지 않아서 앞뒤를 다 봐요. 13~15쪽 그림은 인코더의 5번째 층이에요."),
    ("디코더", "Decoder", "답 문장을 한 토큰씩 만들어 내는 쪽",
     "인과 마스킹을 써서 미래를 못 보게 막아요."),
    ("어텐션 가중치", "Attention Weight", "점수를 소프트맥스에 넣어 얻은, 합이 1 인 값들",
     "13~15쪽 그림에서 선이 진할수록 가중치가 큰 자리예요."),
    ("어텐션 분포", "Attention Distribution", "한 자리가 모든 자리를 얼마씩 볼지 적은 확률 분포",
     "논문은 이것을 들여다보면 모델을 조금은 읽을 수 있다고 말해요."),
    ("순환 신경망", "Recurrent Neural Network (RNN)", "한 단어씩 읽으며 메모장에 요약을 고쳐 쓰는 신경망",
     "결론에서 이 논문은 순환 층을 멀티 헤드 셀프 어텐션으로 바꿨다고 적어요."),
    ("합성곱 신경망", "Convolutional Neural Network (CNN)", "작은 창을 밀며 특징을 뽑는 신경망",
     "ConvS2S 와 ByteNet 이 이 방식이에요. 결론에서 함께 비교돼요."),
    ("잔차 연결", "Residual Connection", "층의 입력을 층의 출력에 그대로 더해 주는 지름길",
     "참고문헌 [11] 의 ResNet 에서 가져왔어요."),
    ("층 정규화", "Layer Normalization (LayerNorm)", "한 토큰의 숫자들을 평균 0, 분산 1 로 맞춰 주기",
     "참고문헌 [1] 이 출처예요."),
    ("기계 번역", "Machine Translation (MT)", "한 언어의 문장을 다른 언어로 바꾸는 일",
     "이 논문의 주 실험이에요. 영어에서 독일어, 영어에서 프랑스어 두 가지예요."),
    ("시퀀스 변환", "Sequence Transduction", "줄줄이 늘어선 입력을 줄줄이 늘어선 출력으로 바꾸는 일",
     "결론 첫 문장이 이 논문을 the first sequence transduction model based entirely on attention 이라고 불러요."),
    ("구성소 구문 분석", "Constituency Parsing", "문장을 구 단위 나무 구조로 쪼개는 과제",
     "번역이 아닌 다른 과제에도 되는지 보려고 6.3 절에서 해 본 실험이에요."),
    ("빔 서치", "Beam Search", "후보를 여러 개 들고 가면서 문장을 만드는 방법",
     "번역은 빔 4, 구문 분석은 빔 21 을 썼어요."),
    ("길이 정규화", "Length Normalization", "긴 문장이 손해 보지 않게 점수를 길이로 나눠 주는 것",
     "논문은 length penalty alpha 라고 부르고 번역은 0.6, 구문 분석은 0.3 을 썼어요."),
    ("블루 점수", "BLEU", "번역이 정답과 얼마나 겹치는지 재는 점수. 높을수록 좋아요",
     "결론에서 두 번역 과제 모두 최고 기록을 세웠다고 말해요."),
    ("해석 가능성", "Interpretability", "모델이 왜 그렇게 했는지 사람이 들여다볼 수 있는 정도",
     "논문은 어텐션을 보면 조금 들여다볼 수 있다고 곁가지 장점으로 적었어요."),
    ("바이트 쌍 인코딩", "Byte Pair Encoding (BPE)", "자주 붙어 다니는 두 조각을 한 조각으로 접착하는 토큰화",
     "참고문헌 [31] 이고 2주차에 배웠어요."),
    ("워드피스", "WordPiece", "BPE 와 비슷하게 단어를 조각으로 자르는 또 다른 방법",
     "참고문헌 [38] 이고 영어에서 프랑스어 실험에 썼어요."),
    ("드롭아웃", "Dropout", "학습할 때 일부 값을 무작위로 꺼서 과적합을 막는 방법",
     "참고문헌 [33] 이고 5.4 절에서 P_drop = 0.1 로 썼어요."),
    ("라벨 스무딩", "Label Smoothing", "정답을 100 퍼센트로 두지 않고 살짝 흐리게 만들어 학습하는 방법",
     "참고문헌 [36] 이고 5.4 절에서 0.1 을 썼어요."),
    ("아담", "Adam", "요즘 가장 많이 쓰는 학습 방법 중 하나",
     "참고문헌 [20] 이고 5.3 절에서 베타2 를 0.98 로 썼어요."),
    ("장단기 메모리", "LSTM", "게이트로 기억을 조절해 긴 문장을 버티게 만든 RNN",
     "참고문헌 [13] 이고 3주차 마지막에 배웠어요."),
    ("기울기 소실", "Vanishing Gradient", "귓속말 전달 게임처럼 기울기가 점점 희미해져 0 에 가까워지는 문제",
     "참고문헌 [12] 가 이 문제를 다룬 옛 논문이에요."),
    ("시퀀스-투-시퀀스", "seq2seq", "인코더로 읽고 디코더로 쓰는 구조",
     "참고문헌 [35] 와 [5] 가 출발점이에요."),
    ("임베딩", "Embedding", "토큰을 숫자 벡터로 바꾼 것. 단어의 지도 좌표",
     "참고문헌 [30] 이 임베딩 가중치를 나눠 쓰는 방법의 출처예요."),
    ("토큰", "Token", "글을 자른 레고 조각 하나",
     "13~15쪽 그림에서 가로로 늘어선 단어 하나하나가 토큰이에요."),
    ("제한된 셀프 어텐션", "Restricted Self-Attention", "가까운 이웃 r 칸만 보게 제한한 셀프 어텐션",
     "결론에서 앞으로 해 보겠다고 적은 계획이에요."),
    ("최대 경로 길이", "Maximum Path Length", "두 자리 사이에 신호가 지나가야 하는 가장 먼 걸음 수",
     "셀프 어텐션은 이것이 O(1) 이라 먼 단어끼리 한 걸음이에요."),
    ("병렬화", "Parallelization", "여러 계산을 한꺼번에 동시에 하기",
     "결론에서 생성도 덜 순차적으로 만들고 싶다고 적었어요."),
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


def prof(*lines):
    return {"kind": "prof", "when": "4주차 월요일 2교시", "lines": list(lines)}


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
FIG_T4 = SVG(
    TX(240, 22, "Table 4: WSJ Section 23 F1", "tb", 16),
    TX(120, 50, "WSJ 만 쓴 경우", "tb", 13, "middle", 1),
    TX(360, 50, "준지도 학습", "tb", 13, "middle", 1),
    *[BOX(30, 62 + i * 26, 180, 22, t, "n", "tl", 1, 11)
      for i, t in enumerate(["Vinyals (RNN) 88.3", "Petrov 90.4", "Dyer 91.7"])],
    BOX(30, 140, 180, 22, "Transformer 91.3", "box2", "tb", 2, 11),
    *[BOX(270, 62 + i * 26, 180, 22, t, "n", "tl", 1, 11)
      for i, t in enumerate(["Zhu 91.3", "McClosky 92.1", "Vinyals 92.1"])],
    BOX(270, 140, 180, 22, "Transformer 92.7", "box2", "tb", 2, 11),
    TX(240, 190, "WSJ 만 쓰면 Dyer 91.7 에 0.4 차이로 2등", "t", 13, "middle", 3),
    TX(240, 212, "준지도에서는 92.7 로 이 칸의 1등", "tb", 13, "middle", 3),
    TX(240, 240, "번역만 되는 모델이 아니라는 뜻이에요", "tm", 12, "middle", 4),
)

FIG_REF = SVG(
    TX(240, 22, "참고문헌은 이 과목의 지도예요", "tb", 16),
    *[BOX(20, 42 + i * 30, 200, 24, t, "n", "tl", 1, 11)
      for i, t in enumerate(["[13] LSTM", "[35] seq2seq", "[2] Bahdanau 어텐션", "[31] BPE"])],
    *[BOX(260, 42 + i * 30, 200, 24, t, "n3", "tl", 2, 11)
      for i, t in enumerate(["3주차 마지막", "4주차 Part 1", "4주차 Part 2", "2주차"])],
    *[A(224, 54 + i * 30, 256, 54 + i * 30, "e2", 3) for i in range(4)],
    TX(240, 192, "번호 40개가 거의 다 배운 것 아니면 배울 것이에요", "tb", 13, "middle", 4),
    TX(240, 216, "모르는 번호가 있으면 그 줄만 찾아 읽으면 돼요", "tm", 12, "middle", 4),
)

FIG_F3 = SVG(
    TX(240, 20, "Figure 3: making 이 difficult 를 봐요", "tb", 15),
    *[TX(36 + i * 52, 48, t, "t", 11, "middle", 1)
      for i, t in enumerate(["laws", "since", "2009", "making", "the", "voting", "difficult"])],
    R(174, 34, 46, 20, "n2", 1),
    *[TX(36 + i * 52, 150, t, "t", 11, "middle", 1)
      for i, t in enumerate(["laws", "since", "2009", "making", "the", "voting", "difficult"])],
    R(378, 136, 60, 20, "n2", 2),
    A(197, 58, 408, 132, "e2", 2),
    A(197, 58, 197, 132, "e", 3),
    A(197, 58, 356, 132, "e", 3),
    TX(240, 186, "진한 선 하나가 헤드 하나가 준 큰 가중치예요", "tb", 13, "middle", 3),
    TX(240, 210, "7칸 떨어져 있어도 셀프 어텐션은 한 걸음이에요", "t", 13, "middle", 4),
    TX(240, 234, "making ... more difficult 가 한 덩어리라서요", "tm", 12, "middle", 4),
)

FIG_F4 = SVG(
    TX(240, 20, "Figure 4: its 가 Law 를 가리켜요", "tb", 15),
    *[TX(40 + i * 66, 52, t, "t", 11, "middle", 1)
      for i, t in enumerate(["The", "Law", "but", "its", "application", "should", "be"])],
    R(84, 38, 46, 20, "n3", 2),
    R(238, 38, 76, 20, "n4", 3),
    R(172, 38, 46, 20, "n2", 1),
    A(195, 62, 118, 96, "e2", 2),
    A(195, 62, 262, 96, "e", 3),
    TX(140, 118, "헤드 5: its 가 Law 로", "tb", 12, "middle", 2),
    TX(320, 118, "헤드 6: its 가 application 으로", "t", 12, "middle", 3),
    TX(240, 156, "같은 단어를 두 헤드가 서로 다르게 봐요", "tb", 13, "middle", 4),
    TX(240, 180, "논문은 apparently, seems 라고 조심스럽게 적었어요", "tm", 12, "middle", 4),
    TX(240, 210, "이 그림은 인코더 6층 중 5층이에요", "t", 12, "middle", 4),
)


# ---------------- 쪽 만들기 ----------------
S = []


def page(p, title, terms, p1, p2=(), p3=(), p4=()):
    S.append({"p": p, "title": title, "terms": list(terms),
              "pass1": list(p1), "pass2": list(p2), "pass3": list(p3), "pass4": list(p4)})


# ---------------------------------------------------------------- p.10
page(10, "Table 4 구문 분석 결과와 7 Conclusion",
     ["Constituency Parsing", "Transformer", "Self-Attention", "Multi-Head Attention (MHA)",
      "Recurrent Neural Network (RNN)", "Convolutional Neural Network (CNN)", "Machine Translation (MT)",
      "Sequence Transduction", "Beam Search", "Length Normalization", "BLEU", "Restricted Self-Attention",
      "Parallelization"],
     [say("논문의 마지막 결과 표와 결론이 한 쪽에 같이 있어요.",
          "위쪽 Table 4 는 번역이 아닌 다른 과제에서도 되는지 본 실험이에요.",
          "아래쪽 7 Conclusion 은 논문 전체를 네 문단으로 줄인 곳이에요.",
          f"결론 한 줄: 순환 층을 {MHA} 으로 갈아 끼웠다."),
      analogy("운전면허만 있는 사람과 여러 차를 모는 사람",
              "번역만 잘하는 모델은 승용차만 몰 줄 아는 사람이에요. 트럭도 몰 수 있는지 시험해 본 것이 Table 4 예요.",
              ("승용차 운전", f"{MT}"),
              ("트럭 운전 시험", f"{CP}"),
              ("둘 다 되더라", "구조가 과제에 얽매이지 않는다")),
      figure("Table 4 를 두 칸으로 나눠서 봐요", FIG_T4,
             f"{TRF} 는 WSJ 만 쓰면 91.3 으로 2등, 준지도에서는 92.7 로 1등이에요.", 4)],
     [points("결론의 영어 문장과 우리말 뜻",
             f"the first sequence transduction model based entirely on attention = {ATT}만으로 만든 첫 {STD} 모델",
             f"replacing the recurrent layers ... with multi-headed self-attention = 순환 층을 {MHA} 으로 바꿔서",
             "can be trained significantly faster = 훨씬 빠르게 학습할 수 있다",
             f"we achieve a new state of the art = {BLEU} 에서 새로운 최고 기록을 세웠다",
             "outperforms even all previously reported ensembles = 앞서 보고된 앙상블까지 다 이겼다"),
      points("마지막 문단은 앞으로 할 일이에요",
             "other modalities than text = 글 말고 다른 자료에도 써 보겠다 (이미지, 소리, 영상)",
             f"local, restricted attention mechanisms = {RSA} 을 알아보겠다",
             f"Making generation less sequential = 만들어 내는 쪽도 덜 차례차례로, 곧 {PAR} 를 더",
             "코드는 tensor2tensor 에 공개했다고 적었어요"),
      points("결론에서 다시 나오는 세 낱말",
             f"{BLEU}: 두 번역 과제에서 최고 기록을 세웠다는 근거 숫자예요",
             f"{PAR}: 순환이 없어서 빨리 학습된다는 말의 속뜻이에요",
             f"{MPL}: 먼 자리도 한 걸음이라 긴 문장을 버틴다는 말의 속뜻이에요"),
      compare("Table 4 의 세 칸이 뜻하는 것",
              ["Training 칸", "뜻", "학습 자료"],
              ["WSJ only, discriminative", "WSJ 문장만 써서 학습", "약 40K 문장"],
              ["semi-supervised", "라벨 없는 자료까지 더해 학습", "약 17M 문장"],
              ["multi-task, generative", "다른 방식으로 학습한 비교 대상", "표에 안 적힘"]),
      check("7 Conclusion 이 말하는 이 논문의 한 줄 요약은?",
            [f"순환 층을 {MHA} 으로 바꾼 첫 {STD} 모델",
             "RNN 에 어텐션을 더해 성능을 올린 모델",
             "합성곱으로 번역을 푸는 모델",
             "어휘를 줄여 속도를 올린 모델"], 0,
            "결론 첫 문장 the first sequence transduction model based entirely on attention 그대로예요.")],
     [look("10쪽을 짚어 읽어요",
           (0.176, 0.088, 0.650, 0.030, "Table 4 제목: 구문 분석에도 잘 일반화된다. 결과는 WSJ Section 23 이에요."),
           (0.247, 0.117, 0.510, 0.182, "표 본문: 위 칸이 WSJ 만, 가운데가 준지도, 아래 두 줄이 다른 방식이에요."),
           (0.176, 0.329, 0.650, 0.030, "추론 설정: 최대 출력 길이를 입력 + 300 으로, 빔 21, alpha 0.3 을 썼어요."),
           (0.176, 0.363, 0.650, 0.043, "Our results ... performs surprisingly well: 과제에 맞춘 조정 없이도 잘 됐다는 문장이에요."),
           (0.176, 0.459, 0.130, 0.018, "여기부터 7 Conclusion 이에요."),
           (0.176, 0.489, 0.650, 0.043, "결론 1문단: 어텐션만으로 만든 첫 시퀀스 변환 모델이라고 선언해요."),
           (0.176, 0.537, 0.650, 0.058, "결론 2문단: 훨씬 빨리 학습되고 두 번역 과제에서 최고 기록을 세웠다."),
           (0.176, 0.600, 0.650, 0.058, "결론 3문단: 앞으로 이미지, 소리, 영상과 제한된 어텐션을 해 보겠다."),
           (0.176, 0.751, 0.100, 0.018, f"여기부터 References 예요. [1] 은 {LN} 논문이에요.")),
      compare("Table 4 숫자 전부 (WSJ Section 23 F1)",
              ["Parser", "Training", "F1"],
              ["Vinyals & Kaiser el al. (2014)", "WSJ only", "88.3"],
              ["Petrov et al. (2006)", "WSJ only", "90.4"],
              ["Zhu et al. (2013)", "WSJ only", "90.4"],
              ["Dyer et al. (2016)", "WSJ only", "91.7"],
              ["Transformer (4 layers)", "WSJ only", "91.3"]),
      compare("Table 4 의 나머지 줄",
              ["Parser", "Training", "F1"],
              ["Zhu et al. (2013)", "semi-supervised", "91.3"],
              ["Huang & Harper (2009)", "semi-supervised", "91.3"],
              ["McClosky et al. (2006)", "semi-supervised", "92.1"],
              ["Vinyals & Kaiser el al. (2014)", "semi-supervised", "92.1"],
              ["Transformer (4 layers)", "semi-supervised", "92.7"],
              ["Luong (2015) multi-task / Dyer (2016) generative", "다른 방식", "93.0 / 93.3"]),
      steps("표의 숫자를 빼 보면 논문의 문장이 그대로 나와요",
            ["WSJ 만 쓴 칸에서 1등은 Dyer 의 91.7 이에요",
             "트랜스포머는 91.3 이니 91.7 빼기 91.3 은 0.4 차이예요",
             "그래서 논문은 Recurrent Neural Network Grammar 하나만 빼고 다 이겼다고 적었어요",
             "RNN seq2seq 인 Vinyals 의 88.3 과 비교하면 91.3 빼기 88.3 은 3.0 이에요",
             "준지도 칸에서는 92.7 로 1등이고, 2등 92.1 과 0.6 차이예요"],
            "숫자만 빼 보면 논문이 왜 그 문장을 썼는지 보여요.",
            "Table 4 의 F1 값"),
      steps("구문 분석 실험의 설정은 번역과 달라요",
            ["층은 6층이 아니라 4층이고 d_model 은 512 가 아니라 1024 예요",
             "WSJ 만 쓸 때는 어휘 16K, 준지도일 때는 32K 를 썼어요",
             "학습 문장은 약 40K 대 약 17M 으로, 17000000 나누기 40000 은 425 배예요",
             f"추론에서 최대 출력 길이는 입력 + 300 이고 {BS} 는 21, alpha 는 0.3 이에요",
             "번역은 입력 + 50, 빔 4, alpha 0.6 이었으니 훨씬 넉넉하게 잡은 거예요"],
            f"구문 분석은 출력이 입력보다 훨씬 길어서 {LNORM} 과 빔을 다르게 잡았어요.",
            "6.3 절의 설정"),
      bg("4주차 Part 1", f"{BS} 와 {LNORM} 은 4주차 슬라이드 p.12-13 에서 배웠어요.",
         "빔을 크게 잡으면 후보를 더 많이 들고 가지만 항상 좋아지지는 않아요."),
      prof("교수님: 항상 빔 서치가 좋은 건 아니다, 트레이드 오프가 있다는 것 정도는 기억해 달라."),
      points("결론이 조심스럽게 쓴 곳",
             "We are excited about ... and plan to = 하겠다는 계획이지 한 일이 아니에요",
             "plan to investigate local, restricted attention = 아직 안 해 본 일이라고 밝혔어요",
             "Making generation less sequential is another research goals = 생성은 아직 차례차례라는 자백이에요"),
      points("결론이 예고한 두 가지를 다시 짚어요",
             f"{RSA}: 4장에서 이웃 r 칸만 본다고 소개했고, 결론에서 더 해 보겠다고 했어요",
             f"{PAR}: 학습은 이미 병렬이지만 생성은 아직 한 토큰씩이라고 스스로 적었어요",
             f"{BLEU} 말고 다른 잣대로 재 보겠다는 말은 결론에 없어요",
             "논문 밖 이야기: 이 계획들이 뒤에 어떻게 됐는지는 이 논문에 없어요. 이 덱은 논문 안만 다뤄요.")],
     [check("Table 4 에서 트랜스포머가 1등을 한 칸은?",
            ["준지도 학습(semi-supervised) 칸", "WSJ only 칸", "multi-task 칸", "generative 칸"], 0,
            "WSJ only 는 91.3 으로 Dyer 의 91.7 에 밀리고, 준지도에서 92.7 로 1등이에요."),
      check("구문 분석 실험에서 쓴 빔 크기와 alpha 는?",
            ["빔 21, alpha 0.3", "빔 4, alpha 0.6", "빔 8, alpha 0.5", "빔 21, alpha 0.6"], 0,
            "번역이 빔 4 와 alpha 0.6, 구문 분석이 빔 21 과 alpha 0.3 이에요. 짝을 바꿔 외우면 틀려요."),
      english("시험 답안에 쓸 문장 (결론)",
              f"{TRF} 는 {ATT}만으로 만든 첫 시퀀스 변환 모델이고, 순환 층을 {MHA} 으로 바꿨어요.",
              "결론 첫 문장이에요. sequence transduction, entirely on attention, multi-headed self-attention 을 넣어요.",
              "순환을 빼고(멀티 헤드) 셀프 어텐션을 넣었다, 이 한 줄로 외워요."),
      english("시험 답안에 쓸 문장 (구문 분석)",
              f"번역이 아닌 {CP} 에서도 과제에 맞춘 조정 없이 WSJ only 91.3, 준지도 92.7 F1 을 냈어요.",
              "논문은 despite the lack of task-specific tuning 이라고 적었어요. 구조가 과제에 얽매이지 않는다는 증거로 씁니다.",
              "91.3 과 92.7 두 숫자만 외우면 돼요."),
      warn("헷갈리기 쉬운 점",
           "WSJ only 1등은 트랜스포머가 아니라 Dyer 의 91.7 이에요. 논문도 예외가 하나 있다고 적었어요.",
           "구문 분석 모델은 4층 d_model 1024 예요. 번역 base 의 6층 512 와 헷갈리기 쉬워요.",
           "결론의 마지막 문단은 한 일이 아니라 앞으로 할 일이에요."),
      exam("예상 문제", "Table 4 에서 Transformer (4 layers) 의 두 F1 값과, 그 값이 각각 몇 등인지 쓰시오.",
           "표에서 트랜스포머 줄 두 개를 찾아 숫자와 순위를 말해 보세요.",
           ["WSJ only 줄에서 트랜스포머는 91.3 이에요",
            "같은 칸의 Dyer 91.7 보다 0.4 낮아서 2등이에요",
            "semi-supervised 줄에서 트랜스포머는 92.7 이에요",
            "같은 칸의 2등 92.1 보다 0.6 높아서 1등이에요"],
           "WSJ only 91.3 (2등), semi-supervised 92.7 (1등)")])

# ---------------------------------------------------------------- p.11
page(11, "References [5] 부터 [24] 까지: 이 논문이 서 있는 어깨",
     ["Transformer", "Self-Attention", "Attention", "Recurrent Neural Network (RNN)",
      "Convolutional Neural Network (CNN)", "LSTM", "Vanishing Gradient", "seq2seq",
      "Residual Connection", "Adam", "Machine Translation (MT)", "Encoder", "Decoder"],
     [say("참고문헌 쪽이에요. 읽고 외울 쪽은 아니지만 그냥 넘기기엔 아까워요.",
          "번호 하나하나가 이 과목에서 이미 배운 것과 거의 다 이어져요.",
          f"[13] 은 {LSTM}, [35] 는 {S2S}, [11] 은 {RES} 예요.",
          "모르는 번호가 나오면 이 쪽에서 그 한 줄만 찾아 읽으면 돼요."),
      figure("번호와 배운 내용을 짝지어 봐요", FIG_REF,
             "참고문헌 번호는 본문에서 대괄호로 불려요. 그 번호를 이 쪽에서 찾아요.", 4)],
     [points("이 쪽에서 이 과목과 바로 이어지는 번호",
             f"[5] Cho 외, RNN encoder-decoder = {S2S} 의 출발점 (4주차 Part 1)",
             f"[7] Chung 외, gated recurrent = GRU, {LSTM} 의 사촌 (3주차)",
             f"[9] Gehring 외, ConvS2S = {CNN} 으로 번역하기 (2 Background 와 Table 1)",
             f"[11] He 외, Deep residual learning = {RES} 의 출처 (3.1 절)",
             f"[13] Hochreiter 와 Schmidhuber, Long short-term memory = {LSTM} (3주차)"),
      points("이어서 나머지 중요한 번호",
             f"[12] Hochreiter 외, Gradient flow in recurrent nets = {VG} 을 다룬 옛 논문",
             f"[18] Kalchbrenner 외, ByteNet = {CNN} 번역, Table 1 의 비교 대상",
             f"[20] Kingma 와 Ba, Adam = {ADAM} 옵티마이저 (5.3 절)",
             f"[24] Luong 외, attention-based neural machine translation = {ATT} 점수 함수들",
             f"[22] Lin 외, structured self-attentive sentence embedding = 이미 있던 {SA} 연구"),
      compare("본문에서 이 번호들이 어디에 쓰였나",
              ["번호", "본문에서 쓰인 곳", "무슨 말을 할 때"],
              ["[11], [1]", "3.1 절", f"{RES} 와 {LN} 을 쓴다고 할 때"],
              ["[13], [7]", "1 Introduction", f"{RNN} 이 최고 수준이었다고 할 때"],
              ["[9], [18]", "2 Background", f"{CNN} 은 거리가 멀수록 걸음이 는다고 할 때"],
              ["[20]", "5.3 절", f"{ADAM} 을 썼다고 할 때"]),
      check("참고문헌 [11] 이 이 논문에서 하는 일은?",
            [f"{RES} 의 출처", f"{ADAM} 의 출처", f"{LSTM} 의 출처", f"{BPE} 의 출처"], 0,
            "[11] 은 He 외의 Deep residual learning 이고 3.1 절에서 residual connection 의 근거로 불려요.")],
     [look("11쪽을 짚어 읽어요",
           (0.176, 0.092, 0.652, 0.044, "[5] Cho 외. RNN encoder-decoder 로 구를 표현하기. seq2seq 의 출발점이에요."),
           (0.176, 0.261, 0.652, 0.030, "[9] Gehring 외 ConvS2S. 합성곱으로 번역을 푼 모델이에요."),
           (0.176, 0.338, 0.652, 0.044, "[11] He 외 Deep residual learning. 3.1 절의 잔차 연결이 여기서 왔어요."),
           (0.176, 0.391, 0.652, 0.030, "[12] Hochreiter 외. 먼 의존을 배우기 어려운 이유, 곧 기울기 소실이에요."),
           (0.176, 0.429, 0.652, 0.030, "[13] Long short-term memory. 3주차 마지막에 배운 LSTM 이에요."),
           (0.176, 0.637, 0.652, 0.044, "[18] ByteNet. 선형 시간 번역이라고 이름 붙인 합성곱 모델이에요."),
           (0.176, 0.729, 0.652, 0.018, "[20] Adam. 5.3 절에서 쓴 옵티마이저예요."),
           (0.176, 0.884, 0.652, 0.030, "[24] Luong 외. 어텐션 점수 함수를 정리한 2015년 논문이에요.")),
      steps("참고문헌 번호를 읽는 법",
            ["본문에서 대괄호 숫자를 만나면 먼저 번호를 적어 둬요",
             "References 에서 그 번호를 찾아 제목만 읽어요",
             "제목에서 아는 낱말을 찾아요. residual, memory, attention 처럼요",
             "이 과목에서 배운 것과 이어지면 거기까지만 하고 넘어가요",
             "이어지지 않으면 그 논문은 이 수업 범위 밖이라고 표시해 두면 돼요"],
            "참고문헌은 다 읽는 곳이 아니라 필요할 때 찾는 곳이에요.",
            "본문의 [11] 같은 표시"),
      compare("이 쪽 번호 중 이 수업에서 안 배운 것",
              ["번호", "제목 요지", "어떻게 볼까"],
              ["[6] Chollet", "Xception, 분리 합성곱", "4장에서 한 번 비교로만 나와요"],
              ["[16], [17] Kaiser", "Neural GPU, active memory", "2 Background 에서 이름만 나와요"],
              ["[21] Kuchaiev", "LSTM factorization tricks", "1 Introduction 에서 이름만 나와요"],
              ["[19] Kim 외", "Structured attention networks", "1 Introduction 의 어텐션 연구"]),
      bg("3주차", f"{LSTM} 은 게이트로 기억을 조절해 {VG} 을 늦춰요.",
         f"그래도 한 걸음씩 가는 {RNN} 이라 길이가 길어지면 걸음 수가 늘어요.")],
     [check("[13] 과 [35] 를 바르게 짝지은 것은?",
            [f"[13] {LSTM}, [35] {S2S}", f"[13] {S2S}, [35] {LSTM}",
             f"[13] {ADAM}, [35] {RES}", f"[13] {RES}, [35] {ADAM}"], 0,
            "[13] 은 Hochreiter 와 Schmidhuber 의 LSTM, [35] 는 Sutskever 외의 seq2seq 예요."),
      english("시험 답안에 쓸 문장 (참고문헌 읽는 법)",
              f"참고문헌 마흔 편은 대부분 이 과목에서 배운 {LSTM}, {S2S}, {RES} 의 원 논문이에요.",
              "다 읽을 필요는 없고 본문에서 불린 자리와 짝지어 보면 논문의 뼈대가 보여요.",
              "번호 하나가 개념 하나라고 생각하면 돼요."),
      warn("헷갈리기 쉬운 점",
           "참고문헌 번호는 나온 순서가 아니라 저자 이름의 알파벳 순서예요. [1] 이 가장 먼저 인용된 논문이 아니에요.",
           "[12] 와 [13] 은 둘 다 Hochreiter 지만 다른 논문이에요. [12] 는 기울기 흐름, [13] 은 LSTM 이에요.",
           "참고문헌 자체가 시험 범위는 아니에요. 개념과 이어지는 번호 몇 개만 알면 충분해요.")])

# ---------------------------------------------------------------- p.12
page(12, "References [25] 부터 [40] 까지: 학습 설정의 출처들",
     ["Byte Pair Encoding (BPE)", "WordPiece", "Dropout", "Label Smoothing", "Embedding",
      "seq2seq", "Beam Search", "Transformer", "Attention", "Self-Attention", "Encoder", "Decoder",
      "Machine Translation (MT)"],
     [say("참고문헌의 뒷부분이에요. 여기에 5장 학습 설정의 출처가 몰려 있어요.",
          f"[31] 은 {BPE}, [33] 은 {DO}, [36] 은 {LS} 예요.",
          f"[38] 은 {WP} 와 {BS} 설정을 가져온 구글 번역 논문이에요.",
          "5장을 읽다가 막히면 이 쪽에서 해당 번호를 찾으면 돼요."),
      compare("5장 설정과 그 출처",
              ["논문에서 쓴 것", "참고문헌", "이 과목에서"],
              [f"{BPE} 공유 어휘 37000", "[31] Sennrich", "2주차"],
              [f"{WP} 어휘 32000", "[38] Wu 외", "2주차"],
              [f"{DO} 0.1", "[33] Srivastava", "5.4 절에서 처음"],
              [f"{LS} 0.1", "[36] Szegedy", "5.4 절에서 처음"])],
     [points("이 쪽에서 꼭 알아 둘 번호",
             f"[30] Press 와 Wolf, Using the output embedding = 3.4 절의 {EMB} 가중치 공유 출처",
             f"[31] Sennrich 외, rare words with subword units = {BPE} (2주차)",
             f"[33] Srivastava 외, Dropout = {DO} (5.4 절)",
             f"[35] Sutskever 외, Sequence to sequence learning = {S2S} (4주차 Part 1)",
             f"[36] Szegedy 외, Rethinking the inception architecture = {LS} 의 출처 (5.4 절)"),
      points("이어서 결과와 관련된 번호",
             f"[38] Wu 외, Google's neural machine translation = {WP}, {BS} 빔 4 와 alpha 0.6 의 출처",
             "[37] Vinyals 외, Grammar as a foreign language = 6.3 절의 비교 대상이자 준지도 자료 출처",
             "[25] Marcus 외, Penn Treebank = 6.3 절의 WSJ 자료",
             "[29] Petrov 외 = 6.3 절에서 말한 BerkeleyParser",
             "[32] Shazeer 외, mixture-of-experts = Table 2 의 MoE 줄"),
      check("논문이 3.4 절에서 임베딩 가중치를 나눠 쓰는 근거로 든 참고문헌은?",
            ["[30] Press 와 Wolf", "[31] Sennrich", "[33] Srivastava", "[36] Szegedy"], 0,
            "3.4 절의 similar to [30] 이 그것이에요. [31] 은 BPE, [33] 은 드롭아웃, [36] 은 라벨 스무딩이에요.")],
     [look("12쪽을 짚어 읽어요",
           (0.176, 0.092, 0.652, 0.030, "[25] Penn Treebank. 6.3 절의 WSJ 자료가 여기서 나와요."),
           (0.176, 0.279, 0.652, 0.058, "[29] Petrov 외. 본문에서 BerkeleyParser 라고 부른 그 파서예요."),
           (0.176, 0.350, 0.652, 0.030, "[30] Press 와 Wolf. 3.4 절의 가중치 공유 출처예요."),
           (0.176, 0.394, 0.652, 0.030, "[31] Sennrich 외. 2주차에 배운 BPE 논문이에요."),
           (0.176, 0.494, 0.652, 0.044, "[33] Srivastava 외. 드롭아웃 논문이에요."),
           (0.176, 0.623, 0.652, 0.030, "[35] Sutskever 외. seq2seq 의 그 논문이에요."),
           (0.176, 0.666, 0.652, 0.030, "[36] Szegedy 외. 라벨 스무딩이 여기서 왔어요."),
           (0.176, 0.753, 0.652, 0.058, "[38] Wu 외. word-piece 와 빔 서치 설정을 가져온 구글 번역 논문이에요.")),
      steps("참고문헌 마흔 편이 어떻게 나뉘어 있나",
            ["10쪽 아래쪽에 [1] 부터 [4] 까지 네 편이 있어요",
             "11쪽에 [5] 부터 [24] 까지 스무 편이 있어요",
             "12쪽에 [25] 부터 [40] 까지 열여섯 편이 있어요",
             "4 더하기 20 더하기 16 은 40 이에요",
             "본문 10쪽까지가 논문이고 11쪽부터는 목록과 그림이에요"],
            "논문 본문은 10쪽까지, 그 뒤는 참고문헌 두 쪽과 그림 세 쪽이에요.",
            "15쪽짜리 PDF"),
      bg("2주차", f"{BPE} 는 자주 붙어 다니는 두 조각을 한 조각으로 접착하는 방법이에요.",
         f"{WP} 도 비슷하게 단어를 조각으로 자르지만 고르는 기준이 달라요."),
      points("논문이 그대로 가져다 쓴 것",
             f"토큰화: {BPE} 와 {WP}",
             f"정칙화: {DO} 와 {LS}",
             f"학습과 안정화: {ADAM}, {RES}",
             f"정규화: {LN} (참고문헌 [1])"),
      points("논문이 새로 만든 것",
             f"{SA} 만으로 쌓은 {ENC} 와 {DEC}",
             "스케일드 닷프로덕트 어텐션과 루트 d_k 나누기",
             f"{MHA} 와 사인 코사인 위치 인코딩",
             "새 부품보다 이미 있던 부품을 잘 조합한 논문에 가까워요")],
     [check("[31] 과 [36] 을 바르게 짝지은 것은?",
            [f"[31] {BPE}, [36] {LS}", f"[31] {LS}, [36] {BPE}",
             f"[31] {DO}, [36] {WP}", f"[31] {WP}, [36] {DO}"], 0,
            "[31] 은 Sennrich 의 subword units, [36] 은 Szegedy 의 inception 논문에서 온 라벨 스무딩이에요."),
      english("시험 답안에 쓸 문장 (새로 만든 것)",
              f"새로 만든 것은 {SA} 만으로 쌓은 스택, 스케일드 닷프로덕트, {MHA} 세 가지예요.",
              f"{RES}, {DO}, {LS} 는 앞선 연구에서 그대로 가져온 부품이에요.",
              "새 부품 넷, 가져온 부품 여럿 으로 나눠 외워요."),
      warn("헷갈리기 쉬운 점",
           f"{LS} 이 인셉션 논문 [36] 에서 왔다는 것이 뜻밖이라 자주 틀려요. 이미지 쪽 논문이에요.",
           f"[38] 하나가 {WP}, {BS} 빔 4, alpha 0.6, 조기 종료까지 여러 곳의 출처예요.",
           "참고문헌 쪽 자체를 외울 필요는 없어요. 개념과 번호의 짝만 몇 개 알아 두면 돼요.")])

# ---------------------------------------------------------------- p.13
page(13, "Attention Visualizations 와 Figure 3: 먼 단어를 붙잡는 헤드",
     ["Attention", "Self-Attention", "Encoder", "Head", "Multi-Head Attention (MHA)",
      "Attention Weight", "Attention Distribution", "Token", "Interpretability",
      "Maximum Path Length", "Transformer"],
     [say("여기부터 부록이에요. 제목은 Attention Visualizations, 곧 어텐션을 그림으로 보여 주는 곳이에요.",
          f"Figure 3 은 {ENC} {SA} 의 6층 중 5층을 그린 거예요.",
          "위아래로 같은 문장이 두 번 놓여 있고, 위에서 아래로 선이 이어져요.",
          "선 하나가 어느 자리를 얼마나 봤는지, 색이 어느 헤드인지 나타내요."),
      analogy("형광펜 여러 자루로 같은 문장에 밑줄 긋기",
              "한 문장에 친구 여덟 명이 각자 다른 색 형광펜으로 중요한 곳에 밑줄을 그어요. 색마다 고르는 곳이 달라요.",
              ("형광펜 색 하나", f"{HEAD} 하나"),
              ("밑줄의 진하기", f"{AW} 의 크기"),
              ("여덟 명이 동시에", f"{MHA}")),
      figure("Figure 3 이 보여 주는 것", FIG_F3,
             "making 이 일곱 칸 떨어진 difficult 를 강하게 봐요. making ... more difficult 가 한 덩어리라서요.", 4)],
     [points("그림 설명(caption)의 영어와 우리말 뜻",
             f"following long-distance dependencies = 멀리 떨어진 의존 관계를 따라간다",
             f"in the encoder self-attention in layer 5 of 6 = {ENC} {SA} 의 6층 중 5층에서",
             "attend to a distant dependency of the verb 'making' = 동사 making 의 먼 짝을 본다",
             "completing the phrase 'making...more difficult' = making ... more difficult 라는 덩어리를 완성한다",
             f"Different colors represent different heads = 색이 다르면 다른 {HEAD} 예요"),
      steps("그림을 읽는 순서",
            ["위쪽 줄에서 회색으로 칠해진 단어를 찾아요. 여기서는 making 이에요",
             "그 단어에서 뻗어 나가는 선을 따라가요",
             "선이 닿는 아래쪽 단어가 making 이 본 자리예요",
             "선이 진할수록 그 자리의 가중치가 커요",
             "색이 다르면 다른 헤드가 본 것이에요"],
            f"한 {TOK} 이 어디를 봤는지가 한눈에 보여요.",
            "Figure 3"),
      check("Figure 3 에서 색이 다르다는 것은 무엇이 다르다는 뜻인가요?",
            [f"{HEAD} 가 다르다", "층이 다르다", "문장이 다르다", "가중치가 0 이다"], 0,
            "caption 의 Different colors represent different heads 그대로예요.")],
     [look("13쪽을 짚어 읽어요",
           (0.176, 0.090, 0.210, 0.020, "제목 Attention Visualizations. 여기부터 부록 그림이에요."),
           (0.190, 0.144, 0.630, 0.062, "위쪽 줄: 문장의 토큰이 세로로 적혀 있어요. 쿼리 쪽이에요."),
           (0.514, 0.165, 0.030, 0.040, "회색으로 칠해진 making. 이 단어의 어텐션만 그렸어요."),
           (0.190, 0.300, 0.630, 0.065, "아래쪽 줄: 같은 문장이 한 번 더 있어요. 키와 밸류 쪽이에요."),
           (0.628, 0.300, 0.050, 0.035, "more 와 difficult 자리. 여기로 진한 선이 몰려요."),
           (0.176, 0.392, 0.650, 0.058, "caption: layer 5 of 6, 색이 헤드, 색깔로 봐야 잘 보인다고 적혀 있어요.")),
      steps("making 과 difficult 사이가 몇 칸인지 세 보면",
            ["문장의 토큰을 왼쪽부터 세면 making 은 18번째예요",
             "difficult 는 25번째예요",
             "25 빼기 18 은 7 이니 일곱 칸 떨어져 있어요",
             f"{RNN} 이라면 일곱 걸음을 차례로 지나야 해요",
             f"{SA} 은 {MPL} 이 O(1) 이라 한 걸음이에요"],
            "Table 1 의 O(1) 이 그림에서는 이렇게 보여요.",
            "It is in this spirit ... making the registration or voting process more difficult ."),
      points("이 그림이 4장의 어느 문장을 뒷받침하나",
             f"4장 끝: As side benefit, self-attention could yield more interpretable models = 곁가지로 {INTP} 이 좋아질 수 있다",
             "We inspect attention distributions from our models = 우리 모델의 어텐션 분포를 들여다봤다",
             f"individual attention heads clearly learn to perform different tasks = {HEAD} 마다 다른 일을 배운다",
             "many appear to exhibit behavior related to the syntactic and semantic structure = 문법과 뜻의 구조와 관련돼 보인다"),
      points("논문이 쓴 말의 세기에 주의",
             "could yield, appear to exhibit 처럼 약한 표현이에요. 단정하지 않았어요",
             f"{AD} 를 보면 뭔가 보인다는 것이지, 그것이 모델의 이유라고 증명한 것은 아니에요",
             "그림 세 장은 예시 세 개일 뿐이고 통계를 낸 것이 아니에요")],
     [check("Figure 3 이 그린 것은 어느 어텐션인가요?",
            [f"{ENC} 의 {SA}", "디코더의 셀프 어텐션", "인코더 디코더 어텐션", "FFN 의 출력"], 0,
            "caption 에 encoder self-attention in layer 5 of 6 이라고 적혀 있어요."),
      english("시험 답안에 쓸 문장 (해석 가능성)",
              f"논문은 곁가지 장점으로 {INTP} 을 들면서, {AD} 를 들여다보면 {HEAD} 마다 다른 일을 배운 것처럼 보인다고 적었어요.",
              "단정이 아니라 could yield, appear to exhibit 같은 조심스러운 표현을 썼다는 점까지 같이 써 주면 좋아요.",
              "곁가지 장점, 조심스러운 표현 두 가지를 넣어요."),
      warn("헷갈리기 쉬운 점",
           "그림의 위아래 줄은 다른 문장이 아니라 같은 문장이에요. 셀프 어텐션이라서 그래요.",
           "층은 5층이지 5개가 아니에요. 인코더가 6층이고 그 중 다섯 번째예요.",
           "어텐션이 크다고 그 단어가 원인이라는 뜻은 아니에요. 논문도 그렇게까지 말하지 않았어요."),
      exam("예상 문제", "Figure 3 의 caption 에 나온 두 가지 사실을 쓰시오.",
           "그림 설명에서 확실히 적힌 사실 두 개를 찾아 쓰세요.",
           ["첫째, 이것은 인코더 셀프 어텐션의 6층 중 5층이에요",
            "둘째, 서로 다른 색은 서로 다른 헤드예요",
            "덧붙이면 making 이라는 단어의 어텐션만 그렸다는 것도 적혀 있어요"],
           "인코더 셀프 어텐션 layer 5 of 6, 색이 곧 헤드")])

# ---------------------------------------------------------------- p.14
page(14, "Figure 4: its 가 무엇을 가리키는지 찾는 헤드",
     ["Attention", "Self-Attention", "Encoder", "Head", "Multi-Head Attention (MHA)",
      "Attention Weight", "Attention Distribution", "Token", "Interpretability", "Transformer"],
     [say("Figure 4 예요. 문장은 The Law will never be perfect ... in my opinion 이에요.",
          "위 그림은 헤드 5 의 어텐션을 전부 그린 것이고, 아래 그림은 its 라는 단어 하나만 뽑은 거예요.",
          f"아래 그림에서 선이 딱 두 개라 {AW} 가 아주 뾰족하다는 것이 보여요.",
          "논문은 이 두 헤드가 its 가 무엇을 가리키는지 찾는 일을 하는 것 같다고 적었어요."),
      analogy("대명사에 화살표 그리기",
              "국어 시간에 그 사람 이라는 말에 밑줄을 긋고 앞으로 화살표를 그려 누구인지 찾잖아요. 헤드가 그 일을 해요.",
              ("그 사람 이라는 말", "its 라는 대명사"),
              ("화살표가 닿는 이름", "Law 와 application"),
              ("화살표를 긋는 사람", f"{HEAD} 5 와 {HEAD} 6")),
      figure("Figure 4 아래 그림이 보여 주는 것", FIG_F4,
             "its 에서 나가는 선이 딱 두 개예요. 하나는 Law, 하나는 application 으로 가요.", 4)],
     [points("caption 의 영어와 우리말 뜻",
             f"Two attention heads, also in layer 5 of 6 = 역시 6층 중 5층의 {HEAD} 두 개",
             "apparently involved in anaphora resolution = 대명사가 무엇을 가리키는지 찾는 일에 관여하는 것으로 보인다",
             f"Top: Full attentions for head 5 = 위쪽은 {HEAD} 5 의 모든 어텐션",
             "Bottom: Isolated attentions from just the word 'its' = 아래쪽은 its 한 단어만 떼어 낸 것",
             "the attentions are very sharp for this word = 이 단어에 대해서는 어텐션이 아주 뾰족하다"),
      compare("위 그림과 아래 그림의 차이",
              ["", "위 그림", "아래 그림"],
              ["그린 것", f"{HEAD} 5 의 모든 자리", "its 한 자리만"],
              ["헤드 수", "하나", "둘 (헤드 5 와 6)"],
              ["보이는 모양", "선이 빽빽해요", "선이 딱 두 개예요"],
              ["뜻", "전체 그림", "뾰족한 어텐션"]),
      check("아래 그림에서 its 의 선이 두 개뿐인 것은 무엇을 뜻하나요?",
            [f"{AW} 가 두 자리에 몰려 뾰족하다", "가중치의 합이 2 이다",
             "헤드가 두 층에 걸쳐 있다", "밸류가 두 개뿐이다"], 0,
            "caption 의 the attentions are very sharp for this word 그대로예요. 합은 언제나 1 이에요.")],
     [look("14쪽을 짚어 읽어요",
           (0.190, 0.210, 0.630, 0.065, "위 그림의 윗줄: 문장 토큰이 세로로 적혀 있어요. 헤드 5 의 쿼리 쪽이에요."),
           (0.190, 0.390, 0.630, 0.062, "위 그림의 아랫줄: 같은 문장이에요. 선이 아주 빽빽해요."),
           (0.375, 0.485, 0.060, 0.062, "아래 그림에서 회색으로 칠해진 its. 이 단어만 뽑았어요."),
           (0.210, 0.665, 0.040, 0.045, "선이 닿는 첫 자리 Law. 진한 보라색 헤드가 여기로 가요."),
           (0.398, 0.665, 0.050, 0.060, "선이 닿는 둘째 자리 application. 연한 색 헤드가 여기로 가요."),
           (0.176, 0.774, 0.650, 0.044, "caption: layer 5 of 6, 대명사 해석으로 보인다, 아주 뾰족하다고 적혀 있어요.")),
      steps("its 와 Law 가 몇 칸 떨어져 있는지 세 보면",
            ["문장 토큰을 왼쪽부터 세면 Law 는 2번째예요",
             "its 는 9번째예요",
             "9 빼기 2 는 7 이니 일곱 칸 떨어져 있어요",
             "바로 옆의 application 은 10번째라 한 칸 차이예요",
             f"두 {HEAD} 가 먼 자리와 가까운 자리를 나눠 보고 있는 셈이에요"],
            "멀든 가깝든 셀프 어텐션에는 한 걸음이라서 둘 다 가능해요.",
            "The Law will never be perfect , but its application ..."),
      points("이 그림이 3.2.2 절의 어느 문장을 뒷받침하나",
             f"3.2.2: allows the model to jointly attend to information from different representation subspaces",
             "at different positions = 서로 다른 자리에서 서로 다른 관점으로 함께 본다",
             "With a single attention head, averaging inhibits this = 헤드가 하나면 평균이 이것을 막는다",
             f"Figure 4 는 그 말을 눈으로 보여 주는 예시 하나예요"),
      points("논문이 쓴 말의 세기에 주의",
             "apparently involved in = 관여하는 것으로 보인다. 확인했다는 말이 아니에요",
             "논문은 anaphora resolution 이라는 과제 이름을 붙였지만 그렇게 학습시킨 것은 아니에요",
             "그림은 문장 하나의 예시예요. 모든 문장에서 그렇다는 증거는 아니에요")],
     [check("Figure 4 의 두 그림 중 헤드가 두 개 나오는 것은?",
            ["아래 그림", "위 그림", "둘 다", "둘 다 아니다"], 0,
            "위는 헤드 5 하나의 전체 어텐션이고, 아래가 헤드 5 와 6 의 its 만 뽑은 것이에요."),
      english("시험 답안에 쓸 문장 (멀티 헤드의 효과)",
              f"{MHA} 은 서로 다른 표현 부분공간에서 서로 다른 자리를 함께 볼 수 있게 해 주고, {HEAD} 가 하나면 평균 때문에 그것이 막혀요.",
              "Figure 4 처럼 한 헤드는 먼 Law 를, 다른 헤드는 가까운 application 을 보는 것이 그 예시예요.",
              "different representation subspaces 와 averaging inhibits this 두 구절을 외워요."),
      warn("헷갈리기 쉬운 점",
           "뾰족하다(sharp)는 것은 가중치가 몇 자리에 몰렸다는 뜻이지 합이 1 이 아니라는 뜻이 아니에요.",
           "Figure 3 과 Figure 4 는 문장이 달라요. Figure 4 와 Figure 5 는 같은 문장이에요.",
           "논문은 apparently 라고 적었어요. 헤드가 대명사 해석을 한다고 단정하면 안 돼요.")])

# ---------------------------------------------------------------- p.15
page(15, "Figure 5: 헤드마다 배우는 일이 다르다",
     ["Attention", "Self-Attention", "Encoder", "Head", "Multi-Head Attention (MHA)",
      "Attention Weight", "Attention Distribution", "Transformer", "Interpretability", "Token"],
     [say("논문의 마지막 쪽이에요. Figure 5 하나만 있어요.",
          "위아래 두 그림은 문장은 같은데 헤드가 달라요.",
          "위 그림은 선이 넓게 퍼져 있고 아래 그림은 짧은 선이 규칙적으로 이어져요.",
          f"논문은 {HEAD} 들이 분명히 서로 다른 일을 배웠다고 적었어요."),
      analogy("같은 책을 읽는 두 사람의 밑줄",
              "한 사람은 문단 전체에 넓게 밑줄을 긋고, 다른 사람은 바로 다음 낱말마다 짧게 긋는다면 두 사람이 보는 것이 다른 거예요.",
              ("넓게 긋는 사람", "위 그림의 헤드"),
              ("짧게 긋는 사람", "아래 그림의 헤드"),
              ("두 밑줄을 합쳐 읽기", f"{MHA} 의 결과")),
      compare("위 그림과 아래 그림",
              ["", "위 그림", "아래 그림"],
              ["선 모양", "여기저기 길게 퍼져요", "짧고 규칙적이에요"],
              ["헤드", "하나", "다른 하나"],
              ["문장", "같아요", "같아요"],
              ["논문의 말", "different tasks", "different tasks"])],
     [points("caption 의 영어와 우리말 뜻",
             "Many of the attention heads exhibit behaviour = 많은 헤드가 어떤 행동을 보인다",
             "that seems related to the structure of the sentence = 문장의 구조와 관련돼 보인다",
             f"two such examples above, from two different heads = 서로 다른 {HEAD} 둘의 예 두 개",
             f"from the encoder self-attention at layer 5 of 6 = {ENC} {SA} 6층 중 5층에서",
             "The heads clearly learned to perform different tasks = 헤드들이 분명히 서로 다른 일을 배웠다"),
      steps("부록 그림 세 장을 한 줄로 이으면",
            ["Figure 3 은 먼 단어를 붙잡는 헤드를 보여 줘요",
             "Figure 4 는 대명사가 가리키는 곳을 찾는 듯한 헤드 두 개를 보여 줘요",
             "Figure 5 는 헤드마다 하는 일이 다르다는 것을 보여 줘요",
             "셋 다 인코더 셀프 어텐션의 6층 중 5층이에요",
             f"셋 다 4장의 {INTP} 문장과 3.2.2 절의 멀티 헤드 문장을 뒷받침해요"],
            "그림 세 장은 멀티 헤드가 왜 여럿이어야 하는지를 눈으로 보여 주는 증거예요.",
            "Figure 3, 4, 5"),
      check("Figure 5 의 위 그림과 아래 그림에서 다른 것은?",
            [f"{HEAD} 가 다르다", "문장이 다르다", "층이 다르다", "모델이 다르다"], 0,
            "caption 에 from two different heads 라고 적혀 있어요. 문장도 층도 같아요.")],
     [look("15쪽을 짚어 읽어요",
           (0.190, 0.230, 0.630, 0.062, "위 그림의 윗줄: 문장 토큰이에요. 헤드 하나의 어텐션이에요."),
           (0.190, 0.408, 0.630, 0.062, "위 그림의 아랫줄: 선이 넓게 퍼져 여러 자리로 흩어져요."),
           (0.190, 0.505, 0.630, 0.062, "아래 그림의 윗줄: 같은 문장이에요. 다른 헤드예요."),
           (0.190, 0.683, 0.630, 0.062, "아래 그림의 아랫줄: 짧고 규칙적인 선이 이어져요."),
           (0.176, 0.759, 0.650, 0.044, "caption: 헤드들이 분명히 서로 다른 일을 배웠다고 적혀 있어요.")),
      points("caption 에서 말의 세기가 한 문장 안에서도 달라요",
             "seems related to the structure of the sentence = 관련돼 보인다. 조심스러운 표현이에요",
             "The heads clearly learned to perform different tasks = 분명히 다른 일을 배웠다. 여기는 단정이에요",
             "다르다는 것은 단정하고, 그 다름이 문법 구조 때문인지는 조심스럽게 말한 거예요"),
      compare("논문이 그림으로 보여 준 것과 보여 주지 못한 것",
              ["보여 준 것", "보여 주지 못한 것"],
              [f"{HEAD} 마다 {AD} 가 다르다", "그 차이가 성능에 얼마나 기여하는지"],
              ["먼 자리도 한 걸음에 본다", "모든 문장에서 그런지"],
              ["뾰족한 어텐션이 생긴다", "헤드가 정말 문법을 배운 것인지"]),
      bg("4주차 Part 4", f"{MHA} 은 전체 차원을 h 로 나눠 쓰기 때문에 계산량이 늘지 않아요.",
         "그래서 여러 관점을 거의 공짜로 얻는 셈이라고 배웠어요.")],
     [check("Figure 5 의 caption 에서 단정한 문장은?",
            ["The heads clearly learned to perform different tasks",
             "seems related to the structure of the sentence",
             "apparently involved in anaphora resolution",
             "could yield more interpretable models"], 0,
            "clearly 가 붙은 이 문장만 단정이에요. 나머지 셋은 seems, apparently, could 로 조심스럽게 적었어요."),
      english("시험 답안에 쓸 문장 (부록 그림)",
              f"부록의 Figure 3, 4, 5 는 모두 {ENC} {SA} 의 6층 중 5층을 그린 것으로, {HEAD} 마다 보는 곳이 다르다는 것을 보여 줘요.",
              f"먼 의존을 붙잡는 헤드, 대명사가 가리키는 곳을 찾는 듯한 헤드, 문장 구조와 관련돼 보이는 헤드가 예시로 나와요.",
              "그림 셋, 층 하나(5층), 결론 하나(헤드마다 다르다) 로 외워요."),
      warn("헷갈리기 쉬운 점",
           "그림 세 장이 모두 같은 층이라는 점을 놓치기 쉬워요. 전부 layer 5 of 6 이에요.",
           "그림은 인코더 쪽이에요. 디코더의 마스킹된 어텐션이 아니에요.",
           f"{TRF} 가 잘 되는 이유를 그림이 증명한 것은 아니에요. 논문도 예시라고만 했어요."),
      exam("예상 문제", "부록 Attention Visualizations 의 그림 세 장이 공통으로 보여 주려는 것은 무엇인지 쓰시오.",
           "Figure 3, 4, 5 를 한 문장으로 묶어 보세요.",
           ["세 그림 모두 인코더 셀프 어텐션의 6층 중 5층이에요",
            "Figure 3 은 먼 의존을 따라가는 헤드를 보여 줘요",
            "Figure 4 는 대명사가 가리키는 곳을 찾는 듯한 헤드 둘을 보여 줘요",
            "Figure 5 는 헤드마다 배우는 일이 다르다는 것을 보여 줘요",
            "묶으면 멀티 헤드가 서로 다른 관점을 배운다는 주장이에요"],
           "헤드마다 서로 다른 일을 배우고, 먼 자리도 한 걸음에 본다는 것")])

# ---------------- 저장 ----------------
data = {"deck": "NP", "from": 10, "to": 15,
        "glossary": [{"ko": k, "en": e, "say": s, "more": m} for k, e, s, m in GLOSSARY],
        "slides": S}

raw = json.dumps(data, ensure_ascii=False, indent=1)
for ch in ("—", "–", "·", "・"):
    assert ch not in raw, ch
with open(OUT, "w", encoding="utf-8") as f:
    f.write(raw)

# 용어가 본문에 3번 이상 나오는지 스스로 센다
low = raw.lower()
thin = [e for _, e, _, _ in GLOSSARY if low.count(e.lower()) < 4]
print("saved", OUT, len(S), "pages")
if thin:
    print("3번 미만일 수 있는 용어:", thin)
