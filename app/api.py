from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator, constr
from typing import List, Annotated

from helper.cleaner import clean_hobbies, clean_city, clean_personality

from app.database import SessionLocal, CreditProfile
from app.database import SalesRecommendation

from app.parse import profile_parse
from app.scoring import calculate_credit_score
from app.label_extractor import classify_label_ai
from app.recommender import generate_whatsapp_recommendation, generate_opener, get_targeted_products

app = FastAPI(title="Credit Profiler API", version="1.0.0")

class NameInput(BaseModel):
    name: str

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

@app.post("/manual-profile")
def manual_profile(data: ManualProfileInput):
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
            "risk_level": credit_score["risk_level"]
        })
        db.add(new_profile)
        db.commit()
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


@app.get("/suggestion/{id}")
def get_chat_suggestion(id: int):
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
