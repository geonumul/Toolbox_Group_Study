# -*- coding: utf-8 -*-
"""기초 다지기 단원이 "어느 주차에 필요한가" 를 그 단원 슬라이드에서 뽑아낸다.

각 기초 단원의 끝에서 두 번째 슬라이드는 "이게 이 과목 어디에 나오나" 라는 points
슬라이드이고, 그 항목마다 그 단원이 쓰이는 강의 쪽과 주차가 적혀 있다.
여기서 주차를 읽어 단원에 "for" 를 붙인다. 손으로 다시 적지 않으므로 둘이 어긋날 수 없다.

    attach_for(units, weeks)      # units 의 각 원소에 u["for"] 를 넣는다

"for" 값은 주차 id 목록(예: ["4", "4L"]) 이거나, 강의가 있는 주차 전부에 쓰이면
문자열 "all" 이다. 가리키는 주차를 하나도 못 찾으면 빈 목록이 된다.

GNN 저장소(02_작업/.../html/_wb_for.py) 에 같은 파일이 있다. 고칠 때 같이 고친다.
"""
import re

HEAD = "어디에 나오나"      # points 슬라이드 머리말에 이 말이 들어가면 그 슬라이드다
BASICS = ("b", "c")         # 기초 주차 자신은 가리킬 수 없다

# "아직 안 나온다", "나중에 나올 예정" 같은 문장은 지금 그 주차에 필요하다는 뜻이 아니다
NEGATIVE = ("나오지 않", "나오지는 않", "아직", "없어요", "예정", "예고", "들어오면", "이 들어오면")


def _refs(weeks):
    """주차 목록에서 (찾을 글자 -> 주차 id) 표를 만든다. 먼저 넣은 쪽이 이긴다."""
    ref = {}

    def put(k, wid):
        k = (k or "").strip()
        if k and k not in ref:
            ref[k] = wid

    ok = [w for w in weeks if str(w.get("id")) not in BASICS]
    # 1) 강의 덱 이름 (N4, L2, S3 ...) 과 주차 이름 (2주차 실습 처럼 긴 것 먼저 쓰려고 그대로 넣는다)
    for w in ok:
        wid = str(w["id"])
        if w.get("deck"):
            put(str(w["deck"]), wid)
        put(w.get("short"), wid)
    # 2) short 와 title 안에 적힌 "N주차", "N강"
    for w in ok:
        wid = str(w["id"])
        text = (w.get("short") or "") + " " + (w.get("title") or "")
        for m in re.finditer(r"(?<!\d)(\d+)\s*주차", text):
            put(m.group(1) + "주차", wid)
        for m in re.finditer(r"(?<!\d)(\d+)\s*강", text):
            put(m.group(1) + "강", wid)
    # 3) 그래도 없으면 주차 id 가 숫자인 것을 그대로 쓴다
    for w in ok:
        wid = str(w["id"])
        if re.fullmatch(r"\d+", wid):
            put(wid + "주차", wid)
            put(wid + "강", wid)
    return ref


def where_items(unit):
    """이 단원의 "어디에 나오나" 슬라이드 항목들."""
    out = []
    for s in unit.get("slides", []):
        if s.get("kind") == "points" and HEAD in (s.get("head") or ""):
            out += [x for x in s.get("items", []) if isinstance(x, str)]
    return out


def weeks_of(unit, weeks):
    """이 단원이 필요한 주차 id 목록. 주차 차례대로 준다."""
    ref = _refs(weeks)
    order = [str(w["id"]) for w in weeks]
    keys = sorted(ref, key=len, reverse=True)      # 긴 글자부터 찾아야 "2주차 실습" 이 "2주차" 에 먹히지 않는다
    got = []
    for item in where_items(unit):
        if any(n in item for n in NEGATIVE):
            continue
        rest = item
        for k in keys:
            if not k:
                continue
            pat = r"(?<![A-Za-z0-9])" + re.escape(k) + r"(?![A-Za-z0-9])" if re.fullmatch(r"[A-Za-z0-9]+", k) else re.escape(k)
            if re.search(pat, rest):
                wid = ref[k]
                if wid not in got:
                    got.append(wid)
                rest = re.sub(pat, " ", rest)      # 찾은 자리는 지워서 짧은 글자가 그 안에서 또 걸리지 않게 한다
    return sorted(got, key=lambda x: order.index(x) if x in order else 999)


def attach_for(units, weeks, verbose=True):
    """units 의 단원마다 u["for"] 를 넣고, 무엇이 붙었는지 알려 준다."""
    # 강의가 붙은 주차를 하나도 빠짐없이 가리키면 "all" 로 적는다 (주차를 다 늘어놓지 않는다)
    content = [str(w["id"]) for w in weeks if w.get("deck") and str(w.get("id")) not in BASICS]
    empty = []
    for u in units:
        got = weeks_of(u, weeks)
        u["for"] = "all" if content and all(c in got for c in content) else got
        if not got:
            empty.append(u["id"])
        if verbose:
            print("  %-7s %-34s -> %s" % (u["id"], u.get("title", "")[:32], u["for"]))
    if verbose and empty:
        print("  [주의] 가리키는 주차를 못 찾은 단원: " + ", ".join(empty))
    return units
