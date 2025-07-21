from langchain_ollama import OllamaLLM
import ast

def classify_label_ai(profile_data):
    prompt = f"""
    Tugasmu adalah mengklasifikasikan profil seseorang menjadi maksimal 3 label pendek yang relevan. 
    Label mencerminkan *minat atau gaya hidup*, bukan tipe umum seperti "orang", "pribadi", atau "manusia".

    ⚠️ Jangan buat label umum seperti: "person", "activity", "other", dll. 
    ⚠️ Fokus pada apa yang terlihat dari hobi, pekerjaan, dan kepribadian.

    Format: list Python valid, tanpa markdown atau penjelasan.

    Data:
    - Hobi: {", ".join(profile_data['hobbies'])}
    - Kepribadian: {profile_data['personality']}
    - Pekerjaan: {profile_data['job']}

    Jawaban:
    """
    llm = OllamaLLM(model="gemma:2b")
    # llm = OllamaLLM(model="phi3:mini")

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
