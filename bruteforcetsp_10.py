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
# Sidebar - Study Kasus Brute Force
# -----------------------------
st.sidebar.title("🔐 Studi Kasus Brute Force")

# Study Kasus II
if st.sidebar.checkbox("Study Kasus II: Tebak Password 6 Digit"):

    def login(username, password):
        return username == "percobaan" and password == "091102"

    st.sidebar.markdown("**Menebak password 6 digit angka:**")
    hasil = None
    attempts = 0

    for i in range(1000000):
        guess = str(i).zfill(6)
        attempts += 1
        if login("percobaan", guess):
            hasil = (guess, attempts)
            break

    if hasil:
        st.sidebar.success(f"Password ditemukan: `{hasil[0]}` dalam {hasil[1]} percobaan")

# Study Kasus III
if st.sidebar.checkbox("Study Kasus III: Multi-Akun"):

    accounts = {
        "Iqbal": "091102",
        "Naufal": "090205",
        "usertest": "112233",
    }

    def login(username, password):
        return accounts.get(username) == password

    st.sidebar.markdown("**Brute force ke banyak username**")
    total_attempts = 0
    result_text = ""

    for user in accounts:
        found = False
        for i in range(1000000):
            guess = str(i).zfill(6)
            total_attempts += 1
            if login(user, guess):
                result_text += f"✅ `{user}` ditemukan password: `{guess}` setelah {i+1} percobaan\n"
                found = True
                break
        if not found:
            result_text += f"❌ `{user}` tidak ditemukan\n"

    st.sidebar.text_area("Hasil Brute Force:", result_text, height=200)

# Study Kasus IV
if st.sidebar.checkbox("Study Kasus IV: Tebak Tanggal Lahir Tetap"):

    target_date = datetime.date(2005, 2, 9)
    attempts = 0
    found = False

    for year in range(1990, 2006):
        for month in range(1, 13):
            for day in range(1, 32):
                try:
                    guess = datetime.date(year, month, day)
                    attempts += 1
                    if guess == target_date:
                        st.sidebar.success(f"Tanggal ditemukan: {guess.strftime('%d-%m-%Y')} dalam {attempts} percobaan.")
                        found = True
                        break
                except ValueError:
                    continue
            if found:
                break
        if found:
            break

# Study Kasus V
if st.sidebar.checkbox("Study Kasus V: Tebak Tanggal Lahir Dinamis + Grafik"):

    input_date_str = st.sidebar.text_input("Masukkan Tanggal (DD-MM-YYYY)", value="09-02-2005")

    if st.sidebar.button("Mulai Brute Force"):
        try:
            target_date = datetime.datetime.strptime(input_date_str, "%d-%m-%Y").date()
            start_year = 1990
            attempts = 0
            found = False
            guess_dates = []
            start_time = time.time()

            for year in range(start_year, target_date.year + 1):
                for month in range(1, 13):
                    for day in range(1, 32):
                        try:
                            guess = datetime.date(year, month, day)
                            attempts += 1
                            guess_dates.append((attempts, guess))

                            if guess == target_date:
                                found = True
                                break
                        except ValueError:
                            continue
                    if found:
                        break
                if found:
                    break

            elapsed = time.time() - start_time
            st.sidebar.success(f"Tanggal ditemukan: {target_date.strftime('%d-%m-%Y')} dalam {attempts} percobaan.")
            st.sidebar.info(f"Waktu pencarian: {elapsed:.2f} detik")

            # Grafik
            x = [i[0] for i in guess_dates]
            y = [i[1].toordinal() for i in guess_dates]
            fig, ax = plt.subplots(figsize=(5, 2))
            ax.plot(x, y, color='green', label='Tebakan')
            ax.axhline(target_date.toordinal(), color='red', linestyle='--', label='Target')
            ax.set_xlabel("Percobaan")
            ax.set_ylabel("Ordinal Tanggal")
            ax.legend()
            st.sidebar.pyplot(fig)

        except ValueError:
            st.sidebar.error("Format salah. Gunakan DD-MM-YYYY")

# -----------------------------
# Tampilan Halaman Utama - TSP
# -----------------------------
st.set_page_config(page_title="Rute Wisata Optimal", layout="wide")
st.title("📍 Optimasi Rute Tempat Wisata - Brute Force TSP")

uploaded_file = st.file_uploader("Unggah file CSV tempat wisata:", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    if 'Nama Tempat Wisata' not in df.columns or 'Latitude' not in df.columns or 'Longitude' not in df.columns:
        st.error("❌ Kolom wajib: 'Nama Tempat Wisata', 'Latitude', dan 'Longitude' tidak ditemukan.")
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

        st.subheader(f"🔁 {jumlah_rute} Rute Terbaik:")
        rute_terbaik = []
        for idx in range(jumlah_rute):
            route, total_jarak = all_routes[idx]
            nama_rute = " -> ".join([locations.loc[i, 'Nama Tempat Wisata'] for i in route])
            rute_terbaik.append({'Rute #': idx + 1, 'Total Jarak (km)': round(total_jarak, 2), 'Rute': nama_rute})

        rute_df = pd.DataFrame(rute_terbaik)
        st.dataframe(rute_df)

        csv = rute_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Unduh Hasil Rute", data=csv, file_name='rute_terbaik.csv', mime='text/csv')

        st.subheader("🗺 Visualisasi Peta Interaktif")
        map_center = [locations['Latitude'].mean(), locations['Longitude'].mean()]
        m = folium.Map(location=map_center, zoom_start=12)
        marker_cluster = MarkerCluster().add_to(m)
        for _, row in locations.iterrows():
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                popup=row['Nama Tempat Wisata']
            ).add_to(marker_cluster)

        best_route = all_routes[0][0]
        route_coords = [[locations.loc[i, 'Latitude'], locations.loc[i, 'Longitude']] for i in best_route]
        folium.PolyLine(route_coords, color='red', weight=5, opacity=0.8).add_to(m)
        st_folium(m, width=900, height=600)
