# *******************************************************
# * Copyright (C) 2016-2017 Joe Kane
# *
# * This file is part of 'Deep Fried Supernova"
# *
# * Deep Fried Supernova can not be copied and/or distributed without the express
# * permission of Joe Kane
# *******************************************************/


import gzip
import random
import Render
import Constants
import Entities.Entity as Entity
import Entities.Components as Components
import Entities.Spells as Spells
import Entities.Entity
import GameState
import Utils
import libtcodpy as libtcod
import xp_loader
from MapGen import CaveGen, SpanningTree, Prefabs, Noise, Themes

level_map = []


class World:
    def __init__(self, name, tags):
        self.name = name
        self.tags = tags
        self.levels = []


class Level:
    def __init__(self, name):
        self.name = name
        self.map_array = None
        self.objects = []
        self.visible_objects = []
        self.stairs_down = None
        self.stairs_up = None
        self.player = None
        self.fov_recompute_required = True
        self.fov_map = None

    def initialize(self, player, generator):
        self.player = player
        self.objects = [player]
        self.map_array = generator(self)
        self.fov_initialize()
        self.recompute_fov()

    @property
    def resoures(self):
        return self.map_array, self.objects, self.player

    def fov_initialize(self):
        self.fov_recompute_required = True
        self.fov_map = libtcod.map_new(Constants.MAP_WIDTH, Constants.MAP_HEIGHT)
        for y in range(Constants.MAP_HEIGHT):
            for x in range(Constants.MAP_WIDTH):
                self.fov_change(x, y, self.map_array[x][y].block_sight, self.map_array[x][y].blocked)

    def fov_change(self, x, y, blocks_sight, blocks):
        if blocks_sight == 'Unchanged':
            blocks_sight = self.map_array[x][y].block_sight
            libtcod.map_set_properties(self.fov_map, x, y, not blocks_sight, not blocks)
        else:
            libtcod.map_set_properties(self.fov_map, x, y, not blocks_sight, not blocks)

    def is_visible(self, pos=None, obj=None, ):
        if pos is None and obj is not None:
            return libtcod.map_is_in_fov(self.fov_map, obj.x, obj.y)
        elif pos is not None and obj is None:
            return libtcod.map_is_in_fov(self.fov_map, pos[0], pos[1])

    def require_recompute(self):
        self.fov_recompute_required = True

    def recompute_fov(self):
        if self.fov_recompute_required:
            self.fov_recompute_required = False
            self.visible_objects = None

            for obj in self.get_all_objects():
                if obj.name != 'player':
                    self.fov_change(obj.x, obj.y, obj.blocks_sight, obj.blocks)

            # print "COMPUTING FOV!!!"
            libtcod.map_compute_fov(self.fov_map, self.player.x, self.player.y,
                                    Constants.TORCH_RADIUS,
                                    Constants.FOV_LIGHT_WALLS,
                                    Constants.FOV_ALGO)
            # Render.clear_map()
            return True
        return False

    def get_fov_map(self):
        return self.fov_map

    def draw(self):
        self.draw_map()
        self.draw_objects()

    def draw_objects(self):
        # libtcod.console_clear(consoles['entity_console'])
        Render.clear_layer(Render.layers['entity_console'])
        for object in self.get_all_objects():
            if object != GameState.get_player():
                if self.is_visible(obj=object):
                    Render.draw_object(object)
                elif object.always_visible and self.is_explored(object.x, object.y):
                    Render.draw_object(object, visible=False)
        Render.draw_object(self.player)

    def clear_object(self, object):
        # erase the character that represents this object
        Render.blank(object.x, object.y)

    def get_open_tiles(self):
        open_nodes = []

        for y in range(Constants.MAP_HEIGHT):
            for x in range(Constants.MAP_WIDTH):
                if not self.map_array[x][y].blocked:
                    open_nodes.append(level_map[x][y])

        return open_nodes

    def has_cross_blocked(self, x, y):
        if self.map_array[x - 1][y].blocked and level_map[x + 1][y].blocked:
            return True
        elif self.map_array[x][y - 1].blocked and level_map[x][y + 1].blocked:
            return True
        return False

    def get_total_blocked_corners(self, x, y):
        count = 0
        if self.map_array[x - 1][y - 1].blocked:
            count += 1
        if self.map_array[x + 1][y - 1].blocked:
            count += 1
        if self.map_array[x - 1][y + 1].blocked:
            count += 1
        if self.map_array[x + 1][y + 1].blocked:
            count += 1
        return count

    def is_explored(self, x, y):
        # first test the map tile
        if self.map_array[x][y].explored:
            return True

        return False

    def is_blocked(self, x, y, ignore_mobs=False):
        # first test the map tile
        try:
            if self.map_array[x][y].blocked:
                # print "Blocked By Map!"
                return True
            # now check for any blocking objects
            if not ignore_mobs:
                for object in self.get_all_objects():
                    if object.blocks and object.x == x and object.y == y:
                        # print "Blocked by Object!"
                        return True
        except:
            return True
        return False

    def directly_adjacent_open_tiles(self, obj):
        open_tiles = []

        if (not self.is_blocked(obj.x, obj.y - 1)):
            open_tiles.append([obj.x, obj.y - 1])
        if (not self.is_blocked(obj.x + 1, obj.y)):
            open_tiles.append([obj.x + 1, obj.y])
        if (not self.is_blocked(obj.x - 1, obj.y + 1)):
            open_tiles.append([obj.x - 1, obj.y + 1])
        if (not self.is_blocked(obj.x, obj.y + 1)):
            open_tiles.append([obj.x, obj.y + 1])

        if (len(open_tiles) == 0):
            return [None, None]

        choice = random.choice(open_tiles)
        # print(choice)
        return choice

    def adjacent_open_tiles(self, obj):
        open_tiles = []

        if not self.is_blocked(obj.x - 1, obj.y - 1):
            open_tiles.append([obj.x - 1, obj.y - 1])
        if (not self.is_blocked(obj.x, obj.y - 1)):
            open_tiles.append([obj.x, obj.y - 1])
        if (not self.is_blocked(obj.x + 1, obj.y - 1)):
            open_tiles.append([obj.x + 1, obj.y - 1])
        if (not self.is_blocked(obj.x - 1, obj.y - 1)):
            open_tiles.append([obj.x - 1, obj.y - 1])
        if (not self.is_blocked(obj.x + 1, obj.y)):
            open_tiles.append([obj.x + 1, obj.y])
        if (not self.is_blocked(obj.x - 1, obj.y + 1)):
            open_tiles.append([obj.x - 1, obj.y + 1])
        if (not self.is_blocked(obj.x, obj.y + 1)):
            open_tiles.append([obj.x, obj.y + 1])
        if (not self.is_blocked(obj.x + 1, obj.y + 1)):
            open_tiles.append([obj.x + 1, obj.y + 1])
        if (len(open_tiles) == 0):
            return [None, None]

        choice = random.choice(open_tiles)
        # print(choice)
        return choice

    def target_tile(self, max_range=None):
        # TODO: This goes somewhere else
        # return the position of a tile left-clicked in player's FOV (optionally in a range), or (None,None) if right-clicked.
        mouse = libtcod.Mouse()
        key = libtcod.Key()

        while True:
            # render the screen. this erases the inventory and shows the names of objects under the mouse.
            libtcod.console_flush()
            libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

            (x, y) = (mouse.cx, mouse.cy)

            # accept the target if the player clicked in FOV, and in case a range is specified, if it's in that range
            if (mouse.lbutton_pressed and self.is_visible(x, y) and
                    (max_range is None or GameState.get_player().distance(x, y) <= max_range)):
                return (x, y)
            if mouse.rbutton_pressed or key.vk == libtcod.KEY_ESCAPE:
                return (None, None)  # cancel if the player right-clicked or pressed Escape

    def target_monster(self, max_range=None):
        # returns a clicked monster inside FOV up to a range, or None if right-clicked
        while True:
            (x, y) = self.target_tile(max_range)
            if x is None:  # player cancelled
                return None

            # return the first clicked monster, otherwise continue looping
            for obj in self.get_visible_objects():
                if obj.x == x and obj.y == y and obj.fighter and obj != GameState.get_player():
                    return obj

    def get_monster_at(self, pos):
        for obj in self.visible_objects:
            if obj.x == pos[0] and obj.y == pos[1] and obj.fighter is not None:
                return obj

    def get_stairs(self):
        return self.stairs_down

    def get_all_objects(self):
        return self.objects

    def get_visible_objects(self):
        if self.visible_objects is None:
            self.visible_objects = [obj for obj in self.objects if self.is_visible(obj=obj)]
            if self.visible_objects is None:
                return self.objects
            else:
                return self.visible_objects
        else:
            return self.visible_objects

    def closest_monster(self, max_range):
        # find closest enemy, up to a maximum range, and in the player's FOV
        closest_enemy = None
        closest_dist = max_range + 1  # start with (slightly more than) maximum range
        for object in self.get_visible_objects():
            if object.fighter and not object == self.player and self.is_visible(obj=object):
                # calculate distance between this object and the player
                dist = self.player.distance_to(object)
                if dist < closest_dist:  # it's closer, so remember it
                    closest_enemy = object
                    closest_dist = dist
        return closest_enemy

    def closest_monsters(self, max_range):
        closest_dist = max_range + 1  # start with (slightly more than) maximum range

        monsters = []

        for object in self.get_visible_objects():
            if object.fighter and not object == self.player and self.is_visible(obj=object):
                dist = self.player.distance_to(object)
                if dist <= max_range:
                    monsters.append((object, dist))

        monsters.sort(key=lambda tup: tup[1])

        print "Monsters: {0}".format(monsters)
        return monsters

    def draw_map(self):

        if self.recompute_fov():

            Render.clear_layer(0)

            map = self.map_array
            player = self.player
            GameState.move_camera(player.x, player.y)
            camera_x, camera_y = GameState.get_camera()

            # Map.d_map[player.x][player.y] = 0

            for y in range(Constants.MAP_CONSOLE_HEIGHT):
                for x in range(Constants.MAP_CONSOLE_WIDTH):

                    map_x, map_y = (camera_x + x, camera_y + y)
                    tile = map[map_x][map_y]
                    visible = self.is_visible(pos=(map_x, map_y))

                    # dist = Utils.distance_between(player.x, player.y, map_x, map_y)
                    # Map.d_map[map_x][map_y] = int(dist)

                    if Constants.DEBUG:
                        # print "IF - Should be Drawing!!!"
                        if self.is_blocked(map_x, map_y):
                            Render.draw_char(Render.layers['map_console'], x, y, '*',
                                             tile.f_color, libtcod.BKGND_SET)
                        # else:
                        if True:
                            dist = self.map_array[map_x][map_y].distance_to_player

                            char = chr(min(dist + 48, 200))  # chr(min(Map.d_map[map_x][map_y] + 48, 200))
                            if dist == -1:
                                char = ' '
                            c_value = max(dist, 0)  # max(Map.d_map[map_x][map_y] , 0)

                            # char = hm_values[min(c_value, len(hm_values) - 1)]
                            db_color = Utils.heat_map_colors[min(c_value, len(Utils.heat_map_colors) - 1)]

                            Render.draw_char(Render.layers['map_console'], x, y, char,
                                             db_color, libtcod.BKGND_SET)

                    else:
                        # print "ELSE - Should be Drawing!!!"
                        if not visible:
                            if tile.explored:
                                if tile.blocked:
                                    char = tile.char
                                    f_color = libtcod.Color(50, 50, 50)
                                    b_color = libtcod.Color(10, 10, 10)
                                else:
                                    char = '.'
                                    f_color = libtcod.Color(50, 50, 50)
                                    b_color = libtcod.Color(0, 0, 0)

                                Render.draw_char(Render.layers['map_console'], x, y, char,
                                                 f_color, libtcod.BKGND_SET)
                                Render.draw_background(Render.layers['map_console'], x, y,
                                                       b_color, flag=libtcod.BKGND_SET)
                                # libtcod.console_put_char_ex(consoles['map_console'], x, y, char,
                                #                            Themes.OUT_OF_FOV_COLOR, libtcod.BKGND_SET)
                            #print "Invis....."
                        else:
                            offset_color = Utils.get_offset_color(map_x, map_y, self.player.x, self.player.y)

                            Render.draw_char(Render.layers['map_console'], x, y, tile.char,
                                             tile.f_color - offset_color, libtcod.BKGND_SET)
                            Render.draw_background(Render.layers['map_console'], x, y,
                                                   tile.b_color - offset_color, flag=libtcod.BKGND_SET)
                            '''
                            Render.draw_background(Render.layers['map_console'], x, y,
                                                   libtcod.light_gray, flag=libtcod.BKGND_SET)
                            Render.draw_char(Render.layers['map_console'], x, y, tile.char,
                                             libtcod.white, libtcod.BKGND_SET)
                            '''


                            tile.explored = True


