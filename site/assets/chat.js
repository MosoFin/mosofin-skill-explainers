// Chat replay. build.py renders the whole example conversation as HTML (.cm messages). This script hides it,
// then replays it like a live chat: the person's message types into the box and sends, the agent "thinks",
// its reply streams in word by word, tool calls spin and finish, and result cards fill one row at a time.
(() => {
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const ABORT = Symbol("abort");

  function setup(root) {
    const log = root.querySelector(".chat-log");
    const msgs = [...log.querySelectorAll(".cm")];
    const input = root.querySelector(".chat-input"), typed = root.querySelector(".chat-typed"), send = root.querySelector(".chat-send");
    const prog = root.querySelector(".chat-prog span");
    const btn = (a) => root.querySelector(`[data-act="${a}"]`);
    const playBtn = btn("play"), speedBtn = btn("speed");
    let token = 0, paused = true, speed = 1, running = false, done = false;

    // Keep each streamed element's full HTML so the replay can rebuild it word by word.
    const streamable = (m) => [...m.querySelectorAll(".cm-body > p:not(.cm-guard), .cm-body li")];
    msgs.forEach((m) => streamable(m).forEach((el) => { el.dataset.html = el.innerHTML; }));
    root.classList.add("js");

    function hideAll() {
      msgs.forEach((m) => {
        m.classList.add("wait"); m.classList.remove("in", "busy");
        m.querySelectorAll(".cm-body > :not(.cm-name), .cm-body li, .cc tr").forEach((x) => x.classList.add("wait"));
        streamable(m).forEach((el) => { el.innerHTML = el.dataset.html; });
        m.querySelectorAll("details").forEach((d) => { d.open = false; });
      });
      log.querySelectorAll(".cm-dots").forEach((d) => d.remove());
      typed.textContent = ""; input.classList.remove("typing"); send.classList.remove("ready");
      prog.style.width = "0";
    }
    function showAll() {
      msgs.forEach((m) => {
        m.classList.remove("wait", "busy");
        m.querySelectorAll(".wait").forEach((x) => x.classList.remove("wait"));
        streamable(m).forEach((el) => { el.innerHTML = el.dataset.html; });
      });
      log.querySelectorAll(".cm-dots").forEach((d) => d.remove());
      typed.textContent = ""; input.classList.remove("typing"); send.classList.remove("ready");
      prog.style.width = "100%";
    }

    // A sleep that stops while paused, runs faster at 2x, and throws when the run restarts.
    function sleep(ms, tk) {
      return new Promise((res, rej) => {
        let left = ms, last = performance.now();
        const f = (now) => {
          if (tk !== token) return rej(ABORT);
          if (!paused) left -= (now - last) * speed;
          last = now;
          left <= 0 ? res() : requestAnimationFrame(f);
        };
        requestAnimationFrame(f);
      });
    }
    const near = () => log.scrollHeight - log.scrollTop - log.clientHeight < 120;
    function follow(stick) { if (stick) log.scrollTop = log.scrollHeight; }

    async function stream(el, tk) {
      const html = el.dataset.html;
      if (reduce) { el.innerHTML = html; return; }
      const parts = html.split(/(<[^>]+>|\s+)/).filter(Boolean);
      let acc = "";
      el.innerHTML = "";
      for (const p of parts) {
        const stick = near();
        acc += p; el.innerHTML = acc; follow(stick);
        if (!p.startsWith("<") && p.trim()) await sleep(34, tk);
      }
    }

    async function playUser(m, tk) {
      const text = m.querySelector(".cm-bubble").textContent;
      input.classList.add("typing");
      for (let i = 1; i <= text.length; i++) {
        typed.textContent = text.slice(0, i);
        send.classList.toggle("ready", i > 0);
        await sleep(reduce ? 0 : 22, tk);
      }
      await sleep(350, tk);
      send.classList.add("press"); await sleep(140, tk); send.classList.remove("press");
      typed.textContent = ""; input.classList.remove("typing"); send.classList.remove("ready");
      const stick = near();
      m.querySelectorAll(".wait").forEach((x) => x.classList.remove("wait"));
      m.classList.remove("wait"); m.classList.add("in"); follow(stick);
    }

    async function playTool(m, tk) {
      const stick = near();
      m.classList.remove("wait"); m.classList.add("in", "busy"); follow(stick);
      await sleep(1300, tk);
      m.classList.remove("busy");
    }

    async function playAgent(m, tk) {
      const body = m.querySelector(".cm-body");
      let stick = near();
      m.classList.remove("wait"); m.classList.add("in");
      const dots = document.createElement("span");
      dots.className = "cm-dots"; dots.setAttribute("aria-hidden", "true"); dots.innerHTML = "<i></i><i></i><i></i>";
      body.append(dots); follow(stick);
      await sleep(800, tk);
      dots.remove();
      for (const part of [...body.children]) {
        if (!part.classList.contains("wait")) continue;
        stick = near();
        part.classList.remove("wait"); follow(stick);
        if (part.tagName === "P" && !part.classList.contains("cm-guard")) await stream(part, tk);
        else if (part.tagName === "OL") for (const li of part.children) { li.classList.remove("wait"); await stream(li, tk); }
        else if (part.classList.contains("cc")) for (const tr of part.querySelectorAll("tr.wait")) { stick = near(); tr.classList.remove("wait"); follow(stick); await sleep(230, tk); }
        await sleep(part.classList.contains("cm-guard") ? 500 : 250, tk);
      }
    }

    async function run() {
      const tk = ++token;
      running = true; done = false;
      hideAll(); log.scrollTop = 0;
      try {
        await sleep(400, tk);
        for (let i = 0; i < msgs.length; i++) {
          const m = msgs[i];
          if (m.classList.contains("cm-user")) await playUser(m, tk);
          else if (m.classList.contains("cm-tool")) await playTool(m, tk);
          else await playAgent(m, tk);
          prog.style.width = `${(100 * (i + 1)) / msgs.length}%`;
          await sleep(m.classList.contains("cm-user") ? 300 : 900, tk);
        }
        running = false; done = true; paused = true; label();
      } catch (err) { if (err !== ABORT) throw err; }
    }

    function label() {
      playBtn.textContent = done ? "↺ Replay" : paused ? "▶ Play" : "❚❚ Pause";
      playBtn.setAttribute("aria-label", done ? "Replay the conversation" : paused ? "Play the conversation" : "Pause the conversation");
    }
    function play() { paused = false; if (!running) run(); label(); }
    function pause() { paused = true; label(); }

    playBtn.addEventListener("click", () => { user = true; paused ? play() : pause(); });
    btn("restart").addEventListener("click", () => { user = true; running = false; paused = false; run(); label(); });
    speedBtn.addEventListener("click", () => { speed = speed === 1 ? 2 : 1; speedBtn.textContent = speed + "×"; });
    btn("skip").addEventListener("click", () => { user = true; token++; running = false; done = true; paused = true; showAll(); label(); });

    hideAll(); label();
    // Before the first play, show the opening message so the panel is not empty.
    msgs[0]?.classList.remove("wait"); msgs[0]?.querySelectorAll(".wait").forEach((x) => x.classList.remove("wait"));
    let user = false, seen = false, autoPaused = false;
    new IntersectionObserver(([e]) => {
      if (e.isIntersecting) {
        if (!seen && !reduce) { seen = true; play(); }
        else if (autoPaused) { autoPaused = false; play(); }
      } else if (!paused && running) { autoPaused = true; pause(); }
    }, { threshold: 0.4 }).observe(log);
  }

  document.querySelectorAll(".chat[data-chat]").forEach(setup);
})();
