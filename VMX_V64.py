from __future__ import with_statement

import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import *
from _Framework.SliderElement import SliderElement
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ChannelStripComponent import ChannelStripComponent
from _Framework.DeviceComponent import DeviceComponent
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.SessionZoomingComponent import SessionZoomingComponent
from .SpecialMixerComponent import SpecialMixerComponent
from .SpecialTransportComponent import SpecialTransportComponent
from .SpecialSessionComponent import SpecialSessionComponent
from .SpecialZoomingComponent import SpecialZoomingComponent
from .SpecialViewControllerComponent import DetailViewControllerComponent
from .MIDI_Map import *


# MIDI_NOTE_TYPE = 0
# MIDI_CC_TYPE = 1
# MIDI_PB_TYPE = 2


class VMX_V64(ControlSurface):  # Make sure you update the name
    __doc__ = " Script for VMX V64 with correct dip switch "  # Make sure you update the name

    _active_instances = []

    def _combine_active_instances():
        track_offset = 0
        scene_offset = 0
        for instance in VMX_V64._active_instances:  # Make sure you update the name
            instance._activate_combination_mode(track_offset, scene_offset)
            track_offset += instance._session.width()

    _combine_active_instances = staticmethod(_combine_active_instances)

    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        # self.set_suppress_rebuild_requests(True)
        with self.component_guard():
            self._note_map = []
            self._ctrl_map = []
            self._menu_map = []
            self._load_MIDI_map()
            self._jog_wheel = None
            self._load_jog_wheel()
            self._session = None
            self._session_zoom = None
            self._mixer = None
            self._setup_session_control()
            self._setup_mixer_control()
            self._session.set_mixer(self._mixer)
            self._setup_device_and_transport_control()
            self.set_highlighting_session_component(self._session)
            # self.set_suppress_rebuild_requests(False)
        self._pads = []
        self._load_pad_translations()
        self._do_combine()

    def disconnect(self):
        self._note_map = None
        self._ctrl_map = None
        self._pads = None
        self._do_uncombine()
        self._shift_button = None
        self._session = None
        self._session_zoom = None
        self._mixer = None
        self._jog_wheel = None
        ControlSurface.disconnect(self)

    def _do_combine(self):
        if self not in VMX_V64._active_instances:
            VMX_V64._active_instances.append(self)
            VMX_V64._combine_active_instances()

    def _do_uncombine(self):
        if (self in VMX_V64._active_instances) and VMX_V64._active_instances.remove(
                self):  # Make sure you update the name
            self._session.unlink()
            VMX_V64._combine_active_instances()  # Make sure you update the name

    def _activate_combination_mode(self, track_offset, scene_offset):
        if TRACK_OFFSET != -1:
            track_offset = TRACK_OFFSET
        if SCENE_OFFSET != -1:
            scene_offset = SCENE_OFFSET
        self._session.link_with_track_offset(track_offset, scene_offset)

    def _setup_session_control(self):
        self._session = SpecialSessionComponent(TSB_X, TSB_Y,
                                                self._menu_map)  # Track selection box size (X,Y) (horizontal, vertical).
        self._session.name = 'Session_Control'
        self._session.set_track_bank_buttons(self._note_map[SESSIONRIGHT], self._note_map[SESSIONLEFT])
        self._session.set_scene_bank_buttons(self._note_map[SESSIONDOWN], self._note_map[SESSIONUP])
        self._session.set_select_buttons(self._note_map[SCENEDN], self._note_map[SCENEUP])
        # range(tsb_x) Range value is the track selection
        self._track_stop_buttons = [self._note_map[TRACKSTOP[index]] for index in range(TSB_X)]
        # range(tsb_y) is the horizontal count for the track selection box
        self._scene_launch_buttons = [self._note_map[SCENELAUNCH[index]] for index in range(TSB_Y)]
        self._session.set_stop_all_clips_button(self._note_map[STOPALLCLIPS])
        self._session.set_stop_track_clip_buttons(tuple(self._track_stop_buttons))
        self._session.selected_scene().name = 'Selected_Scene'
        self._session.selected_scene().set_launch_button(self._note_map[SELSCENELAUNCH])
        self._session.set_slot_launch_button(self._note_map[SELCLIPLAUNCH])
        for scene_index in range(TSB_Y):
            button_row = []
            for track_index in range(TSB_X):
                button = self._note_map[CLIPNOTEMAP[scene_index][track_index]]
                button_row.append(button)
            self._session.clip_launch_buttons.append(button_row)
        self._session.setup_clip_launch()
        self._session_zoom = SpecialZoomingComponent(self._session)
        self._session_zoom.name = 'Session_Overview'
        self._session_zoom.set_nav_buttons(self._note_map[ZOOMUP], self._note_map[ZOOMDOWN], self._note_map[ZOOMLEFT],
                                           self._note_map[ZOOMRIGHT])

    def _setup_mixer_control(self):
        self._mixer = SpecialMixerComponent(TSB_X)
        self._mixer.name = 'Mixer'
        self._mixer.master_strip().name = 'Master_Channel_Strip'
        self._mixer.master_strip().set_select_button(self._note_map[MASTERSEL])
        self._mixer.selected_strip().name = 'Selected_Channel_Strip'
        self._mixer.set_select_buttons(self._note_map[TRACKRIGHT], self._note_map[TRACKLEFT])
        self._mixer.set_crossfader_control(self._ctrl_map[CROSSFADER])
        self._mixer.set_prehear_volume_control(self._ctrl_map[CUELEVEL])
        self._mixer.master_strip().set_volume_control(self._ctrl_map[MASTERVOLUME])
        self._mixer.selected_strip().set_arm_button(self._note_map[SELTRACKREC])
        self._mixer.selected_strip().set_solo_button(self._note_map[SELTRACKSOLO])
        self._mixer.selected_strip().set_mute_button(self._note_map[SELTRACKMUTE])
        for track in range(TSB_X):
            # My guess is that altering the range here will allow you to alter the range of mixer tracks
            # So if you had a 16 fader mixer, this would come in handy.
            strip = self._mixer.channel_strip(track)
            strip.name = 'Channel_Strip_' + str(track)
            strip.set_arm_button(self._note_map[TRACKREC[track]])
            strip.set_solo_button(self._note_map[TRACKSOLO[track]])
            strip.set_mute_button(self._note_map[TRACKMUTE[track]])
            strip.set_select_button(self._note_map[TRACKSEL[track]])
            strip.set_volume_control(self._ctrl_map[TRACKVOL[track]])
            strip.set_pan_control(self._ctrl_map[TRACKPAN[track]])
            strip.set_send_controls((self._ctrl_map[TRACKSENDA[track]], self._ctrl_map[TRACKSENDB[track]],
                                     self._ctrl_map[TRACKSENDC[track]]))
            strip.set_invert_mute_feedback(True)

    def _setup_device_and_transport_control(self):
        self._device = DeviceComponent()
        self._device.name = 'Device_Component'
        device_bank_buttons = []
        device_param_controls = []
        for index in range(8):
            device_param_controls.append(self._ctrl_map[PARAMCONTROL[index]])
            device_bank_buttons.append(self._note_map[DEVICEBANK[index]])
        if None not in device_bank_buttons:
            self._device.set_bank_buttons(tuple(device_bank_buttons))
        if None not in device_param_controls:
            self._device.set_parameter_controls(tuple(device_param_controls))
        self._device.set_on_off_button(self._note_map[DEVICEONOFF])
        self._device.set_bank_nav_buttons(self._note_map[DEVICEBANKNAVLEFT], self._note_map[DEVICEBANKNAVRIGHT])
        self._device.set_lock_button(self._note_map[DEVICELOCK])
        self.set_device_component(self._device)

        detail_view_toggler = DetailViewControllerComponent()
        detail_view_toggler.name = 'Detail_View_Control'
        detail_view_toggler.set_device_clip_toggle_button(self._note_map[CLIPTRACKVIEW])
        detail_view_toggler.set_detail_toggle_button(self._note_map[DETAILVIEW])
        detail_view_toggler.set_device_nav_buttons(self._note_map[DEVICENAVLEFT], self._note_map[DEVICENAVRIGHT])

        transport = SpecialTransportComponent()
        transport.name = 'Transport'
        transport.set_play_button(self._note_map[PLAY])
        transport.set_stop_button(self._note_map[STOP])
        transport.set_record_button(self._note_map[REC])
        transport.set_nudge_buttons(self._note_map[NUDGEUP], self._note_map[NUDGEDOWN])
        transport.set_undo_button(self._note_map[UNDO])
        transport.set_redo_button(self._note_map[REDO])
        transport.set_tap_tempo_button(self._note_map[TAPTEMPO])
        transport.set_quant_toggle_button(self._note_map[RECQUANT])
        transport.set_overdub_button(self._note_map[OVERDUB])
        transport.set_metronome_button(self._note_map[METRONOME])
        transport.set_tempo_control(self._ctrl_map[TEMPOCONTROL])
        transport.set_loop_button(self._note_map[LOOP])
        transport.set_seek_buttons(self._note_map[SEEKFWD], self._note_map[SEEKRWD])
        transport.set_punch_buttons(self._note_map[PUNCHIN], self._note_map[PUNCHOUT])
        transport.set_time(self._jog_wheel)

    def _on_selected_track_changed(self):
        ControlSurface._on_selected_track_changed(self)
        track = self.song().view.selected_track
        device_to_select = track.view.selected_device
        if device_to_select is None and len(track.devices) > 0:
            device_to_select = track.devices[0]
        if device_to_select is not None:
            self.song().view.select_device(device_to_select)
        self._device_component.set_device(device_to_select)

    def _load_pad_translations(self):
        if -1 not in DRUM_PADS:
            pad = []
            for row in range(4):
                for col in range(4):
                    pad = (col, row, DRUM_PADS[row * 4 + col], PADCHANNEL,)
                    self._pads.append(pad)
            self.set_pad_translations(tuple(self._pads))

    def _load_MIDI_map(self):
        for note in range(128):
            if note <= 64:
                is_momentary = False
            else:
                is_momentary = True
            button = ButtonElement(is_momentary, MESSAGETYPE, BUTTONCHANNEL, note)
            button.name = 'Note_' + str(note)
            self._note_map.append(button)

        self._note_map.append(None)  # add None to the end of the list, selectable with [-1]
        if MESSAGETYPE == MIDI_CC_TYPE and BUTTONCHANNEL == SLIDERCHANNEL:
            for ctrl in range(128):
                self._ctrl_map.append(None)
        else:
            for ctrl in range(128):
                control = SliderElement(MIDI_CC_TYPE, SLIDERCHANNEL, ctrl)
                control.name = 'Ctrl_' + str(ctrl)
                self._ctrl_map.append(control)
            self._ctrl_map.append(None)

        for note in MENUBUTTONS:
            self._menu_map.append(self._note_map[note])  # First button of last row will be used to open the menu (IN CASE IT'S X*X BUTTONS GRID)

    def _load_jog_wheel(self):
        self._jog_wheel = ButtonElement(False, MIDI_CC_TYPE, 0, 125)
        self._jog_wheel.name = 'Jog_Wheel'
