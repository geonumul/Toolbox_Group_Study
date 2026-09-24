# -*- coding: utf-8 -*-
"""친환경건축 E1 덱 17-31쪽 회독 레슨(3회독) 생성 스크립트.

자료: _src/png/E1/p017.png ~ p031.png, recall/_ocr/E1.json, notes/slides_w1.json (w1-3 ~ w1-8),
      scratchpad/eco_prof_notes.md (2주차 목요일 녹음).
용어는 lesson/eco_glossary.py 에서만 고른다.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from eco_glossary import pick, label as L  # noqa: E402

OUT = pathlib.Path(__file__).resolve().parent / "E1_017-031.json"
WHEN = "2주차 목요일 수업"

GLOSS_NAMES = [
    "Oil Shock", "Alternative Energy", "Rating System", "BREEAM", "LEED", "G-SEED",
    "Sustainable Future", "Modern Architecture", "Rio Conference", "Kyoto Protocol",
    "Climate Change Convention", "Ecological Order Restoration", "Biotop", "Ecology", "Ecologism",
    "Mechanistic Worldview", "Ecological Worldview", "Machine Aesthetic", "Organic Architecture",
    "Falling water", "Alternative Architecture", "Community", "Sustainable Development",
    "Maintenance", "Renewable Resources", "Habitat", "Landscape",
    "Consumption-dependent Economy", "Natural Ecosystem",
    "Circulation Loop", "One-Way Process", "Circulation System",
    "Human-centered Design Methodology", "Environmental Load", "Comfort", "Applied Technology",
    "Regional Green Network", "Rainwater", "Wastewater", "Infiltration",
    "Fossil Energy", "Renewable Energy", "Microclimate", "Broadleaf Tree", "Conifer", "Biomass",
    "Local Natural Material", "Recycling", "Transpiration", "Heat Island",
]

MANTRA = "**자연에서 빌려 쓰고, 돌려주며 순환시켜요.**"


def box(x, y, w, h, say):
    return {"x": x, "y": y, "w": w, "h": h, "say": say}


slides = []

# ---------------------------------------------------------------- p17
slides.append({
    "p": 17,
    "title": "2차 오일쇼크: 1978년 이란 쿠데타",
    "terms": ["Oil Shock", "Alternative Energy"],
    "pass1": [
        {"kind": "say", "lines": [
            "석유 때문에 세계가 흔들린 일이 5년 만에 또 일어났어요.",
            "1978년 2차 " + L("Oil Shock") + " 이야기예요.",
            "이번 시작은 전쟁이 아니라 이란에서 일어난 쿠데타였어요.",
            "석유가 모자라니 값이 치솟고 세계 경제가 오래 휘청였어요.",
        ]},
    ],
    "pass2": [
        {"kind": "points", "head": "용어 먼저: " + L("Oil Shock") + " 와 " + L("Alternative Energy"), "items": [
            L("Oil Shock") + " 은 석유 값이 갑자기 크게 뛰어 세계가 흔들린 사건이에요.",
            "1973년이 1차, 1978년이 2차예요.",
            L("Alternative Energy") + " 는 석유 대신 쓸 에너지예요.",
        ]},
        {"kind": "points", "head": "4) 2차 " + L("Oil Shock") + " 네 줄", "items": [
            "1978년 이란에서 쿠데타가 발생했어요.",
            "이란의 유전 노동자들이 국왕에 대항해 파업에 돌입했어요.",
            "급격한 이란의 석유수출 감소에 의해 석유 가격이 폭등했어요.",
            "1980년대 초까지 안정되지 않는 석유가격에 의해 세계경제 혼란이 지속됐어요.",
        ]},
        {"kind": "points", "head": "슬라이드 마지막 두 줄", "items": [
            "1차 2차 석유파동에 의한 석유자원의 고갈 위협 등을 겪으면서,",
            "비로소 " + L("Alternative Energy") + " 개발에 관심을 갖기 시작했어요.",
            "'처음으로' 가 아니라 '비로소' 예요. 두 번을 맞고 나서라는 뜻이에요.",
        ]},
        {"kind": "look", "head": "슬라이드 짚어 읽기", "boxes": [
            box(0.08, 0.225, 0.38, 0.042, "제목 줄이에요. 2차 " + L("Oil Shock") + " 이야기예요."),
            box(0.11, 0.285, 0.36, 0.042, "원인이에요. 1978년 이란에서 쿠데타가 발생했어요."),
            box(0.11, 0.345, 0.60, 0.042, "유전 노동자들이 국왕에 대항해 파업에 돌입했어요."),
            box(0.11, 0.405, 0.62, 0.042, "석유수출이 급격히 줄어 석유 가격이 폭등했어요."),
            box(0.11, 0.465, 0.80, 0.042, "1980년대 초까지 세계경제 혼란이 이어졌어요."),
            box(0.11, 0.585, 0.80, 0.105, "결론 두 줄이에요. 비로소 " + L("Alternative Energy") + " 개발에 관심을 가졌어요."),
        ]},
        {"kind": "prof", "when": WHEN, "lines": [
            "2차 오일쇼크는 5년 만에 또 터졌다고 하셨어요.",
            "이번에는 이란에서 유전 노동자들이 쿠데타를 일으켜 파업한 것이 원인이에요.",
            "이란이 석유를 못 만드니 석유량 자체가 급감하고 가격이 폭등했어요.",
            "80년대 초까지 세계 경제가 흔들렸다고 하셨어요.",
        ]},
    ],
    "pass3": [
        {"kind": "check", "q": "2차 " + L("Oil Shock") + " 의 원인으로 맞는 것은?", "choices": [
            "이집트와 시리아가 이스라엘을 침공한 전쟁",
            "이란의 쿠데타와 유전 노동자 파업",
            "미국의 LEED 평가기준 마련",
            "1992년 리우환경회의 개최",
        ], "a": 1, "why": "2차 " + L("Oil Shock") + " 은 1978년 이란의 쿠데타와 유전 노동자 파업에서 시작했어요."},
        {"kind": "warn", "head": "헷갈리기 쉬운 점", "items": [
            "1차는 1973년 중동 전쟁, 2차는 1978년 이란이에요. 나라를 바꾸면 틀려요.",
            "2차 뒤에 '비로소' " + L("Alternative Energy") + " 에 관심을 가졌어요. 1차 뒤가 아니에요.",
        ]},
    ],
    "pass4": [],
})

# ---------------------------------------------------------------- p18
slides.append({
    "p": 18,
    "title": "석유위기 이후: 나라마다 만든 건물 성적표",
    "terms": ["Rating System", "BREEAM", "LEED", "G-SEED", "Sustainable Future",
              "Modern Architecture", "Rio Conference", "Alternative Energy"],
    "pass1": [
        {"kind": "say", "lines": [
            "두 번의 석유 위기를 겪은 뒤 세계가 건축을 돌아봤어요.",
            "그리고 나라마다 건물의 성적표, " + L("Rating System") + " 을 만들었어요.",
            "영국 " + L("BREEAM") + ", 미국 " + L("LEED") + ", 한국 " + L("G-SEED") + " 세 개만은 꼭 외워요.",
        ]},
    ],
    "pass2": [
        {"kind": "points", "head": "용어 먼저: " + L("Rating System"), "items": [
            L("Rating System") + " 은 건물이 얼마나 친환경인지 점수와 등급을 매기는 기준이에요.",
            "건물의 성적표라고 생각하면 쉬워요.",
            "이름이 모두 줄임말이라 대문자로 써요.",
        ]},
        {"kind": "points", "head": "5) 석유위기 이후 두 줄", "items": [
            L("Modern Architecture") + " 과 도시 상태를 돌아보기 시작했어요.",
            "에너지 절감을 바탕으로 한 친환경설계가 시작됐어요.",
            "앞 쪽에서 본 " + L("Alternative Energy") + " 개발 관심이 여기로 이어져요.",
        ]},
        {"kind": "compare", "head": "나라별 " + L("Rating System"), "cols": ["나라", "연도", "이름"], "rows": [
            ["영국", "1990년대부터", L("BREEAM") + " 건축환경등급 평가기준, 요소기술 개발과 가이드북 보급"],
            ["캐나다", "1993년", "C-2000 Program 등급 평가기준"],
            ["미국", "1993년", "USDBC 설립 및 " + L("LEED") + " 친환경건축물등급 평가기준"],
            ["일본, 프랑스, 독일", "표기 없음", "기술 개발 및 보급"],
            ["한국", "2002년", "친환경건축물 인증제도 시행, 현 " + L("G-SEED")],
        ]},
        {"kind": "points", "head": "맨 아래 두 줄", "items": [
            "1992년 " + L("Rio Conference") + " 의 1993년 환경선언이 내건 말이 " + L("Sustainable Future") + " 예요.",
            "우리 세대뿐 아니라 다음 세대까지 쓸 수 있는 지구를 뜻해요.",
            "슬라이드 맨 아래에는 '현 시대에는 기후위기' 라고 덧붙여져 있어요.",
        ]},
        {"kind": "look", "head": "슬라이드 짚어 읽기", "boxes": [
            box(0.08, 0.225, 0.20, 0.042, "제목이에요. 5) 석유위기 이후예요."),
            box(0.14, 0.285, 0.51, 0.105, L("Modern Architecture") + " 과 도시를 돌아보고 에너지 절감 친환경설계가 시작돼요."),
            box(0.14, 0.405, 0.82, 0.105, "영국 줄이에요. " + L("BREEAM") + " 건축환경등급 평가기준이에요."),
            box(0.14, 0.525, 0.82, 0.105, "캐나다 C-2000(1993), 미국 USDBC 와 " + L("LEED") + "(1993) 예요."),
            box(0.14, 0.705, 0.79, 0.042, "한국은 2002년 시행, 지금 이름이 " + L("G-SEED") + " 예요."),
            box(0.14, 0.765, 0.81, 0.042, "1992년 " + L("Rio Conference") + ", 1993년 환경선언은 " + L("Sustainable Future") + " 예요."),
        ]},
        {"kind": "prof", "when": WHEN, "lines": [
            "두 번을 맞고 나서 석유와 거리를 둬야겠다고 한 것이 사실상 대체에너지의 시작점이래요.",
            "산업혁명을 먼저 한 영국에서 친환경 설계 가이드북도 처음 나왔다고 하셨어요.",
            "볼드체로 해 둔 BREEAM(브리암), LEED(리드), G-SEED 세 개만은 외우자고 하셨어요.",
            "인증 제도 이름은 다 줄임말이라 반드시 대문자로 쓰라고 하셨어요.",
        ]},
    ],
    "pass3": [
        {"kind": "check", "q": "나라와 " + L("Rating System") + " 의 연결로 옳지 않은 것은?", "choices": [
            "영국, BREEAM 건축환경등급 평가기준",
            "캐나다, 1993년 C-2000 Program",
            "미국, 1993년 LEED",
            "한국, 1993년 친환경건축물 인증제도",
        ], "a": 3, "why": "한국은 2002년에 시행했고 지금 이름은 " + L("G-SEED") + " 예요."},
        {"kind": "english", "head": "시험 답안에 쓸 문장", "en": "영국은 BREEAM, 미국은 LEED, 한국은 2002년 시행한 G-SEED 를 마련했다.",
         "ko": "세 나라의 " + L("Rating System") + " 이름을 대문자 그대로 쓰는 것이 핵심이에요.",
         "tip": "영미한 순서로 브리암, 리드, 지시드 라고 소리 내어 외워요."},
        {"kind": "warn", "head": "헷갈리기 쉬운 점", "items": [
            "슬라이드 표기는 'USDBC' 예요. 통상 표기는 'USGBC' 예요. 시험에는 슬라이드 표기를 따라요.",
            "캐나다 C-2000 과 미국 " + L("LEED") + " 는 둘 다 1993년이에요.",
            "1993년 환경선언의 말은 " + L("Sustainable Future") + " 예요. 평가기준 이름이 아니에요.",
        ]},
    ],
    "pass4": [],
})

# ---------------------------------------------------------------- p19
slides.append({
    "p": 19,
    "title": "친환경건축의 개념: 생태질서 회복과 생태주의",
    "terms": ["Climate Change Convention", "Ecological Order Restoration", "Biotop",
              "Ecology", "Ecologism", "Rio Conference", "Kyoto Protocol", "Alternative Energy"],
    "pass1": [
        {"kind": "say", "lines": [
            "나라들이 " + L("Climate Change Convention") + " 에 대응하기로 했어요.",
            "그 답으로 나온 여섯 가지 실천이 " + L("Ecological Order Restoration") + " 이에요.",
            "그 바탕에 깔린 생각이 " + L("Ecologism") + " 이고, 그 정신으로 짓는 것이 친환경건축이에요.",
        ]},
    ],
    "pass2": [
        {"kind": "points", "head": "용어 먼저: " + L("Ecology") + " 와 " + L("Ecologism"), "items": [
            L("Ecology") + " 은 생물체간의 상호 관계에 대한 학문이에요.",
            L("Ecologism") + " 는 그 " + L("Ecology") + " 의 기본정신이에요.",
            "친환경건축은 " + L("Ecologism") + " 에 입각하여 건축문화를 주도하는 것이에요.",
            L("Biotop") + " 은 생물이 모여 사는 작은 서식 공간, 곧 소생물권이에요.",
        ]},
        {"kind": "points", "head": "배경 두 줄", "items": [
            "1992년 " + L("Rio Conference") + " 이후 1997년 " + L("Kyoto Protocol") + " 채택으로,",
            L("Climate Change Convention") + " 에 대응할 정부와 민간분야의 실천 방안과 기술개발이 요구됐어요.",
        ]},
        {"kind": "points", "head": L("Ecological Order Restoration") + " 여섯 가지", "items": [
            "1) 에너지 및 자원의 절감  2) " + L("Alternative Energy") + " 개발",
            "3) 생태환경 오염방지 및 보존  4) 자원 및 쓰레기 재활용",
            "5) 녹지공간 확충 및 체계화  6) 소생물권 " + L("Biotop") + " 조성",
            "앞글자로 절대오재녹비: 절감, 대체, 오염, 재활용, 녹지, 비오톱이에요.",
        ]},
        {"kind": "look", "head": "슬라이드 짚어 읽기", "boxes": [
            box(0.11, 0.225, 0.81, 0.105, "1992년 리우 이후 1997년 교토의정서 채택으로 " + L("Climate Change Convention") + " 대응이 요구됐어요."),
            box(0.11, 0.345, 0.81, 0.165, "내용 줄이에요. " + L("Ecological Order Restoration") + " 여섯 가지가 여기 다 있어요."),
            box(0.11, 0.585, 0.73, 0.042, L("Ecologism") + " 는 " + L("Ecology") + " 의 기본정신이라고 적혀 있어요."),
            box(0.08, 0.705, 0.69, 0.042, "친환경건축은 " + L("Ecologism") + " 에 입각하여 건축문화를 주도하는 것이에요."),
        ]},
        {"kind": "prof", "when": WHEN, "lines": [
            "협약에 담긴 내용은 순서가 중요하다고 하셨어요. 첫째가 에너지 절감, 둘째가 대체에너지예요.",
            "덜 써야 대체에너지로 제로 에너지가 된다고 하셨어요.",
            "교재에 생태학의 정의가 없어서 생물체 간의 상호 관계에 대한 학문이라고 추가해 두셨대요.",
            "조상이 망친 생태 질서를 우리 세대에 회복시켜 보자는 것이 친환경건축의 존재 이유래요.",
        ]},
    ],
    "pass3": [
        {"kind": "check", "q": L("Ecologism") + " 의 뜻으로 맞는 것은?", "choices": [
            "생물체간의 상호 관계에 대한 학문",
            "생태학의 기본정신",
            "소생물권을 조성하는 기술",
            "건물에 등급을 매기는 기준",
        ], "a": 1, "why": "학문은 " + L("Ecology") + ", 그 기본정신이 " + L("Ecologism") + " 예요."},
        {"kind": "english", "head": "시험 답안에 쓸 문장",
         "en": "친환경건축은 생태주의에 입각하여 건축문화를 주도하는 것이다.",
         "ko": L("Ecology") + " 은 학문, " + L("Ecologism") + " 는 그 기본정신, 친환경건축은 그 정신으로 건축문화를 이끌어요.",
         "tip": "학문 다음 정신 다음 건축, 세 칸 순서로 외워요."},
        {"kind": "warn", "head": "헷갈리기 쉬운 점", "items": [
            "여섯 가지의 마지막은 소생물권 " + L("Biotop") + " 조성이에요. 순서를 바꾸지 않게 조심해요.",
            L("Rio Conference") + " 는 1992년, " + L("Kyoto Protocol") + " 는 1997년이에요.",
        ]},
    ],
    "pass4": [],
})

# ---------------------------------------------------------------- p20
slides.append({
    "p": 20,
    "title": "기계론적 세계관 vs 생태학적 세계관, 그리고 건축가 세 사람",
    "terms": ["Mechanistic Worldview", "Ecological Worldview", "Machine Aesthetic",
              "Organic Architecture", "Falling water"],
    "pass1": [
        {"kind": "say", "lines": [
            "건물을 기계로 볼지, 살아 있는 몸으로 볼지가 갈리는 쪽이에요.",
            L("Mechanistic Worldview") + " 은 인간중심, " + L("Ecological Worldview") + " 은 자연중심이에요.",
            "자연 편에 선 건축가 세 사람이 시대 순서로 나와요.",
        ]},
        {"kind": "analogy", "head": "자동차와 사람 몸",
         "scene": "자동차는 부품을 조립하면 어디서나 똑같이 굴러가요. 사람 몸은 피부로 숨 쉬고 땀 흘리며 주변과 주고받아요.",
         "map": [
             ["부품을 조립한 자동차", L("Mechanistic Worldview") + " 건축 (인간중심)"],
             ["주변과 주고받는 사람 몸", L("Ecological Worldview") + " 건축 (자연중심)"],
             ["피부로 바깥과 통하기", "자연환경과 인공환경의 열린 소통체계"],
         ]},
    ],
    "pass2": [
        {"kind": "points", "head": "용어 먼저", "items": [
            L("Mechanistic Worldview") + " 은 세상을 기계처럼 보는 인간중심의 눈이에요.",
            L("Ecological Worldview") + " 은 세상을 살아 있는 관계로 보는 자연중심의 눈이에요.",
            L("Machine Aesthetic") + " 은 기계처럼 반듯한 모습을 아름답다고 보는 생각이에요.",
            L("Organic Architecture") + " 은 건축을 자연과 어우러진 살아 있는 몸처럼 짓자는 생각이에요.",
        ]},
        {"kind": "compare", "head": "두 세계관 비교: 인간 vs 자연",
         "cols": ["항목", "기계론적 세계관 건축", "생태학적 세계관 건축"],
         "rows": [
             ["중심", "인간중심", "자연중심"],
             ["위치", "20세기 건축 발전의 바탕", "주류에서 일탈한 건축이념"],
             ["이념", L("Machine Aesthetic") + " 적 건축이념", L("Organic Architecture")],
             ["한 일", "20세기 건축 발전을 이끌었어요", "기하학적 미학에서 벗어나 자연과 조화"],
             ["더", "자료 표기 없음", "자연환경과 인공환경의 열린 소통체계 중시"],
         ]},
        {"kind": "points", "head": L("Organic Architecture") + " 인물 세 사람", "items": [
            "1910년대 F.L Wright. 대표작이 " + L("Falling water") + " 이에요.",
            "1920년대 후반 Le Corbusier. 다음 쪽에 프랑스 롱샹 성당이 나와요.",
            "1930년대 E.Saarinen. 케네디 공항 TWA 터미널과 의자 디자인이 나와요.",
            "십, 이십, 삼십년대 순서로 라이트, 르 코르뷔지에, 사리넨이에요.",
        ]},
        {"kind": "look", "head": "슬라이드 짚어 읽기", "boxes": [
            box(0.11, 0.225, 0.70, 0.045, "맨 위 줄이에요. 인간 대 자연으로 두 세계관을 맞세워요."),
            box(0.11, 0.345, 0.37, 0.042, L("Mechanistic Worldview") + " 건축, 괄호에 인간중심이라고 적혀 있어요."),
            box(0.14, 0.405, 0.60, 0.042, "20세기 건축 발전의 바탕이 된 " + L("Machine Aesthetic") + " 적 건축이념이에요."),
            box(0.08, 0.525, 0.40, 0.042, L("Ecological Worldview") + " 건축, 괄호에 자연중심이라고 적혀 있어요."),
            box(0.14, 0.585, 0.31, 0.042, "주류에서 일탈한 건축이념이라고 적혀 있어요."),
            box(0.16, 0.645, 0.79, 0.125, "건축가 세 사람이 연도와 함께 묶여 " + L("Organic Architecture") + " 으로 이어져요."),
        ]},
        {"kind": "prof", "when": WHEN, "lines": [
            "시험 때는 네 가지만 알자고 하셨어요. 기계론적 세계관은 근대건축, 생태학적 세계관은 친환경건축이에요.",
            "기계론적은 인간 중심주의, 생태학적은 자연 중심주의예요.",
            "기계론적은 대량생산과 대량소비, 생태학적은 소량 다품종 생산과 지역적 소비예요.",
            "도구적 이성과 변증법적 이성은 표현이 어려워 외우지 않아도 된다고 하셨어요.",
        ]},
    ],
    "pass3": [
        {"kind": "check", "q": L("Ecological Worldview") + " 건축에 대한 설명으로 옳지 않은 것은?", "choices": [
            "자연중심이다.",
            "주류에서 일탈한 건축이념이다.",
            "20세기 건축 발전의 바탕이 된 기계미학적 건축이념이다.",
            "자연환경과 인공환경의 열린 소통체계를 중시한다.",
        ], "a": 2, "why": L("Machine Aesthetic") + " 적 건축이념은 " + L("Mechanistic Worldview") + " 건축 쪽이에요."},
        {"kind": "warn", "head": "헷갈리기 쉬운 점", "items": [
            L("Mechanistic Worldview") + " 은 인간중심이고 주류, " + L("Ecological Worldview") + " 은 자연중심이고 일탈이에요.",
            "세 사람의 순서는 Wright, Le Corbusier, Saarinen 이에요. " + L("Falling water") + " 는 Wright 예요.",
        ]},
    ],
    "pass4": [],
})

# ---------------------------------------------------------------- p21
slides.append({
    "p": 21,
    "title": "F.L Wright: Falling water (낙수장)",
    "terms": ["Falling water", "Organic Architecture"],
    "pass1": [
        {"kind": "say", "lines": [
            "폭포 위에 앉은 집 사진이에요.",
            "F.L Wright 의 " + L("Falling water") + " 이고, " + L("Organic Architecture") + " 의 대표작이에요.",
        ]},
    ],
    "pass2": [
        {"kind": "look", "head": "사진 짚어 보기", "boxes": [
            box(0.11, 0.205, 0.40, 0.06, "캡션이에요. F.L Wright : Falling water (낙수장) 이라고 적혀 있어요."),
            box(0.07, 0.31, 0.88, 0.64, "숲과 폭포가 그대로 있고 그 위에 집이 얹혀 있어요."),
            box(0.44, 0.46, 0.28, 0.20, "가로로 길게 뻗은 테라스예요. 나뭇가지가 뻗는 모습을 닮았어요."),
        ]},
        {"kind": "prof", "when": WHEN, "lines": [
            "영문 Falling water, 우리나라에서는 낙수장이라고 하는 라이트의 역작이라고 하셨어요.",
            "보통은 폭포를 밀어버리고 집을 지었겠지만 라이트는 경관을 최대한 덜 해치려 했대요.",
            "테라스의 가로 길이도 나뭇가지가 뻗어 나가는 형태를 모방한 것이래요.",
            "실내외 석재는 그 지역 펜실베이니아에서 구했고, 가구도 전부 라이트가 설계했대요.",
        ]},
    ],
    "pass3": [
        {"kind": "check", "q": L("Falling water") + " 을 설계한 사람은 누구일까요?", "choices": [
            "F.L Wright", "Le Corbusier", "E.Saarinen", "조셉 페스톤",
        ], "a": 0, "why": L("Falling water") + " 은 1910년대 " + L("Organic Architecture") + " 의 인물 F.L Wright 의 작품이에요."},
    ],
    "pass4": [],
})

# ---------------------------------------------------------------- p22
slides.append({
    "p": 22,
    "title": "Le Corbusie: 프랑스 롱샹 성당",
    "terms": ["Organic Architecture"],
    "pass1": [
        {"kind": "say", "lines": [
            "지붕이 크게 휘어 올라간 성당 사진이에요.",
            "프랑스 롱샹 성당이고, " + L("Organic Architecture") + " 의 두 번째 사례예요.",
        ]},
    ],
    "pass2": [
        {"kind": "look", "head": "사진 짚어 보기", "boxes": [
            box(0.11, 0.225, 0.36, 0.045, "캡션이에요. 슬라이드에는 'Le Corbusie : 프랑스 롱샹 성당' 으로 적혀 있어요."),
            box(0.245, 0.305, 0.51, 0.69, "네모 반듯한 근대건축과 달리 곡면으로 된 건물이에요."),
            box(0.31, 0.42, 0.45, 0.23, "휘어 올라간 지붕이에요. 배 밑바닥처럼 두껍게 얹혀 있어요."),
        ]},
        {"kind": "prof", "when": WHEN, "lines": [
            "슬라이드의 이 건물은 빌라 사보아가 아니라 롱샹 성당이라고 짚어 주셨어요.",
            "기계론적 미학의 끝을 달리던 르 코르뷔지에가 후대에 이런 유기체적 건축물도 설계했대요.",
            "잔해를 가지고 콘크리트를 만들었고, 사면의 입면이 다 다르대요.",
            "창의 각도가 다 달라서 빛의 방향을 계산한 건물이라고 하셨어요.",
        ]},
    ],
    "pass3": [
        {"kind": "warn", "head": "헷갈리기 쉬운 점", "items": [
            "슬라이드 표기는 'Le Corbusie' 예요. 통상 표기는 'Le Corbusier' 예요.",
            "이 사진은 빌라 사보아가 아니라 롱샹 성당이에요.",
        ]},
    ],
    "pass4": [],
})

# ---------------------------------------------------------------- p23
slides.append({
    "p": 23,
    "title": "E.Saarinen: 케네디 공항 TWA 터미널 (1)",
    "terms": ["Organic Architecture"],
    "pass1": [
        {"kind": "say", "lines": [
            "공항 터미널인데 지붕이 새의 날개처럼 생겼어요.",
            "E.Saarinen 의 케네디 공항 TWA 터미널이에요.",
        ]},
    ],
    "pass2": [
        {"kind": "look", "head": "사진 짚어 보기", "boxes": [
            box(0.12, 0.20, 0.42, 0.065, "캡션이에요. E.Saarinen : 케네디 공항 TWA 터미널이에요."),
            box(0.06, 0.35, 0.88, 0.59, "옆에서 본 모습이에요. 지붕이 곡면으로 크게 휘어요."),
            box(0.45, 0.46, 0.40, 0.24, "날개처럼 펼쳐진 지붕이에요. " + L("Organic Architecture") + " 의 모습이에요."),
        ]},
        {"kind": "prof", "when": WHEN, "lines": [
            "에로 사리넨의 케네디 공항 TWA 터미널이라고 하셨어요.",
            "옆에서 보면 새 같다고 하셨어요.",
            "네모 반듯하게 짓던 근대건축과는 방향성이 다른 것을 볼 수 있대요.",
        ]},
    ],
    "pass4": [],
    "pass3": [],
})

# ---------------------------------------------------------------- p24
slides.append({
    "p": 24,
    "title": "E.Saarinen: 케네디 공항 TWA 터미널 (2)",
    "terms": ["Organic Architecture"],
    "pass1": [
        {"kind": "say", "lines": [
            "같은 터미널을 정면에서 찍은 흑백 사진이에요.",
            "이번에는 정말 날개를 편 새처럼 보여요.",
        ]},
    ],
    "pass2": [
        {"kind": "look", "head": "사진 짚어 보기", "boxes": [
            box(0.115, 0.215, 0.42, 0.05, "캡션은 앞 쪽과 같아요. 케네디 공항 TWA 터미널이에요."),
            box(0.18, 0.31, 0.63, 0.675, "밤에 정면에서 찍은 사진이에요."),
            box(0.19, 0.58, 0.62, 0.18, "가운데가 낮고 양쪽이 올라간 지붕이 새가 날개를 편 모습이에요."),
        ]},
        {"kind": "prof", "when": WHEN, "lines": [
            "다음 장에는 정말 나는 새처럼 보인다고 하셨어요.",
            "고래를 형상화한 건축물도 있을 만큼 모티브를 자연에서 가져온 유기적 건축물이 많대요.",
            "이런 흐름이 " + L("Organic Architecture") + " 이에요.",
        ]},
    ],
    "pass3": [],
    "pass4": [],
})

# ---------------------------------------------------------------- p25
slides.append({
    "p": 25,
    "title": "E.Saarinen: Tulip Chair / Arm Chair",
    "terms": ["Organic Architecture"],
    "pass1": [
        {"kind": "say", "lines": [
            "이번에는 건물이 아니라 의자예요.",
            "왼쪽이 Tulip Chair, 오른쪽이 Arm Chair 이고 둘 다 E.Saarinen 의 작품이에요.",
        ]},
    ],
    "pass2": [
        {"kind": "look", "head": "사진 짚어 보기", "boxes": [
            box(0.11, 0.225, 0.40, 0.045, "캡션이에요. E.Saarinen : Tulip Chair / Arm Chair 예요."),
            box(0.11, 0.34, 0.41, 0.30, "왼쪽 위가 Tulip Chair 예요. 다리가 하나인 받침이 튤립 같아요."),
            box(0.10, 0.635, 0.42, 0.36, "아래 사진은 튤립 체어와 외다리 식탁을 함께 쓴 실내예요."),
            box(0.54, 0.41, 0.41, 0.40, "오른쪽이 Arm Chair 예요. 팔걸이가 몸을 감싸는 곡선이에요."),
        ]},
        {"kind": "prof", "when": WHEN, "lines": [
            "왼쪽은 튤립 체어, 오른쪽은 암체어라고 짚어 주셨어요.",
            "합판이나 플라스틱을 구부려 인체에 맞는 곡선 형태를 넣은 가구 디자이너 중 한 사람이 사리넨이래요.",
            "외다리 식탁과 의자를 보면 거의 다 사리넨을 따라 한 것이라고 하셨어요.",
        ]},
    ],
    "pass3": [
        {"kind": "check", "q": "Tulip Chair / Arm Chair 를 디자인한 사람은 누구일까요?", "choices": [
            "F.L Wright", "Le Corbusier", "E.Saarinen", "조셉 페스톤",
        ], "a": 2, "why": "의자 둘 다 E.Saarinen 의 작품이에요. " + L("Organic Architecture") + " 은 가구까지 이어졌어요."},
    ],
    "pass4": [],
})

# ---------------------------------------------------------------- p26
slides.append({
    "p": 26,
    "title": "대안건축으로서의 친환경건축: 의지와 일반적 목표 네 가지",
    "terms": ["Alternative Architecture", "Community", "Sustainable Development", "Maintenance",
              "Renewable Resources", "Habitat", "Landscape", "Consumption-dependent Economy",
              "Natural Ecosystem"],
    "pass1": [
        {"kind": "say", "lines": [
            "친환경건축이 왜 '대안' 인지 정리하는 쪽이에요.",
            "한 번 쓰고 버리던 건축 대신 " + L("Alternative Architecture") + " 을 내놓는 거예요.",
            "여기에 일반적 목표 네 가지가 나와요. 시험에 그대로 나올 수 있어요.",
        ]},
        {"kind": "analogy", "head": "일회용 컵과 도서관 책",
         "scene": "일회용 컵은 한 번 쓰고 버려서 쓰레기가 쌓여요. 도서관 책은 빌려 읽고 돌려주니 다음 사람도 또 읽어요.",
         "map": [
             ["한 번 쓰고 버리는 일회용 컵", L("Consumption-dependent Economy")],
             ["빌려 읽고 돌려주는 책", "자연의 순환체계와 " + L("Renewable Resources") + " 활용"],
             ["도서관의 한 회원이 되기", "건축을 " + L("Natural Ecosystem") + " 의 일부로 편입"],
         ]},
    ],
    "pass2": [
        {"kind": "points", "head": "용어 먼저", "items": [
            L("Alternative Architecture") + " 은 기존 건축을 반성하고 새 길을 내놓는 건축이에요.",
            L("Maintenance") + " 는 다 지은 건물을 쓰면서 고치고 돌보는 일이에요.",
            L("Renewable Resources") + " 은 써도 자연이 다시 채워 주는 자원이에요.",
            L("Habitat") + " 은 동물과 식물이 자리 잡고 사는 것, " + L("Landscape") + " 은 건물 주위 풍경이에요.",
        ]},
        {"kind": "points", "head": "의지 두 줄", "items": [
            "구조 방식에서부터 설비, 재처리시설까지 자연친화적 환경을 조성하여,",
            "더불어 사는 " + L("Community") + " 와 " + L("Sustainable Development") + " 적 대안을 찾아가자는 의지예요.",
        ]},
        {"kind": "points", "head": "일반적 목표 네 가지", "items": [
            "1) 건축물 시공과 " + L("Maintenance") + " 에 필요한 에너지 & 자원의 수요 최소화",
            "2) 자연의 순환체계와 " + L("Renewable Resources") + " 활용",
            "3) 다양한 종의 동물과 식물의 " + L("Habitat") + " 가능",
            "4) 건축물을 주위 " + L("Landscape") + " 과 어우러지게 배치, 건강한 생활 가능케 함",
        ]},
        {"kind": "points", "head": "앞글자로 외우기: 최순서경", "items": [
            "최: 시공과 " + L("Maintenance") + " 의 에너지 & 자원 수요 최소화",
            "순: 자연의 순환체계와 " + L("Renewable Resources"),
            "서: 다양한 종의 동물과 식물의 " + L("Habitat"),
            "경: 주위 " + L("Landscape") + " 과 어우러진 배치와 건강한 생활",
        ]},
        {"kind": "points", "head": "맨 아래 두 줄: 왜 대안일까요?", "items": [
            "기존의 일방적인 " + L("Consumption-dependent Economy") + " 가 과소비와 환경오염을 야기했어요.",
            "그래서 건축 자체도 " + L("Natural Ecosystem") + " 의 일부로 편입시켜 전체 시스템을 구성해요.",
            "주문: " + MANTRA,
        ]},
        {"kind": "look", "head": "슬라이드 짚어 읽기", "boxes": [
            box(0.11, 0.245, 0.79, 0.105, "의지 두 줄이에요. " + L("Community") + " 와 " + L("Sustainable Development") + " 적 대안을 찾아가자는 말이에요."),
            box(0.11, 0.365, 0.14, 0.042, "'일반적 목표' 라고 적힌 작은 제목이에요."),
            box(0.13, 0.425, 0.75, 0.105, "목표 1과 2예요. 수요 최소화와 " + L("Renewable Resources") + " 활용이에요."),
            box(0.13, 0.545, 0.74, 0.105, "목표 3과 4예요. 동식물 " + L("Habitat") + " 과 " + L("Landscape") + " 배치예요."),
            box(0.085, 0.725, 0.78, 0.042, L("Consumption-dependent Economy") + " 가 과소비와 환경오염을 불렀어요."),
            box(0.085, 0.785, 0.75, 0.042, "건축 자체도 " + L("Natural Ecosystem") + " 의 일부로 편입시켜요."),
        ]},
        {"kind": "prof", "when": WHEN, "lines": [
            "대안건축으로서 친환경건축의 목표가 넷이라고 하셨어요.",
            "셋째는 동물과 식물의 서식 가능성을 건축 환경에서 보장하는 것이래요.",
            "생태학적 접근은 시공, 유지, 폐기까지 건물의 전 생애 주기에 걸쳐 한다고 하셨어요.",
            "기술이 인간을 해치면 안 된다고 하셨어요.",
        ]},
    ],
    "pass3": [
        {"kind": "check", "q": "옥상과 외벽에 새와 곤충이 머물 식재 공간을 만들었어요. 가장 가까운 일반적 목표는?", "choices": [
            "에너지 & 자원의 수요 최소화",
            "자연의 순환체계와 재생이 가능한 자원 활용",
            "다양한 종의 동물과 식물의 서식 가능",
            "주위 경관과 어우러진 배치",
        ], "a": 2, "why": "새와 곤충이 살 자리를 만드는 것은 목표 3, 동식물의 " + L("Habitat") + " 이에요."},
        {"kind": "english", "head": "시험 답안에 쓸 문장",
         "en": "시공과 유지관리 에너지 최소화, 재생이 가능한 자원 활용, 동식물의 서식 가능, 경관과 어우러진 배치다.",
         "ko": L("Alternative Architecture") + " 으로서 친환경건축의 일반적 목표 네 가지예요.",
         "tip": "최순서경 네 글자로 순서까지 같이 외워요."},
        {"kind": "warn", "head": "헷갈리기 쉬운 점", "items": [
            "목표 1은 수요 '최소화' 예요. 공급 확대가 아니고, 시공과 " + L("Maintenance") + " 두 단계 모두예요.",
            "건축은 " + L("Natural Ecosystem") + " 과 분리된 독립 시스템이 아니라 그 일부로 편입돼요.",
            "의지 줄의 두 낱말은 " + L("Community") + " 와 " + L("Sustainable Development") + " 이에요.",
        ]},
    ],
    "pass4": [],
})

# ---------------------------------------------------------------- p27
slides.append({
    "p": 27,
    "title": "설계 개요: 순환고리를 찾는 설계와 One-Way Process",
    "terms": ["Circulation Loop", "One-Way Process", "Circulation System",
              "Human-centered Design Methodology", "Environmental Load", "Comfort"],
    "pass1": [
        {"kind": "say", "lines": [
            "여기서부터 순환 이야기예요.",
            "기존 건축은 들어온 것이 더러워져 나가기만 하는 " + L("One-Way Process") + " 였어요.",
            "친환경건축은 건물과 주변환경 사이의 " + L("Circulation Loop") + " 를 찾아요.",
            "주문: " + MANTRA,
        ]},
    ],
    "pass2": [
        {"kind": "points", "head": "용어 먼저", "items": [
            L("Human-centered Design Methodology") + " 은 사람 편한 것만 생각하던 옛 설계 방식이에요.",
            L("Circulation Loop") + " 는 건물과 주변환경이 서로 주고받으며 도는 연결 고리예요.",
            L("Environmental Load") + " 는 건물이 지구와 주변환경에 지우는 짐이에요.",
            L("Comfort") + " 은 건물 안 사람이 편하고 기분 좋게 지내는 상태예요.",
        ]},
        {"kind": "points", "head": "글 네 줄 그대로", "items": [
            L("Human-centered Design Methodology") + " 에 대한 회의감에서 비롯됐어요.",
            "개별건축물과 주변환경과의 상호간 " + L("Circulation Loop") + " 를 찾는 것에서 시작해요.",
            "에너지, 재료, 녹지, 대기, 물과의 관계 속에서 건축물을 해석해요.",
            "목표는 지구와 외부환경의 부하 절감 및 인간의 " + L("Comfort") + " 이에요.",
        ]},
        {"kind": "compare", "head": "왼쪽 그림 " + L("One-Way Process") + " 의 네 줄",
         "cols": ["흐름", "들어오는 것", "나가는 것"],
         "rows": [
             ["공기", "Fresh Air", "Dirty Air"],
             ["에너지", "Energy(Electronic/Gas)", "Energy(Heating Air)"],
             ["물", "Clean Water", "Dirty Water"],
             ["제품", "Product", "Trash"],
         ]},
        {"kind": "points", "head": "오른쪽 그림: 친환경건축", "items": [
            "가운데에 Circulation 이라고 적혀 있고 둘레를 Energy, Air, Material, Water 가 감싸요.",
            "이것이 다섯 " + L("Circulation System") + " 중 네 가지이고, 왼쪽 나무 그림이 녹지예요.",
            "곧 에너지, 재료, 녹지, 대기, 물 다섯 가지예요.",
        ]},
        {"kind": "look", "head": "슬라이드 짚어 읽기", "boxes": [
            box(0.11, 0.225, 0.59, 0.042, L("Human-centered Design Methodology") + " 에 대한 회의감에서 비롯됐어요."),
            box(0.11, 0.285, 0.73, 0.042, "굵게 표시된 " + L("Circulation Loop") + " 를 찾는 것에서 시작해요."),
            box(0.11, 0.345, 0.68, 0.042, "굵게 표시된 다섯 가지예요. 에너지, 재료, 녹지, 대기, 물이에요."),
            box(0.11, 0.405, 0.58, 0.042, "목표 줄이에요. 부하 절감 '및' 인간의 " + L("Comfort") + " 이에요."),
            box(0.05, 0.50, 0.48, 0.45, "왼쪽 그림이에요. " + L("One-Way Process") + ", 기존의 건축이에요."),
            box(0.55, 0.50, 0.43, 0.45, "오른쪽 그림이에요. 가운데 Circulation 이 도는 친환경건축이에요."),
        ]},
        {"kind": "prof", "when": WHEN, "lines": [
            "건물이 없었다면 비는 땅에 스며들어 지하수가 되고 바다로 나가 다시 비가 됐다고 하셨어요.",
            "건축물이 들어서면 그 면적만큼 순환이 끊긴다고 하셨어요.",
            "그림 1에서 끊기는 순환이 다섯이고, 오른쪽에 녹지가 안 적혀 있지만 왼쪽 나무가 녹지래요.",
            "순환을 고려한 친환경건축 설계의 다섯 대상은 꼭 말할 수 있어야 한다고 하셨어요.",
        ]},
    ],
    "pass3": [
        {"kind": "check", "q": L("One-Way Process") + " 의 네 줄로 옳지 않은 것은?", "choices": [
            "Fresh Air 가 Dirty Air 로",
            "Energy(Electronic/Gas) 가 Energy(Heating Air) 로",
            "Clean Water 가 Dirty Water 로",
            "Trash 가 Product 로",
        ], "a": 3, "why": "Product 가 Trash 로 가요. 방향을 뒤집으면 " + L("One-Way Process") + " 가 아니에요."},
        {"kind": "english", "head": "시험 답안에 쓸 문장",
         "en": "순환을 고려한 친환경건축 설계의 대상은 에너지, 재료, 녹지, 대기, 물 다섯 가지다.",
         "ko": "다섯 " + L("Circulation System") + " 이고, 목표는 " + L("Environmental Load") + " 절감과 인간의 " + L("Comfort") + " 이에요.",
         "tip": "앞글자로 '에재녹대물' 이라고 외워요."},
    ],
    "pass4": [],
})

# ---------------------------------------------------------------- p28
slides.append({
    "p": 28,
    "title": "순환체계별 적용기술 다섯 줄 (표3)",
    "terms": ["Applied Technology", "Circulation System", "Renewable Energy",
              "Regional Green Network", "Rainwater", "Wastewater", "Infiltration"],
    "pass1": [
        {"kind": "say", "lines": [
            "다섯 " + L("Circulation System") + " 마다 실제로 쓰는 방법이 한 줄씩 적힌 표예요.",
            "이 다섯 줄이 " + L("Applied Technology") + " 이고, 앞으로 배울 내용의 목차예요.",
        ]},
    ],
    "pass2": [
        {"kind": "points", "head": "용어 먼저", "items": [
            L("Applied Technology") + " 은 순환체계마다 실제 설계에 쓰는 방법 한 줄이에요.",
            L("Rainwater") + " 는 하늘에서 내린 빗물, " + L("Wastewater") + " 는 쓰고 난 더러워진 물이에요.",
            L("Infiltration") + " 는 빗물이 흙 속으로 스며드는 것이에요.",
            L("Regional Green Network") + " 는 단지를 넘어 넓게 이어진 녹지 연결망이에요.",
        ]},
        {"kind": "compare", "head": "표3: " + L("Circulation System") + " 별 " + L("Applied Technology"),
         "cols": ["순환체계", "적용기술"],
         "rows": [
             ["에너지", L("Renewable Energy") + " 를 위주로 에너지 순환 도모"],
             ["건축재료", "자연순환적 재료 채택, 생산과 운송에 사용되는 에너지 최소화"],
             ["녹지", L("Regional Green Network") + " 와의 연계성 고려"],
             ["물", "빗물과 " + L("Wastewater") + " 분리, " + L("Rainwater") + " 는 " + L("Infiltration") + " 유도"],
             ["대기", "실내외의 공기 순환"],
         ]},
        {"kind": "points", "head": "한 줄씩 쉬운 말로", "items": [
            "에너지는 " + L("Renewable Energy") + ", 재료는 자연순환과 운송 에너지 줄이기예요.",
            "녹지는 " + L("Regional Green Network") + " 와 이어 주기예요.",
            "물은 " + L("Rainwater") + " 와 " + L("Wastewater") + " 를 나누고 빗물은 땅에 " + L("Infiltration") + " 시켜요.",
            "대기는 실내외 공기가 돌게 해요.",
        ]},
        {"kind": "look", "head": "슬라이드 짚어 읽기", "boxes": [
            box(0.11, 0.225, 0.30, 0.042, "표3 제목이에요. 순환체계별 " + L("Applied Technology") + " 이에요."),
            box(0.12, 0.345, 0.59, 0.042, "에너지 줄이에요. " + L("Renewable Energy") + " 위주예요."),
            box(0.12, 0.405, 0.84, 0.042, "건축재료 줄이에요. 생산과 운송 에너지까지 줄여요."),
            box(0.12, 0.465, 0.44, 0.042, "녹지 줄이에요. " + L("Regional Green Network") + " 와의 연계성이에요."),
            box(0.12, 0.525, 0.47, 0.042, "물 줄이에요. 분리하고 " + L("Infiltration") + " 를 유도해요."),
            box(0.12, 0.585, 0.32, 0.042, "대기 줄이에요. 실내외의 공기 순환이에요."),
        ]},
        {"kind": "prof", "when": WHEN, "lines": [
            "표 3의 활용 기술에 BIPV 같은 낯선 말이 있는데 다 앞으로 배울 것이라고 하셨어요.",
            "중간고사 때쯤 표 3을 보면 무슨 말인지 다 알게 된다고 하셨어요.",
        ]},
    ],
    "pass3": [
        {"kind": "check", "q": L("Circulation System") + " 과 " + L("Applied Technology") + " 의 연결로 옳지 않은 것은?", "choices": [
            "에너지: 신재생 에너지를 위주로 에너지 순환 도모",
            "녹지: 광역녹지체계와의 연계성 고려",
            "물: 빗물과 오수 분리, 우수는 침투 유도",
            "대기: 생산과 운송에 사용되는 에너지 최소화",
        ], "a": 3, "why": "생산과 운송 에너지 최소화는 건축재료 줄이에요. 대기는 실내외의 공기 순환이에요."},
        {"kind": "warn", "head": "헷갈리기 쉬운 점", "items": [
            "'" + L("Regional Green Network") + " 와의 연계성' 은 녹지, '실내외의 공기 순환' 은 대기예요.",
            L("Rainwater") + " 는 저장하고 " + L("Infiltration") + " 시키고, " + L("Wastewater") + " 는 따로 처리해요.",
        ]},
    ],
    "pass4": [],
})

# ---------------------------------------------------------------- p29
slides.append({
    "p": 29,
    "title": "1) 에너지 순환체계: 신재생에너지와 미기후",
    "terms": ["Fossil Energy", "Renewable Energy", "Microclimate", "Broadleaf Tree",
              "Conifer", "Biomass", "Alternative Energy"],
    "pass1": [
        {"kind": "say", "lines": [
            "다섯 순환 중 첫 번째, 에너지 차례예요.",
            "탄소를 내지 않는 " + L("Renewable Energy") + " 를 쓰고, " + L("Microclimate") + " 를 이용해 냉난방을 줄여요.",
            "나무 심는 자리만 잘 골라도 냉난방비가 줄어요.",
        ]},
        {"kind": "analogy", "head": "건물에 입히는 겨울 패딩",
         "scene": "겨울에 찬바람이 부는 쪽은 패딩으로 꽁꽁 감싸요. 건물 둘레의 나무도 바람 쪽은 막고 해 드는 쪽은 열어 줘요.",
         "map": [
             ["사람 몸", "건물"],
             ["찬바람 쪽을 감싼 겨울 패딩", "북쪽의 " + L("Conifer")],
             ["몸 바로 옆의 공기", L("Microclimate") + " (지표면에서 1.5m 정도까지)"],
         ]},
    ],
    "pass2": [
        {"kind": "points", "head": "용어 먼저", "items": [
            L("Fossil Energy") + " 는 석유, 석탄처럼 캐서 쓰고 나면 없어지는 에너지예요.",
            L("Renewable Energy") + " 는 탄소를 내보내지 않고 자연에서 다시 얻는 에너지예요.",
            L("Microclimate") + " 는 지표면에서 1.5m 정도까지의 기후예요.",
            L("Broadleaf Tree") + " 는 잎이 넓은 나무, " + L("Conifer") + " 는 잎이 바늘 같은 나무예요.",
        ]},
        {"kind": "points", "head": "배경 세 줄", "items": [
            L("Fossil Energy") + " 자원 고갈이 예상돼요.",
            "지속적인 지구온난화 진행 및 이상기후현상이 나타나요.",
            "한정된 에너지, 환경오염에 관한 에너지원 고민이 필요해요. 답은 대안에너지예요.",
        ]},
        {"kind": "points", "head": "에너지 순환 방법 두 가지", "items": [
            "1) 탄소를 배출하지 않는 " + L("Renewable Energy") + " 위주의 건축계획이에요.",
            "2) " + L("Microclimate") + " 를 이용한 냉난방 설계계획이에요.",
            "괄호 안 설명 그대로 " + L("Microclimate") + " 는 지표면에서 1.5m 정도까지의 기후예요.",
            "예시는 남쪽의 " + L("Broadleaf Tree") + " + 북쪽의 " + L("Conifer") + " 예요. 앞글자로 남활북침이에요.",
        ]},
        {"kind": "points", "head": L("Alternative Energy") + " 목록", "items": [
            "태양에너지(광/열), 풍력, 조력, 파력, 지열, " + L("Biomass") + " 등이에요.",
            "앞글자로 태풍조파지바예요.",
            "석탄, 석유 같은 " + L("Fossil Energy") + " 는 이 목록에 없어요.",
            "그리고 설계 초기부터의 통합적 고려가 필요해요.",
        ]},
        {"kind": "look", "head": "슬라이드 짚어 읽기", "boxes": [
            box(0.11, 0.245, 0.76, 0.165, "배경 세 줄이에요. 맨 끝에 대안에너지라고 적혀 있어요."),
            box(0.11, 0.485, 0.14, 0.042, "'에너지 순환' 이라고 적힌 작은 제목이에요."),
            box(0.14, 0.545, 0.61, 0.042, "방법 1이에요. 탄소를 배출하지 않는 " + L("Renewable Energy") + " 위주예요."),
            box(0.14, 0.605, 0.79, 0.042, "방법 2예요. 괄호에 1.5m 정도까지라고 적혀 있어요."),
            box(0.18, 0.665, 0.39, 0.042, "예시 줄이에요. 남쪽의 " + L("Broadleaf Tree") + " + 북쪽의 " + L("Conifer") + " 예요."),
            box(0.11, 0.785, 0.78, 0.105, L("Alternative Energy") + " 목록과 설계 초기부터의 통합적 고려예요."),
        ]},
        {"kind": "prof", "when": WHEN, "lines": [
            "에너지 순환의 핵심은 탄소를 배출하지 않는 신재생에너지를 만들어 내는 것이래요. 다만 덜 쓰는 것이 먼저예요.",
            "미기후는 지표면에서 1.5m 정도 높이의 기후대, 곧 사람이 계속 접하는 지표면의 대기래요.",
            "남쪽 활엽수는 여름에 햇빛을 가리고 가을에 잎이 져서 겨울에는 해가 들어온다고 하셨어요.",
            "북쪽 침엽수는 겨울에도 잎이 있어 북서풍을 막아 난방 에너지를 줄여 준대요.",
        ]},
    ],
    "pass3": [
        {"kind": "check", "q": L("Microclimate") + " 의 뜻으로 맞는 것은?", "choices": [
            "지표면에서 1.5m 정도까지의 기후",
            "지표면에서 15m 정도까지의 기후",
            "한 나라 전체의 평균 기후",
            "건물 안의 공기 상태",
        ], "a": 0, "why": "슬라이드 괄호 그대로 지표면에서 1.5m 정도까지의 기후예요."},
        {"kind": "check", "q": "슬라이드의 " + L("Alternative Energy") + " 목록에 없는 것은?", "choices": [
            "조력", "파력", "바이오매스", "석탄",
        ], "a": 3, "why": "목록은 태양에너지(광/열), 풍력, 조력, 파력, 지열, " + L("Biomass") + " 등이에요. 석탄은 " + L("Fossil Energy") + " 예요."},
        {"kind": "warn", "head": "헷갈리기 쉬운 점", "items": [
            L("Microclimate") + " 는 1.5m 예요. 15m 나 150m 가 아니에요.",
            "남쪽이 " + L("Broadleaf Tree") + ", 북쪽이 " + L("Conifer") + " 예요. 뒤집으면 틀려요.",
        ]},
    ],
    "pass4": [],
})

# ---------------------------------------------------------------- p30
slides.append({
    "p": 30,
    "title": "2) 건축재료 순환체계: 돌아가는 재료를 먼저",
    "terms": ["Local Natural Material", "Recycling", "Environmental Load", "Modern Architecture"],
    "pass1": [
        {"kind": "say", "lines": [
            "다섯 순환 중 두 번째, 재료 차례예요.",
            "흙과 나무는 묻으면 자연으로 돌아가고, 철과 콘크리트와 유리는 그렇지 않아요.",
            "그래서 " + L("Local Natural Material") + " 와 " + L("Recycling") + " 자재를 먼저 골라요.",
        ]},
    ],
    "pass2": [
        {"kind": "points", "head": "용어 먼저", "items": [
            L("Local Natural Material") + " 는 주변에서 구하기 쉽고 자연에서 온 건축 재료예요.",
            L("Recycling") + " 은 쓰던 자재를 버리지 않고 다시 살려 쓰는 것이에요.",
            L("Environmental Load") + " 는 건물이 지구와 주변환경에 지우는 짐이에요.",
        ]},
        {"kind": "compare", "head": "옛 건축 재료와 " + L("Modern Architecture") + " 재료",
         "cols": ["구분", "옛 건축", "현대건축"],
         "rows": [
             ["재료", "흙, 나무", "철, 콘크리트, 유리 등"],
             ["쓰는 동안", "자연에서 온 재료", "유해 물질 발생"],
             ["버린 뒤", "쉽게 자연으로 돌아감", "폐기 후 " + L("Environmental Load") + " 가중"],
         ]},
        {"kind": "points", "head": "건축재료 선택 원칙 한 줄", "items": [
            "주변에서 구하기 쉽고, " + L("Local Natural Material") + " 와,",
            L("Recycling") + ", 재사용 및 재생가능한 자재를,",
            "우선적으로 선택하여 디자인해요.",
            "표3의 재료 줄과 같은 말이에요. 자연순환적 재료 채택, 생산과 운송 에너지 최소화예요.",
        ]},
        {"kind": "look", "head": "슬라이드 짚어 읽기", "boxes": [
            box(0.11, 0.245, 0.65, 0.042, "옛 건축의 흙, 나무는 쉽게 자연으로 돌아가는 재료라고 적혀 있어요."),
            box(0.11, 0.305, 0.67, 0.105, L("Modern Architecture") + " 재료는 유해 물질 발생과 폐기 후 " + L("Environmental Load") + " 가중이에요."),
            box(0.08, 0.485, 0.74, 0.105, "결론 줄이에요. " + L("Local Natural Material") + " 와 " + L("Recycling") + " 자재를 우선 선택해요."),
        ]},
        {"kind": "prof", "when": WHEN, "lines": [
            "재료 순환은 앞서 본 토속건축 그 자체라고 하셨어요.",
            "한 줄로 요약하면 주변에서 구하자, 그중 자연적인 재료를 쓰자, 쓴 것은 재활용하자래요.",
            "재활용을 생각하면 왁싱과 코팅을 많이 하지 않는다고 하셨어요.",
            "애초에 재활용할 것을 생각해서 가공하라는 이야기예요.",
        ]},
    ],
    "pass3": [
        {"kind": "check", "q": "건축재료 순환체계의 선택 원칙으로 맞는 것은?", "choices": [
            "철과 콘크리트와 유리의 사용을 법으로 금지한다",
            "지역적 자연적 재료와 재활용 자재를 우선적으로 선택한다",
            "값이 가장 싼 재료를 먼저 고른다",
            "수입 재료를 우선한다",
        ], "a": 1, "why": "슬라이드는 " + L("Local Natural Material") + " 와 " + L("Recycling") + " 자재를 '우선적으로 선택' 하라고 해요."},
        {"kind": "warn", "head": "헷갈리기 쉬운 점", "items": [
            "철, 콘크리트, 유리를 금지한 것이 아니에요. 좋은 재료를 우선적으로 선택하라는 말이에요.",
            L("Environmental Load") + " 가중은 폐기 '후' 의 이야기예요.",
        ]},
    ],
    "pass4": [],
})

# ---------------------------------------------------------------- p31
slides.append({
    "p": 31,
    "title": "3) 녹지 순환체계: 방법 두 가지와 생태녹지의 기능",
    "terms": ["Regional Green Network", "Transpiration", "Heat Island", "Circulation System"],
    "pass1": [
        {"kind": "say", "lines": [
            "다섯 순환 중 세 번째, 녹지 차례예요.",
            "녹지를 만드는 방법이 두 가지, 녹지가 해 주는 일이 여러 가지예요.",
            "건물 밖을 녹지로 만들고, 더 나아가 건물 자체를 녹화해요.",
        ]},
        {"kind": "analogy", "head": "땀 흘리는 몸, 초록 피부",
         "scene": "더운 날 사람은 땀을 흘려 몸을 식혀요. 식물도 잎으로 물을 내보내 주변을 식혀요.",
         "map": [
             ["땀이 마르며 몸이 식음", "식물의 " + L("Transpiration") + " 으로 온도 저감"],
             ["사람 몸의 피부", "건물의 외피, 곧 입면과 지붕"],
             ["피부를 덮어 주는 옷", "토양층이 콘크리트 노화를 막아 줌"],
         ]},
    ],
    "pass2": [
        {"kind": "points", "head": "용어 먼저", "items": [
            L("Transpiration") + " 은 식물이 잎으로 물을 수증기로 내보내 주변을 식히는 일이에요.",
            L("Heat Island") + " 은 도시가 주변보다 섬처럼 뜨거워지는 현상이에요.",
            L("Regional Green Network") + " 는 단지를 넘어 넓게 이어진 녹지 연결망이에요.",
        ]},
        {"kind": "compare", "head": "녹지를 만드는 방법 두 가지", "cols": ["방법", "내용"], "rows": [
            ["기본", "건축물을 제외한 공간을 녹지로 활용하여 구성"],
            ["적극적", "건축물 자체를 녹화 (입면, 지붕 등을 녹화)"],
        ]},
        {"kind": "points", "head": "생태녹지 및 조경의 기능 (앞쪽 네 줄)", "items": [
            "이산화탄소 흡수: 공기질 향상이에요.",
            "증발 및 " + L("Transpiration") + ": " + L("Heat Island") + " 제거, 온도 저감이에요.",
            "열환경 개선(단열)이에요.",
            "우수유출조절, 과잉 건조 완화예요.",
        ]},
        {"kind": "points", "head": "추가기능 두 줄과 외우는 말", "items": [
            "추가기능 1: 소리 흡수로 소음경감이에요.",
            "추가기능 2: 건축물 내구성 향상이에요. 토양층이 콘크리트 노화를 방지해요.",
            "앞글자로 이증단우소내라고 외워요.",
            "녹지도 다섯 " + L("Circulation System") + " 의 하나예요. 주문: " + MANTRA,
        ]},
        {"kind": "look", "head": "슬라이드 짚어 읽기", "boxes": [
            box(0.11, 0.245, 0.77, 0.042, "주변 생태환경과 연계하는 녹지를 건축물과 유기적 관계 속에서 조성해요."),
            box(0.11, 0.305, 0.59, 0.042, "방법 1이에요. 건축물을 제외한 공간을 녹지로 활용해요."),
            box(0.17, 0.365, 0.62, 0.042, "방법 2예요. 적극적으로 건축물 자체를 녹화해요."),
            box(0.11, 0.485, 0.28, 0.042, "'생태녹지 및 조경의 기능' 이라고 적힌 작은 제목이에요."),
            box(0.13, 0.545, 0.56, 0.165, "기능 앞 세 줄이에요. 이산화탄소 흡수, " + L("Transpiration") + ", 열환경 개선이에요."),
            box(0.13, 0.725, 0.73, 0.165, "우수유출조절과 추가기능 두 줄이에요. 소음경감과 내구성 향상이에요."),
        ]},
        {"kind": "prof", "when": WHEN, "lines": [
            "이미 대지는 훼손됐으니 남아 있는 녹지와 건물을 연계시키겠다는 것이 녹지 순환이래요.",
            "방법은 둘, 건축물을 제외한 공간을 다 녹지로 만들기와 옥상과 벽면까지 녹화하는 적극적인 방법이에요.",
            "피부에 알코올 솜을 대면 시원한 것처럼, 식물이 수분을 증발시키며 열섬화를 줄인다고 하셨어요.",
            "우수는 빗물이고, 식물이 흙 속에 빗물을 저장해 주어서 도시 홍수를 막는다고 하셨어요.",
        ]},
    ],
    "pass3": [
        {"kind": "check", "q": "증발 및 " + L("Transpiration") + " 이 하는 일로 맞는 것은?", "choices": [
            "열섬화 현상 제거, 온도 저감",
            "빗물을 지하 탱크에 모음",
            "실내 공기질만 좋게 함",
            "콘크리트를 빨리 굳게 함",
        ], "a": 0, "why": "슬라이드 그대로 " + L("Heat Island") + " 제거와 온도 저감이에요."},
        {"kind": "english", "head": "시험 답안에 쓸 문장",
         "en": "이산화탄소 흡수, 증발 및 증산작용, 열환경 개선, 우수유출조절이 생태녹지의 기능이다.",
         "ko": "추가기능으로 소음경감과 건축물 내구성 향상도 있어요.",
         "tip": "이증단우소내 여섯 글자로 외워요."},
        {"kind": "warn", "head": "헷갈리기 쉬운 점", "items": [
            "방법 두 가지 중 '적극적' 인 쪽이 건축물 자체를 녹화하는 쪽이에요.",
            "내구성 향상의 이유는 토양층이 콘크리트 노화를 막아 주기 때문이에요.",
        ]},
    ],
    "pass4": [],
})

data = {
    "deck": "E1",
    "from": 17,
    "to": 31,
    "glossary": pick(*GLOSS_NAMES),
    "slides": slides,
}

with open(OUT, "w", encoding="utf-8", newline="\n") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
    f.write("\n")
print("wrote", OUT, len(slides), "slides")
