import streamlit as st

# Fungsi login sederhana
def login(username, password, correct_username, correct_password):
    return username == correct_username and password == correct_password

# Fungsi brute force login
def brute_force_login(correct_username, correct_password):
    attempts = 0

    for i in range(1000000):  # dari 000000 hingga 999999
        guess_password = str(i).zfill(6)  # Mengubah ke format 6 digit, contoh: 000007
        attempts += 1

        if login(correct_username, guess_password, correct_username, correct_password):
            return guess_password, attempts

        if i % 500 == 0:
            pass  # Bisa menambahkan log untuk setiap 500 percobaan

    return None, attempts  # Jika password tidak ditemukan dalam rentang tersebut

# -----------------------------
# Sidebar Navbar
# -----------------------------
st.sidebar.title("Menu")
page = st.sidebar.radio("Pilih Halaman", ["Beranda", "Study Kasus II", "Study Kasus III"])

# -----------------------------
# Halaman Study Kasus II
# -----------------------------
if page == "Study Kasus II":
    st.title("🔓 Simulasi Brute Force Login")

    # Input username dan password yang benar
    correct_username_input = st.text_input("Masukkan Username yang Benar", "")
    correct_password_input = st.text_input("Masukkan Password yang Benar", "", type="password")

    # Input username dan password untuk login
    username_input = st.text_input("Username untuk Login", "")
    password_input = st.text_input("Password untuk Login", "", type="password")

    # Tombol untuk cek login
    if st.button("Cek Login"):
        if login(username_input, password_input, correct_username_input, correct_password_input):
            st.success("✅ Login berhasil!")
        else:
            st.error("❌ Username atau password salah!")

    # Simulasi brute force
    st.subheader("Simulasi Serangan Brute Force terhadap Password 6 Digit")

    if st.button("Mulai Brute Force"):
        if correct_username_input == "" or correct_password_input == "":
            st.error("❌ Silakan masukkan username dan password terlebih dahulu.")
        else:
            with st.spinner("🔄 Menjalankan serangan brute force..."):
                correct_password_found, attempts = brute_force_login(correct_username_input, correct_password_input)
                if correct_password_found:
                    st.success(f"✅ Password ditemukan: {correct_password_found}")
                    st.write(f"🔁 Jumlah percobaan: {attempts}")
                else:
                    st.error("❌ Password tidak ditemukan dalam rentang 000000-999999.")
