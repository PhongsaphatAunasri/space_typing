import pygame
import sys
import random
import csv
# import math
import config
import Particle

import survivor


from survivor import survivor_mode
from timetrial import blitz
from timetrial import time_attack
from lesson import run_lessons
from stage1 import adventure_s1
from stage2 import adventure_s2
from stage3 import adventure_s3
from stage4 import adventure_s4
from stage5 import adventure_s5
from stage6 import adventure_s6
from stage7 import adventure_s7
from stage8 import adventure_s8
from stage9 import adventure_s9
from stage10 import adventure_s10

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
info = pygame.display.Info()
# Create the game window
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
pygame.display.set_caption("Space Typing")


icon = pygame.image.load("assets/ship.png")  # Replace with the actual path to your icon
pygame.display.set_icon(icon)

# Load assets
background_image = pygame.image.load("assets/bg.png")  # Replace with your actual background image
spaceship_image = pygame.image.load("assets/ship.png")
meteor_image = pygame.image.load("assets/meteor-3.png")
heart_image = pygame.image.load("assets/heart.png")
missile_image = pygame.image.load("assets/missile.png")
# ufo_image = pygame.image.load("assets/ufo.png")

select_sound = pygame.mixer.Sound("sounds/select.wav")
correct_sound = pygame.mixer.Sound("sounds/correct.wav")
incorrect_sound = pygame.mixer.Sound("sounds/incorrect.wav")
boom_sound = pygame.mixer.Sound("sounds/boom.wav")
max_streak_sound = pygame.mixer.Sound("sounds/MaxStreak.wav")
loss_streak_sound = pygame.mixer.Sound("sounds/LossStreak.wav")
game_over_sound = pygame.mixer.Sound("sounds/gameover.wav")
loss_hp_sound = pygame.mixer.Sound("sounds/losshp.wav")
hp_up_sound = pygame.mixer.Sound("sounds/hpup.wav")
press_sound = pygame.mixer.Sound("sounds/press.wav")


loss_hp_sound.set_volume(0.2)
game_over_sound.set_volume(0.2)
correct_sound.set_volume(0.05)
select_sound.set_volume(0.2)  
boom_sound.set_volume(0.05)
incorrect_sound.set_volume(0.1)
press_sound.set_volume(0.2) 

# Fonts
font = config.FONT_MAIN





# Function to draw text on the screen
def draw_text(text, font, color, x, y, blink=False):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))

    # Blinking effect for the specified text
    if blink and text == "Space Typing" and pygame.time.get_ticks() % 1000 < 500:
        screen.blit(text_surface, text_rect)
    elif not blink:
        screen.blit(text_surface, text_rect)


# Constants
DEADZONE_LINE = config.HEIGHT - 20  # Adjust the value as needed
# player_health = 3
# score = 0
DELAYED_APPEND_EVENT = pygame.USEREVENT + 1
DELAY_DURATION = 1000  # Delay duration in milliseconds (e.g., 1000 ms = 1 second)



