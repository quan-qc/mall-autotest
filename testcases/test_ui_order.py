"""UI 订单查询场景。"""
import allure
import pytest

from pages.order_page import OrderPage

pytestmark = pytest.mark.ui


@allure.feature("UI-订单管理")
class TestUIOrder:
    @allure.story("按订单编号精确查询")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_order_search(self, logged_in_page, ui_base_url):
        order_page = OrderPage(logged_in_page, ui_base_url)
        order_page.open_orders()
        order_sn = order_page.first_order_sn()

        response = order_page.search(order_sn)

        assert response.status == 200
        assert response.json()["code"] == 200
        assert order_page.order_sns() == [order_sn]
