import streamlit as st
import matplotlib
import matplotlib.pyplot as plt
import time
import sys

# Mengatur backend matplotlib agar stabil
matplotlib.use('Agg')

# Mengatur limit rekursi
sys.setrecursionlimit(10**6)
sys.set_int_max_str_digits(0)

# --- FUNGSI ALGORITMA BARU (JUMLAH DERET S_n) ---

def hitung_deret_iteratif(a, r, n):
    """
    Menerjemahkan algoritma Iteratif Deret:
    Menjumlahkan setiap suku dari 1 sampai n menggunakan akumulator.
    """
    total_jumlah = 0
    suku_sekarang = a
    
    # Loop sebanyak n kali untuk menjumlahkan
    for _ in range(n):
        total_jumlah += suku_sekarang
        suku_sekarang = suku_sekarang * r  # Siapkan suku berikutnya
        
    return total_jumlah

def hitung_deret_rekursif(a, r, n):
    """
    Menerjemahkan algoritma Rekursif Deret:
    Menggunakan logika faktorisasi: Sn = a + r * S(n-1)
    """
    # Base Case: Jika n=1, jumlah deretnya adalah suku pertama itu sendiri
    if n == 1:
        return a
    
    # Recursive Step: 
    # Logika: S_n = a + r(S_{n-1})
    # Contoh S3 = a + ar + ar^2 -> bisa ditulis -> a + r(a + ar) -> a + r(S2)
    return a + (r * hitung_deret_rekursif(a, r, n - 1))

# --- ANTARMUKA STREAMLIT ---

st.set_page_config(page_title="Analisis Algoritma - Deret Geometri", layout="centered")

st.markdown("""
<style>
    @media only screen and (max-width: 600px) {
        [data-testid="stCodeBlock"] pre {
            white-space: pre-wrap !important;
            word-wrap: break-word !important;
        }
        [data-testid="stCodeBlock"] code {
            font-size: 11px !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# 1. JUDUL & HEADER
st.title("🌐 Perbandingan Iteratif vs Rekursif")
st.subheader("Studi Kasus: Menghitung Jumlah Deret Geometri (Sn)")

st.info("""
ℹ️ **Info:** Aplikasi ini menghitung **Jumlah Total ($S_n$)** dari barisan geometri.
Contoh: Jika a=2, r=3, n=3. Maka $2 + 6 + 18 = 26$.
""")

# 2. INPUT USER
st.write("### Masukkan Parameter Deret")
col1, col2 = st.columns(2)

with col1:
    a = st.number_input("Suku Pertama (a):", value=2, step=1)
    r = st.number_input("Rasio (r):", value=3, step=1)

with col2:
    n = st.number_input("Jumlah n Suku (n):", min_value=1, value=10, step=1)

st.markdown("---")
st.subheader("📝 Pseudocode Algoritma")
st.caption("Berikut adalah logika (pseudocode) untuk menghitung **TOTAL DERET**:")

# Tab Pseudocode
tab_iter, tab_rec = st.tabs(["🔹 Algoritma Iteratif", "🔸 Algoritma Rekursif"])

with tab_iter:
    st.markdown("##### Pendekatan Iteratif (Akumulasi)")
    st.write("Menggunakan variabel `total` untuk menampung penjumlahan setiap suku.")
    
    code_iteratif = """
FUNCTION HitungDeretIteratif(a, r, n)
    total = 0
    current_term = a

    // Loop sebanyak n kali
    FOR i FROM 1 TO n DO
        total = total + current_term  // Tambahkan suku ke total
        current_term = current_term * r // Hitung suku berikutnya
    END FOR

    RETURN total
END FUNCTION
    """
    st.code(code_iteratif, language='vb') 

with tab_rec:
    st.markdown("##### Pendekatan Rekursif")
    st.write("Menggunakan sifat matematis $S_n = a + r(S_{n-1})$ untuk efisiensi.")
    
    code_rekursif = """
FUNCTION HitungDeretRekursif(a, r, n)
    // Base Case: Jika hanya 1 suku, kembalikan a
    IF n == 1 THEN
        RETURN a
    
    // Recursive Step
    ELSE
        // Rumus: a + (r * HasilRekursifSebelumnya)
        RETURN a + (r * HitungDeretRekursif(a, r, n - 1))
    END IF

END FUNCTION
"""
    st.code(code_rekursif, language='vb')


if st.button("Jalankan Algoritma"):
    
    # 3. LOGIC & PENGUKURAN WAKTU
    
    # --- Iteratif ---
    start_iter = time.perf_counter()
    hasil_iter = hitung_deret_iteratif(a, r, n)
    end_iter = time.perf_counter()
    waktu_iter = (end_iter - start_iter) * 1000 # ms

    # --- Rekursif ---
    start_rec = time.perf_counter()
    hasil_rec = hitung_deret_rekursif(a, r, n)
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
    
    bars = ax.bar(methods, times, color=colors, width=0.5)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.6f} ms',
                ha='center', va='bottom')

    ax.set_ylabel('Waktu (ms)')
    ax.set_title(f'Runtime Menghitung Jumlah {n} Suku Pertama')
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
        hitung_deret_iteratif(a, r, val_n)
        times_iter.append((time.perf_counter() - t0) * 1000)
        
        # Ukur Rekursif
        t0 = time.perf_counter()
        hitung_deret_rekursif(a, r, val_n)
        times_rec.append((time.perf_counter() - t0) * 1000)
        
        progress_bar.progress((i + 1) / len(ns))
        
    # Plotting Line Chart
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    
    ax2.plot(ns, times_iter, label='Iteratif', color='green', marker='o', linestyle='-')
    ax2.plot(ns, times_rec, label='Rekursif', color='red', marker='x', linestyle='--')
    
    ax2.set_xlabel('Nilai n (Jumlah Suku)')
    ax2.set_ylabel('Waktu (ms)')
    ax2.set_title('Grafik Perbandingan: Runtime vs Input Size (Deret)')
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.6)
    
    st.pyplot(fig2)