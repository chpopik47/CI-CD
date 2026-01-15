from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.deps import get_db
from app.models import Doctor, Slot

router = APIRouter(prefix="/appointments", tags=["appointments"])


class AppointmentCreate(BaseModel):
    doctor_id: int
    date: str
    time: str
    patient_id: str


@router.post("")
def create_appointment(payload: AppointmentCreate, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == payload.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    slot = (
        db.query(Slot)
        .filter(
            Slot.doctor_id == payload.doctor_id,
            Slot.date == payload.date,
            Slot.time == payload.time,
        )
        .first()
    )
    if not slot:
        raise HTTPException(status_code=400, detail="Slot does not exist")

    if not slot.is_available:
        raise HTTPException(status_code=409, detail="Slot already booked")

    slot.is_available = False
    db.commit()

    return {"doctor_id": payload.doctor_id, "date": payload.date, "time": payload.time}


@router.delete("")
def cancel_appointment(
    doctor_id: int = Query(...),
    date: str = Query(...),
    time: str = Query(...),
    db: Session = Depends(get_db),
):
    slot = (
        db.query(Slot)
        .filter(Slot.doctor_id == doctor_id, Slot.date == date, Slot.time == time)
        .first()
    )
    if not slot:
        raise HTTPException(status_code=404, detail="Appointment not found")

    if slot.is_available:
        raise HTTPException(status_code=404, detail="Appointment not found")

    slot.is_available = True
    db.commit()
    return {"status": "cancelled"}
