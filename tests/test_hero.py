from sqlmodel import create_engine,SQLModel,Session
from fastapi.testclient import TestClient
from models_with_relationships_in_fastapi.main import app,get_session
def test_create_hero():
    """ 创建英雄 """
    engine = create_engine(  
        "sqlite:///testing.db", connect_args={"check_same_thread": False}
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        def get_session_override():
            return session
        app.dependency_overrides[get_session] = get_session_override
        client = TestClient(app)
        response = client.post(
            "/heroes/", json={"name": "Deadpond", "secret_name": "Dive Wilson"}
        )
        app.dependency_overrides.clear()
        data = response.json()
        assert response.status_code == 200
        assert data["name"] == "Deadpond"
        assert data["secret_name"] == "Dive Wilson"
        assert data["age"] is None
        assert data["id"] is not None