from config import LLM_MODELS, PREDEFINED_LABELS_HOBBIES,PRODUCT_MAPPING_PATH
from langchain_ollama import OllamaLLM
import ast
import json

def get_targeted_products(labels):
    try:
        with open(PRODUCT_MAPPING_PATH, "r", encoding="utf-8") as f:
          mapping = json.load(f)

        products = []
        for label in labels:
            products.extend(mapping.get(label, []))

        return list(set(products))
    except Exception as e:
        print("[Produk Recommender Error]", e)
        return []

def classify_label_ai(profile_data):
    prompt = f"""
    Tugasmu adalah mengklasifikasikan profil seseorang menjadi label pendek yang relevan berdasarkan hobi dan aktivitas yang disebutkan.
    
    Berikut ini adalah daftar label yang diperbolehkan:
    - culinary_business → untuk pelaku usaha makanan seperti jualan nasi goreng, katering, UMKM makanan
    - culinary_enthusiast → untuk orang yang hobi kulineran, suka jajan makanan
    - travel
    - tech
    - finance
    - health
    - sport
    
    ⚠️ Fokus pada makna sebenarnya dari hobi, bukan sekadar kata kunci. Tanyakan pada dirimu: “Orang ini suka makan atau sedang jualan?”
    
    Format: list Python valid, TANPA markdown atau penjelasan tambahan.
    
    Data:
    - Hobi: {profile_data['hobbies']}
    
    Kosongkan jika tidak ada hobi yang relevan.

    Jawaban:
    """

    llm = OllamaLLM(model=LLM_MODELS["label_extractor"])
    response = llm.invoke(prompt)

    try:
        parsed = ast.literal_eval(response.strip())
        valid_labels = set(PREDEFINED_LABELS_HOBBIES)
        parsed = [label.strip().lower() for label in parsed if label.strip().lower() in valid_labels]

        if isinstance(parsed, list):
            return [str(item).strip().lower() for item in parsed]
    except Exception as e:
        print("[Parsing error]:", e)

        # Fallback: parse manual dari string koma
        fallback = response.strip().replace("[", "").replace("]", "").replace('"', "").replace("'", "")
        return [label.strip().lower() for label in fallback.split(",") if label.strip()]

    return []
