"""
dfpretty.themes
~~~~~~~~~~~~~~~
CSS variable definitions for each built-in theme.
Adding a custom theme: add a new key to THEMES with the required variables.
"""

THEMES: dict[str, dict[str, str]] = {
    "dark": {
        "bg":           "#0f172a",
        "bg2":          "#111827",
        "surface":      "#1e293b",
        "surface2":     "#334155",
        "border":       "#334155",
        "border2":      "#1e293b",
        "text":         "#cbd5e1",
        "text_dim":     "#475569",
        "text_muted":   "#94a3b8",
        "text_bright":  "#f1f5f9",
        "accent":       "#3b82f6",
        "accent2":      "#2563eb",
        "num_color":    "#93c5fd",
        "row_odd":      "#111827",
        "row_even":     "#0f172a",
        "row_hover":    "#1e293b",
        "header_bg":    "#1e293b",
        "header_text":  "#94a3b8",
        "th_border":    "#3b82f6",
        "font_body":    "'IBM Plex Sans', sans-serif",
        "font_mono":    "'IBM Plex Mono', monospace",
    },
    "tableau": {
        "bg":           "#f5f5f2",
        "bg2":          "#eeede9",
        "surface":      "#ffffff",
        "surface2":     "#e8e7e3",
        "border":       "#d1cfc9",
        "border2":      "#e8e7e3",
        "text":         "#3b3935",
        "text_dim":     "#8a8780",
        "text_muted":   "#6b6966",
        "text_bright":  "#1a1917",
        "accent":       "#1f6bb0",
        "accent2":      "#174f82",
        "num_color":    "#1f6bb0",
        "row_odd":      "#ffffff",
        "row_even":     "#f5f5f2",
        "row_hover":    "#eaf2fb",
        "header_bg":    "#3b3935",
        "header_text":  "#e8e7e3",
        "th_border":    "#e8702a",
        "font_body":    "'Merriweather Sans', sans-serif",
        "font_mono":    "'IBM Plex Mono', monospace",
    },
    "light": {
        "bg":           "#f8fafc",
        "bg2":          "#f1f5f9",
        "surface":      "#ffffff",
        "surface2":     "#e2e8f0",
        "border":       "#e2e8f0",
        "border2":      "#f1f5f9",
        "text":         "#334155",
        "text_dim":     "#94a3b8",
        "text_muted":   "#64748b",
        "text_bright":  "#0f172a",
        "accent":       "#6366f1",
        "accent2":      "#4f46e5",
        "num_color":    "#6366f1",
        "row_odd":      "#ffffff",
        "row_even":     "#f8fafc",
        "row_hover":    "#eef2ff",
        "header_bg":    "#f1f5f9",
        "header_text":  "#475569",
        "th_border":    "#6366f1",
        "font_body":    "'IBM Plex Sans', sans-serif",
        "font_mono":    "'IBM Plex Mono', monospace",
    },
    "terminal": {
        "bg":           "#0d0d0d",
        "bg2":          "#111111",
        "surface":      "#1a1a1a",
        "surface2":     "#2a2a2a",
        "border":       "#2a2a2a",
        "border2":      "#1a1a1a",
        "text":         "#a3e635",
        "text_dim":     "#4d7c0f",
        "text_muted":   "#65a30d",
        "text_bright":  "#d9f99d",
        "accent":       "#4ade80",
        "accent2":      "#22c55e",
        "num_color":    "#86efac",
        "row_odd":      "#111111",
        "row_even":     "#0d0d0d",
        "row_hover":    "#1a2e1a",
        "header_bg":    "#1a1a1a",
        "header_text":  "#4ade80",
        "th_border":    "#4ade80",
        "font_body":    "'Geist Mono', monospace",
        "font_mono":    "'Geist Mono', monospace",
    },
    "notion": {
        "bg":           "#ffffff",
        "bg2":          "#f7f6f3",
        "surface":      "#ffffff",
        "surface2":     "#f1f1ef",
        "border":       "#e9e9e7",
        "border2":      "#f1f1ef",
        "text":         "#37352f",
        "text_dim":     "#9b9a97",
        "text_muted":   "#6b6a68",
        "text_bright":  "#1a1a1a",
        "accent":       "#2eaadc",
        "accent2":      "#0e8fc4",
        "num_color":    "#0e8fc4",
        "row_odd":      "#ffffff",
        "row_even":     "#f7f6f3",
        "row_hover":    "#f1f1ef",
        "header_bg":    "#f7f6f3",
        "header_text":  "#9b9a97",
        "th_border":    "#e9e9e7",
        "font_body":    "'IBM Plex Sans', sans-serif",
        "font_mono":    "'IBM Plex Mono', monospace",
    },
}

AVAILABLE_THEMES = list(THEMES.keys())


def build_css_vars(theme_name: str) -> str:
    """Return a CSS :root block with the variables for *theme_name*."""
    if theme_name not in THEMES:
        raise ValueError(
            f"Unknown theme '{theme_name}'. "
            f"Available: {', '.join(AVAILABLE_THEMES)}"
        )
    t = THEMES[theme_name]
    lines = ["  :root {"]
    for k, v in t.items():
        css_key = "--" + k.replace("_", "-")
        lines.append(f"    {css_key}: {v};")
    lines.append("  }")
    return "\n".join(lines)
