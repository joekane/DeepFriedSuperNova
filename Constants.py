# *******************************************************
# * Copyright (C) 2016-2017 Joe Kane
# *
# * This file is part of 'Deep Fried Supernova"
# *
# * Deep Fried Supernova can not be copied and/or distributed without the express
# * permission of Joe Kane
# *******************************************************/
import libtcodpy as libtcod

DEBUG = False


TURN_COST = 100
BASE_SPEED = 10

#SOUND
MUSIC_ON = False
SOUND_ON = False

#ANIMATION
ANIMATE_ON = True

# actual size of the window
SCREEN_WIDTH = 100 # 100
SCREEN_HEIGHT = 50 # 100

PANEL_HEIGHT = 12
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT

# size of the map
MAP_CONSOLE_WIDTH = SCREEN_WIDTH - 19
MAP_CONSOLE_HEIGHT = SCREEN_HEIGHT - PANEL_HEIGHT

MAP_WIDTH = MAP_CONSOLE_WIDTH * 3 # 150 # MIN 70
MAP_HEIGHT = MAP_CONSOLE_HEIGHT * 3 # 150 # MIN 40

# sizes and coordinates relevant for the GUI
BAR_WIDTH = 20

MSG_X = 1
MSG_WIDTH = 57
MSG_HEIGHT = PANEL_HEIGHT - 4
# INVENTORY_WIDTH = 50
# CHARACTER_SCREEN_WIDTH = 30
# LEVEL_SCREEN_WIDTH = 40

# parameters for dungeon generator
ROOM_MAX_SIZE = 9
ROOM_MIN_SIZE = 5
MAX_ROOMS = (MAP_HEIGHT * MAP_WIDTH / 1000) + 500

DEPTH = 25
MIN_SIZE = 5
FULL_ROOMS = True

# spell values
HEAL_AMOUNT = 40
LIGHTNING_DAMAGE = 40
LIGHTNING_RANGE = 5
CONFUSE_RANGE = 8
CONFUSE_NUM_TURNS = 10
FIREBALL_RADIUS = 3
FIREBALL_DAMAGE = 25

# experience and level-ups - TEMP
LEVEL_UP_BASE = 5000
LEVEL_UP_FACTOR = 5000

FOV_ALGO = 0  # default FOV algorithm
FOV_LIGHT_WALLS = True  # light walls or not
TORCH_RADIUS = 15  # 15 Def

LIMIT_FPS = 0 # 20 frames-per-second maximum

INSPECTION_DELAY = 0.5

# COLORS
UI_Fore = libtcod.Color(0, 50, 90)
UI_Back = libtcod.Color(0, 10, 25)

UI_Button_Fore = libtcod.light_red
UI_Button_Back = libtcod.dark_azure

UI_PopFore = libtcod.azure
UI_PopBack = libtcod.darkest_azure

# PATHFINDING
BFS_MAX_DISTANCE = 50


# BOX CHARS
BOX_W = 0x2502
BOX_NW = 0x250C
BOX_N = 0x2500
BOX_NE = 0x2510

BOX_E = 0x2502
BOX_SE = 0x2518
BOX_S = 0x2500
BOX_SW = 0x2514
