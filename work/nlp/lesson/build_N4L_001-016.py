# -*- coding: utf-8 -*-
"""N4L (4주차 실습 Lab 3 Self-Attention from Scratch) 회독 레슨 1-16쪽 -> N4L_001-016.json
코드와 저장된 출력은 work/nlp/labs/N4L_pages.json 에서 그대로 가져온다(금지 문자만 바꿈).
줄 설명은 셀 번호별로 여기 적는다. 출력 숫자로 하는 손계산은 assert 로 확인한다.
"""
import json, math, pathlib

W = pathlib.Path(__file__).resolve().parent.parent
PAGES = json.loads((W / "labs" / "N4L_pages.json").read_text(encoding="utf-8"))["pages"]
SRC = {c["n"]: c["src"] for p in PAGES for c in p["cells"]}
OUTS = {c["n"]: (c["out"] or "") for p in PAGES for c in p["cells"]}
FIX = {"—": "-", "–": "-", "·": ",", "・": ",", "…": "...", "−": "-"}


def clean(s):
    for a, b in FIX.items():
        s = s.replace(a, b)
    return s


def smax(xs):
    m = max(xs)
    e = [math.exp(x - m) for x in xs]
    t = sum(e)
    return [v / t for v in e]


# ---- 저장된 출력으로 확인하는 숫자들
sc = [1 * 0.5, 1 * 0.0, 1 * 3.0, -1 * 0.5]
assert sc == [0.5, 0.0, 3.0, -0.5] and "[ 0.5  0.   3.  -0.5]" in OUTS[5]
wt = smax(sc)
assert [round(v, 3) for v in wt] == [0.071, 0.043, 0.861, 0.026]
assert "[0.071 0.043 0.861 0.026]" in OUTS[5]
vals = [[10.0, 0.0], [0.0, 10.0], [5.0, 5.0], [-9.0, -9.0]]
o0 = sum(wt[i] * vals[i][0] for i in range(4))
o1 = sum(wt[i] * vals[i][1] for i in range(4))
assert [round(o0, 2), round(o1, 2)] == [4.78, 4.5] and "[4.78 4.5 ]" in OUTS[5]

base = [2.0, 1.4, 1.0, 0.8, 0.5, 0.3]
assert round(max(smax([b * 0.2 for b in base])), 3) == 0.202
assert round(max(smax([b * 1.0 for b in base])), 3) == 0.381
assert round(max(smax([b * 6.0 for b in base])), 3) == 0.97
assert "max weight=0.202" in OUTS[7] and "max weight=0.970" in OUTS[7]

assert round(math.sqrt(8), 2) == 2.83 and round(math.sqrt(64), 2) == 8.0
assert round(math.sqrt(512), 2) == 22.63
assert "2.83" in OUTS[9] and "22.63" in OUTS[9]

assert round(2.359e-01 / 2.891e-02, 1) == 8.2
assert "2.359e-01" in OUTS[11] and "2.891e-02" in OUTS[11]

assert "(5, 5)" in OUTS[13] and "(5, 16)" in OUTS[13]
assert "1.33e-15" in OUTS[15]
assert "(2, 4, 7, 16)" in OUTS[21] and "2.384185791015625e-07" in OUTS[21]
assert "(2, 4, 7, 7)" in OUTS[23]

qkv = 64 * (3 * 64) + 3 * 64
proj = 64 * 64 + 64
assert qkv == 12480 and proj == 4160 and qkv + proj == 16640
assert "16,640" in OUTS[25]

BADPRE = ("Warning", "WARNING")


def outpts(n, head="강의 노트북에 저장된 출력", lo=0, hi=None, maxn=6):
    ls = []
    for l in clean(OUTS[n]).replace("✓", "(OK)").split("\n"):
        t = l.rstrip()
        if not t.strip() or t.startswith(BADPRE) or "%|" in t or "downloading bytes" in t:
            continue
        if "reconstructing file" in t:
            continue
        ls.append(t)
    ls = ls[lo:hi][:maxn]
    return {"kind": "points", "head": head, "items": [f"`{l.strip()}`" for l in ls]}


def code(n, head, lines, link=None, part=None):
    src = clean(SRC[n])
    ls = src.split("\n")
    cover = set()
    for a, b, _ in lines:
        cover.update(range(a, b + 1))
    need = {i + 1 for i, l in enumerate(ls) if l.strip()}
    assert need <= cover, (n, sorted(need - cover))
    assert max(cover) <= len(ls), (n, max(cover), len(ls))
    f = {"kind": "code", "head": head, "file": f"Lab3 노트북 셀 {n}" + (f" {part}" if part else ""), "code": src,
         "lines": [{"from": a, "to": b, "say": s} for a, b, s in lines]}
    if link:
        f["link"] = link
    return f


def say(*lines):
    return {"kind": "say", "lines": list(lines)}


def pts(head, *items):
    return {"kind": "points", "head": head, "items": list(items)}


def py(name, say_lines, example, out=None):
    f = {"kind": "pyterm", "name": name, "say": list(say_lines), "example": example}
    if out:
        f["out"] = out
    return f


def check(q, choices, a, why):
    return {"kind": "check", "q": q, "choices": choices, "a": a, "why": why}


def warn(head, *items):
    return {"kind": "warn", "head": head, "items": list(items)}


def ana(head, scene, pairs):
    return {"kind": "analogy", "head": head, "scene": scene, "map": [list(p) for p in pairs]}


def steps(head, st, answer, given=None):
    f = {"kind": "steps", "head": head, "steps": st, "answer": answer}
    if given:
        f["given"] = given
    return f


def formula(head, tex, parts, whole):
    return {"kind": "formula", "head": head, "tex": tex, "parts": [{"sym": a, "say": b} for a, b in parts], "whole": whole}


def cmp(head, cols, rows):
    return {"kind": "compare", "head": head, "cols": list(cols), "rows": [list(r) for r in rows]}


def eng(head, en, ko, tip=None):
    f = {"kind": "english", "head": head, "en": en, "ko": ko}
    if tip:
        f["tip"] = tip
    return f


def prof(when, *lines):
    return {"kind": "prof", "when": when, "lines": list(lines)}


G = [
    {"ko": "어텐션", "en": "Attention", "say": "필요한 곳을 골라 보는 장치. 점수를 매기고 가중 평균을 내요.",
     "more": "세 단계예요. 점수 매기기, 소프트맥스로 합이 1 인 가중치 만들기, 밸류를 가중합 하기(N4 p.21-24)."},
    {"ko": "셀프 어텐션", "en": "Self-Attention", "say": "한 문장이 자기 자신을 바라보는 어텐션이에요.",
     "more": "쿼리, 키, 밸류가 모두 같은 시퀀스에서 나와요. 2017년 트랜스포머의 핵심이에요(N4 p.33)."},
    {"ko": "크로스 어텐션", "en": "Cross-Attention", "say": "쿼리는 한 시퀀스에서, 키와 밸류는 다른 시퀀스에서 오는 어텐션이에요.",
     "more": "2015년 번역 어텐션이 이것이에요. 교수님은 이 노트북 Part 1 이 크로스 어텐션 개념이라고 했어요."},
    {"ko": "쿼리", "en": "Query", "say": "지금 내가 무엇을 찾는지를 담은 벡터, 곧 질문이에요.",
     "more": "코드의 query 예요. 쿼리가 바뀌면 어디를 볼지가 바뀌어요."},
    {"ko": "키", "en": "Key", "say": "나는 이런 정보를 갖고 있다고 광고하는 이름표 벡터예요.",
     "more": "쿼리와 키를 내적해서 점수를 만들어요. 사전의 색인 같은 역할이에요."},
    {"ko": "밸류", "en": "Value", "say": "내가 뽑히면 실제로 건네줄 내용 벡터예요.",
     "more": "가중합에 들어가는 것은 키가 아니라 밸류예요. 출력은 밸류들의 가중 평균이에요."},
    {"ko": "어텐션 점수", "en": "Attention Score", "say": "쿼리와 키가 얼마나 맞는지 나타낸 날것 숫자예요.",
     "more": "코드의 scores 예요. 합이 1 이 아니라서 그대로는 가중치로 못 써요."},
    {"ko": "어텐션 분포", "en": "Attention Distribution", "say": "점수를 소프트맥스에 넣어 합이 1 이 되게 만든 분포예요.",
     "more": "행마다 더하면 1 이에요. 그래서 '내 주의가 어디로 얼마나 가는지' 로 읽을 수 있어요."},
    {"ko": "어텐션 가중치", "en": "Attention Weight", "say": "어텐션 분포의 각 칸 값. 그 자리를 얼마나 볼지 정해요.",
     "more": "모두 0 이상이고 다 더하면 1 이에요. 코드의 weights, A 가 이것이에요."},
    {"ko": "가중합", "en": "Weighted Sum", "say": "값마다 가중치를 곱해서 모두 더한 것이에요.",
     "more": "가중치의 합이 1 이면 가중 평균이에요. 어텐션의 출력이 바로 밸류들의 가중합이에요."},
    {"ko": "소프트맥스", "en": "Softmax", "say": "점수를 모두 더해 1 이 되는 확률 파이로 나누는 함수예요.",
     "more": "각 점수에 exp 를 씌운 뒤 전체 합으로 나눠요. 점수가 크면 거의 한 곳만 보게 돼요."},
    {"ko": "내적", "en": "Dot Product", "say": "두 화살표가 얼마나 같은 쪽을 보는지 재는 곱셈이에요.",
     "more": "같은 자리끼리 곱해서 모두 더해요. 어텐션 점수의 가장 단순한 계산법이에요."},
    {"ko": "스케일드 닷프로덕트 어텐션", "en": "Scaled Dot-Product Attention", "say": "내적 점수를 키 차원의 제곱근으로 나눈 뒤 소프트맥스를 쓰는 어텐션이에요.",
     "more": "d_k 가 커지면 점수의 표준편차가 루트 d_k 만큼 커져서, 나눠 주지 않으면 소프트맥스가 포화돼요(N4 p.38)."},
    {"ko": "순열 등변성", "en": "Permutation Equivariance", "say": "입력 순서를 섞으면 출력도 똑같이 섞일 뿐, 값 자체는 그대로인 성질이에요.",
     "more": "셀프 어텐션의 첫 번째 장벽이에요. 순서가 계산 안에 없다는 뜻이라 위치 인코딩이 필요해요(N4 p.40)."},
    {"ko": "위치 인코딩", "en": "Positional Encoding", "say": "몇 번째 자리인지를 알려 주는 벡터를 토큰 벡터에 더해 주는 것이에요.",
     "more": "셀프 어텐션에는 순서 개념이 없어서, 순서를 입력 쪽에 넣어 줘요."},
    {"ko": "사인 코사인 위치 인코딩", "en": "Sinusoidal Positional Encoding", "say": "사인과 코사인 물결로 위치 벡터를 만드는 방식이에요.",
     "more": "2017년 원논문의 방식이에요. 차원마다 파장이 달라서 위치마다 무늬가 달라요. 학습할 파라미터가 없어요."},
    {"ko": "위치별 피드포워드 신경망", "en": "Position-wise Feed-Forward Network (FFN)", "say": "토큰마다 따로 적용하는 2층 신경망이에요.",
     "more": "여기서는 자리끼리 섞이지 않아요. 어텐션은 정보를 옮기고, 이 층이 정보를 바꿔요(N4 p.42)."},
    {"ko": "인과 마스킹", "en": "Causal Masking", "say": "미래 자리의 점수를 소프트맥스 전에 음의 무한대로 만들어 못 보게 막는 것이에요.",
     "more": "언어 모델이 정답을 미리 훔쳐보지 못하게 해요. 마스크는 반드시 소프트맥스 전에 걸어요(N4 p.43)."},
    {"ko": "자기회귀", "en": "Autoregressive", "say": "자기가 방금 만든 토큰을 다시 입력으로 넣어 다음 토큰을 만드는 방식이에요.",
     "more": "GPT 계열이 이 방식이에요. 그래서 인과 마스킹이 꼭 필요해요."},
    {"ko": "멀티 헤드 어텐션", "en": "Multi-Head Attention (MHA)", "say": "전체 차원을 h 조각으로 나눠 서로 다른 관점으로 동시에 보는 어텐션이에요.",
     "more": "교수님: 차원을 키우는 게 아니라 h 로 나눠서 보는 것이라 계산량은 똑같아요(N4 p.47-48)."},
    {"ko": "헤드", "en": "Head", "say": "어텐션을 한 번 보는 행위 하나예요.",
     "more": "교수님 비유로 합성곱의 필터 같아요. 어떤 헤드는 문법을, 어떤 헤드는 가까운 문맥을 봐요."},
    {"ko": "잔차 연결", "en": "Residual Connection", "say": "층의 입력을 층의 출력에 그대로 더해 주는 지름길이에요.",
     "more": "기울기가 곧장 앞층까지 흐르는 항등 경로가 생겨요. 깊게 쌓으려면 꼭 필요해요(N4 p.49)."},
    {"ko": "층 정규화", "en": "Layer Normalization (LayerNorm)", "say": "토큰 하나의 숫자들을 평균 0, 분산 1 로 고르게 만드는 것이에요.",
     "more": "토큰끼리도, 배치끼리도 섞지 않아요. 요즘 모델은 층 앞에 두는 Pre-LN 방식을 써요(N4 p.50-51)."},
    {"ko": "트랜스포머", "en": "Transformer", "say": "어텐션만으로 만든 요즘 언어 모델의 기본 블록이에요.",
     "more": "교수님: 트랜스포머를 좀 크게 쌓으면 그게 LLM 이에요. 이 실습에서 직접 조립해요."},
    {"ko": "병렬화", "en": "Parallelization", "say": "여러 계산을 한꺼번에 동시에 하기예요.",
     "more": "셀프 어텐션은 행렬 곱 한 번으로 모든 자리를 함께 계산해요. 교수님: 패러럴이 핵심이에요."},
    {"ko": "텐서", "en": "Tensor", "say": "PyTorch 와 NumPy 가 쓰는 숫자 배열(벡터, 행렬, 그 이상)이에요.",
     "more": "torch.randn(2, 7, 64) 는 2 x 7 x 64 텐서예요. .shape 로 모양을 봐요."},
    {"ko": "모양", "en": "Shape", "say": "텐서가 몇 줄 몇 칸인지 적은 튜플이에요. (5, 16) 처럼 써요.",
     "more": "노트북이 계속 shape 를 찍어요. 3주차 실습에서 배운 가장 쓸모 있는 디버깅 습관이에요."},
    {"ko": "기울기", "en": "Gradient", "say": "값을 조금 바꾸면 결과가 얼마나, 어느 쪽으로 바뀌는지 알려 주는 숫자예요.",
     "more": "기울기가 0 에 가까우면 그 층은 배우지 못해요. 포화된 소프트맥스가 그런 상태예요."},
    {"ko": "기울기 소실", "en": "Vanishing Gradient", "say": "기울기가 점점 희미해져 0 에 가까워지는 문제예요.",
     "more": "3주차 RNN 의 문제였어요. 포화된 소프트맥스도 같은 증상을 만들어요."},
    {"ko": "파라미터", "en": "Parameter", "say": "모델이 학습하면서 값을 고쳐 나가는 숫자들이에요.",
     "more": "가중치 행렬과 편향 항이 파라미터예요. 개수를 세면 모델의 크기를 알 수 있어요."},
    {"ko": "언어 모델", "en": "Language Model (LM)", "say": "앞 글을 보고 다음 토큰을 맞히는 모델이에요.",
     "more": "3주차에 배웠어요. 언어 모델은 미래를 보면 안 되니까 인과 마스킹이 필요해요."},
]

