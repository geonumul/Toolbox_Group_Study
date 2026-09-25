# -*- coding: utf-8 -*-
"""기초 다지기(week b) 슬라이드 그림 도우미.

build_slides_wb.py 가 불러 쓴다. 모든 함수는 SVG 조각 목록을 돌려주며,
실제 검사(겹치는 글자, 화면 밖 글자)는 icslide_lib.fig 가 한다.
색은 절대 쓰지 않고 클래스(n, n2, n3, n4, e, e2, arrow, t, tb, tm, tl, box, box2, hl)만 쓴다.
"""
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from icslide_lib import R, C, L, TX, A, PL, PG, PATH, BOX, HAT  # noqa: F401


# ---------------------------------------------------------------- 기본 흐름
def hrow(labels, y=110, h=52, bw=104, gap=16, fs=15, hi=None, b0=1, sub=14):
    """왼쪽에서 오른쪽으로 가는 흐름. labels: [글자] 또는 [(위, 아래)]"""
    n = len(labels)
    x0 = (480.0 - (n * bw + (n - 1) * gap)) / 2.0
    els = []
    for i, lab in enumerate(labels):
        x = x0 + i * (bw + gap)
        if isinstance(lab, tuple):
            lines = [(lab[0], fs, "tb")] + ([(lab[1], sub, "tm")] if lab[1] else [])
        else:
            lines = [(lab, fs, "tb")]
        els.append(BOX(x, y, bw, h, lines, "box2" if hi == i else "box", b0 + i))
        if i:
            els.append(A(x - gap + 2, y + h / 2.0, x - 3, y + h / 2.0, "e2", b0 + i))
    return els


def vcol(labels, x=140, w=200, y0=18, h=44, gap=14, fs=16, hi=None, b0=1, sub=14):
    """위에서 아래로 내려가는 흐름."""
    els = []
    for i, lab in enumerate(labels):
        y = y0 + i * (h + gap)
        if isinstance(lab, tuple):
            lines = [(lab[0], fs, "tb")] + ([(lab[1], sub, "tm")] if lab[1] else [])
        else:
            lines = [(lab, fs, "tb")]
        els.append(BOX(x, y, w, h, lines, "box2" if hi == i else "box", b0 + i))
        if i:
            els.append(A(x + w / 2.0, y - gap + 1, x + w / 2.0, y - 3, "e2", b0 + i))
    return els


# ---------------------------------------------------------------- b-1
def fig_life():
    """공사 한 건의 일생 여섯 단계."""
    els = [TX(240, 26, "공사 한 건의 일생", "tb", 1, 17)]
    labs = [("사람", "누가"), ("방식", "어떻게"), ("입찰", "누구에게"),
            ("계획", "무엇을"), ("관리", "잘 되나"), ("준공", "끝내기")]
    n = len(labs)
    bw, gap = 72.0, 6.0
    x0 = (480.0 - (n * bw + (n - 1) * gap)) / 2.0
    for i, (a_, b_) in enumerate(labs):
        x = x0 + i * (bw + gap)
        els.append(BOX(x, 60, bw, 56, [(a_, 15, "tb"), (b_, 14, "tm")], "box", i + 1))
        if i:
            els.append(A(x - gap + 1, 88, x - 2, 88, "e2", i + 1))
    els.append(TX(240, 160, "여기까지가 종이 위에서 일어나는 일이에요", "tm", 6, 15))
    els.append(TX(240, 200, "사람 → 방식 → 입찰 → 계획 → 관리 → 준공", "tb", 6, 16))
    return els


