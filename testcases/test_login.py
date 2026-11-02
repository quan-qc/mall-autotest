"""登录认证模块接口用例。"""
import allure
import pytest

from utils.assert_util import assert_success

FEATURE = "登录认证"


@allure.feature(FEATURE)
class TestLogin:
    @allure.story("正确账号密码登录")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.smoke
    def test_login_success(self, login_api, api_config):
        data = assert_success(login_api.login(api_config["username"], api_config["password"]))
        assert data["tokenHead"] == "Bearer "
        assert len(data["token"].split(".")) == 3, "JWT 应由三段组成"

    @allure.story("错误密码登录失败")
    def test_login_wrong_password(self, login_api, api_config):
        result = login_api.login(api_config["username"], "wrong_password").json()
        assert result["code"] == 500
        assert result["message"] == "密码不正确"

    @allure.story("用户名为空触发参数校验")
    def test_login_empty_username(self, login_api):
        result = login_api.login("", "macro123").json()
        assert result["code"] == 404
        assert "username" in result["message"]

    @allure.story("未携带 token 访问受保护接口")
    def test_access_without_token(self, unauth_client):
        result = unauth_client.get("/product/list").json()
        assert result["code"] == 401
        assert "暂未登录" in result["message"]

    @allure.story("伪造 token 访问受保护接口")
    def test_access_with_fake_token(self, fake_token_client):
        result = fake_token_client.get("/product/list").json()
        assert result["code"] == 401

    @allure.story("获取当前登录管理员信息")
    def test_admin_info(self, auth_login_api):
        data = assert_success(auth_login_api.info())
        assert data["username"] == "admin"
        assert isinstance(data["menus"], list) and data["menus"], "应返回菜单权限"
        assert isinstance(data["roles"], list) and data["roles"], "应返回角色"
