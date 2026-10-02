# -*- coding: utf-8 -*-
"""O5 쪽마다 어떤 용어가 나오는지 뽑아 레슨 모양으로 저장한다.

가리고 설명하기(tools/recall_build.py)는 1단계에 가릴 말을 고를 때
"이 쪽의 용어"(레슨 JSON 의 slides[].terms)를 크게 쳐준다. 5주차는 회독 레슨을
만들지 않았으므로, 용어집(terms/5.json)의 말이 쪽 글에 실제로 나오는지만 보고
그 목록을 만들어 준다. 쪽 제목은 슬라이드 맨 위 띠에서 읽는다.

사용: python work/org-psychology/lesson/build_O5_terms.py
그 다음: python tools/recall_build.py org-psychology O5
"""
import json
import pathlib
import re
import sys

import fitz

sys.stdout.reconfigure(encoding="utf-8")
HERE = pathlib.Path(__file__).resolve().parent
WORK = HERE.parent
ROOT = WORK.parents[1]

DECK = "O5"
# PDF 경로는 subject.json 의 decks 에 저장소 기준 상대 경로로 적혀 있다
PDF = (ROOT / json.loads((WORK / "subject.json").read_text(encoding="utf-8"))["decks"][DECK]["pdf"]).resolve()


def norm(s):
    """띄어쓰기와 괄호를 지워 비교한다. 슬라이드가 '직무수행'처럼 붙여 쓰기 때문."""
    return re.sub(r"[\s()\[\]/,.·:;'\"-]", "", str(s)).lower()


def main():
    terms = json.loads((WORK / "terms" / "5.json").read_text(encoding="utf-8"))
    # 한 용어가 가진 여러 표기 (한글, 영어, 괄호 안 약어)
    forms = []
    for t in terms:
        ko = t.get("ko", "")
        en = t.get("en", "")
        cand = [ko] + ([re.sub(r"\(.*?\)", "", en).strip()] if en else [])
        # 용어 사전 키는 en 이 있으면 en, 없으면 ko 다 (tools/recall_build.py)
        forms.append((en or ko, [norm(c) for c in cand if len(norm(c)) >= 2]))

    doc = fitz.open(str(PDF))
    out = []
    for i, page in enumerate(doc, 1):
        raw = page.get_text()
        flat = norm(raw)
        # 제목: 맨 위 10% 안의 가장 큰 글씨 줄
        title = ""
        top = page.rect.height * 0.14
        best = 0.0
        for b in page.get_text("dict")["blocks"]:
            for ln in b.get("lines", []):
                for sp in ln.get("spans", []):
                    txt = sp["text"].strip()
                    if not txt or sp["bbox"][1] > top or "Organizational Psychology" in txt or "정지희" in txt:
                        continue
                    if sp["size"] > best:
                        best, title = sp["size"], txt
        hit = [key for key, fs in forms if any(f in flat for f in fs)]
        out.append({"p": i, "title": title, "terms": hit})

    path = HERE / "O5_001-037.json"
    path.write_text(json.dumps({"deck": DECK, "slides": out}, ensure_ascii=False, indent=1) + "\n",
                    encoding="utf-8")
    n = sum(len(s["terms"]) for s in out)
    empty = [s["p"] for s in out if not s["terms"]]
    print(f"{DECK}: {len(out)}쪽, 쪽마다 붙은 용어 모두 {n}개, 용어가 하나도 없는 쪽 {empty}")


if __name__ == "__main__":
    main()
