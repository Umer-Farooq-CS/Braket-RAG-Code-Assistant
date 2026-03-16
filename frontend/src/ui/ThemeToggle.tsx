import React from "react";
import type { ThemeName } from "../theme";

interface ThemeToggleProps {
  theme: ThemeName;
  onChange: (theme: ThemeName) => void;
}

export const ThemeToggle: React.FC<ThemeToggleProps> = ({ theme, onChange }) => {
  const isDark = theme === "dark";

  return (
    <button
      type="button"
      className="theme-toggle"
      onClick={() => onChange(isDark ? "light" : "dark")}
      aria-label="Toggle light/dark theme"
    >
      <span className="theme-toggle-track">
        <span className="theme-toggle-thumb" data-mode={theme} />
      </span>
      <span className="theme-toggle-label">{isDark ? "Dark" : "Light"} mode</span>
    </button>
  );
};

