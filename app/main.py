from fastapi import FastAPI

app = FastAPI(title="Clinic Appointment API")

@app.get("/health")
def health():
    return {"status": "ok"}
