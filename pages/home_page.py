"""首页仪表盘页面对象：区块、指标卡、待处理事务、总览与订单统计图表。"""
from pages.base_page import BasePage


class HomePage(BasePage):
    PATH = "/home"

    def open_home(self):
        self.open(self.PATH)

    @property
    def layout_titles(self):
        return self.page.locator(".layout-title")

    @property
    def total_titles(self):
        return self.page.locator(".total-title")

    @property
    def total_values(self):
        return self.page.locator(".total-value")

    @property
    def handle_items(self):
        return self.page.locator(".un-handle-item")

    @property
    def overview_values(self):
        return self.page.locator(".overview-item-value")

    @property
    def overview_titles(self):
        return self.page.locator(".overview-item-title")

    @property
    def range_inputs(self):
        return self.page.locator(".el-range-input")

    @property
    def chart(self):
        return self.page.locator("[_echarts_instance_] canvas")

    @property
    def learn_links(self):
        return self.page.locator(".address-content a")

    def range_values(self) -> list[str]:
        return self.range_inputs.evaluate_all("els => els.map(e => e.value)")

    def link_list(self) -> list[dict]:
        return self.learn_links.evaluate_all(
            "els => els.map(e => ({text: e.textContent.trim(), href: e.href, target: e.target}))"
        )

    def open_date_picker(self):
        self.range_inputs.first.click()

    def select_shortcut(self, text: str):
        self.page.locator(".el-picker-panel__shortcut", has_text=text).click()
