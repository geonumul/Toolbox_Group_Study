// 시험 대비 한 문제를 열어 그림(figure) 장면이 제대로 그려지는지 본다.
//   node tools/checkers/fig_test.js <사이트 폴더> <문제 id>
const { JSDOM } = require('jsdom'); const fs = require('fs'); const path = require('path');
const ROOT = process.argv[2], ID = process.argv[3] || 'q9';
let html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8')
  .replace(/<script src="https?:[^"]+"[^>]*><\/script>/g, '').replace(/<link [^>]*>/g, '')
  .replace(/<script src="([^"?]+)(\?[^"]*)?" defer><\/script>/g, (m, src) => '<script>' + fs.readFileSync(path.join(ROOT, src), 'utf8').replace(/<\/script>/g, '<\/script>') + '</script>');
const dom = new JSDOM(html, { runScripts: 'dangerously', pretendToBeVisual: true, url: 'https://example.test/' });
const w = dom.window, d = w.document; w.scrollTo = () => {}; w.scrollBy = () => {}; w.HTMLElement.prototype.scrollIntoView = () => {};
const errs = []; w.addEventListener('error', e => errs.push(e.message));
const origAppend = d.head.appendChild.bind(d.head);
d.head.appendChild = el => { if (el.tagName === 'SCRIPT' && el.src) { const rel = el.src.replace('https://example.test/','').split('?')[0]; const p = path.join(ROOT, rel); setTimeout(() => { if (fs.existsSync(p)) { try { w.eval(fs.readFileSync(p,'utf8')); el.onload && el.onload(); } catch(e){ errs.push('eval '+rel+': '+e.message); el.onerror && el.onerror(); } } else el.onerror && el.onerror(); }, 0); return el; } return origAppend(el); };
const $ = s => d.querySelector(s), $$ = s => [...d.querySelectorAll(s)];
const wait = ms => new Promise(r => setTimeout(r, ms));
const key = k => d.dispatchEvent(new w.KeyboardEvent('keydown', { key: k, bubbles: true, cancelable: true }));
(async () => {
  await wait(80); w.location.hash = '#/exam/' + ID; await wait(400);
  const bad = [];
  let figs = 0, tbls = 0;
  for (let i = 0; i < 40; i++) {
    const head = ($('#pslide .sh, #pslide h2, #pslide .sk') || {}).textContent || '';
    const svg = $('#pslide svg');
    if (svg) {
      figs++;
      const shapes = $$('#pslide svg circle, #pslide svg line, #pslide svg text, #pslide svg polygon').length;
      const builds = $$('#pslide svg .bld').length;
      const hidden0 = $$('#pslide svg .bld.hide').length;
      console.log('장면 ' + (i+1) + ' 그림: 도형 ' + shapes + '개, 단계칸 ' + builds + '개, 처음 숨은 것 ' + hidden0);
      if (!shapes) bad.push('그림에 도형이 없음');
      if (builds && !hidden0) bad.push('단계가 있는데 처음부터 다 보임');
      // 그 그림의 단계 수만큼만 넘긴다 (더 누르면 다음 장면으로 가 버린다)
      const steps = Math.max(...$$('#pslide svg .bld').map(e => +e.getAttribute('data-s') || 0), 0);
      for (let k2 = 0; k2 < steps; k2++) { key('ArrowRight'); await wait(15); }
      const left = $$('#pslide svg .bld.hide').length;
      console.log('   ' + steps + '번 넘긴 뒤 숨은 것: ' + left);
      if (left) bad.push('단계를 다 넘겨도 안 보이는 칸이 ' + left + '개');
      key('ArrowRight'); await wait(60);   // 다음 장면으로
      continue;
    }
    if ($('#pslide .stbl table')) { tbls++; console.log('장면 ' + (i+1) + ' 표: 줄 ' + $$('#pslide .stbl tbody tr').length + '개'); }
    key('ArrowRight'); await wait(60);
  }
  console.log('\n그림 ' + figs + '개, 표 ' + tbls + '개');
  if (!figs) bad.push('그림 장면을 하나도 못 찾음');
  console.log('오류: ' + (errs.length ? errs.join(' | ') : '없음'));
  console.log('틀린 곳: ' + (bad.length ? '\n  - ' + bad.join('\n  - ') : '없음'));
  process.exit(bad.length || errs.length ? 1 : 0);
})();
