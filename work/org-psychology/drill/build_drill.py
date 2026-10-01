# -*- coding: utf-8 -*-
"""조직심리학 시험 대비 (서술형) 를 만든다.

슬라이드 한 쪽에 서술형 문제 하나. 답은 슬라이드에 적힌 말 그대로 쓰고,
교수님이 수업에서 덧붙인 말은 녹음에서 찾아 붙인다.

사용: python work/org-psychology/drill/build_drill.py
그 다음: python tools/build_site.py org-psychology
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.stdout.reconfigure(encoding="utf-8")

import _lib
import w01
import w02
import w03
import w05

for m in (w01, w02, w03, w05):
    m.build()

_lib.write(
    os.path.join(HERE, "drill.json"),
    "슬라이드 한 쪽에 서술형 한 문제",
    "이 과목은 이해할 것이 적고 외우면 된다. 그래서 읽는 화면을 다 빼고 "
    "**한 쪽에 문제 하나** 만 남겼다. 물음만 떠 있을 때 입으로 답해 보고, "
    "버튼을 누르면 그 밑에 답이 붙는다. 다음을 누르면 바로 다음 문제다. "
    "답은 **슬라이드에 적힌 말 그대로** 썼다. 교수님이 주로 객관식, 빈칸 넣기, 단답형이라고 했고 "
    "빈칸과 단답은 슬라이드 문장을 그대로 비우고 묻는 꼴이라, 바꿔 쓴 말로 외우면 빈칸을 못 채운다.")
