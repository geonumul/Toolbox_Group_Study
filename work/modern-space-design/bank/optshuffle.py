# -*- coding: utf-8 -*-
"""객관식 보기 자리 섞기 (모든 과목 문제은행 생성기가 함께 쓴다).

왜 있나
    보기를 손으로 적다 보면 정답을 자꾸 1번에 두는 버릇이 생긴다. 그러면
    학생이 내용을 몰라도 늘 같은 자리를 찍어 점수를 얻는다. 그래서 파일을
    쓰기 직전에 mcq 의 c 를 섞고 a 를 정답이 옮겨 간 자리로 고쳐 준다.

어떻게 섞나
    섞는 방식은 문항의 id 에서만 나온다(random.Random("optshuffle:" + id)).
    같은 id 는 늘 같은 후보 순열을 뽑으므로 생성기를 다시 돌려도 결과가 같다.
    후보 순열 중에서는 그 파일 안에서 아직 덜 쓰인 자리로 정답이 가는 것을
    고른다. 그래서 파일 하나만 놓고 봐도 정답이 네 자리에 고르게 퍼진다.
    자리를 고정한 문항도 셈에 넣으므로, 섞을 수 있는 문항이 그만큼 반대쪽으로
    가서 균형을 맞춘다.

무엇을 건드리지 않나 (lock)
    - 보기가 다른 보기를 끌어안는다: '위의 모든 것', '정답 없음'
    - 보기가 자리를 가리킨다: 보기 글 안의 '3번', 동그라미 번호
    - 보기가 순서대로 읽힌다: 숫자뿐인 보기, 앞머리 숫자가 오름/내림차순,
      연도가 순서대로인 보기. 섞으면 학생 눈에 오류로 보인다.
    - 해설(e)이나 문제(q)가 자리를 부른다: '4번은 ...', '마지막 보기'
      ('나머지 셋' 처럼 자리와 무관한 말은 고정 대상이 아니다)
    까닭은 lock_reason() 이 돌려준다.

해설의 동그라미 번호
    해설이 보기를 '①은 ...' 처럼 부르는 문항은 고정하는 대신, 보기를 섞은 뒤
    해설의 동그라미 번호를 옮겨 간 자리로 바꾼다. 뜻은 그대로다(① 은 언제나
    '첫 보기'). 다만 동그라미가 보기가 아니라 내용을 가리키는 경우가 있어서
    (제14조 ③항, '역할 ③ 보안', 'IF③ 시계열', '세 문제는 ① ..., ② ...')
    can_renumber() 의 조건을 모두 만족할 때만 바꾼다.

쓰는 법
    import optshuffle
    optshuffle.shuffle_bank(bank)   # 파일에 쓰기 직전 한 번
    optshuffle.check_ids(bank, IDS) # id 가 밀리지 않았는지 확인
"""
import random
import re

__all__ = ["shuffle_bank", "check_ids", "lock_reason", "is_locked", "can_renumber"]


def check_ids(items, ids):
    """만들어진 문항의 id 가 박아 둔 목록과 한 글자도 다르지 않은지 본다.

    대부분의 생성기는 id 를 목록 안 자리로 매긴다(f"wbb-{t}-{i:03d}"). 그래서
    문항을 맨 뒤가 아닌 곳에 끼워 넣으면 그 뒤 같은 유형의 id 가 통째로 한 칸씩
    밀리고, 학생이 푼 기록과 오답노트가 엉뚱한 문항을 가리키게 된다. 그 일이
    조용히 일어나지 않도록 여기서 멈춘다.

    문항을 정말 새로 넣거나 뺐다면 IDS 도 같이 고친다. 이때 밀려난 문항은
    내용이 바뀐 것이므로 id 를 새로 주는 것이 맞다.
    """
    got = [it.get("id") for it in items]
    ids = list(ids)
    if got == ids:
        return
    if len(got) != len(ids):
        raise AssertionError("문항 수가 %d 개에서 %d 개로 바뀌었다. IDS 를 함께 고쳤는지 확인할 것"
                             % (len(ids), len(got)))
    for i, (a, b) in enumerate(zip(got, ids)):
        if a != b:
            raise AssertionError("%d 번째 문항의 id 가 밀렸다: IDS 는 %r 인데 %r 로 만들어졌다" % (i, b, a))

