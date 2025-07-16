def profile_parse(text: str) -> dict:
    lines = text.strip().split("\n")
    print("DEBUG:", lines)

    # Ambil line hobi dan buang label
    hobby_line = lines[3].replace("- Hobi:", "").strip()
    # Pisahkan berdasarkan koma dulu
    hobby_parts = hobby_line.split(",")
    # Kemudian pisahkan juga berdasarkan 'dan' di setiap bagian
    hobbies = []
    for part in hobby_parts:
        for h in part.split("dan"):
            clean = h.strip()
            if clean and clean not in hobbies:
                hobbies.append(clean)

    return {
        "name": lines[0].replace("- Nama:", "").strip(),
        "age": lines[1].replace("- Umur:", "").strip(),
        "job": lines[2].replace("- Pekerjaan:", "").strip(),
        "hobbies": hobbies,
        "city": lines[4].replace("- Kota asal:", "").strip(),
        "personality": lines[5].replace("- Kepribadian:", "").strip()
    }
    
    