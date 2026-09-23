# -*- coding: utf-8 -*-
"""자연어처리 가리고 설명하기 데이터 (tools/recall_build.py 를 고치지 않고 그 함수를 빌려 쓴다)

사용: python work/nlp/recall/build_recall.py [덱 ...] [--png 3,10]
tools/recall_build.py 에 nlp 프로필이 생기면 이 파일 대신 python tools/recall_build.py nlp 를 쓰면 된다.
프로필 내용은 아래 PROF (영어 16:9 슬라이드라 layout "wide", 글자 층이 있는 PDF).
"""
import json, pathlib, sys

W = pathlib.Path(__file__).resolve().parent.parent
ROOT = W.parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.dont_write_bytecode = True
import recall_build as RB   # noqa: E402

cfg = json.loads((W / "subject.json").read_text(encoding="utf-8"))
PROF = {
    "name": "nlp",
    "decks": {k: RB._pdf(v["pdf"]) for k, v in cfg["decks"].items() if v.get("pdf")},   # 실습 덱(N2L, N3L)은 PDF 가 없어서 뺀다
    "lesson": str(W / "lesson" / "{deck}_*.json"),
    "glossary": [],
    "glossary_units": [str(W / "notes" / "slides_w*.json"), str(W / "terms" / "*.json")],
    "corpus": [str(W / "bank" / "*.json")],
    "out": W / "recall",
    "img": ROOT / "subjects" / "nlp" / "img",
    "layout": "wide",
}


def main():
    argv = sys.argv[1:]
    args = {"ocr": False, "png": None}
    if "--png" in argv:
        args["png"] = [int(x) for x in argv[argv.index("--png") + 1].split(",")]
    decks = [a for a in argv if a in PROF["decks"]] or list(PROF["decks"])
    corpus = RB.Corpus(PROF["corpus"])
    gloss = []
    for pat in PROF["glossary_units"]:
        for f, d in RB.load_json_glob(pat):
            if isinstance(d, dict) and "units" in d:
                gloss += [t for u in d["units"] for t in u.get("terms", []) if isinstance(t, dict)]
            else:
                gloss += [t for t in (d if isinstance(d, list) else d.get("terms", [])) if isinstance(t, dict)]
    for deck in cfg["decks"]:
        for f, d in RB.load_json_glob(PROF["lesson"].format(deck=deck)):
            gloss += [g for g in d.get("glossary", []) if isinstance(g, dict)]
    print(f"가리고 설명하기: nlp, 문제 글 {len(corpus.text) / 1e3:.0f}천 자, 용어 {len(gloss)}")
    for deck in decks:
        RB.build_deck(PROF, deck, args, corpus, list(gloss))


if __name__ == "__main__":
    main()
