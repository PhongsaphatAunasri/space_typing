import pygame
import csv
import config
class Boss:
    def __init__(self, x, y, health, animation_speed=200, word_file="assets/word.csv"):
        """
        Initializes the Boss object.

        Args:
            x (int): The x-coordinate of the boss.
            y (int): The y-coordinate of the boss.
            health (int): The boss's total health.
            animation_speed (int): Time in milliseconds for each sprite frame.
            word_file (str): Path to the CSV file containing boss words.
        """
        self.x = config.WIDTH // 2.4
        self.y = y
        self.health = health
        self.max_health = health
        self.boss_words = self.load_words(word_file)  # Load words from CSV
        self.current_word_index = 0
        # Load boss sprites
        self.sprites = [
            pygame.image.load("assets/boss/Boss-stage1-1.png"),
            pygame.image.load("assets/boss/Boss-stage1-2.png"),
            pygame.image.load("assets/boss/Boss-stage1-3.png"),
            pygame.image.load("assets/boss/Boss-stage1-4.png"),
        ]
        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = animation_speed  # Milliseconds per frame

        # Health bar dimensions
        self.health_bar_width = 300
        self.health_bar_height = 20
        self.health_bar_offset = 10  # Offset above the boss sprite

    def load_words(self, word_file):
        """
        Loads words from a CSV file.

        Args:
            word_file (str): Path to the CSV file.

        Returns:
            list: A list of words loaded from the file.
        """
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
        """
        Updates the boss's animation.

        Args:
            delta_time (int): Time elapsed since the last frame in milliseconds.
        """
        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % len(self.sprites)

    def draw(self, screen):
        """
        Draws the boss and its health bar.

        Args:
            screen (pygame.Surface): The game screen to draw on.
        """
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
        """
        Reduces the boss's health.

        Args:
            damage (int): The amount of damage to inflict on the boss.
        """
        self.health = max(0, self.health - damage)

    def is_defeated(self):
        """
        Checks if the boss is defeated.

        Returns:
            bool: True if the boss's health is 0, False otherwise.
        """
        return self.health <= 0

    def get_next_word(self):
        """
        Returns the next word that the player needs to type for the boss.
        """
        if self.current_word_index < len(self.boss_words):
            word = self.boss_words[self.current_word_index]
            self.current_word_index += 1
            return word
        else:
            return None  # No more words, boss is defeated
