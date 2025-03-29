import pygame
import random
import sys
import csv
import math
import config 
import time
import Particle
from pause import pause_game
# Initialize Pygame
pygame.init()

# Constants
info = pygame.display.Info()

screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))

#Load keyboard images
keyboard_image = pygame.image.load("assets/keys/keyboard_layout.png")
key_space = pygame.image.load("assets/keys/key-space.png") 
key_a = pygame.image.load("assets/keys/key-a.png") 
key_b = pygame.image.load("assets/keys/key-b.png") 
key_c = pygame.image.load("assets/keys/key-c.png") 
key_d = pygame.image.load("assets/keys/key-d.png") 
key_e = pygame.image.load("assets/keys/key-e.png") 
key_f = pygame.image.load("assets/keys/key-f.png") 
key_g = pygame.image.load("assets/keys/key-g.png") 
key_h = pygame.image.load("assets/keys/key-h.png") 
key_i = pygame.image.load("assets/keys/key-i.png") 
key_j = pygame.image.load("assets/keys/key-j.png") 
key_k = pygame.image.load("assets/keys/key-k.png") 
key_l = pygame.image.load("assets/keys/key-l.png") 
key_m = pygame.image.load("assets/keys/key-m.png") 
key_n = pygame.image.load("assets/keys/key-n.png") 
key_o = pygame.image.load("assets/keys/key-o.png") 
key_p = pygame.image.load("assets/keys/key-p.png") 
key_q = pygame.image.load("assets/keys/key-q.png") 
key_r = pygame.image.load("assets/keys/key-r.png") 
key_s = pygame.image.load("assets/keys/key-s.png") 
key_t = pygame.image.load("assets/keys/key-t.png") 
key_u = pygame.image.load("assets/keys/key-u.png") 
key_v = pygame.image.load("assets/keys/key-v.png")
key_w = pygame.image.load("assets/keys/key-w.png")  
key_x = pygame.image.load("assets/keys/key-x.png")
key_y = pygame.image.load("assets/keys/key-y.png")  
key_z = pygame.image.load("assets/keys/key-z.png") 
key_A = pygame.image.load("assets/keys/key-CapA.png") 
key_B = pygame.image.load("assets/keys/key-CapB.png") 
key_C = pygame.image.load("assets/keys/key-CapC.png") 
key_D = pygame.image.load("assets/keys/key-CapD.png")
key_E = pygame.image.load("assets/keys/key-CapE.png")
key_F = pygame.image.load("assets/keys/key-CapF.png")
key_G = pygame.image.load("assets/keys/key-CapG.png")
key_H = pygame.image.load("assets/keys/key-CapH.png")
key_I = pygame.image.load("assets/keys/key-CapI.png")
key_J = pygame.image.load("assets/keys/key-CapJ.png")
key_K = pygame.image.load("assets/keys/key-CapK.png")
key_L = pygame.image.load("assets/keys/key-CapL.png")
key_M = pygame.image.load("assets/keys/key-CapM.png")
key_N = pygame.image.load("assets/keys/key-CapN.png")
key_O = pygame.image.load("assets/keys/key-CapO.png")
key_P = pygame.image.load("assets/keys/key-CapP.png")
key_Q = pygame.image.load("assets/keys/key-CapQ.png")
key_R = pygame.image.load("assets/keys/key-CapR.png")
key_S = pygame.image.load("assets/keys/key-CapS.png")
key_T = pygame.image.load("assets/keys/key-CapT.png")
key_U = pygame.image.load("assets/keys/key-CapU.png")
key_V = pygame.image.load("assets/keys/key-CapV.png")
key_W = pygame.image.load("assets/keys/key-CapW.png")
key_X = pygame.image.load("assets/keys/key-CapX.png")
key_Y = pygame.image.load("assets/keys/key-CapY.png")
key_Z = pygame.image.load("assets/keys/key-CapZ.png")
key_1 = pygame.image.load("assets/keys/key-1.png")
key_2 = pygame.image.load("assets/keys/key-2.png")
key_3 = pygame.image.load("assets/keys/key-3.png")
key_4 = pygame.image.load("assets/keys/key-4.png")
key_5 = pygame.image.load("assets/keys/key-5.png")
key_6 = pygame.image.load("assets/keys/key-6.png")
key_7 = pygame.image.load("assets/keys/key-7.png")
key_8 = pygame.image.load("assets/keys/key-8.png")
key_9 = pygame.image.load("assets/keys/key-9.png")
key_0 = pygame.image.load("assets/keys/key-0.png")
key_exclamation = pygame.image.load("assets/keys/key-exclamation.png")
key_at = pygame.image.load("assets/keys/key-at.png")
key_hash = pygame.image.load("assets/keys/key-hash.png")
key_dollarsign = pygame.image.load("assets/keys/key-dollarsign.png")
key_percent = pygame.image.load("assets/keys/key-percent.png")
key_circumflex = pygame.image.load("assets/keys/key-circumflex.png")
key_and = pygame.image.load("assets/keys/key-and.png")
key_star = pygame.image.load("assets/keys/key-star.png")
key_open_parentheses = pygame.image.load("assets/keys/key-open-parentheses.png")
key_close_parentheses = pygame.image.load("assets/keys/key-close-parentheses.png")
key_hyphen = pygame.image.load("assets/keys/key-hyphen.png")
key_underscore = pygame.image.load("assets/keys/key-underscore.png")
key_equal = pygame.image.load("assets/keys/key-equal.png")
key_addition = pygame.image.load("assets/keys/key-addition.png")
key_open_square = pygame.image.load("assets/keys/key-open-square.png")
key_open_curly = pygame.image.load("assets/keys/key-open-curly.png")
key_close_square = pygame.image.load("assets/keys/key-close-square.png")
key_close_curly = pygame.image.load("assets/keys/key-close-curly.png")
key_semicolon = pygame.image.load("assets/keys/key-semicolon.png")
key_colon = pygame.image.load("assets/keys/key-colon.png")
key_apostrophe = pygame.image.load("assets/keys/key-apostrophe.png")
key_quotation = pygame.image.load("assets/keys/key-quotation.png")
key_backslash = pygame.image.load("assets/keys/key-backslash.png")
key_bar = pygame.image.load("assets/keys/key-bar.png")
key_comma = pygame.image.load("assets/keys/key-comma.png")
key_fullstop = pygame.image.load("assets/keys/key-fullstop.png")
key_slash = pygame.image.load("assets/keys/key-slash.png")
key_lessthan = pygame.image.load("assets/keys/key-lessthan.png")
key_greaterthan = pygame.image.load("assets/keys/key-greaterthan.png")
key_question = pygame.image.load("assets/keys/key-question.png")

