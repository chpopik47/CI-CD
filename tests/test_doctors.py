from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_doctors():
    r = client.get("/doctors")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "id" in data[0]
    assert "name" in data[0]
    assert "specialty" in data[0]
