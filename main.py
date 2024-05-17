import pygame
import pygame_gui
from pong_game import PongGame
from pong_gui import PongGUI

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong Game')

# Set up Pygame GUI manager
manager = pygame_gui.UIManager((screen_width, screen_height))

# Create the Pong game and GUI instances
pong_game = PongGame()
pong_gui = PongGUI(manager, pong_game)

# Main game loop
running = True
clock = pygame.time.Clock()
while running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        manager.process_events(event)
        pong_gui.process_events(event)

    pong_game.update(time_delta)
    pong_gui.update(time_delta)

    screen.fill(pong_game.black)
    pong_game.draw(screen)
    pong_gui.draw(screen)

    pygame.display.flip()

pygame.quit()