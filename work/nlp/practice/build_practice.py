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


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(True)}


def code(text):
    return {"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": text.splitlines(True)}


def notebook(spec, solved=False):
    cells = [md(f"# {spec['title']}\n\n" + spec["intro"]), code(spec["setup"])]
    for e in spec["ex"]:
        body = e["md"]
        if e.get("think"):
            body += "\n\n### 생각 순서 (코드 치기 전에 말로 읊어요)\n\n" + "\n".join(
                f"{i + 1}. {t}" for i, t in enumerate(e["think"]))
        cells += [md(body), code(e["sol"] if solved else e["todo"]), md("**확인 셀**: 실행해서 맞았는지 봐요."), code(e["check"])]
    sol = "## 정답 코드\n\n먼저 스스로 풀어 보고, 막혔을 때만 봐요.\n\n" + "\n\n".join(
        f"**{e['md'].splitlines()[0].lstrip('# ')}**\n\n```python\n{e['sol']}\n```" for e in spec["ex"])
    cells.append(md(sol))
    return {"cells": cells, "metadata": {"colab": {"provenance": []}, "kernelspec": {"display_name": "Python 3", "name": "python3"},
                                         "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 0}


def main(test=False):
    OUT.mkdir(parents=True, exist_ok=True)
    for spec in (W2, W3, W4):
        for e in spec["ex"]:
            assert "None" in e["todo"] and "TODO" in e["todo"], e["md"][:20]
            assert e["todo"] != e["sol"], e["md"][:20]
        if spec is W4:
            assert all(e.get("think") for e in spec["ex"]), "W4 는 문제마다 생각 순서가 있어야 해요"
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
