
# Determines Compact Mode or List Mode UIs
default persistent.listui = False
# Automatically reverts the music playing before the player launched.
default persistent.auto_restore_music = True
# Add a fadein/out to the track similar to Poweramp or music players with one.
default persistent.fadein = False
# Use the game menu in the music room over full screen change.
default persistent.use_game_menu = True

image readablePos = DynamicDisplayable(ost_info.music_pos)
image readableDur = DynamicDisplayable(ost_info.music_dur)
image titleName = DynamicDisplayable(ost_info.dynamic_title_text)
image authorName = DynamicDisplayable(renpy.curry(ost_info.dynamic_author_text)(If(
    renpy.android and renpy.version_tuple == (6, 99, 12, 4, 2187), 
        "r6_android_song_author_text", 
        "music_player_text")
        )
)  
image albumName = DynamicDisplayable(renpy.curry(ost_info.dynamic_album_text)(If(
        renpy.android and renpy.version_tuple == (6, 99, 12, 4, 2187), 
        "r6_android_song_author_text", 
        "music_player_text")
    )
)
image coverArt = DynamicDisplayable(ost_info.refresh_cover_data) 

screen new_music_room():

    style_prefix "music_player"

    tag menu

    default bar_val = AdjustableAudioPositionValue()

    if persistent.use_game_menu:
        
        use game_menu(_("OST Player")):
            
            fixed at music_player_transition:

                if persistent.listui:
                    
                    use ostplayer_list_ui(bar_val)
                
                else:

                    use ostplayer_compact_ui(bar_val)
                    
    text "DDLC OST-Player v[ostVersion]":
        xalign 1.0 yalign 1.0
        xoffset -10 yoffset -10
        style "main_menu_version"

    if not config.developer:
        hbox:
            xalign 0.5 
            yalign 0.98

            python:
                try:
                    if renpy.android and renpy.version_tuple == (6, 99, 12, 4, 2187):
                        file(os.environ["ANDROID_PUBLIC"] + "/game/RPASongMetadata.json")
                    else:
                        renpy.file("RPASongMetadata.json")
                    file_found = True
                except: file_found = False
            
            if not file_found:
                imagebutton:
                    idle "mod_assets/music_player/osterror.png"
                    action Show("dialog", message="{b}Warning{/b}\nThe RPA metadata file hasn't been generated.\nSongs in the {i}track{/i} folder won't be listed if you build your mod without it.\n Set {i}config.developer{/i} to {u}True{/u} in order to generate this file.",
                        ok_action=Hide("dialog"))

    # Start the music playing on entry to the music room.
    on "replace" action [Function(ost_main.ost_start), Stop("music", fadeout=1.0)]
    on "show" action [Function(ost_main.ost_start), Stop("music", fadeout=1.0)]

    # Restore the main menu music upon leaving.
    on "hide" action [If(persistent.auto_restore_music,
        [Stop("music_player", fadeout=1.0), SetMute("music", False), Play("music", ost_main.prevTrack, fadein=1.0)],
        SetMute("music", True))]
    on "replaced" action [Hide("music_settings"), Hide("music_list"), Hide("music_list_type"), 
        Hide("music_info"), Function(ost_main.ost_log_stop), If(persistent.auto_restore_music,
        [Function(ost_controls.pause_music), SetMute("music", False), Play("music", ost_main.prevTrack, fadein=1.0)],
        SetMute("music", True))]

screen music_list_type(type=None):

    style_prefix "music_window"

    drag:
        drag_name "mlisttype"
        drag_handle (0, 0, 1.0, 40)
        xsize 470
        ysize 260
        xpos 0.3
        ypos 0.2

        frame:

            if type is not None:
                hbox:
                    xalign 0.05 ypos 0.005
                    textbutton "<-":
                        text_style "navigation_button_text"
                        action [Hide("music_list"), Show("music_list_type")]

            hbox:
                ypos 0.005
                xalign 0.52 
                text "Music List"

            hbox:
                ypos 0.005
                xalign 0.98
                textbutton "X":
                    text_style "navigation_button_text"
                    action Hide("music_list_type")

            side "c":
                xpos 0.05
                ypos 0.2
                xsize 430
                ysize 200

                viewport id "mlt":
                    mousewheel True
                    draggable True
                    has vbox

                    if type is None:
                        textbutton "All Songs":
                            action [Hide("music_list_type"), Show("music_list")]

                        textbutton "Artist":
                            action [Show("music_list_type", type="artist")]

                        textbutton "Album Artist":
                            action [Show("music_list_type", type="albumartist")]

                        textbutton "Composer":
                            action [Show("music_list_type", type="composer")]

                        textbutton "Genre":
                            action [Show("music_list_type", type="genre")]

                    else:
                        python:
                            temp_list = []
                            for st in soundtracks:
                                if type == "artist":
                                    if st.author not in temp_list:
                                        temp_list.append(st.author)
                                elif type == "albumartist":
                                    if st.albumartist not in temp_list:
                                        temp_list.append(st.albumartist)
                                elif type == "composer":
                                    if st.composer not in temp_list:
                                        temp_list.append(st.composer)
                                elif type == "genre":
                                    if st.genre not in temp_list:
                                        temp_list.append(st.genre)
                            
                            temp_list = sorted(temp_list)

                        for st in temp_list:
                            textbutton "[st]":
                                action [Hide("music_list_type"), Show("music_list", type=type, arg=st)]
                        
    on "hide" action With(Dissolve(0.25))
            
