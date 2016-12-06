'''
/*******************************************************
 * Copyright (C) 2016-2017 Joe Kane
 *
 * This file is part of 'Deep Fried Supernova"
 *
 * Deep Fried Supernova can not be copied and/or distributed without the express
 * permission of Joe Kane
 *******************************************************/
'''

from itertools import cycle

from bearlibterminal import terminal

import Combat
import Constants
import Entity
import GameState
import Pathing
import Render
import Utils
import Engine.Animate as Animate
import libtcodpy as libtcod
import random
from Engine import Input, Schedule
from Engine import UI
from Engine import Animation_System as Animate

vCount = 0


class PlayeControlled:
    def __init__(self, owner=None):
        self.owner = owner

    def end_turn(self, cost):
        # self.owner.action_points += 100
        # Schedule.add_to_pq((self.owner.action_points, self.owner))
        self.owner.delay += cost
        # print cost
        if cost > 0:
            # print "Recalc BFS"
            """ UPDATE D-DMAP / PASS TIME"""
            Pathing.BFS(GameState.player)
            self.owner.pass_time()
            # Render.render_all()
        Input.clear()
        return cost

    def process_mouse_clicks(self, mouse):
        (map_x, map_y) = Utils.to_map_coordinates(mouse.cx, mouse.cy)
        if map_x is not None and map_y is not None:
            # walk to target tile

            if mouse.lbutton_pressed and GameState.continue_walking:
                GameState.continue_walking = False
                self.owner.clear_path()
                return 0
            if mouse.lbutton_pressed and GameState.current_level.is_explored(map_x, map_y):
                self.owner.clear_path()
                GameState.continue_walking = self.owner.move_astar_xy(map_x, map_y, True)
                return self.end_turn(Constants.TURN_COST)
            if mouse.rbutton_pressed:
                GameState.continue_walking = False
                self.owner.clear_path()
                GameState.current_level.require_recompute()
                self.owner.x, self.owner.y = Utils.to_map_coordinates(mouse.cx, mouse.cy)
                return 1
        return 0

    def process_mouse_hover(self, mouse):
        (map_x, map_y) = Utils.to_map_coordinates(mouse.cx, mouse.cy)

        if self.owner.x != map_x or self.owner.y != map_y:
            # libtcod.console_set_char_background(0, mouse.cx, mouse.cy, libtcod.Color(10, 10, 240), libtcod.BKGND_SET)
            Utils.inspect_tile(mouse.cx, mouse.cy)
        return 0

    def take_turn(self):
        global vCount
        GameState.render_all()


        mouse = Input.mouse


        while True:
            """
            On player turn this loops continuasouly waiting for user input
            """
            Input.update()
            key = Input.key
            GameState.render_ui()


            """
            Check mouse status
            """
            mouse_click_value = self.process_mouse_clicks(mouse)
            mouse_hover_value = self.process_mouse_hover(mouse)
            if mouse_click_value > 0:
                return self.end_turn(mouse_click_value)
            if mouse_hover_value > 0:
                return self.end_turn(mouse_hover_value)


            """
            Auto-Walking
            """
            if GameState.continue_walking:
                self.owner.walk_path()
                # print "Auto-Walking"
                return self.end_turn(Constants.TURN_COST)
            elif not GameState.continue_walking:
                self.owner.clear_path()

            """
            Basic User Input
            """
            if key == terminal.TK_KP_8 or key == terminal.TK_UP:
                GameState.player_move_or_interact(0, -1)
                return self.end_turn(Constants.TURN_COST)
            elif key == terminal.TK_KP_2 or key == terminal.TK_DOWN:
                GameState.player_move_or_interact(0, 1)
                return self.end_turn(Constants.TURN_COST)
            elif key == terminal.TK_KP_4 or key == terminal.TK_LEFT:
                GameState.player_move_or_interact(-1, 0)
                return self.end_turn(Constants.TURN_COST)
            elif key == terminal.TK_KP_6 or key == terminal.TK_RIGHT:
                GameState.player_move_or_interact(1, 0)
                return self.end_turn(Constants.TURN_COST)
            elif key == terminal.TK_KP_7: # or (terminal.TK_LEFT and terminal.TK_UP):
                GameState.player_move_or_interact(-1, -1)
                return self.end_turn(Constants.TURN_COST)
            elif key == terminal.TK_KP_9:
                GameState.player_move_or_interact(1, -1)
                return self.end_turn(Constants.TURN_COST)
            elif key == terminal.TK_KP_1:
                GameState.player_move_or_interact(-1, 1)
                return self.end_turn(Constants.TURN_COST)
            elif key == terminal.TK_KP_3:
                GameState.player_move_or_interact(1, 1)
                return self.end_turn(Constants.TURN_COST)
            elif key == terminal.TK_KP_5:
                return self.end_turn(Constants.TURN_COST)
            elif key == terminal.TK_X:
                GameState.current_level.require_recompute()
                Constants.DEBUG = not Constants.DEBUG
                GameState.render_all()
            elif key == terminal.TK_G:
                # pick up an item
                for object in GameState.current_level.get_all_objects():  # look for an item in the player's tile
                    if object.x == self.owner.x and object.y == self.owner.y and object.item:
                        object.item.pick_up()
                        break
            elif key == terminal.TK_F:
                for obj in GameState.get_all_equipped(self.owner):
                    if obj.owner.ranged:
                        outcome = obj.owner.ranged.fire()
                        if outcome == 'cancelled':
                            return 0
                        else:
                            return self.end_turn(Constants.TURN_COST)
            elif key == terminal.TK_B:
                title = "Beastiary"

                text = '\n\nDrag Header to move window\n\n'

                pal = UI.Palette(width=20, height=20, title='Title', text=text)

                pal.draw()
            elif key == terminal.TK_COMMA and terminal.check(terminal.TK_SHIFT):
                # go down stairs, if the player is on them
                stairs = GameState.current_level.get_stairs()
                if stairs.x == self.owner.x and stairs.y == self.owner.y:
                    GameState.next_level()
                    return 1
                    '''
                    elif key_char == 'i':
                        # Map.update_d_map()
                        # show the inventory; if an item is selected, use it
                        # img = libtcod.image_load('orc.png')
                        # libtcod.image_blit_2x(img, 0, 0, 0)

                        # img2 = libtcod.image_load('orc_80.png')
                        # libtcod.image_blit_2x(img2, 0, 40, 0)

                        # chosen_item = inventory_menu(
                        #    'Press the key next to an item to use it, or any other to cancel.\n')

                        # if chosen_item is not None:
                        #    chosen_item.use()
                        #    return 0
                        pass
                    elif key_char == '5':
                        return self.end_turn(Constants.TURN_COST)
                    elif key_char == 'f':
                        for obj in GameState.get_all_equipped(player):
                            if obj.owner.ranged:
                                outcome = obj.owner.ranged.fire()
                                if outcome == 'cancelled':
                                    return 0
                                else:
                                    return self.end_turn(Constants.TURN_COST)
                        Utils.message("No ranged weapon equipped!", libtcod.light_amber)
                    elif key_char == 'h':
                        for obj in GameState.get_inventory():
                            if obj.name == 'healing potion':
                                obj.item.use()
                                self.end_turn(Constants.TURN_COST/2)
                        return Utils.message("No helaing potions.", libtcod.light_amber)
                    elif key_char == '<':
                        # go down stairs, if the player is on them
                        stairs = Map.get_stairs()
                        if stairs.x == player.x and stairs.y == player.y:
                            GameState.next_level()

                    elif key_char == 'p':

                        title = "Shadow State Archives II"

                        text = '"The ambient phenomenon was an ancient engine, the wealthy machine. Crushing, pausing...' \
                               ' a conceptual humming which attended to the numbers underneath the intervening, silver' \
                               'sky." \n\n The towering massive ultragovernment concrete superstructure data library that' \
                               'contains the largest digital collection of intergalactic personnel files ever assembled' \
                               'in any known galaxy. Here dwell massive servers guarded by all manner of nanotechnology' \
                               'powered droids, cipher enhanced biowardens, all seeing quantum lenses, and roaming alpha' \
                               'turrets. This place is high alert.\n' \
                               '\n' \
                               'Keycard required.'

                        UI.pop_up(title=title, text=text)
                    elif key_char == 'b':

                        title = "Beastiary"

                        text = 'Cipher Warden\n\n\nHP = 50\nDEF = 10\nDODGE = 5%'

                        pal = UI.Palette(width=20, title='Title', text=text)

                        pal.draw()

                        # I.beastiary(width=50, height=45, title=title, text=text)
                    elif key_char == 's':
                        import pygame
                        print "S!"

                        #UI.skill_tree()
                        pass
                    elif key_char == 'k':
                        print "Pressed 'K'"
                        GameState.next_level()
                        Fov.require_recompute()
                        Render.render_all()
                        return 0
                    elif key_char == 'x':
                        Fov.require_recompute()
                        Constants.DEBUG = not Constants.DEBUG
                        Render.render_all()
                        return 0
                '''


