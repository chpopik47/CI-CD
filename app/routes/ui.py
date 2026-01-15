from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.deps import get_db
from app.models import Doctor, Slot

router = APIRouter(prefix="/ui", tags=["ui"])
templates = Jinja2Templates(directory="templates")


@router.get("", response_class=HTMLResponse)
def ui_index(request: Request, db: Session = Depends(get_db)):
    doctors = db.query(Doctor).order_by(Doctor.id).all()
    data = [{"id": d.id, "name": d.name, "specialty": d.specialty} for d in doctors]
    return templates.TemplateResponse("index.html", {"request": request, "doctors": data})


@router.get("/doctor/{doctor_id}", response_class=HTMLResponse)
def ui_doctor(request: Request, doctor_id: int, date: str = "2026-01-15", db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        return templates.TemplateResponse(
            "base.html",
            {"request": request, "title": "Not found", "message": "Doctor not found"},
            status_code=404,
        )

    slots = (
        db.query(Slot)
        .filter(Slot.doctor_id == doctor_id, Slot.date == date)
        .order_by(Slot.time)
        .all()
    )
    slot_data = [{"time": s.time, "available": bool(s.is_available)} for s in slots]

    return templates.TemplateResponse(
        "doctor.html",
        {
            "request": request,
            "doctor": {"id": doctor.id, "name": doctor.name, "specialty": doctor.specialty},
            "date": date,
            "slots": slot_data,
        },
    )


@router.post("/book")
def ui_book(
    doctor_id: int = Form(...),
    date: str = Form(...),
    time: str = Form(...),
    patient_id: str = Form(...),
    db: Session = Depends(get_db),
):
    slot = (
        db.query(Slot)
        .filter(Slot.doctor_id == doctor_id, Slot.date == date, Slot.time == time)
        .first()
    )
    if slot and slot.is_available:
        slot.is_available = False
        db.commit()

    return RedirectResponse(url=f"/ui/doctor/{doctor_id}?date={date}", status_code=303)


@router.post("/cancel")
def ui_cancel(
    doctor_id: int = Form(...),
    date: str = Form(...),
    time: str = Form(...),
    db: Session = Depends(get_db),
):
    slot = (
        db.query(Slot)
        .filter(Slot.doctor_id == doctor_id, Slot.date == date, Slot.time == time)
        .first()
    )
    if slot and not slot.is_available:
        slot.is_available = True
        db.commit()

    return RedirectResponse(url=f"/ui/doctor/{doctor_id}?date={date}", status_code=303)
