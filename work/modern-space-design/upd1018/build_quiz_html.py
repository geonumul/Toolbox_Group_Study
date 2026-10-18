# -*- coding: utf-8 -*-
"""근현대 예상시험지, 바로 채점하는 HTML 하나 (questions.py 에서 만든다).

사용: python work/modern-space-design/upd1018/build_quiz_html.py
출력: 02_작업/근현대공간디자인/근현대_예상시험지_채점.html  (그림까지 파일 안에 넣어 어디서든 열린다)

왜 (2026-10-18 사용자): "html 로 주라. 정답 바로바로 볼 수 있게 채점 같은 거 되도록."
- 객관식: 누르면 바로 ○ / ✕ 와 해설.
- 단답: 쓰고 확인을 누르면 정답이 나오고, 맞았는지 스스로 고른다 (쓴 말이 정답에 들어 있으면 미리 표시).
- 약술, 논술: 쓰고 답 보기를 누르면 모범 답안과 채점 키워드 체크칸이 나온다. 쓴 글에 들어 있는 키워드는 미리 체크된다.
- 위의 점수판에 구역별 결과, 실전 20문항만 보기, 틀린 것만 보기, 처음부터 다시. 푼 기록은 이 브라우저에만 남는다.
모양은 흑백 노트 꼴 (사용자: 알록달록 금지).
"""
import html, json, pathlib, re, sys

sys.stdout.reconfigure(encoding="utf-8")
sys.dont_write_bytecode = True
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build as B          # noqa: E402  (QS 번호 매기기, 그림 자르기, 답 HTML 을 같이 쓴다)
import questions as QD     # noqa: E402

OUT = B.PDF_DIR / "근현대_예상시험지_채점.html"
SHARE = B.REPO / "share" / "msd-mock-1018.html"


def strip(s):
    return html.unescape(re.sub(r"<[^>]+>", "", str(s)))


def item(q):
    k = q["kind"]
    d = {"no": q["no"], "kind": k, "sec": QD.KIND_SEC[k], "label": QD.KIND_LABEL[k], "unit": B.unit_label(q),
         "q": B.question_body(q, "key"), "ans": B.answer_html(q, "key")}
    if k == "mcq":
        d["choices"] = q["choices"]
        d["a"] = q["ans"]
    if k == "pic":
        deck, p, box = q["img"]
        d["fig"] = B.crop_b64(deck, p, box, width=900, quality=80)
    if k == "short":
        d["plain"] = strip(q["ans"])
    if k == "list":
        d["keys"] = [it[0] for _, items in q["groups"] for it in items]
        d["must"] = [it[0] for _, items in q["groups"] for it in items if it[3]]
    elif q.get("keys"):
        d["keys"] = [strip(x) for x in q["keys"]]
    return d


