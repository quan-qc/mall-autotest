"""UI 商品搜索及上下架场景。"""
import allure
import pytest

from pages.product_page import ProductPage

pytestmark = pytest.mark.ui


@allure.feature("UI-商品管理")
class TestUIProduct:
    @allure.story("按商品名称搜索")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_product_search(self, logged_in_page, ui_base_url):
        product_page = ProductPage(logged_in_page, ui_base_url)
        product_page.open_products()
        keyword = product_page.first_product_name()

        response = product_page.search(keyword)

        assert response.status == 200
        assert response.json()["code"] == 200
        names = product_page.product_names()
        assert names, "搜索结果不应为空"
        assert all(keyword in name for name in names)

    @allure.story("商品上下架状态切换并恢复")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_product_publish_status(self, logged_in_page, ui_base_url):
        product_page = ProductPage(logged_in_page, ui_base_url)
        product_page.open_products()
        original_status = product_page.is_first_product_published()

        try:
            response = product_page.change_first_publish_status()
            assert response.status == 200
            assert response.json()["code"] == 200
            assert product_page.is_first_product_published() is not original_status
        finally:
            if product_page.is_first_product_published() != original_status:
                restore_response = product_page.change_first_publish_status()
                assert restore_response.json()["code"] == 200
