# -*- coding: utf-8 -*-
"""자연어처리 '직접 해보기' 연습 노트북 (Colab 에서 바로 실행). 교수님 실습 노트북과 별개로 새로 만든 연습.

사용: python work/nlp/practice/build_practice.py [--test]
출력: subjects/nlp/practice/nlp_wb_practice.ipynb, nlp_w2_practice.ipynb, nlp_w3_practice.ipynb,
     nlp_w4_practice.ipynb, nlp_w5_practice.ipynb
--test: 빈칸 자리에 정답 코드를 넣은 노트북을 만들어 nbclient 로 끝까지 실행해 본다 (검사용, 결과는 임시 폴더)
노트북 구성: 문제 설명(마크다운) → 빈칸 코드(TODO) → 확인 셀(assert). 맨 끝에 정답 코드 모음(마크다운 코드 블록).

문제 한 개에 쓰는 칸:
  md          문제 설명 (첫 줄이 제목)
  think       생각 순서. 코드를 치기 전에 말로 읊는 단계 (리스트)
  pseudo      모범 의사코드 줄들 (리스트)
  pseudo_first  True 면 코드 칸 바로 앞에 '의사코드 먼저' 칸이 따로 들어간다. 여러 줄을 새로 쓰는 문제에 붙인다
  pseudo_show   pseudo_first 문제에서 모범 의사코드를 그 자리에 보여 줄지. False 면 감추고 맨 아래 정답 모음에서만 보여 준다
  next        이 계산이 나중에 강의 어디에서 다시 나오는지 한 줄
  todo/sol/check  빈칸 코드 / 정답 코드 / 확인 셀
"""
import json, os, pathlib, sys, tempfile

sys.stdout.reconfigure(encoding="utf-8")
W = pathlib.Path(__file__).resolve().parent.parent
ROOT = W.parent.parent
OUT = ROOT / "subjects" / "nlp" / "practice"
BAD = ("\u2014", "\u2013", "\u00b7")

CHECK_HEAD = "def ok(cond, msg):\n    assert cond, msg\n    print('정답! ' + msg)\n"

W2 = {
    "file": "nlp_w2_practice.ipynb",
    "title": "2주차 직접 해보기: 토큰화와 단어 벡터",
    "intro": ("사이트의 2주차 회독과 정리 슬라이드를 본 다음 풀어요. 위에서부터 차례로 `Shift+Enter` 로 실행해요.\n\n"
              "- `# TODO` 가 있는 칸의 `None` 을 알맞은 코드로 바꿔요.\n"
              "- 바로 아래 **확인 셀**을 실행하면 맞았는지 알려 줘요. 틀리면 빨간 AssertionError 와 힌트가 나와요.\n"
              "- 막히면 맨 아래 **정답 코드**를 봐요.\n\n"
              "GPU 는 필요 없어요. 인터넷 다운로드도 없어요."),
    "setup": "import math\nfrom collections import Counter\n" + CHECK_HEAD + "print('준비 끝')",
    "ex": [
        {"md": "## 1. 문장을 토큰으로 자르는 두 가지 방법\n\n강의 N2 p.7(단어 단위), p.9(문자 단위). 공백으로 자르면 **단어(word)** 토큰, 글자 하나하나로 자르면 **문자(character)** 토큰이에요.\n\n`sentence.split()` 은 공백 기준으로 자른 리스트, `list(sentence)` 는 글자 하나씩 자른 리스트를 돌려줘요.",
         "todo": "sentence = \"the cat sat on the mat\"\n\nwords = None   # TODO: 공백으로 자르기\nchars = None   # TODO: 글자 하나씩 (공백도 한 글자로 쳐요)\n\nprint(words)\nprint(len(words), len(chars))",
         "sol": "sentence = \"the cat sat on the mat\"\n\nwords = sentence.split()\nchars = list(sentence)\n\nprint(words)\nprint(len(words), len(chars))",
         "check": "ok(words == ['the', 'cat', 'sat', 'on', 'the', 'mat'], '단어 토큰 6개')\nok(len(chars) == 22, '문자 토큰 22개 (공백 5개 포함)')\nok(len(set(words)) == 5, '서로 다른 단어(어휘)는 5개: the 가 두 번 나와요')"},
        {"md": "## 2. BPE 1단계: 붙어 있는 쌍 세기\n\n강의 N2 p.11-12 의 장난감 말뭉치예요. 단어를 글자 튜플로 쓰고, 끝에 `</w>`(단어 끝 표시)를 붙였어요. 숫자는 그 단어가 나온 횟수예요.\n\n`count_pairs` 는 **바로 옆에 붙은 두 기호 쌍**이 모두 몇 번 나오는지 세요. 단어가 5번 나왔으면 그 단어 안의 쌍도 5번씩 세요.",
         "todo": "corpus = {\n    ('l', 'o', 'w', '</w>'): 5,\n    ('l', 'o', 'w', 'e', 'r', '</w>'): 2,\n    ('n', 'e', 'w', 'e', 's', 't', '</w>'): 6,\n    ('w', 'i', 'd', 'e', 's', 't', '</w>'): 3,\n}\n\ndef count_pairs(corpus):\n    pairs = Counter()\n    for word, freq in corpus.items():\n        for i in range(len(word) - 1):\n            pair = (word[i], word[i + 1])\n            pairs[pair] += None   # TODO: 이 단어가 나온 횟수만큼 더하기\n    return pairs\n\npairs = count_pairs(corpus)\nprint(pairs.most_common(4))",
         "sol": "corpus = {\n    ('l', 'o', 'w', '</w>'): 5,\n    ('l', 'o', 'w', 'e', 'r', '</w>'): 2,\n    ('n', 'e', 'w', 'e', 's', 't', '</w>'): 6,\n    ('w', 'i', 'd', 'e', 's', 't', '</w>'): 3,\n}\n\ndef count_pairs(corpus):\n    pairs = Counter()\n    for word, freq in corpus.items():\n        for i in range(len(word) - 1):\n            pair = (word[i], word[i + 1])\n            pairs[pair] += freq\n    return pairs\n\npairs = count_pairs(corpus)\nprint(pairs.most_common(4))",
         "check": "ok(pairs[('e', 's')] == 9, \"('e','s') 는 newest 6번 + widest 3번 = 9번\")\nok(pairs[('l', 'o')] == 7, \"('l','o') 는 low 5번 + lower 2번 = 7번\")\nok(pairs[('w', 'e')] == 8, \"('w','e') 는 lower 2번 + newest 6번 = 8번\")"},
        {"md": "## 3. BPE 2단계: 가장 많은 쌍을 하나로 합치기\n\n`merge` 는 말뭉치의 모든 단어에서 쌍 `(a, b)` 가 붙어 있는 곳을 한 기호 `a + b` 로 바꿔요. 예를 들어 `('e', 's')` 를 합치면 `n e w e s t` 가 `n e w es t` 가 돼요.",
         "todo": "def merge(corpus, pair):\n    a, b = pair\n    new = {}\n    for word, freq in corpus.items():\n        out, i = [], 0\n        while i < len(word):\n            if i < len(word) - 1 and word[i] == a and word[i + 1] == b:\n                out.append(None)   # TODO: 두 기호를 이어 붙인 새 기호\n                i += 2\n            else:\n                out.append(word[i])\n                i += 1\n        new[tuple(out)] = freq\n    return new\n\nafter = merge(corpus, ('e', 's'))\nfor w, f in after.items():\n    print(' '.join(w), f)",
         "sol": "def merge(corpus, pair):\n    a, b = pair\n    new = {}\n    for word, freq in corpus.items():\n        out, i = [], 0\n        while i < len(word):\n            if i < len(word) - 1 and word[i] == a and word[i + 1] == b:\n                out.append(a + b)\n                i += 2\n            else:\n                out.append(word[i])\n                i += 1\n        new[tuple(out)] = freq\n    return new\n\nafter = merge(corpus, ('e', 's'))\nfor w, f in after.items():\n    print(' '.join(w), f)",
         "check": "ok(('n', 'e', 'w', 'es', 't', '</w>') in after, 'newest 가 n e w es t </w> 로 바뀌었어요')\nok(('l', 'o', 'w', '</w>') in after, 'es 가 없는 low 는 그대로예요')"},
        {"md": "## 4. BPE 학습 반복과 처음 보는 단어 자르기\n\n쌍 세기 → 가장 많은 쌍 합치기 → 규칙 기록을 정해진 횟수만큼 반복하면 BPE 학습이 끝나요(N2 p.11). 배운 병합 규칙을 **같은 순서로** 새 단어에 적용하면 처음 보는 단어도 자를 수 있어요(N2 p.13).\n\n`max(pairs, key=pairs.get)` 은 횟수가 가장 큰 쌍을 골라요(같으면 먼저 센 쌍).",
         "todo": "def train_bpe(corpus, n_merges):\n    rules = []\n    for _ in range(n_merges):\n        pairs = count_pairs(corpus)\n        best = None   # TODO: 가장 많이 나온 쌍 고르기\n        corpus = merge(corpus, best)\n        rules.append(best)\n    return rules\n\ndef tokenize(word, rules):\n    symbols = list(word) + ['</w>']\n    for a, b in rules:\n        symbols = list(merge({tuple(symbols): 1}, (a, b)))[0]\n    return list(symbols)\n\nrules = train_bpe(corpus, 8)\nprint(rules)\nprint(tokenize('lowest', rules))",
         "sol": "def train_bpe(corpus, n_merges):\n    rules = []\n    for _ in range(n_merges):\n        pairs = count_pairs(corpus)\n        best = max(pairs, key=pairs.get)\n        corpus = merge(corpus, best)\n        rules.append(best)\n    return rules\n\ndef tokenize(word, rules):\n    symbols = list(word) + ['</w>']\n    for a, b in rules:\n        symbols = list(merge({tuple(symbols): 1}, (a, b)))[0]\n    return list(symbols)\n\nrules = train_bpe(corpus, 8)\nprint(rules)\nprint(tokenize('lowest', rules))",
         "check": "ok(rules[0] == ('e', 's'), '첫 병합은 9번 나온 (e, s)')\nok(tokenize('lowest', rules) == ['low', 'est</w>'], '학습 때 없던 lowest 도 low + est</w> 로 잘려요')"},
        {"md": "## 5. Fertility: 단어 하나가 토큰 몇 개로 쪼개지나\n\n강의 N2 p.20. **fertility = 토큰 수 / 공백 단어 수**. 영어 중심 토크나이저는 한국어를 잘게 쪼개서 fertility 가 커져요. 아래 토큰 목록은 설명용으로 만든 **예시**예요(실제 토크나이저 결과는 실습 N2L p.14-15 에서 봐요).",
         "todo": "sentence = '오늘은 날씨가 정말 좋네요'\ntokens_a = ['오늘', '은', '날씨', '가', '정말', '좋', '네요']            # 예시: 한국어로 학습한 토크나이저\ntokens_b = ['오', '늘', '은', '날', '씨', '가', '정', '말', '좋', '네', '요']  # 예시: 한국어를 잘 모르는 토크나이저\n\ndef fertility(tokens, sentence):\n    return None   # TODO: 토큰 수 / 공백으로 자른 단어 수\n\nprint(fertility(tokens_a, sentence), fertility(tokens_b, sentence))",
         "sol": "sentence = '오늘은 날씨가 정말 좋네요'\ntokens_a = ['오늘', '은', '날씨', '가', '정말', '좋', '네요']\ntokens_b = ['오', '늘', '은', '날', '씨', '가', '정', '말', '좋', '네', '요']\n\ndef fertility(tokens, sentence):\n    return len(tokens) / len(sentence.split())\n\nprint(fertility(tokens_a, sentence), fertility(tokens_b, sentence))",
         "check": "ok(abs(fertility(tokens_a, sentence) - 1.75) < 1e-9, '7 토큰 / 4 단어 = 1.75')\nok(abs(fertility(tokens_b, sentence) - 2.75) < 1e-9, '11 토큰 / 4 단어 = 2.75: 토큰이 많을수록 비용과 문맥 자리를 더 써요')"},
        {"md": "## 6. 내적과 코사인 유사도\n\n강의 N2 p.27, 기초 다지기 2단원. 내적은 **같은 자리끼리 곱해서 모두 더한 값**, 코사인 유사도는 내적을 두 벡터 길이의 곱으로 나눈 값(-1 ~ 1)이에요. 아래 3차원 벡터는 설명용 **장난감 벡터**예요.",
         "todo": "movie = [0.9, 0.8, 0.1]\ndrama = [0.8, 0.9, 0.2]\nkimchi = [0.1, 0.0, 0.9]\n\ndef dot(u, v):\n    return None   # TODO: 같은 자리끼리 곱해서 더하기 (sum 과 zip 사용)\n\ndef norm(u):\n    return math.sqrt(dot(u, u))\n\ndef cosine(u, v):\n    return dot(u, v) / (norm(u) * norm(v))\n\nprint(round(cosine(movie, drama), 3), round(cosine(movie, kimchi), 3))",
         "sol": "movie = [0.9, 0.8, 0.1]\ndrama = [0.8, 0.9, 0.2]\nkimchi = [0.1, 0.0, 0.9]\n\ndef dot(u, v):\n    return sum(a * b for a, b in zip(u, v))\n\ndef norm(u):\n    return math.sqrt(dot(u, u))\n\ndef cosine(u, v):\n    return dot(u, v) / (norm(u) * norm(v))\n\nprint(round(cosine(movie, drama), 3), round(cosine(movie, kimchi), 3))",
         "check": "ok(abs(dot(movie, drama) - 1.46) < 1e-9, '0.9x0.8 + 0.8x0.9 + 0.1x0.2 = 1.46')\nok(cosine(movie, drama) > 0.9 > cosine(movie, kimchi), '영화와 드라마는 가깝고 영화와 김치는 멀어요')"},
        {"md": "## 7. 소프트맥스: 점수를 확률로\n\n강의 N2 p.33, 기초 다지기 6단원. 점수마다 `exp` 를 씌우고, 전체 합으로 나눠요. 결과는 모두 0보다 크고 합이 1이에요.",
         "todo": "scores = [2.0, 1.0, 0.0]\n\ndef softmax(xs):\n    exps = [math.exp(x) for x in xs]\n    total = None   # TODO: exps 의 합\n    return [e / total for e in exps]\n\nprobs = softmax(scores)\nprint([round(p, 3) for p in probs])",
         "sol": "scores = [2.0, 1.0, 0.0]\n\ndef softmax(xs):\n    exps = [math.exp(x) for x in xs]\n    total = sum(exps)\n    return [e / total for e in exps]\n\nprobs = softmax(scores)\nprint([round(p, 3) for p in probs])",
         "check": "ok(abs(sum(probs) - 1) < 1e-9, '확률의 합은 1')\nok([round(p, 3) for p in probs] == [0.665, 0.245, 0.09], '가장 큰 점수가 가장 큰 확률을 받아요')"},
        {"md": "## 8. Skip-gram 이 만드는 (중심 단어, 문맥 단어) 쌍\n\n강의 N2 p.28-29. 윈도우 크기 m 이면 중심 단어 앞뒤 m 칸 안의 단어가 문맥 단어예요. 중심 단어 자기 자신은 빼요.",
         "todo": "tokens = ['나는', '어제', '재미있는', '영화', '를', '봤다']\nm = 2\n\npairs = []\nfor t, center in enumerate(tokens):\n    for j in range(-m, m + 1):\n        if j == 0:\n            continue\n        k = t + j\n        if None:   # TODO: k 가 0 이상이고 len(tokens) 보다 작을 때만\n            pairs.append((center, tokens[k]))\n\nprint(len(pairs))\nprint([p for p in pairs if p[0] == '영화'])",
         "sol": "tokens = ['나는', '어제', '재미있는', '영화', '를', '봤다']\nm = 2\n\npairs = []\nfor t, center in enumerate(tokens):\n    for j in range(-m, m + 1):\n        if j == 0:\n            continue\n        k = t + j\n        if 0 <= k < len(tokens):\n            pairs.append((center, tokens[k]))\n\nprint(len(pairs))\nprint([p for p in pairs if p[0] == '영화'])",
         "check": "ok(len(pairs) == 18, '6단어, m=2 이면 가장자리를 빼고 18쌍')\nok([p[1] for p in pairs if p[0] == '영화'] == ['어제', '재미있는', '를', '봤다'], '영화의 문맥 단어는 앞 2개, 뒤 2개')"},
        {"md": "## 9. 단어 유추: 왕 - 남자 + 여자\n\n강의 N2 p.41, p.48. 벡터 더하기 빼기로 만든 점에서 코사인 유사도가 가장 큰 단어를 찾아요(질문에 쓴 단어는 빼요). 아래 2차원 벡터는 **장난감 벡터**예요.",
         "todo": "vec = {\n    '왕': [0.9, 0.9], '여왕': [0.9, 0.1], '남자': [0.1, 0.9],\n    '여자': [0.1, 0.1], '사과': [0.5, -0.8],\n}\ntarget = [vec['왕'][i] - vec['남자'][i] + vec['여자'][i] for i in range(2)]\n\ncands = [w for w in vec if w not in ('왕', '남자', '여자')]\nanswer = None   # TODO: cands 중 cosine(vec[w], target) 이 가장 큰 w (max 와 key 사용)\nprint(target, answer)",
         "sol": "vec = {\n    '왕': [0.9, 0.9], '여왕': [0.9, 0.1], '남자': [0.1, 0.9],\n    '여자': [0.1, 0.1], '사과': [0.5, -0.8],\n}\ntarget = [vec['왕'][i] - vec['남자'][i] + vec['여자'][i] for i in range(2)]\n\ncands = [w for w in vec if w not in ('왕', '남자', '여자')]\nanswer = max(cands, key=lambda w: cosine(vec[w], target))\nprint(target, answer)",
         "check": "ok(answer == '여왕', '왕 - 남자 + 여자 ≈ 여왕')"},
    ],
}

