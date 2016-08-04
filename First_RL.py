# -*- coding: utf-8 -*-
import libtcodpy as libtcod
import Utils
import Render
import Fov
import Map
import GameState
import Constants
# import shelve

color_dark_wall = libtcod.Color(30, 30, 30)
color_dark_ground = libtcod.Color(40, 40, 40)

color_light_wall = libtcod.dark_amber
color_light_ground = libtcod.lighter_grey

""" GUI """


def menu(header, options, width):
    global key, mouse
    if len(options) > 26:
        raise ValueError('Cannot have a menu with more than 26 options.')

    # calculate total height for the header (after auto-wrap) and one line per option
    header_height = libtcod.console_get_height_rect(con, 0, 0, width, Constants.SCREEN_HEIGHT, header)
    if header == '':
        header_height = 0
    height = len(options) + header_height

    # create an off-screen console that represents the menu's window
    window = libtcod.console_new(width, height)

    # print the header, with auto-wrap
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

    # print all the options
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += 1
        letter_index += 1

    # blit the contents of "window" to the root console
    x = Constants.SCREEN_WIDTH / 2 - width / 2
    y = Constants.SCREEN_HEIGHT / 2 - height / 2
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.5)

    # compute x and y offsets to convert console position to menu position
    x_offset = x  # x is the left edge of the menu
    y_offset = y + header_height  # subtract the height of the header from the top edge of the menu

    while True:
        # present the root console to the player and check for input
        libtcod.console_flush()
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if mouse.lbutton_pressed:
            (menu_x, menu_y) = (mouse.cx - x_offset, mouse.cy - y_offset)
            # check if click is within the menu and on a choice
            if 0 <= menu_x < width and 0 <= menu_y < height - header_height:
                return menu_y

        if mouse.rbutton_pressed or key.vk == libtcod.KEY_ESCAPE:
            return None  # cancel if the player right-clicked or pressed Escape

        if key.vk == libtcod.KEY_ENTER and key.lalt:
            # Alt+Enter: toggle fullscreen
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        # convert the ASCII code to an index; if it corresponds to an option, return it
        index = key.c - ord('a')
        if 0 <= index < len(options):
            return index
        # if they pressed a letter that is not an option, return None
        if 0 <= index <= 26:
            return


def msgbox(text, width=50):
    menu(text, [], width)  # use menu() as a sort of "message box"


def inventory_menu(header):
    # show a menu with each item of the inventory as an option
    if len(GameState.inventory) == 0:
        options = ['Inventory is empty.']
    else:
        options = []
        for item in GameState.inventory:
            text = item.name
            # show additional information, in case it's equipped
            if item.equipment and item.equipment.is_equipped:
                text = text + ' (on ' + item.equipment.slot + ')'
            options.append(text)

    index = menu(header, options, Constants.INVENTORY_WIDTH)

    # if an item was chosen, return it
    if index is None or len(GameState.inventory) == 0:
        return None
    return GameState.inventory[index].item


""" I/O """


