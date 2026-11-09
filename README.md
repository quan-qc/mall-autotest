# mall-autotest

基于开源电商系统 [mall](https://github.com/macrozheng/mall) 的管理端自动化测试工程，包含接口自动化与 UI 自动化，接入 Allure 报告和 GitHub Actions 持续集成。

- 在线报告：https://quan-qc.github.io/mall-autotest/
- 测试规模：**52 条用例**（40 条接口 + 12 条 UI）

## 测试覆盖

| 模块 | 接口用例 | UI 用例 |
|---|---|---|
| 登录认证 | 登录成功/失败、参数校验、未授权与伪造 token | 登录成功跳转、错误密码提示 |
| 品牌管理 | 列表分页、关键字查询、新增、更新、批量上下架、删除 | 品牌新增、列表展示 |
| 商品管理 | 列表分页、分页参数、关键字、按品牌筛选 | 商品搜索、上架/下架状态 |
| 分类管理 | 一级分类、分类树、新增、删除 | - |
| 订单管理 | 列表分页、按订单号查询（只读） | 订单列表查询 |
| 用户与角色 | 管理员列表/详情/角色、角色 CRUD | - |
| 首页仪表盘 | - | 区块渲染、指标卡、待处理事务、总览数据、链接跳转、订单统计日期筛选 |

## 技术栈

- Python 3.13、pytest、requests、PyYAML
- Playwright（Page Object 模式）
- Allure、pytest-xdist
- GitHub Actions + GitHub Pages

## 目录结构

```text
mall-autotest/
├── .github/workflows/autotest.yml   # CI：执行测试并发布 Allure 报告
├── api/                             # 接口封装（按业务模块划分）
│   ├── base_api.py                  # 公共请求入口
│   ├── login_api.py
│   ├── brand_api.py
│   ├── product_api.py
│   ├── category_api.py
│   ├── order_api.py
│   ├── admin_api.py
│   ├── role_api.py
│   └── home_api.py
├── pages/                           # Page Object
│   ├── base_page.py
│   ├── login_page.py
│   ├── brand_page.py
│   ├── product_page.py
│   ├── order_page.py
│   └── home_page.py
├── data/                            # YAML 数据驱动
├── testcases/                       # 接口与 UI 用例
├── utils/
│   ├── http_client.py               # 会话、鉴权、日志
│   ├── assert_util.py               # HTTP 与业务码断言、分页断言
│   ├── data_loader.py               # YAML 加载与变量渲染
│   ├── config_loader.py
│   └── logger.py
├── config/config.yaml               # 被测环境与被测账号
├── conftest.py                      # 客户端、鉴权、浏览器上下文等 fixture
├── pytest.ini
└── requirements.txt
```

## 环境要求

1. mall-admin 已启动并监听 `http://localhost:8080`（依赖 MySQL、Redis）。
2. 执行 UI 用例时，mall-admin-web 已启动并监听 `http://localhost:5173`。
3. 安装依赖：

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python -m playwright install chromium
```

4. 按需修改 `config/config.yaml`，或用环境变量覆盖：

```powershell
$env:MALL_BASE_URL="http://localhost:8080"
$env:MALL_USERNAME="admin"
$env:MALL_PASSWORD="macro123"
```

## 执行

```powershell
# 全部用例
pytest

# 仅接口用例
pytest -m api

# 仅 UI 用例
pytest -m ui

# 冒烟用例
pytest -m smoke

# 并行执行接口用例
pytest -m api -n 4
```

生成 Allure 报告：

```powershell
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

## 持续集成

工作流 [autotest.yml](.github/workflows/autotest.yml) 在推送后自动执行测试并生成 Allure 报告，成功后部署到 GitHub Pages。

[![CI](https://github.com/quan-qc/mall-autotest/actions/workflows/autotest.yml/badge.svg)](https://github.com/quan-qc/mall-autotest/actions/workflows/autotest.yml)

## 设计要点

- 接口用例同时校验 HTTP 状态码与业务 `code`，避免只判 200 造成漏检。
- 写用例使用唯一测试数据，并在 `finally` 中清理，保证用例独立可重复执行。
- UI 用例使用独立 `BrowserContext` 隔离登录态，显式等待关键元素，失败时自动截图并附加到 Allure。
- 订单相关用例只做查询，避免污染业务数据。

## 覆盖边界

- 仅覆盖 mall 管理端（mall-admin 及其前端），**未覆盖商城前台（mall-portal）**。
- 首页仪表盘数据目前为前端静态数据，用例校验的是页面渲染与交互，不校验后端业务数据一致性。
- 商品、订单模块以查询类场景为主，未覆盖下单、支付等写操作链路。
