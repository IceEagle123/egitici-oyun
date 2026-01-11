import streamlit as st
import random

# Sayfa Ayarları
st.set_page_config(page_title="Eğitici Oyun", page_icon="🎮", layout="centered")

# ---------------- SESSION STATE ----------------
if 'sayfa' not in st.session_state:
    st.session_state.sayfa = 'menu'
if 'puan' not in st.session_state:
    st.session_state.puan = 0
if 'hak' not in st.session_state:
    st.session_state.hak = 3
if 'isim' not in st.session_state:
    st.session_state.isim = "Oyuncu"
if 'soru_metni' not in st.session_state:
    st.session_state.soru_metni = ""
if 'dogru_cevap' not in st.session_state:
    st.session_state.dogru_cevap = None
if 'mesaj' not in st.session_state:
    st.session_state.mesaj = ""
if 'oyun_turu' not in st.session_state:
    st.session_state.oyun_turu = ""
if 'calisma_turu' not in st.session_state:
    st.session_state.calisma_turu = ""
if 'zorluk' not in st.session_state:
    st.session_state.zorluk = "Kolay"

# ---------------- FONKSİYONLAR ----------------
def yeni_soru_olustur():
    st.session_state.mesaj = ""

    if st.session_state.oyun_turu == 'matematik':

        # Zorluk ayarı
        if st.session_state.zorluk == "Kolay":
            alt, ust = 1, 10
        elif st.session_state.zorluk == "Orta":
            alt, ust = 10, 50
        else:
            alt, ust = 50, 100

        islem = random.randint(1, 4)

        if islem == 1:  # Toplama
            s1, s2 = random.randint(alt, ust), random.randint(alt, ust)
            st.session_state.soru_metni = f"{s1} + {s2} = ?"
            st.session_state.dogru_cevap = s1 + s2

        elif islem == 2:  # Çıkarma
            s1 = random.randint(alt, ust)
            s2 = random.randint(1, s1)
            st.session_state.soru_metni = f"{s1} - {s2} = ?"
            st.session_state.dogru_cevap = s1 - s2

        elif islem == 3:  # Çarpma
            s1, s2 = random.randint(2, 10), random.randint(2, 10)
            st.session_state.soru_metni = f"{s1} x {s2} = ?"
            st.session_state.dogru_cevap = s1 * s2

        else:  # Bölme
            s2 = random.randint(2, 10)
            cevap = random.randint(2, 10)
            s1 = s2 * cevap
            st.session_state.soru_metni = f"{s1} ÷ {s2} = ?"
            st.session_state.dogru_cevap = cevap

    elif st.session_state.oyun_turu == 'turkce':
        kelimeler = [
            ("Siyah", "Kara", "Eş"), ("Beyaz", "Ak", "Eş"), ("Kırmızı", "Al", "Eş"),
            ("Okul", "Mektep", "Eş"), ("Doktor", "Hekim", "Eş"),
            ("Büyük", "Küçük", "Zıt"), ("Uzun", "Kısa", "Zıt"),
            ("Sıcak", "Soğuk", "Zıt"), ("Gel", "Git", "Zıt"),
            ("Zengin", "Fakir", "Zıt"), ("Genç", "Yaşlı", "Zıt"),
            ("İyi", "Kötü", "Zıt")
        ]
        kelime, cevap, tur = random.choice(kelimeler)
        st.session_state.dogru_cevap = cevap
        if tur == "Eş":
            st.session_state.soru_metni = f"'{kelime}' kelimesinin EŞ anlamlısı nedir?"
        else:
            st.session_state.soru_metni = f"'{kelime}' kelimesinin ZIT anlamlısı nedir?"

def cevap_kontrol():
    cevap = st.session_state.cevap_input
    if not cevap:
        return

    dogru = False
    if st.session_state.oyun_turu == 'matematik':
        try:
            dogru = int(cevap) == st.session_state.dogru_cevap
        except:
            dogru = False
    else:
        dogru = cevap.lower().replace("ı", "i") == st.session_state.dogru_cevap.lower().replace("ı", "i")

    if dogru:
        st.session_state.puan += 10
        st.session_state.mesaj = "✅ Harika! Doğru Bildin!"
        yeni_soru_olustur()
    else:
        st.session_state.hak -= 1
        st.session_state.mesaj = f"❌ Yanlış! Doğru cevap: {st.session_state.dogru_cevap}"

def oyunu_baslat(tur):
    st.session_state.oyun_turu = tur
    st.session_state.sayfa = 'oyun'
    st.session_state.puan = 0
    yeni_soru_olustur()

def ana_menu():
    st.session_state.sayfa = 'menu'

def calisma_baslat(tur):
    st.session_state.calisma_turu = tur
    st.session_state.sayfa = 'calisma'

# ---------------- ARAYÜZ ----------------
if st.session_state.sayfa == 'menu':
    st.title("Eğitici Oyun Menüsü 🎓")

    st.session_state.isim = st.text_input("İsminiz:", st.session_state.isim)
    st.session_state.hak = st.selectbox("Hak Sayısı:", [3, 5, 10])
    st.session_state.zorluk = st.selectbox("Zorluk Seviyesi:", ["Kolay", "Orta", "Zor"])

    if st.button("MATEMATİK OYUNU ➕"):
        oyunu_baslat("matematik")
    if st.button("TÜRKÇE OYUNU 📚"):
        oyunu_baslat("turkce")

elif st.session_state.sayfa == 'oyun':
    st.write(f"👤 {st.session_state.isim} | 🏆 {st.session_state.puan} | ❤️ {st.session_state.hak}")

    if st.session_state.hak > 0:
        st.header(st.session_state.soru_metni)
        with st.form("cevap_form", clear_on_submit=True):
            st.text_input("Cevabınız:", key="cevap_input")
            if st.form_submit_button("Cevapla"):
                cevap_kontrol()
                st.rerun()

        if st.session_state.mesaj:
            st.info(st.session_state.mesaj)
    else:
        st.error("Oyun Bitti!")
        if st.button("Ana Menü"):
            ana_menu()
            st.rerun()