class Tile:
    # a tile of the map and its properties
    def __init__(self, blocked, block_sight=None, char=' ', f_color=Themes.ground_color(), b_color=libtcod.black,
                 pos_x=0,
                 pos_y=0):
        self.x = pos_x
        self.y = pos_y
        self.blocked = blocked
        self.explored = False
        self.char = char
        self.f_color = f_color
        self.b_color = b_color

        # by default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked
        self.block_sight = block_sight
        self.distance_to_player = -1


class Rect:

    # a rectangle on the map. used to characterize a room.
    def __init__(self, x, y, w, h):
        import sys
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
        self.adjacent = {}
        # Set distance to infinity for all nodes
        self.distance = sys.maxint
        # Mark all nodes unvisited
        self.visited = False
        # Predecessor
        self.previous = None
        self.id = None

    def center(self):
        center_x = (self.x1 + self.x2) / 2
        center_y = (self.y1 + self.y2) / 2
        return center_x, center_y

    def intersect(self, other):
        # returns true if this rectangle intersects with another one
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and
                self.y1 <= other.y2 and self.y2 >= other.y1)

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_weight(self, neighbor):
        # print "Weight: " + str(self.adjacent[neighbor])
        return self.adjacent[neighbor]

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True

    @property
    def width(self):
        return self.x2 - self.x1

    @property
    def height(self):
        return self.y2 - self.y1


