import streamlit as st
from google import genai

# ─────────────────────────────────────────────
# KONFIGURASI HALAMAN
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Customer Service UTPAS",
    page_icon="🎓",
    layout="centered"
)

# ─────────────────────────────────────────────
# SYSTEM PROMPT — PENGETAHUAN TENTANG UTPAS
# ─────────────────────────────────────────────
SYSTEM_PROMPT = """
Kamu adalah **Asisten Virtual Customer Service Universitas Utpadaka Swastika (UTPAS)**.
Jawab semua pertanyaan dengan ramah, informatif, dan profesional dalam Bahasa Indonesia.
Jika pertanyaan di luar konteks UTPAS, arahkan kembali ke topik yang relevan atau sarankan
menghubungi tim kami secara langsung.

---

## INFORMASI UTPAS

### Profil Universitas
- **Nama:** Universitas Utpadaka Swastika (UTPAS)
- **Latar Belakang:** Merupakan penggabungan Sekolah Tinggi Ilmu Ekonomi BISMA LEPISI
  dengan Akademi Sekretari dan Manajemen LEPISI.
- **Visi:** Pendidikan berbasis *technopreneur* yang terkini dan sesuai perkembangan industri.
- **Fokus:** Memadukan teknologi dan kewirausahaan; membentuk wirausaha yang membawa
  kebaikan bagi masyarakat dan lingkungan.
- **Alamat:** Metropolis Town Square Lt. 2, Jl. Hartono Raya Modern,
  Kel. Kelapa Indah, Kota Tangerang 15117, Banten-Indonesia.

### Kontak
- **WhatsApp:** +62 813-8154-1471
- **Telepon:** +62 21 5589161
- **Email:** info@utpas.ac.id
- **Website:** https://utpas.ac.id
- **Pendaftaran:** https://pendaftaran.utpas.ac.id

### Program Studi (S1)
Semua program studi jenjang Sarjana (S1):

**Fakultas Teknologi & Desain:**
1. **Teknologi Informasi** — Pendidikan inovatif di bidang teknologi informasi.
2. **Sistem Informasi** — Program studi unik yang menggabungkan teknologi dan bisnis.
3. **Desain Komunikasi Visual (DKV)** — Cocok bagi yang memiliki minat di bidang desain dan komunikasi visual.

**Fakultas Ekonomi & Bisnis (FEB):**
4. **Akuntansi** — Mempelajari pengukuran, pengungkapan, dan analisis informasi keuangan.
5. **Manajemen** — Dirancang untuk mempersiapkan pemimpin masa depan yang siap menghadapi tantangan dunia kerja.

**Fakultas Hukum (FH):**
6. **Hukum** — Kombinasi sempurna antara teori dan praktik hukum.

### Beasiswa
UTPAS menyediakan beragam beasiswa:
- Beasiswa Kartu Indonesia Pintar Kuliah (KIP-K)
- Beasiswa Prestasi
- Beasiswa Yayasan
- Beasiswa Rumah Ibadah
- Dan beasiswa lainnya

### Pendaftaran Mahasiswa Baru
- Pendaftaran mahasiswa baru dan mahasiswa pindahan dibuka setiap tahun akademik.
- Daftar online di: https://pendaftaran.utpas.ac.id
- Tersedia kesempatan mendapatkan Beasiswa Uang Kuliah bagi pendaftar awal.
- Tersedia program untuk mahasiswa pindahan dari universitas lain.

### Fasilitas & Program Unggulan
- **Metode Belajar:** Fokus pada praktik, kolaborasi, dan pemecahan masalah.
- **Merdeka Belajar:** Mendukung kebebasan akademik dan pengembangan diri.
- **E-Learning:** https://elearning.utpas.ac.id
- **Perpustakaan:** https://perpustakaan.utpas.ac.id
- **Repositori:** https://repositori.utpas.ac.id
- **Jurnal:** https://jurnal.utpas.ac.id
- **SPMI (Penjaminan Mutu):** https://spmi.utpas.ac.id

### Tautan Penting
- Pengumuman: https://pengumuman.utpas.ac.id
- Blog/Tulisan: https://tulisan.utpas.ac.id
- Karier: https://utpas.ac.id/karier/
- Satgas PPKPT (Pencegahan Kekerasan): https://forms.gle/RetukYqzuWqJdTKy9

---

Selalu akhiri jawaban dengan menawarkan bantuan lebih lanjut.
Jika ada pertanyaan yang tidak kamu ketahui jawabannya, sarankan untuk menghubungi
tim UTPAS via WhatsApp +62 813-8154-1471 atau email info@utpas.ac.id.
"""

