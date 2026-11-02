from utils.http_client import HttpClient


class BaseApi:
    """API 层基类：只做接口调用，不做断言。"""

    def __init__(self, client: HttpClient):
        self.client = client
