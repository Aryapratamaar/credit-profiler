from app.database import SessionLocal, CreditProfile
from helper.db_utils import save_profile_to_db

def calculate_credit_score(profile_data: dict, labels: list) -> dict:
    """
    Menghitung credit score berdasarkan profil seseorang
    Score range: 0-100
    """
    
    score = 0
    score_breakdown = {}
    
    # 1. Age scoring (25 points max)
    age_text = profile_data.get("age", "")
    age_num = extract_age_number(age_text)
    
    if 25 <= age_num <= 45:
        age_score = 25
    elif 18 <= age_num <= 60:
        age_score = 20
    elif age_num > 60:
        age_score = 15
    else:
        age_score = 5
    
    score += age_score
    score_breakdown["age"] = {"score": age_score}
    # score_breakdown["age"] = {"score": age_score, "detail": f"Umur {age_num} tahun"}
    
    # 2. Job scoring (30 points max)
    job = profile_data.get("job", "").lower()
    job_score = calculate_job_score(job)
    
    score += job_score
    score_breakdown["job"] = {"score": job_score}
    
    # 3. Hobbies scoring (20 points max)
    hobbies = profile_data.get("hobbies", [])
    hobby_score = calculate_hobby_score(hobbies)
    
    score += hobby_score
    score_breakdown["hobbies"] = {"score": hobby_score}
    
    # 4. City scoring (15 points max)
    city = profile_data.get("city", "").lower()
    city_score = calculate_city_score(city)
    
    score += city_score
    score_breakdown["city"] = {"score": city_score}
    
    # 5. Personality scoring (10 points max)
    personality = profile_data.get("personality", "").lower()
    personality_score = calculate_personality_score(personality)
    
    score += personality_score
    score_breakdown["personality"] = {"score": personality_score}
    
    # Ensure score doesn't exceed 100
    final_score = min(score, 100)
    

    # Simpan data ke database via helper
    save_profile_to_db(profile_data, labels, final_score, get_risk_level(final_score))

    return {
        "final_score": final_score,
        "risk_level": get_risk_level(final_score),
        "score_breakdown": score_breakdown,
    }

def extract_age_number(age_text: str) -> int:
    """Extract age number from text like '32 tahun'"""
    import re
    numbers = re.findall(r'\d+', age_text)
    return int(numbers[0]) if numbers else 25

def calculate_job_score(job: str) -> int:
    """Calculate score based on job stability and income potential"""
    
    # High stability jobs
    if any(keyword in job for keyword in ["dokter", "engineer", "dosen", "pegawai negeri", "pns", "manager", "direktur"]):
        return 30
    
    # Medium stability jobs
    elif any(keyword in job for keyword in ["guru", "perawat", "akuntan", "programmer", "analyst", "konsultan"]):
        return 25
    
    # Self-employed/entrepreneur
    elif any(keyword in job for keyword in ["wiraswasta", "pengusaha", "freelancer", "owner", "founder"]):
        return 20
    
    # Service jobs
    elif any(keyword in job for keyword in ["sales", "marketing", "customer", "admin", "sekretaris"]):
        return 15
    
    # Manual labor
    elif any(keyword in job for keyword in ["sopir", "tukang", "buruh", "kuli", "ojek"]):
        return 10
    
    # Student/unemployed
    elif any(keyword in job for keyword in ["mahasiswa", "pelajar", "tidak bekerja", "pengangguran", " ", ""]):
        return 5
    
    # Default
    else:
        return 15

def calculate_hobby_score(hobbies: list) -> int:
    """Calculate score based on hobbies (financial responsibility indicators)"""
    
    score = 0
    
    # Positive hobbies (show discipline/investment mindset)
    positive_hobbies = ["membaca", "olahraga", "investasi", "menabung", "berkebun", "memasak", "belajar"]
    
    # Expensive hobbies (potential financial burden)
    expensive_hobbies = ["traveling", "belanja", "shopping", "koleksi", "otomotif", "gadget"]
    
    # Neutral hobbies
    neutral_hobbies = ["musik", "film", "game", "fotografi", "menulis"]
    
    for hobby in hobbies:
        hobby_lower = hobby.lower()
        
        if any(pos in hobby_lower for pos in positive_hobbies):
            score += 5
        elif any(exp in hobby_lower for exp in expensive_hobbies):
            score -= 2
        elif any(neu in hobby_lower for neu in neutral_hobbies):
            score += 2
    
    # Ensure score is between 0-20
    return max(0, min(score, 20))

def calculate_city_score(city: str) -> int:
    """Calculate score based on city (economic opportunities)"""
    
    # Major cities (high economic activity)
    if any(major in city for major in ["jakarta", "surabaya", "bandung", "medan", "semarang", "makassar"]):
        return 15
    
    # Medium cities
    elif any(medium in city for medium in ["yogyakarta", "solo", "malang", "denpasar", "palembang"]):
        return 12
    
    # Small cities/rural
    else:
        return 8

def calculate_personality_score(personality: str) -> int:
    """Calculate score based on personality traits"""
    
    # Positive traits for credit
    positive_traits = ["bertanggung jawab", "disiplin", "jujur", "reliable", "stabil", "pekerja keras"]
    
    # Negative traits for credit
    negative_traits = ["impulsif", "boros", "malas", "tidak konsisten", "ceroboh"]
    
    score = 5  # Base score
    
    for trait in positive_traits:
        if trait in personality:
            score += 2
    
    for trait in negative_traits:
        if trait in personality:
            score -= 3
    
    return max(0, min(score, 10))

def get_risk_level(score: int) -> str:
    """Determine risk level based on score"""
    
    if score >= 80:
        return "Very Low Risk"
    elif score >= 65:
        return "Low Risk"
    elif score >= 50:
        return "Medium Risk"
    elif score >= 35:
        return "High Risk"
    else:
        return "Very High Risk"
    

