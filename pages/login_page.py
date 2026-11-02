"""登录页面对象。"""
from pages.base_page import BasePage


class LoginPage(BasePage):
    PATH = "/login"

    def open_login(self):
        self.open(self.PATH)

    def login(self, username: str, password: str):
        self.page.locator('input[name="username"]').fill(username)
        self.page.locator('input[name="password"]').fill(password)
        self.page.get_by_role("button", name="登录", exact=True).click()
