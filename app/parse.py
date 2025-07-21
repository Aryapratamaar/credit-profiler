import re

def profile_parse(text: str) -> dict:
    lines = text.strip().split("\n")
    print("DEBUG:", lines)

    data = {
        "name": "",
        "age": "",
        "job": "",
        "hobbies": [],
        "city": "",
        "personality": ""
    }

    # Map kata kunci ke key utama
    label_map = {
        "nama": "name",
        "umur": "age",
        "pekerjaan": "job",
        "hobi": "hobbies",
        "kota": "city",
        "kota asal": "city",
        "kepribadian": "personality",
        "karakter": "personality"
    }

    for line in lines:
        if not line.strip():
            continue  # skip baris kosong

        # Regex cari pola **Label:** atau Label:
        match = re.match(r"\**\*?\*?(.+?)\*?\*?\**\s*:\s*(.+)", line.strip())
        if match:
            raw_label = match.group(1).strip().lower()
            value = match.group(2).lstrip("*").strip()

            for label, key in label_map.items():
                if label in raw_label:
                    if key == "hobbies":
                        raw_parts = value.split(",")
                        hobbies = []
                        for part in raw_parts:
                            for h in part.split("dan"):
                                clean = h.strip()
                                if clean and clean not in hobbies:
                                    hobbies.append(clean)
                        data["hobbies"] = hobbies
                    else:
                        data[key] = value
                    break

    # Validasi isi minimal
    if not all([data["name"], data["age"], data["job"], data["city"], data["personality"]]):
        raise ValueError("Output AI tidak lengkap atau label tidak dikenali.")

    return data
