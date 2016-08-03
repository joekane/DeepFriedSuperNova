import Constants
import GameState
import libtcodpy as libtcod
import Utils
import Map
import Components

""" SPELLS """


def cast_heal():
    # heal the player
    player = GameState.get_player()
    if player.fighter.hp == player.fighter.max_hp:
        GameState.add_msg('You are already at full health.', libtcod.red)
        return 'cancelled'

    GameState.add_msg('Your wounds start to feel better!', libtcod.light_violet)
    player.fighter.heal(Constants.HEAL_AMOUNT)


def cast_lightning():
    # find closest enemy (inside a maximum range) and damage it
    monster = Map.closest_monster(Constants.LIGHTNING_RANGE)
    if monster is None:  # no enemy found within maximum range
        GameState.add_msg('No enemy is close enough to strike.', libtcod.red)
        return 'cancelled'

    # zap it!
    GameState.add_msg('A lighting bolt strikes the ' + monster.name + ' with a loud thunder! The damage is ' +
                      str(Constants.LIGHTNING_DAMAGE) + ' hit points.', libtcod.light_blue)
    monster.fighter.take_damage(Constants.LIGHTNING_DAMAGE)


def cast_confuse():
    # ask the player for a target to confuse
    GameState.add_msg('Left-click an enemy to confuse it, or right-click to cancel.', libtcod.light_cyan)
    monster = target_monster(Constants.CONFUSE_RANGE)
    if monster is None: return 'cancelled'

    # replace the monster's AI with a "confused" one; after some turns it will restore the old AI
    old_ai = monster.ai
    monster.ai = Components.ConfusedMonster(old_ai)
    monster.ai.owner = monster  # tell the new component who owns it
    GameState.add_msg('The eyes of the ' + monster.name + ' look vacant, as he starts to stumble around!',
                      libtcod.light_green)


def cast_fireball():
    # ask the player for a target tile to throw a fireball at
    GameState.add_msg('Left-click a target tile for the fireball, or right-click to cancel.', libtcod.light_cyan)
    (x, y) = Map.target_tile()
    if x is None: return 'cancelled'
    GameState.add_msg('The fireball explodes, burning everything within ' + str(Constants.FIREBALL_RADIUS) + ' tiles!',
                      libtcod.orange)

    for obj in Map.get_objects():  # damage every fighter in range, including the player
        if obj.distance(x, y) <= Constants.FIREBALL_RADIUS and obj.fighter:
            GameState.add_msg('The ' + obj.name + ' gets burned for ' + str(Constants.FIREBALL_DAMAGE) + ' hit points.',
                              libtcod.orange)
            obj.fighter.take_damage(Constants.FIREBALL_DAMAGE)

