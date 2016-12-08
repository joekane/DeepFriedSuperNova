import libtcodpy as libtcod
import copy

status_list = {
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

# TODO: Expand sysetm to Allow NULLIFY other Status, REFRESH other Status, or ADD_TO other Status.
""" Example: Wet should add wetness to a mob the more its in water. hitting a puddle aand spending 10 turns in a lake are not the same WET."""
""" Example: On_Fire should just reset the On_Fire Timer, you arent MORE on fire, just on fire longer."""
""" Example: Getting Wet while on Fire should reduce if not emilinate the On_Fire Status"""


def new_status(status):
    return copy.deepcopy(status_list[status])


