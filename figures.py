import pygame
from pygame import sprite
from math import sqrt
pygame.init()


class Figure(sprite.Sprite):
    def __init__(self, group, s=1, color=None,  *args, **kwargs):
        print('figure_created')
        super().__init__(group)
        self.end = False
        self.drawing = False
        if color is None:
            self.color = pygame.Color(255, 255, 255)
        else:
            self.color = color
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.s = s
        self.image = pygame.Surface((0, 0), pygame.SRCALPHA)

    def draw(self):
        pass

    def update(self, **kwargs):
        pass

    def __dict__(self):
        col = self.color
        res = dict()
        res['s'] = self.s
        res['color'] = self.color
        res['rect'] = self.rect
        return res


class Rect(Figure):
    def __init__(self, group, *args, **kwargs):
        super().__init__(group, *args, **kwargs)
        self.start_pos = None

    def draw(self):
        self.image = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
        pygame.draw.rect(self.image, self.color,
                         pygame.Rect(0, 0, self.rect.w, self.rect.h),
                         self.s)

    def resize(self, pos):
        x, y = self.start_pos
        w = pos[0] - x
        if w >= 0:
            self.rect.w = w
            self.rect.x = x
        else:
            self.rect.w = -w
            self.rect.x = pos[0]
        h = pos[1] - y
        if h >= 0:
            self.rect.h = h
            self.rect.y = y
        else:
            self.rect.h = -h
            self.rect.y = pos[1]
        self.draw()

    def update(self, **kwargs):
        self.color = kwargs.get('color', self.color)
        event = kwargs.get('event', None)
        if event is None:
            return
        btn = kwargs.get('btn', None)
        if event is None:
            btn = 1
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == btn:
            pos = event.pos
            self.drawing = True
            self.start_pos = pos
            self.resize(pos)
        if self.start_pos is None:
            return
        elif event.type == pygame.MOUSEMOTION and self.drawing:
            pos = event.pos
            self.resize(pos)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == btn:
            pos = event.pos
            self.resize(pos)
            self.drawing = False
            self.end = True


class Circle(Figure):
    def __init__(self, group, *args, **kwargs):
        super().__init__(group, *args, **kwargs)
        self.start_pos = None

    def draw(self):
        self.image = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, self.color, pygame.Rect(0, 0, self.rect.w, self.rect.h), self.s)

    def resize(self, pos):
        x, y = self.start_pos
        x1 = (pos[0] - x)
        y1 = (pos[1] - y)
        d = sqrt(x1 ** 2 + y1 ** 2)
        self.rect.w = d
        self.rect.h = d
        self.rect.x = (x1 / 2 + x) - (d / 2)
        self.rect.y = (y1 / 2 + y) - (d / 2)
        self.draw()

    def update(self, **kwargs):
        self.color = kwargs.get('color', self.color)
        event = kwargs.get('event', None)
        if event is None:
            return
        btn = kwargs.get('btn', None)
        if event is None:
            btn = 1
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == btn:
            pos = event.pos
            self.drawing = True
            self.start_pos = pos
            self.image = pygame.Surface((0, 0), pygame.SRCALPHA)
            print('ok')
        if self.start_pos is None:
            return
        elif event.type == pygame.MOUSEMOTION and self.drawing:
            pos = event.pos
            self.resize(pos)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == btn:
            pos = event.pos
            self.resize(pos)
            self.drawing = False
            self.end = True

