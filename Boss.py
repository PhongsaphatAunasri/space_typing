import pygame
import csv
import config

class Boss:
    def __init__(self, x, y, health, animation_speed=200, word_file="assets/word.csv"):
        self.sprites = [
            pygame.image.load("assets/boss/Boss-stage5-1.png"),
            pygame.image.load("assets/boss/Boss-stage5-2.png"),
            pygame.image.load("assets/boss/Boss-stage5-3.png"),
            pygame.image.load("assets/boss/Boss-stage5-4.png"),
        ]
        
        self.sprite_width = self.sprites[0].get_width()  # Get sprite width
        self.sprite_height = self.sprites[0].get_height()  # Get sprite height

        self.x = (config.WIDTH - self.sprite_width) // 2  # Center x properly
        self.y = y  # Keep y as is

        self.health = health
        self.max_health = health
        self.boss_words = self.load_words(word_file)
        self.current_word_index = 0
        self.current_word = None

        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = animation_speed

        self.health_bar_width = 300
        self.health_bar_height = 20
        self.health_bar_offset = 10


    def load_words(self, word_file):
        words = []
        try:
            with open(word_file, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)  # Automatically handles commas as delimiters
                for row in reader:
                    for word in row:  # Split each row into individual words
                        cleaned_word = word.strip()  # Remove leading/trailing spaces
                        if cleaned_word:  # Skip empty words
                            words.append(cleaned_word)
        except FileNotFoundError:
            print(f"Error: {word_file} not found. Using default boss words.")
            words = ["bossword1", "bossword2", "bossword3"]  # Default words
        return words

    def update(self, delta_time):
        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.sprites)

    def draw(self, screen):
        # Draw the boss sprite
        sprite = self.sprites[self.current_frame]
        screen.blit(sprite, (self.x, self.y))

        # Draw the health bar
        health_ratio = self.health / self.max_health
        health_bar_x = self.x + (sprite.get_width() - self.health_bar_width) // 2
        health_bar_y = self.y - self.health_bar_offset

        # Background of the health bar
        pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, self.health_bar_width, self.health_bar_height))
        # Foreground (current health)
        pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, self.health_bar_width * health_ratio, self.health_bar_height))

    def take_damage(self, damage):
        self.health = max(0, self.health - damage)

    def is_defeated(self):
        return self.health <= 0

    def get_next_word(self):
        if self.current_word_index < len(self.boss_words):
            self.current_word = self.boss_words[self.current_word_index]  # Store the current word
            self.current_word_index += 1
            return self.current_word
        else:
            self.current_word = None  # No more words, boss is defeated
            return None
class Boss1:
    def __init__(self, x, y, health, animation_speed=200, word_file="assets/csv/boss1.csv"):
        self.sprites = [
            pygame.image.load("assets/boss/Boss-stage1-1.png"),
            pygame.image.load("assets/boss/Boss-stage1-2.png"),
            pygame.image.load("assets/boss/Boss-stage1-3.png"),
            pygame.image.load("assets/boss/Boss-stage1-4.png"),
        ]
        
        self.sprite_width = self.sprites[0].get_width()  # Get sprite width
        self.sprite_height = self.sprites[0].get_height()  # Get sprite height

        self.x = (config.WIDTH - self.sprite_width) // 2  # Center x properly
        self.y = y  # Keep y as is

        self.health = health
        self.max_health = health
        self.boss_words = self.load_words(word_file)
        self.current_word_index = 0
        self.current_word = None

        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = animation_speed

        self.health_bar_width = 300
        self.health_bar_height = 20
        self.health_bar_offset = 50


    def load_words(self, word_file):
        words = []
        try:
            with open(word_file, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)  # Automatically handles commas as delimiters
                for row in reader:
                    for word in row:  # Split each row into individual words
                        cleaned_word = word.strip()  # Remove leading/trailing spaces
                        if cleaned_word:  # Skip empty words
                            words.append(cleaned_word)
        except FileNotFoundError:
            print(f"Error: {word_file} not found. Using default boss words.")
            words = ["bossword1", "bossword2", "bossword3"]  # Default words
        return words

    def update(self, delta_time):
        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.sprites)

    def draw(self, screen):
        # Draw the boss sprite
        sprite = self.sprites[self.current_frame]
        screen.blit(sprite, (self.x, self.y))

        # Draw the health bar
        health_ratio = self.health / self.max_health
        health_bar_x = self.x + (sprite.get_width() - self.health_bar_width) // 2
        health_bar_y = self.y - self.health_bar_offset

        # Background of the health bar
        pygame.draw.rect(screen, config.GREY, (health_bar_x, health_bar_y, self.health_bar_width, self.health_bar_height))
        # Foreground (current health)
        pygame.draw.rect(screen, config.RED, (health_bar_x, health_bar_y, self.health_bar_width * health_ratio, self.health_bar_height))

    def take_damage(self, damage):
        self.health = max(0, self.health - damage)

    def is_defeated(self):
        return self.health <= 0

    def get_next_word(self):
        if self.current_word_index < len(self.boss_words):
            self.current_word = self.boss_words[self.current_word_index]  # Store the current word
            self.current_word_index += 1
            return self.current_word
        else:
            self.current_word = None  # No more words, boss is defeated
            return None
        
