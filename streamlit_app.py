import tkinter as tk
import random
import os
from tkinter import simpledialog, messagebox
import json

# Ses için kütüphane (Windows için)
try:
    import winsound
except ImportError:
    winsound = None

# Kamera ve Resim İşleme Kütüphaneleri (Varsa yükle, yoksa hata verme)
try:
    import cv2
    from PIL import Image, ImageTk
    KAMERA_VAR = True
except ImportError:
    cv2 = None
    Image = None
    ImageTk = None
    KAMERA_VAR = False

SES_ACIK = True # Global ses ayarı

def dogru_ses():
    """Doğru cevap sesi çalar."""
    if SES_ACIK and winsound:
        # Daha yumuşak, kulak tırmalamayan bir ton
        winsound.Beep(600, 150)

def yanlis_ses():
    """Yanlış cevap sesi çalar."""
    if SES_ACIK and winsound:
        # Kalın ve biraz daha uzun bir ses
        winsound.Beep(400, 400)

def buton_sesi():
    """Butonlara basınca çıkan kısa pıt sesi."""
    if SES_ACIK and winsound:
        winsound.Beep(2000, 5)

class DersSecimEkrani:
    def __init__(self, root):
        self.root = root
        self.root.title("Eğlenceli Dersler Menüsü")
        self.root.geometry("400x400")
        self.root.configure(bg="#FFF9C4") # Açık sarı arka plan
        self.root.state('zoomed')

        tk.Label(root, text="Ders Seçimi Yapalım! 🎓", font=("Comic Sans MS", 18, "bold"), bg="#FFF9C4", fg="#FF6F00").pack(pady=40)

        # Türkçe Bölümü
        frm_tr = tk.Frame(root, bg="#FFF9C4")
        frm_tr.pack(pady=10)
        tk.Button(frm_tr, text="TÜRKÇE OYUN 📚", command=lambda: [buton_sesi(), self.turkce_secildi()], font=("Arial", 16, "bold"), bg="#FF5252", fg="white", width=25, height=4).pack(side=tk.LEFT, padx=5)
        tk.Button(frm_tr, text="ÇALIŞMA 📖", command=lambda: [buton_sesi(), self.turkce_calisma()], font=("Arial", 16, "bold"), bg="#FF8A80", fg="white", width=18, height=4).pack(side=tk.LEFT, padx=5)

        # Matematik Bölümü
        frm_mat = tk.Frame(root, bg="#FFF9C4")
        frm_mat.pack(pady=10)
        tk.Button(frm_mat, text="MATEMATİK OYUN ➕", command=lambda: [buton_sesi(), self.matematik_secildi()], font=("Arial", 16, "bold"), bg="#448AFF", fg="white", width=25, height=4).pack(side=tk.LEFT, padx=5)
        tk.Button(frm_mat, text="ÇALIŞMA 🔢", command=lambda: [buton_sesi(), self.matematik_calisma()], font=("Arial", 16, "bold"), bg="#82B1FF", fg="white", width=18, height=4).pack(side=tk.LEFT, padx=5)

        # Ayarlar Butonu
        tk.Button(root, text="AYARLAR ⚙️", command=lambda: [buton_sesi(), self.ayarlari_ac()], font=("Arial", 14, "bold"), bg="#607D8B", fg="white", width=20, height=2).pack(pady=20)

        # Çıkış Butonu
        tk.Button(root, text="ÇIKIŞ ❌", command=lambda: [buton_sesi(), self.cikis_yap()], font=("Arial", 14, "bold"), bg="#D32F2F", fg="white", width=20, height=2).pack(pady=5)

        # Yapımcı Etiketi
        tk.Label(root, text="Yapımcı: Ege Kağan Köse", font=("Arial", 16, "bold"), bg="#FFF9C4", fg="#333333").place(relx=1.0, rely=1.0, anchor='se', x=-20, y=-20)

    def ayarlari_ac(self):
        win = tk.Toplevel(self.root)
        win.title("Ayarlar")
        win.geometry("300x200")
        
        def ses_degistir():
            global SES_ACIK
            SES_ACIK = not SES_ACIK
            buton_sesi()
            btn_ses.config(text=f"Ses Efektleri: {'AÇIK 🔊' if SES_ACIK else 'KAPALI 🔇'}")
            
        btn_ses = tk.Button(win, text=f"Ses Efektleri: {'AÇIK 🔊' if SES_ACIK else 'KAPALI 🔇'}", command=ses_degistir, font=("Arial", 14, "bold"), bg="#E0E0E0", width=25, height=2)
        btn_ses.pack(expand=True)

    def cikis_yap(self):
        if messagebox.askyesno("Çıkış", "Çıkmak istediğinizden emin misiniz?"):
            self.root.destroy()

    def turkce_calisma(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        TurkceCalisma(self.root)

    def matematik_calisma(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        MatematikCalisma(self.root)

    def turkce_secildi(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        TurkceOyunu(self.root)

    def matematik_secildi(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        EgiticiOyun(self.root)

class EgiticiOyun:
    def __init__(self, root):
        self.root = root
        self.root.title("Matematik Macerası - Çocuklar İçin")
        self.root.geometry("500x450")
        
        # --- Arka Plan Resmi ---
        try:
            # "arkaplan.png" adında bir resmi kodun yanına koyarsan arka plan olur
            # DÜZELTME: Arkadaşlarında çalışması için tam yol yerine sadece dosya adını kullanıyoruz.
            self.bg_resim = tk.PhotoImage(file="anasınıfı.png")
            self.bg_label = tk.Label(root, image=self.bg_resim)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except:
            # Resim yoksa veya hata olursa eski rengi kullan
            self.root.configure(bg="#E0F7FA")

        # Geri Dön Butonu
        self.geri_btn = tk.Button(root, text="🔙", command=lambda: [buton_sesi(), self.ana_menuye_don()], font=("Arial", 14, "bold"), bg="#FF5722", fg="white", width=5)
        self.geri_btn.place(x=10, y=10)

        self.puan = 0
        self.dogru_cevap = 0
        self.oyuncu_adi = "Oyuncu"
        self.skorlar = self.skorlari_yukle()
        self.yuksek_puan = self.en_yuksek_puani_bul()
        self.baslangic_suresi = 60
        self.kalan_sure = self.baslangic_suresi
        self.oyun_aktif = False
        self.tekrar_hakki = True
        self.ard_arda_carpma_yanlis = 0
        self.duraklatildi = False
        self.islem_turu = 1 # Varsayılan değer (Hata önlemek için)
        self.kalan_hak = 3

        # --- Arayüz Elemanları ---

        # Başlık
        self.baslik = tk.Label(root, text="Matematik Macerası! 🚀", font=("Comic Sans MS", 20, "bold"), bg="#E0F7FA", fg="#FF5722")
        self.baslik.pack(pady=20)

        # Puan Tablosu
        self.puan_label = tk.Label(root, text="Puan: 0", font=("Arial", 14, "bold"), bg="#E0F7FA", fg="#009688")
        self.puan_label.pack()

        # Hak Göstergesi
        self.hak_label = tk.Label(root, text=f"Kalan Hak: {self.kalan_hak}", font=("Arial", 14, "bold"), bg="#E0F7FA", fg="#FF9800")
        self.hak_label.pack()

        # Süre Göstergesi
        self.sure_label = tk.Label(root, text=f"Süre: {self.kalan_sure}", font=("Arial", 14, "bold"), bg="#E0F7FA", fg="#FF0000")
        self.sure_label.pack()

        # En Yüksek Puan Göstergesi
        self.yuksek_puan_label = tk.Label(root, text=f"En Yüksek: {self.yuksek_puan}", font=("Arial", 12), bg="#E0F7FA", fg="#795548")
        self.yuksek_puan_label.pack()

        # Zorluk Seçimi
        self.zorluk_frame = tk.Frame(root, bg="#E0F7FA")
        self.zorluk_frame.pack(pady=5)
        tk.Label(self.zorluk_frame, text="Zorluk:", font=("Arial", 10, "bold"), bg="#E0F7FA").pack(side=tk.LEFT)
        self.zorluk_var = tk.StringVar(value="Orta")
        self.zorluk_menu = tk.OptionMenu(self.zorluk_frame, self.zorluk_var, "Kolay", "Orta", "Zor", "Bonus :)", command=self.zorluk_degisti)
        self.zorluk_menu.config(bg="white", font=("Arial", 10))
        self.zorluk_menu.pack(side=tk.LEFT, padx=5)

        # Soru Alanı
        self.soru_cercevesi = tk.Frame(root, bg="white", bd=2, relief="ridge")
        self.soru_cercevesi.pack(pady=30, padx=50, fill="x")
        
        self.soru_label = tk.Label(self.soru_cercevesi, text="Hazır mısın?", font=("Arial", 30, "bold"), bg="white", fg="#3F51B5")
        self.soru_label.pack(pady=20)

        # Cevap Giriş Alanı
        self.cevap_entry = tk.Entry(root, font=("Arial", 20), justify='center', width=10)
        self.cevap_entry.pack(pady=5)
        self.cevap_entry.bind('<Return>', self.cevabi_kontrol_et)  # Enter tuşuna basınca kontrol et

        # Butonlar
        self.buton_frame = tk.Frame(root, bg="#E0F7FA")
        self.buton_frame.pack(pady=20)

        self.kontrol_btn = tk.Button(self.buton_frame, text="CEVAPLA", command=lambda: [buton_sesi(), self.cevabi_kontrol_et()], font=("Arial", 16, "bold"), bg="#4CAF50", fg="white", width=18, height=3)
        self.kontrol_btn.pack(side=tk.LEFT, padx=10)

        self.pas_btn = tk.Button(self.buton_frame, text="PAS GEÇ", command=lambda: [buton_sesi(), self.pas_gec()], font=("Arial", 16, "bold"), bg="#FF9800", fg="white", width=18, height=3)
        self.pas_btn.pack(side=tk.LEFT, padx=10)

        # Skor Tablosu Butonu
        self.skor_btn = tk.Button(root, text="🏆 Skor Tablosu", command=lambda: [buton_sesi(), self.skor_tablosunu_goster()], font=("Arial", 12, "bold"), bg="#9C27B0", fg="white")
        self.skor_btn.pack(pady=5)

        # Geri Bildirim Mesajı (Doğru/Yanlış)
        self.mesaj_label = tk.Label(root, text="", font=("Arial", 14), bg="#E0F7FA")
        self.mesaj_label.pack(pady=10)

        # Yeniden Oyna Butonu (Başlangıçta gizli)
        self.yeniden_oyna_btn = tk.Button(root, text="YENİDEN OYNA 🔄", command=lambda: [buton_sesi(), self.yeniden_baslat()], font=("Arial", 16, "bold"), bg="#2196F3", fg="white")

        # Başlangıç ayarları ekranını aç (Biraz gecikmeli aç ki ana pencere yüklensin)
        self.root.after(100, self.oyun_kurulum_ekrani)

        # Yapımcı Etiketi
        tk.Label(root, text="Yapımcı: Ege Kağan Köse", font=("Arial", 16, "bold"), bg="#E0F7FA", fg="#333333").place(relx=1.0, rely=1.0, anchor='se', x=-20, y=-20)

    def ana_menuye_don(self):
        self.oyun_aktif = False
        for widget in self.root.winfo_children():
            widget.destroy()
        DersSecimEkrani(self.root)

    def oyun_kurulum_ekrani(self):
        # Önce varsa eski temp dosyasını temizle
        if os.path.exists("temp_profil.png"):
            try: os.remove("temp_profil.png")
            except: pass

        # 1. Adım: Kamera Sorusu (Eğer kamera varsa)
        if KAMERA_VAR:
            if messagebox.askyesno("Kamera", "Profil fotoğrafı çekmek ister misin?"):
                win = self.fotograf_cek("temp")
                if win:
                    self.root.wait_window(win)
        
        # 2. Adım: Ayarlar Penceresi
        self.goster_ayarlar_penceresi()

    def goster_ayarlar_penceresi(self):
        # Ayarlar için yeni bir pencere aç
        kurulum_penceresi = tk.Toplevel(self.root)
        kurulum_penceresi.title("Oyun Ayarları")
        kurulum_penceresi.geometry("300x600") # Pencere boyunu uzattık, her şey sığsın
        kurulum_penceresi.grab_set() # Bu pencere kapanmadan oyuna dönülemez
        kurulum_penceresi.protocol("WM_DELETE_WINDOW", self.root.destroy) # Çarpıya basarsa oyun kapansın

        tk.Label(kurulum_penceresi, text="İsminiz:", font=("Arial", 12, "bold")).pack(pady=10)
        isim_var = tk.StringVar(value=self.oyuncu_adi)
        tk.Entry(kurulum_penceresi, textvariable=isim_var, font=("Arial", 12)).pack()

        # Hak Seçimi (En üstte olsun istendiği için buraya ekledim)
        tk.Label(kurulum_penceresi, text="Hak Sayısı (Can):", font=("Arial", 12, "bold")).pack(pady=5)
        hak_var = tk.IntVar(value=3)
        tk.OptionMenu(kurulum_penceresi, hak_var, 3, 5, 10).pack()

        tk.Label(kurulum_penceresi, text="Süre Seçin (Saniye):", font=("Arial", 12, "bold")).pack(pady=10)
        sure_var = tk.IntVar(value=60)
        tk.OptionMenu(kurulum_penceresi, sure_var, 10, 20, 30, 40, 50, 60).pack()

        def basla():
            self.oyuncu_adi = isim_var.get() or "Oyuncu"
            
            # Temp fotoğraf varsa asıl isme çevir
            if os.path.exists("temp_profil.png"):
                try:
                    hedef = f"{self.oyuncu_adi}_profil.png"
                    if os.path.exists(hedef): os.remove(hedef)
                    os.rename("temp_profil.png", hedef)
                except: pass

            self.baslangic_suresi = sure_var.get()
            self.kalan_hak = hak_var.get()
            self.hak_label.config(text=f"Kalan Hak: {self.kalan_hak}")
            self.kalan_sure = self.baslangic_suresi
            self.root.title(f"Matematik Macerası - Hoş Geldin {self.oyuncu_adi}!")
            self.sure_label.config(text=f"Süre: {self.kalan_sure}")
            kurulum_penceresi.destroy()
            self.oyunu_baslat()

        tk.Button(kurulum_penceresi, text="OYUNA BAŞLA 🚀", command=lambda: [buton_sesi(), basla()], bg="#4CAF50", fg="white", font=("Arial", 14, "bold")).pack(pady=20)

    def fotograf_cek(self, isim):
        if not KAMERA_VAR: return
        if not isim: isim = "Oyuncu"
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Hata", "Kamera açılamadı.", parent=self.root)
            return

        win = tk.Toplevel(self.root)
        win.title("Fotoğraf Çek")
        win.geometry("400x350")
        
        lbl_cam = tk.Label(win)
        lbl_cam.pack(pady=10)
        
        def guncelle():
            if not win.winfo_exists():
                cap.release()
                return

            ret, frame = cap.read()
            if ret:
                # Görüntüyü aynala ve renklendir
                frame = cv2.flip(frame, 1)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                rgb = cv2.resize(rgb, (320, 240))
                img = Image.fromarray(rgb)
                imgtk = ImageTk.PhotoImage(image=img)
                lbl_cam.imgtk = imgtk
                lbl_cam.configure(image=imgtk)
                lbl_cam.after(10, guncelle)
            else:
                cap.release()

        def cek():
            ret, frame = cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                kucuk = cv2.resize(frame, (60, 60))
                cv2.imwrite(f"{isim}_profil.png", kucuk)
                messagebox.showinfo("Bilgi", "Harika! Fotoğrafın kaydedildi. 📸", parent=win)
            cap.release()
            win.destroy()

        tk.Button(win, text="BU FOTOĞRAFI KAYDET ✅", command=lambda: [buton_sesi(), cek()], bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
        win.protocol("WM_DELETE_WINDOW", lambda: (cap.release(), win.destroy()))
        guncelle()
        return win

    def oyunu_baslat(self):
        self.oyun_aktif = True
        self.yeni_soru_olustur()
        self.zamanlayici_baslat()

    def skorlari_yukle(self):
        if os.path.exists("matematik_skorlar.json"):
            try:
                with open("matematik_skorlar.json", "r", encoding="utf-8") as dosya:
                    return json.load(dosya)
            except (json.JSONDecodeError, ValueError):
                return []
        return []

    def en_yuksek_puani_bul(self):
        if not self.skorlar:
            return 0
        return max(skor['puan'] for skor in self.skorlar)

    def skor_kaydet(self):
        self.skorlar.append({"isim": self.oyuncu_adi, "puan": self.puan})
        with open("matematik_skorlar.json", "w", encoding="utf-8") as dosya:
            json.dump(self.skorlar, dosya, ensure_ascii=False, indent=4)

    def zorluk_degisti(self, *args):
        self.yeni_soru_olustur()

    def zamanlayici_baslat(self):
        if self.duraklatildi: return
        if self.kalan_sure > 0 and self.oyun_aktif:
            self.kalan_sure -= 1
            self.sure_label.config(text=f"Süre: {self.kalan_sure}")
            self.root.after(1000, self.zamanlayici_baslat)
        elif self.kalan_sure <= 0 and self.oyun_aktif:
            self.oyunu_bitir()

    def oyunu_bitir(self):
        self.oyun_aktif = False
        self.soru_label.config(text="Oyun Bitti!", fg="red")
        self.mesaj_label.config(text=f"Süre Doldu! Toplam Puan: {self.puan}", fg="blue")
        self.skor_kaydet()
        self.cevap_entry.config(state="disabled")
        self.kontrol_btn.config(state="disabled")
        self.pas_btn.config(state="disabled")
        self.yeniden_oyna_btn.pack(pady=10)

    def pas_gec(self):
        if not self.oyun_aktif: return
        self.mesaj_label.config(text=f"Pas geçildi. Cevap: {self.dogru_cevap}", fg="blue")
        self.cevap_entry.config(state="disabled")
        self.root.after(2000, self.pas_gec_devam)

    def pas_gec_devam(self):
        self.cevap_entry.config(state="normal")
        self.yeni_soru_olustur()

    def skor_tablosunu_goster(self):
        self.skorlar = self.skorlari_yukle() # En güncel hali al
        en_iyi_skorlar = {}
        for skor in self.skorlar:
            isim = skor['isim']
            puan = skor['puan']
            if isim not in en_iyi_skorlar or puan > en_iyi_skorlar[isim]:
                en_iyi_skorlar[isim] = puan
        sirali_liste = sorted(en_iyi_skorlar.items(), key=lambda item: item[1], reverse=True)

        # Özel Pencere Oluştur (Resim gösterebilmek için)
        win = tk.Toplevel(self.root)
        win.title("Skor Tablosu")
        win.geometry("400x500")
        win.configure(bg="#E0F7FA")
        
        tk.Label(win, text="🏆 En Yüksek Skorlar 🏆", font=("Comic Sans MS", 16, "bold"), bg="#E0F7FA", fg="#FF5722").pack(pady=10)
        
        if not sirali_liste:
            tk.Label(win, text="Henüz kayıtlı skor yok.", bg="#E0F7FA").pack()
            
        for i, (isim, puan) in enumerate(sirali_liste[:5], 1): # İlk 5
            frm = tk.Frame(win, bg="white", bd=1, relief="solid")
            frm.pack(pady=5, fill="x", padx=20)
            
            # Varsa profil resmini yükle
            img_path = f"{isim}_profil.png"
            if KAMERA_VAR and os.path.exists(img_path):
                try:
                    img = Image.open(img_path)
                    # OpenCV BGR kaydeder, PIL RGB okur, renkler karışabilir ama basitlik için direkt açıyoruz
                    # Düzeltme: OpenCV ile kaydettik, PIL ile açıyoruz.
                    # Renk düzeltmesi gerekebilir ama şimdilik basit tutalım.
                    img = ImageTk.PhotoImage(img)
                    lbl_img = tk.Label(frm, image=img, bg="white")
                    lbl_img.image = img # Referansı tut
                    lbl_img.pack(side=tk.LEFT, padx=5)
                except: pass
            
            tk.Label(frm, text=f"{i}. {isim}", font=("Arial", 12, "bold"), bg="white").pack(side=tk.LEFT, padx=10)
            tk.Label(frm, text=f"{puan} Puan", font=("Arial", 12, "bold"), fg="#009688", bg="white").pack(side=tk.RIGHT, padx=10)

        def sifirla():
            if messagebox.askyesno("Sıfırla", "Matematik skorlarını silmek istediğine emin misin?", parent=win):
                self.skorlar = []
                with open("matematik_skorlar.json", "w", encoding="utf-8") as f:
                    json.dump([], f)
                win.destroy()
                messagebox.showinfo("Bilgi", "Skorlar silindi.", parent=self.root)

        tk.Button(win, text="SKORLARI SIFIRLA 🗑️", command=lambda: [buton_sesi(), sifirla()], bg="#FF5252", fg="white", font=("Arial", 12, "bold")).pack(pady=10)

    def yeniden_baslat(self):
        self.puan = 0
        self.ard_arda_carpma_yanlis = 0
        self.oyun_aktif = False
        self.puan_label.config(text="Puan: 0")
        self.soru_label.config(fg="#3F51B5")
        self.cevap_entry.config(state="normal")
        self.kontrol_btn.config(state="normal")
        self.pas_btn.config(state="normal")
        self.yeniden_oyna_btn.pack_forget()
        
        # Yeniden başlarken de ayar ekranını göster
        self.oyun_kurulum_ekrani()

    def yeni_soru_olustur(self):
        if not self.oyun_aktif: return
        self.cevap_entry.delete(0, tk.END)
        self.mesaj_label.config(text="")
        self.cevap_entry.focus_set()

        # İşlem türünü rastgele seç: 1=Toplama, 2=Çıkarma, 3=Çarpma, 4=Bölme
        self.islem_turu = random.randint(1, 4)
        zorluk = self.zorluk_var.get()

        if self.islem_turu == 1:  # Toplama
            if zorluk == "Kolay":
                s1, s2 = random.randint(1, 20), random.randint(1, 20)
            elif zorluk == "Zor":
                s1, s2 = random.randint(50, 200), random.randint(50, 200)
            elif zorluk == "Bonus :)":
                s1, s2 = random.randint(100, 1000), random.randint(100, 1000)
            else: # Orta
                s1, s2 = random.randint(10, 50), random.randint(10, 50)
            islem_sembolu = "+"
            self.dogru_cevap = s1 + s2
            
        elif self.islem_turu == 2:  # Çıkarma
            if zorluk == "Kolay":
                s1 = random.randint(5, 20)
                s2 = random.randint(1, s1)
            elif zorluk == "Zor":
                s1 = random.randint(50, 200)
                s2 = random.randint(10, s1)
            elif zorluk == "Bonus :)":
                s1 = random.randint(500, 1500)
                s2 = random.randint(100, s1)
            else: # Orta
                s1 = random.randint(20, 60)
                s2 = random.randint(1, s1)
            islem_sembolu = "-"
            self.dogru_cevap = s1 - s2
            
        elif self.islem_turu == 3:  # Çarpma
            if zorluk == "Kolay":
                s1, s2 = random.randint(1, 6), random.randint(1, 5)
            elif zorluk == "Zor":
                s1, s2 = random.randint(5, 15), random.randint(5, 12)
            elif zorluk == "Bonus :)":
                s1, s2 = random.randint(10, 30), random.randint(10, 20)
            else: # Orta
                s1, s2 = random.randint(1, 10), random.randint(1, 5)
            islem_sembolu = "x"
            self.dogru_cevap = s1 * s2
            
        else: # Bölme (islem_turu == 4)
            # Bölme işleminde sonucun tam sayı çıkması için tersinden gidiyoruz:
            # Önce böleni (s2) ve sonucu (cevap) seçip, bölüneni (s1) hesaplıyoruz.
            if zorluk == "Kolay":
                s2 = random.randint(2, 5)
                cevap = random.randint(2, 5)
            elif zorluk == "Zor":
                s2 = random.randint(5, 20)
                cevap = random.randint(5, 20)
            elif zorluk == "Bonus :)":
                s2 = random.randint(10, 30)
                cevap = random.randint(10, 30)
            else: # Orta
                s2 = random.randint(3, 10)
                cevap = random.randint(3, 10)
            
            s1 = s2 * cevap
            islem_sembolu = "÷"
            self.dogru_cevap = cevap

        self.soru_label.config(text=f"{s1} {islem_sembolu} {s2} = ?")

    def cevabi_kontrol_et(self, event=None):
        if not self.oyun_aktif: return
        try:
            kullanici_cevabi = int(self.cevap_entry.get())
            if kullanici_cevabi == self.dogru_cevap:
                self.ard_arda_carpma_yanlis = 0 # Doğru bilince sayacı sıfırla
                self.puan += 10
                
                if self.puan > self.yuksek_puan:
                    self.yuksek_puan = self.puan
                    self.yuksek_puan_label.config(text=f"En Yüksek: {self.yuksek_puan}")

                self.mesaj_label.config(text="Harika! Doğru Bildin! 🎉", fg="green")
                self.root.after(10, dogru_ses) # Sesi arayüzü dondurmadan çal
                self.root.after(1000, self.yeni_soru_olustur) # 1 saniye sonra yeni soruya geç
            else:
                if self.tekrar_hakki:
                    self.tekrar_hakki = False
                    self.mesaj_label.config(text="Yanlış oldu, tekrar dene! 🤔", fg="orange")
                    self.cevap_entry.delete(0, tk.END)
                else:
                    # Çarpma işlemiyse ve yanlışsa sayacı artır
                    if self.islem_turu == 3:
                        self.ard_arda_carpma_yanlis += 1
                        if self.ard_arda_carpma_yanlis >= 5:
                            self.duraklatildi = True
                            cevap = messagebox.askyesno("Çalışma Zamanı? 💡", "Çarpma işleminde biraz zorlandın gibi.\nÇalışma alanına gidip tekrar etmek ister misin?")
                            if cevap:
                                for widget in self.root.winfo_children(): widget.destroy()
                                MatematikCalisma(self.root)
                                return
                            else:
                                self.duraklatildi = False
                                self.ard_arda_carpma_yanlis = 0
                                self.zamanlayici_baslat()

                    self.puan -= 5
                    self.kalan_hak -= 1
                    self.hak_label.config(text=f"Kalan Hak: {self.kalan_hak}")
                    if self.kalan_hak <= 0:
                        self.oyunu_bitir()
                        return

                    self.root.after(10, yanlis_ses)
                    self.mesaj_label.config(text="Yanlış oldu. Tekrar dene!", fg="red")
            self.puan_label.config(text=f"Puan: {self.puan}")
        except ValueError:
            self.mesaj_label.config(text="Lütfen sadece sayı girin!", fg="orange")

class TurkceOyunu:
    def __init__(self, root):
        self.root = root
        self.root.title("Türkçe Kelime Avı - Eş ve Zıt Anlam")
        self.root.geometry("500x500")
        
        # Arka plan (Matematik oyunuyla aynı mantık)
        try:
            self.bg_resim = tk.PhotoImage(file="anasınıfı.png")
            self.bg_label = tk.Label(root, image=self.bg_resim)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except:
            self.root.configure(bg="#FFF3E0") # Resim yoksa açık turuncu

        # Geri Dön Butonu
        self.geri_btn = tk.Button(root, text="🔙", command=lambda: [buton_sesi(), self.ana_menuye_don()], font=("Arial", 14, "bold"), bg="#FF5722", fg="white", width=5)
        self.geri_btn.place(x=10, y=10)

        self.puan = 0
        self.dogru_cevap = ""
        self.oyuncu_adi = "Oyuncu"
        self.skorlar = self.skorlari_yukle()
        self.yuksek_puan = self.en_yuksek_puani_bul()
        self.baslangic_suresi = 60
        self.kalan_sure = self.baslangic_suresi
        self.oyun_aktif = False
        self.tekrar_hakki = True
        self.ard_arda_yanlis = 0
        self.duraklatildi = False
        self.kalan_hak = 3

        # --- Arayüz ---
        self.baslik = tk.Label(root, text="Kelime Avı! 🔎", font=("Comic Sans MS", 20, "bold"), bg="#FFF3E0", fg="#E65100")
        self.baslik.pack(pady=20)

        self.puan_label = tk.Label(root, text="Puan: 0", font=("Arial", 14, "bold"), bg="#FFF3E0", fg="#009688")
        self.puan_label.pack()

        # Hak Göstergesi
        self.hak_label = tk.Label(root, text=f"Kalan Hak: {self.kalan_hak}", font=("Arial", 14, "bold"), bg="#FFF3E0", fg="#FF9800")
        self.hak_label.pack()

        self.sure_label = tk.Label(root, text=f"Süre: {self.kalan_sure}", font=("Arial", 14, "bold"), bg="#FFF3E0", fg="#FF0000")
        self.sure_label.pack()

        self.yuksek_puan_label = tk.Label(root, text=f"En Yüksek: {self.yuksek_puan}", font=("Arial", 12), bg="#FFF3E0", fg="#795548")
        self.yuksek_puan_label.pack()

        # Soru Alanı
        self.soru_cercevesi = tk.Frame(root, bg="white", bd=2, relief="ridge")
        self.soru_cercevesi.pack(pady=20, padx=50, fill="x")
        
        self.soru_label = tk.Label(self.soru_cercevesi, text="Hazır mısın?", font=("Arial", 18, "bold"), bg="white", fg="#3F51B5")
        self.soru_label.pack(pady=20)

        # Cevap Alanı
        self.cevap_entry = tk.Entry(root, font=("Arial", 16), justify='center', width=15)
        self.cevap_entry.pack(pady=5)
        self.cevap_entry.bind('<Return>', self.cevabi_kontrol_et)

        # Butonlar
        self.buton_frame = tk.Frame(root, bg="#FFF3E0")
        self.buton_frame.pack(pady=20)

        self.kontrol_btn = tk.Button(self.buton_frame, text="CEVAPLA", command=lambda: [buton_sesi(), self.cevabi_kontrol_et()], font=("Arial", 16, "bold"), bg="#4CAF50", fg="white", width=18, height=3)
        self.kontrol_btn.pack(side=tk.LEFT, padx=10)

        self.pas_btn = tk.Button(self.buton_frame, text="PAS GEÇ", command=lambda: [buton_sesi(), self.pas_gec()], font=("Arial", 16, "bold"), bg="#FF9800", fg="white", width=18, height=3)
        self.pas_btn.pack(side=tk.LEFT, padx=10)

        self.skor_btn = tk.Button(root, text="🏆 Skor Tablosu", command=lambda: [buton_sesi(), self.skor_tablosunu_goster()], font=("Arial", 12, "bold"), bg="#9C27B0", fg="white")
        self.skor_btn.pack(pady=5)

        self.mesaj_label = tk.Label(root, text="", font=("Arial", 14), bg="#FFF3E0")
        self.mesaj_label.pack(pady=10)

        self.yeniden_oyna_btn = tk.Button(root, text="YENİDEN OYNA 🔄", command=lambda: [buton_sesi(), self.yeniden_baslat()], font=("Arial", 16, "bold"), bg="#2196F3", fg="white")

        # Başlangıç
        self.root.after(100, self.oyun_kurulum_ekrani)

        # Yapımcı Etiketi
        tk.Label(root, text="Yapımcı: Ege Kağan Köse", font=("Arial", 16, "bold"), bg="#FFF3E0", fg="#333333").place(relx=1.0, rely=1.0, anchor='se', x=-20, y=-20)

    def ana_menuye_don(self):
        self.oyun_aktif = False
        for widget in self.root.winfo_children():
            widget.destroy()
        DersSecimEkrani(self.root)

    # --- Yardımcı Metotlar (EgiticiOyun ile benzer) ---
    def oyun_kurulum_ekrani(self):
        # Önce varsa eski temp dosyasını temizle
        if os.path.exists("temp_profil.png"):
            try: os.remove("temp_profil.png")
            except: pass

        # 1. Adım: Kamera Sorusu (Eğer kamera varsa)
        if KAMERA_VAR:
            if messagebox.askyesno("Kamera", "Profil fotoğrafı çekmek ister misin?"):
                win = self.fotograf_cek("temp")
                if win:
                    self.root.wait_window(win)
        
        # 2. Adım: Ayarlar Penceresi
        self.goster_ayarlar_penceresi()

    def goster_ayarlar_penceresi(self):
        # Ayarlar için yeni bir pencere aç
        kurulum_penceresi = tk.Toplevel(self.root)
        kurulum_penceresi.title("Oyun Ayarları")
        kurulum_penceresi.geometry("300x600")
        kurulum_penceresi.grab_set()
        kurulum_penceresi.protocol("WM_DELETE_WINDOW", self.root.destroy)

        tk.Label(kurulum_penceresi, text="İsminiz:", font=("Arial", 12, "bold")).pack(pady=10)
        isim_var = tk.StringVar(value=self.oyuncu_adi)
        tk.Entry(kurulum_penceresi, textvariable=isim_var, font=("Arial", 12)).pack()

        # Hak Seçimi
        tk.Label(kurulum_penceresi, text="Hak Sayısı (Can):", font=("Arial", 12, "bold")).pack(pady=5)
        hak_var = tk.IntVar(value=3)
        tk.OptionMenu(kurulum_penceresi, hak_var, 3, 5, 10).pack()

        tk.Label(kurulum_penceresi, text="Süre Seçin (Saniye):", font=("Arial", 12, "bold")).pack(pady=10)
        sure_var = tk.IntVar(value=60)
        tk.OptionMenu(kurulum_penceresi, sure_var, 10, 20, 30, 40, 50, 60).pack()

        # Kamera varsa Fotoğraf Çek butonu ekle
        if KAMERA_VAR:
            tk.Button(kurulum_penceresi, text="KAMERAYI AÇ 📸", command=lambda: [buton_sesi(), self.fotograf_cek(isim_var.get())], bg="#FF9800", fg="white", font=("Arial", 12, "bold")).pack(pady=5)

        def basla():
            self.oyuncu_adi = isim_var.get() or "Oyuncu"
            self.baslangic_suresi = sure_var.get()
            self.kalan_hak = hak_var.get()
            self.hak_label.config(text=f"Kalan Hak: {self.kalan_hak}")
            self.kalan_sure = self.baslangic_suresi
            self.root.title(f"Kelime Avı - Hoş Geldin {self.oyuncu_adi}!")
            self.sure_label.config(text=f"Süre: {self.kalan_sure}")
            kurulum_penceresi.destroy()
            self.oyunu_baslat()

        tk.Button(kurulum_penceresi, text="OYUNA BAŞLA 🚀", command=lambda: [buton_sesi(), basla()], bg="#4CAF50", fg="white", font=("Arial", 14, "bold")).pack(pady=20)

    def fotograf_cek(self, isim):
        if not KAMERA_VAR: return
        if not isim: isim = "Oyuncu"
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Hata", "Kamera açılamadı.", parent=self.root)
            return

        win = tk.Toplevel(self.root)
        win.title("Fotoğraf Çek")
        win.geometry("400x350")
        
        lbl_cam = tk.Label(win)
        lbl_cam.pack(pady=10)
        
        def guncelle():
            if not win.winfo_exists():
                cap.release()
                return
            ret, frame = cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                rgb = cv2.resize(rgb, (320, 240))
                img = Image.fromarray(rgb)
                imgtk = ImageTk.PhotoImage(image=img)
                lbl_cam.imgtk = imgtk
                lbl_cam.configure(image=imgtk)
                lbl_cam.after(10, guncelle)

        def cek():
            ret, frame = cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                kucuk = cv2.resize(frame, (60, 60))
                cv2.imwrite(f"{isim}_profil.png", kucuk)
                messagebox.showinfo("Bilgi", "Harika! Fotoğrafın kaydedildi. 📸", parent=win)
            cap.release()
            win.destroy()

        tk.Button(win, text="BU FOTOĞRAFI KAYDET ✅", command=lambda: [buton_sesi(), cek()], bg="#4CAF50", fg="white", font=("Arial", 12, "bold")).pack(pady=10)
        win.protocol("WM_DELETE_WINDOW", lambda: (cap.release(), win.destroy()))
        guncelle()
        return win

    def oyunu_baslat(self):
        self.oyun_aktif = True
        self.yeni_soru_olustur()
        self.zamanlayici_baslat()

    def skorlari_yukle(self):
        if os.path.exists("turkce_skorlar.json"):
            try:
                with open("turkce_skorlar.json", "r", encoding="utf-8") as dosya:
                    return json.load(dosya)
            except: return []
        return []

    def en_yuksek_puani_bul(self):
        if not self.skorlar: return 0
        return max(skor['puan'] for skor in self.skorlar)

    def skor_kaydet(self):
        self.skorlar.append({"isim": self.oyuncu_adi, "puan": self.puan})
        with open("turkce_skorlar.json", "w", encoding="utf-8") as dosya:
            json.dump(self.skorlar, dosya, ensure_ascii=False, indent=4)

    def zamanlayici_baslat(self):
        if self.duraklatildi: return
        if self.kalan_sure > 0 and self.oyun_aktif:
            self.kalan_sure -= 1
            self.sure_label.config(text=f"Süre: {self.kalan_sure}")
            self.root.after(1000, self.zamanlayici_baslat)
        elif self.kalan_sure <= 0 and self.oyun_aktif:
            self.oyunu_bitir()

    def oyunu_bitir(self):
        self.oyun_aktif = False
        self.soru_label.config(text="Oyun Bitti!", fg="red")
        self.mesaj_label.config(text=f"Süre Doldu! Toplam Puan: {self.puan}", fg="blue")
        self.skor_kaydet()
        self.cevap_entry.config(state="disabled")
        self.kontrol_btn.config(state="disabled")
        self.pas_btn.config(state="disabled")
        self.yeniden_oyna_btn.pack(pady=10)

    def pas_gec(self):
        if not self.oyun_aktif: return
        self.mesaj_label.config(text=f"Pas geçildi. Cevap: {self.dogru_cevap}", fg="blue")
        self.cevap_entry.config(state="disabled")
        self.root.after(2000, self.pas_gec_devam)

    def pas_gec_devam(self):
        self.cevap_entry.config(state="normal")
        self.yeni_soru_olustur()

    def skor_tablosunu_goster(self):
        self.skorlar = self.skorlari_yukle()
        en_iyi_skorlar = {}
        for skor in self.skorlar:
            isim = skor['isim']
            puan = skor['puan']
            if isim not in en_iyi_skorlar or puan > en_iyi_skorlar[isim]:
                en_iyi_skorlar[isim] = puan
        sirali_liste = sorted(en_iyi_skorlar.items(), key=lambda item: item[1], reverse=True)

        win = tk.Toplevel(self.root)
        win.title("Skor Tablosu")
        win.geometry("400x500")
        win.configure(bg="#FFF3E0")

        tk.Label(win, text="🏆 En Yüksek Skorlar 🏆", font=("Comic Sans MS", 16, "bold"), bg="#FFF3E0", fg="#FF5722").pack(pady=10)

        if not sirali_liste:
            tk.Label(win, text="Henüz kayıtlı skor yok.", bg="#FFF3E0").pack()

        for i, (isim, puan) in enumerate(sirali_liste[:5], 1): # İlk 5
            frm = tk.Frame(win, bg="white", bd=1, relief="solid")
            frm.pack(pady=5, fill="x", padx=20)
            
            # Varsa profil resmini yükle
            img_path = f"{isim}_profil.png"
            if KAMERA_VAR and os.path.exists(img_path):
                try:
                    img = Image.open(img_path)
                    img = ImageTk.PhotoImage(img)
                    lbl_img = tk.Label(frm, image=img, bg="white")
                    lbl_img.image = img
                    lbl_img.pack(side=tk.LEFT, padx=5)
                except: pass
            
            tk.Label(frm, text=f"{i}. {isim}", font=("Arial", 12, "bold"), bg="white").pack(side=tk.LEFT, padx=10)
            tk.Label(frm, text=f"{puan} Puan", font=("Arial", 12, "bold"), fg="#009688", bg="white").pack(side=tk.RIGHT, padx=10)

        def sifirla():
            if messagebox.askyesno("Sıfırla", "Türkçe skorlarını silmek istediğine emin misin?", parent=win):
                self.skorlar = []
                with open("turkce_skorlar.json", "w", encoding="utf-8") as f:
                    json.dump([], f)
                win.destroy()
                messagebox.showinfo("Bilgi", "Skorlar silindi.", parent=self.root)

        tk.Button(win, text="SKORLARI SIFIRLA 🗑️", command=lambda: [buton_sesi(), sifirla()], bg="#FF5252", fg="white", font=("Arial", 12, "bold")).pack(pady=10)

    def yeniden_baslat(self):
        self.puan = 0
        self.ard_arda_yanlis = 0
        self.oyun_aktif = False
        self.puan_label.config(text="Puan: 0")
        self.soru_label.config(fg="#3F51B5")
        self.cevap_entry.config(state="normal")
        self.kontrol_btn.config(state="normal")
        self.pas_btn.config(state="normal")
        self.yeniden_oyna_btn.pack_forget()
        self.oyun_kurulum_ekrani()

    def yeni_soru_olustur(self):
        if not self.oyun_aktif: return
        self.cevap_entry.delete(0, tk.END)
        self.mesaj_label.config(text="")
        self.cevap_entry.focus_set()
        self.tekrar_hakki = True

        # Kelime Listesi (Eş ve Zıt Anlam Karışık)
        kelimeler = [
            ("Siyah", "Kara", "Eş"), ("Beyaz", "Ak", "Eş"), ("Kırmızı", "Al", "Eş"),
            ("Okul", "Mektep", "Eş"), ("Doktor", "Hekim", "Eş"), ("Yıl", "Sene", "Eş"),
            ("Büyük", "Küçük", "Zıt"), ("Uzun", "Kısa", "Zıt"), ("Sıcak", "Soğuk", "Zıt"),
            ("Açık", "Kapalı", "Zıt"), ("Var", "Yok", "Zıt"), ("Gel", "Git", "Zıt"),
            ("Zengin", "Fakir", "Zıt"), ("Genç", "Yaşlı", "Zıt"), ("İyi", "Kötü", "Zıt"),
            ("Cevap", "Yanıt", "Eş"), ("Soru", "Sual", "Eş"), ("Giriş", "Çıkış", "Zıt"),
            ("Islak", "Kuru", "Zıt"), ("Barış", "Savaş", "Zıt"), ("Hediye", "Armağan", "Eş"),
            ("Kalp", "Yürek", "Eş"), ("İhtiyar", "Yaşlı", "Eş"), ("Taze", "Bayat", "Zıt"),
            ("Uzak", "Yakın", "Zıt"), ("Sabah", "Akşam", "Zıt"), ("Dost", "Düşman", "Zıt"),
            ("Al", "Kırmızı", "Eş"), ("Ak", "Beyaz", "Eş"), ("Kara", "Siyah", "Eş"),
            ("Öğrenci", "Talebe", "Eş"), ("Okul", "Mektep", "Eş"), ("Öğretmen", "Muallim", "Eş")
        ]
        
        secilen = random.choice(kelimeler)
        self.soru_kelime = secilen[0]
        self.dogru_cevap = secilen[1]
        turu = secilen[2]

        if turu == "Eş":
            soru_metni = f"'{self.soru_kelime}' kelimesinin\nEŞ anlamlısı nedir?"
        else:
            soru_metni = f"'{self.soru_kelime}' kelimesinin\nZIT anlamlısı nedir?"
            
        self.soru_label.config(text=soru_metni)

    def cevabi_kontrol_et(self, event=None):
        if not self.oyun_aktif: return
        kullanici_cevabi = self.cevap_entry.get().strip()
        
        # Türkçe karakter uyumlu küçük harf çevirimi
        cev_kucuk = kullanici_cevabi.replace("İ", "i").replace("I", "ı").lower()
        dogru_kucuk = self.dogru_cevap.replace("İ", "i").replace("I", "ı").lower()

        if cev_kucuk == dogru_kucuk:
            self.ard_arda_yanlis = 0
            self.puan += 10
            if self.puan > self.yuksek_puan:
                self.yuksek_puan = self.puan
                self.yuksek_puan_label.config(text=f"En Yüksek: {self.yuksek_puan}")

            self.mesaj_label.config(text=f"Harika! Doğru: {self.dogru_cevap} 🎉", fg="green")
            self.root.after(10, dogru_ses)
            self.root.after(1000, self.yeni_soru_olustur)
        else:
            if self.tekrar_hakki:
                self.tekrar_hakki = False
                self.mesaj_label.config(text="Yanlış oldu, tekrar dene! 🤔", fg="orange")
                self.cevap_entry.delete(0, tk.END)
            else:
                self.ard_arda_yanlis += 1
                if self.ard_arda_yanlis >= 5:
                    self.duraklatildi = True
                    cevap = messagebox.askyesno("Çalışma Zamanı? 💡", "Kelimelerde biraz zorlandın gibi.\nÇalışma alanına gidip listeye bakmak ister misin?")
                    if cevap:
                        for widget in self.root.winfo_children(): widget.destroy()
                        TurkceCalisma(self.root)
                        return
                    else:
                        self.duraklatildi = False
                        self.ard_arda_yanlis = 0
                        self.zamanlayici_baslat()
                
                self.kalan_hak -= 1
                self.hak_label.config(text=f"Kalan Hak: {self.kalan_hak}")
                if self.kalan_hak <= 0:
                    self.oyunu_bitir()
                    return

                self.root.after(10, yanlis_ses)
                self.puan -= 5
                self.mesaj_label.config(text="Yanlış oldu. Tekrar dene!", fg="red")
        
        self.puan_label.config(text=f"Puan: {self.puan}")

class MatematikCalisma:
    def __init__(self, root):
        self.root = root
        self.root.title("Matematik Çalışma Alanı")
        self.root.geometry("600x600")
        self.root.configure(bg="#E0F7FA")

        tk.Label(root, text="Çarpım Tablosu 🔢", font=("Comic Sans MS", 20, "bold"), bg="#E0F7FA", fg="#FF5722").pack(pady=10)

        # Kaydırılabilir metin alanı
        text_area = tk.Text(root, font=("Courier New", 12), width=50, height=20)
        text_area.pack(pady=10, padx=10)
        
        content = ""
        for i in range(1, 11):
            content += f"--- {i}'ler ---\n"
            for j in range(1, 11):
                content += f"{i} x {j} = {i*j}\n"
            content += "\n"
        
        text_area.insert(tk.END, content)
        text_area.config(state='disabled') # Değiştirilemez yap

        tk.Button(root, text="GERİ DÖN 🔙", command=lambda: [buton_sesi(), self.geri_don()], font=("Arial", 16, "bold"), bg="#FF9800", fg="white", width=18, height=3).pack(pady=10)

        # Yapımcı Etiketi
        tk.Label(root, text="Yapımcı: Ege Kağan Köse", font=("Arial", 16, "bold"), bg="#E0F7FA", fg="#333333").place(relx=1.0, rely=1.0, anchor='se', x=-20, y=-20)

    def geri_don(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        DersSecimEkrani(self.root)

class TurkceCalisma:
    def __init__(self, root):
        self.root = root
        self.root.title("Türkçe Çalışma Alanı")
        self.root.geometry("600x600")
        self.root.configure(bg="#FFF3E0")

        tk.Label(root, text="Kelime Listesi 📖", font=("Comic Sans MS", 20, "bold"), bg="#FFF3E0", fg="#E65100").pack(pady=10)

        text_area = tk.Text(root, font=("Arial", 12), width=50, height=20)
        text_area.pack(pady=10, padx=10)

        # Oyundaki kelimelerin listesi
        kelimeler = [
            ("Siyah", "Kara", "Eş"), ("Beyaz", "Ak", "Eş"), ("Kırmızı", "Al", "Eş"),
            ("Okul", "Mektep", "Eş"), ("Doktor", "Hekim", "Eş"), ("Yıl", "Sene", "Eş"),
            ("Büyük", "Küçük", "Zıt"), ("Uzun", "Kısa", "Zıt"), ("Sıcak", "Soğuk", "Zıt"),
            ("Açık", "Kapalı", "Zıt"), ("Var", "Yok", "Zıt"), ("Gel", "Git", "Zıt"),
            ("Zengin", "Fakir", "Zıt"), ("Genç", "Yaşlı", "Zıt"), ("İyi", "Kötü", "Zıt"),
            ("Cevap", "Yanıt", "Eş"), ("Soru", "Sual", "Eş"), ("Giriş", "Çıkış", "Zıt"),
            ("Islak", "Kuru", "Zıt"), ("Barış", "Savaş", "Zıt"), ("Hediye", "Armağan", "Eş"),
            ("Kalp", "Yürek", "Eş"), ("İhtiyar", "Yaşlı", "Eş"), ("Taze", "Bayat", "Zıt"),
            ("Uzak", "Yakın", "Zıt"), ("Sabah", "Akşam", "Zıt"), ("Dost", "Düşman", "Zıt"),
            ("Al", "Kırmızı", "Eş"), ("Ak", "Beyaz", "Eş"), ("Kara", "Siyah", "Eş"),
            ("Öğrenci", "Talebe", "Eş"), ("Okul", "Mektep", "Eş"), ("Öğretmen", "Muallim", "Eş")
        ]

        content = f"{'KELİME':<15} {'KARŞILIĞI':<15} {'TÜR'}\n"
        content += "-"*40 + "\n"
        for k1, k2, tur in kelimeler:
            tur_yazi = "Eş Anlam" if tur == "Eş" else "Zıt Anlam"
            content += f"{k1:<15} {k2:<15} {tur_yazi}\n"

        text_area.insert(tk.END, content)
        text_area.config(state='disabled')

        tk.Button(root, text="GERİ DÖN 🔙", command=lambda: [buton_sesi(), self.geri_don()], font=("Arial", 16, "bold"), bg="#FF9800", fg="white", width=18, height=3).pack(pady=10)

        # Yapımcı Etiketi
        tk.Label(root, text="Yapımcı: Ege Kağan Köse", font=("Arial", 16, "bold"), bg="#FFF3E0", fg="#333333").place(relx=1.0, rely=1.0, anchor='se', x=-20, y=-20)

    def geri_don(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        DersSecimEkrani(self.root)

if __name__ == "__main__":
    root = tk.Tk()
    app = DersSecimEkrani(root)
    messagebox.showinfo("Başarılar", "Oyuna hoş geldin! Başarılar dilerim! 🍀")
    root.mainloop()
