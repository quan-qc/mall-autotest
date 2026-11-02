from api.base_api import BaseApi


class CategoryApi(BaseApi):
    """商品分类。"""

    def list_by_parent(self, parent_id: int = 0, **params):
        return self.client.get(f"/productCategory/list/{parent_id}", params=params or None)

    def tree(self):
        return self.client.get("/productCategory/list/withChildren")

    def detail(self, category_id: int):
        return self.client.get(f"/productCategory/{category_id}")

    def create(self, payload: dict):
        return self.client.post("/productCategory/create", json=payload)

    def delete(self, category_id: int):
        return self.client.post(f"/productCategory/delete/{category_id}")

    def update_show_status(self, ids: list, show_status: int):
        return self.client.post(
            "/productCategory/update/showStatus",
            params={"ids": ids, "showStatus": show_status},
        )