class Fighter:
    # combat-related properties and methods (monster, player, NPC).
    def __init__(self, hp, defense, power, xp, sp=10, death_function=None, owner=None):
        self.xp = xp
        self.death_function = death_function
        self.base_max_hp = hp
        self.hp = hp
        self.base_max_sp = sp
        self.sp = sp
        self.base_defense = defense
        self.base_power = power
        self.owner = owner
        # STATS #
        self.base_str = 5
        self.base_def = 4
        self.base_agl = 3
        self.base_stm = 3
        self.base_skl = 3
        self.base_int = 2


    @property
    def damage(self):
        return Combat.dice(self.power)

    @property
    def save(self):
        dodge_chance = 5
        return Combat.dice('1d100') <= dodge_chance
        # determine best save and attempt it

    @property
    def damage_reduction(self):
        for st in self.owner.status:
            if 'damage_reduction' in st.keys():
                return Combat.dice(st['damage_reduction'])
        return 0

    @property
    def power(self):
        #bonus = sum(equipment.power_bonus for equipment in GameState.get_all_equipped(self.owner))
        bonus = 0
        for st in self.owner.status:
            if 'damage_bonus' in st.keys():
                bonus += st['damage_bonus']
        return self.base_power + "+" + str(bonus)

    @property
    def defense(self):  # return actual defense, by summing up the bonuses from all equipped items
        bonus = sum(equipment.defense_bonus for equipment in GameState.get_all_equipped(self.owner))

        if self.owner is GameState.get_player():
            bonus -= max(0, (GameState.current_level.number_of_adjacent_objects(GameState.get_player()) - 2))
        return self.base_defense + bonus

    @property
    def max_hp(self):  # return actual max_hp, by summing up the bonuses from all equipped items
        bonus = sum(equipment.max_hp_bonus for equipment in GameState.get_all_equipped(self.owner))
        return self.base_max_hp + bonus

    def take_damage(self, damage):
        # apply damage if possible
        player = GameState.get_player()
        if damage > 0:
            self.hp -= damage
        # check for death. if there's a death function, call it
        if self.hp <= 0:
            function = self.death_function
            if self.owner != player:  # yield experience to the player
                player.fighter.xp += self.xp
            if function is not None:
                function(self.owner)

    def heal(self, amount):
        # heal by the given amount, without going over the maximum
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def attack(self, target):
        # a simple formula for attack damage
        '''
        damage = self.power - target.fighter.defense
        if damage > 0:
            # make the target take some damage
            # print self.owner.name.capitalize() + ' attacks ' + target.name + ' for ' + str(damage) + ' hit points.'
            message(self.owner.name.capitalize() + ' attacks ' + target.name + ' for ' + str(damage) + ' hit points.')
            target.fighter.take_damage(damage)
        else:
            # print self.owner.name.capitalize() + ' attacks ' + target.name + ' but it has no effect!'
            message(self.owner.name.capitalize() + ' attacks ' + target.name + ' but it has no effect!')
        '''
        dmg = Combat.damage_calc(self, target)
        if dmg is not False:
            Utils.message(self.owner.name + " does " + str(dmg) + " damage to " + target.name, libtcod.light_red)
            target.fighter.take_damage(dmg)
        else:
            Utils.message(target.name + " evads your attack!", libtcod.light_yellow)

