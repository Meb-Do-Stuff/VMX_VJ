# Logbook!

---

*Here go my logs*

## Origin

While lurking online, searching for some cool MIDI equipment to use with software like Ableton, I found the brand [Codanova](http://codanova.over-blog.com/), which closed in 2012.<br>
Before that, this brand had released a bunch of devices.<br> I managed to get *two*: a [Codanova VMX V64](http://codanova.over-blog.com/article-new-prototype-midi-controller-codanova-vmx-v64-50855556.html) and a [VMX VJ](http://codanova-fr.over-blog.com/article-27262311.html).<br>
Their integration with Ableton is quite poor, and you have to map everything manually each time, which is kinda annoying.<br>
My goal is to create surface controls so it can auto-map itself and do even better stuff.

## Base Knowledge & Finding Resources

Surface controls are Python scripts used by Ableton to turn random MIDI controllers into war machines.<br>
<br>Resources:<br>
[Ableton 12 Other Surface Controls](https://github.com/gluon/AbletonLive12_MIDIRemoteScripts)<br>
[Live Module Functions](https://structure-void.com/PythonLiveAPI_documentation/Live11.0.xml)<br>
[_Framework Module Documentation](https://structure-void.com/AbletonLiveRemoteScripts_Docs/_Framework/)<br>
[Manual for the VMX V64](https://www.manualslib.com/manual/2817471/Codanova-Vmx-V-64.html)

To start with, I'll use [Laidlaw42's Custom MIDI Remote Script repo](https://github.com/laidlaw42/ableton-live-midi-remote-scripts) as a base.

I'll use [PyCharm](https://www.jetbrains.com/pycharm/), [MIDI Tools](https://mountainutilities.eu/miditools), [GIMP](https://www.gimp.org/), and [LibreOffice Draw](https://www.libreoffice.org/discover/draw/) (for now).<br>


**Usage of AI:** I've used AI such as GitHub Copilot to help with completing long lines of characters going in a logic way. *There are not enough ressources online about this to have Copilot working properly anyway.*<br>
*For example:*
```python
MENUBUTTONS = [
    65, 66, 73, 74,
    67, 68, 75, 76,
    69, 70, 77, 78,
    71, 72, 79, 80
]
```
ChatGPT has been used to correct typo errors and information about Ableton (such as what are banks, and can I have more crossfaders than one (the answer is no, but I thought of a way)).
## Step 1: Perfect Controller Settings!

The Codanova VMX V64 can be configured with Dip-Switches.

The first step is to fulfill the [MIDI_Map.py file](https://github.com/laidlaw42/ableton-live-midi-remote-scripts/blob/YourControllerName/YourControllerName%20-%20Live%2011/MIDI_Map.py).<br>
Since my controller is quite special, I'll probably take another path, but I have to do a mapping anyway.

<img src="https://github.com/Meb-Do-Stuff/Codanova-VMX-V64-Ableton-Surface-Control/blob/main/dipswitch.jpg?raw=true" height="200" alt="">

There is software to directly modify settings with the firmware, but this software seems broken (maybe for a future project).

## Step 2: MIDI Mapping

The first thing to do is to re-adapt this script that was made for an 8x8 controller to my 16x4.<br>
There are matrices of -1, and I'm quite sure that the wrong amount of -1 would generate an error.
It's now time to find the buttons and everything.

<img src="https://raw.githubusercontent.com/Meb-Do-Stuff/Codanova-VMX-V64-Ableton-Surface-Control/main/Map.png" height="500">
<br>Outputting is really weird, I'll try again later.

I managed to set the 16x4 buttons to launch clips, and the 16x2 knobs can manage the Send A & B, while the faders manage volume.<br>
The jog wheel can now manage time.<br>
I can now move the view with buttons 65 and 66 for up and down, and 67 and 68 for left and right.<br>
Play, Stop, Stop Clips, and Record with 80, 79, 78, and 77.<br>

## Step 3: Advanced Functions

I managed to create an ALT button that changes the first row of buttons to manage the selection of tracks.<br>
The second row of buttons can now manage the mute, the third solo, and the fourth arm of the selected track.<br>
The 16x2 knobs manage send C and pan in ALT mode.<br>
The 8 faders manage the 8 other volume tracks in ALT mode (since this device should manage 16 tracks).<br>
The jog wheel manages the master volume in ALT mode.<br>
The view buttons now manage the clip selection in ALT mode, and the play button (80) launches the currently selected clip in ALT mode.<br>
The first crossfader can now manage the crossfade, while the second one manages the Cue (preview) level.<br>
In scene mode, the first 15 buttons bind the track to crossfade A, the second remove the binding, and the third bind to crossfade B.<br>

## Now what?

I've pretty much managed to do everything I wanted to do with this controller.<br>
I'll now try to make it more user-friendly, and maybe add some more features, but I need to fix the firmware to have push buttons, and a better comprehension of the input/output.<br>

---

Moral support:<br>
[Max Cooper's Boiler Room](https://soundcloud.com/platform/max-cooper?si=8238550d7a3144bcaceca196e514521c&utm_source=clipboard&utm_medium=text&utm_campaign=social_sharing)<br>
[David August's Boiler Room](https://soundcloud.com/platform/david-august?si=6f764d61632349fcb5e680b10d23418d&utm_source=clipboard&utm_medium=text&utm_campaign=social_sharing)<br>
[David August's Innervisions #50 LIVE Podcast](https://soundcloud.com/davidaugust/innervisions-50-live-podcast?si=6fd98977e3b647429ca6c9d1a45be392&utm_source=clipboard&utm_medium=text&utm_campaign=social_sharing)<br>
[Rimarkable's Boiler Room](https://youtu.be/hoyCaeT_tuo)<br>
[Four Tet's Boiler Room](https://www.youtube.com/watch?v=Ca6pjR2TLns)<br>
[Sweet Valley single *So Serene*](https://open.spotify.com/intl-fr/album/3VM5KHTGJAVkbFc1tkDTHG)<br>
[White Birds *When Women Played Drums*](https://open.spotify.com/intl-fr/album/0pjKENinrmO6cBGplZIEfS)
