'''
/*******************************************************
 * Copyright (C) 2016-2017 Joe Kane
 *
 * This file is part of 'Deep Fried Supernova"
 *
 * Deep Fried Supernova can not be copied and/or distributed without the express
 * permission of Joe Kane
 *******************************************************/
'''

import time

from bearlibterminal import terminal

import Constants
import Utils
import libtcodpy as libtcod
import Render
import GameState
from bltColor import bltColor as Color


def follow_line(source, target, projectile='-', end_tile='*', color=libtcod.yellow):

    if Constants.ANIMATE_ON:
        line = Utils.get_line((source.x, source.y), (target.x, target.y))
        for loc in line:
            Render.clear_layer(Render.layers['animation_console'])
            map_x, map_y = loc

            GameState.render_all()

            x, y = Utils.to_camera_coordinates(map_x, map_y)

            if (x, y) == line[-1]:
                Render.draw_char(Render.layers['animation_console'], x, y, end_tile, color)

            else:
                Render.draw_char(Render.layers['animation_console'], x, y, projectile, color)

            terminal.refresh()
            # time.sleep(0.01325) # 0.01325
        Render.clear_layer(Render.layers['animation_console'])


def explosion(target, radius=3):
    if Constants.ANIMATE_ON:
        x, y = Utils.to_camera_coordinates(target.x, target.y)
        for r in range(0, radius):
            Render.render_all()
            if r >= 0:
                Render.draw_char(0, x, y, 'X', libtcod.red, libtcod.BKGND_NONE)
                print "1"
            if r >= 1:
                Render.draw_char(0, x - 1, y, 'X', libtcod.red, libtcod.BKGND_NONE)
                Render.draw_char(0, x + 1, y, 'X', libtcod.red, libtcod.BKGND_NONE)
                Render.draw_char(0, x, y - 1, 'X', libtcod.red, libtcod.BKGND_NONE)
                Render.draw_char(0, x, y + 1, 'X', libtcod.red, libtcod.BKGND_NONE)
                print "2"
            if r >= 2:
                Render.draw_char(0, x - 2, y, 'X', libtcod.red, libtcod.BKGND_NONE)
                Render.draw_char(0, x + 2, y, 'X', libtcod.red, libtcod.BKGND_NONE)
                Render.draw_char(0, x, y - 2, 'X', libtcod.red, libtcod.BKGND_NONE)
                Render.draw_char(0, x, y + 2, 'X', libtcod.red, libtcod.BKGND_NONE)

                Render.draw_char(0, x + 1, y + 1, 'X', libtcod.red, libtcod.BKGND_NONE)
                Render.draw_char(0, x - 1, y + 1, 'X', libtcod.red, libtcod.BKGND_NONE)
                Render.draw_char(0, x + 1, y - 1, 'X', libtcod.red, libtcod.BKGND_NONE)
                Render.draw_char(0, x - 1, y - 1, 'X', libtcod.red, libtcod.BKGND_NONE)
                print "3"
            libtcod.console_flush()
            print "sleep"
            time.sleep(0.025)


def inspect_banner(x, y, banner_text, new_animation=True):

    animation_console = Render.layers['animation_console']
    # animation_console = 0

    # print "printing"

    color = libtcod.light_blue
    libtcod.console_set_default_foreground(animation_console, libtcod.lighter_blue)
    libtcod.console_set_default_background(animation_console, libtcod.green)
    libtcod.console_set_background_flag(animation_console, libtcod.BKGND_MULTIPLY)

    length = len(banner_text)

    back = libtcod.green

    Render.draw_char(animation_console, x + 1, y, libtcod.CHAR_HLINE, color, back)

    Render.draw_char(animation_console, x + 2, y - 1, libtcod.CHAR_NW, color, back)
    Render.draw_char(animation_console, x + 2, y, libtcod.CHAR_TEEW, color, back)
    Render.draw_char(animation_console, x + 2, y + 1, libtcod.CHAR_SW, color, back)

    if new_animation:
        for z in range(length):

            Render.draw_char(animation_console, x + z + 3, y - 1, libtcod.CHAR_HLINE, color, back)
            Render.draw_char(animation_console, x + z + 3, y, banner_text[z], color, back)
            Render.draw_char(animation_console, x + z + 3, y + 1, libtcod.CHAR_HLINE, color, back)
            # Render.update_animations()
            libtcod.console_flush()
            # time.sleep(0.05)
    else:
        for z in range(length):
            Render.draw_char(animation_console, x + z + 3, y - 1, libtcod.CHAR_HLINE, color, back)
            Render.draw_char(animation_console, x + z + 3, y, ' ', color, back)
            Render.draw_char(animation_console, x + z + 3, y + 1, libtcod.CHAR_HLINE, color, back)

    Render.draw_char(animation_console, x + 3 + length, y - 1, libtcod.CHAR_NE, color, back)
    Render.draw_char(animation_console, x + 3 + length, y, libtcod.CHAR_VLINE, color, back)
    Render.draw_char(animation_console, x + 3 + length, y + 1, libtcod.CHAR_SE, color, back)

    libtcod.console_set_default_foreground(animation_console, libtcod.lightest_blue)
    Render.print_line(animation_console, x + 3, y, libtcod.BKGND_NONE, libtcod.LEFT, banner_text)
    libtcod.console_flush()



def large_button(x, y, text, hover, length=None, target=0):

    animation_console = target

    if hover:
        color = Color('light azure')
    else:
        color = Color('azure')

    if length is None:
        length = len(text)
    text = text.center(length)

    x = x - ((length + 2) / 2)
    base_color = color
    value = 40
    adj = Color("{0},{0},{0}".format(value))
    color1 = base_color - adj - adj
    color2 = base_color - adj
    color3 = base_color


    #Render.draw_char(animation_console, x + 1, y, libtcod.CHAR_HLINE, color, libtcod.BKGND_NONE)

    Render.draw_char(animation_console, x, y - 1, Constants.BOX_NW, color1, libtcod.BKGND_NONE)
    Render.draw_char(animation_console, x, y, Constants.BOX_W, color2, libtcod.BKGND_NONE)
    Render.draw_char(animation_console, x, y + 1, Constants.BOX_SW, color3, libtcod.BKGND_NONE)

    for z in range(length):
        Render.draw_char(animation_console, x + z + 1, y - 1, Constants.BOX_S, color1, libtcod.BKGND_NONE)
        Render.draw_char(animation_console, x + z + 1, y, text[z], color2, libtcod.BKGND_NONE)
        Render.draw_char(animation_console, x + z + 1, y + 1, Constants.BOX_S, color3, libtcod.BKGND_NONE)

    Render.draw_char(animation_console, x + 1 + length, y - 1, Constants.BOX_NE, color1, libtcod.BKGND_NONE)
    Render.draw_char(animation_console, x + 1 + length, y, Constants.BOX_W, color2, libtcod.BKGND_NONE)
    Render.draw_char(animation_console, x + 1 + length, y + 1, Constants.BOX_SE, color3, libtcod.BKGND_NONE)



