# -*- coding: utf-8 -*-
"""주차별 용어집 terms/<주차>.json : rules/용어사전.json 의 weeks 표시로 나눈다 (용어 카드, 용어 게임용)"""
import json, pathlib
W = pathlib.Path(__file__).resolve().parent.parent
d = json.loads((W / "rules" / "용어사전.json").read_text(encoding="utf-8"))
for wk in ("b", "1", "2", "3"):
    arr = [{k: t[k] for k in ("ko", "en", "say", "more")} for t in d if wk in t["weeks"]]
    (W / "terms" / f"{wk}.json").write_text(json.dumps(arr, ensure_ascii=False, indent=1), encoding="utf-8")
    print(wk, len(arr))
