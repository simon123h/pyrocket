
import math
import pygame
import pymunk
from pymunk import Vec2d
from objects import Wall, Ball
from rocket import Rocket


class RocketGame():

    # Settings
    FRAME_WIDTH = 1600  # in px
    FRAME_HEIGHT = 900  # in px
    GRAVITY = 600  # in m/s^2
    DT = 1. / 1000.  # in seconds
    FPS = 50
    SAVE_IMG = False
    # ZOOM = 1  # in px / meter

    def __init__(self):

        # screen and runtime
        self.screen = pygame.display.set_mode(
            (self.FRAME_WIDTH, self.FRAME_HEIGHT))
        self.clock = pygame.time.Clock()

        # game state variables
        self.running = True
        self.run_physics = True

        # physics stuff
        self.space = pymunk.Space()
        self.space.gravity = 0.0, -self.GRAVITY
        self.ntimesteps = 2  # number of timesteps per frame

        # game objects
        self.objects = []
        self.rocket = None

        # list of events and pressed keys
        self.events = []
        self.pressed_keys = []

        # add ground
        for n in range(4):
            self.add_object(Wall(self.space, Vec2d(
                0, 2*n), Vec2d(self.FRAME_WIDTH, 2*n)))
        # add surrounding walls
        self.add_object(Wall(self.space, Vec2d(
            0, 0), Vec2d(0, 1e5*self.FRAME_HEIGHT)))
        self.add_object(Wall(self.space, Vec2d(self.FRAME_WIDTH, 0),
                             Vec2d(self.FRAME_WIDTH, 1e5*self.FRAME_HEIGHT)))
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
        self.rocket = Rocket(self.space, self.FRAME_WIDTH/2, 100)
        # add it to the game
        self.add_object(self.rocket)

    # update the physics of the game and each object
    def update_physics(self):
        if self.run_physics:
            # update the external forces for each object
            for obj in self.objects:
                obj.update_forces()
            # perform time steps
            self.space.step(self.DT)

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
                x, y = event.pos[0], self.flipy(event.pos[1])
                self.add_object(Ball(self.space, x, y))
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.add_new_rocket()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                self.run_physics = not self.run_physics

        # update rocket controls
        self.rocket.handle_controls(self)

    # draw the game
    def draw(self):
        # Clear screen
        self.screen.fill(pygame.Color("white"))
        # Draw background
        h = self.rocket.body.position.y
        f = max(2000/h, 0)
        color = (254-f, 254-f, 254-f)
        dist = 700
        offs = h % dist
        for i in range(-1, 5):
            shift = offs + i*dist
            pygame.draw.rect(self.screen, color,
                             (0, 0+shift, self.FRAME_WIDTH, dist/2))
        # Draw objects
        for obj in self.objects:
            obj.draw(self)
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
""".format(self.rocket.engine.thrust, self.rocket.engine.angle / 180. * math.pi, self.rocket.twr(), self.rocket.body.position.y, self.rocket.body.velocity.y, self.rocket.pilot.sas_mode)
        y = 5
        for line in text.splitlines():
            text = font.render(line, True, pygame.Color("black"))
            self.screen.blit(text, (5, y))
            y += 20

    # Small hack to convert chipmunk physics to pygame coordinates
    def flipy(self, y):
        if self.rocket is None:
            return -y + self.FRAME_HEIGHT
        else:
            return -y + self.FRAME_HEIGHT / 2 + self.rocket.body.position.y