screen music_list(type=None, arg=None):

    style_prefix "music_window"

    drag:
        drag_name "mlist"
        drag_handle (0, 0, 1.0, 40)
        xsize 470
        ysize 260
        xpos 0.3
        ypos 0.2

        python:
            new_soundtrack_list = []
            for st in soundtracks:
                if type == "artist":
                    if arg == st.author:
                        new_soundtrack_list.append(st)
                elif type == "albumartist":
                    if arg == st.albumartist:
                        new_soundtrack_list.append(st)
                elif type == "composer":
                    if arg == st.composer:
                        new_soundtrack_list.append(st)
                elif type == "genre":
                    if arg == st.genre:
                        new_soundtrack_list.append(st)
                else:
                    new_soundtrack_list.append(st)
                    
            new_soundtrack_list = sorted(new_soundtrack_list, key=lambda new_soundtrack_list: new_soundtrack_list.name)

        frame:
            hbox:
                xalign 0.05 ypos 0.005
                textbutton "<-":
                    text_style "navigation_button_text"
                    action [Hide("music_list"), Show("music_list_type", type=type)]

            hbox:
                ypos 0.005
                xalign 0.52 
                text "Music List"

            hbox:
                ypos 0.005
                xalign 0.98
                textbutton "X":
                    text_style "navigation_button_text"
                    action Hide("music_list")

            side "c":
                xpos 0.05
                ypos 0.2
                xsize 430
                ysize 200

                viewport id "ml":
                    draggable True
                    mousewheel True
                    has vbox

                    for nst in new_soundtrack_list:
                        textbutton "[nst.name]":
                            style "l_list"
                            text_style "music_window_button_text"
                            action [Hide("music_list"), Function(ost_info.set_current_soundtrack, nst), Play("music_player", nst.path, loop=ost_controls.loopSong, fadein=2.0)]

    on "hide" action With(Dissolve(0.25))

screen music_settings():

    style_prefix "music_settings"

    drag:
        drag_name "msettings"
        drag_handle (0, 0, 1.0, 40)
        xsize 470
        ysize 260
        xpos 0.5
        ypos 0.5

        frame:
            hbox:
                ypos 0.005
                xalign 0.52 
                text "Settings" style "music_window_text"

            hbox:
                ypos 0.005
                xalign 0.98
                textbutton "X":
                    text_style "navigation_button_text"
                    action Hide("music_settings")

            side "c":
                xpos 0.05
                ypos 0.2
                xsize 430
                ysize 200

                viewport id "mlt":
                    mousewheel True
                    draggable True
                    has vbox
                    
                    label "UI"
                    vbox:
                        textbutton "Compact Mode":
                            style "radio_button" 
                            action [Hide("music_list_type"), Hide("music_list"), Hide("music_info"),
                                ToggleField(persistent, "listui", False, True)]

                    label "Player"
                    vbox:
                        textbutton "Restore Original Music On Exit":
                            style "radio_button" 
                            action InvertSelected(ToggleField(persistent, "auto_restore_music", False, True))
                        
                        textbutton "Song Fade In/Out":
                            style "radio_button" 
                            action InvertSelected(ToggleField(persistent, "fadein", False, True))
                            
                    textbutton "About DDLC OST-Player":
                        text_style "navigation_button_text" 
                        action Show("dialog", message="DDLC OST-Player by GanstaKingofSA.\nCopyright © 2020-2022 GanstaKingofSA.", 
                            ok_action=Hide("dialog"))

    on "hide" action With(Dissolve(0.25))   

screen music_info():

    style_prefix "music_window"

    drag:
        drag_name "minfo"
        drag_handle (0, 0, 1.0, 40)
        xsize 480
        ysize 260
        xpos 0.4
        ypos 0.4

        frame:
            hbox:
                ypos 0.005
                xalign 0.52 
                text "Music Info"

            hbox:
                ypos 0.005
                xalign 0.98
                textbutton "X":
                    text_style "navigation_button_text"
                    action Hide("music_info")

            side "c":
                xpos 0.05
                ypos 0.2
                xsize 460
                ysize 200

                viewport id "mi":
                    mousewheel True
                    draggable True
                    has vbox

                    python:
                        albumartist = ost_info.get_album_artist()
                        composer = ost_info.get_composer()
                        genre = ost_info.get_genre()
                        sideloaded = ost_info.get_sideload()
                        comment = ost_info.get_description() or None
                    
                    if renpy.android and renpy.version_tuple == (6, 99, 12, 4, 2187):
                        text "{u}Album Artist{/u}: [albumartist]" style "r6_android_music_player_info_text"
                        text "{u}Composer{/u}: [composer]" style "r6_android_music_player_info_text"
                        text "{u}Genre{/u}: [genre]" style "r6_android_music_player_info_text"
                        text "{u}Sideloaded{/u}: [sideloaded]" style "r6_android_music_player_info_text"
                        text "{u}Comment{/u}: [comment]" style "r6_android_music_player_info_text"
                    else:
                        text "{u}Album Artist{/u}: [albumartist]" style "music_player_info_text"
                        text "{u}Composer{/u}: [composer]" style "music_player_info_text"
                        text "{u}Genre{/u}: [genre]" style "music_player_info_text"
                        text "{u}Sideloaded{/u}: [sideloaded]" style "music_player_info_text"
                        text "{u}Comment{/u}: [comment]" style "music_player_info_text"

    on "hide" action With(Dissolve(0.25))    