class Boss2:
    def __init__(self, x, y, health, animation_speed=200, word_file="assets/csv/boss2.csv"):
        self.sprites = [
            pygame.image.load("assets/boss/Boss-stage2-1.png"),
            pygame.image.load("assets/boss/Boss-stage2-2.png"),
            pygame.image.load("assets/boss/Boss-stage2-3.png"),
            pygame.image.load("assets/boss/Boss-stage2-4.png"),
        ]
        
        self.sprite_width = self.sprites[0].get_width()  # Get sprite width
        self.sprite_height = self.sprites[0].get_height()  # Get sprite height

        self.x = (config.WIDTH - self.sprite_width) // 2  # Center x properly
        self.y = y  # Keep y as is

        self.health = health
        self.max_health = health
        self.boss_words = self.load_words(word_file)
        self.current_word_index = 0
        self.current_word = None

        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = animation_speed

        self.health_bar_width = 300
        self.health_bar_height = 20
        self.health_bar_offset = 50


    def load_words(self, word_file):
        words = []
        try:
            with open(word_file, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)  # Automatically handles commas as delimiters
                for row in reader:
                    for word in row:  # Split each row into individual words
                        cleaned_word = word.strip()  # Remove leading/trailing spaces
                        if cleaned_word:  # Skip empty words
                            words.append(cleaned_word)
        except FileNotFoundError:
            print(f"Error: {word_file} not found. Using default boss words.")
            words = ["bossword1", "bossword2", "bossword3"]  # Default words
        return words

    def update(self, delta_time):
        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.sprites)

    def draw(self, screen):
        # Draw the boss sprite
        sprite = self.sprites[self.current_frame]
        screen.blit(sprite, (self.x, self.y))

        # Draw the health bar
        health_ratio = self.health / self.max_health
        health_bar_x = self.x + (sprite.get_width() - self.health_bar_width) // 2
        health_bar_y = self.y - self.health_bar_offset

        # Background of the health bar
        pygame.draw.rect(screen, config.GREY, (health_bar_x, health_bar_y, self.health_bar_width, self.health_bar_height))
        # Foreground (current health)
        pygame.draw.rect(screen, config.RED, (health_bar_x, health_bar_y, self.health_bar_width * health_ratio, self.health_bar_height))

    def take_damage(self, damage):
        self.health = max(0, self.health - damage)

    def is_defeated(self):
        return self.health <= 0

    def get_next_word(self):
        if self.current_word_index < len(self.boss_words):
            self.current_word = self.boss_words[self.current_word_index]  # Store the current word
            self.current_word_index += 1
            return self.current_word
        else:
            self.current_word = None  # No more words, boss is defeated
            return None
        
