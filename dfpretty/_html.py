"""
dfpretty._html
~~~~~~~~~~~~~~
Builds the self-contained HTML string rendered in the browser.
"""

from __future__ import annotations
import json
from .themes import AVAILABLE_THEMES, build_css_vars


_GOOGLE_FONTS = (
    "https://fonts.googleapis.com/css2?"
    "family=IBM+Plex+Mono:wght@400;600"
    "&family=IBM+Plex+Sans:wght@400;500;600"
    "&family=Geist+Mono:wght@400;600"
    "&family=Merriweather+Sans:wght@400;600"
    "&display=swap"
)

_BASE_CSS = """
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background: var(--bg);
    font-family: var(--font-body);
    color: var(--text);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    transition: background 0.25s, color 0.25s;
  }

  /* Topbar */
  .topbar {
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 12px 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 100;
    gap: 16px;
    flex-wrap: wrap;
  }
  .topbar-title {
    font-family: var(--font-mono);
    font-size: 13px;
    font-weight: 600;
    color: var(--text-bright);
    letter-spacing: 0.04em;
    white-space: nowrap;
  }
  .topbar-meta {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--text-dim);
    white-space: nowrap;
  }
  .topbar-right {
    display: flex;
    align-items: center;
    gap: 6px;
    flex-wrap: wrap;
  }

  /* Theme switcher */
  .theme-label {
    font-family: var(--font-mono);
    font-size: 10px;
    color: var(--text-dim);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-right: 2px;
  }
  .theme-btn {
    padding: 4px 10px;
    border-radius: 6px;
    font-size: 11px;
    font-family: var(--font-mono);
    cursor: pointer;
    border: 1px solid var(--border);
    background: var(--bg2);
    color: var(--text-muted);
    transition: all 0.15s;
    white-space: nowrap;
  }
  .theme-btn:hover { background: var(--surface2); color: var(--text-bright); }
  .theme-btn.active {
    background: var(--accent);
    color: #fff;
    border-color: var(--accent);
  }

  /* Searchbar */
  .searchbar {
    padding: 10px 20px;
    background: var(--bg);
    border-bottom: 1px solid var(--border2);
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .searchbar input {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    color: var(--text-bright);
    font-family: var(--font-body);
    font-size: 13px;
    padding: 7px 12px;
    outline: none;
    width: 300px;
    transition: border-color 0.2s;
  }
  .searchbar input:focus { border-color: var(--accent); }
  .searchbar input::placeholder { color: var(--text-dim); }
  .clear-btn {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    color: var(--text-muted);
    font-size: 12px;
    padding: 7px 12px;
    cursor: pointer;
    font-family: var(--font-body);
    transition: all 0.2s;
  }
  .clear-btn:hover { background: var(--surface2); color: var(--text-bright); }

  /* Table */
  .table-wrap {
    flex: 1;
    overflow: auto;
    padding: 16px 20px 60px;
  }
  table {
    border-collapse: collapse;
    width: 100%;
    font-size: 13px;
    min-width: 400px;
  }
  thead th {
    background: var(--header-bg);
    color: var(--header-text);
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    padding: 0;
    border-bottom: 2px solid var(--th-border);
    border-right: 1px solid var(--border);
    position: sticky;
    top: 0;
    z-index: 10;
    white-space: nowrap;
    transition: background 0.25s;
  }
  thead th:last-child { border-right: none; }

  .th-inner { display: flex; align-items: stretch; }
  .th-label {
    flex: 1;
    padding: 11px 13px;
    cursor: pointer;
    user-select: none;
    display: flex;
    align-items: center;
    gap: 5px;
    transition: color 0.15s;
  }
  .th-label:hover { color: var(--text-bright); }
  .sort-icon { font-size: 10px; opacity: 0.3; transition: opacity 0.2s; }
  .th-label:hover .sort-icon { opacity: 0.7; }
  th.sorted .sort-icon { opacity: 1; color: var(--accent); }

  /* Filter */
  .filter-btn {
    padding: 0 9px;
    cursor: pointer;
    color: var(--text-dim);
    background: transparent;
    border: none;
    border-left: 1px solid var(--border);
    font-size: 12px;
    transition: all 0.15s;
    display: flex;
    align-items: center;
  }
  .filter-btn:hover { color: var(--text-bright); background: var(--surface2); }
  .filter-btn.active { color: var(--accent); }

  .filter-dropdown {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    z-index: 200;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 10px;
    min-width: 210px;
    box-shadow: 0 12px 40px rgba(0,0,0,0.18);
  }
  .filter-dropdown.open { display: block; }

  .filter-search {
    width: 100%;
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 6px;
    color: var(--text-bright);
    font-family: var(--font-body);
    font-size: 12px;
    padding: 6px 10px;
    outline: none;
    margin-bottom: 8px;
  }
  .filter-search:focus { border-color: var(--accent); }

  .filter-options {
    max-height: 210px;
    overflow-y: auto;
    scrollbar-width: thin;
    scrollbar-color: var(--surface2) transparent;
  }
  .filter-option {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 5px 6px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 12px;
    color: var(--text-muted);
    transition: background 0.1s;
  }
  .filter-option:hover { background: var(--surface2); color: var(--text-bright); }
  .filter-option input[type=checkbox] {
    accent-color: var(--accent);
    width: 13px; height: 13px;
    cursor: pointer;
  }

  .filter-actions {
    display: flex;
    gap: 6px;
    margin-top: 8px;
    padding-top: 8px;
    border-top: 1px solid var(--border);
  }
  .filter-actions button {
    flex: 1;
    padding: 6px;
    border-radius: 6px;
    font-size: 11px;
    cursor: pointer;
    font-family: var(--font-body);
    font-weight: 600;
    transition: all 0.15s;
  }
  .btn-apply  { background: var(--accent); color: #fff; border: 1px solid var(--accent); }
  .btn-apply:hover  { background: var(--accent2); }
  .btn-clear  { background: transparent; color: var(--text-muted); border: 1px solid var(--border); }
  .btn-clear:hover { background: var(--surface2); color: var(--text-bright); }

  /* Rows */
  tbody tr { transition: background 0.08s; }
  tbody tr:nth-child(odd)  td { background: var(--row-odd); }
  tbody tr:nth-child(even) td { background: var(--row-even); }
  tbody tr:hover td { background: var(--row-hover) !important; color: var(--text-bright); }

  td {
    padding: 9px 13px;
    border-bottom: 1px solid var(--border2);
    border-right: 1px solid var(--border2);
    white-space: nowrap;
    transition: background 0.08s, color 0.08s;
  }
  td:last-child { border-right: none; }
  td.num {
    font-family: var(--font-mono);
    text-align: right;
    color: var(--num-color);
  }

  /* Footer */
  .footer {
    position: fixed;
    bottom: 0; left: 0; right: 0;
    background: var(--surface);
    border-top: 1px solid var(--border);
    padding: 7px 20px;
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--text-dim);
    display: flex;
    justify-content: space-between;
    z-index: 100;
    transition: background 0.25s;
  }
"""


