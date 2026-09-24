# -*- coding: utf-8 -*-
"""근현대 공간디자인 회독 레슨 생성기 공용 도구.

쓰는 법 (덱 범위마다 build_<덱>_<시작3자리>-<끝3자리>.py 에서):

    import os, sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from build_msd_common import *

    S = []
    S.append(slide(1, "표지", ["미술공예운동(Arts and Crafts Movement)"],
                   p1=[say("...")], p2=[], p3=[]))
    dump("U1", 1, 16, S)

용어는 work/modern-space-design/terms/<주차>.json 의 표기를 그대로 쓴다.
gl("윌리엄 모리스(William Morris)") 로 그 표기의 용어 항목을 가져온다.
"""
import json, os, re, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.dirname(HERE)
TERMS_DIR = os.path.join(WORK, "terms")
DECK_WEEK = {"U1": "1", "U2": "2", "U3": "3", "U4": "4", "U5": "5", "U6": "6"}

# 주차별 용어 사전을 한 번에 읽어 둔다 (ko 표기 -> 항목). 앞 단원 용어도 부를 수 있다.
DICT = {}
for _w in ("1", "2", "3", "4", "5", "6"):
    for _t in json.load(open(os.path.join(TERMS_DIR, _w + ".json"), encoding="utf-8")):
        _ko, _en = (_t.get("ko") or "").strip(), (_t.get("en") or "").strip()
        for key in (_ko, _en, (_ko + "(" + _en + ")") if (_ko and _en) else ""):
            if key:
                DICT.setdefault(key, _t)

# 금지 문자(긴 줄표, 짧은 줄표, 가운뎃점 두 가지). 이 파일에도 글자를 직접 넣지 않으려고 코드 번호로 적는다.
BAD = {0x2014: "-", 0x2013: "-", 0x00B7: ",", 0x30FB: ","}


def clean(t):
    return t.translate(BAD) if isinstance(t, str) else t


def gl(*names, **extra):
    """용어 목록을 만든다. names 는 terms/*.json 의 ko 표기.
    사전에 없는 용어는 gl("...", 새용어=("영어이름", "쉬운 한 문장", "조금 더")) 처럼 준다."""
    out = []
    for n in names:
        if n not in DICT:
            raise SystemExit("용어 사전에 없어요: " + n + "  (extra 로 직접 넣으세요)")
        t = DICT[n]
        out.append({"ko": t.get("ko", ""), "en": t.get("en", ""), "say": t.get("say", ""), "more": t.get("more", "")})
    for ko, v in extra.items():
        en, say = v[0], v[1]
        more = v[2] if len(v) > 2 else ""
        out.append({"ko": ko, "en": en, "say": say, "more": more})
    seen, uniq = set(), []
    for g in out:
        k = (g.get("en") or g.get("ko") or "").strip()
        if k not in seen:
            seen.add(k)
            uniq.append(g)
    return uniq


def term_key(entry):
    return (entry.get("en") or entry.get("ko") or "").strip()


# ---------------------------------------------------------------- 장면 만들기
def say(*lines):
    return {"kind": "say", "lines": [clean(x) for x in lines]}


def points(head, *items):
    return {"kind": "points", "head": clean(head), "items": [clean(x) for x in items]}


def goal(*items):
    return {"kind": "goal", "items": [clean(x) for x in items]}


def recap(*items):
    return {"kind": "recap", "items": [clean(x) for x in items]}


def analogy(head, scene, *pairs):
    return {"kind": "analogy", "head": clean(head), "scene": clean(scene), "map": [[clean(a), clean(b)] for a, b in pairs]}


def compare(head, cols, *rows):
    return {"kind": "compare", "head": clean(head), "cols": [clean(c) for c in cols], "rows": [[clean(c) for c in r] for r in rows]}


def warn(head, *items):
    return {"kind": "warn", "head": clean(head), "items": [clean(x) for x in items]}


def check(q, choices, a, why):
    return {"kind": "check", "q": clean(q), "choices": [clean(c) for c in choices], "a": a, "why": clean(why)}


def english(head, en, ko, tip=""):
    """이 과목에서 english 는 '논술 답안에 쓸 문장'. en 에 외워 쓸 한국어 문장."""
    d = {"kind": "english", "head": clean(head), "en": clean(en), "ko": clean(ko)}
    if tip:
        d["tip"] = clean(tip)
    return d


def look(head, *boxes):
    """boxes: (x, y, w, h, 설명). 좌표는 슬라이드 그림 왼쪽 위 기준 0~1 비율."""
    bs = []
    for x, y, w, h, s in boxes:
        bs.append({"x": round(x, 3), "y": round(y, 3), "w": round(w, 3), "h": round(h, 3), "say": clean(s)})
    return {"kind": "look", "head": clean(head), "boxes": bs}


def bg(src, *lines):
    return {"kind": "bg", "src": clean(src), "lines": [clean(x) for x in lines]}


def figure(head, svg, caption, builds=1):
    return {"kind": "figure", "head": clean(head), "svg": svg, "caption": clean(caption), "builds": builds}


def slide(p, title, terms, p1, p2=None, p3=None):
    return {"p": p, "title": clean(title), "terms": [clean(t) for t in terms],
            "pass1": p1 or [], "pass2": p2 or [], "pass3": p3 or []}


# ---------------------------------------------------------------- 저장
def dump(deck, lo, hi, slides, glossary):
    ps = [s["p"] for s in slides]
    miss = [p for p in range(lo, hi + 1) if p not in ps]
    if miss:
        raise SystemExit("빠진 쪽: " + str(miss))
    # terms 는 ko, en, "ko(en)" 아무 모양으로 적어도 glossary 의 대표 이름으로 바꿔 준다
    alias = {}
    for g in glossary:
        ko, en = (g.get("ko") or "").strip(), (g.get("en") or "").strip()
        for k in (ko, en, (ko + "(" + en + ")") if (ko and en) else ""):
            if k:
                alias[k] = term_key(g)
    for s in slides:
        fixed = []
        for t in s["terms"]:
            if t not in alias:
                raise SystemExit("p.%d terms '%s' 가 glossary 에 없어요" % (s["p"], t))
            if alias[t] not in fixed:
                fixed.append(alias[t])
        s["terms"] = fixed
    data = {"deck": deck, "from": lo, "to": hi, "glossary": glossary, "slides": sorted(slides, key=lambda s: s["p"])}
    raw = json.dumps(data, ensure_ascii=False, indent=1)
    for code in BAD:
        if chr(code) in raw:
            raise SystemExit("금지 문자 U+%04X" % code)
    out = os.path.join(HERE, "%s_%03d-%03d.json" % (deck, lo, hi))
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(raw)
    n = sum(len(s["pass%d" % k]) for s in slides for k in (1, 2, 3))
    print("%s: %d쪽, 장면 %d개, 용어 %d개 -> %s" % (deck, len(slides), n, len(glossary), out))
