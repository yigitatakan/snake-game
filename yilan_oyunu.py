import pygame
import random
import sys
import json
import os
from enum import Enum

# Pygame'i başlat
pygame.init()
pygame.mixer.init()

# Renk tanımlamaları
SIYAH = (0, 0, 0)
BEYAZ = (255, 255, 255)
KIRMIZI = (255, 0, 0)
YESIL = (0, 255, 0)
MAVI = (0, 0, 255)
ALTIN = (255, 215, 0)
GRI = (128, 128, 128)

# Oyun sabitleri
IZGARA_BOYUT = 20

# Varsayılan ayarlar
VARSAYILAN_AYARLAR = {
    'pencere_genislik': 800,
    'pencere_yukseklik': 600,
    'ses_seviyesi': 0.5,
    'muzik_seviyesi': 0.3,
    'zorluk': 'normal'  # kolay, normal, zor
}

class Ayarlar:
    def __init__(self):
        self.ayarlar = self.ayarlari_yukle()
        self.pencere = None
        self.guncelle_pencere()

    def ayarlari_yukle(self):
        try:
            with open('ayarlar.json', 'r') as f:
                return json.load(f)
        except:
            return VARSAYILAN_AYARLAR.copy()

    def ayarlari_kaydet(self):
        with open('ayarlar.json', 'w') as f:
            json.dump(self.ayarlar, f)

    def guncelle_pencere(self):
        self.pencere = pygame.display.set_mode((
            self.ayarlar['pencere_genislik'],
            self.ayarlar['pencere_yukseklik']
        ))
        return self.pencere

