// 가리고 설명하기: 가린 칸이 순서대로 하나씩 열리는지 본다.
//   node tools/checkers/recall_test.js <사이트 폴더> [덱] [단계]
// 검사끼리 얽히지 않게 하나 볼 때마다 쪽을 새로 연다.
const { JSDOM } = require('jsdom'); const fs = require('fs'); const path = require('path');
const ROOT = process.argv[2];
const DECK = process.argv[3] || 'O2';
const STAGE = process.argv[4] || '1';
let html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8')
  .replace(/<script src="https?:[^"]+"[^>]*><\/script>/g, '')
  .replace(/<link [^>]*>/g, '')
  .replace(/<script src="([^"?]+)(\?[^"]*)?" defer><\/script>/g, (m, src) => '<script>' + fs.readFileSync(path.join(ROOT, src), 'utf8').replace(/<\/script>/g, '<\\/script>') + '</script>');
const dom = new JSDOM(html, { runScripts: 'dangerously', pretendToBeVisual: true, url: 'https://example.test/' });
const w = dom.window, d = w.document;
w.scrollTo = () => {}; w.scrollBy = () => {}; w.HTMLElement.prototype.scrollIntoView = () => {};
const errs = []; w.addEventListener('error', e => errs.push(e.message));
const origAppend = d.head.appendChild.bind(d.head);
d.head.appendChild = el => {
  if (el.tagName === 'SCRIPT' && el.src) {
    const rel = el.src.replace('https://example.test/', '').split('?')[0];
    const p = path.join(ROOT, rel);
    setTimeout(() => { if (fs.existsSync(p)) { try { w.eval(fs.readFileSync(p, 'utf8')); el.onload && el.onload(); } catch (e) { errs.push('eval ' + rel + ': ' + e.message); el.onerror && el.onerror(); } } else { el.onerror && el.onerror(); } }, 0);
    return el;
  }
  return origAppend(el);
};
const $ = s => d.querySelector(s), $$ = s => [...d.querySelectorAll(s)];
const wait = ms => new Promise(r => setTimeout(r, ms));
const open = () => $$('.rcm.open').length;
const key = k => d.dispatchEvent(new w.KeyboardEvent('keydown', { key: k, bubbles: true, cancelable: true }));
const click = (el, extra) => el.dispatchEvent(new w.MouseEvent('click', Object.assign({ bubbles: true, cancelable: true }, extra || {})));
const bad = [];
const check = (name, got, want) => {
  const ok = got === want;
  console.log('  ' + (ok ? 'OK  ' : '틀림 ') + name + ': ' + got + (ok ? '' : ' (바람 ' + want + ')'));
  if (!ok) bad.push(name + ' ' + got + ' != ' + want);
};
// 가린 칸이 있는 쪽을 새로 연다 (첫 쪽은 표지라 칸이 없을 수 있다)
async function fresh() {
  w.location.hash = '#/';
  await wait(40);
  w.location.hash = '#/recall/' + DECK + '/' + STAGE;
  await wait(260);
  for (let t = 0; t < 12 && !$$('.rcm').length; t++) { key('ArrowRight'); await wait(50); }
  const st = $('#pstage');
  if (st) st.getBoundingClientRect = () => ({ left: 0, width: 1000, top: 0, height: 700, right: 1000, bottom: 700 });
  return $$('.rcm');
}

(async () => {
  await wait(80);
  let ms = await fresh();
  console.log(DECK + ' ' + STAGE + '단계: 가린 칸 ' + ms.length + '개');
  if (!ms.length) { console.log('가린 칸이 없어 더 못 봄'); process.exit(0); }

  console.log('\n[1] 오른쪽 키로 하나씩');
  check('처음 열린 수', open(), 0);
  for (let i = 1; i <= Math.min(3, ms.length); i++) { key('ArrowRight'); await wait(20); check(i + '번 누른 뒤', open(), i); }
  check('세는 칸 표시', +$('.rcopen').textContent, Math.min(3, ms.length));

  console.log('\n[2] 왼쪽 키로 되돌리기');
  const b4 = open(); key('ArrowLeft'); await wait(20); check('한 번 되돌린 뒤', open(), b4 - 1);

  console.log('\n[3] 열리는 차례가 위에서 아래로');
  const ys = $$('.rcm').map(b => parseFloat(b.style.top));
  check('어긋난 칸 수', ys.filter((v, i) => i > 0 && v < ys[i - 1] - 0.5).length, 0);

  console.log('\n[4] 화면 누르기 (오른쪽이면 다음, 왼쪽이면 앞)');
  ms = await fresh();
  click($('.rcimg img'), { clientX: 800, clientY: 300 }); await wait(20);
  check('오른쪽 누른 뒤', open(), 1);
  // 칸이 하나뿐인 쪽은 한 번 더 누르면 다음 쪽으로 넘어가는 게 맞다. 그런 쪽은 건너뛴다.
  if (ms.length >= 2) {
    click($('.rcimg img'), { clientX: 800, clientY: 300 }); await wait(20);
    check('한 번 더', open(), 2);
    click($('.rcimg img'), { clientX: 60, clientY: 300 }); await wait(20);
    check('왼쪽 누른 뒤', open(), 1);
  } else {
    console.log('  (칸이 하나뿐이라 건너뜀)');
  }

  console.log('\n[5] 칸을 직접 누르기');
  ms = await fresh();
  const j = Math.min(4, ms.length - 1);
  click($$('.rcm')[j]); await wait(20);
  check((j + 1) + '번째 칸(안 열림) 누른 뒤', open(), j + 1);
  click($$('.rcm')[j]); await wait(20);
  check('같은 칸(이미 열림) 다시 누른 뒤', open(), j);

  console.log('\n[6] 전부 보기 / 다시 가리기');
  ms = await fresh();
  const all = $('.rcall');
  if (all) {
    click(all); await wait(20);
    check('전부 보기', open(), ms.length);
    check('버튼 글이 바뀜', all.textContent, '다시 가리기');
    click(all); await wait(20);
    check('다시 가리기', open(), 0);
  }

  console.log('\n오류: ' + (errs.length ? errs.join(' | ') : '없음'));
  console.log('틀린 곳: ' + (bad.length ? bad.length + '개' : '없음'));
  process.exit(bad.length || errs.length ? 1 : 0);
})();
