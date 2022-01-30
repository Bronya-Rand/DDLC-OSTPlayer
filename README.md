# DDLC OST Player

A heavily revamped version of Nikso's Soundtrack Player for DDLC.

[Download DDLC OST-Player Here!](https://github.com/GanstaKingofSA/DDLC-OSTPlayer/releases/latest) 

<p align="center">
   <img src=".github/assets/OSTPlayerLogo.png" alt="OST Player Logo" width=240x> 
</p>

**DISCLAIMER:** This is not afiliated or endorsed by Team Salvato or Nikso. The Scattered Stars <u>logo</u> in `Wake Up Unchanged` is not free to use, but is only allowed in this build as a display to the soundtrack player. If you plan to use this, remove it in your final build.

> All songs featured above are owned by the developer and are not included in DDLC OST Player. (Shoo UMG, SME, Rooster Teeth)

## What is DDLC OST Player?
This allows the user to play the mods' soundtrack alongside a players' own music outside the main story.

<u>Screenshots:</u> [Compact Mode (Default)](.github/assets/screenshot0001.png) • [List Mode](.github/assets/screenshot0002.png)

## Features
1. Ability to play MP3, OGG, WAV and OPUS files with metadata!
   > Some players will export music files differently than normal. Make sure your tracks are exported properly using your music player or Audacity.
2. Improved music player aesthetic.
3. Dynamic title and font size changes (sort of) and cover art scaling.
4. Sideload songs from your playlist to be played with the mod's tracks.
5. RPA/APK playback and metadata support!
6. Improved fonts for foreign languages*.
   > \* - Due to languages and font character limits, the fonts in DDLC OST-Player will not cover all languages. Riffic-Bold will have to be downloaded separately to comply with the FontSpring license.
7. Android Support! (Ren'Py 7 Recommended)

## Installation Requirements
> This assumes you already have a copy of DDLC with the mod template installed over it.
1. The Latest DDLC OST-Player [ZIP file](https://github.com/GanstaKingofSA/DDLC-OSTPlayer/releases/latest).
2. **(Optional)** Riffic-Bold from [Fontspring](https://www.fontspring.com/fonts/inky-type/riffic/riffic-bold) to add more font characters to the program.
   > This font is free, but requires you to make a Fontspring account and have a _Desktop license_ for it in order for you to use this.

## Install Steps
1. Drop all the contents in this ZIP file into the base folder of DDLC (where `DDLC.exe`/`DDLC.sh` is).
   > If you are on MacOS/OS X, you must right-click DDLC.app and click `Show Package Contents` then navigate to `Contents/Resources/autorun` and drop the ZIP file contents in there.
2. Copy this line to _screens.rpy_ under `textbutton _("Load Game")`.
   ```py
   textbutton _("OST Player") action [ShowMenu("new_music_room"), Function(ost_start), SensitiveIf(renpy.get_screen("new_music_room") == None)]
   ```
3. **(Optional)** Download the `Riffic-Bold` font from [Fontspring](https://www.fontspring.com/fonts/inky-type/riffic/riffic-bold) and copy the `riffic-bold.ttf` in _Fonts_ to `game/mod_assets/music_player`
   - Open _audio_player.rpy_ and remove the `#` symbol in front of line `556`.
4. Put music in the `track` folder inside the `game` folder and try it out!

## Can I still define songs the old way?
Yes you can with some caviats.
   1. `priority` has been removed.
   2. Manually defined songs require the following to be added after you fill out it's details.
      ```py
      manualDefineList.append(Wake_Up_Unchanged)
      ```
      > Change `Wake_Up_Unchanged` to your song variable

See _manualtracks.rpy_ for a example or _audio_code.rpy_ for what can be defined.

## Why is `Riffic-Bold` not included in DDLC OST Player?
Riffic-Bold is not included in DDLC OST-Player due to licensing issues with Fontspring. In order to install Riffic-Bold you will need to download it yourself as a _Desktop license_ and install it onto your project as listed above in **How do I install this?**

## How do I add metadata info?

Right-click your song, Select Properties -> Details, and fill the blank boxes you can.
Alternatively, use [MusicBee](https://www.getmusicbee.com/) or a similar music player, or [MusicBrainz Picard](https://picard.musicbrainz.org/) and find your song.

- For MusicBee: Right-Click your song within the player, select _Edit_ and edit away the info you want, then click _Apply_ then _OK_.
- For MusicBrainz Picard: Add your song to Picard, select it, right-click the rectangle box that has 3 columns, select _Add New Tag_, select the tags you want to add like _Title_, _Artist_, _Comment_, _Album_, etc. There should be a blank box in the box area below, double-click it and edit away the info you want to add, then click _Save_ and press the _Save_ button near _Info_.

## Why is Ren'Py 7 Recommended for Android?
Ren'Py 6 has funky code in Android and requires patches to work properly.</u>

## Why did you do this?
Cause I was bored and wanted to see RWBY songs play within DDLC and see song covers displayed. (Yang _:P_)

## Credits

- Nikso - Original Developer
- Sam Kujo#9403 - Original Design and Beta Tester
- Staryxz#3613 - Original Beta Tester
- PabloLuaxerc#1719 - Artist of *Wake Up Unchanged*
- Tom Rothamel - Ren'Py SDK Style Code, Ren'Py `loader.py`/`main.py` Code and Feedback
- Tom Wallroth - Tinytag Code
- RyzekNoavek#0624 - Adjustable Play Bar Code
- khaase (Pixabay) - Refresh Icon (Prior to Version 2.0)
- eugenialcala (Pixabay) - Replay Icon (Prior to Version 2.0)
- raphaelsilva (Pixabay) - Shuffle Icon (Prior to Version 2.0)
- Josy_Dom_Alexis (Pixabay) - Volume Icon (Prior to Version 2.0)
- Google - Noto Sans SC Font (Author/Description Tag) and Icons (Version 2.0+)
- Ren'Py Discord - Feedback on Ren'Py Universal Player Feats Now In DDLC OST-Player
- Weiss Schnee - Support (Weiss :D)

Copyright 2019-2022 Azariel Del Carmen (GanstaKingofSA). All rights reserved.