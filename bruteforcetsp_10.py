import streamlit as st
import pandas as pd
import math
import itertools
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# -----------------------------
# Fungsi Haversine
# -----------------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius bumi dalam km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

# -----------------------------
# Tampilan Streamlit
# -----------------------------
st.set_page_config(page_title="Rute Wisata Optimal", layout="wide")
st.title("📍 Optimasi Rute Tempat Wisata - Brute Force TSP")

# Upload CSV
uploaded_file = st.file_uploader("📤 Unggah file CSV tempat wisata:", type="csv")

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)

        required_columns = {'Nama Tempat Wisata', 'Latitude', 'Longitude'}
        if not required_columns.issubset(df.columns):
            st.error("❌ Kolom wajib: 'Nama Tempat Wisata', 'Latitude', dan 'Longitude' tidak ditemukan.")
        else:
            locations = df[['Nama Tempat Wisata', 'Latitude', 'Longitude']].dropna().reset_index(drop=True)
            n = len(locations)

            if n < 2:
                st.warning("📌 Setidaknya harus ada dua lokasi wisata untuk menghitung rute.")
            else:
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

                # Slider jumlah rute yang ingin ditampilkan
                jumlah_rute = st.slider("🔢 Pilih jumlah rute terbaik yang ingin ditampilkan:", 
                                        min_value=1, 
                                        max_value=min(10, len(all_routes)), 
                                        value=3)

                st.subheader(f"🔁 {jumlah_rute} Rute Terbaik:")
                rute_terbaik = []
                for idx in range(jumlah_rute):
                    route, total_jarak = all_routes[idx]
                    nama_rute = " -> ".join([locations.loc[i, 'Nama Tempat Wisata'] for i in route])
                    rute_terbaik.append({'Rute #': idx + 1, 'Total Jarak (km)': round(total_jarak, 2), 'Rute': nama_rute})

                rute_df = pd.DataFrame(rute_terbaik)
                st.dataframe(rute_df)

                # Simpan sebagai CSV
                csv = rute_df.to_csv(index=False).encode('utf-8')
                st.download_button("📥 Unduh Hasil Rute", data=csv, file_name='rute_terbaik.csv', mime='text/csv')

                # Visualisasi Peta Interaktif
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

    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {e}")
