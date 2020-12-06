import pygame
import pymunk
from pymunk import Vec2d


def flipy(y):
    """Small hack to convert chipmunk physics to pygame coordinates"""
    return -y + 600


class Ball():

    def __init__(self, space, x, y):
        mass = 10
        moment = 10
        self.body = pymunk.Body(mass, moment)
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, 10, (0, 0))
        self.shape.friction = 0.4
        space.add(self.body, self.shape)
        self.color = "blue"
        self.linecolor = "red"

    def draw(self, screen):
        r = self.shape.radius
        v = self.body.position
        rot = self.body.rotation_vector
        p = int(v[0]), int(flipy(v[1]))
        p2 = p + Vec2d(rot.x, -rot.y) * r * 0.9
        p2 = int(p2.x), int(p2.y)
        pygame.draw.circle(screen, pygame.Color(self.color), p, int(r), 2)
        pygame.draw.line(screen, pygame.Color(self.linecolor), p, p2)


class Line():

    def __init__(self, space, p1, p2):
        self.shape = pymunk.Segment(space.static_body, p1, p2, 0.0)
        self.shape.friction = 0.99
        space.add(self.shape)

    def draw(self, screen):
        body = self.shape.body
        pv1 = body.position + self.shape.a.rotated(body.angle)
        pv2 = body.position + self.shape.b.rotated(body.angle)
        p1 = int(pv1.x), int(flipy(pv1.y))
        p2 = int(pv2.x), int(flipy(pv2.y))
        pygame.draw.lines(screen, pygame.Color(
            "lightgray"), False, [p1, p2])


class VLine(Line):

    def __init__(self, space, L, y):
        p1 = Vec2d(0, y)
        p2 = Vec2d(L, y)
        super().__init__(space, p1, p2)
