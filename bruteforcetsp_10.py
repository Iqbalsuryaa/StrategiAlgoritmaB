import streamlit as st
import pandas as pd
import math
import itertools
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import datetime
import time
import matplotlib.pyplot as plt

# -----------------------------
# Fungsi Haversine
# -----------------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

# -----------------------------
# Sidebar Navbar
# -----------------------------
st.sidebar.title("Menu")
page = st.sidebar.radio("Pilih Halaman", ["Beranda", "Study Kasus II", "Study Kasus III", "Study Kasus IV", "Study Kasus V"])

# -----------------------------
# Halaman Beranda
# -----------------------------
if page == "Beranda":
    st.set_page_config(page_title="Rute Wisata Optimal", layout="wide")
    st.title("📍 Optimasi Rute Tempat Wisata - Brute Force TSP")

    # Upload CSV
    uploaded_file = st.file_uploader("Unggah file CSV tempat wisata:", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        if 'Nama Tempat Wisata' not in df.columns or 'Latitude' not in df.columns or 'Longitude' not in df.columns:
            st.error("❌ Kolom wajib: 'Nama Tempat Wisata', 'Latitude', dan 'Longitude' tidak ditemukan.")
        else:
            locations = df[['Nama Tempat Wisata', 'Latitude', 'Longitude']].dropna().reset_index(drop=True)
            n = len(locations)

            # Matriks Jarak
            distance_matrix = [[0]*n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    if i != j:
                        distance_matrix[i][j] = haversine(
                            locations.loc[i, 'Latitude'], locations.loc[i, 'Longitude'],
                            locations.loc[j, 'Latitude'], locations.loc[j, 'Longitude']
                        )

            # Brute Force TSP
            all_routes = []
            for perm in itertools.permutations(range(1, n)):
                route = [0] + list(perm) + [0]
                dist = sum(distance_matrix[route[i]][route[i+1]] for i in range(n))
                all_routes.append((route, dist))

            # Urutkan hasil
            all_routes.sort(key=lambda x: x[1])

            jumlah_rute = st.slider("Pilih jumlah rute terbaik yang ingin ditampilkan:", 1, min(10, len(all_routes)), 3)

            st.subheader(f"🔁 {jumlah_rute} Rute Terbaik:")
            rute_terbaik = []
            for idx in range(min(jumlah_rute, len(all_routes))):
                route, total_jarak = all_routes[idx]
                nama_rute = " -> ".join([locations.loc[i, 'Nama Tempat Wisata'] for i in route])
                rute_terbaik.append({'Rute #': idx + 1, 'Total Jarak (km)': round(total_jarak, 2), 'Rute': nama_rute})

            rute_df = pd.DataFrame(rute_terbaik)
            st.dataframe(rute_df)

            # Simpan sebagai CSV
            csv = rute_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Unduh Hasil Rute", data=csv, file_name='rute_terbaik.csv', mime='text/csv')

            # Peta Interaktif
            st.subheader("🗺 Visualisasi Peta Interaktif")
            map_center = [locations['Latitude'].mean(), locations['Longitude'].mean()]
            m = folium.Map(location=map_center, zoom_start=12)

            marker_cluster = MarkerCluster().add_to(m)
            for _, row in locations.iterrows():
                folium.Marker(
                    location=[row['Latitude'], row['Longitude']],
                    popup=row['Nama Tempat Wisata']
                ).add_to(marker_cluster)

            # Tampilkan rute terbaik pertama
            best_route = all_routes[0][0]
            route_coords = [[locations.loc[i, 'Latitude'], locations.loc[i, 'Longitude']] for i in best_route]
            folium.PolyLine(route_coords, color='red', weight=5, opacity=0.8).add_to(m)

            st_folium(m, width=900, height=600)

# -----------------------------
# Halaman Study Kasus II
# -----------------------------
elif page == "Study Kasus II":
    # Kode untuk Study Kasus II
    def login(username, password):
        correct_username = "percobaan"
        correct_password = "091102"
        return username == correct_username and password == correct_password

    def brute_force_login():
        target_username = "percobaan"
        attempts = 0

        for i in range(100000):  # dari 0000 sampai 9999
            guess_password = str(i).zfill(6)  # Mengubah ke format 4 digit, contoh: 0007
            attempts += 1

            if login(target_username, guess_password):
                st.write(f"✅ Password ditemukan: {guess_password}")
                st.write(f"🔁 Jumlah percobaan: {attempts}")
                return

            if i % 500 == 0:
                st.write(f"Masih mencoba... saat ini: {guess_password}")

        st.write("❌ Password tidak ditemukan dalam rentang 0000–9999.")

    brute_force_login()

# -----------------------------
# Halaman Study Kasus III
# -----------------------------
elif page == "Study Kasus III":
    # Kode untuk Study Kasus III
    accounts = {
        "Iqbal": "091102",
        "Naufal": "090205",
        "usertest": "112233",
    }

    def login(username, password):
        return accounts.get(username) == password

    def brute_force_multi_user():
        from time import time
        start_time = time()
        total_attempts = 0

        for username in accounts.keys():
            st.write(f"\n🚀 Mencoba username: {username}")
            found = False
            for i in range(1000000):  # Coba 6 digit angka dari 000000 sampai 999999
                guess = str(i).zfill(6)
                total_attempts += 1

                if login(username, guess):
                    st.write(f"✅ Username: {username} | Password ditemukan: {guess}")
                    st.write(f"🔁 Percobaan: {i+1}")
                    found = True
                    break

                if i % 50000 == 0:
                    st.write(f"⏳ Masih mencoba... {guess}")

            if not found:
                st.write(f"❌ Password untuk {username} tidak ditemukan (hanya angka 6 digit yang diuji)")

        end_time = time()
        st.write(f"\n🕒 Total waktu: {end_time - start_time:.2f} detik")
        st.write(f"🔁 Total percobaan semua akun: {total_attempts}")

    brute_force_multi_user()

# -----------------------------
# Halaman Study Kasus IV
# -----------------------------
elif page == "Study Kasus IV":
    # Kode untuk Study Kasus IV
    target_date = datetime.date(2005, 2, 9)
    start_year = 1990
    end_year = 2005
    attempts = 0
    found = False

    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            for day in range(1, 32):
                try:
                    guess = datetime.date(year, month, day)
                    attempts += 1
                    if guess == target_date:
                        st.write(f"🎯 Ditemukan: {guess.strftime('%d-%m-%Y')}")
                        st.write(f"🔁 Percobaan: {attempts}")
                        found = True
                        break
                except ValueError:
                    continue
            if found:
                break
        if found:
            break

# -----------------------------
# Halaman Study Kasus V
# -----------------------------
elif page == "Study Kasus V":
    # Kode untuk Study Kasus V
    input_date_str = st.text_input("Masukkan tanggal lahir (format: DD-MM-YYYY):")
    if input_date_str:
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
                            st.write(f"\n🎯 Tanggal ditemukan: {guess.strftime('%d-%m-%Y')}")
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

        # Visualisasi
        x = [i[0] for i in guess_dates]
        y = [i[1].toordinal() for i in guess_dates]

        plt.figure(figsize=(10, 5))
        plt.plot(x, y, label="Tanggal Tebakan", color='green')
        plt.axhline(target_date.toordinal(), color='red', linestyle='--', label="Tanggal Sebenarnya")
        plt.xlabel("Jumlah Percobaan")
        plt.ylabel("Tanggal (Ordinal)")
        plt.title("Grafik Percobaan Tanggal Lahir")
        plt.legend()
        st.pyplot()
