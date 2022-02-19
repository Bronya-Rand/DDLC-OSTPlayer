
# Determines Compact Mode or List Mode UIs
default persistent.listui = False
# Automatically reverts the music playing before the player launched.
default persistent.auto_restore_music = True

image readablePos = DynamicDisplayable(renpy.curry(ost_info.music_pos)("song_progress_text"))
image readableDur = DynamicDisplayable(renpy.curry(ost_info.music_dur)("song_duration_text"))
image titleName = DynamicDisplayable(renpy.curry(ost_info.dynamic_title_text)(
                    "music_player_music_text")) 
image authorName = DynamicDisplayable(renpy.curry(ost_info.dynamic_author_text)(If(
                    renpy.android and renpy.version_tuple == (6, 99, 12, 4, 2187), 
                    "renpy6_android_song_author_text", 
                    "music_player_song_author_text")))  
image albumName = DynamicDisplayable(renpy.curry(ost_info.dynamic_album_text)(If(
                        renpy.android and renpy.version_tuple == (6, 99, 12, 4, 2187), 
                        "renpy6_android_song_author_text", 
                        "music_player_song_author_text")))
image playPauseButton = DynamicDisplayable(ost_controls.auto_play_pause_button)
image coverArt = DynamicDisplayable(ost_info.refresh_cover_data) 

