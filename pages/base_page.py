"""页面对象基类：提供导航和表格等待能力。"""
from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page, base_url: str):
        self.page = page
        self.base_url = base_url.rstrip("/")

    def open(self, path: str):
        self.page.goto(f"{self.base_url}/#{path}")
        self.page.wait_for_load_state("domcontentloaded")

    def wait_table_loaded(self):
        expect(self.table_rows.first).to_be_visible(timeout=30_000)
        expect(self.page.locator(".el-loading-mask")).to_have_count(0)

    @property
    def table_rows(self):
        return self.page.locator(".el-table__body-wrapper tbody tr")
