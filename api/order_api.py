from api.base_api import BaseApi


class OrderApi(BaseApi):
    """订单管理（只做读操作，避免污染业务数据）。"""

    def list(self, **params):
        return self.client.get("/order/list", params=params or None)

    def detail(self, order_id: int):
        return self.client.get(f"/order/{order_id}")
