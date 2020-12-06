#!/usr/bin/python3

import pygame
import pymunk
from pymunk import Vec2d
from objects import Ball, HWall, Rectangle
from rocket import Rocket

X, Y = 0, 1
# Physics collision types
COLLTYPE_BALL = 2


def flipy(y):
    """Small hack to convert chipmunk physics to pygame coordinates"""
    return -y + 600


pygame.init()
screen = pygame.display.set_mode((900, 600))
clock = pygame.time.Clock()
running = True

# Physics stuff
space = pymunk.Space()
space.gravity = 0.0, 0.0
# space.gravity = 0.0, -900.0
objects = []
run_physics = True

# add ground
for n in range(4):
    objects.append(HWall(space, 900, 5*n))

# add balls
Nballs = 25
for i in range(Nballs):
    x, y = 900*i/Nballs, flipy(60)
    objects.append(Ball(space, x, y, 20))

# add rectangles
for i in range(Nballs):
    x, y = 900*i/Nballs, flipy(30)
    objects.append(Rectangle(space, x, y, 20, 20))

# add the special ball
rocky = Rocket(space, 450, 100)
objects.append(rocky)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos[X], flipy(event.pos[Y])
            objects.append(Ball(space, x, y))
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            run_physics = not run_physics

    # Apply forces
    rocky.apply_force()

    # Update physics
    if run_physics:
        dt = 1.0 / 120.0
        for x in range(1):
            space.step(dt)

    # Draw stuff
    screen.fill(pygame.Color("white"))
    for obj in objects:
        obj.draw(screen)

    # Flip screen
    pygame.display.flip()
    clock.tick(60)
    pygame.display.set_caption("fps: " + str(int(clock.get_fps())))