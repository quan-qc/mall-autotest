"""全局 fixture：配置、登录 token、HTTP 客户端与各业务 API 实例。"""
import platform
import sys
from pathlib import Path

import allure
import pytest

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from api.admin_api import AdminApi  # noqa: E402
from api.brand_api import BrandApi  # noqa: E402
from api.category_api import CategoryApi  # noqa: E402
from api.home_api import HomeApi  # noqa: E402
from api.login_api import LoginApi  # noqa: E402
from api.order_api import OrderApi  # noqa: E402
from api.product_api import ProductApi  # noqa: E402
from api.role_api import RoleApi  # noqa: E402
from pages.login_page import LoginPage  # noqa: E402
from utils.config_loader import config  # noqa: E402
from utils.http_client import HttpClient  # noqa: E402
from utils.logger import get_logger  # noqa: E402

logger = get_logger()


def pytest_addoption(parser):
    parser.addoption("--base-url", action="store", default=None, help="被测服务地址")
    parser.addoption("--username", action="store", default=None, help="管理员账号")
    parser.addoption("--password", action="store", default=None, help="管理员密码")
    parser.addoption("--ui-base-url", action="store", default=None, help="前端页面地址")
    parser.addoption("--headed", action="store_true", help="以有头模式运行浏览器")


@pytest.fixture(scope="session")
def api_config(request) -> dict:
    return {
        "base_url": request.config.getoption("--base-url") or config.get("base_url"),
        "username": request.config.getoption("--username") or config.get("admin.username"),
        "password": request.config.getoption("--password") or config.get("admin.password"),
    }


@pytest.fixture(scope="session")
def admin_token(api_config) -> str:
    client = HttpClient(base_url=api_config["base_url"])
    try:
        resp = client.post(
            "/admin/login",
            json={"username": api_config["username"], "password": api_config["password"]},
        )
        result = resp.json()
        if result.get("code") != 200:
            pytest.exit(f"管理员登录失败，测试终止: {result}", returncode=1)
        logger.info("管理员登录成功，获取到 JWT token")
        return result["data"]["token"]
    finally:
        client.close()


@pytest.fixture(scope="session")
def client(api_config, admin_token) -> HttpClient:
    http = HttpClient(base_url=api_config["base_url"], token=admin_token)
    yield http
    http.close()


@pytest.fixture(scope="session")
def unauth_client(api_config) -> HttpClient:
    http = HttpClient(base_url=api_config["base_url"])
    yield http
    http.close()


@pytest.fixture
def fake_token_client(api_config) -> HttpClient:
    http = HttpClient(base_url=api_config["base_url"], token="fake.token.value")
    yield http
    http.close()


@pytest.fixture(scope="session")
def login_api(unauth_client) -> LoginApi:
    return LoginApi(unauth_client)


@pytest.fixture(scope="session")
def auth_login_api(client) -> LoginApi:
    return LoginApi(client)


@pytest.fixture(scope="session")
def product_api(client) -> ProductApi:
    return ProductApi(client)


@pytest.fixture(scope="session")
def brand_api(client) -> BrandApi:
    return BrandApi(client)


@pytest.fixture(scope="session")
def category_api(client) -> CategoryApi:
    return CategoryApi(client)


@pytest.fixture(scope="session")
def order_api(client) -> OrderApi:
    return OrderApi(client)


@pytest.fixture(scope="session")
def admin_api(client) -> AdminApi:
    return AdminApi(client)


@pytest.fixture(scope="session")
def role_api(client) -> RoleApi:
    return RoleApi(client)


@pytest.fixture(scope="session")
def home_api(client) -> HomeApi:
    return HomeApi(client)


@pytest.fixture(scope="session")
def ui_base_url(request) -> str:
    return (request.config.getoption("--ui-base-url") or config.get("ui_base_url")).rstrip("/")


@pytest.fixture(scope="session")
def browser(request):
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        chromium = playwright.chromium.launch(headless=not request.config.getoption("--headed"))
        yield chromium
        chromium.close()


@pytest.fixture
def page(browser):
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    ui_page = context.new_page()
    ui_page.set_default_timeout(10_000)
    yield ui_page
    context.close()


@pytest.fixture
def logged_in_page(page, api_config, ui_base_url):
    login_page = LoginPage(page, ui_base_url)
    login_page.open_login()
    login_page.login(api_config["username"], api_config["password"])
    page.wait_for_url("**/#/home")
    return page


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """UI 用例失败时保存页面截图并附加到 Allure。"""
    outcome = yield
    report = outcome.get_result()
    if report.when not in ("setup", "call") or not report.failed:
        return
    ui_page = item.funcargs.get("page") or item.funcargs.get("logged_in_page")
    if not ui_page:
        return
    screenshot_dir = PROJECT_ROOT / "reports" / "screenshots"
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    screenshot_path = screenshot_dir / f"{item.name}.png"
    try:
        ui_page.screenshot(path=str(screenshot_path), full_page=True)
        allure.attach.file(
            str(screenshot_path), name="失败截图", attachment_type=allure.attachment_type.PNG
        )
        allure.attach(ui_page.url, name="失败页面 URL", attachment_type=allure.attachment_type.TEXT)
    except Exception as exc:
        logger.warning(f"保存 UI 失败截图失败: {exc}")


def pytest_sessionfinish(session, exitstatus):
    """写入 Allure 报告的环境信息，便于定位执行环境。"""
    try:
        allure_dir = session.config.getoption("--alluredir")
    except ValueError:
        allure_dir = None
    if not allure_dir:
        return
    target = Path(allure_dir)
    if not target.is_absolute():
        target = PROJECT_ROOT / target
    target.mkdir(parents=True, exist_ok=True)
    base_url = session.config.getoption("--base-url") or config.get("base_url")
    info = {
        "Project": "mall-autotest",
        "Base_URL": base_url,
        "Python": platform.python_version(),
        "Pytest": pytest.__version__,
        "OS": f"{platform.system()} {platform.release()}",
    }
    (target / "environment.properties").write_text(
        "\n".join(f"{k}={v}" for k, v in info.items()), encoding="utf-8"
    )
