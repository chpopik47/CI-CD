# Clinic Appointment API

## Run locally
pip install -r requirements.txt
uvicorn app.main:app --reload

## Tests
pytest

## Docker
docker build -t clinic-api .
docker run -p 8000:8000 clinic-api
