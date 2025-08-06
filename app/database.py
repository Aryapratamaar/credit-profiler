from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import DATABASE_URL

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

class SalesRecommendation(Base):
    __tablename__ = "sales_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer)
    do = Column(JSON)
    dont = Column(JSON)
    style = Column(String)
    relevant_products = Column(JSON)
    opener = Column(String)
