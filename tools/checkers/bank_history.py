"""문제 번호는 그대로인데 내용만 바뀐 것을 찾는다.

왜 따로 필요한가:
  문제 번호(id)는 학생의 푼 기록과 오답노트가 가리키는 열쇠다.
  번호를 그대로 둔 채 질문을 다른 내용으로 바꾸면
  bank_check 도, build_site 도, site_test 도 전부 통과한다.
  대신 예전에 그 번호를 틀렸던 학생의 오답노트가 엉뚱한 문제를 가리킨다.
  검사기가 조용하다는 것이 안전하다는 뜻이 아닌 자리라서 이 검사가 있다.

사용:
  python tools/checkers/bank_history.py work/<과목>/bank/*.json
  python tools/checkers/bank_history.py --all
  기준은 git 의 HEAD 다. --ref <커밋> 으로 바꿀 수 있다.

내용이 바뀐 것이 일부러 한 일이면(문항을 새로 쓰기로 했다면) 번호도 새로 주는 편이 맞다.
그러면 예전 기록은 사라진 문항으로 남고, 새 문항은 처음부터 새 기록을 쌓는다.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
WATCH = ("q", "a", "c", "type", "part")   # 이 칸이 달라지면 사실상 다른 문항이다


def need_ref(ref):
    """기준 커밋이 실제로 있는지 먼저 본다. git 이 안 되면 조용히 통과시키지 않고 여기서 멈춘다."""
    r = subprocess.run(["git", "rev-parse", "--verify", f"{ref}^{{commit}}"],
                       cwd=ROOT, capture_output=True)
    if r.returncode:
        print(f"기준 '{ref}' 를 찾을 수 없다. git 저장소가 맞는지, 커밋 이름이 맞는지 확인할 것")
        sys.exit(2)


def built_bank(slug, ref):
    """저장소 밖 문제은행(그래프신경망)은 빌드된 subjects/<과목>/data/bank.js 를 기준으로 삼는다.
       원본이 git 밖에 있어도 학생이 실제로 본 문항은 그 파일에 들어 있기 때문이다."""
    r = subprocess.run(["git", "show", f"{ref}:subjects/{slug}/data/bank.js"], cwd=ROOT, capture_output=True)
    if r.returncode:
        return None
    s = r.stdout.decode("utf-8")
    i, j = s.find("["), s.rfind("]")
    try:
        return json.loads(s[i:j + 1]) if i >= 0 and j > i else None
    except Exception:
        return None


def old_version(path, ref):
    """(옛 내용, 왜) 를 준다. 옛 내용이 None 이면 그 파일은 기준에 없다."""
    try:
        rel = Path(path).resolve().relative_to(ROOT).as_posix()
    except ValueError:
        # 저장소 밖 경로: 그래프신경망 문제은행이 여기 해당한다
        b = built_bank("gnn", ref)
        return (b, "빌드본 기준") if b is not None else (None, "저장소 밖이고 빌드본도 없음")
    r = subprocess.run(["git", "show", f"{ref}:{rel}"], cwd=ROOT, capture_output=True)
    if r.returncode:
        msg = r.stderr.decode("utf-8", "replace")
        if "does not exist" in msg or "exists on disk" in msg or "unknown revision" in msg:
            return None, "새 파일"          # 아직 커밋된 적 없는 파일
        return None, "git 오류: " + msg.strip()[:80]
    try:
        return json.loads(r.stdout.decode("utf-8")), ""
    except Exception as e:
        return None, f"기준본 JSON 오류: {e}"


def check_outside(paths, ref):
    """저장소 밖 문제은행: 빌드본은 여러 파일을 합친 것이라 파일 하나와 견주면 안 된다.
       준 파일들을 한 덩어리로 모아 빌드본과 한 번에 견준다."""
    old = built_bank("gnn", ref)
    if old is None:
        print("저장소 밖 문제은행: 빌드본(subjects/gnn/data/bank.js)이 기준에 없음")
        return False
    new_items = []
    for path in paths:
        try:
            new_items += json.loads(Path(path).read_text(encoding="utf-8"))
        except Exception as e:
            print(f"{path}: JSON 오류 {e}")
            return False
    # 빌드가 자동으로 만드는 용어 퀴즈(term-...)는 원본 파일에 없으니 견주지 않는다
    om = {q.get("id"): q for q in old
          if isinstance(q, dict) and not str(q.get("id", "")).startswith("term-")}
    nm = {q.get("id"): q for q in new_items if isinstance(q, dict)}
    hits, gone = [], [i for i in om if i not in nm]
    for qid, q in nm.items():
        o = om.get(qid)
        if not o:
            continue
        for f in WATCH:
            a, b = o.get(f), q.get(f)
            if isinstance(a, str) and isinstance(b, str):
                a, b = " ".join(a.split()), " ".join(b.split())
            if a != b:
                hits.append((qid, f, o.get(f), q.get(f)))
                break
    print(f"저장소 밖 문제은행 {len(paths)}개 파일, 문항 {len(nm)}개, 빌드본 기준 내용 바뀐 것 {len(hits)}개"
          + (f", 사라진 번호 {len(gone)}개" if gone else ""))
    for qid, f, a, b in hits[:20]:
        print(f"  오류: {qid} 의 {f} 가 바뀜")
        print(f"     전: {str(a)[:70]}")
        print(f"     후: {str(b)[:70]}")
    for i in gone[:10]:
        print(f"  오류: {i} 번호가 사라짐. 그 번호를 푼 기록도 같이 사라진다")
    return not hits and not gone


def check(path, ref):
    old, why = old_version(path, ref)
    if old is None:
        print(f"{path}: {why}" + (", 건너뜀" if why == "새 파일" else ""))
        return why == "새 파일"          # git 오류나 깨진 기준본은 통과가 아니다
    try:
        new = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as e:
        print(f"{path}: JSON 오류 {e}")
        return False
    if not isinstance(old, list) or not isinstance(new, list):
        print(f"{path}: 배열이 아님")
        return False
    om = {q.get("id"): q for q in old if isinstance(q, dict)}
    hits = []
    for q in new:
        if not isinstance(q, dict):
            continue
        o = om.get(q.get("id"))
        if not o:
            continue                     # 새로 생긴 번호는 이 검사의 관심 밖
        for f in WATCH:
            a, b = o.get(f), q.get(f)
            if isinstance(a, str) and isinstance(b, str):
                a, b = " ".join(a.split()), " ".join(b.split())
            if a != b:
                hits.append((q.get("id"), f, o.get(f), q.get(f)))
                break
    gone = [i for i in om if i not in {q.get("id") for q in new if isinstance(q, dict)}]
    print(f"{path}: 문항 {len(new)}개, 번호 그대로인데 내용 바뀐 것 {len(hits)}개"
          + (f", 사라진 번호 {len(gone)}개" if gone else ""))
    for qid, f, a, b in hits[:20]:
        print(f"  오류: {qid} 의 {f} 가 바뀜")
        print(f"     전: {str(a)[:70]}")
        print(f"     후: {str(b)[:70]}")
    for i in gone[:10]:
        print(f"  오류: {i} 번호가 사라짐. 그 번호를 푼 기록도 같이 사라진다")
    return not hits and not gone


if __name__ == "__main__":
    args = sys.argv[1:]
    ref = "HEAD"
    if "--ref" in args:
        i = args.index("--ref")
        ref = args[i + 1]
        del args[i:i + 2]
    need_ref(ref)
    if "--all" in args or not args:
        args = [str(p) for p in sorted(ROOT.glob("work/*/bank/*.json"))]
    inside, outside = [], []
    for a in args:
        try:
            Path(a).resolve().relative_to(ROOT); inside.append(a)
        except ValueError:
            outside.append(a)
    ok = all([check(p, ref) for p in inside])
    if outside:
        ok = check_outside(outside, ref) and ok
    print("결과:", "통과" if ok else "오류 있음")
    sys.exit(0 if ok else 1)
