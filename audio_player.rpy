
init 1 python:
    #import os
    #ost = MusicRoom("music_player", 0.5, 0.5)

    resort()

    #for st in soundtracks:
    #    ost.add(st.path, always_unlocked=st.unlocked)

    #def new_auto_play_pause_button(st, at):
    #    if renpy.music.get_pause('music_player'):
    #        d = renpy.display.behavior.ImageButton("mod_assets/music_player/play.png", action=ost.TogglePause())
    #    else:
    #        d = renpy.display.behavior.ImageButton("mod_assets/music_player/pause.png", action=ost.TogglePause())
    #    return d, 0.20

default persistent.listui = False

image readablePos = DynamicDisplayable(renpy.curry(music_pos)("song_progress_text"))
image readableDur = DynamicDisplayable(renpy.curry(music_dur)("song_duration_text"))
image titleName = DynamicDisplayable(renpy.curry(dynamic_title_text)(
                    "music_player_music_text")) 
image authorName = DynamicDisplayable(renpy.curry(dynamic_author_text)(If(
                    renpy.android and renpy.version_tuple == (6, 99, 12, 4, 2187), 
                    "song_author_text_android6", 
                    "music_player_song_author_text")))  
image albumName = DynamicDisplayable(renpy.curry(dynamic_album_text)(If(
                        renpy.android and renpy.version_tuple == (6, 99, 12, 4, 2187), 
                        "song_author_text_android6", 
                        "music_player_song_author_text")))
image coverArt = DynamicDisplayable(refresh_cover_data)
#image playPauseButton = DynamicDisplayable(auto_play_pause_button)
image coverArt = DynamicDisplayable(refresh_cover_data) 

screen new_music_room():

    tag menu

    default bar_val = AdjustableAudioPositionValue()

    use game_menu(_("OST Player")):
        
        hbox at music_player_transition:
            style "music_player_hbox"
            
            if not current_soundtrack:
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

                    add "coverArt" xsize 200 ysize 200
                else:
                    xpos 0.06
                    yalign 0.25
                
                    add "coverArt" xsize 350 ysize 350

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
                                    action [SensitiveIf(renpy.music.is_playing(channel='music_player')), Function(current_music_backward)]#ost.Previous()]

                                imagebutton:
                                    idle ConditionSwitch(pausedstate, "mod_assets/music_player/pause.png", 
                                        "True", "mod_assets/music_player/play.png")
                                    hover ConditionSwitch(pausedstate, "mod_assets/music_player/play.png", 
                                        "True", "mod_assets/music_player/pause.png")
                                    action If(pausedstate, Function(current_music_play), Function(current_music_pause))

                                imagebutton:
                                    idle "mod_assets/music_player/forward.png"
                                    action [SensitiveIf(renpy.music.is_playing(channel='music_player')), Function(current_music_forward)]#ost.Next()]

                                if persistent.listui:

                                    null width 20

                                    imagebutton:
                                        idle ConditionSwitch("loopSong", "mod_assets/music_player/replayOn.png", 
                                                            "True", "mod_assets/music_player/replay.png")
                                        hover "mod_assets/music_player/replayHover.png"
                                        action [ToggleVariable("loopSong", False, True)]
                                    imagebutton:
                                        idle ConditionSwitch("randomSong", "mod_assets/music_player/shuffleOn.png", 
                                                            "True", "mod_assets/music_player/shuffle.png")
                                        hover "mod_assets/music_player/shuffleHover.png"
                                        action [ToggleVariable("randomSong", False, True)]
                                    imagebutton:
                                        idle "mod_assets/music_player/settings.png"
                                        hover "mod_assets/music_player/settingsHover.png"
                                        action [ShowMenu("music_settings"), With(Dissolve(0.25))]
                                    imagebutton:
                                        idle "mod_assets/music_player/refreshList.png"
                                        hover "mod_assets/music_player/refreshHover.png"
                                        action [Function(refresh_list)]

                                    null width 20
                                    
                                    imagebutton:
                                        idle ConditionSwitch("preferences.get_volume(\"music_player_mixer\") == 0.0", 
                                            "mod_assets/music_player/volume.png", "True", 
                                            "mod_assets/music_player/volumeOn.png")
                                        hover ConditionSwitch("preferences.get_volume(\"music_player_mixer\") == 0.0", 
                                            "mod_assets/music_player/volumeHover.png", "True", 
                                            "mod_assets/music_player/volumeOnHover.png")
                                        action [Function(mute_player)]
                                        yoffset -8
                                    bar value Preference ("music_player_mixer volume") xsize 100 yoffset 8 xoffset -10
                                
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
                                        add "readableDur" xoffset 530

                            if not persistent.listui:

                                hbox:
                                    yoffset 30
                                    spacing 15

                                    imagebutton:
                                        idle ConditionSwitch("loopSong", "mod_assets/music_player/replayOn.png", 
                                                            "True", "mod_assets/music_player/replay.png")
                                        hover "mod_assets/music_player/replayHover.png"
                                        action [ToggleVariable("loopSong", False, True)]
                                    imagebutton:
                                        idle ConditionSwitch("randomSong", "mod_assets/music_player/shuffleOn.png", 
                                                            "True", "mod_assets/music_player/shuffle.png")
                                        hover "mod_assets/music_player/shuffleHover.png"
                                        action [ToggleVariable("randomSong", False, True)]
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
                                        action [Function(refresh_list)]
        
        if persistent.listui:   
            vpgrid id "mpl" at music_player_transition:
                rows len(soundtracks)
                cols 1
                mousewheel True
                scrollbars "vertical"

                xalign 0.5
                ypos 0.25
                xsize 950
                ysize 380
                spacing 5

                for st in soundtracks:
                    frame:
                        xsize 900
                        hbox:
                            imagebutton:
                                xsize 64 ysize 64
                                idle Transform(ConditionSwitch(current_soundtrack == st, If(pausedstate, "mod_assets/music_player/music_list_pause.png", 
                                    "mod_assets/music_player/music_list_play.png"), "True", st.cover_art), size=(64, 64))
                                hover Transform(ConditionSwitch(current_soundtrack == st, If(pausedstate, "mod_assets/music_player/music_list_play.png", 
                                    "mod_assets/music_player/music_list_pause.png"), "True", "mod_assets/music_player/music_list_play.png"), size=(64, 64))
                                action If(current_soundtrack == st, If(pausedstate, Function(current_music_play), Function(current_music_pause)), 
                                    [SetVariable("pausedstate", False), SetVariable("current_soundtrack", st), Play("music_player", st.path, loop=loopSong, 
                                    fadein=2.0)])

                            null width 15

                            vbox:
                                xsize 770
                                text "{b}[st.name]{/b}" style "music_player_alt_list_title_text"
                                text "[st.author]" style "music_player_alt_list_author_text"
                                text "[st.album]" style "music_player_alt_list_author_text"
                            vbox:
                                yalign 0.5
                                text convert_time(st.byteTime) style "music_player_alt_list_author_text"

        if not persistent.listui:
            hbox at music_player_transition:
                xalign 0.4
                yalign 0.85
            
                if current_soundtrack:
                    vbox:
                        hbox:
                            bar:
                                style "music_player_bar"

                                value bar_val
                                hovered bar_val.hovered
                                unhovered bar_val.unhovered

                        hbox:
                            add "readablePos" 
                            add "readableDur" xoffset 600
                          
                    imagebutton:
                        idle ConditionSwitch("preferences.get_volume(\"music_player_mixer\") == 0.0", 
                            "mod_assets/music_player/volume.png", "True", 
                            "mod_assets/music_player/volumeOn.png")
                        hover ConditionSwitch("preferences.get_volume(\"music_player_mixer\") == 0.0", 
                            "mod_assets/music_player/volumeHover.png", "True", 
                            "mod_assets/music_player/volumeOnHover.png")
                        action [Function(mute_player)]
                        yoffset -16 xoffset 10
                    bar value Preference ("music_player_mixer volume") xsize 100 xoffset 10

    text "DDLC OST-Player v[ostVersion]":
        xalign 1.0 yalign 1.0
        xoffset -10 yoffset -10
        style "main_menu_version"

    # Start the music playing on entry to the music room.
    on "replace" action [Function(ost_start), Stop("music", fadeout=1.0)]

    # Restore the main menu music upon leaving.
    on "replaced" action [Function(ost_log_stop), Stop("music_player", fadeout=1.0), Play("music", prevTrack, fadein=1.0)]

