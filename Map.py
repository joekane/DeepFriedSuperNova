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
import GameState
import Entity
import random
import Fov
import Utils
import Components
import Themes
import CaveGen
import Spells

level_map = None
objects = None
visible_objects = None
stairs = None
camera_x = 0
camera_y = 0


def current_map():
    return level_map


def new_map(solid=True):
    global level_map

    if solid:
        level_map = [[Tile(True,
                           block_sight=True,
                           char=Themes.wall_char(),
                           f_color=Themes.wall_color(),
                           b_color=Themes.wall_bcolor())
                      for y in range(Constants.MAP_HEIGHT)] for x in range(Constants.MAP_WIDTH)]
    else:
        level_map = [[Tile(False,
                           block_sight=False,
                           char=Themes.wall_char(),
                           f_color=Themes.wall_color(),
                           b_color=Themes.wall_bcolor())
                      for y in range(Constants.MAP_HEIGHT)] for x in range(Constants.MAP_WIDTH)]


class Tile:
    # a tile of the map and its properties
    def __init__(self, blocked, block_sight=None, char=' ', f_color=Themes.ground_color(), b_color=libtcod.black):
        self.blocked = blocked
        self.explored = False
        self.char = char
        self.f_color = f_color
        self.b_color = b_color

        # by default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            block_sight = blocked
        self.block_sight = block_sight


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


def generate_map():
    import SoundEffects
    level = random.choice(Themes.LEVEL_STYLE)

    new_map()

    if level == 'BSP':
        #bsp_dungeon()
        #basic_dungeon()
        rooms_only_dungeon()
        spawn_doors()
    elif level == 'WILD':
        CaveGen.build()
        read_cavegen_data()
    elif level == 'CAVE_TIGHT':
        # caves(style='TIGHT')
        wilderness()
        #basic_dungeon()
        #spawn_doors()
    elif level == 'CAVE_OPEN':
        caves(style='OPEN')
        basic_dungeon()
    Fov.initialize()
    SoundEffects.play_music('SSA')


def caves(style='DEFAULT'):
    import Noise
    global objects, level_map, stairs

    if style == 'DEFAULT':
        Noise.initialze(scale=10)
    elif style == 'OPEN':
        Noise.initialze(scale=15)
    elif style == 'TIGHT':
        Noise.initialze(scale=5)

    player = GameState.get_player()
    objects = [player]

    # level_map = [[Tile(True,
    #                   block_sight=True,
    #                   char=Themes.wall_char(),
    #                   f_color=Themes.wall_color(),
    #                   b_color=Themes.wall_bcolor())
    #              for y in range(Constants.MAP_HEIGHT)] for x in range(Constants.MAP_WIDTH)]

    for x in range(1,Constants.MAP_WIDTH-1):
        for y in range(1,Constants.MAP_HEIGHT-1):
            pre_value = Noise.get_height_value(x, y)

            if 0.52 <= pre_value < 1:
                level_map[x][y] = Tile(False,
                                       block_sight=False,
                                       char=Themes.ground_char(),
                                       f_color=Themes.ground_color(),
                                       b_color=Themes.ground_bcolor())


