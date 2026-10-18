# -*- coding: utf-8 -*-
"""10월 18일 업데이트 만들기: questions.py 하나에서 사이트 페이지와 PDF 두 개를 만든다.

사용: python work/modern-space-design/upd1018/build.py            (사이트 페이지 + PDF 두 개)
     python work/modern-space-design/upd1018/build.py --no-pdf   (사이트 페이지만)
그 다음 사이트는 python tools/build_site.py modern-space-design --no-home

출력
  work/modern-space-design/pages/upd1018.html          사이트 탭 "10월18일 업데이트" (subject.json extraPages)
  02_작업/근현대공간디자인/근현대_예상시험지.pdf         시험지 (답 없음, 쓰는 칸 있음)
  02_작업/근현대공간디자인/근현대_예상시험지_답지.pdf    답지 (모범답안, 슬라이드 쪽, 채점 키워드)

그림: 사이트는 img/U#/pNNN.jpg 를 CSS 로 잘라 보이고 (캡션과 제목을 가림), PDF 는 같은 칸을 PIL 로 잘라 넣는다.
PDF 는 헤드리스 Chrome (임시 프로필) 으로 찍는다. Chrome 을 이미지 이름으로 죽이지 않는다 (띄운 프로세스만 정리).
"""
import base64, html, io, pathlib, shutil, subprocess, sys, tempfile

sys.stdout.reconfigure(encoding="utf-8")
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import questions as QD  # noqa: E402

