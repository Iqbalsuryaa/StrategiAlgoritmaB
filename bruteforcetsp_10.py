import streamlit as st
import pandas as pd
import math
import itertools
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# Fungsi Haversine
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

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
# Halaman Beranda
# -----------------------------
if page == "Beranda":
    st.title("🌐 Selamat Datang di Halaman Utama")
    st.write("""
    Di sini Anda dapat menjelajahi berbagai kasus studi yang menggunakan simulasi serangan brute force, 
    optimasi rute tempat wisata, dan banyak lagi!
    """)

# -----------------------------
# Halaman Study Kasus II
# -----------------------------
elif page == "Study Kasus II":
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

# -----------------------------
# Halaman Study Kasus III: Rute Wisata Optimal
# -----------------------------
elif page == "Study Kasus III":
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
