
init -1:
    default persistent.old_ui = False

image readablePos = DynamicDisplayable(renpy.curry(music_pos)("song_progress"))
image readableDur = DynamicDisplayable(renpy.curry(music_dur)("song_progress")) 
image titleName = DynamicDisplayable(renpy.curry(dynamic_title_text)("music_player_music_text")) 
image authorName = DynamicDisplayable(renpy.curry(dynamic_author_text)("music_player_song_author_text")) 
image coverArt = DynamicDisplayable(refresh_cover_data) 
image songDescription = DynamicDisplayable(renpy.curry(dynamic_description_text)("music_player_song_author_text")) 
image rpa_map_warning = DynamicDisplayable(renpy.curry(rpa_mapping_detection)("music_player_song_author_text"))
image playPauseButton = DynamicDisplayable(auto_play_pause_button)

screen music_player:

    tag menu

    add "game_menu_bg"
    add "gui/overlay/main_menu.png"
    
    default bar_val = AdjustableAudioPositionValue()

    side "c l":
        
        viewport id "vpo":
            style "music_player_viewport"
            mousewheel True

            child_size (210, 600)

            xpos 20
            ypos 20

            has vbox    
            spacing gui.navigation_spacing
            for st in soundtracks:
                textbutton "[st.name]":
                    style "l_list"
                    text_style "music_navigation_button_text"
                    if current_soundtrack:
                        action [SensitiveIf(current_soundtrack.name != st.name), SetVariable("current_soundtrack", st), Play("music_player", st.path, loop=loopSong, fadein=2.0)]
                    else:
                        action [SetVariable("current_soundtrack", st), Play("music_player", st.path, loop=loopSong, fadein=2.0)]

        vbar value YScrollValue("vpo") xpos 1.0 ypos 20

    if current_soundtrack:
        if current_soundtrack.cover_art:
            if persistent.old_ui:
                add "coverArt" at cover_art_fade(500, 200)
            else:
                add "coverArt" at cover_art_fade(505, 300)

        hbox:
            if persistent.old_ui:
                style "play_pause_buttonO_hbox"
            else:
                style "play_pause_buttonN_hbox"
            imagebutton:
                idle "mod_assets/music_player/backward.png"
                action [SensitiveIf(renpy.music.is_playing(channel='music_player')), Function(current_music_backward)]

            add "playPauseButton"

            imagebutton:
                idle "mod_assets/music_player/forward.png"
                action [SensitiveIf(renpy.music.is_playing(channel='music_player')), Function(current_music_forward)]
        hbox:
            if persistent.old_ui:
                style "music_optionsO_hbox"
            else:
                style "music_optionsN_hbox"
            imagebutton:
                idle ConditionSwitch("organizeAZ", "mod_assets/music_player/A-ZOn.png", "True", "mod_assets/music_player/A-Z.png")
                action [ToggleVariable("organizeAZ", False, True), Function(resort)]
            imagebutton:
                idle ConditionSwitch("organizePriority", "mod_assets/music_player/priorityOn.png", "True", "mod_assets/music_player/priority.png")
                action [ToggleVariable("organizePriority", False, True), Function(resort)]
            imagebutton:
                idle ConditionSwitch("loopSong", "mod_assets/music_player/replayOn.png", "True", "mod_assets/music_player/replay.png")
                action [ToggleVariable("loopSong", False, True), Function(current_music_play)]
            imagebutton:
                idle ConditionSwitch("randomSong", "mod_assets/music_player/shuffleOn.png", "True", "mod_assets/music_player/shuffle.png")
                action [ToggleVariable("randomSong", False, True)]
            if not persistent.old_ui:
                imagebutton:
                    idle "mod_assets/music_player/refreshList.png"
                    action [Function(refresh_list)]
                imagebutton:
                    idle ConditionSwitch("persistent.old_ui", "mod_assets/music_player/OldUI.png", "True", "mod_assets/music_player/NewUI.png")
                    action [ToggleField(persistent, "old_ui", False, True)]
        if persistent.old_ui:
            hbox:
                style "music_options_hboxB"
                imagebutton:
                    idle "mod_assets/music_player/refreshList.png"
                    action [Function(refresh_list)]
                imagebutton:
                    idle ConditionSwitch("persistent.old_ui", "mod_assets/music_player/OldUI.png", "True", "mod_assets/music_player/NewUI.png")
                    action [ToggleField(persistent, "old_ui", False, True)]

        bar:
            if persistent.old_ui:
                xsize 500
            else:
                xsize 710
            value bar_val
            hovered bar_val.hovered
            unhovered bar_val.unhovered
            if persistent.old_ui:
                style "music_player_timeO_bar"
            else:
                style "music_player_timeN_bar"

        if current_soundtrack.author:
            vbox:
                if persistent.old_ui:
                    xoffset 330 
                    yoffset 390

                    hbox: 
                        box_wrap True 
                        vbox:
                            style_prefix "playerO"
                            add "titleName"
                        vbox:
                            style_prefix "playerBO"
                            add "authorName" xpos 6
                else:
                    xoffset 700
                    yoffset 208

                    hbox:
                        vbox:
                            if persistent.old_ui:    
                                style_prefix "playerO"
                            else:
                                style_prefix "playerO"
                            add "titleName"
                    hbox:
                        vbox:
                            style_prefix "playerBN"
                            add "authorName" xpos 6 ypos -3
                    hbox:
                        vbox:
                            style_prefix "playerCN"
                            if current_soundtrack.description:
                                add "songDescription" xpos 6
        
        if persistent.old_ui:
            if current_soundtrack.description:
                viewport id "desc":
                    mousewheel True
                    xpos 640
                    ypos 520
                    xsize 580
                    xfill True
                    style "music_player_description_viewport"
                    add "songDescription"
                vbar value YScrollValue("desc") xpos 1250 ypos 470 ysize 200
        
        if persistent.old_ui:
            bar value Preference ("music_player_mixer volume") style "music_player_volumeO_bar"
        else:
            bar value Preference ("music_player_mixer volume") style "music_player_volumeN_bar"

        imagebutton:
            if persistent.old_ui:
                style "volume_optionsO_hbox"
            else:
                style "volume_optionsN_hbox"
            idle ConditionSwitch("preferences.get_volume(\"music_player_mixer\") == 0.0", "mod_assets/music_player/volume.png", "True", "mod_assets/music_player/volumeOn.png")
            action [Function(mute_player)]

        if current_soundtrack:
            if persistent.old_ui:
                add "readablePos" xpos 540 ypos 480
                add "readableDur" xpos 620 ypos 480
            else:
                add "readablePos" xpos 330 ypos 540
                add "readableDur" xpos 970 ypos 540

    text "DDLC OST-Player v[ostVersion]":
        xalign 1.0 yalign 1.0
        xoffset -10 yoffset -10
        style "main_menu_version"
    
    if not renpy.config.developer:
        add "rpa_map_warning" xpos 0.23 ypos 0.9

    textbutton _("Return"):
        style "return_button"

        action [Return(), If(pausedstate, true=None, false=Function(current_music_pause)), If(prevTrack == False, true=None, false=Play('music', prevTrack, fadein=2.0))]