CIRCLED = "①②③④⑤⑥⑦⑧⑨⑩"
_CIRCLED4 = "①②③④"
_CIRCLED_ANY = re.compile("[" + CIRCLED + "]")

# 자리를 직접 부르는 말. '나머지 셋' 은 자리와 무관하므로 넣지 않는다.
# 동그라미 번호는 따로 다루므로 맨 앞 갈래에 둔다(_POS_REF_NOCIRCLE 이 잘라 쓴다).
_POS_REF = re.compile(
    "[" + CIRCLED + "]"
    r"|(?<![0-9,.])[1-5]\s*번(?!\s*째)"            # 1번 ~ 5번 ('10,000번' 은 걸리지 않는다)
    r"|(?:보기|선지|선택지)\s*[1-5]"
    r"|(?:첫|두|세|네|다섯|마지막)\s*번째\s*(?:보기|선지|선택지|항목)"
    r"|마지막\s*(?:보기|선지|선택지)"
    r"|맨\s*(?:위|아래)\s*(?:보기|선지|선택지)"
    r"|(?:위|아래)에서\s*[1-5]\s*번째"
)
_POS_REF_NOCIRCLE = re.compile(_POS_REF.pattern.split("|", 1)[1])

# '위의 모든 것', '정답 없음' 처럼 다른 보기를 끌어안는 보기
_CATCH_ALL = re.compile(
    r"위의?\s*모든|위\s*모두|앞의?\s*모든"
    r"|모두\s*(?:다\s*)?(?:맞|옳|정답|해당)"
    r"|전부\s*다\s*(?:맞|옳)|이상\s*모두"
    r"|정답\s*(?:이\s*)?없|해당\s*(?:사항\s*)?없음|답\s*없음"
)

# 동그라미 뒤에 이런 말이 붙으면 보기 번호가 아니라 내용 번호다
_BAD_AFTER = re.compile("[" + CIRCLED + r"]\s*(?:항|조|호|절|단계|번|차|부|형|급|종|계층|역할|식|줄|기|유형)")
# 동그라미 앞에 이런 말이 붙어도 보기 번호가 아니다
_BAD_BEFORE = re.compile(r"(?:역할|단계|조건|조|항|법칙|원칙|순서|필요성|식|IF|Q)\s*[" + CIRCLED + "]")
# '세 문제는 ① ..., ② ...' 처럼 해설이 내용을 나열하는 경우
_ENUM_LEAD = re.compile(
    r"(?:두|세|네|다섯|[2-5])\s*(?:가지|문제|단계|요소|조건|항목|원칙|역할|특징|기능|유형|방법|계층|축|갈래)"
    r"(?:은|는|이|가|로|를)?\s*[" + _CIRCLED4 + "]"
)

# 앞머리 숫자 (앞에 붙는 글자는 세 자까지 봐 준다: 'L1', '약 1919', '제3')
_LEAD_NUM = re.compile(r"^[^0-9]{0,3}([0-9]+(?:[.,][0-9]+)*)")
_ANY_NUM = re.compile(r"[0-9]+(?:[.,][0-9]+)*")
_YEAR = re.compile(r"(?<![0-9])(1[6-9][0-9]{2}|20[0-9]{2})(?![0-9])")
# 숫자를 빼면 거의 남는 것이 없는 보기인지 볼 때 세지 않는 글자 ('103mm', '50-60%').
# 이 저장소가 금지한 붙임표 두 가지는 글자를 직접 쓰지 않고 코드값으로 적는다.
_NOT_COUNTED = set("0123456789,. \t\n%~+-/:()[]") | {chr(0x2013), chr(0x2014)}


