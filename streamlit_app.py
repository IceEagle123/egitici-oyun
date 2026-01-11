import streamlit as st
import random

st.set_page_config(page_title="Eğitici Oyun", page_icon="🎮")

# --------- SESSION STATE ---------
if "soru" not in st.session_state:
    st.session_state.soru = ""
if "cevap" not in st.session_state:
    st.session_state.cevap = 0
if "mesaj" not in st.session_state:
    st.session_state.mesaj = ""
if "zorluk" not in st.session_state:
    st.session_state.zorluk = "Kolay"

# --------- SORU OLUŞTUR ---------
def soru_olustur():
    st.session_state.mesaj = ""

    if st.session_state.zorluk == "Kolay":
        alt, ust = 1, 10
    elif st.session_state.zorluk == "Orta":
        alt, ust = 10, 50
    else:
        alt, ust = 50, 100

    a = random.randint(alt, ust)
    b = random.randint(alt, ust)

    st.session_state.soru = f"{a} + {b} kaçtır?"
    st.session_state.cevap = a + b

# --------- ARAYÜZ ---------
st.title("🎓 Eğitici Matematik Oyunu")

st.session_state.zorluk = st.selectbox(
    "Zorluk Seviyesi",
    ["Kolay", "Orta", "Zor"]
)

if st.button("Yeni Soru"):
    soru_olustur()

if st.session_state.soru:
    st.subheader(st.session_state.soru)

    girilen = st.text_input("Cevabın:")

    if st.button("Kontrol Et"):
        try:
            if int(girilen) == st.session_state.cevap:
                st.success("✅ Doğru!")
                soru_olustur()
            else:
                st.error(f"❌ Yanlış. Doğru cevap: {st.session_state.cevap}")
        except:
            st.warning("Lütfen sayı gir"
