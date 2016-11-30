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
import collections

from bearlibterminal import terminal
from timeit import default_timer as timer

Pos = collections.namedtuple('Pos', 'x y')

layers = {}
gameState = None

hm_colors = [libtcod.yellow,
             libtcod.color_lerp(libtcod.yellow, libtcod.amber, 0.5),
             libtcod.color_lerp(libtcod.yellow, libtcod.amber, 0.5),
             libtcod.amber,
             libtcod.color_lerp(libtcod.amber, libtcod.orange, 0.5),
             libtcod.color_lerp(libtcod.amber, libtcod.orange, 0.5),
             libtcod.orange,
             libtcod.color_lerp(libtcod.orange, libtcod.flame, 0.5),
             libtcod.color_lerp(libtcod.orange, libtcod.flame, 0.5),
             libtcod.flame,
             libtcod.color_lerp(libtcod.flame, libtcod.red, 0.5),
             libtcod.color_lerp(libtcod.flame, libtcod.red, 0.5),
             libtcod.red,
             libtcod.color_lerp(libtcod.red, libtcod.crimson, 0.5),
             libtcod.color_lerp(libtcod.red, libtcod.crimson, 0.5),
             libtcod.crimson,
             libtcod.color_lerp(libtcod.crimson, libtcod.pink, 0.5),
             libtcod.color_lerp(libtcod.crimson, libtcod.pink, 0.5),
             libtcod.pink,
             libtcod.color_lerp(libtcod.pink, libtcod.magenta, 0.5),
             libtcod.color_lerp(libtcod.pink, libtcod.magenta, 0.5),
             libtcod.magenta,
             libtcod.color_lerp(libtcod.magenta, libtcod.fuchsia, 0.5),
             libtcod.color_lerp(libtcod.magenta, libtcod.fuchsia, 0.5),
             libtcod.fuchsia,
             libtcod.color_lerp(libtcod.fuchsia, libtcod.purple, 0.5),
             libtcod.color_lerp(libtcod.fuchsia, libtcod.purple, 0.5),
             libtcod.purple,
             libtcod.color_lerp(libtcod.purple, libtcod.violet, 0.5),
             libtcod.color_lerp(libtcod.purple, libtcod.violet, 0.5),
             libtcod.violet,
             libtcod.color_lerp(libtcod.violet, libtcod.han, 0.5),
             libtcod.color_lerp(libtcod.violet, libtcod.han, 0.5),
             libtcod.han,
             libtcod.color_lerp(libtcod.han, libtcod.blue, 0.5),
             libtcod.color_lerp(libtcod.han, libtcod.blue, 0.5),
             libtcod.blue]

hm_values = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K',
             'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


# def initialize(map_console, entity_console, panel_console, side_panel_console, animation_console):
def initialize():
    global layers, gameState
    layers['map_console'] = 0
    layers['panel_console'] = 2
    layers['UI_Back'] = 1
    layers['side_panel_console'] = 2
    layers['entity_console'] = 3
    layers['messages'] = 4
    layers['animation_console'] = 5

    UI.load_from_xp(Constants.MAP_CONSOLE_WIDTH, 0, 'Side_panel', layers['UI_Back'])
    UI.load_from_xp(0, Constants.MAP_CONSOLE_HEIGHT, 'Panel', layers['UI_Back'])


def clear_map_OLD():
    libtcod.console_clear(layers['map_console'])


def full_map():
    import Noise

    if Fov.recompute():

        Utils.clear_layer(0)

        map = Map.current_map()
        player = GameState.get_player()
        Map.move_camera(player.x, player.y)
        camera_x, camera_y = Map.get_camera()

        # Map.d_map[player.x][player.y] = 0


        for y in range(Constants.MAP_CONSOLE_HEIGHT):
            for x in range(Constants.MAP_CONSOLE_WIDTH):
                map_x, map_y = (camera_x + x, camera_y + y)
                tile = map[map_x][map_y]
                visible = Fov.is_visible(pos=(map_x, map_y))

                # dist = Utils.distance_between(player.x, player.y, map_x, map_y)
                # Map.d_map[map_x][map_y] = int(dist)

                if Constants.DEBUG:
                    if Map.is_blocked(map_x,map_y):
                        draw_char(layers['map_console'], x, y, '*',
                                  tile.f_color, libtcod.BKGND_SET)
                    #else:
                    if True:
                        dist = Map.current_map()[map_x][map_y].distance_to_player

                        char = chr(min(dist + 48, 200)) # chr(min(Map.d_map[map_x][map_y] + 48, 200))
                        if dist == -1:
                            char = '!'
                        c_value = max(dist, 0)   # max(Map.d_map[map_x][map_y] , 0)

                        # char = hm_values[min(c_value, len(hm_values) - 1)]
                        db_color = hm_colors[min(c_value, len(hm_colors) - 1)]

                        draw_char(layers['map_console'], x, y, char,
                                  db_color, libtcod.BKGND_SET)


                else:
                    if not visible:
                        if tile.explored:
                            if tile.blocked:
                                char =  tile.char
                                f_color = libtcod.Color(50, 50, 50)
                                b_color = libtcod.Color(10, 10, 10)
                            else:
                                char = '.'
                                f_color = libtcod.Color(50, 50, 50)
                                b_color = libtcod.Color(0, 0, 0)

                            draw_char(layers['map_console'], x, y, char,
                                      f_color, libtcod.BKGND_SET)
                            draw_background(layers['map_console'], x, y,
                                            b_color, flag=libtcod.BKGND_SET)
                            #libtcod.console_put_char_ex(consoles['map_console'], x, y, char,
                            #                            Themes.OUT_OF_FOV_COLOR, libtcod.BKGND_SET)

                    else:
                        offset_color = get_offset_color(map_x, map_y)

                        draw_char(layers['map_console'], x, y, tile.char,
                                  tile.f_color - offset_color, libtcod.BKGND_SET)
                        draw_background(layers['map_console'], x, y,
                                        tile.b_color - offset_color, flag=libtcod.BKGND_SET)
                        tile.explored = True


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


