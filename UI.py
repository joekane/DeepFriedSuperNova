import libtcodpy as libtcod
import Constants


class Button:

    def __init__(self, text, rect, offset_rect, function=None):
        self.text = text
        self.rect = rect
        self.offset_rect = offset_rect
        self.fore = Constants.UI_Button_Fore
        self.back = Constants.UI_Button_Back
        self.fore_alt = Constants.UI_Button_Back
        self.back_alt = Constants.UI_Button_Fore
        self.target = libtcod.console_new(self.rect.width, self.rect.height)
        if function is None:
            self.function = do_nothing
        else:
            self.function = function

    def draw(self, key, mouse):


        min_x = self.rect.x1 + self.offset_rect.x1 - 1 - (self.rect.width / 2)
        max_x = min_x + self.rect.width + 1
        min_y = self.rect.y1 + self.offset_rect.y1

        if min_x < mouse.cx < max_x and min_y == mouse.cy:
            libtcod.console_set_default_foreground(self.target, self.fore_alt)
            libtcod.console_set_default_background(self.target, self.back_alt)
            if mouse.lbutton_pressed:
                return self.function()

        else:
            libtcod.console_set_default_foreground(self.target, self.fore)
            libtcod.console_set_default_background(self.target, self.back)

        libtcod.console_print_ex(self.target, 0, 0, libtcod.BKGND_SET, libtcod.LEFT, self.text)

        libtcod.console_blit(self.target, 0, 0, self.rect.width, self.rect.height, 0 , min_x + 1 , min_y , 1.0, 1.0)


def close_window():
    return 'close'


def test():
    print "TEST CLICK"


def do_nothing():
    return