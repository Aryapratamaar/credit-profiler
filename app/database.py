from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime, Time, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import TIME
from datetime import datetime, time, date
from config import DATABASE_URL
from typing import Optional

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    uid: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    passwordHash: Mapped[str] = mapped_column(String, nullable=False)

    # Waktu (naive, dari Python)
    createdDate: Mapped[Optional[date]] = mapped_column(
        Date(), nullable=True, default=date.today
    )
    createdTime: Mapped[Optional[time]] = mapped_column(
        Time(), nullable=True, default=lambda: datetime.now().replace(microsecond=0).time()
    )
    updatedDate: Mapped[Optional[datetime]] = mapped_column(DateTime(), nullable=True)
    deletedDate: Mapped[Optional[datetime]] = mapped_column(DateTime(), nullable=True)

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
    
    createdDate: Mapped[Optional[date]] = mapped_column(
        Date(),
        nullable=True,
        default=date.today,
    )
    
    createdTime: Mapped[Optional[time]] = mapped_column(
        TIME(precision=0),
        nullable=True,
        default=lambda: datetime.now().replace(microsecond=0).time(),
    )
    
    updatedDate: Mapped[Optional[datetime]] = mapped_column(
        DateTime(),
        nullable=True
    )
    deletedDate: Mapped[Optional[datetime]] = mapped_column(
        DateTime(),
        nullable=True                
    )
    
    uid: Mapped[Optional[str]] = mapped_column(
        String(64), ForeignKey("users.uid"), nullable=True
    )

class SalesRecommendation(Base):
    __tablename__ = "sales_recommendations"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer)
    do = Column(JSON)
    dont = Column(JSON)
    style = Column(String)
    relevant_products = Column(JSON)
    opener = Column(String)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()