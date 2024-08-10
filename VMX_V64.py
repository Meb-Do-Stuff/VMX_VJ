from __future__ import with_statement
import Live
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import *
from _Framework.SliderElement import SliderElement
from _Framework.ButtonElement import ButtonElement
# from _Framework.ButtonMatrixElement import ButtonMatrixElement
# from _Framework.ChannelStripComponent import ChannelStripComponent
from _Framework.DeviceComponent import DeviceComponent
# from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
# from _Framework.SessionZoomingComponent import SessionZoomingComponent
from .SpecialMixerComponent import SpecialMixerComponent
from .SpecialTransportComponent import SpecialTransportComponent
from .SpecialSessionComponent import SpecialSessionComponent
from .SpecialZoomingComponent import SpecialZoomingComponent
from .SpecialViewControllerComponent import DetailViewControllerComponent
from .MIDI_Map import *


# MIDI_NOTE_TYPE = 0
# MIDI_CC_TYPE = 1
# MIDI_PB_TYPE = 2


class VMX_V64(ControlSurface):
    __doc__ = " Script for VMX V64 with correct dip switch "

    _active_instances = []

    def _combine_active_instances():
        """ Static method to set up new instances of the device """
        track_offset = 0
        scene_offset = 0
        for instance in VMX_V64._active_instances:
            instance.activate_combination_mode(track_offset, scene_offset)
            track_offset += instance.session.width()

    _combine_active_instances = staticmethod(_combine_active_instances)

    def __init__(self, c_instance):
        """ Initialize the VMX V64 script """
        ControlSurface.__init__(self, c_instance)
        # self.set_suppress_rebuild_requests(True)
        with self.component_guard():
            self._note_map = []  # Prepare CC note (buttons) map
            self._ctrl_map = []  # Prepare CC control (faders) map
            self._menu_map = []  # Prepare menu map (the 8 buttons on the bottom part)
            self._jog_wheel = None  # Prepare the jog as a button (because it's either 127 in one direction or 0 in the other (so like a button))
            self._session_zoom = None
            self._mixer = None
            self._transport = None
            self.session = None
            self._load_MIDI_map()
            self._setup_mixer_control()
            self._setup_device_and_transport_control()
            self._setup_session_control()  # Set up the session control. The order of execution is important!
            self.set_highlighting_session_component(self.session)
            # self.set_suppress_rebuild_requests(False)
        self._pads = []  # Drum pads (future use?)
        self._load_pad_translations()
        self._do_combine()

    def disconnect(self):
        """
        Reset when the device is disconnected
        """
        self._note_map = None
        self._ctrl_map = None
        self._menu_map = None
        self._jog_wheel = None
        self._do_uncombine()
        self._session_zoom = None
        self._mixer = None
        self._transport = None
        self.session = None
        self._pads = None
        ControlSurface.disconnect(self)

    def _do_combine(self):
        if self not in VMX_V64._active_instances:
            VMX_V64._active_instances.append(self)
            VMX_V64._combine_active_instances()

    def _do_uncombine(self):
        if (self in VMX_V64._active_instances) and VMX_V64._active_instances.remove(self):
            self.session.unlink()
            VMX_V64._combine_active_instances()

    def activate_combination_mode(self, track_offset, scene_offset):
        if TRACK_OFFSET != -1:
            track_offset = TRACK_OFFSET
        if SCENE_OFFSET != -1:
            scene_offset = SCENE_OFFSET
        self.session.link_with_track_offset(track_offset, scene_offset)

    def _setup_mixer_control(self):
        """
        Setup settings related to SpecialMixerComponent
        """
        self._mixer = SpecialMixerComponent(TSB_Y, TSB_X, self._note_map[SESSIONLEFT], self._note_map[SESSIONRIGHT], self._jog_wheel)  # Initialize the component (extended from _Framework.MixerComponent)
        self._mixer.name = 'Mixer'
        self._mixer.master_strip().name = 'Master_Channel_Strip'
        self._mixer.master_strip().set_select_button(self._note_map[MASTERSEL])
        self._mixer.selected_strip().name = 'Selected_Channel_Strip'
        self._mixer.prepare_crossfader_control(self._ctrl_map[CROSSFADER1])
        self._mixer.prepare_prehear_volume_control(self._ctrl_map[CUELEVEL])
        self._mixer.setup_crossfader_binding_button(self._note_map[70])
        self._mixer.master_strip().set_volume_control(self._ctrl_map[MASTERVOLUME])
        self._mixer.selected_strip().set_arm_button(self._note_map[SELTRACKREC])
        self._mixer.selected_strip().set_solo_button(self._note_map[SELTRACKSOLO])
        self._mixer.selected_strip().set_mute_button(self._note_map[SELTRACKMUTE])
        self._mixer.volumes_faders = [self._ctrl_map[TRACKVOL[index]] for index in
                                      range(int(TSB_X / 2))]  # range(tsb_x) (because only 8 faders over 16 tracks)
        self._mixer.send_a = [self._ctrl_map[TRACKSENDA[index]] for index in range(TSB_X)]
        self._mixer.send_b = [self._ctrl_map[TRACKSENDB[index]] for index in range(TSB_X)]
        self._mixer.delete_button = self._note_map[DELETE]

    def _setup_session_control(self):
        self.session = SpecialSessionComponent(TSB_X, TSB_Y, self._menu_map, self._mixer,
                                               self._transport)  # Track selection box size (X,Y) (horizontal, vertical).
        self.session.name = 'Session_Control'
        self.session.session_down = self._note_map[SESSIONDOWN]
        self.session.session_up = self._note_map[SESSIONUP]
        self.session.session_left = self._note_map[SESSIONLEFT]
        self.session.session_right = self._note_map[SESSIONRIGHT]
        self.session.view_setup()
        self._track_stop_buttons = [self._note_map[TRACKSTOP[index]] for index in
                                    range(TSB_X)]  # range(tsb_x) Range value is the track selection
        self._scene_launch_buttons = [self._note_map[SCENELAUNCH[index]] for index in
                                      range(TSB_Y)]  # range(tsb_y) is the horizontal count for the track selection box
        self.session.set_stop_all_clips_button(self._note_map[STOPALLCLIPS])
        self.session.set_stop_track_clip_buttons(tuple(self._track_stop_buttons))
        self.session.selected_scene().name = 'Selected_Scene'
        self.session.selected_scene().set_launch_button(self._note_map[SELSCENELAUNCH])
        self.session.slot_launch_button = self._note_map[SELCLIPLAUNCH]
        self.session.delete_button = self._note_map[DELETE]
        for scene_index in range(TSB_Y):  # Setting up buttons for the 16x4 button matrix
            button_row = []
            for track_index in range(TSB_X):
                button = self._note_map[CLIPNOTEMAP[scene_index][track_index]]
                button_row.append(button)
            self.session.clip_launch_buttons.append(button_row)
            self._mixer.clip_launch_buttons.append(button_row)
        self.session.setup_clip_launch()
        self.session.deletion_manager()
        self._session_zoom = SpecialZoomingComponent(self.session)
        self._session_zoom.name = 'Session_Overview'
        self._session_zoom.set_nav_buttons(self._note_map[ZOOMUP], self._note_map[ZOOMDOWN], self._note_map[ZOOMLEFT],
                                           self._note_map[ZOOMRIGHT])
        self._mixer.session = self.session
        self._mixer.unbind_alt()
        self._mixer.setup_track_deletion()

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

        self._transport = SpecialTransportComponent()
        self._transport.name = 'Transport'
        self._transport.play_button = self._note_map[PLAY]
        self._transport.setup_play_button()
        self._transport.set_stop_button(self._note_map[STOP])
        self._transport.set_record_button(self._note_map[REC])
        self._transport.set_nudge_buttons(self._note_map[NUDGEUP], self._note_map[NUDGEDOWN])
        self._transport.set_undo_button(self._note_map[UNDO])
        self._transport.set_redo_button(self._note_map[REDO])
        self._transport.set_tap_tempo_button(self._note_map[TAPTEMPO])
        self._transport.set_quant_toggle_button(self._note_map[RECQUANT])
        self._transport.set_overdub_button(self._note_map[OVERDUB])
        self._transport.set_metronome_button(self._note_map[METRONOME])
        self._transport.set_tempo_control(self._ctrl_map[TEMPOCONTROL])
        self._transport.set_loop_button(self._note_map[LOOP])
        self._transport.set_seek_buttons(self._note_map[SEEKFWD], self._note_map[SEEKRWD])
        self._transport.set_punch_buttons(self._note_map[PUNCHIN], self._note_map[PUNCHOUT])
        self._transport.time_button = self._jog_wheel
        self._transport.set_jog_wheel_time()

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
            self._menu_map.append(self._note_map[
                                      note])  # First button of last row will be used to open the menu (IN CASE IT'S X*X BUTTONS GRID)

        self._jog_wheel = ButtonElement(False, MIDI_CC_TYPE, 0, 125)
        self._jog_wheel.name = 'Jog_Wheel'
