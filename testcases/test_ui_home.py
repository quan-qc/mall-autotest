"""UI-首页仪表盘功能用例：区块渲染、指标数据、待处理事务与订单统计筛选。"""
import allure
import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage

pytestmark = pytest.mark.ui

FEATURE = "UI-首页仪表盘"


@allure.feature(FEATURE)
class TestUIDashboard:
    @allure.story("仪表盘各区块正常渲染")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_layout_blocks_visible(self, logged_in_page, ui_base_url):
        home = HomePage(logged_in_page, ui_base_url)
        expect(home.layout_titles).to_have_text([
            "Spring Boot项目学习",
            "Spring Cloud项目学习",
            "点Star支持项目",
            "待处理事务",
            "商品总览",
            "用户总览",
            "订单统计",
        ])

    @allure.story("今日订单与销售总额卡片展示")
    def test_today_summary_cards(self, logged_in_page, ui_base_url):
        home = HomePage(logged_in_page, ui_base_url)
        expect(home.total_titles).to_have_text(["今日订单总数", "今日销售总额", "昨日销售总额"])
        expect(home.total_values).to_have_text(["200", "￥5000.00", "￥5000.00"])

    @allure.story("待处理事务 9 项及计数展示")
    def test_pending_task_counts(self, logged_in_page, ui_base_url):
        home = HomePage(logged_in_page, ui_base_url)
        items = [
            "待付款订单",
            "已完成订单",
            "待确认收货订单",
            "待发货订单",
            "新缺货登记",
            "待处理退款申请",
            "已发货订单",
            "待处理退货订单",
            "广告位即将到期",
        ]
        expect(home.handle_items).to_have_count(len(items))
        for index, name in enumerate(items):
            expect(home.handle_items.nth(index)).to_contain_text(name)
            expect(home.handle_items.nth(index)).to_contain_text("(10)")

    @allure.story("商品总览与用户总览数据")
    def test_product_and_member_overview(self, logged_in_page, ui_base_url):
        home = HomePage(logged_in_page, ui_base_url)
        expect(home.overview_titles).to_have_text([
            "已下架",
            "已上架",
            "库存紧张",
            "全部商品",
            "今日新增",
            "昨日新增",
            "本月新增",
            "会员总数",
        ])
        expect(home.overview_values).to_have_text([
            "100",
            "400",
            "50",
            "500",
            "100",
            "200",
            "1000",
            "5000",
        ])

    @allure.story("学习链接可新窗口跳转")
    def test_learning_links(self, logged_in_page, ui_base_url):
        home = HomePage(logged_in_page, ui_base_url)
        links = home.link_list()
        expected = {
            "mall学习教程": "https://www.macrozheng.com/",
            "mall-swarm学习教程": "https://cloud.macrozheng.com/",
            "mall项目": "https://github.com/macrozheng/mall",
        }
        assert len(links) == 3
        for link in links:
            assert link["href"] == expected[link["text"]]
            assert link["target"] == "_blank"

    @allure.story("订单统计默认区间与快捷日期筛选")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_order_statistics_date_filter(self, logged_in_page, ui_base_url):
        home = HomePage(logged_in_page, ui_base_url)
        expect(home.chart).to_be_visible(timeout=15_000)
        assert home.range_values() == ["2026-01-01", "2026-01-08"]

        home.open_date_picker()
        expect(home.page.locator(".el-picker-panel__shortcut")).to_have_text(["最近一周", "最近一月"])

        home.select_shortcut("最近一月")
        expect(home.range_inputs.nth(1)).to_have_value("2026-01-31")
        expect(home.chart).to_be_visible(timeout=15_000)
