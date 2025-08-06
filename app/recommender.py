from config import LLM_MODELS, PRESET_GUIDELINES_PATH
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
from pathlib import Path

import json
import os
import ast
import re

PRODUCT_MAPPING_PATH = os.path.abspath("product_targeting.json")
path = Path(PRESET_GUIDELINES_PATH)

def generate_opener(labels, relevant_products):
    label = labels[0] if labels else ""
    product = relevant_products[0] if relevant_products else "produk dari BNI"

    mapping = {
        "culinary_enthusiast": (
            f"Halo Kak 👋 Semoga harinya menyenangkan ya. Lagi suka eksplor kuliner juga nggak, Kak? 😄\n"
            f"Soalnya bulan ini ada beberapa promo makan seru dari BNI — bisa lebih hemat kalau pakai Kredit Fleksi 🙌\n"
            f"Biasanya Kakak suka jajan di mana nih? Bisa aja tempat favorit Kakak termasuk yang promo 😋"
        ),
        "culinary_business": (
            f"Halo Kak 👋 Semoga usahanya lancar ya hari ini 🙏\n"
            f"Banyak pelaku usaha kuliner yang lagi kembangkan bisnisnya terbantu dengan KUR BNI — modal usaha bisa sampai 50 juta dengan bunga ringan.\n"
            f"Kalau boleh tahu, Kakak lagi jualan apa nih sekarang? Siapa tahu bisa kami bantu juga 😊"
        ),
        "travel": (
            f"Halo Kak 👋 Semoga harinya menyenangkan ya!\n"
            f"Lagi ada rencana liburan atau trip seru dalam waktu dekat? ✈️\n"
            f"BNI lagi punya promo pembiayaan yang bisa bantu wujudkan liburan impian dengan cicilan ringan.\n"
            f"Kalau boleh tahu, Kakak paling pengen jalan-jalan ke mana, nih? 😄"
        ),
        "tech": (
            f"Halo Kak 👋 Semoga aktivitasnya lancar ya!\n"
            f"Lagi kepikiran upgrade gadget atau alat kerja nggak nih? 💻\n"
            f"BNI punya opsi pembiayaan ringan buat bantu Kakak tetap produktif tanpa harus nunggu tabungan penuh 🙌\n"
            f"Kalau boleh tahu, perangkat apa yang lagi Kakak butuhkan sekarang?"
        ),
        "finance": (
            f"Halo Kak 👋 Semoga keuangannya selalu stabil dan aman ya 🙏\n"
            f"Kalau lagi nyusun rencana finansial, BNI punya pilihan pembiayaan atau tabungan yang bisa disesuaikan.\n"
            f"Biasanya Kakak lebih suka atur cash flow bulanan, atau ada target jangka panjang yang lagi dikejar?"
        ),
        "health": (
            f"Halo Kak 👋 Semoga selalu sehat dan semangat ya hari ini 🙌\n"
            f"Kalau lagi ada kebutuhan untuk perawatan atau beli alat kesehatan, BNI punya pembiayaan fleksibel yang bisa bantu banget.\n"
            f"Kakak sendiri biasanya fokus ke preventif atau pengobatan nih?"
        ),
        "sport": (
            f"Halo Kak 👋 Lagi semangat olahraga juga ya belakangan ini? 💪\n"
            f"Kalau Kakak butuh alat olahraga atau mau daftar member gym, ada pilihan pembiayaan ringan dari BNI yang bisa bantu 🙌\n"
            f"Biasanya Kakak paling suka olahraga apa nih?"
        )
    }

    return mapping.get(
        label,
        f"Halo Kak 👋 Saya dari BNI. Kalau Kakak sedang punya kebutuhan tertentu, {product} ini bisa disesuaikan untuk bantu rencana Kakak. Saya siap bantu jawab kalau ada yang ingin ditanyakan ya 🙏"
    )

def get_targeted_products(labels):
    try:
        with open(PRODUCT_MAPPING_PATH, "r", encoding="utf-8") as f:
            mapping = json.load(f)

        products = []
        for label in labels:
            products.extend(mapping.get(label, []))

        return list(set(products))  # hapus duplikat jika ada
    except Exception as e:
        print("[Produk Recommender Error]", e)
        return []

def generate_whatsapp_recommendation(labels: list) -> dict:
    llm = OllamaLLM(model=LLM_MODELS["whatsapp_recommender"])

    prompt = PromptTemplate.from_template("""
    Kamu adalah asisten penjualan pintar untuk bank yang menawarkan produk kredit via WhatsApp.

    Berdasarkan *label minat pribadi* berikut: {labels}

    Tugasmu:
    - Sebutkan 3 hal yang *boleh dilakukan* (do) saat menawarkan produk kredit
    - Sebutkan 3 hal yang *tidak boleh dilakukan* (don't) saat menawarkan produk kredit

    ⚠️ Format jawaban HARUS seperti ini dan tidak boleh ada penjelasan tambahan:
    {{
      "do": ["..."],
      "dont": ["..."],
    }}
    """)

    formatted_prompt = prompt.format(labels=", ".join(labels))
    response = llm.invoke(formatted_prompt)
    relevant_products = get_targeted_products(labels)
    print(relevant_products)
    
    opener = generate_opener(labels, relevant_products)

    try:
        match = re.search(r"\{[\s\S]+\}", response)
        if match:
            parsed = ast.literal_eval(match.group())
            parsed["relevant_products"] = relevant_products 
            parsed["opener"] = opener
            print("[DEBUG] Labels:", labels)
            print("[DEBUG] Relevant Products:", relevant_products)
            return parsed
        else:
            raise ValueError("Format AI tidak sesuai")
    except Exception as e:
        return {
            "do": ["Tawarkan produk sesuai kebutuhan nasabah"],
            "dont": ["Jangan terlalu agresif dalam promosi"],
            "relevant_products": relevant_products,
            "opener": opener
        }