W3 = {
    "file": "nlp_w3_practice.ipynb",
    "title": "3주차 직접 해보기: 신경망, 역전파, 언어 모델",
    "intro": ("사이트의 3주차 회독과 정리 슬라이드를 본 다음 풀어요. 위에서부터 차례로 `Shift+Enter` 로 실행해요.\n\n"
              "- `# TODO` 칸의 `None` 을 알맞은 코드나 값으로 바꾸고, 바로 아래 **확인 셀**을 실행해요.\n"
              "- 막히면 맨 아래 **정답 코드**를 봐요.\n\n"
              "Colab 에는 PyTorch 가 이미 깔려 있어요. GPU 는 필요 없어요."),
    "setup": "import math\nimport torch\n" + CHECK_HEAD + "print('PyTorch', torch.__version__)",
    "ex": [
        {"md": "## 1. 뉴런 하나 계산하기\n\n강의 N3 p.9-10, 기초 다지기 9단원. 뉴런 = **가중합(입력 x 가중치를 모두 더함) + 편향 항(bias term)** 다음에 **활성화 함수**. ReLU 는 음수면 0, 양수면 그대로예요.",
         "todo": "x = [1.0, 2.0, -1.0]\nw = [0.5, -0.25, 1.0]\nb = 0.5\n\nz = sum(xi * wi for xi, wi in zip(x, w)) + b\nh = None   # TODO: ReLU(z) = max(0, z)\nprint(z, h)",
         "sol": "x = [1.0, 2.0, -1.0]\nw = [0.5, -0.25, 1.0]\nb = 0.5\n\nz = sum(xi * wi for xi, wi in zip(x, w)) + b\nh = max(0.0, z)\nprint(z, h)",
         "check": "ok(abs(z - (-0.5)) < 1e-9, '0.5 - 0.5 - 1.0 + 0.5 = -0.5')\nok(h == 0.0, '음수라서 ReLU 를 지나면 0')"},
        {"md": "## 2. 비선형이 없으면 층을 쌓아도 한 층\n\n강의 N3 p.11. 활성화 함수 없이 `W2 @ (W1 @ x)` 를 계산하면 `(W2 @ W1) @ x`, 곧 행렬 하나를 곱한 것과 같아요. `@` 는 행렬 곱이에요.",
         "todo": "torch.manual_seed(0)\nW1 = torch.randn(4, 3)\nW2 = torch.randn(2, 4)\nx = torch.randn(3)\n\ntwo_layers = W2 @ (W1 @ x)\nW = None   # TODO: 두 행렬을 미리 곱한 한 행렬\none_layer = W @ x\nprint(two_layers, one_layer, W.shape)",
         "sol": "torch.manual_seed(0)\nW1 = torch.randn(4, 3)\nW2 = torch.randn(2, 4)\nx = torch.randn(3)\n\ntwo_layers = W2 @ (W1 @ x)\nW = W2 @ W1\none_layer = W @ x\nprint(two_layers, one_layer, W.shape)",
         "check": "ok(torch.allclose(two_layers, one_layer, atol=1e-5), '두 층 = 한 층')\nok(tuple(W.shape) == (2, 3), '(2,4) @ (4,3) = (2,3)')"},
        {"md": "## 3. shape 먼저 예측하기\n\n강의 N3 p.25-26, 실습 N3L p.3. `(행, 열) @ (열,)` 은 `(행,)` 이 돼요. 앞 행렬의 열 수와 뒤 벡터 길이가 같아야 곱할 수 있어요. 코드를 돌리기 **전에** 튜플로 답을 적어요.",
         "todo": "x = torch.randn(5)\nW = torch.randn(3, 5)\nb = torch.randn(3)\nu = torch.randn(3)\n\nz = W @ x + b\ns = u @ torch.tanh(z)\n\nmy_z_shape = None   # TODO: 예: (7,)\nmy_s_shape = None   # TODO: 숫자 하나(스칼라)는 ()",
         "sol": "x = torch.randn(5)\nW = torch.randn(3, 5)\nb = torch.randn(3)\nu = torch.randn(3)\n\nz = W @ x + b\ns = u @ torch.tanh(z)\n\nmy_z_shape = (3,)\nmy_s_shape = ()",
         "check": "ok(tuple(z.shape) == my_z_shape, 'z 는 (3,)')\nok(tuple(s.shape) == my_s_shape, 's 는 스칼라 ()')"},
        {"md": "## 4. 손으로 미분한 값과 autograd 비교\n\n강의 N3 p.18, p.32, 실습 N3L p.4. f(x) = 3x² + 5x 이면 f'(x) = 6x + 5 예요. `requires_grad=True` 로 만든 텐서에 `backward()` 를 부르면 PyTorch 가 `x.grad` 에 기울기를 넣어 줘요.",
         "todo": "x = torch.tensor(1.0, requires_grad=True)\nf = 3 * x**2 + 5 * x\nf.backward()\n\nby_hand = None   # TODO: x=1 에서 6x + 5 의 값\nprint(x.grad.item(), by_hand)",
         "sol": "x = torch.tensor(1.0, requires_grad=True)\nf = 3 * x**2 + 5 * x\nf.backward()\n\nby_hand = 6 * 1.0 + 5\nprint(x.grad.item(), by_hand)",
         "check": "ok(abs(x.grad.item() - by_hand) < 1e-6 and by_hand == 11, 'autograd 와 손계산 모두 11')"},
        {"md": "## 5. 연쇄 법칙\n\n강의 N3 p.20-24. f = (2x + 1)² 를 u = 2x + 1, f = u² 로 나누면 df/dx = (df/du) x (du/dx) = 2u x 2 예요.",
         "todo": "x = torch.tensor(1.0, requires_grad=True)\nu = 2 * x + 1\nf = u ** 2\nf.backward()\n\ndf_du = None   # TODO: 2u 의 값 (u = 3)\ndu_dx = None   # TODO: 2x + 1 을 x 로 미분한 값\nprint(x.grad.item(), df_du * du_dx)",
         "sol": "x = torch.tensor(1.0, requires_grad=True)\nu = 2 * x + 1\nf = u ** 2\nf.backward()\n\ndf_du = 2 * 3.0\ndu_dx = 2.0\nprint(x.grad.item(), df_du * du_dx)",
         "check": "ok(df_du * du_dx == 12 and abs(x.grad.item() - 12) < 1e-6, '6 x 2 = 12')"},
        {"md": "## 6. 계산 그래프 노드 직관: +, max, x\n\n강의 N3 p.30. 위에서 내려온 기울기가 1일 때,\n\n- **+** 는 기울기를 두 입력에 그대로 나눠 줘요.\n- **max** 는 더 큰 입력 쪽에만 보내요(작은 쪽은 0).\n- **x** 는 서로 상대편 값을 곱해 줘요.\n\nf = (x + y) x max(z, w), x=1, y=2, z=3, w=-1 에서 네 기울기를 손으로 적어요.",
         "todo": "grads_by_hand = {'x': None, 'y': None, 'z': None, 'w': None}   # TODO\n\nx = torch.tensor(1.0, requires_grad=True)\ny = torch.tensor(2.0, requires_grad=True)\nz = torch.tensor(3.0, requires_grad=True)\nw = torch.tensor(-1.0, requires_grad=True)\nf = (x + y) * torch.maximum(z, w)\nf.backward()\nauto = {'x': x.grad.item(), 'y': y.grad.item(), 'z': z.grad.item(), 'w': w.grad.item()}\nprint(auto)",
         "sol": "grads_by_hand = {'x': 3.0, 'y': 3.0, 'z': 3.0, 'w': 0.0}\n\nx = torch.tensor(1.0, requires_grad=True)\ny = torch.tensor(2.0, requires_grad=True)\nz = torch.tensor(3.0, requires_grad=True)\nw = torch.tensor(-1.0, requires_grad=True)\nf = (x + y) * torch.maximum(z, w)\nf.backward()\nauto = {'x': x.grad.item(), 'y': y.grad.item(), 'z': z.grad.item(), 'w': w.grad.item()}\nprint(auto)",
         "check": "ok(all(abs(auto[k] - grads_by_hand[k]) < 1e-6 for k in auto), 'x, y 는 max(z,w)=3, z 는 x+y=3, w 는 작은 쪽이라 0')"},
        {"md": "## 7. 바이그램(2-gram) 언어 모델: 세어서 확률 구하기\n\n강의 N3 p.37-38. P(다음 단어 | 앞 단어) = count(앞 단어, 다음 단어) / count(앞 단어). 문장 앞뒤에 `<s>`, `</s>` 를 붙였어요.",
         "todo": "from collections import Counter\nsents = [['<s>', '나는', '영화', '를', '봤다', '</s>'],\n         ['<s>', '나는', '책', '을', '봤다', '</s>'],\n         ['<s>', '너는', '영화', '를', '봤다', '</s>']]\n\nuni = Counter(w for s in sents for w in s[:-1])\nbi = Counter((s[i], s[i + 1]) for s in sents for i in range(len(s) - 1))\n\ndef p(nxt, prev):\n    return None   # TODO: bi[(prev, nxt)] / uni[prev]\n\nprint(p('나는', '<s>'), p('영화', '나는'))",
         "sol": "from collections import Counter\nsents = [['<s>', '나는', '영화', '를', '봤다', '</s>'],\n         ['<s>', '나는', '책', '을', '봤다', '</s>'],\n         ['<s>', '너는', '영화', '를', '봤다', '</s>']]\n\nuni = Counter(w for s in sents for w in s[:-1])\nbi = Counter((s[i], s[i + 1]) for s in sents for i in range(len(s) - 1))\n\ndef p(nxt, prev):\n    return bi[(prev, nxt)] / uni[prev]\n\nprint(p('나는', '<s>'), p('영화', '나는'))",
         "check": "ok(abs(p('나는', '<s>') - 2 / 3) < 1e-9, '<s> 3번 중 나는 2번')\nok(abs(p('영화', '나는') - 0.5) < 1e-9, '나는 2번 중 영화 1번')\nok(p('책', '너는') == 0, '한 번도 안 센 쌍은 0: 희소성 문제(N3 p.39)')"},
        {"md": "## 8. 퍼플렉서티(Perplexity)\n\n강의 N3 p.41-42. 모델이 정답 토큰에 준 확률이 p1, ..., pN 이면\n\nPPL = exp( -(1/N) x (log p1 + ... + log pN) ) = (p1 x ... x pN)^(-1/N)\n\n낮을수록 좋아요. 모든 토큰에 확률 1/4 를 주면 PPL 은 4, 곧 '평균 4개 후보 사이에서 헷갈리는 정도'예요.",
         "todo": "probs = [0.5, 0.25, 0.125, 0.5]\n\nmean_nll = -sum(math.log(q) for q in probs) / len(probs)\nppl = None   # TODO: math.exp 사용\n\nprint(round(mean_nll, 4), round(ppl, 4))",
         "sol": "probs = [0.5, 0.25, 0.125, 0.5]\n\nmean_nll = -sum(math.log(q) for q in probs) / len(probs)\nppl = math.exp(mean_nll)\n\nprint(round(mean_nll, 4), round(ppl, 4))",
         "check": "ok(abs(ppl - (0.5 * 0.25 * 0.125 * 0.5) ** (-1 / 4)) < 1e-9, '두 식이 같은 값')\nok(abs(ppl - 2 ** 1.75) < 1e-9, 'PPL = 2^1.75 = 약 3.364')"},
        {"md": "## 9. RNN 한 걸음\n\n강의 N3 p.47, 실습 N3L p.10. h_t = tanh(W_h h_(t-1) + W_e e_t + b). 은닉 상태 2칸, 임베딩 2칸짜리 아주 작은 예예요.",
         "todo": "W_h = torch.tensor([[0.5, 0.0], [0.0, 0.5]])\nW_e = torch.tensor([[1.0, 0.0], [0.0, -1.0]])\nb = torch.tensor([0.0, 0.0])\nh0 = torch.tensor([0.0, 0.0])\ne1 = torch.tensor([1.0, 1.0])\n\nh1 = None   # TODO: 위 식 그대로 (torch.tanh, @ 사용)\nprint(h1)",
         "sol": "W_h = torch.tensor([[0.5, 0.0], [0.0, 0.5]])\nW_e = torch.tensor([[1.0, 0.0], [0.0, -1.0]])\nb = torch.tensor([0.0, 0.0])\nh0 = torch.tensor([0.0, 0.0])\ne1 = torch.tensor([1.0, 1.0])\n\nh1 = torch.tanh(W_h @ h0 + W_e @ e1 + b)\nprint(h1)",
         "check": "ok(torch.allclose(h1, torch.tensor([math.tanh(1.0), math.tanh(-1.0)])), 'h1 = [tanh(1), tanh(-1)] = [0.7616, -0.7616]')"},
        {"md": "## 10. 기울기 소실, 폭발, 클리핑\n\n강의 N3 p.52-53. 1보다 작은 수를 여러 번 곱하면 0에 가까워지고(소실), 1보다 큰 수를 여러 번 곱하면 아주 커져요(폭발). **기울기 클리핑(Gradient Clipping)** 은 기울기 벡터의 길이가 기준보다 길면 방향은 두고 길이만 기준으로 줄여요.",
         "todo": "vanish = 0.5 ** 20\nexplode = 1.5 ** 20\n\ng = [3.0, 4.0]\nthreshold = 1.0\nlength = math.sqrt(sum(v * v for v in g))\nclipped = None   # TODO: length > threshold 이면 각 값에 threshold / length 를 곱한 리스트\nprint(vanish, round(explode, 1), clipped)",
         "sol": "vanish = 0.5 ** 20\nexplode = 1.5 ** 20\n\ng = [3.0, 4.0]\nthreshold = 1.0\nlength = math.sqrt(sum(v * v for v in g))\nclipped = [v * threshold / length for v in g] if length > threshold else g\nprint(vanish, round(explode, 1), clipped)",
         "check": "ok(vanish < 1e-6 and explode > 3000, '0.5^20 은 약 0.00000095, 1.5^20 은 약 3325')\nok(all(abs(a - b) < 1e-9 for a, b in zip(clipped, [0.6, 0.8])), '길이 5 를 1 로: [0.6, 0.8]')"},
    ],
}



