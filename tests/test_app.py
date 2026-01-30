# tests/test_app.py
import sys
from pathlib import Path
import warnings
import pytest
from dash.testing.application_runners import import_app
from selenium.webdriver.common.by import By

# Silence that urllib3 / selenium deprecation warning (harmless for tests)
warnings.filterwarnings(
    "ignore",
    message="HTTPResponse.getheader() is deprecated",
    category=DeprecationWarning,
)

# Ensure project root is importable so `import_app("app")` finds app.py
sys.path.append(str(Path(__file__).resolve().parents[1]))


@pytest.fixture
def app():
    return import_app("app")


def _wait_for_any_selector(dash_duo, css_selectors=None, xpaths=None, timeout_each=7):
    """
    Try CSS selectors first (each with timeout_each), then XPath fallbacks.
    Returns the first found selenium WebElement or raises the last exception.
    """
    css_selectors = css_selectors or []
    xpaths = xpaths or []

    last_exc = None
    # Try CSS selectors
    for sel in css_selectors:
        try:
            return dash_duo.wait_for_element(sel, timeout=timeout_each)
        except Exception as e:
            last_exc = e
    # Try XPaths directly using driver
    for xp in xpaths:
        try:
            # use a short explicit wait loop for the xpath
            return dash_duo.wait_for_element_by_xpath(xp, timeout=timeout_each)
        except Exception as e:
            last_exc = e

    # If nothing matched, raise the final exception for debugging info
    raise last_exc


def test_header_present(dash_duo, app):
    dash_duo.start_server(app)
    dash_duo.wait_for_page()
    header = dash_duo.wait_for_element("h1", timeout=10)
    assert header.text.strip() == "Soul Foods Pink Morsel Sales Dashboard"


def test_graph_present(dash_duo, app):
    dash_duo.start_server(app)
    dash_duo.wait_for_page()

    # Try several fallbacks because different Dash/Plotly versions render graph wrappers differently
    css_candidates = [
        "#sales-graph",                          # expected id
        'div[data-dash-componentid="sales-graph"]',  # dash sometimes sets this attr
        ".js-plotly-plot",                       # plotly canvas wrapper
    ]
    xpath_candidates = [
        '//*[@id="sales-graph"]',
        '//*[contains(@class,"js-plotly-plot")]',
        '//div[contains(@data-dash-componentid,"sales-graph")]',
    ]

    graph_el = _wait_for_any_selector(
        dash_duo, css_selectors=css_candidates, xpaths=xpath_candidates, timeout_each=7
    )
    assert graph_el is not None


def test_region_picker_present(dash_duo, app):
    dash_duo.start_server(app)
    dash_duo.wait_for_page()

    css_candidates = [
        "#region-filter",  # expected id
        'div[data-dash-componentid="region-filter"]',
    ]
    xpath_candidates = [
        '//*[@id="region-filter"]',
        '//label[contains(normalize-space(.),"Select Region")]',
        '//div[contains(., "Select Region")]',
    ]

    picker_el = _wait_for_any_selector(
        dash_duo, css_selectors=css_candidates, xpaths=xpath_candidates, timeout_each=7
    )
    assert picker_el is not None
