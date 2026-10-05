# -*- coding: utf-8 -*-
"""수식 구간이 어긋난 자리를 찾는다.

달러 기호 짝이 맞아도 자리가 어긋나면 엉뚱하게 갈린다. 1번에서
"$P^{(0)} = $1$: 1, $2$: 0.5" 처럼 숫자는 수식 밖, 콜론은 수식 안으로 갈린 적이 있다.
개수만 세는 검사로는 안 잡힌다.

보는 것
  1) 수식 안에 한글이 들어간 자리 (\\text{} 안이 아니면 거의 실수다)
  2) 수식 안이 문장부호뿐인 자리 (": " 처럼 갈라진 흔적)
  3) 수식이 비어 있는 자리
"""
import io
import json
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
SRC = r"D:/GRAPH_LECTURE_OJLEE/02_작업/그래프신경망/최종정리/_작업/시험지"

MATH = re.compile(r"\$\$[\s\S]+?\$\$|\$[^$\n]*\$")
HANGUL = re.compile(r"[가-힣]")


def walk(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for k, v in o.items():
            if k == "svg":
                continue
            yield from walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v)


bad = []
for name in ("exam.json", "past.json", "practice_cards.json"):
    try:
        d = json.load(open("%s/%s" % (SRC, name), encoding="utf-8"))
    except Exception as e:
        print("못 읽음 %s: %s" % (name, e))
        continue
    items = d.get("items", [])
    for it in items:
        tag = "%s %s번" % (name, it.get("n", it.get("id", "?")))
        for s in walk(it):
            for m in MATH.finditer(s):
                inner = m.group(0).strip("$")
                if not inner.strip():
                    bad.append((tag, "빈 수식", s[:90]))
                    continue
                # \text{...} 안의 한글은 일부러 넣은 것
                stripped = re.sub(r"\\text\{[^}]*\}", "", inner)
                if HANGUL.search(stripped):
                    bad.append((tag, "수식 안에 한글: %s" % inner[:40], s[:90]))
                elif not re.search(r"[A-Za-z0-9\\]", inner):
                    bad.append((tag, "수식이 부호뿐: %r" % inner[:20], s[:90]))
                # begin/end 짝과 중괄호 짝. 어긋나면 KaTeX 가 통째로 못 그려서
                # 화면에 날것 글자가 그대로 나온다.
                begs = re.findall(r"\\begin\{(\w+)\}", inner)
                ends = re.findall(r"\\end\{(\w+)\}", inner)
                if begs != ends:
                    bad.append((tag, "begin/end 짝이 안 맞음: %s vs %s" % (begs, ends), s[:90]))
                if inner.count("{") != inner.count("}"):
                    bad.append((tag, "중괄호 짝이 안 맞음 (%d vs %d)"
                                % (inner.count("{"), inner.count("}")), s[:90]))

print("어긋난 자리 %d곳" % len(bad))
seen = set()
for tag, why, ctx in bad:
    k = (tag, why)
    if k in seen:
        continue
    seen.add(k)
    print("  %-26s %s" % (tag, why))
    print("        %s" % ctx)
