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


class EntityManager():
    entity_list = []
    update_caches = True

    @staticmethod
    def remove_entity(e):
        #print"LIST: ", EntityManager.entity_list
        #print "ITEM: ", e
        if e in EntityManager.entity_list:
            EntityManager.entity_list.remove(e)
        EntityManager.update_caches = True

    @staticmethod
    def UpdateSystems():
        RenderWorldSystem.UpdateCache()
        InputSystem.UpdateCache()
        AISystem.UpdateCache()
        MapSystem.UpdateCache()
        PhysicsSystem.UpdateCache()
        CombatSystem.UpdateCache()
        CollectableSystem.UpdateCache()

    @staticmethod
    def OnUpdate():
        if EntityManager.update_caches:
            EntityManager.update_caches = False
            EntityManager.UpdateSystems()


class MapSystem(object):
    queue_list = []


    @staticmethod
    def UpdateCache():
        entity_list = EntityManager.entity_list
        MapSystem.queue_list = [e for e in entity_list if e.get_component('Map')]



    @staticmethod
    def OnUpdate():
        pass

    @staticmethod
    def OnTurn():
        pass

    @staticmethod
    def is_blocked(position, map='main'):
        for e in MapSystem.queue_list:
            m = e.get_component('Map')
            map = m.map
            width = m.width
            try:
                if map[position.y * width + position.x] == '#':
                    return True, 'a solid wall'
                else:
                    return False, None
            except:
                return True, 'The dark below...'
        return False, None

    @staticmethod
    def render_map(id='main'):
        for e in MapSystem.queue_list:
            m = e.get_component('Map')
            map = m.map
            width = m.width
            height = m.height
            map_id = m.id

            if map_id == id:
                terminal.layer(0)
                for x in xrange(0, width - 1):
                    for y in xrange(0, height - 1):
                        index = y * width + x
                        try:
                            terminal.puts(x, y, "[color={0}]{1}".format('gray', map[index]))
                        except:
                            pass


class RenderWorldSystem(System):
    queue_list = []

    @staticmethod
    def UpdateCache():
        entity_list = EntityManager.entity_list
        RenderWorldSystem.queue_list = [e for e in entity_list if e.get_component('Physics') and e.get_component('Render')]


    @staticmethod
    def OnTurn():
        terminal.layer(1)
        terminal.clear_area(0, 0, 100, 50)
        terminal.layer(2)
        terminal.clear_area(0, 0, 100, 50)
        for e in RenderWorldSystem.queue_list:
            p = e.get_component('Physics')
            r = e.get_component('Render')
            if r.dirty == True:
                pos = p.position
                last_pos = p.last_position

                terminal.layer(r.layer)
                terminal.clear_area(last_pos[0], last_pos[1], 1, 1)
                #p['last_position'] = Position(-1, -1)
                terminal.puts(pos[0], pos[1], "[color={0}]{1}".format(r.color, r.glyph))
                #r.dirty = False


class PhysicsSystem(System):
    queue_list = []
    spindex = None

    @staticmethod
    def UpdateCache():
        entity_list = EntityManager.entity_list
        PhysicsSystem.queue_list = [e for e in entity_list if e.get_component('Physics')]
        PhysicsSystem.spindex = Index(bbox=(0, 0, 80, 25))
        #print PhysicsSystem.spindex.__class__
        for e in PhysicsSystem.queue_list:
            p = e.get_component('Physics')
            if p.solid == True:
                pos = p.position
                PhysicsSystem.add_to_collision_system(e)
        #print "Cache Updated ({0})".format(len(PhysicsSystem.queue_list))
        #print "Index Updated ({0})".format(PhysicsSystem.entity_count())



    @staticmethod
    def OnTurn():
        #PhysicsSystem.spindex = Index(bbox=(0, 0, 80, 25))
        #print "Count: ", count
        #PhysicsSystem.spindex.children
        pass

    @staticmethod
    def entity_count():
        return PhysicsSystem.spindex._countmembers()

    @staticmethod
    def Entities_in(position=None, bbox=None):
        if position:
            return PhysicsSystem.spindex.intersect((position.x - 1, position.y - 1, position.x, position.y))
        if bbox:
            return PhysicsSystem.spindex.intersect(bbox)
        return False

    @staticmethod
    def move(entity, offset):
        pos = entity.get_component('Physics').position
        direction =offset
        new_pos = Position(pos.x + direction.x, pos.y + direction.y)
        # check if can...
        if not MapSystem.is_blocked(new_pos)[0]:
            result = PhysicsSystem.is_blocked(new_pos)
            #print result
            if result[0]:
                #print "Blocked by: ", result.params['target']
                CombatSystem.Combat(entity, result[1])
            else:
                PhysicsSystem.remove_from_collision_system(entity)
                entity.get_component('Physics').last_position = pos
                entity.get_component('Physics').position = new_pos
                PhysicsSystem.add_to_collision_system(entity)
                entity.get_component('Render').dirty = True
        else:
            #print "Blocked by: Map"
            pass

    @staticmethod
    def is_blocked(position):
        result = PhysicsSystem.Entities_in(position) #   .spindex.intersect((pos.x-1, pos.y-1, pos.x, pos.y))

        if len(result) > 0:
            #print result
            return True, result
        return False, None

    @staticmethod
    def remove_from_collision_system(entity):
        pos = entity.get_component('Physics').position
        PhysicsSystem.spindex.remove(entity, (pos.x - 1, pos.y - 1, pos.x, pos.y))

    @staticmethod
    def add_to_collision_system(entity):
        pos = entity.get_component('Physics').position
        PhysicsSystem.spindex.insert(entity, (pos.x, pos.y, pos.x, pos.y))


