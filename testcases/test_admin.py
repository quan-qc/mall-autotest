"""后台用户与角色接口用例。"""
import time

import allure
import pytest

from utils.assert_util import assert_page, assert_success
from utils.data_loader import load_yaml, render

FEATURE = "用户与角色"


@allure.feature(FEATURE)
class TestAdmin:
    @allure.story("管理员列表-默认分页")
    @pytest.mark.smoke
    def test_admin_list(self, admin_api):
        page = assert_page(admin_api.list(), page_size=5, page_num=1)
        assert page["total"] > 0
        assert "username" in page["list"][0]

    @allure.story("管理员详情")
    def test_admin_detail(self, admin_api):
        first = assert_page(admin_api.list(pageSize=1))["list"][0]
        detail = assert_success(admin_api.detail(first["id"]))
        assert detail["id"] == first["id"]
        assert detail["username"] == first["username"]

    @allure.story("管理员角色列表")
    def test_admin_roles(self, admin_api):
        admin_id = assert_page(admin_api.list(pageSize=1))["list"][0]["id"]
        roles = assert_success(admin_api.role_list(admin_id))
        assert isinstance(roles, list) and roles
        assert "name" in roles[0]

    @allure.story("重复注册同名管理员失败")
    def test_register_duplicate(self, login_api, api_config):
        result = login_api.register(
            {"username": api_config["username"], "password": "any_password"}
        ).json()
        assert result["code"] == 500
        assert result["message"] == "操作失败"

    @allure.story("注册管理员-缺少密码校验")
    def test_register_missing_password(self, login_api):
        result = login_api.register({"username": "auto_user"}).json()
        assert result["code"] == 404
        assert "password" in result["message"]


@pytest.fixture(scope="module")
def role_data():
    return load_yaml("role.yaml")


@allure.feature(FEATURE)
class TestRole:
    @allure.story("角色全量列表")
    def test_list_all(self, role_api):
        roles = assert_success(role_api.list_all())
        assert isinstance(roles, list) and roles

    @allure.story("角色新增-查询-更新-删除全流程")
    def test_crud(self, role_api, role_data):
        ts = time.strftime("%Y%m%d%H%M%S")
        payload = render(role_data["create"], ts=ts)
        name = payload["name"]
        assert_success(role_api.create(payload))

        role_id = None
        try:
            page = assert_page(role_api.list(keyword=name, pageSize=10), page_size=10)
            assert page["total"] == 1
            role_id = page["list"][0]["id"]

            update_payload = {**render(role_data["update"]), "name": name}
            assert_success(role_api.update(role_id, update_payload))
            page = assert_page(role_api.list(keyword=name, pageSize=10), page_size=10)
            assert page["list"][0]["description"] == update_payload["description"]
        finally:
            if role_id:
                assert_success(role_api.delete([role_id]))

        page = assert_page(role_api.list(keyword=name, pageSize=10), page_size=10)
        assert page["total"] == 0
