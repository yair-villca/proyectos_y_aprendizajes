import pygame
import os
import sys
import random
from config import *
from Snake_Bullet import SnakeBullet
from Wolf_Bullet import WolfBullet
from GreenRay_Bullet import GreenRayBullet
from player import Player
from GloboEnemy import GloboEnemy
from BatEnemy import BatEnemy




pygame.init()
screen = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Dark Shadow")
clock = pygame.time.Clock()

try:
    MENU_BG_IMG = pygame.image.load('assets/images/fondo_menu.png').convert()
    MENU_BACKGROUND = pygame.transform.scale(MENU_BG_IMG, (ANCHO, ALTO))
except:
    MENU_BACKGROUND = None

niveles = [
    {
        "nombre": "Nivel 1",
        "fondo": "assets/images/fondo_nivel_1.png",
        "bala": "snake",
        "enemigo_clase": GloboEnemy,
        "enemigo_velocidad": 3,
        "enemigo_cantidad": 5,
        "puntos_siguiente": 200,
        "fuente": "assets/fuentes/Minecraft.ttf",
        "mensaje": ("¡Adquiriste un escudo!", "Escudo de lobos 🐺")
    },
    {
        "nombre": "Nivel 2",
        "fondo": "assets/images/fondo_nivel_2.jpg",
        "bala": "wolf",
        "enemigo_clase": GloboEnemy,
        "enemigo_velocidad": 4.5,
        "enemigo_cantidad": 10,
        "puntos_siguiente": 400,
        "fuente": "assets/fuentes/Minecraft.ttf",
        "mensaje": ("¡Adquiriste un escudo!", "Escudo de Espíritu de Tortuga")
    },
    {
        "nombre": "Nivel 3",
        "fondo": "assets/images/fondo_nivel_3.png",
        "bala": "greenray",
        "enemigo_clase": BatEnemy,
        "enemigo_velocidad": 6.5,
        "enemigo_cantidad": 4,
        "puntos_siguiente": 700,
        "fuente": "assets/fuentes/Minecraft.ttf"
    }
]

nivel_actual = 1
game_state = ESTADO_MENU
ESTADO_GAME_OVER = 3

all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player = None

nivel_backgrounds = []
for n in niveles:
    try:
        img = pygame.image.load(n["fondo"]).convert()
        img = pygame.transform.scale(img, (ANCHO, ALTO))
    except:
        img = pygame.Surface((ANCHO, ALTO))
        img.fill((50, 50, 150))
    nivel_backgrounds.append(img)

def draw_text(surf, text, size, x, y, font_path='assets/fuentes/Minecraft.ttf', color=BLANCO):
    font = pygame.font.Font(font_path, size)
    txt = font.render(text, True, color)
    rect = txt.get_rect()
    rect.midtop = (x, y)
    surf.blit(txt, rect)

def show_start_screen():
    if MENU_BACKGROUND:
        screen.blit(MENU_BACKGROUND, (0, 0))
    else:
        screen.fill(NEGRO)
    draw_text(screen, "Presiona cualquier tecla para comenzar", 20, ANCHO//2, ALTO//1.1)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                waiting = False

def spawn_enemy():
    nivel_data = niveles[nivel_actual - 1]
    cls = nivel_data["enemigo_clase"]
    vel = nivel_data["enemigo_velocidad"]
    side = random.choice(['top', 'bottom', 'left', 'right'])
    if side == 'top':
        x, y = random.randrange(ANCHO), -100
    elif side == 'bottom':
        x, y = random.randrange(ANCHO), ALTO + 100
    elif side == 'left':
        x, y = -100, random.randrange(ALTO)
    else:
        x, y = ANCHO + 100, random.randrange(ALTO)
    e = cls(x, y, player)
    e.base_velocidad = vel
    all_sprites.add(e)
    enemies.add(e)

running = True
#bucle principal
while running:
    if game_state == ESTADO_MENU:
        show_start_screen()
        all_sprites.empty()
        bullets.empty()
        enemies.empty()
        clock.tick(0)
        pygame.event.clear()
        player = Player()
        all_sprites.add(player)
        for _ in range(niveles[nivel_actual - 1]["enemigo_cantidad"]):
            spawn_enemy()
        game_state = ESTADO_JUEGO

    elif game_state == ESTADO_JUEGO:
        nivel_data = niveles[nivel_actual - 1]

        golpes = pygame.sprite.spritecollide(player, enemies, True)
        for _ in golpes:
            player.vida -= 1
            spawn_enemy()

        if player.vida <= 0:
            game_state = ESTADO_GAME_OVER
            continue

        player.speed_x = player.speed_y = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: player.speed_x = -player.velocidad
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: player.speed_x = player.velocidad
        if keys[pygame.K_UP] or keys[pygame.K_w]: player.speed_y = -player.velocidad
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: player.speed_y = player.velocidad

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                if nivel_data["bala"] == "snake":
                    b = SnakeBullet(player.rect.centerx, player.rect.centery, mx, my)
                elif nivel_data["bala"] == "wolf":
                    b = WolfBullet(player.rect.centerx, player.rect.centery, mx, my)
                elif nivel_data["bala"] == "greenray":
                    b = GreenRayBullet(player.rect.centerx, player.rect.centery, mx, my)
                else:
                    b = SnakeBullet(player.rect.centerx, player.rect.centery, mx, my)
                all_sprites.add(b)
                bullets.add(b)

        all_sprites.update()

        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for _ in hits:
            player.score += 50
            spawn_enemy()

        if nivel_actual < len(niveles) and player.score >= nivel_data["puntos_siguiente"]:
            nivel_actual += 1
            enemies.empty()
            for _ in range(niveles[nivel_actual - 1]["enemigo_cantidad"]):
                spawn_enemy()

        fondo = nivel_backgrounds[nivel_actual - 1]
        screen.blit(fondo, (0, 0))
        all_sprites.draw(screen)
        draw_text(screen, niveles[nivel_actual - 1]["nombre"], 30, ANCHO - 100, 10)
        draw_text(screen, f"Puntuación: {player.score}", 30, ANCHO // 2, 10)
        draw_text(screen, f"Vidas: {player.vida}", 30, 100, 10)
        pygame.display.flip()

    elif game_state == ESTADO_GAME_OVER:
        screen.fill((0, 0, 0))
        draw_text(screen, "GAME OVER", 60, ANCHO // 2, ALTO // 3)
        draw_text(screen, "Presiona cualquier tecla para reiniciar", 25, ANCHO // 2, ALTO // 2)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                    nivel_actual = 1
                    player = Player()
                    all_sprites.empty(); enemies.empty(); bullets.empty()
                    all_sprites.add(player)
                    for _ in range(niveles[nivel_actual - 1]["enemigo_cantidad"]):
                        spawn_enemy()
                    waiting = False
                    game_state = ESTADO_JUEGO

    clock.tick(60)

pygame.quit()
sys.exit()
