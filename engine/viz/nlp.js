/* 움직이는 개념 그림: 자연어처리(NLP) 묶음. 틀은 viz.js, 설명은 README.md
   숫자는 정리 슬라이드 손계산 예제에서 가져왔다 (단원 id 는 각 그림 머리 주석). */
(function () {
  'use strict';
  const V = window.SDTViz;
  if (!V) return;
  const u = V.u;
  const at = u.at, seg = u.seg, num = u.num;

  /* 네모 칸 하나 (글자는 가운데). 반환 {r, t, x, y, w, h} */
  function box(parent, x, y, w, h, text, tcls) {
    const r = u.el(parent, 'rect', { x, y, width: w, height: h, rx: 4, class: 'vz-box' });
    const t = u.el(parent, 'text', { x: x + w / 2, y: y + h / 2 + 6, 'text-anchor': 'middle', class: tcls || 'vz-tb' }, text == null ? '' : text);
    return { r, t, x, y, w, h };
  }
  /* 칸 글자, 색, 투명도를 한꺼번에 */
  function put(c, text, cls, o) {
    if (text != null) u.txt(c.t, text);
    c.r.setAttribute('class', 'vz-box' + (cls ? ' ' + cls : ''));
    u.op(c.r, o); u.op(c.t, o);
  }
  /* 가로 막대 한 줄 (배경 + 채우는 막대) */
  function hbar(parent, x, y, w, h, cls) {
    const bg = u.el(parent, 'rect', { x, y, width: w, height: h, rx: 3, class: 'vz-area' });
    const b = u.el(parent, 'rect', { x, y, width: 0, height: h, rx: 3, class: 'vz-bar' + (cls ? ' ' + cls : '') });
    return { bg, b, x, y, w, h };
  }
  function setH(v, frac, cls, o) {
    u.set(v.b, { width: Math.max(0, v.w * u.clamp(frac, 0, 1)) });
    v.b.setAttribute('class', 'vz-bar' + (cls ? ' ' + cls : ''));
    u.op(v.bg, o); u.op(v.b, o);
  }
  /* 세로 막대 (밑에서 위로 자란다) */
  function vbar(parent, x, base, w, cls) {
    return { b: u.el(parent, 'rect', { x, y: base, width: w, height: 0, rx: 2, class: 'vz-bar' + (cls ? ' ' + cls : '') }), x, base, w };
  }
  function setV(v, h, cls, o) {
    h = Math.max(0, h);
    u.set(v.b, { y: v.base - h, height: h });
    v.b.setAttribute('class', 'vz-bar' + (cls ? ' ' + cls : ''));
    u.op(v.b, o);
  }
  const soft = xs => { const e = xs.map(Math.exp), s = e.reduce((a, b) => a + b, 0); return e.map(x => x / s); };
  const dot = (a, b) => a.reduce((s, x, i) => s + x * b[i], 0);

  /* ---------- 1. 어텐션 네 단계: 점수, 소프트맥스, 가중합, 예측 (w4-3, wb-6) ---------- */
  V.add('nlp.attn4', {
    title: '어텐션 네 단계',
    w: 480, h: 320,
    dur: 1200,
    states: [
      { cap: '소스 상태 h1~h4 와 쿼리 s 가 있어요. 점수는 아직 없어요.' },
      { tag: '1 점수', cap: '**내적(Dot Product)** 으로 3.6, 0.8, 0.5, 0.4 를 내요.' },
      { tag: '2 소프트맥스', cap: 'exp 를 씌워 합 41.97 로 나눠요. 0.87, 0.05, 0.04, 0.04.' },
      { tag: '3 가중합', cap: '가중치대로 섞으면 문맥 벡터 c = (1.78, 0.14).' },
      { tag: '4 예측', cap: 'c 로 다음 단어를 골라요. 이 네 단계가 핵심이에요.' },
    ],
    build(ctx) {
      const g = ctx.g = {};
      const cx = g.cx = [166, 250, 334, 418];
      g.hv = [[2, 0], [0, 2], [1, 1], [0, 0]];
      g.sc = [3.6, 0.8, 0.5, 0.4];
      g.ex = ['36.6', '2.23', '1.65', '1.49'];
      g.al = [0.87, 0.05, 0.04, 0.04];
      g.q = box(ctx.svg, 20, 46, 116, 40, '쿼리 s');
      g.h = cx.map((x, i) => box(ctx.svg, x - 40, 46, 80, 40, 'h' + (i + 1) + ' (' + g.hv[i][0] + ',' + g.hv[i][1] + ')'));
      g.lab = ['1 점수', '2 소프트맥스', '3 가중합', '4 예측'].map((t, i) => u.el(ctx.svg, 'text', { x: 18, y: [116, 170, 268, 308][i], class: 'vz-tb' }, t));
      g.sT = cx.map(x => u.el(ctx.svg, 'text', { x, y: 116, 'text-anchor': 'middle', class: 'vz-ta' }, ''));
      g.eT = cx.map(x => u.el(ctx.svg, 'text', { x, y: 138, 'text-anchor': 'middle', class: 'vz-ts' }, ''));
      g.sum = u.el(ctx.svg, 'text', { x: 18, y: 196, class: 'vz-ts' }, '');
      g.bars = cx.map(x => vbar(ctx.svg, x - 17, 210, 34, 'tl'));
      g.aT = cx.map(x => u.el(ctx.svg, 'text', { x, y: 230, 'text-anchor': 'middle', class: 'vz-tt' }, ''));
      g.mix = cx.map(() => u.el(ctx.svg, 'line', { class: 'vz-e tl' }));
      g.c = box(ctx.svg, 248, 244, 200, 34, '');
      g.pred = box(ctx.svg, 248, 286, 200, 30, '');
    },
    draw(ctx, s, k) {
      const g = ctx.g;
      const p1 = at(s, k, 1), p2 = at(s, k, 2), p3 = at(s, k, 3), p4 = at(s, k, 4);
      g.q.r.setAttribute('class', 'vz-box' + (s === 1 ? ' on' : ''));
      g.h.forEach((b, i) => {
        const hit = s === 1 ? seg(p1, i * 0.15, i * 0.15 + 0.4) : (s === 3 ? p3 : 0);
        b.r.setAttribute('class', 'vz-box' + (hit > 0.5 ? (s === 3 ? ' tl' : ' on') : ''));
      });
      g.sT.forEach((t, i) => {
        u.txt(t, num(g.sc[i], 1));
        u.op(t, s === 1 ? seg(p1, i * 0.15, i * 0.15 + 0.4) : (s >= 1 ? 1 : 0));
      });
      g.eT.forEach((t, i) => { u.txt(t, 'exp ' + g.ex[i]); u.op(t, s === 2 ? seg(p2, 0, 0.45) : 0); });
      u.txt(g.sum, '합 41.97');
      u.op(g.sum, s === 2 ? seg(p2, 0.2, 0.6) : (s > 2 ? 1 : 0));
      const grow = s === 2 ? seg(p2, 0.5, 1) : (s >= 2 ? 1 : 0);
      g.bars.forEach((b, i) => { setV(b, 60 * g.al[i] / 0.87 * grow, i === 0 ? '' : 'tl', grow > 0.01 ? 1 : 0); });
      g.aT.forEach((t, i) => {
        u.txt(t, num(g.al[i], 2));
        u.op(t, s === 2 ? seg(p2, 0.6, 1) : (s >= 2 ? 1 : 0));
      });
      g.mix.forEach((l, i) => u.draw(l, [g.cx[i], 234], [348, 244], s >= 3 ? seg(p3, 0, 0.7) : 0));
      put(g.c, 'c = (1.78, 0.14)', s >= 3 ? 'tl' : '', s >= 3 ? seg(p3, 0.5, 1) : 0);
      put(g.pred, '다음 단어 예측', s === 4 ? 'on' : '', p4);
      g.lab.forEach((t, i) => u.op(t, s >= i + 1 ? 1 : 0.35));
    },
  });

  /* ---------- 2. 같은 말을 세 가지로 자르기, 그리고 fertility (w2-1, w2-3) ---------- */
  V.add('nlp.tokenize', {
    title: '단어, 글자, 서브워드',
    w: 480, h: 300,
    dur: 1200,
    states: [
      { cap: 'unbelievable 한 단어예요. 어떻게 자를까요?' },
      { tag: '단어', cap: '단어로 자르면 1조각. 처음 보는 말은 못 다뤄요.' },
      { tag: '글자', cap: '글자로 자르면 12조각. 줄이 12배 길어져요.' },
      { tag: '서브워드', cap: '서브워드는 un, believ, able 3조각이에요.' },
      { tag: '한국어', cap: '4어절을 영어 토크나이저가 17토큰으로 잘라요.' },
      { cap: '17 ÷ 4 = 4.25, 8 ÷ 4 = 2.0 이에요.' },
    ],
    build(ctx) {
      const g = ctx.g = {};
      g.rowLab = ['단어', '글자', '서브워드'].map((t, i) => u.el(ctx.svg, 'text', { x: 66, y: [66, 122, 178][i], 'text-anchor': 'end', class: 'vz-tm' }, t));
      g.cnt = ['1조각', '12조각', '3조각'].map((t, i) => u.el(ctx.svg, 'text', { x: 462, y: [66, 150, 178][i], 'text-anchor': 'end', class: 'vz-ts' }, t));
      g.word = box(ctx.svg, 140, 44, 200, 32, 'unbelievable');
      g.chars = 'unbelievable'.split('').map((ch, i) => box(ctx.svg, 76 + i * 26, 100, 24, 32, ch));
      g.sub = [['un', 110, 60], ['believ', 174, 100], ['able', 278, 70]].map(a => box(ctx.svg, a[1], 156, a[2], 32, a[0]));
      g.kTitle = u.el(ctx.svg, 'text', { x: 18, y: 214, class: 'vz-tb' }, '한국어 4어절, 토크나이저 둘');
      g.kLab = ['영어 중심', '한국어 맞춤'].map((t, i) => u.el(ctx.svg, 'text', { x: 18, y: [248, 282][i], class: 'vz-ts' }, t));
      g.kBar = [hbar(ctx.svg, 110, 232, 266, 20, 'cr'), hbar(ctx.svg, 110, 266, 266, 20, 'ok')];
      g.kVal = ['17토큰, 4.25', '8토큰, 2.0'].map((t, i) => u.el(ctx.svg, 'text', { x: 476, y: [248, 282][i], 'text-anchor': 'end', class: i === 0 ? 'vz-tc' : 'vz-tok' }, t));
    },
    draw(ctx, s, k) {
      const g = ctx.g;
      const p1 = at(s, k, 1), p2 = at(s, k, 2), p3 = at(s, k, 3), p4 = at(s, k, 4), p5 = at(s, k, 5);
      /* 0번 상태에서도 자를 낱말은 보여 준다 (빈 화면으로 시작하지 않게) */
      put(g.word, null, s === 1 ? 'on' : '', 1);
      g.chars.forEach((c, i) => put(c, null, s === 2 ? 'tl' : '', seg(p2, i * 0.04, i * 0.04 + 0.4)));
      g.sub.forEach((c, i) => put(c, null, s === 3 ? 'ok' : '', seg(p3, i * 0.18, i * 0.18 + 0.5)));
      g.rowLab.forEach((t, i) => u.op(t, [1, p2, p3][i]));
      g.cnt.forEach((t, i) => u.op(t, [p1, p2, p3][i]));
      u.op(g.kTitle, p4);
      g.kLab.forEach((t, i) => u.op(t, i === 0 ? p4 : p5));
      setH(g.kBar[0], 1 * seg(p4, 0.2, 1), 'cr', p4);
      setH(g.kBar[1], 8 / 17 * seg(p5, 0, 0.7), 'ok', p5);
      u.op(g.kVal[0], s === 4 ? seg(p4, 0.6, 1) : (s >= 4 ? 1 : 0));
      u.op(g.kVal[1], s === 5 ? seg(p5, 0.5, 1) : (s >= 5 ? 1 : 0));
    },
  });

  /* ---------- 3. BPE 병합을 한 라운드씩 (w2-2) ---------- */
  /* 글자 칸은 자리를 지키고, 붙은 조각을 감싸는 테두리가 생긴다 */
  const BPEW = [
    { w: 'low', n: 5, ch: ['l', 'o', 'w'], grp: [[], [], [], [[0, 1]]], tok: [3, 3, 3, 2] },
    { w: 'lower', n: 2, ch: ['l', 'o', 'w', 'e', 'r'], grp: [[], [], [], [[0, 1]]], tok: [5, 5, 5, 4] },
    { w: 'newest', n: 6, ch: ['n', 'e', 'w', 'e', 's', 't'], grp: [[], [[3, 4]], [[3, 5]], [[3, 5]]], tok: [6, 5, 4, 4] },
    { w: 'widest', n: 3, ch: ['w', 'i', 'd', 'e', 's', 't'], grp: [[], [[3, 4]], [[3, 5]], [[3, 5]]], tok: [6, 5, 4, 4] },
  ];
  const BPEP = [
    [['(e,s)', 9], ['(s,t)', 9], ['(w,e)', 8], ['(l,o)', 7]],
    [['(es,t)', 9], ['(l,o)', 7], ['(o,w)', 7], ['(w,es)', 6]],
    [['(l,o)', 7], ['(o,w)', 7], ['(n,e)', 6], ['(e,w)', 6]],
  ];
  V.add('nlp.bpe', {
    title: 'BPE 병합 세 라운드',
    w: 480, h: 300,
    dur: 1300,
    states: [
      { cap: '말뭉치 4단어를 글자로 쪼갰어요. 빈도는 5, 2, 6, 3.' },
      { tag: '세기', cap: '이웃 쌍 세기. (e,s) 가 9번으로 1등이에요.' },
      { tag: '병합 1', cap: 'e + s 를 es 로. 다시 세면 (es,t) 9 가 1등.' },
      { tag: '병합 2', cap: 'es + t 를 est 로. 다시 세면 (l,o) 7 이 1등.' },
      { tag: '병합 3', cap: 'l + o 를 lo 로. **병합 규칙(Merge Rule)** 3줄 완성.' },
      { cap: '처음 보는 lowest 도 lo, w, est 로 잘려요.' },
    ],
    build(ctx) {
      const g = ctx.g = {};
      g.rows = BPEW.map((W, r) => {
        const y = 40 + r * 36;
        const lab = u.el(ctx.svg, 'text', { x: 16, y: y + 19, class: 'vz-ts' }, W.w + ' ' + W.n + '번');
        const chips = W.ch.map((ch, i) => box(ctx.svg, 96 + i * 27, y, 24, 28, ch));
        const ring = [0, 1].map(() => u.el(ctx.svg, 'rect', { rx: 6, class: 'vz-hl on' }));
        const tok = u.el(ctx.svg, 'text', { x: 292, y: y + 19, 'text-anchor': 'end', class: 'vz-ts' }, '');
        return { W, y, lab, chips, ring, tok };
      });
      g.barTitle = u.el(ctx.svg, 'text', { x: 302, y: 26, class: 'vz-ts' }, '이웃 쌍 세기');
      g.bars = [0, 1, 2, 3].map(i => {
        const y = 44 + i * 34;
        return { t: u.el(ctx.svg, 'text', { x: 302, y, class: 'vz-tb' }, ''), b: hbar(ctx.svg, 302, y + 6, 160, 14, '') };
      });
      g.ruleTitle = u.el(ctx.svg, 'text', { x: 302, y: 26, class: 'vz-ts' }, '병합 규칙');
      g.rules = ['1 (e,s) → es', '2 (es,t) → est', '3 (l,o) → lo'].map((t, i) => u.el(ctx.svg, 'text', { x: 302, y: 52 + i * 30, class: 'vz-ta' }, t));
      g.newTitle = u.el(ctx.svg, 'text', { x: 16, y: 206, class: 'vz-tb' }, '처음 보는 단어 lowest');
      g.newChips = 'lowest'.split('').map((ch, i) => box(ctx.svg, 140 + i * 27, 216, 24, 28, ch));
      g.newRing = [0, 1].map(() => u.el(ctx.svg, 'rect', { rx: 6, class: 'vz-hl on' }));
      g.newOut = u.el(ctx.svg, 'text', { x: 240, y: 282, 'text-anchor': 'middle', class: 'vz-ta' }, 'lowest → lo + w + est');
    },
    draw(ctx, s, k) {
      const g = ctx.g;
      const stage = s <= 1 ? 0 : Math.min(3, s - 1);          // 글자 칸을 감싸는 테두리 단계
      const prev = Math.max(0, stage - 1);
      const mrg = s >= 2 && s <= 4 ? seg(k, 0.1, 0.7) : 1;    // 병합 테두리가 자라는 정도
      g.rows.forEach(row => {
        const now = row.W.grp[stage], old = row.W.grp[prev];
        const hot1 = s === 1 && row.W.ch[3] === 'e' && row.W.ch[4] === 's';   // 세는 단계에서는 1등 쌍 (e,s) 만 표시
        row.chips.forEach((c, i) => {
          const on = hot1 ? (i === 3 || i === 4) : (s >= 2 && now.some(a => i >= a[0] && i <= a[1]));
          put(c, null, on ? (s === 1 ? 'am' : 'tl') : '', 1);
        });
        row.ring.forEach((rc, j) => {
          const a = now[j], b = old[j];
          if (!a) { u.set(rc, { x: 0, y: 0, width: 0, height: 0 }); u.op(rc, 0); return; }
          const from = b || [a[0], a[0]];
          const x0 = row.chips[a[0]].x - 3;
          const x1 = u.lerp(row.chips[from[1]].x + 27, row.chips[a[1]].x + 27, mrg) - 3;
          u.set(rc, { x: x0, y: row.y - 4, width: Math.max(4, x1 - x0), height: 36 });
          u.op(rc, s >= 2 ? 1 : 0);
        });
        u.txt(row.tok, row.W.tok[stage] + '조각');
        u.op(row.tok, s >= 1 ? 1 : 0);
      });
      const bs = s >= 1 && s <= 3 ? s - 1 : -1;
      u.op(g.barTitle, bs >= 0 ? 1 : 0);
      g.bars.forEach((bar, i) => {
        const e = bs >= 0 ? BPEP[bs][i] : null;
        u.txt(bar.t, e ? e[0] + ' ' + e[1] : '');
        const show = e ? (s >= 2 ? seg(k, 0.7, 1) : seg(at(s, k, 1), i * 0.12, i * 0.12 + 0.5)) : 0;
        setH(bar.b, e ? e[1] / 9 * show : 0, e && i === 0 ? 'cr' : '', show);
        u.op(bar.t, show);
      });
      u.op(g.ruleTitle, s >= 4 ? 1 : 0);
      g.rules.forEach((t, i) => u.op(t, s >= 4 ? (s === 4 ? seg(k, i * 0.2, i * 0.2 + 0.5) : 1) : 0));
      const p5 = at(s, k, 5);
      u.op(g.newTitle, p5);
      g.newChips.forEach((c, i) => {
        const inG = i <= 1 || i >= 3;
        put(c, null, p5 > 0.6 && inG ? 'tl' : '', p5);
      });
      [[0, 1], [3, 5]].forEach((a, j) => {
        const rc = g.newRing[j];
        const x0 = g.newChips[a[0]].x - 3, x1 = g.newChips[a[1]].x + 24 + 3;
        u.set(rc, { x: x0, y: 212, width: x1 - x0, height: 36 });
        u.op(rc, seg(p5, 0.4 + j * 0.2, 0.8 + j * 0.2));
      });
      u.op(g.newOut, seg(p5, 0.75, 1));
    },
  });

  /* ---------- 4. 스킵그램 한 걸음: 점수, 확률, 벌점, 기울기 (w2-5, w2-6) ---------- */
  const SGU = [[1, 2], [1, 0], [-1, 2]];
  const SGN = ['banking', 'crises', 'pizza'];
  const SGV = [[1, 0.5], [1.09, 0.745]];
  function sg(v) { const sc = SGU.map(x => dot(v, x)); return { sc, pr: soft(sc) }; }
  V.add('nlp.skipgram', {
    title: '스킵그램 한 걸음',
    w: 480, h: 312,
    dur: 1200,
    states: [
      { cap: '중심 단어 into 의 v = (1, 0.5), 정답 이웃은 banking.' },
      { tag: '점수', cap: '**내적(Dot Product)**: banking 2, crises 1, pizza 0.' },
      { tag: '확률', cap: '**소프트맥스(Softmax)** 로 0.665, 0.245, 0.090.' },
      { tag: '벌점', cap: '정답 확률의 음의 로그: -log 0.665 = 0.408.' },
      { tag: '기울기', cap: '(1, 2) 빼기 (0.82, 1.51) = (0.18, 0.49).' },
      { tag: '한 걸음', cap: '학습률 0.5 로 v 가 (1.09, 0.745) 로 옮겨요.' },
      { cap: '다시 재면 banking 0.747, 벌점 0.291 로 줄어요.' },
    ],
    build(ctx) {
      const g = ctx.g = {};
      const sx = g.sx = x => 145 + x * 70, sy = g.sy = y => 250 - y * 84;
      u.el(ctx.svg, 'line', { x1: 40, y1: 250, x2: 256, y2: 250, class: 'vz-axis' });
      u.el(ctx.svg, 'line', { x1: 145, y1: 34, x2: 145, y2: 256, class: 'vz-axis' });
      u.el(ctx.svg, 'text', { x: 20, y: 30, class: 'vz-ts' }, '단어 지도 (2차원)');
      g.uArr = SGU.map((p, i) => {
        const a = u.arrow(ctx.svg, i === 2 ? 'mu' : 'tl');
        u.setArrow(a, [sx(0), sy(0)], [sx(p[0]), sy(p[1])], 1);
        return a;
      });
      g.uLab = SGU.map((p, i) => u.el(ctx.svg, 'text', { x: sx(p[0]) + (i === 2 ? -6 : 6), y: sy(p[1]) - 8, 'text-anchor': i === 2 ? 'end' : 'start', class: 'vz-ts' }, SGN[i]));
      g.vArr = u.arrow(ctx.svg, 'cr');
      g.vLab = u.el(ctx.svg, 'text', { x: 0, y: 0, class: 'vz-tc' }, 'v');
      g.rows = [0, 1, 2].map(i => {
        const y = 50 + i * 72;
        return {
          n: u.el(ctx.svg, 'text', { x: 288, y, class: 'vz-ts' }, SGN[i]),
          s: u.el(ctx.svg, 'text', { x: 462, y, 'text-anchor': 'end', class: 'vz-ta' }, ''),
          b: hbar(ctx.svg, 288, y + 8, 174, 22, i === 0 ? 'tl' : ''),
          p: u.el(ctx.svg, 'text', { x: 290, y: y + 50, class: 'vz-tt' }, ''),
        };
      });
      g.loss = u.el(ctx.svg, 'text', { x: 20, y: 282, class: 'vz-tc' }, '');
      g.grad = u.el(ctx.svg, 'text', { x: 20, y: 304, class: 'vz-ta' }, '');
    },
    draw(ctx, s, k) {
      const g = ctx.g, sx = g.sx, sy = g.sy;
      const p5 = at(s, k, 5), p6 = at(s, k, 6);
      const vNow = s >= 5 ? [u.lerp(SGV[0][0], SGV[1][0], u.ease(p5)), u.lerp(SGV[0][1], SGV[1][1], u.ease(p5))] : SGV[0];
      u.setArrow(g.vArr, [sx(0), sy(0)], [sx(vNow[0]), sy(vNow[1])], 1);
      u.set(g.vLab, { x: sx(vNow[0]) + 8, y: sy(vNow[1]) + 16 });
      g.uArr.forEach((a, i) => u.op(a.g, s >= 1 ? 1 : 0.4));
      g.uLab.forEach(t => u.op(t, 1));
      const r0 = sg(SGV[0]), r1 = sg(SGV[1]);
      const tp = s >= 6 ? u.lerp(0, 1, u.ease(p6)) : 0;
      g.rows.forEach((row, i) => {
        const sc = u.lerp(r0.sc[i], r1.sc[i], tp), pr = u.lerp(r0.pr[i], r1.pr[i], tp);
        u.txt(row.s, '점수 ' + num(sc, 2));
        u.op(row.s, s === 1 ? seg(k, i * 0.15, i * 0.15 + 0.5) : (s >= 1 ? 1 : 0));
        const bo = s === 2 ? seg(k, i * 0.12, i * 0.12 + 0.6) : (s >= 2 ? 1 : 0);
        setH(row.b, pr * (s === 2 ? seg(k, 0.1, 1) : 1), i === 0 ? 'tl' : '', bo);
        u.txt(row.p, num(pr, 3));
        u.op(row.p, bo);
        u.op(row.n, s >= 1 ? 1 : 0.4);
      });
      const loss0 = -Math.log(r0.pr[0]), loss1 = -Math.log(r1.pr[0]);
      u.txt(g.loss, s >= 6 ? '벌점 ' + num(loss0, 3) + ' → ' + num(u.lerp(loss0, loss1, tp), 3) : '벌점 -log 0.665 = ' + num(loss0, 3));
      u.op(g.loss, at(s, k, 3));
      u.txt(g.grad, s >= 5 ? '한 걸음: v = (' + num(vNow[0], 3) + ', ' + num(vNow[1], 3) + ')' : '기울기 = (0.18, 0.49)');
      u.op(g.grad, at(s, k, 4));
    },
  });

  /* ---------- 5. RNN 은 차례대로, 셀프 어텐션은 한 번에 (w3-9, w4-6) ---------- */
  V.add('nlp.parallel', {
    title: '차례대로 대 한 번에',
    w: 480, h: 310,
    dur: 1200,
    states: [
      { cap: '토큰 5개 문장이에요. 두 방식을 나란히 봐요.' },
      { tag: 'RNN 1걸음', cap: 'The 를 읽고 메모 h1 을 써요.' },
      { tag: 'RNN 2걸음', cap: 'h1 이 나와야 h2 를 쓸 수 있어요.' },
      { tag: 'RNN 5걸음', cap: '5걸음이 필요해요. 행렬은 Wh, We, U 3개뿐.' },
      { tag: '셀프 어텐션', cap: '5자리를 한 번에 계산해요. 기다림이 없어요.' },
      { cap: '값은 치러요. 점수 칸 5 x 5 = 25 개예요.' },
    ],
    build(ctx) {
      const g = ctx.g = {};
      const toks = g.toks = ['The', 'chef', 'who', 'made', 'tea'];
      const cx = g.cx = [76, 156, 236, 316, 396];
      u.el(ctx.svg, 'text', { x: 18, y: 26, class: 'vz-tb' }, 'RNN: 차례대로');
      g.rnnTok = cx.map((x, i) => box(ctx.svg, x - 34, 96, 68, 30, toks[i]));
      g.rnnH = cx.map((x, i) => u.node(ctx.svg, x, 58, 18, 'h' + (i + 1)));
      g.rnnUp = cx.map(() => u.el(ctx.svg, 'line', { class: 'vz-e' }));
      g.rnnAcross = [0, 1, 2, 3].map(() => u.arrow(ctx.svg, 'cr'));
      g.rnnN = u.el(ctx.svg, 'text', { x: 462, y: 26, 'text-anchor': 'end', class: 'vz-tc' }, '');
      u.el(ctx.svg, 'line', { x1: 14, y1: 146, x2: 466, y2: 146, class: 'vz-grid' });
      u.el(ctx.svg, 'text', { x: 18, y: 174, class: 'vz-tb' }, '셀프 어텐션: 한 번에');
      g.saTok = cx.map((x, i) => box(ctx.svg, x - 34, 246, 68, 30, toks[i]));
      g.saZ = cx.map((x, i) => u.node(ctx.svg, x, 208, 18, 'z' + (i + 1)));
      g.saLine = cx.map(() => u.el(ctx.svg, 'line', { class: 'vz-e tl' }));
      g.saN = u.el(ctx.svg, 'text', { x: 462, y: 174, 'text-anchor': 'end', class: 'vz-tt' }, '');
      g.note = u.el(ctx.svg, 'text', { x: 240, y: 300, 'text-anchor': 'middle', class: 'vz-ta' }, '');
    },
    draw(ctx, s, k) {
      const g = ctx.g, cx = g.cx;
      /* RNN: 상태 1, 2 에서 한 걸음씩, 상태 3 에서 남은 걸음을 훑는다 */
      const done = s >= 3 ? (s === 3 ? 2 + u.clamp(Math.floor(k * 3.2), 0, 3) : 5) : (s === 1 ? (k > 0.5 ? 1 : 0) : s === 2 ? (k > 0.5 ? 2 : 1) : 0);
      g.rnnTok.forEach((b, i) => put(b, null, i < done ? 'cr' : '', s >= 1 ? 1 : 0.5));
      g.rnnH.forEach((nd, i) => {
        nd.g.setAttribute('class', 'vz-node' + (i < done ? ' cr' : ' off'));
        u.op(nd.g, s >= 1 ? 1 : 0.5);
      });
      g.rnnUp.forEach((l, i) => u.draw(l, [cx[i], 96], [cx[i], 78], i < done ? 1 : 0));
      g.rnnAcross.forEach((a, i) => u.setArrow(a, [cx[i] + 20, 58], [cx[i + 1] - 20, 58], i + 1 < done ? 1 : 0));
      u.txt(g.rnnN, 'RNN 걸음 ' + done + ' / 5');
      u.op(g.rnnN, s >= 1 ? 1 : 0);
      /* 셀프 어텐션: 상태 4 에서 다섯 자리가 동시에 켜진다 */
      const p4 = at(s, k, 4);
      g.saTok.forEach(b => put(b, null, p4 > 0.2 ? 'tl' : '', s >= 4 ? 1 : 0.5));
      g.saZ.forEach(nd => {
        nd.g.setAttribute('class', 'vz-node' + (p4 > 0.55 ? ' tl' : ' off'));
        u.op(nd.g, s >= 4 ? 1 : 0.5);
      });
      g.saLine.forEach((l, i) => u.draw(l, [cx[i], 246], [236, 226], seg(p4, 0.15, 0.55)));
      u.txt(g.saN, 'SA 걸음 1 / 1');
      u.op(g.saN, p4);
      u.txt(g.note, s === 5 ? '길이가 2배면 점수 칸은 4배예요' : s === 4 ? '병렬화(Parallelization)' : s >= 3 ? '서로 다른 행렬은 3개' : '');
      u.op(g.note, s >= 3 ? 1 : 0);
    },
  });

  /* ---------- 6. 사인 코사인 위치 인코딩 (w4-7) ---------- */
  const PEW = [
    ['sin i=0', 'vz-ta', p => Math.sin(p), 'vz-curve'],
    ['cos i=0', 'vz-tt', p => Math.cos(p), 'vz-curve tl'],
    ['sin i=1', 'vz-tc', p => Math.sin(p / 100), 'vz-curve cr'],
    ['cos i=1', 'vz-tm', p => Math.cos(p / 100), 'vz-curve mu'],
  ];
  V.add('nlp.posenc', {
    title: '자리마다 다른 물결',
    w: 480, h: 300,
    dur: 1200,
    params: { pos: 1 },
    capsDependOn: true,
    controls: [{ key: 'pos', type: 'range', label: '자리 pos', min: 0, max: 12, step: 1, fmt: v => '자리 ' + v }],
    states: P => [
      { set: { pos: 1 }, cap: 'pos 는 자리 번호, d = 4 라 칸이 4개예요.' },
      { tag: 'i = 0', cap: '첫 짝은 10000^0 = 1 로 나눠 빨리 흔들려요.' },
      { tag: 'i = 1', cap: '둘째 짝은 100 으로 나눠 거의 안 움직여요.' },
      { set: { pos: 1 }, tag: 'pos = 1', cap: 'sin 1 = 0.8415, cos 1 = 0.5403 을 읽어요.' },
      { cap: '자리 ' + P.pos + ' 의 첫 칸은 ' + num(Math.sin(P.pos), 4) + ' 이에요.' },
      { set: { pos: 5 }, cap: '자리 5 로 옮기면 네 칸이 다 바뀌어요.' },
    ],
    build(ctx) {
      const g = ctx.g = {};
      const sx = g.sx = p => 60 + p / 12 * 350, sy = g.sy = v => 124 - 62 * v;
      u.el(ctx.svg, 'line', { x1: 60, y1: 124, x2: 414, y2: 124, class: 'vz-grid' });
      u.el(ctx.svg, 'line', { x1: 60, y1: 56, x2: 60, y2: 192, class: 'vz-axis' });
      u.el(ctx.svg, 'text', { x: 54, y: 62, 'text-anchor': 'end', class: 'vz-ts' }, '1');
      u.el(ctx.svg, 'text', { x: 54, y: 196, 'text-anchor': 'end', class: 'vz-ts' }, '-1');
      [0, 4, 8, 12].forEach(p => u.el(ctx.svg, 'text', { x: sx(p), y: 210, 'text-anchor': 'middle', class: 'vz-ts' }, String(p)));
      u.el(ctx.svg, 'text', { x: 456, y: 214, 'text-anchor': 'end', class: 'vz-ts' }, 'pos');
      g.curve = PEW.map(w => {
        const pts = [];
        for (let p = 0; p <= 12.001; p += 0.05) pts.push(u.r(sx(p)) + ' ' + u.r(sy(w[2](p))));
        return u.el(ctx.svg, 'path', { d: 'M' + pts.join(' L'), class: w[3] });
      });
      g.mark = u.el(ctx.svg, 'line', { class: 'vz-e cr' });
      g.dots = PEW.map(() => u.el(ctx.svg, 'circle', { r: 7, class: 'vz-dot am' }));
      g.cellLab = PEW.map((w, i) => u.el(ctx.svg, 'text', { x: 110 + i * 86, y: 240, 'text-anchor': 'middle', class: w[1] }, w[0]));
      g.cells = PEW.map((w, i) => box(ctx.svg, 70 + i * 86, 248, 80, 34, ''));
      g.posT = u.el(ctx.svg, 'text', { x: 240, y: 30, 'text-anchor': 'middle', class: 'vz-tb' }, '');
    },
    draw(ctx, s, k) {
      const g = ctx.g, P = ctx.p;
      /* 상태 5 는 자리 1 에서 P.pos 로 미끄러진다 */
      const pos = s === 5 ? u.lerp(1, P.pos, u.ease(k)) : P.pos;
      const show = [at(s, k, 1), at(s, k, 1), at(s, k, 2), at(s, k, 2)];
      g.curve.forEach((c, i) => u.op(c, show[i]));
      const p3 = at(s, k, 3);
      u.set(g.mark, { x1: g.sx(pos), y1: 50, x2: g.sx(pos), y2: 196 });
      u.op(g.mark, p3);
      g.dots.forEach((c, i) => {
        u.set(c, { cx: g.sx(pos), cy: g.sy(PEW[i][2](pos)) });
        u.op(c, Math.min(p3, show[i]));
      });
      const p4 = at(s, k, 4);
      g.cellLab.forEach((t, i) => u.op(t, Math.min(p3, show[i])));
      g.cells.forEach((c, i) => put(c, num(PEW[i][2](pos), 4), s >= 4 ? 'on' : '', s >= 3 ? Math.max(p3 * 0.5, p4) : 0));
      u.txt(g.posT, '자리 pos = ' + num(pos, 0) + ' 의 위치 벡터');
      u.op(g.posT, p3);
    },
  });

  /* ---------- 7. 인과 마스킹: 오른쪽 위 삼각형 (w4-7) ---------- */
  V.add('nlp.mask', {
    title: '미래를 가리는 삼각형',
    w: 480, h: 300,
    dur: 1300,
    states: [
      { cap: '행은 지금 토큰, 열은 바라보는 토큰. 칸 25개.' },
      { cap: 'who 행을 그냥 두면 뒤의 made, tea 까지 봐요.' },
      { tag: '마스킹', cap: '오른쪽 위 10칸을 소프트맥스 전에 막아요.' },
      { tag: '소프트맥스', cap: '막은 칸의 가중치는 정확히 0 이 돼요.' },
      { cap: '삼각형이 있으면 GPT, 없으면 BERT 예요.' },
    ],
    build(ctx) {
      const g = ctx.g = {};
      const toks = ['The', 'chef', 'who', 'made', 'tea'];
      const x0 = 96, y0 = 70, cw = 54, ch = 38;
      g.x0 = x0; g.y0 = y0; g.cw = cw; g.ch = ch;
      u.el(ctx.svg, 'text', { x: 240, y: 30, 'text-anchor': 'middle', class: 'vz-tm' }, '행 = 지금 토큰, 열 = 바라보는 토큰');
      toks.forEach((t, j) => u.el(ctx.svg, 'text', { x: x0 + (j + 0.5) * cw, y: 62, 'text-anchor': 'middle', class: 'vz-ts' }, t));
      toks.forEach((t, i) => u.el(ctx.svg, 'text', { x: 88, y: y0 + (i + 0.5) * ch + 5, 'text-anchor': 'end', class: 'vz-ts' }, t));
      g.cells = [];
      for (let i = 0; i < 5; i++) for (let j = 0; j < 5; j++) g.cells.push(Object.assign(box(ctx.svg, x0 + j * cw + 2, y0 + i * ch + 2, cw - 4, ch - 4, '', 'vz-ts'), { i, j }));
      g.hl = u.el(ctx.svg, 'rect', { x: x0 - 3, y: y0 + 2 * ch - 3, width: 5 * cw + 6, height: ch + 6, rx: 6, class: 'vz-hl' });
      g.miniT = u.el(ctx.svg, 'text', { x: 427, y: 96, 'text-anchor': 'middle', class: 'vz-ts' }, '인코더');
      g.mini = [];
      for (let i = 0; i < 5; i++) for (let j = 0; j < 5; j++) g.mini.push(u.el(ctx.svg, 'rect', { x: 392 + j * 14 + 1, y: 104 + i * 14 + 1, width: 12, height: 12, rx: 2, class: 'vz-box on' }));
      g.note = u.el(ctx.svg, 'text', { x: 240, y: 288, 'text-anchor': 'middle', class: 'vz-tb' }, '');
    },
    draw(ctx, s, k) {
      const g = ctx.g;
      const p2 = at(s, k, 2);
      let ord = 0;
      const ordOf = {};
      for (let d = 1; d < 5; d++) for (let i = 0; i < 5 - d; i++) ordOf[i + ',' + (i + d)] = ord++;
      g.cells.forEach(c => {
        const masked = c.j > c.i;
        const o = masked ? seg(p2, (ordOf[c.i + ',' + c.j] || 0) * 0.06, (ordOf[c.i + ',' + c.j] || 0) * 0.06 + 0.4) : 0;
        let txt = '', cls = 'on';
        if (masked && o > 0.5) { txt = s >= 3 ? '0' : '막음'; cls = 'off'; }
        else if (!masked && s >= 3) { txt = num(1 / (c.i + 1), 2); cls = 'tl'; }
        else if (s === 1 && c.i === 2 && c.j > 2) { cls = 'cr'; }
        put(c, txt, cls, 1);
      });
      u.op(g.hl, s === 1 ? at(s, k, 1) : 0);
      const p4 = at(s, k, 4);
      u.op(g.miniT, p4);
      g.mini.forEach(r => u.op(r, p4));
      u.txt(g.note, s === 4 ? '삼각형 있으면 GPT, 없으면 BERT'
        : s === 3 ? '남은 칸끼리 1 을 나눠 가져요 (예시 숫자)'
          : s === 2 ? '막은 칸 10개, 소프트맥스 전에 막아요'
            : s === 1 ? 'who 가 made, tea 를 보면 반칙이에요' : '칸 5 x 5 = 25 개');
      u.op(g.note, 1);
    },
  });

  /* ---------- 8. 루트 d_k 로 나누는 까닭 (w4-6) ---------- */
  V.add('nlp.scale', {
    title: '루트 d_k 로 나누기',
    w: 480, h: 310,
    dur: 1200,
    states: [
      { cap: 'd_k = 64 이면 루트 64 = 8 이에요.' },
      { cap: '점수 24, 8, 16 에 그냥 소프트맥스를 씌워요.' },
      { tag: '뾰족', cap: '0.9997 로 거의 1. 기울기가 죽어요.' },
      { tag: '나누기', cap: '8 로 나누면 점수가 3, 1, 2 가 돼요.' },
      { cap: '이제 0.665, 0.090, 0.245. 부드러워요.' },
    ],
    build(ctx) {
      const g = ctx.g = {};
      g.dk = u.el(ctx.svg, 'text', { x: 240, y: 28, 'text-anchor': 'middle', class: 'vz-tb' }, 'd_k = 64, 루트 64 = 8');
      g.title = [['그냥 소프트맥스', 118], ['8 로 나눈 뒤', 358]].map(a => u.el(ctx.svg, 'text', { x: a[1], y: 56, 'text-anchor': 'middle', class: 'vz-tb' }, a[0]));
      u.el(ctx.svg, 'line', { x1: 240, y1: 44, x2: 240, y2: 300, class: 'vz-grid' });
      g.sm = [['소프트맥스', 118], ['소프트맥스', 358]].map(a => u.el(ctx.svg, 'text', { x: a[1], y: 132, 'text-anchor': 'middle', class: 'vz-ts' }, a[0]));
      g.raw = [24, 8, 16];
      g.div = [3, 1, 2];
      g.pRaw = soft(g.raw);
      g.pDiv = soft(g.div);
      g.cells = [0, 1, 2].map(i => box(ctx.svg, 33 + i * 60, 72, 50, 34, ''));
      g.cells2 = [0, 1, 2].map(i => box(ctx.svg, 273 + i * 60, 72, 50, 34, ''));
      g.bars = [0, 1, 2].map(i => vbar(ctx.svg, 38 + i * 60, 256, 40, 'cr'));
      g.bars2 = [0, 1, 2].map(i => vbar(ctx.svg, 278 + i * 60, 256, 40, 'ok'));
      g.pT = [0, 1, 2].map(i => u.el(ctx.svg, 'text', { x: 58 + i * 60, y: 276, 'text-anchor': 'middle', class: 'vz-tc' }, ''));
      g.pT2 = [0, 1, 2].map(i => u.el(ctx.svg, 'text', { x: 298 + i * 60, y: 276, 'text-anchor': 'middle', class: 'vz-tok' }, ''));
      g.abc = [0, 1, 2].map(i => u.el(ctx.svg, 'text', { x: 58 + i * 60, y: 298, 'text-anchor': 'middle', class: 'vz-ts' }, 'ABC'[i]));
      g.abc2 = [0, 1, 2].map(i => u.el(ctx.svg, 'text', { x: 298 + i * 60, y: 298, 'text-anchor': 'middle', class: 'vz-ts' }, 'ABC'[i]));
    },
    draw(ctx, s, k) {
      const g = ctx.g;
      const p1 = at(s, k, 1), p2 = at(s, k, 2), p3 = at(s, k, 3), p4 = at(s, k, 4);
      u.op(g.dk, 1);
      u.op(g.title[0], p1); u.op(g.title[1], p3);
      u.op(g.sm[0], p2); u.op(g.sm[1], p4);
      g.cells.forEach((c, i) => put(c, String(g.raw[i]), s === 1 ? 'cr' : '', seg(p1, i * 0.15, i * 0.15 + 0.5)));
      g.cells2.forEach((c, i) => put(c, String(g.div[i]), s === 3 ? 'ok' : '', seg(p3, i * 0.15, i * 0.15 + 0.5)));
      g.bars.forEach((b, i) => setV(b, 110 * g.pRaw[i] * seg(p2, 0.1, 1), 'cr', p2));
      g.bars2.forEach((b, i) => setV(b, 110 * g.pDiv[i] * seg(p4, 0.1, 1), 'ok', p4));
      g.pT.forEach((t, i) => { u.txt(t, g.pRaw[i].toFixed(4)); u.op(t, seg(p2, 0.5, 1)); });
      g.pT2.forEach((t, i) => { u.txt(t, g.pDiv[i].toFixed(3)); u.op(t, seg(p4, 0.5, 1)); });
      g.abc.forEach(t => u.op(t, p1));
      g.abc2.forEach(t => u.op(t, p3));
    },
  });
})();
