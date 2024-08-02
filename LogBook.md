# Logbook!

*Here goes my logs*

## Origin

While lurking around online, searching for some cool MIDI equipment to mess with softwares like Ableton, I found the brand [Codanova](http://codanova.over-blog.com/), which closed in 2012.<br>
Beforewards, this brand had released a bunch of devices.<br>I managed to get ~~1~~ *2*, a [Codanova VMX V64](http://codanova.over-blog.com/article-new-prototype-midi-controller-codanova-vmx-v64-50855556.html) *and a [VMX VJ](http://codanova-fr.over-blog.com/article-27262311.html)*.<br>
Their integrations with Ableton is quite poor, and you have to map everything manually each time, kinda annoying.<br>
My goal will be to create surface controls, so it can auto-map itself, and do even better stuff.

## Base knowledge & Finding ressources

Surface controls are Python scripts, that are used by Ableton to turn random Midi controllers, into war machines.<br>
<br>Ressources:<br>
[Ableton 12 other surface controls](https://github.com/gluon/AbletonLive12_MIDIRemoteScripts)<br>
[Live module functions](https://structure-void.com/PythonLiveAPI_documentation/Live11.0.xml)<br>
[_framework module documentation](https://structure-void.com/AbletonLiveRemoteScripts_Docs/_Framework/)<br>
[Manuel of the VMX V64](https://www.manualslib.com/manual/2817471/Codanova-Vmx-V-64.html)

To start with, I'll use [Laidlaw42's Custom MIDI Remote Script repo](https://github.com/laidlaw42/ableton-live-midi-remote-scripts) as a base.


I'll use [PyCharm](https://www.jetbrains.com/pycharm/), [MIDI Tools](https://mountainutilities.eu/miditools), [GIMP](https://www.gimp.org/) and [LibreOffice Draw](https://www.libreoffice.org/discover/draw/) (for now).


## Step 1: Perfect Controller Settings!

The Codanova VMX V64 can be configured with Dip-Switches

First step is to fulfill the [MIDI_Map.py file](https://github.com/laidlaw42/ableton-live-midi-remote-scripts/blob/YourControllerName/YourControllerName%20-%20Live%2011/MIDI_Map.py).<br>
Since my controller is quite special, I'll probably take another path, but I have to do a mapping anyway.

<img src="https://github.com/Meb-Do-Stuff/Codanova-VMX-V64-Ableton-Surface-Control/blob/main/dipswitch.jpg?raw=true" height="200">

There is a software to directly modify settings with the firmware, but this software looks broken (maybe for a future project).

## Step 2: MIDI Mapping

First thing to do is the re-adapt this script that was made for an 8x8 controller, to my 16x4.<br>
There are matrix of -1, and I'm quite sure that the wrong amount of -1 would generate an error.
It's now time to find buttons and everything.

<img src="https://raw.githubusercontent.com/Meb-Do-Stuff/Codanova-VMX-V64-Ableton-Surface-Control/main/Map.png" height="500">
Outputing is really weird, I'll try again later.

---

Moral support:<br>
[Max Cooper's Boiler Room](https://soundcloud.com/platform/max-cooper?si=8238550d7a3144bcaceca196e514521c&utm_source=clipboard&utm_medium=text&utm_campaign=social_sharing)<br>
[David August's Boiler Room](https://soundcloud.com/platform/david-august?si=6f764d61632349fcb5e680b10d23418d&utm_source=clipboard&utm_medium=text&utm_campaign=social_sharing)
