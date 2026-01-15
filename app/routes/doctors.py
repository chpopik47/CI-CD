from fastapi import APIRouter

router = APIRouter(prefix="/doctors", tags=["doctors"])

DOCTORS = [
    {"id": 1, "name": "Dr. Alice Carter", "specialty": "Cardiology"},
    {"id": 2, "name": "Dr. Ben Novak", "specialty": "Dermatology"},
]

@router.get("")
def list_doctors():
    return DOCTORS