class Boss3:
    def __init__(self, x, y, health, animation_speed=200, word_file="assets/csv/boss3.csv"):
        self.sprites = [
            pygame.image.load("assets/boss/Boss-stage3-1.png"),
            pygame.image.load("assets/boss/Boss-stage3-2.png"),
            pygame.image.load("assets/boss/Boss-stage3-3.png"),
            pygame.image.load("assets/boss/Boss-stage3-4.png"),
        ]
        
        self.sprite_width = self.sprites[0].get_width()  # Get sprite width
        self.sprite_height = self.sprites[0].get_height()  # Get sprite height

        self.x = (config.WIDTH - self.sprite_width) // 2  # Center x properly
        self.y = y  # Keep y as is

        self.health = health
        self.max_health = health
        self.boss_words = self.load_words(word_file)
        self.current_word_index = 0
        self.current_word = None

        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = animation_speed

        self.health_bar_width = 300
        self.health_bar_height = 20
        self.health_bar_offset = 50


    def load_words(self, word_file):
        words = []
        try:
            with open(word_file, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)  # Automatically handles commas as delimiters
                for row in reader:
                    for word in row:  # Split each row into individual words
                        cleaned_word = word.strip()  # Remove leading/trailing spaces
                        if cleaned_word:  # Skip empty words
                            words.append(cleaned_word)
        except FileNotFoundError:
            print(f"Error: {word_file} not found. Using default boss words.")
            words = ["bossword1", "bossword2", "bossword3"]  # Default words
        return words

    def update(self, delta_time):
        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.sprites)

    def draw(self, screen):
        # Draw the boss sprite
        sprite = self.sprites[self.current_frame]
        screen.blit(sprite, (self.x, self.y))

        # Draw the health bar
        health_ratio = self.health / self.max_health
        health_bar_x = self.x + (sprite.get_width() - self.health_bar_width) // 2
        health_bar_y = self.y - self.health_bar_offset

        # Background of the health bar
        pygame.draw.rect(screen, config.GREY, (health_bar_x, health_bar_y, self.health_bar_width, self.health_bar_height))
        # Foreground (current health)
        pygame.draw.rect(screen, config.RED, (health_bar_x, health_bar_y, self.health_bar_width * health_ratio, self.health_bar_height))

    def take_damage(self, damage):
        self.health = max(0, self.health - damage)

    def is_defeated(self):
        return self.health <= 0

    def get_next_word(self):
        if self.current_word_index < len(self.boss_words):
            self.current_word = self.boss_words[self.current_word_index]  # Store the current word
            self.current_word_index += 1
            return self.current_word
        else:
            self.current_word = None  # No more words, boss is defeated
            return None

class Boss4:
    def __init__(self, x, y, health, animation_speed=200, word_file="assets/csv/boss4.csv"):
        self.sprites = [
            pygame.image.load("assets/boss/Boss-stage4-1.png"),
            pygame.image.load("assets/boss/Boss-stage4-2.png"),
            pygame.image.load("assets/boss/Boss-stage4-3.png"),
            pygame.image.load("assets/boss/Boss-stage4-4.png"),
        ]
        
        self.sprite_width = self.sprites[0].get_width()  # Get sprite width
        self.sprite_height = self.sprites[0].get_height()  # Get sprite height

        self.x = (config.WIDTH - self.sprite_width) // 2  # Center x properly
        self.y = y  # Keep y as is

        self.health = health
        self.max_health = health
        self.boss_words = self.load_words(word_file)
        self.current_word_index = 0
        self.current_word = None

        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = animation_speed

        self.health_bar_width = 300
        self.health_bar_height = 20
        self.health_bar_offset = 50


    def load_words(self, word_file):
        words = []
        try:
            with open(word_file, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)  # Automatically handles commas as delimiters
                for row in reader:
                    for word in row:  # Split each row into individual words
                        cleaned_word = word.strip()  # Remove leading/trailing spaces
                        if cleaned_word:  # Skip empty words
                            words.append(cleaned_word)
        except FileNotFoundError:
            print(f"Error: {word_file} not found. Using default boss words.")
            words = ["bossword1", "bossword2", "bossword3"]  # Default words
        return words

    def update(self, delta_time):
        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.sprites)

    def draw(self, screen):
        # Draw the boss sprite
        sprite = self.sprites[self.current_frame]
        screen.blit(sprite, (self.x, self.y))

        # Draw the health bar
        health_ratio = self.health / self.max_health
        health_bar_x = self.x + (sprite.get_width() - self.health_bar_width) // 2
        health_bar_y = self.y - self.health_bar_offset

        # Background of the health bar
        pygame.draw.rect(screen, config.GREY, (health_bar_x, health_bar_y, self.health_bar_width, self.health_bar_height))
        # Foreground (current health)
        pygame.draw.rect(screen, config.RED, (health_bar_x, health_bar_y, self.health_bar_width * health_ratio, self.health_bar_height))

    def take_damage(self, damage):
        self.health = max(0, self.health - damage)

    def is_defeated(self):
        return self.health <= 0

    def get_next_word(self):
        if self.current_word_index < len(self.boss_words):
            self.current_word = self.boss_words[self.current_word_index]  # Store the current word
            self.current_word_index += 1
            return self.current_word
        else:
            self.current_word = None  # No more words, boss is defeated
            return None

