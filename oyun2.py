import pygame
import random

# Pygame hazırlık
pygame.init()

# Pencere oluşturuyorum
genislik, yukseklik = 1200, 750
pencere = pygame.display.set_mode((genislik, yukseklik))

# FPS değeri giriyoruz oyundaki akıcılık
FPS = 60
saat = pygame.time.Clock()

# Sınıfları oluşturuyorum
class oyun():
    def __init__(self, oyuncu, uzayli_grup, oyuncu_mermi_grup, uzayli_mermi_grup):
        # Oyun değişkenleri
        self.bolum_no = 1
        self.puan = 0
        # Nesneleri tanımlama
        self.oyuncu = oyuncu
        self.uzayli_grup = uzayli_grup 
        self.oyuncu_mermi_grup = oyuncu_mermi_grup
        self.uzayli_mermi_grup = uzayli_mermi_grup
        # Arka plan koyma
        self.arka_plan1 = pygame.image.load("arka_plan1.png")
        self.arka_plan2 = pygame.image.load("arka_plan2.jpg")
        self.arka_plan3 = pygame.image.load("arka_plan3.png")
        self.tebrikler = pygame.image.load("tebrikler.png")
        # Şarkı ve ses efektleri
        self.uzayli_vurus = pygame.mixer.Sound("uzayli_vurus.wav")
        self.oyuncu_vurus = pygame.mixer.Sound("oyuncu_vurus.wav")
        
        

        self.sarkilar = [
            "altaylardan tunaya.wav",  # Bölüm 1 için şarkı
            "olurum.wav",        # Bölüm 2 için şarkı
            "deniz.wav",        # Bölüm 3 için şarkı
            
        ]
        
        # Başlangıç müziği
        pygame.mixer.music.load(self.sarkilar[0])  # İlk bölüm için şarkıyı başlat
        pygame.mixer.music.play(-1)
        #font eklemek
        self.oyun_font=pygame.font.Font("oyun_font.ttf",64)

    def update(self):
        self.uzayli_konum_degistirme()
        self.temas()
        self.tamamlandi()

    def cizdir(self):
        puan_yazi=self.oyun_font.render("SKOR:"+str(self.puan),True,(255,0,255),(0,0,0))
        puan_yazi_konum=puan_yazi.get_rect()
        puan_yazi_konum.topleft=(10,10)

        bolum_no_yazi=self.oyun_font.render("Bölüm"+str(self.bolum_no),True,(255,0,255),(0,0,0))
        bolum_no_yazi_konum=bolum_no_yazi.get_rect()
        bolum_no_yazi_konum.topleft=(genislik-250,10)
        if self.bolum_no==1:
            pencere.blit(self.arka_plan1,(0,0))
        elif self.bolum_no==2:
            pencere.blit(self.arka_plan2,(0,0))
        elif self.bolum_no==3:
            pencere.blit(self.arka_plan3,(0,0))
        elif self.bolum_no==4:
            self.bitir()
        pencere.blit(puan_yazi,puan_yazi_konum)
        pencere.blit(bolum_no_yazi,bolum_no_yazi_konum)

    def uzayli_konum_degistirme(self):
        hareket,carpisma=False,False
        for uzayli in self.uzayli_grup.sprites():
            if uzayli.rect.left<=0 or uzayli.rect.right >= genislik:
                hareket=True
        if hareket==True:
            for uzayli in self.uzayli_grup.sprites():
                uzayli.rect.y+=50 *self.bolum_no
                uzayli.yon*=-1
                if uzayli.rect.bottom>=yukseklik-70:
                    carpisma=True
        if carpisma==True:
            self.oyuncu.can-=1
            self.oyun_durumu()
    def temas(self):
        if pygame.sprite.groupcollide(self.oyuncu_mermi_grup,self.uzayli_grup,True,True):
            self.oyuncu_vurus.play()
            self.puan+=100*self.bolum_no
        if pygame.sprite.spritecollide(self.oyuncu,self.uzayli_mermi_grup,True):
            self.uzayli_vurus.play()
            self.oyuncu.can-=1
            self.oyun_durumu()


    def bitir(self):
        bittimi=True
        pencere.blit(self.tebrikler,(0,0))
        pygame.display.update()
        while bittimi:
            for etkinlik in pygame.event.get():
                if etkinlik.type==pygame.KEYDOWN:
                    if etkinlik.key==pygame.K_RETURN:
                        self.oyun_reset()
                        bittimi=False

    def bolum(self):
        for i in range(10):
            for j in range(5):
                uzayli=Uzayli(64+i*64,100+j*64,self.bolum_no,self.uzayli_mermi_grup)
                self.uzayli_grup.add(uzayli)

    def oyun_durumu(self):
        self.uzayli_mermi_grup.empty()
        self.oyuncu_mermi_grup.empty()
        self.oyuncu.reset()
        for uzayli in self.uzayli_grup.sprites():
            uzayli.reset()
        if self.oyuncu.can==0:
            self.oyun_reset()
        else:
            self.durdur()

    def tamamlandi(self):
        if not self.uzayli_grup:
            self.bolum_no+=1
            self.bolum()
            if self.bolum_no == 2:
                pygame.mixer.music.load(self.sarkilar[1])  # 2. bölüm için müzik
                pygame.mixer.music.play(-1)  # Sonsuz çal

            elif self.bolum_no == 3:
                pygame.mixer.music.load(self.sarkilar[2])  # 3. bölüm için müzik
                pygame.mixer.music.play(-1)  # Sonsuz çal

    def durdur(self):
        durdurumu=True
        global durum
        yazi1=self.oyun_font.render("Uzaylılar yüzünden "+str(self.oyuncu.can)+" Canınız Kaldı! ",True,(0,110,0),(255,0,0))
        yazi1_konum=yazi1.get_rect()
        yazi1_konum.topleft=(100,150)
        
        yazi2=self.oyun_font.render("Devam etmek için 'Enter' tuşuna basınız",True,(0,110,0),(255,0,0))
        yazi2_konum=yazi2.get_rect()
        yazi2_konum.topleft=(100,250)

        pencere.blit(yazi1,yazi1_konum)
        pencere.blit(yazi2,yazi2_konum)
        pygame.display.update()

        while durdurumu:
            for etkinlik in pygame.event.get():
                if etkinlik.type==pygame.KEYDOWN:
                    if etkinlik.key==pygame.K_RETURN:
                        durdurumu=False
                if etkinlik.type==pygame.QUIT:
                    durdurumu=False
                    durum=False


    def oyun_reset(self):
        #oyun degıskenlerı
        self.bolum_no=1
        self.puan=0
        self.oyuncu.can=5
        #grupları temızlemek
        self.uzayli_grup.empty()
        self.uzayli_mermi_grup.empty()
        self.oyuncu_mermi_grup.empty()
        self.bolum()
        pygame.mixer.music.load(self.sarkilar[0])  #sarkıyı bastan baslatmak ıcın 
        pygame.mixer.music.play(-1)

