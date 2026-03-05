"""Basic tests for dfpretty."""
import pandas as pd
import pytest
from dfpretty import pretty, AVAILABLE_THEMES


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "name":    ["Alice", "Bob", "Carol"],
        "score":   [95.5, 82.0, 78.3],
        "rank":    [1, 2, 3],
        "active":  [True, False, True],
    })


def test_returns_path(tmp_path, sample_df):
    out = pretty(sample_df, save=tmp_path / "out.html", open_browser=False)
    assert out.exists()
    assert out.suffix == ".html"


def test_html_contains_title(tmp_path, sample_df):
    out = pretty(sample_df, title="My Test", save=tmp_path / "out.html", open_browser=False)
    content = out.read_text()
    assert "My Test" in content


def test_html_contains_data(tmp_path, sample_df):
    out = pretty(sample_df, save=tmp_path / "out.html", open_browser=False)
    content = out.read_text()
    assert "Alice" in content
    assert "95.5" in content


def test_all_themes(tmp_path, sample_df):
    for theme in AVAILABLE_THEMES:
        out = pretty(sample_df, theme=theme, save=tmp_path / f"{theme}.html", open_browser=False)
        assert out.exists()
        content = out.read_text()
        assert f'data-theme="{theme}"' in content


def test_invalid_theme(sample_df):
    with pytest.raises(ValueError, match="Unknown theme"):
        pretty(sample_df, theme="neon_pink", open_browser=False)


def test_available_themes_list():
    assert "dark" in AVAILABLE_THEMES
    assert "tableau" in AVAILABLE_THEMES
    assert len(AVAILABLE_THEMES) == 5