#transform for the cover art
transform cover_art_fade(x,y):
    anchor(0.5, 0.5)
    pos(x, y)
    size(350,350) # adjusts so any cover art is 350x350
    alpha 0
    linear 0.2 alpha 1

#play and pause button position
style play_pause_buttonO_hbox:
    pos (335, 520)
    spacing 25

#controls music options position
style music_optionsO_hbox:
    pos (335, 570)
    spacing 25

#controls volume position
style volume_optionsO_hbox:
    pos (323, 481)
 
# controls title formatting
style playerO_vbox:
    xsize 510
    xfill True

# controls artist formatting
style playerBO_vbox: 
    xsize 430
    xfill True 

#the slider that indicates how far music is
style music_player_timeO_bar:
    xsize 900
    pos (320, 460)
    thumb "gui/slider/horizontal_hover_thumb.png"

#slider that controls player music sound
style music_player_volumeO_bar:
    xsize 150
    pos (373, 490)
    thumb "gui/slider/horizontal_hover_thumb.png"

#controls music control position (New UI)
style play_pause_buttonN_hbox:
    pos (715, 410)
    spacing 25

#controls music options position (New UI)
style music_optionsN_hbox:
    pos (715, 450)
    spacing 25

#controls volume position (New UI)
style volume_optionsN_hbox:
    pos (1075, 507)

#controls title formatting (New UI)
style playerN_vbox: 
    xsize 580
    xfill True

#controls artist formatting (New UI)
style playerBN_vbox: 
    xsize 580
    xfill True

style playerCN_vbox: 
    xsize 580
    xfill True

#the slider that indicates how far music is
style music_player_timeN_bar:
    xsize 400
    pos (330, 520)
    thumb "gui/slider/horizontal_hover_thumb.png"

#slider that controls player music sound
style music_player_volumeN_bar:
    xsize 120
    pos (1130, 520)
    thumb "gui/slider/horizontal_hover_thumb.png"

#style that handles additional buttons in the Old UI
style music_options_hboxB:
    pos (335, 610)
    spacing 25

# default responsible for other l_ info
style l_default:
    font gui.default_font
    #font "mod_assets/music_player/riffic-bold.ttf"
    size 18
    color gui.text_color
    outlines [(2, "#000000aa", 0, 0)]
    line_overlap_split 1
    line_spacing 1

# controls list formatting
style l_list is l_default: 
    left_padding 20
    size 16
    xfill True

#style for the list buttons
style music_navigation_button_text:
    font "gui/font/RifficFree-Bold.ttf"
    #font "mod_assets/music_player/riffic-bold.ttf"
    color "#fff"
    outlines [(4, "#b59", 0, 0), (2, "#b59", 2, 2)]
    hover_outlines [(4, "#fac", 0, 0), (2, "#fac", 2, 2)]
    insensitive_outlines [(4, "#fce", 0, 0), (2, "#fce", 2, 2)]

#style for the name of the music that appears when it is playing
style music_player_music_text:
    font "gui/font/RifficFree-Bold.ttf"
    #font "mod_assets/music_player/riffic-bold.ttf"
    color "#000"
    outlines [(0, "#000", 0, 0)]
    size 36

#style for author of the music
style music_player_song_author_text is music_player_description_text
style music_player_song_author_text:
    font "mod_assets/music_player/NotoSansSC-Light.otf"
    size 22
    outlines[]
    color "#000"

# halogen for time progress
style song_progress:
    font "gui/font/Halogen.ttf"
    size 25
    outlines[]
    color "#000"

#style for viewport where description shows
style music_player_description_viewport:
    xsize 600
    ysize 200

#style for description text
style music_player_description_text:
    font "mod_assets/music_player/NotoSansSC-Light.otf"
    size 24
    outlines[]
    color "#000"

#style for the scrollable music list 
style music_player_viewport:
    xsize 210
    ysize 600