def new_map(solid=True):
    # TODO: Create craible sized maps
    level_map = []

    if solid:
        level_map = [[Tile(True,
                           block_sight=True,
                           char=Themes.wall_char(),
                           f_color=Themes.wall_color(),
                           b_color=Themes.wall_bcolor(),
                           pos_x=x,
                           pos_y=y)
                      for y in range(Constants.MAP_HEIGHT)] for x in range(Constants.MAP_WIDTH)]
    else:
        level_map = [[Tile(False,
                           block_sight=False,
                           char=Themes.wall_char(),
                           f_color=Themes.wall_color(),
                           b_color=Themes.wall_bcolor(),
                           pos_x=x,
                           pos_y=y)
                      for y in range(Constants.MAP_HEIGHT)] for x in range(Constants.MAP_WIDTH)]
    return level_map


def load_prefab(level_map, x, y, key, rotation):
    room_type = Prefabs.get_prefab(key)

    xp_file = gzip.open('Levels\_' + room_type + '.xp')
    raw_data = xp_file.read()
    xp_file.close()

    xp_data = xp_loader.load_xp_string(raw_data)

    # xp_loader.load_layer_to_console(layer_0_console, xp_data['layer_data'][0])
    # xp_loader.load_layer_to_console(layer_1_console, xp_data['layer_data'][1])

    # print "XP:"
    # print len(xp_data['layer_data'])

    map_x = x
    map_y = y

    level_map = xp_loader.load_layer_to_map(level_map, map_x, map_y, xp_data['layer_data'][0],
                                                   rotation=rotation)
    if len(xp_data['layer_data']) >= 2:
        xp_objects = xp_loader.load_layer_to_objects(level_map, map_x, map_y, xp_data['layer_data'][1],
                                                            rotation=rotation)
        for obj in xp_objects:
            if obj[0] == 'door':
                # TODO: Randomly Select +'s for doors and spit it back out for connection data

                # spawn_door_at(obj[1][0], obj[1][1], 'Door')
                create_ground(obj[1][0], obj[1][1])
                pass

    if len(xp_data['layer_data']) >= 3:
        level_map = xp_loader.load_layer_to_map_cosmetic(level_map, map_x, map_y, xp_data['layer_data'][2],
                                                                rotation=rotation)


# MAIN METHOD TO CALL LEVEL GEN BASED ON THEME
def generate_map():
    level = random.choice(Themes.LEVEL_STYLE)

    level = 'BSP'

    new_map()

    if level == 'BSP':
        #bsp_dungeon()
        #basic_dungeon()
        mst_dungeon()
        #pre_fabs_v2()
        #spawn_doors()
        #Engine.Fov.require_recompute()
    elif level == 'CAVEGEN':
        CaveGen.build()
        read_cavegen_data()
    elif level == 'CAVE_TIGHT': # FUN?
        caves(style='TIGHT')

        # drunk_walk()
        # basic_dungeon()
        # spawn_doors()

    elif level == 'WILD': # EMPTY.....
        wilderness()
    elif level == 'CAVE_OPEN':  # SUCKS
        caves(style='OPEN')
        basic_dungeon()
    #Engine.Fov.initialize()

    # update_dmap()
    #Engine.SoundEffects.play_music('SSA')


def caves(style='DEFAULT'):
    global objects, level_map, stairs

    if style == 'DEFAULT':
        Noise.initialze(scale=10)
    elif style == 'OPEN':
        Noise.initialze(scale=15)
    elif style == 'TIGHT':
        Noise.initialze(scale=5)

    player = GameState.get_player()
    objects = [player]

    for x in range(1, Constants.MAP_WIDTH-1):
        for y in range(1, Constants.MAP_HEIGHT-1):
            pre_value = Noise.get_height_value(x, y)

            if 0.52 <= pre_value < 1:
                create_ground(x, y)


def wilderness():
    global objects, level_map, stairs

    Noise.initialze(scale=100)

    player = GameState.get_player()
    objects = [player]

    for x in range(Constants.MAP_WIDTH):
        for y in range(Constants.MAP_HEIGHT):
            pre_value = Noise.get_height_value(x, y)
            # print pre_value

            if 0 <= pre_value < 0.1:
                level_map[x][y] = Tile(False,
                                       block_sight=False,
                                       char='~',
                                       f_color=libtcod.darker_blue,
                                       b_color=libtcod.black,
                                       pos_x=x,
                                       pos_y=y)
            elif 0.1 <= pre_value < 0.2:
                level_map[x][y] = Tile(False,
                                       block_sight=False,
                                       char='~',
                                       f_color=libtcod.dark_blue,
                                       b_color=libtcod.black,
                                       pos_x=x,
                                       pos_y=y)
            elif 0.2 <= pre_value < 0.3:
                level_map[x][y] = Tile(False,
                                       block_sight=False,
                                       char='~',
                                       f_color=libtcod.blue,
                                       b_color=libtcod.black,
                                       pos_x=x,
                                       pos_y=y)
            elif 0.3 <= pre_value < 0.4:
                level_map[x][y] = Tile(False,
                                       block_sight=False,
                                       char='%',
                                       f_color=libtcod.blue,
                                       b_color=libtcod.black,
                                       pos_x=x,
                                       pos_y=y)
            elif 0.4 <= pre_value < 0.5:
                level_map[x][y] = Tile(False,
                                       block_sight=False,
                                       char='~',
                                       f_color=libtcod.light_blue,
                                       b_color=libtcod.black,
                                       pos_x=x,
                                       pos_y=y)
            elif 0.5 <= pre_value < 0.6:
                level_map[x][y] = Tile(False,
                                       block_sight=False,
                                       char=';',
                                       f_color=libtcod.light_green,
                                       b_color=libtcod.black,
                                       pos_x=x,
                                       pos_y=y)
            elif 0.6 <= pre_value < 0.7:
                level_map[x][y] = Tile(False,
                                       block_sight=False,
                                       char=',',
                                       f_color=libtcod.green,
                                       b_color=libtcod.black,
                                       pos_x=x,
                                       pos_y=y)
            elif 0.7 <= pre_value < 0.90:
                level_map[x][y] = Tile(False,
                                       block_sight=False,
                                       char='*',
                                       f_color=libtcod.dark_green,
                                       b_color=libtcod.black,
                                       pos_x=x,
                                       pos_y=y)
            elif 0.90 <= pre_value < 0.999:
                level_map[x][y] = Tile(False,
                                       block_sight=False,
                                       char='^',
                                       f_color=libtcod.dark_sepia,
                                       b_color=libtcod.black,
                                       pos_x=x,
                                       pos_y=y)
            else:
                level_map[x][y] = Tile(False,
                                       block_sight=False,
                                       char='^',
                                       f_color=libtcod.dark_grey,
                                       b_color=libtcod.black,
                                       pos_x=x,
                                       pos_y=y)
            level_map[x][y].explored = True


