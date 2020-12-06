import math
from objects import Poly, flipy
import pygame
import pymunk


class Rocket(Poly):

    def __init__(self, space, x, y, w=15, h=150, mass=10):
        points = [(-w/2, -h/2), (w/2, -h/2),
                  (w/2, h/2), (0, h/1.8), (-w/2, h/2)]
        super().__init__(space, x, y, points, mass)
        self.space = space
        self.mass = mass
        self.edgecolor = "blue"

        self.w = w
        self.h = h
        self.thrust_origin = pymunk.Vec2d(0, -h/2)

        self.thrust = self.mass * abs(self.space.gravity[1])
        self.thrust_angle = 0
        self.body.angle = 0
        self.ignited = True

        self.sas_mode = "OFF"

    def live(self):
        self.autopilot()
        angle = self.thrust_angle / 180. * math.pi
        thrust_x = self.thrust * math.sin(angle)
        thrust_y = self.thrust * math.cos(angle)
        thrust_force = (thrust_x, thrust_y)
        if self.ignited:
            self.body.apply_force_at_local_point(
                thrust_force, self.thrust_origin)

    def autopilot(self):
        # get telemetry data
        position = self.body.position
        angle = self.body.angle
        velocity = self.body.velocity
        angular_velocity = self.body.angular_velocity

        if self.sas_mode == "OFF":
            pass
        elif self.sas_mode == "stability_assist":
            pass
        elif self.sas_mode == "hover":
            # control thrust
            self.thrust = self.mass * abs(self.space.gravity[1])
            vy_tol = 1e-4
            if velocity.y < vy_tol:
                self.thrust *= 1.05
            if velocity.y > vy_tol:
                self.thrust *= 0.95
            # control thrust angle
            vx_tol = 1e-4
            if angle < vx_tol:
                self.thrust_angle += 0.01
            if angle > vx_tol:
                self.thrust_angle -= 0.01

        elif self.sas_mode == "land":
            pass

    # thrust to weight ratio
    def twr(self):
        return -self.thrust / self.mass / self.space.gravity[1]

    def draw(self, screen):
        ps = [p.rotated(self.body.angle) +
              self.body.position for p in self.shape.get_vertices()]
        ps.append(ps[0])
        for i, p in enumerate(ps):
            ps[i] = int(p.x), int(flipy(p.y))
        pygame.draw.lines(screen, pygame.Color(self.edgecolor), False, ps, 2)
        if self.ignited:
            # bottom_l = ps[0]
            # bottom_r = ps[1]
            # mid = bottom_l.x - bottom_
            thrust_pos = self.body.position + \
                self.thrust_origin.rotated(self.body.angle)
            ll = 20
            angle = -self.thrust_angle / 180. * math.pi + self.body.angle - math.pi/2
            thrust_end = thrust_pos + ll * \
                pymunk.Vec2d(math.cos(angle), math.sin(angle))
            p1 = int(thrust_pos.x), int(flipy(thrust_pos.y))
            p2 = int(thrust_end.x), int(flipy(thrust_end.y))
            pygame.draw.lines(screen, pygame.Color(
                "red"), False, [p1, p2], 2)

            # print(pos)
