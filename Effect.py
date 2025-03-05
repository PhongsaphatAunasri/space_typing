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

explosion_frames = [
    pygame.image.load("assets/explode-effect-1.png"),
    pygame.image.load("assets/explode-effect-2.png"),
    pygame.image.load("assets/explode-effect-3.png"),
    pygame.image.load("assets/explode-effect-4.png"),
    pygame.image.load("assets/explode-effect-5.png"),
    pygame.image.load("assets/explode-effect-6.png"),
    
]

class Explosion:
    def __init__(self, x, y):
        self.frames = explosion_frames  # Ensure explosion frames are loaded
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=(x, y))
        self.animation_speed = 5  # Control animation speed
        self.counter = 0
        self.finished = False
        

    def update(self):
        """Update explosion animation"""
        self.counter += 1
        if self.counter % self.animation_speed == 0:
            self.index += 1
            if self.index < len(self.frames):
                self.image = self.frames[self.index]
            else:
                self.finished = True  # Animation finished

    def draw(self, screen):
        """Draw the explosion if not finished"""
        if not self.finished:
            screen.blit(self.image, self.rect)

