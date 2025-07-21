from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator, constr
from app.generate import profile_generate
from app.parse import profile_parse
from app.scoring import calculate_credit_score
from typing import List, Annotated
from app.database import SessionLocal, CreditProfile
from app.label_extractor import classify_label_ai
from helper.cleaner import clean_hobbies, clean_city, clean_personality

app = FastAPI(title="Credit Profiler API", version="1.0.0")

class NameInput(BaseModel):
    name: str

class ManualProfileInput(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=50, pattern=r"^[A-Za-z\s]+$")]
    age: Annotated[int, Field(ge=17, le=100)]
    job: Annotated[str, Field(min_length=3)]
    hobbies: Annotated[List[str], Field(min_items=1, max_items=5)]
    city: Annotated[str, Field(min_length=3)]
    personality: Annotated[str, Field(min_length=5)]

    @field_validator("hobbies")
    @classmethod
    def validate_hobbies(cls, v):
        if any(h.strip() == "" for h in v):
            raise ValueError("Hobi tidak boleh kosong")
        return v

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

        return {
            "profile": profile_dict,
            "credit_analysis": credit_score
        }

    except Exception as e:
        return {
            "error": str(e),
            "message": "Gagal menyimpan dari input manual"
        }

# @app.post("/input-profile")
# def generate_profile(data: NameInput):
    # """
    # Input profile and score for a person
    # """
    # try:
    #     raw_output = profile_generate(data.name)
    #     parsed_result = profile_parse(raw_output)
    #     labels = classify_label_ai(parsed_result)
    #     parsed_result["labels"] = labels

    #     credit_score = calculate_credit_score(parsed_result, labels)
        
    #     return {
    #         "profile": parsed_result,
    #         "credit_analysis": credit_score,
    #         "raw_ai_output": raw_output
    #     }
        
    # except Exception as e:
    #     return {
    #         "error": str(e),
    #         "message": "Failed to generate profile"
    #     }
