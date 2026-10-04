# -*- coding: utf-8 -*-
"""그림에 그린 그래프가 그 문제의 인접행렬과 같은지 본다.

그림은 좌표가 멀쩡해도 "엉뚱한 그래프" 를 그리고 있을 수 있다. 눈으로는
비슷해 보여서 못 잡는다. 그래서 선 끝점을 노드 자리에 맞춰 간선 집합을
되살린 뒤, build_exam 이 쓴 행렬에서 나온 간선 집합과 맞춰 본다.

푸는 그림(answer_graph, solve_graph)만 본다. 개념 도식은 일부러 다른 모양을
그리기도 하므로 "노드가 있는 그림" 가운데 문제 번호와 짝지을 수 있는 것만 본다.
"""
import io
import json
import pathlib
import re
import sys

import numpy as np

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
WORK = pathlib.Path(r"D:/GRAPH_LECTURE_OJLEE/02_작업/그래프신경망/최종정리/_작업/시험지")
sys.path.insert(0, str(WORK))

CIR = re.compile(r'<circle class="([^"]*)" cx="(-?\d+)" cy="(-?\d+)" r="(\d+)"/>'
                 r'<text class="[^"]*" x="-?\d+" y="-?\d+" font-size="\d+" '
                 r'text-anchor="middle">([^<]*)</text>')
LINE = re.compile(r'<line class="[^"]*" x1="(-?\d+)" y1="(-?\d+)" x2="(-?\d+)" y2="(-?\d+)"')


def fig_edges(svg):
    """그림에서 노드 자리와 간선을 되살린다."""
    at = {}
    for _, x, y, r, lab in CIR.findall(svg):
        if lab.strip():
            at.setdefault((int(x), int(y)), lab.strip())
    edges = set()
    for x1, y1, x2, y2 in LINE.findall(svg):
        a, b = at.get((int(x1), int(y1))), at.get((int(x2), int(y2)))
        if a and b and a != b:
            edges.add(tuple(sorted((a, b))))
    return set(at.values()), edges


def mat_edges(A, names):
    n = A.shape[0]
    return {tuple(sorted((names[i], names[j])))
            for i in range(n) for j in range(i + 1, n) if A[i, j]}


# 문제 번호 -> (행렬 변수, 이름 목록 변수). 소스를 읽어 확인한 것만.
PAIR = {11: ("A3", "NAMES"), 12: ("A4", "N5"), 13: ("A5", "N6"), 14: ("A6", "N6"),
        15: ("A7", "N5"), 16: ("A8", "N5"), 17: ("A9", "N4"), 1: ("A10", "N10"),
        2: ("A11", "N5"), 3: ("A12", "N5"), 4: ("A13", "N4"), 5: ("A14", "N4"),
        6: ("A15", "N4"), 8: ("A17", "N4")}

import build_exam as B   # noqa: E402

d = json.load(open(WORK / "exam.json", encoding="utf-8"))
bad, seen = [], 0
for it in sorted(d["items"], key=lambda x: x["n"]):
    n = it["n"]
    if n not in PAIR:
        continue
    ak, nk = PAIR[n]
    A = np.asarray(getattr(B, ak))
    names = list(getattr(B, nk))[:A.shape[0]]
    want = mat_edges(A, names)
    lead = it["lead"]
    for i, f in enumerate(it["slides"]):
        if f.get("kind") != "figure":
            continue
        nodes, got = fig_edges(f["svg"])
        if not got or not (nodes & set(names)):
            continue          # 노드 이름이 안 겹치면 개념 도식이다
        seen += 1
        where = "앞머리" if i < lead else "풀이"
        extra, miss = got - want, want - got
        if extra or miss:
            bad.append("%d번 [%s] \"%s\"\n      더 그림: %s\n      빠뜨림: %s"
                       % (n, where, f["head"],
                          sorted("-".join(e) for e in extra) or "없음",
                          sorted("-".join(e) for e in miss) or "없음"))

print("그래프를 그린 그림 %d장 맞춰 봄" % seen)
print("안 맞는 것 %d장" % len(bad))
for b in bad:
    print("  - " + b)
