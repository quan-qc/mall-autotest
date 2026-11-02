from api.base_api import BaseApi


class AdminApi(BaseApi):
    """后台用户管理。"""

    def list(self, **params):
        return self.client.get("/admin/list", params=params or None)

    def detail(self, admin_id: int):
        return self.client.get(f"/admin/{admin_id}")

    def role_list(self, admin_id: int):
        return self.client.get(f"/admin/role/{admin_id}")
