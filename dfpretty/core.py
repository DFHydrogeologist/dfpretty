"""
dfpretty.core
~~~~~~~~~~~~~
Main entry point: the pretty() function.
"""

from __future__ import annotations
import json
import tempfile
import webbrowser
from pathlib import Path

import pandas as pd

from .themes import AVAILABLE_THEMES
from ._html import build_html


def pretty(
    df: pd.DataFrame,
    title: str = "DataFrame",
    theme: str = "dark",
    locale: str = "en-US",
    save: str | Path | None = None,
    open_browser: bool = True,
) -> Path:
    """
    Render a DataFrame as a styled interactive table in the browser.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to display.
    title : str
        Window / page title shown in the top bar.
    theme : str
        Initial colour theme. One of: 'dark', 'tableau', 'light',
        'terminal', 'notion'.  Can be changed live in the browser.
    locale : str
        BCP-47 locale string used by Intl.NumberFormat for number
        formatting (e.g. 'en-US', 'es-ES', 'de-DE').
    save : str | Path | None
        If given, save the HTML file at this path instead of a
        temporary file.  The file persists after the browser closes.
    open_browser : bool
        If False, build the file but don't launch the browser.
        Useful for testing or headless environments.

    Returns
    -------
    Path
        Path to the generated HTML file.

    Examples
    --------
    >>> import pandas as pd
    >>> from dfpretty import pretty
    >>> df = pd.DataFrame({"x": [1, 2], "y": ["a", "b"]})
    >>> pretty(df)
    >>> pretty(df, theme="tableau", title="My Data")
    >>> pretty(df, save="output.html", open_browser=False)
    """
    if theme not in AVAILABLE_THEMES:
        raise ValueError(
            f"Unknown theme '{theme}'. "
            f"Choose one of: {', '.join(AVAILABLE_THEMES)}"
        )

    data_json = df.to_json(orient="records")
    cols_json = json.dumps(list(df.columns))

    html = build_html(
        data_json=data_json,
        cols_json=cols_json,
        title=title,
        theme=theme,
        locale=locale,
    )

    if save is not None:
        out_path = Path(save)
        out_path.write_text(html, encoding="utf-8")
    else:
        tmp = tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".html",
            delete=False,
            encoding="utf-8",
            prefix="dfpretty_",
        )
        tmp.write(html)
        tmp.close()
        out_path = Path(tmp.name)

    if open_browser:
        webbrowser.open(out_path.as_uri())
        print(f"✓ dfpretty [{theme}]  →  {out_path}")

    return out_path
