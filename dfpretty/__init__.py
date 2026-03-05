"""
dfpretty
~~~~~~~~
Pretty-print pandas DataFrames as styled interactive HTML tables
that open in your browser — with theme switcher and Excel-like filters.

Basic usage::

    import pandas as pd
    from dfpretty import pretty

    df = pd.DataFrame(...)
    pretty(df)                              # dark theme (default)
    pretty(df, theme="tableau")
    pretty(df, theme="terminal", title="My Results")
    pretty(df, save="report.html", open_browser=False)

Available themes: dark · tableau · light · terminal · notion
"""

from .core import pretty
from .themes import AVAILABLE_THEMES

__all__ = ["pretty", "AVAILABLE_THEMES"]
__version__ = "0.1.0"
