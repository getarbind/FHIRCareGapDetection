from sqlalchemy.orm import Session
from app.db.models import Patient, CareGap, User


# ── User ──────────────────────────────────────────────
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, username: str, email: str, hashed_password: str, full_name: str = "", role: str = "patient"):
    user = User(username=username, email=email, hashed_password=hashed_password, full_name=full_name, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# ── Patients ───────────────────────────────────────────
def get_all_patients(db: Session):
    return db.query(Patient).all()


def get_patient_by_id(db: Session, patient_id: int):
    return db.query(Patient).filter(Patient.id == patient_id).first()


# ── Care Gaps ──────────────────────────────────────────
def get_all_care_gaps(db: Session):
    return db.query(CareGap).all()


def get_care_gaps_by_patient(db: Session, patient_id: int):
    return db.query(CareGap).filter(CareGap.patient_id == patient_id).all()