W = HERE.parent                         # work/modern-space-design
REPO = W.parents[1]                     # Toolbox_Group_Study
IMG = REPO / "subjects" / "modern-space-design" / "img"
PAGE_OUT = W / "pages" / "upd1018.html"
PDF_DIR = REPO.parents[1] / "02_작업" / "근현대공간디자인"
PDF_PAPER = PDF_DIR / "근현대_예상시험지.pdf"
PDF_KEY = PDF_DIR / "근현대_예상시험지_답지.pdf"
BAD = ("\u2014", "\u2013", "\u00b7", "\u30fb")
CIRC = "①②③④⑤⑥"
SLIDE_W, SLIDE_H = 1000, 750
CHROME = [pathlib.Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
          pathlib.Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
          pathlib.Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")]

QS = QD.ordered()
SEC_NAME = dict(QD.SECTIONS)


def esc(s):
    return html.escape(str(s), quote=True)


def unit_label(q):
    return ", ".join(QD.UNIT[u] for u in QD.units_of(q))


def slide_path(deck, p):
    return IMG / deck / f"p{int(p):03d}.jpg"


# ---------------------------------------------------------------- 그림
def crop_b64(deck, p, box, width=None, quality=85):
    from PIL import Image
    im = Image.open(slide_path(deck, p)).convert("RGB")
    if box:
        x, y, w, h = box
        X, Y = im.size
        im = im.crop((round(x * X), round(y * Y), round((x + w) * X), round((y + h) * Y)))
    if width and im.width > width:
        im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=quality, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def site_crop(deck, p, box, alt):
    """사이트용: 원본 슬라이드 그림을 CSS 로 잘라 보인다 (캡션과 제목이 칸 밖으로 나가게)."""
    x, y, w, h = box
    cw, ch = w * SLIDE_W, h * SLIDE_H
    mw = round(min(cw, 600, 430 * cw / ch))
    return (f'<div class="crop" style="aspect-ratio:{cw:.0f}/{ch:.0f};max-width:{mw}px">'
            f'<img loading="lazy" decoding="async" alt="{esc(alt)}" src="img/{deck}/p{int(p):03d}.jpg" '
            f'style="width:{100 / w:.3f}%;left:-{x / w * 100:.3f}%;top:-{y / h * 100:.3f}%"></div>')


# ---------------------------------------------------------------- 답 (사이트와 답지가 같이 쓴다)
def keys_html(keys):
    return '<p class="k"><b>채점 키워드</b> ' + ", ".join(esc(k) for k in keys) + "</p>" if keys else ""


def src_html(q):
    return f'<p class="src">근거: {esc(q["src"])}</p>'


def note_html(s):
    return f'<p class="nt">{s}</p>' if s else ""


def answer_html(q, mode):
    """mode: site (답 보기 속) 또는 key (답지 PDF)"""
    k = q["kind"]
    out = []
    if k == "mcq":
        a = q["ans"]
        out.append(f'<p><b>정답 {CIRC[a - 1]}</b> {q["choices"][a - 1]}</p><p>{q["why"]}</p>')
    elif k == "short":
        out.append(f'<p>{q["ans"]}</p>' + note_html(q.get("note")))
    elif k == "pic":
        out.append(f'<p><b>작품</b> {esc(q["work"])}<br><b>설계자</b> {esc(q["who"])}<br><b>장소, 연도</b> {esc(q["where"])}</p>')
        out.append("<p><b>특징 (슬라이드 말)</b></p><ul>" + "".join(f"<li>{f}</li>" for f in q["feats"]) + "</ul>")
        out.append(keys_html(q["keys"]))
    elif k == "list":
        must = sum(1 for _, items in q["groups"] for it in items if it[3])
        out.append(f'<p class="nt">[꼭 쓸 것] 표시 {must}개는 슬라이드 분량이 많거나 강조된 작품이다. 이것부터 쓰고 나머지를 더한다.</p>')
        for g, items in q["groups"]:
            out.append(f'<p class="g"><b>{esc(g)}</b></p><ul class="lst">')
            for work, meta, ref, m in items:
                out.append(f'<li>{"<b>[꼭 쓸 것]</b> " if m else ""}{"<b>" + esc(work) + "</b>" if m else esc(work)}'
                           f' <span class="m">{esc(meta)}</span> <span class="r">({esc(ref)})</span></li>')
            out.append("</ul>")
        out.append(note_html(q.get("note")))
    elif k == "brief":
        out.append("<ul>" + "".join(f"<li>{a}</li>" for a in q["ans"]) + "</ul>" + keys_html(q["keys"]))
    elif k == "essay":
        out.append(f'<p><b>서론</b> {q["intro"]}</p><p><b>핵심</b></p><ol>'
                   + "".join(f"<li><b>{esc(h)}</b> {t}</li>" for h, t in q["points"]) + "</ol>")
        out.append("<p><b>대표 사례</b></p><ul>" + "".join(f"<li>{c}</li>" for c in q["cases"]) + "</ul>")
        out.append(f'<p><b>결론</b> {q["concl"]}</p>' + keys_html(q["keys"]) + note_html(q.get("note")))
    elif k == "change":
        for label, works, feats in q["periods"]:
            out.append(f'<p class="g"><b>{esc(label)}</b></p><p class="w">작품: {", ".join(esc(x) for x in works)}</p>'
                       "<ul>" + "".join(f"<li>{f}</li>" for f in feats) + "</ul>")
        out.append(f'<p><b>변화</b> {q["what"]}</p><p><b>이유</b> {q["why"]}</p>' + keys_html(q["keys"]) + note_html(q.get("note")))
    out.append(src_html(q))
    if k == "pic":
        deck, p, _ = q["img"]
        if mode == "site":
            out.append(f'<div class="full"><p class="nt">원본 슬라이드 ({QD.UNIT[deck]} p.{p}, 캡션 포함)</p>'
                       f'<img loading="lazy" decoding="async" alt="{esc(q["work"])}" src="img/{deck}/p{int(p):03d}.jpg"></div>')
        else:
            out.append(f'<div class="full"><p class="nt">원본 슬라이드 ({QD.UNIT[deck]} p.{p}, 캡션 포함)</p>'
                       f'<img alt="" src="{crop_b64(deck, p, None, width=760, quality=78)}"></div>')
    return "".join(out)


def question_body(q, mode):
    """문제 글 + 보기 + 그림. mode: site, paper, key (key 는 보기와 그림을 줄인다)"""
    out = [f'<div class="qq">{q["q"]}</div>']
    if q["kind"] == "mcq" and mode != "key":
        out.append('<ol class="ch">' + "".join(f"<li>{CIRC[i]} {c}</li>" for i, c in enumerate(q["choices"])) + "</ol>")
    if q["kind"] == "pic" and mode != "key":
        deck, p, box = q["img"]
        out.append(site_crop(deck, p, box, "문제 그림") if mode == "site"
                   else f'<div class="fig"><img alt="" src="{crop_b64(deck, p, box)}"></div>')
    return "".join(out)


def qhead(q):
    return f'<div class="qh"><span class="qn">{q["no"]}.</span>{esc(QD.KIND_LABEL[q["kind"]])}, {esc(unit_label(q))}</div>'


# ---------------------------------------------------------------- 실전 20문항 고르기 (선배 후기 비율)
PICK20 = [("mcq", "19세기 철물건축"), ("mcq", "빈 분리파(Wiener Secession)"), ("mcq", "표현주의 건축물과 건축가의 짝"), ("mcq", "프레이리형 주택(대초원 주택)의 특징"),
          ("short", "CIAM 은 무엇의 약자"), ("short", "공업화 건축의 3요소"), ("short", "건축의 5원칙"), ("short", "1908년"), ("short", "Less is more"),
          ("pic", "바르셀로나 박람회 독일관"), ("pic", "아인슈타인 타워"), ("list", "아르누보(독일의 유겐트슈틸 포함)"), ("list", "4강(독일공작연맹"),
          ("brief", "장점과 단점"),
          ("essay", "신건축"), ("change", "르 코르뷔지에의"), ("change", "미스 반 데어 로에의"), ("change", "프랭크 로이드 라이트의"),
          ("change", "오토 바그너의"), ("essay", "아르누보(Art Nouveau)의 등장")]


def pick20():
    """선배 후기 비율 (논술 6 + 나머지 14) 로 고른 20문항. 문항 글의 한 조각으로 찾는다 (하나만 맞아야 한다)"""
    got = []
    for kind, word in PICK20:
        m = [q for q in QS if q["kind"] == kind and word in q["q"] + q.get("work", "")]
        if len(m) != 1:
            raise SystemExit(f"실전 20문항 고르기: '{word}' ({kind}) 에 맞는 문항이 {len(m)}개")
        got.append(m[0])
    units = {u for q in got for u in QD.units_of(q)}
    if len(got) != 20 or len(units) != 9 or sum(1 for q in got if QD.KIND_SEC[q["kind"]] == "essay") != 6:
        raise SystemExit(f"실전 20문항 묶음이 이상해요: {len(got)}문항, 단원 {sorted(units)}")
    return sorted(got, key=lambda q: q["no"])


def counts():
    sec = {s: [q for q in QS if QD.KIND_SEC[q["kind"]] == s] for s, _ in QD.SECTIONS}
    by_unit = {u: 0 for u in QD.UNIT}
    for q in QS:
        for u in QD.units_of(q):
            by_unit[u] += 1
    return sec, by_unit


# ---------------------------------------------------------------- 사이트 페이지
SITE_CSS = """
#upd1018{padding-top:22px;color:var(--ink)}
#upd1018 .eye{font-size:13px;color:var(--sub)}
#upd1018 h1{font-size:26px;line-height:1.35;margin:4px 0 8px;font-weight:700}
#upd1018 h2{font-size:19px;margin:36px 0 4px;padding-bottom:6px;border-bottom:1px solid var(--ink);font-weight:700}
#upd1018 h3{font-size:16px;margin:22px 0 6px;font-weight:700}
#upd1018 p,#upd1018 li{font-size:15px}
#upd1018 .lead{color:var(--ink-2)}
#upd1018 .nt{color:var(--sub);font-size:13.5px}
#upd1018 table.t{border-collapse:collapse;width:100%;margin:8px 0;font-size:14.5px}
#upd1018 table.t th,#upd1018 table.t td{border-bottom:1px solid var(--line);padding:6px 8px;text-align:left;vertical-align:top}
#upd1018 table.t th{font-weight:600;color:var(--ink-2);white-space:nowrap}
#upd1018 ul.plain{padding-left:1.2em}
#upd1018 .q{border-top:1px solid var(--line);padding:16px 0 12px}
#upd1018 .qh{font-size:13px;color:var(--sub);margin-bottom:4px}
#upd1018 .qn{color:var(--ink);font-size:16px;font-weight:700;margin-right:8px}
#upd1018 .qq{font-size:15.5px;line-height:1.75}
#upd1018 ol.ch{list-style:none;padding:0;margin:8px 0 0}
#upd1018 ol.ch li{padding:2px 0 2px 1.5em;text-indent:-1.5em;font-size:15px}
#upd1018 .crop{position:relative;overflow:hidden;width:100%;margin:10px 0 2px;border:1px solid var(--line);background:#fff}
#upd1018 .crop img{position:absolute;max-width:none;height:auto;display:block}
#upd1018 details{margin-top:10px}
#upd1018 summary{cursor:pointer;color:var(--sub);font-size:14px;display:inline-block;padding:2px 0;list-style:none;border-bottom:1px solid var(--line-2)}
#upd1018 summary::-webkit-details-marker{display:none}
#upd1018 details[open] summary{color:var(--ink)}
#upd1018 .a{margin-top:8px;padding-left:12px;border-left:2px solid var(--line-2)}
#upd1018 .a p,#upd1018 .a li{font-size:14.5px;margin:4px 0}
#upd1018 .a ul,#upd1018 .a ol{padding-left:1.3em;margin:4px 0 8px}
#upd1018 .a .g{margin-top:10px}
#upd1018 .a .w{color:var(--ink-2)}
#upd1018 .a .m{color:var(--ink-2)}
#upd1018 .a .r,#upd1018 .a .src{color:var(--sub);font-size:13px}
#upd1018 .a .k{color:var(--ink-2)}
#upd1018 .full img{width:100%;max-width:520px;border:1px solid var(--line);display:block}
"""


def build_site_page():
    sec, by_unit = counts()
    n = len(QS)
    I = QD.INFO
    h = [f"<style>{SITE_CSS}</style>",
         '<div class="eye">10월 18일 업데이트</div>',
         "<h1>선배 후기로 본 중간고사, 그리고 예상 시험지</h1>",
         f'<p class="lead">{esc(I["src"])} 아래에 시험 모양을 정리하고, 그 모양대로 만든 예상 시험지를 붙였어요. '
         "답은 모두 <b>답 보기</b> 를 눌러야 보여요. 내용은 2026 강의자료 9개 덱에서만 가져왔고, 답마다 덱과 쪽을 적었어요.</p>",
         "<h2>선배 후기 요약 (2024년 2학기 중간고사)</h2>",
         '<table class="t">' + "".join(f"<tr><th>{esc(a)}</th><td>{esc(b)}</td></tr>" for a, b in I["format"]) + "</table>",
         "<h3>공부 전략</h3><ul class=\"plain\">" + "".join(f"<li>{s}</li>" for s in I["strategy"]) + "</ul>",
         "<h3>문제 예시</h3><ol>" + "".join(f"<li>{esc(s)}</li>" for s in I["examples"]) + "</ol>",
         f'<p class="nt">{esc(I["caveat"])}</p>',
         "<h2>이 시험지 쓰는 법</h2>",
         f"<p>실제 시험은 <b>약 20문제 (논술 6)</b> 예요. 이 시험지는 그보다 훨씬 많은 <b>{n}문항짜리 연습용 전체판</b>이에요. "
         "선배가 말한 유형을 모두 넣었어요: 그림 보고 특징과 디자이너 쓰기, 아는 대로 모두 적기 (단원마다 하나 이상), "
         "신건축과 대립 양식 논술, 건축가마다 초기작과 후기작의 디자인 변화 논술, CIAM 과 공업화 건축 같은 단답.</p>",
         "<h3>목차</h3>",
         '<table class="t"><tr><th>구역</th><th>문항</th><th>번호</th></tr>'
         + "".join(f"<tr><td>{esc(name)}</td><td>{len(sec[s])}문항</td><td>{sec[s][0]['no']}~{sec[s][-1]['no']}번</td></tr>"
                   for s, name in QD.SECTIONS) + "</table>",
         '<p class="nt">약술형 안에서는 그림 문제, 아는 대로 모두 적기, 그 밖의 약술 순서예요. 논술형은 신건축과 대립 양식, 건축가별 초기작과 후기작, 주제 논술 순서예요.</p>',
         "<h3>단원별 문항 수</h3>",
         '<table class="t"><tr>' + "".join(f"<th>{QD.UNIT[u]}</th>" for u in QD.UNIT) + "</tr><tr>"
         + "".join(f"<td>{by_unit[u]}</td>" for u in QD.UNIT) + "</tr></table>",
         '<p class="nt">한 문항이 여러 단원에 걸치면 단원마다 하나로 셌어요. 슬라이드 분량이 많은 2강, 3강, 7강에 문항이 더 많아요.</p>',
         "<h3>실전처럼 20문항만 풀어 보기</h3>",
         "<p>선배 후기의 비율 (논술 6 + 객관식, 단답, 약술 14) 로 고른 묶음이에요. 9개 단원이 모두 들어가요. 시간을 재고 풀어 보세요.</p>",
         "<p><b>" + ", ".join(str(q["no"]) for q in pick20()) + "번</b></p>"]
    for s, name in QD.SECTIONS:
        h.append(f"<h2>{esc(name)} ({len(sec[s])}문항)</h2>")
        for q in sec[s]:
            h.append(f'<div class="q">{qhead(q)}{question_body(q, "site")}'
                     f'<details><summary>답 보기</summary><div class="a">{answer_html(q, "site")}</div></details></div>')
    text = "\n".join(h) + "\n"
    check(text, "upd1018.html")
    PAGE_OUT.write_text(text, encoding="utf-8", newline="\n")
    print(f"사이트 페이지: {PAGE_OUT} ({len(text) / 1e3:.0f} KB, {n}문항)")


# ---------------------------------------------------------------- PDF
PDF_CSS = """
@page{size:A4;margin:15mm 16mm 16mm 16mm;
  @bottom-center{content:counter(page) " / " counter(pages);font-family:"Malgun Gothic",sans-serif;font-size:8.5pt;color:#777}}
*{box-sizing:border-box}
body{margin:0;font-family:"Malgun Gothic","Apple SD Gothic Neo",sans-serif;font-size:10.3pt;line-height:1.6;color:#111;word-break:keep-all;overflow-wrap:break-word}
h1{font-size:17pt;margin:0 0 1mm;font-weight:700}
.sub{color:#555;font-size:10pt;margin:0 0 3mm}
.idline{margin:3mm 0 4mm;font-size:10.5pt}
.idline span{display:inline-block;border-bottom:0.6pt solid #333;width:45mm;margin:0 8mm 0 2mm}
.box{border:0.6pt solid #777;padding:2.5mm 3.5mm;font-size:9.5pt;color:#222;margin-bottom:2mm}
.box p{margin:0.6mm 0}
h2{font-size:12.5pt;border-bottom:0.8pt solid #111;padding-bottom:1mm;margin:5mm 0 1mm;font-weight:700}
.blk{break-inside:avoid}
.q{break-inside:avoid;padding:2.6mm 0 3mm;border-bottom:0.3pt solid #bbb}
.qh{font-size:8.6pt;color:#666;margin-bottom:0.6mm}
.qn{font-weight:700;font-size:11pt;color:#111;margin-right:2mm}
.qq{font-size:10.5pt}
ol.ch{list-style:none;padding:0 0 0 3mm;margin:1.2mm 0 0}
ol.ch li{padding:0.3mm 0 0.3mm 5mm;text-indent:-5mm}
.fig img{display:block;max-width:112mm;max-height:62mm;border:0.4pt solid #999;margin:2mm 0 1mm}
.ln{height:7.6mm;border-bottom:0.4pt solid #aaa}
.q.wl{border-bottom:0;padding-bottom:4mm}
.ans{margin-top:2.5mm;font-size:10pt;color:#333}
.ans span{display:inline-block;border-bottom:0.5pt solid #555;width:120mm}
.a{margin-top:1.5mm;padding-left:3mm;border-left:0.8pt solid #999;font-size:9.8pt}
.a p{margin:0.8mm 0}
.a ul,.a ol{margin:0.6mm 0 1.4mm;padding-left:5mm}
.a li{margin:0.3mm 0}
.a .g{margin-top:2mm}
.a .w,.a .m,.a .k{color:#333}
.a .r,.a .src,.a .nt{color:#666;font-size:8.8pt}
.full img{display:block;width:62mm;border:0.4pt solid #999;margin:1mm 0}
"""
LINES = {"pic": 5, "list": 7, "brief": 5, "essay": 14, "change": 14}


def paper_html():
    sec, _ = counts()
    n = len(QS)
    h = ["<!doctype html><html lang=\"ko\"><head><meta charset=\"utf-8\"><title>근현대 예상시험지</title>",
         f"<style>{PDF_CSS}</style></head><body>",
         "<h1>근현대 공간디자인 중간고사 예상 시험지</h1>",
         f'<p class="sub">연습용 전체판, {n}문항. 2026 강의자료 9개 덱 기준</p>',
         '<div class="idline">학번<span></span>이름<span></span></div>',
         '<div class="box"><p><b>실제는 약 20문제 (논술 6), 연습용 전체판</b>이다. 선배 후기 (2024년 2학기): 논술형 6개, 단답과 객관식 합쳐 10~15개, 시간이 빡빡함.</p>'
         "<p>구성: " + ", ".join(f"{name} {len(sec[s])}문항" for s, name in QD.SECTIONS) + ". "
         "실전처럼 20문항만 풀려면 " + ", ".join(str(q["no"]) for q in pick20()) + "번.</p>"
         "<p>답은 슬라이드에 나온 말로 쓴다. 그림 문제는 그림의 캡션과 제목을 가렸다.</p></div>"]
    for s, name in QD.SECTIONS:
        items = sec[s]
        for i, q in enumerate(items):
            nl = LINES.get(q["kind"], 0)
            body = f'<div class="q{" wl" if nl else ""}">{qhead(q)}{question_body(q, "paper")}'
            if q["kind"] == "short":
                body += '<div class="ans">답: <span></span></div>'
            body += "".join('<div class="ln"></div>' for _ in range(nl)) + "</div>"
            if i == 0:   # 구역 제목이 쪽 끝에 홀로 남지 않게 첫 문항과 묶는다
                body = f'<div class="blk"><h2>{esc(name)} ({len(items)}문항)</h2>{body}</div>'
            h.append(body)
    h.append("</body></html>")
    return "\n".join(h)


def key_html():
    sec, _ = counts()
    h = ["<!doctype html><html lang=\"ko\"><head><meta charset=\"utf-8\"><title>근현대 예상시험지 답지</title>",
         f"<style>{PDF_CSS}</style></head><body>",
         "<h1>근현대 공간디자인 예상 시험지 답지</h1>",
         f'<p class="sub">번호는 시험지와 같다. 모범답안은 슬라이드에 나온 말로 적었고, 근거에 덱(강)과 쪽을 달았다.</p>',
         '<div class="box"><p>논술은 서론 한 줄, 핵심 서너 개, 대표 사례, 결론 한 줄의 뼈대로 쓴다. 채점 키워드가 답안에 들어갔는지 확인한다.</p>'
         "<p>초기작과 후기작 논술은 시기, 시기별 작품과 연도, 시기별 특징, 변화와 그 이유 순서로 쓴다.</p></div>"]
    for s, name in QD.SECTIONS:
        items = sec[s]
        for i, q in enumerate(items):
            body = f'<div class="q">{qhead(q)}{question_body(q, "key")}<div class="a">{answer_html(q, "key")}</div></div>'
            if i == 0:
                body = f'<div class="blk"><h2>{esc(name)} ({len(items)}문항)</h2>{body}</div>'
            h.append(body)
    h.append("</body></html>")
    return "\n".join(h)


def check(text, name):
    bad = {hex(ord(c)): text.count(c) for c in BAD if c in text}
    if bad:
        raise SystemExit(f"{name}: 금지 문자 {bad}")


def print_pdf(html_text, out, tmp, name):
    src = tmp / f"{name}.html"   # 임시 폴더와 파일 이름은 영어만 (Chrome 에 한글 경로를 넘기지 않는다)
    src.write_text(html_text, encoding="utf-8")
    pdf = src.with_suffix(".pdf")
    exe = next((c for c in CHROME if c.exists()), None)
    if not exe:
        raise SystemExit("Chrome 이 없어요")
    prof = tmp / "profile"
    cmd = [str(exe), "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check", "--disable-extensions",
           f"--user-data-dir={prof}", "--no-pdf-header-footer", "--virtual-time-budget=15000", f"--print-to-pdf={pdf}", src.as_uri()]
    p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        p.wait(timeout=180)
    except subprocess.TimeoutExpired:
        p.kill()   # 이 실행에서 띄운 프로세스만 정리한다
        raise SystemExit("Chrome 이 PDF 를 다 못 찍었어요 (시간 초과)")
    if not pdf.exists():
        raise SystemExit("PDF 가 안 나왔어요")
    out.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(pdf, out)
    try:
        import fitz
        doc = fitz.open(str(out))
        n = doc.page_count
        txt = "".join(pg.get_text() for pg in doc)
        doc.close()
        check(txt, out.name)
    except ImportError:
        n = "?"
    print(f"PDF: {out} ({n}쪽, {out.stat().st_size / 1e6:.1f} MB)")


def main():
    build_site_page()
    if "--no-pdf" in sys.argv:
        return
    paper, key = paper_html(), key_html()
    check(paper, "시험지 html")
    check(key, "답지 html")
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="msd_upd1018_"))
    try:
        print_pdf(paper, PDF_PAPER, tmp, "paper")
        print_pdf(key, PDF_KEY, tmp, "key")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