CSS = """
:root{--ink:#16171b;--ink2:#3d3f46;--sub:#6b6d75;--line:#d9dade;--soft:#f3f3f5;--bg:#fff}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--ink:#ececef;--ink2:#c9cad0;--sub:#9a9ca4;--line:#3a3b41;--soft:#202126;--bg:#141518}}
:root[data-theme="dark"]{--ink:#ececef;--ink2:#c9cad0;--sub:#9a9ca4;--line:#3a3b41;--soft:#202126;--bg:#141518}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.65 "Pretendard","Malgun Gothic","Apple SD Gothic Neo",sans-serif}
main{max-width:820px;margin:0 auto;padding:0 16px 80px}
h1{font-size:24px;margin:22px 0 4px}
h2{font-size:19px;margin:34px 0 10px;padding-bottom:6px;border-bottom:1.5px solid var(--ink)}
.sub{color:var(--sub);font-size:14px}
.info{border:1px solid var(--line);padding:10px 14px;margin:12px 0;font-size:14.5px}
.info p{margin:4px 0}
.bar{position:sticky;top:0;z-index:5;background:var(--bg);border-bottom:1px solid var(--line);padding:8px 0;margin:0 -16px;padding-left:16px;padding-right:16px}
.score{display:flex;flex-wrap:wrap;gap:6px 16px;font-size:14px}
.score b{font-weight:700}
.ctl{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px}
button{font:inherit;font-size:14px;border:1px solid var(--ink2);background:var(--bg);color:var(--ink);padding:5px 12px;border-radius:4px;cursor:pointer}
button.on{background:var(--ink);color:var(--bg)}
button:disabled{opacity:.45;cursor:default}
.q{border-top:1px solid var(--line);padding:16px 0}
.qh{font-size:13.5px;color:var(--sub);margin-bottom:4px}
.qh b{color:var(--ink);font-size:16px;margin-right:6px}
.qh .mark{font-weight:700;color:var(--ink);margin-left:8px;font-size:15px}
.qq{margin:2px 0 8px}
.fig img,.ans img{max-width:100%;height:auto;border:1px solid var(--line);display:block;margin:6px 0}
.ch{display:flex;flex-direction:column;gap:6px;margin:8px 0}
.ch button{text-align:left;border-color:var(--line);padding:8px 12px;font-size:15px;line-height:1.5}
.ch button.pick{border:2px solid var(--ink)}
.ch button.right{border:2px solid var(--ink);font-weight:700}
.ch button.right::after{content:"  ○ 정답"}
.ch button.pick.wrong::after{content:"  ✕ 내 답"}
textarea,input[type=text]{width:100%;font:inherit;font-size:15px;border:1px solid var(--line);background:var(--bg);color:var(--ink);padding:8px;border-radius:4px}
textarea{min-height:90px;resize:vertical}
.row{display:flex;gap:6px;flex-wrap:wrap;margin:8px 0;align-items:center}
.ans{background:var(--soft);border-left:3px solid var(--ink);padding:10px 14px;margin-top:10px;font-size:15px}
.ans p,.ans li{margin:3px 0}
.ans .k{color:var(--ink2)}
.ans .src,.ans .nt{color:var(--sub);font-size:13.5px}
.chk{margin-top:10px;border-top:1px dashed var(--line);padding-top:8px}
.chk label{display:inline-flex;align-items:center;gap:4px;margin:3px 10px 3px 0;font-size:14.5px}
.chk .must{font-weight:700}
.pct{font-weight:700}
.hint{color:var(--sub);font-size:13.5px}
.hide{display:none}
@media print{.bar,.ctl,button{display:none}}
"""

