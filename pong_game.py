import pygame
import sys
import tkinter as tk
from tkinter import simpledialog

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
paddle_width = 10
paddle_height = 100
ball_size = 20

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

def show_start_menu():
    root = tk.Tk()
    root.withdraw()
    global game_mode
    game_mode = simpledialog.askstring("Game Mode", "Enter '1' for Single Player or '2' for Two Player:")
    root.destroy()

# Show start menu
show_start_menu()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                player1_dy = -paddle_speed
            if event.key == pygame.K_s:
                player1_dy = paddle_speed
            if game_mode == '2':
                if event.key == pygame.K_UP:
                    player2_dy = -paddle_speed
                if event.key == pygame.K_DOWN:
                    player2_dy = paddle_speed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                player1_dy = 0
            if game_mode == '2':
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player2_dy = 0

    # Move paddles
    player1_y += player1_dy
    if game_mode == '2':
        player2_y += player2_dy
    else:
        # Simple AI for single player mode
        if ball_y < player2_y + paddle_height // 2:
            player2_y -= paddle_speed
        elif ball_y > player2_y + paddle_height // 2:
            player2_y += paddle_speed

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
    pygame.draw.aaline(screen, white, (screen_width // 2, 0), (screen_width // 2, screen_height))

    # Display scores
    score_text = font.render(str(score1), True, white)
    screen.blit(score_text, (screen_width // 4, 20))
    score_text = font.render(str(score2), True, white)
    screen.blit(score_text, (screen_width * 3 // 4, 20))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)
