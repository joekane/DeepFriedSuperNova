import xml.etree.ElementTree
import sys
import heapq
from collections import namedtuple
import GameState
import Events
import Engine.Input as Input
from copy import copy, deepcopy
import time
from bearlibterminal import terminal
import random

SPAWNS = 1000

Position = namedtuple('Positon', 'x y')

import Systems

player = None


class Component(object):
    def __init__(self):
        self.priority = 100
        self.owner = None
        self.name = ''

    def fire_event(self, event):
        return event

    def __cmp__(self, other):
        return cmp(self.priority, other.priority)

    def __repr__(self):
        return self.__class__.__name__ + " | " + str(self.priority)

    def __eq__(self, other):
        if self.__class__.__name__ == other.__class__.__name__:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.__repr__())


class Entity(object):
    def __init__(self, name, components):
        self.name = name
        self.components = components
        for c in self.components:
            c.owner = self

    def __repr__(self):
        return "\r\n" + self.name + "\r\n" + str([e.name for e in self.components])

    def get_component(self, name):
        for c in self.components:
            if c.name == name:
                return c
        return False

    def remove_component(self, component):
        return self.components.remove(component)

    def fire_event(self, event):
        for c in sorted(self.components):
            event = c.fire_event(event)
        return event


class EntityFactory(object):
    root = xml.etree.ElementTree.parse(r'./ECS/objects.xml').getroot()
    blueprints = root.getchildren()

    @staticmethod
    def CreateObject(object_name):
        #return GameObjectFactory.ParseXMLComponents(object_name, GameObjectFactory.get_blueprint(object_name))
        return EntityFactory.ParseXMLComponents(object_name, EntityFactory.get_blueprint(object_name))


    @staticmethod
    def ParseXMLComponents(name, bp_list):
        import Components
        component_list = []
        added_components = []
        #print "Parse_List: ", bp_list
        bp_list = deepcopy(bp_list)
        for bp in bp_list:
            for component in bp.iter('Component'):

                component_name = component.attrib.pop('name')
                if component_name not in added_components:
                    #print "Comp..."
                    added_components.append(component_name)
                    component_type = getattr(sys.modules['ECS.Components'], component_name)
                    component_list.append(component_type(**component.attrib))

        print "List: ", component_list
        return Entity(name, component_list)

    @staticmethod
    def ParseXMLComponentsForEntity(name, bp_list):
        entity = Entity(name)

        added_components = []
        #print "Parse_List: ", bp_list
        bp_list = deepcopy(bp_list)
        for bp in bp_list:
            for component in bp.iter('Component'):
                component_name = component.attrib.pop('name')
                if component_name not in added_components:
                    added_components.append(component_name)
                    entity.components[component_name] = component.attrib
                    #component_list.append(component_type(**component.attrib))
        return entity

    @staticmethod
    def get_blueprint(name, bp_list=None):
        if not bp_list:
            #print "Cleared"
            bp_list = []

        for bp in EntityFactory.blueprints:
            if bp.get('name') == name:
                bp_list.append(bp)
                #print name
                if bp.get('inherits'):
                    i_name = bp.get('inherits')
                    #print "Inherits ", i_name
                    #print "Before: ", bp_list
                    bp_list = EntityFactory.get_blueprint(i_name, bp_list)
#                    print "After: ", bp_list
            else:
                #rint 'No ', name, " Found"
                pass
        return bp_list



def game_loop():
    initialize_objects()
    print "###########################################"

    Systems.EntityManager.UpdateSystems()
    Systems.MapSystem.render_map()

    while True:
        Input.update()
        mouse = Input.mouse
        key = Input.key

        status = Systems.InputSystem().OnTurn()
        if status == 'waiting':
            pass
        elif status == 'charging':
            Systems.AISystem().OnTurn()
        elif status == 'turn_end':
            #print Systems.PhysicsSystem.entity_count()
            pass
        Systems.PhysicsSystem().OnTurn()
        Systems.RenderWorldSystem.OnTurn()




        """ testing """
        #terminal.composition(False)

        terminal.layer(10)
        terminal.clear_area(0,0,100,50)
        unit_test = Systems.PhysicsSystem.is_blocked(Position(mouse.cx, mouse.cy))
        if unit_test[0]:
            terminal.puts(0,30, "{0}|{1} => {2}".format(mouse.cx, mouse.cy, unit_test[1][0].name))
        else:
            terminal.puts(0, 30, "{0}|{1}".format(mouse.cx, mouse.cy))
        terminal.puts(0,31, "{0}".format(Systems.PhysicsSystem.entity_count()))

        """ ------- """


        Systems.EntityManager.OnUpdate()
        terminal.refresh()



