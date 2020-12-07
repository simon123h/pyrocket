
import pygame
import pymunk
from pymunk import Vec2d
from objects import Wall
from rocket import Rocket
from settings import FRAME_WIDTH, FRAME_HEIGHT, GRAVITY, track, draw_background


class RocketGame():

    def __init__(self):

        # screen and runtime
        self.screen = pygame.display.set_mode((FRAME_WIDTH, FRAME_HEIGHT))
        self.clock = pygame.time.Clock()

        # game state variables
        self.running = True
        self.run_physics = True

        # physics stuff
        self.space = pymunk.Space()
        self.space.gravity = 0.0, -GRAVITY
        # time step
        self.dt = 1. / 100.

        # game objects
        self.objects = []
        self.rocket = None

        # add ground
        for n in range(4):
            self.add_object(Wall(self.space, Vec2d(
                0, 5*n), Vec2d(FRAME_WIDTH, 5*n)))

        # add surrounding walls
        self.add_object(Wall(self.space, Vec2d(
            0, 0), Vec2d(0, 1e5*FRAME_HEIGHT)))
        self.add_object(Wall(self.space, Vec2d(FRAME_WIDTH, 0),
                             Vec2d(FRAME_WIDTH, 1e5*FRAME_HEIGHT)))

        # add the rocket
        self.add_new_rocket()

    # add an object to the game and return it
    def add_object(self, obj):
        if obj not in self.objects:
            self.objects.append(obj)
        return obj

    # remove an object from the game
    def remove_object(self, obj):
        if obj in self.objects:
            self.objects.remove(obj)

    # add a new rocket
    def add_new_rocket(self):
        # remove the previous rocket
        if self.rocket is not None:
            self.remove_object(self.rocket)
        # create new rocket
        self.rocket = Rocket(self.space, FRAME_WIDTH/2, 100)
        # add it to the game and activate tracking
        self.add_object(self.rocket)
        track(self.rocket)

    # update the physics of the game and each object
    def update_physics(self):
        if self.run_physics:
            # update the external forces for each object
            for obj in self.objects:
                obj.update_forces()
            # perform a time step
            self.space.step(self.dt)

    # draw the game
    def draw(self):
        # Clear screen
        self.screen.fill(pygame.Color("white"))
        # Draw background
        draw_background(self.screen)
        # Draw objects
        for obj in self.objects:
            obj.draw(self.screen)
