# -*- coding: utf-8 -*-
# *******************************************************
# * Copyright (C) 2016-2017 Joe Kane
# *
# * This file is part of 'Deep Fried Supernova"
# *
# * Deep Fried Supernova can not be copied and/or distributed without the express
# * permission of Joe Kane
# *******************************************************/

import collections
from bearlibterminal import terminal
import GameState
import Constants
import Utils
import libtcodpy as libtcod
from bltColor import bltColor as Color

Pos = collections.namedtuple('Pos', 'x y')
layers = {}

lorem_ipsum = \
    "[c=orange]Lorem[/c] ipsum dolor sit amet, consectetur adipisicing elit, " \
    "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. " \
    "[c=orange]Ut[/c] enim ad minim veniam, quis nostrud exercitation ullamco " \
    "laboris nisi ut aliquip ex ea commodo consequat. [c=orange]Duis[/c] aute " \
    "irure dolor in reprehenderit in voluptate velit esse cillum dolore eu " \
    "fugiat nulla pariatur. [c=orange]Excepteur[/c] sint occaecat cupidatat " \
    "non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."

# def initialize(map_console, entity_console, panel_console, side_panel_console, animation_console):
def initialize():
    global layers
    layers['map_console'] = 0
    layers['panel_console'] = 2
    layers['UI_Back'] = 1
    layers['side_panel_console'] = 2
    layers['entity_console'] = 3
    layers['messages'] = 4
    layers['animation_console'] = 5
    layers['overlay_console'] = 6


def clear_layer(layer, color='black'):
    terminal.bkcolor(color)
    terminal.layer(layer)
    terminal.clear_area(0, 0, Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT)


def draw_blank(x, y):
    x, y = Utils.to_camera_coordinates(x, y)
    # libtcod.console_put_char(consoles['entity_console'], x, y, ' ', libtcod.BKGND_NONE)
    draw_char(layers['entity_console'], x, y, ' ', None, libtcod.BKGND_NONE)

def set_foreground(dest, color):
    # LIBTCOD
    # libtcod.console_set_default_foreground(dest, color)
    # BEARLIB
    # TODO: Replace / Obsolete?
    #color = Utils.convert_color(color)
    #print color
    try:
        terminal.color(color)
    except:
        print "ERROR!"
        print color


def set_background(dest, color):
    # LIBTCOD
    # libtcod.console_set_default_background(dest, color)
    # BEARLIB
    # TODO: Replace / Obsolete?
    #color = Utils.convert_color(color)
    terminal.bkcolor(color)


def print_line(dest, x, y, text, f_color=None): # bottom-right for BEARLIB
    # LIBTCOD
    # libtcod.console_print_ex(dest, x, y, flag, alignment, text)

    # BERALIB

    if f_color:
        set_foreground(dest, f_color)

    terminal.layer(dest)

    terminal.puts(x, y, text)


def print_rect(dest, x, y, w, h, text):
    # LIBTCOD
    # libtcod.console_print_rect(dest, x, y, w, h, text)

    # BEARLIB
    terminal.layer(dest)
    terminal.print_(x, y, "{0}[bbox={1}x{2}]".format(text, w, h))


