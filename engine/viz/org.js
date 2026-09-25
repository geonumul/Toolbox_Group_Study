/* 움직이는 개념 그림: 조직심리학 묶음. 틀은 viz.js, 설명은 README.md
   글과 이름은 work/org-psychology/notes/slides_w2.json, slides_w3.json 과 rules/용어사전.json 에서 가져왔다.
   강의 자료에 없는 숫자(사람 수, 연구 개수)는 자리표 캡션에 예시라고 적는다. */
(function () {
  'use strict';
  const V = window.SDTViz;
  if (!V) return;
  const u = V.u;
  const at = u.at, seg = u.seg;

  /* 글자 하나. anchor 기본은 가운데 */
  function t1(parent, x, y, cls, s, anchor) {
    return u.el(parent, 'text', { x: x, y: y, class: cls, 'text-anchor': anchor || 'middle' }, s == null ? '' : s);
  }
  /* 이름표 상자 {g, r, t, s(작은 글씨)} */
  function tag(parent, x, y, w, h, label, small) {
    const g = u.el(parent, 'g');
    const r = u.el(g, 'rect', { x: x - w / 2, y: y - h / 2, width: w, height: h, rx: 7, class: 'vz-box' });
    const t = t1(g, x, y + (small ? -3 : 5), 'vz-tb', label);
    const s = t1(g, x, y + 16, 'vz-ts', small || '');
    return { g: g, r: r, t: t, s: s, x: x, y: y };
  }
  const boxCls = (b, c) => b.r.setAttribute('class', 'vz-box' + (c ? ' ' + c : ''));

  /* ---------- 1. 유인-선발-퇴출(ASA) 순환 (w3-3, p.6 그림과 p.7 만화) ---------- */
  /* 자리마다 사람이 서는 곳. i 는 그 자리에서 몇 번째인지 */
  const ASA_SLOT = {
    start: i => [150 + i * 14, 30],
    start2: i => [150 + i * 14, 30],
    hide: i => [150 + i * 14, 30],
    g1: i => [172 + i * 14, 84],
    g2: i => [190 + i * 14, 133],
    g3: i => [196 + i * 14, 182],
    org: i => [176 + i * 14, 232],
    away: i => [330 + i * 14, 30],
    rej: i => [330 + i * 14, 133],
    out: i => [330 + i * 14, 182],
  };
  const ASA_OP = { start: 1, start2: 1, hide: 0, g1: 1, g2: 1, g3: 1, org: 1, away: 0.3, rej: 0.3, out: 0.3 };
  /* 아직 남아 있는 사람으로 셀 자리 */
  const ASA_IN = { start: 1, start2: 1, hide: 0, g1: 1, g2: 1, g3: 1, org: 1, away: 0, rej: 0, out: 0 };
  const ASA_WHO = (function () {
    const stay = ['start', 'g1', 'g2', 'g3', 'org', 'org', 'org', 'org'];
    const quit = ['start', 'g1', 'g2', 'out', 'out', 'out', 'out', 'out'];
    const nope = ['start', 'g1', 'rej', 'rej', 'rej', 'rej', 'rej', 'rej'];
    const gone = ['start', 'away', 'away', 'away', 'away', 'away', 'away', 'away'];
    const late = ['hide', 'hide', 'hide', 'hide', 'hide', 'start2', 'org', 'org'];
    const L = [];
    for (let i = 0; i < 5; i++) L.push([0, stay]);   // 조직 문화와 비슷한 사람
    L.push([1, quit]);                               // 뽑혔지만 안 맞아 나가는 사람
    L.push([1, nope]); L.push([1, nope]);            // 끌려왔지만 안 뽑히는 사람
    L.push([2, gone]); L.push([2, gone]);            // 아예 매력을 못 느끼는 사람
    for (let i = 0; i < 3; i++) L.push([0, late]);   // 다음 라운드에 오는 비슷한 사람
    return L;
  })();
  V.add('org.asa', {
    title: '유인, 선발, 퇴출이 한 바퀴 돌 때',
    w: 480, h: 300,
    dur: 1300,
    states: [
      { cap: '지원자 10명이 있어요. 성격과 가치가 저마다 달라요.' },
      { tag: '유인', cap: '자신의 성격과 일치하는 문화를 가진 조직에 매력을 느껴요.' },
      { tag: '선발', cap: '조직은 유사한 성격과 가치를 지닌 사람을 선발해요.' },
      { tag: '퇴출', cap: '문화가 자신과 부합하지 않으면 이직하는 경향이 있어요.' },
      { cap: '남은 사람끼리는 비슷해요. 왼쪽 아래 숫자를 보세요.' },
      { tag: '다음 라운드', cap: '새로 뽑을 때도 비슷한 사람이 끌려와요.' },
      { cap: '또 비슷한 사람만 남아요. 비슷 8명, 다름 0명이에요.' },
      { cap: '구성원이 가치 태도, 성격 등에서 상당히 동질성을 가져요.' },
    ],
    build(ctx) {
      const g = ctx.g = {};
      g.gates = [
        u.el(ctx.svg, 'polygon', { points: '150,52 310,52 296,96 164,96', class: 'vz-box' }),
        u.el(ctx.svg, 'polygon', { points: '164,102 296,102 282,146 178,146', class: 'vz-box' }),
        u.el(ctx.svg, 'polygon', { points: '178,152 282,152 270,196 190,196', class: 'vz-box' }),
      ];
      g.org = u.el(ctx.svg, 'rect', { x: 150, y: 208, width: 160, height: 40, rx: 6, class: 'vz-box' });
      t1(ctx.svg, 20, 74, 'vz-tb', '유인', 'start');
      t1(ctx.svg, 20, 92, 'vz-ts', 'Attraction', 'start');
      t1(ctx.svg, 20, 124, 'vz-tb', '선발', 'start');
      t1(ctx.svg, 20, 142, 'vz-ts', 'Selection', 'start');
      t1(ctx.svg, 20, 174, 'vz-tb', '퇴출', 'start');
      t1(ctx.svg, 20, 192, 'vz-ts', 'Attrition', 'start');
      t1(ctx.svg, 152, 202, 'vz-tb', '조직의 동질화', 'start');
      t1(ctx.svg, 144, 35, 'vz-ts', '지원자', 'end');
      g.awayT = t1(ctx.svg, 358, 35, 'vz-ts', '안 끌려요', 'start');
      g.rejT = t1(ctx.svg, 358, 138, 'vz-ts', '안 뽑혀요', 'start');
      g.outT = t1(ctx.svg, 358, 187, 'vz-ts', '나가요', 'start');
      t1(ctx.svg, 20, 224, 'vz-ts', '남은 사람 (예시)', 'start');
      g.same = t1(ctx.svg, 20, 248, 'vz-ta', '', 'start');
      g.diff = t1(ctx.svg, 20, 272, 'vz-tm', '', 'start');
      g.cyc = u.el(ctx.svg, 'path', { d: 'M200 250 V286 H8 V66 H140', class: 'vz-e on' });
      g.cycH = u.el(ctx.svg, 'polygon', { points: '150,66 141,61 141,71', class: 'vz-bar' });
      g.cycT = t1(ctx.svg, 216, 282, 'vz-ta', '자기강화적 ASA 순환', 'start');
      const N = ASA_WHO[0][1].length;
      g.P = ASA_WHO.map(w => ({ t: w[0], path: w[1], xy: [], op: [] }));
      for (let s = 0; s < N; s++) {
        const cnt = {};
        g.P.forEach(p => {
          const sl = p.path[s];
          const i = (cnt[sl] = (cnt[sl] == null ? 0 : cnt[sl] + 1));
          p.xy[s] = ASA_SLOT[sl](i);
          p.op[s] = ASA_OP[sl];
        });
      }
      g.P.forEach(p => { p.c = u.el(ctx.svg, 'circle', { r: 7, class: 'vz-dot' + (p.t === 1 ? ' am' : p.t === 2 ? ' cr' : '') }); });
    },
    draw(ctx, s, k) {
      const g = ctx.g, p0 = Math.max(0, s - 1), mv = seg(k, 0, 0.85);
      g.P.forEach(p => {
        const q = u.pt(p.xy[p0], p.xy[s], mv);
        u.set(p.c, { cx: q[0], cy: q[1] });
        u.op(p.c, u.lerp(p.op[p0], p.op[s], mv));
      });
      const count = st => {
        let a = 0, b = 0;
        g.P.forEach(p => { if (!ASA_IN[p.path[st]]) return; if (p.t === 0) a++; else b++; });
        return [a, b];
      };
      const A = count(p0), B = count(s);
      u.txt(g.same, '비슷 ' + Math.round(u.lerp(A[0], B[0], mv)) + '명');
      u.txt(g.diff, '다름 ' + Math.round(u.lerp(A[1], B[1], mv)) + '명');
      const cls = [s === 1 || s === 5 ? ' on' : '', s === 2 || s === 6 ? ' tl' : '', s === 3 ? ' cr' : ''];
      g.gates.forEach((el, i) => el.setAttribute('class', 'vz-box' + cls[i]));
      g.org.setAttribute('class', 'vz-box' + (s >= 4 ? ' ok' : ''));
      u.op(g.awayT, s >= 1 ? 1 : 0);
      u.op(g.rejT, s >= 2 ? 1 : 0);
      u.op(g.outT, s >= 3 ? 1 : 0);
      const cy = at(s, k, 4);
      u.op(g.cyc, cy); u.op(g.cycH, cy); u.op(g.cycT, cy);
    },
  });

  /* ---------- 2. 호손 연구의 네 갈래와 이름이 붙은 때 (w2-4, p.7~9) ---------- */
  const HAW_X = [152, 212, 272, 332, 392, 452];
  const HAW_Y = [200, 174, 156, 156, 130, 106];
  const HAW_ON = [1, 1, 2, 3, 5, 6];
  const HAW_LAB = ['처음', '밝게', '어둡게', '성과급', '작업조건', '인터뷰'];
  const HAW_HEAD = [
    '어떻게 효율성을 높일 것인가?',
    '가설: 밝을수록 작업 효율이 높다',
    '조명 가설 기각',
    '가설: 성과급을 주면 더 만든다',
    '성과급 가설도 기각',
    '작업 조건을 바꿔 봐요',
    '심리적 조건이 더 셌어요',
    '이름은 몇십 년 뒤에 붙었어요',
  ];
  V.add('org.hawthorne', {
    title: '호손 연구: 가설이 두 번 기각되는 동안',
    w: 480, h: 300,
    dur: 1300,
    states: [
      { tag: '1924', cap: 'Western Electric 의 호손 공장, 하버드 연구진과 함께예요.' },
      { tag: '조명', cap: '밝은 전구가 어두운 전구보다 나을 것이라고 봤어요.' },
      { tag: '조명', cap: '밝게 해도 늘고 어둡게 해도 늘어요. 조명 가설은 기각이에요.' },
      { tag: '성과급', cap: '작업량에 따라 돈을 더 줬는데 생산이 늘지 않아요.' },
      { tag: '규범', cap: '사람들끼리 비공식적으로 생산량을 정해 뒀어요.' },
      { tag: '작업 조건', cap: '좋아하는 4명과 한 조로 시간, 휴식, 간식, 임금을 바꿔요.' },
      { tag: '인터뷰', cap: '2~3년간 한 명씩 물어요. 우리는 선택된 사람들이야.' },
      { tag: '이름', cap: '호손 효과라는 이름은 몇십 년 뒤 자료를 다시 보며 붙었어요.' },
    ],
    build(ctx) {
      const g = ctx.g = {};
      g.hd = u.el(ctx.svg, 'rect', { x: 150, y: 20, width: 300, height: 32, rx: 6, class: 'vz-box' });
      g.hdT = t1(ctx.svg, 300, 41, 'vz-tb', '');
      g.lamp = u.el(ctx.svg, 'circle', { cx: 58, cy: 74, r: 22, class: 'vz-box' });
      t1(ctx.svg, 58, 108, 'vz-tb', '조명');
      g.lampT = t1(ctx.svg, 58, 130, 'vz-ta', '');
      g.men = [0, 1, 2, 3, 4].map(i => u.el(ctx.svg, 'circle', { cx: 24 + i * 20, cy: 172, r: 7, class: 'vz-dot' }));
      t1(ctx.svg, 58, 196, 'vz-ts', '작업자');
      g.itv = t1(ctx.svg, 58, 222, 'vz-tt', '한 명씩 인터뷰');
      g.itv2 = t1(ctx.svg, 58, 242, 'vz-ts', '2~3년간');
      u.el(ctx.svg, 'line', { x1: 120, y1: 56, x2: 120, y2: 236, class: 'vz-axis' });
      u.el(ctx.svg, 'line', { x1: 120, y1: 236, x2: 470, y2: 236, class: 'vz-axis' });
      /* 머리 상자(x 150~450, y 20~52)에 꼬리가 가리지 않게 오른쪽 끝을 146 에 맞춘다 */
      t1(ctx.svg, 146, 52, 'vz-ts', '생산량', 'end');
      g.norm = u.el(ctx.svg, 'line', { x1: 140, y1: 156, x2: 462, y2: 156, class: 'vz-e off' });
      g.normT = t1(ctx.svg, 300, 148, 'vz-tc', '집단이 정한 생산량 규범');
      g.seg = [0, 1, 2, 3, 4].map(i => u.el(ctx.svg, 'line', { class: 'vz-e' + (i === 2 ? ' cr' : ' on') }));
      g.pt = HAW_X.map((x, i) => u.el(ctx.svg, 'circle', { cx: x, cy: HAW_Y[i], r: 6, class: 'vz-dot' }));
      g.lab = HAW_X.map((x, i) => t1(ctx.svg, x, 256, 'vz-ts', HAW_LAB[i]));
      g.end = u.el(ctx.svg, 'rect', { x: 120, y: 262, width: 350, height: 34, rx: 6, class: 'vz-box am' });
      g.endT = t1(ctx.svg, 295, 284, 'vz-tb', '관심을 받으면 평소와 다르게 행동한다');
    },
    draw(ctx, s, k) {
      const g = ctx.g;
      u.txt(g.hdT, HAW_HEAD[s]);
      g.hd.setAttribute('class', 'vz-box' + (s === 2 || s === 4 ? ' cr' : s === 6 ? ' ok' : s === 7 ? ' am' : ''));
      g.lamp.setAttribute('class', 'vz-box' + (s === 1 ? ' am' : s === 2 ? ' off' : ''));
      u.txt(g.lampT, s === 1 ? '밝게' : s === 2 ? '어둡게' : '');
      u.op(g.lampT, s === 1 || s === 2 ? 1 : 0);
      g.men.forEach(m => m.setAttribute('class', 'vz-dot' + (s === 5 ? ' tl' : '')));
      u.op(g.itv, s === 6 ? seg(k, 0, 0.4) : s === 7 ? 1 : 0);
      u.op(g.itv2, s === 6 ? seg(k, 0.2, 0.6) : s === 7 ? 1 : 0);
      g.pt.forEach((c, i) => u.op(c, HAW_ON[i] < s ? 1 : HAW_ON[i] === s ? seg(k, 0.2, 0.8) : 0));
      g.seg.forEach((l, i) => {
        const w = HAW_ON[i + 1];
        const p = w < s ? 1 : w === s ? seg(k, 0, 0.9) : 0;
        u.draw(l, [HAW_X[i], HAW_Y[i]], [HAW_X[i + 1], HAW_Y[i + 1]], p);
      });
      g.lab.forEach((t, i) => u.op(t, HAW_ON[i] <= s ? 1 : 0));
      const nm = at(s, k, 4);
      u.op(g.norm, nm); u.op(g.normT, nm);
      const e = at(s, k, 7);
      u.op(g.end, e); u.op(g.endT, e);
    },
  });

  /* ---------- 3. Feldman 의 사회화 단계 (w3-5, p.9) ---------- */
  V.add('org.feldman', {
    title: 'Feldman 의 사회화 단계를 한 칸씩',
    w: 480, h: 300,
    dur: 1200,
    states: [
      { cap: '가운데 빨간 선이 입사 시점이에요. 왼쪽이 입사 전이에요.' },
      { tag: '선행 사회화', cap: '입사 전 모집 과정에서 정보를 모으고 적합성을 평가해요.' },
      { tag: '대면', cap: '들어와서 직무와 조직의 현실적인 모습을 보기 시작해요.' },
      { tag: '변화와 습득', cap: '조직문화에 적응해 편안해지고 역량을 충분히 발휘해요.' },
      { tag: '행동적 결과', cap: '수행, 자발적 혁신, 동료와 협력, 이직이 이 칸이에요.' },
      { tag: '정서적 결과', cap: '태도, 동기부여, 직무몰입, 조직 내포성이 이 칸이에요.' },
      { cap: '앞 셋은 과정, 뒤 둘은 결과예요. Feldman, 1981.' },
    ],
    build(ctx) {
      const g = ctx.g = {};
      u.el(ctx.svg, 'line', { x1: 150, y1: 44, x2: 150, y2: 150, class: 'vz-e cr' });
      t1(ctx.svg, 150, 38, 'vz-tc', '입사');
      t1(ctx.svg, 74, 38, 'vz-ts', '입사 전');
      t1(ctx.svg, 226, 38, 'vz-ts', '입사 후');
      g.box = [
        { r: u.el(ctx.svg, 'rect', { x: 10, y: 56, width: 126, height: 48, rx: 6, class: 'vz-box' }), x: 73 },
        { r: u.el(ctx.svg, 'rect', { x: 164, y: 56, width: 132, height: 48, rx: 6, class: 'vz-box' }), x: 230 },
        { r: u.el(ctx.svg, 'rect', { x: 324, y: 56, width: 146, height: 48, rx: 6, class: 'vz-box' }), x: 397 },
      ];
      t1(ctx.svg, 73, 86, 'vz-tb', '선행 사회화');
      t1(ctx.svg, 230, 86, 'vz-tb', '대면');
      t1(ctx.svg, 397, 86, 'vz-tb', '변화와 습득');
      g.det = [
        [t1(ctx.svg, 73, 124, 'vz-ts', '입사 전 정보 수집'), t1(ctx.svg, 73, 142, 'vz-ts', 'RJP, 인턴십')],
        [t1(ctx.svg, 230, 124, 'vz-ts', '직무와 조직의 현실을 봄'), t1(ctx.svg, 230, 142, 'vz-ts', '역할 학습, 가족과의 갈등')],
        [t1(ctx.svg, 397, 124, 'vz-ts', '편안함, 역할 파악'), t1(ctx.svg, 397, 142, 'vz-ts', '역량을 충분히 발휘')],
      ];
      g.ar = u.arrow(ctx.svg, 'tl');
      g.down = u.arrow(ctx.svg);
      g.res = [
        { r: u.el(ctx.svg, 'rect', { x: 16, y: 178, width: 212, height: 66, rx: 6, class: 'vz-box' }), x: 122 },
        { r: u.el(ctx.svg, 'rect', { x: 252, y: 178, width: 212, height: 66, rx: 6, class: 'vz-box' }), x: 358 },
      ];
      g.resT = [
        [t1(ctx.svg, 122, 202, 'vz-tb', '행동적 결과'), t1(ctx.svg, 122, 222, 'vz-ts', '성공적 수행, 동료와 협력'), t1(ctx.svg, 122, 240, 'vz-ts', '자발적 혁신, 이직')],
        [t1(ctx.svg, 358, 202, 'vz-tb', '정서적 결과'), t1(ctx.svg, 358, 222, 'vz-ts', '태도, 동기부여, 직무몰입'), t1(ctx.svg, 358, 240, 'vz-ts', '조직 내포성')],
      ];
      g.extra = [
        t1(ctx.svg, 122, 258, 'vz-ta', '수호형 vs 혁신형'),
        t1(ctx.svg, 358, 258, 'vz-ts', '연결된 느낌, 합치, 잃을 느낌'),
      ];
      g.who = u.el(ctx.svg, 'circle', { r: 8, class: 'vz-dot' });
      g.note = t1(ctx.svg, 240, 282, 'vz-ta', '앞 셋은 과정, 뒤 둘은 결과예요');
      t1(ctx.svg, 472, 296, 'vz-ts', 'Feldman, 1981', 'end');
    },
    draw(ctx, s, k) {
      const g = ctx.g;
      const spot = [[30, 80], [73, 80], [230, 80], [397, 80], [397, 80], [397, 80], [397, 80]];
      const q = u.pt(spot[Math.max(0, s - 1)], spot[s], seg(k, 0, 0.8));
      u.set(g.who, { cx: q[0], cy: q[1] });
      u.op(g.who, s <= 3 ? 1 : 0.35);
      g.box.forEach((b, i) => {
        const on = s === i + 1;
        b.r.setAttribute('class', 'vz-box' + (on ? ' on' : s > i + 1 ? ' ok' : ''));
        const o = i + 1 < s ? 1 : i + 1 === s ? seg(k, 0.3, 0.9) : 0;
        g.det[i].forEach(t => u.op(t, o));
      });
      u.setArrow(g.ar, [298, 80], [320, 80], at(s, k, 3));
      u.setArrow(g.down, [240, 152], [240, 172], at(s, k, 4));
      g.res.forEach((b, i) => {
        const w = i + 4;
        const on = s === w;
        b.r.setAttribute('class', 'vz-box' + (on ? (i ? ' tl' : ' am') : s > w ? ' ok' : ''));
        const o = w < s ? 1 : w === s ? seg(k, 0.3, 0.9) : 0;
        g.resT[i].forEach(t => u.op(t, o));
        u.op(g.extra[i], w < s ? 0.6 : w === s ? seg(k, 0.6, 1) : 0);
      });
      u.op(g.note, at(s, k, 6));
    },
  });

  /* ---------- 4. 서류 서랍 효과 (w2-9, p.30) ---------- */
  const FD_X = [58, 76, 94, 112, 152, 182, 208, 236, 260, 286];
  const FD_NULL = 4;                    // 왼쪽 네 개가 결과가 안 나온 연구
  const FD_MEAN_ALL = FD_X.reduce((a, b) => a + b, 0) / FD_X.length;
  const FD_MEAN_PUB = FD_X.slice(FD_NULL).reduce((a, b) => a + b, 0) / (FD_X.length - FD_NULL);
  V.add('org.filedrawer', {
    title: '서랍에 들어간 연구와 치우친 평균',
    w: 480, h: 300,
    dur: 1300,
    states: [
      { cap: '같은 주제 연구 10개예요. 가로 자리가 효과의 크기예요.' },
      { tag: '출판', cap: '결과가 뚜렷한 연구 6개는 학술지에 실려요.' },
      { tag: '서랍', cap: '결과가 안 나온 연구 4개는 서랍으로 들어가요.' },
      { tag: '메타분석', cap: '메타분석은 출판된 연구만 모아요. 서랍은 못 봐요.' },
      { cap: '그래서 평균이 효과가 큰 쪽으로 치우쳐요.' },
      { cap: '이름은 서류(file) 서랍(drawer) 효과예요. 순서를 바꾸지 않아요.' },
    ],
    build(ctx) {
      const g = ctx.g = {};
      u.el(ctx.svg, 'line', { x1: 36, y1: 210, x2: 306, y2: 210, class: 'vz-axis' });
      t1(ctx.svg, 36, 232, 'vz-ts', '효과 없음', 'start');
      t1(ctx.svg, 306, 232, 'vz-ts', '효과 큼', 'end');
      t1(ctx.svg, 36, 178, 'vz-ts', '연구 10개 (예시)', 'start');
      g.shelf = u.el(ctx.svg, 'rect', { x: 324, y: 30, width: 148, height: 68, rx: 6, class: 'vz-box' });
      t1(ctx.svg, 408, 52, 'vz-tb', '출판된 연구');
      g.shelfN = t1(ctx.svg, 332, 52, 'vz-ta', '', 'start');
      g.meta = u.el(ctx.svg, 'rect', { x: 324, y: 128, width: 148, height: 52, rx: 6, class: 'vz-box tl' });
      g.metaT = [t1(ctx.svg, 398, 150, 'vz-tb', '메타분석'), t1(ctx.svg, 398, 170, 'vz-ts', '출판된 것만 모음')];
      g.draw1 = u.el(ctx.svg, 'rect', { x: 324, y: 196, width: 148, height: 74, rx: 6, class: 'vz-box off' });
      t1(ctx.svg, 408, 218, 'vz-tb', '서랍');
      g.drawN = t1(ctx.svg, 332, 218, 'vz-tm', '', 'start');
      g.drawT = t1(ctx.svg, 398, 264, 'vz-tm', '출판 안 됨');
      g.up = u.arrow(ctx.svg, 'tl');
      g.side = u.arrow(ctx.svg, 'mu');
      g.shift = u.arrow(ctx.svg);
      g.mAll = u.el(ctx.svg, 'polygon', { points: [FD_MEAN_ALL, 206, FD_MEAN_ALL - 8, 220, FD_MEAN_ALL + 8, 220].map(u.r).join(','), class: 'vz-bar mu' });
      g.mAllT = t1(ctx.svg, FD_MEAN_ALL, 250, 'vz-tm', '모든 연구 평균');
      g.mPub = u.el(ctx.svg, 'polygon', { points: [FD_MEAN_PUB, 206, FD_MEAN_PUB - 8, 220, FD_MEAN_PUB + 8, 220].map(u.r).join(','), class: 'vz-bar' });
      g.mPubT = t1(ctx.svg, FD_MEAN_PUB, 272, 'vz-ta', '출판된 것만 평균');
      g.name = t1(ctx.svg, 170, 292, 'vz-ta', '서류(file) 서랍(drawer) 효과');
      g.S = FD_X.map((x, i) => {
        const nul = i < FD_NULL;
        const path = nul ? ['axis', 'axis', 'box', 'box', 'box', 'box'] : ['axis', 'pub', 'pub', 'pub', 'pub', 'pub'];
        const home = [x, 210];
        const seat = nul ? [346 + i * 22, 244] : [336 + (i - FD_NULL) * 20, 78];
        return { c: u.el(ctx.svg, 'circle', { cx: x, cy: 210, r: 8, class: 'vz-dot' + (nul ? ' mu' : '') }), path: path, home: home, seat: seat };
      });
    },
    draw(ctx, s, k) {
      const g = ctx.g, p0 = Math.max(0, s - 1), mv = seg(k, 0, 0.85);
      let pub = 0, box = 0, pub0 = 0, box0 = 0;
      g.S.forEach(st => {
        const a = st.path[p0] === 'axis' ? st.home : st.seat;
        const b = st.path[s] === 'axis' ? st.home : st.seat;
        const q = u.pt(a, b, mv);
        u.set(st.c, { cx: q[0], cy: q[1] });
        if (st.path[s] === 'pub') pub++;
        if (st.path[s] === 'box') box++;
        if (st.path[p0] === 'pub') pub0++;
        if (st.path[p0] === 'box') box0++;
      });
      u.txt(g.shelfN, Math.round(u.lerp(pub0, pub, mv)) + '개');
      u.op(g.shelfN, s >= 1 ? 1 : 0);
      u.txt(g.drawN, Math.round(u.lerp(box0, box, mv)) + '개');
      u.op(g.drawN, s >= 2 ? 1 : 0);
      g.shelf.setAttribute('class', 'vz-box' + (s === 1 ? ' ok' : ''));
      g.draw1.setAttribute('class', 'vz-box' + (s === 2 ? ' cr' : ' off'));
      u.op(g.drawT, s >= 2 ? 1 : 0);
      const m = at(s, k, 3);
      u.op(g.meta, m); g.metaT.forEach(t => u.op(t, m));
      u.setArrow(g.up, [398, 102], [398, 126], m);
      const f = at(s, k, 4);
      u.setArrow(g.side, [322, 154], [FD_MEAN_PUB + 10, 196], f);
      u.setArrow(g.shift, [FD_MEAN_ALL + 10, 230], [FD_MEAN_PUB - 6, 230], f);
      u.op(g.mAll, f); u.op(g.mAllT, f);
      u.op(g.mPub, f); u.op(g.mPubT, f);
      u.op(g.name, at(s, k, 5));
    },
  });

  /* ---------- 5. 개인-직무 부합과 개인-조직 부합 (w3-3, p.5) ---------- */
  const FIT_TOP = [70, 28, 28, 28, 28, 28];
  const FIT_BOT = [70, 70, 28, 68, 28, 28];
  V.add('org.fit', {
    title: '두 가지 부합도, 겹치는 자리가 달라요',
    w: 480, h: 300,
    dur: 1200,
    states: [
      { cap: '지원자 한 명을 두고 조직은 두 가지를 따로 물어요.' },
      { tag: 'P-J', cap: '직무에서 요구하는 기술과 능력을 자신이 보유하고 있는가?' },
      { tag: 'P-O', cap: '조직의 가치가 자신의 성격과 합치되는가?' },
      { cap: '기술은 맞는데 가치가 안 맞는 경우예요.' },
      { cap: '둘 다 맞으면 매력을 느끼고 계속 남아 있게 돼요.' },
      { cap: 'Job 은 일, Organization 은 조직 전체예요.' },
    ],
    build(ctx) {
      const g = ctx.g = {};
      g.tt = t1(ctx.svg, 190, 26, 'vz-tb', '개인-직무 부합');
      t1(ctx.svg, 392, 26, 'vz-ts', 'Person-Job Fit');
      g.bt = t1(ctx.svg, 190, 186, 'vz-tb', '개인-조직 부합');
      t1(ctx.svg, 380, 186, 'vz-ts', 'Person-Organization Fit');
      g.c1 = u.el(ctx.svg, 'circle', { cy: 90, r: 42, class: 'vz-box on' });
      g.c2 = u.el(ctx.svg, 'circle', { cy: 90, r: 42, class: 'vz-box tl' });
      g.c3 = u.el(ctx.svg, 'circle', { cy: 232, r: 42, class: 'vz-box on' });
      g.c4 = u.el(ctx.svg, 'circle', { cy: 232, r: 42, class: 'vz-box tl' });
      t1(ctx.svg, 8, 96, 'vz-ts', '내 능력', 'start');
      t1(ctx.svg, 316, 96, 'vz-ts', '직무 요구', 'start');
      t1(ctx.svg, 8, 238, 'vz-ts', '내 가치', 'start');
      t1(ctx.svg, 316, 238, 'vz-ts', '조직 가치', 'start');
      g.m1 = t1(ctx.svg, 190, 96, 'vz-tok', '');
      g.m2 = t1(ctx.svg, 190, 238, 'vz-tok', '');
      g.q1 = t1(ctx.svg, 200, 152, 'vz-ts', '직무가 요구하는 기술과 능력을 자신이 보유하고 있는가?');
      g.q2 = t1(ctx.svg, 200, 292, 'vz-ts', '조직의 가치가 자신의 성격과 합치되는가?');
    },
    draw(ctx, s, k) {
      const g = ctx.g, p0 = Math.max(0, s - 1), mv = seg(k, 0, 0.85);
      const gt = u.lerp(FIT_TOP[p0], FIT_TOP[s], mv);
      const gb = u.lerp(FIT_BOT[p0], FIT_BOT[s], mv);
      u.set(g.c1, { cx: 190 - gt }); u.set(g.c2, { cx: 190 + gt });
      u.set(g.c3, { cx: 190 - gb }); u.set(g.c4, { cx: 190 + gb });
      [g.c1, g.c2, g.c3, g.c4].forEach(c => u.op(c, 0.8));
      const mark = (t, v) => {
        const ok = v <= 50;
        u.txt(t, ok ? '맞음' : '안 맞음');
        t.setAttribute('class', ok ? 'vz-tok' : 'vz-tc');
      };
      mark(g.m1, gt); mark(g.m2, gb);
      u.op(g.m1, s >= 1 ? 1 : 0);
      u.op(g.m2, s >= 2 ? 1 : 0);
      u.op(g.q1, s >= 1 ? 1 : 0.35);
      u.op(g.q2, s >= 2 ? 1 : 0.35);
      g.tt.setAttribute('class', s === 1 || s === 3 || s >= 4 ? 'vz-ta' : 'vz-tb');
      g.bt.setAttribute('class', s === 2 || s >= 4 ? 'vz-ta' : 'vz-tb');
    },
  });

  /* ---------- 6. 조직사회화의 6가지 차원 (w3-4, p.8, Chao et al. 1994) ---------- */
  const DIM = [
    ['1. 역사', '관습과 전통에 친숙'],
    ['2. 언어', '전문용어와 은어'],
    ['3. 정치', '명시되지 않은 규칙'],
    ['4. 사람', '좋은 업무 관계'],
    ['5. 목표와 가치', '목표와 가치 동화'],
    ['6. 수행 숙련성', '내 일을 능숙하게'],
  ];
  V.add('org.socialdim', {
    title: '이방인이 구성원이 되기까지 배우는 여섯 가지',
    w: 480, h: 300,
    dur: 1150,
    states: [
      { cap: '개인이 이방인에서 조직 구성원으로 전환되는 장기적 과정이에요.' },
      { tag: '역사', cap: '관습이나 전통과 같은 조직의 역사에 친숙해지기예요.' },
      { tag: '언어', cap: '구성원들에게 친숙한 전문용어와 은어를 쓰게 돼요.' },
      { tag: '정치', cap: '명시되지 않은 규칙과 정치적 역학을 이해해요.' },
      { tag: '사람', cap: '다른 사람들과 좋은 업무 관계를 만들고 유지해요.' },
      { tag: '목표와 가치', cap: '조직의 목표와 가치를 학습해 동화해요.' },
      { tag: '수행 숙련성', cap: '자신의 직무를 능숙하게 수행하도록 학습해요. 가장 큰 목표예요.' },
      { cap: '여섯을 다 배우면 구성원이에요. 학습이자 문화적 적응이에요.' },
    ],
    build(ctx) {
      const g = ctx.g = {};
      t1(ctx.svg, 472, 18, 'vz-ts', 'Chao et al. 1994', 'end');
      g.out = tag(ctx.svg, 74, 52, 120, 44, '이방인');
      g.inn = tag(ctx.svg, 406, 52, 120, 44, '조직 구성원');
      g.ar = u.arrow(ctx.svg, 'tl');
      g.arT = t1(ctx.svg, 240, 44, 'vz-ts', '전환');
      g.arT2 = t1(ctx.svg, 240, 70, 'vz-ts', '장기적 과정');
      g.B = DIM.map((d, i) => {
        const col = i % 3, row = i < 3 ? 0 : 1;
        const x = 14 + col * 156, y = 90 + row * 76;
        return {
          r: u.el(ctx.svg, 'rect', { x: x, y: y, width: 140, height: 54, rx: 6, class: 'vz-box' }),
          t: t1(ctx.svg, x + 70, y + 21, 'vz-tb', d[0]),
          s: t1(ctx.svg, x + 70, y + 41, 'vz-ts', d[1]),
          at: [x + 12, y + 27],
        };
      });
      g.band = u.el(ctx.svg, 'rect', { x: 8, y: 236, width: 464, height: 34, rx: 6, class: 'vz-box' });
      t1(ctx.svg, 240, 258, 'vz-tb', '온보딩: 적응을 돕는 관행, 프로그램, 정책');
      g.note = t1(ctx.svg, 240, 288, 'vz-ts', '학습이자 문화적 적응이에요');
      g.who = u.el(ctx.svg, 'circle', { r: 8, class: 'vz-dot' });
    },
    draw(ctx, s, k) {
      const g = ctx.g;
      const spot = [[74, 52]].concat(g.B.map(b => b.at)).concat([[406, 52]]);
      const q = u.pt(spot[Math.max(0, s - 1)], spot[s], seg(k, 0, 0.8));
      u.set(g.who, { cx: q[0], cy: q[1] });
      g.B.forEach((b, i) => {
        const w = i + 1;
        b.r.setAttribute('class', 'vz-box' + (s === w ? ' on' : s > w ? ' ok' : ''));
        const o = w < s ? 1 : w === s ? seg(k, 0.25, 0.8) : 0.3;
        u.op(b.s, o);
      });
      boxCls(g.out, s === 0 ? 'am' : '');
      boxCls(g.inn, s === 7 ? 'ok' : '');
      const a = at(s, k, 7);
      u.setArrow(g.ar, [138, 52], [342, 52], 1);
      u.op(g.ar.g, u.lerp(0.3, 1, a));
      u.op(g.arT, u.lerp(0.4, 1, a));
      g.band.setAttribute('class', 'vz-box' + (s === 7 ? ' on' : ''));
      u.op(g.note, a);
    },
  });
})();