class oyuncu(pygame.sprite.Sprite):   #burada sprite ı kalıtım olarak kullanıyoruz cunku çoklu dusmanları oldurebılmeyı ve karakterımızı gormemız fonksıyonları kullanmamız gerekıyor o yuzden kullanıyoruz
    def __init__(self, oyuncuMermi_grup):
        super().__init__()
        self.image = pygame.image.load("uzay_gemi.png")
        self.rect = self.image.get_rect() #oyuncunun hareket edebılmesı ıcın 
        self.oyuncuMermi_grup = oyuncuMermi_grup   #oyuncu mermısını burda tanımlıyoruz cunku mermının konumunu ayarlarken  orıjın noktası yanı gemının ana noktasından alması ıcın parametrelerı buna verecegız 
        self.rect.centerx = genislik / 2    #oyuncunun başlama konumu
        self.rect.top = yukseklik - 70

        # Oyuncu değişkenleri
        self.hiz = 10
        self.can = 5
        # Mermi ses efekti koymak için
        self.mermi_sesi = pygame.mixer.Sound("oyuncu_mermi.wav")

    def update(self):   #sprite dan gelen fonksıyon bu kalıtımın ozellıgı 
        tus = pygame.key.get_pressed()  #tusa basılıp basılmadıgını kontrol eder 
        if tus[pygame.K_LEFT] and self.rect.left >= 0:    #en sola gıdınce duracak
            self.rect.x -= self.hiz
        if tus[pygame.K_RIGHT] and self.rect.right <= genislik:   #en saga gıdınce duracak
            self.rect.x += self.hiz

    def ates(self):
        if len(self.oyuncuMermi_grup) < 4:
            # Yeni mermi nesnesi oluşturuluyor ve gruba ekleniyor
            oyuncuMermi(self.rect.centerx, self.rect.top, self.oyuncuMermi_grup)  #mermı gemının orta noktasından cıkıyor 
            self.mermi_sesi.play()  # Ses çalınıyor

    def reset(self):
        self.rect.centerx = genislik // 2

