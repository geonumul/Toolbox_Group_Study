# -*- coding: utf-8 -*-
"""그림 SVG 를 좌표로 검사한다. 색은 사이트 CSS 가 입히므로 여기서는 배치만 본다.

보는 것
  1) 노드끼리 겹치나 (중심 거리 < 반지름 합)
  2) 그림 밖(가로 0~480, 세로 0~높이)으로 나간 것이 있나
  3) 글자가 노드 원 안에 걸쳐 가려지나 (노드 글자 제외)
  4) 선이 엉뚱한 곳에서 끝나나 (노드 중심에 안 닿는 선)
"""
import io
import json
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
D = json.load(open(r"D:/GRAPH_LECTURE_OJLEE/02_작업/그래프신경망/최종정리/_작업/시험지/exam.json",
                   encoding="utf-8"))

CIR = re.compile(r'<circle class="([^"]*)" cx="(-?\d+)" cy="(-?\d+)" r="(\d+)"')
TXT = re.compile(r'<text class="([^"]*)" x="(-?\d+)" y="(-?\d+)" font-size="(\d+)"[^>]*>([^<]*)</text>')
VB = re.compile(r'viewBox="0 0 (\d+) (\d+)"')
RECT = re.compile(r'<rect class="([^"]*)" x="(-?\d+)" y="(-?\d+)" width="(\d+)" height="(\d+)"')

bad = []
for it in sorted(D["items"], key=lambda x: x["n"]):
    for f in [x for x in it["slides"] if x.get("kind") == "figure"]:
        s, name = f["svg"], "%d번 '%s'" % (it["n"], f["head"])
        W, H = (int(x) for x in VB.search(s).groups())
        cir = [(c, int(x), int(y), int(r)) for c, x, y, r in CIR.findall(s)]
        txt = [(c, int(x), int(y), int(fs), t) for c, x, y, fs, t in TXT.findall(s)]
        # 1) 노드 겹침
        for i in range(len(cir)):
            for j in range(i + 1, len(cir)):
                _, x1, y1, r1 = cir[i]
                _, x2, y2, r2 = cir[j]
                if (x1, y1) == (x2, y2):
                    continue          # 단계마다 색을 바꾸려고 같은 자리에 덧그린 것
                if ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5 < r1 + r2 + 6:
                    bad.append("%s: 노드가 겹침 (%d,%d)-(%d,%d)" % (name, x1, y1, x2, y2))
        # 2) 그림 밖
        for c, x, y, r in cir:
            if x - r < 0 or x + r > W or y - r < 0 or y + r > H:
                bad.append("%s: 노드가 그림 밖 (%d,%d)" % (name, x, y))
        for c, x, y, fs, t in txt:
            w = len(t) * fs * 0.62
            if y > H or y - fs < 0 or x - w / 2 < -4 or x + w / 2 > W + 4:
                bad.append("%s: 글자가 그림 밖/넘침 \"%s\" (x=%d, 폭 %.0f, 한계 %d)" % (name, t[:26], x, w, W))
        for c, x, y, w, h in RECT.findall(s):
            x, y, w, h = int(x), int(y), int(w), int(h)
            if x < 0 or y < 0 or x + w > W or y + h > H:
                bad.append("%s: 칸이 그림 밖 (%d,%d %dx%d)" % (name, x, y, w, h))
        # 3) 노드 글자가 아닌 글자가 노드 원 안에 들어갔나
        for c, x, y, fs, t in txt:
            if "tl" in c.split():
                continue
            for _, cx, cy, r in cir:
                if ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5 < r - 2:
                    bad.append("%s: 글자가 노드에 가림 \"%s\"" % (name, t[:20]))

print("그림 %d장 검사" % sum(1 for it in D["items"] for x in it["slides"] if x.get("kind") == "figure"))
print("문제 %d건" % len(bad))
for b in bad:
    print("  - " + b)
