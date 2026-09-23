# -*- coding: utf-8 -*-
# S3 1~33쪽 그림 (build_S3_001-033.py 가 exec 로 읽는다. lib 이름들이 이미 있음)

# p.3 단위원 위를 도는 점
_cx, _cy, _r = 150, 140, 90
_th = math.radians(50)
_px, _py = _cx + _r * math.cos(_th), _cy - _r * math.sin(_th)
FIG_CIRCLE = SVG(
    L(40, _cy, 262, _cy), L(_cx, 30, _cx, 250), C(_cx, _cy, _r, "hl"),
    TX(268, _cy + 5, "실수", "tm", 14, "start"), TX(_cx + 6, 26, "허수", "tm", 14, "start"),
    A(_cx, _cy, _px, _py, "e2", 1), C(_px, _py, 6, "n2", 1),
    TX(_px + 10, _py - 8, "도는 점", "tb", 15, "start", 1),
    L(_px, _py, _px, _cy, "e", 2), L(_cx + 3, _cy + 14, _px, _cy + 14, "e2", 2),
    TX((_cx + _px) / 2, _cy + 34, "가로 그림자 = cos", "tb", 14, "middle", 2),
    L(_px, _py, _cx, _py, "e", 3), L(_cx - 14, _cy, _cx - 14, _py, "e2", 3),
    TX(_cx - 20, (_cy + _py) / 2 + 5, "세로 그림자 = sin", "tb", 14, "end", 3),
    BOX(300, 70, 160, 34, "빙글빙글 = 회전", "box2", "tb", 1, 15),
    TX(380, 140, "그림자는 출렁여요", "t", 15, "middle", 3),
    TX(380, 166, "(진동, 위상)", "tm", 14, "middle", 3),
)
assert abs(_px - (150 + 90 * math.cos(_th))) < 1e-9

# p.5 RC 충전과 방전 (RC=1, v_s=1)
def _curve(f, x0, y0, sx, sy, t1, n=40):
    return [(x0 + t * sx, y0 - f(t) * sy) for t in [t1 * i / n for i in range(n + 1)]]
FIG_RC = SVG(
    L(40, 120, 225, 120), L(40, 120, 40, 25), TX(132, 20, "충전(스위치 켬)", "tb", 15),
    PL(_curve(lambda t: 1 - math.exp(-t), 40, 120, 36, 80, 5), "e2", 1),
    L(40, 40, 225, 40, "e", 1), TX(228, 45, "vs", "tm", 14, "start", 1),
    TX(215, 140, "t", "tm", 14),
    L(260, 120, 450, 120), L(260, 120, 260, 25), TX(356, 20, "방전(전원 끊김)", "tb", 15),
    PL(_curve(lambda t: math.exp(-t), 260, 120, 36, 80, 5), "e2", 2),
    TX(440, 140, "t", "tm", 14),
    TX(240, 190, "둘 다 실수 지수 모양이에요", "tb", 16, "middle", 3),
    TX(240, 220, "0에서 차오르거나, 0으로 빠져요", "tm", 15, "middle", 3),
)
assert abs(1 - math.exp(-5) - 0.99326) < 1e-4

# p.6 LC 회로 전압이 출렁임 (omega0 = 2)
FIG_LC = SVG(
    L(30, 120, 460, 120), TX(455, 140, "t", "tm", 14),
    PL(_curve(lambda t: math.cos(2 * t), 30, 120, 60, 70, 7, 120), "e2", 1),
    TX(240, 225, "저항이 없으면 끝없이 왔다 갔다", "tb", 16, "middle", 2),
    TX(240, 252, "실수 부분 cos, 허수 부분 sin", "tm", 15, "middle", 2),
)

