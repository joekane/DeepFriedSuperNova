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

import ConfigParser

from bearlibterminal import terminal

import Constants
import Engine.Schedule
from Engine import UI
import MapGen.WorldGen
import Utils
import Engine.Animation_System as Animation
import random
import libtcodpy as libtcod
from Entities import Entity, Components, Pathing


imported_items_list = {}
imported_npc_list = {}
imported_quest_list = {}
current_quests = []
player = None
inventory = []
game_msgs = []
dungeon_level = 1
dungeon_name = "Test"
dungeon_tags = []

animation_queue = []

inventory = []


visible_objects = None

camera_x = 0
camera_y = 0

goals = [((20, 20), 0)]

continue_walking = False

""" Worlds """
# diner
# level1


current_level = None


def initialize():
    global imported_items_list, imported_npc_list, imported_quest_list
    global current_quests, player, inventory, game_msgs, dungeon_level

    import Engine.Schedule

    imported_items_list = {}
    imported_npc_list = {}
    imported_quest_list = {}
    current_quests = []
    inventory = []
    game_msgs = []

    read_external_items()
    read_external_npcs()
    read_external_quests()

    # create object representing the player
    fighter_component = Components.Fighter(hp=500,
                                           defense=100,
                                           power='1d3',
                                           xp=0,
                                           sp=100,
                                           death_function=Components.player_death)
    player = Entity.Entity(0, 0, '@', 'player', libtcod.white,
                           blocks=True,
                           ai=Components.PlayeControlled(),
                           fighter=fighter_component)

    starting_equipment()
    player.base_speed = 10

    # TODO: Refresh duration(AKA replace old one) or make stacking ones that allow this.....)

    player.apply_status('Rage')
    player.apply_status('Blessed')
    player.apply_status('Poisoned')

    player.level = 1
    player.action_points = 100

    Engine.Schedule.register(player)

    dungeon_level = 1


def starting_equipment():
    # initial equipment: a dagger
    equipment_component = Components.Equipment(slot='right hand', power_bonus=2)
    obj = Entity.Entity(0, 0, '-', 'dagger', libtcod.sky, equipment=equipment_component)
    inventory.append(obj)
    equipment_component.equip()
    obj.always_visible = True

    # Starting Pistol
    equipment_component = Components.Equipment(slot='left hand', power_bonus=2)
    ranged_component = Components.Ranged(10,
                                         aoe=1,
                                         animation='Shot'
                                         )
    obj = Entity.Entity(0, 0, libtcod.CHAR_NW, 'pistol', libtcod.sky,
                        equipment=equipment_component,
                        ranged=ranged_component)
    inventory.append(obj)
    equipment_component.equip()
    obj.always_visible = True


def get_player():
    return player


def get_dungeon_level():
    return dungeon_level


def get_inventory():
    return inventory


def get_quests():
    return current_quests


def get_equipped_in_slot(slot):  # returns the equipment in a slot, or None if it's empty
    for obj in inventory:
        if obj.equipment and obj.equipment.slot == slot and obj.equipment.is_equipped:
            return obj.equipment
    return None


def get_all_equipped(obj):  # returns a list of equipped items
    if obj == player:
        equipped_list = []
        for item in inventory:
            if item.equipment and item.equipment.is_equipped:
                equipped_list.append(item.equipment)
        return equipped_list
    else:
        return []  # other objects have no equipment


def get_quest_item(number):
    return imported_items_list[imported_quest_list[number]['quest_req']]['name']


def player_has_item(name):
    for item in inventory:
        #print item.name + " | " + name
        if item.name == name:
            #print "True!"
            return True
    #print "False"
    return False


def remove_from_inventory(name):
    global inventory
    for item in inventory:
        if item.name == name:
            inventory.remove(item)
            add_msg(item.name + " removed from inventory.", libtcod.amber)
            return


def get_msg_queue():
    return game_msgs


def del_msg(number):
    del game_msgs[number]


def add_msg(line, color):
    game_msgs.append((line, color))


def read_external_items():
    global imported_items_list
    config = ConfigParser.RawConfigParser()
    config.read('Assets\Objects\_items.list')

    for i in config.sections():
        imported_items_list[str(i)] = dict(config.items(i))


def read_external_npcs():
    global imported_npc_list
    config = ConfigParser.RawConfigParser()
    config.read('Assets\Objects\_npcs.list')

    for i in config.sections():
        imported_npc_list[str(i)] = dict(config.items(i))


def read_external_quests():
    global imported_quest_list
    config = ConfigParser.RawConfigParser()
    config.read('Assets\Objects\_quests.list')

    for i in config.sections():
        imported_quest_list[str(i)] = dict(config.items(i))

def main_menu():
    Engine.UI.Display_MainMenu()


