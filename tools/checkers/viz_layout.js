/* 움직이는 개념 그림(viz) 자리 시험 (진짜 크롬). 설명은 engine/viz/README.md
   사용
     node tools/checkers/viz_layout.js              engine/viz 의 모든 묶음
     node tools/checkers/viz_layout.js gnn iot      고른 묶음만
     CHROME=C:\경로\chrome.exe node tools/checkers/viz_layout.js    크롬 위치를 직접 줄 때
   보는 것
     등록된 그림을 헤드리스 크롬에 붙이고 상태마다 진짜 글자 크기를 재요.
     - 속성이나 글자에 NaN, undefined 가 섞였는지
     - 글자 테두리가 viewBox 밖으로 나갔는지
     - 글자가 나중에 그려진 불투명한 도형에 가려졌는지 (글자 가로 다섯 지점을 elementFromPoint 로 찍어요)
     - 글자끼리 테두리가 겹쳤는지 (작은 쪽 넓이의 25% 넘게)
   못 보는 것
     되돌리기(이전 상태와 같은지)와 조절값 시험, 금지 문자 검사는 안 해요.
     그건 jsdom 시험 tools/checkers/viz_check.js 가 봐요. 두 시험을 둘 다 돌려요.
   왜 따로 있나
     jsdom 에는 배치 엔진이 없어서 getBBox 가 늘 0 이에요. 그래서 viz_check.js 는 겹침과
     밖으로 나감을 구조적으로 못 봐요. 이 시험만 진짜 글자 크기를 알아요. */
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');
const { pathToFileURL } = require('url');

const ROOT = path.resolve(__dirname, '..', '..');
const VIZ = path.join(ROOT, 'engine', 'viz');
const FONT_CSS = 'https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css';

/* 크롬 찾기. CHROME 환경변수가 있으면 그것을 먼저 써요. */
function findChrome() {
  const cands = [];
  if (process.env.CHROME) cands.push(process.env.CHROME);
  const pf = process.env['ProgramFiles'] || 'C:\\Program Files';
  const px = process.env['ProgramFiles(x86)'] || 'C:\\Program Files (x86)';
  const la = process.env['LOCALAPPDATA'] || '';
  cands.push(path.join(pf, 'Google', 'Chrome', 'Application', 'chrome.exe'));
  cands.push(path.join(px, 'Google', 'Chrome', 'Application', 'chrome.exe'));
  if (la) cands.push(path.join(la, 'Google', 'Chrome', 'Application', 'chrome.exe'));
  for (const c of cands) { try { if (fs.statSync(c).isFile()) return c; } catch (e) { /* 다음 후보 */ } }
  return null;
}

const packs = process.argv.slice(2).length
  ? process.argv.slice(2).map(x => x.replace(/\.js$/, ''))
  : fs.readdirSync(VIZ).filter(f => f.endsWith('.js') && f !== 'viz.js').map(f => f.slice(0, -3)).sort();
if (!packs.length) { console.log('engine/viz 에 묶음 파일이 없어요.'); process.exit(1); }
const missing = packs.filter(p => !fs.existsSync(path.join(VIZ, p + '.js')));
if (missing.length) { console.log('없는 묶음: ' + missing.map(p => p + '.js').join(', ')); process.exit(1); }

const chrome = findChrome();
if (!chrome) {
  console.log('크롬을 못 찾았어요. 이 시험은 진짜 브라우저가 있어야 돌아가요.');
  console.log('찾아본 곳: Program Files, Program Files (x86), LOCALAPPDATA 의 Google\\Chrome\\Application\\chrome.exe');
  console.log('크롬이 다른 곳에 있으면 CHROME 환경변수로 chrome.exe 경로를 주세요.');
  process.exit(1);
}

/* 검사용 페이지를 임시 폴더에 만들어요 (저장소 안에는 안 만들어요). */
const work = fs.mkdtempSync(path.join(os.tmpdir(), 'vizlayout-'));
const fileUrl = p => pathToFileURL(p).href;
const scripts = [path.join(VIZ, 'viz.js')].concat(packs.map(p => path.join(VIZ, p + '.js')));

