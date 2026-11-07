// Browser test for one skill's chat replay on its landing page.
//
// usage:  python3 build.py --stage _site
//         python3 -m http.server 8765 --directory _site      (in the background)
//         node .claude/skills/write-chat-replay/scripts/test_chat.js <skill> [base-url]
//
// base-url defaults to http://127.0.0.1:8765. Exit code 1 means at least one check failed.
// Checks, at 1280px (light) and 390px (dark):
//   - the page loads with no script error and no failed request
//   - the chat starts playing by itself when it comes into view
//   - "Show all" shows every message, and every MosoFin call ends ticked, with its summary
//   - the four assistant styles change the name and the logo, and the message text stays the same
//   - no safeguard notes, no sideways scrolling, and every card and message fits its box
const { chromium } = require("playwright");

const [skill, base = "http://127.0.0.1:8765"] = process.argv.slice(2);
if (!skill) { console.error("usage: node test_chat.js <skill> [base-url]"); process.exit(2); }
const STYLES = ["chatgpt", "claude", "muse", "grok"];

(async () => {
  const browser = await chromium.launch();
  const failures = [];
  const fail = (tag, msg) => failures.push(`${tag}: ${msg}`);

  for (const [width, scheme, tag] of [[1280, "light", "desktop"], [390, "dark", "phone"]]) {
    const ctx = await browser.newContext({ viewport: { width, height: 900 }, colorScheme: scheme });
    const page = await ctx.newPage();
    const errors = [];
    page.on("pageerror", (e) => errors.push("script error: " + e.message));
    page.on("response", (r) => { if (r.status() >= 400) errors.push(`${r.status()} ${r.url()}`); });

    await page.goto(`${base}/skills/${skill}/`, { waitUntil: "networkidle" });
    if (!(await page.locator(".chat[data-chat]").count())) { fail(tag, "no chat replay on the page"); await ctx.close(); continue; }

    await page.locator(".chat").scrollIntoViewIfNeeded();
    await page.waitForTimeout(2500);
    const playLabel = (await page.locator('.chat [data-act="play"]').textContent()).trim();
    if (!/Pause/.test(playLabel)) fail(tag, `the chat did not start by itself (button says "${playLabel}")`);

    await page.click('.chat [data-act="skip"]');
    const state = await page.evaluate(() => {
      const r = document.querySelector(".chat");
      return {
        total: r.querySelectorAll(".chat-log .cm").length,
        hidden: r.querySelectorAll(".chat-log .cm.wait").length,
        pendingCalls: r.querySelectorAll(".mf-rows li.pend, .mf-rows li.run").length,
        mfCards: r.querySelectorAll(".cm-mf").length,
        summaries: [...r.querySelectorAll(".mf-sum")].filter((x) => getComputedStyle(x).display !== "none").length,
        summaryFields: r.querySelectorAll(".mf-sum").length,
        guards: r.querySelectorAll(".cm-guard").length,
        logoOk: [...r.querySelectorAll(".mf-logo")].every((i) => i.complete && i.naturalWidth > 0),
        overflow: document.documentElement.scrollWidth > innerWidth,
        // A card must fit its box. A table inside .cc-scroll may scroll on purpose.
        tooWide: [...r.querySelectorAll(".cc")].filter((cc) => !cc.querySelector(".cc-scroll"))
                   .filter((cc) => { const t = cc.querySelector("table"); return t && t.scrollWidth > cc.clientWidth + 1; })
                   .map((cc) => cc.querySelector(".cc-title")?.textContent || cc.className)
                 .concat([...r.querySelectorAll(".chat-log .cm")].filter((m) => m.scrollWidth > m.clientWidth + 1)
                   .map((m) => "message: " + m.textContent.trim().slice(0, 40))),
      };
    });
    if (state.hidden) fail(tag, `"Show all" left ${state.hidden} of ${state.total} messages hidden`);
    if (state.pendingCalls) fail(tag, `${state.pendingCalls} MosoFin call(s) did not finish`);
    if (state.summaries !== state.summaryFields) fail(tag, "a MosoFin card summary is not shown");
    if (state.mfCards && !state.logoOk) fail(tag, "the MosoFin logo did not load");
    if (state.guards) fail(tag, `${state.guards} safeguard note(s) in the chat. A real chat shows none`);
    if (state.overflow) fail(tag, "the page scrolls sideways");
    for (const t of state.tooWide) fail(tag, `wider than its box: ${t}`);

    // The words of every message, without the assistant's name, must be the same in every style.
    const words = () => page.evaluate(() => [...document.querySelectorAll(".chat-log .cm")].map((m) => {
      const c = m.cloneNode(true);
      c.querySelectorAll(".cm-name, .cm-av").forEach((x) => x.remove());
      return c.textContent.replace(/\s+/g, " ").trim();
    }).join("\n"));
    let first = null;
    for (const ai of STYLES) {
      const btn = page.locator(`.chat .ai-btn[data-ai="${ai}"]`);
      if (!(await btn.count())) { fail(tag, `no ${ai} button`); continue; }
      await btn.click();
      const s = await page.evaluate(() => {
        const r = document.querySelector(".chat");
        return { ai: r.dataset.ai, names: [...new Set([...r.querySelectorAll(".cm-name")].map((n) => n.textContent))],
                 logos: [...new Set([...r.querySelectorAll(".cm-av use")].map((u) => u.getAttribute("href")))] };
      });
      if (s.ai !== ai || s.logos.length !== 1 || s.logos[0] !== `#ai-${ai}` || s.names.length !== 1)
        fail(tag, `the ${ai} style did not switch cleanly: ${JSON.stringify(s)}`);
      const w = await words();
      if (first === null) first = w;
      else if (w !== first) fail(tag, `the message text changed in the ${ai} style`);
    }
    await page.click('.chat .ai-btn[data-ai="claude"]');

    for (const e of errors) fail(tag, e);
    console.log(`${tag}: ${state.total} messages, ${state.mfCards} MosoFin card(s), ${errors.length} error(s)`);
    await ctx.close();
  }

  await browser.close();
  if (failures.length) { console.log("FAILED\n  " + failures.join("\n  ")); process.exit(1); }
  console.log(`PASSED: ${skill} chat replay`);
})();
