import Live

from _Framework.CompoundComponent import CompoundComponent


class SpecialMenuSystem:  # (CompoundComponent)
    def __init__(self, buttons):
        # super().__init__()
        self._igniter = buttons[0]  # First button of last row will be used to open the menu
        self._last_known_listener = []

    def _setup_igniter(self):
        assert (self._igniter is not None)
        self._igniter.add_value_listener(self._engage_menu)

    def _engage_menu(self, value):
        if value == 127:
            Live.Base.log("Menu open!")
