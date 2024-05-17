import pygame
import pygame_gui

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong Game')

# Set up the colors
white = (255, 255, 255)
black = (0, 0, 0)

# Set up the paddles and ball
paddle_width = 15
paddle_height = 100
ball_size = 15

# Initialize paddle positions
player1_x = 50
player1_y = screen_height // 2 - paddle_height // 2
player2_x = screen_width - 50 - paddle_width
player2_y = screen_height // 2 - paddle_height // 2

# Initialize ball position and velocity
ball_x = screen_width // 2 - ball_size // 2
ball_y = screen_height // 2 - ball_size // 2
ball_dx = 4
ball_dy = 4

# Initialize paddle velocities
paddle_speed = 6
player1_dy = 0
player2_dy = 0

# Set up the font for scoring
font = pygame.font.Font(None, 74)

# Initialize scores
score1 = 0
score2 = 0

# Initialize game mode
game_mode = None

# Set up Pygame GUI manager
manager = pygame_gui.UIManager((screen_width, screen_height))

# Create buttons for the main menu
single_player_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 250), (100, 50)),
                                                     text='Single Player',
                                                     manager=manager)
two_player_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 310), (100, 50)),
                                                  text='Two Player',
                                                  manager=manager)
quit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 370), (100, 50)),
                                           text='Quit',
                                           manager=manager)

# Create pause button
pause_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((700, 10), (80, 50)),
                                            text='Pause',
                                            manager=manager)
pause_button.hide()

# Function to start the game
def start_game(mode):
    global game_mode
    game_mode = mode
    manager.clear_and_reset()
    pause_button.show()

# Function to show the pause menu
def show_pause_menu():
    resume_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 250), (100, 50)),
                                                 text='Resume',
                                                 manager=manager)
    main_menu_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 310), (100, 50)),
                                                    text='Main Menu',
                                                    manager=manager)
    quit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((350, 370), (100, 50)),
                                               text='Quit',
                                               manager=manager)

# Main game loop
running = True
paused = False
clock = pygame.time.Clock()
while running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == single_player_button:
                start_game('single')
            elif event.ui_element == two_player_button:
                start_game('two')
            elif event.ui_element == quit_button:
                running = False
            elif event.ui_element == pause_button:
                paused = True
                pause_button.hide()  # Hide the pause button when paused
            elif event.ui_element.text == 'Resume':
                paused = False
                pause_button.show()  # Show the pause button when resumed
            elif event.ui_element.text == 'Main Menu':
                paused = False
                game_mode = None
                manager.clear_and_reset()
                single_player_button.show()
                two_player_button.show()
                quit_button.show()
                pause_button.hide()  # Hide the pause button when returning to the main menu
            elif event.ui_element.text == 'Quit':
                running = False

        manager.process_events(event)

    if game_mode and not paused:
        # Game logic
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player1_dy = -paddle_speed
        elif keys[pygame.K_s]:
            player1_dy = paddle_speed
        else:
            player1_dy = 0

        if game_mode == 'two':
            if keys[pygame.K_UP]:
                player2_dy = -paddle_speed
            elif keys[pygame.K_DOWN]:
                player2_dy = paddle_speed
            else:
                player2_dy = 0
        else:
            # Simple AI for single player mode
            if ball_y < player2_y + paddle_height // 2:
                player2_dy = -paddle_speed
            elif ball_y > player2_y + paddle_height // 2:
                player2_dy = paddle_speed

        # Move paddles
        player1_y += player1_dy
        player2_y += player2_dy

        # Prevent paddles from going out of bounds
        player1_y = max(0, min(screen_height - paddle_height, player1_y))
        player2_y = max(0, min(screen_height - paddle_height, player2_y))

        # Move ball
        ball_x += ball_dx
        ball_y += ball_dy

        # Ball collision with top and bottom
        if ball_y <= 0 or ball_y >= screen_height - ball_size:
            ball_dy *= -1

        # Ball collision with paddles
        if (ball_x <= player1_x + paddle_width and player1_y < ball_y < player1_y + paddle_height) or \
           (ball_x >= player2_x - ball_size and player2_y < ball_y < player2_y + paddle_height):
            ball_dx *= -1

        # Ball out of bounds (left or right)
        if ball_x <= 0:
            score2 += 1
            ball_x, ball_y = screen_width // 2 - ball_size // 2, screen_height // 2 - ball_size // 2
            ball_dx *= -1
        if ball_x >= screen_width - ball_size:
            score1 += 1
            ball_x, ball_y = screen_width // 2 - ball_size // 2, screen_height // 2 - ball_size // 2
            ball_dx *= -1

        # Fill screen with black
        screen.fill(black)

        # Draw paddles and ball
        pygame.draw.rect(screen, white, (player1_x, player1_y, paddle_width, paddle_height))
        pygame.draw.rect(screen, white, (player2_x, player2_y, paddle_width, paddle_height))
        pygame.draw.ellipse(screen, white, (ball_x, ball_y, ball_size, ball_size))

        # Draw the net
        for i in range(10, screen_height, 40):
            if i % 2 == 0:
                continue
            pygame.draw.rect(screen, white, (screen_width // 2 - 2, i, 4, 20))

        # Display scores
        score_text = font.render(str(score1), True, white)
        screen.blit(score_text, (screen_width // 4, 20))
        score_text = font.render(str(score2), True, white)
        screen.blit(score_text, (screen_width * 3 // 4, 20))

        # Update the display
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()

    else:
        # Update the display when paused
        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()

pygame.quit()