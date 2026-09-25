# -*- coding: utf-8 -*-
"""기초 다지기(week b) 용어집 -> terms/b.json
사용: python work/interior-construction/terms/build_terms_b.py

terms/2.json, terms/3.json 에 이미 있는 용어는 넣지 않는다(표기가 두 벌이 되면 안 된다).
기초 다지기에서 처음 나오는 도면, 단위, 돈 관련 낱말만 담는다."""
import json, pathlib, sys

sys.stdout.reconfigure(encoding="utf-8")
HERE = pathlib.Path(__file__).resolve().parent

T = [
    {"ko": "축척", "en": "Scale",
     "say": "도면에 그린 길이와 실제 길이의 비율",
     "more": "1/50 이면 실제를 50분의 1로 줄여 그린 것이라, 도면 길이에 50 을 곱하면 실제 길이가 돼요."},
    {"ko": "평면도", "en": "Floor Plan",
     "say": "공간을 위에서 내려다본 모습으로 그린 도면",
     "more": "방의 배치와 가로, 세로 길이, 문과 창의 위치를 읽어요. 실측도 평면도부터 시작해요."},
    {"ko": "입면도", "en": "Elevation",
     "say": "벽 한 면을 정면에서 바라본 모습으로 그린 도면",
     "more": "천장고, 창과 문의 높이처럼 높이에 관한 것을 읽어요. 방마다 네 면을 그려요."},
    {"ko": "단면도", "en": "Section",
     "say": "건물이나 벽을 잘라 낸 것처럼 그려 속을 보여 주는 도면",
     "more": "석고보드가 몇 겹인지, 스터드와 단열재가 어디에 있는지가 여기서 보여요."},
    {"ko": "천장도", "en": "Ceiling Plan",
     "say": "천장을 그려 조명과 점검구의 자리를 보여 주는 도면",
     "more": "실측 순서는 평면도, 입면도, 천장도예요. 조명 중심 간격과 냉난방기 자리를 재요."},
    {"ko": "범례", "en": "Legend",
     "say": "도면에 쓴 기호와 선이 무슨 뜻인지 모아 적은 표",
     "more": "범례를 먼저 읽어야 도면의 기호가 읽혀요. 실측할 때는 벽, 전기, 수도를 색으로 나누기도 해요."},
    {"ko": "치수선", "en": "Dimension Line",
     "say": "두 점 사이의 길이를 화살표와 숫자로 나타낸 가는 선",
     "more": "재는 곳에서 끌어낸 치수보조선 사이에 긋고, 숫자는 mm 로 적어요."},
    {"ko": "해칭", "en": "Hatching",
     "say": "잘린 재료의 속을 빗금이나 무늬로 칠해 표시하는 것",
     "more": "단면도와 상세도에서 콘크리트, 석고보드, 단열재를 서로 다른 무늬로 구별해요."},
    {"ko": "밀리미터", "en": "mm",
     "say": "1m 의 1000분의 1 인 길이 단위",
     "more": "실내 도면과 실측은 모두 mm 로 적어요. 1,200 이라고 적혀 있으면 1,200mm, 곧 1.2m 예요."},
    {"ko": "실측", "en": "",
     "say": "현장에 가서 줄자로 실제 치수를 재는 일",
     "more": "전체 스케치, 평면도, 입면도, 천장도 순으로 재고 단위는 mm 로 적어요."},
    {"ko": "일반관리비", "en": "",
     "say": "본사를 유지하는 데 드는 비용",
     "more": "현장에 들어가는 돈이 아니라 본사 인원 등 기업 경영을 위한 돈이에요. 공사원가에 더하면 총원가예요."},
    {"ko": "계약금액", "en": "",
     "say": "발주자가 실제로 내기로 한 최종 공사 금액",
     "more": "총원가에 부가이윤 및 부가가치세를 더한 금액이에요. 공사비라고도 해요."},
]

OLD = set()
for w in ("2", "3"):
    for x in json.load(open(HERE / (w + ".json"), encoding="utf-8")):
        for k in ((x.get("ko") or "").strip(), (x.get("en") or "").strip()):
            if k:
                OLD.add(k)

for x in T:
    for k in (x["ko"], x["en"]):
        assert not k or k not in OLD, "이미 %s 에 있는 용어예요: %r" % ("terms/2, 3.json", k)
    assert len(x["ko"]) >= 2, "한 글자 용어 금지: %r" % x["ko"]
    assert x["say"], x["ko"]

raw = json.dumps(T, ensure_ascii=False, indent=1)
for ch in (chr(0x2014), chr(0x2013), chr(0x00B7), chr(0x30FB)):
    assert ch not in raw, "금지 문자"
(HERE / "b.json").write_text(raw, encoding="utf-8", newline="\n")
print("saved terms/b.json", len(T), "개")
