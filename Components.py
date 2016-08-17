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

import libtcodpy as libtcod
import Combat
import Constants
import Entity
import GameState
import Map
import Fov
import Utils
import Animate
import Render
import Schedule


class PlayeControlled:
    def __init__(self, owner=None):
        self.owner = owner


    def end_turn(self, cost):
        # self.owner.action_points += 100
        # Schedule.add_to_pq((self.owner.action_points, self.owner))
        return cost

    def process_mouse_clicks(self, mouse):

        # (x, y) = Map.to_camera_coordinates(mouse.cx, mouse.cy)
        (map_x, map_y) = Map.to_map_coordinates(mouse.cx, mouse.cy)

        # walk to target tile
        if mouse.lbutton_pressed and Map.is_explored(map_x, map_y):
            GameState.continue_walking = GameState.get_player().move_astar_xy(map_x, map_y, True)
            return self.end_turn(Constants.TURN_COST)
        if mouse.rbutton_pressed:
            # print "Mouse Pressed!"
            x, y = Map.to_map_coordinates(mouse.cx, mouse.cy)
            GameState.get_player().x = x
            GameState.get_player().y = y
            Fov.require_recompute()
            return 0

    def process_mouse_hover(self, mouse):
        (map_x, map_y) = Map.to_map_coordinates(mouse.cx, mouse.cy)

        if self.owner.x != map_x or self.owner.y != map_y:
            # libtcod.console_set_char_background(0, mouse.cx, mouse.cy, libtcod.Color(10, 10, 240), libtcod.BKGND_SET)
            Utils.inspect_tile(mouse.cx, mouse.cy)



    # AI for a basic monster.
    def take_turn(self):
        if GameState.continue_walking:
            self.owner.walk_path()
            return self.end_turn(Constants.TURN_COST)
        elif not GameState.continue_walking:
            GameState.get_player().clear_path()
        while True:
            # print "looping"
            key = libtcod.Key()
            mouse = libtcod.Mouse()

            libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

            (x, y) = (mouse.cx, mouse.cy)

            player = GameState.get_player()

            if key.vk == libtcod.KEY_ENTER and key.lalt:
                # Alt+Enter: toggle fullscreen
                libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

            elif key.vk == libtcod.KEY_ESCAPE:
                return 0  # exit game

            if self.process_mouse_clicks(mouse):
                return 0

            if self.process_mouse_hover(mouse):
                return 0

            # movement keys
            if True:
                # movement keys
                # movement keys
                if key.vk == libtcod.KEY_UP or key.vk == libtcod.KEY_KP8:
                    Map.player_move_or_interact(0, -1)
                    return self.end_turn(Constants.TURN_COST)
                elif key.vk == libtcod.KEY_DOWN or key.vk == libtcod.KEY_KP2:
                    Map.player_move_or_interact(0, 1)
                    return self.end_turn(Constants.TURN_COST)
                elif key.vk == libtcod.KEY_LEFT or key.vk == libtcod.KEY_KP4:
                    Map.player_move_or_interact(-1, 0)
                    return self.end_turn(Constants.TURN_COST)
                elif key.vk == libtcod.KEY_RIGHT or key.vk == libtcod.KEY_KP6:
                    Map.player_move_or_interact(1, 0)
                    return self.end_turn(Constants.TURN_COST)
                elif key.vk == libtcod.KEY_HOME or key.vk == libtcod.KEY_KP7:
                    Map.player_move_or_interact(-1, -1)
                    return self.end_turn(Constants.TURN_COST)
                elif key.vk == libtcod.KEY_PAGEUP or key.vk == libtcod.KEY_KP9:
                    Map.player_move_or_interact(1, -1)
                    return self.end_turn(Constants.TURN_COST)
                elif key.vk == libtcod.KEY_END or key.vk == libtcod.KEY_KP1:
                    Map.player_move_or_interact(-1, 1)
                    return self.end_turn(Constants.TURN_COST)
                elif key.vk == libtcod.KEY_PAGEDOWN or key.vk == libtcod.KEY_KP3:
                    Map.player_move_or_interact(1, 1)
                    return self.end_turn(Constants.TURN_COST)
                elif key.vk == libtcod.KEY_KP5:
                    pass  # do nothing ie wait for the monster to come to you
                else:
                    # test for other keys
                    key_char = chr(key.c)

                    if key_char == 'g':
                        # pick up an item
                        for object in Map.get_all_objects():  # look for an item in the player's tile
                            if object.x == player.x and object.y == player.y and object.item:
                                object.item.pick_up()
                                break
                    elif key_char == 'i':
                        # show the inventory; if an item is selected, use it
                        # img = libtcod.image_load('orc.png')
                        # libtcod.image_blit_2x(img, 0, 0, 0)

                        # img2 = libtcod.image_load('orc_80.png')
                        # libtcod.image_blit_2x(img2, 0, 40, 0)

                        chosen_item = inventory_menu(
                            'Press the key next to an item to use it, or any other to cancel.\n')

                        if chosen_item is not None:
                            chosen_item.use()
                            return 0
                    elif key_char == 'd':
                        # show the inventory; if an item is selected, drop it
                        chosen_item = inventory_menu(
                            'Press the key next to an item to drop it, or any other to cancel.\n')

                        if chosen_item is not None:
                            chosen_item.drop()
                    elif key_char == 'f':
                        for obj in GameState.get_all_equipped(player):
                            if obj.owner.ranged:
                                obj.owner.ranged.fire()
                                Constants.TURN_COST
                        Utils.message("No ranged weapon equipped!", libtcod.light_amber)
                    elif key_char == 'h':
                        for obj in GameState.get_inventory():
                            if obj.name == 'healing potion':
                                obj.item.use()
                                return 0
                        return Utils.message("No helaing potions.", libtcod.light_amber)
                    elif key_char == '<':
                        # go down stairs, if the player is on them
                        stairs = Map.get_stairs()
                        if stairs.x == player.x and stairs.y == player.y:
                            GameState.next_level()
                    elif key_char == 'c':
                        # show character information
                        player = GameState.get_player()
                        level_up_xp = Constants.LEVEL_UP_BASE + player.level * Constants.LEVEL_UP_FACTOR

                        text = 'Character Information\n\nLevel: ' + str(player.level) + '\nExperience: ' + str(
                            player.fighter.xp) + \
                               '\nExperience to level up: ' + str(level_up_xp) + '\n\nMaximum HP: ' + str(
                            player.fighter.max_hp) + \
                               '\nAttack: ' + str(player.fighter.power) + '\nDefense: ' + str(player.fighter.defense)
                        Render.pop_up(width=40, title='Inventory Screen', text=text)

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

                        Render.pop_up(title=title, text=text)
                    elif key_char == 'b':

                        title = "Beastiary"

                        text = 'Cipher Warden\n\n\nHP = 50\nDEF = 10\nDODGE = 5%'

                        Render.beastiary(width=50, height=45, title=title, text=text)
                    elif key_char == 'x':
                        Fov.require_recompute()
                        Constants.DEBUG = not Constants.DEBUG



                    # return 0
                # print "took turn"
                # return Constants.TURN_COST
                # print "rendering"
                # Render.render_all()

                Render.update()
                #libtcod.console_flush()


