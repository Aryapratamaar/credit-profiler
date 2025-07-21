from app.database import SessionLocal, CreditProfile

def save_profile_to_db(profile_data: dict, labels: list, score: int, risk_level: str):
    try:
        db = SessionLocal()
        db_profile = CreditProfile(
            name=profile_data.get("name"),
            age=profile_data.get("age"),
            job=profile_data.get("job"),
            hobbies=profile_data.get("hobbies"),
            city=profile_data.get("city"),
            personality=profile_data.get("personality"),
            labels=labels,
            score=score,
            risk_level=risk_level
        )
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
    except Exception as e:
        print("[DB Error] Gagal menyimpan profil:", e)