press_space = pygame.image.load("assets/keys/key-space-p.png")
blank = pygame.image.load("assets/keys/blank-layout.png")
space_key_position = (config.WIDTH/5 , config.HEIGHT - 350) 

def load_lesson_from_csv(filename):
    with open(filename, "r") as file:
        reader = csv.reader(file)
        return [row[0] for row in reader if row]  # Assume each word/character is in the first column

# Helper function to display text
def draw_text(text, font, color, x, y, center=True):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(x, y) if center else (x, y))
    screen.blit(surface, rect)

# Constants
BLINK_INTERVAL = 500  # Milliseconds (adjust to change blink speed)

# Variables
blink_enabled = False  # Toggle blinking effect
last_blink_time = 1
show_highlight = False  # Toggle state

def toggle_blink():
    global blink_enabled
    blink_enabled = not blink_enabled  # Enable/Disable blinking

# Draw keyboard layout and highlight current key
def draw_keyboard_layout(current_char):
    global last_blink_time, show_highlight
    screen.blit(keyboard_image, (config.WIDTH / 5, config.HEIGHT - 350))  # Display at the bottom of the screen
    
    if blink_enabled:
        current_time = pygame.time.get_ticks()
        if current_time - last_blink_time > BLINK_INTERVAL:
            show_highlight = not show_highlight  # Toggle visibility
            last_blink_time = current_time  # Reset timer
    else:
        show_highlight = True  # Ensure highlight is always shown if blinking is disabled

    # Highlight the key only if blinking state is "on"
    if show_highlight:
        if current_char == " ":
            space_key_position = (config.WIDTH / 5, config.HEIGHT - 350)
            screen.blit(key_space, space_key_position)
        elif current_char == "a":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350) 
            screen.blit(key_a, space_key_position)
        elif current_char == "b":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_b, space_key_position)
        elif current_char == "c":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_c, space_key_position)
        elif current_char == "d":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_d, space_key_position)
        elif current_char == "e":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_e, space_key_position)
        elif current_char == "f":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_f, space_key_position)
        elif current_char == "g":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_g, space_key_position)
        elif current_char == "h":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_h, space_key_position)
        elif current_char == "i":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_i, space_key_position)
        elif current_char == "j":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_j, space_key_position)
        elif current_char == "k":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_k, space_key_position)
        elif current_char == "l":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_l, space_key_position)
        elif current_char == "m":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_m, space_key_position)
        elif current_char == "n":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_n, space_key_position)
        elif current_char == "o":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_o, space_key_position)
        elif current_char == "p":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_p, space_key_position)
        elif current_char == "q":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_q, space_key_position)
        elif current_char == "r":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_r, space_key_position)
        elif current_char == "s":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_s, space_key_position)
        elif current_char == "t":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_t, space_key_position)
        elif current_char == "u":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_u, space_key_position)
        elif current_char == "v":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_v, space_key_position)
        elif current_char == "w":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_w, space_key_position)
        elif current_char == "x":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_x, space_key_position)
        elif current_char == "y":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_y, space_key_position)
        elif current_char == "z":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_z, space_key_position)
        elif current_char == "A":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350) 
            screen.blit(key_A, space_key_position)
        elif current_char == "B":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_B, space_key_position)
        elif current_char == "C":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_C, space_key_position)
        elif current_char == "D":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_D, space_key_position)
        elif current_char == "E":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_E, space_key_position)
        elif current_char == "F":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_F, space_key_position)
        elif current_char == "G":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_G, space_key_position)
        elif current_char == "H":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_H, space_key_position)
        elif current_char == "I":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_I, space_key_position)
        elif current_char == "J":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_J, space_key_position)
        elif current_char == "K":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_K, space_key_position)
        elif current_char == "L":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_L, space_key_position)
        elif current_char == "M":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_M, space_key_position)
        elif current_char == "N":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_N, space_key_position)
        elif current_char == "O":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_O, space_key_position)
        elif current_char == "P":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_P, space_key_position)
        elif current_char == "Q":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_Q, space_key_position)
        elif current_char == "R":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_R, space_key_position)
        elif current_char == "S":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_S, space_key_position)
        elif current_char == "T":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_T, space_key_position)
        elif current_char == "U":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_U, space_key_position)
        elif current_char == "V":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_V, space_key_position)
        elif current_char == "W":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_W, space_key_position)
        elif current_char == "X":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_X, space_key_position)
        elif current_char == "Y":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_Y, space_key_position)
        elif current_char == "Z":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_Z, space_key_position)
        elif current_char == "1":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_1, space_key_position)
        elif current_char == "2":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_2, space_key_position)
        elif current_char == "3":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_3, space_key_position)
        elif current_char == "4":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_4, space_key_position)
        elif current_char == "5":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_5, space_key_position)
        elif current_char == "6":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_6, space_key_position)
        elif current_char == "7":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_7, space_key_position)
        elif current_char == "8":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_8, space_key_position)
        elif current_char == "9":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_9, space_key_position)
        elif current_char == "0":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_0, space_key_position)
        elif current_char == "!":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_exclamation, space_key_position)
        elif current_char == "@":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_at, space_key_position)
        elif current_char == "#":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_hash, space_key_position)
        elif current_char == "$":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_dollarsign, space_key_position)
        elif current_char == "%":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_percent, space_key_position)
        elif current_char == "^":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_circumflex, space_key_position)
        elif current_char == "&":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_and, space_key_position)
        elif current_char == "*":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_star, space_key_position)
        elif current_char == "(":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_open_parentheses, space_key_position)
        elif current_char == ")":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_close_parentheses, space_key_position)
        elif current_char == "-":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_hyphen, space_key_position)
        elif current_char == "=":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_equal, space_key_position)
        elif current_char == "_":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_underscore, space_key_position)
        elif current_char == "+":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_addition, space_key_position)
        elif current_char == "[":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_open_square, space_key_position)
        elif current_char == "{":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_open_curly, space_key_position)
        elif current_char == "]":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_close_square, space_key_position)
        elif current_char == "}":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_close_curly, space_key_position)
        elif current_char == ";":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_semicolon, space_key_position)
        elif current_char == ":":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_colon, space_key_position)
        elif current_char == "'":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_apostrophe, space_key_position)
        elif current_char == '"':
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_quotation, space_key_position)
        elif current_char == chr(92):
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_backslash, space_key_position)
        elif current_char == "|":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_bar, space_key_position)
        elif current_char == ",":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_comma, space_key_position)
        elif current_char == ".":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_fullstop, space_key_position)
        elif current_char == "/":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_slash, space_key_position)
        elif current_char == "<":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_lessthan, space_key_position)
        elif current_char == ">":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_greaterthan, space_key_position)
        elif current_char == "?":
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350)  
            screen.blit(key_question, space_key_position)  
        elif current_char.isalpha():
            # Logic for other keys (optional: add highlighting for other characters)
            pass

