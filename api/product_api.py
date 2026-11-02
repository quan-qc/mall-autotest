from api.base_api import BaseApi


class ProductApi(BaseApi):
    """商品管理。"""

    def list(self, **params):
        return self.client.get("/product/list", params=params or None)

    def simple_list(self, keyword: str):
        return self.client.get("/product/simpleList", params={"keyword": keyword})

    def update_info(self, product_id: int):
        return self.client.get(f"/product/updateInfo/{product_id}")

    def create(self, payload: dict):
        return self.client.post("/product/create", json=payload)

    def update(self, product_id: int, payload: dict):
        return self.client.post(f"/product/update/{product_id}", json=payload)

    def update_status(self, action: str, ids: list, **params):
        """action: verifyStatus / publishStatus / recommendStatus / newStatus / deleteStatus"""
        return self.client.post(f"/product/update/{action}", params={"ids": ids, **params})