# p.8 단위 임펄스와 단위 계단
_ns = list(range(-3, 5))
FIG_DU = SVG(
    TX(120, 30, "단위 임펄스: 손뼉 한 번", "tb", 15),
    STEM(35, 150, 24, 80, _ns, [1 if n == 0 else 0 for n in _ns], 1),
    TX(360, 30, "단위 계단: 스위치 켬", "tb", 15, "middle", 2),
    STEM(275, 150, 24, 80, _ns, [1 if n >= 0 else 0 for n in _ns], 2, vlab=False),
    TX(120, 210, "n=0 에서만 1", "tm", 15, "middle", 1),
    TX(360, 210, "n=0 부터 계속 1", "tm", 15, "middle", 2),
)

# p.13 신호를 손뼉 조각으로 쪼개기: x[-1]=1, x[0]=2, x[1]=-1
_xd = {-1: 1, 0: 2, 1: -1}
_n5 = list(range(-2, 3))
FIG_DECOMP = SVG(
    TX(240, 20, "x[n]", "tb", 15),
    STEM(192, 100, 24, 28, _n5, [_xd.get(n, 0) for n in _n5]),
    TX(80, 150, "1 x 손뼉(칸 -1)", "tm", 14, "middle", 1),
    STEM(32, 225, 24, 28, _n5, [1 if n == -1 else 0 for n in _n5], 1),
    TX(240, 150, "2 x 손뼉(칸 0)", "tm", 14, "middle", 2),
    STEM(192, 225, 24, 28, _n5, [2 if n == 0 else 0 for n in _n5], 2),
    TX(400, 150, "-1 x 손뼉(칸 1)", "tm", 14, "middle", 3),
    STEM(352, 225, 24, 28, _n5, [-1 if n == 1 else 0 for n in _n5], 3),
    TX(160, 200, "+", "tb", 20, "middle", 2), TX(320, 200, "+", "tb", 20, "middle", 3),
    h=285,
)

# p.16 손뼉 -> 메아리, 늦은 손뼉 -> 늦은 메아리 (예시 메아리 1, 0.6, 0.3)
_e = {0: 1, 1: 0.6, 2: 0.3}
_n6 = list(range(-1, 5))
FIG_ECHO = SVG(
    STEM(20, 90, 20, 50, _n6, [1 if n == 0 else 0 for n in _n6], 1, vlab=False),
    A(140, 70, 180, 70, "e2", 1), BOX(185, 50, 100, 40, "LTI 시스템", "box2", "tb", 1, 15), A(290, 70, 330, 70, "e2", 1),
    STEM(345, 90, 20, 50, _n6, [_e.get(n, 0) for n in _n6], 1, vlab=False),
    TX(75, 25, "손뼉 (n=0)", "tb", 14, "middle", 1), TX(400, 25, "메아리 h[n]", "tb", 14, "middle", 1),
    STEM(20, 215, 20, 50, _n6, [1 if n == 2 else 0 for n in _n6], 2, vlab=False),
    A(140, 195, 180, 195, "e2", 2), BOX(185, 175, 100, 40, "LTI 시스템", "box2", "tb", 2, 15), A(290, 195, 330, 195, "e2", 2),
    STEM(345, 215, 20, 50, _n6, [_e.get(n - 2, 0) for n in _n6], 2, vlab=False),
    TX(75, 150, "2칸 늦은 손뼉", "tb", 14, "middle", 2), TX(400, 150, "같은 메아리, 2칸 늦게", "tb", 14, "middle", 2),
    h=250,
)

# p.19 세 가지 임펄스 응답
_n7 = list(range(0, 7))
_h_fir = [1, 0.5, 0.25, 0, 0, 0, 0]
_h_st = [0.7 ** n for n in _n7]
_h_un = [1.3 ** n for n in _n7]
assert abs(1.3 ** 10 - 13.7858) < 1e-3
FIG_IR3 = SVG(
    TX(80, 30, "유한 번 울림", "tb", 15, "middle", 1),
    STEM(20, 190, 20, 60, _n7, _h_fir, 1, vlab=False),
    TX(240, 30, "점점 작아짐", "tb", 15, "middle", 2),
    STEM(180, 190, 20, 60, _n7, _h_st, 2, vlab=False),
    TX(400, 30, "점점 커짐", "tb", 15, "middle", 3),
    STEM(340, 190, 20, 30, _n7, _h_un, 3, vlab=False),
    TX(80, 240, "0.5x[n-1] 등", "tm", 14, "middle", 1), TX(240, 240, "0.7 배씩", "tm", 14, "middle", 2),
    TX(400, 240, "1.3 배씩: 불안정", "tm", 14, "middle", 3),
)