def initialize_objects():
    global object_list, player

    #terminal.composition(False)

    map = EntityFactory.CreateObject('map')

    r = EntityFactory.CreateObject('rat')

    player = EntityFactory.CreateObject('player')

    things = [ 'kobold', 'rat', 'sword']

    for thing in range(SPAWNS):
        obj_name = random.choice(things)
        obj = EntityFactory.CreateObject(obj_name)

        #obj.fire_event(Events.move_to(Position(random.randint(1, 79), random.randint(1, 24))))
        obj.get_component('Physics').position = Position(random.randint(1, 79), random.randint(1, 24))
        #obj.getComponent('Physics')['position'] = Position(8, 10)
        obj.get_component('Physics').last_position = Position(-1, -1)

        Systems.EntityManager.entity_list.append(obj)
        #object_list.append(obj)

    #print player
    #print player['Container']





    #p.fire_event(Events.add_item(s))
    player.get_component('Physics').position = Position(22, 8)
    player.get_component('Physics').last_position = Position(-1, -1)
    player.get_component('Render').layer = 2
    Systems.EntityManager.entity_list.append(player)

    map.get_component('Map').map = [c for c in
                    '######.........#.#.......#.....#...#.....#.........#.#...#.#.......#.......###########.#.###.#.#.#.#######.#.#####.#.###.#.#.#####.#.###.#.#.#######.###########.....#.#.#...#.#.........#.#.#.....#.###...#.#.....#.......#.......#.....#######.#.#.###.#.#####.#.#.#######.#.#.#.#.#####################.#.###.#######.#######.#.#.#...#...#...#.#...#.#.#.#.#.#.#.........#.....#...........#.#.............#####.#.#######.#######.#.#.#.#.#.#######.#.#.#.#.#.#.#######.#######.#######.#.###...#...#####.#.#####.#...#...#.#...#.#.#.#...#.#...###...#.#.......#.......#.#####.###.#####.#.#####.#.###.#.###.###.#.#.###.#########.#####.###.#############.........###.#.....###.#...#.#.#.#.......#.#...#...#.#.#.#.......#.###...#.....#########.###.#.#.#.###.#.#.###.#.#.#####.#.###.#.###.#.#.#.#.###.#####.###.#.###.......#.....#.#.#.#...#.#...........#...#.#.....#.......#.#...#.#.........#...#####.#.#.#####.#.###.#######.#######.###.#.#.###.#.#####.#.#####.#.#.#####.#####...#.#.#.......#...#.....#.....#.#...#####.#...#.......#.#...#.....#...#.#.....###.###.#.#.#.###.#####.#.#####.#.#.#######.#####.#####.#.###.#.###.#####.#####.###...#...#.#.#.......#.#.....#...#.......#...#...#.....#.....#...#...........#.#####.#.###########.###.#.###.#####.#######.###.###########.###.###.#####.###.#######...###.....#...#.#.#...#...........###...#.###...#.###.###...#.....#.#.....#####.#####.#######.#.###.###.#.#####.#.#############.#.###.#####.#####.#.###.#######.........#.#...#.....#.#.#.#.....#.###.#...#.............#...#####.#...#...#######.#.#####.#.###.#.#.#.###.#######.###.#.#####.###.#################.#############.#...#.#.....#.#.#.#...#...###...###.....#...#.......#########...#.......#######.###.#.#####.#####.#.###.#.###.#.###.#.###.###.#####.#########.#########.#######.#.#.#...###...#...#.#.#.#...#.#.....#.#.#...#.###...#########...#.......#########.#.###.#######.#.#.#.###.#######.###.#.#####.###############.#.###.#############...###.........#.#.......#######.#.....#####.......#########.#.........#'
                    ]

    Systems.EntityManager.entity_list.append(map)




