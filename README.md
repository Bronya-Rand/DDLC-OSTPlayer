# DDLC-OSTPlayer

A heavily revamped version of Nikso's Soundtrack Player for DDLC. <u>Current Version:</u> [**1.34**](https://github.com/GanstaKingofSA/DDLC-OSTPlayer/releases/latest)

<img src="assets/screenshot0001.png" alt="New UI" width=420x> 
<img src="assets/screenshot0002.png" alt="Old UI" width=420x>

**DISCLAIMER:** This is not afiliated or endorsed by Team Salvato or Nikso. The Scattered Stars <u>Logo</u> in `Wake Up Unchanged` is not free to use, but is only allowed in this build as a display to the soundtrack player. If you plan to use this, remove it in your final build.

> All songs featured above are owned by the developer and are not included in DDLC-OSTPlayer. (Shoo UMG, SME and all other major labels.)

## Credits

- Nikso - Original Developer
- Sam Kujo#9403 - Original Design and Beta Tester
- Staryxz#3613 - Original Beta Tester
- PabloLuaxerc#1719 - Artist of `Wake Up Unchanged`
- Tom Rothamel - Ren'Py SDK Style Code and Feedback
- RyzekNoavek#0624 - Adjustable Play Bar Code
- khaase (Pixabay) - Refresh Icon
- eugenialcala (Pixabay) - Replay Icon
- raphaelsilva (Pixabay) - Shuffle Icon
- Josy_Dom_Alexis (Pixabay) - Volume Icon
- Google - Noto Sans SC Font (Author/Description Tag)
- Weiss Schnee - Support (Weiss :D)

## What does this do?

This allows the user to play the soundtrack of mods outside the main story, sideload music to play alongside it or for mod authors to automatically add their songs in a custom music room.

## What does this version improve on?

1. Ability to play MP3's.
2. Improved music player aesthetic.
3. Dynamic title and font size changes (sort of) and cover art scaling.
4. Song metadata support.
5. Sideload songs from your playlist to be played with the mod's tracks.
6. RPA Playback and Metadata Support
   > You will need to enable Developer Mode in order to make the metadata of songs in the track RPA folder generate for distribution.
7. Forward and Rewind back a song in progress.
8. Refresh Song List Support.
9. Sorting from within the player.
10. Replay/Shuffle Support
11. Automatically jumps to the next song after current song has ended.
12. Improved fonts for some languages. See Notes Below.

    > Due to languages and font character limits, the fonts in DDLC-OSTPlayer will not cover all languages.

    > Riffic-Bold will have to be downloaded separately to comply with the FontSpring license.

## What do I need to run this?

1. Copy of DDLC from [DDLC.moe](https://ddlc.moe)
2. The Latest DDLC-OSTPlayer [ZIP File](https://github.com/GanstaKingofSA/DDLC-OSTPlayer/releases/latest)
   > If you already have Nikso's Audio Player installed in your mod and are upgrading to this one, copy the ZIP contents to your mod's game folder **and** delete the `audio_player.rpy` file from within within `mod_assets`.
3. **(Recommended but Optional)** Riffic-Bold from [Fontspring](https://www.fontspring.com/fonts/inky-type/riffic/riffic-bold) to add more font characters to the program.
   > This font is free, but requires you to make a Fontspring account and have a _Desktop license_ for it in order for you to use this.
4. **(Optional)** Custom Music in a folder called `track` in the `game` folder
   > You can change this folder name or path to something else if you like. Do let people knowing that you changed it if they want to sideload songs to it.

## How do I install this?

1. Drop all the contents in this ZIP file to the game folder where DDLC.exe/DDLC.sh is.
   > If you are on MacOS/OS X, you must right-click DDLC.app and click `Show Package Contents` then navigate to `Contents/Resources/autorun/game` and drop the ZIP file contents in there.
2. Open `options.rpy` and add this line under line `192`
   ```py
   build.classify("game/RPASongMetadata.json", "scripts all")
   ```
3. **(Recommended but Optional)** Download the `Riffic-Bold` font from [Fontspring](https://www.fontspring.com/fonts/inky-type/riffic/riffic-bold) and copy the `riffic-bold.ttf` in _Fonts_ to `game/mod_assets/music_player`
   - Open `audio_player.rpy` and add a `#` to the front of lines `280`, `302` and `311`. Then remove the `#` in the front of lines `281`, `303` and `312`.

## How do I access the player?

Copy this line to `screens.rpy` under lines `443-478` and restart DDLC.

```python
if main_menu:
    textbutton _("OST Player") action [Show("music_player"), SetMute("music", True), SetMute("music_player_mixer", False), SetVariable("current_soundtrack", False), If(renpy.game.preferences.mute.get("music", False), true=SetVariable("music_was_muted_before_soundtrack_player_opened", True), false=SetVariable("music_was_muted_before_soundtrack_player_opened", False)), Function(refresh_list)]
```

## Can I still define songs the old way?

Yes you can. The old format still works despite the revamp however you must add this line after defining it.

```python
manualDefineList.append(Wake_Up_Unchanged)
```

> Change `Wake_Up_Unchanged` to your song variable

## How do I priortize a song or make a song the first one?

Set organizePriority to True and set the song priority by a value. 0 is the highest priority you can make a song be while 1, 2, etc. will be prioritzed lower in the list. i.e. `0 > 1 > 2 > ...`

## How do I organize the list alphabetically?

Turn on the A-Z Priority in the music player when playing a song or default it on, by setting `organizeAZ` to True.

## Can the organizations work together?

Yes. See the following organization images below.

- [Priority Organization](assets/screenshot0024.png)
- [A-Z Organization](assets/screenshot0020.png)
- [A-Z and Priority Organization](assets/screenshot0025.png)

## Why is there a file called `tinytag.py` in `python-packages`?

This handles the metadata of songs sideloaded or those that have metadata in the game.

## Why is `Riffic-Bold` not included in DDLC-OSTPlayer?

Riffic-Bold is not included in DDLC-OSTPlayer due to licensing issues with Fontspring. In order to install Riffic-Bold you will need to download it yourself as a _Desktop license_ and install it onto your project as listed above in **How do I install this?**

## How do I add metadata info?

Right-click your song, Select Properties -> Details, and fill the blank boxes you can.
Alternatively, use [MusicBee](https://www.getmusicbee.com/) or a similar music player, or [MusicBrainz Picard](https://picard.musicbrainz.org/) and find your song.

- For MusicBee: Right-Click your song within the player, select _Edit_ and edit away the info you want, then click _Apply_ then _OK_.
- For MusicBrainz Picard: Add your song to Picard, select it, right-click the rectangle box that has 3 columns, select _Add New Tag_, select the tags you want to add like _Title_, _Artist_, _Comment_, _Album_, etc. There should be a blank box in the box area below, double-click it and edit away the info you want to add, then click _Save_ and press the _Save_ button near _Info_.

## Why did you do this?

Cause I was bored and wanted to see RWBY songs play within DDLC and see song covers displayed. (Yang _:P_)
