import streamlit as st
import matplotlib
import matplotlib.pyplot as plt
import time
import sys

matplotlib.use('Agg')
sys.setrecursionlimit(10**6)
if sys.version_info >= (3, 11):
    sys.set_int_max_str_digits(0)

st.set_page_config(page_title="Analisis Algoritma", layout="centered")

st.markdown("""
<style>
    /* Agar code block rapi di HP */
    @media only screen and (max-width: 600px) {
        [data-testid="stCodeBlock"] pre {
            white-space: pre-wrap !important;
            word-wrap: break-word !important;
        }
    }

    /* Kotak Penjelasan (Card Style) */
    .desc-container {
        background-color: rgba(41, 182, 246, 0.1);
        border: 1px solid rgba(41, 182, 246, 0.4);
        color: inherit;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        height: 300px;
        display: flex;
        flex-direction: column;
        overflow-y: auto;
    }
    
    .desc-container h4 {
        margin-top: 0;
        margin-bottom: 10px;
        font-size: 1.1rem;
        color: #29B6F6 !important;
        border-bottom: 1px solid rgba(41, 182, 246, 0.2);
        padding-bottom: 5px;
    }

    .desc-container p, .desc-container li {
        font-size: 0.9rem;
        line-height: 1.5;
        margin-bottom: 8px;
    }

    .code-highlight {
        background-color: rgba(41, 182, 246, 0.1);
        padding: 2px 6px;
        border-radius: 4px;
        font-family: monospace;
        color: #29B6F6;
        font-weight: bold;
    }
    
    .math-step {
        background-color: rgba(41, 182, 246, 0.05);
        border-left: 4px solid #29B6F6;
        padding: 10px 15px;
        margin: 10px 0;
        border-radius: 0 8px 8px 0;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

def hitung_deret_iteratif(a, r, n):
    total_jumlah = 0
    suku_sekarang = a
    for _ in range(n):
        total_jumlah += suku_sekarang
        suku_sekarang = suku_sekarang * r
    return total_jumlah

def hitung_deret_rekursif(a, r, n):
    if n == 1:
        return a
    return a + (r * hitung_deret_rekursif(a, r, n - 1))

st.title("🌐 Perbandingan Iteratif vs Rekursif")
st.subheader("Studi Kasus: Menghitung Jumlah Deret Geometri (Sn)")

st.info("Aplikasi ini menghitung **Jumlah Total** ($S_n$) dari barisan geometri.")

col1, col2 = st.columns(2)
with col1:
    a = st.number_input("Suku Pertama (a):", value=2, step=1)
    r = st.number_input("Rasio (r):", value=3, step=1)
with col2:
    # Sedikit limitasi n agar grafik tidak terlalu lama digenerate saat looping
    n = st.number_input("Jumlah n Suku (n):", min_value=1, max_value=900, value=10, step=1)

st.subheader("📝 Pseudocode Algoritma")

tab_iter, tab_rec = st.tabs(["🔹 Algoritma Iteratif", "🔸 Algoritma Rekursif"])

with tab_iter:
    st.markdown("##### Pendekatan Iteratif (Looping)")
    st.write("Menggunakan variabel penampung untuk menjumlahkan nilai.")
    st.code("""
FUNCTION HitungDeretIteratif(a, r, n)
    total = 0
    current_term = a
    FOR i FROM 1 TO n DO
        total = total + current_term
        current_term = current_term * r
    END FOR
    RETURN total
END FUNCTION
""", language='vb')

with tab_rec:
    st.markdown("##### Pendekatan Rekursif")
    st.write("Memanggil fungsi dirinya sendiri sampai mencapai base case.")
    st.code("""
FUNCTION HitungDeretRekursif(a, r, n)
    IF n == 1 THEN
        RETURN a
    ELSE
        RETURN a + (r * HitungDeretRekursif(a, r, n - 1))
    END IF
END FUNCTION
""", language='vb')

# --- BAGIAN UTAMA YANG DIMODIFIKASI ---
if st.button("🚀 Jalankan Algoritma & Analisis Grafik"):
    # 1. Hitung Hasil Akhir (Untuk Display Text)
    start_iter = time.perf_counter()
    hasil_iter = hitung_deret_iteratif(a, r, n)
    end_iter = time.perf_counter()
    waktu_iter_final = (end_iter - start_iter) * 1000

    start_rec = time.perf_counter()
    hasil_rec = hitung_deret_rekursif(a, r, n)
    end_rec = time.perf_counter()
    waktu_rec_final = (end_rec - start_rec) * 1000

    st.success(f"✅ **Iteratif:** S({n}) = {hasil_iter} | Waktu Akhir = {waktu_iter_final:.6f} ms")
    st.error(f"🔁 **Rekursif:** S({n}) = {hasil_rec} | Waktu Akhir = {waktu_rec_final:.6f} ms")

    # 2. Persiapkan Data Grafik (Looping dari 1 s.d n)
    st.write("### 📊 Perbandingan Runtime (Line Chart)")
    st.caption(f"Mengukur performa dari input n=1 sampai n={n}...")
    
    input_range = range(1, n + 1)
    history_iter = []
    history_rec = []

    # Progress bar karena looping n kali bisa memakan waktu sedikit
    progress_bar = st.progress(0)
    
    for i, current_n in enumerate(input_range):
        # Ukur Iteratif
        t0 = time.perf_counter()
        hitung_deret_iteratif(a, r, current_n)
        t1 = time.perf_counter()
        history_iter.append((t1 - t0) * 1000)

        # Ukur Rekursif
        t0 = time.perf_counter()
        hitung_deret_rekursif(a, r, current_n)
        t1 = time.perf_counter()
        history_rec.append((t1 - t0) * 1000)
        
        # Update progress
        progress_bar.progress((i + 1) / len(input_range))

    # 3. Membuat Plotting Garis Beririsan
    fig, ax = plt.subplots(figsize=(8, 4))
    
    # Plot Garis Iteratif
    ax.plot(input_range, history_iter, label='Iteratif O(n)', color='#4CAF50', linewidth=2)
    # Plot Garis Rekursif
    ax.plot(input_range, history_rec, label='Rekursif O(n)', color='#F44336', linewidth=2, linestyle='--')

    # Dekorasi Grafik
    ax.set_title(f"Komparasi Waktu Eksekusi (1 s.d {n})")
    ax.set_xlabel('Input Size (n)')
    ax.set_ylabel('Waktu Eksekusi (ms)')
    ax.legend() # Ini yang membuat label muncul
    ax.grid(True, linestyle=':', alpha=0.6)

    # Mengisi area di antara garis (opsional, untuk efek visual "beririsan/gap")
    ax.fill_between(input_range, history_iter, history_rec, color='grey', alpha=0.1)

    st.pyplot(fig)
# --- AKHIR MODIFIKASI ---

st.subheader("🔢 Analisis & Pembuktian Matematis")
st.caption("Penjelasan langkah demi langkah kenapa kompleksitasnya Linear O(n).")

math_tab1, math_tab2 = st.tabs(["📐 Analisis Iteratif (Sigma)", "📐 Analisis Rekursif (Substitusi)"])

with math_tab1:
    st.markdown(r"""
    <div class="desc-container">
        <h4>1. Analisis Loop dengan Notasi Sigma (Σ)</h4>
        <p>Pada algoritma iteratif, kita menjumlahkan biaya (cost) dari setiap baris kode yang dieksekusi.</p>
        <p><b>Identifikasi Biaya:</b></p>
        <ul>
            <li>Inisialisasi (<span class="code-highlight">total=0</span>) = Konstan (<i>c<sub>init</sub></i>)</li>
            <li>Operasi dalam Loop (<span class="code-highlight">+</span> dan <span class="code-highlight">*</span>) = Konstan (<i>c<sub>ops</sub></i>)</li>
            <li>Karena operasi dalam loop selalu sama (tidak tergantung nilai i), kita pakai <b>Sum of 1</b>.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.latex(r"T(n) = c_{\mathrm{init}} + \sum_{i=1}^{n} (c_{\mathrm{ops}})")

    st.markdown(r"""
    <div class='math-step'>
        Menggunakan rumus deret aritmatika konstanta <b>&Sigma; 1 = n</b>:
    </div>
    """, unsafe_allow_html=True)

    st.latex(r"""
    \begin{aligned}
    T(n) &= c_{\mathrm{init}} + c_{\mathrm{ops}} \cdot n \\
    T(n) &\approx C \cdot n
    \end{aligned}
    """)
    
    st.success("Kesimpulan: Karena pangkat tertinggi dari n adalah 1, maka kompleksitasnya **Linear O(n)**.")

with math_tab2:
    st.markdown(r"""
    <div class="desc-container">
        <h4>2. Analisis Rekursif dengan Metode Substitusi</h4>
        <p>Pada rekursif, waktu eksekusi dinyatakan sebagai fungsi rekurensi <i>T(n)</i>.</p>
        <p><b>Relasi Rekurensi:</b></p>
        <ul>
            <li><b>Base Case (n=1):</b> Hanya return. Biaya = <i>c<sub>1</sub></i>.</li>
            <li><b>Recursive Step (n>1):</b> 1x pemanggilan rekursif (<i>T(n-1)</i>) + operasi aritmatika (<i>c<sub>2</sub></i>).</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    st.latex(r"""
    T(n) = \begin{cases} 
    c_1 & \text{jika } n = 1 \\
    T(n-1) + c_2 & \text{jika } n > 1 
    \end{cases}
    """)

    st.markdown(r"""
    <div class='math-step'>
        <b>Langkah Substitusi Mundur (Unfolding):</b><br>
        Kita ganti <i>T(n-1)</i> dengan definisinya sendiri berulang kali.
    </div>
    """, unsafe_allow_html=True)

    st.latex(r"""
    \begin{aligned}
    T(n) &= T(n-1) + c_2 \\
    &= (T(n-2) + c_2) + c_2 = T(n-2) + 2c_2 \\
    &= T(n-3) + 3c_2 \\
    &\dots \\
    &= T(n-k) + k \cdot c_2
    \end{aligned}
    """)

    st.markdown(r"""
    <div class='math-step'>
        <b>Mencari Base Case:</b><br>
        Berhenti saat <i>n - k = 1</i> yang berarti <i>k = n - 1</i>.
    </div>
    """, unsafe_allow_html=True)

    st.latex(r"T(n) = c_1 + c_2(n-1) \approx A \cdot n + B")

    st.error("Kesimpulan: Hasil akhirnya adalah fungsi linear, maka kompleksitasnya **Linear O(n)**.")

st.subheader("📚 Teori Dasar")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
<div class="desc-container">
    <h4>📖 Konsep Deret Geometri</h4>
    <p>Kode ini menghitung <b>Jumlah Total (Sn)</b>, yaitu akumulasi penjumlahan dari suku pertama hingga suku ke-n.</p>
    <p><b>Definisi:</b><br>
    Deret di mana rasio antara dua suku berturutan selalu tetap (r).</p>
    <p><b>Rumus:</b> <i>S<sub>n</sub></i> = a(r<sup>n</sup> - 1) / (r - 1) <small>(untuk r > 1)</small></p>
    <p><b>Variabel:</b></p>
    <ul>
        <li><span class="code-highlight">a</span>: Suku awal.</li>
        <li><span class="code-highlight">r</span>: Rasio pengali.</li>
        <li><span class="code-highlight">n</span>: Jumlah iterasi.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="desc-container">
        <h4>🔄 Logika Iteratif (Loop)</h4>
        <p>Pendekatan <code>hitung_deret_iteratif</code> menggunakan metode <b>Akumulasi State</b>.</p>
        <p><b>Cara Kerja:</b></p>
        <ol>
            <li>Inisialisasi <code>total = 0</code>.</li>
            <li>Loop <code>i</code> dari 1 sampai <code>n</code>.</li>
            <li>Update total: <code>total += suku_sekarang</code>.</li>
            <li>Update suku: <code>suku_sekarang *= r</code>.</li>
        </ol>
        <p><b>Kelebihan:</b><br>
        Sangat efisien memori (Space O(1)). Tidak ada risiko stack overflow meski n = 1.000.000.</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="desc-container">
        <h4>⚡ Logika Rekursif</h4>
        <p>Pendekatan <code>hitung_deret_rekursif</code> memecah masalah menjadi sub-masalah kecil (Divide & Conquer).</p>
        <p><b>Konsep:</b> <code>S(n) = a + r * S(n-1)</code></p>
        <p><b>Alur Eksekusi:</b></p>
        <ul>
            <li>Cek <b>Base Case</b>: Jika n=1, return a.</li>
            <li>Jika tidak, panggil fungsi dirinya sendiri dengan n-1.</li>
            <li>Hasil panggilan dikalikan r, lalu ditambah a.</li>
        </ul>
        <p><b>Kekurangan:</b> Memakan memori stack (Space O(n)).</p>
    </div>
    """, unsafe_allow_html=True)

c4, c5, c6 = st.columns(3)

with c4:
    st.markdown("""
    <div class="desc-container">
        <h4>📈 Time & Space Complexity</h4>
        <p>Perbandingan teoritis Big-O Notation:</p>
        <ul>
            <li><b>Time Complexity: O(n)</b><br>
            Kedua algoritma linear. Waktu proses berbanding lurus dengan input n.</li>
            <li><b>Space Complexity:</b>
                <ul>
                    <li><b>Iteratif: O(1)</b> - Konstan. Hanya butuh variabel temp.</li>
                    <li><b>Rekursif: O(n)</b> - Linear. Butuh tumpukan memori (stack frame) sebanyak n.</li>
                </ul>
            </li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with c5:
    st.markdown("""
    <div class="desc-container">
        <h4>⚖️ Mengapa Rekursif Lebih Lambat?</h4>
        <p>Secara teknis komputer (Low Level), rekursif memiliki <b>Overhead</b>:</p>
        <ol>
            <li><b>Context Switching:</b> CPU harus menyimpan state fungsi saat ini ke RAM sebelum masuk ke fungsi baru.</li>
            <li><b>Stack Allocation:</b> Pembuatan frame baru di memori stack memakan siklus CPU tambahan.</li>
        </ol>
        <p>Sebaliknya, Iteratif hanya melakukan operasi aritmatika (ADD, MUL) di register CPU tanpa pindah konteks.</p>
    </div>
    """, unsafe_allow_html=True)

with c6:
    st.markdown("""
    <div class="desc-container">
        <h4>📊 Kesimpulan Grafik</h4>
        <p>Dari visualisasi grafik Line Chart di atas:</p>
        <ul>
            <li><b>Linearity:</b> Garis lurus mengonfirmasi O(n).</li>
            <li><b>Gap:</b> Jarak vertikal antara garis hijau dan merah adalah representasi visual dari "biaya" overhead rekursi.</li>
            <li><b>Rekomendasi:</b> Gunakan Iteratif untuk perhitungan deret sederhana. Gunakan Rekursif untuk struktur data hierarkis (Tree) atau algoritma Backtracking.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)