import pygame
import sys
import random
import csv
import math
import config
from lesson import run_lessons
from lesson import lesson
import Particle
from survivor import survivor_mode
from timetrial import time_trial_mode
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

select_sound.set_volume(0.05)  # Adjust volume 
correct_sound.set_volume(0.05)
incorrect_sound.set_volume(0.05)
boom_sound.set_volume(0.05)
max_streak_sound.set_volume(0.05)
loss_streak_sound.set_volume(0.05)
game_over_sound.set_volume(0.05)
loss_hp_sound.set_volume(0.05)
hp_up_sound.set_volume(0.05)

# Fonts
font = config.FONT_MAIN


word_database = []

# Function to load words from any level-specific file
def load_words_level(file_path):
    words = []
    with open(file_path, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            words.extend(row)
    return words
def load_words(file_path):
    words = []
    with open(file_path, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            words.extend(row)
    return words

# Load words specifically for Level 1
level_1_words = load_words_level("assets/level1.csv")
level_2_words = load_words_level("assets/level2.csv")
level_3_words = load_words_level("assets/level3.csv")
level_4_words = load_words_level("assets/level4.csv")
level_5_words = load_words_level("assets/level5.csv")
level_6_words = load_words_level("assets/level6.csv")
level_7_words = load_words_level("assets/level7.csv")
level_8_words = load_words_level("assets/level8.csv")
level_9_words = load_words_level("assets/level9.csv")
level_10_words = load_words_level("assets/level10.csv")
survivor_words = load_words_level("assets/word.csv")

# Update the main word database for Level 1
word_database.extend(survivor_words)
word_database.extend(level_1_words)
word_database.extend(level_2_words)
word_database.extend(level_3_words)
word_database.extend(level_4_words)
word_database.extend(level_5_words)
word_database.extend(level_6_words)
word_database.extend(level_7_words)
word_database.extend(level_8_words)
word_database.extend(level_9_words)
word_database.extend(level_10_words)



# Function to draw text on the screen
def draw_text(text, font, color, x, y, blink=False):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))

    # Blinking effect for the specified text
    if blink and text == "Space Typing" and pygame.time.get_ticks() % 1000 < 500:
        screen.blit(text_surface, text_rect)
    elif not blink:
        screen.blit(text_surface, text_rect)

def generate_random_word():
    return random.choice(survivor_words)
def generate_random_word_a(level):
    if level == 1:
        return random.choice(level_1_words)
    elif level == 2:
        return random.choice(level_2_words)
    elif level == 3:
        return random.choice(level_3_words)
    elif level == 4:
        return random.choice(level_4_words)
    elif level == 5:
        return random.choice(level_5_words)
    elif level == 6:
        return random.choice(level_6_words)
    elif level == 7:
        return random.choice(level_7_words)
    elif level == 8:
        return random.choice(level_8_words)
    elif level == 9:
        return random.choice(level_9_words)
    elif level == 10:
        return random.choice(level_10_words)
    else:
        return random.choice(word_database)

# Constants
DEADZONE_LINE = config.HEIGHT - 20  # Adjust the value as needed
player_health = 3
score = 0
DELAYED_APPEND_EVENT = pygame.USEREVENT + 1
DELAY_DURATION = 1000  # Delay duration in milliseconds (e.g., 1000 ms = 1 second)

