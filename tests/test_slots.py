from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_list_slots_returns_availability():
    r = client.get("/doctors/1/slots", params={"date": "2026-01-15"})
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert "time" in data[0]
    assert "available" in data[0]
