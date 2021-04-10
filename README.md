# DDLC-OSTPlayer
A heavily revamped version of Nikso's Soundtrack Player for DDLC. <u>Current Version:</u> [**1.32**](https://github.com/GanstaKingofSA/DDLC-OSTPlayer/releases/latest)

![Sample preview](assets/screenshot0005.png)

**DISCLAIMER:** This is not afiliated or endorsed by Team Salvato or Nikso. The Scattered Stars Logo in `Wake Up Unchanged` is not free to use, but is only allowed in this build as a showcase to the soundtrack player. If you plan to use this, please remove it in your final build.

> Music Disclaimer: All songs featured are owned by the developer either digitally or in CD format and are not included in DDLC-OSTPlayer. (Shoo UMG, SME and all other major labels.)

## Credits
* Nikso - Original Developer
* Sam Kujo#9403 - Original Design and Beta Tester
* Staryxz#3613 - Original Beta Tester
* PabloLuaxerc#1719 - Artist of `Wake Up Unchanged`
* Tom Rothamel - Ren'Py SDK Style Code
* RyzekNoavek#0624 - Adjustable Play Bar Code
* khaase (Pixabay) - Refresh Icon
* eugenialcala (Pixabay) - Replay Icon
* raphaelsilva (Pixabay) - Shuffle Icon
* Weiss Schnee - Support (Weiss :D)

## What does this do?
This allows anyone to play the mod soundtrack outside of the mod itself and sideload songs to be played alongside it.

## What does this version improve on?
- Ability to play MP3's.
- Improved music player aesthetic.
- Dynamic title and font size changes (sort of) and cover art scaling (no need to descale art to 350x350).
- Song metadata support.
- Sideload songs from your playlist to be played with the mod's tracks.
- Forward and Rewind back a song in progress.
- Refresh Song List Support.
- Sorting from within the player.
- Loop/Shuffle Support
- Automatically jumps to the next song after current song has ended.

## What do I need to do to install this?
1. Copy of DDLC (New Blank Copy from [DDLC.moe](https://ddlc.moe)
2. This ZIP [file](https://github.com/GanstaKingofSA/DDLC-OSTPlayer/releases/latest) with the `game` folder inside.

**Note:** If you already have Nikso's Audio Player installed and are upgrading to this one, copy the ZIP contents from the game folder to your mod's game folder **and** delete the `audio_player.rpy` file from within within `mod_assets`. 

3. **(Optional)** Custom Music in a folder called `track` in the `game` folder
    * You can change this folder name or path to something else if you like. If you plan to do so, replace the phrase `track` to something else.
    > Do let people knowing that you changed it if they want to sideload songs to it.

4. Drop all the contents in this ZIP file to the base folder where DDLC.exe/DDLC.sh is.
> If you are on MacOS/OS X, you must right-click DDLC.app and click `Show Package Contents` then navigate to `Contents/Resources/autorun` and drop the ZIP file contents in there.

5. Copy this line to screens.rpy under lines `443-478` and restart DDLC.

```python
if main_menu:
    textbutton _("OST Player") action [Show("music_player"), SetMute("music", True), SetMute("music_player_mixer", False), SetVariable("current_soundtrack", False), If(renpy.game.preferences.mute.get("music", False), true=SetVariable("music_was_muted_before_soundtrack_player_opened", True), false=SetVariable("music_was_muted_before_soundtrack_player_opened", False)), Function(refresh_list)]
```

## Can I still define songs the old way?
Yes you can. The old format still works, **however** you must add this line after defining it.
```
manualDefineList.append(Wake_Up_Unchanged) # change Wake_Up_Unchanged to your song variable
```
This is done so it can be added with other songs in the `track` folder.

## How do I priortize a song or make a song the first one?
Set organizePriority to True and set the song priority by a value. 0 is the highest priority you can make a song be while 1, 2, etc. will be prioritzed lower in the list. i.e. `0 > 1 > 2 > ...`

## How do I organize the list alphabetically?
Turn on the A-Z Priority in the music player when playing a song or default it on, by setting `organizeAZ` to True.

## Can the organizations work together?
Yes. See the following organization images below.

* [Priority Organization](assets/screenshot0006.png)
* [A-Z Organization](assets/screenshot0007.png)
* [A-Z and Priority Organization](assets/screenshot0008.png)

## Why is there a file called `tinytag.py` in `python-packages`?
This handles the metadata of songs sideloaded or those that have metadata in the game.

## How do I add metadata info?
Right-click your song, Select Properties -> Details, and fill the blank boxes you can.
Alternatively, use [MusicBee](https://www.getmusicbee.com/) or a similar music player, or [MusicBrainz Picard](https://picard.musicbrainz.org/) and find your song.
  * For MusicBee: Right-Click your song within the player, select `Edit` and edit away the info you want, then click `Apply` then `OK`.
  * For MusicBrainz Picard: Add your song to Picard, select it, right-click the rectangle box that has 3 columns, select `Add New Tag`, select the tags you want to add like `Title`, `Artist`, `Comment`, `Album`, etc. There should be a blank box in the box area below, double-click it and edit away the info you want to add, then click `Save` and press the `Save` button near `Info`.

## Why did you do this?
Cause I was bored and wanted to see RWBY songs play within DDLC and see song covers displayed. (Yang *:P*)
