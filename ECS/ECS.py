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

SPAWNS = 25

Position = namedtuple('Positon', 'x y')

import Systems
player = None

class Component(object):
    def __init__(self):
        self.priority = 100
        self.owner = None

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


class Entity(dict):
    def __init__(self, *arg, **kwargs):
        super(Entity, self).__init__(*arg, **kwargs)
        self.name = kwargs.get('name')

    def __repr__(self):
        return self.name + "\r\n" + str(self.keys())

    def getComponent(self, key):
        if key in self.keys():
            return self[key]
        else:
            return None

    def removeComponent(self, component):
        pass



class GameObject(object):
    def __init__(self, name, component_list):
        self.name = name
        self.component_list = component_list
        for c in self.component_list:
            c.owner = self

    @property
    def position(self):
        return self.fire_event(Events.position()).params['position']


    def fire_event(self, event):
        for c in sorted(self.component_list): # Needs to be a priority list
            event = c.fire_event(event)
        return event

    def __repr__(self):
        return '<GameObject name={0}>'.format(self.name).encode('utf-8')


class GameObjectFactory(object):
    root = xml.etree.ElementTree.parse(r'./ECS/objects.xml').getroot()
    blueprints = root.getchildren()

    @staticmethod
    def CreateObject(object_name):
        #return GameObjectFactory.ParseXMLComponents(object_name, GameObjectFactory.get_blueprint(object_name))
        return GameObjectFactory.ParseXMLComponentsForEntity(object_name, GameObjectFactory.get_blueprint(object_name))


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
        return GameObject(name, component_list)

    @staticmethod
    def ParseXMLComponentsForEntity(name, bp_list):
        entity = Entity()
        entity.name = name
        added_components = []
        #print "Parse_List: ", bp_list
        bp_list = deepcopy(bp_list)
        for bp in bp_list:
            for component in bp.iter('Component'):
                component_name = component.attrib.pop('name')
                if component_name not in added_components:
                    added_components.append(component_name)
                    entity[component_name] = component.attrib
                    #component_list.append(component_type(**component.attrib))
        return entity

    @staticmethod
    def get_blueprint(name, bp_list=None):
        if not bp_list:
            #print "Cleared"
            bp_list = []

        for bp in GameObjectFactory.blueprints:
            if bp.get('name') == name:
                bp_list.append(bp)
                #print name
                if bp.get('inherits'):
                    i_name = bp.get('inherits')
                    #print "Inherits ", i_name
                    #print "Before: ", bp_list
                    bp_list = GameObjectFactory.get_blueprint(i_name, bp_list)
#                    print "After: ", bp_list
            else:
                #rint 'No ', name, " Found"
                pass
        return bp_list


object_list = []


def send_global_event(event, key=None, value=None):
    for o in object_list:
        result = o.fire_event(copy(event))
        if key and value and result:
            if result.params[key] == value:
                return result
    return False
    #print event


def remove_object(obj):
    global object_list
    object_list.remove(obj)


def game_loop():
    test()
    print "###########################################"
    #print object_list

    Systems.RenderWorldSystem.UpdateCache(object_list)
    Systems.InputSystem().UpdateCache(object_list)
    Systems.AISystem().UpdateCache(object_list)
    #Systems.MapSystem().UpdateCache(object_list)
    Systems.PhysicsSystem().UpdateCache(object_list)

    #print "Draw Map"
    Systems.MapSystem.Event(Events.render_map('main'))
    #send_global_event(Events.draw('map'))
    #send_global_event(Events.draw('objects'))

    while True:
        #terminal.layer(1)
        #terminal.clear_area(0, 0, 80, 25)
        Input.update()
        mouse = Input.mouse
        key = Input.key

        #print "Draw Objects"
        #send_global_event(Events.draw('objects'))

        #print "players turn"
        #if send_global_event(Events.input(key, mouse), 'status', 'charging'):
        #    send_global_event(Events.AI())
        status = Systems.InputSystem().OnTurn()
        if status == 'waiting':
            pass
        elif status == 'charging':
            Systems.AISystem().OnTurn()
        elif status == 'turn_end':
            pass
        Systems.PhysicsSystem().OnTurn()
        Systems.RenderWorldSystem.OnTurn()


        #if player.fire_event(Events.input(key, mouse)).params['status'] == 'charging':
        #    send_global_event(Events.AI())

        terminal.refresh()



