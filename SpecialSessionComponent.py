# emacs-mode: -*- python-*-
# -*- coding: utf-8 -*-

import Live
from _Framework.SessionComponent import SessionComponent
from _Framework.ButtonElement import ButtonElement
from math import sqrt


class SpecialSessionComponent(SessionComponent):
    """ Special SessionComponent for VMX V64 combination mode and button to fire selected clip slot, as well as an alt system """
    __module__ = __name__

    def __init__(self, num_tracks, num_scenes, buttons, mixer, transport):
        SessionComponent.__init__(self, num_tracks, num_scenes)
        self.num_scenes = num_scenes
        self.num_tracks = num_tracks
        self._slot_launch_button = None
        self._alt0_igniter = buttons[int(sqrt(len(buttons))) * -1]
        self._alt1_igniter = buttons[int(sqrt(len(buttons))) * -1 + 1]
        # self._igniter.is_momentary = False
        self._buttons = buttons
        self._mixer = mixer
        self._transport = None
        self.clip_launch_buttons = []
        self._setup_igniter()
        self._last_known_listener = []
        self.session_right = None
        self.session_left = None
        self.session_up = None
        self.session_down = None

    def setup_clip_launch(self):
        for scene_index in range(self.num_scenes):
            scene = self.scene(scene_index)
            scene.name = 'Scene_' + str(scene_index)
            button_row = []
            # scene.set_launch_button(self._scene_launch_buttons[scene_index])
            scene.set_triggered_value(2)
            for track_index in range(self.num_tracks):
                button = self.clip_launch_buttons[scene_index][track_index]
                button_row.append(button)
                clip_slot = scene.clip_slot(track_index)
                clip_slot.name = str(track_index) + '_Clip_Slot_' + str(scene_index)
                clip_slot.set_launch_button(button)

    def unbind_clip_launch(self):
        for scene_index in range(self.num_scenes):
            scene = self.scene(scene_index)
            for track_index in range(self.num_tracks):
                clip_slot = scene.clip_slot(track_index)
                clip_slot.set_launch_button(None)

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
        assert (self._alt0_igniter is not None)
        self._alt0_igniter.add_value_listener(self._engage_alt)
        assert (self._alt1_igniter is not None)
        self._alt1_igniter.add_value_listener(self._engage_sceneLaunch)
        self.update()

    def view_setup(self):
        self.set_track_bank_buttons(self.session_right, self.session_left)
        self.set_scene_bank_buttons(self.session_down, self.session_up)
        self.set_select_buttons(None, None)

    def _engage_sceneLaunch(self, value):
        if value == 127 and not self._alt0_igniter.is_pressed():  # Scene launch mod open
            self.unbind_clip_launch()
            for scene_index in range(self.num_scenes):
                scene = self.scene(scene_index)
                scene.name = 'Scene_' + str(scene_index)
                scene.set_launch_button(self.clip_launch_buttons[scene_index][-1])  # Button is in push mode while it's toggle (problem comes from scene scripts (have to figure out a way to bypass the problem))
                scene.set_triggered_value(2)
        elif value == 0:
            for scene_index in range(self.num_scenes):
                self.scene(scene_index).set_launch_button(None)
            self.setup_clip_launch()

    def _engage_alt(self, value):
        if value == 127 and not self._alt1_igniter.is_pressed():  # Alt enabled
            self.set_track_bank_buttons(None, None)
            self.set_scene_bank_buttons(None, None)
            self.set_select_buttons(self.session_down, self.session_up)
            self.unbind_clip_launch()
            self._mixer.alt_binding()
            self._transport.unbind_jog_wheel()
        elif value == 0:  # Alt disabled
            self.view_setup()
            self.setup_clip_launch()
            self._mixer.unbind_alt()
            self._transport.set_jog_wheel_time()