def print_line(dest, x, y, text, flag=libtcod.BKGND_NONE, alignment=libtcod.LEFT): # bottom-right for BEARLIB
    # LIBTCOD
    # libtcod.console_print_ex(dest, x, y, flag, alignment, text)

    # BERALIB
    if alignment == libtcod.LEFT:
        alignment = "left"
    terminal.layer(dest)
    terminal.print_(x, y, "{0}[align={1}]".format(text,alignment))


def print_rect(dest, x, y, w, h, text):
    # LIBTCOD
    # libtcod.console_print_rect(dest, x, y, w, h, text)

    # BEARLIB
    terminal.layer(dest)
    terminal.print_(x, y, "{0}[bbox={1}x{2}]".format(text, w, h))


def draw_rect(dest, x, y, w, h, frame=False, f_color=None, bk_color=None):
    terminal.layer(dest)
    for x1 in range(w):
        for y1 in range(h):
            print "Hellow"
            terminal.color(bk_color)
            draw_char(dest, x1 + x, y1 + y, Utils.get_unicode(219))
            if frame:
                terminal.color(f_color)
                if (x1, y1) == (0, 0):
                    draw_char(dest, x1 + x, y1 + y, 0x250C)
                elif (x1, y1) == (w - 1, 0):
                    draw_char(dest, x1 + x, y1 + y, 0x2510)
                elif (x1, y1) == (0, h - 1):
                    draw_char(dest, x1 + x, y1 + y, 0x2514)
                elif (x1, y1) == (w - 1, h - 1):
                    draw_char(dest, x1 + x, y1 + y, 0x2518)
                elif x1 == 0 or x1 == w - 1:
                    draw_char(dest, x1 + x, y1 + y, 0x2502)
                elif y1 == 0 or y1 == h - 1:
                    draw_char(dest, x1 + x, y1 + y, 0x2500)





def object_clear():
    for obj in Map.get_all_objects():
        obj.clear()


def objects():
    # libtcod.console_clear(consoles['entity_console'])
    Utils.clear_layer(layers['entity_console'])
    for object in Map.get_all_objects():
        if object != GameState.get_player():
            object.draw()
    GameState.get_player().draw()


def ui():
    Utils.clear_layer(layers['panel_console'])
    Utils.clear_layer(layers['side_panel_console'])

    render_common()

    render_messages()

    render_status()

    render_stat_bars()


def update_OLD():
    # blit the contents of "panel" to the root console
    libtcod.console_blit(layers['map_console'], 0, 0,
                         Constants.SCREEN_WIDTH,
                         Constants.SCREEN_HEIGHT, 0, 0, 0)
    libtcod.console_blit(layers['entity_console'], 0, 0,
                         Constants.SCREEN_WIDTH,
                         Constants.SCREEN_HEIGHT, 0, 0, 0, 1.0, 0)
    libtcod.console_blit(layers['panel_console'], 0, 0, Constants.SCREEN_WIDTH,
                         Constants.PANEL_HEIGHT, 0, 0,
                         Constants.PANEL_Y)
    libtcod.console_blit(layers['side_panel_console'], 0, 0, Constants.SCREEN_WIDTH - Constants.MAP_CONSOLE_WIDTH,
                         Constants.SCREEN_HEIGHT, 0,
                         Constants.MAP_CONSOLE_WIDTH, 0)
    libtcod.console_blit(layers['animation_console'], 0, 0,
                         Constants.SCREEN_WIDTH,
                         Constants.SCREEN_HEIGHT, 0, 0, 0, 1.0, 0.0)


