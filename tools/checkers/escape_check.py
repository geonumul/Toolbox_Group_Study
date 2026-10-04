# -*- coding: utf-8 -*-
"""한 겹 역슬래시로 적힌 TeX 를 찾아 두 겹으로 만든다.

파이썬 보통 문자열에서 "\t" 는 TAB, "\n" 은 줄바꿈이다. 그래서 "$\tilde A$" 라고
적으면 화면에 "$<TAB>ilde A$" 가 나온다. r"..." 가 아니면 반드시 두 겹이어야 한다.

이미 r"..." 로 적힌 줄은 건드리지 않는다.
"""
import io
import pathlib
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
BASE = pathlib.Path(r"D:/GRAPH_LECTURE_OJLEE/02_작업/그래프신경망/최종정리/_작업/시험지")

# 파이썬이 다른 뜻으로 읽어 버리는 글자들
DANGER = "abfnrtv0123456789xNuU"
# 한 겹 역슬래시 + 위험 글자 (앞에 역슬래시가 더 없을 때)
PAT = re.compile(r"(?<!\\)\\([%s])" % DANGER)

total = 0
for p in sorted(BASE.glob("*.py")):
    lines = p.read_text(encoding="utf-8").split("\n")
    hit = []
    for i, ln in enumerate(lines):
        # r"..." 나 r'''...''' 로 시작하는 줄은 날것이라 괜찮다
        if re.search(r"\br['\"]", ln):
            continue
        if PAT.search(ln):
            hit.append(i)
    if not hit:
        continue
    print("\n%s: %d줄" % (p.name, len(hit)))
    for i in hit:
        before = lines[i]
        lines[i] = PAT.sub(lambda m: "\\\\" + m.group(1), before)
        shown = PAT.findall(before)
        print("   %d행  \\%s  ->  %s" % (i + 1, ", \\".join(shown), lines[i].strip()[:62]))
        total += 1
    p.write_text("\n".join(lines), encoding="utf-8")

print("\n고친 줄 %d개" % total)
