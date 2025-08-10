import tkinter as tk
import random
import threading
import winsound

kelimeler = {
    "Hayvan": [
        "kedi", "köpek", "aslan", "kaplan", "tavşan", "zürafa", "penguen", "kartal", "tilki", "ayı",
        "yılan", "fare", "inek", "keçi", "deve", "at", "eşek", "ördek", "kaz", "tavuk",
        "horoz", "balık", "yunus", "köpekbalığı", "karınca", "arı", "sinek", "akrep", "kaplumbağa", "leopar",
        "çita", "lama", "alpaka", "baykuş", "martı", "serçe", "güvercin", "karga", "inek", "domuz",
        "koala", "kanguru", "gergedan", "fil", "maymun", "orangutan", "goril", "çakal", "kunduz", "mürekkepbalığı"
    ],
    "İsim": [
        "ahmet", "ayşe", "mehmet", "zeynep", "musa", "mustafa", "fatma", "selin", "ali", "veli",
        "can", "cem", "emre", "elif", "burak", "melis", "naz", "berk", "berna", "deniz",
        "özge", "özlem", "tuna", "tamer", "gül", "gülay", "gökhan", "gizem", "serkan", "serap",
        "sibel", "sinem", "arda", "arda", "arda", "arda", "arda", "arda", "arda", "arda",
        "arda", "arda", "arda", "arda", "arda", "arda", "arda", "arda", "arda", "arda"
    ],
    "Şehir": [
        "istanbul", "ankara", "izmir", "siirt", "antalya", "gaziantep", "trabzon", "adana", "bursa", "konya",
        "kayseri", "sakarya", "mardin", "van", "rize", "ordu", "samsun", "malatya", "elazığ", "diyarbakır",
        "şanlıurfa", "hatay", "kocaeli", "tekirdağ", "edirne", "çanakkale", "muğla", "aydın", "uşak", "afyon",
        "karaman", "nevşehir", "kırşehir", "kırıkkale", "yozgat", "tokat", "amasya", "çorum", "kastamonu", "sinop",
        "zonguldak", "bartın", "karabük", "bolu", "düzce", "bingöl", "bitlis", "hakkari", "ığdır", "bayburt"
    ],
    "Eşya": [
        "masa", "sandalye", "telefon", "kalem", "ayna", "bilgisayar", "çanta", "kitap", "defter", "silgi",
        "cetvel", "makas", "lamba", "televizyon", "kumanda", "buzdolabı", "çamaşır makinesi", "ütü", "fırın", "mikrodalga",
        "tabak", "çatal", "kaşık", "bardak", "tencere", "yastık", "battaniye", "halı", "perde", "saat",
        "klavye", "mouse", "hoparlör", "kulaklık", "kamera", "çerçeve", "ayna", "dolap", "çekmece", "raf",
        "terlik", "ayakkabı", "mont", "pantolon", "gömlek", "tişört", "şemsiye", "cüzdan", "anahtar", "çakmak"
    ],
    "Araba": [
        "ford", "volvo", "honda", "mercedes", "toyota", "chevrolet", "renault", "bmw", "audi", "fiat",
        "hyundai", "kia", "mazda", "nissan", "skoda", "seat", "peugeot", "citroen", "opel", "suzuki",
        "subaru", "mitsubishi", "jeep", "tesla", "dacia", "mini", "jaguar", "land rover", "alfa romeo", "lancia",
        "ferrari", "lamborghini", "bugatti", "maserati", "bentley", "rolls royce", "cadillac", "lincoln", "chrysler", "ram",
        "daewoo", "hummer", "infiniti", "isuzu", "saab", "smart", "tata", "volkswagen", "ds", "byd"
    ]
}


adam_parcalari = [
    lambda canvas: canvas.create_oval(120, 50, 180, 110, width=3),
    lambda canvas: canvas.create_line(150, 110, 150, 180, width=3),
    lambda canvas: canvas.create_line(150, 130, 110, 160, width=3),
    lambda canvas: canvas.create_line(150, 130, 190, 160, width=3),
    lambda canvas: canvas.create_line(150, 180, 120, 220, width=3),
    lambda canvas: canvas.create_line(150, 180, 180, 220, width=3)
]

