from objects import Poly
import math


class Rocket(Poly):

    def __init__(self, space, x, y, w=15, h=150, mass=10):
        points = [(-w/2, -h/2), (w/2, -h/2),
                  (w/2, h/2), (0, h/1.8), (-w/2, h/2)]
        super().__init__(space, x, y, points, mass)
        self.space = space
        self.mass = mass
        self.edgecolor = "red"

        self.w = w
        self.h = h
        self.thrust_origin = (0, -h/2)

        self.thrust = 0
        self.thrust_angle = 0
        self.body.angle = 0
        self.ignited = False

    def live(self):
        angle = self.thrust_angle / 180. * math.pi
        thrust_x = self.thrust * math.sin(angle)
        thrust_y = self.thrust * math.cos(angle)
        thrust_force = (thrust_x, thrust_y)
        if self.ignited:
            self.body.apply_force_at_local_point(thrust_force, self.thrust_origin)


    # thrust to weight ratio
    def twr(self):
        return -self.thrust / self.mass / self.space.gravity[1]
