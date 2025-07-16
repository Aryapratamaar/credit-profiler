from fastapi import FastAPI
from pydantic import BaseModel
from generate_profile import generate_profile as generate_ai_profile  # Import dari file terpisah

app = FastAPI()

class NameInput(BaseModel):
    name: str

@app.post("/generate-profile")
def generate(data: NameInput):
    output = generate_ai_profile(data.name)

    # Cek output mentah
    lines = output.strip().split("\n")
    print("DEBUG:", lines)

    parsed = {
        "name": lines[0].replace("- Nama:", "").strip(),
        "age": lines[1].replace("- Umur:", "").strip(),
        "job": lines[2].replace("- Pekerjaan:", "").strip(),
        "hobbies": [h.strip() for h in lines[3].replace("- Hobi:", "").split(",")],
        "city": lines[4].replace("- Kota asal:", "").strip(),
        "personality": lines[5].replace("- Kepribadian:", "").strip()
    }

    return parsed
