#!/usr/bin/python3

import math
import pygame
import pymunk
from pymunk import Vec2d
from objects import Ball, Wall, Rectangle, flipy, track
from rocket import Rocket

X, Y = 0, 1
# Physics collision types
COLLTYPE_BALL = 2


pygame.init()
Lx, Ly = 1600, 900
screen = pygame.display.set_mode((Lx, Ly))
clock = pygame.time.Clock()
running = True


# Physics stuff
space = pymunk.Space()
space.gravity = 0.0, -600.0
# space.gravity = 0.0, 0.0
# space.gravity = 0.0, -900.0
objects = []
run_physics = True

# add ground
for n in range(4):
    objects.append(Wall(space, Vec2d(0, 5*n), Vec2d(Lx, 5*n)))

# add surrounding walls
objects.append(Wall(space, Vec2d(0, 0), Vec2d(0, 100*Ly)))
objects.append(Wall(space, Vec2d(Lx, 0), Vec2d(Lx, 100*Ly)))

# add balls
Nballs = 0
for i in range(Nballs):
    x, y = Lx*i/Nballs, flipy(60)
    objects.append(Ball(space, x, y, 20))

# add rectangles
for i in range(Nballs):
    x, y = Lx*i/Nballs, flipy(30)
    objects.append(Rectangle(space, x, y, 20, 20))

# add the rocket
rocky = Rocket(space, Lx/2, 100, mass=10)
objects.append(rocky)
track(rocky)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos[X], flipy(event.pos[Y])
            objects.append(Ball(space, x, y))
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            run_physics = not run_physics
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            rocky.ignited = not rocky.ignited
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_0:
            rocky.sas_mode = "OFF"
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            rocky.sas_mode = "assist"
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_2:
            rocky.sas_mode = "stabilize"
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_3:
            rocky.sas_mode = "hover"
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_4:
            rocky.sas_mode = "land"
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            objects.remove(rocky)
            rocky = Rocket(space, Lx/2, 100)
            objects.append(rocky)
            track(rocky)

    dt = 1.0 / 100.0

    # update autopilot
    rocky.autopilot(dt)

    # handle pressed keys
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_UP]:
        rocky.thrust += 50
    if keys_pressed[pygame.K_DOWN]:
        rocky.thrust -= 50
        rocky.thrust = max(rocky.thrust, 0)
    if keys_pressed[pygame.K_LEFT]:
        rocky.thrust_angle += 0.2 / 180. * math.pi
    if keys_pressed[pygame.K_RIGHT]:
        rocky.thrust_angle -= 0.2 / 180. * math.pi


    # Apply forces
    rocky.live()

    # Update physics
    if run_physics:
        for x in range(1):
            space.step(dt)

    # Draw stuff
    screen.fill(pygame.Color("white"))
    for obj in objects:
        obj.draw(screen)

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
0-9 - switch SAS mode
mouse - add obstacle
P - pause
R - restart
""".format(rocky.thrust, rocky.thrust_angle / 180. * math.pi, rocky.twr(), rocky.body.position.y, rocky.body.velocity.y, rocky.sas_mode)
    y = 5
    for line in text.splitlines():
        text = font.render(line, True, pygame.Color("black"))
        screen.blit(text, (5, y))
        y += 20

    # Flip screen
    pygame.display.flip()
    clock.tick(50)
    pygame.display.set_caption("fps: " + str(int(clock.get_fps())))
