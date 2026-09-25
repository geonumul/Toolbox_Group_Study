/* 움직이는 개념 그림: 신호및시스템 묶음. 틀은 viz.js, 설명은 README.md
   숫자는 기초 다지기(wb-*)와 1~3주차 정리 슬라이드의 손계산에서 그대로 가져왔다 (단원 id 는 각 그림 머리 주석).
   학생이 미적분, 복소수 배경이 거의 없으니 캡션은 쉬운 말과 숫자로 짧게 쓴다. 수식은 KaTeX 없이 평범한 글자로 쓴다. */
(function () {
  'use strict';
  const V = window.SDTViz;
  if (!V) return;
  const u = V.u;
  const at = u.at, seg = u.seg, num = u.num;
  const PI = Math.PI;

  /* ---------- 공통 도우미 ---------- */
  /* 가로축 하나. 오른쪽 끝에 변수 이름 */
  function axisH(parent, x0, x1, y, label) {
    u.el(parent, 'line', { x1: x0, y1: y, x2: x1, y2: y, class: 'vz-axis' });
    if (label) u.el(parent, 'text', { x: x1 + 5, y: y + 5, class: 'vz-ts' }, label);
    return y;
  }
  /* 눈금 하나 + 숫자 (dy 를 주면 숫자 자리를 옮긴다) */
  function tick(parent, x, y, label, dy) {
    u.el(parent, 'line', { x1: x, y1: y - 4, x2: x, y2: y + 4, class: 'vz-axis' });
    if (label != null) u.el(parent, 'text', { x, y: y + (dy == null ? 19 : dy), 'text-anchor': 'middle', class: 'vz-ts' }, label);
  }
  /* 이산 신호 막대 하나: 선 + 동그라미 + 숫자 */
  function stem(parent, cls) {
    const g = u.el(parent, 'g');
    const l = u.el(g, 'line', { class: 'vz-e' + (cls ? ' ' + cls : '') });
    const c = u.el(g, 'circle', { r: 5, class: 'vz-dot' + (cls ? ' ' + cls : '') });
    const t = u.el(g, 'text', { 'text-anchor': 'middle', class: 'vz-ts' }, '');
    return { g, l, c, t };
  }
  /* 막대를 x 칸, 바닥 base 에서 값 v (한 칸 sc px) 만큼. o 투명도, lab 위에 적을 글자 */
  function putStem(st, x, base, v, sc, o, lab) {
    const y = base - v * sc;
    u.set(st.l, { x1: x, y1: base, x2: x, y2: y });
    u.set(st.c, { cx: x, cy: y });
    u.set(st.t, { x, y: v >= 0 ? y - 10 : y - 9 });
    u.txt(st.t, lab == null ? '' : lab);
    u.op(st.g, o);
  }
  const stemCls = (st, cls) => {
    st.l.setAttribute('class', 'vz-e' + (cls ? ' ' + cls : ''));
    st.c.setAttribute('class', 'vz-dot' + (cls ? ' ' + cls : ''));
  };
  /* 점 목록을 잇는 길 */
  const pathD = pts => 'M' + pts.map(p => u.r(p[0]) + ' ' + u.r(p[1])).join(' L');
  /* 막대 한 칸 (표 모양 그림에 쓴다) */
  function bar(parent, cls) {
    const g = u.el(parent, 'g');
    return { g, r: u.el(g, 'rect', { width: 18, rx: 2, class: 'vz-bar' + (cls ? ' ' + cls : '') }), t: u.el(g, 'text', { 'text-anchor': 'middle', class: 'vz-ts' }, '') };
  }
  function putBar(b, x, base, v, sc, o, lab) {
    const h = Math.abs(v) * sc;
    u.set(b.r, { x: x - 9, y: v >= 0 ? base - h : base, height: h });
    u.set(b.t, { x, y: base - h - 6 });
    u.txt(b.t, lab == null ? '' : lab);
    u.op(b.g, o);
  }

  /* ---------- 1. 시간 이동, 반전, 척도 (w2-2, wb-2) ---------- */
  /* S2 p.13 신호: 0~1 에서 1, 1~2 에서 1 에서 0 으로. 꼭짓점 t = 0, 1, 2 */
  const SH = { cx: 210, sc: 42, hv: 52, x0: 30, x1: 452 };
  const SHST = [[1, 0], [1, -2], [1, 1], [-1, 0], [-1, 1], [1.5, 0], [1.5, 1]];
  const shX = t => SH.cx + t * SH.sc;
  const shVert = (a, b) => [0, 1, 2].map(tau => (tau - b) / a);
  function shPath(p, base) {
    const y0 = base, y1 = base - SH.hv;
    const fwd = p[2] >= p[0];
    const pts = fwd
      ? [[SH.x0, y0], [shX(p[0]), y0], [shX(p[0]), y1], [shX(p[1]), y1], [shX(p[2]), y0], [SH.x1, y0]]
      : [[SH.x0, y0], [shX(p[2]), y0], [shX(p[1]), y1], [shX(p[0]), y1], [shX(p[0]), y0], [SH.x1, y0]];
    return pathD(pts);
  }
  function shLabel(a, b) {
    const A = a === 1 ? 't' : a === -1 ? '-t' : a === 1.5 ? '3t/2' : num(a, 2) + 't';
    return 'x(' + A + (b > 0 ? '+' + num(b, 2) : b < 0 ? '-' + num(-b, 2) : '') + ')';
  }
  V.add('sig.shift', {
    title: '밀고, 뒤집고, 늘이는 신호',
    w: 480, h: 300,
    dur: 1200,
    params: { a: 1, b: 0 },
    controls: [
      { key: 'b', type: 'range', label: '이동 b', min: -2, max: 2, step: 0.5, fmt: v => 'b = ' + num(v, 1) },
      { key: 'a', type: 'choice', label: 'a', options: [[1, '1'], [-1, '-1'], [1.5, '1.5']] },
    ],
    states: [
      { set: { a: 1, b: 0 }, cap: '원래 신호예요. 꼭짓점은 0, 1, 2이고 높이는 1이에요.' },
      { set: { a: 1, b: -2 }, tag: '이동', cap: 'x(t-2): 빼기는 오른쪽. 꼭짓점이 2, 3, 4로 가요.' },
      { set: { a: 1, b: 1 }, tag: '이동', cap: 'x(t+1): 더하기는 왼쪽. 꼭짓점은 -1, 0, 1이에요.' },
      { set: { a: -1, b: 0 }, tag: '반전', cap: 'x(-t): 좌우로 뒤집혀 꼭짓점이 0, -1, -2예요.' },
      { set: { a: -1, b: 1 }, tag: '반전과 이동', cap: 'x(-t+1): 뒤집고 오른쪽 1칸. 꼭짓점 1, 0, -1이에요.' },
      { set: { a: 1.5, b: 0 }, tag: '척도', cap: 'x(3t/2): 폭이 2에서 1.33으로 줄어요.' },
      { set: { a: 1.5, b: 1 }, tag: '척도와 이동', cap: 'x(3t/2+1): 이동량은 b가 아니라 b/a = 0.67이에요.' },
    ],
    build(ctx) {
      const g = ctx.g = {};
      const TOP = g.TOP = 108, BOT = g.BOT = 262;
      u.el(ctx.svg, 'text', { x: 30, y: 36, class: 'vz-tb' }, '원래 x(t)');
      axisH(ctx.svg, SH.x0, SH.x1, TOP, 't');
      axisH(ctx.svg, SH.x0, SH.x1, BOT, 't');
      for (let t = -3; t <= 5; t++) { tick(ctx.svg, shX(t), TOP, String(t)); tick(ctx.svg, shX(t), BOT, String(t)); }
      u.el(ctx.svg, 'path', { d: shPath([0, 1, 2], TOP), class: 'vz-curve' });
      g.topDots = [0, 1, 2].map(i => u.el(ctx.svg, 'circle', { cx: shX(i), cy: TOP - (i === 2 ? 0 : SH.hv), r: 5, class: 'vz-dot' }));
      g.curve = u.el(ctx.svg, 'path', { class: 'vz-curve tl' });
      g.dots = [0, 1, 2].map(() => u.el(ctx.svg, 'circle', { r: 6, class: 'vz-dot tl' }));
      g.dotT = [0, 1, 2].map(() => u.el(ctx.svg, 'text', { 'text-anchor': 'middle', class: 'vz-tt' }, ''));
      g.form = u.el(ctx.svg, 'text', { x: 30, y: 190, class: 'vz-tb' }, '');
      g.vert = u.el(ctx.svg, 'text', { x: SH.x1, y: 190, 'text-anchor': 'end', class: 'vz-ts' }, '');
      u.el(ctx.svg, 'text', { x: 30, y: 62, class: 'vz-ts' }, '높이 1, 폭 2');
    },
    draw(ctx, s, k) {
      const g = ctx.g, P = ctx.p;
      const pv = SHST[s > 0 ? s - 1 : 0];
      const p0 = shVert(pv[0], pv[1]), p1 = shVert(P.a, P.b);
      const kk = s > 0 ? u.ease(k) : 1;
      const p = [0, 1, 2].map(i => u.lerp(p0[i], p1[i], kk));
      u.set(g.curve, { d: shPath(p, g.BOT) });
      g.dots.forEach((c, i) => {
        u.set(c, { cx: shX(p[i]), cy: g.BOT - (i === 2 ? 0 : SH.hv) });
        u.set(g.dotT[i], { x: shX(p[i]), y: g.BOT - (i === 2 ? 0 : SH.hv) - 12 });
        u.txt(g.dotT[i], num(p[i], 2));
        u.op(c, 1); u.op(g.dotT[i], kk > 0.6 ? 1 : 0);
      });
      g.topDots.forEach(c => u.op(c, 1));
      u.txt(g.form, 'y(t) = ' + shLabel(P.a, P.b));
      u.txt(g.vert, '꼭짓점 ' + p1.map(x => num(x, 2)).join(', '));
      u.op(g.form, 1); u.op(g.vert, kk > 0.6 ? 1 : 0);
    },
  });

  /* ---------- 2. 주기 신호와 비주기 (w2-3, w2-6) ---------- */
  /* 이산 두 줄은 왼쪽 이름표와 값 글자가 겹치지 않게 x = 130 부터 그린다 */
  const PD = { x0: 60, dx0: 130, ax: 88, bx: 196, cx: 306, am: 34, bm: 30, cm: 26, T0: 2 * PI / 3, sc: 58, ds: 19 };
  V.add('sig.period', {
    title: '밀어도 똑같은 신호, 절대 안 맞는 신호',
    w: 480, h: 356,
    dur: 1300,
    states: [
      { cap: '주기 신호는 T만큼 밀어도 모양이 똑같아요.' },
      { tag: '연속', cap: 'cos 3t: 3t가 2pi 늘려면 t는 2pi/3 = 2.09 늘어요.' },
      { tag: '연속', cap: 'T0 = 2.09만큼 밀면 곡선이 딱 겹쳐요.' },
      { tag: '이산', cap: 'cos(pi n/4)는 정수 칸만 찍어요. 8칸마다 같아요.' },
      { tag: '이산', cap: '0번 칸과 8번 칸이 둘 다 1이에요. N0 = 8이에요.' },
      { tag: '비주기', cap: 'cos(n)은 0번 칸 1, 6번 칸 0.96. 안 맞아요.' },
      { cap: 'w0를 2pi로 나눈 값이 유리수일 때만 주기예요.' },
    ],
    build(ctx) {
      const g = ctx.g = {};
      const X = t => PD.x0 + t * PD.sc;
      g.X = X;
      u.el(ctx.svg, 'text', { x: 14, y: 28, class: 'vz-tb' }, 'cos 3t (연속시간)');
      axisH(ctx.svg, PD.x0, 446, PD.ax, 't');
      [[0, '0'], [PD.T0, '2.09'], [2 * PD.T0, '4.19'], [3 * PD.T0, '6.28']].forEach(([t, lab]) => tick(ctx.svg, X(t), PD.ax, lab));
      let d = '';
      for (let i = 0; i <= 200; i++) { const t = 6.6 * i / 200; d += (d ? ' L' : 'M') + u.r(X(t)) + ' ' + u.r(PD.ax - PD.am * Math.cos(3 * t)); }
      u.el(ctx.svg, 'path', { d, class: 'vz-curve' });
      let d1 = '';
      for (let i = 0; i <= 70; i++) { const t = PD.T0 * i / 70; d1 += (d1 ? ' L' : 'M') + u.r(X(t)) + ' ' + u.r(PD.ax - PD.am * Math.cos(3 * t)); }
      g.copy = u.el(ctx.svg, 'path', { d: d1, class: 'vz-curve tl' });
      g.win = u.el(ctx.svg, 'rect', { x: X(0), y: PD.ax - PD.am - 4, width: PD.T0 * PD.sc, height: 2 * PD.am + 8, rx: 4, class: 'vz-hl' });
      g.winT = u.el(ctx.svg, 'text', { x: X(PD.T0 / 2), y: PD.ax - PD.am - 12, 'text-anchor': 'middle', class: 'vz-tc' }, 'T0 = 2.09');
      /* 이산 cos(pi n/4) */
      g.gb = u.el(ctx.svg, 'g');
      const DX = n => PD.dx0 + n * PD.ds;
      g.DX = DX;
      u.el(g.gb, 'text', { x: 14, y: 150, class: 'vz-tb' }, 'cos(pi n/4)');
      u.el(g.gb, 'text', { x: 446, y: 150, 'text-anchor': 'end', class: 'vz-ta' }, 'w0/2pi = 1/8, N0 = 8');
      axisH(g.gb, PD.dx0 - 20, 446, PD.bx, 'n');
      [0, 4, 8, 12, 16].forEach(n => tick(g.gb, DX(n), PD.bx, String(n), 44));
      g.bst = [];
      for (let n = 0; n <= 16; n++) g.bst.push(stem(g.gb, 'tl'));
      g.bar8 = u.el(g.gb, 'line', { x1: DX(0), y1: PD.bx - PD.bm, x2: DX(8), y2: PD.bx - PD.bm, class: 'vz-e off' });
      g.bar8T = u.el(g.gb, 'text', { x: DX(4), y: 150, 'text-anchor': 'middle', class: 'vz-tc' }, '8칸 뒤 같은 값');
      /* 이산 cos(n) */
      g.gc = u.el(ctx.svg, 'g');
      u.el(g.gc, 'text', { x: 14, y: 264, class: 'vz-tb' }, 'cos(n)');
      g.cNote = u.el(g.gc, 'text', { x: 446, y: 264, 'text-anchor': 'end', class: 'vz-tc' }, '');
      axisH(g.gc, PD.dx0 - 20, 446, PD.cx, 'n');
      [0, 6, 12, 16].forEach(n => tick(g.gc, DX(n), PD.cx, String(n), 44));
      g.cst = [];
      for (let n = 0; n <= 16; n++) g.cst.push(stem(g.gc, ''));
    },
    draw(ctx, s, k) {
      const g = ctx.g;
      const w = at(s, k, 1);
      u.op(g.win, w); u.op(g.winT, seg(w, 0.5, 1));
      const mv = at(s, k, 2);
      u.set(g.copy, { transform: 'translate(' + u.r(PD.T0 * PD.sc * u.ease(mv)) + ' 0)' });
      u.op(g.copy, s >= 2 ? 1 : 0);
      const bo = at(s, k, 3);
      u.op(g.gb, bo > 0 ? 1 : 0);
      g.bst.forEach((st, n) => {
        const v = Math.cos(PI * n / 4);
        const on = seg(bo, n / 20, (n + 2) / 20);
        const mark = s >= 4 && (n === 0 || n === 8);
        stemCls(st, mark ? 'cr' : 'tl');
        putStem(st, g.DX(n), PD.bx, v, PD.bm, on, mark ? '1' : '');
      });
      const m8 = at(s, k, 4);
      u.set(g.bar8, { x2: u.lerp(g.DX(0), g.DX(8), seg(m8, 0, 0.8)) });
      u.op(g.bar8, m8 > 0 ? 1 : 0); u.op(g.bar8T, seg(m8, 0.6, 1));
      const co = at(s, k, 5);
      u.op(g.gc, co > 0 ? 1 : 0);
      g.cst.forEach((st, n) => {
        const v = Math.cos(n);
        const on = seg(co, n / 20, (n + 2) / 20);
        const mark = n === 0 || n === 6;
        stemCls(st, mark ? 'cr' : '');
        putStem(st, g.DX(n), PD.cx, v, PD.cm, on, mark ? num(v, 2) : '');
        /* 값 글자는 축 아래로 내린다 (오른쪽 결론 글과 겹치지 않게) */
        st.t.setAttribute('class', mark ? 'vz-ts vz-tc' : 'vz-ts');
        if (mark) u.set(st.t, { y: PD.cx + 18 });
      });
      u.txt(g.cNote, s >= 6 ? 'w0/2pi = 1/(2pi), 무리수라서 주기 없음' : '');
      u.op(g.cNote, at(s, k, 6));
    },
  });

  /* ---------- 3. 짝수와 홀수로 쪼개기 (w2-4) ---------- */
  /* w2-4 손계산 3: x[-1]=1, x[0]=2, x[1]=3 이면 xe = 2,2,2 와 xo = -1,0,1 */
  const EO = { vx: [1, 2, 3], base1: 112, base2: 252, sc: 20, dx: 30, lx: 120, rx: 350 };
  V.add('sig.evenodd', {
    title: '어떤 신호든 짝수 더하기 홀수',
    w: 480, h: 312,
    dur: 1200,
    states: [
      { cap: 'x[n]은 -1, 0, 1칸에서 1, 2, 3이에요.' },
      { tag: '뒤집기', cap: 'x[-n]: 좌우를 뒤집으면 3, 2, 1이에요.' },
      { tag: '짝수', cap: '더해서 반으로: (3+1)/2 = 2, 세 칸 모두 2예요.' },
      { tag: '홀수', cap: '빼서 반으로: (3-1)/2 = 1, 그래서 -1, 0, 1이에요.' },
      { tag: '확인', cap: '칸마다 더하면 1, 2, 3. 원래 x[n]이에요.' },
      { cap: '짝수는 거울 대칭, 홀수는 0번 칸이 0이에요.' },
    ],
    build(ctx) {
      const g = ctx.g = {};
      const P = (cx, base, title, cls) => {
        u.el(ctx.svg, 'text', { x: cx, y: base - 90, 'text-anchor': 'middle', class: 'vz-tb' }, title);
        axisH(ctx.svg, cx - 2.4 * EO.dx, cx + 2.4 * EO.dx, base, 'n');
        return { cx, base, st: [0, 1, 2].map(() => stem(ctx.svg, cls)) };
      };
      g.p1 = P(EO.lx, EO.base1, 'x[n]', '');
      g.p2 = P(EO.rx, EO.base1, 'x[-n] 뒤집기', 'cr');
      g.p3 = P(EO.lx, EO.base2, '짝수 부분 xe[n]', 'tl');
      g.p4 = P(EO.rx, EO.base2, '홀수 부분 xo[n]', 'am');
      [[g.p1, [-2, -1, 0, 1, 2]], [g.p2, [-2, -1, 0, 1, 2]], [g.p3, [-2, -1, 0, 1, 2]], [g.p4, [-2, 2]]].forEach(([p, ns]) => {
        ns.forEach(n => tick(ctx.svg, p.cx + n * EO.dx, p.base, String(n)));
      });
      g.sum = [0, 1, 2].map(i => u.el(ctx.svg, 'text', { x: 90 + i * 150, y: 298, 'text-anchor': 'middle', class: 'vz-tok' }, ''));
    },
    draw(ctx, s, k) {
      const g = ctx.g;
      const X = (p, n) => p.cx + n * EO.dx;
      g.p1.st.forEach((st, i) => {
        const n = i - 1;
        stemCls(st, s === 4 ? 'tok' : '');
        putStem(st, X(g.p1, n), g.p1.base, EO.vx[i], EO.sc, 1, String(EO.vx[i]));
      });
      const fl = at(s, k, 1);
      g.p2.st.forEach((st, i) => {
        const n = u.lerp(i - 1, -(i - 1), u.ease(fl));
        putStem(st, X(g.p2, n), g.p2.base, EO.vx[i], EO.sc, s >= 1 ? 1 : 0, String(EO.vx[i]));
      });
      const eo = at(s, k, 2), oo = at(s, k, 3);
      g.p3.st.forEach((st, i) => {
        const v = (EO.vx[i] + EO.vx[2 - i]) / 2;
        putStem(st, X(g.p3, i - 1), g.p3.base, v, EO.sc, seg(eo, i * 0.22, i * 0.22 + 0.5), num(v, 1));
      });
      g.p4.st.forEach((st, i) => {
        const v = (EO.vx[i] - EO.vx[2 - i]) / 2;
        putStem(st, X(g.p4, i - 1), g.p4.base, v, EO.sc, seg(oo, i * 0.22, i * 0.22 + 0.5), num(v, 1));
      });
      g.sum.forEach((t, i) => {
        const e = (EO.vx[i] + EO.vx[2 - i]) / 2, o = (EO.vx[i] - EO.vx[2 - i]) / 2;
        u.txt(t, num(e, 1) + (o < 0 ? ' - ' + num(-o, 1) : ' + ' + num(o, 1)) + ' = ' + num(EO.vx[i], 1));
        u.op(t, seg(at(s, k, 4), i * 0.2, i * 0.2 + 0.5));
      });
    },
  });

  /* ---------- 4. 오일러 공식: 도는 점과 cos 그림자 (wb-6, w2-5, w3-1) ---------- */
  /* wb-6 손계산 4: w0 = pi/2 이면 t = 0,1,2,3,4 에서 1, j, -1, -j, 1. T0 = 2pi/w0 = 4 */
  const EU = { cx: 112, cy: 150, r: 76, gx: 236, gsc: 54, gam: 60, base: 150 };
  const EUT = [0, 0.5, 1, 2, 3, 4, 4];
  const EUA = ['0', 'pi/4', 'pi/2', 'pi', '3pi/2', '2pi', '2pi'];
  V.add('sig.euler', {
    title: '원 위를 도는 점의 그림자가 cos',
    w: 480, h: 300,
    dur: 1300,
    states: [
      { cap: '반지름 1인 원 위의 점이에요. 각도 0에서 값은 1이에요.' },
      { tag: 'pi/4', cap: '45도에서 가로 0.71, 세로 0.71이에요.' },
      { tag: 'pi/2', cap: 't=1에서 각도 pi/2, 값은 j예요. 가로는 0이에요.' },
      { tag: 'pi', cap: 't=2에서 반 바퀴. e^jpi = -1, 왼쪽 끝이에요.' },
      { tag: '3pi/2', cap: 't=3에서 아래쪽. 값은 -j, 가로는 다시 0이에요.' },
      { tag: '한 바퀴', cap: 't=4에 제자리. T0 = 2pi/w0 = 4예요.' },
      { cap: '가로 위치를 시간 순서로 펴면 cos w0t 곡선이에요.' },
    ],
    build(ctx) {
      const g = ctx.g = {};
      u.el(ctx.svg, 'text', { x: 16, y: 34, class: 'vz-tb' }, '복소평면의 단위원');
      u.el(ctx.svg, 'text', { x: EU.gx, y: 34, class: 'vz-tb' }, '가로 위치를 시간 순서로');
      u.el(ctx.svg, 'circle', { cx: EU.cx, cy: EU.cy, r: EU.r, class: 'vz-axis' });
      u.el(ctx.svg, 'line', { x1: EU.cx - 96, y1: EU.cy, x2: EU.cx + 96, y2: EU.cy, class: 'vz-grid' });
      u.el(ctx.svg, 'line', { x1: EU.cx, y1: EU.cy - 96, x2: EU.cx, y2: EU.cy + 96, class: 'vz-grid' });
      u.el(ctx.svg, 'text', { x: EU.cx + 100, y: EU.cy - 8, 'text-anchor': 'end', class: 'vz-ts' }, 'cos');
      u.el(ctx.svg, 'text', { x: EU.cx + 8, y: EU.cy - 100, class: 'vz-ts' }, 'sin');
      g.cosL = u.el(ctx.svg, 'line', { class: 'vz-e cr' });
      g.sinL = u.el(ctx.svg, 'line', { class: 'vz-e tl' });
      g.gd1 = u.el(ctx.svg, 'line', { class: 'vz-e off' });
      g.gd2 = u.el(ctx.svg, 'line', { class: 'vz-e off' });
      g.arc = u.el(ctx.svg, 'path', { class: 'vz-curve mu' });
      g.dot = u.el(ctx.svg, 'circle', { r: 7, class: 'vz-dot' });
      g.ang = u.el(ctx.svg, 'text', { x: EU.cx, y: 274, 'text-anchor': 'middle', class: 'vz-ta' }, '');
      g.val = u.el(ctx.svg, 'text', { x: EU.cx, y: 252, 'text-anchor': 'middle', class: 'vz-tb' }, '');
      /* 오른쪽 cos 그래프 */
      axisH(ctx.svg, EU.gx - 8, 460, EU.base, 't');
      for (let t = 0; t <= 4; t++) tick(ctx.svg, EU.gx + t * EU.gsc, EU.base, String(t));
      u.el(ctx.svg, 'line', { x1: EU.gx, y1: EU.base - EU.gam, x2: 456, y2: EU.base - EU.gam, class: 'vz-grid' });
      u.el(ctx.svg, 'line', { x1: EU.gx, y1: EU.base + EU.gam, x2: 456, y2: EU.base + EU.gam, class: 'vz-grid' });
      u.el(ctx.svg, 'text', { x: EU.gx - 12, y: EU.base - EU.gam + 5, 'text-anchor': 'end', class: 'vz-ts' }, '1');
      u.el(ctx.svg, 'text', { x: EU.gx - 12, y: EU.base + EU.gam + 5, 'text-anchor': 'end', class: 'vz-ts' }, '-1');
      g.trace = u.el(ctx.svg, 'path', { class: 'vz-curve cr' });
      g.gbar = u.el(ctx.svg, 'line', { class: 'vz-e cr' });
      g.gdot = u.el(ctx.svg, 'circle', { r: 6, class: 'vz-dot cr' });
      g.gT = u.el(ctx.svg, 'text', { 'text-anchor': 'middle', class: 'vz-tc' }, '');
      g.name = u.el(ctx.svg, 'text', { x: 458, y: 274, 'text-anchor': 'end', class: 'vz-ta' }, '');
    },
    draw(ctx, s, k) {
      const g = ctx.g;
      const t0 = EUT[s > 0 ? s - 1 : 0], t1 = EUT[s];
      const t = s > 0 ? u.lerp(t0, t1, u.ease(k)) : 0;
      const th = PI / 2 * t;
      const px = EU.cx + EU.r * Math.cos(th), py = EU.cy - EU.r * Math.sin(th);
      u.set(g.dot, { cx: px, cy: py });
      u.set(g.cosL, { x1: EU.cx, y1: EU.cy, x2: px, y2: EU.cy });
      u.set(g.sinL, { x1: EU.cx, y1: EU.cy, x2: EU.cx, y2: py });
      u.set(g.gd1, { x1: px, y1: py, x2: px, y2: EU.cy });
      u.set(g.gd2, { x1: px, y1: py, x2: EU.cx, y2: py });
      u.op(g.gd1, 1); u.op(g.gd2, 1);
      const ar = 30, ae = Math.min(th, 2 * PI - 0.03), a1 = -ae;
      const big = ae > PI ? 1 : 0;
      u.set(g.arc, { d: 'M' + u.r(EU.cx + ar) + ' ' + EU.cy + ' A' + ar + ' ' + ar + ' 0 ' + big + ' 0 ' + u.r(EU.cx + ar * Math.cos(a1)) + ' ' + u.r(EU.cy + ar * Math.sin(a1)) });
      u.op(g.arc, th > 0.05 ? 1 : 0);
      u.txt(g.ang, '각도 ' + EUA[s] + ', t = ' + num(t1, 1));
      const c = Math.cos(th), sn = Math.sin(th);
      u.txt(g.val, '가로 ' + num(c, 2) + ', 세로 ' + num(sn, 2));
      u.op(g.ang, 1); u.op(g.val, 1);
      let d = '';
      for (let i = 0; i <= 120; i++) {
        const tt = 4 * i / 120;
        if (tt > t + 1e-9) break;
        d += (d ? ' L' : 'M') + u.r(EU.gx + tt * EU.gsc) + ' ' + u.r(EU.base - EU.gam * Math.cos(PI / 2 * tt));
      }
      u.set(g.trace, { d: d || 'M' + EU.gx + ' ' + u.r(EU.base - EU.gam) });
      g.trace.setAttribute('class', 'vz-curve' + (s === 6 ? '' : ' cr'));
      const gx = EU.gx + t * EU.gsc, gy = EU.base - EU.gam * c;
      u.set(g.gbar, { x1: gx, y1: EU.base, x2: gx, y2: gy });
      u.set(g.gdot, { cx: gx, cy: gy });
      u.set(g.gT, { x: u.clamp(gx, EU.gx + 16, 440), y: gy - 12 });
      u.txt(g.gT, 'cos = ' + num(c, 2));
      u.op(g.gbar, 1); u.op(g.gdot, 1); u.op(g.gT, 1);
      u.txt(g.name, s >= 6 ? 'cos w0t, w0 = pi/2' : '');
      u.op(g.name, at(s, k, 6));
    },
  });

  /* ---------- 5. 손뼉마다 메아리 도장 (wb-10 손계산 1, w3-2) ---------- */
  /* x = [1, 2, 1], h = [1, 1] 이면 y = [1, 3, 3, 1]. 길이 3+2-1 = 4, 합 4 x 2 = 8 */
  const IM = { x: [1, 2, 1], h: [1, 1], cols: [270, 320, 370, 420], rows: [128, 186, 244], sum: 318, sc: 15 };
  V.add('sig.stamp', {
    title: '손뼉마다 메아리 도장을 찍고 더하기',
    w: 480, h: 344,
    dur: 1300,
    states: [
      { cap: '입력 x는 1, 2, 1이고 메아리 h는 1, 1이에요.' },
      { tag: '쪼개기', cap: 'x를 칸마다 손뼉 3개로 쪼개요.' },
      { tag: '도장 1', cap: 'x[0]=1이니 0번 칸부터 1, 1을 찍어요.' },
      { tag: '도장 2', cap: 'x[1]=2니 1번 칸부터 2, 2를 찍어요.' },
      { tag: '도장 3', cap: 'x[2]=1이니 2번 칸부터 1, 1을 찍어요.' },
      { tag: '더하기', cap: '칸마다 세로로 더하면 1, 3, 3, 1이에요.' },
      { cap: '길이는 3+2-1 = 4칸, 합은 4 x 2 = 8이에요.' },
    ],
    build(ctx) {
      const g = ctx.g = {};
      u.el(ctx.svg, 'text', { x: 26, y: 34, class: 'vz-tb' }, '입력 x[n]');
      axisH(ctx.svg, 26, 120, 96, 'n');
      [0, 1, 2].forEach(n => tick(ctx.svg, 40 + n * 30, 96, String(n)));
      g.xs = [0, 1, 2].map(() => stem(ctx.svg, ''));
      u.el(ctx.svg, 'text', { x: 146, y: 34, class: 'vz-tb' }, '메아리 h[n]');
      axisH(ctx.svg, 146, 212, 96, 'n');
      [0, 1].forEach(n => tick(ctx.svg, 160 + n * 30, 96, String(n)));
      g.hs = [0, 1].map(() => stem(ctx.svg, 'tl'));
      IM.cols.forEach((x, i) => u.el(ctx.svg, 'text', { x, y: 48, 'text-anchor': 'middle', class: 'vz-ts' }, 'n=' + i));
      g.rowT = IM.rows.map((y, i) => u.el(ctx.svg, 'text', { x: 252, y: y - 10, 'text-anchor': 'end', class: 'vz-tb' }, '도장 ' + (i + 1)));
      g.rowA = IM.rows.map((y) => u.el(ctx.svg, 'text', { x: 252, y: y + 4, 'text-anchor': 'end', class: 'vz-ts' }, ''));
      g.cells = IM.rows.map(() => IM.cols.map(() => bar(ctx.svg, '')));
      u.el(ctx.svg, 'line', { x1: 252, y1: IM.sum - 58, x2: 456, y2: IM.sum - 58, class: 'vz-grid' });
      u.el(ctx.svg, 'text', { x: 252, y: IM.sum - 14, 'text-anchor': 'end', class: 'vz-tb' }, '합 y[n]');
      g.sumA = u.el(ctx.svg, 'text', { x: 252, y: IM.sum + 4, 'text-anchor': 'end', class: 'vz-ts' }, '');
      g.sums = IM.cols.map(() => bar(ctx.svg, 'tl'));
      g.arr = [0, 1, 2].map(() => u.arrow(ctx.svg, 'mu'));
      g.chk = u.el(ctx.svg, 'text', { x: 456, y: IM.sum + 22, 'text-anchor': 'end', class: 'vz-tok' }, '');
    },
    draw(ctx, s, k) {
      const g = ctx.g;
      g.xs.forEach((st, n) => {
        const hot = (s === 1 && k > n * 0.3) || s === n + 2;
        stemCls(st, hot ? 'cr' : '');
        putStem(st, 40 + n * 30, 96, IM.x[n], 18, 1, String(IM.x[n]));
      });
      g.hs.forEach((st, n) => putStem(st, 160 + n * 30, 96, IM.h[n], 18, 1, '1'));
      const rowOn = [at(s, k, 2), at(s, k, 3), at(s, k, 4)];
      g.cells.forEach((row, i) => {
        u.op(g.rowT[i], rowOn[i] > 0 ? 1 : 0);
        const arr = IM.cols.map((x, j) => (j >= i && j <= i + 1) ? IM.x[i] * IM.h[j - i] : 0);
        u.txt(g.rowA[i], '[' + arr.join(', ') + ']');
        u.op(g.rowA[i], seg(rowOn[i], 0.6, 1));
        row.forEach((b, j) => {
          const o = seg(rowOn[i], j * 0.16, j * 0.16 + 0.5);
          b.r.setAttribute('class', 'vz-bar' + (s === i + 2 ? ' cr' : ''));
          putBar(b, IM.cols[j], IM.rows[i], arr[j], IM.sc, o, String(arr[j]));
        });
      });
      const ys = [1, 3, 3, 1];
      const so = at(s, k, 5);
      g.sums.forEach((b, j) => {
        const o = seg(so, j * 0.2, j * 0.2 + 0.4);
        putBar(b, IM.cols[j], IM.sum, ys[j] * o, IM.sc, o > 0 ? 1 : 0, o > 0.6 ? String(ys[j]) : '');
      });
      u.txt(g.sumA, '[' + ys.join(', ') + ']');
      u.op(g.sumA, seg(so, 0.8, 1));
      g.arr.forEach((a, i) => {
        // 화살촉을 182 에서 멈춰요. 238 이면 줄 이름('도장 3')과 배열 글자 위에 화살촉이 얹혀요
        u.setArrow(a, [40 + i * 30, 110], [182, IM.rows[i] - 6], seg(at(s, k, 1), i * 0.25, i * 0.25 + 0.6));
        a.g.setAttribute('class', 'vz-arr' + (s === i + 2 ? '' : ' mu'));
      });
      u.txt(g.chk, s >= 6 ? '길이 3+2-1 = 4, 합 1+3+3+1 = 8 = 4 x 2' : '');
      u.op(g.chk, at(s, k, 6));
    },
  });

  /* ---------- 6. 뒤집고, 밀고, 곱하고, 더하기 (wb-10 손계산 2, w3-3) ---------- */
  const CV = { x0: 92, dx: 46, off: 2, r1: 96, r2: 178, r3: 250, r4: 330, sc: 22, ysc: 12, xv: [1, 2, 1], y: [1, 3, 3, 1] };
  const CVN = [0, 0, 0, 1, 2, 3, 4, 4];
  V.add('sig.conv', {
    title: '뒤집고 밀고 곱하고 더해서 한 칸씩',
    w: 480, h: 356,
    dur: 1300,
    states: [
      { cap: 'x[k]는 0, 1, 2칸에서 1, 2, 1이에요. h는 1, 1이에요.' },
      { tag: '뒤집기', cap: 'h[k]를 h[-k]로 뒤집어요. 이게 n=0 자리예요.' },
      { tag: 'n=0', cap: '겹친 칸은 k=0 하나, 곱은 1. y[0]=1이에요.' },
      { tag: 'n=1', cap: '오른쪽 1칸. 겹친 곱 1과 2를 더해 y[1]=3이에요.' },
      { tag: 'n=2', cap: '또 1칸. 곱 2와 1을 더해 y[2]=3이에요.' },
      { tag: 'n=3', cap: '겹친 칸은 k=2 하나뿐. y[3]=1이에요.' },
      { tag: 'n=4', cap: '더는 겹치지 않아서 y[4]=0이에요.' },
      { cap: 'y = 1, 3, 3, 1. 길이는 3+2-1 = 4칸이에요.' },
    ],
    build(ctx) {
      const g = ctx.g = {};
      const X = k => CV.x0 + (k + CV.off) * CV.dx;
      g.X = X;
      [[CV.r1, 'x[k]'], [CV.r2, ''], [CV.r3, '곱하기'], [CV.r4, 'y[n]']].forEach(([y, lab]) => {
        if (lab) u.el(ctx.svg, 'text', { x: 16, y: y - 10, class: 'vz-tb' }, lab);
        axisH(ctx.svg, CV.x0 - 12, 440, y, y === CV.r4 ? 'n' : 'k');
      });
      g.r2lab = u.el(ctx.svg, 'text', { x: 16, y: CV.r2 - 10, class: 'vz-tb' }, '');
      for (let k = -2; k <= 5; k++) tick(ctx.svg, X(k), CV.r1, String(k));
      for (let k = -2; k <= 5; k++) tick(ctx.svg, X(k), CV.r2, null);
      for (let k = -2; k <= 5; k++) tick(ctx.svg, X(k), CV.r3, null);
      for (let k = 0; k <= 4; k++) tick(ctx.svg, X(k), CV.r4, String(k));
      g.xs = []; g.ps = [];
      for (let k = -2; k <= 5; k++) { g.xs.push(stem(ctx.svg, '')); g.ps.push(stem(ctx.svg, 'tl')); }
      g.hs = [stem(ctx.svg, 'cr'), stem(ctx.svg, 'cr')];
      g.ys = [0, 1, 2, 3, 4].map(() => stem(ctx.svg, 'tl'));
      g.eq = u.el(ctx.svg, 'text', { x: 428, y: CV.r3 + 16, 'text-anchor': 'end', class: 'vz-tb' }, '');
      g.win = u.el(ctx.svg, 'rect', { y: CV.r1 - 56, height: CV.r3 - CV.r1 + 12, rx: 4, class: 'vz-hl' });
    },
    draw(ctx, s, k) {
      const g = ctx.g, X = g.X;
      const n = CVN[s], np = CVN[s > 0 ? s - 1 : 0];
      const nn = s > 0 ? u.lerp(np, n, u.ease(k)) : 0;
      /* 위 줄: 입력 */
      for (let i = 0; i < g.xs.length; i++) {
        const kk = i - 2;
        const v = kk >= 0 && kk <= 2 ? CV.xv[kk] : 0;
        const hot = s >= 2 && (kk === n || kk === n - 1) && v > 0;
        stemCls(g.xs[i], hot ? 'cr' : '');
        putStem(g.xs[i], X(kk), CV.r1, v, CV.sc, 1, v ? String(v) : '');
      }
      /* 가운데 줄: 뒤집어 민 메아리. s=0 은 아직 안 뒤집은 h[k] */
      let pA, pB;
      if (s === 0) { pA = 0; pB = 1; }
      else if (s === 1) { pA = 0; pB = u.lerp(1, -1, u.ease(k)); }
      else { pA = nn; pB = nn - 1; }
      const last = s === 7;   /* 마지막 장은 출력만 남긴다 */
      [pA, pB].forEach((p, i) => putStem(g.hs[i], X(p), CV.r2, 1, CV.sc, last ? 0 : 1, '1'));
      u.txt(g.r2lab, s === 0 ? 'h[k]' : 'h[n-k]');
      u.op(g.r2lab, last ? 0.3 : 1);
      /* 아래 줄: 곱한 값 */
      const show = last ? 0 : s >= 2 ? seg(k, 0.5, 0.85) : 0;
      let tot = 0;
      const terms = [];
      for (let i = 0; i < g.ps.length; i++) {
        const kk = i - 2;
        const xv = kk >= 0 && kk <= 2 ? CV.xv[kk] : 0;
        const hv = (kk === n || kk === n - 1) ? 1 : 0;
        const v = xv * hv;
        if (v) { tot += v; terms.push(String(v)); }
        putStem(g.ps[i], X(kk), CV.r3, v * show, CV.sc, v ? show : 0, v && show > 0.6 ? String(v) : '');
      }
      u.txt(g.eq, last ? 'y = [1, 3, 3, 1], 길이 3+2-1 = 4' : s >= 2 ? 'y[' + n + '] = ' + (terms.length ? terms.join(' + ') + ' = ' + tot : '0') : '');
      u.op(g.eq, last ? 1 : s >= 2 ? seg(k, 0.6, 0.9) : 0);
      /* 겹치는 칸 테두리 */
      u.set(g.win, { x: X(n - 1) - 16, width: X(n) - X(n - 1) + 32 });
      u.op(g.win, last ? 0 : s >= 2 ? seg(k, 0.4, 0.7) : 0);
      /* 맨 아래: 출력이 한 칸씩 */
      g.ys.forEach((st, i) => {
        const v = i < 4 ? CV.y[i] : 0;
        const done = s >= i + 3 ? 1 : s === i + 2 ? seg(k, 0.85, 1) : 0;
        putStem(st, X(i), CV.r4, v * done, CV.ysc, done, done > 0.5 ? String(v) : '');
      });
    },
  });

  /* ---------- 7. 컨볼루션 적분: 띠를 밀어 겹친 넓이 (w3-4 Example 2.6) ---------- */
  /* x(tau) = e^(-tau) (tau > 0), h(t) = u(t). y(t) = 1 - e^(-t). y(1) = 0.632 */
  const CI = { x0: 80, sc: 70, base: 152, am: 70, ybase: 282, yam: 70, lo: -1.5, hi: 3.4 };
  const CIT = [-1, 0.5, 1, 2, 3, 3];
  V.add('sig.convint', {
    title: '도장 띠를 밀어 겹친 넓이 재기',
    w: 480, h: 310,
    dur: 1300,
    params: { tt: -1 },
    controls: [{ key: 'tt', type: 'range', label: '민 위치', min: -1, max: 3, step: 0.5, fmt: v => 't = ' + num(v, 1) }],
    states: [
      { set: { tt: -1 }, cap: 't = -1: 겹치는 곳이 없어서 y = 0이에요.' },
      { set: { tt: 0.5 }, tag: 't=0.5', cap: '겹친 넓이 0.39가 그대로 y(0.5)예요.' },
      { set: { tt: 1 }, tag: 't=1', cap: 'Example 2.6: y(1) = 1 - 0.368 = 0.632예요.' },
      { set: { tt: 2 }, tag: 't=2', cap: 'y(2) = 0.87. 넓이가 아직 자라요.' },
      { set: { tt: 3 }, tag: 't=3', cap: 'y(3) = 0.95. 1에 다가가며 멈춰요.' },
      { set: { tt: 3 }, tag: '정리', cap: '식으로는 y(t) = 1 - e^(-t), t가 0보다 작으면 0이에요.' },
    ],
    build(ctx) {
      const g = ctx.g = {};
      const X = t => CI.x0 + (t - CI.lo) * CI.sc;
      g.X = X;
      u.el(ctx.svg, 'text', { x: 16, y: 34, class: 'vz-tb' }, '겹치기');
      u.el(ctx.svg, 'text', { x: 16, y: 52, class: 'vz-ts' }, 'x(tau)와 h(t-tau)');
      axisH(ctx.svg, CI.x0 - 6, 444, CI.base, 'tau');
      for (let t = -1; t <= 3; t++) tick(ctx.svg, X(t), CI.base, String(t));
      g.area = u.el(ctx.svg, 'path', { class: 'vz-box ok' });
      let d = '';
      for (let i = 0; i <= 120; i++) { const t = i / 120 * CI.hi; d += (d ? ' L' : 'M') + u.r(X(t)) + ' ' + u.r(CI.base - CI.am * Math.exp(-t)); }
      u.el(ctx.svg, 'path', { d: pathD([[X(CI.lo), CI.base], [X(0), CI.base]]), class: 'vz-curve' });
      u.el(ctx.svg, 'path', { d, class: 'vz-curve' });
      u.el(ctx.svg, 'text', { x: X(0.1), y: CI.base - CI.am - 8, class: 'vz-ta' }, 'x(tau) = e^(-tau)');
      g.step = u.el(ctx.svg, 'path', { class: 'vz-curve tl' });
      g.stepT = u.el(ctx.svg, 'text', { 'text-anchor': 'end', class: 'vz-tt' }, 'h(t-tau) = 1');
      g.edge = u.el(ctx.svg, 'line', { class: 'vz-e off' });
      g.areaT = u.el(ctx.svg, 'text', { 'text-anchor': 'middle', class: 'vz-tok' }, '');
      /* 아래: 출력 y(t) */
      u.el(ctx.svg, 'text', { x: 16, y: CI.ybase - 86, class: 'vz-tb' }, '출력 y(t)');
      axisH(ctx.svg, CI.x0 - 6, 444, CI.ybase, 't');
      for (let t = -1; t <= 3; t++) tick(ctx.svg, X(t), CI.ybase, String(t));
      u.el(ctx.svg, 'line', { x1: CI.x0, y1: CI.ybase - CI.yam, x2: 440, y2: CI.ybase - CI.yam, class: 'vz-grid' });
      u.el(ctx.svg, 'text', { x: CI.x0 - 12, y: CI.ybase - CI.yam + 5, 'text-anchor': 'end', class: 'vz-ts' }, '1');
      g.ycur = u.el(ctx.svg, 'path', { class: 'vz-curve tl' });
      g.ydot = u.el(ctx.svg, 'circle', { r: 6, class: 'vz-dot tl' });
      g.yT = u.el(ctx.svg, 'text', { 'text-anchor': 'middle', class: 'vz-tt' }, '');
      g.link = u.el(ctx.svg, 'line', { class: 'vz-e off' });
    },
    draw(ctx, s, k) {
      const g = ctx.g, X = g.X;
      const t0 = CIT[s > 0 ? s - 1 : 0];
      const t = s > 0 ? u.lerp(t0, ctx.p.tt, u.ease(k)) : ctx.p.tt;
      const tc = u.clamp(t, 0, CI.hi);
      /* 뒤집어 민 단위 계단: tau < t 에서 1 */
      const y1 = CI.base - CI.am;
      u.set(g.step, { d: pathD([[X(CI.lo), y1], [X(Math.max(t, CI.lo)), y1], [X(Math.max(t, CI.lo)), CI.base], [X(CI.hi), CI.base]]) });
      u.op(g.step, 1);
      u.set(g.stepT, { x: u.clamp(X(t) - 8, 210, 440), y: y1 - 30 });
      u.op(g.stepT, 1);
      u.set(g.edge, { x1: X(t), y1: CI.base + 8, x2: X(t), y2: y1 - 4 });
      u.op(g.edge, 1);
      /* 겹친 넓이 */
      let ad = 'M' + u.r(X(0)) + ' ' + CI.base;
      const nA = 40;
      for (let i = 0; i <= nA; i++) { const tt = tc * i / nA; ad += ' L' + u.r(X(tt)) + ' ' + u.r(CI.base - CI.am * Math.exp(-tt)); }
      ad += ' L' + u.r(X(tc)) + ' ' + CI.base + ' Z';
      u.set(g.area, { d: ad });
      const yv = t > 0 ? 1 - Math.exp(-t) : 0;
      u.op(g.area, t > 0.02 ? 1 : 0);
      u.set(g.areaT, { x: u.clamp(X(tc / 2), 120, 420), y: CI.base - 16 });
      u.txt(g.areaT, t > 0.02 ? '넓이 ' + num(yv, 2) : '');
      u.op(g.areaT, t > 0.05 ? 1 : 0);
      /* 출력 곡선 */
      let yd = 'M' + u.r(X(CI.lo)) + ' ' + CI.ybase + ' L' + u.r(X(Math.min(0, t))) + ' ' + CI.ybase;
      if (t > 0) for (let i = 0; i <= 60; i++) { const tt = t * i / 60; yd += ' L' + u.r(X(tt)) + ' ' + u.r(CI.ybase - CI.yam * (1 - Math.exp(-tt))); }
      u.set(g.ycur, { d: yd });
      u.op(g.ycur, 1);
      const gx = X(t), gy = CI.ybase - CI.yam * yv;
      u.set(g.ydot, { cx: gx, cy: gy });
      u.set(g.yT, { x: u.clamp(gx, 110, 420), y: gy - 12 });
      u.txt(g.yT, 'y(' + num(t, 1) + ') = ' + num(yv, 3));
      u.op(g.ydot, 1); u.op(g.yT, 1);
      u.set(g.link, { x1: gx, y1: CI.base + 10, x2: gx, y2: gy - 8 });
      u.op(g.link, s >= 1 ? 0.9 : 0.3);
    },
  });

  /* ---------- 8. 단위 계단과 단위 임펄스 (wb-9, w2-7) ---------- */
  /* 오른쪽 끝(x > 380)은 화살표와 이름표 자리로 비워 둔다 */
  const ST = { x0: 70, dx: 46, r1: 100, r2: 190, r3: 278, sc: 34 };
  V.add('sig.step', {
    title: '스위치와 손뼉은 서로를 만들어요',
    w: 480, h: 322,
    dur: 1200,
    states: [
      { cap: 'u[n]은 0번 칸부터 계속 1인 스위치예요.' },
      { tag: '한 칸 지연', cap: 'u[n-1]은 1번 칸부터 1이에요. 빼기는 오른쪽.' },
      { tag: '1차 차분', cap: '칸마다 빼요. 1-0 = 1은 0번 칸뿐이에요.' },
      { tag: '임펄스', cap: '남은 것이 델타 n이에요. 손뼉 한 번이죠.' },
      { tag: '누적 합', cap: '거꾸로 델타를 처음 칸부터 더해 가요. 합은 0이에요.' },
      { tag: '누적 합', cap: '0번 칸에서 1이 들어와 그 뒤로 계속 1이에요.' },
      { cap: '계단은 임펄스의 누적 합, 임펄스는 계단의 1차 차분이에요.' },
    ],
    build(ctx) {
      const g = ctx.g = {};
      const X = n => ST.x0 + (n + 2) * ST.dx;
      g.X = X;
      [[ST.r1, 'u[n]'], [ST.r2, 'u[n-1]'], [ST.r3, '차분']].forEach(([y, lab]) => {
        u.el(ctx.svg, 'text', { x: 8, y: y - 12, class: 'vz-tb' }, lab);
        axisH(ctx.svg, ST.x0 - 14, 366, y, 'n');
        for (let n = -2; n <= 4; n++) tick(ctx.svg, X(n), y, String(n), 16);
      });
      g.s1 = []; g.s2 = []; g.s3 = [];
      for (let n = -2; n <= 4; n++) { g.s1.push(stem(ctx.svg, 'tl')); g.s2.push(stem(ctx.svg, 'am')); g.s3.push(stem(ctx.svg, '')); }
      g.sub = [];
      for (let n = -2; n <= 4; n++) g.sub.push(u.el(ctx.svg, 'text', { x: X(n), y: ST.r3 - 58, 'text-anchor': 'middle', class: 'vz-ts' }, ''));
      g.name = u.el(ctx.svg, 'text', { x: 432, y: ST.r3 - 44, 'text-anchor': 'end', class: 'vz-ta' }, '');
      g.mark = u.el(ctx.svg, 'polygon', { class: 'vz-bar cr' });
      g.tot = u.el(ctx.svg, 'text', { x: 8, y: ST.r3 + 34, class: 'vz-tc' }, '');
      g.up = u.arrow(ctx.svg, 'tl');
      g.down = u.arrow(ctx.svg, 'cr');
      g.upT = u.el(ctx.svg, 'text', { x: 440, y: ST.r2 - 8, 'text-anchor': 'end', class: 'vz-tt' }, '');
      g.downT = u.el(ctx.svg, 'text', { x: 440, y: ST.r2 + 18, 'text-anchor': 'end', class: 'vz-tc' }, '');
    },
    draw(ctx, s, k) {
      const g = ctx.g, X = g.X;
      /* 누적 합 단계에서 계단을 다시 채우는 진행도 */
      const swp = s === 4 ? 0 : s === 5 ? seg(k, 0.1, 0.95) : s >= 6 ? 1 : -1;
      g.s1.forEach((st, i) => {
        const n = i - 2;
        const v = n >= 0 ? 1 : 0;
        let o = 1;
        if (swp >= 0) o = u.clamp(swp * 6.6 - i + 0.4, 0, 1);
        stemCls(st, swp >= 0 ? 'tok' : 'tl');
        putStem(st, X(n), ST.r1, v, ST.sc, o, v ? '1' : '0');
      });
      g.s2.forEach((st, i) => {
        const n = i - 2;
        const v = n >= 1 ? 1 : 0;
        putStem(st, X(n), ST.r2, v, ST.sc, at(s, k, 1), v ? '1' : '0');
      });
      const dif = at(s, k, 2);
      g.s3.forEach((st, i) => {
        const n = i - 2;
        const v = (n >= 0 ? 1 : 0) - (n >= 1 ? 1 : 0);
        const o = seg(dif, i * 0.12, i * 0.12 + 0.4);
        const hot = s >= 3 && v > 0;
        stemCls(st, hot ? 'cr' : '');
        putStem(st, X(n), ST.r3, v, ST.sc, o, v ? '1' : '0');
      });
      g.sub.forEach((t, i) => {
        const n = i - 2;
        const a = n >= 0 ? 1 : 0, b = n >= 1 ? 1 : 0;
        u.txt(t, a + '-' + b);
        u.op(t, s === 2 ? seg(dif, i * 0.12, i * 0.12 + 0.4) : 0);
      });
      u.txt(g.name, s >= 3 ? '= 델타 n (손뼉)' : '');
      u.op(g.name, at(s, k, 3));
      /* 누적 합 표시 */
      if (swp >= 0) {
        const nx = X(u.lerp(-2, 4.6, swp));
        // 눈금 숫자(r3 + 16 자리)보다 아래에 둬요. +10 이면 세모가 -2 눈금 위에 올라앉아요
        u.set(g.mark, { points: [nx, ST.r3 + 22, nx - 7, ST.r3 + 36, nx + 7, ST.r3 + 36].map(u.r).join(',') });
        u.op(g.mark, 1);
        u.txt(g.tot, '합 ' + (swp * 6.6 >= 2 ? '1' : '0'));
        u.op(g.tot, 1);
      } else { u.set(g.mark, { points: '0,0 0,0 0,0' }); u.op(g.mark, 0); u.txt(g.tot, ''); u.op(g.tot, 0); }
      const fin = at(s, k, 6);
      u.setArrow(g.up, [452, ST.r3 - 30], [452, ST.r1 + 30], fin);
      u.setArrow(g.down, [468, ST.r1 + 30], [468, ST.r3 - 30], fin);
      u.txt(g.upT, fin > 0.4 ? '누적 합' : '');
      u.txt(g.downT, fin > 0.4 ? '1차 차분' : '');
      u.op(g.upT, fin); u.op(g.downT, fin);
    },
  });
})();