def fig_site_order():
    """현장 작업 순서 네 단계."""
    els = [TX(240, 28, "현장에서 몸으로 하는 순서", "tb", 1, 17)]
    els += hrow([("가설", "발판, 보양"), ("철거", "걷어 내기"), ("경량철골", "뼈대 세우기"),
                 ("마감", "살 붙이기")], y=70, h=60, bw=104, gap=16, b0=1)
    els.append(L(20, 170, 460, 170, "e", 5))
    els.append(TX(240, 196, "가설 → 철거 → 경량철골 → 마감", "tb", 5, 17))
    els.append(TX(240, 226, "가설재는 공사가 끝나면 다 걷어 내요", "tm", 5, 15))
    return els


def fig_three_people():
    """식당 비유: 손님, 요리사, 심사위원."""
    els = [TX(240, 28, "공사는 식당 한 판", "tb", 1, 17)]
    box = [("손님", "발주자"), ("요리사", "시공자"), ("심사위원", "감리자")]
    for i, (a_, b_) in enumerate(box):
        x = 20 + i * 155
        els.append(BOX(x, 70, 140, 62, [(a_, 16, "tb"), (b_, 15, "tl")],
                       "box2" if i == 0 else "box", i + 1))
    els.append(A(160, 92, 172, 92, "e2", 2))
    els.append(A(315, 92, 327, 92, "e2", 3))
    els.append(TX(95, 165, "돈을 내고 주문", "tm", 2, 14))
    els.append(TX(250, 165, "만들어 줌", "tm", 3, 14))
    els.append(TX(405, 165, "도면대로인지 확인", "tm", 4, 14))
    els.append(TX(240, 210, "손님이 갑, 요리사가 을 이에요", "tb", 4, 16))
    return els


# ---------------------------------------------------------------- b-2
def fig_chain():
    """계약 사슬: 발주자, 원도급자, 하도급자, 감리자."""
    els = [TX(150, 26, "계약 사슬", "tb", 1, 17)]
    els.append(BOX(50, 46, 200, 48, [("발주자", 16, "tb"), ("갑, 돈을 낸다", 14, "tm")], "box2", 1))
    els.append(BOX(50, 128, 200, 48, [("원도급자", 16, "tb"), ("발주자와 직접 계약", 14, "tm")], "box", 2))
    els.append(BOX(50, 210, 200, 48, [("하도급자", 16, "tb"), ("원도급자와 계약", 14, "tm")], "box", 3))
    els.append(A(150, 96, 150, 125, "e2", 2))
    els.append(A(150, 178, 150, 207, "e2", 3))
    els.append(TX(268, 116, "돈, 지시", "tm", 2, 14, "start"))
    els.append(TX(268, 198, "돈, 지시", "tm", 3, 14, "start"))
    els.append(BOX(330, 46, 140, 48, [("감리자", 16, "tb"), ("확인만 한다", 14, "tm")], "box", 4))
    els.append(L(398, 96, 398, 152, "e", 4))
    els.append(A(398, 152, 254, 152, "e", 4))
    els.append(TX(398, 178, "도면대로인지 확인", "tm", 4, 14))
    return els


def fig_boss5():
    """현장관리자의 주요 업무 5가지."""
    els = [TX(240, 26, "현장소장이 보는 다섯 가지", "tb", 1, 17)]
    els.append(BOX(170, 50, 140, 50, [("현장소장", 16, "tb")], "box2", 1))
    labs = ["공정관리", "품질관리", "안전관리", "원가관리", "현장운영"]
    bw, gap = 84.0, 10.0
    x0 = (480.0 - (5 * bw + 4 * gap)) / 2.0
    for i, lab in enumerate(labs):
        x = x0 + i * (bw + gap)
        els.append(BOX(x, 170, bw, 46, [(lab, 14, "tb")], "box", i + 2))
        els.append(A(240, 104, x + bw / 2.0, 166, "e2", i + 2))
    els.append(TX(240, 248, "공정, 품질, 안전, 원가, 현장운영", "tm", 6, 15))
    return els


