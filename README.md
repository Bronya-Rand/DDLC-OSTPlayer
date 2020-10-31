# DDLC-OSTPlayer
A heavily revamped version of Nikso's Soundtrack Player for DDLC.

![Sample preview](https://cdn.discordapp.com/attachments/373669030747308032/762123533052149760/Preview.png)

**DISCLAIMER:** This is not afiliated or endorsed by Team Salvato or Nikso. All support questions for this version, please address to GanstaKingofSA. This is semi-<ins>beta</ins>, meaning possible bugs may exist. Please report them to me be fixed.

## Credits
* Nikso - Original Developer of the Soundtrack Player
* Sam Kujo#9403 - Original Design and Beta Tester
* Staryxz#3613 - Original Beta Tester
* PabloLuaxerc#1719 - Artist of `Wake Up Unchanged`
* Tom Rothamel - Ren'Py SDK Style Code

The Scattered Stars Logo in `Wake Up Unchanged` is not free to use but is only allowed in this build as a showcase display to the soundtrack player. If you plan to use this, remove it in your final build.

## What does this do?
This allows the user to play the soundtrack of mods outside the main story, sideload actual music to play along with the mod OST or mod authors automatically adding their songs and having them display on the player.

## What does this version improve on?
- Added MP3 compatibility to be read and played
- Improved Music Progress Capability and music player aesthetic
- Dynamic title and font size changes (sort of) and Dynamic Cover Art Scaling (no need to descale art to 350x350)
- Metadata Support for songs
- Sideloading songs from your playlist to a directory if available in a mod

## What do I need to run this?
1. Copy of DDLC (New Blank Copy from [DDLC.moe](https://ddlc.moe)
2. This ZIP [file](https://github.com/GanstaKingofSA/DDLC-OSTPlayer/releases) with `audio_player.rpy`, `mod_assets` and `python-packages`
   * If you don't have these, please re-download the ZIP.
   * If all you are missing is `mod_assets`, copy the one from Nikso's ZIP **but** delete the `audio_player.rpy` file from within it unless you already replaced it with this version.
   * If you are missing `python-packages`, you can either re-download the ZIP or run the command below in Command Prompt/Terminal/Powershell. Make sure Python 2.7 is installed on your system and are pointed at the base directory of the game.
      
        > pip install --target game/python-packages tinytag

3. (Optional) Custom Music in a folder called `track` in the `game` folder
    * You can change this folder name or path to something else if you like. If you plan to do so, look at lines `336`, `353`, `384`, `407`, `408`, `417`, and `418` and change their respective paths to your new location.

## How do I install this?
* Drop everything in this ZIP to the game folder. 
    * If you are running Nikso's Player and installing this, drop `audio_player.rpy` to the `mod_assets` folder and click `Replace` if prompted.

## How do I access the player?
Copy this line to screens.rpy under lines `443-478` and restart DDLC.

    ```
    if main_menu:
        textbutton _("Soundtrack player") action [Show("music_player"), SetMute("music", True), SetMute("music_player_mixer", False), SetVariable("current_soundtrack", False), If(renpy.game.preferences.mute.get("music", False), true=SetVariable("music_was_muted_before_soundtrack_player_opened", True), false=SetVariable("music_was_muted_before_soundtrack_player_opened", False))]
    ```

## Can I still define songs the old way?
Yes you can. The old format still works despite the revamp. It will just ignore some metadata changes and will be priortized as value `2`.

## How do I priortize a song or make a song the first one?
Set organizePriority to True and set the song priority by a value. 0 is the highest priority you can make a song be while 1, 2, etc. will be prioritzed lower in the list. i.e. `0 > 1 > 2 > ...`

## How do I organize the list alphabetically?
Set organizeAZ to True

## Can the organizations work together?
Yes.

* Preview of Organization
![Organization preview](https://cdn.discordapp.com/attachments/373669030747308032/762177096411643904/Untitled-1.png)

## Why is there a file called `tinytag.py` in `python-packages`?
This handles the metadata of songs sideloaded or those that have metadata in the game.

## Why is the menu buggy? I got a error for pressing nothing?
Current bug with the current screen by Nikso's Player though do report them to me still to be fixed.

## How do I add a description to a metadata file to explain my song?
Right-click your song, Select Properties -> Details, Double-Click the Box near Comments and type it in
* Alternatively, use [MusicBee](https://www.getmusicbee.com/) or a similar music player, or [MusicBrainz Picard](https://picard.musicbrainz.org/) and find your song.
  * For MusicBee: Right-Click your song within the player, select `Edit` and edit away the info you want, then click `Save`.
  * For MusicBrainz Picard: Add your song to Picard, select it, right-click the rectangle box that has 3 columns, select `Add New Tag` and type `comment`. Select `comment` and there should be a blank box in the box area below. Double-click it and edit away the info you want to add, then click `Save` and press the `Save` button near `Info`.

## How do I add metadata info?
Right-click your song, Select Properties -> Details, and fill the blank boxes you can
* Alternatively, use [MusicBee](https://www.getmusicbee.com/) or a similar music player, or [MusicBrainz Picard](https://picard.musicbrainz.org/) and find your song.
  * For MusicBee: Right-Click your song within the player, select `Edit` and edit away the info you want, then click `Apply` then `OK`.
  * For MusicBrainz Picard: Add your song to Picard, select it, right-click the rectangle box that has 3 columns, select `Add New Tag`, select the tags you want to add like `Title`, `Artist`, `Comment`, `Album`, etc. There should be a blank box in the box area below, double-click it and edit away the info you want to add, then click `Save` and press the `Save` button near `Info`.

## Why did you do this?
Cause I was bored and wanted to see RWBY songs play within DDLC and see song covers displayed. (Also to fix and improve Python code)