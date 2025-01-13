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
class WhiteParticle:
    def __init__(self):
        self.rect = pygame.Rect(
            random.randint(0, config.WIDTH),
            random.randint(0, config.HEIGHT),
            random.randint(2, 4),
            random.randint(2, 4)
        )
        self.speed = random.uniform(0.5, 2.0)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > config.HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randint(0, config.WIDTH)

    def draw(self):
        pygame.draw.rect(screen, config.WHITE, self.rect)

particles = [WhiteParticle() for _ in range(50)]