def fig_money_flow():
    """돈과 지시는 아래로, 확인은 옆에서."""
    els = [TX(240, 26, "세 가지 흐름", "tb", 1, 17)]
    rows = [("돈", "발주자 → 원도급자 → 하도급자", 1),
            ("지시", "발주자 → 현장소장 → 하도급자", 2),
            ("확인", "감리자가 도면대로인지 본다", 3)]
    for i, (a_, b_, bi) in enumerate(rows):
        y = 60 + i * 62
        els.append(BOX(20, y, 86, 46, [(a_, 16, "tb")], "box2" if i == 2 else "box", bi))
        els.append(HAT(120, y, 340, 46, [(b_, 15, "t")], "box", bi))
    els.append(TX(240, 250, "돈과 지시는 같은 길, 확인은 다른 길이에요", "tm", 3, 15))
    return els


# ---------------------------------------------------------------- b-3
def fig_bid_funnel():
    """입찰 네 가지, 문이 점점 좁아져요."""
    els = [TX(140, 26, "문이 점점 좁아져요", "tb", 1, 17)]
    labs = [("공개경쟁입찰", 300), ("제한경쟁입찰", 240), ("지명경쟁입찰", 180), ("수의계약", 120)]
    for i, (lab, w) in enumerate(labs):
        y = 50 + i * 54
        els.append(BOX(240 - w / 2.0, y, w, 44, [(lab, 16, "tb")],
                       "box2" if i == 3 else "box", i + 1))
    els.append(TX(470, 80, "누구나", "tm", 1, 14, "end"))
    els.append(TX(470, 242, "한 곳만", "tm", 4, 14, "end"))
    return els


def fig_contract_tree():
    """시공 방식의 갈래."""
    els = [TX(240, 26, "일을 맡기는 길", "tb", 1, 17)]
    els.append(BOX(180, 42, 120, 40, [("시공 방식", 16, "tb")], "box2", 1))
    row = [("직영공사", 30.0), ("도급공사", 175.0), ("턴키", 320.0)]
    for i, (lab, x) in enumerate(row):
        els.append(BOX(x, 112, 130, 44, [(lab, 16, "tb")], "box", i + 2))
        els.append(A(240, 86, x + 65, 108, "e2", i + 2))
    els.append(BOX(52, 192, 180, 52, [("공사 시행 방식", 15, "tb"),
                                      ("일식, 분할, 공동", 14, "tm")], "box", 5))
    els.append(BOX(250, 192, 180, 52, [("공사비 지급 방식", 15, "tb"),
                                       ("정액, 단가, 실비정산", 14, "tm")], "box", 5))
    els.append(A(230, 160, 142, 188, "e2", 5))
    els.append(A(250, 160, 340, 188, "e2", 5))
    return els


def fig_price3():
    """값 정하는 세 가지."""
    els = [TX(240, 26, "값을 정하는 세 가지", "tb", 1, 17)]
    box = [("정액도급", "총액을 미리 확정"), ("단가도급", "단가 X 실제 수량"),
           ("실비정산", "실제 공사비 + 보수")]
    for i, (a_, b_) in enumerate(box):
        x = 14 + i * 154
        els.append(BOX(x, 72, 144, 66, [(a_, 16, "tb"), (b_, 14, "tm")], "box", i + 1))
    els.append(TX(240, 180, "정액은 총액, 단가는 수량, 실비정산은 영수증", "tm", 3, 15))
    els.append(TX(240, 216, "택시로 치면 정액 요금, 거리 요금, 실비 정산이에요", "tb", 3, 15))
    return els


