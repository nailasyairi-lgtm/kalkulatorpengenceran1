import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Konfigurasi halaman utama
st.set_page_config(page_title="Chemical Analyst Tools", page_icon="🧪", layout="wide")

# Header Aplikasi
st.title("🧪 Web Tools Analis Kimia")
st.markdown("Selamat datang di aplikasi web interaktif untuk mempermudah analisis di laboratorium!")

# Membuat Tab untuk fitur yang berbeda
tab1, tab2 = st.tabs(["🧮 Kalkulator Larutan", "📈 Simulator Kurva Titrasi"])

# ==========================================
# TAB 1: KALKULATOR LARUTAN
# ==========================================
with tab1:
    st.header("Kalkulator Pengenceran Larutan")
    st.write("Hitung volume pekatan yang dibutuhkan untuk pengenceran ($V_1 \\times M_1 = V_2 \\times M_2$)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        m1 = st.number_input("Molaritas Stok/Pekatan ($M_1$) dalam M", min_value=0.01, value=12.0, step=0.1)
        m2 = st.number_input("Molaritas yang Diinginkan ($M_2$) dalam M", min_value=0.01, value=0.1, step=0.01)
        v2 = st.number_input("Volume Akhir yang Diinginkan ($V_2$) dalam mL", min_value=1.0, value=100.0, step=10.0)

    with col2:
        if m1 <= m2:
            st.error("⚠️ Molaritas stok ($M_1$) harus lebih besar dari molaritas yang diinginkan ($M_2$)!")
        else:
            # Rumus: V1 = (M2 * V2) / M1
            v1 = (m2 * v2) / m1
            
            st.metric(label="Volume Stok yang Harus Dipipet ($V_1$)", value=f"{v1:.3f} mL")
            
            st.info(f"💡 **Cara Pembuatan:** Pipet sebanyak **{v1:.3f} mL** larutan stok {m1} M, "
                    f"masukkan ke dalam labu takar {v2} mL, lalu tambahkan akuades hingga tanda batas.")

# ==========================================
# TAB 2: SIMULATOR KURVA TITRASI
# ==========================================
with tab2:
    st.header("Simulasi Kurva Titrasi Asam Kuat - Basa Kuat")
    st.write("Visualisasi perubahan pH pada titrasi 25 mL HCl dengan NaOH.")

    # Input dari user
    c_acid = st.slider("Konsentrasi HCl (M)", min_value=0.05, max_value=0.5, value=0.1, step=0.05)
    c_base = st.slider("Konsentrasi NaOH (M)", min_value=0.05, max_value=0.5, value=0.1, step=0.05)

    # Perhitungan Kurva Titrasi Sederhana
    v_acid = 25.0  # mL
    v_base_add = np.linspace(0, 60, 500) # Volume NaOH dari 0 sampai 60 mL
    
    n_acid_init = c_acid * v_acid
    ph_values = []

    for v in v_base_add:
        n_base_add = c_base * v
        total_vol_liters = (v_acid + v) / 1000.0
        
        if n_acid_init > n_base_add:
            # Kelebihan asam
            h_conc = (n_acid_init - n_base_add) / (v_acid + v)
            ph = -np.log10(h_conc)
        elif n_acid_init < n_base_add:
            # Kelebihan basa
            oh_conc = (n_base_add - n_acid_init) / (v_acid + v)
            poh = -np.log10(oh_conc)
            ph = 14 - poh
        else:
            # Titik Ekuivalen
            ph = 7.0
        ph_values.append(ph)

    # Plotting menggunakan Matplotlib
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(v_base_add, ph_values, color="emerald" if 'emerald' in plt.colormaps else "green", linewidth=2.5)
    
    # Titik Ekuivalen (V_eq = (c_acid * v_acid) / c_base)
    v_eq = (c_acid * v_acid) / c_base
    if v_eq <= 60:
        ax.plot(v_eq, 7, 'ro', label=f'Titik Ekuivalen ({v_eq:.1f} mL, pH 7)')
        ax.legend()
        
    ax.set_xlabel("Volume NaOH yang Ditambahkan (mL)")
    ax.set_ylabel("pH Larutan")
    ax.set_title(f"Kurva Titrasi HCl {c_acid} M vs NaOH {c_base} M")
    ax.grid(True, linestyle="--", alpha=0.6)

    # Tampilkan grafik di Streamlit
    st.pyplot(fig)
