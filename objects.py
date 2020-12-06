import pygame
import pymunk
from pymunk import Vec2d


def flipy(y):
    """Small hack to convert chipmunk physics to pygame coordinates"""
    return -y + 600


class Object():

    def __init__(self):
        self.body = None
        self.shape = None
        self.facecolor = "red"
        self.edgecolor = "blue"

    def draw(self, screen):
        pass


class Ball(Object):

    def __init__(self, space, x, y, radius=10, mass=10):
        super().__init__()
        moment = mass
        self.body = pymunk.Body(mass, moment)
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, radius, (0, 0))
        self.shape.friction = 0.5
        space.add(self.body, self.shape)

    def draw(self, screen):
        r = self.shape.radius
        v = self.body.position
        rot = self.body.rotation_vector
        p = int(v[0]), int(flipy(v[1]))
        p2 = p + Vec2d(rot.x, -rot.y) * r * 0.9
        p2 = int(p2.x), int(p2.y)
        pygame.draw.circle(screen, pygame.Color(self.edgecolor), p, int(r), 2)
        pygame.draw.line(screen, pygame.Color(self.facecolor), p, p2)


class Wall(Object):

    def __init__(self, space, p1, p2):
        super().__init__()
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


class HWall(Wall):

    def __init__(self, space, L, y):
        super().__init__(space, Vec2d(0, y), Vec2d(L, y))


class Poly(Object):

    def __init__(self, space, x, y, points, mass=10):
        super().__init__()
        moment = pymunk.moment_for_poly(mass, points)
        self.body = pymunk.Body(mass, moment)
        self.body.position = x, y
        self.shape = pymunk.Poly(self.body, points)
        self.shape.friction = 0.5
        space.add(self.body, self.shape)

    def draw(self, screen):
        ps = [p.rotated(self.body.angle) +
              self.body.position for p in self.shape.get_vertices()]
        ps.append(ps[0])
        for i, p in enumerate(ps):
            ps[i] = int(p.x), int(flipy(p.y))
        pygame.draw.lines(screen, pygame.Color(self.edgecolor), False, ps)


class Rectangle(Poly):

    def __init__(self, space, x, y, w, h, mass=10):
        points = [(-w/2, -h/2), (w/2, -h/2), (w/2, h/2), (-w/2, h/2)]
        super().__init__(space, x, y, points, mass)
