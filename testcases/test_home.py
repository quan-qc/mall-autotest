"""首页运营模块接口用例。"""
import allure
import pytest

from utils.assert_util import assert_page

FEATURE = "首页运营"


@allure.feature(FEATURE)
class TestHome:
    @allure.story("广告列表")
    @pytest.mark.smoke
    def test_advertise_list(self, home_api):
        page = assert_page(home_api.advertise_list(), page_size=5, page_num=1)
        assert page["total"] > 0
        for key in ("id", "name", "type", "startTime", "endTime", "status"):
            assert key in page["list"][0]

    @allure.story("首页品牌推荐列表")
    def test_brand_list(self, home_api):
        page = assert_page(home_api.brand_list(), page_size=5, page_num=1)
        assert page["total"] > 0
        assert "brandName" in page["list"][0]

    @allure.story("首页人气商品推荐列表")
    def test_recommend_product_list(self, home_api):
        page = assert_page(home_api.recommend_product_list(), page_size=5, page_num=1)
        assert page["total"] > 0
        assert "productName" in page["list"][0]

    @allure.story("首页新品推荐列表")
    def test_new_product_list(self, home_api):
        page = assert_page(home_api.new_product_list(), page_size=5, page_num=1)
        assert page["total"] > 0
        assert "productName" in page["list"][0]

    @allure.story("首页专题推荐列表")
    def test_recommend_subject_list(self, home_api):
        page = assert_page(home_api.recommend_subject_list(), page_size=5, page_num=1)
        assert page["total"] > 0
        assert "subjectName" in page["list"][0]
