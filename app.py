import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from groq import Groq

# ─── Setup client (tidak diubah) ─────────────────────────────────────────────
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ─── Konfigurasi halaman ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="Ringkasin — Summarization & QA Berita Indonesia",
    page_icon="🗞️",
    layout="wide"
)

# ─── Custom CSS untuk tampilan premium ────────────────────────────────────────
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Font global — background dibiarkan default theme Streamlit */
    .stApp {
        font-family: 'Inter', sans-serif;
    }

    /* Header styling */
    h1 {
        background: linear-gradient(135deg, #1a73e8 0%, #6c5ce7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700 !important;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    [data-testid="stSidebar"] * {
        color: #e0e0e0 !important;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
    }

    /* Primary button styling */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #1a73e8 0%, #6c5ce7 100%);
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1.5rem;
        font-weight: 600;
        letter-spacing: 0.3px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(26, 115, 232, 0.3);
    }
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(26, 115, 232, 0.45);
    }

    /* Card hasil output — summarization (biru) */
    .result-card-summary {
        background: linear-gradient(135deg, #ebf5ff 0%, #f0f4ff 100%);
        border-left: 5px solid #1a73e8;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        line-height: 1.7;
        font-size: 0.95rem;
        color: #1a1a2e;
    }
    .result-card-summary .card-header {
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: 700;
        font-size: 1.05rem;
        color: #1a73e8;
        margin-bottom: 0.75rem;
    }

    /* Card hasil output — QA (hijau) */
    .result-card-qa {
        background: linear-gradient(135deg, #e8faf0 0%, #f0fdf4 100%);
        border-left: 5px solid #00b894;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
        line-height: 1.7;
        font-size: 0.95rem;
        color: #1a1a2e;
    }
    .result-card-qa .card-header {
        display: flex;
        align-items: center;
        gap: 8px;
        font-weight: 700;
        font-size: 1.05rem;
        color: #00b894;
        margin-bottom: 0.75rem;
    }

    /* Metric card */
    .metric-container {
        display: flex;
        gap: 1rem;
        margin-top: 1rem;
    }
    .metric-card {
        background: #ffffff;
        border-radius: 10px;
        padding: 1rem 1.25rem;
        flex: 1;
        text-align: center;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
        border: 1px solid #e8ecf1;
    }
    .metric-card .metric-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #1a73e8;
    }
    .metric-card .metric-label {
        font-size: 0.78rem;
        color: #6b7280;
        margin-top: 4px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Scraping success card */
    .scrape-success {
        background: linear-gradient(135deg, #e8faf0, #f0fdf4);
        border-left: 4px solid #00b894;
        border-radius: 10px;
        padding: 1rem 1.25rem;
        margin: 0.5rem 0;
        font-size: 0.88rem;
        color: #1a1a2e;
    }

    /* Text area styling */
    .stTextArea textarea {
        border-radius: 10px !important;
        border: 1.5px solid #d1d5db !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.92rem !important;
    }
    .stTextArea textarea:focus {
        border-color: #1a73e8 !important;
        box-shadow: 0 0 0 3px rgba(26, 115, 232, 0.15) !important;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
    }

    /* Radio button horizontal */
    .stRadio > div {
        flex-direction: row !important;
        gap: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🗞️ Ringkasin")
    st.markdown(
        "Aplikasi **Summarization** & **Question Answering** untuk artikel "
        "berita berbahasa Indonesia, didukung oleh Large Language Model."
    )

    st.markdown("---")

    st.markdown("### 🤖 Model yang Digunakan")
    st.markdown(
        "**LLaMA 3.3 70B** *(Versatile)*  \n"
        "Diakses melalui Groq API dengan latensi rendah."
    )

    st.markdown("---")

    st.markdown("### 📖 Cara Penggunaan")
    st.markdown(
        "1. **Masukkan artikel** — ketik manual atau scraping dari URL\n"
        "2. **Pilih fitur** — tab *Summarization* atau *Question Answering*\n"
        "3. **Klik tombol** — dan hasil akan muncul dalam hitungan detik"
    )

    st.markdown("---")
    st.caption("© 2026 — Project NLP | Ringkasin")

# ─── Header utama ────────────────────────────────────────────────────────────
st.title("🗞️ Ringkasin — Summarization & QA Berita")
st.markdown("Masukkan artikel berita berbahasa Indonesia, lalu pilih fitur yang ingin digunakan.")
st.divider()

# ─── Pilihan input: Manual vs Scraping ────────────────────────────────────────
input_mode = st.radio(
    "Pilih metode input artikel:",
    ["✍️ Input Manual", "🔗 Scraping dari URL"],
    horizontal=True
)

# Variabel untuk menampung teks hasil scraping
scraped_text = ""

if input_mode == "🔗 Scraping dari URL":
    # ── Input URL dan tombol scraping ─────────────────────────────────────────
    url_input = st.text_input(
        "🌐 Masukkan URL artikel berita:",
        placeholder="https://www.contoh-berita.com/artikel/..."
    )

    if st.button("📥 Ambil Artikel", type="primary", key="btn_scrape"):
        if not url_input.strip():
            st.error("❌ Silakan masukkan URL terlebih dahulu.")
        else:
            # Validasi format URL sederhana
            url_pattern = re.compile(
                r'^https?://'
                r'(?:[a-zA-Z0-9\-]+\.)+[a-zA-Z]{2,}'
                r'(?:/[^\s]*)?$'
            )
            if not url_pattern.match(url_input.strip()):
                st.error("❌ Format URL tidak valid. Pastikan URL diawali dengan http:// atau https://")
            else:
                try:
                    with st.spinner("🔄 Mengambil konten dari URL... Mohon tunggu sebentar."):
                        # Request dengan User-Agent header agar tidak diblokir
                        headers = {
                            "User-Agent": (
                                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                "AppleWebKit/537.36 (KHTML, like Gecko) "
                                "Chrome/120.0.0.0 Safari/537.36"
                            )
                        }
                        response = requests.get(
                            url_input.strip(),
                            headers=headers,
                            timeout=15
                        )
                        response.raise_for_status()

                        # Parsing HTML dan ambil semua tag <p>
                        soup = BeautifulSoup(response.text, "html.parser")
                        paragraphs = soup.find_all("p")
                        raw_text = " ".join(p.get_text() for p in paragraphs)

                        # Bersihkan whitespace berlebih
                        cleaned_text = re.sub(r'\s+', ' ', raw_text).strip()

                        if not cleaned_text:
                            st.error(
                                "❌ Tidak ditemukan konten teks pada halaman ini. "
                                "Coba URL artikel yang berbeda."
                            )
                        else:
                            scraped_text = cleaned_text
                            st.session_state["scraped_text"] = cleaned_text
                            # Preview hasil scraping
                            preview = cleaned_text[:150] + ("..." if len(cleaned_text) > 150 else "")
                            st.success("✅ Artikel berhasil diambil!")
                            st.markdown(
                                f'<div class="scrape-success">'
                                f'<strong>Preview:</strong> {preview}'
                                f'</div>',
                                unsafe_allow_html=True
                            )

                except requests.exceptions.ConnectionError:
                    st.error(
                        "❌ Gagal terhubung ke server. Periksa koneksi internet Anda "
                        "atau pastikan URL dapat diakses."
                    )
                except requests.exceptions.Timeout:
                    st.error(
                        "❌ Koneksi timeout. Server terlalu lama merespons. "
                        "Coba lagi nanti."
                    )
                except requests.exceptions.HTTPError as e:
                    st.error(f"❌ Server mengembalikan error: {e.response.status_code}. Coba URL lain.")
                except requests.exceptions.RequestException as e:
                    st.error(f"❌ Terjadi kesalahan saat mengambil artikel: {str(e)}")

    # Ambil teks dari session state jika sudah pernah di-scrape
    if "scraped_text" in st.session_state:
        scraped_text = st.session_state["scraped_text"]

# ─── Text area input artikel ─────────────────────────────────────────────────
# Jika mode scraping, isi default dengan hasil scraping
default_value = scraped_text if input_mode == "🔗 Scraping dari URL" else ""

artikel = st.text_area(
    "📝 Artikel berita:",
    value=default_value,
    height=250,
    placeholder="Masukkan teks artikel berita berbahasa Indonesia..."
)

# ─── Fungsi summarization (logika tidak diubah) ──────────────────────────────
def summarize_artikel(teks):
    prompt = f"""Kamu adalah asisten peringkas berita berbahasa Indonesia.
Ringkas artikel berita berikut dalam 3-5 kalimat yang padat dan informatif.
Gunakan bahasa Indonesia yang baik. Hanya tulis ringkasannya saja.

Artikel:
{teks[:3000]}

Ringkasan:"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=256,
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

# ─── Fungsi QA (logika tidak diubah) ─────────────────────────────────────────
def jawab_pertanyaan(teks, pertanyaan):
    prompt = f"""Jawab pertanyaan berikut berdasarkan artikel yang diberikan.
Jawab singkat, faktual, dan hanya berdasarkan informasi yang ada di artikel.
Jika jawaban tidak ada di artikel, katakan "Informasi tidak tersedia dalam artikel."

Artikel:
{teks[:3000]}

Pertanyaan: {pertanyaan}

Jawaban:"""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

# ─── Helper: hitung jumlah kata ──────────────────────────────────────────────
def hitung_kata(teks):
    return len(teks.split())

# ─── Tab untuk dua fitur ─────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["📄 Summarization", "❓ Question Answering"])

with tab1:
    st.subheader("Ringkasan Artikel")
    if st.button("🔍 Ringkas Artikel", type="primary", key="btn_summary"):
        if not artikel.strip():
            st.warning("⚠️ Silakan masukkan artikel terlebih dahulu.")
        else:
            with st.spinner("🧠 AI sedang membaca dan meringkas artikel Anda... Mohon tunggu."):
                hasil = summarize_artikel(artikel)

            # Card hasil ringkasan (biru)
            st.markdown(
                f"""
                <div class="result-card-summary">
                    <div class="card-header">📋 Hasil Ringkasan</div>
                    {hasil}
                </div>
                """,
                unsafe_allow_html=True
            )

            # Metrik kompresi
            kata_asli = hitung_kata(artikel)
            kata_ringkasan = hitung_kata(hasil)
            persen_kompresi = round((1 - kata_ringkasan / kata_asli) * 100, 1) if kata_asli > 0 else 0

            st.markdown(
                f"""
                <div class="metric-container">
                    <div class="metric-card">
                        <div class="metric-value">{kata_asli:,}</div>
                        <div class="metric-label">Kata Artikel Asli</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{kata_ringkasan:,}</div>
                        <div class="metric-label">Kata Ringkasan</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{persen_kompresi}%</div>
                        <div class="metric-label">Kompresi</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

with tab2:
    st.subheader("Tanya Jawab Berdasarkan Artikel")
    pertanyaan = st.text_input(
        "❓ Masukkan pertanyaan:",
        placeholder="Contoh: Siapa yang terlibat dalam kejadian ini?"
    )
    if st.button("💬 Jawab Pertanyaan", type="primary", key="btn_qa"):
        if not artikel.strip():
            st.warning("⚠️ Silakan masukkan artikel terlebih dahulu.")
        elif not pertanyaan.strip():
            st.warning("⚠️ Silakan masukkan pertanyaan terlebih dahulu.")
        else:
            with st.spinner("🧠 AI sedang menganalisis artikel untuk menjawab pertanyaan Anda..."):
                jawaban = jawab_pertanyaan(artikel, pertanyaan)

            # Card hasil QA (hijau)
            st.markdown(
                f"""
                <div class="result-card-qa">
                    <div class="card-header">💡 Jawaban</div>
                    {jawaban}
                </div>
                """,
                unsafe_allow_html=True
            )

# ─── Footer ──────────────────────────────────────────────────────────────────
st.divider()
st.caption("Project NLP — Implementasi LLM untuk Summarization & QA Berita Indonesia | Powered by LLaMA 3.3 70B via Groq")