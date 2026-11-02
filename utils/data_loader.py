"""YAML 数据加载与占位符渲染。"""
import copy
from pathlib import Path

import yaml

from utils.config_loader import PROJECT_ROOT

DATA_DIR = PROJECT_ROOT / "data"


def load_yaml(name: str):
    with open(DATA_DIR / name, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def render(obj, **kwargs):
    """递归渲染 YAML 中的 {placeholder}，返回副本，避免污染原始数据。"""
    obj = copy.deepcopy(obj)
    if isinstance(obj, dict):
        return {k: render(v, **kwargs) for k, v in obj.items()}
    if isinstance(obj, list):
        return [render(item, **kwargs) for item in obj]
    if isinstance(obj, str):
        for key, value in kwargs.items():
            obj = obj.replace("{" + key + "}", str(value))
        return obj
    return obj