'''
class QuestNpc:
    def __init__(self, quest_num="0001", owner=None):
        self.given = False
        self.quest_num = quest_num
        self.owner = owner

    def take_turn(self):
        self.owner.CT=100
        return False

    def talk(self):
        global inventory
        test_item_name = GameState.get_quest_item(self.quest_num)

        if GameState.player_has_item(test_item_name):
            Utils.message("Good you got my key", libtcod.blue)
            GameState.remove_from_inventory(test_item_name)
            self.reward()
        elif self.quest_num in GameState.get_quests():
            Utils.message("Hello, we talked already!", libtcod.blue)
        else:
            # TESTING QUEST
            GameState.get_quests().append(self.quest_num)
            Utils.message(GameState.imported_quest_list[self.quest_num]['quest_text'], libtcod.blue)
            WorldGen.spawn_item_at(self.owner.x, self.owner.y + 1, 'GrisKeyRing')

    def reward(self):
        if (not self.given):
            Utils.message("That was easy, wasn't it!")
            WorldGen.spawn_item_at(self.owner.x, self.owner.y + 1, 'QuestSword')
            self.given = True
        else:
            Utils.message("greedy bastard.")
'''

class MeleeMonster:
    def __init__(self, owner=None):
        self.given = False
        self.owner = owner
        self.active = False

    # AI for a basic monster.
    def take_turn(self):
            # a basic monster takes its turn. If you can see it, it can see you
            monster = self.owner
            player = GameState.get_player()

            if GameState.current_level.is_visible(obj=monster):
                self.active = True
                GameState.continue_walking = False

            if self.active:
                # move towards player if far away
                dist = GameState.current_level.map_array[monster.x][monster.y].distance_to_player
                # print self.owner.name + " | " + str(dist)
                if dist == 1 and player.fighter.hp > 0:
                    # print "{0} fights Player.".format(monster.name)
                    monster.fighter.attack(player)
                else:
                    # print "{0} is at {1}".format(monster.name, (monster.x, monster.y))
                    dest = Pathing.get_lowest_neighbor(monster.x, monster.y)
                    # print "{0} moves to {1}.".format(monster.name, dest)
                    monster.move_to(dest[0], dest[1])
                    # monster.move_astar(player)
                    # monster.move_dijkstra(player)

            # self.owner.action_points += 100
            # Schedule.add_to_pq((self.owner.action_points, self.owner))
            return Constants.TURN_COST


