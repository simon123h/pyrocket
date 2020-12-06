import math
from objects import Poly, flipy
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
        self.flame_img = pygame.image.load('res/flame.png').convert_alpha()

        self.w = w
        self.h = h
        self.thrust_origin = pymunk.Vec2d(0, -h/2)

        self.thrust = self.mass * abs(self.space.gravity[1])
        self.thrust_angle = 0
        self.body.angle = 0
        self.ignited = True

        self.sas_mode = "OFF"

    def live(self):
        angle = self.thrust_angle
        thrust_x = self.thrust * math.sin(angle)
        thrust_y = self.thrust * math.cos(angle)
        thrust_force = (thrust_x, thrust_y)
        if self.ignited:
            self.body.apply_force_at_local_point(
                thrust_force, self.thrust_origin)

    def autopilot(self, dt=1):
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
            # control thrust angle
            # self.thrust_angle = -abs(angular_velocity)*angle*0.02
            sas_aggr = dt * 120. # how aggressive is SAS?
            self.thrust_angle = 0
            self.thrust_angle -= abs(velocity.x)*angle*0.2 * sas_aggr
            self.thrust_angle -= angular_velocity*2
            self.thrust_angle += 0.006*velocity.x * sas_aggr
            self.thrust_angle = min(self.thrust_angle, math.pi/4)
            self.thrust_angle = max(self.thrust_angle, -math.pi/4)
            # control absolute thrust
            self.thrust = self.mass * abs(self.space.gravity[1])
            self.thrust -= self.mass * velocity.y * sas_aggr
            self.thrust = max(self.thrust, 0)
            self.thrust /= max(abs(math.cos(self.thrust_angle-self.body.angle)), 0.7)

        elif self.sas_mode == "land":
            pass

    # thrust to weight ratio
    def twr(self):
        return -self.thrust / self.mass / self.space.gravity[1]

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
        fins = [pymunk.Vec2d(p).rotated(self.body.angle) + self.body.position for p in fins]
        for i, p in enumerate(fins):
            fins[i] = int(p.x), int(flipy(p.y))
        pygame.draw.lines(screen, pygame.Color(self.edgecolor), False, fins, 2)
        fins = [(w/2, -h/2.1), (w*1.4, -h/2.1), (w/2, -h/5), (w/2, -h/2.1)]
        fins = [pymunk.Vec2d(p).rotated(self.body.angle) + self.body.position for p in fins]
        for i, p in enumerate(fins):
            fins[i] = int(p.x), int(flipy(p.y))
        pygame.draw.lines(screen, pygame.Color(self.edgecolor), False, fins, 2)
        # flame
        if self.ignited:
            thrust_pos = self.body.position + \
                self.thrust_origin.rotated(self.body.angle)
            ll = 0.2 * math.sqrt(self.thrust)
            angle = -self.thrust_angle + self.body.angle
            p1 = int(thrust_pos.x), int(flipy(thrust_pos.y))
            thrust_end = thrust_pos + ll * \
                pymunk.Vec2d(math.sin(angle), -math.cos(angle))
            p2 = int(thrust_end.x), int(flipy(thrust_end.y))
            pygame.draw.lines(screen, pygame.Color("red"), False, [p1, p2], 2)
            w, h = self.flame_img.get_size()
            aux_img = pygame.Surface((w*2, h*2), pygame.SRCALPHA)
            aux_img.blit(self.flame_img, (w/2, h))
            aux_img = pygame.transform.rotozoom(aux_img, angle*180/math.pi, 0.01*ll)
            aux_rect = aux_img.get_rect()
            aux_rect.centerx, aux_rect.centery = p1
            screen.blit(aux_img, aux_rect)
