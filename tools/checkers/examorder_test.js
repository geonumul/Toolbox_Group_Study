// 시험 대비 목록이 "배우고 -> 그 모델 연습 카드" 차례로 나오는지 본다.
const { JSDOM } = require('jsdom'); const fs = require('fs'); const path = require('path');
const ROOT = process.argv[2];
let html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8')
  .replace(/<script src="https?:[^"]+"[^>]*><\/script>/g, '').replace(/<link [^>]*>/g, '')
  .replace(/<script src="([^"?]+)(\?[^"]*)?" defer><\/script>/g, (m, src) => '<script>' + fs.readFileSync(path.join(ROOT, src), 'utf8').replace(/<\/script>/g, '<\/script>') + '</script>');
const dom = new JSDOM(html, { runScripts: 'dangerously', pretendToBeVisual: true, url: 'https://example.test/' });
const w = dom.window, d = w.document; w.scrollTo = () => {}; w.scrollBy = () => {}; w.HTMLElement.prototype.scrollIntoView = () => {};
const errs = []; w.addEventListener('error', e => errs.push(e.message));
const origAppend = d.head.appendChild.bind(d.head);
d.head.appendChild = el => { if (el.tagName === 'SCRIPT' && el.src) { const rel = el.src.replace('https://example.test/','').split('?')[0]; const p = path.join(ROOT, rel); setTimeout(() => { if (fs.existsSync(p)) { try { w.eval(fs.readFileSync(p,'utf8')); el.onload && el.onload(); } catch(e){ errs.push('eval '+rel+': '+e.message); el.onerror && el.onerror(); } } else el.onerror && el.onerror(); }, 0); return el; } return origAppend(el); };
const $$ = s => [...d.querySelectorAll(s)];
const wait = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  await wait(80); w.location.hash = '#/exam'; await wait(400);
  const secs = $$('.dsec').map(e => e.textContent.trim());
  console.log('칸 차례:'); secs.forEach((s, i) => console.log('  ' + (i+1) + '. ' + s));
  const cards = $$('.dcard').length, folds = $$('.dfold').length;
  console.log('카드 ' + cards + '개, 접힌 묶음 ' + folds + '개');
  const chips = $$('.pillrow .chip').map(c => c.textContent.trim());
  console.log('칩: ' + chips.join(' | '));
  const bad = [], bad0 = [];
  const di = secs.findIndex(s => /^연습 카드/.test(s));
  const pi = secs.findIndex(s => /^1단계/.test(s));
  const ni = secs.findIndex(s => /^2단계/.test(s));
  const ri = secs.findIndex(s => /^마지막/.test(s));
  if (ri >= 0 && di >= 0 && !(di < ri)) bad.push('기출 원본은 연습 카드 뒤여야 함');
  if (pi < 0) bad.push('기출에 나온 모델 칸이 없음');
  if (di < 0) bad.push('연습 카드 칸이 없음');
  if (pi >= 0 && ni >= 0 && !(pi < ni)) bad.push('기출에 나온 모델이 새 모델보다 앞이어야 함');
  if (pi >= 0 && di >= 0 && !(pi < di)) bad.push('연습 카드는 모델 칸 뒤여야 함 (모델 ' + pi + ', 카드 ' + di + ')');
  if (!cards) bad.push('카드가 하나도 안 그려짐');
  console.log('\n오류: ' + (errs.length ? errs.join(' | ') : '없음'));
  console.log('틀린 곳: ' + (bad.length ? '\n  - ' + bad.join('\n  - ') : '없음'));
  process.exit(bad.length || errs.length ? 1 : 0);
})();
