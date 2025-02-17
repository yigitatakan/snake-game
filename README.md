# Gelişmiş Yılan Oyunu

Klasik yılan oyununun Python ve Pygame ile yapılmış gelişmiş bir versiyonu.

## Özellikler

- Başlangıç menüsü ve ayarlar ekranı
- 3 farklı çözünürlük seçeneği (800x600, 1024x768, 1280x720)
- Ses ve müzik seviyesi ayarları
- 3 farklı zorluk seviyesi (Kolay, Normal, Zor)
- Güç-up'lar (Hızlanma, Yavaşlama, Ekstra Puan)
- En yüksek skor takibi
- Ses efektleri
- Modern görünüm
- Pürüzsüz kontroller

## Gereksinimler

- Python 3.x
- Pygame

## Kurulum

1. Gerekli bağımlılıkları yükleyin:
```bash
pip install -r requirements.txt
```

2. Oyunu başlatın:
```bash
python yilan_oyunu.py
```

## Nasıl Oynanır

### Ana Menü
- "Oyuna Başla" butonu ile oyunu başlatın
- "Ayarlar" butonu ile oyun ayarlarını değiştirin
- "Çıkış" butonu ile oyundan çıkın

### Ayarlar Menüsü
- Ses ve müzik seviyelerini ayarlayın
- Ekran çözünürlüğünü seçin (800x600, 1024x768, 1280x720)
- Zorluk seviyesini belirleyin (Kolay, Normal, Zor)
- "Geri" butonu ile ana menüye dönün

### Oyun Kontrolleri
- Yılanı yön tuşları ile kontrol edin (↑, ↓, ←, →)
- Kırmızı yemleri yiyerek yılanı büyütün ve puan kazanın
- Altın renkli güç-up'ları toplayarak özel güçler kazanın
- Duvarlara veya yılanın kendi vücuduna çarpmamaya dikkat edin
- Oyun bittiğinde SPACE tuşuna basarak ana menüye dönün

## Seviyeler

1. Seviye (0-19 puan)
   - Normal hız
   - Her yem 1 puan
   - %10 güç-up şansı

2. Seviye (20-49 puan)
   - Artan hız
   - Her yem 2 puan
   - %15 güç-up şansı

3. Seviye (50+ puan)
   - Maksimum hız
   - Her yem 3 puan
   - %20 güç-up şansı

## Güç-up'lar

- 🏃 HIZLANMA: Yılanın hızını 10 saniye boyunca %50 artırır
- 🐌 YAVASLAMA: Yılanın hızını 10 saniye boyunca %30 azaltır
- ⭐ EKSTRA_PUAN: Anlık bonus puan

## Ayarlar Dosyası

Oyun ayarları `ayarlar.json` dosyasında saklanır ve oyun her başlatıldığında otomatik olarak yüklenir. Eğer dosya yoksa varsayılan ayarlar kullanılır. 