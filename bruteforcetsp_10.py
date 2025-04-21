import datetime
import time
import matplotlib.pyplot as plt
import streamlit as st

# Fungsi untuk memeriksa apakah tahun kabisat
def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

# Judul aplikasi
st.title("Pencarian Brute Force Tanggal Lahir")

# Input dari pengguna
input_date_str = st.text_input("Masukkan tanggal lahir (format: DD-MM-YYYY): ")
if input_date_str:
    try:
        target_date = datetime.datetime.strptime(input_date_str, "%d-%m-%Y").date()

        # Rentang tahun tebakan
        start_year = 1990
        end_year = target_date.year

        attempts = 0
        found = False
        start_time = time.time()  # Mulai hitung waktu

        guess_dates = []

        # Daftar jumlah hari di tiap bulan
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        for year in range(start_year, end_year + 1):
            for month in range(1, 13):
                # Perbaiki jumlah hari pada bulan Februari jika tahun kabisat
                if month == 2 and is_leap_year(year):
                    max_days = 29
                else:
                    max_days = days_in_month[month - 1]

                for day in range(1, max_days + 1):
                    try:
                        # Coba membuat objek tanggal
                        guess = datetime.date(year, month, day)
                        attempts += 1
                        guess_dates.append((attempts, guess))

                        # Jika tanggal cocok dengan target
                        if guess == target_date:
                            end_time = time.time()
                            st.subheader(f"🎯 Tanggal ditemukan: {guess.strftime('%d-%m-%Y')}")
                            st.write(f"🔁 Jumlah percobaan: {attempts}")
                            st.write(f"🕒 Total waktu pencarian: {end_time - start_time:.4f} detik")
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

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(x, y, label="Tanggal Tebakan", color='green')
            ax.axhline(target_date.toordinal(), color='red', linestyle='--', label="Tanggal Sebenarnya")
            ax.set_xlabel("Jumlah Percobaan")
            ax.set_ylabel("Ordinal Tanggal")
            ax.set_title("Grafik Waktu Pencarian Brute Force")
            ax.legend()
            ax.grid(True)

            # Menampilkan grafik pada Streamlit
            st.pyplot(fig)
        else:
            st.write("Tanggal tidak ditemukan dalam rentang yang ditentukan.")

    except ValueError:
        st.write("Format tanggal tidak valid. Harap masukkan tanggal dalam format DD-MM-YYYY.")
