import pytest
from playwright.sync_api import Page
from slugify import slugify
from pathlib import Path
from support.helpers.gmail_client import GmailClient
from support.page_objects.login_page import LoginPage
from support.page_objects.home_page import HomePage

class Context():
    def __init__(self, page: Page):
        self.gmail_client = GmailClient()
        self.home_page = HomePage(page)
        self.login_page = LoginPage(page)

@pytest.fixture()
def poms(page):
    return Context(page)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    screen_file = ''
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    if report.when == "call":
        xfail = hasattr(report, "wasxfail")
        # if the test fails, take a screenshot
        if report.failed or xfail and "page" in item.funcargs:
            page = item.funcargs["page"]
            screenshot_dir = Path("html_report/screenshots")
            screenshot_dir.mkdir(exist_ok=True)
            screenshot_name = f"{slugify(item.nodeid)}.png"
            screen_file = str(screenshot_dir / screenshot_name)
            page.screenshot(path=screen_file)

        if (report.skipped and xfail) or (report.failed and not xfail):
            # add the screenshots to the html report
            extra.append(pytest_html.extras.png(f"screenshots/{screenshot_name}"))
        report.extra = extra