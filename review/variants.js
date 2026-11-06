// Review variants B (storyboard) and C (chat replay). Both read the same flow data as variant A.
(() => {
  const FLOW = JSON.parse(document.getElementById("flow-src").textContent);
  const LANES = { you: "You", agent: "Agent", data: "Your data" };
  const TYPES = { act: "You", work: "Agent", read: "Reads, read-only", decide: "Decision", approve: "Your approval", output: "Result", optional: "Optional" };
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const esc = (s) => String(s || "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const words = (s) => String(s || "").split(/\s+/).filter(Boolean).length;
  const ICON = {
    you: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="8" r="4"/><path d="M4 21c1.5-4 4.5-6 8-6s6.5 2 8 6"/></svg>',
    agent: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="4" y="7" width="16" height="12" rx="3"/><path d="M12 3v4M9 12h.01M15 12h.01M9 16h6"/></svg>',
    data: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><ellipse cx="12" cy="6" rx="7" ry="3"/><path d="M5 6v12c0 1.7 3.1 3 7 3s7-1.3 7-3V6M5 12c0 1.7 3.1 3 7 3s7-1.3 7-3"/></svg>',
  };
  const rows = FLOW.steps.map((r) => (Array.isArray(r) ? r : [r]));
  const keys = Object.keys(FLOW.paths || {});

  // A small player: frames, timer, controls, timeline. The view supplies show(i, frames) and reset().
  function player(root, view) {
    let path = keys[0] || "", frames = [], idx = -1, playing = false, timer = 0, dur = 0, spent = 0, started = 0;
    const bar = root.querySelector(".pl-bar"), time = root.querySelector(".pl-time");
    const playBtn = bar.querySelector('[data-act="play"]');
    const box = bar.querySelector(".flow-paths");
    keys.forEach((k) => {
      const b = document.createElement("button");
      b.type = "button"; b.textContent = FLOW.paths[k]; b.dataset.path = k;
      b.addEventListener("click", () => { path = k; pause(); build(); view.reset(frames, path); go(0); });
      box.append(b);
    });
    function build() {
      box.querySelectorAll("button").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.path === path)));
      frames = rows.map((r) => r.filter((s) => !s.path || s.path === path)).filter((f) => f.length);
      time.replaceChildren(...frames.map((f, i) => {
        const s = document.createElement("button");
        s.type = "button"; s.className = "flow-seg"; s.setAttribute("aria-label", `Go to step ${i + 1}: ${f[0].title}`);
        s.append(document.createElement("span"));
        s.addEventListener("click", () => { pause(); go(i); });
        return s;
      }));
    }
    function go(i) {
      idx = i;
      [...time.children].forEach((s, k) => { const b = s.firstChild; b.style.transition = "none"; b.style.width = k < i ? "100%" : "0"; });
      view.show(i, frames, path);
      const text = frames[i].map((s) => `${s.title} ${s.say} ${s.guard || ""}`).join(" ");
      dur = Math.min(8000, 1400 + 220 * words(text)) + (view.extra ? view.extra(frames[i]) : 0);
      spent = 0;
    }
    function fill() {
      const b = time.children[idx]?.firstChild; if (!b) return;
      b.style.transition = "none"; b.style.width = (100 * spent / dur) + "%"; void b.offsetWidth;
      b.style.transition = `width ${dur - spent}ms linear`; b.style.width = "100%";
    }
    function schedule() {
      clearTimeout(timer); started = performance.now(); fill();
      timer = setTimeout(() => { if (idx + 1 < frames.length) { go(idx + 1); schedule(); } else end(); }, dur - spent);
    }
    function end() { playing = false; label("↺ Watch again"); view.end && view.end(frames); idx = frames.length; }
    function play() { if (idx < 0 || idx >= frames.length) { view.reset(frames, path); go(0); } playing = true; label("❚❚ Pause"); schedule(); }
    function pause() {
      if (!playing) return;
      playing = false; clearTimeout(timer); spent += performance.now() - started;
      const b = time.children[idx]?.firstChild; if (b) { const w = getComputedStyle(b).width; b.style.transition = "none"; b.style.width = w; }
      label("▶ Play");
    }
    function label(t) { playBtn.textContent = t; }
    playBtn.addEventListener("click", () => (playing ? pause() : play()));
    bar.querySelector('[data-act="prev"]').addEventListener("click", () => { pause(); go(Math.max(0, Math.min(idx, frames.length) - 1)); });
    bar.querySelector('[data-act="next"]').addEventListener("click", () => { pause(); go(Math.min(frames.length - 1, idx + 1)); });
    bar.querySelector('[data-act="restart"]').addEventListener("click", () => { pause(); view.reset(frames, path); go(0); play(); });
    build(); view.reset(frames, path); go(0);
    return { play, pause, goTo: (i) => { pause(); go(i); }, get playing() { return playing; } };
  }

  // ---------------------------------------------------------------- B. Storyboard
  function storyboard(root) {
    const track = root.querySelector(".sb-track"), stage = root.querySelector(".sb-stage"), strip = root.querySelector(".sb-strip");
    let P, cur = [];
    const laneY = { you: 18, agent: 54, data: 90 };
    function drawTrack(frames, i) {
      if (track.clientWidth < 120) return;   // hidden tab: draw when it is shown
      const W = track.clientWidth - 32, left = 86, step = (W - left - 12) / Math.max(1, frames.length - 1);
      const pts = frames.map((f, k) => ({ x: left + k * step, y: laneY[f[0].lane], f, k }));
      let s = `<svg viewBox="0 0 ${W} 108" aria-hidden="true">`;
      for (const [l, y] of Object.entries(laneY)) s += `<rect class="lane-r" x="0" y="${y - 13}" width="${W}" height="26" rx="13"/><text class="lane-l" x="12" y="${y + 4}" fill="var(--fl-${l})">${LANES[l]}</text>`;
      for (let k = 1; k < pts.length; k++) {
        const a = pts[k - 1], b = pts[k], mx = (a.x + b.x) / 2;
        s += `<path class="ln ${k <= i ? "lit" : ""}" d="M${a.x},${a.y} C${mx},${a.y} ${mx},${b.y} ${b.x},${b.y}"/>`;
      }
      for (const p of pts) {
        const st = p.f[0], c = st.type === "approve" ? "gate" : st.lane;
        if (p.k === i) s += `<circle class="halo" cx="${p.x}" cy="${p.y}" r="14" stroke="var(--fl-${c})"><animate attributeName="r" values="10;16;10" dur="1.6s" repeatCount="indefinite"/></circle>`;
        s += `<circle class="dot ${p.k < i ? "past" : p.k === i ? "now" : "future"}" data-k="${p.k}" cx="${p.x}" cy="${p.y}" r="6.5" fill="var(--fl-${c})"><title>Step ${p.k + 1}: ${esc(st.title)}</title></circle>`;
      }
      track.innerHTML = s + "</svg>";
      track.querySelectorAll(".dot").forEach((d) => d.addEventListener("click", () => P.goTo(+d.dataset.k)));
    }
    function card(st, i, n) {
      const c = st.type === "approve" ? "t-approve" : "";
      return `<article class="sb-card l-${st.lane} ${c}">
        <div class="sb-who"><span class="sb-av">${ICON[st.lane]}</span><div><b>${LANES[st.lane]}</b><span>${esc(TYPES[st.type])}</span></div><span class="sb-step">Step ${i + 1} of ${n}</span></div>
        <h3>${esc(st.title)}</h3><p>${esc(st.say)}</p>
        ${st.guard ? `<div class="sb-guard"><span aria-hidden="true">⛨</span><span>${esc(st.guard)}</span></div>` : ""}
      </article>`;
    }
    function scene(html) {
      const old = stage.querySelector(".sb-scene:not(.out)");
      const el = document.createElement("div");
      el.className = "sb-scene" + (reduce ? "" : " in"); el.innerHTML = html;
      stage.append(el);
      if (old) { old.classList.add("out"); setTimeout(() => old.remove(), reduce ? 0 : 400); }
      requestAnimationFrame(() => requestAnimationFrame(() => el.classList.remove("in")));
    }
    const view = {
      reset(frames) {
        strip.innerHTML = frames.map((f, k) => `<button type="button" class="sb-thumb l-${f[0].lane} ${f[0].type === "approve" ? "t-approve" : ""}" data-k="${k}"><i>${k + 1} · ${LANES[f[0].lane]}</i>${esc(f[0].title)}</button>`).join("");
        strip.querySelectorAll(".sb-thumb").forEach((b) => b.addEventListener("click", () => P.goTo(+b.dataset.k)));
      },
      show(i, frames) {
        cur = frames;
        drawTrack(frames, i);
        scene(frames[i].map((st) => card(st, i, frames.length)).join(""));
        strip.querySelectorAll(".sb-thumb").forEach((b, k) => { b.classList.toggle("past", k < i); b.classList.toggle("now", k === i); });
        const t = strip.children[i]; if (t) strip.scrollTo({ left: t.offsetLeft - strip.clientWidth / 2 + t.clientWidth / 2, behavior: reduce ? "auto" : "smooth" });
      },
      end(frames) {
        drawTrack(frames, frames.length);
        scene(`<article class="sb-card"><div class="sb-who"><span class="sb-av">✓</span><div><b>Run complete</b><span>${frames.length} steps</span></div></div><h3>What you end with</h3><p>${esc(FLOW.end)}</p></article>`);
      },
    };
    P = player(root, view);
    new ResizeObserver(() => { const i = [...strip.children].findIndex((b) => b.classList.contains("now")); if (i >= 0) drawTrack(cur, i); }).observe(track);
    return P;
  }

  // ---------------------------------------------------------------- C. Chat replay
  function chat(root) {
    const win = root.querySelector(".ch-win");
    let shown = -1, P;
    function bubble(st, path) {
      if (st.type === "read") {
        return `<div class="ch-tool"><span class="ch-chip"><span class="spin" aria-hidden="true"></span><span class="st">Reading</span>${esc(st.title)}</span><small>${esc(st.say)}</small>${st.guard ? `<span class="ch-guard">⛨ ${esc(st.guard)}</span>` : ""}</div>`;
      }
      const cls = st.type === "approve" ? "you approve" : st.lane;
      const who = st.type === "approve" ? "You · approval" : st.lane === "you" ? "You" : st.type === "work" ? "Agent" : "Agent · " + TYPES[st.type].toLowerCase();
      let extra = "";
      if (st.type === "decide" && FLOW.paths) extra = `<div class="ch-opts">${keys.map((k) => `<span class="${k === path ? "on" : ""}">${esc(FLOW.paths[k])}</span>`).join("")}</div>`;
      const body = st.type === "approve" ? `<b>${esc(st.title)}</b>${esc(st.say)}<div class="ch-opts"><span class="on">Yes</span><span>Not yet</span></div>` : `<b>${esc(st.title)}</b>${esc(st.say)}${extra}`;
      return `<div class="ch-msg ${cls}"><span class="who">${who}</span><div class="ch-bub">${body}</div>${st.guard ? `<span class="ch-guard">⛨ ${esc(st.guard)}</span>` : ""}</div>`;
    }
    function add(html) { win.insertAdjacentHTML("beforeend", html); win.scrollTop = win.scrollHeight; }
    function finishTools() { win.querySelectorAll(".ch-chip .spin").forEach((s) => { s.outerHTML = '<span aria-hidden="true">✓</span>'; }); win.querySelectorAll(".ch-chip .st").forEach((s) => { if (s.textContent === "Reading") s.textContent = "Read"; }); }
    let typingTimer = 0, pending = null;
    // A step that is still "typing" is shown at once when the run moves on, so no message is lost.
    const flush = () => { clearTimeout(typingTimer); if (pending) { const f = pending; pending = null; f(); } };
    const view = {
      extra: () => (reduce ? 0 : 700),
      reset() { clearTimeout(typingTimer); pending = null; win.innerHTML = ""; shown = -1; },
      show(i, frames, path) {
        flush();
        if (i <= shown) { view.reset(); for (let k = 0; k < i; k++) frames[k].forEach((st) => add(bubble(st, path))); finishTools(); shown = i - 1; }
        for (let k = shown + 1; k < i; k++) frames[k].forEach((st) => add(bubble(st, path)));
        finishTools();
        shown = i;
        const f = frames[i];
        const reveal = () => { pending = null; win.querySelector(".ch-typing")?.remove(); f.forEach((st) => add(bubble(st, path))); };
        if (reduce || f[0].type === "read") return reveal();
        add(`<div class="ch-typing ${f[0].lane === "you" ? "you" : ""}" aria-hidden="true"><i></i><i></i><i></i></div>`);
        pending = reveal;
        typingTimer = setTimeout(reveal, 700);
      },
      end() { flush(); finishTools(); add(`<div class="ch-tool"><span class="ch-chip" style="border-style:solid;border-color:var(--fl-agent);background:var(--fl-agent-soft)"><span aria-hidden="true">✓</span><span class="st" style="color:var(--fl-agent)">Done</span>Run complete</span><small>${esc(FLOW.end)}</small></div>`); },
    };
    P = player(root, view);
    return P;
  }

  const players = { b: storyboard(document.getElementById("pl-b")), c: chat(document.getElementById("pl-c")) };
  window.__rvPlayers = players;
})();