def read_cavegen_data(): # OBSOLETE?
    global objects, level_map, stairs

    data = CaveGen.get_level_data()

    player = GameState.get_player()
    objects = [player]

    for x in range(Constants.MAP_WIDTH):
        for y in range(Constants.MAP_HEIGHT):
            if data[x][y] != 1:
                create_ground(x, y)
            elif data[x][y] == 2:
                level_map[x][y] = Tile(False,
                                       block_sight=False,
                                       char='x',
                                       f_color=Themes.ground_color(),
                                       b_color=Themes.ground_bcolor(),
                                       pos_x=x,
                                       pos_y=y)
            elif data[x][y] == 4:
                player.x, player.y = x, y

                level_map[x][y] = Tile(False,
                                       block_sight=False,
                                       char='c',
                                       f_color=Themes.ground_color(),
                                       b_color=Themes.ground_bcolor(),
                                       pos_x=x,
                                       pos_y=y)
            level_map[x][y].explored = False

    return level_map


def load_diner_map():
    global objects, level_map, stairs

    level = GameState.current_level
    player = GameState.get_player()
    objects = [player]

    player.x = 10
    player.y = 4

    file = open('Assets\Levels\diner.map', 'r')

    Themes.set_theme('Diner')

    new_map()

    y = 0

    for l in range(Constants.MAP_HEIGHT):
        line = file.readline()
        x = 0
        for c in line:
            if c == ' ':
                #print(str(x) + " " + str(y))
                create_ground(x, y)
            if c == 'D':
                #print(str(x) + "+" + str(y))
                level_map[x][y].blocked = False
                level_map[x][y].block_sight = True
            if c == '-':
                #print(str(x) + "-" + str(y))
                level_map[x][y].blocked = True
                level_map[x][y].block_sight = False
            if c == '|':
                #print(str(x) + "|" + str(y))
                level_map[x][y].blocked = True
                level_map[x][y].block_sight = False
            if c == '*':
                #print(str(x) + "|" + str(y))
                level_map[x][y].blocked = True
                level_map[x][y].block_sight = False
            if c == 'p':
                create_ground(x, y)
                player.x = x
                player.y = y
            if c == 'Q':
                create_ground(x, y)
                spawn_npc_at(level, x, y, 'QuestGuy')
            if c == '+':
                create_ground(x, y)
                spawn_npc_at(level, x, y, 'UnlockedDoor')
            if c == '_':
                create_ground(x, y)
                spawn_npc_at(level, x, y, 'OpenDoor')
            if c == 's':

                create_ground(x, y)
                stairs = Entities.Entity.Entity(x, y, '<', 'stairs', libtcod.white, always_visible=True)
                objects.append(stairs)
            x += 1
        y += 1


def basic_dungeon(level):
    global level_map, objects, stairs

    player = GameState.get_player()

    objects = [player]

    rooms = []
    num_rooms = 0

    for r in range(Constants.MAX_ROOMS):
        # random width and height
        w = libtcod.random_get_int(0, Constants.ROOM_MIN_SIZE, Constants.ROOM_MAX_SIZE)
        h = libtcod.random_get_int(0, Constants.ROOM_MIN_SIZE, Constants.ROOM_MAX_SIZE)
        # random position without going out of the boundaries of the map
        x = libtcod.random_get_int(0, 0, Constants.MAP_WIDTH - w - 1)
        y = libtcod.random_get_int(0, 0, Constants.MAP_HEIGHT - h - 1)
        # "Rect" class makes rectangles easier to work with
        new_room = Rect(x, y, w, h)

        # run through the other rooms and see if they intersect with this one
        failed = False
        for other_room in rooms:
            if new_room.intersect(other_room):
                failed = True
                break

        if not failed:
            # this means there are no intersections, so this room is valid

            # "paint" it to the map's tiles
            create_room(new_room)

            # center coordinates of new room, will be useful later
            (new_x, new_y) = new_room.center()
            # optional: print "room number" to see how the map drawing worked
            #          we may have more than ten rooms, so print 'A' for the first room, 'B' for the next...
            # room_no = Object(new_x, new_y, chr(65+num_rooms), 'Room #', libtcod.white)
            # objects.insert(0, room_no) #draw early, so monsters are drawn on top


            if num_rooms == 0:
                # this is the first room, where the player starts at
                player.x = new_x
                player.y = new_y
            else:
                # all rooms after the first:
                # connect it to the previous room with a tunnel

                # center coordinates of previous room
                (prev_x, prev_y) = rooms[num_rooms - 1].center()

                # draw a coin (random number that is either 0 or 1)
                if libtcod.random_get_int(0, 0, 1) == 1:
                    # first move horizontally, then vertically
                    create_h_tunnel(prev_x, new_x, prev_y)
                    create_v_tunnel(prev_y, new_y, new_x)
                else:
                    # first move vertically, then horizontally
                    create_v_tunnel(prev_y, new_y, prev_x)
                    create_h_tunnel(prev_x, new_x, new_y)
            # add some contents to this room, such as monsters
            place_objects(level, new_room)
            # finally, append the new room to the list
            rooms.append(new_room)
            num_rooms += 1

    # create stairs at the center of the last room
    stairs = Entities.Entity.Entity(new_x, new_y, '<', 'stairs', libtcod.white, always_visible=True)
    objects.append(stairs)
    stairs.send_to_back()  # so it's drawn below the monsters
    return level_map


