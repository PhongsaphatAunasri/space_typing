import pygame
import random
import config
from Spaceship import Spaceship
from FallingWord import FallingWordAdventure
from Boss import Boss
from pause import pause_game
import Particle

pygame.init()
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
font = config.FONT_MAIN

# Load resources
heart_image = pygame.image.load("assets/heart.png")
missile_image = pygame.image.load("assets/missile.png")

# Sound effects
loss_hp_sound = pygame.mixer.Sound("sounds/losshp.wav")
game_over_sound = pygame.mixer.Sound("sounds/gameover.wav")
correct_sound = pygame.mixer.Sound("sounds/correct.wav")
# bonus_sound = pygame.mixer.Sound("sounds/bonus.wav")

loss_hp_sound.set_volume(0.05)
game_over_sound.set_volume(0.05)
correct_sound.set_volume(0.05)
# bonus_sound.set_volume(0.05)

def draw_health(health, x, y):
    for i in range(health):
        screen.blit(heart_image, (x + i * (heart_image.get_width() + 10), y))

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

import pygame

def adventure_mode():
    player_health = 999
    player_score = 0
    clock = pygame.time.Clock()
    spaceship = Spaceship()
    player_word = ""

    # State variables
    state = 1
    state_timer = 0
    boss = Boss(x=config.WIDTH // 2 - 100, y=100, health=100)
    falling_words = []
    boss_health = 10  # Boss health for State 3
    remembered_words = []

    # State-specific counters
    correct_word_count = 0  # Tracks correct words in State 1
    wave_count = 0  # Tracks waves completed in State 2
    bonus_timer = 15 * 1000  # 15 seconds for State 4
    max_wave_count = 3  # Maximum waves before transitioning to state 3
    waves_completed = 0  # Track the waves completed in state 2

    running = True
    last_time = pygame.time.get_ticks()  # Initialize last_time to current time

    while running:
        screen.fill(config.BLACK)

        for particle in Particle.particles:
            particle.update()
            particle.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if pause_game() == "Main Menu":
                        running = False
                elif event.key == pygame.K_BACKSPACE:
                    player_word = player_word[:-1]
                elif event.key != pygame.K_SPACE:
                    player_word += event.unicode

        # Calculate delta_time
        current_time = pygame.time.get_ticks()  # Get the current time in milliseconds
        delta_time = current_time - last_time  # Calculate the time difference
        last_time = current_time  # Update last_time for the next frame

        # Handle states
        if state == 1:
            # Spawn new words periodically
            if len(falling_words) == 0 or (state_timer > 2000 and len(falling_words) < 3):
                falling_words.append(FallingWordAdventure(existing_words=[], speed=1 + random.random()))
                state_timer = 0

            # Process words
            for word in falling_words[:]:
                if player_word == word.word:
                    correct_sound.play()
                    player_score += len(word.word) * 1000
                    spaceship.shoot_missile(word, missile_image)
                    remembered_words.append(word.word)
                    player_word = ""
                    falling_words.remove(word)
                    correct_word_count += 1  # Increment correct word count

                word.update(player_health)
                word.draw(player_word)

                # Check if the word has reached the bottom of the screen
                if word.rect.y > config.HEIGHT:
                    # Remove the word from the falling_words list
                    falling_words.remove(word)

            # Transition to State 2 after 20 correct words
            if correct_word_count >= 3:
                state = 2
                falling_words = []
                state_timer = 0

        elif state == 2:
            # After the 3rd wave, stop generating new words
            if waves_completed < max_wave_count:
                # Spawn waves of words
                if state_timer < 3000 and len(falling_words) < 3:
                    for _ in range(random.randint(3, 3)):
                        falling_words.append(FallingWordAdventure(existing_words=[], speed=1 + random.random()))
                    wave_count += 1  # Increment wave count
                    waves_completed += 1
                    state_timer = 0
            else:
                # If the third wave is complete, stop generating new words
                if len(falling_words) == 0:
                    state = 3  # Transition to state 3 when no more words left
                    boss = Boss(x=config.WIDTH // 2 - 100, y=100, health=10)  # Initialize boss
                    state_timer = 0

            # Process words
            for word in falling_words[:]:
                if player_word == word.word:
                    correct_sound.play()
                    player_score += len(word.word) * 1000
                    spaceship.shoot_missile(word, missile_image)
                    remembered_words.append(word.word)
                    player_word = ""
                    falling_words.remove(word)

                word.update(player_health)
                word.draw(player_word)

                # Check if the word has reached the bottom of the screen
                if word.rect.y > config.HEIGHT:
                    # Remove the word from the falling_words list
                    falling_words.remove(word)

        elif state == 3:
            boss.draw(screen)  # Pass the screen to the draw method
            boss.update(delta_time)

            boss_word = "bossword"  # Example of boss word
            if player_word == boss_word:
                correct_sound.play()
                boss_health -= 1
                player_score += 2000
                player_word = ""
                if boss_health <= 0:
                    state = 4
                    state_timer = 0

            elif player_word:
                player_health -= 1
                loss_hp_sound.play()
                player_word = ""

            draw_health(player_health, 20, 20)

            if player_health <= 0:
                running = False

        elif state == 4:
            draw_text("Bonus Round!", font, config.YELLOW, config.WIDTH // 2, 50)

            for word in remembered_words:
                draw_text(word, font, config.WHITE, random.randint(50, config.WIDTH - 50), random.randint(100, config.HEIGHT - 100))

            bonus_timer -= clock.get_time()

            if bonus_timer <= 0:
                running = False  # End the game and proceed to score summary

        # Update and draw spaceship
        spaceship.update()
        spaceship.draw()

        # Draw score
        draw_text(f"Score: {player_score}", font, config.WHITE, config.WIDTH - 100, 20)

        pygame.display.flip()
        clock.tick(config.FPS)

    return player_score






adventure_mode()