# ---------------------------------------------------------------- b-4
def fig_onion():
    """공사원가 양파."""
    lv = [(152, 130, 176, 74, "직접공사비", "", 1),
          (116, 100, 248, 134, "순공사비", "+ 간접공사비", 2),
          (80, 70, 320, 194, "공사원가", "+ 현장경비", 3),
          (44, 40, 392, 224, "총원가", "+ 일반관리비", 4),
          (8, 10, 464, 254, "계약금액", "+ 부가이윤, 부가세", 5)]
    els = []
    for x, y, w, h, name, note, b in reversed(lv):
        els.append(R(x, y, w, h, "box2" if b == 1 else "box", b))
    for x, y, w, h, name, note, b in lv:
        els.append(TX(x + 8, y + 22, name, "tb", b, 15, "start"))
        if note:
            els.append(TX(x + w - 8, y + 22, note, "tm", b, 14, "end"))
    els.append(TX(240, 178, "재노외경", "tm", 1, 14))
    return els


def fig_onion_num():
    """예시 숫자로 양파 까기 (만 원)."""
    els = [TX(240, 26, "예시 숫자로 한 번 (만 원)", "tb", 1, 17)]
    box = [("직접공사비", "4,000"), ("순공사비", "4,500"), ("공사원가", "4,800"), ("총원가", "5,000")]
    bw, gap = 100.0, 20.0
    x0 = (480.0 - (4 * bw + 3 * gap)) / 2.0
    for i, (a_, b_) in enumerate(box):
        x = x0 + i * (bw + gap)
        els.append(BOX(x, 84, bw, 60, [(a_, 15, "tb"), (b_, 16, "tl")], "box", i + 1))
        if i:
            els.append(A(x - gap + 2, 114, x - 3, 114, "e2", i + 1))
    adds = ["+ 간접 500", "+ 현장 300", "+ 일반 200"]
    for i, s in enumerate(adds):
        els.append(TX(x0 + bw + gap / 2.0 + i * (bw + gap), 64, s, "tm", i + 2, 14))
    els.append(TX(240, 186, "안에서 밖으로 한 겹씩 더해요", "tm", 4, 15))
    els.append(TX(240, 222, "재노외경 → 간접 → 현장 → 일반 → 이윤", "tb", 4, 16))
    return els


def fig_actual():
    """실행내역서는 계약금액에서 무엇을 뺀 것인가."""
    els = [TX(240, 28, "계약금액을 갈라 보면", "tb", 1, 17)]
    els.append(R(20, 60, 440, 54, "box", 1))
    els.append(TX(240, 94, "계약금액", "tb", 1, 17))
    els.append(R(20, 140, 280, 54, "box2", 2))
    els.append(TX(160, 174, "공사원가", "tb", 2, 16))
    els.append(R(302, 140, 80, 54, "box", 3))
    els.append(TX(342, 174, "일반관리비", "tl", 3, 14))
    els.append(R(384, 140, 76, 54, "box", 3))
    els.append(TX(422, 174, "이윤", "tl", 3, 15))
    els.append(TX(160, 220, "여기가 실행내역서", "tb", 4, 16))
    els.append(TX(240, 252, "실행내역은 대외비예요", "tm", 4, 15))
    return els


# ---------------------------------------------------------------- b-5
def fig_barchart():
    """바차트 공정표 (슬라이드 예시 숫자)."""
    els = [TX(240, 24, "바차트 공정표", "tb", 1, 16)]
    els.append(L(90, 48, 400, 48, "e", 1))
    for i in range(6):
        d = i * 2
        x = 90 + d * 30
        els.append(L(x, 44, x, 52, "e", 1))
        els.append(TX(x, 40, str(d), "tm", 1, 14))
    rows = [("철거", 0, 2, 2), ("전기", 2, 5, 3), ("마감", 5, 8, 4), ("도장", 8, 10, 5)]
    for i, (name, a_, b_, bi) in enumerate(rows):
        y = 62 + i * 46
        els.append(TX(14, y + 22, name, "tb", bi, 15, "start"))
        els.append(R(90 + a_ * 30, y, (b_ - a_) * 30, 30, "box2" if i else "box", bi))
    els.append(TX(240, 262, "가로 막대로 언제 시작해 언제 끝나는지가 보여요", "tm", 5, 15))
    return els


