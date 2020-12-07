#!/usr/bin/python3

import math
import pygame
from settings import flipy
from game import RocketGame
from objects import Ball

# initalize pygame
pygame.init()

# create the game
game = RocketGame()

while game.running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game.running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            game.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos[0], flipy(event.pos[1])
            game.add_object(Ball(game.space, x, y))
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            run_physics = not run_physics
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game.rocket.engine.ignited = not game.rocket.engine.ignited
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_0:
            game.rocket.pilot.sas_mode = "OFF"
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            game.rocket.pilot.sas_mode = "assist"
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
            game.rocket.pilot.sas_mode = "stabilize"
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
            game.rocket.pilot.sas_mode = "hover"
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_4:
            game.rocket.pilot.sas_mode = "land"
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            game.add_new_rocket()

    # update autopilot
    game.rocket.control(game.dt)

    # handle pressed keys
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_UP]:
        game.rocket.engine.thrust += 50
    if keys_pressed[pygame.K_DOWN]:
        game.rocket.engine.thrust -= 50
        game.rocket.engine.thrust = max(game.rocket.engine.thrust, 0)
    if keys_pressed[pygame.K_LEFT]:
        game.rocket.body.angle += 0.002
        game.rocket.engine.angle += 0.2 / 180. * math.pi
    if keys_pressed[pygame.K_RIGHT]:
        game.rocket.body.angle -= 0.002
        game.rocket.engine.angle -= 0.2 / 180. * math.pi

    # Update physics
    game.update_physics()

    # Draw the game
    game.draw()

    # Display some text
    font = pygame.font.Font(None, 24)
    text = """Thrust: {:f}
Angle: {:f}°
TWR: {:f}
Height: {:.1e}
Velocity: {:.1e}
SAS: {:s}

Controls:
---------
Up/Down - throttle
Left/Right - thrust vector control
space - start/stop engine
0-9 - switch SAS mode
mouse - add obstacle
P - pause
R - restart
""".format(game.rocket.engine.thrust, game.rocket.engine.angle / 180. * math.pi, game.rocket.twr(), game.rocket.body.position.y, game.rocket.body.velocity.y, game.rocket.pilot.sas_mode)
    y = 5
    for line in text.splitlines():
        text = font.render(line, True, pygame.Color("black"))
        game.screen.blit(text, (5, y))
        y += 20

    # Flip screen
    pygame.display.flip()
    game.clock.tick(1/game.dt)
    pygame.display.set_caption("fps: " + str(int(game.clock.get_fps())))
