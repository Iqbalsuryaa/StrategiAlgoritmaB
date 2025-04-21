import datetime
import time
import matplotlib.pyplot as plt
import streamlit as st

# Judul aplikasi
st.title('Brute Force Date Searcher')

# Input dari pengguna: Tanggal lahir
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
        
        if found:
            # Visualisasi grafik
            x = [i[0] for i in guess_dates]
            y = [i[1].toordinal() for i in guess_dates]  # ordinal untuk menggambarkan tanggal
            
            plt.figure(figsize=(10, 5))
            plt.plot(x, y, label="Tanggal Tebakan", color='green')
            plt.axhline(target_date.toordinal(), color='red', linestyle='--', label="Tanggal Sebenarnya")
            plt.xlabel("Jumlah Percobaan")
            plt.ylabel("Ordinal Tanggal")
            plt.title("Grafik Waktu Pencarian Brute Force")
            plt.legend()
            plt.tight_layout()
            plt.grid(True)
            st.pyplot(plt)
        else:
            st.warning("Tanggal tidak ditemukan dalam rentang yang ditentukan.")
    except ValueError:
        st.error("Format tanggal tidak valid. Harap masukkan tanggal dengan format DD-MM-YYYY.")
