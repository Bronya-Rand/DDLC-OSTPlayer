
Installation:

This assumes you already have a copy of DDLC with the mod template installed over it.

1. Copy the 'game' folder to your DDLC directory folder (where DDLC.exe/DDLC.sh reside in).
  a. If you are on MacOS/OS X, you must right-click DDLC.app and click Show Package Contents 
  then navigate to Contents/Resources/autorun and drop the ZIP file contents in there.

2. Copy this line to 'screens.rpy' under textbutton _("Load Game").

    textbutton _("OST Player") action [[Show("new_music_room"), Function(ost_player_controls.enter), SensitiveIf(renpy.get_screen("new_music_room") == None)]]

3. Define music you want to add via the OSTLocalTrack class
4. Run DDLC and enjoy!

Credits!
- Nikso - Original Developer
- Sam Kujo#9403 - Original Design and Beta Tester
- Staryxz#3613 - Original Beta Tester
- PabloLuaxerc#1719 - Artist of "Wake Up Unchanged"
- Tom Rothamel - Ren'Py SDK Style Code, R7 Loader/Main Code and feedback
- Tom Wallroth - Tinytag
- RyzekNoavek#0624 - Adjustable Play Bar Code
- khaase (Pixabay) - Refresh Icon (Prior to Version 2.0)
- eugenialcala (Pixabay) - Replay Icon (Prior to Version 2.0)
- raphaelsilva (Pixabay) - Shuffle Icon (Prior to Version 2.0)
- Josy_Dom_Alexis (Pixabay) - Volume Icon (Prior to Version 2.0)
- Google - Noto Sans SC/Regular Font and Icons (Version 2.0+)
- Ren'Py Discord - Feedback on Ren'Py Universal Player Feats Now In DDLC OST-Player
- Weiss Schnee - Support (Weiss :D)