def wilderness():
    import Noise
    global objects, level_map, stairs

    Noise.initialze(scale=100)

    player = GameState.get_player()
    objects = [player]

    #level_map = [[Tile(True,
    #                   block_sight=True,
    #                   char=Themes.wall_char(),
    #                   f_color=Themes.wall_color(),
    #                   b_color=Themes.wall_bcolor())
    #              for y in range(Constants.MAP_HEIGHT)] for x in range(Constants.MAP_WIDTH)]

    for x in range(Constants.MAP_WIDTH):
        for y in range(Constants.MAP_HEIGHT):
            pre_value = Noise.get_height_value(x, y)
            # print pre_value

            if 0 <= pre_value < 0.1:
                level_map[x][y] = Tile(False,
                                       block_sight=False,
                                       char='~',
                                       f_color=libtcod.darker_blue,
                                       b_color=libtcod.black)
            elif 0.1 <= pre_value < 0.2:
                level_map[x][y] = Tile(False,
                                       block_sight=False,
                                       char='~',
                                       f_color=libtcod.dark_blue,
                                       b_color=libtcod.black)
            elif 0.2 <= pre_value < 0.3:
                level_map[x][y] = Tile(False,
                                       block_sight=False,
                                       char='~',
                                       f_color=libtcod.blue,
                                       b_color=libtcod.black)
            elif 0.3 <= pre_value < 0.4:
                level_map[x][y] = Tile(False,
                                       block_sight=False,
                                       char='%',
                                       f_color=libtcod.blue,
                                       b_color=libtcod.black)
            elif 0.4 <= pre_value < 0.5:
                level_map[x][y] = Tile(False,
                                       block_sight=False,
                                       char='~',
                                       f_color=libtcod.light_blue,
                                       b_color=libtcod.black)
            elif 0.5 <= pre_value < 0.6:
                level_map[x][y] = Tile(False,
                                       block_sight=False,
                                       char=';',
                                       f_color=libtcod.light_green,
                                       b_color=libtcod.black)
            elif 0.6 <= pre_value < 0.7:
                level_map[x][y] = Tile(False,
                                       block_sight=False,
                                       char=',',
                                       f_color=libtcod.green,
                                       b_color=libtcod.black)
            elif 0.7 <= pre_value < 0.90:
                level_map[x][y] = Tile(False,
                                       block_sight=False,
                                       char='*',
                                       f_color=libtcod.dark_green,
                                       b_color=libtcod.black)
            elif 0.90 <= pre_value < 0.999:
                level_map[x][y] = Tile(False,
                                       block_sight=False,
                                       char='^',
                                       f_color=libtcod.dark_sepia,
                                       b_color=libtcod.black)
            else:
                level_map[x][y] = Tile(False,
                                       block_sight=False,
                                       char='^',
                                       f_color=libtcod.dark_grey,
                                       b_color=libtcod.black)
            level_map[x][y].explored = True


def read_cavegen_data(): # OBSOLETE?
    import CaveGen
    global objects, level_map, stairs

    data = CaveGen.get_level_data()

    # Themes.apply_forrest_theme()

    player = GameState.get_player()
    objects = [player]

    # level_map = [[Tile(True,
    #                    block_sight=True,
    #                  char=Themes.wall_char(),
    #                   f_color=Themes.wall_color(),
    #                   b_color=Themes.wall_bcolor())
    #              for y in range(Constants.MAP_HEIGHT)] for x in range(Constants.MAP_WIDTH)]

    for x in range(Constants.MAP_WIDTH):
        for y in range(Constants.MAP_HEIGHT):
            if data[x][y] != 1:
                level_map[x][y] = Tile(False,
                                       block_sight=False,
                                       char=Themes.ground_char(),
                                       f_color=Themes.ground_color(),
                                       b_color=Themes.ground_bcolor())
            elif data[x][y] == 2:
                level_map[x][y] = Tile(False,
                                       block_sight=False,
                                       char='x',
                                       f_color=Themes.ground_color(),
                                       b_color=Themes.ground_bcolor())
            elif data[x][y] == 4:
                player.x, player.y = x, y

                level_map[x][y] = Tile(False,
                                       block_sight=False,
                                       char='c',
                                       f_color=Themes.ground_color(),
                                       b_color=Themes.ground_bcolor())
            level_map[x][y].explored = False

    return level_map


def load_diner_map():
    global objects, level_map, stairs

    player = GameState.get_player()
    objects = [player]

    player.x = 10
    player.y = 4

    file = open('Levels\diner.map', 'r')

    Themes.set_theme('Diner')

    new_map()

    # fill map with "blocked" tiles
    # level_map = [[Tile(True,
    #                   block_sight=True,
    #                   char=Themes.wall_char(),
    #                   f_color=Themes.wall_color(),
    #                   b_color=Themes.wall_bcolor())
    #              for y in range(Constants.MAP_HEIGHT)] for x in range(Constants.MAP_WIDTH)]

    y = 0

    for l in range(Constants.MAP_HEIGHT):
        line = file.readline()
        x = 0
        for c in line:
            if c == ' ':
                #print(str(x) + " " + str(y))
                level_map[x][y] = Tile(False,
                                       block_sight=False,
                                       char=Themes.ground_char(),
                                       f_color=Themes.ground_color(),
                                       b_color=Themes.ground_bcolor())
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
                level_map[x][y] = Tile(False,
                                       block_sight=False,
                                       char=Themes.ground_char(),
                                       f_color=Themes.ground_color(),
                                       b_color=Themes.ground_bcolor())
                player.x = x
                player.y = y
            if c == 'Q':
                level_map[x][y] = Tile(False,
                                       block_sight=False,
                                       char=Themes.ground_char(),
                                       f_color=Themes.ground_color(),
                                       b_color=Themes.ground_bcolor())
                spawn_npc_at(x, y, 'QuestGuy')
            if c == '+':
                level_map[x][y] = Tile(False,
                                       block_sight=False,
                                       char=Themes.ground_char(),
                                       f_color=Themes.ground_color(),
                                       b_color=Themes.ground_bcolor())
                spawn_npc_at(x, y, 'UnlockedDoor')
            if c == '_':
                level_map[x][y] = Tile(False,
                                       block_sight=False,
                                       char=Themes.ground_char(),
                                       f_color=Themes.ground_color(),
                                       b_color=Themes.ground_bcolor())
                spawn_npc_at(x, y, 'OpenDoor')
            if c == 's':
                level_map[x][y] = Tile(False,
                                       block_sight=False,
                                       char=Themes.ground_char(),
                                       f_color=Themes.ground_color(),
                                       b_color=Themes.ground_bcolor())
                stairs = Entity.Entity(x, y, '<', 'stairs', libtcod.white, always_visible=True)
                objects.append(stairs)
            x += 1
        y += 1


