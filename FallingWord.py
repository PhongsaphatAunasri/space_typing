import pygame
import random
import sys
import csv
import math
import config 
import time
import Missile
# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))

background_image = pygame.image.load("assets/bg.png")  # Replace with your actual background image
spaceship_image = pygame.image.load("assets/ship.png")
meteor_image = pygame.image.load("assets/meteor-3.png")


# ufo_image = pygame.image.load("assets/ufo.png")




font = config.FONT_MAIN
def generate_random_word():
    return random.choice(survivor_words)
def word_stage1():
    return random.choice(level_1_words)
def word_stage2():
    return random.choice(level_2_words)
def word_stage3():
    return random.choice(level_3_words)
def word_stage4():
    return random.choice(level_4_words)
def word_stage5():
    return random.choice(level_5_words)
def word_stage6():
    return random.choice(level_6_words)
def word_stage7():
    return random.choice(level_7_words)
def word_stage8():
    return random.choice(level_8_words)
def word_stage9():
    return random.choice(level_9_words)
def word_stage10():
    return random.choice(level_10_words)

def load_words_level(file_path):
    words = []
    with open(file_path, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            words.extend(row)
    return words
level_1_words = load_words_level("assets/csv/stage1.csv")
level_2_words = load_words_level("assets/csv/stage2.csv")
level_3_words = load_words_level("assets/csv/stage3.csv")
level_4_words = load_words_level("assets/csv/stage4.csv")
level_5_words = load_words_level("assets/csv/stage5.csv")
level_6_words = load_words_level("assets/csv/stage6.csv")
level_7_words = load_words_level("assets/csv/stage7.csv")
level_8_words = load_words_level("assets/csv/stage8.csv")
level_9_words = load_words_level("assets/csv/stage9.csv")
level_10_words = load_words_level("assets/csv/stage10.csv")
survivor_words = load_words_level("assets/word.csv")

def load_words(file_path):
    words = []
    with open(file_path, "r") as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            words.extend(row)
    return words

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
        pass
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
            self.rect.y -= 10 * step_back_count  # Move the word back by 2 pixels for each newly correct letter
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
        pass
        # Draw each character in the word with appropriate color
        for i, char in enumerate(self.word):
            if i < len(player_word) and char == player_word[i]:
                char_color = config.CYAN  # Color for correct letters
            else:
                char_color = config.TEAL  # Keep the other letters white
            char_surface = font.render(char, True, char_color)
            char_rect = char_surface.get_rect(center=(x_offset + font.size(char)[0] / 2, y_offset))
            screen.blit(char_surface, char_rect.topleft)

            # Update the x-coordinate for the next character
            x_offset += font.size(char)[0]
        pass
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
        pass
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
        pass
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
            char_color = config.DARKGREEN
            if i < len(player_word) and char == player_word[i]:
                char_color = config.LIME
            char_surface = font.render(char, True, char_color)
            char_rect = char_surface.get_rect(center=(x_offset + font.size(char)[0] / 2, y_offset))
            screen.blit(char_surface, char_rect.topleft)
            x_offset += font.size(char)[0]
    def hit_by_missile(self):
        pass

class FallingWordAdventure:
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
        pass
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
        pass
        # Draw each character in the word with appropriate color
        for i, char in enumerate(self.word):
            if i < len(player_word) and char == player_word[i]:
                char_color = config.CYAN  # Color for correct letters
            else:
                char_color = config.TEAL  # Keep the other letters white
            char_surface = font.render(char, True, char_color)
            char_rect = char_surface.get_rect(center=(x_offset + font.size(char)[0] / 2, y_offset))
            screen.blit(char_surface, char_rect.topleft)

            # Update the x-coordinate for the next character
            x_offset += font.size(char)[0]
        pass
    def hit_by_missile(self):
        # Define what happens when the word is hit by a missile
        # Remove the word from the set of words in play
        if self.word in FallingWord.words_in_play:
            FallingWord.words_in_play.remove(self.word)
        pass  # Add any additional logic for handling the hit
    
class Stage1:
    words_in_play = set()  # Static variable to keep track of current words in play

    def __init__(self, existing_words, speed,x):
        # Generate a random word and ensure it is not already in play
        self.word = word_stage1()
        while self.word in FallingWord.words_in_play:
            self.word = word_stage1()

        # Add the word to the set of words currently in play
        FallingWord.words_in_play.add(self.word)

        # Set up the position and speed
        self.rect = pygame.Rect(0, 0, 50, 10)  # Initial rect, position will be adjusted
        self.rect.midtop = (x, 0)  # Adjust the range

        # Ensure the new word doesn't overlap with existing words' positions
        while any(word.rect.colliderect(self.rect) for word in existing_words):
            self.rect.midtop = (random.randint(100, config.WIDTH - 50), 0)  # Update the position

        self.speed = speed
        self.rotation_angle = 0  # Initialize the rotation angle
        self.rotation_speed = random.uniform(0.5, 1)  # Random rotation speed
        self.correct_letters_stepped_back = 0
        pass
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
        pass
        # Draw each character in the word with appropriate color
        for i, char in enumerate(self.word):
            if i < len(player_word) and char == player_word[i]:
                char_color = config.CYAN  # Color for correct letters
            else:
                char_color = config.TEAL  # Keep the other letters white
            char_surface = font.render(char, True, char_color)
            char_rect = char_surface.get_rect(center=(x_offset + font.size(char)[0] / 2, y_offset))
            screen.blit(char_surface, char_rect.topleft)

            # Update the x-coordinate for the next character
            x_offset += font.size(char)[0]
        pass
    def hit_by_missile(self):
        # Define what happens when the word is hit by a missile
        # Remove the word from the set of words in play
        if self.word in FallingWord.words_in_play:
            FallingWord.words_in_play.remove(self.word)
        pass  # Add any additional logic for handling the hit

class Stage2:
    words_in_play = set()  # Static variable to keep track of current words in play

    def __init__(self, existing_words, speed,x):
        # Generate a random word and ensure it is not already in play
        self.word = word_stage2()
        while self.word in FallingWord.words_in_play:
            self.word = word_stage2()

        # Add the word to the set of words currently in play
        FallingWord.words_in_play.add(self.word)

        # Set up the position and speed
        self.rect = pygame.Rect(0, 0, 50, 10)  # Initial rect, position will be adjusted
        self.rect.midtop = (x, 0)  # Adjust the range

        # Ensure the new word doesn't overlap with existing words' positions
        while any(word.rect.colliderect(self.rect) for word in existing_words):
            self.rect.midtop = (random.randint(100, config.WIDTH - 50), 0)  # Update the position

        self.speed = speed
        self.rotation_angle = 0  # Initialize the rotation angle
        self.rotation_speed = random.uniform(0.5, 1)  # Random rotation speed
        self.correct_letters_stepped_back = 0
        pass
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
        pass
        # Draw each character in the word with appropriate color
        for i, char in enumerate(self.word):
            if i < len(player_word) and char == player_word[i]:
                char_color = config.CYAN  # Color for correct letters
            else:
                char_color = config.TEAL  # Keep the other letters white
            char_surface = font.render(char, True, char_color)
            char_rect = char_surface.get_rect(center=(x_offset + font.size(char)[0] / 2, y_offset))
            screen.blit(char_surface, char_rect.topleft)

            # Update the x-coordinate for the next character
            x_offset += font.size(char)[0]
        pass
    def hit_by_missile(self):
        # Define what happens when the word is hit by a missile
        # Remove the word from the set of words in play
        if self.word in FallingWord.words_in_play:
            FallingWord.words_in_play.remove(self.word)
        pass  # Add any additional logic for handling the hit

class Stage3:
    words_in_play = set()  # Static variable to keep track of current words in play

    def __init__(self, existing_words, speed,x):
        # Generate a random word and ensure it is not already in play
        self.word = word_stage3()
        while self.word in FallingWord.words_in_play:
            self.word = word_stage3()

        # Add the word to the set of words currently in play
        FallingWord.words_in_play.add(self.word)

        # Set up the position and speed
        self.rect = pygame.Rect(0, 0, 50, 10)  # Initial rect, position will be adjusted
        self.rect.midtop = (x, 0)  # Adjust the range

        # Ensure the new word doesn't overlap with existing words' positions
        while any(word.rect.colliderect(self.rect) for word in existing_words):
            self.rect.midtop = (random.randint(100, config.WIDTH - 50), 0)  # Update the position

        self.speed = speed
        self.rotation_angle = 0  # Initialize the rotation angle
        self.rotation_speed = random.uniform(0.5, 1)  # Random rotation speed
        self.correct_letters_stepped_back = 0
        pass
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
        pass
        # Draw each character in the word with appropriate color
        for i, char in enumerate(self.word):
            if i < len(player_word) and char == player_word[i]:
                char_color = config.CYAN  # Color for correct letters
            else:
                char_color = config.TEAL  # Keep the other letters white
            char_surface = font.render(char, True, char_color)
            char_rect = char_surface.get_rect(center=(x_offset + font.size(char)[0] / 2, y_offset))
            screen.blit(char_surface, char_rect.topleft)

            # Update the x-coordinate for the next character
            x_offset += font.size(char)[0]
        pass
    def hit_by_missile(self):
        # Define what happens when the word is hit by a missile
        # Remove the word from the set of words in play
        if self.word in FallingWord.words_in_play:
            FallingWord.words_in_play.remove(self.word)
        pass  # Add any additional logic for handling the hit
    
class Stage4:
    words_in_play = set()  # Static variable to keep track of current words in play

    def __init__(self, existing_words, speed,x):
        # Generate a random word and ensure it is not already in play
        self.word = word_stage4()
        while self.word in FallingWord.words_in_play:
            self.word = word_stage4()

        # Add the word to the set of words currently in play
        FallingWord.words_in_play.add(self.word)

        # Set up the position and speed
        self.rect = pygame.Rect(0, 0, 50, 10)  # Initial rect, position will be adjusted
        self.rect.midtop = (x, 0)  # Adjust the range

        # Ensure the new word doesn't overlap with existing words' positions
        while any(word.rect.colliderect(self.rect) for word in existing_words):
            self.rect.midtop = (random.randint(100, config.WIDTH - 50), 0)  # Update the position

        self.speed = speed
        self.rotation_angle = 0  # Initialize the rotation angle
        self.rotation_speed = random.uniform(0.5, 1)  # Random rotation speed
        self.correct_letters_stepped_back = 0
        pass
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
        pass
        # Draw each character in the word with appropriate color
        for i, char in enumerate(self.word):
            if i < len(player_word) and char == player_word[i]:
                char_color = config.CYAN  # Color for correct letters
            else:
                char_color = config.TEAL  # Keep the other letters white
            char_surface = font.render(char, True, char_color)
            char_rect = char_surface.get_rect(center=(x_offset + font.size(char)[0] / 2, y_offset))
            screen.blit(char_surface, char_rect.topleft)

            # Update the x-coordinate for the next character
            x_offset += font.size(char)[0]
        pass
    def hit_by_missile(self):
        # Define what happens when the word is hit by a missile
        # Remove the word from the set of words in play
        if self.word in FallingWord.words_in_play:
            FallingWord.words_in_play.remove(self.word)
        pass  # Add any additional logic for handling the hit
    
class Stage5:
    words_in_play = set()  # Static variable to keep track of current words in play

    def __init__(self, existing_words, speed,x):
        # Generate a random word and ensure it is not already in play
        self.word = word_stage5()
        while self.word in FallingWord.words_in_play:
            self.word = word_stage5()

        # Add the word to the set of words currently in play
        FallingWord.words_in_play.add(self.word)

        # Set up the position and speed
        self.rect = pygame.Rect(0, 0, 50, 10)  # Initial rect, position will be adjusted
        self.rect.midtop = (x, 0)  # Adjust the range

        # Ensure the new word doesn't overlap with existing words' positions
        while any(word.rect.colliderect(self.rect) for word in existing_words):
            self.rect.midtop = (random.randint(100, config.WIDTH - 50), 0)  # Update the position

        self.speed = speed
        self.rotation_angle = 0  # Initialize the rotation angle
        self.rotation_speed = random.uniform(0.5, 1)  # Random rotation speed
        self.correct_letters_stepped_back = 0
        pass
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
        pass
        # Draw each character in the word with appropriate color
        for i, char in enumerate(self.word):
            if i < len(player_word) and char == player_word[i]:
                char_color = config.CYAN  # Color for correct letters
            else:
                char_color = config.TEAL  # Keep the other letters white
            char_surface = font.render(char, True, char_color)
            char_rect = char_surface.get_rect(center=(x_offset + font.size(char)[0] / 2, y_offset))
            screen.blit(char_surface, char_rect.topleft)

            # Update the x-coordinate for the next character
            x_offset += font.size(char)[0]
        pass
    def hit_by_missile(self):
        # Define what happens when the word is hit by a missile
        # Remove the word from the set of words in play
        if self.word in FallingWord.words_in_play:
            FallingWord.words_in_play.remove(self.word)
        pass  # Add any additional logic for handling the hit
    
class Stage6:
    words_in_play = set()  # Static variable to keep track of current words in play

    def __init__(self, existing_words, speed,x):
        # Generate a random word and ensure it is not already in play
        self.word = word_stage6()
        while self.word in FallingWord.words_in_play:
            self.word = word_stage6()

        # Add the word to the set of words currently in play
        FallingWord.words_in_play.add(self.word)

        # Set up the position and speed
        self.rect = pygame.Rect(0, 0, 50, 10)  # Initial rect, position will be adjusted
        self.rect.midtop = (x, 0)  # Adjust the range

        # Ensure the new word doesn't overlap with existing words' positions
        while any(word.rect.colliderect(self.rect) for word in existing_words):
            self.rect.midtop = (random.randint(100, config.WIDTH - 50), 0)  # Update the position

        self.speed = speed
        self.rotation_angle = 0  # Initialize the rotation angle
        self.rotation_speed = random.uniform(0.5, 1)  # Random rotation speed
        self.correct_letters_stepped_back = 0
        pass
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
        pass
        # Draw each character in the word with appropriate color
        for i, char in enumerate(self.word):
            if i < len(player_word) and char == player_word[i]:
                char_color = config.CYAN  # Color for correct letters
            else:
                char_color = config.TEAL  # Keep the other letters white
            char_surface = font.render(char, True, char_color)
            char_rect = char_surface.get_rect(center=(x_offset + font.size(char)[0] / 2, y_offset))
            screen.blit(char_surface, char_rect.topleft)

            # Update the x-coordinate for the next character
            x_offset += font.size(char)[0]
        pass
    def hit_by_missile(self):
        # Define what happens when the word is hit by a missile
        # Remove the word from the set of words in play
        if self.word in FallingWord.words_in_play:
            FallingWord.words_in_play.remove(self.word)
        pass  # Add any additional logic for handling the hit
    
class Stage7:
    words_in_play = set()  # Static variable to keep track of current words in play

    def __init__(self, existing_words, speed,x):
        # Generate a random word and ensure it is not already in play
        self.word = word_stage7()
        while self.word in FallingWord.words_in_play:
            self.word = word_stage7()

        # Add the word to the set of words currently in play
        FallingWord.words_in_play.add(self.word)

        # Set up the position and speed
        self.rect = pygame.Rect(0, 0, 50, 10)  # Initial rect, position will be adjusted
        self.rect.midtop = (x, 0)  # Adjust the range

        # Ensure the new word doesn't overlap with existing words' positions
        while any(word.rect.colliderect(self.rect) for word in existing_words):
            self.rect.midtop = (random.randint(100, config.WIDTH - 50), 0)  # Update the position

        self.speed = speed
        self.rotation_angle = 0  # Initialize the rotation angle
        self.rotation_speed = random.uniform(0.5, 1)  # Random rotation speed
        self.correct_letters_stepped_back = 0
        pass
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
        pass
        # Draw each character in the word with appropriate color
        for i, char in enumerate(self.word):
            if i < len(player_word) and char == player_word[i]:
                char_color = config.CYAN  # Color for correct letters
            else:
                char_color = config.TEAL  # Keep the other letters white
            char_surface = font.render(char, True, char_color)
            char_rect = char_surface.get_rect(center=(x_offset + font.size(char)[0] / 2, y_offset))
            screen.blit(char_surface, char_rect.topleft)

            # Update the x-coordinate for the next character
            x_offset += font.size(char)[0]
        pass
    def hit_by_missile(self):
        # Define what happens when the word is hit by a missile
        # Remove the word from the set of words in play
        if self.word in FallingWord.words_in_play:
            FallingWord.words_in_play.remove(self.word)
        pass  # Add any additional logic for handling the hit
    
class Stage8:
    words_in_play = set()  # Static variable to keep track of current words in play

    def __init__(self, existing_words, speed,x):
        # Generate a random word and ensure it is not already in play
        self.word = word_stage8()
        while self.word in FallingWord.words_in_play:
            self.word = word_stage8()

        # Add the word to the set of words currently in play
        FallingWord.words_in_play.add(self.word)

        # Set up the position and speed
        self.rect = pygame.Rect(0, 0, 50, 10)  # Initial rect, position will be adjusted
        self.rect.midtop = (x, 0)  # Adjust the range

        # Ensure the new word doesn't overlap with existing words' positions
        while any(word.rect.colliderect(self.rect) for word in existing_words):
            self.rect.midtop = (random.randint(100, config.WIDTH - 50), 0)  # Update the position

        self.speed = speed
        self.rotation_angle = 0  # Initialize the rotation angle
        self.rotation_speed = random.uniform(0.5, 1)  # Random rotation speed
        self.correct_letters_stepped_back = 0
        pass
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
        pass
        # Draw each character in the word with appropriate color
        for i, char in enumerate(self.word):
            if i < len(player_word) and char == player_word[i]:
                char_color = config.CYAN  # Color for correct letters
            else:
                char_color = config.TEAL  # Keep the other letters white
            char_surface = font.render(char, True, char_color)
            char_rect = char_surface.get_rect(center=(x_offset + font.size(char)[0] / 2, y_offset))
            screen.blit(char_surface, char_rect.topleft)

            # Update the x-coordinate for the next character
            x_offset += font.size(char)[0]
        pass
    def hit_by_missile(self):
        # Define what happens when the word is hit by a missile
        # Remove the word from the set of words in play
        if self.word in FallingWord.words_in_play:
            FallingWord.words_in_play.remove(self.word)
        pass  # Add any additional logic for handling the hit
    
class Stage9:
    words_in_play = set()  # Static variable to keep track of current words in play

    def __init__(self, existing_words, speed,x):
        # Generate a random word and ensure it is not already in play
        self.word = word_stage9()
        while self.word in FallingWord.words_in_play:
            self.word = word_stage9()

        # Add the word to the set of words currently in play
        FallingWord.words_in_play.add(self.word)

        # Set up the position and speed
        self.rect = pygame.Rect(0, 0, 50, 10)  # Initial rect, position will be adjusted
        self.rect.midtop = (x, 0)  # Adjust the range

        # Ensure the new word doesn't overlap with existing words' positions
        while any(word.rect.colliderect(self.rect) for word in existing_words):
            self.rect.midtop = (random.randint(100, config.WIDTH - 50), 0)  # Update the position

        self.speed = speed
        self.rotation_angle = 0  # Initialize the rotation angle
        self.rotation_speed = random.uniform(0.5, 1)  # Random rotation speed
        self.correct_letters_stepped_back = 0
        pass
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
        pass
        # Draw each character in the word with appropriate color
        for i, char in enumerate(self.word):
            if i < len(player_word) and char == player_word[i]:
                char_color = config.CYAN  # Color for correct letters
            else:
                char_color = config.TEAL  # Keep the other letters white
            char_surface = font.render(char, True, char_color)
            char_rect = char_surface.get_rect(center=(x_offset + font.size(char)[0] / 2, y_offset))
            screen.blit(char_surface, char_rect.topleft)

            # Update the x-coordinate for the next character
            x_offset += font.size(char)[0]
        pass
    def hit_by_missile(self):
        # Define what happens when the word is hit by a missile
        # Remove the word from the set of words in play
        if self.word in FallingWord.words_in_play:
            FallingWord.words_in_play.remove(self.word)
        pass  # Add any additional logic for handling the hit
    
class Stage10:
    words_in_play = set()  # Static variable to keep track of current words in play

    def __init__(self, existing_words, speed,x):
        # Generate a random word and ensure it is not already in play
        self.word = word_stage10()
        while self.word in FallingWord.words_in_play:
            self.word = word_stage10()

        # Add the word to the set of words currently in play
        FallingWord.words_in_play.add(self.word)

        # Set up the position and speed
        self.rect = pygame.Rect(0, 0, 50, 10)  # Initial rect, position will be adjusted
        self.rect.midtop = (x, 0)  # Adjust the range

        # Ensure the new word doesn't overlap with existing words' positions
        while any(word.rect.colliderect(self.rect) for word in existing_words):
            self.rect.midtop = (random.randint(100, config.WIDTH - 50), 0)  # Update the position

        self.speed = speed
        self.rotation_angle = 0  # Initialize the rotation angle
        self.rotation_speed = random.uniform(0.5, 1)  # Random rotation speed
        self.correct_letters_stepped_back = 0
        pass
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
        pass
        # Draw each character in the word with appropriate color
        for i, char in enumerate(self.word):
            if i < len(player_word) and char == player_word[i]:
                char_color = config.CYAN  # Color for correct letters
            else:
                char_color = config.TEAL  # Keep the other letters white
            char_surface = font.render(char, True, char_color)
            char_rect = char_surface.get_rect(center=(x_offset + font.size(char)[0] / 2, y_offset))
            screen.blit(char_surface, char_rect.topleft)

            # Update the x-coordinate for the next character
            x_offset += font.size(char)[0]
        pass
    def hit_by_missile(self):
        # Define what happens when the word is hit by a missile
        # Remove the word from the set of words in play
        if self.word in FallingWord.words_in_play:
            FallingWord.words_in_play.remove(self.word)
        pass  # Add any additional logic for handling the hit