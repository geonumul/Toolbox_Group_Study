# -*- coding: utf-8 -*-
"""기초 다지기(주차 b) 정리 슬라이드 생성. 실행: python build_slides_wb.py

출력: notes/slides_wb.json
- 슬라이드 도구는 orgslide_lib 을 그대로 쓴다(새 라이브러리를 만들지 않는다).
- 기초 통계 용어(평균, 표준편차, 효과 크기 ...)는 rules/용어사전.json 에 없으므로
  terms/b.json 을 읽어 wb_common.py 가 orgslide_lib.TERMS 에 넣어 준다.
  용어사전에 있는 말은 그 표기를 그대로 쓴다.
- 단원 본문은 wb_units_1_4.py, wb_units_5_7.py, wb_units_8_10.py 에 나눠 두었다.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

_WORK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # work/org-psychology
sys.path.insert(0, os.path.dirname(_WORK))                            # work/
import _wb_for   # noqa: E402

import wb_common                      # 용어 주입이 먼저 일어나야 한다
from orgslide_lib import write
import wb_units_1_4, wb_units_5_7, wb_units_8_10

UNITS = wb_units_1_4.UNITS + wb_units_5_7.UNITS + wb_units_8_10.UNITS

assert 8 <= len(UNITS) <= 10, "단원 %d개" % len(UNITS)
for i, u in enumerate(UNITS, 1):
    assert u["id"] == "wb-%d" % i, u["id"]
    assert 14 <= len(u["slides"]) <= 18, "%s 슬라이드 %d장" % (u["id"], len(u["slides"]))
    kinds = [s["kind"] for s in u["slides"]]
    assert kinds[-2] == "points", "%s: recap 바로 앞은 points" % u["id"]
    assert u["slides"][-2]["head"] == wb_common.WHERE, "%s: '%s' 슬라이드 없음" % (u["id"], wb_common.WHERE)
    assert kinds.count("figure") >= 3, "%s: 그림 %d개" % (u["id"], kinds.count("figure"))
    assert kinds.count("check") >= 2, "%s: 퀴즈 %d개" % (u["id"], kinds.count("check"))

OUT = os.path.join(HERE, "slides_wb.json")
_weeks = json.load(open(os.path.join(_WORK, "subject.json"), encoding="utf-8"))["weeks"]
_wb_for.attach_for(UNITS, _weeks)
write(OUT, "b", "기초 다지기. 심리학과 통계, 연구방법 처음부터", UNITS)
for u in UNITS:
    print("  %-5s %-34s %2d장, 그림 %d, 퀴즈 %d"
          % (u["id"], u["title"], len(u["slides"]),
             sum(1 for s in u["slides"] if s["kind"] == "figure"),
             sum(1 for s in u["slides"] if s["kind"] == "check")))