class FallingWord:
    words_in_play = set()  # Static variable to keep track of current words in play

    def __init__(self, existing_words, speed):
        # Generate a random word and ensure it is not already in play
        self.word = generate_random_word()
        while self.word in FallingWord.words_in_play:
            self.word = generate_random_word()

        # Add the word to the set of words currently in play
        FallingWord.words_in_play.add(self.word)

        # Set up the position and speed
        self.rect = pygame.Rect(0, 0, 50, 10)  # Initial rect, position will be adjusted
        self.rect.midtop = (random.randint(50, config.WIDTH - 50), 0)  # Adjust the range

        # Ensure the new word doesn't overlap with existing words' positions
        while any(word.rect.colliderect(self.rect) for word in existing_words):
            self.rect.midtop = (random.randint(100, config.WIDTH - 50), 0)  # Update the position

        self.speed = speed
        self.rotation_angle = 0  # Initialize the rotation angle
        self.rotation_speed = random.uniform(0.5, 1)  # Random rotation speed
        self.correct_letters_stepped_back = 0

    def update(self, player_health):
        self.rect.y += self.speed

        # Update the rotation angle
        self.rotation_angle += self.rotation_speed
        self.rotation_angle %= 360  # Keep the angle within 0-359 degrees

        # Check if the falling word has passed the deadzone line
        if self.rect.y > config.HEIGHT:
            player_health -= 1
            # Remove the word from the set of words in play
            FallingWord.words_in_play.remove(self.word)
            return True  # Signal that the word should be removed

        return False  # Signal that the word should not be removed

    def draw(self, player_word):
        # Count how many letters of the word are typed correctly
        correct_letters = 0
        for i in range(min(len(player_word), len(self.word))):
            if player_word[i] == self.word[i]:
                correct_letters += 1
            else:
                break

        if correct_letters > self.correct_letters_stepped_back:
            step_back_count = correct_letters - self.correct_letters_stepped_back
            self.rect.y -= 5 * step_back_count  # Move the word back by 2 pixels for each newly correct letter
            self.correct_letters_stepped_back = correct_letters  # Update the count of correct letters that have been stepped back

        # Center the text on the meteor image
        text_surface = font.render(self.word, True, config.WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)

        # Rotate the meteor image
        rotated_meteor = pygame.transform.rotate(meteor_image, self.rotation_angle)
        rotated_rect = rotated_meteor.get_rect(center=self.rect.center)

        # Draw the rotated meteor
        screen.blit(rotated_meteor, rotated_rect.topleft)

        total_width = sum(font.size(char)[0] for char in self.word)

        # Initial x-coordinate for the first character
        x_offset = self.rect.centerx - total_width / 2
        # Move the word up a little bit
        y_offset = self.rect.centery - 5

        # Draw each character in the word with appropriate color
        for i, char in enumerate(self.word):
            if i < len(player_word) and char == player_word[i]:
                char_color = config.CYAN  # Color for correct letters
            else:
                char_color = config.WHITE  # Keep the other letters white
            char_surface = font.render(char, True, char_color)
            char_rect = char_surface.get_rect(center=(x_offset + font.size(char)[0] / 2, y_offset))
            screen.blit(char_surface, char_rect.topleft)

            # Update the x-coordinate for the next character
            x_offset += font.size(char)[0]

    def hit_by_missile(self):
        # Define what happens when the word is hit by a missile
        # Remove the word from the set of words in play
        if self.word in FallingWord.words_in_play:
            FallingWord.words_in_play.remove(self.word)
        pass  # Add any additional logic for handling the hit


