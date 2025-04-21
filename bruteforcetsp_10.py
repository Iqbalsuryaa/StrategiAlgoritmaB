# streamlit_app.py

import streamlit as st
import pandas as pd
import math
import itertools
import datetime
import time
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# -----------------------------
# Fungsi Haversine (Study Case I)
# -----------------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

# -----------------------------
# Fungsi Login & Brute Force (Study Case III)
# -----------------------------
def login(username, password, accounts):
    return accounts.get(username) == password

def brute_force_multi_user(accounts):
    start_time = time.time()
    total_attempts = 0
    results = []

    for username in accounts.keys():
        result = {"username": username, "found": False, "password": None, "attempts": 0}
        for i in range(1000000):  # 6-digit password
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
    end_time = time.time()
    return results, total_attempts, end_time - start_time

# -----------------------------
# Fungsi Brute Force Tanggal Lahir (Study Case IV & V)
# -----------------------------
def input_target_date():
    date_input = st.text_input("Masukkan tanggal lahir (DD-MM-YYYY):")
    if date_input:
        try:
            return datetime.datetime.strptime(date_input, "%d-%m-%Y").date()
        except ValueError:
            st.error("Format tanggal salah. Harap gunakan format DD-MM-YYYY.")
    return None

def brute_force_birthday(target_date, record_attempts=False):
    start_year, end_year = 1990, 2005
    attempts = 0
    tries = []

    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            for day in range(1, 32):
                try:
                    guess = datetime.date(year, month, day)
                    attempts += 1
                    if record_attempts:
                        tries.append(guess)
                    if guess == target_date:
                        return guess, attempts, tries
                except ValueError:
                    continue
    return None, attempts, tries

# -----------------------------
# Sidebar Navigation
# -----------------------------
st.sidebar.title("📌 Menu Navigasi")
page = st.sidebar.radio("Pilih Study Case", [
    "Study Case I: Rute Wisata (TSP)",
    "Study Case III: Brute Force Login",
    "Study Case IV: Tebak Tanggal Lahir",
    "Study Case V: Grafik Pencarian Tanggal Lahir"
])

