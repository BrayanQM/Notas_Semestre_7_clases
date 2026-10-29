(function(){
  'use strict';
  const canvas = document.getElementById('track');
  const ctx = canvas.getContext('2d');
  const balanceEl = document.getElementById('balance');
  const statusEl = document.getElementById('status');
  const raceStatusEl = document.getElementById('racestatus');
  const betPanel = document.getElementById('betpanel');
  const picker = document.getElementById('picker');
  const startBtn = document.getElementById('startBtn');
  const betAmountEl = document.getElementById('betAmount');

  // Spritesheet: 4x4 grid, each frame 124x77 (image 500x335)
  const FRAME_W = 124;
  const FRAME_H = 77;
  const COLS = 4;
  const ROWS = 4;
  const TOTAL_FRAMES = COLS * ROWS;

  const NUM_HORSES = 6;
  const HORSE_NAMES = ['Relámpago','Trueno','Centella','Furia','Duque','Viento'];
  const HORSE_COLORS = ['#ff5252','#ffa726','#ffeb3b','#66bb6a','#42a5f5','#ab47bc'];

  const sheet = new Image();
  sheet.src = 'Photoroom-20260901_163511.png';
  sheet.onload = buildPicker;

  let balance = 1000;
  let selected = 0;
  let bet = 130;
  let state = 'betting';   // 'betting' | 'racing' | 'done'

  // ---- dynamic geometry ----
  let W = 0, H = 0, SW = 0, SH = 0;
  let TRACK_TOP = 0, TRACK_BOTTOM = 0, SLOT_H = 0, START_X = 0, FINISH_X = 0;

  const horses = [];
  for (let i = 0; i < NUM_HORSES; i++) {
    horses.push({
      index: i,
      x: 0,
      y: 0,
      speed: 0,
      baseSpeed: 0,
      frame: i % TOTAL_FRAMES,
      frameTimer: 0,
      finished: false,
      place: 0,
      color: HORSE_COLORS[i],
      name: HORSE_NAMES[i]
    });
  }

  function layout() {
    W = window.innerWidth;
    H = window.innerHeight;
    canvas.width = W;
    canvas.height = H;

    SH = Math.min(H * 0.14, W * 0.22, 140);
    const scale = SH / FRAME_H;
    SW = FRAME_W * scale;

    TRACK_TOP = SH * 0.32;
    TRACK_BOTTOM = H - SH * 0.24;
    SLOT_H = (TRACK_BOTTOM - TRACK_TOP) / NUM_HORSES;
    START_X = SW * 0.18;
    FINISH_X = W - SW * 0.55;

    for (let i = 0; i < NUM_HORSES; i++) {
      horses[i].y = TRACK_TOP + SLOT_H * i + SLOT_H / 2;
    }
  }

  function onResize() {
    const oldW = W || window.innerWidth;
    layout();
    if (oldW !== W) {
      const f = oldW === 0 ? 1 : W / oldW;
      for (const h of horses) h.x *= f;
    }
    drawScene();
  }
  window.addEventListener('resize', onResize);

  // ------- Scene drawing -------
  function drawScene() {
    // full-bleed grass
    const g = ctx.createLinearGradient(0, 0, 0, H);
    g.addColorStop(0, '#8fb944');
    g.addColorStop(0.12, '#79a63a');
    g.addColorStop(1, '#4e7a22');
    ctx.fillStyle = g;
    ctx.fillRect(0, 0, W, H);

    // subtle track strip
    ctx.fillStyle = 'rgba(120,105,70,.35)';
    ctx.fillRect(0, TRACK_TOP - SLOT_H * 0.1, W, TRACK_BOTTOM - TRACK_TOP + SLOT_H * 0.2);

    // lane separators
    ctx.strokeStyle = 'rgba(255,255,255,.25)';
    ctx.lineWidth = 2;
    for (let i = 1; i < NUM_HORSES; i++) {
      const y = TRACK_TOP + SLOT_H * i;
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(W, y);
      ctx.stroke();
    }

    // start line
    ctx.fillStyle = 'rgba(255,255,255,.9)';
    ctx.fillRect(START_X + SW * 0.25, TRACK_TOP, 6, TRACK_BOTTOM - TRACK_TOP);

    // finish line (checkered)
    const cw = Math.max(10, Math.round(SLOT_H * 0.18));
    const fby = TRACK_BOTTOM;
    for (let yy = TRACK_TOP; yy < fby; yy += cw) {
      for (let x = FINISH_X; x < FINISH_X + cw * 2; x += cw) {
        const row = Math.floor((yy - TRACK_TOP) / cw);
        const col = Math.floor((x - FINISH_X) / cw);
        ctx.fillStyle = (row + col) % 2 === 0 ? '#fff' : '#222';
        ctx.fillRect(x, yy, cw, cw);
      }
    }

    const order = [...horses].sort((a, b) => (a.finished ? 1 : 0) - (b.finished ? 1 : 0));
    order.forEach(drawHorse);
  }

  function drawHorse(h) {
    const sx = (h.frame % COLS) * FRAME_W;
    const sy = Math.floor(h.frame / COLS) % ROWS * FRAME_H;
    const y = h.y - SH * 0.72;

    // shadow
    ctx.fillStyle = 'rgba(0,0,0,.3)';
    ctx.beginPath();
    ctx.ellipse(h.x + SW / 2.5, h.y + SH * 0.34, SW * 0.55, SH * 0.12, 0, 0, Math.PI * 2);
    ctx.fill();

    if (sheet.complete && sheet.naturalWidth > 0) {
      ctx.drawImage(sheet, sx, sy, FRAME_W, FRAME_H, h.x, y, SW, SH);
    }

    const font = Math.max(12, Math.round(SH * 0.19));
    ctx.font = `bold ${font}px "Segoe UI", sans-serif`;
    ctx.lineWidth = 3;
    ctx.strokeStyle = 'rgba(0,0,0,.75)';
    ctx.strokeText(h.name, h.x + SW + 8, y + font - 2);
    ctx.fillStyle = h.color;
    ctx.fillText(h.name, h.x + SW + 8, y + font - 2);

    if (h.place > 0) {
      const label = '#' + h.place;
      ctx.font = `bold ${font + 2}px "Segoe UI", sans-serif`;
      ctx.lineWidth = 3;
      ctx.strokeStyle = 'rgba(0,0,0,.8)';
      ctx.strokeText(label, h.x - 14, y + SH - 4);
      ctx.fillStyle = h.place === 1 ? '#f4c542' : '#ddd';
      ctx.fillText(label, h.x - 14, y + SH - 4);
    }
  }

  // ------- Race logic -------
  let placedCount = 0;
  let winner = null;

  function resetRace() {
    placedCount = 0;
    for (const h of horses) {
      h.x = START_X;
      h.speed = 0;
      h.baseSpeed = 85 + Math.random() * 55;
      h.frame = Math.floor(Math.random() * TOTAL_FRAMES);
      h.frameTimer = 0;
      h.finished = false;
      h.place = 0;
    }
  }

  function update(dt) {
    for (const h of horses) {
      if (h.finished) continue;

      h.speed = h.baseSpeed * (0.72 + Math.random() * 0.56);
      h.x += h.speed * dt;

      h.frameTimer += dt * (7 + h.speed * 0.03);
      if (h.frameTimer >= 1) {
        h.frameTimer = 0;
        h.frame = (h.frame + 1) % TOTAL_FRAMES;
      }

      if (h.x + SW >= FINISH_X) {
        h.x = FINISH_X - SW;
        h.finished = true;
        placedCount++;
        h.place = placedCount;
        if (placedCount === 1) winner = h;
        if (placedCount === NUM_HORSES) {
          state = 'done';
          endRace(winner);
        }
      }
    }
  }

  function endRace(w) {
    const win = w.index === selected;
    if (win) {
      const prize = Math.round(bet * 3.5);
      balance += prize;
      statusEl.innerHTML = `🏆 ¡Tu caballo <b>${w.name}</b> ganó! +$${prize}`;
      statusEl.style.color = '#7CFC00';
    } else {
      balance -= bet;
      statusEl.innerHTML = `😢 Ganó <b>${w.name}</b>. Perdiste $${bet}`;
      statusEl.style.color = '#ff6b6b';
    }
    balance = Math.max(balance, 10);
    balanceEl.textContent = `💰 $${balance}`;

    raceStatusEl.innerHTML = `🏆 ¡${w.name} GANA!`;
    raceStatusEl.style.display = 'block';

    setTimeout(() => {
      raceStatusEl.style.display = 'none';
      statusEl.innerHTML = '&nbsp;';
      betPanel.classList.remove('hidden');
      resetRace();
      winner = null;
      state = 'betting';
      drawScene();
    }, 2600);
  }

  let raf = null;
  let lastT = 0;

  function loop(now) {
    const dt = Math.min((now - lastT) / 1000, 0.05);
    lastT = now;
    if (state === 'racing') update(dt);
    drawScene();
    raf = requestAnimationFrame(loop);
  }

  // ------- UI -------
  function buildPicker() {
    picker.innerHTML = '';
    for (let i = 0; i < NUM_HORSES; i++) {
      const btn = document.createElement('button');
      btn.className = 'horse-btn' + (i === selected ? ' selected' : '');
      const col = i % COLS;
      const row = Math.floor(i / COLS) % ROWS;

      const cv = document.createElement('canvas');
      cv.width = 124;
      cv.height = 77;
      const c = cv.getContext('2d');
      c.drawImage(sheet, col * FRAME_W, row * FRAME_H, FRAME_W, FRAME_H, 0, 0, 124, 77);

      const span = document.createElement('span');
      span.textContent = `${i + 1}º ${HORSE_NAMES[i]}`;
      span.style.color = HORSE_COLORS[i];

      btn.appendChild(cv);
      btn.appendChild(span);
      btn.addEventListener('click', () => {
        selected = i;
        buildPicker();
      });
      picker.appendChild(btn);
    }
  }

  startBtn.addEventListener('click', () => {
    bet = parseInt(betAmountEl.value, 10) || 100;
    bet = Math.max(10, Math.round(bet));
    betAmountEl.value = bet;
    if (bet > balance) { statusEl.innerHTML = '⚠ No tienes suficiente dinero'; return; }
    resetRace();
    state = 'racing';
    statusEl.innerHTML = '🏁 ¡Corriendo!';
    statusEl.style.color = '#fff';
    betPanel.classList.add('hidden');
    lastT = performance.now();
  });

  layout();
  resetRace();
  buildPicker();
  lastT = performance.now();
  requestAnimationFrame(loop);
})();