class FallingWordTimeTrial:
    def __init__(self, position):
        self.word = generate_random_word()
        self.position = position  # Store the initial position
        self.rect = pygame.Rect(0, 0, 50, 10)
        self.rect.midtop = position
        self.speed = 20
        self.frozen = False
        self.frames = [
            pygame.image.load("assets/ufo-1.png").convert_alpha(),
            pygame.image.load("assets/ufo-2.png").convert_alpha(),
            pygame.image.load("assets/ufo-3.png").convert_alpha(),
            pygame.image.load("assets/ufo-4.png").convert_alpha()
        ]
        self.current_frame = 0
        self.animation_speed = 0.1  # Adjust animation speed as needed
        self.ufo_image = self.frames[self.current_frame]
        self.last_frame_update = pygame.time.get_ticks()
    def update(self):
        if not self.frozen:
            self.rect.y += self.speed
            if self.rect.y >= config.HEIGHT // 2:
                self.rect.y = config.HEIGHT // 2
                self.frozen = True
        now = pygame.time.get_ticks()
        if now - self.last_frame_update > (1000 * self.animation_speed):  # Update frame based on animation speed
            self.current_frame = (self.current_frame + 1) % len(self.frames)  # Cycle through frames
            self.ufo_image = self.frames[self.current_frame]
            self.last_frame_update = now  # Update the time of the last frame update

    def draw(self, player_word):
        font_size = 50
        font = config.FONT
        text_surface = font.render(self.word, True, config.WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        meteor_rect = self.ufo_image.get_rect(center=self.rect.midtop)
        screen.blit(self.ufo_image, meteor_rect.topleft)
        total_width = sum(font.size(char)[0] for char in self.word)
        x_offset = self.rect.centerx - total_width / 2
        y_offset = self.rect.centery + 15
        for i, char in enumerate(self.word):
            char_color = config.BLACK
            if i < len(player_word) and char == player_word[i]:
                char_color = config.YELLOW
            char_surface = font.render(char, True, char_color)
            char_rect = char_surface.get_rect(center=(x_offset + font.size(char)[0] / 2, y_offset))
            screen.blit(char_surface, char_rect.topleft)
            x_offset += font.size(char)[0]
    def hit_by_missile(self):
        pass

# Class to represent a falling word
class FallingWordA:
    words_in_play = set()  # Static variable to keep track of current words in play

    def __init__(self, existing_words, level):
        # Generate a random word for the given level
        self.word = generate_random_word_a(level)
        
        # Ensure the word is not already in play
        while self.word in FallingWordA.words_in_play:
            self.word = generate_random_word_a(level)
        
        # Add the new word to the set of words in play
        FallingWordA.words_in_play.add(self.word)
        
        # Set up the position and speed
        self.rect = pygame.Rect(0, 0, 50, 10)  # Initial rect, the position will be adjusted
        self.rect.midtop = (random.randint(50, config.WIDTH - 50), 0)  # Adjusted the range
        
        # Ensure the new word doesn't overlap with existing words
        while any(word.rect.colliderect(self.rect) for word in existing_words):
            self.rect.midtop = (random.randint(100, config.WIDTH - 50), 0)  # Update the position
        
        self.speed = random.uniform(0.5, 0.5)
        self.correct_letters_stepped_back = 0  # Track how many letters have been stepped back

    def update(self, player_health):
        self.rect.y += self.speed
        
        # Check if the falling word has passed the deadzone line
        if self.rect.y > config.HEIGHT:
            player_health -= 1
            # Remove the word from the set of words in play
            FallingWordA.words_in_play.remove(self.word)
            return True  # Signal that the word should be removed

        return False  # Signal that the word should not be removed
        
    def draw(self, player_word):
        # Count how many letters of the word are typed correctly
        correct_letters = 0
        for i in range(min(len(player_word), len(self.word))):
            if player_word[i] == self.word[i]:
                correct_letters += 1
            else:
                break

        # Only step back for new correct letters
        if correct_letters > self.correct_letters_stepped_back:
            step_back_count = correct_letters - self.correct_letters_stepped_back
            self.rect.y -= 5 * step_back_count  # Move the word back by 2 pixels for each newly correct letter
            self.correct_letters_stepped_back = correct_letters  # Update correct letters that have stepped back

        # Center the text on the meteor image
        text_surface = font.render(self.word, True, config.WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)

        # Draw meteor image with the correct dimensions
        meteor_rect = meteor_image.get_rect(center=self.rect.midtop)
        screen.blit(meteor_image, meteor_rect.topleft)

        total_width = sum(font.size(char)[0] for char in self.word)

        # Initial x-coordinate for the first character
        x_offset = self.rect.centerx - total_width / 2
        # Move the word up a little bit
        y_offset = self.rect.centery - 5
        
        # Draw each character in the word with appropriate color
        for i, char in enumerate(self.word):
            char_color = config.WHITE
            if i < len(player_word) and char == player_word[i]:
                char_color = config.CYAN  # Color for correct letters
            else:
                char_color = config.WHITE  # Keep the other letters white
            char_surface = font.render(char, True, char_color)
            char_rect = char_surface.get_rect(center=(x_offset + font.size(char)[0] / 2, y_offset))
            screen.blit(char_surface, char_rect.topleft)

            # Update the x-coordinate for the next character
            x_offset += font.size(char)[0]

    def hit_by_missile(self):
        # Handle what happens when the word is hit by a missile
        # Remove the word from the set when hit by missile
        if self.word in FallingWordA.words_in_play:
            FallingWordA.words_in_play.remove(self.word)
        pass  # Placeholder for further implementation if needed



        
# Class to represent the player's spaceship
class Spaceship:
    def __init__(self):
        self.frames = [
            pygame.image.load("assets/ship1-1.png").convert_alpha(),
            pygame.image.load("assets/ship1-2.png").convert_alpha(),
            pygame.image.load("assets/ship1-3.png").convert_alpha(),
            pygame.image.load("assets/ship1-4.png").convert_alpha()
        ]
        self.current_frame = 0
        self.animation_speed = 0.1  # Adjust animation speed as needed
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect()
        self.rect.centerx = config.WIDTH // 2
        self.rect.bottom = config.HEIGHT - 10
        self.missiles = []
        self.animation_timer = 0
    
    def animate(self):
        self.animation_timer += self.animation_speed
        if self.animation_timer >= 1:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
    
    def draw(self):
        screen.blit(self.image, self.rect)
    
    def update(self):
        self.animate()
    
    def shoot_missile(self, target_word, missile_image):
        missile = Missile(self.rect.centerx, self.rect.top, target_word, missile_image)
        self.missiles.append(missile)

    def update_missiles(self, falling_words):
        for missile in self.missiles[:]:
            missile.update()
            if missile.rect.bottom < 0:
                self.missiles.remove(missile)
            for word in falling_words:
                if missile.rect.colliderect(word.rect):
                    self.missiles.remove(missile)
                    falling_words.remove(word)
                    break

    def draw_missiles(self):
        for missile in self.missiles:
            missile.draw()


class Missile:
    def __init__(self, x, y, target_word, missile_image):
        self.image = missile_image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.target_word = target_word
        self.speed = 30  # Initial speed
        

    def update(self):
        #self.rect.y += self.speed
        # Calculate direction vector towards the target word
        dx = self.target_word.rect.centerx - self.rect.centerx
        dy = self.target_word.rect.centery - self.rect.centery
        # distance = math.sqrt(dx**2 + dy**2)
        angle = math.atan2(dy, dx)
        self.rect.x += self.speed * math.cos(angle)
        self.rect.y += self.speed * math.sin(angle)


        # Check collision with the target word
        if self.rect.colliderect(self.target_word.rect):
            boom_sound.play()
            # Handle collision with the target word
            self.target_word.hit_by_missile()
            return True  # Signal that the missile should be removed
        return False  # Signal that the missile should not be removed
    
    def draw(self):
        screen.blit(self.image, self.rect)

def draw_health(health, x, y):
    for i in range(health):
        screen.blit(heart_image, (x + i * (heart_image.get_width() + 10), y))   

def pause_game():
    pause_font = config.FONT
    pause_start_ticks = pygame.time.get_ticks()  # Record the time when the game is paused
    button_height = 60  # config.Height of each button
    spacing = 120  # Vertical spacing between buttons
    pause_options = ["Resume", "Surrender"]
    current_selection = 0

    while True:
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
                    if current_selection == 0:
                        # Calculate the total paused time
                        paused_time = pygame.time.get_ticks() - pause_start_ticks
                        return paused_time  # Return the total paused duration
                    elif current_selection == 1:
                        return "Main Menu"  # Return to main menu
                elif event.key == pygame.K_ESCAPE:
                    return "Main Menu"  # Return to main menu
                elif event.key == pygame.K_UP:
                    current_selection = (current_selection - 1) % len(pause_options)
                elif event.key == pygame.K_DOWN:
                    current_selection = (current_selection + 1) % len(pause_options)


def select_mode():
    # Track the current selection
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

        draw_text("Select Mode", config.FONT_Large, config.WHITE, config.WIDTH // 2, config.HEIGHT // 2 - 100, blink=False)

        # Draw mode options with config.grey border around the current selection
        for i, option in enumerate(mode_options):
            if i == current_selection:
                # Fill the selected option with white
                pygame.draw.rect(screen, config.WHITE, (config.WIDTH // 2 - 100, config.HEIGHT // 2 + i * 100, 200, 50))
                # Draw the border in config.grey
                pygame.draw.rect(screen, config.YELLOW, (config.WIDTH // 2 - 100, config.HEIGHT // 2 + i * 100, 200, 50), 5)
                # Draw the text in config.black
                draw_text(option, font, config.BLACK, config.WIDTH // 2, config.HEIGHT // 2 + i * 100 + 25)
            else:
                # Draw the unselected option's border in white
                pygame.draw.rect(screen, config.WHITE, (config.WIDTH // 2 - 100, config.HEIGHT // 2 + i * 100, 200, 50), 5)
                # Draw the text in white
                draw_text(option, font, config.WHITE, config.WIDTH // 2, config.HEIGHT // 2 + i * 100 + 25)

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
                    select_sound.play()
                    current_selection = (current_selection - 1) % len(mode_options)
                elif event.key == pygame.K_DOWN:
                    select_sound.play()
                    current_selection = (current_selection + 1) % len(mode_options)

def select_adventure_level():
    current_selection = 0
    levels = [f"Level {i+1}" for i in range(10)]  # List of 10 levels
    levels.append("Back")  # Add a "Back" option
    columns = 2 # Number of columns in the grid
    rows = 5     # Number of rows in the grid
    box_width = 200  # Width of each selection box
    box_height = 50  # config.Height of each selection box
    padding = 20     # Space between the boxes

    while True:
        screen.blit(background_image, (0, 0))
        for particle in Particle.particles:
            particle.update()

        # Draw everything
        screen.fill(config.BLACK)  # Fill the screen with the background color
        for particle in Particle.particles:
            particle.draw()

        draw_text("Select Adventure Level", config.FONT_Large, config.WHITE, config.WIDTH // 2, config.HEIGHT // 2 - 200, blink=False)

        # Draw level options in a 2x5 grid
        for i, level in enumerate(levels):
            if i < 10:  # Draw levels in the grid (2x5)
                row = i // columns
                col = i % columns
                x = config.WIDTH // 2 - (box_width + padding) + col * (box_width + padding)  # X position
                y = config.HEIGHT // 2 - 100 + row * (box_height + padding)  # Y position
            else:  # Draw "Back" button at the bottom
                x = config.WIDTH // 2 - box_width // 2
                y = config.HEIGHT // 2 + 250

            # Highlight the selected level
            if i == current_selection:
                pygame.draw.rect(screen, config.WHITE, (x, y, box_width, box_height))
                pygame.draw.rect(screen, config.YELLOW, (x, y, box_width, box_height), 5)
                draw_text(level, font, config.BLACK, x + box_width // 2, y + box_height // 2)
            else:
                pygame.draw.rect(screen, config.WHITE, (x, y, box_width, box_height), 5)
                draw_text(level, font, config.WHITE, x + box_width // 2, y + box_height // 2)

        pygame.display.flip()

        # Event handling for keyboard input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    select_sound.play()
                    if current_selection == len(levels) - 1:  # If "Back" is selected
                        return "Main Menu"
                    else:
                        return current_selection + 1  # Return the selected level number
                elif event.key == pygame.K_UP:
                    select_sound.play()
                    current_selection = (current_selection - columns) % len(levels)  # Move up in the grid
                elif event.key == pygame.K_DOWN:
                    select_sound.play()
                    current_selection = (current_selection + columns) % len(levels)  # Move down in the grid
                elif event.key == pygame.K_LEFT:
                    select_sound.play()
                    current_selection = (current_selection - 1) % len(levels)  # Move left in the grid
                elif event.key == pygame.K_RIGHT:
                    select_sound.play()
                    current_selection = (current_selection + 1) % len(levels)  # Move right in the grid

def game_over_menu_a(player_score):
    game_over_sound.play()
    options = ["Restart", "Main Menu"]
    current_selection = 0
    button_height = 60  # config.Height of each button
    spacing = 120  # Vertical spacing between buttons

    while True:
        screen.blit(background_image, (0, 0))
        for particle in Particle.particles:
            particle.update()

        # Draw everything
        screen.fill(config.BLACK)  # Fill the screen with the background color
        for particle in Particle.particles:
            particle.draw()

        draw_text("Game Over", pygame.font.Font("assets/mania.ttf", 60), config.WHITE, config.WIDTH // 2, config.HEIGHT // 3)
        draw_text(f"Total Score : {player_score}", pygame.font.Font("assets/mania.ttf", 42), config.YELLOW, config.WIDTH // 2, config.HEIGHT // 2.15)

        for i, option in enumerate(options):
            button_rect = pygame.Rect(config.WIDTH // 2 - 100, config.HEIGHT - 400 + i * spacing, 200, button_height)
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
                    if current_selection == 0:  # Restart option
                        return select_adventure_level()  # Restart the game with initial health
                    elif current_selection == 1:  # Main Menu option
                        return main_menu()
                elif event.key == pygame.K_UP:
                    select_sound.play()
                    current_selection = (current_selection - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    select_sound.play()
                    current_selection = (current_selection + 1) % len(options)                    
                 
def level_complete_screen(level, player_score):
    screen.fill(config.BLACK)
    draw_text(f"Level {level} Complete!", pygame.font.Font("assets/mania.ttf", 60), config.YELLOW, config.WIDTH // 2, config.HEIGHT // 2 - 50)
    draw_text(f"Score: {player_score}", pygame.font.Font("assets/mania.ttf", 50), config.WHITE, config.WIDTH // 2, config.HEIGHT // 2 + 20)
    pygame.display.flip()
    pygame.time.delay(1000)  # Wait for 3 seconds

def game_completed_screen(player_score):
    screen.fill(config.BLACK)
    draw_text("Congratulations!", pygame.font.Font("assets/mania.ttf", 60), config.YELLOW, config.WIDTH // 2, config.HEIGHT // 2 - 50)
    draw_text("You have completed Adventure Mode!", pygame.font.Font("assets/mania.ttf", 50), config.WHITE, config.WIDTH // 2, config.HEIGHT // 2 + 20)
    draw_text(f"Total Score: {player_score}", pygame.font.Font("assets/mania.ttf", 50), config.WHITE, config.WIDTH // 2, config.HEIGHT // 2 + 80)
    pygame.display.flip()
    pygame.time.delay(5000)  # Wait for 5 seconds
    return main_menu()

# Main Menu Loop
def main_menu():
    # Track the current selection
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

        draw_text("Space Typing", config.FONT_Large, config.WHITE, config.WIDTH // 2, config.HEIGHT // 2 - 100, blink=True)
        
        # Draw menu options with config.grey border around the current selection
        for i, option in enumerate(menu_options):
            if i == current_selection:
                # Fill the selected option with white
                pygame.draw.rect(screen, config.WHITE, (config.WIDTH // 2 - 100, config.HEIGHT // 2 + i * 100, 200, 50))
                # Draw the border in config.grey
                pygame.draw.rect(screen, config.YELLOW, (config.WIDTH // 2 - 100, config.HEIGHT // 2 + i * 100, 200, 50), 5)
                # Draw the text in config.black
                draw_text(option, font, config.BLACK, config.WIDTH // 2, config.HEIGHT // 2 + i * 100 + 25)
            else:
                # Draw the unselected option's border in white
                pygame.draw.rect(screen, config.WHITE, (config.WIDTH // 2 - 100, config.HEIGHT // 2 + i * 100, 200, 50), 5)
                # Draw the text in white
                draw_text(option, font, config.WHITE, config.WIDTH // 2, config.HEIGHT // 2 + i * 100 + 25)

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
                    select_sound.play()
                    current_selection = (current_selection - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    select_sound.play()
                    current_selection = (current_selection + 1) % len(menu_options)


# Gameplay Loop
def gameplay_a(player_health, mode, level_info, player_score, current_level):
    word_to_type = generate_random_word_a(current_level)
    # player_score = 0
    current_score = 0  # Total score accumulated throughout the game
    score_multiplier = 1  # Initialize the score multiplier
    max_multiplier = 10  # Set the maximum multiplier
    clock = pygame.time.Clock()
    falling_words = []
    spaceship = Spaceship()
    player_word = ""

    # Variables for displaying multiplier streak
    multiplier_streak = 0
    multiplier_display_timer = 0
    if mode == "Adventure" and level_info is not None:
        level = level_info["level"]
        word_speed = level_info["speed"]
        words_to_destroy = level_info["word_count"]
        words_destroyed = 0
    else:
        # Default settings for Survivor Mode
        word_speed = 1
        level = None

    running = True

    while running and player_health > 0:
        screen.blit(background_image, (0, 0))
        for particle in Particle.particles:
            particle.update()

        # Draw everything
        screen.fill(config.BLACK)  # Fill the screen with the background color
        for particle in Particle.particles:
            particle.draw()

        # Display the falling word for the player to type
        if len(falling_words) < 4 and random.randint(0, 100) < 2:
            new_word = FallingWordA(falling_words, current_level)  # Pass current_level to the constructor
            if mode == "Adventure":
                new_word.speed = word_speed  # Set word speed based on level
            falling_words.append(new_word)

        # Display the input word
        draw_text(player_word, font, config.WHITE, config.WIDTH // 2, config.HEIGHT - 150)
        draw_text(f"Words Left: {words_to_destroy - words_destroyed}", font, config.WHITE, 95, 50)
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    result = pause_game()
                    if result == "Main Menu":
                        running = False

                elif event.key == pygame.K_BACKSPACE:
                    player_word = player_word[:-1]  # Remove the last character from the input word
                else:
                    player_word += event.unicode
                    
                    correct_word = None
                    for word in falling_words:
                        if player_word == word.word:
                            correct_word = word
                            break
                
                    if correct_word:
                            
                            correct_sound.play()
                            word_length = len(correct_word.word)
                            # Increase the score with multiplier
                            player_score += word_length * 100 * score_multiplier
                            current_score += word_length * 100 * score_multiplier
                            # Increase the multiplier, cap at max_multiplier
                            score_multiplier = min(score_multiplier + 1, max_multiplier)
                            # missile_image = pygame.image.load("assets/missile.png")
                            spaceship.shoot_missile(correct_word, missile_image)
                            # falling_words.remove(correct_word)
                            player_word = ""
                            if mode == "Adventure":
                                words_destroyed += 1
                                if words_destroyed == words_to_destroy:
                                # Level completed
                                    return {
                                    "player_health": player_health,
                                    "player_score": player_score
                                }

        # Update and draw missiles
        spaceship.update_missiles(falling_words)
        spaceship.draw_missiles()

        # Update and draw falling words
        for word in falling_words:
            if word.update(player_health):  # Pass player_health as an argument
                falling_words.remove(word)
            else:
                word.draw(player_word)

        # Check for collision 
        for word in falling_words:
            if word.rect.y >= spaceship.rect.top and word.rect.y <= spaceship.rect.bottom and \
                    word.rect.x >= spaceship.rect.left and word.rect.x <= spaceship.rect.right:
                if player_word == word.word:
                    player_score += 200 * score_multiplier  # Multiply score by multiplier
                    current_score += 200 * score_multiplier # Add to total score
                    # falling_words.remove(word)
                    player_word = ""
                    break
                else:
                    # If the spaceship collides with an incorrect word, handle it accordingly
                    player_health -= 1
                    score_multiplier = 1  # Reset multiplier when health decreases
                    falling_words.remove(word)
                    player_word = ""  # Clear the input word immediately

        # Check for words that have passed the deadzone line
        for word in falling_words:
            if word.rect.y > DEADZONE_LINE:
                if player_word == word.word:
                    player_score += 200 * score_multiplier  # Multiply score by multiplier
                    current_score += 200 * score_multiplier  # Add to total score
                else:
                    # If an incorrect word passes the deadzone line, handle it accordingly
                    player_health -= 1
                    loss_hp_sound.play()
                    score_multiplier = 1  # Reset multiplier when health decreases
                falling_words.remove(word)

        # Display player score and health
        draw_text(f"Score : {player_score}", font, config.WHITE, 95, 20)  # Top left
        #draw_text(f"CountingScore : {current_score}", font, config.WHITE, 80, 60)  # Display total score
        draw_health(player_health, 15, 65) # Top right



        # Display multiplier streak
        if multiplier_display_timer > 0:
            draw_text(f"Multiplier: {score_multiplier}x", font, config.WHITE, config.WIDTH - 150, 20)
            multiplier_display_timer -= 1

        # Display the spaceship
        spaceship.update()
        spaceship.draw()

        # Remove words that have fallen off the screen
        falling_words = [word for word in falling_words if word.rect.y < config.HEIGHT]
        

        # Update multiplier display timer
        if score_multiplier > 1:
            multiplier_display_timer = 120  # Reset the display timer if multiplier is active

        if player_health <= 0:
            game_over_sound.play()
        pygame.display.flip()
        clock.tick(config.FPS)

    # Game Over menu
    return game_over_menu_a(player_score)
def adventure_mode():
    current_level = 1
    player_health = 3  # Reset health for adventure mode
    player_score = 0
    levels = [
        {"level": 1, "speed": 0.5, "word_count": 10},
        {"level": 2, "speed": 0.5, "word_count": 15},
        {"level": 3, "speed": 1, "word_count": 20},
        {"level": 4, "speed": 1.2, "word_count": 25},
        {"level": 5, "speed": 1.3, "word_count": 5},
        {"level": 6, "speed": 1.5, "word_count": 5},
        {"level": 7, "speed": 1.7, "word_count": 5},
        {"level": 8, "speed": 2, "word_count": 5},
        {"level": 9, "speed": 2.2, "word_count": 5},
        {"level": 10, "speed":2.5, "word_count": 5}
        # Add more levels as needed
    ]

    selected_level = select_adventure_level()
    if selected_level == "Main Menu":
        return "Main Menu"  # Return to main menu without continuing

    # Convert the selected level (1-indexed) to the appropriate index
    current_level = int(selected_level)  # Selected level is returned as a number (1-10)

    # current_level = selected_level

    while current_level <= len(levels):
        level_info = levels[current_level - 1]  # Get the current level's info

        # Call the gameplay function, passing relevant information
        result = gameplay_a(player_health, mode="Adventure", level_info=level_info, player_score=player_score, current_level=current_level)

        if isinstance(result, str):  # If result is a string (like "Game Over" or "Main Menu")
            if result == "Game Over":
                return game_over_menu_a(player_score)
            elif result == "Main Menu":
                return main_menu()
        else:
            # Update player health and score between levels
            player_health = result.get("player_health", player_health)  # Use .get() to avoid KeyError
            player_score = result.get("player_score", player_score)

            # Optionally, show a level complete screen
            level_complete_screen(level_info["level"], player_score)

            # Move to the next level
            current_level += 1
    # If all levels are completed
    return game_completed_screen(player_score)

# In your main game loop
menu_option = main_menu()

while menu_option != "Exit":
    if menu_option == "Survivor":
        menu_option = survivor_mode(player_health)
    elif menu_option == "Adventure":
        menu_option = adventure_mode()
    elif menu_option == "Time Trial":
        menu_option = time_trial_mode(score)
    elif menu_option == "Lesson":
        menu_option = run_lessons() # Pass the screen object to the lesson function
    elif menu_option == "Select Mode":
        menu_option = select_mode()
    elif menu_option == "Main Menu":
        menu_option = main_menu()

        
