import pygame
import sys
import time
import config
import Particle
from FallingWord import FallingWordTimeTrial
from Spaceship import Spaceship
from Effect import Explosion
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

def draw_text(text, font, color, x, y, blink=False):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
        # Blinking effect for the specified text
    if blink and text == "Space Typing" and pygame.time.get_ticks() % 1000 < 500:
        screen.blit(text_surface, text_rect)
    elif not blink:
        screen.blit(text_surface, text_rect)
def draw_text_top(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x  # Center horizontally
    text_rect.top = y  # Position from the top
    screen.blit(text_surface, text_rect)
def draw_text_left_aligned(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(topleft=(x, y))  # Align to the left
    screen.blit(text_surface, text_rect)
 # Grey bar with height 50px
 # Grey bar with height 50px
def draw_text_right_aligned(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(topright=(x, y))  # Align to the right
    screen.blit(text_surface, text_rect)    


def game_over_menu_1(score,elapsed_time):
    config.TIME_SONG.stop()
    config.GAMEOVER.play()
    options = ["Restart", "Main Menu"]
    current_selection = 0
    button_height = 60  # config.Height of each button
    spacing = 120  # Vertical spacing between buttons
    start_time = time.time()  # Get the current absolute time
    # elapsed_time = game_time - (time.time() - start_time)  # Remaining time
    
    score_display = 1
    start_time = time.time()

    while True:
        # Draw everything
        screen.fill(config.BLACK)  # Fill the screen with the background color
        for particle in Particle.particles:
            particle.draw()
            particle.update()

        draw_text("Game Over", config.FONT_TITLE, config.WHITE, config.WIDTH // 2, config.HEIGHT // 3)
        draw_text("Total Score", config.FONT_SEMI_LARGE, config.YELLOW, config.WIDTH // 2, config.HEIGHT // 2.15)
        if elapsed_time < 60:  # If the player quits before time runs out
            draw_text("Failed", config.FONT_SEMI_LARGE, config.RED, config.WIDTH // 2, config.HEIGHT // 1.75)
        else:  # If time ran out, show the score
            draw_text(f"{score:,}", config.NUM_SEMI_LARGE, config.YELLOW, config.WIDTH // 2, config.HEIGHT // 1.75)
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
        pygame.time.Clock().tick(config.FPS)
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    config.SELECT.play()
                    if current_selection == 0:  # Restart option
                        pygame.mixer.stop()
                        config.TIME_SONG.play(-1)
                        return time_attack(score)  # Restart the game
                    elif current_selection == 1:  # Main Menu option
                        return "Main Menu"
                elif event.key == pygame.K_UP:
                    config.PRESS.play()
                    current_selection = (current_selection - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    config.PRESS.play()
                    current_selection = (current_selection + 1) % len(options) 
def game_over_menu_2(formatted_time, score, target_words):
    config.TIME_SONG.stop()
    config.GAMEOVER.play()
    options = ["Restart", "Main Menu"]
    current_selection = 0
    button_height = 60  # config.Height of each button
    spacing = 120  # Vertical spacing between buttons
    start_ticks = None
    score_display = 1
    start_time = time.time()
    paused_time_total = 0 

    while True:
        # Draw everything
        screen.fill(config.BLACK)  # Fill the screen with the background color
        for particle in Particle.particles:
            particle.draw()
            particle.update()

        draw_text("Game Over", config.FONT_TITLE, config.WHITE, config.WIDTH // 2, config.HEIGHT // 3)
        draw_text("Time Result", config.FONT_SEMI_LARGE, config.YELLOW, config.WIDTH // 2, config.HEIGHT // 2.15)
        if start_ticks is not None:
            elapsed_time = (pygame.time.get_ticks() - start_ticks - paused_time_total) / 1000
        else:
            elapsed_time = 0  # Default value before the timer starts

        if score < target_words:  # If player quits before finishing 100 words
            draw_text("Failed", config.FONT_SEMI_LARGE, config.RED, config.WIDTH // 2, config.HEIGHT // 1.75)
        else:
            draw_text(f"{formatted_time}", config.NUM_SEMI_LARGE, config.YELLOW, config.WIDTH // 2, config.HEIGHT // 1.75)

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
        pygame.time.Clock().tick(config.FPS)
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    config.SELECT.play()
                    if current_selection == 0:  # Restart option
                        pygame.mixer.stop()
                        config.TIME_SONG.play(-1)
                        return blitz(score)  # Restart the game
                    elif current_selection == 1:  # Main Menu option
                        config.TIME_SONG.stop()
                        return "Main Menu"
                elif event.key == pygame.K_UP:
                    config.PRESS.play()
                    current_selection = (current_selection - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    config.PRESS.play()
                    current_selection = (current_selection + 1) % len(options)                  
def time_attack(score):
    player = Spaceship()
    falling_words = []
    player_word = ""
    score = 0
    game_time = 60
    start_ticks = None  # Timer starts as None
    paused_time_total = 0  # Track the total paused time
    word_positions = [(config.WIDTH // 2, 0)]
    generate_new_word = False  # Flag to indicate new word generation
    lasers = []
    explosions = []
    ############################ Trapezoid ####################################
    top_width = 240  # Width of the top side
    bottom_width = 200  # Width of the bottom side
    height = 60  # Height of the trapezoid
    x_center = config.WIDTH // 2  # Center X position
    y_top = 0  # Distance from the top of the bar
    trapezoid_points = [
        (x_center - top_width // 2, y_top),  # Top-left
        (x_center + top_width // 2, y_top),  # Top-right
        (x_center + bottom_width // 2, y_top + height),  # Bottom-right
        (x_center - bottom_width // 2, y_top + height)  # Bottom-left
    ]
    ############################ Trapezoid ####################################

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
        # draw_text(player_word, font, config.WHITE, config.WIDTH // 2, config.HEIGHT - 150)

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
                config.PRESS.play()
                if event.key == pygame.K_ESCAPE:
                    paused_duration = pause_game()
                    
                    if paused_duration == "Main Menu":
                        config.TIME_SONG.stop()
                        running = False
                    else:
                        paused_time_total += paused_duration
                elif event.key == pygame.K_BACKSPACE:
                    player_word = player_word[:-1]
                elif event.key != pygame.K_SPACE:
                    all_falling_words = [word.word for word in falling_words]
                    
                    if player_word == "":  # If no word is started, only allow first letters of falling words
                        valid_first_letters = {word[0] for word in all_falling_words}  # Get all unique first letters
                        if event.unicode in valid_first_letters:
                            player_word += event.unicode  # Allow only valid first letters
                        else:
                            config.INCORRECT.play()
                    else:
                        # Find words that match current player_word as a prefix
                        possible_words = [word for word in all_falling_words if word.startswith(player_word)]
                        
                        if possible_words:  # If there are valid words
                            next_letter_index = len(player_word)

                            # Get all possible next letters
                            valid_next_letters = {word[next_letter_index] for word in possible_words if next_letter_index < len(word)}

                            if event.unicode in valid_next_letters:  # Allow only valid next letters
                                player_word += event.unicode
                            else:
                                config.INCORRECT.play()
                        else:
                            pass  # Ignore incorrect input

                    # Automatically check if the typed word is correct
                    correct_word = None
                    for word in falling_words:
                        if player_word == word.word:
                            correct_word = word
                            break

                    if correct_word:
                        config.LASER.play()
                        # missile_image = pygame.image.load("assets/missile.png")
                        # player.shoot_missile(correct_word, missile_image)
                        
                        score += 1
                        lasers.append((player.rect.centerx, player.rect.top, correct_word.rect.centerx, correct_word.rect.centery))
                        config.BOOM.play()
                        explosions.append(Explosion(correct_word.rect.centerx, correct_word.rect.centery))
                        falling_words.remove(correct_word)
                        player_word = ""
                        generate_new_word = True  # Flag to generate a new word

        # Generate a new word if flagged
        if generate_new_word:
            falling_words.append(FallingWordTimeTrial((config.WIDTH // 2, 0)))
            generate_new_word = False
        for laser in lasers:
            pygame.draw.line(screen, config.CYAN, (laser[0], laser[1]), (laser[2], laser[3]), 20)
            pygame.draw.line(screen, config.WHITE, (laser[0], laser[1]), (laser[2], laser[3]), 10)
            pygame.draw.circle(screen, config.CYAN,(laser[0], laser[1]), 20)
            pygame.draw.circle(screen, config.WHITE,(laser[0], laser[1]), 10)
        lasers.clear()
        for explosion in explosions[:]:
            explosion.update()
            
            explosion.draw(screen)
            if explosion.finished:
                explosions.remove(explosion)
        # Update and draw missiles
        player.update_missiles(falling_words)
        player.draw_missiles()

        # Update falling words
        for word in falling_words[:]:
            word.update()

        # Draw score and timer
        pygame.draw.rect(screen, config.LIGHTGREY, (0, 0, config.WIDTH, 81))
        pygame.draw.rect(screen, config.GREY, (0, 0, config.WIDTH, 77)) 
        pygame.draw.rect(screen, config.LIGHTGREY, (0, 0, config.WIDTH, 54)) 

        pygame.draw.rect(screen, config.DARKGREY, (0, 0, config.WIDTH, 50)) 
        # draw_text_left_aligned(f"Score :", font, config.WHITE, 5, 0)
        pygame.draw.rect(screen, config.GREY, (0, 54, config.WIDTH, 15))
        if start_ticks is not None:
            line_length = int((config.WIDTH * (game_time - seconds)) / game_time)
            pygame.draw.rect(screen, config.LIGHTYELLOW, (line_length - config.WIDTH, 58, config.WIDTH, 15))
        pygame.draw.polygon(screen, config.GREY, trapezoid_points)
        # pygame.draw.polygon(screen, config.DARKGREY, trapezoid_points,10)  # Change color as needed
        
        pygame.draw.lines(screen, config.DARKYELLOW, False, [  # False = not a closed shape
            trapezoid_points[0],  # Top-left
            trapezoid_points[3],  # Bottom-left
            trapezoid_points[2],  # Bottom-right
            trapezoid_points[1]   # Top-right (skipping the last connection)
        ], 5) 
        

        # draw_text_left_aligned(f"{score:,}", font, config.LIGHTYELLOW, config.WIDTH // 11, 0)
        draw_text_top(f"{score:,}", config.NUM_DIS, config.LIGHTYELLOW, config.WIDTH // 2,10)
        

        # Update and draw the player
        player.update()
        player.draw()

        # End the game when time runs out
        if start_ticks is not None and seconds > game_time:
            config.GAMEOVER.play()
            running = False

        # Refresh the screen
        pygame.display.flip()
        pygame.time.Clock().tick(config.FPS)

    # Game Over menu
    return game_over_menu_1(score, seconds)

def blitz(score):
    correct_word = 0
    player = Spaceship()
    falling_words = []
    player_word = ""
    score = 0
    target_words = 100 # Player must type 100 words
    start_ticks = None  # Timer starts as None
    paused_time_total = 0  # Track the total paused time
    word_positions = [(config.WIDTH // 2, 0)]
    generate_new_word = False
    lasers = []
    explosions = []
    
    
    for position in word_positions:
        falling_words.append(FallingWordTimeTrial(position))

    running = True
    paused = False

    while running:
        screen.fill(config.BLACK)

        for particle in Particle.particles:
            particle.update()
            particle.draw()

        if all(word.frozen for word in falling_words) and start_ticks is None:
            start_ticks = pygame.time.get_ticks()

        if start_ticks is not None:
            elapsed_time = (pygame.time.get_ticks() - start_ticks - paused_time_total) / 1000
        else:
            elapsed_time = 0  # Default value before the timer starts

        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        formatted_time = f"{minutes}:{seconds:02d}"

        for word in falling_words:
            word.draw(player_word)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                config.PRESS.play()
                if event.key == pygame.K_ESCAPE:
                    paused_duration = pause_game()
                    
                    if paused_duration == "Main Menu":
                        config.TIME_SONG.stop()
                        running = False
                    else:
                        paused_time_total += paused_duration
                elif event.key == pygame.K_BACKSPACE:
                    player_word = player_word[:-1]
                elif event.key != pygame.K_SPACE:
                    all_falling_words = [word.word for word in falling_words]
                    
                    if player_word == "":
                        valid_first_letters = {word[0] for word in all_falling_words}
                        if event.unicode in valid_first_letters:
                            player_word += event.unicode
                        else:
                            config.INCORRECT.play()
                    else:
                        possible_words = [word for word in all_falling_words if word.startswith(player_word)]
                        
                        if possible_words:
                            next_letter_index = len(player_word)
                            valid_next_letters = {word[next_letter_index] for word in possible_words if next_letter_index < len(word)}

                            if event.unicode in valid_next_letters:
                                player_word += event.unicode
                            else:
                                config.INCORRECT.play()

                    correct_word = None
                    for word in falling_words:
                        if player_word == word.word:
                            correct_word = word
                            break

                    if correct_word:
                        config.LASER.play()
                        score += 1
                        lasers.append((player.rect.centerx, player.rect.top, correct_word.rect.centerx, correct_word.rect.centery))
                        config.BOOM.play()
                        explosions.append(Explosion(correct_word.rect.centerx, correct_word.rect.centery))
                        falling_words.remove(correct_word)
                        player_word = ""
                        generate_new_word = True

        if generate_new_word:
            falling_words.append(FallingWordTimeTrial((config.WIDTH // 2, 0)))
            generate_new_word = False
        
        for laser in lasers:
            pygame.draw.line(screen, config.CYAN, (laser[0], laser[1]), (laser[2], laser[3]), 20)
            pygame.draw.line(screen, config.WHITE, (laser[0], laser[1]), (laser[2], laser[3]), 10)
            pygame.draw.circle(screen, config.CYAN,(laser[0], laser[1]), 20)
            pygame.draw.circle(screen, config.WHITE,(laser[0], laser[1]), 10)
        lasers.clear()

        for explosion in explosions[:]:
            explosion.update()
            explosion.draw(screen)
            if explosion.finished:
                explosions.remove(explosion)

        player.update_missiles(falling_words)
        player.draw_missiles()

        for word in falling_words[:]:
            word.update()

        pygame.draw.rect(screen, config.DARKGREY, (0, 0, config.WIDTH, 50))
        pygame.draw.circle(screen, config.YELLOW, (config.WIDTH , 0), 180)
        pygame.draw.circle(screen, config.GREY, (config.WIDTH , 0), 170)
        pygame.draw.circle(screen, config.YELLOW, (0 , 0), 180)
        pygame.draw.circle(screen, config.GREY, (0 , 0), 170)
        
        remaining_words = target_words - score
        draw_text_top(f"{remaining_words}", config.NUM_SEMI_LARGE, config.LIGHTYELLOW, 70, 45)
        draw_text_top(f"{formatted_time}", config.NUM_MAIN, config.LIGHTYELLOW, (config.WIDTH - 75), 50)

        player.update()
        player.draw()

        if score >= target_words:
            config.GAMEOVER.play()
            running = False

        pygame.display.flip()
        pygame.time.Clock().tick(config.FPS)

    return game_over_menu_2(formatted_time, score, target_words)





# time_attack(score)# 
# blitz(score)