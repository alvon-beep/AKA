import streamlit as st
import matplotlib
import matplotlib.pyplot as plt
import time
import sys

# Mengatur backend matplotlib agar stabil
matplotlib.use('Agg')

# Mengatur limit rekursi (Penting karena algoritma rekursif ini memakan stack O(n))
sys.setrecursionlimit(10**6)
sys.set_int_max_str_digits(0)

# --- FUNGSI ALGORITMA BARU (SUKU KE-N) ---

def hitung_suku_iteratif(a, r, n):
    """
    Menerjemahkan algoritma Iteratif dari Pseudo-code:
    Mencari suku ke-n dengan loop.
    """
    suku_sekarang = a
    if n <= 1:
        return a
    
    for _ in range(2, n + 1):
        suku_sekarang = suku_sekarang * r
        
    return suku_sekarang

def hitung_suku_rekursif(a, r, n):
    """
    Menerjemahkan algoritma Rekursif dari Pseudo-code:
    Mencari suku ke-n dengan memanggil fungsi diri sendiri (n-1).
    """

    if n == 1:
        return a
    return hitung_suku_rekursif(a, r, n - 1) * r

# --- ANTARMUKA STREAMLIT ---

st.set_page_config(page_title="Analisis Algoritma - Suku Geometri", layout="centered")

st.markdown("""
<style>
    /* 1. CSS untuk Layar HP (Lebar < 600px) */
    @media only screen and (max-width: 600px) {
        [data-testid="stCodeBlock"] pre {
            white-space: pre-wrap !important; /* Paksa turun baris di HP */
            word-wrap: break-word !important;
        }
        
        /* Kecilkan font sedikit biar muat banyak di HP */
        [data-testid="stCodeBlock"] code {
            font-size: 11px !important;
        }
    }

    /* 2. CSS untuk PC (Biarkan default / scroll samping jika perlu) */
    /* Tidak perlu coding apa-apa, Streamlit defaultnya sudah bagus buat PC */
</style>
""", unsafe_allow_html=True)

# 1. JUDUL & HEADER
st.title("🌐 Perbandingan Iteratif vs Rekursif")
st.subheader("Studi Kasus: Menghitung Suku Ke-n Deret Geometri")

st.info("""
ℹ️ **Info:** Aplikasi ini menghitung nilai suku ke-n ($S_n$) dari sebuah barisan geometri.
Algoritma yang digunakan adalah Iteratif dan Rekursif. Algoritma ini hanya untuk mencari suku tertentu, bukan jumlah deret.
""")

# 2. INPUT USER
st.write("### Masukkan Parameter Barisan")
col1, col2 = st.columns(2)

with col1:
    a = st.number_input("Suku Pertama (a):", value=2, step=1)
    r = st.number_input("Rasio (r):", value=3, step=1)

with col2:
    n = st.number_input("Cari Suku ke- (n):", min_value=1, value=10, step=1)

st.markdown("---")
st.subheader("📝 Pseudocode Algoritma")
st.caption("Berikut adalah rancangan logika (pseudocode) dari kedua algoritma yang digunakan:")

# Membuat Tab agar user bisa memilih mau lihat yang mana (mirip tombol di screenshot)
tab_iter, tab_rec = st.tabs(["🔹 Algoritma Iteratif", "🔸 Algoritma Rekursif"])

with tab_iter:
    st.markdown("##### Pendekatan Iteratif (Looping)")
    st.write("Menggunakan perulangan `FOR` dari suku ke-2 hingga ke-n.")
    
    # Kita tulis string pseudocode-nya manual agar formatnya rapi
    code_iteratif = """
FUNCTION HitungSukuIteratif(a, r, n)
    // a: Suku pertama, r: Rasio, n: Suku dicari

    IF n <= 1 THEN
        RETURN a
    END IF

    suku_current = a
    
    // Loop dari 2 sampai n
    FOR i FROM 2 TO n DO
        suku_current = suku_current * r
    END FOR

    RETURN suku_current
END FUNCTION
    """
    # language='vb' atau 'lua' biasanya memberikan coloring yang bagus untuk pseudocode
    st.code(code_iteratif, language='vb') 