screen new_music_room():

    tag menu

    default bar_val = AdjustableAudioPositionValue()

    use game_menu(_("OST Player")):
        
        hbox at music_player_transition:
            style "music_player_hbox"
            
            if not ost_info.get_current_soundtrack():
                if persistent.listui:
                    xpos 0.35
                else:
                    xpos 0.3
                    ypos 0.4
                    spacing 10

                vbox:
                    text "No music is currently playing.":
                        color "#000"
                        outlines[]
                        size 24

                    if not persistent.listui:
                        textbutton "Music List":
                            text_style "navigation_button_text"
                            action [ShowMenu("music_list_type"), With(Dissolve(0.25))]
                            xalign 0.5
            else:
                if persistent.listui:
                    xpos 0.08
                    yalign -0.25

                    add "coverArt" at cover_art_resize(200)
                else:
                    xpos 0.06
                    yalign 0.25
                
                    add "coverArt" at cover_art_resize(350)

                vbox:
                    hbox:
                        if not persistent.listui:
                            yoffset 80
                        else:
                            yoffset -2

                        vbox:
                            if not persistent.listui:
                                xsize 520
                            else:
                                xsize 640

                            add "titleName"

                            add "authorName"

                            add "albumName"

                            hbox:
                                if not persistent.listui:
                                    yoffset 20
                                else:
                                    yoffset 10
                                spacing 15

                                imagebutton:
                                    idle "mod_assets/music_player/backward.png"
                                    hover "mod_assets/music_player/backwardHover.png"
                                    action [SensitiveIf(renpy.music.is_playing(channel='music_player')), Function(ost_controls.rewind_music)]

                                add "playPauseButton"

                                imagebutton:
                                    idle "mod_assets/music_player/forward.png"
                                    hover "mod_assets/music_player/forwardHover.png"
                                    action [SensitiveIf(renpy.music.is_playing(channel='music_player')), Function(ost_controls.forward_music)]

                                if persistent.listui:

                                    null width 15

                                    imagebutton:
                                        idle ConditionSwitch("ost_controls.loopSong", "mod_assets/music_player/replayOn.png", 
                                                            "True", "mod_assets/music_player/replay.png")
                                        hover "mod_assets/music_player/replayHover.png"
                                        action [ToggleVariable("ost_controls.loopSong", False, True)]
                                    imagebutton:
                                        idle ConditionSwitch("ost_controls.randomSong", "mod_assets/music_player/shuffleOn.png", 
                                                            "True", "mod_assets/music_player/shuffle.png")
                                        hover "mod_assets/music_player/shuffleHover.png"
                                        action [ToggleVariable("ost_controls.randomSong", False, True)]
                                    imagebutton:
                                        idle "mod_assets/music_player/info.png"
                                        hover "mod_assets/music_player/infoHover.png"
                                        action [ShowMenu("music_info"), With(Dissolve(0.25))]
                                    imagebutton:
                                        idle "mod_assets/music_player/settings.png"
                                        hover "mod_assets/music_player/settingsHover.png"
                                        action [ShowMenu("music_settings"), With(Dissolve(0.25))]
                                    imagebutton:
                                        idle "mod_assets/music_player/refreshList.png"
                                        hover "mod_assets/music_player/refreshHover.png"
                                        action [Function(ost_song_assign.refresh_list)]

                                    null width 15
                                    
                                    imagebutton:
                                        idle ConditionSwitch("preferences.get_volume(\"music_player_mixer\") == 0.0", 
                                            "mod_assets/music_player/volume.png", "True", 
                                            "mod_assets/music_player/volumeOn.png")
                                        hover ConditionSwitch("preferences.get_volume(\"music_player_mixer\") == 0.0", 
                                            "mod_assets/music_player/volumeHover.png", "True", 
                                            "mod_assets/music_player/volumeOnHover.png")
                                        action [Function(ost_controls.mute_player)]
                                        yoffset -8
                                    bar value Preference ("music_player_mixer volume") xsize 100 yoffset 8 xoffset -15
                                
                            if persistent.listui:
                                yoffset 20
                                vbox:
                                    hbox:
                                        bar:
                                            style "music_player_list_bar"

                                            value bar_val
                                            hovered bar_val.hovered
                                            unhovered bar_val.unhovered

                                    hbox:
                                        add "readablePos" 
                                        add "readableDur" xpos 550

                            if not persistent.listui:

                                hbox:
                                    yoffset 30
                                    spacing 15

                                    imagebutton:
                                        idle ConditionSwitch("ost_controls.loopSong", "mod_assets/music_player/replayOn.png", 
                                                            "True", "mod_assets/music_player/replay.png")
                                        hover "mod_assets/music_player/replayHover.png"
                                        action [ToggleVariable("ost_controls.loopSong", False, True)]
                                    imagebutton:
                                        idle ConditionSwitch("ost_controls.randomSong", "mod_assets/music_player/shuffleOn.png", 
                                                            "True", "mod_assets/music_player/shuffle.png")
                                        hover "mod_assets/music_player/shuffleHover.png"
                                        action [ToggleVariable("ost_controls.randomSong", False, True)]
                                    imagebutton:
                                        idle "mod_assets/music_player/info.png"
                                        hover "mod_assets/music_player/infoHover.png"
                                        action [ShowMenu("music_info"), With(Dissolve(0.25))]
                                    imagebutton:
                                        idle "mod_assets/music_player/musicwindow.png"
                                        hover "mod_assets/music_player/musicwindowHover.png"
                                        action [ShowMenu("music_list_type"), With(Dissolve(0.25))]
                                    imagebutton:
                                        idle "mod_assets/music_player/settings.png"
                                        hover "mod_assets/music_player/settingsHover.png"
                                        action [ShowMenu("music_settings"), With(Dissolve(0.25))]
                                    imagebutton:
                                        idle "mod_assets/music_player/refreshList.png"
                                        hover "mod_assets/music_player/refreshHover.png"
                                        action [Function(ost_song_assign.refresh_list)]
        
        if persistent.listui:   
            vpgrid id "mpl" at music_player_transition:
                rows len(soundtracks)
                cols 1
                mousewheel True
                draggable True

                xpos 0.03
                ypos 0.25
                xsize 950
                ysize 380
                spacing 5

                for st in soundtracks:
                    frame:
                        xsize 900
                        hbox:
                            imagebutton:
                                xsize 66 ysize 66
                                idle Transform(ConditionSwitch(ost_info.get_current_soundtrack() == st, If(ost_controls.pausedState, "mod_assets/music_player/music_list_pause.png", 
                                    "mod_assets/music_player/music_list_play.png"), "True", st.cover_art), size=(64, 64))
                                hover Transform(ConditionSwitch(ost_info.get_current_soundtrack() == st, If(ost_controls.pausedState, "mod_assets/music_player/music_list_play.png", 
                                    "mod_assets/music_player/music_list_pause.png"), "True", "mod_assets/music_player/music_list_play.png"), size=(64, 64))
                                action If(ost_info.get_current_soundtrack() == st, If(ost_controls.pausedState, Function(ost_controls.play_music), Function(ost_controls.pause_music)), 
                                    [SetVariable("ost_controls.pausedState", False), Function(ost_info.set_current_soundtrack, st), Play("music_player", st.path, loop=ost_controls.loopSong, 
                                    fadein=2.0)])

                            null width 15

                            vbox:
                                xsize 770
                                if renpy.version_tuple == (6, 99, 12, 4, 2187) and renpy.android:
                                    text "{b}[st.name]{/b}" style "renpy6_android_alt_list_title_text"
                                    text "[st.author]" style "renpy6_android_alt_list_author_text"
                                    text "[st.album]"  style "renpy6_android_alt_list_author_text"
                                else:
                                    text "{b}[st.name]{/b}" style "music_player_alt_list_title_text"
                                    text "[st.author]" style "music_player_alt_list_author_text"
                                    text "[st.album]"  style "music_player_alt_list_author_text"
                            if st.byteTime:
                                vbox:
                                    yalign 0.5
                                    xpos -20
                                    if renpy.version_tuple == (6, 99, 12, 4, 2187) and renpy.android:
                                        text ost_info.convert_time(st.byteTime) style "renpy6_android_alt_list_author_text"
                                    else:
                                        text ost_info.convert_time(st.byteTime) style "music_player_alt_list_author_text"

        if not persistent.listui:
            hbox at music_player_transition:
                xalign 0.4
                yalign 0.85
            
                if ost_info.get_current_soundtrack():
                    vbox:
                        hbox:
                            bar:
                                style "music_player_bar"

                                value bar_val
                                hovered bar_val.hovered
                                unhovered bar_val.unhovered

                        hbox:
                            add "readablePos" 
                            add "readableDur" xpos 630
                          
                    imagebutton:
                        idle ConditionSwitch("preferences.get_volume(\"music_player_mixer\") == 0.0", 
                            "mod_assets/music_player/volume.png", "True", 
                            "mod_assets/music_player/volumeOn.png")
                        hover ConditionSwitch("preferences.get_volume(\"music_player_mixer\") == 0.0", 
                            "mod_assets/music_player/volumeHover.png", "True", 
                            "mod_assets/music_player/volumeOnHover.png")
                        action [Function(ost_controls.mute_player)]
                        yoffset -16 xoffset 10
                    bar value Preference ("music_player_mixer volume") xsize 100 xoffset 10

    text "DDLC OST-Player v[ostVersion]":
        xalign 1.0 yalign 1.0
        xoffset -10 yoffset -10
        style "main_menu_version"

    if not config.developer:
        hbox:
            xalign 0.5 yalign 0.98

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
        [Stop("music_player", fadeout=1.0), SetMute("music", False), Play("music", ost_main.prevTrack, fadein=1.0)],
        SetMute("music", True))]

