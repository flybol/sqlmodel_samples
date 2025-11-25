import pytest
@pytest.fixture
def first_entry():
    return "a"

@pytest.fixture
# def order(first_entry): #fixture 也能请求别的 fixture：
#     return [first_entry]

def test_order(order):
    assert order[0] == "a"

@pytest.fixture
def order():
    return []

@pytest.fixture
def append_first(order):
    order.append("first")

def test_order_shared(order, append_first):
    # 这点在“有副作用的 fixture”里非常关键。
    assert order == ["first"]  # append_first 修改的就是同一个 order

# @pytest.fixture(scope=...) 决定缓存/复用的范围。
@pytest.fixture
def config():
    return {"url": "https://api.test"}

@pytest.fixture
def auth(config):
    return f"token-from-{config['url']}"

@pytest.fixture
def api_client(auth):
    return {"Authorization": auth}

def test_api(api_client):
    print(api_client)

@pytest.fixture(autouse=True)
def log():
    print("before test")

@pytest.fixture(params=[1, 2, 3])
def number(request):
    return request.param

def test_num(number):
    print(number)