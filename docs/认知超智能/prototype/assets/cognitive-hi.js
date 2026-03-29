/**
 * 主题切换 + 可选的层栈键盘导航
 */
(function () {
  const STORAGE_KEY = "cognitive-hi-theme";

  function getPreferredTheme() {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved === "light" || saved === "dark") return saved;
    return window.matchMedia("(prefers-color-scheme: light)").matches
      ? "light"
      : "dark";
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem(STORAGE_KEY, theme);
    document.querySelectorAll("[data-theme-toggle]").forEach((btn) => {
      btn.setAttribute("aria-pressed", theme === "light" ? "true" : "false");
      btn.textContent = theme === "light" ? "深色" : "浅色";
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    applyTheme(getPreferredTheme());
    document.querySelectorAll("[data-theme-toggle]").forEach((btn) => {
      btn.addEventListener("click", () => {
        const next =
          document.documentElement.getAttribute("data-theme") === "light"
            ? "dark"
            : "light";
        applyTheme(next);
      });
    });
  });
})();
