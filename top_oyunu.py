import sys
import pygame
import random


pygame.init()

genislik = 920
yukseklik = 624
FPS = 30
oyuncu_deger = 10
deger = 8
f_skor = 0
k_skor = 0

dx = random.choice([-1, 1])
dy = random.choice([-1, 1])
saat = pygame.time.Clock()
goruntu_yuzeyi = pygame.display.set_mode((genislik, yukseklik))

futbolcu = pygame.image.load("goalkeeper.png")
futbolcu_koordinati = futbolcu.get_rect()
futbolcu_koordinati.center = (genislik//2+400, yukseklik//2)

kaleci = pygame.image.load("vietnam.png")
kaleci_koordinati = kaleci.get_rect()
kaleci_koordinati.center = (genislik//2-400, yukseklik//2)

arka_plan = pygame.image.load("saha_2.png")
arka_plan_koordinati = arka_plan.get_rect()
arka_plan_koordinati.topleft = (0, 0)

top = pygame.image.load("football.png")
top_koordinati = top.get_rect()
top_koordinati.center = (random.randint(0+50, genislik-50), random.randint(0+50, yukseklik-50))

ses_efekti = pygame.mixer.Sound("top_sesi.wav")

font = pygame.font.SysFont("arial", 32)


while True:
    for etkinlik in pygame.event.get():
        if etkinlik.type == pygame.QUIT:
            sys.exit()

        if etkinlik.type == pygame.KEYDOWN:
            if etkinlik.key == pygame.K_ESCAPE:
                durum = False
            if etkinlik.key == pygame.K_o:
                oyuncu_deger *= 2

            if etkinlik.key == pygame.K_p:
                oyuncu_deger /= 2

            if etkinlik.key == pygame.K_SPACE:
                futbolcu_koordinati.center = (genislik // 2+400, yukseklik // 2)
                kaleci_koordinati.center = (genislik // 2-400, yukseklik // 2)

    tuslar = pygame.key.get_pressed()

    if tuslar[pygame.K_UP] and futbolcu_koordinati.top > 0:
        futbolcu_koordinati.y -= oyuncu_deger

    elif tuslar[pygame.K_DOWN] and futbolcu_koordinati.bottom < yukseklik:
        futbolcu_koordinati.y += oyuncu_deger

    elif tuslar[pygame.K_w] and kaleci_koordinati.top > 0:
        kaleci_koordinati.y -= oyuncu_deger

    elif tuslar[pygame.K_s] and kaleci_koordinati.bottom < yukseklik:
        kaleci_koordinati.y += oyuncu_deger

    top_koordinati.x += deger * dx
    top_koordinati.y += deger * dy

    if top_koordinati.left < 0:
        top_koordinati.center = (random.randint(50, genislik-50), random.randint(50, yukseklik-50))
        f_skor += 1
        deger = 8

    if top_koordinati.right > genislik:
        top_koordinati.center = (random.randint(50, genislik-50), random.randint(50, yukseklik-50))
        k_skor += 1
        deger = 8


    if top_koordinati.top < 40:
        dy = -dy

    if top_koordinati.bottom > yukseklik - 50:
        dy = -dy

    if futbolcu_koordinati.colliderect(top_koordinati):
        ses_efekti.play()
        dx = -dx
        deger += 1

    if kaleci_koordinati.colliderect(top_koordinati):
        ses_efekti.play()
        dx = -dx
        deger += 1

    futbolcu_skor = font.render("1_PLEYER_SKOR:" + str(f_skor), True, (0, 0, 0),(250,250,250))
    futbolcu_skor_koordinati = futbolcu_skor.get_rect()
    futbolcu_skor_koordinati.topleft = (0, 0)

    kaleci_skor = font.render("2_PLEYER_SKOR:" + str(k_skor), True, (0, 0, 0),(250, 250, 250))
    kaleci_skor_koordinati = kaleci_skor.get_rect()
    kaleci_skor_koordinati.topright = (genislik - 0, 0)

    goruntu_yuzeyi.blit(arka_plan, arka_plan_koordinati)
    goruntu_yuzeyi.blit(futbolcu_skor, futbolcu_skor_koordinati)
    goruntu_yuzeyi.blit(kaleci_skor, kaleci_skor_koordinati)
    goruntu_yuzeyi.blit(top, top_koordinati)
    goruntu_yuzeyi.blit(kaleci, kaleci_koordinati)
    goruntu_yuzeyi.blit(futbolcu, futbolcu_koordinati)
    pygame.display.update()
    saat.tick(FPS)

pygame.quit()
