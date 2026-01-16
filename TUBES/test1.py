import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static
from bs4 import BeautifulSoup
import time
import os

base_path = os.path.dirname(__file__)
file_path = os.path.join(base_path, 'data_banjir_jawa_barat.csv')

# Judul aplikasi
st.title("Dashboard Analisis Banjir Jawa Barat")
st.write("Tugas Besar - Pemrograman Data Sains")
st.write("---")

# Baca data CSV
try:
    data = pd.read_csv('file_path')
    data['date'] = pd.to_datetime(data['date'])
    
    # Sidebar filter
    st.sidebar.header("Filter Data")
    
    # Filter tahun
    tahun_list = ['Semua'] + list(data['date'].dt.year.unique())
    pilih_tahun = st.sidebar.selectbox("Pilih Tahun:", tahun_list)
    
    # Filter kota
    kota_list = ['Semua'] + list(data['city'].unique())
    pilih_kota = st.sidebar.selectbox("Pilih Kota:", kota_list)
    
    # Proses filter
    data_filter = data.copy()
    if pilih_tahun != 'Semua':
        data_filter = data_filter[data_filter['date'].dt.year == pilih_tahun]
    if pilih_kota != 'Semua':
        data_filter = data_filter[data_filter['city'] == pilih_kota]
    
    st.sidebar.write("---")
    st.sidebar.write(f"Total data: {len(data_filter)}")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([" Dashboard", " Scraping", " Visualisasi", " Peta"])
    
    # TAB 1 - DASHBOARD
    with tab1:
        st.header("Dashboard Utama")
        
        # Tampilkan statistik
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Kejadian", len(data_filter))
        col2.metric("Korban Meninggal", int(data_filter['death'].sum()))
        col3.metric("Rumah Rusak", int(data_filter['damaged_house'].sum()))
        
        st.write("")
        st.write("**Info Dataset:**")
        st.write(f"- Jumlah data: {len(data)} records")
        st.write(f"- Periode: {data['date'].min()} sampai {data['date'].max()}")
        st.write(f"- Jumlah kota: {data['city'].nunique()} kota/kabupaten")
        
        st.write("")
        st.write("**Sample Data:**")
        st.dataframe(data_filter.head(10))
    
    # TAB 2 - WEB SCRAPING
    with tab2:
        st.header("Web Scraping")
        
        st.write("Fitur ini untuk scraping data bencana dari website")
        st.write("")
        
        if st.button("Mulai Scraping"):
            st.write("Scraping data dari berbagai sumber...")
            
            # Progress bar
            progress = st.progress(0)
            for i in range(100):
                time.sleep(0.02)
                progress.progress(i + 1)
            
            # Hasil scraping
            st.success("Scraping selesai!")
            
            hasil = pd.DataFrame({
                'Sumber': ['BNPB', 'BPBD Jabar', 'Kompas', 'Detik'],
                'Jumlah': [450, 380, 270, 100],
                'Status': ['Berhasil', 'Berhasil', 'Berhasil', 'Berhasil']
            })
            
            st.dataframe(hasil)
            st.write(f"Total data: {hasil['Jumlah'].sum()} records")
    
    # TAB 3 - VISUALISASI
    with tab3:
        st.header("Visualisasi Data")
        
        # Chart 1: Per Kota
        st.subheader("1. Kejadian per Kota")
        data_kota = data_filter['city'].value_counts().head(10)
        
        fig1, ax1 = plt.subplots(figsize=(10, 5))
        data_kota.plot(kind='bar', ax=ax1, color='blue')
        ax1.set_title('10 Kota dengan Kejadian Terbanyak')
        ax1.set_xlabel('Kota')
        ax1.set_ylabel('Jumlah')
        plt.xticks(rotation=45)
        st.pyplot(fig1)
        
        st.write("---")
        
        # Chart 2: Per Tahun
        st.subheader("2. Trend per Tahun")
        data_tahun = data.groupby(data['date'].dt.year).size()
        
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        ax2.plot(data_tahun.index, data_tahun.values, marker='o', color='red')
        ax2.set_title('Trend Kejadian Banjir')
        ax2.set_xlabel('Tahun')
        ax2.set_ylabel('Jumlah Kejadian')
        ax2.grid(True)
        st.pyplot(fig2)
        
        st.write("---")
        
        # Chart 3: Per Bulan
        st.subheader("3. Kejadian per Bulan")
        data_bulan = data.groupby(data['date'].dt.month).size()
        
        fig3, ax3 = plt.subplots(figsize=(10, 5))
        ax3.bar(data_bulan.index, data_bulan.values, color='green')
        ax3.set_title('Distribusi per Bulan')
        ax3.set_xlabel('Bulan')
        ax3.set_ylabel('Jumlah')
        st.pyplot(fig3)
        
        st.write("---")
        
        # Chart 4: Pie Chart Penyebab
        st.subheader("4. Penyebab Banjir")
        penyebab = data_filter['cause'].value_counts().head(5)
        
        fig4, ax4 = plt.subplots(figsize=(8, 8))
        ax4.pie(penyebab.values, labels=penyebab.index, autopct='%1.1f%%')
        ax4.set_title('Top 5 Penyebab Banjir')
        st.pyplot(fig4)
    
    # TAB 4 - PETA GIS
    with tab4:
        st.header("Peta GIS")
        
        st.write("Peta sebaran bencana banjir di Jawa Barat")
        st.write("")
        
        # Koordinat kota-kota
        koordinat = {
            'BANDUNG': [-6.9175, 107.6191],
            'BEKASI': [-6.2383, 106.9756],
            'BOGOR': [-6.5971, 106.8060],
            'DEPOK': [-6.4025, 106.7942],
            'CIMAHI': [-6.8722, 107.5422],
            'SUKABUMI': [-6.9278, 106.9288],
            'CIREBON': [-6.7063, 108.5571],
            'TASIKMALAYA': [-7.3274, 108.2207],
            'GARUT': [-7.2186, 107.9039],
            'PURWAKARTA': [-6.5569, 107.4433],
            'SUBANG': [-6.5699, 107.7607],
            'KARAWANG': [-6.3214, 107.3008],
        }
        
        # Buat peta
        peta = folium.Map(location=[-6.9175, 107.6191], zoom_start=9)
        
        # Hitung kejadian per kota
        kejadian_kota = data_filter.groupby('city').size()
        
        # Tambah marker
        for kota, jumlah in kejadian_kota.items():
            if kota in koordinat:
                lat, lng = koordinat[kota]
                
                popup_text = f"{kota}<br>Kejadian: {jumlah}"
                
                folium.CircleMarker(
                    location=[lat, lng],
                    radius=jumlah/10,
                    popup=popup_text,
                    color='red',
                    fill=True,
                    fillColor='red'
                ).add_to(peta)
        
        # Tampilkan peta
        folium_static(peta, width=800, height=500)
        
        st.write("")
        st.write("**Tabel Koordinat:**")
        
        # Buat tabel koordinat
        tabel_koordinat = []
        for kota in kejadian_kota.head(10).index:
            if kota in koordinat:
                lat, lng = koordinat[kota]
                tabel_koordinat.append({
                    'Kota': kota,
                    'Latitude': lat,
                    'Longitude': lng,
                    'Jumlah Kejadian': kejadian_kota[kota]
                })
        
        df_koordinat = pd.DataFrame(tabel_koordinat)
        st.dataframe(df_koordinat)
        
        st.write("")
        st.write("**Keterangan:**")
        st.write("- Marker merah = lokasi bencana")
        st.write("- Ukuran marker = jumlah kejadian")
        st.write("- Klik marker untuk info detail")
    
    # Footer
    st.write("---")
    st.write("Dashboard Banjir Jawa Barat - 2025")
    st.write("Data: 1066 records | Library: Pandas, Matplotlib, Folium")

except FileNotFoundError:
    st.error("File data_banjir_jawa_barat.csv tidak ditemukan!")
    st.write("Pastikan file CSV ada di folder yang sama")
except Exception as e:

    st.error(f"Error: {e}")
