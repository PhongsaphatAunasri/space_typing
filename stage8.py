import pygame
import random
import sys
import config
import time
from Spaceship import Spaceship
from FallingWord import FallingWordAdventure
from FallingWord import Stage8
from Boss import Boss8
from pause import pause_game
from Effect import Explosion
import Particle

pygame.init()
screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
font = config.FONT_MAIN
font2 = config.FONT_SEMI_LARGE
font3 = config.FONT_LARGE
# Load resources
heart_image = pygame.image.load("assets/heart.png")
missile_image = pygame.image.load("assets/missile.png")
bonus_box = pygame.image.load("assets/bonus-box-big.png")

# Sound effects
loss_hp_sound = pygame.mixer.Sound("sounds/losshp.wav")
game_over_sound = pygame.mixer.Sound("sounds/gameover.wav")
correct_sound = pygame.mixer.Sound("sounds/correct.wav")
select_sound = pygame.mixer.Sound("sounds/select.wav")
boom_sound = pygame.mixer.Sound("sounds/boom.wav")
laser_sound = pygame.mixer.Sound("sounds/laser.wav")
press_sound = pygame.mixer.Sound("sounds/press.wav")
incorrect_sound = pygame.mixer.Sound("sounds/incorrect.wav")
#set volume
loss_hp_sound.set_volume(0.2)
game_over_sound.set_volume(0.2)
correct_sound.set_volume(0.05)
select_sound.set_volume(0.2)  
boom_sound.set_volume(0.05)
laser_sound.set_volume(0.2)
press_sound.set_volume(0.2) 
incorrect_sound.set_volume(0.1)
player_health = 3
def draw_health(health, x, y):
    for i in range(health):
        screen.blit(heart_image, (x + (player_health - 1 - i) * (heart_image.get_width() + 10), y))

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
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
def is_overlapping(new_rect, existing_rects, min_distance=50):
    for rect in existing_rects:
        if new_rect.colliderect(rect.inflate(min_distance, min_distance)):
            return True
    return False
