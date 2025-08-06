#DB
DATABASE_URL = "postgresql://postgres:1234@localhost:5432/credit_profiler"

#SERVER
API_HOST = "127.0.0.1"
API_PORT = 8000
DEBUG_MODE = True  #reload

#Model yang dipakai
LLM_MODELS = {
    "label_extractor": "mistral",
    "whatsapp_recommender": "openhermes"
}

#Label dari hobi
PREDEFINED_LABELS_HOBBIES = [
    "culinary_business", "culinary_enthusiast",
    "travel", "tech", "finance", "health", "sport"
]
PRESET_GUIDELINES_PATH = "preset_guidelines.json"
PRODUCT_MAPPING_PATH = "product_targeting.json"

#Atur Skor maksimal
SCORING_WEIGHTS = {
    "age": 25,
    "job": 30,
    "hobbies": 20,
    "city": 15,
    "personality": 10
}

