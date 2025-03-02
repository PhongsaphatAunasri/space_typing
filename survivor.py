import pygame
import sys
import random
import csv
import math
import config
import time
from lesson import run_lessons
from lesson import lesson
import Particle
from FallingWord import FallingWord
from Spaceship import Spaceship
from Effect import Explosion
from pause import pause_game
# Initialize Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
font = config.FONT_MAIN
#image
heart_image = pygame.image.load("assets/heart.png")
missile_image = pygame.image.load("assets/missile.png")

#sound
loss_hp_sound = pygame.mixer.Sound("sounds/losshp.wav")
game_over_sound = pygame.mixer.Sound("sounds/gameover.wav")
correct_sound = pygame.mixer.Sound("sounds/correct.wav")
select_sound = pygame.mixer.Sound("sounds/select.wav")
boom_sound = pygame.mixer.Sound("sounds/boom.wav")
laser_sound = pygame.mixer.Sound("sounds/laser.wav")
press_sound = pygame.mixer.Sound("sounds/press.wav")
#set volume
loss_hp_sound.set_volume(0.05)
game_over_sound.set_volume(0.05)
correct_sound.set_volume(0.05)
select_sound.set_volume(0.05)  
boom_sound.set_volume(0.05)
laser_sound.set_volume(0.05)
press_sound.set_volume(0.05) 

player_health = 3

def draw_health(health, x, y):
    for i in range(health):
        screen.blit(heart_image, (x + (player_health - 1 - i) * (heart_image.get_width() + 10), y))

def draw_text(text, font, color, x, y, blink=False):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
        # Blinking effect for the specified text
    if blink and text == "Space Typing" and pygame.time.get_ticks() % 1000 < 500:
        screen.blit(text_surface, text_rect)
    elif not blink:
        screen.blit(text_surface, text_rect)
