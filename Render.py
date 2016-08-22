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

    # libtcod.console_set_default_background(consoles['animation_console'], libtcod.Color(255,255,255))
    # libtcod.console_set_background_flag(consoles['animation_console'], libtcod.BKGND_MULTIPLY)


def clear_map():
    libtcod.console_clear(consoles['map_console'])


def full_map():
    import Noise

    if Fov.recompute():

        print "Draw Map"

        map = Map.current_map()
        player = GameState.get_player()

        Map.move_camera(player.x, player.y)

        camera_x, camera_y = Map.get_camera()
    # print "cx: " + str(camera_x) + " | cy: " + str(camera_y)

    # go through all tiles, and set their background color
        for y in range(Constants.MAP_CONSOLE_HEIGHT):
            for x in range(Constants.MAP_CONSOLE_WIDTH):
                map_x, map_y = (camera_x + x, camera_y + y)
                tile = map[map_x][map_y]
                visible = Fov.is_visible(pos=(map_x, map_y))

                if Constants.DEBUG:
                    if Fov.is_visible(pos=(map_x, map_y)):
                        color = libtcod.white
                    else:
                        color = libtcod.dark_grey

                    pre_value = Noise.get_height_value(x,y)

                    # print nx, ny, pre_value
                    if 0 <= pre_value < 0.1:
                        char = '0'
                    elif 0.1 <= pre_value < 0.2:
                        char = '1'
                    elif 0.2 <= pre_value < 0.3:
                        char = '2'
                    elif 0.3 <= pre_value < 0.4:
                        char = '3'
                    elif 0.4 <= pre_value < 0.5:
                        char = '4'
                    elif 0.5 <= pre_value < 0.6:
                        char = '5'
                    elif 0.6 <= pre_value < 0.96:
                        char = '6'
                    elif 0.96 <= pre_value < 0.97:
                        char = '7'
                    elif 0.97 <= pre_value < 0.99:
                        char = '8'
                    elif 0.99 <= pre_value < 1.0:
                        char = '9'
                    else:
                        char = '0'

                    if libtcod.map_is_walkable(Fov.get_fov_map(), map_x, map_y):
                        libtcod.console_put_char_ex(consoles['map_console'], x, y, '.',
                                                    color, libtcod.BKGND_SET)
                    else:
                        libtcod.console_put_char_ex(consoles['map_console'], x, y, char,
                                                    color, libtcod.BKGND_SET)
                    tile.explored = True
                else:
                    if not visible:
                        # if it's not visible right now, the player can only see it if it's explored
                        if tile.explored:
                            if tile.blocked:
                                char = 206
                            else:
                                char = '.'
                            libtcod.console_put_char_ex(consoles['map_console'], x, y, char,
                                                        Themes.OUT_OF_FOV_COLOR, libtcod.BKGND_SET)

                    else:
                        print tile.char, tile.f_color, tile.b_color
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
    libtcod.console_set_default_background(consoles['panel_console'], libtcod.black)
    libtcod.console_clear(consoles['panel_console'])

    # prepare to render the GUI panel
    libtcod.console_set_default_background(consoles['side_panel_console'], libtcod.black)
    libtcod.console_clear(consoles['side_panel_console'])

    #render_hoz_line(0, 0, Constants.SCREEN_WIDTH, libtcod.Color(30, 30, 30), consoles['panel_console'])

    # print the Side Panel, with auto-wrap
    libtcod.console_set_default_foreground(consoles['panel_console'], Constants.UI_Fore)
    libtcod.console_set_default_background(consoles['panel_console'], Constants.UI_Back)
    libtcod.console_print_frame(consoles['panel_console'], 0, 0,
                                Constants.SCREEN_WIDTH,
                                Constants.PANEL_HEIGHT,
                                clear=True,
                                flag=libtcod.BKGND_SET,
                                fmt=None)


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

    # render_vert_line(0, 0, Constants.SCREEN_HEIGHT - Constants.PANEL_HEIGHT, libtcod.Color(30, 30, 100),
    #                 consoles['side_panel_console'])

    # print the Side Panel, with auto-wrap
    libtcod.console_set_default_foreground(consoles['side_panel_console'], Constants.UI_Fore)
    libtcod.console_set_default_background(consoles['side_panel_console'], Constants.UI_Back)
    libtcod.console_print_frame(consoles['side_panel_console'], 0, 0,
                                Constants.SCREEN_WIDTH-Constants.MAP_CONSOLE_WIDTH,
                                Constants.SCREEN_HEIGHT-Constants.PANEL_HEIGHT,
                                clear=True,
                                flag=libtcod.BKGND_SET,
                                fmt=None)

    libtcod.console_print_ex(consoles['panel_console'], 1, 4, libtcod.BKGND_NONE, libtcod.LEFT, 'FPS ' +
                             str(libtcod.sys_get_fps()))
    libtcod.console_print_ex(consoles['panel_console'], 1, 5, libtcod.BKGND_NONE, libtcod.LEFT, '# ' +
                             str(GameState.get_player().x) + "/" + str(GameState.get_player().y))
    libtcod.console_print_ex(consoles['panel_console'], 1, 6, libtcod.BKGND_NONE, libtcod.LEFT, 'Level: ' +
                             str(GameState.get_dungeon_level()))

    # RENDER HEALTH BARS
    temp_y = 2
    for object in Map.get_all_objects():
        if object.fighter and Fov.is_visible(obj=object) and (object is not GameState.get_player()):
            render_bar(2, temp_y, 17, '', object.fighter.hp, object.fighter.max_hp, libtcod.dark_green,
                       libtcod.darker_red, consoles['side_panel_console'])
            if object in Utils.get_fighters_under_mouse():
                libtcod.console_set_default_foreground(consoles['side_panel_console'], libtcod.white)
            else:
                libtcod.console_set_default_foreground(consoles['side_panel_console'], libtcod.black)
            libtcod.console_print_ex(consoles['side_panel_console'], 3, temp_y, libtcod.BKGND_NONE, libtcod.LEFT,
                                     object.name)
            temp_y += 1


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
    dist = int(Utils.distance_between(map_x, map_y, GameState.player.x, GameState.player.y))
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


