from langchain_ollama import OllamaLLM
import ast

PREDEFINED_LABELS_HOBBIES = [
    "culinary", "travel", "tech", "finance", "health", "sport"
]

def classify_label_ai(profile_data):
    prompt = f"""
    Tugasmu adalah mengklasifikasikan profil seseorang menjadi label pendek yang relevan. 
    Berikut ini adalah daftar label yang diperbolehkan:
    {', '.join(PREDEFINED_LABELS_HOBBIES)}

    ⚠️ Fokus pada apa yang terlihat dari hobi

    Format: list Python valid, TANPA markdown atau penjelasan atau catatan.

    Data:
    - Hobi: {profile_data['hobbies']}

    Tolong pilih label yang paling sesuai dari daftar tersebut berdasarkan data profil di atas. 
    ⚠️ Balas hanya dengan format list Python seperti ini: ["label1"]

    Jawaban:
    """
    
    # llm = OllamaLLM(model="gemma:2b")
    # llm = OllamaLLM(model="phi3:mini")
    # llm = OllamaLLM(model="mistral")
    llm = OllamaLLM(model="openhermes")

    response = llm.invoke(prompt)

    try:
        parsed = ast.literal_eval(response.strip())
        if isinstance(parsed, list):
            return [str(item).strip().lower() for item in parsed]
    except Exception as e:
        print("[Parsing error]:", e)

        # Fallback: parse manual dari string koma
        fallback = response.strip().replace("[", "").replace("]", "").replace('"', "").replace("'", "")
        return [label.strip().lower() for label in fallback.split(",") if label.strip()]

    return []