# Updated lesson function to include accuracy tracking
def is_valid_keypress(event):
    """Check if the key pressed is valid, ignoring Shift."""
    # Ignore modifier keys like Shift
    if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
        return False
    return True


def show_error_summary(screen, error_count, correct_count, lesson_title):
    clock = pygame.time.Clock()
    running = True

    # Calculate accuracy
    total_keystrokes = correct_count + error_count
    accuracy = (correct_count / total_keystrokes) * 100 if total_keystrokes > 0 else 0

    # Timing for when to show error and accuracy
    error_display_time = 0.7  # seconds
    accuracy_display_time = 0.7 + error_display_time
    start_time = time.time()  # Record the start time

    while running:
        screen.fill(config.BLACK)
        for particle in Particle.particles:
            particle.update()
            particle.draw()

        # Display static messages
        draw_text("Congratulations", config.FONT_LARGE, config.WHITE, config.WIDTH // 2, config.HEIGHT // 5.5)
        draw_text("You've completed", config.FONT_LARGE, config.WHITE, config.WIDTH // 2, config.HEIGHT // 3.5)
        draw_text(f"{lesson_title}", config.FONT, config.GREEN, config.WIDTH // 2, config.HEIGHT // 2.5)
        draw_text(f"Total Errors : ", config.FONT, config.WHITE, (config.WIDTH // 2) - 130, config.HEIGHT // 2)
        draw_text(f"Accuracy : ", config.FONT, config.WHITE, (config.WIDTH // 2) - 100, config.HEIGHT // 1.7)
        # Display "Total Errors" after 2 seconds
        if time.time() - start_time >= error_display_time:
            draw_text(f"{error_count}", config.FONT, config.RED, (config.WIDTH // 2) + 100, config.HEIGHT // 2)

        # Display "Accuracy" after 3 seconds
        if time.time() - start_time >= accuracy_display_time:
            draw_text(f"{accuracy:.2f}%", config.FONT, config.YELLOW, (config.WIDTH // 2) + 110, config.HEIGHT // 1.7)

        # Display prompt to continue
        draw_text("Press Enter to continue", config.FONT, config.WHITE, config.WIDTH // 2 , config.HEIGHT // 1.4)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Continue on Enter key
                    running = False

        pygame.display.flip()
        clock.tick(config.FPS)
    
    return "Next Lesson"


def lesson(screen, lesson_content, title, use_letter_spacing=True):
    clock = pygame.time.Clock()
    typed_index = 0
    current_item_index = 0
    current_item = lesson_content[current_item_index]
    feedback = "---"
    error_count = 0
    correct_count = 0
    mistake_indices = set()  # Track indices where errors have occurred
    running = True

    # Cursor blinking variables
    cursor_visible = True
    cursor_blink_interval = 250  # Cursor toggles every 250ms
    last_blink_time = pygame.time.get_ticks()

    letter_spacing = 10 if use_letter_spacing else 1  # Conditional spacing

    # Load the "Next" and "Previous" button images
    next_button = pygame.image.load("assets/next-button.png").convert_alpha()
    next_button_rect = next_button.get_rect()
    next_button_rect.bottomright = (config.WIDTH - 10, config.HEIGHT - 10)

    prev_button = pygame.image.load("assets/prev-button.png").convert_alpha()
    prev_button_rect = prev_button.get_rect()
    prev_button_rect.bottomleft = (10, config.HEIGHT - 10)
    
    # progress_bar_config.width = 924
    # progress_bar_height = 5
    # progress_bar_x = config.WIDTH / 5
    # progress_bar_y = config.HEIGHT - 365
    circle_radius = 46
    circle_center = (config.WIDTH //4, config.HEIGHT *0.53)
    circle_thickness = 20 # Thickness of the arc
    space_pressed = False
    while running:
        screen.fill(config.BLACK)

        # Particle effects (if any)
        for particle in Particle.particles:
            particle.update()
            particle.draw()

        # Handle events
        for event in pygame.event.get():
            space_key_position = (config.WIDTH/5 , config.HEIGHT - 350) 
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    config.SELECT.play()
                    if pause_game() == "Main Menu":
                        config.LESSON_SONG.stop()
                        running = False
                elif event.key == pygame.K_RIGHT:  # Go to the next lesson
                    config.PRESS.play()
                    return "Next Lesson"
                elif event.key == pygame.K_LEFT:  # Go to the previous lesson
                    config.PRESS.play()
                    return "Previous Lesson"
                elif is_valid_keypress(event):  # Check if the key is valid
                    if event.key == pygame.K_BACKSPACE:
                        feedback = "No skipping!"
                        config.INCORRECT.play()
                        error_count += 1
                    
                    elif event.unicode == current_item[typed_index]:
                        typed_index += 1
                        feedback = "Good job!"
                        config.PRESS.play()
                        correct_count += 1
                        # Clear mistakes for the current index when correctly typed
                        # mistake_indices.discard(typed_index - 1)
                        # Move to the next word if the current one is completed
                        if typed_index == len(current_item):
                            current_item_index += 1
                            if current_item_index >= len(lesson_content):
                                result = show_error_summary(screen, error_count, correct_count, title)
                                if result == "Next Lesson":
                                    return "Next Lesson"  # Now the lesson will transition to the next one
                                else:
                                    return result
                            current_item = lesson_content[current_item_index]
                            typed_index = 0
                            mistake_indices.clear()  # Reset mistakes for the new word
                        
                    elif typed_index not in mistake_indices:
                        feedback = "Try again!"
                        config.INCORRECT.play()
                        error_count += 1
                        mistake_indices.add(typed_index)  # Ensure mistakes are recorded
                elif event.key == pygame.K_SPACE:
                    space_pressed = True  # Draw image when spacebar is pressed
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    space_pressed = False  # Clear image when spacebar is released
        if space_pressed:
            screen.blit(press_space, space_key_position)
        # Draw lesson title
        draw_text(title, config.FONT,config. WHITE, config.WIDTH // 2, config.HEIGHT // 10)

        # Draw the current word/character in the center
        text_height = config.FONT.get_height()  # Get full font height
        word_surface = pygame.Surface((config.WIDTH, text_height), pygame.SRCALPHA)

        x_offset = config.WIDTH // 2 - (config.FONT.size(current_item)[0] + (len(current_item) - 1) * letter_spacing) // 2
        for i, letter in enumerate(current_item):
            if i in mistake_indices:  
                color = config.RED  # Keep red if there was a mistake at this index
            elif i < typed_index:
                color = config.CYAN  # If typed correctly on first attempt, keep cyan
            elif i == typed_index:
                color = config.WHITE  # Current letter being typed is white
            else:
                color = config.WHITE  # Future letters remain white

            letter_surface = config.FONT.render(letter, True, color)
            word_surface.blit(letter_surface, (x_offset, (text_height - config.FONT.size(letter)[1]) // 2))
            x_offset += config.FONT.size(letter)[0] + letter_spacing



        
        screen.blit(word_surface, (0, config.HEIGHT // 3))

        # Draw feedback
        draw_text(feedback, config.FONT, config.WHITE, config.WIDTH // 2,config.HEIGHT // 1.5)

        # Draw error count and accuracy
        total_keystrokes = correct_count + error_count
        accuracy = (correct_count / total_keystrokes) * 100 if total_keystrokes > 0 else 0
        draw_text(f"Errors : {error_count}", config.FONT, config.WHITE,config.WIDTH * 0.7, config.HEIGHT - 400)
        draw_text(f"Accuracy : {accuracy:.2f}%",config.FONT, config.WHITE, config.WIDTH // 2.18, config.HEIGHT - 400)
        draw_text(f"Prev", config.FONT, config.WHITE,130, config.HEIGHT - 40)
        draw_text(f"Next", config.FONT, config.WHITE,config.WIDTH - 130, config.HEIGHT - 40)
        
        # progress = (current_item_index + typed_index / len(current_item)) / len(lesson_content)
        # pygame.draw.rect(screen, WHITE, (progress_bar_x, progress_bar_y, progress_bar_config.width, progress_bar_height))
        # pygame.draw.rect(screen, GREEN, (progress_bar_x, progress_bar_y, progress_bar_config.width * progress, progress_bar_height))

        # Calculate and draw the circular progress
        progress = (current_item_index + typed_index / len(current_item)) / len(lesson_content)
        start_angle = 90  # Start at the top of the circle
        end_angle = start_angle - (progress * 360) # Progress angle (clockwise)
        
        pygame.draw.circle(screen, config.GREY, circle_center, circle_radius, circle_thickness)
        # Progress arc (filled portion) – Draw the arc clockwise
        pygame.draw.arc(screen, config.WHITE, 
                        (circle_center[0] - circle_radius, circle_center[1] - circle_radius,
                        circle_radius * 2, circle_radius * 2), 
                        math.radians(end_angle), 
                        math.radians(start_angle), 
                        circle_thickness)

        # Draw the "Next" and "Previous" buttons
        screen.blit(next_button, next_button_rect)
        screen.blit(prev_button, prev_button_rect)
        # Blink the cursor
        current_time = pygame.time.get_ticks()
        if current_time - last_blink_time > cursor_blink_interval:
            cursor_visible = not cursor_visible
            last_blink_time = current_time

        if cursor_visible:
            # Calculate cursor x-position based on typed letters
            cursor_x = config.WIDTH // 2 - (config.FONT.size(current_item)[0] + (len(current_item) - 1) * letter_spacing) // 2 + sum(
                config.FONT.size(current_item[i])[0] + letter_spacing for i in range(typed_index)
            )
            # Position the cursor just below the current line of text
            cursor_y = config.HEIGHT // 3 + config.FONT.get_height() + 5  # Add padding for spacing
            pygame.draw.line(screen, config.YELLOW, (cursor_x, cursor_y), (cursor_x + config.FONT.size(current_item[typed_index])[0], cursor_y), 3)

        # Draw keyboard layout and highlight the current key
        draw_keyboard_layout(current_item[typed_index])

        # Draw the "Next" and "Previous" buttons
        screen.blit(next_button, next_button_rect)
        screen.blit(prev_button, prev_button_rect)

        pygame.display.flip()
        clock.tick(config.FPS)

    return "Main Menu"

# Run all lessons
def run_lessons():  
    lessons = [
        ('Lesson 1 : Home Row ', "assets/csv/lesson1.csv"),
        ("Lesson 2 : G and H", "assets/csv/lesson2.csv"),
        ("Lesson 3 : Left Hand Exercise", "assets/csv/lesson3.csv"),
        ("Lesson 4 : Right Hand Exercise", "assets/csv/lesson4.csv"),
        ('Lesson 5 : Common Pattern 1 "the", "ing", "tion"', "assets/csv/lesson5.csv"),
        ('Lesson 6 : Common Pattern 2 "est", "and", "int"', "assets/csv/lesson6.csv"),
        ('Lesson 7 : Common Pattern 3 "nth", "ear", "ore"', "assets/csv/lesson7.csv"),
        ('Lesson 8 : Common Pattern 4 "eal", "ate", "ted"', "assets/csv/lesson8.csv"),
        ('Lesson 9 : Common Pattern 5 "one", "ame", "tor"', "assets/csv/lesson9.csv"),
        ('Lesson 10 : Common Pattern 6 "ine", "ave", "ound"', "assets/csv/lesson10.csv"),
        ('Lesson 11 : Common Pattern 7 "own", "ill", "son"', "assets/csv/lesson11.csv"),
        ('Lesson 12 : Common Pattern 8 "ink", "rea", "eed"', "assets/csv/lesson12.csv"),
        ('Lesson 13 : Common Pattern 9 "ast", "you", "utt"', "assets/csv/lesson13.csv"),
        ('Lesson 14 : Common Pattern 10 "ship", "age", "ity"', "assets/csv/lesson14.csv"),
        ("Lesson 15 : Capitalization and Punctuation.", "assets/csv/lesson15.csv"),
        ("Lesson 16 : Question Mark , Hyphen, Slash", "assets/csv/lesson16.csv"),
        ("Lesson 17 : Numeral", "assets/csv/lesson17.csv"),
        ("Lesson 18 : Symbols", "assets/csv/lesson18.csv"),
        ("Lesson 19 : test", "assets/csv/test.csv"),
    ]
    current_index = 0  # Start with the first lesson

    while 0 <= current_index < len(lessons):
        title, filename = lessons[current_index]
        use_letter_spacing = current_index not in (14, 15)  # Example spacing logic
        lesson_content = load_lesson_from_csv(filename)

        # Run the lesson
        lesson_result = lesson(screen, lesson_content, title, use_letter_spacing=use_letter_spacing)

        # Handle the returned value
        if lesson_result == "Main Menu":
            config.LESSON_SONG.stop()
            return "Main Menu"
        elif lesson_result == "Next Lesson":
            if current_index < len(lessons) - 1:
                current_index += 1  # Move to the next lesson
        elif lesson_result == "Previous Lesson" and current_index > 0:
            current_index -= 1  # Move to the previous lesson

# Start the lessons
# run_lessons()# 
