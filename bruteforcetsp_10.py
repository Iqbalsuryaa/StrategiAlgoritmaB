import streamlit as st
import datetime
import time
import matplotlib.pyplot as plt

# Title and Description
st.title("Pencarian Brute Force Tanggal Lahir")
st.markdown("""
Implementasi pencarian brute force untuk menemukan tanggal lahir yang dimasukkan pengguna.
Melakukan pencatatan waktu dan memvisualisasikan grafik dari proses pencarian tanggal yang dicoba.
""")

# Input dari pengguna
input_date_str = st.text_input("Masukkan tanggal lahir (format: DD-MM-YYYY):", "")
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

        for year in range(start_year, end_year + 1):
            for month in range(1, 13):
                for day in range(1, 32):
                    try:
                        guess = datetime.date(year, month, day)
                        attempts += 1
                        guess_dates.append((attempts, guess))

                        if guess == target_date:
                            end_time = time.time()
                            st.success(f"🎯 Tanggal ditemukan: {guess.strftime('%d-%m-%Y')}")
                            st.write(f"🔁 Jumlah percobaan: {attempts}")
                            st.write(f"🕒 Total waktu pencarian: {end_time - start_time:.4f} detik")
                            found = True
                            break
                    except ValueError:
                        continue
                if found:
                    break
            if found:
                break

        if not found:
            st.warning("Tanggal tidak ditemukan dalam rentang tahun yang diberikan.")

        # Visualisasi
        x = [i[0] for i in guess_dates]
        y = [i[1].toordinal() for i in guess_dates]  # ordinal untuk menggambarkan tanggal

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(x, y, label="Tanggal Tebakan", color='green')
        ax.axhline(target_date.toordinal(), color='red', linestyle='--', label="Tanggal Sebenarnya")
        ax.set_xlabel("Jumlah Percobaan")
        ax.set_ylabel("Ordinal Tanggal")
        ax.set_title("Grafik Waktu Pencarian Brute Force")
        ax.legend()
        ax.grid(True)
        st.pyplot(fig)

    except ValueError:
        st.error("Format tanggal salah. Harap masukkan tanggal dalam format DD-MM-YYYY.")