JS = r"""
const D = window.QDATA, PICK = new Set(window.PICK20);
const KEY = 'msd_upd1018_v1';
let S = {}; try { S = JSON.parse(localStorage.getItem(KEY) || '{}') || {}; } catch (e) { S = {}; }
const save = () => { try { localStorage.setItem(KEY, JSON.stringify(S)); } catch (e) {} };
const st = no => (S[no] = S[no] || {});
const norm = s => String(s || '').toLowerCase().replace(/<[^>]+>/g, '').replace(/[^0-9a-zㄱ-ㆎ가-힣]/g, '');
const $ = (s, el) => (el || document).querySelector(s), $$ = (s, el) => Array.from((el || document).querySelectorAll(s));
const SECN = {mcq: 'Ⅰ. 객관식', short: 'Ⅱ. 단답형', brief: 'Ⅲ. 약술형', essay: 'Ⅳ. 논술형'};
let view = 'all';

function render() {
  const m = $('#qs'); let h = '', last = '';
  D.forEach(q => {
    if (q.sec !== last) { h += '<h2 data-sec="' + q.sec + '">' + SECN[q.sec] + '</h2>'; last = q.sec; }
    h += '<div class="q" id="q' + q.no + '" data-no="' + q.no + '"><div class="qh"><b>' + q.no + '.</b>' + q.label + ', ' + q.unit
      + (PICK.has(q.no) ? ', 실전20' : '') + '<span class="mark"></span></div><div class="qq">' + q.q + '</div>';
    if (q.fig) h += '<div class="fig"><img alt="문제 그림" src="' + q.fig + '"></div>';
    if (q.kind === 'mcq') {
      h += '<div class="ch">' + q.choices.map((c, i) => '<button type="button" data-i="' + (i + 1) + '">' + '①②③④⑤⑥'[i] + ' ' + c + '</button>').join('') + '</div>';
    } else if (q.kind === 'short') {
      h += '<div class="row"><input type="text" placeholder="답을 쓰고 확인을 누른다"><button type="button" class="go">확인</button></div>';
    } else {
      h += '<textarea placeholder="답을 써 보고 답 보기를 누른다 (안 써도 된다)"></textarea><div class="row"><button type="button" class="go">답 보기</button></div>';
    }
    h += '<div class="ans hide">' + q.ans + '</div><div class="grade hide"></div></div>';
  });
  m.innerHTML = h;
  D.forEach(q => wire(q));
  apply();
}

function wire(q) {
  const el = $('#q' + q.no), s = st(q.no);
  if (q.kind === 'mcq') {
    $$('.ch button', el).forEach(b => b.addEventListener('click', () => { if (s.pick) return; s.pick = +b.dataset.i; save(); showMcq(q); tally(); apply(); }));
    if (s.pick) showMcq(q);
  } else if (q.kind === 'short') {
    const inp = $('input', el); inp.value = s.text || '';
    inp.addEventListener('input', () => { s.text = inp.value; save(); });
    inp.addEventListener('keydown', e => { if (e.key === 'Enter') $('.go', el).click(); });
    $('.go', el).addEventListener('click', () => { s.open = 1; s.text = inp.value; save(); showShort(q); });
    if (s.open) showShort(q);
  } else {
    const ta = $('textarea', el); ta.value = s.text || '';
    ta.addEventListener('input', () => { s.text = ta.value; save(); });
    $('.go', el).addEventListener('click', () => { s.open = 1; s.text = ta.value; save(); showLong(q); });
    if (s.open) showLong(q);
  }
}

function showMcq(q) {
  const el = $('#q' + q.no), s = st(q.no);
  $$('.ch button', el).forEach(b => { const i = +b.dataset.i; b.disabled = true;
    if (i === q.a) b.classList.add('right'); if (i === s.pick) b.classList.add('pick'); if (i === s.pick && i !== q.a) b.classList.add('wrong'); });
  $('.mark', el).textContent = s.pick === q.a ? '○' : '✕';
  $('.ans', el).classList.remove('hide');
}

function selfBtns(q, el, opts) {
  const s = st(q.no), g = $('.grade', el);
  g.classList.remove('hide');
  g.innerHTML = '<div class="row">' + opts.map(o => '<button type="button" data-v="' + o[0] + '"' + (s.self === o[0] ? ' class="on"' : '') + '>' + o[1] + '</button>').join('') + '</div>';
  $$('button', g).forEach(b => b.addEventListener('click', () => { s.self = +b.dataset.v; save(); $$('button', g).forEach(x => x.classList.toggle('on', x === b)); markSelf(q); tally(); apply(); }));
}

function markSelf(q) {
  const el = $('#q' + q.no), s = st(q.no);
  const t = {2: '○', 1: '△', 0: '✕'}[s.self];
  $('.mark', el).textContent = t == null ? '' : t;
}

function showShort(q) {
  const el = $('#q' + q.no), s = st(q.no), a = $('.ans', el);
  a.classList.remove('hide');
  const t = norm(s.text), p = norm(q.plain);
  const hit = t.length >= 2 && (p.includes(t) || t.includes(p));
  let hint = $('.hint', a); if (!hint) { hint = document.createElement('p'); hint.className = 'hint'; a.prepend(hint); }
  hint.textContent = !s.text ? '쓴 답이 없다. 정답을 보고 맞았는지 고른다.' : hit ? '쓴 말이 정답에 들어 있다. 맞음으로 보인다.' : '쓴 말이 정답과 글자로 같지 않다. 뜻이 맞으면 맞음을 고른다.';
  if (hit && s.self == null) s.self = 2;
  selfBtns(q, el, [[2, '○ 맞음'], [0, '✕ 틀림']]);
  markSelf(q); tally();
}

function showLong(q) {
  const el = $('#q' + q.no), s = st(q.no), a = $('.ans', el);
  a.classList.remove('hide');
  if (q.keys && q.keys.length && !$('.chk', a)) {
    const t = norm(s.text), must = new Set(q.must || []);
    s.kk = s.kk || q.keys.map(k => { const n = norm(k).slice(0, 12); return !!(t && n.length >= 2 && t.includes(n)); });
    const box = document.createElement('div'); box.className = 'chk';
    box.innerHTML = '<p><b>' + (q.kind === 'list' ? '쓴 작품에 체크' : '내 답에 들어간 키워드에 체크') + '</b> <span class="pct"></span>'
      + (s.text ? ' <span class="hint">(쓴 글에 있는 것은 미리 체크했다)</span>' : '') + '</p>'
      + q.keys.map((k, i) => '<label' + (must.has(k) ? ' class="must"' : '') + '><input type="checkbox" data-i="' + i + '"' + (s.kk[i] ? ' checked' : '') + '>' + k + (must.has(k) ? ' (꼭)' : '') + '</label>').join('');
    a.appendChild(box);
    $$('input', box).forEach(c => c.addEventListener('change', () => { s.kk[+c.dataset.i] = c.checked; save(); pct(q); tally(); }));
    pct(q);
  }
  selfBtns(q, el, [[2, '○ 잘 썼다'], [1, '△ 일부'], [0, '✕ 못 썼다']]);
  markSelf(q); save(); tally();
}

function pct(q) {
  const el = $('#q' + q.no), s = st(q.no), sp = $('.pct', el);
  if (!sp || !s.kk) return;
  const n = s.kk.filter(Boolean).length; sp.textContent = n + ' / ' + s.kk.length + ' (' + Math.round(100 * n / s.kk.length) + '%)';
}

function done(q) { const s = S[q.no] || {}; return q.kind === 'mcq' ? !!s.pick : s.self != null; }
function wrong(q) { const s = S[q.no] || {}; return q.kind === 'mcq' ? (s.pick && s.pick !== q.a) : (s.self != null && s.self < 2); }

function tally() {
  const sec = {mcq: [0, 0, 0], short: [0, 0, 0], brief: [0, 0, 0], essay: [0, 0, 0]};   // 맞음 점수, 푼 수, 전체
  D.forEach(q => { if (view === 'pick' && !PICK.has(q.no)) return;
    const s = S[q.no] || {}, r = sec[q.sec]; r[2]++;
    if (!done(q)) return; r[1]++;
    r[0] += q.kind === 'mcq' ? (s.pick === q.a ? 1 : 0) : (s.self === 2 ? 1 : s.self === 1 ? 0.5 : 0); });
  const f = (k, n) => { const r = sec[k]; return '<span>' + n + ' <b>' + (Math.round(r[0] * 10) / 10) + '</b> / ' + r[1] + ' 푼 것 (전체 ' + r[2] + ')</span>'; };
  const tot = Object.values(sec).reduce((a, r) => [a[0] + r[0], a[1] + r[1], a[2] + r[2]], [0, 0, 0]);
  $('#score').innerHTML = f('mcq', '객관식') + f('short', '단답') + f('brief', '약술') + f('essay', '논술')
    + '<span>전체 <b>' + (tot[1] ? Math.round(100 * tot[0] / tot[1]) : 0) + '%</b> (' + tot[1] + ' / ' + tot[2] + ' 품)</span>';
}

function apply() {
  D.forEach(q => { const el = $('#q' + q.no);
    const show = view === 'all' || (view === 'pick' && PICK.has(q.no)) || (view === 'wrong' && wrong(q)) || (view === 'todo' && !done(q));
    el.classList.toggle('hide', !show); });
  $$('h2[data-sec]').forEach(h => { const any = D.some(q => q.sec === h.dataset.sec && !$('#q' + q.no).classList.contains('hide')); h.classList.toggle('hide', !any); });
  $$('.ctl button[data-v]').forEach(b => b.classList.toggle('on', b.dataset.v === view));
  tally();
}

document.addEventListener('DOMContentLoaded', () => {
  render();
  $$('.ctl button[data-v]').forEach(b => b.addEventListener('click', () => { view = b.dataset.v; apply(); window.scrollTo(0, $('#qs').offsetTop - 80); }));
  $('#reset').addEventListener('click', () => { if (confirm('푼 기록을 모두 지우고 처음부터 다시 할까?')) { S = {}; save(); render(); } });
});
"""