def game_over_menu(player_score):
    clock = pygame.time.Clock()
    running = True
    game_over_sound.play()
    options = ["Restart", "Next Stage","Main Menu"]
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

        draw_text("Stage 8", pygame.font.Font("assets/Prototype.ttf", 100), config.WHITE, config.WIDTH // 2, config.HEIGHT // 3)
        draw_text("Total Score", pygame.font.Font("assets/Prototype.ttf", 60), config.YELLOW, config.WIDTH // 2, config.HEIGHT // 2.15)
        if time.time() - start_time >= score_display:
            draw_text(f"{player_score:,}", config.NUM_MAIN, config.YELLOW, config.WIDTH // 2, config.HEIGHT // 1.75)

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
                        return adventure_s8()  # Restart the game with initial health
                    elif current_selection == 1:  
                        return "Stage 9"
                    elif current_selection == 2:  # Main Menu option
                        return "Main Menu"
                elif event.key == pygame.K_UP:
                    press_sound.play()
                    current_selection = (current_selection - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    press_sound.play()
                    current_selection = (current_selection + 1) % len(options)

def adventure_s8():
    player_health = 3
    player_score = 0
    clock = pygame.time.Clock()
    spaceship = Spaceship()
    player_word = ""

    # State variables
    state = 1
    state_timer = 0
    boss = Boss8(x=config.WIDTH // 2 - 100, y=100, health=100)
    falling_words = []
    remembered_words = []

    # Boss health and waves
    boss_health = 20  
    correct_word_count = 0  
    wave_count = 0  
    max_wave_count = 4 
    waves_completed = 0  
    boss_word_timer = 0
    bonus_timer = 15 * 1000  # 40 seconds for State 4
    running = True
    last_time = pygame.time.get_ticks()
    
    bar_width = 200  # Full width of the bar
    bar_height = 5 # Bar height
    bar_x = config.WIDTH // 2 - bar_width // 2  # Center the bar
    bar_y = config.HEIGHT // 2 + 40  # Position below the word


    # Effects
    explosions = []  # Stores explosion effects

    correct_word_positions = []  # Stores positions for laser lines
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
    ##########################################################################

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
                press_sound.play()
                if event.key == pygame.K_ESCAPE:
                    if pause_game() == "Main Menu":
                        running = False
                elif event.type == pygame.KEYDOWN and state == 3:
                    if event.key == pygame.K_BACKSPACE:
                        player_word = player_word[:-1]
                    elif player_word == "":  # If no word is started, only allow first letter of the boss word
                        if event.unicode == boss.current_word[0]:  # Check first letter
                            player_word += event.unicode  # Allow only valid first letter
                        else:
                            incorrect_sound.play()
                    else:
                        # Ensure we have a word to compare with
                        if boss.current_word.startswith(player_word):  
                            next_letter_index = len(player_word)
                            
                            if next_letter_index < len(boss.current_word):  # Prevent index out of range
                                next_letter = boss.current_word[next_letter_index]
                                if event.unicode == next_letter:  # Allow only valid next letter
                                    player_word += event.unicode
                                else:
                                    incorrect_sound.play()
                        else:
                            incorrect_sound.play()

                        
                        
                elif event.type == pygame.KEYDOWN and state == 4:
                    if event.key == pygame.K_BACKSPACE:
                        player_word = player_word[:-1]
                    elif event.key != pygame.K_SPACE:
                        all_falling_words = random_words
                                        
                        if player_word == "":  # If no word is started, only allow first letters of falling words
                            valid_first_letters = {word[0] for word in all_falling_words}  # Get all unique first letters
                            if event.unicode in valid_first_letters:
                                player_word += event.unicode  # Allow only valid first letters
                            else:
                                incorrect_sound.play()
                        else:
                            # Find words that match current player_word as a prefix
                            possible_words = [word for word in all_falling_words if word.startswith(player_word)]
                                        
                            if possible_words:  # If there are valid words
                                next_letter_index = len(player_word)  # Get the index for the next letter to type
                                valid_next_letters = {word[next_letter_index] for word in possible_words if next_letter_index < len(word)}

                                if event.unicode in valid_next_letters:  # Allow only valid next letters
                                    player_word += event.unicode
                                else:
                                    incorrect_sound.play()
                            else:
                                pass  # Ignore incorrect input
                            
                
                elif event.key == pygame.K_BACKSPACE:
                    player_word = player_word[:-1]
                elif event.key != pygame.K_SPACE:
                    all_falling_words = [word.word for word in (falling_words)]
                        
                    if player_word == "":  # If no word is started, only allow first letters of falling words
                        valid_first_letters = {word[0] for word in all_falling_words}  # Get all unique first letters
                        if event.unicode in valid_first_letters:
                            player_word += event.unicode  # Allow only valid first letters
                        else:
                            incorrect_sound.play()
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
                                incorrect_sound.play()
                        else:
                            pass  # Ignore incorrect input

        # Handle words falling past the deadzone
        for word in falling_words[:]:
            if word.rect.y > config.DEADZONE_LINE:
                player_health -= 1
                loss_hp_sound.play()
                falling_words.remove(word)

                # Clear player's input if it matches the removed word
                if player_word and word.word.startswith(player_word):
                    player_word = ""


        # Calculate delta_time
        current_time = pygame.time.get_ticks()
        delta_time = current_time - last_time
        last_time = current_time

        # Draw player health
        draw_health(player_health, 20, 20)

        #---------------------------- state 1 -----------------------------#
        if state == 1:
            
            pygame.draw.rect(screen, config.WHITE, (0, 0, config.WIDTH, 54)) 
            pygame.draw.rect(screen, config.DARKGREY, (0, 0, config.WIDTH, 50)) 
            pygame.draw.polygon(screen, config.GREY, trapezoid_points)
            # pygame.draw.polygon(screen, config.DARKGREY, trapezoid_points,10)  # Change color as needed
            pygame.draw.lines(screen, config.WHITE, False, [  # False = not a closed shape
                trapezoid_points[0],  # Top-left
                trapezoid_points[3],  # Bottom-left
                trapezoid_points[2],  # Bottom-right
                trapezoid_points[1]   # Top-right (skipping the last connection)
            ], 5) 
            spaceship.update()
            spaceship.draw()
            # draw_text(player_word, font, config.WHITE, config.WIDTH // 2, config.HEIGHT - 150)
            # state = 3
            # Spawn words
            if len(falling_words) == 0 or (state_timer > 2000 and len(falling_words) < 3):
                falling_words.append(Stage8(existing_words=[], speed=1 + random.random()))
                state_timer = 0

            # Process words
            for word in falling_words[:]:
                if player_word == word.word:
                    laser_sound.play()
                    player_score += len(word.word) * 100
                    spaceship.shoot_missile(word, missile_image)
                    remembered_words.append(word.word)
                    boom_sound.play()
                    explosions.append(Explosion(word.rect.centerx, word.rect.centery))

                    # Store correct word position for laser effect
                    correct_word_positions.append((spaceship.rect.center, word.rect.center))
                    
                    player_word = ""
                    falling_words.remove(word)
                    correct_word_count += 1

                word.update(player_health)
                word.draw(player_word)

            if correct_word_count >= 15:
                state = 2
                falling_words = []
                state_timer = 0

            if player_health <= 0:
                game_over_sound.play()
                running = False
            pygame.draw.rect(screen, config.WHITE, (0, 0, config.WIDTH, 54)) 
            pygame.draw.rect(screen, config.DARKGREY, (0, 0, config.WIDTH, 50)) 
            draw_text_left_aligned(f"Score :", font, config.WHITE, 5, 0)
            pygame.draw.polygon(screen, config.GREY, trapezoid_points)
            # pygame.draw.polygon(screen, config.DARKGREY, trapezoid_points,10)  # Change color as needed
            pygame.draw.lines(screen, config.WHITE, False, [  # False = not a closed shape
                trapezoid_points[0],  # Top-left
                trapezoid_points[3],  # Bottom-left
                trapezoid_points[2],  # Bottom-right
                trapezoid_points[1]   # Top-right (skipping the last connection)
            ], 5) 
            draw_text_top(player_word, config.FONT_DIS, config.CYAN, config.WIDTH // 2, 0)
        #---------------------------- state 2 -----------------------------#
        elif state == 2:
            
            # draw_text(player_word, font, config.WHITE, config.WIDTH // 2, config.HEIGHT - 150)
            spaceship.update()
            spaceship.draw()
            if waves_completed < max_wave_count:
                if state_timer < 3000 and len(falling_words) < 1:
                    for _ in range(3):
                        falling_words.append(Stage8(existing_words=[], speed=0.5 + random.random()))
                    wave_count += 1
                    waves_completed += 1
                    state_timer = 0
            else:
                if len(falling_words) == 0:
                    state = 3
                    boss = Boss8(x=config.WIDTH // 2 , y=config.HEIGHT // 4 , health=boss_health, word_file="assets/csv/boss8.csv")
                    state_timer = 0

            for word in falling_words[:]:
                if player_word == word.word:
                    laser_sound.play()
                    player_score += len(word.word) * 1000
                    spaceship.shoot_missile(word, missile_image)
                    remembered_words.append(word.word)
                    boom_sound.play()
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
            pygame.draw.rect(screen, config.WHITE, (0, 0, config.WIDTH, 54)) 
            pygame.draw.rect(screen, config.DARKGREY, (0, 0, config.WIDTH, 50)) 
            draw_text_left_aligned(f"Score :", font, config.WHITE, 5, 0)
            pygame.draw.polygon(screen, config.GREY, trapezoid_points)
            # pygame.draw.polygon(screen, config.DARKGREY, trapezoid_points,10)  # Change color as needed
            pygame.draw.lines(screen, config.WHITE, False, [  # False = not a closed shape
                trapezoid_points[0],  # Top-left
                trapezoid_points[3],  # Bottom-left
                trapezoid_points[2],  # Bottom-right
                trapezoid_points[1]   # Top-right (skipping the last connection)
            ], 5) 
            
            draw_text_top(player_word, config.FONT_DIS, config.CYAN, config.WIDTH // 2, 0)
        #---------------------------- state 3 -----------------------------#
        elif state == 3:
            
            # state = 4
            # draw_text(player_word, font, config.WHITE, config.WIDTH // 2, config.HEIGHT - 150)
            spaceship.update()
            spaceship.draw()
            # Draw and update the boss
            boss.draw(screen)
            boss.update(delta_time)
            
            # Boss word handling
            if not hasattr(boss, "current_word") or boss.current_word is None:
                boss.current_word = boss.get_next_word()

            if boss.current_word:
                correct_part = player_word  # The part typed correctly
                remaining_part = boss.current_word[len(player_word):]  # The remaining part of the word

                # Render both parts
                correct_surface = font.render(correct_part, True, config.YELLOW)
                remaining_surface = font.render(remaining_part, True, config.DARKRED)

                # Combine the total word width for centering
                total_width = correct_surface.get_width() + remaining_surface.get_width()
                text_x = (config.WIDTH - total_width) // 2  # Center the combined text

                text_y = config.HEIGHT // 2 - 90 # Keep Y position unchanged

                # Draw both parts with correct positioning
                screen.blit(correct_surface, (text_x, text_y))  # Draw correct part
                screen.blit(remaining_surface, (text_x + correct_surface.get_width(), text_y))  # Draw remaining part
                
                if boss_word_timer == 0:  # Start the timer when a new word appears
                    boss_word_timer = pygame.time.get_ticks()

                elapsed_time = pygame.time.get_ticks() - boss_word_timer
                remaining_time = max(0, 5000 - elapsed_time)  # Ensure it doesn't go negative

                # Calculate bar width based on remaining time
                current_bar_width = int((remaining_time / 5000) * bar_width)

                # Draw background bar (empty part)
                pygame.draw.rect(screen, config.DARKGREY, (bar_x, bar_y, bar_width, bar_height))

                # Draw progress bar (time left)
                pygame.draw.rect(screen, config.WHITE, (bar_x, bar_y, current_bar_width, bar_height))

                # If 3 seconds pass and word is not typed, decrease health
                if elapsed_time > 5000:
                    # spaceship.update()
                    # spaceship.draw()
                    loss_hp_sound.play()
                    player_health -= 1
                    explosions.append(Explosion(spaceship.rect.centerx, config.HEIGHT-50))
                    player_word = ""
                    boss.current_word = boss.get_next_word()  # Get a new word
                    boss_word_timer = pygame.time.get_ticks()  # Reset timer

            if player_word.strip() == boss.current_word:
                boss.take_damage(1)  
                player_score += 2000  
                player_word = ""  
                laser_sound.play()
                
                # Define three possible explosion positions
                explosion_positions = [
                    (config.WIDTH // 2, config.HEIGHT // 2 - 150),
                    (config.WIDTH // 2 - 70, config.HEIGHT // 2 + 20),
                    (config.WIDTH // 2 + 70, config.HEIGHT // 2 + 20),
                ]
                # Choose one explosion randomly
                random_explosion = random.choice(explosion_positions)
                explosions.append(Explosion(*random_explosion))
                
                correct_word_positions.append((spaceship.rect.center, (config.WIDTH // 2, text_y)))
                boss.current_word = boss.get_next_word()  # Get new word
                boss_word_timer = pygame.time.get_ticks()  # Reset timer

                # Add explosion effect at boss position
                # explosions.append(Explosion(boss.rect.centerx, boss.rect.centery))

            # Check if boss is defeated
            if boss.is_defeated():
                boom_sound.play()
                state = 4  
                state_timer = 0

            if player_health <= 0:
                running = False
            pygame.draw.rect(screen, config.WHITE, (0, 0, config.WIDTH, 54)) 
            pygame.draw.rect(screen, config.DARKGREY, (0, 0, config.WIDTH, 50)) 
            draw_text_left_aligned(f"Score :", font, config.WHITE, 5, 0)
            pygame.draw.polygon(screen, config.GREY, trapezoid_points)
            # pygame.draw.polygon(screen, config.DARKGREY, trapezoid_points,10)  # Change color as needed
            pygame.draw.lines(screen, config.WHITE, False, [  # False = not a closed shape
                trapezoid_points[0],  # Top-left
                trapezoid_points[3],  # Bottom-left
                trapezoid_points[2],  # Bottom-right
                trapezoid_points[1]   # Top-right (skipping the last connection)
            ], 5) 
            draw_text_top(player_word, config.FONT_DIS, config.CYAN, config.WIDTH // 2, 0)
        #---------------------------- state 4 -----------------------------#
        elif state == 4:
            spaceship.update()
            spaceship.draw()
            # Initialize words and positions (Only once)
            if 'word_positions' not in locals():
                word_positions = []  # Stores positions of words
                random_words = random.sample(remembered_words, min(len(remembered_words), 15))  # Pick up to 15 words
                
                for word in random_words:
                    max_attempts = 100  # Avoid infinite loops
                    while max_attempts > 0:
                        x_pos = random.randint(100, config.WIDTH - 200)  # Adjust for word width
                        y_pos = random.randint(100, config.HEIGHT - 200)

                        # Check if new position overlaps with existing words
                        collision = False
                        for existing_word, ex, ey in word_positions:
                            distance = ((x_pos - ex) ** 2 + (y_pos - ey) ** 2) ** 0.5
                            if distance < 100:  # Adjust distance to prevent overlapping
                                collision = True
                                break
                        
                        if not collision:  # If no overlap, accept the position
                            word_positions.append((word, x_pos, y_pos))
                            break
                        
                        max_attempts -= 1  # Retry with a new position
            for word, x_pos, y_pos in word_positions:
                screen.blit(bonus_box, (x_pos - 96, y_pos - 96))  # Draw box

                # Compare typed letters
                typed_word = player_word  # Assume `player_input` holds the player's current input
                correct_length = min(len(typed_word), len(word))  # Prevent out-of-bounds errors

                # Split the word into correctly typed (red) and remaining (white)
                correct_part = word[:correct_length] if word[:correct_length] == typed_word else ""
                remaining_part = word[len(correct_part):]

                # Render text with colors
                correct_surface = font.render(correct_part, True, config.YELLOW)  # Red for correct letters
                remaining_surface = font.render(remaining_part, True, config.WHITE)  # Yellow for remaining letters
                
                # Position text
                total_width = correct_surface.get_width() + remaining_surface.get_width()

                # Calculate the center for the full text (both correct and remaining)
                start_x = x_pos - 96 + 96 - total_width // 2  # Center the text in the bonus box
                correct_rect = correct_surface.get_rect(topleft=(start_x, y_pos-28  ))
                remaining_rect = remaining_surface.get_rect(topleft=(correct_rect.right, y_pos-28  ))

                # Draw text
                screen.blit(correct_surface, correct_rect)
                screen.blit(remaining_surface, remaining_rect)

                
            # Draw countdown timer
            remaining_time = max(0, bonus_timer // 1000)
            # draw_text_top(player_word, config.FONT_DIS, config.CYAN, config.WIDTH // 2, 0)
            draw_text_top(f"{remaining_time}", config.FONT_DIS, config.YELLOW, config.WIDTH // 2, 0)

            # Draw words at their positions
            # for word, x, y in word_positions:
            #     draw_text(word, font, config.WHITE, x, y)

            # Check player input
            if player_word in [w[0] for w in word_positions]:  # If player typed a correct word
                correct_sound.play()
                player_score += len(player_word) * 2000
                word_positions = [(w, x, y) for w, x, y in word_positions if w != player_word]  # Remove typed word
                player_word = ""

            # End game when all words are typed or time runs out
            if not word_positions or bonus_timer <= 0:
                running = False

            bonus_timer -= delta_time


            if bonus_timer <= 0:
                running = False
            pygame.draw.rect(screen, config.WHITE, (0, 0, config.WIDTH, 54)) 
            pygame.draw.rect(screen, config.DARKGREY, (0, 0, config.WIDTH, 50)) 
            draw_text_left_aligned(f"Score :", font, config.WHITE, 5, 0)
            pygame.draw.polygon(screen, config.GREY, trapezoid_points)
            # pygame.draw.polygon(screen, config.DARKGREY, trapezoid_points,10)  # Change color as needed
            pygame.draw.lines(screen, config.WHITE, False, [  # False = not a closed shape
                trapezoid_points[0],  # Top-left
                trapezoid_points[3],  # Bottom-left
                trapezoid_points[2],  # Bottom-right
                trapezoid_points[1]   # Top-right (skipping the last connection)
            ], 5) 
            draw_text_right_aligned(f"Bonus Time", font, config.WHITE,  ((config.WIDTH // 6)*5), 0)
            draw_text_top(f"{remaining_time}", config.FONT_DIS, config.YELLOW, config.WIDTH // 2, 0)
            # draw_text_top(player_word, config.FONT_DIS, config.CYAN, config.WIDTH // 2, 0)
        
        # Draw laser lines
        for start_pos, end_pos in correct_word_positions:
            # Outer yellow line (thickness 2)
            adjusted_start = (start_pos[0], start_pos[1] - 40)
            pygame.draw.line(screen, config.CYAN, adjusted_start, end_pos, 20)  

            # Middle white line (thickness 4)
            pygame.draw.line(screen, config.WHITE, adjusted_start, end_pos, 10)  
            
            pygame.draw.circle(screen, config.CYAN, adjusted_start, 20)
            pygame.draw.circle(screen, config.WHITE, adjusted_start, 10)
        # Clear laser effects after a short duration
        correct_word_positions.clear()
        
        

        # Update explosions
        for explosion in explosions[:]:
            explosion.update()
            
            explosion.draw(screen)
            if explosion.finished:
                explosions.remove(explosion)
        
        draw_text_left_aligned(f"{player_score:,}", config.SCORE, config.LIGHTYELLOW, config.WIDTH // 11, -10)

        draw_health(player_health, config.WIDTH - 150, 5)
        
        
        pygame.display.flip()
        clock.tick(config.FPS)

    return game_over_menu(player_score)

# draw_text("Bonus Round!", font2, config.YELLOW, config.WIDTH // 2, 200)
# draw_text("Type the previously memorized words!", font2, config.YELLOW, config.WIDTH // 2, 280)



# adventure_s8()
