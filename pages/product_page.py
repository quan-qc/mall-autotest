"""商品列表页面对象。"""
from pages.base_page import BasePage


class ProductPage(BasePage):
    PATH = "/pms/product"

    def open_products(self):
        self.open(self.PATH)
        self.wait_table_loaded()

    def first_product_name(self) -> str:
        return self.table_rows.first.locator("td").nth(3).locator("p").first.inner_text().strip()

    def search(self, keyword: str):
        self.page.get_by_placeholder("商品名称", exact=True).fill(keyword)
        with self.page.expect_response(
            lambda response: "/product/list" in response.url and response.request.method == "GET"
        ) as response_info:
            self.page.get_by_role("button", name="查询结果", exact=True).click()
        self.wait_table_loaded()
        return response_info.value

    def product_names(self) -> list[str]:
        return [
            text.strip()
            for text in self.table_rows.locator("td:nth-child(4) p:first-child").all_inner_texts()
        ]

    @property
    def first_publish_switch(self):
        return self.table_rows.first.locator(".el-switch").first

    def is_first_product_published(self) -> bool:
        class_name = self.first_publish_switch.get_attribute("class") or ""
        return "is-checked" in class_name

    def change_first_publish_status(self):
        with self.page.expect_response(
            lambda response: "/product/update/publishStatus" in response.url
            and response.request.method == "POST"
        ) as response_info:
            self.first_publish_switch.click()
        return response_info.value
