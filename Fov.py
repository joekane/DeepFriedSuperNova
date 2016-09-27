# *******************************************************
# * Copyright (C) 2016-2017 Joe Kane
# *
# * This file is part of 'Deep Fried Supernova"
# *
# * Deep Fried Supernova can not be copied and/or distributed without the express
# * permission of Joe Kane
# *******************************************************/


import libtcodpy as libtcod
import Constants
import Map
import GameState
import Render

fov_recompute = True
fov_map = None
player = None


def initialize():
    global fov_recompute, fov_map, player
    # unexplored areas start black (which is the default background color)
    from Render import clear_map
    clear_map()
    map = Map.current_map()
    player = GameState.get_player()
    require_recompute()

    fov_map = libtcod.map_new(Constants.MAP_WIDTH, Constants.MAP_HEIGHT)
    for y in range(Constants.MAP_HEIGHT):
        for x in range(Constants.MAP_WIDTH):
            fov_change(x, y, map[x][y].block_sight, map[x][y].blocked)


def fov_change(x,y, blocks_sight, blocks):
    if blocks_sight == 'Unchanged':
        blocks_sight = Map.level_map[x][y].block_sight
        libtcod.map_set_properties(fov_map, x, y, not blocks_sight, not blocks)
    else:
        libtcod.map_set_properties(fov_map, x, y, not blocks_sight, not blocks)


def require_recompute():
    global fov_recompute
    fov_recompute = True


def recompute():
    global fov_recompute

    if fov_recompute:

        fov_recompute = False
        Map.visible_objects = None

        for obj in Map.get_all_objects():
            if obj.name != 'player':
                fov_change(obj.x, obj.y, obj.blocks_sight, obj.blocks)

        # print "COMPUTING FOV!!!"
        libtcod.map_compute_fov(fov_map, player.x, player.y,
                                Constants.TORCH_RADIUS,
                                Constants.FOV_LIGHT_WALLS,
                                Constants.FOV_ALGO)
        Render.clear_map()
        return True
    return False


def is_visible(pos=None, obj=None, ):
    global fov_map
    if pos is None and obj is not None:
        return libtcod.map_is_in_fov(fov_map, obj.x, obj.y)
    elif pos is not None and obj is None:
        return libtcod.map_is_in_fov(fov_map, pos[0], pos[1])


def is_blocked(pos):
    return not libtcod.map_is_walkable(fov_map, pos[0], pos[1])


def get_fov_map():
    return fov_map
