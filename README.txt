BGT 205 Siber Güvenlik 1 - Ara Sınav Projesi
Konu 3: Ağ Trafiği Anomali Tespiti ve Uzaklık Vektörleri Analizi

Python sürümü: Python 3.14

Harici kütüphane kullanmadım, sadece Python'un kendi kütüphaneleri kullanıldı (csv, math, os, random, datetime)

Terminalde proje klasörünün içerisine girip:
  "python3 proje.py" komutu çalıştırılabilir.
 (Windows'ta python3 yerine "python proje.py" yazılabilir.)

Veri, "proje.py" içinde yapay zekâ desteğiyle rastgele üretilmiştir. Dışarıdan hazır bir veri seti kullanılmamıştır.

Veri dosyası: veri/trafik.csv
  - 520 satır: 500 normal + 20 anormal (DDoS şüphesi) trafik
  - Sütunlar: zaman, paket_sn, ort_boyut, hedef_port, etiket
  - proje.py her çalıştırıldığında bu dosyayı yeniden oluşturur,
    ardından okuyup analiz eder. Seed sabit olduğu için içerik aynı kalır.

Her çalıştırmada aynı sonuç oluşması için random.seed(42) olarak sabitlenmiştir.
