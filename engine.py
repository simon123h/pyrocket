import math
import pygame
import pymunk
from settings import flipy


class Engine():

    def __init__(self):

        # the thrust of the engine
        self.thrust = 0
        self.ignited = False
        self.MAX_THRUST = 1e9
        self.MIN_THRUST = 0
        self.MAX_THRUST_CHANGE = 1e9

        # the angle of the thrust vector
        self.angle = 0
        self.MAX_ANGLE = math.pi / 4
        self.MAX_ANGLE_CHANGE = 1e9

        # graphics
        self.flame_img = pygame.image.load('res/flame.png').convert_alpha()

    def set_thrust(self, thrust):
        # TODO: mind MAX_CHANGE
        self.thrust = min(max(thrust, self.MIN_THRUST), self.MAX_THRUST)

    def set_angle(self, angle):
        # TODO: mind MAX_CHANGE
        self.angle = min(max(angle, -self.MAX_ANGLE), self.MAX_ANGLE)

    def draw(self, screen, pos, global_angle):
        if not self.ignited:
            return
        ll = 0.2 * math.sqrt(self.thrust)
        angle = global_angle - self.angle
        p1 = int(pos.x), int(flipy(pos.y))
        # thrust_end = pos + ll * \
        #     pymunk.Vec2d(math.sin(angle), -math.cos(angle))
        # p2 = int(thrust_end.x), int(flipy(thrust_end.y))
        # pygame.draw.lines(screen, pygame.Color("red"), False, [p1, p2], 2)
        w, h = self.flame_img.get_size()
        aux_img = pygame.Surface((w*2, h*2), pygame.SRCALPHA)
        aux_img.blit(self.flame_img, (w/2, h))
        aux_img = pygame.transform.rotozoom(
            aux_img, angle*180/math.pi, 0.01*ll)
        aux_rect = aux_img.get_rect()
        aux_rect.centerx, aux_rect.centery = p1
        screen.blit(aux_img, aux_rect)
