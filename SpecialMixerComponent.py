from _Framework.MixerComponent import MixerComponent
from .SpecialChannelStripComponent import SpecialChannelStripComponent
from _Framework.ButtonElement import ButtonElement
from _Framework.SliderElement import SliderElement


class SpecialMixerComponent(MixerComponent):
    """ Special mixer class that uses return tracks alongside midi and audio tracks """
    __module__ = __name__

    def __init__(self, num_scenes: int, num_tracks: int):
        MixerComponent.__init__(self, num_tracks)
        self.num_scenes = num_scenes
        self.num_tracks = num_tracks
        self.clip_launch_buttons = []

    def tracks_to_use(self):
        """
        Return the tracks, including return tracks.
        Returns a tuple of Track.Track objects.
        """
        return tuple(self.song().visible_tracks) + tuple(self.song().return_tracks)

    def _create_strip(self):
        return SpecialChannelStripComponent()

    def _master_control(self, value: float):
        """
        Control master volume, 0 is -0.01, else it's +0.01.
        """
        if value == 0:
            self.song().master_track.mixer_device.volume.value -= 0.01
        else:
            self.song().master_track.mixer_device.volume.value += 0.01

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

    def _delete_track(self, index: int):
        """
        Delete a track at the specified index.
        :param index: The index of the track to delete.
        """
        self.song().delete_track(index)
