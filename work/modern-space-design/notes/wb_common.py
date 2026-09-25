# -*- coding: utf-8 -*-
"""기초 다지기(week b) 전용 도우미.

msdslide_lib 은 1~6주차만 생각하고 만들어져서 terms/1.json ~ 6.json 만 읽는다.
기초 다지기 용어(terms/b.json)는 여기서 msdslide_lib.TERMS 에 끼워 넣는다.
- 이미 있는 열쇠말은 절대 덮어쓰지 않는다(1~6주차 결과가 바뀌면 안 된다).
- 끼워 넣는 모양은 msdslide_lib 이 쓰는 (ko, en, say, more, week) 그대로다.
- 등록하는 열쇠말도 msdslide_lib 과 같이 ko, en, "ko(en)" 세 가지다.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import msdslide_lib


def load_basics_terms(week="b"):
    """terms/<week>.json 을 msdslide_lib.TERMS 에 더한다. 더한 열쇠말 수를 돌려준다."""
    path = os.path.join(msdslide_lib.WORK, "terms", week + ".json")
    added = 0
    for item in json.load(open(path, encoding="utf-8")):
        ko = (item.get("ko") or "").strip()
        en = (item.get("en") or "").strip()
        entry = (ko, en, (item.get("say") or "").strip(),
                 (item.get("more") or "").strip(), week)
        for key in (ko, en, (ko + "(" + en + ")") if (ko and en) else ""):
            if key and key not in msdslide_lib.TERMS:
                msdslide_lib.TERMS[key] = entry
                added += 1
    return added
