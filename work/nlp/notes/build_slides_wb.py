# -*- coding: utf-8 -*-
"""자연어처리 기초 다지기 슬라이드 생성: slides_wb.json (week b).
실행: python build_slides_wb.py   (저장소 어디서 실행해도 된다)

단원 10개는 wb_units_1_4.py, wb_units_5_7.py, wb_units_8_10.py 에 나누어 적혀 있고
함께 쓰는 도우미(용어 사전, 슬라이드 도우미, SVG 도우미, 검사)는 wb_common.py 에 있다.
모든 숫자 예제는 각 단원 파일 안에서 Python 으로 계산하고 assert 로 확인한다.
"""
import json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.dont_write_bytecode = True

import wb_units_1_4, wb_units_5_7, wb_units_8_10   # noqa: E402

OUT = os.path.join(HERE, "slides_wb.json")
UNITS = wb_units_1_4.UNITS + wb_units_5_7.UNITS + wb_units_8_10.UNITS

assert [u["id"] for u in UNITS] == ["wb-%d" % i for i in range(1, 11)], [u["id"] for u in UNITS]

DATA = {"week": "b", "title": "기초 다지기. 자연어처리에 필요한 수학과 파이썬 처음부터", "units": UNITS}
raw = json.dumps(DATA, ensure_ascii=False, indent=1)
for ch in ("—", "–", "·", "・"):
    assert ch not in raw, ch
with open(OUT, "w", encoding="utf-8") as f:
    f.write(raw)

print("저장:", OUT)
print("단원", len(UNITS), "슬라이드", sum(len(u["slides"]) for u in UNITS),
      "그림", sum(1 for u in UNITS for s in u["slides"] if s["kind"] == "figure"))
for u in UNITS:
    print("  %-6s %-34s %2d장, 용어 %d" % (u["id"], u["title"], len(u["slides"]), len(u["terms"])))
