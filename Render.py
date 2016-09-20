# *******************************************************
# * Copyright (C) 2016-2017 Joe Kane
# *
# * This file is part of 'Deep Fried Supernova"
# *
# * Deep Fried Supernova can not be copied and/or distributed without the express
# * permission of Joe Kane
# *******************************************************/


import libtcodpy as libtcod
import Constants
import Utils
import Fov
import GameState
import Map
import Themes
import UI

consoles = {}
gameState = None


def initialize(map_console, entity_console, panel_console, side_panel_console, animation_console):
    global consoles, gameState
    consoles['map_console'] = map_console
    consoles['panel_console'] = panel_console
    consoles['side_panel_console'] = side_panel_console
    consoles['entity_console'] = entity_console
    consoles['animation_console'] = animation_console

    UI.load_from_xp(0, 0, 'Side_panel', consoles['side_panel_console'])
    UI.load_from_xp(0, 0, 'Panel', consoles['panel_console'])

    # libtcod.console_set_default_background(consoles['animation_console'], libtcod.Color(255,255,255))
    # libtcod.console_set_background_flag(consoles['animation_console'], libtcod.BKGND_MULTIPLY)


def clear_map():
    libtcod.console_clear(consoles['map_console'])


def full_map():
    import Noise

    if Fov.recompute():
        map = Map.current_map()
        player = GameState.get_player()
        Map.move_camera(player.x, player.y)
        camera_x, camera_y = Map.get_camera()
        for y in range(Constants.MAP_CONSOLE_HEIGHT):
            for x in range(Constants.MAP_CONSOLE_WIDTH):
                map_x, map_y = (camera_x + x, camera_y + y)
                tile = map[map_x][map_y]
                visible = Fov.is_visible(pos=(map_x, map_y))

                if Constants.DEBUG:
                    offset_color = libtcod.Color(0,0,0)
                    libtcod.console_put_char_ex(consoles['map_console'], x, y, tile.char,
                                                tile.f_color - offset_color, libtcod.BKGND_SET)
                    libtcod.console_set_char_background(consoles['map_console'], x, y,
                                                        tile.b_color - offset_color, flag=libtcod.BKGND_SET)
                else:
                    if not visible:
                        if tile.explored:
                            if tile.blocked:
                                char = 206
                            else:
                                char = '.'
                            libtcod.console_put_char_ex(consoles['map_console'], x, y, char,
                                                        Themes.OUT_OF_FOV_COLOR, libtcod.BKGND_SET)

                    else:
                        offset_color = get_offset_color(map_x, map_y)
                        libtcod.console_put_char_ex(consoles['map_console'], x, y, tile.char,
                                                    tile.f_color - offset_color, libtcod.BKGND_SET)
                        libtcod.console_set_char_background(consoles['map_console'], x, y,
                                                            tile.b_color - offset_color, flag=libtcod.BKGND_SET)
                        tile.explored = True


def object_clear():
    for obj in Map.get_all_objects():
        obj.clear()


def objects():
    libtcod.console_clear(consoles['entity_console'])
    for object in Map.get_all_objects():
        if object != GameState.get_player():
            object.draw()
    GameState.get_player().draw()


def ui():
    # prepare to render the GUI panel
    # libtcod.console_set_default_background(consoles['panel_console'], libtcod.black)
    # libtcod.console_clear(consoles['panel_console'])

    # print the Side Panel, with auto-wrap
    # libtcod.console_set_default_foreground(consoles['panel_console'], Constants.UI_Fore)
    # libtcod.console_set_default_background(consoles['panel_console'], Constants.UI_Back)
    #libtcod.console_print_frame(consoles['panel_console'], 0, 0,
    #                            Constants.SCREEN_WIDTH,
    #                            Constants.PANEL_HEIGHT,
    #                            clear=True,
    #                            flag=libtcod.BKGND_SET,
    #                            fmt=None)

    render_common()

    render_messages()

    render_status()

    render_stat_bars()



    # DEBUG STUFF
    # libtcod.console_print_ex(consoles['panel_console'], 1, 4, libtcod.BKGND_NONE, libtcod.LEFT, str(GameState.get_player().fighter.hp) + ' -> FPS' +
    #                         str(libtcod.sys_get_fps()))
    #libtcod.console_print_ex(consoles['panel_console'], 1, 5, libtcod.BKGND_NONE, libtcod.LEFT, '# ' +
    #                         str(GameState.get_player().x) + "/" + str(GameState.get_player().y))
    #libtcod.console_print_ex(consoles['panel_console'], 1, 6, libtcod.BKGND_NONE, libtcod.LEFT, 'Level: ' +
    #                         str(GameState.get_dungeon_level()))


