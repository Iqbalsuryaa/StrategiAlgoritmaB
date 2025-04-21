import datetime

# Fungsi untuk meminta input tanggal lahir dari pengguna
def input_target_date():
    # Meminta input untuk tanggal lahir (DD-MM-YYYY)
    date_input = st.text_input("Masukkan tanggal lahir yang benar (DD-MM-YYYY):")
    
    if date_input:
        try:
            # Mengonversi input menjadi tipe datetime
            target_date = datetime.datetime.strptime(date_input, "%d-%m-%Y").date()
            return target_date
        except ValueError:
            st.error("Format tanggal salah. Harap gunakan format DD-MM-YYYY.")
            return None
    return None

# Fungsi brute force untuk menebak tanggal lahir
def brute_force_birthday(target_date):
    start_year = 1990
    end_year = 2005

    attempts = 0
    found = False  # Flag untuk menghentikan semua loop

    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            for day in range(1, 32):
                try:
                    guess = datetime.date(year, month, day)
                    attempts += 1
                    if guess == target_date:
                        return guess, attempts
                except ValueError:
                    continue
    return None, attempts

# -----------------------------
# Streamlit Interface
# -----------------------------
import streamlit as st

st.title("🎯 Brute Force Menebak Tanggal Lahir")

# Meminta input untuk tanggal lahir yang benar
target_date = input_target_date()

# Jika tanggal lahir dimasukkan, jalankan brute force
if target_date:
    with st.spinner("🔄 Menjalankan serangan brute force..."):
        guess, attempts = brute_force_birthday(target_date)
        if guess:
            st.success(f"🎯 Tanggal lahir ditemukan: {guess.strftime('%d-%m-%Y')}")
            st.write(f"🔁 Jumlah percobaan: {attempts}")
        else:
            st.error("❌ Tanggal lahir tidak ditemukan.")