class Menu:
    def __init__(self, ayarlar):
        self.ayarlar = ayarlar
        self.font_buyuk = pygame.font.Font(None, 64)
        self.font_normal = pygame.font.Font(None, 36)
        self.butonlar = {}
        self.aktif_menu = 'ana_menu'
        self.slider_secili = None
        self.kaydirma_baslangic = None

    def buton_ciz(self, text, y_pos, aktif=False, genislik=200, yukseklik=50):
        font = self.font_normal
        renk = MAVI if aktif else BEYAZ
        text_surface = font.render(text, True, renk)
        buton_rect = pygame.Rect(
            (self.ayarlar.ayarlar['pencere_genislik'] - genislik) // 2,
            y_pos,
            genislik,
            yukseklik
        )
        pygame.draw.rect(self.ayarlar.pencere, GRI if aktif else SIYAH, buton_rect, border_radius=10)
        pygame.draw.rect(self.ayarlar.pencere, renk, buton_rect, 2, border_radius=10)
        text_rect = text_surface.get_rect(center=buton_rect.center)
        self.ayarlar.pencere.blit(text_surface, text_rect)
        self.butonlar[text] = buton_rect
        return buton_rect

    def slider_ciz(self, text, y_pos, deger):
        font = self.font_normal
        text_surface = font.render(text, True, BEYAZ)
        self.ayarlar.pencere.blit(text_surface, (50, y_pos))
        
        slider_rect = pygame.Rect(300, y_pos + 10, 200, 10)
        pygame.draw.rect(self.ayarlar.pencere, GRI, slider_rect)
        
        deger_pos = 300 + (200 * deger)
        pygame.draw.circle(self.ayarlar.pencere, BEYAZ, (int(deger_pos), y_pos + 15), 10)
        return slider_rect

    def ana_menu_goster(self):
        self.ayarlar.pencere.fill(SIYAH)
        baslik = self.font_buyuk.render("Yılan Oyunu", True, YESIL)
        baslik_rect = baslik.get_rect(center=(self.ayarlar.ayarlar['pencere_genislik']//2, 100))
        self.ayarlar.pencere.blit(baslik, baslik_rect)

        self.buton_ciz("Oyuna Başla", 200)
        self.buton_ciz("Ayarlar", 300)
        self.buton_ciz("Çıkış", 400)

    def ayarlar_menu_goster(self):
        self.ayarlar.pencere.fill(SIYAH)
        baslik = self.font_buyuk.render("Ayarlar", True, BEYAZ)
        baslik_rect = baslik.get_rect(center=(self.ayarlar.ayarlar['pencere_genislik']//2, 50))
        self.ayarlar.pencere.blit(baslik, baslik_rect)

        # Ses ayarları
        self.slider_ciz("Ses Seviyesi", 150, self.ayarlar.ayarlar['ses_seviyesi'])
        self.slider_ciz("Müzik Seviyesi", 200, self.ayarlar.ayarlar['muzik_seviyesi'])

        # Çözünürlük seçenekleri
        self.buton_ciz("800x600", 300, self.ayarlar.ayarlar['pencere_genislik'] == 800)
        self.buton_ciz("1024x768", 370, self.ayarlar.ayarlar['pencere_genislik'] == 1024)
        self.buton_ciz("1280x720", 440, self.ayarlar.ayarlar['pencere_genislik'] == 1280)

        # Zorluk seçenekleri
        self.buton_ciz("Kolay", 510, self.ayarlar.ayarlar['zorluk'] == 'kolay')
        self.buton_ciz("Normal", 580, self.ayarlar.ayarlar['zorluk'] == 'normal')
        self.buton_ciz("Zor", 650, self.ayarlar.ayarlar['zorluk'] == 'zor')

        self.buton_ciz("Geri", 720)

    def menu_dongusu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.aktif_menu == 'ana_menu':
                        if self.butonlar["Oyuna Başla"].collidepoint(pos):
                            return True
                        elif self.butonlar["Ayarlar"].collidepoint(pos):
                            self.aktif_menu = 'ayarlar'
                        elif self.butonlar["Çıkış"].collidepoint(pos):
                            pygame.quit()
                            sys.exit()
                    
                    elif self.aktif_menu == 'ayarlar':
                        if self.butonlar["Geri"].collidepoint(pos):
                            self.aktif_menu = 'ana_menu'
                            self.ayarlar.ayarlari_kaydet()
                        elif self.butonlar["800x600"].collidepoint(pos):
                            self.ayarlar.ayarlar['pencere_genislik'] = 800
                            self.ayarlar.ayarlar['pencere_yukseklik'] = 600
                            self.ayarlar.guncelle_pencere()
                        elif self.butonlar["1024x768"].collidepoint(pos):
                            self.ayarlar.ayarlar['pencere_genislik'] = 1024
                            self.ayarlar.ayarlar['pencere_yukseklik'] = 768
                            self.ayarlar.guncelle_pencere()
                        elif self.butonlar["1280x720"].collidepoint(pos):
                            self.ayarlar.ayarlar['pencere_genislik'] = 1280
                            self.ayarlar.ayarlar['pencere_yukseklik'] = 720
                            self.ayarlar.guncelle_pencere()
                        elif self.butonlar["Kolay"].collidepoint(pos):
                            self.ayarlar.ayarlar['zorluk'] = 'kolay'
                        elif self.butonlar["Normal"].collidepoint(pos):
                            self.ayarlar.ayarlar['zorluk'] = 'normal'
                        elif self.butonlar["Zor"].collidepoint(pos):
                            self.ayarlar.ayarlar['zorluk'] = 'zor'

            if self.aktif_menu == 'ana_menu':
                self.ana_menu_goster()
            elif self.aktif_menu == 'ayarlar':
                self.ayarlar_menu_goster()

            pygame.display.flip()
            pygame.time.Clock().tick(60)

class Seviye:
    def __init__(self, hiz, yem_degeri, guc_up_olasiligi):
        self.hiz = hiz
        self.yem_degeri = yem_degeri
        self.guc_up_olasiligi = guc_up_olasiligi

SEVIYELER = {
    1: Seviye(10, 1, 0.1),
    2: Seviye(15, 2, 0.15),
    3: Seviye(20, 3, 0.2)
}

class GucUp(Enum):
    HIZLANMA = 1
    YAVASLAMA = 2
    EKSTRA_PUAN = 3

# Pencereyi oluştur
pygame.display.set_caption('Gelişmiş Yılan Oyunu')
saat = pygame.time.Clock()

class Yilan:
    def __init__(self, ayarlar):
        self.ayarlar = ayarlar
        self.pozisyon = [(ayarlar.ayarlar['pencere_genislik']//2, ayarlar.ayarlar['pencere_yukseklik']//2)]
        self.yon = [IZGARA_BOYUT, 0]
        self.uzunluk = 1
        self.hiz_carpani = 1
        self.guc_up_suresi = 0
        self.aktif_guc = None

    def hareket_et(self):
        yeni_bas = (
            self.pozisyon[0][0] + self.yon[0],
            self.pozisyon[0][1] + self.yon[1]
        )
        self.pozisyon.insert(0, yeni_bas)
        if len(self.pozisyon) > self.uzunluk:
            self.pozisyon.pop()

    def yem_ye(self):
        self.uzunluk += 1

    def kendine_carpti_mi(self):
        return self.pozisyon[0] in self.pozisyon[1:]

    def duvara_carpti_mi(self):
        x, y = self.pozisyon[0]
        return (x < 0 or x >= self.ayarlar.ayarlar['pencere_genislik'] or 
                y < 0 or y >= self.ayarlar.ayarlar['pencere_yukseklik'])

    def guc_up_uygula(self, guc):
        self.aktif_guc = guc
        self.guc_up_suresi = 150  # 10 saniye
        if guc == GucUp.HIZLANMA:
            self.hiz_carpani = 1.5
        elif guc == GucUp.YAVASLAMA:
            self.hiz_carpani = 0.7

    def guc_up_guncelle(self):
        if self.guc_up_suresi > 0:
            self.guc_up_suresi -= 1
            if self.guc_up_suresi == 0:
                self.hiz_carpani = 1
                self.aktif_guc = None

class Oyun:
    def __init__(self, ayarlar):
        self.ayarlar = ayarlar
        self.en_yuksek_skor = self.en_yuksek_skoru_yukle()
        self.ses_efektleri = {
            'yem': pygame.mixer.Sound('sesler/yem.wav') if os.path.exists('sesler/yem.wav') else None,
            'guc_up': pygame.mixer.Sound('sesler/guc_up.wav') if os.path.exists('sesler/guc_up.wav') else None,
            'game_over': pygame.mixer.Sound('sesler/game_over.wav') if os.path.exists('sesler/game_over.wav') else None
        }
        self.ses_seviyesini_ayarla()

    def ses_seviyesini_ayarla(self):
        for ses in self.ses_efektleri.values():
            if ses:
                ses.set_volume(self.ayarlar.ayarlar['ses_seviyesi'])

    def en_yuksek_skoru_yukle(self):
        try:
            with open('en_yuksek_skor.json', 'r') as f:
                return json.load(f)['en_yuksek_skor']
        except:
            return 0

    def en_yuksek_skoru_kaydet(self, skor):
        if skor > self.en_yuksek_skor:
            self.en_yuksek_skor = skor
            with open('en_yuksek_skor.json', 'w') as f:
                json.dump({'en_yuksek_skor': skor}, f)

def yem_olustur(yilan):
    while True:
        x = random.randrange(0, yilan.ayarlar.ayarlar['pencere_genislik'], IZGARA_BOYUT)
        y = random.randrange(0, yilan.ayarlar.ayarlar['pencere_yukseklik'], IZGARA_BOYUT)
        if (x, y) not in yilan.pozisyon:
            return (x, y)

def guc_up_olustur(yilan, seviye):
    if random.random() < seviye.guc_up_olasiligi:
        while True:
            x = random.randrange(0, yilan.ayarlar.ayarlar['pencere_genislik'], IZGARA_BOYUT)
            y = random.randrange(0, yilan.ayarlar.ayarlar['pencere_yukseklik'], IZGARA_BOYUT)
            if (x, y) not in yilan.pozisyon:
                return (x, y), random.choice(list(GucUp))
    return None, None

def oyunu_baslat(ayarlar):
    oyun = Oyun(ayarlar)
    yilan = Yilan(ayarlar)
    seviye_no = 1
    seviye = SEVIYELER[seviye_no]
    yem = yem_olustur(yilan)
    guc_up_poz, aktif_guc = guc_up_olustur(yilan, seviye)
    skor = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and yilan.yon != [0, IZGARA_BOYUT]:
                    yilan.yon = [0, -IZGARA_BOYUT]
                elif event.key == pygame.K_DOWN and yilan.yon != [0, -IZGARA_BOYUT]:
                    yilan.yon = [0, IZGARA_BOYUT]
                elif event.key == pygame.K_LEFT and yilan.yon != [IZGARA_BOYUT, 0]:
                    yilan.yon = [-IZGARA_BOYUT, 0]
                elif event.key == pygame.K_RIGHT and yilan.yon != [-IZGARA_BOYUT, 0]:
                    yilan.yon = [IZGARA_BOYUT, 0]

        yilan.hareket_et()
        yilan.guc_up_guncelle()

        # Çarpışma kontrolleri
        if yilan.kendine_carpti_mi() or yilan.duvara_carpti_mi():
            if oyun.ses_efektleri['game_over']:
                oyun.ses_efektleri['game_over'].play()
            oyun.en_yuksek_skoru_kaydet(skor)
            return skor

        # Yem yeme kontrolü
        if yilan.pozisyon[0] == yem:
            if oyun.ses_efektleri['yem']:
                oyun.ses_efektleri['yem'].play()
            yilan.yem_ye()
            skor += seviye.yem_degeri
            yem = yem_olustur(yilan)
            
            # Seviye kontrolü
            if skor >= 20 and seviye_no == 1:
                seviye_no = 2
                seviye = SEVIYELER[seviye_no]
            elif skor >= 50 and seviye_no == 2:
                seviye_no = 3
                seviye = SEVIYELER[seviye_no]

        # Güç-up kontrolü
        if guc_up_poz and yilan.pozisyon[0] == guc_up_poz:
            if oyun.ses_efektleri['guc_up']:
                oyun.ses_efektleri['guc_up'].play()
            yilan.guc_up_uygula(aktif_guc)
            guc_up_poz, aktif_guc = None, None

        if not guc_up_poz:
            guc_up_poz, aktif_guc = guc_up_olustur(yilan, seviye)

        # Ekranı temizle
        ayarlar.pencere.fill(SIYAH)

        # Yemi çiz
        pygame.draw.rect(ayarlar.pencere, KIRMIZI, (yem[0], yem[1], IZGARA_BOYUT, IZGARA_BOYUT))

        # Güç-up'ı çiz
        if guc_up_poz:
            pygame.draw.rect(ayarlar.pencere, ALTIN, (guc_up_poz[0], guc_up_poz[1], IZGARA_BOYUT, IZGARA_BOYUT))

        # Yılanı çiz
        for segment in yilan.pozisyon:
            renk = MAVI if yilan.aktif_guc else YESIL
            pygame.draw.rect(ayarlar.pencere, renk, (segment[0], segment[1], IZGARA_BOYUT, IZGARA_BOYUT))

        # Bilgileri göster
        font = pygame.font.Font(None, 36)
        skor_text = font.render(f'Skor: {skor}', True, BEYAZ)
        en_yuksek_text = font.render(f'En Yüksek: {oyun.en_yuksek_skor}', True, BEYAZ)
        seviye_text = font.render(f'Seviye: {seviye_no}', True, BEYAZ)
        
        ayarlar.pencere.blit(skor_text, (10, 10))
        ayarlar.pencere.blit(en_yuksek_text, (10, 50))
        ayarlar.pencere.blit(seviye_text, (10, 90))

        if yilan.aktif_guc:
            guc_text = font.render(f'Güç: {yilan.aktif_guc.name}', True, ALTIN)
            ayarlar.pencere.blit(guc_text, (10, 130))

        pygame.display.flip()
        saat.tick(int(seviye.hiz * yilan.hiz_carpani))

def main():
    ayarlar = Ayarlar()
    menu = Menu(ayarlar)
    
    while True:
        if menu.menu_dongusu():
            skor = oyunu_baslat(ayarlar)
            menu.aktif_menu = 'ana_menu'

if __name__ == '__main__':
    main() 