#!/usr/bin/python3

import pygame
from game import RocketGame

# initalize pygame
pygame.init()

# create the game
game = RocketGame()

n = 0
while game.running:

    # calculate number of physical steps and resulting frames per second
    n_physics_steps = int(1 / game.DT / game.FPS)
    fps = 1 / game.DT / n_physics_steps

    # Process the controls of the game (events, pressed keys, etc.)
    game.handle_controls()

    # Update physics
    for _ in range(n_physics_steps):
        game.update_physics()

    # Draw the game
    game.draw()

    # Flip the screen
    pygame.display.flip()
    game.clock.tick(fps)
    pygame.display.set_caption("fps: " + str(int(game.clock.get_fps())))

    if game.SAVE_IMG:
        pygame.image.save(game.screen, "out/{:08d}.png".format(n))
        n += 1