def update():
    # blit the contents of "panel" to the root console
    libtcod.console_blit(consoles['map_console'], 0, 0,
                         Constants.SCREEN_WIDTH,
                         Constants.SCREEN_HEIGHT, 0, 0, 0)
    libtcod.console_blit(consoles['entity_console'], 0, 0,
                         Constants.SCREEN_WIDTH,
                         Constants.SCREEN_HEIGHT, 0, 0, 0, 1.0, 0)
    libtcod.console_blit(consoles['panel_console'], 0, 0, Constants.SCREEN_WIDTH,
                         Constants.PANEL_HEIGHT, 0, 0,
                         Constants.PANEL_Y)
    libtcod.console_blit(consoles['side_panel_console'], 0, 0, Constants.SCREEN_WIDTH - Constants.MAP_CONSOLE_WIDTH,
                         Constants.SCREEN_HEIGHT, 0,
                         Constants.MAP_CONSOLE_WIDTH, 0)
    libtcod.console_blit(consoles['animation_console'], 0, 0,
                         Constants.SCREEN_WIDTH,
                         Constants.SCREEN_HEIGHT, 0, 0, 0, 1.0, 0.0)


def clear_animations():
    # print "clear"
    libtcod.console_clear(consoles['animation_console'])
    libtcod.console_blit(consoles['animation_console'], 0, 0, Constants.MAP_CONSOLE_WIDTH, Constants.MAP_CONSOLE_HEIGHT, 0, 0, 0, 1.0, 0.0)


def update_animations():
    # print "update"
    libtcod.console_blit(consoles['animation_console'], 0, 0, Constants.MAP_CONSOLE_WIDTH, Constants.MAP_CONSOLE_HEIGHT, 0, 0, 0, 1.0, 0.0)
    libtcod.console_flush()


def blank(x, y):
    x, y = Map.to_camera_coordinates(x, y)
    libtcod.console_put_char(consoles['entity_console'], x, y, ' ', libtcod.BKGND_NONE)


def get_offset_color(map_x, map_y):
    try:
        dist = int(Utils.distance_between(map_x, map_y, GameState.player.x, GameState.player.y))
    except:
        dist = 0
    offset_value = int((float(dist) / Constants.TORCH_RADIUS) * 255)
    offset_value = max(0, min(offset_value, 255)) / 2
    offset_color = libtcod.Color(offset_value, offset_value, offset_value)
    return offset_color


def draw_object(obj, visible=True):
    x, y = Map.to_camera_coordinates(obj.x, obj.y)

    if visible:
        libtcod.console_put_char_ex(consoles['entity_console'], x, y, obj.char, obj.color, libtcod.BKGND_NONE)
        libtcod.console_set_char_background(consoles['entity_console'], x, y, Themes.ground_bcolor() - get_offset_color(obj.x, obj.y), libtcod.BKGND_SET)
    else:
        libtcod.console_put_char_ex(consoles['entity_console'], x, y, obj.char, libtcod.darker_gray,
                                    libtcod.BKGND_NONE)


def render_messages():
    #clear old messages
    libtcod.console_set_default_foreground(consoles['panel_console'], libtcod.black)
    libtcod.console_set_default_background(consoles['panel_console'], libtcod.black)
    libtcod.console_rect(consoles['panel_console'], 1, 3, 57, Constants.PANEL_HEIGHT - 4, True, libtcod.BKGND_SET)
    # print the game messages, one line at a time
    y = 3
    for (line, color) in GameState.get_msg_queue():
        if y < Constants.PANEL_HEIGHT - 1:
            libtcod.console_set_default_foreground(consoles['panel_console'], color)
            line_height = libtcod.console_get_height_rect(consoles['panel_console'], 0, 0, Constants.MSG_WIDTH,
                                                            Constants.PANEL_HEIGHT - 3, line)
            libtcod.console_print_rect(consoles['panel_console'], Constants.MSG_X, y, Constants.MSG_WIDTH, line_height, line)

            y += line_height


def render_common():
    import Input

    libtcod.console_set_default_foreground(consoles['side_panel_console'], libtcod.Color(0,70,140))
    libtcod.console_print_rect(consoles['side_panel_console'],1,1, 17,1, "Level 1".center(17, ' '))

    libtcod.console_print_rect(consoles['side_panel_console'], 9, 18, 17, 2,
                               "X: " + str(Input.mouse.cx) + "  \nY: " + str(Input.mouse.cy) + "  ")



    libtcod.console_set_default_foreground(consoles['panel_console'], libtcod.Color(175,175,255))
    libtcod.console_set_default_background(consoles['panel_console'], libtcod.Color(0,32,64))
    libtcod.console_set_background_flag(consoles['panel_console'], libtcod.BKGND_SET)
    libtcod.console_print_rect(consoles['panel_console'], 1, 1, Constants.SCREEN_WIDTH - 19, 1, GameState.dungeon_name.center(57, ' '))



