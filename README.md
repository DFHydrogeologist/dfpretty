# dfpretty

> Pretty-print pandas DataFrames as styled interactive HTML tables — with theme switcher and Excel-like column filters.

Opens a standalone browser window (no Jupyter required).

```python
from dfpretty import pretty
pretty(df, theme="tableau", title="Sales Q1")
```

![themes preview](https://raw.githubusercontent.com/YOUR_USERNAME/dfpretty/main/docs/preview.png)

---

## Installation

```bash
# pip
pip install dfpretty

# conda (once on conda-forge)
conda install -c conda-forge dfpretty
```

---

## Usage

```python
import pandas as pd
from dfpretty import pretty

df = pd.read_csv("data.csv")

pretty(df)                                        # dark theme, opens browser
pretty(df, theme="tableau", title="My Table")     # Tableau style
pretty(df, theme="terminal")                      # green-on-black
pretty(df, locale="de-DE")                        # German number formatting
pretty(df, save="report.html", open_browser=False) # save without opening
```

### Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `df` | `pd.DataFrame` | — | DataFrame to display |
| `title` | `str` | `"DataFrame"` | Title in the top bar |
| `theme` | `str` | `"dark"` | Initial colour theme |
| `locale` | `str` | `"en-US"` | BCP-47 locale for number formatting |
| `save` | `str \| Path \| None` | `None` | Save HTML to this path |
| `open_browser` | `bool` | `True` | Open browser automatically |

**Returns:** `Path` — path to the generated HTML file.

---

## Themes

Themes can be switched live in the browser via the buttons in the top bar.

| Name | Style |
|---|---|
| `dark` | Deep blue-slate, blue accents |
| `tableau` | Cream background, charcoal header, orange accent — Tableau-inspired |
| `light` | Clean white, indigo accents |
| `terminal` | Black, green-on-black Matrix style |
| `notion` | Soft white, editorial typography |

---

## Features

- **Column filters** — click ▾ on any column header to filter by value (Excel-style)
- **Global search** — filter across all columns at once
- **Sort** — click any column name to sort ↑ ↓
- **Number formatting** — integers and floats formatted with locale-aware separators
- **Theme switcher** — switch themes live without reopening
- **Save to file** — export a standalone HTML report

---

## Development

```bash
git clone https://github.com/YOUR_USERNAME/dfpretty
cd dfpretty
pip install -e ".[dev]"
pytest
```

---

## License

MIT
