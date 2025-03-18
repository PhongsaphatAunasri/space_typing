import pygame
import random
import sys
import csv
import math
import config 
import time
import Missile
import Particle
# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))

background_image = pygame.image.load("assets/bg.png") 
font = config.FONT_MAIN
def draw_text(text, font, color, x, y, blink=False):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
        # Blinking effect for the specified text
    if blink and text == "Space Typing" and pygame.time.get_ticks() % 1000 < 500:
        screen.blit(text_surface, text_rect)
    elif not blink:
        screen.blit(text_surface, text_rect)
def pause_game():
    pygame.mixer.pause()
    pause_font = config.FONT
    pause_start_ticks = pygame.time.get_ticks()  # Record the time when the game is paused
    button_height = 60  # config.Height of each button
    spacing = 120  # Vertical spacing between buttons
    pause_options = ["Resume", "Exit"]
    current_selection = 0

    while True:


        # Draw everything
        screen.blit(background_image, (0, 0))
        for particle in Particle.particles:
            particle.update()

        # Draw everything
        screen.fill(config.BLACK)  # Fill the screen with the background color
        for particle in Particle.particles:
            particle.draw()
            
        # Draw pause text
        draw_text("Game Paused", pause_font, config.WHITE, config.WIDTH // 2, config.HEIGHT // 3)

        # Draw pause menu options
        for i, option in enumerate(pause_options):
            button_rect = pygame.Rect(config.WIDTH // 2 - 100, config.HEIGHT - 500 + i * spacing, 200, button_height)
            if i == current_selection:
                pygame.draw.rect(screen, config.WHITE, button_rect)
                pygame.draw.rect(screen, config.YELLOW, button_rect, 5)
                draw_text(option, font, config.BLACK, button_rect.centerx, button_rect.centery)
            else:
                pygame.draw.rect(screen, config.WHITE, button_rect, 5)
                draw_text(option, font, config.WHITE, button_rect.centerx, button_rect.centery)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    config.SELECT.play()
                    if current_selection == 0:
                        pygame.mixer.unpause()
                        # Calculate the total paused time
                        paused_time = pygame.time.get_ticks() - pause_start_ticks
                        return paused_time  # Return the total paused duration
                    elif current_selection == 1:
                        return "Main Menu"  # Return to main menu
                elif event.key == pygame.K_ESCAPE:
                    return "Main Menu"  # Return to main menu
                elif event.key == pygame.K_UP:
                    config.PRESS.play()
                    current_selection = (current_selection - 1) % len(pause_options)
                elif event.key == pygame.K_DOWN:
                    config.PRESS.play()
                    current_selection = (current_selection + 1) % len(pause_options)