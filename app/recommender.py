from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

import ast

def generate_whatsapp_recommendation(labels: list) -> dict:
    # llm = Ollama(model="phi3:mini") 
    llm = OllamaLLM(model="mistral")

    prompt = PromptTemplate.from_template("""
    Kamu adalah pakar komunikasi pemasaran via WhatsApp.

    Berdasarkan *label minat pribadi* berikut: {labels}

    Tentukan:
    - 3 hal yang *boleh dilakukan* (Do) saat menawarkan produk kredit via WhatsApp
    - 3 hal yang *tidak boleh dilakukan* (Don't)

    Fokuskan pendekatan berdasarkan minat nasabah yang tercermin dari label-label tersebut.

    ❌ Jangan gunakan istilah generik seperti "layanan cepat dan mudah", "semua konsumen", atau "chatbot".
    ✅ Gunakan strategi spesifik, misalnya: "Gunakan contoh benefit cicilan untuk keperluan olahraga outdoor".

    Format jawaban:
    {{
    "do": ["...", "...", "..."],
    "dont": ["...", "...", "..."]
    }}

    Jawaban harus valid dalam format Python dictionary. Tidak ada penjelasan tambahan.
    """)

    formatted_prompt = prompt.format(labels=", ".join(labels))
    response = llm.invoke(formatted_prompt)

    try:
        return ast.literal_eval(response)
    except Exception as e:
        return {
            "do": ["Gagal memproses AI output"],
            "dont": [str(e)]
        }
