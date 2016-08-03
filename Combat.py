import random


def dice(s):
    num, temp = s.split('d')
    if num == '': num = 1
    die,bonus = temp,0
    if "+" in temp:
        die, bonus = temp.split('+')
    elif "-" in temp:
        die, bonus = temp.split('-')
        bonus = -int(bonus)
    return sum([random.randint(1,int(die)) for a in range(int(num))])+int(bonus)


def damage_calc(attacker, target):
    if target.fighter.save:
        return False
    else:
        return attacker.damage - target.fighter.damage_reduction
