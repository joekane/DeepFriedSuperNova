import libtcodpy as libtcod
from enum import Enum


class Effect:
    def __init__(self, type, value, stat=None, dmgtype=None):
        self.type = type
        self.value = value
        self.stat = stat
        self.dmgtype = dmgtype


status_list_OLD = {
    'Rage': {
        'name': 'Rage',
        'color': libtcod.red,
        'damage_bonus' : 5,
        'duration': 100,
    },
    'Blessed': {
        'name': 'Blessed',
        'color': libtcod.yellow,
        'damage_reduction' : '1d5',
        'duration': 100,
    },
    'Poisoned': {
        'name': 'Poisoned',
        'color': libtcod.green,
        'duration': 25,
        'HP': -1
    },
    'Regen': {
        'name': 'Regen',
        'color': libtcod.light_green,
        'duration': 25,
        'HP': 1
    },
    'Haste': {
        'name': 'Haste',
        'color': libtcod.orange,
        'duration': 100,
        'speed': 10
    },
    'Slow': {
        'name': 'Slow',
        'color': libtcod.lighter_blue,
        'duration': 100,
        'speed': -5
    },
}

EffectType = Enum('EffectType', "StatBonus DmgBonus HealOT DmgOT None")


status_db = {
    'Wet': {
        'effect_name': "Wet",
        'effect_tags': ['Wet'],
        'effect_text': "{0} is soaked.",
        'effect': Effect(EffectType.DmgBonus, 10, dmgtype='Elec'),
        'start_duration': 1000,
        'immune_to': ['Fire'],
        'cancels': ['Fire'],
        'stack_type': 'Stack'},
    'On_fire': {
        'effect_name': "On Fire",
        'effect_tags': ['Fire'],
        'effect_text': "{0} is on fire!.",
        'effect': Effect(EffectType.DmgOT, 10, dmgtype='Fire'),
        'start_duration': 1000,
        'immune_to': [],
        'cancels': [],
        'stack_type': 'Reset'},
    'Regen': {
        'effect_name': "Regen",
        'effect_tags': ['Heal'],
        'effect_text': "{0} is regenerating.",
        'effect': Effect(EffectType.HealOT, 5, dmgtype='Heal'),
        'start_duration': 1000,
        'immune_to': [],
        'cancels': [],
        'stack_type': 'Reset'},
    'Poison': {
        'effect_name': "Poison",
        'effect_tags': ['Poison'],
        'effect_text': "{0} is poisoned.",
        'effect': Effect(EffectType.DmgOT, 5, dmgtype='Poison'),
        'start_duration': 1000,
        'immune_to': ['Heal'],
        'cancels': ['Heal'],
        'stack_type': 'Reset'},
    'Antidote': {
        'effect_name': "Antidote",
        'effect_tags': ['Antidote'],
        'effect_text': "{0} is cleansed.",
        'effect': Effect(None, None),
        'start_duration': 0,
        'immune_to': [],
        'cancels': ['Poison'],
        'stack_type': 'Reset'},
    'Rage': {
        'effect_name': "Rage",
        'effect_tags': ['Rage'],
        'effect_text': "{0} is enraged!.",
        'effect': Effect(EffectType.StatBonus, 10, stat='STR'),
        'start_duration': 0,
        'immune_to': [],
        'cancels': ['Poison'],
        'stack_type': 'Reset'}
    }



class StatusList:
    def __init__(self):
        self.status_list = []


    # TODO: Simplify?

    def add_status(self, status_name):
        # Check if immune to new status
        for s in self.status_list:
            if status_name in status_db[s.name]['immune_to']:
                return

        # add status
        self.status_list.append(Status(status_name))

        # cancel any eddects new status cancesls.
        for cancel in status_db[status_name]['cancels']:
            for s in self.status_list:
                for t in status_db[s.name]['effect_tags']:
                    if cancel == t:
                        self.status_list.remove(s)

    def get_bonus(self, stat_name, base_value):
        bonus = 0
        for s in self.status_list:
            if status_db[s.name]['effect'].stat == stat_name:
                bonus += status_db[s.name]['effect'].value
        return bonus

    def pass_time(self, time_units):
        to_remove = []
        for s in self.status_list:
            result = s.pass_time(time_units)
            if result[0] <= 0:
                to_remove.append(s)
        for rem in to_remove:
            self.status_list.remove(rem)

    def summary(self):
        summary = []
        for s in self.status_list:
            summary.append((s.name, s.duration))
        return summary


class Status:
    def __init__(self, status_name):
        self.name = str(status_db[status_name]['effect_name'])
        self.duration = status_db[status_name]['start_duration']

    def pass_time(self, time_units):
        self.duration -= time_units
        plus_hp = 0
        minus_hp = 0

        if status_db[self.name]['effect'].type == EffectType.HealOT:
            plus_hp = status_db[self.name]['effect'].value
        if status_db[self.name]['effect'].type == EffectType.DmgOT:
            minus_hp = status_db[self.name]['effect'].value
        return self.duration, plus_hp, minus_hp

    def get_bonus(self, stat_name):
        if status_db[self.name]['effect'].type == EffectType.StatBonus:
            if stat_name in status_db[self.name]['effect'].stat:
                return status_db[self.name]['effect'].value




# TODO: Expand sysetm to Allow NULLIFY other Status, REFRESH other Status, or ADD_TO other Status.
""" Example: Wet should add wetness to a mob the more its in water. hitting a puddle aand spending 10 turns in a lake are not the same WET."""
""" Example: On_Fire should just reset the On_Fire Timer, you arent MORE on fire, just on fire longer."""
""" Example: Getting Wet while on Fire should reduce if not emilinate the On_Fire Status"""



