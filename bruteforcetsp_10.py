import streamlit as st
import datetime
import time
import matplotlib.pyplot as plt

# Judul halaman Streamlit
st.set_page_config(page_title="Pencarian Brute Force Tanggal Lahir", layout="wide")

# Sidebar Navbar
st.sidebar.title("Menu")
menu = st.sidebar.radio("Pilih menu", ("Pencarian Tanggal Lahir", "Tentang"))

# Fungsi untuk pencarian brute force
def brute_force_search(target_date):
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
                        st.write(f"🎯 Tanggal ditemukan: {guess.strftime('%d-%m-%Y')}")
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

    return guess_dates, target_date, attempts, start_time

# Menampilkan konten berdasarkan menu
if menu == "Pencarian Tanggal Lahir":
    # Input tanggal lahir dari pengguna
    input_date_str = st.text_input("Masukkan tanggal lahir (format: DD-MM-YYYY):", "")
    
    if input_date_str:
        try:
            # Parse tanggal
            target_date = datetime.datetime.strptime(input_date_str, "%d-%m-%Y").date()

            # Melakukan pencarian brute force
            guess_dates, target_date, attempts, start_time = brute_force_search(target_date)

            # Visualisasi (tanpa emoji di judul)
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

            # Menampilkan grafik
            st.pyplot(plt)

        except ValueError:
            st.error("Format tanggal tidak valid. Pastikan format yang dimasukkan adalah DD-MM-YYYY.")
    
elif menu == "Tentang":
    # Halaman tentang
    st.title("Tentang Aplikasi")
    st.write(
        """
        Aplikasi ini adalah implementasi pencarian brute force untuk menemukan tanggal lahir
        yang dimasukkan oleh pengguna. Pengguna dapat memasukkan tanggal lahir mereka dalam
        format DD-MM-YYYY, dan aplikasi akan mencoba setiap tanggal dari tahun 1990 hingga
        tahun yang sesuai untuk menemukan tanggal yang dimaksud.
        
        Aplikasi ini juga mencatat waktu yang dibutuhkan untuk menemukan tanggal yang dicari
        dan memvisualisasikan hasil pencarian dalam bentuk grafik.
        """
    )

