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

import random


def dice(s):
    print "Die String: {0}".format(s)
    num, temp = s.split('d')
    # print "First Split: {0}, {1}".format(num, temp)
    if num == '': num = 1
    die, bonus = temp, 0
    if "+" in temp:

        die, bonus = temp.split('+')
        # print "Die, Bonus: {0}, {1}".format(die, bonus)
    elif "-" in temp:
        die, bonus = temp.split('-')
        bonus = -int(bonus)
    return sum([random.randint(1,int(die)) for a in range(int(num))])+int(bonus)


# TODO: Move all Damage incoming / outgoing to this class. Make classes recive messages from here. Only classes that acctually NEED the info should be contacted
# TODO: Perhaps targeting should be there as well............most targety things will be combat related.
# TODO: Combat should always use PROPERTY based stats. Therefore all manipulation of stats is done inside each enitity.

def damage_calc(attacker, target):
    if target.fighter.save:
        return False
    else:
        dmg = attacker.damage - target.fighter.damage_reduction
        return dmg


# TESTING
class Stat:
    def __init__(self, base_max, base_threshold, base_regen, base_bonus_max):
        self.base_max = base_max
        self.current_value = base_max
        self.current_bonus = 0
        self. base_threshold = base_threshold
        self.base_regen = base_regen
        self.base_bonus_max = base_bonus_max

    @property
    def value(self):
        result = self.current_value + self.current_bonus
        max = self.base_bonus_max * self.base_max
        return min(result, max)



