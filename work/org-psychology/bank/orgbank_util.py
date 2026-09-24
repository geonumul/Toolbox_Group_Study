# -*- coding: utf-8 -*-
"""조직심리학 문제은행 생성 도우미 (build_w*.py 가 함께 쓴다).

이 과목은 계산 문항이 없어서 calc 도우미를 두지 않는다.
"""
import json, pathlib, random, zlib

HERE = pathlib.Path(__file__).resolve().parent
BAD_CHARS = "—–·・"   # em dash, en dash, 가운뎃점 2종


class Bank:
    def __init__(self, prefix, part, level):
        self.prefix, self.part, self.level = prefix, part, level
        self.items, self.n = [], {}

    def _id(self, t):
        self.n[t] = self.n.get(t, 0) + 1
        return f"{self.prefix}-{t}-{self.n[t]:03d}"

    def _base(self, t, unit, slides, src):
        q = {"id": self._id(t), "type": t, "part": self.part, "level": self.level,
             "unit": unit, "slides": slides}
        if src:
            q["src"] = src
        return q

    def mcq(self, unit, slides, q, c, a, e, src=None):
        assert len(c) == 4 and len(set(c)) == 4 and 0 <= a < 4, q
        d = self._base("mcq", unit, slides, src)
        rnd = random.Random(zlib.crc32(d["id"].encode()))   # 정답 자리를 고르게 섞는다 (id 로 고정)
        order = list(range(4))
        rnd.shuffle(order)
        d.update(q=q, c=[c[i] for i in order], a=order.index(a), e=e)
        self.items.append(d)

    def ox(self, unit, slides, q, a, e, src=None):
        assert isinstance(a, bool), q
        d = self._base("ox", unit, slides, src)
        d.update(q=q, a=a, e=e)
        self.items.append(d)

    def short(self, unit, slides, q, a, e, src=None, num=False, tol=0.01):
        assert isinstance(a, (list, tuple)) and a, q
        d = self._base("short", unit, slides, src)
        d.update(q=q, a=[str(x) for x in a], e=e)
        if num:
            float(d["a"][0])
            d.update(num=True, tol=tol)
        self.items.append(d)

    def blank(self, unit, slides, q, a, e, num=False):
        """빈칸 넣기: src 를 '빈칸' 으로 고정한 short."""
        self.short(unit, slides, q, a, e, src="빈칸", num=num)

    def essay(self, unit, slides, q, answer, points, model, src=None):
        assert 4 <= len(points) <= 10, q
        d = self._base("essay", unit, slides, src)
        d.update(q=q, answer=answer, points=points, model=model)
        self.items.append(d)

    def save(self, name):
        raw = json.dumps(self.items, ensure_ascii=False, indent=1)
        for ch in BAD_CHARS:
            assert ch not in raw, f"금지 문자 {ch!r}"
        qs = {}
        for it in self.items:
            key = (it["type"], it["q"])
            assert key not in qs, f"질문 중복: {it['q'][:40]}"
            qs[key] = 1
        (HERE / name).write_text(raw, encoding="utf-8")
        cnt, blanks = {}, 0
        for it in self.items:
            cnt[it["type"]] = cnt.get(it["type"], 0) + 1
            if it.get("src") == "빈칸":
                blanks += 1
        print(name, len(self.items), cnt, "빈칸", blanks)


def ko_en(*forms):
    """허용 답 배열을 만든다. 공백 변형을 자동으로 더한다."""
    out = []
    for f in forms:
        for v in (f, f.replace(" ", "")):
            if v and v not in out:
                out.append(v)
    return out


def two(a, b, *extra):
    """빈칸 두 개짜리 정답: 'A, B' 와 'A B', 'AB' 를 모두 받아 준다."""
    out = [f"{a}, {b}", f"{a} {b}", f"{a}{b}", f"{a},{b}"]
    for x in extra:
        if x not in out:
            out.append(x)
    return out
