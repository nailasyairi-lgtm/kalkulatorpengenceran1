import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Konfigurasi halaman utama
st.set_page_config(page_title="Chemical Analyst Dashboard", page_icon="🧪", layout="wide")

# Navigasi di Sidebar (Sebelah Kiri)
st.sidebar.title("🔬 Menu Analis Kimia")
menu = st.sidebar.radio(
    "Pilih Fitur Aplikasi:",
    ["Home", "Identifikasi Gugus Fungsi", "Konverter Konsentrasi", "Cari Data Unsur"]
)

# ==========================================
# HALAMAN 1: HOME
# ==========================================
if menu == "Home":
    st.title("🧪 Smart Web Apps Analis Kimia")
    st.markdown("""
    Selamat datang di aplikasi web interaktif khusus untuk praktisi dan mahasiswa Analis Kimia! 
    Aplikasi ini dirancang untuk mempercepat pekerjaan laboratorium, mulai dari perhitungan hingga identifikasi sampel.
    
    ### 👈 Silakan pilih fitur pada menu di sebelah kiri:
    * **Identifikasi Gugus Fungsi:** Tebak senyawa organik berdasarkan hasil uji reagen lab.
    * **Konverter Konsentrasi:** Ubah kadar persen (%) menjadi Molaritas (M) secara instan.
    * **Cari Data Unsur:** Intip data nomor atom dan massa atom relatif (Ar) tanpa perlu buka poster tabel periodik.
    """)
    st.info("💡 Aplikasi ini dibuat menggunakan Python dan Streamlit. Sangat ringan dan mudah dikembangkan!")

# ==========================================
# HALAMAN 2: IDENTIFIKASI GUGUS FUNGSI
# ==========================================
elif menu == "Identifikasi Gugus Fungsi":
    st.title("🧪 Sistem Pakar Identifikasi Gugus Fungsi")
    st.write("Masukkan hasil pengamatan uji lab kamu untuk mengetahui jenis gugus fungsi sampel organik.")

    st.subheader("Hasil Uji Laboratorium:")
    
    # Input pilihan hasil uji dari analis
    uji_schiff = st.selectbox("1. Hasil Uji Schiff (Identifikasi Aldehid):", ["Tidak Diuji", "Muncul warna ungu kemerahan", "Tetap bening / tidak berwarna"])
    uji_benedict = st.selectbox("2. Hasil Uji Benedict / Fehling (Gula Pereduksi/Aldehid):", ["Tidak Diuji", "Terbentuk endapan merah bata", "Tetap biru / tidak ada endapan"])
    uji_bisulit = st.selectbox("3. Hasil Uji Natrium Bisulfite (Gugus Karbonil):", ["Tidak Diuji", "Terbentuk kristal/endapan putih", "Tidak terbentuk endapan"])

    st.markdown("---")
    st.subheader("🔍 Hasil Analisis Sistem:")

    # Logika penentuan gugus fungsi sederhana
    if uji_schiff == "Muncul warna ungu kemerahan" or uji_benedict == "Terbentuk endapan merah bata":
        st.success("🎯 **Kesimpulan Sementara:** Sampel kamu mengandung gugus **Aldehid (Alkanal)**.")
        st.caption("Catatan: Uji Schiff positif spesifik menunjukkan adanya gugus aldehid bebas.")
    elif uji_bisulit == "Terbentuk kristal/endapan putih" and uji_schiff == "Tetap bening / tidak berwarna":
        st.success("🎯 **Kesimpulan Sementara:** Sampel kamu kemungkinan besar adalah **Keton (Alkanon)**.")
        st.caption("Catatan: Keton bereaksi dengan bisulit membentuk adisi kristal putih, tetapi negatif pada uji Schiff.")
    elif uji_schiff == "Tidak Diuji" and uji_benedict == "Tidak Diuji" and uji_bisulit == "Tidak Diuji":
        st.warning("Silakan pilih hasil uji lab pada menu di atas terlebih dahulu.")
    else:
        st.info("ℹ️ Hasil uji belum spesifik. Pastikan kombinasi uji reagen sudah sesuai dengan prosedur identifikasi.")

# ==========================================
# HALAMAN 3: KONVERTER KONSENTRASI
# ==========================================
elif menu == "Konverter Konsentrasi":
    st.title("🧮 Konverter % b/b ke Molaritas")
    st.write("Ubah konsentrasi larutan pekat (misal HCl 37% atau H2SO4 98%) menjadi satuan Molaritas ($M$).")
    
    st.write("Rumus yang digunakan: $M = \\frac{\\% \\times \\rho \\times 10}{Mr}$")

    col1, col2 = st.columns(2)
    
    with col1:
        persen = st.number_input("Kadar Larutan (%)", min_value=0.1, max_value=100.0, value=37.0, step=0.1)
        massa_jenis = st.number_input("Massa Jenis / Density (ρ) dalam g/mL", min_value=0.5, max_value=3.0, value=1.19, step=0.01)
        mr = st.number_input("Massa Molar / Mr Zat (g/mol)", min_value=1.0, value=36.5, step=0.1) # Default HCl

    with col2:
        # Menghitung Molaritas
        molaritas = (persen * massa_jenis * 10) / mr
        
        st.metric(label="Hasil Konsentrasi Molaritas (M)", value=f"{molaritas:.3f} M")
        st.success(f"Jadi, larutan dengan kadar {persen}% dan density {massa_jenis} g/mL memiliki konsentrasi **{molaritas:.3f} M**.")

# ==========================================
# HALAMAN 4: CARI DATA UNSUR (TABEL PERIODIK MINI)
# ==========================================
elif menu == "Cari Data Unsur":
    st.title("🧬 Data Unsur Kimia Instan")
    st.write("Ketik simbol unsur atau nama unsur untuk mencari Nomor Atom dan Massa Atom Relatif (Ar).")

    # Database unsur sederhana (bisa kamu tambah sendiri nanti)
    kamus_unsur = {
        "H": {"Nama": "Hidrogen", "Nomor": 1, "Ar": 1.008},
        "C": {"Nama": "Karbon", "Nomor": 6, "Ar": 12.011},
        "N": {"Nama": "Nitrogen", "Nomor": 7, "Ar": 14.007},
        "O": {"Nama": "Oksigen", "Nomor": 8, "Ar": 15.999},
        "Na": {"Nama": "Natrium", "Nomor": 11, "Ar": 22.990},
        "Cl": {"Nama": "Klorida", "Nomor": 17, "Ar": 35.45},
        "Fe": {"Nama": "Besi / Iron", "Nomor": 26, "Ar": 55.845},
        "Cu": {"Nama": "Tembaga / Copper", "Nomor": 29, "Ar": 63.546},
    }

    pilihan_unsur = st.selectbox("Pilih Simbol Unsur:", list(kamus_unsur.keys()))

    # Tampilkan data dalam bentuk kartu/box yang rapi
    data = kamus_unsur[pilihan_unsur]
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(label="Nama Unsur", value=data["Nama"])
    with c2:
        st.metric(label="Nomor Atom", value=data["Nomor"])
    with c3:
        st.metric(label="Massa Atom (Ar)", value=data["Ar"])
   
