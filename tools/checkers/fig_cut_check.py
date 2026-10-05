# -*- coding: utf-8 -*-
"""그림에서 점선으로 그린 "버린 선" 이 정말 그 문제가 버리는 선인지 본다.

8번에서 문제는 (A, D) 와 (B, C) 를 지우는데 그림은 (A, C) 와 (B, D) 를 점선으로
그리고 있었다. 간선 집합은 같아서 fig_graph_check 로는 안 잡힌다.

보는 법: 점선 두 끝의 노드 이름을 찾고, 그 짝이 문제 글에서 "버린다/지운다/사라진다"
같은 말과 함께 나오는지 본다.
"""
import io
import json
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
SRC = r"D:/GRAPH_LECTURE_OJLEE/02_작업/그래프신경망/최종정리/_작업/시험지/exam.json"

CIR = re.compile(r'<circle class="[^"]*" cx="(-?\d+)" cy="(-?\d+)" r="\d+"/>'
                 r'<text class="[^"]*" x="-?\d+" y="-?\d+" font-size="\d+" '
                 r'text-anchor="middle">([^<]*)</text>')
DASH = re.compile(r'<line class="[^"]*" x1="(-?\d+)" y1="(-?\d+)" x2="(-?\d+)" y2="(-?\d+)"'
                  r'[^>]*stroke-dasharray')
# 한국어 활용까지 (버리/버릴/버린, 지우/지운/지워 ...). "버릴" 은 "버리" 로 안 잡힌다.
CUTWORD = re.compile(r"버[리릴린려렸]|지[우운워웠]|빼[고는며]|사라|끊|제외|밖으로|dropped|drop")


def texts(it):
    out = []
    for f in it["slides"]:
        for k in ("items", "steps"):
            out += [str(x) for x in (f.get(k) or [])]
        for k in ("head", "given", "answer", "caption", "ask"):
            if f.get(k):
                out.append(str(f[k]))
    out.append(str(it.get("ask", "")))
    return out


d = json.load(open(SRC, encoding="utf-8"))
bad = n = 0
for it in sorted(d["items"], key=lambda x: x["n"]):
    body = texts(it)
    cutlines = [t for t in body if CUTWORD.search(t)]
    for f in it["slides"]:
        if f.get("kind") != "figure":
            continue
        svg = f["svg"]
        at = {(int(x), int(y)): lab.strip() for x, y, lab in CIR.findall(svg) if lab.strip()}
        for x1, y1, x2, y2 in DASH.findall(svg):
            a, b = at.get((int(x1), int(y1))), at.get((int(x2), int(y2)))
            if not a or not b:
                continue
            n += 1
            # 그 두 이름이 "버린다" 말이 든 줄에 함께 나오나
            ok = any(re.search(r"\b%s\b" % re.escape(a), t) and re.search(r"\b%s\b" % re.escape(b), t)
                     for t in cutlines)
            if not ok:
                bad += 1
                print("  %d번 '%s': 점선 %s-%s 가 '버린다' 는 글에 안 나옴" % (it["n"], f["head"], a, b))
                for t in cutlines[:2]:
                    print("        글: %s" % t[:76])

print("\n점선 %d개 검사, 어긋난 것 %d개" % (n, bad))
