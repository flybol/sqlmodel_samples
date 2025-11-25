
import pytest
def connect_db():
    return "db"
@pytest.fixture(scope="module")
def db():
    return connect_db()