screen music_list_type(type=None):

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
                        action [Hide("music_list"), ShowMenu("music_list_type")]

            hbox:
                ypos 0.005
                xalign 0.52 
                text "Music List":
                    style "music_player_generic_text"

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
                            text_style "music_list_button_text"
                            action [Hide("music_list_type"), ShowMenu("music_list")]

                        textbutton "Artist":
                            text_style "music_list_button_text"
                            action [Hide("music_list_type"), ShowMenu("music_list_type", type="artist")]

                        textbutton "Album Artist":
                            text_style "music_list_button_text"
                            action [Hide("music_list_type"), ShowMenu("music_list_type", type="albumartist")]

                        textbutton "Composer":
                            text_style "music_list_button_text"
                            action [Hide("music_list_type"), ShowMenu("music_list_type", type="composer")]

                        textbutton "Genre":
                            text_style "music_list_button_text"
                            action [Hide("music_list_type"), ShowMenu("music_list_type", type="genre")]

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
                                style "l_list"
                                text_style "music_list_button_text"
                                action [Hide("music_list_type"), ShowMenu("music_list", type=type, arg=st)]
                        
    on "hide" action With(Dissolve(0.25))
            
screen music_list(type=None, arg=None):

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
                    action [Hide("music_list"), ShowMenu("music_list_type", type=type)]

            hbox:
                ypos 0.005
                xalign 0.52 
                text "Music List":
                    style "music_player_generic_text"
                    size 24

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
                            text_style "music_list_button_text"
                            action [Hide("music_list"), Function(ost_info.set_current_soundtrack, nst), Play("music_player", nst.path, loop=ost_controls.loopSong, fadein=2.0)]

    on "hide" action With(Dissolve(0.25))

