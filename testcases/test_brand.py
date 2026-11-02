"""品牌管理模块接口用例。"""
import time

import allure
import pytest

from utils.assert_util import assert_code, assert_page, assert_success
from utils.data_loader import load_yaml, render

FEATURE = "品牌管理"


@pytest.fixture(scope="module")
def data():
    return load_yaml("brand.yaml")


@allure.feature(FEATURE)
class TestBrand:
    @allure.story("品牌列表-默认分页")
    @pytest.mark.smoke
    def test_list_default(self, brand_api):
        page = assert_page(brand_api.list(), page_size=5, page_num=1)
        assert page["total"] > 0

    @allure.story("品牌列表-按关键字查询")
    def test_list_by_keyword(self, brand_api, data):
        keyword = data["query"]["keyword"]
        page = assert_page(brand_api.list(keyword=keyword, pageSize=data["query"]["page_size"]))
        assert page["total"] >= 1
        assert all(keyword in item["name"] for item in page["list"])

    @allure.story("品牌详情")
    def test_detail(self, brand_api):
        first = assert_page(brand_api.list(pageSize=1))["list"][0]
        detail = assert_success(brand_api.detail(first["id"]))
        assert detail["id"] == first["id"]
        assert detail["name"] == first["name"]

    @allure.story("品牌新增-查询-更新-删除全流程")
    def test_crud(self, brand_api, data):
        ts = time.strftime("%Y%m%d%H%M%S")
        payload = render(data["create"], ts=ts)
        name = payload["name"]
        assert_success(brand_api.create(payload))

        created_id = None
        try:
            page = assert_page(brand_api.list(keyword=name, pageSize=10), page_size=10)
            assert page["total"] == 1, "新建品牌应能被关键字精确检索到"
            created_id = page["list"][0]["id"]

            payload["name"] = f"{name}-更新"
            assert_success(brand_api.update(created_id, payload))
            detail = assert_success(brand_api.detail(created_id))
            assert detail["name"] == f"{name}-更新"
        finally:
            if created_id:
                assert_success(brand_api.delete(created_id))

        page = assert_page(brand_api.list(keyword=name, pageSize=10), page_size=10)
        assert page["total"] == 0, "删除后品牌不应再被检索到"

    @allure.story("品牌新增-必填项缺失校验")
    def test_create_missing_logo(self, brand_api, data):
        ts = time.strftime("%Y%m%d%H%M%S")
        payload = render(data["missing_logo"], ts=ts)
        resp = brand_api.create(payload)
        assert assert_code(resp, 404) is None
        assert "logo" in resp.json()["message"]

    @allure.story("品牌列表-全量查询")
    def test_list_all(self, brand_api):
        brands = assert_success(brand_api.list_all())
        assert isinstance(brands, list) and brands

    @allure.story("品牌批量修改显示状态")
    def test_update_show_status(self, brand_api):
        brand_id = assert_page(brand_api.list(pageSize=1))["list"][0]["id"]
        assert_success(brand_api.update_show_status([brand_id], 1))
        detail = assert_success(brand_api.detail(brand_id))
        assert detail["showStatus"] == 1
