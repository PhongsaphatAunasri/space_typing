import pygame
import sys
pygame.init()
pygame.mixer.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
FPS = 60
DEADZONE_LINE = HEIGHT - 20  # Adjust the value as needed
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (228, 62, 62)
GREY = (100, 100, 100)
YELLOW = (255, 214, 3)
GREEN = (54, 205, 86)
CYAN = (98, 217, 250)
DARKRED = (156, 30, 30)
DARKGREY = (23, 23, 23)
LIGHTYELLOW = (255, 233, 110)

FONT = pygame.font.Font("assets/Prototype.ttf", 50)
FONT_MAIN = pygame.font.Font("assets/Prototype.ttf", 40)
FONT_SMALL = pygame.font.Font("assets/Prototype.ttf", 30)
FONT_SEMI_LARGE = pygame.font.Font("assets/Prototype.ttf", 60)
FONT_Large = pygame.font.Font("assets/Prototype.ttf", 80)
