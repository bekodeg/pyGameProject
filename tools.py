import os
import sys
import pygame

pygame.init()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class BlackRect(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.image = pygame.Surface((0, 0), pygame.SRCALPHA)

    def move(self, rect):
        self.rect = pygame.Rect(rect.x - 2, rect.y - 2, rect.w + 4, rect.h + 4)
        self.image = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
        pygame.draw.rect(self.image, pygame.Color('black'),
                         pygame.Rect(0, 0, self.rect.w, self.rect.h), 1)


class Button(pygame.sprite.Sprite):
    def __init__(self, group, image, func, pos, type=None):
        super().__init__(group)
        self.image = image
        self.func = func
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.type = type

    def update(self, **kwargs):
        event = kwargs.get('event', None)
        if event is None:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1\
                and self.rect.collidepoint(event.pos):
            self.func(self)
            if self.type is not None:
                self.type.move(self.rect)


class Palette(Button):
    def __init__(self, group, pos, func, type, color=pygame.Color((255, 255, 255)), size=15):
        image = pygame.Surface((size, size), pygame.SRCALPHA)
        image.fill(color)
        super().__init__(group, image, func, pos, type=type)
        self.color = color

    def update(self, **kwargs):
        color = kwargs.get('color', None)
        if color is not None:
            self.color = color
            self.image.fill(color)
        super().update(**kwargs)
