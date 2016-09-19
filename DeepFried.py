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


#############################################
# Initialization & Main Loop
#############################################

# libtcod.console_set_custom_font('terminal10x10_gs_tc.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
libtcod.console_set_custom_font('Fonts/cp437_16x16.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)

libtcod.console_init_root(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT, 'Deep Fried Supernova', False)
libtcod.sys_set_fps(Constants.LIMIT_FPS)
libtcod.sys_force_fullscreen_resolution(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT)

SoundEffects.initilize()
Themes.initialize()

import Keys

UI.Display_MainMenu()

