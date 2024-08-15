from _Framework.SessionComponent import SessionComponent
from _Framework.ButtonElement import ButtonElement
from _Framework.ClipSlotComponent import ClipSlotComponent
from math import sqrt


class SpecialSessionComponent(SessionComponent):
    """ Special SessionComponent for VMX VJ combination mode and button to fire selected clip slot, as well as an alt system """
    __module__ = __name__

    def __init__(self, num_tracks: int, num_scenes: int):
        SessionComponent.__init__(self, num_tracks, num_scenes)
        self.num_scenes = num_scenes
        self.num_tracks = num_tracks
        self.slot_launch_button = None
        self.clip_launch_buttons = []

    def setup_clip_launch(self):
        """
        Setup the 16x4 matrix of button to launch clips.
        """
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
        """
        Unbind the 16x4 matrix of button to launch clips.
        """
        for scene_index in range(self.num_scenes):
            scene = self.scene(scene_index)
            for track_index in range(self.num_tracks):
                clip_slot = scene.clip_slot(track_index)
                clip_slot.set_launch_button(None)

    def setup_clip_delete(self):
        """
        Setup the 16x4 matrix of button to delete clips.
        """
        for scene_index in range(self.num_scenes):
            scene = self.scene(scene_index)
            scene.name = 'Scene_' + str(scene_index)
            scene.set_triggered_value(2)
            for track_index in range(self.num_tracks):
                self.clip_launch_buttons[scene_index][track_index].add_value_listener(lambda value, cs=scene.clip_slot(track_index): self._delete_clip(cs))

    def _delete_clip(self, clip_slot: ClipSlotComponent):
        """
        Delete given clip slot.
        """
        # self.clip_launch_buttons[scene_index][track_index].add_value_listener(lambda value, cs=scene.clip_slot(track_index): self._delete_clip(cs))
        if clip_slot._clip_slot is None or not clip_slot._clip_slot.has_clip:
            return
        clip_slot._clip_slot.delete_clip()

    def disconnect(self):
        SessionComponent.disconnect(self)
        if self.slot_launch_button is not None:
            self.slot_launch_button.remove_value_listener(self._slot_launch_value)
            self.slot_launch_button = None

    def link_with_track_offset(self, track_offset: int, scene_offset: int):
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
        """
        Set the button to launch the selected clip slot.
        """
        assert ((self.slot_launch_button is None) or isinstance(self.slot_launch_button, ButtonElement))
        if self.slot_launch_button is not None:
            self.slot_launch_button.add_value_listener(self._slot_launch_value)
        self.update()

    def unset_slot_launch_button(self):
        """
        Unset the button to launch the selected clip slot.
        """
        if self.slot_launch_button is not None:
            self.slot_launch_button.remove_value_listener(self._slot_launch_value)
            self.update()

    def _slot_launch_value(self, value: int):
        """
        Launch the selected clip slot (value have to be not 0).
        """
        assert (value in range(128))
        if self.is_enabled() and value > 0 and self.song().view.highlighted_clip_slot is not None:
            self.song().view.highlighted_clip_slot.fire()
