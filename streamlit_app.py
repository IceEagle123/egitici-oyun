import streamlit as st
import random

# Sayfa Ayarları
st.set_page_config(page_title="Eğitici Oyun", page_icon="🎮", layout="centered")

# --- Session State (Değişkenler - Hafıza) ---
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

# --- Fonksiyonlar ---
def yeni_soru_olustur():
    st.session_state.mesaj = ""
    
    if st.session_state.oyun_turu == 'matematik':
        islem = random.randint(1, 4)
        if islem == 1: # Toplama
            s1, s2 = random.randint(10, 50), random.randint(10, 50)
            st.session_state.soru_metni = f"{s1} + {s2} = ?"
            st.session_state.dogru_cevap = s1 + s2
        elif islem == 2: # Çıkarma
            s1 = random.randint(20, 60)
            s2 = random.randint(1, s1)
            st.session_state.soru_metni = f"{s1} - {s2} = ?"
            st.session_state.dogru_cevap = s1 - s2
        elif islem == 3: # Çarpma
            s1, s2 = random.randint(2, 10), random.randint(2, 10)
            st.session_state.soru_metni = f"{s1} x {s2} = ?"
            st.session_state.dogru_cevap = s1 * s2
        elif islem == 4: # Bölme
            s2 = random.randint(2, 10)
            cevap = random.randint(2, 10)
            s1 = s2 * cevap
            st.session_state.soru_metni = f"{s1} ÷ {s2} = ?"
            st.session_state.dogru_cevap = cevap

    elif st.session_state.oyun_turu == 'turkce':
        kelimeler = [
            ("Siyah", "Kara", "Eş"), ("Beyaz", "Ak", "Eş"), ("Kırmızı", "Al", "Eş"),
            ("Okul", "Mektep", "Eş"), ("Doktor", "Hekim", "Eş"), ("Büyük", "Küçük", "Zıt"), 
            ("Uzun", "Kısa", "Zıt"), ("Sıcak", "Soğuk", "Zıt"), ("Gel", "Git", "Zıt"),
            ("Zengin", "Fakir", "Zıt"), ("Genç", "Yaşlı", "Zıt"), ("İyi", "Kötü", "Zıt")
        ]
        secilen = random.choice(kelimeler)
        kelime, cevap, tur = secilen
        st.session_state.dogru_cevap = cevap
        if tur == "Eş":
            st.session_state.soru_metni = f"'{kelime}' kelimesinin EŞ anlamlısı nedir?"
        else:
            st.session_state.soru_metni = f"'{kelime}' kelimesinin ZIT anlamlısı nedir?"

def cevap_kontrol():
    kullanici_cevabi = st.session_state.cevap_input
    if not kullanici_cevabi: return

    dogru = False
    if st.session_state.oyun_turu == 'matematik':
        try:
            if int(kullanici_cevabi) == st.session_state.dogru_cevap:
                dogru = True
        except: pass
    else:
        # Türkçe kontrolü (küçük harf duyarsız)
        if str(kullanici_cevabi).lower().replace('ı','i') == str(st.session_state.dogru_cevap).lower().replace('ı','i'):
            dogru = True
    
    if dogru:
        st.session_state.puan += 10
        st.session_state.mesaj = "✅ Harika! Doğru Bildin!"
        yeni_soru_olustur()
    else:
        st.session_state.hak -= 1
        st.session_state.mesaj = f"❌ Yanlış! Doğru cevap: {st.session_state.dogru_cevap}"
        if st.session_state.hak <= 0:
            st.session_state.mesaj = "💀 Oyun Bitti!"

def oyunu_baslat(tur):
    st.session_state.oyun_turu = tur
    st.session_state.sayfa = 'oyun'
    st.session_state.puan = 0
    # Hak session'dan geliyor
    yeni_soru_olustur()

def ana_menu():
    st.session_state.sayfa = 'menu'

def calisma_baslat(tur):
    st.session_state.calisma_turu = tur
    st.session_state.sayfa = 'calisma'

def hakkinda_ac():
    st.session_state.sayfa = 'hakkinda'

# --- Arayüz Tasarımı ---

if st.session_state.sayfa == 'menu':
    st.title("Eğitici Oyun Menüsü 🎓")
    
    st.session_state.isim = st.text_input("İsminiz:", value=st.session_state.isim)
    st.session_state.hak = st.selectbox("Hak Sayısı (Can):", [3, 5, 10])
    
    st.write("---")
    st.write("Profil Fotoğrafı (İsteğe Bağlı):")
    img = st.camera_input("Kamerayı Aç")
    if img:
        st.success("Fotoğraf alındı!")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("MATEMATİK OYUNU ➕", use_container_width=True):
            oyunu_baslat('matematik')
        if st.button("ÇARPIM TABLOSU 🔢", use_container_width=True):
            calisma_baslat('matematik')
    with col2:
        if st.button("TÜRKÇE OYUNU 📚", use_container_width=True):
            oyunu_baslat('turkce')
        if st.button("KELİME LİSTESİ 📖", use_container_width=True):
            calisma_baslat('turkce')
            
    st.write("")
    if st.button("HAKKINDA ℹ️", use_container_width=True):
        hakkinda_ac()

