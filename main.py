import pygame
import sys
from pygame import sprite
from figures import *
from tools import load_image, Button, BlackRect, Palette
from PyQt5.QtWidgets import QColorDialog, QApplication, QFileDialog, QMainWindow

pygame.init()
pygame.display.set_caption('графический редактор')
size = width, height = 1400, 960
background = pygame.Surface(size)
main_screen = pygame.display.set_mode(size)
draw_group = sprite.Group()
tool_group = sprite.Group()
markers = sprite.Group()


def update_screen():
    main_screen.blit(background, (0, 0))
    draw_group.draw(main_screen)
    tool_group.draw(main_screen)
    markers.draw(main_screen)
    pygame.display.flip()


def tool_setting(c, im, pos, t=False):
    def func(*args):
        global figure
        figure = c
        if drawing:
            figure_arr.pop()
            figure_arr.append(c(draw_group))
    b = Button(tool_group, load_image(fr'tools\{im}.bmp', pygame.Color((255, 255, 255))), func, pos, type=mode)
    if t:
        mode.move(b.rect)


def new_color(*args):
    color_new = QColorDialog.getColor().getRgb()
    if not color_new:
        return
    global color
    color.update(color=pygame.Color(color_new[:-1]))
    print(color_new)


def update_color(pal):
    global color
    color = pal


def save(*args):
    try:
        f_name = QFileDialog.getSaveFileName(
            QMainWindow(), 'выбрать файл', '', "Картинка (*.png *.xpm *.jpg *.bmp)")[0]
        screen = pygame.Surface((width, height - 60))
        screen.blit(main_screen, (0, -60))
        pygame.image.save(screen, f_name)
    except Exception:
        pass


def open_im(*args):
    try:
        f_name = QFileDialog.getOpenFileName(
            QMainWindow(), 'выбрать файл', '', "Картинка (*.png *.xpm *.jpg *.bmp)")[0]
        global size, width, height, main_screen, background
        screen = pygame.image.load(f_name)
        rect_im = screen.get_rect()
        size = width, height = max(width, rect_im.w), max(height, rect_im.h + 60)
        main_screen = pygame.display.set_mode(size)
        background = pygame.Surface(size)
        background.blit(screen, (0, 60))
    except Exception:
        pass


def tool_init():
    global back
    back = sprite.Sprite(tool_group)
    back.image = pygame.Surface((width, 60), pygame.SRCALPHA)
    back.image.fill((255, 255, 255))
    back.rect = back.image.get_rect()

    Button(tool_group, load_image(fr'tools\save.jpg'), save, (5, 5))
    Button(tool_group, load_image(fr'tools\open.png'), open_im, (60, 5))

    Button(tool_group, load_image(fr'tools\palette.png'), new_color, (width - 80, 0))
    for i in range(5, 36, 30):
        for j in range(width - 370, width - 100, 30):
            Palette(tool_group, (j, i), update_color, col_mark, pygame.Color('red'), 20)
    tool_group.update(event=pygame.event.Event(pygame.MOUSEBUTTONDOWN, button=1, pos=(width - 369, 6)))
    tool_setting(Rect, 'rect', (width - 500, 5), True)
    tool_setting(Circle, 'circle', (width - 440, 5))
    tool_setting(Line, 'line', (width - 560, 5))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    back = None
    clock = pygame.time.Clock()
    rect_col = pygame.Color('green')

    color = None
    mode = BlackRect(markers)
    col_mark = BlackRect(markers)
    tool_init()

    figure = Rect
    start_pos = None
    figure_arr = [figure(draw_group)]
    rect = Rect(draw_group)
    copy = None
    old = None
    tool = None

    print(*map(lambda x: x.rect, tool_group))
    running = True
    drawing = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not pygame.mouse.get_focused():
                continue
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_z and\
                    len(figure_arr) > 1 and event.mod & pygame.KMOD_CTRL:
                figure_arr.pop(-2).kill()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_c and\
                    event.mod & pygame.KMOD_CTRL:
                r = rect.rect
                if r.w <= 2 or r.h <= 2:
                    continue
                copy = pygame.Surface((r.w - 2, r.h - 2))
                copy.blit(main_screen, (-r.x - 1, -r.y - 1))
                rect.kill()
                rect = Rect(draw_group)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_v and\
                    event.mod & pygame.KMOD_CTRL and copy:
                if figure_arr and drawing:
                    old = figure_arr.pop()
                figure_arr.append(sprite.Sprite(draw_group))
                pos = pygame.mouse.get_pos()
                figure_arr[-1].image = copy
                figure_arr[-1].rect = copy.get_rect()
                figure_arr[-1].rect.x = pos[0]
                figure_arr[-1].rect.y = pos[1]
                copy = None
                rect.kill()
                rect = Rect(draw_group)
                if old is not None:
                    figure_arr.append(old)
                    old = None

            elif back.rect.collidepoint(pygame.mouse.get_pos()):
                tool_group.update(event=event)
            elif not figure_arr:
                continue
            elif figure_arr[-1] and drawing:
                figure_arr[-1].update(event=event, btn=1, color=color.color)
                if figure_arr[-1].end:
                    figure_arr.append(figure(draw_group))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    print(event)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button != 3:
                    rect.kill()
                    rect = Rect(draw_group)
                rect.update(event=event, btn=3)
        update_screen()
