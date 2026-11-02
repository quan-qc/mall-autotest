from api.base_api import BaseApi


class LoginApi(BaseApi):
    """登录 / 当前用户 / 登出。"""

    def login(self, username: str, password: str):
        return self.client.post("/admin/login", json={"username": username, "password": password})

    def register(self, payload: dict):
        return self.client.post("/admin/register", json=payload)

    def info(self):
        return self.client.get("/admin/info")

    def logout(self):
        return self.client.post("/admin/logout")
