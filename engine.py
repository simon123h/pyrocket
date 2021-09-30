import math
import pygame


class Engine():

    def __init__(self):

        # the thrust of the engine
        self.ignited = False
        self.MAX_THRUST = 3.6e8
        self.MIN_THRUST = 3.6e7
        self.MAX_THRUST_CHANGE = 1e7
        self.thrust = self.MAX_THRUST
        # amout of fuel consumed per thrust generated
        self.FUEL_CONSUMPTION = 1

        # the angle of the thrust vector
        self.angle = 0
        self.MAX_ANGLE = math.pi / 4
        self.MAX_ANGLE_CHANGE = 1e9

        # graphics
        self.flame_img = pygame.image.load('res/flame.png').convert_alpha()

    def set_thrust(self, thrust):
        thrust = min(thrust, self.thrust + self.MAX_THRUST_CHANGE)
        thrust = max(thrust, self.thrust - self.MAX_THRUST_CHANGE)
        thrust = min(thrust, self.MAX_THRUST)
        thrust = max(thrust, self.MIN_THRUST)
        self.thrust = thrust

    def increase_thrust(self, dthrust):
        self.set_thrust(self.thrust + dthrust)

    def set_angle(self, angle):
        angle = min(angle, self.angle + self.MAX_ANGLE_CHANGE)
        angle = max(angle, self.angle - self.MAX_ANGLE_CHANGE)
        angle = min(angle, self.MAX_ANGLE)
        angle = max(angle, -self.MAX_ANGLE)
        self.angle = angle

    def increase_angle(self, dangle):
        self.set_angle(self.angle + dangle)

    def ignite(self):
        self.ignited = True

    def cut_off(self):
        self.ignited = False

    def draw(self, game, pos, global_angle):
        if not self.ignited:
            return
        ll = 0.2 * math.sqrt(self.thrust/3e4)
        angle = global_angle - self.angle
        p1 = game.pos2screen(pos)
        # thrust_end = pos + ll * \
        #     pymunk.Vec2d(math.sin(angle), -math.cos(angle))
        # p2 = game.pos2screen(thrust_end)
        # pygame.draw.lines(game.screen, pygame.Color("red"), False, [p1, p2], 2)
        w, h = self.flame_img.get_size()
        aux_img = pygame.Surface((w*2, h*2), pygame.SRCALPHA)
        aux_img.blit(self.flame_img, (w/2, h))
        aux_img = pygame.transform.rotozoom(
            aux_img, angle*180/math.pi, 0.01*ll)
        aux_rect = aux_img.get_rect()
        aux_rect.centerx, aux_rect.centery = p1
        game.screen.blit(aux_img, aux_rect)
