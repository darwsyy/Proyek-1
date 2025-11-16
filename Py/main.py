import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.file_utils import safe_read, write_json
from utils.datetime_utils import get_today

def header(text):
    print("=" * 53)
    print(text.center(53))
    print("=" * 53,)

def header_jam(text):
    print(f"<< {text.center(20)} >>\n")

def prompt(msg):
    return input(msg)

def warn(msg):
    print(f"[PERINGATAN] {msg}")

def info(msg):
    print(msg)

def reset_status_if_new_day():
    status = safe_read("data/status_pengumpulan.json", {"tkj1": False, "tkj2": False})
    for k in status:
        status[k] = False
    write_json("data/status_pengumpulan.json", status)

def main():
    os.system('cls')
    header("< E-JOURNAL AREK AI >")

    while True:
        kelas = prompt("Masukkan kelas (tkj1/tkj2): ").lower()
        if kelas not in ["tkj1", "tkj2"]:
            warn("Kelas tidak valid.")
        else:
            os.system('cls')
            header("< E-JOURNAL AREK AI >")
            break
        
    # Reset status tiap hari baru
    reset_status_if_new_day()

    hari, tanggal, waktu = get_today()
    print(f"\nHari: {hari.capitalize()} | Tanggal: {tanggal} | Waktu: {waktu}\n")

    jadwal = safe_read("data/jadwal.json", {})
    if kelas not in jadwal or hari not in jadwal[kelas]:
        warn("Tidak ada jadwal untuk hari ini.")
        return

    pelajaran = jadwal[kelas][hari]
    data_harian = []
    jam_skip = []
    
    for i, mapel in enumerate(pelajaran, start=1):
        header_jam(f"Jam Pelajaran {i} - {mapel}")

    # OPSIONALITAS AWAL
        isi = prompt("Isi jurnal pada jam ini? (y/n): ").lower().strip()
        while isi not in ("y", "n"):
            warn("Masukkan hanya y atau n.")
            isi = prompt("Isi jurnal untuk jam ini? (y/n): ").lower().strip()
            
        if isi == "n":
            warn("Jam ini dilewati. Jangan lupa mengisi keterangan guru tidak masuk setelah jam selesai.\n")
            jam_skip.append(i)
            data_harian.append({
            "jam": i,
            "mapel": mapel,
            "guru": "-",
            "materi": "Guru tidak hadir (opsi skip)",
            "hadir": "-",
            "tidak_hadir": "-"
            })
            continue
    
        guru = prompt("> Nama guru pengajar\t\t: ")
        while not guru:
            warn("Tidak boleh kosong.")
            guru = prompt("> Nama guru pengajar\t\t: ").strip()
        
        materi = prompt("> Materi pelajaran\t\t: ")
        while not materi:
            warn("Tidak boleh kosong.")
            materi = prompt("> Nama guru pengajar\t\t: ").strip()

        tak_hadir = prompt("> Jumlah siswa tidak hadir\t: ").strip()
        while not tak_hadir.isdigit():
            warn("Masukkan angka.")
            tak_hadir = prompt("> Jumlah siswa tidak hadir\t: ").strip()
        
        if int(tak_hadir) > 37:
            warn("Jumlah ketidakhadiran tidak boleh melebihi jumlah siswa")
            print("cek dan masukan jumlah yang valid")
            if kelas == "tkj1":
                print("\n-> Jumlah siswa 36")
            else:
                print("\n-> Jumlah siswa 37")
            tak_hadir = prompt("> Jumlah siswa tidak hadir\t: ").strip()
            
        
        hadir_total = 36 if kelas == "tkj1" else 37
        hadir_siswa = hadir_total - int(tak_hadir)

        data_harian.append({
            "jam": i,
            "mapel": mapel,
            "guru": guru,
            "materi": materi,
            "hadir": hadir_siswa,
            "tidak_hadir": int(tak_hadir or 0)
        })
        
    if jam_skip:
        print("\n===== JAM YANG DI-SKIP =====")
        print("Jam yang dilewati:", jam_skip)
        print("=================================\n")

        ulang = prompt("Ingin mengisi jam yang dilewati? (y/n): ").lower().strip()
        while ulang not in ("y", "n"):
            warn("Masukkan y atau n.")
            ulang = prompt("Ingin mengisi jam yang dilewati? (y/n): ").lower().strip()

        if ulang == "y":
            for js in jam_skip:
                print(f"\n=== Mengisi ulang jam {js} ===")
                mapel = pelajaran[js - 1]

                guru_pengganti = prompt("> Nama guru pengganti\t\t: ")
                while not guru_pengganti:
                    warn("Tidak boleh kosong.")
                    guru = prompt("> Nama guru pengganti\t\t: ")
                
                materi = prompt("> Materi pelajaran\t\t: ")
                while not materi:
                    warn("Tidak boleh kosong.")
                    materi = prompt("> Materi pelajaran\t\t: ").strip()
                    
        tak_hadir = prompt("> Jumlah siswa tidak hadir\t: ").strip()
        while not tak_hadir.isdigit():
            warn("Masukkan angka.")
            tak_hadir = prompt("> Jumlah siswa tidak hadir\t: ").strip()
        
        if int(tak_hadir) > 37:
            warn("Jumlah ketidakhadiran tidak boleh melebihi jumlah siswa")
            print("cek dan masukan jumlah yang valid")
            if kelas == "tkj1":
                print("\n-> Jumlah siswa 36")
            else:
                print("\n-> Jumlah siswa 37")
            tak_hadir = prompt("> Jumlah siswa tidak hadir\t: ").strip()
            
        
        hadir_total = 36 if kelas == "tkj1" else 37
        hadir_siswa = hadir_total - int(tak_hadir)
        hadir_total = 36 if kelas == "tkj1" else 37

            # update data_harian
        for d in data_harian:
            if d["jam"] == js:
                d["guru"] = guru
                d["materi"] = materi
                d["hadir"] = hadir_total
                d["tidak_hadir"] = 0
                break

    info("\nSemua jam pelajaran sudah terisi.")
    kumpulkan = prompt("Kumpulkan data hari ini? (Y/N): ").lower()

    all_data = safe_read("data/journal_data.json", [])
    status = safe_read("data/status_pengumpulan.json", {"tkj1": False, "tkj2": False})

    if kumpulkan == "y":
        all_data.append({
            "kelas": kelas,
            "tanggal": tanggal,
            "hari": hari,
            "pelajaran": data_harian
        })
        write_json("data/journal_data.json", all_data)
        status[kelas] = True
        write_json("data/status_pengumpulan.json", status)
        info(f"\nData {kelas.upper()} berhasil dikumpulkan.")
    else:
        warn("Data disimpan sementara tanpa pengumpulan.")

    info("\nStatus Pengumpulan Saat Ini:")
    for k, v in status.items():
        print(f"  - {k.upper()} : {'Sudah' if v else 'Belum'}")

if __name__ == "__main__":
    main()