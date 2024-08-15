from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SliderElement import SliderElement
from _Framework.ButtonElement import ButtonElement


class SpecialMenuComponent(ControlSurfaceComponent):
    __module__ = __name__

    def __init__(self, name: str):
        ControlSurfaceComponent.__init__(self)
        self.unbind_functions = []
        self.bind_functions = []
        self.name = name

    def activated(self):
        for bind, note in self.bind_functions:
            if note is None:
                bind()
            else:
                bind(note)

    def deactivated(self):
        for unbind, note in self.unbind_functions:
            if note is None:
                unbind()
            else:
                unbind(None)

    def add_binds(self, bind_function, unbind_function, note: None):
        self.bind_functions.append((bind_function, note))
        self.unbind_functions.append((unbind_function, note))


class MenuManager(ControlSurfaceComponent):
    __module__ = __name__

    def __init__(self, note_map: list[ButtonElement], ctrl_map: list[SliderElement]):
        ControlSurfaceComponent.__init__(self)
        self._note_map = note_map
        self._ctrl_map = ctrl_map
        self._menus = {}
        self.current_menu = None

    def add_menu(self, menu: SpecialMenuComponent):
        self._menus[menu.name] = menu

    def activate_menu(self, menu_name: str):
        if self.current_menu is not None:
            self.current_menu.deactivated()
        self.current_menu = self.menus[menu_name]
        self.current_menu.activated()

    def add_binds_to_menu(self, name: str, bind_function, unbind_function, note: None):
        self._menus[name].add_binds(bind_function, unbind_function, note)
