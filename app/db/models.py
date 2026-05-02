from sqlalchemy import Column, Integer, Text, Date, ForeignKey
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(Text, unique=True, nullable=False, index=True)
    email = Column(Text, unique=True, nullable=False)
    hashed_password = Column(Text, nullable=False)
    full_name = Column(Text)
    role = Column(Text, nullable=False, default="patient")

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    gender = Column(Text)
    birth_date = Column(Date)
    age = Column(Integer)
    language = Column(Text)
    marital_status = Column(Text)
    phone = Column(Text)
    address = Column(Text)


class CareGap(Base):
    __tablename__ = "care_gaps"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    gap_type = Column(Text, nullable=False)
    status = Column(Text)
    description = Column(Text)