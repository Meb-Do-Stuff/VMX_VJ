# emacs-mode: -*- python-*-
# -*- coding: utf-8 -*-

import Live
from _Framework.SessionComponent import SessionComponent
from _Framework.ButtonElement import ButtonElement
from math import sqrt


class SpecialSessionComponent(SessionComponent):
    """ Special SessionComponent for VMX V64 combination mode and button to fire selected clip slot, as well as a menu system """
    __module__ = __name__

    def __init__(self, num_tracks, num_scenes, buttons):
        SessionComponent.__init__(self, num_tracks, num_scenes)
        self.num_scenes = num_scenes
        self.num_tracks = num_tracks
        self._slot_launch_button = None
        self._igniter = buttons[int(sqrt(len(buttons))) * -1]
        # self._igniter.is_momentary = False
        self._buttons = buttons
        Live.Base.log(self._igniter.name)
        self.clip_launch_buttons = []
        self._setup_igniter()
        self._last_known_listener = []

    def setup_clip_launch(self):
        for scene_index in range(self.num_scenes):
            scene = self.scene(scene_index)
            scene.name = 'Scene_' + str(scene_index)
            button_row = []
            scene.set_launch_button(self._scene_launch_buttons[scene_index])
            scene.set_triggered_value(2)
            for track_index in range(self.num_tracks):
                button = self.clip_launch_buttons[scene_index][track_index]
                button_row.append(button)
                clip_slot = scene.clip_slot(track_index)
                clip_slot.name = str(track_index) + '_Clip_Slot_' + str(scene_index)
                clip_slot.set_launch_button(button)

    def disconnect(self):
        SessionComponent.disconnect(self)
        if self._slot_launch_button is not None:
            self._slot_launch_button.remove_value_listener(self._slot_launch_value)
            self._slot_launch_button = None

    def link_with_track_offset(self, track_offset, scene_offset):
        assert (track_offset >= 0)
        assert (scene_offset >= 0)
        if self._is_linked():
            self._unlink()
        self.set_offsets(track_offset, scene_offset)
        self._link()

    def unlink(self):
        if self._is_linked():
            self._unlink()

    def set_slot_launch_button(self, button):
        assert ((button is None) or isinstance(button, ButtonElement))
        if self._slot_launch_button != button:
            if self._slot_launch_button is not None:
                self._slot_launch_button.remove_value_listener(self._slot_launch_value)
            self._slot_launch_button = button
            if self._slot_launch_button is not None:
                self._slot_launch_button.add_value_listener(self._slot_launch_value)

            self.update()

    def _slot_launch_value(self, value):
        assert (value in range(128))
        assert (self._slot_launch_button is not None)
        if self.is_enabled():
            if (value != 0) or (not self._slot_launch_button.is_momentary()):
                if self.song().view.highlighted_clip_slot is not None:
                    self.song().view.highlighted_clip_slot.fire()

    def _setup_igniter(self):
        assert (self._igniter is not None)
        self._igniter.add_value_listener(self._engage_menu)
        self.update()

    def _engage_menu(self, value):
        if value == 127:
            for button in self.row_button:
                button
        elif value == 0:
            Live.Base.log("Menu closed!")

# local variables:
# tab-width: 4
