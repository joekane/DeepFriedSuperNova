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

Pos = collections.namedtuple('Pos', 'x y')
layers = {}


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


def blank(x, y):
    x, y = Utils.to_camera_coordinates(x, y)
    # libtcod.console_put_char(consoles['entity_console'], x, y, ' ', libtcod.BKGND_NONE)
    draw_char(layers['entity_console'], x, y, ' ', None, libtcod.BKGND_NONE)


def draw_char(dest, x, y, char, color=None, flag=None):
    # LIBTCOD
    # libtcod.console_put_char_ex(dest, x, y, char, color, flag)

    #BEARLIB
    terminal.layer(dest)
    # TODO: CONVERT COLORS ON THEME IMPORT, INSTEAD OF INLINE (all render func)
    if color is not None:
        color = Utils.convert_color(color)
        terminal.color(color)
    terminal.put(x, y, char)


def draw_background(dest, x, y, color, flag=libtcod.BKGND_SET):
    # LIBTCOD
    # libtcod.console_set_char_background(dest, x, y, color, flag)
    # BEARLIB
    color = Utils.convert_color(color)
    terminal.bkcolor(color)
    terminal.put(x, y, terminal.pick(x,y, 0))


def set_foreground(dest, color):
    # LIBTCOD
    # libtcod.console_set_default_foreground(dest, color)
    # BEARLIB
    color = Utils.convert_color(color)
    terminal.color(color)


def set_background(dest, color):
    # LIBTCOD
    # libtcod.console_set_default_background(dest, color)
    # BEARLIB
    color = Utils.convert_color(color)
    terminal.bkcolor(color)


def print_line(dest, x, y, text): # bottom-right for BEARLIB
    # LIBTCOD
    # libtcod.console_print_ex(dest, x, y, flag, alignment, text)

    # BERALIB

    terminal.layer(dest)
    terminal.print_(x, y, text)


def print_rect(dest, x, y, w, h, text):
    # LIBTCOD
    # libtcod.console_print_rect(dest, x, y, w, h, text)

    # BEARLIB
    terminal.layer(dest)
    terminal.print_(x, y, "{0}[bbox={1}x{2}]".format(text, w, h))


def draw_rect(dest, x, y, w, h, frame=False, f_color=None, bk_color=None, title=None):
    terminal.layer(dest)

    if title:
        offset_x1 = ((w - len(title)) / 2) + 1
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
                elif (y1 == 0 and (offset_x1-1 > x1 or x1 > w - offset_x2)) or y1 == h - 1:
                    draw_char(dest, x1 + x, y1 + y, Constants.BOX_N)
    if title:
        print_line(dest, x + (w / 2), y, "[wrap={0}x{1}][align=center-center]{2}".format(w, h, title))


def draw_vert_line(x, y, length, color, target):
    # render the background first
    set_background(target, color)
    draw_rect(target, x, y, 1, length, False, libtcod.BKGND_SCREEN)


def draw_hoz_line(x, y, length, color, target):
    # render the background first
    set_background(target, color)
    draw_rect(target, x, y, length, 1, False, libtcod.BKGND_SCREEN)


""" EVERYTHING BELOW THIS LINE SHOULD MOVE TO A UI FILE """

def ui(): # TODO: These should all be in UI (Move UI bits to a UI.Component class or something)
    clear_layer(layers['panel_console'])
    clear_layer(layers['side_panel_console'])

    render_common()

    render_messages()

    render_status()

    render_stat_bars()


def draw_object(obj, visible=True):
    x, y = Utils.to_camera_coordinates(obj.x, obj.y)

    if visible:
        draw_char(layers['entity_console'], x, y, obj.char, obj.color,
                  libtcod.BKGND_NONE)
    else:
        draw_char(layers['entity_console'], x, y, obj.char, libtcod.darker_gray,
                  libtcod.BKGND_NONE)


def render_messages():
    print "DONT BE HERE"
    clear_layer(layers['messages'])
    y = 3 + Constants.MAP_CONSOLE_HEIGHT
    for (line, color) in GameState.get_msg_queue():
        if y < Constants.SCREEN_HEIGHT - 1:
            set_foreground(layers['messages'], color)
            # line_height = libtcod.console_get_height_rect(consoles['panel_console'], 0, 0, Constants.MSG_WIDTH, Constants.PANEL_HEIGHT - 3, line)
            line_height = 1
            print_rect(layers['messages'], Constants.MSG_X, y, Constants.MSG_WIDTH, line_height, line)

            y += line_height


