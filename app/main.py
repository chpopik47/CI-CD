from fastapi import FastAPI
from app.routes.doctors import router as doctors_router

app = FastAPI(title="Clinic Appointment API")

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(doctors_router)