screen music_settings():

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
                text "OST-Player Settings":
                    style "music_player_generic_text"

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
                    
                    textbutton "Compact Mode":
                        style "radio_button" 
                        action [Hide("music_list_type"), Hide("music_list"), Hide("music_info"),
                            ToggleField(persistent, "listui", False, True)]

                    textbutton "Restore Music Channel Music":
                        style "radio_button" 
                        action InvertSelected(ToggleField(persistent, "auto_restore_music", False, True))
                            
                    textbutton "About DDLC OST-Player":
                        text_style "navigation_button_text" 
                        action Show("dialog", message="DDLC OST-Player by GanstaKingofSA.\nCopyright © 2020-2022 GanstaKingofSA.", 
                            ok_action=Hide("dialog"))

    on "hide" action With(Dissolve(0.25))    

screen music_info():

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
                text "Music Info" style "music_player_generic_text"

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
                        text "{u}Album Artist{/u}: [albumartist]" style "renpy6_android_music_player_info_text"
                        text "{u}Composer{/u}: [composer]" style "renpy6_android_music_player_info_text"
                        text "{u}Genre{/u}: [genre]" style "renpy6_android_music_player_info_text"
                        text "{u}Sideloaded{/u}: [sideloaded]" style "renpy6_android_music_player_info_text"
                        text "{u}Comment{/u}: [comment]" style "renpy6_android_music_player_info_text"
                    else:
                        text "{u}Album Artist{/u}: [albumartist]" style "music_player_info_text"
                        text "{u}Composer{/u}: [composer]" style "music_player_info_text"
                        text "{u}Genre{/u}: [genre]" style "music_player_info_text"
                        text "{u}Sideloaded{/u}: [sideloaded]" style "music_player_info_text"
                        text "{u}Comment{/u}: [comment]" style "music_player_info_text"

    on "hide" action With(Dissolve(0.25))    

style music_player_music_text is navigation_button_text:
    #font "mod_assets/music_player/riffic-bold.ttf"
    color "#000"
    outlines [(0, "#000", 0, 0)]
    hover_outlines []
    insensitive_outlines []
    size 36

style music_player_song_author_text:
    font "mod_assets/music_player/NotoSansSC-Light.otf"
    size 22
    outlines[]
    color "#000"

style music_list_button_text is navigation_button_text:
    size 22

style music_player_hbox:
    spacing 25

style music_player_bar:
    xsize 710
    thumb "gui/slider/horizontal_hover_thumb.png"

style music_player_list_bar is music_player_bar:
    xsize 600

style music_player_alt_list_title_text:
    font "mod_assets/music_player/NotoSansSC-Light.otf"
    color "#000"
    outlines []
    size 15
    bold True

style music_player_alt_list_author_text is music_player_alt_list_title_text:
    size 13
    bold False

transform music_player_transition:
    alpha(0.0)
    linear 0.5 alpha(1.0)

style song_progress_text:
    font "gui/font/Halogen.ttf"
    size 25
    outlines[]
    color "#000"
    xalign 0.28 
    yalign 0.78

style song_duration_text is song_progress_text:
    xalign 0.79 
    yalign 0.78

style l_list:
    left_padding 5

style renpy_generic_text:
    font "mod_assets/music_player/NotoSans-Regular.ttf"
    color "#000"
    outlines []

style music_player_info_text is music_player_alt_list_title_text:
    size 20
    bold False

style music_player_generic_text is renpy_generic_text:
    size 24
    bold False

style renpy6_android_song_title_text is renpy_generic_text:
    size 36
    bold True

style renpy6_android_song_author_text is renpy_generic_text:
    size 22

style renpy6_android_alt_list_title_text is renpy_generic_text:
    size 15
    bold True

style renpy6_android_alt_list_author_text is renpy_generic_text:
    size 14

style renpy6_android_music_player_info_text is renpy_generic_text:
    size 22

transform cover_art_resize(x):
    size(x, x)
