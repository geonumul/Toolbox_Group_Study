// 홈페이지 jsdom 스모크 테스트: 라우트 전부 열고, 문제 풀이, 오답노트, 용어 카드, (있으면) 회독과 정리 슬라이드 넘기기
const { JSDOM } = require('jsdom'); const fs = require('fs'); const path = require('path');
const ROOT = process.argv[2] || path.resolve(__dirname, '..', '..', '..', 'Graph-Neural-Networks-Fall-2026');   // 03_사이트 안의 GNN 홈페이지 저장소
let html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8')
  .replace(/<script src="https?:[^"]+"[^>]*><\/script>/g, '')
  .replace(/<link [^>]*>/g, '')
  .replace(/<script src="([^"?]+)(\?[^"]*)?" defer><\/script>/g, (m, src) => '<script>' + fs.readFileSync(path.join(ROOT, src), 'utf8').replace(/<\/script>/g, '<\\/script>') + '</script>');
const dom = new JSDOM(html, { runScripts: 'dangerously', pretendToBeVisual: true, url: 'https://example.test/' });
const w = dom.window, d = w.document; w.scrollTo = () => {}; w.HTMLElement.prototype.scrollIntoView = () => {}; w.confirm = () => true;
const errs = []; w.addEventListener('error', e => errs.push(e.message));
// 동적 스크립트(lesson, notes)를 파일에서 읽어 실행
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
const go = async h => { w.location.hash = h; await wait(60); };
(async () => {
  await wait(50);
  console.log('home cards:', $$('.wcard').length, 'plan cells:', $$('.pcell').length, 'tools:', $$('.tool').length);
  const meta = w.GNN_META || w.SDT_META;   // GNN 저장소는 GNN_META, 과목 사이트는 SDT_META
  const weeks = (meta.weeks || []).map(x => String(x.id));
  for (const wk of weeks) { await go('#/week/' + wk); console.log('week', wk, 'ptiles', $$('.ptile').length, 'units', $$('.ucard').length, 'qbtns', $$('.qbtn').length); }
  const qweek = weeks.find(x => (meta.units || {})[x]) || weeks[0];   // 문제가 있는 주차 하나를 골라 풀어 본다
  await go('#/quiz?week=' + qweek + '&level=basic&mode=all&start=1&n=0');
  let types = {}, guard = 0;
  while (guard++ < 400) {
    const card = $('#qstage .card'); if (!card) { console.log('no card'); break; }
    if (card.classList.contains('result')) { console.log('RESULT', card.querySelector('.big').textContent, card.querySelector('p').textContent); break; }
    const tag = card.querySelector('.tag').textContent; types[tag] = (types[tag] || 0) + 1;
    if ($('#qstage .ch')) { $$('#qstage .ch')[guard % 2].click(); $('#nx').click(); }
    else if ($('#qstage .oxbtn')) { $$('#qstage .oxbtn')[guard % 2].click(); $('#nx').click(); }
    else if ($('#qstage .blank')) { $$('#qstage .blank input').forEach(i => i.value = '1'); $('#hint').click(); $('#chk').click(); $('#markOk').click(); $('#nx').click(); }
    else if ($('#qstage #ans') && $('#qstage #ans').tagName === 'INPUT') { $('#ans').value = 'x'; $('#chk').click(); $('#nx').click(); }
    else { $('#showKey').click(); $$('#qstage .kitem input').slice(0, 1).forEach(c => { c.checked = true; c.dispatchEvent(new w.Event('change', { bubbles: true })); }); $('#grade').click(); }
  }
  console.log('types', types, 'badge', $('#wrongBadge').textContent);
  // ---------- 용어 퀴즈: 주차별과 전 주차 ----------
  const TERM_UNIT = '%EC%9A%A9%EC%96%B4';
  const qtotal = () => { const m = (($('#setupStat') || {}).textContent || '').match(/출제 가능 (\d+)/); return m ? +m[1] : -1; };
  const qWeekLabel = () => { const sp = $('#qstage .qmeta span'); if (!sp) return ''; return [...sp.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join('').split(',')[0].trim(); };
  const answerOne = i => {   // 지금 화면의 문제 하나를 아무렇게나 풀고 다음으로
    const card = $('#qstage .card'); if (!card || card.classList.contains('result')) return false;
    if ($('#qstage .ch')) { $$('#qstage .ch')[i % 2].click(); $('#nx').click(); }
    else if ($('#qstage .oxbtn')) { $$('#qstage .oxbtn')[i % 2].click(); $('#nx').click(); }
    else if ($('#qstage .blank')) { $$('#qstage .blank input').forEach(x => x.value = '1'); $('#hint').click(); $('#chk').click(); $('#markOk').click(); $('#nx').click(); }
    else if ($('#qstage #ans') && $('#qstage #ans').tagName === 'INPUT') { $('#ans').value = 'x'; $('#chk').click(); $('#nx').click(); }
    else { $('#showKey').click(); $$('#qstage .kitem input').slice(0, 1).forEach(c => { c.checked = true; c.dispatchEvent(new w.Event('change', { bubbles: true })); }); $('#grade').click(); }
    return true;
  };
  const playTerms = async (hash, max) => {   // 용어 퀴즈를 풀면서 문제마다 적힌 주차를 모은다
    await go(hash);
    const got = {}; let k = 0;
    while (k < max) { const lab = qWeekLabel(); if (lab) got[lab] = (got[lab] || 0) + 1; if (!answerOne(k)) break; k++; await wait(0); }
    return { weeks: Object.keys(got), n: k, count: got };
  };
  const bank = (w.SDTApp && w.SDTApp.BANK) || [];
  const termByWeek = {}; bank.forEach(q => { if (q.unit === '용어') termByWeek[q.part] = (termByWeek[q.part] || 0) + 1; });
  const termWeeks = Object.keys(termByWeek), termAll = termWeeks.reduce((a, k) => a + termByWeek[k], 0);
  await go('#/quiz?week=' + qweek + '&unit=' + TERM_UNIT + '&start=1');
  console.log('term quiz first:', ($('#qstage .qtext') || {}).textContent);
  await go('#/quiz?week=all&unit=' + TERM_UNIT);
  const allTotal = qtotal(), perWeek = {};
  for (const wk of termWeeks) { await go('#/quiz?week=' + wk + '&unit=' + TERM_UNIT); perWeek[wk] = qtotal(); }
  console.log('term quiz pool  all:', allTotal, ' per week:', JSON.stringify(perWeek), ' bank 용어:', termAll, JSON.stringify(termByWeek));
  if (termAll) {
    if (allTotal !== termAll) errs.push('전 주차 용어 퀴즈 문항 수가 문제은행과 달라요: ' + allTotal + ' vs ' + termAll);
    termWeeks.forEach(wk => { if (perWeek[wk] !== termByWeek[wk]) errs.push('주차 용어 퀴즈(' + wk + ') 문항 수가 어긋나요: ' + perWeek[wk] + ' vs ' + termByWeek[wk]); });
    if (termWeeks.length > 1 && allTotal <= Math.max.apply(null, termWeeks.map(k => termByWeek[k]))) errs.push('전 주차 용어 퀴즈가 한 주차만 내요');
  }
  // 실제로 풀어 보며 문제에 적힌 주차가 여러 주차인지 본다 (한 주차만 내면서 전 주차라고 하면 실패)
  if (termWeeks.length) {
    const allPlay = await playTerms('#/quiz?week=all&unit=' + TERM_UNIT + '&start=1&n=0', 40);
    console.log('all term quiz played:', allPlay.n, '문항, 나온 주차:', allPlay.weeks.join(' / '));
    if (termWeeks.length > 1 && allPlay.weeks.length < 2) errs.push('전 주차 용어 퀴즈를 ' + allPlay.n + '문항 풀었는데 주차가 하나뿐이에요: ' + allPlay.weeks.join(','));
    const wk1 = termWeeks.find(x => termByWeek[x] >= 4) || termWeeks[0];
    const onePlay = await playTerms('#/quiz?week=' + wk1 + '&unit=' + TERM_UNIT + '&start=1&n=0', 12);
    const want = w.SDTApp.weekName(wk1);
    console.log('week term quiz played:', wk1, onePlay.n, '문항, 나온 주차:', onePlay.weeks.join(' / '));
    if (onePlay.weeks.some(x => x !== want)) errs.push('주차 용어 퀴즈(' + wk1 + ')에 다른 주차가 섞였어요: ' + onePlay.weeks.join(','));
  }
  await go('#/mock?week=' + qweek); $('#mockGo').click(); await wait(20); console.log('mock label:', ($('#qstage .mocklbl') || {}).textContent);
  await go('#/wrong'); console.log('wrong items:', $$('.witem').length); $('#retryWrong').click(); await wait(20); console.log('retry card:', !!$('#qstage .card'));
  await go('#/terms/' + qweek); console.log('term card:', !!$('#fcard'), ($('.whead p') || {}).textContent); if ($('#fcard')) { $('#fcard').click(); $('#fKnow').click(); console.log('after know:', ($('.whead p') || {}).textContent); }
  await go('#/terms/all'); console.log('all terms card:', !!$('#fcard'));
  await go('#/exams'); console.log('exams cards:', $$('#exams .card').length);
  await go('#/tips'); console.log('tips cards:', $$('#tips .card').length);
  for (const deck of Object.keys(meta.decks)) {
    if (!meta.decks[deck].have) continue;
    for (const pass of [1, 2, 3, 4]) {
      if (!meta.decks[deck].frames[pass - 1]) continue;
      await go('#/lesson/' + deck + '/' + pass); await wait(80);
      let n = 0; const kinds = {};
      while (n++ < 5000) {
        const f = w.eval('null'); // placeholder
        const slide = $('#pslide'); if (!slide) break;
        const ch = slide.querySelector('.schoices button'); if (ch && !ch.disabled) ch.click();
        const cnt = $('#pcount').textContent; const [a, b] = cnt.split(' / ').map(Number);
        if (a === b && !slide.querySelector('[data-s].hide')) break;
        $('#pNext').click();
      }
      console.log('lesson', deck, 'pass', pass, 'frames', $('#pcount') && $('#pcount').textContent);
    }
  }
  for (const wk of Object.keys(meta.units)) {
    for (const u of meta.units[wk]) {
      await go('#/unit/' + u.id); await wait(80);
      let n = 0;
      while (n++ < 2000) { const slide = $('#pslide'); if (!slide) break; const ch = slide.querySelector('.schoices button'); if (ch && !ch.disabled) ch.click(); const [a, b] = $('#pcount').textContent.split(' / ').map(Number); if (a === b && !slide.querySelector('[data-s].hide')) break; $('#pNext').click(); }
      console.log('unit', u.id, $('#pcount') && $('#pcount').textContent);
    }
  }
  await go('#/'); console.log('home again cards:', $$('.wcard').length, 'last:', ($('.intro .btn.primary') || {}).textContent);
  const allTermTool = $$('.toolrow .tool').find(a => (a.getAttribute('href') || '').indexOf('week=all&unit=%EC%9A%A9%EC%96%B4') >= 0);
  console.log('all term quiz tool:', allTermTool ? allTermTool.textContent : '없음');
  if (!allTermTool && termAll) errs.push('홈 도구에 전 주차 용어 퀴즈가 없어요');
  await go('#/week/' + qweek);
  const allTermBtn = $$('.termbar .btn').find(a => (a.getAttribute('href') || '').indexOf('week=all&unit=%EC%9A%A9%EC%96%B4') >= 0);
  console.log('week term bar all-quiz btn:', allTermBtn ? allTermBtn.textContent : '없음');
  await go('#/');
  console.log('errors:', errs.length ? errs.slice(0, 10) : '없음');
  process.exit(0);
})();
