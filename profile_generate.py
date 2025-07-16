from ollama import Client

client = Client()

def profile_generate(name: str) -> str:
    prompt = f"""
    Buatkan profil singkat tentang seseorang bernama {name}.
    Format:
    - Nama:
    - Umur:
    - Pekerjaan:
    - Hobi:
    - Kota asal:
    - Kepribadian:
    """
    
    response = client.chat(
        model="mistral",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response['message']['content']