def draw_rect(dest, x, y, w, h, frame=False, f_color=None, bk_color=None, title=None):
    terminal.layer(dest)

    if title:
        if len(title) % 2 == 0:
            adj = 1
        else:
            adj = 2
        offset_x1 = ((w - len(title)) / 2) + adj
        offset_x2 = (w - len(title)) - (offset_x1 - 2)
    else:
        offset_x1 = w
        offset_x2 = 0

    for x1 in range(w):
        for y1 in range(h):
            terminal.color(bk_color)
            draw_char(dest, x1 + x, y1 + y, Utils.get_unicode(219))
            if frame:
                terminal.color(f_color)
                if (x1, y1) == (0, 0):
                    draw_char(dest, x1 + x, y1 + y, Constants.BOX_NW)
                elif (x1, y1) == (w - 1, 0):
                    draw_char(dest, x1 + x, y1 + y, Constants.BOX_NE)
                elif (x1, y1) == (0, h - 1):
                    draw_char(dest, x1 + x, y1 + y, Constants.BOX_SW)
                elif (x1, y1) == (w - 1, h - 1):
                    draw_char(dest, x1 + x, y1 + y, Constants.BOX_SE)
                elif x1 == 0 or x1 == w - 1:
                    draw_char(dest, x1 + x, y1 + y, Constants.BOX_E)
                elif  y1 == h - 1:
                    draw_char(dest, x1 + x, y1 + y, Constants.BOX_N)
    if title:
        print_line(dest, x, y, " " )
        print_line(dest, x, y, "{0}".format(title).center(w, ' '))


def draw_vert_line(x, y, length, color, target):
    # render the background first
    set_background(target, color)
    draw_rect(target, x, y, 1, length, False, libtcod.BKGND_SCREEN)


def draw_hoz_line(x, y, length, color, target):
    # render the background first
    set_background(target, color)
    draw_rect(target, x, y, length, 1, False, libtcod.BKGND_SCREEN)


def draw_object(obj, visible=True):
    x, y = Utils.to_camera_coordinates(obj.x, obj.y)

    if visible:
        if obj.fighter and Constants.HEALTH_BARS:
            char = 0x0398
            draw_char(layers['entity_console'], x, y, char, libtcod.red)

            percentage = (float(obj.fighter.hp) / float(obj.fighter.max_hp))*100

            if percentage <=10:
                char = 0x03B1
            elif percentage <=20:
                char = 0x00DF
            elif percentage <=30:
                char = 0x0393
            elif percentage <=40:
                char = 0x03C0
            elif percentage <=50:
                char = 0x03A3
            elif percentage <=60:
                char = 0x03C3
            elif percentage <=70:
                char = 0x00B5
            elif percentage <=80:
                char = 0x03C4
            elif percentage <=90:
                char = 0x03A6
            else:
                char = 0x0398
            draw_char(layers['entity_console'], x, y, char, 'green')

        draw_char(layers['entity_console'], x, y, obj.char, obj.color,
                  libtcod.BKGND_NONE)
    else:
        draw_char(layers['entity_console'], x, y, obj.char, 'darker gray',
                  libtcod.BKGND_NONE)


def draw_stat_bars():

    pos = Pos(Constants.MAP_CONSOLE_WIDTH + 4, 35)

    # SHOW PLAYER STAT BARS
    draw_box_bar(pos.x, pos.y, 14, '', GameState.get_player().fighter.hp, GameState.get_player().fighter.base_max_hp,
                 Color("178, 0, 45"),
                 Color("64, 0, 16"), layers['side_panel_console'])
    draw_box_bar(pos.x, pos.y + 1, 14, '', GameState.get_player().fighter.sp, GameState.get_player().fighter.base_max_sp,
                 Color("0, 30, 255"),
                 Color("0, 10, 64"), layers['side_panel_console'])
    draw_box_bar(pos.x, pos.y + 2, 14, '', GameState.get_player().fighter.xp, 1000,  # TODO: will be NEXT_LVL_XP
                   Color("255, 255, 0"),
                 Color("65, 65, 0"), layers['side_panel_console'])

    # RENDER MONSTER HEALTH BARS
    temp_y = 3
    for object in GameState.get_visible_objects():
        if object.fighter and (object is not GameState.get_player()):  # and Fov.is_visible(obj=object)
            if temp_y < 17: # TODO: Make constant to scale UI
                draw_box_bar(Constants.MAP_CONSOLE_WIDTH + 1, temp_y, 17, object.name, object.fighter.hp, object.fighter.max_hp,
                             Color("0, 255, 0"),
                             Color("0, 64, 0"),
                             layers['side_panel_console'])
                temp_y += 2