def handle_keys():
    global key, char_cycle

    player = GameState.get_player()

    if key.vk == libtcod.KEY_ENTER and key.lalt:
        # Alt+Enter: toggle fullscreen
        libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

    elif key.vk == libtcod.KEY_ESCAPE:
        return 'exit'  # exit game

    # movement keys
    if game_state == 'playing':
        # movement keys
        # movement keys
        if key.vk == libtcod.KEY_UP or key.vk == libtcod.KEY_KP8:
            Map.player_move_or_interact(0, -1)
        elif key.vk == libtcod.KEY_DOWN or key.vk == libtcod.KEY_KP2:
            Map.player_move_or_interact(0, 1)
        elif key.vk == libtcod.KEY_LEFT or key.vk == libtcod.KEY_KP4:
            Map.player_move_or_interact(-1, 0)
        elif key.vk == libtcod.KEY_RIGHT or key.vk == libtcod.KEY_KP6:
            Map.player_move_or_interact(1, 0)
        elif key.vk == libtcod.KEY_HOME or key.vk == libtcod.KEY_KP7:
            Map.player_move_or_interact(-1, -1)
        elif key.vk == libtcod.KEY_PAGEUP or key.vk == libtcod.KEY_KP9:
            Map.player_move_or_interact(1, -1)
        elif key.vk == libtcod.KEY_END or key.vk == libtcod.KEY_KP1:
            Map.player_move_or_interact(-1, 1)
        elif key.vk == libtcod.KEY_PAGEDOWN or key.vk == libtcod.KEY_KP3:
            Map.player_move_or_interact(1, 1)
        elif key.vk == libtcod.KEY_KP5:
            pass  # do nothing ie wait for the monster to come to you
        else:
            # test for other keys
            key_char = chr(key.c)

            if key_char == 'g':
                # pick up an item
                for object in Map.get_objects():  # look for an item in the player's tile
                    if object.x == player.x and object.y == player.y and object.item:
                        object.item.pick_up()
                        break
            elif key_char == 'i':
                # show the inventory; if an item is selected, use it
                # img = libtcod.image_load('orc.png')
                # libtcod.image_blit_2x(img, 0, 0, 0)

                # img2 = libtcod.image_load('orc_80.png')
                # libtcod.image_blit_2x(img2, 0, 40, 0)

                chosen_item = inventory_menu('Press the key next to an item to use it, or any other to cancel.\n')

                if chosen_item is not None:
                    chosen_item.use()
                    return 'used_item'
            elif key_char == 'd':
                # show the inventory; if an item is selected, drop it
                chosen_item = inventory_menu('Press the key next to an item to drop it, or any other to cancel.\n')

                if chosen_item is not None:
                    chosen_item.drop()
            elif key_char == 'f':
                for obj in GameState.get_all_equipped(player):
                    if obj.owner.ranged:
                        obj.owner.ranged.fire()
                        return 'fired_ranged'
                Utils.message("No ranged weapon equipped!", libtcod.light_amber)
            elif key_char == 'h':
                for obj in GameState.get_inventory():
                    if obj.name == 'healing potion':
                        obj.item.use()
                        return 'used_item'
                return Utils.message("No helaing potions.", libtcod.light_amber)
            elif key_char == '<':
                # go down stairs, if the player is on them
                stairs = Map.get_stairs()
                if stairs.x == player.x and stairs.y == player.y:
                    next_level()
            elif key_char == 'c':
                # show character information
                level_up_xp = Constants.LEVEL_UP_BASE + player.level * Constants.LEVEL_UP_FACTOR
                msgbox(
                    'Character Information\n\nLevel: ' + str(player.level) + '\nExperience: ' + str(player.fighter.xp) +
                    '\nExperience to level up: ' + str(level_up_xp) + '\n\nMaximum HP: ' + str(player.fighter.max_hp) +
                    '\nAttack: ' + str(player.fighter.power) + '\nDefense: ' + str(player.fighter.defense),
                    Constants.CHARACTER_SCREEN_WIDTH)
            elif key_char == 'p':

                libtcod.console_put_char_ex(0, 0, 0, chr(char_cycle), libtcod.red, libtcod.BKGND_NONE)
                libtcod.console_print_ex(0, 0, 1, libtcod.BKGND_NONE, libtcod.LEFT, str(char_cycle))
                libtcod.console_flush()
                char_cycle += 1

            return 'didnt-take-turn'


""" GAME STATES """


def new_game():
    global game_state

    GameState.initialize()

    Render.initialize(con, panel, side_panel)

    Map.load_diner_map()
    Fov.initialize()

    # States
    game_state = 'playing'


def next_level():
    # advance to the next level
    GameState.add_msg('You take a moment to rest, and recover your strength.', libtcod.light_violet)
    GameState.get_player().fighter.heal(GameState.get_player().fighter.max_hp / 2)  # heal the player by 50%

    GameState.add_msg('After a rare moment of peace, you descend deeper into the heart of the dungeon...', libtcod.red)
    GameState.dungeon_level += 1
    # Map.make_map()  # create a fresh new level!
    Map.make_bsp()
    Fov.initialize()
    Map.spawn_doors()