def mst_dungeon(level):
    global level_map

    level.map_array = new_map()
    level_map = level.map_array
    player = level.player
    objects = level.objects

    num_rooms = 0

    g = SpanningTree.Graph()

    for r in range(Constants.MAX_ROOMS):
        # random width and height
        w = libtcod.random_get_int(0, Constants.ROOM_MIN_SIZE, Constants.ROOM_MAX_SIZE)
        h = libtcod.random_get_int(0, Constants.ROOM_MIN_SIZE, Constants.ROOM_MAX_SIZE)
        # random position without going out of the boundaries of the map
        x = libtcod.random_get_int(0, 0, Constants.MAP_WIDTH - w - 1)
        y = libtcod.random_get_int(0, 0, Constants.MAP_HEIGHT - h - 1)
        # "Rect" class makes rectangles easier to work with
        new_room = Rect(x, y, w, h)

        # run through the other rooms and see if they intersect with this one
        failed = False
        for other_room in g.room_list:
            if new_room.intersect(other_room):
                failed = True
                break

        if not failed:
            # Add room to MST graph
            g.add_room(new_room, num_rooms)

            # Carve room in level
            create_room(new_room)
            # print "Place things....."
            place_objects(level, new_room)
            num_rooms += 1

    # add Player to fist room
    (new_x, new_y) = g.room_list[0].center()
    player.x = new_x
    player.y = new_y


    # import plot_test
    triangles = SpanningTree.get_triangles(g.room_list)

    for tri in triangles:
        new_room = g.room_list[tri[0]]
        lastRoom = g.room_list[tri[1]]
        g.add_room_edge(new_room, lastRoom, Utils.distance_between(new_room.x1, new_room.x2,
                                                                   lastRoom.x1, lastRoom.x2))

        new_room = g.room_list[tri[1]]
        lastRoom = g.room_list[tri[2]]
        g.add_room_edge(new_room, lastRoom, Utils.distance_between(new_room.x1, new_room.x2,
                                                                   lastRoom.x1, lastRoom.x2))

        new_room = g.room_list[tri[2]]
        lastRoom = g.room_list[tri[0]]
        g.add_room_edge(new_room, lastRoom, Utils.distance_between(new_room.x1, new_room.x2,
                                                                   lastRoom.x1, lastRoom.x2))

    SpanningTree.calculate_all_paths(g, g.room_list[0])

    #room = g.room_list[3]
    for room in g.room_list:
        path = [room.center()]
        SpanningTree.shortest(room, path)
        # print 'The shortest path for %s : %s' % (room.center(), path[::-1])

        s_node = None
        for node in path:

            if s_node is not None:
                # TODO: Need better tunnels
                # Line Tunnels
                #create_tunnel(s_node, node)

                # Shitty L Tunnels
                if libtcod.random_get_int(0, 0, 1) == 1:
                    # first move horizontally, then vertically
                    create_h_tunnel(s_node[0], node[0], s_node[1])
                    create_v_tunnel(s_node[1], node[1], node[0])
                else:
                    # first move vertically, then horizontally
                    create_v_tunnel(s_node[1], node[1], s_node[0])
                    create_h_tunnel(s_node[0], node[0], node[1])

            s_node = node

    (new_x, new_y) = g.room_list[-1].center()
    # create stairs at the center of the last room
    stairs = Entities.Entity.Entity(new_x, new_y, '<', 'stairs', libtcod.white, always_visible=True)
    objects.append(stairs)
    stairs.send_to_back()  # so it's drawn below the monsters
    GameState.current_level.stairs_down = stairs
    return level_map


def bsp_dungeon(level):
    global level_map, objects, stairs, bsp_rooms

    player = GameState.get_player()

    objects = [player]

    # Empty global list for storing room coordinates
    bsp_rooms = []

    # New root node
    bsp = libtcod.bsp_new_with_size(0, 0, Constants.MAP_WIDTH, Constants.MAP_HEIGHT)

    # Split into nodes
    libtcod.bsp_split_recursive(bsp, 0, Constants.DEPTH, Constants.MIN_SIZE + 1, Constants.MIN_SIZE + 1, 1.5, 1.5)

    # Traverse the nodes and create rooms
    libtcod.bsp_traverse_inverted_level_order(bsp, traverse_node)
    # print "ROOMS:"
    # print bsp_rooms

    # Random room for the stairs
    stairs_location = random.choice(bsp_rooms)
    bsp_rooms.remove(stairs_location)
    stairs = Entities.Entity.Entity.Entity(stairs_location[0], stairs_location[1], '<', 'stairs', libtcod.white, always_visible=True)
    objects.append(stairs)
    stairs.send_to_back()

    # Random room for player start
    player_room = random.choice(bsp_rooms)
    bsp_rooms.remove(player_room)
    player.x = player_room[0]
    player.y = player_room[1]

    # Add monsters and items
    for room in bsp_rooms:
        new_room = Rect(room[0], room[1], 5, 5)
        place_objects(level, new_room)

    # Engine.Fov.require_recompute()


def traverse_node(node, dat):
    global level_map, bsp_rooms

    # Create rooms
    if libtcod.bsp_is_leaf(node):
        minx = node.x + 1
        maxx = node.x + node.w - 1
        miny = node.y + 1
        maxy = node.y + node.h - 1

        if maxx == Constants.MAP_WIDTH - 1:
            maxx -= 1
        if maxy == Constants.MAP_HEIGHT - 1:
            maxy -= 1

        # If it's False the rooms sizes are random, else the rooms are filled to the node's size
        if Constants.FULL_ROOMS is False:
            minx = libtcod.random_get_int(None, minx, maxx - Constants.MIN_SIZE + 1)
            miny = libtcod.random_get_int(None, miny, maxy - Constants.MIN_SIZE + 1)
            maxx = libtcod.random_get_int(None, minx + Constants.MIN_SIZE - 2, maxx)
            maxy = libtcod.random_get_int(None, miny + Constants.MIN_SIZE - 2, maxy)

        node.x = minx
        node.y = miny
        node.w = maxx - minx + 1
        node.h = maxy - miny + 1

        # Dig room
        for x in range(minx, maxx + 1):
            for y in range(miny, maxy + 1):
                create_ground(x, y)

        # Add center coordinates to the list of rooms
        bsp_rooms.append(((minx + maxx) / 2, (miny + maxy) / 2))

    # Create corridors
    else:
        left = libtcod.bsp_left(node)
        right = libtcod.bsp_right(node)
        node.x = min(left.x, right.x)
        node.y = min(left.y, right.y)
        node.w = max(left.x + left.w, right.x + right.w) - node.x
        node.h = max(left.y + left.h, right.y + right.h) - node.y
        if node.horizontal:
            if left.x + left.w - 1 < right.x or right.x + right.w - 1 < left.x:
                x1 = libtcod.random_get_int(None, left.x, left.x + left.w - 1)
                x2 = libtcod.random_get_int(None, right.x, right.x + right.w - 1)
                y = libtcod.random_get_int(None, left.y + left.h, right.y)
                vline_up(level_map, x1, y - 1)
                hline(level_map, x1, y, x2)
                vline_down(level_map, x2, y + 1)

            else:
                minx = max(left.x, right.x)
                maxx = min(left.x + left.w - 1, right.x + right.w - 1)
                x = libtcod.random_get_int(None, minx, maxx)
                vline_down(level_map, x, right.y)
                vline_up(level_map, x, right.y - 1)

        else:
            if left.y + left.h - 1 < right.y or right.y + right.h - 1 < left.y:
                y1 = libtcod.random_get_int(None, left.y, left.y + left.h - 1)
                y2 = libtcod.random_get_int(None, right.y, right.y + right.h - 1)
                x = libtcod.random_get_int(None, left.x + left.w, right.x)
                hline_left(level_map, x - 1, y1)
                vline(level_map, x, y1, y2)
                hline_right(level_map, x + 1, y2)
            else:
                miny = max(left.y, right.y)
                maxy = min(left.y + left.h - 1, right.y + right.h - 1)
                y = libtcod.random_get_int(None, miny, maxy)
                hline_left(level_map, right.x - 1, y)
                hline_right(level_map, right.x, y)

    return True