def build_html(
    data_json: str,
    cols_json: str,
    title: str,
    theme: str,
    locale: str,
) -> str:
    """Return the full self-contained HTML string."""

    theme_buttons = "\n    ".join(
        f'<button class="theme-btn" onclick="setTheme(\'{t}\')">'
        f'{t.capitalize()}</button>'
        for t in AVAILABLE_THEMES
    )

    css_vars = build_css_vars(theme)

    return f"""<!DOCTYPE html>
<html lang="es" data-theme="{theme}">
<head>
<meta charset="UTF-8">
<title>{title}</title>
<link rel="stylesheet" href="{_GOOGLE_FONTS}">
<style>
{css_vars}
{_BASE_CSS}
</style>
</head>
<body>

<div class="topbar">
  <div class="topbar-title">⬡ {title}</div>
  <div class="topbar-right">
    <span class="theme-label">theme</span>
    {theme_buttons}
  </div>
  <div class="topbar-meta" id="meta"></div>
</div>

<div class="searchbar">
  <input type="text" id="globalSearch" placeholder="🔍  Search…" oninput="applyAll()">
  <button class="clear-btn" onclick="clearAll()">✕ Clear filters</button>
</div>

<div class="table-wrap">
  <table id="tbl">
    <thead id="thead"></thead>
    <tbody id="tbody"></tbody>
  </table>
</div>

<div class="footer">
  <span>dfpretty</span>
  <span id="footerRight"></span>
</div>

<script>
const RAW   = {data_json};
const COLS  = {cols_json};
const LOCALE = "{locale}";

let sortCol = null, sortDir = 1;
const activeFilters = {{}};
let openDropdown = null;

const numCols = new Set(
  COLS.filter(c => RAW.every(r => r[c] === null || r[c] === undefined || typeof r[c] === "number"))
);

/* ── Theme ── */
function setTheme(t) {{
  document.documentElement.setAttribute("data-theme", t);
  document.querySelectorAll(".theme-btn").forEach(b =>
    b.classList.toggle("active", b.textContent.toLowerCase() === t)
  );
}}
(function() {{
  const cur = document.documentElement.getAttribute("data-theme");
  document.querySelectorAll(".theme-btn").forEach(b =>
    b.classList.toggle("active", b.textContent.toLowerCase() === cur)
  );
}})();

/* ── Format ── */
function fmt(v) {{
  if (v === null || v === undefined) return "—";
  if (typeof v === "number")
    return Number.isInteger(v)
      ? v.toLocaleString(LOCALE)
      : v.toLocaleString(LOCALE, {{minimumFractionDigits:2, maximumFractionDigits:2}});
  return v;
}}

/* ── Header ── */
function buildHeader() {{
  const tr = document.createElement("tr");
  COLS.forEach(col => {{
    const th = document.createElement("th");
    th.dataset.col = col;
    th.style.position = "relative";
    th.innerHTML = `
      <div class="th-inner">
        <div class="th-label" onclick="sortBy('${{col}}')">
          ${{col}}<span class="sort-icon" id="si-${{col}}">⇅</span>
        </div>
        <button class="filter-btn" id="fb-${{col}}" onclick="toggleDropdown(event,'${{col}}')">▾</button>
        <div class="filter-dropdown" id="fd-${{col}}">
          <input class="filter-search" placeholder="Search…" oninput="renderOptions('${{col}}',this.value)">
          <div class="filter-options" id="fo-${{col}}"></div>
          <div class="filter-actions">
            <button class="btn-clear" onclick="clearFilter('${{col}}')">Clear</button>
            <button class="btn-apply" onclick="closeDropdown()">Apply</button>
          </div>
        </div>
      </div>`;
    tr.appendChild(th);
  }});
  document.getElementById("thead").appendChild(tr);
}}

function uniqueVals(col) {{
  return [...new Set(RAW.map(r => r[col]))].sort((a,b) => {{
    if (a === null) return 1; if (b === null) return -1;
    return a > b ? 1 : -1;
  }});
}}

function renderOptions(col, search="") {{
  const container = document.getElementById(`fo-${{col}}`);
  const vals = uniqueVals(col).filter(v => String(v).toLowerCase().includes(search.toLowerCase()));
  const sel  = activeFilters[col] || new Set(uniqueVals(col).map(String));
  container.innerHTML = vals.map(v => `
    <label class="filter-option">
      <input type="checkbox" value="${{v}}" ${{sel.has(String(v)) ? "checked" : ""}}
        onchange="toggleVal('${{col}}',this.value,this.checked)">
      ${{fmt(v)}}
    </label>`).join("");
}}

function toggleVal(col, val, checked) {{
  if (!activeFilters[col]) activeFilters[col] = new Set(uniqueVals(col).map(String));
  checked ? activeFilters[col].add(val) : activeFilters[col].delete(val);
  document.getElementById(`fb-${{col}}`).classList.toggle(
    "active", activeFilters[col].size < uniqueVals(col).length
  );
  applyAll();
}}

function clearFilter(col) {{
  delete activeFilters[col];
  document.getElementById(`fb-${{col}}`).classList.remove("active");
  renderOptions(col);
  applyAll();
}}

function clearAll() {{
  COLS.forEach(c => {{ delete activeFilters[c]; document.getElementById(`fb-${{c}}`).classList.remove("active"); }});
  document.getElementById("globalSearch").value = "";
  applyAll();
}}

function toggleDropdown(e, col) {{
  e.stopPropagation();
  const fd = document.getElementById(`fd-${{col}}`);
  if (openDropdown && openDropdown !== fd) openDropdown.classList.remove("open");
  const isOpen = fd.classList.toggle("open");
  openDropdown = isOpen ? fd : null;
  if (isOpen) renderOptions(col);
}}

function closeDropdown() {{
  if (openDropdown) {{ openDropdown.classList.remove("open"); openDropdown = null; }}
}}

document.addEventListener("click", e => {{
  if (!e.target.closest(".filter-dropdown") && !e.target.closest(".filter-btn")) closeDropdown();
}});

function sortBy(col) {{
  if (sortCol === col) sortDir *= -1; else {{ sortCol = col; sortDir = 1; }}
  COLS.forEach(c => {{
    document.getElementById(`si-${{c}}`).textContent = "⇅";
    document.querySelector(`[data-col="${{c}}"]`).classList.remove("sorted");
  }});
  document.getElementById(`si-${{col}}`).textContent = sortDir === 1 ? "↑" : "↓";
  document.querySelector(`[data-col="${{col}}"]`).classList.add("sorted");
  applyAll();
}}

function applyAll() {{
  const q = document.getElementById("globalSearch").value.toLowerCase();
  let rows = [...RAW];
  COLS.forEach(col => {{
    if (activeFilters[col]) rows = rows.filter(r => activeFilters[col].has(String(r[col])));
  }});
  if (q) rows = rows.filter(r => COLS.some(c => String(r[c]).toLowerCase().includes(q)));
  if (sortCol) rows.sort((a,b) => {{
    const va = a[sortCol], vb = b[sortCol];
    if (va === null) return 1; if (vb === null) return -1;
    return (va > vb ? 1 : va < vb ? -1 : 0) * sortDir;
  }});

  document.getElementById("tbody").innerHTML = rows.map(r =>
    `<tr>${{COLS.map(c=>`<td class="${{numCols.has(c)?"num":""}}">${{fmt(r[c])}}</td>`).join("")}}</tr>`
  ).join("");

  document.getElementById("meta").textContent = `${{rows.length}} / ${{RAW.length}} rows`;
  document.getElementById("footerRight").textContent = `${{rows.length}} rows · ${{COLS.length}} cols`;
}}

buildHeader();
applyAll();
</script>
</body>
</html>"""
