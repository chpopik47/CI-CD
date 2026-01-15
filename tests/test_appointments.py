from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_appointment_and_block_double_booking():
    payload = {"doctor_id": 1, "date": "2026-01-15", "time": "09:00", "patient_id": "p1"}

    r1 = client.post("/appointments", json=payload)
    assert r1.status_code == 200

    r2 = client.post("/appointments", json=payload)
    assert r2.status_code == 409

    r3 = client.delete("/appointments", params={"doctor_id": 1, "date": "2026-01-15", "time": "09:00"})
    assert r3.status_code == 200

    r4 = client.post("/appointments", json=payload)
    assert r4.status_code == 200
