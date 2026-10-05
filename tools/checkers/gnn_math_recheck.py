# -*- coding: utf-8 -*-
"""시험지에 적힌 답이 정말 맞는지 다시 계산해 본다.

build_exam 이 numpy 로 계산해 넣지만, 글로 적어 둔 답과 실제 계산이
어긋날 수 있다 (사람이 손으로 적은 줄이 섞여 있다). 그래서 배열에서
다시 계산해 exam.json 의 답 문자열과 맞춰 본다.
"""
import io
import json
import re
import sys

import numpy as np

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
WORK = r"D:/GRAPH_LECTURE_OJLEE/02_작업/그래프신경망/최종정리/_작업/시험지"
sys.path.insert(0, WORK)
import build_exam as B   # noqa: E402


def g(v):
    v = float(v)
    return int(round(v)) if abs(v - round(v)) < 1e-9 else round(v, 4)


def nums(s):
    """글에서 숫자만 뽑는다."""
    return [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", s)]


d = json.load(open(WORK + "/exam.json", encoding="utf-8"))
BY = {x["n"]: x for x in d["items"]}
bad = []


def ans_of(n, head_part):
    for f in BY[n]["slides"]:
        if f.get("kind") == "steps" and head_part in (f.get("head") or ""):
            return f.get("answer", "")
    return ""


def check(name, got, want, tol=5e-4):
    got, want = list(got), list(want)
    if len(got) != len(want) or any(abs(a - b) > tol for a, b in zip(got, want)):
        bad.append("%s: 적힌 값 %s, 다시 계산 %s" % (name, got, [round(x, 4) for x in want]))
        print("  틀림 %-26s 적힌 %s / 계산 %s" % (name, got, [round(x, 4) for x in want]))
    else:
        print("  OK   %-26s %s" % (name, [round(x, 4) for x in want]))


rn, relu = B.rownorm, B.relu

# 11 GCN: H(1) = relu(Atilde H(0))
want = relu(rn(B.A3) @ B.H3).ravel()
check("11 GCN H(1)", nums(ans_of(11, "c 풀기"))[-5:], want)

# 15 JKNet: max(relu(A~H0), relu(A~H1))
h1 = relu(rn(B.A7) @ B.H7)
h2 = np.maximum(h1, relu(rn(B.A7) @ h1))
check("15 JKNet H(2)", nums(ans_of(15, "2단계"))[-5:], h2.ravel())

# 16 GCNII
inner = 0.5 * (rn(B.A8) @ B.H8) + 0.5 * B.H8
check("16 GCNII H(1)", nums(ans_of(16, "2단계"))[-5:], relu(0.5 * inner).ravel())

# 17 DeepGCN
d1 = relu(rn(B.A9) @ B.H9) + B.H9
d2 = relu(rn(B.A9) @ d1) + d1
check("17 DeepGCN H(1)", nums(ans_of(17, "k = 1"))[-4:], d1.ravel())
check("17 DeepGCN H(2)", nums(ans_of(17, "k = 2"))[-4:], d2.ravel())

# 4 APPNP
z1 = 0.5 * (rn(B.A13) @ B.H13) + 0.5 * B.H13
z2 = 0.5 * (rn(B.A13) @ z1) + 0.5 * B.H13
check("4 APPNP Z(2)", nums(ans_of(4, "c 풀기"))[-4:], z2.ravel())

# 5 GPR-GNN
at = rn(B.A14)
p0, p1, p2 = B.H14, at @ B.H14, at @ (at @ B.H14)
z = 0.5 * p0 + 0.3 * p1 - 0.2 * p2
check("5 GPR-GNN Z", nums(ans_of(5, "가중합"))[-4:], z.ravel())

# 2 FastGCN q(u)
atq = rn(B.A11)
sq = (atq ** 2).sum(axis=0)
check("2 FastGCN q(u)", nums(ans_of(2, "뽑기 확률"))[-5:], (sq / sq.sum()))

# 7 PairNorm
X = np.asarray(B.X16)
Xc = X - X.mean(axis=0)
den = np.sqrt((Xc ** 2).sum(axis=1).mean())
check("7 PairNorm x_i", nums(ans_of(7, "크기로"))[-8:], (Xc / den).ravel())

print("\n틀린 답 %d개" % len(bad))
