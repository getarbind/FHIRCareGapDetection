from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.db.database import engine, Base, SessionLocal
from app.db import models  # noqa: F401
from app.db.database import get_db
from app.db.crud import (
    get_all_patients,
    get_patient_by_id,
    get_all_care_gaps,
    get_care_gaps_by_patient,
    get_user_by_username,
    get_user_by_email,
    create_user,
)
from app.auth import hash_password, verify_password, create_access_token, decode_access_token

Base.metadata.create_all(bind=engine)


def _seed_default_user():
    db = SessionLocal()
    try:
        if not get_user_by_username(db, "admin"):
            create_user(db, "admin", "admin@localhost", hash_password("admin"), "Administrator", "admin")
    finally:
        db.close()


_seed_default_user()

app = FastAPI(title="FHIR Care Gap Backend")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

VALID_ROLES = {"patient", "clinician", "admin", "analyst"}


# ── Pydantic schemas ───────────────────────────────────
class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    full_name: str = ""
    role: str = "patient"


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str
    full_name: str
    role: str


# ── Auth helpers ───────────────────────────────────────
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    user = get_user_by_username(db, payload.get("sub"))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user


# ── Auth routes ────────────────────────────────────────
@app.get("/")
def root():
    return {"message": "Backend is running"}


@app.post("/auth/register", response_model=TokenResponse)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    if req.role not in VALID_ROLES:
        raise HTTPException(status_code=400, detail=f"Invalid role. Choose from: {', '.join(VALID_ROLES)}")
    if get_user_by_username(db, req.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    if get_user_by_email(db, req.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    user = create_user(db, req.username, req.email, hash_password(req.password), req.full_name, req.role)
    token = create_access_token({"sub": user.username})
    return TokenResponse(access_token=token, username=user.username, full_name=user.full_name, role=user.role)


@app.post("/auth/login", response_model=TokenResponse)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_username(db, form.username)
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = create_access_token({"sub": user.username})
    return TokenResponse(access_token=token, username=user.username, full_name=user.full_name, role=user.role)


@app.get("/auth/me")
def get_me(current_user=Depends(get_current_user)):
    return {
        "username": current_user.username,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
    }


# ── Patient routes (protected) ─────────────────────────
@app.get("/patients")
def read_patients(db: Session = Depends(get_db), _=Depends(get_current_user)):
    patients = get_all_patients(db)
    return [
        {
            "id": p.id, "name": p.name, "gender": p.gender,
            "birth_date": str(p.birth_date) if p.birth_date else None,
            "age": p.age, "language": p.language,
            "marital_status": p.marital_status, "phone": p.phone, "address": p.address,
        }
        for p in patients
    ]


@app.get("/patients/{patient_id}")
def read_patient(patient_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    p = get_patient_by_id(db, patient_id)
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {
        "id": p.id, "name": p.name, "gender": p.gender,
        "birth_date": str(p.birth_date) if p.birth_date else None,
        "age": p.age, "language": p.language,
        "marital_status": p.marital_status, "phone": p.phone, "address": p.address,
    }


@app.get("/care-gaps")
def read_care_gaps(db: Session = Depends(get_db), _=Depends(get_current_user)):
    gaps = get_all_care_gaps(db)
    return [
        {"id": g.id, "patient_id": g.patient_id, "gap_type": g.gap_type, "status": g.status, "description": g.description}
        for g in gaps
    ]


@app.get("/patients/{patient_id}/care-gaps")
def read_patient_care_gaps(patient_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    gaps = get_care_gaps_by_patient(db, patient_id)
    return [
        {"id": g.id, "patient_id": g.patient_id, "gap_type": g.gap_type, "status": g.status, "description": g.description}
        for g in gaps
    ]
