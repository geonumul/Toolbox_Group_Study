# -*- coding: utf-8 -*-
"""이 과목에만 있는 추가 규칙 검사.
  - prof 장면 금지 (녹음 없음)
  - look 은 pass2 에만, 한 쪽에 최대 한 개 (walk_build 가 첫 look 하나만 쓰기 때문)
  - pass4 이상 금지 (3회독 과목)
  - 금지 문자
  - 맡은 범위의 모든 쪽
사용: python IC_rules_check.py
"""
import json, pathlib, re, sys

sys.stdout.reconfigure(encoding="utf-8")
L = pathlib.Path(__file__).resolve().parent
TOTAL = {"L2": 104, "L3": 63}
BAD = {"—": "em dash", "–": "en dash", "·": "가운뎃점",
       "•": "불릿 가운뎃점", "・": "가운뎃점"}   # 찾는 글자는 escape 로 적는다

errs = []
seen = {"L2": set(), "L3": set()}
for f in sorted(L.glob("L*_*.json")):
    raw = f.read_text(encoding="utf-8")
    for ch, name in BAD.items():
        if ch in raw:
            errs.append(f"{f.name}: {name} {raw.count(ch)}개")
    d = json.loads(raw)
    deck = d["deck"]
    for s in d["slides"]:
        p = s["p"]
        if p in seen[deck]:
            errs.append(f"{deck} p.{p}: 두 파일에 중복")
        seen[deck].add(p)
        for k in ("pass4", "pass5", "pass6"):
            if s.get(k):
                errs.append(f"{f.name} p.{p}: {k} 는 만들지 않아요 (3회독 과목)")
        looks = {}
        for n in (1, 2, 3):
            for fr in s.get(f"pass{n}", []):
                if fr.get("kind") == "prof":
                    errs.append(f"{f.name} p.{p}: prof 장면 (녹음 없음)")
                if fr.get("kind") == "look":
                    looks.setdefault(n, 0)
                    looks[n] += 1
        if looks.get(1) or looks.get(3):
            errs.append(f"{f.name} p.{p}: look 은 2회독에만 (있는 곳 {sorted(looks)})")
        if looks.get(2, 0) > 1:
            errs.append(f"{f.name} p.{p}: look {looks[2]}개 (한 쪽에 하나만)")

for deck, n in TOTAL.items():
    miss = [p for p in range(1, n + 1) if p not in seen[deck]]
    if miss:
        errs.append(f"{deck}: 빠진 쪽 {miss[:20]}{' ...' if len(miss) > 20 else ''} (총 {len(miss)}쪽)")
    else:
        print(f"{deck}: {n}쪽 모두 있어요")

for e in errs:
    print("  오류:", e)
print("결과:", "통과" if not errs else f"오류 {len(errs)}건")
sys.exit(0 if not errs else 1)
