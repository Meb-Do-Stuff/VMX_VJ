import Live
from _Framework.TransportComponent import TransportComponent
from _Framework.ButtonElement import ButtonElement
from _Framework.EncoderElement import EncoderElement
from _Framework.SubjectSlot import subject_slot
from .MIDI_Map import TEMPO_TOP
from .MIDI_Map import TEMPO_BOTTOM


class SpecialTransportComponent(TransportComponent):
    __doc__ = ' TransportComponent that only uses certain buttons if a shift button is pressed '

    def __init__(self):
        TransportComponent.__init__(self)
        self._quant_toggle_button = None
        self._last_quant_value = Live.Song.RecordingQuantization.rec_q_eight
        self.song().add_midi_recording_quantization_listener(self._on_quantisation_changed)
        self._on_quantisation_changed()
        self._undo_button = None
        self._redo_button = None
        self._tempo_encoder_control = None
        self.time_button = None
        self.play_button = None
        # TEMPO_TOP = 300.0
        # TEMPO_BOTTOM = 40.0

    def disconnect(self):
        TransportComponent.disconnect(self)
        if self._quant_toggle_button is not None:
            self._quant_toggle_button.remove_value_listener(self._quant_toggle_value)
            self._quant_toggle_button = None
        self.song().remove_midi_recording_quantization_listener(self._on_quantisation_changed)
        if self._undo_button is not None:
            self._undo_button.remove_value_listener(self._undo_value)
            self._undo_button = None
        if self._redo_button is not None:
            self._redo_button.remove_value_listener(self._redo_value)
            self._redo_button = None
        if self._tempo_encoder_control is not None:
            self._tempo_encoder_control.remove_value_listener(self._tempo_encoder_value)
            self._tempo_encoder_control = None
        if self.time_button is not None:
            self.time_button.remove_value_listener(self._time_value)
            self.time_button = None

    def set_quant_toggle_button(self, button: ButtonElement):
        """
        Set the button to toggle the recording quantization
        """
        if self._quant_toggle_button != button:
            if self._quant_toggle_button is not None:
                self._quant_toggle_button.remove_value_listener(self._quant_toggle_value)
            self._quant_toggle_button = button
            if self._quant_toggle_button is not None:
                self._quant_toggle_button.add_value_listener(self._quant_toggle_value)
            self.update()

    def set_jog_wheel_time(self):
        """
        Hook jog to time control
        """
        if self.time_button is not None:
            self.time_button.add_value_listener(self._time_value)
        self.update()

    def _time_value(self, value):
        """
        Function to move the current song time, 1 is left, else it's right
        """
        assert (self.time_button is not None)
        if self.is_enabled():
            if value == 1:
                self._move_current_song_time(-1, 1)
            else:
                self._move_current_song_time(1, 1)

    def unbind_jog_wheel(self):
        """
        Bind jog wheel to time control
        """
        if self.time_button is not None:
            self.time_button.remove_value_listener(self._time_value)

    def _quant_toggle_value(self, value: int):
        """
        Toggle the recording quantization.
        Enable with value > 0, disable with value = 0.
        """
        assert (self._quant_toggle_button is not None)
        assert (value in range(128))
        assert (self._last_quant_value != Live.Song.RecordingQuantization.rec_q_no_q)
        if self.is_enabled():  # and (not self._shift_pressed):
            if (value != 0) or (not self._quant_toggle_button.is_momentary()):
                quant_value = self.song().midi_recording_quantization
                if quant_value != Live.Song.RecordingQuantization.rec_q_no_q:
                    self._last_quant_value = quant_value
                    self.song().midi_recording_quantization = Live.Song.RecordingQuantization.rec_q_no_q
                else:
                    self.song().midi_recording_quantization = self._last_quant_value

    def _on_quantisation_changed(self):
        """
        Update the quantisation button.
        """
        if self.is_enabled():
            quant_value = self.song().midi_recording_quantization
            quant_on = (quant_value != Live.Song.RecordingQuantization.rec_q_no_q)
            if quant_on:
                self._last_quant_value = quant_value
            if self._quant_toggle_button is not None:
                if quant_on:
                    self._quant_toggle_button.turn_on()
                else:
                    self._quant_toggle_button.turn_off()

    def set_undo_button(self, undo_button: ButtonElement):
        """
        Set the button to undo the last action.
        """
        assert isinstance(undo_button, (ButtonElement, type(None)))
        if undo_button != self._undo_button:
            if self._undo_button is not None:
                self._undo_button.remove_value_listener(self._undo_value)
            self._undo_button = undo_button
            if self._undo_button is not None:
                self._undo_button.add_value_listener(self._undo_value)
            self.update()

    def _undo_value(self, value: int):
        """
        Undo the last action.
        """
        assert (self._undo_button is not None)
        assert (value in range(128))
        if self.is_enabled():
            if (value != 0) or (not self._undo_button.is_momentary()):
                if self.song().can_undo:
                    self.song().undo()

    def set_redo_button(self, redo_button):
        """
        Set the button to redo the last action.
        """
        assert isinstance(redo_button, (ButtonElement, type(None)))
        if redo_button != self._redo_button:
            if self._redo_button is not None:
                self._redo_button.remove_value_listener(self._redo_value)
            self._redo_button = redo_button
            if self._redo_button is not None:
                self._redo_button.add_value_listener(self._redo_value)
            self.update()

    def _redo_value(self, value: int):
        """
        Redo the last action.
        """
        assert (self._redo_button is not None)
        assert (value in range(128))
        if self.is_enabled():
            if (value != 0) or (not self._redo_button.is_momentary()):
                if self.song().can_redo:
                    self.song().redo()

    def _tempo_encoder_value(self, value: int):
        """
        Change the tempo with the encoder.
        """
        assert (self._tempo_encoder_control is not None)
        assert (value in range(128))
        backwards = (value >= 64)
        step = 0.1
        if backwards:
            amount = (value - 128)
        else:
            amount = value
        tempo = max(20, min(999, (self.song().tempo + (amount * step))))
        self.song().tempo = tempo

    def set_tempo_encoder(self, control):
        assert ((control is None) or (isinstance(control, EncoderElement) and (
                control.message_map_mode() is Live.MidiMap.MapMode.relative_two_compliment)))
        if self._tempo_encoder_control is not None:
            self._tempo_encoder_control.remove_value_listener(self._tempo_encoder_value)
        self._tempo_encoder_control = control
        if self._tempo_encoder_control is not None:
            self._tempo_encoder_control.add_value_listener(self._tempo_encoder_value)
        self.update()

    @subject_slot('value')
    def _tempo_value(self, value):
        assert (self._tempo_control is not None)
        assert (value in range(128))
        if self.is_enabled():
            fraction = ((TEMPO_TOP - TEMPO_BOTTOM) / 127.0)
            self.song().tempo = ((fraction * value) + TEMPO_BOTTOM)

    def setup_play_button(self):
        """
        Bind play button to play the song.
        """
        self.set_play_button(self.play_button)

    def unbind_play_button(self):
        """
        Unbind play button from playing the song.
        """
        self.set_play_button(None)
