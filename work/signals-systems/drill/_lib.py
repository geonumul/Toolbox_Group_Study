"""예제와 과제만 (#/drill) 데이터 도우미.

강의자료에서 "Example", "Homework" 라고 적힌 쪽만 모은다. 그 판정은 눈으로 했다:
슬라이드를 그림으로 뽑아 하나씩 보고, 쪽 안에 그 말이 실제로 적혀 있는 것만 넣었다.
"수업에서 풀어 준 예시" 는 Example 이라고 적혀 있지 않으면 넣지 않는다.

정리 슬라이드와 같은 장면 틀(title, points, steps, figure, check, warn ...)을 쓰므로
그리기 도구는 ../notes/slides_w12_lib.py 를 그대로 가져다 쓴다.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "notes"))
import slides_w12_lib as L   # noqa: E402

fig, stp, pts, chk, warn, cmp, fml, recap = L.fig, L.stp, L.pts, L.chk, L.warn, L.cmp, L.fml, L.recap
Plot, T, L_, R, C, A, PL, PG, BOX = L.Plot, L.T, L.L, L.R, L.C, L.A, L.PL, L.PG, L.BOX
num, S = L.num, L.S

ITEMS = []


def item(id, week, deck, pages, kind, no, title, ask, bank, slides, out=""):
    """문제 하나. pages 는 그 문제가 걸쳐 있는 강의자료 쪽 번호 (여러 쪽이면 순서대로).
       out 에 글을 넣으면 "이번 시험 범위 밖" 으로 표시된다 (지우지는 않는다)."""
    assert kind in ("예제", "과제"), kind
    assert pages and all(isinstance(p, int) for p in pages), id
    assert len(title) <= 28, title
    assert 2 <= len(slides) <= 9, (id, len(slides))
    d = {"id": id, "week": week, "deck": deck, "pages": list(pages), "kind": kind,
         "no": no, "title": title, "ask": ask, "bank": list(bank), "slides": list(slides)}
    if out:
        d["out"] = out
    ITEMS.append(d)


def write(path, title, intro):
    seen = set()
    for x in ITEMS:
        assert x["id"] not in seen, x["id"]
        seen.add(x["id"])
    out = {"title": title, "intro": intro, "label": "예제와 과제만", "items": ITEMS}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(L.fill(out), f, ensure_ascii=False, indent=1)
    n = sum(len(x["slides"]) for x in ITEMS)
    ex = sum(1 for x in ITEMS if x["kind"] == "예제")
    out = sum(1 for x in ITEMS if x.get("out"))
    print("예제 %d개, 과제 %d개, 풀이 장면 %d장%s -> %s"
          % (ex, len(ITEMS) - ex, n, ", 시험 범위 밖 %d개" % out if out else "", os.path.basename(path)))