def fig_network():
    """네트워크 공정표 (슬라이드 예시 숫자)."""
    els = [TX(240, 24, "네트워크 공정표", "tb", 1, 16)]
    els.append(BOX(14, 112, 80, 48, [("철거", 15, "tb"), ("2일", 14, "tm")], "box", 1))
    els.append(BOX(134, 52, 92, 48, [("전기 배선", 15, "tb"), ("3일", 14, "tm")], "box2", 2))
    els.append(BOX(134, 172, 92, 48, [("설비 배관", 15, "tb"), ("2일", 14, "tm")], "box", 2))
    els.append(BOX(264, 112, 80, 48, [("마감", 15, "tb"), ("3일", 14, "tm")], "box2", 3))
    els.append(BOX(378, 112, 88, 48, [("도장", 15, "tb"), ("2일", 14, "tm")], "box2", 3))
    els.append(A(96, 128, 130, 84, "e2", 2))
    els.append(A(96, 148, 130, 190, "e2", 2))
    els.append(A(228, 84, 262, 128, "e2", 3))
    els.append(A(228, 190, 262, 148, "e2", 3))
    els.append(A(346, 136, 374, 136, "e2", 3))
    els.append(TX(240, 250, "경로 A 10일, 경로 B 9일. 긴 쪽이 주공정선이에요", "tb", 4, 15))
    return els


def fig_float():
    """여유시간."""
    els = [TX(240, 28, "여유시간이 생기는 자리", "tb", 1, 17)]
    els.append(TX(14, 92, "전기", "tb", 1, 15, "start"))
    els.append(R(80, 70, 270, 32, "box2", 1))
    els.append(TX(215, 92, "3일", "tl", 1, 15))
    els.append(TX(14, 162, "설비", "tb", 2, 15, "start"))
    els.append(R(80, 140, 180, 32, "box", 2))
    els.append(TX(170, 162, "2일", "tl", 2, 15))
    els.append(R(262, 140, 88, 32, "box", 3))
    els.append(TX(306, 162, "여유 1일", "tm", 3, 14))
    els.append(TX(240, 216, "설비가 하루 늦어도 전기를 기다리는 동안 따라잡아요", "tm", 3, 15))
    els.append(TX(240, 248, "주공정선에 있는 전기가 늦으면 준공이 늦어져요", "tb", 3, 15))
    return els


# ---------------------------------------------------------------- b-6
def fig_three_views():
    """같은 방을 평면도, 입면도, 단면도로."""
    els = [TX(240, 28, "같은 방을 세 가지로 그려요", "tb", 1, 17)]
    # 평면도: 벽 두께가 보이는 테두리 + 문 열림 자국
    els.append(R(20, 60, 120, 90, "n", 1))
    els.append(R(30, 70, 100, 70, "box", 1))
    els.append(R(86, 140, 34, 10, "box", 1))
    els.append(PATH("M 86 140 A 34 34 0 0 0 120 106", "e", 1))
    els.append(L(86, 140, 86, 108, "e2", 1))
    els.append(TX(80, 178, "평면도", "tb", 1, 16))
    els.append(TX(80, 202, "위에서 내려다본 모습", "tm", 1, 14))
    # 입면도: 벽면에 창과 문, 바닥선
    els.append(R(180, 60, 120, 90, "box", 2))
    els.append(R(196, 78, 54, 34, "n", 2))
    els.append(L(223, 78, 223, 112, "e", 2))
    els.append(L(196, 95, 250, 95, "e", 2))
    els.append(R(266, 104, 26, 46, "n3", 2))
    els.append(L(180, 150, 300, 150, "e2", 2))
    els.append(TX(240, 178, "입면도", "tb", 2, 16))
    els.append(TX(240, 202, "벽을 정면에서 본 모습", "tm", 2, 14))
    # 단면도
    els.append(R(368, 60, 12, 90, "n2", 3))
    els.append(R(410, 60, 12, 90, "n2", 3))
    for i in range(5):
        y = 70 + i * 18
        els.append(L(382, y, 408, y + 12, "e", 3))
    els.append(TX(400, 178, "단면도", "tb", 3, 16))
    els.append(TX(400, 202, "잘라서 속을 본 모습", "tm", 3, 14))
    els.append(TX(240, 236, "평면도는 어디에, 입면도는 얼마나 높이, 단면도는 속에 무엇이", "tm", 3, 15))
    return els


