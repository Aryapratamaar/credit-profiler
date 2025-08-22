from config import SCORING_WEIGHTS
from app.database import SessionLocal, CreditProfile
from helper.db_utils import save_profile_to_db

def calculate_credit_score(profile_data: dict, labels: list) -> dict:
    """
    Menghitung credit score berdasarkan profil seseorang
    Score range: 0-100
    """
    score = 0
    score_breakdown = {}

    #Age
    age_text = profile_data.get("age", "")
    age_num = extract_age_number(age_text)
    age_score = get_age_score(age_num)
    score += age_score
    score_breakdown["age"] = {"score": age_score}

    #Job
    job = profile_data.get("job", "").lower()
    job_score = calculate_job_score(job)
    score += job_score
    score_breakdown["job"] = {"score": job_score}

    #Hobbies
    hobbies = profile_data.get("hobbies", [])
    hobby_score = calculate_hobby_score(hobbies)
    score += hobby_score
    score_breakdown["hobbies"] = {"score": hobby_score}

    #City
    city = profile_data.get("city", "").lower()
    city_score = calculate_city_score(city)
    score += city_score
    score_breakdown["city"] = {"score": city_score}

    #Personality scoring
    personality = profile_data.get("personality", "").lower()
    personality_score = calculate_personality_score(personality)
    score += personality_score
    score_breakdown["personality"] = {"score": personality_score}

    final_score = min(score, 100)
    risk_level = get_risk_level(final_score)

    # save_profile_to_db(profile_data, labels, final_score, risk_level)

    return {
        "final_score": final_score,
        "risk_level": risk_level,
        "score_breakdown": score_breakdown,
    }

def extract_age_number(age_text: str) -> int:
    import re
    numbers = re.findall(r'\d+', age_text)
    return int(numbers[0]) if numbers else 25

def get_age_score(age: int) -> int:
    max_score = SCORING_WEIGHTS["age"]
    if 25 <= age <= 45:
        return max_score
    elif 18 <= age <= 60:
        return int(max_score * 0.8)
    elif age > 60:
        return int(max_score * 0.6)
    return int(max_score * 0.2)

def calculate_job_score(job: str) -> int:
    max_score = SCORING_WEIGHTS["job"]
    job_map = [
        (30, ["dokter", "engineer", "dosen", "pegawai negeri", "pns", "manager", "direktur"]),
        (25, ["guru", "perawat", "akuntan", "programmer", "analyst", "konsultan"]),
        (20, ["wiraswasta", "pengusaha", "freelancer", "owner", "founder"]),
        (15, ["sales", "marketing", "customer", "admin", "sekretaris"]),
        (10, ["sopir", "tukang", "buruh", "kuli", "ojek"]),
        (5, ["mahasiswa", "pelajar", "tidak bekerja", "pengangguran"])
    ]
    for score, keywords in job_map:
        if any(keyword in job for keyword in keywords):
            return min(score, max_score)
    return int(max_score * 0.5)  # default score

def calculate_hobby_score(hobbies: list) -> int:
    max_score = SCORING_WEIGHTS["hobbies"]
    score = 0
    positive = ["membaca", "olahraga", "investasi", "menabung", "berkebun", "memasak", "belajar"]
    expensive = ["traveling", "belanja", "shopping", "koleksi", "otomotif", "gadget"]
    neutral = ["musik", "film", "game", "fotografi", "menulis"]

    for hobby in hobbies:
        hobby_lower = hobby.lower()
        if any(pos in hobby_lower for pos in positive):
            score += 5
        elif any(exp in hobby_lower for exp in expensive):
            score -= 2
        elif any(neu in hobby_lower for neu in neutral):
            score += 2

    return max(0, min(score, max_score))

def calculate_city_score(city: str) -> int:
    max_score = SCORING_WEIGHTS["city"]
    if any(c in city for c in ["jakarta", "surabaya", "bandung", "medan", "semarang", "makassar"]):
        return max_score
    elif any(c in city for c in ["yogyakarta", "solo", "malang", "denpasar", "palembang"]):
        return int(max_score * 0.8)
    return int(max_score * 0.5)

def calculate_personality_score(personality: str) -> int:
    max_score = SCORING_WEIGHTS["personality"]
    positive = ["bertanggung jawab", "disiplin", "jujur", "reliable", "stabil", "pekerja keras"]
    negative = ["impulsif", "boros", "malas", "tidak konsisten", "ceroboh"]
    score = 5
    for trait in positive:
        if trait in personality:
            score += 2
    for trait in negative:
        if trait in personality:
            score -= 3
    return max(0, min(score, max_score))

def get_risk_level(score: int) -> str:
    if score >= 80:
        return "Very Low Risk"
    elif score >= 65:
        return "Low Risk"
    elif score >= 50:
        return "Medium Risk"
    elif score >= 35:
        return "High Risk"
    return "Very High Risk"
