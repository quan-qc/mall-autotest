"""UI 登录场景。"""
import allure
import pytest
from playwright.sync_api import expect

from pages.login_page import LoginPage

pytestmark = pytest.mark.ui


@allure.feature("UI-登录认证")
class TestUILogin:
    @allure.story("正确账号密码登录成功")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_login_success(self, page, api_config, ui_base_url):
        login_page = LoginPage(page, ui_base_url)
        login_page.open_login()
        login_page.login(api_config["username"], api_config["password"])

        expect(page).to_have_url(f"{ui_base_url}/#/home")
        expect(page.locator(".avatar-container")).to_be_visible()
        expect(page.locator(".sidebar-container")).to_be_visible()

    @allure.story("错误密码登录失败并提示")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_wrong_password(self, page, api_config, ui_base_url):
        login_page = LoginPage(page, ui_base_url)
        login_page.open_login()
        login_page.login(api_config["username"], "wrong_password")

        error_message = page.locator(".el-message--error")
        expect(error_message).to_be_visible()
        expect(error_message).to_contain_text("密码不正确")
        expect(page).to_have_url(f"{ui_base_url}/#/login")