S = []


def page(p, title, terms, p1, p2=(), p3=(), p4=()):
    S.append({"p": p, "title": title, "terms": terms, "pass1": list(p1), "pass2": list(p2), "pass3": list(p3), "pass4": list(p4)})


# ---------------------------------------------------------------- p.1
page(1, "Lab 3 소개: 트랜스포머를 손으로 만들기",
     ["Attention", "Self-Attention", "Transformer", "Multi-Head Attention (MHA)"],
     [say("4주차 강의를 그대로 코드로 옮기는 실습이에요.",
          "**트랜스포머(Transformer)** 블록을 NumPy 로, 그다음 PyTorch 로 직접 만들어요."),
      pts("오늘의 여섯 부분",
          "Part 0: 환경 준비(약 2분)",
          "Part 1: NumPy 로 **어텐션(Attention)** 세 단계, 루트 d 로 나누는 까닭",
          "Part 2: **셀프 어텐션(Self-Attention)** 과 강의의 장벽 세 개를 숫자로",
          "Part 3: PyTorch 로 **멀티 헤드 어텐션(Multi-Head Attention)** 모듈 만들기",
          "Part 4: 미니 **트랜스포머(Transformer)** 블록을 학습시키고 어텐션 그림 보기",
          "Part 5: 실제 사전 학습 모델(DistilBERT)의 진짜 헤드 들여다보기")],
     [pts("노트북이 미리 알려 주는 것",
          "전부 Colab 무료 CPU 에서 돌아가요. GPU 가 필요 없어요.",
          "Part 4 에서 학습하는 모델은 **파라미터(Parameter)** 약 5만 개, 학습 약 2초예요.",
          "Part 5 에서 250MB 짜리 모델을 한 번 내려받아요.",
          "셀을 순서대로 실행하세요. 앞서 나가면 값이 어긋나요."),
      say("주문: 글을 토큰으로 자르고, 토큰을 벡터로 바꾸고, 벡터로 다음 토큰을 맞혀요.",
          "오늘은 '벡터를 서로 섞는 방법' 을 **어텐션(Attention)** 으로 바꿔요.")],
     [prof("4주차 3교시 수업",
           "교수님: 20분밖에 안 남아서 오늘 실습은 건너뛰겠습니다.",
           "풀 코드를 아웃풋까지 찍어서 올려놨으니 복습으로 돌려 보세요.",
           "최대한 이 셀만 읽어도 이해할 수 있게 굉장히 친절하게 적어 놨습니다."),
      prof("4주차 3교시 수업",
           "교수님이 말한 파트 구성이에요.",
           "Part 1 은 2장에서 배운 **크로스 어텐션(Cross-Attention)** 개념, Part 2 는 **셀프 어텐션(Self-Attention)**,",
           "Part 3 은 PyTorch 의 셀프 어텐션과 우리가 직접 만든 것의 차이,",
           "Part 4 는 **트랜스포머(Transformer)** 블록, Part 5 는 층별 **헤드(Head)** 분석이에요.")],
     [check("교수님이 Lab 3 을 수업에서 건너뛴 까닭은?",
            ["시간이 20분밖에 남지 않아서", "코드에 오류가 있어서", "시험 범위가 아니라서", "GPU 가 없어서"], 0,
            "프로젝트 안내 뒤 20분이 남아서, 출력까지 찍힌 풀 코드를 올려 두고 복습하라고 했어요."),
      check("이 노트북 Part 1 이 다루는 개념은?",
            ["**크로스 어텐션(Cross-Attention)**", "**층 정규화(LayerNorm)**", "빔 서치", "토큰화"], 0,
            "교수님 말: Part 1 은 어텐션 2장에서 배운 크로스 어텐션 개념이에요.")])

# ---------------------------------------------------------------- p.2
page(2, "Part 0 환경 준비: 도구 부르기와 씨앗 심기",
     ["Tensor", "Parallelization", "Shape"],
     [say("쓸 도구를 불러오고, 무작위 숫자가 매번 같게 나오도록 씨앗을 심어요.",
          "오늘은 GPU 가 필요 없어요. 모델이 작아서 CPU 가 오히려 빠를 때도 있어요.")],
     [py("import ... as ...",
         ["`import numpy as np` 는 NumPy 를 np 라는 짧은 이름으로 불러와요.",
          "`import torch.nn as nn` 은 신경망 부품 묶음이에요.",
          "`import torch.nn.functional as F` 는 함수 모양의 부품 묶음이에요."],
         "import numpy as np\nprint(np.array([1, 2, 3]).sum())", "6"),
      py("manual_seed 와 seed",
         ["`torch.manual_seed(0)` 은 무작위 숫자의 시작점을 0 으로 고정해요.",
          "씨앗을 같게 심으면 몇 번을 돌려도 같은 무작위 숫자가 나와요.",
          "그래서 여러분 화면의 값과 저장된 출력이 같아요."],
         "import torch\ntorch.manual_seed(0)\nprint(torch.randn(1).shape)", "torch.Size([1])"),
      py("set_num_threads",
         ["`torch.set_num_threads(2)` 는 CPU 코어를 2개만 쓰라는 뜻이에요.",
          "Colab 무료 등급이 코어를 2개쯤 주기 때문이에요. **병렬화(Parallelization)** 와 이어지는 설정이에요."],
         "torch.set_num_threads(2)")],
     [code(3, "도구와 씨앗",
           [(1, 6, "수학(math), 시간(time), NumPy, PyTorch, 신경망 부품(nn), 함수 부품(F), 그림(plt)을 불러와요."),
            (8, 9, "PyTorch 와 NumPy 의 무작위 씨앗을 둘 다 0 으로 고정해요."),
            (10, 10, "CPU 코어를 2개만 쓰게 정해요. 주석처럼 Colab 무료 등급이 약 2코어를 줘요."),
            (12, 14, "NumPy 와 PyTorch 의 버전, 그리고 장치가 cpu 라는 것을 출력해요.")],
           link="강의 N4 p.59 Lab 3 안내"),
      outpts(3)],
     [check("씨앗(manual_seed)을 고정하는 까닭은?",
            ["돌릴 때마다 같은 무작위 숫자가 나오게 하려고", "속도를 올리려고", "GPU 를 쓰려고", "**모양(Shape)** 을 맞추려고"], 0,
            "씨앗이 같으면 무작위 **텐서(Tensor)** 도 같아서, 저장된 출력과 내 화면이 같아져요."),
      warn("헷갈리는 점",
           "버전 숫자(numpy 2.1.3, torch 2.11.0)는 여러분 환경에 따라 달라요.",
           "셀을 순서대로 돌리지 않으면 씨앗이 어긋나서 뒤 숫자가 달라져요.")])