class AISystem(System):
    queue_list = []

    @staticmethod
    def UpdateCache():
        entity_list = EntityManager.entity_list
        AISystem.queue_list = [e for e in entity_list if e.get_component('AI') and e.get_component('Physics')]

    @staticmethod
    def OnTurn():
        for e in AISystem.queue_list:
            ai = e.get_component('AI')
            if ai.energy >= ai.energy_max:
                #print self.owner.name + ", takes a turn"
                pos = random.choice([Position(1, 0), Position(0, 1), Position(-1, 0), Position(0, -1)])
                PhysicsSystem.move(e, pos)
                ai.energy = 0
                pass
            else:
                ai.energy += 10


class CombatSystem(System):
    queue_list = []

    COMBAT_MESSAGES = False

    @staticmethod
    def UpdateCache():
        entity_list = EntityManager.entity_list
        CombatSystem.queue_list = [e for e in entity_list if e.get_component('Combat')]

    @staticmethod
    def OnTurn():
        pass

    @staticmethod
    def Combat(attacker, defender, area=False):
        if attacker.name == 'player' or defender[0].name == 'player':
            CombatSystem.COMBAT_MESSAGES = True
        else:
            CombatSystem.COMBAT_MESSAGES = False
        if not attacker.get_component('Combat'):
            return False
        if not area:
            if not defender[0].get_component('Breakble'):
                if not defender[0].get_component('Combat'):
                    return False
                else:
                    event = attacker.fire_event(Events.attack())
                    if CombatSystem.COMBAT_MESSAGES: print event.params['power']
                    added_power = event.params['power']
                    atk_combat = attacker.get_component('Combat')
                    def_combat = defender[0].get_component('Combat')
                    damage = (atk_combat.power + added_power) - def_combat.defense
                    def_combat.hp = def_combat.hp - damage
                    if CombatSystem.COMBAT_MESSAGES: print "{0} did {1} damage to {2}. ({2} HP={3}".format(str(attacker.name).capitalize(), damage, defender[0].name, def_combat.hp)

                    if def_combat.hp <= 0:
                        if CombatSystem.COMBAT_MESSAGES: print defender[0].name.capitalize(), "is dead..."
                        CombatSystem.Death(defender[0])

                    pass
            else:
                # BREAKABLE
                pass
            return False

    @staticmethod
    def Death(entity):
        # Do death things in nessasary
        PhysicsSystem.remove_from_collision_system(entity)
        EntityManager.remove_entity(entity)
        del entity
        pass

    def _MonsterCombat(self):
        pass

    def CombatValues(self, entity):
        c = entity.get_component('Combat')
    pass


class CollectableSystem(System):
    queue_list = []

    @staticmethod
    def UpdateCache():
        entity_list = EntityManager.entity_list
        CollectableSystem.queue_list = [e for e in entity_list if e.get_component('Collectible') and e.get_component('Physics')]

    @staticmethod
    def pickup(entity):
        if entity.get_component('Container'):
            for c in CollectableSystem.queue_list:
                pos = entity.get_component('Physics').position
                if pos == c.get_component('Physics').position:

                    if entity.fire_event(Events.add_item(c)).params['result']:
                        EntityManager.remove_entity(c)
                        print "Picked me up!"
                    else:
                        print "something went wrong...."



class Containter(System):
    pass


class InputSystem(System):
    queue_list = []

    @staticmethod
    def UpdateCache():
        entity_list = EntityManager.entity_list
        InputSystem.queue_list = [e for e in entity_list if e.get_component('Input') and e.get_component('Physics')]

    @staticmethod
    def OnTurn():
        key = Input.key
        mouse = Input.mouse
        for e in InputSystem.queue_list:
            i = e.get_component('Input')
            if i.energy >= i.energy_max:
                #print "HERE?????"
                if key == terminal.TK_LEFT:
                    PhysicsSystem.move(e, Position(-1, 0))
                    i.energy = 0
                    return 'turn_end'
                if key == terminal.TK_RIGHT:
                    PhysicsSystem.move(e, Position(1, 0))
                    i.energy = 0
                    return 'turn_end'
                if key == terminal.TK_UP:
                    PhysicsSystem.move(e, Position(0, -1))
                    i.energy = 0
                    return 'turn_end'
                if key == terminal.TK_DOWN:
                    PhysicsSystem.move(e, Position(0, 1))
                    i.energy = 0
                    return 'turn_end'
                if key == terminal.TK_COMMA:
                    CollectableSystem.pickup(e)
                if key == terminal.TK_I:
                    splist = PhysicsSystem.spindex

                    print splist._countmembers()
                    print "Result: ", splist.intersect((7,9,8,10))

                if key == terminal.TK_I:
                    event = e.fire_event(Events.contents())
                    print event.params['contents'], event.params['space']

                if key == terminal.TK_E:
                    event = e.fire_event(Events.equip())
                    print e.get_component('Equipment').equipment



                if mouse.lbutton_pressed:
                    terminal.layer(10)
                    terminal.clear_area(0,0,100,50)
                    print "Entities: ", PhysicsSystem.Entities_in(bbox=(mouse.cx-1, mouse.cy-1, mouse.cx+1, mouse.cy + 1))

                    terminal.puts(mouse.cx, mouse.cy, "[c=64,255,255,0]X")



                return 'waiting'


            else:
                i.energy += 10
                return 'charging'



