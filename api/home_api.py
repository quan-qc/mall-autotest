from api.base_api import BaseApi


class HomeApi(BaseApi):
    """首页运营：广告、品牌推荐、新品、人气推荐、专题推荐。"""

    def advertise_list(self, **params):
        return self.client.get("/home/advertise/list", params=params or None)

    def brand_list(self, **params):
        return self.client.get("/home/brand/list", params=params or None)

    def recommend_product_list(self, **params):
        return self.client.get("/home/recommendProduct/list", params=params or None)

    def new_product_list(self, **params):
        return self.client.get("/home/newProduct/list", params=params or None)

    def recommend_subject_list(self, **params):
        return self.client.get("/home/recommendSubject/list", params=params or None)