class GaseusCloud:
    def __init__(self, owner=None, s_vol=50):
        self.owner = owner
        self.active = True
        self.sVol = s_vol
        self.cVol = s_vol
        self.radius = 3
        self.spread = 100
        self.points = []
        self.points = Utils.get_circle_points(self.owner.x, self.owner.y, self.radius)

    def take_turn(self):
        pass


class AssassinMonster:
    def __init__(self, owner=None):
        self.owner = owner
        self.active = True

    # AI for a basic monster.
    def take_turn(self):
            # a basic monster takes its turn. If you can see it, it can see you
            monster = self.owner
            player = GameState.get_player()
            dist = monster.distance_to(player)


            if GameState.current_level.is_visible(obj=monster):
                self.active = True
                GameState.continue_walking = False
            else:
                if dist > 250:
                    self.active = False
                else:
                    self.active = False

            if self.active:
                # move towards player if far away

                # print self.owner.name + " | " + str(dist)
                if dist <= 1.5 and player.fighter.hp > 0:
                    monster.fighter.attack(player)
                else:
                    monster.move_astar(player)


            # self.owner.action_points += 100
            # Schedule.add_to_pq((self.owner.action_points, self.owner))
            return Constants.TURN_COST


class SentinelMonster:
    def __init__(self, owner=None):
        self.given = False
        self.owner = owner
        self.active = False



    # AI for a basic monster.
    def take_turn(self):
            # a basic monster takes its turn. If you can see it, it can see you
            monster = self.owner
            player = GameState.get_player()

            if GameState.current_level.is_visible(obj=monster):
                if not self.active:
                    self.active = True
                    self.post_x = self.owner.x
                    self.post_y = self.owner.y
                GameState.continue_walking = False

            if self.active:
                # move towards player if far away
                dist = monster.distance_to(player)
                print self.owner.name + " | " + str(dist)
                if dist <= 1.5 and player.fighter.hp > 0:
                    monster.fighter.attack(player)
                if dist >= 6:
                    monster.move_astar_xy(self.post_x, self.post_y)
                else:
                    monster.move_astar(player)
            else:
                self.post_x = self.owner.x
                self.post_y = self.owner.y

            # self.owner.action_points += 100
            # Schedule.add_to_pq((self.owner.action_points, self.owner))
            return Constants.TURN_COST


