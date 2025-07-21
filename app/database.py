from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Ganti username, password, host, dbname sesuai PostgreSQL kamu
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/credit_profiler"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class CreditProfile(Base):
    __tablename__ = "credit_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(String)
    job = Column(String)
    hobbies = Column(JSON)
    city = Column(String)
    personality = Column(String)
    labels = Column(JSON)
    score = Column(Integer)
    risk_level = Column(String)