class AdamAsmaca:
    def __init__(self, root):
        self.root = root
        self.root.title("Adam Asmaca")
        self.root.geometry("700x600")
        self.root.configure(bg="#f0f0f0")
        self.oyunu_sifirla()

    def kategori_secimi(self):
        self.kategori_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.kategori_frame.pack()
        tk.Label(self.kategori_frame, text="Kategori Seçin:", font=("Arial", 16), bg="#f0f0f0").pack()
        for kategori in kelimeler.keys():
            tk.Button(self.kategori_frame, text=kategori, font=("Arial", 14), width=12,
                      command=lambda k=kategori: self.zorluk_sec(k)).pack(pady=5)

    def zorluk_sec(self, kategori):
        self.kategori = kategori
        self.kategori_frame.destroy()
        self.zorluk_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.zorluk_frame.pack()
        tk.Label(self.zorluk_frame, text="Zorluk Seçin:", font=("Arial", 16), bg="#f0f0f0").pack()
        for z in ["Kolay", "Zor"]:
            tk.Button(self.zorluk_frame, text=z, font=("Arial", 14), width=10,
                      command=lambda zorluk=z: self.baslat_oyun(zorluk)).pack(pady=5)

    def baslat_oyun(self, zorluk):
        self.zorluk = zorluk
        self.zorluk_frame.destroy()
        kelime_listesi = kelimeler[self.kategori]
        if zorluk == "Kolay":
            kelime_listesi = [k for k in kelime_listesi if len(k) <= 6]
        else:
            kelime_listesi = [k for k in kelime_listesi if len(k) > 6]
        self.kelime = random.choice(kelime_listesi)

        self.kategori_label = tk.Label(self.root, text=f"Kategori: {self.kategori} | Zorluk: {self.zorluk}",
                                       font=("Arial", 18, "bold"), fg="blue", bg="#f0f0f0")
        self.kategori_label.pack()

        self.kelime_label = tk.Label(self.root, font=("Arial", 32), bg="#f0f0f0")
        self.kelime_label.pack(pady=10)

        self.bilgi_label = tk.Label(self.root, font=("Arial", 14), bg="#f0f0f0", justify="left")
        self.bilgi_label.pack()

        self.root.bind("<Key>", self.klavye_tahmin)
        self.guncelle_ekran()

    def klavye_tahmin(self, event):
        if self.hata_sayisi >= len(adam_parcalari):
            return

        harf = event.char.lower()
        if not harf or not harf.isalpha() or harf in self.tahmin_edilen:
            return

        self.tahmin_edilen.append(harf)

        if harf in self.kelime:
            self.dogru_harfler.append(harf)
            threading.Thread(target=lambda: winsound.Beep(1000, 200)).start()
        else:
            self.yanlis_harfler.append(harf)
            self.hata_sayisi += 1
            self.adam_ciz()
            threading.Thread(target=lambda: winsound.Beep(400, 300)).start()

        self.guncelle_ekran()
        self.kontrol_et()

    def kontrol_et(self):
        if "_" not in [h if h in self.tahmin_edilen else "_" for h in self.kelime]:
            self.kelime_label.config(text=f"🎉 Tebrikler! Kelime: {self.kelime}")
            self.root.unbind("<Key>")
            self.yeniden_baslat_butonu()
        elif self.hata_sayisi >= len(adam_parcalari):
            self.kelime_label.config(text=f"💀 Kaybettiniz! Kelime: {self.kelime}")
            self.root.unbind("<Key>")
            self.yeniden_baslat_butonu()

    def guncelle_ekran(self):
        gosterim = " ".join([harf if harf in self.tahmin_edilen else "_" for harf in self.kelime])
        self.kelime_label.config(text=gosterim)

        kalan = max(0, len(adam_parcalari) - self.hata_sayisi)
        bilgi = f"Kalan Tahmin Hakkı: {kalan}\n"
        bilgi += f"✅ Doğru Harfler: {' '.join(self.dogru_harfler)}\n"
        bilgi += f"❌ Yanlış Harfler: {' '.join(self.yanlis_harfler)}"
        self.bilgi_label.config(text=bilgi)

    def adam_ciz(self):
        if 0 < self.hata_sayisi <= len(adam_parcalari):
            adam_parcalari[self.hata_sayisi - 1](self.canvas)

    def yeniden_baslat_butonu(self):
        btn = tk.Button(self.root, text="🔁 Yeniden Başla", font=("Arial", 14), bg="#d0f0d0",
                        command=self.oyunu_sifirla)
        btn.pack(pady=20)

    def oyunu_sifirla(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.kelime = ""
        self.kategori = ""
        self.zorluk = "Kolay"
        self.tahmin_edilen = []
        self.dogru_harfler = []
        self.yanlis_harfler = []
        self.hata_sayisi = 0
        self.canvas = tk.Canvas(self.root, width=300, height=250, bg="white")
        self.canvas.pack(pady=10)
        self.kategori_secimi()


if __name__ == "__main__":
    root = tk.Tk()
    oyun = AdamAsmaca(root)
    root.mainloop()
