import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.file_utils import safe_read, write_json
from utils.datetime_utils import get_today

def header(text):
    print("","=" * 40)
    print(text.center(40))
    print("=" * 40)

def prompt(msg):
    return input(msg)

def warn(msg):
    print(f"[PERINGATAN] {msg}")

def info(msg):
    print(msg)

import os

def reset_status_if_new_day():
    status = safe_read("data/status_pengumpulan.json", {"tkj1": False, "tkj2": False})
    for k in status:
        status[k] = False
    write_json("data/status_pengumpulan.json", status)

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    header("E-JOURNAL CLI 2.0")

    kelas = prompt("Masukkan kelas (tkj1/tkj2): ").lower()
    if kelas not in ["tkj1", "tkj2"]:
        warn("Kelas tidak valid.")
        return

    # Reset status tiap hari baru
    reset_status_if_new_day()

    hari, tanggal, waktu = get_today()
    info(f"\nHari: {hari.capitalize()} | Tanggal: {tanggal} | Waktu: {waktu}\n")

    jadwal = safe_read("data/jadwal.json", {})
    if kelas not in jadwal or hari not in jadwal[kelas]:
        warn("Tidak ada jadwal untuk hari ini.")
        return

    pelajaran = jadwal[kelas][hari]
    data_harian = []

    for i, mapel in enumerate(pelajaran, start=1):
        header(f"Jam Pelajaran {i} - {mapel}")
        guru = prompt("Nama guru pengajar: ")
        materi = prompt("Materi pelajaran: ")
        tak_hadir = prompt("Jumlah siswa tidak hadir: ")

        hadir_total = 36 if kelas == "tkj1" else 37
        hadir_siswa = hadir_total - int(tak_hadir or 0)

        tanda_guru = prompt("Guru hadir? (y/n): ").lower()
        if tanda_guru == "n":
            warn("1. Isi keterangan guru tidak masuk")
            warn("2. Ulangi input")
            opsi = prompt("Pilih (1/2): ")
            if opsi == "1":
                materi = "Guru tidak hadir"
            elif opsi == "2":
                continue

        data_harian.append({
            "jam": i,
            "mapel": mapel,
            "guru": guru,
            "materi": materi,
            "hadir": hadir_siswa,
            "tidak_hadir": int(tak_hadir or 0),
            "tanda_tangan": tanda_guru == "y"
        })

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