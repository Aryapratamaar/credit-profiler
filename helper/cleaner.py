def clean_hobbies(hobbies_raw):
    if isinstance(hobbies_raw, str):
        hobbies = hobbies_raw.replace("dan", "").split(",")
    else:
        hobbies = hobbies_raw

    return list(dict.fromkeys([
        h.strip().lower()
        for h in hobbies
        if h.strip()
    ]))

def clean_city(city: str):
    return " ".join(city.strip().lower().split())

def clean_personality(personality: str):
    traits = personality.replace("dan", ",").split(",")
    return ", ".join(dict.fromkeys([
        t.strip().lower()
        for t in traits
        if t.strip()
    ]))
