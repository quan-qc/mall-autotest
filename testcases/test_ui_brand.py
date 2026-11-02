"""UI 新增品牌场景，测试后自动清理数据。"""
import json
import time

import allure
import pytest
from playwright.sync_api import expect

from pages.brand_page import BrandPage
from utils.assert_util import assert_page

pytestmark = pytest.mark.ui


@allure.feature("UI-品牌管理")
class TestUIBrand:
    @allure.story("新增品牌并可在列表查询")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_brand(self, logged_in_page, ui_base_url, brand_api):
        brand_page = BrandPage(logged_in_page, ui_base_url)
        name = f"UI自动化品牌-{time.strftime('%Y%m%d%H%M%S')}"

        # 文件存储是外部依赖，仅 Mock 上传响应；品牌新增仍请求真实后端。
        def mock_minio_upload(route):
            route.fulfill(
                status=200,
                content_type="application/json",
                body=json.dumps({
                    "code": 200,
                    "message": "操作成功",
                    "data": {"url": "https://example.com/ui-automation-logo.png"},
                }),
            )

        logged_in_page.route("**/minio/upload", mock_minio_upload)

        try:
            response = brand_page.add_brand(name)
            assert response.status == 200
            assert response.json()["code"] == 200

            brand_page.open_brands()
            brand_page.search(name)
            expect(brand_page.brand_row(name)).to_have_count(1)
        finally:
            page_data = assert_page(brand_api.list(keyword=name, pageSize=10), page_size=10)
            for brand in page_data["list"]:
                if brand["name"] == name:
                    delete_response = brand_api.delete(brand["id"])
                    assert delete_response.json()["code"] == 200
