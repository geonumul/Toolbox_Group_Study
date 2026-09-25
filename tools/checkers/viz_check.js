/* 움직이는 개념 그림(viz) 묶음 단위 시험 (jsdom). 설명은 engine/viz/README.md
   사용
     node tools/checkers/viz_check.js              engine/viz 의 모든 묶음
     node tools/checkers/viz_check.js sig nlp      고른 묶음만
   보는 것
     - 등록된 그림을 모두 붙이고 상태를 끝까지 넘긴 뒤 거꾸로 돌아오며 SVG 가 같은지
       (draw(ctx, s, k) 가 s, k, ctx.p 만 보고 그리는지. 앞 상태에서 쓴 값이 남아 있으면 여기서 잡힌다)
     - 조절값(range, choice)을 바꿔도 오류가 없고, 상태 수가 조절값에 따라 달라지지 않는지
     - SVG 안에 id 속성이 없는지, 금지 문자(em dash, en dash, 가운뎃점)가 없는지
   못 보는 것
     jsdom 은 글자 크기를 재지 않는다(getBBox 가 0). 글자가 겹치거나 viewBox 를 벗어나는 것은
     진짜 브라우저로 봐야 한다. */
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '..', '..');
const VIZ = path.join(ROOT, 'engine', 'viz');
const { createRequire } = require('module');
const { JSDOM } = createRequire(path.join(ROOT, 'package.json'))('jsdom');

const packs = process.argv.slice(2).length
  ? process.argv.slice(2).map(x => x.replace(/\.js$/, ''))
  : fs.readdirSync(VIZ).filter(f => f.endsWith('.js') && f !== 'viz.js').map(f => f.slice(0, -3)).sort();
if (!packs.length) { console.log('engine/viz 에 묶음 파일이 없어요.'); process.exit(1); }

const dom = new JSDOM('<!doctype html><html><body></body></html>', { runScripts: 'dangerously', pretendToBeVisual: true, url: 'https://example.test/' });
const w = dom.window, d = w.document;
const errs = [];
w.addEventListener('error', e => errs.push('window error: ' + e.message));
w.eval(fs.readFileSync(path.join(VIZ, 'viz.js'), 'utf8'));
const V = w.SDTViz;
V.instant = true; V.freeze = true;

const BAD = { '—': 'em dash', '–': 'en dash', '·': '가운뎃점' };
packs.forEach(p => {
  const f = path.join(VIZ, p + '.js');
  if (!fs.existsSync(f)) { errs.push('engine/viz/' + p + '.js 가 없어요'); return; }
  const src = fs.readFileSync(f, 'utf8');
  Object.keys(BAD).forEach(ch => { if (src.indexOf(ch) >= 0) errs.push(p + '.js: 금지 문자 ' + BAD[ch]); });
  w.eval(src);
});

const names = V.names().filter(n => packs.indexOf(n.split('.')[0]) >= 0);
if (!names.length) { console.log('등록된 그림이 없어요:', packs.join(', ')); process.exit(1); }

names.forEach(name => {
  const def = V.get(name);
  const host = d.createElement('div');
  d.body.appendChild(host);
  let r;
  try { r = V.frame({ kind: 'viz', viz: name, head: '시험' }, {}); } catch (e) { errs.push(name + ': frame 오류 ' + e.message); return; }
  host.innerHTML = r.html;
  try { r.after(host); } catch (e) { errs.push(name + ': build 오류 ' + e.message); return; }
  const root = host.querySelector('.vz');
  const inst = root && root._viz;
  if (!inst) { errs.push(name + ': 붙지 않음'); return; }
  const svg = root.querySelector('svg.vz-svg');
  const snaps = [];
  for (let s = 0; s <= r.steps; s++) {
    try { inst.onStep(s); inst.finish(); } catch (e) { errs.push(name + ' 상태 ' + s + ': draw 오류 ' + e.message); return; }
    snaps[s] = inst.snapshot();
  }
  for (let s = r.steps; s >= 0; s--) {
    try { inst.onStep(s); inst.finish(); } catch (e) { errs.push(name + ' 상태 ' + s + '(되돌리기): draw 오류 ' + e.message); return; }
    if (inst.snapshot() !== snaps[s]) errs.push(name + ': 상태 ' + s + ' 로 되돌아갔을 때 모습이 달라요');
  }
  if (svg.querySelector('[id]')) errs.push(name + ': SVG 안에 id 속성이 있어요');
  const raw = snaps.join('');
  Object.keys(BAD).forEach(ch => { if (raw.indexOf(ch) >= 0) errs.push(name + ': 그림 글자에 금지 문자 ' + BAD[ch]); });
  if (/NaN|undefined/.test(raw)) errs.push(name + ': 그림에 NaN 이나 undefined 가 들어갔어요');
  (def.controls || []).forEach(c => {
    const vals = c.type === 'choice' ? c.options.map(o => o[0])
      : [c.min, c.max, Math.round(((+c.min + +c.max) / 2) / (c.step || 1)) * (c.step || 1)];
    vals.forEach(v => {
      for (let s = 0; s <= r.steps; s++) {
        try { inst.onStep(s); inst.set(c.key, v); inst.finish(); } catch (e) { errs.push(name + ' 조절값 ' + c.key + '=' + v + ' 상태 ' + s + ': ' + e.message); return; }
      }
      const base = Object.assign({}, def.params); base[c.key] = v;
      const st = typeof def.states === 'function' ? def.states(base) : def.states;
      if (st.length !== r.steps + 1) errs.push(name + ': 조절값 ' + c.key + '=' + v + ' 일 때 상태 수가 ' + st.length + ' (원래 ' + (r.steps + 1) + ')');
    });
    inst.set(c.key, (def.params || {})[c.key]);
  });
  const caps = Array.from(root.querySelectorAll('.vz-cap')).map(x => x.textContent.trim());
  const empty = caps.filter(x => !x).length;
  console.log('  ' + name + ': 상태 ' + (r.steps + 1) + ', 조절 ' + (def.controls || []).length + (empty ? ', 빈 캡션 ' + empty : ''));
});

if (errs.length) { console.log('\nerrors:'); errs.forEach(e => console.log('  - ' + e)); process.exit(1); }
console.log('\nviz errors: 없음 (' + names.length + '개, 묶음 ' + packs.join(', ') + ')');