const harness = '<!doctype html>\n'
  + '<html lang="ko"><head><meta charset="utf-8"><title>viz layout</title>\n'
  + '<link rel="stylesheet" href="' + FONT_CSS + '">\n'
  + '<link rel="stylesheet" href="' + fileUrl(path.join(ROOT, 'engine', 'app.css')) + '">\n'
  + '<link rel="stylesheet" href="' + fileUrl(path.join(ROOT, 'engine', 'site.css')) + '">\n'
  + '<style>body{margin:0;padding:8px}#hosts{width:900px}.hostbox{width:900px}#report{white-space:pre-wrap;font:13px monospace}\n'
  + '/* 가림 검사용: 모든 요소가 자기 칸 어디서나 잡히게 해서 elementFromPoint 로 맨 위를 본다 */\n'
  + '.vz-svg *{pointer-events:all !important}</style>\n'
  + '</head><body>\n'
  + '<div id="hosts"></div>\n'
  + '<pre id="report">RUNNING</pre>\n'
  + scripts.map(s => '<script src="' + fileUrl(s) + '"><\/script>').join('\n') + '\n'
  + '<script>\nvar VIZ_PACKS = ' + JSON.stringify(packs) + ';\n' + auditSource() + '\n<\/script>\n'
  + '</body></html>\n';