def drunk_walk():
    global level_map, objects, stairs, bsp_rooms

    player = GameState.get_player()

    objects = [player]

    max_walk_attempts = 10000
    walk_attempts = 0

    x, y = Constants.MAP_WIDTH / 2, Constants.MAP_HEIGHT / 2
    x = 5
    y = 5

    while walk_attempts <= max_walk_attempts:

        # carve current space
        create_ground(x, y)

        # decide which direction to go
        d = random.randint(1, 100)

        if 1 <= d < 25:
            x -= 1
        elif 25 <= d < 50:
            x += 1
        elif 50 <= d < 75:
            y -= 1
        elif 75 <= d < 101:
            y += 1

        if x > Constants.MAP_WIDTH -1:
            x = Constants.MAP_WIDTH - 1
        if x < 1:
            x = 1
        if y > Constants.MAP_HEIGHT -1:
            y = Constants.MAP_HEIGHT - 1
        if y < 1:
            y = 1
        walk_attempts += 1


def pre_fabs_v2():
    global level_map, objects, stairs, bsp_rooms

    player = GameState.get_player()
    directions = ['Up', 'Down', 'Left', 'Right']
    rotations = ['90', '180', '270', 'None']
    objects = [player]

    builders = []
    max_attempts = 10000
    attempts = 1

    x = Constants.MAP_WIDTH / 2
    y = Constants.MAP_HEIGHT / 2

    # place room in center of map...ish

    start_room = 'Room'

    load_prefab(x, y, start_room, 'None')
    fab_size = Prefabs.get_size(start_room, 'None')
    fab_pos = x, y

    old_size = fab_size
    old_pos = fab_pos

    fits = False

    while attempts <= max_attempts:

        if fits:
            old_size = fab_size
            old_pos = fab_pos

        direction = random.choice(directions)
        # direction = 'Up'
        rotation = random.choice(rotations)
        # rotation = '90'
        fab_choice = random.choice(Prefabs.get_keys())
        # fab_choice = '+hall'

        fab_size = Prefabs.get_size(fab_choice, rotation)
        # print fab_size

        if direction == 'Right':
            # shoud come from PFloader
            connector_pos = old_pos[0] + old_size[0] - 1, old_pos[1] + 1

            # calculate position of new PreFab
            fab_pos = old_pos[0] + old_size[0] + 1, old_pos[1]

            if can_fit(fab_pos[0], fab_pos[1], fab_size[0], fab_size[1]):
                # Draw Prefab at new Pos
                load_prefab(fab_pos[0], fab_pos[1], fab_choice, rotation)

                # Draw connective elements Between
                #spawn_door_at(con_x, con_y, 'Door')
                create_ground(connector_pos[0], connector_pos[1])
                create_ground(connector_pos[0]+1, connector_pos[1])
                create_ground(connector_pos[0]+2, connector_pos[1])

                fits = True
                # print "Fit Right!"
            else:
                fits = False
                # print "Cannot Fit Right!"

        elif direction == 'Left':
            # shoud come from PFloader
            connector_pos = old_pos[0], old_pos[1] + 1

            # calculate position of new PreFab
            fab_pos = old_pos[0] - fab_size[0] - 1, old_pos[1]

            if can_fit(fab_pos[0], fab_pos[1], fab_size[0], fab_size[1]):
                # Draw Prefab at new Pos
                load_prefab(fab_pos[0], fab_pos[1], fab_choice, rotation)

                # Draw connective elements Between
                # spawn_door_at(con_x, con_y, 'Door')
                create_ground(connector_pos[0], connector_pos[1])
                create_ground(connector_pos[0] - 1, connector_pos[1])
                create_ground(connector_pos[0] - 2, connector_pos[1])

                fits = True
                # print "Fit Left!"
            else:
                fits = False
                # print "Cannot Fit Left!"

        elif direction == 'Down':
            # shoud come from PFloader
            connector_pos = old_pos[0] + 1, old_pos[1] + old_size[1] - 1

            # calculate position of new PreFab
            fab_pos = old_pos[0], old_pos[1] + old_size[1] + 1

            if can_fit(fab_pos[0], fab_pos[1], fab_size[0], fab_size[1]):
                # Draw Prefab at new Pos
                load_prefab(fab_pos[0], fab_pos[1], fab_choice, rotation)

                # Draw connective elements Between
                # spawn_door_at(con_x, con_y, 'Door')
                create_ground(connector_pos[0], connector_pos[1])
                create_ground(connector_pos[0], connector_pos[1]+1)
                create_ground(connector_pos[0], connector_pos[1]+2)

                fits = True
                # print "Fit Down!"
            else:
                fits = False
                # print "Cannot Fit Down!"

        elif direction == 'Up':
            # shoud come from PFloader
            connector_pos = old_pos[0] + 1, old_pos[1]

            # calculate position of new PreFab
            fab_pos = old_pos[0], old_pos[1] - fab_size[1] - 1

            if can_fit(fab_pos[0], fab_pos[1], fab_size[0], fab_size[1]):
                # Draw Prefab at new Pos
                load_prefab(fab_pos[0], fab_pos[1], fab_choice, rotation)

                # Draw connective elements Between
                # spawn_door_at(con_x, con_y, 'Door')
                create_ground(connector_pos[0], connector_pos[1])
                create_ground(connector_pos[0], connector_pos[1]-1)
                create_ground(connector_pos[0], connector_pos[1]-2)

                fits = True
                # print "Fit Up!"
            else:
                fits = False
                # print "Cannot Fit Up!"


        attempts += 1


