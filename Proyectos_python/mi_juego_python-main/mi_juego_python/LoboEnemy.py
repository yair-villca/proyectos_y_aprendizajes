import pygame
import os
import math
import random
from config import *

class LoboEnemy(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, player_ref):
        super().__init__()
        self.player = player_ref
        self.ancho_sprite = 80
        self.alto_sprite = 80
        self.base_velocidad = 3
        self.attack_range = 100
        self.animations = self.load_animations()
        self.current_animation = self.animations['attack']
        self.base_image_to_rotate = self.animations['attack']
        self.image = self.current_animation
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y

    def load_animations(self):
        file_names = {
            'idle': 'globo_idle.png',
            'right': 'globo_right.png',
            'left': 'globo_left.png',
            'up': 'globo_up.png',
            'down': 'globo_down.png',
            'attack': 'globo_ataque.png'
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
                fallback.fill((255, 100, 0, 255))
                animations[state] = fallback
        if 'idle' not in animations:
            fallback = pygame.Surface((self.ancho_sprite, self.alto_sprite), pygame.SRCALPHA)
            fallback.fill((255, 100, 0, 255))
            animations['idle'] = fallback
        return animations

    def update(self):
        current_speed = self.base_velocidad
        image_is_rotated = False
        if self.player:
            target_x = self.player.rect.centerx
            target_y = self.player.rect.centery
            dx = target_x - self.rect.centerx
            dy = target_y - self.rect.centery
            distance = math.sqrt(dx**2 + dy**2)
            if distance <= self.attack_range:
                current_speed = self.base_velocidad * 1.5
                self.base_image_to_rotate = self.animations.get('attack', self.animations['idle'])
                image_is_rotated = True
                angle_rad = math.atan2(dy, dx)
                angle_deg = math.degrees(angle_rad)
            else:
                current_speed = self.base_velocidad
                if abs(dx) > abs(dy):
                    if dx > 0:
                        self.current_animation = self.animations.get('right', self.animations['idle'])
                    else:
                        self.current_animation = self.animations.get('left', self.animations['idle'])
                else:
                    if dy > 0:
                        self.current_animation = self.animations.get('down', self.animations['idle'])
                    else:
                        self.current_animation = self.animations.get('up', self.animations['idle'])
                self.image = self.current_animation
            angle = math.atan2(dy, dx)
            self.rect.x += current_speed * math.cos(angle)
            self.rect.y += current_speed * math.sin(angle)
            if image_is_rotated:
                center = self.rect.center
                self.image = pygame.transform.rotate(self.base_image_to_rotate, -angle_deg)
                self.rect = self.image.get_rect(center=center)

