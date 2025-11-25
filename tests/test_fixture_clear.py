"""
teardown：fixture 的清理/回收（yield）
fixture 可以用 yield 实现“前置 + 后置清理”。

记忆点：
yield 前：setup
yield 后：teardown（无论测试成功/失败都会执行）
"""

import pytest
@pytest.fixture
def temp_file(tmp_path):
    p = tmp_path / "data.txt"
    p.write_text("hello")
    yield p
    # 这里是 teardown（yield 之后）
    p.unlink(missing_ok=True)

def test_read(temp_file):
    assert temp_file.read_text() == "hello"


# autouse：不用显式请求也会自动生效
# 给 fixture 加 autouse=True 后，pytest 会对其作用域内所有测试自动启用。
@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("MODE", "test")


# parametrized fixtures：让 fixture 自带多组参数
# fixture 也可以参数化，pytest 会为每个参数值跑一遍测试。
@pytest.fixture(params=[1, 2, 3])
def num(request):
    # 这里 request 是 pytest 内置 fixture，提供测试上下文，其中 request.param 取到当前参数值
    return request.param

def test_num_is_positive(num):
    assert num > 0


# fixture 可以“知道是谁请求了它”（request 上下文）
@pytest.fixture
def whoami(request):
    return request.node.name

def test_a(whoami):
    assert whoami == "test_a"

# 工厂型 fixture（fixture 返回一个函数）
@pytest.fixture
def make_user():
    def _make(name, role="user"):
        return {"name": name, "role": role}
    return _make

def test_factory(make_user):
    u1 = make_user("A")
    u2 = make_user("B", role="admin")
    assert u2["role"] == "admin"