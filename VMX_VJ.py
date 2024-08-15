from __future__ import with_statement
# import Live
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
from .MenuManager import MenuManager, SpecialMenuComponent
from .MIDI_Map import *


# MIDI_NOTE_TYPE = 0
# MIDI_CC_TYPE = 1
# MIDI_PB_TYPE = 2


class VMX_VJ(ControlSurface):
    __doc__ = " Script for VMX VJ with correct dip switch "

    _active_instances = []

    def _combine_active_instances():
        """ Static method to set up new instances of the device """
        track_offset = 0
        scene_offset = 0
        for instance in VMX_VJ._active_instances:
            instance.activate_combination_mode(track_offset, scene_offset)
            track_offset += instance.session.width()

    _combine_active_instances = staticmethod(_combine_active_instances)

    def __init__(self, c_instance):
        """ Initialize the VMX VJ script """
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
            self.menu_manager = MenuManager(self._note_map, self._ctrl_map)
            self._setup_menu_control()
            self._setup_mixer_control()
            self._setup_device_and_transport_control()
            self._setup_session_control()  # Set up the session control. The order of execution is important!
            self.set_highlighting_session_component(self.session)
            # self.set_suppress_rebuild_requests(False)
            self.menu_manager.activate_menu("default")
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
        if self not in VMX_VJ._active_instances:
            VMX_VJ._active_instances.append(self)
            VMX_VJ._combine_active_instances()

    def _do_uncombine(self):
        if (self in VMX_VJ._active_instances) and VMX_VJ._active_instances.remove(self):
            self.session.unlink()
            VMX_VJ._combine_active_instances()

    def activate_combination_mode(self, track_offset, scene_offset):
        if TRACK_OFFSET != -1:
            track_offset = TRACK_OFFSET
        if SCENE_OFFSET != -1:
            scene_offset = SCENE_OFFSET
        self.session.link_with_track_offset(track_offset, scene_offset)

    def _setup_menu_control(self):
        """
        Setup menu master and menus
        """
        self.menu_manager.name = 'Menu_Manager'
        self.menu_manager.add_menu(SpecialMenuComponent("default"))
        self.menu_manager.add_menu(SpecialMenuComponent("default_mixer_0", True))
        self.menu_manager.add_menu(SpecialMenuComponent("default_mixer_1", True))
        self.menu_manager.add_menu(SpecialMenuComponent("default_mixer_2", True))
        self.menu_manager.add_menu(SpecialMenuComponent("default_mixer_3", True))
        self.menu_manager.add_opposite(["default_mixer_0", "default_mixer_1", "default_mixer_2", "default_mixer_3"])
        self.menu_manager.set_button("default_mixer_0", self._note_map[81])
        self.menu_manager.set_button("default_mixer_1", self._note_map[71])
        self.menu_manager.set_button("default_mixer_2", self._note_map[61])
        self.menu_manager.set_button("default_mixer_3", self._note_map[51])

    def _setup_mixer_control(self):
        """
        Setup settings related to SpecialMixerComponent
        """
        self._mixer = SpecialMixerComponent(TSB_Y, TSB_X)  # Initialize the component (extended from _Framework.MixerComponent)
        self._mixer.name = 'Mixer'
        self._mixer.master_strip().name = 'Master_Channel_Strip'
        # self._mixer.master_strip().set_select_button(self._note_map[MASTERSEL])
        # self.menu_manager.add_binds_to_menu("default", self._mixer.master_strip().set_select_button, self._mixer.master_strip().set_select_button, self._note_map[MASTERSEL])
        self._mixer.selected_strip().name = 'Selected_Channel_Strip'
        # self._mixer.set_crossfader_control(self._ctrl_map[CROSSFADER1])
        # self.menu_manager.add_binds_to_menu("default", self._mixer.set_crossfader_control, self._mixer.set_crossfader_control, self._ctrl_map[CROSSFADER1])
        # self._mixer.set_prehear_volume_control(self._ctrl_map[CUELEVEL])
        # self.menu_manager.add_binds_to_menu("default", self._mixer.set_prehear_volume_control, self._mixer.set_prehear_volume_control, self._ctrl_map[CUELEVEL])
        # self._mixer.master_strip().set_volume_control(self._ctrl_map[MASTERVOLUME])
        # self.menu_manager.add_binds_to_menu("default", self._mixer.set_volume_control, self._mixer.set_volume_control, self._ctrl_map[MASTERVOLUME])
        # self._mixer.selected_strip().set_arm_button(self._note_map[SELTRACKREC])
        # self.menu_manager.add_binds_to_menu("default", self._mixer.set_arm_button, self._mixer.set_arm_button, self._ctrl_map[SELTRACKREC])
        # self._mixer.selected_strip().set_solo_button(self._note_map[SELTRACKSOLO])
        # self.menu_manager.add_binds_to_menu("default", self._mixer.set_solo_button, self._mixer.set_solo_button, self._ctrl_map[SELTRACKSOLO])
        # self._mixer.selected_strip().set_mute_button(self._note_map[SELTRACKMUTE])
        # self.menu_manager.add_binds_to_menu("default", self._mixer.set_mute_button, self._mixer.set_mute_button, self._ctrl_map[SELTRACKMUTE])
        for track in range(TSB_X):
            strip = self._mixer.channel_strip(track)
            strip.name = 'Channel_Strip_' + str(track)
            self.menu_manager.add_binds_to_menu("default", strip.set_select_button, strip.set_select_button,
                                                self._note_map[TRACKSEL[track]])
            self.menu_manager.add_binds_to_menu("default", strip.set_volume_control, strip.set_volume_control,
                                                self._ctrl_map[TRACKVOL[track]])
            self.menu_manager.add_binds_to_menu("default_mixer_1", strip.set_arm_button, strip.set_arm_button,
                                                self._note_map[TRACKREC[track]])
            self.menu_manager.add_binds_to_menu("default_mixer_2", strip.set_mute_button, strip.set_mute_button,
                                                self._note_map[TRACKMUTE[track]])
            self.menu_manager.add_binds_to_menu("default_mixer_3", strip.set_solo_button, strip.set_solo_button,
                                                self._note_map[TRACKSOLO[track]])
            # # strip.set_mute_button(self._note_map[TRACKMUTE[track]])
            # self.menu_manager.add_binds_to_menu("default_mixer_3", strip.set_, strip.set_, self._note_map[TRACKREC[track]])  # Have to do something for stopping the thing
            # strip.set_pan_control(self._ctrl_map[TRACKPAN[track]])
            # strip.set_send_controls((self._ctrl_map[TRACKSENDA[track]], self._ctrl_map[TRACKSENDB[track]], self._ctrl_map[TRACKSENDC[track]]))
            strip.set_invert_mute_feedback(True)

    def _setup_device_and_transport_control(self):
        """
        Setup settings related to DeviceComponent and SpecialTransportComponent
        """
        self._device = DeviceComponent()
        self._device.name = 'Device_Component'
        device_bank_buttons = []
        device_param_controls = []
        for index in range(8):  # Bank and parameters setup (unused)
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
        self._transport.time_button = self._jog_wheel
        self.menu_manager.add_binds_to_menu("default", self._transport.set_play_button, self._transport.set_play_button,
                                            self._note_map[PLAY])
        self.menu_manager.add_binds_to_menu("default", self._transport.set_stop_button, self._transport.set_stop_button,
                                            self._note_map[STOP])
        # self._transport.set_record_button(self._note_map[REC])
        # self.menu_manager.add_binds_to_menu("default", self._transport.set_record_button, self._transport.set_record_button, self._note_map[REC])
        # self._transport.set_nudge_buttons(self._note_map[NUDGEUP], self._note_map[NUDGEDOWN])
        # self.menu_manager.add_binds_to_menu("default", self._transport.set_nudge_buttons, self._transport.set_nudge_buttons, self._note_map[NUDGEUP])
        # self._transport.set_undo_button(self._note_map[UNDO])
        # self.menu_manager.add_binds_to_menu("default", self._transport.set_undo_button, self._transport.set_undo_button, self._note_map[UNDO])
        # self._transport.set_redo_button(self._note_map[REDO])
        # self.menu_manager.add_binds_to_menu("default", self._transport.set_redo_button, self._transport.set_redo_button, self._note_map[REDO])
        # self._transport.set_tap_tempo_button(self._note_map[TAPTEMPO])
        # self.menu_manager.add_binds_to_menu("default", self._transport.set_tap_tempo_button, self._transport.set_tap_tempo_button, self._note_map[TAPTEMPO])
        # self._transport.set_quant_toggle_button(self._note_map[RECQUANT])
        # self.menu_manager.add_binds_to_menu("default", self._transport.set_quant_toggle_button, self._transport.set_quant_toggle_button, self._note_map[RECQUANT])
        # self._transport.set_overdub_button(self._note_map[OVERDUB])
        # self.menu_manager.add_binds_to_menu("default", self._transport.set_overdub_button, self._transport.set_overdub_button, self._note_map[OVERDUB])
        # self._transport.set_metronome_button(self._note_map[METRONOME])
        # self.menu_manager.add_binds_to_menu("default", self._transport.set_metronome_button, self._transport.set_metronome_button, self._note_map[METRONOME])
        # self._transport.set_tempo_control(self._ctrl_map[TEMPOCONTROL])
        # self.menu_manager.add_binds_to_menu("default", self._transport.set_tempo_control, self._transport.set_tempo_control, self._ctrl_map[TEMPOCONTROL])
        # self._transport.set_loop_button(self._note_map[LOOP])
        # self.menu_manager.add_binds_to_menu("default", self._transport.set_loop_button, self._transport.set_loop_button, self._note_map[LOOP])
        # self._transport.set_seek_buttons(self._note_map[SEEKFWD], self._note_map[SEEKRWD])
        # self.menu_manager.add_binds_to_menu("default", self._transport.set_seek_buttons, self._transport.set_seek_buttons, self._note_map[SEEKFWD])
        # self._transport.set_punch_buttons(self._note_map[PUNCHIN], self._note_map[PUNCHOUT])
        # self.menu_manager.add_binds_to_menu("default", self._transport.set_punch_buttons, self._transport.set_punch_buttons, self._note_map[PUNCHIN])
        # self._transport.set_jog_wheel_time()
        self.menu_manager.add_binds_to_menu("default", self._transport.set_jog_wheel_time,
                                            self._transport.unbind_jog_wheel, None)

    def _setup_session_control(self):
        """
        Setup settings related to SpecialSessionComponent
        """
        self.session = SpecialSessionComponent(TSB_X, TSB_Y)  # Track selection box size (X,Y) (horizontal, vertical).
        self.session.name = 'Session_Control'
        self.session.set_track_bank_buttons(self._note_map[SESSIONRIGHT], self._note_map[SESSIONLEFT])
        self.session.set_scene_bank_buttons(self._note_map[SESSIONDOWN], self._note_map[SESSIONUP])
        self.session.set_select_buttons(self._note_map[SCENEDN], self._note_map[SCENEUP])
        self._scene_launch_buttons = [self._note_map[SCENELAUNCH[index]] for index in
                                      range(TSB_Y)]  # range(tsb_y) is the horizontal count for the track selection box
        self.session.set_stop_all_clips_button(self._note_map[STOPALLCLIPS])
        # self.session.set_stop_track_clip_buttons
        self.menu_manager.add_binds_to_menu("default_mixer_0", self.session.set_stop_all_clips_button, self.session.set_stop_all_clips_button, ([self._note_map[TRACKSTOP[index]] for index in range(TSB_X)]))
        self.session.selected_scene().name = 'Selected_Scene'
        self.session.selected_scene().set_launch_button(self._note_map[SELSCENELAUNCH])
        self.session.slot_launch_button = self._note_map[SELCLIPLAUNCH]
        for scene_index in range(TSB_Y):  # Setting up buttons for the 16x4 button matrix (starting with Y (horizontal / the scenes))
            button_row = []
            for track_index in range(TSB_X):  # (X (vertical / the tracks))
                button = self._note_map[CLIPNOTEMAP[scene_index][track_index]]
                button_row.append(button)
            self.session.clip_launch_buttons.append(button_row)
            self._mixer.clip_launch_buttons.append(button_row)
        self.session.setup_clip_launch()
        self.session.set_mixer(self._mixer)
        # self.session.deletion_manager()
        self._session_zoom = SpecialZoomingComponent(self.session)
        self._session_zoom.name = 'Session_Overview'
        self._session_zoom.set_nav_buttons(self._note_map[ZOOMUP], self._note_map[ZOOMDOWN], self._note_map[ZOOMLEFT],
                                           self._note_map[ZOOMRIGHT])
        # self._mixer.setup_track_deletion()

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
        """
        Load MIDI map.
        """
        for note in range(128):
            if note in TOGGLE_NOTES:  # The 16x4 matrix is toggle until I found out how to have it in push mode.
                is_momentary = False
            else:
                is_momentary = True
            button = ButtonElement(is_momentary, MESSAGETYPE, BUTTONCHANNEL, note)
            button.name = 'Note_' + str(note)
            self._note_map.append(button)

        self._note_map.append(None)  # Add None to the end of the list, selectable with [-1] (for un-attributed)
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

        self._jog_wheel = ButtonElement(False, MIDI_CC_TYPE, 5, 101)
        self._jog_wheel.name = 'Jog_Wheel'