def main():
    data = [item(q) for q in B.QS]
    pick = [q["no"] for q in B.pick20()]
    info = QD.INFO
    head = ("<h1>근현대공간디자인 예상시험지 (채점용)</h1>"
            f'<p class="sub">문제 {len(data)}개. 실제 시험은 약 20문제 (논술 6) 이고, 이건 연습용 전체판이다. 실전 비율 20문항은 "실전 20" 으로 볼 수 있다.</p>'
            '<div class="info"><p><b>선배 후기 (2024년 2학기 중간)</b></p>'
            + "".join(f"<p><b>{html.escape(k)}</b> {html.escape(v)}</p>" for k, v in info["format"])
            + "".join(f"<p>- {s}</p>" for s in info["strategy"][:3]) + "</div>"
            '<p class="sub">쓰는 법: 객관식은 누르면 바로 채점. 단답은 쓰고 확인, 약술과 논술은 쓰고 답 보기를 누른 뒤 키워드에 체크하고 ○ △ ✕ 를 고른다. '
            "기록은 이 브라우저에만 남는다.</p>")
    bar = ('<div class="bar"><div class="score" id="score"></div><div class="ctl">'
           '<button type="button" data-v="all">전체</button><button type="button" data-v="pick">실전 20</button>'
           '<button type="button" data-v="todo">안 푼 것</button><button type="button" data-v="wrong">틀린 것</button>'
           '<button type="button" id="reset">처음부터</button></div></div>')
    doc = ("<!doctype html><html lang=\"ko\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
           "<title>근현대 예상시험지 채점</title><style>" + CSS + "</style></head><body><main>" + head + bar + '<div id="qs"></div></main>'
           "<script>window.QDATA=" + json.dumps(data, ensure_ascii=False) + ";window.PICK20=" + json.dumps(pick) + ";</script>"
           "<script>" + JS + "</script></body></html>")
    bad = [c for c in B.BAD if c in doc]
    if bad:
        raise SystemExit("금지 문자: %r" % bad)
    OUT.write_text(doc, encoding="utf-8")
    # 카톡 안에서 링크로 열리게 사이트 저장소에도 둔다 (2026-10-18 사용자: "모바일에서 안 열려, 카톡 내부에서 열릴 수 있게")
    # https://geonumul.github.io/Toolbox_Group_Study/share/msd-mock-1018.html  (로그인 없이 열린다)
    SHARE.parent.mkdir(exist_ok=True)
    SHARE.write_text(doc, encoding="utf-8")
    print(f"{OUT}  {len(data)}문항, 실전 20 = {pick}, {OUT.stat().st_size / 1e6:.1f} MB")
    print(f"{SHARE}")


if __name__ == "__main__":
    main()
