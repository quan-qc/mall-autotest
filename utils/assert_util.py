"""统一断言：校验 HTTP 状态码与业务 code，返回 data。"""
from requests import Response


def body(resp: Response) -> dict:
    try:
        return resp.json()
    except ValueError:
        raise AssertionError(f"响应不是合法 JSON: {resp.text[:500]}")


def assert_code(resp: Response, expected: int = 200) -> any:
    assert resp.status_code == 200, f"HTTP 状态码异常: {resp.status_code}, body={resp.text[:500]}"
    data = body(resp)
    assert data.get("code") == expected, (
        f"业务 code 异常: 期望 {expected}, 实际 {data.get('code')}, "
        f"message={data.get('message')}"
    )
    return data.get("data")


def assert_success(resp: Response) -> any:
    return assert_code(resp, 200)


def assert_page(resp: Response, page_size: int = None, page_num: int = None) -> dict:
    data = assert_success(resp)
    assert isinstance(data, dict), f"分页响应应为对象, 实际: {data}"
    for key in ("pageNum", "pageSize", "total", "list"):
        assert key in data, f"分页响应缺少字段 {key}: {data}"
    if page_size is not None:
        assert len(data["list"]) <= page_size, (
            f"返回条数超过 pageSize: {len(data['list'])} > {page_size}"
        )
    if page_num is not None:
        assert data["pageNum"] == page_num, f"pageNum 异常: {data['pageNum']} != {page_num}"
    return data
