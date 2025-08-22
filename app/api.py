from fastapi import FastAPI, HTTPException, APIRouter, Depends, HTTPException, status # pyright: ignore[reportMissingImports]
from pydantic import BaseModel, Field, field_validator
from typing import List, Annotated
from sqlalchemy.orm import Session
from sqlalchemy import select

from helper.cleaner import clean_hobbies, clean_city, clean_personality

from app.database import SessionLocal, CreditProfile, SalesRecommendation, User, get_db
from app.parse import profile_parse
from app.scoring import calculate_credit_score
from app.label_extractor import classify_label_ai
from app.recommender import generate_whatsapp_recommendation, generate_opener, get_targeted_products
from app.schemas_auth import RegisterIn, RegisterOut, UserPublic, LoginIn, LoginOut
from app.security import hash_password, verify_password
from app.jwt_utils import create_access_token

from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import select
from jose import jwt, JWTError
from config import JWT_SECRET, JWT_ALGORITHM
from app.database import get_db, User 
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
bearer_scheme = HTTPBearer()

TAGS_METADATA = [
    {"name": "auth",    "description": "Login & Register"},
    {"name": "profile", "description": "Manual Profile & Suggestions"},
]

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="missing bearer token")

    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")

    uid = payload.get("sub")
    if not uid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token subject")

    user = db.scalar(select(User).where(User.uid == uid))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="user not found")
    return user

router = APIRouter(prefix="/auth", tags=["auth"])
app = FastAPI(title="Credit Profiler API",
              version="1.0.0",
              openapi_tags=TAGS_METADATA,
              )
app.include_router(router)

class ManualProfileInput(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=50, pattern=r"^[A-Za-z\s]+$")]
    age: Annotated[int, Field(ge=17, le=100)]
    job: Annotated[str, Field(min_length=3)]
    hobbies: Annotated[str, Field(min_length=3)]
    city: Annotated[str, Field(min_length=3)]
    personality: Annotated[str, Field(min_length=5)]

    @field_validator("personality")
    @classmethod
    def validate_personality(cls, v):
        if len(v.split()) < 2:
            raise ValueError("Kepribadian minimal harus 2 kata")
        return v

@router.post("/register", response_model=RegisterOut, status_code=status.HTTP_201_CREATED, tags=["auth"])
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    existing = db.scalar(select(User).where(User.uid == payload.uid))
    if existing:
        raise HTTPException(status_code=409, detail="uid already exists")
    pwd_hash = hash_password(payload.password)
    
    user = User(
        uid=payload.uid,
        name=payload.name,
        passwordHash=pwd_hash,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return RegisterOut(ok=True, user=UserPublic(uid=user.uid, name=user.name))

@router.post("/login", response_model=LoginOut, tags=["auth"])
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.uid == payload.uid))

    if not user or not verify_password(payload.password, user.passwordHash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")

    token = create_access_token(subject=user.uid, extra_claims={"name": user.name})

    return LoginOut(
        accessToken=token,
        user=UserPublic(uid=user.uid, name=user.name),
    )

@app.post("/manual-profile", tags=["profile"])
def manual_profile(
    data: ManualProfileInput,
    current_user: User = Depends(get_current_user),
    ):
    try:
        profile_dict = {
            "name": data.name.strip(),
            "age": f"{data.age}",
            "job": data.job.strip(),
            "hobbies": clean_hobbies(data.hobbies),
            "city": clean_city(data.city),
            "personality": clean_personality(data.personality)
        }

        labels = classify_label_ai(profile_dict)
        profile_dict["labels"] = labels

        credit_score = calculate_credit_score(profile_dict, labels)

        # Simpan ke database
        db = SessionLocal()

        new_profile = CreditProfile(**{
            **profile_dict,
            "labels": labels,
            "score": credit_score["final_score"],
            "risk_level": credit_score["risk_level"],
            "uid" : current_user.uid,
        })
        db.add(new_profile)
        db.commit()
        print("aku dipanggil")
        db.refresh(new_profile)
        
        profile_dict["id"] = new_profile.id

        return {
            "profile": profile_dict,
            "credit_analysis": credit_score,
        }

    except Exception as e:
        return {
            "error": str(e),
            "message": "Gagal menyimpan dari input manual"
        }

@app.get("/suggestion/{id}", tags=["profile"])
def get_chat_suggestion(
    id: int,
    current_user: User = Depends(get_current_user),
    ):
    db = SessionLocal()
    profile = db.query(CreditProfile).filter(CreditProfile.id == id).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    if not profile.labels:
        raise HTTPException(status_code=400, detail="Profile does not have labels")

    # Handle label format (list atau string JSON)
    if isinstance(profile.labels, str):
        try:
            import json
            labels = json.loads(profile.labels)
        except:
            labels = [profile.labels]
    else:
        labels = profile.labels

    products = get_targeted_products(labels)
    strategy = generate_whatsapp_recommendation(labels)
    opener = generate_opener(labels, products)

    return {
        "id": profile.id,
        "name": profile.name,
        "labels": labels,
        "products": products,
        "recommendation": strategy,
    }

app.include_router(router)