# ---------------------------------------------------------------- p.3
page(3, "1.1 어텐션의 전부는 세 줄",
     ["Attention", "Query", "Key", "Value", "Softmax", "Weighted Sum", "Attention Score", "Cross-Attention"],
     [say("**어텐션(Attention)** 은 딱 세 단계예요.",
          "점수 매기기 → **소프트맥스(Softmax)** → **가중합(Weighted Sum)**.",
          "강의 N4 p.21-23 의 세 단계 그대로예요."),
      ana("어텐션은 부드러운 사전 찾기",
          "파이썬 사전은 키 하나가 딱 맞아야 값을 줘요. 어텐션은 모든 키와 조금씩 맞고, 값들을 섞어서 줘요.",
          [("사전의 찾는 말", "**쿼리(Query)**"), ("사전의 표제어", "**키(Key)**"),
           ("표제어의 뜻풀이", "**밸류(Value)**"), ("섞어서 내놓기", "**가중합(Weighted Sum)**")])],
     [pts("영어 제목과 문장의 뜻",
          "**The whole idea in three lines** = 핵심 생각은 세 줄이면 끝이에요.",
          "**score → softmax → weighted sum** = 점수 → 소프트맥스 → 가중합.",
          "**A query asks a question** = **쿼리(Query)** 가 질문을 던져요.",
          "**Every key advertises what it has** = 각 **키(Key)** 가 자기를 광고해요.",
          "**nothing is hidden** = 숨겨진 장치는 하나도 없어요."),
      cmp("세 벡터의 역할", ["이름", "하는 일"],
          [["**쿼리(Query)**", "지금 내가 무엇을 찾는지"],
           ["**키(Key)**", "나는 이런 걸 갖고 있다는 이름표"],
           ["**밸류(Value)**", "뽑히면 실제로 건네줄 내용"]]),
      pts("이 셀이 노리는 것",
          "**쿼리(Query)** 를 2번 **키(Key)** 와 거의 같게 만들어 둬요.",
          "그러면 출력이 2번 **밸류(Value)** 와 거의 같게 나와야 해요.",
          "여기서는 키와 밸류를 우리가 그냥 줬어요. 그래서 **크로스 어텐션(Cross-Attention)** 쪽 그림이에요.")],
     [prof("4주차 2교시 수업",
           "교수님: 스코어를 계산하고, 노멀라이즈 해서 웨이트를 만들고,",
           "웨이티드 썸으로 컨텍스트 벡터를 만들고, 그걸로 예측을 합니다.",
           "이 네 단계가 **어텐션(Attention)** 에 가장 중요한 겁니다."),
      pts("강의와 짝",
          "N4 p.20 Soft Dictionary Lookup 이 이 쪽의 비유예요.",
          "N4 p.21 Step 1 이 **어텐션 점수(Attention Score)** 구하기,",
          "N4 p.22 Step 2 가 **소프트맥스(Softmax)**, N4 p.23 Step 3 이 **가중합(Weighted Sum)** 이에요.")],
     [check("어텐션의 출력은 무엇들의 가중 평균인가요?",
            ["**밸류(Value)** 들", "**키(Key)** 들", "**쿼리(Query)** 들", "**어텐션 점수(Attention Score)** 들"], 0,
            "점수는 **키(Key)** 로 매기지만, 실제로 섞어서 내놓는 것은 **밸류(Value)** 예요.")])

# ---------------------------------------------------------------- p.4
page(4, "어텐션 세 줄을 NumPy 로 직접",
     ["Softmax", "Attention Score", "Attention Weight", "Weighted Sum", "Dot Product", "Query", "Key", "Value", "Attention"],
     [say("**어텐션(Attention)** 을 파이썬 세 줄로 씁니다.",
          "점수 → **소프트맥스(Softmax)** → **가중합(Weighted Sum)**, 정말 이게 전부예요.")],
     [py("def 로 함수 만들기",
         ["`def softmax(x, axis=-1):` 는 softmax 라는 함수를 정의해요.",
          "`axis=-1` 은 기본값이에요. 안 적으면 마지막 축을 뜻해요.",
          "`return` 이 결과를 돌려줘요."],
         "def twice(x):\n    return x * 2\nprint(twice(5))", "10"),
      py("np.array",
         ["`np.array([[1., 0.], [0., 1.]])` 는 2행 2열 숫자 표를 만들어요.",
          "숫자 뒤의 점(1.)은 정수가 아니라 소수라는 표시예요."],
         "import numpy as np\nprint(np.array([[1., 0.], [0., 1.]]).shape)", "(2, 2)"),
      py("행렬 곱 기호 @",
         ["`keys @ query` 는 행렬 곱이에요. 각 행과 **쿼리(Query)** 의 **내적(Dot Product)** 을 한 번에 구해요.",
          "(4, 3) @ (3,) 은 (4,) 가 돼요. 키가 4개니까 점수도 4개예요."],
         "print(np.array([[1., 0.], [0., 1.]]) @ np.array([3., 5.]))", "[3. 5.]"),
      py("axis 와 keepdims",
         ["`x.max(axis=-1, keepdims=True)` 는 마지막 축에서 최댓값을 찾고 칸 모양을 유지해요.",
          "가장 큰 값을 먼저 빼 주면 exp 가 너무 커져서 넘치는 일을 막아요. 결과는 똑같아요."],
         "import numpy as np\nx = np.array([1., 2., 3.])\nprint(np.exp(x - x.max()).round(3))", "[0.135 0.368 1.   ]")],
     [formula("어텐션 세 단계",
              r"s = K q,\qquad \alpha = \mathrm{softmax}(s),\qquad o = \alpha^\top V",
              [(r"K q", "각 키와 쿼리의 내적, 곧 어텐션 점수 s"),
               (r"\mathrm{softmax}(s)", "합이 1 인 어텐션 가중치 알파"),
               (r"\alpha^\top V", "밸류들의 가중합, 곧 출력 o")],
              "강의 N4 p.24 의 네 식 중 앞 세 줄이 이 코드의 18, 19, 20번 줄이에요."),
      code(5, "네 칸짜리 기억 장치에서 하나 꺼내 오기",
           [(1, 4, "안전한 **소프트맥스(Softmax)** 함수예요. 최댓값을 빼고 exp 를 씌운 뒤 전체 합으로 나눠요."),
            (6, 10, "**키(Key)** 4개예요. 주석처럼 각 칸이 '나는 이런 걸 갖고 있다' 고 광고해요."),
            (11, 14, "**밸류(Value)** 4개예요. 뽑히면 실제로 건네줄 내용이고 2칸짜리예요."),
            (16, 16, "**쿼리(Query)** 예요. 주석처럼 대부분 2번 키 쪽을 향해요."),
            (18, 18, "(1) 점수: 각 키와 쿼리의 **내적(Dot Product)** 을 구해요. 4개 숫자가 나와요."),
            (19, 19, "(2) **소프트맥스(Softmax)**: 점수를 합이 1 인 **어텐션 가중치(Attention Weight)** 로 바꿔요."),
            (20, 20, "(3) 섞기: 가중치로 **밸류(Value)** 들의 **가중합(Weighted Sum)** 을 내요."),
            (22, 25, "점수, 가중치와 그 합, 출력, 그리고 2번 밸류를 나란히 출력해요.")],
           link="강의 N4 p.21-24 어텐션 세 단계와 네 식"),
      outpts(5),
      steps("점수와 가중치를 손으로",
            ["키 0 은 [1, 0, 0] 이라 쿼리 [0.5, 0, 3] 과의 내적은 0.5 예요.",
             "키 1 은 [0, 1, 0] 이라 0, 키 2 는 [0, 0, 1] 이라 3, 키 3 은 [-1, 0, 0] 이라 -0.5 예요.",
             "exp 를 씌우면 2번 칸만 크게 남아요. 나눠 주면 0.861 이 2번 칸에 몰려요.",
             "출력 = 0.071x10 + 0.043x0 + 0.861x5 + 0.026x(-9) = 4.78 (첫 칸)"],
            "출력 [4.78, 4.50] 은 2번 **밸류(Value)** [5, 5] 와 거의 같아요. 예상대로예요."),
      pts("읽는 요령",
          "`sum = 1.0` 은 **소프트맥스(Softmax)** 가 제대로 확률을 만들었다는 확인이에요.",
          "쿼리가 키 2 를 가장 닮았으니 밸류 2 가 거의 그대로 나온 거예요.")],
     [check("**어텐션 가중치(Attention Weight)** 가 [0.071, 0.043, 0.861, 0.026] 일 때, 출력에 가장 크게 기여하는 것은?",
            ["2번 **밸류(Value)**", "0번 **밸류(Value)**", "2번 **키(Key)**", "**쿼리(Query)**"], 0,
            "가중치 0.861 이 2번 자리에 몰려 있고, 곱해지는 것은 키가 아니라 밸류예요."),
      warn("흔한 실수",
           "점수 계산에는 **키(Key)** 를 쓰고, 가중합에는 **밸류(Value)** 를 써요. 둘을 바꾸면 안 돼요.",
           "**소프트맥스(Softmax)** 에서 최댓값을 빼는 것은 값을 바꾸는 게 아니라 넘침을 막는 요령이에요.")])

# ---------------------------------------------------------------- p.5
page(5, "1.2 날카로운 가중치와 평평한 가중치",
     ["Softmax", "Attention Weight", "Attention Distribution", "Attention Score"],
     [say("같은 세 줄인데, 점수의 크기에 따라 결과가 크게 달라져요.",
          "점수가 크면 거의 한 곳만 보고, 작으면 골고루 봐요."),
      ana("가중치의 모양",
          "손전등 같아요. 좁게 비추면 한 곳만 환하고, 넓게 비추면 온 방이 어스름해요.",
          [("좁은 손전등", "날카로운 **어텐션 분포(Attention Distribution)**"),
           ("넓은 손전등", "평평한 **어텐션 분포(Attention Distribution)**"),
           ("빛의 세기 조절", "**어텐션 점수(Attention Score)** 의 크기")])],
     [pts("영어 문장의 뜻",
          "**Sharp weights vs flat weights** = 날카로운 가중치 대 평평한 가중치.",
          "**Large scores → an almost one-hot distribution** = 점수가 크면 한 칸만 1 에 가까워요.",
          "**Small scores → an almost uniform distribution** = 점수가 작으면 거의 고르게 나뉘어요.",
          "**it is exactly why the Transformer divides by root d** = 루트 d 로 나누는 이유가 바로 이것이에요."),
      py("for ... in (a, b, c)",
         ["괄호로 묶은 값들을 하나씩 꺼내 같은 일을 되풀이해요.",
          "`for scale in (0.2, 1.0, 6.0):` 은 0.2, 1.0, 6.0 에 대해 차례로 돌아요."],
         "for s in (1, 2, 3):\n    print(s * 10)", "10\n20\n30"),
      py("f-string 의 칸 맞추기",
         ["`f\"{scale:>4}\"` 는 오른쪽 정렬로 4칸을 써요.",
          "`f\"{w.max():.3f}\"` 는 소수 셋째 자리까지만 보여 줘요.",
          "표처럼 줄을 맞추려고 쓰는 문법이에요."],
         "x = 0.38123\nprint(f\"{x:.3f}\")", "0.381")],
     [code(7, "같은 점수에 배율만 바꿔 보기",
           [(1, 1, "여섯 칸짜리 기본 점수를 만들어요. 가장 큰 값이 2.0 이에요."),
            (3, 3, "배율 0.2, 1.0, 6.0 을 차례로 넣어 봐요."),
            (4, 4, "점수 전체에 배율을 곱한 뒤 **소프트맥스(Softmax)** 를 걸어요."),
            (5, 5, "배율, 가장 큰 **어텐션 가중치(Attention Weight)**, 여섯 칸 전부를 한 줄로 출력해요.")],
           link="강의 N4 p.19 Sharp weights = look here, Flat weights = everything matters"),
      outpts(7),
      steps("숫자로 확인",
            ["배율 0.2 면 점수가 [0.4, 0.28, ...] 로 작아요. 가장 큰 칸도 0.202 뿐이에요.",
             "배율 1.0 이면 가장 큰 칸이 0.381 이에요. 적당히 한 곳을 가리켜요.",
             "배율 6.0 이면 점수가 [12, 8.4, ...] 로 커요. 가장 큰 칸이 0.970 이에요.",
             "여섯 칸이 모두 같다면 1/6 = 0.167 이었을 거예요."],
            "점수의 크기만 바꿨는데 **어텐션 분포(Attention Distribution)** 가 평평 → 날카로움으로 변해요.")],
     [check("배율 6.0 에서 가장 큰 **어텐션 가중치(Attention Weight)** 가 0.970 이라는 뜻은?",
            ["나머지 다섯 칸을 사실상 안 본다는 뜻", "점수가 확률이라는 뜻", "**소프트맥스(Softmax)** 가 틀렸다는 뜻", "가중치 합이 6 이라는 뜻"], 0,
            "한 칸에 97% 가 몰리면 다른 칸의 **밸류(Value)** 는 거의 반영되지 않아요."),
      warn("헷갈리는 점",
           "점수의 순서는 세 경우 모두 같아요. 달라진 것은 크기뿐이에요.",
           "날카로운 게 늘 좋은 것도, 평평한 게 늘 나쁜 것도 아니에요. 모델이 골라 배워요.")])

