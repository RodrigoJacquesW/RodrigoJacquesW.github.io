// Circuit-board background: faint traces everywhere, a spotlight that lights them up around
// the mouse, a small parallax, and a few signals travelling along the traces.
(function () {
  const canvas = document.getElementById("circuit");
  if (!canvas || !canvas.getContext) return;
  const ctx = canvas.getContext("2d");
  const reduceMotion = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const finePointer = matchMedia("(pointer: fine)").matches;

  const GRID = 26;          // trace grid (px)
  const MARGIN = 40;        // extra area drawn around the viewport, used by the parallax
  const PARALLAX = 0.018;   // how much the board follows the mouse
  const RADIUS = 260;       // spotlight radius (px)

  let W, H, dpr, base, lit, tmp, paths = [], pulses = [];
  let mouse = { x: innerWidth * 0.7, y: innerHeight * 0.25 }, pos = { ...mouse };
  let colors = {};

  // deterministic random, so the board does not change on every resize
  let seed = 7;
  const rand = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);

  function readColors() {
    const s = getComputedStyle(document.documentElement);
    colors = {
      trace: s.getPropertyValue("--trace").trim(),
      lit: s.getPropertyValue("--trace-lit").trim(),
      pulse: s.getPropertyValue("--accent").trim(),
    };
  }

  // One trace: orthogonal runs with an occasional 45° bend, ending in a pad.
  function makePath(cols, rows) {
    let x = Math.floor(rand() * cols), y = Math.floor(rand() * rows);
    const pts = [[x, y]];
    let dir = rand() < 0.5 ? [1, 0] : [0, 1];
    if (rand() < 0.5) dir = [-dir[0], -dir[1]];
    const segs = 2 + Math.floor(rand() * 4);
    for (let i = 0; i < segs; i++) {
      const len = 2 + Math.floor(rand() * 7);
      x += dir[0] * len; y += dir[1] * len;
      pts.push([x, y]);
      if (rand() < 0.6) { // 45° bend
        const turn = rand() < 0.5 ? 1 : -1;
        const diag = dir[0] !== 0 ? [dir[0], turn] : [turn, dir[1]];
        const d = 1 + Math.floor(rand() * 2);
        x += diag[0] * d; y += diag[1] * d;
        pts.push([x, y]);
      }
    }
    return pts.map(([a, b]) => [a * GRID, b * GRID]);
  }

  function drawBoard(target, color) {
    const c = target.getContext("2d");
    c.setTransform(dpr, 0, 0, dpr, 0, 0);
    c.clearRect(0, 0, W, H);
    c.strokeStyle = color; c.fillStyle = color;
    c.lineWidth = 1.4; c.lineJoin = "round"; c.lineCap = "round";
    for (const p of paths) {
      c.beginPath(); c.moveTo(p[0][0], p[0][1]);
      for (let i = 1; i < p.length; i++) c.lineTo(p[i][0], p[i][1]);
      c.stroke();
      const [ex, ey] = p[p.length - 1];
      c.beginPath(); c.arc(ex, ey, 3.2, 0, Math.PI * 2); c.stroke();   // end pad (ring)
      c.beginPath(); c.arc(p[0][0], p[0][1], 2.2, 0, Math.PI * 2); c.fill(); // start via
    }
    // a few chips: rectangle with pins
    seed = 99;
    const chips = Math.round((W * H) / 260000);
    for (let i = 0; i < chips; i++) {
      const cw = GRID * (2 + Math.floor(rand() * 2)), ch = GRID * (1 + Math.floor(rand() * 2));
      const cx = Math.round((rand() * (W - cw)) / GRID) * GRID, cy = Math.round((rand() * (H - ch)) / GRID) * GRID;
      c.strokeRect(cx, cy, cw, ch);
      for (let px = cx + 6; px < cx + cw - 2; px += 8) {
        c.beginPath(); c.moveTo(px, cy); c.lineTo(px, cy - 6); c.moveTo(px, cy + ch); c.lineTo(px, cy + ch + 6); c.stroke();
      }
    }
  }

  function build() {
    dpr = Math.min(devicePixelRatio || 1, 2);
    W = innerWidth + MARGIN * 2; H = innerHeight + MARGIN * 2;
    canvas.width = innerWidth * dpr; canvas.height = innerHeight * dpr;
    seed = 7;
    const cols = Math.ceil(W / GRID), rows = Math.ceil(H / GRID);
    const count = Math.round((W * H) / 9000);
    paths = Array.from({ length: count }, () => makePath(cols, rows));
    base = document.createElement("canvas"); lit = document.createElement("canvas");
    for (const c of [base, lit]) { c.width = W * dpr; c.height = H * dpr; }
    tmp = document.createElement("canvas"); tmp.width = canvas.width; tmp.height = canvas.height;
    readColors();
    drawBoard(base, colors.trace);
    drawBoard(lit, colors.lit);
    pulses = [];
  }

  function spawnPulse() {
    const p = paths[Math.floor(Math.random() * paths.length)];
    if (p) pulses.push({ p, seg: 0, t: 0, speed: 0.9 + Math.random() * 1.4 });
  }

  function frame() {
    // ease the spotlight towards the mouse
    pos.x += (mouse.x - pos.x) * 0.12; pos.y += (mouse.y - pos.y) * 0.12;
    const ox = -MARGIN - (pos.x - innerWidth / 2) * PARALLAX;
    const oy = -MARGIN - (pos.y - innerHeight / 2) * PARALLAX;

    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.drawImage(base, ox * dpr, oy * dpr);

    // lit board only inside the spotlight, faded at the edge, drawn on top of the faint board.
    // Touch screens have no cursor to follow: no spotlight there.
    if (finePointer) {
    const tc = tmp.getContext("2d");
    tc.setTransform(1, 0, 0, 1, 0, 0);
    tc.globalCompositeOperation = "source-over";
    tc.clearRect(0, 0, tmp.width, tmp.height);
    tc.drawImage(lit, ox * dpr, oy * dpr);
    const g = tc.createRadialGradient(pos.x * dpr, pos.y * dpr, 0, pos.x * dpr, pos.y * dpr, RADIUS * dpr);
    g.addColorStop(0, "rgba(0,0,0,1)"); g.addColorStop(0.55, "rgba(0,0,0,.55)"); g.addColorStop(1, "rgba(0,0,0,0)");
    tc.globalCompositeOperation = "destination-in";
    tc.fillStyle = g; tc.fillRect(0, 0, tmp.width, tmp.height);
    ctx.drawImage(tmp, 0, 0);
    }

    // signals travelling along traces
    if (!reduceMotion) {
      if (pulses.length < 7 && Math.random() < 0.04) spawnPulse();
      ctx.save(); ctx.setTransform(dpr, 0, 0, dpr, ox * dpr, oy * dpr);
      ctx.fillStyle = colors.pulse; ctx.shadowColor = colors.pulse; ctx.shadowBlur = 10;
      pulses = pulses.filter((q) => {
        const a = q.p[q.seg], b = q.p[q.seg + 1];
        if (!b) return false;
        const len = Math.hypot(b[0] - a[0], b[1] - a[1]) || 1;
        q.t += q.speed / len * 4;
        if (q.t >= 1) { q.seg++; q.t = 0; return q.seg < q.p.length - 1; }
        const x = a[0] + (b[0] - a[0]) * q.t, y = a[1] + (b[1] - a[1]) * q.t;
        ctx.globalAlpha = 0.85; ctx.beginPath(); ctx.arc(x, y, 2.4, 0, Math.PI * 2); ctx.fill();
        return true;
      });
      ctx.restore();
    }
    if (!reduceMotion) requestAnimationFrame(frame);
  }

  build();
  if (finePointer && !reduceMotion) {
    addEventListener("pointermove", (e) => { mouse.x = e.clientX; mouse.y = e.clientY; }, { passive: true });
  }
  let t; addEventListener("resize", () => { clearTimeout(t); t = setTimeout(() => { build(); if (reduceMotion) frame(); }, 150); });
  // theme toggle and OS theme change: redraw with the new colors
  new MutationObserver(() => { build(); if (reduceMotion) frame(); }).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => { build(); if (reduceMotion) frame(); });
  frame();
})();