# -----------------------------
# Study Case I: TSP Rute Wisata
# -----------------------------
if page == "Study Case I: Rute Wisata (TSP)":
    st.title("📍 Optimasi Rute Tempat Wisata - Brute Force TSP")
    uploaded_file = st.file_uploader("Unggah file CSV tempat wisata:", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if 'Nama Tempat Wisata' not in df.columns or 'Latitude' not in df.columns or 'Longitude' not in df.columns:
            st.error("❌ Kolom wajib tidak ditemukan.")
        else:
            locations = df[['Nama Tempat Wisata', 'Latitude', 'Longitude']].dropna().reset_index(drop=True)
            n = len(locations)

            distance_matrix = [[0]*n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    if i != j:
                        distance_matrix[i][j] = haversine(
                            locations.loc[i, 'Latitude'], locations.loc[i, 'Longitude'],
                            locations.loc[j, 'Latitude'], locations.loc[j, 'Longitude']
                        )

            all_routes = []
            for perm in itertools.permutations(range(1, n)):
                route = [0] + list(perm) + [0]
                dist = sum(distance_matrix[route[i]][route[i+1]] for i in range(n))
                all_routes.append((route, dist))

            all_routes.sort(key=lambda x: x[1])
            jumlah_rute = st.slider("Pilih jumlah rute terbaik:", 1, min(10, len(all_routes)), 3)

            rute_terbaik = []
            for idx in range(jumlah_rute):
                route, total_jarak = all_routes[idx]
                nama_rute = " -> ".join([locations.loc[i, 'Nama Tempat Wisata'] for i in route])
                rute_terbaik.append({'Rute #': idx + 1, 'Total Jarak (km)': round(total_jarak, 2), 'Rute': nama_rute})

            st.dataframe(pd.DataFrame(rute_terbaik))

            csv = pd.DataFrame(rute_terbaik).to_csv(index=False).encode('utf-8')
            st.download_button("📥 Unduh Hasil Rute", data=csv, file_name='rute_terbaik.csv', mime='text/csv')

            st.subheader("🗺 Visualisasi Peta Interaktif")
            map_center = [locations['Latitude'].mean(), locations['Longitude'].mean()]
            m = folium.Map(location=map_center, zoom_start=12)
            marker_cluster = MarkerCluster().add_to(m)
            for _, row in locations.iterrows():
                folium.Marker(location=[row['Latitude'], row['Longitude']], popup=row['Nama Tempat Wisata']).add_to(marker_cluster)

            best_route = all_routes[0][0]
            route_coords = [[locations.loc[i, 'Latitude'], locations.loc[i, 'Longitude']] for i in best_route]
            folium.PolyLine(route_coords, color='red', weight=5, opacity=0.8).add_to(m)
            st_folium(m, width=900, height=600)

# -----------------------------
# Study Case III: Brute Force Login
# -----------------------------
elif page == "Study Case III: Brute Force Login":
    st.title("🔓 Simulasi Brute Force pada Sistem Login")
    st.subheader("Masukkan Daftar Akun:")
    if 'accounts' not in st.session_state:
        st.session_state.accounts = {}

    with st.form("add_account_form", clear_on_submit=True):
        new_username = st.text_input("Username baru")
        new_password = st.text_input("Password baru", type="password")
        if st.form_submit_button("Tambah Akun"):
            if new_username and new_password:
                st.session_state.accounts[new_username] = new_password
                st.success(f"Akun {new_username} berhasil ditambahkan.")
            else:
                st.warning("Isi username dan password terlebih dahulu.")

    if st.session_state.accounts:
        selected_user = st.selectbox("Pilih Username untuk Tes Brute Force", list(st.session_state.accounts.keys()))
        if st.button("Mulai Brute Force"):
            with st.spinner("🔄 Menjalankan serangan brute force..."):
                results, total_attempts, elapsed_time = brute_force_multi_user(st.session_state.accounts)
                user_result = next((r for r in results if r["username"] == selected_user), None)
                if user_result and user_result["found"]:
                    st.success(f"Password ditemukan untuk {user_result['username']}: {user_result['password']}")
                    st.write(f"Jumlah percobaan: {user_result['attempts']}")
                else:
                    st.error(f"Password tidak ditemukan.")
                st.write(f"Total waktu: {elapsed_time:.2f} detik")

# -----------------------------
# Study Case IV: Tebak Tanggal Lahir
# -----------------------------
elif page == "Study Case IV: Tebak Tanggal Lahir":
    st.title("🎯 Brute Force Menebak Tanggal Lahir")
    target_date = input_target_date()
    if target_date:
        with st.spinner("🔄 Menjalankan brute force..."):
            guess, attempts, _ = brute_force_birthday(target_date)
            if guess:
                st.success(f"🎯 Tanggal ditemukan: {guess.strftime('%d-%m-%Y')}")
                st.write(f"Jumlah percobaan: {attempts}")
            else:
                st.error("❌ Tanggal tidak ditemukan.")

# -----------------------------
# Study Case V: Grafik Brute Force
# -----------------------------
elif page == "Study Case V: Grafik Pencarian Tanggal Lahir":
    st.title("📊 Visualisasi Pencarian Tanggal Lahir Brute Force")
    target_date = input_target_date()
    if target_date:
        with st.spinner("🔄 Menjalankan brute force dan mencatat proses..."):
            guess, attempts, tries = brute_force_birthday(target_date, record_attempts=True)
            if guess:
                st.success(f"Tanggal lahir ditemukan: {guess.strftime('%d-%m-%Y')}")
                st.write(f"Percobaan: {attempts}")

                dates = [d.strftime("%d-%m-%Y") for d in tries]
                plt.figure(figsize=(10, 4))
                plt.plot(range(len(dates)), list(range(len(dates))))
                plt.title("Visualisasi Jumlah Percobaan")
                plt.xlabel("Tanggal ke-n")
                plt.ylabel("Jumlah Percobaan")
                st.pyplot(plt)
            else:
                st.error("Tanggal tidak ditemukan.")
