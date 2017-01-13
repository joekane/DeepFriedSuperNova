# coding=utf8
import PyBearLibTerminal as terminal
from itertools import cycle
import line



lorem_ipsum = \
    "[c=orange]Lorem[/c] ipsum dolor sit amet, consectetur adipisicing elit, " \
    "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. " \
    "[c=orange]Ut[/c] enim ad minim veniam, quis nostrud exercitation ullamco " \
    "laboris nisi ut aliquip ex ea commodo consequat. [c=orange]Duis[/c] aute " \
    "irure dolor in reprehenderit in voluptate velit esse cillum dolore eu " \
    "fugiat nulla pariatur. [c=orange]Excepteur[/c] sint occaecat cupidatat " \
    "non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."



class bltColor(str):
    def __init__(self, color):
        #long.__init__(self, terminal.color_from_name(color))
        self.colorname = color
        self.color = terminal.color_from_name(color)

    def __str__(self):
        """ Returns object as str for use in formatting tags """
        return str(self.colorname)

    def __add__(self, color2):
        r1, g1, b1, a1 = self.getRGB()
        r2, g2, b2, a2 = color2.getRGB()

        return bltColor(str(terminal.color_from_argb(
            a1,
            min(r1 + r2, 255),
            min(g1 + g2, 255),
            min(b1 + b2, 255),
        )))

    def __sub__(self, color2):
        r1, g1, b1, a1 = self.getRGB()
        r2, g2, b2, a2 = color2.getRGB()

        return bltColor(str(terminal.color_from_argb(
            a1,
            max(r1 - r2, 0),
            max(g1 - g2, 0),
            max(b1 - b2, 0),
        )))

    def __mul__(self, color2):
        if isinstance(color2, bltColor):
            r1, g1, b1, a1 = self.getRGB()
            r2, g2, b2, a2 = color2.getRGB()
            return bltColor(str(terminal.color_from_argb(
                a1,
                max(min(int(r1 * r2) // 255, 255), 0),
                max(min(int(g1 * g2) // 255, 255), 0),
                max(min(int(b1 * b2) // 255, 255), 0),
            )))
        else:
            r1, g1, b1, a1 = self.getRGB()
            r2, g2, b2, a2 = color2, color2, color2, 1.0
            return bltColor(str(terminal.color_from_argb(
                a1,
                max(min(int(r1 * r2), 255), 0),
                max(min(int(g1 * g2), 255), 0),
                max(min(int(b1 * b2), 255), 0),
            )))

    __rmul__ = __mul__

    @staticmethod
    def color_map(color_list, keylist):
        # TODO: List shoudl be tuple ( str , inex )
        total_len = keylist[-1]

        current_key = 0
        color_map = []
        for i, key in enumerate(keylist):
            color_map.append(bltColor(color_list[i]))
            try:
                interp_num = keylist[current_key+1] - keylist[current_key] - 1
                bias_inc = 1.0 / (interp_num + 2)
                print "Bias_iv: {0}".format(bias_inc)
                bias = bias_inc
                for i in xrange(interp_num):
                    colorA = bltColor(color_list[current_key]).getRGB()
                    colorB = bltColor(color_list[current_key+1]).getRGB()

                    a = max(min(int(colorA[3] + ((colorB[3] - colorA[3]) * bias)), 255), 0)
                    r = max(min(int(colorA[0] + ((colorB[0] - colorA[0]) * bias)), 255), 0)
                    g = max(min(int(colorA[1] + ((colorB[1] - colorA[1]) * bias)), 255), 0)
                    b = max(min(int(colorA[2] + ((colorB[2] - colorA[2]) * bias)), 255), 0)

                    color_map.append(bltColor(str(terminal.color_from_argb(a, r, g, b))))
                    #print "Bias_iv: {1} -> {0}".format(bias_inc, i)
                    bias += bias_inc
                current_key+=1
                print "InterOp: {0}".format(interp_num)
                index += interp_num
            except:
                pass
            print color_map
        return color_map


    def getRGB(self):
        """ Provides RGB values of name, usually for use in alpha transparency """
        if isinstance(self.colorname, str):
            blue = (self.color >> 0) & 255
            green = (self.color >> 8) & 255
            red = (self.color >> 16) & 255
            alpha = (self.color >> 24) & 255
            #print alpha, red, green, blue
        return int(red), int(green), int(blue), int(alpha)

    def blend(self, color2, bias=0.5, alpha=255 ):
        """Returns bltColor halfway between this color and color2"""
        colorA = self.getRGB()
        colorB = color2.getRGB()

        a = max(min(int(colorA[3] + ((colorB[3] - colorA[3]) * bias)), 255), 0)
        r = max(min(int(colorA[0] + ((colorB[0] - colorA[0]) * bias)), 255), 0)
        g = max(min(int(colorA[1] + ((colorB[1] - colorA[1]) * bias)), 255), 0)
        b = max(min(int(colorA[2] + ((colorB[2] - colorA[2]) * bias)), 255), 0)

        return bltColor(str(terminal.color_from_argb(a, r, g, b)))

    def trans(self, alpha_value):
        """Returns a color with the alpha_value"""
        r, g, b, a= self.getRGB()
        #print alpha_value, r, g, b
        alpha_value = max(min(alpha_value, 255), 1)
        return bltColor(str(terminal.color_from_argb(alpha_value, r, g, b)))







def drawRect(x, y, width, height):
    for w in xrange(width):
        for h in xrange(height):
            terminal.printf(x + w, y + h, "[U+2588]")



color1 = bltColor("red")

color2 = bltColor("#80905025")

color3 = bltColor("blue")




terminal.open()

terminal.set("window: size=80x25, cellsize=auto, title='Omni: menu';"
            "font: default;"
            "input: filter={keyboard}")

terminal.composition(True)

alphas = [16, 32, 64,80, 96, 112, 128, 144, 160, 176, 192, 208, 224, 240, 255, 240, 224, 208, 192, 176, 160, 144, 128, 112, 96, 80, 64, 32]
_alphas = cycle(alphas)

terminal.color(terminal.color_from_argb(128, 255,30,30))
drawRect(5,5,10,10)

color10 = bltColor('blue')

terminal.color(terminal.color_from_argb(128, 30,30,255))
#terminal.color(color10.trans(255))
drawRect(10,10,10,10)


l1 = (40, 12)
l2 = (25, 5)
l3 = (60, 18)
l4 = (5, 5)
l5 = (5, 18)


red = terminal.color_from_name('red')
green = terminal.color_from_name('green')
blue = terminal.color_from_name('blue')

n_red = terminal.color_from_name('255,0,0')
n_green = terminal.color_from_name('0,255,0')
n_blue = terminal.color_from_name('0,0,255')

c_red = bltColor('red')
c_green = bltColor('green')
c_blue = bltColor('blue')

n_c_red = bltColor('255,0,0')
n_c_green = bltColor('0,255,0')
n_c_blue = bltColor('0,0,255')


#Example Colors
color11 = bltColor('yellow')
color12 = bltColor('pink')


cmap = bltColor.color_map([bltColor('red').trans(0), 'blue', bltColor('red').trans(0)], [0,25,50])
cmap2 = bltColor.color_map(['blue', bltColor('red').trans(0), 'blue'], [0,25,50])



key = None
terminal.composition(True)
while True:
    terminal.clear()

    x, y = 10, 15



    terminal.color(red)
    terminal.printf(0,0, "red")
    terminal.color(green)
    terminal.printf(5, 0, "green")
    terminal.color(blue)
    terminal.printf(12, 0, "blue")

    #print red
    #print type(red)

    terminal.color('white')
    terminal.printf(18,0, ": {0}, {1}, {2} | type: {3}".format(red, green, blue, type(red)))

    terminal.color(n_red)
    terminal.printf(0,1, "red")
    terminal.color(n_green)
    terminal.printf(5, 1, "green")
    terminal.color(n_blue)
    terminal.printf(12, 1, "blue")

    terminal.color('white')
    terminal.printf(18, 1, ": {0}, {1}, {2} | type: {3}".format(n_red, n_green, n_blue, type(n_red)))

    #print c_red
    #print type(c_red)

    terminal.color(c_red)
    terminal.printf(0, 2, "red")
    terminal.color(c_green)
    terminal.printf(5, 2, "green")
    terminal.color(c_blue)
    terminal.printf(12, 2, "blue")

    terminal.color('white')
    terminal.printf(18, 2, ": {0}, {1}, {2} | type: {3}".format(c_red, c_green, c_blue, type(c_red)))

    terminal.color(n_c_red)
    terminal.printf(0, 3, "red")
    terminal.color(n_c_green)
    terminal.printf(5, 3, "green")
    terminal.color(n_c_blue)
    terminal.printf(12, 3, "blue")

    terminal.color('white')
    terminal.printf(18, 3, ": {0}, {1}, {2} | type: {3}".format(n_c_red, n_c_green, n_c_blue, type(n_c_red)))

    terminal.printf(0, 4, "[color={0}]red".format(red))
    terminal.printf(0, 5, "[color={0}]n_red".format(n_red))
    terminal.printf(0, 6, "[color={0}]c_red".format(c_red))
    terminal.printf(0, 7, "[color={0}]n_c_red".format(n_c_red))


    terminal.printf(0, 8, "[color={0}]green".format(green))
    terminal.printf(0, 9, "[color={0}]n_green".format(n_green))
    terminal.printf(0, 10, "[color={0}]c_green".format(c_green.trans(64)))
    terminal.printf(0, 11, "[color={0}]n_c_green".format(n_c_green.trans(64)))

    for i, c in enumerate(cmap):
        terminal.printf(20+i, 6, "[color={0}]C".format(c))

    for i, c in enumerate(cmap2):
        terminal.printf(20+i, 7, "[color={0}]C".format(c))

    terminal.color('white')

    terminal.printf(x, y, "[color={0}]Color11".format(color11))
    terminal.printf(x + 8, y, "x  {0} ".format(0.75))
    terminal.printf(x + 18, y, "= [color={0}]NewColor".format(color11 * 0.75))


    terminal.printf(x, y + 1, "[color={0}]Color11".format(color11))
    terminal.printf(x + 8, y + 1, "x [color={0}]Color12".format(color12))
    terminal.printf(x + 18, y + 1, "= [color={0}]NewColor".format(color11 * color12))

    terminal.printf(x, y + 2, "[color={0}]Color11".format(color11))
    terminal.printf(x + 8, y + 2, "+ [color={0}]Color12".format(color12))
    terminal.printf(x + 18, y + 2, "= [color={0}]NewColor".format(color11 + color12))

    terminal.printf(x, y + 3, "[color={0}]Color11".format(color11))
    terminal.printf(x + 8, y + 3, "- [color={0}]Color12".format(color12))
    terminal.printf(x + 18, y + 3, "= [color={0}]NewColor".format(color11 - color12))

    terminal.printf(x, y + 4, "[color={0}]Color11".format(color11))
    terminal.printf(x + 8, y + 4, "blend({1}) [color={0}]Color12".format(color12, 0.00))
    terminal.printf(x + 28, y + 4, "= [color={0}]NewColor".format(color11.blend(color12, 0.00)))

    terminal.printf(x, y + 5, "[color={0}]Color11".format(color11))
    terminal.printf(x + 8, y + 5, "blend({1}) [color={0}]Color12".format(color12, 0.25))
    terminal.printf(x + 28, y + 5, "= [color={0}]NewColor".format(color11.blend(color12, 0.25)))

    terminal.printf(x, y + 6, "[color={0}]Color11".format(color11))
    terminal.printf(x + 8, y + 6, "blend({1}) [color={0}]Color12".format(color12, 0.5))
    terminal.printf(x + 28, y + 6, "= [color={0}]NewColor".format(color11.blend(color12, 0.5)))

    terminal.printf(x, y + 7, "[color={0}]Color11".format(color11))
    terminal.printf(x + 8, y + 7, "blend({1}) [color={0}]Color12".format(color12, 0.75))
    terminal.printf(x + 28, y + 7, "= [color={0}]NewColor".format(color11.blend(color12, 0.75)))

    terminal.printf(x, y + 8, "[color={0}]Color11".format(color11))
    terminal.printf(x + 8, y + 8, "blend({1}) [color={0}]Color12".format(color12, 1.00))
    terminal.printf(x + 28, y + 8, "= [color={0}]NewColor".format(color11.blend(color12, 1.00)))

    #bline = b_line.get_line(l1, l2)

    key = None
    terminal.color('yellow')
    terminal.printf(l1[0] - 1, l1[1], '>')

    color10 = bltColor('sky')
    line.draw_line((l1[0], l1[1]), (l2[0], l2[1]), color10)

    terminal.color(bltColor('255, 255,64,64'))
    terminal.print_(15, 8, "[wrap=25x5][align=left-bottom]Hello my name is rudy!!!!!!!! I want to be your friend")



    terminal.color('yellow')
    terminal.printf(l2[0] + 1, l2[1], '<')



    terminal.refresh()

    if terminal.has_input():
        key = terminal.read()
    if key == terminal.TK_CLOSE:
        break
    elif key == terminal.TK_UP:
        l2 = (l2[0], l2[1] - 1)
    elif key == terminal.TK_DOWN:
        l2 = (l2[0], l2[1] + 1)
    elif key == terminal.TK_LEFT:
        l2 = (l2[0] - 1, l2[1])
    elif key == terminal.TK_RIGHT:
        l2 = (l2[0] + 1, l2[1])


terminal.close()