class Uzayli(pygame.sprite.Sprite):
    def __init__(self, x, y, hiz, mermi_grup):
        super().__init__()
        self.image = pygame.image.load("uzayli.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        # Uzaylıya özel değişkenler
        self.basx = x
        self.basy = y
        self.yon = 1
        self.hiz = hiz
        self.mermi_grup = mermi_grup
        self.uzayli_mermi_sesi = pygame.mixer.Sound("uzayli_mermi.wav")
    
    def update(self):
        self.rect.x += self.yon * self.hiz
        if random.randint(0, 100) > 98 and len(self.mermi_grup) < 3:  # Burada yüzde 2 ihtimalle mermi atılıyor
            self.uzayli_mermi_sesi.play()  # Ses çalınıyor
            self.ates()

    def ates(self):
        # Uzaylı mermisi oluşturuluyor
        uzayliMermi(self.rect.centerx, self.rect.bottom, self.mermi_grup)

    def reset(self):
        self.rect.topleft = (self.basx, self.basy)
        self.yon = 1

class oyuncuMermi(pygame.sprite.Sprite):
    def __init__(self, x, y, oyuncuMermi_grup):
        super().__init__()
        self.image = pygame.image.load("oyuncu_mermi.png")
        self.rect = self.image.get_rect()  #mermının konumunu ayarlıyoruz   
        self.rect.centerx = x
        self.rect.centery = y
        # Mermi değişkeni
        self.hiz = 10
        # Mermi grup nesnesine ekleniyor
        oyuncuMermi_grup.add(self)

    def update(self):
        self.rect.y -= self.hiz
        if self.rect.bottom < 0:   #mermı ekrandan cıkıyorsa 
            self.kill()

class uzayliMermi(pygame.sprite.Sprite):
    def __init__(self, x, y, mermi_grup):
        super().__init__()
        self.image = pygame.image.load("uzayli_mermi.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        mermi_grup.add(self)
        self.hiz = 10

    def update(self):
        self.rect.y += self.hiz
        if self.rect.top > yukseklik:  # Burada doğru koşul
            self.kill()
#Bu yazdıklarımızı Group ıcıne almamız gerekıyor sprite diye tanımladıgın sınıfları yonetırken kolaylık saglıyor uzaylılar mesela bırden fazla oldukları ıcın group ıcıne alarak hepsını ortak hareket ettırebılıyorum
# Mermi grup    
oyuncuMermi_grup = pygame.sprite.Group()
uzayli_mermi_grup = pygame.sprite.Group()

# Oyuncu tanımlama
oyuncu_grup = pygame.sprite.Group()
oyuncu = oyuncu(oyuncuMermi_grup)
oyuncu_grup.add(oyuncu)

# Uzaylı grubu
uzayli_grup = pygame.sprite.Group()

# Oyun sınıfı
oyun = oyun(oyuncu, uzayli_grup, oyuncuMermi_grup, uzayli_mermi_grup)
oyun.bolum()


# Oyun döngüsü ne zaman devam edecek duracak
durum = True
oyun_baslatildi = False  # Oyun başlangıcını kontrol etmek için bir bayrak değişkeni ekliyoruz.

while durum:
    for etkinlik in pygame.event.get():
        if etkinlik.type == pygame.QUIT:
            durum = False
        if etkinlik.type == pygame.KEYDOWN:  #bır tusa basııp basılmadıgını kontrol eder basıldıysa asagıdakı olusturacagım ıflerle ıstedıgım tussa ıslemı yapmasını soyleyecegım 
            if not oyun_baslatildi:  # Oyun başlatılmadıysa
                oyun_baslatildi = True  # Oyun başlatıldı
            elif etkinlik.key == pygame.K_SPACE:  # Boşluk tuşuna basıldığında ateş etsin
                oyuncu.ates()

    if oyun_baslatildi:  # Eğer oyun başladıysa, oyunun geri kalan kısmı çalışacak
        oyun.update()
        oyun.cizdir()

        oyuncu_grup.update()
        oyuncu_grup.draw(pencere)

        oyuncuMermi_grup.update()
        oyuncuMermi_grup.draw(pencere)

        uzayli_grup.update()
        uzayli_grup.draw(pencere)

        uzayli_mermi_grup.update()
        uzayli_mermi_grup.draw(pencere)

    else:  # Eğer oyun başlamamışsa, başlangıç ekranı gösterilecek
        baslangic_mesaji = oyun.oyun_font.render("Başlamak için bir tuşa basınız", True, (255, 255, 255))
        baslangic_mesaji_konum = baslangic_mesaji.get_rect(center=(genislik // 2, yukseklik // 2))
        pencere.fill((0, 0, 0))  # Arka planı siyah yap
        pencere.blit(baslangic_mesaji, baslangic_mesaji_konum)
    
    pygame.display.update()
    saat.tick(FPS)

pygame.quit()
