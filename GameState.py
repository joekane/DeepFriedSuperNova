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
import Entity
import ConfigParser
import Map
import CaveGen
import Fov
import SoundEffects


imported_items_list = {}
imported_npc_list = {}
imported_quest_list = {}
current_quests = []
player = None
inventory = []
game_msgs = []
dungeon_level = 0

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
    fighter_component = Components.Fighter(hp=10000,
                                           defense=100,
                                           power=200,
                                           xp=0,
                                           death_function=Components.player_death)
    player = Entity.Entity(0, 0, '@', 'player', libtcod.white,
                           blocks=True,
                           ai=Components.PlayeControlled(),
                           fighter=fighter_component)

    starting_equipment()
    player.speed = 10

    player.level = 1
    player.action_points = 100

    Schedule.register(player)
    Schedule.add_to_pq((player.action_points, player))

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
    ranged_component = Components.Ranged(10)
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



def next_level():
    global dungeon_level


    # advance to the next level
    add_msg('You take a moment to rest, and recover your strength.', libtcod.light_violet)
    get_player().fighter.heal(get_player().fighter.max_hp / 2)  # heal the player by 50%
    get_player().action_points = 0
    add_msg('After a rare moment of peace, you descend deeper into the heart of the dungeon...', libtcod.red)
    dungeon_level += 1


    # CAVES ONLY
    # CaveGen.build()
    # Map.translate_map_data()

    # OG MAPS
    #Map.make_map()

    # BSP Maps
    Map.make_bsp()


    # YOU CAN  CA->MAP as map's tiles[][] supercedes maps
    # Map.make_bsp(map=Map.translate_map_data())


    # Cannot MAP -> CA as CA map is not tiles[][]
    # BORKED!
    # CaveGen.build(Map.make_map())

    Fov.initialize()
    # Map.spawn_doors()

    SoundEffects.play_music('SSA')
