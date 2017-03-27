from bearlibterminal import terminal
import Engine.Input as Input
from ECS import Position
import Events
import random
from QuadTree import Index

class System(object):
    @staticmethod
    def UpdateCache(object_list):
        pass

    @staticmethod
    def OnUpdate():
        pass

    @staticmethod
    def OnTurn():
        pass

    @staticmethod
    def Event(event):
        pass


class MapSystem(object):
    queue_list = []


    @staticmethod
    def UpdateCache(object_list):
        MapSystem.queue_list = [e for e in object_list if e.getComponent('Map')]



    @staticmethod
    def OnUpdate():
        pass

    @staticmethod
    def OnTurn():
        pass

    @staticmethod
    def Event(event):
        if event.ID == 'is_blocked':
            for e in MapSystem.queue_list:
                map = e.getComponent('Map')['map']
                width = int(e.getComponent('Map')['width'])
                try:
                    if map[event.params['position'].y * width + event.params['position'].x] == '#':
                        event.params['blocked'] = True
                        event.params['target'] = 'a solid wall'

                    else:
                        pass
                except:
                    event.params['blocked'] = True
                    event.params['target'] = 'the dark below...'
        if event.ID == 'render_map':
            for e in MapSystem.queue_list:
                map = e.getComponent('Map')['map']
                width = int(e.getComponent('Map')['width'])
                height = int(e.getComponent('Map')['height'])
                id = e.getComponent('Map')['id']

                if id == event.params['id']:
                    terminal.layer(0)
                    for x in xrange(0, width-1):
                        for y in xrange(0, height-1):
                            index = y * width + x
                            try:
                                terminal.puts(x, y, "[color={0}]{1}".format('gray', map[index]))
                            except:
                                pass

        return event






class RenderWorldSystem(System):
    queue_list = []

    @staticmethod
    def UpdateCache(object_list):
        RenderWorldSystem.queue_list = [e for e in object_list if e.getComponent('Physics') and e.getComponent('Render')]


    @staticmethod
    def OnTurn():
        terminal.layer(1)
        terminal.clear_area(0, 0, 100, 50)
        terminal.layer(2)
        terminal.clear_area(0, 0, 100, 50)
        for e in RenderWorldSystem.queue_list:
            p = e['Physics']
            r = e['Render']
            if r['dirty'] == 'True':
                pos = p['position']
                last_pos = p['last_position']
                layer = r['layer']

                #terminal.layer(layer)
                #terminal.clear_area(last_pos[0], last_pos[1], 1, 1)
                #p['last_position'] = Position(-1, -1)
                terminal.puts(pos[0], pos[1], "[color={0}]{1}".format(r['color'], r['glyph']))
                #r['dirty'] = 'False'


class PhysicsSystem(System):
    queue_list = []
    spindex = None

    @staticmethod
    def UpdateCache(object_list):
        PhysicsSystem.queue_list = [e for e in object_list if e.getComponent('Physics')]
        PhysicsSystem.spindex = Index(bbox=(0, 0, 80, 25))
        #print PhysicsSystem.spindex.__class__
        for e in PhysicsSystem.queue_list:
            if e['Physics']['solid'] == 'True':
                pos = e['Physics']['position']
                PhysicsSystem.spindex.insert(e, (pos.x, pos.y, pos.x, pos.y) )

    @staticmethod
    def OnTurn():
        #PhysicsSystem.spindex = Index(bbox=(0, 0, 80, 25))

        #print "Count: ", count
        #PhysicsSystem.spindex.children
        pass

    @staticmethod
    def OnUpdate():
        pass

    @staticmethod
    def Event(event):
        if event.ID == 'move':
            e = event.params['actor']
            pos = event.params['actor'].getComponent('Physics')['position']
            direction = event.params['direction']
            new_pos = Position(pos.x + direction.x, pos.y + direction.y)
            # check if can...
            map_blocked = MapSystem.Event(Events.is_blocked(new_pos)).params['blocked']
            if not map_blocked:
                result = PhysicsSystem.Event(Events.is_blocked(new_pos))
                #print result
                if result.params['blocked']:
                    #print "Blocked by: ", result.params['target']
                    CombatSystem.Combat(e, result.params['target'])
                    pass
                else:
                    PhysicsSystem.spindex.remove(e, (pos.x - 1, pos.y - 1, pos.x, pos.y) )
                    event.params['actor'].getComponent('Physics')['last_position'] = pos
                    event.params['actor'].getComponent('Physics')['position'] = new_pos
                    PhysicsSystem.spindex.insert(e, (new_pos.x, new_pos.y, new_pos.x, new_pos.y))
                    event.params['actor'].getComponent('Render')['dirty'] = "True"
            else:
                #print "Blocked by: Map"
                pass


        if event.ID == 'is_blocked':
            pos = event.params['position']

            result = PhysicsSystem.spindex.intersect((pos.x-1, pos.y-1, pos.x, pos.y))
            #print pos, result
            if len(result) > 0:
                event.params['blocked'] = True
                event.params['target'] = result[0]

        return event

