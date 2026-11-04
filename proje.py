
import csv
import math
import os
import random
from datetime import datetime, timedelta

#değişkenleri standart olarak snake_case standartlarında tanımladım.

def ortalama(liste):
    return sum(liste) / len(liste)


def standart_sapma(liste):
    ort = ortalama(liste)
    toplam = 0
    for x in liste:
        toplam += (x - ort) ** 2
    return math.sqrt(toplam / len(liste))


def oklid(a, b):
    toplam = 0
    for i in range(len(a)):
        toplam += (a[i] - b[i]) ** 2
    return math.sqrt(toplam)


def manhattan(a, b):
    toplam = 0
    for i in range(len(a)):
        toplam += abs(a[i] - b[i])
    return toplam

os.makedirs("veri", exist_ok=True)
random.seed(42)  

baslangic = datetime(2026, 10, 20, 8, 0)
satirlar = []

for i in range(500):
    paket = round(random.gauss(1200, 150))      
    boyut = round(random.gauss(800, 100))       
    port = round(random.gauss(25, 5))           
    satirlar.append([paket, boyut, port, "normal"])

for i in range(20):
    paket = random.randint(8000, 15000)
    boyut = random.randint(60, 120)
    port = random.randint(2, 10)
    satirlar.append([paket, boyut, port, "anormal"])

random.shuffle(satirlar)

with open("veri/trafik.csv", "w", newline="", encoding="utf-8") as dosya:
    yazici = csv.writer(dosya)
    yazici.writerow(["zaman", "paket_sn", "ort_boyut", "hedef_port",
                     "etiket"])
    for i, satir in enumerate(satirlar):
        zaman = baslangic + timedelta(minutes=i)
        yazici.writerow([zaman.strftime("%Y-%m-%d %H:%M")] + satir)

print("veri/trafik.csv oluşturuldu:", len(satirlar), "satır")

vektorler = []
etiketler = []
zamanlar = []

with open("veri/trafik.csv", encoding="utf-8") as dosya:
    okuyucu = csv.DictReader(dosya)
    for satir in okuyucu:
        vektor = [float(satir["paket_sn"]),
                  float(satir["ort_boyut"]),
                  float(satir["hedef_port"])]
        vektorler.append(vektor)
        etiketler.append(satir["etiket"])
        zamanlar.append(satir["zaman"])

print("Okunan satır sayısı:", len(vektorler))
print("Örnek vektör (ilk satır):", vektorler[0])

normal_vektorler = []
for i in range(len(vektorler)):
    if etiketler[i] == "normal":
        normal_vektorler.append(vektorler[i])

mu = []
sigma = []
for j in range(3):
    sutun = [v[j] for v in normal_vektorler]
    mu.append(ortalama(sutun))
    sigma.append(standart_sapma(sutun))

print("\nμ (normal):", [round(m, 2) for m in mu])
print("σ (normal):", [round(s, 2) for s in sigma])

z_vektorler = []
for v in vektorler:
    z = []
    for j in range(3):
        z.append((v[j] - mu[j]) / sigma[j])
    z_vektorler.append(z)

z_normal = []
for i in range(len(z_vektorler)):
    if etiketler[i] == "normal":
        z_normal.append(z_vektorler[i])

centroid = []
for j in range(3):
    centroid.append(ortalama([z[j] for z in z_normal]))

print("Centroid (z-skor uzayında):", [round(c, 4) + 0.0 for c in centroid])

oklid_mesafeler = []
manhattan_mesafeler = []
for z in z_vektorler:
    oklid_mesafeler.append(oklid(z, centroid))
    manhattan_mesafeler.append(manhattan(z, centroid))

normal_oklid = []
for i in range(len(oklid_mesafeler)):
    if etiketler[i] == "normal":
        normal_oklid.append(oklid_mesafeler[i])

mu_d = ortalama(normal_oklid)
sigma_d = standart_sapma(normal_oklid)
esik = mu_d + 3 * sigma_d

print("\nNormal Öklid mesafeleri: μd = {:.3f}, σd = {:.3f}".format(
    mu_d, sigma_d))
print("Eşik (μd + 3σd) = {:.3f}".format(esik))

print("\n--- ANOMALİ OLARAK ETİKETLENEN SATIRLAR ---")
print("{:<18}{:>10}{:>12}   {}".format(
    "Zaman", "Öklid", "Manhattan", "Gerçek etiket"))
anomali_sayisi = 0
dogru = 0
for i in range(len(oklid_mesafeler)):
    if oklid_mesafeler[i] > esik:
        anomali_sayisi += 1
        if etiketler[i] == "anormal":
            dogru += 1
        print("{:<18}{:>10.3f}{:>12.3f}   {}  -> ANOMALİ".format(
            zamanlar[i], oklid_mesafeler[i], manhattan_mesafeler[i],
            etiketler[i])) 

print("\nToplam ANOMALİ:", anomali_sayisi)
print("Bunlardan gerçekten anormal olan:", dogru, "/ 20")

normal_manhattan = []
anormal_oklid = []
anormal_manhattan = []
for i in range(len(etiketler)):
    if etiketler[i] == "normal":
        normal_manhattan.append(manhattan_mesafeler[i])
    else:
        anormal_oklid.append(oklid_mesafeler[i])
        anormal_manhattan.append(manhattan_mesafeler[i])



"""
alt kısmı kendim kodlamaya çalıştım fakat bazı kısımları
kafamda kuramadım. kendi yazdığım
kısımların debugging aşamasında ve sonrasında ai dan destek aldım.
"""

print("\n--- ÖKLİD VE MANHATTAN KARŞILAŞTIRMASI ---")
print("{:<12}{:>16}{:>16}{:>10}".format("Metrik", "Normal ort.",
                                        "Anormal ort.", "Oran"))
oran_o = ortalama(anormal_oklid) / ortalama(normal_oklid)
oran_m = ortalama(anormal_manhattan) / ortalama(normal_manhattan)
print("{:<12}{:>16.3f}{:>16.3f}{:>10.1f}".format(
    "Öklid", ortalama(normal_oklid), ortalama(anormal_oklid), oran_o))
print("{:<12}{:>16.3f}{:>16.3f}{:>10.1f}".format(
    "Manhattan", ortalama(normal_manhattan), ortalama(anormal_manhattan),
    oran_m))
