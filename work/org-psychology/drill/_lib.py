# -*- coding: utf-8 -*-
"""조직심리학 시험 대비: 슬라이드마다 서술형 문제 한 쪽.

**한 쪽에 한 문제** 다. 화면에는 물음만 떠 있고, 버튼을 한 번 누르면 그 밑에 답이 붙는다.
다음을 누르면 바로 다음 문제로 간다. 제목 쪽도 끝 쪽도 없다.

왜 슬라이드 말 그대로인가:
  교수님이 1주차에 "주로 객관식, 빈칸 넣기, 단답형" 이라고 했다. 빈칸과 단답은
  슬라이드 문장을 그대로 비우고 묻는 꼴이라, 바꿔 쓴 말로 외우면 빈칸을 못 채운다.
"""
import json
import os

ITEMS = []


def card(deck, week, page, q, answer, prof=None, tip=None, title=None):
    """슬라이드 한 쪽 = 서술형 문제 하나.

    q       물음 (버튼을 누르기 전에는 이것만 보인다)
    answer  모범 답. 슬라이드에 적힌 말 그대로. 줄 목록.
    prof    교수님이 수업에서 덧붙인 것. 녹음에서 찾은 것만 넣는다. 없으면 생략.
    tip     외우는 요령이나 헷갈리는 짝.
    """
    qa = {"answer": list(answer)}
    if prof:
        qa["prof"] = list(prof)
    if tip:
        qa["tip"] = list(tip)
    ITEMS.append({"id": "%s-p%03d" % (deck.lower(), page), "week": str(week), "deck": deck,
                  "pages": [page], "kind": "서술형", "no": "p.%d" % page,
                  "title": title or (q[:26] + ("…" if len(q) > 26 else "")),
                  "ask": q, "bank": [], "slides": [], "qa": qa})


def write(path, title, intro):
    seen = set()
    for x in ITEMS:
        assert x["id"] not in seen, x["id"]
        seen.add(x["id"])
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"title": title, "intro": intro, "label": "서술형", "items": ITEMS},
                  f, ensure_ascii=False, indent=1)
    byw = {}
    for x in ITEMS:
        byw[x["week"]] = byw.get(x["week"], 0) + 1
    n_prof = sum(1 for x in ITEMS if x["qa"].get("prof"))
    print("서술형 %d문제 (주차별 %s), 교수님 말 붙은 것 %d개 -> %s"
          % (len(ITEMS), byw, n_prof, os.path.basename(path)))
