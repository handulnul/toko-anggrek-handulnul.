import streamlit as st
import pandas as pd
import os

# ==============================================================================
# 1. KONFIGURASI HALAMAN & JUDUL WEB
# ==============================================================================
st.set_page_config(
    page_title="Sistem Katalog Toko Bunga Handulnul", 
    page_icon="🌸", 
    layout="wide"
)

# ==============================================================================
# 2. MENAMPILKAN BANNER TOKO (Paling Atas)
# ==============================================================================
nama_file_banner = "Merah Muda Hijau Lembut Minimalis Estetik Promosi Toko Bunga Spanduk.jpg"

# Di sini use_column_width diganti dengan use_container_width agar tidak muncul warning
if os.path.exists(nama_file_banner):
    st.image(nama_file_banner, use_container_width=True)
else:
    if os.path.exists("banner.jpg"):
        st.image("banner.jpg", use_container_width=True)
    else:
        st.warning("⚠️ File Gambar Banner/Spanduk tidak ditemukan di folder. Pastikan file gambar spanduk berada di folder yang sama dengan main.py")

st.markdown("---")

# ==============================================================================
# 3. MEMBACA DATA BASE CSV (buku1.csv)
# ==============================================================================
df = pd.read_csv('buku1.csv')
df = df.dropna(how='all')

# ==============================================================================
# 4. SIDEBAR: PANEL FILTER & PENCARIAN
# ==============================================================================
st.sidebar.header("⚙️ Panel Filter & Pencarian")

pilihan_kategori = st.sidebar.multiselect(
    "Pilih Warna/Kategori Anggrek:",
    options=['putih', 'ungu', 'pink'],
    default=['putih', 'ungu', 'pink']
)

cari_nama = st.sidebar.text_input("🔍 Cari berdasarkan nama:", "")

# PROSES MENYARING DATA
if 'kategori' in df.columns:
    df_filtered = df[df['kategori'].astype(str).str.strip().str.lower().isin(pilihan_kategori)]
else:
    df_filtered = df

if cari_nama and 'nama' in df.columns:
    df_filtered = df_filtered[df_filtered['nama'].astype(str).str.contains(cari_nama, case=False, na=False)]

# ==============================================================================
# 5. SIDEBAR: FORM UNTUK MENAMBAH ANGGREK BARU
# ==============================================================================
st.sidebar.markdown("---")
st.sidebar.subheader("➕ Tambah Anggrek Baru")

nama_baru = st.sidebar.text_input("Nama Anggrek Baru:")
kategori_baru = st.sidebar.selectbox("Pilih Kategori Warna:", ["putih", "ungu", "pink"])
harga_baru = st.sidebar.text_input("Harga (Contoh: 10.000 btg):", "10.000 btg")
stok_baru = st.sidebar.text_input("Jumlah Stok (Contoh: 100):", "100")
foto_baru = st.sidebar.text_input("Nama File Gambar (contoh: anggrek1.jpg):")
status_baru = st.sidebar.selectbox("Status Ketersediaan:", ["tersedia", "habis"])

if st.sidebar.button("Simpan ke Katalog"):
    if nama_baru and foto_baru:
        data_baru = {
            'nama': [nama_baru],
            'kategori': [kategori_baru],
            'harga': [harga_baru],
            'stok': [stok_baru],
            'foto': [foto_baru],
            'status': [status_baru]
        }
        df_baru = pd.DataFrame(data_baru)
        
        try:
            df_baru.to_csv('buku1.csv', mode='a', header=False, index=False)
            st.sidebar.success(f"✅ Berhasil menambahkan {nama_baru}!")
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"Gagal menyimpan data: {e}")
    else:
        st.sidebar.warning("Mohon isi minimal Nama dan Nama File Gambar terlebih dahulu!")

# ==============================================================================
# 6. HALAMAN UTAMA: MENAMPILKAN DAFTAR KOLEKSI ANGGREK (GRID 3 KOLOM)
# ==============================================================================
st.subheader("🛍️ Daftar Koleksi Anggrek")

if not df_filtered.empty:
    kolom = st.columns(3)
    for index, row in df_filtered.reset_index().iterrows():
        col_idx = index % 3
        with kolom[col_idx]:
            st.markdown(f"### {row['nama']}")
            
            nama_gambar = str(row['foto']).strip()
            # Di sini use_column_width diganti dengan use_container_width agar tidak muncul warning
            if os.path.exists(nama_gambar):
                st.image(nama_gambar, use_container_width=True)
            else:
                st.warning(f"⚠️ Gambar '{nama_gambar}' tidak ditemukan.")
                
            st.info(f"🎨 **Kategori:** {str(row['kategori']).upper()}")
            st.success(f"💰 **Harga:** {row['harga']}")
            st.markdown(f"📦 **Stok:** {row['stok']} | **Status:** {str(row['status']).upper()}")
            st.markdown("---")
else:
    st.info("Tidak ada data anggrek yang cocok dengan filter Anda.")

# ==============================================================================
# 7. HALAMAN UTAMA: TABEL DATA SPREADSHEET (Bagian Bawah)
# ==============================================================================
with st.expander("📊 Lihat Seluruh Data Tabel (Spreadsheet)"):
    st.dataframe(df, use_container_width=True)