def select_mode():
    # Track the current selection
    button_height = 60  # config.Height of each button
    spacing = 120  # Vertical spacing between buttons
    current_selection = 0
    mode_options = ["Adventure", "Survivor", "Time Trial", "Back"]

    while True:
        screen.blit(background_image, (0, 0))
        for particle in Particle.particles:
            particle.update()

        # Draw everything
        screen.fill(config.BLACK)  # Fill the screen with the background color
        for particle in Particle.particles:
            particle.draw()

        draw_text("Select Mode", config.FONT_LARGE, config.WHITE, config.WIDTH // 2, config.HEIGHT // 2 - 100, blink=False)

        # Draw mode options with config.grey border around the current selection
        for i, option in enumerate(mode_options):
            button_rect = pygame.Rect(config.WIDTH // 2 - 125, config.HEIGHT - 450 + i * spacing, 250, button_height)
            if i == current_selection:
                pygame.draw.rect(screen, config.WHITE, button_rect)
                pygame.draw.rect(screen, config.YELLOW, button_rect, 5)
                draw_text(option, font, config.BLACK, button_rect.centerx, button_rect.centery)
            else:
                pygame.draw.rect(screen, config.WHITE, button_rect, 5)
                draw_text(option, font, config.WHITE, button_rect.centerx, button_rect.centery)

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    select_sound.play()
                    if current_selection == 0:  # Adventure mode
                        # story_mode()  # Call the story_mode function
                        return "Adventure"
                    elif current_selection == 1:  # Survivor mode
                        return "Survivor"
                    elif current_selection == 2:  # Time Trial mode
                        return "Time Trial"
                    elif current_selection == 3:  # Back to Main Menu
                        return "Main Menu"
                elif event.key == pygame.K_UP:
                    press_sound.play()
                    current_selection = (current_selection - 1) % len(mode_options)
                elif event.key == pygame.K_DOWN:
                    press_sound.play()
                    current_selection = (current_selection + 1) % len(mode_options)
def select_time_mode():
    # Track the current selection
    button_height = 60  # config.Height of each button
    spacing = 120  # Vertical spacing between buttons
    current_selection = 0
    mode_options = ["60 Second", "Blitz", "Back"]

    while True:
        screen.blit(background_image, (0, 0))
        for particle in Particle.particles:
            particle.update()

        # Draw everything
        screen.fill(config.BLACK)  # Fill the screen with the background color
        for particle in Particle.particles:
            particle.draw()

        draw_text("Select Time Mode", config.FONT_LARGE, config.WHITE, config.WIDTH // 2, config.HEIGHT // 2 - 100, blink=False)

        # Draw mode options with config.grey border around the current selection
        for i, option in enumerate(mode_options):
            button_rect = pygame.Rect(config.WIDTH // 2 - 125, config.HEIGHT - 400 + i * spacing, 250, button_height)
            if i == current_selection:
                pygame.draw.rect(screen, config.WHITE, button_rect)
                pygame.draw.rect(screen, config.YELLOW, button_rect, 5)
                draw_text(option, font, config.BLACK, button_rect.centerx, button_rect.centery)
            else:
                pygame.draw.rect(screen, config.WHITE, button_rect, 5)
                draw_text(option, font, config.WHITE, button_rect.centerx, button_rect.centery)
        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    select_sound.play()
                    if current_selection == 0:  # Adventure mode
                        # story_mode()  # Call the story_mode function
                        return "60 Second"
                    elif current_selection == 1:  # Survivor mode
                        return "Blitz"
                    elif current_selection == 2:  # Time Trial mode
                        return "Select Mode"
                elif event.key == pygame.K_UP:
                    press_sound.play()
                    current_selection = (current_selection - 1) % len(mode_options)
                elif event.key == pygame.K_DOWN:
                    press_sound.play()
                    current_selection = (current_selection + 1) % len(mode_options)

def select_stage():
    button_width, button_height = 180, 60  # Button size
    spacing_x, spacing_y = 20, 50  # Spacing between buttons
    start_x = config.WIDTH // 2 - ((5 * button_width + 4 * spacing_x) // 2)  # Centering horizontally
    start_y = 200  # Y start position

    current_selection = 0
    mode_options = ["Stage 1", "Stage 2", "Stage 3", "Stage 4", "Stage 5",
                    "Stage 6", "Stage 7", "Stage 8", "Stage 9", "Stage 10", "Back"]
    
    cols = 5  # Number of columns in the grid
    rows = 2  # Number of rows
    total_stages = cols * rows  # Total number of stage buttons
    last_index = len(mode_options) - 1  # "Back" button index

    while True:
        screen.blit(background_image, (0, 0))
        for particle in Particle.particles:
            particle.update()

        # Draw everything
        screen.fill(config.BLACK)  # Fill the screen with the background color
        for particle in Particle.particles:
            particle.draw()
        
        draw_text("Select Stage", config.FONT_LARGE, config.WHITE, config.WIDTH // 2, 100, blink=False)

        # Draw grid buttons (2 rows, 5 columns)
        for i in range(total_stages):
            col = i % cols
            row = i // cols
            x = start_x + col * (button_width + spacing_x)
            y = start_y + row * (button_height + spacing_y)
            button_rect = pygame.Rect(x, y, button_width, button_height)

            if i == current_selection:
                pygame.draw.rect(screen, config.WHITE, button_rect)
                pygame.draw.rect(screen, config.YELLOW, button_rect, 5)
                draw_text(mode_options[i], config.FONT_MAIN, config.BLACK, button_rect.centerx, button_rect.centery)
            else:
                pygame.draw.rect(screen, config.WHITE, button_rect, 5)
                draw_text(mode_options[i], config.FONT_MAIN, config.WHITE, button_rect.centerx, button_rect.centery)

        # Draw the "Back" button separately at the bottom
        back_button_rect = pygame.Rect(config.WIDTH // 2 - button_width // 2, config.HEIGHT - 100, button_width, button_height)
        if current_selection == last_index:
            pygame.draw.rect(screen, config.WHITE, back_button_rect)
            pygame.draw.rect(screen, config.YELLOW, back_button_rect, 5)
            draw_text("Back", config.FONT_MAIN, config.BLACK, back_button_rect.centerx, back_button_rect.centery)
        else:
            pygame.draw.rect(screen, config.WHITE, back_button_rect, 5)
            draw_text("Back", config.FONT_MAIN, config.WHITE, back_button_rect.centerx, back_button_rect.centery)

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    select_sound.play()
                    if current_selection == last_index:  
                        return "Select Mode"  # ✅ Correctly exit when selecting "Back"
                    return mode_options[current_selection]  # Return the selected stage  # Return the selected stage

                elif event.key == pygame.K_LEFT:
                    press_sound.play()
                    if current_selection > 0 and current_selection != last_index:
                        current_selection -= 1

                elif event.key == pygame.K_RIGHT:
                    press_sound.play()
                    if current_selection < total_stages - 1:
                        current_selection += 1

                elif event.key == pygame.K_UP:
                    press_sound.play()
                    if current_selection >= cols:  # Move up in the grid
                        current_selection -= cols
                    elif current_selection == last_index:  # Back to the grid
                        current_selection = total_stages - 1

                elif event.key == pygame.K_DOWN:
                    press_sound.play()
                    if current_selection < total_stages - cols:  # Move down in grid
                        current_selection += cols
                    else:
                        current_selection = last_index  # Move to "Back" button
                # elif current_selection == 0:  # Adventure mode
                #         # story_mode()  # Call the story_mode function
                #         return "Stage 1"
                # elif current_selection == 1:  
                #     return "Stage 2"
                # elif current_selection == 2:  
                #     return "Stage 3"
                # elif current_selection == 3:  
                #     return "Stage 4"
                # elif current_selection == 4:  
                #     return "Stage 5"
                # elif current_selection == 5:  
                #     return "Stage 6"
                # elif current_selection == 6:  
                #     return "Stage 7"
                # elif current_selection == 7:  
                #     return "Stage 8"
                # elif current_selection == 8:  
                #     return "Stage 9"
                # elif current_selection == 9:  
                #     return "Stage 10"
                # elif current_selection == 10:  
                #     return "Select Mode"
        pygame.display.flip()

        # Event handling
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
        #         sys.exit()
        #     elif event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_RETURN:
        #             select_sound.play()
        #             if current_selection == 0:  # Adventure mode
        #                 # story_mode()  # Call the story_mode function
        #                 return "Stage 1"
        #             elif current_selection == 1:  
        #                 return "Stage 2"
        #             elif current_selection == 2:  
        #                 return "Stage 3"
        #             elif current_selection == 3:  
        #                 return "Stage 4"
        #             elif current_selection == 4:  
        #                 return "Stage 5"
        #             elif current_selection == 5:  
        #                 return "Stage 6"
        #             elif current_selection == 6:  
        #                 return "Stage 7"
        #             elif current_selection == 7:  
        #                 return "Stage 8"
        #             elif current_selection == 8:  
        #                 return "Stage 9"
        #             elif current_selection == 9:  
        #                 return "Stage 10"
        #             elif current_selection == 10:  
        #                 return "Select Mode"
        #         elif event.key == pygame.K_UP:
        #             press_sound.play()
        #             current_selection = (current_selection - 1) % len(mode_options)
        #         elif event.key == pygame.K_DOWN:
        #             press_sound.play()
        #             current_selection = (current_selection + 1) % len(mode_options)


# Main Menu Loop
def main_menu():
    # Track the current selection
    button_height = 60  # config.Height of each button
    spacing = 100  # Vertical spacing between buttons
    current_selection = 0
    menu_options = ["Start","Lesson", "Exit"]

    while True:
        screen.blit(background_image, (0, 0))
        for particle in Particle.particles:
            particle.update()

        # Draw everything
        screen.fill(config.BLACK)  # Fill the screen with the background color
        for particle in Particle.particles:
            particle.draw()

        draw_text("Space Typing", config.FONT_LARGE, config.WHITE, config.WIDTH // 2, config.HEIGHT // 2 - 100, blink=True)
        
        # Draw menu options with config.grey border around the current selection
        for i, option in enumerate(menu_options):
            button_rect = pygame.Rect(config.WIDTH // 2 - 125, config.HEIGHT - 400 + i * spacing, 250, button_height)
            if i == current_selection:
                pygame.draw.rect(screen, config.WHITE, button_rect)
                pygame.draw.rect(screen, config.YELLOW, button_rect, 5)
                draw_text(option, font, config.BLACK, button_rect.centerx, button_rect.centery)
            else:
                pygame.draw.rect(screen, config.WHITE, button_rect, 5)
                draw_text(option, font, config.WHITE, button_rect.centerx, button_rect.centery)

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    select_sound.play()
                    if current_selection == 0:  # Select Mode option
                        return "Select Mode"
                    elif current_selection == 1:  # Lesson option
                        return "Lesson"
                    elif current_selection == 2:  # Exit option
                        pygame.quit()
                        sys.exit()
                elif event.key == pygame.K_UP:
                    press_sound.play()
                    current_selection = (current_selection - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    press_sound.play()
                    current_selection = (current_selection + 1) % len(menu_options)



menu_option = main_menu()

while menu_option != "Exit":
    if menu_option == "Survivor":
        menu_option = survivor_mode(survivor.player_health)
    elif menu_option == "Adventure":
        menu_option = select_stage()
    elif menu_option == "Stage 1":
        menu_option = adventure_s1()
    elif menu_option == "Stage 2":
        menu_option = adventure_s2()
    elif menu_option == "Stage 3":
        menu_option = adventure_s3()
    elif menu_option == "Stage 4":
        menu_option = adventure_s4()
    elif menu_option == "Stage 5":
        menu_option = adventure_s5()
    elif menu_option == "Stage 6":
        menu_option = adventure_s6()
    elif menu_option == "Stage 7":
        menu_option = adventure_s7()
    elif menu_option == "Stage 8":
        menu_option = adventure_s8()
    elif menu_option == "Stage 9":
        menu_option = adventure_s9()
    elif menu_option == "Stage 10":
        menu_option = adventure_s10()
    elif menu_option == "Time Trial":
        menu_option = select_time_mode()
    elif menu_option == "60 Second":
        menu_option = time_attack(0)
    elif menu_option == "Blitz":
        menu_option = blitz(0)
    elif menu_option == "Lesson":
        menu_option = run_lessons() # Pass the screen object to the lesson function
    elif menu_option == "Select Mode":
        menu_option = select_mode()
    elif menu_option == "Main Menu":
        menu_option = main_menu()

        
