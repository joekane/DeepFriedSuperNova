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
import Constants
import Map
import GameState

fov_recompute = True
fov_map = None


def initialize():
    global fov_recompute, fov_map, map, player
    # unexplored areas start black (which is the default background color)
    from Render import clear_map
    clear_map()
    map = Map.current_map()
    player = GameState.get_player()

    fov_recompute = True

    fov_map = libtcod.map_new(Constants.MAP_WIDTH, Constants.MAP_HEIGHT)
    for y in range(Constants.MAP_HEIGHT):
        for x in range(Constants.MAP_WIDTH):
            libtcod.map_set_properties(fov_map, x, y, not map[x][y].block_sight, not map[x][y].blocked)


def fov_change(x,y, block, sight):
    libtcod.map_set_properties(fov_map, x, y, not sight, not block)


def require_recompute():
    global fov_recompute
    fov_recompute = True


def recompute():
    if fov_recompute:
        libtcod.map_compute_fov(fov_map, player.x, player.y,
                                Constants.TORCH_RADIUS + 5,
                                Constants.FOV_LIGHT_WALLS,
                                Constants.FOV_ALGO)


def is_visible(pos = None, obj = None, ):
    global fov_map
    if pos is None and obj is not None:
        return libtcod.map_is_in_fov(fov_map, obj.x, obj.y)
    elif pos is not None and obj is None:
        return libtcod.map_is_in_fov(fov_map, pos[0], pos[1])

