from datetime import datetime

def get_today():
    now = datetime.now()
    hari_eng = now.strftime("%A").lower()
    hari_map = {
        "monday": "senin",
        "tuesday": "selasa",
        "wednesday": "rabu",
        "thursday": "kamis",
        "friday": "jumat",
        "saturday": "sabtu",
        "sunday": "minggu"
    }
    hari = hari_map.get(hari_eng, hari_eng)
    tanggal = now.strftime("%d-%m-%Y")
    waktu = now.strftime("%H:%M:%S")
    return hari, tanggal, waktu