def _num(s):
    return float(str(s).replace(",", ""))


def _monotone(vals):
    if len(vals) < 3 or len(set(vals)) != len(vals):
        return False
    return vals == sorted(vals) or vals == sorted(vals, reverse=True)


def _numericish(opt):
    """숫자와 단위뿐이라 순서대로 읽히기 쉬운 보기인가."""
    if not _ANY_NUM.search(opt):
        return False
    return sum(1 for ch in opt if ch not in _NOT_COUNTED) <= 4


def can_renumber(item):
    """보기를 섞은 뒤 해설의 동그라미 번호만 고쳐 주면 되는 문항인가."""
    c = item.get("c")
    if not isinstance(c, list) or len(c) != 4:
        return False
    e = item.get("e")
    if not isinstance(e, str):
        return False
    marks = _CIRCLED_ANY.findall(e)
    if not marks or any(m not in _CIRCLED4 for m in marks):
        return False
    if _BAD_AFTER.search(e) or _BAD_BEFORE.search(e) or _ENUM_LEAD.search(e):
        return False
    if _POS_REF_NOCIRCLE.search(e):
        return False
    for key in ("q", "qko"):
        v = item.get(key)
        if isinstance(v, str) and (_CIRCLED_ANY.search(v) or _POS_REF.search(v)):
            return False
    return not any(_CIRCLED_ANY.search(x) for x in c)


def lock_reason(item):
    """섞으면 안 되는 문항이면 그 까닭을, 섞어도 되면 None 을 돌려준다."""
    c = item.get("c")
    if item.get("type") != "mcq" or not isinstance(c, list) or len(c) < 2:
        return "mcq 아님"
    a = item.get("a")
    if not isinstance(a, int) or isinstance(a, bool):
        return "a 가 정수 아님"
    if not 0 <= a < len(c):
        return "a 범위 밖"

    for x in c:
        if _CATCH_ALL.search(x):
            return "보기가 다른 보기를 끌어안는다: " + x
        if _POS_REF.search(x):
            return "보기가 자리를 가리킨다: " + x

    if all(_numericish(x) for x in c):
        return "보기가 숫자뿐이라 순서대로 읽힌다"

    lead = [_LEAD_NUM.match(x) for x in c]
    if all(lead) and _monotone([_num(m.group(1)) for m in lead]):
        return "앞머리 숫자가 순서대로다"

    yrs = [_YEAR.search(x) for x in c]
    if all(yrs) and _monotone([int(m.group(1)) for m in yrs]):
        return "연도가 순서대로다"

    if can_renumber(item):
        return None

    for key in ("e", "q", "qko"):
        v = item.get(key)
        if isinstance(v, str):
            m = _POS_REF.search(v)
            if m:
                return "%s 가 자리를 부른다: %r" % (key, m.group(0))

    return None


def is_locked(item):
    return lock_reason(item) is not None


def _candidates(qid, n, k=16):
    """id 로만 정해지는 후보 순열. perm[i] = 새 i 번 자리에 올 옛 보기 번호."""
    rnd = random.Random("optshuffle:" + str(qid))
    seen, out = set(), []
    for _ in range(k * 12):
        if len(out) >= k:
            break
        p = tuple(rnd.sample(range(n), n))
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


# 동그라미 뒤 조사는 번호를 읽는 소리에 맞춘다(일, 삼 은 받침이 있고 이, 사 는 없다)
_PARTICLE = {"은": "은는", "는": "은는", "이": "이가", "가": "이가",
             "을": "을를", "를": "을를", "과": "과와", "와": "과와"}
_PARTICLE_RE = re.compile(r"([" + _CIRCLED4 + r"])(\s*)(은|는|이|가|을|를|과|와)(?![가-힣])")
_RANGE_RE = re.compile(r"([" + _CIRCLED4 + r"])\s*[~〜]\s*([" + _CIRCLED4 + r"])")
_RUN_RE = re.compile(r"[" + _CIRCLED4 + r"]{2,}")
_COMMA_RUN_RE = re.compile(r"([" + _CIRCLED4 + r"])((?:\s*,\s*[" + _CIRCLED4 + r"])+)")
_PAIR_RE = re.compile(r"([" + _CIRCLED4 + r"])\s*(?:와|과)\s*([" + _CIRCLED4 + r"])")