/* 페이지 안에서 도는 검사 코드. scratch 의 audit.html 에 있던 것과 같은 검사예요. */
function auditSource() {
  return `(function () {
  var V = window.SDTViz;
  var out = [];
  if (!V) { document.getElementById('report').textContent = 'ERROR viz.js 가 안 올라왔어요'; return; }
  V.instant = true; V.freeze = true;
  var names = V.names().filter(function (n) { return VIZ_PACKS.indexOf(n.split('.')[0]) >= 0; });

  function visible(el, svg) {
    for (var n = el; n && n !== svg.parentNode; n = n.parentNode) {
      if (n.nodeType !== 1) break;
      var cs = getComputedStyle(n);
      if (cs.visibility === 'hidden' || cs.display === 'none') return false;
      if (parseFloat(cs.opacity) <= 0.02) return false;
    }
    return true;
  }
  function inter(a, b) {
    var x = Math.max(0, Math.min(a.x + a.width, b.x + b.width) - Math.max(a.x, b.x));
    var y = Math.max(0, Math.min(a.y + a.height, b.y + b.height) - Math.max(a.y, b.y));
    return x * y;
  }

  names.forEach(function (name) {
    var def = V.get(name);
    // 한 번에 그림 하나만 붙여요. 여러 개를 쌓으면 아래쪽 그림이 창 밖으로 나가고,
    // 그러면 elementFromPoint 가 null 을 돌려줘서 가림 검사가 조용히 건너뛰어져요.
    var host = document.createElement('div');
    host.className = 'hostbox';
    var hosts = document.getElementById('hosts');
    hosts.textContent = '';
    hosts.appendChild(host);
    var bad = [];
    var r, root, inst, svg;
    try {
      r = V.frame({ kind: 'viz', viz: name, head: name }, {});
      host.innerHTML = r.html;
      r.after(host);
      root = host.querySelector('.vz');
      inst = root && root._viz;
      svg = root && root.querySelector('svg.vz-svg');
    } catch (e) {
      out.push('FAIL ' + name + ' (붙지 않음)');
      out.push('       frame 오류 ' + e.message);
      return;
    }
    if (!inst || !svg) { out.push('FAIL ' + name + ' (붙지 않음)'); return; }
    var W = def.w || 480, H = def.h || 300;
    for (var s = 0; s <= r.steps; s++) {
      try { inst.onStep(s); inst.finish(); } catch (e) { bad.push('s' + s + ' draw 오류 ' + e.message); continue; }
      // NaN / undefined 가 속성이나 글자에 섞였는지
      Array.prototype.forEach.call(svg.querySelectorAll('*'), function (el) {
        for (var i = 0; i < el.attributes.length; i++) {
          var v = el.attributes[i].value;
          if (/NaN|undefined/.test(v)) bad.push('s' + s + ' <' + el.tagName + ' ' + el.attributes[i].name + '="' + v + '">');
        }
        if (el.tagName === 'text' && /NaN|undefined/.test(el.textContent)) bad.push('s' + s + ' text "' + el.textContent + '"');
      });
      // 글자가 viewBox 를 벗어나는지 + 글자끼리 겹치는지
      var texts = [];
      Array.prototype.forEach.call(svg.querySelectorAll('text'), function (el) {
        if (!el.textContent.trim()) return;
        if (!visible(el, svg)) return;
        var b;
        try { b = el.getBBox(); } catch (e) { return; }
        if (!b || !b.width) return;
        texts.push({ el: el, b: b, t: el.textContent.trim() });
        if (b.x < -1 || b.y < -1 || b.x + b.width > W + 1 || b.y + b.height > H + 1) {
          bad.push('s' + s + ' 밖으로 "' + el.textContent.trim().slice(0, 22) + '" x=' + b.x.toFixed(1) + ' y=' + b.y.toFixed(1) + ' w=' + b.width.toFixed(1) + ' h=' + b.height.toFixed(1) + ' (viewBox ' + W + 'x' + H + ')');
        }
      });
      // 글자가 나중에 그려진 도형에 가려졌는지 (화면에서 안 보이게 되는 것)
      texts.forEach(function (t) {
        var cr = t.el.getBoundingClientRect();
        if (!cr.width || !cr.height) return;
        // 글자 가로를 다섯 군데 찍어 본다 (가운데만 보면 끝자락이 가려진 것을 놓친다)
        var cy = cr.top + cr.height / 2, covered = null, nCov = 0;
        [0.1, 0.3, 0.5, 0.7, 0.9].forEach(function (fx) {
          var hit = document.elementFromPoint(cr.left + cr.width * fx, cy);
          if (!hit || hit === t.el) return;
          if (hit.tagName === 'text') return;                 // 글자끼리는 위 검사가 본다
          if (hit.contains && hit.contains(t.el)) return;      // 조상 요소는 가린 것이 아니다
          // 글자보다 먼저 그려진 것은 글자 아래에 있다. 이 지점이 글자 획 사이 빈 틈이라서
          // 뒤에 있는 배경이 잡힌 것뿐이다. 나중에 그려진 것만 진짜로 가린다.
          if (!(t.el.compareDocumentPosition(hit) & 4)) return;   // 4 = DOCUMENT_POSITION_FOLLOWING
          if (!visible(hit, svg)) return;                     // 안 보이는 도형은 가리지 못한다
          // line, polyline 은 fill 이 그려지지 않는다. 얇은 선 획에 찍힌 것은 가림이 아니다.
          if (hit.tagName === 'line' || hit.tagName === 'polyline') return;
          var f = getComputedStyle(hit).fill;
          if (f === 'none' || /rgba\\(.*,\\s*0\\)/.test(f)) return;
          if (parseFloat(getComputedStyle(hit).fillOpacity) <= 0.35) return;   // 반투명 칸은 글자가 비쳐 보인다
          nCov++; covered = hit;
        });
        if (covered) bad.push('s' + s + ' 가림 "' + t.t.slice(0, 20) + '" ' + nCov + '/5 지점이 <' + covered.tagName + ' class="' + (covered.getAttribute('class') || '') + '"> 아래');
      });
      for (var i = 0; i < texts.length; i++) {
        for (var j = i + 1; j < texts.length; j++) {
          var A = texts[i].b, B = texts[j].b;
          var ov = inter(A, B);
          if (!ov) continue;
          var small = Math.min(A.width * A.height, B.width * B.height);
          if (ov > 0.25 * small) {
            bad.push('s' + s + ' 겹침 "' + texts[i].t.slice(0, 18) + '" x "' + texts[j].t.slice(0, 18) + '" ' + Math.round(ov / small * 100) + '%');
          }
        }
      }
    }
    var uniq = [];
    bad.forEach(function (x) { if (uniq.indexOf(x) < 0) uniq.push(x); });
    out.push((uniq.length ? 'FAIL ' : 'ok   ') + name + ' (상태 ' + (r.steps + 1) + ')');
    uniq.forEach(function (x) { out.push('       ' + x); });
  });
  out.push('COUNT ' + names.length);
  out.push('DONE');
  document.getElementById('report').textContent = out.join('\\n');
})();`;
}