def new_game():
    global current_level
    initialize()

    # map_console = libtcod.console_new(Constants.MAP_CONSOLE_WIDTH, Constants.MAP_CONSOLE_HEIGHT)
    # entity_console = libtcod.console_new(Constants.MAP_CONSOLE_WIDTH, Constants.MAP_CONSOLE_HEIGHT)
    # panel = libtcod.console_new(Constants.SCREEN_WIDTH, Constants.PANEL_HEIGHT)
    # side_panel = libtcod.console_new(20, Constants.SCREEN_HEIGHT - Constants.PANEL_HEIGHT)
    # animation_console = libtcod.console_new(Constants.MAP_CONSOLE_WIDTH, Constants.MAP_CONSOLE_HEIGHT)

    # Render.initialize(map_console, entity_console, panel, side_panel, animation_console)
    """ OLD WAY """
    '''
    Render.initialize()

    MapGen.Map.load_diner_map()
    next_level()
    Fov.initialize()

    play_game()
    '''
    """ NEW WAY """

    import MapGen.Themes
    MapGen.Themes.set_theme('Shadow State Archive')

    current_level = MapGen.WorldGen.Level("Test World")
    current_level.initialize(player, MapGen.WorldGen.mst_dungeon)

    #current_level.map_array = MapGen.WorldGen.new_map()
    #MapGen.WorldGen.mst_dungeon(current_level)

    #current_level.fov_initialize()
    #current_level.require_recompute()
    #current_level.recompute_fov()


    play_game()


def next_level():
    global dungeon_level, dungeon_name, dungeon_tags
    from Engine import Keys

    print "SHOULD NOT BE HERE....."

    # advance to the next level
    add_msg('You take a moment to rest, and recover your strength.', libtcod.light_violet)
    get_player().fighter.heal(get_player().fighter.max_hp / 2)  # heal the player by 50%
    get_player().action_points = 0
    add_msg('After a rare moment of peace, you descend deeper into the heart of the dungeon...', libtcod.red)
    dungeon_level += 1

    # TODO: eventually set theme and other stats based on tags generated HERE.
    key = Keys.generate_world_title()
    dungeon_name = Utils.remove_tags(key)
    dungeon_tags = Utils.get_tags(key)

    """ SHOULD BE IN LEVEL/WORLD CONSTRUCTION """
    '''
    if '<M+>' in dungeon_tags:
        Themes.set_theme('Shadow State Archive')
    elif '<PRE>' in dungeon_tags:
        Themes.set_theme('Forest')
    else:
        Themes.set_theme('Valley of Devils')
    # Themes.set_theme('Abyss of the Fish Men')

    # OVERRIDE
    Themes.set_theme('Shadow State Archive')
    '''

    Engine.Schedule.reset()

    # TODO: THIS NEEDS TO BE BROUGHT UP TO SPEED """
    # MapGen.Map.generate_map()
    new_game()


    current_level.require_recompute()
    Pathing.BFS(player)


def play_game():
    UI.initilize_hud()
    current_level.require_recompute()
    Pathing.BFS(player)

    while not libtcod.console_is_window_closed():
        #print animation_queue
        #print not animation_queue
        if not animation_queue:
            Engine.Schedule.process()
        else:
            render_ui()


def check_level_up():
    # see if the player's experience is enough to level-up

    level_up_xp = Constants.LEVEL_UP_BASE + player.level * Constants.LEVEL_UP_FACTOR
    if player.fighter.xp >= level_up_xp:
        # it is! level up
        player.level += 1
        player.fighter.xp -= level_up_xp
        Utils.message('Your battle skills grow stronger! You reached level ' + str(player.level) + '!', libtcod.yellow)

        choice = None
        while choice is None:  # keep asking until a choice is made
            choice = Engine.UI.menu('Level up! Choose a stat to raise:\n',
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


# CAMERA
def get_camera():
    return camera_x, camera_y


def move_camera(target_x, target_y):
    global camera_x, camera_y

    try:
    # new camera coordinates (top-left corner of the screen relative to the map)
        x = target_x - Constants.MAP_CONSOLE_WIDTH / 2  # coordinates so that the target is at the center of the screen
        y = target_y - Constants.MAP_CONSOLE_HEIGHT / 2
    except:
        x = camera_x
        y = camera_y

    # make sure the camera doesn't see outside the map
    if x < 0:
        x = 0
    if y < 0:
        y = 0
    if x > Constants.MAP_WIDTH - Constants.MAP_CONSOLE_WIDTH:
        x = Constants.MAP_WIDTH - Constants.MAP_CONSOLE_WIDTH
    if y > Constants.MAP_HEIGHT - Constants.MAP_CONSOLE_HEIGHT:
        y = Constants.MAP_HEIGHT - Constants.MAP_CONSOLE_HEIGHT

    if x != camera_x or y != camera_y:
        current_level.require_recompute()

    (camera_x, camera_y) = (x, y)


def render_all():
    current_level.draw()
    UI.draw_hud()

    terminal.refresh()


def render_ui():
    UI.draw_hud()
    render_animations()
    terminal.refresh()


def render_animations():
    import Render
    Render.clear_layer(10)
    for ani in animation_queue:
        #print "Animating................."
        result = ani.play()
        if result == 'Done':
            #print "Want?"
            animation_queue.remove(ani)
        terminal.refresh()



def player_move_or_interact(dx, dy):
    # the coordinates the player is moving to/interacting


    x = player.x + dx
    y = player.y + dy

    # try to find an interactable object there

    for object in current_level.get_visible_objects():

        if object.fighter and object.x == x and object.y == y:
            player.fighter.attack(object)

            return
        """ DISABLE QUEST SYSTEM """
        '''
        if isinstance(object.ai, Components.QuestNpc) and object.x == x and object.y == y:
            # print "Reward!!!! .... ??"
            object.ai.talk()
            return
        '''
        if object.blocks:
            if isinstance(object.ai, Components.Door) and object.x == x and object.y == y:
                object.ai.interact()
                current_level.require_recompute()
                return

    player.move(dx, dy)
    current_level.require_recompute()


def add_animation(animation, animation_params):
    animation_queue.append(Animation.AddAnimation(animation, animation_params))
