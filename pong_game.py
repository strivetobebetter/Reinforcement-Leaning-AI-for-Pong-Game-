import pygame
import pygame_gui

# Initialize pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Set up the GUI manager
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# Define the start menu
start_menu_rect = pygame.Rect((WIDTH // 2 - 100, HEIGHT // 2 - 100), (200, 200))
start_menu = pygame_gui.elements.UIPanel(relative_rect=start_menu_rect, manager=manager, starting_layer_height=1)
single_player_button_rect = pygame.Rect((0, 0), (180, 50))
single_player_button = pygame_gui.elements.UIButton(relative_rect=single_player_button_rect, text='Single Player', manager=manager, container=start_menu)
two_player_button_rect = pygame.Rect((0, 60), (180, 50))
two_player_button = pygame_gui.elements.UIButton(relative_rect=two_player_button_rect, text='Two Player', manager=manager, container=start_menu)

# Define the pause menu
pause_menu_rect = pygame.Rect((WIDTH // 2 - 100, HEIGHT // 2 - 100), (200, 200))
pause_menu = pygame_gui.elements.UIPanel(relative_rect=pause_menu_rect, manager=manager, starting_layer_height=1)
pause_menu.hide()
resume_button_rect = pygame.Rect((0, 0), (180, 50))
resume_button = pygame_gui.elements.UIButton(relative_rect=resume_button_rect, text='Resume', manager=manager, container=pause_menu)
quit_button_rect = pygame.Rect((0, 60), (180, 50))
quit_button = pygame_gui.elements.UIButton(relative_rect=quit_button_rect, text='Quit', manager=manager, container=pause_menu)

# Game variables
running = True
game_started = False
paused = False
clock = pygame.time.Clock()

# Pong game variables
paddle_speed = 400
ball_speed_x = 300
ball_speed_y = 300
player_score = 0
opponent_score = 0
ball_pos = [WIDTH // 2, HEIGHT // 2]
player_paddle_pos = [WIDTH - 20, HEIGHT // 2 - 70]
opponent_paddle_pos = [10, HEIGHT // 2 - 70]
ball_radius = 7

# Pong game functions
def draw_paddle(pos):
    pygame.draw.rect(screen, (255, 255, 255), (*pos, 10, 140))

def draw_ball(pos):
    pygame.draw.circle(screen, (255, 255, 255), pos, ball_radius)

def update_ball():
    global ball_speed_x, ball_speed_y, player_score, opponent_score
    ball_pos[0] += int(ball_speed_x * time_delta)
    ball_pos[1] += int(ball_speed_y * time_delta)

    # Collision with top and bottom
    if ball_pos[1] - ball_radius < 0 or ball_pos[1] + ball_radius > HEIGHT:
        ball_speed_y *= -1

    # Collision with paddles
    if ball_pos[0] - ball_radius < player_paddle_pos[0] + 10 and \
       player_paddle_pos[1] < ball_pos[1] < player_paddle_pos[1] + 140:
        ball_speed_x *= -1
    elif ball_pos[0] + ball_radius > opponent_paddle_pos[0] and \
         opponent_paddle_pos[1] < ball_pos[1] < opponent_paddle_pos[1] + 140:
        ball_speed_x *= -1

    # Scoring points
    if ball_pos[0] < 0:
        opponent_score += 1
        reset_ball()
    elif ball_pos[0] > WIDTH:
        player_score += 1
        reset_ball()

def reset_ball():
    global ball_speed_x, ball_speed_y, ball_pos
    ball_pos = [WIDTH // 2, HEIGHT // 2]
    ball_speed_x *= -1
    ball_speed_y *= -1

def update_paddles():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        opponent_paddle_pos[1] -= paddle_speed * time_delta
    if keys[pygame.K_DOWN]:
        opponent_paddle_pos[1] += paddle_speed * time_delta

# Main game loop
while running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == single_player_button:
                game_started = True
                start_menu.hide()
            elif event.ui_element == two_player_button:
                game_started = True
                start_menu.hide()
            elif event.ui_element == resume_button:
                paused = False
                pause_menu.hide()
            elif event.ui_element == quit_button:
                running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused
                if paused:
                    pause_menu.show()
                else:
                    pause_menu.hide()

    if game_started and not paused:
        screen.fill((0, 0, 0))
        update_paddles()
        update_ball()
        draw_paddle(player_paddle_pos)
        draw_paddle(opponent_paddle_pos)
        draw_ball(ball_pos)

    manager.update(time_delta)
    manager.draw_ui(screen)
    pygame.display.flip()

pygame.quit()