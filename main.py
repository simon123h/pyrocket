#!/usr/bin/python3

import math
import pygame
from game import RocketGame
from settings import PHYSICS_DT

# initalize pygame
pygame.init()

# create the game
game = RocketGame()

while game.running:

    # Process the controls of the game (events, pressed keys, etc.)
    game.handle_controls()

    # Update physics
    game.update_physics()

    # Draw the game
    # TODO: reduce the FPS
    game.draw()

    # Flip the screen
    pygame.display.flip()
    game.clock.tick(1 / PHYSICS_DT)
    pygame.display.set_caption("fps: " + str(int(game.clock.get_fps())))