def render_common():
    from Engine import Input

    pos = Pos(Constants.MAP_CONSOLE_WIDTH, 0)

    set_foreground(layers['side_panel_console'], libtcod.Color(0, 70, 140))

    """ LEVEL NUMBER """
    print_rect(layers['side_panel_console'], pos.x + 1, pos.y + 1, 17, 1, "Level 1".center(17, ' '))

    """ MOUSE X / Y """
    print_rect(layers['side_panel_console'], pos.x + 9, pos.y + 18, 17, 2,
                               "X: " + str(Input.mouse.cx) + "  \nY: " + str(Input.mouse.cy) + "  ")

    """ STATS """
    set_foreground(layers['panel_console'], libtcod.Color(175, 175, 255))
    player = GameState.get_player()

    print_line(layers['side_panel_console'], Constants.MAP_CONSOLE_WIDTH + 5, 18, str(player.fighter.base_str).rjust(3))
    print_line(layers['side_panel_console'], Constants.MAP_CONSOLE_WIDTH + 5, 19, str(player.fighter.base_def).rjust(3))
    print_line(layers['side_panel_console'], Constants.MAP_CONSOLE_WIDTH + 5, 20, str(player.fighter.base_agl).rjust(3))
    print_line(layers['side_panel_console'], Constants.MAP_CONSOLE_WIDTH + 5, 21, str(player.fighter.base_stm).rjust(3))
    print_line(layers['side_panel_console'], Constants.MAP_CONSOLE_WIDTH + 5, 22, str(player.fighter.base_skl).rjust(3))
    print_line(layers['side_panel_console'], Constants.MAP_CONSOLE_WIDTH + 5, 23, str(player.fighter.base_int).rjust(3))

    """ CONTROLS """
    print_line(layers['side_panel_console'], 59, 39, "Move:      NUMPAD")
    print_line(layers['side_panel_console'], 59, 40, "Fire:           F")
    print_line(layers['side_panel_console'], 59, 41, "Pickup:         G")
    print_line(layers['side_panel_console'], 59, 42, "Pop-Up Test:    B")
    print_line(layers['side_panel_console'], 59, 43, "Decend:         <")
    print_line(layers['side_panel_console'], 59, 44, "DEBUG:          X")


    """ DUNGEON NAME """
    pos = Pos(0, Constants.MAP_CONSOLE_HEIGHT)

    print_rect(layers['panel_console'], pos.x + 1, pos.y + 1, Constants.SCREEN_WIDTH - 19, 1,
               GameState.dungeon_name.center(57, ' '))
    # print_rect(layers['panel_console'], pos.x + 1, pos.y + 1, Constants.SCREEN_WIDTH - 19, 1,'TEST')


def render_status():
    # RENDER HEALTH BARS
    pos = Pos(Constants.MAP_CONSOLE_WIDTH + 1, 25)
    # CLEAR HP AREA / Status Area
    set_foreground(layers['side_panel_console'], libtcod.black)
    set_background(layers['side_panel_console'], libtcod.black)
    # draw_rect(layers['side_panel_console'], 1, 3, 17, 14, True, libtcod.BKGND_SET)
    # draw_rect(layers['side_panel_console'], pos.x, pos.y, 10, 9, True, libtcod.BKGND_SET)

    # print GameState.player.status

    num_of_status = 0
    inc = 0
    for st in GameState.player.status:
        if num_of_status == 9:
            set_background(layers['side_panel_console'], libtcod.black)
            set_foreground(layers['side_panel_console'], libtcod.Color(51, 51, 51))
            print_line(layers['side_panel_console'], pos.x, pos.y - 1 + inc,
                                  "...             ")  # + " (" + str(st[1]) + ")")
            return
        set_background(layers['side_panel_console'], libtcod.black)
        set_foreground(layers['side_panel_console'], st['color'])

        if Utils.is_mouse_in(pos.x, pos.y + inc, 17, 1):
            print_line(layers['side_panel_console'], pos.x, pos.y + inc, str(st['duration']) + " Turns")  # + " (" + str(st[1]) + ")")
        else:
            print_line(layers['side_panel_console'], pos.x, pos.y + inc, st['name'])  # + " (" + str(st[1]) + ")")
        num_of_status += 1
        inc += 1


def render_stat_bars():

    pos = Pos(Constants.MAP_CONSOLE_WIDTH + 4, 35)

    # SHOW PLAYER STAT BARS
    render_box_bar(pos.x, pos.y, 14, '', GameState.get_player().fighter.hp, GameState.get_player().fighter.base_max_hp,
                   libtcod.Color(178, 0, 45),
                   libtcod.Color(64, 0, 16), layers['side_panel_console'])
    render_box_bar(pos.x, pos.y + 1, 14, '', GameState.get_player().fighter.sp, GameState.get_player().fighter.base_max_sp,
                   libtcod.Color(0, 30, 255),
                   libtcod.Color(0, 10, 64), layers['side_panel_console'])
    render_box_bar(pos.x, pos.y + 2, 14, '', GameState.get_player().fighter.xp, 1000,  # TODO: will be NEXT_LVL_XP
                   libtcod.Color(255, 255, 0),
                   libtcod.Color(65, 65, 0), layers['side_panel_console'])

    # RENDER MONSTER HEALTH BARS
    temp_y = 3
    for object in GameState.get_visible_objects():
        if object.fighter and (object is not GameState.get_player()):  # and Fov.is_visible(obj=object)
            if temp_y < 17: # TODO: Make constant to scale UI
                render_box_bar(Constants.MAP_CONSOLE_WIDTH + 1, temp_y, 17, object.name, object.fighter.hp, object.fighter.max_hp,
                               libtcod.Color(0, 255, 0),
                               libtcod.Color(0, 64, 0),
                               layers['side_panel_console'])
                temp_y += 2


def render_box_bar(x, y, total_width, name, value, maximum, bar_color, back_color, target):
    # render a bar (HP, experience, etc). first calculate the width of the bar

    pos = Pos(Constants.MAP_CONSOLE_WIDTH + 4, 35)

    bar_width = int(float(value) / maximum * total_width)
    og_y = y
    height = 1
    offset_color = libtcod.Color(128, 128, 128)

    if name != '':
        set_background(target, libtcod.black)
        set_foreground(target, libtcod.Color(51, 51, 51))
        print_line(target, x, y, name)
        y += 1
        height += 1

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
        line = str(value) + "/" + str(maximum)
        set_foreground(target, 'white')
        print_line(target, x, y, line)


def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color, target):
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

