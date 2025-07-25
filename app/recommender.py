from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
import ast
import re

def generate_whatsapp_recommendation(labels: list) -> dict:
    llm = OllamaLLM(model="openhermes")

    prompt = PromptTemplate.from_template("""
    Kamu adalah asisten penjualan pintar untuk bank yang menawarkan produk kredit via WhatsApp.

    Berdasarkan *label minat pribadi* berikut: {labels}

    Tugasmu:
    - Sebutkan 3 hal yang *boleh dilakukan* (do) saat menawarkan produk kredit
    - Sebutkan 3 hal yang *tidak boleh dilakukan* (don't)
    - Tentukan gaya komunikasi yang cocok (style)
    - Rekomendasikan 2 produk kredit yang sesuai (relevant_products)
    - Buat 1 kalimat pembuka WhatsApp yang menarik (opener)

    ⚠️ Format jawaban HARUS seperti ini dan tidak boleh ada penjelasan tambahan:
    {{
      "do": ["..."],
      "dont": ["..."],
      "style": "...",
      "relevant_products": ["...", "..."],
      "opener": "..."
    }}
    """)

    formatted_prompt = prompt.format(labels=", ".join(labels))
    response = llm.invoke(formatted_prompt)

    try:
        # Ambil hanya bagian dictionary
        match = re.search(r"\{[\s\S]+\}", response)
        if match:
            return ast.literal_eval(match.group())
        else:
            raise ValueError("Format AI tidak sesuai")

    except Exception as e:
        return {
            "do": ["Gagal memproses AI output"],
            "dont": [str(e)],
            "style": "-",
            "relevant_products": [],
            "opener": "-"
        }
