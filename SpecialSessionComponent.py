from _Framework.SessionComponent import SessionComponent
from _Framework.ButtonElement import ButtonElement
from math import sqrt
import Live


class SpecialSessionComponent(SessionComponent):
    """ Special SessionComponent for VMX V64 combination mode and button to fire selected clip slot, as well as an alt system """
    __module__ = __name__

    def __init__(self, num_tracks, num_scenes, buttons, mixer, transport):
        SessionComponent.__init__(self, num_tracks, num_scenes)
        self.num_scenes = num_scenes
        self.num_tracks = num_tracks
        self.slot_launch_button = None
        self._alt0_igniter = buttons[int(sqrt(len(buttons))) * -1]
        self._alt1_igniter = buttons[int(sqrt(len(buttons))) * -1 + 1]
        # self._igniter.is_momentary = False
        self._buttons = buttons
        self._mixer = mixer
        self._transport = transport
        self.clip_launch_buttons = []
        self._setup_igniter()
        self._last_known_listener = []
        self.session_right = None
        self.session_left = None
        self.session_up = None
        self.session_down = None
        self.delete_button = None

    def setup_clip_launch(self):
        self.unbind_clip_launch()
        for scene_index in range(self.num_scenes):
            scene = self.scene(scene_index)
            scene.name = 'Scene_' + str(scene_index)
            scene.set_triggered_value(2)
            for track_index in range(self.num_tracks):
                clip_slot = scene.clip_slot(track_index)
                clip_slot.name = str(track_index) + '_Clip_Slot_' + str(scene_index)
                clip_slot.set_launch_button(self.clip_launch_buttons[scene_index][track_index])

    def unbind_clip_launch(self):
        for scene_index in range(self.num_scenes):
            scene = self.scene(scene_index)
            for track_index in range(self.num_tracks):
                clip_slot = scene.clip_slot(track_index)
                clip_slot.set_launch_button(None)

    def setup_clip_delete(self):
        for scene_index in range(self.num_scenes):
            scene = self.scene(scene_index)
            scene.name = 'Scene_' + str(scene_index)
            scene.set_triggered_value(2)
            for track_index in range(self.num_tracks):
                self.clip_launch_buttons[scene_index][track_index].add_value_listener(lambda value, cs=scene.clip_slot(track_index): self._delete_clip(cs))

    def _delete_clip(self, clip_slot):
        if not self.delete_button.is_pressed() or self._alt0_igniter.is_pressed() or self._alt1_igniter.is_pressed() or clip_slot._clip_slot is None or not clip_slot._clip_slot.has_clip:
            return
        clip_slot._clip_slot.delete_clip()

    def disconnect(self):
        SessionComponent.disconnect(self)
        if self.slot_launch_button is not None:
            self.slot_launch_button.remove_value_listener(self._slot_launch_value)
            self.slot_launch_button = None

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

    def set_slot_launch_button(self):
        assert ((self.slot_launch_button is None) or isinstance(self.slot_launch_button, ButtonElement))
        if self.slot_launch_button is not None:
            self.slot_launch_button.add_value_listener(self._slot_launch_value)
        self.update()

    def unset_slot_launch_button(self):
        if self.slot_launch_button is not None:
            self.slot_launch_button.remove_value_listener(self._slot_launch_value)
            self.update()

    def _slot_launch_value(self, value):
        assert (value in range(128))
        if self.is_enabled():
            if (value != 0) or (not self.slot_launch_button.is_momentary()):
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
        if self._alt0_igniter.is_pressed() or self._mixer.crossfader_binding_button.is_pressed():
            return
        if value == 127:  # Scene launch mod open
            self.unbind_clip_launch()
            for scene_index in range(self.num_scenes):
                scene = self.scene(scene_index)
                scene.name = 'Scene_' + str(scene_index)
                scene.set_launch_button(self.clip_launch_buttons[scene_index][-1])  # Button is in push mode while it's toggle (problem comes from scene scripts (have to figure out a way to bypass the problem))
                scene.set_triggered_value(2)
                self.set_stop_track_clip_buttons([self.clip_launch_buttons[-1][track_index] for track_index in range(self.num_tracks - 1)])
            self._mixer.set_scene_mode(True)
        elif value == 0:
            for scene_index in range(self.num_scenes):
                self.scene(scene_index).set_launch_button(None)
            self.set_stop_track_clip_buttons([])
            self.setup_clip_launch()
            self._mixer.set_scene_mode(False)

    def _engage_alt(self, value):
        if self._mixer.crossfader_binding_button.is_pressed() or self._alt1_igniter.is_pressed():
            return
        if value == 127:
            self.set_track_bank_buttons(None, None)
            self.set_scene_bank_buttons(None, None)
            self.set_select_buttons(self.session_down, self.session_up)
            self.unbind_clip_launch()
            self._mixer.alt_binding()
            self._transport.unbind_jog_wheel()
            self.set_slot_launch_button()
            self._transport.unbind_play_button()
        elif value == 0:
            self.view_setup()
            self.setup_clip_launch()
            self._mixer.unbind_alt()
            self._transport.set_jog_wheel_time()
            self.unset_slot_launch_button()
            self._transport.setup_play_button()

    def deletion_manager(self):
        self.delete_button.add_value_listener(self._deletion)
        self.session_up.add_value_listener(lambda value: self._reset_value(0))
        self.session_down.add_value_listener(lambda value: self._reset_value(0))
        self.session_left.add_value_listener(lambda value: self._reset_value(1))
        self.session_right.add_value_listener(lambda value: self._reset_value(1))

        self.setup_clip_delete()
        self.update()

    def _deletion(self, value):
        if value == 127 and not self._alt0_igniter.is_pressed() and not self._alt1_igniter.is_pressed():
            self.unbind_clip_launch()
        if value == 0:
            self.setup_clip_launch()

    def _reset_value(self, setting_type):
        """
        type 0 = View Up & Down
        type 1 = View Left & Right
        """
        if not self.delete_button.is_pressed():
            return
        if self._alt0_igniter.is_pressed():
            if setting_type == 0:
                self.song().view.selected_scene = self.song().scenes[0]
            elif setting_type == 1:
                self.song().view.selected_track = self.song().tracks[0]
        if setting_type == 0:
            self.set_offsets(self.track_offset(), 0)
        elif setting_type == 1:
            self.set_offsets(0, self.scene_offset())
