from objects import Poly
import math


class Rocket(Poly):

    def __init__(self, space, x, y, w=15, h=150, mass=10):
        points = [(-w/2, -h/2), (w/2, -h/2),
                  (w/2, h/2), (0, h/1.8), (-w/2, h/2)]
        super().__init__(space, x, y, points, mass)
        self.edgecolor = "red"

        self.thrust = 5000
        self.thrust_angle = 0

    def apply_force(self):
        thrust_x = self.thrust * math.sin(self.thrust_angle)
        thrust_y = self.thrust * math.cos(self.thrust_angle)
        thrust_force = (thrust_x, thrust_y)
        thrust_origin = (0, 0)
        self.body.apply_force_at_local_point(thrust_force, thrust_origin)
