"""商品管理模块接口用例。"""
import allure
import pytest

from utils.assert_util import assert_page, assert_success
from utils.data_loader import load_yaml

FEATURE = "商品管理"


@pytest.fixture(scope="module")
def data():
    return load_yaml("product.yaml")


@allure.feature(FEATURE)
class TestProduct:
    @allure.story("商品列表-默认分页")
    @pytest.mark.smoke
    def test_list_default(self, product_api):
        page = assert_page(product_api.list(), page_size=5, page_num=1)
        assert page["total"] > 0
        item = page["list"][0]
        for key in ("id", "name", "price", "productSn"):
            assert key in item, f"商品列表项缺少字段 {key}"

    @allure.story("商品列表-分页参数生效")
    def test_list_pagination(self, product_api, data):
        page = assert_page(
            product_api.list(
                pageNum=data["pagination"]["page_num"],
                pageSize=data["pagination"]["page_size"],
            ),
            page_size=data["pagination"]["page_size"],
            page_num=data["pagination"]["page_num"],
        )
        assert page["totalPage"] >= data["pagination"]["page_num"]

    @allure.story("商品列表-按名称关键字查询")
    def test_list_by_keyword(self, product_api, data):
        keyword = data["list"]["keyword"]
        page = assert_page(
            product_api.list(keyword=keyword, pageSize=data["list"]["page_size"]),
            page_size=data["list"]["page_size"],
        )
        assert page["total"] >= 1
        assert all(keyword in item["name"] for item in page["list"])

    @allure.story("商品列表-按品牌筛选")
    def test_list_by_brand(self, product_api):
        first = assert_page(product_api.list(pageSize=1))["list"][0]
        brand_id = first["brandId"]
        page = assert_page(product_api.list(brandId=brand_id, pageSize=5), page_size=5)
        assert page["total"] >= 1
        assert all(item["brandId"] == brand_id for item in page["list"])

    @allure.story("商品详情-存在的商品")
    def test_update_info(self, product_api):
        first = assert_page(product_api.list(pageSize=1))["list"][0]
        data = assert_success(product_api.update_info(first["id"]))
        assert data["id"] == first["id"]
        assert data["name"] == first["name"]
        assert "cateParentId" in data, "编辑详情应返回分类父 id"

    @allure.story("商品详情-不存在的商品")
    def test_update_info_not_exist(self, product_api):
        data = assert_success(product_api.update_info(999999))
        assert data is None

    @allure.story("商品简单列表-按关键字模糊查询")
    def test_simple_list(self, product_api, data):
        products = assert_success(product_api.simple_list(data["list"]["keyword"]))
        assert isinstance(products, list) and products
        assert all(data["list"]["keyword"] in item["name"] for item in products)
