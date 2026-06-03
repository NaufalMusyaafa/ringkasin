# 🗞️ Summarization & QA Berita Indonesia

Project NLP untuk meringkas dan menjawab pertanyaan dari artikel berita berbahasa Indonesia menggunakan LLM (LLaMA 3.3 via Groq API).

## Fitur
- 📄 **Summarization** — Meringkas artikel berita dalam 3-5 kalimat
- ❓ **Question Answering** — Menjawab pertanyaan berdasarkan isi artikel

## Tech Stack
- **LLM**: LLaMA 3.3 70B via Groq API
- **Frontend**: Streamlit
- **Dataset Evaluasi**: IndoSum

## Cara Menjalankan

### 1. Clone repository
```bash
git clone https://github.com/username/nama-repo.git
cd nama-repo
```

### 2. Buat virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Install library
```bash
pip install -r requirements.txt
```

### 4. Setup API Key
Buat file `.streamlit/secrets.toml` lalu isi:
```toml
GROQ_API_KEY = "api_key_groq_kamu"
```
> API key Groq bisa didapat gratis di [console.groq.com](https://console.groq.com)

### 5. Jalankan
```bash
streamlit run app.py
```

## Anggota Kelompok
- Nama 1
- Nama 2  
- Nama 3