class Fighter:
    # combat-related properties and methods (monster, player, NPC).
    def __init__(self, hp, defense, power, xp, death_function=None, owner=None):
        self.xp = xp
        self.death_function = death_function
        self.base_max_hp = hp
        self.hp = hp
        self.base_defense = defense
        self.base_power = power
        self.owner = owner

    @property
    def damage(self):
        return Combat.dice('1d4')

    @property
    def save(self):
        dodge_chance = 5
        return Combat.dice('1d100') <= dodge_chance
        # determine best save and attempt it

    @property
    def damage_reduction(self):
        return Combat.dice('1d1')

    @property
    def power(self):
        bonus = sum(equipment.power_bonus for equipment in GameState.get_all_equipped(self.owner))
        return self.base_power + bonus

    @property
    def defense(self):  # return actual defense, by summing up the bonuses from all equipped items
        bonus = sum(equipment.defense_bonus for equipment in GameState.get_all_equipped(self.owner))

        if self.owner is GameState.get_player():
            bonus -= max(0, (Map.number_of_adjacent_objects(GameState.get_player()) - 2))
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
            Map.spawn_item_at(self.owner.x, self.owner.y + 1, 'GrisKeyRing')

    def reward(self):
        if (not self.given):
            Utils.message("That was easy, wasn't it!")
            Map.spawn_item_at(self.owner.x, self.owner.y+1, 'QuestSword')
            self.given = True
        else:
            Utils.message("greedy bastard.")


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

            if Fov.is_visible(obj=monster):
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