class Boss5:
    def __init__(self, x, y, health, animation_speed=200, word_file="assets/csv/boss5.csv"):
        self.sprites = [
            pygame.image.load("assets/boss/Boss-stage5-1.png"),
            pygame.image.load("assets/boss/Boss-stage5-2.png"),
            pygame.image.load("assets/boss/Boss-stage5-3.png"),
            pygame.image.load("assets/boss/Boss-stage5-4.png"),
        ]
        
        self.sprite_width = self.sprites[0].get_width()  # Get sprite width
        self.sprite_height = self.sprites[0].get_height()  # Get sprite height

        self.x = (config.WIDTH - self.sprite_width) // 2  # Center x properly
        self.y = y  # Keep y as is

        self.health = health
        self.max_health = health
        self.boss_words = self.load_words(word_file)
        self.current_word_index = 0
        self.current_word = None

        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = animation_speed

        self.health_bar_width = 300
        self.health_bar_height = 20
        self.health_bar_offset = 50


    def load_words(self, word_file):
        words = []
        try:
            with open(word_file, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)  # Automatically handles commas as delimiters
                for row in reader:
                    for word in row:  # Split each row into individual words
                        cleaned_word = word.strip()  # Remove leading/trailing spaces
                        if cleaned_word:  # Skip empty words
                            words.append(cleaned_word)
        except FileNotFoundError:
            print(f"Error: {word_file} not found. Using default boss words.")
            words = ["bossword1", "bossword2", "bossword3"]  # Default words
        return words

    def update(self, delta_time):
        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.sprites)

    def draw(self, screen):
        # Draw the boss sprite
        sprite = self.sprites[self.current_frame]
        screen.blit(sprite, (self.x, self.y))

        # Draw the health bar
        health_ratio = self.health / self.max_health
        health_bar_x = self.x + (sprite.get_width() - self.health_bar_width) // 2
        health_bar_y = self.y - self.health_bar_offset

        # Background of the health bar
        pygame.draw.rect(screen, config.GREY, (health_bar_x, health_bar_y, self.health_bar_width, self.health_bar_height))
        # Foreground (current health)
        pygame.draw.rect(screen, config.RED, (health_bar_x, health_bar_y, self.health_bar_width * health_ratio, self.health_bar_height))

    def take_damage(self, damage):
        self.health = max(0, self.health - damage)

    def is_defeated(self):
        return self.health <= 0

    def get_next_word(self):
        if self.current_word_index < len(self.boss_words):
            self.current_word = self.boss_words[self.current_word_index]  # Store the current word
            self.current_word_index += 1
            return self.current_word
        else:
            self.current_word = None  # No more words, boss is defeated
            return None

