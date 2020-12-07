import pygame

FRAME_WIDTH = 1600
FRAME_HEIGHT = 900

TRACK_TARGET = None

GRAVITY = 600


# Small hack to convert chipmunk physics to pygame coordinates
def flipy(y):
    if TRACK_TARGET is None:
        return -y + FRAME_HEIGHT
    else:
        return -y + FRAME_HEIGHT / 2 + TRACK_TARGET.body.position.y


def track(target):
    global TRACK_TARGET
    TRACK_TARGET = target


def draw_background(screen):
    global TRACK_TARGET
    h = TRACK_TARGET.body.position.y
    f = 2000/h
    color = (254-f, 254-f, 254-f)
    dist = 700
    offs = h % dist
    for i in range(-1, 5):
        shift = offs + i*dist
        pygame.draw.rect(screen, color, (0, 0+shift, 1600, dist/2))
