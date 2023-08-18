import pygame
import random
import cv2
import mediapipe
import numpy

pygame.init()

FPS = 200
saat = pygame.time.Clock()

dosya = cv2.VideoCapture(0)
dosya.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
dosya.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

genislik = 1280
yukseklik = 720

skor = 0
cani = 3
deger = 8




dx = random.choice([-1, 1])
dy = random.choice([-1, 1])

goruntu_yuzeyi = pygame.display.set_mode((genislik, yukseklik))

karakter = pygame.image.load("goblin.png")
karakter_koordinati = karakter.get_rect()
x = 500
y = 300

zehir = pygame.image.load("zehir.png")
zehir_koordinati = zehir.get_rect()
zehir_koordinati.center = (random.randint(50, genislik - 50), random.randint(50, yukseklik - 50))
zehir_dx, zehir_dy = random.choice([(1, 1), (-1, 1), (1, -1), (-1, -1)])
zehir_hiz = 2

can = pygame.image.load("meat.png")
can_koordinati = can.get_rect()
can_koordinati.center = (random.randint(50, genislik - 50), random.randint(50, yukseklik - 50))
can_dx, can_dy = random.choice([(1, 1), (-1, 1), (1, -1), (-1, -1)])

para = pygame.image.load("coin.png")
para_koordinati = para.get_rect()
para_koordinati.center = (random.randint(50, genislik - 50), random.randint(50, yukseklik - 50))
para_dx, para_dy = random.choice([(1, 1), (-1, 1), (1, -1), (-1, -1)])

arka_plan = pygame.image.load("zindan.jpg")
arka_plan_koordinati = arka_plan.get_rect()
arka_plan_koordinati.topleft = (0, 0)


font = pygame.font.SysFont("arial", 32)

skor_metni = font.render("SKOR:" + str(skor), True, (255, 50, 185), (250, 250, 250))
skor_koordinati = skor_metni.get_rect()
skor_koordinati.topright = (genislik - 10, 10)

can_metni = font.render("CAN:" + str(cani), True, (255, 50, 185), (250, 250, 250))
canimiz_koordinati = can_metni.get_rect()
canimiz_koordinati.topright = (genislik - 0, 40)

ses_efekti1 = pygame.mixer.Sound("arka_ses.wav")
ses_efekti2 = pygame.mixer.Sound("para_ses.wav")
ses_efekti3 = pygame.mixer.Sound("et_ses.wav")
ses_efekti4 = pygame.mixer.Sound("zehir_ses.wav")
ses_efekti1.play(-1)

el_model = mediapipe.solutions.hands


with el_model.Hands(min_tracking_confidence=0.5, min_detection_confidence=0.5) as el:
    while True:
        kontrol, webcam = dosya.read()
        yukseklik, genislik, kanal = webcam.shape
        rgb = cv2.cvtColor(webcam, cv2.COLOR_BGR2RGB)
        sonuc = el.process(rgb)
        if sonuc.multi_hand_landmarks:
            for hand_mark in sonuc.multi_hand_landmarks:
                for koordinat in el_model.HandLandmark:

                    mark = hand_mark.landmark[8]
                    x = int(mark.x*genislik)
                    y = int(mark.y*yukseklik)

        karakter_koordinati.center = (x, y)
        rgb = numpy.rot90(rgb)
        web_cam_goruntu_yuzeyi = pygame.surfarray.make_surface(rgb).convert()
        web_cam_goruntu_yuzeyi = pygame.transform.flip(web_cam_goruntu_yuzeyi, True, False)


        if karakter_koordinati.colliderect(para_koordinati):
            skor += 1
            """zehir_hiz += 1"""
            ses_efekti2.play()
            para_koordinati.x = random.randint(50, genislik - 50)
            para_koordinati.y = random.randint(50, yukseklik - 50)

        if karakter_koordinati.colliderect(zehir_koordinati):
            cani -= 1
            """zehir_hiz -= 1"""
            ses_efekti4.play()
            zehir_koordinati.x = random.randint(50, genislik - 50)
            zehir_koordinati.y = random.randint(50, yukseklik - 50)

        if karakter_koordinati.colliderect(can_koordinati):
            cani += 1
            """zehir_hiz += 1.5"""
            ses_efekti3.play()
            can_koordinati.x = random.randint(50, genislik - 50)
            can_koordinati.y = random.randint(50, yukseklik - 50)

        zehir_koordinati.x += zehir_dx * zehir_hiz
        zehir_koordinati.y += zehir_dy * zehir_hiz
        if zehir_koordinati.left < 0 or zehir_koordinati.right > genislik:
            zehir_dx = -1 * zehir_dx
        if zehir_koordinati.top < 0 or zehir_koordinati.bottom > yukseklik:
            zehir_dy = -1 * zehir_dy

        skor_metni = font.render("SKOR:" + str(skor), True, (255, 50, 185), (250, 250, 250))
        can_metni = font.render("CAN:" + str(cani), True, (255, 50, 185), (250, 250, 250))

        if cani == 0:
            durum = False


        goruntu_yuzeyi.blit(web_cam_goruntu_yuzeyi, (0, 0))
        goruntu_yuzeyi.blit(skor_metni, skor_koordinati)
        goruntu_yuzeyi.blit(can_metni, canimiz_koordinati)
        goruntu_yuzeyi.blit(karakter, karakter_koordinati)
        goruntu_yuzeyi.blit(zehir, zehir_koordinati)
        goruntu_yuzeyi.blit(can, can_koordinati)
        goruntu_yuzeyi.blit(para, para_koordinati)
        pygame.display.update()
        saat.tick(FPS)
pygame.quit()
