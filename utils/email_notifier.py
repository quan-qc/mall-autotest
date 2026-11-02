"""通过 SMTP 发送 pytest 结果摘要；未配置邮件参数时跳过。"""
import os
import smtplib
import ssl
import xml.etree.ElementTree as ET
from email.message import EmailMessage
from pathlib import Path


def test_summary():
    report = Path("reports/junit.xml")
    if not report.exists():
        return {"tests": 0, "failures": 0, "errors": 0, "skipped": 0, "time": "0"}
    root = ET.parse(report).getroot()
    suite = root if root.tag == "testsuite" else root.find("testsuite")
    return {
        key: suite.attrib.get(key, "0")
        for key in ("tests", "failures", "errors", "skipped", "time")
    }


def main():
    required = ("SMTP_HOST", "SMTP_USER", "SMTP_PASSWORD", "EMAIL_TO")
    missing = [key for key in required if not os.getenv(key)]
    if missing:
        print(f"邮件配置不完整，跳过发送：{', '.join(missing)}")
        return

    outcome = os.getenv("TEST_OUTCOME", "unknown")
    passed = outcome == "success"
    summary = test_summary()
    repository = os.getenv("GITHUB_REPOSITORY", "local")
    run_url = (
        f"{os.getenv('GITHUB_SERVER_URL', '')}/{repository}"
        f"/actions/runs/{os.getenv('GITHUB_RUN_ID', '')}"
    )

    message = EmailMessage()
    message["Subject"] = f"[mall-autotest] {'测试通过' if passed else '测试失败'}"
    message["From"] = os.environ["SMTP_USER"]
    message["To"] = os.environ["EMAIL_TO"]
    message.set_content(
        "mall 自动化测试执行完成\n\n"
        f"仓库：{repository}\n"
        f"分支：{os.getenv('GITHUB_REF_NAME', 'local')}\n"
        f"执行结果：{outcome}\n"
        f"用例总数：{summary['tests']}\n"
        f"失败：{summary['failures']}\n"
        f"错误：{summary['errors']}\n"
        f"跳过：{summary['skipped']}\n"
        f"耗时：{summary['time']} 秒\n\n"
        f"流水线及报告下载：{run_url}\n"
    )

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(
        os.environ["SMTP_HOST"], int(os.getenv("SMTP_PORT", "465")), context=context
    ) as smtp:
        smtp.login(os.environ["SMTP_USER"], os.environ["SMTP_PASSWORD"])
        smtp.send_message(message)
    print("测试结果邮件已发送")


if __name__ == "__main__":
    main()