class ScoutMonster:
    def __init__(self, owner=None):
        self.given = False
        self.owner = owner
        self.active = False

    # AI for a basic monster.
    def take_turn(self):
            # a basic monster takes its turn. If you can see it, it can see you
            monster = self.owner
            player = GameState.get_player()

            if GameState.current_level.is_visible(obj=monster):
                self.active = True
                GameState.continue_walking = False

            if self.active:
                # move towards player if far away
                dist = monster.distance_to(player)
                # print self.owner.name + " | " + str(dist)
                if dist <= 1.5 and player.fighter.hp > 0:
                    monster.fighter.attack(player)
                else:
                    monster.move_astar(player)

            # self.owner.action_points += 100
            # Schedule.add_to_pq((self.owner.action_points, self.owner))
            return Constants.TURN_COST


class RangedMonster:
    # AI for a basic monster.
    def __init__(self, attack_range=5, owner=None):
        self.owner = owner
        self.attack_range = attack_range
        self.reload = 0
        self.active = False

    def take_turn(self):
            # a basic monster takes its turn. If you can see it, it can see you
            monster = self.owner
            player = GameState.get_player()

            if GameState.current_level.is_visible(obj=monster):
                self.active = True
                GameState.continue_walking = False
                # move towards player if far away

            if self.active:
                dist = monster.distance_to(player)

                if dist > self.attack_range:
                    # monster.move_astar(player)
                    dest = Pathing.get_lowest_neighbor(monster.x, monster.y)
                    # print "{0} moves to {1}.".format(monster.name, dest)
                    monster.move_to(dest[0], dest[1])
                    self.reload -= 1
                # close enough, attack! (if the player is still alive.)
                elif player.fighter.hp > 0 and self.reload <= 0 and GameState.current_level.is_visible(obj=monster):
                    monster.fighter.attack(player)
                    self.play_animation('Shot', self.owner, player.x, player.y)
                    self.reload = 3
                else:
                    # Move away?
                    self.reload -= 1



            return Constants.TURN_COST

    def play_animation(self, animation_name, source, target_x, target_y):
        animation_params = {}
        animation_params['origin'] = (source.x, source.y)
        animation_params['target'] = (target_x, target_y)
        animation_params['target_angle'] = Utils.get_angle(source.x, source.y, target_x, target_y)

        GameState.add_animation(animation_name, animation_params)


class RangedTurretMonster:
    # AI for a basic monster.
    def __init__(self, attack_range=5, owner=None):
        self.owner = owner
        self.attack_range = attack_range
        self.reload = 0
        self.active = False

    def take_turn(self):
        # a basic monster takes its turn. If you can see it, it can see you
        monster = self.owner
        player = GameState.get_player()

        if GameState.current_level.is_visible(obj=monster):
            self.active = True
            GameState.continue_walking = False
            # move towards player if far away

        if self.active:

            dist = monster.distance_to(player)

            if dist > self.attack_range:
                # monster.move_astar(player)
                self.reload -= 1
            # close enough, attack! (if the player is still alive.)
            elif player.fighter.hp > 0 and self.reload <= 0 and GameState.current_level.is_visible(obj=monster):
                """ DISABLE """
                #Animate.follow_line(self.owner, player)

                self.play_animation('Shot', self.owner,  player.x, player.y )
                monster.fighter.attack(player)


                self.reload = 3
            else:
                # Move away?
                self.reload -= 1

        return Constants.TURN_COST

    def play_animation(self, animation_name, source, target_x, target_y):
        animation_params = {}
        animation_params['origin'] = (source.x, source.y)
        animation_params['target'] = (target_x, target_y)
        animation_params['target_angle'] = Utils.get_angle(source.x, source.y, target_x, target_y)

        GameState.add_animation(animation_name, animation_params)


