# -*- coding: utf-8 -*-
"""신호및시스템 문제은행 생성 도우미 (build_*.py 가 함께 쓴다)"""
import json, pathlib, re
import optshuffle

HERE = pathlib.Path(__file__).resolve().parent


class Bank:
    def __init__(self, prefix, part, level):
        self.prefix, self.part, self.level = prefix, part, level
        self.items, self.n = [], {}

    def _id(self, t):
        self.n[t] = self.n.get(t, 0) + 1
        return f"{self.prefix}-{t}-{self.n[t]:03d}"

    def _base(self, t, unit, slides, src):
        q = {"id": self._id(t), "type": t, "part": self.part, "level": self.level, "unit": unit, "slides": slides}
        if src:
            q["src"] = src
        return q

    def mcq(self, unit, slides, q, c, a, e, src=None):
        assert len(c) == 4 and len(set(c)) == 4 and 0 <= a < 4
        d = self._base("mcq", unit, slides, src)
        d.update(q=q, c=c, a=a, e=e); self.items.append(d)

    def ox(self, unit, slides, q, a, e, src=None):
        assert isinstance(a, bool)
        d = self._base("ox", unit, slides, src); d.update(q=q, a=a, e=e); self.items.append(d)

    def short(self, unit, slides, q, a, e, src=None, num=False, tol=0.01):
        d = self._base("short", unit, slides, src); d.update(q=q, a=[str(x) for x in a], e=e)
        if num:
            float(d["a"][0]); d.update(num=True, tol=tol)
        self.items.append(d)

    def essay(self, unit, slides, q, answer, points, model, src=None):
        assert len(points) >= 4
        d = self._base("essay", unit, slides, src); d.update(q=q, answer=answer, points=points, model=model); self.items.append(d)

    def calc(self, unit, slides, q, qko, blanks, steps, answer, e, model, src=None):
        assert len(steps) >= 3 and blanks
        bl = []
        for lab, ans, *tol in blanks:
            bl.append({"label": lab, "ans": round(float(ans), 6) if not float(ans).is_integer() else int(ans), "tol": tol[0] if tol else 0.01})
        d = self._base("calc", unit, slides, src); d.update(q=q, qko=qko, blanks=bl, steps=steps, answer=answer, e=e, model=model)
        self.items.append(d)

    def save(self, name, ids):
        """ids 는 만들어질 문항의 id 목록이다(optshuffle.check_ids 설명 참고)."""
        # 정답이 한 자리에 몰리면 내용을 몰라도 같은 번호만 찍어 맞힐 수 있다. 그래서
        # 파일에 쓰기 직전에 보기 자리를 섞는다(까닭과 예외는 optshuffle.py 에).
        optshuffle.shuffle_bank(self.items)
        optshuffle.check_ids(self.items, ids)
        raw = json.dumps(self.items, ensure_ascii=False, indent=1)
        for ch in "—–·":
            assert ch not in raw, ch
        (HERE / name).write_text(raw, encoding="utf-8")
        cnt = {}
        for q in self.items:
            cnt[q["type"]] = cnt.get(q["type"], 0) + 1
        print(name, len(self.items), cnt)


def seq(v, start=0):
    """[1,2,3] (시작 칸 start) -> '$x[0]=1,\\ x[1]=2$' 식 대신 표기용 문자열"""
    return ", ".join(f"{start + i}칸 {fmt(x)}" for i, x in enumerate(v))


def fmt(x):
    x = float(x)
    if abs(x - round(x)) < 1e-9:
        return str(int(round(x)))
    return f"{x:.4f}".rstrip("0").rstrip(".")


def conv(x, h):
    y = [0.0] * (len(x) + len(h) - 1)
    for i, a in enumerate(x):
        for j, b in enumerate(h):
            y[i + j] += a * b
    return y