# ---------------------------------------------------------------- p.6
page(6, "1.3 왜 루트 d 로 나누나: 직접 재 보기",
     ["Dot Product", "Scaled Dot-Product Attention", "Attention Score", "Softmax"],
     [say("강의는 **내적(Dot Product)** 의 분산이 d_k 라고 했어요.",
          "그러면 표준편차는 루트 d_k 만큼 커져요. 믿지 말고 재 봐요.")],
     [pts("영어 문장의 뜻",
          "**Why divide by root d ?** = 왜 루트 d 로 나누나요?",
          "**Var(q dot k) = d_k** = 내적의 흩어진 정도가 차원 수만큼 커져요.",
          "**the scores are routinely plus or minus 20** = d_k 가 512 면 점수가 보통 20 안팎까지 커져요.",
          "**Let us measure it instead of trusting the formula** = 식을 믿지 말고 직접 재 봅시다."),
      py("np.random.default_rng",
         ["`rng = np.random.default_rng(0)` 은 씨앗 0 짜리 난수 생성기를 만들어요.",
          "`rng.normal(size=(20000, d))` 은 평균 0, 표준편차 1 인 숫자를 그 **모양(Shape)** 대로 뽑아요."],
         "import numpy as np\nrng = np.random.default_rng(0)\nprint(rng.normal(size=(2, 3)).shape)", "(2, 3)"),
      py("(q * k).sum(axis=1) 과 .std()",
         ["`q * k` 는 같은 자리끼리 곱해요. 거기에 `.sum(axis=1)` 로 한 줄씩 더하면 **내적(Dot Product)** 이에요.",
          "`.std()` 는 표준편차, 곧 숫자들이 평균에서 얼마나 흩어졌는지예요."],
         "import numpy as np\nq = np.array([[1., 2.]])\nk = np.array([[3., 4.]])\nprint((q * k).sum(axis=1))", "[11.]")],
     [formula("내적의 흩어짐",
              r"\mathrm{Var}(q\cdot k)=d_k \;\Rightarrow\; \mathrm{sd}(q\cdot k)=\sqrt{d_k}",
              [(r"q\cdot k", "두 벡터의 내적, 곧 어텐션 점수"),
               (r"d_k", "키 벡터의 칸 수(차원)"),
               (r"\sqrt{d_k}", "점수의 표준편차. 차원이 커지면 점수도 커져요")],
              "그래서 점수를 루트 d_k 로 나누면 흩어짐이 다시 1 로 돌아와요. 이것이 **스케일드 닷프로덕트 어텐션(Scaled Dot-Product Attention)** 이에요."),
      code(9, "차원을 키우며 점수의 표준편차 재기",
           [(1, 1, "씨앗 0 짜리 난수 생성기를 만들어요."),
            (3, 3, "표의 머리글을 출력해요. d_k, 잰 표준편차, 루트 d_k 세 칸이에요."),
            (4, 4, "차원 8, 64, 512 를 차례로 시험해요."),
            (5, 6, "각 차원마다 **쿼리(Query)** 20000개, **키(Key)** 20000개를 무작위로 뽑아요."),
            (7, 7, "같은 자리끼리 곱해 더해서 20000개의 **내적(Dot Product)** 을 구해요."),
            (8, 8, "잰 표준편차와 루트 d_k 를 나란히 출력해요.")],
           link="강의 N4 p.38 Why the Scaled Dot Product"),
      outpts(9),
      steps("표가 말해 주는 것",
            ["d_k = 8 일 때 잰 값 2.86, 루트 8 = 2.83",
             "d_k = 64 일 때 잰 값 8.02, 루트 64 = 8.00",
             "d_k = 512 일 때 잰 값 22.57, 루트 512 = 22.63",
             "세 줄 모두 두 숫자가 거의 같아요."],
            "강의의 식이 맞았어요. 차원이 512 면 **어텐션 점수(Attention Score)** 가 보통 20 을 넘나들어요.")],
     [check("d_k = 512 에서 점수의 표준편차가 약 22.6 이면 무슨 일이 생기나요?",
            ["**소프트맥스(Softmax)** 가 거의 한 칸만 보게 포화돼요", "점수가 0 이 돼요",
             "**키(Key)** 가 사라져요", "계산이 느려져요"], 0,
            "앞 쪽에서 본 배율 6.0 과 같은 상황이에요. 그래서 루트 d_k 로 나눠 줘요."),
      warn("헷갈리는 점",
           "나누는 값은 루트 d_k 이지 d_k 가 아니에요. 분산이 d_k 라서 표준편차는 루트 d_k 예요.",
           "잰 값과 루트 값이 소수점 둘째 자리에서 조금 다른 것은 무작위 표본이라 그래요.")])

# ---------------------------------------------------------------- p.7
page(7, "포화된 소프트맥스는 기울기를 잃어요",
     ["Softmax", "Gradient", "Vanishing Gradient", "Scaled Dot-Product Attention", "Attention Weight"],
     [say("점수가 너무 크면 **소프트맥스(Softmax)** 가 포화돼요.",
          "포화되면 **기울기(Gradient)** 가 거의 사라져서, 그 층은 배우지 못해요.")],
     [pts("영어 문장의 뜻",
          "**its gradient almost disappears** = 기울기가 거의 사라져요.",
          "**A layer that cannot pass a gradient cannot learn** = 기울기를 못 흘리는 층은 학습이 안 돼요.",
          "**the saturated softmax passes ~8x less gradient** = 포화된 소프트맥스는 기울기를 약 8분의 1 만 흘려요.",
          "3주차 RNN 의 **기울기 소실(Vanishing Gradient)** 과 원인은 다르지만 증상은 같아요."),
      py("requires_grad_() 와 backward()",
         ["`z.requires_grad_(True)` 는 '이 값에 대한 **기울기(Gradient)** 를 기록해 줘' 라는 표시예요.",
          "결과에 `.backward()` 를 부르면 거꾸로 따라가며 계산하고 `z.grad` 에 기울기를 넣어요.",
          "3주차 실습에서 배운 자동 미분이에요."],
         "import torch\nz = torch.tensor([2.0], requires_grad=True)\n(z * z).sum().backward()\nprint(z.grad)", "tensor([4.])"),
      py(".softmax(-1) 과 .item()",
         ["`z.softmax(-1)` 은 마지막 축에 **소프트맥스(Softmax)** 를 걸어요.",
          "`.item()` 은 숫자 하나짜리 **텐서(Tensor)** 에서 파이썬 숫자를 꺼내요.",
          "`.abs().max()` 는 절댓값 중 가장 큰 것이에요."],
         "import torch\nprint(torch.tensor([-3.0]).abs().max().item())", "3.0")],
     [code(11, "배율 1 과 배율 6 의 기울기 비교",
           [(1, 2, "배율 1.0 과 6.0 을 차례로 넣고, 앞에서 쓴 여섯 칸 점수에 배율을 곱해요."),
            (3, 3, "이 **텐서(Tensor)** 의 **기울기(Gradient)** 를 기록하라고 표시해요."),
            (4, 4, "**소프트맥스(Softmax)** 를 걸어 **어텐션 가중치(Attention Weight)** 를 만들어요."),
            (5, 5, "가장 큰 가중치 하나에 대해 거꾸로 미분해요. 주석처럼 '그 칸이 얼마나 움직일 수 있나' 를 재요."),
            (6, 7, "배율, 가장 큰 가중치, 기울기 절댓값의 최댓값을 한 줄로 출력해요."),
            (9, 10, "포화된 소프트맥스는 기울기를 약 8분의 1 만 흘린다고, 루트 d_k 가 그래서 필요하다고 알려 줘요.")],
           link="강의 N4 p.38 a saturated softmax has almost no gradient"),
      outpts(11),
      steps("두 숫자를 나눠 보기",
            ["배율 1.0: 가장 큰 가중치 0.3811, 기울기 0.2359",
             "배율 6.0: 가장 큰 가중치 0.9702, 기울기 0.02891",
             "0.2359 나누기 0.02891 은 약 8.2 예요."],
            "포화되면 기울기가 약 8분의 1 로 줄어요. 3주차의 **기울기 소실(Vanishing Gradient)** 과 같은 증상이에요."),
      prof("4주차 2교시 수업",
           "교수님: 소프트맥스 안에 들어가는 닷 프로덕트 값이 너무 커지면",
           "큰 값에 너무 몰리게 돼서 굉장히 뾰족한 분포가 만들어집니다.",
           "그래서 루트 d_k 로 스케일링 해 준다고 보면 됩니다.")],
     [check("**스케일드 닷프로덕트 어텐션(Scaled Dot-Product Attention)** 에서 루트 d_k 로 나누지 않으면?",
            ["**소프트맥스(Softmax)** 가 포화돼 **기울기(Gradient)** 가 거의 안 흘러요", "점수가 음수가 돼요",
             "**밸류(Value)** 가 사라져요", "메모리를 더 써요"], 0,
            "포화 → 기울기 약 8분의 1 → 학습이 안 돼요. 시험에 나오기 좋은 한 줄이에요."),
      warn("헷갈리는 점",
           "루트 d_k 는 장식이 아니라 학습을 살리는 장치예요.",
           "0.02891 은 0.2359 보다 한 자리 작아요. e 뒤 숫자(e-01, e-02)를 꼭 보세요.")])

