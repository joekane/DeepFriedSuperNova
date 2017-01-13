# *******************************************************
# * Copyright (C) 2016-2017 Joe Kane
# *
# * This file is part of 'Deep Fried Supernova"
# *
# * Deep Fried Supernova can not be copied and/or distributed without the express
# * permission of Joe Kane
# *******************************************************/


import math
import GameState
import Components
import libtcodpy as libtcod
import Status
from bltColor import bltColor as Color

# TODO: Need "Inanimate AI" for barrels and the like. They still need fighter component, but should prevent them from being time_travelers.

class Entity:
    # this is a generic object: the player, a monster, an item, the stairs...
    # it's always represented by a character on screen.
    def __init__(self, x, y, char, name, color,
                 speed= 10,
                 blocks=False,
                 blocks_sight=False,
                 delay=0,
                 fighter=None,
                 always_visible=False,
                 ai=None,
                 item=None,
                 equipment=None, ranged=None):
        self.name = name
        self.blocks = blocks
        self.blocks_sight = blocks_sight
        self.x = x
        self.y = y
        self.delay = delay
        self.base_speed = speed
        self.char = char
        self.color = Color(color)
        self.always_visible = always_visible
        self.path = None
        self.status = Status.StatusList()

        # Optional Components
        self.fighter = fighter
        if self.fighter:  # let the fighter component know who owns it
            self.fighter.owner = self

        self.ranged = ranged
        if self.ranged:  # let the fighter component know who owns it
            self.ranged.owner = self

        self.ai = ai
        if self.ai:  # let the AI component know who owns it
            self.ai.owner = self

        self.item = item
        if self.item:  # let the Item component know who owns it
            self.item.owner = self

        self.equipment = equipment
        if self.equipment:  # let the Equipment component know who owns it
            self.equipment.owner = self
            self.item = Components.Item()
            self.item.owner = self


    @property
    def pos(self):
        return self.x, self.y

    @property
    def speed(self):
        spd = self.base_speed
        spd += self.status.get_bonus('SPD', spd)
        return spd


    def pass_time(self, time_units):
        ''' PASSES TIME AT END OF EACH TURN, REGARDLESS OF ACTION (Non-Zero)'''
        self.status.pass_time(time_units)

    def send_to_back(self):
        # make this object be drawn first, so all others appear above it if they're in the same tile.
        objects = GameState.current_level.get_all_objects()
        objects.remove(self)
        objects.insert(0, self)

    def move(self, dx, dy):
        # move by the given amount, if the destination is not blocked
        if not GameState.current_level.is_blocked(self.x + dx, self.y + dy):
            GameState.current_level.fov_change(self.x, self.y, 'Unchanged', False)
            self.x += dx
            self.y += dy
            if self.name != 'player':
                Fov.fov_change(self.x, self.y, 'Unchanged', True)
                pass
            else:
                pass

                #Map.recalc_dmap = True

                # print "d_Map Start."
                # Map.update_d_map()
                # print "d_Map End."
            return True
        else:
            return False

    def move_to(self, x, y):
        # move by the given amount, if the destination is not blocked
        if not GameState.current_level.is_blocked(x, y):
            # Fov.fov_change(self.x, self.y, 'Unchanged', False)
            self.x = x
            self.y = y
            GameState.current_level.require_recompute()
        else:
            return False

    def move_towards(self, target_x, target_y):
        # vector from this object to the target, and distance
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # normalize it to length 1 (preserving direction), then round it and
        # convert to integer so the movement is restricted to the map grid
        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not self.move(dx, dy):
            if dy == 0:
                if not self.move(dx, dy + 1):
                    if not self.move(dx, dy - 1):
                        if not self.move(0, dy + 1):
                            if not self.move(0, dy - 1):
                                if not self.move(-dx, dy - 1):
                                    if not self.move(-dx, dy + 1):
                                        if not self.move(-dx, dy):
                                            pass


            elif dx == 0:
                if not self.move(dx-1, dy):
                    if not self.move(dx+1, dy):
                        if not self.move(dx - 1, 0):
                            if not self.move(dx + 1, 0):
                                if not self.move(dx - 1, -dy):
                                    if not self.move(dx + 1, -dy):
                                        if not self.move(dx, -dy):
                                            pass

    def distance_to(self, other):
        # return the distance to another object
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def distance(self, x, y):
        # return the distance to some coordinates
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def move_astar(self, target):
        import Pathing
        print "Astar for " + self.name

        path = Pathing.astar((self.x, self.y), (target.x, target.y))

        if not path:
            return False

        self.path = libtcod.path_new_using_map(Fov.get_fov_map(), 1.41)
        libtcod.path_compute(self.path, self.x, self.y, target.x, target.y)

        if not libtcod.path_is_empty(self.path) and libtcod.path_size(self.path) < 75:
            self.walk_path()
        else:
            self.move_towards(target.x, target.y)

    def move_dijkstra(self, target):
        self.path = libtcod.dijkstra_new(Fov.get_fov_map(), 1.41)

        libtcod.dijkstra_compute(self.path,self.x, self.y)
        libtcod.dijkstra_path_set(self.path, target.x, target.y)

        self.walk_path()

    def move_astar_xy(self, target_x, target_y, force=False):
        if self.path is None or force:
            # print "a* self.path is None"
            # Create a FOV map that has the dimensions of the map

            if self.x == target_x and self.y == target_y:
                return

            # Allocate a A* path
            # The 1.41 is the normal diagonal cost of moving, it can be set as 0.0 if diagonal moves are prohibited
            my_path = libtcod.path_new_using_map(GameState.current_level.get_fov_map(), 1.41)

            # Compute the path between self's coordinates and the target's coordinates
            libtcod.path_compute(my_path, self.x, self.y, target_x, target_y)

            # Check if the path exists, and in this case, also the path is shorter than 25 tiles
            # The path size matters if you want the monster to use alternative longer paths (for example through
            # other rooms) if for example the player is in a corridor
            # It makes sense to keep path size relatively low to keep the monsters from running around the map if
            # there's an alternative path really far away
            if not libtcod.path_is_empty(my_path):
                self.path = my_path
                return self.walk_path()
            else:
                # Keep the old move function as a backup so that if there are no paths (for example another
                    # monster blocks a corridor)
                # it will still try to move towards the player (closer to the corridor opening)
                self.move_towards(target_x, target_y)
                return False
        else:
            # print "Had path so walked it"
            return self.walk_path()

    def clear_path(self):
        self.path = None

    def walk_path(self):
        if self.path is None:
            GameState.continue_walking = False
        else:
            x, y = libtcod.path_walk(self.path, True)
            if x or y:
                # Set self's coordinates to the next path tile
                # print "Moving To {0}, {1}".format(x, y)
                self.move_to(x, y)
                # print "Path Walk"
                GameState.current_level.require_recompute()
                return True
            self.path = None
            GameState.continue_walking = False
