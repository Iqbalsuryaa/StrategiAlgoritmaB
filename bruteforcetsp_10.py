import datetime
import time
import matplotlib.pyplot as plt

# Input dari pengguna
input_date_str = input("Masukkan tanggal lahir (format: DD-MM-YYYY): ")
target_date = datetime.datetime.strptime(input_date_str, "%d-%m-%Y").date()

# Rentang tahun tebakan
start_year = 1990
end_year = target_date.year

attempts = 0
found = False
start_time = time.time()  # Mulai hitung waktu

guess_dates = []

for year in range(start_year, end_year + 1):
    for month in range(1, 13):
        for day in range(1, 32):
            try:
                # Coba membuat objek tanggal
                guess = datetime.date(year, month, day)
                attempts += 1
                guess_dates.append((attempts, guess))

                # Jika tanggal cocok dengan target
                if guess == target_date:
                    end_time = time.time()
                    print(f"\n🎯 Tanggal ditemukan: {guess.strftime('%d-%m-%Y')}")
                    print(f"🔁 Jumlah percobaan: {attempts}")
                    print(f"🕒 Total waktu pencarian: {end_time - start_time:.4f} detik")
                    found = True
                    break
            except ValueError:
                # Melewatkan tanggal yang tidak valid, seperti 30 Februari
                continue
        if found:
            break
    if found:
        break

# Jika tanggal ditemukan, lanjutkan visualisasi
if found:
    # Visualisasi grafik
    x = [i[0] for i in guess_dates]
    y = [i[1].toordinal() for i in guess_dates]  # Menggunakan ordinal untuk representasi tanggal

    plt.figure(figsize=(10, 5))
    plt.plot(x, y, label="Tanggal Tebakan", color='green')
    plt.axhline(target_date.toordinal(), color='red', linestyle='--', label="Tanggal Sebenarnya")
    plt.xlabel("Jumlah Percobaan")
    plt.ylabel("Ordinal Tanggal")
    plt.title("Grafik Waktu Pencarian Brute Force")
    plt.legend()
    plt.tight_layout()
    plt.grid(True)
    plt.show()
else:
    print("Tanggal tidak ditemukan dalam rentang yang ditentukan.")