# ---------------------------------------------------------------- p.8
page(8, "Part 2 셀프 어텐션: 한 문장에서 Q, K, V 를 만들기",
     ["Self-Attention", "Query", "Key", "Value", "Attention Weight", "Scaled Dot-Product Attention", "Parallelization", "Shape", "Cross-Attention"],
     [say("Part 1 에서는 **키(Key)** 와 **밸류(Value)** 를 우리가 그냥 줬어요.",
          "**셀프 어텐션(Self-Attention)** 에서는 토큰 스스로 세 가지를 만들어요."),
      ana("한 사람이 세 역할",
          "회의에서 한 사람이 질문도 하고, 명찰도 달고, 자료도 건네요. 역할만 셋이지 사람은 하나예요.",
          [("질문", "**쿼리(Query)**"), ("명찰", "**키(Key)**"),
           ("건네는 자료", "**밸류(Value)**"), ("같은 사람", "같은 토큰 벡터 x")])],
     [pts("영어 문장의 뜻",
          "**Q, K, V from one sequence** = 세 가지가 모두 같은 문장에서 나와요.",
          "**every token produces its own query, key and value** = 토큰마다 자기 쿼리, 키, 밸류를 내놔요.",
          "**through three learned linear maps** = 학습되는 행렬 세 개를 곱해서 만들어요."),
      cmp("둘의 차이", ["이름", "쿼리는 어디서", "키와 밸류는 어디서"],
          [["**크로스 어텐션(Cross-Attention)**", "디코더 쪽", "인코더 쪽(다른 시퀀스)"],
           ["**셀프 어텐션(Self-Attention)**", "같은 시퀀스", "같은 시퀀스"]]),
      py("함수의 기본값과 None",
         ["`def self_attention(X, Wq, Wk, Wv, mask=None):` 에서 mask 는 안 주면 None 이에요.",
          "`if mask is not None:` 은 '마스크를 줬을 때만' 이라는 뜻이에요."],
         "def f(a, b=None):\n    return a if b is None else a + b\nprint(f(1), f(1, 2))", "1 3"),
      py(".T 와 np.where",
         ["`K.T` 는 행과 열을 뒤집은 전치예요. (5, 16) 이 (16, 5) 가 돼요.",
          "`np.where(mask, a, b)` 는 mask 가 참인 자리는 a, 거짓인 자리는 b 를 골라요."],
         "import numpy as np\nprint(np.array([[1., 2.]]).T.shape)", "(2, 1)"),
      py("여러 값 한 번에 대입",
         ["`Q, K, V = X @ Wq, X @ Wk, X @ Wv` 는 세 계산을 한 줄에 써요.",
          "`return A @ V, A` 처럼 두 값을 함께 돌려줄 수도 있어요."],
         "a, b = 1 + 1, 2 * 3\nprint(a, b)", "2 6")],
     [formula("셀프 어텐션의 식",
              r"\mathrm{Attention}(Q,K,V)=\mathrm{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V",
              [(r"Q", "쿼리를 모두 쌓은 행렬. 행 하나가 토큰 하나의 질문"),
               (r"K^\top", "키 행렬을 눕힌 것. 모든 쿼리와 모든 키를 한 번에 비교해요"),
               (r"\sqrt{d_k}", "점수가 커지는 것을 되돌리는 나눗셈"),
               (r"V", "뽑힌 만큼 건네줄 밸류 행렬")],
              "강의 N4 p.36-37 의 식 그대로예요. 반복문이 없어서 **병렬화(Parallelization)** 가 잘 돼요."),
      code(13, "다섯 토큰짜리 문장으로 셀프 어텐션",
           [(1, 2, "토큰 5개, 차원 16 으로 정하고, 무작위 숫자로 '문장' X 를 만들어요."),
            (4, 6, "학습될 행렬 세 개 Wq, Wk, Wv 를 만들어요. 0.3 을 곱해 값을 작게 해 둬요."),
            (8, 8, "**셀프 어텐션(Self-Attention)** 함수를 정의해요. mask 는 안 주면 없는 것으로 쳐요."),
            (9, 9, "같은 X 에 세 행렬을 곱해 **쿼리(Query)**, **키(Key)**, **밸류(Value)** 를 만들어요."),
            (10, 10, "모든 쿼리와 모든 키를 비교하고 루트 d_k 로 나눠요. 주석처럼 (n, n) 크기예요."),
            (11, 12, "마스크를 줬으면 볼 수 없는 자리의 점수를 음의 무한대로 바꿔요."),
            (13, 13, "**소프트맥스(Softmax)** 로 행마다 합이 1 인 **어텐션 가중치(Attention Weight)** 를 만들어요."),
            (14, 14, "가중치로 밸류를 섞은 출력과 가중치 행렬 둘 다 돌려줘요."),
            (16, 16, "함수를 불러 out 과 A 를 받아요."),
            (18, 20, "X, A, out 의 **모양(Shape)** 을 출력해요. 주석에 뜻이 적혀 있어요."),
            (21, 23, "어텐션 행렬을 소수 둘째 자리로 찍고, 행 합이 정말 1 인지 확인해요.")],
           link="강의 N4 p.34-37 Queries, Keys and Values, 그리고 행렬 형태"),
      outpts(13, maxn=4, head="저장된 출력 1: 모양"),
      outpts(13, lo=4, maxn=7, head="저장된 출력 2: 어텐션 행렬과 행 합"),
      prof("4주차 2교시 수업",
           "교수님: 쿼리, 키, 밸류 이 3개의 컨셉을 이해해야",
           "뒤에 트랜스포머를 이해할 수 있고 자연어 처리를 이해할 수 있습니다.",
           "그리고 셀프 어텐션의 가장 큰 장점은 **병렬화(Parallelization)**, 패러럴이 핵심이에요.")],
     [check("A 의 **모양(Shape)** 이 (5, 5) 인 까닭은?",
            ["토큰 5개가 서로 서로를 다 보기 때문", "차원이 5 라서", "**밸류(Value)** 가 5칸이라서", "무작위라서"], 0,
            "행 i 는 '토큰 i 가 어디를 보는지' 예요. 토큰이 n 개면 어텐션 행렬은 n x n 이에요."),
      warn("헷갈리는 점",
           "Wq, Wk, Wv 는 자리마다 다른 게 아니라 모든 자리가 같은 행렬을 나눠 써요.",
           "출력 out 의 모양은 입력 X 와 같은 (5, 16) 이에요. 모양이 유지돼야 블록을 쌓을 수 있어요.")])

# ---------------------------------------------------------------- p.9
page(9, "2.1 장벽 1: 셀프 어텐션은 순서를 몰라요",
     ["Permutation Equivariance", "Self-Attention", "Positional Encoding", "Attention"],
     [say("강의는 **셀프 어텐션(Self-Attention)** 이 **순열 등변성(Permutation Equivariance)** 을 갖는다고 했어요.",
          "입력을 섞으면 출력도 똑같이 섞일 뿐이에요. 정말 그런지 숫자로 확인해요.")],
     [pts("영어 문장의 뜻",
          "**self-attention does not know about order** = 셀프 어텐션은 순서를 몰라요.",
          "**shuffle the input and the output just shuffles the same way** = 입력을 섞으면 출력도 같은 식으로 섞여요.",
          "**dog bites man and man bites dog** = 개가 사람을 문다와 사람이 개를 문다.",
          "**Order is simply not in the mechanism** = 순서는 계산 장치 안에 아예 없어요."),
      py("배열로 골라 뽑기",
         ["`perm = np.array([2, 0, 4, 1, 3])` 처럼 번호 배열을 만들고 `X[perm]` 으로 행 순서를 바꿔요.",
          "2번 행이 맨 앞, 0번 행이 그다음, 이런 식이에요."],
         "import numpy as np\nX = np.array([10., 20., 30.])\nprint(X[np.array([2, 0, 1])])", "[30. 10. 20.]"),
      py("받지 않을 값은 밑줄",
         ["`out_shuffled_input, _ = self_attention(...)` 의 밑줄은 '이 값은 안 쓸게요' 라는 뜻이에요.",
          "함수가 두 값을 돌려주는데 하나만 필요할 때 써요."],
         "a, _ = (1, 2)\nprint(a)", "1")],
     [formula("순열 등변성",
              r"\mathrm{SA}(PX)=P\,\mathrm{SA}(X)",
              [(r"P", "순서를 섞는 조작(퍼뮤테이션)"),
               (r"\mathrm{SA}(PX)", "섞고 나서 셀프 어텐션 하기"),
               (r"P\,\mathrm{SA}(X)", "셀프 어텐션 하고 나서 섞기")],
              "두 결과가 같다는 것이 **순열 등변성(Permutation Equivariance)** 이에요. 강의 N4 p.40 의 그 식이에요."),
      code(15, "섞고 나서와 섞기 전, 두 결과 비교",
           [(1, 1, "다섯 자리를 섞는 순서표를 만들어요."),
            (3, 3, "섞은 입력으로 **셀프 어텐션(Self-Attention)** 을 해요. 주석의 SA(PX) 예요."),
            (4, 4, "앞에서 구한 출력을 같은 순서로 섞어요. 주석의 P x SA(X) 예요."),
            (6, 6, "두 결과의 차이를 절댓값으로 재서 가장 큰 값을 구해요."),
            (7, 7, "그 값을 지수 표기로 출력해요. 주석처럼 소수 오차 수준의 0 이에요."),
            (8, 9, "순서는 장치 안에 없고, 고치는 방법은 입력에 **위치 인코딩(Positional Encoding)** 을 더하는 것이라고 알려 줘요.")],
           link="강의 N4 p.40 Barrier 1 - Positional Encoding"),
      outpts(15),
      prof("4주차 2교시 수업",
           "교수님: 셀프 어텐션에는 부족한 정보와 배리어가 있어요.",
           "이 배리어 3개를 기억해 봅시다. 첫 번째는 순서 정보가 없다는 거예요.",
           "병렬로 바꿨는데 그만큼 순서가 상관없어져 버린 겁니다.")],
     [check("차이가 1.33e-15 로 나왔다는 뜻은?",
            ["사실상 0, 곧 두 결과가 같다는 뜻", "오차가 크다는 뜻", "계산이 틀렸다는 뜻", "1.33 이라는 뜻"], 0,
            "e-15 는 소수점 아래 15째 자리라는 뜻이에요. 컴퓨터가 소수를 다루며 생기는 티끌이에요."),
      warn("헷갈리는 점",
           "'순서를 모른다' 는 '순서를 무시한다' 가 아니라 '섞으면 출력도 같이 섞인다' 예요.",
           "고치는 자리는 어텐션 계산 안이 아니라 입력이에요. 첫 층 전에 위치 벡터를 더해요.")])

