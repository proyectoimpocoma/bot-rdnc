"""Crea una nueva página de Playwright para interactuar con el sitio web de RNDC."""

from playwright.sync_api import sync_playwright


def new_rndc_page():
    """Crea una nueva página de Playwright para interactuar con el sitio web de RNDC."""
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False, channel="chrome", timeout=30000)
    context = browser.new_context(accept_downloads=True)
    page = context.new_page()  # ✅ Correcto: context.new_page(), no browser.new_page()
    return browser, context, page
