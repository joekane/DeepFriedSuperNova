from bearlibterminal import terminal

class bltColor(str):
    def __init__(self, color):
        #long.__init__(self, terminal.color_from_name(color))
        self.colorname = color

    def __str__(self):
        """ Returns object as str for use in formatting tags """
        return str(self.colorname)

    def __add__(self, color2):
        r1, g1, b1 = self.getRGB()
        r2, g2, b2 = color2.getRGB()

        return bltColor(terminal.color_from_argb(
            255,
            min(r1 + r2, 255),
            min(g1 + g2, 255),
            min(b1 + b2, 255),
        ))

    def __sub__(self, color2):
        r1, g1, b1 = self.getRGB()
        r2, g2, b2 = color2.getRGB()

        return bltColor(terminal.color_from_argb(
            255,
            max(r1 - r2, 0),
            max(g1 - g2, 0),
            max(b1 - b2, 0),
        ))

    def __mul__(self, color2):
        if isinstance(color2, bltColor):
            r1, g1, b1 = self.getRGB()
            r2, g2, b2 = color2.getRGB()
            return bltColor(terminal.color_from_argb(
                255,
                max(min((r1 * r2) // 255, 255), 0),
                max(min((g1 * g2) // 255, 255), 0),
                max(min((b1 * b2) // 255, 255), 0),
            ))
        else:
            r1, g1, b1 = self.getRGB()
            r2, g2, b2 = color2, color2, color2
            return bltColor(terminal.color_from_argb(
                255,
                max(min((r1 * r2), 255), 0),
                max(min((g1 * g2), 255), 0),
                max(min((b1 * b2), 255), 0),
            ))

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
                alpha = 255
                for i in xrange(interp_num):
                    colorA = bltColor(color_list[current_key]).getRGB()
                    colorB = bltColor(color_list[current_key+1]).getRGB()

                    r = max(min(int(colorA[0] + ((colorB[0] - colorA[0]) * bias_inc)), 255), 0)
                    g = max(min(int(colorA[1] + ((colorB[1] - colorA[1]) * bias_inc)), 255), 0)
                    b = max(min(int(colorA[2] + ((colorB[2] - colorA[2]) * bias_inc)), 255), 0)

                    color_map.append(bltColor(terminal.color_from_argb(alpha, r, g, b)))
                    bias_inc += bias_inc
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
            blue = (terminal.color_from_name(self.colorname) >> 0) & 255
            green = (terminal.color_from_name(self.colorname) >> 8) & 255
            red = (terminal.color_from_name(self.colorname) >> 16) & 255
        else:
            blue = (self.colorname >> 0) & 255
            green = (self.colorname >> 8) & 255
            red = (self.colorname >> 16) & 255
        return int(red), int(green), int(blue)

    def blend(self, color2, bias=0.5, alpha=255 ):
        """Returns bltColor halfway between this color and color2"""
        colorA = self.getRGB()
        colorB = color2.getRGB()

        r = max(min(int(colorA[0] + ((colorB[0] - colorA[0]) * bias)), 255), 0)
        g = max(min(int(colorA[1] + ((colorB[1] - colorA[1]) * bias)), 255), 0)
        b = max(min(int(colorA[2] + ((colorB[2] - colorA[2]) * bias)), 255), 0)

        return bltColor(terminal.color_from_argb(alpha, r, g, b))

    def trans(self, alpha_value):
        """Returns a color with the alpha_value"""
        r, g, b = self.getRGB()
        #print alpha_value, r, g, b
        alpha_value = max(min(alpha_value, 255), 1)
        return bltColor(terminal.color_from_argb(alpha_value, r, g, b))
