from ECS import Component
from ECS import Position
from ECS import GameObject
from ECS import send_global_event
from ECS import remove_object
import Events
from ast import literal_eval as make_tuple
from bltColor import bltColor
from bearlibterminal import terminal
import random


class Map(Component):
    def __init__(self, *args, **kwargs):
        Component.__init__(self)
        self.map = [c for c in
                    '######.........#.#.......#.....#...#.....#.........#.#...#.#.......#.......###########.#.###.#.#.#.#######.#.#####.#.###.#.#.#####.#.###.#.#.#######.###########.....#.#.#...#.#.........#.#.#.....#.###...#.#.....#.......#.......#.....#######.#.#.###.#.#####.#.#.#######.#.#.#.#.#####################.#.###.#######.#######.#.#.#...#...#...#.#...#.#.#.#.#.#.#.........#.....#...........#.#.............#####.#.#######.#######.#.#.#.#.#.#######.#.#.#.#.#.#.#######.#######.#######.#.###...#...#####.#.#####.#...#...#.#...#.#.#.#...#.#...###...#.#.......#.......#.#####.###.#####.#.#####.#.###.#.###.###.#.#.###.#########.#####.###.#############.........###.#.....###.#...#.#.#.#.......#.#...#...#.#.#.#.......#.###...#.....#########.###.#.#.#.###.#.#.###.#.#.#####.#.###.#.###.#.#.#.#.###.#####.###.#.###.......#.....#.#.#.#...#.#...........#...#.#.....#.......#.#...#.#.........#...#####.#.#.#####.#.###.#######.#######.###.#.#.###.#.#####.#.#####.#.#.#####.#####...#.#.#.......#...#.....#.....#.#...#####.#...#.......#.#...#.....#...#.#.....###.###.#.#.#.###.#####.#.#####.#.#.#######.#####.#####.#.###.#.###.#####.#####.###...#...#.#.#.......#.#.....#...#.......#...#...#.....#.....#...#...........#.#####.#.###########.###.#.###.#####.#######.###.###########.###.###.#####.###.#######...###.....#...#.#.#...#...........###...#.###...#.###.###...#.....#.#.....#####.#####.#######.#.###.###.#.#####.#.#############.#.###.#####.#####.#.###.#######.........#.#...#.....#.#.#.#.....#.###.#...#.............#...#####.#...#...#######.#.#####.#.###.#.#.#.###.#######.###.#.#####.###.#################.#############.#...#.#.....#.#.#.#...#...###...###.....#...#.......#########...#.......#######.###.#.#####.#####.#.###.#.###.#.###.#.###.###.#####.#########.#########.#######.#.#.#...###...#...#.#.#.#...#.#.....#.#.#...#.###...#########...#.......#########.#.###.#######.#.#.#.###.#######.###.#.#####.###############.#.###.#############...###.........#.#.......#######.#.....#####.......#########.#.........#'
                    ]
        self.width = 80
        self.height = 25
        self.priority = 1

    def fire_event(self, event):
        if event.ID == 'draw_map':
            terminal.layer(0)
            for x in xrange(0, self.width):
                for y in xrange(0, self.height):
                    terminal.puts(x, y, "[color={0}]{1}".format('gray', self.map[y * self.width + x]))

        if event.ID == 'is_blocked':
            try:
                if self.map[event.params['position'].y * self.width + event.params['position'].x] == '#':
                    event.params['blocked'] = True
                    event.params['target'] = 'a solid wall'
                else:
                    pass #print "Not Blocked by map."
            except:

                event.params['blocked'] = True
                event.params['target'] = 'the dark below...'
        return event


class Input(Component):
    def __init__(self, **kwargs):
        Component.__init__(self)
        self.energy_max = int(kwargs.get('energy_max'))
        self.energy_cost = int(kwargs.get('energy_cost'))
        self.energy = self.energy_max
        self.priority = 2

    def fire_event(self, event):
        if event.ID == 'input':
            if self.energy >= self.energy_max:
                event.params['status'] = 'waiting'
                if event.params['key'] == terminal.TK_LEFT:

                    self.owner.fire_event(Events.move(Position(-1, 0)))
                    event.params['status'] = 'turn_end'
                    self.energy = 0
                if event.params['key'] == terminal.TK_RIGHT:

                    self.owner.fire_event(Events.move(Position(1, 0)))
                    event.params['status'] = 'turn_end'
                    self.energy = 0
                if event.params['key'] == terminal.TK_UP:
                    self.owner.fire_event(Events.move(Position(0, -1)))
                    event.params['status'] = 'turn_end'
                    self.energy = 0
                if event.params['key'] == terminal.TK_DOWN:
                    self.owner.fire_event(Events.move(Position(0, 1)))
                    event.params['status'] = 'turn_end'
                    self.energy = 0
                if event.params['key'] == terminal.TK_COMMA:
                    print "attempt to pickup"
                    send_global_event(Events.search(self.owner.position, self.owner))
                if event.params['key'] == terminal.TK_I:
                    results = self.owner.fire_event(Events.contents())
                    print "Inventory: {0} | {1} slots remaining".format(results.params['contents'], results.params['space'])
                if event.params['key'] == terminal.TK_E:
                    self.owner.fire_event(Events.equip())
                if event.params['key'] == terminal.TK_0:
                    terminal.layer(0)
                    terminal.clear_area(0, 0, 80, 25)
                if event.params['key'] == terminal.TK_1:
                    terminal.layer(1)
                    terminal.clear_area(0, 0, 80, 25)
                if event.params['key'] == terminal.TK_2:
                    terminal.layer(2)
                    terminal.clear_area(0, 0, 80, 25)
            else:
                self.energy += 10
                event.params['status'] = 'charging'




        return event


