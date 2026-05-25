import streamlit as st
import os
import tempfile
import time
from google import genai
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Meeting Summarizer", page_icon="🎙️", layout="centered")

st.title("🎙️ AI Voice Meeting Summarizer")
st.markdown("Unggah rekaman audio (MP3, WAV, M4A) dari rapat, *interview*, atau kuliah. AI akan secara otomatis mendengarkan dan membuatkan **Notulensi, Ringkasan, dan Daftar Tugas (Action Items)**!")

# Periksa ketersediaan API Key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("⚠️ GEMINI_API_KEY tidak ditemukan di file .env! Silakan tambahkan terlebih dahulu.")
    st.stop()

# Inisialisasi klien Gemini SDK
client = genai.Client(api_key=api_key)

uploaded_file = st.file_uploader("Upload Rekaman Audio", type=["mp3", "wav", "m4a", "ogg"])

if uploaded_file is not None:
    st.audio(uploaded_file)
    
    if st.button("Proses dengan AI"):
        with st.spinner("🤖 AI sedang memproses... (Bisa memakan waktu 10-30 detik tergantung ukuran file)"):
            try:
                # 1. Simpan audio sementara ke dalam sistem
                file_extension = uploaded_file.name.split('.')[-1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name
                
                # 2. Upload file ke server Google AI Studio menggunakan File API
                st.info("Mengunggah audio ke mesin AI...")
                audio_file = client.files.upload(file=tmp_path)
                
                # Tunggu hingga status pemrosesan file selesai di sisi server
                while audio_file.state.name == "PROCESSING":
                    time.sleep(2)
                    audio_file = client.files.get(name=audio_file.name)
                
                if audio_file.state.name == "FAILED":
                    st.error("Gagal memproses file audio. Format mungkin rusak atau tidak didukung.")
                    os.unlink(tmp_path)
                    st.stop()

                # 3. Prompting menggunakan Gemini Multimodal (Mendengarkan audio secara langsung)
                st.info("Mendengarkan percakapan dan mengetik notulensi...")
                prompt = """
                Anda adalah asisten notulis profesional tingkat eksekutif.
                Dengarkan rekaman audio ini dengan teliti, lalu buatkan laporan dengan struktur Markdown berikut:
                
                ## 📝 Ringkasan Eksekutif
                (Rangkum secara singkat dan jelas inti dari percakapan)
                
                ## 💡 Poin-poin Penting
                (Buat daftar topik atau diskusi krusial yang dibahas)
                
                ## 🎯 Daftar Tugas (Action Items)
                (Sebutkan siapa yang harus melakukan apa. Jika nama tidak disebutkan, tulis 'Tim')
                
                Gunakan Bahasa Indonesia yang rapi, profesional, dan mudah dibaca. Jika isi audio bukan tentang rapat bisnis, tetap rangkum isinya sebaik mungkin sesuai konteks percakapan.
                """
                
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[audio_file, prompt]
                )
                
                # Hapus file dari server Google dan file sementara lokal demi privasi
                client.files.delete(name=audio_file.name)
                os.unlink(tmp_path)
                
                st.success("✅ Selesai!")
                
                # Tampilkan hasil
                st.divider()
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Terjadi kesalahan teknis: {e}")
