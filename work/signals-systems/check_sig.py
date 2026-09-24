# -*- coding: utf-8 -*-
"""신호및시스템 추가 검사 (공통 검사기 다음에 돌린다).
사용: python work/signals-systems/check_sig.py [파일.json ...] [--katex]
  파일을 안 주면 lesson/, notes/, bank/, terms/ 의 모든 json.
검사
  1) 금지 문자(em dash, en dash, 가운뎃점), 이모지
  2) 수식 밖에서 공백으로 둘러싸인 숫자 " 3 " (엔진 fmt() 가 이 모양을 수식 자리표로 오인해서 지워 버린다)
     고치는 법: 숫자를 $3$ 처럼 수식으로 감싸거나, 단위나 조사를 붙인다(3개, 3칸, 3이에요).
  3) $ 짝, 수식 안 한글 (KaTeX 에서 경고)
  4) --katex: Chrome headless 로 모든 수식을 KaTeX 0.16.11 로 실제 렌더링 (formula 의 tex, parts.sym 은 $ 없이 통째로)
"""
import sys, json, re, pathlib, subprocess, html, tempfile, os
sys.stdout.reconfigure(encoding="utf-8")
W = pathlib.Path(__file__).resolve().parent
BAD = {"\u2014": "em dash", "\u2013": "en dash", "\u00b7": "가운뎃점", "\u30fb": "가운뎃점"}
MATH = re.compile(r"\$\$[\s\S]+?\$\$|\$[^$\n]+?\$")
EMOJI = re.compile("[\U0001F300-\U0001FAFF\u2600-\u27BF]")
SKIP = {"svg", "fig", "id", "img"}
TEXKEYS = {"tex", "sym"}
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"


def walk(o, path=""):
    if isinstance(o, str):
        yield path, o
    elif isinstance(o, list):
        for i, x in enumerate(o):
            yield from walk(x, f"{path}[{i}]")
    elif isinstance(o, dict):
        for k, v in o.items():
            if k in SKIP:
                continue
            yield from walk(v, f"{path}.{k}")


def check_file(f, items, errs, warns):
    raw = f.read_text(encoding="utf-8")
    for ch, name in BAD.items():
        if ch in raw:
            errs.append(f"{f.name}: {name} {raw.count(ch)}개")
    try:
        d = json.loads(raw)
    except Exception as e:
        errs.append(f"{f.name}: JSON 오류 {e}")
        return
    for p, s in walk(d):
        key = p.rsplit(".", 1)[-1].split("[")[0]
        where = f"{f.name}{p}"
        if EMOJI.search(s):
            errs.append(f"{where}: 이모지")
        if key in TEXKEYS:
            items.append((where, s, True))
            continue
        if s.count("$") % 2:
            errs.append(f"{where}: $ 짝 안 맞음: {s[:60]}")
            continue
        for m in MATH.finditer(s):
            t = m.group(0)
            disp = t.startswith("$$")
            body = t[2:-2] if disp else t[1:-1]
            items.append((where, body, disp))
            if re.search("[가-힣]", body) and "\\text" not in body:
                errs.append(f"{where}: 수식 안 한글은 \\text{{}} 로: {body[:50]}")
        # (2026-09-23) 엔진 fmt() 의 숫자 자리표 버그는 고쳐졌다. 이제는 권장 사항이라 경고로만 알린다.
        plain = MATH.sub(" X ", s)
        for m in re.finditer(r"(?<= )\d+(?= )", plain):
            a = max(0, m.start() - 15)
            warns.append(f"{where}: 공백 사이 숫자 '{plain[a:m.end() + 10]}' ($..$ 로 감싸면 더 보기 좋아요)")
            break


def katex(items):
    page = """<!doctype html><meta charset="utf-8">
<script src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<body><pre id="out">NOT RUN</pre><script>
var items = %s; var bad = [];
if (!window.katex) { document.getElementById("out").textContent = "KATEX NOT LOADED"; }
else {
  items.forEach(function (it) {
    try { katex.renderToString(it[1], {displayMode: it[2], throwOnError: true, strict: false}); }
    catch (e) { bad.push(it[0] + "  ::  " + it[1].slice(0, 120) + "  ::  " + String(e.message).slice(0, 160)); }
  });
  document.getElementById("out").textContent = "CHECKED " + items.length + "\\nBAD " + bad.length + "\\n" + bad.join("\\n");
}
</script>""" % json.dumps(items, ensure_ascii=False).replace("</", "<\\/")
    tmpdir = pathlib.Path(tempfile.gettempdir()) / "sig_katex"
    tmpdir.mkdir(exist_ok=True)
    tmp = tmpdir / f"k{os.getpid()}.html"
    tmp.write_text(page, encoding="utf-8")
    prof = tmpdir / "profile"
    r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", f"--user-data-dir={prof}", "--no-first-run",
                        "--virtual-time-budget=30000", "--dump-dom", tmp.as_uri()], capture_output=True, timeout=300)
    out = r.stdout.decode("utf-8", "replace")
    m = re.search(r'<pre id="out">(.*?)</pre>', out, re.S)
    tmp.unlink(missing_ok=True)
    res = html.unescape(m.group(1)) if m else out[:2000]
    return res


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    files = [pathlib.Path(a) for a in args] or sorted(
        [p for d in ("lesson", "notes", "bank", "terms") for p in (W / d).glob("*.json")])
    errs, warns, items = [], [], []
    for f in files:
        check_file(f, items, errs, warns)
    for w in warns[:20]:
        print("  경고:", w)
    for e in errs[:80]:
        print("  오류:", e)
    if len(errs) > 80:
        print(f"  ... 외 {len(errs) - 80}건")
    print(f"파일 {len(files)}개, 수식 {len(items)}개, 오류 {len(errs)}건, 경고 {len(warns)}건")
    ok = not errs
    if "--katex" in sys.argv:
        res = katex(items)
        print(res[:6000])
        ok = ok and "\nBAD 0" in ("\n" + res.split("\n", 1)[-1]) if res.startswith("CHECKED") else False
    print("결과:", "통과" if ok else "고칠 것 있음")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