def draw_text_left_aligned(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(topleft=(x, y))  # Align to the left
    screen.blit(text_surface, text_rect)
 # Grey bar with height 50px
 # Grey bar with height 50px
def draw_text_right_aligned(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(topright=(x, y))  # Align to the right
    screen.blit(text_surface, text_rect)

# Example Usage


def game_over_menu_s(player_score):
    clock = pygame.time.Clock()
    running = True
    game_over_sound.play()
    options = ["Restart", "Main Menu"]
    current_selection = 0
    button_height = 60  # config.Height of each button
    spacing = 100  # Vertical spacing between buttons
    
    score_display = 1
    start_time = time.time()
    
    while running:
        # Draw everything
        
        screen.fill(config.BLACK)  # Fill the screen with the background color
        for particle in Particle.particles:
            particle.draw()
            particle.update()

        draw_text("Game Over", pygame.font.Font("assets/Prototype.ttf", 100), config.WHITE, config.WIDTH // 2, config.HEIGHT // 3)
        draw_text("Total Score", pygame.font.Font("assets/Prototype.ttf", 60), config.YELLOW, config.WIDTH // 2, config.HEIGHT // 2.15)
        if time.time() - start_time >= score_display:
            draw_text(f"{player_score:,}", pygame.font.Font("assets/Prototype.ttf", 60), config.YELLOW, config.WIDTH // 2, config.HEIGHT // 1.75)
        
        for i, option in enumerate(options):
            button_rect = pygame.Rect(config.WIDTH // 2 - 125, config.HEIGHT - 300 + i * spacing, 250, button_height)
            if i == current_selection:
                pygame.draw.rect(screen, config.WHITE, button_rect)
                pygame.draw.rect(screen, config.YELLOW, button_rect, 5)
                draw_text(option, font, config.BLACK, button_rect.centerx, button_rect.centery)
            else:
                pygame.draw.rect(screen, config.WHITE, button_rect, 5)
                draw_text(option, font, config.WHITE, button_rect.centerx, button_rect.centery)

        pygame.display.flip()
        clock.tick(config.FPS) 
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    select_sound.play()
                    if current_selection == 0:  # Restart option
                        return survivor_mode(player_health)  # Restart the game with initial health
                    elif current_selection == 1:  # Main Menu option
                        return "Main Menu"
                elif event.key == pygame.K_UP:
                    select_sound.play()
                    current_selection = (current_selection - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    select_sound.play()
                    current_selection = (current_selection + 1) % len(options)


def survivor_mode(player_health):
    player_score = 0
    score_multiplier = 1  
    max_multiplier = 99999
    clock = pygame.time.Clock()
    falling_words = []
    fast_falling_words = []  # New word group for fast words
    spaceship = Spaceship()
    player_word = ""
    base_speed = 0.5  
    current_speed = base_speed
    correct_word_count = 0  # Track correct words
    last_fast_word_count = 0  # Track when last fast word was added
    multiplier_display_timer = 0
    running = True
    lasers = []
    explosions = []

    while running and player_health > 0:
        falling_word_speed = current_speed

        screen.fill(config.BLACK)  
        for particle in Particle.particles:
            particle.draw()
            particle.update()

        # Regular falling words (at variable speed)
        if len(falling_words) < 4 and random.randint(0, 100) < 2:
            falling_words.append(FallingWord(falling_words, falling_word_speed))

        # Spawn one fast-falling word every 25 correct words
        if correct_word_count >= last_fast_word_count + 10:
            fast_falling_words.append(FallingWord(fast_falling_words, 3))
            last_fast_word_count = correct_word_count  # Update last spawn count

        draw_text(player_word, font, config.WHITE, config.WIDTH // 2, config.HEIGHT - 150)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                press_sound.play()
                if event.key == pygame.K_ESCAPE:
                    result = pause_game()
                    if result == "Main Menu":
                        running = False
                elif event.key == pygame.K_BACKSPACE:
                    player_word = player_word[:-1]  
                elif event.key != pygame.K_SPACE:  
                    player_word += event.unicode
                    
                    correct_word = None
                    all_falling_words = falling_words + fast_falling_words
                    for word in all_falling_words:
                        if player_word == word.word:
                            correct_word = word
                            break
                    if correct_word:
                        laser_sound.play()
                        word_length = len(correct_word.word)
                        player_score += word_length * 100 * score_multiplier
                        score_multiplier = min(score_multiplier + 1, max_multiplier)
                        lasers.append((spaceship.rect.centerx, spaceship.rect.top, correct_word.rect.centerx, correct_word.rect.centery))
                        boom_sound.play()
                        explosions.append(Explosion(correct_word.rect.centerx, correct_word.rect.centery))
                        
                        # Remove word from correct group
                        if correct_word in falling_words:
                            falling_words.remove(correct_word)
                        elif correct_word in fast_falling_words:
                            fast_falling_words.remove(correct_word)

                        player_word = ""

                        # Update speed based on correct words
                        correct_word_count += 1
                        if correct_word_count % 10 == 0:
                            current_speed += 0.5  # Increase speed
                        if correct_word_count % 30 == 0:
                            current_speed = base_speed  # Reset to base speed

        # Draw lasers
        for laser in lasers:
            pygame.draw.line(screen, config.CYAN, (laser[0], laser[1]), (laser[2], laser[3]), 10)
            pygame.draw.line(screen, config.WHITE, (laser[0], laser[1]), (laser[2], laser[3]), 4)
            pygame.draw.circle(screen, config.CYAN,(laser[0], laser[1]), 10)
            pygame.draw.circle(screen, config.WHITE,(laser[0], laser[1]), 6)
        lasers.clear()

        # Update and draw regular falling words
        for word in falling_words[:]:
            if word.update(player_health):  
                falling_words.remove(word)
            else:
                word.draw(player_word)

        # Update and draw fast falling words
        for word in fast_falling_words[:]:
            if word.update(player_health):  
                fast_falling_words.remove(word)
            else:
                word.draw(player_word)

        # Check deadzone  
        for word in falling_words + fast_falling_words:
            if word.rect.y > config.DEADZONE_LINE:
                player_health -= 1
                loss_hp_sound.play()
                score_multiplier = 2  
                if word in falling_words:
                    falling_words.remove(word)
                elif word in fast_falling_words:
                    fast_falling_words.remove(word)

        # Display score and health
        pygame.draw.rect(screen, config.WHITE, (0, 0, config.WIDTH, 54)) 
        pygame.draw.rect(screen, config.DARKGREY, (0, 0, config.WIDTH, 50)) 
        draw_text_left_aligned(f"Score {player_score:,}", font, config.WHITE, 5, 0)
        draw_health(player_health, config.WIDTH - 150, 5)

        if multiplier_display_timer > 0:
            draw_text_left_aligned(f"{score_multiplier - 1}x Streak", font, config.LIGHTYELLOW, config.WIDTH // 4.8, 0)
            multiplier_display_timer -= 1

        spaceship.update()
        spaceship.draw()

        if score_multiplier > 1:
            multiplier_display_timer = 120  

        if player_health <= 0:
            game_over_sound.play()
        pygame.display.flip()
        clock.tick(config.FPS)

    return game_over_menu_s(player_score)






survivor_mode(player_health)# 