def pre_fabs():
    global level_map, objects, stairs, bsp_rooms

    player = GameState.get_player()

    directions = ['Up', 'Down', 'Left', 'Right']

    rotations = ['90', '180', '270', 'None']

    objects = [player]

    builders = []
    max_attempts = 3
    attempts = 1

    x = 15
    y = 15




    # place room in center of map...ish
    load_prefab(x, y, 'Room', 'None')
    fab_size = Prefabs.get_size('Room', 'None')




    while attempts <= max_attempts:

        direction = random.choice(directions)
        # direction = 'Down'
        rotation = random.choice(rotations)
        rotation = 'None'

        fab_choice = random.choice(Prefabs.get_keys())
        fab_choice = 'Room'

        last_fab_size = fab_size

        fab_size = Prefabs.get_size(fab_choice, rotation)

        if attempts == 1:
            if direction == 'Right':
                con_x = x + last_fab_size[0]
                con_y = y + 2
            elif direction == 'Left':
                con_x = x + 1
                con_y = y + 2
            elif direction == 'Up':
                con_x = x + 2
                con_y = y + 1
            elif direction == 'Down':
                con_x = x + 2
                con_y = y + last_fab_size[1]

        # print attempts
        # print "Builder Loc: {0}, {1}".format(con_x, con_y)
        # print direction, rotation, fab_size, fab_choice

        if direction == 'Right':
            offset_x = 1
            offset_y = 2
            con_x = x + last_fab_size[0]
            con_y = y + 2

            if can_fit(con_x, con_y, offset_x, offset_y, fab_size[0], fab_size[1],
                       direction=direction):  # Needs direction
                load_prefab(con_x + offset_x, con_y-offset_y, fab_choice, rotation)
                try:
                    spawn_door_at(con_x, con_y, 'Door')
                    create_ground(con_x + 1, con_y)
                    create_ground(con_x + 2, con_y)
                except:
                    # print "Door/Ground FAIL"
                    pass
                #con_x += fab_size[0] + 1
        elif direction == 'Left':
            offset_x = fab_size[0]
            offset_y = 2
            if can_fit(con_x, con_y, offset_x, offset_y, fab_size[0], fab_size[1],
                       direction=direction): # Needs direction
                load_prefab(con_x - offset_x - 2 , con_y-offset_y, fab_choice, rotation)
                try:
                    spawn_door_at(con_x, con_y, 'Door')
                    create_ground(con_x - 1, con_y)
                    create_ground(con_x - 2, con_y)
                except:
                    # print "BAIL!"
                    pass
                #con_x -= offset_x + 1
        elif direction == 'Up':
            offset_x = 2
            offset_y = fab_size[1] + 1
            if can_fit(con_x, con_y, offset_x, offset_y, fab_size[0], fab_size[1],
                       direction=direction): # Needs direction
                load_prefab(con_x - offset_x, con_y - offset_y - 1, fab_choice, rotation)
                try:
                    spawn_door_at(con_x, con_y, 'Door')
                    create_ground(con_x, con_y-1)
                    create_ground(con_x, con_y-2)
                except:
                    pass
                #con_y -= fab_size[1] + 1
        elif direction == 'Down':
            offset_x = 2
            offset_y = 1
            if can_fit(con_x, con_y, offset_x, offset_y, fab_size[0], fab_size[1],
                           direction=direction): # Needs direction
                load_prefab(con_x - offset_x , con_y+1, fab_choice, rotation)
                try:
                    spawn_door_at(con_x, con_y, 'Door')
                    create_ground(con_x, con_y+1)
                    create_ground(con_x, con_y+2)
                except:
                    pass
                #con_y += fab_size[1] + 1
        else:
            # print "Blocked"
            pass

        attempts += 1


def can_fit(fab_x, fab_y, w, h):
    global level_map
    # print fab_x, fab_y, w, h

    if fab_x < 1 or (fab_x + w) > Constants.MAP_WIDTH - 1 or fab_y < 1 or (fab_y + h) > Constants.MAP_HEIGHT - 1:
        return False

    for x in range(fab_x, fab_x + w):
        for y in range(fab_y, fab_y + h):
            if level_map[x][y].blocked is False:
                # print "Blocked!"
                return False
    return True


def vline(map, x, y1, y2):
    if y1 > y2:
        y1, y2 = y2, y1

    for y in range(y1, y2 + 1):
        create_ground(x, y)


def vline_up(map, x, y):
    while y >= 0 and map[x][y].blocked == True:
        create_ground(x, y)
        y -= 1


def vline_down(map, x, y):
    while y < Constants.MAP_HEIGHT and map[x][y].blocked == True:
        create_ground(x, y)
        y += 1


def hline(map, x1, y, x2):
    if x1 > x2:
        x1, x2 = x2, x1
    for x in range(x1, x2 + 1):
        create_ground(x, y)


def hline_left(map, x, y):
    while x >= 0 and map[x][y].blocked == True:
        create_ground(x, y)
        x -= 1


def hline_right(map, x, y):
    while x < Constants.MAP_WIDTH and map[x][y].blocked == True:
        create_ground(x, y)
        x += 1


def create_room(room):
    global level_map
    # go through the tiles in the rectangle and make them passable
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            create_ground(x, y)


def create_ground(x, y, id=None):
    global level_map
    if id is not None:
        char = 48 + id
    else:
        char = Themes.ground_char()
    level_map[x][y] = Tile(False,
                           block_sight=False,
                           char=char,
                           f_color=Themes.ground_color(),
                           b_color=Themes.ground_bcolor(),
                           pos_x=x,
                           pos_y=y)


def create_wall(x, y):
    global level_map
    level_map[x][y] = Tile(True,
                           block_sight=True,
                           char=Themes.wall_char(),
                           f_color=Themes.wall_color(),
                           b_color=Themes.wall_bcolor(),
                           pos_x=x,
                           pos_y=y)


def create_shroud(x, y):
    global level_map
    level_map[x][y] = Tile(False,
                           block_sight=True,
                           char=Themes.shroud_char(),
                           f_color=Themes.shroud_color(),
                           b_color=Themes.shroud_bcolor(),
                           pos_x = x,
                           pos_y = y)


def create_glass(x, y):
    global level_map
    level_map[x][y] = Tile(True,
                           block_sight=False,
                           char=Themes.glass_char(),
                           f_color=Themes.glass_color(),
                           b_color=Themes.glass_bcolor(),
                           pos_x=x,
                           pos_y=y)


def create_tunnel(start, end):
    global level_map
    # print start, end
    points = Utils.get_line(start, end)

    # print "points"
    # print points

    for p in points:
        create_ground(p[0], p[1])


def create_v_tunnel(y1, y2, x):
    global level_map
    # vertical tunnel
    for y in range(min(y1, y2), max(y1, y2) + 1):
        create_ground(x, y)


def create_h_tunnel(x1, x2, y):
    global level_map
    for x in range(min(x1, x2), max(x1, x2) + 1):
        create_ground(x, y)


# HELPERS