def play_game():
    global key, mouse
    player_action = None

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
        (x, y) = (mouse.cx, mouse.cy)

        # render the screen
        # render_all()

        Render.render_all()
        Utils.inspect_tile(x, y)
        libtcod.console_flush()

        # erase all objects at their old locations, before they move
        for obj in Map.get_objects():
            obj.clear()

            # handle keys and exit game if needed
        if not check_level_up():
            player_action = handle_keys()
        if player_action == 'exit':
            save_game()
            break
        # let monsters take their turn

        if game_state == 'playing' and player_action != 'didnt-take-turn':
            for obj in Map.get_objects():
                if obj.ai:
                    obj.ai.take_turn()
        else:
            if mouse.lbutton_pressed and Map.is_explored(x, y):
                GameState.get_player().move_astar_xy(x, y)


def main_menu():
    img = libtcod.image_load('diner.png')

    while not libtcod.console_is_window_closed():
        # show the background image, at twice the regular console resolution
        libtcod.image_blit_2x(img, 0, 0, 0)

        libtcod.console_print_ex(0, Constants.SCREEN_WIDTH / 2, Constants.SCREEN_HEIGHT - 2, libtcod.BKGND_NONE,
                                 libtcod.CENTER,
                                 'By Tapeworm / N Gregory')

        # show options and wait for the player's choice
        choice = menu('', ['Play a new game', 'Continue last game', 'Quit'], 24)

        if choice == 0:  # new game
            new_game()
            play_game()
        elif choice == 1:  # load last game
            try:
                load_game()
            except:
                msgbox('\n No saved game to load.\n', 24)
                continue
            play_game()

        elif choice == 2:  # quit
            break


def save_game():
    # file = shelve.open('savegame', 'n')
    # file['map'] = map
    # file['objects'] = objects
    # file['player_index'] = objects.index(player)
    # file['inventory'] = inventory
    # file['game_msgs'] = game_msgs
    # file['game_state'] = game_state
    # file['stairs_index'] = objects.index(stairs)
    # file['dungeon_level'] = dungeon_level
    # file.close()
    pass


def load_game():
    # open the previously saved shelve and load the game data
    # global map, objects, player, inventory, game_msgs, game_state, dungeon_level, stairs

    # file = shelve.open('savegame', 'r')
    # map = file['map']
    # objects = file['objects']
    # player = objects[file['player_index']]  # get index of player in objects list and access it
    # inventory = file['inventory']
    # game_msgs = file['game_msgs']
    # game_state = file['game_state']
    # stairs = objects[file['stairs_index']]
    # # dungeon_level = file['dungeon_level']
    # file.close()
    # Fov.initialize()
    pass


#############################################
# Initialization & Main Loop
#############################################

def check_level_up():
    # see if the player's experience is enough to level-up
    player = GameState.get_player()
    level_up_xp = Constants.LEVEL_UP_BASE + player.level * Constants.LEVEL_UP_FACTOR
    if player.fighter.xp >= level_up_xp:
        # it is! level up
        player.level += 1
        player.fighter.xp -= level_up_xp
        Utils.message('Your battle skills grow stronger! You reached level ' + str(player.level) + '!', libtcod.yellow)

        choice = None
        while choice is None:  # keep asking until a choice is made
            choice = menu('Level up! Choose a stat to raise:\n',
                          ['Constitution (+20 HP, from ' + str(player.fighter.base_max_hp) + ')',
                           'Strength (+1 attack, from ' + str(player.fighter.base_power) + ')',
                           'Agility (+1 defense, from ' + str(player.fighter.base_defense) + ')'],
                          Constants.LEVEL_SCREEN_WIDTH)

        if choice == 0:
            player.fighter.base_max_hp += 20
            player.fighter.hp += 20
        elif choice == 1:
            player.fighter.base_power += 1
        elif choice == 2:
            player.fighter.base_defense += 1
        return True


""" INITIALIZATION """

libtcod.console_set_custom_font('terminal10x10_gs_tc.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_init_root(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT, 'python/libtcod tutorial', False)
libtcod.sys_set_fps(Constants.LIMIT_FPS)

con = libtcod.console_new(Constants.MAP_WIDTH, Constants.MAP_HEIGHT)
panel = libtcod.console_new(Constants.SCREEN_WIDTH, Constants.PANEL_HEIGHT)
side_panel = libtcod.console_new(Constants.SCREEN_WIDTH - Constants.MAP_WIDTH,
                                 Constants.SCREEN_HEIGHT - Constants.PANEL_HEIGHT)

mouse = libtcod.Mouse()
key = libtcod.Key()
Fov.require_recompute()
game_state = None
char_cycle = 1

main_menu()
