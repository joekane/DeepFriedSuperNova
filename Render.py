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

import libtcodpy as libtcod
import Constants
import Utils
import Fov
import GameState
import Map
import Themes

consoles = {}
gameState = None


def initialize(map_console, panel_console, side_panel_console):
    global consoles, gameState
    consoles['map_console'] = map_console
    consoles['panel_console'] = panel_console
    consoles['side_panel_console'] = side_panel_console


def clear_map():
    libtcod.console_clear(consoles['map_console'])


def render_tile(x, y):
    # NOT SURE IF WORKS!?!?!
    Fov.recompute()

    map = Map.current_map()

    # go through all tiles, and set their background color

    visible = Fov.is_visible(pos=(x, y))

    player = GameState.get_player()

    offset_value = int(Utils.distance_between(x, y, player.x, player.y)) * Constants.TORCH_RADIUS
    offset_color = libtcod.Color(offset_value, offset_value, offset_value)

    tile = map[x][y]

    if not visible:
        # if it's not visible right now, the player can only see it if it's explored
        if tile.explored:
            libtcod.console_put_char_ex(consoles['map_console'], x, y, tile.char,
                                        Themes.OUT_OF_FOV_COLOR, libtcod.BKGND_SET)
    else:
            libtcod.console_put_char_ex(consoles['map_console'], x, y, tile.char,
                                        tile.f_color - offset_color, libtcod.BKGND_SET)
            tile.explored = True


def full_map():
    libtcod.console_clear(consoles['map_console'])
    Fov.recompute()

    map = Map.current_map()
    player = GameState.get_player()

    Map.move_camera(player.x, player.y)

    camera_x, camera_y = Map.get_camera()
    # print "cx: " + str(camera_x) + " | cy: " + str(camera_y)

    # go through all tiles, and set their background color
    for y in range(Constants.MAP_CONSOLE_HEIGHT):
        for x in range(Constants.MAP_CONSOLE_WIDTH):
            map_x, map_y = (camera_x + x, camera_y + y)

            visible = Fov.is_visible(pos=(map_x, map_y))
            # print x, y

            wall = map[map_x][map_y].block_sight and map[map_x][map_y].blocked
            glass = not map[map_x][map_y].block_sight and map[map_x][map_y].blocked
            box = map[map_x][map_y].block_sight and not map[map_x][map_y].blocked
            wall_char = libtcod.CHAR_BLOCK1

            # floor_char = libtcod.CHAR_SUBP_DIAG
            floor_char = '.'

            wall_color = libtcod.red
            floor_color = libtcod.white

            player = GameState.get_player()


            tile = map[map_x][map_y]

            if not visible:
                # if it's not visible right now, the player can only see it if it's explored
                if tile.explored:
                    libtcod.console_put_char_ex(consoles['map_console'], x, y, tile.char,
                                                libtcod.Color(55, 55, 55), libtcod.BKGND_SET)

            else:
                dist = int(Utils.distance_between(map_x, map_y, player.x, player.y))

                offset_value = int((float(dist) / (Constants.TORCH_RADIUS + 2)  ) * 255)
                offset_value = max(0, min(offset_value, 64))
                offset_color = libtcod.Color(offset_value, offset_value, offset_value)

                libtcod.console_put_char_ex(consoles['map_console'], x, y, tile.char,
                                            tile.f_color - offset_color, libtcod.BKGND_SET)
                libtcod.console_set_char_background(consoles['map_console'], x, y,
                                                    tile.b_color - offset_color, flag=libtcod.BKGND_SET)

                tile.explored = True



def objects():
    for object in Map.get_objects():
        if object != GameState.get_player():
            object.draw()
    GameState.get_player().draw()