def _fix_particles(s):
    def rep(m):
        ch, gap, p = m.group(1), m.group(2), m.group(3)
        return ch + gap + _PARTICLE[p][0 if ch in "①③" else 1]
    return _PARTICLE_RE.sub(rep, s)


def _renumber(e, perm):
    """옛 j 번 보기는 perm.index(j) 자리로 간다. 해설의 동그라미를 그에 맞춰 옮긴다.

    '②~④', '①②③', '①, ③', '②와 ④' 처럼 번호를 묶어 부르는 자리는 옮긴 뒤
    다시 오름차순으로 적는다. 번호가 흩어져 범위(~)가 깨지면 낱개로 풀어 쓴다.
    마지막으로 번호를 읽는 소리에 맞게 조사를 고친다.
    """
    where = {j: perm.index(j) for j in range(len(perm))}

    def move(ch):
        return _CIRCLED4[where[_CIRCLED4.index(ch)]]

    def expand(m):
        lo, hi = sorted(_CIRCLED4.index(x) for x in m.groups())
        return _CIRCLED4[lo:hi + 1]

    def order(chs):
        return sorted(chs, key=_CIRCLED4.index)

    def pair(m):
        a, b = order(m.groups())
        return a + ("와" if a in "②④" else "과") + " " + b

    def comma(m):
        return ", ".join(order([m.group(1)] + re.findall("[" + _CIRCLED4 + "]", m.group(2))))

    out = _RANGE_RE.sub(expand, e)                          # 범위는 옮기기 전에 낱개로 푼다
    out = _CIRCLED_ANY.sub(lambda m: move(m.group(0)), out)  # 번호를 새 자리로 옮긴다
    out = _PAIR_RE.sub(pair, out)                            # 묶어 부르는 자리를 다시 오름차순으로
    out = _COMMA_RUN_RE.sub(comma, out)
    out = _RUN_RE.sub(lambda m: "".join(order(m.group(0))), out)
    return _fix_particles(out)


def shuffle_bank(items, stats=None):
    """파일 하나치 문항 목록을 받아 mcq 의 c 와 a 를 제자리에서 고쳐 준다.

    돌려주는 값은 (섞은 문항 수, 자리를 고정한 문항 수). stats 에 dict 를 주면
    {'locked': [(id, 까닭), ...], 'renumbered': [id, ...], 'used': [...]} 를 채운다.
    """
    used = [0] * 12
    moved = locked = 0
    lock_log, renum = [], []

    # 자리를 고정한 문항을 먼저 세어 둔다. 그래야 그 뒤에 나오든 앞에 나오든 상관없이
    # 섞을 수 있는 문항이 빈 자리 쪽으로 가서 파일 전체의 균형이 맞는다.
    free = []
    for it in items:
        if it.get("type") != "mcq":
            continue
        why = lock_reason(it)
        if why is None:
            free.append(it)
            continue
        if why != "mcq 아님":
            locked += 1
            lock_log.append((it.get("id"), why))
            a = it.get("a")
            if isinstance(a, int) and not isinstance(a, bool) and 0 <= a < len(used):
                used[a] += 1

    for it in free:
        c, a = it["c"], it["a"]
        best = min(_candidates(it["id"], len(c)), key=lambda p: used[p.index(a)])
        marked = can_renumber(it)
        it["c"] = [c[i] for i in best]
        it["a"] = best.index(a)
        if marked:
            it["e"] = _renumber(it["e"], best)
            renum.append(it.get("id"))
        used[it["a"]] += 1
        moved += 1
    if stats is not None:
        stats["locked"] = lock_log
        stats["renumbered"] = renum
        stats["used"] = used
    return moved, locked
