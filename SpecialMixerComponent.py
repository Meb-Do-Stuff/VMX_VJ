from _Framework.MixerComponent import MixerComponent
from .SpecialChannelStripComponent import SpecialChannelStripComponent


class SpecialMixerComponent(MixerComponent):
    """ Special mixer class that uses return tracks alongside midi and audio tracks """
    __module__ = __name__

    def __init__(self, num_tracks):
        MixerComponent.__init__(self, num_tracks)
        self.num_tracks = num_tracks
        self.volumes_faders = []
        self.send_a = []
        self.send_b = []
        self.clip_launch_buttons = []

    def tracks_to_use(self):
        return tuple(self.song().visible_tracks) + tuple(self.song().return_tracks)

    def _create_strip(self):
        return SpecialChannelStripComponent()

    def alt_binding(self):
        for track in range(self.num_tracks):
            strip = self.channel_strip(track)
            strip.name = 'Channel_Strip_' + str(track)
            strip.set_select_button(self.clip_launch_buttons[0][track])
            strip.set_mute_button(self.clip_launch_buttons[1][track])
            strip.set_solo_button(self.clip_launch_buttons[2][track])
            strip.set_arm_button(self.clip_launch_buttons[3][track])
            if track < 8:
                strip.set_volume_control(None)
            else:
                strip.set_volume_control(self.volumes_faders[track-8])
            strip.set_pan_control(self.send_a[track])
            strip.set_send_controls((None, None, self.send_b[track]))
            strip.set_invert_mute_feedback(True)

    def unbind_alt(self):
        for track in range(self.num_tracks):
            strip = self.channel_strip(track)
            strip.set_select_button(None)
            strip.set_mute_button(None)
            strip.set_solo_button(None)
            strip.set_arm_button(None)
            strip.set_pan_control(None)
            strip.set_send_controls(None)
            strip.set_invert_mute_feedback(False)
            if track < 8:
                strip.set_volume_control(self.volumes_faders[track])
            else:
                strip.set_volume_control(None)
            strip.set_pan_control(None)
            strip.set_send_controls((self.send_a[track], self.send_b[track], None))
