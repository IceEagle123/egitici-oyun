# ============================================================
# EĞİTİCİ OYUN PLATFORMU - ULTRA SÜRÜM
# Yapımcı: Ege Kağan Köse
# Streamlit | Python
# ============================================================
OPENAI_API_KEY="sk-xxxxxxxx"
import streamlit as st
from openai import OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
import random
import time
import unicodedata
from datetime import datetime
def openai_soru_uret(ders, zorluk):
    prompt = f"""
    {ders} dersi için {zorluk} seviyesinde,
    tek cevaplı, kısa bir soru üret.
    Sadece soru ve cevabı JSON olarak döndür.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    icerik = response.choices[0].message.content

    try:
        data = eval(icerik)
        return data["soru"], data["cevap"]
    except:
        return "2 + 2 = ?", 4
# ============================================================
# AI BENZERİ AKILLI SORU ÜRETİMİ
# ============================================================

def ai_matematik_soru(zorluk):
    """
    AI mantığıyla matematik sorusu üretir
    """
    if zorluk == "Kolay":
        aralik = (1, 10)
        islemler = ["+", "-"]
    elif zorluk == "Orta":
        aralik = (5, 30)
        islemler = ["+", "-", "x"]
    else:  # Zor
        aralik = (10, 100)
        islemler = ["+", "-", "x", "÷"]

    a = random.randint(*aralik)
    b = random.randint(*aralik)
    islem = random.choice(islemler)

    if islem == "+":
        return f"{a} + {b} = ?", a + b

    if islem == "-":
        if b > a:
            a, b = b, a
        return f"{a} - {b} = ?", a - b

    if islem == "x":
        return f"{a} × {b} = ?", a * b

    # Bölme (tam bölünecek şekilde)
    b = random.randint(2, 10)
    c = random.randint(2, 10)
    return f"{b*c} ÷ {b} = ?", c


def ai_turkce_soru(zorluk):
    """
    AI mantığıyla Türkçe soru üretir
    """
    kolay = [
        ("Siyah", "Kara"),
        ("Beyaz", "Ak"),
        ("İyi", "Kötü")
    ]
    orta = [
        ("Doktor", "Hekim"),
        ("Büyük", "Küçük"),
        ("Uzun", "Kısa")
    ]
    zor = [
        ("Cesur", "Korkak"),
        ("Zengin", "Fakir"),
        ("Genç", "Yaşlı")
    ]

    havuz = kolay if zorluk == "Kolay" else orta if zorluk == "Orta" else zor
    kelime, cevap = random.choice(havuz)

    return f"'{kelime}' kelimesinin anlamını yaz:", cevap

# ============================================================
# SAYFA AYARLARI
# ============================================================
st.set_page_config(
    page_title="Eğitici Oyun Ultra",
    page_icon="🎮",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ============================================================
# YARDIMCI FONKSİYONLAR
# ============================================================

def normalize_tr(text):
    """
    Türkçe karakterleri normalize eder.
    ş,ğ,ı,İ farklarını ortadan kaldırır
    """
    if not isinstance(text, str):
        return ""
    text = unicodedata.normalize("NFKD", text)
    text = "".join(c for c in text if not unicodedata.combining(c))
    return text.lower().strip()

def zaman_damgasi():
    return datetime.now().strftime("%H:%M:%S")

# ============================================================
# SESSION STATE BAŞLATMA
# ============================================================

default_state = {
    "sayfa": "menu",
    "isim": "Oyuncu",
    "puan": 0,
    "hak": 3,
    "max_hak": 3,
    "oyun_turu": "",
    "zorluk": "Orta",
    "sure": 20,
    "soru": "",
    "dogru_cevap": None,
    "mesaj": "",
    "baslangic": time.time(),
    "dogru": 0,
    "yanlis": 0,
    "pas": 0,
    "soru_no": 0,
    "liderlik": [],
    "log": [],
    "tema": "Açık",
    "calisma_turu": ""
}

for key, value in default_state.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ============================================================
# SORU ÜRETİCİ
# ============================================================

def matematik_soru():
    z = st.session_state.zorluk
    if z == "Kolay":
        a, b = random.randint(1, 10), random.randint(1, 10)
    elif z == "Orta":
        a, b = random.randint(10, 30), random.randint(5, 20)
    else:
        a, b = random.randint(20, 80), random.randint(10, 50)

    islem = random.choice(["+", "-", "x", "÷"])

    if islem == "+":
        return f"{a} + {b} = ?", a + b
    if islem == "-":
        return f"{a} - {b} = ?", a - b
    if islem == "x":
        return f"{a} × {b} = ?", a * b

    # Bölme
    b = random.randint(2, 10)
    c = random.randint(2, 10)
    return f"{b*c} ÷ {b} = ?", c

def turkce_soru():
    kelimeler = [
        ("Siyah", "Kara", "Eş"),
        ("Beyaz", "Ak", "Eş"),
        ("Doktor", "Hekim", "Eş"),
        ("Büyük", "Küçük", "Zıt"),
        ("Uzun", "Kısa", "Zıt"),
        ("İyi", "Kötü", "Zıt"),
        ("Sıcak", "Soğuk", "Zıt"),
        ("Genç", "Yaşlı", "Zıt"),
    ]
    k, c, t = random.choice(kelimeler)
    return f"'{k}' kelimesinin {t.upper()} anlamlısı nedir?", c

def yeni_soru():
    st.session_state.baslangic = time.time()
    st.session_state.mesaj = ""
    st.session_state.soru_no += 1

    if st.session_state.oyun_turu == "matematik":
        s, c = matematik_soru()
    else:
        s, c = turkce_soru()

    st.session_state.soru = s
    st.session_state.dogru_cevap = c

# ============================================================
# CEVAP KONTROL
# ============================================================

def cevap_kontrol(girdi):
    dogru = False

    if st.session_state.oyun_turu == "matematik":
        try:
            dogru = int(girdi) == st.session_state.dogru_cevap
        except:
            dogru = False
    else:
        dogru = normalize_tr(girdi) == normalize_tr(st.session_state.dogru_cevap)

    if dogru:
        st.session_state.puan += 10
        st.session_state.dogru += 1
        st.session_state.mesaj = "✅ Doğru!"
        st.session_state.log.append(
            f"[{zaman_damgasi()}] DOĞRU: {st.session_state.soru}"
        )
        def yeni_soru():
    st.session_state.baslangic = time.time()
    st.session_state.mesaj = ""
    st.session_state.soru_no += 1
    

    if st.session_state.oyun_turu == "matematik":
        s, c = openai_soru_uret("Matematik", st.session_state.zorluk)
    else:
        s, c = openai_soru_uret("Türkçe", st.session_state.zorluk)

    st.session_state.soru = s
    st.session_state.dogru_cevap = c
    else:
        st.session_state.hak -= 1
        st.session_state.yanlis += 1
        st.session_state.mesaj = "❌ Yanlış!"
        st.session_state.log.append(
            f"[{zaman_damgasi()}] YANLIŞ: {st.session_state.soru}"
        )

# ============================================================
# MENÜ
# ============================================================

if st.session_state.sayfa == "menu":
    st.title("🎓 Eğitici Oyun Platformu")

    st.session_state.isim = st.text_input(
        "👤 Oyuncu Adı", st.session_state.isim
    )

    st.session_state.max_hak = st.selectbox(
        "❤️ Can Sayısı", [3, 5, 10]
    )
    st.session_state.hak = st.session_state.max_hak

    st.session_state.zorluk = st.selectbox(
        "⚙️ Zorluk Seviyesi", ["Kolay", "Orta", "Zor"]
    )

    st.session_state.sure = st.selectbox(
        "⏱ Soru Süresi (sn)", [10, 20, 30]
    )

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("➕ Matematik Oyunu", use_container_width=True):
            st.session_state.oyun_turu = "matematik"
            st.session_state.sayfa = "oyun"
            yeni_soru()
    with col2:
        if st.button("📚 Türkçe Oyunu", use_container_width=True):
            st.session_state.oyun_turu = "turkce"
            st.session_state.sayfa = "oyun"
            yeni_soru()

    st.divider()

    if st.button("📖 Çalışma Modu"):
        st.session_state.sayfa = "calisma"

    if st.button("ℹ️ Hakkında"):
        st.session_state.sayfa = "hakkinda"

# ============================================================
# OYUN EKRANI
# ============================================================

elif st.session_state.sayfa == "oyun":
    kalan = st.session_state.sure - int(time.time() - st.session_state.baslangic)

    st.markdown(
        f"**👤 {st.session_state.isim} | 🏆 {st.session_state.puan} | ❤️ {st.session_state.hak}**"
    )

    st.progress(max(0, kalan) / st.session_state.sure)

    if kalan <= 0:
        st.session_state.hak -= 1
        st.session_state.yanlis += 1
        yeni_soru()
        st.rerun()

    if st.session_state.hak > 0:
        st.header(st.session_state.soru)

        with st.form("cevap_form", clear_on_submit=True):
            cevap = st.text_input("Cevabın")
            gonder = st.form_submit_button("Gönder")

        if gonder:
            cevap_kontrol(cevap)
            st.rerun()

        if st.button("➡️ Pas Geç"):
            st.session_state.pas += 1
            yeni_soru()
            st.rerun()

        if st.session_state.mesaj:
            if "✅" in st.session_state.mesaj:
                st.success(st.session_state.mesaj)
            else:
                st.error(st.session_state.mesaj)

    else:
        st.error("💀 Oyun Bitti")

        st.subheader("📊 İstatistikler")
        st.write(f"""
        - Soru Sayısı: {st.session_state.soru_no}
        - Doğru: {st.session_state.dogru}
        - Yanlış: {st.session_state.yanlis}
        - Pas: {st.session_state.pas}
        - Puan: {st.session_state.puan}
        """)

        st.session_state.liderlik.append(
            (st.session_state.isim, st.session_state.puan)
        )

        if st.button("🔁 Ana Menü"):
            for k in default_state:
                if k not in ["liderlik"]:
                    st.session_state[k] = default_state[k]
            st.session_state.sayfa = "menu"
            st.rerun()

# ============================================================
# ÇALIŞMA MODU
# ============================================================

elif st.session_state.sayfa == "calisma":
    st.header("📖 Çalışma Modu")

    st.subheader("🔢 Çarpım Tablosu")
    for i in range(1, 11):
        with st.expander(f"{i}'ler"):
            for j in range(1, 11):
                st.write(f"{i} × {j} = {i*j}")

    st.divider()

    st.subheader("📚 Eş / Zıt Anlamlılar")
    st.markdown("""
| Kelime | Karşılık | Tür |
|------|----------|-----|
| Siyah | Kara | Eş |
| Büyük | Küçük | Zıt |
| İyi | Kötü | Zıt |
| Doktor | Hekim | Eş |
""")

    if st.button("⬅️ Menü"):
        st.session_state.sayfa = "menu"
        st.rerun()

# ============================================================
# HAKKINDA
# ============================================================

elif st.session_state.sayfa == "hakkinda":
    st.header("ℹ️ Hakkında")
    st.write("""
    Bu uygulama:
    - Öğrenciler için
    - Eğitim + oyun mantığında
    - Python & Streamlit ile
    geliştirilmiştir.
    """)

    st.subheader("👨‍💻 Yapımcı")
    st.write("**Ege Kağan Köse**")

    if st.button("⬅️ Menü"):
        st.session_state.sayfa = "menu"
        st.rerun()

# ============================================================
# ALT BİLGİ
# ============================================================

st.divider()
st.caption("© 2026 | Eğitici Oyun Ultra | Ege Kağan Köse")