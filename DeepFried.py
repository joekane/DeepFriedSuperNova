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
from bearlibterminal import terminal
import Constants
import SoundEffects
import Themes
import GameState
import graphics


term = "BEAR"


if term == "TCOD":
    """
    LIBTCOD Init stuff
    """
    # libtcod.console_set_custom_font('terminal10x10_gs_tc.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.console_set_custom_font('Fonts/cp437_16x16.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
    libtcod.console_init_root(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT, 'Deep Fried Supernova', False)
    libtcod.sys_set_fps(Constants.LIMIT_FPS)
    libtcod.sys_force_fullscreen_resolution(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT)




"""
Sound Init
"""
SoundEffects.initilize()

"""
Load Themes from file & set default theme.
"""
Themes.initialize()


"""
ALT-Graphics init
"""
# graphics.initilize()  # PYGAME



terminal.open()
    # blt.set("window: size=80x25, cellsize=auto, title='Omni: menu'; font: default")
    # blt.set("window: size=80x25, cellsize=auto, title='Omni: menu'; font: arial.ttf, size=8")  # font: UbuntuMono-R.ttf, size=12"
terminal.set("window: size={0}x{1}, cellsize=auto, title='DFS 2016'; font: .\Fonts\cp437_16x16_alpha.png, size=16x16, codepage=437".format(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))  # font: UbuntuMono-R.ttf, size=12"
terminal.set('input.filter=[keyboard+, mouse]')
terminal.composition(terminal.TK_ON)
terminal.color("white")
terminal.refresh()




"""
Launch Menu
"""
GameState.main_menu()

terminal.close()

