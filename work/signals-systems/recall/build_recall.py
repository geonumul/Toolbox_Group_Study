# -*- coding: utf-8 -*-
"""신호및시스템 가리고 설명하기 데이터: tools/recall_build.py 를 고치지 않고 이 과목 프로필만 붙여서 돌린다.
사용: python work/signals-systems/recall/build_recall.py [덱 ...] [--png 3,10]
출력: work/signals-systems/recall/<덱>.json (tools/build_site.py 가 data/recall_<덱>.js 로 옮긴다)
tools/recall_build.py 의 PROFILES 에 이 프로필이 들어가면 이 파일은 필요 없다 (보고서 참고).
S1 은 A4 가로 비율 슬라이드라서 layout "a4", S2, S3 는 16:9 라서 "wide".
"""
import json, pathlib, sys

sys.dont_write_bytecode = True
ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import recall_build as R   # noqa: E402

W = ROOT / "work" / "signals-systems"
LAYOUT = {"S1": "a4", "S2": "wide", "S3": "wide"}


def profile():
    cfg = json.loads((W / "subject.json").read_text(encoding="utf-8"))
    return {
        "name": "signals-systems",
        "decks": {k: str((ROOT / v["pdf"]).resolve()) for k, v in cfg["decks"].items()},
        "lesson": str(W / "lesson" / "{deck}_*.json"),
        "glossary": [str(W / "rules" / "용어사전.json")],
        "corpus": [str(W / "bank" / "*.json")],
        "out": W / "recall",
        "img": ROOT / "subjects" / "signals-systems" / "img",
        "layout": "wide",
    }


def main():
    argv = sys.argv[1:]
    prof = profile()
    args = {"ocr": False, "png": None}
    if "--png" in argv:
        args["png"] = [int(x) for x in argv[argv.index("--png") + 1].split(",")]
    decks = [a for a in argv if a in prof["decks"]] or list(prof["decks"])
    corpus = R.Corpus(prof["corpus"])
    gloss = []
    for g in prof["glossary"]:
        gloss += json.loads(pathlib.Path(g).read_text(encoding="utf-8"))
    for deck in prof["decks"]:
        for f, d in R.load_json_glob(prof["lesson"].format(deck=deck)):
            gloss += [g for g in d.get("glossary", []) if isinstance(g, dict)]
    print(f"가리고 설명하기: signals-systems, 문제 글 {len(corpus.text) / 1e3:.0f}천 자, 용어 {len(gloss)}")
    for deck in decks:
        p = dict(prof, layout=LAYOUT.get(deck, "wide"))
        R.build_deck(p, deck, args, corpus, list(gloss))


if __name__ == "__main__":
    main()