def basic_dungeon():
    global level_map, objects, stairs

    player = GameState.get_player()

    objects = [player]

    # if map is None:
    #    # fill map with "blocked" tiles
    #    level_map = [[Tile(True)
    #                  for y in range(Constants.MAP_HEIGHT)]
    #                 for x in range(Constants.MAP_WIDTH)]
    #else:
    #    level_map = map


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
            place_objects(new_room)
            # finally, append the new room to the list
            rooms.append(new_room)
            num_rooms += 1

    # create stairs at the center of the last room
    stairs = Entity.Entity(new_x, new_y, '<', 'stairs', libtcod.white, always_visible=True)
    objects.append(stairs)
    stairs.send_to_back()  # so it's drawn below the monsters
    return level_map


def rooms_only_dungeon():
    import SpanningTree
    global level_map, objects, stairs

    player = GameState.get_player()

    objects = [player]

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
            place_objects(new_room)
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
        print 'The shortest path for %s : %s' % (room.center(), path[::-1])

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
    stairs = Entity.Entity(new_x, new_y, '<', 'stairs', libtcod.white, always_visible=True)
    objects.append(stairs)
    stairs.send_to_back()  # so it's drawn below the monsters
    return level_map


def bsp_dungeon():
    global level_map, objects, stairs, bsp_rooms

    player = GameState.get_player()

    objects = [player]

    # Themes.apply_ssa_theme()
    # Themes.set_theme('Shadow State Archive')
    # Themes.set_theme('Valley of Devils')

    # Themes.apply_forrest_theme()

    # if map is None:
    #    # fill map with "blocked" tiles
    #    level_map = [[Tile(True,
    #                       block_sight=True,
    #                       char=Themes.wall_char(),
    #                       f_color=Themes.wall_color(),
    #                       b_color=Themes.wall_bcolor())
    #                  for y in range(Constants.MAP_HEIGHT)] for x in range(Constants.MAP_WIDTH)]
    #else:
    #    level_map = map



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
    stairs = Entity.Entity(stairs_location[0], stairs_location[1], '<', 'stairs', libtcod.white, always_visible=True)
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
        place_objects(new_room)

    Fov.require_recompute()


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
                level_map[x][y] = Tile(False,
                                       block_sight=False,
                                       char=Themes.ground_char(),
                                       f_color=Themes.ground_color(),
                                       b_color=Themes.ground_bcolor())

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


def vline(map, x, y1, y2):
    if y1 > y2:
        y1, y2 = y2, y1

    for y in range(y1, y2 + 1):
        map[x][y] = Tile(False,
                         block_sight=False,
                         char=Themes.ground_char(),
                         f_color=Themes.ground_color(),
                         b_color=Themes.ground_bcolor())


def vline_up(map, x, y):
    while y >= 0 and map[x][y].blocked == True:
        map[x][y] = Tile(False,
                         block_sight=False,
                         char=Themes.ground_char(),
                         f_color=Themes.ground_color(),
                         b_color=Themes.ground_bcolor())
        y -= 1


def vline_down(map, x, y):
    while y < Constants.MAP_HEIGHT and map[x][y].blocked == True:
        map[x][y] = Tile(False,
                         block_sight=False,
                         char=Themes.ground_char(),
                         f_color=Themes.ground_color(),
                         b_color=Themes.ground_bcolor())
        y += 1


