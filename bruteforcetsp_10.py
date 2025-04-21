import streamlit as st
import datetime
import time
import matplotlib.pyplot as plt

# ----------------------------
# Sidebar Navigation
# ----------------------------
st.sidebar.title("📚 Navigasi")
page = st.sidebar.radio("Pilih Halaman:", ["Beranda", "Study Case II", "Study Case III", "Study Case IV", "Study Case V"])

# ----------------------------
# Halaman: Beranda
# ----------------------------
if page == "Beranda":
    st.title("👥 Kelompok 10 - Brute Force App")
    st.markdown("""
    Selamat datang di aplikasi Kelompok 10!  
    Aplikasi ini berisi beberapa studi kasus yang menjelaskan konsep algoritma *Brute Force*.

    **Daftar Halaman:**
    - 🏠 **Beranda**: Halaman informasi umum.
    - 📘 **Study Case II**: (Konten disesuaikan)
    - 📙 **Study Case III**: (Konten disesuaikan)
    - 📗 **Study Case IV**: Menebak tanggal lahir menggunakan brute force.
    - 📕 **Study Case V**: Brute force tanggal lahir + waktu proses dan grafik.
    """)

# ----------------------------
# Halaman: Study Case II
# ----------------------------
elif page == "Study Case II":
    st.title("📘 Study Case II")
    st.markdown("**(Silakan tambahkan isi dari Study Case II di sini)**")

# ----------------------------
# Halaman: Study Case III
# ----------------------------
elif page == "Study Case III":
    st.title("📙 Study Case III")
    st.markdown("**(Silakan tambahkan isi dari Study Case III di sini)**")

# ----------------------------
# Halaman: Study Case IV
# ----------------------------
elif page == "Study Case IV":
    st.title("🎯 Study Case IV - Brute Force Menebak Tanggal Lahir")

    def input_target_date():
        date_input = st.text_input("Masukkan tanggal lahir yang benar (DD-MM-YYYY):")
        if date_input:
            try:
                return datetime.datetime.strptime(date_input, "%d-%m-%Y").date()
            except ValueError:
                st.error("Format tanggal salah. Harap gunakan format DD-MM-YYYY.")
        return None

    def brute_force_birthday(target_date):
        start_year = 1990
        end_year = 2005
        attempts = 0
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

    target_date = input_target_date()
    if target_date:
        with st.spinner("🔄 Menjalankan brute force..."):
            guess, attempts = brute_force_birthday(target_date)
            if guess:
                st.success(f"🎯 Tanggal lahir ditemukan: {guess.strftime('%d-%m-%Y')}")
                st.write(f"🔁 Jumlah percobaan: {attempts}")
            else:
                st.error("❌ Tanggal lahir tidak ditemukan.")

# ----------------------------
# Halaman: Study Case V
# ----------------------------
elif page == "Study Case V":
    st.title("📕 Study Case V - Brute Force dengan Visualisasi")

    input_date_str = st.text_input("Masukkan tanggal lahir (format: DD-MM-YYYY):", "")
    if input_date_str:
        try:
            target_date = datetime.datetime.strptime(input_date_str, "%d-%m-%Y").date()

            start_year = 1990
            end_year = target_date.year
            attempts = 0
            guess_dates = []
            found = False

            start_time = time.time()

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

            # Visualisasi Grafik
            x = [i[0] for i in guess_dates]
            y = [i[1].toordinal() for i in guess_dates]

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(x, y, label="Tanggal Tebakan", color='green')
            ax.axhline(target_date.toordinal(), color='red', linestyle='--', label="Tanggal Sebenarnya")
            ax.set_xlabel("Jumlah Percobaan")
            ax.set_ylabel("Ordinal Tanggal")
            ax.set_title("Grafik Proses Brute Force")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)

        except ValueError:
            st.error("Format tanggal salah. Harap gunakan DD-MM-YYYY.")