def ui():
    # prepare to render the GUI panel
    libtcod.console_set_default_background(consoles['panel_console'], libtcod.black)
    libtcod.console_clear(consoles['panel_console'])

    # prepare to render the GUI panel
    libtcod.console_set_default_background(consoles['side_panel_console'], libtcod.black)
    libtcod.console_clear(consoles['side_panel_console'])

    render_hoz_line(0, 0, Constants.SCREEN_WIDTH, libtcod.Color(30, 30, 30), consoles['panel_console'])

    # display names of objects under the mouse
    libtcod.console_set_default_foreground(consoles['panel_console'], libtcod.purple)
    libtcod.console_print_ex(consoles['panel_console'], 1, 1, libtcod.BKGND_NONE, libtcod.LEFT,
                             Utils.get_names_under_mouse())

    # print the game messages, one line at a time
    y = 1
    for (line, color) in GameState.get_msg_queue():
        libtcod.console_set_default_foreground(consoles['panel_console'], color)
        libtcod.console_print_ex(consoles['panel_console'], Constants.MSG_X, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
        y += 1

    # show the player's stats
    render_bar(1, 2, Constants.BAR_WIDTH, 'HP', GameState.get_player().fighter.hp,
               GameState.get_player().fighter.max_hp,
               libtcod.light_red,
               libtcod.darker_red,
               consoles['panel_console'])

    render_vert_line(0, 0, Constants.SCREEN_HEIGHT - Constants.PANEL_HEIGHT, libtcod.Color(30, 30, 30),
                     consoles['side_panel_console'])

    libtcod.console_print_ex(consoles['panel_console'], 1, 4, libtcod.BKGND_NONE, libtcod.LEFT, 'FPS ' +
                             str(libtcod.sys_get_fps()))
    libtcod.console_print_ex(consoles['panel_console'], 1, 5, libtcod.BKGND_NONE, libtcod.LEFT, '# ' +
                             str(GameState.get_player().x) + "/" + str(GameState.get_player().y))

    temp_y = 2

    for object in Map.get_objects():
        if object.fighter and Fov.is_visible(obj=object) and (object is not GameState.get_player()):
            render_bar(1, temp_y, 8, '', object.fighter.hp, object.fighter.max_hp, libtcod.dark_green,
                       libtcod.darker_red, consoles['side_panel_console'])
            if object in Utils.get_fighters_under_mouse():
                libtcod.console_set_default_foreground(consoles['side_panel_console'], libtcod.white)
            else:
                libtcod.console_set_default_foreground(consoles['side_panel_console'], libtcod.black)
            libtcod.console_print_ex(consoles['side_panel_console'], 1, temp_y, libtcod.BKGND_NONE, libtcod.LEFT,
                                     object.name)
            temp_y += 1


def update():
    # blit the contents of "panel" to the root console
    libtcod.console_blit(consoles['map_console'], 0, 0, Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT, 0, 0, 0)
    libtcod.console_blit(consoles['panel_console'], 0, 0, Constants.SCREEN_WIDTH, Constants.PANEL_HEIGHT, 0, 0,
                         Constants.PANEL_Y)
    libtcod.console_blit(consoles['side_panel_console'], 0, 0, 10, Constants.SCREEN_HEIGHT, 0, Constants.MAP_WIDTH, 0)


def blank(x, y):
    libtcod.console_put_char(consoles['map_console'], x, y, ' ', libtcod.BKGND_NONE)


def draw_object(obj, visible=True):
    x, y = Map.to_camera_coordinates(obj.x, obj.y)

    if visible:
        libtcod.console_put_char_ex(consoles['map_console'], x, y, obj.char, obj.color, libtcod.BKGND_NONE)
    else:
        libtcod.console_put_char_ex(consoles['map_console'], x, y, obj.char, libtcod.darker_gray,
                                    libtcod.BKGND_NONE)


def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color, target):
    # render a bar (HP, experience, etc). first calculate the width of the bar
    bar_width = int(float(value) / maximum * total_width)

    # render the background first
    libtcod.console_set_default_background(target, back_color)
    libtcod.console_rect(target, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

    # now render the bar on top
    libtcod.console_set_default_background(target, bar_color)
    if bar_width > 0:
        libtcod.console_rect(target, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

    # finally, some centered text with the values
    libtcod.console_set_default_foreground(target, libtcod.white)

    if name is not '':
        libtcod.console_print_ex(target, x + total_width / 2, y, libtcod.BKGND_NONE, libtcod.CENTER,
                                 name + ': ' + str(value) + '/' + str(maximum))


def render_vert_line(x, y, length, color, target):
    # render the background first
    libtcod.console_set_default_background(target, color)
    libtcod.console_rect(target, x, y, 1, length, False, libtcod.BKGND_SCREEN)


def render_hoz_line(x, y, length, color, target):
    # render the background first
    libtcod.console_set_default_background(target, color)
    libtcod.console_rect(target, x, y, length, 1, False, libtcod.BKGND_SCREEN)


def render_all():
    full_map()
    objects()
    ui()
    update()
