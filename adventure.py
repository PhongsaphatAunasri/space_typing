import pygame
import random
import sys
import config
import time
from Spaceship import Spaceship
from FallingWord import FallingWordAdventure
from Boss import Boss
from pause import pause_game
from Effect import Explosion
import Particle

pygame.init()
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
font = config.FONT_MAIN
font2 = config.FONT_SEMI_LARGE
font3 = config.FONT_Large
# Load resources
heart_image = pygame.image.load("assets/heart.png")
missile_image = pygame.image.load("assets/missile.png")

# Sound effects
loss_hp_sound = pygame.mixer.Sound("sounds/losshp.wav")
game_over_sound = pygame.mixer.Sound("sounds/gameover.wav")
correct_sound = pygame.mixer.Sound("sounds/correct.wav")
select_sound = pygame.mixer.Sound("sounds/select.wav")
# bonus_sound = pygame.mixer.Sound("sounds/bonus.wav")

loss_hp_sound.set_volume(0.05)
game_over_sound.set_volume(0.05)
correct_sound.set_volume(0.05)
select_sound.set_volume(0.05)
# bonus_sound.set_volume(0.05)

def draw_health(health, x, y):
    for i in range(health):
        screen.blit(heart_image, (x + i * (heart_image.get_width() + 10), y))

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


def game_over_menu_a(player_score):
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
                        return adventure_mode()  # Restart the game with initial health
                    elif current_selection == 1:  # Main Menu option
                        return "Main Menu"
                elif event.key == pygame.K_UP:
                    select_sound.play()
                    current_selection = (current_selection - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    select_sound.play()
                    current_selection = (current_selection + 1) % len(options)

def adventure_mode():
    player_health = 3
    player_score = 0
    clock = pygame.time.Clock()
    spaceship = Spaceship()
    player_word = ""

    # State variables
    state = 1
    state_timer = 0
    boss = Boss(x=config.WIDTH // 2 - 100, y=100, health=100)
    falling_words = []
    remembered_words = []

    # Boss health and waves
    boss_health = 10  
    correct_word_count = 0  
    wave_count = 0  
    max_wave_count = 3  
    waves_completed = 0  

    bonus_timer = 10 * 1000  # 40 seconds for State 4
    running = True
    last_time = pygame.time.get_ticks()

    # Effects
    explosions = []  # Stores explosion effects
    correct_word_positions = []  # Stores positions for laser lines

    while running:
        screen.fill(config.BLACK)

        # Update particles
        for particle in Particle.particles:
            particle.update()
            particle.draw()

        # Handle events
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

        # Handle words falling past the deadzone
        for word in falling_words[:]:
            if word.rect.y > config.DEADZONE_LINE:
                player_health -= 1
                loss_hp_sound.play()
                falling_words.remove(word)

        # Calculate delta_time
        current_time = pygame.time.get_ticks()
        delta_time = current_time - last_time
        last_time = current_time

        # Draw player health
        draw_health(player_health, 20, 20)

        # Handle game states
        if state == 1:
            draw_text(player_word, font, config.WHITE, config.WIDTH // 2, config.HEIGHT - 150)

            # Spawn words
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
                    explosions.append(Explosion(word.rect.centerx, word.rect.centery))

                    # Store correct word position for laser effect
                    correct_word_positions.append((spaceship.rect.center, word.rect.center))
                    
                    player_word = ""
                    falling_words.remove(word)
                    correct_word_count += 1

                word.update(player_health)
                word.draw(player_word)

            if correct_word_count >= 3:
                state = 2
                falling_words = []
                state_timer = 0

            if player_health <= 0:
                game_over_sound.play()
                running = False

        elif state == 2:
            draw_text(player_word, font, config.WHITE, config.WIDTH // 2, config.HEIGHT - 150)

            if waves_completed < max_wave_count:
                if state_timer < 3000 and len(falling_words) < 3:
                    for _ in range(3):
                        falling_words.append(FallingWordAdventure(existing_words=[], speed=1 + random.random()))
                    wave_count += 1
                    waves_completed += 1
                    state_timer = 0
            else:
                if len(falling_words) == 0:
                    state = 3
                    boss = Boss(x=config.WIDTH // 2.5 - 100, y=100, health=10, word_file="assets/word.csv")
                    state_timer = 0

            for word in falling_words[:]:
                if player_word == word.word:
                    correct_sound.play()
                    player_score += len(word.word) * 1000
                    spaceship.shoot_missile(word, missile_image)
                    remembered_words.append(word.word)
                    explosions.append(Explosion(word.rect.centerx, word.rect.centery))

                    # Store correct word position for laser effect
                    correct_word_positions.append((spaceship.rect.center, word.rect.center))

                    player_word = ""
                    falling_words.remove(word)

                word.update(player_health)
                word.draw(player_word)

            if player_health <= 0:
                game_over_sound.play()
                running = False

        elif state == 3:
            draw_text(player_word, font, config.WHITE, config.WIDTH // 2, config.HEIGHT - 150)

            # Draw and update the boss
            boss.draw(screen)
            boss.update(delta_time)

            # Boss word handling
            if not hasattr(boss, "current_word") or boss.current_word is None:
                boss.current_word = boss.get_next_word()

            if boss.current_word:
                draw_text(boss.current_word, font, config.WHITE, config.WIDTH // 2, config.HEIGHT // 2)

            # Player input check
            if player_word.strip() == boss.current_word:
                correct_sound.play()
                boss.take_damage(1)  
                player_score += 2000  
                player_word = ""  
                boss.current_word = boss.get_next_word()

                # Add explosion effect at boss position
                # explosions.append(Explosion(boss.rect.centerx, boss.rect.centery))

            # Check if boss is defeated
            if boss.is_defeated():
                state = 4  
                state_timer = 0

            if player_health <= 0:
                running = False

        elif state == 4:
            draw_text("Bonus Round!", font2, config.YELLOW, config.WIDTH // 2, 200)
            draw_text("Type the previously memorized words!", font2, config.YELLOW, config.WIDTH // 2, 280)
            
            draw_text(player_word, font3, config.CYAN, config.WIDTH // 2, config.HEIGHT - 400)

            remaining_time = max(0, bonus_timer // 1000)
            draw_text(f"Time Left: {remaining_time}", font, config.RED, config.WIDTH - 150, 100)

            if player_word in remembered_words:
                correct_sound.play()
                player_score += len(player_word) * 2000
                spaceship.shoot_missile(FallingWordAdventure(existing_words=[], speed=1 + random.random()), missile_image)
                remembered_words.remove(player_word)
                player_word = ""

            if remembered_words:
                draw_text("Remembered Words: " + ", ".join(remembered_words), font, config.WHITE, config.WIDTH // 2, config.HEIGHT - 100)

            bonus_timer -= delta_time

            if bonus_timer <= 0:
                running = False

        # Draw laser lines
        for start_pos, end_pos in correct_word_positions:
            pygame.draw.line(screen, config.WHITE, start_pos, end_pos, 10)

        # Clear laser effects after a short duration
        correct_word_positions.clear()

        # Update explosions
        for explosion in explosions[:]:
            explosion.update()
            explosion.draw(screen)
            if explosion.finished:
                explosions.remove(explosion)

        # Update and draw spaceship
        spaceship.update()
        spaceship.draw()

        # Draw score
        draw_text(f"Score: {player_score}", font, config.WHITE, config.WIDTH - 150, 20)

        pygame.display.flip()
        clock.tick(config.FPS)

    return game_over_menu_a(player_score)





adventure_mode()