def hline(map, x1, y, x2):
    if x1 > x2:
        x1, x2 = x2, x1
    for x in range(x1, x2 + 1):
        map[x][y] = Tile(False,
                         block_sight=False,
                         char=Themes.ground_char(),
                         f_color=Themes.ground_color(),
                         b_color=Themes.ground_bcolor())


def hline_left(map, x, y):
    while x >= 0 and map[x][y].blocked == True:
        map[x][y] = Tile(False,
                         block_sight=False,
                         char=Themes.ground_char(),
                         f_color=Themes.ground_color(),
                         b_color=Themes.ground_bcolor())
        x -= 1


def hline_right(map, x, y):
    while x < Constants.MAP_WIDTH and map[x][y].blocked == True:
        map[x][y] = Tile(False,
                         block_sight=False,
                         char=Themes.ground_char(),
                         f_color=Themes.ground_color(),
                         b_color=Themes.ground_bcolor())
        x += 1


def create_room(room):
    global level_map
    # go through the tiles in the rectangle and make them passable
    for x in range(room.x1 + 1, room.x2):
        for y in range(room.y1 + 1, room.y2):
            level_map[x][y] = Tile(False,
                                   block_sight=False,
                                   char=Themes.ground_char(),
                                   f_color=Themes.ground_color(),
                                   b_color=Themes.ground_bcolor())


def create_tunnel(start, end):
    global level_map
    # print start, end
    points = Utils.get_line(start, end)

    # print "points"
    # print points

    for p in points:
        level_map[p[0]][p[1]] = Tile(False,
                               block_sight=False,
                               char=Themes.ground_char(),
                               f_color=Themes.ground_color(),
                               b_color=Themes.ground_bcolor())




def create_v_tunnel(y1, y2, x):
    global level_map
    # vertical tunnel
    for y in range(min(y1, y2), max(y1, y2) + 1):
        level_map[x][y] = Tile(False,
                               block_sight=False,
                               char=Themes.ground_char(),
                               f_color=Themes.ground_color(),
                               b_color=Themes.ground_bcolor())


def create_h_tunnel(x1, x2, y):
    global level_map
    for x in range(min(x1, x2), max(x1, x2) + 1):
        level_map[x][y] = Tile(False,
                               block_sight=False,
                               char=Themes.ground_char(),
                               f_color=Themes.ground_color(),
                               b_color=Themes.ground_bcolor())


# HELPERS


def place_objects(room):
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
    # print("Num_Mon: " + str(num_monsters))
    for i in range(num_monsters):
        # choose random spot for this monster
        x = libtcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
        y = libtcod.random_get_int(0, room.y1 + 1, room.y2 - 1)

        # only place it if the tile is not blocked
        if not is_blocked(x, y):
            choice = Utils.random_choice(monster_chances)
            spawn_npc_at(x,y, choice)

    # choose random number of items

    num_items = libtcod.random_get_int(0, 0, max_items)

    for i in range(num_items):
        # choose random spot for this item
        x = libtcod.random_get_int(0, room.x1 + 1, room.x2 - 1)
        y = libtcod.random_get_int(0, room.y1 + 1, room.y2 - 1)
        choice = Utils.random_choice(item_chances)

        spawn_item_at(x,y, choice)


def number_of_adjacent_objects(obj):
    num = 0
    for object in get_visible_objects():
        difx = abs(object.x - obj.x)
        dify = abs(object.y - obj.y)
        if object.fighter and (difx <= 1 and dify <= 1) and object is not obj:
            # print(object.name + " X:" + str(difx) + " Y:" + str(dify))
            num += 1
    return num


def spawn_npc_at(x, y, npc):
    import Schedule
    fighter_component = None
    ai_component = None
    if 'fighter_component' in GameState.imported_npc_list[npc]:
        fighter_component = Components.Fighter(hp=int(GameState.imported_npc_list[npc]['hp']),
                                    defense=int(GameState.imported_npc_list[npc]['defense']),
                                    power=int(GameState.imported_npc_list[npc]['power']),
                                    xp=int(GameState.imported_npc_list[npc]['xp']),
                                    death_function=eval('Components.' + GameState.imported_npc_list[npc]['death_function']))

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
                            fighter=fighter_component,
                            ai=ai_component)

    objects.append(monster)
    monster.action_points = 0

    if monster.speed > 0:
        Schedule.register(monster)