# ---------------------------------------------------------------- p.10
page(10, "2.2 장벽 2: 어텐션은 평균만 낼 수 있어요",
     ["Attention Weight", "Position-wise Feed-Forward Network (FFN)", "Value", "Weighted Sum", "Attention"],
     [say("**어텐션 가중치(Attention Weight)** 는 0 이상이고 합이 1 이에요.",
          "그래서 출력은 늘 **밸류(Value)** 들 사이 어딘가에 있어요. 밖으로 못 나가요."),
      ana("평균의 한계",
          "반 친구들 키를 아무리 잘 섞어 평균 내도, 반에서 가장 큰 키보다 큰 값은 절대 안 나와요.",
          [("친구들 키", "**밸류(Value)** 들"), ("섞는 비율", "**어텐션 가중치(Attention Weight)**"),
           ("절대 못 넘는 최댓값", "볼록 결합의 한계"), ("새 값을 만들려면", "**위치별 피드포워드 신경망(FFN)**")])],
     [pts("영어 문장의 뜻",
          "**attention can only average, never leave the hull** = 어텐션은 평균만 낼 뿐, 범위를 벗어나지 못해요.",
          "**a convex combination of the value vectors** = 밸류 벡터들의 볼록 결합이에요.",
          "**Attention MOVES information. The feed-forward layer TRANSFORMS it.** = 어텐션은 정보를 옮기고, 피드포워드 층은 정보를 바꿔요."),
      py("비교와 & 그리고 .all()",
         ["`out >= V.min(axis=0)` 은 칸마다 참/거짓 표를 만들어요.",
          "`&` 는 '둘 다 참' 이고, `.all()` 은 '전부 참인가' 를 묻어요.",
          "`1e-9` 는 0.000000001 이에요. 소수 오차를 눈감아 주는 여유예요."],
         "import numpy as np\nprint((np.array([1., 2.]) > 0).all())", "True"),
      py("bool() 로 보기 좋게",
         ["NumPy 의 참/거짓은 np.True_ 처럼 찍혀요. `bool(...)` 로 감싸면 True 로 깔끔하게 나와요."],
         "import numpy as np\nprint(bool(np.array([True, True]).all()))", "True")],
     [code(17, "가중치와 출력의 성질 확인",
           [(1, 1, "**밸류(Value)** 행렬 V 를 다시 만들어요. X 에 Wv 를 곱한 것이에요."),
            (2, 2, "출력이 칸마다 V 의 최솟값과 최댓값 사이에 있는지 한 번에 확인해요."),
            (3, 4, "**어텐션 가중치(Attention Weight)** 가 모두 0 이상인지, 행 합이 1 인지 출력해요."),
            (5, 5, "출력이 밸류가 만드는 범위 안에 있는지 출력해요."),
            (6, 6, "어텐션은 정보를 옮기고 피드포워드 층은 정보를 바꾼다고 알려 줘요.")],
           link="강의 N4 p.42 Barrier 2 - The Feed-Forward Layer"),
      outpts(17),
      pts("세 줄이 증명한 것",
          "가중치가 음수가 아니고 합이 1 이면 출력은 **가중합(Weighted Sum)** 이 아니라 가중 '평균' 이에요.",
          "평균은 재료들의 범위를 벗어나지 못해요. 어텐션을 더 쌓아도 마찬가지예요.",
          "그래서 **트랜스포머(Transformer)** 에는 **위치별 피드포워드 신경망(FFN)** 이 꼭 있어야 해요.")],
     [check("어텐션을 여러 층 쌓으면 밸류 범위를 벗어날 수 있나요?",
            ["아니요. 평균의 평균도 여전히 평균이에요", "네, 두 층부터 벗어나요",
             "**소프트맥스(Softmax)** 를 빼면 가능해요", "**키(Key)** 를 늘리면 가능해요"], 0,
            "그래서 강의가 **위치별 피드포워드 신경망(FFN)** 을 장벽 2 의 처방으로 내놓았어요."),
      warn("헷갈리는 점",
           "'평균만 낸다' 는 어텐션이 쓸모없다는 뜻이 아니에요. 정보를 옮기는 일은 어텐션이 제일 잘해요.",
           "FFN 은 자리마다 따로 걸려요. 여기서는 토큰끼리 섞이지 않아요.")])

# ---------------------------------------------------------------- p.11
page(11, "2.3 장벽 3: 미래 가리기와 순서의 함정",
     ["Causal Masking", "Softmax", "Attention Weight", "Autoregressive", "Language Model (LM)"],
     [say("**언어 모델(Language Model)** 에서 토큰 i 는 자기 뒤 토큰을 보면 안 돼요.",
          "안 그러면 정답을 미리 보는 셈이라 아무것도 못 배워요.",
          "그래서 그 자리의 점수를 **소프트맥스(Softmax)** 전에 음의 무한대로 만들어요."),
      ana("시험지 가리개",
          "시험을 볼 때 뒷장을 종이로 덮어 두는 것과 같아요. 답을 다 채운 뒤 걷으면 이미 늦어요.",
          [("뒷장 덮기", "**인과 마스킹(Causal Masking)**"),
           ("덮는 시점이 먼저", "**소프트맥스(Softmax)** 전에 가리기"),
           ("다 푼 뒤 지우기", "소프트맥스 뒤에 0 으로 만드는 흔한 버그")])],
     [pts("영어 문장의 뜻",
          "**masking the future** = 미래를 가리기.",
          "**token i must not see tokens j > i** = 토큰 i 는 자기보다 뒤인 j 를 보면 안 돼요.",
          "**We set those scores to minus infinity before the softmax** = 그 점수를 소프트맥스 전에 음의 무한대로 둬요.",
          "**A very common bug is to zero the weights after the softmax** = 소프트맥스 뒤에 0 으로 만드는 것이 아주 흔한 버그예요."),
      py("np.tril 과 == 1",
         ["`np.tril(np.ones((n, n)))` 은 아래쪽 삼각형만 1 인 표를 만들어요.",
          "`== 1` 을 붙이면 참/거짓 표가 돼요. 참인 자리만 볼 수 있어요."],
         "import numpy as np\nprint(np.tril(np.ones((2, 2))))", "[[1. 0.]\n [1. 1.]]"),
      py("물결표 ~ 는 반대",
         ["`~causal` 은 참과 거짓을 뒤집어요. 곧 '볼 수 없는 자리' 예요.",
          "`A_masked[~causal].max()` 는 미래 자리에 남은 가장 큰 가중치를 봐요."],
         "import numpy as np\nprint(~np.array([True, False]))", "[False  True]"),
      py("표끼리 곱하기",
         ["`A * causal` 은 같은 자리끼리 곱해요. 거짓(0)인 자리는 0 이 돼요.",
          "이게 바로 노트북이 말하는 '흔한 버그' 를 재현하는 줄이에요."],
         "import numpy as np\nprint(np.array([0.5, 0.5]) * np.array([1, 0]))", "[0.5 0. ]")],
     [code(19, "올바른 마스킹과 틀린 마스킹",
           [(1, 1, "아래쪽 삼각형만 참인 표를 만들어요. 주석처럼 참인 자리만 볼 수 있어요."),
            (3, 3, "그 표를 마스크로 넘겨 **셀프 어텐션(Self-Attention)** 을 다시 해요."),
            (5, 7, "올바른 방식의 어텐션 행렬과 행 합을 출력해요. 행 합은 여전히 1 이에요."),
            (8, 8, "미래 자리에 남은 가장 큰 **어텐션 가중치(Attention Weight)** 를 출력해요. 0.0 이어야 해요."),
            (10, 10, "틀린 방식이에요. **소프트맥스(Softmax)** 를 건 뒤에 미래 자리를 0 으로 눌러요."),
            (11, 12, "그 결과의 행 합을 출력해요. 더 이상 1 이 아니에요.")],
           link="강의 N4 p.43 Barrier 3 - Masking the Future"),
      outpts(19, maxn=8, head="저장된 출력 1: 올바른 마스킹"),
      outpts(19, lo=8, maxn=3, head="저장된 출력 2: 틀린 마스킹"),
      prof("4주차 2교시 수업",
           "교수님: 마이너스 무한대는 익스포넨셜을 치면 0 에 가까운 수가 되죠.",
           "그래서 **인과 마스킹(Causal Masking)** 은 점수를 마이너스 무한으로 만들어서",
           "모델이 아직 보지 말아야 할 미래 토큰 정보를 완전히 차단하는 겁니다.")],
     [check("**소프트맥스(Softmax)** 뒤에 가중치를 0 으로 만들면 무엇이 깨지나요?",
            ["행의 합이 1 이 아니게 돼서 더 이상 가중 평균이 아니에요", "점수가 음수가 돼요",
             "**밸류(Value)** 가 바뀌어요", "아무 문제 없어요"], 0,
            "출력 행 합이 [0.054, 0.761, 0.529, 0.97, 1.0] 로 제각각이에요. 남은 가중치를 다시 나눠 주지 않았거든요."),
      warn("시험에 나오기 좋은 점",
           "마스크는 반드시 **소프트맥스(Softmax)** 앞에 걸어요. 강의 Check Yourself 2번 문제예요.",
           "첫 행이 [1, 0, 0, 0, 0] 인 것은 첫 토큰이 자기 자신밖에 볼 게 없어서예요.",
           "인코더는 이 마스크를 쓰지 않고 양쪽을 다 봐요. **자기회귀(Autoregressive)** 모델만 써요."),
      check("**인과 마스킹(Causal Masking)** 이 꼭 필요한 모델은?",
            ["**자기회귀(Autoregressive)** **언어 모델(Language Model)**", "양쪽을 다 보는 인코더",
             "번역기 인코더", "**위치 인코딩(Positional Encoding)**"], 0,
            "다음 토큰을 맞혀야 하는 **언어 모델(Language Model)** 만 미래를 가려요. 인코더는 양쪽을 봐요.")])

# ---------------------------------------------------------------- p.12
page(12, "Part 3 PyTorch 로 옮기고 내장 구현과 대조",
     ["Scaled Dot-Product Attention", "Tensor", "Shape", "Causal Masking", "Softmax"],
     [say("같은 식을 이제 PyTorch 로 옮겨요. 그래야 학습을 시킬 수 있어요.",
          "직접 만든 함수를 PyTorch 내장 구현과 맞대 봐요. 1e-6 수준에서 같으면 잘 만든 거예요.")],
     [pts("영어 문장의 뜻",
          "**Same maths, now in PyTorch so it can be trained** = 같은 수식인데 학습이 되게 PyTorch 로 옮겨요.",
          "**check it against PyTorch's own built-in implementation** = PyTorch 가 이미 갖고 있는 구현과 대조해요.",
          "**if they agree to 1e-6, we got it right** = 1e-6 안에서 같으면 제대로 만든 거예요."),
      py("따옴표 세 개 설명문",
         ["함수 첫 줄의 `'''...'''` 는 이 함수의 설명이에요. 실행에는 영향이 없어요.",
          "여기서는 q, k, v 의 **모양(Shape)** 이 (묶음, 헤드, 길이, 헤드 차원) 이라고 알려 줘요."],
         "def f():\n    '''설명'''\n    return 1\nprint(f())", "1"),
      py(".transpose(-2, -1)",
         ["마지막 두 축만 뒤집어요. (B, H, T, D) 가 (B, H, D, T) 가 돼요.",
          "앞 두 축은 그대로 둬야 묶음과 **헤드(Head)** 가 섞이지 않아요."],
         "import torch\nprint(tuple(torch.zeros(2, 3, 4, 5).transpose(-2, -1).shape))", "(2, 3, 5, 4)"),
      py("torch.triu 와 masked_fill",
         ["`torch.triu(..., diagonal=1)` 은 대각선 위쪽, 곧 미래 자리만 참으로 만들어요.",
          "`scores.masked_fill(future, float(\"-inf\"))` 는 참인 자리를 음의 무한대로 채워요."],
         "import torch\nprint(torch.triu(torch.ones(2, 2), diagonal=1))", "tensor([[0., 1.],\n        [0., 0.]])"),
      py("F.scaled_dot_product_attention",
         ["PyTorch 가 이미 갖고 있는 **스케일드 닷프로덕트 어텐션(Scaled Dot-Product Attention)** 이에요.",
          "`is_causal=True` 로 **인과 마스킹(Causal Masking)** 을 켜요. 답을 맞춰 보는 용도로 써요."],
         "import torch.nn.functional as F")],
     [code(21, "내가 만든 어텐션 대 PyTorch 내장 어텐션",
           [(1, 2, "함수를 정의하고, 설명문으로 입력 **모양(Shape)** 을 알려 줘요."),
            (3, 3, "키 차원 d_k 를 마지막 축 크기에서 꺼내요."),
            (4, 4, "점수를 구하고 루트 d_k 로 나눠요. 주석처럼 (B, H, T, T) 크기예요."),
            (5, 8, "causal 이 참이면 미래 자리를 찾아 음의 무한대로 채워요."),
            (9, 9, "마지막 축에 **소프트맥스(Softmax)** 를 걸어 가중치를 만들어요."),
            (10, 10, "가중치로 밸류를 섞은 출력과 가중치를 함께 돌려줘요."),
            (12, 12, "묶음 2, 길이 7, 전체 차원 64, **헤드(Head)** 4개로 정해요."),
            (13, 15, "q, k, v 를 (2, 4, 7, 16) 크기 무작위 **텐서(Tensor)** 로 만들어요. 16 은 64 나누기 4 예요."),
            (17, 17, "우리 함수로 계산해요."),
            (18, 18, "PyTorch 내장 함수로 같은 계산을 해요."),
            (20, 21, "우리 결과의 모양과 두 결과의 최대 차이를 출력해요.")],
           link="강의 N4 p.36 The Equations, p.43 마스킹"),
      outpts(21),
      steps("모양을 따라가기",
            ["q 는 (2, 4, 7, 16), k 를 눕히면 (2, 4, 16, 7)",
             "둘을 곱하면 (2, 4, 7, 7). 길이 7 짜리 어텐션 행렬이 묶음 2 x 헤드 4 개 생겨요.",
             "거기에 v (2, 4, 7, 16) 을 곱하면 다시 (2, 4, 7, 16)"],
            "입력과 출력의 **모양(Shape)** 이 같아요. 그래서 블록을 계속 쌓을 수 있어요.")],
     [check("두 결과의 최대 차이가 2.38e-07 이라는 뜻은?",
            ["소수 표현 오차 수준이라 사실상 같다는 뜻", "우리 구현이 틀렸다는 뜻",
             "PyTorch 가 틀렸다는 뜻", "차이가 2.38 이라는 뜻"], 0,
            "1e-6 보다 작으면 같다고 봐요. 노트북이 미리 정한 합격선이에요."),
      warn("헷갈리는 점",
           "우리 함수는 causal, 내장 함수는 is_causal 로 이름이 달라요. 옵션 이름을 틀리면 마스크가 안 걸려요.",
           "float(\"-inf\") 는 음의 무한대예요. 0 을 넣으면 마스킹이 안 돼요.")])

