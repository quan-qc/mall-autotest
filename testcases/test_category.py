"""商品分类模块接口用例。"""
import time

import allure
import pytest

from utils.assert_util import assert_page, assert_success
from utils.data_loader import load_yaml, render

FEATURE = "商品分类"


@pytest.fixture(scope="module")
def data():
    return load_yaml("category.yaml")


@allure.feature(FEATURE)
class TestCategory:
    @allure.story("一级分类列表")
    @pytest.mark.smoke
    def test_list_by_parent(self, category_api):
        page = assert_page(category_api.list_by_parent(0, pageSize=5), page_size=5)
        assert page["total"] > 0

    @allure.story("分类树结构")
    def test_tree(self, category_api):
        tree = assert_success(category_api.tree())
        assert isinstance(tree, list) and tree
        assert all("children" in node for node in tree)
        assert any(node["children"] for node in tree), "分类树应包含子分类"

    @allure.story("分类详情")
    def test_detail(self, category_api):
        first = assert_page(category_api.list_by_parent(0, pageSize=1))["list"][0]
        detail = assert_success(category_api.detail(first["id"]))
        assert detail["id"] == first["id"]
        assert detail["name"] == first["name"]

    @allure.story("分类新增-查询-删除全流程")
    def test_create_and_delete(self, category_api, data):
        ts = time.strftime("%Y%m%d%H%M%S")
        payload = render(data["create"], ts=ts)
        name = payload["name"]
        assert_success(category_api.create(payload))

        created_id = None
        try:
            page = assert_page(category_api.list_by_parent(0, pageSize=200), page_size=200)
            matched = [item for item in page["list"] if item["name"] == name]
            assert len(matched) == 1, "新建分类应出现在一级分类列表中"
            created_id = matched[0]["id"]

            detail = assert_success(category_api.detail(created_id))
            assert detail["parentId"] == 0
            assert detail["showStatus"] == payload["showStatus"]
        finally:
            if created_id:
                assert_success(category_api.delete(created_id))

        page = assert_page(category_api.list_by_parent(0, pageSize=200), page_size=200)
        assert all(item["name"] != name for item in page["list"]), "删除后分类不应再出现"
