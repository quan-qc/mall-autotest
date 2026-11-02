from api.base_api import BaseApi


class BrandApi(BaseApi):
    """品牌管理。"""

    def list(self, **params):
        return self.client.get("/brand/list", params=params or None)

    def list_all(self):
        return self.client.get("/brand/listAll")

    def detail(self, brand_id: int):
        return self.client.get(f"/brand/{brand_id}")

    def create(self, payload: dict):
        return self.client.post("/brand/create", json=payload)

    def update(self, brand_id: int, payload: dict):
        return self.client.post(f"/brand/update/{brand_id}", json=payload)

    def delete(self, brand_id: int):
        return self.client.get(f"/brand/delete/{brand_id}")

    def update_show_status(self, ids: list, show_status: int):
        return self.client.post(
            "/brand/update/showStatus", params={"ids": ids, "showStatus": show_status}
        )