def fig_ceiling_plan():
    """천장도."""
    els = [TX(240, 28, "천장도에는 무엇이 있나", "tb", 1, 17)]
    els.append(R(90, 54, 300, 150, "box", 1))
    for i in range(2):
        for j in range(3):
            els.append(C(150 + j * 90, 96 + i * 66, 13, "n2", 2))
    els.append(R(352, 150, 32, 44, "n3", 3))
    els.append(TX(368, 226, "점검구", "tm", 3, 14))
    els.append(TX(150, 226, "조명 여섯 개", "tm", 2, 14))
    els.append(TX(240, 252, "조명 간격, 점검구, 냉난방기 자리를 그려요", "tb", 3, 15))
    return els


def fig_detail():
    """상세도는 한 자리를 크게."""
    els = [TX(240, 26, "상세도는 한 자리를 크게", "tb", 1, 17)]
    els.append(R(20, 56, 150, 130, "box", 1))
    els.append(TX(95, 78, "단면도", "tb", 1, 15))
    els.append(R(60, 96, 70, 56, "n", 1))
    els.append(TX(95, 172, "여기 한 자리", "tm", 1, 14))
    els.append(A(176, 124, 246, 124, "e2", 2))
    els.append(R(254, 56, 210, 130, "box2", 2))
    els.append(TX(359, 80, "상세도", "tb", 2, 16))
    rows = ["석고보드 2겹", "메탈 스터드 65", "단열재 충진"]
    for i, s in enumerate(rows):
        els.append(TX(359, 110 + i * 26, s, "t", 3, 14))
    els.append(TX(240, 226, "재료와 치수, 붙이는 순서까지 적어요", "tb", 3, 15))
    els.append(TX(240, 254, "상세도를 그리는 것을 디테일을 푼다고 해요", "tm", 3, 15))
    return els


# ---------------------------------------------------------------- b-7
def fig_dimline():
    """치수선과 치수보조선."""
    els = [TX(240, 28, "치수선 읽는 법", "tb", 1, 17)]
    els.append(R(60, 56, 320, 22, "n2", 1))
    els.append(TX(220, 73, "벽", "tl", 1, 14))
    els.append(L(60, 82, 60, 176, "e", 2))
    els.append(L(380, 82, 380, 176, "e", 2))
    els.append(L(60, 150, 380, 150, "e2", 3))
    els.append(A(90, 150, 62, 150, "e2", 3))
    els.append(A(350, 150, 378, 150, "e2", 3))
    els.append(TX(220, 142, "3,600", "tb", 3, 17))
    els.append(TX(60, 200, "치수보조선", "tm", 2, 14))
    els.append(TX(398, 155, "치수선", "tm", 3, 14, "start"))
    els.append(TX(240, 240, "숫자에 단위가 없으면 mm 예요. 3,600 은 3.6m", "tb", 4, 15))
    return els


def fig_scale():
    """같은 벽을 두 축척으로."""
    els = [TX(240, 26, "같은 벽, 다른 축척", "tb", 1, 17)]
    els.append(TX(44, 84, "1/50", "tb", 1, 16))
    els.append(R(80, 66, 288, 26, "box2", 1))
    els.append(TX(380, 84, "도면 72mm", "tm", 1, 14, "start"))
    els.append(TX(44, 154, "1/100", "tb", 2, 16))
    els.append(R(80, 136, 144, 26, "box", 2))
    els.append(TX(236, 154, "도면 36mm", "tm", 2, 14, "start"))
    els.append(TX(240, 202, "실제 길이는 3,600mm 로 똑같아요", "tb", 3, 16))
    els.append(TX(240, 234, "분모가 커질수록 도면에서는 작게 그려져요", "tm", 3, 15))
    return els


