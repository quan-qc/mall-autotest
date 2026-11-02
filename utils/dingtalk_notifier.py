"""通过钉钉自定义机器人发送 pytest 结果摘要；未配置 Webhook 时跳过。"""
import base64
import hashlib
import hmac
import os
import time

import requests
from email_notifier import test_summary


def main():
    webhook = os.getenv("DINGTALK_WEBHOOK")
    if not webhook:
        print("钉钉配置不完整，跳过发送：DINGTALK_WEBHOOK")
        return

    outcome = os.getenv("TEST_OUTCOME", "unknown")
    passed = outcome == "success"
    summary = test_summary()
    repository = os.getenv("GITHUB_REPOSITORY", "local")
    run_url = (
        f"{os.getenv('GITHUB_SERVER_URL', '')}/{repository}"
        f"/actions/runs/{os.getenv('GITHUB_RUN_ID', '')}"
    )
    title = f"[mall-autotest] {'测试通过' if passed else '测试失败'}"

    params = {}
    secret = os.getenv("DINGTALK_SECRET")
    if secret:
        timestamp = str(int(time.time() * 1000))
        string_to_sign = f"{timestamp}\n{secret}".encode("utf-8")
        digest = hmac.new(
            secret.encode("utf-8"), string_to_sign, hashlib.sha256
        ).digest()
        params = {
            "timestamp": timestamp,
            "sign": base64.b64encode(digest).decode("utf-8"),
        }

    payload = {
        "msgtype": "markdown",
        "markdown": {
            "title": title,
            "text": (
                f"### {title}\n\n"
                f"- 仓库：{repository}\n"
                f"- 分支：{os.getenv('GITHUB_REF_NAME', 'local')}\n"
                f"- 执行结果：{outcome}\n"
                f"- 用例总数：{summary['tests']}\n"
                f"- 失败：{summary['failures']}\n"
                f"- 错误：{summary['errors']}\n"
                f"- 跳过：{summary['skipped']}\n"
                f"- 耗时：{summary['time']} 秒\n\n"
                f"[查看流水线及报告]({run_url})"
            ),
        },
    }
    response = requests.post(webhook, params=params, json=payload, timeout=10)
    response.raise_for_status()
    result = response.json()
    if result.get("errcode") != 0:
        raise RuntimeError(f"钉钉通知发送失败：{result}")
    print("测试结果钉钉通知已发送")


if __name__ == "__main__":
    main()
