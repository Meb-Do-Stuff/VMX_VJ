# Combination Mode offsets
# ------------------------

TRACK_OFFSET = -1  # offset from the left of linked session origin; set to -1 for auto-joining of multiple instances
SCENE_OFFSET = 0  # offset from the top of linked session origin (no auto-join)

# Buttons / Pads
# -------------
# Valid Note/CC assignments are 0 to 127, or -1 for NONE
# Duplicate assignments are permitted

BUTTONCHANNEL = 2  # Channel assignment for all mapped buttons/pads; valid range is 0 to 15 ; 0=1, 1=2 etc.
MESSAGETYPE = 1  # Message type for buttons/pads; set to 0 for MIDI Notes, 1 for CCs.
# When using CCs for buttons/pads, set BUTTONCHANNEL and SLIDERCHANNEL to different values.


# Track selection box (aka that coloured box for scene/track launching)
TSB_X = 8  # Controls the vertical value for the track selection box. Default value is 8
TSB_Y = 4  # Controls the horizontal value for the track selection box. Default value is 8

# General
PLAY = 11  # Global play
STOP = 55  # Global stop
REC = -1  # Global record
DELETE = -1  # Delete selected clip
TAPTEMPO = -1  # Tap tempo
NUDGEUP = -1  # Tempo Nudge Up
NUDGEDOWN = -1  # Tempo Nudge Down
UNDO = -1  # Undo
REDO = -1  # Redo
LOOP = -1  # Loop on/off
PUNCHIN = -1  # Punch in
PUNCHOUT = -1  # Punch out
OVERDUB = -1  # Overdub on/off
METRONOME = -1  # Metronome on/off
RECQUANT = -1  # Record quantization on/off
DETAILVIEW = -1  # Detail view switch
CLIPTRACKVIEW = -1  # Clip/Track view switch

# Device Control
DEVICELOCK = -1  # Device Lock (lock "blue hand")
DEVICEONOFF = -1  # Device on/off
DEVICENAVLEFT = -1  # Device nav left
DEVICENAVRIGHT = -1  # Device nav right
DEVICEBANKNAVLEFT = -1  # Device bank nav left
DEVICEBANKNAVRIGHT = -1  # Device bank nav right
DEVICEBANK = tuple([-1] * 8)  # Device bank buttons

# Arrangement View Controls
SEEKFWD = -1  # Seek forward
SEEKRWD = -1  # Seek rewind

# Session Navigation
SESSIONLEFT = 45  # Session left
SESSIONRIGHT = 1  # Session right
SESSIONUP = 15  # Session up
SESSIONDOWN = 5  # Session down
ZOOMUP = -1  # Session Zoom up
ZOOMDOWN = -1  # Session Zoom down
ZOOMLEFT = -1  # Session Zoom left
ZOOMRIGHT = -1  # Session Zoom right

# Scene Navigation
SCENEUP = -1  # Scene down
SCENEDN = -1  # Scene up

# Scene Launch
SELSCENELAUNCH = -1  # Selected scene launch
SCENELAUNCH = tuple([-1] * 4)  # Scene launch buttons

# Clip Launch / Stop
SELCLIPLAUNCH = -1  # Selected clip launch
STOPALLCLIPS = -1  # Stop all clips

# 8x4 Matrix note assignments
CLIPNOTEMAP = tuple(tuple([[-1] * 8])*4)

# Track Control
MASTERSEL = -1  # Master track select
SELTRACKREC = -1  # Arm Selected Track
SELTRACKSOLO = -1  # Solo Selected Track
SELTRACKMUTE = -1  # Mute Selected Track

TRACKSTOP = tuple([-1] * 8)  # Track stop buttons
TRACKSEL = tuple([-1] * 8)  # Track select buttons
TRACKMUTE = tuple([-1] * 8)  # Track mute buttons
TRACKSOLO = tuple([-1] * 8)  # Track solo buttons
TRACKREC = tuple([-1] * 8)  # Track record arm buttons

# Pad Translations for Drum Rack
PADCHANNEL = 0  # MIDI channel for Drum Rack notes
DRUM_PADS = (-1, -1, -1, -1,  # MIDI note numbers for 4 x 4 Drum Rack
             -1, -1, -1, -1,  # Mapping will be disabled if any notes are set to -1
             -1, -1, -1, -1,  # Notes will be "swallowed" if already mapped elsewhere
             -1, -1, -1, -1,
             )

# Sliders / Knobs
# ---------------
# Valid CC assignments are 0 to 127, or -1 for NONE
# Duplicate assignments will be ignored
SLIDERCHANNEL = 0  # Channel assignment for all mapped CCs; valid range is 0 to 15
TEMPO_TOP = 180.0  # Upper limit of tempo control in BPM (max is 999)
TEMPO_BOTTOM = 100.0  # Lower limit of tempo control in BPM (min is 0)

TEMPOCONTROL = -1  # Tempo control CC assignment; control range is set above
MASTERVOLUME = -1  # Master track volume
CUELEVEL = -1  # Cue level control
CROSSFADER1 = -1  # Crossfader control

TRACKVOL = (28, 29, 30, 31, 27, 26, 25, 24)  # Track volume controls

TRACKPAN = tuple([-1] * 8)  # Track pan controls

TRACKSENDA = tuple([-1] * 8)  # Track send A controls

TRACKSENDB = tuple([-1] * 8)  # Track send B controls

TRACKSENDC = tuple([-1] * 8)  # Track send C controls

PARAMCONTROL = tuple([-1] * 8)  # Device control

# Custom Menu
# ----------
MENUBUTTONS = []  # Unused

TOGGLE_NOTES = []