class SpawningMonster:
    # AI for a basic monster.
    def __init__(self, new_monster, owner=None):
        self.new_monster = new_monster
        self.owner = owner

    def take_turn(self, fov):
        if self.owner.CT >= 100:
            self.owner.CT = 0
            # a basic monster takes its turn. If you can see it, it can see you
            monster = self.owner
            player = GameState.get_player()
            if GameState.current_level.is_visible(obj=monster):
                # TO-DO: Randomize location of spawn
                #       Randomize how often spawn occurs
                # move towards player if far away
                chance_to_spawn = libtcod.random_get_int(0, 0, 10)

                if chance_to_spawn >= 7:
                    # self.split()
                    pass
                else:
                    if monster.distance_to(player) >= 2:
                        monster.move_astar(player)
                    # close enough, attack! (if the player is 8still alive.)
                    elif player.fighter.hp > 0:
                        monster.fighter.attack(player)
            else:
                return False

    def split(self):
        loc = GameState.current_level.adjacent_open_tiles(self.owner)
        # spawn = Object(loc[0], loc[1], self.new_monster.char, self.new_monster.name, self.new_monster.color,
        # blocks=True, fighter=self.new_monster.fighter, ai=self.new_monster.ai)

        if loc != [None, None]:
            fighter_component = None
            ai_component = None
            if 'fighter_component' in GameState.imported_npc_list[self.new_monster]:
                fighter_component = Fighter(hp=int(GameState.imported_npc_list[self.new_monster]['hp']),
                                            defense=int(GameState.imported_npc_list[self.new_monster]['defense']),
                                            power=str(GameState.imported_npc_list[self.new_monster]['power']),
                                            xp=int(GameState.imported_npc_list[self.new_monster]['xp']),
                                            death_function=eval(
                                                GameState.imported_npc_list[self.new_monster]['death_function']))

            if 'ai_component' in GameState.imported_npc_list[self.new_monster]:
                ai_component = eval(GameState.imported_npc_list[self.new_monster]['ai_component'])

            monster = Entity.Entity(loc[0], loc[1], GameState.imported_npc_list[self.new_monster]['char'],
                                    GameState.imported_npc_list[self.new_monster]['name'],
                                    eval(GameState.imported_npc_list[self.new_monster]['color']),
                                    blocks=True,
                                    fighter=fighter_component,
                                    ai=ai_component)

            GameState.current_level.get_all_objects().append(monster)


class ConfusedMonster:
    # AI for a confused monster.
    def __init__(self, old_ai, num_turns=Constants.CONFUSE_NUM_TURNS, owner=None):
        self.old_ai = old_ai
        self.num_turns = num_turns
        self.owner = owner

    def take_turn(self):
        if self.owner.CT >= 100:
            self.owner.CT = 0
            if self.num_turns > 0:  # still confused...
                # move in a random direction, and decrease the number of turns confused
                self.owner.move(libtcod.random_get_int(0, -1, 1), libtcod.random_get_int(0, -1, 1))
                self.num_turns -= 1

            else:  # restore the previous AI (this one will be deleted because it's not referenced anymore)
                self.owner.ai = self.old_ai
                Utils.message('The ' + self.owner.name + ' is no longer confused!', libtcod.red)
            return False