W4 = {
    "file": "nlp_w4_practice.ipynb",
    "title": "4주차 직접 해보기: 어텐션과 트랜스포머",
    "intro": ("사이트의 4주차 회독과 정리 슬라이드를 본 다음 풀어요. 위에서부터 차례로 `Shift+Enter` 로 실행해요.\n\n"
              "- 문제마다 **생각 순서**가 먼저 나와요. 코드를 치기 전에 그 순서를 말로 한 번 읊어요.\n"
              "- `# TODO` 가 있는 칸의 `None` 을 알맞은 코드로 바꿔요.\n"
              "- 바로 아래 **확인 셀**을 실행하면 맞았는지 알려 줘요. 틀리면 빨간 AssertionError 와 힌트가 나와요.\n"
              "- 막히면 맨 아래 **정답 코드**를 봐요.\n\n"
              "GPU 는 필요 없어요. 인터넷 다운로드도 없어요."),
    "setup": "import math\nimport numpy as np\nimport torch\nimport torch.nn as nn\ntorch.manual_seed(0)\n" + CHECK_HEAD + "print('준비 끝')",
    "ex": [
        {"md": "## 1. 1단계: 내적으로 어텐션 점수 만들기\n\n강의 N4 p.21. 지금 디코더 상태 s 를 인코더 상태 h 하나하나와 **내적(Dot Product)** 해서 점수를 만들어요. 점수가 크면 그 자리가 지금 중요하다는 뜻이에요.\n\n`H @ s` 는 H 의 각 줄과 s 를 내적한 결과를 한 번에 줘요.",
         "think": ["점수는 몇 개 나와야 하나요? 인코더 상태 개수만큼, 곧 4개",
                   "점수 하나 = s 와 h 를 같은 자리끼리 곱해서 더하기",
                   "for 문으로 쓰면: for h in H: score = sum(s[i] * h[i] for i in ...)",
                   "행렬로 쓰면 그 for 문이 H @ s 한 줄이 돼요",
                   "모양 확인: (4, 2) @ (2,) -> (4,)"],
         "todo": "s = np.array([1.0, 2.0])\nH = np.array([[3.0, 0.3],\n              [0.4, 0.2],\n              [0.1, 0.2],\n              [0.2, 0.1]])\n\nscores = None   # TODO: H 의 각 줄과 s 의 내적\n\nprint(scores, scores.shape)",
         "sol": "s = np.array([1.0, 2.0])\nH = np.array([[3.0, 0.3],\n              [0.4, 0.2],\n              [0.1, 0.2],\n              [0.2, 0.1]])\n\nscores = H @ s\n\nprint(scores, scores.shape)",
         "check": "ok(scores.shape == (4,), '점수는 인코더 상태 개수만큼 4개')\nok(np.allclose(scores, [3.6, 0.8, 0.5, 0.4]), '점수 [3.6, 0.8, 0.5, 0.4]')\nok(int(np.argmax(scores)) == 0, '첫 자리가 가장 관련이 커요')"},

        {"md": "## 2. 2단계: 소프트맥스를 직접 만들기\n\n강의 N4 p.22. 점수는 합이 1 이 아니라서 그대로 가중치로 못 써요. **소프트맥스(Softmax)** 로 합이 1 인 분포를 만들어요.\n\n큰 수에 `exp` 를 씌우면 값이 넘칠 수 있어서, 먼저 최댓값을 빼 주는 게 안전한 구현이에요. 빼도 결과는 똑같아요.",
         "think": ["최댓값을 빼요. 결과는 안 변하고 넘침만 막아요",
                   "각 값에 exp 를 씌워요",
                   "전체 합으로 나눠요",
                   "말로 하면 빼기, exp, 합으로 나누기 세 줄이에요",
                   "확인: 결과를 다 더하면 정확히 1 이어야 해요"],
         "todo": "def softmax(x):\n    x = x - x.max()            # 넘침 막기\n    e = None                   # TODO: exp 씌우기\n    return None                # TODO: 전체 합으로 나누기\n\nalpha = softmax(np.array([2.0, 1.0, 0.0]))\nprint(alpha, alpha.sum())",
         "sol": "def softmax(x):\n    x = x - x.max()            # 넘침 막기\n    e = np.exp(x)\n    return e / e.sum()\n\nalpha = softmax(np.array([2.0, 1.0, 0.0]))\nprint(alpha, alpha.sum())",
         "check": "ok(abs(alpha.sum() - 1.0) < 1e-12, '다 더하면 1')\nok(np.allclose(alpha, [0.6652, 0.2447, 0.0900], atol=1e-4), '[0.6652, 0.2447, 0.0900]')\nok(np.allclose(softmax(np.array([2.0, 1.0, 0.0]) + 100), alpha), '전체에 상수를 더해도 결과가 같아요')"},

        {"md": "## 3. 3단계: 가중합으로 문맥 벡터 만들기\n\n강의 N4 p.23. 가중치를 각 상태에 곱해서 모두 더하면 **문맥 벡터(Context Vector)** 가 나와요. 가중치 합이 1 이므로 가중 평균이에요.",
         "think": ["문맥 벡터의 칸 수는 상태 하나와 같아요, 곧 2칸",
                   "for 문으로 쓰면 c = alpha[0]*h0 + alpha[1]*h1 + alpha[2]*h2",
                   "행렬로 쓰면 (3,) @ (3, 2) -> (2,)",
                   "가중치가 큰 자리의 내용이 많이 들어갔는지 눈으로 확인해요"],
         "todo": "alpha3 = np.array([0.5, 0.3, 0.2])\nHs = np.array([[2.0, 0.0],\n               [0.0, 2.0],\n               [1.0, 1.0]])\n\ncontext = None   # TODO: 가중합\n\nprint(context)",
         "sol": "alpha3 = np.array([0.5, 0.3, 0.2])\nHs = np.array([[2.0, 0.0],\n               [0.0, 2.0],\n               [1.0, 1.0]])\n\ncontext = alpha3 @ Hs\n\nprint(context)",
         "check": "ok(context.shape == (2,), '문맥 벡터는 상태 하나와 같은 2칸')\nok(np.allclose(context, [1.2, 0.8]), '[1.2, 0.8]')\nok(np.allclose(np.array([0.5, 0.3, 0.2]) @ Hs, context), '가중치 합이 1 이라 가중 평균이에요')"},

        {"md": "## 4. 왜 루트 d 로 나눌까\n\n강의 N4 p.38. 점수가 커질수록 소프트맥스가 뾰족해져요. 뾰족해지면 **기울기(Gradient)** 가 거의 0 이 돼서 학습이 멈춰요. 그래서 점수를 $\\sqrt{d_k}$ 로 나눠요.",
         "think": ["같은 점수로 두 번 계산해 보면 돼요",
                   "그냥 소프트맥스를 하고 최댓값을 봐요",
                   "sqrt(d_k) 로 나눈 뒤 소프트맥스를 하고 최댓값을 봐요",
                   "d_k = 4 이니까 나누는 값은 2 예요",
                   "어느 쪽이 더 평평해졌는지 숫자로 비교해요"],
         "todo": "raw = np.array([4.0, 2.0, 0.0])\nd_k = 4\n\nunscaled = softmax(raw)\nscaled = None   # TODO: raw 를 math.sqrt(d_k) 로 나눈 뒤 softmax\n\nprint(unscaled.max(), scaled.max())",
         "sol": "raw = np.array([4.0, 2.0, 0.0])\nd_k = 4\n\nunscaled = softmax(raw)\nscaled = softmax(raw / math.sqrt(d_k))\n\nprint(unscaled.max(), scaled.max())",
         "check": "ok(abs(unscaled.max() - 0.8668) < 1e-3, '나누기 전 최대 가중치 약 0.8668')\nok(abs(scaled.max() - 0.6652) < 1e-3, '나눈 뒤 최대 가중치 약 0.6652')\nok(scaled.max() < unscaled.max(), '나누면 분포가 덜 뾰족해져요')"},

        {"md": "## 5. 한 입력에서 Q, K, V 만들기\n\n강의 N4 p.34. 토큰 하나가 **쿼리(Query)**, **키(Key)**, **밸류(Value)** 세 역할을 동시에 해요. 같은 입력 X 에 서로 다른 행렬 세 개를 곱해서 만들어요. 세 행렬은 모든 자리가 함께 써요.",
         "think": ["X 의 모양은 (토큰 수, 입력 칸 수) = (3, 4) 예요",
                   "W 의 모양은 (입력 칸 수, 결과 칸 수) = (4, 2) 예요",
                   "(3, 4) @ (4, 2) -> (3, 2). 가운데 4 가 맞아야 곱할 수 있어요",
                   "Q, K, V 세 번 똑같이 하면 끝이에요",
                   "여기서는 K 를 만드는 행렬이 Q 와 같게 준비돼 있어요"],
         "todo": "X  = np.array([[1.0, 0.0, 1.0, 0.0],\n               [0.0, 1.0, 0.0, 1.0],\n               [1.0, 1.0, 0.0, 0.0]])\nWq = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 0.0], [0.0, 1.0]])\nWk = Wq.copy()\nWv = np.array([[1.0, 1.0], [1.0, 0.0], [0.0, 1.0], [0.0, 0.0]])\n\nQ = None   # TODO\nK = None   # TODO\nV = None   # TODO\n\nprint(Q.shape, K.shape, V.shape)\nprint(Q)",
         "sol": "X  = np.array([[1.0, 0.0, 1.0, 0.0],\n               [0.0, 1.0, 0.0, 1.0],\n               [1.0, 1.0, 0.0, 0.0]])\nWq = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 0.0], [0.0, 1.0]])\nWk = Wq.copy()\nWv = np.array([[1.0, 1.0], [1.0, 0.0], [0.0, 1.0], [0.0, 0.0]])\n\nQ = X @ Wq\nK = X @ Wk\nV = X @ Wv\n\nprint(Q.shape, K.shape, V.shape)\nprint(Q)",
         "check": "ok(Q.shape == (3, 2) and K.shape == (3, 2) and V.shape == (3, 2), '셋 다 (3, 2)')\nok(np.allclose(Q, [[2, 0], [0, 2], [1, 1]]), 'Q = [[2,0],[0,2],[1,1]]')\nok(np.allclose(V, [[1, 2], [1, 0], [2, 1]]), 'V = [[1,2],[1,0],[2,1]]')"},

        {"md": "## 6. 셀프 어텐션을 행렬 한 번에\n\n강의 N4 p.36-37. $\\mathrm{Attention}(Q,K,V) = \\mathrm{softmax}(QK^{\\top}/\\sqrt{d_k})V$. 자리를 도는 for 문이 없어서 GPU 가 아주 잘해요.\n\n줄마다 소프트맥스를 해야 하므로 `axis=1` 로 합이 1 이 되게 만들어요.",
         "think": ["먼저 모양을 종이에 적어요. Q 는 (3,2), K 전치는 (2,3), 점수는 (3,3)",
                   "점수를 sqrt(d_k) 로 나눠요. 여기서 d_k 는 Q 의 칸 수 2 예요",
                   "줄마다 소프트맥스를 하면 A 는 (3,3) 이고 줄 합이 각각 1 이에요",
                   "A @ V 는 (3,3) @ (3,2) = (3,2) 예요",
                   "마지막 줄은 점수가 모두 같아서 가중치가 3분의 1 씩 나올 거예요"],
         "todo": "def row_softmax(M):\n    M = M - M.max(axis=1, keepdims=True)\n    e = np.exp(M)\n    return e / e.sum(axis=1, keepdims=True)\n\nd_k = Q.shape[1]\nS = None   # TODO: Q 와 K 전치를 곱하고 math.sqrt(d_k) 로 나누기 (K.T 사용)\nA = None   # TODO: 줄마다 소프트맥스\nO = None   # TODO: 가중치로 V 를 섞기\n\nprint(A.round(4))\nprint(O.round(4))",
         "sol": "def row_softmax(M):\n    M = M - M.max(axis=1, keepdims=True)\n    e = np.exp(M)\n    return e / e.sum(axis=1, keepdims=True)\n\nd_k = Q.shape[1]\nS = Q @ K.T / math.sqrt(d_k)\nA = row_softmax(S)\nO = A @ V\n\nprint(A.round(4))\nprint(O.round(4))",
         "check": "ok(S.shape == (3, 3) and A.shape == (3, 3) and O.shape == (3, 2), '점수와 A 는 (3,3), 출력은 (3,2)')\nok(np.allclose(A.sum(axis=1), 1.0), '줄마다 합이 1')\nok(np.allclose(A[0], [0.7679, 0.0454, 0.1867], atol=1e-4), '첫 줄 [0.7679, 0.0454, 0.1867]')\nok(np.allclose(A[2], [1/3, 1/3, 1/3]), '셋째 줄은 점수가 모두 같아 3분의 1 씩')"},

        {"md": "## 7. 배리어 3: 미래 가리기\n\n강의 N4 p.43. **언어 모델(Language Model (LM))** 은 아직 만들지 않은 토큰을 보면 안 돼요. 미래 자리의 점수를 **소프트맥스 전에** 마이너스 무한으로 바꿔요. `exp(-inf)` 가 0 이라 가중치가 정확히 0 이 돼요.\n\n`np.triu(np.ones((n, n)), 1)` 는 대각선 위쪽만 1 인 표를 만들어요.",
         "think": ["가려야 하는 칸은 j 가 i 보다 큰 곳, 곧 오른쪽 위 삼각형이에요",
                   "np.triu(..., 1) 로 그 자리를 찾아요",
                   "그 자리 점수를 -np.inf 로 바꿔요. 0 으로 바꾸면 안 돼요",
                   "그다음에 줄마다 소프트맥스를 해요",
                   "확인: 첫 줄은 [1, 0, 0] 이고 모든 줄 합이 1 이에요"],
         "todo": "raw_scores = np.array([[2.0, 1.0, 0.0],\n                       [1.0, 2.0, 1.0],\n                       [0.0, 1.0, 2.0]])\n\nfuture = np.triu(np.ones((3, 3)), 1) == 1\nmasked = None   # TODO: future 자리를 -np.inf 로 (np.where 사용)\nAm = None       # TODO: 줄마다 소프트맥스\n\nprint(Am.round(4))",
         "sol": "raw_scores = np.array([[2.0, 1.0, 0.0],\n                       [1.0, 2.0, 1.0],\n                       [0.0, 1.0, 2.0]])\n\nfuture = np.triu(np.ones((3, 3)), 1) == 1\nmasked = np.where(future, -np.inf, raw_scores)\nAm = row_softmax(masked)\n\nprint(Am.round(4))",
         "check": "ok(np.allclose(Am.sum(axis=1), 1.0), '마스크를 씌워도 줄마다 합은 정확히 1')\nok(np.allclose(Am[0], [1.0, 0.0, 0.0]), '첫 줄은 자기 자신만 봐요')\nok(np.allclose(Am[1], [0.2689, 0.7311, 0.0], atol=1e-4), '둘째 줄 [0.2689, 0.7311, 0]')\nok(np.allclose(np.triu(Am, 1), 0.0), '오른쪽 위가 전부 정확히 0')"},

        {"md": "## 8. 멀티 헤드: 나누고, 보고, 이어 붙이기\n\n강의 N4 p.47-48. 전체 차원 d 를 헤드 h 개로 나눠서 d/h 차원에서 각각 어텐션을 해요. 결과를 이어 붙이고 $W^O$ 로 섞어요.\n\n핵심은 `reshape` 으로 (배치, 토큰, d) 를 (배치, 헤드, 토큰, d/h) 로 바꾸는 것이에요.",
         "think": ["d = 8, h = 2 이니까 헤드 하나의 차원은 8 나누기 2 로 4 예요",
                   "(1, 3, 8) 을 (1, 3, 2, 4) 로 reshape 하면 헤드가 갈라져요",
                   "그다음 transpose 로 (1, 2, 3, 4), 곧 (배치, 헤드, 토큰, 칸) 으로 바꿔요",
                   "파라미터 수는 Linear(8, 8) 하나가 가중치 64 더하기 편향 8 로 72 개예요",
                   "Q, K, V, O 네 개면 72 곱하기 4 로 288 개. 헤드를 몇 개로 나눠도 이 수는 그대로예요"],
         "todo": "d, h, n = 8, 2, 3\nhead_dim = None   # TODO: d 를 h 로 나눈 값 (//)\n\nx = torch.arange(float(n * d)).reshape(1, n, d)\nsplit = x.reshape(1, n, h, head_dim).transpose(1, 2)   # (배치, 헤드, 토큰, 칸)\n\nWq, Wk, Wv, Wo = (nn.Linear(d, d) for _ in range(4))\nn_params = None   # TODO: 네 Linear 의 파라미터 수를 모두 더하기 (p.numel() 사용)\n\nprint(head_dim, tuple(split.shape), n_params)",
         "sol": "d, h, n = 8, 2, 3\nhead_dim = d // h\n\nx = torch.arange(float(n * d)).reshape(1, n, d)\nsplit = x.reshape(1, n, h, head_dim).transpose(1, 2)   # (배치, 헤드, 토큰, 칸)\n\nWq, Wk, Wv, Wo = (nn.Linear(d, d) for _ in range(4))\nn_params = sum(p.numel() for L in (Wq, Wk, Wv, Wo) for p in L.parameters())\n\nprint(head_dim, tuple(split.shape), n_params)",
         "check": "ok(head_dim == 4, '헤드 하나의 차원은 d 나누기 h 로 4')\nok(tuple(split.shape) == (1, 2, 3, 4), '(배치, 헤드, 토큰, 칸) = (1, 2, 3, 4)')\nok(n_params == 288, '네 Linear 합쳐 288개. 헤드 수와 상관없어요')\nok(torch.allclose(split.transpose(1, 2).reshape(1, n, d), x), '되돌리면 원래 x 와 같아요. 이게 이어 붙이기예요')"},

        {"md": "## 9. 사인 코사인 위치 인코딩 만들기\n\n강의 N4 p.40. $PE_{pos,2i} = \\sin(pos/10000^{2i/d})$, $PE_{pos,2i+1} = \\cos(pos/10000^{2i/d})$.\n\n짝수 칸은 sin, 홀수 칸은 cos 이에요. 학습하는 값이 아니라 계산하는 값이라 **파라미터(Parameter)** 가 0 개예요.",
         "think": ["만들 표의 모양은 (자리 수, d) = (3, 4) 예요",
                   "칸 쌍마다 각도가 달라요. 각도는 pos 나누기 10000의 (2i/d) 제곱이에요",
                   "짝수 칸 [:, 0::2] 에 sin, 홀수 칸 [:, 1::2] 에 cos 을 넣어요",
                   "자리 0 은 sin(0)=0, cos(0)=1 이라 (0, 1, 0, 1) 이 나와야 해요",
                   "두 자리의 벡터가 서로 다른지 확인하면 순서가 살아난 거예요"],
         "todo": "def sinusoidal_pe(max_len, d_model):\n    pe = torch.zeros(max_len, d_model)\n    pos = torch.arange(max_len).unsqueeze(1).float()\n    div = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))\n    pe[:, 0::2] = None   # TODO: sin\n    pe[:, 1::2] = None   # TODO: cos\n    return pe\n\nP = sinusoidal_pe(3, 4)\nprint(P)",
         "sol": "def sinusoidal_pe(max_len, d_model):\n    pe = torch.zeros(max_len, d_model)\n    pos = torch.arange(max_len).unsqueeze(1).float()\n    div = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))\n    pe[:, 0::2] = torch.sin(pos * div)\n    pe[:, 1::2] = torch.cos(pos * div)\n    return pe\n\nP = sinusoidal_pe(3, 4)\nprint(P)",
         "check": "ok(tuple(P.shape) == (3, 4), '(자리 3개, 칸 4개)')\nok(torch.allclose(P[0], torch.tensor([0.0, 1.0, 0.0, 1.0]), atol=1e-5), '자리 0 은 (0, 1, 0, 1)')\nok(torch.allclose(P[1][:2], torch.tensor([0.8415, 0.5403]), atol=1e-3), '자리 1 의 앞 두 칸 (0.8415, 0.5403)')\nok(not torch.allclose(P[1], P[2]), '자리마다 값이 달라서 순서를 구별할 수 있어요')"},

        {"md": "## 10. 층 정규화와 Pre-LN 블록\n\n강의 N4 p.50-51. **층 정규화(Layer Normalization (LayerNorm))** 는 한 토큰의 숫자들을 평균 0, 분산 1 로 맞춰요. 토큰끼리도 배치끼리도 섞지 않아요.\n\nPre-LN 블록은 `x = x + Attention(LN(x))` 다음에 `x = x + FFN(LN(x))` 예요. 이 더하기가 **잔차 연결(Residual Connection)** 이에요.",
         "think": ["먼저 손으로 해요. x = (2, 4, 4, 10) 의 평균은 20 나누기 4 로 5 예요",
                   "편차는 (-3, -1, -1, 5), 제곱 평균인 분산은 36 나누기 4 로 9, 표준편차는 3 이에요",
                   "정규화 결과는 (-1, -1/3, -1/3, 5/3) 이에요",
                   "블록은 더하기 두 번이에요. x + f(LN(x)) 를 두 번 해요",
                   "모양은 절대 바뀌지 않아요. 들어간 모양 그대로 나와요"],
         "todo": "x = torch.tensor([2.0, 4.0, 4.0, 10.0])\nln = nn.LayerNorm(4, elementwise_affine=False)\n\nby_hand = None   # TODO: (x - 평균) / 표준편차. x.mean(), x.std(unbiased=False) 사용\n\nd = 4\nblock_ln1, block_ln2 = nn.LayerNorm(d), nn.LayerNorm(d)\nffn = nn.Sequential(nn.Linear(d, 4 * d), nn.ReLU(), nn.Linear(4 * d, d))\nattn = nn.Linear(d, d)   # 어텐션 자리에 넣은 가짜 층\n\nh = x.reshape(1, 1, d)\nh = None   # TODO: h + attn(block_ln1(h))\nh = h + ffn(block_ln2(h))\n\nprint(by_hand, tuple(h.shape))",
         "sol": "x = torch.tensor([2.0, 4.0, 4.0, 10.0])\nln = nn.LayerNorm(4, elementwise_affine=False)\n\nby_hand = (x - x.mean()) / x.std(unbiased=False)\n\nd = 4\nblock_ln1, block_ln2 = nn.LayerNorm(d), nn.LayerNorm(d)\nffn = nn.Sequential(nn.Linear(d, 4 * d), nn.ReLU(), nn.Linear(4 * d, d))\nattn = nn.Linear(d, d)   # 어텐션 자리에 넣은 가짜 층\n\nh = x.reshape(1, 1, d)\nh = h + attn(block_ln1(h))\nh = h + ffn(block_ln2(h))\n\nprint(by_hand, tuple(h.shape))",
         "check": "ok(torch.allclose(by_hand, torch.tensor([-1.0, -1/3, -1/3, 5/3]), atol=1e-5), '손계산 (-1, -0.3333, -0.3333, 1.6667)')\nok(torch.allclose(by_hand, ln(x), atol=1e-4), 'PyTorch LayerNorm 과 같은 값')\nok(abs(float(by_hand.mean())) < 1e-5 and abs(float((by_hand ** 2).mean()) - 1.0) < 1e-4, '평균 0, 분산 1')\nok(tuple(h.shape) == (1, 1, 4), '블록을 지나도 모양은 그대로 (1, 1, 4)')"},
    ],
}


