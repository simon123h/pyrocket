import math
import pygame

class Engine():

    def __init__(self):

        # the thrust of the engine
        self.thrust = 0
        self.ignited = False
        self.MAX_THRUST = 1e5
        self.MIN_THRUST = 1e3
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

    def increase_thrust(self, dthrust):
        self.set_thrust(self.thrust + dthrust)

    def set_angle(self, angle):
        # TODO: mind MAX_CHANGE
        self.angle = min(max(angle, -self.MAX_ANGLE), self.MAX_ANGLE)

    def increase_angle(self, dangle):
        self.set_angle(self.angle + dangle)

    def draw(self, game, pos, global_angle):
        if not self.ignited:
            return
        ll = 0.2 * math.sqrt(self.thrust)
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