with tab_rec:
    st.markdown("##### Pendekatan Rekursif")
    st.write("Fungsi memanggil dirinya sendiri `(n-1)` sampai mencapai basis `n=1`.")
    
    code_rekursif = """
FUNCTION HitungSukuRekursif(a, r, n)
    // Base Case
    IF n == 1 THEN
        RETURN a
    
    // Recursive Step
    ELSE
        // Panggil fungsi diri sendiri untuk (n-1) lalu kalikan rasio
        RETURN HitungSukuRekursif(a, r, n - 1) * r
    END IF

END FUNCTION
"""
    st.code(code_rekursif, language='vb')


if st.button("Jalankan Algoritma"):
    
    # 3. LOGIC & PENGUKURAN WAKTU
    
    # --- Iteratif ---
    start_iter = time.perf_counter()
    hasil_iter = hitung_suku_iteratif(a, r, n)
    end_iter = time.perf_counter()
    waktu_iter = (end_iter - start_iter) * 1000 # ms

    # --- Rekursif ---
    start_rec = time.perf_counter()
    hasil_rec = hitung_suku_rekursif(a, r, n)
    end_rec = time.perf_counter()
    waktu_rec = (end_rec - start_rec) * 1000 # ms

    # 4. OUTPUT HASIL
    st.success(f"✅ **Iteratif:** S({n}) = {hasil_iter} | Waktu = {waktu_iter:.6f} ms")
    st.error(f"🔁 **Rekursif:** S({n}) = {hasil_rec} | Waktu = {waktu_rec:.6f} ms")

    # 5. VISUALISASI BAR CHART
    st.write("### 📊 Perbandingan Waktu Eksekusi")
    
    fig, ax = plt.subplots(figsize=(8, 4))
    methods = ['Iteratif', 'Rekursif']
    times = [waktu_iter, waktu_rec]
    colors = ['green', 'red']
    
    # Style: width=0.5
    bars = ax.bar(methods, times, color=colors, width=0.5)
    
    # Style: Label presisi di atas batang
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.6f} ms',
                ha='center', va='bottom')

    ax.set_ylabel('Waktu (ms)')
    ax.set_title(f'Runtime Mencari Suku ke-{n}')
    st.pyplot(fig)

# 6. OUTPUT VISUAL GRAFIK GARIS
st.markdown("---")
tampilkan_grafik = st.checkbox(f"Tampilkan grafik runtime (n = 1 hingga {n})")

if tampilkan_grafik:
    st.write(f"Memproses data grafik untuk n=1 s.d {n}...")
    
    ns = range(1, n + 1)
    times_iter = []
    times_rec = []
    
    progress_bar = st.progress(0)
    
    for i, val_n in enumerate(ns):
        # Ukur Iteratif
        t0 = time.perf_counter()
        hitung_suku_iteratif(a, r, val_n)
        times_iter.append((time.perf_counter() - t0) * 1000)
        
        # Ukur Rekursif
        t0 = time.perf_counter()
        hitung_suku_rekursif(a, r, val_n)
        times_rec.append((time.perf_counter() - t0) * 1000)
        
        progress_bar.progress((i + 1) / len(ns))
        
    # Plotting Line Chart
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    
    # Style: Marker 'o' & 'x', Linestyle '-' & '--', Warna Green & Red
    ax2.plot(ns, times_iter, label='Iteratif', color='green', marker='o', linestyle='-')
    ax2.plot(ns, times_rec, label='Rekursif', color='red', marker='x', linestyle='--')
    
    ax2.set_xlabel('Nilai n (Suku ke-)')
    ax2.set_ylabel('Waktu (ms)')
    ax2.set_title('Grafik Perbandingan: Runtime vs Input Size')
    ax2.legend()
    
    # Style: Grid putus-putus dengan alpha 0.6
    ax2.grid(True, linestyle='--', alpha=0.6)
    
    st.pyplot(fig2)
    st.caption("Catatan: Fungsi rekursif di sini memanggil dirinya sendiri sebanyak (n-1) kali, sehingga kompleksitasnya O(n), sama seperti iteratif loop.")