elif st.session_state.sayfa == 'oyun':
    # Üst Bilgi Çubuğu
    c1, c2, c3 = st.columns(3)
    c1.write(f"👤 **{st.session_state.isim}**")
    c2.write(f"🏆 Puan: **{st.session_state.puan}**")
    c3.write(f"❤️ Hak: **{st.session_state.hak}**")
    
    st.markdown("---")
    
    if st.session_state.hak > 0:
        st.header(st.session_state.soru_metni)
        
        # Form kullanarak enter ile göndermeyi sağla
        with st.form("cevap_formu", clear_on_submit=True):
            st.text_input("Cevabınız:", key="cevap_input")
            submitted = st.form_submit_button("CEVAPLA")
            if submitted:
                cevap_kontrol()
                st.rerun() # Sayfayı yenile
        
        if st.session_state.mesaj:
            if "✅" in st.session_state.mesaj:
                st.success(st.session_state.mesaj)
            else:
                st.error(st.session_state.mesaj)
                
        if st.button("PAS GEÇ"):
            yeni_soru_olustur()
            st.rerun()
            
    else:
        st.error("Oyun Bitti! Haklarınız tükendi.")
        if st.button("YENİDEN OYNA"):
            ana_menu()
            st.rerun()

    st.markdown("---")
    if st.button("🔙 Ana Menüye Dön"):
        ana_menu()
        st.rerun()

elif st.session_state.sayfa == 'calisma':
    if st.session_state.calisma_turu == 'matematik':
        st.header("Çarpım Tablosu 🔢")
        st.info("Ezberlemek istediğin sayının üzerine tıkla!")
        
        # 1'den 10'a kadar olanlar için açılır kapanır liste
        for i in range(1, 11):
            with st.expander(f"{i}'ler Çarpım Tablosu"):
                for j in range(1, 11):
                    st.write(f"{i} x {j} = {i*j}")
                    
    elif st.session_state.calisma_turu == 'turkce':
        st.header("Kelime Listesi 📖")
        st.write("Eş ve Zıt anlamlı kelimeler:")
        
        # Kelime listesi verisi
        kelimeler = [
            ("Siyah", "Kara", "Eş"), ("Beyaz", "Ak", "Eş"), ("Kırmızı", "Al", "Eş"),
            ("Okul", "Mektep", "Eş"), ("Doktor", "Hekim", "Eş"), ("Büyük", "Küçük", "Zıt"), 
            ("Uzun", "Kısa", "Zıt"), ("Sıcak", "Soğuk", "Zıt"), ("Gel", "Git", "Zıt"),
            ("Zengin", "Fakir", "Zıt"), ("Genç", "Yaşlı", "Zıt"), ("İyi", "Kötü", "Zıt")
        ]
        
        # Tablo oluşturma (Markdown ile)
        tablo = "| Kelime | Karşılığı | Türü |\n|---|---|---|\n"
        for k, c, t in kelimeler:
            tur_ikon = "🔄 Eş" if t == "Eş" else "↔️ Zıt"
            tablo += f"| {k} | {c} | {tur_ikon} |\n"
        
        st.markdown(tablo)

    st.markdown("---")
    if st.button("🔙 Ana Menüye Dön"):
        ana_menu()
        st.rerun()

elif st.session_state.sayfa == 'hakkinda':
    st.header("Hakkında ℹ️")
    st.info("Bu uygulama çocukların eğitimine katkı sağlamak amacıyla geliştirilmiştir.")
    
    st.write("""
    **Özellikler:**
    - ➕ **Matematik Oyunu:** Toplama, çıkarma, çarpma ve bölme işlemleri.
    - 📚 **Türkçe Oyunu:** Eş ve zıt anlamlı kelimeler.
    - 🔢 **Çarpım Tablosu:** Ezberlemek için interaktif tablo.
    - 📖 **Kelime Listesi:** Çalışmak için kelime listesi.
    """)
    
    st.write("---")
    st.subheader("Yapımcı")
    st.write("👨‍💻 **Ege Kağan Köse**")
    st.write("📸 **Instagram:** [kose_egekagan](https://www.instagram.com/kose_egekagan)")
    
    st.write("---")
    if st.button("🔙 Ana Menüye Dön"):
        ana_menu()
        st.rerun()

# Alt Bilgi
st.markdown("---")

st.caption("**Yapımcı: Ege Kağan Köse**")

