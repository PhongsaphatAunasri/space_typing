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
BROWN  = (46, 24, 0)
CREAM = (255, 236, 201)
DARKPURPLE = (40, 0, 71)
PURPLE = (151, 72, 212)
PINK = (255, 133, 251)
LAVENDER = (236, 182, 252)
############################## FONT ##################################
FONT = pygame.font.Font("assets/Prototype.ttf", 50)
FONT_DIS = pygame.font.Font("assets/Prototype.ttf", 45)
FONT_MAIN = pygame.font.Font("assets/Prototype.ttf", 40)
FONT_SMALL = pygame.font.Font("assets/Prototype.ttf", 30)
FONT_SEMI_LARGE = pygame.font.Font("assets/Prototype.ttf", 60)
FONT_LARGE = pygame.font.Font("assets/Prototype.ttf", 80)
FONT_TITLE = pygame.font.Font("assets/Prototype.ttf", 100)

NUM = pygame.font.Font("assets/Robotica.ttf", 50)
NUM_DIS = pygame.font.Font("assets/Robotica.ttf",45)
NUM_MAIN = pygame.font.Font("assets/Robotica.ttf",40)
NUM_SMALL = pygame.font.Font("assets/Robotica.ttf", 30)
NUM_SEMI_LARGE = pygame.font.Font("assets/Robotica.ttf", 60)
NUM_LARGE = pygame.font.Font("assets/Robotica.ttf", 80)
NUM_TITLE = pygame.font.Font("assets/Robotica.ttf", 100)

SCORE = pygame.font.Font("assets/Hermes-Regular.otf",55)
SCORE_SEMI_LARGE = pygame.font.Font("assets/Hermes-Regular.otf",70)

############################## BGM ##################################
TITLE_SONG = pygame.mixer.Sound("sounds/title.mp3")
TITLE_SONG.set_volume(0.1)
STAGE_SONG = pygame.mixer.Sound("sounds/stage.mp3")
STAGE_SONG.set_volume(0.1)
LESSON_SONG = pygame.mixer.Sound("sounds/lesson.mp3")
LESSON_SONG.set_volume(0.1)
SURVIVOR_SONG = pygame.mixer.Sound("sounds/survivor.mp3")
SURVIVOR_SONG.set_volume(0.1)
TIME_SONG = pygame.mixer.Sound("sounds/time.mp3")
TIME_SONG.set_volume(0.1)

BGM = [TITLE_SONG,STAGE_SONG,LESSON_SONG,TIME_SONG,SURVIVOR_SONG]

SELECT = pygame.mixer.Sound("sounds/select.wav")
CORRECT = pygame.mixer.Sound("sounds/correct.wav")
INCORRECT = pygame.mixer.Sound("sounds/incorrect.wav")
BOOM = pygame.mixer.Sound("sounds/boom.wav")
GAMEOVER = pygame.mixer.Sound("sounds/gameover.wav")
LOSS_HP = pygame.mixer.Sound("sounds/losshp.wav")
PRESS = pygame.mixer.Sound("sounds/press.wav")
LASER = pygame.mixer.Sound("sounds/laser.wav")

SELECT.set_volume(0.2)  
CORRECT.set_volume(0.05)
INCORRECT.set_volume(0.1)
BOOM.set_volume(0.05)
GAMEOVER.set_volume(0.2)
LOSS_HP.set_volume(0.2)
PRESS.set_volume(0.2) 
LASER.set_volume(0.2)

SFX = [SELECT,PRESS,LASER,BOOM,GAMEOVER,CORRECT,INCORRECT,LOSS_HP]