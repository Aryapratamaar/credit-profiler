from ollama import Client

client = Client()

def profile_generate(name: str) -> str:
    prompt = f"""
    Kamu adalah sistem AI yang bertugas menghasilkan profil pengguna berdasarkan nama. 
    Buat profil dalam bahasa Indonesia dengan format PERSIS seperti di bawah ini, tanpa penjelasan tambahan, tanpa numbering, dan satu baris per elemen.

    FORMAT WAJIB:
    - Nama: [isi nama orang]
    - Umur: [dari 17-60 tahun]
    - Pekerjaan: [contoh: Programmer]
    - Hobi: [pisahkan dengan koma, boleh ada 'dan']
    - Kota asal: [kota, negara]
    - Kepribadian: [maksimal 1 kalimat deskriptif]

    Buatkan profil untuk nama: **{name}**
    Tampilkan langsung hasilnya sesuai format di atas.
    """

    response = client.chat(
        model="gemma:2b",  # atau model lain seperti mistral
        messages=[{"role": "user", "content": prompt}]
    )

    return response['message']['content']

    