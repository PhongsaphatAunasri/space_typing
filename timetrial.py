import pygame
import sys
import config
import Particle
from FallingWord import FallingWordTimeTrial
from Spaceship import Spaceship

from pause import pause_game

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
font = config.FONT_MAIN
score = 0
#image
heart_image = pygame.image.load("assets/heart.png")
missile_image = pygame.image.load("assets/missile.png")

#sound
loss_hp_sound = pygame.mixer.Sound("sounds/losshp.wav")
game_over_sound = pygame.mixer.Sound("sounds/gameover.wav")
correct_sound = pygame.mixer.Sound("sounds/correct.wav")
select_sound = pygame.mixer.Sound("sounds/select.wav")
incorrect_sound = pygame.mixer.Sound("sounds/incorrect.wav")
#set volume
loss_hp_sound.set_volume(0.05)
game_over_sound.set_volume(0.05)
correct_sound.set_volume(0.05)
select_sound.set_volume(0.05)  # Adjust volume 
incorrect_sound.set_volume(0.05)
def draw_text(text, font, color, x, y, blink=False):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
        # Blinking effect for the specified text
    if blink and text == "Space Typing" and pygame.time.get_ticks() % 1000 < 500:
        screen.blit(text_surface, text_rect)
    elif not blink:
        screen.blit(text_surface, text_rect)
def game_over_menu_t(score):
    game_over_sound.play()
    options = ["Restart", "Main Menu"]
    current_selection = 0
    button_height = 60  # config.Height of each button
    spacing = 120  # Vertical spacing between buttons

    while True:
        # Draw everything
        screen.fill(config.BLACK)  # Fill the screen with the background color
        for particle in Particle.particles:
            particle.draw()
            particle.update()

        draw_text("Game Over", pygame.font.Font("assets/mania.ttf", 60), config.WHITE, config.WIDTH // 2, config.HEIGHT // 3)
        draw_text(f"Total Score : {score}", pygame.font.Font("assets/mania.ttf", 42), config.YELLOW, config.WIDTH // 2, config.HEIGHT // 2.15)

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
        pygame.time.Clock().tick(config.FPS)
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    select_sound.play()
                    if current_selection == 0:  # Restart option
                        return time_trial_mode(score)  # Restart the game
                    elif current_selection == 1:  # Main Menu option
                        return "Main Menu"
                elif event.key == pygame.K_UP:
                    select_sound.play()
                    current_selection = (current_selection - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    select_sound.play()
                    current_selection = (current_selection + 1) % len(options)                  
def time_trial_mode(score):
    player = Spaceship()
    falling_words = []
    player_word = ""
    score = 0
    game_time = 60
    start_ticks = None  # Timer starts as None
    paused_time_total = 0  # Track the total paused time
    word_positions = [(config.WIDTH // 2, 0)]
    generate_new_word = False  # Flag to indicate new word generation

    for position in word_positions:
        falling_words.append(FallingWordTimeTrial(position))

    running = True  # Initialize running
    paused = False  # Initialize paused state

    while running:
        screen.fill(config.BLACK)

        # Update and draw particles
        for particle in Particle.particles:
            particle.update()
            particle.draw()

        # Start the timer only when all initial words are frozen
        if all(word.frozen for word in falling_words) and start_ticks is None:
            start_ticks = pygame.time.get_ticks()

        # Calculate elapsed time if the timer has started
        if start_ticks is not None:
            seconds = (pygame.time.get_ticks() - start_ticks - paused_time_total) / 1000

        # Display the player's typed word
        draw_text(player_word, font, config.WHITE, config.WIDTH // 2, config.HEIGHT - 150)

        # Update and draw falling words
        for word in falling_words:
            word.draw(player_word)
            if word.rect.y >= player.rect.top and word.rect.y <= player.rect.bottom and \
                    word.rect.x >= player.rect.left and word.rect.x <= player.rect.right:
                if player_word == word.word:
                    player_word = ""
                    break
                else:
                    falling_words.remove(word)
                    player_word = ""

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused_duration = pause_game()
                    if paused_duration == "Main Menu":
                        running = False
                    else:
                        paused_time_total += paused_duration
                elif event.key == pygame.K_BACKSPACE:
                    player_word = player_word[:-1]
                elif event.key != pygame.K_SPACE:  
                    player_word += event.unicode
                # else:
                #     player_word += event.unicode

        # Automatically check if the typed word is correct
        correct_word = None
        for word in falling_words:
            if player_word == word.word:
                correct_word = word
                break

        if correct_word:
            correct_sound.play()
            missile_image = pygame.image.load("assets/missile.png")
            player.shoot_missile(correct_word, missile_image)
            player_word = ""
            score += 1
            generate_new_word = True  # Flag to generate a new word

        # Generate a new word if flagged
        if generate_new_word:
            falling_words.append(FallingWordTimeTrial((config.WIDTH // 2, 0)))
            generate_new_word = False

        # Update and draw missiles
        player.update_missiles(falling_words)
        player.draw_missiles()

        # Update falling words
        for word in falling_words[:]:
            word.update()

        # Draw score and timer
        draw_text("Score", font, config.WHITE, 65, 30)
        draw_text(f"{score}", font, config.WHITE, 60, 65)
        if start_ticks is not None:
            line_length = int((config.WIDTH * (game_time - seconds)) / game_time)
            pygame.draw.rect(screen, config.YELLOW, (line_length - config.WIDTH, 0, config.WIDTH, 10))

        # Update and draw the player
        player.update()
        player.draw()

        # End the game when time runs out
        if start_ticks is not None and seconds > game_time:
            game_over_sound.play()
            running = False

        # Refresh the screen
        pygame.display.flip()
        pygame.time.Clock().tick(config.FPS)

    # Game Over menu
    return game_over_menu_t(score)
  


# time_trial_mode(score)