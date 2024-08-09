import Live
from _Framework.MixerComponent import MixerComponent
from .SpecialChannelStripComponent import SpecialChannelStripComponent


class SpecialMixerComponent(MixerComponent):
    """ Special mixer class that uses return tracks alongside midi and audio tracks """
    __module__ = __name__

    def __init__(self, num_tracks, track_left, track_right, jog_wheel):
        MixerComponent.__init__(self, num_tracks)
        self.num_tracks = num_tracks
        self.volumes_faders = []
        self.send_a = []
        self.send_b = []
        self.track_left = track_left
        self.track_right = track_right
        self.clip_launch_buttons = []
        self._jog_wheel = jog_wheel
        self.delete_button = None
        self._is_scene_mode = False
        self._is_alt_mode = False

    def tracks_to_use(self):
        return tuple(self.song().visible_tracks) + tuple(self.song().return_tracks)

    def _create_strip(self):
        return SpecialChannelStripComponent()

    def set_scene_mode(self, value):
        self._is_scene_mode = value

    def alt_binding(self):
        self.set_select_buttons(self.track_right, self.track_left)
        for track in range(self.num_tracks):
            strip = self.channel_strip(track)
            strip.name = 'Channel_Strip_' + str(track)
            strip.set_select_button(self.clip_launch_buttons[0][track])
            strip.set_mute_button(self.clip_launch_buttons[1][track])
            strip.set_solo_button(self.clip_launch_buttons[2][track])
            strip.set_arm_button(self.clip_launch_buttons[3][track])
            strip.set_volume_control(([None] * 8 + self.volumes_faders)[track])
            strip.set_pan_control(self.send_b[track])
            strip.set_send_controls((None, None, self.send_a[track]))
            strip.set_invert_mute_feedback(True)
        if self._jog_wheel is not None:
            self._jog_wheel.add_value_listener(self._master_control)
        self._is_alt_mode = True
        self.update()

    def _master_control(self, value):
        if value == 0:
            self.song().master_track.mixer_device.volume.value -= 0.01
        else:
            self.song().master_track.mixer_device.volume.value += 0.01

    def unbind_alt(self):
        self.set_select_buttons(None, None)
        for track in range(self.num_tracks):
            strip = self.channel_strip(track)
            strip.name = 'Channel_Strip_' + str(track)
            strip.set_select_button(None)
            strip.set_mute_button(None)
            strip.set_solo_button(None)
            strip.set_arm_button(None)
            strip.set_volume_control((self.volumes_faders + [None] * 8)[track])
            strip.set_pan_control(None)
            strip.set_send_controls((self.send_a[track], self.send_b[track], None))
            strip.set_invert_mute_feedback(True)
        if self._jog_wheel is not None:
            self._jog_wheel.remove_value_listener(self._master_control)
        self._is_alt_mode = False
        self.update_all()

    def setup_track_deletion(self):
        for button in range(self.num_tracks - 1):
            self.clip_launch_buttons[-1][button].add_value_listener(lambda value, index=button: self._delete_track(index))
        for button in range(self.num_tracks // 2):
            Live.Base.log("Setting fader")
            self.volumes_faders[button].add_value_listener(lambda value, index=button: self._reset_value(index, 0))
            self.volumes_faders[button].add_value_listener(lambda value, index=button: self._reset_value(index + 8, 0))
            self.send_a[button].add_value_listener(lambda value, index=button: self._reset_value(index, 1))
            self.send_b[button].add_value_listener(lambda value, index=button: self._reset_value(index, 2))
            self._jog_wheel.add_value_listener(lambda value, index=button: self._reset_value(index, 3))
        self.update()

    def _delete_track(self, index):
        if self.delete_button.is_pressed() and self._is_scene_mode:
            self.song().delete_track(index)

    def _reset_value(self, index, setting_type):
        """
        type 0 = Volume
        type 1 = Send A & C
        type 2 = Send B & Pan
        type 3 = Master Volume
        """
        if not self.delete_button.is_pressed():
            return
        tracks = self.song().tracks + self.song().return_tracks
        if setting_type == 0:
            if (index > 7 and not self._is_alt_mode) or len(tracks) <= index + self._track_offset:
                return
            tracks[index + self._track_offset].mixer_device.volume.value = 0.85
        if setting_type == 1:
            if len(tracks) <= index + self._track_offset:
                return
            if not self._is_alt_mode and len(tracks[index + self._track_offset].mixer_device.sends) > 0:
                tracks[index + self._track_offset].mixer_device.sends[0].value = 0
            elif len(tracks[index + self._track_offset].mixer_device.sends) > 2:
                tracks[index + self._track_offset].mixer_device.sends[2].value = 0
        if setting_type == 2:
            if len(tracks) <= index + self._track_offset:
                return
            if not self._is_alt_mode and len(tracks[index + self._track_offset].mixer_device.sends) > 1:
                tracks[index + self._track_offset].mixer_device.sends[1].value = 0
            else:
                tracks[index + self._track_offset].mixer_device.panning.value = 0
        if setting_type == 3:
            if self._is_alt_mode:
                self.song().master_track.mixer_device.volume.value = 0.85