const page = path.join(work, 'harness.html');
fs.writeFileSync(page, harness, 'utf8');

/* 크롬은 한 번 부를 때마다 자기 --user-data-dir 가 있어야 하고, 끝날 때까지 기다려야 해요.
   그냥 줄줄이 부르면 조용히 아무 일도 안 일어나요. 그래서 spawnSync 로 기다려요.
   --dump-dom 은 --headless=old 에서만 되니까(스크린샷은 반대로 =new 에서만) old 를 써요.
   chrome.exe 를 이름으로 강제 종료하지 않아요(사용자 규칙). 넉넉한 시간을 주고 스스로 끝나게 둬요. */
const udd = path.join(work, 'cud');
const args = [
  '--headless=old', '--dump-dom', '--disable-gpu', '--hide-scrollbars',
  '--no-first-run', '--no-default-browser-check', '--disable-extensions',
  '--window-size=1280,3000',
  '--virtual-time-budget=60000',
  '--user-data-dir=' + udd,
  fileUrl(page),
];
const res = spawnSync(chrome, args, { encoding: 'buffer', timeout: 180000, maxBuffer: 256 * 1024 * 1024, windowsHide: true });

function cleanup() { try { fs.rmSync(work, { recursive: true, force: true }); } catch (e) { /* 다음에 OS 가 지워요 */ } }

if (res.error) { cleanup(); console.log('크롬을 돌리지 못했어요: ' + res.error.message); process.exit(1); }
// --dump-dom 은 UTF-8 로 뱉어요. 그대로 UTF-8 로 읽어요.
const dom = (res.stdout || Buffer.alloc(0)).toString('utf8');
const err = (res.stderr || Buffer.alloc(0)).toString('utf8');
cleanup();

const m = dom.match(/<pre id="report">([\s\S]*?)<\/pre>/);
if (!m) {
  console.log('크롬이 보고를 안 남겼어요. 페이지가 안 열렸을 수 있어요.');
  if (err.trim()) console.log(err.trim().split('\n').slice(-12).map(l => '  ' + l).join('\n'));
  process.exit(1);
}
const report = m[1]
  .replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"')
  .replace(/&#39;/g, "'").replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&');

const lines = report.split('\n');
if (lines.indexOf('DONE') < 0) {
  console.log('검사가 끝까지 못 갔어요:');
  console.log(lines.map(l => '  ' + l).join('\n'));
  if (err.trim()) console.log(err.trim().split('\n').slice(-12).map(l => '  ' + l).join('\n'));
  process.exit(1);
}

const countLine = lines.find(l => l.indexOf('COUNT ') === 0);
const total = countLine ? parseInt(countLine.slice(6), 10) : 0;
const body = lines.filter(l => l !== 'DONE' && l.indexOf('COUNT ') !== 0);
body.forEach(l => console.log('  ' + l));

const fails = body.filter(l => l.indexOf('FAIL') === 0);
if (!total) { console.log('\n등록된 그림이 없어요: ' + packs.join(', ')); process.exit(1); }
if (fails.length) {
  console.log('\nviz layout errors: 그림 ' + total + '개 중 ' + fails.length + '개에 문제가 있어요 (묶음 ' + packs.join(', ') + ')');
  process.exit(1);
}
console.log('\nviz layout errors: 없음 (' + total + '개, 묶음 ' + packs.join(', ') + ')');
