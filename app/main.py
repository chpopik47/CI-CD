from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.init_db import init_db
from app.routes.doctors import router as doctors_router
from app.routes.slots import router as slots_router
from app.routes.appointments import router as appointments_router
from app.routes.ui import router as ui_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Clinic Appointment API", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(doctors_router)
app.include_router(slots_router)
app.include_router(appointments_router)
app.include_router(ui_router)


@app.get("/", operation_id="get_root")
def get_root():
    return {"ui": "/ui", "docs": "/docs", "health": "/health"}


@app.get("/health")
def health():
    return {"status": "ok"}