def test():
    global object_list, player

    #terminal.composition(False)

    map = GameObjectFactory.CreateObject('map')

    r = GameObjectFactory.CreateObject('rat')

    player = GameObjectFactory.CreateObject('player')

    things = ['rat', 'kobold', 'sword']

    for thing in range(SPAWNS):
        obj_name = random.choice(things)
        obj = GameObjectFactory.CreateObject(obj_name)

        #obj.fire_event(Events.move_to(Position(random.randint(1, 79), random.randint(1, 24))))
        obj.getComponent('Physics')['position'] = Position(random.randint(1, 79), random.randint(1, 24))
        #obj.getComponent('Physics')['position'] = Position(8, 10)
        obj.getComponent('Physics')['last_position'] = Position(-1, -1)

        obj.getComponent('Render')['layer'] = 2


        object_list.append(obj)

    print player
    print player['Container']





    #p.fire_event(Events.add_item(s))
    player['Physics']['position'] = Position(20, 8)
    player['Physics']['last_position'] = Position(-1, -1)
    player['Render']['layer'] = 2
    object_list.append(player)

    map['Map']['map'] = [c for c in
                    '######.........#.#.......#.....#...#.....#.........#.#...#.#.......#.......###########.#.###.#.#.#.#######.#.#####.#.###.#.#.#####.#.###.#.#.#######.###########.....#.#.#...#.#.........#.#.#.....#.###...#.#.....#.......#.......#.....#######.#.#.###.#.#####.#.#.#######.#.#.#.#.#####################.#.###.#######.#######.#.#.#...#...#...#.#...#.#.#.#.#.#.#.........#.....#...........#.#.............#####.#.#######.#######.#.#.#.#.#.#######.#.#.#.#.#.#.#######.#######.#######.#.###...#...#####.#.#####.#...#...#.#...#.#.#.#...#.#...###...#.#.......#.......#.#####.###.#####.#.#####.#.###.#.###.###.#.#.###.#########.#####.###.#############.........###.#.....###.#...#.#.#.#.......#.#...#...#.#.#.#.......#.###...#.....#########.###.#.#.#.###.#.#.###.#.#.#####.#.###.#.###.#.#.#.#.###.#####.###.#.###.......#.....#.#.#.#...#.#...........#...#.#.....#.......#.#...#.#.........#...#####.#.#.#####.#.###.#######.#######.###.#.#.###.#.#####.#.#####.#.#.#####.#####...#.#.#.......#...#.....#.....#.#...#####.#...#.......#.#...#.....#...#.#.....###.###.#.#.#.###.#####.#.#####.#.#.#######.#####.#####.#.###.#.###.#####.#####.###...#...#.#.#.......#.#.....#...#.......#...#...#.....#.....#...#...........#.#####.#.###########.###.#.###.#####.#######.###.###########.###.###.#####.###.#######...###.....#...#.#.#...#...........###...#.###...#.###.###...#.....#.#.....#####.#####.#######.#.###.###.#.#####.#.#############.#.###.#####.#####.#.###.#######.........#.#...#.....#.#.#.#.....#.###.#...#.............#...#####.#...#...#######.#.#####.#.###.#.#.#.###.#######.###.#.#####.###.#################.#############.#...#.#.....#.#.#.#...#...###...###.....#...#.......#########...#.......#######.###.#.#####.#####.#.###.#.###.#.###.#.###.###.#####.#########.#########.#######.#.#.#...###...#...#.#.#.#...#.#.....#.#.#...#.###...#########...#.......#########.#.###.#######.#.#.#.###.#######.###.#.#####.###############.#.###.#############...###.........#.#.......#######.#.....#####.......#########.#.........#'
                    ]

    object_list.append(map)




