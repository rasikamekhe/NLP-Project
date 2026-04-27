from typing import Dict, List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

try:
    from .database import create_user, get_history, init_db, save_prediction, validate_user
    from .model import ThreatModelService
except ImportError:
    from database import create_user, get_history, init_db, save_prediction, validate_user
    from model import ThreatModelService


app = FastAPI(title="AI Threat Intelligence API", version="1.0.0")
model_service = ThreatModelService()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    password: str


class PredictRequest(BaseModel):
    text: str
    username: str


@app.on_event("startup")
def startup():
    init_db()
    try:
        model_service.load()
    except FileNotFoundError:
        # Model can be loaded later after train.py execution.
        pass


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/login")
def login(payload: LoginRequest):
    if validate_user(payload.username, payload.password):
        return {"message": "Login successful", "username": payload.username}
    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.post("/register")
def register(payload: RegisterRequest):
    if not payload.username.strip() or not payload.password:
        raise HTTPException(status_code=400, detail="Username and password are required")

    created = create_user(payload.username, payload.password)
    if not created:
        raise HTTPException(status_code=409, detail="Username already exists")

    return {"message": "Registration successful", "username": payload.username}


@app.post("/predict")
def predict(payload: PredictRequest):
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Text input cannot be empty")
    try:
        result = model_service.predict(payload.text)
    except Exception as exc:
        print(f"[app] /predict error: {exc!r}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {exc}") from exc

    save_prediction(payload.username, payload.text, result["prediction"], result["confidence"])
    return result


@app.get("/metrics")
def metrics():
    try:
        return model_service.get_metrics()
    except Exception as exc:
        print(f"[app] /metrics error: {exc!r}")
        return {}


@app.get("/history")
def history() -> List[Dict]:
    return get_history(limit=100)

