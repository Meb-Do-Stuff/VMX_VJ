import Live
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent


# from _Framework.SliderElement import SliderElement
from _Framework.ButtonElement import ButtonElement


class SpecialMenuComponent:

    def __init__(self, name: str, is_additive: bool = False):
        self.unbind_functions = []
        self.bind_functions = []
        self.name = name
        self.is_additive = is_additive
        self.is_enabled = False
        self.opposite_menu = []  # Menus that have to be disabled in additive mode when this one is enabled

    def activated(self):
        for bind, arg in self.bind_functions:
            if arg is None:
                bind()
            else:
                bind(arg)
        self.is_enabled = True

    def deactivated(self):
        for unbind, arg in self.unbind_functions:
            if arg is None:
                unbind()
            else:
                unbind(None)
        self.is_enabled = False

    def add_bind(self, bind_function, unbind_function, note: None):
        self.bind_functions.append((bind_function, note))
        self.unbind_functions.append((unbind_function, note))


class MenuManager(ControlSurfaceComponent):
    __module__ = __name__

    def __init__(self, note_map, ctrl_map):
        ControlSurfaceComponent.__init__(self)
        self._note_map = note_map
        self._ctrl_map = ctrl_map
        self._menus = {}
        self._current_menu = {}
        self._buttons = {}

    def add_menu(self, menu: SpecialMenuComponent):
        self._menus[menu.name] = menu

    def activate_menu(self, menu_name: str):
        if len(self._current_menu) != 0 and not self._menus[menu_name].is_additive:
            for menu in self._menus:
                self._menus[menu].deactivated()
        self._current_menu[menu_name] = self._menus[menu_name]
        self._current_menu[menu_name].activated()
        if self._current_menu[menu_name].is_additive:
            for menu in self._menus:
                if self._menus[menu].is_additive and menu is not menu_name and menu in self._menus[menu].opposite_menu and menu in self._current_menu:
                    self._current_menu[menu].deactivated()

    def add_binds_to_menu(self, name: str, bind_function, unbind_function, arg=None):
        self._menus[name].add_bind(bind_function, unbind_function, arg)

    def set_button(self, name: str, button: ButtonElement):
        self._buttons[name] = (button, lambda value: self.activate_menu(name))
        button.add_value_listener(self._buttons[name][1])

    def add_opposite(self, menu_names: list):
        for menu_name in menu_names:
            self._menus[menu_name].opposite_menu = menu_names
