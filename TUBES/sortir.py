import pandas as pd

# 1. Membaca dataset utama
df = pd.read_excel('data_bencana.xlsx')

# 2. Filter data: 
# - Jenis Bencana (disaster_type) mengandung kata 'BANJIR'
# - Provinsi (province) mengandung kata 'JAWA BARAT'
df_banjir_jabar = df[
    (df['disaster_type'].str.contains('BANJIR', case=False, na=False)) & 
    (df['province'].str.contains('JAWA BARAT', case=False, na=False))
]

# 3. Mengubah format kolom tanggal agar bisa diurutkan
df_banjir_jabar['date'] = pd.to_datetime(df_banjir_jabar['date'])

# 4. Sortir data berdasarkan tanggal (dari terlama ke terbaru)
df_sorted = df_banjir_jabar.sort_values(by='date')

# 5. Menyimpan hasil sortir ke file CSV baru untuk digunakan di aplikasi/laporan
df_sorted.to_csv('data_banjir_jawa_barat.csv', index=False)

# Menampilkan hasil
print(f"Berhasil menyaring {len(df_sorted)} data banjir di Jawa Barat.")
print(df_sorted[['date', 'city', 'disaster_type']].head())