WB = {
    "file": "nlp_wb_practice.ipynb",
    "title": "기초 다지기 직접 해보기: 수학과 파이썬 열 단원",
    "intro": ("기초 다지기 주차의 정리 슬라이드 열 단원을 한 문제씩 손으로 옮겨 보는 연습이에요. 파이썬을 한 줄도 안 써 봤어도 괜찮아요.\n\n"
              "- 문제마다 **생각 순서**가 먼저 나와요. 코드를 치기 전에 그 순서를 말로 한 번 읊어요.\n"
              "- 여러 줄을 새로 쓰는 문제에는 **의사코드**가 따로 붙어 있어요. 의사코드 한 줄이 파이썬 한 줄이 돼요.\n"
              "- `# TODO` 가 있는 칸의 `None` 을 알맞은 코드나 값으로 바꿔요.\n"
              "- 바로 아래 **확인 셀**을 실행하면 맞았는지 알려 줘요. 틀리면 빨간 AssertionError 와 힌트가 나와요.\n"
              "- 막히면 맨 아래 **정답 코드**를 봐요. 모범 의사코드도 거기 같이 있어요.\n\n"
              "여기 나오는 숫자는 거의 다 정리 슬라이드의 손계산에 그대로 적혀 있어요. 답이 안 맞으면 그 슬라이드를 다시 봐요. "
              "1번부터 7번까지는 파이썬만, 3번과 6번과 9번은 넘파이, 10번만 PyTorch 를 써요. GPU 도 다운로드도 필요 없어요."),
    "setup": "import math\nfrom collections import Counter\nimport numpy as np\nimport torch\n" + CHECK_HEAD + "print('준비 끝')",
    "ex": [
        {"md": "## 1. 벡터는 숫자 목록, 차원은 칸의 개수\n\n기초 1단원. **벡터(Vector)** 는 숫자를 순서대로 적은 목록이고, 파이썬에서는 대괄호로 적어요. `a = [2, 1]` 이에요.\n\n**차원(Dimension)** 은 칸이 몇 개인지, 곧 `len(a)` 예요. 더하기는 같은 자리끼리만 해요. **원-핫 벡터(One-hot Vector)** 는 자기 자리만 1 이고 나머지는 모두 0 인 목록이에요.\n\n숫자는 슬라이드 손계산 1 과 손계산 3 에 그대로 있어요.",
         "think": ["벡터는 리스트로 적어요. a = [2, 1] 이면 칸이 두 개예요",
                   "차원은 칸의 개수예요. len(a) 가 바로 그 답이에요",
                   "더하기는 첫 칸은 첫 칸끼리, 둘째 칸은 둘째 칸끼리예요. 자리가 섞이지 않아요",
                   "원-핫 벡터는 단어 목록에서 그 단어의 번호 자리만 1 로 켜요",
                   "모텔과 호텔을 같은 자리끼리 곱해서 더하면 0 이 나와야 해요"],
         "pseudo": ["a 와 b 를 리스트로 적는다",
                    "차원 = a 의 칸 개수",
                    "a + b = [첫 칸끼리 더한 값, 둘째 칸끼리 더한 값]",
                    "모텔 벡터와 호텔 벡터를 같은 자리끼리 곱해서 모두 더한다"],
         "next": "N2 p.23-25 에서 단어를 기호로만 다루면 **원-핫 벡터** 가 되고, p.25 슬라이드가 motel 과 hotel 의 값이 0 이라고 적어요. 그 한계 때문에 N2 p.26-27 의 **단어 벡터** 가 나오고, N4 p.40 에서는 그 임베딩 벡터에 위치 벡터를 더해서 트랜스포머에 넣어요.",
         "todo": "a = [2, 1]\nb = [1, 3]\n\ndim = None         # TODO: a 의 차원. 칸이 몇 개인지 (len 사용)\na_plus_b = None    # TODO: 같은 자리끼리 더한 리스트. [첫 칸 합, 둘째 칸 합]\ntwo_a = [2 * v for v in a]\n\nvocab = ['개', '고양이', '모텔', '호텔', '사과']\n\ndef onehot(word):\n    i = vocab.index(word)\n    return [1 if k == i else 0 for k in range(len(vocab))]\n\nmotel = onehot('모텔')\nhotel = onehot('호텔')\nsame = None        # TODO: motel 과 hotel 을 같은 자리끼리 곱해서 모두 더하기 (sum 과 zip)\n\nprint(dim, a_plus_b, two_a)\nprint(motel, hotel, same)",
         "sol": "a = [2, 1]\nb = [1, 3]\n\ndim = len(a)\na_plus_b = [a[0] + b[0], a[1] + b[1]]\ntwo_a = [2 * v for v in a]\n\nvocab = ['개', '고양이', '모텔', '호텔', '사과']\n\ndef onehot(word):\n    i = vocab.index(word)\n    return [1 if k == i else 0 for k in range(len(vocab))]\n\nmotel = onehot('모텔')\nhotel = onehot('호텔')\nsame = sum(x * y for x, y in zip(motel, hotel))\n\nprint(dim, a_plus_b, two_a)\nprint(motel, hotel, same)",
         "check": "ok(dim == 2, '(2, 1) 은 칸이 2개라 2차원')\nok(a_plus_b == [3, 4], '(2,1) + (1,3) = (3,4). 슬라이드 손계산 1 과 같아요')\nok(two_a == [4, 2], '스칼라 배는 칸마다 똑같이 곱해요')\nok(motel == [0, 0, 1, 0, 0] and hotel == [0, 0, 0, 1, 0], '원-핫 벡터는 자기 자리만 1')\nok(same == 0, '모텔과 호텔은 뜻이 비슷한데 값이 0. 원-핫 벡터는 비슷함을 전혀 못 담아요')"},

        {"md": "## 2. 내적, 길이, 코사인 유사도를 함수로\n\n기초 2단원. **내적(Dot Product)** 은 같은 자리끼리 곱해서 모두 더한 값이고 답은 숫자 하나예요. **노름(Norm)** 은 칸마다 제곱해서 더한 뒤 루트를 씌운 길이예요. **코사인 유사도(Cosine Similarity)** 는 내적을 두 길이의 곱으로 나눈 값이에요.\n\n마지막 칸에서는 찾는 벡터 하나를 후보 셋과 내적해서 점수를 매겨요. 이 점수가 4주차의 **어텐션 점수(Attention Score)** 예요.",
         "think": ["내적은 자리마다 곱한 값을 모두 더하기예요. zip 이 두 리스트를 자리별로 짝지어 줘요",
                   "노름은 자기 자신과의 내적에 루트예요. dot(u, u) 에 math.sqrt 를 씌우면 끝이에요",
                   "코사인은 내적을 두 노름의 곱으로 나누기예요. 함수 두 개를 이미 만들어 뒀으니 한 줄이에요",
                   "점수 매기기는 후보마다 내적 한 번이에요. 리스트 내포로 한 줄에 써요",
                   "확인: (3,2)와 (1,4) 는 11, (3,4) 의 길이는 5, (3,4)와 (4,3) 의 코사인은 0.96"],
         "pseudo": ["dot(u, v) = 자리마다 u 와 v 를 곱한 값을 모두 더한다",
                    "norm(u) = dot(u, u) 에 루트를 씌운다",
                    "cosine(u, v) = dot(u, v) 를 norm(u) 곱하기 norm(v) 로 나눈다",
                    "점수 = 후보마다 dot(q, 후보)",
                    "가장 큰 점수의 자리 번호를 찾는다"],
         "pseudo_first": True,
         "pseudo_show": True,
         "next": "N2 p.47-48 에서 단어 벡터를 평가할 때 사람 점수와 코사인 유사도를 견주고, 단어 유추도 코사인이 가장 큰 단어를 골라요. N4 p.21 은 the simplest score is a dot product 라고 적어요. 여기 만든 `dot` 이 그 어텐션 점수이고, N4 p.38 에서 그 값을 루트 $d_k$ 로 나눠요.",
         "todo": "def dot(u, v):\n    return None        # TODO: 같은 자리끼리 곱해서 모두 더하기 (sum 과 zip)\n\ndef norm(u):\n    return None        # TODO: 자기 자신과의 내적에 루트 (math.sqrt)\n\ndef cosine(u, v):\n    return None        # TODO: 내적을 두 노름의 곱으로 나누기\n\nprint(dot([3, 2], [1, 4]), norm([3, 4]), round(cosine([3, 4], [4, 3]), 4))\n\nq = [1, 2]\nkeys = [[2, 0], [0, 3], [1, 1]]\nscores = [dot(q, k) for k in keys]\nbest = scores.index(max(scores))\nprint(scores, best)",
         "sol": "def dot(u, v):\n    return sum(x * y for x, y in zip(u, v))\n\ndef norm(u):\n    return math.sqrt(dot(u, u))\n\ndef cosine(u, v):\n    return dot(u, v) / (norm(u) * norm(v))\n\nprint(dot([3, 2], [1, 4]), norm([3, 4]), round(cosine([3, 4], [4, 3]), 4))\n\nq = [1, 2]\nkeys = [[2, 0], [0, 3], [1, 1]]\nscores = [dot(q, k) for k in keys]\nbest = scores.index(max(scores))\nprint(scores, best)",
         "check": "ok(dot([3, 2], [1, 4]) == 11, '3x1 + 2x4 = 11. 슬라이드 손계산 1 과 같아요')\nok(norm([3, 4]) == 5.0, '9 + 16 = 25, 루트를 씌우면 5')\nok(abs(cosine([3, 4], [4, 3]) - 0.96) < 1e-9, '24 나누기 25 = 0.96')\nok(abs(cosine([1, 0], [0, 1])) < 1e-12, '직각이면 코사인도 내적도 0')\nok(scores == [2, 6, 3], '어텐션 점수는 2, 6, 3')\nok(best == 1, '가장 큰 점수는 두 번째 후보. 이 고르기가 어텐션의 1단계예요')"},

        {"md": "## 3. shape 을 먼저 적고 나서 곱하기\n\n기초 3단원. **행렬(Matrix)** 의 **모양(Shape)** 은 언제나 (행, 열) 순서예요. 곱셈 규칙은 `(a, b) @ (b, c) -> (a, c)` 하나예요. 가운데가 같아야 곱할 수 있고, 그 숫자는 사라져요.\n\n코드를 돌리기 **전에** 답을 튜플로 적어요. 교수님이 3주차에 transpose 위치를 외우기보다 shape 을 맞춘다고 생각하라고 했어요.",
         "think": ["A 는 (2, 3), x 는 (3,) 이에요. 가운데 3 이 같으니 곱할 수 있어요",
                   "가운데 3 이 사라지고 바깥 2 만 남아요. 그래서 A @ x 는 (2,) 예요",
                   "Q 와 K 는 둘 다 (3, 2) 예요. 그냥 곱하면 2 와 3 이 달라서 안 돼요",
                   "K 를 전치하면 (2, 3) 이 되고, (3,2) @ (2,3) 은 (3,3) 이에요",
                   "멀티 헤드는 전체 칸 수를 헤드 수로 나누는 것뿐이에요. 512 를 8 로 나눠요"],
         "pseudo": ["A @ x 의 모양을 먼저 종이에 적는다: (2,3) 과 (3,) 이니 (2,)",
                    "실제로 곱해서 값을 본다",
                    "Q 와 K 의 모양을 적는다: 둘 다 (3,2)",
                    "K 를 전치해서 (2,3) 으로 만들고 Q 와 곱한다",
                    "헤드 하나의 칸 수 = 전체 칸 수 나누기 헤드 수"],
         "next": "N3 p.25-26 이 전치와 shape 맞추기, 기울기의 shape 은 파라미터와 같아야 한다는 쪽이에요. N4 p.37 에서 $Q @ K^{\\top}$ 가 만드는 $(n, n)$ 점수 행렬이 여기 만든 `S` 이고, N4 p.47 의 멀티 헤드가 $d = 512$ 를 $h = 8$ 로 나눠 64 칸씩 쓰는 그 나눗셈이에요. 과제 2(N3 p.57)에서 word2vec 기울기를 손으로 구할 때 첫 번째 검산도 이 shape 확인이에요.",
         "todo": "A = np.array([[1.0, 2.0, 3.0],\n              [4.0, 5.0, 6.0]])\nx = np.array([1.0, 0.0, 2.0])\n\nAx = A @ x\nmy_Ax_shape = None     # TODO: 돌리기 전에 튜플로 적어요. 칸이 하나면 (7,) 처럼 써요\n\nQ = np.array([[2.0, 0.0],\n              [0.0, 2.0],\n              [1.0, 1.0]])\nK = Q.copy()\nS = None               # TODO: Q 와 K 의 전치를 곱하기 (K.T 사용)\nmy_S_shape = None      # TODO: S 의 모양\n\nd, h = 512, 8\nhead_dim = None        # TODO: 헤드 하나가 쓰는 칸 수 (// 사용)\n\nprint(Ax, tuple(S.shape), head_dim)",
         "sol": "A = np.array([[1.0, 2.0, 3.0],\n              [4.0, 5.0, 6.0]])\nx = np.array([1.0, 0.0, 2.0])\n\nAx = A @ x\nmy_Ax_shape = (2,)\n\nQ = np.array([[2.0, 0.0],\n              [0.0, 2.0],\n              [1.0, 1.0]])\nK = Q.copy()\nS = Q @ K.T\nmy_S_shape = (3, 3)\n\nd, h = 512, 8\nhead_dim = d // h\n\nprint(Ax, tuple(S.shape), head_dim)",
         "check": "ok(np.allclose(Ax, [7.0, 16.0]), 'A @ x = (7, 16). 줄마다 내적 한 번씩이에요')\nok(tuple(Ax.shape) == my_Ax_shape == (2,), '(2,3) @ (3,) 은 (2,). 가운데 3 이 사라져요')\nok(tuple(S.shape) == my_S_shape == (3, 3), '(3,2) @ (2,3) = (3,3). 단어끼리 전부 비교한 표예요')\nok(np.allclose(S, [[4, 0, 2], [0, 4, 2], [2, 2, 2]]), 'S 의 값은 [[4,0,2],[0,4,2],[2,2,2]]')\nok(head_dim == 64, 'd = 512 를 h = 8 로 나누면 헤드마다 64 칸')"},

        {"md": "## 4. 로그가 곱을 합으로 바꿔요\n\n기초 4단원. $\\exp$ 는 어떤 수든 양수로 바꿔 줘요. **로그(Logarithm)** 는 그 반대이고, 이 과목에서 $\\log$ 라고만 적혀 있으면 **자연로그(Natural Logarithm)** 예요.\n\n오늘의 핵심 한 줄은 $\\log(xy) = \\log x + \\log y$ 예요. 확률을 계속 곱하면 0 으로 뭉개지지만, 로그를 씌우면 더하기가 되어 멀쩡해요.",
         "think": ["exp(0) 은 1, exp(1) 은 약 2.718, exp(2) 는 약 7.389 예요",
                   "곱한 뒤 로그를 씌운 값과, 따로 로그를 씌워 더한 값이 같은지 봐요",
                   "단어 20개 문장에서 단어마다 확률이 0.1 이면 전체는 0.1 을 20번 곱한 값이에요",
                   "로그로 바꾸면 ln 0.1 을 20번 더하는 것이 돼요. 곱하기가 더하기가 됐어요",
                   "퍼플렉서티는 평균 손실을 exp 에 넣은 값이에요. 후보 4개에 0.25 씩 주면 4 가 나와야 해요"],
         "pseudo": ["exp 값 세 개를 구한다",
                    "log(0.5) 더하기 log(0.25) 와 log(0.5 곱하기 0.25) 를 견준다",
                    "문장 로그 확률 = log(0.1) 곱하기 20",
                    "손실 = 정답 확률의 음의 로그",
                    "퍼플렉서티 = exp(손실)"],
         "next": "N3 p.41-42 의 **퍼플렉서티** 가 바로 $\\exp$(교차 엔트로피 손실) 이에요. N2 p.30-31 에서 word2vec 의 우도는 확률의 곱이고 로그를 씌워 합으로 만든 뒤 손실로 써요. N4 p.13 의 **빔 서치** 도 로그 확률을 더해서 점수를 매기고 길이로 나눠요.",
         "todo": "e0, e1, e2 = math.exp(0), math.exp(1), math.exp(2)\n\nlog_prod = math.log(0.5 * 0.25)\nlog_sum = None      # TODO: math.log(0.5) 와 math.log(0.25) 를 더하기\n\nlogp = None         # TODO: 확률 0.1 짜리 단어 20개. math.log(0.1) 에 20 을 곱해요\n\nloss = -math.log(0.25)\nppl = None          # TODO: 손실을 exp 에 넣기\n\nprint(round(e2, 3), round(log_sum, 3), round(logp, 2), round(ppl, 4))",
         "sol": "e0, e1, e2 = math.exp(0), math.exp(1), math.exp(2)\n\nlog_prod = math.log(0.5 * 0.25)\nlog_sum = math.log(0.5) + math.log(0.25)\n\nlogp = 20 * math.log(0.1)\n\nloss = -math.log(0.25)\nppl = math.exp(loss)\n\nprint(round(e2, 3), round(log_sum, 3), round(logp, 2), round(ppl, 4))",
         "check": "ok(abs(e0 - 1.0) < 1e-12 and abs(e2 - 7.389) < 1e-3, 'exp(0) 은 1, exp(2) 는 약 7.389')\nok(abs(log_sum - log_prod) < 1e-12, 'log(xy) = log x + log y. 곱이 합이 돼요')\nok(abs(log_sum - (-2.079)) < 1e-3, '두 값 모두 약 -2.079')\nok(abs(logp - (-46.05)) < 0.01, '0.1 을 20번 곱한 값은 로그로 -46.05. 그냥 곱하면 0 으로 뭉개져요')\nok(abs(ppl - 4.0) < 1e-9, '후보 4개에 0.25 씩 준 모델의 퍼플렉서티는 4')"},

        {"md": "## 5. 말뭉치에서 세어서 확률 구하기\n\n기초 5단원. **확률(Probability)** 은 일어난 횟수를 전체 횟수로 나눈 값이에요. 조건을 붙이면 세는 범위가 그 안으로 좁아져요. 이것이 **조건부 확률(Conditional Probability)** 이에요.\n\n`Counter` 는 목록에 무엇이 몇 번 나왔는지 세 주는 도구예요. 여기 말뭉치에서는 '나는' 과 '밥을' 이 문장 끝에 오는 일이 없어서 분모를 그냥 `uni[prev]` 로 써도 돼요.",
         "think": ["단어를 모두 세요. 4문장에 3단어씩이니 12개예요",
                   "단어 하나의 확률은 그 단어 횟수를 12 로 나눈 값이에요",
                   "조건부 확률은 분모가 좁아져요. '밥을' 뒤를 볼 때 분모는 12 가 아니라 3 이에요",
                   "붙어 있는 두 단어를 세려면 문장마다 (i 번째, i+1 번째) 짝을 만들어요",
                   "문장 확률은 곱의 규칙으로 한 단어씩 곱해 나가요"],
         "pseudo": ["uni = 단어마다 몇 번 나왔는지 센다",
                    "bi = 붙어 있는 두 단어 짝이 몇 번 나왔는지 센다",
                    "total = uni 의 값을 모두 더한다",
                    "p_word(w) = uni[w] 를 total 로 나눈다",
                    "p_next(다음, 앞) = bi[(앞, 다음)] 을 uni[앞] 으로 나눈다",
                    "문장 확률 = p_word(첫 단어) 곱하기 p_next(...) 곱하기 p_next(...)"],
         "pseudo_first": True,
         "pseudo_show": True,
         "next": "N3 p.35-38 의 **엔그램 언어 모델** 이 바로 이 세어서 나누기예요. 여기서 `zero` 가 0 으로 나오는 것이 N3 p.39 의 희소성 문제이고, 그 때문에 N3 p.43 부터 신경망 언어 모델로 넘어가요. N4 p.10 의 디코더도 원문이 주어졌을 때의 조건부 확률 언어 모델이에요.",
         "todo": "corpus = [['나는', '밥을', '먹었다'],\n          ['나는', '빵을', '먹었다'],\n          ['나는', '밥을', '지었다'],\n          ['너는', '밥을', '먹었다']]\n\nuni = Counter(w for s in corpus for w in s)\nbi = Counter((s[i], s[i + 1]) for s in corpus for i in range(len(s) - 1))\n\ntotal = None                # TODO: 단어가 모두 몇 개인지. sum(uni.values())\n\ndef p_word(w):\n    return None             # TODO: uni[w] 를 total 로 나누기\n\ndef p_next(nxt, prev):\n    return None             # TODO: bi[(prev, nxt)] 를 uni[prev] 로 나누기\n\nsent_p = None               # TODO: p_word('나는') 과 p_next('밥을', '나는') 과 0.5 를 모두 곱하기\nzero = p_next('빵을', '밥을')\n\nprint(total, round(p_word('빵을'), 4), round(p_next('먹었다', '밥을'), 4))\nprint(round(sent_p, 4), zero)",
         "sol": "corpus = [['나는', '밥을', '먹었다'],\n          ['나는', '빵을', '먹었다'],\n          ['나는', '밥을', '지었다'],\n          ['너는', '밥을', '먹었다']]\n\nuni = Counter(w for s in corpus for w in s)\nbi = Counter((s[i], s[i + 1]) for s in corpus for i in range(len(s) - 1))\n\ntotal = sum(uni.values())\n\ndef p_word(w):\n    return uni[w] / total\n\ndef p_next(nxt, prev):\n    return bi[(prev, nxt)] / uni[prev]\n\nsent_p = p_word('나는') * p_next('밥을', '나는') * 0.5\nzero = p_next('빵을', '밥을')\n\nprint(total, round(p_word('빵을'), 4), round(p_next('먹었다', '밥을'), 4))\nprint(round(sent_p, 4), zero)",
         "check": "ok(total == 12, '4문장에 3단어씩이라 모두 12개')\nok(abs(p_word('빵을') - 1 / 12) < 1e-12, '빵을 은 12개 중 1번이라 1/12, 약 0.083')\nok(abs(p_next('먹었다', '밥을') - 2 / 3) < 1e-12, '밥을 3번 중 먹었다가 2번이라 0.667')\nok(abs(p_next('지었다', '밥을') - 1 / 3) < 1e-12, '밥을 3번 중 지었다가 1번. 둘을 더하면 정확히 1 이에요')\nok(abs(sent_p - 1 / 12) < 1e-12, '0.25 x 0.667 x 0.5 = 1/12, 약 0.083')\nok(zero == 0, '밥을 빵을 은 한 번도 안 나와서 0. 이게 N3 p.39 의 희소성 문제예요')"},

        {"md": "## 6. 소프트맥스로 확률을 만들고 교차 엔트로피로 벌점을 매기기\n\n기초 6단원. **소프트맥스(Softmax)** 는 두 줄이에요. exp 를 씌우고, 전체 합으로 나눠요. 모든 점수에서 최댓값을 똑같이 빼도 답이 변하지 않아서, 그렇게 하면 큰 수에서 넘치는 일을 막을 수 있어요.\n\n**교차 엔트로피(Cross-Entropy)** 는 정답 자리에 준 확률의 **음의 로그(Negative Log)** 예요. 정답에 자신 있으면 벌점이 작고, 자신 있게 틀리면 벌점이 커요.",
         "think": ["최댓값을 빼요. 결과는 안 변하고 넘침만 막아요",
                   "각 점수에 exp 를 씌워요",
                   "전체 합으로 나눠요. 여기까지가 소프트맥스예요",
                   "교차 엔트로피는 정답 자리 확률 하나만 보고 음의 로그를 씌워요",
                   "확인: 점수 2, 1, 0 은 확률 0.665, 0.245, 0.090 이 되고 벌점은 0.408 과 2.408 이에요"],
         "pseudo": ["softmax(z):",
                    "  z 에서 z 의 최댓값을 뺀다",
                    "  각 칸에 exp 를 씌운다",
                    "  전체 합으로 나눠서 돌려준다",
                    "cross_entropy(p, y):",
                    "  정답 자리 확률 p[y] 에 로그를 씌우고 마이너스를 붙인다"],
         "pseudo_first": True,
         "pseudo_show": True,
         "next": "N2 p.32-33 에서 내적 점수를 소프트맥스로 확률로 바꾸는 것이 word2vec 의 마지막 조각이에요. N4 p.22 의 어텐션 2단계가 바로 이 `softmax` 이고, 교수님이 어텐션에서 가장 중요하다고 한 네 단계 중 하나예요. N4 p.38 은 점수가 너무 크면 이 분포가 뾰족해져서 기울기가 사라진다고 말해요.",
         "todo": "def softmax(z):\n    z = z - z.max()     # 최댓값 빼기. 답은 그대로고 넘침만 막아요\n    e = None            # TODO: exp 씌우기 (np.exp)\n    return None         # TODO: 전체 합으로 나누기 (e.sum())\n\ndef cross_entropy(p, y):\n    return None         # TODO: 정답 자리 확률의 음의 로그 (np.log 사용)\n\nz = np.array([2.0, 1.0, 0.0])\np = softmax(z)\nloss_A = cross_entropy(p, 0)\nloss_C = cross_entropy(p, 2)\n\nprint(p.round(3), round(float(loss_A), 3), round(float(loss_C), 3))",
         "sol": "def softmax(z):\n    z = z - z.max()     # 최댓값 빼기. 답은 그대로고 넘침만 막아요\n    e = np.exp(z)\n    return e / e.sum()\n\ndef cross_entropy(p, y):\n    return -np.log(p[y])\n\nz = np.array([2.0, 1.0, 0.0])\np = softmax(z)\nloss_A = cross_entropy(p, 0)\nloss_C = cross_entropy(p, 2)\n\nprint(p.round(3), round(float(loss_A), 3), round(float(loss_C), 3))",
         "check": "ok(abs(p.sum() - 1.0) < 1e-12, '확률을 다 더하면 정확히 1')\nok(np.allclose(p, [0.665, 0.245, 0.090], atol=1e-3), '점수 2, 1, 0 이 확률 0.665, 0.245, 0.090 이 돼요')\nok(np.allclose(softmax(z + 100), p), '모든 점수에 같은 수를 더해도 결과가 같아요. 점수 차이만 중요해요')\nok(abs(float(loss_A) - 0.408) < 1e-3, '정답이 A 면 벌점 0.408')\nok(abs(float(loss_C) - 2.408) < 1e-3, '정답이 C 면 벌점 2.408. 자신 있게 틀리면 크게 혼나요')\nok(abs(float(loss_C - loss_A) - 2.0) < 1e-9, '벌점 차이 2 는 점수 차이 2 빼기 0 과 정확히 같아요')"},

        {"md": "## 7. 살짝 움직여 기울기 재기, 그리고 연쇄 법칙\n\n기초 7단원. **미분(Derivative)** 은 x 를 아주 조금 움직였을 때 y 가 바뀌는 비율이에요. 그래서 `(f(x + h) - f(x)) / h` 에서 h 를 작게 줄이면 미분 값에 다가가요.\n\n**연쇄 법칙(Chain Rule)** 은 단계마다의 기울기를 곱해서 잇는 규칙이에요. **편미분(Partial Derivative)** 은 하나만 움직이고 나머지는 상수처럼 두는 것이에요.",
         "think": ["기울기 재기는 세로 변화를 가로 변화로 나누기예요",
                   "h 를 0.01 로 하면 6.01, 더 작게 하면 6 에 다가가요",
                   "미분 규칙 네 개만 쓰면 돼요. 상수는 0, x제곱은 2x, x세제곱은 3x제곱, 상수배와 합은 그대로",
                   "연쇄 법칙은 dy/du 와 du/dx 를 각각 구해서 곱하기예요",
                   "편미분은 한 변수만 움직여요. 나머지는 숫자처럼 취급해요"],
         "pseudo": ["slope(f, x, h) = (f(x 더하기 h) 빼기 f(x)) 를 h 로 나눈다",
                    "g 프라임 = 10x 더하기 3x제곱 에 x = 2 를 넣는다",
                    "u = 3x 더하기 1 을 먼저 계산한다",
                    "dy/du = 2u, du/dx = 3",
                    "dy/dx = dy/du 곱하기 du/dx"],
         "pseudo_first": True,
         "pseudo_show": True,
         "next": "N3 p.18-24 가 연쇄 법칙과 야코비안이고, 교수님이 3주차에 연쇄 법칙이 가장 중요하다고 했어요. N3 p.30 의 더하기, max, 곱하기 노드가 기울기를 흘리는 방식도 같은 규칙이에요. 무엇보다 과제 2(N3 p.57)가 word2vec 기울기를 손으로 유도하는 문제인데, 그 핵심이 소프트맥스에 이 연쇄 법칙을 쓰는 것이에요.",
         "todo": "def slope(f, x, hstep):\n    return None        # TODO: (f(x + hstep) - f(x)) / hstep\n\nsq = lambda t: t * t\nnear = slope(sq, 3.0, 0.01)\n\ng_prime_at_2 = None    # TODO: g(t) = 5t^2 + t^3 이면 g'(t) = 10t + 3t^2. t = 2 를 넣은 값\n\nu = 3 * 1 + 1\ndy_du = None           # TODO: y = u^2 이니 2u. u 는 위에서 구했어요\ndu_dx = None           # TODO: u = 3x + 1 을 x 로 미분한 값\ndy_dx = dy_du * du_dx\n\ndF_dx = 2 * 2 + 3 * 1  # F = x^2 + 3xy 를 x 로 편미분하면 2x + 3y, (2, 1) 을 넣었어요\ndF_dy = None           # TODO: F 를 y 로 편미분하면 3x. (2, 1) 에서의 값\n\nprint(near, g_prime_at_2, dy_dx, dF_dx, dF_dy)",
         "sol": "def slope(f, x, hstep):\n    return (f(x + hstep) - f(x)) / hstep\n\nsq = lambda t: t * t\nnear = slope(sq, 3.0, 0.01)\n\ng_prime_at_2 = 10 * 2 + 3 * 2 ** 2\n\nu = 3 * 1 + 1\ndy_du = 2 * u\ndu_dx = 3\ndy_dx = dy_du * du_dx\n\ndF_dx = 2 * 2 + 3 * 1\ndF_dy = 3 * 2\n\nprint(near, g_prime_at_2, dy_dx, dF_dx, dF_dy)",
         "check": "ok(abs(near - 6.01) < 1e-6, 'x = 3 에서 0.01 만큼 움직이면 6.01 이 나와요')\nok(abs(slope(sq, 3.0, 1e-7) - 6.0) < 1e-5, '움직이는 양을 아주 작게 줄이면 미분 값 6 에 다가가요')\nok(g_prime_at_2 == 32, '10x2 = 20, 3x4 = 12, 더하면 32')\nok(dy_du == 8 and du_dx == 3 and dy_dx == 24, '2u x 3 = 8 x 3 = 24. 펼쳐서 18x + 6 에 x = 1 을 넣어도 24 예요')\nok(dF_dx == 7 and dF_dy == 6, '편미분은 하나만 움직여요. 7 과 6 이에요')"},

        {"md": "## 8. 경사 하강법 한 걸음씩 내려가기\n\n기초 8단원. **경사 하강법(Gradient Descent)** 한 걸음은 `w <- w - alpha * 기울기` 예요. 기울기는 올라갈 방향이라서 빼요. `alpha` 가 **학습률(Learning Rate)**, 곧 보폭이에요.\n\n여기서는 $L(w) = w^2$ 라서 기울기가 $2w$ 예요. 보폭을 1.5 로 키우면 내려가기는커녕 튕겨 나가는 것도 같이 봐요.",
         "think": ["기울기는 2w 예요. 함수 한 줄로 만들어 두면 반복이 쉬워요",
                   "한 걸음은 지금 w 에서 alpha 곱하기 기울기를 빼는 것이에요",
                   "세 걸음을 걸으려면 같은 일을 세 번 반복해요. for 문이 그 일을 해 줘요",
                   "걸음마다 w 를 기록해 두면 4, 2, 1, 0.5 로 줄어드는 게 보여요",
                   "보폭 1.5 로 같은 자리에서 시작하면 -8, 16 으로 커져요. 보폭이 크면 발산해요"],
         "pseudo": ["step(w, alpha):",
                    "  기울기 = 2 곱하기 w",
                    "  새 w = w 빼기 alpha 곱하기 기울기",
                    "w 를 4 에서 시작해 같은 일을 세 번 반복하고 기록한다",
                    "보폭만 1.5 로 바꿔서 두 번 반복하고 기록한다",
                    "한 에폭의 걸음 수 = 데이터 개수 나누기 미니배치 크기"],
         "pseudo_first": True,
         "pseudo_show": True,
         "next": "N2 p.35 가 경사 하강법과 보폭 $\\alpha$, N2 p.36 이 미니배치를 쓰는 **확률적 경사 하강법** 이에요. N3 p.17 의 신경망 학습도 같은 방식이고, 3주차 실습 N3L p.12 의 학습 루프가 이 `for` 문 그대로예요. 과제 2 에서 스킵그램을 구현할 때도 이 걸음을 돌려요.",
         "todo": "def step(w, alpha):\n    grad = None        # TODO: L(w) = w^2 의 기울기, 곧 2w\n    return None        # TODO: w 에서 alpha 곱하기 grad 를 빼기\n\nw = 4.0\npath = [w]\nfor _ in range(3):\n    w = step(w, 0.25)\n    path.append(w)\n\nbig = [4.0]\nfor _ in range(2):\n    big.append(step(big[-1], 1.5))\n\nn_data, batch = 1000, 100\nsteps_per_epoch = None   # TODO: 한 에폭에 몇 걸음인지 (// 사용)\n\nprint(path)\nprint(big, steps_per_epoch)",
         "sol": "def step(w, alpha):\n    grad = 2 * w\n    return w - alpha * grad\n\nw = 4.0\npath = [w]\nfor _ in range(3):\n    w = step(w, 0.25)\n    path.append(w)\n\nbig = [4.0]\nfor _ in range(2):\n    big.append(step(big[-1], 1.5))\n\nn_data, batch = 1000, 100\nsteps_per_epoch = n_data // batch\n\nprint(path)\nprint(big, steps_per_epoch)",
         "check": "ok(path == [4.0, 2.0, 1.0, 0.5], 'w 가 4, 2, 1, 0.5 로 줄어요. 슬라이드 손계산 2 와 같아요')\nok([v * v for v in path] == [16.0, 4.0, 1.0, 0.25], '손실은 16, 4, 1, 0.25 로 줄어요')\nok(big == [4.0, -8.0, 16.0], '보폭 1.5 면 -8, 16 으로 튕겨 나가요. 손실은 64, 256 이에요')\nok(steps_per_epoch == 10, '1000 을 100 으로 나누면 한 에폭에 10 걸음, 3 에폭이면 30 걸음')"},

        {"md": "## 9. 뉴런 한 줄과 순전파 한 번\n\n기초 9단원. **뉴런(Neuron)** 하나는 **가중합(Weighted Sum)** 에 **편향 항(Bias Term)** 을 더하고 **활성화 함수(Activation Function)** 로 한 번 구부린 것이에요.\n\n여기서는 뉴런 셋을 한 층으로 모아 한 번에 계산하고, **렐루(ReLU)** 를 지나 마지막 한 칸으로 줄여요. 입력에서 출력까지 앞으로 한 번 계산하는 것이 **순전파(Forward Pass)** 예요. 마지막 칸에서는 활성화 함수가 없으면 층을 쌓아도 한 층이라는 것도 확인해요.",
         "think": ["층 하나를 행렬 곱 한 번으로 써요. W1 은 (3, 2), x 는 (2,) 라서 결과는 (3,)",
                   "거기에 편향 항 b1 을 더해요. 칸마다 하나씩 더해져요",
                   "렐루는 음수를 0 으로 눌러요. -1 이 0 이 되고 5 와 2 는 그대로예요",
                   "둘째 층은 칸이 하나뿐이라 내적 한 번에 편향을 더하면 끝이에요",
                   "마지막은 시그모이드라 0 과 1 사이 값, 곧 확률처럼 읽을 수 있어요",
                   "직선 두 개를 이으면 y = 2t + 1 다음 z = 3y - 2 가 결국 z = 6t + 1 한 줄이에요"],
         "pseudo": ["z1 = W1 과 x 를 행렬 곱 하고 b1 을 더한다",
                    "h1 = z1 을 렐루에 통과시킨다",
                    "z2 = w2 와 h1 의 내적에 b2 를 더한다",
                    "out = z2 를 시그모이드에 넣는다",
                    "직선 두 개를 하나로 합치면 6t 더하기 1 이라고 적는다"],
         "pseudo_first": True,
         "pseudo_show": False,
         "next": "N3 p.9-10 이 뉴런과 활성화 함수이고, 교수님이 렐루가 딥러닝에서 가장 중요한 함수 중 하나라고 했어요. N3 p.11 이 여기 마지막 칸에서 확인한 것, 곧 비선형성이 없으면 탑 전체가 한 층으로 무너진다는 내용이에요. N3 p.44 의 고정 윈도우 신경망 언어 모델이 정확히 이 구조이고, N4 p.42 의 트랜스포머 위치별 피드포워드 신경망도 2층짜리 같은 구조예요.",
         "todo": "def relu(v):\n    return np.maximum(0.0, v)\n\ndef sigmoid(t):\n    return 1.0 / (1.0 + math.exp(-t))\n\nx = np.array([1.0, 2.0])\nW1 = np.array([[1.0, -1.0],\n               [0.0, 2.0],\n               [1.0, 1.0]])\nb1 = np.array([0.0, 1.0, -1.0])\nw2 = np.array([1.0, -1.0, 2.0])\nb2 = 0.5\n\nz1 = None        # TODO: W1 과 x 의 행렬 곱에 b1 을 더하기\nh1 = None        # TODO: z1 을 렐루에 통과시키기\nz2 = None        # TODO: w2 와 h1 의 내적에 b2 를 더하기 (w2 @ h1)\nout = sigmoid(float(z2))\n\nlin = lambda t: 3 * (2 * t + 1) - 2\ncollapsed = None  # TODO: 위 두 직선을 하나로 합친 식. lambda t: 로 시작해요\n\nprint(z1, h1, round(float(z2), 4), round(out, 4))\nprint(lin(2), collapsed(2))",
         "sol": "def relu(v):\n    return np.maximum(0.0, v)\n\ndef sigmoid(t):\n    return 1.0 / (1.0 + math.exp(-t))\n\nx = np.array([1.0, 2.0])\nW1 = np.array([[1.0, -1.0],\n               [0.0, 2.0],\n               [1.0, 1.0]])\nb1 = np.array([0.0, 1.0, -1.0])\nw2 = np.array([1.0, -1.0, 2.0])\nb2 = 0.5\n\nz1 = W1 @ x + b1\nh1 = relu(z1)\nz2 = w2 @ h1 + b2\nout = sigmoid(float(z2))\n\nlin = lambda t: 3 * (2 * t + 1) - 2\ncollapsed = lambda t: 6 * t + 1\n\nprint(z1, h1, round(float(z2), 4), round(out, 4))\nprint(lin(2), collapsed(2))",
         "check": "ok(np.allclose(z1, [-1.0, 5.0, 2.0]), '가중합에 편향 항을 더하면 (-1, 5, 2)')\nok(np.allclose(h1, [0.0, 5.0, 2.0]), '렐루가 음수 -1 을 0 으로 눌러요')\nok(abs(float(z2) - (-0.5)) < 1e-12, '0 - 5 + 4 = -1 에 편향 0.5 를 더해 -0.5')\nok(abs(out - 0.3775) < 1e-4, '시그모이드에 넣으면 약 0.3775, 곧 약 38 퍼센트')\nok(all(lin(t) == collapsed(t) for t in (0, 1, 2, 5)), '직선 두 층은 결국 6t + 1 한 층이에요. 그래서 비선형성이 필요해요')"},

        {"md": "## 10. 실습 노트북에 나오는 파이썬과 PyTorch\n\n기초 10단원. 실습 탭 코드에 계속 나오는 것만 모았어요. **리스트(List)** 의 칸 번호는 0 부터이고, `Counter` 는 무엇이 몇 번 나왔는지 세 줘요.\n\n골뱅이 `@` 는 같은 자리끼리 곱하기가 아니라 **행렬 곱(Matrix Multiplication)** 이에요. `requires_grad=True` 로 만든 텐서에 `backward()` 를 부르면 **자동 미분(Automatic Differentiation (Autodiff))** 이 기울기를 대신 구해 줘요. 손으로 구한 값과 같은지 꼭 견줘 봐요.",
         "think": ["칸 번호는 0 부터라서 h[1] 이 둘째 칸이에요",
                   "Counter 에 목록을 넣으면 무엇이 몇 번인지 세 줘요",
                   "W 는 (3, 2), x 는 (2,) 라서 골뱅이 곱의 결과는 (3,) 이에요",
                   "f = x세제곱 + 2x 를 손으로 미분하면 3x제곱 + 2 예요",
                   "x = 2 를 넣으면 3 곱하기 4 더하기 2 로 14 예요. autograd 도 14 가 나와야 해요"],
         "pseudo": ["h 의 둘째 칸과 칸 개수를 읽는다",
                    "Counter 로 단어를 센다",
                    "z = W 골뱅이 x",
                    "x 를 requires_grad 로 만들고 f 를 계산한 뒤 backward 를 부른다",
                    "손으로 미분한 3x제곱 더하기 2 에 x = 2 를 넣어 견준다"],
         "pseudo_first": True,
         "pseudo_show": False,
         "next": "2주차 실습 N2L p.9-10 이 딕셔너리로 만든 말뭉치와 Counter 로 짝 세기, 3주차 실습 N3L p.3 이 shape 찍어 보기와 골뱅이, p.4 가 requires_grad 와 backward 예요. 저장된 출력도 14.0 이에요. N3L p.12 의 학습 루프가 그 기울기로 8번 문제의 걸음을 걷고, 4주차 실습 N4L 은 같은 문법으로 쿼리, 키, 밸류를 만들어요.",
         "todo": "h = [0, 5, 2]\nsecond = None       # TODO: 둘째 칸의 값. 칸 번호는 0 부터예요\nlength = None       # TODO: 칸이 몇 개인지\n\nwords = ['영화', '영화', '배우', '최고', '영화', '배우']\nfreq = None         # TODO: Counter 로 세기\n\nW = torch.tensor([[1.0, -1.0],\n                  [0.0, 2.0],\n                  [1.0, 1.0]])\nxt = torch.tensor([1.0, 2.0])\nz = None            # TODO: 골뱅이로 행렬 곱\n\nxg = torch.tensor(2.0, requires_grad=True)\nf = xg ** 3 + 2 * xg\nf.backward()\nby_hand = None      # TODO: f' = 3x^2 + 2 에 x = 2 를 넣은 값\n\nprint(second, length, freq.most_common(2))\nprint(z, tuple(z.shape), xg.grad.item(), by_hand)",
         "sol": "h = [0, 5, 2]\nsecond = h[1]\nlength = len(h)\n\nwords = ['영화', '영화', '배우', '최고', '영화', '배우']\nfreq = Counter(words)\n\nW = torch.tensor([[1.0, -1.0],\n                  [0.0, 2.0],\n                  [1.0, 1.0]])\nxt = torch.tensor([1.0, 2.0])\nz = W @ xt\n\nxg = torch.tensor(2.0, requires_grad=True)\nf = xg ** 3 + 2 * xg\nf.backward()\nby_hand = 3 * 2 ** 2 + 2\n\nprint(second, length, freq.most_common(2))\nprint(z, tuple(z.shape), xg.grad.item(), by_hand)",
         "check": "ok(second == 5 and length == 3, 'h[1] 은 5, len(h) 는 3. 칸 번호는 0 부터예요')\nok(freq.most_common(2) == [('영화', 3), ('배우', 2)], '영화 3번, 배우 2번이에요')\nok(tuple(z.shape) == (3,), '(3,2) 골뱅이 (2,) 는 (3,). 가운데 2 가 사라져요')\nok(torch.allclose(z, torch.tensor([-1.0, 4.0, 3.0])), 'z 는 (-1, 4, 3). 9번 문제의 가중합과 같은 숫자예요')\nok(by_hand == 14 and abs(xg.grad.item() - 14.0) < 1e-6, '손계산도 14, autograd 도 14. 실습 N3L p.4 의 저장된 출력과 같아요')"},
    ],
}



