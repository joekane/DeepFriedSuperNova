from ECS import Component
from ECS import Position
import Events
from ast import literal_eval as make_tuple
from bltColor import bltColor


class Map(Component):
    def __init__(self, *args, **kwargs):
        Component.__init__(self)
        self.name = "Map"
        self.map = [c for c in
                    '######.........#.#.......#.....#...#.....#.........#.#...#.#.......#.......###########.#.###.#.#.#.#######.#.#####.#.###.#.#.#####.#.###.#.#.#######.###########.....#.#.#...#.#.........#.#.#.....#.###...#.#.....#.......#.......#.....#######.#.#.###.#.#####.#.#.#######.#.#.#.#.#####################.#.###.#######.#######.#.#.#...#...#...#.#...#.#.#.#.#.#.#.........#.....#...........#.#.............#####.#.#######.#######.#.#.#.#.#.#######.#.#.#.#.#.#.#######.#######.#######.#.###...#...#####.#.#####.#...#...#.#...#.#.#.#...#.#...###...#.#.......#.......#.#####.###.#####.#.#####.#.###.#.###.###.#.#.###.#########.#####.###.#############.........###.#.....###.#...#.#.#.#.......#.#...#...#.#.#.#.......#.###...#.....#########.###.#.#.#.###.#.#.###.#.#.#####.#.###.#.###.#.#.#.#.###.#####.###.#.###.......#.....#.#.#.#...#.#...........#...#.#.....#.......#.#...#.#.........#...#####.#.#.#####.#.###.#######.#######.###.#.#.###.#.#####.#.#####.#.#.#####.#####...#.#.#.......#...#.....#.....#.#...#####.#...#.......#.#...#.....#...#.#.....###.###.#.#.#.###.#####.#.#####.#.#.#######.#####.#####.#.###.#.###.#####.#####.###...#...#.#.#.......#.#.....#...#.......#...#...#.....#.....#...#...........#.#####.#.###########.###.#.###.#####.#######.###.###########.###.###.#####.###.#######...###.....#...#.#.#...#...........###...#.###...#.###.###...#.....#.#.....#####.#####.#######.#.###.###.#.#####.#.#############.#.###.#####.#####.#.###.#######.........#.#...#.....#.#.#.#.....#.###.#...#.............#...#####.#...#...#######.#.#####.#.###.#.#.#.###.#######.###.#.#####.###.#################.#############.#...#.#.....#.#.#.#...#...###...###.....#...#.......#########...#.......#######.###.#.#####.#####.#.###.#.###.#.###.#.###.###.#####.#########.#########.#######.#.#.#...###...#...#.#.#.#...#.#.....#.#.#...#.###...#########...#.......#########.#.###.#######.#.#.#.###.#######.###.#.#####.###############.#.###.#############...###.........#.#.......#######.#.....#####.......#########.#.........#'
                    ]
        self.width = 80
        self.height = 25
        self.id = 'main'
        self.priority = 1


class Input(Component):
    def __init__(self, **kwargs):
        Component.__init__(self)
        self.name = "Input"
        self.energy_max = int(kwargs.get('energy_max'))
        self.energy_cost = int(kwargs.get('energy_cost'))
        self.energy = self.energy_max
        self.priority = 2


class AI(Component):
    def __init__(self, *args, **kwargs):
        Component.__init__(self)
        self.name = "AI"
        self.energy_max = int(kwargs.get('energy_max'))
        self.energy_cost = int(kwargs.get('energy_cost'))
        self.energy = self.energy_max
        self.priority = 3


class Container(Component):
    def __init__(self, size):
        Component.__init__(self)
        self.name = "Container"
        self.size = int(size)
        self.contents = []
        self.priority = 10

    def fire_event(self, event):
        if event.ID == 'contents' or event.ID == 'equip':
            #print self.owner.name
            #print self.contents
            #self.contents.append('Yo!')
            event.params['contents'] = self.contents
            event.params['space'] = self.size - len(self.contents)

        if event.ID == 'add_item':

            if len(self.contents) < self.size:
                item = event.params['item']
                self.contents.append(item)
                event.params['result'] = True
            else:
                event.params['result'] = False

        if event.ID == 'remove_item':
            if event.params['item'] in self.contents:
                self.contents.remove(event.params['item'])
                event.params['result'] = True
            else:
                event.params['result'] = False
        return event


