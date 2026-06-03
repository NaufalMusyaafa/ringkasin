import streamlit as st
from groq import Groq

# Setup client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# Konfigurasi halaman
st.set_page_config(
    page_title="Summarization & QA Berita Indonesia",
    page_icon="🗞️",
    layout="wide"
)

# Header
st.title("🗞️ Summarization & QA Berita Indonesia")
st.markdown("Masukkan artikel berita berbahasa Indonesia, lalu pilih fitur yang ingin digunakan.")
st.divider()

# Input artikel
artikel = st.text_area(
    "📝 Paste artikel berita di sini:",
    height=250,
    placeholder="Masukkan teks artikel berita berbahasa Indonesia..."
)

# Fungsi summarization
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

# Fungsi QA
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

# Tab untuk dua fitur
tab1, tab2 = st.tabs(["📄 Summarization", "❓ Question Answering"])

with tab1:
    st.subheader("Ringkasan Artikel")
    if st.button("🔍 Ringkas Artikel", type="primary", key="btn_summary"):
        if not artikel.strip():
            st.warning("⚠️ Silakan masukkan artikel terlebih dahulu.")
        else:
            with st.spinner("Sedang meringkas artikel..."):
                hasil = summarize_artikel(artikel)
            st.success("✅ Ringkasan berhasil dibuat!")
            st.markdown("### Hasil Ringkasan")
            st.info(hasil)

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
            with st.spinner("Sedang mencari jawaban..."):
                jawaban = jawab_pertanyaan(artikel, pertanyaan)
            st.success("✅ Jawaban ditemukan!")
            st.markdown("### Jawaban")
            st.info(jawaban)

st.divider()
st.caption("Project NLP — Implementasi LLM untuk Summarization & QA Berita Indonesia")