"""订单模块接口用例（只做查询，避免修改业务数据）。"""
import allure
import pytest

from utils.assert_util import assert_page, assert_success

FEATURE = "订单管理"


@allure.feature(FEATURE)
class TestOrder:
    @allure.story("订单列表-默认分页")
    @pytest.mark.smoke
    def test_list_default(self, order_api):
        page = assert_page(order_api.list(), page_size=5, page_num=1)
        assert page["total"] > 0
        for key in ("id", "orderSn", "memberUsername", "totalAmount", "status"):
            assert key in page["list"][0]

    @allure.story("订单列表-按订单号查询")
    def test_list_by_order_sn(self, order_api):
        first = assert_page(order_api.list(pageSize=1))["list"][0]
        order_sn = first["orderSn"]
        page = assert_page(order_api.list(orderSn=order_sn, pageSize=5), page_size=5)
        assert page["total"] == 1
        assert page["list"][0]["orderSn"] == order_sn

    @allure.story("订单详情")
    def test_detail(self, order_api):
        first = assert_page(order_api.list(pageSize=1))["list"][0]
        detail = assert_success(order_api.detail(first["id"]))
        assert detail["id"] == first["id"]
        assert detail["orderSn"] == first["orderSn"]
        assert isinstance(detail["orderItemList"], list) and detail["orderItemList"]
        assert isinstance(detail["historyList"], list)

    @allure.story("订单详情-不存在的订单")
    def test_detail_not_exist(self, order_api):
        data = assert_success(order_api.detail(99999999))
        assert data is None