# p.24 뒤집고 밀고 곱하고 더하기 (Example 2.1)
X21 = {0: 0.5, 1: 2}
H21 = {0: 1, 1: 1, 2: 1}
Y21 = conv(X21, H21)
assert Y21 == {0: 0.5, 1: 2.5, 2: 2.5, 3: 2}
_nk = list(range(-3, 5))


def fig_flip(n):
    hs = [H21.get(n - k, 0) for k in _nk]
    pr = [X21.get(k, 0) * H21.get(n - k, 0) for k in _nk]
    tot = sum(pr)
    assert tot == Y21.get(n, 0)
    return SVG(
        TX(40, 52, "x[k]", "tb", 15, "start"),
        STEM(130, 60, 36, 18, _nk, [X21.get(k, 0) for k in _nk], 0),
        TX(40, 137, f"h[{n}-k]", "tb", 15, "start", 1),
        STEM(130, 145, 36, 18, _nk, hs, 1, cls="e2", dot="n3"),
        TX(40, 222, "곱", "tb", 15, "start", 2),
        STEM(130, 230, 36, 18, _nk, pr, 2, dot="n4"),
        TX(240, 285, f"더하기: y[{n}] = {fmtv(tot)}", "tb", 17, "middle", 3),
        h=300,
    )


FIG_FLIP1 = fig_flip(1)
FIG_FLIP3 = fig_flip(3)

# p.24 4단계 흐름
FIG_RECIPE = SVG(
    BOX(10, 100, 95, 44, "1 뒤집기", "box2", "tb", 1, 16), A(106, 122, 124, 122, "e2", 2),
    BOX(128, 100, 95, 44, "2 밀기", "box2", "tb", 2, 16), A(224, 122, 242, 122, "e2", 3),
    BOX(246, 100, 95, 44, "3 곱하기", "box2", "tb", 3, 16), A(342, 122, 360, 122, "e2", 4),
    BOX(364, 100, 100, 44, "4 더하기", "box2", "tb", 4, 16),
    TX(57, 175, "메아리 틀", "tm", 14, "middle", 1), TX(57, 195, "거울에 비춤", "tm", 14, "middle", 1),
    TX(175, 175, "원하는 칸 n", "tm", 14, "middle", 2), TX(175, 195, "까지 밀기", "tm", 14, "middle", 2),
    TX(293, 175, "입력과", "tm", 14, "middle", 3), TX(293, 195, "칸마다 곱", "tm", 14, "middle", 3),
    TX(414, 175, "출력 한 점", "tm", 14, "middle", 4), TX(414, 195, "y[n] 완성", "tm", 14, "middle", 4),
    TX(240, 60, "출력 한 칸을 구하는 4단계", "tb", 17),
)

# p.26 메아리 도장 찍고 더하기 (Example 2.1)
_n8 = list(range(-1, 5))
FIG_STAMP = SVG(
    TX(20, 40, "0.5h[n]", "tb", 15, "start", 1),
    STEM(130, 60, 50, 18, _n8, [0.5 * H21.get(n, 0) for n in _n8], 1),
    TX(20, 125, "2h[n-1]", "tb", 15, "start", 2),
    STEM(130, 145, 50, 18, _n8, [2 * H21.get(n - 1, 0) for n in _n8], 2, dot="n3"),
    TX(20, 215, "y[n] 합", "tb", 15, "start", 3),
    STEM(130, 245, 50, 18, _n8, [Y21.get(n, 0) for n in _n8], 3, dot="n4"),
    h=275,
)

