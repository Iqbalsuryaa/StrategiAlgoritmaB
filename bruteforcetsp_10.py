import streamlit as st

# Menambahkan dan menghapus akun dalam daftar
accounts = {}

# Fungsi untuk menambah akun
def add_account(username, password):
    if username in accounts:
        st.warning(f"🛑 Username {username} sudah ada!")
    else:
        accounts[username] = password
        st.success(f"✅ Akun {username} berhasil ditambahkan!")

# Fungsi untuk menghapus akun
def remove_account(username):
    if username in accounts:
        del accounts[username]
        st.success(f"✅ Akun {username} berhasil dihapus!")
    else:
        st.warning(f"🛑 Akun {username} tidak ditemukan!")

# Menampilkan akun yang tersedia
def show_accounts():
    if accounts:
        st.write("🔑 Daftar Akun yang Tersedia:")
        for username in accounts.keys():
            st.write(f"- {username}")
    else:
        st.write("❌ Belum ada akun yang tersedia.")

# Input untuk username dan password
username_input = st.text_input("Masukkan Username")
password_input = st.text_input("Masukkan Password", type="password")

# Menu untuk memilih aksi
action = st.selectbox("Pilih Aksi", ("Tambah Akun", "Hapus Akun", "Tampilkan Daftar Akun"))

# Berdasarkan pilihan aksi, eksekusi fungsi yang sesuai
if action == "Tambah Akun":
    if st.button("Tambah Akun"):
        add_account(username_input, password_input)
        st._rerun()  # Refresh halaman setelah penambahan akun

elif action == "Hapus Akun":
    if st.button("Hapus Akun"):
        remove_account(username_input)
        st._rerun()  # Refresh halaman setelah penghapusan akun

elif action == "Tampilkan Daftar Akun":
    show_accounts()

