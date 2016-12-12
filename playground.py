from bearlibterminal import terminal
import Engine.Animation_System
import Utils
import Engine.Input
import random
import Render
# test_anim = Engine.Animation_System.Cell(['a', 'b', 'c'], [libtcod.red, libtcod.green], 50)
# test_anim = Engine.Animation_System.Cell(['a', 'b'], Utils.heat_map_colors, 5)
#vect = Engine.Animation_System.Line(5, 5, 25, 40, loop=False)
#vect_test = Engine.Animation_System.Cell(5, 5, ['X'], [libtcod.red, libtcod.green], delay=1, vector=Engine.Animation_System.Line(5, 5, 25, 40, loop=False))

x, y = 50, 25

animations = []


def play():

    while True:
        # Engine.Input.clear()
        Engine.Input.update()
        key = Engine.Input.key
        terminal.clear()
        terminal.color('white')
        # terminal.print_(terminal.state(terminal.TK_MOUSE_X), terminal.state(terminal.TK_MOUSE_Y),"HellowWorld")
        #test_anim.draw(terminal.state(terminal.TK_MOUSE_X),terminal.state(terminal.TK_MOUSE_Y))

        if key == terminal.TK_MOUSE_LEFT:
            x, y = terminal.state(terminal.TK_MOUSE_X), terminal.state(terminal.TK_MOUSE_Y)
            # animations.append(create_anim(x,y, Utils.heat_map_chrs, Utils.explosion_colors, number=50))
            #animations.append(Engine.Animation_System.Flame(x, y, size=25, density=70))
            choice = random.randint(0,5)

            # Engine.Animation_System.(Engine.Animation_System.A_FLAME, **kwargs)

            #choice = 0
            print choice

            # TODO: Cleaup Call. ADD KWARG support, Accept POS(x, y) instead of x,y. make all default variables overrideable via Kwargs

            animation_params={
                'origin': (x, y),
                'target': (x, y)
            }

            if choice == 0:
                    animations.append(
                            Engine.Animation_System.Animation('Flame', animation_params))   # , angle=random.randint(270, 270)))
            if choice == 1:
                    animations.append(
                            Engine.Animation_System.Animation('Burst', animation_params))
            if choice == 4:
                    animations.append(
                            Engine.Animation_System.Animation('Line', animation_params))
            if choice == 2:
                    animations.append(
                            Engine.Animation_System.Animation('IceBreath', animation_params))
            if choice == 3:
                    animations.append(
                            Engine.Animation_System.Animation('TinyFire', animation_params))
            if choice == 5:
                    animations.append(
                            Engine.Animation_System.Animation('Xmas', animation_params))

            #print len(animations)

        Render.draw_char(0, 15,15, '@')
        terminal.color('han')
        Render.draw_char(0, 17, 15, 'T')

        for ani in animations:
            result = ani.play()
            if result == 'Done':
                print "Want?"
                animations.remove(ani)

        #print len(animations)

        terminal.refresh()