screen music_list_type(type=None):

    frame:
        xsize 480
        ysize 260
        xpos 0.3
        ypos 0.2

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
                color "#000"
                outlines[]
                size 24

        hbox:
            ypos 0.005
            xalign 0.98
            textbutton "X":
                text_style "navigation_button_text"
                action Hide("music_list_type")

        side "c":
            xpos 0.05
            ypos 0.2
            xsize 460
            ysize 200

            viewport id "mlt":
                mousewheel True
                has vbox

                if type is None:
                    textbutton "All Songs":
                        text_style "music_list_button_text"
                        action [Hide("music_list_type"), ShowMenu("music_list", arg=None)]

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
                        textbutton st:
                            style "l_list"
                            text_style "music_list_button_text"
                            action [Hide("music_list_type"), ShowMenu("music_list", type=type, arg=st)]
                        
    on "hide" action With(Dissolve(0.25))
            
screen music_list(type=None, arg=None):

    frame:
        xsize 480
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

        hbox:
            xalign 0.05 ypos 0.005
            textbutton "<-":
                text_style "navigation_button_text"
                action [Hide("music_list"), ShowMenu("music_list_type", type=type)]

        hbox:
            ypos 0.005
            xalign 0.52 
            text "Music List":
                color "#000"
                outlines[]
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
            xsize 450
            ysize 200

            viewport id "ml":
                
                mousewheel True
                has vbox

                for nst in new_soundtrack_list:
                    textbutton "[nst.name]":
                        style "l_list"
                        text_style "music_list_button_text"
                        action [Hide("music_list"), SetVariable("current_soundtrack", nst), Play("music_player", nst.path, loop=loopSong, fadein=2.0)]#ost.Play(nst.path)]

    on "hide" action With(Dissolve(0.25))

screen music_settings():

    frame:
        xsize 480
        ysize 260
        xpos 0.5
        ypos 0.5

        hbox:
            ypos 0.005
            xalign 0.52 
            text "Music Settings":
                color "#000"
                outlines[]
                size 24

        hbox:
            ypos 0.005
            xalign 0.98
            textbutton "X":
                text_style "navigation_button_text"
                action Hide("music_settings")

        side "c":
            xpos 0.05
            ypos 0.2
            xsize 460
            ysize 200

            viewport id "mlt":
                mousewheel True
                scrollbars "vertical"
                has vbox
                
                
                textbutton "Compact Mode":
                    style_prefix "radio" 
                    action ToggleVariable("persistent.listui", False, True)
                textbutton "About DDLC OST-Player":
                    text_style "navigation_button_text" 
                    action Show("dialog", message="DDLC OST-Player by GanstaKingofSA.\nCopyright 2020-2022 GanstaKingofSA. All rights reserved.", 
                        ok_action=Hide("dialog"))

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
    color "#000"
    hover_outlines [(4, "#9b9b9b", 2, 2)]
    outlines []
    size 18
    bold True

style music_player_alt_list_author_text is music_player_alt_list_title_text:
    size 16
    hover_outlines []
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
