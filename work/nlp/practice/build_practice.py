# -*- coding: utf-8 -*-
"""자연어처리 '직접 해보기' 연습 노트북 (Colab 에서 바로 실행). 교수님 실습 노트북과 별개로 새로 만든 연습.

사용: python work/nlp/practice/build_practice.py [--test]
출력: subjects/nlp/practice/nlp_w2_practice.ipynb, nlp_w3_practice.ipynb
--test: 빈칸 자리에 정답 코드를 넣은 노트북을 만들어 nbclient 로 끝까지 실행해 본다 (검사용, 결과는 임시 폴더)
노트북 구성: 문제 설명(마크다운) → 빈칸 코드(TODO) → 확인 셀(assert). 맨 끝에 정답 코드 모음(마크다운 코드 블록).
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


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(True)}


def code(text):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": text.splitlines(True)}


def notebook(spec, solved=False):
    cells = [md(f"# {spec['title']}\n\n" + spec["intro"]), code(spec["setup"])]
    for e in spec["ex"]:
        cells += [md(e["md"]), code(e["sol"] if solved else e["todo"]), md("**확인 셀**: 실행해서 맞았는지 봐요."), code(e["check"])]
    sol = "## 정답 코드\n\n먼저 스스로 풀어 보고, 막혔을 때만 봐요.\n\n" + "\n\n".join(
        f"**{e['md'].splitlines()[0].lstrip('# ')}**\n\n```python\n{e['sol']}\n```" for e in spec["ex"])
    cells.append(md(sol))
    return {"cells": cells, "metadata": {"colab": {"provenance": []}, "kernelspec": {"display_name": "Python 3", "name": "python3"},
                                         "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 0}


def main(test=False):
    OUT.mkdir(parents=True, exist_ok=True)
    for spec in (W2, W3):
        for e in spec["ex"]:
            assert "None" in e["todo"] and "TODO" in e["todo"], e["md"][:20]
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
