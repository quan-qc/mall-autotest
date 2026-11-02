"""HTTP 客户端封装：Session 复用、JWT 注入、请求/响应日志与 Allure 附件。"""
import json
import time
from urllib.parse import urljoin

import allure
import requests

from utils.config_loader import config
from utils.logger import get_logger

logger = get_logger()


class HttpClient:
    def __init__(self, base_url: str = None, token: str = None, token_head: str = None):
        self.base_url = (base_url or config.get("base_url")).rstrip("/") + "/"
        self.timeout = config.get("timeout", 10)
        self.token_head = token_head or config.get("admin.token_head", "Bearer ")
        self.session = requests.Session()
        self.session.headers.update(
            {"Content-Type": "application/json", "Accept": "application/json"}
        )
        if token:
            self.set_token(token)

    def set_token(self, token: str):
        self.session.headers["Authorization"] = f"{self.token_head}{token}"
        return self

    def clear_token(self):
        self.session.headers.pop("Authorization", None)
        return self

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        url = urljoin(self.base_url, path.lstrip("/"))
        kwargs.setdefault("timeout", self.timeout)
        start = time.time()
        logger.info(
            "--> %s %s params=%s body=%s",
            method.upper(), url, kwargs.get("params"), kwargs.get("json"),
        )
        resp = self.session.request(method.upper(), url, **kwargs)
        cost = round((time.time() - start) * 1000, 2)
        logger.info("<-- %s %s [%sms] %s", resp.status_code, url, cost, resp.text[:800])
        self._attach(method.upper(), url, kwargs, resp, cost)
        return resp

    def get(self, path: str, params: dict = None, **kwargs) -> requests.Response:
        return self.request("GET", path, params=params, **kwargs)

    def post(self, path: str, json: dict = None, **kwargs) -> requests.Response:
        return self.request("POST", path, json=json, **kwargs)

    def close(self):
        self.session.close()

    @staticmethod
    def _attach(method: str, url: str, kwargs: dict, resp, cost: float):
        try:
            req = {k: kwargs.get(k) for k in ("params", "json", "data") if kwargs.get(k) is not None}
            allure.attach(
                json.dumps({"method": method, "url": url, **req}, ensure_ascii=False, indent=2, default=str),
                name=f"Request {method} {url}",
                attachment_type=allure.attachment_type.JSON,
            )
            allure.attach(
                json.dumps(
                    {"status": resp.status_code, "cost_ms": cost, "body": resp.text},
                    ensure_ascii=False, indent=2, default=str,
                ),
                name=f"Response {resp.status_code} {url}",
                attachment_type=allure.attachment_type.JSON,
            )
        except Exception as exc:  # 附件失败不影响用例执行
            logger.debug("写入 allure 附件失败: %s", exc)