class Item:
    def __init__(self, use_function=None, owner=None):
        self.use_function = use_function
        self.owner = owner

    # an item that can be picked up and used.
    def pick_up(self):
        # add to the player's inventory and remove from the map
        if len(GameState.inventory) >= 26:
            Utils.message('Your inventory is full, cannot pick up ' + self.owner.name + '.', libtcod.red)
        else:
            GameState.inventory.append(self.owner)
            GameState.current_level.get_all_objects().remove(self.owner)
            Utils.message('You picked up a ' + self.owner.name + '!', libtcod.green)
            # special case: automatically equip, if the corresponding equipment slot is unused
            equipment = self.owner.equipment
            if equipment and GameState.get_equipped_in_slot(equipment.slot) is None:
                equipment.equip()

    def use(self):
        if self.owner.equipment:
            self.owner.equipment.toggle_equip()
            return
        # just call the "use_function" if it is defined
        if self.use_function is None:
            Utils.message('The ' + self.owner.name + ' cannot be used.')
        else:
            if self.use_function() != 'cancelled':
                GameState.inventory.remove(self.owner)  # destroy after use, unless it was cancelled for some reason

    def drop(self):
        # add to the map and remove from the player's inventory. also, place it at the player's coordinates
        GameState.current_level.get_all_objects().append(self.owner)
        GameState.inventory.remove(self.owner)
        player = GameState.get_player()
        self.owner.x = player.x
        self.owner.y = player.y
        # special case: if the object has the Equipment component, dequip it before dropping
        if self.owner.equipment:
            self.owner.equipment.dequip()
            Utils.message('You dropped a ' + self.owner.name + '.', libtcod.yellow)


class Equipment:
    # an object that can be equipped, yielding bonuses. automatically adds the Item component.
    def __init__(self, slot, power_bonus=0, defense_bonus=0, max_hp_bonus=0, owner=None):
        self.power_bonus = power_bonus
        self.defense_bonus = defense_bonus
        self.max_hp_bonus = max_hp_bonus
        self.slot = slot
        self.is_equipped = False
        self.owner = owner

    def toggle_equip(self):  # toggle equip/dequip status
        if self.is_equipped:
            self.dequip()
        else:
            self.equip()

    def equip(self):
        # if the slot is already being used, dequip whatever is there first
        old_equipment = GameState.get_equipped_in_slot(self.slot)
        if old_equipment is not None:
            old_equipment.dequip()

        # equip object and show a message about it
        self.is_equipped = True
        Utils.message('Equipped ' + self.owner.name + ' on ' + self.slot + '.', libtcod.light_green)

    def dequip(self):
        # dequip object and show a message about it
        if not self.is_equipped: return
        self.is_equipped = False
        Utils.message('Dequipped ' + self.owner.name + ' from ' + self.slot + '.', libtcod.light_yellow)


