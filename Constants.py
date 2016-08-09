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

#SOUND
MUSIC_ON = False
SOUND_ON = False

#ANIMATION
ANIMATE_ON = True

# actual size of the window
SCREEN_WIDTH = 120
SCREEN_HEIGHT = 60

# size of the map
MAP_CONSOLE_WIDTH = SCREEN_WIDTH - 20
MAP_CONSOLE_HEIGHT = SCREEN_HEIGHT - 8

MAP_WIDTH = 100 # MIN 70
MAP_HEIGHT = 52 # MIN 40

# sizes and coordinates relevant for the GUI
BAR_WIDTH = 20
PANEL_HEIGHT = 8
PANEL_Y = SCREEN_HEIGHT - PANEL_HEIGHT
MSG_X = BAR_WIDTH + 2
MSG_WIDTH = SCREEN_WIDTH - BAR_WIDTH - 2
MSG_HEIGHT = PANEL_HEIGHT - 1
INVENTORY_WIDTH = 50
CHARACTER_SCREEN_WIDTH = 30
LEVEL_SCREEN_WIDTH = 40

# parameters for dungeon generator
ROOM_MAX_SIZE = 10
ROOM_MIN_SIZE = 6
MAX_ROOMS = 30

DEPTH = 12
MIN_SIZE = 10
FULL_ROOMS = False

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
TORCH_RADIUS = 10  # 15 Def

LIMIT_FPS = 35  # 20 frames-per-second maximum

INSPECTION_DELAY = 0.5