def spawn_door_at(x, y, npc):
    import Schedule
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

    objects.append(monster)


def spawn_item_at(x,y, item_name):
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
    objects.append(item)
    item.send_to_back()  # items appear below other objects
    item.always_visible = True  # items are visible even out-of-FOV, if in an explored area


def closest_monster(max_range):
    # find closest enemy, up to a maximum range, and in the player's FOV
    closest_enemy = None
    closest_dist = max_range + 1  # start with (slightly more than) maximum range
    player = GameState.get_player()
    for object in get_visible_objects():
        if object.fighter and not object == player and Fov.is_visible(obj=object):
            # calculate distance between this object and the player
            dist = player.distance_to(object)
            if dist < closest_dist:  # it's closer, so remember it
                closest_enemy = object
                closest_dist = dist
    return closest_enemy


def is_explored(x,y):
    # first test the map tile
    if level_map[x][y].explored:
        return True

    return False


def is_blocked(x, y):
    # first test the map tile
    if level_map[x][y].blocked:
        # print "Blocked By Map!"
        return True

    # now check for any blocking objects
    for object in get_visible_objects():
        if object.blocks and object.x == x and object.y == y:
            # print "Blocked by Object!"
            return True

    return False


def directly_adjacent_open_tiles(obj):
    open_tiles = []


    if (not is_blocked(obj.x, obj.y - 1)):
        open_tiles.append([obj.x, obj.y - 1])
    if (not is_blocked(obj.x + 1, obj.y)):
        open_tiles.append([obj.x + 1, obj.y])
    if (not is_blocked(obj.x - 1, obj.y + 1)):
        open_tiles.append([obj.x - 1, obj.y + 1])
    if (not is_blocked(obj.x, obj.y + 1)):
        open_tiles.append([obj.x, obj.y + 1])

    if (len(open_tiles) == 0):
        return [None, None]

    choice = random.choice(open_tiles)
    # print(choice)
    return choice


def adjacent_open_tiles(obj):
    open_tiles = []

    if not is_blocked(obj.x - 1, obj.y - 1):
        open_tiles.append([obj.x - 1, obj.y - 1])
    if (not is_blocked(obj.x, obj.y - 1)):
        open_tiles.append([obj.x, obj.y - 1])
    if (not is_blocked(obj.x + 1, obj.y - 1)):
        open_tiles.append([obj.x + 1, obj.y - 1])
    if (not is_blocked(obj.x - 1, obj.y - 1)):
        open_tiles.append([obj.x - 1, obj.y - 1])
    if (not is_blocked(obj.x + 1, obj.y)):
        open_tiles.append([obj.x + 1, obj.y])
    if (not is_blocked(obj.x - 1, obj.y + 1)):
        open_tiles.append([obj.x - 1, obj.y + 1])
    if (not is_blocked(obj.x, obj.y + 1)):
        open_tiles.append([obj.x, obj.y + 1])
    if (not is_blocked(obj.x + 1, obj.y + 1)):
        open_tiles.append([obj.x + 1, obj.y + 1])
    if (len(open_tiles) == 0):
        return [None, None]

    choice = random.choice(open_tiles)
    # print(choice)
    return choice


def target_tile(max_range=None):
    # return the position of a tile left-clicked in player's FOV (optionally in a range), or (None,None) if right-clicked.
    mouse = libtcod.Mouse()
    key = libtcod.Key()

    while True:
        # render the screen. this erases the inventory and shows the names of objects under the mouse.
        libtcod.console_flush()
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        (x, y) = (mouse.cx, mouse.cy)

        # accept the target if the player clicked in FOV, and in case a range is specified, if it's in that range
        if (mouse.lbutton_pressed and Fov.is_visible(x, y) and
                (max_range is None or GameState.get_player().distance(x, y) <= max_range)):
            return (x, y)
        if mouse.rbutton_pressed or key.vk == libtcod.KEY_ESCAPE:
            return (None, None)  # cancel if the player right-clicked or pressed Escape


def target_monster(max_range=None):
    # returns a clicked monster inside FOV up to a range, or None if right-clicked
    while True:
        (x, y) = target_tile(max_range)
        if x is None:  # player cancelled
            return None

        # return the first clicked monster, otherwise continue looping
        for obj in get_visible_objects():
            if obj.x == x and obj.y == y and obj.fighter and obj != GameState.get_player():
                return obj


def get_camera():
    return camera_x, camera_y


