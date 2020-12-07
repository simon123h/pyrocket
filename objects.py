import pygame
import pymunk
from pymunk import Vec2d


class Object():

    def __init__(self):
        self.body = None
        self.shape = None
        self.facecolor = "red"
        self.edgecolor = "blue"

    # update the external forces
    def update_forces(self):
        pass

    # draw the object on a game's screen
    def draw(self, game):
        pass


class Ball(Object):

    def __init__(self, space, x, y, radius=10, mass=10):
        super().__init__()
        moment = mass
        self.body = pymunk.Body(mass, moment)
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, radius, (0, 0))
        self.shape.friction = 0.8
        space.add(self.body, self.shape)

    def draw(self, game):
        r = self.shape.radius
        v = self.body.position
        rot = self.body.rotation_vector
        p = game.pos2screen(v)
        p2 = p + Vec2d(rot.x, -rot.y) * r * 0.9
        p2 = int(p2.x), int(p2.y)
        pygame.draw.circle(game.screen, pygame.Color(
            self.edgecolor), p, int(r), 2)
        pygame.draw.line(game.screen, pygame.Color(self.facecolor), p, p2)


class Wall(Object):

    def __init__(self, space, p1, p2):
        super().__init__()
        self.body = space.static_body
        self.shape = pymunk.Segment(self.body, p1, p2, 0.0)
        self.shape.friction = 0.99
        space.add(self.shape)

    def draw(self, game):
        pv1 = self.body.position + self.shape.a.rotated(self.body.angle)
        pv2 = self.body.position + self.shape.b.rotated(self.body.angle)
        p1 = game.pos2screen(pv1)
        p2 = game.pos2screen(pv2)
        pygame.draw.lines(game.screen, pygame.Color(
            "black"), False, [p1, p2], 2)


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
        self.shape.friction = 0.8
        space.add(self.body, self.shape)

    def draw(self, game):
        ps = [p.rotated(self.body.angle) +
              self.body.position for p in self.shape.get_vertices()]
        ps.append(ps[0])
        for i, p in enumerate(ps):
            ps[i] = game.pos2screen(p)
        pygame.draw.lines(game.screen, pygame.Color(
            self.edgecolor), False, ps, 2)


class Rectangle(Poly):

    def __init__(self, space, x, y, w, h, mass=10):
        points = [(-w/2, -h/2), (w/2, -h/2), (w/2, h/2), (-w/2, h/2)]
        super().__init__(space, x, y, points, mass)