W5 = {
    "file": "nlp_w5_practice.ipynb",
    "title": "5주차 직접 해보기: 사전 학습 언어 모델",
    "intro": ("사이트의 5주차 회독과 정리 슬라이드를 본 다음 풀어요. 위에서부터 차례로 `Shift+Enter` 로 실행해요.\n\n"
              "- 문제마다 **생각 순서**가 먼저 나와요. 코드를 치기 전에 그 순서를 말로 한 번 읊어요.\n"
              "- `# TODO` 가 있는 칸의 `None` 을 알맞은 코드로 바꿔요.\n"
              "- 바로 아래 **확인 셀**을 실행하면 맞았는지 알려 줘요. 틀리면 빨간 AssertionError 와 힌트가 나와요.\n"
              "- 막히면 맨 아래 **정답 코드**를 봐요.\n\n"
              "GPU 도, 인터넷 다운로드도, 모델 내려받기도 없어요. 실습 노트북 Lab 4 와 달리 여기서는 숫자만 손으로 따라가요."),
    "setup": "import math\nimport numpy as np\nimport torch\nimport torch.nn as nn\ntorch.manual_seed(0)\n" + CHECK_HEAD + "print('준비 끝')",
    "ex": [
        {"md": "## 1. 15 퍼센트 마스킹과 80/10/10 세기\n\n강의 N5 p.19-20. **마스크 언어 모델(Masked Language Modelling (MLM))** 은 토큰의 15 퍼센트를 골라서 가리고, 그 자리를 맞히게 해요.\n\n고른 15 퍼센트가 전부 **마스크 토큰([MASK])** 이 되는 것은 아니에요. 그중 80 퍼센트만 [MASK] 가 되고, 10 퍼센트는 아무 토큰으로 바뀌고, 10 퍼센트는 그대로 둬요. 세 경우 모두 원래 단어를 맞혀야 해요.",
         "think": ["먼저 몇 개를 고르는지 세요. 토큰 200개의 15 퍼센트예요",
                   "그 30개를 다시 80 대 10 대 10 으로 나눠요",
                   "80 퍼센트는 30 의 0.8 이라서 24개예요",
                   "10 퍼센트는 3개씩이고, 24 더하기 3 더하기 3 이 30 이어야 해요",
                   "손실을 세는 자리는 [MASK] 가 된 24개가 아니라 고른 30개 전부예요"],
         "pseudo": ["고른 수 = 전체 토큰 수 곱하기 0.15",
                    "마스크로 바꾸는 수 = 고른 수 곱하기 0.8",
                    "아무 토큰으로 바꾸는 수 = 고른 수 곱하기 0.1",
                    "그대로 두는 수 = 고른 수 빼기 앞의 둘",
                    "손실을 세는 자리 수 = 고른 수"],
         "pseudo_first": True,
         "pseudo_show": True,
         "next": "N5 p.20 이 80/10/10 그림이고, 미세조정 때는 [MASK] 가 아예 없어서 모델이 [MASK] 를 보는 데 기대면 안 된다는 것이 이유예요. 실습 N5L p.13 에서 실제로 빈칸을 채워 봐요.",
         "todo": "n_tokens = 200\n\nchosen = None      # TODO: 15 퍼센트를 고르기 (int() 로 버림)\nto_mask = None     # TODO: 고른 것의 80 퍼센트\nto_random = None   # TODO: 고른 것의 10 퍼센트\nto_keep = None     # TODO: 나머지 (고른 수에서 둘을 빼기)\nloss_positions = None   # TODO: 손실을 세는 자리 수\n\nprint(chosen, to_mask, to_random, to_keep, loss_positions)",
         "sol": "n_tokens = 200\n\nchosen = int(0.15 * n_tokens)\nto_mask = int(0.8 * chosen)\nto_random = int(0.1 * chosen)\nto_keep = chosen - to_mask - to_random\nloss_positions = chosen\n\nprint(chosen, to_mask, to_random, to_keep, loss_positions)",
         "check": "ok(chosen == 30, '200 의 15 퍼센트는 30개예요')\nok(to_mask == 24, '30 의 80 퍼센트는 24개가 [MASK] 가 돼요')\nok(to_random == 3 and to_keep == 3, '10 퍼센트씩 3개는 아무 토큰으로, 3개는 그대로 둬요')\nok(to_mask + to_random + to_keep == chosen, '셋을 더하면 고른 30개가 다시 나와요')\nok(loss_positions == 30, '손실은 [MASK] 24자리가 아니라 고른 30자리 전부에서 세요')"},

        {"md": "## 2. 마스크 자리에서만 손실 세기\n\n강의 N5 p.19. **손실 함수(Loss Function)** 는 가린 자리에서만 계산해요. 가리지 않은 자리는 답이 그대로 보이니까 점수를 매길 이유가 없어요.\n\n한 자리의 손실은 2주차, 3주차에서 본 그대로예요. 어휘 전체에 **소프트맥스(Softmax)** 를 씌워 확률을 만들고, 정답 토큰에 준 확률의 음의 로그가 **교차 엔트로피(Cross-Entropy)** 예요.",
         "think": ["어휘가 5개라서 한 자리마다 점수가 5개 나와요",
                   "줄마다 소프트맥스를 해요. 줄 합이 1 이 되어야 해요",
                   "첫 줄의 정답은 0번 칸, 둘째 줄의 정답은 1번 칸이에요",
                   "정답 칸의 확률을 꺼내고 음의 로그를 씌워요",
                   "가린 자리가 두 개니까 두 값을 평균 내요. 나머지 세 자리는 아예 안 세요"],
         "pseudo": ["줄마다 최댓값을 빼고 exp 를 씌운 뒤 줄 합으로 나눈다",
                    "정답 칸의 확률만 꺼낸다",
                    "음의 로그를 씌운다",
                    "가린 자리 수로 평균을 낸다"],
         "pseudo_first": True,
         "pseudo_show": True,
         "next": "N2 p.33 의 소프트맥스와 N3 p.41 의 교차 엔트로피가 그대로 쓰여요. 실습 N5L p.13 의 빈칸 채우기 출력에 나오는 서울 0.64 같은 숫자가 바로 이 확률이에요.",
         "todo": "scores = np.array([[2.0, 1.0, 0.0, 0.0, 1.0],\n                   [0.0, 3.0, 1.0, 0.0, 0.0]])\ngold = np.array([0, 1])\n\ndef row_softmax(M):\n    M = M - M.max(axis=1, keepdims=True)\n    e = np.exp(M)\n    return e / e.sum(axis=1, keepdims=True)\n\nP = None          # TODO: 줄마다 소프트맥스\np_gold = None     # TODO: 정답 칸의 확률만 꺼내기 (P[np.arange(2), gold])\nloss = None       # TODO: 음의 로그를 씌워 평균 내기\n\nprint(P.round(4))\nprint(p_gold.round(4), round(float(loss), 4))",
         "sol": "scores = np.array([[2.0, 1.0, 0.0, 0.0, 1.0],\n                   [0.0, 3.0, 1.0, 0.0, 0.0]])\ngold = np.array([0, 1])\n\ndef row_softmax(M):\n    M = M - M.max(axis=1, keepdims=True)\n    e = np.exp(M)\n    return e / e.sum(axis=1, keepdims=True)\n\nP = row_softmax(scores)\np_gold = P[np.arange(2), gold]\nloss = -np.log(p_gold).mean()\n\nprint(P.round(4))\nprint(p_gold.round(4), round(float(loss), 4))",
         "check": "ok(np.allclose(P.sum(axis=1), 1.0), '줄마다 합이 정확히 1 이에요')\nok(np.allclose(p_gold, [0.4984, 0.7784], atol=1e-4), '정답 확률은 0.4984 와 0.7784 예요')\nok(abs(float(loss) - 0.4734) < 1e-4, '두 자리 손실의 평균은 약 0.4734 예요')\nok(abs(float(loss) - float(-np.log(P[0, 0]) - np.log(P[1, 1])) / 2) < 1e-12, '가린 두 자리만 더해서 2 로 나눈 값이에요')"},

        {"md": "## 3. 양쪽을 다 보는 BERT, 앞만 보는 GPT\n\n강의 N5 p.17-18, 4주차 N4 p.43. 4주차에서 **인코더(Encoder)** 는 양쪽을 다 보고 **디코더(Decoder)** 는 앞만 본다고 배웠죠. 그 차이가 5주차에서 **버트(BERT)** 와 **지피티(GPT)** 로 갈려요.\n\n디코더는 **인과 마스킹(Causal Masking)** 때문에 오른쪽 위가 막혀 있어요. 인코더는 막힌 데가 없어서 다음 단어 맞히기가 아예 문제가 되지 않아요. 답이 이미 입력에 보이니까요.",
         "think": ["토큰 4개짜리 문장 하나로 해 봐요. 표는 4 곱하기 4 예요",
                   "BERT 는 모든 칸이 1 이에요. np.ones 로 만들면 끝이에요",
                   "GPT 는 아래쪽 삼각형만 1 이에요. np.tril 이 그 표를 만들어요",
                   "볼 수 있는 칸을 세면 BERT 는 16, GPT 는 1 더하기 2 더하기 3 더하기 4 로 10 이에요",
                   "GPT 의 줄마다 개수를 찍어 보면 1, 2, 3, 4 로 늘어나요"],
         "pseudo": ["bert = 4 곱하기 4 짜리 전부 1 인 표",
                    "gpt = 같은 크기에서 아래쪽 삼각형만 1 인 표",
                    "각각 다 더해서 볼 수 있는 칸 수를 센다",
                    "gpt 는 줄마다 합을 따로 찍어 본다"],
         "pseudo_first": False,
         "next": "N4 p.43 의 인과 마스킹이 GPT 표를 만들고, N5 p.18 이 그래서 인코더로는 다음 단어 맞히기를 못 한다고 말해요. N5 p.30 의 디코더 목적 함수는 3주차 N3 p.46-47 의 RNN 언어 모델과 같은 일이에요.",
         "todo": "n = 4\n\nbert_mask = None   # TODO: 4 x 4 전부 1 (np.ones)\ngpt_mask = None    # TODO: 아래쪽 삼각형만 1 (np.tril 에 np.ones 를 넣기)\n\nbert_seen = None   # TODO: 볼 수 있는 칸 수 (int(...sum()))\ngpt_seen = None    # TODO: 볼 수 있는 칸 수\n\nprint(gpt_mask)\nprint(bert_seen, gpt_seen, gpt_mask.sum(axis=1))",
         "sol": "n = 4\n\nbert_mask = np.ones((n, n))\ngpt_mask = np.tril(np.ones((n, n)))\n\nbert_seen = int(bert_mask.sum())\ngpt_seen = int(gpt_mask.sum())\n\nprint(gpt_mask)\nprint(bert_seen, gpt_seen, gpt_mask.sum(axis=1))",
         "check": "ok(bert_seen == 16, 'BERT 는 16칸을 다 봐요. 그래서 다음 단어가 이미 보여요')\nok(gpt_seen == 10, 'GPT 는 10칸만 봐요. 1 더하기 2 더하기 3 더하기 4 예요')\nok(np.allclose(gpt_mask.sum(axis=1), [1, 2, 3, 4]), '줄마다 1, 2, 3, 4 로 늘어나요')\nok(np.allclose(np.triu(gpt_mask, 1), 0.0), '오른쪽 위, 곧 미래는 전부 0 이에요')"},

        {"md": "## 4. BERT 를 숫자로 읽기\n\n강의 N5 p.22. **버트(BERT)** 는 두 가지 크기로 나왔어요.\n\n| | 층 | 은닉 | 헤드 | 파라미터 |\n|---|---|---|---|---|\n| BERT-base | 12 | 768 | 12 | 110M |\n| BERT-large | 24 | 1024 | 16 | 340M |\n\n4주차 N4 p.47 에서 **멀티 헤드 어텐션(Multi-Head Attention (MHA))** 은 전체 차원을 헤드 수로 나눠 쓴다고 배웠어요. 그 규칙을 여기 숫자에 그대로 대 봐요.",
         "think": ["헤드 하나가 쓰는 칸 수는 은닉을 헤드 수로 나눈 값이에요",
                   "base 는 768 나누기 12, large 는 1024 나누기 16 이에요",
                   "두 값이 같은지 보세요. 둘 다 64 가 나와요",
                   "large 가 base 보다 파라미터가 몇 배인지도 나눠 보면 돼요",
                   "340 나누기 110 은 약 3.09 배예요. 층은 2배인데 파라미터는 3배가 넘어요"],
         "pseudo": ["base 헤드 차원 = 768 나누기 12",
                    "large 헤드 차원 = 1024 나누기 16",
                    "파라미터 배수 = 340 나누기 110",
                    "세 값을 찍어서 비교한다"],
         "pseudo_first": False,
         "next": "N4 p.47 의 d 나누기 h 규칙이 그대로예요. 실습 N5L p.10 에서 쓰는 `klue/bert-base` 가 바로 이 표의 왼쪽 줄, 곧 층 12, 은닉 768, 파라미터 110M 짜리 한국어 BERT 예요.",
         "todo": "base = {\"layers\": 12, \"hidden\": 768, \"heads\": 12, \"params_m\": 110}\nlarge = {\"layers\": 24, \"hidden\": 1024, \"heads\": 16, \"params_m\": 340}\n\nbase_head_dim = None    # TODO: 은닉을 헤드 수로 나누기 (// 사용)\nlarge_head_dim = None   # TODO: 같은 방식으로\nparam_ratio = None      # TODO: large 파라미터가 base 의 몇 배인지\n\nprint(base_head_dim, large_head_dim, round(param_ratio, 4))",
         "sol": "base = {\"layers\": 12, \"hidden\": 768, \"heads\": 12, \"params_m\": 110}\nlarge = {\"layers\": 24, \"hidden\": 1024, \"heads\": 16, \"params_m\": 340}\n\nbase_head_dim = base[\"hidden\"] // base[\"heads\"]\nlarge_head_dim = large[\"hidden\"] // large[\"heads\"]\nparam_ratio = large[\"params_m\"] / base[\"params_m\"]\n\nprint(base_head_dim, large_head_dim, round(param_ratio, 4))",
         "check": "ok(base_head_dim == 64, '768 나누기 12 는 64. 헤드 하나가 64칸을 봐요')\nok(large_head_dim == 64, '1024 나누기 16 도 64 예요. 크기를 키워도 헤드 한 개의 칸 수는 그대로예요')\nok(abs(param_ratio - 3.0909) < 1e-3, '340 나누기 110 은 약 3.09 배예요')\nok(base[\"layers\"] * 2 == large[\"layers\"], '층은 정확히 2배인데 파라미터는 3배가 넘어요')"},

        {"md": "## 5. 몸통은 그대로, 과제 헤드만 갈아 끼우기\n\n강의 N5 p.23. 같은 **몸통(Body)** 위에 **과제 헤드(Task Head)** 만 바꿔 끼우면 거의 모든 과제가 돼요. 공구 자루 하나에 날만 갈아 끼우는 것과 같아요.\n\n**인코더(Encoder)** 가 내놓는 것은 토큰마다 768칸짜리 줄이에요. 문장 하나를 분류할 때는 **분류 토큰([CLS])** 자리만 쓰고, 토큰마다 꼬리표를 붙일 때는 모든 자리를 써요.",
         "think": ["인코더 출력 모양부터 적어요. (문장 4개, 토큰 16개, 768칸) 이에요",
                   "문장 분류는 [CLS] 자리 한 줄만 꺼내요. x[:, 0] 이 그 자리예요",
                   "토큰 태깅은 모든 자리에 그대로 씌워요. 모양이 (4, 16, 태그 수) 가 돼요",
                   "헤드 파라미터는 Linear(768, k) 라서 768 곱하기 k 에 편향 k 를 더한 값이에요",
                   "2 클래스면 1538개. 몸통 1억 1천만 개에 견주면 거의 없는 수준이에요"],
         "pseudo": ["인코더 출력 자리에 (4, 16, 768) 짜리 0 텐서를 둔다",
                    "분류 헤드 = Linear(768, 2), [CLS] 자리 한 줄에만 씌운다",
                    "태깅 헤드 = Linear(768, 9), 모든 자리에 씌운다",
                    "파라미터 수 = 768 곱하기 클래스 수 더하기 클래스 수",
                    "몸통 대비 몇 퍼센트인지 나눠 본다"],
         "pseudo_first": True,
         "pseudo_show": False,
         "next": "N5 p.23 의 네 가지 과제 모양(문장 하나, 문장 쌍, 토큰 태깅, 스팬 추출)이 이 계산이에요. 실습 N5L p.14 에서 Hugging Face 가 마스크 언어 모델 헤드를 버리고 2 클래스 헤드를 새로 붙이는 장면이 바로 이것이고, N5L p.15 의 학습 전 정확도 57.0 퍼센트가 그 새 헤드가 아직 무작위라는 증거예요.",
         "todo": "enc_out = torch.zeros(4, 16, 768)    # (문장 4개, 토큰 16개, 768칸)\n\ncls_head = nn.Linear(768, 2)         # 문장 하나 분류\ntag_head = nn.Linear(768, 9)         # 토큰마다 꼬리표 9종\n\ncls_logits = None    # TODO: [CLS] 자리(enc_out[:, 0])에만 cls_head 를 씌우기\ntag_logits = None    # TODO: 모든 자리에 tag_head 를 씌우기\n\ncls_params = None    # TODO: 768 곱하기 2 더하기 2\nbody_params = 110_000_000\nhead_share = None    # TODO: cls_params 가 body_params 의 몇 퍼센트인지\n\nprint(tuple(cls_logits.shape), tuple(tag_logits.shape))\nprint(cls_params, round(head_share, 4))",
         "sol": "enc_out = torch.zeros(4, 16, 768)    # (문장 4개, 토큰 16개, 768칸)\n\ncls_head = nn.Linear(768, 2)         # 문장 하나 분류\ntag_head = nn.Linear(768, 9)         # 토큰마다 꼬리표 9종\n\ncls_logits = cls_head(enc_out[:, 0])\ntag_logits = tag_head(enc_out)\n\ncls_params = 768 * 2 + 2\nbody_params = 110_000_000\nhead_share = 100 * cls_params / body_params\n\nprint(tuple(cls_logits.shape), tuple(tag_logits.shape))\nprint(cls_params, round(head_share, 4))",
         "check": "ok(tuple(cls_logits.shape) == (4, 2), '문장 분류는 문장마다 답 하나라서 (4, 2)')\nok(tuple(tag_logits.shape) == (4, 16, 9), '토큰 태깅은 토큰마다 답이라서 (4, 16, 9)')\nok(cls_params == 1538, '768 곱하기 2 에 편향 2 를 더해 1538개')\nok(cls_params == sum(p.numel() for p in cls_head.parameters()), 'PyTorch 가 센 수와 같아요')\nok(head_share < 0.01, '몸통의 0.01 퍼센트도 안 돼요. 새로 배우는 것은 이것뿐이에요')"},

        {"md": "## 6. 미세조정 레시피를 걸음 수로 바꾸기\n\n강의 N5 p.44. **미세조정(Finetuning)** 은 네 숫자면 끝이에요. **학습률(Learning Rate)** 2e-5 에서 5e-5, **에폭(Epoch)** 2 에서 4, **배치 크기(Batch Size)** 16 또는 32, 그리고 처음 약 10 퍼센트 걸음은 **워밍업(Warmup)** 이에요.\n\n실습 N5L p.20 이 정확히 이 숫자로 돌아가요. 레이블 15,000개, 배치 32, 에폭 2 일 때 몇 걸음을 걷는지 세어 봐요.",
         "think": ["한 에폭은 데이터를 한 번 다 보는 것이에요",
                   "한 에폭의 걸음 수는 15000 나누기 32 인데, 남는 것도 한 걸음이라 올림이에요",
                   "math.ceil(15000 / 32) 은 469 예요. 468.75 를 올린 값이에요",
                   "에폭이 2 이니까 전체 걸음은 469 곱하기 2 로 938 이에요",
                   "워밍업은 전체의 10 퍼센트를 버림해서 93 걸음이에요",
                   "미세조정 학습률이 사전 학습보다 100배 작다고 했으니, 거꾸로 100을 곱하면 사전 학습 쪽 보폭이에요"],
         "pseudo": ["한 에폭 걸음 수 = 데이터 수 나누기 배치 크기, 올림",
                    "전체 걸음 수 = 한 에폭 걸음 수 곱하기 에폭 수",
                    "워밍업 걸음 수 = 전체 걸음 수 곱하기 0.1, 버림",
                    "사전 학습 학습률 = 미세조정 학습률 곱하기 100"],
         "pseudo_first": True,
         "pseudo_show": True,
         "next": "실습 N5L p.20 의 `warmup_steps=max(1, int(0.1 * total_steps))` 가 그대로 이 계산이에요. N5 p.44 는 가장 흔한 실수가 사전 학습 학습률을 그대로 쓰는 것이라고 경고해요. 그러면 모델이 알던 것이 지워져요.",
         "todo": "n_train, batch, epochs = 15000, 32, 2\nlr_finetune = 2e-5\n\nsteps_per_epoch = None   # TODO: 올림 (math.ceil)\ntotal_steps = None       # TODO: 에폭 수만큼 곱하기\nwarmup_steps = None      # TODO: 전체의 10 퍼센트, 버림 (int)\nlr_pretrain = None       # TODO: 미세조정보다 100배 큰 값\n\nprint(steps_per_epoch, total_steps, warmup_steps, lr_pretrain)",
         "sol": "n_train, batch, epochs = 15000, 32, 2\nlr_finetune = 2e-5\n\nsteps_per_epoch = math.ceil(n_train / batch)\ntotal_steps = steps_per_epoch * epochs\nwarmup_steps = int(0.1 * total_steps)\nlr_pretrain = lr_finetune * 100\n\nprint(steps_per_epoch, total_steps, warmup_steps, lr_pretrain)",
         "check": "ok(steps_per_epoch == 469, '15000 나누기 32 는 468.75, 올려서 469 걸음이에요')\nok(total_steps == 938, '에폭 2 니까 938 걸음이에요')\nok(warmup_steps == 93, '938 의 10 퍼센트를 버림하면 93 걸음이에요')\nok(abs(lr_pretrain - 2e-3) < 1e-12, '미세조정 2e-5 의 100배는 2e-3 이에요. 이 보폭으로 미세조정하면 안 돼요')"},

        {"md": "## 7. 1 퍼센트만 움직이기\n\n강의 N5 p.46. **파라미터 효율적 미세조정(Parameter-efficient Finetuning (PEFT))** 은 사전 학습된 **몸통(Body)** 을 **동결(Freezing)** 하고 작은 **어댑터(Adapter)** 만 학습해요. 움직이는 가중치가 전체의 약 1 퍼센트예요.\n\n왜 좋은지는 과제가 여러 개일 때 확 드러나요. 전체 미세조정은 과제마다 모델을 통째로 한 벌씩 저장해야 하지만, PEFT 는 몸통 한 벌에 작은 조각만 여러 개 붙여 두면 돼요.",
         "think": ["몸통은 1억 1천만 개예요. 파이썬으로는 110_000_000 이라고 써도 돼요",
                   "1 퍼센트는 0.01 을 곱한 값이라서 110만 개예요",
                   "전체 미세조정은 몸통 전부가 움직이니 110만 개의 100배를 움직여요",
                   "과제 10개를 전부 전체 미세조정하면 110M 짜리를 10벌 저장해요",
                   "PEFT 는 몸통 1벌에 110만 짜리 조각 10개만 더하면 돼요",
                   "두 저장 용량을 나눠 보면 9배가 넘게 차이가 나요"],
         "pseudo": ["움직이는 수 = 몸통 수 곱하기 0.01",
                    "몇 배 적게 움직이나 = 몸통 수 나누기 움직이는 수",
                    "전체 미세조정 저장량 = 몸통 수 곱하기 과제 수",
                    "PEFT 저장량 = 몸통 수 더하기 움직이는 수 곱하기 과제 수",
                    "두 저장량을 나눈다"],
         "pseudo_first": True,
         "pseudo_show": False,
         "next": "N5 p.46 이 1 퍼센트라는 숫자가 나오는 쪽이고, LoRA 와 어댑터가 그 방법이에요. N5 p.48 의 '한 번 비싸게 배우고 계속 다시 쓴다' 가 이 계산으로 설명돼요. 이 과목에서 직접 PEFT 를 돌리지는 않아요.",
         "todo": "body = 110_000_000\ntasks = 10\n\ntrainable = None      # TODO: 몸통의 1 퍼센트 (int 로)\nfewer_times = None    # TODO: 몸통이 trainable 의 몇 배인지 (// 사용)\nfull_store = None     # TODO: 전체 미세조정으로 과제 10개를 저장할 때\npeft_store = None     # TODO: PEFT 로 과제 10개를 저장할 때 (몸통 1벌 + 조각 10개)\n\nprint(trainable, fewer_times)\nprint(full_store, peft_store, round(full_store / peft_store, 4))",
         "sol": "body = 110_000_000\ntasks = 10\n\ntrainable = int(0.01 * body)\nfewer_times = body // trainable\nfull_store = body * tasks\npeft_store = body + trainable * tasks\n\nprint(trainable, fewer_times)\nprint(full_store, peft_store, round(full_store / peft_store, 4))",
         "check": "ok(trainable == 1_100_000, '1억 1천만의 1 퍼센트는 110만 개예요')\nok(fewer_times == 100, '몸통은 그 100배예요')\nok(full_store == 1_100_000_000, '과제 10개면 11억 개를 저장해요')\nok(peft_store == 121_000_000, 'PEFT 는 1억 2천 1백만 개면 끝이에요')\nok(abs(full_store / peft_store - 9.0909) < 1e-3, '약 9.09배 차이예요')"},

        {"md": "## 8. 혼동 행렬에서 네 가지 숫자 구하기\n\n실습 N5L p.24. **정확도(Accuracy)** 하나로는 언제 틀리는지 알 수 없어요. **혼동 행렬(Confusion Matrix)** 로 쪼개 봐야 해요.\n\n먼저 노트북에 저장된 보고서를 거꾸로 풀어 봐요. 부정 리뷰 2516건의 **재현율(Recall)** 이 0.874, 긍정 리뷰 2484건의 재현율도 0.874 였어요. 재현율은 '실제로 그 반인 것 중 몇 개를 맞혔나' 예요.\n\n그다음에는 연습용 작은 표로 네 숫자를 모두 구해 봐요.",
         "think": ["재현율 곱하기 실제 개수가 맞힌 개수예요",
                   "부정은 0.874 곱하기 2516 이라서 약 2199 건이에요",
                   "긍정은 0.874 곱하기 2484 라서 약 2171 건이에요",
                   "둘을 더해 전체 5000 으로 나누면 정확도 0.874 가 그대로 나와요",
                   "작은 표에서는 오른쪽 아래가 맞힌 긍정, 오른쪽 위가 긍정이라고 잘못 부른 것이에요",
                   "정밀도는 긍정이라고 부른 것 중 맞은 비율, 재현율은 실제 긍정 중 맞은 비율이에요",
                   "F1 은 두 값의 조화 평균이라 2pr 나누기 (p 더하기 r) 예요"],
         "pseudo": ["맞힌 부정 = 0.874 곱하기 2516, 반올림",
                    "맞힌 긍정 = 0.874 곱하기 2484, 반올림",
                    "정확도 = (둘의 합) 나누기 5000",
                    "작은 표에서 정확도 = 대각선 합 나누기 전체",
                    "정밀도 = 오른쪽 아래 나누기 오른쪽 열 합",
                    "재현율 = 오른쪽 아래 나누기 아랫줄 합",
                    "F1 = 2 곱하기 정밀도 곱하기 재현율 나누기 (정밀도 더하기 재현율)"],
         "pseudo_first": True,
         "pseudo_show": True,
         "next": "실습 N5L p.24 의 보고서가 이 숫자이고, N5L p.25 는 확신까지 하면서 틀린 12건을 꺼내 읽어요. 노트북 본문은 정확도를 87.5 퍼센트라고 적었지만 저장된 출력은 0.8740 이에요. 출력 숫자를 따라요.",
         "todo": "rec_neg, n_neg = 0.874, 2516\nrec_pos, n_pos = 0.874, 2484\n\ncorrect_neg = None   # TODO: 재현율 곱하기 개수, 반올림 (round)\ncorrect_pos = None   # TODO: 같은 방식\naccuracy = None      # TODO: 둘을 더해 5000 으로 나누기\n\ncm = np.array([[45, 5],\n               [10, 40]])   # 줄: 실제 부정, 실제 긍정 / 칸: 부정이라 부름, 긍정이라 부름\n\nacc2 = None      # TODO: 대각선 합 나누기 전체 합\nprecision = None # TODO: cm[1, 1] 나누기 긍정이라 부른 것 전체 (cm[:, 1].sum())\nrecall = None    # TODO: cm[1, 1] 나누기 실제 긍정 전체 (cm[1].sum())\nf1 = None        # TODO: 2 곱하기 precision 곱하기 recall 나누기 (precision 더하기 recall)\n\nprint(correct_neg, correct_pos, accuracy)\nprint(acc2, round(precision, 4), recall, round(f1, 4))",
         "sol": "rec_neg, n_neg = 0.874, 2516\nrec_pos, n_pos = 0.874, 2484\n\ncorrect_neg = round(rec_neg * n_neg)\ncorrect_pos = round(rec_pos * n_pos)\naccuracy = (correct_neg + correct_pos) / 5000\n\ncm = np.array([[45, 5],\n               [10, 40]])   # 줄: 실제 부정, 실제 긍정 / 칸: 부정이라 부름, 긍정이라 부름\n\nacc2 = (cm[0, 0] + cm[1, 1]) / cm.sum()\nprecision = cm[1, 1] / cm[:, 1].sum()\nrecall = cm[1, 1] / cm[1].sum()\nf1 = 2 * precision * recall / (precision + recall)\n\nprint(correct_neg, correct_pos, accuracy)\nprint(acc2, round(precision, 4), recall, round(f1, 4))",
         "check": "ok(correct_neg == 2199 and correct_pos == 2171, '부정 2199건, 긍정 2171건을 맞혔어요')\nok(abs(accuracy - 0.874) < 1e-12, '4370 나누기 5000 은 정확히 0.874. 노트북 출력과 같아요')\nok(abs(acc2 - 0.85) < 1e-12, '작은 표의 정확도는 85 나누기 100 으로 0.85 예요')\nok(abs(precision - 40 / 45) < 1e-12, '긍정이라 부른 45건 중 40건이 맞아서 약 0.8889')\nok(abs(recall - 0.8) < 1e-12, '실제 긍정 50건 중 40건을 찾아서 0.8')\nok(abs(f1 - 16 / 19) < 1e-12, 'F1 은 약 0.8421. 정밀도와 재현율 사이에 있어요')"},

        {"md": "## 9. 레이블을 늘리면 얼마나 좋아질까\n\n강의 N5 p.45, 실습 N5L p.30. 사전 학습은 레이블을 사 줘요. 몇 백 개만 있어도 꽤 멀리 가요.\n\n실습에서 같은 모델을 레이블 500개, 2,000개, 15,000개로 각각 미세조정했더니 정확도가 0.8050, 0.8418, 0.8740 이 나왔어요. **수확 체감(Diminishing Returns)** 이 어떤 모습인지 숫자로 봐요.",
         "think": ["상승폭은 뒤 정확도에서 앞 정확도를 뺀 값이에요. 퍼센트 포인트로 보려면 100을 곱해요",
                   "500 에서 2000 은 3.68 포인트, 2000 에서 15000 은 3.22 포인트 올라요",
                   "그런데 데이터는 각각 4배, 7.5배가 들었어요",
                   "상승폭은 비슷한데 값이 점점 비싸지는 게 수확 체감이에요",
                   "500개만으로 15000개 성능의 몇 퍼센트인지도 나눠 봐요. 92 퍼센트가 넘어요",
                   "데이터는 3.3 퍼센트만 썼는데 성능은 92 퍼센트예요"],
         "pseudo": ["상승폭 = (뒤 정확도 빼기 앞 정확도) 곱하기 100",
                    "데이터 배수 = 뒤 레이블 수 나누기 앞 레이블 수",
                    "성능 비율 = 500 정확도 나누기 15000 정확도, 곱하기 100",
                    "데이터 비율 = 500 나누기 15000, 곱하기 100"],
         "pseudo_first": False,
         "next": "N5 p.45 의 그림은 schematic, 곧 눈금이 실제 측정값이 아니라고 슬라이드에 적혀 있어요. 실습 N5L p.30, p.31 이 진짜 측정값이에요. 노트북 본문 표는 80.5, 84.1, 87.5 로 반올림해 적었는데, 저장된 출력은 0.8050, 0.8418, 0.8740 이에요.",
         "todo": "acc = {500: 0.8050, 2000: 0.8418, 15000: 0.8740}\n\ngain1 = None      # TODO: 500 에서 2000 으로 갈 때 오른 퍼센트 포인트\ngain2 = None      # TODO: 2000 에서 15000 으로 갈 때\ncost1 = None      # TODO: 데이터가 몇 배 들었는지 (2000 나누기 500)\ncost2 = None      # TODO: 15000 나누기 2000\n\nshare_perf = None # TODO: 500 정확도가 15000 정확도의 몇 퍼센트인지\nshare_data = None # TODO: 500 이 15000 의 몇 퍼센트인지\n\nprint(round(gain1, 2), round(gain2, 2), cost1, cost2)\nprint(round(share_perf, 1), round(share_data, 1))",
         "sol": "acc = {500: 0.8050, 2000: 0.8418, 15000: 0.8740}\n\ngain1 = 100 * (acc[2000] - acc[500])\ngain2 = 100 * (acc[15000] - acc[2000])\ncost1 = 2000 / 500\ncost2 = 15000 / 2000\n\nshare_perf = 100 * acc[500] / acc[15000]\nshare_data = 100 * 500 / 15000\n\nprint(round(gain1, 2), round(gain2, 2), cost1, cost2)\nprint(round(share_perf, 1), round(share_data, 1))",
         "check": "ok(abs(gain1 - 3.68) < 1e-6, '500 에서 2000 은 3.68 포인트 올라요')\nok(abs(gain2 - 3.22) < 1e-6, '2000 에서 15000 은 3.22 포인트 올라요')\nok(cost1 == 4.0 and cost2 == 7.5, '같은 크기 상승에 데이터가 4배, 그다음 7.5배 들었어요')\nok(abs(share_perf - 92.1) < 0.05, '500개만으로 15000개 성능의 약 92.1 퍼센트예요')\nok(abs(share_data - 3.3) < 0.05, '데이터는 3.3 퍼센트만 썼어요. 첫 몇 백 개가 가장 값져요')"},

        {"md": "## 10. T5 의 스팬 손상 만들어 보기\n\n강의 N5 p.37. **티파이브(T5)** 는 토큰 하나가 아니라 **스팬(Span)**, 곧 이어진 여러 토큰을 통째로 지워요. 지운 자리마다 서로 다른 **센티널 토큰(Sentinel Token)** 을 넣고, **디코더(Decoder)** 가 빠진 조각만 써 내게 해요.\n\n슬라이드 예시를 그대로 코드로 만들어 봐요. `Thank you for inviting me to your party last week` 에서 `for inviting` 과 `last` 를 지워요.",
         "think": ["토큰 목록을 왼쪽부터 훑어요",
                   "지금 자리가 스팬의 시작이면 센티널을 넣고, 그 스팬 끝까지 건너뛰어요",
                   "스팬이 아니면 토큰을 그대로 인코더 입력에 넣어요",
                   "디코더 쪽은 센티널을 쓰고, 그 뒤에 지운 토큰들을 이어 붙여요",
                   "맨 끝에는 다음 센티널 하나를 더 붙여서 끝을 알려요",
                   "센티널 이름은 슬라이드처럼 X, Y, Z 를 꺾쇠에 넣어 써요"],
         "pseudo": ["i 를 0 부터 시작해 토큰을 훑는다",
                    "i 가 다음 스팬의 시작이면: 인코더에 센티널을 넣고, 디코더에 센티널과 지운 토큰들을 넣고, i 를 스팬 끝으로 옮긴다",
                    "아니면: 인코더에 토큰을 그대로 넣고 i 를 하나 늘린다",
                    "다 끝나면 디코더 끝에 센티널 하나를 더 붙인다"],
         "pseudo_first": True,
         "pseudo_show": False,
         "next": "N5 p.37 이 이 그림이고, N5 p.36 의 인코더 디코더는 4주차 N4 p.52-53 에서 이미 만든 구조예요. N5 p.17 의 표에서 인코더 디코더 칸의 목적 함수가 바로 이 스팬 손상이에요. BERT 의 마스킹(N5 p.19)과 견줘 보면 어느 쪽이 더 어려운 문제인지 보여요.",
         "todo": "tokens = [\"Thank\", \"you\", \"for\", \"inviting\", \"me\", \"to\", \"your\", \"party\", \"last\", \"week\"]\nspans = [(2, 4), (8, 9)]          # 반열린 구간. (2, 4) 는 for, inviting\nsentinels = [\"<X>\", \"<Y>\", \"<Z>\"]\n\nenc, dec, i, k = [], [], 0, 0\nwhile i < len(tokens):\n    if k < len(spans) and i == spans[k][0]:\n        enc.append(None)                      # TODO: 이 자리에 넣을 센티널\n        dec.append(sentinels[k])\n        dec += None                           # TODO: 지운 토큰들 (tokens 의 스팬 구간)\n        i = spans[k][1]\n        k += 1\n    else:\n        enc.append(tokens[i])\n        i += 1\ndec.append(sentinels[k])\n\nprint(\"encoder input :\", \" \".join(enc))\nprint(\"decoder target:\", \" \".join(dec))",
         "sol": "tokens = [\"Thank\", \"you\", \"for\", \"inviting\", \"me\", \"to\", \"your\", \"party\", \"last\", \"week\"]\nspans = [(2, 4), (8, 9)]          # 반열린 구간. (2, 4) 는 for, inviting\nsentinels = [\"<X>\", \"<Y>\", \"<Z>\"]\n\nenc, dec, i, k = [], [], 0, 0\nwhile i < len(tokens):\n    if k < len(spans) and i == spans[k][0]:\n        enc.append(sentinels[k])\n        dec.append(sentinels[k])\n        dec += tokens[spans[k][0]:spans[k][1]]\n        i = spans[k][1]\n        k += 1\n    else:\n        enc.append(tokens[i])\n        i += 1\ndec.append(sentinels[k])\n\nprint(\"encoder input :\", \" \".join(enc))\nprint(\"decoder target:\", \" \".join(dec))",
         "check": "ok(enc == ['Thank', 'you', '<X>', 'me', 'to', 'your', 'party', '<Y>', 'week'], '인코더 입력이 슬라이드 그림과 같아요')\nok(dec == ['<X>', 'for', 'inviting', '<Y>', 'last', '<Z>'], '디코더는 빠진 조각만 써요')\nok(len(enc) == 9 and len(dec) == 6, '원문 10개가 인코더 9개, 디코더 6개가 돼요')\nok(all(t not in dec for t in ('Thank', 'you', 'me', 'week')), '지우지 않은 토큰은 디코더가 다시 쓰지 않아요')"},
    ],
}


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(True)}