def move_camera(target_x, target_y):
    global camera_x, camera_y

    try:
    # new camera coordinates (top-left corner of the screen relative to the map)
        x = target_x - Constants.MAP_CONSOLE_WIDTH / 2  # coordinates so that the target is at the center of the screen
        y = target_y - Constants.MAP_CONSOLE_HEIGHT / 2
    except:
        x = camera_x
        y = camera_y

    # make sure the camera doesn't see outside the map
    if x < 0:
        x = 0
    if y < 0:
        y = 0
    if x > Constants.MAP_WIDTH - Constants.MAP_CONSOLE_WIDTH:
        x = Constants.MAP_WIDTH - Constants.MAP_CONSOLE_WIDTH
    if y > Constants.MAP_HEIGHT - Constants.MAP_CONSOLE_HEIGHT:
        y = Constants.MAP_HEIGHT - Constants.MAP_CONSOLE_HEIGHT

    if x != camera_x or y != camera_y:
        Fov.require_recompute()

    (camera_x, camera_y) = (x, y)


def to_camera_coordinates(x, y):
    # convert coordinates on the map to coordinates on the screen
    # print "ToCam: " + str(x) + " " + str(y)
    (x, y) = (x - camera_x, y - camera_y)

    if x < 0 or y < 0 or x > Constants.MAP_CONSOLE_WIDTH or y > Constants.MAP_CONSOLE_HEIGHT:
        return None, None  # if it's outside the map, return nothing

    return x, y


def to_map_coordinates(x, y):
    # convert coordinates on the map to coordinates on the screen
    # print "ToMap: " + str(x) + " " + str(y)
    (x, y) = (x + camera_x, y + camera_y)

    if x < 0 or y < 0 or x > Constants.MAP_WIDTH -1 or y > Constants.MAP_HEIGHT - 1:
        return None, None  # if it's outside the map, return nothing

    return x, y


def get_all_objects():
    return objects


def get_visible_objects():
    global visible_objects
    if visible_objects is None:
        visible_objects = [obj for obj in objects if Fov.is_visible(obj=obj)]
        if visible_objects is None:
            return objects
        else:
            return visible_objects
    else:
        return visible_objects


def get_stairs():
    return stairs


def player_move_or_interact(dx, dy):
    # the coordinates the player is moving to/interacting

    player = GameState.get_player()
    x = player.x + dx
    y = player.y + dy

    # try to find an interactable object there

    for object in get_visible_objects():

        if object.fighter and object.x == x and object.y == y:
            player.fighter.attack(object)

            return
        if isinstance(object.ai, Components.QuestNpc) and object.x == x and object.y == y:
            # print "Reward!!!! .... ??"
            object.ai.talk()
            return
        if object.blocks:
            if isinstance(object.ai, Components.Door) and object.x == x and object.y == y:
                object.ai.interact()
                Fov.require_recompute()
                return

    player.move(dx, dy)
    Fov.require_recompute()


def get_open_tiles():
    global level_map

    open_nodes = []

    for y in range(Constants.MAP_HEIGHT):
        for x in range(Constants.MAP_WIDTH):
            if not level_map[x][y].blocked:
                open_nodes.append(level_map[x][y])

    return open_nodes


def has_cross_blocked(x,y):
    if level_map[x-1][y].blocked and level_map[x+1][y].blocked:
        return True
    elif level_map[x][y-1].blocked and level_map[x][y+1].blocked:
        return True
    return False


def get_total_blocked_corners(x,y):
    count = 0
    if level_map[x-1][y-1].blocked:
        count += 1
    if level_map[x+1][y-1].blocked:
        count += 1
    if level_map[x-1][y+1].blocked:
        count += 1
    if level_map[x+1][y+1].blocked:
        count += 1
    return count


def spawn_doors():

    valid_nodes = []

    for y in range(1,Constants.MAP_HEIGHT-1):
        for x in range(1,Constants.MAP_WIDTH-1):
            if not level_map[x][y].blocked and has_cross_blocked(x, y):
                count = get_total_blocked_corners(x,y)
                chance = libtcod.random_get_int(0, 0, 100)
                if count == 0 and chance <= 50:
                    spawn_door_at(x,y, 'Door')
                elif count == 1 and chance <= 40:
                    spawn_door_at(x,y, 'Door')
                elif count == 2 and chance <= 30:
                    spawn_door_at(x,y, 'Door')
                elif count == 3 and chance <= 2:
                    spawn_door_at(x,y, 'Door')

