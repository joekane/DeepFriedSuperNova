import pygame
import libtcodpy as libtcod
import Constants
import Render



def initilize():
    global screen, font, surface
    screen = pygame.display.set_mode((Constants.SCREEN_WIDTH*16, Constants.SCREEN_HEIGHT*16))
    surface = pygame.display.get_surface().copy()
    font = load_font_tiles('.\Fonts\cp437_16x16_alpha.png', 16, 16)



def clear():
    global screen, surface
    #screen.blit(surface, (0, 0), special_flags=(pygame.BLEND_RGB_MAX))
    #pygame.display.flip()
    surface.fill((0, 0, 0, 0))
    pass


def clear_con():
    global screen, surface
    # screen.fill((0, 0, 0, 0))
    # screen.blit(surface, (0, 0), special_flags=(pygame.BLEND_RGB_MAX))
    # pygame.display.flip()

    pass






def draw_image(x , y, file_name='.\Images\cipher_warden.png', enlarge=False):
    global screen

    image = pygame.image.load(file_name).convert_alpha()
    if enlarge: image = pygame.transform.scale2x(image).convert_alpha()

    surface.blit(image, (x*16, y*16))
    #screen.blit(surface, (0, 0),  special_flags=(pygame.BLEND_RGBA_ADD))
    screen.blit(surface, (0, 0), special_flags=(pygame.BLEND_PREMULTIPLIED))
    # pygame.display.flip()


def load_font_tiles(filename, width, height):
    image = pygame.image.load(filename).convert_alpha()
    #image = inverted(image).convert_alpha()
    image = colorize(image, (255,0,0)).convert_alpha()
    image_width, image_height = image.get_size()
    tile_table = []
    for tile_x in range(0, image_width/width):
        line = []
        tile_table.append(line)
        for tile_y in range(0, image_height/height):
            rect = (tile_x*width, tile_y*height, width, height)
            line.append(image.subsurface(rect))
    return tile_table


def draw_font(x, y):
    global font
    for x, row in enumerate(font):
        for y, tile in enumerate(row):
            screen.blit(tile, (x * 16, y * 16))


def colorize(image, newColor):
    image = image.copy()
    image.fill(newColor[0:3] + (0,), None, pygame.BLEND_RGB_ADD)
    return image


def inverted(img):
    inv = pygame.Surface(img.get_rect().size, pygame.SRCALPHA)
    inv.fill((255,255,255,255))
    inv.blit(img, (0,0), None, pygame.BLEND_RGB_SUB)
    return inv


def callback(sdl_renderer):
    clear()
    pass



libtcod.sys_register_SDL_renderer(callback)