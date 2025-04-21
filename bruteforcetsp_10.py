import streamlit as st
import datetime
import time
import matplotlib.pyplot as plt

# ------------------------------
# Halaman: Beranda
# ------------------------------
def beranda():
    st.title("📚 Kelompok 10 - Aplikasi Brute Force")
    st.markdown("""
    Selamat datang di aplikasi Brute Force Kelompok 10.

    Aplikasi ini menampilkan berbagai *studi kasus brute force* dari yang sederhana hingga dengan visualisasi.

    Silakan pilih halaman dari sidebar untuk mulai eksplorasi.
    """)

# ------------------------------
# Halaman: Study Case I
# ------------------------------
def study_case_I():
    st.title("🧩 Study Case I")
    st.info("⚠ Halaman belum diisi. Silakan tambahkan implementasi Study Case I.")

# ------------------------------
# Halaman: Study Case II
# ------------------------------
def study_case_II():
    st.title("🧩 Study Case II")
    st.info("⚠ Halaman belum diisi. Silakan tambahkan implementasi Study Case II.")

# ------------------------------
# Halaman: Study Case III
# ------------------------------
def study_case_III():
    st.title("🔓 Simulasi Brute Force pada Sistem Login")

    from time import time

    # Fungsi login (simulasi server)
    def login(username, password, accounts):
        return accounts.get(username) == password

    # Brute force terhadap banyak username
    def brute_force_multi_user(accounts):
        start_time = time()
        total_attempts = 0
        results = []

        for username in accounts.keys():
            result = {"username": username, "found": False, "password": None, "attempts": 0}
            for i in range(1000000):  # 6 digit dari 000000 sampai 999999
                guess = str(i).zfill(6)
                total_attempts += 1

                if login(username, guess, accounts):
                    result["password"] = guess
                    result["attempts"] = i + 1
                    result["found"] = True
                    results.append(result)
                    break

            if not result["found"]:
                result["password"] = "Tidak ditemukan"
                result["attempts"] = 1000000
                results.append(result)

        end_time = time()
        return results, total_attempts, end_time - start_time

    # Input akun
    st.subheader("Masukkan Daftar Akun:")
    if 'accounts' not in st.session_state:
        st.session_state.accounts = {}

    with st.form("add_account_form", clear_on_submit=True):
        new_username = st.text_input("Username baru")
        new_password = st.text_input("Password baru", type="password")
        add_account_button = st.form_submit_button("Tambah Akun")

        if add_account_button:
            if new_username and new_password:
                st.session_state.accounts[new_username] = new_password
                st.success(f"Akun {new_username} berhasil ditambahkan!")
            else:
                st.warning("Harap masukkan username dan password.")

    st.subheader("Daftar Akun yang Tersedia:")
    if st.session_state.accounts:
        for user in list(st.session_state.accounts.keys()):
            st.write(f"- {user}")
            delete_button = st.button(f"Hapus {user}", key=f"delete_{user}")
            if delete_button:
                del st.session_state.accounts[user]
                st.success(f"Akun {user} telah dihapus!")

    else:
        st.write("Belum ada akun yang ditambahkan.")

    if st.session_state.accounts:
        selected_user = st.selectbox("Pilih Username untuk Tes Brute Force", list(st.session_state.accounts.keys()))

        if st.button("Mulai Brute Force"):
            with st.spinner("🔄 Menjalankan serangan brute force..."):
                results, total_attempts, elapsed_time = brute_force_multi_user(st.session_state.accounts)

                st.subheader(f"🔑 Hasil Brute Force untuk Akun: {selected_user}")
                user_result = next((result for result in results if result["username"] == selected_user), None)
                if user_result:
                    if user_result["found"]:
                        st.success(f"✅ Password ditemukan untuk {user_result['username']}: {user_result['password']}")
                        st.write(f"🔁 Jumlah percobaan: {user_result['attempts']}")
                    else:
                        st.error(f"❌ Password untuk {user_result['username']} tidak ditemukan.")
                else:
                    st.error(f"❌ Tidak ada hasil ditemukan untuk {selected_user}.")

                st.write(f"🕒 Total waktu: {elapsed_time:.2f} detik")
                st.write(f"🔁 Total percobaan semua akun: {total_attempts}")

# ------------------------------
# Halaman: Study Case IV
# ------------------------------
def study_case_IV():
    st.title("🎯 Brute Force Menebak Tanggal Lahir (Case IV)")
    date_input = st.text_input("Masukkan tanggal lahir yang benar (DD-MM-YYYY):")
    if date_input:
        try:
            target_date = datetime.datetime.strptime(date_input, "%d-%m-%Y").date()
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
                                st.success(f"🎯 Tanggal ditemukan: {guess.strftime('%d-%m-%Y')}")
                                st.write(f"🔁 Jumlah percobaan: {attempts}")
                                return
                        except ValueError:
                            continue
            st.error("❌ Tanggal tidak ditemukan.")
        except ValueError:
            st.error("❌ Format tanggal salah. Gunakan format DD-MM-YYYY.")

# ------------------------------
# Halaman: Study Case V
# ------------------------------
def study_case_V():
    st.title("📈 Brute Force + Visualisasi (Case V)")
    input_date_str = st.text_input("Masukkan tanggal lahir (format: DD-MM-YYYY):", "")
    if input_date_str:
        try:
            target_date = datetime.datetime.strptime(input_date_str, "%d-%m-%Y").date()
            start_year = 1990
            end_year = target_date.year
            attempts = 0
            found = False
            start_time = time.time()
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
                                st.write(f"🕒 Total waktu: {end_time - start_time:.4f} detik")
                                found = True
                                break
                        except ValueError:
                            continue
                    if found:
                        break
                if found:
                    break

            if not found:
                st.warning("❌ Tanggal tidak ditemukan.")

            x = [i[0] for i in guess_dates]
            y = [i[1].toordinal() for i in guess_dates]
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(x, y, label="Tebakan Tanggal", color='green')
            ax.axhline(target_date.toordinal(), color='red', linestyle='--', label="Tanggal Asli")
            ax.set_xlabel("Percobaan ke-")
            ax.set_ylabel("Ordinal Tanggal")
            ax.set_title("Grafik Brute Force")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)
        except ValueError:
            st.error("Format tanggal salah. Gunakan format DD-MM-YYYY.")

# ------------------------------
# Sidebar Navigasi
# ------------------------------
st.sidebar.title("📌 Navigasi")
halaman = st.sidebar.selectbox(
    "Pilih Halaman",
    ("Beranda", "Study Case I", "Study Case II", "Study Case III", "Study Case IV", "Study Case V")
)

# ------------------------------
# Routing ke halaman dipilih
# ------------------------------
if halaman == "Beranda":
    beranda()
elif halaman == "Study Case I":
    study_case_I()
elif halaman == "Study Case II":
    study_case_II()
elif halaman == "Study Case III":
    study_case_III()
elif halaman == "Study Case IV":
    study_case_IV()
elif halaman == "Study Case V":
    study_case_V()
