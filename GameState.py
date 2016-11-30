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
import Components
import Constants
import Entity
import ConfigParser
import Map
import Themes
import UI
import Utils
import Fov
import Render
import Schedule
import Pathing
import Input
import SoundEffects
import Status


imported_items_list = {}
imported_npc_list = {}
imported_quest_list = {}
current_quests = []
player = None
inventory = []
game_msgs = []
dungeon_level = 0
dungeon_name = "Test"
dungeon_tags = []

goals = [((20, 20), 0)]

continue_walking = False


def initialize():
    global imported_items_list, imported_npc_list, imported_quest_list
    global current_quests, player, inventory, game_msgs, dungeon_level

    import Schedule

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

    Schedule.register(player)

    dungeon_level = 0


def starting_equipment():
    # initial equipment: a dagger
    equipment_component = Components.Equipment(slot='right hand', power_bonus=2)
    obj = Entity.Entity(0, 0, '-', 'dagger', libtcod.sky, equipment=equipment_component)
    inventory.append(obj)
    equipment_component.equip()
    obj.always_visible = True

    # Starting Pistol
    equipment_component = Components.Equipment(slot='left hand', power_bonus=2)
    ranged_component = Components.Ranged(10, aoe=1)
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
    config = ConfigParser.RawConfigParser()
    config.read('Objects\_items.list')

    for i in config.sections():
        imported_items_list[str(i)] = dict(config.items(i))


def read_external_npcs():
    config = ConfigParser.RawConfigParser()
    config.read('Objects\_npcs.list')

    for i in config.sections():
        imported_npc_list[str(i)] = dict(config.items(i))


def read_external_quests():
    config = ConfigParser.RawConfigParser()
    config.read('Objects\_quests.list')

    for i in config.sections():
        imported_quest_list[str(i)] = dict(config.items(i))

def main_menu():
    UI.Display_MainMenu()


def new_game():
    initialize()

    # map_console = libtcod.console_new(Constants.MAP_CONSOLE_WIDTH, Constants.MAP_CONSOLE_HEIGHT)
    # entity_console = libtcod.console_new(Constants.MAP_CONSOLE_WIDTH, Constants.MAP_CONSOLE_HEIGHT)
    # panel = libtcod.console_new(Constants.SCREEN_WIDTH, Constants.PANEL_HEIGHT)
    # side_panel = libtcod.console_new(20, Constants.SCREEN_HEIGHT - Constants.PANEL_HEIGHT)
    # animation_console = libtcod.console_new(Constants.MAP_CONSOLE_WIDTH, Constants.MAP_CONSOLE_HEIGHT)

    # Render.initialize(map_console, entity_console, panel, side_panel, animation_console)
    Render.initialize()

    Map.load_diner_map()
    next_level()
    Fov.initialize()
    play_game()


def next_level():
    global dungeon_level, dungeon_name, dungeon_tags
    import Keys

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

    if '<M+>' in dungeon_tags:
        Themes.set_theme('Shadow State Archive')
    elif '<PRE>' in dungeon_tags:
        Themes.set_theme('Forest')
    else:
        Themes.set_theme('Valley of Devils')
    # Themes.set_theme('Abyss of the Fish Men')

    # OVERRIDE
    Themes.set_theme('Shadow State Archive')

    Schedule.reset()
    Map.generate_map()
    print "Objects: " + str(len(Map.objects))
    print "VisObjects: " + str(len(Map.get_visible_objects()))
    print "Dungeon Lvl: " + str(dungeon_level)

    Fov.require_recompute()
    Pathing.BFS(player)



def play_game():

    Fov.require_recompute()
    Pathing.BFS(player)

    while not libtcod.console_is_window_closed():
        Input.clear()
        Schedule.process()


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
            choice = UI.menu('Level up! Choose a stat to raise:\n',
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
