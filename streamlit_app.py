import streamlit as st
import random
import time
import unicodedata

# =================================================
# AYARLAR
# =================================================
st.set_page_config("Eğitici Oyun Ultimate", "🎮", "centered")

def tr_norm(t):
    t = unicodedata.normalize("NFKD", t)
    return "".join(c for c in t if not unicodedata.combining(c)).lower().strip()

# =================================================
# SESSION STATE
# =================================================
defaults = {
    "sayfa": "menu",
    "isim": "Oyuncu",
    "puan": 0,
    "hak": 3,
    "max_hak": 3,
    "soru": "",
    "cevap": None,
    "mesaj": "",
    "oyun": "",
    "zorluk": "Orta",
    "sure": 20,
    "baslangic": time.time(),
    "dogru": 0,
    "yanlis": 0,
    "pas": 0,
    "liderlik": []
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# =================================================
# SORU ÜRETİMİ
# =================================================
def yeni_soru():
    st.session_state.baslangic = time.time()
    st.session_state.mesaj = ""

    z = st.session_state.zorluk
    carp = {"Kolay": 5, "Orta": 10, "Zor": 20}[z]

    if st.session_state.oyun == "mat":
        a, b = random.randint(1, carp), random.randint(1, carp)
        op = random.choice(["+", "-", "x"])
        if op == "+":
            st.session_state.soru = f"{a} + {b} = ?"
            st.session_state.cevap = a + b
        elif op == "-":
            st.session_state.soru = f"{a+b} - {a} = ?"
            st.session_state.cevap = b
        else:
            st.session_state.soru = f"{a} × {b} = ?"
            st.session_state.cevap = a * b
    else:
        kelimeler = [
            ("Siyah","Kara"),("Beyaz","Ak"),("İyi","Kötü"),
            ("Uzun","Kısa"),("Doktor","Hekim")
        ]
        k, c = random.choice(kelimeler)
        st.session_state.soru = f"'{k}' kelimesinin anlamı?"
        st.session_state.cevap = c

# =================================================
# KONTROL
# =================================================
def kontrol(girdi):
    if not girdi:
        return
    dogru = False
    if st.session_state.oyun == "mat":
        try:
            dogru = int(girdi) == st.session_state.cevap
        except:
            pass
    else:
        dogru = tr_norm(girdi) == tr_norm(st.session_state.cevap)

    if dogru:
        st.session_state.puan += 10
        st.session_state.dogru += 1
        st.session_state.mesaj = "✅ Doğru!"
        yeni_soru()
    else:
        st.session_state.hak -= 1
        st.session_state.yanlis += 1
        st.session_state.mesaj = "❌ Yanlış!"

# =================================================
# MENU
# =================================================
if st.session_state.sayfa == "menu":
    st.title("🎓 Eğitici Oyun Ultimate")

    st.session_state.isim = st.text_input("👤 İsim", st.session_state.isim)
    st.session_state.max_hak = st.selectbox("❤️ Can", [3,5,10])
    st.session_state.zorluk = st.selectbox("⚙️ Zorluk", ["Kolay","Orta","Zor"])
    st.session_state.sure = st.selectbox("⏱ Süre (sn)", [10,20,30])
    st.session_state.hak = st.session_state.max_hak

    c1, c2 = st.columns(2)
    if c1.button("➕ Matematik", use_container_width=True):
        st.session_state.oyun = "mat"
        st.session_state.sayfa = "oyun"
        yeni_soru()
    if c2.button("📚 Türkçe", use_container_width=True):
        st.session_state.oyun = "tr"
        st.session_state.sayfa = "oyun"
        yeni_soru()

# =================================================
# OYUN
# =================================================
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

        with st.form("f", clear_on_submit=True):
            g = st.text_input("Cevap")
            if st.form_submit_button("Gönder"):
                kontrol(g)
                st.rerun()

        if st.button("➡️ Pas"):
            st.session_state.pas += 1
            yeni_soru()
            st.rerun()

        if st.session_state.mesaj:
            st.success(st.session_state.mesaj) if "✅" in st.session_state.mesaj else st.error(st.session_state.mesaj)
    else:
        st.session_state.liderlik.append(
            (st.session_state.isim, st.session_state.puan)
        )
        st.error("💀 Oyun Bitti")

        st.write(f"""
        📊 **İstatistik**
        - ✅ Doğru: {st.session_state.dogru}
        - ❌ Yanlış: {st.session_state.yanlis}
        - ➡️ Pas: {st.session_state.pas}
        """)

        if st.button("🔁 Menü"):
            st.session_state.sayfa = "menu"
            st.rerun()

# =================================================
# ALT
# =================================================
st.divider()
st.caption("👨‍💻 Yapımcı: **Ege Kağan Köse**")