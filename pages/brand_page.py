"""品牌列表及新增品牌页面对象。"""
from pages.base_page import BasePage


# 有效的 1x1 PNG，用于触发前端文件上传组件。
PNG_1X1 = bytes.fromhex(
    "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c489"
    "0000000d49444154789c626001000000ffff03000006000557bfabd40000000049454e44ae426082"
)


class BrandPage(BasePage):
    LIST_PATH = "/pms/brand"
    ADD_PATH = "/pms/addBrand"

    def open_brands(self):
        self.open(self.LIST_PATH)
        self.wait_table_loaded()

    def open_add_brand(self):
        self.open(self.ADD_PATH)

    def search(self, keyword: str):
        self.page.get_by_placeholder("品牌名称/关键字", exact=True).fill(keyword)
        with self.page.expect_response(
            lambda response: "/brand/list" in response.url and response.request.method == "GET"
        ) as response_info:
            self.page.get_by_role("button", name="查询结果", exact=True).click()
        self.wait_table_loaded()
        return response_info.value

    def brand_row(self, name: str):
        return self.table_rows.filter(has_text=name)

    def add_brand(self, name: str, first_letter: str = "A"):
        self.open_add_brand()
        form_items = self.page.locator(".el-form-item")
        form_items.filter(has_text="品牌名称").locator("input").fill(name)
        form_items.filter(has_text="品牌首字母").locator("input").fill(first_letter)
        form_items.filter(has_text="排序").locator("input").fill("1")

        with self.page.expect_response(
            lambda response: "/minio/upload" in response.url and response.request.method == "POST"
        ) as upload_info:
            self.page.locator('input[type="file"]').first.set_input_files(
                {"name": "logo.png", "mimeType": "image/png", "buffer": PNG_1X1}
            )
        upload_response = upload_info.value
        if upload_response.json().get("code") != 200:
            raise AssertionError(f"品牌 LOGO 上传失败: {upload_response.text()}")

        self.page.get_by_role("button", name="提交", exact=True).click()
        with self.page.expect_response(
            lambda response: "/brand/create" in response.url and response.request.method == "POST"
        ) as create_info:
            self.page.locator(".el-message-box").get_by_role("button", name="确定", exact=True).click()
        return create_info.value
