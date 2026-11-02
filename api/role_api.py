from api.base_api import BaseApi


class RoleApi(BaseApi):
    """角色管理。"""

    def list_all(self):
        return self.client.get("/role/listAll")

    def list(self, **params):
        return self.client.get("/role/list", params=params or None)

    def create(self, payload: dict):
        return self.client.post("/role/create", json=payload)

    def update(self, role_id: int, payload: dict):
        return self.client.post(f"/role/update/{role_id}", json=payload)

    def delete(self, ids: list):
        return self.client.post("/role/delete", params={"ids": ids})
