# Logbook!

---

*Here go my logs*

## Origin

While lurking online, searching for some cool MIDI equipment to use with software like Ableton, I found the brand [Codanova](http://codanova.over-blog.com/), which closed in 2012.<br>
Before that, this brand had released a bunch of devices.<br> I managed to get two of them: a [Codanova VMX V64](http://codanova.over-blog.com/article-new-prototype-midi-controller-codanova-vmx-v64-50855556.html) and a [VMX VJ](http://codanova-fr.over-blog.com/article-27262311.html).<br>
Their integration with Ableton is quite poor, and you have to map everything manually each time, which is kinda annoying.<br>
My goal is to create surface controls, so it can auto-map itself and do even better stuff.

## Base Knowledge & Finding Resources

#### I just achieved a surface control for the VMX V64, so a lot of my work will be based on that.

Surface controls are Python scripts used by Ableton to turn random MIDI controllers into war machines.<br>
<br>Resources:<br>
[Ableton 12 Other Surface Controls](https://github.com/gluon/AbletonLive12_MIDIRemoteScripts)<br>
[Live Module Functions](https://structure-void.com/PythonLiveAPI_documentation/Live11.0.xml)<br>
[_Framework Module Documentation](https://structure-void.com/AbletonLiveRemoteScripts_Docs/_Framework/)<br>
[Manual for the VMX VJ](https://www.manualslib.fr/manual/447662/Coda-Audio-Vmx-Vj.html?page=13)

To start with, I'll use [my VMX V64 Control Surface](https://github.com/Meb-Do-Stuff/VMX_V64) as a base (based on [Laidlaw42's Custom MIDI Remote Script repo](https://github.com/laidlaw42/ableton-live-midi-remote-scripts)).

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

## Goals & achievements

As said above, I worked a lot on my VMX V64 control surface before moving on on this project.<br>
I want to have move functions. While the V64 have 2 menus (the ALT mode and Scene mode), I want this one to be full of menus and sub-menus, to do everything.
So that's what I spent the most time on for this one.<br>
For now, only the default menu is working (that let you manage volume and tons of stuff for 8 tracks).<br>
Next menu I'm working on is for an EQ8 (Equalizer) controllable with the faders.<br>
Though, I'm having a problem at the moment with working on that, so I have to figure out a way to do that.<br>
Still in WIP, if you want to see how it would look like as a final result, look at my VMX V64 support.

---

Moral support:<br>
[Max Cooper's Boiler Room](https://soundcloud.com/platform/max-cooper?si=8238550d7a3144bcaceca196e514521c&utm_source=clipboard&utm_medium=text&utm_campaign=social_sharing)<br>
[David August's Boiler Room](https://soundcloud.com/platform/david-august?si=6f764d61632349fcb5e680b10d23418d&utm_source=clipboard&utm_medium=text&utm_campaign=social_sharing)<br>
[David August's Innervisions #50 LIVE Podcast](https://soundcloud.com/davidaugust/innervisions-50-live-podcast?si=6fd98977e3b647429ca6c9d1a45be392&utm_source=clipboard&utm_medium=text&utm_campaign=social_sharing)<br>
[Rimarkable's Boiler Room](https://youtu.be/hoyCaeT_tuo)<br>
[Four Tet's Boiler Room](https://www.youtube.com/watch?v=Ca6pjR2TLns)<br>
[Sweet Valley single *So Serene*](https://open.spotify.com/intl-fr/album/3VM5KHTGJAVkbFc1tkDTHG)<br>
[White Birds *When Women Played Drums*](https://open.spotify.com/intl-fr/album/0pjKENinrmO6cBGplZIEfS)<br>
[Bryan Deister *Into the Sky*](https://open.spotify.com/intl-fr/track/1nNKZconhkdmqQxbi52lOM?si=8dc37bf1cdad4696)<br>
