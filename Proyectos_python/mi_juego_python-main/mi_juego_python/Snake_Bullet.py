import pygame
import math
from config import *
import os

class SnakeBullet(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, target_x, target_y):
        super().__init__()
        self.size = 45
        self.speed = 10
        bullet_image_path = os.path.join('assets', 'images', 'snake_bullet.png')
        try:
            original_image = pygame.image.load(bullet_image_path).convert_alpha()
            self.image = pygame.transform.scale(original_image, (self.size, self.size))
        except pygame.error:
            self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            self.image.fill((0, 255, 0, 200))
        self.rect = self.image.get_rect(center=(start_x, start_y))
        dx = target_x - start_x
        dy = target_y - start_y
        distance = math.sqrt(dx**2 + dy**2)
        if distance == 0:
            distance = 1
        self.vel_x = (dx / distance) * self.speed
        self.vel_y = (dy / distance) * self.speed
        self.creation_time = pygame.time.get_ticks()
        self.lifetime = 2000

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if (self.rect.left > ANCHO or 
            self.rect.right < 0 or
            self.rect.top > ALTO or
            self.rect.bottom < 0):
            self.kill()
        if pygame.time.get_ticks() - self.creation_time > self.lifetime:
            self.kill()
