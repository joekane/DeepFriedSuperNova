# *******************************************************
# * Copyright (C) 2016-2017 Joe Kane
# *
# * This file is part of 'Deep Fried Supernova"
# *
# * Deep Fried Supernova can not be copied and/or distributed without the express
# * permission of Joe Kane
# *******************************************************/


# -*- coding: utf-8 -*-
import libtcodpy as libtcod
import Constants
import SoundEffects
import Themes
import UI
import Noise


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

# libtcod.console_set_custom_font('terminal10x10_gs_tc.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_set_custom_font('cp437_16x16.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)

libtcod.console_init_root(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT, 'Deep Fried Supernova', False)
libtcod.sys_set_fps(Constants.LIMIT_FPS)

SoundEffects.initilize()
Themes.initialize()
Noise.initialze()

UI.Display_MainMenu()

