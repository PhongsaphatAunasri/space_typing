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
#set volume
loss_hp_sound.set_volume(0.05)
game_over_sound.set_volume(0.05)
correct_sound.set_volume(0.05)
select_sound.set_volume(0.05)  # Adjust volume 

player_health = 1

def draw_health(health, x, y):
    for i in range(health):
        screen.blit(heart_image, (x + i * (heart_image.get_width() + 10), y))   
def draw_text(text, font, color, x, y, blink=False):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
        # Blinking effect for the specified text
    if blink and text == "Space Typing" and pygame.time.get_ticks() % 1000 < 500:
        screen.blit(text_surface, text_rect)
    elif not blink:
        screen.blit(text_surface, text_rect)

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
            draw_text(f"{player_score}", pygame.font.Font("assets/Prototype.ttf", 60), config.YELLOW, config.WIDTH // 2, config.HEIGHT // 1.75)
        
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
    max_multiplier = 10  
    clock = pygame.time.Clock()
    falling_words = []
    spaceship = Spaceship()
    player_word = ""
    base_speed = 0.5  
    multiplier_display_timer = 0
    running = True
    explosions = []

    while running and player_health > 0:
        speed_increase = (player_score // 100000) * 1  
        falling_word_speed = base_speed + speed_increase

        screen.fill(config.BLACK)  
        for particle in Particle.particles:
            particle.draw()
            particle.update()

        if len(falling_words) < 4 and random.randint(0, 100) < 2:
            falling_words.append(FallingWord(falling_words, falling_word_speed))

        draw_text(player_word, font, config.WHITE, config.WIDTH // 2, config.HEIGHT - 150)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    result = pause_game()
                    if result == "Main Menu":
                        running = False
                elif event.key == pygame.K_BACKSPACE:
                    player_word = player_word[:-1]  
                elif event.key != pygame.K_SPACE:  
                    player_word += event.unicode
                    
                    correct_word = None
                    for word in falling_words:
                        if player_word == word.word:
                            correct_word = word
                            break
                    if correct_word:
                        correct_sound.play()
                        word_length = len(correct_word.word)
                        player_score += word_length * 1000 * score_multiplier
                        score_multiplier = min(score_multiplier + 1, max_multiplier)
                        spaceship.shoot_missile(correct_word, missile_image)
                        player_word = ""

        # Update missiles and check for collisions
        missiles_to_remove = []
        words_to_remove = []
        
        for missile in spaceship.missiles:
            missile.update()
            for word in falling_words:
                if missile.rect.colliderect(word.rect):
                    explosions.append(Explosion(word.rect.centerx, word.rect.centery))
                    words_to_remove.append(word)
                    missiles_to_remove.append(missile)

        # Remove missiles and words that collided
        for missile in missiles_to_remove:
            spaceship.missiles.remove(missile)
        for word in words_to_remove:
            falling_words.remove(word)

        spaceship.draw_missiles()

        # Update and draw falling words
        for word in falling_words:
            if word.update(player_health):  
                falling_words.remove(word)
            else:
                word.draw(player_word)

        # Update and draw explosions
        for explosion in explosions[:]:
            explosion.update()
            explosion.draw(screen)
            if explosion.finished:
                explosions.remove(explosion)

        # Check deadzone 
        for word in falling_words:
            if word.rect.y > config.DEADZONE_LINE:
                player_health -= 1
                loss_hp_sound.play()
                score_multiplier = 1  
                falling_words.remove(word)

        # Display score and health
        draw_text(f"Score", font, config.WHITE, 60, 20)
        draw_text(f"{player_score}", font, config.WHITE, 60, 55)
        draw_health(player_health, 3, 70)

        if multiplier_display_timer > 0:
            draw_text(f"Multiplier: {score_multiplier}x", font, config.WHITE, config.WIDTH - 150, 20)
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