def pop_up(width=None, height=None, title=None, text=None):
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # calculate total height for the header (after auto-wrap) and one line per option
    if width is None:
        width = Constants.MAP_CONSOLE_WIDTH - 30

    if height is None:
        height = libtcod.console_get_height_rect(0, 0, 0, width, Constants.SCREEN_HEIGHT, text) + 7

    pop = libtcod.console_new(width, height)
    # print the header, with auto-wrap
    libtcod.console_set_default_foreground(pop, Constants.UI_PopFore)
    libtcod.console_set_default_background(pop, Constants.UI_PopBack)

    libtcod.console_print_frame(pop, 0, 0, width, height, clear=True,
                                flag=libtcod.BKGND_SET,
                                fmt=title)

    libtcod.console_print_rect(pop, 3, 3, width-6, height, text)


    # blit the contents of "window" to the root console
    x = Constants.MAP_CONSOLE_WIDTH / 2 - width / 2
    y = Constants.MAP_CONSOLE_HEIGHT / 2 - height / 2


    button_text = 'Click to Continue'
    button = UI.Button(button_text,
                       width / 2,
                       height - 3,
                       function=UI.close_window,
                       target=pop,
                       length=len(button_text))

    libtcod.console_blit(pop, 0, 0, width, height, 0, x, y, 1.0, .85)

    while True:
        libtcod.console_blit(pop, 0, 0, width, height, 0, x, y, 1.0, 0.0)
        libtcod.console_flush()
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if button.draw(key, mouse) == 'close':
            return

        if key.vk == libtcod.KEY_ENTER and key.lalt:
            # Alt+Enter: toggle fullscreen
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
        if key.vk == libtcod.KEY_ESCAPE or key.vk == libtcod.KEY_ESCAPE or key.vk == libtcod.KEY_SPACE:
            return


def beastiary(width=None, height=None, title=None, text=None):
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # calculate total height for the header (after auto-wrap) and one line per option
    if width is None:
        width = Constants.MAP_CONSOLE_WIDTH - 10

    if height is None:
        height = libtcod.console_get_height_rect(0, 0, 0, width, Constants.SCREEN_HEIGHT, text) + 7

    pop = libtcod.console_new(width, height)
    # print the header, with auto-wrap
    libtcod.console_set_default_foreground(pop, Constants.UI_PopFore)
    libtcod.console_set_default_background(pop, Constants.UI_PopBack)

    libtcod.console_print_frame(pop, 0, 0, width, height, clear=True,
                                flag=libtcod.BKGND_SET,
                                fmt=title)




    # blit the contents of "window" to the root console
    x = 0
    y = 0


    button_text = '[ Click to Continue ]'
    button = UI.Button(button_text,
                       width / 2,
                       height - 2,
                       function=UI.close_window)

    img = libtcod.image_load('cipher_warden_80x80_test_01.png')
    libtcod.image_set_key_color(img, libtcod.Color(0, 0, 0))
    # show the background image, at twice the regular console resolution
    libtcod.image_blit_2x(img, pop, 9, 2)

    libtcod.console_set_default_foreground(pop, Constants.UI_PopFore)
    libtcod.console_set_default_background(pop, Constants.UI_PopBack)
    libtcod.console_print_rect(pop, 3, 3, width - 6, height, text)


    libtcod.console_blit(pop, 0, 0, width, height, 0, x, y, 1.0, .85)

    while True:

        libtcod.console_flush()
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if button.draw(key, mouse) == 'close':
            return

        if key.vk == libtcod.KEY_ENTER and key.lalt:
            # Alt+Enter: toggle fullscreen
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
        if key.vk == libtcod.KEY_ESCAPE or key.vk == libtcod.KEY_ESCAPE or key.vk == libtcod.KEY_SPACE:
            return



def render_all():
    # libtcod.console_clear(0)
    full_map()
    if not Constants.DEBUG:
        objects()
    ui()
    update()
    libtcod.console_flush()
