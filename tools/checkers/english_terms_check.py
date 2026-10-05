# -*- coding: utf-8 -*-
"""답안에서 "이 말을 꼭 쓰세요" 로 짚은 용어가 강의자료에 있는 말인지 본다.

채점은 교수님이 자료에 쓴 말로 한다. 내가 뜻만 통하게 바꿔 쓴 말을 외우면
시험에서 손해를 본다 (9번 BFS 를 "structural role" 로 적어 둔 적이 있다.
자료의 말은 "structural equivalence" 였다).

문장 전체를 맞춰 보면 평범한 영어 표현까지 걸려서 쓸모가 없다. 그래서
팁에 **굵게** 표시한 말, 곧 "채점 기준" 으로 짚은 것만 본다.
"""
import io
import json
import pathlib
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
WORK = pathlib.Path(r"D:/GRAPH_LECTURE_OJLEE/02_작업/그래프신경망/최종정리/_작업")

corpus = []
for d in ("lesson", "html"):
    for f in (WORK / d).glob("*.json"):
        try:
            corpus.append(f.read_text(encoding="utf-8"))
        except Exception:
            pass
BIG = re.sub(r"\s+", " ", " ".join(corpus)).lower()
print("강의자료 글 %d만 자에서 찾는다\n" % (len(BIG) // 10000))

d = json.load(open(WORK / "시험지" / "exam.json", encoding="utf-8"))
ok = bad = 0
rows = []
for it in sorted(d["items"], key=lambda x: x["n"]):
    for f in it["slides"]:
        if f.get("kind") != "english":
            continue
        tip = f.get("tip") or ""
        en = (f.get("en") or "")
        for term in re.findall(r"\*\*([^*]+)\*\*", tip):
            t = term.strip().strip(".,").lower()
            # 한글이 섞였거나 너무 짧으면 용어가 아니다
            if re.search(r"[가-힣]", t) or len(t) < 4:
                continue
            found = t in BIG
            # 답안 문장에 실제로 그 말이 들어 있는지도 본다
            inen = t in en.lower()
            if found:
                ok += 1
            else:
                bad += 1
                rows.append((it["n"], term, en[:74], inen))

print("짚은 용어 %d개 가운데 자료에 있는 것 %d, 없는 것 %d\n" % (ok + bad, ok, bad))
if rows:
    print("자료에서 못 찾은 용어 (사람이 보고 판단할 것)")
    for n, term, en, inen in rows:
        print("  %2d번  \"%s\"%s" % (n, term, "" if inen else "   (답안 문장에도 없음)"))
        print("        답안: %s..." % en)
else:
    print("짚은 용어가 전부 강의자료에 있는 말이다")