# p.23 시불변 vs 시변 (메아리 모양)
_n9 = list(range(-2, 4))
_same = {0: 1, 1: 0.5}


def _mini(ox, oy, d, b):
    return STEM(ox, oy, 17, 40, _n9, [d.get(n, 0) for n in _n9], b, vlab=False, nlab=False)


FIG_TV = SVG(
    TX(240, 22, "시불변: 같은 모양이 옆으로만", "tb", 15, "middle", 1),
    _mini(30, 100, {n - 1: v for n, v in _same.items()}, 1),
    _mini(190, 100, _same, 1),
    _mini(350, 100, {n + 1: v for n, v in _same.items()}, 1),
    TX(240, 150, "시변: 손뼉마다 모양이 제각각", "tb", 15, "middle", 2),
    _mini(30, 225, {-1: -1, 0: -0.5, 1: 0.4}, 2),
    _mini(190, 225, {0: 0.5, 1: 0.8, 2: 1.2}, 2),
    _mini(350, 225, {0: 0.3, 1: -1, 2: -0.6}, 2),
    TX(73, 262, "칸 -1 손뼉", "tm", 14, "middle", 2), TX(233, 262, "칸 0 손뼉", "tm", 14, "middle", 2),
    TX(393, 262, "칸 1 손뼉", "tm", 14, "middle", 2),
    h=275,
)

# p.31 Example 2.3, alpha = 0.5
AL = 0.5
Y23 = {n: sum(AL ** k for k in range(n + 1)) for n in range(0, 8)}
for n in range(0, 8):
    assert abs(Y23[n] - (1 - AL ** (n + 1)) / (1 - AL)) < 1e-12
_n10 = list(range(-2, 8))
FIG_EX23 = SVG(
    L(40, 70, 470, 70, "e", 1), TX(470, 60, "높이 2 = 1/(1-0.5)", "tm", 14, "end", 1),
    STEM(60, 230, 42, 80, _n10, [Y23.get(n, 0) for n in _n10], 0,
         labs=[("" if n < 0 else (fmtv(Y23[n]) if n <= 3 else "")) for n in _n10]),
    TX(330, 130, "점점 차올라 2에 가까워져요", "tb", 15, "middle", 1),
)

# p.32 Example 2.4, alpha = 2
X24 = {n: 1 for n in range(0, 5)}
H24 = {n: 2 ** n for n in range(0, 7)}
Y24 = conv(X24, H24)
assert [Y24[n] for n in range(11)] == [1, 3, 7, 15, 31, 62, 124, 120, 112, 96, 64]
_n11 = list(range(-1, 13))
FIG_EX24 = SVG(
    STEM(30, 240, 32, 1.5, _n11, [Y24.get(n, 0) for n in _n11], 0,
         labs=[{4: "31", 6: "124", 8: "112", 10: "64"}.get(n, "") for n in _n11]),
    TX(120, 60, "알파 = 2 로 넣은 모양", "tb", 15),
    TX(120, 85, "n=6 에서 가장 높고 n=11 부터 0", "tm", 14),
)

# p.33 Example 2.5
Y25 = {}
for n in range(-4, 4):
    Y25[n] = sum(2.0 ** k for k in range(-60, min(0, n) + 1))
    assert abs(Y25[n] - (2.0 ** (n + 1) if n < 0 else 2.0)) < 1e-9
_n12 = list(range(-4, 4))
FIG_EX25 = SVG(
    STEM(60, 230, 50, 80, _n12, [Y25[n] for n in _n12], 0,
         labs=["1/8", "1/4", "1/2", "1", "2", "2", "2", "2"]),
    TX(120, 40, "n 이 0 이상이면 계속 2", "tb", 15),
    TX(120, 65, "왼쪽으로 갈수록 절반씩", "tm", 14),
)
