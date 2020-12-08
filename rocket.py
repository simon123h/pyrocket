import math
import pygame
import pymunk
from objects import Poly
from engine import Engine
from pilot import Autopilot


class Rocket(Poly):

    def __init__(self, space, x, y, w=15, h=150, mass=10):
        points = [(-w/2, -h/2), (w/2, -h/2),
                  (w/2, h/2), (0, h/1.5), (-w/2, h/2)]
        super().__init__(space, x, y, points, mass)
        self.space = space
        self.mass = mass
        self.color = 112, 122, 255
        self.shape.friction = 0.5

        # rocket dimensions
        self.w = w
        self.h = h

        # drag coefficient
        self.drag_coeff = 1e-5
        self.airbrakes_enabled = False

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

    # the aerodynamic drag
    def update_drag(self):
        # velocity
        v = self.body.velocity
        # orientation
        rot = self.body.rotation_vector
        # exposed area
        A = abs(v.normalized().dot(rot))
        A = A * self.h**2 + (1-A) * self.w**2
        A *= self.drag_coeff
        # calculate and apply drag force
        drag_force = super()._drag_formula(A, v)
        # where is drag force applied?
        drag_fp = pymunk.Vec2d(0, -5*self.h)
        if self.airbrakes_enabled:
            drag_fp = -0.3*drag_fp
            drag_force *= 1
        self.body.apply_force_at_local_point(
            drag_force.rotated(-self.body.angle), drag_fp)
        # relax angular velocity
        self.body.angular_velocity *= 0.999

    # get telemetry data, e.g., for autopilot
    def get_telemetry(self):
        data = {}
        data["position"] = self.body.position
        data["velocity"] = self.body.velocity
        angle = (self.body.angle + math.pi) % (2 * math.pi) - math.pi
        data["angle"] = angle
        data["angular_velocity"] = self.body.angular_velocity
        return data

    # control the rocket using the pilot / autopilot
    def handle_controls(self, game):
        self.pilot.handle_controls(game)

    # thrust to weight ratio
    def twr(self):
        return -self.engine.thrust / self.mass / self.space.gravity[1]

    # draw the rocket to the game's screen
    def draw(self, game):
        # main body
        ps = [p.rotated(self.body.angle) +
              self.body.position for p in self.shape.get_vertices()]
        ps.append(ps[0])
        for i, p in enumerate(ps):
            ps[i] = game.pos2screen(p)
        pygame.draw.polygon(game.screen, pygame.Color(*self.color), ps)
        pygame.draw.lines(game.screen, pygame.Color("black"), False, ps, 2)
        # fins
        h = self.h
        w = self.w
        fins = [(-w/2, -h/2.1), (-w*1.4, -h/2.1), (-w/2, -h/5), (-w/2, -h/2.1)]
        fins = [pymunk.Vec2d(p).rotated(self.body.angle) +
                self.body.position for p in fins]
        for i, p in enumerate(fins):
            fins[i] = game.pos2screen(p)
        pygame.draw.polygon(game.screen, pygame.Color(*self.color), fins)
        pygame.draw.lines(game.screen, pygame.Color("black"), False, fins, 2)
        fins = [(w/2, -h/2.1), (w*1.4, -h/2.1), (w/2, -h/5), (w/2, -h/2.1)]
        fins = [pymunk.Vec2d(p).rotated(self.body.angle) +
                self.body.position for p in fins]
        for i, p in enumerate(fins):
            fins[i] = game.pos2screen(p)
        pygame.draw.polygon(game.screen, pygame.Color(*self.color), fins)
        pygame.draw.lines(game.screen, pygame.Color("black"), False, fins, 2)
        # draw the engine
        engine_position = self.body.position + \
            self.engine_pos.rotated(self.body.angle)
        self.engine.draw(game, engine_position, self.body.angle)
        # draw the airbrakes
        if self.airbrakes_enabled:
            airbs = [
                (-w/2, 0.47*h), (-w*1.5, 0.47*h), (-w/2, 0.5*h),
                (+w/2, 0.5*h), (+w*1.5, 0.47*h), (+w/2, 0.47*h)
            ]
            airbs = [pymunk.Vec2d(p).rotated(self.body.angle) +
                     self.body.position for p in airbs]
            for i, p in enumerate(airbs):
                airbs[i] = game.pos2screen(p)
            pygame.draw.polygon(game.screen, pygame.Color(*self.color), airbs)
            pygame.draw.lines(game.screen, pygame.Color(
                "black"), False, airbs, 2)
