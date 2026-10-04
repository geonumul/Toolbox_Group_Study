# -*- coding: utf-8 -*-
"""최종 점검: 데이터가 멀쩡한지. 화면이 그려지는 것과 내용이 맞는 것은 다른 문제다.

보는 것
  1) 오늘 사고가 났던 것들: TAB 으로 깨진 TeX, em dash(전역 규칙 위반)
  2) 앞머리(연습 카드가 물려받는 부분)가 모든 문제에 있나
  3) 수식 달러 기호가 짝이 맞나 (홀수면 깨져 보인다)
  4) 신호 예제 수, 계획표 쪽수 같은 숫자가 말한 대로인가
"""
import io
import json
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = r"D:/GRAPH_LECTURE_OJLEE"
bad = []


def walk(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v)


# ---- 1, 3) 시험지 데이터
d = json.load(open(BASE + "/02_작업/그래프신경망/최종정리/_작업/시험지/exam.json", encoding="utf-8"))
items = sorted(d["items"], key=lambda x: x["n"])
print("시험 대비 문제 %d개" % len(items))
nt = nd = nodd = 0
for it in items:
    for s in walk(it):
        if "\t" in s:
            nt += 1
            bad.append("%d번: TAB 으로 깨진 글 \"%s\"" % (it["n"], s[:40]))
        if "\u2014" in s:
            nd += 1
            bad.append("%d번: em dash \"%s\"" % (it["n"], s[:40]))
        # 수식 기호 짝 (이스케이프된 \$ 는 제외)
        if s.count("$") % 2:
            nodd += 1
            bad.append("%d번: $ 개수가 홀수 \"%s\"" % (it["n"], s[:50]))
print("  TAB %d, em dash %d, $ 홀수 %d" % (nt, nd, nodd))

# ---- 2) 앞머리와 그림
no_lead = [it["n"] for it in items if it.get("lead", 0) < 2]
no_fig = [it["n"] for it in items if not any(f.get("kind") == "figure" for f in it["slides"])]
figs = sum(1 for it in items for f in it["slides"] if f.get("kind") == "figure")
print("  앞머리 2장 미만: %s" % (no_lead or "없음"))
print("  그림 없는 문제 : %s   (그림 합계 %d장)" % (no_fig or "없음", figs))
if no_lead:
    bad.append("앞머리가 모자란 문제 %s" % no_lead)
if no_fig:
    bad.append("그림 없는 문제 %s" % no_fig)

# ---- 연습 카드가 앞머리를 물려받았나
pc = json.load(open(BASE + "/02_작업/그래프신경망/최종정리/_작업/시험지/practice_cards.json",
                    encoding="utf-8"))
print("연습 카드 %d개 (%d회차)" % (len(pc["items"]), pc["rounds"]))
if len(pc["items"]) != 85:
    bad.append("연습 카드가 85개가 아님: %d" % len(pc["items"]))

# ---- 4) 신호 예제와 과제
sd = json.load(open(BASE + "/03_사이트/Toolbox_Group_Study/work/signals-systems/drill/drill.json",
                    encoding="utf-8"))
ex = sum(1 for x in sd["items"] if x["kind"] == "예제")
hw = len(sd["items"]) - ex
ch3 = [x for x in sd["items"] if x["deck"] == "S5"]
print("신호 예제와 과제 %d개 (예제 %d, 과제 %d), 그중 3장 %d개" % (len(sd["items"]), ex, hw, len(ch3)))
if len(sd["items"]) != 32 or len(ch3) != 5:
    bad.append("신호 문제 수가 말한 것과 다름")
out = [x for x in sd["items"] if x.get("out")]
if out:
    bad.append("아직 '시험 범위 밖' 표시가 남음: %s" % [x["no"] for x in out])

print("\n문제 %d건" % len(bad))
for b in bad[:20]:
    print("  - " + b)