class AISystem(System):
    queue_list = []

    @staticmethod
    def UpdateCache(object_list):
        AISystem.queue_list = [e for e in object_list if e.getComponent('AI') and e.getComponent('Physics')]

    @staticmethod
    def OnTurn():
        for e in AISystem.queue_list:
            if int(e['AI']['energy']) >= int(e['AI']['energy_max']):
                #print self.owner.name + ", takes a turn"
                pos = random.choice([Position(1, 0), Position(0, 1), Position(-1, 0), Position(0, -1)])
                PhysicsSystem.Event(Events.move(e, pos))
                e['AI']['energy'] = 0
                pass
            else:
                e['AI']['energy'] += 10



class CombatSystem(System):
    queue_list = []

    @staticmethod
    def UpdateCache(object_list):
        CombatSystem.queue_list = [e for e in object_list if e.getComponent('Combat')]

    @staticmethod
    def OnTurn():
        pass

    @staticmethod
    def Combat(attacker, defender):
        if not attacker.getComponent('Combat'):
            return False
        if not defender.getComponent('Breakble'):
            if not defender.getComponent('Combat'):
                return False
            else:
                print attacker.name, " Bumped into ", defender.name, "."
                pass
        else:
            # BREAKABLE
            pass
        return False


    def _MonsterCombat(self):
        pass

    def CombatValues(self, entity):
        c = entity.getComponent('Combat')








class InputSystem(System):
    queue_list = []

    @staticmethod
    def UpdateCache(object_list):
        InputSystem.queue_list = [e for e in object_list if e.getComponent('Input') and e.getComponent('Physics')]

    @staticmethod
    def OnTurn():
        key = Input.key
        mouse = Input.mouse
        for e in InputSystem.queue_list:
            if int(e['Input']['energy']) >= int(e['Input']['energy_max']):
                #print "HERE?????"
                if key == terminal.TK_LEFT:

                    PhysicsSystem.Event(Events.move(e, Position(-1, 0)))
                    e['Input']['energy'] = 0
                    return 'turn_end'
                if key == terminal.TK_RIGHT:
                    PhysicsSystem.Event(Events.move(e, Position(1, 0)))
                    e['Input']['energy'] = 0
                    return 'turn_end'
                if key == terminal.TK_UP:
                    PhysicsSystem.Event(Events.move(e, Position(0, -1)))
                    e['Input']['energy'] = 0
                    return 'turn_end'
                if key == terminal.TK_DOWN:
                    PhysicsSystem.Event(Events.move(e, Position(0, 1)))
                    e['Input']['energy'] = 0
                    return 'turn_end'
                if key == terminal.TK_COMMA:
                    pass
                if key == terminal.TK_I:
                    splist = PhysicsSystem.spindex

                    print splist._countmembers()
                    print "Result: ", splist.intersect((7,9,8,10))

                if key == terminal.TK_E:
                    pass
                return 'waiting'
            else:
                e['Input']['energy'] += 10
                return 'charging'