# ─────────────────────────────────────────────
# AMBIL API KEY DARI st.secrets
# ─────────────────────────────────────────────
# Di Streamlit Community Cloud: tambahkan GOOGLE_API_KEY di menu Secrets
# Di lokal: buat file .streamlit/secrets.toml berisi:
#   GOOGLE_API_KEY = "isi-api-key-kamu"
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except (KeyError, FileNotFoundError):
    GOOGLE_API_KEY = None

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding: 1rem 0 0.5rem;">
    <h1 style="color:#1a3c6e; margin-bottom:0;">🎓 UTPAS</h1>
    <p style="color:#555; font-size:1rem; margin-top:4px;">
        Customer Service — Universitas Utpadaka Swastika
    </p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.image("https://utpas.ac.id/images/logo.svg", width=180)
    st.markdown("---")

    # Jika API key tidak ada di secrets, tampilkan input manual (mode development)
    if not GOOGLE_API_KEY:
        st.subheader("⚙️ Pengaturan")
        manual_key = st.text_input(
            "Google AI API Key",
            type="password",
            help="Masukkan API key untuk mode development lokal"
        )
        if manual_key:
            GOOGLE_API_KEY = manual_key

    reset_button = st.button("🔄 Reset Percakapan")
    st.markdown("---")
    st.markdown("**📞 Kontak UTPAS**")
    st.markdown("📱 [WhatsApp](https://api.whatsapp.com/send/?phone=628131541471)")
    st.markdown("📞 +62 21 5589161")
    st.markdown("📧 info@utpas.ac.id")
    st.markdown("---")
    st.markdown("**🔗 Link Penting**")
    st.markdown("[🌐 Website](https://utpas.ac.id)")
    st.markdown("[📝 Daftar Sekarang](https://pendaftaran.utpas.ac.id)")
    st.markdown("[📢 Pengumuman](https://pengumuman.utpas.ac.id)")
    st.markdown("[📚 E-Learning](https://elearning.utpas.ac.id)")

# ─────────────────────────────────────────────
# VALIDASI API KEY
# ─────────────────────────────────────────────
if not GOOGLE_API_KEY:
    st.info("🔑 API Key belum dikonfigurasi. Hubungi administrator.", icon="ℹ️")
    st.stop()

# ─────────────────────────────────────────────
# INISIALISASI GEMINI CLIENT
# ─────────────────────────────────────────────
if ("genai_client" not in st.session_state) or (
    st.session_state.get("_last_key") != GOOGLE_API_KEY
):
    try:
        st.session_state.genai_client = genai.Client(api_key=GOOGLE_API_KEY)
        st.session_state._last_key = GOOGLE_API_KEY
        st.session_state.pop("chat", None)
        st.session_state.pop("messages", None)
    except Exception as e:
        st.error(f"❌ Gagal menginisialisasi AI: {e}")
        st.stop()

# ─────────────────────────────────────────────
# INISIALISASI CHAT SESSION & RIWAYAT
# ─────────────────────────────────────────────
if "chat" not in st.session_state:
    st.session_state.chat = st.session_state.genai_client.chats.create(
        model="gemini-2.5-flash",
        config={"system_instruction": SYSTEM_PROMPT}
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

# ─────────────────────────────────────────────
# TOMBOL RESET
# ─────────────────────────────────────────────
if reset_button:
    st.session_state.pop("chat", None)
    st.session_state.pop("messages", None)
    st.rerun()

# ─────────────────────────────────────────────
# PESAN SELAMAT DATANG
# ─────────────────────────────────────────────
if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.markdown("""
Halo! 👋 Selamat datang di **Customer Service Universitas Utpadaka Swastika (UTPAS)**!

Saya siap membantu Anda dengan informasi seputar:
- 🎓 Program Studi (Manajemen, Akuntansi, Sistem Informasi, TI, DKV, Hukum)
- 📝 Pendaftaran mahasiswa baru & pindahan
- 💰 Beasiswa yang tersedia
- 📍 Lokasi dan kontak kampus
- 📚 Fasilitas dan layanan akademik

Ada yang bisa saya bantu hari ini? 😊
        """)

# ─────────────────────────────────────────────
# TAMPILKAN RIWAYAT PERCAKAPAN
# ─────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ─────────────────────────────────────────────
# INPUT & RESPONS
# ─────────────────────────────────────────────
prompt = st.chat_input("Tanyakan sesuatu tentang UTPAS...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            with st.spinner("Sedang menjawab..."):
                response = st.session_state.chat.send_message(prompt)
                answer = response.text if hasattr(response, "text") else str(response)
            st.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})

    except Exception as e:
        error_msg = f"⚠️ Terjadi kesalahan: {e}. Silakan coba lagi atau hubungi tim kami di WhatsApp +62 813-8154-1471."
        with st.chat_message("assistant"):
            st.error(error_msg)
        st.session_state.messages.append({"role": "assistant", "content": error_msg})

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#888; font-size:0.8rem;'>"
    "© 2026 Universitas Utpadaka Swastika · "
    "<a href='https://utpas.ac.id' target='_blank'>utpas.ac.id</a>"
    "</p>",
    unsafe_allow_html=True
)