def clear_animations_OLD():
    # print "clear"
    libtcod.console_clear(layers['animation_console'])
    libtcod.console_blit(layers['animation_console'], 0, 0, Constants.MAP_CONSOLE_WIDTH, Constants.MAP_CONSOLE_HEIGHT, 0, 0, 0, 1.0, 0.0)


def update_animations_OLD():
    # print "update"
    libtcod.console_blit(layers['animation_console'], 0, 0, Constants.MAP_CONSOLE_WIDTH, Constants.MAP_CONSOLE_HEIGHT, 0, 0, 0, 1.0, 0.0)
    libtcod.console_flush()


def blank(x, y):
    x, y = Map.to_camera_coordinates(x, y)
    # libtcod.console_put_char(consoles['entity_console'], x, y, ' ', libtcod.BKGND_NONE)
    draw_char(layers['entity_console'], x, y, ' ', None, libtcod.BKGND_NONE)


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
        draw_char(layers['entity_console'], x, y, obj.char, obj.color, libtcod.BKGND_NONE)
        # draw_background(layers['entity_console'], x, y, Themes.ground_bcolor() - get_offset_color(obj.x, obj.y), libtcod.BKGND_SET)
    else:
        draw_char(layers['entity_console'], x, y, obj.char, libtcod.darker_gray,
                  libtcod.BKGND_NONE)


def render_messages():
    Utils.clear_layer(layers['messages'])
    y = 3 + Constants.MAP_CONSOLE_HEIGHT
    for (line, color) in GameState.get_msg_queue():
        if y < Constants.SCREEN_HEIGHT - 1:
            set_foreground(layers['messages'], color)
            # line_height = libtcod.console_get_height_rect(consoles['panel_console'], 0, 0, Constants.MSG_WIDTH, Constants.PANEL_HEIGHT - 3, line)
            line_height = 1
            print_rect(layers['messages'], Constants.MSG_X, y, Constants.MSG_WIDTH, line_height, line)

            y += line_height


def render_common():
    import Input

    pos = Pos(Constants.MAP_CONSOLE_WIDTH, 0)

    set_foreground(layers['side_panel_console'], libtcod.Color(0, 70, 140))

    print_rect(layers['side_panel_console'], pos.x + 1, pos.y + 1, 17, 1, "Level 1".center(17, ' '))

    print_rect(layers['side_panel_console'], pos.x + 9, pos.y + 18, 17, 2,
                               "X: " + str(Input.mouse.cx) + "  \nY: " + str(Input.mouse.cy) + "  ")

    set_foreground(layers['panel_console'], libtcod.Color(175, 175, 255))
    set_background(layers['panel_console'], libtcod.Color(0, 32, 64))
    # libtcod.console_set_background_flag(consoles['panel_console'], libtcod.BKGND_SET)



    pos = Pos(0, Constants.MAP_CONSOLE_HEIGHT)
    print_rect(layers['panel_console'], pos.x + 1, pos.y + 1, Constants.SCREEN_WIDTH - 19, 1,GameState.dungeon_name.center(57, ' '))
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
    for object in Map.get_visible_objects():
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
        print_line(target, x, y, line, libtcod.BKGND_NONE, libtcod.CENTER)



def render_bar(x, y, total_width, name, value, maximum, bar_color, back_color, target):
    # TODO: convert to 219s
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
        print_line(target, x + total_width / 2, y, name + ': ' + str(value) + '/' + str(maximum),
                   libtcod.BKGND_NONE, libtcod.CENTER)


def render_vert_line(x, y, length, color, target):
    # render the background first
    set_background(target, color)
    draw_rect(target, x, y, 1, length, False, libtcod.BKGND_SCREEN)


def render_hoz_line(x, y, length, color, target):
    # render the background first
    set_background(target, color)
    draw_rect(target, x, y, length, 1, False, libtcod.BKGND_SCREEN)


def blit(source, target, x=0, y=0, width=Constants.SCREEN_WIDTH, height=Constants.SCREEN_HEIGHT,
         f_alpha=1.0,
         b_alpha=1.0):
    libtcod.console_blit(source, 0, 0, width, height, target, x, y, f_alpha, b_alpha)



def render_all():
    #print "Render All"
    # graphics.clear_con()
    # libtcod.console_clear(0)

    # terminal.bkcolor('black')
    # terminal.clear()

    Fov.require_recompute()

    full_map()

    objects()

    ui()

    terminal.refresh()


def render_ui():
    # Input.update()
    ui()
    # update()
    # libtcod.console_flush()
    terminal.refresh()

    # print "Full: {0}, Object: {1}, UI: {2}, Update: {3}".format(startB - startA, startC - startB, startD - startC, startE - startD)

