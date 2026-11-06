// Flow movie. build.py renders each step as a card (.fnode) with data-row, data-path and data-lane.
// This script draws the wires, then plays the run one row ("frame") at a time: the card lights up,
// a dot travels along the wire into it, the subtitle reads the step aloud in text, and the timeline fills.
(() => {
  const LANES = { you: "You", agent: "Agent", data: "Your data" };
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const narrow = matchMedia("(max-width: 760px)");
  const SVGNS = "http://www.w3.org/2000/svg";

  function setup(root) {
    const cfg = JSON.parse(root.querySelector(".flow-data").textContent);
    const grid = root.querySelector(".flow-grid");
    const nodes = [...root.querySelectorAll(".fnode")];
    const sub = root.querySelector(".flow-sub");
    const subK = sub.querySelector(".flow-sub-k"), subT = sub.querySelector(".flow-sub-t"), subG = sub.querySelector(".flow-sub-g");
    const time = sub.querySelector(".flow-time");
    const playBtn = root.querySelector('[data-act="play"]');
    const pathKeys = Object.keys(cfg.paths || {});
    let path = pathKeys[0] || "";
    let frames = [], idx = -1, playing = false, timer = 0, started = 0, spent = 0, dur = 0, user = false;

    root.classList.add("js");
    // Minimal mode: cards show titles only. The playing card opens its details; a card the reader opens stays open.
    const min = root.classList.contains("min");
    const count = min ? Object.assign(document.createElement("span"), { className: "flow-count" }) : null;
    if (min) root.querySelector(".flow-btns").after(count);
    const svg = document.createElementNS(SVGNS, "svg");
    svg.setAttribute("class", "flow-wires");
    svg.setAttribute("aria-hidden", "true");
    grid.prepend(svg);

    // Path choice (for example "Connected" or "Upload files").
    const pathBox = root.querySelector(".flow-paths");
    if (pathKeys.length > 1) {
      for (const k of pathKeys) {
        const b = document.createElement("button");
        b.type = "button"; b.textContent = cfg.paths[k]; b.dataset.path = k;
        b.setAttribute("aria-pressed", String(k === path));
        b.addEventListener("click", () => { path = k; user = true; pause(); build(); go(Math.min(idx, frames.length - 1), false); });
        pathBox.append(b);
      }
    } else pathBox.remove();

    const onPath = (n) => !n.dataset.path || n.dataset.path === path;

    function build() {
      pathBox.querySelectorAll && pathBox.querySelectorAll("button").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.path === path)));
      for (const n of nodes) {
        // Side-by-side alternatives stay visible on wide screens (dimmed); one column shows the chosen path only.
        // An off-path card that shares its cell (same row, same lane) with an on-path card is hidden too.
        const shared = nodes.some((m) => m !== n && onPath(m) && m.dataset.row === n.dataset.row && m.dataset.lane === n.dataset.lane);
        n.hidden = !onPath(n) && (narrow.matches || shared);
        n.classList.toggle("off", !onPath(n));
      }
      root.querySelectorAll(".frow").forEach((r) => r.classList.toggle("solo", [...r.children].filter((c) => !c.hidden).length === 1));
      const rows = new Map();
      for (const n of nodes) if (onPath(n)) (rows.get(+n.dataset.row) || rows.set(+n.dataset.row, []).get(+n.dataset.row)).push(n);
      frames = [...rows.keys()].sort((a, b) => a - b).map((k) => rows.get(k));
      time.replaceChildren(...frames.map((f, i) => {
        const s = document.createElement("button");
        s.type = "button"; s.className = "flow-seg";
        s.setAttribute("aria-label", `Go to step ${i + 1}: ${title(f[0])}`);
        s.append(document.createElement("span"));
        s.addEventListener("click", () => { user = true; pause(); go(i, true); });
        return s;
      }));
    }

    const title = (n) => n.querySelector(".ft").textContent.trim();
    const say = (n) => n.querySelector(".fs")?.textContent.trim() || "";
    const guard = (n) => n.querySelector(".fg")?.textContent.replace(/^\s*⛨\s*/, "").trim() || "";
    const words = (s) => s.split(/\s+/).filter(Boolean).length;

    function wire(a, b, g) {
      const ra = a.getBoundingClientRect(), rb = b.getBoundingClientRect();
      const x1 = ra.left + ra.width / 2 - g.left, y1 = ra.bottom - g.top;
      const x2 = rb.left + rb.width / 2 - g.left, y2 = rb.top - g.top;
      if (y2 <= y1 + 2) return null;
      const my = y1 + Math.min(14, (y2 - y1) / 2);
      if (Math.abs(x2 - x1) < 2) return { d: `M${x1},${y1} V${y2 - 2}`, x1, x2, my };
      const r = Math.min(7, Math.abs(x2 - x1) / 2, (my - y1));
      const sx = Math.sign(x2 - x1);
      return { d: `M${x1},${y1} V${my - r} Q${x1},${my} ${x1 + sx * r},${my} H${x2 - sx * r} Q${x2},${my} ${x2},${my + r} V${y2 - 2}`, x1, x2, my };
    }

    function draw(animate) {
      const g = grid.getBoundingClientRect();
      const out = ['<defs><marker id="fa-' + root.id + '" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z"/></marker></defs>'];
      const dots = [];
      // Connect every visible card in one row to every visible card in the next row that shares its path.
      const rows = [...new Set(nodes.filter((n) => !n.hidden).map((n) => +n.dataset.row))].sort((a, b) => a - b);
      for (let i = 0; i + 1 < rows.length; i++) {
        const A = nodes.filter((n) => !n.hidden && +n.dataset.row === rows[i]);
        const B = nodes.filter((n) => !n.hidden && +n.dataset.row === rows[i + 1]);
        for (const a of A) for (const b of B) {
          if (a.dataset.path && b.dataset.path && a.dataset.path !== b.dataset.path) continue;
          const w = wire(a, b, g); if (!w) continue;
          const live = onPath(a) && onPath(b);
          const lit = live && a.classList.contains("past") && (b.classList.contains("past") || b.classList.contains("now"));
          out.push(`<path class="${lit ? "lit" : ""} ${live ? "" : "dim"}" d="${w.d}" marker-end="url(#fa-${root.id})"/>`);
          if (b.dataset.path && a.classList.contains("t-decide") && cfg.paths[b.dataset.path]) {
            const right = w.x2 > w.x1;
            out.push(`<text x="${w.x2 + (right ? -10 : 10)}" y="${w.my - 5}" text-anchor="${right ? "end" : "start"}" opacity="${live ? 1 : .4}">${esc(cfg.when?.[b.dataset.path] || "")}</text>`);
          }
          if (animate && live && b.classList.contains("now") && a.classList.contains("past")) dots.push(w.d);
        }
      }
      for (const d of dots) out.push(`<circle r="5" cx="0" cy="0"><animateMotion dur="0.7s" fill="freeze" begin="indefinite" path="${d}" calcMode="spline" keyTimes="0;1" keySplines="0.4 0 0.2 1"/></circle>`);
      svg.innerHTML = out.join("");
      if (!dots.length) return;
      svg.querySelectorAll("animateMotion").forEach((m) => { try { m.beginElement(); } catch {} });
      setTimeout(() => svg.querySelectorAll("circle").forEach((c) => c.remove()), 900);
    }

    function go(i, animate) {
      idx = i;
      nodes.forEach((n) => n.classList.remove("past", "now", "future"));
      frames.forEach((f, k) => f.forEach((n) => n.classList.add(k < i ? "past" : k === i ? "now" : "future")));
      [...time.children].forEach((s, k) => {
        s.classList.toggle("done", k < i);
        const bar = s.firstChild; bar.style.transition = "none"; bar.style.width = k < i ? "100%" : "0";
        if (k === i) s.setAttribute("aria-current", "step"); else s.removeAttribute("aria-current");
      });
      root.classList.remove("ended");
      if (min) {
        const cur = i >= 0 ? frames[i] : [];
        nodes.forEach((n) => { const o = n.classList.contains("pinned") || cur.includes(n); n.classList.toggle("open", o); n.setAttribute("aria-expanded", String(o)); });
        count.textContent = i >= 0 ? `Step ${i + 1} of ${frames.length}` : `${frames.length} steps`;
      }
      if (i < 0) { caption(null); draw(false); return; }
      const f = frames[i];
      caption(f, i);
      draw(animate && !reduce);
      if (user && playing) {
        const r = f[0].getBoundingClientRect(), bottom = innerHeight - sub.offsetHeight;
        if (r.top < 0 || r.bottom > bottom) f[0].scrollIntoView({ block: "center", behavior: reduce ? "auto" : "smooth" });
      }
      const text = f.map((n) => title(n) + " " + say(n) + " " + guard(n)).join(" ");
      dur = Math.min(8000, 1400 + 220 * words(text));   // about 4.5 words a second, plus a pause to look at the card
      spent = 0;
    }

    function caption(f, i) {
      if (!f) {
        subK.innerHTML = `<span>${frames.length} steps</span>`;
        subT.textContent = cfg.intro || "Press play to watch one run, step by step.";
        subG.hidden = true; return;
      }
      const lanes = [...new Set(f.map((n) => n.dataset.lane))];
      subK.innerHTML = `<span>Step ${i + 1} of ${frames.length}</span>` + lanes.map((l) => `<b style="--c:var(--fl-${l})">${LANES[l]}</b>`).join("");
      subT.innerHTML = f.map((n) => `<strong>${esc(title(n))}.</strong> ${esc(say(n))}`).join("<br>");
      const gs = f.map(guard).filter(Boolean);
      subG.hidden = !gs.length;
      subG.innerHTML = gs.length ? `<span aria-hidden="true">⛨</span><span>${gs.map(esc).join(" ")}</span>` : "";
    }

    function fill() {
      const bar = time.children[idx]?.firstChild; if (!bar) return;
      const left = Math.max(0, dur - spent);
      bar.style.transition = "none";
      bar.style.width = (100 * spent / dur) + "%";
      void bar.offsetWidth;
      bar.style.transition = `width ${left}ms linear`;
      bar.style.width = "100%";
    }

    function schedule() {
      clearTimeout(timer);
      started = performance.now();
      fill();
      timer = setTimeout(() => {
        if (idx + 1 < frames.length) { go(idx + 1, true); schedule(); }
        else end();
      }, Math.max(0, dur - spent));
    }

    function end() {
      playing = false;
      time.children[idx]?.classList.add("done");
      frames[idx].forEach((n) => { n.classList.remove("now"); n.classList.add("past"); });
      draw(false);
      subK.innerHTML = `<span>Run complete</span>`;
      subT.textContent = cfg.end || "The run is complete.";
      subG.hidden = true;
      if (min) {
        root.classList.add("ended"); count.textContent = "Run complete";
        nodes.forEach((n) => { const o = n.classList.contains("pinned"); n.classList.toggle("open", o); n.setAttribute("aria-expanded", String(o)); });
      }
      label("↺ Watch again", "Watch the run again");
      idx = frames.length;
    }

    function play() {
      if (idx >= frames.length || idx < 0) { go(0, true); }
      playing = true; label("❚❚ Pause", "Pause the run"); schedule();
    }
    function pause() {
      if (!playing) return;
      playing = false; clearTimeout(timer);
      spent += performance.now() - started;
      const bar = time.children[idx]?.firstChild;
      if (bar) { const w = getComputedStyle(bar).width; bar.style.transition = "none"; bar.style.width = w; }
      label("▶ Play", "Play the run");
    }
    function label(t, a) { playBtn.textContent = t; playBtn.setAttribute("aria-label", a); }

    root.querySelector('[data-act="play"]').addEventListener("click", () => { user = true; sub.setAttribute("aria-live", "polite"); playing ? pause() : play(); });
    root.querySelector('[data-act="prev"]').addEventListener("click", () => { user = true; pause(); go(Math.max(0, Math.min(idx, frames.length) - 1), true); });
    root.querySelector('[data-act="next"]').addEventListener("click", () => { user = true; pause(); go(Math.min(frames.length - 1, idx + 1), true); });
    root.querySelector('[data-act="restart"]').addEventListener("click", () => { user = true; pause(); go(0, true); play(); });
    for (const n of nodes) n.addEventListener("click", () => {
      if (min) {   // open or close this card's details, and keep the run going
        const o = !n.classList.contains("open");
        n.classList.toggle("pinned", o); n.classList.toggle("open", o); n.setAttribute("aria-expanded", String(o));
        return;
      }
      const i = frames.findIndex((f) => f.includes(n));
      if (i < 0) return;
      user = true; pause(); go(i, true);
    });

    build(); go(-1, false);
    narrow.addEventListener("change", () => { build(); draw(false); });
    new ResizeObserver(() => draw(false)).observe(grid);
    document.fonts?.ready.then(() => draw(false));

    // Start once when the chart comes into view, and pause while it is off screen.
    let autoPaused = false, seen = false;
    new IntersectionObserver(([e]) => {
      if (e.isIntersecting) {
        if (!seen && !reduce) { seen = true; play(); }
        else if (autoPaused) { autoPaused = false; play(); }
      } else if (playing) { autoPaused = true; pause(); }
    }, { threshold: 0.35 }).observe(grid);
  }

  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  document.querySelectorAll(".flow[data-flow]").forEach(setup);
})();
