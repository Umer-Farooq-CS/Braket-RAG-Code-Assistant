export type ThemeName = "light" | "dark";

const THEME_KEY = "braket-rag-theme";

export function getInitialTheme(): ThemeName {
  if (typeof globalThis === "undefined" || !("window" in globalThis)) {
    return "dark";
  }
  const stored = globalThis.window.localStorage.getItem(THEME_KEY) as ThemeName | null;
  if (stored === "light" || stored === "dark") return stored;
  const prefersDark = globalThis.window.matchMedia?.("(prefers-color-scheme: dark)").matches;
  return prefersDark ? "dark" : "light";
}

export function applyTheme(theme: ThemeName): void {
  if (typeof globalThis === "undefined" || !("document" in globalThis) || !("window" in globalThis)) {
    return;
  }
  const root = globalThis.document.documentElement;
  root.dataset.theme = theme;
  globalThis.window.localStorage.setItem(THEME_KEY, theme);
}

