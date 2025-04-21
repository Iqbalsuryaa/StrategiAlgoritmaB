import streamlit as st
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
        for i in range(1000000):  # Coba 6 digit angka dari 000000 sampai 999999
            guess = str(i).zfill(6)
            total_attempts += 1

            if login(username, guess, accounts):
                result["password"] = guess
                result["attempts"] = i + 1
                result["found"] = True
                results.append(result)
                break

            if i % 50000 == 0:
                pass  # Menyembunyikan log percobaan untuk efisiensi

        if not result["found"]:
            result["password"] = "Tidak ditemukan"
            result["attempts"] = 1000000
            results.append(result)

    end_time = time()
    return results, total_attempts, end_time - start_time

# -----------------------------
# Sidebar Navbar
# -----------------------------
st.sidebar.title("Menu")
page = st.sidebar.radio("Pilih Halaman", ["Beranda", "Study Kasus II", "Study Kasus III"])

# -----------------------------
# Halaman Study Kasus III
# -----------------------------
if page == "Study Kasus III":
    st.title("🔓 Simulasi Brute Force pada Sistem Login")

    # Input untuk mengisi daftar akun
    st.subheader("Masukkan Daftar Akun:")
    
    # Menggunakan session state untuk menyimpan akun
    if 'accounts' not in st.session_state:
        st.session_state.accounts = {}

    # Form untuk menambah akun
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

    # Menampilkan daftar akun yang telah ditambahkan
    st.subheader("Daftar Akun yang Tersedia:")
    if st.session_state.accounts:
        for user in st.session_state.accounts:
            st.write(f"- {user}")
    else:
        st.write("Belum ada akun yang ditambahkan.")

    # Input untuk memilih akun yang ingin dites login
    if st.session_state.accounts:
        selected_user = st.selectbox("Pilih Username untuk Tes Brute Force", list(st.session_state.accounts.keys()))

        # Tombol untuk mulai brute force
        if st.button("Mulai Brute Force"):
            with st.spinner("🔄 Menjalankan serangan brute force..."):
                results, total_attempts, elapsed_time = brute_force_multi_user(st.session_state.accounts)

                # Menampilkan hasil
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