class Boss6:
    def __init__(self, x, y, health, animation_speed=200, word_file="assets/csv/boss6.csv"):
        self.sprites = [
            pygame.image.load("assets/boss/Boss-stage6-1.png"),
            pygame.image.load("assets/boss/Boss-stage6-2.png"),
            pygame.image.load("assets/boss/Boss-stage6-3.png"),
            pygame.image.load("assets/boss/Boss-stage6-4.png"),
        ]
        
        self.sprite_width = self.sprites[0].get_width()  # Get sprite width
        self.sprite_height = self.sprites[0].get_height()  # Get sprite height

        self.x = (config.WIDTH - self.sprite_width) // 2  # Center x properly
        self.y = y  # Keep y as is

        self.health = health
        self.max_health = health
        self.boss_words = self.load_words(word_file)
        self.current_word_index = 0
        self.current_word = None

        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = animation_speed

        self.health_bar_width = 300
        self.health_bar_height = 20
        self.health_bar_offset = 50


    def load_words(self, word_file):
        words = []
        try:
            with open(word_file, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)  # Automatically handles commas as delimiters
                for row in reader:
                    for word in row:  # Split each row into individual words
                        cleaned_word = word.strip()  # Remove leading/trailing spaces
                        if cleaned_word:  # Skip empty words
                            words.append(cleaned_word)
        except FileNotFoundError:
            print(f"Error: {word_file} not found. Using default boss words.")
            words = ["bossword1", "bossword2", "bossword3"]  # Default words
        return words

    def update(self, delta_time):
        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.sprites)

    def draw(self, screen):
        # Draw the boss sprite
        sprite = self.sprites[self.current_frame]
        screen.blit(sprite, (self.x, self.y))

        # Draw the health bar
        health_ratio = self.health / self.max_health
        health_bar_x = self.x + (sprite.get_width() - self.health_bar_width) // 2
        health_bar_y = self.y - self.health_bar_offset

        # Background of the health bar
        pygame.draw.rect(screen, config.GREY, (health_bar_x, health_bar_y, self.health_bar_width, self.health_bar_height))
        # Foreground (current health)
        pygame.draw.rect(screen, config.RED, (health_bar_x, health_bar_y, self.health_bar_width * health_ratio, self.health_bar_height))

    def take_damage(self, damage):
        self.health = max(0, self.health - damage)

    def is_defeated(self):
        return self.health <= 0

    def get_next_word(self):
        if self.current_word_index < len(self.boss_words):
            self.current_word = self.boss_words[self.current_word_index]  # Store the current word
            self.current_word_index += 1
            return self.current_word
        else:
            self.current_word = None  # No more words, boss is defeated
            return None

class Boss7:
    def __init__(self, x, y, health, animation_speed=200, word_file="assets/csv/boss7.csv"):
        self.sprites = [
            pygame.image.load("assets/boss/Boss-stage7-1.png"),
            pygame.image.load("assets/boss/Boss-stage7-2.png"),
            pygame.image.load("assets/boss/Boss-stage7-3.png"),
            pygame.image.load("assets/boss/Boss-stage7-4.png"),
        ]
        
        self.sprite_width = self.sprites[0].get_width()  # Get sprite width
        self.sprite_height = self.sprites[0].get_height()  # Get sprite height

        self.x = (config.WIDTH - self.sprite_width) // 2  # Center x properly
        self.y = y  # Keep y as is

        self.health = health
        self.max_health = health
        self.boss_words = self.load_words(word_file)
        self.current_word_index = 0
        self.current_word = None

        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = animation_speed

        self.health_bar_width = 300
        self.health_bar_height = 20
        self.health_bar_offset = 50


    def load_words(self, word_file):
        words = []
        try:
            with open(word_file, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)  # Automatically handles commas as delimiters
                for row in reader:
                    for word in row:  # Split each row into individual words
                        cleaned_word = word.strip()  # Remove leading/trailing spaces
                        if cleaned_word:  # Skip empty words
                            words.append(cleaned_word)
        except FileNotFoundError:
            print(f"Error: {word_file} not found. Using default boss words.")
            words = ["bossword1", "bossword2", "bossword3"]  # Default words
        return words

    def update(self, delta_time):
        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.sprites)

    def draw(self, screen):
        # Draw the boss sprite
        sprite = self.sprites[self.current_frame]
        screen.blit(sprite, (self.x, self.y))

        # Draw the health bar
        health_ratio = self.health / self.max_health
        health_bar_x = self.x + (sprite.get_width() - self.health_bar_width) // 2
        health_bar_y = self.y - self.health_bar_offset

        # Background of the health bar
        pygame.draw.rect(screen, config.GREY, (health_bar_x, health_bar_y, self.health_bar_width, self.health_bar_height))
        # Foreground (current health)
        pygame.draw.rect(screen, config.RED, (health_bar_x, health_bar_y, self.health_bar_width * health_ratio, self.health_bar_height))

    def take_damage(self, damage):
        self.health = max(0, self.health - damage)

    def is_defeated(self):
        return self.health <= 0

    def get_next_word(self):
        if self.current_word_index < len(self.boss_words):
            self.current_word = self.boss_words[self.current_word_index]  # Store the current word
            self.current_word_index += 1
            return self.current_word
        else:
            self.current_word = None  # No more words, boss is defeated
            return None

