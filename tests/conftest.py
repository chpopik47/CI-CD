import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# ruff: noqa: E402

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db import Base
from app.deps import get_db
from app.main import app
from app.models import Doctor, Slot


TEST_DB_URL = "sqlite:///./test.db"

engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        d1 = Doctor(name="Dr. Alice Carter", specialty="Cardiology")
        d2 = Doctor(name="Dr. Ben Novak", specialty="Dermatology")
        db.add_all([d1, d2])
        db.commit()
        db.refresh(d1)
        db.refresh(d2)

        db.add_all(
            [
                Slot(doctor_id=d1.id, date="2026-01-15", time="09:00"),
                Slot(doctor_id=d1.id, date="2026-01-15", time="09:30"),
                Slot(doctor_id=d1.id, date="2026-01-16", time="11:00"),
                Slot(doctor_id=d2.id, date="2026-01-15", time="13:00"),
            ]
        )
        db.commit()
    finally:
        db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()
