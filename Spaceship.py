import pygame
import random
import sys
import csv
import math
import config 
import time
from Missile import Missile
# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
class Spaceship:
    def __init__(self):
        self.frames = [
            pygame.image.load("assets/ship1-1.png").convert_alpha(),
            pygame.image.load("assets/ship1-2.png").convert_alpha(),
            pygame.image.load("assets/ship1-3.png").convert_alpha(),
            pygame.image.load("assets/ship1-4.png").convert_alpha()
        ]
        self.current_frame = 0
        self.animation_speed = 0.1  # Adjust animation speed as needed
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.centerx = config.WIDTH // 2
        self.rect.bottom = config.HEIGHT - 10
        self.missiles = []
        self.animation_timer = 0
        pass
    def animate(self):
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
        pass
    def draw(self):
        screen.blit(self.image, self.rect)
        pass
    def update(self):
        self.animate()
        pass
    def shoot_missile(self, target_word, missile_image):
        missile = Missile(self.rect.centerx, self.rect.top, target_word, missile_image)
        self.missiles.append(missile)
        pass
    def update_missiles(self, falling_words):
        for missile in self.missiles[:]:
            missile.update()
            if missile.rect.bottom < 0:
                self.missiles.remove(missile)
            for word in falling_words:
                if missile.rect.colliderect(word.rect):
                    self.missiles.remove(missile)
                    falling_words.remove(word)
                    break
        pass
    def draw_missiles(self):
        for missile in self.missiles:
            missile.draw()
        pass