class Boss8:
    def __init__(self, x, y, health, animation_speed=200, word_file="assets/csv/boss8.csv"):
        self.sprites = [
            pygame.image.load("assets/boss/Boss-stage8-1.png"),
            pygame.image.load("assets/boss/Boss-stage8-2.png"),
            pygame.image.load("assets/boss/Boss-stage8-3.png"),
            pygame.image.load("assets/boss/Boss-stage8-4.png"),
        ]
        
        self.sprite_width = self.sprites[0].get_width()  # Get sprite width
        self.sprite_height = self.sprites[0].get_height()  # Get sprite height

        self.x = (config.WIDTH - self.sprite_width) // 2  # Center x properly
        self.y = y  # Keep y as is

        self.health = health
        self.max_health = health
        self.boss_words = self.load_words(word_file)
        self.current_word_index = 0
        self.current_word = None

        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = animation_speed

        self.health_bar_width = 300
        self.health_bar_height = 20
        self.health_bar_offset = 50


    def load_words(self, word_file):
        words = []
        try:
            with open(word_file, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)  # Automatically handles commas as delimiters
                for row in reader:
                    for word in row:  # Split each row into individual words
                        cleaned_word = word.strip()  # Remove leading/trailing spaces
                        if cleaned_word:  # Skip empty words
                            words.append(cleaned_word)
        except FileNotFoundError:
            print(f"Error: {word_file} not found. Using default boss words.")
            words = ["bossword1", "bossword2", "bossword3"]  # Default words
        return words

    def update(self, delta_time):
        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.sprites)

    def draw(self, screen):
        # Draw the boss sprite
        sprite = self.sprites[self.current_frame]
        screen.blit(sprite, (self.x, self.y))

        # Draw the health bar
        health_ratio = self.health / self.max_health
        health_bar_x = self.x + (sprite.get_width() - self.health_bar_width) // 2
        health_bar_y = self.y - self.health_bar_offset

        # Background of the health bar
        pygame.draw.rect(screen, config.GREY, (health_bar_x, health_bar_y, self.health_bar_width, self.health_bar_height))
        # Foreground (current health)
        pygame.draw.rect(screen, config.RED, (health_bar_x, health_bar_y, self.health_bar_width * health_ratio, self.health_bar_height))

    def take_damage(self, damage):
        self.health = max(0, self.health - damage)

    def is_defeated(self):
        return self.health <= 0

    def get_next_word(self):
        if self.current_word_index < len(self.boss_words):
            self.current_word = self.boss_words[self.current_word_index]  # Store the current word
            self.current_word_index += 1
            return self.current_word
        else:
            self.current_word = None  # No more words, boss is defeated
            return None