def place_objects(level, room):
    # this is where we decide the chance of each monster or item appearing.


    '''MONSTERS'''

    # maximum number of monsters per room
    max_monsters = Utils.from_dungeon_level([[2, 1], [3, 4], [5, 6]])

    # chance of each monster
    monster_chances = {}

    for key in GameState.imported_npc_list:

        s = GameState.imported_npc_list[key]['freq']
        s_list = [tuple(x.split(':')) for x in s.split(',')]
        #print s_list

        monster_chances[key] = Utils.from_dungeon_level(s_list)
        #print item_chances

    '''ITEMS'''
    # maximum number of items per room
    max_items = Utils.from_dungeon_level([[1, 1]])

    # chance of each item (by default they have a chance of 0 at level 1, which then goes up)
    item_chances = {}
    for key in GameState.imported_items_list:

        s = GameState.imported_items_list[key]['freq']
        s_list = [tuple(x.split(':')) for x in s.split(',')]
        #print s_list

        item_chances[key] = Utils.from_dungeon_level(s_list)
        #print item_chances


    # choose random number of monsters
    num_monsters = libtcod.random_get_int(0, 0, max_monsters)
    # print("Num_Mon: " + str(num_monsters) + " | " + str(max_monsters))
    for i in range(num_monsters):
        # choose random spot for this monster
        x = libtcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
        y = libtcod.random_get_int(0, room.y1 + 1, room.y2 - 1)

        # only place it if the tile is not blocked
        if not GameState.current_level.is_blocked(x, y):
            choice = Utils.random_choice(monster_chances)
            spawn_npc_at(level, x, y, choice)

    # choose random number of items

    num_items = libtcod.random_get_int(0, 0, max_items)

    for i in range(num_items):
        # choose random spot for this item
        x = libtcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
        y = libtcod.random_get_int(0, room.y1 + 1, room.y2 - 1)
        choice = Utils.random_choice(item_chances)

        spawn_item_at(level, x,y, choice)


def number_of_adjacent_objects(obj):
    num = 0
    for object in get_visible_objects():
        difx = abs(object.x - obj.x)
        dify = abs(object.y - obj.y)
        if object.fighter and (difx <= 1 and dify <= 1) and object is not obj:
            # print(object.name + " X:" + str(difx) + " Y:" + str(dify))
            num += 1
    return num


def spawn_npc_at(level, x, y, npc):
    import Engine.Schedule
    import Entities.Components
    fighter_component = None
    ai_component = None
    if 'fighter_component' in GameState.imported_npc_list[npc]:
        fighter_component = Entities.Components.Fighter(hp=int(GameState.imported_npc_list[npc]['hp']),
                                                        defense=int(GameState.imported_npc_list[npc]['defense']),
                                                        power=str(GameState.imported_npc_list[npc]['power']),
                                                        xp=int(GameState.imported_npc_list[npc]['xp']),
                                                        death_function=eval('Components.' + GameState.imported_npc_list[npc]['death_function']))

    if 'ai_component' in GameState.imported_npc_list[npc]:
        ai_component = eval('Components.' + GameState.imported_npc_list[npc]['ai_component'])

    if 'always_visible' in GameState.imported_npc_list[npc]:
        vis = GameState.imported_npc_list[npc]['color']
    else:
        vis = False


    monster = Entities.Entity.Entity(x, y,
                            GameState.imported_npc_list[npc]['char'],
                            GameState.imported_npc_list[npc]['name'],
                            eval(GameState.imported_npc_list[npc]['color']),
                            always_visible=vis,
                            speed=int(GameState.imported_npc_list[npc]['speed']),
                            blocks=True,
                            fighter=fighter_component,
                            ai=ai_component)

    level.objects.append(monster)
    monster.action_points = 0

    if monster.base_speed > 0:
        GameState.schedule.register(monster)


def spawn_door_at(level, x, y, npc):
    create_ground(x, y)
    fighter_component = None
    ai_component = None
    if 'fighter_component' in GameState.imported_npc_list[npc]:
        fighter_component = Components.Fighter(hp=int(GameState.imported_npc_list[npc]['hp']),
                                               defense=int(GameState.imported_npc_list[npc]['defense']),
                                               power=int(GameState.imported_npc_list[npc]['power']),
                                               xp=int(GameState.imported_npc_list[npc]['xp']),
                                               death_function=eval(
                                                   'Components.' + GameState.imported_npc_list[npc]['death_function']))

    if 'ai_component' in GameState.imported_npc_list[npc]:
        ai_component = eval('Components.' + GameState.imported_npc_list[npc]['ai_component'])

    if 'always_visible' in GameState.imported_npc_list[npc]:
        vis = GameState.imported_npc_list[npc]['color']
    else:
        vis = False

    monster = Entity.Entity(x, y,
                            GameState.imported_npc_list[npc]['char'],
                            GameState.imported_npc_list[npc]['name'],
                            eval(GameState.imported_npc_list[npc]['color']),
                            always_visible=vis,
                            speed=int(GameState.imported_npc_list[npc]['speed']),
                            blocks=True,
                            blocks_sight=True,
                            fighter=fighter_component,
                            ai=ai_component)

    level.objects.append(monster)


def spawn_item_at(level, x,y, item_name):
    item_component = None
    equipment_component = None
    if 'item_component' in GameState.imported_items_list[item_name]:
        if 'use_function' in GameState.imported_items_list[item_name]:
            item_component = \
                Components.Item(use_function=eval('Spells.' + GameState.imported_items_list[item_name]['use_function']))
        else:
            item_component = Components.Item()
    if 'equipment_component' in GameState.imported_items_list[item_name]:
        equipment_component = \
            Components.Equipment(slot=GameState.imported_items_list[item_name]['slot'],
                                 defense_bonus=int(GameState.imported_items_list[item_name]['defense_bonus']),
                                 power_bonus=int(GameState.imported_items_list[item_name]['power_bonus']))
    item = Entity.Entity(x, y, GameState.imported_items_list[item_name]['char'],
                         GameState.imported_items_list[item_name]['name'],
                         eval(GameState.imported_items_list[item_name]['color']),
                         item=item_component,
                         equipment=equipment_component)
    level.objects.append(item)
    item.send_to_back()  # items appear below other objects
    item.always_visible = True  # items are visible even out-of-FOV, if in an explored area




def spawn_doors():

    valid_nodes = []

    for y in range(1, Constants.MAP_HEIGHT-1):
        for x in range(1, Constants.MAP_WIDTH-1):
            if not level_map[x][y].blocked and GameState.current_level.has_cross_blocked(x, y):
                count = GameState.current_level.get_total_blocked_corners(x,y)
                chance = libtcod.random_get_int(0, 0, 100)
                if count == 0 and chance <= 50:
                    spawn_door_at(x,y, 'Door')
                elif count == 1 and chance <= 40:
                    spawn_door_at(x,y, 'Door')
                elif count == 2 and chance <= 30:
                    spawn_door_at(x,y, 'Door')
                elif count == 3 and chance <= 2:
                    spawn_door_at(x,y, 'Door')