class AI(Component):
    def __init__(self, *args, **kwargs):
        Component.__init__(self)
        self.energy_max = int(kwargs.get('energy_max'))
        self.energy_cost = int(kwargs.get('energy_cost'))
        self.energy = self.energy_max
        self.priority = 3

    def fire_event(self, event):
        if event.ID == 'AI':
            if self.energy >= self.energy_max:
                #print self.owner.name + ", takes a turn"
                pos = random.choice([Position(1, 0),Position(0, 1),Position(-1, 0),Position(0, -1)])
                self.owner.fire_event(Events.move(pos))
                self.energy = 0
                pass
            else:
                self.energy += 10
        return event




class Container(Component):
    def __init__(self, size):
        Component.__init__(self)
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
        self.equip_on = kwargs.get('equip_on').split()
        self.priority = 15

    def fire_event(self, event):
        if event.ID == 'equip':
            event.params['equipable_on'] = self.equip_on

        return event


class Equipment(Component):
    def __init__(self, **kwargs):
        Component.__init__(self)
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
        self.position = Position(*make_tuple(kwargs['position']))
        self.solid = kwargs['solid'] == 'True'
        self.trans = kwargs['trans'] == 'True'
        self.priority = 100

    def fire_event(self, event):
        #print self.owner.name, " Physics......"
        if event.ID == 'position' or event.ID == 'draw_objects':
            #print self.position, " position of ", self.owner.name
            event.params['position'] = self.position
            event.params['new_position'] = self.position
            event.params['last_position'] = None

        #if event.ID == 'draw_objects':
        #    #print "Added Pos to Draw Event", self.position
        #    event.params['position'] = self.position
        if event.ID == 'move':
            new_pos = Position(self.position[0] + event.params['move'][0], self.position[1] + event.params['move'][1])
            blocked_result = send_global_event(*Events.is_blocked(new_pos))

            if blocked_result:
                if isinstance(blocked_result.params['target'], GameObject):
                    #print "You should be attacking a {0}".format(blocked_result.params['target'].name)
                    self.owner.fire_event(Events.attack(blocked_result.params['target']))

                else:
                    #print "You cannot move there because of {0}".format(blocked_result.params['target'])
                    pass
            else:
                print "set....."
                event.params['new_position'] = new_pos
                event.params['last_position'] = self.position
                self.position = new_pos

        if event.ID == 'move_to':
            new_pos = event.params['move_to']
            blocked_result = send_global_event(*Events.is_blocked(new_pos))

            if blocked_result:
                if isinstance(blocked_result.params['target'], GameObject):
                    #print "You should be attacking a {0}".format(blocked_result.params['target'].name)
                    self.owner.fire_event(Events.attack(blocked_result.params['target']))

                else:
                    #print "You cannot move there because of {0}".format(blocked_result.params['target'])
                    pass
            else:
                self.position = new_pos

        if event.ID == 'is_blocked':
            #print "Self: ", self.position
            #print "Event: ", event.params['position']
            if self.solid:
                if self.position == event.params['position']:
                    event.params['blocked'] = True
                    event.params['target'] = self.owner
        if event.ID == 'draw_objects':
            event.params['layer'] = 2

        return event


class Collectible(Component):
    def __init__(self, **kwargs):
        Component.__init__(self)
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
                    remove_object(item)
                    print "Picked it up!"
                else:
                    print "Cannot pick_up"
        if event.ID == 'draw_objects':
            event.params['layer'] = 1
        return event


class Combat(Component):
    def __init__(self, **kwargs):
        Component.__init__(self)
        self.hp = int(kwargs.get('hp'))
        self.power = int(kwargs.get('power'))
        self.defense = int(kwargs.get('defense'))
        self.priority = 175

    def fire_event(self, event):
        if event.ID == 'attack':

            target = event.params['target']
            #print "{0} attacks {1}".format(self.owner.name, target.name)
            power = event.params['power'] + self.power
            type = event.params['type']
            result = target.fire_event(Events.take_damage(power, type))

        if event.ID == 'take_damage':
            damage = max((event.params['power'] - self.defense), 0)   # Simple placeholder
            type = event.params['type']
            self.hp = self.hp - damage
            if self.hp <= 0:
                self.owner.fire_event(Events.death())
            #print "{0} takes {1} {2} damage.".format(self.owner.name, damage, type )
            #print "{0} has {1} HP remaining".format(self.owner.name, self.hp)
        if event.ID == 'death':
            remove_object(self.owner)
        return event


class Render(Component):

    def __init__(self, *args, **kwargs):
        Component.__init__(self)
        self.glyph = kwargs['glyph']
        self.color = bltColor(kwargs['color'])
        self.priority = 195

    def fire_event(self, event):
        if event.ID == 'move' or event.ID == 'draw_objects': # was draw_objects

            pos = event.params['new_position']
            last_pos = event.params['last_position']

            #print "Draw: ", pos, self.glyph
            if 'layer' in event.params.keys():
                terminal.layer(event.params['layer'])
            else:
                terminal.layer(2)

            if last_pos:
                print "Had Last...."
                terminal.composition(False)
                terminal.puts(last_pos[0], last_pos[1], " ")
            if pos:
                terminal.composition(True)
                terminal.puts(pos[0], pos[1], "[color={0}]{1}".format(self.color, self.glyph))
            #print "Added stuff to Draw event!"
            #event.params['color'] = self.color
            #event.params['glyph'] = self.glyph
        return event



