import streamlit as st
import pandas as pd
import math
import itertools
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# -----------------------------
# Fungsi Haversine untuk perhitungan jarak
# -----------------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # radius bumi dalam km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

# -----------------------------
# Streamlit Setup
# -----------------------------
st.set_page_config(page_title="Rute Wisata Optimal", layout="wide")
st.title("📍 Optimasi Rute Tempat Wisata - Brute Force TSP")

# Sidebar navigasi
st.sidebar.title("Navigasi")
page = st.sidebar.radio("Pilih Halaman", ["Beranda", "Peta Rute", "Hasil Optimal", "Tentang"])

# -----------------------------
# Halaman Beranda
# -----------------------------
if page == "Beranda":
    st.title("Selamat datang di aplikasi perencanaan rute wisata!")
    st.markdown("""
    Aplikasi ini menggunakan algoritma Brute Force untuk menentukan rute terpendek dari daftar lokasi wisata yang Anda masukkan.
    """)
    st.image("img/banner.jpg")  # Pastikan gambar ada di path yang benar

# -----------------------------
# Halaman Peta Rute
# -----------------------------
elif page == "Peta Rute":
    st.title("🗺 Visualisasi Peta Rute")
    # Menampilkan peta rute wisata
    uploaded_file = st.file_uploader("Unggah file CSV tempat wisata:", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if 'Nama Tempat Wisata' not in df.columns or 'Latitude' not in df.columns or 'Longitude' not in df.columns:
            st.error("❌ Kolom wajib: 'Nama Tempat Wisata', 'Latitude', dan 'Longitude' tidak ditemukan.")
        else:
            locations = df[['Nama Tempat Wisata', 'Latitude', 'Longitude']].dropna().reset_index(drop=True)
            map_center = [locations['Latitude'].mean(), locations['Longitude'].mean()]
            m = folium.Map(location=map_center, zoom_start=12)

            # Menambahkan marker
            marker_cluster = MarkerCluster().add_to(m)
            for _, row in locations.iterrows():
                folium.Marker(
                    location=[row['Latitude'], row['Longitude']],
                    popup=row['Nama Tempat Wisata']
                ).add_to(marker_cluster)

            st_folium(m, width=900, height=600)

# -----------------------------
# Halaman Hasil Optimal
# -----------------------------
elif page == "Hasil Optimal":
    st.title("📊 Hasil Perhitungan Rute Optimal")
    # Proses perhitungan rute terbaik dengan brute force
    uploaded_file = st.file_uploader("Unggah file CSV tempat wisata:", type="csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if 'Nama Tempat Wisata' not in df.columns or 'Latitude' not in df.columns or 'Longitude' not in df.columns:
            st.error("❌ Kolom wajib: 'Nama Tempat Wisata', 'Latitude', dan 'Longitude' tidak ditemukan.")
        else:
            locations = df[['Nama Tempat Wisata', 'Latitude', 'Longitude']].dropna().reset_index(drop=True)
            n = len(locations)

            # Matriks jarak antar lokasi
            distance_matrix = [[0]*n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    if i != j:
                        distance_matrix[i][j] = haversine(
                            locations.loc[i, 'Latitude'], locations.loc[i, 'Longitude'],
                            locations.loc[j, 'Latitude'], locations.loc[j, 'Longitude']
                        )

            # Brute force untuk mencari rute optimal
            all_routes = []
            for perm in itertools.permutations(range(1, n)):
                route = [0] + list(perm) + [0]
                dist = sum(distance_matrix[route[i]][route[i+1]] for i in range(n))
                all_routes.append((route, dist))

            # Urutkan rute berdasarkan jarak
            all_routes.sort(key=lambda x: x[1])

            # Pilihan jumlah rute terbaik untuk ditampilkan
            jumlah_rute = st.slider("Pilih jumlah rute terbaik yang ingin ditampilkan:", 1, min(10, len(all_routes)), 3)

            st.subheader(f"🔁 {jumlah_rute} Rute Terbaik:")
            rute_terbaik = []
            for idx in range(min(jumlah_rute, len(all_routes))):
                route, total_jarak = all_routes[idx]
                nama_rute = " -> ".join([locations.loc[i, 'Nama Tempat Wisata'] for i in route])
                rute_terbaik.append({'Rute #': idx + 1, 'Total Jarak (km)': round(total_jarak, 2), 'Rute': nama_rute})

            rute_df = pd.DataFrame(rute_terbaik)
            st.dataframe(rute_df)

            # Simpan hasil sebagai CSV
            csv = rute_df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Unduh Hasil Rute", data=csv, file_name='rute_terbaik.csv', mime='text/csv')

# -----------------------------
# Halaman Tentang
# -----------------------------
elif page == "Tentang":
    st.title("ℹ Tentang Aplikasi")
    st.markdown("""
    Aplikasi ini dibuat menggunakan Python dan Streamlit, dengan implementasi algoritma Brute Force untuk menyelesaikan masalah Traveling Salesman Problem (TSP).
    
    Dibuat oleh: [Namamu]  
    Tahun: 2025
    """)