def fig_units():
    """단위 사다리."""
    els = [TX(240, 28, "단위 사다리", "tb", 1, 17)]
    box = [("mm", "3,600"), ("cm", "360"), ("m", "3.6")]
    for i, (a_, b_) in enumerate(box):
        x = 34 + i * 145
        els.append(BOX(x, 78, 130, 62, [(a_, 17, "tb"), (b_, 16, "tl")],
                       "box2" if i == 0 else "box", i + 1))
        if i:
            els.append(A(x - 11, 109, x - 4, 109, "e2", i + 1))
    els.append(TX(172, 62, "÷ 10", "tm", 2, 14))
    els.append(TX(317, 62, "÷ 100", "tm", 3, 14))
    els.append(TX(240, 178, "거꾸로 가려면 곱해요. 3.6m X 1,000 = 3,600mm", "tb", 3, 15))
    els.append(TX(240, 214, "실내 도면은 언제나 mm 로 적어요", "tm", 3, 15))
    return els


# ---------------------------------------------------------------- b-8
def fig_stage4():
    """현장 네 단계에서 하는 일."""
    els = [TX(240, 26, "네 단계에서 하는 일", "tb", 1, 17)]
    rows = [("가설", "비계, 보양, 가설전기, 먹매김"), ("철거", "옛 마감재와 시설 걷어 내기"),
            ("경량철골", "스터드 벽체 틀, 천장 틀"), ("마감", "도장, 타일, 바닥재")]
    for i, (a_, b_) in enumerate(rows):
        y = 50 + i * 56
        els.append(BOX(14, y, 106, 44, [(a_, 15, "tb")], "box2" if i == 0 else "box", i + 1))
        els.append(HAT(134, y, 330, 44, [(b_, 15, "t")], "box", i + 1))
        if i:
            els.append(A(67, y - 12, 67, y - 3, "e2", i + 1))
    return els


def fig_temp_work():
    """가설은 공사를 위한 공사."""
    els = [TX(240, 26, "가설은 공사를 위한 공사", "tb", 1, 17)]
    els.append(R(172, 58, 136, 152, "box", 1))
    els.append(TX(240, 142, "본 공사", "tb", 1, 16))
    els.append(L(140, 50, 140, 222, "e", 2))
    els.append(L(340, 50, 340, 222, "e", 2))
    for y in (96, 148, 198):
        els.append(R(136, y, 36, 8, "n2", 2))
        els.append(R(308, y, 36, 8, "n2", 2))
    els.append(TX(100, 142, "비계", "tm", 2, 15))
    els.append(TX(382, 142, "발판", "tm", 2, 15))
    els.append(TX(240, 250, "공사가 끝나면 비계도 발판도 다 걷어 내요", "tb", 3, 15))
    return els


def fig_wall_skeleton():
    """뼈대에 살 붙이기."""
    els = [TX(240, 26, "뼈대에 살 붙이기", "tb", 1, 17)]
    els.append(R(90, 60, 300, 12, "n3", 1))
    els.append(R(90, 198, 300, 12, "n3", 1))
    els.append(TX(240, 46, "런너", "tm", 1, 14))
    for i in range(4):
        x = 120 + i * 80
        els.append(R(x, 72, 12, 126, "n2", 2))
    els.append(TX(286, 232, "스터드", "tm", 2, 14))
    els.append(R(60, 60, 26, 150, "n", 3))
    els.append(TX(73, 232, "석고보드", "tm", 3, 14))
    els.append(TX(240, 258, "스터드와 런너가 뼈, 석고보드가 살이에요", "tb", 3, 15))
    return els
