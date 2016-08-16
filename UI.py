import libtcodpy as libtcod
import Constants
import Map
import GameState
import Render
import Animate


class Button:

    def __init__(self, text, x, y, function=None, length=16, target=0):
        self.text = text
        self.x = x
        self.y = y
        self.target = target
        self.length = length
        self.fore = Constants.UI_Button_Fore
        self.back = Constants.UI_Button_Back
        self.fore_alt = Constants.UI_Button_Back
        self.back_alt = Constants.UI_Button_Fore

        if function is None:
            self.function = do_nothing
        else:
            self.function = function

    def draw(self, key, mouse):


        # min_x = self.rect.x1 + self.offset_rect.x1 - 1 - (self.rect.width / 2)
        # max_x = min_x + self.rect.width + 1
        # min_y = self.rect.y1 + self.offset_rect.y1
        #print self.length

        min_x = self.x - (self.length / 2) - 2
        max_x = min_x + self.length + 3

        if min_x < mouse.cx < max_x and self.y - 1 <= mouse.cy <= self.y + 1:
            # libtcod.console_set_default_foreground(self.target, self.fore_alt)
            # libtcod.console_set_default_background(self.target, self.back_alt)
            Animate.large_button(self.x, self.y, self.text, True, length=self.length, target=self.target)
            if mouse.lbutton_pressed:
                # print "Func!"
                return self.function()

        else:
            # libtcod.console_set_default_foreground(self.target, self.fore)
            # libtcod.console_set_default_background(self.target, self.back)
            Animate.large_button(self.x, self.y, self.text, False, length=self.length, target=self.target)

        # libtcod.console_print_ex(self.target, 0, 0, libtcod.BKGND_SET, libtcod.LEFT, self.text)

        # libtcod.console_blit(self.target, 0, 0, self.rect.width, self.rect.height, 0 , min_x + 1 , min_y , 1.0, 1.0)


def menu(header, options, width):
    key = libtcod.Key()
    mouse = libtcod.Mouse()
    if len(options) > 26:
        raise ValueError('Cannot have a menu with more than 26 options.')

    # calculate total height for the header (after auto-wrap) and one line per option
    header_height = libtcod.console_get_height_rect(Render.consoles['map_console'], 0, 0, width, Constants.SCREEN_HEIGHT, header)
    if header == '':
        header_height = 0
    height = len(options) + header_height

    # create an off-screen console that represents the menu's window
    window = libtcod.console_new(width, height)

    # print the header, with auto-wrap
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

    # print all the options
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += 1
        letter_index += 1

    # blit the contents of "window" to the root console
    x = Constants.SCREEN_WIDTH / 2 - width / 2
    y = Constants.SCREEN_HEIGHT / 2 - height / 2
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.5)

    # compute x and y offsets to convert console position to menu position
    x_offset = x  # x is the left edge of the menu
    y_offset = y + header_height  # subtract the height of the header from the top edge of the menu

    while True:
        # present the root console to the player and check for input
        libtcod.console_flush()
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if mouse.lbutton_pressed:
            (menu_x, menu_y) = (mouse.cx - x_offset, mouse.cy - y_offset)
            # check if click is within the menu and on a choice
            if 0 <= menu_x < width and 0 <= menu_y < height - header_height:
                return menu_y

        if mouse.rbutton_pressed or key.vk == libtcod.KEY_ESCAPE:
            return None  # cancel if the player right-clicked or pressed Escape

        if key.vk == libtcod.KEY_ENTER and key.lalt:
            # Alt+Enter: toggle fullscreen
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        # convert the ASCII code to an index; if it corresponds to an option, return it
        index = key.c - ord('a')
        if 0 <= index < len(options):
            return index
        # if they pressed a letter that is not an option, return None
        if 0 <= index <= 26:
            return



def Display_MainMenu():
    key = libtcod.Key()
    mouse = libtcod.Mouse()

    # calculate total height for the header (after auto-wrap) and one line per option
    width = Constants.SCREEN_WIDTH
    height = Constants.SCREEN_HEIGHT

    mm = libtcod.console_new(width, height)
    # print the header, with auto-wrap
    libtcod.console_set_default_foreground(mm, Constants.UI_PopFore)
    libtcod.console_set_default_background(mm, Constants.UI_PopBack)

    libtcod.console_print_frame(mm, 0, 0, width, height, clear=True,
                                flag=libtcod.BKGND_SET,
                                fmt="Deep Fried Supernova")

    libtcod.console_print_rect(mm, 4, 4, width, height, 'Welcome to Deep Fried Supernova')


    # blit the contents of "window" to the root console
    x = 0
    y = 0


    button_text = 'New Game'
    ng_button = Button(button_text,
                       width / 2,
                       height - 12,
                       function=new_game)

    button_text = 'Continue Game'
    ct_button = Button(button_text,
                       width / 2,
                       height - 9,
                       function=close_window)

    button_text = 'Quit'
    qt_button = Button(button_text,
                       width / 2,
                       height - 6,
                       function=close_window)

    img = libtcod.image_load('diner_logo_sm.png')
    libtcod.image_set_key_color(img, libtcod.Color(0, 0, 0))
    # show the background image, at twice the regular console resolution
    libtcod.image_blit_2x(img, mm, 37, 2)

    libtcod.console_blit(mm, 0, 0, width, height, 0, 0, 0, 1.0, 1.0)

    while True:

        libtcod.console_flush()
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if qt_button.draw(key, mouse) == 'close':
            return

        ct_button.draw(key, mouse)
        ng_button.draw(key, mouse)

        if key.vk == libtcod.KEY_ENTER and key.lalt:
            # Alt+Enter: toggle fullscreen
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())
        if key.vk == libtcod.KEY_ESCAPE or key.vk == libtcod.KEY_ESCAPE or key.vk == libtcod.KEY_SPACE:
            return


def msgbox(text, width=50):
    menu(text, [], width)  # use menu() as a sort of "message box"


def inventory_menu(header):
    # show a menu with each item of the inventory as an option
    if len(GameState.inventory) == 0:
        options = ['Inventory is empty.']
    else:
        options = []
        for item in GameState.inventory:
            text = item.name
            # show additional information, in case it's equipped
            if item.equipment and item.equipment.is_equipped:
                text = text + ' (on ' + item.equipment.slot + ')'
            options.append(text)

    index = menu(header, options, Constants.INVENTORY_WIDTH)

    # if an item was chosen, return it
    if index is None or len(GameState.inventory) == 0:
        return None
    return GameState.inventory[index].item


def close_window():
    return 'close'


def new_game():
    print "NG?"
    return GameState.new_game()


def test():
    print "TEST CLICK"


def do_nothing():
    return