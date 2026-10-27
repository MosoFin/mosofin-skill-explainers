(() => {
  const root = document.documentElement;
  const toggle = document.querySelector(".theme-toggle");
  const media = window.matchMedia("(prefers-color-scheme: dark)");

  function activeTheme() {
    return root.dataset.theme || (media.matches ? "dark" : "light");
  }

  function updateControl() {
    if (!toggle) return;
    const dark = activeTheme() === "dark";
    toggle.setAttribute("aria-label", `Switch to ${dark ? "light" : "dark"} mode`);
    toggle.title = `Switch to ${dark ? "light" : "dark"} mode`;
    const glyph = toggle.querySelector(".theme-glyph");
    const label = toggle.querySelector(".theme-name");
    if (glyph) glyph.textContent = dark ? "☼" : "◐";
    if (label) label.textContent = dark ? "Dark" : "Light";
  }

  if (toggle) {
    updateControl();
    toggle.addEventListener("click", () => {
      const next = activeTheme() === "dark" ? "light" : "dark";
      root.dataset.theme = next;
      try { localStorage.setItem("mosofin-theme", next); } catch {}
      updateControl();
    });
  }

  media.addEventListener?.("change", () => {
    if (!root.dataset.theme) updateControl();
  });
})();
