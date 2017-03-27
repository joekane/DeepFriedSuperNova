# coding=utf8
# *******************************************************
# * Copyright (C) 2016-2017 Joe Kane
# *
# * This file is part of 'Deep Fried Supernova"
# *
# * Deep Fried Supernova can not be copied and/or distributed without the express
# * permission of Joe Kane
# *******************************************************/

from bearlibterminal import terminal

import libtcodpy as libtcod

import Constants
import GameState
import Render
from Engine import SoundEffects
from MapGen import Themes
import Engine.Animation_System

terminal.open()
# terminal.set("window: size=80x25, cellsize=auto, title='Omni: menu'; font: default")
# blt.set("window: size=80x25, cellsize=auto, title='Omni: menu'; font: arial.ttf, size=8")  # font: UbuntuMono-R.ttf, size=12"
terminal.set("window: size={0}x{1}, cellsize=auto, title='DFS 2016'; font: .\Fonts\cp437_16x16_alpha_plus.png, size=16x16, codepage=437".format(
             Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))  # font: UbuntuMono-R.ttf, size=12"
# terminal.set("window: size={0}x{1}, cellsize=auto, title='DFS 2016'; font: .\Fonts\yoshis_island_opaque.png, size=9x12, codepage=437".format(Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT))  # font: UbuntuMono-R.ttf, size=12"

terminal.set('input.filter=[keyboard+, mouse+]')
terminal.composition(terminal.TK_ON)
terminal.set('output.vsync=false')
terminal.color("white")
terminal.refresh()

"""
Sound Init
"""
SoundEffects.initilize()

""""
Animation Init
"""
Engine.Animation_System.initilize()

"""
Load Themes from file & set default theme.
"""
Themes.initialize()

"""
ALT-Graphics init
"""
Render.initialize()

# import playground
# playground.play()

"""
Launch Menu
"""
# ECS Hijack
import ECS.ECS
ECS.ECS.game_loop()

# Normal Entry Point
#GameState.main_menu()

"""
Close Window in Exit
"""
terminal.close()


# TODO: Convert all MESSAGES to tagged colored messages (BearLibStyle)
