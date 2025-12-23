import streamlit as st
import matplotlib
import matplotlib.pyplot as plt
import time
import sys

matplotlib.use('Agg')

sys.setrecursionlimit(10**6)
sys.set_int_max_str_digits(0)

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

st.title("🌐 Perbandingan Iteratif vs Rekursif")
st.subheader("Studi Kasus: Menghitung Jumlah Deret Geometri (Sn)")

st.info("""
ℹ️ **Info:** Aplikasi ini menghitung **Jumlah Total ($S_n$)** dari barisan geometri.
Contoh: Jika a=2, r=3, n=3. Maka $2 + 6 + 18 = 26$.
""")

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

    start_iter = time.perf_counter()
    hasil_iter = hitung_deret_iteratif(a, r, n)
    end_iter = time.perf_counter()
    waktu_iter = (end_iter - start_iter) * 1000

    start_rec = time.perf_counter()
    hasil_rec = hitung_deret_rekursif(a, r, n)
    end_rec = time.perf_counter()
    waktu_rec = (end_rec - start_rec) * 1000

    st.success(f"✅ **Iteratif:** S({n}) = {hasil_iter} | Waktu = {waktu_iter:.6f} ms")
    st.error(f"🔁 **Rekursif:** S({n}) = {hasil_rec} | Waktu = {waktu_rec:.6f} ms")

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

st.markdown("---")
tampilkan_grafik = st.checkbox(f"Tampilkan grafik runtime (n = 1 hingga {n})")

if tampilkan_grafik:
    st.write(f"Memproses data grafik untuk n=1 s.d {n}...")

    ns = range(1, n + 1)
    times_iter = []
    times_rec = []

    progress_bar = st.progress(0)

    for i, val_n in enumerate(ns):
        t0 = time.perf_counter()
        hitung_deret_iteratif(a, r, val_n)
        times_iter.append((time.perf_counter() - t0) * 1000)

        t0 = time.perf_counter()
        hitung_deret_rekursif(a, r, val_n)
        times_rec.append((time.perf_counter() - t0) * 1000)

        progress_bar.progress((i + 1) / len(ns))

    fig2, ax2 = plt.subplots(figsize=(10, 5))

    ax2.plot(ns, times_iter, label='Iteratif', color='green', marker='o', linestyle='-')
    ax2.plot(ns, times_rec, label='Rekursif', color='red', marker='x', linestyle='--')

    ax2.set_xlabel('Nilai n (Jumlah Suku)')
    ax2.set_ylabel('Waktu (ms)')
    ax2.set_title('Grafik Perbandingan: Runtime vs Input Size (Deret)')
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.6)

    st.pyplot(fig2)

st.markdown("---")
st.subheader("📝 Penjelasan & Analisis Logika")

st.markdown("""
<style>
    .desc-container {
        background-color: transparent;
        border: 1px solid rgba(41, 182, 246, 0.3);
        color: inherit;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;

        height: 480px !important;
        overflow-y: auto;

        display: flex;
        flex-direction: column;
    }

    .desc-container::-webkit-scrollbar {
        width: 6px;
    }
    .desc-container::-webkit-scrollbar-thumb {
        background-color: rgba(41, 182, 246, 0.3);
        border-radius: 4px;
    }

    .desc-container h4 {
        margin-bottom: 12px;
        font-size: 1.1rem;
        font-weight: 700;
        color: #29B6F6 !important;
        border-bottom: 1px solid rgba(41, 182, 246, 0.2);
        padding-bottom: 10px;

        min-height: 50px;
        display: flex;
        align-items: center;
    }

    .desc-container p, .desc-container li {
        font-size: 0.85rem;
        line-height: 1.5;
        opacity: 0.9;
        margin-bottom: 8px;
    }

    .desc-container ul, .desc-container ol {
        padding-left: 18px;
        margin-top: 5px;
        margin-bottom: 10px;
    }

    .desc-container code {
        background-color: rgba(41, 182, 246, 0.1);
        padding: 2px 5px;
        border-radius: 4px;
        font-family: monospace;
        color: #B3E5FC;
        font-size: 0.8rem;
    }

    @media (max-width: 768px) {
        .desc-container {
            height: auto !important;
        }
    }
</style>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="desc-container">
        <h4>📖 Konsep Deret Geometri</h4>
        <p>Kode ini menghitung <b>Jumlah Total (Sn)</b>, yaitu akumulasi penjumlahan dari suku pertama hingga suku ke-n.</p>
        <p><b>Definisi:</b><br>
        Deret di mana rasio antara dua suku berturutan selalu tetap (r).</p>
        <p><b>Rumus:</b> $S_n = a(r^n - 1) / (r - 1)$ (untuk r>1)</p>
        <p><b>Variabel:</b></p>
        <ul>
            <li><code>a</code>: Suku awal.</li>
            <li><code>r</code>: Rasio pengali.</li>
            <li><code>n</code>: Jumlah iterasi.</li>
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