# ---------------------------------------------------------------- p.13
page(13, "3.1 멀티 헤드 셀프 어텐션을 모듈로",
     ["Multi-Head Attention (MHA)", "Head", "Self-Attention", "Shape", "Parameter", "Tensor"],
     [say("전체 차원 d 를 **헤드(Head)** h 개로 나눠서 따로 어텐션을 하고, 이어 붙인 뒤 다시 섞어요.",
          "이것이 **멀티 헤드 어텐션(Multi-Head Attention)** 이에요."),
      ana("여러 관점으로 한 문장 보기",
          "같은 사진을 문법 담당, 가까운 문맥 담당, 뜻 담당이 각각 본 뒤 의견을 모으는 것과 같아요.",
          [("담당자 한 명", "**헤드(Head)** 하나"), ("담당자 여러 명", "**멀티 헤드 어텐션(Multi-Head Attention)**"),
           ("의견 모으기", "이어 붙인 뒤 W^O 곱하기"), ("일을 나눠 맡기", "차원을 d/h 로 쪼개기")])],
     [pts("영어 문장의 뜻",
          "**Split d into h heads of size d/h** = d 를 크기 d/h 인 **헤드(Head)** h 개로 나눠요.",
          "**run attention in each independently, concatenate** = 각각 따로 어텐션 하고 이어 붙여요.",
          "**project back with W^O** = 마지막에 출력 행렬로 다시 섞어요.",
          "**One nn.Linear produces Q, K and V at once** = 선형층 하나로 Q, K, V 를 한 번에 만드는 구현 요령이에요."),
      py("class 와 nn.Module",
         ["`class MultiHeadSelfAttention(nn.Module):` 는 PyTorch 부품을 새로 만들어요.",
          "`__init__` 은 부품을 준비하는 곳, `forward` 는 실제로 계산하는 곳이에요.",
          "`super().__init__()` 은 부모가 준비할 것을 먼저 챙겨 줘요."],
         "import torch.nn as nn\nclass M(nn.Module):\n    def __init__(self):\n        super().__init__()\nprint(type(M()).__name__)", "M"),
      py("nn.Linear",
         ["`nn.Linear(64, 192)` 는 64칸을 192칸으로 바꾸는 학습되는 층이에요.",
          "곱할 행렬과 더할 편향 항이 **파라미터(Parameter)** 예요."],
         "import torch, torch.nn as nn\nprint(tuple(nn.Linear(64, 192)(torch.zeros(1, 64)).shape))", "(1, 192)"),
      py(".view, .transpose, .reshape",
         ["`.view(B, T, h, d_head)` 는 숫자는 그대로 두고 **모양(Shape)** 만 바꿔요.",
          "`.transpose(1, 2)` 는 축 1 과 2 를 맞바꿔요. `.reshape` 는 다시 합칠 때 써요."],
         "import torch\nprint(tuple(torch.zeros(2, 7, 64).view(2, 7, 4, 16).transpose(1, 2).shape))", "(2, 4, 7, 16)"),
      py(".split 과 map",
         ["`self.qkv(x).split(D, dim=-1)` 은 192칸을 64칸씩 셋으로 잘라요.",
          "`map(self.split_heads, (q, k, v))` 는 세 **텐서(Tensor)** 에 같은 함수를 한 번에 걸어요."],
         "print(list(map(abs, (-1, -2))))", "[1, 2]"),
      py("assert 와 나머지 연산 %",
         ["`d_model % n_heads == 0` 은 나눠떨어지는지 보는 것이에요.",
          "`assert 조건, \"메시지\"` 는 조건이 거짓이면 그 메시지와 함께 멈춰요."],
         "print(64 % 4, 64 % 5)", "0 4")],
     [code(23, "멀티 헤드 셀프 어텐션 모듈",
           [(1, 3, "새 부품을 정의하고, 만들 때 전체 차원, **헤드(Head)** 수, 마스크 여부를 받아요."),
            (4, 4, "전체 차원이 헤드 수로 나눠떨어지는지 먼저 확인해요."),
            (5, 5, "헤드 수, 헤드 하나의 차원(d/h), 마스크 여부를 저장해요."),
            (6, 6, "선형층 하나로 Q, K, V 를 한 번에 만들어요. 주석처럼 세 행렬을 한 행렬에 넣은 거예요."),
            (7, 7, "헤드를 합친 뒤 다시 섞어 줄 출력 행렬 W^O 예요."),
            (9, 11, "(B, T, D) 를 (B, h, T, D/h) 로 바꾸는 함수예요. 주석에 모양 변화가 적혀 있어요."),
            (13, 14, "실제 계산이에요. 입력의 묶음 수, 길이, 차원을 꺼내요."),
            (15, 15, "한 번에 만든 192칸을 64칸씩 q, k, v 로 잘라요."),
            (16, 16, "셋 모두 **헤드(Head)** 별로 쪼개요."),
            (17, 17, "앞 쪽에서 만든 **스케일드 닷프로덕트 어텐션(Scaled Dot-Product Attention)** 을 불러요."),
            (18, 18, "헤드를 다시 이어 붙여 (B, T, D) 로 돌려놔요."),
            (19, 19, "나중에 그림으로 보려고 **어텐션 가중치(Attention Weight)** 를 따로 보관해요."),
            (20, 20, "출력 행렬을 곱해 돌려줘요."),
            (22, 24, "차원 64, 헤드 4개짜리 모듈을 만들고 (2, 7, 64) 입력을 넣어요."),
            (25, 27, "입력, 출력, 어텐션의 **모양(Shape)** 을 출력해요.")],
           link="강의 N4 p.47 Multi-Head Attention"),
      outpts(23),
      prof("4주차 2교시 수업",
           "교수님: 헤드는 그야말로 어텐션을 보는 행위 하나입니다.",
           "헤드 1은 문법적인 관계, 헤드 2는 가까운 문맥, 헤드 3은 의미의 뜻을 보겠다,",
           "이렇게 각 헤드가 서로 다른 Wq, Wk, Wv 를 씁니다.")],
     [check("입력이 (2, 7, 64) 인데 출력도 (2, 7, 64) 인 까닭은?",
            ["헤드를 다시 이어 붙이고 W^O 로 섞어 원래 차원으로 돌려놓기 때문", "**헤드(Head)** 가 4개라서",
             "**소프트맥스(Softmax)** 때문", "무작위라서"], 0,
            "모양이 그대로여야 블록을 몇 층이든 쌓을 수 있어요. 노트북 주석도 같은 모양 들어가 같은 모양 나온다고 해요."),
      warn("헷갈리는 점",
           "attn 의 **모양(Shape)** 은 (묶음, 헤드, 쿼리, 키) 예요. (2, 4, 7, 7) 의 마지막 두 7 을 바꿔 읽으면 안 돼요.",
           "`self.qkv` 의 출력이 3 x 64 = 192 칸인 것은 Q, K, V 를 한 층에 몰아넣었기 때문이에요.")])

# ---------------------------------------------------------------- p.14
page(14, "3.2 헤드를 늘려도 공짜인지 세어 보기",
     ["Multi-Head Attention (MHA)", "Head", "Parameter"],
     [say("강의는 **헤드(Head)** 가 d/h 차원만 쓰니까 h 개를 써도 비용이 같다고 했어요.",
          "**파라미터(Parameter)** 개수를 직접 세어 확인해요.")],
     [pts("영어 문장의 뜻",
          "**h heads really are free** = 헤드 h 개는 정말 공짜예요.",
          "**Count the parameters and see** = 파라미터를 세어서 확인해 보세요.",
          "**h different views of the sentence, at no extra cost** = 추가 비용 없이 문장을 h 가지 관점으로 봐요."),
      py(".parameters() 와 .numel()",
         ["`m.parameters()` 는 모델 안의 학습되는 숫자 묶음을 모두 꺼내요.",
          "`p.numel()` 은 그 묶음에 숫자가 몇 개인지예요.",
          "`sum(p.numel() for p in m.parameters())` 가 전체 **파라미터(Parameter)** 수예요."],
         "import torch.nn as nn\nprint(sum(p.numel() for p in nn.Linear(2, 3).parameters()))", "9"),
      py("천 단위 쉼표 서식",
         ["`f\"{16640:,}\"` 은 16,640 처럼 세 자리마다 쉼표를 넣어요.",
          "`{h:>8}` 은 오른쪽으로 8칸 맞춰 표처럼 보이게 해요."],
         "print(f\"{16640:,}\")", "16,640")],
     [code(25, "헤드 수만 바꿔 가며 파라미터 세기",
           [(1, 1, "표의 머리글을 출력해요."),
            (2, 2, "**헤드(Head)** 를 1, 2, 4, 8, 16 개로 바꿔 가며 돌아요."),
            (3, 3, "그때마다 차원 64 짜리 모듈을 새로 만들어요."),
            (4, 4, "그 모듈의 **파라미터(Parameter)** 개수를 모두 더해 출력해요."),
            (5, 5, "값이 전부 같다고, 곧 h 가지 관점이 추가 비용 없이 공짜라고 알려 줘요.")],
           link="강의 N4 p.48 Multi-Head Costs Nothing Extra"),
      outpts(25),
      steps("16,640 을 손으로 세기",
            ["qkv 층: 64칸을 192칸으로. 곱할 행렬 64 x 192 = 12,288",
             "거기에 편향 항 192 개를 더하면 12,480",
             "출력 층 W^O: 64 x 64 = 4,096 에 편향 항 64 개를 더해 4,160",
             "12,480 + 4,160 = 16,640"],
            "**헤드(Head)** 수는 이 계산 어디에도 안 나와요. 그래서 h 를 바꿔도 값이 같아요."),
      prof("4주차 2교시 수업",
           "교수님: 헤드를 여러 개 쓴다고 전체 차원을 키우는 게 아니라",
           "전체 차원을 h 로 나눠서 서로 다른 관점에서 보는 겁니다.",
           "그래서 멀티 헤드라고 헤드를 여러 번 했을 때 계산량이 더 많아지는 건 아니에요.")],
     [check("**헤드(Head)** 를 1개에서 16개로 늘렸는데 **파라미터(Parameter)** 가 그대로인 까닭은?",
            ["헤드마다 쓰는 차원이 64/h 로 줄어들기 때문", "PyTorch 가 아껴 주기 때문",
             "**소프트맥스(Softmax)** 때문", "편향 항이 없기 때문"], 0,
            "쪼개서 나눠 쓰는 것이지 더 붙이는 게 아니에요. 교수님이 강조한 부분이에요."),
      eng("답안 문장",
          "멀티 헤드 어텐션은 전체 차원 d 를 헤드 수 h 로 나눈 d/h 차원 부분공간에서 어텐션을 각각 수행한 뒤 이어 붙여 출력 행렬로 사영하므로, 파라미터 수와 계산량은 헤드 하나일 때와 같다.",
          "차원을 키우는 게 아니라 쪼개는 것이라서 비용이 같아요. 실습에서 16,640 으로 확인했어요.",
          "'쪼개는 것이지 붙이는 게 아니다' 한 줄로 외워요."),
      warn("헷갈리는 점",
           "'공짜' 는 **파라미터(Parameter)** 와 계산량 이야기예요. 성능이 늘 좋아진다는 뜻은 아니에요.",
           "64 를 16 으로 나누면 헤드마다 4칸뿐이에요. 너무 잘게 쪼개면 헤드 하나가 볼 게 적어져요.")])

