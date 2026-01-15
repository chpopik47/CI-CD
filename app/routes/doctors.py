from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.deps import get_db
from app.models import Doctor

router = APIRouter(prefix="/doctors", tags=["doctors"])

@router.get("")
def list_doctors(db: Session = Depends(get_db)):
    doctors = db.query(Doctor).order_by(Doctor.id).all()
    return [{"id": d.id, "name": d.name, "specialty": d.specialty} for d in doctors]