def render_status():
    # RENDER HEALTH BARS
    sx = 1
    sy = 25
    # CLEAR HP AREA / Status Area
    libtcod.console_set_default_foreground(consoles['side_panel_console'], libtcod.black)
    libtcod.console_set_default_background(consoles['side_panel_console'], libtcod.black)
    libtcod.console_rect(consoles['side_panel_console'], 1, 3, 17, 14, True, libtcod.BKGND_SET)
    libtcod.console_rect(consoles['side_panel_console'], sx, sy, 10, 9, True, libtcod.BKGND_SET)

    # print GameState.player.status

    num_of_status = 0

    for st in GameState.player.status:
        if num_of_status == 9:
            libtcod.console_set_default_background(consoles['side_panel_console'], libtcod.black)
            libtcod.console_set_default_foreground(consoles['side_panel_console'], libtcod.Color(51,51,51))
            libtcod.console_print(consoles['side_panel_console'], sx, sy-1,
                                  "...             ")  # + " (" + str(st[1]) + ")")
            return
        libtcod.console_set_default_background(consoles['side_panel_console'], libtcod.black)
        libtcod.console_set_default_foreground(consoles['side_panel_console'], st['color'])
        if Utils.is_mouse_in(Constants.MAP_CONSOLE_WIDTH + sx, sy, 17, 1):
            libtcod.console_print(consoles['side_panel_console'], sx, sy, str(st['duration']) + " Turns")  # + " (" + str(st[1]) + ")")
        else:
            libtcod.console_print(consoles['side_panel_console'], sx, sy, st['name'])  # + " (" + str(st[1]) + ")")
        num_of_status += 1
        sy += 1


def render_stat_bars():

    # SHOW PLAYER STAT BARS
    render_box_bar(4, 35, 14, '', GameState.get_player().fighter.hp, GameState.get_player().fighter.base_max_hp,
                   libtcod.Color(178, 0, 45),
                   libtcod.Color(64, 0, 16), consoles['side_panel_console'])
    render_box_bar(4, 36, 14, '', GameState.get_player().fighter.sp, GameState.get_player().fighter.base_max_sp,
                   libtcod.Color(0, 0, 217),
                   libtcod.Color(0, 0, 64), consoles['side_panel_console'])

    # RENDER MONSTER HEALTH BARS
    temp_y = 3
    for object in Map.get_visible_objects():
        if object.fighter and (object is not GameState.get_player()):  # and Fov.is_visible(obj=object)
            if temp_y < 17:
                render_box_bar(1, temp_y, 17, object.name, object.fighter.hp, object.fighter.max_hp,
                               libtcod.Color(0, 255, 0),
                               libtcod.Color(0, 64, 0),
                               consoles['side_panel_console'])
                temp_y += 2


def render_box_bar(x, y, total_width, name, value, maximum, bar_color, back_color, target):
    # render a bar (HP, experience, etc). first calculate the width of the bar
    bar_width = int(float(value) / maximum * total_width)
    og_y = y
    height = 1
    #print "Box Bar!"
    if name != '':
        libtcod.console_set_default_background(target, libtcod.black)
        libtcod.console_set_default_foreground(target, libtcod.Color(51, 51, 51))
        libtcod.console_print(target, x, y, name)
        y += 1
        height += 1
    # render the background first
    libtcod.console_set_default_background(target, back_color)
    libtcod.console_set_default_foreground(target, bar_color)
    for x1 in range(x, x+total_width):
        libtcod.console_put_char(target, x1, y, 255, libtcod.BKGND_SET)
    for x1 in range(x, x+bar_width):
        libtcod.console_put_char(target, x1, y, 254, libtcod.BKGND_SET)

    if Utils.is_mouse_in(Constants.MAP_CONSOLE_WIDTH + x, og_y, total_width, height):
        libtcod.console_print_ex(target, x, y, libtcod.BKGND_SET, libtcod.LEFT, str(value) + "/" + str(maximum))


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


def blit(source, target, x=0, y=0, width=Constants.SCREEN_WIDTH, height=Constants.SCREEN_HEIGHT,
         f_alpha=1.0,
         b_alpha=1.0):
    libtcod.console_blit(source, 0, 0, width, height, target, x, y, f_alpha, b_alpha)


def render_all():
    libtcod.console_clear(0)
    full_map()
    objects()
    ui()
    update()
    libtcod.console_flush()