class Ranged:
    def __init__(self, max_range, ammo_type=0, ammo_consumed=0, aoe=1, animation=None, animation_params={'none': None}, owner=None):
        self.max_range = max_range
        self.ammo_type = ammo_type
        self.ammo_consumed = ammo_consumed
        self.owner = owner
        self.aoe = aoe
        self.animation = animation
        self.animation_params = animation_params

    def fire(self, source=None, target=None):

        targets = []
        target_x = 0
        target_y = 0

        if source is None:
            source = GameState.get_player()
        if target is None:
            tile_effected = None
            Utils.message('Choose Target. Left Click/Space to execute. Right Click/ESC to cancel.', libtcod.gold)

            ''' Get list of visible enemies to cycle through '''
            target_list = GameState.current_level.closest_monsters(self.max_range)
            if target_list:
                target_list = cycle(target_list)
                target = next(target_list)[0]

            ''' Used to detect mouse movement '''
            mouse = Input.mouse
            mouse_last_x, mouse_last_y = mouse.cx, mouse.cy
            mouse_moved = False

            while True:
                ''' Clear Screen '''
                Render.clear_layer(5)


                ''' Get Inputs '''
                Input.update()
                key = Input.key

                ''' determine if mouse moved, otherwise use auto-target '''
                if mouse.cx != mouse_last_x or mouse.cy != mouse_last_y:
                    mouse_moved = True
                    moues_last_x, mouse_last_y = mouse.cx, mouse.cy
                if mouse_moved:
                    target_x, target_y = Utils.to_map_coordinates(mouse.cx, mouse.cy)
                elif target:
                    target_x, target_y = target.x, target.y
                else:
                    target_x, target_y = source.x, source.y

                ''' determine line of fire (You may not be able to hit every enemy you see) '''
                line = Utils.get_line((source.x, source.y),
                                      (target_x, target_y),
                                      walkable=True,
                                      ignore_mobs=True,
                                      max_length=self.max_range)
                for point in line:
                    if point == (None, None):
                        break
                    point = Utils.to_camera_coordinates(point[0], point[1])
                    libtcod.console_set_char_background(0, point[0], point[1], libtcod.lighter_blue, libtcod.BKGND_SET)
                    Render.draw_char(5, point[0], point[1], 0x2588, terminal.color_from_argb(128, 64, 64, 255),
                                     libtcod.BKGND_SET)



                if len(line) > 0:
                    index = Utils.find_element_in_list((None, None), line)

                    if index is None:
                        point = line[-1]
                    else:
                        point = line[index-1]

                    circle = Utils.get_circle_points(point[0], point[1], self.aoe)
                    if circle:
                        tile_effected = set(circle)

                        for points in circle:
                            points = Utils.to_camera_coordinates(points[0], points[1])
                            Render.draw_char(5, points[0], points[1], 0x2588, terminal.color_from_argb(128, 200, 32, 32),
                                             libtcod.BKGND_SET)
                            Render.draw_char(5, points[0], points[1], 0xE000, terminal.color_from_argb(128, 255, 0, 0),
                                             libtcod.BKGND_SET)

                if mouse.lbutton_pressed or key == terminal.TK_SPACE:
                    # target_tile = (target_x, target_y)
                    #print tile_effected
                    for target in tile_effected:
                        #target = Map.to_map_coordinates(target[0], target[1])
                        monster = GameState.current_level.get_monster_at((target[0], target[1]))
                        if monster is not None:
                            print "Monster: " + str(monster) + " at " + str(target)
                            targets.append(monster)
                    break


                if mouse.rbutton_pressed or key == terminal.TK_ESCAPE:
                    break

                if key == terminal.TK_F:
                    if target_list:
                        target = next(target_list)[0]

                GameState.render_ui()



            if not targets:  # no enemy found within maximum range
                Utils.message('Cancelled.', libtcod.red)
                Render.clear_layer(5)
                return 'cancelled'


        # TODO: add animation back in when appropriate, Fix Target
        #Animate.follow_line(source, target_tile)
        # Animate.explosion(target)

        # zap it!
        if self.animation:
            self.animation_params['origin'] = (source.x, source.y)
            self.animation_params['target'] = (target_x, target_y)
            self.animation_params['target_angle'] = Utils.get_angle(source.x, source.y, target_x, target_y)

            GameState.add_animation(self.animation, self.animation_params)

        for target in targets:
            if target.fighter:
                Utils.message('{0} takes {1} damage.'.format(target.name, self.owner.equipment.power_bonus),
                              libtcod.light_blue)
                target.fighter.take_damage(self.owner.equipment.power_bonus)
        Render.clear_layer(5)
        return 'fired'


def player_death(player):
    Utils.message('Dead dead deadski!', libtcod.dark_red)

    # for added effect, transform the player into a corpse!
    player.char = '%'
    player.color = libtcod.dark_red


def monster_death(monster):
    # transform it into a nasty corpse! it doesn't block, can't be
    # attacked and doesn't move
    Utils.message('The ' + monster.name + ' is dead! You gain ' + str(monster.fighter.xp) + ' experience points.',
                  libtcod.orange)
    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of ' + monster.name
    Schedule.release(monster)
    # Schedule.pq

    monster.send_to_back()


class Door:
    def __init__(self, door_status=None, owner=None):
        self.owner = owner
        if door_status is None:
            chance = libtcod.random_get_int(0, 0, 1000)
            if chance <= 5:
                self.status = 'locked'
            else:
                self.status = 'closed'
        else:
            self.status = door_status

    def take_turn(self):
        if self.status is 'closed':
            self.owner.blocks = True
            self.owner.blocks_sight = True
            self.owner.char = '+'
        elif self.status is 'open':
            self.owner.blocks = False
            self.owner.blocks_sight = False
            self.owner.char = '_'
        elif self.status is 'locked':
            self.owner.blocks = True
            self.owner.blocks_sight = True
            self.owner.name = 'locked door'
        return 0

    def interact(self):
        # print "interact!"
        if self.status == 'closed':
            self.status = 'open'
        if self.status == 'open':
            pass
        else:
            Utils.message("Locked!", libtcod.dark_red)
        self.take_turn()
