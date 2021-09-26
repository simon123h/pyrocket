
import math
import pygame
import pymunk
from pymunk import Vec2d
from objects import Wall, Ball, Rectangle
from rocket import Rocket
from tests import ALL_TESTS


class RocketGame():

    # Settings
    FRAME_WIDTH = 1600  # in px
    FRAME_HEIGHT = 900  # in px
    GRAVITY = 600
    DRAG = 1
    DT = 1. / 1000.  # in seconds
    FPS = 50
    SAVE_IMG = False
    # ZOOM = 1  # in px / meter

    def __init__(self):

        # screen and runtime
        self.screen = pygame.display.set_mode(
            (self.FRAME_WIDTH, self.FRAME_HEIGHT), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.time = 0

        # game state variables
        self.running = True
        self.run_physics = True

        # physics stuff
        self.space = pymunk.Space()
        self.space.gravity = 0.0, -self.GRAVITY

        # game objects
        self.objects = []
        self.rocket = None

        # list of events and pressed keys
        self.events = []
        self.pressed_keys = []

        # add ground
        for n in range(4):
            self.add_object(
                Wall(self.space, Vec2d(-1e9, 2*n), Vec2d(1e9, 2*n)))
        # add the rocket
        self.add_new_rocket()

        # storage for a unit test, if performing a test
        self.test = None

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
        self.rocket = Rocket(self.space, 0, 100)
        # add it to the game
        self.add_object(self.rocket)

        # # add some component
        # rpos = self.rocket.body.position + Vec2d(20, 0)
        # rect = Rectangle(self.space, *rpos, 10, 10)
        # self.add_object(rect)
        # constraint = pymunk.PinJoint(self.rocket.body, rect.body, (20, 0), (0, 0))
        # self.space.add(constraint)

        # # add some component
        # rpos = self.rocket.body.position + Vec2d(-20, 0)
        # rect = Rectangle(self.space, *rpos, 10, 10)
        # self.add_object(rect)
        # constraint = pymunk.PinJoint(self.rocket.body, rect.body, (-20, 0), (0, 0))
        # self.space.add(constraint)

    # update the physics of the game and each object
    def update_physics(self):
        if self.run_physics:
            # update the external forces for each object
            for obj in self.objects:
                obj.update_drag()
                obj.update_forces()
            # perform time steps
            self.space.step(self.DT)
            # update time
            self.time += self.DT

    # process the controls of the game (events, pressed keys, etc.)
    def handle_controls(self):

        self.events = pygame.event.get()
        self.pressed_keys = pygame.key.get_pressed()

        for event in self.events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = self.screen2pos(event.pos)
                self.add_object(Ball(self.space, x, y))
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.add_new_rocket()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                self.run_physics = not self.run_physics
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                if self.test is None:
                    self.run_tests()
            elif event.type == pygame.VIDEORESIZE:
                self.FRAME_WIDTH = event.w
                self.FRAME_HEIGHT = event.h
                self.screen = pygame.display.set_mode(
                    (self.FRAME_WIDTH, self.FRAME_HEIGHT), pygame.RESIZABLE)

        # handle unit tests
        if self.test is not None:
            if self.test.is_finished():
                self.test = self.test.next_test
                if self.test is not None:
                    self.test.start(self)

        # update rocket controls
        self.rocket.handle_controls(self)

    # draw the game
    def draw(self):
        # Clear screen
        self.screen.fill(pygame.Color("white"))
        # Draw background
        x, y = self.rocket.body.position
        color = (240, 240, 240)
        dist = 700
        offsx, offsy = -x % dist, y % dist
        for i in range(-1, 5):
            pygame.draw.rect(self.screen, color,
                             (offsx + i*dist, 0, dist/20, self.FRAME_HEIGHT))
            pygame.draw.rect(self.screen, color,
                             (0, offsy + i*dist, self.FRAME_WIDTH, dist/20))
        # Draw objects
        for obj in self.objects:
            obj.draw(self)
        # Display some text
        font = pygame.font.Font(None, 24)

        thrust = self.rocket.engine.thrust/self.rocket.engine.MAX_THRUST
        twr = self.rocket.twr()
        h = self.length_unit(self.rocket.body.position.y)
        v = self.velocity_unit(self.rocket.body.velocity.y)
        sas = self.rocket.pilot.sas_mode
        text = f"""Thrust: {thrust:3.0%}
TWR: {twr:.2f}
Height: {h}
Velocity: {v}
SAS: {sas}

Controls:
---------
Up/Down - throttle
Left/Right - thrust vector control
space - start/stop engine
0-4 - switch SAS mode
mouse - add obstacle
P - pause
R - restart
T - run tests
"""
        y = 5
        for line in text.splitlines():
            text = font.render(line, True, pygame.Color("black"))
            self.screen.blit(text, (5, y))
            y += 20

    # transform global coordinates to screen coordinates
    def pos2screen(self, pos):
        x = pos.x + self.FRAME_WIDTH / 2.
        y = pos.y - self.FRAME_HEIGHT / 2.
        if self.rocket is not None:
            x -= self.rocket.body.position.x
            y -= self.rocket.body.position.y
        return int(x), -int(y)

    # transform screen coordinates to global coordinates
    def screen2pos(self, pos):
        x = pos[0] - self.FRAME_WIDTH / 2.
        y = -pos[1] + self.FRAME_HEIGHT / 2.
        if self.rocket is not None:
            x += self.rocket.body.position.x
            y += self.rocket.body.position.y
        return Vec2d(x, y)

    # convert lengthlength_unitto string with units
    def length_unit(self, h, precision=1):
        if abs(h) < 1e3:
            return f"{h:,.{precision}f}m"
        ly = 9.461e15
        if abs(h) < 0.1*ly:
            return f"{h/1e3:,.{precision}f}km"
        else:
            return f"{h/ly:,.{precision}f}ly"

    # convert velocity to string with units
    def velocity_unit(self, v, precision=1):
        if abs(v) < 1e3:
            return f"{v:,.{precision}f}m/s"
        if abs(v) > 1e3:
            return f"{v/1e3:,.{precision}f}km/s"

    # Performs landing tests for different scenarios and measures how well the rocket performs.
    def run_tests(self):
        for n in range(len(ALL_TESTS)-1):
            ALL_TESTS[n].next_test = ALL_TESTS[n+1]
        ALL_TESTS[0].start(self)
