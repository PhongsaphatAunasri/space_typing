import pygame
import random
import sys
import csv
import math
import config 
import time

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
boom_sound = pygame.mixer.Sound("sounds/boom.wav")
boom_sound.set_volume(0.05)
def draw_text(text, font, color, x, y, blink=False):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
class Missile:
    def __init__(self, x, y, target_word, missile_image):
        self.image = missile_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.target_word = target_word
        self.speed = 30  # Initial speed
        pass

    def update(self):
        #self.rect.y += self.speed
        # Calculate direction vector towards the target word
        dx = self.target_word.rect.centerx - self.rect.centerx
        dy = self.target_word.rect.centery - self.rect.centery
        # distance = math.sqrt(dx**2 + dy**2)
        angle = math.atan2(dy, dx)
        self.rect.x += self.speed * math.cos(angle)
        self.rect.y += self.speed * math.sin(angle)


        # Check collision with the target word
        if self.rect.colliderect(self.target_word.rect):
            boom_sound.play()
            # Handle collision with the target word
            self.target_word.hit_by_missile()
            return True  # Signal that the missile should be removed
        return False  # Signal that the missile should not be removed
    
    def draw(self):
        screen.blit(self.image, self.rect)
        pass