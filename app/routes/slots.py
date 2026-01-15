from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.deps import get_db
from app.models import Doctor, Slot

router = APIRouter(prefix="/doctors", tags=["slots"])

@router.get("/{doctor_id}/slots")
def list_slots(doctor_id: int, date: str, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    slots = (
        db.query(Slot)
        .filter(Slot.doctor_id == doctor_id, Slot.date == date)
        .order_by(Slot.time)
        .all()
    )
    return [{"time": s.time, "available": bool(s.is_available)} for s in slots]
