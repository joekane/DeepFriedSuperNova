import libtcodpy as libtcod
import Constants
import Utils
import Fov
import GameState
import Map

consoles = {}
gameState = None


def initialize(map_console, panel_console, side_panel_console):
    global consoles, gameState
    consoles['map_console'] = map_console
    consoles['panel_console'] = panel_console
    consoles['side_panel_console'] = side_panel_console


def clear_map():
    libtcod.console_clear(consoles['map_console'])


def map():

    Fov.recompute()

    map = Map.current_map()

    # go through all tiles, and set their background color
    for y in range(Constants.MAP_HEIGHT):
        for x in range(Constants.MAP_WIDTH):
            visible = Fov.is_visible(pos=(x, y))
            wall = map[x][y].block_sight and map[x][y].blocked
            glass = not map[x][y].block_sight and map[x][y].blocked
            box = map[x][y].block_sight and not map[x][y].blocked
            wall_char = libtcod.CHAR_BLOCK1

            # floor_char = libtcod.CHAR_SUBP_DIAG
            floor_char = '.'

            wall_color = libtcod.red
            floor_color = libtcod.white

            player = GameState.get_player()

            vOffset = int(Utils.distance_between(x, y, player.x, player.y)) * 15
            offset_color = libtcod.Color(vOffset, vOffset, vOffset)

            if not visible:
                # if it's not visible right now, the player can only see it if it's explored
                if map[x][y].explored:
                    # it's out of the player's FOV
                    if wall:
                        libtcod.console_put_char_ex(consoles['map_console'], x, y, wall_char, libtcod.darker_grey, libtcod.BKGND_SET)
                    elif glass:
                        libtcod.console_put_char_ex(consoles['map_console'], x, y, chr(219), libtcod.darker_grey, libtcod.BKGND_SET)
                    elif box:
                        libtcod.console_put_char_ex(consoles['map_console'], x, y, '~', libtcod.darker_grey, libtcod.BKGND_SET)
                    else:
                        libtcod.console_put_char_ex(consoles['map_console'], x, y, floor_char, floor_color * .09, libtcod.BKGND_SET)
            else:
                # it's visible
                # print(vOffset)
                if wall:
                    libtcod.console_put_char_ex(consoles['map_console'], x, y, wall_char, wall_color - offset_color, libtcod.BKGND_SET)
                elif glass:
                    libtcod.console_put_char_ex(consoles['map_console'], x, y, chr(178),
                                                libtcod.Color(max(0, 10 - vOffset), max(0, 10 - vOffset),
                                                              max(0, 100 - vOffset)), libtcod.BKGND_SET)
                elif box:
                    libtcod.console_put_char_ex(consoles['map_console'], x, y, '~',
                                                libtcod.Color(max(0, 100 - vOffset), max(0, 100 - vOffset),
                                                              max(0, 130 - vOffset)), libtcod.BKGND_SET)
                else:
                    libtcod.console_put_char_ex(consoles['map_console'], x, y, floor_char,
                                                floor_color - offset_color, libtcod.BKGND_SET)
                map[x][y].explored = True


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
    libtcod.console_print_ex(consoles['panel_console'], 1, 1, libtcod.BKGND_NONE, libtcod.LEFT, Utils.get_names_under_mouse(objects))

    # print the game messages, one line at a time
    y = 1
    for (line, color) in GameState.get_msg_queue():
        libtcod.console_set_default_foreground(consoles['panel_console'], color)
        libtcod.console_print_ex(consoles['panel_console'], Constants.MSG_X, y, libtcod.BKGND_NONE, libtcod.LEFT, line)
        y += 1

    # show the player's stats
    render_bar(1, 2, Constants.BAR_WIDTH, 'HP', GameState.get_player().fighter.hp, GameState.get_player().fighter.max_hp,
               libtcod.light_red, libtcod.darker_red, consoles['panel_console'])

    render_vert_line(0, 0, Constants.SCREEN_HEIGHT - Constants.PANEL_HEIGHT, libtcod.Color(30, 30, 30), consoles['side_panel_console'])

    libtcod.console_print_ex(consoles['panel_console'], 1, 4, libtcod.BKGND_NONE, libtcod.LEFT, 'Dungeon level ' + str(GameState.get_dungeon_level()))
    libtcod.console_print_ex(consoles['panel_console'], 1, 5, libtcod.BKGND_NONE, libtcod.LEFT, '# ' + str(GameState.get_player().x) + "/" + str(GameState.get_player().y))

    tempY = 2
    for object in Map.get_objects():
        if object.fighter and Fov.is_visible(obj=object) and (object is not GameState.get_player()):
            render_bar(1, tempY, 8, '', object.fighter.hp, object.fighter.max_hp, libtcod.dark_green,
                       libtcod.darker_red, consoles['side_panel_console'])
            if object in Utils.get_fighters_under_mouse(objects):
                libtcod.console_set_default_foreground(consoles['side_panel_console'], libtcod.white)
            else:
                libtcod.console_set_default_foreground(consoles['side_panel_console'], libtcod.black)
            libtcod.console_print_ex(consoles['side_panel_console'], 1, tempY, libtcod.BKGND_NONE, libtcod.LEFT, object.name)
            tempY += 1


def update():
    # blit the contents of "panel" to the root console
    libtcod.console_blit(consoles['map_console'], 0, 0, Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT, 0, 0, 0)
    libtcod.console_blit(consoles['panel_console'], 0, 0, Constants.SCREEN_WIDTH, Constants.PANEL_HEIGHT, 0, 0, Constants.PANEL_Y)
    libtcod.console_blit(consoles['side_panel_console'], 0, 0, 10, Constants.SCREEN_HEIGHT, 0, Constants.MAP_WIDTH, 0)


def blank(x,y):
    libtcod.console_put_char(consoles['map_console'], x, y, ' ', libtcod.BKGND_NONE)


def draw_object(obj):
    libtcod.console_put_char_ex(consoles['map_console'], obj.x, obj.y, obj.char, obj.color, libtcod.BKGND_NONE)


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