# ---------------------------------------------------------------- p.15
page(15, "Part 4 시작: 위치 인코딩과 Pre-LN 블록",
     ["Positional Encoding", "Sinusoidal Positional Encoding", "Residual Connection",
      "Layer Normalization (LayerNorm)", "Transformer", "Position-wise Feed-Forward Network (FFN)"],
     [say("이제 전부 조립해요. **위치 인코딩(Positional Encoding)** 을 더하고,",
          "어텐션과 **위치별 피드포워드 신경망(FFN)** 을 **잔차 연결(Residual Connection)** 로 잇고,",
          "**층 정규화(Layer Normalization)** 를 앞에 두는 Pre-LN 블록을 쌓아요."),
      pts("Part 4 에서 할 일",
          "4.1 **사인 코사인 위치 인코딩(Sinusoidal Positional Encoding)** 만들고 그림으로 보기",
          "4.2 **트랜스포머(Transformer)** 블록과 미니 모델 조립하기",
          "4.3 어텐션이 보이는 과제로 실제 학습시키기",
          "4.4 어텐션 그림 읽기, 4.5 장벽 세 개를 실험으로 확인하기")],
     [pts("영어 문장의 뜻",
          "**positional encoding + Pre-LN block** = 위치 인코딩과 층 정규화를 앞에 둔 블록.",
          "**attention → FFN, each with a residual** = 어텐션 다음 **위치별 피드포워드 신경망(FFN)**, 각각 **잔차 연결(Residual Connection)** 을 달고.",
          "**The heatmap looks striped** = 히트맵이 줄무늬처럼 보여요.",
          "**a sin/cos pair of the same frequency** = 이웃한 두 열이 같은 주파수의 사인, 코사인 쌍이에요.",
          "**Low dimensions turn fast, high dimensions turn slowly** = 낮은 차원은 빨리, 높은 차원은 천천히 돌아요."),
      pts("왜 줄무늬가 보이나",
          "차원 0 과 1 이 같은 파장, 차원 2 와 3 이 그다음 파장을 써요.",
          "그래서 이웃한 두 열이 비슷하게 보이고 줄무늬처럼 나타나요.",
          "위치마다 64칸 전체의 무늬가 달라서 자리를 구별할 수 있어요.")],
     [pts("강의와 짝",
          "N4 p.40 Barrier 1 이 **위치 인코딩(Positional Encoding)** 이에요.",
          "N4 p.49 가 **잔차 연결(Residual Connection)**, N4 p.50 이 **층 정규화(Layer Normalization)** 예요.",
          "N4 p.51 Pre-LN or Post-LN 이 이 노트북이 고른 배치예요. 요즘 LLM 은 전부 Pre-LN 이에요.")],
     [check("**사인 코사인 위치 인코딩(Sinusoidal Positional Encoding)** 의 히트맵이 줄무늬인 까닭은?",
            ["이웃한 두 열이 같은 파장의 사인, 코사인 쌍이라서", "무작위라서", "**헤드(Head)** 가 여러 개라서", "학습이 덜 돼서"], 0,
            "차원 0 과 1 이 한 쌍, 2 와 3 이 다음 쌍이에요. 그래서 옆 열끼리 닮아 보여요."),
      warn("헷갈리는 점",
           "**층 정규화(Layer Normalization)** 는 토큰 하나 안에서만 고르게 만들어요. 토큰끼리 섞지 않아요.",
           "Pre-LN 은 **잔차 연결(Residual Connection)** 길을 깨끗이 남겨 둬서 깊게 쌓아도 학습이 돼요.")])

# ---------------------------------------------------------------- p.16
page(16, "4.1 사인 코사인 위치 인코딩 만들기",
     ["Sinusoidal Positional Encoding", "Positional Encoding", "Tensor", "Shape", "Permutation Equivariance"],
     [say("자리마다 다른 물결 무늬 벡터를 만들어요.",
          "이걸 토큰 벡터에 더하면 **셀프 어텐션(Self-Attention)** 도 순서를 알게 돼요.")],
     [pts("무엇을 만드나",
          "**모양(Shape)** 이 (60, 64) 인 표예요. 자리 60개, 차원 64칸.",
          "짝수 칸은 사인, 홀수 칸은 코사인으로 채워요.",
          "파장이 차원마다 달라서 자리마다 고유한 무늬가 생겨요."),
      py("torch.zeros 와 torch.arange",
         ["`torch.zeros(60, 64)` 는 0 으로 채운 60행 64열 **텐서(Tensor)** 예요.",
          "`torch.arange(60)` 은 0, 1, 2, ... 59 를 만들어요.",
          "`.unsqueeze(1)` 은 칸 하나를 끼워 넣어 (60,) 을 (60, 1) 로 만들어요."],
         "import torch\nprint(tuple(torch.arange(3).unsqueeze(1).shape))", "(3, 1)"),
      py("건너뛰며 고르는 [:, 0::2]",
         ["`pe[:, 0::2]` 는 모든 행의 0, 2, 4, ... 번째 열, 곧 짝수 칸이에요.",
          "`pe[:, 1::2]` 는 홀수 칸이에요. 사인과 코사인을 번갈아 넣으려고 써요."],
         "import torch\nprint(torch.arange(6)[0::2])", "tensor([0, 2, 4])"),
      py("torch.pow 와 나눗셈 방송",
         ["`torch.pow(10000.0, ...)` 은 10000 의 거듭제곱이에요. 칸마다 파장이 달라져요.",
          "`pos / div` 는 (60, 1) 과 (32,) 가 만나 (60, 32) 가 돼요. 모양이 자동으로 맞춰져요."],
         "import torch\nprint(tuple((torch.zeros(60, 1) / torch.zeros(32)).shape))", "(60, 32)"),
      py("plt.subplots 와 imshow",
         ["`plt.subplots(1, 2, ...)` 는 그림 하나에 그래프 칸 두 개를 만들어요.",
          "`imshow` 는 숫자 표를 색으로 칠한 히트맵이에요. `plt.show()` 로 화면에 띄워요."],
         "import matplotlib.pyplot as plt")],
     [formula("사인 코사인 위치 인코딩",
              r"PE_{(pos,2i)}=\sin\!\left(\frac{pos}{10000^{2i/d}}\right),\quad PE_{(pos,2i+1)}=\cos\!\left(\frac{pos}{10000^{2i/d}}\right)",
              [(r"pos", "몇 번째 자리인지"),
               (r"2i,\,2i+1", "짝수 칸은 사인, 홀수 칸은 코사인"),
               (r"10000^{2i/d}", "칸마다 다른 파장. 뒤 칸일수록 천천히 돌아요")],
              "학습할 **파라미터(Parameter)** 가 하나도 없어요. 식으로 바로 계산해요."),
      code(27, "위치 인코딩 표 만들고 그림 그리기",
           [(1, 1, "자리 수와 차원 수를 받아 **위치 인코딩(Positional Encoding)** 표를 만드는 함수예요."),
            (2, 2, "0 으로 채운 (자리 수, 차원) 표를 준비해요."),
            (3, 3, "0부터 자리 수 - 1 까지 번호를 세로로 세워요."),
            (4, 4, "칸마다 다른 파장을 계산해요. 10000 의 거듭제곱이에요."),
            (5, 6, "짝수 칸은 사인, 홀수 칸은 코사인으로 채워요."),
            (7, 7, "완성한 표를 돌려줘요."),
            (9, 9, "자리 60개, 차원 64칸짜리 표를 만들어요."),
            (10, 10, "그림 칸 두 개를 준비해요."),
            (11, 13, "왼쪽 칸에 표 전체를 히트맵으로 칠하고, 축 이름과 제목, 색 막대를 붙여요."),
            (14, 15, "오른쪽 칸에 차원 0, 8, 24 세 개를 물결 곡선으로 그려요."),
            (16, 17, "범례와 축 이름, 제목을 붙여요."),
            (18, 18, "여백을 정리하고 화면에 띄워요.")],
           link="강의 N4 p.40 sinusoids of geometrically spaced frequencies"),
      pts("저장된 출력",
          "`<Figure size 1100x280 with 3 Axes>` 와 그림이 나와요. 숫자 출력은 없어요.",
          "왼쪽 히트맵은 줄무늬, 오른쪽은 차원마다 파장이 다른 물결 곡선이에요.",
          "차원 0 은 빠르게, 차원 24 는 아주 천천히 돌아요."),
      steps("맨 첫 자리를 손으로",
            ["pos = 0 이면 사인은 sin(0) = 0",
             "코사인은 cos(0) = 1",
             "그래서 0번 자리 벡터는 0, 1, 0, 1, ... 이 돼요.",
             "pos = 1 이면 칸마다 조금씩 다른 값이 나와요."],
            "자리마다 64칸 무늬가 달라서, 같은 단어라도 자리가 다르면 벡터가 달라져요.")],
     [check("**위치 인코딩(Positional Encoding)** 을 토큰 벡터에 더하는 까닭은?",
            ["**순열 등변성(Permutation Equivariance)** 때문에 순서를 입력에 넣어 줘야 해서",
             "학습을 빠르게 하려고", "**파라미터(Parameter)** 를 줄이려고", "**소프트맥스(Softmax)** 를 위해"], 0,
            "2.1 에서 잰 그대로예요. 순서가 계산 안에 없으니 입력에 넣어 줘요."),
      warn("헷갈리는 점",
           "더하는 것이지 이어 붙이는 게 아니에요. 차원이 늘지 않아요.",
           "**사인 코사인 위치 인코딩(Sinusoidal Positional Encoding)** 은 학습하지 않아요. 요즘 LLM 은 RoPE 를 더 많이 써요.")])

d = {"deck": "N4L", "from": 1, "to": 16, "glossary": G, "slides": S}
raw = json.dumps(d, ensure_ascii=False, indent=1)
for ch in ("—", "–", "·", "・"):
    assert ch not in raw, ch
(W / "lesson" / "N4L_001-016.json").write_text(raw, encoding="utf-8")
print("ok", len(S))
