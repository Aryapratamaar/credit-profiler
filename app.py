from fastapi import FastAPI
from pydantic import BaseModel
from profile_generate import profile_generate
from profile_parse import profile_parse

app = FastAPI()

class NameInput(BaseModel):
    name: str

@app.post("/generate-profile")
def generate(data: NameInput):
    raw_output = profile_generate(data.name)
    parsed_result = profile_parse(raw_output)
    return parsed_result
