"""예제와 과제만 (#/drill) 데이터 도우미.



강의자료에서 "Example", "Homework" 라고 적힌 쪽만 모은다. 그 판정은 눈으로 했다:

슬라이드를 그림으로 뽑아 하나씩 보고, 쪽 안에 그 말이 실제로 적혀 있는 것만 넣었다.

"수업에서 풀어 준 예시" 는 Example 이라고 적혀 있지 않으면 넣지 않는다.



정리 슬라이드와 같은 장면 틀(title, points, steps, figure, check, warn ...)을 쓰므로

그리기 도구는 ../notes/slides_w12_lib.py 를 그대로 가져다 쓴다.

"""

import json

import os

import re

import sys



sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "notes"))

import slides_w12_lib as L   # noqa: E402



fig, stp, pts, chk, warn, cmp, fml, recap = L.fig, L.stp, L.pts, L.chk, L.warn, L.cmp, L.fml, L.recap

Plot, T, L_, R, C, A, PL, PG, BOX = L.Plot, L.T, L.L, L.R, L.C, L.A, L.PL, L.PG, L.BOX

num, S = L.num, L.S





# ---------------------------------------------------------------- 용어를 영어로

# 강의자료가 영어라서, 시험지에서 그대로 만날 말만 영어로 바꾼다.

# 교재와 슬라이드에 그 영어가 실제로 적혀 있는 것만 넣는다 (널리 쓰이는 것만).

# 긴 말이 먼저 와야 "초기 안정 상태" 의 "안정" 이 따로 바뀌지 않는다.

EN = [

    ("초기 안정 상태", "Initial Rest"), ("영입력 응답", "Zero-input Response"),

    ("증분 선형", "Incrementally Linear"), ("분배 법칙", "Distributive Property"),

    ("교환 법칙", "Commutative Property"), ("오일러 공식", "Euler's formula"),

    ("임펄스 응답", "Impulse Response"), ("단위 계단", "Unit Step"),

    ("기본 주기", "Fundamental Period"), ("각주파수", "Angular Frequency"),

    ("시불변성", "Time Invariance"), ("시불변", "Time Invariant"), ("시변", "Time Varying"),

    ("선형성", "Linearity"), ("비선형", "Nonlinear"), ("선형", "Linear"),

    ("인과성", "Causality"), ("인과", "Causal"),

    ("안정성", "Stability"), ("불안정", "Unstable"), ("안정", "Stable"),

    ("역시스템", "Inverse System"), ("가역", "Invertible"),

    ("누산기", "Accumulator"), ("적분기", "Integrator"),

    ("컨볼루션", "Convolution"), ("임펄스", "Impulse"),

]

# 조사: 한국어 낱말의 받침에 맞춰 붙어 있던 것을 영어 낱말을 "한국어로 읽은" 소리에 맞게 다시 고른다.
# 긴 조사가 먼저 와야 "이란" 의 "이" 가 "이/가" 로 잘못 잡히지 않는다. 앞쪽이 받침 있을 때 쓰는 꼴이다.
_JOSA = ["이에요/예요", "이면서/면서", "이라면/라면", "이라는/라는", "이라고/라고",
         "이라서/라서", "이려면/려면", "이지만/지만", "이란/란", "이며/며", "이고/고",
         "으로/로", "은/는", "이/가", "을/를", "과/와"]


def josa_en(word, pair):
    """영어 낱말 뒤에 올 조사. 한국어로 읽었을 때 받침이 있는지로 고른다.
       Stable 은 "스테이블" 이라 받침이 있고, Accumulator 는 "어큐뮬레이터" 라 없다."""
    a, b = pair.split("/")                      # a 는 받침 있을 때, b 는 없을 때
    w = word.strip().split()[-1].lower().strip(".'")
    if w.endswith("'s"):
        w = w[:-2]
    if len(w) > 2 and w.endswith("e") and w[-2] not in "aeiou":
        w = w[:-1]                              # 묵음 e: Stable -> stabl
    if not w:
        return b
    if w.endswith("ng") or w[-1] in "lmn":      # ㅇ, ㄹ, ㅁ, ㄴ 받침
        return "로" if (a == "으로" and w[-1] == "l") else a
    if w[-1] in "ptk" and len(w) > 1 and w[-2] in "aeiou":
        return a                                # Step -> 스텝 (ㅂ 받침)
    return b                                    # 나머지는 으/ㅡ 나 모음으로 끝난다


def enize(s):
    """글 속의 용어를 영어로 바꾸고, 바로 뒤에 붙은 조사를 영어 낱말에 맞게 고른다."""
    if not isinstance(s, str):
        return s
    for ko, en in EN:
        s = s.replace(ko, "«" + en + "»")

    def one(m):
        en, tail = m.group(1), m.group(2)
        for pair in _JOSA:
            a, b = pair.split("/")
            for cand in (a, b):
                if tail.startswith(cand):
                    return en + " " + josa_en(en, pair) + tail[len(cand):]
        return en + (" " if tail else "") + tail

    s = re.sub("«(.+?)»([가-힣]{0,4})", one, s)
    s = s.replace("«", "").replace("»", "")
    return re.sub(r"  +", " ", s)


def _en(o):

    if isinstance(o, str):

        return enize(o)

    if isinstance(o, list):

        return [_en(x) for x in o]

    if isinstance(o, dict):

        return {k: (v if k in ("svg", "id", "deck", "kind") else _en(v)) for k, v in o.items()}

    return o





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

        json.dump(_en(L.fill(out)), f, ensure_ascii=False, indent=1)

    n = sum(len(x["slides"]) for x in ITEMS)

    ex = sum(1 for x in ITEMS if x["kind"] == "예제")

    out = sum(1 for x in ITEMS if x.get("out"))

    print("예제 %d개, 과제 %d개, 풀이 장면 %d장%s -> %s"

          % (ex, len(ITEMS) - ex, n, ", 시험 범위 밖 %d개" % out if out else "", os.path.basename(path)))

