"""订单列表页面对象。"""
from pages.base_page import BasePage


class OrderPage(BasePage):
    PATH = "/oms/order"

    def open_orders(self):
        self.open(self.PATH)
        self.wait_table_loaded()

    def first_order_sn(self) -> str:
        return self.table_rows.first.locator("td").nth(2).inner_text().strip()

    def search(self, order_sn: str):
        self.page.get_by_placeholder("订单编号", exact=True).fill(order_sn)
        with self.page.expect_response(
            lambda response: "/order/list" in response.url and response.request.method == "GET"
        ) as response_info:
            self.page.get_by_role("button", name="查询搜索", exact=True).click()
        self.wait_table_loaded()
        return response_info.value

    def order_sns(self) -> list[str]:
        return [text.strip() for text in self.table_rows.locator("td:nth-child(3)").all_inner_texts()]
