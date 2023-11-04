from playwright.sync_api import Page, Locator
from support.page_objects.base_page import BasePage

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self._userName: Locator = self.page.locator('#login-username')
        self._password: Locator = self.page.locator('#login-password')
        self._signInButton: Locator = self.page.locator('button[data-arrow-down="#login-username"]')

    def open(self, url: str):
        self.page.goto(url)

    def login_to_email(self, userName: str, password: str):
        self._userName.fill(userName)
        self._signInButton.click()
        self._password.fill(password)
        self._signInButton.click()