class AssassinMonster:
    def __init__(self, owner=None):
        self.given = False
        self.owner = owner
        self.active = True

    # AI for a basic monster.
    def take_turn(self):
            # a basic monster takes its turn. If you can see it, it can see you
            monster = self.owner
            player = GameState.get_player()
            dist = monster.distance_to(player)


            if Fov.is_visible(obj=monster):
                self.active = True
                GameState.continue_walking = False
            else:
                if dist > 25:
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

            if Fov.is_visible(obj=monster):
                self.active = True
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

            if Fov.is_visible(obj=monster):
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

            if Fov.is_visible(obj=monster):
                self.active = True
                GameState.continue_walking = False
                # move towards player if far away

            if self.active:

                dist = monster.distance_to(player)

                if dist > self.attack_range:
                    monster.move_astar(player)
                    self.reload -= 1
                # close enough, attack! (if the player is still alive.)
                elif player.fighter.hp > 0 and self.reload <= 0:
                    Animate.follow_line(self.owner, player)
                    monster.fighter.attack(player)
                    self.reload = 3
                else:
                    # Move away?
                    self.reload -= 1

            return Constants.TURN_COST


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

        if Fov.is_visible(obj=monster):
            self.active = True
            GameState.continue_walking = False
            # move towards player if far away

        if self.active:

            dist = monster.distance_to(player)

            if dist > self.attack_range:
                # monster.move_astar(player)
                self.reload -= 1
            # close enough, attack! (if the player is still alive.)
            elif player.fighter.hp > 0 and self.reload <= 0:
                Animate.follow_line(self.owner, player)
                monster.fighter.attack(player)
                self.reload = 3
            else:
                # Move away?
                self.reload -= 1

        return Constants.TURN_COST


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
            if Fov.is_visible(obj=monster):
                # TO-DO: Randomize location of spawn
                #       Randomize how often spawn occurs
                # move towards player if far away
                chance_to_spawn = libtcod.random_get_int(0, 0, 10)

                if chance_to_spawn >= 7:
                    self.split()
                else:
                    if monster.distance_to(player) >= 2:
                        monster.move_astar(player)
                    # close enough, attack! (if the player is 8still alive.)
                    elif player.fighter.hp > 0:
                        monster.fighter.attack(player)
            else:
                return False

    def split(self):
        loc = Map.adjacent_open_tiles(self.owner)
        # spawn = Object(loc[0], loc[1], self.new_monster.char, self.new_monster.name, self.new_monster.color,
        # blocks=True, fighter=self.new_monster.fighter, ai=self.new_monster.ai)

        if loc != [None, None]:
            fighter_component = None
            ai_component = None
            if 'fighter_component' in GameState.imported_npc_list[self.new_monster]:
                fighter_component = Fighter(hp=int(GameState.imported_npc_list[self.new_monster]['hp']),
                                            defense=int(GameState.imported_npc_list[self.new_monster]['defense']),
                                            power=int(GameState.imported_npc_list[self.new_monster]['power']),
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

            Map.get_all_objects().append(monster)


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
            Map.get_all_objects().remove(self.owner)
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
                inventory.remove(self.owner)  # destroy after use, unless it was cancelled for some reason

    def drop(self):
        # add to the map and remove from the player's inventory. also, place it at the player's coordinates
        Map.get_all_objects().append(self.owner)
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
    def __init__(self, max_range, ammo_type=0, ammo_consumed=0, owner=None):
        self.max_range = max_range
        self.ammo_type = ammo_type
        self.ammo_consumed = ammo_consumed
        self.owner = owner

    def fire(self, source=None, target=None):
        # find closest enemy (inside a maximum range) and damage it
        if source is None:
            source = GameState.get_player()
        if target is None:
            target = Map.closest_monster(self.max_range)
            if target is None:  # no enemy found within maximum range
                Utils.message('No enemy is close enough to fire.', libtcod.red)
                return 'cancelled'

        Animate.follow_line(source, target)
        # Animate.explosion(target)

        # zap it!
        Utils.message('A shot rings out and ' + target.name + ' takes an arrow to the knee! The damage is ' + str(
            self.owner.equipment.power_bonus) + ' hit points.', libtcod.light_blue)
        target.fighter.take_damage(self.owner.equipment.power_bonus)


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
    Schedule.pq

    monster.send_to_back()


class Door:
    def __init__(self, door_status=None, owner=None):
        self.owner = owner
        if door_status is None:
            chance = libtcod.random_get_int(0, 0, 100)
            if chance <= 2:
                self.status = 'locked'
            else:
                self.status = 'closed'
        else:
            self.status = door_status

    def take_turn(self):
        self.owner.CT = 100
        if self.status is 'closed':
            self.owner.blocks = True
            self.owner.blocks_sight = True
            # Fov.fov_change(self.owner.x, self.owner.y, True, True)
            # Map.level_map[self.owner.x][self.owner.y].blocked = True
            # Map.level_map[self.owner.x][self.owner.y].block_sight = True
            self.owner.char = '+'
        if self.status is 'open':
            self.owner.blocks = False
            self.owner.blocks_sight = False
            # Fov.fov_change(self.owner.x, self.owner.y, False, False)
            # Map.level_map[self.owner.x][self.owner.y].blocked = False
            # Map.level_map[self.owner.x][self.owner.y].block_sight = False

            self.owner.char = '_'
        if self.status is 'locked':
            self.owner.blocks = True
            self.owner.blocks_sight = True
            self.owner.name = 'locked door'
        return False

    def interact(self):
        # print "interact!"
        if self.status == 'closed':
            self.status = 'open'
        if self.status == 'open':
            pass
        else:
            Utils.message("Locked!", libtcod.dark_red)
