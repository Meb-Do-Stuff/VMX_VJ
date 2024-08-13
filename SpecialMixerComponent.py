from _Framework.MixerComponent import MixerComponent
from .SpecialChannelStripComponent import SpecialChannelStripComponent
from _Framework.ButtonElement import ButtonElement
from _Framework.SliderElement import SliderElement


class SpecialMixerComponent(MixerComponent):
    """ Special mixer class that uses return tracks alongside midi and audio tracks """
    __module__ = __name__

    def __init__(self, num_scenes: int, num_tracks: int, track_left: ButtonElement, track_right: ButtonElement):
        MixerComponent.__init__(self, num_tracks)
        self.num_scenes = num_scenes
        self.num_tracks = num_tracks
        self.volumes_faders = []
        self.send_a = []
        self.send_b = []
        self.track_left = track_left
        self.track_right = track_right
        self.clip_launch_buttons = []
        self._crossfader = None
        self.delete_button = None
        self._prehear_fader = None
        self._is_scene_mode = False
        self._is_alt_mode = False

    def tracks_to_use(self):
        """
        Return the tracks, including return tracks.
        Returns a tuple of Track.Track objects.
        """
        return tuple(self.song().visible_tracks) + tuple(self.song().return_tracks)

    def _create_strip(self):
        return SpecialChannelStripComponent()

    def set_scene_mode(self, state: bool):
        """
        Set the scene mode for the mixer.
        :param state: Whether to scene mode is enabled or not.
        """
        self._is_scene_mode = state
        self.engage_crossfader_binding()

    def alt_binding(self):
        """
        Setup ALT mode for the mixer.
        """
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
        self.update()

    def _master_control(self, value: float):
        """
        Control master volume, 0 is -0.01, else it's +0.01.
        """
        if value == 0:
            self.song().master_track.mixer_device.volume.value -= 0.01
        else:
            self.song().master_track.mixer_device.volume.value += 0.01

    def prepare_crossfader_control(self, crossfader: SliderElement):
        """
        Assign crossfader slider.
        """
        self._crossfader = crossfader
        self.set_crossfader_control(self._crossfader)

    def prepare_prehear_volume_control(self, prehear_volume: SliderElement):
        """
        Assign Cue (prehear) slider.
        """
        self._prehear_fader = prehear_volume
        self.set_prehear_volume_control(self._prehear_fader)

    def engage_crossfader_binding(self):
        """
        Bind each buttons (normally used for clip launching) to the crossfader control.
        (Have to clear the clip launching bindings first)
        """
        for scene_index in range(min(self.num_scenes, 3)):
            for track_index in range(min(len(self.tracks_to_use()), 15)):
                self.clip_launch_buttons[scene_index][track_index].add_value_listener(lambda value, si=scene_index, ti=track_index: self._set_crossfader_control(si, ti))

    def _set_crossfader_control(self, value: int, index: int):
        """
        Set the crossfader bind set for a track.\n
        0 = A, 1 = None, 2 = B
        :param value: The value to set the crossfader to.
        :param index: The index of the track to set the crossfader for (depending on the view, track offset already counted).
        """
        self.tracks_to_use()[index + self._track_offset].mixer_device.crossfade_assign = value

    def setup_track_deletion(self):
        """
        Setup the deletion manager for the mixer.
        """
        for button in range(self.num_tracks - 1):
            self.clip_launch_buttons[-1][button].add_value_listener(lambda value, index=button: self._delete_track(index))
        for button in range(self.num_tracks // 2):
            self.volumes_faders[button].add_value_listener(lambda value, index=button: self._reset_value(index, 0))
            self.volumes_faders[button].add_value_listener(lambda value, index=button: self._reset_value(index + 8, 0))
            self.send_a[button].add_value_listener(lambda value, index=button: self._reset_value(index, 1))
            self.send_b[button].add_value_listener(lambda value, index=button: self._reset_value(index, 2))
        self._crossfader.add_value_listener(lambda value: self._reset_value(0, 4))
        self._prehear_fader.add_value_listener(lambda value: self._reset_value(0, 5))
        self.update()

    def _delete_track(self, index: int):
        """
        Delete a track at the specified index.
        :param index: The index of the track to delete.
        """
        if self.delete_button.is_pressed() and self._is_scene_mode:
            self.song().delete_track(index)

    def _reset_value(self, index: int, setting_type: int):
        """
        Let you reset certain parameters listed below.

        Setting types:\n
        setting_type 0 = Volume\n
        setting_type 1 = Send A & C\n
        setting_type 2 = Send B & Pan\n
        setting_type 3 = Master Volume\n
        setting_type 4 = Crossfader\n
        setting_type 5 = Prehear

        :param index: The index of the parameter to reset (unused for some settings).
        :param setting_type: The type of setting to reset.
        """
        if not self.delete_button.is_pressed():
            return
        tracks = self.song().tracks + self.song().return_tracks
        if setting_type == 0:
            if (index > 7 and not self._is_alt_mode) or len(tracks) <= index + self._track_offset:
                return
            tracks[index + self._track_offset].mixer_device.volume.value = 0.85
        elif setting_type == 1:
            if len(tracks) <= index + self._track_offset:
                return
            if not self._is_alt_mode and len(tracks[index + self._track_offset].mixer_device.sends) > 0:
                tracks[index + self._track_offset].mixer_device.sends[0].value = 0
            elif len(tracks[index + self._track_offset].mixer_device.sends) > 2:
                tracks[index + self._track_offset].mixer_device.sends[2].value = 0
        elif setting_type == 2:
            if len(tracks) <= index + self._track_offset:
                return
            if not self._is_alt_mode and len(tracks[index + self._track_offset].mixer_device.sends) > 1:
                tracks[index + self._track_offset].mixer_device.sends[1].value = 0
            else:
                tracks[index + self._track_offset].mixer_device.panning.value = 0
        elif setting_type == 3:
            if self._is_alt_mode:
                self.song().master_track.mixer_device.volume.value = 0.85
        elif setting_type == 4:
            self.song().master_track.mixer_device.crossfader.value = 0
        elif setting_type == 5:
            self.song().master_track.mixer_device.cue_volume.value = 0.85
