from playwright.sync_api import Page, Locator, expect
from support.page_objects.base_page import BasePage

class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.create_email_button: Locator = self.page.locator('a[data-command="compose:new"]')
        self.send_email_button: Locator = self.page.locator('button[data-command="compose:send"]:not([class="mobile"])')
        self.recipient_field: Locator = self.page.locator('input[placeholder="Komu…"]')
        self.subject_field: Locator = self.page.locator('input[placeholder="Předmět…"]')
        self.email_body_field: Locator = self.page.locator('div[placeholder="Text e-mailu…"]')
        self.file_upload_button: Locator = self.page.locator('button[title="Přidat přílohu"]')
        self.attachment: Locator = self.page.locator('li[class="attachment"]')
        self.sent_email_nav: Locator = self.page.locator('a[title="Odeslané"]')
        self.last_sent_email_name: Locator = self.page.locator('(//a[@class="name"])[1]')
        self.last_sent_email_subject: Locator = self.page.locator('(//a[@class="subject"])[1]')
        self.notification: Locator = self.page.locator('div.notification')
        self.login_widget: Locator = self.page.locator('szn-login-widget[data-dot="login-badge"]')
        self.login_section: Locator = self.page.locator('#login')
        self.users_button: Locator = self.page.locator('#badge')
        self.log_out_button: Locator = self.page.locator('[data-dot="logout"]')

    def send_email(self, recipient, subject, email_body, file_upload_path):
        self.create_email_button.click()
        self.recipient_field.fill(recipient)
        self.subject_field.fill(subject)
        self.email_body_field.fill(email_body)
        with self.page.expect_file_chooser() as fc_info:
            self.file_upload_button.click()
            file_chooser = fc_info.value
            file_chooser.set_files(file_upload_path)    
        expect(self.attachment).to_be_visible()
        self.send_email_button.click()
        expect(self.notification).to_be_visible()

    def check_that_email_was_sent(self, recipient, subject):
        self.sent_email_nav.click()
        assert self.last_sent_email_name.inner_text() == recipient
        assert self.last_sent_email_subject.inner_text() == subject

    def log_out(self):
        self.users_button.click()
        self.log_out_button.click()
        expect(self.login_section).to_be_visible()
