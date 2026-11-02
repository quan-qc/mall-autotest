"""配置读取：config/config.yaml + 环境变量覆盖。"""
import os
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = PROJECT_ROOT / "config" / "config.yaml"

# 支持通过环境变量覆盖，便于 CI / 多环境切换
ENV_OVERRIDE = {
    "base_url": "MALL_BASE_URL",
    "admin.username": "MALL_USERNAME",
    "admin.password": "MALL_PASSWORD",
}


class Config:
    def __init__(self, path: Path = CONFIG_FILE):
        with open(path, encoding="utf-8") as f:
            self._data = yaml.safe_load(f) or {}

    def get(self, key: str, default=None):
        env_key = ENV_OVERRIDE.get(key)
        if env_key and os.getenv(env_key):
            return os.getenv(env_key)
        node = self._data
        for part in key.split("."):
            if not isinstance(node, dict) or part not in node:
                return default
            node = node[part]
        return node


config = Config()