def draw_box_bar(x, y, total_width, name, value, maximum, bar_color, back_color, target):
    # render a bar (HP, experience, etc). first calculate the width of the bar

    pos = Pos(Constants.MAP_CONSOLE_WIDTH + 4, 35)

    bar_width = int(float(value) / maximum * total_width)
    og_y = y
    height = 1
    offset_color = Color("128, 128, 128")

    if name != '':
        set_background(target, libtcod.black)
        set_foreground(target, Color("51, 51, 51"))
        print_line(target, x, y, name)
        y += 1
        height += 1

    #print "Bar Colors"
    #print bar_color
    #print back_color

    ''' render MAX value '''
    # set_background(target, back_color-offset_color)
    # set_foreground(target, bar_color-offset_color)
    for x1 in range(x, x+total_width):
        draw_char(target, x1, y, Utils.get_unicode(219), back_color, libtcod.BKGND_SET)
        draw_char(target, x1, y, Utils.get_unicode(255), bar_color, libtcod.BKGND_SET)

    ''' render current value '''
    #set_background(target, back_color)
    # set_foreground(target, bar_color)
    for x1 in range(x, x+bar_width):
        draw_char(target, x1, y, Utils.get_unicode(219), back_color, libtcod.BKGND_SET)
        draw_char(target, x1, y, Utils.get_unicode(254), bar_color, libtcod.BKGND_SET)

    if Utils.is_mouse_in(x, og_y, total_width, height):
        terminal.composition(terminal.TK_OFF)
        line = str(value) + "/" + str(maximum)
        set_foreground(target, 'white')
        print_line(target, x, y, line)
        terminal.composition(terminal.TK_ON)


def draw_bar(x, y, total_width, name, value, maximum, bar_color, back_color, target):
    # render a bar (HP, experience, etc). first calculate the width of the bar
    bar_width = int(float(value) / maximum * total_width)

    # render the background first
    set_background(target, back_color)
    draw_rect(target, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

    # now render the bar on top
    set_background(target, bar_color)
    if bar_width > 0:
        draw_rect(target, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

    # finally, some centered text with the values
    set_foreground(target, libtcod.white)

    if name is not '':
        print_line(target, x + total_width / 2, y, name + ': ' + str(value) + '/' + str(maximum))


def draw_char(dest, x, y, char, color=None, flag=None, alpha=255, verbose=False):
    # LIBTCOD
    # libtcod.console_put_char_ex(dest, x, y, char, color, flag)

    #BEARLIB
    terminal.layer(dest)
    # TODO: CONVERT COLORS ON THEME IMPORT, INSTEAD OF INLINE (all render func)
    if color is not None:
        if verbose:
            print color
            print int(color)
            print color.getRGB()
        #color = Utils.convert_color(color, alpha)
        #print "Color: {0}".format(color)
        #print "In DrawChar Color: {0}".format(color)
        terminal.color(color)
    terminal.put(x, y, char)


def draw_char_ex(dest, x, y, dx, dy, char, color=None, flag=None, alpha=255):
    # LIBTCOD
    # libtcod.console_put_char_ex(dest, x, y, char, color, flag)

    # BEARLIB
    terminal.layer(dest)
    # TODO: CONVERT COLORS ON THEME IMPORT, INSTEAD OF INLINE (all render func)
    if color is not None:
        #color = Utils.convert_color(color, alpha)
        terminal.color(color)
    terminal.put_ext(x, y, dx, dy, char, None)


def draw_background(dest, x, y, color, flag=libtcod.BKGND_SET, verbose=False):
    # LIBTCOD
    # libtcod.console_set_char_background(dest, x, y, color, flag)
    # BEARLIB
    # TODO: Replace / Obsolete?
    #color = Utils.convert_color(color)
    if verbose:
        print color.getRGB()
    terminal.bkcolor(color)
    terminal.put(x, y, terminal.pick(x,y, 0))

