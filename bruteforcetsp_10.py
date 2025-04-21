import streamlit as st
st.set_page_config(page_title="Rute Wisata Optimal", layout="wide")

# Tambahkan opsi halaman di sidebar
st.sidebar.title("Navigasi")
page = st.sidebar.radio("Pilih Halaman", ["Beranda", "Peta Rute", "Hasil Optimal", "Tentang"])

# Halaman Beranda
if page == "Beranda":
    st.title("📍 Aplikasi Rute Wisata Optimal")
    st.markdown("""
    Selamat datang di aplikasi perencanaan rute wisata!
    
    Aplikasi ini menggunakan algoritma Brute Force untuk menentukan rute terpendek dari daftar lokasi wisata yang Anda masukkan.
    """)
    st.image("img/banner.jpg")  # opsional, sesuaikan dengan path gambarmu

# Halaman Peta Rute
elif page == "Peta Rute":
    st.title("🗺️ Visualisasi Peta Rute")
    # TODO: tampilkan lokasi wisata dan rute pada peta
    # contoh placeholder:
    st.map()  # ganti dengan plot folium/mapbox/plotly sesuai data koordinat

# Halaman Hasil Optimal
elif page == "Hasil Optimal":
    st.title("📊 Hasil Perhitungan Rute Optimal")
    # TODO: tampilkan hasil algoritma brute force
    st.write("Menampilkan urutan rute terpendek...")
    # st.table(rute_terpendek) dsb

# Halaman Tentang
elif page == "Tentang":
    st.title("ℹ️ Tentang Aplikasi")
    st.markdown("""
    Aplikasi ini dibuat menggunakan Python dan Streamlit, dengan implementasi algoritma Brute Force untuk menyelesaikan masalah Traveling Salesman Problem (TSP).
    
    Dibuat oleh: [Namamu]  
    Tahun: 2025
    """)
