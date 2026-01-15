from app.db import Base, engine, SessionLocal
from app.models import Doctor, Slot

def init_db():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if db.query(Doctor).count() == 0:
            d1 = Doctor(name="Dr. Alice Carter", specialty="Cardiology")
            d2 = Doctor(name="Dr. Ben Novak", specialty="Dermatology")
            db.add_all([d1, d2])
            db.commit()
            db.refresh(d1)
            db.refresh(d2)

            slots = [
                Slot(doctor_id=d1.id, date="2026-01-15", time="09:00"),
                Slot(doctor_id=d1.id, date="2026-01-15", time="09:30"),
                Slot(doctor_id=d1.id, date="2026-01-15", time="10:00"),
                Slot(doctor_id=d1.id, date="2026-01-16", time="11:00"),
                Slot(doctor_id=d1.id, date="2026-01-16", time="11:30"),
                Slot(doctor_id=d2.id, date="2026-01-15", time="13:00"),
                Slot(doctor_id=d2.id, date="2026-01-15", time="13:30"),
            ]
            db.add_all(slots)
            db.commit()
    finally:
        db.close()
