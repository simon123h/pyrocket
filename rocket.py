import math
from objects import Poly
from settings import flipy
from engine import Engine
from pilot import Autopilot
import pygame
import pymunk


class Rocket(Poly):

    def __init__(self, space, x, y, w=15, h=150, mass=10):
        points = [(-w/2, -h/2), (w/2, -h/2),
                  (w/2, h/2), (0, h/1.5), (-w/2, h/2)]
        super().__init__(space, x, y, points, mass)
        self.space = space
        self.mass = mass
        self.edgecolor = "blue"

        self.w = w
        self.h = h

        # the rocket engine
        self.engine = Engine()
        self.engine_pos = pymunk.Vec2d(0, -h/2)  # position of the engine
        self.engine.set_thrust(2 * self.mass * abs(self.space.gravity[1]))

        # the pilot / autopilot system
        self.pilot = Autopilot(self)
        self.sas_mode = "OFF"

    # apply the physical forces to the rocket
    def update_forces(self):
        angle = self.engine.angle
        thrust_x = self.engine.thrust * math.sin(angle)
        thrust_y = self.engine.thrust * math.cos(angle)
        thrust_force = (thrust_x, thrust_y)
        if self.engine.ignited:
            self.body.apply_force_at_local_point(
                thrust_force, self.engine_pos)

    # get telemetry data, e.g., for autopilot
    def get_telemetry(self):
        data = {}
        data["position"] = self.body.position
        data["velocity"] = self.body.velocity
        data["angle"] = self.body.angle
        data["angular_velocity"] = self.body.angular_velocity
        return data

    # control the rocket using the pilot / autopilot
    def handle_controls(self, game):
        self.pilot.handle_controls(game)

    # thrust to weight ratio
    def twr(self):
        return -self.engine.thrust / self.mass / self.space.gravity[1]

    # draw the rocket to a screen
    def draw(self, screen):
        # main body
        ps = [p.rotated(self.body.angle) +
              self.body.position for p in self.shape.get_vertices()]
        ps.append(ps[0])
        for i, p in enumerate(ps):
            ps[i] = int(p.x), int(flipy(p.y))
        pygame.draw.lines(screen, pygame.Color(self.edgecolor), False, ps, 2)
        # fins
        h = self.h
        w = self.w
        fins = [(-w/2, -h/2.1), (-w*1.4, -h/2.1), (-w/2, -h/5), (-w/2, -h/2.1)]
        fins = [pymunk.Vec2d(p).rotated(self.body.angle) +
                self.body.position for p in fins]
        for i, p in enumerate(fins):
            fins[i] = int(p.x), int(flipy(p.y))
        pygame.draw.lines(screen, pygame.Color(self.edgecolor), False, fins, 2)
        fins = [(w/2, -h/2.1), (w*1.4, -h/2.1), (w/2, -h/5), (w/2, -h/2.1)]
        fins = [pymunk.Vec2d(p).rotated(self.body.angle) +
                self.body.position for p in fins]
        for i, p in enumerate(fins):
            fins[i] = int(p.x), int(flipy(p.y))
        pygame.draw.lines(screen, pygame.Color(self.edgecolor), False, fins, 2)
        # draw the engine
        engine_position = self.body.position + \
            self.engine_pos.rotated(self.body.angle)
        self.engine.draw(screen, engine_position, self.body.angle)
