# *******************************************************
# * Copyright (C) 2016-2017 Joe Kane
# *
# * This file is part of 'Deep Fried Supernova"
# *
# * Deep Fried Supernova can not be copied and/or distributed without the express
# * permission of Joe Kane
# *******************************************************/


import libtcodpy as libtcod
import Components
import Constants
import Fov
import Map
import math
import Render
import random
import GameState


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
        self.color = color
        self.always_visible = always_visible
        self.path = None
        self.status = []

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
    def speed(self):
        spd = self.base_speed
        for st in self.status:
            if 'speed' in st.keys():
                spd += st['speed']
        return spd


    def pass_time(self):
        for st in self.status:
            st['duration'] -= 1

            if 'HP' in st.keys() and self.fighter is not None:
                amount = st['HP']
                if amount < 0:
                    self.fighter.take_damage(amount)
                elif amount > 0:
                    self.fighter.heal(abs(amount))

            if st['duration'] < 0:
                self.status.remove(st)

    def send_to_back(self):
        # make this object be drawn first, so all others appear above it if they're in the same tile.
        objects = Map.get_all_objects()
        objects.remove(self)
        objects.insert(0, self)

    def move(self, dx, dy):
        # move by the given amount, if the destination is not blocked
        if not Map.is_blocked(self.x + dx, self.y + dy):
            Fov.fov_change(self.x, self.y, 'Unchanged', False)
            self.x += dx
            self.y += dy
            if self.name != 'player':
                Fov.fov_change(self.x, self.y, 'Unchanged', True)
                pass
            return True
        else:
            return False

    def move_to(self, x, y):
        # move by the given amount, if the destination is not blocked
        if not Map.is_blocked(x, y):
            Fov.fov_change(self.x, self.y, 'Unchanged', False)
            self.x = x
            self.y = y
            if self.name != 'player':
                Fov.fov_change(self.x, self.y, 'Unchanged', True)
                pass
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
        self.move(dx, dy)

    def distance_to(self, other):
        # return the distance to another object
        dx = other.x - self.x
        dy = other.y - self.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def distance(self, x, y):
        # return the distance to some coordinates
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def move_astar(self, target):

        import astar

        path = astar.astar( (self.x, self.y) , (target.x, target.y))

        if path:
            dest = path[0]
            self.move_towards(dest[0], dest[1])
            print "Path: " + str(path)
        else:
            print "No Path"
        return



        self.path = libtcod.path_new_using_map(Fov.get_fov_map(), 1.5)
        libtcod.path_compute(self.path, self.x, self.y, target.x, target.y)

        if not libtcod.path_is_empty(self.path) and libtcod.path_size(self.path) < 250:
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
            my_path = libtcod.path_new_using_map(Fov.get_fov_map(), 1.41)

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
            # print path
            # Find the next coordinates in the computed full path
            x, y = libtcod.path_walk(self.path, True)
            # print "{0}'s Path: {1}".format(self.name, libtcod.dijkstra_size(self.path))
            #x, y = libtcod.dijkstra_path_walk(self.path)
            if x or y:
                # Set self's coordinates to the next path tile
                print "Moving To {0}, {1}".format(x, y)
                self.move_to(x, y)
                # print "Path Walk"
                Fov.require_recompute()
                return True
            self.path = None
            GameState.continue_walking = False

    def draw(self):
        # set the color and then draw the character that represents this object at its positionss

        if Fov.is_visible(obj=self):
            Render.draw_object(self)
        elif self.always_visible and Map.is_explored(self.x, self.y):
            Render.draw_object(self, visible=False)

    def clear(self):
        # erase the character that represents this object
        Render.blank(self.x, self.y)