class Boss9:
    def __init__(self, x, y, health, animation_speed=200, word_file="assets/csv/boss9.csv"):
        self.sprites = [
            pygame.image.load("assets/boss/Boss-stage9-1.png"),
            pygame.image.load("assets/boss/Boss-stage9-2.png"),
            pygame.image.load("assets/boss/Boss-stage9-3.png"),
            pygame.image.load("assets/boss/Boss-stage9-4.png"),
        ]
        
        self.sprite_width = self.sprites[0].get_width()  # Get sprite width
        self.sprite_height = self.sprites[0].get_height()  # Get sprite height

        self.x = (config.WIDTH - self.sprite_width) // 2  # Center x properly
        self.y = y  # Keep y as is

        self.health = health
        self.max_health = health
        self.boss_words = self.load_words(word_file)
        self.current_word_index = 0
        self.current_word = None

        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = animation_speed

        self.health_bar_width = 300
        self.health_bar_height = 20
        self.health_bar_offset = 50


    def load_words(self, word_file):
        words = []
        try:
            with open(word_file, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)  # Automatically handles commas as delimiters
                for row in reader:
                    for word in row:  # Split each row into individual words
                        cleaned_word = word.strip()  # Remove leading/trailing spaces
                        if cleaned_word:  # Skip empty words
                            words.append(cleaned_word)
        except FileNotFoundError:
            print(f"Error: {word_file} not found. Using default boss words.")
            words = ["bossword1", "bossword2", "bossword3"]  # Default words
        return words

    def update(self, delta_time):
        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.sprites)

    def draw(self, screen):
        # Draw the boss sprite
        sprite = self.sprites[self.current_frame]
        screen.blit(sprite, (self.x, self.y))

        # Draw the health bar
        health_ratio = self.health / self.max_health
        health_bar_x = self.x + (sprite.get_width() - self.health_bar_width) // 2
        health_bar_y = self.y - self.health_bar_offset

        # Background of the health bar
        pygame.draw.rect(screen, config.GREY, (health_bar_x, health_bar_y, self.health_bar_width, self.health_bar_height))
        # Foreground (current health)
        pygame.draw.rect(screen, config.RED, (health_bar_x, health_bar_y, self.health_bar_width * health_ratio, self.health_bar_height))

    def take_damage(self, damage):
        self.health = max(0, self.health - damage)

    def is_defeated(self):
        return self.health <= 0

    def get_next_word(self):
        if self.current_word_index < len(self.boss_words):
            self.current_word = self.boss_words[self.current_word_index]  # Store the current word
            self.current_word_index += 1
            return self.current_word
        else:
            self.current_word = None  # No more words, boss is defeated
            return None

class Boss10:
    def __init__(self, x, y, health, animation_speed=200, word_file="assets/csv/boss10.csv"):
        self.sprites = [
            pygame.image.load("assets/boss/Boss-stage10-1.png"),
            pygame.image.load("assets/boss/Boss-stage10-2.png"),
            pygame.image.load("assets/boss/Boss-stage10-3.png"),
            pygame.image.load("assets/boss/Boss-stage10-4.png"),
        ]
        
        self.sprite_width = self.sprites[0].get_width()  # Get sprite width
        self.sprite_height = self.sprites[0].get_height()  # Get sprite height

        self.x = (config.WIDTH - self.sprite_width) // 2  # Center x properly
        self.y = y  # Keep y as is

        self.health = health
        self.max_health = health
        self.boss_words = self.load_words(word_file)
        self.current_word_index = 0
        self.current_word = None

        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = animation_speed

        self.health_bar_width = 300
        self.health_bar_height = 20
        self.health_bar_offset = 50


    def load_words(self, word_file):
        words = []
        try:
            with open(word_file, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)  # Automatically handles commas as delimiters
                for row in reader:
                    for word in row:  # Split each row into individual words
                        cleaned_word = word.strip()  # Remove leading/trailing spaces
                        if cleaned_word:  # Skip empty words
                            words.append(cleaned_word)
        except FileNotFoundError:
            print(f"Error: {word_file} not found. Using default boss words.")
            words = ["bossword1", "bossword2", "bossword3"]  # Default words
        return words

    def update(self, delta_time):
        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.sprites)

    def draw(self, screen):
        # Draw the boss sprite
        sprite = self.sprites[self.current_frame]
        screen.blit(sprite, (self.x, self.y))

        # Draw the health bar
        health_ratio = self.health / self.max_health
        health_bar_x = self.x + (sprite.get_width() - self.health_bar_width) // 2
        health_bar_y = self.y - self.health_bar_offset

        # Background of the health bar
        pygame.draw.rect(screen, config.GREY, (health_bar_x, health_bar_y, self.health_bar_width, self.health_bar_height))
        # Foreground (current health)
        pygame.draw.rect(screen, config.RED, (health_bar_x, health_bar_y, self.health_bar_width * health_ratio, self.health_bar_height))

    def take_damage(self, damage):
        self.health = max(0, self.health - damage)

    def is_defeated(self):
        return self.health <= 0

    def get_next_word(self):
        if self.current_word_index < len(self.boss_words):
            self.current_word = self.boss_words[self.current_word_index]  # Store the current word
            self.current_word_index += 1
            return self.current_word
        else:
            self.current_word = None  # No more words, boss is defeated
            return None