class Equipable(Component):
    def __init__(self, **kwargs):
        Component.__init__(self)
        self.name = "Equipable"
        self.equip_on = kwargs.get('equip_on').split()
        self.priority = 15

    def fire_event(self, event):
        if event.ID == 'equip':
            event.params['equipable_on'] = self.equip_on

        return event


class Equipment(Component):
    def __init__(self, **kwargs):
        Component.__init__(self)
        self.name = "Equipment"
        self.equipment = dict(zip(kwargs.get('slots').split(), [None for i in kwargs.get('slots').split()]))
        self.priority = 40

    def fire_event(self, event):
        if event.ID == 'equip':
            item = event.params['item']

            inventory = event.params['contents']
            #print "Equip", inventory
            # AUTO EQUIP
            for i in inventory:
                print "I loop"
                equip_on = i.fire_event(Events.equip()).params['equipable_on']
                for location in equip_on:
                    print "L loop"
                    if self.equipment[location] is None:
                        print "do It!"
                        self.equipment[location] = i
                        self.owner.fire_event(Events.remove_item(i))
                        break

                #if all(name in event.params[''] for name in e)
        if event.ID == 'attack':
            for equip in self.equipment.keys():
                if self.equipment[equip] is not None:
                    event = self.equipment[equip].fire_event(event)

        return event


class Fiery(Component):
    def __init__(self, **kwargs):
        Component.__init__(self)
        self.name = "Fiery"
        self.damage_type = 'Fire'
        self.power = int(kwargs.get('power'))
        self.priority = 90

    def fire_event(self, event):
        if event.ID == 'attack':
            #print "Added {0} Fire Damage!".format(self.power)
            event.params['power'] += self.power
            event.params['type'] += "," + self.damage_type
        return event


class Weapon(Component):
    def __init__(self, **kwargs):
        Component.__init__(self)
        self.name = "Weapon"
        self.damage = int(kwargs.get('damage'))
        self.type = kwargs.get('type')
        self.equiped = False
        self.priority = 90

    def fire_event(self, event):
        if event.ID == 'attack':
            #print "Added {0} {1} Damage!".format(self.damage, self.type)
            event.params['power'] += self.damage
            event.params['type'] += "," + self.type
        return event


class Physics(Component):
    def __init__(self, *args, **kwargs):
        Component.__init__(self)
        self.name = "Physics"
        self.position = Position(*make_tuple(kwargs['position']))
        self.last_position = Position(-1, -1)
        self.solid = kwargs['solid'] == 'True'
        self.trans = kwargs['trans'] == 'True'
        self.priority = 100


class Collectible(Component):
    def __init__(self, **kwargs):
        Component.__init__(self)
        self.name = "Collectible"
        self.priority = 150

    def fire_event(self, event):
        if event.ID == 'search':
            item_pos = self.owner.position
            pickup_pos = event.params['position']
            searcher = event.params['owner']
            if item_pos == pickup_pos:
                item = self.owner
                result = event.params['owner'].fire_event(Events.add_item(item))
                if result.params['result']:
                    #remove_object(item)
                    print "Picked it up!"
                else:
                    print "Cannot pick_up"
        return event


class Combat(Component):
    def __init__(self, **kwargs):
        Component.__init__(self)
        self.name = "Combat"
        self.hp = int(kwargs.get('hp'))
        self.power = int(kwargs.get('power'))
        self.defense = int(kwargs.get('defense'))
        self.priority = 175


class Render(Component):

    def __init__(self, *args, **kwargs):
        Component.__init__(self)
        self.name = "Render"
        self.glyph = kwargs['glyph']
        self.layer = int(kwargs['layer'])
        self.color = bltColor(kwargs['color'])
        self.dirty = True
        self.priority = 195

