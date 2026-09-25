import pygame
import os
import math
from config import *
from Snake_Bullet import SnakeBullet

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.vida = 50
        self.ancho_sprite = 85
        self.alto_sprite = 85
        self.velocidad = 5
        self.speed_x = 0
        self.speed_y = 0
        self.facing = 'down'
        self.animations = self.load_animations()
        self.current_animation = self.animations['idle']
        self.image = self.current_animation
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.centery = ALTO // 2
        self.last_shot_time = pygame.time.get_ticks()
        self.shot_cooldown = 300

    def load_animations(self):
        file_names = {
            'idle': 'player_idle.png',
            'right': 'player_right.png',
            'left': 'player_left.png',
            'up': 'player_up.png',
            'down': 'player_down.png'
        }
        animations = {}
        for state, file_name in file_names.items():
            path = os.path.join('assets', 'images', file_name)
            try:
                original_image = pygame.image.load(path).convert_alpha()
                scaled_image = pygame.transform.scale(original_image, (self.ancho_sprite, self.alto_sprite))
                animations[state] = scaled_image
            except pygame.error:
                fallback = pygame.Surface((self.ancho_sprite, self.alto_sprite), pygame.SRCALPHA)
                fallback.fill((255, 255, 255, 255))
                animations[state] = fallback
        if 'idle' not in animations:
            fallback = pygame.Surface((self.ancho_sprite, self.alto_sprite), pygame.SRCALPHA)
            fallback.fill((255, 255, 255, 255))
            animations['idle'] = fallback
        return animations

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.speed_x > 0:
            self.current_animation = self.animations.get('right', self.animations['idle'])
            self.facing = 'right'
        elif self.speed_x < 0:
            self.current_animation = self.animations.get('left', self.animations['idle'])
            self.facing = 'left'
        elif self.speed_y > 0:
            self.current_animation = self.animations.get('down', self.animations['idle'])
            self.facing = 'down'
        elif self.speed_y < 0:
            self.current_animation = self.animations.get('up', self.animations['idle'])
            self.facing = 'up'
        else:
            self.current_animation = self.animations['idle']
        center = self.rect.center
        self.image = self.current_animation
        self.rect = self.image.get_rect(center=center)
        if self.rect.right > ANCHO:
            self.rect.right = ANCHO
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > ALTO:
            self.rect.bottom = ALTO
        if self.rect.top < 0:
            self.rect.top = 0

    def can_shoot(self):
        now = pygame.time.get_ticks()
        return now - self.last_shot_time > self.shot_cooldown

    def shoot(self, target_x, target_y):
        if self.can_shoot():
            self.last_shot_time = pygame.time.get_ticks()
            return SnakeBullet(self.rect.centerx, self.rect.centery, target_x, target_y)
        return None