def code(text):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": text.splitlines(True)}


def pseudo_block(e):
    return "```\n" + "\n".join(e["pseudo"]) + "\n```"


def notebook(spec, solved=False):
    cells = [md(f"# {spec['title']}\n\n" + spec["intro"]), code(spec["setup"])]
    for e in spec["ex"]:
        body = e["md"]
        if e.get("think"):
            body += "\n\n### 생각 순서 (코드 치기 전에 말로 읊어요)\n\n" + "\n".join(
                f"{i + 1}. {t}" for i, t in enumerate(e["think"]))
        first = e.get("pseudo_first", False)
        if e.get("pseudo") and not first and e.get("pseudo_show", True):
            body += "\n\n### 의사코드 (한 줄이 파이썬 한 줄이 돼요)\n\n" + pseudo_block(e)
        if e.get("next"):
            body += "\n\n> **나중에 여기서 만나요** " + e["next"]
        cells.append(md(body))
        if first:
            if e.get("pseudo_show", True):
                cells.append(md("### 의사코드 먼저\n\n코드를 치기 전에 아래 줄을 종이에 옮겨 적어요. 한 줄이 파이썬 한 줄이 돼요.\n\n"
                                + pseudo_block(e)))
            else:
                cells.append(md("### 의사코드 먼저\n\n이번에는 순서를 스스로 세워 봐요. 위 **생각 순서**를 보고 의사코드를 서너 줄로 적은 다음에 코드를 쳐요. "
                                "모범 의사코드는 맨 아래 정답 모음에 있어요."))
        cells += [code(e["sol"] if solved else e["todo"]), md("**확인 셀**: 실행해서 맞았는지 봐요."), code(e["check"])]
    blocks = []
    for e in spec["ex"]:
        head = e["md"].splitlines()[0].lstrip("# ")
        b = f"**{head}**\n\n"
        if e.get("pseudo"):
            b += "의사코드\n\n" + pseudo_block(e) + "\n\n"
        blocks.append(b + f"```python\n{e['sol']}\n```")
    sol = "## 정답 코드\n\n먼저 스스로 풀어 보고, 막혔을 때만 봐요.\n\n" + "\n\n".join(blocks)
    cells.append(md(sol))
    return {"cells": cells, "metadata": {"colab": {"provenance": []}, "kernelspec": {"display_name": "Python 3", "name": "python3"},
                                         "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 0}


def main(test=False):
    OUT.mkdir(parents=True, exist_ok=True)
    for spec in (WB, W2, W3, W4, W5):
        for e in spec["ex"]:
            assert "None" in e["todo"] and "TODO" in e["todo"], e["md"][:20]
            assert e["todo"] != e["sol"], e["md"][:20]
        if spec is W4:
            assert all(e.get("think") for e in spec["ex"]), "W4 는 문제마다 생각 순서가 있어야 해요"
        if spec is W5:
            for e in spec["ex"]:
                head = e["md"][:24]
                assert e.get("think") and e.get("pseudo"), f"{head}: 생각 순서와 의사코드가 둘 다 있어야 해요"
                assert e.get("next"), f"{head}: 나중에 어디서 만나는지 한 줄이 있어야 해요"
                if e.get("pseudo_first"):
                    assert "pseudo_show" in e, f"{head}: 쓰기형 문제는 pseudo_show 를 정해 줘야 해요"
        if spec is WB:
            for e in spec["ex"]:
                head = e["md"][:24]
                assert e.get("think") and e.get("pseudo"), f"{head}: 생각 순서와 의사코드가 둘 다 있어야 해요"
                assert e.get("next"), f"{head}: 나중에 어디서 만나는지 한 줄이 있어야 해요"
                if e.get("pseudo_first"):
                    assert "pseudo_show" in e, f"{head}: 쓰기형 문제는 pseudo_show 를 정해 줘야 해요"
            assert len(spec["ex"]) == 10, "기초 다지기는 열 단원에 한 문제씩이에요"
        nb = notebook(spec)
        raw = json.dumps(nb, ensure_ascii=False, indent=1)
        bad = [c for c in BAD if c in raw]
        assert not bad, f"금지 문자 {bad}"
        (OUT / spec["file"]).write_text(raw, encoding="utf-8")
        print(f"{spec['file']}: 문제 {len(spec['ex'])}개")
        if test:
            import nbformat
            from nbclient import NotebookClient
            tmp = pathlib.Path(tempfile.gettempdir()) / ("solved_" + spec["file"])
            snb = nbformat.reads(json.dumps(notebook(spec, solved=True)), as_version=4)
            NotebookClient(snb, timeout=120, kernel_name="python3").execute()
            nbformat.write(snb, str(tmp))
            outs = [o.get("text", "") for c in snb.cells if c.cell_type == "code" for o in c.get("outputs", [])]
            n_ok = sum(t.count("정답!") for t in outs)
            print(f"  정답 코드로 실행: '정답!' {n_ok}번, 오류 없음")


if __name__ == "__main__":
    main("--test" in sys.argv)
