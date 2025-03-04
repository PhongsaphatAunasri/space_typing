import pygame
import sys
pygame.init()
pygame.mixer.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
FPS = 60
DEADZONE_LINE = HEIGHT - 20  # Adjust the value as needed
############################## COLOR ##################################
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (228, 62, 62)
GREY = (40, 40, 40)
DARKGREY = (23, 23, 23)
YELLOW = (255, 214, 3)
DARKYELLOW =(196, 165, 2)
GREEN = (54, 205, 86)
CYAN = (98, 217, 250)
DARKRED = (156, 30, 30)
LIGHTYELLOW = (252, 230, 81)
ORANGE = (255, 127, 15)
LIGHTGREY = (180, 180, 180)
LIME = (182, 245, 66)
NAVY = (1, 32, 87)
MINT = (130, 196, 179)
TEAL = (204, 255, 247)
AZURE = (61, 187, 255)
DARKGREEN = (22, 38, 16)

############################## FONT ##################################
FONT = pygame.font.Font("assets/Prototype.ttf", 50)
FONT_DIS = pygame.font.Font("assets/Prototype.ttf", 45)
FONT_MAIN = pygame.font.Font("assets/Prototype.ttf", 40)
FONT_SMALL = pygame.font.Font("assets/Prototype.ttf", 30)
FONT_SEMI_LARGE = pygame.font.Font("assets/Prototype.ttf", 60)
FONT_Large = pygame.font.Font("assets/Prototype.ttf", 80)
FONT_TITLE = pygame.font.Font("assets/Prototype.ttf", 100)
