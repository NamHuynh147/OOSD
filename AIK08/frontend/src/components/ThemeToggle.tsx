import { useEffect, useState } from "react";

type Theme = "dark" | "light";
const STORAGE_KEY = "aik08-theme";

function getInitialTheme(): Theme {
  try {
    const saved = window.localStorage.getItem(STORAGE_KEY);
    const theme: Theme = saved === "light" ? "light" : "dark";
    document.documentElement.dataset.theme = theme;
    return theme;
  } catch {
    return "dark";
  }
}

export function ThemeToggle() {
  const [theme, setTheme] = useState<Theme>(getInitialTheme);

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    try {
      window.localStorage.setItem(STORAGE_KEY, theme);
    } catch {
      // Theme still works for the current page when storage is unavailable.
    }
  }, [theme]);

  const isDark = theme === "dark";

  return (
    <button
      type="button"
      className="theme-toggle"
      onClick={() =>
        setTheme((current) => (current === "dark" ? "light" : "dark"))
      }
      aria-label={isDark ? "Chuyển sang Light Mode" : "Chuyển sang Dark Mode"}
      aria-pressed={!isDark}
      title={isDark ? "Chuyển sang Light Mode" : "Chuyển sang Dark Mode"}
    >
      <span className="theme-toggle-icon" aria-hidden="true">
        {isDark ? "☀" : "☾"}
      </span>
      <span>{isDark ? "Light Mode" : "Dark Mode"}</span>
    </button>
  );
}
